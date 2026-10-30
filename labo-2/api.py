from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from meerdere import lees_meerdere
from regels import lees_met_regels
from structured_output import lees_met_schema

app = FastAPI()


@app.get("/regels")
def regels(tekst: str):
    return lees_met_regels(tekst)


# Opdracht: maak hier /schema, /meerdere en /ticket.


app.mount("/", StaticFiles(directory="web", html=True))
