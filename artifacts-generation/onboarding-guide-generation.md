# Developer Onboarding Guide - Comprehensive Prompt Suite

A structured prompt suite for generating an evidence-grounded developer onboarding guide from a remote or local repository. It helps a new team member install the toolchain, run the application, understand the architecture and code organization, execute tests, debug common issues, and contribute safely.

---

## AI assistant skill

This prompt suite corresponds to the `/onboarding-guide` AI assistant skill.

The first positional input may be a remote repository URL or a local repository path. Quote local paths containing spaces. Inspect local paths directly and record Git provenance when available; never clone or delete the supplied local repository.

**Supported flags:**

| Flag | Format | Default | Description |
|------|--------|---------|-------------|
| Repository or path | First positional value | *(required)* | GitHub URL, local repository, or supplied repository path |
| `--output` | `--output ./docs/onboarding` | Current directory | Output directory |
| `--path` | `--path services/api` | Repository root | Monorepo application to onboard |
| `--sections` | `--sections setup,testing` | All | Sections to generate |
| `--force` | flag | Off | Overwrite existing output |
| `--dry-run` | flag | Off | Preview scope and planned output without writing |

```
/onboarding-guide https://github.com/org/repo
/onboarding-guide https://github.com/org/repo --path apps/web
/onboarding-guide https://github.com/org/repo --sections prerequisites,setup,testing
/onboarding-guide https://github.com/org/repo --output ./docs/onboarding --force
/onboarding-guide https://github.com/org/repo --dry-run
```

---

## Manual usage

Analyse `[REPOSITORY_INPUT]` at `[ANALYSIS_PATH]`. The input may be a remote URL or local path. For a monorepo, select one application with `--path`.

Before generating:

1. Record repository URL/path, branch, commit SHA, analysis path, and timestamp.
2. Verify the selected application path and its manifest or workspace target.
3. Detect monorepo candidates; stop and request `--path` when multiple applications are plausible.
4. Check output conflicts and stop unless `--force` is supplied.
5. Use N/A or Assumption for unsupported information.
6. In dry-run mode, write nothing.

---

## Grounding and Evidence Rules

Every command, setup requirement, version, architecture fact, test instruction, and contribution rule must be traceable to repository evidence.

### Valid evidence sources

| Evidence Type | Examples |
|---------------|---------|
| Repository documentation | README.md, docs/, CONTRIBUTING.md, SECURITY.md |
| Toolchain files | .tool-versions, .nvmrc, package.json, go.mod, pom.xml, Dockerfile |
| Dependency and workspace files | Lockfiles, package manifests, pnpm-workspace.yaml, nx.json, turbo.json |
| Scripts and task definitions | Makefile, package scripts, task runners, setup/bootstrap scripts |
| CI/CD | GitHub Actions, Jenkins, GitLab CI, build and test jobs |
| Source code | Entry points, modules, configuration, handlers, generated-code markers |
| Tests | Test files, fixtures, test configuration, coverage configuration |
| Repository metadata | CODEOWNERS, PR templates, issues, ADRs, commit history |

### Prohibited behaviours

- Do not infer prerequisites from framework conventions.
- Do not invent commands, tools, versions, architecture, contacts, policies, or workflow requirements.
- Do not present supplied context or assumptions as repository facts.
- Do not copy credentials, tokens, private keys, personal data, or secret values.
- Do not call an unexecuted command verified.
- Do not recommend destructive cleanup unless its scope and impact are documented.

### Command verification statuses

Use exactly one:

- **Verified** - executed successfully in a clean environment.
- **CI-verified** - passed in CI at the analyzed commit with context available.
- **Repository-documented** - present in repository instructions or executable configuration but not executed.
- **Unverified** - supplied or unresolved; never present as a required step.

Every command must record working directory, shell/platform, prerequisites, expected result, verification method, rerun safety, side effects, and citation.

### Citation requirement

Cite every claim and command:

- File: `(scripts/setup.sh:15-20)`
- Configuration: `(package.json -> scripts.test)`
- CI: `(.github/workflows/ci.yml:42-58)`
- Documentation: `(CONTRIBUTING.md ? Testing)`

### N/A and assumption rules

For unsupported content:

> **N/A** - no supporting evidence found in repository

For supplied but unverified context:

> **Assumption** - [statement]; validate with [owner or artifact]

---

## Repository discovery and monorepo scope

Create a shared discovery context containing:

- Provenance, branch, commit SHA, analysis path, and timestamp.
- Languages, runtimes, compilers, package managers, version files, lockfile mode, and architecture.
- Operating-system, shell, CPU architecture, native-package, and container requirements.
- Root bootstrap commands and application-specific commands.
- Workspace tool, selected application, manifest, entry point, transitive workspace dependencies, and excluded siblings.
- Services, databases, queues, caches, external dependencies, configuration, and environment variables.
- Test types, commands, fixtures, required services, side effects, runtime, and CI-only checks.
- Branch, formatting, linting, commit, PR, issue, review, ownership, and security-reporting guidance.
- Documentation gaps, command conflicts, platform differences, stale evidence, and tool failures.

For monorepos:

- Detect workspace files, multiple manifests, and application directories.
- If `--path` is absent and multiple runnable apps exist, list candidates and stop.
- Scope application claims to `ANALYSIS_PATH` and shared files that directly govern it.
- Resolve direct and transitive workspace dependencies.
- Use app-scoped workspace filters and do not mix sibling applications.
- Write output under `{output}/{application-name}/` and list excluded siblings.

---

## Output Structure

```
{output}/
  {application-name}/
    onboarding-guide.md
    evidence-register.md
```

For a non-monorepo, use `{output}/onboarding-guide.md` and `{output}/evidence-register.md`.

