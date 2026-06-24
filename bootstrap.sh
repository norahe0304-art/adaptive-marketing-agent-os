#!/bin/sh
# ============================================================
# Adaptive Marketing Agent OS — one-line bootstrap
# ------------------------------------------------------------
# Pin the protocol and scaffold a consumer agent instance into your repo,
# in one command. Runtime-neutral: this only GENERATES the agent; you point
# any runtime (Codex / Claude Code / Claude Tag / CLI / Slack) at the result.
#
#   curl -fsSL https://raw.githubusercontent.com/norahe0304-art/adaptive-marketing-agent-os/master/bootstrap.sh | sh -s -- \
#     --domain Ads --tenant Acme \
#     --role ads-adaptive-operator --playbook daily-maintenance --dest .
#   (--name defaults to <tenant>-<domain>, e.g. acme-ads; pass --name to override)
#
# Env overrides: AMAO_VERSION (default v0.1.0), AMAO_REPO (clone URL).
# ============================================================
set -eu

# AMAO_VERSION pins a release tag/branch; empty = the default branch (latest).
VERSION="${AMAO_VERSION:-}"
REPO="${AMAO_REPO:-https://github.com/norahe0304-art/adaptive-marketing-agent-os.git}"

command -v git >/dev/null 2>&1     || { echo "bootstrap: git is required" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "bootstrap: python3 is required" >&2; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

if [ -n "$VERSION" ]; then
  echo "bootstrap: fetching protocol $VERSION ..."
  git clone --depth 1 --branch "$VERSION" "$REPO" "$TMP/src" >/dev/null 2>&1
else
  echo "bootstrap: fetching protocol (latest) ..."
  git clone --depth 1 "$REPO" "$TMP/src" >/dev/null 2>&1
fi

if [ ! -f "$TMP/src/scripts/scaffold_consumer.py" ]; then
  echo "bootstrap: this protocol ref has no scaffolder; pin a newer AMAO_VERSION" >&2
  exit 1
fi

# Hand off to the scaffolder (the hands). It pins the protocol under <dest>/protocol/,
# stamps a green minimal instance from templates, and validates.
exec python3 "$TMP/src/scripts/scaffold_consumer.py" ${VERSION:+--version "$VERSION"} "$@"
