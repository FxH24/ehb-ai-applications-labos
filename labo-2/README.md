# Labo 2: helpdesktickets lezen met een LLM

Hoe je de bestanden ophaalt en de scripts start. De opdrachten krijg je in de les. uv, je sleutel in `.env` en Ollama installeerde je in labo 1.

---

## Je werk bewaren en labo 2 ophalen

In de map van je repo. Bewaar eerst je werk:

```bash
git add .
git status
```

Staat `.env` **niet** in de lijst? Dan:

```bash
git commit -m "Labo 1"
git push
```

Open je fork op GitHub, klik **Sync fork** → **Update branch**, en dan:

```bash
git pull
uv sync
```

Ga in de terminal naar de map van dit labo. Zit je nog in `labo-1`, typ dan eerst `cd ..`

```bash
cd labo-2
```

---

## Ollama

Je hebt `gemma3:270m` en `gemma4:e2b` al uit labo 1. Start de Ollama-app voor je `lokaal_taalmodel.py` of `controleer.py` start.

Op een Mac gebruik je voor Gemma 4 deze versie:

```bash
ollama pull gemma4:e2b-it-q4_K_M
```

---

## De scripts starten

In de map van dit labo:

```bash
uv run regels.py
uv run prompt_json.py
uv run structured_output.py
uv run pydantic_ticket.py
uv run pydantic_enum.py
uv run lokaal_taalmodel.py
uv run controleer.py
uv run meerdere.py
```

---

## De API en de webpagina

```bash
uv run fastapi dev api.py
```

Open <http://127.0.0.1:8000> (de webpagina) of <http://127.0.0.1:8000/docs>. Sla je een bestand op, dan herstart de server vanzelf. Stoppen met `Ctrl+C`.

---

## Lukt het niet?

| Wat je ziet | Wat je doet |
|---|---|
| "uv wordt niet herkend" of "command not found" | sluit alle terminals (ook die in VS Code) en open een nieuwe |
| rode kronkellijnen onder een `import` in VS Code | `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`), **Python: Select Interpreter**, kies die met `.venv` erin |
| `AuthenticationError` of `401` | je sleutel ontbreekt in `.env` of klopt niet |
| `Missing credentials` | er is geen `.env`, of hij staat niet in de hoofdmap van de repo (ook de scripts met Ollama lezen hem) |
| "Google antwoordt niet: 20 seconden wachten" | de rate limit: het script wacht en probeert opnieuw. Blijft het duren, dan zit je aan de limiet per dag |
| `Connection refused` of `could not connect` bij Ollama | start de Ollama-app, of `ollama serve` in een aparte terminal |
| `501` en "structured output is unavailable" bij Ollama op een Mac | gebruik `gemma4:e2b-it-q4_K_M` in plaats van `gemma4:e2b` |
| "Address already in use" | `uv run fastapi dev api.py --port 8001` |
| "nog geen endpoint" op de webpagina | dat endpoint staat nog niet in `api.py`, of staat onder de laatste regel (`app.mount`) |
| de tabel is te breed voor je terminal | maak het venster breder, of sleep het terminalpaneel in VS Code naar boven |

---

## Bewaren

```bash
git add .
git status
git commit -m "Labo 2"
git push
```

Kijk bij `git status` of `.env` **niet** in de lijst staat.
