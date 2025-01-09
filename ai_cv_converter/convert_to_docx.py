from htmldocx import HtmlToDocx
import functions_framework
from flask import request, jsonify
from dotenv import load_dotenv
from flask import send_file
import io
from google.cloud import storage
import time

load_dotenv()


# Upload the DOCX content to Google Cloud Storage

# Initialize a client
storage_client = storage.Client()

# Define the bucket name and the destination blob name
bucket_name = "public-yuri-sa"
destination_blob_name = str(time.time()) + "-converted_cv.docx"

# Get the bucket
bucket = storage_client.bucket(bucket_name)


@functions_framework.http
def convert_html_to_docx(request):
    if request.method != "POST":
        return jsonify({"error": "Only POST method is allowed"}), 405

    html_content = request.json.get("html_content")

    converter = HtmlToDocx()
    docx_content = converter.parse_html_string(html_content)

    # Save the DOCX content to a BytesIO object
    docx_io = io.BytesIO()
    docx_content.save(docx_io)
    docx_io.seek(0)

    # Create a new blob and upload the file's content
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(docx_io, content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    # Make the blob publicly accessible
    blob.make_public()

    # Get the public URL
    public_url = blob.public_url

    #DEBUG Save the DOCX content to a file
    with open("output_from_api.docx", "wb") as f:
        f.write(docx_io.getvalue())

    return jsonify({"filename": public_url})
