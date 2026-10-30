import json

from openai import OpenAI

from hulp import evalueer
from structured_output import PROMPT, SCHEMA

OLLAMA = "http://localhost:11434/v1"
llm = OpenAI(base_url=OLLAMA, api_key="ollama")
MODEL = "gemma3:270m"


def lees_met_lokaal_taalmodel(tekst):
    antwoord = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT + tekst}],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "ticket", "schema": SCHEMA},
        },
    )
    return json.loads(antwoord.choices[0].message.content)


evalueer(lees_met_lokaal_taalmodel)
