<!--
[INPUT]: Depends on role-package.schema.md host_adapters and capability-boundary.schema.md capability restrictions.
[OUTPUT]: Provides host adapter interface for slack, cli, portal, cron, api, and codex hosts.
[POS]: protocols invocation boundary between external environments and domain roles.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Host Adapter Interface

Host adapters define how an external environment invokes a role. They do not define the role itself.

## Host Kinds

- `slack`
- `cli`
- `portal`
- `cron`
- `api`
- `codex`

Concrete host adapter implementations are tenant overlay choices. They are not Agent OS core protocol concepts.

## Interface Sections

```yaml
host_adapter:
  kind: ""
  implementation: ""
  entrypoints: []
  identity_mapping:
    external_user: ""
    role_actor: ""
  session_thread_model:
    session_id: ""
    thread_id: ""
    retention: ""
  approval_surface:
    supports_receipts: true
    approver_identity_required: true
  message_action_payload:
    input_schema: {}
    action_schema: {}
  evidence_handoff:
    artifacts: []
    readback_target: ""
  capability_restrictions:
    max_mode: "propose"
    blocked_capabilities: ["future_live_action"]
  failure_behavior:
    on_missing_identity: "stop"
    on_missing_approval: "stop"
    on_tool_error: "readback_failure"
```

## Host Neutrality Rule

Base roles should stay host-neutral unless the domain itself requires a host. Tenant overlays may require a host for a specific customer operating model.

Example: a base role can stay host-neutral while a tenant overlay requires a collaboration host and names its preferred adapter.
