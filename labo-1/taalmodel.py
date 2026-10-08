import time

from openai import InternalServerError, OpenAI, RateLimitError

from hulp import evalueer

GOOGLE = "https://generativelanguage.googleapis.com/v1beta/openai/"
llm = OpenAI(base_url=GOOGLE, max_retries=0)
#MODEL = "gemini-3.5-flash-lite"
MODEL="gemma-4-26b-a4b-it"


def voorspel_met_taalmodel(tekst):
    prompt = "Is dit bericht positief of negatief? "
    prompt = prompt + "Antwoord met één woord.\n\n" + tekst
    try:
        antwoord = llm.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
    except (RateLimitError, InternalServerError):
        print("  Google antwoordt niet: 20 seconden wachten")
        time.sleep(20)
        return voorspel_met_taalmodel(tekst)
    woord = antwoord.choices[0].message.content
    return woord.lower().strip(" .")


evalueer(voorspel_met_taalmodel)
