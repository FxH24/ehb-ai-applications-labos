// De webpagina van labo 2. Ze stuurt het ticket naar jouw API, één keer per aanpak,
// toont de velden naast elkaar, en wat de helpdesk met het ticket zou doen.
// Je hoeft hier niets te wijzigen: de opdracht zit in api.py.

const TEAMS = {
  facturatie: "Boekhouding",
  levering: "Logistiek",
  defect: "Werkplaats",
  account: "Klantendienst",
  verhuur: "Verhuur",
};
const TALEN = { nl: "het Nederlands", fr: "het Frans" };

const formulier = document.querySelector("#formulier");
const tekstveld = document.querySelector("#tekst");
const rijen = [...document.querySelectorAll("tr[data-aanpak]")];
const acties = document.querySelector("#acties");

document.querySelector("#voorbeelden").addEventListener("change", (event) => {
  if (event.target.value) tekstveld.value = event.target.value;
});

// Eén categorie ("categorie") of een lijst ("categorieen"): altijd een lijst terug.
function categorieen(data) {
  if (Array.isArray(data.categorieen)) return data.categorieen;
  if (data.categorie) return [data.categorie];
  return [];
}

async function vulRij(rij, tekst) {
  const cellen = ["categorie", "taal", "klantnummer", "factuurnummer"].map((veld) => rij.querySelector(`.${veld}`));
  const tijdCel = rij.querySelector(".tijd");
  cellen.forEach((cel) => { cel.textContent = "…"; cel.className = cel.classList[0]; });
  tijdCel.textContent = "";
  const start = performance.now();
  try {
    const antwoord = await fetch(`/${rij.dataset.aanpak}?tekst=${encodeURIComponent(tekst)}`);
    if (antwoord.status === 404) {
      cellen[0].textContent = "nog geen endpoint";
      cellen[0].classList.add("onbekend");
      cellen.slice(1).forEach((cel) => { cel.textContent = ""; });
      return undefined;
    }
    if (!antwoord.ok) throw new Error(antwoord.status);
    const data = await antwoord.json();
    cellen[0].textContent = categorieen(data).join(", ") || "—";
    cellen[1].textContent = data.taal ?? "—";
    cellen[2].textContent = data.klantnummer ?? "—";
    cellen[3].textContent = data.factuurnummer ?? "—";
    tijdCel.textContent = `${Math.round(performance.now() - start)} ms`;
    return data;
  } catch (fout) {
    cellen[0].textContent = "fout: kijk in de terminal van je API";
    cellen[0].classList.add("onbekend");
    cellen.slice(1).forEach((cel) => { cel.textContent = ""; });
    return undefined;
  }
}

function toonActies(data, aanpak) {
  acties.innerHTML = "";
  if (!data) {
    acties.innerHTML = "<li>Nog geen antwoord om mee te werken.</li>";
    return;
  }
  const regels = [];
  const teams = categorieen(data).map((c) => TEAMS[c] ?? c);
  regels.push(`Doorsturen naar: ${teams.join(" en ") || "niemand (geen categorie)"}`);
  regels.push(data.taal ? `Antwoorden in ${TALEN[data.taal] ?? data.taal}` : "Taal onbekend: antwoorden in het Nederlands en het Frans");
  if (data.klantnummer) regels.push(`Klant opzoeken: ${data.klantnummer}`);
  if (data.factuurnummer) regels.push(`Factuur opzoeken: ${data.factuurnummer}`);
  for (const regel of regels) {
    const li = document.createElement("li");
    li.textContent = regel;
    acties.append(li);
  }
  const bron = document.createElement("li");
  bron.className = "bron";
  bron.textContent = `(gelezen door: ${aanpak})`;
  acties.append(bron);
}

formulier.addEventListener("submit", async (event) => {
  event.preventDefault();
  const tekst = tekstveld.value;
  acties.innerHTML = "<li>…</li>";
  const antwoorden = await Promise.all(rijen.map((rij) => vulRij(rij, tekst)));
  // de helpdesk gebruikt de laatste aanpak in de tabel die een antwoord gaf
  for (let i = rijen.length - 1; i >= 0; i--) {
    if (antwoorden[i]) {
      toonActies(antwoorden[i], rijen[i].cells[0].textContent);
      return;
    }
  }
  toonActies(undefined);
});
