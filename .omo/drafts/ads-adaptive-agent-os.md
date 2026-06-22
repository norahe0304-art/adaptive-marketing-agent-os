---
slug: ads-adaptive-agent-os
status: plan-written
intent: unclear
pending-action: none
approach: Build a narrow Ads Adaptive Agent OS plan. Use a reusable base Ads Agent skeleton, mount Jetpartner as the first tenant overlay, reuse 30x-ads as the deterministic domain engine, map OMO to execution governance, use GEB L1-L3 for agent documentation, and treat Record & Replay as a gated skill-factory mechanism.
---

# Draft: ads-adaptive-agent-os

## Components (topology ledger)
| id | outcome | status | evidence path |
| --- | --- | --- | --- |
| base-ads-agent | Reusable Ads Agent skeleton separate from tenant facts. | active | /Users/nora/.codex/skills/ads/SKILL.md:8 |
| domain-engine | 30x-ads remains deterministic Google Ads engine and report surface. | active | /Users/nora/30x-ads/README.md:6 |
| role-package | Existing Jetpartner role package provides first concrete role boundary. | active | /Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:1 |
| tenant-overlay | Jetpartner mounts as context overlay, not base-agent knowledge. | active | /Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md:5 |
| typed-workflow | Flyte-style typed DAG is schema-only in v0. | active | https://flyteorg-flyte.mintlify.app/key-concepts |
| omo-governance | OMO roles provide plan/delegate/evidence/QA/gate discipline. | active | /Users/nora/.codex/agents/explorer.toml |
| geb-docs | GEB L1-L3 documents the Ads Agent skeleton, module maps, and unit contracts. | active | /Users/nora/30x-ads/AGENTS.md:1 |
| skill-factory | Record & Replay produces skill candidates after replay/redaction, not auto-installed skills. | active | https://developers.openai.com/codex/record-and-replay |

## Open assumptions (announced defaults)
| assumption | adopted default | rationale | reversible? |
| --- | --- | --- | --- |
| Scope | Ads Adaptive Agent OS, not broad Marketing OS. | User corrected that Ads Agent is first and tenant should not bloat L1-L3. | yes |
| v0 runtime | Schema/runbook/docs only; no new queue, DB, dashboard, or Flyte deployment. | 30x-ads already has engine and report surface. | yes |
| Flyte | Borrow typed task/workflow/launch-plan concepts only. | Running Flyte/Kubernetes is overkill for v0. | yes |
| Tenant | Jetpartner is overlay; base agent stays generic. | Needed for scale across future clients. | yes |
| Record & Replay | Candidate skill factory only after verified replay. | Prevents skill explosion and unsafe auto-learning. | yes |
| Live data | Default to existing artifacts; live commands require explicit authorization. | Avoids credential/PII exposure. | yes |
| SEO | Optional future signal, not v0 acceptance. | User asked Ads Agent first. | yes |

## Findings (cited - path:lines)
- `/Users/nora/.codex/skills/ads/SKILL.md:8` - global ads skill is the natural-language entry point and router.
- `/Users/nora/.codex/skills/ads/SKILL.md:23` - ads skill routes user intents into specialized capabilities.
- `/Users/nora/30x-ads/README.md:6` - 30x-ads is already the multi-tenant Google Ads engine; it explicitly avoids a new dashboard/orchestrator.
- `/Users/nora/30x-ads/README.md:10` - observe writes per-tenant report artifacts.
- `/Users/nora/30x-ads/README.md:20` - apply defaults to dry-run unless `--apply` is used.
- `/Users/nora/30x-ads/AGENTS.md:5` - existing GEB-style project map lists source directories and boundaries.
- `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:1` - Jetpartner role uses `agent-role/preview-0.1`.
- `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:22` - role forbids auto-apply without human approval.
- `/Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md:5` - Jetpartner optimization truth is qualified lead, not raw lead volume.
- `/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:40` - Jetpartner role defaults to read-only audit and recommendation.
- OpenAI Record & Replay docs - demonstrated workflows can be drafted into reusable skills.
- Flyte docs - tasks/workflows/launch plans provide typed workflow abstractions.
- Librarian evidence - agent-roles-spec, Flyte, Trellis, LazyCodex/OMO, and agency-agents each contribute one bounded design idea.
- Metis evidence - previous broad Marketing OS plan was over-scoped and must be narrowed.

## Decisions (with rationale)
- The base object is `Ads Adaptive Agent OS`, not `Marketing Adaptive Agent OS`.
- GEB L1-L3 describes the reusable Ads Agent skeleton, not all tenants.
- Jetpartner is the first runtime overlay and v0 proof case.
- 30x-ads remains the domain engine; the OS should not reimplement Google Ads API logic.
- v0 is read-only by default and stops at proposal/approval/semantic delta.
- Record & Replay produces candidate skills; registry admission requires replay and redaction.
- Flyte is conceptual only in v0; typed JSON schemas are enough.

## Scope IN
- Evidence baseline.
- GEB L1-L3 Ads Agent skeleton contract.
- Capability registry with source-priority rules.
- Tenant overlay contract.
- Typed workflow and semantic-delta schemas with valid/invalid samples.
- Jetpartner Ads read-only v0 runbook.
- OMO governance map.
- Skill-factory gate.
- Privacy/redaction/evidence policy.
- Integration blueprint.

## Scope OUT (Must NOT have)
- New dashboard.
- Google Ads or Supabase mutation.
- Flyte/Kubernetes deployment.
- New database or queue.
- SEO as v0 mainline.
- Multi-tenant marketplace.
- Auto-installing generated skills.
- Storing credentials, tokens, raw tenant exports, or PII in docs/evidence.

## Open questions
- None blocking for plan generation. Execution can proceed with adopted defaults above.

## Approval gate
status: plan-written
Plan file: `.omo/plans/ads-adaptive-agent-os.md`
Approval already implied by the user's direct request to use `ulw-plan` to plan this goal. Approval authorizes planning only, not implementation.
