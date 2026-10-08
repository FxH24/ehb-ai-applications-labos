from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from lokaal import voorspel_met_lokaal_model
from regels import voorspel_met_regel
from taalmodel import voorspel_met_taalmodel

app = FastAPI()


@app.get("/regel")
def regel(tekst: str):
    return {"sentiment": voorspel_met_regel(tekst)}


# Mini-oefening: zet hier de endpoints /lokaal en /taalmodel.


app.mount("/", StaticFiles(directory="web", html=True))
