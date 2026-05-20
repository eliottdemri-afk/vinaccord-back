# donnees_vins.py

BASE_COULEURS = {
    "rouge": {
        "ingredients": [
            # EN - Viandes rouges
            "beef", "steak", "ribeye", "sirloin", "brisket", "short ribs", "beef broth", "beef stock",
            "lamb", "mutton", "venison", "deer", "elk", "boar", "wild boar",
            "duck", "duck breast", "goose", "game", "quail", "pigeon",
            "chorizo", "salami", "pepperoni", "prosciutto", "pancetta",
            "bacon", "sausage", "andouille", "bresaola", "coppa",
            "red wine", "wine",
            # FR - Viandes rouges
            "boeuf", "bœuf", "agneau", "mouton", "chevreuil", "sanglier",
            "canard", "oie", "gibier", "caille", "pigeonneau",
            "chorizo", "lardons", "saucisse", "boudin",
            "vin rouge",
        ],
        "vins_recommandes": ["Bordeaux rouge", "Côtes du Rhône", "Cahors", "Madiran", "Barolo", "Chianti", "Malbec"]
    },

    "blanc": {
        "ingredients": [
            # EN - Viandes blanches
            "chicken", "chicken breast", "chicken broth", "turkey", "pork", "pork chop", "pork loin",
            "veal", "rabbit", "pheasant", "guinea fowl",
            # EN - Poissons blancs
            "cod", "haddock", "halibut", "sea bass", "sole", "turbot", "monkfish",
            "tilapia", "snapper", "hake", "whiting", "white fish",
            # EN - Fruits de mer
            "scallops", "lobster", "crab", "clams", "oysters", "mussels", "calamari", "squid", "octopus",
            # EN - Fromages blancs
            "mozzarella", "burrata", "ricotta", "feta", "goat cheese",
            "cream cheese", "mascarpone", "cottage cheese",
            # EN - Légumes blancs
            "cauliflower", "white beans", "fennel", "leeks", "onions", "garlic",
            "potatoes", "cream", "butter", "milk", "tofu",
            # FR - Viandes blanches
            "poulet", "dinde", "porc", "côte de porc", "veau", "lapin", "faisan",
            # FR - Poissons blancs
            "cabillaud", "merlu", "sole", "bar", "turbot", "lotte", "lieu", "merlan",
            # FR - Fruits de mer
            "noix de saint-jacques", "homard", "crabe", "palourdes", "huîtres", "moules",
            "calamar", "seiche", "poulpe",
            # FR - Fromages blancs
            "chèvre", "fromage blanc", "ricotta", "feta",
            # FR - Légumes blancs
            "chou-fleur", "haricots blancs", "fenouil", "poireaux", "oignons", "ail",
            "pommes de terre", "crème", "beurre", "lait",
        ],
        "vins_recommandes": ["Chablis", "Sancerre", "Muscadet", "Pinot Grigio", "Albariño", "Soave", "Verdicchio"]
    },

    "vert": {
        "ingredients": [
            # EN
            "spinach", "kale", "arugula", "lettuce", "zucchini", "green beans", "peas",
            "asparagus", "broccoli", "cucumber", "avocado", "green peppers", "artichokes",
            "basil", "parsley", "cilantro", "mint", "dill", "thyme", "rosemary", "sage",
            "capers", "pesto", "lime", "green apple",
            # FR
            "épinards", "roquette", "laitue", "courgette", "haricots verts", "petits pois",
            "asperges", "brocoli", "concombre", "avocat", "poivron vert", "artichauts",
            "basilic", "persil", "coriandre", "menthe", "aneth", "thym", "romarin", "sauge",
            "câpres", "citron vert", "pomme verte",
        ],
        "vins_recommandes": ["Sauvignon Blanc", "Vermentino", "Vinho Verde", "Riesling sec", "Grüner Veltliner"]
    },

    "dore": {
        "ingredients": [
            # EN
            "foie gras", "pâté", "terrine", "liver",
            "parmesan", "aged cheese", "cheddar", "gouda", "manchego", "emmental",
            "gratin", "quiche", "soufflé", "cheese",
            "peach", "apricot", "mango", "pineapple", "lemon", "orange",
            "corn", "sweet potato", "pumpkin", "saffron", "turmeric", "curry", "honey",
            "eggs", "egg yolk", "mayonnaise",
            # FR
            "foie gras", "pâté", "terrine", "foie",
            "parmesan", "comté", "gruyère", "fromage affiné", "cheddar", "gouda",
            "gratin", "quiche", "soufflé", "fromage",
            "pêche", "abricot", "mangue", "ananas", "citron", "orange",
            "maïs", "patate douce", "potiron", "safran", "curcuma", "curry", "miel",
            "oeufs", "oeuf", "jaune d'oeuf", "mayonnaise",
        ],
        "vins_recommandes": ["Chardonnay", "Gewurztraminer", "Chenin Blanc", "Viognier", "White Burgundy"]
    },

    "rose": {
        "ingredients": [
            # EN
            "salmon", "smoked salmon", "trout", "tuna", "red mullet",
            "shrimp", "prawns", "langoustine", "crayfish",
            "ham", "cooked ham", "mortadella",
            "radish", "beets", "tomatoes", "tomato", "cherry tomatoes", "tomato sauce", "marinara",
            "red peppers", "red bell pepper",
            # FR
            "saumon", "saumon fumé", "truite", "thon", "rouget",
            "crevettes", "gambas", "langoustine", "écrevisse",
            "jambon", "jambon cuit", "mortadelle",
            "radis", "betterave", "tomates", "tomate", "tomates cerises", "sauce tomate",
            "poivron rouge",
        ],
        "vins_recommandes": ["Provence rosé", "Tavel", "Bandol rosé", "Rosé de Loire", "Côtes de Provence"]
    },

    "brun": {
        "ingredients": [
            # EN
            "mushrooms", "porcini", "shiitake", "portobello", "truffle", "chanterelles", "morel",
            "stew", "braised", "pot roast", "casserole", "oxtail", "roasted",
            "lentils", "black beans", "kidney beans",
            "dark chocolate", "cocoa", "coffee", "balsamic", "soy sauce", "miso",
            "walnuts", "chestnuts", "hazelnuts",
            # FR
            "champignons", "cèpes", "shiitake", "portobello", "truffe", "girolles", "morilles",
            "mijoté", "braisé", "daube", "pot-au-feu",
            "lentilles", "haricots noirs",
            "chocolat noir", "cacao", "café", "vinaigre balsamique",
            "noix", "châtaignes", "noisettes",
        ],
        "vins_recommandes": ["Châteauneuf-du-Pape", "Amarone", "Brunello", "Hermitage", "Priorat"]
    },

    "epice": {
        "ingredients": [
            # EN
            "chili", "jalapeño", "cayenne", "paprika", "hot sauce", "sriracha",
            "curry", "ginger", "wasabi", "horseradish", "pepper",
            "spicy", "cajun", "mexican", "thai",
            # FR
            "piment", "piment fort", "paprika", "sauce piquante",
            "curry", "gingembre", "raifort", "poivre",
            "épicé", "relevé", "mexicain", "thaï", "indien",
        ],
        "vins_recommandes": ["Gewurztraminer", "Riesling demi-sec", "Viognier", "Grenache rosé", "Beaujolais"]
    },

    "pates": {
        "ingredients": [
            # EN
            "pasta", "spaghetti", "penne", "linguine", "fettuccine", "rigatoni", "fusilli",
            "macaroni", "lasagna", "ravioli", "tortellini", "gnocchi", "tagliatelle",
            "noodles", "rice", "risotto", "couscous", "quinoa", "barley",
            # FR
            "pâtes", "spaghettis", "penne", "linguines", "tagliatelles", "lasagnes",
            "raviolis", "tortellinis", "gnocchis",
            "nouilles", "riz", "risotto", "couscous", "quinoa", "orge",
        ],
        "vins_recommandes": ["Dépend de la sauce — Chianti pour tomate, Pinot Grigio pour crème"]
    },

    "neutre": {
        "ingredients": [
            # EN
            "salt", "pepper", "olive oil", "vegetable oil", "oil",
            "vinegar", "flour", "sugar", "broth", "stock", "water",
            # FR
            "sel", "poivre", "huile d'olive", "huile", "vinaigre",
            "farine", "sucre", "bouillon", "eau",
        ],
        "vins_recommandes": ["Dépend du plat principal"]
    }
}


