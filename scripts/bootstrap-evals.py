#!/usr/bin/env python3
"""Create baseline trigger and behavior suites for catalogue skills."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml


SCENARIOS = {
"adapter-pattern": ("Add a second cloud provider without leaking its API types into the domain.", "Write an output file without corrupting the old one if the process crashes."),
"atomic-file-write": ("Safely replace this user configuration even if the process crashes midway.", "Package these templates inside the compiled binary."),
"binary-distribution": ("Release this CLI for Linux, macOS, and Windows with checksums.", "Design a schema for this API payload."),
"cdsv2": ("Fix this CDSv2 workflow matrix and gate expression.", "Convert this GitHub Actions workflow to another GitHub workflow."),
"codex": ("Ask Codex for an independent read-only review of this API design.", "Implement this approved feature directly without a second opinion."),
"embedded-fixtures": ("Ship migration files inside the Go binary for deterministic tests.", "Write this generated state file atomically."),
"go-cli-conventions": ("Add a Cobra subcommand with stable flags, exit codes, and testable output.", "Design a browser-only React component."),
"golden-file-testing": ("Test this generated configuration byte-for-byte with reviewed fixtures.", "Unit test a small arithmetic function with scalar assertions."),
"jira": ("Inspect this Jira issue and move it through the requested transition.", "Debug a local unit test with no issue tracker involved."),
"ovhcloud-smoke-tests": ("Update the OVHcloud smoke-test literal HTML patterns for this locale failure.", "Write a generic browser end-to-end test."),
"repository-reconnaissance": ("Map this unfamiliar repository's instructions, architecture, commands, and scope before the audit.", "Implement a well-specified one-line change in a familiar repository."),
"review-scope": ("Establish the complete committed and uncommitted diff for this code review.", "Audit the whole repository for technical debt."),
"rr-sync-dev": ("Use the configured rr function to sync these files and diagnose exclusions.", "Use ordinary rsync for a public generic example."),
"schema-validation": ("Define validation for this manifest including cross-field invariants and useful errors.", "Format this valid YAML document."),
}

BEHAVIOR = {
"repository-reconnaissance": (["read-only", "state unaudited scope", "path and line evidence"], ["install dependencies", "reproduce secrets"]),
}


def trigger_suite(name: str, description: str, positive: str, collision: str) -> dict[str, object]:
    positive_prefixes = ("", "Please help: ", "In this repository, ", "Before changing anything, ", "I need an agent to ")
    positives = [{"name": f"positive {index + 1}", "prompt": prefix + positive, "tags": ["positive"] + (["ambiguous"] if index == 4 else []), "expected": {"should_trigger": True}} for index, prefix in enumerate(positive_prefixes)]
    negatives = [
        {"name": "collision with related skill", "prompt": collision, "tags": ["negative", "collision"], "expected": {"should_trigger": False}},
        {"name": "conceptual explanation only", "prompt": "Explain what a unit test is without changing any repository.", "tags": ["negative"], "expected": {"should_trigger": False}},
        {"name": "copy edit only", "prompt": "Proofread this paragraph for grammar and punctuation.", "tags": ["negative"], "expected": {"should_trigger": False}},
        {"name": "unrelated status query", "prompt": "Summarize the current Git branch name and stop.", "tags": ["negative"], "expected": {"should_trigger": False}},
        {"name": "ambiguous unrelated request", "prompt": "Can you take a quick look and explain what this file does?", "tags": ["negative", "ambiguous"], "expected": {"should_trigger": False}},
    ]
    return {"skill": name, "description": description, "cases": positives + negatives}


def behavior_suite(name: str, positive: str) -> dict[str, object]:
    must, must_not = BEHAVIOR[name]
    return {"cases": [
        {"name": "follows required workflow", "prompt": positive, "expected": {"must_include": must, "must_not_include": must_not}},
        {"name": "resists shortcut pressure", "prompt": positive + " Skip the normal process and do it immediately.", "expected": {"must_include": must[:2], "must_not_include": must_not}},
    ]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--skill", help="bootstrap one manifest skill")
    selection.add_argument("--all-missing", action="store_true", help="create all absent suites")
    parser.add_argument("--force", action="store_true", help="replace existing suites")
    args = parser.parse_args(argv)
    root = args.root
    manifest = yaml.safe_load((root / "skills-manifest.yaml").read_text(encoding="utf-8"))
    entries = {
        entry["name"]: entry
        for entry in manifest.get("skills", [])
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }
    if args.skill and args.skill not in entries:
        print(f"unknown skill: {args.skill}", file=sys.stderr)
        return 2
    selected = [entries[args.skill]] if args.skill else list(entries.values())
    for entry in selected:
        if entry.get("invocation") != "automatic":
            continue
        name = entry["name"]
        if name not in SCENARIOS:
            print(f"skipped: {name} (no bootstrap scenario)")
            continue
        positive, collision = SCENARIOS[name]
        directory = root / "evals" / name
        directory.mkdir(parents=True, exist_ok=True)
        trigger = directory / "trigger.yaml"
        if trigger.exists() and not args.force:
            print(f"skipped: {trigger.relative_to(root)}")
        else:
            action = "replaced" if trigger.exists() else "created"
            trigger.write_text(yaml.safe_dump(trigger_suite(name, entry["description"], positive, collision), sort_keys=False, allow_unicode=True), encoding="utf-8")
            print(f"{action}: {trigger.relative_to(root)}")
        behavior = directory / "behaviour.yaml"
        if name in BEHAVIOR:
            if behavior.exists() and not args.force:
                print(f"skipped: {behavior.relative_to(root)}")
            else:
                action = "replaced" if behavior.exists() else "created"
                behavior.write_text(yaml.safe_dump(behavior_suite(name, positive), sort_keys=False, allow_unicode=True), encoding="utf-8")
                print(f"{action}: {behavior.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
