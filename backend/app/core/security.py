"""
SkillBridge AI — Security Utilities.

Provides password hashing, verification, and JWT token structure.
Actual JWT authentication will be implemented in a later phase.
"""

from passlib.context import CryptContext

from app.core.config import get_settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt.

    Args:
        password: The plain-text password to hash.

    Returns:
        The bcrypt-hashed password string.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash.

    Args:
        plain_password: The plain-text password to verify.
        hashed_password: The bcrypt hash to compare against.

    Returns:
        True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, object]) -> str:
    """Create a JWT access token.

    This is a structural placeholder. Full JWT implementation
    will be added in the authentication phase.

    Args:
        data: The payload data to encode in the token.

    Returns:
        The encoded JWT string.
    """
    from datetime import datetime, timedelta, timezone

    from jose import jwt

    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, object]:
    """Decode and validate a JWT access token.

    This is a structural placeholder. Full JWT validation
    will be added in the authentication phase.

    Args:
        token: The JWT string to decode.

    Returns:
        The decoded payload dictionary.

    Raises:
        JWTError: If the token is invalid or expired.
    """
    from jose import jwt

    settings = get_settings()
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )
