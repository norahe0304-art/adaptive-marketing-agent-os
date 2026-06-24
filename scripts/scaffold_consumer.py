#!/usr/bin/env python3
# [INPUT]: 读取 agents/templates/*.tmpl 与协议树(agents/protocols, agents/roles, validators, dry_run_agent.py)，按场景参数生成一个消费方 agent 实例。
# [OUTPUT]: 对外提供 scaffold_consumer 脚手架；在 <dest> 下盖出 pin 好协议、含 run-state ledger 的最小可校验 agent 实例骨架。
# [POS]: scripts 生成回路的「手」，确定性盖骨架;内容由 runtime 填 TODO，validator 把关。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = REPO_ROOT / "agents/templates"


def protocol_version() -> str:
    # Single source of truth: the repo-root VERSION file. No hardcoded literals.
    return (REPO_ROOT / "VERSION").read_text().strip()


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def title_case(name: str) -> str:
    return " ".join(part.capitalize() for part in name.replace("_", "-").split("-"))


def source_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except Exception:
        return "unknown"


def vendor_protocol(dest: Path, version: str) -> None:
    # Pin: copy the protocol invariants into <dest>/protocol/ (vendored-copy mechanism).
    proto = dest / "protocol"
    if proto.exists():
        shutil.rmtree(proto)
    (proto / "agents").mkdir(parents=True)
    (proto / "scripts").mkdir(parents=True)
    # Ship the invariants + the reference-role library (optional seeds you may fork).
    for sub in ["protocols", "roles"]:
        shutil.copytree(REPO_ROOT / "agents" / sub, proto / "agents" / sub)
    for script in ["validate_roles.py", "validate_mounted_agents.py", "dry_run_agent.py"]:
        shutil.copy2(REPO_ROOT / "scripts" / script, proto / "scripts" / script)
    (proto / "VERSION").write_text(
        "name: adaptive-marketing-agent-os\n"
        f"version: {version}\n"
        f"source_commit: {source_commit()}\n"
        "mechanism: vendored-copy\n"
        "resync: re-run scaffold or re-copy agents/{protocols,roles} + scripts at the new tag\n"
    )


def render(template: str, repl: dict) -> str:
    text = (TEMPLATES / template).read_text()
    for token, value in repl.items():
        text = text.replace(token, value)
    return text


