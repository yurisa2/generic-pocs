import functions_framework
from flask import request, jsonify
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os
from dotenv import load_dotenv
import json
from jinja2 import Environment, FileSystemLoader

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
vertexai.init(project=PROJECT_ID, location=REGION)

file_loader = FileSystemLoader("ai_cv_converter/templates")
env = Environment(loader=file_loader)

# Load the template
template = env.get_template("resume-template-3.0.html")


with open("ai_cv_converter/json_spec.json", "r") as file:
    json_spec = file.read()

with open("ai_cv_converter/main_prompt.txt", "r") as file:
    main_prompt = file.read()

@functions_framework.http
def get_file_and_add_prompt(request):
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
                "gemini-1.5-flash-002"
            )  # Use gemini-pro for multimodal
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

            return output, 200

        except Exception as e:
            print(f"Error processing PDF: {e}")  # Print the error for debugging
            return (
                jsonify({"error": f"Error processing PDF: {e}"}),
                500,
            )  # Return error to client

    else:
        return jsonify({"error": "Unsupported file type"}), 400
