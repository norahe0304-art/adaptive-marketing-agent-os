# adaptive-agent-role-design - Routing Index

## Status

This mixed plan has been split because Ads agent must not own the shared Agent OS protocol.

Correct responsibility boundary:

- Shared architecture owns Agent OS protocol.
- Ads agent consumes that protocol and designs Ads/Jetpartner roles.
- Event agent consumes that protocol and designs Event/HubSpot/Slack/Caylent roles.

## Active Plans

| Plan | Owner layer | Purpose |
| --- | --- | --- |
| `.omo/plans/shared-agent-os-protocol.md` | Shared architecture | Defines reusable Role schema, capability boundary, approval/evidence model, OMO governance, GEB semantic delta, host adapter interface, and cross-role validation. |
| `.omo/plans/ads-agent-role-design.md` | Ads agent | Designs `ads-adaptive-operator`, Jetpartner overlay, Ads read-only review workflow, and Ads-specific evidence/approval/learning. |
| `.omo/plans/event-agent-role-design.md` | Event agent | Designs `event-adaptive-operator`, Caylent overlay, HubSpot workflow, tenant collaboration host use, campaign association, approval/audit, and portal evidence console. |

## Today's Two Agents

```text
Adaptive Agent OS Protocol
  -> JP Ads Adaptive Agent
     -> ads-adaptive-operator
     -> jetpartners-ads-operator.overlay
     -> jetpartners-ads-readonly-review.workflow
  -> Caylent Event Adaptive Agent
     -> event-adaptive-operator
     -> caylent-event-operator.overlay
     -> caylent-event-launch.workflow
```

## Non-Negotiable Boundary

Ads agent consumes the shared Agent OS protocol.  
Ads agent does not define the shared Agent OS protocol.

Event agent consumes the shared Agent OS protocol.  
Event agent does not define the shared Agent OS protocol.

## Why This Split Exists

The previous plan mixed two jobs:

1. Design a reusable Agent OS protocol.
2. Design the Ads/Jetpartner role.

That makes Ads responsible for architecture it should only consume. The clean model is:

```text
Shared Agent OS Protocol
  Role schema
  Capability boundary
  Approval model
  Evidence contract
  OMO governance
  GEB semantic delta
  Host adapter interface
  Cross-role validation

Ads Agent
  Ads role
  Ads tools
  Ads workflows
  Jetpartner overlay

Event Agent
  Event role
  HubSpot tools
  tenant collaboration host flow
  Caylent campaign asset workflow
```

## Execution Rule

Do not execute this routing index as a work plan. Execute the active plan that matches the layer being changed.
