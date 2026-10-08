from transformers import pipeline

from hulp import evalueer

MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"
model = pipeline("text-classification", model=MODEL)


def voorspel_met_lokaal_model(tekst):
    resultaat = model(tekst)
    if resultaat[0]["label"] in ["4 stars", "5 stars"]:
        return "positief"
    return "negatief"


evalueer(voorspel_met_lokaal_model)
