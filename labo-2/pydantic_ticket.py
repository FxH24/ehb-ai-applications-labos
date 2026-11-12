import time
from typing import Literal

from openai import InternalServerError, RateLimitError
from pydantic import BaseModel

from hulp import evalueer
from structured_output import MODEL, PROMPT, llm


# Opdracht: beschrijf hier het antwoord als Pydantic-klasse,
# met categorie, taal, klantnummer en factuurnummer.
# dit is een kortere notatie hierbij ga je dus geen JSON schema schrijven maar krijg je wel hetzelfde als een JSON schema
class Ticket(BaseModel):
    
    categorie: Literal ["facturatie", "levering", "defect", "account", "verhuur"]
    taal: Literal ["nl","fr"]
    klantnummer: str | None
    factuurnummer:str | None



def lees_met_pydantic(tekst):
    try:
        antwoord = llm.chat.completions.parse(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT + tekst}],
            response_format=Ticket, #gebruikt de pydantic ipv json schema
        )
    except (RateLimitError, InternalServerError):
        print("  Google antwoordt niet: 20 seconden wachten")
        time.sleep(20)
        return lees_met_pydantic(tekst)
    ticket = antwoord.choices[0].message.parsed
    return ticket.model_dump()


evalueer(lees_met_pydantic)
