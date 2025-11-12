import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from ..core.config import get_settings

settings = get_settings()


class StorageService:
    """
    Service for generating presigned URLs for S3/R2 storage.
    This follows the security pattern mandated in the PRD.
    """

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key_id,
            aws_secret_access_key=settings.s3_secret_access_key,
            region_name=settings.s3_region,
            config=Config(signature_version='s3v4'),
        )
        self.bucket_name = settings.s3_bucket_name

    def generate_presigned_upload_url(
        self,
        storage_path: str,
        content_type: str,
        expires_in: int = 300,  # 5 minutes
    ) -> str:
        """
        Generate a presigned POST URL for direct client-to-S3 upload.

        Args:
            storage_path: The S3 key path (e.g., tenant_id/project_id/filename)
            content_type: MIME type of the file
            expires_in: URL expiration time in seconds

        Returns:
            Presigned URL for upload
        """
        try:
            presigned_url = self.s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': storage_path,
                    'ContentType': content_type,
                },
                ExpiresIn=expires_in,
            )
            return presigned_url
        except ClientError as e:
            raise Exception(f"Failed to generate presigned URL: {str(e)}")

    def generate_presigned_download_url(
        self,
        storage_path: str,
        expires_in: int = 3600,  # 1 hour
    ) -> str:
        """
        Generate a presigned GET URL for downloading files.

        Args:
            storage_path: The S3 key path
            expires_in: URL expiration time in seconds

        Returns:
            Presigned URL for download
        """
        try:
            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': storage_path,
                },
                ExpiresIn=expires_in,
            )
            return presigned_url
        except ClientError as e:
            raise Exception(f"Failed to generate presigned URL: {str(e)}")

    def verify_file_exists(self, storage_path: str) -> bool:
        """
        Verify that a file exists in S3/R2.

        Args:
            storage_path: The S3 key path

        Returns:
            True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=storage_path)
            return True
        except ClientError:
            return False


# Singleton instance
storage_service = StorageService()
