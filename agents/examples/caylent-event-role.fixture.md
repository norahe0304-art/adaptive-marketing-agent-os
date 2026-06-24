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
      - Keep runtime and host choice in overlay.
      - Stop at propose in v1.
  skills:
    recommended:
      - hubspot:hubspot
    optional:
      - documents:documents
  playbooks:
    available:
      - id: event-launch-kit
        name: Event Launch Kit
        workflow_contract: agents/workflows/caylent-event-launch.workflow.md
        description: Caylent event brief to HubSpot draft assets, approval packet, and launch readback.
        skills_called:
          - hubspot:hubspot
          - documents:documents
        approval_gate: required_for_apply_lab
        tenant_overlay_required: true
  memory_scope:
    base_role_memory:
      allowed:
        - reusable Event launch pattern
      forbidden:
        - tenant CRM object IDs
  runtime_requirements:
    binding_owner: tenant_overlay_or_workflow
    abstract_surfaces:
      - event_asset_system
      - crm_context_source
      - document_source
    concrete_bindings_forbidden:
      - provider account IDs
      - MCP server config
      - plugin install state
      - runtime or host binding
      - project secrets
  capability_manifest:
    boundary_schema: agents/protocols/capability-boundary.schema.md
    default_profile: draft_asset_apply_lab_candidate
    apply_lab_owner: workflow
    surfaces:
      event_asset_system:
        profile: draft_asset_apply_lab_candidate
      crm_context_source:
        profile: read_observe
      document_source:
        profile: read_observe_propose
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
