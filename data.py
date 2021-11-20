'''Version 0.35'''
from bs4 import BeautifulSoup
import requests
from collections import defaultdict


Liquid_Measurements=set(["Tbsp",
      "Tbsps",
      "bottle",
      "bottles",
      "c",
      "cs",
      "cup",
      "cups",
      "dessertspoon",
      "dessertspoons",
      "fl oz",
      "fl ozs",
      "fluid ounce",
      "fluid ounces",
      "fluid oz",
      "fluid ozs",
      "gal",
      "gallon",
      "gallons",
      "gals",
      "jar",
      "jars",
      "liter",
      "liters",
      "milliliter",
      "milliliters",
      "ml",
      "mls",
      "pint",
      "pints",
      "pt",
      "pts",
      "qt",
      "qts",
      "quart",
      "quarts",
      "tablespoon",
      "tablespoons",
      "teaspoon",
      "teaspoons",
      "tsp",
      "tsps",
      "scoops"])
Solid_Measurements=set([
       "#",
      "#s",
      "bag",
      "bags",
      "bunch",
      "bunches",
      "can",
      "cans",
      "clove",
      "cloves",
      "cube",
      "cubes",
      "dash",
      "dashes",
      "envelope",
      "envelopes",
      "gram",
      "grams",
      "head",
      "heads",
      "inch",
      "inches",
      "kilogram",
      "kilograms",
      "lb",
      "lbs",
      "loaf",
      "ounce",
      "ounces",
      "oz",
      "ozs",
      "package",
      "packages",
      "packet",
      "packets",
      "piece",
      "pieces",
      "pinch",
      "pinches",
      "pound",
      "pounds",
      "sheet",
      "sheets",
      "slice",
      "slices",
      "strip",
      "strips"
])
prep=set( [
      "al dente",
      "allumette",
      "battered",
      "baton",
      "batonnet",
      "beaten",
      "bias",
      "blackened",
      "blanched",
      "blended",
      "boiled",
      "boned",
      "braised",
      "brewed",
      "broiled",
      "browned",
      "brunoise",
      "caked",
      "chopped",
      #"canned",
      "charred",
      "chilled",
      "chiffonade"
      "chopped",
      "cored",
      "creamed",
      "crumbled",
      "crushed",
      "cubed",
      "cured",
      "curried",
      "cut",
      "deglazed",
      "dehydrated",
      "debone",
      "deboned",
      "devein",
      "deviled",
      "diced",
      "dice",
      "divided",
      "drained",
      #"dried",
      "escalloped",
      "evaporated",
      "fermented",
      "flambé",
      "fricassed",
      "grated",
      "ground",
      "halved",
      "julienned",
      "mashed",
      "melted",
      "minced",
      "mince",
      "peeled",
      "pitted",
      "removed",
      "reserved",
      "rinsed",
      "roasted",
      "rubbed",
      "reduced",
      "seasoned",
      "seeded",
      "separated",
      "shredded",
      "sliced",
      "soaked",
      "softened",
      "stemmed",
      "thawed",
      "thawed",
      "torn",
      "patted",
      "quartered",
      "trimmed",
      "zested",
      "juiced"
    ])

