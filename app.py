from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from essai import recommander_vin, recommander_vin_plat
from donnees_vins import BASE_PLATS
from rapidfuzz import process, fuzz
import unicodedata

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

app = Flask(__name__)
CORS(app)

MA_CLE_SPOONACULAR = os.environ.get("SPOONACULAR_KEY", "8e3a8ffbe0934a31910616110c98b2c5")
MA_CLE_GEMINI      = os.environ.get("GEMINI_KEY")
MA_CLE_CLAUDE      = os.environ.get("CLAUDE_KEY")

# Liste des plats pour fuzzy search
PLATS_LIST = list(BASE_PLATS.keys())


# ── Helpers ───────────────────────────────────────────────────────────────────

def normalize(text):
    """Supprime les accents pour comparaison insensible aux accents."""
    return unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8").lower()

PLATS_NORMALIZED = {normalize(p): p for p in PLATS_LIST}


def fuzzy_search_bdd(query, limit=5):
    """Recherche floue dans BASE_PLATS avec gestion des accents."""
    q_norm = normalize(query)
    results = process.extract(
        q_norm,
        list(PLATS_NORMALIZED.keys()),
        scorer=fuzz.partial_ratio,
        limit=limit,
        score_cutoff=50
    )
    return [PLATS_NORMALIZED[r[0]].title() for r in results]


def search_spoonacular(query, api_key, limit=4):
    """Cherche des suggestions de plats sur Spoonacular."""
    try:
        r = requests.get(
            "https://api.spoonacular.com/recipes/complexSearch",
            params={"query": query, "number": limit, "apiKey": api_key},
            timeout=6,
        )
        data = r.json()
        return [item["title"] for item in data.get("results", [])]
    except Exception as e:
        print(f"Erreur Spoonacular search : {e}")
        return []


def analyser_plat_avec_api(nom_plat, api_key):
    """Récupère les ingrédients d\'un plat via Spoonacular."""
    try:
        r = requests.get(
            "https://api.spoonacular.com/recipes/complexSearch",
            params={"query": nom_plat, "number": 1, "apiKey": api_key},
            timeout=8,
        )
        data = r.json()
        if not data.get("results"):
            return None
        recipe_id    = data["results"][0]["id"]
        recipe_title = data["results"][0]["title"]
        r2 = requests.get(
            f"https://api.spoonacular.com/recipes/{recipe_id}/information",
            params={"apiKey": api_key},
            timeout=8,
        )
        recipe_data = r2.json()
        ingredients = [ing["name"] for ing in recipe_data.get("extendedIngredients", [])[:5]]
        return {"nom": recipe_title, "ingredients": ingredients}
    except Exception as e:
        print(f"Erreur Spoonacular : {e}")
        return None


def generer_mots_cles_gemini(nom_plat, vins, api_key):
    """Génère des mots-clés d\'accord mets-vins via Gemini."""
    if not api_key or not GEMINI_AVAILABLE:
        return {}
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        mots_cles = {}
        for vin in vins[:3]:
            prompt = (
                f"Pour l\'accord entre le plat \'{nom_plat}\' et le vin \'{vin}\', "
                f"donne exactement 3 mots-clés de dégustation séparés par des virgules. "
                f"Exemples: minéral, fruité, élégant. Réponds uniquement avec les 3 mots."
            )
            response = model.generate_content(prompt)
            mots = [m.strip().lower() for m in response.text.split(",")][:3]
            mots_cles[vin] = mots
        return mots_cles
    except Exception as e:
        print(f"Erreur Gemini : {e}")
        return {}


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return jsonify({"status": "VinAccord API is running"})


