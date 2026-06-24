<!--
[INPUT]: Depends on ads-adaptive-operator.role.md, Jetpartner operating evidence, and JP Ads workflow contracts.
[OUTPUT]: Provides Jetpartner tenant overlay for Ads Adaptive Operator.
[POS]: overlays tenant truth layer mounted on the Ads base role; never changes the shared OS protocol.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Jetpartner Ads Operator Overlay

This overlay mounts Jetpartner-specific operating truth on top of `ads-adaptive-operator`. It is the first real Ads implementation sample, not a shared protocol file.

```yaml
tenant_overlay:
  identity:
    id: jetpartners-ads-operator
    tenant: Jetpartner
    mounts_on: ads-adaptive-operator
    version: 0.1.0

  tenant_truth_boundary:
    allowed_here:
      - stable operating contracts
      - source pointers
      - lead quality definitions
      - account review defaults
      - approval owners or approval surfaces
    forbidden_here:
      - reusable Ads base-role rules
      - shared Agent OS protocol
      - uncited tenant facts
      - transient campaign metrics without evidence path

  source_of_truth:
    role_package:
      source_pointer: "/Users/nora/30x-ads/roles/jetpartners-ads-operator"
      stable_meaning: "Existing project-local role package, memory, tools, and operator skill for JP Ads."
    runtime_repo:
      source_pointer: "/Users/nora/30x-ads"
      stable_meaning: "30x-ads is the implementation substrate for JP Ads evidence, daily prep, dashboards, and approved apply-lab candidates."
    tenant_root:
      source_pointer: "/Users/nora/30x-ads/tenants/jetpartners"
      stable_meaning: "Tenant-specific brand profile, runtime reports, daily artifacts, and tenant-local config live here."
    reporting:
      latest_dashboard: "reports.30x.company/jetpartners/latest"
      usage: "Read-only source pointer for latest reporting evidence."
    daily_prep:
      source_pointer: "/Users/nora/30x-ads/tenants/jetpartners/scripts/daily-9-30am.sh"
      stable_meaning: "Read-only morning prep builds date-stamped artifacts and publishes the client-safe report before operator decisions."
    daily_artifacts:
      morning_brief_pattern: "/Users/nora/30x-ads/tenants/jetpartners/reports/morning-brief-<YYYY-MM-DD>.md"
      actions_pattern: "/Users/nora/30x-ads/tenants/jetpartners/reports/actions-<YYYY-MM-DD>.json"
      monitor_pattern: "/Users/nora/30x-ads/tenants/jetpartners/reports/monitor-<YYYY-MM-DD>.md"
      lead_quality_pattern: "/Users/nora/30x-ads/tenants/jetpartners/reports/lead-quality-<YYYY-MM-DD>.json"
      conflicts_pattern: "/Users/nora/30x-ads/tenants/jetpartners/reports/conflicts-<YYYY-MM-DD>.json"
      account_changes_pattern: "/Users/nora/30x-ads/tenants/jetpartners/reports/account-changes-<YYYY-MM-DD>.json"
    crm_quality:
      source: "Supabase qualified lead source"
      stable_meaning: "Qualified lead status and lead quality review source."
    status_language:
      observed_terms:
        - Contacted
        - Pre-Qualified
        - Application In-Pre-Qualified
        - Flyer
        - Converted
      rule: "Treat status terms as tenant CRM semantics; cite source before using in recommendations."
    operating_lessons:
      qualified_goal_rule: "Optimize to qualified lead truth, not raw GA4 form lead volume."
      search_term_semantics: "A bad phrase appearing in Google Ads may be a matched search term rather than a targeted keyword; cite range and search term status before replying."
      core_keyword_protection: "Do not negative high-intent converter terms only because CPA is high; optimize RSA, landing relevance, match type, and structure first."
      positive_keyword_gate: "Positive keyword additions require DataForSEO or Google Ads volume evidence plus account/qualified evidence, unless explicitly framed as a narrow exact local-route test."
      low_qs_converter_rule: "Low Quality Score keywords with conversions are relevance-improvement candidates, not automatic pause candidates."
      mutation_readback_rule: "After a live Google Ads mutation, require object readback plus negative conflict or account health smoke test."

  positioning_notes:
    current_known_risk:
      - "Private aviation intent mismatch must be checked before recommending expansion."
    review_rule:
      - "Lead quality can override surface-level platform conversion volume."
      - "Core private aviation converter terms should be improved before they are paused or negated."
      - "Negative keyword expansion must protect valid route, destination, and private charter intent."

  runtime_bindings:
    binding_owner: tenant_overlay
    implementation_substrate:
      repo: source_of_truth.runtime_repo.source_pointer
      tenant_root: source_of_truth.tenant_root.source_pointer
      existing_role_package: source_of_truth.role_package.source_pointer
      daily_prep: source_of_truth.daily_prep.source_pointer
      report_url: source_of_truth.reporting.latest_dashboard
    role_playbook_bindings:
      daily-maintenance:
        workflow_contract: agents/workflows/jetpartners-ads-daily-maintenance.workflow.md
        legacy_surface: "/Users/nora/30x-ads/.claude/skills/ads-daily/SKILL.md"
        prep_runtime: source_of_truth.daily_prep.source_pointer
        evidence_artifacts: source_of_truth.daily_artifacts
      account-review:
        workflow_contract: agents/workflows/jetpartners-ads-readonly-review.workflow.md
        evidence_artifacts: source_of_truth.daily_artifacts
      keyword-hygiene:
        workflow_contract: agents/workflows/jetpartners-ads-keyword-hygiene.workflow.md
        evidence_artifacts: source_of_truth.daily_artifacts
        source_surfaces:
          - "/Users/nora/30x-ads/.claude/skills/ads-keywords/SKILL.md"
          - "/Users/nora/30x-ads/scripts/audit-conflicts.ts"
          - "/Users/nora/30x-ads/scripts/build-keyword-inventory.ts"
      account-health-check:
        workflow_contract: agents/workflows/jetpartners-ads-account-health-check.workflow.md
        evidence_artifacts: source_of_truth.daily_artifacts
        source_surfaces:
          - "/Users/nora/30x-ads/.claude/skills/ads-health/SKILL.md"
          - "/Users/nora/30x-ads/.claude/skills/ads-monitor/SKILL.md"
          - "/Users/nora/30x-ads/scripts/preflight.ts"
          - "/Users/nora/30x-ads/scripts/observe.ts"
      monthly-report:
        workflow_contract: agents/workflows/jetpartners-ads-monthly-report.workflow.md
        evidence_artifacts: source_of_truth.daily_artifacts
        source_surfaces:
          - "/Users/nora/30x-ads/.claude/skills/ads-monthly-report/SKILL.md"
          - "/Users/nora/30x-ads/.claude/skills/ads-report/SKILL.md"
          - "/Users/nora/30x-ads/scripts/build-monitor-report.ts"
          - "/Users/nora/30x-ads/scripts/publish-dashboard.ts"
    abstract_surface_map:
      paid_media_platform:
        provider: google-ads
        binding_rule: "Use the tenant-scoped paid media connector only; never store credentials or account secrets in this overlay."
        evidence_required:
          - account or campaign scope
          - export path or dashboard URL
      analytics_source:
        provider: 30x-reporting-dashboard
        source_pointer: reporting.latest_dashboard
        mode: read
      crm_quality_source:
        provider: supabase-qualified-lead-source
        source_pointer: crm_quality.source
        mode: read
      landing_page_source:
        provider: browser-or-doc-source
        mode: read_observe
      memory_patch:
        provider: tenant-memory
        mode: propose

  capability_overrides:
    default_mode: read
    max_mode_v1: propose
    future_live_action_default: blocked_by_runtime_review
    allowed_without_human_approval:
      - read platform exports
      - observe landing pages
      - compare CRM quality summaries
      - draft proposal packets
    approval_required_for:
      - Google Ads mutation
      - budget change
      - bidding change
      - ad copy change
      - targeting change
      - conversion tracking change
      - tenant memory promotion

  evidence_contract:
    artifact_schema: agents/protocols/approval-evidence.schema.md#EvidenceArtifact
    required:
      - dashboard URL or export path
      - account/campaign/ad group scope
      - time window
      - CRM quality evidence
      - landing page URL if relevance is discussed
      - approval receipt for any future live action
      - final readback

  tenant_memory_records:
    - id: jp-reporting-latest-dashboard
      fact: "Latest reporting evidence is expected at reports.30x.company/jetpartners/latest."
      source_of_truth: reporting.latest_dashboard
      evidence_url: reports.30x.company/jetpartners/latest
      owner: 30x-ads-operator
      last_verified_at: "2026-06-21"
      review_after: "2026-07-21"
      promotion_target: tenant_memory
      expiry_reason: ""
    - id: jp-qualified-lead-source
      fact: "Qualified lead review should cite the Supabase qualified lead source."
      source_of_truth: crm_quality.source
      evidence_url: Supabase qualified lead source
      owner: 30x-ads-operator
      last_verified_at: "2026-06-21"
      review_after: "2026-07-21"
      promotion_target: tenant_memory
      expiry_reason: ""
    - id: jp-status-language
      fact: "Contacted, Pre-Qualified, Application In-Pre-Qualified, Flyer, and Converted are accepted JP qualified lead status terms and must be source-cited before recommendation use."
      source_of_truth: status_language.observed_terms
      evidence_url: Supabase qualified lead source
      owner: 30x-ads-operator
      last_verified_at: "2026-06-21"
      review_after: "2026-07-21"
      promotion_target: tenant_memory
      expiry_reason: ""
    - id: jp-search-term-not-target-keyword
      fact: "Client-visible bad phrases may be matched search terms rather than targeted keywords; responses must distinguish targeted keyword, matched search term, date range, and exclusion status."
      source_of_truth: source_of_truth.operating_lessons.search_term_semantics
      evidence_url: reports.30x.company/jetpartners/latest
      owner: 30x-ads-operator
      last_verified_at: "2026-06-22"
      review_after: "2026-07-22"
      promotion_target: tenant_memory
      expiry_reason: ""
    - id: jp-core-keyword-protection
      fact: "High-intent converter terms such as private jet charter, private jet flights, and new york charter jet should be improved through RSA/landing/match structure before pause or negative action."
      source_of_truth: source_of_truth.operating_lessons.core_keyword_protection
      evidence_url: reports.30x.company/jetpartners/latest
      owner: 30x-ads-operator
      last_verified_at: "2026-06-22"
      review_after: "2026-07-22"
      promotion_target: tenant_memory
      expiry_reason: ""
    - id: jp-positive-keyword-evidence-gate
      fact: "JP positive keyword additions require DataForSEO or Google Ads volume evidence plus account/qualified evidence, unless approved as a narrow exact local-route test."
      source_of_truth: source_of_truth.operating_lessons.positive_keyword_gate
      evidence_url: reports.30x.company/jetpartners/latest
      owner: 30x-ads-operator
      last_verified_at: "2026-06-22"
      review_after: "2026-07-22"
      promotion_target: tenant_memory
      expiry_reason: ""
    - id: jp-private-aviation-intent-risk
      fact: "Private aviation intent mismatch must be checked before recommending expansion."
      source_of_truth: positioning_notes.current_known_risk
      evidence_url: reports.30x.company/jetpartners/latest
      owner: 30x-ads-operator
      last_verified_at: "2026-06-21"
      review_after: "2026-07-21"
      promotion_target: tenant_memory
      expiry_reason: ""

  overlay_memory_rule:
    fields:
      - source_of_truth
      - evidence_url
      - owner
      - last_verified_at
      - review_after
      - promotion_target
      - expiry_reason
    promotion_targets:
      tenant_memory: "Stable JP truth."
      ads_playbook: "Reusable Ads rule proven across tenants."
      workflow: "Repeated JP Ads procedure."
      skill_candidate: "Stable execution sequence worth packaging."
      protocol: "Shared OS change; requires cross-role proof."

  learning_route:
    default: tenant_memory
    must_not_promote_to_base_role:
      - Jetpartner account facts
      - JP lead status semantics
      - JP dashboard paths
      - JP positioning constraints
      - JP campaign-specific keyword decisions
```

## Overlay Rule

This file may contain Jetpartner truth only when it points to an evidence source and has a review path. Durable cross-tenant rules must be proposed as GEB deltas, not silently copied into the Ads base role.
