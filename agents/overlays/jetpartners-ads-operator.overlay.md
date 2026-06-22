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
    reporting:
      latest_dashboard: "reports.30x.company/jetpartners/latest"
      usage: "Read-only source pointer for latest reporting evidence."
    crm_quality:
      source: "Supabase qualified lead source"
      stable_meaning: "Qualified lead status and lead quality review source."
    status_language:
      observed_terms:
        - Contacted
        - Pre-Qualified
      rule: "Treat status terms as tenant CRM semantics; cite source before using in recommendations."

  positioning_notes:
    current_known_risk:
      - "Private aviation intent mismatch must be checked before recommending expansion."
    review_rule:
      - "Lead quality can override surface-level platform conversion volume."

  host_adapters:
    required:
      - codex
    optional:
      - portal
      - slack
    preferred: {}
    unsupported: []
    notes: "JP Ads work can start in Codex and move to portal or Slack if the tenant asks for that host."

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
      fact: "Contacted and Pre-Qualified are tenant CRM status terms and must be source-cited before recommendation use."
      source_of_truth: status_language.observed_terms
      evidence_url: Supabase qualified lead source
      owner: 30x-ads-operator
      last_verified_at: "2026-06-21"
      review_after: "2026-07-21"
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
```

## Overlay Rule

This file may contain Jetpartner truth only when it points to an evidence source and has a review path. Durable cross-tenant rules must be proposed as GEB deltas, not silently copied into the Ads base role.
