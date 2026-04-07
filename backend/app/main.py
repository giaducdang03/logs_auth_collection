from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import Base, engine
from app.api import router as auth_router
from app.api.logs import router as logs_router
from app.api.dashboard import router as dashboard_router
from app.tasks import start_scheduler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Create tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="SSH Auth Log Monitor",
    description="API for SSH authentication log monitoring",
    version="1.0.0",
    root_path=settings.backend_root_path,
)


@app.middleware("http")
async def root_path_proxy_middleware(request, call_next):
    """Support deployments where proxy forwards path with backend root prefix."""
    root_prefix = (settings.backend_root_path or "").rstrip("/")
    request_path = request.scope.get("path", "")

    if root_prefix and request_path.startswith(root_prefix):
        stripped_path = request_path[len(root_prefix):] or "/"
        request.scope["root_path"] = root_prefix
        request.scope["path"] = stripped_path

    return await call_next(request)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(logs_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")


@app.on_event("startup")
def startup_event():
    """Start scheduler and run initial log collection when app starts"""
    app.state.scheduler = start_scheduler(run_on_startup=True)


@app.on_event("shutdown")
def shutdown_event():
    """Shutdown scheduler when app stops"""
    scheduler = getattr(app.state, "scheduler", None)
    if scheduler:
        scheduler.shutdown()


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
