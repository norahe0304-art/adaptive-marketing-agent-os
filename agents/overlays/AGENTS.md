# overlays/
> L2 | 父级: /agents/AGENTS.md

成员清单
caylent-event-operator.overlay.md: Caylent Event overlay，mounts on event-adaptive-operator and stores Caylent operating contracts, source pointers, Slack approval/readback surface, and runtime bindings. In-repo Event-domain proof.

注：真实 tenant overlay 是「用协议生成的实例」，随实例搬到消费方 repo。JP Ads overlay 已搬到 30x-ads/agents/jetpartners-ads.overlay.md。

边界
overlays/ stores stable tenant operating contracts and concrete runtime bindings only. No unbounded transcripts, CRM dumps, raw campaign history, credentials, or provider secrets. Tenant overlays live in consumer repos; only neutral/domain-proof overlays stay here.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
