# STRIDE Threat Modeling — Comprehensive Prompt Suite

A structured set of prompts for generating an evidence-grounded STRIDE threat model from a repository or supplied system description. The suite produces data-flow and trust-boundary diagrams, attack trees, a prioritized risk register, and Markdown documentation.

---

## AI assistant skill

This prompt suite corresponds to the `/threat-model` AI assistant skill.

The first positional input may be a remote repository URL, a local repository path, or a supplied system description. Quote local paths containing spaces. Inspect local paths directly and record Git provenance when available; never clone or delete the supplied local repository.

**Supported flags:**

| Flag | Format | Default | Description |
|------|--------|---------|-------------|
| Repository or system | First positional value | *(required)* | GitHub URL, local repository, or supplied system description |
| `--output` | `--output ./threat-model` | Current directory | Output directory |
| `--path` | `--path services/api` | Repository root | Monorepo subdirectory to analyse |
| `--sections` | `--sections discovery,stride` | All | Run only selected analysis sections |
| `--force` | flag | Off | Overwrite existing output files |
| `--dry-run` | flag | Off | Preview scope, batches, conflicts, and artifacts without writing |

```
/threat-model https://github.com/org/repo
/threat-model https://github.com/org/repo --path services/api
/threat-model https://github.com/org/repo --sections discovery,stride,risk
/threat-model https://github.com/org/repo --output ./security/threat-model --force
/threat-model https://github.com/org/repo --dry-run
```

This is an architecture risk assessment, not a penetration test, exploit verification, or formal security certification.

---

## Manual usage

Analyse `[REPOSITORY_INPUT]` at `[ANALYSIS_PATH]`, or analyse the supplied system description when no repository is available.

Before writing anything:

1. Resolve scope, repository access, output paths, commit SHA, branch, and ISO 8601 timestamp.
2. Check all output conflicts; stop unless `--force` is supplied.
3. If multiple monorepo services are plausible, list them and request a scope choice.
4. Define attacker profiles and trust zones before scoring threats.
5. Use N/A for unsupported claims and label unverified supplied-system details as assumptions.

---

## STRIDE methodology

Use the Microsoft STRIDE reference as the primary source for category definitions:

