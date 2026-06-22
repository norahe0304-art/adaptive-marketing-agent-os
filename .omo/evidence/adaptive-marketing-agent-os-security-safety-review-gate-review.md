# Adaptive Marketing Agent OS Security/Safety Gate Review

recommendation: APPROVE
verdict: PASS
generated: 2026-06-21

## originalIntent

对 `/Users/nora/Documents/agency agents` 中 Adaptive Marketing Agent OS 文档工件做只读安全审查，重点验证 capability boundary、approval/evidence schema、base roles、tenant overlays、workflows 是否阻止 v1 直接变更外部系统，并保持租户事实、凭证、adapter 选择与 OS core 的边界。

## desiredOutcome

- V1 不能 live-mutate 外部系统，当前可执行 mode 只能到 `propose`。
- 未来 live action 必须绑定 `runtime_security_review_id`、typed `ApprovalReceipt`、`EvidenceArtifact`/evidence readback、exact scope、named approver、readback。
- 文档中不保存 secrets、raw credentials、unsafe tenant runtime bindings。
- Shared protocols 与 base roles 不包含 JP/Caylent tenant truth。
- Adapter 选择不升级为 OS core；Hermes/tenant host 偏好只留在 tenant overlay。

## userOutcomeReview

当前 scoped artifacts 满足用户安全目标。`capability-boundary.schema.md` 把 `apply` 标为 reserved 且 `Not in v1`，并要求 v1 role/workflow 声明 `max_mode_v1: propose` 且不得把 `apply` 列为当前 executable mode。两个 base role、两个 overlay、两个 workflow 的 YAML 结构化解析未发现 `mode: apply` 或 `modes` 包含 `apply`，全部 `max_mode_v1` 均为 `propose`。

未来 live-action gate 在 shared schema 与 role/workflow 层都有约束：`ApprovalReceipt` 定义 approver identity、authority、action hash、exact scope、evidence ids、expiry/revocation；`EvidenceArtifact` 定义 source/scope/integrity/readback；roles 引用 `ApprovalReceipt` 与 `EvidenceArtifact` anchors；workflows 在 future_live_action_policy 中保留 runtime security review、approval receipt、exact scope、pre-change evidence/readback。

凭证扫描未发现 API keys、bearer/basic tokens、password/secret/credential assignments、UUID/email/raw runtime URLs 或高熵 token。`agents/` 下未发现 runtime/config 实现文件如 `mcp.json`、`package.json`、`*.js`、`*.ts`、`*.py`、`*.go`、`*.rs`、`.env`、`*.json`、`*.yaml`、`*.yml`。

租户事实位置正确：Jetpartner reporting/Supabase/status/private-aviation facts 只在 JP overlay/workflow 中作为 source pointers 使用；Caylent Slack/Hermes host preference 只在 Caylent overlay 中出现。Shared protocols/base roles 未包含 JP/Caylent concrete tenant truth。Slack/Codex/portal 作为 optional host/channel vocabulary 出现在 shared/base 文档中，但未被要求为 OS core adapter；concrete adapter `hermes` 只在 `agents/overlays/caylent-event-operator.overlay.md`。

## blockers

None.

## safetyFindings

- PASS: V1 live mutation 被阻断。证据：`agents/protocols/capability-boundary.schema.md:20-41`、`agents/roles/ads-adaptive-operator.role.md:138-209`、`agents/roles/event-adaptive-operator.role.md:128-195`、`agents/workflows/jetpartners-ads-readonly-review.workflow.md:40-84`、`agents/workflows/caylent-event-launch.workflow.md:42-97`。
- PASS: 未来 live action 有 typed approval/evidence/readback contract。证据：`agents/protocols/approval-evidence.schema.md:12-83`、`agents/protocols/approval-evidence.schema.md:99-106`、`agents/roles/ads-adaptive-operator.role.md:211-242`、`agents/roles/event-adaptive-operator.role.md:197-227`、`agents/overlays/jetpartners-ads-operator.overlay.md:80-89`、`agents/overlays/caylent-event-operator.overlay.md:88-97`。
- PASS: 未发现 secrets/raw credentials/unsafe runtime bindings。证据：credential/high-entropy/URL/UUID/email scans over scoped files returned no matches; runtime file inventory under `agents/` returned no files.
- PASS: Tenant truth 未泄漏到 shared protocols/base roles。证据：tenant-term scan places Jetpartner-specific facts in `agents/overlays/jetpartners-ads-operator.overlay.md` and JP workflow evidence requirements; Caylent/Hermes facts in `agents/overlays/caylent-event-operator.overlay.md`.
- PASS: Adapter choice 未成为 OS core。证据：`hermes` scan across `agents .omo/plans` returns only `agents/overlays/caylent-event-operator.overlay.md`; `agents/protocols/capability-boundary.schema.md:70-74` explicitly forbids host-specific behavior in the protocol.

