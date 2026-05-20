from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from essai import recommander_vin, recommander_vin_plat
from donnees_vins import BASE_PLATS
from rapidfuzz import process, fuzz
import unicodedata

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

app = Flask(__name__)
CORS(app)

MA_CLE_GEMINI = os.environ.get('GEMINI_KEY')

PLATS_LIST = list(BASE_PLATS.keys())

def normalize(text):
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8').lower()

PLATS_NORMALIZED = {normalize(p): p for p in PLATS_LIST}

def fuzzy_search_bdd(query, limit=3):
    q_norm = normalize(query)
    results = process.extract(
        q_norm,
        list(PLATS_NORMALIZED.keys()),
        scorer=fuzz.partial_ratio,
        limit=limit,
        score_cutoff=70
    )
    return [PLATS_NORMALIZED[r[0]].title() for r in results]

def generer_mots_cles_gemini(nom_plat, vins, api_key):
    if not api_key or not GEMINI_AVAILABLE:
        return {}
    try:
        client = genai.Client(api_key=api_key)
        mots_cles = {}
        for vin in vins[:3]:
            prompt = (
                'Pour l accord entre le plat ' + nom_plat + ' et le vin ' + vin + ', '
                'donne exactement 3 mots-cles de degustation separes par des virgules. '
                'Exemples: mineral, fruite, elegant. Reponds uniquement avec les 3 mots.'
            )
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            mots = [m.strip().lower() for m in response.text.split(',')][:3]
            mots_cles[vin] = mots
        return mots_cles
    except Exception as e:
        print('Erreur Gemini : ' + str(e))
        return {}

@app.route('/')
def index():
    return jsonify({'status': 'VinAccord API is running'})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    if not query or len(query) < 2:
        return jsonify({'bdd': []})
    bdd_results = fuzzy_search_bdd(query, limit=3)
    return jsonify({'bdd': bdd_results})

@app.route('/recommend', methods=['POST'])
def recommend():
    body     = request.get_json(force=True)
    nom_plat = body.get('plat', '').strip().lower()
    ingredients_directs = body.get('ingredients', None)

    if ingredients_directs:
        rec = recommander_vin_plat(ingredients_directs)
        if isinstance(rec, dict) and rec.get('vins'):
            vins = rec['vins']
            mots_cles = generer_mots_cles_gemini('ce plat', vins, MA_CLE_GEMINI)
            return jsonify({
                'plat': 'Selection par ingredients',
                'vins': vins,
                'couleur': rec.get('couleur_dominante', ''),
                'mots_cles': mots_cles,
                'source': 'ingredients'
            })
        return jsonify({'error': 'Impossible de determiner un vin pour ces ingredients.'}), 404

    if not nom_plat:
        return jsonify({'error': 'Veuillez entrer un nom de plat.'}), 400

    if nom_plat in BASE_PLATS:
        rec  = recommander_vin(nom_plat=nom_plat, ingredients=None)
        vins = rec['vins']
        mots_cles = generer_mots_cles_gemini(nom_plat, vins, MA_CLE_GEMINI)
        return jsonify({'plat': nom_plat.title(), 'vins': vins, 'mots_cles': mots_cles, 'source': 'expert'})

    fuzzy_result = process.extractOne(
        normalize(nom_plat),
        list(PLATS_NORMALIZED.keys()),
        scorer=fuzz.partial_ratio,
        score_cutoff=75
    )
    if fuzzy_result:
        plat_trouve = PLATS_NORMALIZED[fuzzy_result[0]]
        rec  = recommander_vin(nom_plat=plat_trouve, ingredients=None)
        vins = rec['vins']
        mots_cles = generer_mots_cles_gemini(plat_trouve, vins, MA_CLE_GEMINI)
        return jsonify({'plat': plat_trouve.title(), 'vins': vins, 'mots_cles': mots_cles, 'source': 'expert'})

    return jsonify({'error': 'Plat non reconnu, essayez un autre nom.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
