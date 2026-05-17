# k8s-memory-sre-simulation

Simulation repo for `KAN-26`: a small Kubernetes service that intentionally runs with a
memory limit that is too low. The goal is to run it on minikube or Docker Desktop
Kubernetes, let the DevOps SRE Agent collect the failure evidence, and ask Cursor Cloud
Agent to open a PR that raises the memory request/limit.

## What This Simulates

- A Python HTTP service allocates memory on startup using `MEMORY_ALLOC_MB`.
- The Kubernetes Deployment sets `MEMORY_ALLOC_MB=96`.
- The Deployment intentionally limits the container to `64Mi`.
- The expected failure is `OOMKilled`, restart loops, or very high memory saturation.

The SRE agent should identify that the memory limit is too low and propose a PR that
raises memory resources, for example to `requests.memory: 128Mi` and `limits.memory:
256Mi`.

## Local Prerequisites

- Docker Desktop with Kubernetes enabled, or minikube.
- `kubectl`.
- Python 3.11+.
- A `CURSOR_API_KEY` for the DevOps SRE Agent.
- The `devops-sre-agent` CLI installed from
  `https://github.com/itzikgabay22/devops-sre-agent`.

## Run On Docker Desktop Kubernetes

```bash
./scripts/deploy-local.sh docker-desktop
./scripts/watch-failure.sh
```

## Run On minikube

```bash
minikube start
./scripts/deploy-local.sh minikube
./scripts/watch-failure.sh
```

## Ask The SRE Agent To Open A PR

Set the repo URL to this repository after it is pushed to GitHub:

```bash
export CURSOR_API_KEY="your_cursor_api_key"
export REPO_URL="https://github.com/itzikgabay22/k8s-memory-sre-simulation"

./scripts/run-sre-agent-auto-pr.sh
```

The script runs:

```bash
devops-sre-agent run \
  "The deployment is restarting with OOMKilled symptoms. Review Kubernetes evidence and raise memory requests/limits safely." \
  --repo-url "$REPO_URL" \
  --ref main \
  --namespace memory-sim \
  --workload deployment/memory-hungry-api \
  --scenario resource-safety \
  --auto-pr
```

If Prometheus is available locally, add:

```bash
export PROMETHEUS_URL="http://localhost:9090"
```

## Jira Branch Automation

The workflow `.github/workflows/jira-branch-running.yml` transitions a Jira issue to
`Running` or `In Progress` when a branch or PR branch contains a key like `KAN-26`.

Required GitHub repository secrets:

- `JIRA_BASE_URL`: `https://gabay.atlassian.net`
- `JIRA_EMAIL`: Atlassian account email.
- `JIRA_API_TOKEN`: Atlassian API token.

See `docs/jira-integration.md`.