descriptors= {
      "meat": set([
            "boneless",
            "instant",
            "lean",
            "lukewarm",
            "raw",
            "marbled",
            "refrigerated",
            "skinless",
            "halves",
            "skin",
            "bone",
            "breast",
            "neck",
            "giblets"
      ]),
      "other": set([
            "whole",
            "finger-sized",
            "all-purpose",
            "a la carte",
            "a la king",
            "a la mode",
            "acid",
            "acidic",
            "acrid",
            "airy",
            "alcoholic",
            "ambrosial",
            "aromatic",
            "au fromage",
            "au gratin",
            "au jus",
            "balsamic",
            "bite size",
            "bitter",
            "blah",
            "bland",
            "bold",
            "bolognese",
            "brackish",
            "briny",
            "brittle",
            "bubbly",
            "burning",
            "bursting",
            "buttery",
            "béarnaise",
            "cacciatore",
            "cakey",
            "candied",
            "carmelized",
            "caustic",
            "chalky",
            "charcuterie",
            "cheesy",
            "chewy",
            "chipotle",
            "chocolately",
            "classical",
            "crispy",
            "crumbly",
            "crunchy",
            "crusty",
            "crystalized",
            "curdled",
            "cold",
            "cubes",
            "dark",
            "decadent",
            "delactable",
            "dense",
            "diluted",
            "distinctive",
            "doughy",
            "dredged",
            "dried out",
            "dry",
            "earthy",
            "fatty",
            "feathery",
            "fibrous",
            "fiery",
            "finely",
            "filled",
            "filling",
            "finger licking good",
            "fishy",
            "fizzy",
            "flakey",
            "floury",
            "fluffy",
            "folded",
            "fragrant",
            "fried",
            "unsalted",
            "strips",
            "thinly",
            "slices",
            "hard",
            "extra-virgin",
            "seedless"
      ]),
      "seafood": set([
            "cooked",
            "freshly",
            "frozen"
      ]),
      "seasoning": set([
            "seasoning",
            "active",
            "all purpose",
            "boiling",
            "distilled",
            "dry",
            "extra firm",
            "extra virgin",
            "frying",
            "ground",
            "hickory flavored",
            "low sodium",
            "non dairy",
            "nonfat",
            "reduced sodium",
            "room temperature",
            "superfine",
            "sweetened",
            "unsweetened",
            "black"
      ]),
      "style": set([
            "african",
            "albanian",
            "algerian",
            "american",
            "andorrian",
            "argentinean",
            "argentinian",
            "armenian",
            "australian",
            "austrian",
            "bangladesh",
            "barbados",
            "belarus",
            "belgian",
            "belize",
            "bolivian",
            "brazilian",
            "british",
            "bulgarian",
            "cambodian",
            "canadian",
            "chad",
            "chilean",
            "chinese",
            "colombian",
            "costa rica",
            "creole",
            "croatian",
            "cuban",
            "dominican",
            "egyptian",
            "el salvadorian",
            "english",
            "estonian",
            "ethiopian",
            "finnish",
            "florentine",
            "french",
            "georgian",
            "german",
            "greek",
            "guatemalan",
            "hungarian",
            "indian",
            "indonesian",
            "iranian",
            "irish",
            "israeli",
            "italian",
            "japanese",
            "kenyan",
            "korean",
            "kosher",
            "liberian",
            "libyan",
            "lithuanian",
            "malaysian",
            "mediterranean",
            "mexican",
            "mongolian",
            "moroccan",
            "nigerian",
            "norwegian",
            "peruvian",
            "phillippino",
            "polish",
            "portuguese",
            "puerto rican",
            "romanian",
            "russian",
            "samoan",
            "serbian",
            "sichuan",
            "singapore",
            "slovakian",
            "somalian",
            "south african",
            "spanish",
            "sudanese",
            "swedish",
            "swiss",
            "syrian",
            "szechuan",
            "taiwanese",
            "thai",
            "tunisian",
            "turkish",
            "ukrainian",
            "venezuelan",
            "vietnamese"
      ]),
      "veggie": set([
            "condensed",
            "fresh",
            "large",
            "organic",
            "packed",
            "ripe",
            "very ripe",
            "flat-leaf"
      ]),
      "dairy":set([
            "skim",
            "whole"
      ])
      }


descriptors_non_nation=set([
      "boneless",
      "instant",
      "lean",
      "lukewarm",
      "raw",
      "marbled",
      "refrigerated",
      "skinless",
      "halves",
      "skin",
      "bone",
      "breast",
      "neck",
      "giblets"

      "whole",
      "finger-sized",
      "all-purpose",
      "a la carte",
      "a la king",
      "a la mode",
      "acid",
      "acidic",
      "acrid",
      "airy",
      "alcoholic",
      "ambrosial",
      "aromatic",
      "au fromage",
      "au gratin",
      "au jus",
      "balsamic",
      "bite size",
      "bitter",
      "blah",
      "bland",
      "bold",
      "bolognese",
      "brackish",
      "briny",
      "brittle",
      "bubbly",
      "burning",
      "bursting",
      "buttery",
      "béarnaise",
      "cacciatore",
      "cakey",
      "candied",
      "carmelized",
      "caustic",
      "chalky",
      "charcuterie",
      "cheesy",
      "chewy",
      "chipotle",
      "chocolately",
      "classical",
      "crispy",
      "crumbly",
      "crunchy",
      "crusty",
      "crystalized",
      "curdled",
      "cold",
      "cubes",
      "dark",
      "decadent",
      "delactable",
      "dense",
      "diluted",
      "distinctive",
      "doughy",
      "dredged",
      "dried out",
      "dry",
      "earthy",
      "fatty",
      "feathery",
      "fibrous",
      "fiery",
      "finely",
      "filled",
      "filling",
      "finger licking good",
      "fishy",
      "fizzy",
      "flakey",
      "floury",
      "fluffy",
      "folded",
      "fragrant",
      "fried",
      "unsalted",
      "strips",
      "thinly",
      "slices",
      "hard",
      "extra-virgin",
      "seedless"

      "cooked",
      "freshly",
      "frozen"

      "seasoning",
      "active",
      "all purpose",
      "boiling",
      "distilled",
      "dry",
      "extra firm",
      "extra virgin",
      "frying",
      "ground",
      "hickory flavored",
      "low sodium",
      "non dairy",
      "nonfat",
      "reduced sodium",
      "room temperature",
      "superfine",
      "sweetened",
      "unsweetened",
      "black"

      "condensed",
      "fresh",
      "large",
      "organic",
      "packed",
      "ripe",
      "very ripe",
      "flat-leaf"

      "skim",
      "whole"
])
      

