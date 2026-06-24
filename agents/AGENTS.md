# agents/
> L2 | 父级: /AGENTS.md

成员清单
protocols/: Internal guardrails for schema, safety, execution, learning, packaging, onboarding, and validation.
examples/: Schema fixtures proving role package composition without granting runtime access.
mounted/: Assembled agent definitions that bind a base role, tenant attachment, playbooks, work substrate, and entrypoints. Runtime-neutral; which agent runtime runs it is the user's choice.
roles/: Tenant-neutral base roles for marketing domains.
overlays/: Tenant attachments holding stable operating contracts, source pointers, and runtime bindings. Real tenants live in consumer repos; only neutral/domain-proof overlays stay here.
workflows/: Internal workflow contracts behind role playbooks, with capability refs, evidence gates, approval gates, and readback. Real tenants live in consumer repos.
templates/: Scaffold templates the generation loop stamps into a consumer instance (overlay, mounted agent, workflow, entrypoint, AGENTS.md).

边界
agents/ owns design artifacts only. It may describe mounted agents and apply-lab contracts, but it must not install runtime packages, write MCP provider configs, or execute marketing platform mutations.

依赖
mounted/ -> compose role + tenant attachment + playbook workflows into a runnable agent contract.
templates/ -> consumed by scripts/scaffold_consumer.py to grow a consumer instance pinned to the protocol.
roles/ -> define the reusable product unit: identity, abstract surfaces, memory, approval, learning.
overlays/ -> attach tenant facts and runtime bindings onto a role.
workflows/ -> define machine-readable execution contracts behind role playbooks.
protocols/ -> validate role + tenant attachment + playbook; not a separate product layer.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
