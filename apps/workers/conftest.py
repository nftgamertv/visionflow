"""
Pytest configuration for worker tests
"""
import os

# Set test environment variables
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/postgres"
os.environ["REDIS_URL"] = "redis://localhost:6379"
os.environ["S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["S3_ACCESS_KEY_ID"] = "test"
os.environ["S3_SECRET_ACCESS_KEY"] = "test"
os.environ["S3_BUCKET_NAME"] = "test-bucket"
