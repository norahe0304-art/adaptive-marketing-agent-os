# templates/
> L2 | 父级: /agents/AGENTS.md

Scaffold templates for the generation loop. `scripts/scaffold_consumer.py` reads
these, substitutes `__TOKEN__` placeholders from the scenario, and stamps a
green, minimal consumer agent instance pinned to the protocol. Content is then
filled into the `TODO` markers by any runtime; the validator keeps it honest.

成员清单
consumer.agent.md.tmpl: Mounted agent stub — role + tenant attachment + work substrate + entrypoint + playbooks + run-state + proactive GEB readback; passes validate_mounted_agents out of the box.
consumer.role.md.tmpl: Base role stub for a consumer-owned role (--role-mode new) — schema-shaped, tenant-neutral, fill your own domain. Reference roles in protocol/agents/roles/ are optional seeds to fork instead.
consumer.overlay.md.tmpl: Tenant overlay stub — tenant truth boundary, runtime bindings, approval surfaces, memory records, learning route.
consumer.workflow.md.tmpl: Playbook workflow stub — task graph, capability refs, apply_lab gate, evidence packet, proactive learning verdict, readback, semantic delta.
consumer.workflows.AGENTS.md.tmpl: Consumer workflows L2 map stub; lists the generated playbook workflow and its ownership boundary.
consumer.entrypoint.md.tmpl: Runtime-neutral doorway stub; requires loading the mounted contract and state ledger before execution.
consumer.state.AGENTS.md.tmpl: Consumer run-state L2 map stub; documents structured readbacks, proactive reusable-learning verdicts, verified deltas, and memory pointers.
consumer.state.runs.AGENTS.md.tmpl: Run readbacks L2 map stub; documents per-run evidence/readback YAML records.
consumer.state.deltas.AGENTS.md.tmpl: Verified GEB deltas L2 map stub; documents promoted learning delta records.
consumer.state.memory.AGENTS.md.tmpl: Tenant memory L2 map stub; documents reviewed memory pointers and tenant-memory.md.
consumer.tenant-memory.md.tmpl: Initial tenant memory ledger stub under agents/state/memory/.
consumer.AGENTS.md.tmpl: Consumer instance L2 module map stub (agents/AGENTS.md); declares 父级 /AGENTS.md and proactive GEB readback surfaces.
consumer.root.AGENTS.md.tmpl: Consumer repo L1 constitution stub (root AGENTS.md); seeded write-if-absent to close the agents/ 父级 link and state-ledger verdict map — never clobbers a consumer's own root.
consumer.protocol.AGENTS.md.tmpl: Vendored protocol wrapper L2 map stub for consumer repos.
consumer.protocol.agents.AGENTS.md.tmpl: Vendored protocol agents/ L2 map stub; points at protocols/ and roles/.
consumer.protocol.scripts.AGENTS.md.tmpl: Vendored protocol scripts/ L2 map stub; lists validators and dry-run tools.

占位符
__NAME__ / __NAME_TITLE__ / __DOMAIN__ / __DOMAIN_TITLE__ / __TENANT__ / __ROLE_ID__ / __ROLE_PATH__ / __ROLE_TITLE__ / __ROLE_SOURCE_DESC__ / __PLAYBOOK__ / __PLAYBOOK_TITLE__ / __LOCAL_ROLE_MEMBER__

边界
templates/ holds inert stubs only. They reference the protocol at protocol/agents/...
and the instance locally; they bind no runtime, store no tenant truth, and grant
no live mutation permission.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
