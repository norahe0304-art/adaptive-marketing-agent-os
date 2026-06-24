# mounted/
> L2 | 父级: /agents/AGENTS.md

成员清单
（空）真实 mounted agent 是「用协议生成的实例」，住在消费方 repo，不住协议 repo。
样例：JP Ads Agent 已搬到 30x-ads/agents/jetpartners-ads.agent.md。

边界
mounted/ 是 assembly 层的占位与文档锚点。装配规则由 protocol-consumption.contract.md 定义；mounted agent = 一个 base role + 一个 tenant attachment + 命名 playbooks，adaptive/installable/detachable，runtime 由用户选择。参考 role 见 roles/，活体实例见消费方 repo。

依赖
mounted agent（在消费方 repo）-> protocol/ 里的 base role + 本地 tenant attachment + 本地 workflow playbook contracts + work substrate。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
