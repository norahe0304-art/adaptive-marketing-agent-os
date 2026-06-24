# adapters/
> L2 | 父级: /agents/AGENTS.md

Thin runtime adapter notes for opening a mounted agent from different execution
surfaces. Adapters are boot guidance only; they do not own agent state, install
provider credentials, or change protocol semantics.

成员清单
codex.md: Codex runtime boot note; load mounted agent, overlay, workflow, run-state ledger, then execute by playbook gates.
claude-code.md: Claude Code boot note; same contract, different execution surface.
browser-automation.md: Browser automation boot note; use only approved read/observe/dry_run/propose surfaces unless apply_lab gates are active.
local-runtime.md: Local runtime boot note; CLI or service wrappers read the same mounted contract and write structured readbacks.
mcp-backed.md: MCP-backed execution note; MCP bindings attach at runtime/overlay layer and never become base role state; a missing binding blocks apply AND proposes the binding to wire (generative half), never degrading to manual.

边界
Runtime adapters are replaceable. The durable agent remains the consumer repo:
mounted agent, overlay, workflow, run-state ledger, and pinned protocol.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
