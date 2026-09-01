---
name: threat-model
description: Generate evidence-grounded STRIDE threat models from repositories or system descriptions, including data-flow diagrams, trust boundaries, attack trees, prioritized risk registers, and draw.io plus Markdown deliverables.
allowed-tools: WebFetch, Bash(gh auth status:*), Bash(gh repo view:*), Bash(gh api repos/*:*), Bash(git clone:*), Bash(git rev-parse:*), Bash(git status:*), Read, Glob, Grep, Write, Agent
---

Generate a complete, evidence-grounded STRIDE threat model and matching diagrams. This is an architecture risk assessment, not a penetration test, exploit verification, or formal security certification.

## Arguments

Parse $ARGUMENTS before analysis:

| Argument | Format | Default |
|---|---|---|
| Repository or system | First positional value | Required |
| --output | --output ./threat-model | Current directory |
| --path | --path services/api | Repository root |
| --force | Flag | Off |
| --dry-run | Flag | Off |
| --sections | Comma-separated section names | All | Run only specified analysis sections; list skipped sections in outputs |

Resolve scope, repository access, and output paths before analysis. Resolve every output path and perform an overwrite check before writing. If conflicts exist and --force is absent, list them and stop. Create directories only after the check. If a monorepo has multiple plausible services and no --path is supplied, list them and stop for a scope choice.

## Operating rules
## STRIDE methodology source

Use the Microsoft STRIDE reference as the primary source for category definitions and threat-modeling terminology:

[Microsoft STRIDE threat modeling](https://learn.microsoft.com/en-us/previous-versions/commerce-server/ee823878(v=cs.20)?redirectedfrom=MSDN)

Apply the source definitions for Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege. Cite this source in the methodology section of `threat-model.md`. Treat it as methodological guidance only; it is not evidence that a repository implements a control or contains a threat. Preserve the source URL exactly in the generated references.

- Inspect source, configuration, infrastructure, CI/CD, API schemas, documentation, tests, and dependency metadata.
- Cite every observed fact with a path plus line or section reference.
- Distinguish facts, assumptions, and hypothetical threats. Label assumptions explicitly.
- Do not infer architecture or controls from conventions or general security knowledge. For external system descriptions supplied by the user, analyze them as stated context and label every unverified property as an assumption.
- Use STRIDE: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.
- Preserve stable IDs and terminology across Markdown, diagrams, attack trees, and the risk register.
- Use ISO 8601 timestamps with timezone. Recommend reassessment after major architecture changes, new trust boundaries, new external integrations, authentication or authorization changes, material incidents, or significant data-classification changes.
- Never copy credentials, tokens, private keys, or secrets into output.
- Record repository URL or path, commit SHA, branch, analysis path, timestamp, inspected files, exclusions, and access/tool failures.

For unsupported claims write:

> **N/A** -- no supporting evidence found in the analysis scope

For assumptions write:

> **Assumption** -- [statement]; validate with [owner or artifact]

## Workflow

### 1. Discovery

Identify actors, entry points, assets, processes, data stores, external systems, protocols, environments, trust zones, and security-relevant evidence gaps. Record a citation for each item.

Use stable IDs:

| Prefix | Meaning |
|---|---|
| E | External actor or system |
| P | Process or service |
| D | Data store |
| F | Data flow |
| B | Trust boundary |
| T | Threat |
| AT | Attack-tree node |

### Attacker model

Define attacker profiles before scoring threats:

| Profile | Access and capabilities | Out of scope |
|---|---|---|
| Unauthenticated attacker | Public entry points and network-reachable behavior | Internal credentials |
| Authenticated user | Permissions evidenced for the role | Admin-only capabilities |
| Compromised account | Credentials and sessions available to that account | Unrelated accounts |
| Malicious insider | Access supported by repository or supplied context | Unsupported physical access |
| Compromised dependency/workload | Dependencies or workloads evidenced in scope | Unrelated infrastructure |

State which profiles apply and their assumptions. Tie every likelihood score to an attacker profile.

### 2. Data flows and trust boundaries

Create a canonical inventory:

| ID | Element | Type | Trust zone | Data handled | Evidence |
|---|---|---|---|---|---|
| P-01 | Service name | Process | Zone | Data classes | Citation |
| D-01 | Store name | Data store | Zone | Data classes | Citation |
| E-01 | Actor/system | External entity | Zone | Data classes | Citation |
| F-01 | Source -> destination | Flow | Boundary crossing | Protocol/auth | Citation |
| B-01 | Boundary name | Boundary | Between zones | Reason | Citation |

For every flow record source, destination, direction, protocol, authentication, authorization, encryption, validation, logging, and data classification. Draw a boundary whenever privilege, administrative control, network exposure, identity authority, data sensitivity, or deployment ownership changes.

### STRIDE coverage

Before writing findings, create a coverage matrix for every canonical element and flow:

| Element ID | S | T | R | I | D | E | Rationale or threat IDs |
|---|---|---|---|---|---|---|---|

Use threat IDs in cells. Use N/A only with a rationale. This matrix is the completeness check.

### 3. STRIDE analysis

Analyze every relevant process, store, external entity, and flow. Consider:

- Spoofing: identity, token, session, service-account, or webhook impersonation.
- Tampering: requests, messages, files, configuration, code, or stored data.
- Repudiation: missing identity binding, audit events, timestamps, or tamper resistance.
- Information Disclosure: unauthorized reads, logs/errors, backups, metadata, or transit.
- Denial of Service: resource exhaustion, dependency failure, queues, storage, or rate limits.
- Elevation of Privilege: broken authorization, confused deputy, tenant, workload, or admin escalation.

Record each finding:

| Field | Required content |
|---|---|
| Threat ID | T-001 style stable identifier |
| STRIDE | One category |
| Target | Element or flow ID |
| Scenario | Attacker action and consequence |
| Preconditions | Required access or condition |
| Evidence | Citations and assumptions |
| Existing controls | Evidence-backed controls only; never recommendations |
| Control effectiveness | Effective, Partial, Unknown, or Not evidenced |
| Gaps | Missing or insufficient controls |
| Proposed mitigation | Recommendation, separate from existing controls |
| Likelihood | 1-5 with rationale |
| Impact | 1-5 with rationale |
| Score | Likelihood x Impact |
| Priority | Critical, High, Medium, or Low |
| Mitigation | Specific action and owner if known |
| Residual risk | Rating after mitigation |
| Evidence confidence | High, Medium, or Low |
| Confidence rationale | Why the evidence confidence was assigned |
| Evidence gaps | Missing artifacts or unknowns |

Threats are modeled scenarios, not proof of exploitability. Use hedged language only for hypothetical attack paths.

### 4. Attack trees

Create trees for Critical/High threats and threats with multiple paths. Use a root attacker goal, AND/OR branches, prerequisites, observable evidence, controls, and leaf-to-threat mappings. Use IDs such as AT-001, AT-001-OR-01, and AT-001-LEAF-01.

### 5. Risk prioritization

Calculate inherent risk as likelihood x impact on a 1-5 scale:

| Score | Priority |
|---:|---|
| 20-25 | Critical |
| 12-19 | High |
| 6-11 | Medium |
| 1-5 | Low |

Sort by priority, then score descending. Include residual risk, mitigation status, evidence, and uncertainty. Use N/A rather than inventing a rating.

### Workflow execution

Use six explicit batches: (1) discovery and provenance, (2) canonical modeling, (3) STRIDE and abuse-case analysis, (4) risk scoring, (5) diagram generation, and (6) final consistency validation. Pass the artifacts from each batch to the next. Run independent discovery tasks in parallel only when they cannot create competing inventories. The final consistency batch is mandatory and owns cross-artifact reconciliation. Downstream batches must not rename, renumber, or invent IDs.

### Deterministic naming and IDs

Create IDs in canonical discovery order and never renumber them after the inventory is written. Use zero-padded IDs: E-001, P-001, D-001, F-001, B-001, T-001, and AT-001. Normalize names consistently and preserve an existing ID when an element is renamed; record the old and new names. Reuse stable filenames and IDs on reruns when the underlying element remains present.

### Dry-run behavior

In --dry-run mode, do not create, modify, or delete files. Report the resolved input, access method, commit SHA, analysis path, detected elements and evidence gaps, attacker profiles, planned batches and dependencies, output paths and conflicts, planned diagrams, and validation steps. Stop after printing this plan.

### Partial-failure handling

If any batch fails, record the stage, artifact, error, and affected IDs. Continue only with independent evidence-safe work. Mark dependent outputs incomplete or N/A; never silently omit them or claim success. Include diagram failures in diagrams/README.md and the final summary. A required-batch failure produces a non-success completion summary. Clean up only the temporary clone created by this invocation.
## Required output

Skip file generation for --dry-run; print the planned artifacts and exit. If --sections is used, generate only the requested sections/artifacts, list skipped sections explicitly, and do not infer findings for skipped sections.

Create:

```
{output}/
  threat-model.md
  risk-register.md
  attack-trees.md
  diagrams/
    01-data-flow.drawio
    02-trust-boundaries.drawio
    03-attack-trees.drawio
    04-threat-surface.drawio
    README.md
```

### threat-model.md

Include scope, repository commit or timestamp, methodology, executive summary, top risks, assumptions, system context, inventories, data-flow narrative, STRIDE findings, control coverage, evidence gaps, open questions, review owner, and reassessment triggers. Link to every diagram.

### risk-register.md

Create one Markdown table row per threat with these columns. Keep one row per threat, escape pipe characters inside cells, and sort by priority then score descending:

| ID | Priority | Inherent score | STRIDE | Target | Scenario | Evidence | Existing controls | Control effectiveness | Mitigation | Mitigation status | Residual likelihood | Residual impact | Residual risk | Owner | Status |
|---|---|---:|---|---|---|---|---|---|---|---|---:|---:|---|---|---|

Keep IDs identical across all outputs.

### attack-trees.md

For each tree include the root goal, AND/OR structure, leaf mappings, evidence, controls, unresolved assumptions, and a link to 03-attack-trees.drawio.

## draw.io requirements

Write valid, uncompressed XML beginning with <mxGraphModel and ending with </mxGraphModel>. Use a root containing <mxCell id="0" /> and <mxCell id="1" parent="0" />. Give every cell a unique numeric ID, use vertex="1" for shapes, edge="1" for connectors, and parent="1" for direct children. Include a legend and never put secrets in labels.

Create:

- 01-data-flow.drawio: actors, processes, stores, flows, protocols, and direction.
- 02-trust-boundaries.drawio: trust zones and labeled boundary crossings.
- 03-attack-trees.drawio: prioritized goals, AND/OR branches, leaves, and threat IDs.
- 04-threat-surface.drawio: entry points, exposed assets, controls, and high-priority threats.

After writing each diagram, read it back and run an XML parser. Also verify start/end elements, closed mxCell and mxGeometry tags, unique cell IDs, valid edge references, and mapping to canonical IDs. XML parsing is mandatory; if unavailable, report validation as blocked. If validation fails, replace it with a valid placeholder skeleton and list it in README.md under "Diagrams requiring manual review". Never report a failed diagram as complete.

## Diagram reliability

Use this exact uncompressed draw.io skeleton for every diagram:

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" page="1">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <!-- diagram cells -->
  </root>
</mxGraphModel>
```

Use unique numeric cell IDs across the entire file. Every edge must reference existing source and target cells. Escape XML label content, include a title and legend, and use explicit boundary containers or shapes for trust zones. Do not use labels as identifiers. Every diagram must map its element and threat IDs to the canonical inventories.

The diagram index, `diagrams/README.md`, must contain a table with file, purpose, referenced element IDs, referenced threat IDs, and validation status. Add a separate **Diagrams requiring manual review** table for failures, including the failure reason.

## Evidence and analysis quality

### Provenance

Record repository URL or local path, commit SHA, branch, analysis path, generation timestamp, inspected files, excluded files, inaccessible resources, and tool failures. Require a commit SHA for Git repositories whenever it is available.

### Citation format

Use one consistent citation format:

- `(src/auth/middleware.ts:42-58)`
- `(docker-compose.yml -> services.api.environment)`
- `(docs/security.md § Authentication)`
- `(#123)`

Cite inventory rows, data flows, existing controls, likelihood rationale, impact rationale, and recommendations based on repository issues or TODOs. Do not cite general security knowledge as repository evidence.

### Evidence confidence

Add these fields to every threat:

- Evidence confidence: High, Medium, or Low.
- Confidence rationale.
- Evidence gaps.

Evidence confidence is separate from likelihood and impact. A threat may have high impact but low evidence confidence.

### Data classification and privacy

For every data flow and store, classify handled data as Public, Internal, Confidential, Sensitive Personal Data, Credentials/Secrets, Regulated Data, or N/A. Record exposure locations, logging leakage, retention/deletion concerns, and data-minimization concerns where applicable.

### Abuse cases

In addition to STRIDE, analyze business-logic abuse cases such as tenant isolation failure, workflow manipulation, excessive privilege use, fraud, replay, resource abuse, and race conditions. Map each abuse case to one or more STRIDE threats and label it as an abuse case in the risk register.

### STRIDE coverage

Create a coverage matrix for every canonical process, store, external entity, and flow. Each STRIDE cell must contain threat IDs or N/A with a rationale. Do not claim analysis is complete until every canonical element has a matrix row.
## Final validation

Before completion:

- Validate Markdown fences, tables, headings, and relative links.
- Verify every threat, element, attack-tree ID, and diagram link is consistent.
- Verify every risk-register row maps to a STRIDE finding.
- Verify the STRIDE coverage matrix covers every canonical element and flow.
- Verify existing controls are separated from proposed mitigations.
- Verify provenance includes commit SHA, scope, timestamp, inspected files, and exclusions.
- Verify all diagrams exist and appear in diagrams/README.md.
- Remove only the temporary clone created by this invocation, including after failures.
- Report files, skipped/N/A areas, assumptions, top risks, and manual-review diagrams.

## Output confirmation

Print a flat list of all generated files and warnings:

```
✓ threat-model.md
✓ risk-register.md
✓ attack-trees.md
✓ diagrams/01-data-flow.drawio
✓ diagrams/02-trust-boundaries.drawio
✓ diagrams/03-attack-trees.drawio
✓ diagrams/04-threat-surface.drawio
✓ diagrams/README.md
```
