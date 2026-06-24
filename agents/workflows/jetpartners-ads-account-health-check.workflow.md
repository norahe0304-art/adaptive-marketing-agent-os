<!--
[INPUT]: Depends on ads-adaptive-operator.role.md, jetpartners-ads-operator.overlay.md, 30x-ads ads-health/ads-monitor behavior, preflight/observe/run-monitor scripts, OMO governance, and GEB delta protocol.
[OUTPUT]: Provides JP Ads account health check playbook workflow for readiness probes, drift scans, client-safe diagnosis, blocked-action handling, readback, and learning routes.
[POS]: workflows JP Ads account health check playbook; internal workflow contract behind the Ads Role's readiness and drift-health task.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Jetpartner Ads Account Health Check Workflow

This workflow is the machine-readable contract behind the Ads Role's `account-health-check` playbook for Jetpartner. It is read-first and diagnose-first; fixes become proposals unless an approved apply-lab operation is explicitly requested.

```yaml
workflow_contract:
  id: jetpartners-ads-account-health-check
  role: ads-adaptive-operator
  overlay: jetpartners-ads-operator
  default_mode: propose
  workflow_kind: ads_account_health_check_playbook

  playbook:
    name: account health check
    product_surface: role_playbook
    internal_workflow_contract: true
    source_surfaces:
      - "30x-ads .claude/skills/ads-health/SKILL.md"
      - "30x-ads .claude/skills/ads-monitor/SKILL.md"
      - "30x-ads scripts/preflight.ts"
      - "30x-ads scripts/observe.ts"
      - "30x-ads scripts/run-monitor.ts"
    calls_skills:
      - ads-health
      - ads-monitor
      - ads-audit

  apply_lab:
    enabled: true
    runtime_binding_id: jp-ads-health-apply-lab-v1
    max_risk_class_v1: reversible_low
    allowed_operations:
      - add account or campaign label
      - create platform draft or experiment draft
    forbidden_operations:
      - budget change
      - bidding change
      - live ad copy change
      - audience targeting change
      - conversion tracking change
      - pause or enable campaign
    required_gates:
      - runtime_security_review_id
      - active ApprovalReceipt
      - exact account/campaign/ad group scope
      - pre_apply EvidenceArtifact
      - rollback plan
      - post_apply readback EvidenceArtifact

  trigger:
    accepted_inputs:
      - health check
      - account readiness
      - check if JP Ads is healthy
      - diagnose conversion tracking
      - run drift scan
    required_scope:
      - tenant
      - time window
      - health area or all-account scope

  self_check:
    must_confirm:
      - Jetpartner overlay loaded
      - TENANT_ID scope is Jetpartner when command guidance is used
      - no live mutation is implied by a health check
      - conversion tracking claims have platform or Supabase evidence
      - landing-page outage claims have browser or runtime evidence
      - recommendations are separated from approved apply-lab operations

  task_graph:
    - step: collect_health_sources
      mode: read
      capability_refs:
        - paid_media_platform
        - analytics_source
        - crm_quality_source
        - landing_page_source
      outputs:
        - preflight or observe status
        - conversion action evidence
        - recent spend/conversion evidence
        - CRM qualified lead source reference
        - landing page smoke evidence
    - step: classify_health_state
      mode: observe
      capability_refs:
        - paid_media_platform
        - analytics_source
        - crm_quality_source
      outputs:
        - green checks
        - soft warnings
        - hard blockers
        - owner action list
        - false-positive risks
    - step: draft_health_recommendation
      mode: propose
      capability_refs:
        - paid_media_platform
        - landing_page_source
      outputs:
        - health diagnosis
        - proposed fixes
        - blocked live actions
        - evidence table
    - step: approval_gate
      mode: propose
      capability_refs:
        - paid_media_platform
        - memory_patch
      outputs:
        - approval packet if apply_lab is requested
        - exact object scope
        - rollback note
    - step: apply_lab_execute_approved_health_label_or_draft
      mode: apply
      apply_lab: true
      capability_refs:
        - paid_media_platform
      runs_only_when:
        - approved_for_apply_lab
        - runtime binding available
        - requested operation is in apply_lab.allowed_operations
      outputs:
        - apply_run EvidenceArtifact
        - platform readback
        - rollback reference
    - step: readback_and_delta
      mode: observe
      capability_refs:
        - paid_media_platform
        - analytics_source
        - crm_quality_source
      outputs:
        - final health state
        - hard blockers
        - owner action list
        - post_run_delta

  future_live_action_policy:
    default_state: propose_only_unless_apply_lab_requested
    allowed_only_after:
      - runtime_security_review_id
      - approval receipt
      - exact account/campaign/ad group scope
      - pre-change evidence
      - rollback or irreversible-action note
      - post-apply readback

  evidence_packet:
    required:
      - preflight or observe result when account access is discussed
      - account or campaign scope
      - time window
      - conversion action evidence when conversion health is discussed
      - Supabase or qualified lead source when lead quality is discussed
      - landing page URL when site health is discussed
      - approval receipt if apply_lab executes
      - apply_run artifact if apply_lab executes

  failure_behavior:
    missing_platform_source: stop_and_request_source
    missing_crm_quality_for_lead_claim: remove_claim_or_request_source
    missing_landing_page_evidence: remove_outage_claim_or_request_source
    approval_missing_for_apply_lab: stop_at_plan
    operation_outside_apply_lab: stop_at_plan

  readback:
    include:
      - checks run
      - green state
      - warnings
      - blockers
      - owner actions
      - learning route

  semantic_delta:
    tail_rule: "After every run, edit the right playbook tail if health checks, blocker classes, owner-action format, or readback shape changed."
    route_options:
      - tenant_memory_patch
      - account_health_playbook_patch
      - workflow_patch
      - skill_patch
      - new_skill_candidate
      - protocol_update
    default_route: workflow_patch
    promotion_requires:
      - repeated evidence
      - owner
      - review_after
      - contradiction check
```

## Playbook Rule

Account health check is not daily maintenance. It is invoked when the task is readiness, tracking, drift, access, or blocker diagnosis. It can produce proposals and owner actions; it does not silently fix live systems.
