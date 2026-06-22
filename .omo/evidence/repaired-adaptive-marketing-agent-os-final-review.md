# Repaired Adaptive Marketing Agent OS - Final Review Index

Generated: 2026-06-21

## Status

This index supersedes earlier failed review artifacts:

- `.omo/evidence/adaptive-marketing-agent-os-artifacts-code-review.md`
- `.omo/evidence/adaptive-marketing-agent-os-gate-review.md`
- `.omo/evidence/repaired-adaptive-marketing-agent-os-gate-review.md`
- `.omo/evidence/repaired-adaptive-marketing-agent-os-code-review.md`
- `.omo/evidence/adaptive-marketing-agent-os-final-artifacts-code-review.md`
- `.omo/evidence/final-adaptive-marketing-agent-os-gate-review.md`
- `.omo/evidence/final-minimal-qa-latest-files/04-forbidden-stale-vocabulary.txt` before the final cleanup

Those files record useful failures, but the blocking items they cite were repaired in the current artifact set.

## Current Artifact Surface

- `AGENTS.md`
- `agents/AGENTS.md`
- `agents/protocols/*.md`
- `agents/examples/*.md`
- `agents/roles/*.md`
- `agents/overlays/*.md`
- `agents/workflows/*.md`
- `.omo/plans/adaptive-agent-review-board.zh-CN.html`
- `.omo/plans/ads-agent-role-design.md`
- `.omo/plans/event-agent-role-design.md`
- `.omo/plans/shared-agent-os-protocol.md`

`git diff` is not sufficient for this review because the artifact set is still untracked in this worktree. Use `git status --short` plus the file inventory below as the reviewable delta.

## Manual QA Matrix

| Check | Command shape | Result |
| --- | --- | --- |
| L2 GEB protocol line | `find . -name AGENTS.md` plus exact `[PROTOCOL]` grep | PASS |
| L3 headers | all non-AGENTS markdown under `agents/` include `[INPUT]`, `[OUTPUT]`, `[POS]`, `[PROTOCOL]` | PASS |
| Deprecated mode vocabulary | negative scan for live `apply`, read-only pseudo-mode, stale apply states, old delta name, old owner field, blocked modes | PASS |
| Role/fixture conformance | roles and fixtures parse as YAML and include the canonical `role_package` fields, legal modes, `learning_rules.routes`, `learning_rules.promotion_requires`, and `max_mode_v1: propose` | PASS |
| Workflow boundary | workflows include `workflow_contract`, role, overlay, task graph, evidence packet, readback, `post_run_delta`, `future_live_action_policy` | PASS |
| Overlay memory | overlays include `tenant_memory_records` and `overlay_memory_rule` | PASS |
| Tenant isolation | Ads base has no JP tenant truth; Event base has no tenant adapter binding; concrete tenant adapter binding appears only in Caylent overlay | PASS |
| Runtime absence | no `mcp.json`, `package.json`, `*.js`, or `*.ts` under `agents/` | PASS |
| Stale plan cleanup | no `post_launch_delta`; review board no longer says generated files are pending | PASS |
| Final HTML host alignment | review board Ads host block has `required: []` and `codex` under optional | PASS |
| Concrete adapter isolation | concrete adapter name appears only in `agents/overlays/caylent-event-operator.overlay.md` across `agents/` and `.omo/plans/` | PASS |

## OMO QA Evidence

The latest QA executor pass wrote:

- `.omo/evidence/repaired-adaptive-marketing-agent-os-qa/S1-L2-GEB-protocol-line.txt`
- `.omo/evidence/repaired-adaptive-marketing-agent-os-qa/S2-L3-headers.txt`
- `.omo/evidence/repaired-adaptive-marketing-agent-os-qa/S3-S4-forbidden-terms.txt`
- `.omo/evidence/repaired-adaptive-marketing-agent-os-qa/S5-role-fixture-required-fields.txt`
- `.omo/evidence/repaired-adaptive-marketing-agent-os-qa/S6-S7-overlay-workflow-fields.txt`
- `.omo/evidence/final-adaptive-marketing-agent-os-qa/11-tenant-adapter-isolation-pass.txt`
- `.omo/evidence/repaired-adaptive-marketing-agent-os-qa/S9-no-runtime-files.txt`
- `.omo/evidence/repaired-adaptive-marketing-agent-os-qa/artifact-index.txt`

