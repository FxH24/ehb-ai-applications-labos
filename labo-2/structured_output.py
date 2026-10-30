import json
import time

from openai import InternalServerError, OpenAI, RateLimitError

from hulp import evalueer

GOOGLE = "https://generativelanguage.googleapis.com/v1beta/openai/"
llm = OpenAI(base_url=GOOGLE, max_retries=0)
MODEL = "gemini-3.5-flash-lite"

PROMPT = """Lees dit helpdeskticket.
Geef JSON met deze velden:
- categorie: facturatie, levering, defect, account of verhuur
- taal: nl of fr
- klantnummer: zoals K12345, of null
- factuurnummer: zoals F2026-1234, of null

Ticket: """

# Opdracht: beschrijf hier het antwoord als JSON Schema: een object
# met categorie, taal, klantnummer en factuurnummer.
SCHEMA = {
    "type": "object",
}


def lees_met_schema(tekst):
    try:
        antwoord = llm.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT + tekst}],
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "ticket", "schema": SCHEMA},
            },
        )
    except (RateLimitError, InternalServerError):
        print("  Google antwoordt niet: 20 seconden wachten")
        time.sleep(20)
        return lees_met_schema(tekst)
    return json.loads(antwoord.choices[0].message.content)


evalueer(lees_met_schema)
