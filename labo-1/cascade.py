from hulp import evalueer
from lokaal import model
from taalmodel import voorspel_met_taalmodel

DREMPEL = 0.8


def lokaal_met_confidence(tekst):
    # Opdracht: vraag het sentimentmodel om alle vijf de kansen.
    # Geef het antwoord van lokaal.py terug, en hoe zeker het daarvan is.
    return "positief", 1.0


def voorspel_met_cascade(tekst):
    # Opdracht: vraag het eerst aan het sentimentmodel.
    # Is de confidence lager dan DREMPEL? Vraag het dan aan de LLM.
    return "positief"


evalueer(voorspel_met_cascade, "moeilijke_berichten.csv")
