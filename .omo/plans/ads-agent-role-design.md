# ads-agent-role-design - Work Plan

## TL;DR

**What you'll get:** Ads agent role design only: `ads-adaptive-operator`, Jetpartner overlay, Ads read-only review workflow, Ads-specific evidence/approval/learning rules.

**Owner:** Ads agent.

**Consumes:** `.omo/plans/shared-agent-os-protocol.md`.

**Produces:** Ads role artifacts and Jetpartner-specific operating contracts.

**Does not produce:** Role package schema, host adapter interface, OMO governance generalization, GEB protocol generalization, cross-role validation.

## Responsibility Boundary

Ads agent consumes the shared Agent OS protocol.  
Ads agent does not define the shared Agent OS protocol.

```text
Shared Agent OS Protocol
  -> role schema
  -> capability boundary
  -> approval/evidence contract
  -> OMO governance
  -> GEB semantic delta

Ads Agent
  -> ads-adaptive-operator
  -> jetpartners-ads-operator overlay
  -> Jetpartner read-only review workflow
  -> Ads-specific learning deltas
```

## Scope In

- `agents/roles/ads-adaptive-operator.role.md`
- `agents/overlays/jetpartners-ads-operator.overlay.md`
- `agents/workflows/jetpartners-ads-readonly-review.workflow.md`
- Ads-specific instances of shared `evidence_contract`.
- Ads-specific instances of shared `approval_policy`.
- Ads-specific instances of shared `learning_rules` that route deltas back to shared GEB protocol.
- GEB L2 docs for Ads role, overlay, and workflow directories if missing.

## Scope Out

- No shared Role schema definition.
- No shared Host Adapter Interface definition.
- No shared OMO/GEB protocol definition.
- No Event role.
- No tenant adapter or Slack runtime.
- No real Google Ads mutation.
- No Jetpartner facts inside base Ads role.

## Inputs From Shared Protocol

Ads role must conform to:

- `agents/protocols/role-package.schema.md`
- `agents/protocols/capability-boundary.schema.md`
- `agents/protocols/omo-execution-governance.md`
- `agents/protocols/geb-semantic-delta.md`

Ads role may reference `agents/protocols/host-adapter.interface.md`, but Ads does not require Slack or a concrete tenant adapter.

Ads role must not define new protocol fields, permission modes, approval states, host kinds, or evidence semantics. If Ads needs a new shared semantic, update `shared-agent-os-protocol.md` first.

## Base Ads Role

Create `agents/roles/ads-adaptive-operator.role.md`.

Purpose:

- Operate advertising accounts through read-first evidence loops.
- Support Google Ads, Meta, LinkedIn, TikTok, Microsoft, Apple, YouTube as capability surfaces where available.
- Analyze campaign structure, search terms, lead quality, budgets, creatives, landing pages, and conversion quality.
- Produce proposals before mutations.

Structured host adapters:

```yaml
host_adapters:
  required:
    - codex
  optional:
    - portal
    - slack
  preferred: {}
  unsupported: []
  notes: "Ads role can run through optional hosts without requiring one in the base role."
```

Must not include:

- Jetpartner
- Eric
- Benton
- `reports.30x.company/jetpartners`
- `Contacted`
- `Pre-Qualified`
- private aviation bad intent

## Jetpartner Overlay

Create `agents/overlays/jetpartners-ads-operator.overlay.md`.

Overlay adds:

- `mounts_on: ads-adaptive-operator`
- tenant memory boundary
- qualified lead truth
- Supabase qualified lead source
- report surface
- known bad intent such as private aviation mismatch
- read-only default
- human approval for mutations

Overlay must not duplicate the base role.

Overlay memory rule: overlays store stable tenant operating contracts and pointers to sources of truth, not unbounded transcripts, CRM exports, or raw campaign history. Each tenant fact must include `source_of_truth`, `evidence_url`, `owner`, `last_verified_at`, `review_after`, and `promotion_target` or `expiry_reason`.

## Jetpartner Read-Only Review Workflow

Create `agents/workflows/jetpartners-ads-readonly-review.workflow.md`.

