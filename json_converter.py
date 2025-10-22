import os
import csv
import json


UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def csv_to_json_list(csv_filepath):
    data = []
    try:
        with open(csv_filepath, encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                data.append(row)
        return data
    except Exception as e:
        print(f"Error while reading CSV: {e}")
        return None

def generate_json_file(data, output_filepath):
    try:
        with open(output_filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4, ensure_ascii=False)
        return output_filepath
    except Exception as e:
        print(f"Error while writing JSON: {e}")
        return None

