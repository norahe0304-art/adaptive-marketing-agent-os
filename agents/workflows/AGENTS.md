# workflows/
> L2 | 父级: /agents/AGENTS.md

成员清单
caylent-event-launch.workflow.md: Internal workflow contract behind the Caylent Event launch playbook, covering HubSpot draft kit, approval loop, and draft-asset apply lab. In-repo Event-domain proof.

注：tenant 专属 workflow 随实例搬到消费方 repo。JP Ads 的五个 workflow 已搬到 30x-ads/agents/workflows/。workflow 用 id 引用 role/overlay，所以跨 repo 搬迁零改动。

边界
workflows/ defines machine-readable execution contracts behind role playbooks. A workflow may call skills and define approval-gated `apply_lab` steps, but it does not execute platform mutations itself. Tenant-specific workflows live in consumer repos; only neutral/domain-proof workflows stay here.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