Workflow:

```text
request
  -> confirm tenant and account
  -> gather ads/search-term/lead evidence
  -> classify lead quality
  -> identify waste and opportunity
  -> propose negatives/budget/copy/landing changes
  -> approval gate
  -> semantic delta handoff
  -> readback
```

Default stop point: proposal only.

Mutation requires explicit approval, and v1 execution still stops at proposal unless a later runtime/security review enables live `apply`.

Approval rule: the agent cannot approve its own proposal. Approval receipts must name the human approver, approved action, tenant/account, timestamp, evidence packet, and exact mutation scope. Missing or stale approval keeps the workflow in proposal mode.

## Ads Learning Rules

Ads-specific deltas route to shared GEB learning classes:

- tenant memory patch for Jetpartner-only truth
- industry playbook patch for reusable private aviation / B2B lead-quality patterns
- workflow patch for repeatable Ads review steps
- skill patch only after repeated stable use
- new skill candidate only after review

Interactive session learning is allowed. Record & Replay is required only when promoting a stable repeatable workflow into automation.

## Todos

- [ ] 1. Confirm shared Agent OS protocol files exist or mark Ads plan blocked on shared architecture.
- [ ] 2. Create/validate `agents/roles/ads-adaptive-operator.role.md`.
- [ ] 3. Create/validate `agents/overlays/jetpartners-ads-operator.overlay.md`.
- [ ] 4. Create/validate `agents/workflows/jetpartners-ads-readonly-review.workflow.md`.
- [ ] 5. Add Ads-specific evidence, approval, and learning rules.
- [ ] 6. Verify base Ads role has no Jetpartner tenant facts.
- [ ] 7. Verify workflow is read-only/proposal-first by default.
- [ ] 8. Verify Ads GEB docs list role, overlay, and workflow files with `[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md`.

## Acceptance

```bash
test -f agents/roles/ads-adaptive-operator.role.md
test -f agents/overlays/jetpartners-ads-operator.overlay.md
test -f agents/workflows/jetpartners-ads-readonly-review.workflow.md
test -f agents/roles/AGENTS.md
test -f agents/overlays/AGENTS.md
test -f agents/workflows/AGENTS.md
for token in identity capability_surface host_adapters approval_policy evidence_contract learning_rules; do
  rg -q "$token" agents/roles/ads-adaptive-operator.role.md
done
for token in mounts_on ads-adaptive-operator "qualified lead" read-only "human approval" source_of_truth evidence_url owner last_verified_at review_after; do
  rg -q "$token" agents/overlays/jetpartners-ads-operator.overlay.md
done
for token in inputs outputs "task graph" proposal approval_gate evidence readback semantic_delta; do
  rg -q "$token" agents/workflows/jetpartners-ads-readonly-review.workflow.md
done
rg -q "\\[PROTOCOL\\]: 变更时更新此头部，然后检查 AGENTS.md" agents/roles/AGENTS.md agents/overlays/AGENTS.md agents/workflows/AGENTS.md
rg -q "ads-adaptive-operator.role.md" agents/roles/AGENTS.md
rg -q "jetpartners-ads-operator.overlay.md" agents/overlays/AGENTS.md
rg -q "jetpartners-ads-readonly-review.workflow.md" agents/workflows/AGENTS.md
! rg -n "Jetpartner|Eric|Benton|reports.30x.company/jetpartners|Contacted|Pre-Qualified|private aviation" agents/roles/ads-adaptive-operator.role.md
! rg -n "defines shared Role schema|defines Host Adapter Interface|requires concrete host adapter|requires Slack host" agents/roles/ads-adaptive-operator.role.md agents/overlays/jetpartners-ads-operator.overlay.md agents/workflows/jetpartners-ads-readonly-review.workflow.md
```

## Final Success Criteria

- Ads plan is domain-focused.
- Ads consumes shared protocol instead of defining it.
- Base Ads role is tenant-neutral.
- Jetpartner overlay contains tenant truth.
- Workflow is read-only/proposal-first unless approved.
- Approval receipts and tenant facts are source-backed, dated, and reviewable.
