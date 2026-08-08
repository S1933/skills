<!-- Generated from skills-manifest.yaml; do not edit manually. -->

# Generated skill catalogue

## Public skills

### `adapter-pattern`

Use when one domain model must interoperate with multiple external APIs, file formats, providers, CLIs, storage engines, or versioned protocols without leaking vendor details into core logic.

- Path: `adapter-pattern`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 386

### `atomic-file-write`

Use when replacing configuration, state, generated, or user-owned files where crashes, partial writes, permissions, concurrent readers, or durability can corrupt observable state.

- Path: `atomic-file-write`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 408

### `binary-distribution`

Use when releasing compiled command-line tools across operating systems or architectures, including version metadata, archives, checksums, signing, installers, and reproducible release automation.

- Path: `binary-distribution`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 359

### `codex`

Use when an independent technical second opinion, verification, repository analysis, or deeper library or API research would materially reduce uncertainty.

- Path: `codex`
- Invocation: automatic
- Clients: codex
- Required skills: none
- Optional skills: none
- Commands: codex
- Compatibility: Requires the Codex CLI with exec and sandbox support.
- Main-file words: approximately 333

### `embedded-fixtures`

Use when binaries or tests need deterministic templates, schemas, migrations, defaults, or sample files packaged with the executable through Go embed or an equivalent resource mechanism.

- Path: `embedded-fixtures`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 345

### `go-cli-conventions`

Use when creating, extending, or reviewing Go 1.24+ command-line applications, especially Cobra commands, flags, exit behavior, configuration, and testable CLI boundaries.

- Path: `go-cli-conventions`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 371

### `golden-file-testing`

Use when testing generated text, configuration, serialization, templates, compiler output, or other stable artifacts whose complete shape matters more than isolated fields.

- Path: `golden-file-testing`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 369

### `repository-reconnaissance`

Use when an audit, review, plan, or unfamiliar repository task needs an evidence-based map of instructions, architecture, commands, history, and inspectable scope before conclusions are drawn.

- Path: `repository-reconnaissance`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: git
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 297

### `review-scope`

Use when beginning a code review that must include committed, staged, unstaged, and relevant untracked changes against the correct base.

- Path: `review-scope`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Requires Git repository access.
- Main-file words: approximately 342

### `scaleflex-api`

Use when integrating the Scaleflex, Filerobot, or Cloudimage API — searching DAM assets by metadata, uploading files, running Visual AI models, or invalidating CDN cache.

- Path: `scaleflex-api`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 428

### `schema-validation`

Use when defining or reviewing validation for configuration files, API payloads, manifests, serialized models, cross-field invariants, or human-readable validation errors.

- Path: `schema-validation`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 400

## Private skills

### `cdsv2`

Use when authoring, reviewing, testing, troubleshooting, or migrating OVH CDSv2 workflow, action, worker-model, template, gate, matrix, service, or expression YAML.

- Path: `private-skills/cdsv2`
- Invocation: automatic
- Clients: local-shell
- Required skills: none
- Optional skills: none
- Commands: cdsctl
- Compatibility: Environment-specific; runtime validation requires access to OVH CDSv2 and cdsctl.
- Main-file words: approximately 255

### `jira`

Use when a locally configured Jira CLI is required to inspect or mutate issues, comments, assignments, transitions, Tempo entries, or Confluence pages.

- Path: `private-skills/jira`
- Invocation: automatic
- Clients: local-shell
- Required skills: none
- Optional skills: none
- Commands: jira
- Compatibility: Environment-specific; requires the locally configured private Jira CLI.
- Main-file words: approximately 268

### `ovhcloud-smoke-tests`

Use when OVHcloud smoke-test patterns fail literal HTML matching or the locale-specific pattern catalogue needs updating.

- Path: `private-skills/ovhcloud-smoke-tests`
- Invocation: automatic
- Clients: local-shell
- Required skills: none
- Optional skills: none
- Commands: python3
- Compatibility: Environment-specific; requires the smoke-test repository and access to rendered locale pages.
- Main-file words: approximately 523

### `rr-sync-dev`

Use when syncing local project files to a configured development server through the rr Zsh function, or when rr produces unexpected results.

- Path: `private-skills/rr-sync-dev`
- Invocation: automatic
- Clients: local-shell
- Required skills: none
- Optional skills: none
- Commands: git, rsync, ssh, zsh
- Compatibility: Environment-specific; requires Zsh, Git, rsync, SSH, and local RR_* configuration.
- Main-file words: approximately 389
