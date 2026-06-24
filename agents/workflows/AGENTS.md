# workflows/
> L2 | 父级: /agents/AGENTS.md

成员清单
jetpartners-ads-readonly-review.workflow.md: Internal workflow contract behind the JP Ads review playbook, covering lead quality/search-term review plus approval-gated apply lab.
jetpartners-ads-daily-maintenance.workflow.md: Internal workflow contract behind the JP Ads daily maintenance playbook, mapping 30x-ads morning brief, decision queue, apply-lab gate, dashboard readback, and learning route.
jetpartners-ads-keyword-hygiene.workflow.md: Internal workflow contract behind the JP Ads keyword hygiene playbook, covering search-term triage, negatives/positives, DataForSEO evidence, conflict audits, and GEB tail updates.
jetpartners-ads-account-health-check.workflow.md: Internal workflow contract behind the JP Ads account health check playbook, covering readiness probes, drift scans, blocker diagnosis, owner actions, and GEB tail updates.
jetpartners-ads-monthly-report.workflow.md: Internal workflow contract behind the JP Ads monthly report playbook, covering month-window evidence, client-facing narrative, delivery gate, readback, and GEB tail updates.
caylent-event-launch.workflow.md: Internal workflow contract behind the Caylent Event launch playbook, covering HubSpot draft kit, approval loop, and draft-asset apply lab.

边界
workflows/ defines machine-readable execution contracts behind role playbooks. A workflow may call skills and define approval-gated `apply_lab` steps, but it does not execute platform mutations itself.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
