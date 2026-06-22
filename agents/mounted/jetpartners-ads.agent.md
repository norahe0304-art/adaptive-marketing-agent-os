<!--
[INPUT]: Depends on ads-adaptive-operator.role.md, jetpartners-ads-operator.overlay.md, JP Ads workflows, 30x-ads role package, and the global jetpartners-ads-operator Codex skill trigger.
[OUTPUT]: Provides the mounted Jetpartner Ads Agent composition: role, tenant attachment, playbooks, runtime bindings, entrypoints, evidence roots, approval gates, and GEB learning route.
[POS]: mounted first real Adaptive Marketing Agent OS agent; product-facing composition consumed by Codex before running JP Ads work.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Jetpartner Ads Agent

This is the mounted JP Ads Agent. It is not a base role and not a standalone skill. It composes the reusable Ads role with the Jetpartner tenant attachment, two playbooks, and the existing 30x-ads runtime.

```yaml
mounted_agent:
  identity:
    id: jetpartners-ads-agent
    name: Jetpartner Ads Agent
    version: 0.1.0
    domain: Ads
    tenant: Jetpartner
    status: mounted_v1

  product_contract:
    user_facing_model: "install role, attach tenant, run playbook"
    role: agents/roles/ads-adaptive-operator.role.md
    tenant_attachment: agents/overlays/jetpartners-ads-operator.overlay.md
    primary_runtime: /Users/nora/30x-ads
    legacy_role_package: /Users/nora/30x-ads/roles/jetpartners-ads-operator
    entrypoint_skill: /Users/nora/.codex/skills/jetpartners-ads-operator/SKILL.md
    trigger: "$jetpartners-ads-operator"
    primary_host: codex
    optional_host_adapters:
      - portal
      - slack
      - hermes

  host_runtime_policy:
    default_host: codex
    reason: "JP Ads work needs repo-local evidence, live file inspection, iterative operator conversation, and 30x-ads command/readback loops; Codex is the primary surface for that."
    hermes_role: optional_adapter
    hermes_allowed_for:
      - Slack request intake
      - notification delivery
      - approval receipt handoff
      - readback posting
    hermes_not_allowed_for:
      - replacing Codex as the reasoning/runtime core
      - storing JP tenant truth
      - bypassing workflow approval gates
      - applying Google Ads mutations

  boot_sequence:
    always_read:
      - agents/mounted/jetpartners-ads.agent.md
      - agents/roles/ads-adaptive-operator.role.md
      - agents/overlays/jetpartners-ads-operator.overlay.md
      - /Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md
      - /Users/nora/30x-ads/roles/jetpartners-ads-operator/skills/ads-operator/SKILL.md
    select_playbook_by_intent:
      daily maintenance:
        workflow: agents/workflows/jetpartners-ads-daily-maintenance.workflow.md
        legacy_surface: /Users/nora/30x-ads/.claude/skills/ads-daily/SKILL.md
      account review:
        workflow: agents/workflows/jetpartners-ads-readonly-review.workflow.md
      client update:
        optional_prompt: /Users/nora/30x-ads/roles/jetpartners-ads-operator/prompts/client-update.md
      live command guidance:
        optional_tools: /Users/nora/30x-ads/roles/jetpartners-ads-operator/tools/README.md

  playbooks:
    daily-maintenance:
      name: Daily Maintenance
      workflow_contract: agents/workflows/jetpartners-ads-daily-maintenance.workflow.md
      default_mode: propose
      runtime_prep: /Users/nora/30x-ads/tenants/jetpartners/scripts/daily-9-30am.sh
      source_artifacts:
        morning_brief: /Users/nora/30x-ads/tenants/jetpartners/reports/morning-brief-<YYYY-MM-DD>.md
        actions: /Users/nora/30x-ads/tenants/jetpartners/reports/actions-<YYYY-MM-DD>.json
        monitor: /Users/nora/30x-ads/tenants/jetpartners/reports/monitor-<YYYY-MM-DD>.md
        lead_quality: /Users/nora/30x-ads/tenants/jetpartners/reports/lead-quality-<YYYY-MM-DD>.json
        conflicts: /Users/nora/30x-ads/tenants/jetpartners/reports/conflicts-<YYYY-MM-DD>.json
        account_changes: /Users/nora/30x-ads/tenants/jetpartners/reports/account-changes-<YYYY-MM-DD>.json
      allowed_apply_lab: jp-ads-daily-apply-lab-v1
      approval_required_before:
        - Google Ads mutation
        - Supabase mutation
        - tenant memory promotion
      readback_required:
        - decision summary
        - changed-object readback when apply_lab executes
        - conflict audit reference when negatives change
        - dashboard URL
        - GEB learning route
    account-review:
      name: Account Review
      workflow_contract: agents/workflows/jetpartners-ads-readonly-review.workflow.md
      default_mode: propose
      source_artifacts:
        dashboard: https://reports.30x.company/jetpartners/latest
        tenant_root: /Users/nora/30x-ads/tenants/jetpartners
        role_memory: /Users/nora/30x-ads/roles/jetpartners-ads-operator/memory.md
      allowed_apply_lab: jp-ads-apply-lab-v1
      approval_required_before:
        - Google Ads mutation
        - budget change
        - bidding change
        - ad copy change
        - targeting change
        - conversion tracking change
      readback_required:
        - evidence used
        - recommendation
        - approval status
        - what was not changed
        - GEB learning route

  runtime_boundaries:
    tenant_id: jetpartners
    timezone: America/New_York
    report_url: https://reports.30x.company/jetpartners/latest
    default_mode: propose
    read_allowed_without_approval:
      - local date-stamped report artifacts
      - 30x-ads role memory and tools docs
      - client-safe dashboard
      - dry-run output
    apply_never_allowed_without:
      - active ApprovalReceipt
      - runtime_security_review_id
      - exact account/campaign/ad group scope
      - pre-apply evidence
      - rollback note
      - post-apply readback
    forbidden_storage:
      - credentials
      - OAuth tokens
      - raw CRM exports
      - unbounded chat transcripts
      - transient campaign metrics without source path

  geb_learning:
    default_post_run_route: tenant_memory_patch
    route_rules:
      tenant_memory_patch: stable JP-specific truth or source pointer
      workflow_patch: repeated JP playbook step, gate, failure behavior, or readback change
      skill_candidate: repeated atomic action worth packaging
      ads_playbook_patch: Ads pattern proven reusable beyond JP
      protocol_update: shared OS constraint requiring cross-role proof
    required_fields:
      - evidence_url_or_path
      - owner
      - last_verified_at
      - review_after
      - contradiction_check
```

## Agent Rule

When `$jetpartners-ads-operator` fires, load this mounted agent first. Then load the base role, JP tenant attachment, selected playbook workflow, and 30x-ads project-local memory. The global skill is only the doorway; this file is the mounted agent contract.
