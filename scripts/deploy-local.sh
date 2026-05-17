#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-docker-desktop}"
IMAGE="memory-hungry-api:local"

case "$TARGET" in
  docker-desktop)
    kubectl config use-context docker-desktop
    docker build -t "$IMAGE" .
    ;;
  minikube)
    kubectl config use-context minikube
    eval "$(minikube docker-env)"
    docker build -t "$IMAGE" .
    ;;
  *)
    echo "Usage: $0 docker-desktop|minikube" >&2
    exit 2
    ;;
esac

kubectl apply -k k8s
kubectl -n memory-sim rollout restart deployment/memory-hungry-api
kubectl -n memory-sim get deployment,pods,events
