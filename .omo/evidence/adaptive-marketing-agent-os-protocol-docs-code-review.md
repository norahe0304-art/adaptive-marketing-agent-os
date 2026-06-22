# Adaptive Marketing Agent OS Protocol Docs - Code Review

Scope: `/Users/nora/Documents/agency agents`, especially `AGENTS.md` and `agents/**/*.md`.

Skill-perspective check: ran by reading `omo:remove-ai-slops` and `omo:programming` skill instructions before judging maintainability/test relevance. No CRITICAL/HIGH violation from either perspective. Medium issues remain around underspecified schema validation and soft evidence pointers.

Verification performed:
- `YAML/protocol marker/mode check PASS`
- `role-package.schema validation PASS`
- `cross-role-validation command PASS`
- Line count scan: largest docs are `agents/roles/ads-adaptive-operator.role.md` at 290 lines and `agents/roles/event-adaptive-operator.role.md` at 274 lines.
- Folder count scan: `agents/protocols` has 9 Markdown files including its required `AGENTS.md` map, or 8 protocol documents excluding the map.

## CRITICAL

None.

## HIGH

None.

## MEDIUM

1. Capability surface sub-schema is not strict enough to enforce the protocol's own boundary.

   `agents/protocols/role-package.schema.md:101` to `agents/protocols/role-package.schema.md:107` says domain roles must not introduce new protocol fields or permission semantics. `agents/protocols/capability-boundary.schema.md:43` to `agents/protocols/capability-boundary.schema.md:56` defines a capability record shape, but the role files use repeated, undeclared surface keys such as `default` and `future_live_action_requires_approval` in `agents/roles/ads-adaptive-operator.role.md:138` to `agents/roles/ads-adaptive-operator.role.md:169` and `agents/roles/event-adaptive-operator.role.md:127` to `agents/roles/event-adaptive-operator.role.md:154`.

   The validation snippets only check that `modes` stay within the allowed enum (`agents/protocols/role-package.schema.md:148` to `agents/protocols/role-package.schema.md:151`, `agents/protocols/cross-role-validation.md:102` to `agents/protocols/cross-role-validation.md:105`). That means future SEO, Content, or Lifecycle roles could add arbitrary surface keys and still pass as schema-conformant. The fix is to define the exact shape for `capability_surface.surfaces.<surface>` or explicitly route defaults and approval requirements through existing `permissions` and `approval_policy`.

2. Tenant memory evidence pointers are not uniformly auditable.

   `agents/protocols/approval-evidence.schema.md:64` to `agents/protocols/approval-evidence.schema.md:68` expects source-backed evidence with `url_or_path`, and `agents/overlays/jetpartners-ads-operator.overlay.md:154` to `agents/overlays/jetpartners-ads-operator.overlay.md:156` says Jetpartner tenant truth must point to an evidence source. Some records use labels or broad planning artifacts instead of concrete source paths: `agents/overlays/jetpartners-ads-operator.overlay.md:104` and `agents/overlays/jetpartners-ads-operator.overlay.md:113` use `Supabase qualified lead source`; `agents/overlays/caylent-event-operator.overlay.md:103`, `agents/overlays/caylent-event-operator.overlay.md:112`, and `agents/overlays/caylent-event-operator.overlay.md:121` all point to `.omo/plans/adaptive-agent-review-board.zh-CN.html`.

   This is not a role/overlay separation failure, but it weakens evidence readback. The overlay can claim durable tenant truth without a reviewer being able to reopen the exact source artifact. Require either a resolvable URL/path or an explicit typed source id plus adapter binding.

## LOW

1. `agents/protocols` is at the folder-size edge.

   `agents/protocols/AGENTS.md:4` to `agents/protocols/AGENTS.md:12` lists 8 protocol documents, and the directory has 9 Markdown files including the required `AGENTS.md`. That is acceptable now, but the next shared protocol should probably create a subfolder boundary instead of making `protocols/` a catch-all.

2. Future live-action boilerplate is controlled but duplicated.

   The repeated future-action gates are consistent and do not expose `apply`, but the same concepts appear in the protocol, roles, overlays, and workflows. Examples include `agents/protocols/capability-boundary.schema.md:28` to `agents/protocols/capability-boundary.schema.md:41`, `agents/roles/ads-adaptive-operator.role.md:196` to `agents/roles/ads-adaptive-operator.role.md:204`, `agents/roles/event-adaptive-operator.role.md:182` to `agents/roles/event-adaptive-operator.role.md:190`, `agents/workflows/jetpartners-ads-readonly-review.workflow.md:76` to `agents/workflows/jetpartners-ads-readonly-review.workflow.md:85`, and `agents/workflows/caylent-event-launch.workflow.md:83` to `agents/workflows/caylent-event-launch.workflow.md:97`. Keep it centralized as the protocol hardens.

## Positive Checks

- No executable workflow step uses `apply`; workflow task modes stop at read, observe, or propose.
- Shared protocol files do not contain Jetpartner/Caylent tenant truth. Domain examples appear only as validation/examples, not as tenant operating facts.
- Base role vs overlay separation is mostly clean: base roles declare domain surfaces; overlays hold Jetpartner/Caylent host, evidence, and tenant-memory deltas.
- GEB L1/L2/L3 is practical rather than bloated: root `AGENTS.md` is 30 lines, module `AGENTS.md` files are 11 to 20 lines, and every checked Markdown artifact includes the required `[PROTOCOL]` marker.
- Future SEO/Content/Lifecycle can instantiate the current schema without changing core protocol, provided the capability surface shape is tightened before adding more domains.

## Status

codeQualityStatus: WATCH
recommendation: APPROVE
blockers: []
