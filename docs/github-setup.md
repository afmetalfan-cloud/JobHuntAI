# Publish the generic project

Create an empty repository named `JobHuntAI` in your GitHub account. A private repository is the suggested initial visibility. Do not initialize it with a README if pushing this snapshot as the first commit.

## Browser upload

Unzip the project and upload its contents into the repository. Include `AGENTS.md`, `START_HERE.md`, and the directories. GitHub browser upload may omit hidden configuration files; inspect `.gitignore` and `.github/workflows/checks.yml` separately. Commit the generic files only.

## Git CLI

From the extracted project directory, with your own authorized GitHub credentials:

```bash
git init -b main
git add .
git diff --cached --stat
git commit -m "Add reusable career development workflow"
git remote add origin https://github.com/YOUR-LOGIN/JobHuntAI.git
git push -u origin main
```

Replace YOUR-LOGIN with the actual account owner. Review staged content before pushing. Do not commit private sessions, original resumes, local credentials, or source materials. The reusable project is MIT licensed. Template-repository settings are optional; every participant still needs an external private workspace.

This project includes a proposed CI workflow that runs structural checks. It has not been executed on GitHub until you see a successful repository workflow run. Local tests are documented separately.
