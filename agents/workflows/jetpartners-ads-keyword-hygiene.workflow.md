<!--
[INPUT]: Depends on ads-adaptive-operator.role.md, jetpartners-ads-operator.overlay.md, 30x-ads ads-keywords skill behavior, audit-conflicts.ts, DataForSEO evidence, OMO governance, and GEB delta protocol.
[OUTPUT]: Provides JP Ads keyword hygiene playbook workflow for search-term triage, negatives, positive candidates, conflict checks, approval-gated apply lab, readback, and learning routes.
[POS]: workflows JP Ads keyword hygiene playbook; internal workflow contract behind the Ads Role's search-term and keyword task.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Jetpartner Ads Keyword Hygiene Workflow

This workflow is the machine-readable contract behind the Ads Role's `keyword-hygiene` playbook for Jetpartner. It turns search-term evidence, DataForSEO checks, negative keyword safety, and conflict audit into one approval-gated operating path.

```yaml
workflow_contract:
  id: jetpartners-ads-keyword-hygiene
  role: ads-adaptive-operator
  overlay: jetpartners-ads-operator
  default_mode: propose
  workflow_kind: ads_keyword_hygiene_playbook

  playbook:
    name: keyword hygiene
    product_surface: role_playbook
    internal_workflow_contract: true
    source_surfaces:
      - "30x-ads .claude/skills/ads-keywords/SKILL.md"
      - "30x-ads scripts/audit-conflicts.ts"
      - "30x-ads scripts/build-keyword-inventory.ts"
      - "30x-ads scripts/kw-strategy-pull.ts"
      - "30x-ads scripts/kw-strategy-review.ts"
    calls_skills:
      - ads-keywords
      - ads-audit
      - ads-landing

  apply_lab:
    enabled: true
    runtime_binding_id: jp-ads-keyword-apply-lab-v1
    max_risk_class_v1: reversible_low
    allowed_operations:
      - add negative keyword
      - add exact positive keyword
      - add phrase positive keyword
      - add account or campaign label
      - create platform draft or experiment draft
    forbidden_operations:
      - broad positive keyword without explicit approval
      - budget change
      - bidding change
      - live ad copy change
      - conversion tracking change
    required_gates:
      - runtime_security_review_id
      - active ApprovalReceipt
      - exact account/campaign/ad group scope
      - pre_apply EvidenceArtifact
      - negative conflict precheck
      - rollback plan
      - post_apply conflict audit
      - post_apply readback EvidenceArtifact

  trigger:
    accepted_inputs:
      - review search terms
      - clean negatives
      - keyword hygiene
      - add positive keyword candidates
      - check keyword conflicts
    required_scope:
      - tenant
      - time window
      - campaign or ad group scope
      - requested keyword decision

  self_check:
    must_confirm:
      - Jetpartner overlay loaded
      - search-term evidence exists or can be pulled
      - DataForSEO or Google Ads volume evidence exists before positive keyword proposal unless narrow exact local-route test is explicitly approved
      - landing page relevance evidence exists before positive expansion
      - no negative batch can apply without conflict precheck and post-apply conflict audit
      - no apply_lab mutation requested without user confirmation, runtime review, exact scope, and rollback

  task_graph:
    - step: collect_keyword_evidence
      mode: read
      capability_refs:
        - paid_media_platform
        - analytics_source
      outputs:
        - search-term evidence
        - current positive keyword scope
        - negative inventory reference
        - conversion and spend window
    - step: classify_keyword_intent
      mode: observe
      capability_refs:
        - paid_media_platform
        - analytics_source
      outputs:
        - bad intent clusters
        - valid private aviation intent
        - converter protection list
        - positive candidate list
        - review-only list
    - step: validate_expansion_and_relevance
      mode: propose
      capability_refs:
        - paid_media_platform
        - landing_page_source
      outputs:
        - positive keyword proposal
        - negative keyword proposal
        - landing page relevance notes
        - DataForSEO or Google Ads volume references
    - step: approval_gate
      mode: propose
      capability_refs:
        - paid_media_platform
        - memory_patch
      outputs:
        - exact mutation batch preview
        - blocked terms
        - rollback note
        - explicit yes/no/change-mind request
    - step: apply_lab_execute_approved_keyword_batch
      mode: apply
      apply_lab: true
      capability_refs:
        - paid_media_platform
      runs_only_when:
        - approved_for_apply_lab
        - runtime binding available
        - requested operation is in apply_lab.allowed_operations
      outputs:
        - apply_run EvidenceArtifact
        - changed-object readback
        - post-apply conflict audit reference
        - rollback reference
    - step: readback_and_delta
      mode: observe
      capability_refs:
        - paid_media_platform
        - analytics_source
      outputs:
        - applied/skipped terms
        - protected converter terms
        - conflict audit result
        - post_run_delta

  future_live_action_policy:
    default_state: apply_lab_requires_approval
    allowed_only_after:
      - runtime_security_review_id
      - approval receipt
      - exact account/campaign/ad group scope
      - pre-change evidence
      - negative conflict precheck
      - rollback or irreversible-action note
      - post-apply conflict audit
      - post-apply readback

  evidence_packet:
    required:
      - search-term evidence path or export
      - keyword inventory path when available
      - campaign/ad group scope
      - time window
      - conversion and spend evidence
      - DataForSEO or Google Ads volume evidence for positive additions
      - landing page URL when relevance is discussed
      - conflicts-<date>.json if negatives are applied
      - approval receipt if apply_lab executes
      - apply_run artifact if apply_lab executes

  failure_behavior:
    missing_search_term_evidence: stop_and_request_source
    missing_positive_keyword_evidence: downgrade_positive_to_review_only
    missing_landing_page_relevance: block_positive_expansion
    conflict_precheck_missing: stop_at_plan
    approval_missing_for_apply_lab: stop_at_plan
    operation_outside_apply_lab: stop_at_plan

  readback:
    include:
      - what was reviewed
      - terms proposed
      - terms applied
      - terms skipped or protected
      - conflict audit result
      - learning route

  semantic_delta:
    tail_rule: "After every run, edit the right playbook tail if the decision queue, evidence requirement, approval gate, or readback shape changed."
    route_options:
      - tenant_memory_patch
      - keyword_hygiene_playbook_patch
      - workflow_patch
      - skill_patch
      - new_skill_candidate
      - protocol_update
    default_route: workflow_patch
    promotion_requires:
      - repeated evidence
      - owner
      - review_after
      - contradiction check
```

## Playbook Rule

Keyword hygiene is separate from daily maintenance only when the user asks for a deeper keyword/search-term pass. Daily maintenance may surface keyword items, but this playbook owns deeper negative safety, positive expansion, DataForSEO validation, and conflict-audit discipline.
