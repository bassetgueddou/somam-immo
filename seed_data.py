# seed_data.py — versions en DA + "Résidence Le Rosier"
import os
from datetime import date
from app import create_app
from extensions import db
from models import Property, Project

app = create_app()

def ensure_img(path_rel):
    """Vérifie/Crée le chemin image; duplique placeholder s'il manque."""
    if not path_rel:
        return None
    base = os.path.abspath(os.path.dirname(__file__))
    abs_path = os.path.join(base, path_rel.lstrip("/"))
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    if not os.path.exists(abs_path):
        # copie du placeholder si l'image n'existe pas
        from shutil import copyfile
        placeholder = os.path.join(base, "static", "img", "placeholder.jpg")
        if os.path.exists(placeholder):
            copyfile(placeholder, abs_path)
    return path_rel

properties = [
    {
        "title": "Appartement T3 vue mer – Sidi Ali L’Bher",
        "description": "Appartement lumineux au 4e étage, double orientation, séjour avec balcon, cuisine équipée, deux chambres, salle de bain rénovée. Proche commerces, écoles et front de mer.",
        "city": "Béjaïa",
        "price": 17_500_000,  # ~17,5 M DA
        "surface": 78, "rooms": 3,
        "image_url": "/static/img/immobilier/appart1.jpg",
    },
    {
        "title": "Villa contemporaine avec jardin – Tichy",
        "description": "Villa individuelle sur deux niveaux, suite parentale, grand séjour, cuisine ouverte, baies vitrées, jardin arboré de 300 m².",
        "city": "Tichy",
        "price": 45_000_000,  # ~45 M DA
        "surface": 210, "rooms": 6,
        "image_url": "/static/img/immobilier/villa1.jpg",
    },
    {
        "title": "Studio rénové centre-ville – Ihaddaden",
        "description": "Studio compact idéal premier achat ou investissement locatif. Cuisine équipée, salle d’eau, fenêtres PVC, faibles charges.",
        "city": "Béjaïa",
        "price": 5_800_000,   # ~5,8 M DA
        "surface": 30, "rooms": 1,
        "image_url": "/static/img/immobilier/studio1.jpg",
    },
    {
        "title": "F4 familial – Sidi Ahmed",
        "description": "Grand F4 traversant, 3 chambres, séjour, cuisine séparée, cellier. Étage élevé avec ascenseur, vue dégagée.",
        "city": "Béjaïa",
        "price": 22_000_000,  # ~22 M DA
        "surface": 95, "rooms": 4,
        "image_url": "/static/img/immobilier/f4_sidi_ahmed.jpg",
    },
    {
        "title": "Terrain constructible – Tala Hamza",
        "description": "Terrain viabilisé en zone résidentielle, accès rapide RN9. Idéal projet de maison individuelle.",
        "city": "Tala Hamza",
        "price": 12_000_000,  # ~12 M DA
        "surface": 420, "rooms": 0,
        "image_url": "/static/img/immobilier/terrain1.jpg",
    },
    {
        "title": "Duplex récent – Oued Ghir",
        "description": "Duplex 3 chambres, 2 salles d’eau, terrasse, climatisation, parking. Construction 2022.",
        "city": "Oued Ghir",
        "price": 28_000_000,  # ~28 M DA
        "surface": 140, "rooms": 5,
        "image_url": "/static/img/immobilier/duplex1.jpg",
    },
]

projects = [
    {
        "name": "Résidence Le Rosier",
        "status": "En cours",
        "description": "Programme résidentiel avec commerces en pied d’immeuble. Logements lumineux, terrasses, vitrines commerciales, normes parasismiques et attention particulière aux performances thermiques.",
        "start_date": date(2024, 10, 1),
        "end_date": None,
        "image_url": "/static/img/projets/le_rosier.jpg",   # mets l'image réelle ici
    },
    {
        "name": "Résidence El Bahia",
        "status": "En cours",
        "description": "Programme résidentiel de 60 logements, structure béton, normes parasismiques, espaces verts et parkings.",
        "start_date": date(2025, 2, 1),
        "end_date": None,
        "image_url": "/static/img/projets/el_bahia.jpg",
    },
    {
        "name": "Complexe tertiaire Aokas",
        "status": "Études",
        "description": "Bureaux + commerces, approche HQE, optimisation thermique et acoustique.",
        "start_date": date(2025, 6, 1),
        "end_date": None,
        "image_url": "/static/img/projets/tertiaire_aokas.jpg",
    },
    {
        "name": "Lotissement Tassoust",
        "status": "En cours",
        "description": "Voirie et réseaux divers, éclairage public, espaces paysagers, lots individuels.",
        "start_date": date(2025, 3, 15),
        "end_date": None,
        "image_url": "/static/img/projets/tassoust.jpg",
    },
]

with app.app_context():
    db.create_all()
    for p in properties:
        p["image_url"] = ensure_img(p["image_url"])
    for pr in projects:
        pr["image_url"] = ensure_img(pr["image_url"])

    # ⚠️ Si tu veux repartir propre : décommente les 2 lignes suivantes pour vider puis réinsérer
    # db.drop_all(); db.create_all()

    if Project.query.count() == 0:
        db.session.add_all([Project(**pr) for pr in projects])
    if Property.query.count() == 0:
        db.session.add_all([Property(**p) for p in properties])

    db.session.commit()
    print("Données seed insérées/à jour (DA).")
