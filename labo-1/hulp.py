"""Hulp bij labo 1. Je hoeft dit bestand niet te wijzigen.

- leest je sleutels uit het bestand .env in de hoofdmap van de repo
- BERICHTEN: de 12 gelabelde klantberichten uit berichten.csv
- evalueer(functie): test jouw functie op gelabelde berichten en telt hoe vaak
  haar antwoord gelijk is aan het label
- geeft je functie een dictionary terug (zoals de cascade), dan is "sentiment" het
  antwoord en komt de rest als extra kolommen in de tabel
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
    """Leest gelabelde berichten uit een csv-bestand: een lijst van (tekst, label)."""
    berichten = []
    with open(MAP / bestand, encoding="utf-8-sig", newline="") as csv_bestand:
        lezer = csv.DictReader(csv_bestand)
        for rij in lezer:
            label = (rij.get("label") or "").strip().lower()
            if label not in ("positief", "negatief") or None in rij:
                raise SystemExit(
                    f"{bestand}, regel {lezer.line_num}: het label moet positief of negatief zijn.\n"
                    'Elke regel is: "het bericht",label. Staat er een komma in het bericht? '
                    "Zet het bericht dan tussen dubbele aanhalingstekens."
                )
            berichten.append((rij["tekst"], label))
    return berichten


BERICHTEN = lees("berichten.csv")


def evalueer(functie, bestand="berichten.csv"):
    """Test functie(tekst) op de gelabelde berichten in het bestand.

    Toont per bericht het antwoord naast het label, dan de score, en wat het je eigen laptop
    kostte: CPU-tijd en geheugen.
    """
    if functie.__module__ != "__main__":
        return  # een ander bestand (zoals api.py) gebruikt jouw functie: dan evalueren we niet opnieuw

    import psutil

    berichten = lees(bestand)
    if not berichten:
        raise SystemExit(f"{bestand} is nog leeg: zet er eerst berichten in, één per regel.")
    rijen = []
    kolommen = []  # extra kolommen, als de functie een dictionary teruggeeft
    start = time.perf_counter()
    start_cpu = time.process_time()
    juist = 0
    for tekst, label in berichten:
        antwoord = functie(tekst)
        extra = {}
        if isinstance(antwoord, dict):
            extra = {naam: waarde for naam, waarde in antwoord.items() if naam != "sentiment"}
            antwoord = antwoord.get("sentiment")
        antwoord = str(antwoord).strip(" .!*\n").lower()
        kolommen = kolommen + [naam for naam in extra if naam not in kolommen]
        if antwoord == label:
            juist = juist + 1
            rijen.append((tekst, Text(f"{antwoord} ✓", style="green"), label, extra))
        else:
            rijen.append((tekst, Text(f"{antwoord} ✗", style="red"), label, extra))
    seconden = (time.perf_counter() - start) / len(berichten)
    cpu_tijd = (time.process_time() - start_cpu) / len(berichten)
    geheugen = psutil.Process().memory_info().rss / 1_000_000

    tabel = Table(title=f"{functie.__name__} op {bestand}", title_justify="left")
    for kolom in ["bericht", "antwoord", "label"] + kolommen:
        tabel.add_column(kolom)
    for tekst, antwoord, label, extra in rijen:
        waarden = [extra.get(kolom, "") for kolom in kolommen]
        tabel.add_row(tekst, antwoord, label, *[f"{w:.2f}" if isinstance(w, float) else str(w) for w in waarden])
    console.print(tabel)
    console.print(f"[bold]{juist}/{len(berichten)} juist[/] · {seconden:.3f} seconden per bericht")
    if "door" in kolommen:
        wie = [extra.get("door") for tekst, antwoord, label, extra in rijen]
        telling = " · ".join(f"{wie.count(naam)} {naam}" for naam in sorted(set(wie), reverse=True))
        console.print(f"beantwoord door: {telling}")
    console.print(f"op je eigen laptop: {cpu_tijd:.3f} seconden CPU-tijd per bericht, {geheugen:.0f} MB geheugen")
