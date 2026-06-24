<!--
[INPUT]: Depends on a consumer repo mounted agent and protocol/agents/protocols/run-state-ledger.protocol.md.
[OUTPUT]: Provides thin Claude Code boot guidance for runtime-neutral mounted agents.
[POS]: adapters Claude Code execution surface note; not a protocol layer and not durable memory.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Claude Code Adapter Note

Use Claude Code as an execution surface for a mounted agent.

Boot order:

1. Read `agents/<name>.agent.md`.
2. Load the referenced role, overlay, and selected workflow.
3. Respect approval, evidence, and apply_lab gates.
4. Write only structured readbacks or verified GEB deltas to `agents/state/`.

The runtime may change; the mounted agent contract and run-state ledger remain
the durable source of truth.
