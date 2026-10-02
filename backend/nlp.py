import spacy


MODEL_NAME = "en_core_web_sm"

try:
    nlp = spacy.load(MODEL_NAME)
except OSError:
    nlp = None


def extract_entities(text: str):
    if nlp is None:
        return {
            "error": (
                "spaCy model is not installed. "
                "Run: python -m spacy download en_core_web_sm"
            )
        }

    document = nlp(text)

    entities = []

    for entity in document.ents:
        entities.append({
            "text": entity.text,
            "label": entity.label_,
            "start": entity.start_char,
            "end": entity.end_char
        })

    return {
        "entities": entities
    }
