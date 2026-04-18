# test_scraping.py
# Premier exemple de scraping — on s'entraîne sur un site fait pour ça

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------
# ÉTAPE 1 : Télécharger la page
# ---------------------------------------------------------
# On utilise "quotes.toscrape.com", un site fait exprès pour
# apprendre le scraping — pas de blocage, pas de JS

url = "http://quotes.toscrape.com"

# requests.get() envoie une requête HTTP GET, comme ton navigateur
reponse = requests.get(url)

# On vérifie que la requête a réussi (200 = OK)
print(f"Statut de la requête : {reponse.status_code}")

# ---------------------------------------------------------
# ÉTAPE 2 : Analyser le HTML avec BeautifulSoup
# ---------------------------------------------------------
# On crée un objet "soupe" qui représente tout le HTML de la page
# "html.parser" est le moteur d'analyse intégré à Python

soupe = BeautifulSoup(reponse.text, "html.parser")

# ---------------------------------------------------------
# ÉTAPE 3 : Extraire les données
# ---------------------------------------------------------
# Sur ce site, chaque citation est dans une balise <span class="text">
# On récupère TOUTES les citations d'un coup avec find_all()

citations = soupe.find_all("span", class_="text")
auteurs   = soupe.find_all("small", class_="author")

print(f"\n{len(citations)} citations trouvées :\n")

# On parcourt les citations et auteurs ensemble avec zip()
for citation, auteur in zip(citations, auteurs):
    # .get_text() extrait le texte brut, sans les balises HTML
    print(f"{citation.get_text()}")
    print(f"  — {auteur.get_text()}\n")