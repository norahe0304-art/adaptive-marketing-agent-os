# Marketing Adaptive Agent OS

## TL;DR
> Summary:      建立一个以 Jetpartners 为 v0 试点的 Marketing Adaptive Agent OS：用 30x-ads 负责付费获客闭环，用 30x SEO skills 负责自然搜索与 AI 搜索闭环，用 agent-roles-spec 固化角色包，用 OMO/LazyCodex 执行循环保证证据与 QA，用 GEB semantic delta 让代码相、文档相、操作相持续同构。
> Deliverables:
> - 分层架构：Tenant / Data / Capability / Role / Execution / Learning 六层。
> - v0 最小闭环：Jetpartners 每日 observe → delta → SEO/Ads 诊断 → proposal → human gate → apply/read-only action → evidence → skill factory。
> - 文件/目录建议：`marketing-adaptive-agent-os/` 仓库骨架、roles、skills、tenants、deltas、evidence、playbooks。
> - Agent 角色设计：Marketing OS Director、Ads Operator、SEO Strategist、Semantic Delta Keeper、Skill Factory Curator、LazyCodex Conductor、QA Gate Reviewer。
> - 运行流程：从人工操作观察到可复用 skill 的闭环。
> - 30/60/90 天路线：30 天 Jetpartners 可跑，60 天多租户推广，90 天形成自进化技能工厂。
> Effort:       Large
> Risk:         Medium - 最大风险不是模型能力，而是没有把营销决策、人工批准、证据、文档变更绑定成同一个 delta。

## Scope
### Must have
- 以 Jetpartners 作为唯一 v0 试点租户；不得先做泛化平台。
- 复用 30x-ads 的既有多租户 Google Ads 引擎、`TENANT_ID` 操作流、`blueprint.json`、`monitor.html`、T+N verdict 和真实 CPA 思路；证据来源：`/Users/nora/30x-ads/SYSTEM-OVERVIEW.md:15`、`/Users/nora/30x-ads/SYSTEM-OVERVIEW.md:95`、`/Users/nora/30x-ads/SYSTEM-OVERVIEW.md:117`。
- 接入 30x SEO skills 作为 capability registry，不把每个 SEO 能力重写成产品代码。
- 接入 30x Ads engine 与 Jetpartners role package；Jetpartners 的优化真值必须是 qualified lead，不是 GA4 raw lead；证据来源：`/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:51`。
- Agent role package 必须兼容 `agent-role/preview-0.1` 风格的 `role.toml`，包括 identity、contents、permissions；证据来源：`/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:1`、`/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:29`、`/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:36`。
- LazyCodex/OMO loop 必须作为执行协议：计划选择、Boulder 状态、子任务派发、真实表面 QA、ledger evidence、独立 reviewer gate；证据来源：`/Users/nora/.codex/plugins/cache/sisyphuslabs/omo/4.12.1/skills/start-work/SKILL.md:47`、`/Users/nora/.codex/plugins/cache/sisyphuslabs/omo/4.12.1/skills/start-work/SKILL.md:67`、`/Users/nora/.codex/plugins/cache/sisyphuslabs/omo/4.12.1/skills/start-work/SKILL.md:115`。
- GEB semantic delta 必须成为 OS 的最小数据单元：每次营销事实变化、人工操作、代码/文档/skill 变化都落成一个 delta。
- Skill factory 必须从 Codex Record & Replay / skill-creator 原理出发：观察人工操作、抽取可变输入、生成 SKILL.md、回放验证、再纳入 capability registry；官方依据：`https://developers.openai.com/codex/record-and-replay` 行 688-695，`https://developers.openai.com/codex/skills` 行 672-680。
- 所有执行任务必须有 agent-executed QA，不允许“人工看一下”作为验收。

### Must NOT have (guardrails, anti-slop, scope boundaries)
- 不做新的 dashboard 作为 v0 核心；30x-ads 已明确 Claude Code conversation 是控制平面、`monitor.html` 是静态可视化；证据来源：`/Users/nora/30x-ads/ARCHITECTURE.md:18`、`/Users/nora/30x-ads/ARCHITECTURE.md:20`。
- 不允许未经当前任务明确确认的 Google Ads / Supabase mutation；证据来源：`/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:40`。
- 不把 SEO skills、Ads engine、role package、OMO loop 合并成一个巨型 agent prompt；它们必须是 registry + role + execution contract。
- 不把 GA4 raw lead volume 当作 lead quality；证据来源：`/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:65`。
- 不跳过 AGENTS.md / GEB 文档同步；Codex 官方也把 AGENTS.md 定义为持久项目 guidance；依据：`https://developers.openai.com/codex/guides/agents-md` 行 673-680。
- 不把 skill factory 生成的 skill 直接上线；必须先通过回放、触发描述检查、证据脱敏检查和至少一个真实 Jetpartners replay case。

## Verification strategy
> Zero human intervention - all verification is agent-executed.
- Test decision: tests-after + Markdown/JSON/TOML structural checks, shell assertions, optional schema validation once schema文件存在。
- QA policy: every task has agent-executed scenarios；所有浏览器或操作表面 QA 必须走真实页面、真实 CLI 输出、真实文件检查或真实 API readback。
- Evidence: `.omo/evidence/task-<N>-<slug>.<ext>`

## Execution strategy
### Parallel execution waves
> Target 5-8 tasks per wave. <3 per wave (except final) = under-splitting.
> Extract shared dependencies as Wave-1 tasks to maximize parallelism.

Wave 1 (no dependencies):
- Task 1: 证据基线与系统边界审计
- Task 2: 分层架构文档
- Task 3: Capability registry 设计
- Task 4: Role package 标准
- Task 5: Semantic delta/GEB 契约

