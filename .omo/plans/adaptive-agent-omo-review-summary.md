# adaptive-agent-omo-review-summary

## Verdict

OMO family review result: `ITERATE`, not `REJECT`.

The architecture direction is correct:

- Shared Adaptive Marketing Agent OS Protocol owns the protocol.
- JP Ads Adaptive Agent consumes the protocol.
- Caylent Event Adaptive Agent consumes the protocol.
- Concrete Slack adapters are tenant overlay choices, not OS core.

The protocol needed hardening before user sign-off.

## Reviewers

| Reviewer | Verdict | Main finding |
| --- | --- | --- |
| Explorer | ITERATE | Shared plan was still too pair-framed around JP Ads and Caylent Event; add generic agent onboarding/registry. |
| Librarian | ITERATE | External sources support separate protocol layer and evidence-gated lifecycle; mark Flyte as inspired contract, and make GEB a proposed extension layer. |
| Metis | ITERATE | Approval/apply boundary, overlay memory schema, evidence contract, and GEB structural role were too soft. |
| Momus | ITERATE | Acceptance checks could false-pass; shared plan should validate fixtures, while domain plans validate real role files after creation. |

## Applied Changes

### Shared Protocol

- Added Agent Registry / Onboarding Contract.
- Added rule that domain roles instantiate shared fields but cannot invent protocol semantics.
- Hardened `apply`: V1 may use workflow-scoped `apply_lab`; base roles still default to `propose`.
- Added Evidence Gates and required evidence fields.
- Renamed GEB framing to semantic and structural delta.
- Made cross-role validation generic, with JP Ads and Caylent Event as seed examples.
- Changed shared validation to use `agents/examples/*-role.fixture.md` instead of future real role files.
- Added GEB `AGENTS.md` acceptance checks.

### JP Ads Agent

- Clarified Ads evidence/approval/learning are instances of shared schema.
- Added overlay memory rule with source, owner, verification, review, and expiry/promotion fields.
- Added human approval receipt rule.
- Added GEB docs and member-list acceptance checks.
- Converted broad `rg "a|b|c"` checks into token-by-token checks.

### Caylent Event Agent

- Made base Event role host-neutral.
- Moved required collaboration host and preferred adapter into the tenant overlay.
- Added overlay memory rule with source, owner, verification, review, and expiry/promotion fields.
- Added human approval receipt rule.
- Added GEB docs and member-list acceptance checks.
- Converted broad `rg "a|b|c"` checks into token-by-token checks.

## User Sign-off Questions

1. Should v1 allow workflow-scoped `apply_lab` while base roles remain propose-first?
2. Where is the canonical evidence/audit store: repo docs, portal evidence console, CRM, Slack thread, or dedicated database?
3. Should tenant overlays contain small stable facts directly, or only pointers plus operating rules?
4. Who can approve high-risk marketing actions, and which actions require second approval?
5. Is the Event tenant overlay allowed to require a collaboration host while base Event remains host-neutral?
6. Are we signing off GEB as both learning governance and L1/L2/L3 structural isomorphism?

## Recommended Sign-off

Sign off only if the answer is yes to:

- Shared protocol can onboard future marketing agents through the onboarding contract.
- Domain roles cannot redefine shared protocol semantics.
- `apply_lab` is allowed only with runtime binding, evidence, approval, exact scope, and readback.
- GEB is semantic plus structural, not just learning.
- Tenant overlays are bounded operating contracts, not memory dumps.
