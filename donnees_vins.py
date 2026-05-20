# donnees_vins.py

# Base de données couleurs -> types de vins (EN ANGLAIS pour Spoonacular API)
BASE_COULEURS = {
    # Aliments rouges -> vins rouges tanniques
    "rouge": {
        "ingredients": [
            # Viandes rouges
            "beef", "steak", "ribeye", "sirloin", "brisket", "short ribs", "beef broth", "beef stock",
            "lamb", "mutton", "venison", "deer", "elk", "boar", "wild boar",
            "duck", "duck breast", "goose", "game", "quail", "pigeon",
            # Charcuteries
            "chorizo", "salami", "pepperoni", "prosciutto", "pancetta",
            "bacon", "applewood bacon", "smoked bacon", "sausage", "andouille", "bresaola", "coppa",
            # Autres
            "red meat", "beef liver", "kidney", "blood sausage", "red wine", "wine"
        ],
        "vins_recommandes": ["Bordeaux rouge", "Côtes du Rhône", "Cahors", "Madiran", "Barolo", "Chianti", "Malbec"]
    },
    
    # Aliments blancs -> vins blancs secs
    "blanc": {
        "ingredients": [
            # Viandes blanches
            "chicken", "chicken breast", "chicken broth", "chicken stock", "turkey", "pork", "pork chop", "pork loin",
            "veal", "rabbit", "pheasant", "guinea fowl",
            # Poissons blancs
            "cod", "haddock", "halibut", "sea bass", "sole", "turbot", "monkfish",
            "tilapia", "snapper", "grouper", "hake", "pollock", "whiting", "white fish",
            # Fruits de mer
            "scallops", "lobster", "crab", "clams", "oysters", "mussels",
            "calamari", "squid", "octopus",
            # Fromages blancs
            "mozzarella", "burrata", "ricotta", "feta", "goat cheese", "chèvre",
            "cream cheese", "mascarpone", "cottage cheese", "white cheese",
            # Légumes blancs
            "cauliflower", "white beans", "cannellini beans", "navy beans",
            "white mushrooms", "button mushrooms", "fennel", "leeks", "onions", "white onions",
            "garlic", "shallots", "parsnips", "turnips", "potatoes", "white potato",
            # Autres
            "cream", "heavy cream", "milk", "butter", "white sauce", "béchamel",
            "egg whites", "tofu"
        ],
        "vins_recommandes": ["Chablis", "Sancerre", "Muscadet", "Pinot Grigio", "Albariño", "Soave", "Verdicchio"]
    },
    
    # Aliments verts -> vins blancs frais/minéraux
    "vert": {
        "ingredients": [
            # Légumes verts
            "spinach", "kale", "arugula", "rocket", "lettuce", "romaine", "watercress", "mesclun",
            "zucchini", "courgette", "green beans", "snap peas", "peas", "edamame", "snow peas",
            "asparagus", "broccoli", "brussels sprouts", "green cabbage", "bok choy", "chinese cabbage",
            "cucumber", "celery", "avocado", "green peppers", "bell pepper", "green bell pepper",
            "artichokes", "green olives", "okra", "green chilies",
            # Herbes
            "basil", "parsley", "cilantro", "coriander", "mint", "dill", "tarragon",
            "chives", "oregano", "thyme", "rosemary", "sage", "bay leaves", "bay leaf",
            "green onions", "scallions", "spring onions",
            # Autres
            "capers", "pesto", "green salad", "green lentils", "lime", "green apple"
        ],
        "vins_recommandes": ["Sauvignon Blanc", "Vermentino", "Vinho Verde", "Riesling sec", "Grüner Veltliner"]
    },
    
    # Aliments dorés/jaunes -> vins blancs évolués/riches
    "dore": {
        "ingredients": [
            # Foie gras et terrines
            "foie gras", "pâté", "terrine", "duck liver", "liver",
            # Fromages affinés
            "comté", "gruyère", "parmesan", "aged cheese", "cheddar", "parmigiano",
            "gouda", "manchego", "pecorino", "emmental", "swiss cheese",
            # Plats gratinés
            "gratin", "au gratin", "gratin dauphinois", "mac and cheese", "macaroni and cheese",
            "quiche", "soufflé", "cheese sauce", "cheese",
            # Fruits dorés
            "peach", "apricot", "mango", "pineapple", "golden apple", "yellow apple",
            "lemon", "orange", "grapefruit",
            # Légumes dorés
            "corn", "yellow corn", "sweet corn", "polenta", "butternut squash",
            "sweet potato", "yams", "pumpkin", "yellow peppers", "yellow bell pepper",
            "golden beets", "yellow squash",
            # Épices dorées
            "saffron", "turmeric", "curry", "curry powder", "mustard", "honey",
            # Autres
            "eggs", "egg yolk", "egg", "mayonnaise", "hollandaise"
        ],
        "vins_recommandes": ["Chardonnay", "Gewurztraminer", "Chenin Blanc", "Viognier", "White Burgundy"]
    },
    
    # Aliments rosés -> vins rosés
    "rose": {
        "ingredients": [
            # Poissons rosés
            "salmon", "smoked salmon", "pink salmon", "sockeye salmon", "coho salmon",
            "trout", "sea trout", "rainbow trout", "tuna", "tuna steak", "red mullet",
            # Crustacés
            "shrimp", "prawns", "langoustine", "pink prawns", "crayfish", "pink shrimp",
            # Charcuteries rosées
            "ham", "cooked ham", "prosciutto cotto", "mortadella", "canadian bacon",
            # Légumes/fruits rosés
            "pink grapefruit", "radish", "pink onion", "red onion", "beets", "beetroot", "rhubarb",
            "tomatoes", "tomato", "cherry tomatoes", "tomato sauce", "marinara",
            "red peppers", "red bell pepper", "roasted red peppers",
            # Autres
            "provençal", "mediterranean", "nicoise", "rose water"
        ],
        "vins_recommandes": ["Provence rosé", "Tavel", "Bandol rosé", "Rosé de Loire", "Côtes de Provence"]
    },
    
    # Aliments bruns/foncés -> vins rouges puissants
    "brun": {
        "ingredients": [
            # Champignons
            "mushrooms", "cremini mushrooms", "baby bella", "porcini", "shiitake", "portobello",
            "oyster mushrooms", "chanterelles", "truffle", "black truffle", "morel", "dried mushrooms",
            # Plats mijotés
            "stew", "braised", "pot roast", "beef bourguignon", "osso buco", "casserole",
            "short ribs", "oxtail", "daube", "roast", "roasted", "slow cooked",
            # Légumineuses
            "lentils", "brown lentils", "black beans", "black lentils", "kidney beans",
            # Autres
            "dark chocolate", "cocoa", "coffee", "espresso", "balsamic", "balsamic vinegar",
            "soy sauce", "worcestershire", "miso", "brown sugar", "molasses",
            "walnuts", "pecans", "chestnuts", "hazelnuts"
        ],
        "vins_recommandes": ["Châteauneuf-du-Pape", "Amarone", "Brunello", "Hermitage", "Priorat"]
    },
    
    # Aliments épicés -> vins adaptés
    "epice": {
        "ingredients": [
            # Épices et piments
            "chili", "chili powder", "jalapeño", "serrano", "habanero", "cayenne", "cayenne pepper",
            "paprika", "hot sauce", "tabasco", "sriracha", "red pepper flakes", "crushed red pepper",
            "curry", "curry paste", "ginger", "fresh ginger", "wasabi", "horseradish",
            "mustard", "dijon mustard", "pepper", "black pepper", "white pepper",
            "peppercorns", "chipotle", "ancho", "poblano",
            # Styles de cuisine
            "spicy", "spiced", "cajun", "creole", "mexican", "indian", "thai",
            "szechuan", "korean", "hot", "picante"
        ],
        "vins_recommandes": ["Gewurztraminer", "Riesling demi-sec", "Viognier", "Grenache rosé", "Beaujolais"]
    },
    
    # Pâtes et féculents -> selon la sauce
    "pates": {
        "ingredients": [
            # Pâtes
            "pasta", "spaghetti", "penne", "linguine", "fettuccine", "rigatoni", "fusilli",
            "macaroni", "lasagna", "ravioli", "tortellini", "gnocchi", "tagliatelle",
            "angel hair", "capellini", "orzo", "farfalle", "bow tie pasta",
            # Autres féculents
            "noodles", "rice", "risotto", "arborio rice", "basmati", "jasmine rice",
            "couscous", "quinoa", "bulgur", "farro", "barley", "bread", "breadcrumbs"
        ],
        "vins_recommandes": ["Dépend de la sauce - Chianti pour tomate, Pinot Grigio pour crème"]
    },
    
    # Assaisonnements et bases (neutres)
    "neutre": {
        "ingredients": [
            # Assaisonnements
            "salt", "kosher salt", "sea salt", "pepper", "salt and pepper",
            "olive oil", "vegetable oil", "canola oil", "oil",
            "vinegar", "red wine vinegar", "white wine vinegar", "apple cider vinegar",
            "flour", "all-purpose flour", "cornstarch", "sugar", "brown sugar",
            # Bouillons
            "broth", "stock", "vegetable broth", "vegetable stock",
            "water", "ice", "ice cubes"
        ],
        "vins_recommandes": ["Dépend du plat principal"]
    }
}

