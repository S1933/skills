---
name: rr-sync-dev
description: Use when syncing local project files to gw2sdev-docker dev server via the rr zsh function, or when rr produces unexpected results
---

# rr — rsync sync to SDEV

One-way `rsync` push from local working tree to `gw2sdev-docker.ovh.net` over the sshfs OCMS mount.

- **Remote**: `gw2sdev-docker.ovh.net`
- **Destination**: `/home/jnuel/sshfs/<PROJECT>` (default: `ocms`)

## Usage

```zsh
# Explicit files or directories
rr chemin/vers/fichier.php autre/dossier/

# Change project (first arg = project name under /home/jnuel/sshfs/)
rr tmgmt chemin/vers/fichier.php

# No args: sync everything from git status
rr
```

## Behaviour

1. **First arg** → project name under `/home/jnuel/sshfs/` (default `ocms`). Remaining args → file list.
2. **No file args** → file list built from `git status --porcelain`.
3. File list is printed, then confirmation prompt `(y/N)` — only `y`/`Y` proceeds.
4. Each file synced with `rsync -avz`:
   - **Directory** → contents synced (`trailing /` on source).
   - **File** → direct sync.
   - **Missing locally** → skipped with `⚠️ Missing:` (e.g. deleted files from git status — deletions are NOT propagated).

## Pitfalls

- Paths are relative to the **current directory**. Run from repo root so git paths match the remote tree.
- Sync is **one-way** (local → remote), no `--delete`. Deleted local files are NOT removed remotely.
- For bidirectional sync, use **Unison** (see OCMS technical notes).

## Installation

Sourced from `~/.zshrc`:

```zsh
source ~/.claude/skills/rr-sync-dev/rr.zsh
```

## Diagnostics

| Symptom | Likely cause |
|---------|-------------|
| `⚠️ Missing: …` | File listed by git status was deleted locally; sync does not propagate deletions |
| `ssh: Could not resolve hostname` | SSH connection to `gw2sdev-docker.ovh.net` unavailable |
| `rsync: change_dir … failed` | Project directory doesn't exist under `/home/jnuel/sshfs/` |
