# Labo 1: klantberichten indelen als positief of negatief

Hoe je alles installeert en start. De opdrachten krijg je in de les.

---

## uv installeren

**Windows** (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux**:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Sluit daarna je terminal en open een nieuwe. Dan:

```bash
uv --version
```

**Je ziet nu** iets als `uv 0.11.19`.

---

## De repo ophalen

Ga naar <https://github.com/orchardsol/ehb-ai-applications-labos> en klik rechtsboven op **Fork**. Haal je fork naar je laptop (vervang `<jouw-gebruikersnaam>` door je GitHub-naam):

```bash
git clone https://github.com/<jouw-gebruikersnaam>/ehb-ai-applications-labos.git
cd ehb-ai-applications-labos
uv sync
```

De eerste keer duurt `uv sync` even: er zit onder andere PyTorch bij (± 500 MB).

Kopieer `.env.example` naar `.env` (Windows: `copy .env.example .env`). `.env` staat in `.gitignore`: een sleutel hoort nooit in git.

Open de repo in VS Code en ga in de terminal van VS Code (*Terminal → New Terminal*) naar de map van dit labo:

```bash
code .
```

```bash
cd labo-1
```

---

## Een sleutel bij Google AI Studio

1. Ga naar <https://aistudio.google.com> en meld je aan met je Google-account.
2. Klik op *Get API key* en dan *Create API key*. Kopieer de sleutel.
3. Zet hem in `.env`:

```text
OPENAI_API_KEY=AQ....
```

---

## Ollama

Windows (PowerShell):

```powershell
irm https://ollama.com/install.ps1 | iex
```

macOS / Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Of download `OllamaSetup.exe` (Windows) of `Ollama.dmg` (macOS) van <https://ollama.com/download>. Sluit daarna je terminal, open een nieuwe en controleer met `ollama --version`.

Haal de modellen op:

```bash
ollama pull gemma3:270m
ollama pull gemma4:e2b
```

`gemma4:e2b` is 4,6 GB: haal het thuis, niet op de campus. Het neemt ± 5 GB werkgeheugen terwijl het draait.

---

## De scripts starten

In de map van dit labo:

```bash
uv run regels.py
uv run lokaal.py
uv run taalmodel.py
uv run lokaal_taalmodel.py
uv run cascade.py
```

De eerste keer downloadt `lokaal.py` het sentimentmodel (669 MB): doe dat thuis.

Een REPL starten: `uv run python`. Met `uv run python -i lokaal.py` voert Python eerst `lokaal.py` uit en blijft de REPL daarna open. Verlaten met `exit()`.

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
| "Google antwoordt niet: 20 seconden wachten" | de rate limit: het script wacht en probeert opnieuw. Blijft het duren, dan zit je aan de limiet per dag |
| `Connection refused` of `could not connect` bij Ollama | start de Ollama-app, of `ollama serve` in een aparte terminal |
| "Address already in use" | `uv run fastapi dev api.py --port 8001` |

---

## Bewaren en nieuwe bestanden ophalen

Bewaren, in de map van je repo:

```bash
git add .
git status
```

Staat `.env` **niet** in de lijst? Dan:

```bash
git commit -m "Labo 1"
git push
```

Nieuwe bestanden ophalen: open je fork op GitHub, klik **Sync fork** → **Update branch**, en dan:

```bash
git pull
uv sync
```
