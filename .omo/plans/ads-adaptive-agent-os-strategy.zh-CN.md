# Ads Adaptive Agent OS - Strategy Blueprint

## 0. 一句话战略
先做 **Ads Adaptive Agent OS**，不是泛 Marketing OS。

用一个可复用的 Ads Agent 骨架，挂载 Jetpartner 作为第一个 tenant overlay，复用 `30x-ads` 作为确定性执行引擎，用 OMO 保证执行纪律，用 GEB 保证经验回写，用 Record & Replay 把稳定 session 沉淀成 skill candidate。

```text
Ads Adaptive Agent OS
= Base Ads Agent
+ Tenant Overlay
+ 30x Ads Domain Engine
+ agent-role Package Boundary
+ Flyte-style Typed Workflow
+ OMO Execution Governance
+ GEB Semantic Memory
+ Record & Replay Skill Factory
```

## 1. 战略判断
之前失败的根因不是 agent 不够聪明，而是边界没有锁死：

```text
skills 很多，但没有统一 routing / ownership
tenant facts 和 agent instructions 混在一起
session 学习没有分流，容易变成 skill 爆炸
执行没有 typed workflow，靠聊天临场组织
验证没有 readback / evidence gate
```

这次的战略不是“多做几个 agent”，而是建立一个能持续学习的 Ads 操作系统。

## 2. 战略北极星
北极星：

```text
让 Ads Agent 每做完一次真实运营动作，
都能留下可验证的 evidence、
可审计的 semantic delta、
可复用的 workflow/skill candidate，
并且不污染 base agent。
```

第一条证明链路：

```text
Jetpartner Ads Search Term / Lead Quality Review
```

原因：

```text
有真实客户：Jetpartner
有真实引擎：30x-ads
有真实真值：qualified lead > raw lead
有真实权限边界：mutation needs human approval
有真实报告表面：reports.30x.company/jetpartners/latest
有可沉淀 SOP：search term hygiene / negative proposal / lead-quality explanation
```

## 3. 核心分层
只保留三层战略模型：

```text
Truth Layer
  相信什么事实，边界是什么。

Work Layer
  谁做，按什么 workflow 做，用什么 engine 做，如何验证。

Learning Layer
  做完以后学到了什么，写回哪里，是否能变成 skill。
```

对应到 Ads Agent：

```text
Truth:
  Tenant overlay + industry overlay + role memory

Work:
  agent-role + capability registry + typed workflow + 30x-ads + OMO

Learning:
  GEB semantic delta + Record & Replay + skill patch/new skill candidate
```

## 4. 各参考项目怎么用

| 参考物 | 吸收什么 | 放在哪一层 | 明确不用什么 |
| --- | --- | --- | --- |
| `agent-roles-spec` | role package 边界：identity、memory、skills、tools、permissions、lifecycle | Work / Packaging | 不照搬成复杂包管理器；先对齐现有 `role.toml` |
| OMO / LazyCodex | plan、delegate、evidence、QA、review gate、verified completion | Work / Execution Governance | 不让 OMO 变成 Ads engine；它管执行纪律，不管广告 API 细节 |
| GEB | L1/L2/L3 分形文档、semantic delta、文档与执行同构 | Learning / Memory | 不把所有 tenant facts 塞进 L1-L3；L1-L3 只管 Ads Agent 骨架 |
| Flyte | typed task、workflow DAG、launch plan、execution record 的抽象 | Work / Workflow Graph | v0 不部署 Flyte、不上 Kubernetes、不建 queue/database |
| Trellis | task/spec/workspace/journal/finish writeback 的学习闭环 | Learning / Session Persistence | 不照搬 Trellis runtime；只学“任务结束后把 learnings 写回 spec” |
| agency-agents | agent catalog 的目录化方法：专职角色、交付物、成功标准 | Work / Role Catalog | 不导入 232 个 agents；只学它如何定义单个岗位 |
| Codex Record & Replay | 观察人工操作，生成 reusable skill draft，再 replay 验证 | Learning / Skill Factory | 不让每次 session 自动变新 skill；先变 delta，稳定后才变 skill candidate |
| 30x-ads | Google Ads / Supabase / report 的确定性执行引擎 | Work / Domain Engine | 不把业务规则散落到 prompt；高风险动作必须走 engine + dry-run/readback |
| 30x SEO skills | 未来 cross-channel signal 和 SEO/AEO 扩展能力 | Future Capability | v0 不作为主线，不混进 Ads Agent 第一闭环 |
| Jetpartner | 第一个 mounted tenant，提供真实 truth、memory、permissions、report surface | Truth / Tenant Overlay | 不写死进 base Ads Agent |

## 5. 为什么一定需要 30x-ads domain engine
Agent 负责判断、编排、解释；domain engine 负责确定性执行。

没有 `30x-ads`，Ads Agent 只能聊天：

```text
看一点上下文
→ 猜账户状态
→ 写建议
→ 人工复制
→ 没有 schema
→ 没有 dry-run
→ 没有 readback
```

