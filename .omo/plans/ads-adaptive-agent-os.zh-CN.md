# ads-adaptive-agent-os - 中文工作计划

## 给人看的 TL;DR
**你会得到什么：** 一份收窄后的 Ads Adaptive Agent OS 计划，不是泛化的 Marketing OS。它定义一个可复用的 Ads Agent 骨架，把 Jetpartner 作为第一个租户 overlay 挂载，并复用现有 `30x-ads` 执行能力，而不是重新发明运行时。

**为什么这样做：** 可复用 agent 必须和 tenant facts 分离，否则无法 scale。第一条验证链路选 Jetpartner Ads 只读审查，因为它已经有真实引擎、角色包、qualified-lead truth、人工 approval gate 和报告表面。

**不会做什么：** 不建新 dashboard，不自动修改 Google Ads，不把 SEO 放进 v0 必需范围，不把 Record & Replay 生成的 skill 未经 replay 验证就安装。

**工作量：** Large
**风险：** Medium - 设计跨 role package、workflow contract、execution governance、evidence 和 learning loop，但 v0 保持 docs/schema/runbook-first。
**我替你做的默认决策：** 把本任务视为开放式架构规划；v0 只采用 schema-only 的 Flyte-style workflow；GEB L1-L3 只描述 Ads Agent 骨架；Jetpartner 只作为运行时 overlay；Record & Replay 只生成 skill candidate，replay 通过前不进 registry；除非用户明确授权，live external reads 默认使用已有 artifact。

下一步：你可以批准用 `$start-work` 执行该计划，或者先要求一次高精度 Momus review。

---

> 机器版 TL;DR：Large/Medium；交付 Ads Adaptive Agent OS 骨架计划，包含 GEB L1-L3、role-package contract、typed workflow schemas、Jetpartner v0 runbook、OMO evidence gates、skill-factory governance。

## 范围
### 必须有
- 把目标重新定义为 `Ads Adaptive Agent OS`，不是 `Marketing Adaptive Agent OS`。
- 以 `/Users/nora/.codex/skills/ads` 作为通用 Ads capability system 的基础；它已经有自然语言 router 和 specialized sub-skill/worker routing，见 `/Users/nora/.codex/skills/ads/SKILL.md:8` 和 `/Users/nora/.codex/skills/ads/SKILL.md:23`。
- 保留 `30x-ads` 作为确定性 domain engine。它已经定义每个 tenant 的三步流：`pnpm observe`、agent proposal、`pnpm apply --blueprint` dry-run/apply，见 `/Users/nora/30x-ads/README.md:8`。
- Jetpartner 只作为第一个 tenant overlay，不作为 base agent。现有 tenant truth 在 `/Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md:5`。
- 所有 Google Ads/Supabase mutation 必须保留 human approval。role package 在 `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:22` 禁止 auto-apply；skill 在 `/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:40` 要求明确确认。
- GEB L1-L3 只定义 Ads Agent 骨架：
  - L1：Ads Adaptive Agent constitution。
  - L2：可复用模块地图，例如 search-term review、lead-quality review、budget review。
  - L3：skill/workflow contract，包含 input、output、position、approval、evidence、learning-delta rules。
- tenant overlay 是 runtime context：`tenant_truth`、`tenant_memory`、`permissions`、`approved_examples`、`launchplans`；不要把 tenant 内容复制进 base agent。
- Flyte 只作为 typed task/workflow/launch-plan 的抽象来源。v0 不部署 Flyte。Flyte docs 把 task 定义为强类型、版本化 compute unit，把 workflow 定义为 DAG，把 launch plan 定义为输入/schedule 绑定。
- agent-roles-spec 作为 role package 的心智模型：role definition、memory、skills、tools、host adapters、lifecycle。
- OMO/LazyCodex 作为 execution governance：planner、executor、QA、reviewer、evidence、gate；它不是 Ads domain engine。
- Trellis 作为 persisted workflow/spec/task/workspace learning loop 的参考。
- agency-agents 只作为 catalog inspiration：清晰 deliverables、success metrics、multi-host conversion；v0 不导入 232 个 agents。
- Codex Record & Replay 只用于 repetitive、stable、success criteria 清晰的 workflow。v0 中生成的 skill 必须作为 candidate，只有 replay 和 redaction 通过后才能进入 registry。
- 产出可执行 artifact：docs、schemas、sample instances、runbooks、verification commands。worker 不需要再次采访用户就能执行。

