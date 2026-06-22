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
  memory_scope:
    base_role_memory:
      allowed:
        - reusable Ads review pattern
      forbidden:
        - tenant private account data
  tools:
    platform_surfaces:
      - google-ads
    supporting_surfaces:
      - analytics
      - landing-page-review
  plugins:
    required: []
    optional:
      - omo
  capability_surface:
    default_mode: propose
    max_mode_v1: propose
    surfaces:
      google-ads:
        modes: [read, observe, dry_run, propose]
      analytics:
        modes: [read, observe]
      landing-page-review:
        modes: [read, observe, propose]
  host_adapters:
    required: []
    optional:
      - codex
      - portal
      - slack
    preferred: {}
    unsupported: []
    notes: "JP Ads can use Codex, portal, or Slack without changing the base role."
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