@app.route("/search", methods=["GET"])
def search():
    """Suggestions pour le dropdown : BDD (fuzzy) + Spoonacular."""
    query  = request.args.get("q", "").strip()
    source = request.args.get("source", "bdd")  # "bdd" ou "spoonacular"

    if not query or len(query) < 2:
        return jsonify({"bdd": [], "spoonacular": []})

    if source == "spoonacular":
        suggestions = search_spoonacular(query, MA_CLE_SPOONACULAR, limit=4)
        return jsonify({"bdd": [], "spoonacular": suggestions})

    # Source BDD par défaut
    bdd_results = fuzzy_search_bdd(query, limit=5)
    return jsonify({"bdd": bdd_results, "spoonacular": []})


@app.route("/recommend", methods=["POST"])
def recommend():
    body     = request.get_json(force=True)
    nom_plat = body.get("plat", "").strip().lower()
    ingredients_directs = body.get("ingredients", None)

    # ── Mode ingrédients directs ──
    if ingredients_directs:
        rec = recommander_vin_plat(ingredients_directs)
        if isinstance(rec, dict) and rec.get("vins"):
            vins = rec["vins"]
            mots_cles = generer_mots_cles_gemini("ce plat", vins, MA_CLE_GEMINI)
            return jsonify({
                "plat": "Sélection par ingrédients",
                "vins": vins,
                "couleur": rec.get("couleur_dominante", ""),
                "mots_cles": mots_cles,
                "source": "ingredients"
            })
        return jsonify({"error": "Impossible de déterminer un vin pour ces ingrédients."}), 404

    # ── Mode plat ──
    if not nom_plat:
        return jsonify({"error": "Veuillez entrer un nom de plat."}), 400

    # Priorité 1 : BDD locale (exact + fuzzy)
    if nom_plat in BASE_PLATS:
        rec  = recommander_vin(nom_plat=nom_plat, ingredients=None)
        vins = rec["vins"]
        mots_cles = generer_mots_cles_gemini(nom_plat, vins, MA_CLE_GEMINI)
        return jsonify({"plat": nom_plat.title(), "vins": vins, "mots_cles": mots_cles, "source": "expert"})

    # Fuzzy fallback BDD
    fuzzy_results = process.extractOne(
        normalize(nom_plat),
        list(PLATS_NORMALIZED.keys()),
        scorer=fuzz.partial_ratio,
        score_cutoff=75
    )
    if fuzzy_results:
        plat_trouve = PLATS_NORMALIZED[fuzzy_results[0]]
        rec  = recommander_vin(nom_plat=plat_trouve, ingredients=None)
        vins = rec["vins"]
        mots_cles = generer_mots_cles_gemini(plat_trouve, vins, MA_CLE_GEMINI)
        return jsonify({"plat": plat_trouve.title(), "vins": vins, "mots_cles": mots_cles, "source": "expert"})

    # Priorité 2 : Spoonacular
    resultat    = analyser_plat_avec_api(nom_plat, MA_CLE_SPOONACULAR)
    ingredients = resultat["ingredients"] if resultat else None
    rec         = recommander_vin(nom_plat=nom_plat, ingredients=ingredients)

    if rec.get("vins"):
        display_name = resultat["nom"] if resultat else nom_plat.title()
        vins = rec["vins"]
        mots_cles = generer_mots_cles_gemini(display_name, vins, MA_CLE_GEMINI)
        return jsonify({"plat": display_name, "vins": vins, "mots_cles": mots_cles, "source": "ingredients"})

    return jsonify({"error": "Plat non reconnu — essayez un autre nom."}), 404


if __name__ == "__main__":
    app.run(debug=True)
'''

with open("output/vinaccord-back/app.py", "w", encoding="utf-8") as f:
    f.write(app_py)

# Copier essai.py et donnees_vins.py depuis le dossier output (versions corrigées)
shutil.copy("output/essai.py", "output/vinaccord-back/essai.py")
shutil.copy("output/donnees_vins.py", "output/vinaccord-back/donnees_vins.py")
print("app.py OK")
print("essai.py OK (copié)")
print("donnees_vins.py OK (copié)")
