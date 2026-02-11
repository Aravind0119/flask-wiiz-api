# from flask import Flask, request, jsonify
# import os

# app = Flask(__name__)

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route("/process", methods=["POST"])
# def process_multipart():
#     # ---- Validate file ----
#     if "file" not in request.files:
#         return jsonify({"error": "Missing 'file' in multipart request"}), 400

#     file = request.files["file"]

#     if file.filename == "":
#         return jsonify({"error": "Empty filename received"}), 400

#     # ---- Extract other form fields ----
#     user_id = request.form.get("user_id")
#     document_type = request.form.get("document_type")

#     # ---- Read file content (optional) ----
#     file_bytes = file.read()
#     file_size = len(file_bytes)

#     # Reset pointer and save file
#     file.seek(0)
#     save_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(save_path)

#     # ---- Build response ----
#     response = {
#         "status": "success",
#         "message": "Multipart data received and processed",
#         "extracted_data": {
#             "filename": file.filename,
#             "file_size_bytes": file_size,
#             "content_type": file.content_type,
#             "user_id": user_id,
#             "document_type": document_type,
#             "saved_path": save_path
#         }
#     }

#     return jsonify(response), 200


# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route("/process", methods=["POST"])
# def read_file():
#     # Check if file is present
#     if "file" not in request.files:
#         return jsonify({"error": "Missing 'file' in request"}), 400

#     file = request.files["file"]

#     if file.filename == "":
#         return jsonify({"error": "Empty filename"}), 400

#     try:
#         # Try to read as text (UTF-8)
#         content = file.read().decode("utf-8")
#     except Exception as e:
#         return jsonify({"error": f"Unable to read file as text: {str(e)}"}), 400

#     return jsonify({
#         "filename": file.filename,
#         "content": content
#     }), 200


# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # ---- YOUR API KEY (store this safely) ----
# VALID_API_KEY = "my-secure-api-key-12345"

# def require_api_key():
#     api_key = request.headers.get("x-api-key")
#     if not api_key or api_key != VALID_API_KEY:
#         return False
#     return True

# @app.route("/read-file", methods=["POST"])
# def read_file():
#     # ---- Check API Key first ----
#     if not require_api_key():
#         return jsonify({"error": "Unauthorized - Invalid API Key"}), 401

#     if "file" not in request.files:
#         return jsonify({"error": "Missing file"}), 400

#     file = request.files["file"]

#     try:
#         content = file.read().decode("utf-8")
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

#     return jsonify({
#         "filename": file.filename,
#         "content": content
#     }), 200

# if __name__ == "__main__":
#     app.run(debug=True)



import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

VALID_API_KEY = os.getenv("API_KEY")

# POINT THIS TO YOUR ACTUAL FOLDER
UPLOAD_FOLDER = r"C:\Users\FA2703TX\Desktop\flask-wiiz-api\uploads"
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


# -------- READ ALL FILES --------
@app.route("/read-all-files", methods=["GET"])
def read_all_files():

    if not is_valid_api_key():
        return jsonify({"error": "Unauthorized - Invalid API Key"}), 401

    files = os.listdir(UPLOAD_FOLDER)

    if not files:
        return jsonify({"error": "No files found in uploads folder"}), 404

    all_files_data = []

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
        "total_files": len(files),
        "files": all_files_data
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


