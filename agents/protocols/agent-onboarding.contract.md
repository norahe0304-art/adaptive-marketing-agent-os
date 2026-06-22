<!--
[INPUT]: Depends on role-package.schema.md, capability-boundary.schema.md, approval-evidence.schema.md, host-adapter.interface.md, and geb-semantic-delta.md.
[OUTPUT]: Provides workflow_contract and onboarding checklist for any new marketing agent.
[POS]: protocols scale rule for adding future Ads, Event, SEO, Content, Lifecycle, or Partner Ops agents.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Agent Onboarding Contract

New marketing agents must be boring to add. They fill the same onboarding contract instead of inventing a new protocol.

## Required Declaration

```yaml
agent_onboarding:
  domain: ""
  base_role: ""
  tenant_overlay: ""
  workflow_contract: ""
  capability_surface: []
  host_adapters:
    required: []
    optional: []
    preferred: {}
    unsupported: []
  evidence_contract: []
  approval_policy: ""
  approval_receipt_schema: "agents/protocols/approval-evidence.schema.md#ApprovalReceipt"
  evidence_artifact_schema: "agents/protocols/approval-evidence.schema.md#EvidenceArtifact"
  learning_route: []
  post_run_delta: ""
```

## Onboarding Steps

1. Declare `domain`: Ads, Event, SEO, Content, Lifecycle, Partner Ops, or another named marketing domain.
2. Declare `base_role`: reusable role file with no tenant truth.
3. Declare `tenant_overlay`: stable operating contract and source pointers.
4. Declare `workflow_contract`: inputs, outputs, task graph, evidence, approval gate, failure behavior, readback.
5. Declare `learning_route`: tenant memory, industry playbook, workflow patch, skill candidate, or protocol update.

## Acceptance

- Base role contains no tenant truth.
- Overlay contains no unbounded transcript, CRM export, or raw campaign history.
- Workflow stops at propose unless a future runtime security review and full approval gate exist.
- Host adapter choice does not leak into shared protocol.
- GEB delta route is declared before completion.
