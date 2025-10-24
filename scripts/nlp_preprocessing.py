import spacy

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

if __name__ == "__main__":
    sample = "This is a sample log entry with some errors like NullPointerException."
    print(preprocess_text(sample))
