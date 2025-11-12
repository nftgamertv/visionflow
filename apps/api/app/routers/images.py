from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from ..core.database import get_db
from ..dependencies.auth import get_current_user, AuthenticatedUser
from ..models.schemas import Image, ImageCreate, CompleteUploadRequest
from ..services.storage import storage_service

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/complete_upload", response_model=Image, status_code=status.HTTP_201_CREATED)
async def complete_upload(
    request: CompleteUploadRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Complete the upload process after client uploads to S3.
    This is the final step of the secure upload flow.
    Verifies the file exists in S3 and creates the database record.
    """
    # Verify file exists in S3
    if not storage_service.verify_file_exists(request.storage_path):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File not found in storage. Upload may have failed.",
        )

    # This will create the image record in the database
    # For now, return a placeholder
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Database schema not yet initialized",
    )


@router.get("/{image_id}", response_model=Image)
async def get_image(
    image_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get an image by ID.
    Returns the image metadata with a presigned download URL.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Database schema not yet initialized",
    )
