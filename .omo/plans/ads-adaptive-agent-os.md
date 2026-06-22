# ads-adaptive-agent-os - Work Plan

> Superseded on 2026-06-21.
> This was an earlier Ads-first draft. The active strategy is now split into:
> - `.omo/plans/shared-agent-os-protocol.md` for the reusable Adaptive Agent OS protocol.
> - `.omo/plans/ads-agent-role-design.md` for JP Ads as a domain consumer.
> - `.omo/plans/event-agent-role-design.md` for Caylent Event as a second domain consumer.
> Do not execute this file as the current strategy.

## TL;DR (For humans)
**What you'll get:** A narrow Ads Adaptive Agent OS plan, not another broad Marketing OS plan. It defines a reusable Ads Agent skeleton, mounts Jetpartner as the first tenant overlay, and uses existing 30x-ads execution instead of inventing a new runtime.

**Why this approach:** The reusable agent must stay separate from tenant facts, or it will not scale. The first proof should be Jetpartner Ads read-only review because it already has a real engine, role package, qualified-lead truth, approval gate, and report surface.

**What it will NOT do:** It will not build a dashboard, auto-mutate Google Ads, make SEO a v0 requirement, or install generated skills without replay verification.

**Effort:** Large
**Risk:** Medium - the design spans role packages, workflow contracts, execution governance, evidence, and learning loops, but v0 stays documentation/schema/runbook-first.
**Decisions I made for you:** Treat this as an open-ended architecture request; adopt schema-only Flyte-style workflows for v0; keep GEB L1-L3 scoped to the Ads Agent skeleton; use Jetpartner only as runtime overlay; use Record & Replay only for candidate skill generation until replay passes; default live external reads to existing artifacts unless the user explicitly authorizes credentials-backed commands.

Your next move: approve this plan for execution with `$start-work`, or ask for a high-accuracy Momus review first. Full execution detail follows below.

---

> TL;DR (machine): Large/Medium; deliver an Ads Adaptive Agent OS skeleton plan with GEB L1-L3, role-package contract, typed workflow schemas, Jetpartner v0 runbook, OMO evidence gates, and skill-factory governance.

## Scope
### Must have
- Reframe the target as `Ads Adaptive Agent OS`, not `Marketing Adaptive Agent OS`.
- Build the reusable base around `/Users/nora/.codex/skills/ads` as the generic Ads capability system; this is supported by its natural-language router and specialized sub-skill/worker routing at `/Users/nora/.codex/skills/ads/SKILL.md:8` and `/Users/nora/.codex/skills/ads/SKILL.md:23`.
- Keep `30x-ads` as the deterministic domain engine. It already defines a 3-step per-tenant flow: `pnpm observe`, agent proposal, and `pnpm apply --blueprint` dry-run/apply at `/Users/nora/30x-ads/README.md:8`.
- Use Jetpartner only as the first tenant overlay, not as the base agent. Existing tenant truth lives in `/Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md:5`.
- Preserve human approval for all Google Ads/Supabase mutation. The role package forbids auto-apply at `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:22`, and the skill requires explicit confirmation at `/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:40`.
- Define GEB L1-L3 only for the Ads Agent skeleton:
  - L1: Ads Adaptive Agent constitution.
  - L2: reusable module maps such as search-term review, lead-quality review, budget review.
  - L3: skill/workflow contracts with input, output, position, approval, evidence, and learning-delta rules.
- Define tenant overlays as runtime context: `tenant_truth`, `tenant_memory`, `permissions`, `approved_examples`, and `launchplans`; do not copy tenant content into the base agent.
- Use Flyte only as an abstraction source for typed task/workflow/launch-plan ideas. Do not deploy Flyte in v0. Flyte docs define tasks as strongly typed, versioned compute units and workflows as DAGs; launch plans bind inputs/schedules.
- Use agent-roles-spec as the role package mental model: role definition, memory, skills, tools, host adapters, lifecycle.
- Use OMO/LazyCodex as execution governance: planner, executor, QA, reviewer, evidence, and gate, not as the Ads domain engine.
- Use Trellis as inspiration for persisted workflow/spec/task/workspace learning loops.
- Use agency-agents only as catalog inspiration for clear deliverables, success metrics, and multi-host conversion; do not import 232 agents into v0.
- Use Codex Record & Replay only for workflows that are repetitive, stable, and have clear success criteria. Official OpenAI docs say Record & Replay drafts a reusable skill after observing a workflow; v0 must keep generated skills as candidates until replay and redaction pass.
- Produce executable artifacts: docs, schemas, sample instances, runbooks, and verification commands. The worker should be able to execute without re-interviewing the user.

### Must NOT have (guardrails, anti-slop, scope boundaries)
- Must not build a new dashboard or product UI in v0. 30x-ads already says the agent is the control plane and not a dashboard at `/Users/nora/30x-ads/README.md:6`.
- Must not make SEO required for v0. 30x SEO can remain a future capability extension or optional signal.
- Must not read `.env`, OAuth tokens, raw credentials, or tenant exports as evidence.
- Must not run Google Ads or Supabase mutations without explicit current-task confirmation.
- Must not make every session create a new skill. Every session creates a learning delta; only stable, replayable deltas can become skill drafts.
- Must not store tenant-specific private aviation rules inside the base Ads Agent except as examples.
- Must not introduce Flyte, Kubernetes, a new queue, or a new database in v0.
- Must not rely on grep-only acceptance for schemas; every schema must validate a good sample and reject a bad sample.

## Verification strategy
> Zero human intervention - all verification is agent-executed.
- Test decision: tests-after + schema validation + markdown contract checks. No production code behavior change is planned for v0.
- Evidence: `.omo/evidence/task-<N>-ads-adaptive-agent-os.<ext>`
- Real-surface proof: for v0, the faithful surface is CLI/filesystem artifacts: existing 30x-ads reports, dry-run commands, schema validators, and generated plan/runbook files. Browser QA is only needed if a task explicitly touches the existing report URL or generated `monitor.html`.
- Security proof: every evidence artifact must pass secret/PII grep checks.
- Review proof: final verification must include plan compliance, scope fidelity, schema sample validation, and a Jetpartner read-only dry-run/readback scenario.

## Execution strategy
### Parallel execution waves
> Target 5-8 todos per wave. Fewer than 3 (except the final) means you under-split.

