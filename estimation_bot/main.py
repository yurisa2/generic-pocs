import functions_framework
from flask import request, jsonify
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os
from dotenv import load_dotenv
import json
from jinja2 import Environment, FileSystemLoader
import io
from google.cloud import storage
import time
import base64


load_dotenv()

# Initialize a client
storage_client = storage.Client()

# Define the bucket name and the destination blob name
bucket_name = "generic_files"

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
vertexai.init(project=PROJECT_ID, location=REGION)

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)

# Load the template
# template = env.get_template("resume-template-3.0.html")


# with open("json_spec.json", "r") as file:
#     json_spec = file.read()

# with open("main_prompt.txt", "r") as file:
#     main_prompt = file.read()

def decode_base64_file(file_data):
    base64_data = file_data.get("data")
    if not base64_data:
        raise ValueError("Missing 'data' key in file object")

    parts = base64_data.split(",", 1)
    if len(parts) != 2:
        raise ValueError("Invalid data URI format")

    base64_string = parts[1]
    return base64.b64decode(base64_string)

def upload_to_gcs(bucket, filename, data, content_type):
    blob = bucket.blob(filename)
    blob.upload_from_string(data, content_type=content_type)
    return f"gs://{bucket.name}/{filename}"

@functions_framework.http
def get_files_and_add_prompt(request):
    file_content = request.json.get("allfiles")
    if file_content is None:
        return jsonify({"error": "No files provided"}), 400

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    uploaded_files = []

    for file_data in file_content:
        try:
            decoded_data = decode_base64_file(file_data)

            filename = file_data.get("name")
            if not filename:
                return jsonify({"error": "Missing 'name' key in file object"}), 400

            gcs_uri = upload_to_gcs(bucket, filename, decoded_data, file_data.get("type"))
            uploaded_files.append({"filename": filename, "gcs_uri": gcs_uri})

        except (base64.binascii.Error, ValueError) as e:
            return jsonify({"error": f"Error decoding base64 data: {e}"}), 400
        except Exception as e:
            return jsonify({"error": f"Error uploading file: {e}"}), 500

    return (
        jsonify({"message": "Files uploaded successfully", "files": uploaded_files}),
        200,
    )
