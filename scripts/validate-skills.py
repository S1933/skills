#!/usr/bin/env python3
"""Validate the structure, metadata, references, and examples of all skills."""

from __future__ import annotations

import argparse
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import NamedTuple

import yaml


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
FENCED_EXAMPLE = re.compile(r"```(json|ya?ml|dot)\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
FENCED_CODE = re.compile(
    r"^(?P<fence>`{3,})[^\n]*\n.*?^(?P=fence)\s*$",
    re.DOTALL | re.MULTILINE,
)
LEGACY_ALIAS_REFERENCE = re.compile(
    r"\b(?:use|using|via|unlike|invoke|invoking|runs?)\s+/([a-z][a-z0-9-]*)",
    re.IGNORECASE,
)
PRIVATE_PATTERNS = (
    re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+"),
    re.compile(r"~/(?:Projects|go)/"),
    re.compile(r"\b[A-Za-z0-9.-]+\.internal(?:\.[A-Za-z0-9.-]+)?\b", re.IGNORECASE),
    re.compile(r"\b[A-Za-z0-9.-]+\.corp\b", re.IGNORECASE),
    re.compile(r"\b[A-Za-z0-9.-]+\.k8s\.[A-Za-z0-9.-]+\b", re.IGNORECASE),
    re.compile(r"\b[A-Za-z0-9.-]*sdev[A-Za-z0-9.-]*\.[A-Za-z]{2,}\b", re.IGNORECASE),
    re.compile(r"\b[A-Za-z0-9.-]+\.ovh\.net\b", re.IGNORECASE),
)
SUPPORTED_FRONTMATTER_TYPES = {
    "name": str,
    "description": str,
    "disable-model-invocation": bool,
    "argument-hint": str,
    "license": str,
    "compatibility": str,
    "metadata": dict,
    "allowed-tools": (str, list),
}


class Diagnostic(NamedTuple):
    code: str
    path: str
    line: int
    message: str
    severity: str = "error"


def diagnostic(
    code: str,
    path: Path | str,
    message: str,
    *,
    line: int = 1,
    severity: str = "error",
) -> Diagnostic:
    return Diagnostic(code, Path(path).as_posix(), line, message, severity)


def load_yaml(path: Path, code: str, diagnostics: list[Diagnostic]):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        diagnostics.append(diagnostic(code, path, str(error).splitlines()[0]))
        return None


def parse_frontmatter(path: Path, diagnostics: list[Diagnostic]):
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        diagnostics.append(diagnostic("E001_SKILL_FILE_MISSING", path, str(error)))
        return None, ""

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        diagnostics.append(
            diagnostic("E002_FRONTMATTER_MISSING", path, "SKILL.md must begin with YAML frontmatter")
        )
        return None, text

    closing = next((index for index, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if closing is None:
        diagnostics.append(
            diagnostic("E002_FRONTMATTER_MISSING", path, "frontmatter closing delimiter is missing")
        )
        return None, text

    frontmatter_text = "".join(lines[1:closing])
    if len(frontmatter_text.encode("utf-8")) > 1024:
        diagnostics.append(
            diagnostic("E009_FRONTMATTER_SIZE", path, "frontmatter exceeds 1024 bytes")
        )
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as error:
        problem_line = getattr(getattr(error, "problem_mark", None), "line", 0) + 2
        diagnostics.append(
            diagnostic(
                "E003_FRONTMATTER_YAML",
                path,
                str(error).splitlines()[0],
                line=problem_line,
            )
        )
        return None, text
    if not isinstance(frontmatter, dict):
        diagnostics.append(
            diagnostic("E003_FRONTMATTER_YAML", path, "frontmatter must decode to a mapping")
        )
        return None, text
    return frontmatter, text


def validate_frontmatter(
    path: Path,
    frontmatter: dict[str, object],
    manifest_entry: dict[str, object],
    diagnostics: list[Diagnostic],
) -> None:
    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if not isinstance(name, str) or not name:
        diagnostics.append(diagnostic("E004_NAME_REQUIRED", path, "name is required and must be a string"))
    else:
        if not NAME_PATTERN.fullmatch(name):
            diagnostics.append(diagnostic("E007_NAME_FORMAT", path, f"invalid skill name: {name}"))
        if name != path.parent.name:
            diagnostics.append(
                diagnostic(
                    "E006_NAME_MISMATCH",
                    path,
                    f"frontmatter name {name!r} does not match directory {path.parent.name!r}",
                )
            )

    if not isinstance(description, str) or not description.strip():
        diagnostics.append(
            diagnostic("E005_DESCRIPTION_REQUIRED", path, "description is required and must be a string")
        )
    else:
        if not description.startswith("Use when"):
            diagnostics.append(
                diagnostic("E010_DESCRIPTION_TRIGGER", path, "description must start with 'Use when'")
            )
        if len(description) > 500:
            diagnostics.append(
                diagnostic(
                    "E011_DESCRIPTION_LENGTH",
                    path,
                    f"description is {len(description)} characters; maximum is 500",
                )
            )
        manifest_description = manifest_entry.get("description")
        if isinstance(manifest_description, str) and manifest_description != description:
            diagnostics.append(
                diagnostic(
                    "E036_MANIFEST_DESCRIPTION_MISMATCH",
                    path,
                    "manifest description does not match SKILL.md frontmatter",
                )
            )

    for key, value in frontmatter.items():
        expected = SUPPORTED_FRONTMATTER_TYPES.get(key)
        if expected is not None and not isinstance(value, expected):
            code = "E008_DISABLE_INVOCATION_TYPE" if key == "disable-model-invocation" else "E022_METADATA_TYPE"
            diagnostics.append(
                diagnostic(code, path, f"frontmatter field {key!r} has an unsupported type")
            )

    invocation = manifest_entry.get("invocation")
    expected_invocation = "manual" if frontmatter.get("disable-model-invocation") is True else "automatic"
    if invocation and invocation != expected_invocation:
        diagnostics.append(
            diagnostic(
                "E022_METADATA_TYPE",
                path,
                f"manifest invocation {invocation!r} does not match frontmatter {expected_invocation!r}",
            )
        )

    clients = manifest_entry.get("clients", ["agent-skills"])
    if isinstance(clients, list) and any(client != "agent-skills" for client in clients):
        compatibility = frontmatter.get("compatibility")
        if not isinstance(compatibility, str) or not compatibility.strip():
            diagnostics.append(
                diagnostic(
                    "E026_COMPATIBILITY_REQUIRED",
                    path,
                    "non-portable skills must declare frontmatter compatibility",
                )
            )


def markdown_files(skill_directory: Path) -> list[Path]:
    return sorted(path for path in skill_directory.rglob("*.md") if "__pycache__" not in path.parts)


def validate_links(path: Path, root: Path, diagnostics: list[Diagnostic]) -> None:
    text = path.read_text(encoding="utf-8")
    searchable = FENCED_CODE.sub(
        lambda match: "".join("\n" if character == "\n" else " " for character in match.group()),
        text,
    )
    for match in MARKDOWN_LINK.finditer(searchable):
        raw_target = match.group(1).strip()
        target = raw_target.strip("<>").split(maxsplit=1)[0]
        if target.startswith(("http://", "https://", "mailto:", "#", "/")):
            continue
        relative_target = target.split("#", 1)[0]
        if not relative_target:
            continue
        destination = (path.parent / relative_target).resolve()
        if not destination.exists():
            line = text.count("\n", 0, match.start()) + 1
            diagnostics.append(
                diagnostic(
                    "E013_BROKEN_LINK",
                    path.relative_to(root),
                    f"relative link does not resolve: {target}",
                    line=line,
                )
            )


def validate_content(
    path: Path,
    root: Path,
    visibility: str,
    known_names: set[str],
    known_aliases: set[str],
    word_budget: int | None,
    diagnostics: list[Diagnostic],
) -> None:
    text = path.read_text(encoding="utf-8")
    relative_path = path.relative_to(root)

    if visibility == "public":
        for pattern in PRIVATE_PATTERNS:
            match = pattern.search(text)
            if match:
                diagnostics.append(
                    diagnostic(
                        "E018_PRIVATE_LITERAL",
                        relative_path,
                        f"public skill contains a private path or hostname matching {pattern.pattern!r}",
                        line=text.count("\n", 0, match.start()) + 1,
                    )
                )
                break

    if "--dangerously-bypass-approvals-and-sandbox" in text:
        elevated = text.find("## Elevated execution")
        bypass = text.find("--dangerously-bypass-approvals-and-sandbox")
        if elevated < 0 or bypass < elevated:
            diagnostics.append(
                diagnostic(
                    "E019_DANGEROUS_EXAMPLE",
                    relative_path,
                    "sandbox bypass appears outside an Elevated execution warning",
                    line=text.count("\n", 0, bypass) + 1,
                )
            )

    for match in LEGACY_ALIAS_REFERENCE.finditer(text):
        alias = match.group(1)
        if alias not in known_names and alias not in known_aliases:
            diagnostics.append(
                diagnostic(
                    "E016_ALIAS_UNKNOWN",
                    relative_path,
                    f"slash-command alias is not declared: /{alias}",
                    line=text.count("\n", 0, match.start()) + 1,
                )
            )

    word_count = len(text.split())
    effective_word_budget = word_budget or 800
    if path.name == "SKILL.md" and word_count > effective_word_budget:
        diagnostics.append(
            diagnostic(
                "E035_WORD_BUDGET",
                relative_path,
                f"main skill contains approximately {word_count} words; budget is {effective_word_budget}",
            )
        )


def validate_examples(path: Path, root: Path, diagnostics: list[Diagnostic]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    dot_blocks: list[str] = []
    for match in FENCED_EXAMPLE.finditer(text):
        language = match.group(1).lower()
        body = match.group(2)
        line = text.count("\n", 0, match.start()) + 1
        try:
            if language == "json":
                json.loads(body)
            elif language in {"yaml", "yml"}:
                yaml.safe_load(body)
            else:
                dot_blocks.append(body)
        except (json.JSONDecodeError, yaml.YAMLError) as error:
            code = "E030_JSON_EXAMPLE" if language == "json" else "E031_YAML_EXAMPLE"
            diagnostics.append(
                diagnostic(code, path.relative_to(root), str(error).splitlines()[0], line=line)
            )
    return dot_blocks


def validate_graphviz(
    blocks: list[tuple[Path, str]], root: Path, diagnostics: list[Diagnostic]
) -> None:
    dot = shutil.which("dot")
    if not blocks:
        return
    if dot is None:
        diagnostics.append(
            diagnostic(
                "W002_OPTIONAL_TOOL",
                root,
                "Graphviz 'dot' is unavailable; diagram compilation was skipped",
                severity="warning",
            )
        )
        return
    for path, body in blocks:
        result = subprocess.run(
            [dot, "-Tsvg"],
            input=body,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            diagnostics.append(
                diagnostic(
                    "E032_GRAPHVIZ",
                    path.relative_to(root),
                    result.stderr.strip().splitlines()[0],
                )
            )


def validate_shell_scripts(skill_directories: list[Path], root: Path, diagnostics: list[Diagnostic]) -> None:
    scripts = sorted(
        path
        for directory in skill_directories
        for path in directory.rglob("*.sh")
        if path.is_file()
    )
    for script in scripts:
        result = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            diagnostics.append(
                diagnostic(
                    "E033_SHELL_SYNTAX",
                    script.relative_to(root),
                    result.stderr.strip().splitlines()[0],
                )
            )

    shellcheck = shutil.which("shellcheck")
    if scripts and shellcheck is None:
        diagnostics.append(
            diagnostic(
                "W002_OPTIONAL_TOOL",
                root,
                "ShellCheck is unavailable; shell linting was skipped",
                severity="warning",
            )
        )
        return
    for script in scripts:
        result = subprocess.run(
            [shellcheck, str(script)], capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            diagnostics.append(
                diagnostic(
                    "E034_SHELLCHECK",
                    script.relative_to(root),
                    result.stdout.strip().splitlines()[0],
                )
            )


def dependency_cycles(entries: list[dict[str, object]]) -> list[list[str]]:
    graph = {
        str(entry.get("name")): [str(item) for item in entry.get("requires_skills", [])]
        for entry in entries
    }
    state: dict[str, int] = {}
    stack: list[str] = []
    cycles: list[list[str]] = []

    def visit(name: str) -> None:
        state[name] = 1
        stack.append(name)
        for dependency in graph.get(name, []):
            if dependency not in graph:
                continue
            if state.get(dependency, 0) == 0:
                visit(dependency)
            elif state.get(dependency) == 1:
                start = stack.index(dependency)
                cycles.append(stack[start:] + [dependency])
        stack.pop()
        state[name] = 2

    for name in sorted(graph):
        if state.get(name, 0) == 0:
            visit(name)
    return cycles


def clients_are_compatible(
    requiring_entry: dict[str, object], required_entry: dict[str, object]
) -> bool:
    """Return whether a required skill is available to at least one caller client."""
    requiring_clients = {
        client for client in requiring_entry.get("clients", []) if isinstance(client, str)
    }
    required_clients = {
        client for client in required_entry.get("clients", []) if isinstance(client, str)
    }
    return "agent-skills" in required_clients or bool(requiring_clients & required_clients)


def validate_dependency_contracts(
    entries: list[dict[str, object]], manifest_path: Path, diagnostics: list[Diagnostic]
) -> None:
    entries_by_name = {
        entry["name"]: entry for entry in entries if isinstance(entry.get("name"), str)
    }
    for entry in entries:
        name = entry.get("name")
        if not isinstance(name, str):
            continue
        notes = entry.get("dependency_notes", {})
        if not isinstance(notes, dict):
            diagnostics.append(
                diagnostic(
                    "E042_MANIFEST_SCHEMA",
                    manifest_path,
                    f"{name}.dependency_notes must be a mapping",
                )
            )
            notes = {}

        for dependency_name in entry.get("requires_skills", []):
            if not isinstance(dependency_name, str):
                continue
            dependency = entries_by_name.get(dependency_name)
            if dependency is None:
                continue

            explanation = notes.get(dependency_name)
            if (
                entry.get("invocation") == "automatic"
                and dependency.get("invocation") == "manual"
                and (not isinstance(explanation, str) or not explanation.strip())
            ):
                diagnostics.append(
                    diagnostic(
                        "E028_MANUAL_DEPENDENCY",
                        manifest_path,
                        f"automatic skill {name!r} requires manual skill {dependency_name!r} "
                        "without a dependency_notes explanation",
                    )
                )

            if not clients_are_compatible(entry, dependency):
                diagnostics.append(
                    diagnostic(
                        "E029_INCOMPATIBLE_DEPENDENCY",
                        manifest_path,
                        f"{name!r} and required skill {dependency_name!r} have no compatible client",
                    )
                )


def apply_exceptions(root: Path, diagnostics: list[Diagnostic]) -> list[Diagnostic]:
    path = root / "validation-exceptions.yaml"
    if not path.exists():
        return diagnostics
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    exception_map = {
        (item.get("code"), item.get("path")): item.get("reason", "temporary exception")
        for item in data.get("exceptions", [])
        if isinstance(item, dict)
    }
    result=[]
    for item in diagnostics:
        reason = exception_map.get((item.code, item.path))
        if reason and item.severity == "error":
            result.append(item._replace(severity="warning", message=f"{item.message}; exception: {reason}"))
        else:
            result.append(item)
    return result


def validate_catalogue(root: Path | str) -> list[Diagnostic]:
    root = Path(root).resolve()
    diagnostics: list[Diagnostic] = []
    manifest_path = root / "skills-manifest.yaml"
    if not manifest_path.exists():
        return [diagnostic("E040_MANIFEST_MISSING", manifest_path, "skills-manifest.yaml is required")]
    manifest = load_yaml(manifest_path, "E041_MANIFEST_YAML", diagnostics)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("skills"), list):
        diagnostics.append(
            diagnostic("E042_MANIFEST_SCHEMA", manifest_path, "manifest skills must be a list")
        )
        return diagnostics

    entries = [entry for entry in manifest["skills"] if isinstance(entry, dict)]
    names = [entry.get("name") for entry in entries if isinstance(entry.get("name"), str)]
    known_names = set(names)
    aliases = [
        alias
        for entry in entries
        for alias in entry.get("aliases", [])
        if isinstance(alias, str)
    ]
    known_aliases = set(aliases)
    for name in sorted(set(names)):
        if names.count(name) > 1:
            diagnostics.append(
                diagnostic("E012_DUPLICATE_NAME", manifest_path, f"duplicate skill name: {name}")
            )
    for alias in sorted(set(aliases)):
        if aliases.count(alias) > 1 or alias in known_names:
            diagnostics.append(
                diagnostic("E016_ALIAS_UNKNOWN", manifest_path, f"duplicate or conflicting alias: {alias}")
            )

    skill_directories: list[Path] = []
    descriptions: list[tuple[str, str, Path]] = []
    graphviz_blocks: list[tuple[Path, str]] = []
    listed_paths: set[str] = set()
    for entry in entries:
        raw_path = entry.get("path")
        name = entry.get("name")
        if not isinstance(raw_path, str) or not isinstance(name, str):
            diagnostics.append(
                diagnostic("E042_MANIFEST_SCHEMA", manifest_path, "each skill needs string name and path")
            )
            continue
        listed_paths.add(raw_path)
        skill_directory = root / raw_path
        skill_directories.append(skill_directory)
        skill_file = skill_directory / "SKILL.md"
        if not skill_file.exists():
            diagnostics.append(
                diagnostic("E001_SKILL_FILE_MISSING", skill_file, "manifest path has no SKILL.md")
            )
            continue
        if skill_file.is_symlink() and not skill_file.resolve().is_relative_to(root):
            diagnostics.append(
                diagnostic(
                    "E027_SYMLINK_OUTSIDE",
                    skill_file.relative_to(root),
                    f"skill symlink escapes repository: {skill_file.readlink()}",
                )
            )
            continue

        frontmatter, skill_text = parse_frontmatter(skill_file, diagnostics)
        actual_word_count = len(skill_text.split())
        declared_word_count = entry.get("approximate_word_count")
        if (
            not isinstance(declared_word_count, int)
            or isinstance(declared_word_count, bool)
            or declared_word_count < 0
        ):
            diagnostics.append(
                diagnostic(
                    "E042_MANIFEST_SCHEMA",
                    manifest_path,
                    f"{name}.approximate_word_count must be a non-negative integer",
                )
            )
        elif abs(declared_word_count - actual_word_count) > max(
            5, round(actual_word_count * 0.05)
        ):
            diagnostics.append(
                diagnostic(
                    "E037_MANIFEST_WORD_COUNT_STALE",
                    manifest_path,
                    f"{name}.approximate_word_count is {declared_word_count}; current count is {actual_word_count}",
                )
            )
        if frontmatter is not None:
            validate_frontmatter(skill_file.relative_to(root), frontmatter, entry, diagnostics)
            description = frontmatter.get("description")
            if isinstance(description, str):
                descriptions.append((name, description, skill_file.relative_to(root)))

        for supporting in entry.get("supporting_files", []):
            supporting_path = root / supporting if isinstance(supporting, str) else None
            if supporting_path is not None and not supporting_path.exists():
                diagnostics.append(
                    diagnostic(
                        "E014_SUPPORTING_FILE_MISSING",
                        manifest_path,
                        f"supporting file does not exist: {supporting}",
                    )
                )
            elif (
                supporting_path is not None
                and supporting_path.is_symlink()
                and not supporting_path.resolve().is_relative_to(root)
            ):
                diagnostics.append(
                    diagnostic(
                        "E027_SYMLINK_OUTSIDE",
                        supporting_path.relative_to(root),
                        f"supporting-file symlink escapes repository: {supporting_path.readlink()}",
                    )
                )

        visibility = str(entry.get("visibility", "public"))
        raw_word_budget = entry.get("word_budget")
        word_budget = (
            raw_word_budget
            if isinstance(raw_word_budget, int) and not isinstance(raw_word_budget, bool) and raw_word_budget > 0
            else None
        )
        if raw_word_budget is not None and word_budget is None:
            diagnostics.append(
                diagnostic(
                    "E042_MANIFEST_SCHEMA",
                    manifest_path,
                    f"{name}.word_budget must be a positive integer",
                )
            )
        for markdown in markdown_files(skill_directory):
            validate_links(markdown, root, diagnostics)
            validate_content(
                markdown,
                root,
                visibility,
                known_names,
                known_aliases,
                word_budget,
                diagnostics,
            )
            graphviz_blocks.extend((markdown, block) for block in validate_examples(markdown, root, diagnostics))

        for field in ("requires_skills", "optional_skills", "referenced_skills"):
            for dependency in entry.get(field, []):
                if isinstance(dependency, str) and dependency not in known_names:
                    diagnostics.append(
                        diagnostic(
                            "E015_SKILL_DEPENDENCY_MISSING",
                            manifest_path,
                            f"{name}.{field} references missing skill {dependency!r}",
                        )
                    )

    discovered = {
        path.parent.relative_to(root).as_posix()
        for pattern in ("*/SKILL.md", "private-skills/*/SKILL.md")
        for path in root.glob(pattern)
    }
    for unlisted in sorted(discovered - listed_paths):
        diagnostics.append(
            diagnostic("E021_MANIFEST_ENTRY_MISSING", root / unlisted, "skill is absent from manifest")
        )

    for index, (name, description, path) in enumerate(descriptions):
        for other_name, other_description, other_path in descriptions[index + 1 :]:
            if SequenceMatcher(None, description.lower(), other_description.lower()).ratio() >= 0.98:
                diagnostics.append(
                    diagnostic(
                        "E025_DESCRIPTION_DUPLICATE",
                        path,
                        f"description is nearly identical to {other_name} ({other_path})",
                    )
                )

    validate_dependency_contracts(entries, manifest_path, diagnostics)
    for cycle in dependency_cycles(entries):
        diagnostics.append(
            diagnostic("E023_DEPENDENCY_CYCLE", manifest_path, " -> ".join(cycle))
        )

    validate_shell_scripts(skill_directories, root, diagnostics)
    validate_graphviz(graphviz_blocks, root, diagnostics)
    diagnostics = apply_exceptions(root, diagnostics)
    return sorted(diagnostics, key=lambda item: (item.severity != "error", item.path, item.line, item.code))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--warnings-as-errors", action="store_true")
    arguments = parser.parse_args(argv)

    diagnostics = validate_catalogue(arguments.root)
    for item in diagnostics:
        print(
            f"{item.path}:{item.line}: {item.severity}: [{item.code}] {item.message}",
            file=sys.stderr if item.severity == "error" else sys.stdout,
        )
    errors = sum(item.severity == "error" for item in diagnostics)
    warnings = sum(item.severity == "warning" for item in diagnostics)
    print(f"validated catalogue: {errors} error(s), {warnings} warning(s)")
    return 1 if errors or (arguments.warnings_as_errors and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
