from huggingface_hub import InferenceClient

from hulp import evalueer

hf = InferenceClient()
MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"


def voorspel_met_model(tekst):
    resultaat = hf.text_classification(tekst, model=MODEL)
    if resultaat[0].label in ["4 stars", "5 stars"]:
        return "positief"
    return "negatief"


evalueer(voorspel_met_model)
