from database.postgresql.connection import get_postgres_connection


connection = get_postgres_connection()

print("PostgreSQL connection successful!")

connection.close()