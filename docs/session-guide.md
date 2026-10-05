# Private sessions and resuming

The helper resolves symlinks and requires the session root outside this project. Use a private folder not tracked by another repository. Do not use a folder shared with other candidates unless access is correctly isolated.

`init` refuses an existing path. It creates profile.json, preferences.json, roles.json, research.json, state.json, source-resume/, and outputs/. Blank record values are unknown; do not complete intake using placeholder text.

`import-resume` preserves file bytes and a SHA-256 checksum, records an evidence source, and refuses overwriting an imported filename. Supported original files: DOCX, PDF, TXT, and Markdown. AI extraction requires its own tools and must not overwrite originals.

`next` writes a prompt containing the next stage instructions and current structured records. `status` prints progress without personal details. `validate` reports structural problems. `render-resume` produces a Markdown baseline from verified roles and claims; improve wording and layout manually with the assistant.

Stages complete in order: intake, interview, preferences, master, roles, market, profiles, action. Each stage requires its output file(s), non-placeholder text, applicable valid structured records, and explicit participant confirmation. Confirmation of the master profile is distinct from confirmation of a profile publication or application action.

```bash
python career.py render-resume --session ../private-career-session
python career.py validate --session ../private-career-session
python career.py complete --session ../private-career-session --stage master --confirmed
```

The helper stores approved stages and timestamps, but cannot verify that consent really occurred or that prose is accurate. The assistant and participant must perform that review. Corrections to approved profile/preferences/roles/research records invalidate affected stage completions automatically when status or next is run. Read the resulting checkpoint and re-approve dependent outputs; do not merely re-attest unchanged content.

When research is blocked, keep market pending, save the reason and next sources to gather, and resume later. Drafts of later material may be useful, but core completion must not be claimed. A record must include all three compensation lanes; unsupported lanes can be unavailable with a reason.

`--fictional` allows read-only validation/status of the repository's explicitly fictional reference example. It never permits new personal records or example mutations. Fictional evidence cannot pass the market completion gate in a real session.

The output files and notes may contain personal information. Deleting a private session is a user-managed operation; retain/export records only as desired. GitHub issues and CI logs are not candidate storage.
