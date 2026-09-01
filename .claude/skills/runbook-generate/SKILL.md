---
description: Generate comprehensive operational runbooks from a GitHub repository including deployment, troubleshooting, scaling, and incident response procedures
allowed-tools: WebFetch, Bash(gh auth status:*), Bash(gh repo view:*), Bash(gh api repos/*:*), Bash(git clone:*), Bash(Remove-Item:*), Read, Glob, Grep, Write, Agent
---

Generate operational runbooks for a software system by analyzing its GitHub repository.

## Arguments

Parse `$ARGUMENTS` for the following before doing anything else:

| Argument | Format | Default | Description |
|----------|--------|---------|-------------|
| Repo URL | First positional value | *(required — ask if missing)* | The GitHub repository to analyze |
| `--runbooks` | `--runbooks deploy,troubleshoot` | All 7 runbooks | Comma-separated list of runbooks to generate: `deploy`, `rollback`, `scale`, `troubleshoot`, `secrets`, `monitor`, `disaster` |
| `--output` | `--output ./runbooks` | Current working directory | Directory where runbook markdown files are written |
| `--path` | `--path services/api` | Repo root | Subdirectory within the repo to treat as the analysis root; use for monorepos |
| `--force` | flag, no value | Off | Overwrite existing output files without prompting |
| `--dry-run` | flag, no value | Off | Run discovery only; print the planned runbooks without generating files |

### Examples

```text
/runbook-generate https://github.com/org/repo
/runbook-generate https://github.com/org/repo --runbooks deploy,rollback
/runbook-generate https://github.com/org/repo --output ./docs/operations
/runbook-generate https://github.com/org/monorepo --path services/api
/runbook-generate https://github.com/org/repo --dry-run
```

**`--runbooks` validation:** If provided, verify that every runbook name is valid. Valid values are: `deploy`, `rollback`, `scale`, `troubleshoot`, `secrets`, `monitor`, `disaster`. If any value is invalid, stop immediately:
> `Error: Invalid runbook names in --runbooks: [names]. Valid values are: deploy, rollback, scale, troubleshoot, secrets, monitor, disaster.`

**Important prerequisite:** Not all runbooks will have complete information for every repository. Use the N/A rule (see Grounding Rules below) for any procedure where insufficient evidence exists.

## Repo Access Strategy

**Step 1 — Extract the repo URL from `$ARGUMENTS`:**
Parse `$ARGUMENTS` to isolate the repo URL (the first positional value, not prefixed with `--`). Store it as `REPO_URL`. Example:
- `$ARGUMENTS` = `https://github.com/org/repo --runbooks deploy,scale --output ./out`
- `REPO_URL` = `https://github.com/org/repo`
- Also derive `REPO_OWNER` and `REPO_NAME` by splitting the URL path.

**Step 2 — Determine access method:**

First, run `gh auth status` to determine authentication state:
- **Unauthenticated:** Prefer cloning to avoid API rate limits. Only use the API if cloning fails.
- **Authenticated:** Use GitHub API for public repos. If any `gh api` call returns HTTP 403 or 429, retry up to 3 times with exponential backoff (5s, 10s, 20s). If all retries fail, fall back to cloning.

- **Public repo** (authenticated user): use `gh api repos/REPO_OWNER/REPO_NAME/contents/{path}` and `gh api repos/REPO_OWNER/REPO_NAME/git/trees/HEAD?recursive=1`
- **Private repo or unauthenticated**: clone the repo once to a temp directory (e.g. `./runbook-tmp-{unix-timestamp}/`) and record the absolute path as `localClonePath`. All subsequent agents read from that local clone.

After all runbooks complete (or after dry-run), delete the temp clone directory if one was created. Always perform cleanup in a finally-style step, including when discovery or generation fails.

**Step 3 — Resolve the analysis path:**
- If `--path` was provided, set `ANALYSIS_PATH` to that subdirectory. Verify it exists; if not, stop and report an error.
- If `--path` was **not** provided, detect whether the repo is a monorepo using these heuristics:
  - Multiple `package.json`, `pom.xml`, `go.mod`, `build.gradle`, or `pyproject.toml` files at different depths
  - Presence of top-level directories: `packages/`, `apps/`, `services/`, `libs/`, or `modules/`
  - Presence of monorepo config: `lerna.json`, `nx.json`, `turbo.json`, `pnpm-workspace.yaml`, or `WORKSPACE`
- If a monorepo is detected and `--path` was not provided: list the discovered services and **stop**. Ask: *"This appears to be a monorepo. Which service should be analyzed? Re-run with `--path <service-path>`, or type the path to continue."*
- If not a monorepo, set `ANALYSIS_PATH` to the repo root.

---

## Dry-run Mode

If `--dry-run` was passed:

1. Parse all arguments as normal (Step 1 of Repo Access Strategy).
2. Run discovery phase only — verify repo access, collect metadata, detect deployment tools.
3. Print the following plan:

```text
Dry-run: runbook-generate
─────────────────────────────────────────────────────
Repository: https://github.com/org/repo (public)
Analysis path: services/api
## Output dir: ./runbooks

Runbooks to generate (7 of 7):
1. Deployment Procedure
2. Rollback Procedure
3. Scaling Operations
4. Troubleshooting Guide
5. Secrets Rotation
6. Monitoring & Alerting
7. Disaster Recovery

Detected deployment tools:
- Kubernetes (Helm charts found in charts/)
- Docker (Dockerfile found)
- GitHub Actions (CI/CD in .github/workflows/)
- PostgreSQL database (detected in docker-compose.yml)

Files that would be written:
runbooks/
00-index.md
01-deployment.md
02-rollback.md
03-scaling.md
04-troubleshooting.md
05-secrets-rotation.md
06-monitoring.md
07-disaster-recovery.md
─────────────────────────────────────────────────────
Re-run without --dry-run to generate the runbooks.
```


If `--runbooks` was provided, list only the requested runbooks. If output files already exist and `--force` was not passed, mark them with `⚠ already exists`.

4. **Stop.** Do not generate any runbooks or write any files.

---

## Pre-generation setup

Before generating runbooks:

### Step 1 — Overwrite check

Resolve every path that will be written. If any already exist and `--force` was **not** passed:
- List every conflicting path
- Stop with: *"Output files already exist. Re-run with `--force` to overwrite, or choose a different `--output` path."*

If `--force` was passed, proceed without prompting.

### Step 2 — Create output directory

Create `{output-dir}/runbooks/` if it doesn't already exist.

---

## Discovery Phase

Before generating any runbooks, run one discovery agent to collect operational metadata. It must return a JSON object with the following schema:

```json
{
  "repo": {
 "name": "string — owner/repo",
 "description": "string | null",
 "defaultBranch": "string",
 "isPrivate": "boolean",
 "localClonePath": "string | null"
  },
  "deployment": {
 "tools": ["string — Kubernetes | Docker | Helm | Terraform | CloudFormation | Ansible | etc."],
 "cicd": ["string — GitHub Actions | GitLab CI | Jenkins | CircleCI | etc."],
 "configFiles": [
   { "path": "string", "type": "string — Dockerfile | docker-compose | Helm values | K8s manifest | etc." }
 ],
 "environments": ["string — dev | staging | production | etc."]
  },
  "infrastructure": {
 "databases": [
   { "type": "string — PostgreSQL | MySQL | MongoDB | Redis | etc.", "evidence": "string — file path" }
 ],
 "messageQueues": [
   { "type": "string — RabbitMQ | Kafka | SQS | etc.", "evidence": "string" }
 ],
 "caches": [
   { "type": "string — Redis | Memcached | etc.", "evidence": "string" }
 ],
 "cloudProvider": "string | null — AWS | GCP | Azure | on-premises | null"
  },
  "healthChecks": [
 { "path": "string — file path", "endpoint": "string — /health | /ready | etc.", "type": "string — liveness | readiness | startup" }
  ],
  "environmentVariables": [
 { "name": "string", "required": "boolean", "defaultValue": "string | null", "evidence": "string — file path" }
  ],
  "secrets": [
 { "name": "string", "purpose": "string", "evidence": "string — e.g., .env.example:5" }
  ],
  "ports": [
 { "port": "number", "protocol": "string — HTTP | HTTPS | gRPC | etc.", "evidence": "string" }
  ],
  "dependencies": [
 { "name": "string", "type": "string — external-api | database | message-queue | cache | etc." }
  ],
  "monitoring": {
 "loggingTools": ["string — file paths to logging config"],
 "metricsTools": ["string — Prometheus | Datadog | CloudWatch | etc."],
 "tracingTools": ["string — OpenTelemetry | Jaeger | etc."],
 "alertingConfig": ["string — file paths to alert definitions"]
  },
  "backup": {
 "databaseBackup": ["string — file paths to backup scripts/configs"],
 "dataRetention": ["string — file paths to retention policies"]
  },
  "analysisPath": "string — relative path from repo root"
}

Pass this JSON object to every runbook generation agent. Agents must restrict evidence and citations to `ANALYSIS_PATH` and must not invent values that are absent from the repository.

## Grounding and Evidence Rules
These rules apply to every runbook and every procedure step. All output must be traceable to the actual repository.

## Valid evidence sources
| Evidence Type | Examples |
|---|---|
Deployment configs	Dockerfile, docker-compose.yml, Kubernetes manifests, Helm charts, values.yaml
CI/CD definitions	.github/workflows/, Jenkinsfile, .gitlab-ci.yml, .circleci/config.yml
Infrastructure as Code	Terraform, CloudFormation, Ansible playbooks, Bicep
Application code	Health check endpoints, startup code, graceful shutdown handlers
Configuration files	appsettings.json, application.properties, .env.example, config.yaml
Scripts	Deploy scripts, rollback scripts, backup scripts in repo
Documentation	README.md, docs/, CONTRIBUTING.md, operational guides
Repository metadata	Issues labeled "incident", "outage", "troubleshooting"
## Prohibited behaviours
No inference from conventions — do not assume standard procedures unless explicitly documented in the repo
No general knowledge fill-in — do not use general DevOps knowledge to fill gaps (e.g. "Postgres backups are typically done using pg_dump...")
No hedged speculation — words like typically, usually, probably, should are banned for factual claims about procedures
No fabricated steps — every step in a procedure must be grounded in a file, script, or config
No assumed tools — do not state that a tool is used unless config or docs explicitly reference it
## Citation requirement
Every non-trivial step must include an inline citation:

Config reference: (docker-compose.yml → services.app.deploy)
Script reference: (scripts/deploy.sh:15-20)
Code reference: (src/main.go:45 — graceful shutdown timeout)
Doc reference: (docs/operations.md § Rollback)
Issue reference: (#456 — incident postmortem)
## N/A rule
For any procedure or section where no valid evidence exists:

Write > **N/A** — no supporting evidence found in repository
A runbook may be partially or entirely N/A — that is a valid and honest result
Clearly state what information is missing and where operators should document it
Runbook 1: Deployment Procedure
Generate a step-by-step deployment runbook. Create the following sections:

1.1 Prerequisites
Required tools and versions (e.g., kubectl, helm, docker)
Required access (cloud accounts, registries, VPN)
Environment variables that must be set
Secrets that must be available
1.2 Pre-Deployment Checklist
Health check of current production environment
Backup verification
Dependency availability checks
Communication plan (who to notify)
1.3 Deployment Steps
Numbered steps Extracted from:

CI/CD pipeline definitions (.github/workflows/, Jenkinsfile)
Deployment scripts (scripts/deploy.sh, Makefile targets)
Helm charts (helm upgrade commands)
Container orchestration manifests
Include exact commands with placeholders for environment-specific values.

1.4 Post-Deployment Verification
Health check URLs and expected responses
Smoke tests to run
Metrics to monitor
Log checks
1.5 Deployment Timing
Estimated duration
Recommended deployment windows (if documented)
Maintenance window requirements
1.6 Rollback Decision Criteria
When to abort and rollback (link to Runbook 2)

Runbook 2: Rollback Procedure
Generate a rollback runbook. Create the following sections:

2.1 Rollback Triggers
Specific failure conditions that require rollback
Health check thresholds
Error rate thresholds
Decision tree
2.2 Rollback Steps
Numbered steps Extracted from:

Rollback scripts (scripts/rollback.sh)
CI/CD rollback jobs
Helm rollback commands (helm rollback)
Database migration rollback (e.g., Flyway undo, EF Core migrations)
2.3 Data Consistency
Database rollback procedures
Data migration reversals
Cache invalidation
2.4 Verification After Rollback
Health checks
Smoke tests
Metrics to confirm stability
2.5 Rollback Timing
Estimated duration
RTO (Recovery Time Objective) if documented
Runbook 3: Scaling Operations
Generate a scaling runbook. Create the following sections:

3.1 Horizontal Scaling
How to scale replicas (e.g., kubectl scale, Helm values)
Auto-scaling configuration (HPA settings from manifests)
Manual scaling commands
3.2 Vertical Scaling
Resource limit adjustments (CPU, memory)
Instance type upgrades (if using VMs)
Downtime requirements
3.3 Database Scaling
Read replicas
Connection pool adjustments
Partitioning/sharding strategy (if documented)
3.4 Cache Scaling
Cache cluster expansion
Cache invalidation during scaling
3.5 Scaling Verification
Metrics to monitor post-scaling
Load testing procedures (if scripts exist in repo)
Runbook 4: Troubleshooting Guide
Generate a troubleshooting runbook. Create the following sections:

4.1 Common Issues
Extract from:

Issues and PRs tagged "bug", "incident", "troubleshooting"
Inline code comments with FIXME, HACK, TODO related to errors
Error handling code (try/catch blocks, error messages)
Format as table:

Symptom	Possible Cause	Diagnostic Steps	Resolution
4.2 Health Check Failures
For each health check endpoint found:

What the check validates
Common failure causes
How to diagnose
How to resolve
4.3 Log Analysis
Where logs are stored
Key log patterns to search for
Log levels and their meaning
Example queries (if monitoring tool config exists)
4.4 Performance Issues
Metrics indicating performance degradation
Profiling tools/commands
Database slow query analysis
Cache hit rate checks
4.5 Connectivity Issues
Network connectivity checks
DNS resolution verification
TLS/SSL certificate validation
Firewall/security group verification
4.6 Emergency Contacts
Extract from:

CODEOWNERS file
README maintainers section
Support documentation
Runbook 5: Secrets Rotation
Generate a secrets rotation runbook. Create the following sections:

5.1 Secret Inventory
List all secrets detected:

Database credentials
API keys
TLS certificates
OAuth client secrets
Encryption keys
5.2 Rotation Procedures
For each secret type:

How to generate new secret
Where to update it (secret manager, config files)
Application restart requirements
Zero-downtime rotation strategy (if documented)
5.3 Certificate Renewal
Certificate expiry monitoring
Renewal commands (e.g., certbot, ACME client)
Certificate deployment
Verification after renewal
5.4 Rotation Verification
Tests to confirm new secrets work
Rollback if rotation fails
5.5 Rotation Schedule
Recommended rotation frequency (if documented)
Expiry warnings and lead times
Runbook 6: Monitoring & Alerting
Generate a monitoring runbook. Create the following sections:

6.1 Monitoring Stack
Logging system (Elasticsearch, CloudWatch, etc.)
Metrics system (Prometheus, Datadog, etc.)
Tracing system (Jaeger, Zipkin, etc.)
Alerting system (AlertManager, PagerDuty, etc.)
6.2 Key Metrics
Extract from:

Prometheus alert rules
Application health check code
Monitoring dashboards (if JSON definitions exist in repo)
Format as table:

Metric	Threshold	Severity	Action
6.3 Alert Response
For each alert type found:

What it means
Diagnostic steps
Resolution steps
Escalation path
6.4 Dashboard Access
URLs to monitoring dashboards (if in config)
Required credentials/access
Key visualizations to monitor
6.5 On-Call Procedures
Extract from:

On-call rotation config
Incident response docs
Escalation policies
Runbook 7: Disaster Recovery
Generate a disaster recovery runbook. Create the following sections:

7.1 Disaster Scenarios
Infrastructure failure (cloud region outage)
Data loss or corruption
Security breach
Complete system failure
7.2 RTO and RPO
Recovery Time Objective
Recovery Point Objective
(Extract from SLA docs, incident response docs, or backup configs)
7.3 Backup Procedures
What is backed up (databases, files, configs)
Backup frequency
Backup location and retention
Backup verification steps
7.4 Restore Procedures
Numbered steps Extracted from:

Backup scripts (scripts/restore.sh)
Database restore commands
Infrastructure rebuild scripts (Terraform apply)
7.5 Failover Procedures
Multi-region failover (if configured)
DNS failover
Database failover (primary to replica)
Verification after failover
7.6 Communication Plan
Who to notify (stakeholders, customers)
Communication channels
Status page updates
7.7 Post-Incident Review
Log collection for analysis
Incident report template (if exists)
Lessons learned process
## Output
Skip this entire section if --dry-run was passed.

The expected output layout is:
{output-dir}/runbooks/
  00-index.md
  01-deployment.md
  02-rollback.md
  03-scaling.md
  04-troubleshooting.md
  05-secrets-rotation.md
  06-monitoring.md
  07-disaster-recovery.md

Only write runbook files that were requested. Omit files for skipped runbooks entirely.

## Step 1 — Index file (00-index.md)
The index must contain:

Title: # Operational Runbooks: {repo name}

Table of contents with relative file links:
## Runbooks
- [1. Deployment Procedure](01-deployment.md)
- [2. Rollback Procedure](02-rollback.md)
- [3. Scaling Operations](03-scaling.md)
- [4. Troubleshooting Guide](04-troubleshooting.md)
- [5. Secrets Rotation](05-secrets-rotation.md)
- [6. Monitoring & Alerting](06-monitoring.md)
- [7. Disaster Recovery](07-disaster-recovery.md)

System Overview — Brief summary of what the system does and its key components (from README or discovery context)

Quick Reference — Emergency contacts, key URLs, critical alerts

Runbooks not generated — if --runbooks was used, list omitted runbooks for traceability

Last updated — Timestamp when runbooks were generated, formatted as ISO 8601 with timezone

## Step 2 — Individual runbook files
Each runbook file must:

Begin with # Runbook N: {Title} as its H1
Use ## N.X Section Name for every section (H2)
Include a back-link at the very top: [← Runbook Index](00-index.md)
Use code blocks for commands with syntax highlighting (bash, yaml, or sql)
Include inline citations for every command and procedure step
Use tables for structured information (checklists, metrics, issues)
Include ⚠️ WARNING or ℹ️ NOTE callouts for critical information
## Step 3 — Confirm output
After all files are written, validate that Markdown fences are balanced, tables are valid, and all relative links resolve. Then print a flat confirmation list:
✓ runbooks/00-index.md
✓ runbooks/01-deployment.md
✓ runbooks/02-rollback.md
✓ runbooks/03-scaling.md
✓ runbooks/04-troubleshooting.md
✓ runbooks/05-secrets-rotation.md
✓ runbooks/06-monitoring.md
✓ runbooks/07-disaster-recovery.md

if any runbook was skipped (insufficient evidence), note it:
⚠ runbooks/04-troubleshooting.md — LIMITED: Only 2 of 6 sections had sufficient evidence
