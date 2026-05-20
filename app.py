from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
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

MA_CLE_SPOONACULAR = os.environ.get('SPOONACULAR_KEY', '')
MA_CLE_GEMINI      = os.environ.get('GEMINI_KEY')

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

def gemini_mots_cles(nom_plat, vins, api_key):
    """Genere 3 mots-cles de degustation pour chaque vin via Gemini."""
    if not api_key or not GEMINI_AVAILABLE:
        return {}
    try:
        client = genai.Client(api_key=api_key)
        mots_cles = {}
        for vin in vins[:5]:
            prompt = (
                'Pour l accord entre le plat ' + nom_plat + ' et le vin ' + vin + ', '
                'donne exactement 3 mots-cles de degustation separes par des virgules. '
                'Exemples: mineral, fruite, elegant. Reponds uniquement avec les 3 mots, rien d autre.'
            )
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            mots = [m.strip().lower() for m in response.text.strip().split(',')][:3]
            mots_cles[vin] = mots
        return mots_cles
    except Exception as e:
        print('Erreur Gemini mots_cles : ' + str(e))
        return {}

def gemini_vin_inconnu(nom_plat, api_key):
    """Pour un plat inconnu, Gemini suggere 1 type de vin + 3 mots-cles."""
    if not api_key or not GEMINI_AVAILABLE:
        return None
    try:
        client = genai.Client(api_key=api_key)
        prompt = (
            'Quel type de vin s accorde le mieux avec le plat : ' + nom_plat + ' ? '
            'Reponds avec exactement ce format sur deux lignes:\n'
            'VIN: [type de vin en 2-4 mots]\n'
            'MOTS: [mot1, mot2, mot3]\n'
            'Exemple:\nVIN: Bourgogne blanc sec\nMOTS: mineral, fruite, elegant\n'
            'Ne mets rien d autre.'
        )
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        lines = response.text.strip().splitlines()
        vin = None
        mots = []
        for line in lines:
            if line.startswith('VIN:'):
                vin = line.replace('VIN:', '').strip()
            elif line.startswith('MOTS:'):
                mots = [m.strip().lower() for m in line.replace('MOTS:', '').split(',')][:3]
        if vin:
            return {'vin': vin, 'mots': mots}
        return None
    except Exception as e:
        print('Erreur Gemini vin_inconnu : ' + str(e))
        return None

@app.route('/')
def index():
    return jsonify({'status': 'VinAccord API is running'})

@app.route('/search', methods=['GET'])
def search():
    query  = request.args.get('q', '').strip()
    source = request.args.get('source', 'bdd')
    if not query or len(query) < 2:
        return jsonify({'bdd': [], 'spoonacular': []})
    if source == 'spoonacular' and MA_CLE_SPOONACULAR:
        try:
            r = requests.get(
                'https://api.spoonacular.com/recipes/complexSearch',
                params={'query': query, 'number': 4, 'apiKey': MA_CLE_SPOONACULAR},
                timeout=6,
            )
            data = r.json()
            suggestions = [item['title'] for item in data.get('results', [])]
            return jsonify({'bdd': [], 'spoonacular': suggestions})
        except Exception as e:
            print('Erreur Spoonacular search : ' + str(e))
            return jsonify({'bdd': [], 'spoonacular': []})
    bdd_results = fuzzy_search_bdd(query, limit=3)
    return jsonify({'bdd': bdd_results, 'spoonacular': []})

@app.route('/recommend', methods=['POST'])
def recommend():
    body     = request.get_json(force=True)
    nom_plat = body.get('plat', '').strip().lower()
    ingredients_directs = body.get('ingredients', None)

    if ingredients_directs:
        rec = recommander_vin_plat(ingredients_directs)
        if isinstance(rec, dict) and rec.get('vins'):
            vins = rec['vins']
            mots_cles = gemini_mots_cles('ce plat', vins, MA_CLE_GEMINI)
            return jsonify({
                'plat': 'Selection par ingredients',
                'vins': vins,
                'couleur': rec.get('couleur_dominante', ''),
                'mots_cles': mots_cles,
                'source': 'expert'
            })
        return jsonify({'error': 'Impossible de determiner un vin pour ces ingredients.'}), 404

    if not nom_plat:
        return jsonify({'error': 'Veuillez entrer un nom de plat.'}), 400

    # Plat exact dans la BDD
    if nom_plat in BASE_PLATS:
        rec  = recommander_vin(nom_plat=nom_plat, ingredients=None)
        vins = rec['vins']
        mots_cles = gemini_mots_cles(nom_plat, vins, MA_CLE_GEMINI)
        return jsonify({'plat': nom_plat.title(), 'vins': vins, 'mots_cles': mots_cles, 'source': 'expert'})

    # Fuzzy match dans la BDD
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
        mots_cles = gemini_mots_cles(plat_trouve, vins, MA_CLE_GEMINI)
        return jsonify({'plat': plat_trouve.title(), 'vins': vins, 'mots_cles': mots_cles, 'source': 'expert'})

    # Plat inconnu => Gemini suggere 1 vin
    resultat_gemini = gemini_vin_inconnu(nom_plat, MA_CLE_GEMINI)
    if resultat_gemini:
        vin  = resultat_gemini['vin']
        mots = resultat_gemini['mots']
        return jsonify({
            'plat': nom_plat.title(),
            'vins': [vin],
            'mots_cles': {vin: mots},
            'source': 'expert'
        })

    return jsonify({'error': 'Plat non reconnu, essayez un autre nom.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
