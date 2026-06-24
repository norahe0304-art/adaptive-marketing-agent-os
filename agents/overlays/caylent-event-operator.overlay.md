<!--
[INPUT]: Depends on event-adaptive-operator.role.md, Caylent event operating evidence, and Caylent Event workflow contracts.
[OUTPUT]: Provides Caylent tenant overlay for Event Adaptive Operator.
[POS]: overlays tenant truth layer mounted on the Event base role; names Slack as an approval/readback surface, not a runtime.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Caylent Event Operator Overlay

This overlay mounts Caylent-specific operating truth on top of `event-adaptive-operator`. Caylent's team approves and reads back in Slack threads, so Slack is named here as an approval/readback surface. Which agent runtime runs the work is the user's choice and is not encoded here.

```yaml
tenant_overlay:
  identity:
    id: caylent-event-operator
    tenant: Caylent
    mounts_on: event-adaptive-operator
    version: 0.1.0

  tenant_truth_boundary:
    allowed_here:
      - tenant naming conventions
      - HubSpot portal binding notes
      - Salesforce read-only context notes
      - Slack approval/readback surface
      - approval owners and approval surfaces
      - launch checklist deltas
    forbidden_here:
      - reusable Event base-role rules
      - shared Agent OS protocol
      - real secrets
      - uncited tenant facts
      - unapproved publish/send/activate permissions

  runtime_bindings:
    binding_owner: tenant_overlay
    abstract_surface_map:
      event_asset_system:
        provider: hubspot
        provider_surfaces:
          - pages
          - emails
          - workflows
          - lists
        binding_rule: "Use configured tenant connector only; never store secrets in this overlay."
      crm_context_source:
        provider: salesforce
        mode: read
        usage: "Use for account and campaign context evidence; no CRM writes from this workflow."
      document_source:
        provider: tenant-document-store
        mode: read_observe_propose
      calendar_source:
        provider: tenant-calendar
        mode: read_observe
      memory_patch:
        provider: tenant-memory
        mode: propose

  operating_contract:
    event_launch_defaults:
      - collect brief before drafting assets
      - map event to campaign or campaign placeholder
      - create draft assets before requesting approval
      - require approval before page publish, email send, workflow activation, or list mutation
      - produce launch readback in the originating Slack thread or configured portal
    approval_surfaces:
      - slack_thread_receipt
      - portal_approval_record
      - document_comment_receipt

  capability_overrides:
    default_mode: propose
    max_mode_v1: propose
    future_live_action_default: blocked_by_runtime_review
    allowed_without_human_approval:
      - read brief
      - read CRM context
      - draft landing page copy
      - draft email copy
      - draft workflow checklist
      - prepare list update proposal
    approval_required_for:
      - page publish
      - email send
      - workflow activation
      - list membership mutation
      - tenant memory promotion

  evidence_contract:
    artifact_schema: agents/protocols/approval-evidence.schema.md#EvidenceArtifact
    required:
      - brief source
      - Slack thread or portal request reference
      - HubSpot campaign or placeholder ID
      - draft asset URLs
      - Salesforce source reference when account context is used
      - approval receipt when future live action is requested
      - launch readback

  tenant_memory_records:
    - id: caylent-slack-approval-surface
      fact: "Caylent Event approvals and launch readbacks happen in Slack threads."
      source_of_truth: operating_contract.approval_surfaces
      evidence_url: .omo/plans/adaptive-agent-review-board.zh-CN.html
      owner: event-operator
      last_verified_at: "2026-06-21"
      review_after: "2026-07-21"
      promotion_target: tenant_memory
      expiry_reason: ""
    - id: caylent-hubspot-draft-surfaces
      fact: "Caylent Event workflow may prepare HubSpot page, email, workflow, and list proposals."
      source_of_truth: runtime_bindings.abstract_surface_map.event_asset_system.provider_surfaces
      evidence_url: .omo/plans/adaptive-agent-review-board.zh-CN.html
      owner: event-operator
      last_verified_at: "2026-06-21"
      review_after: "2026-07-21"
      promotion_target: tenant_memory
      expiry_reason: ""
    - id: caylent-salesforce-read-only
      fact: "Salesforce context is read-only in the Caylent Event workflow."
      source_of_truth: runtime_bindings.abstract_surface_map.crm_context_source.mode
      evidence_url: .omo/plans/adaptive-agent-review-board.zh-CN.html
      owner: event-operator
      last_verified_at: "2026-06-21"
      review_after: "2026-07-21"
      promotion_target: tenant_memory
      expiry_reason: ""

  overlay_memory_rule:
    fields:
      - source_of_truth
      - evidence_url
      - owner
      - last_verified_at
      - review_after
      - promotion_target
      - expiry_reason
    promotion_targets:
      tenant_memory: "Stable Caylent operating truth."
      event_playbook: "Reusable Event rule proven across tenants."
      workflow: "Repeated Caylent Event procedure."
      skill_candidate: "Stable launch procedure worth packaging."
      protocol: "Shared OS change; requires cross-role proof."

  learning_route:
    default: tenant_memory
    must_not_promote_to_base_role:
      - Caylent Slack approval surface
      - Caylent HubSpot naming rules
      - Caylent approval owners
      - Caylent Slack thread conventions
```

## Overlay Rule

This file is the tenant adapter. It may name Slack as the approval/readback surface because Caylent's team works there, but this surface choice must not leak into the Event base role or the shared protocol, and it never names which agent runtime runs the work.
