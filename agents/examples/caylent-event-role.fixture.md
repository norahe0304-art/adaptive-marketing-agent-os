<!--
[INPUT]: Depends on agents/protocols/role-package.schema.md and .omo/plans/event-agent-role-design.md.
[OUTPUT]: Provides Caylent Event fixture for shared role schema validation.
[POS]: examples seed proof that Event + Caylent can be expressed without changing shared protocol.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Caylent Event Role Fixture

```yaml
role_package:
  identity:
    id: event-adaptive-operator
    name: Event Adaptive Operator
    version: 0.1.0
    domain: Event
    layer: base_role
  tenant_overlay: caylent-event-operator
  purpose:
    - Prove Event role schema conformance with Caylent overlay composition.
  when_to_use:
    - Caylent Event launch fixture validation
  inputs:
    brief:
      required: true
    tenant_overlay:
      required: true
  outputs:
    - approval_packet
    - launch_readback
    - post_run_delta
  role_instructions:
    operating_principles:
      - Keep host adapter choice in overlay.
      - Stop at propose in v1.
  skills:
    recommended:
      - hubspot:hubspot
    optional:
      - documents:documents
  memory_scope:
    base_role_memory:
      allowed:
        - reusable Event launch pattern
      forbidden:
        - tenant CRM object IDs
  tools:
    platform_surfaces:
      - hubspot.pages
      - hubspot.emails
      - hubspot.workflows
      - hubspot.lists
      - salesforce.read
    supporting_surfaces:
      - documents
  plugins:
    required: []
    optional:
      - hubspot
      - omo
  capability_surface:
    default_mode: propose
    max_mode_v1: propose
    surfaces:
      hubspot.pages:
        modes: [read, observe, dry_run, propose]
      hubspot.emails:
        modes: [read, observe, dry_run, propose]
      hubspot.workflows:
        modes: [read, observe, dry_run, propose]
      hubspot.lists:
        modes: [read, observe, dry_run, propose]
      salesforce.read:
        modes: [read, observe]
  host_adapters:
    required: []
    optional:
      - portal
      - codex
      - slack
    preferred: {}
    unsupported: []
    notes: "Caylent can require Slack in overlay without binding the base Event role."
  permissions:
    default_mode: propose
    max_mode_v1: propose
    live_mutation: runtime_security_review_required
  mcp_boundary:
    read: {}
    observe: {}
    dry_run: {}
    propose: {}
    future_live_action:
      reserved_until:
        - runtime_security_review_id
        - ApprovalReceipt
  approval_policy:
    default_state: not_requested
    future_live_action_state: blocked_by_runtime_review
    receipt_schema: agents/protocols/approval-evidence.schema.md#ApprovalReceipt
  evidence_contract:
    artifact_schema: agents/protocols/approval-evidence.schema.md#EvidenceArtifact
    required:
      - event brief
      - campaign id
      - asset urls
      - approval receipt when future live action is requested
      - post_run_delta
  learning_rules:
    routes:
      memory: tenant_memory_patch
      playbook: industry_playbook_patch
      workflow: workflow_patch
    promotion_requires:
      - repeated evidence
      - owner
      - review_after
      - contradiction check
  lifecycle:
    states:
      - brief_received
      - context_collected
      - approval_ready
      - readback_complete
      - post_run_delta_routed
  success_criteria:
    - Fixture validates shared role_package fields.
  non_goals:
    - runtime mutation
  versioning:
    owner: shared-architecture
    review_gate: Metis/Momus
    status: draft
    change_log: []
```
