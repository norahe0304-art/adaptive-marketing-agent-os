# Repaired Adaptive Marketing Agent OS Gate Review

recommendation: REJECT
verdict: FAIL

## originalIntent

Build a reusable Adaptive Marketing Agent OS protocol plus two first consumers: JP Ads and Caylent Event. The shared protocol must own common schema, permission modes, approval/evidence, OMO governance, GEB delta, host adapters, onboarding, and cross-role validation. Domain roles must consume the protocol rather than redefine it. Tenant truth must live in overlays. Workflows must be proposal-first. GEB L1/L2/L3 documentation must be present and aligned.

## desiredOutcome

- `agents/protocols/` defines reusable shared semantics with no tenant truth and no runtime provider config.
- `agents/roles/` contains tenant-neutral Ads and Event base roles that instantiate shared protocol fields.
- `agents/overlays/` contains Jetpartner and Caylent tenant operating truth with source pointers and review metadata.
- `agents/workflows/` contains JP Ads and Caylent Event workflow contracts that stop at `propose` in v1.
- Prior reviewer failures are repaired: no permission mode drift, no live apply ambiguity, no role schema mismatch, concrete approval receipt schema, non-tautological validation, structured overlay memory records, and `post_run_delta` naming.
- Evidence supports sign-off without relying on token-only checks or stale reports.

## userOutcomeReview

The current `agents/` product files are substantially closer to the intended architecture than the earlier failed review: `draft` is no longer a current mode in `agents/protocols/capability-boundary.schema.md`, workflow task modes stop at `propose`, live mutation is blocked behind future runtime security review, approval receipts now have a concrete schema, overlays carry structured memory fields, and active workflows use `post_run_delta`.

The artifact set still cannot pass final gate. The shared validation contract remains internally inconsistent: `cross-role-validation.md` says roles/fixtures must include `workflow_contract`, but the canonical `role-package` schema does not define it, the role/fixture files do not include it, and the validation command omits that requirement for roles/fixtures. That is exactly the kind of overfit/token validation slop prior review was meant to eliminate. The evidence package also remains incomplete/stale: the only code review report in scope still says `REQUEST_CHANGES`, the old gate review still says `REJECT`, there is no tracked diff, no notepad path, and no complete manual QA matrix.

## blockers

1. Cross-role validation still contradicts the shipped schema and instances.
   - `agents/protocols/cross-role-validation.md:14-23` requires both roles to include `workflow_contract` and `post_run_delta`.
   - `agents/protocols/role-package.schema.md:14-80` defines the canonical `role_package` object but has no `workflow_contract` field.
   - Direct check: `rg -n "workflow_contract" agents/roles agents/examples agents/protocols/role-package.schema.md agents/protocols/cross-role-validation.md` returns only `agents/protocols/cross-role-validation.md:22` and the workflow-file validation loop at line 69, not any role or fixture.

2. Validation evidence is still overfit/sloppy.
   - `agents/protocols/cross-role-validation.md:51-52` checks roles/fixtures for token presence but omits the `workflow_contract` token that the same file declares mandatory at line 22.
   - `.omo/evidence/repaired-adaptive-marketing-agent-os-qa/S5-role-fixture-required-fields.txt` reports PASS for roles/fixtures, but its evidence shows only token matches for `role_package`, `identity`, `capability_surface`, `host_adapters`, `permissions`, `approval_policy`, `evidence_contract`, `learning_rules`, `versioning`, and `post_run_delta`; it does not prove schema conformance or catch the missing `workflow_contract`.
   - This fails the direct `remove-ai-slops` pass: the check can pass while the declared contract is violated.

3. Evidence bundle does not support final approval.
   - `git ls-files`, `git diff --name-only`, and `git diff --cached --name-only` returned no tracked or staged artifacts, so there is no normal diff to review.
   - `.omo/evidence/adaptive-marketing-agent-os-artifacts-code-review.md:3-6` still records `Status: FAIL`, `codeQualityStatus: BLOCK`, and `recommendation: REQUEST_CHANGES`.
   - `.omo/evidence/adaptive-marketing-agent-os-gate-review.md:3` still records `recommendation: REJECT`.
   - `.omo/evidence/adaptive-marketing-agent-os-gate-review.md:85-91` records missing executor evidence package, diff summary, manual QA matrix, and notepad path. I found repaired QA command artifacts, but not the missing final-gate inputs.

4. Stale scoped artifacts still carry prior naming and user-visible state drift.
   - `.omo/plans/event-agent-role-design.md:121-128` still documents `post_launch_delta`, while the repaired active protocol uses `post_run_delta`.
   - `.omo/plans/adaptive-agent-review-board.zh-CN.html:516-542` still tells the user the next step is generating `agents/protocols/*`, `agents/roles/*`, `agents/overlays/*`, `agents/workflows/*`, and GEB files, even though those files now exist.

## warnings

- Active `agents/` files pass direct L2/L3 GEB checks: every `AGENTS.md` contains `[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md`, and every non-AGENTS markdown file under `agents/` contains `[INPUT]`, `[OUTPUT]`, `[POS]`, and `[PROTOCOL]`.
- Direct scan found no current `mode: apply`, `modes: [...apply...]`, `blocked_until_approval`, `apply_default`, `default_mode: read_only_review`, or `default_mode: draft_and_approval_first` patterns under `agents/`.
- Approval receipt abstraction is improved by `agents/protocols/approval-evidence.schema.md`, which now defines approver identity, authority, action hash, exact scope, timing, evidence links, and revocation fields.
- Overlay memory records are structured, but some `evidence_url` values are still labels such as `Supabase qualified lead source` rather than concrete URL/path evidence.

## checked artifact paths

- `AGENTS.md`
- `DESIGN.md`
- `agents/AGENTS.md`
- `agents/protocols/AGENTS.md`
- `agents/protocols/role-package.schema.md`
- `agents/protocols/capability-boundary.schema.md`
- `agents/protocols/approval-evidence.schema.md`
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
- `.omo/evidence/adaptive-marketing-agent-os-artifacts-code-review.md`
- `.omo/evidence/adaptive-marketing-agent-os-gate-review.md`
- `.omo/evidence/adaptive-marketing-agent-os-qa/*.txt`
- `.omo/evidence/repaired-adaptive-marketing-agent-os-qa/*.txt`
- `.omo/plans/adaptive-agent-review-board.zh-CN.html`
- `.omo/plans/event-agent-role-design.md`
- `.omo/plans/shared-agent-os-protocol.md`

## exactEvidenceGaps

- No tracked/staged diff or explicit changed-file list for this repaired pass.
- No updated independent code review report that supersedes the existing `REQUEST_CHANGES` report.
- No complete manual QA matrix; repaired evidence is command-output snippets, mostly token checks.
- No notepad path.
- No schema-aware validation artifact proving role/fixture/workflow YAML blocks conform to one canonical contract.

## directSkillPass

- `omo:remove-ai-slops`: Direct pass rejects the token-only validation as false-confidence slop because it omits a declared required field and would still pass inconsistent artifacts.
- `omo:programming`: No Python/Rust/TypeScript/Go source code was in scope, so language-specific references were not triggered. Applied shared programming criteria for strict contracts, parse/structure over ad hoc token validation, and rejection of maintenance burden from contradictory schema docs.
