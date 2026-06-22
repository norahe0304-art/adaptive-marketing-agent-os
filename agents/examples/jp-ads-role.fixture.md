<!--
[INPUT]: Depends on agents/protocols/role-package.schema.md and .omo/plans/ads-agent-role-design.md.
[OUTPUT]: Provides JP Ads fixture for shared role schema validation.
[POS]: examples seed proof that Ads + Jetpartner can be expressed without changing shared protocol.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# JP Ads Role Fixture

```yaml
role_package:
  identity:
    id: ads-adaptive-operator
    name: Ads Adaptive Operator
    version: 0.1.0
    domain: Ads
    layer: base_role
  tenant_overlay: jetpartners-ads-operator
  purpose:
    - Prove Ads role schema conformance with JP overlay composition.
  when_to_use:
    - JP Ads read-only review fixture validation
  inputs:
    brief:
      required: true
    tenant_overlay:
      required: true
  outputs:
    - approval_packet
    - evidence_readback
    - post_run_delta
  role_instructions:
    operating_principles:
      - Keep tenant truth in overlay.
      - Stop at propose in v1.
  skills:
    recommended:
      - ads
      - ads-audit
    optional:
      - ads-google
  playbooks:
    available:
      - id: daily-maintenance
        name: Daily Maintenance
        workflow_contract: agents/workflows/jetpartners-ads-daily-maintenance.workflow.md
        description: JP Ads daily evidence queue, decisions, apply-lab gate, publish/readback, and learning route.
        skills_called:
          - ads-monitor
          - ads-health
          - ads-keywords
          - ads-audit
        approval_gate: required_for_apply_lab
        tenant_overlay_required: true
      - id: account-review
        name: Account Review
        workflow_contract: agents/workflows/jetpartners-ads-readonly-review.workflow.md
        description: JP Ads read-only review with proposal-first approval packet.
        skills_called:
          - ads
          - ads-audit
          - ads-google
        approval_gate: required_for_apply_lab
        tenant_overlay_required: true
  memory_scope:
    base_role_memory:
      allowed:
        - reusable Ads review pattern
      forbidden:
        - tenant private account data
  runtime_requirements:
    binding_owner: tenant_overlay_or_workflow
    abstract_surfaces:
      - paid_media_platform
      - analytics_source
      - landing_page_source
    concrete_bindings_forbidden:
      - provider account IDs
      - MCP server config
      - plugin install state
      - host adapter implementation
      - project secrets
  capability_manifest:
    boundary_schema: agents/protocols/capability-boundary.schema.md
    default_profile: paid_media_apply_lab_candidate
    apply_lab_owner: workflow
    surfaces:
      paid_media_platform:
        profile: paid_media_apply_lab_candidate
      analytics_source:
        profile: read_observe
      landing_page_source:
        profile: read_observe_propose
  approval_policy:
    default_state: not_requested
    future_live_action_state: blocked_by_runtime_review
    receipt_schema: agents/protocols/approval-evidence.schema.md#ApprovalReceipt
  evidence_contract:
    artifact_schema: agents/protocols/approval-evidence.schema.md#EvidenceArtifact
    required:
      - ads report
      - search-term evidence
      - lead quality evidence
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
      - triggered
      - evidence_collected
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
