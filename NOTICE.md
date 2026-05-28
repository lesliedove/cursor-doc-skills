# NOTICE

This repository contains internal Synopsys / Ansys tooling. The skill
patterns, the helper scripts, and the conventions documented here are
internal-use only and reference internal infrastructure (Azure DevOps
on-prem TFS, NTLM with the ANSYS\ domain, internal SharePoint paths,
internal product release pipelines).

Do not redistribute the contents of this repository — including the
zips in `dist/` and the package sources under `packages/` — outside
Synopsys without explicit approval from Leslie Poff (`ldove@synopsys.com`).

The general patterns and approaches (skill structure, hook gating,
credential handling via `Invoke-RestMethod -Credential`, etc.) are fine
to discuss externally — at conferences, in blog posts, in cross-team
demos. The corporate-specific configs, style-guide content, ticket
numbers, repo paths, and infrastructure URLs are not.

When in doubt, ask.
