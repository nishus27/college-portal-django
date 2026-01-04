def ai_summarize(text):
    """
    Basic summarization logic.
    Replace this later with Gemini/OpenAI.
    """
    sentences = text.split('.')
    summary = '.'.join(sentences[:3])
    return summary.strip() + '.'
