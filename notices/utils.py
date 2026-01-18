from PyPDF2 import PdfReader
from openai import OpenAI
from django.conf import settings


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def ai_summarize_notice(description="", pdf_file=None):
    text = ""

    if pdf_file:
        text = extract_text_from_pdf(pdf_file)

    if not text:
        text = description

    if not text:
        return "• No content available to summarize."

    # ✅ Create client INSIDE function
    client = get_openai_client()#OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "Summarize the following college notice into 4–5 short, clear bullet points "
                    "for students."
                )
            },
            {
                "role": "user",
                "content": text[:8000]
            }
        ],
        max_tokens=200
    )

    return response.choices[0].message.content
 