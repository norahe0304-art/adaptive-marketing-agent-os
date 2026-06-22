<!--
[INPUT]: Depends on event-adaptive-operator.role.md, caylent-event-operator.overlay.md, OMO governance, and GEB delta protocol.
[OUTPUT]: Provides Caylent Event launch workflow with draft, approval-gated apply lab, readback, and learning routes.
[POS]: workflows first Event implementation path; consumes shared protocol and Caylent overlay.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Caylent Event Launch Workflow

This workflow runs the Event base role through the Caylent overlay. It is proposal-first by default, with V1 apply lab for approved HubSpot draft asset creation. Publish, send, activate, and list membership mutation remain outside V1 apply lab.

```yaml
workflow_contract:
  id: caylent-event-launch
  role: event-adaptive-operator
  overlay: caylent-event-operator
  default_mode: propose
  workflow_kind: event_launch_approval_first

  apply_lab:
    enabled: true
    runtime_binding_id: caylent-event-apply-lab-v1
    max_risk_class_v1: reversible_low
    allowed_operations:
      - create HubSpot draft page
      - create HubSpot draft email
      - create HubSpot draft workflow artifact
      - create HubSpot list draft or static draft
    forbidden_operations:
      - page publish
      - email send
      - workflow activation
      - list membership mutation
      - Salesforce write
    required_gates:
      - runtime_security_review_id
      - active ApprovalReceipt
      - exact HubSpot portal and asset scope
      - pre_apply EvidenceArtifact
      - rollback plan
      - post_apply readback EvidenceArtifact

  trigger:
    accepted_inputs:
      - create event launch kit
      - prepare HubSpot event assets
      - draft promotion email
      - prepare workflow/list changes
      - prepare future launch packet after approval request
    required_scope:
      - event brief
      - event owner
      - launch deadline
      - target audience
      - channels

  self_check:
    must_confirm:
      - Caylent overlay loaded
      - Slack host thread or portal request identified
      - no apply_lab draft creation requested without runtime security review, active approval, exact scope, and rollback
      - HubSpot context available
      - Salesforce context is read-only if used

  task_graph:
    - step: brief_received
      mode: read
      outputs:
        - brief summary
        - missing fields
        - owner and deadline
    - step: context_collected
      mode: read
      outputs:
        - HubSpot campaign or placeholder reference
        - Salesforce account context reference
        - prior asset examples
    - step: drafting_assets
      mode: propose
      outputs:
        - landing page draft
        - email draft
        - workflow draft checklist
        - list update proposal
    - step: ready_for_approval
      mode: propose
      outputs:
        - approval packet
        - affected assets
        - risk class
        - launch checklist
    - step: apply_lab_create_draft_assets
      mode: apply
      apply_lab: true
      runs_only_when:
        - approved_for_apply_lab
        - runtime binding available
        - requested operation is in apply_lab.allowed_operations
      outputs:
        - apply_run EvidenceArtifact
        - HubSpot draft asset URLs
        - rollback reference
    - step: launch_packet_prepared
      mode: propose
      outputs:
        - future launch approval packet
        - blocked reason for live action
        - exact asset and list scope
    - step: readback
      mode: observe
      outputs:
        - final status
        - evidence table
        - open blockers
        - post_run_delta

  future_live_action_policy:
    default_state: apply_lab_requires_approval
    approval_required_for:
      - page publish
      - email send
      - workflow activation
      - list membership mutation
    allowed_only_after:
      - runtime_security_review_id
      - named approver
      - Slack thread, portal, or document approval receipt
      - exact HubSpot asset scope
      - pre-change evidence
      - rollback or irreversible-action note
      - apply_run evidence when apply_lab executes

  evidence_packet:
    required:
      - event brief source
      - Slack thread or portal request reference
      - HubSpot campaign or placeholder ID
      - draft asset URLs
      - Salesforce source reference if used
      - approval receipt when future live action is requested
      - apply_run artifact if apply_lab executes
      - proposal readback

  failure_behavior:
    missing_brief: request_missing_fields
    missing_host_thread: stop_and_request_host_context
    missing_hubspot_context: draft_plan_only
    missing_approval_for_apply_lab: stop_at_ready_for_approval
    operation_outside_apply_lab: stop_at_ready_for_approval
    unclear_salesforce_context: remove_claim_or_request_source

  readback:
    include:
      - what was requested
      - assets drafted
      - live actions requested or blocked
      - approval evidence
      - remaining owner actions
      - learning route

  semantic_delta:
    route_options:
      - tenant_memory_patch
      - event_playbook_patch
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

## Workflow Rule

The launch packet models the full lifecycle. V1 apply lab may create approved draft assets only; publish, send, activate, and list membership mutation remain blocked until a separate runtime security review expands the allowed operation list.
