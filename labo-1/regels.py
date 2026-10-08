from hulp import evalueer


def voorspel_met_regel(tekst):
    if "kapot" in tekst:
        return "negatief"
    return "positief"


evalueer(voorspel_met_regel)
