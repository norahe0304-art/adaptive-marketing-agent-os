# workflows/
> L2 | 父级: /agents/AGENTS.md

成员清单
（空）真实 workflow 是「用协议生成的实例」，住在消费方 repo。workflow 用 id 引用 role/overlay，所以跨 repo 搬迁零改动。

真实 workflow 随各自实例住在独立消费方 repo（用 id 引用 role/overlay，跨 repo 搬迁零改动）；纯 spec 协议仓不点名任何具体租户。

边界
workflows/ 是 execution-contract 层的占位与文档锚点。workflow schema（task_graph、capability_refs、apply_lab、evidence、readback）由 capability-boundary.schema.md / cross-role-validation.md 定义；真实 workflow 由 scaffold_consumer.py 生成模板后在消费方 repo 填实。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
