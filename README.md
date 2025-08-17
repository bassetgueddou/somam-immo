# Site web — SNC Bouanani & Cie SOMAM (Bâtiment & Immobilier)

# 🌍 SOMAM – Site web de gestion immobilière et de projets

Ce projet a été développé dans le cadre de mon **stage de fin d’année (Licence Informatique Bac+3)** à la société **SNC Bouanani & Cie SOMAM** (secteur Bâtiment & Immobilier).  
L’objectif était de concevoir un site web permettant de mettre en valeur les **biens immobiliers** et les **projets de construction** réalisés par l’entreprise.

---

## 📌 Fonctionnalités principales

✅ Page d’accueil avec carrousel dynamique (Bootstrap 5).  
✅ Catalogue des **biens immobiliers** (filtrage par ville et prix).  
✅ Fiches détaillées avec description, surface, prix et photos.  
✅ Section **projets récents** (affichage dynamique depuis la base de données).  
✅ Back-office simplifié pour l’administrateur.  
✅ Sécurité (CSRF protection, validation des formulaires).  
✅ Base de données SQLite (extensible vers PostgreSQL/MySQL).

---

## 🛠️ Technologies utilisées

- **Backend** : Python 3, Flask, SQLAlchemy  
- **Frontend** : HTML5, CSS3, Bootstrap 5, Jinja2  
- **Base de données** : SQLite (par défaut)  
- **Outils** : Git, VS Code, Virtualenv  
- **Gestion sécurité** : Flask-WTF, CSRFProtect  

---

## ⚙️ Installation et utilisation

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/toncompte/somam.git
cd somam


## Démarrage

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # puis ajustez les variables (SECRET_KEY, ADMIN_*, etc.)
python app.py
```

Accès admin : `ADMIN_USERNAME=admin` / `ADMIN_PASSWORD=admin123` (modifiez-les dans `.env`).

## Structure

- `app.py`: factory Flask + enregistrement des blueprints
- `models.py`: SQLAlchemy (Property, Project, Message)
- `views.py`: routes publiques + admin CRUD
- `templates/`: pages Jinja + Bootstrap
- `static/`: CSS/JS + images
- `instance/`: base SQLite (créée automatiquement)

## Données de test

Vous pouvez créer quelques projets/biens via l'interface admin.

## Déploiement (piste rapide)

- Gunicorn + Nginx sur un VPS
- `FLASK_ENV=production`, `DEBUG=0`
- Base SQLite (petit) ou Postgres (recommandé si croissance)
