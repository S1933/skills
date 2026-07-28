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

### `brainstorming`

Use when creating features, components, functionality, or any behaviour change that requires intent and design to be clarified before implementation.

- Path: `brainstorming`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: node
- Compatibility: Agent Skills compatible; the optional visual companion requires Node.js and a local browser.
- Main-file words: approximately 293

### `caveman`

Use when the user explicitly requests caveman mode, ultra-compressed responses, fewer tokens, or unusually terse technical communication.

- Path: `caveman`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 255

### `codebase-design`

Use when designing or improving module interfaces, seams, information hiding, testability, navigability, or deep-module boundaries.

- Path: `codebase-design`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 251

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

### `decision-mapping`

Use when explicitly invoking /decision-mapping to turn a loose idea into sequenced investigation tickets whose findings drive later decisions.

- Path: `decision-mapping`
- Invocation: manual
- Clients: agent-skills
- Required skills: none
- Optional skills: domain-modeling, grilling, prototype, to-prd
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 592

### `design-an-interface`

Use when exploring multiple substantially different API or module-interface designs before choosing one.

- Path: `design-an-interface`
- Invocation: automatic
- Clients: claude-code, codex, opencode
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Requires a client with parallel subagent support.
- Main-file words: approximately 483

### `dispatching-parallel-agents`

Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies

- Path: `dispatching-parallel-agents`
- Invocation: automatic
- Clients: claude-code, codex, opencode
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Requires a client with parallel subagent support.
- Main-file words: approximately 237

### `domain-modeling`

Use when defining domain terminology, ubiquitous language, bounded contexts, or architectural decisions tied to a domain model.

- Path: `domain-modeling`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 497

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

### `executing-plans`

Use when explicitly invoking /executing-plans with an approved implementation plan in a separate session.

- Path: `executing-plans`
- Invocation: manual
- Clients: agent-skills
- Required skills: finishing-a-development-branch, using-git-worktrees
- Optional skills: subagent-driven-development, writing-plans
- Commands: git
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 376

### `finishing-a-development-branch`

Use when implementation and verification are complete and the branch needs an explicit merge, pull-request, retention, or cleanup decision.

- Path: `finishing-a-development-branch`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: git
- Compatibility: Requires Git; pull-request options require a configured repository host integration.
- Main-file words: approximately 289

### `git-guardrails-claude-code`

Use when setting up Claude Code hooks to prevent pushes or destructive Git operations from running without user control.

- Path: `git-guardrails-claude-code`
- Invocation: automatic
- Clients: claude-code
- Required skills: none
- Optional skills: none
- Commands: bash, python3
- Compatibility: Requires Claude Code with Bash PreToolUse hooks and Python 3.
- Main-file words: approximately 497

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

### `grill-me`

Use when explicitly invoking /grill-me to stress-test and sharpen a plan or design.

- Path: `grill-me`
- Invocation: manual
- Clients: agent-skills
- Required skills: grilling
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 25

### `grill-with-docs`

Use when explicitly invoking /grill-with-docs to stress-test a plan while recording ADRs and a domain glossary.

- Path: `grill-with-docs`
- Invocation: manual
- Clients: agent-skills
- Required skills: domain-modeling, grilling
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 32

### `grilling`

Use when a plan or design needs a rigorous one-question-at-a-time stress test before implementation.

- Path: `grilling`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 90

### `handoff`

Use when explicitly preparing the current conversation for another agent to continue with minimal context loss.

- Path: `handoff`
- Invocation: manual
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 136

### `implement`

Use when explicitly implementing work from an approved PRD, specification, or issue set.

- Path: `implement`
- Invocation: manual
- Clients: claude-code, codex, opencode
- Required skills: requesting-code-review, test-driven-development, verification-before-completion
- Optional skills: none
- Commands: git
- Compatibility: Requires a client with repository editing, command execution, and subagent review support.
- Main-file words: approximately 87

### `improve`

Use when surveying a codebase for prioritized improvement opportunities across correctness, security, performance, testing, maintainability, developer experience, migrations, or product direction.

- Path: `improve`
- Invocation: automatic
- Clients: agent-skills
- Required skills: repository-reconnaissance
- Optional skills: none
- Commands: none
- Compatibility: Requires repository read access; parallel subagent support is recommended.
- Main-file words: approximately 335

### `improve-codebase-architecture`

Use when explicitly auditing a codebase for deep-module, seam, interface, or information-hiding opportunities in an architecture-focused visual report.

- Path: `improve-codebase-architecture`
- Invocation: manual
- Clients: agent-skills
- Required skills: codebase-design, grilling, repository-reconnaissance
- Optional skills: domain-modeling
- Commands: none
- Compatibility: Requires repository read access and a local browser for the visual report.
- Main-file words: approximately 299

### `migrate-to-shoehorn`

Use when TypeScript tests use as assertions for partial fixtures and should migrate to @total-typescript/shoehorn.

- Path: `migrate-to-shoehorn`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 405

### `prototype`

Use when explicitly building a throwaway prototype to answer design questions about business logic, state transitions, or alternative user interfaces.

- Path: `prototype`
- Invocation: manual
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Terminal prototypes are portable; visual UI mode requires Node.js and a local browser.
- Main-file words: approximately 508

### `qa`

