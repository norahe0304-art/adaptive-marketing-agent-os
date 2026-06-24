<!--
[INPUT]: Depends on agent-onboarding.contract.md, protocol-consumption.contract.md, role-package.schema.md, capability-boundary.schema.md, geb-semantic-delta.md, the scaffold_consumer.py scaffolder, and the validators.
[OUTPUT]: Provides the executable loop that grows a conformant consumer agent from a real scenario, for any runtime.
[POS]: protocols generation loop; turns onboarding from a description into a runnable recipe. The protocol grows agents.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Agent Generation Loop

A consumer uses this protocol to grow its own agent from a real scenario, on
whatever runtime it picks. The protocol does not ship the answer; it ships the
shape (schema), the rules (gates), the hands (scaffolder), and the judge
(validators). Content is generated; structure is enforced.

This is the executable form of `agent-onboarding.contract.md`. Onboarding
describes the five steps; this loop runs them.

## Division of labor

```
deterministic (code, the hands)        |  generated (runtime, the judgment)
---------------------------------------+--------------------------------------
pin the protocol at a version          |  read the real scenario
correct paths + required schema fields |  fill tenant truth into the overlay
a green, minimal skeleton              |  write playbook steps + gates
the validator verdict                  |  iterate until green, then keep learning
```

Lock the mechanical, free the creative. This mirrors the whole protocol: schema
and gates are fixed; role / playbook / overlay / GEB-delta content is dynamic.

## The loop

```text
1. SCENARIO  collect the brief:
     domain, tenant, real systems (providers), approval surface,
     which base role to mount, which playbooks the agent must run

2. SCAFFOLD  run the hands (deterministic):
     python3 scripts/scaffold_consumer.py \
       --name <kebab-id> --domain <Domain> --tenant <Tenant> \
       --role <base-role-id> --playbook <kebab> --dest <consumer-repo>
     -> pins the protocol under <dest>/protocol/
     -> emits a green, minimal overlay + mounted agent + workflow + entrypoint

3. GENERATE  fill the TODO markers from the scenario (any runtime):
     overlay   -> source_of_truth, runtime_bindings, approval_surfaces, memory records
     mounted   -> playbook approval/readback lists, runtime_boundaries
     workflow  -> task_graph steps, capability_refs, apply_lab, evidence_packet
     never bind a runtime; never store credentials; never edit protocol/

4. VALIDATE  run the judge:
     python3 protocol/scripts/validate_mounted_agents.py --root . --glob 'agents/*.agent.md'
     not green -> back to step 3. green -> the instance is well-formed.

5. RUN       point any runtime (Codex / Claude Code / Claude Tag / CLI / Slack) at
     agents/<name>.agent.md. The gates live in the playbook, so the runtime can
     be anything and still cannot bypass approval/evidence.

6. LEARN     after each real run, route a GEB delta (geb-semantic-delta.md):
     tenant memory / workflow tail / skill candidate / protocol proposal,
     each carrying evidence + owner + review_after + contradiction_check.
     The agent keeps growing; the base role and protocol stay clean.
```

## Why this is safe to be dynamic

Generation is free, but every generated artifact passes the validator before it
runs, and every post-run change passes the GEB rails. A runtime can invent the
content; it cannot invent a way around the gates. That is the difference between
an adaptive agent and a hallucinating one.

## Adding a new base role

If no shipped base role fits the domain, that is a protocol change, not a
consumer change: add `agents/roles/<domain>-adaptive-operator.role.md` in the
protocol repo, validate with `scripts/validate_roles.py`, cut a new protocol
version, and consumers re-pin to it. Base roles are the one part the protocol
grows centrally; everything else grows in the consumer.
