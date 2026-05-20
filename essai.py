import numpy as np 

from collections import Counter
from donnees_vins import BASE_COULEURS, BASE_PLATS


def recommander_vin(nom_plat,ingredients = None):

    nom_plat = nom_plat.lower()

    if not nom_plat :
        return {
            "erreur",
            "nom de plat vide"
        }
    
    if nom_plat in BASE_PLATS :
        return {
            "source" : "base_plats",
            "plat" : nom_plat,
            "vins" : BASE_PLATS[nom_plat]["vins_recommandes"]
        }
    
    if ingredients : 
        recommendation = recommander_vin_plat(ingredients)
        if isinstance(recommendation, dict) and "vins" in recommendation:
            recommendation["source"] = "ingredients"
            recommendation["plat"] = nom_plat
            return recommendation
    
    return {
        "source" : "indéterminée",
        "plat" : nom_plat,
        "message" : "plat inconnu et ingrédients insuffisants"
    }



def detecter_couleur_ingredient(ingredient):
    ingredient = ingredient.lower() # met en minuscule

    for couleur, data in BASE_COULEURS.items():
        for item in data['ingredients']:
            if item in ingredient : 
                return couleur
    return None

def recommander_couleur_vin(plat):
    plat = plat.lower()

    couleur_trouvee = detecter_couleur_ingredient(plat)
    
    if couleur_trouvee:
        vins = BASE_COULEURS[couleur_trouvee]["vins_recommandes"]
        return f"Couleur détectée {couleur_trouvee} -> {', '.join(vins[:3])}"
    else : 
        return 'ingrédient non reconnue'
    

def recommander_vin_plat(ingredients):
    """ Prends une liste d'ingrédient et retourne une recommendation de vins"""


    #REGLES PRIORITAIRES
    ingredients_lower = [ing.lower() for ing in ingredients]
    plat_complet = ' '.join(ingredients_lower)
    
    # Sauce tomate = vin rouge léger
    if any(x in plat_complet for x in ['tomato', 'marinara', 'pomodoro']):
        return {
            "ATTENTION Y'A DU ROUGE"
            "couleur_dominante": "rouge",
            "vins": ["Chianti", "Sangiovese", "Barbera"],
            "raison": "Détecté: sauce tomate"
        }
    
    #Rajouter d'autres règles principales


    couleurs_ponderees = []

    for ingredient in ingredients:
        couleur = detecter_couleur_ingredient(ingredient)
        
        if couleur == "neutre" or not couleur:
            continue

        poids = 1


        # Crème + Beurre
        if any(x in ingredient.lower() for x in ['cream','butter']):
            poids = 3

        # Viandes blanches = poids moyen
        elif any(x in ingredient.lower() for x in ['chicken', 'turkey', 'pork', 'veal', 'rabbit']):
            poids = 2

        
        # Poissons = poids moyen
        elif any(x in ingredient.lower() for x in ["salmon", "smoked salmon", "pink salmon", "sockeye salmon", "coho salmon",
            "trout", "sea trout", "rainbow trout", "tuna", "tuna steak", "red mullet","shrimp", "prawns", "langoustine", "pink prawns",
            "crayfish", "pink shrimp"]):
            poids = 2

        
        # Viandes rouges
        elif any(x in ingredient.lower() for x in ["beef", "steak", "ribeye", "sirloin", "brisket", "short ribs", "beef broth", "beef stock",
        "lamb", "mutton", "venison", "deer", "elk", "boar", "wild boar",
        "duck", "duck breast", "goose", "game", "quail", "pigeon","chorizo", "salami", "pepperoni", "prosciutto", "pancetta",
        "bacon", "applewood bacon", "smoked bacon", "sausage", "andouille", "bresaola", "coppa","red meat", "beef liver", "kidney"]):
            poids = 3

    
        elif couleur == "pates":
            poids = 0.5
        
        # Ajouter la couleur plusieurs fois selon le poids
        for _ in range(int(poids * 2)):  # Multiplier par 2 pour avoir des entiers
            couleurs_ponderees.append(couleur)

    if not couleurs_ponderees:
        return "Impossible de déterminer un vin adapté"
    

    compteur = Counter(couleurs_ponderees)
    couleur_dominante = compteur.most_common(1)[0][0]
    
    # Si c'est "pates", regarder la deuxième couleur
    if couleur_dominante == "pates" and len(compteur) > 1:
        couleur_dominante = compteur.most_common(2)[1][0]

    vins = BASE_COULEURS[couleur_dominante]["vins_recommandes"]

    
    return {
        "couleur_dominante": couleur_dominante,
        "vins": vins[:3],
        "debug": dict(compteur)  # Pour voir le comptage
    }
    