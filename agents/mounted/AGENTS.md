# mounted/
> L2 | 父级: /agents/AGENTS.md

成员清单
jetpartners-ads.agent.md: Mounted JP Ads Agent，组合 Ads base role、Jetpartner tenant attachment、30x-ads work substrate、五个 playbooks、中立 entrypoints，并声明 adaptive/installable/detachable 契约；runtime 由用户选择，协议不写死。

边界
mounted/ stores assembled agent definitions. A mounted agent wires one base role to one tenant attachment and named playbooks; it is adaptive, installable, and detachable, but does not redefine shared protocol, duplicate tenant memory, store secrets, or execute platform mutations.

依赖
mounted agent -> roles/ base role + overlays/ tenant attachment + workflows/ playbook contracts + external work-substrate source pointers.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
