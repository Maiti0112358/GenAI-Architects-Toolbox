# Compliance Checking - Comprehensive Prompt Suite

A structured set of prompts for assessing a repository against GDPR, SOC 2, ISO 27001, and PCI-DSS. The suite produces framework-specific readiness reports and an evidence matrix showing what is covered, missing, unknown, or requires external evidence.

---

## Claude Code skill

This prompt suite powers the `/compliance-check` Claude Code skill.

**Supported flags:**

| Flag | Format | Default | Description |
|------|--------|---------|-------------|
| Repository or system | First positional value | *(required)* | GitHub URL, local repository, or supplied system context |
| `--frameworks` | `--frameworks gdpr,soc2` | All four | Frameworks to assess |
| `--output` | `--output ./compliance` | Current directory | Output directory |
| `--path` | `--path services/api` | Repository root | Monorepo scope |
| `--force` | flag | Off | Overwrite existing output |
| `--dry-run` | flag | Off | Preview scope and artifacts without writing |

Valid framework names are `gdpr`, `soc2`, `iso27001`, and `pci-dss`.

```
/compliance-check https://github.com/org/repo
/compliance-check https://github.com/org/repo --frameworks gdpr,soc2
/compliance-check https://github.com/org/repo --frameworks pci-dss --path services/payments
/compliance-check https://github.com/org/repo --output ./security/compliance --force
/compliance-check https://github.com/org/repo --dry-run
```

This is an evidence-based readiness assessment, not legal advice, an audit opinion, certification, compliance attestation, or a declaration that an organization is compliant or non-compliant.

---

## Manual usage

Analyse `[REPO_URL]` at `[ANALYSIS_PATH]`. Before assessment:

1. Record repository/path, branch, commit SHA, analysis path, and timestamp.
2. Validate selected framework names.
3. Establish framework version, applicability, scope, and control catalog.
4. For PCI-DSS, establish the cardholder-data environment and payment flows.
5. For ISO 27001, establish edition, ISMS scope, risk methodology, and Statement of Applicability.
6. For SOC 2, establish Trust Services Criteria, service boundary, and assessment period.
7. For GDPR, establish jurisdiction, processing scope, and controller/processor context.
8. Stop and produce a scope-readiness report when any required gate is unknown.

---

## Methodology sources

Use and preserve these sources in generated references:

