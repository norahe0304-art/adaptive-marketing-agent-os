#!/usr/bin/env python3
# [INPUT]: 读取 scripts/scaffold_consumer.py、agents/templates/ 与协议树(agents/protocols, agents/roles, validators)，打包成一个自包含 skill bundle。
# [OUTPUT]: 对外提供 build_skill 打包器；把生成回路装进一个 Claude Code / Codex skill 目录(含 SKILL.md)，别人装上就能长 agent，无需访问本 repo。
# [POS]: scripts 第三条分发入口的构建器;skill 是协议的派生物，repo 保持纯 spec。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def protocol_version() -> str:
    # Single source of truth: the repo-root VERSION file. No hardcoded literals.
    return (REPO_ROOT / "VERSION").read_text().strip()


SKILL_MD = """---
name: {skill_name}
description: Grow a marketing agent from the Adaptive Marketing Agent OS protocol. Use when the user wants to create, scaffold, or "grow" a new marketing agent (Ads, Event, ...), pin the protocol, and produce a validated, runtime-neutral agent instance they can run on any runtime. Triggers: "grow an agent", "scaffold an agent", "new marketing agent", "用协议长一个 agent".
---

# Grow a Marketing Agent

This skill bundles the Adaptive Marketing Agent OS generation loop. It grows a
consumer agent instance from a real scenario, pins the protocol, and validates —
all self-contained, no access to any external repo required.

The protocol is `role + playbook + GEB learning`. Runtime is the user's choice and
is never baked in: this skill GENERATES the agent; the user points any runtime
(Codex / Claude Code / Claude Tag / CLI / Slack) at the result.

## When invoked

1. Collect the scenario from the user (ask only for what is missing):
   - `domain`   marketing domain, e.g. `Ads` or `Event`
   - `tenant`   customer name, e.g. `Acme`
   - `playbook` kebab playbook id, e.g. `daily-maintenance`
   - `dest`     the user's repo to scaffold into (default: current directory)
   - `role`     optional — omit to generate your own role for the domain
                (`<domain>-operator`); pass a reference role id to reuse one.
                list reference roles: `ls "$SKILL_DIR/agents/roles"/*.role.md`
   - `name`     optional — instance id; defaults to `<tenant>-<domain>`

2. Run the scaffolder (the hands — deterministic):

   ```bash
   # default: generate your own role for the domain
   python3 "$SKILL_DIR/scripts/scaffold_consumer.py" \\
     --domain <Domain> --tenant <Tenant> --playbook <playbook> --dest <dest>
   # reuse a curated reference role instead: add --role <id> [--role-mode own]
   ```

   It pins the bundled protocol under `<dest>/protocol/` and stamps a green,
   minimal instance (overlay + mounted agent + workflow + entrypoint).

3. Fill the `TODO` markers in the generated files from the real scenario
   (overlay tenant truth, playbook approval/readback, workflow task_graph).
   Never bind a runtime, never store credentials, never edit `<dest>/protocol/`.

4. Re-validate:

   ```bash
   python3 "<dest>/protocol/scripts/validate_mounted_agents.py" --root <dest> --glob 'agents/*.agent.md'
   ```

5. Tell the user to point any runtime at `<dest>/agents/<name>.agent.md`. The
   approval/evidence gates live in the playbook, so no runtime can bypass them.

`$SKILL_DIR` is this skill's own directory. The full generation loop, schemas,
and gates are under `$SKILL_DIR/agents/protocols/`.
"""


def build(dest: Path, skill_name: str, version: str) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "agents").mkdir(parents=True)
    (dest / "scripts").mkdir(parents=True)
    # Bundle the protocol snapshot + the hands + the templates (same subset consumers vendor).
    for sub in ["protocols", "roles", "templates"]:
        shutil.copytree(REPO_ROOT / "agents" / sub, dest / "agents" / sub)
    for script in ["scaffold_consumer.py", "validate_roles.py", "validate_mounted_agents.py"]:
        shutil.copy2(REPO_ROOT / "scripts" / script, dest / "scripts" / script)
    (dest / "SKILL.md").write_text(SKILL_MD.format(skill_name=skill_name))
    try:
        commit = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        commit = "unknown"
    (dest / "VERSION").write_text(
        "name: adaptive-marketing-agent-os\n"
        f"version: {version}\n"
        f"source_commit: {commit}\n"
        "bundle: claude-code-or-codex-skill\n"
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Package the generation loop into a self-contained skill bundle.")
    p.add_argument("--dest", default=str(REPO_ROOT / "dist/skill/grow-marketing-agent"),
                   help="output skill directory (default: dist/skill/grow-marketing-agent, gitignored)")
    p.add_argument("--skill-name", default="grow-marketing-agent", help="skill name in SKILL.md frontmatter")
    p.add_argument("--version", default=protocol_version(), help="protocol version to stamp (default: repo-root VERSION)")
    args = p.parse_args()

    dest = Path(args.dest).resolve()
    build(dest, args.skill_name, args.version)
    print(f"built skill bundle -> {dest}")
    print(f"  SKILL.md + bundled protocol + scaffolder; self-contained, no repo access needed")
    print(f"  install: copy this directory into your .claude/skills/ (or .codex/skills/)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
