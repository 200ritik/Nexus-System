import psycopg2

from configuration.config import (
    postgres_host,
    postgres_port,
    postgres_database,
    postgres_user,
    postgres_password,
)

def get_postgres_connection():

    connection = psycopg2.connect(
        host=postgres_host,
        port=postgres_port,
        database=postgres_database,
        user=postgres_user,
        password=postgres_password,
    )
    return connection



