<!--
[INPUT]: Depends on event-adaptive-operator.role.md, Caylent event operating evidence, and Caylent Event workflow contracts.
[OUTPUT]: Provides Caylent tenant overlay for Event Adaptive Operator.
[POS]: overlays tenant truth and host adapter selection layer mounted on the Event base role.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Caylent Event Operator Overlay

This overlay mounts Caylent-specific operating truth on top of `event-adaptive-operator`. It is where Slack/Hermes belongs for this tenant; Hermes is not the Agent OS core.

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
      - Slack/Hermes host preference
      - approval owners and approval surfaces
      - launch checklist deltas
    forbidden_here:
      - reusable Event base-role rules
      - shared Agent OS protocol
      - real secrets
      - uncited tenant facts
      - unapproved publish/send/activate permissions

  host_adapters:
    required:
      - slack
    optional:
      - portal
      - codex
    preferred:
      slack: hermes
    unsupported: []
    notes: "Caylent event operations use Slack as the required host and Hermes as the preferred Slack adapter."

  tool_bindings:
    hubspot:
      surfaces:
        - pages
        - emails
        - workflows
        - lists
      binding_rule: "Use configured tenant connector only; never store secrets in this overlay."
    salesforce:
      mode: read
      usage: "Use for account and campaign context evidence; no CRM writes from this workflow."

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
    - id: caylent-slack-hermes-host
      fact: "Caylent Event operations require Slack and prefer Hermes as the Slack adapter."
      source_of_truth: host_adapters.preferred
      evidence_url: .omo/plans/adaptive-agent-review-board.zh-CN.html
      owner: event-operator
      last_verified_at: "2026-06-21"
      review_after: "2026-07-21"
      promotion_target: tenant_memory
      expiry_reason: ""
    - id: caylent-hubspot-draft-surfaces
      fact: "Caylent Event workflow may prepare HubSpot page, email, workflow, and list proposals."
      source_of_truth: tool_bindings.hubspot.surfaces
      evidence_url: .omo/plans/adaptive-agent-review-board.zh-CN.html
      owner: event-operator
      last_verified_at: "2026-06-21"
      review_after: "2026-07-21"
      promotion_target: tenant_memory
      expiry_reason: ""
    - id: caylent-salesforce-read-only
      fact: "Salesforce context is read-only in the Caylent Event workflow."
      source_of_truth: tool_bindings.salesforce.mode
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
      - Caylent host preference
      - Caylent HubSpot naming rules
      - Caylent approval owners
      - Caylent Slack thread conventions
```

## Overlay Rule

This file is the tenant adapter. It may require Slack and prefer Hermes because Caylent Event needs that host, but this preference must not leak into the Event base role or the shared protocol.
