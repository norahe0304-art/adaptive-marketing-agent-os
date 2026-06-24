#!/usr/bin/env python3
# [INPUT]: 读取 repo-root VERSION（唯一真相）与所有 git 追踪文件中的版本字面量。
# [OUTPUT]: 对外提供 check_version_sync 闸门;任何与 VERSION 漂移的 vX.Y.Z 字面量 -> 非零退出。
# [POS]: scripts 版本同构闸门，让"复述的版本"被"引用的真相"审判;由 pre-commit 调用。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""Fail if any tracked file states a protocol version that drifts from VERSION.

Single source of truth = repo-root VERSION. Docs cannot interpolate, so they
hardcode the version string; this gate is the judge that keeps every hardcoded
copy equal to the source. Historical/example lines that must keep an older
version add a trailing `version-sync: ignore` marker to opt out.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSION_RE = re.compile(r"v\d+\.\d+\.\d+")
IGNORE_MARK = "version-sync: ignore"
# Evidence artifacts are frozen historical records of past versions, not live spec.
SKIP_PREFIXES = (".omo/",)
SKIP_FILES = {"VERSION"}


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.splitlines()


def main() -> int:
    canonical = (REPO_ROOT / "VERSION").read_text().strip()
    if not VERSION_RE.fullmatch(canonical):
        print(f"FAIL  VERSION holds '{canonical}', expected a vX.Y.Z string", file=sys.stderr)
        return 1

    drift: list[str] = []
    for rel in tracked_files():
        if rel in SKIP_FILES or rel.startswith(SKIP_PREFIXES):
            continue
        path = REPO_ROOT / rel
        try:
            lines = path.read_text(errors="ignore").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for n, line in enumerate(lines, 1):
            if IGNORE_MARK in line:
                continue
            for hit in VERSION_RE.findall(line):
                if hit != canonical:
                    drift.append(f"  {rel}:{n}: states {hit}, VERSION is {canonical}")

    if drift:
        print(f"FAIL  version drift vs VERSION ({canonical}):", file=sys.stderr)
        print("\n".join(drift), file=sys.stderr)
        print(f"\nfix: bump the literal to {canonical}, or append "
              f"`{IGNORE_MARK}` for an intentional historical mention", file=sys.stderr)
        return 1

    print(f"PASS  all version literals match VERSION ({canonical})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