- GDPR: [GDPR Info](https://gdpr-info.eu/)
- SOC 2: applicable authoritative Trust Services Criteria or organization-provided audit scope.
- ISO 27001: applicable edition and organization-provided Statement of Applicability.
- PCI-DSS: applicable PCI DSS version and ROC/SAQ/CDE scope.

Methodology sources explain requirements; they do not prove that controls exist. Do not reproduce copyrighted standards beyond short summaries.

---

## Grounding and Evidence Rules

Every claim and evidence-matrix row must be traceable to repository evidence, supplied context, or an explicitly identified external evidence requirement.

### Valid evidence sources

| Evidence Type | Examples |
|---------------|---------|
| Source and configuration | Authentication, authorization, logging, encryption, retention, deployment, and network configuration |
| Infrastructure and CI/CD | Terraform, Kubernetes, Docker, workflows, build and deployment jobs |
| Policies and procedures | Security, privacy, access, incident, continuity, supplier, and change-management documents |
| Operational records | Access reviews, test results, incidents, training, vendor reviews, risk registers, and audit records |
| API and data definitions | OpenAPI, schemas, data models, processing inventories, payment flows |
| Repository metadata | CODEOWNERS, issues, PRs, ADRs, commit history |
| Supplied context | User-provided scope, ownership, applicability, and organizational evidence |

### Prohibited behaviours

- Do not infer compliance from framework, technology, naming, or policy-file presence.
- Do not fabricate controls, clauses, evidence, owners, dates, risk scores, or applicability.
- Do not treat missing repository evidence as proof that a control is absent.
- Do not copy secrets, personal data, cardholder data, or sensitive authentication data.
- Do not make legal, audit, or certification conclusions.

### Status values

Use exactly:

| Status | Meaning |
|--------|---------|
| Covered | Current evidence supports the requirement |
| Partially covered | Some control or evidence elements are present |
| Missing control | Reliable evidence indicates the control is absent or ineffective |
| Unknown | Scope, applicability, interpretation, or evidence is unresolved |
| Not applicable | Explicitly supported by scope evidence |
| External evidence required | Repository evidence cannot establish the requirement |
| Evidence insufficient | Evidence is absent or too incomplete to determine control state |

Record control state separately from evidence state:

| Field | Values |
|---|---|
| Control state | Implemented, Partially implemented, Not implemented, Unknown |
| Evidence state | Repository, External, Insufficient, Conflicting |
| Evidence maturity | Policy, Design, Implementation, Operation, Test, External |
| Control effectiveness | Effective, Partial, Ineffective, Unknown |

### Citation requirement

Use citations such as:

- `(src/auth/middleware.ts:42-58)`
- `(docker-compose.yml -> services.api.environment)`
- `(docs/security.md -> Access Control)`
- `(#123)`

Cite every matrix row, existing control, evidence location, risk rationale, and recommended action grounded in repository evidence.

### Sensitive-data handling

Before writing output, redact credentials, tokens, private keys, personal data, card data, authentication material, and confidential incident details. Preserve only safe paths, keys, line references, and control summaries.

---

## Terminology and maintenance

Use these canonical terms everywhere: `PCI-DSS`, `ISO 27001`, `SOC 2`, `Partially covered`, `Missing control`, `Evidence insufficient`, `Unknown`, `Not applicable`, and `External evidence required`. Do not use synonyms as formal status values.

Record catalog release identifier/checksum and report maintenance metadata when known:

| Field | Value |
|-------|-------|
| Report owner | Named only when supplied |
| Technical reviewer | Named only when supplied |
| Compliance/privacy reviewer | Named only when supplied |
| Review date | Date only when known |
| Next review date | Date only when known |
| Approval status | Draft, In review, Approved, or Unknown |
| Reassessment triggers | Framework/version, scope, architecture, vendor, incident, or evidence changes |

Recommend reassessment when evidence becomes stale, a new audit period begins, a framework version changes, a control owner changes, or external evidence expires.
## Scope, provenance, and control catalog

Record:

- Repository URL/path, branch, commit SHA, analysis path, timestamp, inspected/excluded files, and tool failures.
- Framework, version/edition, catalog source, retrieval date, release identifier/checksum, scope, and completeness.
- Business/system context, environments, data classes, vendors, processors, controllers, services, and trust boundaries.
- Applicability decisions and assumptions.
- Evidence owner, currentness, environment, deployment relevance, and freshness.

Load a complete versioned control catalog before scoring. If the catalog is unavailable or incomplete, produce only a scope-readiness report.

---

## Evidence model

For each evidence item record:

| Evidence ID | Artifact | Location | Type | Commit/age | Environment | Frameworks | Confidence | Verification | Freshness | Notes |
|------------|----------|----------|------|------------|-------------|------------|------------|--------------|----------|-------|

Confidence is High, Medium, or Low. Separate:

- Control state: Implemented, Partially implemented, Not implemented, Unknown.
- Evidence state: Repository, External, Insufficient, Conflicting.
- Evidence maturity: Policy, Design, Implementation, Operation, Test, External.
- Control effectiveness: Effective, Partial, Ineffective, Unknown.

For operating-effectiveness evidence, record owner, test procedure, test period, population, result, exception, and environment.

---

## Prompt 1: Discovery and applicability

```
Analyse [REPO_URL] at [ANALYSIS_PATH]. Establish provenance, framework gates, scope, and applicability.

Identify:
- In-scope services, environments, assets, data, vendors, and trust boundaries
- GDPR processing activities, data subjects, roles, purposes, rights, retention, transfers, and processors
- SOC 2 service boundary, Trust Services Criteria, and assessment period
- ISO 27001 edition, ISMS scope, risk methodology, and Statement of Applicability
- PCI-DSS version, ROC/SAQ type, CDE, payment flows, segmentation, and service-provider scope

Stop with a scope-readiness result if a required gate or control catalog is unavailable.
```

## Prompt 2: Evidence collection and mapping

```
Collect repository, supplied, and external evidence. Build a source register and map each selected framework's complete control catalog.

Use stable requirement IDs that include framework and version. Use internal area IDs only when official IDs are unavailable, and label them as internal. Preserve IDs across reruns.

Record evidence state, control state, maturity, currentness, environment, confidence, and conflicts.
```

## Prompt 3: Evidence matrix

```
Create one row per applicable catalog requirement or explicit exclusion:

Requirement ID | Framework | Requirement summary | Applicability | Applicability rationale | Status | Evidence IDs/locations | Evidence maturity | Evidence freshness | Control effectiveness | Gap | Risk | Recommended action | Owner | External evidence

Every Covered or Partially covered row must have suitable evidence references and rationale. Every Not applicable row must have scope evidence, decision owner/date when known, and a reassessment trigger.
```

## Prompt 4: GDPR assessment

```
Assess:
- Controller/processor roles, records of processing, purposes, and lawful basis
- Transparency, notices, consent withdrawal, minimization, accuracy, and retention
- Data-subject rights workflows
- Deletion execution, processors, subprocessors, and international transfers
- Article 32 security of processing
- Breach response, DPIAs, privacy by design/default, DPO, and automated decision-making where applicable

Separate repository evidence, organizational evidence, and legal interpretation requiring a DPO or privacy counsel.
```

## Prompt 5: SOC 2 assessment

```
Assess the supplied scope against applicable Trust Services Criteria:
Security, Availability, Processing Integrity, Confidentiality, and Privacy.

Separate design from operating effectiveness. For each control record phase, owner, population/period, test procedure, test result, and exception. Identify external evidence such as access reviews, change approvals, incident exercises, vendor reviews, training, and monitoring results.
```

## Prompt 6: ISO 27001 assessment

```
Assess:
- ISMS context, scope, leadership, roles, policy, and objectives
- Risk assessment, risk treatment, and Statement of Applicability
- Asset, access, supplier, incident, continuity, change, development, and operations management
- Monitoring, internal audit, management review, corrective action, and continual improvement
- Annex A only for the confirmed edition and applicability statement

Mark Unknown when edition, ISMS scope, risk method, or Statement of Applicability is unavailable.
```

## Prompt 7: PCI-DSS assessment

```
Assess only the established CDE and applicable PCI DSS version:
- Network security, segmentation, secure configuration, and vulnerability management
- Stored/transmitted account-data protection, encryption, and key management
- Malware, secure development, access, authentication, logging, testing, and policies
- Service-provider responsibilities and formally documented compensating controls

If CDE scope, version, or payment flows are unknown, produce a scope-readiness report and do not score requirements.
```

---

## Gap prioritization and conflicts

Prioritize using these fields only when supported:

| Field | Values |
|---|---|
| Impact | Low, Medium, High, Critical |
| Likelihood | Low, Medium, High, Unknown |
| Evidence confidence | High, Medium, Low |
| Risk rationale | Evidence-based explanation |
| Scoring method | Named method or N/A |
| Dependency | Prerequisite control or evidence |
| Scope | Requirement, system, environment, or organization |

Do not calculate numeric scores without a declared scoring method.

Maintain an exceptions/conflicts register:

| Exception ID | Framework | Requirement ID | Conflicting evidence | Resolution | Owner | Status |
|-------------|-----------|----------------|----------------------|------------|-------|--------|

Prefer current production evidence, current deployment configuration, current operational records, source/tests, documentation, historical metadata, and supplied assumptions in that order. Preserve unresolved conflicts.

---

## Output Structure

```
{output}/
  compliance-index.md
  evidence-matrix.md
  gdpr-report.md
  soc2-report.md
  iso27001-report.md
  pci-dss-report.md
  evidence/
    README.md
  exceptions-and-conflicts.md  (only when entries exist)
```

Write reports only for selected frameworks. Always write the index and matrix unless dry-run is used. In dry-run mode, write no files.

### compliance-index.md
Include the report owner, review status, review dates, and reassessment triggers when known.

Include provenance, selected frameworks and versions, catalog metadata, scope, limitations, counts by framework/status, highest-priority gaps, skipped frameworks, report links, and this disclaimer: This is an evidence-based readiness assessment and is not an audit opinion, legal determination, certification, or compliance attestation. Do not convert counts into a compliance percentage or score.

### evidence-matrix.md

Include the full catalog mapping, status legend, source register, control/evidence state fields, external-evidence list, assumptions, applicability decisions, conflicts, owner-validation gaps, and the same non-certification disclaimer as the index.

### Framework reports

Each selected report must:

- Begin with `# {Framework} Compliance Assessment`.
- Include scope, version, catalog completeness, applicability, evidence summary, matrix, gaps, risks, external evidence, conflicts, limitations, and review record.
- State: This is an evidence-based readiness assessment and is not an audit opinion, legal determination, certification, or compliance attestation.

### evidence/README.md

List external evidence needed to close gaps, owner, acceptable evidence type, related requirement IDs, and status. Never store sensitive evidence here.

---

## Validation and confirmation

Before completion:

1. Validate Markdown headings, tables, fences, and relative links.
2. Verify every catalog requirement has exactly one matrix row or explicit exclusion.
3. Verify no duplicate requirement IDs, orphan evidence IDs, or report/matrix mismatches.
4. Verify every Covered or Partially covered row has appropriate evidence maturity, freshness, and effectiveness rationale.
5. Verify every Not applicable row has a complete applicability decision.
6. Verify framework versions, catalog metadata, scope gates, and source URLs are recorded.
7. Verify no secrets or sensitive values appear in output.
8. Report stale evidence, conflicts, inaccessible sources, assumptions, external evidence, and unresolved applicability.
9. Include review owner, reviewer, approval status, review dates, and reassessment triggers only when evidenced.
10. Clean up only the temporary clone created by this invocation.

```
- compliance-index.md
- evidence-matrix.md
- gdpr-report.md
- evidence/README.md
- exceptions-and-conflicts.md (when applicable)
- SOC 2 report - not selected
- PCI-DSS scope - UNKNOWN: CDE not established
```

