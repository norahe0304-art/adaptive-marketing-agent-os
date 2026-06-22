# Agency Agents

Adaptive Marketing Agent OS v0.1.0.

This repository defines the protocol surface for installable marketing agents:
one reusable role, one tenant attachment, mounted playbooks, runtime pointers, and
validation gates that keep the package honest.

## Structure

- `agents/protocols/` - internal guardrails for schema, safety, execution, learning, packaging, onboarding, and validation.
- `agents/roles/` - tenant-neutral base roles.
- `agents/overlays/` - tenant attachments and runtime bindings.
- `agents/workflows/` - machine-readable workflow contracts behind playbooks.
- `agents/mounted/` - assembled agent definitions.
- `scripts/` - validators and the pre-commit hook.
- `.omo/` - planning, review, and evidence artifacts.

## Validate

```bash
python3 scripts/validate_roles.py
python3 scripts/validate_mounted_agents.py
```

To enable the local commit gate:

```bash
git config core.hooksPath scripts/githooks
```