Method_Primary=set([
      "bake",
      "boil",
      "broil",
      "blanch",
      "microwave",
      "stir-fry",
      "fry",
      "pressure cook",
      "grill",
      "mix",
      "simmer",
      "blend",
      "sear",
      "steam",
      "saute",
      "poach",
      "deep-fry",
      "shallow-fry"
    ])
Tools_to_Method={
      "air-fryer":"air-fry",
      "fryer":"fry",
      "wok":"stir-fry",
      "pressure cooker":"pressure cook"
}

Method_Secondary=set([
      "arrange",
      "add",
      "bake",
      "beat",
      "boil",
      "brush",
      "cover",
      "cool",
      "combine",
      "cream",
      "cut",
      "crush",
      "dip",
      "drain",
      "dry",
      "chill",
      "crumble",
      "flour",
      "flip",
      "fold",
      "grease",
      "grate",
      "heat",
      "line",
      "mash",
      "measure",
      "mix",
      "melt",
      "pour",
      "garnish",
      "preheat",
      "pound",
      "layer",
      "stuff",
      "knead",
      "refrigerate",
      "rinse",
      "saute",
      "serve",
      "season",
      "shake",
      "squeeze",
      "simmer",
      "sift",
      "slice",
      "soak",
      "spoon",
      "spread",
      "sprinkle",
      "stir",
      "strain",
      "toast",
      "toss",
      "turn",
      "whisk",
      "coat",
      "place",
      "rub",
      "lower"
    ])
