#!/usr/bin/env python3
# [INPUT]: 读取 validate_roles.py 的常量 (REQUIRED_FIELDS, ALLOWED_PROFILES) 与
#          role-package.schema.md / capability-boundary.schema.md 的 YAML 骨架。
# [OUTPUT]: 对外提供 check_schema_sync 闸门;Python 常量与文档契约漂移即非零退出。
# [POS]: scripts schema 同构闸门;让"散文契约"与"执行常量"互相审判,是 schema 化触发器的自我引爆装置;由 pre-commit 调用。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""Fail if validate_roles.py's constants drift from the schema docs.

role-package.schema.md states the contract in prose+YAML; validate_roles.py
executes it via REQUIRED_FIELDS / ALLOWED_PROFILES. Those are two copies of one
truth, hand-synced — exactly the drift `check_version_sync.py` kills for the
version string, applied to the schema contract. This gate is what makes the
"schema-ize WHEN REQUIRED_FIELDS drift from the doc" trigger in
role-package.schema.md self-firing instead of relying on a human noticing.

Two structured, robust cross-checks (YAML-to-set, no prose parsing):
- REQUIRED_FIELDS  ==  role-package.schema.md role_package keys minus `# optional`
- ALLOWED_PROFILES ==  capability-boundary.schema.md capability_profiles keys
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from validate_roles import REQUIRED_FIELDS, ALLOWED_PROFILES  # noqa: E402

ROLE_SCHEMA = REPO_ROOT / "agents/protocols/role-package.schema.md"
BOUNDARY_SCHEMA = REPO_ROOT / "agents/protocols/capability-boundary.schema.md"


def first_yaml_block(path: Path) -> str:
    text = path.read_text()
    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not match:
        raise SystemExit(f"FAIL  {path}: no yaml block")
    return match.group(1)


def named_yaml_block(path: Path, top_key: str) -> dict:
    # Return the first ```yaml block whose loaded content has top_key at root.
    text = path.read_text()
    for body in re.findall(r"```yaml\n(.*?)\n```", text, re.S):
        data = yaml.safe_load(body)
        if isinstance(data, dict) and top_key in data:
            return data[top_key]
    raise SystemExit(f"FAIL  {path}: no yaml block defining {top_key}")


def doc_role_fields() -> set[str]:
    # role_package's direct children (2-space indent), minus those marked optional.
    block = first_yaml_block(ROLE_SCHEMA)
    keys, optional = set(), set()
    for line in block.splitlines():
        m = re.match(r"^  ([a-z_]+):", line)
        if not m:
            continue
        key = m.group(1)
        keys.add(key)
        if "# optional" in line:
            optional.add(key)
    return keys - optional


def doc_profiles() -> set[str]:
    return set(named_yaml_block(BOUNDARY_SCHEMA, "capability_profiles").keys())


def diff(label: str, code: set[str], doc: set[str]) -> list[str]:
    if code == doc:
        return []
    return [
        f"  {label} drift:",
        f"    in code, not in doc: {sorted(code - doc) or '—'}",
        f"    in doc, not in code: {sorted(doc - code) or '—'}",
    ]


def main() -> int:
    errors = []
    errors += diff("REQUIRED_FIELDS vs role-package.schema.md", set(REQUIRED_FIELDS), doc_role_fields())
    errors += diff("ALLOWED_PROFILES vs capability-boundary.schema.md", set(ALLOWED_PROFILES), doc_profiles())
    if errors:
        print("FAIL  schema contract drift (validate_roles.py vs schema docs):", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        print("\nfix: bring the doc and the constant back in sync (they are one truth, "
              "two copies). If the shape surface keeps growing, this is the trigger to "
              "schema-ize per role-package.schema.md.", file=sys.stderr)
        return 1
    print("PASS  validate_roles.py constants match the schema docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
