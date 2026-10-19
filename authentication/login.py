import logging

import pwdlib

from database.postgresql.connection import (
    get_postgres_connection,
)

from authentication.jwt_token_creation import (
    create_access_token,
)


logger = logging.getLogger(__name__)

password_hasher = pwdlib.PasswordHash.recommended()


def user_login(
    email: str,
    password: str,
) -> dict:

    connection = None
    cursor = None

    try:
        connection = get_postgres_connection()
        cursor = connection.cursor()

        # Find user
        query = """
            SELECT
                user_id,
                username,
                email,
                password_hash
            FROM users
            WHERE email = %s;
        """

        cursor.execute(
            query,
            (email,),
        )

        user = cursor.fetchone()

        if user is None:
            raise ValueError(
                "Invalid email or password."
            )

        (
            user_id,
            username,
            stored_email,
            stored_password_hash,
        ) = user

        # Verify password
        password_valid = password_hasher.verify(
            password,
            stored_password_hash,
        )

        if not password_valid:
            raise ValueError(
                "Invalid email or password."
            )

        # Create JWT only after successful authentication
        access_token = create_access_token(
            user_id=str(user_id)
        )

        logger.info(
            "User login successful | user_id=%s",
            user_id,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    except ValueError:
        raise

    except Exception:
        if connection:
            connection.rollback()

        logger.exception(
            "User login failed | email=%s",
            email,
        )

        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()