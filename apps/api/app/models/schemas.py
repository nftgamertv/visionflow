from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Any


class WorkspaceBase(BaseModel):
    name: str


class WorkspaceCreate(WorkspaceBase):
    pass


class Workspace(WorkspaceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class ProjectBase(BaseModel):
    name: str
    project_type: str  # object_detection, segmentation, keypoint, etc.


class ProjectCreate(ProjectBase):
    workspace_id: UUID


class Project(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    created_at: datetime


class ImageBase(BaseModel):
    filename: str
    width: int
    height: int


class ImageCreate(ImageBase):
    project_id: UUID
    storage_path: str


class Image(ImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    storage_path: str
    created_at: datetime


class AnnotationBase(BaseModel):
    class_name: str
    data: dict[str, Any]
    status: str = "draft"  # draft, submitted, approved


class AnnotationCreate(AnnotationBase):
    image_id: UUID
    project_id: UUID


class Annotation(AnnotationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    image_id: UUID
    project_id: UUID
    annotator_id: UUID
    created_at: datetime
    updated_at: datetime


class PresignedUploadRequest(BaseModel):
    filename: str
    content_type: str


class PresignedUploadResponse(BaseModel):
    presigned_url: str
    storage_path: str
    expires_in: int


class CompleteUploadRequest(BaseModel):
    storage_path: str
    width: int
    height: int


class DatasetVersionBase(BaseModel):
    name: str
    config: dict[str, Any]


class DatasetVersionCreate(DatasetVersionBase):
    project_id: UUID


class DatasetVersion(DatasetVersionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    status: str  # QUEUED, PROCESSING, COMPLETED, FAILED
    created_at: datetime
    updated_at: datetime