### 必须不做
- v0 不建新的 dashboard 或产品 UI。`30x-ads` 已经说明 agent 是 control plane，不是 dashboard，见 `/Users/nora/30x-ads/README.md:6`。
- v0 不要求 SEO。`30x SEO` 只作为未来 capability extension 或 optional signal。
- 不读取 `.env`、OAuth tokens、raw credentials、tenant exports 作为 evidence。
- 未经当前任务明确确认，不执行 Google Ads 或 Supabase mutation。
- 不让每次 session 都创建新 skill。每次 session 先产生 learning delta；只有稳定、可 replay 的 delta 才能变成 skill draft。
- 不把 tenant-specific private aviation rules 写进 base Ads Agent，除非作为 example。
- v0 不引入 Flyte、Kubernetes、新 queue、新 database。
- schema 验收不能只靠 grep；每个 schema 必须有 good sample 通过和 bad sample 拒绝。

## 验证策略
> Zero human intervention - all verification is agent-executed.
- 测试策略：tests-after + schema validation + markdown contract checks。v0 不涉及 production code behavior change。
- 证据路径：`.omo/evidence/task-<N>-ads-adaptive-agent-os.<ext>`
- 真实表面：v0 的 faithful surface 是 CLI/filesystem artifacts：现有 `30x-ads` reports、dry-run commands、schema validators、生成的 plan/runbook files。只有任务明确触碰现有 report URL 或 generated `monitor.html` 时才需要 browser QA。
- 安全证明：所有 evidence artifact 必须通过 secret/PII grep checks。
- Review 证明：final verification 必须覆盖 plan compliance、scope fidelity、schema sample validation、Jetpartner read-only dry-run/readback scenario。

## 执行策略
### 并行执行波次
> 每波目标 5-8 个 todo；除最终波外少于 3 个说明拆分不足。

Wave 1，无依赖：
- Todo 1：Evidence baseline and repo boundaries。
- Todo 2：Ads Agent GEB L1-L3 skeleton contract。
- Todo 3：Capability and source-priority registry。
- Todo 4：Tenant overlay contract。
- Todo 5：Typed workflow and semantic-delta schemas。

Wave 2，依赖 Wave 1：
- Todo 6：Jetpartner Ads v0 read-only runbook。
- Todo 7：OMO execution governance mapping。
- Todo 8：Record & Replay skill-factory gate。
- Todo 9：Privacy, redaction, and evidence rules。

Wave 3，依赖 Wave 2：
- Todo 10：Integration blueprint and handoff package。
- Todo 11：Final verification wave。

Critical path：Todo 1 -> Todo 2 -> Todo 5 -> Todo 6 -> Todo 10 -> Todo 11