有 `30x-ads`，才是 OS：

```text
TENANT_ID=jetpartners pnpm observe
→ 生成 report artifacts
→ agent 基于 qualified lead truth 诊断
→ 生成 proposal / blueprint candidate
→ human approval
→ dry-run / apply
→ readback / conflict audit / report
→ semantic delta
```

所以战略分工是：

```text
agent-role:
  谁负责，权限是什么，记忆是什么，不能做什么。

OMO:
  怎么把任务按证据做完。

GEB:
  做完以后怎么让系统变聪明。

30x-ads:
  怎么真实、安全、可回滚地操作广告系统。
```

## 6. GEB L1-L3 怎么放
这里必须锁死：GEB L1-L3 不是 tenant 仓库。

```text
L1 = Ads Adaptive Agent Constitution
  这个 base agent 的原则、边界、目录、学习协议。

L2 = Ads Module Map
  search-term-review、lead-quality-review、budget-review 等模块地图。

L3 = Skill / Workflow Contract
  单个 skill/workflow 的 INPUT、OUTPUT、POS、APPROVAL、EVIDENCE、DELTA。
```

tenant 作为 runtime overlay：

```text
tenants/jetpartner/
  truth.md
  memory.md
  permissions.toml
  launchplans/
  approved-examples/
```

这保证未来有更多客户时：

```text
Base Ads Agent 不膨胀。
Tenant overlay 可替换。
Industry overlay 可复用。
Session delta 可审计。
```

## 7. 运行逻辑
一次真实任务这样跑：

```text
User asks:
  看看 Jetpartner 最近广告有没有垃圾流量

1. Resolve Tenant Overlay
  读取 Jetpartner truth / memory / permissions。

2. Select Role Package
  选择 ads-adaptive-agent + jetpartners-ads-operator overlay。

3. Build Typed Workflow
  search-term-review DAG:
    observe_artifacts
    classify_intent
    join_qualified_lead_truth
    draft_negative_keyword_proposal
    approval_gate
    readback_plan
    semantic_delta

4. Route Capabilities
  observe_artifacts -> 30x-ads
  classify_intent -> Ads skill + tenant memory
  proposal -> role package prompt/skill
  semantic_delta -> GEB keeper

5. Execute With OMO Discipline
  explorer 查本地事实
  librarian 查外部依据
  metis 找风险
  plan 写 run plan
  momus 审 plan
  executor 执行
  QA/gate reviewer 验收

6. Learn
  session delta 分类：
    Jetpartner-only -> tenant memory
    private aviation 通用 -> industry playbook
    ads workflow 通用 -> skill patch
    新稳定流程 -> new skill candidate
    系统规则 -> protocol / GEB
```

## 8. v0 锁定范围
v0 只做：

```text
Jetpartner Ads Read-only Review Loop
```

输入：

```text
Jetpartner memory
existing report artifacts
30x-ads command surface
current role package
private aviation bad-intent rules
```

输出：

```text
proposal
evidence list
approval gate
semantic delta
skill candidate decision
```

不输出：

```text
new dashboard
auto-applied Google Ads changes
full Marketing OS
multi-tenant marketplace
SEO automation
unverified new skill
```

## 9. v1 / v2 扩展路径
v1：把 v0 的 read-only loop 变成可重复 workflow。

```text
search-term-review
lead-quality-review
budget-review
conversion-tracking-review
client-update-draft
```

v2：抽象出可复用 tenant + industry overlay。

```text
private-aviation overlay
local-service overlay
B2B-lead-gen overlay
ecommerce overlay
```

v3：再考虑 Marketing OS。

```text
Ads Agent
SEO Agent
Content Agent
Lifecycle Agent
Analytics Agent
```

但 Ads Agent 必须先跑通，否则 Marketing OS 没有地基。

## 10. 最关键的战略取舍
这次必须牺牲“大而全”，换取“第一条闭环真实可跑”。

锁定：

```text
先做 Ads。
先做 Jetpartner。
先做 read-only。
先做 evidence。
先做 semantic delta。
先做 skill candidate，不做自动 skill 安装。
```

不锁死：

```text
未来是否接 SEO。
未来是否多租户。
未来是否上真正 workflow runner。
未来是否把 agent-role-spec 做成正式 package manager。
```

战略判断：

```text
如果 Jetpartner Ads Agent 能跑通：
  你就拥有一个可复制的 adaptive operator pattern。

如果一开始做 Marketing OS：
  你会再次落回 prompt、skills、memory、tenant facts 混杂的旧坑。
```

## 11. 最终蓝图
最终形态不是一个 agent，而是一套 agent 操作协议：

```text
Ads Adaptive Agent OS

Base Agent:
  ads-adaptive-agent

Runtime Context:
  tenant overlay
  industry overlay
  run context

Execution:
  typed workflow
  OMO verification
  30x-ads engine

Learning:
  semantic delta
  memory patch
  skill patch
  Record & Replay candidate
```

这就是当前战略蓝图。
