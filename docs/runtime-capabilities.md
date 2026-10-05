# Runtime capabilities

| Capability | Use | If missing |
| --- | --- | --- |
| AI conversation | Adaptive interviews and reasoning | The Python helper alone cannot conduct the project |
| Document reading | Resume extraction and layout inspection | Ask for readable text or use the no-resume path |
| Private file writing | Structured records and checkpoints | Keep records in chat and export a checkpoint; explain persistence limitations |
| Live web research | Current roles, salary, and platform features | Mark research blocked; draft the research plan |
| Document generation/rendering | Optional polished DOCX/PDF | Deliver reviewed Markdown, do not claim polished files exist |
| Authorized account connectors | Optional profile changes or applications | Provide approved copy and manual steps |

AI instructions are model-neutral; runtime privacy, access policies, file persistence, and authentication differ. Review them for the actual environment. This repository makes no zero-retention or autonomous-execution promise.

Future automation could add model adapters and a research service around these contracts. It must retain evidence, checkpoints, participant review, and action-specific authorization. No scheduled jobs or model adapters are included in v0.1.0.
