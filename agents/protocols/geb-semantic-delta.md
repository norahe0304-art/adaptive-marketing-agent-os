<!--
[INPUT]: Depends on AGENTS.md L1/L2 docs, role-package.schema.md learning_rules, and OMO final_readback.
[OUTPUT]: Provides post_run_delta routing, knowledge_updates, skill_candidate_updates, and structural L1/L2/L3 sync rules.
[POS]: protocols GEB governance for semantic and structural evolution.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# GEB Semantic and Structural Delta

GEB is not only learning. Every result must decide both semantic placement and structural documentation impact.

## Delta Classes

- `tenant_memory_patch`: tenant-only operating truth or source pointer.
- `industry_playbook_patch`: reusable domain pattern across tenants.
- `role_schema_patch`: role package field or boundary change.
- `workflow_patch`: repeatable task graph or gate change.
- `skill_patch`: improvement to an existing stable skill.
- `new_skill_candidate`: candidate produced from repeated stable sessions.
- `protocol_update`: shared semantic change required by multiple roles.

## Structural Delta

Structural deltas preserve L1/L2/L3 isomorphism for every created, moved, renamed, or responsibility-shifted artifact.

- L1 `/AGENTS.md`: project constitution and global map.
- L2 `/{module}/AGENTS.md`: module map and member list.
- L3 file header: `[INPUT]`, `[OUTPUT]`, `[POS]`, `[PROTOCOL]`.

## Post Run Delta

```yaml
post_run_delta:
  semantic_delta:
    class: ""
    target: ""
    evidence_id: ""
  structural_delta:
    files_created: []
    files_moved: []
    files_responsibility_changed: []
    agents_md_updates: []
  knowledge_updates: []
  skill_candidate_updates: []
  final_readback: ""
```

## Skill Candidate Rule

Interactive session learning is valid, but it becomes a skill candidate only after:

- repeated stable use
- evidence of replayability
- replay artifact with input fixtures, expected outputs, tool versions, and pass/fail criteria
- redaction review for tenant secrets, raw CRM exports, credentials, and private personal data
- reviewer approval
- documented GEB route

Record & Replay is useful for stable workflows, not every session.

## Replay Artifact

```yaml
replay_artifact:
  id: ""
  source_sessions: []
  redaction_status: ""
  tool_versions: []
  input_fixtures: []
  expected_outputs: []
  pass_fail_criteria: []
  reviewer: ""
  target_skill_candidate: ""
```

Session distillation may create memory, playbook, workflow, or skill-candidate deltas. Only a replay artifact can promote a session pattern into a skill candidate.
