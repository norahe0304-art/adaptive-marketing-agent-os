# Quickstart

Grow your own marketing agent from this protocol in one command. You choose the
domain, the tenant, and the runtime — the protocol gives you a validated,
runtime-neutral agent that's safe, composable, and learns over time.

## Fastest: one command

Run this in your repo. Replace the `<...>` with your own values.

```bash
curl -fsSL https://raw.githubusercontent.com/norahe0304-art/adaptive-marketing-agent-os/master/bootstrap.sh | sh -s -- \
  --domain <your-domain> --tenant <your-tenant> --playbook <your-playbook> --dest .
```

Concrete example:

```bash
curl -fsSL .../bootstrap.sh | sh -s -- \
  --domain SEO --tenant Acme --playbook content-audit --dest .
```

That pins the protocol, generates your own role (`<domain>-operator`), and
scaffolds a validated agent instance named `<tenant>-<domain>` (e.g. `acme-seo`).

## Three ways to use it

| Way | Command | Best for |
| --- | --- | --- |
| **curl** | the one-liner above | any environment, zero setup |
| **skill** | install once, then say *"grow a SEO agent for Acme"* | Claude Code / Codex users (no flags) |
| **manual** | `git clone` + `python3 scripts/scaffold_consumer.py ...` | want to read/modify first |

Install the skill:

```bash
python3 <(curl -fsSL https://raw.githubusercontent.com/norahe0304-art/adaptive-marketing-agent-os/master/scripts/build_skill.py) \
  --dest ~/.claude/skills/grow-marketing-agent
```

## Roles: yours by default

- **Omit `--role`** → the scaffolder generates your own role for the domain
  (`<domain>-operator`). The protocol does not dictate which domains exist.
- **`--role <id>`** → reuse a curated reference role (`agents/roles/`), e.g.
  `--role ads-adaptive-operator`.
- **`--role <id> --role-mode own`** → fork a reference role into your repo and adapt it.

## What you get, and what's next

```
your-repo/
  protocol/                 pinned protocol (don't edit; re-pin to update)
  agents/
    <tenant>-<domain>.agent.md      the mounted agent
    <tenant>-<domain>.overlay.md    your tenant truth (fill the TODOs)
    <domain>-operator.role.md       your role (when generated)
    workflows/*.workflow.md         how the work runs
    state/                          structured readbacks, verified deltas, memory pointers
```

1. Fill the `TODO` markers from your real scenario. Store secret references only
   (`${ENV_NAME}`, `vault://...`, `1password://...`), never literal keys or tokens.
2. Validate:
   ```bash
   python3 protocol/scripts/validate_mounted_agents.py --root . --glob 'agents/*.agent.md'
   ```
3. Dry-run the mounted playbook:
   ```bash
   python3 protocol/scripts/dry_run_agent.py --root . --agent agents/<tenant>-<domain>.agent.md --playbook <your-playbook>
   ```
4. Point **any** runtime (Codex, Claude Code, Hermes, browser automation,
   MCP-backed tools, internal tools, or a local runner)
   at `agents/<tenant>-<domain>.agent.md`. The approval/evidence gates live in the
   playbook, so no runtime can bypass them.
5. After each real run, write a structured readback under `agents/state/runs/`
   and route any reusable learning as a reviewed GEB delta under
   `agents/state/deltas/` or the owning agent artifact.

See `README.md` for the full model and `agents/protocols/` for the contracts.