Wave 1 (no dependencies):
- Todo 1: Evidence baseline and repo boundaries.
- Todo 2: Ads Agent GEB L1-L3 skeleton contract.
- Todo 3: Capability and source-priority registry.
- Todo 4: Tenant overlay contract.
- Todo 5: Typed workflow and semantic-delta schemas.

Wave 2 (after Wave 1):
- Todo 6: Jetpartner Ads v0 read-only runbook.
- Todo 7: OMO execution governance mapping.
- Todo 8: Record & Replay skill-factory gate.
- Todo 9: Privacy, redaction, and evidence rules.

Wave 3 (after Wave 2):
- Todo 10: Integration blueprint and handoff package.
- Todo 11: Final verification wave.

Critical path: Todo 1 -> Todo 2 -> Todo 5 -> Todo 6 -> Todo 10 -> Todo 11

### Dependency matrix
| Todo | Depends on | Blocks | Can parallelize with |
| --- | --- | --- | --- |
| 1 | none | 6, 9, 10 | 2, 3, 4, 5 |
| 2 | none | 6, 7, 10 | 1, 3, 4, 5 |
| 3 | none | 6, 8, 10 | 1, 2, 4, 5 |
| 4 | none | 6, 9, 10 | 1, 2, 3, 5 |
| 5 | none | 6, 8, 9, 10 | 1, 2, 3, 4 |
| 6 | 1, 2, 3, 4, 5 | 10, 11 | 7, 8, 9 |
| 7 | 2, 5 | 10, 11 | 6, 8, 9 |
| 8 | 3, 5 | 10, 11 | 6, 7, 9 |
| 9 | 1, 4, 5 | 10, 11 | 6, 7, 8 |
| 10 | 6, 7, 8, 9 | 11 | none |
| 11 | 10 | final | none |

## Todos
> Implementation + Test = ONE todo. Never separate.

- [ ] 1. Evidence baseline and boundary audit
  What to do / Must NOT do: Create `docs/research/ads-adaptive-agent-os-evidence.md`. Capture verified local and external evidence for: base Ads skill, 30x-ads engine, Jetpartner role package, tenant overlay, OMO agents, GEB docs, Flyte, agent-roles-spec, Trellis, agency-agents, Codex Record & Replay. Include source family, path or URL, one-line claim, and whether it is v0 requirement or later inspiration. Must not read credentials, `.env`, raw tenant exports, or stale chat logs as evidence.
  Parallelization: Wave 1 | Blocked by: none | Blocks: 6, 9, 10
  References (executor has NO interview context - be exhaustive):
  - `/Users/nora/.codex/skills/ads/SKILL.md:8` - base Ads skill routes natural-language ad tasks.
  - `/Users/nora/30x-ads/README.md:6` - 30x-ads is the multi-tenant Google Ads engine and avoids a new dashboard/orchestrator.
  - `/Users/nora/30x-ads/README.md:64` - 30x-ads command surface.
  - `/Users/nora/30x-ads/AGENTS.md:5` - 30x-ads GEB L1 project map.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:1` - role package schema marker.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md:5` - qualified lead truth.
  - `https://developers.openai.com/codex/record-and-replay` - Record & Replay turns a demonstrated workflow into a reusable skill.
  - `https://developers.openai.com/codex/concepts/customization` - AGENTS, memories, skills, MCP, and subagents are complementary.
  Acceptance criteria (agent-executable):
  - [ ] `test -f docs/research/ads-adaptive-agent-os-evidence.md`
  - [ ] `rg -n "Base Ads Agent|30x-ads|Jetpartner|GEB|OMO|Flyte|agent-roles-spec|Trellis|agency-agents|Record & Replay" docs/research/ads-adaptive-agent-os-evidence.md`
  - [ ] `rg -n "v0 requirement|later inspiration|source family" docs/research/ads-adaptive-agent-os-evidence.md`
  QA scenarios (name the exact tool + invocation):
  ```
  Scenario: evidence baseline covers all source families
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "Base Ads Agent|30x-ads|Jetpartner|GEB|OMO|Flyte|agent-roles-spec|Trellis|agency-agents|Record & Replay" docs/research/ads-adaptive-agent-os-evidence.md | tee .omo/evidence/task-1-ads-adaptive-agent-os.txt
    Expected: command exits 0 and prints every required source family.
    Evidence: .omo/evidence/task-1-ads-adaptive-agent-os.txt

  Scenario: evidence baseline excludes secrets
    Tool:     bash
    Steps:    bash -lc 'if rg -n "(refresh_token\\s*=|client_secret\\s*=|access_token\\s*=|Authorization:\\s*|Bearer\\s+[A-Za-z0-9._-]+|google_ads_refresh_token\\s*=)" docs/research/ads-adaptive-agent-os-evidence.md; then exit 1; else echo "PASS no secret value patterns" | tee .omo/evidence/task-1-ads-adaptive-agent-os-error.txt; fi'
    Expected: command exits 0 because no secret value pattern is present.
    Evidence: .omo/evidence/task-1-ads-adaptive-agent-os-error.txt
  ```
  Commit: Y | docs(research): establish ads adaptive agent evidence baseline

