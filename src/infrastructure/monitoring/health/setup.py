from .client import Health


health = Health(
    ("/api/-/health/readiness",),
    ("/api/-/health/liveness",),
    ("/api/-/health/startup",),
)
