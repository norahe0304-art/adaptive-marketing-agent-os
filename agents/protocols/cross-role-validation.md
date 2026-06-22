<!--
[INPUT]: Depends on role-package.schema.md, agent-onboarding.contract.md, Ads and Event fixture files.
[OUTPUT]: Provides cross-role validation proving shared schema vs domain-specific tools and host-specific adapter differences.
[POS]: protocols validation layer for proving the Agent OS is not Ads-only.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Cross-Role Validation

The shared protocol must be shaped so future domain roles can join without changing the core every time. The Ads and Event fixtures prove the first two distinct consumers; they do not prove every future domain by themselves.

## Shared Schema

Both `ads-adaptive-operator` and `event-adaptive-operator` role packages must include these shared protocol fields:

- identity
- capability_surface
- host_adapters
- permissions
- approval_policy
- evidence_contract
- learning_rules

Role outputs may include `post_run_delta` as a promised deliverable. Workflow files, not role files, must include `workflow_contract` and define the concrete readback step that produces `post_run_delta`.

## Domain-Specific Tools

`ads-adaptive-operator` may use Ads tools such as Google Ads, Meta, LinkedIn, and landing-page review.

`event-adaptive-operator` may use HubSpot pages/emails/workflows/lists, Salesforce read-only context, docs, and approval packets.

## Host-Specific Adapter

Base Ads may optionally support Codex, portal, or Slack. It does not require a host adapter.

Base Event is host-neutral. Tenant overlays may require a collaboration host and name their preferred adapter.

## Seed Proofs

- The Ads overlay fixture proves domain role plus tenant overlay composition.
- The Event overlay fixture proves a second domain role plus tenant overlay composition.

## Validation Command

```bash
python3 - <<'PY'
from pathlib import Path
import re
import yaml

bad = [
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

allowed_role_modes = {"read", "observe", "dry_run", "propose"}
allowed_workflow_modes = {"read", "observe", "dry_run", "propose", "apply"}
allowed_surface_keys = {"modes", "default", "future_live_action_requires_approval"}
role_required = [
    "identity", "purpose", "when_to_use", "inputs", "outputs",
    "role_instructions", "skills", "memory_scope", "tools", "plugins",
    "host_adapters", "capability_surface", "mcp_boundary", "permissions",
    "approval_policy", "evidence_contract", "learning_rules", "lifecycle",
    "success_criteria", "non_goals", "versioning",
]

def yaml_block(path):
    text = Path(path).read_text()
    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not match:
        raise SystemExit(f"missing yaml block: {path}")
    return yaml.safe_load(match.group(1))

for path in [*Path("agents/roles").glob("*.role.md"), *Path("agents/examples").glob("*-role.fixture.md")]:
    doc = yaml_block(path)
    pkg = doc.get("role_package")
    if not isinstance(pkg, dict):
        raise SystemExit(f"missing role_package: {path}")
    missing = [key for key in role_required if key not in pkg]
    if missing:
        raise SystemExit(f"missing {missing}: {path}")
    if "workflow_contract" in pkg:
        raise SystemExit(f"role_package must not include workflow_contract: {path}")
    if pkg["permissions"].get("max_mode_v1") != "propose":
        raise SystemExit(f"bad max_mode_v1: {path}")
    if not isinstance(pkg["learning_rules"].get("routes"), dict):
        raise SystemExit(f"bad learning_rules.routes: {path}")
    if not isinstance(pkg["learning_rules"].get("promotion_requires"), list):
        raise SystemExit(f"bad learning_rules.promotion_requires: {path}")
    for surface, spec in pkg["capability_surface"].get("surfaces", {}).items():
        extra = set(spec) - allowed_surface_keys
        if extra:
            raise SystemExit(f"unknown surface keys {extra} in {surface}: {path}")
        modes = set(spec.get("modes", []))
        if not modes <= allowed_role_modes:
            raise SystemExit(f"bad role modes {modes - allowed_role_modes} in {surface}: {path}")
        if not modes:
            raise SystemExit(f"missing modes in {surface}: {path}")
        default = spec.get("default")
        if default is not None and default not in modes:
            raise SystemExit(f"default not in modes for {surface}: {path}")
        approval_flag = spec.get("future_live_action_requires_approval")
        if approval_flag is not None and not isinstance(approval_flag, bool):
            raise SystemExit(f"bad future_live_action_requires_approval in {surface}: {path}")

for path in Path("agents/overlays").glob("*.overlay.md"):
    overlay = yaml_block(path).get("tenant_overlay")
    for key in ["identity", "tenant_memory_records", "overlay_memory_rule"]:
        if key not in overlay:
            raise SystemExit(f"missing {key}: {path}")

for path in Path("agents/workflows").glob("*.workflow.md"):
    workflow = yaml_block(path).get("workflow_contract")
    for key in ["role", "overlay", "task_graph", "evidence_packet", "readback", "future_live_action_policy", "apply_lab"]:
        if key not in workflow:
            raise SystemExit(f"missing {key}: {path}")
    apply_lab = workflow.get("apply_lab") or {}
    for step in workflow.get("task_graph", []):
        mode = step.get("mode")
        if mode not in allowed_workflow_modes:
            raise SystemExit(f"bad workflow mode {mode}: {path}")
        if mode == "apply":
            if not apply_lab.get("enabled"):
                raise SystemExit(f"apply step without enabled apply_lab: {path}")
            if step.get("apply_lab") is not True:
                raise SystemExit(f"apply step missing apply_lab true: {path}")
            for key in ["runtime_binding_id", "allowed_operations", "required_gates"]:
                if key not in apply_lab:
                    raise SystemExit(f"apply_lab missing {key}: {path}")
PY
```
