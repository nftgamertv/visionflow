from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .routers import projects, images, annotations

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router, prefix=settings.api_v1_prefix)
app.include_router(images.router, prefix=settings.api_v1_prefix)
app.include_router(annotations.router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    return {"message": "VisionFlow API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get(f"{settings.api_v1_prefix}/openapi.json")
async def get_openapi():
    """
    Export OpenAPI schema for type generation.
    This is used by packages/shared-types to generate Zod schemas.
    """
    return app.openapi()
