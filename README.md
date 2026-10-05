# JobHuntAI

A reusable, AI-guided career development workflow: resume intake, adaptive interview, verified master resume, role exploration, compensation research, profile positioning, and an actionable career plan.

Version 0.1.0 is a portable workflow with a Python session helper. An AI reads the instructions and conducts the work; the helper saves progress, checks records, and assembles the next prompt. It does not call a model, browse websites, or update accounts on its own.

## Start with an AI

Give an assistant this repository and [`START_HERE.md`](START_HERE.md), or paste that file into a conversation and attach the referenced workflow files. In a coding assistant, open the repository and say:

> Read AGENTS.md and START_HERE.md. Run the career workflow for me. Explain the process and expected time before asking for my resume. Keep my records in a private folder outside this repository. Save progress after each interview round.

The assistant should explain the process first, request a resume if one exists, ask small groups of questions, and build the master profile before doing market research. A resume is optional.

## Start with the session helper

Requires Python 3.10 or later. No package installation, API key, or network access is required for the helper.

```bash
python career.py init --session ../private-career-session
python career.py status --session ../private-career-session
python career.py next --session ../private-career-session
```

`next` creates `next-prompt.md` in the private session. Give that file and the relevant private records to your chosen assistant. The assistant must still read AGENTS.md. The file includes personal information once intake has begun; share only with the chosen runtime.

Optional resume intake:

```bash
python career.py import-resume --session ../private-career-session --file /path/to/resume.docx
```

The helper copies the original into private storage and records its checksum. Extraction and visual review are the assistant's responsibility; the helper does not parse DOCX or PDF.

Check records and mark a stage complete after the participant has reviewed the result:

```bash
python career.py validate --session ../private-career-session
python career.py complete --session ../private-career-session --stage intake --confirmed
```

`--confirmed` is an attestation that the participant approved that stage. An assistant must not use it without an explicit participant confirmation in the current session. See [`docs/session-guide.md`](docs/session-guide.md) for stage-specific requirements, blocked research, and resuming sessions.

## What the participant receives

1. A verified master career profile and comprehensive master resume.
2. Career criteria separating requirements, preferences, and learning interests.
3. Direct, adjacent, and stretch role suggestions with transferable skills and gaps.
4. Dated compensation evidence and separate current-scope, external-move, and stretch recommendations.
5. LinkedIn copy and a justified selection of other career websites.
6. An action plan covering search, networking, negotiation, learning, and longer-term growth.

Optional modules cover tailored application resumes, recruiter messages, application tracking, interview preparation, and offer comparison. The master resume is a source document, not the default application resume.

## Expected time

Initial planning estimate: 60–90 minutes for intake and interviews, 20–40 minutes for review, and approximately 30–90 minutes for AI research and preparation. Advertise about 1½–2½ hours of participant involvement, with research potentially extending elapsed time. Re-estimate after resume intake; extensive careers, pivots, missing records, or multiple markets can take longer. Short sessions are supported.

## Privacy and portability

The repository contains only reusable instructions, blank templates, code, and explicitly fictional examples. Candidate sessions must be outside the repository, even for a private GitHub repository. `.gitignore` is a second layer, not the storage policy. The helper refuses sessions inside the project and refuses overwriting an existing session.

An AI requires document-reading and file-writing capabilities. Current market conclusions also require live research; without it, save a blocked research status and a research plan, not invented salary numbers. Account changes and person-directed outreach require explicit authorization. See [`docs/runtime-capabilities.md`](docs/runtime-capabilities.md).

## Project layout

| Path | Purpose |
| --- | --- |
| `AGENTS.md`, `START_HERE.md` | Agent rules and opening behavior |
| `workflows/` | Stages, requirements, and completion criteria |
| `interviews/` | Adaptive questions and follow-up rules |
| `schemas/` | Machine-readable record contracts |
| `templates/` | Blank records and deliverable formats |
| `examples/` | Fictional scenarios and a structurally completed reference session |
| `career.py` | Local progress, validation, and prompt helper |
| `tests/`, `evaluations/` | Structural tests and qualitative evaluation rubric |

## Verification

```bash
python -m unittest discover -s tests -v
python career.py validate --session examples/reference-session --fictional
```

Tests validate isolation, stage ordering, evidence references, confirmation gates, research requirements, and resume generation. They do not establish the quality of an AI interview or validate real-world salary recommendations. Use the scenario rubric in `evaluations/README.md` with a live assistant before claiming production readiness.

## GitHub setup

See [`docs/github-setup.md`](docs/github-setup.md). Start with a private repository named `JobHuntAI`; make it public only after reviewing its contents. Do not upload source resumes or private sessions. A downloaded ZIP is a project snapshot; the GitHub repository is the canonical project.

## License

MIT licensed. See [LICENSE](LICENSE). The reusable workflow and helper can be adapted and redistributed; participant records are separate private data.
