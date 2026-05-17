# Jira Branch Integration

The workflow `.github/workflows/jira-branch-running.yml` moves a Jira issue to
`Running` or `In Progress` when a GitHub branch or pull request branch contains a Jira
issue key.

Examples:

- `KAN-26/memory-limit-simulation`
- `feature/KAN-26-memory-limit-simulation`
- `codex/KAN-26-memory-limit-simulation`

## Required Secrets

Set these repository secrets in GitHub:

- `JIRA_BASE_URL`: `https://gabay.atlassian.net`
- `JIRA_EMAIL`: your Atlassian account email.
- `JIRA_API_TOKEN`: an Atlassian API token with Jira issue transition permission.

The workflow discovers the correct transition dynamically by looking for transition or
destination status names equal to `Running` or `In Progress`.

For this Jira project, `KAN-26` currently exposes `In Progress` as transition id `21`,
but the workflow does not hardcode that id.
