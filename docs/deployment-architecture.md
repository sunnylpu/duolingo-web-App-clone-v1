# Deployment Architecture Blueprint

```text
  LOCAL DEV            CI/CD PIPELINE             CONTAINERIZATION           PRODUCTION ORCHESTRATION
┌───────────┐         ┌──────────────┐          ┌─────────────────┐        ┌─────────────────────────┐
│ Git Repo  │ ──────> │ Jenkins CI   │ ───────> │ Docker Images   │ ─────> │ Kubernetes (EKS / AWS)  │
│ (v1.0.0)  │         │ (Build/Test) │          │ (Frontend/Back) │        │ (Pods, Ingress, HPA)    │
└───────────┘         └──────────────┘          └─────────────────┘        └─────────────────────────┘
```

## Intended Deployment Pipeline
1. **Docker Containerization**: Multi-stage Dockerfiles for FastAPI backend & Next.js frontend.
2. **Jenkins CI/CD**: Automated execution of `./scripts/release-check.sh`, Docker build, security scan, image tag, and deployment trigger.
3. **Kubernetes Orchestration**: Deployment manifests, Horizontal Pod Autoscaling (HPA), Liveness & Readiness Probes (`/health/live`, `/health/ready`), ConfigMaps & Secrets.
4. **AWS Infrastructure**: Production cloud deployment on AWS EKS with Ingress Controller.
