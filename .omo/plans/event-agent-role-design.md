# event-agent-role-design - Work Plan

## TL;DR

**What you'll get:** Event Adaptive Agent for Caylent: reusable `event-adaptive-operator` base role, `caylent-event-operator` tenant overlay, HubSpot event launch workflow, overlay-defined collaboration host usage, campaign association evidence, approval/audit surfaces.

**Owner:** Event agent.

**Consumes:** `.omo/plans/shared-agent-os-protocol.md`.

**Produces:** Event role artifacts and Caylent-specific operating contracts.

**Does not produce:** Shared Role schema, host adapter interface, OMO governance, GEB protocol, Ads workflow, or tenant adapter runtime.

## Responsibility Boundary

Event agent consumes the shared Agent OS protocol.  
Event agent does not define the shared Agent OS protocol.

```text
Shared Agent OS Protocol
  -> role schema
  -> host adapter interface
  -> capability boundary
  -> approval/evidence contract
  -> OMO governance
  -> GEB semantic delta

Event Agent
  -> event-adaptive-operator
  -> caylent-event-operator overlay
  -> overlay-defined host preference
  -> HubSpot event launch workflow
  -> campaign association evidence
  -> approval/audit handoff
```

## Scope In

- `agents/roles/event-adaptive-operator.role.md`
- `agents/overlays/caylent-event-operator.overlay.md`
- `agents/workflows/caylent-event-launch.workflow.md`
- HubSpot draft asset tool surface.
- Salesforce read-only context surface.
- Caylent collaboration host requirement with preferred adapter.
- Caylent tenant memory boundary.
- Campaign association evidence.
- Approval gates for publish/send/activate/list updates.
- Portal evidence console notes if needed.

## Scope Out

- No shared Role schema definition.
- No shared Host Adapter Interface definition.
- No Ads role.
- No Google Ads tools.
- No tenant adapter runtime implementation.
- No actual HubSpot publish/send/activate actions.
- No Salesforce mutation.
- No Caylent facts inside the base Event role.

## Inputs From Shared Protocol

Event role must conform to:

- `agents/protocols/role-package.schema.md`
- `agents/protocols/capability-boundary.schema.md`
- `agents/protocols/host-adapter.interface.md`
- `agents/protocols/omo-execution-governance.md`
- `agents/protocols/geb-semantic-delta.md`

Event role must not define new protocol fields, permission modes, approval states, host kinds, or evidence semantics. If Event needs a new shared semantic, update `shared-agent-os-protocol.md` first.

## Base Event Role

Create `agents/roles/event-adaptive-operator.role.md`.

Purpose:

- Operate B2B event launch workflows through evidence-first loops.
- Draft and coordinate event pages, emails, workflows, lists, campaign associations, and approval packets.
- Read CRM/account context before creating launch assets.
- Produce proposals and draft artifacts before publish/send/activate actions.

Structured host adapters:

```yaml
host_adapters:
  required: []
  optional:
    - portal
    - codex
    - slack
  preferred: {}
  unsupported: []
  notes: "Base Event role is host-neutral; tenant overlays may require a collaboration host."
```

Capability surface:

- `hubspot.pages`: draft/propose; publish requires approval.
- `hubspot.emails`: draft/propose; send requires approval.
- `hubspot.workflows`: draft/propose; activate requires approval.
- `hubspot.lists`: read/propose; list updates require approval.
- `salesforce`: read only.
- `docs`: draft briefs, launch plans, and approval packets.

Evidence contract:

- event brief
- campaign id
- asset urls
- CRM/account context source
- approval receipts
- owner identity
- launch timestamp
- failure/readback notes

Lifecycle:

```text
brief_received
  -> context_collected
  -> drafting_assets
  -> ready_for_approval
  -> launch_packet_prepared
  -> post_run_delta
```

Must not include:

- Caylent tenant-only facts
- real HubSpot portal IDs
- real Salesforce account IDs
- unapproved publish/send/activate behavior

## Caylent Overlay

Create `agents/overlays/caylent-event-operator.overlay.md`.

Overlay adds:

- `mounts_on: event-adaptive-operator`
- Caylent tenant memory boundary
- Caylent event naming conventions
- Caylent HubSpot portal binding notes
- Caylent Salesforce read-only context notes
- Caylent approval owners and approval receipt requirements
- Caylent portal evidence console surfaces
- tenant-specific launch checklist deltas
- required Slack host with overlay-defined adapter

Overlay must not duplicate the base Event role.

Caylent host adapter instance:

```yaml
host_adapters:
  required:
    - slack
  optional:
    - portal
    - codex
  preferred:
    slack: overlay-defined
  unsupported: []
  notes: "Caylent Event uses Slack as the primary collaboration host; the preferred adapter is defined in the overlay."
```

