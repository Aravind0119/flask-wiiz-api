

import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

VALID_API_KEY = os.getenv("API_KEY")

# POINT THIS TO YOUR ACTUAL FOLDER
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def is_valid_api_key():
    # Try header first
    api_key = request.headers.get("x-api-key")

    # If not in header, try URL query parameter (for Chrome testing)
    if not api_key:
        api_key = request.args.get("api_key")

    print("Received API Key:", api_key)
    print("Expected API Key:", VALID_API_KEY)

    return api_key == VALID_API_KEY


# -------- READ ROOT FILES --------
@app.route("/read-root-files", methods=["GET"])
def read_root_files():

    if not is_valid_api_key():
        return jsonify({"error": "Unauthorized - Invalid API Key"}), 401

    files = []
    all_files_data = []

    # Only read files in uploads root (ignore folders)
    for item in os.listdir(UPLOAD_FOLDER):
        full_path = os.path.join(UPLOAD_FOLDER, item)

        if os.path.isfile(full_path):
            files.append(item)

    if not files:
        return jsonify({"error": "No root files found"}), 404

    for filename in files:
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            content = f"Error reading file: {str(e)}"

        all_files_data.append({
            "filename": filename,
            "stored_path": file_path,
            "content": content
        })

    return jsonify({
        "location": "root",
        "total_files": len(all_files_data),
        "files": all_files_data
    }), 200


# -------- READ SPECIFIC FOLDER --------
@app.route("/read-folder/<folder_name>", methods=["GET"])
def read_folder(folder_name):

    if not is_valid_api_key():
        return jsonify({"error": "Unauthorized - Invalid API Key"}), 401

    target_folder = os.path.join(UPLOAD_FOLDER, folder_name)

    if not os.path.exists(target_folder) or not os.path.isdir(target_folder):
        return jsonify({"error": "Folder not found"}), 404

    files = os.listdir(target_folder)
    all_files_data = []

    for filename in files:
        file_path = os.path.join(target_folder, filename)

        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                content = f"Error reading file: {str(e)}"

            all_files_data.append({
                "filename": filename,
                "stored_path": file_path,
                "content": content
            })

    if not all_files_data:
        return jsonify({"error": "No files found in folder"}), 404

    return jsonify({
        "location": folder_name,
        "total_files": len(all_files_data),
        "files": all_files_data
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)