## checkedArtifactPaths

- `agents/protocols/capability-boundary.schema.md`
- `agents/protocols/approval-evidence.schema.md`
- `agents/roles/ads-adaptive-operator.role.md`
- `agents/roles/event-adaptive-operator.role.md`
- `agents/overlays/jetpartners-ads-operator.overlay.md`
- `agents/overlays/caylent-event-operator.overlay.md`
- `agents/workflows/jetpartners-ads-readonly-review.workflow.md`
- `agents/workflows/caylent-event-launch.workflow.md`
- `agents/roles/AGENTS.md`
- `agents/overlays/AGENTS.md`
- `agents/workflows/AGENTS.md`
- `.omo/evidence/final-minimal-code-doc-review-code-review.md`
- `.omo/evidence/final-minimal-qa-latest-files/01-concrete-adapter-isolation.txt`
- `.omo/evidence/final-minimal-qa-latest-files/03b-pyyaml-role-fixture-validation-schema-aligned.txt`
- `.omo/evidence/final-minimal-qa-latest-files/05-no-runtime-files-under-agents.txt`
- `.omo/evidence/adapter-isolation-html-host-fixes-gate-review.md`

## directValidation

- `rg --files agents/protocols agents/roles agents/overlays agents/workflows .omo | sort`
- `git status --short && git diff --stat && git diff -- agents/protocols agents/roles agents/overlays agents/workflows`
- Direct reads of all scoped protocol/role/overlay/workflow files.
- `rg -n "\b(apply|mutat|publish|send|activate|write|delete|update|create|live|runtime_security_review|ApprovalReceipt|EvidenceArtifact|approval receipt|readback|approver|exact_scope)\b" ...`
- `rg -n -i "(secret|credential|password|api[_-]?key|token|bearer|oauth|client[_-]?secret|private[_-]?key|sk-|ghp_|xox)" ...`
- `rg -n -i "(Jetpartner|JP|Caylent|Hermes|Slack|Supabase|reports\.30x|Contacted|Pre-Qualified|Private aviation)" ...`
- PyYAML parse over 10 scoped YAML blocks; no executable `apply`, all `max_mode_v1` values equal `propose`.
- `find agents -type f \( -name 'mcp.json' -o -name 'package.json' -o -name '*.js' -o -name '*.ts' -o -name '*.py' -o -name '*.go' -o -name '*.rs' -o -name '*.env' -o -name '*.json' -o -name '*.yaml' -o -name '*.yml' \) -print`

## slopAndProgrammingReview

- `omo:remove-ai-slops`: loaded and applied as read-only overfit/slop pass. No deletion-only tests, tautological tests, implementation-mirroring tests, unnecessary production extraction, parsing, or normalization were found in the scoped production docs. Old failing QA artifacts remain in `.omo/evidence`, but current direct validation and schema-aligned evidence supersede them.
- `omo:programming`: loaded and applied for structured contract rigor. No Python/Rust/TypeScript/Go source changes were reviewed; structured YAML parsing was used instead of token-only proof for executable mode checks.
- Code review report coverage: `.omo/evidence/final-minimal-code-doc-review-code-review.md` explicitly documents both `omo:remove-ai-slops` and `omo:programming` perspectives and reports no blockers. Direct review above confirms the same safety result.

## exactEvidenceGaps

- No tracked/staged diff exists; `git status --short` shows the artifact set is untracked, so current filesystem inspection was used as the source of truth.
- No notepad path was supplied in the executable review request.
- Historical `.omo/evidence/*` contains superseded FAIL reports; current PASS evidence and direct validation were used instead of trusting older artifact names.
- JP workflow future-live `allowed_only_after` lists `approval receipt` and has `named approver request` in the approval gate output; the named approver is also structurally carried by `ApprovalReceipt`. This is acceptable for current safety but could be hardened by repeating `named approver` inside `allowed_only_after`.
