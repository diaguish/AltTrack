# AltTrack

> Ton copilote Python pour trouver ton alternance — scraping automatique des offres, suivi des candidatures et rappels de relance, le tout depuis ton terminal.

---

## Fonctionnalités

- **Veille automatique** — scrape Indeed et Welcome to the Jungle selon tes mots-clés
- **Suivi des candidatures** — stockage dans un fichier CSV (entreprise, poste, date, statut)
- **Rappels de relance** — mail automatique via Gmail quand une candidature dépasse 10 jours sans réponse

---

## Stack technique

- Python 3.11+
- `requests` + `BeautifulSoup4` — scraping des sites simples
- `Selenium` + `webdriver-manager` — scraping des sites en JavaScript
- `pandas` — manipulation du fichier CSV
- `smtplib` — envoi des mails de relance (Gmail)

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/ton-pseudo/alttrack.git
cd AltTrack
```

### 2. Créer et activer l'environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer Gmail

Crée un fichier `config.py` à la racine (il est dans `.gitignore`, ne le push jamais) :

```python
# config.py
GMAIL_EXPEDITEUR = "ton.adresse@gmail.com"
GMAIL_MOT_DE_PASSE = "ton_mot_de_passe_application"  # mot de passe d'application Gmail
GMAIL_DESTINATAIRE = "ton.adresse@gmail.com"
```

> Pour générer un mot de passe d'application Gmail : Mon compte Google → Sécurité → Validation en deux étapes → Mots de passe des applications.

---

## Structure du projet
AltTrack/
│
├── scraper/
│   ├── indeed_scraper.py       # Scraping Indeed via Selenium
│   └── wttj_scraper.py         # Scraping Welcome to the Jungle
│
├── tracker/
│   └── candidatures.py         # Gestion du fichier CSV
│
├── notifier/
│   └── gmail_notifier.py       # Envoi des mails de relance
│
├── main.py                     # Script principal
├── candidatures.csv            # Base de données des candidatures
├── requirements.txt            # Dépendances Python
├── config.py                   # Credentials Gmail (non versionné)
└── README.md

---

## Utilisation

### Lancer la veille des offres

```bash
python main.py
```

### Ajouter une candidature manuellement

```bash
python tracker/candidatures.py
```

---

## Mots-clés configurés

- `alternance développeur java`
- `alternance full stack`
- `alternance IA data`
- `alternance cybersécurité`

> Modifiables dans `scraper/indeed_scraper.py` → variable `MOTS_CLES`

---

## Auteure

**Diago Alioune Tall**
