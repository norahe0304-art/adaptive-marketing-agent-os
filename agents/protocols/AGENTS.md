# protocols/
> L2 | 父级: /agents/AGENTS.md

成员清单
role-package.schema.md: Role package schema，定义 identity/instructions/skills/memory/tools/plugins/host_adapters/lifecycle/evidence/approval/learning/versioning，并校验 role surface 字段。
capability-boundary.schema.md: Capability and MCP boundary，定义 read/observe/dry_run/propose 默认权限、workflow-scoped apply_lab、surface record 字段。
approval-evidence.schema.md: Approval and evidence schema，定义 ApprovalReceipt、EvidenceArtifact、apply_lab run evidence、approval_state 与 action_hash/scope/expiry/revocation 硬契约。
host-adapter.interface.md: Host adapter interface，定义 slack/cli/portal/cron/api/codex 的 entrypoints、identity、session、approval、evidence handoff。
omo-execution-governance.md: OMO execution governance，定义 trigger/self-check/plan/delegate/evidence/QA/review/readback。
geb-semantic-delta.md: GEB semantic and structural delta，定义 learning placement 与 L1/L2/L3 同构回写。
agent-onboarding.contract.md: Generic marketing agent onboarding contract，定义未来 agent 接入表。
cross-role-validation.md: Cross-role validation，证明 shared protocol 与 domain-specific differences 可分离。

边界
protocols/ defines shared semantics only. Domain-specific facts belong in roles/, overlays/, and workflows/.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
