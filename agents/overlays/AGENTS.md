# overlays/
> L2 | 父级: /agents/AGENTS.md

成员清单
jetpartners-ads-operator.overlay.md: Jetpartner Ads overlay，mounts on ads-adaptive-operator and stores Jetpartner operating contracts, source pointers, and runtime bindings.
caylent-event-operator.overlay.md: Caylent Event overlay，mounts on event-adaptive-operator and stores Caylent operating contracts, source pointers, Slack approval/readback surface, and runtime bindings.

边界
overlays/ stores stable tenant operating contracts and concrete runtime bindings only. No unbounded transcripts, CRM dumps, raw campaign history, credentials, or provider secrets.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
