import os
import csv
import json
import re

# Folder setup
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Regex pattern for unwanted characters
pattern = r"(?:\s|''|/)"

#Function to check if text contains spaces, empty quotes, or slashes.
def character_checker(text):
    return bool(re.search(pattern, text))

#Remove slashes (/), empty quotes ('') and extra spaces.
def clear_character(text):
    
    # Remove empty quotes and slashes
    cleaned = re.sub(r"''|/+", '', text)
    # Replace multiple spaces with one
    cleaned = re.sub(r'\s+', ' ', cleaned)
    # Trim spaces at start and end
    cleaned = cleaned.strip()
    return cleaned


def fix_nested_json(data):

    fixed_data = {}

    for key, value in data.items():
        if isinstance(value, str):
            value = value.strip()

            # Detect if the value looks like JSON (starts with [ or {)
            if (value.startswith('[') and value.endswith(']')) or (value.startswith('{') and value.endswith('}')):
                try:
                    fixed_data[key] = json.loads(value)
                    continue
                except json.JSONDecodeError:
                    pass

            # Clean other normal string fields
            if character_checker(value):
                value = clear_character(value)

        fixed_data[key] = value

    return fixed_data


def csv_to_dict_list(csv_filepath):
    data = []
    try:
        with open(csv_filepath, encoding='utf-8', newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)

            for row in csv_reader:
                
                cleaned_row = fix_nested_json(row)
                data.append(cleaned_row)
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
