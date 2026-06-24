# overlays/
> L2 | 父级: /agents/AGENTS.md

成员清单
（空）真实 tenant overlay 是「用协议生成的实例」，住在消费方 repo，不住协议 repo。schema 证明见 examples/ 的 *-role.fixture.md。

已搬出的实例：JP Ads -> 30x-ads/agents/jetpartners-ads.overlay.md；Caylent Event -> /Users/nora/caylent-event/agents/caylent-event.overlay.md。

边界
overlays/ 是 tenant-attachment 层的占位与文档锚点。overlay schema 与边界由 role-package.schema.md / protocol-consumption.contract.md 定义；真实 overlay 由 scaffold_consumer.py 在消费方 repo 生成。No credentials, secrets, raw dumps anywhere.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
