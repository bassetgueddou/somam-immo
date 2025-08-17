import os
from flask import Flask
from flask_wtf import CSRFProtect
from extensions import db  # <-- ici !
# Charger .env si présent
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    register_template_filters(app)


    # Dossier du projet (absolu)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # Dossier instance (absolu)
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    os.makedirs(INSTANCE_DIR, exist_ok=True)

    # Chemin DB absolu (Windows friendly)
    db_path = os.path.join(INSTANCE_DIR, "app.db")
    db_uri_default = "sqlite:///" + db_path.replace("\\", "/")

    # Si une URI env relative, on l’ignore
    env_uri = os.environ.get("SQLALCHEMY_DATABASE_URI", "").strip()
    if env_uri.startswith("sqlite:///") and not env_uri.startswith("sqlite:////"):
        env_uri = ""
    SQLALCHEMY_DATABASE_URI = env_uri or db_uri_default

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-key"),
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Attacher les extensions
    db.init_app(app)
    csrf.init_app(app)

    # Import modèles après init (évite boucles)
    from models import Property, Project, Message  # noqa: F401
    with app.app_context():
        db.create_all()  # crée la base/tables si besoin

    # Blueprints
    from views import main_bp, admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    return app

# --- Formatage DZD pour les templates ---
def format_dzd(value):
    """
    Formate un nombre en Dinar algérien avec séparateur d’espace.
    Ex: 28000000 -> '28 000 000 DA'
    """
    try:
        n = int(round(float(value)))
        return f"{n:,}".replace(",", " ") + " DA"
    except Exception:
        return f"{value} DA"

def register_template_filters(app: Flask):
    app.add_template_filter(format_dzd, name="dzd")


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
