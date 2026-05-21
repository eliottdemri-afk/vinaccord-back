from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import resend
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
RESEND_API_KEY     = os.environ.get('RESEND_API_KEY')
GMAIL_USER         = os.environ.get('GMAIL_USER', 'eliott.demri@gmail.com')

PLATS_LIST = list(BASE_PLATS.keys())

def normalize(text):
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8').lower()

PLATS_NORMALIZED = {normalize(p): p for p in PLATS_LIST}

def fuzzy_search_bdd(query, limit=3):
    q_norm = normalize(query)
    results = process.extract(
        q_norm, list(PLATS_NORMALIZED.keys()),
        scorer=fuzz.partial_ratio, limit=limit, score_cutoff=70
    )
    return [PLATS_NORMALIZED[r[0]].title() for r in results]

def gemini_mots_cles(nom_plat, vins, api_key):
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
            response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
            mots = [m.strip().lower() for m in response.text.strip().split(',')][:3]
            mots_cles[vin] = mots
        return mots_cles
    except Exception as e:
        print('Erreur Gemini mots_cles : ' + str(e))
        return {}

def gemini_vin_inconnu(nom_plat, api_key):
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
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        lines = response.text.strip().splitlines()
        vin, mots = None, []
        for line in lines:
            if line.startswith('VIN:'):
                vin = line.replace('VIN:', '').strip()
            elif line.startswith('MOTS:'):
                mots = [m.strip().lower() for m in line.replace('MOTS:', '').split(',')][:3]
        return {'vin': vin, 'mots': mots} if vin else None
    except Exception as e:
        print('Erreur Gemini vin_inconnu : ' + str(e))
        return None

def send_email(subject, body):
    if not RESEND_API_KEY:
        raise ValueError('RESEND_API_KEY manquante.')
    resend.api_key = RESEND_API_KEY
    resend.Emails.send({
        'from': 'Vin/20 <onboarding@resend.dev>',
        'to': [GMAIL_USER],
        'subject': subject,
        'text': body
    })

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
            suggestions = [item['title'] for item in r.json().get('results', [])]
            return jsonify({'bdd': [], 'spoonacular': suggestions})
        except Exception as e:
            print('Erreur Spoonacular : ' + str(e))
            return jsonify({'bdd': [], 'spoonacular': []})
    return jsonify({'bdd': fuzzy_search_bdd(query, limit=3), 'spoonacular': []})

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
            return jsonify({'plat': 'Selection par ingredients', 'vins': vins,
                            'couleur': rec.get('couleur_dominante', ''),
                            'mots_cles': mots_cles, 'source': 'expert'})
        return jsonify({'error': 'Impossible de determiner un vin pour ces ingredients.'}), 404

    if not nom_plat:
        return jsonify({'error': 'Veuillez entrer un nom de plat.'}), 400

    if nom_plat in BASE_PLATS:
        rec = recommander_vin(nom_plat=nom_plat, ingredients=None)
        vins = rec['vins']
        mots_cles = gemini_mots_cles(nom_plat, vins, MA_CLE_GEMINI)
        return jsonify({'plat': nom_plat.title(), 'vins': vins, 'mots_cles': mots_cles, 'source': 'expert'})

    fuzzy_result = process.extractOne(
        normalize(nom_plat), list(PLATS_NORMALIZED.keys()),
        scorer=fuzz.partial_ratio, score_cutoff=75
    )
    if fuzzy_result:
        plat_trouve = PLATS_NORMALIZED[fuzzy_result[0]]
        rec = recommander_vin(nom_plat=plat_trouve, ingredients=None)
        vins = rec['vins']
        mots_cles = gemini_mots_cles(plat_trouve, vins, MA_CLE_GEMINI)
        return jsonify({'plat': plat_trouve.title(), 'vins': vins, 'mots_cles': mots_cles, 'source': 'expert'})

    resultat_gemini = gemini_vin_inconnu(nom_plat, MA_CLE_GEMINI)
    if resultat_gemini:
        vin  = resultat_gemini['vin']
        mots = resultat_gemini['mots']
        return jsonify({'plat': nom_plat.title(), 'vins': [vin],
                        'mots_cles': {vin: mots}, 'source': 'expert'})

    return jsonify({'error': 'Plat non reconnu, essayez un autre nom.'}), 404

@app.route('/contribution', methods=['POST'])
def contribution():
    body       = request.get_json(force=True)
    prenom     = body.get('prenom', '').strip()
    plat       = body.get('plat', '').strip()
    vin        = body.get('vin', '').strip()
    experience = body.get('experience', '').strip()
    if not prenom or not plat or not vin or not experience:
        return jsonify({'error': 'Tous les champs sont obligatoires.'}), 400
    try:
        send_email(
            subject=f'[Vin/20] Nouvelle contribution \u2014 {plat}',
            body=(
                f'Nouvelle contribution Vin/20\n{"="*40}\n\n'
                f'Pr\u00e9nom     : {prenom}\n'
                f'Plat       : {plat}\n'
                f'Vin        : {vin}\n\n'
                f'Exp\u00e9rience :\n{experience}\n'
            )
        )
        return jsonify({'ok': True})
    except Exception as e:
        print(f'Erreur contribution : {e}')
        return jsonify({'error': 'Impossible d envoyer l email.'}), 500

@app.route('/suggestion', methods=['POST'])
def suggestion():
    body   = request.get_json(force=True)
    prenom = body.get('prenom', '').strip()
    nom    = body.get('nom', '').strip()
    email  = body.get('email', '').strip()
    plat   = body.get('plat', '').strip()
    if not prenom or not nom or not email or not plat:
        return jsonify({'error': 'Tous les champs sont obligatoires.'}), 400
    try:
        send_email(
            subject=f'[Vin/20] Suggestion de plat \u2014 {plat}',
            body=(
                f'Demande d\u2019ajout de plat\n{"="*40}\n\n'
                f'Pr\u00e9nom : {prenom}\n'
                f'Nom    : {nom}\n'
                f'Email  : {email}\n\n'
                f'Plat demand\u00e9 : {plat}\n'
            )
        )
        return jsonify({'ok': True})
    except Exception as e:
        print(f'Erreur suggestion : {e}')
        return jsonify({'error': 'Impossible d envoyer l email.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