Tools=set([
    "apple corer",
    "apple cutter",
    "bag",
    "baking sheet",
    "balloon whisk",
    "basket skimmer",
    "baster",
    "basting brush",
    "beanpot",
    "bell whisk",
    "bench knife",
    "bench scraper",
    "biscuit mould",
    "blender",
    "blow torch",
    "blowlamp",
    "blowtorch",
    "boil oven preventer",
    "bottle opener",
    "bowl",
    "bread knife",
    "browning bowl",
    "browning plate",
    "browning tray",
    "bulb baster",
    "burger spatula",
    "burr grinder",
    "burr mill",
    "buscuit cutter",
    "buscuit press",
    "butcher's twine",
    "butter curler",
    "cake server",
    "cake shovel",
    "can opener",
    "candy thermometer",
    "carving knife",
    "cheese cutter",
    "cheese grater",
    "cheese knife",
    "cheese knives",
    "cheese slicer",
    "cheese spreader",
    "cheesecloth",
    "chef knife",
    "chef's knife",
    "chefs knife",
    "cherry pitter",
    "chinois",
    "chinoise",
    "citrus reamer",
    "clay pot",
    "cleaver",
    "colander",
    "cookie cutter",
    "cookie mould",
    "cookie press",
    "cooking twine",
    "corkscrew",
    "crab cracker",
    "cup",
    "cutting board",
    "deep spoon",
    "dish",
    "dough scraper",
    "drum sieve",
    "dutch oven",
    "edible tableware",
    "egg piercer",
    "egg poacher",
    "egg separator",
    "egg slicer",
    "egg timer",
    "fat separator",
    "fillet knife",
    "fish scaler",
    "fish slice",
    "fish spatula",
    "flat coil whisk",
    "flat whisk",
    "flour sifter",
    "food mill",
    "food storage container",
    "french whisk",
    "frying pan",
    "funnel",
    "fryer",
    "garlic press",
    "grapefruit knife",
    "grater",
    "gravy separator",
    "gravy strainer",
    "gravy whisk",
    "griddle",
    "herb chopper",
    "honey dipper",
    "ice cream scoop",
    "kitchen mallet",
    "kitchen scale",
    "kitchen scissor",
    "kitchen scraper",
    "kitchen string",
    "kitchen tool crock",
    "kitchen twine",
    "knife",
    "ladle",
    "lame",
    "lemon reamer",
    "lemon squeezer",
    "lobster fork",
    "lobster pick",
    "mandoline",
    "mashers",
    "mated colander pot",
    "measuring cup",
    "measuring jar",
    "measuring jug",
    "measuring spoon",
    "meat grinder",
    "meat tenderiser",
    "meat tenderizer",
    "meat thermometer",
    "melon ball",
    "melon baller",
    "metal tong",
    "mezzaluna",
    "microplane",
    "milk frother",
    "milk guard",
    "milk watcher",
    "mincer",
    "mini whisk",
    "mixing bowl",
    "mixing whisk",
    "molcajete",
    "mortar",
    "nutcracker",
    "nutmeg grater",
    "olive stoner",
    "oven glove",
    "oven mitt",
    "oven",
    "pan",
    "panini spatula",
    "pasta fork",
    "pastry bag",
    "pastry blender",
    "pastry brush",
    "pastry wheel",
    "paper towel",
    "peeler",
    "pepper grinder",
    "pepper mill",
    "pestle",
    "pie bird",
    "pie cutter",
    "pie funnel",
    "pie server",
    "pie vent",
    "pizza cutter",
    "pizza shovel",
    "pizza slicer",
    "pot holder",
    "pot minder",
    "pot",
    "pot-holder",
    "potato masher",
    "potato ricer",
    "potholder",
    "poultry shears",
    "ricer",
    "roast lifter",
    "roller docker",
    "rolling pin",
    "salt shaker",
    "santoku knife",
    "saucepan",
    "scale",
    "scissor",
    "scoop",
    "scraper",
    "serrated bread knife",
    "serving platter",
    "shredder",
    "sieve",
    "sifter",
    "silicone tong",
    "skillet",
    "slotted spoon",
    "spatula",
    "spider strainer",
    "spider",
    "spoon sieve",
    "spoon skimmer",
    "steak knife",
    "stove",
    "strainer",
    "sugar thermometer",
    "tablespoon",
    "tamis",
    "teaspoon",
    "tin opener",
    "tomato knife",
    "tong",
    "trussing needle",
    "turner",
    "twine",
    "urokotori",
    "utility knife",
    "vegetable peeler",
    "weighing scales",
    "whisk",
    "wooden spoon",
    "zester",
    "nonstick spray"
])
Time_Units=set([
      "second",
      "seconds",
      "minute",
      "minutes",
      "hour",
      "hours",
      "day",
      "days"
])
Vegan_Protein=set([
      "cauliflower",
      "lentils",
      "tempeh",
      "king oyster mushrooms",
      "cabbage",
      "tofu",
      "chickpeas",
      "black beans",
      "pinto"
])
Non_Vegan={"meat":[
      "beef",
      "pork",
      "lamb",
      "chicken",
      "duck",
      "turkey",
      "fish",
      "cod",
      "crab",
      "clam",
      "mussels",
      "shrimp",
      "salmon",
      "tuna",
      "tilapia",
      "rib",
      "sirloin",
      "brisket",
      "bacon",
      "bison",
      "goose",
      "mutton",
      "venison",
      "catfish",
      "ham",
      "lobster",
      "octopus"
]}

Vegetable=set([
      "potatoes",
      "potato",
      "tomatoes",
      "tomato",
      "onion",
      "onions",
      "carrots",
      "lettuce",
      "bell peppers",
      "broccoli",
      "cucumbers",
      "celery",
      "mushrooms",
      "mushroom",
      "corn",
      "spinach",
      "green beans",
      "cauliflower",
      "cabbage",
      "asparagus",
      "brussel sprouts",
      "crookneck",
      "edamame",
      "eggplant",
      "pumkin",
      "chickpeas"
])
#Intentionally ignored ingredients that serve as seasonings.
Vegan={
      "milk powder":"almond milk powder",
      "milk":"soy milk",
	  "mozzarella cheese": "vegan mozzarella cheese",
      "mozzarella": "vegan mozzarella",
      "parmesan cheese": "vegan parmesan cheese",
      "cheese": "crumbled tofu",
      "butter": "vegan margarine",
      "yogurt": "almond milk yogurt",
      "scrambled egg": "tofu scramble",
      "egg whites":'tofu',
      "egg white":"tofu",
      "egg yolk": "tofu",
      "egg": "tofu",
      "yolk": "tofu",
      "instant pudding": "dairy free instant pudding",
      "pudding": "dairy free pudding",
      "sour cream": "vegan sour cream",
      "mayonnaise": "vegan mayonnaise",
      "ketchup": "vegan ketchup",
      "gelatin": "agar flakes",
      "honey": "agave nectar",
      "chocolate": "non-dairy chocolate",
      "hollandaise sauce": "vegan hollandaise sauce",
      "oyster sauce": "vegetarian oyster sauce",
      "worcestershire sauce": "organic worcestershire sauce",
      "bread": "wheat tortilla",
      "bread toasts": "wheat tortilla",
      "bagel": "vegan bagel",
      "pancake": "vegan pancake"
}