### 依赖矩阵
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
  要做 / 不要做：创建 `docs/research/ads-adaptive-agent-os-evidence.md`。记录已验证的本地和外部证据：base Ads skill、30x-ads engine、Jetpartner role package、tenant overlay、OMO agents、GEB docs、Flyte、agent-roles-spec、Trellis、agency-agents、Codex Record & Replay。每条证据包含 source family、path/URL、一句话 claim、是否属于 v0 requirement 或 later inspiration。不得读取 credentials、`.env`、raw tenant exports、stale chat logs。
  并行：Wave 1 | Blocked by: none | Blocks: 6, 9, 10
  References:
  - `/Users/nora/.codex/skills/ads/SKILL.md:8` - base Ads skill routes natural-language ad tasks.
  - `/Users/nora/30x-ads/README.md:6` - 30x-ads is the multi-tenant Google Ads engine and avoids a new dashboard/orchestrator.
  - `/Users/nora/30x-ads/README.md:64` - 30x-ads command surface.
  - `/Users/nora/30x-ads/AGENTS.md:5` - 30x-ads GEB L1 project map.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:1` - role package schema marker.
  - `/Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md:5` - qualified lead truth.
  - `https://developers.openai.com/codex/record-and-replay` - Record & Replay turns a demonstrated workflow into a reusable skill.
  - `https://developers.openai.com/codex/concepts/customization` - AGENTS, memories, skills, MCP, and subagents are complementary.
  Acceptance criteria:
  - [ ] `test -f docs/research/ads-adaptive-agent-os-evidence.md`
  - [ ] `rg -n "Base Ads Agent|30x-ads|Jetpartner|GEB|OMO|Flyte|agent-roles-spec|Trellis|agency-agents|Record & Replay" docs/research/ads-adaptive-agent-os-evidence.md`
  - [ ] `rg -n "v0 requirement|later inspiration|source family" docs/research/ads-adaptive-agent-os-evidence.md`
  QA scenarios:
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
  要做 / 不要做：创建 `docs/architecture/geb-l1-l3-ads-agent.md`。只为 reusable Ads Adaptive Agent 定义 GEB L1/L2/L3：L1 constitution、L2 module maps、L3 unit contracts。明确 tenants 是 overlay，不属于 base skeleton。可以写未来 `agents/ads-adaptive-agent/` 树形建议，但除非此 todo 明确 scaffold，否则不创建目录。不得把 Jetpartner-specific rules 写进 L1，除非作为 examples。
  并行：Wave 1 | Blocked by: none | Blocks: 6, 7, 10
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
  要做 / 不要做：创建 `docs/capabilities/ads-capability-registry.md`、`docs/capabilities/ads-capability.schema.json`、`docs/capabilities/examples/ads-capability.valid.json`、`docs/capabilities/examples/ads-capability.invalid.json`。定义 capability fields：`id`、`kind`、`trigger`、`inputs`、`outputs`、`side_effects`、`approval_gate`、`evidence_required`、`source_priority`、`source_ref`、`version`。定义 source priority：project-local Jetpartner role package > 30x-ads repo skills/scripts > global ads skills > SEO skills as optional future signal。不得复制完整 skill body。
  并行：Wave 1 | Blocked by: none | Blocks: 6, 8, 10
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
  ```
  Commit: Y | docs(capabilities): define ads capability registry

- [ ] 4. Tenant overlay contract
  要做 / 不要做：创建 `docs/tenants/tenant-overlay-contract.md`、`docs/tenants/tenant-overlay.schema.json`、`docs/tenants/examples/jetpartner-overlay.valid.json`、`docs/tenants/examples/jetpartner-overlay.invalid.json`。定义 runtime overlay fields：`tenant_id`、`business_truth`、`industry_overlay_refs`、`role_package_ref`、`permissions`、`data_freshness_policy`、`report_artifact_refs`、`approved_examples`、`mutation_policy`、`pii_policy`。用 Jetpartner 做 sample，但不能把 private aviation rules 烧进 base Ads Agent。不得复制 engine code 或存 secrets。
  并行：Wave 1 | Blocked by: none | Blocks: 6, 9, 10
  Acceptance criteria:
  - [ ] `test -f docs/tenants/tenant-overlay-contract.md`
  - [ ] `test -f docs/tenants/tenant-overlay.schema.json`
  - [ ] `test -f docs/tenants/examples/jetpartner-overlay.valid.json`
  - [ ] `test -f docs/tenants/examples/jetpartner-overlay.invalid.json`
  - [ ] `python3 -m json.tool docs/tenants/tenant-overlay.schema.json >/tmp/tenant-overlay.schema.json`
  - [ ] `npx --yes ajv-cli@5 validate -s docs/tenants/tenant-overlay.schema.json -d docs/tenants/examples/jetpartner-overlay.valid.json`
  - [ ] `bash -lc 'if npx --yes ajv-cli@5 validate -s docs/tenants/tenant-overlay.schema.json -d docs/tenants/examples/jetpartner-overlay.invalid.json; then exit 1; else echo "PASS invalid tenant overlay rejected"; fi'`
  - [ ] `rg -n "tenant_id|business_truth|permissions|data_freshness_policy|mutation_policy|pii_policy|Jetpartner" docs/tenants/tenant-overlay-contract.md`
  Commit: Y | docs(tenants): define ads tenant overlay contract

- [ ] 5. Typed workflow and semantic-delta schemas
  要做 / 不要做：创建 `docs/workflows/ads-workflow.schema.json`、`docs/workflows/semantic-delta.schema.json`、valid/invalid workflow examples、valid/invalid delta examples。借鉴 Flyte 的 typed steps，但不引入 Flyte runtime。workflow 必须有 task id、typed inputs/outputs、dependencies、side effects、approval gate、evidence path。delta 必须有 observed action、machine artifacts、semantic artifacts、approval state、QA evidence、learning classification、skill candidate、replay status、rollback plan。delta 不能是自由文本 journal。
  并行：Wave 1 | Blocked by: none | Blocks: 6, 8, 9, 10
  Commit: Y | docs(workflows): define typed ads workflow schemas

- [ ] 6. Jetpartner Ads v0 read-only runbook
  要做 / 不要做：创建 `docs/runbooks/jetpartner-ads-readonly-v0.md`。定义第一条端到端 workflow：读取 tenant truth，定位最新 report artifacts，在授权时运行或引用 read-only observe/audit，分类 search-term 和 lead-quality issues，起草 proposal，在 human approval 前停止，并产生 semantic delta。v0 默认使用已有 report artifacts；live commands 需要用户明确授权，且不得使用 `--apply`。不得把 SEO 放进 required path。
  并行：Wave 2 | Blocked by: 1, 2, 3, 4, 5 | Blocks: 10, 11
  Commit: Y | docs(runbooks): define jetpartner ads readonly v0

- [ ] 7. OMO execution governance mapping
  要做 / 不要做：创建 `docs/governance/omo-execution-governance.md`。把 OMO roles 映射到 Ads operations：explorer 查本地 artifacts，librarian 查外部政策/docs，metis 做风险，plan 写 run plan，momus 做 executable review，executor 执行已批准实现，QA/gate reviewers 做 readback。定义 evidence ledger、stop rules、no-self-approval rule。不得暗示 Ads Agent 可以自己验证自己。
  并行：Wave 2 | Blocked by: 2, 5 | Blocks: 10, 11
  Commit: Y | docs(governance): map omo execution gates

- [ ] 8. Record & Replay skill-factory gate
  要做 / 不要做：创建 `docs/learning/skill-factory.md`。定义 session learning pipeline：session delta -> classification -> memory patch / skill patch / new skill draft / protocol update -> redaction -> replay -> registry admission。定义 skill-worthy threshold：repetitive、stable steps、clear inputs、clear success criteria、至少一个 verified replay。不得 auto-install generated skills。
  并行：Wave 2 | Blocked by: 3, 5 | Blocks: 10, 11
  Commit: Y | docs(learning): define ads skill factory gate

- [ ] 9. Privacy, redaction, and evidence rules
  要做 / 不要做：创建 `docs/governance/evidence-redaction.md`。定义 evidence classes：safe counts、hashed identifiers、redacted lead examples、raw local-only artifacts、prohibited secrets。定义 v0 command whitelist：read-only file inspection、schema validation、只有 blueprint 已存在时允许 `pnpm apply` dry-run、no `--apply`、no credential reads。所有 live account state claim 必须记录 report timestamp、query window 或 command evidence。不得包含 PII 或 tokens。
  并行：Wave 2 | Blocked by: 1, 4, 5 | Blocks: 10, 11
  Commit: Y | docs(governance): define ads evidence redaction

- [ ] 10. Integration blueprint and handoff package
  要做 / 不要做：创建 `docs/ads-adaptive-agent-os-blueprint.md`。把前面 artifact 整合成一个 operating blueprint：mental model、directory proposal、v0 run sequence、owner boundaries、runtime mount 内容、session 结束后写回内容、worker 如何执行下一步。包含一个表格：每个外部 repo 吸收了什么 practical idea。不得增加 v0 以外的新 scope。
  并行：Wave 3 | Blocked by: 6, 7, 8, 9 | Blocks: 11
  Commit: Y | docs: assemble ads adaptive agent os blueprint

- [ ] 11. Final verification wave
  要做 / 不要做：执行 final plan compliance、schema validation、scope fidelity、redaction checks、Jetpartner v0 artifact proof。捕获 evidence 并写 final verification summary。不得从推断或 subagent summary 宣称完成。
  并行：Wave 3 | Blocked by: 10 | Blocks: final
  Commit: N | final verification only; include results in handoff.

## Final verification wave
> 所有 todos 完成后并行执行，全部通过后才能交付。
- [ ] F1. Plan compliance audit - 确认所有计划 artifact 存在。
- [ ] F2. Scope fidelity - 拒绝 v0 引入 SEO requirement、新 dashboard、auto-mutation、Flyte runtime、或把 tenant facts 写进 base agent skeleton。
- [ ] F3. Schema and sample validation - 四类 schema 都必须 parse，valid sample 通过，invalid sample 被拒绝。
- [ ] F4. Redaction and privacy review - docs/evidence 中不得出现 secret value patterns。
- [ ] F5. Jetpartner read-only surface proof - runbook 必须引用现有 30x-ads commands，并且不包含 `pnpm apply .*--apply`。

## Commit strategy
- 不自动 commit，除非用户明确要求。
- 如果执行，按 artifact family 分组提交：
  - `docs(research): establish ads adaptive agent evidence baseline`
  - `docs(architecture): define ads agent geb skeleton`
  - `docs(capabilities): define ads capability registry`
  - `docs(tenants): define ads tenant overlay contract`
  - `docs(workflows): define typed ads workflow schemas`
  - `docs(runbooks): define jetpartner ads readonly v0`
  - `docs(governance): map omo execution gates`
  - `docs(learning): define ads skill factory gate`
  - `docs: assemble ads adaptive agent os blueprint`
- 每个 commit footer 加：`Plan: .omo/plans/ads-adaptive-agent-os.md`

## Success criteria
- Ads Adaptive Agent OS 被定义为 reusable base agent + runtime tenant overlays。
- GEB L1-L3 只描述 Ads Agent skeleton，不描述所有 tenants。
- Jetpartner v0 默认 read-only，并围绕 qualified lead truth 优化。
- Typed workflows 和 semantic deltas 有 schemas + valid/invalid examples。
- OMO roles 被映射为 evidence-backed execution governance。
- Record & Replay 被定义为 skill-candidate factory，并带 replay/redaction gates。
- 所有 docs 和 evidence 通过 secret-pattern checks。
- 最终 handoff 能让 worker 不再采访用户，直接知道下一步要建什么。
