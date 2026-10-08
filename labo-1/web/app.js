// De webpagina van labo 1. Ze stuurt het bericht naar jouw API, één keer per aanpak,
// en toont de antwoorden naast elkaar.

// Mini-oefening: vraag aan de API wat één aanpak van deze tekst vindt.
// De URL is bijvoorbeeld /regel?tekst=Mijn%20fiets%20is%20kapot
// Het antwoord is JSON, bijvoorbeeld {"sentiment": "negatief"}.
async function vraagSentiment(aanpak, tekst) {
  // TODO: vul aan met fetch()
}

// ---------- Vanaf hier hoef je niets te wijzigen ----------

const formulier = document.querySelector("#formulier");
const rijen = [...document.querySelectorAll("tr[data-aanpak]")];
const samenvatting = document.querySelector("#samenvatting");

async function vulRij(rij, tekst) {
  const antwoordCel = rij.querySelector(".antwoord");
  const tijdCel = rij.querySelector(".tijd");
  antwoordCel.textContent = "…";
  antwoordCel.className = "antwoord";
  tijdCel.textContent = "";
  const start = performance.now();
  try {
    const sentiment = await vraagSentiment(rij.dataset.aanpak, tekst);
    antwoordCel.textContent = sentiment ?? "geen antwoord (is vraagSentiment af?)";
    antwoordCel.classList.add(sentiment === "positief" ? "positief" : sentiment === "negatief" ? "negatief" : "onbekend");
    tijdCel.textContent = `${Math.round(performance.now() - start)} ms`;
    return sentiment;
  } catch (fout) {
    antwoordCel.textContent = "fout: kijk in de terminal van je API";
    antwoordCel.classList.add("onbekend");
    return undefined;
  }
}

formulier.addEventListener("submit", async (event) => {
  event.preventDefault();
  const tekst = document.querySelector("#tekst").value;
  samenvatting.textContent = "";
  const antwoorden = await Promise.all(rijen.map((rij) => vulRij(rij, tekst)));
  const negatief = antwoorden.filter((a) => a === "negatief").length;
  const positief = antwoorden.filter((a) => a === "positief").length;
  if (positief + negatief < rijen.length) {
    samenvatting.textContent = "Niet elke aanpak gaf een antwoord.";
  } else if (positief === 0 || negatief === 0) {
    samenvatting.textContent = `Alle aanpakken zijn het eens: ${antwoorden[0]}.`;
  } else {
    samenvatting.textContent = `Ze zijn het niet eens: ${positief} keer positief, ${negatief} keer negatief.`;
  }
});