- [ ] 2. Ads Agent GEB L1-L3 skeleton contract
  What to do / Must NOT do: Create `docs/architecture/geb-l1-l3-ads-agent.md`. Define GEB L1/L2/L3 for the reusable Ads Adaptive Agent only: L1 constitution, L2 module maps, L3 unit contracts. State explicitly that tenants are overlays, not part of the base skeleton. Include a proposed future tree for `agents/ads-adaptive-agent/` without creating the tree unless this todo is explicitly scoped to scaffold. Must not put Jetpartner-specific rules into L1 except as examples.
  Parallelization: Wave 1 | Blocked by: none | Blocks: 6, 7, 10
  References:
  - `/Users/nora/30x-ads/AGENTS.md:1` - existing project constitution style.
  - `/Users/nora/30x-ads/roles/AGENTS.md` - role-layer L2 map pattern.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/AGENTS.md` - local role package map pattern.
  - `/Users/nora/.codex/skills/ads/AGENTS.md` - base ads skill map discovered by explorer.
  - OpenAI AGENTS guidance: `https://developers.openai.com/codex/guides/agents-md`
  Acceptance criteria:
  - [ ] `test -f docs/architecture/geb-l1-l3-ads-agent.md`
  - [ ] `rg -n "L1.*Ads Adaptive Agent|L2.*module|L3.*contract|tenant overlay|not tenant warehouse" docs/architecture/geb-l1-l3-ads-agent.md`
  - [ ] `rg -n "\\[PROTOCOL\\]: 变更时更新此头部，然后检查 AGENTS.md" docs/architecture/geb-l1-l3-ads-agent.md`
  QA scenarios:
  ```
  Scenario: GEB skeleton separates agent and tenant
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "tenant overlay|not tenant warehouse|Base Ads Agent|Jetpartner.*example" docs/architecture/geb-l1-l3-ads-agent.md | tee .omo/evidence/task-2-ads-adaptive-agent-os.txt
    Expected: command exits 0 and proves the base agent is separated from tenant overlays.
    Evidence: .omo/evidence/task-2-ads-adaptive-agent-os.txt

  Scenario: GEB protocol phrase is present
    Tool:     bash
    Steps:    rg -n "\\[PROTOCOL\\]: 变更时更新此头部，然后检查 AGENTS.md" docs/architecture/geb-l1-l3-ads-agent.md | tee .omo/evidence/task-2-ads-adaptive-agent-os-error.txt
    Expected: command exits 0 and prints the fixed GEB protocol phrase.
    Evidence: .omo/evidence/task-2-ads-adaptive-agent-os-error.txt
  ```
  Commit: Y | docs(architecture): define ads agent geb skeleton

