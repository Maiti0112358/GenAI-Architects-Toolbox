---
name: arch-describe
description: Generate a comprehensive architecture description document from a GitHub repository using 15 structured analysis sections
allowed-tools: WebFetch, Bash(gh repo view:*), Bash(gh api repos/*:*), Bash(git clone:*), Read, Glob, Grep, Write, Agent
---

Generate a comprehensive architecture description document for a GitHub repository.

## Arguments

Parse `$ARGUMENTS` for the following before doing anything else:

| Argument | Format | Default | Description |
|----------|--------|---------|-------------|
| Repo URL | First positional value | *(required — ask if missing)* | The GitHub repository to analyse |
| `--sections` | `--sections 1,4,7` | All 15 sections | Comma-separated list of section numbers to run; skip all others and their agents |
| `--output` | `--output ./docs/arch` | Current working directory | Directory where `architecture-description.md` and the `diagrams/` folder are written |
| `--path` | `--path services/api` | Repo root | Subdirectory within the repo to treat as the analysis root; use for monorepos to focus on one service |
| `--force` | flag, no value | Off | Overwrite existing output files without prompting; without this flag the skill stops if any output file already exists |
| `--dry-run` | flag, no value | Off | Run discovery only; print the planned output structure and section list without generating any analysis or writing any files |

Examples:
```
/arch-describe https://github.com/org/repo
/arch-describe https://github.com/org/repo --sections 5,7,12
/arch-describe https://github.com/org/repo --output ./docs/architecture
/arch-describe https://github.com/org/repo --sections 1,2,3 --output ./out
/arch-describe https://github.com/org/monorepo --path services/payments
/arch-describe https://github.com/org/repo --output ./docs --force
/arch-describe https://github.com/org/repo --dry-run
/arch-describe https://github.com/org/monorepo --path services/payments --dry-run
/arch-describe https://github.com/org/repo --sections 4,7 --output ./out --dry-run
```

**`--sections` validation:** After parsing `$ARGUMENTS`, if `--sections` was provided, verify that every number is an integer in the range 1–15. If any value is outside this range or non-numeric, stop immediately:
> `Error: Invalid section numbers in --sections: [N]. Valid section numbers are 1–15.`

When `--sections` is provided, only run the specified sections. Skip their batches entirely if no section in that batch was requested; run a reduced batch if only some sections were requested. The Conclusion (Section 15) always synthesises only the sections that were actually run.

**Important prerequisite:** Not all prompts will yield results for every repository — availability of information varies. Skip any section where insufficient information exists in the repo, and note it as "N/A — insufficient information available."

## Repo Access Strategy

**Step 1 — Extract the repo URL from `$ARGUMENTS` before doing anything else:**
Parse `$ARGUMENTS` to isolate the repo URL (the first positional value, not prefixed with `--`). Store it as `REPO_URL`. All subsequent steps use `REPO_URL`, never the raw `$ARGUMENTS` string. Example:
- `$ARGUMENTS` = `https://github.com/org/repo --sections 5,7 --output ./out`
- `REPO_URL` = `https://github.com/org/repo`
- Also derive `REPO_OWNER` and `REPO_NAME` by splitting the URL path.

**Step 2 — Determine access method** and use it consistently for all agents:

First, run `gh auth status` to determine authentication state:
- **Unauthenticated:** the GitHub API allows only 60 requests/hour. With 15 parallel agents each making multiple calls, this limit will be exhausted in seconds. **Prefer cloning (treat as private)** to avoid hitting the limit. Only use the API if cloning fails.
- **Authenticated:** 5,000 requests/hour is sufficient for normal use. If any `gh api` call returns HTTP 403 or 429, retry up to 3 times with exponential backoff (wait 5 s, then 10 s, then 20 s). If all retries fail, fall back to cloning.

- **Public repo** (`gh repo view REPO_URL` exits 0 and user is authenticated): use `gh api repos/REPO_OWNER/REPO_NAME/contents/{path}` and `gh api repos/REPO_OWNER/REPO_NAME/git/trees/HEAD?recursive=1` to read files. Do not clone.
- **Private repo** (`gh repo view REPO_URL` exits non-zero), **or unauthenticated user with a public repo**: the **Batch 0 discovery agent** must clone the repo once to a uniquely named local temp directory (e.g. `./arch-describe-tmp-{unix-timestamp}/`) and record the absolute path in the discovery context as `localClonePath`. All subsequent section agents read from that local clone using `Read`, `Glob`, and `Grep` — they must not clone again. The unique timestamp in the directory name prevents conflicts when two invocations run concurrently in the same working directory.

After all batches complete (or after the dry-run plan is printed), delete the temp clone directory if one was created.

**Step 3 — Resolve the analysis path:**
- If `--path` was provided, set `ANALYSIS_PATH` to that subdirectory. Verify it exists in the repo; if not, stop and report an error.
- If `--path` was **not** provided, the Batch 0 discovery agent must detect whether the repo is a monorepo using the following heuristics:
  - Multiple `package.json`, `pom.xml`, `go.mod`, `build.gradle`, or `pyproject.toml` files at different directory depths
  - Presence of top-level directories named `packages/`, `apps/`, `services/`, `libs/`, or `modules/`
  - Presence of a monorepo orchestration config: `lerna.json`, `nx.json`, `turbo.json`, `pnpm-workspace.yaml`, or `WORKSPACE` (Bazel)
- If a monorepo is detected and `--path` was not provided: list the discovered services/packages (name + path) and **stop**. Ask the user: *"This appears to be a monorepo. Which service should be analysed? Re-run with `--path <service-path>`, or type the path to continue."* Do not proceed until a path is confirmed.
- If the repo is not a monorepo, set `ANALYSIS_PATH` to the repo root.

---

## Dry-run mode

If `--dry-run` was passed:

1. Parse all arguments as normal (Step 1 of Repo Access Strategy).
2. Run **Batch 0 only** — verify repo access, collect metadata, and detect monorepos. Follow the full Repo Access Strategy (Steps 2 and 3), including the monorepo stop-and-ask behaviour.
3. After the discovery agent returns, print the following plan to the user (adapt to the actual arguments):

   ```
   Dry-run: arch-describe
   ─────────────────────────────────────────────────────
   Repository:    https://github.com/org/repo  (public)
   Analysis path: services/payments
   Output dir:    ./docs/arch

   Sections to run (15 of 15):
     Batch 1: §1 Introduction, §2 Context, §3 Architecture Overview
     Batch 2: §4 Components & Structure, §5 Technology Stack, §6 Deployment & Infrastructure
     Batch 3: §7 Security, §8 Performance & Scalability, §9 Reliability & Availability
     Batch 4: §10 Maintainability, §11 Governance & Compliance, §12 Dependencies & Integrations
     Batch 5: §13 Observability & Monitoring, §14 Evolution & Roadmap
     Batch 6: Consistency Pass
     Batch 7: §15 Conclusion

   Files that would be written:
     architecture-description.md
     sections/
       01-introduction.md … 15-conclusion.md  (15 files)
     diagrams/
       04-data-flow.drawio
       04-data-models.drawio
       04-interfaces.drawio
       04-sequence.drawio
       06-infrastructure.drawio
       06-cicd-pipeline.drawio
       08-scalability.drawio
       12-dependencies.drawio
       13-observability.drawio
       README.md
   ─────────────────────────────────────────────────────
   Re-run without --dry-run to generate the full analysis.
   ```

   - If `--sections` was provided, list only the batches and section files that would actually run; omit diagram files belonging to skipped sections.
   - If any output files already exist and `--force` was not passed, mark them with `⚠ already exists` in the file list.
   - If a temp clone was created during discovery, delete it now.

4. **Stop.** Do not run Batches 1–7. Do not write any files.

---

## Pre-batch setup

Before launching Batch 1, complete the following two steps in order. These steps run **after** the Batch 0 discovery agent returns and `ANALYSIS_PATH` is confirmed, but **before** any section batch starts.

### Pre-batch Step 1 — Overwrite check

Resolve every path that will be written: all section files for sections that will run, the master index (`architecture-description.md`), all diagram files belonging to sections that will run, and `diagrams/README.md`. If any already exist and `--force` was **not** passed:
- List every conflicting path
- Stop with: *"Output files already exist. Re-run with `--force` to overwrite, or choose a different `--output` path."*

If `--force` was passed, proceed without prompting.

### Pre-batch Step 2 — Create output directories

Create the following directories (if they do not already exist) before any section agent runs:
- `{output-dir}/sections/`
- `{output-dir}/diagrams/`

Both directories must exist before Batch 1 starts, because section agents write diagram files directly during their batch execution.

### Pre-batch Step 3 — Diagram file ownership

Each diagram filename is owned by exactly one section. No two parallel agents ever write to the same path:

| Diagram file | Owning section |
|---|---|
| `04-data-flow.drawio`, `04-data-models.drawio`, `04-interfaces.drawio`, `04-sequence.drawio` | Section 4 only |
| `06-infrastructure.drawio`, `06-cicd-pipeline.drawio` | Section 6 only |
| `08-scalability.drawio` | Section 8 only |
| `12-dependencies.drawio` | Section 12 only |
| `13-observability.drawio` | Section 13 only |

A section agent must only write diagram files listed under its own section. Writing a diagram file from the wrong section agent is an error.

---

Work through the sections in **batches**, as described below. Within each batch, launch all agents simultaneously. Wait for all agents in the current batch to finish before starting the next batch. Collect and hold all results, then assemble them in order at the end.

After each batch completes, print a one-line progress message before starting the next, e.g.:
> `✓ Batch 1 complete (Sections 1–3: Introduction, Context, Architecture Overview). Starting Batch 2…`

**Batch 0 — Discovery (single agent, runs first):**
Before any section agents start, run one discovery agent against the repository. It must return a shared context object in **exactly** the following JSON schema — section agents will parse this structure directly, so field names and types must match:

```json
{
  "repo": {
    "name": "string — owner/repo",
    "description": "string | null — from GitHub repo description or README first paragraph",
    "defaultBranch": "string",
    "isPrivate": "boolean",
    "localClonePath": "string | null — absolute path if cloned, null for public API access"
  },
  "languages": [
    { "name": "string", "version": "string | null", "detectedIn": "string — file path" }
  ],
  "frameworks": [
    { "name": "string", "version": "string | null", "detectedIn": "string — file path" }
  ],
  "directoryTree": "string — `tree -L 2` style listing rooted at `analysisPath` (not the repo root)",
  "readme": "string — full content if ≤500 lines, otherwise first 100 + last 50 lines with [truncated] marker",
  "docs": [
    { "path": "string", "type": "string — ADR | CONTRIBUTING | CHANGELOG | runbook | other" }
  ],
  "cicd": [
    { "path": "string", "tool": "string — GitHub Actions | Jenkins | GitLab CI | other" }
  ],
  "deployment": {
    "targets": ["string — e.g. AWS, GCP, Azure, on-premises, Kubernetes, serverless"],
    "evidence": ["string — file paths that indicate the deployment target"]
  },
  "security": {
    "authFiles": ["string — paths to auth-related config, e.g. OAuth config, JWT setup"],
    "secretsManagement": ["string — paths to secrets config, e.g. Vault, AWS Secrets Manager"]
  },
  "monorepo": {
    "detected": "boolean",
    "tool": "string | null — lerna | nx | turborepo | pnpm-workspaces | bazel | other | null",
    "services": [
      { "name": "string", "path": "string — relative path from repo root" }
    ]
  },
  "repoRoot": {
    "cicd": ["string — paths to CI/CD files at the repo root regardless of analysisPath, e.g. .github/workflows/, Jenkinsfile"],
    "licenceFiles": ["string — paths to LICENCE, LICENSE, COPYING, NOTICE at the repo root"],
    "composeFiles": ["string — paths to docker-compose.yml and docker-compose.*.yml at the repo root"],
    "securityFiles": ["string — paths to SECURITY.md, .github/SECURITY.md at the repo root"],
    "rootReadme": "string | null — path to root-level README.md (only if different from analysisPath)"
  },
  "analysisPath": "string — relative path from repo root that all section agents must treat as their root; '.' for full repo"
}
```

Pass this JSON object verbatim to every section agent in Batches 1–5 so they do not need to re-read the repository from scratch. Section agents must reference `localClonePath` (if set) for all file reads, or use the GitHub API otherwise.

**Important:** When `analysisPath` is not the repo root, repo-level files (CI/CD pipelines, licence files, compose files, security policies) will not appear under `analysisPath`. Section agents for **Section 6** (Deployment & Infrastructure) and **Section 11** (Governance & Compliance) must check `repoRoot.cicd`, `repoRoot.licenceFiles`, `repoRoot.composeFiles`, and `repoRoot.securityFiles` in addition to files under `analysisPath`. Other sections should also consult `repoRoot` when their topic is typically documented at the repo level rather than inside a service subdirectory.

**Batch 1 (parallel):** Sections 1, 2, 3 — Introduction, Context, Architecture Overview
**Batch 2 (parallel):** Sections 4, 5, 6 — Components & Structure, Technology Stack, Deployment & Infrastructure
**Batch 3 (parallel):** Sections 7, 8, 9 — Security, Performance & Scalability, Reliability & Availability
**Batch 4 (parallel):** Sections 10, 11, 12 — Maintainability, Governance & Compliance, Dependencies & Integrations
**Batch 5 (parallel):** Sections 13, 14 — Observability & Monitoring, Evolution & Roadmap
**Batch 6 (sequential):** Consistency Pass — single agent; runs after Batches 1–5 complete (see below)
**Batch 7 (sequential):** Section 15 — Conclusion; runs after the Consistency Pass and must use the normalised section outputs

For each section, analyze the repository at `REPO_URL` within `analysisPath` (supplemented by the shared discovery context) and produce the deliverable described. Do not begin a new batch until every agent in the current batch has returned a result.

---

### Batch 6 — Consistency Pass

Run a single agent that receives the raw output of all sections completed so far. It must:

1. **Build a canonical terminology table** — extract every named entity that appears in more than one section: component names, service names, database names, technology names, API names, and environment names. For each, choose one canonical name (prefer the name used in source code or config files) and list every variant found.

   Example output:
   | Canonical Name | Variants Found | Sections Affected |
   |----------------|---------------|-------------------|
   | `AuthService` | "Auth Service", "auth-service", "AuthSvc" | 4, 7, 12 |
   | `PostgreSQL` | "Postgres", "PG", "postgres" | 5, 4, 9 |

2. **Apply normalization** — rewrite each affected section's output, replacing every variant with the canonical name. Preserve all other content exactly.

3. **Return** the normalized section outputs (keyed by section number) and the canonical terminology table. All downstream steps (Batch 7, Output assembly) must use the normalized outputs, not the raw ones.

---

## Grounding and Evidence Rules

These rules apply to **every section, every subsection, and every individual claim** throughout the document. They are non-negotiable and override any instruction to "generate", "describe", or "provide" content.

### What counts as valid evidence

Only the following sources are acceptable. Every claim must be traceable to one of them:

| Evidence Type | Examples |
|---------------|---------|
| Source code | File path + line number or function name |
| Configuration | Config file key/value (e.g. `docker-compose.yml`, `.env.example`, `values.yaml`) |
| Build or package manifest | `package.json`, `pom.xml`, `go.mod`, `requirements.txt`, `Dockerfile` |
| Infrastructure as code | Terraform, Bicep, CloudFormation, Kubernetes manifests |
| CI/CD definitions | `.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml` |
| Documentation in the repo | `README.md`, `docs/`, ADRs, `CONTRIBUTING.md`, `CHANGELOG.md` |
| Repository metadata | Open issues, PR descriptions, milestone titles, commit messages, branch names |
| Inline annotations | `TODO`, `FIXME`, `HACK`, `@deprecated` comments with file + line |

### Prohibited behaviours

- **No inference from shape** — do not conclude intent from naming conventions, folder structure, or code patterns (e.g. "the layered structure suggests they intend to…")
- **No general knowledge fill-in** — do not use knowledge of the framework/platform to fill gaps (e.g. "Spring Boot apps typically use…")
- **No hedged speculation about facts** — the words *likely*, *probably*, *appears to*, *seems*, *presumably* are banned when making factual claims about the codebase (e.g. "the app probably uses JWT" is not acceptable)
- **No fabricated tables** — every row in a table must correspond to a real artifact; do not add rows to make a table look complete
- **No assumed defaults** — do not state that a default configuration applies unless a config file explicitly inherits or documents it

### Carve-out: legitimate forward-looking language

The following sections deal with scenarios, risks, and failure modes that are inherently hypothetical. In **Sections 7, 8, 9, and 14 only**, hedged language (*may*, *could*, *might*, *if*, *in the event of*) is permitted — but only when:
- Describing a **threat, attack vector, or failure mode** (not a fact about the codebase)
- Describing a **planned or possible future state** grounded in a cited issue, ADR, or TODO
- The sentence makes clear it is a scenario, not an observed fact (e.g. "If the token store is compromised, an attacker could…" is acceptable; "the app likely uses token-based auth" is not)

Outside these sections, the prohibition is absolute.

### Citation requirement

Every non-trivial claim must include an inline citation in one of these forms:
- File reference: `(src/auth/middleware.ts:42)`
- Config reference: `(docker-compose.yml → services.db.image)`
- Issue/PR reference: `(#123)` or `(PR #456)`
- Doc reference: `(docs/architecture.md § Deployment)`

If a claim cannot be cited, it must not be made.

### N/A rule

For any sub-point where no valid evidence exists:
- Write `> **N/A** — no supporting evidence found in repository`
- A subsection may be entirely N/A — that is a valid and honest result
- A section may be entirely N/A — do not pad it with adjacent information to avoid the N/A verdict

---

## Section 1: Introduction

Analyze the repository and generate an introduction. Create the following subsections:

- **1.1 Purpose** — Why this architecture description exists and what decisions it supports
- **1.2 Scope** — What is covered and explicitly what is out of scope
- **1.3 Stakeholders** — Key roles and their interest in the architecture (table: Role, Responsibilities, Concerns)
- **1.4 Document Conventions** — Notation, diagram key, and abbreviations used throughout
- **1.5 References** — Links to related documents, ADRs, RFCs, or external standards found in the repository

---

## Section 2: Context

Analyze the repository and generate the context section. Do not include infrastructure, deployment, or technology stack details here — those belong in later sections. Create the following subsections:

- **2.1 Business Context** — Business goals, objectives, and value the system delivers; the problem it solves
- **2.2 Operational Context** — Operational environment: user base, usage patterns, SLA expectations, geographic scope
- **2.3 Technical Context** — Broader technical landscape: upstream/downstream systems, platform constraints, integration obligations
- **2.4 Constraints and Assumptions** — Known constraints (regulatory, organisational, budget) and assumptions the architecture rests on

---

## Section 3: Architecture Overview

Analyze the repository and generate the architecture overview section. Create the following subsections:

- **3.1 Architecture Vision** — High-level statement of intent: what the architecture is optimised for and why
- **3.2 Architecture Principles** — Guiding principles (table: Principle, Rationale, Implications)
- **3.3 Architecture Styles and Patterns** — Dominant styles (e.g. microservices, event-driven, layered) with evidence from the codebase
- **3.4 Key Architecture Decisions** — Significant decisions already made, their drivers, and the alternatives considered (ADR-style table if ADRs are absent)

---

## Section 4: Components and Structure

Analyze the repository and generate the components and structure section. Create the following subsections:

- **4.1 Core Components** — Identify and describe each major component: name, responsibility, technology, and owner (table)
- **4.2 Modules and Services** — Detail modules/services and their interactions (table: Module, Purpose, Depends On, Exposes)
- **4.3 Data Flow** — Narrative description of how data moves through the system; save diagram as `diagrams/04-data-flow.drawio`
- **4.4 Data Models** — Key entities, attributes, and relationships; save ER diagram as `diagrams/04-data-models.drawio`
- **4.5 Component Interfaces** — API contracts, message schemas, and integration surfaces between components; save diagram as `diagrams/04-interfaces.drawio`
- **4.6 Sequence Diagrams** — Step-by-step flows for the 2–3 most critical interactions; save as `diagrams/04-sequence.drawio`

---

## Section 5: Technology Stack

Analyze the repository and generate the technology stack section. Create the following subsections:

- **5.1 Programming Languages** — Language, version, and primary use (table)
- **5.2 Frameworks and Libraries** — Name, version, purpose, and licence (table)
- **5.3 Databases and Data Storage** — Engine, version, data type stored, and access pattern (table)
- **5.4 Middleware and Messaging** — Message brokers, service meshes, API gateways, caches — name, version, role (table)
- **5.5 Third-Party Services and APIs** — External SaaS, cloud services, or APIs the system calls (table: Service, Provider, Purpose)

---

## Section 6: Deployment and Infrastructure

Analyze the repository and generate the deployment and infrastructure section. Create the following subsections:

- **6.1 Deployment Model** — Cloud, on-premises, hybrid, or serverless; provider and region(s)
- **6.2 Infrastructure Components** — Servers, networks, load balancers, storage — names and roles (table)
- **6.3 Environment Configuration** — Differences between dev, staging, and production environments
- **6.4 Containerisation and Orchestration** — Docker images, Kubernetes manifests, Helm charts, or equivalent
- **6.5 Infrastructure Topology** — Save draw.io XML diagram showing cloud regions, VPCs, subnets, and services as `diagrams/06-infrastructure.drawio`
- **6.6 CI/CD Pipeline** — Stages, tools, gates, and deployment targets; save draw.io XML diagram as `diagrams/06-cicd-pipeline.drawio`

---

## Section 7: Security

Analyze the repository and generate the security section. Create the following subsections:

- **7.1 Security Requirements** — Functional and non-functional security requirements (table: Requirement, Priority, Source)
- **7.2 Authentication and Authorisation** — Identity providers, token types, session management, and RBAC/ABAC model
- **7.3 Data Protection** — Encryption at rest and in transit, key management, secrets handling
- **7.4 Network Security** — Firewall rules, network policies, ingress/egress controls, mTLS
- **7.5 Threat Model** — STRIDE or equivalent: assets, threats, and likelihood/impact (table)
- **7.6 Security Controls and Mitigations** — Controls in place mapped to the threats identified above

---

## Section 8: Performance and Scalability

Analyze the repository and generate the performance and scalability section. Create the following subsections:

- **8.1 Performance Requirements** — Target SLAs: response time, throughput, concurrency (table: Metric, Target, Measurement Method)
- **8.2 Caching Strategy** — What is cached, where (client/CDN/server), TTL, and invalidation approach
- **8.3 Scalability Strategies** — Horizontal vs. vertical scaling decisions per component; auto-scaling triggers
- **8.4 Bottlenecks and Hotspots** — Known or anticipated performance bottlenecks and mitigation approaches
- **8.5 Scalability Architecture** — Save draw.io XML diagram illustrating scaling topology as `diagrams/08-scalability.drawio`

---

## Section 9: Reliability and Availability

Analyze the repository and generate the reliability and availability section. Create the following subsections:

- **9.1 Reliability Requirements** — Uptime targets, error budgets, and fault-tolerance SLAs (table)
- **9.2 Fault Tolerance** — Circuit breakers, retries, timeouts, and graceful degradation patterns found in the code
- **9.3 High Availability Strategies** — Redundancy, active-active / active-passive topology, failover mechanisms
- **9.4 Disaster Recovery** — RTO and RPO targets, backup strategy, and recovery runbooks referenced in the repo
- **9.5 Backup and Restore** — What is backed up, frequency, retention, and restore procedure

---

## Section 10: Maintainability and Extensibility

Analyze the repository and generate the maintainability and extensibility section. Create the following subsections:

- **10.1 Code Organisation and Modularity** — Directory structure, layer separation, and module boundaries
- **10.2 Documentation Strategy** — Inline docs, README coverage, API docs, and ADRs present in the repo
- **10.3 Testing Strategy** — Unit, integration, E2E, contract — coverage targets and tooling found
- **10.4 Technical Debt** — Known debt items, workarounds, or TODO comments that affect maintainability
- **10.5 Extension Points** — Plugin systems, feature flags, hooks, or interfaces designed for future extension

---

## Section 11: Governance and Compliance

Analyze the repository and generate the governance and compliance section. Create the following subsections:

- **11.1 Governance Model** — Ownership, review processes, change control, and decision-making bodies
- **11.2 Compliance Requirements** — Regulatory or standards obligations (GDPR, SOC 2, ISO 27001, HIPAA, etc.) and evidence of how they are met
- **11.3 Data Residency and Privacy** — Where data is stored, PII handling, data classification, and retention policies
- **11.4 Audit and Logging Requirements** — What must be logged for compliance, retention periods, and audit trail mechanisms
- **11.5 Licence Compliance** — Open-source licences in use and any obligations they impose

---

## Section 12: Dependencies and Integrations

Analyze the repository and generate the dependencies and integrations section. Create the following subsections:

- **12.1 Internal Dependencies** — Dependencies between internal modules or services (table: Consumer, Dependency, Type, Criticality)
- **12.2 External Dependencies** — Third-party systems, SaaS platforms, or cloud services the system depends on
- **12.3 Integration Patterns** — Synchronous REST/gRPC, asynchronous messaging, webhooks, ETL, file-based, etc.
- **12.4 API Contracts** — Public or shared API definitions (OpenAPI, AsyncAPI, protobuf) found in the repo
- **12.5 Dependency and Integration Diagram** — Save draw.io XML diagram as `diagrams/12-dependencies.drawio`

---

## Section 13: Observability and Monitoring

Analyze the repository and generate the observability and monitoring section. Create the following subsections:

- **13.1 Logging Strategy** — Log levels, structured vs. unstructured, log aggregation tools, and retention
- **13.2 Metrics and KPIs** — Key metrics collected, instrumentation libraries, and storage backend (table: Metric, Tool, Retention)
- **13.3 Distributed Tracing** — Tracing framework (OpenTelemetry, Jaeger, etc.), sampling strategy, and trace propagation
- **13.4 Alerting and Incident Response** — Alert rules, notification channels, on-call runbooks, and escalation paths found in the repo
- **13.5 Dashboards and Visualisation** — Dashboarding tools referenced (Grafana, Datadog, etc.) and what they cover
- **13.6 Observability Architecture Diagram** — Save draw.io XML diagram as `diagrams/13-observability.drawio`

---

## Section 14: Evolution and Roadmap *(if information is available)*

Analyze the repository and generate the evolution and roadmap section. Create the following subsections:

- **14.1 Known Technical Debt** — Debt items with architectural impact: what they are, why they exist, and estimated effort to resolve
- **14.2 Planned Enhancements** — Features or changes in backlog/issues that will affect the architecture
- **14.3 Migration Strategies** — Any in-flight or planned migrations (database, platform, framework) with approach and risk
- **14.4 Architecture Roadmap** — Phased timeline of architectural evolution (table or narrative)
- **14.5 Deprecation Plans** — Components, APIs, or integrations scheduled for removal and their replacement

---

## Section 15: Conclusion

Generate the conclusion using the completed output of **all sections that were actually run** (i.e. those produced by the current invocation, which may be a subset if `--sections` was used) — do not re-analyze the repository, and do not reference or invent findings for sections that were not run. Create the following subsections:

- **15.1 Summary of Key Findings** — Concise recap of the most significant findings from each section that was run; list skipped sections explicitly as "not run in this invocation"
- **15.2 Architecture Strengths** — What the architecture does well, each point citing the section and evidence it came from
- **15.3 Architecture Gaps and Risks** — Gaps, weaknesses, or risks surfaced across the sections that ran, ranked by severity
- **15.4 Recommended Next Steps** — Concrete, prioritised actions to address the gaps and risks above, each traceable to a specific section finding
- **15.5 Open Questions** — Decisions still unmade, N/A subsections, and sections not run that may contain relevant information

---

## draw.io Diagram Format

All diagrams must be valid draw.io XML. Use this skeleton as the base for every `.drawio` file — replace only the `<mxCell>` contents, never the outer structure:

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <!-- diagram cells go here, each with a unique id starting from "2" -->
    <!-- Box example:   <mxCell id="2" value="Service A" style="rounded=1;whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="100" y="100" width="120" height="60" as="geometry"/></mxCell> -->
    <!-- Arrow example: <mxCell id="3" value="calls" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="2" target="4" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell> -->
  </root>
</mxGraphModel>
```

Each cell must have a unique numeric `id`. Use `vertex="1"` for shapes and `edge="1"` for connectors. Set `parent="1"` on all direct children.

### Validation — required after writing every `.drawio` file

Immediately after writing each diagram file, read it back with the `Read` tool and run the following checks in order:

1. Content begins with `<mxGraphModel` — confirms the outer element is present
2. Content ends with `</mxGraphModel>` — confirms the element is closed
3. Count of `<mxCell` equals the count of `</mxCell>` plus self-closing `/>` occurrences on `mxCell` lines — confirms no unclosed cell tags
4. Count of `<mxGeometry` equals count of `</mxGeometry>` plus self-closing instances — confirms geometry nodes are closed

**If any check fails:**
- Log: `⚠ Diagram validation failed: diagrams/NN-name.drawio — [which check failed]`
- Overwrite the file with the skeleton template containing a single placeholder cell and this comment: `<!-- VALIDATION FAILED: diagram could not be generated — replace with a valid draw.io diagram -->`
- Add the diagram to the final output summary under a **"Diagrams requiring manual review"** section with the failure reason

**If all checks pass:** log `✓ diagrams/NN-name.drawio — valid`

---

## Output

> **Skip this entire section if `--dry-run` was passed.** Dry-run mode prints a plan and exits without writing any files.
>
> **Note:** The overwrite check and output directory creation were already performed in Pre-batch setup (Steps 1 and 2). The `sections/` and `diagrams/` directories exist. Diagram files were written by section agents during batch execution. This section assembles only the markdown files and index.

The expected output layout (for reference) is:

```
{output-dir}/
  architecture-description.md       ← master index (see Step 1 below)
  sections/
    01-introduction.md              ← only files for sections that actually ran
    …
    15-conclusion.md
  diagrams/
    04-data-flow.drawio             ← written during batch execution
    …
    README.md                       ← diagram index (see Step 3 below)
```

Only write markdown section files for sections that were actually run. Omit files for skipped sections entirely.

---

### Step 1 — Master index (`architecture-description.md`)

The master index must contain:

1. **Title:** `# Architecture Description: {repo name}`
2. **Table of contents** with a relative file link and anchor for every section that was run, e.g.:

   ```markdown
   ## Table of Contents
   - [1. Introduction](sections/01-introduction.md)
   - [2. Context](sections/02-context.md)
   - [3. Architecture Overview](sections/03-architecture-overview.md)
   …
   - [Diagrams](diagrams/README.md)
   ```

3. **Canonical terminology table** produced by the Consistency Pass (Batch 6) — list every normalised name and the variants it replaced.
4. **Diagrams requiring manual review** — if any diagram failed XML validation, list them here with their failure reasons.
5. **Sections not run** — if `--sections` was used, list the omitted sections here for traceability.

---

### Step 2 — Individual section files (`sections/NN-name.md`)

Each section file must:
- Begin with `# Section N: {Title}` as its `H1`
- Use `## N.X Subsection Name` for every subsection (`H2`)
- Include a back-link at the very top: `[← Architecture Description Index](../architecture-description.md)`
- Reference diagram files with paths relative to the section file, e.g. `[View diagram](../diagrams/04-data-flow.drawio)`
- Include a subsection anchor at the top of each `H2` so deep-links work, e.g.:
  ```markdown
  ## 4.3 Data Flow {#43-data-flow}
  ```

---

### Step 3 — Diagram index (`diagrams/README.md`)

After all diagram files are written, generate `diagrams/README.md` with:
- A title: `# Diagrams`
- A back-link: `[← Architecture Description Index](../architecture-description.md)`
- A table listing every diagram that was produced:

  | File | Section | Depicts |
  |------|---------|---------|
  | `04-data-flow.drawio` | [4. Components & Structure](../sections/04-components-and-structure.md#43-data-flow) | Data flow between components |
  | `04-data-models.drawio` | [4. Components & Structure](../sections/04-components-and-structure.md#44-data-models) | Entity-relationship model |
  | … | … | … |

  Only list diagrams that were actually written and passed XML validation. Failed diagrams appear in a separate **"Failed — requires manual replacement"** table.

---

### Step 4 — Confirm output

After all markdown files are written, print a flat confirmation list of all output files. Diagram files (written during batch execution) are listed alongside markdown files — do not nest them under section files:

```
✓ architecture-description.md
✓ sections/01-introduction.md
✓ sections/02-context.md
…
✓ sections/15-conclusion.md
✓ diagrams/04-data-flow.drawio
✓ diagrams/04-data-models.drawio
⚠ diagrams/04-interfaces.drawio — VALIDATION FAILED
…
✓ diagrams/README.md
```