BASE_PLATS = {

    # === VIANDES & PLATS TRADITIONNELS ===
    "magret de canard": {"vins_recommandes": ["Bordeaux rouge", "Pécharmant"]},
    "confit de canard": {"vins_recommandes": ["Cahors", "Irouléguy"]},
    "côte de bœuf": {"vins_recommandes": ["Côtes-du-Rhône", "Margaux", "Saint-Julien"]},
    "steak frites": {"vins_recommandes": ["Beaujolais", "Saumur-Champigny", "Côtes-de-Bourg"]},
    "bœuf bourguignon": {"vins_recommandes": ["Bourgogne rouge", "Mercurey", "Gigondas"]},
    "pot-au-feu": {"vins_recommandes": ["Chinon", "Bourgueil"]},
    "gigot d'agneau de 4 heures": {"vins_recommandes": ["Médoc", "Côte-Rôtie"]},
    "gigot d'agneau": {"vins_recommandes": ["Médoc", "Côte-Rôtie"]},
    "tajine d'agneau": {"vins_recommandes": ["Coteaux-du-Languedoc rouge", "Beaumes-de-Venise rouge"]},
    "tajine de poulet": {"vins_recommandes": ["Coteaux-du-Languedoc blanc", "Condrieu"]},
    "lapin à la moutarde": {"vins_recommandes": ["Chinon", "Bourgueil"]},
    "osso-buco": {"vins_recommandes": ["Bandol rouge", "Montepulciano"]},
    "filet mignon de porc": {"vins_recommandes": ["Saint-Émilion", "Pomerol"]},
    "escalope de veau à la milanaise": {"vins_recommandes": ["Chinon", "Saint-Nicolas-de-Bourgueil"]},
    "blanquette de veau": {"vins_recommandes": ["Mâconnais blanc", "Limoux blanc"]},
    "hachis parmentier": {"vins_recommandes": ["Sancerre rouge", "Beaujolais"]},
    "cassoulet": {"vins_recommandes": ["Madiran", "Bergerac", "Cahors"]},
    "chili con carne": {"vins_recommandes": ["Fronton", "Saint-Chinian"]},
    "tartare de bœuf": {"vins_recommandes": ["Morgon", "Moulin-à-Vent", "Vacqueyras"]},
    "côtes d'agneau": {"vins_recommandes": ["Côte-Rôtie", "Saint-Joseph rouge"]},

    # === VOLAILLES ===
    "poulet rôti": {"vins_recommandes": ["Bourgogne rouge", "Tavel rosé"]},
    "poulet basquaise": {"vins_recommandes": ["Irouléguy rouge", "Côtes-du-Roussillon"]},
    "poulet à la crème": {"vins_recommandes": ["Mâcon blanc", "Pouilly-Fuissé"]},
    "curry de poulet": {"vins_recommandes": ["Vin jaune", "Coteaux-du-Layon", "Condrieu"]},
    "dinde farcie": {"vins_recommandes": ["Châteauneuf-du-Pape blanc", "Gevrey-Chambertin"]},

    # === POISSONS & MER ===
    "pavé de saumon grillé": {"vins_recommandes": ["Riesling", "Chablis"]},
    "saumon en papillote": {"vins_recommandes": ["Chablis", "Sancerre blanc"]},
    "moules-frites": {"vins_recommandes": ["Muscadet", "Entre-deux-Mers"]},
    "moules marinières": {"vins_recommandes": ["Muscadet", "Gros-Plant"]},
    "sushis": {"vins_recommandes": ["Sauvignon", "Sancerre rosé", "Entre-deux-Mers"]},
    "sashimis": {"vins_recommandes": ["Sauvignon Blanc", "Chablis", "Champagne Brut"]},
    "brandade de morue": {"vins_recommandes": ["Blanc de Provence", "Blanc de Corse"]},
    "bouillabaisse": {"vins_recommandes": ["Provence blanc", "Bandol rosé"]},
    "sole meunière": {"vins_recommandes": ["Meursault", "Chablis premier cru"]},
    "dos de cabillaud": {"vins_recommandes": ["Chablis", "Muscadet sur lie"]},
    "crevettes sautées": {"vins_recommandes": ["Provence rosé", "Muscadet"]},
    "homard grillé": {"vins_recommandes": ["Meursault", "Corton-Charlemagne"]},

    # === PÂTES, RIZ & FÉCULENTS ===
    "lasagnes à la bolognaise": {"vins_recommandes": ["Bandol", "Patrimonio rouge"]},
    "spaghettis à la bolognaise": {"vins_recommandes": ["Côtes-du-Rhône-Villages", "Chianti"]},
    "tagliatelles à la carbonara": {"vins_recommandes": ["Pinot Grigio", "Dolcetto", "Franciacorta"]},
    "spaghettis à la carbonara": {"vins_recommandes": ["Pinot Grigio", "Dolcetto", "Franciacorta"]},
    "risotto aux champignons": {"vins_recommandes": ["Chablis grand cru", "Côte-de-Beaune blanc", "Bourgogne Pinot Noir"]},
    "risotto aux fruits de mer": {"vins_recommandes": ["Vermentino", "Chablis", "Muscadet"]},
    "gratin dauphinois": {"vins_recommandes": ["Côtes-du-Rhône blanc", "Arbois rouge"]},
    "paella": {"vins_recommandes": ["Rioja", "Côtes-du-Roussillon rouge", "Provence rosé"]},
    "paella valenciana": {"vins_recommandes": ["Rioja", "Côtes-du-Roussillon rouge"]},
    "couscous": {"vins_recommandes": ["Costières-de-Nîmes", "Languedoc", "Tavel rosé"]},
    "couscous au poulet": {"vins_recommandes": ["Roussillon blanc", "Languedoc rosé"]},
    "couscous royal": {"vins_recommandes": ["Madiran", "Costières-de-Nîmes rouge"]},

    # === PLATS DU MONDE ===
    "mafe au poulet": {"vins_recommandes": ["Loire Chenin Blanc", "Meursault"]},
    "mafé au poulet": {"vins_recommandes": ["Loire Chenin Blanc", "Meursault"]},
    "mafe": {"vins_recommandes": ["Loire Chenin Blanc", "Meursault"]},
    "mafé": {"vins_recommandes": ["Loire Chenin Blanc", "Meursault"]},
    "pad thaï": {"vins_recommandes": ["Gewurztraminer", "Riesling demi-sec", "Viognier"]},
    "pad thai": {"vins_recommandes": ["Gewurztraminer", "Riesling demi-sec", "Viognier"]},
    "nems": {"vins_recommandes": ["Gewurztraminer", "Muscat sec"]},
    "bo bun": {"vins_recommandes": ["Sauvignon Blanc", "Riesling sec"]},
    "moussaka": {"vins_recommandes": ["Côtes-du-Rhône rouge", "Vacqueyras"]},
    "choucroute": {"vins_recommandes": ["Pinot blanc", "Riesling d'Alsace"]},
    "choucroute garnie": {"vins_recommandes": ["Riesling d'Alsace", "Pinot Gris"]},
    "pierrade": {"vins_recommandes": ["Côtes-du-Rhône", "Beaujolais Village"]},
    "fondue savoyarde": {"vins_recommandes": ["Savoie blanc", "Apremont"]},
    "fondue bourguignonne": {"vins_recommandes": ["Bourgogne rouge"]},
    "currywurst": {"vins_recommandes": ["Riesling sec", "Pinot Gris"]},
    "kebab": {"vins_recommandes": ["Côtes-du-Rhône rouge", "Languedoc rouge"]},
    "gyros": {"vins_recommandes": ["Côtes-du-Rhône rosé", "Provence rosé"]},
    "falafel": {"vins_recommandes": ["Sauvignon Blanc", "Vermentino"]},
    "houmous": {"vins_recommandes": ["Sauvignon Blanc", "Muscat sec"]},

    # === PLATS VÉGÉTARIENS ===
    "ratatouille": {"vins_recommandes": ["Costières-de-Nîmes", "Rosé de Provence", "Côtes-du-Rhône"]},
    "tomates farcies": {"vins_recommandes": ["Côtes-du-Rhône-Villages", "Côtes-de-Provence rosé"]},
    "soupe à l'oignon gratinée": {"vins_recommandes": ["Coteaux-du-Lyonnais blanc", "Arbois blanc"]},
    "gaspacho": {"vins_recommandes": ["Manzanilla", "Sauvignon Blanc"]},
    "quiche lorraine": {"vins_recommandes": ["Alsace Pinot Gris", "Chablis"]},
    "tarte aux légumes": {"vins_recommandes": ["Sauvignon Blanc", "Côtes-de-Provence blanc"]},

    # === OEUFS ===
    "oeufs bénédicte": {"vins_recommandes": ["Champagne Rosé", "Blanc de Blancs Champagne"]},
    "oeufs brouillés": {"vins_recommandes": ["Champagne", "Blanc de Blancs Champagne", "Cava"]},
    "omelette": {"vins_recommandes": ["Champagne", "Crémant de Bourgogne"]},

    # === FROMAGES & PLATS AU FROMAGE ===
    "raclette": {"vins_recommandes": ["Savagnin du Jura", "Roussette-de-Savoie"]},
    "tartiflette": {"vins_recommandes": ["Savoie blanc", "Côtes-du-Rhône blanc"]},
    "croque-monsieur": {"vins_recommandes": ["Beaujolais", "Bourgueil", "Chardonnay"]},
    "fish and chips": {"vins_recommandes": ["Chablis", "Loire Chenin Blanc"]},
    "soufflé au fromage": {"vins_recommandes": ["Saint-Véran", "Rully blanc"]},
    "escargots à l'ail": {"vins_recommandes": ["Bourgogne aligoté", "Mâcon blanc"]},

    # === BURGERS & FAST-FOOD ===
    "hamburger": {"vins_recommandes": ["Saint-Joseph", "Pic-Saint-Loup", "Blaye-Côtes-de-Bordeaux"]},
    "pizza margherita": {"vins_recommandes": ["Côtes-de-Provence rosé", "Gigondas"]},
    "pizza quatre fromages": {"vins_recommandes": ["Chardonnay", "Pinot Gris"]},
    "pizza napolitaine": {"vins_recommandes": ["Chianti", "Côtes-du-Rhône rouge"]},

    # === APÉRITIF ===
    "charcuterie": {"vins_recommandes": ["Dolcetto", "Morgon", "Lambrusco"]},
    "rillettes au saumon": {"vins_recommandes": ["Chablis", "Loire Chenin Blanc"]},
    "rillettes au lapin": {"vins_recommandes": ["Bourgogne Chardonnay", "Loire Chenin Blanc"]},
    "rillettes au porc": {"vins_recommandes": ["Beaujolais Fleurie", "Juliénas"]},
    "petit fours": {"vins_recommandes": ["Champagne Demi-sec", "Bonnezeaux", "Sauternes"]},
    "plateau de fromages": {"vins_recommandes": ["Sauternes", "Banyuls", "Porto"]},
    "galette jambon-fromage": {"vins_recommandes": ["Crémant", "Rosé d'Anjou"]},

    # === DESSERTS ===
    "tarte aux pommes": {"vins_recommandes": ["Bonnezeaux", "Coteaux-du-Layon"]},
    "tarte tatin": {"vins_recommandes": ["Bonnezeaux", "Jurançon moelleux"]},
    "tarte au citron meringuée": {"vins_recommandes": ["Bonnezeaux", "Muscat-de-Beaumes-de-Venise"]},
    "gâteau au chocolat": {"vins_recommandes": ["Porto Ruby", "Maury", "Banyuls"]},
    "fondant au chocolat": {"vins_recommandes": ["Porto Ruby", "Maury"]},
    "marbré au chocolat": {"vins_recommandes": ["Porto Ruby"]},
    "profiteroles": {"vins_recommandes": ["Porto Ruby", "Banyuls"]},
    "tarte aux myrtilles": {"vins_recommandes": ["Porto Ruby", "Maury"]},
    "éclair au chocolat": {"vins_recommandes": ["Porto Ruby"]},
    "baba au rhum": {"vins_recommandes": ["Porto Tawny", "Floc de Gascogne"]},
    "tiramisu": {"vins_recommandes": ["Moscato d'Asti", "Porto Tawny"]},
    "crème brûlée": {"vins_recommandes": ["Sauternes", "Coteaux-du-Layon"]},
    "île flottante": {"vins_recommandes": ["Coteaux-du-Layon", "Vouvray moelleux"]},
    "mousse au chocolat": {"vins_recommandes": ["Banyuls", "Maury", "Porto Ruby"]},
    "glace au café": {"vins_recommandes": ["Porto Tawny", "Rivesaltes ambré"]},
    "figues": {"vins_recommandes": ["Porto Tawny", "Banyuls", "Muscat de Rivesaltes"]},
    "foie gras de canard": {"vins_recommandes": ["Pinot gris vendanges tardives", "Jurançon moelleux", "Sauternes"]},
}
