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
from htmldocx import HtmlToDocx


load_dotenv()

# Initialize a client
storage_client = storage.Client()

# Define the bucket name and the destination blob name
bucket_name = "public-yuri-sa"
destination_blob_name = str(time.time()) + "-converted_cv.docx"


PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
vertexai.init(project=PROJECT_ID, location=REGION)

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)

# Load the template
template = env.get_template("resume-template-3.0.html")


with open("json_spec.json", "r") as file:
    json_spec = file.read()

with open("main_prompt.txt", "r") as file:
    main_prompt = file.read()

@functions_framework.http
def get_file_and_add_prompt(request):
    """
    ---
    post:
      summary: Process a PDF file and generate HTML output
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file_receive:
                  type: string
                  format: binary
                  description: The PDF file to be processed
      responses:
        '200':
          description: Successfully processed the PDF and generated HTML output
          content:
            text/html:
              schema:
                type: string
        '400':
          description: Bad request, either no file provided or unsupported file type
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
        '405':
          description: Method not allowed, only POST method is allowed
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
        '500':
          description: Internal server error while processing the PDF
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
    """
    if request.method != "POST":
        return jsonify({"error": "Only POST method is allowed"}), 405

    if "file_receive" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file_receive"]
    filename = file.filename
    file_extension = filename.split(".")[-1].lower()

    if file_extension == "pdf":
        try:
            # Read the PDF file content into memory
            pdf_content = file.read()

            # Create a Part object for the PDF data
            pdf_part = Part.from_data(
                pdf_content, mime_type="application/pdf"
            )

            generative_multimodal_model = GenerativeModel(
                "gemini-1.5-flash-002",
                system_instruction="You are a HR manager reviewing a resume for a job opening in your company, and you need to assist on the conversion of the resume to a specific format so other can understand better."                
            )  
            prompt = f"""
                {main_prompt}
                
                get the response in JSON format as it follows on the spec below, but remove all definitions:

                {json_spec}
                
                """  # More specific prompt

            responses = generative_multimodal_model.generate_content(
                [prompt, pdf_part],
                generation_config={
                    "max_output_tokens": 8192  # Increase max output tokens for potentially long PDFs
                },
            )

            # print(responses)

            text = responses.candidates[0].content.text  # Extract the text from the response

            text = text.replace("```json", "").replace("```", "").replace("\n", "").replace("\r", "").replace("\t", "")

            with open("llm_response.json", "w") as response_file:
                response_file.write(text)

            # Render the template with the JSON data
            output = template.render(json.loads(text))

            with open("generated_output.html", "w") as response_file:
                response_file.write(output)

            return {"html_output": output, "json_output": text}, 200

        except Exception as e:
            print(f"Error processing PDF: {e}")  # Print the error for debugging
            return (
                jsonify({"error": f"Error processing PDF: {e}"}),
                500,
            )  # Return error to client

    else:
        return jsonify({"error": "Unsupported file type"}), 400


@functions_framework.http
def convert_html_to_docx(request):
    bucket = storage_client.bucket(bucket_name)

    if request.method != "POST":
        return jsonify({"error": "Only POST method is allowed"}), 405

    html_content = request.json.get("html_content")

    

    converter = HtmlToDocx()
    if html_content is None:
        return jsonify({"error": "No HTML content provided"}), 400

    docx_content = converter.parse_html_string(html_content)

    # Save the DOCX content to a BytesIO object
    docx_io = io.BytesIO()
    docx_content.save(docx_io)
    docx_io.seek(0)

    # Create a new blob and upload the file's content
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(
        docx_io,
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    # Make the blob publicly accessible
    blob.make_public()

    # Get the public URL
    public_url = blob.public_url

    # DEBUG Save the DOCX content to a file
    with open("output_from_api.docx", "wb") as f:
        f.write(docx_io.getvalue())

    return jsonify({"filename": public_url})
