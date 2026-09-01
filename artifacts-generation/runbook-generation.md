# Runbook Generation — Comprehensive Prompt Suite

A structured set of prompts for generating evidence-grounded operational runbooks from a GitHub repository. The suite covers deployment, rollback, scaling, troubleshooting, secrets rotation, monitoring, and disaster recovery.

---

## Claude Code skill

This prompt suite powers the `/runbook-generate` Claude Code skill.

**Supported flags:**

| Flag | Format | Default | Description |
|------|--------|---------|-------------|
| Repo URL | First positional value | *(required)* | GitHub repository to analyse |
| `--runbooks` | `--runbooks deploy,troubleshoot` | All 7 | Runbooks to generate |
| `--output` | `--output ./docs/operations` | Current directory | Output directory |
| `--path` | `--path services/api` | Repo root | Monorepo subdirectory to analyse |
| `--force` | flag | Off | Overwrite existing output files |
| `--dry-run` | flag | Off | Preview discovery and planned output without writing |

```
/runbook-generate https://github.com/org/repo
/runbook-generate https://github.com/org/repo --runbooks deploy,rollback
/runbook-generate https://github.com/org/repo --path services/api
/runbook-generate https://github.com/org/repo --output ./docs/operations --force
/runbook-generate https://github.com/org/repo --dry-run
```

---

## Manual usage

Analyse the repository at `[REPO_URL]`. For monorepos, use `[ANALYSIS_PATH]` to identify the service or application being documented.

Before writing anything:

1. Resolve repository access and record the commit SHA, branch, analysis path, and generation timestamp.
2. Resolve every output path and check for conflicts.
3. Stop if requested output files exist and `--force` was not supplied.
4. If the repository contains multiple plausible services and no path is supplied, list them and request a scope choice.
5. Use N/A wherever the repository does not provide supporting evidence.

---

## Grounding and Evidence Rules

Every operational claim and procedure must be traceable to the repository.

### Valid evidence sources

| Evidence Type | Examples |
|---------------|---------|
| Deployment configuration | Dockerfile, docker-compose.yml, Kubernetes manifests, Helm charts, values.yaml |
| CI/CD definitions | .github/workflows/, Jenkinsfile, .gitlab-ci.yml |
| Infrastructure as code | Terraform, CloudFormation, Ansible, Bicep |
| Application code | Health endpoints, startup, shutdown, migrations, error handling |
| Configuration | .env.example, appsettings.json, application.properties, config.yaml |
| Scripts | Deployment, rollback, backup, restore, migration, or operational scripts |
| Documentation | README.md, docs/, CONTRIBUTING.md, operational guides |
| Repository metadata | Issues, PRs, incident documents, commit messages |
| Monitoring configuration | Alert rules, dashboards, logging, metrics, tracing configuration |

### Prohibited behaviours

- Do not infer procedures from industry conventions.
- Do not fill gaps with general DevOps knowledge.
- Do not present assumptions as repository facts.
- Do not fabricate commands, thresholds, contacts, tools, credentials, or recovery objectives.
- Do not claim a control, backup, alert, or escalation path exists without evidence.
- Do not expose secrets, tokens, private keys, or sensitive values in output.

### Citation requirement

Every non-trivial procedure step and factual claim must include an inline citation:

- File: `(scripts/deploy.sh:15-20)`
- Configuration: `(docker-compose.yml -> services.app.deploy)`
- Code: `(src/main.go:45-52)`
- Documentation: `(docs/operations.md § Rollback)`
- Issue or PR: `(#456)`

### N/A rule

For any unsupported procedure or section, write:

> **N/A** — no supporting evidence found in repository

State what information is missing and where operators should document it.

---

## Repository access and discovery

Use one discovery pass before generating runbooks. Record:

- Repository name, URL, visibility, branch, commit SHA, and description.
- Local clone path when cloning is required.
- Analysis path and excluded paths.
- Deployment tools and configuration files.
- CI/CD systems and environments.
- Databases, queues, caches, cloud providers, ports, and external dependencies.
- Health checks, environment variables, secrets references, monitoring, backups, and retention policies.
- Evidence gaps and tool/access failures.

Use the same discovery result for every runbook agent. Agents must restrict citations to the analysis scope unless a repository-root operational file is explicitly required.

---

## Output Structure

The output is:

```
{output-dir}/
  runbooks/
    00-index.md
    01-deployment.md
    02-rollback.md
    03-scaling.md
    04-troubleshooting.md
    05-secrets-rotation.md
    06-monitoring.md
    07-disaster-recovery.md
```

Write only requested runbooks. Omit skipped files entirely. In dry-run mode, write no files.

---

## Prompt 1: Deployment Procedure

```
Analyse [REPO_URL] at [ANALYSIS_PATH] and generate an evidence-grounded deployment runbook.

Create:
1.1 Prerequisites — tools and versions, access, environment variables, and required secrets
1.2 Pre-Deployment Checklist — current health, backup verification, dependencies, and communications
1.3 Deployment Steps — exact commands from CI/CD, scripts, Helm, containers, or manifests
1.4 Post-Deployment Verification — health URLs, expected responses, smoke tests, metrics, and logs
1.5 Deployment Timing — documented duration, windows, and maintenance requirements
1.6 Rollback Decision Criteria — evidence-backed abort conditions and link to Runbook 2

Use placeholders for environment-specific values. Cite every step. Mark undocumented items N/A.
```

