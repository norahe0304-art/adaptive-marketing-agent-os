# Adaptive Marketing Agent OS Gate Review

recommendation: REJECT

## originalIntent

Build the first concrete Adaptive Marketing Agent OS artifacts that scale beyond one customer: a shared protocol layer, tenant-neutral Ads and Event base roles, Jetpartner and Caylent tenant overlays, and JP Ads / Caylent Event workflow implementations. Shared protocol owns schema, capability/MCP boundary, approval/evidence, OMO governance, GEB delta, host adapter interface, onboarding, and cross-role validation. Domain roles consume the protocol; they do not define it.

## desiredOutcome

- Protocol files define reusable OS semantics with no Ads/Event runtime implementation and no tenant truth storage.
- Base Ads role contains no Jetpartner facts.
- Base Event role contains no Caylent facts and no `slack: hermes` binding.
- Jetpartner and Caylent tenant truth lives in overlays.
- Workflows express the first two agents: JP Ads and Caylent Event.
- GEB L1/L2/L3 docs are complete: L1 project constitution, L2 module maps with the required protocol line, and L3 file contracts on every non-AGENTS markdown artifact.
- Review/evidence artifacts support completion without relying on shallow token-only checks.

## userOutcomeReview

The implementation is directionally aligned and contains the expected artifact families, but it is not ready for user sign-off. A user trying to treat these files as a completed, scalable protocol would hit internal contract drift: the seed fixtures do not satisfy the cross-role validation contract, base role packages do not instantiate the required schema exactly, the shared capability vocabulary introduces an undefined `draft` mode, and the HTML sign-off packet still says entity file generation is a next step even though entity files now exist.

## blockers

1. Seed fixtures do not satisfy the protocol's own cross-role validation contract.
   - `agents/protocols/cross-role-validation.md:14-23` requires both roles to include `identity`, `capability_surface`, `host_adapters`, `approval_policy`, `evidence_contract`, `learning_rules`, `workflow_contract`, and `post_run_delta`.
   - `agents/examples/jp-ads-role.fixture.md:10-38` and `agents/examples/caylent-event-role.fixture.md:10-40` include the first six concepts only; `workflow_contract` and `post_run_delta` are absent.
   - Direct check: `rg -n "workflow_contract|post_run_delta" agents/examples/*.fixture.md` returned no matches.

2. Base role packages drift from the canonical `role_package` schema.
   - Schema requires top-level `role_package.version`, `identity.owner_layer`, `mcp_boundary.provider/binding/scope/modes`, and `permissions` at `agents/protocols/role-package.schema.md:15-47`.
   - Both base roles place `version` under `identity`, use `layer: base_role` instead of `owner_layer`, omit a `permissions` object, and reshape `mcp_boundary` into mode subsections: see `agents/roles/ads-adaptive-operator.role.md:13-19`, `agents/roles/ads-adaptive-operator.role.md:162-195`, `agents/roles/event-adaptive-operator.role.md:13-19`, and `agents/roles/event-adaptive-operator.role.md:155-188`.
   - This violates the expected "roles consume schema" property because the concrete role packages are not exact schema instances.

3. Shared permission vocabulary is inconsistent.
   - The mode table defines only `read`, `observe`, `dry_run`, `propose`, and `apply` at `agents/protocols/capability-boundary.schema.md:18-27`.
   - The same protocol then lists `draft` as if it were a capability mode at `agents/protocols/capability-boundary.schema.md:59-64`; the HTML repeats `draft/propose` as capability surface language at `.omo/plans/adaptive-agent-review-board.zh-CN.html:432-437`.
   - If `draft` is an output type, it needs to be named that way; if it is a mode, it must be added to the shared mode table and propagated consistently.

4. The scoped HTML artifact is stale relative to the claimed completed implementation.
   - `.omo/plans/adaptive-agent-review-board.zh-CN.html:126` says the packet is waiting for final sign-off.
   - `.omo/plans/adaptive-agent-review-board.zh-CN.html:542` says the next step is generating `agents/protocols/*`, `agents/roles/*`, `agents/overlays/*`, `agents/workflows/*`, and GEB `AGENTS.md` files.
   - Those files already exist in the reviewed scope, so the user-visible packet does not represent the completed state.