Overlay memory rule: overlays store stable tenant operating contracts and pointers to sources of truth, not unbounded transcripts, CRM exports, or raw campaign history. Each tenant fact must include `source_of_truth`, `evidence_url`, `owner`, `last_verified_at`, `review_after`, and `promotion_target` or `expiry_reason`.

## Caylent Event Launch Workflow

Create `agents/workflows/caylent-event-launch.workflow.md`.

Workflow:

```text
brief_received
  -> normalize Caylent event brief
  -> read Salesforce/account context
  -> draft HubSpot page/email/workflow/list assets
  -> associate campaign id
  -> prepare Slack approval packet
  -> prepare future launch packet
  -> block publish/send/activate until runtime security review
  -> evidence readback
  -> semantic delta handoff
```

Default stop point: approval packet and draft assets.

Publish/send/activate/list updates require explicit approval and a future runtime security review. V1 execution stops at proposal/approval packet.

Approval rule: the agent cannot approve its own proposal. Approval receipts must name the human approver, approved action, tenant/account, timestamp, evidence packet, exact mutation scope, expiry, channel, and revocation state. Missing, stale, or unbound approval keeps the workflow in proposal mode.

## Event Learning Rules

Event-specific deltas route to shared GEB learning classes:

- tenant memory patch for Caylent-only truth
- industry playbook patch for reusable B2B event launch patterns
- workflow patch for repeatable HubSpot event launch steps
- skill patch only after repeated stable use
- new skill candidate only after review

Interactive session learning is allowed. Record & Replay is required only when promoting a stable repeatable workflow into automation.

## Todos

- [ ] 1. Confirm shared Agent OS protocol files exist or mark Event plan blocked on shared architecture.
- [ ] 2. Create/validate `agents/roles/event-adaptive-operator.role.md`.
- [ ] 3. Create/validate `agents/overlays/caylent-event-operator.overlay.md`.
- [ ] 4. Create/validate `agents/workflows/caylent-event-launch.workflow.md`.
- [ ] 5. Add Event capability surface for HubSpot, Salesforce read-only context, docs, optional Slack approval packets, and portal evidence.
- [ ] 6. Add Caylent-specific evidence, approval, and learning rules.
- [ ] 7. Verify base Event role has no Caylent tenant facts.
- [ ] 8. Verify workflow is proposal/approval-first by default.
- [ ] 9. Verify Event GEB docs list role, overlay, and workflow files with `[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md`.

## Acceptance

```bash
test -f agents/roles/event-adaptive-operator.role.md
test -f agents/overlays/caylent-event-operator.overlay.md
test -f agents/workflows/caylent-event-launch.workflow.md
test -f agents/roles/AGENTS.md
test -f agents/overlays/AGENTS.md
test -f agents/workflows/AGENTS.md
for token in identity capability_surface host_adapters approval_policy evidence_contract learning_rules; do
  rg -q "$token" agents/roles/event-adaptive-operator.role.md
done
for token in event-adaptive-operator HubSpot host_adapters hubspot.pages hubspot.emails hubspot.workflows hubspot.lists salesforce "campaign id" "asset urls" "approval receipts"; do
  rg -q "$token" agents/roles/event-adaptive-operator.role.md
done
for token in mounts_on event-adaptive-operator Caylent "approval owners" "portal evidence" "tenant memory" slack source_of_truth evidence_url owner last_verified_at review_after; do
  rg -q "$token" agents/overlays/caylent-event-operator.overlay.md
done
for token in brief_received context_collected drafting_assets ready_for_approval launch_packet_prepared approval; do
  rg -q "$token" agents/workflows/caylent-event-launch.workflow.md
done
rg -q "\\[PROTOCOL\\]: 变更时更新此头部，然后检查 AGENTS.md" agents/roles/AGENTS.md agents/overlays/AGENTS.md agents/workflows/AGENTS.md
rg -q "event-adaptive-operator.role.md" agents/roles/AGENTS.md
rg -q "caylent-event-operator.overlay.md" agents/overlays/AGENTS.md
rg -q "caylent-event-launch.workflow.md" agents/workflows/AGENTS.md
! rg -n "Caylent|real HubSpot portal ID|real Salesforce account ID|slack: overlay-defined" agents/roles/event-adaptive-operator.role.md
! rg -n "defines shared Role schema|defines Host Adapter Interface|implements host runtime|approval bypass" agents/roles/event-adaptive-operator.role.md agents/overlays/caylent-event-operator.overlay.md agents/workflows/caylent-event-launch.workflow.md
```

## Final Success Criteria

- Event plan is domain-focused.
- Event consumes shared protocol instead of defining it.
- Base Event role is tenant-neutral.
- Caylent overlay contains tenant truth.
- Concrete collaboration host preference is overlay-specific, not global and not base Event.
- HubSpot actions stay draft/approval-first unless approved.
- Campaign evidence and approval receipts are first-class.
