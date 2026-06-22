# shared-agent-os-protocol - Work Plan

## TL;DR

**What you'll get:** 一套可复用 Agent OS 协议，供 Ads、Event、SEO、Lifecycle 等 role 消费。它只定义共同标准，不实现任何单个业务 agent。今天的两个消费者是 JP Ads Adaptive Agent 和 Caylent Event Adaptive Agent。

**Owner:** Shared architecture.

**Consumes:** `agent-roles-spec`, OMO agent design logic, GEB L1/L2/L3 doctrine.

**Produces:** Role schema, capability/MCP boundary, approval model, evidence contract, evidence gates, OMO governance, GEB semantic and structural delta, host adapter interface, agent onboarding contract, cross-role validation.

**Does not produce:** Ads role, Event role, tenant adapter runtime, Slack UX, Google Ads tools, HubSpot tools, tenant workflows, tenant memory.

## Responsibility Boundary

Shared architecture defines the protocol. Domain agents consume it.

```text
Shared Agent OS Protocol
  -> consumed by JP Ads Adaptive Agent
  -> consumed by Caylent Event Adaptive Agent
  -> consumed by future Marketing roles
```

Tenant adapter implementations are not the foundation. They are selected by tenant overlays.

## Scope In

- `agents/protocols/role-package.schema.md`
- `agents/protocols/capability-boundary.schema.md`
- `agents/protocols/host-adapter.interface.md`
- `agents/protocols/omo-execution-governance.md`
- `agents/protocols/geb-semantic-delta.md`
- `agents/protocols/agent-onboarding.contract.md`
- `agents/protocols/cross-role-validation.md`
- `agents/examples/jp-ads-role.fixture.md`
- `agents/examples/caylent-event-role.fixture.md`
- GEB L1/L2 docs for shared protocol directories.

## Scope Out

- No Ads role implementation.
- No Event role implementation.
- No MCP provider config.
- No package manager.
- No tenant adapter config.
- No Google Ads, HubSpot, Salesforce, CRM, or tenant-memory mutation.

## Agent Registry / Onboarding Contract

The protocol must make new marketing agents boring to add. JP Ads and Caylent Event are seed consumers, not the complete universe.

Every new domain agent must declare:

- `domain`: Ads, Event, SEO, Content, Lifecycle, Partner Ops, or another named marketing domain.
- `base_role`: reusable role file that contains no tenant truth.
- `tenant_overlay`: tenant-specific operating contract and source pointers.
- `workflow_contract`: typed workflow with inputs, outputs, evidence, approval gates, failure states, and readback.
- `capability_surface`: tools instantiated from shared permission modes.
- `host_adapters`: required, optional, preferred, unsupported, and notes.
- `evidence_contract`: source-backed artifacts, timestamps, actor, tenant/account binding, before/after readback, and approval receipt binding.
- `learning_route`: tenant memory, industry playbook, role patch, workflow patch, skill candidate, or protocol update.

Domain agents may instantiate shared protocol fields. They must not invent new protocol fields, permission modes, approval states, host kinds, or evidence semantics. New shared semantics require a shared protocol update first.

## Required Protocol Decisions

### Role Package Schema

The schema must define Role as a complete package:

- `identity`
- `purpose`
- `when_to_use`
- `inputs`
- `outputs`
- `role_instructions`
- `skills`
- `memory_scope`
- `tools`
- `plugins`
- `host_adapters`
- `capability_surface`
- `mcp_boundary`
- `permissions`
- `lifecycle`
- `evidence_contract`
- `approval_policy`
- `success_criteria`
- `non_goals`
- `learning_rules`
- `versioning`

`host_adapters` must be structured:

```yaml
host_adapters:
  required: []
  optional: []
  preferred: {}
  unsupported: []
  notes: ""
```

Domain roles may instantiate shared `evidence_contract`, `approval_policy`, `learning_rules`, and `capability_surface`; they must not introduce new protocol fields, permission modes, approval states, or host kinds. New shared semantics require a protocol update first.

### Capability / MCP Boundary

This protocol is host-neutral. It describes permission modes, not host-adapter behavior.

Modes:

- `read`
- `observe`
- `dry_run`
- `propose`
- `apply`

Each capability must declare:

- provider
- binding
- tenant/global scope
- allowed operations
- approval gate
- evidence/readback
- rollback or dry-run behavior

Protocol rule: `apply` is a capability state, not permission to mutate in this implementation pass. Any live mutation requires a role-level risk class, tenant/account binding, named human approver, approval receipt, pre-apply evidence, post-apply readback, and rollback or explicit irreversible-action acknowledgement. If any item is missing, execution must stop at `propose`.

### Host Adapter Interface

This protocol defines how external environments invoke a Role. It does not implement any adapter.

Host kinds:

- `slack`
- `cli`
- `portal`
- `cron`
- `api`
- `codex`

Required sections:

- entrypoints
- identity mapping
- session/thread model
- approval surface
- message/action payload contract
- evidence handoff
- capability restrictions
- failure behavior

