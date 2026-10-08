from openai import OpenAI

from hulp import evalueer

OLLAMA = "http://localhost:11434/v1"
llm = OpenAI(base_url=OLLAMA, api_key="ollama")
MODEL = "gemma3:270m"


def voorspel_met_lokaal_taalmodel(tekst):
    prompt = "Is dit bericht positief of negatief? "
    prompt = prompt + "Antwoord met één woord.\n\n" + tekst
    antwoord = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    woord = antwoord.choices[0].message.content
    return woord.lower().strip(" .")


evalueer(voorspel_met_lokaal_taalmodel)
