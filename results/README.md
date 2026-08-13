# Result recording

Append one row per completed or failed run to `ledger.csv`. Do not overwrite or
remove rows. The run directory is the source of truth and must validate against
`schema.json`.

Required run artifacts:

- resolved configuration;
- git commit and dirty-tree flag;
- Python, PyTorch, CUDA, GPU, host, and dependency metadata;
- start/end timestamps and wall time;
- training/evaluation metrics by step and test depth;
- unique parameter count and block evaluation count;
- terminal status and failure class/message;
- protocol deviations and reason.

Aggregates must include every seed. Failed seeds cannot be silently replaced;
retries receive new run IDs linked to the original.

