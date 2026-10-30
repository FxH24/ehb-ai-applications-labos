import re

from hulp import evalueer

WOORDEN = {
    "facturatie": ["factuur", "betaling", "facture"],
    "levering": ["levering", "pakket", "livraison"],
    "defect": ["kapot", "defect", "panne"],
    "account": ["account", "wachtwoord", "compte"],
    "verhuur": ["huren", "huur", "location"],
}


def zoek(patroon, tekst):
    gevonden = re.search(patroon, tekst)
    if gevonden:
        return gevonden.group()
    return None


def lees_met_regels(tekst):
    categorie = None
    for naam in WOORDEN:
        for woord in WOORDEN[naam]:
            if woord in tekst.lower():
                categorie = naam
    taal = "nl"
    if zoek(r"\b(je|mon|ma|le|la|est)\b", tekst.lower()):
        taal = "fr"
    return {
        "categorie": categorie,
        "taal": taal,
        "klantnummer": zoek(r"K\d{5}", tekst),
        "factuurnummer": zoek(r"F\d{4}-\d{4}", tekst),
    }


evalueer(lees_met_regels)