5. Review evidence has gaps and contains shallow overfit checks.
   - No executor diff, independent code review report, manual QA matrix, or notepad path was provided in the workspace artifacts I inspected.
   - `.omo/evidence/adaptive-marketing-agent-os-qa/03_role_fixture_sections.txt:1-9` claims fixtures pass required sections, but the check only covered six terms and omitted the protocol-required `workflow_contract` and `post_run_delta`.
   - `.omo/evidence/adaptive-marketing-agent-os-qa/01_l2_protocol.txt:4-10` records a false failure from an incorrect command, later corrected in `01_l2_protocol_corrected.txt`; this is acceptable as history, but it reinforces that counts alone are not sufficient evidence.

## warnings

- Protocol files mention seed tenant examples inside shared protocol docs, including `agents/protocols/host-adapter.interface.md:59` and `agents/protocols/cross-role-validation.md:35-40`. This may be acceptable for validation, but the strict "shared protocol must not store JP/Caylent tenant truth" rule would be cleaner if tenant-specific facts stayed in overlays/fixtures and protocol text referenced them only as external fixture IDs.
- The L1/L2/L3 documentation checks pass for the scoped agent files: all non-AGENTS markdown artifacts under `agents/` have `[INPUT]`, `[OUTPUT]`, `[POS]`, and `[PROTOCOL]`; all L2 AGENTS files contain `[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md`.
- Base Ads passed the forbidden tenant-term scan for Jetpartner-specific details; Base Event passed the precise forbidden scan for Caylent name, `slack: hermes`, and real-looking HubSpot/Salesforce ID assignments.

## checked artifact paths

- `AGENTS.md`
- `agents/AGENTS.md`
- `agents/protocols/AGENTS.md`
- `agents/protocols/role-package.schema.md`
- `agents/protocols/capability-boundary.schema.md`
- `agents/protocols/host-adapter.interface.md`
- `agents/protocols/omo-execution-governance.md`
- `agents/protocols/geb-semantic-delta.md`
- `agents/protocols/agent-onboarding.contract.md`
- `agents/protocols/cross-role-validation.md`
- `agents/roles/AGENTS.md`
- `agents/roles/ads-adaptive-operator.role.md`
- `agents/roles/event-adaptive-operator.role.md`
- `agents/overlays/AGENTS.md`
- `agents/overlays/jetpartners-ads-operator.overlay.md`
- `agents/overlays/caylent-event-operator.overlay.md`
- `agents/workflows/AGENTS.md`
- `agents/workflows/jetpartners-ads-readonly-review.workflow.md`
- `agents/workflows/caylent-event-launch.workflow.md`
- `agents/examples/AGENTS.md`
- `agents/examples/jp-ads-role.fixture.md`
- `agents/examples/caylent-event-role.fixture.md`
- `.omo/plans/adaptive-agent-review-board.zh-CN.html`
- `.omo/plans/adaptive-agent-omo-review-summary.md`
- `.omo/evidence/adaptive-agent-review-board-qa.json`
- `.omo/evidence/adaptive-marketing-agent-os-qa/*.txt`

## exactEvidenceGaps

- Missing executor evidence package and diff summary for the completed implementation.
- Missing independent code review report that explicitly covers `omo:remove-ai-slops` / overfit-slop criteria.
- Missing manual QA matrix for the protocol artifacts beyond screenshot/overflow checks.
- Missing notepad path.
- Existing QA does not validate schema conformance deeply enough to catch fixture omissions or role-schema drift.

## directSkillPass

- `omo:remove-ai-slops`: Direct pass found test/QA slop in the artifact checks: token-only fixture validation passed despite missing contract-required fields. No production code was edited.
- `omo:programming`: No Python/Rust/TypeScript/Go code was in scope, so language-specific references were not triggered. Applied the shared criteria for strict contracts, avoidance of false confidence, and rejection of overfit checks.
