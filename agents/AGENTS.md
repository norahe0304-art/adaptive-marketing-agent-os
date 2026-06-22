# agents/
> L2 | 父级: /AGENTS.md

成员清单
protocols/: Shared Agent OS protocol documents: role schema, capability boundary, host adapters, OMO governance, GEB delta, onboarding, cross-role validation.
examples/: Schema fixtures proving role package composition without granting runtime access.
roles/: Tenant-neutral base roles for marketing domains.
overlays/: Tenant overlays holding stable operating contracts and source pointers.
workflows/: Typed workflow contracts for tenant-scoped execution loops.

边界
agents/ owns product-level role protocol artifacts only. It may describe apply-lab contracts, but it must not install runtime packages, write MCP provider configs, or execute marketing platform mutations.

依赖
protocols/ -> examples/, roles/, overlays/, workflows/ consume protocol rules.
roles/ -> protocols/ for schema and gates.
overlays/ -> roles/ and protocols/ for tenant-scoped deltas.
workflows/ -> roles/, overlays/, protocols/ for execution contracts.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