- [ ] 3. Capability registry and source-priority contract
  What to do / Must NOT do: Create `docs/capabilities/ads-capability-registry.md`, `docs/capabilities/ads-capability.schema.json`, `docs/capabilities/examples/ads-capability.valid.json`, and `docs/capabilities/examples/ads-capability.invalid.json`. Define capability fields: `id`, `kind`, `trigger`, `inputs`, `outputs`, `side_effects`, `approval_gate`, `evidence_required`, `source_priority`, `source_ref`, `version`. Establish source priority: project-local Jetpartner role package > 30x-ads repo skills/scripts > global ads skills > SEO skills as optional future signal. Must not copy full skill bodies.
  Parallelization: Wave 1 | Blocked by: none | Blocks: 6, 8, 10
  References:
  - `/Users/nora/.codex/skills/ads/SKILL.md:23` - router table for global ads capabilities.
  - `/Users/nora/.codex/skills/ads/SKILL.md:70` - orchestration logic and subagent delegation.
  - `/Users/nora/30x-ads/README.md:90` - deterministic engine directories.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:20` - Jetpartner workflow rules.
  Acceptance criteria:
  - [ ] `test -f docs/capabilities/ads-capability-registry.md`
  - [ ] `test -f docs/capabilities/ads-capability.schema.json`
  - [ ] `test -f docs/capabilities/examples/ads-capability.valid.json`
  - [ ] `test -f docs/capabilities/examples/ads-capability.invalid.json`
  - [ ] `python3 -m json.tool docs/capabilities/ads-capability.schema.json >/tmp/ads-capability.schema.json`
  - [ ] `npx --yes ajv-cli@5 validate -s docs/capabilities/ads-capability.schema.json -d docs/capabilities/examples/ads-capability.valid.json`
  - [ ] `bash -lc 'if npx --yes ajv-cli@5 validate -s docs/capabilities/ads-capability.schema.json -d docs/capabilities/examples/ads-capability.invalid.json; then exit 1; else echo "PASS invalid capability rejected"; fi'`
  - [ ] `rg -n "source_priority|project-local|30x-ads repo|global ads skills|optional future signal" docs/capabilities/ads-capability-registry.md`
  QA scenarios:
  ```
  Scenario: capability schema is valid and requires source_ref
    Tool:     bash
    Steps:    bash -lc 'mkdir -p .omo/evidence && python3 -m json.tool docs/capabilities/ads-capability.schema.json > .omo/evidence/task-3-ads-adaptive-agent-os.txt && npx --yes ajv-cli@5 validate -s docs/capabilities/ads-capability.schema.json -d docs/capabilities/examples/ads-capability.valid.json && if npx --yes ajv-cli@5 validate -s docs/capabilities/ads-capability.schema.json -d docs/capabilities/examples/ads-capability.invalid.json; then exit 1; fi && rg -n "\"source_ref\"|\"required\"" docs/capabilities/ads-capability.schema.json'
    Expected: command exits 0; valid capability sample passes, invalid capability sample fails, and schema declares source_ref/required.
    Evidence: .omo/evidence/task-3-ads-adaptive-agent-os.txt

  Scenario: registry blocks SEO from v0 mainline
    Tool:     bash
    Steps:    rg -n "SEO.*optional future signal|not.*v0 mainline|v0.*Ads only" docs/capabilities/ads-capability-registry.md | tee .omo/evidence/task-3-ads-adaptive-agent-os-error.txt
    Expected: command exits 0 and proves SEO is not a v0 requirement.
    Evidence: .omo/evidence/task-3-ads-adaptive-agent-os-error.txt
  ```
  Commit: Y | docs(capabilities): define ads capability registry

- [ ] 4. Tenant overlay contract
  What to do / Must NOT do: Create `docs/tenants/tenant-overlay-contract.md`, `docs/tenants/tenant-overlay.schema.json`, `docs/tenants/examples/jetpartner-overlay.valid.json`, and `docs/tenants/examples/jetpartner-overlay.invalid.json`. Define runtime overlay fields: `tenant_id`, `business_truth`, `industry_overlay_refs`, `role_package_ref`, `permissions`, `data_freshness_policy`, `report_artifact_refs`, `approved_examples`, `mutation_policy`, `pii_policy`. Use Jetpartner as one sample, referencing qualified lead truth and private aviation bad-intent rules without baking them into base Ads Agent. Must not duplicate engine code or store secrets.
  Parallelization: Wave 1 | Blocked by: none | Blocks: 6, 9, 10
  References:
  - `/Users/nora/30x-ads/README.md:129` - tenants directory stores per-client config and reports.
  - `/Users/nora/30x-ads/AGENTS.md:9` - tenant data stays local and gitignored.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md:31` - Jetpartner bad-intent examples.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:36` - role permissions.
  Acceptance criteria:
  - [ ] `test -f docs/tenants/tenant-overlay-contract.md`
  - [ ] `test -f docs/tenants/tenant-overlay.schema.json`
  - [ ] `test -f docs/tenants/examples/jetpartner-overlay.valid.json`
  - [ ] `test -f docs/tenants/examples/jetpartner-overlay.invalid.json`
  - [ ] `python3 -m json.tool docs/tenants/tenant-overlay.schema.json >/tmp/tenant-overlay.schema.json`
  - [ ] `npx --yes ajv-cli@5 validate -s docs/tenants/tenant-overlay.schema.json -d docs/tenants/examples/jetpartner-overlay.valid.json`
  - [ ] `bash -lc 'if npx --yes ajv-cli@5 validate -s docs/tenants/tenant-overlay.schema.json -d docs/tenants/examples/jetpartner-overlay.invalid.json; then exit 1; else echo "PASS invalid tenant overlay rejected"; fi'`
  - [ ] `rg -n "tenant_id|business_truth|permissions|data_freshness_policy|mutation_policy|pii_policy|Jetpartner" docs/tenants/tenant-overlay-contract.md`
  QA scenarios:
  ```
  Scenario: tenant overlay schema is valid
    Tool:     bash
    Steps:    bash -lc 'mkdir -p .omo/evidence && python3 -m json.tool docs/tenants/tenant-overlay.schema.json > .omo/evidence/task-4-ads-adaptive-agent-os.txt && npx --yes ajv-cli@5 validate -s docs/tenants/tenant-overlay.schema.json -d docs/tenants/examples/jetpartner-overlay.valid.json && if npx --yes ajv-cli@5 validate -s docs/tenants/tenant-overlay.schema.json -d docs/tenants/examples/jetpartner-overlay.invalid.json; then exit 1; fi'
    Expected: command exits 0; valid tenant overlay sample passes and invalid tenant overlay sample fails.
    Evidence: .omo/evidence/task-4-ads-adaptive-agent-os.txt

  Scenario: tenant contract forbids secrets
    Tool:     bash
    Steps:    rg -n "Must not.*secret|must not.*credential|\\.env.*not|gitignored" docs/tenants/tenant-overlay-contract.md | tee .omo/evidence/task-4-ads-adaptive-agent-os-error.txt
    Expected: command exits 0 and prints explicit secret exclusion.
    Evidence: .omo/evidence/task-4-ads-adaptive-agent-os-error.txt
  ```
  Commit: Y | docs(tenants): define ads tenant overlay contract

- [ ] 5. Typed workflow and semantic-delta schemas
  What to do / Must NOT do: Create `docs/workflows/ads-workflow.schema.json`, `docs/workflows/semantic-delta.schema.json`, `docs/workflows/examples/jetpartner-search-term-review.workflow.valid.json`, `docs/workflows/examples/jetpartner-search-term-review.workflow.invalid.json`, `docs/workflows/examples/jetpartner-search-term-review.delta.valid.json`, and `docs/workflows/examples/jetpartner-search-term-review.delta.invalid.json`. Model Flyte-inspired typed steps without introducing Flyte runtime. Required workflow concepts: task id, typed inputs/outputs, dependencies, side effects, approval gate, evidence path. Required delta concepts: observed action, machine artifacts, semantic artifacts, approval state, QA evidence, learning classification, skill candidate, replay status, rollback plan. Must not make delta a free-text journal.
  Parallelization: Wave 1 | Blocked by: none | Blocks: 6, 8, 9, 10
  References:
  - Flyte task/workflow/launch-plan docs: `https://flyteorg-flyte.mintlify.app/key-concepts`
  - `/Users/nora/30x-ads/README.md:20` - apply dry-run/apply as side-effect boundary.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:44` - post-mutation readback surfaces.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md:21` - live-check requirement.
  Acceptance criteria:
  - [ ] `test -f docs/workflows/ads-workflow.schema.json`
  - [ ] `test -f docs/workflows/semantic-delta.schema.json`
  - [ ] `test -f docs/workflows/examples/jetpartner-search-term-review.workflow.valid.json`
  - [ ] `test -f docs/workflows/examples/jetpartner-search-term-review.workflow.invalid.json`
  - [ ] `test -f docs/workflows/examples/jetpartner-search-term-review.delta.valid.json`
  - [ ] `test -f docs/workflows/examples/jetpartner-search-term-review.delta.invalid.json`
  - [ ] `python3 -m json.tool docs/workflows/ads-workflow.schema.json >/tmp/ads-workflow.schema.json`
  - [ ] `python3 -m json.tool docs/workflows/semantic-delta.schema.json >/tmp/semantic-delta.schema.json`
  - [ ] `npx --yes ajv-cli@5 validate -s docs/workflows/ads-workflow.schema.json -d docs/workflows/examples/jetpartner-search-term-review.workflow.valid.json`
  - [ ] `bash -lc 'if npx --yes ajv-cli@5 validate -s docs/workflows/ads-workflow.schema.json -d docs/workflows/examples/jetpartner-search-term-review.workflow.invalid.json; then exit 1; else echo "PASS invalid workflow rejected"; fi'`
  - [ ] `npx --yes ajv-cli@5 validate -s docs/workflows/semantic-delta.schema.json -d docs/workflows/examples/jetpartner-search-term-review.delta.valid.json`
  - [ ] `bash -lc 'if npx --yes ajv-cli@5 validate -s docs/workflows/semantic-delta.schema.json -d docs/workflows/examples/jetpartner-search-term-review.delta.invalid.json; then exit 1; else echo "PASS invalid delta rejected"; fi'`
  QA scenarios:
  ```
  Scenario: workflow and delta schemas are parseable
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && python3 -m json.tool docs/workflows/ads-workflow.schema.json > .omo/evidence/task-5-ads-adaptive-agent-os.txt && python3 -m json.tool docs/workflows/semantic-delta.schema.json >> .omo/evidence/task-5-ads-adaptive-agent-os.txt
    Expected: command exits 0 and evidence contains both formatted schemas.
    Evidence: .omo/evidence/task-5-ads-adaptive-agent-os.txt

  Scenario: valid samples pass and invalid samples are rejected
    Tool:     bash
    Steps:    bash -lc 'npx --yes ajv-cli@5 validate -s docs/workflows/ads-workflow.schema.json -d docs/workflows/examples/jetpartner-search-term-review.workflow.valid.json && npx --yes ajv-cli@5 validate -s docs/workflows/semantic-delta.schema.json -d docs/workflows/examples/jetpartner-search-term-review.delta.valid.json && if npx --yes ajv-cli@5 validate -s docs/workflows/ads-workflow.schema.json -d docs/workflows/examples/jetpartner-search-term-review.workflow.invalid.json; then exit 1; fi && if npx --yes ajv-cli@5 validate -s docs/workflows/semantic-delta.schema.json -d docs/workflows/examples/jetpartner-search-term-review.delta.invalid.json; then exit 1; fi; echo "PASS valid samples accepted and invalid samples rejected" | tee .omo/evidence/task-5-ads-adaptive-agent-os-error.txt'
    Expected: command exits 0; valid workflow/delta samples pass and invalid workflow/delta samples fail validation.
    Evidence: .omo/evidence/task-5-ads-adaptive-agent-os-error.txt
  ```
  Commit: Y | docs(workflows): define typed ads workflow schemas

