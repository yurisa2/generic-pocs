gcloud functions deploy ai_cv_converter_be \
--gen2 \
--region=us-central1 \
--runtime=python312 \
--source=. \
--entry-point=get_file_and_add_prompt \
--trigger-http \
--allow-unauthenticated \
--memory 1024MB

gcloud functions deploy convert_html_to_docx \
--gen2 \
--region=us-central1 \
--runtime=python312 \
--source=. \
--entry-point=convert_html_to_docx \
--trigger-http \
--allow-unauthenticated \
--memory 1024MB
