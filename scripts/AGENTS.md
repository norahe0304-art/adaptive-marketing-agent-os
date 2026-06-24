# scripts/
> L2 | 父级: /AGENTS.md

成员清单
validate_roles.py: 角色包契约校验器，role-package.schema.md 的执行相；校验 agents/roles/*.role.md 与 agents/examples/*-role.fixture.md。
validate_mounted_agents.py: Mounted agent 装配校验器；校验 agents/mounted/*.agent.md（或 --root/--glob 指向消费方 repo）是否接上 role、tenant attachment、playbook、work_substrate、entrypoints；空 mounted 优雅返回 0（spec repo）。
scaffold_consumer.py: 生成回路的「手」；读 agents/templates/ + 协议树，按场景参数在 <dest> 盖出 pin 好协议的最小可校验 agent 实例骨架，内容留 TODO 给 runtime 填。
githooks/pre-commit: 提交前闸门，调用 validate_roles.py 与 validate_mounted_agents.py；违约阻断提交。经 `git config core.hooksPath scripts/githooks` 生效。

边界
scripts/ 只做文档契约的自动审判，不含运行时业务逻辑、不连任何营销平台、不写 provider 配置。

依赖
validate_roles.py -> agents/protocols/role-package.schema.md (契约定义)
validate_mounted_agents.py -> agents/mounted/*.agent.md 或消费方 repo (装配定义)
scaffold_consumer.py -> agents/templates/ + 协议树 (生成回路的脚手架)
githooks/pre-commit -> validate_roles.py + validate_mounted_agents.py (执行审判)

安装
clone 后执行一次：`git config core.hooksPath scripts/githooks`

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