The final minimal review pass wrote:

- `.omo/evidence/final-minimal-code-doc-review-code-review.md`
- `.omo/evidence/adapter-isolation-html-host-fixes-gate-review.md`
- `.omo/evidence/final-minimal-qa-latest-files/01-concrete-adapter-isolation.txt`
- `.omo/evidence/final-minimal-qa-latest-files/02-html-ads-host-block.txt`
- `.omo/evidence/final-minimal-qa-latest-files/03b-pyyaml-role-fixture-validation-schema-aligned.txt`
- `.omo/evidence/final-minimal-qa-latest-files/04-forbidden-stale-vocabulary.txt`
- `.omo/evidence/final-minimal-qa-latest-files/05-no-runtime-files-under-agents.txt`

## Review Commands

```bash
for f in $(find agents -type f -name '*.md' ! -name 'AGENTS.md' | sort); do
  rg -q "\\[INPUT\\]" "$f"
  rg -q "\\[OUTPUT\\]" "$f"
  rg -q "\\[POS\\]" "$f"
  rg -q "\\[PROTOCOL\\]" "$f"
done

python3 - <<'PY'
from pathlib import Path
import re
bad = [
    "mode: " + "apply",
    r"modes: \[[^\]]*" + "apply",
    "required_for_" + "apply",
    "blocked_until_" + "approval",
    r"post[_-]launch[_-]delta",
    "owner_" + "layer",
    "blocked_" + "modes",
]
hits = []
for path in Path("agents").rglob("*.md"):
    text = path.read_text()
    for pattern in bad:
        if re.search(pattern, text):
            hits.append((str(path), pattern))
if hits:
    raise SystemExit(hits)
PY

python3 - <<'PY'
from pathlib import Path
import re
import yaml
allowed_modes = {"read", "observe", "dry_run", "propose"}
required = ["identity", "purpose", "when_to_use", "inputs", "outputs", "role_instructions", "skills", "memory_scope", "tools", "plugins", "host_adapters", "capability_surface", "mcp_boundary", "permissions", "approval_policy", "evidence_contract", "learning_rules", "lifecycle", "success_criteria", "non_goals", "versioning"]
def yaml_block(path):
    match = re.search(r"```yaml\n(.*?)\n```", Path(path).read_text(), re.S)
    if not match:
        raise SystemExit(f"missing yaml block: {path}")
    return yaml.safe_load(match.group(1))
for path in [*Path("agents/roles").glob("*.role.md"), *Path("agents/examples").glob("*-role.fixture.md")]:
    pkg = yaml_block(path).get("role_package")
    missing = [key for key in required if key not in pkg]
    if missing:
        raise SystemExit(f"missing {missing}: {path}")
    if "workflow_contract" in pkg:
        raise SystemExit(f"role_package must not include workflow_contract: {path}")
    if pkg["permissions"].get("max_mode_v1") != "propose":
        raise SystemExit(f"bad max_mode_v1: {path}")
    if not isinstance(pkg["learning_rules"].get("routes"), dict) or not isinstance(pkg["learning_rules"].get("promotion_requires"), list):
        raise SystemExit(f"bad learning_rules: {path}")
    for surface, spec in pkg["capability_surface"].get("surfaces", {}).items():
        modes = set(spec.get("modes", []))
        if not modes <= allowed_modes:
            raise SystemExit(f"bad modes {modes - allowed_modes} in {surface}: {path}")
PY

for file in agents/workflows/*.workflow.md; do
  for token in workflow_contract role overlay task_graph evidence_packet readback post_run_delta future_live_action_policy; do
    rg -q "$token" "$file"
  done
done
```

## Current Boundary

V1 is protocol and role-contract only. Current workflows stop at `propose`. Future live actions require a separate runtime security review and an active `ApprovalReceipt`.
