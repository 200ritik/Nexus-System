import logging
import uuid

import pwdlib

from database.postgresql.connection import (
    get_postgres_connection,
)


logger = logging.getLogger(__name__)

password_hasher = pwdlib.PasswordHash.recommended()


def user_registration(
    user_name: str,
    email: str,
    password: str,
) -> dict:

    connection = None
    cursor = None

    try:
        connection = get_postgres_connection()
        cursor = connection.cursor()

        # Check existing email
        query = """
            SELECT user_id
            FROM users
            WHERE email = %s;
        """

        cursor.execute(
            query,
            (email,),
        )

        existing_user = cursor.fetchone()

        if existing_user:
            raise ValueError(
                "User with this email already exists."
            )

        # Generate unique user ID
        user_id = str(uuid.uuid4())

        # Hash password
        hashed_password = password_hasher.hash(
            password
        )

        # Insert user
        query = """
            INSERT INTO users (
                user_id,
                username,
                email,
                password_hash
            )
            VALUES (%s, %s, %s, %s);
        """

        cursor.execute(
            query,
            (
                user_id,
                user_name,
                email,
                hashed_password,
            ),
        )

        connection.commit()

        logger.info(
            "User registered successfully | user_id=%s",
            user_id,
        )

        return {
            "user_id": user_id,
            "username": user_name,
            "email": email,
        }

    except ValueError:
        if connection:
            connection.rollback()
        raise

    except Exception:
        if connection:
            connection.rollback()

        logger.exception(
            "User registration failed | email=%s",
            email,
        )

        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()