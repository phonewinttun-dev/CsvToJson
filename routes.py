from json_converter import *
from flask import Flask, request, jsonify, send_file, render_template
from file_cleanup import cleanup_old_files
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('templates/index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return jsonify({"message": "Please upload a CSV file from the home page."}), 200
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

    json_data = csv_to_dict_list(csv_path)
    if json_data is None:
        return jsonify({"error": "Invalid CSV format"}), 400

    output_file = generate_json_file(json_data, json_path)

    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)