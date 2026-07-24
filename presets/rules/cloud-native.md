# Cloud Native Rules

- Applications must follow the 12-Factor App methodology.
- Containerize all applications using Docker with multi-stage builds to minimize image size.
- Do not hardcode configurations; read from environment variables or ConfigMaps/Secrets.
- Implement readiness and liveness probes for Kubernetes.
- Ensure graceful shutdown by handling SIGTERM signals.