Make_Healthy={"approach":{
      "fry":"air-fry",
      "grill":"broil"
      },
      "tools":{
            "fryer":"air-fryer",
            "grill":"oven"
      }
      ,
      "ingredients":{
            "sugar":"honey",
            "white sugar":"honey",
            "brown sugar":"honey",
            "sour cream":"greek yogurt",
            "flour":"whole wheat flour",
            "butter":"margarine",
            "whole milk":"skim milk",
            "peanut butter":"powdered peanut",
            "baking powder":"baking soda",
            "chocolate":"berries",
            "cream cheese":"fat-free cream",
            "mayonnaise":"plain yogurt",
            "mayo":"plain yogurt",
            "white bread":"wheat bread",
            "sausage":"bacon",
            "egg":"egg white",
            "pasta":"whole grain pasta",
            "spaghetti":"whole grain spaghetti",
            "potato":"cauliflower",
            "potatoes":"cauliflowers",
            "pork":"beef",
            "noodles":"zucchini noodles",
            "potato chips":"popcorn",
            "ranch dressing":"balsamic vinegar",
            "salami":"low-sodium ham",
            "pickle":"cucumber",
            "cheese":"low-fat cheese",
            "margarine":"diet margarine",
            "turkey bacon":"fresh turkey stripes",
            "chocolate":"carob",
            "beef":"extra-lean beef",
            "soy sauce":"low-sodium soy sauce"
      }
}

Make_Unhealthy={"approach":{
      "broil":"grill",
      "steam":"fry",
      "saute":"fry"
      },
      "tools":{
            "steamer":"deep fryer",
            "oven":"grill",
            "pan":"deep fryer"
      }
      ,
      "ingredients":{
            "honey":"sugar",
            "sweet potato":"potato",
            "beef":"pork",
            "chicken":"pork",
            "salmon":"pork",
            "mushroom":"pork",
            "milk":"creamer",
            "bacon":"sausage",
            "hummus":"mayo",
            "broccoli":"potato",
            "bell pepper":"bacon",
            "cauliflower":"potato",
            "edamame":"sausage",
            "chickpeas":"sausage",
            "carrot":"potato",
            "jam":"sugar",
            "olive oil":"butter",
            "nuts":"chocolate",
            "greek yogurt":"sour cream",
            "cinnamon":"sugar",
            "applesauce":"sugar",
            "maple syrup":"sugar"
      }
}

Gluten_Free={
      "farro":"rice",
      "barley":"quinoa",
      "bulgur":"millet",
      "spelt":"buckwheat",
      "kamut":"rice",
      "breadcrumbs":"chickpea crumbs",
      "noodle":"rice noodles",
      "noodles":"rice noodles",
      "pasta":"kelp noodles",
      "spaghetti":"spaghetti squash",
      "fettuccine":"veggie noodles",
      "macaroni":"kelp noodles",
      "bow ties":"rice noodles",
      "tortillas":"corn tortillas",
      "flour tortillas":"corn tortillas",
      "soy sauce":"coconut aminos",
      "pizza crust":"cauliflower crust",
      "flour":"rice flour",
      "rigatoni pasta":"kelp noodles"
}