def main() -> int:
    p = argparse.ArgumentParser(description="Scaffold a consumer agent instance pinned to this protocol.")
    p.add_argument("--name", default=None,
                   help="instance id / file slug; default <tenant>-<domain> (e.g. acme-ads)")
    p.add_argument("--domain", required=True, help="marketing domain, e.g. Event")
    p.add_argument("--tenant", required=True, help="tenant/customer name, e.g. Acme")
    p.add_argument("--role", default=None,
                   help="role id; omit to generate your own role for the domain (<domain>-operator), or pass a reference role id to reuse/fork")
    p.add_argument("--role-mode", choices=["reference", "own", "new"], default=None,
                   help="reference: use a shipped reference role; own: fork it into your repo; new: generate a blank role stub. Default: reference when --role is given, else new")
    p.add_argument("--role-title", default=None, help="display title for a new/own role")
    p.add_argument("--playbook", default="first-playbook", help="kebab playbook id, e.g. event-launch")
    p.add_argument("--title", default=None, help="display title; default derived from --name")
    p.add_argument("--playbook-title", default=None, help="display title for the playbook")
    p.add_argument("--dest", required=True, help="consumer repo path to scaffold into")
    p.add_argument("--version", default=protocol_version(), help="protocol version to stamp in the pin (default: repo-root VERSION)")
    p.add_argument("--force", action="store_true", help="overwrite an existing agents/ in dest")
    p.add_argument("--no-validate", action="store_true", help="skip the post-scaffold validation run")
    args = p.parse_args()
    if not args.name:
        args.name = f"{slugify(args.tenant)}-{slugify(args.domain)}"
    # Universal default: no role given -> generate your own role for the domain.
    if not args.role:
        args.role = f"{slugify(args.domain)}-operator"
        args.role_mode = "new"
    elif args.role_mode is None:
        args.role_mode = "reference"

    source_role = REPO_ROOT / "agents/roles" / f"{args.role}.role.md"
    if args.role_mode in ("reference", "own") and not source_role.exists():
        avail = ", ".join(sorted(p.name[:-len(".role.md")] for p in (REPO_ROOT / "agents/roles").glob("*.role.md")))
        print(f"FAIL  no reference role '{args.role}' (available: {avail}); use --role-mode new to define your own",
              file=sys.stderr)
        return 1

    dest = Path(args.dest).resolve()
    agents = dest / "agents"
    if agents.exists() and not args.force:
        print(f"FAIL  {agents} already exists (use --force to overwrite)", file=sys.stderr)
        return 1

    # reference = share the protocol's role; own/new = the consumer owns its role.
    if args.role_mode == "reference":
        role_path = f"protocol/agents/roles/{args.role}.role.md"
    else:
        role_path = f"agents/{args.role}.role.md"

    repl = {
        "__NAME__": args.name,
        "__NAME_TITLE__": args.title or title_case(args.name),
        "__DOMAIN__": args.domain,
        "__TENANT__": args.tenant,
        "__ROLE_ID__": args.role,
        "__ROLE_PATH__": role_path,
        "__ROLE_TITLE__": args.role_title or title_case(args.role),
        "__PLAYBOOK__": args.playbook,
        "__PLAYBOOK_TITLE__": args.playbook_title or title_case(args.playbook),
    }

    vendor_protocol(dest, args.version)
    (agents / "workflows").mkdir(parents=True, exist_ok=True)
    (agents / "state" / "runs").mkdir(parents=True, exist_ok=True)
    (agents / "state" / "deltas").mkdir(parents=True, exist_ok=True)
    (agents / "state" / "memory").mkdir(parents=True, exist_ok=True)
    (agents / f"{args.name}.agent.md").write_text(render("consumer.agent.md.tmpl", repl))
    (agents / f"{args.name}.overlay.md").write_text(render("consumer.overlay.md.tmpl", repl))
    (agents / f"{args.name}.entrypoint.md").write_text(render("consumer.entrypoint.md.tmpl", repl))
    (agents / "workflows" / f"{args.name}-{args.playbook}.workflow.md").write_text(
        render("consumer.workflow.md.tmpl", repl))
    (agents / "AGENTS.md").write_text(render("consumer.AGENTS.md.tmpl", repl))
    (agents / "state" / "AGENTS.md").write_text(render("consumer.state.AGENTS.md.tmpl", repl))
    (agents / "state" / "memory" / "tenant-memory.md").write_text(
        render("consumer.tenant-memory.md.tmpl", repl))
    (agents / "state" / "runs" / ".gitkeep").write_text("")
    (agents / "state" / "deltas" / ".gitkeep").write_text("")
    # L1 constitution closes the agents/AGENTS.md `父级: /AGENTS.md` link.
    # Write-if-absent: never clobber a consumer repo that already owns a root AGENTS.md.
    root_l1 = dest / "AGENTS.md"
    root_l1_written = not root_l1.exists()
    if root_l1_written:
        root_l1.write_text(render("consumer.root.AGENTS.md.tmpl", repl))

    # Own a role locally: fork a reference role, or generate a blank stub to fill.
    if args.role_mode == "own":
        forked = source_role.read_text().replace("agents/protocols/", "protocol/agents/protocols/")
        (agents / f"{args.role}.role.md").write_text(forked)
    elif args.role_mode == "new":
        (agents / f"{args.role}.role.md").write_text(render("consumer.role.md.tmpl", repl))

    print(f"scaffolded consumer instance at {dest}")
    print(f"  protocol pinned -> {dest}/protocol/VERSION ({args.version})")
    print(f"  mounted agent   -> agents/{args.name}.agent.md")
    if args.role_mode == "reference":
        print(f"  role            -> protocol/agents/roles/{args.role}.role.md (reference, shared)")
    else:
        print(f"  role            -> agents/{args.role}.role.md (your own, {args.role_mode})")
    if root_l1_written:
        print(f"  root L1 (宪法)   -> AGENTS.md (seeded; closes the agents/ 父级 link)")
    print(f"  fill the TODO markers from the real scenario, then validate and dry-run.")

    if args.no_validate:
        return 0

    validator = dest / "protocol/scripts/validate_mounted_agents.py"
    result = subprocess.run(
        [sys.executable, str(validator), "--root", str(dest), "--glob", "agents/*.agent.md"],
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