BASE_PLATS = {

    # === VIANDES & PLATS TRADITIONNELS ===
    "magret de canard": {
        "vins_recommandes": ["Bordeaux rouge", "Pécharmant"]
    },
    "confit de canard": {
        "vins_recommandes": ["Cahors", "Irouléguy"]
    },
    "côte de bœuf": {
        "vins_recommandes": ["Côtes-du-Rhône", "Margaux", "Saint-Julien"]
    },
    "steak frites": {
        "vins_recommandes": ["Beaujolais", "Saumur-Champigny", "Côtes-de-Bourg"]
    },
    "bœuf bourguignon": {
        "vins_recommandes": ["Bourgogne rouge", "Mercurey", "Gigondas"]
    },
    "pot-au-feu": {
        "vins_recommandes": ["Chinon", "Bourgueil"]
    },
    "gigot d’agneau de 4 heures": {
        "vins_recommandes": ["Médoc", "Côte-Rôtie"]
    },
    "tajine d’agneau": {
        "vins_recommandes": ["Coteaux-du-Languedoc rouge", "Beaumes-de-Venise rouge"]
    },
    "lapin à la moutarde": {
        "vins_recommandes": ["Chinon", "Bourgueil"]
    },
    "osso-buco": {
        "vins_recommandes": ["Bandol rouge", "Montepulciano"]
    },
    "filet mignon de porc": {
        "vins_recommandes": ["Saint-Émilion", "Pomerol"]
    },
    "escalope de veau à la milanaise": {
        "vins_recommandes": ["Chinon", "Saint-Nicolas-de-Bourgueil"]
    },
    "blanquette de veau": {
        "vins_recommandes": ["Mâconnais blanc", "Limoux blanc"]
    },
    "hachis parmentier": {
        "vins_recommandes": ["Sancerre rouge", "Beaujolais"]
    },
    "cassoulet": {
        "vins_recommandes": ["Madiran", "Bergerac", "Cahors"]
    },
    "chili con carne": {
        "vins_recommandes": ["Fronton", "Saint-Chinian"]
    },

    # === VOLAILLES ===
    "poulet rôti": {
        "vins_recommandes": ["Bourgogne rouge", "Tavel rosé"]
    },
    "curry de poulet": {
        "vins_recommandes": ["Vin jaune", "Coteaux-du-Layon", "Condrieu"]
    },
    "dinde farcie": {
        "vins_recommandes": ["Châteauneuf-du-Pape blanc", "Gevrey-Chambertin"]
    },

    # === POISSONS & MER ===
    "pavé de saumon grillé": {
        "vins_recommandes": ["Riesling", "Chablis"]
    },
    "moules-frites": {
        "vins_recommandes": ["Muscadet", "Entre-deux-Mers"]
    },
    "sushis": {
        "vins_recommandes": ["Sauvignon", "Sancerre rosé", "Entre-deux-Mers"]
    },
    "brandade de morue": {
        "vins_recommandes": ["Blanc de Provence", "Blanc de Corse"]
    },
    "bouillabaisse": {
        "vins_recommandes": ["Provence blanc", "Bandol rosé"]
    },

    # === PÂTES, RIZ & FÉCULENTS ===
    "lasagnes à la bolognaise": {
        "vins_recommandes": ["Bandol", "Patrimonio rouge"]
    },
    "spaghettis à la bolognaise": {
        "vins_recommandes": ["Côtes-du-Rhône-Villages"]
    },

    "tagliatelles à la carbonara": {
        "vins_recommandes": ["Sauvignon", "Saint-Véran", "Pinot gris", "Pinot Grigio", "Dolcetto", "Franciacorta"]
    },

    "spaghettis à la carbonara" : {
        "vins_recommandes" : ["Pinot Grigio", "Dolcetto", "Franciacorta"]
    },

    "risotto aux champignons": {
        "vins_recommandes": ["Chablis grand cru", "Côte-de-Beaune blanc","Bourgogne Pinot Noir"]
    },

    "gratin dauphinois": {
        "vins_recommandes": ["Côtes-du-Rhône blanc", "Arbois rouge"]
    },

    # === PLATS VÉGÉTARIENS & SIMPLES ===
    "ratatouille": {
        "vins_recommandes": ["Costières-de-Nîmes", "Rosé de Provence", "Côtes-du-Rhône"]
    },
    "tomates farcies": {
        "vins_recommandes": ["Côtes-du-Rhône-Villages", "Côtes-de-Provence rosé"]
    },
    "omelette": {
        "vins_recommandes": ["Jasnières", "Anjou blanc", "Chignin-Bergeron"]
    },
    "soupe à l’oignon gratinée": {
        "vins_recommandes": ["Coteaux-du-Lyonnais blanc", "Arbois blanc", "Xérès"]
    },

    # === OEUFS ===

    "oeufs bénedicte": {
        "vins_recommandes": ["Champagne Rosé","Blanc de Blancs Champagne"]
    },

    "oeufs brouillés": {
        "vins_recommandes": ["Champagne","Blanc de Blancs Champagne","Cava"]
    },

    "omelette": {
        "vins_recommandes": ["Champagne","Crémant de Bourgogne"]
    },

    # === FROMAGES & PLATS AU FROMAGE ===
    "raclette": {
        "vins_recommandes": ["Savagnin du Jura", "Roussette-de-Savoie"]
    },
    "tartiflette": {
        "vins_recommandes": ["Savoie blanc", "Côtes-du-Rhône blanc"]
    },
    "fondue bourguignonne": {
        "vins_recommandes": ["Bourgogne rouge"]
    },
    "croque-monsieur": {
        "vins_recommandes": ["Beaujolais", "Bourgueil", "Chardonnay"]
    },

    "fish and chips" : {
        "vins_recommandes" : ["Chablis", "Loire Chenin Blanc"]
    }, 

    "soufflé au fromage": {
        "vins_recommandes": ["Saint-Véran", "Rully blanc"]
    },
    "escargots à l’ail": {
        "vins_recommandes": ["Bourgogne aligoté", "Mâcon blanc", "Chardonnay du Jura"]
    },

    # === PLATS DU MONDE & DIVERS ===
    "paella": {
        "vins_recommandes": ["Rioja", "Côtes-du-Roussillon rouge"]
    },
    "couscous": {
        "vins_recommandes": ["Vins du Maghreb", "Costières-de-Nîmes", "Languedoc", "Tavel rosé"]
    },
    "pizza margherita": {
        "vins_recommandes": ["Côtes-de-Provence rosé", "Gigondas"]
    },
    "hamburger": {
        "vins_recommandes": ["Saint-Joseph", "Pic-Saint-Loup", "Blaye-Côtes-de-Bordeaux"]
    },
    "galette jambon-fromage": {
        "vins_recommandes": ["Crémant", "Rosé d’Anjou"]
    },
    "jambon pâtes": {
        "vins_recommandes": ["Saint-Pourçain", "Beaujolais", "Gamay de Loire"]
    },
    "choucroute": {
        "vins_recommandes": ["Pinot blanc", "Riesling"]
    },

    "mafe au poulet" : {
        "vins_recommandes" : ["Loire Chenin Blanc", "Meursault"]
    },

    # === PLATS D’EXCEPTION ===
    "tartare de bœuf": {
        "vins_recommandes": ["Morgon", "Moulin-à-Vent", "Vacqueyras", "Lussac-Saint-Émilion"]
    },
    "foie gras de canard": {
        "vins_recommandes": ["Pinot gris vendanges tardives", "Jurançon moelleux"]
    },

    # === APERITIF ===
    "charcuterie" : {
        "vins_recommandes" : ["Dolcetto","Morgon","Lambrusco Rouge (effervescent)"]
    },

    " rillettes au saumon " : {
        "vins_recommandes" : ["Chablis", "Loire Chenin Blanc (Touraine, Anjou, Coteaux du Layon)"]
    },

    "rillettes au lapin" : {
        "vins_recommandes" : ["Bourgogne Chardonnay", "Loire Chenin Blanc (Touraine, Anjou, Coteaux du Layon)"]
    },

    "rillettes au porc" : {
        "vins_recommandes" : ["Beaujolais (Fleurie, Juliénas, Saint-Amour)"]
    },

    "petit fours" : {
        "vins_recommandes" : ["Champagne Demi-sec","Bonnezeaux","Sauternes"]
    },
    

    # === DESSERT ===

    "tarte au pomme" : {
        "vins_recommandes" : ["Bonnezeaux"]
    },

    "tarte tatin" : {
        "vins_recommandes" : ["Bonnezeaux"]
    },

    "tarte citron meringué" : {
        "vins_recommandes" : ["Bonnezeaux"]
    },

    "marbré au chocolat" : {
        "vins_recommandes" : ["Porto Ruby"]
    },

    "gâteau au chocolat" : {
        "vins_recommandes" : ["Porto Ruby"]
    },

    "gâteau aux prunes" : {
        "vins_recommandes" : ["Porto Ruby"]
    },

    "Profiteroles" : {
        "vins_recommandes" : ["Porto Ruby"]
    },

    "tarte aux myrtilles" : {
        "vins_recommandes" : ["Porto Ruby"]
    },

    "gâteau au chocolat et aux framboises" : {
        "vins_recommandes" : ["Porto Ruby"]
    },
   
    "éclair au chocolat" : {
        "vins_recommandes" : ["Porto Ruby"]
    },

    "baba au rhum" : {
        "vins_recommandes" : ["Porto Tawny"]
    },

    "baba au rhum" : {
        "vins_recommandes" : ["Porto Tawny"]
    },

    "glace au café" : {
        "vins_recommandes" : ["Porto Tawny"]
    },

    "brownies au caramel beurre salé" : {
        "vins_recommandes" : ["Porto Tawny"]
    },

    "cookies au pépites de chocolat" : {
        "vins_recommandes" : ["Porto Tawny"]
    },

    "figues" : {
        "vins_recommandes" : ["Porto Tawny"]
    },
}   