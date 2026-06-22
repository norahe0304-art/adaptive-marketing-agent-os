<!--
[INPUT]: Depends on ads-adaptive-operator.role.md, jetpartners-ads-operator.overlay.md, 30x-ads ads-daily legacy playbook wrapper, OMO governance, and GEB delta protocol.
[OUTPUT]: Provides JP Ads daily maintenance playbook workflow with morning brief triage, approval-gated apply lab, dashboard readback, and learning routes.
[POS]: workflows JP Ads daily maintenance playbook; internal workflow contract behind the Ads Role's daily operator task.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Jetpartner Ads Daily Maintenance Workflow

This workflow is the machine-readable contract behind the Ads Role's `daily maintenance` playbook for Jetpartner. It maps the existing 30x-ads `/ads-daily` operating pattern into Role-first OS terms.

```yaml
workflow_contract:
  id: jetpartners-ads-daily-maintenance
  role: ads-adaptive-operator
  overlay: jetpartners-ads-operator
  default_mode: propose
  workflow_kind: ads_daily_maintenance_playbook

  playbook:
    name: daily maintenance
    product_surface: role_playbook
    internal_workflow_contract: true
    source_surfaces:
      - "30x-ads .claude/skills/ads-daily/SKILL.md as legacy playbook wrapper"
      - "30x-ads tenants/jetpartners/scripts/daily-9-30am.sh as read-only prep runtime"
    calls_skills:
      - ads-monitor
      - ads-health
      - ads-keywords
      - ads-audit

  apply_lab:
    enabled: true
    runtime_binding_id: jp-ads-daily-apply-lab-v1
    max_risk_class_v1: reversible_low
    allowed_operations:
      - add negative keyword
      - add exact positive keyword
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
      - run daily maintenance
      - review today's morning brief
      - process JP daily ads items
      - go through today's optimizations
    required_scope:
      - tenant
      - business date
      - morning brief path
      - actions artifact path

  self_check:
    must_confirm:
      - Jetpartner overlay loaded
      - current business date resolved in America/New_York
      - morning brief exists or can be rebuilt
      - actions artifact exists or audit prep must run first
      - no apply_lab mutation requested without user confirmation, runtime review, exact scope, and rollback
      - dashboard publish/readback target available

  task_graph:
    - step: load_daily_artifacts
      mode: read
      capability_refs:
        - paid_media_platform
        - analytics_source
        - crm_quality_source
      outputs:
        - morning brief
        - actions artifact
        - audit digest references
        - lead quality snapshot
        - account change log reference
    - step: triage_decision_queue
      mode: observe
      capability_refs:
        - paid_media_platform
        - analytics_source
        - crm_quality_source
      outputs:
        - swall todos
        - red monitor items
        - yellow monitor items
        - growth candidates
        - skip candidates
    - step: draft_daily_plan
      mode: propose
      capability_refs:
        - paid_media_platform
        - landing_page_source
      outputs:
        - ordered decision queue
        - proposed mutations
        - expected CPA impact
        - evidence links
        - risk notes
    - step: approval_gate
      mode: propose
      capability_refs:
        - paid_media_platform
        - memory_patch
      outputs:
        - decision summary
        - mutation batch preview
        - explicit yes/no/change-mind request
        - rollback note
    - step: apply_lab_execute_approved_batch
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
        - changed-object readback
        - conflict audit reference
        - rollback reference
    - step: publish_and_readback
      mode: observe
      capability_refs:
        - paid_media_platform
        - analytics_source
        - crm_quality_source
      outputs:
        - daily report URL
        - applied/skipped summary
        - failed or deferred items
        - post_run_delta

  future_live_action_policy:
    default_state: apply_lab_requires_approval
    allowed_only_after:
      - runtime_security_review_id
      - approval receipt
      - exact account/campaign/ad group scope
      - pre-change evidence
      - rollback or irreversible-action note
      - post-apply readback

  evidence_packet:
    required:
      - morning-brief-<date>.md
      - actions-<date>.json
      - audit-full-<date>.md
      - monitor-<date>.md
      - lead-quality-<date>.json when lead quality is discussed
      - account-changes-<date>.json when shipped changes are discussed
      - approval receipt if apply_lab executes
      - apply_run artifact if apply_lab executes
      - final report URL

  failure_behavior:
    missing_morning_brief: rebuild_once_then_stop
    missing_actions_artifact: stop_and_request_daily_prep
    approval_missing_for_apply_lab: stop_at_plan
    operation_outside_apply_lab: stop_at_plan
    publish_failed: keep_local_readback_and_report_failure
    swall_writeback_failed: save_pending_writeback

  readback:
    include:
      - what was reviewed
      - what was applied
      - what was skipped
      - evidence used
      - dashboard URL
      - learning route

  semantic_delta:
    route_options:
      - tenant_memory_patch
      - ads_playbook_patch
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

Daily maintenance is a role playbook, not a skill. The existing 30x-ads `/ads-daily` skill is treated as a legacy playbook wrapper until it is split into this workflow plus smaller atomic skills. The playbook owns the business route. Its workflow contract owns steps, capability refs, approval gates, and readback. Skills are atomic actions the playbook may call.
