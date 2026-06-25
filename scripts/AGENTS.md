# scripts/
> L2 | 父级: /AGENTS.md

成员清单
validate_roles.py: 角色包契约校验器，role-package.schema.md 的执行相；校验 agents/roles/*.role.md(参考 role 库)。
validate_mounted_agents.py: Mounted agent 装配校验器；校验 agents/mounted/*.agent.md（或 --root/--glob 指向消费方 repo）是否接上 role、tenant attachment、work_substrate、entrypoints、run_state_contract、proactive learning gate，且 mount playbooks ⊆ role playbooks（子集，非相等；role 空声明则显式打印 note 并跳过 surface 检查；无 tenant 特例）；空 mounted 优雅返回 0（spec repo）。
scaffold_consumer.py: 生成回路的「手」；读 agents/templates/ + 协议树，按场景参数在 <dest> 盖出 pin 好协议的最小可校验 agent 实例骨架与 L2 地图，内容留 TODO 给 runtime 填。
build_skill.py: 第三条分发入口构建器；把 scaffolder + templates + 协议快照打包成自包含 skill bundle(含 SKILL.md)，别人装上就能长 agent，无需访问本 repo。输出默认 dist/(gitignored)。
dry_run_agent.py: Runtime warm-up 校验器；读取消费方 mounted agent、role、overlay、workflow 与 run-state ledger，模拟含 proactive learning verdict 的 boot/readback skeleton，不调用外部系统、不写 provider。
check_run_conformance.py: 行为一致性回放器；审判一次真运行的 run_readback（agents/state/runs/*.readback.yaml）是否守住 propose-first/apply 门禁、no-silent-success verdict、verdict 完整性、无明文密钥。结构校验管"契约写得对"，本器管"运行做得对"。随 scaffolder vendor 进 consumer；诚实限制:判 readback 声明,非 ground truth。
check_version_sync.py: 版本同构闸门；以 repo-root VERSION 为唯一真相，扫描所有 git 追踪文件(排除 .omo/ 历史证据)的 vX.Y.Z 字面量，任一漂移即非零退出。`version-sync: ignore` 行级豁免历史引用。
check_schema_sync.py: schema 同构闸门；让 validate_roles.py 的 REQUIRED_FIELDS/ALLOWED_PROFILES 与 role-package.schema.md(role_package 键，`# optional` 标记可选)/capability-boundary.schema.md(capability_profiles)互相审判，漂移即非零退出。是 schema 化触发器的自我引爆装置。
githooks/pre-commit: 提交前闸门，依次调用 validate_roles.py、validate_mounted_agents.py、check_version_sync.py、check_schema_sync.py；违约阻断提交。经 `git config core.hooksPath scripts/githooks` 生效。

边界
scripts/ 只做文档契约的自动审判与 dry-run 热身，不含运行时业务逻辑、不连任何营销平台、不写 provider 配置。

依赖
validate_roles.py -> agents/protocols/role-package.schema.md (契约定义)
validate_mounted_agents.py -> agents/mounted/*.agent.md 或消费方 repo (装配定义) + base role 的 playbooks.available (声明面真相源)
scaffold_consumer.py -> agents/templates/ + 协议树 + VERSION (生成回路的脚手架;版本默认读 VERSION)
dry_run_agent.py -> 消费方 mounted agent + workflow + agents/state + proactive learning gate (无副作用 boot 模拟)
check_run_conformance.py -> 消费方 agents/state/runs/*.readback.yaml (审判对象) + run-state-ledger.protocol.md (行为不变量真相源)
check_version_sync.py -> VERSION (唯一真相) + git ls-files (审判对象)
check_schema_sync.py -> validate_roles.py (常量) + role-package.schema.md + capability-boundary.schema.md (契约真相源)
githooks/pre-commit -> validate_roles.py + validate_mounted_agents.py + check_version_sync.py + check_schema_sync.py (执行审判)

安装
clone 后执行一次：`git config core.hooksPath scripts/githooks`

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
