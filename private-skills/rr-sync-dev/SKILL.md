---
name: rr-sync-dev
description: Use when syncing local project files to a configured development server through the rr Zsh function, or when rr produces unexpected results.
---

# rr — rsync sync to remote development

One-way `rsync` push from a local working tree to a configured development
server.

- **Remote**: `$RR_REMOTE_HOST`
- **Destination**: `$RR_REMOTE_PROJECT_ROOT/<PROJECT>`
- **Default project**: `$RR_DEFAULT_PROJECT`

Set these values from the ignored `.local/skills-environment.yaml` inventory
before sourcing the function. Do not commit the resolved host or path.

## Usage

```zsh
# Explicit files or directories
rr chemin/vers/fichier.php autre/dossier/

# Change project (first arg = project name under <remote-project-root>)
rr tmgmt chemin/vers/fichier.php

# No args: sync everything from git status
rr
```

## Behaviour

1. **First arg** → project name under `<remote-project-root>` (default from
   `$RR_DEFAULT_PROJECT`). Remaining args → file list.
2. **No file args** → file list built from `git status --porcelain`.
3. File list is printed, then confirmation prompt `(y/N)` — only `y`/`Y` proceeds.
4. Each file synced with `rsync -avz`:
   - **Directory** → contents synced (`trailing /` on source).
   - **File** → direct sync.
   - **Missing locally** → skipped with `⚠️ Missing:` (e.g. deleted files from git status — deletions are NOT propagated).

## Pitfalls

- Paths are relative to the **current directory**. Run from repo root so git paths match the remote tree.
- Sync is **one-way** (local → remote), no `--delete`. Deleted local files are NOT removed remotely.
- For bidirectional sync, use a dedicated bidirectional synchronisation tool.

## Installation

Sourced from `~/.zshrc`:

```zsh
source ~/.claude/skills/rr-sync-dev/rr.zsh
```

## Diagnostics

| Symptom | Likely cause |
|---------|-------------|
| `⚠️ Missing: …` | File listed by git status was deleted locally; sync does not propagate deletions |
| `ssh: Could not resolve hostname` | `$RR_REMOTE_HOST` is wrong or unavailable |
| `rsync: change_dir … failed` | Project directory does not exist under `$RR_REMOTE_PROJECT_ROOT` |