- [ ] 6. Jetpartner Ads v0 read-only runbook
  What to do / Must NOT do: Create `docs/runbooks/jetpartner-ads-readonly-v0.md`. Define the first end-to-end workflow: read tenant truth, locate latest report artifacts, run or reference read-only observe/audit if authorized, classify search-term and lead-quality issues, draft proposal, stop at human approval, and produce semantic delta. Default v0 uses existing report artifacts; live commands require explicit user authorization and must not use `--apply`. Must not include SEO as required path.
  Parallelization: Wave 2 | Blocked by: 1, 2, 3, 4, 5 | Blocks: 10, 11
  References:
  - `/Users/nora/30x-ads/README.md:10` - observe writes findings/account artifacts.
  - `/Users/nora/30x-ads/README.md:20` - apply dry-run/apply distinction.
  - `/Users/nora/30x-ads/README.md:64` - command list.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md:62` - do not trust remembered numbers.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:51` - qualified lead rule.
  Acceptance criteria:
  - [ ] `test -f docs/runbooks/jetpartner-ads-readonly-v0.md`
  - [ ] `rg -n "read-only|TENANT_ID=jetpartners|no --apply|qualified lead|approval gate|semantic delta|search term" docs/runbooks/jetpartner-ads-readonly-v0.md`
  - [ ] `! rg -n "SEO.*required|pnpm apply .*--apply" docs/runbooks/jetpartner-ads-readonly-v0.md`
  - [ ] `rg -n "no --apply|must not.*--apply" docs/runbooks/jetpartner-ads-readonly-v0.md`
  QA scenarios:
  ```
  Scenario: runbook has a complete read-only chain
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "tenant truth|report artifacts|proposal|approval gate|semantic delta" docs/runbooks/jetpartner-ads-readonly-v0.md | tee .omo/evidence/task-6-ads-adaptive-agent-os.txt
    Expected: command exits 0 and prints every stage.
    Evidence: .omo/evidence/task-6-ads-adaptive-agent-os.txt

  Scenario: runbook rejects mutation in v0
    Tool:     bash
    Steps:    bash -lc 'if rg -n "pnpm apply .*--apply|Google Ads mutation without approval|Supabase mutation without approval" docs/runbooks/jetpartner-ads-readonly-v0.md; then exit 1; else echo "PASS no mutation path in v0 runbook" | tee .omo/evidence/task-6-ads-adaptive-agent-os-error.txt; fi'
    Expected: command exits 0 because no v0 mutation command is present.
    Evidence: .omo/evidence/task-6-ads-adaptive-agent-os-error.txt
  ```
  Commit: Y | docs(runbooks): define jetpartner ads readonly v0

- [ ] 7. OMO execution governance mapping
  What to do / Must NOT do: Create `docs/governance/omo-execution-governance.md`. Map OMO roles to Ads operations: explorer for local artifacts, librarian for external policy/docs, metis for risk, plan for run plan, momus for executable review, executor for approved implementation, QA/gate reviewers for readback. Define evidence ledger, stop rules, and no-self-approval rule. Must not imply the Ads Agent can verify itself.
  Parallelization: Wave 2 | Blocked by: 2, 5 | Blocks: 10, 11
  References:
  - `/Users/nora/.codex/agents/explorer.toml` - read-only codebase search specialist.
  - `/Users/nora/.codex/agents/plan.toml` - planner writes one executable plan.
  - `/Users/nora/.codex/agents/metis.toml` - pre-plan gap analyst.
  - `/Users/nora/.codex/agents/momus.toml` - plan reviewer.
  - OpenAI Subagents docs: `https://developers.openai.com/codex/subagents`
  Acceptance criteria:
  - [ ] `test -f docs/governance/omo-execution-governance.md`
  - [ ] `rg -n "explorer|librarian|metis|plan|momus|executor|QA|gate|no-self-approval" docs/governance/omo-execution-governance.md`
  - [ ] `rg -n "evidence ledger|stop rule|readback|approval" docs/governance/omo-execution-governance.md`
  QA scenarios:
  ```
  Scenario: OMO governance maps all required roles
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && for x in explorer librarian metis plan momus executor QA gate; do rg -n "$x" docs/governance/omo-execution-governance.md; done | tee .omo/evidence/task-7-ads-adaptive-agent-os.txt
    Expected: command exits 0 and prints all role names.
    Evidence: .omo/evidence/task-7-ads-adaptive-agent-os.txt

  Scenario: governance forbids self-approval
    Tool:     bash
    Steps:    rg -n "no-self-approval|cannot verify itself|independent reviewer" docs/governance/omo-execution-governance.md | tee .omo/evidence/task-7-ads-adaptive-agent-os-error.txt
    Expected: command exits 0 and proves independent verification is required.
    Evidence: .omo/evidence/task-7-ads-adaptive-agent-os-error.txt
  ```
  Commit: Y | docs(governance): map omo execution gates

