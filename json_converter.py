import os
import csv
import json
import re

from db_helper import sync_regions

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
    unique_regions = set()
    raw_records = []

    try:
        with open(csv_filepath, encoding="utf-8-sig", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                normalized_row = {normalize_key(k): clean_value(v) for k, v in row.items()}

                if "region" in normalized_row:
                    unique_regions.add(normalized_row["region"])

                raw_records.append(normalized_row)

        region_map = sync_regions(list(unique_regions))

        for rec in raw_records:
            final_record = {
                "region": rec["region"],
                "township": rec.get("town_township"), # Key check
                "quarter_village_tract": rec.get("quarter_village_tract"),
                "postal_code": int(rec["postal_code"]),
                "region_id": region_map.get(rec["region"])
            }
            data.append(final_record)

        return data, region_map

    except Exception as e:
        raise RuntimeError(f"Processing error: {e}")

def generate_json_file(data, output_filepath):
    try:
        with open(output_filepath, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, indent=4, ensure_ascii=False)
        return output_filepath

    except Exception as e:
        raise RuntimeError(f"JSON write error: {e}")