### OMO Execution Governance

Define execution flow:

```text
trigger
  -> self-check
  -> plan
  -> delegate
  -> gather evidence
  -> execute read/dry-run/propose/apply by permission
  -> QA
  -> Metis/Momus review gate
  -> readback
```

### Evidence Gates

Every role and workflow must pass evidence gates before completion:

- request/brief evidence
- source evidence
- plan/proposal evidence
- approval evidence when risk requires it
- final readback evidence
- failure evidence for blocked or aborted actions

Evidence records must include `evidence_id`, `source_url`, `created_at`, `actor`, `tenant`, `account_or_campaign`, `before_state`, `after_state`, `approval_receipt`, and `readback_summary` when applicable.

### GEB Semantic and Structural Delta

GEB is not only learning. Every result must decide both semantic placement and structural documentation impact.

Learning deltas route to:

- tenant memory patch
- industry playbook patch
- role schema patch
- workflow patch
- skill patch
- new skill candidate
- protocol update

Structural deltas preserve L1/L2/L3 isomorphism for every created, moved, renamed, or responsibility-shifted artifact. Every code/doc structure change must preserve the map and terrain together.

## Cross-Role Validation

Create validation proving the shared protocol supports any domain role, with JP Ads and Caylent Event as seed examples.

Any domain role must share:

- role schema
- capability boundary
- approval model
- evidence contract
- OMO governance
- GEB delta

Domain roles may differ in:

- tools
- host adapters
- memory
- workflows
- approval risk classes

Seed examples:

- JP Ads Adaptive Agent proves Ads + Jetpartner tenant overlay.
- Caylent Event Adaptive Agent proves Event + HubSpot/Slack tenant overlay.

Acceptance:

```bash
for token in ads-adaptive-operator jetpartners-ads-operator event-adaptive-operator caylent-event-operator "shared schema" "domain-specific tools" "host-specific adapter"; do
  rg -q "$token" agents/protocols/cross-role-validation.md
done
```

Fixture schema validation:

```bash
for role in agents/examples/*-role.fixture.md; do
  rg -q "identity" "$role"
  rg -q "capability_surface" "$role"
  rg -q "host_adapters" "$role"
  rg -q "approval_policy" "$role"
done
```

## Todos

- [ ] 1. Create shared GEB docs for `agents/`, `agents/protocols/`, and `agents/examples/`.
- [ ] 2. Create `agents/protocols/role-package.schema.md` with structured `host_adapters`.
- [ ] 3. Create `agents/protocols/capability-boundary.schema.md` with host-neutral permission modes.
- [ ] 4. Create `agents/protocols/host-adapter.interface.md` without binding all roles to a concrete tenant adapter.
- [ ] 5. Create `agents/protocols/omo-execution-governance.md`.
- [ ] 6. Create `agents/protocols/geb-semantic-delta.md` as semantic and structural delta, not only learning routing.
- [ ] 7. Create `agents/protocols/agent-onboarding.contract.md`.
- [ ] 8. Create `agents/protocols/cross-role-validation.md`.
- [ ] 9. Create schema fixtures for JP Ads and Caylent Event examples.
- [ ] 10. Run fixture schema validation across `agents/examples/*-role.fixture.md`.
- [ ] 11. Verify shared GEB docs exist and carry `[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md`.

## Acceptance

```bash
test -f agents/AGENTS.md
test -f agents/protocols/AGENTS.md
test -f agents/examples/AGENTS.md
rg -q "\\[PROTOCOL\\]: 变更时更新此头部，然后检查 AGENTS.md" agents/AGENTS.md
rg -q "\\[PROTOCOL\\]: 变更时更新此头部，然后检查 AGENTS.md" agents/protocols/AGENTS.md
rg -q "\\[PROTOCOL\\]: 变更时更新此头部，然后检查 AGENTS.md" agents/examples/AGENTS.md
for file in role-package.schema.md capability-boundary.schema.md host-adapter.interface.md omo-execution-governance.md geb-semantic-delta.md agent-onboarding.contract.md cross-role-validation.md; do
  test -f "agents/protocols/$file"
done
for token in role_package evidence_gates host_neutrality workflow_contract post_run_delta final_readback; do
  rg -q "$token" agents/protocols/role-package.schema.md agents/protocols/omo-execution-governance.md agents/protocols/geb-semantic-delta.md agents/protocols/agent-onboarding.contract.md
done
```

## Final Success Criteria

- Shared protocol exists independently of Ads and Event.
- JP Ads and Caylent Event plans can cite shared protocol as input, not redefine it.
- New marketing agents can be added through `agent-onboarding.contract.md`, not new one-off protocol work.
- Concrete adapter choices appear only in tenant overlays.
- Capability boundary stays host-neutral.
- `apply` stays blocked at `propose` unless the full approval/evidence gate exists.
- GEB is signed off as both learning governance and L1/L2/L3 structural isomorphism.
- Cross-role validation proves shared protocol vs JP Ads / Caylent Event differences.
