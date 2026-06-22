# mounted/
> L2 | 父级: /agents/AGENTS.md

成员清单
jetpartners-ads.agent.md: Mounted JP Ads Agent，组合 Ads base role、Jetpartner tenant attachment、30x-ads runtime、daily maintenance/account review playbooks、Codex skill entrypoint。

边界
mounted/ stores assembled agent definitions. A mounted agent wires one base role to one tenant attachment and named playbooks; it does not redefine shared protocol, duplicate tenant memory, store secrets, or execute platform mutations.

依赖
mounted agent -> roles/ base role + overlays/ tenant attachment + workflows/ playbook contracts + external runtime source pointers.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
