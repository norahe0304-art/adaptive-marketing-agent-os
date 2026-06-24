# protocols/
> L2 | 父级: /agents/AGENTS.md

成员清单
role-package.schema.md: Role guardrail，定义 base role 的 identity、instructions、abstract surfaces、memory、evidence、approval、learning。
capability-boundary.schema.md: Capability guardrail，定义 playbook workflow step 的 mode 与 capability_refs，不作为独立安装层。
approval-evidence.schema.md: Approval/evidence guardrail，定义 ApprovalReceipt、EvidenceArtifact 与 apply_lab 证据硬契约。
omo-execution-governance.md: OMO execution guardrail，定义 trigger/self-check/plan/delegate/evidence/QA/review/readback。
geb-semantic-delta.md: GEB learning guardrail，定义 role、tenant attachment、playbook workflow、skill candidate 与 L1/L2/L3 的 post-run delta 回写。
agent-onboarding.contract.md: Role-first onboarding，定义 role、tenant attachments、playbooks 的接入模型。
install-mount-lifecycle.protocol.md: Packaging note，定义 install role、attach tenant、run playbook、detach tenant 的最小拆卸语义。
cross-role-validation.md: Validation guardrail，证明 Ads/Event 共用 role-first 模型且 playbook 不越权。

边界
protocols/ defines internal guardrails only. User-facing design remains one role that can attach tenants and run playbooks. Domain-specific facts belong in roles/, overlays/, and workflows/.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
