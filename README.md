# 🧩 CSV to JSON Converter (Flask App)

A lightweight Python Flask web application that allows users to upload a CSV file and automatically convert it into a JSON file with the same filename.

> Example: Upload `students.csv` → download `students.json`

---

## 🚀 Features

- Converts any valid CSV file to JSON format
- Automatically names the output file (same name as uploaded CSV)
- Auto-cleans old uploaded/generated files

---

## 📁 Project Structure

CSVTOJSON
│
├── json_converter.py # CSV to JSON converter methods
├── file_cleanup.py # method to clean up old files
├── routes.py # Main Flask application
├── uploads/ # Temporary folder for uploaded CSV files
├── outputs/ # Folder for generated JSON files

## 🧱 Requirements

Make sure you have:

- **Python 3.8+**
- **pip**
- **Flask**

## ⚙️ Installation

### Clone or download this repository

```bash

git clone https://github.com/yourusername/flask_csv_to_json.git
cd flask_csv_to_json


```

---

### Manaul Setup

- Create a virtual environment

```bash

python -m venv venv

```

After creating a virtual environment

Activate the virtual environment

For Windows users,

```bash

venv\Scripts\activate


```

### Dependencies Installation

```bash

pip install flask

```

And run the app in terminal

```bash

python routes.py

```

- region VARCHAR(120)
- township VARCHAR(120)
- quarter_village_tract VARCHAR(120)
- postal_code integer PRIMARY KEY UNIQUE
- is_deleted boolean DEFAULT false