- [ ] 8. Record & Replay skill-factory gate
  What to do / Must NOT do: Create `docs/learning/skill-factory.md`. Define the session learning pipeline: session delta -> classification -> memory patch / skill patch / new skill draft / protocol update -> redaction -> replay -> registry admission. Define skill-worthy threshold: repetitive, stable steps, clear inputs, clear success criteria, at least one verified replay. Must not auto-install generated skills.
  Parallelization: Wave 2 | Blocked by: 3, 5 | Blocks: 10, 11
  References:
  - OpenAI Record & Replay docs: `https://developers.openai.com/codex/record-and-replay`
  - OpenAI Skills docs: `https://developers.openai.com/codex/skills`
  - OpenAI reusable skills use case: `https://developers.openai.com/codex/use-cases/reusable-codex-skills`
  - Trellis workflow inspiration from librarian evidence: task/workspace/spec finish writeback.
  Acceptance criteria:
  - [ ] `test -f docs/learning/skill-factory.md`
  - [ ] `rg -n "session delta|classification|memory patch|skill patch|new skill draft|redaction|replay|registry admission|do not auto-install" docs/learning/skill-factory.md`
  - [ ] `rg -n "repetitive|stable|clear inputs|clear success criteria|verified replay" docs/learning/skill-factory.md`
  QA scenarios:
  ```
  Scenario: skill factory requires replay before registry admission
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "verified replay|registry admission|do not auto-install|candidate" docs/learning/skill-factory.md | tee .omo/evidence/task-8-ads-adaptive-agent-os.txt
    Expected: command exits 0 and prints replay/admission rules.
    Evidence: .omo/evidence/task-8-ads-adaptive-agent-os.txt

  Scenario: skill factory avoids skill explosion
    Tool:     bash
    Steps:    rg -n "not every session|skill explosion|session delta.*not.*skill|classification" docs/learning/skill-factory.md | tee .omo/evidence/task-8-ads-adaptive-agent-os-error.txt
    Expected: command exits 0 and proves every session becomes a delta, not necessarily a skill.
    Evidence: .omo/evidence/task-8-ads-adaptive-agent-os-error.txt
  ```
  Commit: Y | docs(learning): define ads skill factory gate

- [ ] 9. Privacy, redaction, and evidence rules
  What to do / Must NOT do: Create `docs/governance/evidence-redaction.md`. Define evidence classes: safe counts, hashed identifiers, redacted lead examples, raw local-only artifacts, prohibited secrets. Define command whitelist for v0: read-only file inspection, schema validation, `pnpm apply` dry-run only when blueprint exists, no `--apply`, no credential reads. Define data freshness: every claim about live account state needs report timestamp, query window, or command evidence. Must not include PII or tokens.
  Parallelization: Wave 2 | Blocked by: 1, 4, 5 | Blocks: 10, 11
  References:
  - `/Users/nora/30x-ads/AGENTS.md:17` - `.gitignore` excludes credentials and tenant-local data.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md:21` - live-check before quoting facts.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:44` - readback surfaces after mutation.
  Acceptance criteria:
  - [ ] `test -f docs/governance/evidence-redaction.md`
  - [ ] `rg -n "safe counts|hashed|redacted|raw local-only|prohibited secrets|no --apply|data freshness" docs/governance/evidence-redaction.md`
  - [ ] `! rg -n "(refresh_token\\s*=|client_secret\\s*=|access_token\\s*=|Authorization:\\s*|Bearer\\s+[A-Za-z0-9._-]+)" docs/governance/evidence-redaction.md`
  QA scenarios:
  ```
  Scenario: redaction rules classify evidence safely
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "safe counts|hashed identifiers|redacted lead|raw local-only|prohibited secrets" docs/governance/evidence-redaction.md | tee .omo/evidence/task-9-ads-adaptive-agent-os.txt
    Expected: command exits 0 and prints every evidence class.
    Evidence: .omo/evidence/task-9-ads-adaptive-agent-os.txt

  Scenario: no secret patterns appear in evidence policy
    Tool:     bash
    Steps:    bash -lc 'if rg -n "(refresh_token\\s*=|client_secret\\s*=|access_token\\s*=|Authorization:\\s*|Bearer\\s+[A-Za-z0-9._-]+)" docs/governance/evidence-redaction.md; then exit 1; else echo "PASS no secret value patterns" | tee .omo/evidence/task-9-ads-adaptive-agent-os-error.txt; fi'
    Expected: command exits 0 because no secret value pattern is present.
    Evidence: .omo/evidence/task-9-ads-adaptive-agent-os-error.txt
  ```
  Commit: Y | docs(governance): define ads evidence redaction

- [ ] 10. Integration blueprint and handoff package
  What to do / Must NOT do: Create `docs/ads-adaptive-agent-os-blueprint.md`. Integrate all prior artifacts into one operating blueprint: mental model, directory proposal, v0 run sequence, owner boundaries, what gets mounted at runtime, what gets written after a session, and how a worker should execute the next build. Include a compact table mapping each external repo to the one practical idea absorbed. Must not add new scope beyond v0.
  Parallelization: Wave 3 | Blocked by: 6, 7, 8, 9 | Blocks: 11
  References:
  - `docs/research/ads-adaptive-agent-os-evidence.md`
  - `docs/architecture/geb-l1-l3-ads-agent.md`
  - `docs/capabilities/ads-capability-registry.md`
  - `docs/runbooks/jetpartner-ads-readonly-v0.md`
  - External mappings: Flyte typed DAG, agent-roles-spec role package, Trellis persisted learning loop, LazyCodex/OMO verification, agency-agents catalog.
  Acceptance criteria:
  - [ ] `test -f docs/ads-adaptive-agent-os-blueprint.md`
  - [ ] `rg -n "Truth|Work|Learning|Base Ads Agent|Tenant Overlay|Typed Workflow|OMO|GEB|Record & Replay|Jetpartner v0" docs/ads-adaptive-agent-os-blueprint.md`
  - [ ] `rg -n "Flyte|agent-roles-spec|Trellis|LazyCodex|agency-agents" docs/ads-adaptive-agent-os-blueprint.md`
  QA scenarios:
  ```
  Scenario: blueprint includes all core mechanisms
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "Base Ads Agent|Tenant Overlay|Typed Workflow|OMO|GEB|Record & Replay|Jetpartner v0" docs/ads-adaptive-agent-os-blueprint.md | tee .omo/evidence/task-10-ads-adaptive-agent-os.txt
    Expected: command exits 0 and prints every mechanism.
    Evidence: .omo/evidence/task-10-ads-adaptive-agent-os.txt

  Scenario: blueprint stays Ads-only for v0
    Tool:     bash
    Steps:    rg -n "v0.*Ads-only|SEO.*future|no new dashboard|no auto-mutation" docs/ads-adaptive-agent-os-blueprint.md | tee .omo/evidence/task-10-ads-adaptive-agent-os-error.txt
    Expected: command exits 0 and proves scope discipline.
    Evidence: .omo/evidence/task-10-ads-adaptive-agent-os-error.txt
  ```
  Commit: Y | docs: assemble ads adaptive agent os blueprint

