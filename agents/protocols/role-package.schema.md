<!--
[INPUT]: Depends on agent-roles-spec concepts, approval-evidence.schema.md, OMO execution gates, and GEB semantic/structural delta.
[OUTPUT]: Provides the canonical role_package schema and minimum validation for all Adaptive Marketing Agent OS roles.
[POS]: protocols shared schema consumed by roles, overlays, workflows, and examples.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Role Package Schema

Role is a complete operating package, not a prompt and not a single skill.

## Required Object

```yaml
role_package:
  identity:
    id: ""
    name: ""
    version: ""
    domain: ""
    layer: ""
  tenant_overlay: ""
  purpose: ""
  when_to_use: []
  inputs: {}
  outputs: []
  role_instructions: {}
  skills:
    recommended: []
    optional: []
  memory_scope:
    base_role_memory:
      allowed: []
      forbidden: []
  tools:
    platform_surfaces: []
    supporting_surfaces: []
  plugins:
    required: []
    optional: []
  host_adapters:
    required: []
    optional: []
    preferred: {}
    unsupported: []
    notes: ""
  capability_surface:
    default_mode: "propose"
    max_mode_v1: "propose"
    surfaces: {}
  mcp_boundary:
    read: {}
    observe: {}
    dry_run: {}
    propose: {}
    future_live_action:
      reserved_until: []
  permissions:
    default_mode: "propose"
    max_mode_v1: "propose"
    live_mutation: "runtime_security_review_required"
  lifecycle:
    states: []
  evidence_contract:
    artifact_schema: "agents/protocols/approval-evidence.schema.md#EvidenceArtifact"
    required: []
    forbidden: []
  approval_policy:
    default_state: "not_requested"
    future_live_action_state: "blocked_by_runtime_review"
    receipt_schema: "agents/protocols/approval-evidence.schema.md#ApprovalReceipt"
    approval_required_for: []
    approval_packet_requires: []
  success_criteria: []
  non_goals: []
  learning_rules:
    routes: {}
    promotion_requires: []
  versioning:
    owner: ""
    review_gate: ""
    status: "draft"
    change_log: []
```

## Field Rules

- `identity` names the role and its domain.
- `tenant_overlay` is optional and only points to a tenant overlay in fixtures or composed role packages.
- `role_instructions` describes role behavior, not tenant facts.
- `skills` names callable domain skills or candidate skills.
- `memory_scope` separates durable memory from forbidden raw dumps.
- `tools` and `plugins` are declared surfaces, not global access grants.
- `host_adapters` is structured; do not replace it with free-text notes.
- `capability_surface` must reference shared permission modes and declare `max_mode_v1: propose`.
- `evidence_contract` must include source-backed artifacts and readback.
- `approval_policy` must require a typed human receipt for any future live action.
- `learning_rules.routes` must route deltas through GEB, and `learning_rules.promotion_requires` must state promotion gates.
- `versioning` must include owner, review gate, status, and change log.

## Domain Role Constraint

Domain roles may instantiate shared `evidence_contract`, `approval_policy`, `learning_rules`, and `capability_surface`; they must not introduce new protocol fields, permission modes, approval states, host kinds, or evidence semantics. New shared semantics require a protocol update first.

Current role packages may describe live-action gates, but base role `capability_surface` values must stop at `propose`. V1 `mode: apply` is allowed only in workflow `apply_lab` steps with runtime binding, security review, an active `ApprovalReceipt`, and readback evidence.

`mcp_boundary.future_live_action` is a reserved non-executable section for documenting future live-action gates. It is not a permission mode and cannot appear in a workflow task `mode`.

## Minimum Validation

This contract is executed by a single source of truth, not by a copy pasted here.
Run it directly, or let the pre-commit hook run it for you:

```bash
python3 scripts/validate_roles.py
```

The validator (`scripts/validate_roles.py`) enforces, for every
`agents/roles/*.role.md` and `agents/examples/*-role.fixture.md`:

- all required fields present, and no `workflow_contract` inside a `role_package`;
- `permissions.max_mode_v1 == "propose"`;
- `learning_rules.routes` is a map and `learning_rules.promotion_requires` is a list;
- each `capability_surface.surfaces.*` uses only allowed keys, a non-empty
  `modes` subset of `{read, observe, dry_run, propose}`, a `default` within
  `modes`, and a boolean `future_live_action_requires_approval`.

Changing the rules above means changing `scripts/validate_roles.py` and this
section together — the executable and the prose stay isomorphic.
