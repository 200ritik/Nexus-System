# creating the postgresql environment

from database.postgresql.connection import get_postgres_connection
import logging
import json


logger = logging.getLogger(__name__)

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

JSON_FILE = "medicines.json"


# --------------------------------------------------
# INSERT QUERY
# --------------------------------------------------

INSERT_QUERY = """
INSERT INTO medicines (
    medicine_name,
    composition,
    uses,
    side_effects,
    manufacturer
)
VALUES (%s, %s, %s, %s, %s);
"""


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    # Load JSON
    with open(
        JSON_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    medicines = data["medicines"]

    print(
        f"Loaded {len(medicines)} medicines."
    )

    # PostgreSQL connection
    connection = get_postgres_connection()

    cursor = connection.cursor()

    try:

        # Insert medicines
        for medicine in medicines:

            cursor.execute(
                INSERT_QUERY,
                (
                    medicine.get("Medicine Name"),
                    medicine.get("Composition"),
                    medicine.get("Uses"),
                    medicine.get("Side_effects"),
                    medicine.get("Manufacturer")
                )
            )

        # Commit once
        connection.commit()

        print(
            f"Successfully inserted "
            f"{len(medicines)} medicines."
        )

    except Exception as e:

        connection.rollback()

        logger.error(
            "Failed to insert medicines: %s",
            e
        )

        raise

    finally:

        cursor.close()
        connection.close()


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    main()