# AI CV Converter

## Overview

The AI CV Converter is a powerful tool that leverages AI to convert CVs from PDF format to HTML and DOCX formats. It uses Google's Vertex AI for processing and Google Cloud Storage for storing the converted files.

## Features

- Convert PDF CVs to HTML format.
- Convert HTML content to DOCX format.
- Store converted DOCX files in Google Cloud Storage.
- Generate public URLs for easy access to converted files.

## Setup

### Prerequisites

- Python 3.12
- Google Cloud SDK
- Google Cloud Storage bucket
- Vertex AI setup

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/ai_cv_converter.git
    cd ai_cv_converter
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    Create a `.env` file in the root directory and add the following variables:
    ```env
    PROJECT_ID=your-gcp-project-id
    REGION=your-gcp-region
    ```

4. Deploy the Cloud Functions:
    ```bash
    ./deploy.sh
    ```

## Usage

### Endpoints

#### 1. Convert PDF to HTML

- **URL:** `/get_file_and_add_prompt`
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Request Body:**
    - `file_receive`: The PDF file to be processed.
- **Response:**
    - `200 OK`: Successfully processed the PDF and generated HTML output.
    - `400 Bad Request`: No file provided or unsupported file type.
    - `405 Method Not Allowed`: Only POST method is allowed.
    - `500 Internal Server Error`: Error while processing the PDF.

#### 2. Convert HTML to DOCX

- **URL:** `/convert_html_to_docx`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Request Body:**
    - `html_content`: The HTML content to be converted.
- **Response:**
    - `200 OK`: Successfully converted HTML to DOCX and uploaded to Google Cloud Storage.
    - `400 Bad Request`: No HTML content provided.
    - `405 Method Not Allowed`: Only POST method is allowed.
    - `500 Internal Server Error`: Error while processing the HTML content.

## OpenAPI Specification

The OpenAPI specification for the API is available in the `openapi.json` file.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Contact

For any inquiries, please contact [your-email@example.com](mailto:your-email@example.com).
