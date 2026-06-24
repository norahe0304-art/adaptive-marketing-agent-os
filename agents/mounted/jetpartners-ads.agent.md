<!--
[INPUT]: Depends on ads-adaptive-operator.role.md, jetpartners-ads-operator.overlay.md, JP Ads workflows, 30x-ads role package, and the global jetpartners-ads-operator Codex skill trigger.
[OUTPUT]: Provides the mounted Jetpartner Ads Agent composition: role, tenant attachment, playbooks, runtime bindings, entrypoints, evidence roots, approval gates, and GEB learning route.
[POS]: mounted first real Adaptive Marketing Agent OS agent; product-facing composition consumed by Codex before running JP Ads work.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Jetpartner Ads Agent

This is the mounted JP Ads Agent. It is not a base role and not a standalone skill. It composes the reusable Ads role with the Jetpartner tenant attachment, five playbooks, and the existing 30x-ads runtime.

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
    work_substrate: /Users/nora/30x-ads
    legacy_role_package: /Users/nora/30x-ads/roles/jetpartners-ads-operator
    entrypoints:
      # Doorways an agent runtime can use to reach this composition.
      # Which runtime runs it (Codex, Claude Code, Claude Tag, ...) is the user's choice, never a protocol member.
      - /Users/nora/.codex/skills/jetpartners-ads-operator/SKILL.md

  adaptivity_contract:
    adaptive: true
    rule: "Every playbook run ends with readback plus GEB delta routing; stable deltas patch tenant memory, workflow tails, playbook rules, skill candidates, or protocol."
    updates_allowed:
      - tenant memory record
      - playbook workflow tail
      - workflow evidence gate
      - workflow failure behavior
      - readback shape
      - skill candidate
      - protocol proposal
    updates_forbidden:
      - silent base role mutation from JP-only evidence
      - hidden prompt drift
      - unbounded transcript storage
      - live mutation permission expansion without protocol review
    promotion_requires:
      - evidence_url_or_path
      - owner
      - last_verified_at
      - review_after
      - contradiction_check

  install_contract:
    installable: true
    unit: mounted_agent
    installs:
      - mounted agent definition
      - base role reference
      - tenant attachment reference
      - playbook workflow references
      - entrypoint skill reference
    does_not_install:
      - credentials
      - provider account secrets
      - live mutation permission
      - raw CRM export
      - unbounded tenant history
    install_check:
      - role file exists
      - tenant attachment file exists
      - playbook workflow files exist
      - entrypoint skill exists
      - primary runtime exists

  detach_contract:
    detachable: true
    detaches:
      - tenant runtime binding
      - entrypoint projection
    preserves:
      - base role
      - workflow contracts
      - required audit evidence
      - approved learning deltas
    removal_readback_required:
      - active workflows
      - runtime bindings revoked
      - entrypoint projections removed
      - evidence archives retained
      - tenant memory retained or exported
      - blocked reason
    blocked_when:
      - active apply_lab run
      - pending approval receipt
      - unresolved evidence handoff

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
      keyword hygiene:
        workflow: agents/workflows/jetpartners-ads-keyword-hygiene.workflow.md
      account health check:
        workflow: agents/workflows/jetpartners-ads-account-health-check.workflow.md
      monthly report:
        workflow: agents/workflows/jetpartners-ads-monthly-report.workflow.md
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
    keyword-hygiene:
      name: Keyword Hygiene
      workflow_contract: agents/workflows/jetpartners-ads-keyword-hygiene.workflow.md
      default_mode: propose
      source_artifacts:
        keyword_inventory: /Users/nora/30x-ads/tenants/jetpartners/reports/keyword-inventory-<YYYY-MM-DD>.md
        conflicts: /Users/nora/30x-ads/tenants/jetpartners/reports/conflicts-<YYYY-MM-DD>.json
        actions: /Users/nora/30x-ads/tenants/jetpartners/reports/actions-<YYYY-MM-DD>.json
        tenant_root: /Users/nora/30x-ads/tenants/jetpartners
      allowed_apply_lab: jp-ads-keyword-apply-lab-v1
      approval_required_before:
        - negative keyword mutation
        - positive keyword mutation
        - tenant memory promotion
      readback_required:
        - terms reviewed
        - terms applied
        - terms skipped or protected
        - conflict audit result
        - GEB learning route
    account-health-check:
      name: Account Health Check
      workflow_contract: agents/workflows/jetpartners-ads-account-health-check.workflow.md
      default_mode: propose
      source_artifacts:
        preflight: /Users/nora/30x-ads/scripts/preflight.ts
        observe: /Users/nora/30x-ads/scripts/observe.ts
        monitor: /Users/nora/30x-ads/tenants/jetpartners/reports/monitor-<YYYY-MM-DD>.md
        lead_quality: /Users/nora/30x-ads/tenants/jetpartners/reports/lead-quality-<YYYY-MM-DD>.json
      allowed_apply_lab: jp-ads-health-apply-lab-v1
      approval_required_before:
        - account label or draft creation
        - tenant memory promotion
      readback_required:
        - checks run
        - warnings
        - blockers
        - owner actions
        - GEB learning route
    monthly-report:
      name: Monthly Report
      workflow_contract: agents/workflows/jetpartners-ads-monthly-report.workflow.md
      default_mode: propose
      source_artifacts:
        dashboard: https://reports.30x.company/jetpartners/latest
        monthly_report_pattern: /Users/nora/30x-ads/tenants/jetpartners/reports/monthly-<YYYY-MM>.md
        account_changes_pattern: /Users/nora/30x-ads/tenants/jetpartners/reports/account-changes-<YYYY-MM-DD>.json
        monitor_pattern: /Users/nora/30x-ads/tenants/jetpartners/reports/monitor-<YYYY-MM-DD>.md
      allowed_apply_lab: jp-ads-monthly-report-apply-lab-v1
      approval_required_before:
        - report publish
        - swall report issue creation
        - tenant memory promotion
      readback_required:
        - report month
        - sources used
        - published or draft status
        - client-safe URL or path
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
      workflow_patch: repeated JP playbook step, gate, failure behavior, tail rule, or readback change
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

When this agent is invoked, load this mounted contract first. Then load the base role, JP tenant attachment, selected playbook workflow, and 30x-ads project-local memory. An entrypoint is only the doorway; this file is the mounted agent contract.

This agent is adaptive, installable, and detachable. Adaptive means playbook tails and memory improve through GEB deltas after real runs. Installable means the mounted contract can be added without secrets or live mutation permission. Detachable means tenant runtime and entrypoint projection can be removed while preserving base role, workflows, audit evidence, and approved learnings.

This contract is runtime-neutral: role, tenant attachment, playbooks, evidence/approval gates, and GEB learning are the same whichever agent runtime reads it. Which runtime runs it is the user's choice and is never encoded here. The gates live in the playbook, so any runtime that runs the work must pass them.
