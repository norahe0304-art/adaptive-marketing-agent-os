# Agency Agents - Adaptive Marketing Agent OS

Adaptive Marketing Agent OS foundation: install one role, attach one tenant, run mounted agent playbooks. Protocol files are guardrails, not user-facing layers.

<directory>
agents/ - Product-owned agent surface (mounted agents, roles, tenant attachments, role playbooks, internal guardrails)
</directory>

<directory>
.omo/ - Planning, review, and evidence artifacts for OMO-governed work
</directory>

<directory>
scripts/ - Contract validators and git pre-commit hook (executes role package and mounted agent checks)
</directory>

<config>
README.md - Human entrypoint for v0.1.0 repo purpose, structure, and validation commands
</config>

<config>
DESIGN.md - Visual design system for strategy and review HTML packets
</config>

<architecture>
Role is the reusable product unit. A tenant attachment binds that role to one customer and its real systems. A mounted agent is the assembled runtime contract. Playbooks are the role's callable business tasks; each playbook is backed by an internal workflow contract and may call reusable skills. Capability, approval, evidence, OMO, install, and GEB are internal guardrails.
</architecture>

<rules>
- Shared protocol and base roles must not contain tenant truth.
- Domain roles must not bind tenant tools, provider accounts, host adapters, or customer truth.
- Mounted agents compose one base role, one tenant attachment, named playbooks, and runtime source pointers.
- Skill is an atomic reusable action; playbook is a business task route; workflow is the machine-readable execution contract behind a playbook.
- V1 `apply` exists only as workflow-scoped `apply_lab`: default mode remains `propose`; mutation requires runtime binding, typed approval, evidence, exact scope, and readback.
- GEB runs after work: route learning to role, tenant attachment, playbook, skill candidate, protocol, or L1/L2/L3 docs.
</rules>

法则: 极简·稳定·导航·版本精确

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