[Microsoft STRIDE threat modeling](https://learn.microsoft.com/en-us/previous-versions/commerce-server/ee823878(v=cs.20)?redirectedfrom=MSDN)

Use it for Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege terminology. Cite this URL in the methodology section of `threat-model.md`. Treat it as methodology guidance, not repository evidence.

---

## Grounding and Evidence Rules

Every observed fact must be traceable to the repository or explicitly supplied system context.

### Valid evidence sources

| Evidence Type | Examples |
|---------------|---------|
| Source code | Authentication, authorization, validation, logging, handlers |
| Configuration | Docker, Kubernetes, Helm, network, identity, secrets references |
| Infrastructure as code | Terraform, CloudFormation, Ansible, Bicep |
| API and schemas | OpenAPI, AsyncAPI, protobuf, message schemas |
| CI/CD and dependencies | Workflows, build manifests, lockfiles, dependency metadata |
| Documentation | README.md, docs/, ADRs, security and operational guides |
| Repository metadata | Issues, PRs, TODOs, incident documents, commit history |
| Supplied context | User-provided architecture facts, explicitly labeled assumptions |

### Prohibited behaviours

- Do not infer architecture or controls from naming conventions or general security knowledge.
- Do not present assumptions as repository facts.
- Do not fabricate assets, flows, threats, controls, scores, owners, or mitigations.
- Do not copy secrets, tokens, private keys, or sensitive values into output.
- Do not cite the Microsoft STRIDE source as evidence that a repository implements a control.

### Citation requirement

Cite every inventory row, data flow, existing control, likelihood rationale, impact rationale, and repository-grounded recommendation:

- File: `(src/auth/middleware.ts:42-58)`
- Configuration: `(docker-compose.yml -> services.api.environment)`
- Documentation: `(docs/security.md § Authentication)`
- Issue or PR: `(#123)`

### N/A rule

For unsupported information write:

> **N/A** — no supporting evidence found in the analysis scope

For unverified supplied context write:

> **Assumption** — [statement]; validate with [owner or artifact]

---

## Discovery and provenance

Record:

- Repository URL/path, visibility, branch, commit SHA, analysis path, and timestamp.
- Inspected files, excluded files, inaccessible resources, and tool failures.
- Actors, entry points, assets, processes, data stores, external systems, protocols, environments, and trust zones.
- Security-relevant assumptions and evidence gaps.
- Attacker profiles: unauthenticated attacker, authenticated user, compromised account, malicious insider, and compromised dependency/workload where applicable.

Use stable zero-padded IDs in discovery order: E-001, P-001, D-001, F-001, B-001, T-001, and AT-001. Never renumber an existing element on reruns; record renamed elements in consistency notes.

---

## Output Structure

The output is:

```
{output-dir}/
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

Write only requested sections and artifacts when `--sections` is supplied. List skipped sections explicitly. In dry-run mode, write no files.

---

## Prompt 1: Discovery and Canonical Model

```
Analyse [REPOSITORY_INPUT] at [ANALYSIS_PATH]. Establish provenance and create the canonical inventory.

Identify:
- External actors and systems
- Processes and services
- Data stores and data classes
- Data flows, protocols, direction, authentication, authorization, encryption, validation, and logging
- Trust zones and boundary crossings
- Entry points, assets, environments, and evidence gaps
- Applicable attacker profiles and scope assumptions

Assign stable IDs in discovery order. Cite every item. For each store and flow classify data as Public, Internal, Confidential, Sensitive Personal Data, Credentials/Secrets, Regulated Data, or N/A.
```

## Prompt 2: Data Flow and Trust Boundaries

```
Using the canonical inventory, describe how data moves through the system.

Create:
2.1 Element inventory — ID, name, type, trust zone, data handled, and evidence
2.2 Flow inventory — source, destination, direction, protocol, identity, authorization, encryption, validation, logging, and evidence
2.3 Trust boundaries — boundary ID, zones separated, privilege or ownership change, and evidence
2.4 Privacy impact — exposure locations, logging leakage, retention/deletion, and minimization concerns
2.5 Data-flow and trust-boundary diagram links

Do not add flows or boundaries that are not supported by repository or supplied-context evidence.
```

## Prompt 3: STRIDE and Abuse Cases

```
Using the canonical inventory and Microsoft STRIDE definitions, analyse every relevant process, store, external entity, and flow.

Consider:
- Spoofing — identity, token, session, service-account, or webhook impersonation
- Tampering — requests, messages, files, configuration, code, or stored data
- Repudiation — missing identity binding, audit events, timestamps, or tamper resistance
- Information Disclosure — unauthorized reads, logs/errors, backups, metadata, or transit
- Denial of Service — resource exhaustion, dependency failure, queues, storage, or rate limits
- Elevation of Privilege — broken authorization, confused deputy, tenant, workload, or admin escalation

Also analyse business-logic abuse cases: tenant isolation, workflow manipulation, excessive privilege, fraud, replay, resource abuse, and race conditions.

For every element create a STRIDE coverage matrix. Each cell contains threat IDs or N/A with a rationale. Record each threat with ID, category, target, scenario, preconditions, evidence, existing controls, control effectiveness, gaps, proposed mitigation, likelihood, impact, score, priority, residual risk, evidence confidence, and evidence gaps.
```

## Prompt 4: Attack Trees

```
Create attack trees for Critical and High threats and threats with multiple paths.

For each tree include:
- Root attacker goal
- AND/OR branches
- Preconditions and observable evidence
- Leaf-to-threat mappings
- Existing controls and proposed mitigations
- Unresolved assumptions

Use AT-001, AT-001-OR-01, and AT-001-LEAF-01 IDs. Label trees as modeled scenarios, not proof of exploitability.
```

## Prompt 5: Risk Register

```
Create a sortable risk register with one row per threat.

Use likelihood and impact from 1-5 and calculate score as likelihood x impact:

20-25 Critical
12-19 High
6-11 Medium
1-5 Low

Use these columns:

ID | Priority | Inherent score | STRIDE | Target | Scenario | Evidence | Existing controls | Control effectiveness | Mitigation | Mitigation status | Residual likelihood | Residual impact | Residual risk | Owner | Status

Sort by priority, then score descending. Separate observed controls from proposed mitigations. Use N/A where evidence cannot support a rating.
```

## Prompt 6: Diagram Generation

```
Generate four valid, uncompressed draw.io XML diagrams from the canonical model:

01-data-flow.drawio — actors, processes, stores, flows, protocols, and direction
02-trust-boundaries.drawio — trust zones and labeled boundary crossings
03-attack-trees.drawio — prioritized goals, AND/OR branches, leaves, and threat IDs
04-threat-surface.drawio — entry points, exposed assets, controls, and high-priority threats

Use the fixed mxGraphModel/root skeleton, unique numeric cell IDs, existing edge targets, escaped XML labels, titles, legends, and canonical element/threat IDs. Never put secrets in labels.
```

---

## Output requirements

### threat-model.md

Include:

- Scope, provenance, methodology, and Microsoft STRIDE reference.
- Executive summary, top risks, attacker profiles, assumptions, and open questions.
- Canonical inventories, data-flow narrative, trust boundaries, classifications, and privacy impact.
- STRIDE findings, coverage matrix, control coverage, evidence gaps, and abuse cases.
- Links to every generated diagram and documented reassessment triggers.

### risk-register.md

Use one Markdown table row per threat with the exact schema specified in Prompt 5. Keep IDs consistent with every other artifact.

### attack-trees.md

Document each tree's root, AND/OR structure, leaf mappings, evidence, controls, assumptions, and diagram link.

### diagrams/README.md

Include a table with file, purpose, referenced element IDs, referenced threat IDs, and validation status. Add a separate **Diagrams requiring manual review** table with failure reasons.

---

## Agent workflow and validation

Use six batches:

1. Discovery and provenance.
2. Canonical modeling.
3. STRIDE and abuse-case analysis.
4. Risk scoring.
5. Diagram generation.
6. Final consistency validation.

The final consistency pass is mandatory. Downstream agents must not rename, renumber, or invent IDs.

In dry-run mode, report resolved input, access method, commit SHA, scope, detected elements, attacker profiles, planned batches, conflicts, artifacts, and validation steps, then stop without writing.

If a batch fails, record the stage, artifact, error, and affected IDs. Continue only with independent evidence-safe work. Mark dependent outputs incomplete or N/A and report a non-success completion summary. Clean up only the temporary clone created by this invocation.

---

## Diagram Format and Validation

Use this skeleton for every diagram:

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" page="1">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <!-- diagram cells -->
  </root>
</mxGraphModel>
```

After writing each diagram:

1. Read it back.
2. Parse it as XML; parsing is mandatory.
3. Verify the start and end elements.
4. Verify every `mxCell` and `mxGeometry` is closed.
5. Verify unique numeric IDs and valid edge references.
6. Verify canonical element and threat IDs are mapped.
7. Report failures in `diagrams/README.md`; never report a failed diagram as complete.

---

## Confirmation and validation

After generation:

1. Validate Markdown fences, tables, headings, and relative links.
2. Verify every threat maps to the coverage matrix and risk register.
3. Verify existing controls are separate from proposed mitigations.
4. Verify provenance fields are complete.
5. Verify diagrams exist, parse, and appear in the diagram index.
6. Report skipped/N/A sections, assumptions, evidence gaps, top risks, and manual-review diagrams.

Example:

```
✓ threat-model.md
✓ risk-register.md
✓ attack-trees.md
✓ diagrams/01-data-flow.drawio
✓ diagrams/02-trust-boundaries.drawio
✓ diagrams/03-attack-trees.drawio
✓ diagrams/04-threat-surface.drawio
✓ diagrams/README.md
⚠ diagrams/04-threat-surface.drawio — VALIDATION FAILED: invalid edge reference
```

