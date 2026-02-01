import re
import unicodedata

def preprocess_text(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))

    text = text.lower()

    text = re.sub(r"[^\w\s.,!?]", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()
