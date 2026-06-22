# Repaired Adaptive Marketing Agent OS - Code/Document Quality Review

PASS/FAIL: FAIL
codeQualityStatus: BLOCK
recommendation: REQUEST_CHANGES
reportPath: .omo/evidence/repaired-adaptive-marketing-agent-os-code-review.md

## CRITICAL

None.

## HIGH

1. `role_package` schema still does not match role and fixture instances for `learning_rules`.

`agents/protocols/role-package.schema.md:74` declares `learning_rules: []`, which is an array-shaped contract. The base role instances use a mapping with `routes` and `promotion_requires` at `agents/roles/ads-adaptive-operator.role.md:259` and `agents/roles/event-adaptive-operator.role.md:251`. The fixtures use a different singular mapping, `learning_rules.route`, at `agents/examples/jp-ads-role.fixture.md:102` and `agents/examples/caylent-event-role.fixture.md:109`.

Impact: prior blocker 1 remains open. A validator cannot know whether `learning_rules` is supposed to be an array, a `routes` object, or a singular `route` list. This breaks the shared contract for future roles.

2. Ads capability names are still not consistent enough across the base role and JP fixture.

The Ads base role declares supporting/capability surfaces such as `landing_page_review`, `google-ads`, `meta-ads`, `linkedin-ads`, `crm.read`, and `memory` at `agents/roles/ads-adaptive-operator.role.md:100-160`. The JP fixture introduces `ads-reporting` and `landing-review` in both `tools.supporting_surfaces` and `capability_surface.surfaces` at `agents/examples/jp-ads-role.fixture.md:48-67`, with no alias table or mapping back to the base role/protocol names.

Impact: prior blocker 6 remains open for Ads. Consumers cannot reliably join a fixture capability to the corresponding base role capability.

3. Ads host-adapter contradiction remains in cross-role validation.

The Ads base role currently has `host_adapters.required: []` and lists `codex` only as optional at `agents/roles/ads-adaptive-operator.role.md:125-136`. The host adapter protocol says base roles should stay host-neutral unless the domain itself requires a host at `agents/protocols/host-adapter.interface.md:57`. But `agents/protocols/cross-role-validation.md:33` still says, "Base Ads may require Codex and optionally support portal or Slack."

Impact: prior blocker 5 is fixed in the base role file but not in the protocol validation narrative. The shared validation doc still teaches the old contradiction.

4. Validation commands now inspect other files, but remain token-only and miss the open schema drift.

`agents/protocols/role-package.schema.md:105-109` and `agents/protocols/cross-role-validation.md:51-52` validate by grepping for tokens, not by parsing the YAML contract. The repaired QA artifact also states its criterion as "contain required role package fields" at `.omo/evidence/repaired-adaptive-marketing-agent-os-qa/S5-role-fixture-required-fields.txt:1-4`, then records PASS based on token presence at lines 6-49. Those checks pass while the current `learning_rules` shape mismatch above remains.

Impact: this violates the `omo:remove-ai-slops` and `omo:programming` review perspectives. It is an implementation-mirroring, false-confidence validation pass rather than a contract check.

## MEDIUM

1. `cross-role-validation.md` still lists role/schema requirements that are not in `role-package.schema.md`.

`agents/protocols/cross-role-validation.md:14-23` says both `ads-adaptive-operator` and `event-adaptive-operator` must include `workflow_contract` and `post_run_delta`. The canonical `role_package` schema at `agents/protocols/role-package.schema.md:15-79` does not define `workflow_contract`, and the role files include `post_run_delta` only as an output/lifecycle concept, not as a first-class schema field.

Impact: this is not a live mutation risk, but it keeps the validation document semantically out of sync with the schema it claims to validate.

2. Repaired evidence is stale relative to current fixture line numbers.

`.omo/evidence/repaired-adaptive-marketing-agent-os-qa/S5-role-fixture-required-fields.txt:6-27` records old fixture line numbers for `capability_surface`, `host_adapters`, and `versioning`; the current JP fixture places those sections at `agents/examples/jp-ads-role.fixture.md:58-122`, and the current Caylent fixture places them at `agents/examples/caylent-event-role.fixture.md:61-129`.

Impact: the evidence artifact is still useful as history, but it cannot be treated as authoritative proof of the current disk state.

## LOW

None.

## Prior Blocking Issue Status

1. role_package schema matches role/fixture instances: FAIL. Top-level fields are now present, but `learning_rules` shape still drifts.
2. No current role/workflow modes list apply; no old default mode names as `default_mode`: PASS. Structured scan found no current `apply` task/surface modes and no `read_only_review` or `draft_and_approval_first` default modes.
3. ApprovalReceipt/EvidenceArtifact schemas exist and are referenced: PASS. `agents/protocols/approval-evidence.schema.md:12-83` defines both contracts; role/fixture references point to those anchors.
4. Validation commands no longer grep only their own protocol files: PASS with WATCH. They now target roles/examples/overlays/workflows, but remain token-only and miss real drift.
5. Ads base role no longer has host adapter contradiction: FAIL. Base role is fixed, but `cross-role-validation.md` still states the old Codex requirement.
6. Capability names are consistent enough across roles and fixtures: FAIL for Ads.
7. Event base approval receipt is conditional for future live action, not universal: PASS. Event role and workflow use "approval receipt when future live action is requested" at `agents/roles/event-adaptive-operator.role.md:227` and `agents/workflows/caylent-event-launch.workflow.md:105`.

## Review Basis

Scope reviewed:
- `AGENTS.md`
- `agents/**/*.md`

Repository state:
- Current branch has no commits; `git status --short` shows `?? .omo/`, `?? AGENTS.md`, `?? DESIGN.md`, and `?? agents/`.
- No changed-file list, full diff, or notepad path was provided. I reviewed the current filesystem state and inspected existing `.omo/evidence` artifacts as untrusted supporting evidence.

Checks run:
- Loaded and applied `omo:remove-ai-slops` perspective before judging validation/test relevance.
- Loaded and applied `omo:programming` perspective before judging maintainability and contract rigor.
- Enumerated scoped Markdown files with `rg --files`.
- Parsed YAML fences with Ruby/YAML for schema-vs-instance checks.
- Ran current-mode scans for `apply`, `read_only_review`, and `draft_and_approval_first`.
- Ran L2/L3 GEB header checks.
- Ran the documented token validation commands and compared them against structured results.

Skill-perspective result:
- `remove-ai-slops`: violation found. Token-only QA/validation creates false confidence and misses contract drift.
- `programming`: violation found. The validation mirrors implementation constants instead of parsing typed structure; prompt/protocol tests should assert structured decisions and rule data, not token presence.

## Blockers

- Align `role-package.schema.md`, base roles, and fixtures on one `learning_rules` shape.
- Normalize or explicitly map Ads fixture capability names (`ads-reporting`, `landing-review`) to the base/protocol surface names.
- Update `cross-role-validation.md` so Ads base host requirements match the host-neutral base role.
- Replace token-only validation snippets/evidence with structured YAML checks that would fail on the current drift.
