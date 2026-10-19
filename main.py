import logging
from authentication.current_user import get_current_user_id

from fastapi import FastAPI, HTTPException, status,Depends

from authentication.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
)

from authentication.registration import (
    user_registration,
)

from authentication.login import (
    user_login,
)


logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Medical System",
    version="1.0.0",
)

@app.get("/me")
def get_my_profile(
    user_id: str = Depends(get_current_user_id),
):
    return {"user_id": user_id}


# ============================================================
# REGISTER
# ============================================================

@app.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserCreate,
):

    try:

        created_user = user_registration(
            user_name=user.username,
            email=user.email,
            password=user.password,
        )

        return created_user

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )

    except Exception:

        logger.exception(
            "Unexpected registration error."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed.",
        )


# ============================================================
# LOGIN
# ============================================================

@app.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    user: UserLogin,
):

    try:

        result = user_login(
            email=user.email,
            password=user.password,
        )

        return result

    except ValueError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    except Exception:

        logger.exception(
            "Unexpected login error."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed.",
        )