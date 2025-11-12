from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel
from uuid import UUID
from ..core.config import get_settings

security = HTTPBearer()
settings = get_settings()


class AuthenticatedUser(BaseModel):
    id: UUID
    email: str
    tenant_id: UUID | None = None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AuthenticatedUser:
    """
    Validates Supabase JWT token and returns authenticated user.
    This is a dependency that should be injected into all protected endpoints.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
        )

        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract tenant_id from custom claims if it exists
        tenant_id = payload.get("tenant_id")

        return AuthenticatedUser(
            id=UUID(user_id),
            email=email,
            tenant_id=UUID(tenant_id) if tenant_id else None,
        )

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token format: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


class RoleRequired:
    """
    Dependency for checking user roles at project level.
    Usage: @Depends(RoleRequired("admin"))
    """

    def __init__(self, required_role: str):
        self.required_role = required_role

    async def __call__(self, user: AuthenticatedUser = Depends(get_current_user)):
        # This will be implemented when we add project_members table
        # For now, just return the user
        return user
