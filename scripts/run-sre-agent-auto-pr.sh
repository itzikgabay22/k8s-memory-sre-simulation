#!/usr/bin/env bash
set -euo pipefail

: "${CURSOR_API_KEY:?Set CURSOR_API_KEY before running the agent}"
: "${REPO_URL:=https://github.com/itzikgabay22/k8s-memory-sre-simulation}"

PROM_ARGS=()
if [[ -n "${PROMETHEUS_URL:-}" ]]; then
  PROM_ARGS+=(--prometheus-url "$PROMETHEUS_URL")
fi

devops-sre-agent run \
  "The deployment is restarting with OOMKilled symptoms. Review Kubernetes evidence and raise memory requests/limits safely." \
  --repo-url "$REPO_URL" \
  --ref main \
  --namespace memory-sim \
  --workload deployment/memory-hungry-api \
  --scenario resource-safety \
  "${PROM_ARGS[@]}" \
  --auto-pr
