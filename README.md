# CSV to JSON Converter (Flask App)

A lightweight Python Flask web application that allows users to upload a CSV file and automatically convert it into a JSON file with the same filename.

> Example: Upload `students.csv` → download `students.json`

Originally designed for general CSV-to-JSON conversion, it was later adapted as a utility for extracting postal codes from CSV to JSON.

---

## Features

- Converts valid CSV file to JSON format
- Automatically names the output file (same name as uploaded CSV)
- Auto-cleans old uploaded/generated files

---

## Project Structure

```
CSVTOJSON/

├── db.config.py # Database setup and configuration (added to .gitignore)
├── dbhelper.py # Helper functions for bulk data insertion
├── jsonconverter.py # CSV to JSON conversion methods
├── filecleanup.py # Methods for cleaning up old files
├── routes.py # Main Flask application routes
├── uploads/ # Temporary folder for uploaded CSV files
└── outputs/ # Folder for generated JSON files

```

## Requirements

Make sure you have:

- **Python 3.8+**
- **pip**
- **Flask**

## ⚙️ Installation

### Clone or download this repository

```bash

git clone https://github.com/yourusername/PostalCodesCsvToJson
cd csv_to_json

```

---

### Manaul Setup

- Create a virtual environment

For Windows,

```bash
python -m venv venv
```

For MacOS/Linux

```
source venv/bin/activate
```

After creating a virtual environment,

- Activate the virtual environment:

For Windows users,

```bash
venv\Scripts\activate
```

For MacOS/Linux users:

```bash
source venv\bin\activate
```

### Dependencies Installation

```bash
pip install flask
```

And run the app in terminal

```bash
python routes.py
```

### Database schema:

| Column                | Type                          | Description                |
| --------------------- | ----------------------------- | -------------------------- |
| region                | VARCHAR(120)                  | Region name                |
| township              | VARCHAR(120)                  | Township name              |
| quarter/village/tract | VARCHAR(120)                  | Quarter, village, or tract |
| postalcode            | INTEGER (PRIMARY KEY, UNIQUE) | Postal code                |
| isdeleted             | BOOLEAN (DEFAULT FALSE)       | Deletion flag              |

---

### Usage

- Start the Flask app by running `python routes.py`.

- Open your browser and navigate to http://localhost:5000 (or the configured port).

- Upload a CSV file via the web interface.

- Download the generated JSON file from the outputs folder.
