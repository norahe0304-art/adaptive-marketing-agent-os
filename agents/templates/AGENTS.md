# templates/
> L2 | 父级: /agents/AGENTS.md

Scaffold templates for the generation loop. `scripts/scaffold_consumer.py` reads
these, substitutes `__TOKEN__` placeholders from the scenario, and stamps a
green, minimal consumer agent instance pinned to the protocol. Content is then
filled into the `TODO` markers by any runtime; the validator keeps it honest.

成员清单
consumer.agent.md.tmpl: Mounted agent stub — role + tenant attachment + work substrate + entrypoint + playbooks + GEB; passes validate_mounted_agents out of the box.
consumer.role.md.tmpl: Base role stub for a consumer-owned role (--role-mode new) — schema-shaped, tenant-neutral, fill your own domain. Reference roles in protocol/agents/roles/ are optional seeds to fork instead.
consumer.overlay.md.tmpl: Tenant overlay stub — tenant truth boundary, runtime bindings, approval surfaces, memory records, learning route.
consumer.workflow.md.tmpl: Playbook workflow stub — task graph, capability refs, apply_lab gate, evidence packet, readback, semantic delta.
consumer.entrypoint.md.tmpl: Runtime-neutral doorway stub.
consumer.AGENTS.md.tmpl: Consumer instance module map stub.

占位符
__NAME__ / __NAME_TITLE__ / __DOMAIN__ / __TENANT__ / __ROLE_ID__ / __ROLE_PATH__ / __ROLE_TITLE__ / __PLAYBOOK__ / __PLAYBOOK_TITLE__

边界
templates/ holds inert stubs only. They reference the protocol at protocol/agents/...
and the instance locally; they bind no runtime, store no tenant truth, and grant
no live mutation permission.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
