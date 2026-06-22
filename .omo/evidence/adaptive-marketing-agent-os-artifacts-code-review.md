# Adaptive Marketing Agent OS Artifacts - Code/Document Quality Review

Status: FAIL
codeQualityStatus: BLOCK
recommendation: REQUEST_CHANGES
reportPath: .omo/evidence/adaptive-marketing-agent-os-artifacts-code-review.md

## Review Basis

Scope reviewed:
- AGENTS.md
- agents/AGENTS.md
- agents/protocols/*.md
- agents/examples/*.md
- agents/roles/*.md
- agents/overlays/*.md
- agents/workflows/*.md

Input completeness:
- No changed-file list, full diff, notepad path, or external evidence bundle was provided.
- `git diff --name-only` returned empty because the reviewed artifacts are currently untracked.
- `git status --short` shows `?? .omo/`, `?? AGENTS.md`, `?? DESIGN.md`, and `?? agents/`.

Skill-perspective check:
- Ran `omo:remove-ai-slops` perspective before maintainability/test relevance judgment.
- Ran `omo:programming` perspective before maintainability/test relevance judgment.
- Violations found: tautological validation commands, schema/instance drift, undefined mode vocabulary, and contract naming drift create false confidence and scale risk.

## CRITICAL

None.

## HIGH

1. Role schema and role instances do not share one canonical contract.

The canonical schema defines `role_package.version` and `identity.owner_layer` at `agents/protocols/role-package.schema.md:15-21`, but both base role instances put `version` under `identity` and use `layer` instead of `owner_layer` at `agents/roles/ads-adaptive-operator.role.md:13-19` and `agents/roles/event-adaptive-operator.role.md:13-19`. Cross-role validation then claims `workflow_contract` and `post_run_delta` are shared-schema requirements at `agents/protocols/cross-role-validation.md:14-23`, but `role-package.schema.md` does not define `workflow_contract`, neither base role includes it, and the Event role/workflow use `post_launch_delta` instead at `agents/roles/event-adaptive-operator.role.md:53-59` and `agents/workflows/caylent-event-launch.workflow.md:74-80`.

Impact: future Ads/Event/SEO/Content/Lifecycle agents cannot be validated mechanically because the schema, role files, workflow files, and validation doc disagree on required fields and names.

2. Permission modes and approval states drift beyond the shared vocabulary.

The shared capability modes are only `read`, `observe`, `dry_run`, `propose`, and `apply` at `agents/protocols/capability-boundary.schema.md:18-27`. The same protocol introduces `draft` as if it were a mode at `agents/protocols/capability-boundary.schema.md:56-64`, onboarding says workflows stop at `propose/draft` at `agents/protocols/agent-onboarding.contract.md:40-45`, workflows use bespoke `default_mode` values `read_only_review` and `draft_and_approval_first` at `agents/workflows/jetpartners-ads-readonly-review.workflow.md:13-18` and `agents/workflows/caylent-event-launch.workflow.md:13-18`, and overlays introduce `apply_default: blocked` / `blocked_until_approval` at `agents/overlays/jetpartners-ads-operator.overlay.md:62-64` and `agents/overlays/caylent-event-operator.overlay.md:70-72`.

Impact: "mode", "default mode", "draft", and "blocked" are mixed as permission modes, workflow styles, and approval states. That breaks the capability boundary and makes host/MCP enforcement ambiguous.

3. Live apply is declared blocked globally, but the Event workflow models apply as executable after approval.

The project constitution says live `apply` is blocked until a later runtime/security review at `AGENTS.md:21-25`. The capability protocol repeats that `apply` is not permission to mutate in this implementation pass at `agents/protocols/capability-boundary.schema.md:28-40`. The Caylent workflow accepts "launch after approval" at `agents/workflows/caylent-event-launch.workflow.md:19-25`, includes a task step with `mode: apply` at `agents/workflows/caylent-event-launch.workflow.md:68-73`, and states live actions remain blocked only until the approval contract is satisfied at `agents/workflows/caylent-event-launch.workflow.md:138-140`.

Impact: this collapses two gates into one. Human approval is necessary, but the root protocol also requires a later runtime/security review before live apply exists at all.

4. The documented validation commands are tautological and would pass while the real artifacts are inconsistent.

`agents/protocols/role-package.schema.md:79-84` greps for schema tokens inside the schema file itself. `agents/protocols/cross-role-validation.md:42-48` greps for validation tokens inside the validation file itself. These checks do not inspect base roles, overlays, workflows, or fixtures, so they would not catch the schema/instance mismatches above.

Impact: this violates the `remove-ai-slops` and `programming` review perspectives: the checks mirror implementation constants and create false confidence instead of proving behavior or contract conformance.

## MEDIUM

1. Base Ads host ownership contradicts the host adapter boundary.

The host protocol says base roles should stay host-neutral unless the domain itself requires a host at `agents/protocols/host-adapter.interface.md:55-59`. The Ads base role requires `codex` at `agents/roles/ads-adaptive-operator.role.md:125-136`, while the same note says no host adapter is part of the base role. Cross-role validation reinforces the exception without explaining why Ads inherently requires Codex at `agents/protocols/cross-role-validation.md:31-35`.

Impact: base Ads is not purely tenant/host neutral, and future portal/Slack/API Ads agents inherit a Codex requirement they may not need.

2. Capability surface names are not normalized across protocol, roles, fixtures, and overlays.

The protocol uses names like `google-ads`, `hubspot.pages`, and `salesforce` at `agents/protocols/capability-boundary.schema.md:56-66`. Base roles use `google_ads`, `hubspot_pages`, and `salesforce_read` at `agents/roles/ads-adaptive-operator.role.md:100-115` and `agents/roles/event-adaptive-operator.role.md:93-105`. Fixtures use `google-ads`, `ads-reporting`, `hubspot.pages`, and `salesforce.read` at `agents/examples/jp-ads-role.fixture.md:14-17` and `agents/examples/caylent-event-role.fixture.md:14-20`. Overlays use provider-local names like `pages`, `emails`, `workflows`, and `lists` at `agents/overlays/caylent-event-operator.overlay.md:46-57`.

Impact: consumers cannot reliably join a capability declared in a role to the same capability in a fixture, overlay, workflow, or host adapter.

3. Event base role requires approval receipt as universal evidence, while its workflow makes approval conditional on live actions.

The Event role requires `approval receipt` in the general evidence contract at `agents/roles/event-adaptive-operator.role.md:208-218`. The Caylent workflow correctly narrows this to `approval receipt for live actions` at `agents/workflows/caylent-event-launch.workflow.md:96-104`.

Impact: draft-only Event runs become impossible to complete under the base role's evidence contract even though the workflow permits draft/proposal outcomes.

## LOW

1. GEB headers are present, but some dependency references are too loose to be useful as navigation.

All scoped artifact files include `[INPUT]`, `[OUTPUT]`, `[POS]`, and `[PROTOCOL]` markers where expected. The example headers point to `ads-agent-role-design.md` / `event-agent-role-design.md` as "signed packet" inputs at `agents/examples/jp-ads-role.fixture.md:1-6` and `agents/examples/caylent-event-role.fixture.md:1-6`; the actual files are under `.omo/plans/` and are work plans, not clearly signed packets.

Impact: low immediate risk, but the headers become decorative if they do not name the real artifact path and state.

## Blockers

- Align `role-package.schema.md`, base role instances, fixtures, and cross-role validation on one field set: `version`, `owner_layer`/`layer`, `workflow_contract`, and `post_run_delta`.
- Normalize the permission vocabulary so `draft`, `read_only_review`, `draft_and_approval_first`, `blocked`, and `blocked_until_approval` are not confused with shared capability modes.
- Keep live `apply` blocked until the documented runtime/security review gate exists; approval alone must not imply execution permission.
- Replace tautological `rg` validation snippets with checks that inspect actual role, overlay, workflow, and fixture conformance.

## Positive Notes

- Tenant facts are mostly kept out of the base roles; JP and Caylent operating details are concentrated in overlays.
- L2 AGENTS maps are complete for the scoped files.
- GEB L3 headers are broadly present and aligned with the intended document graph.

