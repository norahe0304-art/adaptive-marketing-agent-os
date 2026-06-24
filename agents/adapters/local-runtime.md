<!--
[INPUT]: Depends on protocol-consumption.contract.md and run-state-ledger.protocol.md.
[OUTPUT]: Provides thin local runtime boot guidance for runtime-neutral mounted agents.
[POS]: adapters local execution surface note for CLI/service wrappers.
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Local Runtime Adapter Note

A local runtime may be a CLI, service wrapper, or scheduled worker. It must read
the same mounted agent contract as every other runtime.

Minimum boot contract:

```text
load mounted agent
  -> resolve role, overlay, workflow
  -> validate assembly
  -> execute playbook by mode
  -> write final readback
  -> route GEB delta
```

Local runtimes may cache operational data outside the repo, but durable agent
learning enters the repo only as structured readback or verified delta.
