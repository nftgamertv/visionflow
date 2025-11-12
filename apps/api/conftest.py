"""
Pytest configuration for API tests
"""
import os

# Set test environment variables
os.environ["SUPABASE_URL"] = "http://localhost:54321"
os.environ["SUPABASE_ANON_KEY"] = "test-key"
os.environ["SUPABASE_JWT_SECRET"] = "test-secret"
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/postgres"
os.environ["REDIS_URL"] = "redis://localhost:6379"
os.environ["S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["S3_ACCESS_KEY_ID"] = "test"
os.environ["S3_SECRET_ACCESS_KEY"] = "test"
os.environ["S3_BUCKET_NAME"] = "test-bucket"
