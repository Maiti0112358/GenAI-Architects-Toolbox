---
name: compliance-check
description: Assess a remote or local repository against GDPR, SOC 2, ISO 27001, and PCI-DSS requirements, producing framework-specific compliance reports and an evidence matrix showing covered, partially covered, missing, and unknown controls with repository locations. Use for compliance readiness reviews, gap assessments, audit preparation, and evidence discovery.
allowed-tools: WebFetch, Bash(gh auth status:*), Bash(gh repo view:*), Bash(gh api repos/*:*), Bash(git clone:*), Bash(git rev-parse:*), Bash(git status:*), Read, Glob, Grep, Write, Agent
---

Generate an evidence-grounded compliance gap assessment from a GitHub repository or supplied system context. This is a readiness assessment, not legal advice, an audit opinion, or certification.

## Arguments

Parse `$ARGUMENTS` before analysis:

| Argument | Format | Default | Description |
|---|---|---|---|
| Repository or system | First positional value | Required | GitHub URL, local repository, or supplied system description |
| `--frameworks` | `--frameworks gdpr,soc2` | All four | Frameworks to assess: `gdpr`, `soc2`, `iso27001`, `pci-dss` |
| `--output` | `--output ./compliance` | Current directory | Output directory |
| `--path` | `--path services/api` | Repository root | Monorepo analysis path |
| `--force` | Flag | Off | Overwrite existing output |
| `--dry-run` | Flag | Off | Discover scope and planned artifacts without writing |

### Repository input and access

The first positional value may be a remote GitHub URL or a local repository path. Quote local paths containing spaces.

- For `http://` or `https://` input, classify the source as `REMOTE`, resolve the repository through the approved GitHub access strategy, and clone at most once when API access is unavailable or unsuitable.
- For any other input, resolve it to an existing local directory and classify the source as `LOCAL`. Use that directory directly; do not call GitHub APIs, clone it, or remove it. If it is a Git repository, record the canonical path, branch, and commit SHA with local Git commands. For a non-Git directory, record branch and commit SHA as N/A and label the evidence source accordingly.
- Record the original repository URL or canonical local path, access method, commit/branch provenance, analysis path, inspected files, exclusions, and tool failures in every report.
- Clean up only temporary clones created for remote input. Never delete or overwrite the supplied local repository.

### Framework selection semantics

When multiple frameworks are selected, maintain one row per framework requirement. Shared evidence may be referenced by multiple rows but must not merge requirement IDs. The index must report counts by framework and status. Unselected framework reports must not be created and must be listed as skipped. A single-framework run still produces the same evidence-register and matrix schema.
Validate every framework name. If invalid, stop with:
> Error: Invalid framework names. Valid values are: gdpr, soc2, iso27001, pci-dss.

Resolve repository access, commit SHA, branch, analysis path, output paths, and timestamp before analysis. If multiple monorepo services are plausible and no path is supplied, list them and stop for a scope choice. Check all output conflicts and stop unless `--force` is supplied.

## Methodology sources

Use the following as methodology sources and preserve their URLs in generated references:

- GDPR: [GDPR Info](https://gdpr-info.eu/)
- SOC 2: use only an applicable authoritative standard, organization-provided criteria, or supplied audit scope. Do not claim a specific AICPA criterion unless the source or scope is available.
- ISO 27001: use the applicable edition and organization-provided statement of applicability when available. Do not invent control applicability.
- PCI-DSS: use the applicable PCI DSS version and supplied cardholder-data environment scope when available.

Methodology sources explain requirements; they are not evidence that the repository satisfies them. Do not reproduce copyrighted standards beyond short requirement summaries.

### Control-catalog acquisition

Before scoring, obtain a complete control catalog through one of these approved paths:

1. A bundled, versioned catalog included with the skill.
2. A user-provided catalog or audit scope.
3. An authoritative source retrieved with WebFetch.

Record framework, version/edition, catalog source, retrieval date, release identifier or checksum, scope, and completeness. If the catalog cannot be verified as complete, produce only a scope-readiness report and do not present a generic checklist as an assessment. Do not reproduce copyrighted standards beyond short requirement summaries.
## Assessment gates

Do not begin framework scoring until the applicable version/edition, assessment scope, and control source are established:

- GDPR: confirm jurisdiction, processing scope, controller/processor role, and applicable legal context.
- SOC 2: confirm Trust Services Criteria scope, service boundaries, and assessment period.
- ISO 27001: confirm edition, ISMS scope, risk methodology, and Statement of Applicability.
- PCI-DSS: confirm version, ROC/SAQ type, cardholder-data environment, payment flows, segmentation assumptions, and service-provider scope.

If a gate cannot be established, produce a scope-readiness report and mark affected requirements **Unknown**. Do not present a generic checklist as a framework assessment.

- Inspect source, configuration, infrastructure, CI/CD, dependencies, documentation, logging, access control, backup, privacy, and operational artifacts.
- Cite every factual claim and every evidence-matrix entry with a repository path plus line, key, or section reference.
- Distinguish implemented evidence, documented intent, supplied context, assumptions, and missing evidence.
- Do not infer compliance from technology choice, naming, framework defaults, or the presence of a policy file alone.
- Never expose credentials, tokens, private keys, personal data, card data, or secret values.
- Do not declare the organization compliant or non-compliant. Report evidence status and gaps.
- Use ISO 8601 timestamps with timezone and record repository URL/path, commit SHA, branch, analysis path, inspected files, exclusions, and tool failures.

For unsupported evidence write:

> **N/A** — no supporting evidence found in the analysis scope

For unverified supplied context write:

> **Assumption** — [statement]; validate with [owner or artifact]

### Sensitive-data handling

Before writing any output, scan evidence and generated text for credentials, tokens, private keys, personal data, cardholder data, authentication material, and confidential incident details. Replace values with `[REDACTED]`. Preserve only the minimum safe artifact path, key name, line reference, or control summary needed to locate evidence. Never copy raw logs or sensitive records into reports. Mark evidence as reviewed-but-redacted when applicable.
## Terminology

Use these exact status values everywhere: `Covered`, `Partially covered`, `Missing`, `Unknown`, `Not applicable`, and `External evidence required`. Use `PCI-DSS`, `ISO 27001`, and `SOC 2` consistently. Do not replace these values with synonyms such as `Partial`, `N/A`, or `Evidence required externally` except in explanatory prose.
### Control and evidence state

Record control state separately from evidence state:

| Field | Values |
|---|---|
| Control state | Implemented, Partially implemented, Not implemented, or Unknown |
| Evidence state | Repository evidence, External evidence, Insufficient evidence, or Conflicting evidence |
| Evidence environment | Production, Staging, Development, Organizational, or Unknown |
| Evidence maturity | Policy, Design, Implementation, Operation, Test, or External |
| Control effectiveness | Effective, Partial, Ineffective, or Unknown |

Absence of repository evidence does not prove that a control is absent. Use Unknown or External evidence required unless reliable scope evidence supports Missing.
## Evidence status model

Use these statuses consistently:

| Status | Meaning |
|---|---|
| Covered | Direct, current evidence supports the mapped requirement |
| Partially covered | Some required evidence or control elements are present |
| Missing | No supporting evidence was found |
| Unknown | Scope, applicability, or requirement interpretation is unresolved |
| Not applicable | Applicability is explicitly supported by scope evidence |
| External evidence required | Repository evidence cannot establish the requirement |

Never use Covered when only a policy statement exists but implementation or operation evidence is required. Record evidence age or commit when available.

## Workflow

### 1. Discovery and scope

Record:

- Repository identity, commit, branch, analysis path, and provenance.
- Business/system context supplied by the user.
- Data types: personal data, sensitive personal data, payment/cardholder data, credentials, financial data, and telemetry.
- Data subjects, customers, regions, processors, controllers, vendors, and external services where evidenced.
- Applicable environments, assets, services, trust boundaries, and repositories.
- Compliance scope assumptions, exclusions, and evidence gaps.

For PCI-DSS, identify the cardholder data environment and payment flows. For GDPR, identify processing activities, data subjects, purposes, lawful-basis evidence, rights workflows, retention, transfers, processors, and breach-response evidence. For SOC 2 and ISO 27001, identify in-scope services, policies, risk-management evidence, access controls, change management, operations, monitoring, incident response, and supplier controls.

### Evidence testing and conflicts

For evidence relevant to operating effectiveness, record control owner, test procedure, test period, population, test result, exception, environment, timestamp, and currentness. Apply these fields to all frameworks where operational evidence matters, not only SOC 2.

When evidence conflicts, preserve the conflict and record both sources. Prefer current production evidence, then current deployment configuration, current operational records, source/tests, documentation/policy, historical metadata, and supplied assumptions. Do not silently resolve contradictions.
### 2. Evidence collection

Create a source register:

| Evidence ID | Artifact | Location | Type | Commit/age | Frameworks | Notes |
|---|---|---|---|---|---|---|

Inspect repository evidence such as policies, procedures, code, configuration, IaC, CI/CD, access controls, security tooling, logs/metrics configuration, tickets, training records, vendor assessments, risk registers, and incident documents. Mark evidence that must be supplied externally.

### Requirement ID rules

Use official requirement IDs only when the applicable source version and catalog are known. Include the version in the control-catalog metadata. When an official ID is unavailable, use a clearly marked internal area ID such as `GDPR-AREA-RETENTION`; never make it look like an official clause. Preserve IDs across reruns and maintain a mapping table from internal IDs to official clauses.
### 3. Framework mapping

Load or receive the complete applicable control catalog for each selected framework and version. Record the catalog source, version, retrieval date, and scope. Create one matrix row for every catalog requirement or an explicit exclusion row with an applicability decision. If the catalog is unavailable or incomplete, stop framework scoring and report the assessment as limited.

Map each selected framework to assessable requirement areas. Use requirement IDs that identify the framework and source version, for example `GDPR-ART-32`, `SOC2-CC6`, `ISO27001-A.5.15`, or `PCI-Req-8`. Do not fabricate clause numbers; if the applicable edition or criteria is unavailable, use a clearly labeled requirement area and mark the mapping Unknown.

### 4. Evidence matrix

Create one row per selected requirement or requirement area:

| Requirement ID | Framework | Requirement summary | Applicability | Applicability rationale | Status | Evidence IDs/locations | Evidence maturity | Evidence freshness | Control effectiveness | Gap | Risk | Recommended action | Owner | External evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

The matrix must answer: what is covered, what is missing, and where evidence can be found. Separate repository evidence from external evidence required. Include rationale for Covered, Partially covered, Unknown, and Not applicable statuses. Every Not applicable result must include an applicability decision, scope evidence, decision owner, decision date, and reassessment trigger.

### Applicability decisions

For every Not applicable or scope-excluded requirement, record:

| Field | Required content |
|---|---|
| Applicability decision | Applicable, Not applicable, or Unknown |
| Rationale | Why the decision was made |
| Scope evidence | Artifact, location, or supplied context |
| Decision owner | Named owner only when supplied |
| Decision date | Date only when known |
| Reassessment trigger | Change that requires reconsideration |

Never infer Not applicable from the absence of code or configuration. Use Unknown when the scope evidence is insufficient.

### Risk schema

For every gap, record:

| Field | Values |
|---|---|
| Impact | Low, Medium, High, or Critical |
| Likelihood | Low, Medium, High, or Unknown |
| Risk rationale | Evidence-based explanation |
| Scoring method | Named method, or N/A |
| Dependency | Prerequisite control or evidence |
| Scope | Requirement, system, environment, or organization |

Do not calculate numeric scores unless the scoring method is explicitly selected. Do not equate missing repository evidence with a confirmed control failure.

### 5. Gap prioritization

Prioritize gaps using:

- Impact: Low, Medium, High, Critical.
- Evidence confidence: High, Medium, Low.
- Scope: requirement, system, environment, or organization.
- Dependency: prerequisite controls or evidence.
- Recommended owner and target date when supplied.

Do not invent risk scores, owners, dates, audit scope, or applicability. If numeric scoring is requested, document the scoring method and assumptions.

## Framework-specific report prompts

### GDPR evidence requirements

For each applicable processing activity, identify evidence for:

- Controller/processor role, records of processing, and processing purpose.
- Lawful basis, transparency/privacy notices, consent withdrawal, and data minimization.
- Data-subject access, correction, deletion, portability, objection, and restriction workflows.
- Retention schedules and deletion execution.
- Processor/subprocessor contracts and oversight.
- International transfers and safeguards.
- Security of processing under Article 32.
- Breach detection, notification workflow, and response timing.
- DPIAs, privacy by design/default, DPO responsibilities, and automated decision-making where applicable.

Separate repository evidence, organizational evidence, legal interpretation, and evidence required from a DPO or privacy counsel.

### GDPR report

Assess, where applicable:

- Roles and records of processing.
- Lawful basis, purpose limitation, minimization, accuracy, retention, and deletion.
- Data-subject rights and request workflows.
- Privacy notices, consent, and preference management.
- Processor and subprocessor management.
- International transfers and safeguards.
- Security of processing under Article 32.
- Breach detection, notification, and response.
- DPIAs, privacy by design, DPO/contact evidence, and governance.

Use GDPR Info as the primary source reference. Do not determine legal applicability without supplied context.

### SOC 2 evidence requirements

Separate design evidence from operating-effectiveness evidence. Add these fields to each applicable control:

| Field | Required content |
|---|---|
| Evidence phase | Design, Operating effectiveness, or Both |
| Control owner | Named only when supplied |
| Population/period | Population and review period when known |
| Test procedure | How operation was or must be tested |
| Test result | Pass, Exception, Not tested, or Unknown |
| Exception | Evidence-backed exception or N/A |

Identify organizational records commonly needed outside the repository: access reviews, change approvals, incident exercises, vendor reviews, risk assessments, training, and monitoring results.

### SOC 2 report

Assess the supplied scope against applicable Trust Services Criteria:

- Security/common criteria.
- Availability.
- Processing integrity.
- Confidentiality.
- Privacy.

Separate design evidence from operating-effectiveness evidence. Identify evidence commonly requiring organizational records, such as access reviews, change approvals, incident exercises, vendor reviews, risk assessments, training, and monitoring results. Do not claim SOC 2 readiness or certification from repository evidence alone.

### ISO 27001 scope gates

Do not produce an Annex A control assessment until the edition, ISMS scope, risk methodology, risk-treatment plan, and Statement of Applicability are known. Assess these ISMS elements separately:

- Organizational context, interested parties, leadership, roles, policy, and objectives.
- Risk assessment, risk treatment, and Statement of Applicability.
- Asset, access, supplier, incident, continuity, change, secure-development, and operational management.
- Monitoring, internal audit, management review, corrective action, and continual improvement.

Mark affected controls Unknown when the edition, ISMS scope, or Statement of Applicability is unavailable.

### ISO 27001 report

Assess, according to the applicable edition and statement of applicability:

- ISMS scope and context.
- Leadership, roles, policy, and objectives.
- Risk assessment and treatment.
- Asset, access, supplier, incident, continuity, and change management.
- Secure development and operations.
- Monitoring, internal audit, corrective action, and continual improvement.
- Annex A control areas only when the applicable edition is known.

Mark Unknown when the edition, scope, or statement of applicability is unavailable.

### PCI-DSS scope gates

Before scoring PCI-DSS requirements, establish the PCI DSS version, ROC/SAQ type, cardholder-data environment, payment channels, account-data flows, segmentation assumptions, and service-provider responsibilities. If these are unavailable, produce a PCI-DSS scope-readiness report and mark requirement applicability Unknown.

Assess compensating controls only when formally documented. Do not reproduce cardholder data or sensitive authentication data.
### PCI-DSS report

Assess only the defined cardholder data environment and applicable PCI DSS version:

- Network security and segmentation.
- Secure configurations and vulnerability management.
- Protection of stored/transmitted cardholder data.
- Encryption and key management.
- Malware, secure development, access control, authentication, logging, testing, and policy.
- Service-provider responsibilities and evidence.
- Compensating controls only when formally documented.

Do not reproduce cardholder data in reports. Mark the assessment Unknown when CDE scope or payment flows are not established.

## Agent workflow and partial failures

Use these batches:

1. Scope and provenance.
2. Evidence collection and source register.
3. Framework control-catalog mapping.
4. Evidence classification and applicability decisions.
5. Gap prioritization.
6. Framework report generation.
7. Cross-framework consistency and validation.

Pass the canonical provenance, control catalog, evidence register, and applicability decisions between batches. Downstream batches must not invent requirement IDs or change statuses without recording a rationale.

If a framework source, repository, artifact, or batch fails, record the stage, framework, artifact, error, and affected requirement IDs. Continue only with independent frameworks and mark dependent rows Unknown or External evidence required. Do not silently omit rows or report successful completion when a required batch fails.
## Reassessment and review

Recommend reassessment after:

- A framework-version or audit-scope change.
- A new processing activity, payment flow, vendor, or subprocessor.
- A major architecture, authentication, authorization, or data-residency change.
- A material security or privacy incident.
- A significant retention, deletion, or data-classification change.
- A change to the ISO 27001 Statement of Applicability or PCI-DSS CDE boundary.
- Evidence becomes stale, a new audit period begins, a control owner changes, or external evidence expires.

Include a review record:

| Field | Value |
|---|---|
| Technical reviewer | Named only when supplied |
| Compliance/privacy reviewer | Named only when supplied |
| Control owner | Named only when supplied |
| Evidence owner | Named only when supplied |
| Approval status | Draft, In review, Approved, or Unknown |
| Review date | Date only when known |
| Next review date | Date only when known |
| Reassessment triggers | Applicable triggers from the list above |

Never invent reviewer names, ownership, approval, or dates.
## Required output

Skip file generation in `--dry-run`; report resolved scope, selected frameworks, planned batches, output paths, conflicts, and evidence categories, then stop.

Create:

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
```

Write only reports for selected frameworks. The index and evidence matrix are always written unless dry-run is used.

### Management summary

Include these counts without presenting them as compliance percentages:

- Total catalog requirements.
- Applicable, not applicable, and unknown requirements.
- Covered, partially covered, missing, and external-evidence-required rows.
- Rows supported by repository evidence versus organizational/external evidence.
- Rows with current evidence.
- Assessment limitations, excluded scope, and unresolved framework-version questions.

Do not convert these counts into a certification score or legal conclusion.

### compliance-index.md

Include scope, provenance, selected frameworks, methodology links, assessment limitations, summary counts by status/framework, highest-priority gaps, skipped frameworks, and links to generated reports.

### exceptions-and-conflicts.md

Create an exceptions and conflicts register when evidence is contradictory, stale, unavailable, or formally excepted:

| Exception ID | Framework | Requirement ID | Conflicting evidence | Resolution | Owner | Status |
|---|---|---|---|---|---|---|

Include this file in the output when it contains entries. Each conflict must also be linked from the affected matrix row.
### evidence-matrix.md

Include the complete matrix, a status legend, evidence register, external-evidence list, assumptions, and gaps requiring owner validation. Keep requirement IDs and evidence IDs stable across all reports.

### Framework report schema

Every selected framework report must use this order:

1. Scope and applicability.
2. Framework version, edition, catalog source, and completeness.
3. Evidence summary and environment coverage.
4. Requirement matrix.
5. Gaps, risks, and dependencies.
6. External evidence required.
7. Conflicts, assumptions, and limitations.
8. Review and approval record.

Each report must include: This is an evidence-based readiness assessment and is not an audit opinion, legal determination, certification, or compliance attestation.
### Framework reports

Each selected report must:

- Begin with `# {Framework} Compliance Assessment`.
- State framework version/edition and applicability status.
- Link back to `compliance-index.md` and `evidence-matrix.md`.
- Summarize covered, partially covered, missing, unknown, and external-evidence-required items.
- Include requirement mappings, evidence locations, gaps, recommended actions, owners/status where known, and limitations.
- Avoid legal conclusions and certification claims.

### evidence/README.md

List every external evidence item needed to close a gap, its requested owner, acceptable evidence type, related requirement IDs, and status. Never store sensitive evidence in this directory.

### Cross-artifact validation

Before completion, verify:

- Every applicable catalog requirement has exactly one matrix row.
- No duplicate requirement IDs exist.
- No evidence ID is orphaned or points to an absent artifact.
- Every report finding appears in the matrix.
- Every matrix row appears in the relevant framework report.
- Every Covered row has the required evidence maturity, freshness, and effectiveness rationale.
- Every Not applicable row has a complete applicability decision record.
- Shared evidence references remain traceable to their source register entries.

## Validation and confirmation

Before completion:

1. Validate Markdown headings, tables, fences, and relative links.
2. Verify every matrix row has a framework, requirement ID, applicability decision, status, evidence or an explicit N/A, and evidence maturity.
3. Verify every Covered or Partially covered row has evidence references, appropriate evidence maturity, freshness, and control-effectiveness rationale.
4. Verify every selected framework has exactly one report.
5. Verify unselected framework reports were not written.
6. Verify no secrets, personal data, card data, or sensitive values appear in output.
7. Verify requirement IDs and evidence IDs are consistent across all artifacts. Verify every applicable control-catalog requirement has exactly one matrix row, with no duplicate or orphan IDs.
8. Report inaccessible sources, assumptions, external evidence required, and unresolved applicability.

Print a flat confirmation list:

```
✓ compliance-index.md
✓ evidence-matrix.md
✓ gdpr-report.md
✓ evidence/README.md
⚠ soc2-report.md — not selected
⚠ PCI-DSS scope — UNKNOWN: cardholder data environment not established
```