Write only requested sections. Automatically include prerequisite sections for selected sections that depend on them, and list included/skipped sections explicitly.

---

## Prompt 1: Overview and prerequisites

```
Analyse [REPOSITORY_INPUT] at [ANALYSIS_PATH] and generate the onboarding overview and prerequisites.

Include:
- Audience and assumed experience.
- Repository scope, commit, timestamp, and limitations.
- A first-day path from clone to first test.
- Operating system, shell, architecture, runtime, compiler, package manager, lockfile, native tools, containers, accounts, permissions, VPN, and license requirements.
- A platform/reproducibility matrix with version source and verification commands.
- Environment-variable names and safe configuration locations, never values.

For every item include purpose, verification, evidence, confidence, and platform differences.
```

## Prompt 2: Local setup

```
Analyse [REPOSITORY_INPUT] at [ANALYSIS_PATH] and generate an ordered local setup guide.

Separate:
1. Repository-root bootstrap and workspace installation.
2. Shared services required by the selected application.
3. Application-specific configuration and startup.
4. Migrations or seed data, only when documented.
5. Application startup and health verification.

For every command include command ID, working directory, shell/platform, prerequisites, expected result, verification status, rerun safety, side effects, cleanup/recovery, and citation. Use workspace filters or target selectors when documented.
```

## Prompt 3: Architecture and code organization

```
Analyse [REPOSITORY_INPUT] at [ANALYSIS_PATH] and explain the selected application's architecture and code organization.

Include:
- Entry points and representative request/event flow.
- Services, modules, data stores, queues, caches, external systems, and configuration boundaries.
- Top-level directory and module responsibilities.
- Shared libraries, dependency direction, generated code, and files that must not be edited.
- Naming, formatting, and repository-specific terminology.
- A cited "Where should I make this change?" decision guide.
- A reading path from entry point to handler, domain logic, persistence/integration, tests, configuration, and error handling.

Do not use sibling application facts as evidence.
```

## Prompt 4: Testing and debugging

```
Analyse [REPOSITORY_INPUT] at [ANALYSIS_PATH] and document testing and troubleshooting.

Create a test execution matrix:
Test | Command | Local/CI | Prerequisites | Network | Data side effects | Isolation | Runtime | Evidence

Cover unit, integration, end-to-end, contract, smoke, static-analysis, fixtures, containers, filtering, coverage, CI-only checks, flaky tests, and cleanup.

Create a troubleshooting table:
Symptom | Evidence-backed cause | Diagnostic command/step | Resolution | Risk | Scope | Citation

Label reset, migration, seed, cleanup, database, container, and diagnostic commands Safe, Mutating, or Destructive.
```

## Prompt 5: Contribution workflow and first change

```
Analyse [REPOSITORY_INPUT] at [ANALYSIS_PATH] and document repository-supported contribution practices.

Cover:
- Branch/fork workflow.
- Formatting, linting, type checking, hooks, tests, and CI gates.
- Commit messages, PR templates, reviews, CODEOWNERS, issues, design documents, and security reporting.
- Release and migration coordination.
- A concrete first-change path using a real low-risk module and test when evidence permits.

Classify each instruction as Repository-documented, Organization-supplied, Assumption, or N/A.
```

---

## Evidence register

Create `evidence-register.md`:

| Evidence ID | Claim/instruction | Evidence type | Source | Location | Commit | Environment | Confidence | Verification status | Freshness | Command ID | Notes |
|-------------|------------------|---------------|--------|----------|--------|-------------|------------|---------------------|-----------|------------|-------|

Also record command conflicts:

| Command ID | Affected section | Source A | Source B | Selected authority | Reason | Resolution status | Evidence IDs |
|------------|------------------|----------|----------|-------------------|--------|------------------|-------------|

Use High, Medium, or Low confidence. Every guide instruction must map to an evidence ID or explicit N/A/Assumption.

---

## Output requirements

### onboarding-guide.md

The guide must:

- Begin with `# Developer Onboarding Guide: {repo name}`.
- Include selected application, workspace, commit, timestamp, scope, audience, and excluded siblings.
- Include a table of contents.
- Use `## N. Section Name` headings.
- Use language-tagged fenced code blocks.
- Use tables for prerequisites, commands, tests, and troubleshooting.
- Link every section to `evidence-register.md`.
- Include secret, destructive-command, production-access, and unavailable-dependency warnings.
- Include guide owner/reviewer/review dates only when evidenced.

### Monorepo output

For each selected application:

- Use a stable application-name derived from its manifest or workspace target.
- Prevent output collisions.
- Validate app-specific commands, workspace selectors, nested links, and evidence paths.
- List sibling applications under `Excluded from this guide`.

---

## Validation and confirmation

Before completion:

1. Validate Markdown headings, tables, fences, and relative links.
2. Verify every requested section appears exactly once.
3. Verify prerequisite sections were included for dependent sections.
4. Verify every command has complete execution metadata and a valid citation.
5. Verify platform, toolchain, version, and environment-variable claims.
6. Verify workspace commands target the selected application and dependency closure is complete.
7. Verify no sibling application facts leaked into the guide.
8. Verify every evidence ID is used and every instruction maps to evidence or N/A/Assumption.
9. Validate test commands, side effects, destructive-operation labels, and cleanup.
10. Scan output for secrets and redact sensitive values.
11. Report stale documentation, command conflicts, incomplete sections, assumptions, and platform limitations.
12. Clean up only the temporary clone created by this invocation.

```
- onboarding-guide.md
- evidence-register.md
- Section 6 - LIMITED: integration-test dependency not documented
- Section 8 - N/A: contribution workflow not found
```

