<!--
[INPUT]: Depends on role-package.schema.md runtime_requirements and capability-boundary.schema.md runtime split.
[OUTPUT]: Provides thin MCP-backed execution guidance for runtime-neutral mounted agents.
[POS]: adapters MCP execution surface note; prevents MCP bindings from becoming base role state.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# MCP-Backed Execution Note

MCP-backed tools are execution bindings. They do not belong in base role state.

Rules:

- Base roles may name abstract surfaces only.
- Tenant overlays or workflow runtime bindings may point those surfaces at MCP-backed providers.
- Secret values stay in environment variables or secret stores; overlays may store only references.
- A missing MCP binding blocks apply and produces a readback; it must not mutate the base role.
- That readback must also propose the binding: name the unbound surface, the MCP
  provider it would wire, and the exact overlay `runtime_bindings` reference to add
  (a reference only, no secret), then request authorization. Blocking is the safe
  floor; proposing the binding is the generative half — never degrade to asking the
  user for screenshots of what the connector would have read.

This keeps MCP useful without making the agent depend on one runtime host.
