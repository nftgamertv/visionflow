from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from ..core.database import get_db
from ..dependencies.auth import get_current_user, AuthenticatedUser
from ..models.schemas import (
    Project,
    ProjectCreate,
    PresignedUploadRequest,
    PresignedUploadResponse,
)
from ..services.storage import storage_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new project.
    Requires authentication and workspace membership.
    """
    # This will be implemented with SQLAlchemy models
    # For now, return a placeholder to avoid errors
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Database schema not yet initialized",
    )


@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get a project by ID.
    RLS will ensure user can only see projects in their workspace.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Database schema not yet initialized",
    )


@router.post("/{project_id}/upload_url", response_model=PresignedUploadResponse)
async def get_upload_url(
    project_id: UUID,
    request: PresignedUploadRequest,
    user: AuthenticatedUser = Depends(get_current_user),
):
    """
    Generate a presigned URL for direct client-to-S3 upload.
    This is step 1 of the secure upload flow.
    """
    if not user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must be associated with a workspace",
        )

    # Generate storage path: tenant_id/project_id/filename
    storage_path = f"{user.tenant_id}/{project_id}/{request.filename}"

    try:
        presigned_url = storage_service.generate_presigned_upload_url(
            storage_path=storage_path,
            content_type=request.content_type,
            expires_in=300,  # 5 minutes
        )

        return PresignedUploadResponse(
            presigned_url=presigned_url,
            storage_path=storage_path,
            expires_in=300,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate upload URL: {str(e)}",
        )
