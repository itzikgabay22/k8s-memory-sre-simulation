#!/usr/bin/env bash
set -euo pipefail

kubectl -n memory-sim get pods -w &
WATCH_PID="$!"

sleep 20
kill "$WATCH_PID" 2>/dev/null || true

kubectl -n memory-sim describe deployment/memory-hungry-api
kubectl -n memory-sim get pods
kubectl -n memory-sim get events --sort-by=.lastTimestamp | tail -30
