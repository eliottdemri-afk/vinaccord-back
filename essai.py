import numpy as np
from collections import Counter
from donnees_vins import BASE_COULEURS, BASE_PLATS

def recommander_vin(nom_plat, ingredients=None):
    nom_plat = nom_plat.lower().strip()
    if not nom_plat:
        return {"erreur": "nom de plat vide"}

    if nom_plat in BASE_PLATS:
        return {
            "source": "base_plats",
            "plat": nom_plat,
            "vins": BASE_PLATS[nom_plat]["vins_recommandes"]
        }

    if ingredients:
        recommendation = recommander_vin_plat(ingredients)
        if isinstance(recommendation, dict) and "vins" in recommendation:
            recommendation["source"] = "ingredients"
            recommendation["plat"] = nom_plat
            return recommendation

    return {
        "source": "indéterminée",
        "plat": nom_plat,
        "message": "plat inconnu et ingrédients insuffisants"
    }


def detecter_couleur_ingredient(ingredient):
    ingredient = ingredient.lower()
    for couleur, data in BASE_COULEURS.items():
        for item in data["ingredients"]:
            if item in ingredient:
                return couleur
    return None


def recommander_vin_plat(ingredients):
    """Prend une liste d'ingrédients (FR ou EN) et retourne une recommandation de vins."""
    ingredients_lower = [ing.lower() for ing in ingredients]
    plat_complet = " ".join(ingredients_lower)

    # Règles prioritaires
    if any(x in plat_complet for x in ["tomato", "marinara", "pomodoro", "tomate", "coulis de tomate"]):
        return {
            "couleur_dominante": "rouge",
            "vins": ["Chianti", "Sangiovese", "Barbera"],
            "raison": "Détecté: sauce tomate"
        }

    couleurs_ponderees = []

    for ingredient in ingredients:
        couleur = detecter_couleur_ingredient(ingredient)
        if couleur == "neutre" or not couleur:
            continue

        poids = 1
        ing = ingredient.lower()

        # Crème + Beurre (FR + EN)
        if any(x in ing for x in ["cream", "butter", "crème", "beurre"]):
            poids = 3
        # Viandes blanches (FR + EN)
        elif any(x in ing for x in ["chicken", "turkey", "pork", "veal", "rabbit",
                                     "poulet", "dinde", "porc", "veau", "lapin"]):
            poids = 2
        # Poissons rosés (FR + EN)
        elif any(x in ing for x in ["salmon", "trout", "tuna", "shrimp", "prawns", "langoustine",
                                     "saumon", "truite", "thon", "crevette", "gambas"]):
            poids = 2
        # Viandes rouges (FR + EN)
        elif any(x in ing for x in ["beef", "steak", "lamb", "mutton", "venison", "duck", "goose",
                                     "chorizo", "bacon", "sausage",
                                     "bœuf", "agneau", "mouton", "canard", "oie", "gibier",
                                     "saucisse", "lardons"]):
            poids = 3
        elif couleur == "pates":
            poids = 0.5

        for _ in range(int(poids * 2)):
            couleurs_ponderees.append(couleur)

    if not couleurs_ponderees:
        return {"erreur": "Impossible de déterminer un vin adapté"}

    compteur = Counter(couleurs_ponderees)
    couleur_dominante = compteur.most_common(1)[0][0]

    if couleur_dominante == "pates" and len(compteur) > 1:
        couleur_dominante = compteur.most_common(2)[1][0]

    vins = BASE_COULEURS[couleur_dominante]["vins_recommandes"]
    return {
        "couleur_dominante": couleur_dominante,
        "vins": vins[:3],
        "debug": dict(compteur)
    }