Wave 2 (after Wave 1):
- Task 6: Jetpartners v0 最小闭环 runbook，depends [1, 2, 3, 4, 5]
- Task 7: OMO/LazyCodex 执行协议映射，depends [2, 4, 5]
- Task 8: Skill factory 流程设计，depends [3, 4, 5]
- Task 9: 文件/目录骨架建议，depends [2, 3, 4, 5]
- Task 10: QA/evidence/redaction 策略，depends [1, 5, 7]

Wave 3 (after Wave 2):
- Task 11: 30/60/90 天路线与 KPI，depends [6, 8, 10]
- Task 12: 集成蓝图总装与评审包，depends [6, 7, 8, 9, 10, 11]

Critical path: Task 1 -> Task 5 -> Task 7 -> Task 10 -> Task 12

### Dependency matrix
| Task | Depends on | Blocks | Can parallelize with |
|------|------------|--------|----------------------|
| 1    | none       | 6, 10  | 2, 3, 4, 5           |
| 2    | none       | 6, 7, 9 | 1, 3, 4, 5          |
| 3    | none       | 6, 8, 9 | 1, 2, 4, 5          |
| 4    | none       | 6, 7, 8, 9 | 1, 2, 3, 5      |
| 5    | none       | 6, 7, 8, 9, 10 | 1, 2, 3, 4  |
| 6    | 1, 2, 3, 4, 5 | 11, 12 | 7, 8, 9, 10    |
| 7    | 2, 4, 5    | 10, 12 | 6, 8, 9             |
| 8    | 3, 4, 5    | 11, 12 | 6, 7, 9, 10         |
| 9    | 2, 3, 4, 5 | 12     | 6, 7, 8, 10         |
| 10   | 1, 5, 7    | 11, 12 | 6, 8, 9             |
| 11   | 6, 8, 10   | 12     | none                 |
| 12   | 6, 7, 8, 9, 10, 11 | final | none          |

## Todos
> Implementation + Test = ONE task. Never separate.
> Every task MUST have: References + Acceptance Criteria + QA Scenarios + Commit.

