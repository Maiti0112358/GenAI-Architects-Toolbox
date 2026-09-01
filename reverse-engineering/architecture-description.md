# Architecture Description — Comprehensive Prompt Suite

A structured set of 15 prompts for generating a complete architecture description from any GitHub repository. Each prompt covers a distinct architectural concern and produces a focused, evidence-grounded output section.

---

## Claude Code skill

This prompt suite powers the `/arch-describe` Claude Code skill (https://github.com/Maiti0112358/architects-prompts/blob/main/.claude/skills/arch-describe/SKILL.md). The skill automates parallel agent execution, consistency passes, diagram generation, and structured file output.

**Supported flags:**

| Flag | Format | Default | Description |
|------|--------|---------|-------------|
| Repo URL | First positional value | *(required)* | GitHub repository to analyse |
| `--sections` | `--sections 1,4,7` | All 15 | Comma-separated list of section numbers to run |
| `--output` | `--output ./docs/arch` | Current directory | Directory for output files |
| `--path` | `--path services/api` | Repo root | Monorepo subdirectory to focus on |
| `--force` | flag | Off | Overwrite existing output files |
| `--dry-run` | flag | Off | Preview what would be generated without writing files |

```
/arch-describe https://github.com/org/repo
/arch-describe https://github.com/org/repo --sections 5,7,12
/arch-describe https://github.com/org/repo --path services/payments
/arch-describe https://github.com/org/repo --output ./docs/arch --force
/arch-describe https://github.com/org/repo --dry-run
```

---

## Manual usage

Run each prompt in sequence, substituting `[REPO_URL]` with the target repository URL. For monorepos, also substitute `[ANALYSIS_PATH]` with the service subdirectory (e.g. `services/payments`).

**Prerequisite:** Add the repository to your LLM context, or provide the URL and let the model fetch it. Not every prompt will yield results for every repository — availability of information varies. Use the N/A rule (see Grounding Rules below) for any topic not covered by the repo.

---

## Grounding and Evidence Rules

These rules apply to **every section and every claim**. All output must be traceable to the actual repository.

### Valid evidence sources

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

- **No inference from shape** — do not conclude intent from naming conventions, folder structure, or code patterns
- **No general knowledge fill-in** — do not use knowledge of the framework/platform to fill gaps (e.g. "Spring Boot apps typically use…")
- **No hedged speculation about facts** — words like *likely*, *probably*, *appears to*, *seems* are banned for factual claims about the codebase
- **No fabricated tables** — every row in a table must correspond to a real artifact
- **No assumed defaults** — do not state that a default configuration applies unless a config file explicitly documents it

### Carve-out: forward-looking language

In **Sections 7, 8, 9, and 14 only**, hedged language (*may*, *could*, *might*) is permitted when:
- Describing a threat, attack vector, or failure mode
- Describing a planned or possible future state grounded in a cited issue, ADR, or TODO
- The sentence clearly signals it is a scenario, not an observed fact

### Citation requirement

Every non-trivial claim must include an inline citation:
- File reference: `(src/auth/middleware.ts:42)`
- Config reference: `(docker-compose.yml → services.db.image)`
- Issue/PR reference: `(#123)` or `(PR #456)`
- Doc reference: `(docs/architecture.md § Deployment)`

### N/A rule

For any sub-point where no valid evidence exists, write:
> **N/A** — no supporting evidence found in repository

A section or subsection may be entirely N/A — that is a valid and honest result.

---

## Output Structure

The skill (and recommended manual approach) produces a multi-file output:

```
{output-dir}/
  architecture-description.md       ← master index with TOC and terminology table
  sections/
    01-introduction.md
    02-context.md
    03-architecture-overview.md
    04-components-and-structure.md
    05-technology-stack.md
    06-deployment-and-infrastructure.md
    07-security.md
    08-performance-and-scalability.md
    09-reliability-and-availability.md
    10-maintainability-and-extensibility.md
    11-governance-and-compliance.md
    12-dependencies-and-integrations.md
    13-observability-and-monitoring.md
    14-evolution-and-roadmap.md
    15-conclusion.md
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
```

All diagrams are draw.io XML files (see [Diagram Format](#diagram-format) below).

---

## Prompt 1: Introduction

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Introduction section for an architecture description.
Apply the grounding rules strictly — every claim must cite a file, config, issue, or doc.

Create the following subsections:

1.1 Purpose — Why this architecture description exists and what decisions it supports
1.2 Scope — What is covered and explicitly what is out of scope
1.3 Stakeholders — Key roles and their interest in the architecture
        (table: Role | Responsibilities | Concerns)
1.4 Document Conventions — Notation, diagram key, and abbreviations used throughout
1.5 References — Links to related documents, ADRs, RFCs, or external standards
        found in the repository
```

---

## Prompt 2: Context

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Context section for an architecture description.
Do not include infrastructure, deployment, or technology stack details — those belong
in later sections. Apply the grounding rules strictly.

Create the following subsections:

2.1 Business Context — Business goals, objectives, and value the system delivers;
        the problem it solves
2.2 Operational Context — Operational environment: user base, usage patterns,
        SLA expectations, geographic scope
2.3 Technical Context — Broader technical landscape: upstream/downstream systems,
        platform constraints, integration obligations
2.4 Constraints and Assumptions — Known constraints (regulatory, organisational, budget)
        and assumptions the architecture rests on
```

---

## Prompt 3: Architecture Overview

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Architecture Overview section. Apply the grounding rules strictly.

Create the following subsections:

3.1 Architecture Vision — High-level statement of intent: what the architecture is
        optimised for and why
3.2 Architecture Principles — Guiding principles
        (table: Principle | Rationale | Implications)
3.3 Architecture Styles and Patterns — Dominant styles (e.g. microservices,
        event-driven, layered) with evidence from the codebase
3.4 Key Architecture Decisions — Significant decisions already made, their drivers,
        and the alternatives considered (ADR-style table if ADRs are absent)
```

---

## Prompt 4: Components and Structure

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Components and Structure section. Apply the grounding rules strictly.
Produce draw.io XML diagrams for all diagram subsections.

Create the following subsections:

4.1 Core Components — Identify and describe each major component:
        name, responsibility, technology, and owner (table)
4.2 Modules and Services — Detail modules/services and their interactions
        (table: Module | Purpose | Depends On | Exposes)
4.3 Data Flow — Narrative description of how data moves through the system;
        produce a draw.io data flow diagram (save as 04-data-flow.drawio)
4.4 Data Models — Key entities, attributes, and relationships;
        produce a draw.io ER diagram (save as 04-data-models.drawio)
4.5 Component Interfaces — API contracts, message schemas, and integration surfaces
        between components; produce a draw.io interfaces diagram (save as 04-interfaces.drawio)
4.6 Sequence Diagrams — Step-by-step flows for the 2–3 most critical interactions;
        produce a draw.io sequence diagram (save as 04-sequence.drawio)
```

---

## Prompt 5: Technology Stack

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Technology Stack section. Apply the grounding rules strictly —
list only technologies that are explicitly declared in manifests, config files,
or source imports. Do not infer from framework conventions.

Create the following subsections:

5.1 Programming Languages — Language, version, and primary use (table)
5.2 Frameworks and Libraries — Name, version, purpose, and licence (table)
5.3 Databases and Data Storage — Engine, version, data type stored,
        and access pattern (table)
5.4 Middleware and Messaging — Message brokers, service meshes, API gateways,
        caches — name, version, role (table)
5.5 Third-Party Services and APIs — External SaaS, cloud services, or APIs
        the system calls (table: Service | Provider | Purpose)
```

---

## Prompt 6: Deployment and Infrastructure

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Deployment and Infrastructure section. Apply the grounding rules strictly.
Also check the repository root for CI/CD configs (.github/workflows/, Jenkinsfile, etc.)
and infrastructure files even if they lie outside the analysis subdirectory.
Produce draw.io XML diagrams for subsections 6.5 and 6.6.

Create the following subsections:

6.1 Deployment Model — Cloud, on-premises, hybrid, or serverless; provider and region(s)
6.2 Infrastructure Components — Servers, networks, load balancers, storage —
        names and roles (table)
6.3 Environment Configuration — Differences between dev, staging, and production
        environments
6.4 Containerisation and Orchestration — Docker images, Kubernetes manifests,
        Helm charts, or equivalent
6.5 Infrastructure Topology — draw.io XML diagram showing cloud regions, VPCs,
        subnets, and services (save as 06-infrastructure.drawio)
6.6 CI/CD Pipeline — Stages, tools, gates, and deployment targets;
        draw.io XML pipeline diagram (save as 06-cicd-pipeline.drawio)
```

---

## Prompt 7: Security

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Security section. Apply the grounding rules strictly for facts about
the codebase. For threat modeling (subsection 7.5), hedged language (may/could/might)
is permitted when describing attack vectors and failure scenarios.

Create the following subsections:

7.1 Security Requirements — Functional and non-functional security requirements
        (table: Requirement | Priority | Source)
7.2 Authentication and Authorisation — Identity providers, token types,
        session management, and RBAC/ABAC model
7.3 Data Protection — Encryption at rest and in transit, key management,
        secrets handling
7.4 Network Security — Firewall rules, network policies, ingress/egress controls, mTLS
7.5 Threat Model — STRIDE or equivalent: assets, threats, and likelihood/impact (table)
7.6 Security Controls and Mitigations — Controls in place mapped to the threats
        identified above
```

---

## Prompt 8: Performance and Scalability

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Performance and Scalability section. Apply the grounding rules strictly
for documented requirements and implemented strategies. Hedged language is permitted
for anticipated bottlenecks and failure scenarios. Produce a draw.io XML diagram
for subsection 8.5.

Create the following subsections:

8.1 Performance Requirements — Target SLAs: response time, throughput, concurrency
        (table: Metric | Target | Measurement Method)
8.2 Caching Strategy — What is cached, where (client/CDN/server), TTL,
        and invalidation approach
8.3 Scalability Strategies — Horizontal vs. vertical scaling decisions per component;
        auto-scaling triggers
8.4 Bottlenecks and Hotspots — Known or anticipated performance bottlenecks
        and mitigation approaches
8.5 Scalability Architecture — draw.io XML diagram illustrating scaling topology
        (save as 08-scalability.drawio)
```

---

## Prompt 9: Reliability and Availability

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Reliability and Availability section. Apply the grounding rules strictly
for documented requirements and implemented patterns. Hedged language is permitted
for failure mode descriptions.

Create the following subsections:

9.1 Reliability Requirements — Uptime targets, error budgets, and fault-tolerance
        SLAs (table)
9.2 Fault Tolerance — Circuit breakers, retries, timeouts, and graceful degradation
        patterns found in the code
9.3 High Availability Strategies — Redundancy, active-active / active-passive topology,
        failover mechanisms
9.4 Disaster Recovery — RTO and RPO targets, backup strategy, and recovery runbooks
        referenced in the repo
9.5 Backup and Restore — What is backed up, frequency, retention, and restore procedure
```

---

## Prompt 10: Maintainability and Extensibility

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Maintainability and Extensibility section.
Apply the grounding rules strictly.

Create the following subsections:

10.1 Code Organisation and Modularity — Directory structure, layer separation,
        and module boundaries
10.2 Documentation Strategy — Inline docs, README coverage, API docs,
        and ADRs present in the repo
10.3 Testing Strategy — Unit, integration, E2E, contract — coverage targets
        and tooling found
10.4 Technical Debt — Known debt items, workarounds, or TODO comments
        that affect maintainability
10.5 Extension Points — Plugin systems, feature flags, hooks, or interfaces
        designed for future extension
```

---

## Prompt 11: Governance and Compliance

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Governance and Compliance section. Apply the grounding rules strictly.
Also check the repository root for licence files (LICENCE, LICENSE, COPYING, NOTICE)
even if they lie outside the analysis subdirectory.

Create the following subsections:

11.1 Governance Model — Ownership, review processes, change control,
        and decision-making bodies
11.2 Compliance Requirements — Regulatory or standards obligations
        (GDPR, SOC 2, ISO 27001, HIPAA, etc.) and evidence of how they are met
11.3 Data Residency and Privacy — Where data is stored, PII handling,
        data classification, and retention policies
11.4 Audit and Logging Requirements — What must be logged for compliance,
        retention periods, and audit trail mechanisms
11.5 Licence Compliance — Open-source licences in use and any obligations they impose
```

---

## Prompt 12: Dependencies and Integrations

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Dependencies and Integrations section. Apply the grounding rules strictly.
Produce a draw.io XML diagram for subsection 12.5.

Create the following subsections:

12.1 Internal Dependencies — Dependencies between internal modules or services
        (table: Consumer | Dependency | Type | Criticality)
12.2 External Dependencies — Third-party systems, SaaS platforms, or cloud services
        the system depends on
12.3 Integration Patterns — Synchronous REST/gRPC, asynchronous messaging,
        webhooks, ETL, file-based, etc.
12.4 API Contracts — Public or shared API definitions (OpenAPI, AsyncAPI, protobuf)
        found in the repo
12.5 Dependency and Integration Diagram — draw.io XML diagram showing all integration
        points (save as 12-dependencies.drawio)
```

---

## Prompt 13: Observability and Monitoring

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Observability and Monitoring section. Apply the grounding rules strictly.
Produce a draw.io XML diagram for subsection 13.6.

Create the following subsections:

13.1 Logging Strategy — Log levels, structured vs. unstructured, log aggregation tools,
        and retention
13.2 Metrics and KPIs — Key metrics collected, instrumentation libraries,
        and storage backend (table: Metric | Tool | Retention)
13.3 Distributed Tracing — Tracing framework (OpenTelemetry, Jaeger, etc.),
        sampling strategy, and trace propagation
13.4 Alerting and Incident Response — Alert rules, notification channels,
        on-call runbooks, and escalation paths found in the repo
13.5 Dashboards and Visualisation — Dashboarding tools referenced
        (Grafana, Datadog, etc.) and what they cover
13.6 Observability Architecture Diagram — draw.io XML diagram of the observability
        stack (save as 13-observability.drawio)
```

---

## Prompt 14: Evolution and Roadmap *(run only if evidence is available)*

```
Analyze the GitHub repository [REPO_URL] (subdirectory: [ANALYSIS_PATH] if applicable)
and generate the Evolution and Roadmap section. Apply the grounding rules strictly —
only document items evidenced by open issues, ADRs, TODOs, or CHANGELOG entries.
Hedged language (may/could/might) is permitted for planned future states
that are grounded in cited issues or ADRs.

Create the following subsections:

14.1 Known Technical Debt — Debt items with architectural impact:
        what they are, why they exist, and estimated effort to resolve
14.2 Planned Enhancements — Features or changes in backlog/issues
        that will affect the architecture
14.3 Migration Strategies — Any in-flight or planned migrations
        (database, platform, framework) with approach and risk
14.4 Architecture Roadmap — Phased timeline of architectural evolution
        (table or narrative)
14.5 Deprecation Plans — Components, APIs, or integrations scheduled for removal
        and their replacement
```

---

## Prompt 15: Conclusion

```
Generate the Conclusion using the completed outputs of all sections produced in this
analysis session — do not re-analyze the repository, and do not reference findings
for any section that was not run.

Create the following subsections:

15.1 Summary of Key Findings — Concise recap of the most significant findings
        from each section that was run; list any skipped sections explicitly
15.2 Architecture Strengths — What the architecture does well, each point citing
        the section and evidence it came from
15.3 Architecture Gaps and Risks — Gaps, weaknesses, or risks surfaced across
        the sections that ran, ranked by severity
15.4 Recommended Next Steps — Concrete, prioritised actions to address the gaps
        and risks above, each traceable to a specific section finding
15.5 Open Questions — Decisions still unmade, N/A subsections, and sections
        not run that may contain relevant information
```

---

## Diagram Format

All diagrams must be valid draw.io XML. Use this skeleton as the base for every diagram file — replace only the `<mxCell>` contents, never the outer structure:

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1"
              connect="1" arrows="1" fold="1" page="1" pageScale="1"
              pageWidth="1169" pageHeight="827" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <!-- Box:  <mxCell id="2" value="Service A" style="rounded=1;whiteSpace=wrap;"
                vertex="1" parent="1">
                <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
              </mxCell> -->
    <!-- Arrow: <mxCell id="3" value="calls" style="edgeStyle=orthogonalEdgeStyle;"
                 edge="1" source="2" target="4" parent="1">
                 <mxGeometry relative="1" as="geometry"/>
               </mxCell> -->
  </root>
</mxGraphModel>
```

Rules:
- Each `<mxCell>` must have a unique numeric `id` starting from `2`
- Use `vertex="1"` for shapes, `edge="1"` for connectors
- Set `parent="1"` on all direct children of `<root>`
- Every opening `<mxCell>` must be closed with `</mxCell>` or self-close with `/>`

---

Happy reverse-engineering!
