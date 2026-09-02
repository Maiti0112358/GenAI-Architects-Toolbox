## Purpose
The architects-prompts/reverse-engineering provides a comprehensive toolkit for solution architects to perform automated architecture reverse-engineering from a remote or local repository. It contains a structured set of 15 prompts and an assistant-agnostic skill that generates complete architecture description documents grounded in actual codebase evidence.

## Key Features
**15-section architecture analysis framework** covering all architectural concerns from introduction to evolution

**AI assistant skill integration** via `/arch-describe` for automated, parallel execution

**Evidence-based analysis** where every claim must be directly traceable to source code, configuration, or documentation

**Monorepo support** to analyze specific services within large monorepos using --path flag

**Flexible execution** to run all sections or cherry-pick specific ones with --sections

**Dry-run mode** to preview the analysis plan before committing to full execution

**Remote and local repository support** using either a repository URL or a local filesystem path

**Multi-file structured output** producing organized markdown sections and draw.io diagrams

## Use Cases

**For Solution Architects**
  - Onboarding: Quickly understand unfamiliar codebases
  - Documentation: Generate comprehensive architecture docs from code
  - Due Diligence: Assess technical debt and architecture quality
  - Migration Planning: Document current state before modernization

**For Development Teams**
  - Knowledge Transfer: Create architecture documentation for team members
  - Audit Preparation: Generate evidence-based architecture descriptions
  - Technical Debt Analysis: Identify areas needing refactoring
  - Stakeholder Communication: Produce architecture overviews for non-technical audiences

**For Enterprise Architects**
  - Portfolio Management: Analyze multiple repositories consistently
  - Compliance Validation: Check architectural standards adherence
  - Dependency Mapping: Understand cross-system integrations
  - Risk Assessment: Identify security and scalability concerns

## For Best Results
- Start with dry-run: Use --dry-run to verify the skill has access and understands your repo structure
- Monorepos require --path: For multi-service repos, specify which service to analyze
- Iterate with --sections: Run quick passes on specific sections (e.g., --sections 5,12) to validate before full analysis
- Force flag with caution: Use --force only when intentionally overwriting previous analysis
- Review N/A sections: "No evidence found" may indicate:
- Missing documentation (opportunity for improvement)
- Different approach than expected (valid architectural choice)
- Need to adjust --path or include additional repos

## Performance Notes
- Public repos (authenticated): Fast API-based access, ~2-5 minutes for full analysis
- Private repos or unauthenticated: Falls back to cloning, slightly slower initial setup
- Large repos (>10k files): Consider using --sections for iterative analysis
- Parallel execution: The skill runs sections in batches for optimal performance

## License
MIT License with Non-Commercial Clause

Copyright © 2026 Eeran Maiti
📄 See LICENSE for full terms
