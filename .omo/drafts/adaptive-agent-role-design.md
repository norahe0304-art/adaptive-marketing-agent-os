---
slug: adaptive-agent-role-design
status: first-artifacts-written
intent: clear
pending-action: review produced protocol, role, overlay, and workflow artifacts under agents/
approach: Split the previous mixed plan into shared architecture, Ads role design, and Event role design so domain agents consume the Agent OS protocol instead of owning it.
---

# Draft: adaptive-agent-role-design split

## Components (topology ledger)

| id | outcome | status | evidence path |
| --- | --- | --- | --- |
| C1 | Shared Agent OS protocol plan owns Role schema, capability boundary, host adapter interface, OMO governance, GEB semantic delta, and cross-role validation. | active | .omo/plans/shared-agent-os-protocol.md |
| C2 | Ads role plan owns JP Ads Adaptive Agent: `ads-adaptive-operator`, Jetpartner overlay, Ads read-only workflow, and Ads-specific evidence/approval/learning. | active | .omo/plans/ads-agent-role-design.md |
| C3 | Event role plan owns Caylent Event Adaptive Agent: `event-adaptive-operator`, Caylent overlay, HubSpot launch workflow, Slack/Hermes host use, campaign evidence, and approval audit. | active | .omo/plans/event-agent-role-design.md |
| C4 | Routing index keeps old `adaptive-agent-role-design.md` references from misleading execution. | active | .omo/plans/adaptive-agent-role-design.md |
| C5 | OMO review gate records Explorer/Librarian/Metis/Momus findings and applied hardening changes. | active | .omo/plans/adaptive-agent-omo-review-summary.md |
| C6 | Generic marketing agent onboarding contract prevents the platform from becoming a two-agent system. | active | .omo/plans/shared-agent-os-protocol.md |

## Open assumptions (announced defaults)

| assumption | adopted default | rationale | reversible? |
| --- | --- | --- | --- |
| Runtime scope | Design docs and role package files only; no package manager/runtime implementation. | The user wants to lock strategy before implementation. | Yes |
| Directory shape | Create `agents/` as product-owned Agent OS protocol surface, with GEB `AGENTS.md` at root and module levels. | Keeps role design separate from `.omo` planning artifacts and global Codex config. | Yes |
| Shared ownership | Shared architecture owns Agent OS protocol. | Ads/Event agents should not invent the operating system while doing domain work. | Yes |
| Ads ownership | Ads agent only owns Ads role, Jetpartner overlay, and Ads workflows. | Keeps Google Ads / lead-quality decisions with the Ads domain. | Yes |
| Event ownership | Event agent only owns Event role, Caylent overlay, and HubSpot/Slack workflow. | Keeps HubSpot/Slack implementation separate from shared schema. | Yes |
| Tool boundary | Declare MCP/capability manifests as docs/contracts only. | Avoids exposing global MCP tools before protocol sign-off. | Yes |
| Learning | Session Distillation first; Record & Replay only for stable repeatable workflow candidates. | Most useful learning happens inside interactive sessions before it becomes replayable automation. | Yes |
| GEB scope | GEB is semantic and structural delta, not only learning promotion. | The system must preserve L1/L2/L3 isomorphism while deciding where knowledge goes. | No |
| Apply scope | `apply` is a capability state, not permission for live mutation in v1. | Live marketing actions need risk class, human approver, evidence packet, readback, and rollback/irreversible acknowledgement. | Yes |

## Findings (cited)