- [ ] 1. 证据基线与系统边界审计

  What to do: 建立 `docs/research/evidence-baseline.md`，列出当前工作区为空仓库、30x-ads 现状、Jetpartners role package、30x SEO/Ads skill inventories、OMO/LazyCodex loop、OpenAI Codex skill/AGENTS/subagents 官方依据。标出每条证据的路径、行号、可信级别、是否可用于 v0。
  Must NOT do: 不推断不存在的源码；不把历史记忆当 live facts；不读取或写入密钥。

  Parallelization: Can parallel: YES | Wave 1 | Blocks: [6, 10] | Blocked by: []

  References (executor has NO interview context - be exhaustive):
  - Pattern:  `/Users/nora/30x-ads/SYSTEM-OVERVIEW.md:15` - 30x-ads 是 multi-tenant Google Ads engine，Claude Code 是控制面。
  - Pattern:  `/Users/nora/30x-ads/ARCHITECTURE.md:12` - 30x-ads 北极星原则。
  - Pattern:  `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:1` - role package schema。
  - Pattern:  `/Users/nora/.codex/plugins/cache/sisyphuslabs/omo/4.12.1/skills/start-work/SKILL.md:24` - orchestrator 不直接实现的约束。
  - External: `https://developers.openai.com/codex/skills` - Codex skills 的结构与渐进披露。
  - External: `https://developers.openai.com/codex/guides/agents-md` - AGENTS.md discovery 与优先级。

  Acceptance criteria (agent-executable only):
  - [ ] `test -f docs/research/evidence-baseline.md`
  - [ ] `rg -n "Jetpartners|30x SEO|30x Ads|agent-role/preview-0.1|LazyCodex|OMO|GEB|Record & Replay" docs/research/evidence-baseline.md`
  - [ ] `rg -n "/Users/nora/30x-ads/.+:[0-9]+" docs/research/evidence-baseline.md`
  - [ ] `rg -n "https://developers.openai.com/codex" docs/research/evidence-baseline.md`

  QA scenarios (MANDATORY - task incomplete without these):
  > Name the exact tool AND its exact invocation - not "verify it works". Browser use: use Chrome to drive the page; if Chrome is not available, download and use agent-browser (https://github.com/vercel-labs/agent-browser). Computer use: OS-level GUI automation for a non-browser desktop app.
  ```
  Scenario: baseline captures all source families
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "Jetpartners|30x SEO|30x Ads|agent-role/preview-0.1|LazyCodex|OMO|GEB|Record & Replay" docs/research/evidence-baseline.md | tee .omo/evidence/task-1-evidence-baseline.txt
    Expected: command exits 0 and output contains all eight tokens.
    Evidence: .omo/evidence/task-1-evidence-baseline.txt

  Scenario: no secret-bearing files referenced as evidence
    Tool:     bash
    Steps:    ! rg -n "(\\.env|refresh_token|client_secret|access_token|Authorization:|Bearer )" docs/research/evidence-baseline.md | tee .omo/evidence/task-1-evidence-baseline-error.txt
    Expected: command exits 0 because no secret pattern is found.
    Evidence: .omo/evidence/task-1-evidence-baseline-error.txt
  ```

  Commit: YES | Message: `docs(research): establish marketing os evidence baseline` | Files: [docs/research/evidence-baseline.md]

- [ ] 2. 分层架构文档

  What to do: 创建 `docs/architecture/layered-architecture.md`，定义六层：L0 Operating Doctrine、L1 Tenant & Truth、L2 Data/Signal Plane、L3 Capability Registry、L4 Role & Policy Plane、L5 Execution/Evidence Plane、L6 Learning/Skill Factory Plane。明确每层输入、输出、状态归属、失败模式和 v0 取舍。
  Must NOT do: 不画只有名词的空架构图；每层必须落到 Jetpartners/30x-ads/30x-seo/OMO/GEB/skill factory 的实际职责。

  Parallelization: Can parallel: YES | Wave 1 | Blocks: [6, 7, 9] | Blocked by: []

  References (executor has NO interview context - be exhaustive):
  - Pattern:  `/Users/nora/30x-ads/ARCHITECTURE.md:24` - 30x-ads 已有四层架构，可作为 OS 的 Ads 子系统参考。
  - Pattern:  `/Users/nora/30x-ads/ARCHITECTURE.md:95` - tenant data 是客户级状态边界。
  - Pattern:  `/Users/nora/30x-ads/SYSTEM-OVERVIEW.md:26` - engine 模块清单。
  - External: `https://developers.openai.com/codex/concepts/customization` - AGENTS、skills、MCP、subagents 是互补层。

  Acceptance criteria (agent-executable only):
  - [ ] `test -f docs/architecture/layered-architecture.md`
  - [ ] `rg -n "L0 Operating Doctrine|L1 Tenant|L2 Data|L3 Capability|L4 Role|L5 Execution|L6 Learning" docs/architecture/layered-architecture.md`
  - [ ] `rg -n "Input|Output|State owner|Failure mode|v0" docs/architecture/layered-architecture.md`

  QA scenarios (MANDATORY - task incomplete without these):
  ```
  Scenario: all six layers are present
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && for x in "L0 Operating Doctrine" "L1 Tenant" "L2 Data" "L3 Capability" "L4 Role" "L5 Execution" "L6 Learning"; do rg -n "$x" docs/architecture/layered-architecture.md; done | tee .omo/evidence/task-2-layered-architecture.txt
    Expected: command exits 0 and prints at least one line for every layer.
    Evidence: .omo/evidence/task-2-layered-architecture.txt

  Scenario: architecture rejects dashboard-first v0
    Tool:     bash
    Steps:    rg -n "Must NOT.*dashboard|dashboard.*Must NOT|no dashboard|不做新的 dashboard" docs/architecture/layered-architecture.md | tee .omo/evidence/task-2-layered-architecture-error.txt
    Expected: command exits 0 and proves dashboard-first is explicitly excluded.
    Evidence: .omo/evidence/task-2-layered-architecture-error.txt
  ```

  Commit: YES | Message: `docs(architecture): define marketing os layers` | Files: [docs/architecture/layered-architecture.md]

- [ ] 3. Capability registry 设计

  What to do: 创建 `docs/capabilities/registry.md` 和 `docs/capabilities/capability-registry.schema.json`，把 30x SEO skills、30x Ads skills、Jetpartners operator、skill factory、semantic delta keeper 登记为 capability。每个 capability 至少包含 `id`、`trigger`、`inputs`、`outputs`、`side_effects`、`approval_gate`、`evidence_required`、`source_ref`。
  Must NOT do: 不复制整份 SKILL.md；只保存路由元数据和执行契约。

  Parallelization: Can parallel: YES | Wave 1 | Blocks: [6, 8, 9] | Blocked by: []

  References (executor has NO interview context - be exhaustive):
  - Pattern:  `/Users/nora/.agents/skills/30x-seo-plan/SKILL.md:1` - SEO strategy planning skill。
  - Pattern:  `/Users/nora/.agents/skills/30x-seo-keywords/SKILL.md:1` - keyword research capability。
  - Pattern:  `/Users/nora/.agents/skills/30x-seo-content-brief/SKILL.md:1` - content brief capability。
  - Pattern:  `/Users/nora/.agents/skills/30x-seo-content-writer/SKILL.md:1` - content/copy production capability。
  - Pattern:  `/Users/nora/.agents/skills/30x-seo-monitor/SKILL.md:1` - SEO monitoring/tracking capability。
  - Pattern:  `/Users/nora/.codex/skills/ads/AGENTS.md:1` - Ads skill family root guidance, if present.
  - Pattern:  `/Users/nora/.codex/skills/ads-audit/SKILL.md:1` - multi-platform audit capability。
  - Pattern:  `/Users/nora/.codex/skills/ads-plan/SKILL.md:1` - paid media planning capability。
  - Pattern:  `/Users/nora/.codex/skills/jetpartners-ads-operator/SKILL.md:1` - thin trigger into project-local Jetpartners role。
  - External: `https://developers.openai.com/codex/skills` - skill metadata drives discovery and activation。

  Acceptance criteria (agent-executable only):
  - [ ] `test -f docs/capabilities/registry.md`
  - [ ] `test -f docs/capabilities/capability-registry.schema.json`
  - [ ] `rg -n "30x-seo-plan|30x-seo-keywords|30x-seo-content-brief|30x-seo-content-writer|30x-seo-monitor|ads-audit|ads-plan|jetpartners-ads-operator|skill-factory|semantic-delta" docs/capabilities/registry.md`
  - [ ] `python3 -m json.tool docs/capabilities/capability-registry.schema.json >/tmp/capability-registry-schema.json`

  QA scenarios (MANDATORY - task incomplete without these):
  ```
  Scenario: registry includes required capability fields
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "id:|trigger:|inputs:|outputs:|side_effects:|approval_gate:|evidence_required:|source_ref:" docs/capabilities/registry.md | tee .omo/evidence/task-3-capability-registry.txt
    Expected: command exits 0 and prints all required field names.
    Evidence: .omo/evidence/task-3-capability-registry.txt

  Scenario: registry schema is valid JSON and rejects missing source_ref by inspection
    Tool:     bash
    Steps:    python3 -m json.tool docs/capabilities/capability-registry.schema.json > .omo/evidence/task-3-capability-registry-error.txt && rg -n '"source_ref".*"required"|\"required\".*\"source_ref\"' docs/capabilities/capability-registry.schema.json
    Expected: command exits 0 and evidence contains formatted JSON.
    Evidence: .omo/evidence/task-3-capability-registry-error.txt
  ```

  Commit: YES | Message: `docs(capabilities): define marketing capability registry` | Files: [docs/capabilities/registry.md, docs/capabilities/capability-registry.schema.json]

- [ ] 4. Role package 标准

  What to do: 创建 `docs/roles/role-package-standard.md`，定义 role package 的目录、`role.toml` 字段、`memory.md`、`skills/<role-skill>/SKILL.md`、`prompts/`、`tools/README.md`、permissions、人类批准边界和 non-goals。以 Jetpartners role package 为模板，扩展出 OS 角色：Marketing OS Director、Ads Operator、SEO Strategist、Semantic Delta Keeper、Skill Factory Curator、LazyCodex Conductor、QA Gate Reviewer。
  Must NOT do: 不把 role package 写成单个超级 prompt；每个角色必须有明确 non-goals。

  Parallelization: Can parallel: YES | Wave 1 | Blocks: [6, 7, 8, 9] | Blocked by: []

  References (executor has NO interview context - be exhaustive):
  - Pattern:  `/Users/nora/30x-ads/roles/AGENTS.md:1` - roles L2 边界。
  - Pattern:  `/Users/nora/30x-ads/roles/jetpartners-ads-operator/AGENTS.md:1` - Jetpartners role package 成员清单。
  - Pattern:  `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:11` - identity 字段。
  - Pattern:  `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:22` - non_goals 字段。
  - Pattern:  `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:36` - permissions 字段。

  Acceptance criteria (agent-executable only):
  - [ ] `test -f docs/roles/role-package-standard.md`
  - [ ] `rg -n "Marketing OS Director|Ads Operator|SEO Strategist|Semantic Delta Keeper|Skill Factory Curator|LazyCodex Conductor|QA Gate Reviewer" docs/roles/role-package-standard.md`
  - [ ] `rg -n "role.toml|memory.md|skills/.*/SKILL.md|prompts/|tools/README.md|non_goals|permissions|mutations_require_human_confirmation" docs/roles/role-package-standard.md`

  QA scenarios (MANDATORY - task incomplete without these):
  ```
  Scenario: role standard covers every required role
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && for x in "Marketing OS Director" "Ads Operator" "SEO Strategist" "Semantic Delta Keeper" "Skill Factory Curator" "LazyCodex Conductor" "QA Gate Reviewer"; do rg -n "$x" docs/roles/role-package-standard.md; done | tee .omo/evidence/task-4-role-standard.txt
    Expected: command exits 0 and prints every role.
    Evidence: .omo/evidence/task-4-role-standard.txt

  Scenario: mutation guard is mandatory
    Tool:     bash
    Steps:    rg -n "mutations_require_human_confirmation|human confirmation|人工确认|approval" docs/roles/role-package-standard.md | tee .omo/evidence/task-4-role-standard-error.txt
    Expected: command exits 0 and proves mutation approval is part of the role standard.
    Evidence: .omo/evidence/task-4-role-standard-error.txt
  ```

  Commit: YES | Message: `docs(roles): standardize marketing os role packages` | Files: [docs/roles/role-package-standard.md]

- [ ] 5. Semantic delta/GEB 契约

  What to do: 创建 `docs/semantic-delta/semantic-delta.md`、`docs/semantic-delta/semantic-delta.schema.json`，定义 GEB semantic delta 为 OS 的原子事件：`delta_id`、`tenant_id`、`source_surface`、`observed_action`、`marketing_hypothesis`、`machine_artifacts`、`semantic_artifacts`、`role_owner`、`capabilities_invoked`、`approval_state`、`qa_evidence`、`skill_candidate`、`replay_status`、`rollback_plan`。明确 L1/L2/L3 AGENTS 同构规则。
  Must NOT do: 不把 delta 设计成自由文本日志；必须可 diff、可验收、可回放、可审计。

  Parallelization: Can parallel: YES | Wave 1 | Blocks: [6, 7, 8, 9, 10] | Blocked by: []

  References (executor has NO interview context - be exhaustive):
  - Pattern:  `/Users/nora/30x-ads/AGENTS.md:1` - 项目级 AGENTS 若存在，作为 GEB L1 参考。
  - Pattern:  `/Users/nora/30x-ads/roles/jetpartners-ads-operator/AGENTS.md:1` - L2 member map 样式。
  - Pattern:  `/Users/nora/30x-ads/ARCHITECTURE.md:95` - tenant data artifacts 可成为 machine_artifacts。
  - External: `https://developers.openai.com/codex/guides/agents-md` - AGENTS.md project instruction discovery。

  Acceptance criteria (agent-executable only):
  - [ ] `test -f docs/semantic-delta/semantic-delta.md`
  - [ ] `test -f docs/semantic-delta/semantic-delta.schema.json`
  - [ ] `python3 -m json.tool docs/semantic-delta/semantic-delta.schema.json >/tmp/semantic-delta-schema.json`
  - [ ] `rg -n "delta_id|tenant_id|source_surface|observed_action|marketing_hypothesis|machine_artifacts|semantic_artifacts|role_owner|capabilities_invoked|approval_state|qa_evidence|skill_candidate|replay_status|rollback_plan" docs/semantic-delta/semantic-delta.md`
  - [ ] `rg -n "\\[PROTOCOL\\]: 变更时更新此头部，然后检查 AGENTS.md" docs/semantic-delta/semantic-delta.md`

  QA scenarios (MANDATORY - task incomplete without these):
  ```
  Scenario: semantic delta schema is parseable
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && python3 -m json.tool docs/semantic-delta/semantic-delta.schema.json | tee .omo/evidence/task-5-semantic-delta.txt
    Expected: command exits 0 and writes formatted JSON.
    Evidence: .omo/evidence/task-5-semantic-delta.txt

  Scenario: semantic delta is not a free-text log
    Tool:     bash
    Steps:    rg -n "required|properties|delta_id|qa_evidence|rollback_plan" docs/semantic-delta/semantic-delta.schema.json | tee .omo/evidence/task-5-semantic-delta-error.txt
    Expected: command exits 0 and shows typed required fields.
    Evidence: .omo/evidence/task-5-semantic-delta-error.txt
  ```

  Commit: YES | Message: `docs(delta): define geb semantic delta contract` | Files: [docs/semantic-delta/semantic-delta.md, docs/semantic-delta/semantic-delta.schema.json]

- [ ] 6. Jetpartners v0 最小闭环 runbook

  What to do: 创建 `docs/playbooks/jetpartners-v0-loop.md`，给出最小闭环：每日/每周触发 → 30x-ads observe/read-only audits → semantic delta → Ads/SEO capability routing → proposal artifact → human approval gate → permitted mutation or read-only recommendation → smoke/readback → T+7/14/30 verdict → skill factory candidate。必须覆盖 Ads 和 SEO 两条线的交叉：paid search query 发现 SEO content gap，SEO page/CRO 反馈 landing/ad copy。
  Must NOT do: 不允许直接 auto-apply；不允许把 v0 做成多租户模板；不允许省略负例/失败路径。

  Parallelization: Can parallel: YES | Wave 2 | Blocks: [11, 12] | Blocked by: [1, 2, 3, 4, 5]

  References (executor has NO interview context - be exhaustive):
  - Pattern:  `/Users/nora/30x-ads/SYSTEM-OVERVIEW.md:131` - Day 1 observe/apply flow。
  - Pattern:  `/Users/nora/30x-ads/SYSTEM-OVERVIEW.md:151` - daily drift + optimize。
  - Pattern:  `/Users/nora/30x-ads/SYSTEM-OVERVIEW.md:161` - T+7/T+14/T+30 verdict。
  - Pattern:  `/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:20` - Jetpartners review workflow。
  - Pattern:  `/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:83` - positive keyword evidence rule。
  - Pattern:  `/Users/nora/.agents/skills/30x-seo-content-brief/SKILL.md:1` - SERP brief generation。
  - Pattern:  `/Users/nora/.agents/skills/30x-seo-page/SKILL.md:1` - page SEO/CRO analysis。

  Acceptance criteria (agent-executable only):
  - [ ] `test -f docs/playbooks/jetpartners-v0-loop.md`
  - [ ] `rg -n "observe|semantic delta|capability routing|proposal|human approval|smoke|readback|T\\+7|T\\+14|T\\+30|skill factory" docs/playbooks/jetpartners-v0-loop.md`
  - [ ] `rg -n "paid search query.*SEO|SEO.*landing|CRO.*ad copy|content gap" docs/playbooks/jetpartners-v0-loop.md`

  QA scenarios (MANDATORY - task incomplete without these):
  ```
  Scenario: v0 loop contains every closed-loop step
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "observe|semantic delta|proposal|human approval|readback|T\\+7|skill factory" docs/playbooks/jetpartners-v0-loop.md | tee .omo/evidence/task-6-jetpartners-v0-loop.txt
    Expected: command exits 0 and prints each step.
    Evidence: .omo/evidence/task-6-jetpartners-v0-loop.txt

  Scenario: v0 loop blocks auto-apply
    Tool:     bash
    Steps:    rg -n "no auto-apply|不允许直接 auto-apply|human approval|人工确认" docs/playbooks/jetpartners-v0-loop.md | tee .omo/evidence/task-6-jetpartners-v0-loop-error.txt
    Expected: command exits 0 and proves mutation is gated.
    Evidence: .omo/evidence/task-6-jetpartners-v0-loop-error.txt
  ```

  Commit: YES | Message: `docs(playbooks): define jetpartners v0 loop` | Files: [docs/playbooks/jetpartners-v0-loop.md]

- [ ] 7. OMO/LazyCodex 执行协议映射

  What to do: 创建 `docs/execution/omo-lazycodex-loop.md`，把 Marketing OS 的 task lifecycle 映射到 OMO/LazyCodex：plan file、Boulder active work、parallel subagents、DoneClaim、AdversarialVerify、ledger、manual QA artifact、cleanup receipt、final gates。说明哪些角色可执行，哪些角色只审查，哪些任务必须 human approval。
  Must NOT do: 不允许把 tests-only 当完成；不允许 root/orchestrator 直接实现。

  Parallelization: Can parallel: YES | Wave 2 | Blocks: [10, 12] | Blocked by: [2, 4, 5]

  References (executor has NO interview context - be exhaustive):
  - Pattern:  `/Users/nora/.codex/plugins/cache/sisyphuslabs/omo/4.12.1/skills/start-work/SKILL.md:24` - orchestrator 不直接实现。
  - Pattern:  `/Users/nora/.codex/plugins/cache/sisyphuslabs/omo/4.12.1/skills/start-work/SKILL.md:90` - checkbox execution process。
  - Pattern:  `/Users/nora/.codex/plugins/cache/sisyphuslabs/omo/4.12.1/skills/start-work/SKILL.md:115` - verify and record evidence。
  - Pattern:  `/Users/nora/.codex/plugins/cache/sisyphuslabs/omo/4.12.1/skills/start-work/SKILL.md:127` - DoneClaim / AdversarialVerify contract。
  - Pattern:  `/Users/nora/.codex/plugins/cache/sisyphuslabs/omo/4.12.1/skills/ulw-loop/SKILL.md:20` - evidence-led non-negotiables。

  Acceptance criteria (agent-executable only):
  - [ ] `test -f docs/execution/omo-lazycodex-loop.md`
  - [ ] `rg -n "Boulder|DoneClaim|AdversarialVerify|ledger|manual QA|cleanup receipt|final gates|human approval" docs/execution/omo-lazycodex-loop.md`
  - [ ] `rg -n "tests-only.*not|不允许.*tests-only|orchestrator.*not.*implement|不直接实现" docs/execution/omo-lazycodex-loop.md`

  QA scenarios (MANDATORY - task incomplete without these):
  ```
  Scenario: execution protocol maps all OMO lifecycle concepts
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "Boulder|DoneClaim|AdversarialVerify|ledger|cleanup receipt|final gates" docs/execution/omo-lazycodex-loop.md | tee .omo/evidence/task-7-omo-loop.txt
    Expected: command exits 0 and prints all core lifecycle terms.
    Evidence: .omo/evidence/task-7-omo-loop.txt

  Scenario: tests-only completion is rejected
    Tool:     bash
    Steps:    rg -n "tests-only|Manual-QA|real surface|真实表面" docs/execution/omo-lazycodex-loop.md | tee .omo/evidence/task-7-omo-loop-error.txt
    Expected: command exits 0 and shows tests alone are insufficient.
    Evidence: .omo/evidence/task-7-omo-loop-error.txt
  ```

  Commit: YES | Message: `docs(execution): map omo lazycodex loop` | Files: [docs/execution/omo-lazycodex-loop.md]

- [ ] 8. Skill factory 流程设计

  What to do: 创建 `docs/skill-factory/skill-factory.md`，定义从“Codex 观察人工操作”到可复用 skill 的 pipeline：record scope → action trace → variable extraction → invariant extraction → safety filter → SKILL.md draft → references/scripts/assets decision → replay QA → trigger eval → registry entry → role package adoption。明确什么情况下生成 skill、更新 AGENTS、还是只写 memory。
  Must NOT do: 不允许把一次性操作都变成 skill；不允许记录 secrets；不允许没有 replay 就安装。

  Parallelization: Can parallel: YES | Wave 2 | Blocks: [11, 12] | Blocked by: [3, 4, 5]

  References (executor has NO interview context - be exhaustive):
  - Pattern:  `/Users/nora/.codex/skills/.system/skill-creator/SKILL.md:16` - skills 提供 specialized workflows/tools/domain expertise/resources。
  - Pattern:  `/Users/nora/.codex/skills/.system/skill-creator/SKILL.md:54` - skill anatomy。
  - Pattern:  `/Users/nora/.codex/skills/.system/skill-creator/SKILL.md:119` - skill creation process。
  - External: `https://developers.openai.com/codex/record-and-replay` - Codex observes actions and drafts a skill after recording。
  - External: `https://developers.openai.com/codex/use-cases/reusable-codex-skills` - start with one working example。

  Acceptance criteria (agent-executable only):
  - [ ] `test -f docs/skill-factory/skill-factory.md`
  - [ ] `rg -n "record scope|action trace|variable extraction|invariant extraction|safety filter|SKILL.md draft|replay QA|trigger eval|registry entry|role package adoption" docs/skill-factory/skill-factory.md`
  - [ ] `rg -n "do not record secrets|avoid secrets|不记录 secrets|no replay.*no install|没有 replay.*不安装" docs/skill-factory/skill-factory.md`

  QA scenarios (MANDATORY - task incomplete without these):
  ```
  Scenario: skill factory has full observe-to-skill pipeline
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "record scope|action trace|SKILL.md draft|replay QA|registry entry" docs/skill-factory/skill-factory.md | tee .omo/evidence/task-8-skill-factory.txt
    Expected: command exits 0 and prints every pipeline stage.
    Evidence: .omo/evidence/task-8-skill-factory.txt

  Scenario: skill factory blocks secret capture and unreplayed installs
    Tool:     bash
    Steps:    rg -n "secret|secrets|replay|install" docs/skill-factory/skill-factory.md | tee .omo/evidence/task-8-skill-factory-error.txt
    Expected: command exits 0 and output includes both secret redaction and replay-before-install constraints.
    Evidence: .omo/evidence/task-8-skill-factory-error.txt
  ```

  Commit: YES | Message: `docs(skill-factory): design observe to skill loop` | Files: [docs/skill-factory/skill-factory.md]

- [ ] 9. 文件/目录骨架建议

  What to do: 创建 `docs/architecture/file-directory-blueprint.md`，给出目标仓库树：`AGENTS.md`、`docs/`、`roles/`、`skills/`、`tenants/jetpartners/`、`capabilities/`、`deltas/`、`evidence/`、`playbooks/`、`schemas/`、`ops/`。每个目录一句职责、owner role、GEB 文档层级、禁止放入内容。
  Must NOT do: 不创建这些目录本身，除非任务范围已被明确改为 scaffold；本任务只写建议文档。

  Parallelization: Can parallel: YES | Wave 2 | Blocks: [12] | Blocked by: [2, 3, 4, 5]

  References (executor has NO interview context - be exhaustive):
  - Pattern:  `/Users/nora/30x-ads/ARCHITECTURE.md:95` - tenant data pattern。
  - Pattern:  `/Users/nora/30x-ads/roles/jetpartners-ads-operator/AGENTS.md:1` - role package member map。
  - Pattern:  `/Users/nora/30x-ads/SYSTEM-OVERVIEW.md:95` - tenant reports artifacts。
  - External: `https://developers.openai.com/codex/guides/agents-md` - nested instruction files as directory-specific rules。

  Acceptance criteria (agent-executable only):
  - [ ] `test -f docs/architecture/file-directory-blueprint.md`
  - [ ] `rg -n "AGENTS.md|docs/|roles/|skills/|tenants/jetpartners/|capabilities/|deltas/|evidence/|playbooks/|schemas/|ops/" docs/architecture/file-directory-blueprint.md`
  - [ ] `rg -n "Owner role|GEB|Must NOT|禁止" docs/architecture/file-directory-blueprint.md`

  QA scenarios (MANDATORY - task incomplete without these):
  ```
  Scenario: directory blueprint includes required folders
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "roles/|skills/|tenants/jetpartners/|deltas/|evidence/|playbooks/|schemas/" docs/architecture/file-directory-blueprint.md | tee .omo/evidence/task-9-directory-blueprint.txt
    Expected: command exits 0 and prints required folders.
    Evidence: .omo/evidence/task-9-directory-blueprint.txt

  Scenario: task did not create target scaffold directories
    Tool:     bash
    Steps:    test ! -d roles && test ! -d skills && test ! -d tenants && echo "scaffold not created" | tee .omo/evidence/task-9-directory-blueprint-error.txt
    Expected: command exits 0 and evidence says scaffold not created.
    Evidence: .omo/evidence/task-9-directory-blueprint-error.txt
  ```

  Commit: YES | Message: `docs(architecture): propose marketing os directory blueprint` | Files: [docs/architecture/file-directory-blueprint.md]

- [ ] 10. QA/evidence/redaction 策略

  What to do: 创建 `docs/qa/evidence-and-redaction.md`，定义每个营销动作的证据等级：read-only observation、proposal、human approval、mutation readback、SEO crawl/browser evidence、report artifact、skill replay。定义 redaction rules、secret patterns、PII boundaries、evidence file naming、cleanup receipt。
  Must NOT do: 不保存 raw tokens、credentials、auth headers、cookies、完整 PII；不接受 screenshot-only 作为 Ads mutation readback。

  Parallelization: Can parallel: YES | Wave 2 | Blocks: [11, 12] | Blocked by: [1, 5, 7]

  References (executor has NO interview context - be exhaustive):
  - Pattern:  `/Users/nora/.codex/plugins/cache/sisyphuslabs/omo/4.12.1/skills/start-work/SKILL.md:115` - evidence gates。
  - Pattern:  `/Users/nora/.codex/plugins/cache/sisyphuslabs/omo/4.12.1/skills/start-work/SKILL.md:175` - evidence hygiene and redaction。
  - Pattern:  `/Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md:44` - mutation 后 readback/smoke。
  - Pattern:  `/Users/nora/30x-ads/roles/jetpartners-ads-operator/role.toml:22` - no credentials in role package。

  Acceptance criteria (agent-executable only):
  - [ ] `test -f docs/qa/evidence-and-redaction.md`
  - [ ] `rg -n "read-only observation|proposal|human approval|mutation readback|SEO crawl|browser evidence|report artifact|skill replay|cleanup receipt" docs/qa/evidence-and-redaction.md`
  - [ ] `rg -n "token|credential|auth header|cookie|PII|redact|mask" docs/qa/evidence-and-redaction.md`

  QA scenarios (MANDATORY - task incomplete without these):
  ```
  Scenario: evidence strategy covers all evidence levels
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "read-only observation|human approval|mutation readback|skill replay" docs/qa/evidence-and-redaction.md | tee .omo/evidence/task-10-evidence-redaction.txt
    Expected: command exits 0 and prints the evidence levels.
    Evidence: .omo/evidence/task-10-evidence-redaction.txt

  Scenario: redaction rules catch secret-like terms
    Tool:     bash
    Steps:    rg -n "Bearer|Authorization|refresh_token|client_secret|cookie|PII" docs/qa/evidence-and-redaction.md | tee .omo/evidence/task-10-evidence-redaction-error.txt
    Expected: command exits 0 and shows each pattern is listed for redaction, not present as real secret value.
    Evidence: .omo/evidence/task-10-evidence-redaction-error.txt
  ```

  Commit: YES | Message: `docs(qa): define evidence and redaction gates` | Files: [docs/qa/evidence-and-redaction.md]

- [ ] 11. 30/60/90 天路线与 KPI

  What to do: 创建 `docs/roadmap/30-60-90.md`，给出三个阶段。30 天：Jetpartners v0 每日闭环、manual approval、delta registry、2 个 skill factory 成果。60 天：第二租户模板、SEO/Ads cross-channel planning、skill eval harness、monthly report integration。90 天：multi-tenant operating cadence、capability marketplace、自动 semantic delta review、role package versioning、management scorecard。每阶段写 KPI、exit criteria、风险和 rollback。
  Must NOT do: 不承诺全自动投放；不把 90 天目标写成无约束平台化。

  Parallelization: Can parallel: NO | Wave 3 | Blocks: [12] | Blocked by: [6, 8, 10]

  References (executor has NO interview context - be exhaustive):
  - Pattern:  `docs/playbooks/jetpartners-v0-loop.md` - v0 loop must drive Day 30。
  - Pattern:  `docs/skill-factory/skill-factory.md` - skill factory milestones。
  - Pattern:  `docs/qa/evidence-and-redaction.md` - evidence KPIs。
  - Pattern:  `/Users/nora/30x-ads/SYSTEM-OVERVIEW.md:196` - 30x-ads operating time savings and differentiator。

  Acceptance criteria (agent-executable only):
  - [ ] `test -f docs/roadmap/30-60-90.md`
  - [ ] `rg -n "30 天|60 天|90 天|KPI|Exit criteria|Rollback|Risk" docs/roadmap/30-60-90.md`
  - [ ] `rg -n "Jetpartners|semantic delta|skill factory|multi-tenant|role package" docs/roadmap/30-60-90.md`

  QA scenarios (MANDATORY - task incomplete without these):
  ```
  Scenario: roadmap includes three phases and exit criteria
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "30 天|60 天|90 天|Exit criteria" docs/roadmap/30-60-90.md | tee .omo/evidence/task-11-roadmap.txt
    Expected: command exits 0 and prints all three phases plus exit criteria.
    Evidence: .omo/evidence/task-11-roadmap.txt

  Scenario: roadmap blocks full auto-apply promises
    Tool:     bash
    Steps:    rg -n "不承诺全自动|no full auto-apply|human approval|人工确认" docs/roadmap/30-60-90.md | tee .omo/evidence/task-11-roadmap-error.txt
    Expected: command exits 0 and proves roadmap retains human approval boundary.
    Evidence: .omo/evidence/task-11-roadmap-error.txt
  ```

  Commit: YES | Message: `docs(roadmap): set marketing os 30 60 90 plan` | Files: [docs/roadmap/30-60-90.md]

- [ ] 12. 集成蓝图总装与评审包

  What to do: 创建 `docs/marketing-adaptive-agent-os.md` 作为总入口，汇总：1) 分层架构；2) v0 最小闭环；3) 文件/目录建议；4) agent 角色设计；5) 运行流程；6) 30/60/90 天路线。创建 `docs/reviews/blueprint-review-checklist.md`，让 reviewer 能逐项核对 Must Have/Must NOT/QA/evidence/roadmap。
  Must NOT do: 不复制所有子文档全文；总入口只给决策摘要和链接。

  Parallelization: Can parallel: NO | Wave 3 | Blocks: [] | Blocked by: [6, 7, 8, 9, 10, 11]

  References (executor has NO interview context - be exhaustive):
  - Pattern:  `docs/architecture/layered-architecture.md` - architecture source。
  - Pattern:  `docs/playbooks/jetpartners-v0-loop.md` - v0 loop source。
  - Pattern:  `docs/architecture/file-directory-blueprint.md` - directory source。
  - Pattern:  `docs/roles/role-package-standard.md` - agent roles source。
  - Pattern:  `docs/execution/omo-lazycodex-loop.md` - runtime source。
  - Pattern:  `docs/roadmap/30-60-90.md` - roadmap source。

  Acceptance criteria (agent-executable only):
  - [ ] `test -f docs/marketing-adaptive-agent-os.md`
  - [ ] `test -f docs/reviews/blueprint-review-checklist.md`
  - [ ] `rg -n "分层架构|v0 最小闭环|文件/目录建议|agent 角色设计|运行流程|30/60/90" docs/marketing-adaptive-agent-os.md`
  - [ ] `rg -n "Must have|Must NOT|QA|evidence|roadmap|Jetpartners|30x SEO|30x Ads|GEB|Skill Factory" docs/reviews/blueprint-review-checklist.md`

  QA scenarios (MANDATORY - task incomplete without these):
  ```
  Scenario: final blueprint answers the user's six requested sections
    Tool:     bash
    Steps:    mkdir -p .omo/evidence && rg -n "分层架构|v0 最小闭环|文件/目录建议|agent 角色设计|运行流程|30/60/90" docs/marketing-adaptive-agent-os.md | tee .omo/evidence/task-12-final-blueprint.txt
    Expected: command exits 0 and prints all six requested section headings.
    Evidence: .omo/evidence/task-12-final-blueprint.txt

  Scenario: review checklist blocks missing integration surfaces
    Tool:     bash
    Steps:    rg -n "Jetpartners|30x SEO|30x Ads|agent-role|LazyCodex|OMO|GEB|skill factory" docs/reviews/blueprint-review-checklist.md | tee .omo/evidence/task-12-final-blueprint-error.txt
    Expected: command exits 0 and prints every required integration surface.
    Evidence: .omo/evidence/task-12-final-blueprint-error.txt
  ```

  Commit: YES | Message: `docs(marketing-os): assemble adaptive agent os blueprint` | Files: [docs/marketing-adaptive-agent-os.md, docs/reviews/blueprint-review-checklist.md]

## Final verification wave (MANDATORY - after all implementation tasks)
> Runs in PARALLEL. ALL must APPROVE. Surface results to the caller and wait for an explicit "okay" before declaring complete.
- [ ] F1. Plan compliance audit - every task done, every acceptance criterion met
- [ ] F2. Code quality review - diagnostics clean, idioms match, no dead code
- [ ] F3. Real manual QA - every QA scenario executed with evidence captured
- [ ] F4. Scope fidelity - nothing extra shipped beyond Must-Have, nothing Must-NOT-Have introduced

## Commit strategy
- One logical change per commit. Conventional Commits (`<type>(<scope>): <subject>` body + footer).
- Atomic: every commit builds and passes tests on its own.
- No "WIP" / "fix typo squash later" commits on the final branch - clean up before merge.
- Reference the plan file path in the final commit footer: `Plan: .omo/plans/marketing-adaptive-agent-os.md`.

## Success criteria
- All Must-Have shipped; all QA scenarios pass with captured evidence; F1-F4 approved; commit history clean.
