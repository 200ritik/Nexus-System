
import pandas as pd
import json
import os


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

INPUT_FILE = "C:/Users/ritik/Downloads/Medicine_Details.csv/Medicine_Details.csv"
OUTPUT_FILE = "medicines.json"


# --------------------------------------------------
# LOAD CSV
# --------------------------------------------------

def load_csv(file_path: str) -> pd.DataFrame:
    """Load the medicine CSV file."""

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    print("CSV loaded successfully.")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    return df


# --------------------------------------------------
# CLEAN DATA
# --------------------------------------------------

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean data and remove unnecessary columns."""

    # Remove Image URL
    if "Image URL" in df.columns:
        df = df.drop(columns=["Image URL"])
        print("Removed column: Image URL")
        
    if "Excellent Review %" in df.columns:
        df = df.drop(columns=["Excellent Review %"])
        
    if "Average Review %" in df.columns:
        df = df.drop(columns=["Average Review %"])
        
    if "Poor Review %" in df.columns:
        df = df.drop(columns=["Poor Review %"])
            

    # Replace missing values
    df = df.fillna("")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Clean text values
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].astype(str).str.strip()

    # Remove completely empty rows
    df = df.dropna(how="all")

    return df


# --------------------------------------------------
# CONVERT TO JSON
# --------------------------------------------------

def convert_to_json(
    df: pd.DataFrame,
    output_file: str
):
    """Convert DataFrame into JSON."""

    medicines = df.to_dict(orient="records")

    output = {
        "metadata": {
            "record_count": len(medicines),
            "source": "Medicine CSV Dataset",
            "description": "Medicine information dataset"
        },
        "medicines": medicines
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\nJSON created successfully.")
    print(f"Output: {output_file}")
    print(f"Medicines: {len(medicines)}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("=" * 50)
    print("MEDICINE CSV → JSON CONVERTER")
    print("=" * 50)

    # Load CSV
    df = load_csv(INPUT_FILE)

    # Show original columns
    print("\nOriginal columns:")
    for column in df.columns:
        print(f"  - {column}")

    # Clean data
    df = clean_data(df)

    # Show final columns
    print("\nFinal columns:")
    for column in df.columns:
        print(f"  - {column}")

    # Convert to JSON
    convert_to_json(
        df,
        OUTPUT_FILE
    )

    print("\nConversion completed successfully.")


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    main()