Use when the user wants a conversational QA session to report, investigate, and file reproducible software issues.

- Path: `qa`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Requires repository read access and a configured GitHub issue integration.
- Main-file words: approximately 788

### `receiving-code-review`

Use when review feedback must be understood, verified, prioritized, or challenged before implementation.

- Path: `receiving-code-review`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 316

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

### `request-refactor-plan`

Use when planning a risky or substantial refactor as safe incremental commits and a reviewable issue or RFC.

- Path: `request-refactor-plan`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Requires repository read access and a configured GitHub issue integration.
- Main-file words: approximately 432

### `requesting-code-review`

Use when implementation work needs an independent code review before completion, integration, or merge.

- Path: `requesting-code-review`
- Invocation: automatic
- Clients: claude-code, codex, opencode
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Requires a client with subagent support.
- Main-file words: approximately 400

### `resolving-merge-conflicts`

Use when you need to resolve an in-progress git merge/rebase conflict.

- Path: `resolving-merge-conflicts`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 134

### `review-scope`

Use when beginning a code review that must include committed, staged, unstaged, and relevant untracked changes against the correct base.

- Path: `review-scope`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Requires Git repository access.
- Main-file words: approximately 162

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

### `setup-pre-commit`

Use when adding or repairing Husky pre-commit automation for formatting, type checking, and tests in a JavaScript or TypeScript repository.

- Path: `setup-pre-commit`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 320

### `subagent-driven-development`

Use when executing implementation plans with independent tasks in the current session

- Path: `subagent-driven-development`
- Invocation: automatic
- Clients: claude-code, codex, opencode
- Required skills: finishing-a-development-branch, requesting-code-review, test-driven-development, using-git-worktrees
- Optional skills: executing-plans, implement, writing-plans
- Commands: bash, git
- Compatibility: Requires a client with subagent support and Bash.
- Main-file words: approximately 382

### `systematic-debugging`

Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes

- Path: `systematic-debugging`
- Invocation: automatic
- Clients: agent-skills
- Required skills: test-driven-development
- Optional skills: verification-before-completion
- Commands: bash
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 343

### `tech-debt-audit`

Use when explicitly requesting a broad repository-wide technical-debt, architecture, or code-health audit delivered as one evidence-backed report.

- Path: `tech-debt-audit`
- Invocation: manual
- Clients: agent-skills
- Required skills: repository-reconnaissance
- Optional skills: none
- Commands: none
- Compatibility: Requires repository read access and permission to write the report file.
- Main-file words: approximately 314

### `test-driven-development`

Use when implementing any feature or bugfix, before writing implementation code

- Path: `test-driven-development`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 364

### `to-issues`

Use when explicitly converting an approved plan, specification, or PRD into independently assignable vertical-slice issues.

- Path: `to-issues`
- Invocation: manual
- Clients: agent-skills
- Required skills: none
- Optional skills: triage
- Commands: none
- Compatibility: Requires a configured project issue-tracker integration.
- Main-file words: approximately 537

### `to-prd`

Use when explicitly publishing requirements already established in conversation as a PRD without another discovery interview.

- Path: `to-prd`
- Invocation: manual
- Clients: agent-skills
- Required skills: none
- Optional skills: triage
- Commands: none
- Compatibility: Requires a configured project issue-tracker integration.
- Main-file words: approximately 492

### `triage`

Use when explicitly moving issue reports through categorisation, reproduction, clarification, and agent-ready briefing.

- Path: `triage`
- Invocation: manual
- Clients: agent-skills
- Required skills: none
- Optional skills: domain-modeling, grilling
- Commands: none
- Compatibility: Requires a configured project issue-tracker integration.
- Main-file words: approximately 734

### `ubiquitous-language`

Use when explicitly extracting or refining canonical domain terminology, definitions, ambiguities, and discouraged synonyms from the conversation.

- Path: `ubiquitous-language`
- Invocation: manual
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 678

### `using-git-worktrees`

Use when implementation work needs an isolated Git workspace or when an execution workflow requires isolation before changes begin.

- Path: `using-git-worktrees`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: git
- Compatibility: Requires Git worktree support or an equivalent client-native isolation mechanism.
- Main-file words: approximately 299

### `using-superpowers`

Use when explicitly invoking /using-superpowers at the start of a conversation where repository skills are available.

- Path: `using-superpowers`
- Invocation: manual
- Clients: agent-skills
- Required skills: none
- Optional skills: brainstorming, codex, systematic-debugging
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 477

### `verification-before-completion`

Use when about to claim work is complete, fixed, passing, ready to commit, or ready to merge.

- Path: `verification-before-completion`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: none
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 652

### `writing-plans`

Use when you have a spec or requirements for a multi-step task, before touching code

- Path: `writing-plans`
- Invocation: automatic
- Clients: agent-skills
- Required skills: none
- Optional skills: executing-plans, subagent-driven-development, using-git-worktrees
- Commands: none
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 266

### `writing-skills`

Use when creating new skills, editing existing skills, or verifying skills work before deployment

- Path: `writing-skills`
- Invocation: automatic
- Clients: agent-skills
- Required skills: test-driven-development
- Optional skills: systematic-debugging
- Commands: node
- Compatibility: Agent Skills compatible.
- Main-file words: approximately 440

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
