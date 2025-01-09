from htmldocx import HtmlToDocx
import functions_framework
from flask import request, jsonify
from dotenv import load_dotenv
from flask import send_file
import io

load_dotenv()

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

    # Return the DOCX file as a response
    return send_file(docx_io, as_attachment=True, download_name="output.docx", mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