- [ ] 11. Final verification wave
  What to do / Must NOT do: Run final plan compliance, schema validation, scope fidelity, redaction checks, and Jetpartner v0 artifact proof. Capture evidence and produce a final verification summary. Must not claim completion from inference or subagent summaries.
  Parallelization: Wave 3 | Blocked by: 10 | Blocks: final
  References:
  - All files produced by Todos 1-10.
  - `/Users/nora/30x-ads/README.md:10` - expected report artifact pattern.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:40` - approval gate.
  Acceptance criteria:
  - [ ] `find docs -type f | sort | tee .omo/evidence/task-11-ads-adaptive-agent-os-files.txt`
  - [ ] `python3 -m json.tool docs/capabilities/ads-capability.schema.json >/tmp/final-capability-schema.json`
  - [ ] `python3 -m json.tool docs/tenants/tenant-overlay.schema.json >/tmp/final-tenant-schema.json`
  - [ ] `python3 -m json.tool docs/workflows/ads-workflow.schema.json >/tmp/final-workflow-schema.json`
  - [ ] `python3 -m json.tool docs/workflows/semantic-delta.schema.json >/tmp/final-delta-schema.json`
  - [ ] `npx --yes ajv-cli@5 validate -s docs/capabilities/ads-capability.schema.json -d docs/capabilities/examples/ads-capability.valid.json`
  - [ ] `bash -lc 'if npx --yes ajv-cli@5 validate -s docs/capabilities/ads-capability.schema.json -d docs/capabilities/examples/ads-capability.invalid.json; then exit 1; else echo "PASS invalid capability rejected"; fi'`
  - [ ] `npx --yes ajv-cli@5 validate -s docs/tenants/tenant-overlay.schema.json -d docs/tenants/examples/jetpartner-overlay.valid.json`
  - [ ] `bash -lc 'if npx --yes ajv-cli@5 validate -s docs/tenants/tenant-overlay.schema.json -d docs/tenants/examples/jetpartner-overlay.invalid.json; then exit 1; else echo "PASS invalid tenant overlay rejected"; fi'`
  - [ ] `npx --yes ajv-cli@5 validate -s docs/workflows/ads-workflow.schema.json -d docs/workflows/examples/jetpartner-search-term-review.workflow.valid.json`
  - [ ] `bash -lc 'if npx --yes ajv-cli@5 validate -s docs/workflows/ads-workflow.schema.json -d docs/workflows/examples/jetpartner-search-term-review.workflow.invalid.json; then exit 1; else echo "PASS invalid workflow rejected"; fi'`
  - [ ] `npx --yes ajv-cli@5 validate -s docs/workflows/semantic-delta.schema.json -d docs/workflows/examples/jetpartner-search-term-review.delta.valid.json`
  - [ ] `bash -lc 'if npx --yes ajv-cli@5 validate -s docs/workflows/semantic-delta.schema.json -d docs/workflows/examples/jetpartner-search-term-review.delta.invalid.json; then exit 1; else echo "PASS invalid delta rejected"; fi'`
  - [ ] `! rg -n "(refresh_token\\s*=|client_secret\\s*=|access_token\\s*=|Authorization:\\s*|Bearer\\s+[A-Za-z0-9._-]+)" docs .omo/evidence`
  QA scenarios:
  ```
  Scenario: final document set exists and schemas parse
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && find docs -type f | sort | tee .omo/evidence/task-11-ads-adaptive-agent-os.txt && python3 -m json.tool docs/capabilities/ads-capability.schema.json >/tmp/final-capability-schema.json && python3 -m json.tool docs/tenants/tenant-overlay.schema.json >/tmp/final-tenant-schema.json && python3 -m json.tool docs/workflows/ads-workflow.schema.json >/tmp/final-workflow-schema.json && python3 -m json.tool docs/workflows/semantic-delta.schema.json >/tmp/final-delta-schema.json && npx --yes ajv-cli@5 validate -s docs/capabilities/ads-capability.schema.json -d docs/capabilities/examples/ads-capability.valid.json && npx --yes ajv-cli@5 validate -s docs/tenants/tenant-overlay.schema.json -d docs/tenants/examples/jetpartner-overlay.valid.json && npx --yes ajv-cli@5 validate -s docs/workflows/ads-workflow.schema.json -d docs/workflows/examples/jetpartner-search-term-review.workflow.valid.json && npx --yes ajv-cli@5 validate -s docs/workflows/semantic-delta.schema.json -d docs/workflows/examples/jetpartner-search-term-review.delta.valid.json
    Expected: command exits 0 and evidence lists every produced docs file.
    Evidence: .omo/evidence/task-11-ads-adaptive-agent-os.txt

  Scenario: final artifacts do not contain secrets
    Tool:     bash
    Steps:    bash -lc 'if rg -n "(refresh_token\\s*=|client_secret\\s*=|access_token\\s*=|Authorization:\\s*|Bearer\\s+[A-Za-z0-9._-]+)" docs .omo/evidence; then exit 1; else echo "PASS no secret value patterns" | tee .omo/evidence/task-11-ads-adaptive-agent-os-error.txt; fi'
    Expected: command exits 0 because docs and evidence contain no secret value patterns.
    Evidence: .omo/evidence/task-11-ads-adaptive-agent-os-error.txt
  ```
  Commit: N | final verification only; include results in handoff.

## Final verification wave
> Runs in parallel after ALL todos. ALL must APPROVE. Surface results and wait for the user's explicit okay before declaring complete.
- [ ] F1. Plan compliance audit
  ```
  Scenario: every planned artifact exists after execution
    Tool:     bash
    Steps:    bash -lc 'set -euo pipefail; mkdir -p .omo/evidence; for f in docs/research/ads-adaptive-agent-os-evidence.md docs/architecture/geb-l1-l3-ads-agent.md docs/capabilities/ads-capability-registry.md docs/capabilities/ads-capability.schema.json docs/capabilities/examples/ads-capability.valid.json docs/capabilities/examples/ads-capability.invalid.json docs/tenants/tenant-overlay-contract.md docs/tenants/tenant-overlay.schema.json docs/tenants/examples/jetpartner-overlay.valid.json docs/tenants/examples/jetpartner-overlay.invalid.json docs/workflows/ads-workflow.schema.json docs/workflows/semantic-delta.schema.json docs/workflows/examples/jetpartner-search-term-review.workflow.valid.json docs/workflows/examples/jetpartner-search-term-review.workflow.invalid.json docs/workflows/examples/jetpartner-search-term-review.delta.valid.json docs/workflows/examples/jetpartner-search-term-review.delta.invalid.json docs/runbooks/jetpartner-ads-readonly-v0.md docs/governance/omo-execution-governance.md docs/learning/skill-factory.md docs/governance/evidence-redaction.md docs/ads-adaptive-agent-os-blueprint.md; do test -f "$f"; echo "FOUND $f"; done | tee .omo/evidence/f1-plan-compliance.txt'
    Expected: command exits 0.
    Evidence: .omo/evidence/f1-plan-compliance.txt
  ```
- [ ] F2. Scope fidelity
  ```
  Scenario: v0 remains Ads-only and excludes forbidden runtime expansion
    Tool:     bash
    Steps:    bash -lc 'if rg -n "SEO.*required|new dashboard.*must build|auto-mutate|deploy Flyte|Kubernetes.*v0|tenant facts.*base agent" docs; then exit 1; else echo "PASS scope fidelity" | tee .omo/evidence/f2-scope-fidelity.txt; fi'
    Expected: command exits 0 and prints PASS.
    Evidence: .omo/evidence/f2-scope-fidelity.txt
  ```
- [ ] F3. Schema and sample validation
  ```
  Scenario: schemas parse and samples validate/reject correctly
    Tool:     bash
    Steps:    bash -lc 'python3 -m json.tool docs/capabilities/ads-capability.schema.json >/tmp/final-capability-schema.json && python3 -m json.tool docs/tenants/tenant-overlay.schema.json >/tmp/final-tenant-schema.json && python3 -m json.tool docs/workflows/ads-workflow.schema.json >/tmp/final-workflow-schema.json && python3 -m json.tool docs/workflows/semantic-delta.schema.json >/tmp/final-delta-schema.json && npx --yes ajv-cli@5 validate -s docs/capabilities/ads-capability.schema.json -d docs/capabilities/examples/ads-capability.valid.json && npx --yes ajv-cli@5 validate -s docs/tenants/tenant-overlay.schema.json -d docs/tenants/examples/jetpartner-overlay.valid.json && npx --yes ajv-cli@5 validate -s docs/workflows/ads-workflow.schema.json -d docs/workflows/examples/jetpartner-search-term-review.workflow.valid.json && npx --yes ajv-cli@5 validate -s docs/workflows/semantic-delta.schema.json -d docs/workflows/examples/jetpartner-search-term-review.delta.valid.json && if npx --yes ajv-cli@5 validate -s docs/capabilities/ads-capability.schema.json -d docs/capabilities/examples/ads-capability.invalid.json; then exit 1; fi && if npx --yes ajv-cli@5 validate -s docs/tenants/tenant-overlay.schema.json -d docs/tenants/examples/jetpartner-overlay.invalid.json; then exit 1; fi && if npx --yes ajv-cli@5 validate -s docs/workflows/ads-workflow.schema.json -d docs/workflows/examples/jetpartner-search-term-review.workflow.invalid.json; then exit 1; fi && if npx --yes ajv-cli@5 validate -s docs/workflows/semantic-delta.schema.json -d docs/workflows/examples/jetpartner-search-term-review.delta.invalid.json; then exit 1; fi; echo "PASS schema samples" | tee .omo/evidence/f3-schema-validation.txt'
    Expected: command exits 0; all four valid samples pass and all four invalid samples fail.
    Evidence: .omo/evidence/f3-schema-validation.txt
  ```
- [ ] F4. Redaction and privacy review
  ```
  Scenario: docs and evidence contain no secret value patterns
    Tool:     bash
    Steps:    bash -lc 'if rg -n "(refresh_token\\s*=|client_secret\\s*=|access_token\\s*=|Authorization:\\s*|Bearer\\s+[A-Za-z0-9._-]+)" docs .omo/evidence; then exit 1; else echo "PASS privacy redaction" | tee .omo/evidence/f4-redaction.txt; fi'
    Expected: command exits 0 and prints PASS.
    Evidence: .omo/evidence/f4-redaction.txt
  ```
- [ ] F5. Jetpartner read-only surface proof
  ```
  Scenario: runbook proves Jetpartner v0 is read-only and tied to existing 30x-ads commands
    Tool:     bash
    Steps:    bash -lc 'rg -n "TENANT_ID=jetpartners|pnpm observe|qualified lead|approval gate|semantic delta" docs/runbooks/jetpartner-ads-readonly-v0.md && if rg -n "pnpm apply .*--apply" docs/runbooks/jetpartner-ads-readonly-v0.md; then exit 1; fi; echo "PASS jetpartner readonly proof" | tee .omo/evidence/f5-jetpartner-readonly.txt'
    Expected: command exits 0 and prints PASS.
    Evidence: .omo/evidence/f5-jetpartner-readonly.txt
  ```

## Commit strategy
- Do not auto-commit unless the user explicitly asks.
- If executed, group commits by artifact family:
  - `docs(research): establish ads adaptive agent evidence baseline`
  - `docs(architecture): define ads agent geb skeleton`
  - `docs(capabilities): define ads capability registry`
  - `docs(tenants): define ads tenant overlay contract`
  - `docs(workflows): define typed ads workflow schemas`
  - `docs(runbooks): define jetpartner ads readonly v0`
  - `docs(governance): map omo execution gates`
  - `docs(learning): define ads skill factory gate`
  - `docs: assemble ads adaptive agent os blueprint`
- Each commit should include `Plan: .omo/plans/ads-adaptive-agent-os.md` in the footer.

## Success criteria
- Ads Adaptive Agent OS is defined as a reusable base agent plus runtime tenant overlays.
- GEB L1-L3 is scoped to the Ads Agent skeleton, not to all tenants.
- Jetpartner v0 is read-only by default and optimizes around qualified lead truth.
- Typed workflows and semantic deltas have schemas plus valid/invalid examples.
- OMO roles are mapped to evidence-backed execution governance.
- Record & Replay is treated as a skill-candidate factory with replay/redaction gates.
- All docs and evidence pass secret-pattern checks.
- Final handoff tells the worker exactly what to build next without another interview.
