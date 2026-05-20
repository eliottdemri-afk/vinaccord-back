from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from essai import recommander_vin, recommander_vin_plat
from donnees_vins import BASE_PLATS

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

app = Flask(__name__)
CORS(app)

MA_CLE_SPOONACULAR = os.environ.get("SPOONACULAR_KEY", "8e3a8ffbe0934a31910616110c98b2c5")
MA_CLE_CLAUDE      = os.environ.get("CLAUDE_KEY")


# ── Helpers ───────────────────────────────────────────────────────────────────

def analyser_plat_avec_api(nom_plat, api_key):
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


def analyser_plat_avec_claude(nom_plat, api_key):
    client  = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"Liste les 5 ingrédients principaux du plat '{nom_plat}' en anglais, séparés par des virgules. Réponds uniquement avec la liste."
        }]
    )
    return [i.strip() for i in message.content[0].text.split(",")]


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return jsonify({"status": "VinAccord API is running"})


@app.route("/search", methods=["GET"])
def search():
    """Retourne les suggestions de plats pour l'autocomplétion."""
    query = request.args.get("q", "").strip().lower()
    if not query or len(query) < 2:
        return jsonify([])

    suggestions = []
    for plat in BASE_PLATS.keys():
        if query in plat.lower():
            suggestions.append(plat.title())
        if len(suggestions) >= 8:
            break

    return jsonify(suggestions)


@app.route("/recommend", methods=["POST"])
def recommend():
    body     = request.get_json(force=True)
    nom_plat = body.get("plat", "").strip().lower()
    ingredients_directs = body.get("ingredients", None)  # mode ingrédients directs

    # Mode ingrédients directs (page ingrédients)
    if ingredients_directs:
        rec = recommander_vin_plat(ingredients_directs)
        if isinstance(rec, dict) and rec.get("vins"):
            return jsonify({
                "plat": "Sélection par ingrédients",
                "vins": rec["vins"],
                "couleur": rec.get("couleur_dominante", ""),
                "source": "ingredients"
            })
        return jsonify({"error": "Impossible de déterminer un vin pour ces ingrédients."}), 404

    # Mode plat
    if not nom_plat:
        return jsonify({"error": "Veuillez entrer un nom de plat."}), 400

    # Priorité 1 : BDD locale
    if nom_plat in BASE_PLATS:
        rec = recommander_vin(nom_plat=nom_plat, ingredients=None)
        return jsonify({"plat": nom_plat.title(), "vins": rec["vins"], "source": "expert"})

    # Priorité 2 : Spoonacular
    resultat    = analyser_plat_avec_api(nom_plat, MA_CLE_SPOONACULAR)
    ingredients = resultat["ingredients"] if resultat else None
    rec         = recommander_vin(nom_plat=nom_plat, ingredients=ingredients)

    if rec.get("vins"):
        display_name = resultat["nom"] if resultat else nom_plat.title()
        return jsonify({"plat": display_name, "vins": rec["vins"], "source": "ingredients"})

    # Priorité 3 : Claude
    if MA_CLE_CLAUDE and ANTHROPIC_AVAILABLE:
        try:
            ingredients_claude = analyser_plat_avec_claude(nom_plat, MA_CLE_CLAUDE)
            rec = recommander_vin(nom_plat=nom_plat, ingredients=ingredients_claude)
            if rec.get("vins"):
                return jsonify({"plat": nom_plat.title(), "vins": rec["vins"], "source": "claude"})
        except Exception as e:
            print(f"Erreur Claude : {e}")

    return jsonify({"error": "Plat non reconnu — essayez un autre nom."}), 404


if __name__ == "__main__":
    app.run(debug=True)
