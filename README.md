# Adaptive Marketing Agent OS

A runtime-neutral **protocol** for growing marketing agents. v0.1.0.

The protocol is three things: **role** (who the agent is) · **playbook** (the
work it does, which calls skills) · **GEB learning** (how it improves after each
run). Which runtime runs the agent — Codex, Claude Code, Claude Tag, a CLI, a
Slack mention — is **your choice and is never part of the protocol**. The
approval/evidence gates live in the playbook, so whatever runtime runs the work
must pass them.

This repo is **pure spec**: schema, gates, validators, a generation loop, and
tenant-neutral base roles. Real tenant agents live in their own consumer repos
that pin this protocol (see `agents/protocols/protocol-consumption.contract.md`).

## Use it — three ways

**1. One-line bootstrap** (pin + scaffold + validate, any environment)

```bash
curl -fsSL https://raw.githubusercontent.com/norahe0304-art/adaptive-marketing-agent-os/master/bootstrap.sh | sh -s -- \
  --domain <your-domain> --tenant <your-tenant> --playbook <your-playbook> --dest .
# e.g.  --domain SEO --tenant Acme --playbook content-audit
# generates your own role (<domain>-operator) + instance (<tenant>-<domain>).
# reuse a curated reference role instead: add --role <reference-role-id>
# override the instance id: add --name <id>
```

**2. Skill** (self-contained, no repo access needed)

```bash
python3 scripts/build_skill.py --dest ~/.claude/skills/grow-marketing-agent
# then invoke the skill in your runtime: "grow an ads agent for Acme"
```

**3. Manual** (vendor + scaffold)

```bash
python3 scripts/scaffold_consumer.py \
  --domain <your-domain> --tenant <your-tenant> --playbook <your-playbook> --dest <your-repo>
# e.g.  --domain SEO --tenant Acme --playbook content-audit --dest ../acme-seo
```

All three produce the same thing: a consumer instance (mounted agent + overlay +
workflows) pinned to the protocol and validated. Then point any runtime at
`agents/<name>.agent.md`, fill the `TODO` markers from the real scenario, and run.

## Concepts

- **role** — the reusable, tenant-neutral product unit. The protocol ships *reference* roles (`agents/roles/`) you may use, fork (`--role-mode own`), or replace with your own (`--role-mode new`). Marketing domains are unbounded; the schema is the invariant, not the list of domains.
- **skill** — an atomic action a playbook calls (e.g. spend check, keyword cluster).
- **playbook** — a business job the role exposes (e.g. daily maintenance), backed by a workflow.
- **workflow** — the machine-readable execution graph behind a playbook (steps, capability refs, approval gates, readback).
- **overlay** — a tenant attachment: customer truth + runtime bindings, mounted on a base role.
- **GEB learning** — post-run deltas that patch memory/playbook/skill/protocol, each gated by evidence + owner + review.

The full how-to-use is in `agents/protocols/`: `agent-generation.loop.md` (grow an
agent), `protocol-consumption.contract.md` (pin / reference / validate),
`agent-onboarding.contract.md` (add a new agent).

## Structure (pure spec)

```
agents/protocols/   schemas, gates, consumption + generation contracts
agents/roles/       reference roles (optional seeds — use, fork, or replace)
agents/templates/   stubs the generation loop stamps into a consumer instance
scripts/            validators, scaffolder, skill builder, pre-commit hook
bootstrap.sh        one-line consumer bootstrap
```

## Validate

```bash
python3 scripts/validate_roles.py
python3 scripts/validate_mounted_agents.py
git config core.hooksPath scripts/githooks   # enable the commit gate
```
