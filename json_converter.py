import os
import csv
import json
import re

# Folder setup
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def normalize_key(key: str) -> str:
    return (
        key.replace("\ufeff", "")   # remove BOM if present
           .strip()
           .lower()
           .replace(" / ", "_")
           .replace(" ", "_")
    )


def clean_value(value):
    if value is None:
        return None
    return value.strip()

def csv_to_dict_list(csv_filepath):
    data = []

    try:
        with open(csv_filepath, encoding="utf-8-sig", newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                normalized_row = {
                    normalize_key(k): clean_value(v)
                    for k, v in row.items()
                }

                if "region" not in normalized_row:
                    raise RuntimeError(f"Region column missing. Got keys: {list(normalized_row.keys())}")

                record = {
                    "region": normalized_row["region"],
                    "township": normalized_row["town_township"],
                    "quarter_village_tract": normalized_row["quarter_village_tract"],
                    "postal_code": int(normalized_row["postal_code"]),
                    "is_deleted": False
                }

                data.append(record)

        return data

    except KeyError as e:
        raise RuntimeError(f"Missing expected CSV column: {e}")
    except Exception as e:
        raise RuntimeError(f"CSV read error: {e}")

def generate_json_file(data, output_filepath):
    try:
        with open(output_filepath, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, indent=4, ensure_ascii=False)
        return output_filepath

    except Exception as e:
        raise RuntimeError(f"JSON write error: {e}")
