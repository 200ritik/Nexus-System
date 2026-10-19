import logging
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from configuration.jwt_configuration import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

logger = logging.getLogger(__name__)


def create_access_token(
    user_id: str,
) -> str:

    issued_at = datetime.now(timezone.utc)

    expires_at = (
        issued_at
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": user_id,
        "iat": issued_at,
        "exp": expires_at,
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    logger.info(
        "Access token created | user_id=%s",
        user_id,
    )

    return token


def verify_access_token(
    token: str,
) -> dict:

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if not user_id:
            raise InvalidTokenError(
                "Token subject is missing."
            )

        return payload

    except InvalidTokenError:
        logger.warning(
            "Invalid JWT received."
        )
        raise