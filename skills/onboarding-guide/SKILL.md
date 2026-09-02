---
name: onboarding-guide
description: Generate an evidence-grounded developer onboarding guide from a remote or local repository, covering prerequisites, local setup, key architecture concepts, code organization, testing, debugging, and contribution workflow for new team members.
allowed-tools: WebFetch, Bash(gh auth status:*), Bash(gh repo view:*), Bash(gh api repos/*:*), Bash(git clone:*), Bash(git rev-parse:*), Bash(git status:*), Bash(Remove-Item:*), Read, Glob, Grep, Write, Agent
---

Generate a practical, evidence-grounded developer onboarding guide for a repository. Target a new team member who needs to make and validate their first change. Do not invent commands, tools, architecture, contacts, or policies.

## Arguments

Parse `$ARGUMENTS` before analysis:

| Argument | Format | Default | Description |
|---|---|---|---|
| Repo URL or path | First positional value | Required | Repository to analyse |
| `--output` | `--output ./docs/onboarding` | Current directory | Output directory |
| `--path` | `--path services/api` | Repository root | Monorepo service to analyse |
| `--sections` | `--sections setup,testing` | All | Sections to generate |
| `--force` | Flag | Off | Overwrite existing output |
| `--dry-run` | Flag | Off | Discover scope and planned output without writing |

Valid sections are `overview`, `prerequisites`, `setup`, `architecture`, `code-organization`, `testing`, `debugging`, and `contributing`. Reject invalid section names before analysis.

## Section selection
Validate every `--sections` value. `overview` runs whenever any section is selected. `setup` depends on `prerequisites`; `testing` depends on `setup`; `debugging` depends on `testing`; `contributing` depends on `overview` and `testing`. Automatically include prerequisite sections, report them as automatically included, and list genuinely skipped sections explicitly. Do not generate testing without the setup context needed to run it. List skipped sections explicitly in the guide.
## Operating rules
## Command and evidence trust

Classify every command as Verified, Repository-documented, or Unverified. Never call an unexecuted command verified. Record source, working directory, shell, expected exit code, required environment, rerun safety, and side effects.

- Inspect source, manifests, lockfiles, tool-version files, scripts, CI/CD, configuration, documentation, tests, and contribution guidance.
- Cite every command, version, setup requirement, architecture fact, and workflow rule with a path and line, key, or section reference.
- Prefer commands documented in README files, scripts, Makefiles, package manifests, task runners, and CI configuration.
- Do not infer prerequisites from framework conventions.
- Distinguish verified repository instructions from assumptions and machine-specific caveats.
- Never include credentials, tokens, private keys, personal data, or secret values.
- Use ISO 8601 timestamps and record repository URL/path, commit SHA, branch, analysis path, inspected files, and evidence gaps.

For unsupported information write:

> **N/A** - no supporting evidence found in repository

For assumptions write:

> **Assumption** - [statement]; validate with [owner or artifact]

### Monorepo behavior
Detect monorepos from workspace files, multiple manifests, and directories such as `apps/`, `services/`, `packages/`, `modules/`, and `libs/`. When multiple runnable applications exist and `--path` is absent, list each candidate with name, path, manifest, runtime, and likely entry point, then stop and request a path.
When `--path` is supplied, set `ANALYSIS_PATH` to that application. Verify it exists and is a runnable scope before generating the guide. Do not merge sibling applications into the guide. Analyze shared workspace files only when they affect the selected application.
## Repository access and scope

### Input handling

Classify the first positional input as `REMOTE` when it starts with `http://` or `https://`; otherwise resolve it to an existing local directory as `LOCAL`. Quote local paths containing spaces. For local paths, verify Git status and commit without cloning. For GitHub URLs, clone at most once. For non-Git directories, set commit and branch to N/A and label supplied context. If access fails, stop with a diagnostic. Never delete or overwrite a supplied local repository; clean up only a temporary clone created for a remote URL.
Resolve repository access and analysis scope before writing:

1. Record repository identity, branch, commit SHA, and local clone path if cloning is required.
2. Verify an explicit `--path`; if it does not exist, stop.
3. Detect monorepos using workspace files, multiple manifests, and top-level service directories.
4. If multiple services are plausible without `--path`, list them and stop for a scope choice.
5. Inspect repository-root files even when `--path` targets a service, especially README, contribution, CI/CD, license, and tool-version files.
6. Check output conflicts and stop unless `--force` is supplied.
7. In `--dry-run`, perform discovery only, print the planned sections and files, and write nothing.

### Evidence confidence
Use `High`, `Medium`, or `Low` confidence in the evidence register:
- High: direct, current repository evidence at the analyzed commit.
- Medium: indirect or incomplete evidence, such as a referenced script or stale documentation.
- Low: supplied context, historical material, or unresolved interpretation.
Every guide instruction must map to an evidence ID or explicit N/A/Assumption.
### Monorepo scope context
For a selected application, record:

| Field | Required value |
|---|---|
| Repository root | Absolute or canonical repository path |
| Workspace tool | pnpm, npm, Yarn, Nx, Turborepo, Bazel, Gradle, or N/A |
| Application path | Relative path from repository root |
| Application manifest | Exact path |
| Workspace dependencies | Shared packages required by the application |
| Application entry point | File, script, or target |
| Root setup | Shared install/bootstrap commands |
| App setup | Application-specific commands |
| Sibling scope | Explicitly excluded paths |

Every application-specific claim must cite a file under `ANALYSIS_PATH` or a shared-root file that directly governs the selected application. Record sibling applications as excluded context, not as part of the onboarding guide.
## Discovery context

Create one shared context for all section agents:

| Area | Required facts |
|---|---|
| Provenance | URL/path, branch, commit SHA, timestamp, analysis path |
| Toolchain | Languages, runtimes, package managers, version files, required versions |
| Setup | Install commands, environment variables, service dependencies, seed/migration commands |
| Architecture | Services, modules, entry points, data stores, queues, external systems |
| Code organization | Top-level directories, ownership boundaries, conventions, generated code |
| Testing | Test commands, test types, fixtures, containers, required services, CI commands |
| Contribution | Branch, formatting, linting, review, commit, PR, issue, and release guidance |
| Gaps | Missing documentation, ambiguous commands, platform-specific issues |

### Platform and reproducibility matrix

Record tool version constraints, sources, required/optional status, verification commands, supported OS/shell/architecture, native packages, container images, lockfile mode, and version-manager configuration. If a version is not pinned, report the setup as non-reproducible.
Pass the shared context to every section agent. Agents must not create competing command or terminology variants without evidence.

### Command conflict resolution
When README, scripts, Makefiles, manifests, CI, or service documentation disagree, record the conflict:

| Command ID | Source A | Source B | Selected command | Reason | Unresolved |
|---|---|---|---|---|---|
Prefer current CI/build definitions and executable task configuration over stale prose, but preserve unresolved conflicts in the evidence register.
## Workflow

Use these batches:

1. Discovery and provenance.
2. Prerequisites and local setup.
3. Architecture and code organization.
4. Testing and debugging.
5. Contribution workflow.
6. Consistency and validation.

The final consistency pass must reconcile commands, paths, service names, versions, links, and citations across all sections. If a batch fails, record the stage and affected sections, mark dependent content N/A or incomplete, and report a non-success summary. Clean up only the temporary clone created by this invocation.

### Output assembly
The final consistency pass must merge section-agent results in canonical order, remove duplicate headings, reconcile command variants, paths, versions, and citations, and include only requested sections. Every requested section appears exactly once; every skipped section is listed with its reason.
## Required output

Skip file generation in `--dry-run`.

Create:

```
{output}/
  {application-name}/
    onboarding-guide.md
    evidence-register.md
```

Write only requested sections, but always include the main guide and evidence register unless dry-run is used.

## Section 1: Overview

Create:

- Audience and assumed experience.
- Repository scope and commit analyzed.
- A first-day path from clone to first test.
- Key links to generated sections.
- Explicit limitations and missing evidence.

## Section 2: Prerequisites

Document only evidenced requirements:

- Operating-system or platform requirements.
- Runtime and compiler versions.
- Package managers and exact versions.
- Required local tools.
- Container or service dependencies.
- Accounts, permissions, VPN, cloud, registry, or license requirements.
- Environment variables, using names and safe locations but never values.

For each item include purpose, verification command, expected result, and citation. Mark machine-specific or undocumented requirements as assumptions or N/A.

### Monorepo setup order
For a selected application, separate commands into:
1. Repository-root bootstrap, workspace install, or dependency linking.
2. Shared service startup required by the selected application.
3. Application-specific configuration and startup.
4. Application-specific tests and validation.
Use workspace filters or target selectors when the repository documents them. Never run a repository-wide build, test, reset, or cleanup command unless the repository requires it for the selected application and the scope is clearly labeled.
## Section 3: Local setup
### Command execution context

For every command record exact command, working directory, shell/platform, prerequisites, expected result, verification status, rerun safety, cleanup/recovery, and citation. Do not call a command copyable when any of these is unknown.
- System purpose and entry points.
- Main applications, services, modules, and responsibilities.
- Request/event/data flow.
- Databases, queues, caches, and external dependencies.
- Configuration and environment boundaries.
- Authentication and authorization concepts when documented.
- Important failure or operational boundaries.

Link to files and functions. Do not turn a directory name into an architectural claim without supporting evidence.


Provide an ordered, copyable setup flow:

1. Clone and select the repository revision.
2. Install the evidenced toolchain.
3. Install dependencies.
4. Create configuration from documented examples.
5. Start required services.
6. Run migrations or seed data only when documented.
7. Start the application.
8. Verify a documented health endpoint, CLI command, or test.

For every command include a citation, expected output or success condition, cleanup command where documented, and troubleshooting note where evidenced. Use placeholders for values that must be supplied by the developer.

## Section 4: Architecture concepts

Explain only architecture evidenced by the repository:

## Section 5: Code organization

Walk through the repository:

- Top-level directory purpose.
- Application entry points.
- Module and service boundaries.
- Shared libraries and dependency direction.
- API, domain, persistence, configuration, and infrastructure locations where evidenced.
### Newcomer navigation

Provide a cited reading path: entry point, routing/handler, domain logic, persistence/integration, tests, configuration, and error handling. Identify where a common change belongs and which dependencies are optional for a first change.
- Generated code and files that must not be edited.
- Naming, formatting, and code conventions from repository guidance.

Include a "Where should I make this change?" decision guide grounded in paths and examples.

## Section 6: Testing
### Test execution matrix

For each test record command, local/CI status, prerequisites, network, data side effects, isolation, runtime, cleanup, and evidence. Identify external-service, shared-fixture, flaky, and CI-only tests.

Include documented logs, error messages, health checks, local ports, debugger configuration, reset commands, and known environment issues. Never recommend destructive cleanup unless the repository documents it and clearly label data-loss impact.


Document:

- Unit, integration, end-to-end, contract, smoke, and static-analysis tests.
- Exact commands from manifests, scripts, Makefiles, and CI.
- Required services, fixtures, databases, containers, and environment variables.
- Test selection and filtering.
- Expected duration or output only when documented.
- Coverage commands and thresholds only when evidenced.
- How to diagnose test failures from repository guidance.

Separate tests that run locally from CI-only checks. Never claim that passing tests proves production readiness.

## Section 7: Debugging and common problems
### Safe-operation labels

Label every reset, migration, seed, cleanup, database, container, or diagnostic command as Safe, Mutating, or Destructive; record scope, confirmation requirement, and backup/recovery evidence. Never include shared or production commands without explicit evidence and warnings.

Every non-trivial statement in the guide must map to an evidence ID or be labeled N/A/Assumption. Keep commands and their citations together.


Create a table:

| Symptom | Evidence-backed cause | Diagnostic command/step | Resolution | Citation |
|---|---|---|---|---|
## Section 8: Contribution workflow
### Contribution evidence classes

Classify workflow instructions as Repository-documented, Organization-supplied, Assumption, or N/A. Do not turn general practice into a requirement.
- Use `## N. Section Name` headings.
- Use fenced code blocks with language identifiers.
- Use tables for prerequisites, commands, tests, and troubleshooting.
- Include a back-link only when a section is split into separate files.
- Include warnings for secrets, destructive commands, production access, and unavailable dependencies.
- Link every section to `evidence-register.md`.

### First-change walkthrough
When evidence permits, include a concrete first-change path: identify a low-risk change, locate its module and tests, make the change, run the smallest relevant test, run required formatting/linting, inspect the diff, commit it, and open a pull request using documented rules. Mark any unsupported step N/A rather than inventing a workflow.

Document only repository-supported practices:

- Branch and fork workflow.
- Formatting, linting, type checking, and pre-commit hooks.
- Required test and build checks.
- Commit message rules.
- Pull-request template, review requirements, ownership, and CI gates.
- Issue or design-document requirements.
- Security reporting path.
- Release or migration coordination when documented.

If a workflow is not documented, write N/A and identify where the team should document it.

## Evidence register

Create `evidence-register.md`:

| Evidence ID | Claim or instruction | Source | Location | Commit | Confidence | Notes |
|---|---|---|---|---|---|---|
## Output requirements
### Monorepo output
When `--path` selects an application, include the selected path and workspace name in the guide title and scope. Use an output path that does not overwrite another application's guide, such as `{output}/{application-name}/onboarding-guide.md`, unless the caller explicitly provides an application-specific output directory. Include sibling applications in an `Excluded from this guide` list.

`onboarding-guide.md` must:

- Begin with `# Developer Onboarding Guide: {repo name}`.
- Include the analyzed commit, timestamp, scope, and audience.
- Include a table of contents linking generated sections.
### Maintenance metadata
Include guide owner, technical reviewer, last reviewed date, next review date, and reassessment triggers only when supplied or evidenced. Recommend reassessment when the repository commit changes materially, setup documentation becomes stale, a tool/runtime changes, a control owner changes, or a new platform/dependency is introduced.
### Dependency health
Report only evidenced warnings for deprecated runtimes, unsupported package managers, missing lockfiles, unpinned images, outdated setup scripts, or dependency maintenance concerns. Cite the source and do not make vulnerability claims without an authoritative scan or repository evidence.
### Monorepo validation
Verify that:
- The selected application path exists and is represented by a manifest or documented workspace target.
- Application commands target the selected app rather than a sibling or the entire repository unintentionally.
- Shared-root commands are labeled as shared and cite their controlling workspace file.
- Workspace filters, package names, and target names match repository configuration.
- No sibling application's setup, tests, architecture, or contribution rules appear as facts in the selected guide.
- The final guide records `ANALYSIS_PATH`, workspace tool, selected application, and excluded sibling paths.
## Reliability and robustness requirements

### Command verification authority

Use these verification statuses:

- Verified by execution in a clean environment.
- CI-verified at the analyzed commit.
- Repository-documented but not executed.
- Unverified.

A command found in CI is CI-verified only when its job, working directory, prerequisites, and result are clear. Never label a command Verified without an execution result or explicit CI result.

### Command metadata

Add these fields to every command:

`Command ID | Command | Working directory | Shell/platform | Preconditions | Expected exit code/result | Verification status | Verification method | Rerun safety | Side effects | Citation`

### Evidence register schema

Use:

`Evidence ID | Claim/instruction | Evidence type | Source | Location | Commit | Environment | Confidence | Verification status | Freshness | Command ID | Notes`

Confidence values are High, Medium, or Low. Record documentation and CI dates when available and warn when documentation is older than the manifest or CI configuration.

### Monorepo dependency closure

For the selected application, resolve direct and transitive workspace dependencies, shared configuration, generated code, root lifecycle scripts, and required build targets. Classify each as Required, Optional, Build-only, or Excluded. Do not treat a sibling application as a dependency without evidence.

Every workspace command must record the workspace tool, package/project selector, resolved target, affected packages, and command scope. Reject or clearly warn on commands that operate on the entire repository when an app-scoped command exists.

### Monorepo output isolation

Derive `application-name` from the selected manifest or workspace target and normalize it to a safe directory name. If names collide, append a stable path-derived suffix. Never write one application's guide into another application's output directory. Validate all nested relative links and evidence-register paths.

### Platform-specific guidance

For every supported platform record shell, installation differences, native packages, path/environment differences, container requirements, and unsupported cases. A platform claim without platform-specific evidence is N/A or an Assumption.

### Command conflicts

Assign a stable Command ID to conflicting instructions and record:

`Command ID | Affected section | Source A | Source B | Selected authority | Reason | Resolution status | Evidence IDs`

Prefer current executable task definitions and CI over stale prose, but preserve unresolved conflicts.

### Destructive-operation controls

For reset, migration, seed, cleanup, database, container, or diagnostic commands record:

`Risk | Scope | Confirmation required | Backup/recovery evidence`

Scope must be Local, Shared development, Staging, or Production. Do not include shared or production commands without explicit evidence and warnings.

### First-change path

When evidence permits, identify a real low-risk file/module, its associated test, the smallest relevant test command, required formatting/linting, diff review, commit, and documented PR flow. Mark unsupported steps N/A.

### Partial output and consistency

The final consistency pass must merge agents in canonical section order, remove duplicate headings, reconcile command variants, and ensure each requested section appears once. If a batch fails, record the stage and affected sections, mark dependent content incomplete/N/A, and return a non-success summary.

### Cleanup

Remove only the temporary clone created by this invocation. Resolve and verify the target path before cleanup; never remove the repository, output directory, or user files. Perform cleanup after success, failure, and dry-run discovery.

### Ownership and maintenance

Include guide owner, technical reviewer, CODEOWNERS/maintainer evidence, last reviewed date, next review date, and reassessment triggers only when supplied or evidenced.

### Dependency-health evidence

Report deprecated runtimes, unsupported tools, missing lockfiles, unpinned images, or outdated setup scripts only with repository, CI, official-support, or authoritative-scan evidence. Do not make vulnerability claims from model knowledge alone.

### Validation additions

Verify the selected path is represented by a manifest or documented workspace target; workspace filters resolve to that application; no sibling facts leak into the guide; all nested links resolve; every evidence ID is used; no command lacks verification metadata; and the guide records excluded sibling paths.
## Validation and confirmation

Before completion:

1. Validate Markdown headings, tables, fences, and relative links.
2. Verify every command has a citation and an expected success condition.
3. Verify every version and environment variable is evidence-backed.
4. Verify setup steps are ordered and do not depend on undocumented state.
5. Verify test commands match manifests, scripts, or CI.
6. Verify all section claims map to evidence IDs or explicit N/A/Assumption markers.
7. Scan output for secrets and redact sensitive values.
8. Verify requested sections only, provenance, commit SHA, and output conflicts.
9. Report incomplete sections, assumptions, missing documentation, and platform-specific limitations.

Print:

```
- onboarding-guide.md
- evidence-register.md
- Section 6 - LIMITED: integration-test dependency not documented
- Section 8 - N/A: contribution workflow not found
```

