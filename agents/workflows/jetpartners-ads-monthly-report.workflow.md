<!--
[INPUT]: Depends on ads-adaptive-operator.role.md, jetpartners-ads-operator.overlay.md, 30x-ads ads-monthly-report/ads-report behavior, monthly report artifacts, OMO governance, and GEB delta protocol.
[OUTPUT]: Provides JP Ads monthly report playbook workflow for month-window evidence, client-facing narrative, approval/review, delivery readback, and learning routes.
[POS]: workflows JP Ads monthly report playbook; internal workflow contract behind the Ads Role's month-end client report task.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Jetpartner Ads Monthly Report Workflow

This workflow is the machine-readable contract behind the Ads Role's `monthly-report` playbook for Jetpartner. It is separate from daily maintenance because it has a different audience, data window, narrative, and delivery surface.

```yaml
workflow_contract:
  id: jetpartners-ads-monthly-report
  role: ads-adaptive-operator
  overlay: jetpartners-ads-operator
  default_mode: propose
  workflow_kind: ads_monthly_report_playbook

  playbook:
    name: monthly report
    product_surface: role_playbook
    internal_workflow_contract: true
    source_surfaces:
      - "30x-ads .claude/skills/ads-monthly-report/SKILL.md"
      - "30x-ads .claude/skills/ads-report/SKILL.md"
      - "30x-ads scripts/build-monitor-report.ts"
      - "30x-ads scripts/publish-dashboard.ts"
    calls_skills:
      - ads-monthly-report
      - ads-report
      - ads-audit

  apply_lab:
    enabled: true
    runtime_binding_id: jp-ads-monthly-report-apply-lab-v1
    max_risk_class_v1: reversible_low
    allowed_operations:
      - create report draft
      - publish client-safe report page
      - create swall report issue draft
    forbidden_operations:
      - Google Ads mutation
      - Supabase mutation
      - budget change
      - bidding change
      - live ad copy change
      - conversion tracking change
    required_gates:
      - runtime_security_review_id
      - active ApprovalReceipt for publishing or swall issue creation
      - exact tenant and month scope
      - pre_apply EvidenceArtifact
      - rollback or correction plan
      - post_apply readback EvidenceArtifact

  trigger:
    accepted_inputs:
      - monthly report
      - month-end report
      - client report
      - what did we do this month
      - send monthly update
    required_scope:
      - tenant
      - report month
      - audience
      - delivery surface

  self_check:
    must_confirm:
      - Jetpartner overlay loaded
      - report month resolved
      - report audience is client-facing or internal
      - daily artifacts and shipped changes exist for the month or missing data is disclosed
      - no platform mutation is requested by this playbook
      - publish/swall delivery has approval if requested

  task_graph:
    - step: collect_month_window_evidence
      mode: read
      capability_refs:
        - paid_media_platform
        - analytics_source
        - crm_quality_source
      outputs:
        - month artifact index
        - lead and qualified lead summary
        - shipped changes
        - account health summary
        - unresolved blockers
    - step: classify_month_story
      mode: observe
      capability_refs:
        - paid_media_platform
        - analytics_source
        - crm_quality_source
      outputs:
        - wins
        - regressions
        - lead quality narrative
        - next-month priorities
        - evidence gaps
    - step: draft_client_report
      mode: propose
      capability_refs:
        - paid_media_platform
        - landing_page_source
      outputs:
        - monthly report draft
        - client-safe summary
        - internal notes excluded from client view
        - next-month recommendation
    - step: approval_gate
      mode: propose
      capability_refs:
        - paid_media_platform
        - memory_patch
      outputs:
        - report approval packet
        - delivery plan
        - correction plan
    - step: apply_lab_publish_or_create_report_issue
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
        - published report URL or issue draft URL
        - correction reference
    - step: readback_and_delta
      mode: observe
      capability_refs:
        - paid_media_platform
        - analytics_source
        - crm_quality_source
      outputs:
        - report status
        - delivery target
        - evidence caveats
        - post_run_delta

  future_live_action_policy:
    default_state: report_draft_only
    allowed_only_after:
      - runtime_security_review_id
      - approval receipt for publish or swall issue
      - exact tenant and month scope
      - pre-delivery evidence
      - correction plan
      - post-delivery readback

  evidence_packet:
    required:
      - report month
      - dashboard URL or generated report path
      - account/campaign scope when campaign claims are made
      - lead quality evidence when quality is discussed
      - shipped changes or account-changes references
      - missing data disclosure when artifacts are incomplete
      - approval receipt if publish or swall delivery executes
      - apply_run artifact if apply_lab executes

  failure_behavior:
    missing_month_artifacts: disclose_gap_and_draft_only
    missing_crm_quality_for_quality_claim: remove_claim_or_request_source
    unclear_audience: draft_internal_only
    approval_missing_for_publish: stop_at_draft
    publish_failed: keep_local_report_and_report_failure

  readback:
    include:
      - report month
      - sources used
      - published or draft status
      - client-safe URL or path
      - missing data caveats
      - learning route

  semantic_delta:
    tail_rule: "After every run, edit the right playbook tail if report sections, evidence tables, approval handoff, delivery channel, or readback shape changed."
    route_options:
      - tenant_memory_patch
      - monthly_report_playbook_patch
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

Daily reports stay inside daily maintenance as readback. Monthly report is a separate playbook because it owns a month window, client-facing narrative, delivery review, and month-end recommendations.
