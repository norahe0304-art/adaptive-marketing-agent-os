<!--
[INPUT]: Depends on role-package.schema.md, agent-onboarding.contract.md, host-adapter.interface.md, capability-boundary.schema.md, approval-evidence.schema.md, and geb-semantic-delta.md.
[OUTPUT]: Provides a simple install role, attach tenant, run playbook, and detach tenant note for Adaptive Marketing Agent OS agents.
[POS]: protocols optional packaging guardrail; not a fourth business object.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Role Install / Tenant Attach Note

This is not a core layer. It is packaging sugar around the role-first model.

Users do three things:

- install a reusable `role`;
- attach a `tenant`;
- run a role `playbook`.

## Operational Units

```yaml
role_install:
  id: ""
  role_package: ""
  workflow_templates: []
  protocol_refs:
    - role-package.schema.md
    - capability-boundary.schema.md
    - approval-evidence.schema.md
    - omo-execution-governance.md
    - geb-semantic-delta.md
  validation_fixtures: []
  skill_refs: []
  excludes:
    - tenant truth
    - provider account IDs
    - runtime bindings
    - host adapter implementation
    - approval receipts
    - evidence archives
tenant_attachment:
  id: ""
  tenant: ""
  mounts_on: ""
  tenant_overlay: ""
  workflow_bindings: []
  runtime_bindings: []
  host_adapters: []
  approval_surfaces: []
  evidence_roots: []
  learning_routes: []
  excludes:
    - shared protocol changes
    - base role behavior changes
    - global provider secrets
playbook_activation:
  id: ""
  playbook: ""
  workflow_contract: ""
  skills_allowed: []
  mounted_role: ""
  attached_tenant: ""
  default_mode: "propose"
```

## Lifecycle

```text
install_role
  -> attach_tenant
  -> activate_playbook
  -> run
  -> readback
  -> route_geb_delta
  -> detach_tenant_when_needed
```

## Rules

- Role install is harmless: no tenant truth, no provider account, no host adapter implementation, no mutation permission.
- Tenant attach is reversible: detach removes project-private bindings without modifying the base role.
- Provider runtime may be shared, but the tenant attachment decides which tenant and role may use it.
- `apply` is never installed by a role. It can only be enabled by a workflow-scoped `apply_lab`.
- Evidence and approval receipts are audit artifacts. Detach may remove live runtime access, but must not silently delete required audit evidence.
- GEB updates the right target after lifecycle changes: role, tenant attachment, playbook workflow, skill candidate, protocol, or AGENTS.md.

## Why This Stays Simple

The user-facing model has one product unit:

- Role: who the agent is, what skills it can call, what playbooks it can run, and which tenants can attach.

Tenant attachment and playbooks are part of operating the role. Capability, evidence, approval, OMO, and GEB are guardrails, not separate install layers.

## Removal Safety

Before detach or removal, the runtime must produce a readback:

```yaml
removal_readback:
  target: ""
  active_workflows: []
  runtime_bindings_revoked: []
  host_adapters_unprojected: []
  evidence_archives_retained: []
  tenant_memory_retained_or_exported: []
  blocked_reason: ""
```

If active `apply_lab` runs, pending approval receipts, or unresolved evidence handoffs exist, removal must stop and produce `blocked_reason`.
