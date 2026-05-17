# SRE Agent Scenario

This scenario demonstrates a memory limit that is lower than the service's startup
working set.

## Expected Kubernetes Evidence

- Pod restart count increases.
- Pod status may show `CrashLoopBackOff`.
- The previous container state should show `reason: OOMKilled`.
- Events may include container kill or backoff messages.
- The Deployment manifest shows `MEMORY_ALLOC_MB=96` with `limits.memory=64Mi`.

## Expected Agent Recommendation

The SRE agent should recommend increasing memory resources. A safe first fix is:

```yaml
resources:
  requests:
    cpu: 50m
    memory: 128Mi
  limits:
    cpu: 250m
    memory: 256Mi
```

The PR should keep probes and the service contract unchanged.
