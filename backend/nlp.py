import nltk
import string

from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

nltk.download('stopwords')
nltk.download('rslp')

stop_words = set(stopwords.words('portuguese'))
stemmer = RSLPStemmer()

def preprocess_text(text: str) -> str:
    text = text.lower()

    text = text.translate(str.maketrans('', '', string.punctuation))

    words = text.split()

    processed_words = [
        stemmer.stem(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(processed_words)
