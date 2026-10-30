import json
import time

from openai import InternalServerError, RateLimitError

from hulp import lees
from structured_output import MODEL, llm

# Opdracht 1: een ticket kan over meer dan één probleem gaan.
# Schrijf hier een PROMPT en een SCHEMA, zoals in
# structured_output.py, met een veld categorieen: een lijst
# van categorieën, in de volgorde waarin ze in het ticket staan.


def lees_meerdere(tekst):
    # Opdracht 2: vraag het aan de LLM met jouw PROMPT en SCHEMA,
    # zoals lees_met_schema in structured_output.py.
    return {"categorieen": ["facturatie"]}


def evalueer_meerdere(functie):
    # Opdracht 3: tel hoe vaak de lijst van categorieën juist is.
    # Telt de volgorde mee? Tel het op meer dan één manier.
    tickets = lees("tickets_meerdere.csv")
    for ticket in tickets:
        antwoord = functie(ticket["tekst"])
        label = ticket["categorieen"].split("|")
        print(antwoord["categorieen"], label)


if __name__ == "__main__":
    evalueer_meerdere(lees_meerdere)