## Prompt 2: Rollback Procedure

```
Analyse [REPO_URL] at [ANALYSIS_PATH] and generate an evidence-grounded rollback runbook.

Create:
2.1 Rollback Triggers — documented failure conditions, thresholds, and decision logic
2.2 Rollback Steps — rollback scripts, CI/CD jobs, Helm commands, and migration reversals
2.3 Data Consistency — database, migration, cache, and asynchronous-data implications
2.4 Verification After Rollback — health, smoke tests, metrics, and stability checks
2.5 Rollback Timing — documented duration and RTO

Do not invent rollback commands or data-reversal procedures.
```

## Prompt 3: Scaling Operations

```
Analyse [REPO_URL] at [ANALYSIS_PATH] and generate a scaling runbook.

Create:
3.1 Horizontal Scaling — replicas, HPA/autoscaling, and manual commands
3.2 Vertical Scaling — CPU, memory, instance types, and downtime
3.3 Database Scaling — replicas, connection pools, partitioning, or sharding
3.4 Cache Scaling — cluster expansion and invalidation
3.5 Scaling Verification — metrics and repository load-test procedures

Separate implemented scaling from recommended future actions.
```

## Prompt 4: Troubleshooting Guide

```
Analyse [REPO_URL] at [ANALYSIS_PATH] and generate a troubleshooting guide.

Create:
4.1 Common Issues — repository issues, error handling, TODO/FIXME/HACK items
4.2 Health Check Failures — validation, diagnosis, and evidence-backed resolution
4.3 Log Analysis — storage, patterns, levels, and configured queries
4.4 Performance Issues — metrics, profiling, slow queries, and cache checks
4.5 Connectivity Issues — DNS, TLS, network, firewall, and security-group checks
4.6 Emergency Contacts — CODEOWNERS, maintainers, and support documentation

Use a table with Symptom, Evidence-backed Cause, Diagnostic Steps, and Resolution.
```

## Prompt 5: Secrets Rotation

```
Analyse [REPO_URL] at [ANALYSIS_PATH] and generate a secrets-rotation runbook.

Create:
5.1 Secret Inventory — credentials, API keys, certificates, OAuth secrets, and encryption keys
5.2 Rotation Procedures — generation, update location, restart requirements, and documented zero-downtime flow
5.3 Certificate Renewal — expiry monitoring, renewal, deployment, and verification
5.4 Rotation Verification — tests and documented rollback
5.5 Rotation Schedule — only documented frequencies and expiry warnings

Never reproduce secret values. Cite only names, purposes, and safe evidence locations.
```

## Prompt 6: Monitoring and Alerting

```
Analyse [REPO_URL] at [ANALYSIS_PATH] and generate a monitoring runbook.

Create:
6.1 Monitoring Stack — logging, metrics, tracing, and alerting systems
6.2 Key Metrics — source, threshold, severity, and action
6.3 Alert Response — meaning, diagnosis, resolution, and escalation
6.4 Dashboard Access — documented URLs and access requirements
6.5 On-Call Procedures — rotation, incident response, and escalation configuration

Use a Metric, Threshold, Severity, Action table. Do not invent thresholds.
```

## Prompt 7: Disaster Recovery

```
Analyse [REPO_URL] at [ANALYSIS_PATH] and generate a disaster-recovery runbook.

Create:
7.1 Disaster Scenarios — only scenarios relevant to evidenced architecture
7.2 RTO and RPO — extract from SLA, incident, backup, or recovery evidence
7.3 Backup Procedures — scope, frequency, location, retention, and verification
7.4 Restore Procedures — scripts, database restores, and infrastructure rebuilds
7.5 Failover Procedures — configured region, DNS, database, and verification steps
7.6 Communication Plan — documented stakeholders and channels
7.7 Post-Incident Review — evidence-backed collection and review process

Do not claim that failover or backups exist without repository evidence.
```

---

## Output requirements

### Index file

`00-index.md` must contain:

- `# Operational Runbooks: {repo name}`
- A table of contents linking only generated runbooks.
- System overview from repository evidence.
- Quick reference for documented contacts, URLs, and critical alerts.
- A list of omitted runbooks when `--runbooks` was supplied.
- Commit SHA and ISO 8601 generation timestamp.

### Individual runbook files

Each file must:

- Begin with `# Runbook N: {Title}`.
- Include `[← Runbook Index](00-index.md)` at the top.
- Use `## N.X Section Name` for every section.
- Use fenced code blocks with language identifiers for commands.
- Cite every command and procedure step.
- Use tables for structured information.
- Use `⚠️ WARNING` or `ℹ️ NOTE` callouts for critical information.
- Mark unsupported sections N/A rather than padding them.

### Confirmation and validation

After generation:

1. Validate Markdown fences, tables, headings, and relative links.
2. Verify every command and step has a citation.
3. Verify only requested files exist.
4. Verify terminology and runbook links are consistent.
5. Print a flat confirmation list.
6. Report limited or N/A runbooks, evidence gaps, assumptions, and validation failures.

Example:

```
✓ runbooks/00-index.md
✓ runbooks/01-deployment.md
✓ runbooks/02-rollback.md
⚠ runbooks/04-troubleshooting.md — LIMITED: 2 of 6 sections had evidence
```