Chinese = \
      {"approach":{
            "fry":"stir-fry",
            "saute":"stir-fry",
            "sear":"stir-fry",
            "soak":"boil",
            "immerse":"braise",
            "bath":"braise",
            "broil":"roast",
            "grill":"roast",
            "bake":"steam"
      },
      "tools":{
            "fork":"chopsticks",
            "spoon":"cooking shovel",
            "pan":"wok",
            "tray":"wok",
            "oven":"steamer"
      },
      "ingredients":{
            "chili":"dried chili",
            "hot pepper":"chili powder",
            #"pepper":"sichuan peppercorns",
            "pepper":"white pepper",
            "spice":"five spice powder",
            "parsley":"bay leaf",
            "coriander":"bay leaf",
            "seasoning":"parsley",
            "salt":"soy sauce",
            "lemon":"vinegar",
            "olive oil": "sesame oil",
            "butter":"sesame oil",
            "starch":"cornstarch",
            "bbq sauce":"oyster sauce",
            "tomato sauce":"hoisin sauce",
            "ketchup":"hosin sauce",
            #"cabbage":"bok choy",
            "cabbage":"napa cabbage",
            "mushroom":"shiitake mushroom",
            "mushrooms":"shiitake mushrooms",
            "cinnamon":"chinese five spice",
            "tomato sauce":"chilli bean sauce",
            "red chilli sauce":"chilli bean sauce",
            "mayonnaise":"chilli bean sauce",
            "mayo":"chilli bean sauce",
            "red wine":"shaoxing rice wine",
            "vinegar":"white rice vinegar",
            "pasta":"dried egg noodles",
            "spaghetti":"dried egg noodles",
            #"noodles":"vermicelli noodles"
      }
}

Cajun=\
{
      "approach":
      {
            "stir-fry":"saute",
            "steam":"smoke",

      },
      "tools":{
            "chopsticks":"fork",
            "steamer":"smoker"
      },
      "ingredients":
      {
            "miripoix":"holy trinity",
            "soffrito":"holy trinity",
            "carrot":"bell pepper",
            "roux":"dark roux",
            "shallot":"green onion",
            "chili":'cayenne',
            "sausage":"andouille",
            "chorizo":"boudin",
            "pork":"boar",
            "pork belly":"salt pork",
            "stew":"gumbo",
            "rice":"dirty rice"
      }

}

German=\
{
      "ingredients":
      {
            "sour cream":"schmandt",
            "beef":"veal",
            "fennel":"caraway"
      }
}


Mexican={
      "approach":{
            "bake":"roast",
            "wok":"plancha",
            "griddle":"plancha",
            "broil":"roast"
      },
      "tools":{
            "oven":"steamer",
            "spoon":"spatula"
      },
      "ingredients":{
            "pasta":"pinto",
            "spaghetti":"black beans",
            "flour":"rice flour",
            "potato":"avocado",
            "potatoes":"avocado",
            "basil":"cilantro",
            "parsley":"cilantro",
            "lemon":"lime",
            "soy sauce":"vinegar",
            "ketchup":"salsas",
            "broccoli":"corn",
            "cauliflower":"corn",
            "hot pepper":"jalapenos",
            "beef":"pork",
            "miripoix":"soffrito",
            "steak":"pork",
            "macaroni":"rice",
            "lasagne":"rice",
            "chiles":"guajillo chiles",
            "cinnamon":"mexican cinnamon",
            "chocolate":"mexican chocolate",
            "butter":"lard",
            "vegetable oil":"lard"
      }
}

Lactose_Free={
      "milk":"soy milk",
      "butter":"coconut oil",
      "cheese":"plant-based cheese",
      "hard cheese":"tofu",
      "ice cream":"sherbet",
      "yogurt":"coconut milk yogurt",
      "cream":"coconut milk",
      "heavy cream":"coconut milk",
      "whipping cream":"coconut milk",
      "sour cream":"nondairy yogurt"
}

Cook_Approach=set([
      "bake",
      "boil",
      "broil",
      "stir-fry",
      "fry",
      "pressure cook",
      "grill",
      "steam",
      "saute",
      "deep-fry"
])

Approach_Tools={
      "oven",
      "wok",
      "fryer",
      "pressure cooker",
      "grill",
      "steamer",
      "fry pan",
      "sauce pan",
      "stock pot",
      "skillet",
      "griddle",
      "plancha",
      "deep fryer"
}


Meat_Parts=set([
      "neck",
      "chuck",
      "shank",
      "brisket",
      "shank",
      "rib",
      "loin",
      "rump",
      "sirloin",
      "flank",
      "tail",
      "thigh",
      "thighs",
      "wing",
      "wings",
      "tender",
      "tenderloin",
      "drum stick",
      "breast",
      "breasts",
      "head",
      "belly",
      "leg",
      "legs",
      "hock",
      "totters"
])