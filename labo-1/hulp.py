"""Hulp bij labo 1. Je hoeft dit bestand niet te wijzigen.

- leest je sleutels uit het bestand .env in de hoofdmap van de repo
- BERICHTEN: de 12 gelabelde klantberichten uit berichten.csv
- evalueer(functie): test jouw functie op gelabelde berichten en telt hoe vaak
  haar antwoord gelijk is aan het label
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
    with open(MAP / bestand, encoding="utf-8", newline="") as csv_bestand:
        return [(rij["tekst"], rij["label"]) for rij in csv.DictReader(csv_bestand)]


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
    tabel = Table(title=f"{functie.__name__} op {bestand}", title_justify="left")
    tabel.add_column("bericht")
    tabel.add_column("antwoord")
    tabel.add_column("label")
    start = time.perf_counter()
    start_cpu = time.process_time()
    juist = 0
    for tekst, label in berichten:
        antwoord = str(functie(tekst)).strip(" .!*\n").lower()
        if antwoord == label:
            juist = juist + 1
            tabel.add_row(tekst, Text(f"{antwoord} ✓", style="green"), label)
        else:
            tabel.add_row(tekst, Text(f"{antwoord} ✗", style="red"), label)
    seconden = (time.perf_counter() - start) / len(berichten)
    cpu_tijd = (time.process_time() - start_cpu) / len(berichten)
    geheugen = psutil.Process().memory_info().rss / 1_000_000
    console.print(tabel)
    console.print(f"[bold]{juist}/{len(berichten)} juist[/] · {seconden:.3f} seconden per bericht")
    console.print(f"op je eigen laptop: {cpu_tijd:.3f} seconden CPU-tijd per bericht, {geheugen:.0f} MB geheugen")
