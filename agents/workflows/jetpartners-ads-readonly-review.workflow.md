<!--
[INPUT]: Depends on ads-adaptive-operator.role.md, jetpartners-ads-operator.overlay.md, OMO governance, and GEB delta protocol.
[OUTPUT]: Provides JP Ads review workflow with proposal, evidence, approval-gated apply lab, and learning routes.
[POS]: workflows first Ads implementation path; consumes shared protocol and JP overlay.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Jetpartner Ads Read-Only Review Workflow

This workflow runs the Ads base role through the Jetpartner overlay. It is proposal-first by default, with a V1 apply lab for explicitly approved, low-risk reversible operations.

```yaml
workflow_contract:
  id: jetpartners-ads-readonly-review
  role: ads-adaptive-operator
  overlay: jetpartners-ads-operator
  default_mode: propose
  workflow_kind: ads_review_proposal

  apply_lab:
    enabled: true
    runtime_binding_id: jp-ads-apply-lab-v1
    max_risk_class_v1: reversible_low
    allowed_operations:
      - add negative keyword
      - add account or campaign label
      - create platform draft or experiment draft
    forbidden_operations:
      - budget change
      - bidding change
      - live ad copy change
      - audience targeting change
      - conversion tracking change
    required_gates:
      - runtime_security_review_id
      - active ApprovalReceipt
      - exact account/campaign/ad group scope
      - pre_apply EvidenceArtifact
      - rollback plan
      - post_apply readback EvidenceArtifact

  trigger:
    accepted_inputs:
      - review latest account performance
      - explain lead quality mismatch
      - propose campaign optimization
      - prepare approval packet
    required_scope:
      - platform
      - time window
      - account or campaign scope
      - requested decision

  self_check:
    must_confirm:
      - tenant overlay loaded
      - no apply_lab mutation requested without runtime security review, active approval, exact scope, and rollback
      - dashboard or export source available
      - CRM quality source available when lead quality is discussed
      - landing page source available when relevance is discussed

  task_graph:
    - step: collect_evidence
      mode: read
      outputs:
        - platform metrics
        - dashboard reference
        - CRM lead quality reference
        - landing page reference
    - step: classify_account_state
      mode: observe
      outputs:
        - trend summary
        - anomaly list
        - lead quality mismatch diagnosis
        - risk class
    - step: draft_proposal
      mode: propose
      outputs:
        - proposed changes
        - expected impact
        - evidence links
        - risk notes
    - step: approval_gate
      mode: propose
      outputs:
        - approval packet
        - named approver request
        - rollback or irreversible-action note
    - step: apply_lab_execute_approved_change
      mode: apply
      apply_lab: true
      runs_only_when:
        - approved_for_apply_lab
        - runtime binding available
        - requested operation is in apply_lab.allowed_operations
      outputs:
        - apply_run EvidenceArtifact
        - platform readback
        - rollback reference
    - step: readback
      mode: observe
      outputs:
        - final decision summary
        - evidence table
        - unresolved blockers
        - post_run_delta

  future_live_action_policy:
    default_state: apply_lab_requires_approval
    allowed_only_after:
      - runtime_security_review_id
      - approval receipt
      - exact account/campaign/ad group scope
      - pre-change evidence
      - rollback or irreversible-action note
      - final readback target
      - apply_run evidence when apply_lab executes

  evidence_packet:
    required:
      - reports.30x.company/jetpartners/latest or export path
      - platform account/campaign/ad group scope
      - time window
      - Supabase qualified lead source reference when used
      - landing page URL when used
      - proposal artifact path
      - approval receipt if future live action is requested
      - apply_run artifact if apply_lab executes

  failure_behavior:
    missing_dashboard: stop_and_request_source
    missing_crm_quality_for_lead_claim: remove_claim_or_request_source
    unclear_tenant_fact: keep_as_question
    approval_missing_for_apply_lab: stop_at_proposal
    operation_outside_apply_lab: stop_at_proposal

  readback:
    include:
      - what was reviewed
      - evidence used
      - recommendation
      - approval status
      - what was not changed
      - learning route

  semantic_delta:
    route_options:
      - tenant_memory_patch
      - ads_playbook_patch
      - workflow_patch
      - skill_patch
      - new_skill_candidate
      - protocol_update
    default_route: tenant_memory_patch
    promotion_requires:
      - repeated evidence
      - owner
      - review_after
      - contradiction check
```

## Workflow Rule

This workflow can recommend Ads actions and may run approved apply-lab mutations. The default failure mode is still a better approval packet, not a hidden live change.
