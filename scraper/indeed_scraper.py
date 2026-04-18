# scraper/indeed_scraper.py
# Version Selenium — contourne le blocage 403 de Indeed

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

MOTS_CLES = [
    "alternance développeur java",
    "alternance full stack",
    "alternance IA data",
    "alternance cybersécurité",
]

URL_BASE = "https://fr.indeed.com/jobs?q={query}&l=France&fromage=7"


# ---------------------------------------------------------
# INITIALISATION DU NAVIGATEUR
# ---------------------------------------------------------

def creer_navigateur():
    """
    Crée un navigateur Chrome configuré pour le scraping.
    headless=False = on voit le navigateur s'ouvrir (utile pour déboguer).
    Passe à headless=True quand tout fonctionne.
    """
    options = Options()

    # Pour l'instant on laisse le navigateur visible pour déboguer
    # options.add_argument("--headless")

    # Options pour éviter la détection par Indeed
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # webdriver-manager installe automatiquement le bon ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # On masque le fait que c'est Selenium
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


# ---------------------------------------------------------
# FONCTION DE SCRAPING
# ---------------------------------------------------------

def scraper_indeed(driver, mot_cle):
    """
    Scrape les offres Indeed pour un mot-clé donné.
    Retourne une liste de dictionnaires {titre, entreprise, lieu, lien}.
    """

    url = URL_BASE.format(query=mot_cle.replace(" ", "+"))
    print(f"\nRecherche : '{mot_cle}'")

    driver.get(url)

    # On attend que les cartes d'offres soient bien chargées
    # (max 10 secondes, sinon on continue quand même)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
        )
    except Exception:
        print("Timeout — la page a mis trop de temps ou aucune offre trouvée")

    # Petite pause humaine pour éviter la détection
    time.sleep(2)

    # On récupère le HTML final (après chargement JavaScript)
    soupe = BeautifulSoup(driver.page_source, "html.parser")

    cartes = soupe.find_all("div", class_="job_seen_beacon")
    print(f"{len(cartes)} offres trouvées")

    offres = []

    for carte in cartes:

        # --- Titre ---
        balise_titre = carte.find("h2", class_="jobTitle")
        titre = balise_titre.get_text(strip=True) if balise_titre else "Titre inconnu"

        # --- Entreprise ---
        balise_entreprise = carte.find("span", attrs={"data-testid": "company-name"})
        entreprise = balise_entreprise.get_text(strip=True) if balise_entreprise else "Entreprise inconnue"

        # --- Lieu ---
        balise_lieu = carte.find("div", attrs={"data-testid": "text-location"})
        lieu = balise_lieu.get_text(strip=True) if balise_lieu else "Lieu inconnu"

        # --- Lien ---
        balise_lien = carte.find("a", class_="jcs-JobTitle")
        if balise_lien and balise_lien.get("href"):
            lien = "https://fr.indeed.com" + balise_lien["href"]
        else:
            lien = "Lien indisponible"

        offres.append({
            "titre":      titre,
            "entreprise": entreprise,
            "lieu":       lieu,
            "lien":       lien,
            "mot_cle":    mot_cle,
        })

    return offres


# ---------------------------------------------------------
# TEST DU MODULE
# ---------------------------------------------------------

if __name__ == "__main__":

    driver = creer_navigateur()
    toutes_les_offres = []

    try:
        for mot_cle in MOTS_CLES:
            offres = scraper_indeed(driver, mot_cle)
            toutes_les_offres.extend(offres)
            time.sleep(3)  # pause entre chaque recherche

    finally:
        # On ferme toujours le navigateur, même en cas d'erreur
        driver.quit()

    # Affichage
    print(f"\n{'='*50}")
    print(f"Total : {len(toutes_les_offres)} offres trouvées\n")

    for offre in toutes_les_offres:
        print(f"Poste      : {offre['titre']}")
        print(f"Entreprise : {offre['entreprise']}")
        print(f"Lieu       : {offre['lieu']}")
        print(f"Lien       : {offre['lien']}")
        print("-" * 40)