from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from ..core.database import get_db
from ..dependencies.auth import get_current_user, AuthenticatedUser
from ..models.schemas import Annotation, AnnotationCreate

router = APIRouter(prefix="/annotations", tags=["annotations"])


@router.post("", response_model=Annotation, status_code=status.HTTP_201_CREATED)
async def create_annotation(
    annotation: AnnotationCreate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new annotation.
    This is called when the user saves an annotation in the workbench.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Database schema not yet initialized",
    )


@router.get("/image/{image_id}", response_model=List[Annotation])
async def get_image_annotations(
    image_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get all annotations for an image.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Database schema not yet initialized",
    )


@router.put("/{annotation_id}", response_model=Annotation)
async def update_annotation(
    annotation_id: UUID,
    annotation: AnnotationCreate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update an existing annotation.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Database schema not yet initialized",
    )


@router.delete("/{annotation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_annotation(
    annotation_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete an annotation.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Database schema not yet initialized",
    )
