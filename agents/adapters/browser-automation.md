<!--
[INPUT]: Depends on workflow capability_refs and approval-evidence.schema.md.
[OUTPUT]: Provides thin browser automation boot guidance for runtime-neutral mounted agents.
[POS]: adapters browser execution surface note; keeps browser actions behind workflow gates.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Browser Automation Adapter Note

Use browser automation only through a workflow step whose capability profile
allows the requested mode.

Rules:

- `read`, `observe`, `dry_run`, and `propose` may collect evidence or prepare drafts.
- `apply` requires workflow-scoped apply_lab, active ApprovalReceipt, exact scope, and post-apply readback.
- Browser session artifacts may be referenced by path; raw cookies, tokens, and unbounded logs must not be stored in the repo.

The browser is a tool surface, not the agent state.
