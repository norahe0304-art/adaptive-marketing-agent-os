# Agency Agents - Adaptive Marketing Agent OS

Adaptive Marketing Agent OS foundation: shared protocol, tenant-neutral base roles, tenant overlays, workflow contracts, and validation fixtures.

<directory>
agents/ - Product-owned agent protocol surface (5 modules: protocols, examples, roles, overlays, workflows)
</directory>

<directory>
.omo/ - Planning, review, and evidence artifacts for OMO-governed work
</directory>

<directory>
scripts/ - Contract validator and git pre-commit hook (executes role-package.schema.md)
</directory>

<config>
DESIGN.md - Visual design system for strategy and review HTML packets
</config>

<architecture>
Shared protocol defines the operating contract. Domain agents consume it. Tenant overlays hold tenant operating truth and source pointers. Workflows hold typed execution loops. GEB keeps L1/L2/L3 docs aligned with the actual artifact graph.
</architecture>

<rules>
- Shared protocol and base roles must not contain tenant truth.
- Domain roles must not redefine shared protocol fields, permission modes, approval states, host kinds, or evidence semantics.
- V1 `apply` exists only as workflow-scoped `apply_lab`: default mode remains `propose`; mutation requires runtime binding, typed approval, evidence, exact scope, and readback.
- GEB is semantic and structural delta: learning placement plus L1/L2/L3 documentation isomorphism.
</rules>

法则: 极简·稳定·导航·版本精确

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