- `agent-roles-spec` defines Role as a complete professional agent role, not just prompt/skill, and includes instructions, skills, memory, tools, plugins, host adapters, lifecycle rules: https://github.com/SeemSeam/agent-roles-spec/blob/main/docs/i18n/README.zh-CN.md
- `agent-roles-spec` also calls out host adapters and role-scoped tool/MCP surfaces as part of role portability: https://github.com/SeemSeam/agent-roles-spec/blob/main/docs/i18n/README.zh-CN.md
- OMO `explorer` role is read-only, trigger-scoped, output-shaped, and has explicit tool strategy and success criteria: `/Users/nora/.codex/agents/explorer.toml:1-75`.
- OMO `plan` role is planner-only, refuses implementation, and requires executable plan tasks with references, acceptance, QA, and commit instructions: `/Users/nora/.codex/agents/plan.toml:1-130`.
- OMO `metis` and `momus` show the critic/reviewer pattern: detect contradictions and verify plan executability before work starts: `/Users/nora/.codex/agents/metis.toml:1-64`, `/Users/nora/.codex/agents/momus.toml:1-68`.
- Existing Jetpartner role package has `schema`, `id`, `identity`, `contents`, and `permissions`, including human confirmation for mutations: `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:1-45`.
- Existing Jetpartner memory locks qualified lead truth and read-only audit first: `/Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md:1-68`.
- Existing Jetpartner skill has activation, workflow, human approval gate, readback surfaces, and qualified lead rule: `/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:1-104`.
- Existing 30x role docs already use GEB L2 `AGENTS.md` module maps and `[PROTOCOL]` lines: `/Users/nora/30x-ads/roles/AGENTS.md:1-10`, `/Users/nora/30x-ads/roles/jetpartners-ads-operator/AGENTS.md:1-15`.
- Current sign-off HTML already states Truth/Work/Learning layers and has role/MCP boundary fields: `.omo/plans/adaptive-agent-os-ads-first-signoff.zh-CN.html:176-220`, `.omo/plans/adaptive-agent-os-ads-first-signoff.zh-CN.html:304-370`.
- User correction supplied on 2026-06-21 tightened the structural issue: Ads agent should not be responsible for Agent OS protocol. Shared protocol must be its own architecture plan; JP Ads and Caylent Event consume it.
- User clarified the day-one outputs: one Ad Adaptive Agent for JP and one Event Adaptive Agent for Caylent.
- OMO family review found the plan direction correct but required ITERATE: add generic onboarding, harden apply/evidence/overlay/GEB boundaries, and make acceptance checks token-complete.

## Decisions (with rationale)

- Split plans by owner: shared architecture, Ads agent, Event agent.
- Use three shared protocol layers: Role Package Protocol, Execution Governance, Learning/GEB. This avoids L1-L6 overdesign while preserving GEB L1/L2/L3.
- Treat MCP/tool surfaces as explicit role fields, not hidden runtime state.
- Make `host_adapters` a structured schema field with required, optional, preferred, unsupported, and notes.
- Keep Hermes as optional host adapter implementation, not universal OS core.
- Keep base role, tenant overlay, and industry/domain workflow separate so Jetpartner does not pollute the base Ads agent.
- Put Caylent Event Adaptive Agent in its own Event plan, not inside Ads plan.
- Validate role files directly with schema checks, not only by grepping protocol docs.
- Validate shared fixtures in the shared plan; validate real role files only in domain or final integration plans.
- Treat Flyte as a typed workflow contract inspiration, not an adopted runtime.
- Treat GEB semantic delta as our extension layer and explicitly include structural L1/L2/L3 document isomorphism.

## Scope IN

- Shared architecture plan: protocol schemas and validation.
- Ads plan: Ads role, Jetpartner overlay, Ads workflow.
- Event plan: Event role, Caylent overlay, HubSpot/Slack workflow.
- Routing index: old mixed plan points to the right owner-specific plan.
- OMO review summary: four-agent review findings and applied changes.

## Scope OUT (Must NOT have)

- Ads plan does not define shared protocol.
- Event plan does not define shared protocol.
- Shared plan does not implement Ads or Event business workflows.
- No runtime package manager, MCP config mutation, Hermes-as-core assumption, or unapproved platform mutation.
- No live `apply` in v1 without a separate runtime/security approval design.

## Open questions

None blocking. Defaults are reversible and surfaced above.

## Approval gate

status: first-artifacts-written
next: user reviews the produced artifacts under `agents/protocols/`, `agents/roles/`, `agents/overlays/`, and `agents/workflows/`.
