<!--
[INPUT]: Depends on a consumer repo mounted agent and protocol/agents/protocols/run-state-ledger.protocol.md.
[OUTPUT]: Provides thin Codex boot guidance for runtime-neutral mounted agents.
[POS]: adapters Codex execution surface note; not a protocol layer and not durable memory.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Codex Adapter Note

Use Codex as an execution surface for a mounted agent.

Boot order:

1. Read `agents/<name>.agent.md`.
2. Follow `product_contract.role`, `tenant_attachment`, and selected playbook workflow.
3. Read `agents/state/AGENTS.md` when present.
4. Execute in `propose` by default.
5. End with final readback and a GEB route.

Codex may edit the consumer repo only through verified semantic or structural
deltas. It must not store raw transcripts, credentials, OAuth tokens, or raw
exports in the run-state ledger.
