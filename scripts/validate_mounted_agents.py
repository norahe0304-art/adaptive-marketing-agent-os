#!/usr/bin/env python3
# [INPUT]: 读取 agents/mounted/*.agent.md 的 yaml 块，并检查其 role、tenant attachment、playbook、work_substrate、entrypoints 引用。
# [OUTPUT]: 对外提供 mounted agent 装配校验器；通过返回 0，违约返回 1 并打印第一个错误。
# [POS]: scripts mounted-agent 校验器，审判 assembled agent 是否真的接上 role、tenant、playbook、work_substrate；runtime 不在协议内，不校验。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


class ContractError(Exception):
    pass


def yaml_block(path: Path) -> dict:
    text = path.read_text()
    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not match:
        raise ContractError(f"{path}: missing yaml block")
    return yaml.safe_load(match.group(1))


def resolve_ref(ref: str) -> Path:
    path = Path(ref)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def require_existing(path: Path, label: str, owner: Path) -> None:
    if not path.exists():
        raise ContractError(f"{owner}: missing {label}: {path}")


def validate_agent(path: Path) -> None:
    agent = yaml_block(path).get("mounted_agent")
    if not isinstance(agent, dict):
        raise ContractError(f"{path}: missing mounted_agent")

    for section in [
        "identity",
        "product_contract",
        "adaptivity_contract",
        "install_contract",
        "detach_contract",
        "boot_sequence",
        "playbooks",
        "runtime_boundaries",
        "geb_learning",
    ]:
        if section not in agent:
            raise ContractError(f"{path}: missing {section}")

    # Protocol = role + playbook + 回流. A mounted agent points at a base role, a
    # tenant attachment, and a work substrate. Which agent runtime runs it is the
    # user's choice, so no host/runtime field is required or checked here.
    product = agent["product_contract"]
    for key in ["role", "tenant_attachment", "work_substrate"]:
        if key not in product:
            raise ContractError(f"{path}: product_contract missing {key}")
        require_existing(resolve_ref(product[key]), key, path)
    entrypoints = product.get("entrypoints", [])
    if not isinstance(entrypoints, list) or not entrypoints:
        raise ContractError(f"{path}: product_contract.entrypoints must be a non-empty list")
    for ref in entrypoints:
        require_existing(resolve_ref(ref), "entrypoints", path)

    adaptivity = agent["adaptivity_contract"]
    if adaptivity.get("adaptive") is not True:
        raise ContractError(f"{path}: adaptivity_contract.adaptive must be true")
    for key in ["updates_allowed", "updates_forbidden", "promotion_requires"]:
        if not isinstance(adaptivity.get(key), list) or not adaptivity[key]:
            raise ContractError(f"{path}: adaptivity_contract.{key} must be a non-empty list")

    install = agent["install_contract"]
    if install.get("installable") is not True:
        raise ContractError(f"{path}: install_contract.installable must be true")
    for forbidden in ["credentials", "provider account secrets", "live mutation permission"]:
        if forbidden not in install.get("does_not_install", []):
            raise ContractError(f"{path}: install_contract.does_not_install must include {forbidden}")
    for key in ["installs", "install_check"]:
        if not isinstance(install.get(key), list) or not install[key]:
            raise ContractError(f"{path}: install_contract.{key} must be a non-empty list")

    detach = agent["detach_contract"]
    if detach.get("detachable") is not True:
        raise ContractError(f"{path}: detach_contract.detachable must be true")
    for key in ["detaches", "preserves", "removal_readback_required", "blocked_when"]:
        if not isinstance(detach.get(key), list) or not detach[key]:
            raise ContractError(f"{path}: detach_contract.{key} must be a non-empty list")

    boot = agent["boot_sequence"]
    always_read = boot.get("always_read")
    if not isinstance(always_read, list) or not always_read:
        raise ContractError(f"{path}: boot_sequence.always_read must be non-empty")
    for ref in always_read:
        require_existing(resolve_ref(ref), "boot_sequence.always_read", path)

    playbooks = agent["playbooks"]
    if not isinstance(playbooks, dict) or not playbooks:
        raise ContractError(f"{path}: playbooks must be a non-empty map")
    if agent["identity"].get("id") == "jetpartners-ads-agent":
        expected = {
            "daily-maintenance",
            "account-review",
            "keyword-hygiene",
            "account-health-check",
            "monthly-report",
        }
        if set(playbooks) != expected:
            raise ContractError(f"{path}: jetpartners-ads-agent playbooks must be {sorted(expected)}")
    for playbook_id, spec in playbooks.items():
        workflow = spec.get("workflow_contract")
        if not workflow:
            raise ContractError(f"{path}: playbook {playbook_id} missing workflow_contract")
        require_existing(resolve_ref(workflow), f"playbook {playbook_id} workflow_contract", path)
        if spec.get("default_mode") != "propose":
            raise ContractError(f"{path}: playbook {playbook_id} default_mode must be propose")
        if "approval_required_before" not in spec or "readback_required" not in spec:
            raise ContractError(f"{path}: playbook {playbook_id} missing approval/readback lists")


def main() -> int:
    targets = sorted((REPO_ROOT / "agents/mounted").glob("*.agent.md"))
    if not targets:
        print("validate_mounted_agents: no mounted agents found", file=sys.stderr)
        return 1

    for path in targets:
        try:
            validate_agent(path)
        except ContractError as err:
            print(f"FAIL  {err}", file=sys.stderr)
            return 1
        print(f"ok    {path.relative_to(REPO_ROOT)}")

    print(f"PASS  {len(targets)} mounted agent(s) conform")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
