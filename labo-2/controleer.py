from hulp import evalueer
from lokaal_taalmodel import lees_met_lokaal_taalmodel

NUMMERS = ["klantnummer", "factuurnummer"]


def controleer(antwoord, tekst):
    # Opdracht: staat een nummer uit het antwoord niet in de
    # tekst van het ticket? Maak het dan None.
    return antwoord


def lees_met_controle(tekst):
    # Opdracht: vraag het aan het lokale taalmodel,
    # en controleer dan het antwoord.
    return lees_met_lokaal_taalmodel(tekst)


evalueer(lees_met_controle)
