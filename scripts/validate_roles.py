#!/usr/bin/env python3
# [INPUT]: 读取 agents/roles/*.role.md 与 agents/examples/*-role.fixture.md 的 yaml 块；
#          契约定义来自 agents/protocols/role-package.schema.md。
# [OUTPUT]: 对外提供命令行校验器；通过返回 0，违约返回 1 并打印第一个错误。
# [POS]: scripts 唯一真相源校验器，被 scripts/githooks/pre-commit 调用，是 role-package.schema.md 的执行相。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""Adaptive Marketing Agent OS 角色包校验器。

role-package.schema.md 描述契约（语义相），本脚本执行契约（机器相）。
两相必须同构：schema 改字段，此处同步；此处改规则，schema 同步。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

# ============================================================
# 契约常量 —— 与 role-package.schema.md / capability-boundary.schema.md 对齐
# ============================================================
REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FIELDS = [
    "identity", "purpose", "when_to_use", "inputs", "outputs",
    "role_instructions", "skills", "memory_scope", "tools", "plugins",
    "host_adapters", "capability_surface", "mcp_boundary", "permissions",
    "lifecycle", "evidence_contract", "approval_policy", "success_criteria",
    "non_goals", "learning_rules", "versioning",
]
ALLOWED_MODES = {"read", "observe", "dry_run", "propose"}
ALLOWED_SURFACE_KEYS = {"modes", "default", "future_live_action_requires_approval"}


class ContractError(Exception):
    """单条契约违约。携带文件路径与原因。"""


# ============================================================
# 解析 —— 从 markdown 抽出首个 yaml 块
# ============================================================
def yaml_block(path: Path) -> dict:
    text = path.read_text()
    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not match:
        raise ContractError(f"{path}: missing yaml block")
    return yaml.safe_load(match.group(1))


# ============================================================
# 校验 —— 单个角色包逐条体检
# ============================================================
def validate_role(path: Path) -> None:
    pkg = yaml_block(path).get("role_package")
    if not isinstance(pkg, dict):
        raise ContractError(f"{path}: missing role_package")

    missing = [k for k in REQUIRED_FIELDS if k not in pkg]
    if missing:
        raise ContractError(f"{path}: missing fields {missing}")

    if "workflow_contract" in pkg:
        raise ContractError(f"{path}: role_package must not include workflow_contract")

    if pkg["permissions"].get("max_mode_v1") != "propose":
        raise ContractError(f"{path}: permissions.max_mode_v1 must be 'propose'")

    learning = pkg["learning_rules"]
    if not isinstance(learning.get("routes"), dict) or not isinstance(learning.get("promotion_requires"), list):
        raise ContractError(f"{path}: bad learning_rules shape")

    for surface, spec in pkg["capability_surface"].get("surfaces", {}).items():
        extra = set(spec) - ALLOWED_SURFACE_KEYS
        if extra:
            raise ContractError(f"{path}: unknown surface keys {extra} in '{surface}'")
        modes = set(spec.get("modes", []))
        if not modes:
            raise ContractError(f"{path}: missing modes in '{surface}'")
        if not modes <= ALLOWED_MODES:
            raise ContractError(f"{path}: bad modes {modes - ALLOWED_MODES} in '{surface}'")
        default = spec.get("default")
        if default is not None and default not in modes:
            raise ContractError(f"{path}: default '{default}' not in modes for '{surface}'")
        flag = spec.get("future_live_action_requires_approval")
        if flag is not None and not isinstance(flag, bool):
            raise ContractError(f"{path}: future_live_action_requires_approval must be bool in '{surface}'")


# ============================================================
# 入口 —— 收集目标、逐个校验、汇报
# ============================================================
def main() -> int:
    targets = sorted([
        *(REPO_ROOT / "agents/roles").glob("*.role.md"),
        *(REPO_ROOT / "agents/examples").glob("*-role.fixture.md"),
    ])
    if not targets:
        print("validate_roles: no role packages found", file=sys.stderr)
        return 1

    for path in targets:
        try:
            validate_role(path)
        except ContractError as err:
            print(f"FAIL  {err}", file=sys.stderr)
            return 1
        print(f"ok    {path.relative_to(REPO_ROOT)}")

    print(f"PASS  {len(targets)} role package(s) conform to role-package.schema.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
