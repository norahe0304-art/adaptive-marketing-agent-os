#!/usr/bin/env python3
# [INPUT]: 读取 agents/mounted/*.agent.md 的 yaml 块，并检查其 role、tenant attachment、workflow、runtime、entrypoint 引用。
# [OUTPUT]: 对外提供 mounted agent 装配校验器；通过返回 0，违约返回 1 并打印第一个错误。
# [POS]: scripts mounted-agent 校验器，审判 assembled agent 是否真的接上 role、tenant、playbook、runtime。
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
        "host_runtime_policy",
        "boot_sequence",
        "playbooks",
        "runtime_boundaries",
        "geb_learning",
    ]:
        if section not in agent:
            raise ContractError(f"{path}: missing {section}")

    product = agent["product_contract"]
    for key in ["role", "tenant_attachment", "primary_runtime", "entrypoint_skill"]:
        if key not in product:
            raise ContractError(f"{path}: product_contract missing {key}")
        require_existing(resolve_ref(product[key]), key, path)
    if product.get("primary_host") != "codex":
        raise ContractError(f"{path}: product_contract.primary_host must be codex")

    host_policy = agent["host_runtime_policy"]
    if host_policy.get("default_host") != "codex":
        raise ContractError(f"{path}: host_runtime_policy.default_host must be codex")
    if host_policy.get("hermes_role") != "optional_adapter":
        raise ContractError(f"{path}: host_runtime_policy.hermes_role must be optional_adapter")

    boot = agent["boot_sequence"]
    always_read = boot.get("always_read")
    if not isinstance(always_read, list) or not always_read:
        raise ContractError(f"{path}: boot_sequence.always_read must be non-empty")
    for ref in always_read:
        require_existing(resolve_ref(ref), "boot_sequence.always_read", path)

    playbooks = agent["playbooks"]
    if not isinstance(playbooks, dict) or not playbooks:
        raise ContractError(f"{path}: playbooks must be a non-empty map")
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
