def clean_text(text: str) -> str:
    if not text:
        return text

    text = text.replace('\t', ' ').replace('\n', ' ')
    return ' '.join(text.split())
