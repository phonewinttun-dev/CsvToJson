from db_helper import insert_locations
from json_converter import *
from flask import Flask, request, jsonify, send_file, render_template
from file_cleanup import cleanup_old_files
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():

    # Clean up old files before new uploads
    cleanup_old_files(UPLOAD_FOLDER)
    cleanup_old_files(OUTPUT_FOLDER)

    file = request.files['file']

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename
    base_name, _ = os.path.splitext(filename)
    csv_path = os.path.join(UPLOAD_FOLDER, filename)
    json_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.json")

    file.save(csv_path)

    try:
        json_data = csv_to_dict_list(csv_path)
        if json_data is None:
            return jsonify({"error": "Invalid CSV format"}), 400

        inserted = insert_locations(json_data)
        if inserted == 0:
            return jsonify({
                "status": "success",
                "rows_processed": len(json_data),
                "rows_inserted": inserted
            })

        output_file = generate_json_file(json_data, json_path)

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
