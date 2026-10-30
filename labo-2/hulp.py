"""Hulp bij labo 2. Je hoeft dit bestand niet te wijzigen.

- leest je sleutel uit het bestand .env in de hoofdmap van de repo
- evalueer(functie): test jouw functie op de gelabelde tickets in tickets.csv.
  Je functie krijgt de tekst van een ticket en geeft een dictionary terug, zoals
  {"categorie": "levering", "taal": "nl", "klantnummer": None, ...}.
  evalueer telt drie dingen: hoeveel antwoorden bruikbaar zijn (een dictionary), per veld
  hoe vaak de vorm klopt (het veld is er, en de waarde is een string of None, en bij
  categorie en taal een van de waarden uit de labels), en per veld hoe vaak de waarde
  gelijk is aan het label.
- loopt je functie vast op een ticket, of geeft ze geen dictionary terug, dan is dat
  antwoord niet bruikbaar: evalueer toont de fout en gaat door met het volgende ticket
"""

import csv
import time
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.text import Text

MAP = Path(__file__).parent
load_dotenv(MAP.parent / ".env")

console = Console()


def lees(bestand):
    """Leest gelabelde tickets uit een csv-bestand: een lijst van dictionaries."""
    with open(MAP / bestand, encoding="utf-8-sig", newline="") as csv_bestand:
        lezer = csv.DictReader(csv_bestand)
        tickets = list(lezer)
    for nummer, ticket in enumerate(tickets, start=2):
        if None in ticket or not ticket.get("tekst"):
            raise SystemExit(
                f"{bestand}, regel {nummer}: elke regel is de tekst van het ticket en dan de labels, "
                "gescheiden door komma's. Staat er een komma in de tekst? Zet de tekst dan tussen "
                "dubbele aanhalingstekens."
            )
    return tickets


def als_tekst(waarde):
    """Een antwoord als tekst, zoals het in de tabel komt: None wordt een lege tekst."""
    if waarde is None:
        return ""
    return str(waarde).strip()


def gelijk(antwoord, label):
    """Hoofdletters en spaties aan het begin of einde tellen niet mee."""
    return als_tekst(antwoord).lower() == als_tekst(label).lower()


def evalueer(functie, bestand="tickets.csv"):
    """Test functie(tekst) op de gelabelde tickets in het bestand.

    Toont per ticket elk veld naast het label, dan hoeveel antwoorden bruikbaar waren, per veld
    hoe vaak de vorm klopte en hoe vaak de waarde juist was, en wat het je eigen laptop kostte:
    CPU-tijd en geheugen.
    """
    if functie.__module__ != "__main__":
        return  # een ander bestand (zoals controleer.py) gebruikt jouw functie: dan evalueren we niet opnieuw

    import psutil

    tickets = lees(bestand)
    labels = [naam for naam in tickets[0] if naam != "tekst"]
    antwoorden = []
    start = time.perf_counter()
    start_cpu = time.process_time()
    for ticket in tickets:
        try:
            antwoord = functie(ticket["tekst"])
        except Exception as fout:
            antwoord = fout
        antwoorden.append(antwoord)
    seconden = (time.perf_counter() - start) / len(tickets)
    cpu_tijd = (time.process_time() - start_cpu) / len(tickets)
    geheugen = psutil.Process().memory_info().rss / 1_000_000

    # de kolommen: elk label dat je functie minstens één keer invult, dan velden zonder label
    velden = []
    for antwoord in antwoorden:
        if isinstance(antwoord, dict):
            velden = velden + [naam for naam in antwoord if naam not in velden]
    gescoord = [naam for naam in labels if naam in velden]
    extra = [naam for naam in velden if naam not in labels]

    tabel = Table(title=f"{functie.__name__} op {bestand}", title_justify="left", show_lines=True)
    tabel.add_column("ticket", max_width=44)
    for naam in gescoord + extra:
        tabel.add_column(naam)
    if not velden:
        tabel.add_column("antwoord")
    # de vorm: een string of None; bij categorie en taal ook een van de waarden die in de labels staan
    toegelaten = {}
    for naam in ["categorie", "taal"]:
        if naam in gescoord:
            toegelaten[naam] = {als_tekst(t[naam]).lower() for t in tickets} - {""}
    vorm = {naam: 0 for naam in gescoord}
    juist = {naam: 0 for naam in gescoord}
    bruikbaar = 0
    for ticket, antwoord in zip(tickets, antwoorden):
        if isinstance(antwoord, Exception):
            fout = f"{type(antwoord).__name__}: {antwoord}"[:60]
            tabel.add_row(ticket["tekst"], Text(f"niet bruikbaar ✗ {fout}", style="red"))
            continue
        if not isinstance(antwoord, dict):
            soort = type(antwoord).__name__
            tabel.add_row(ticket["tekst"], Text(f"niet bruikbaar ✗ geen dictionary maar {soort}", style="red"))
            continue
        bruikbaar = bruikbaar + 1
        cellen = []
        for naam in gescoord:
            waarde = antwoord.get(naam)
            geldig = waarde is None or isinstance(waarde, str)
            if geldig and isinstance(waarde, str) and naam in toegelaten:
                geldig = als_tekst(waarde).lower() in toegelaten[naam]
            if naam not in antwoord:
                cellen.append(Text(f"ontbreekt ✗ ({ticket[naam] or 'leeg'})", style="red"))
            elif not geldig:
                cellen.append(Text(f"{als_tekst(waarde)[:20]} ✗ vorm ({ticket[naam] or 'leeg'})", style="red"))
            elif gelijk(antwoord[naam], ticket[naam]):
                vorm[naam] = vorm[naam] + 1
                juist[naam] = juist[naam] + 1
                cellen.append(Text(f"{als_tekst(antwoord[naam]) or '—'} ✓", style="green"))
            else:
                vorm[naam] = vorm[naam] + 1
                cellen.append(Text(f"{als_tekst(antwoord[naam]) or '—'} ✗ ({ticket[naam] or 'leeg'})", style="red"))
        for naam in extra:
            cellen.append(als_tekst(antwoord.get(naam)))
        tabel.add_row(ticket["tekst"], *cellen)
    console.print(tabel)

    n = len(tickets)
    console.print(f"[bold]{bruikbaar}/{n} bruikbaar[/]")
    if gescoord:
        console.print("vorm   " + " · ".join(f"{naam} {vorm[naam]}/{n}" for naam in gescoord))
        console.print("juist  " + " · ".join(f"{naam} {juist[naam]}/{n}" for naam in gescoord))
    console.print(f"{seconden:.2f} seconden per ticket")
    console.print(f"op je eigen laptop: {cpu_tijd:.3f} seconden CPU-tijd per ticket, {geheugen:.0f} MB geheugen")
