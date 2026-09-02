# GenAI-Architects-Toolbox
The repository provides a comprehensive toolkit including prompts and Claude/Codex/GHCP skills for solution architects useful for regular tasks.

1. Create extensive and comprehensive Architectural Documentation from a code repo
2. Generate advisory compliance report for your application for specific regulations (GDPR/ISO etc)
3. Produce threat model as per STRIDE guidelines for your services
4. Generate onboarding guides fot your developers for an easy start
5. Produce runbook for your applications

## Available skills

Use the skill name with a repository URL or local repository path. Assistant-specific invocation syntax may vary; for example: `/skill-name <repository> [options]`.

| Skill | Purpose | How to use |
|---|---|---|
| `arch-describe` | Produces a comprehensive, structured architecture description from repository evidence. | Invoke with a remote URL or local path, for example `/arch-describe C:\Repos\my-repo`. |
| `compliance-check` | Assesses GDPR, SOC 2, ISO 27001, or PCI-DSS readiness and produces framework-specific reports plus an evidence matrix. | Specify one or more frameworks, for example `/compliance-check ./repo --framework GDPR,SOC2`. |
| `onboarding-guide` | Creates an evidence-grounded developer guide covering prerequisites, setup, architecture, code organization, testing, debugging, and contribution. | Invoke for the whole repository or a monorepo application, for example `/onboarding-guide ./repo --app apps/web`. |
| `runbook-generate` | Generates operational runbooks for deployment, troubleshooting, scaling, and incident response. | Invoke with a remote URL or local path, for example `/runbook-generate C:\Repos\my-repo`. |
| `threat-model` | Produces an evidence-grounded STRIDE model with data-flow diagrams, trust boundaries, attack trees, a prioritized risk register, draw.io diagrams, and Markdown. | Invoke with a repository or system description, for example `/threat-model ./repo`. |

## Corresponding prompts

These prompt documents are assistant-agnostic templates for running the same
workflows manually or adapting them to another AI assistant. Each prompt points
to the related skill and defines the expected inputs, analysis boundaries, and
deliverables.

| Prompt | Corresponding skill | Use it for |
|---|---|---|
| [`architecture-description.md`](reverse-engineering/architecture-description.md) | `arch-describe` | Generating a detailed architecture description from a repository. |
| [`compliance-checker.md`](artifacts-generation/compliance-checker.md) | `compliance-check` | Producing framework-specific compliance assessments and an evidence matrix. |
| [`onboarding-guide-generation.md`](artifacts-generation/onboarding-guide-generation.md) | `onboarding-guide` | Creating a new-developer onboarding guide, including an independently scoped monorepo application. |
| [`runbook-generation.md`](artifacts-generation/runbook-generation.md) | `runbook-generate` | Generating operational runbooks from repository evidence. |
| [`threat-model-stride.md`](security/threat-model-stride.md) | `threat-model` | Creating a STRIDE threat model with Markdown and draw.io deliverables. |

### Prompt usage

1. Open the prompt document corresponding to the desired workflow.
2. Provide the repository URL or local path and any required scope, such as a framework or monorepo application.
3. Paste the prompt into the AI assistant, or adapt its instructions to the assistant’s skill or command format.
4. Review the generated evidence, assumptions, and output files before using the deliverables.

## Shared skills

### Setup

1. Install Python 3 and either clone a remote repository or identify an existing local repository.
2. From the repository root, create the assistant adapters:
   - Windows PowerShell: `.\scripts\link-skills.ps1`
   - macOS/Linux: `sh ./scripts/link-skills.sh`
3. Verify the adapters: `python scripts/link-skills.py --check`.
4. Use the skills through `.claude/skills`, `.codex/skills`, or `.github/skills`.
5. Edit only the canonical files under `skills/<skill-name>/`; rerun the validator after changes.

The canonical skill sources live under [`skills/`](skills/). The assistant-specific
directories are links to those sources, so a skill is maintained once:

- `.claude/skills/` — Claude-compatible discovery location.
- `.codex/skills/` — Codex-compatible discovery location.
- `.github/skills/` — repository adapter location for assistants and integrations
  that use GitHub conventions; verify the consuming tool's exact discovery rules.

Run `scripts/link-skills.py --check` (or `scripts/link-skills.ps1 -Check` on
Windows) to validate the links. To recreate them, run the same command without
the check option. macOS and Linux use symbolic links. Windows first tries
symbolic links and falls back to directory junctions, which normally work
without Administrator privileges.

The bootstrap requires Python 3 and uses relative links where possible. Git
must preserve symlinks when cloning on Unix-like systems. On Windows, enable
Developer Mode or use the junction fallback. Do not edit files through an
adapter path; edit the corresponding file under `skills/` instead.


MIT License with Non-Commercial Clause

Copyright © 2026 Eeran Maiti 📄 See [LICENSE](https://github.com/Maiti0112358/GenAI-Architects-Toolbox/blob/main/LICENSE) for full terms.
