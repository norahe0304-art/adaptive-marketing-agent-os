<!--
[INPUT]: Depends on role-package.schema.md for role_package fields and host-adapter.interface.md for host-neutral invocation.
[OUTPUT]: Provides shared capability modes, apply-lab gates, surface record fields, and MCP permission boundaries for all domain roles.
[POS]: protocols permission boundary consumed by Ads, Event, and future marketing agents.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Capability / MCP Boundary Schema

This protocol is host-neutral. It describes tool permission modes, not Slack, email, portal, or any one host UX.

## Runtime Split

- `provider-shared runtime`: external provider capability such as Google Ads, HubSpot, Salesforce, browser, docs, CRM, memory.
- `project-private binding`: tenant/project scoped binding that limits account, tenant, object, and approval policy.
- `role-scoped manifest`: the role-specific list of allowed surfaces and modes.

## Modes

| Mode | Meaning | Can change external state |
| --- | --- | --- |
| `read` | Read existing records or docs. | No |
| `observe` | Inspect live state without modifying it. | No |
| `dry_run` | Simulate an operation and produce expected result/risk. | No |
| `propose` | Produce a human-reviewable action plan. | No |
| `apply` | Execute an approved mutation through a workflow-scoped apply lab. | V1 apply lab only |

## Apply Gate

`apply` is not a default role permission. V1 may connect `apply` only inside a workflow-scoped `apply_lab`. Base roles still default to `propose`; a workflow must opt in before any task may use `mode: apply`.

Every V1 apply-lab mutation requires:

- `runtime_security_review_id`
- role-level risk class
- tenant/account binding
- named human approver
- typed approval receipt
- pre-apply evidence
- post-apply readback
- rollback plan or explicit irreversible-action acknowledgement

If any item is missing, execution must stop at `propose`.

## Capability Record

```yaml
capability:
  provider: ""
  binding: ""
  scope: "tenant"
  modes: ["read", "observe", "dry_run", "propose", "apply"]
  default: "propose"
  max_mode_v1: "apply_lab"
  future_live_action_requires_approval: true
  allowed_operations: []
  approval_gate: ""
  evidence_readback: []
  rollback_or_dry_run: ""
```

## Apply Lab Record

```yaml
apply_lab:
  enabled: false
  runtime_binding_id: ""
  max_risk_class_v1: "reversible_low"
  allowed_operations: []
  forbidden_operations: []
  required_gates:
    - runtime_security_review_id
    - active ApprovalReceipt
    - exact tenant/account/object scope
    - pre_apply EvidenceArtifact
    - rollback plan or irreversible-action acknowledgement
    - post_apply readback EvidenceArtifact
```

## Surface Record

Role `capability_surface.surfaces.*` entries may only use these fields:

- `modes`: required list drawn from `read`, `observe`, `dry_run`, and `propose`.
- `default`: optional mode value; when present, it must be included in `modes`.
- `future_live_action_requires_approval`: optional boolean that marks whether the surface could ever need a future live-action gate.

Base role surfaces must not list `apply`. Apply belongs to workflow `apply_lab` records and task steps that explicitly set `apply_lab: true`.

No domain role may add extra capability surface keys without updating this shared protocol first.

## Example Surfaces

- `google-ads`: read, observe, dry_run, propose by default; apply lab may execute only approved low-risk reversible operations.
- `hubspot.pages`: read, dry_run, propose by default; apply lab may create approved draft pages, not publish.
- `hubspot.emails`: read, dry_run, propose by default; apply lab may create approved draft emails, not send.
- `hubspot.workflows`: read, dry_run, propose by default; apply lab may create draft workflow artifacts, not activate.
- `salesforce`: read only.
- `browser`: read, observe.
- `docs`: read, propose.
- `crm`: read, observe, propose.
- `memory`: read, propose patch.

## Forbidden

- No global tool exposure.
- No provider config files in this protocol directory.
- No host-specific behavior such as Slack thread UX or tenant adapter runtime.
