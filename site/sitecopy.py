"""Namaste Crystal Shop (namastecrystalshop.com): the all-around online crystal shop, organized stone by stone with meanings,
hardness and care, plus beginner kits. Copy written for this site only."""
import re, types, json
E = __import__('html').escape
ICON = 'gem'
FAM_LABEL, FAM_ALL, STYLE_LABEL, STYLE_ALL = 'Stone', 'All stones', 'Size', 'All sizes'
NO_FAMILY = ('care',)
READINGS = 'https://namastebookshop.com/pages/book-a-reading'

_TYPES = {
 'tumbled': ['Crystal Tumbled', 'Worry Stones Crystals', 'Worry Stone', 'Crystal Gallet', 'Crystal Palmstone Gallet', 'Palm Stone', 'Cube Crystal', 'Teardrop'],
 'raw': ['Crystal Rough Raw', 'Fossils Crystal'],
 'points': ['Crystal Tower Obeliak', 'Crystal Tower Obeliak Generator', 'Crystal Points', 'CrystalS Point', 'Cut Base Crystal Point', 'Cutbase Cluster / Point', 'Crystal D/T Stones Points',
            'Crystal Flame', 'Aura Quartz Points, Cluster, Tower', 'Aura Quartz Points, Cluster, Tower, Heart', 'Crystal Wand', 'Healing Stick Magic Wand', 'Healing Stick Wand', 'Top Polished Cut Base'],
 'shapes': ['Crystal Sphere', 'crystal Heart', 'Crystal Carving', 'Crystal Eggs', 'Crystal Skulls', 'Pyramid', 'Orgone Pyramids', 'Merkaba Crystal', 'Spirit Animals', 'Free Form Crystals'],
 'clusters': ['Clusters Crystal', 'Crystal Geode', 'Enhydro Quartz', 'Crystals Specimens', 'Crystal specimen', 'Crystal specime', 'Crystal Specimen', 'Crystal Polished Slabs, POF, Irregular',
              'Crystal Polished Slabs, POF', 'Crystals Slabs POF', 'Naturally Polished Faceted Crystal', 'Gallery Pieces Crystals Stones', 'Crystals', 'Crystal', 'Polished Crystal', 'Stones'],
 'kits': ['chakra Stone Kit Set', 'Chakra Kit', 'Crystal Gem Tree', 'Sacred Geometry Set', 'Massager Crystal Gua Sha', 'Gua Sha', 'Massage Therapy Stone'],
 'care': ['Stand', 'Bags & Pouches', 'Wood Storage Box', 'Crystal Bowl'],
}
_T2C = {t: k for k, ts in _TYPES.items() for t in ts}
def category(p):
    t, ty = p['title'], p.get('product_type', '')
    if ty == 'Spiritual Kit & Bundle' and re.search(r'crystal|stone', t, re.I): return 'kits'
    if ty in ('Info Charts', 'Info Guides') and re.search(r'crystal|gem', t, re.I): return 'care'
    c = _T2C.get(ty)
    if c == 'raw' and re.search(r'fossil', t, re.I) and not re.search(r'stone|crystal|ammonite|orthoceras|petrified|amber', t, re.I): return None
    if c == 'clusters' and re.search(r'cluster|geode|druzy', t, re.I) is None and ty in ('Crystals', 'Crystal', 'Stones', 'Polished Crystal'):
        if re.search(r'tumble', t, re.I): return 'tumbled'
        if re.search(r'tower|point|wand|obelisk|generator', t, re.I): return 'points'
        if re.search(r'sphere|heart|egg|skull|pyramid|carv', t, re.I): return 'shapes'
        if re.search(r'\braw\b|rough', t, re.I): return 'raw'
    return c
def assign(x): return x['base']

_ST = [('Rose Quartz', r'rose quartz'), ('Clear Quartz', r'clear quartz|crystal quartz|quartz crystal'), ('Smoky Quartz', r'smok(e)?y quartz'),
 ('Aura Quartz', r'\baura\b|angel aura|titanium'), ('Amethyst', r'amethyst'), ('Citrine', r'citrine'), ("Tiger's Eye", r"tiger'?s? ?eye"),
 ('Moonstone', r'moonstone'), ('Black Tourmaline', r'tourmaline'), ('Obsidian', r'obsidian'), ('Pyrite', r'pyrite'), ('Malachite', r'malachite'),
 ('Lapis Lazuli', r'lapis'), ('Fluorite', r'fluorite'), ('Labradorite', r'labradorite'), ('Aquamarine', r'aquamarine'), ('Agate', r'agate'),
 ('Jasper', r'jasper'), ('Kyanite', r'kyanite'), ('Garnet', r'garnet'), ('Jade', r'\bjade\b'), ('Hematite', r'hematite'), ('Carnelian', r'carnelian'),
 ('Moldavite', r'moldavite'), ('Selenite', r'selenite'), ('Aventurine', r'aventurine'), ('Rhodochrosite', r'rhodochrosite'), ('Shungite', r'shungite'),
 ('Lepidolite', r'lepidolite'), ('Turquoise', r'turquoise'), ('Chrysocolla', r'chrysocolla'), ('Sodalite', r'sodalite'), ('Calcite', r'calcite'),
 ('Sunstone', r'sunstone'), ('Amazonite', r'amazonite'), ('Black Onyx', r'onyx'), ('Howlite', r'howlite'), ('Dolomite', r'dolomite'), ('Lodolite', r'lodolite'),
 ('Ocean Jasper', r'ocean jasper'), ('Quartz', r'quartz')]
def _slug(n): return re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
FAMILIES = [(_slug(n), n, rx) for n, rx in _ST]
# stone notes: (traditional associations, Mohs hardness, color/what it is, care). Traditions are folklore, labeled as such on every page.
NOTES = {
 'rose-quartz': ('love, self-compassion and gentle emotional healing', '7', 'a pink variety of quartz', 'Fine to rinse; keep out of strong sun, which can fade the pink.'),
 'clear-quartz': ('clarity and amplifying whatever intention you set', '7', 'colorless crystalline quartz', 'Hard and easy to clean with water and a soft cloth.'),
 'smoky-quartz': ('grounding and letting go of stress', '7', 'quartz colored brown to gray by natural irradiation', 'Rinse and dry; long sun exposure can lighten it.'),
 'aura-quartz': ('joy, play and lifting the mood', '7', 'quartz coated with a thin metallic film that makes the rainbow sheen', 'Wipe gently; scratches and harsh cleaners can wear the coating.'),
 'amethyst': ('calm, restful sleep and intuition', '7', 'a purple variety of quartz', 'Keep out of sunny windows; the purple fades with long sun exposure.'),
 'citrine': ('abundance, warmth and optimism', '7', 'a yellow to orange quartz; much of what is sold is heat-treated amethyst', 'Rinse and dry; avoid long sun exposure.'),
 'tiger-s-eye': ('confidence, focus and steady courage', '6.5 to 7', 'a chatoyant quartz with a golden, shifting band of light', 'Durable; wipe with a damp cloth.'),
 'moonstone': ('new beginnings, cycles and intuition', '6 to 6.5', 'a feldspar with a soft blue or white sheen', 'Avoid knocks; it can chip along cleavage planes.'),
 'black-tourmaline': ('protection and shielding', '7 to 7.5', 'a black, striated borosilicate mineral (schorl)', 'Raw pieces can be brittle along the striations.'),
 'obsidian': ('protection, truth and grounding', '5 to 5.5', 'natural volcanic glass', 'Edges can be sharp and chip; handle and store with care.'),
 'pyrite': ('prosperity and willpower', '6 to 6.5', "an iron sulfide often called fool's gold", 'Keep dry; moisture can tarnish it.'),
 'malachite': ('transformation and change', '3.5 to 4', 'a banded green copper carbonate', 'Keep dry and never use it in drinking water; do not sand or breathe its dust.'),
 'lapis-lazuli': ('wisdom, truth and honest speech', '5 to 5.5', 'a deep blue rock of lazurite, often flecked with pyrite', 'Keep away from water and chemicals.'),
 'fluorite': ('focus, order and a clear head', '4', 'a soft mineral that grows in cubes and octahedrons, often banded purple and green', 'Scratches easily; store it apart and away from sun.'),
 'labradorite': ('intuition and a touch of magic', '6 to 6.5', 'a feldspar whose blue and gold flash is called labradorescence', 'Wipe clean; avoid hard knocks.'),
 'aquamarine': ('calm, clear communication and courage', '7.5 to 8', 'a blue-green beryl', 'Hard and durable; rinse and dry.'),
 'agate': ('balance and stability', '6.5 to 7', 'a banded chalcedony; brightly colored pieces are often dyed', 'Durable; dyed pieces should stay out of water.'),
 'jasper': ('nurturing, steady energy', '6.5 to 7', 'an opaque chalcedony in reds, yellows, greens and patterns', 'Durable and easy to clean.'),
 'kyanite': ('alignment and calm communication', '4.5 to 7 (it varies with direction)', 'a bladed blue mineral', 'Fragile along its blades; keep dry and handle gently.'),
 'garnet': ('passion, vitality and commitment', '6.5 to 7.5', 'a family of deep red to orange silicate minerals', 'Durable; rinse and dry.'),
 'jade': ('luck, harmony and long life', '6 to 7', 'nephrite or jadeite; many green stones sold as jade are other minerals', 'Durable; wipe with a soft cloth.'),
 'hematite': ('grounding and focus', '5.5 to 6.5', 'an iron oxide with a metallic sheen', 'Keep dry; it can rust.'),
 'carnelian': ('motivation, creativity and courage', '6.5 to 7', 'an orange to red chalcedony', 'Durable; rinse and dry.'),
 'moldavite': ('transformation and big change', 'about 5.5', 'a green natural glass (tektite) from central Europe; imitations are common', 'Handle gently; buy from sellers who can tell you its source.'),
 'selenite': ('cleansing and peace', '2', 'a soft, fibrous variety of gypsum', 'Never wet it; water dissolves and dulls it. Dust only.'),
 'aventurine': ('luck and opportunity', '6.5 to 7', 'a quartz with tiny glittering inclusions, most often green', 'Durable; rinse and dry.'),
 'rhodochrosite': ('compassion and healing old hurts', '3.5 to 4', 'a pink-banded manganese carbonate', 'Soft; keep dry and away from acids.'),
 'shungite': ('protection and purifying lore', '3.5 to 4', 'a black, carbon-rich rock from Karelia, Russia', 'Leaves black marks; keep dry.'),
 'lepidolite': ('calm during change', '2.5 to 3', 'a lilac, lithium-bearing mica', 'Soft and flaky; keep dry.'),
 'turquoise': ('protection, travel and friendship', '5 to 6', 'a blue-green copper phosphate; much on the market is stabilized or dyed', 'Porous; keep away from water, oils and perfume.'),
 'chrysocolla': ('gentle communication', '2 to 4', 'a blue-green copper silicate, often mixed with quartz', 'Soft; keep dry.'),
 'sodalite': ('logic and truth', '5.5 to 6', 'a royal blue mineral with white veins', 'Wipe clean; avoid harsh cleaners.'),
 'calcite': ('energy and motivation, depending on its color', '3', 'a calcium carbonate found in many colors', 'Soft; keep dry and away from vinegar or acids.'),
 'sunstone': ('joy and leadership', '6 to 6.5', 'a feldspar with coppery glitter', 'Durable; wipe clean.'),
 'amazonite': ('soothing and honest expression', '6 to 6.5', 'a blue-green feldspar', 'Avoid knocks and long sun exposure.'),
 'black-onyx': ('strength and protection', '6.5 to 7', 'a black chalcedony, frequently dyed', 'Durable; dyed pieces should stay dry.'),
 'howlite': ('patience and calm', '3.5', 'a white, gray-veined borate, often dyed to imitate turquoise', 'Porous; keep dry.'),
 'dolomite': ('balance and steadiness', '3.5 to 4', 'a calcium magnesium carbonate, often carved into small animals', 'Soft; keep dry and dust gently.'),
 'lodolite': ('dreaming and inner journeys', '7', 'quartz with mineral "gardens" trapped inside, also called garden quartz', 'Hard; rinse and dry.'),
 'ocean-jasper': ('joy and patience', '6.5 to 7', 'an orbicular jasper from Madagascar with round "eyes"', 'Durable; rinse and dry.'),
 'quartz': ('clarity and focus', '7', "one of Earth's most common minerals, in many colors", 'Hard; rinse and dry.'),
}
def style_of(t, b, base):
    m = re.search(r'(\d+(?:\.\d+)?)\s*(?:-|to)?\s*(?:\d+(?:\.\d+)?)?\s*(?:"|”|in\b|inch)', t, re.I)
    if not m: return ''
    v = float(m.group(1))
    return 'Pocket (under 2 in)' if v < 2 else ('Hand-sized (2 to 4 in)' if v < 4 else 'Display (4 in and up)')

_BRANDS = [('heaven-earth', 'Heaven & Earth', r'heaven ?& ?earth', ['Heaven & Earth LLC', 'HVNRTH']), ('starborn', 'Starborn', r'\bstarborn\b', ['STARBORN']),
           ('crystal-earth-studio', 'Crystal Earth Studio', r'crystal earth studio', ['crystal Earth Studio']), ('zorbitz', 'Zorbitz', r'zorbitz', ['ZORBITZ Inc'])]
_V = {v: k for k, _, _, vs in _BRANDS for v in vs}
def _brand_of(title, vendor=''):
    for k, _, rx, _ in _BRANDS:
        if re.search(rx, title, re.I): return k
    return _V.get(vendor or '', '')
BR = types.SimpleNamespace(NAME={k: n for k, n, _, _ in _BRANDS}, brand_of=_brand_of, FACTS={})

AISLES = {
 'tumbled':  ('Tumbled, Palm & Worry Stones', 'Tumbled', 'tumbled-palm-worry-stones', 'Smooth stones to carry, hold or set on a grid: tumbles, palm stones, worry stones and cubes.', '#d94f70'),
 'raw':      ('Raw & Rough Crystals', 'Raw', 'raw-rough-crystals', 'Stones as they came out of the ground, plus a few fossils.', '#9a6b3f'),
 'points':   ('Towers, Points & Wands', 'Towers & Points', 'towers-points-wands', 'Generators, obelisks, natural and cut-base points, flames and wands.', '#6c4ab6'),
 'shapes':   ('Spheres, Hearts & Carvings', 'Shapes', 'spheres-hearts-carvings', 'Polished spheres, hearts, eggs, skulls, pyramids, free forms and spirit animals.', '#2e86ab'),
 'clusters': ('Clusters, Geodes & Specimens', 'Clusters', 'clusters-geodes-specimens', 'Druzy clusters, geodes, slabs and one-of-a-kind specimens.', '#1b998b'),
 'kits':     ('Kits, Gem Trees & Sets', 'Kits & Sets', 'crystal-kits-sets', 'Chakra sets, starter kits, gem trees, sacred geometry sets and stone face tools.', '#e09f3e'),
 'care':     ('Stands, Pouches & Crystal Guides', 'Stands & Care', 'crystal-stands-pouches-guides', 'Sphere stands, velvet pouches, storage boxes and printed stone guides.', '#55606e'),
}

VISIT_EYEBROW = 'Prefer to choose in person?'
def STORE_DESC(S): return f'Online crystal shop with about {S.ABOUT_N:,} crystals organized stone by stone, with meanings, hardness and care, and pickup inside Namaste Bookshop near Union Square.'
REVIEW_TITLE = 'Found your stone with us?'
REVIEW_TEXT = 'A quick Google review helps other crystal lovers find a shop that explains every stone.'
LOGO_SVG = '<svg viewBox="0 0 40 40"><path d="M20 3l7 9-7 25-7-25z" fill="none" stroke="#b9a2ff" stroke-width="2.2" stroke-linejoin="round"/><path d="M13 12h14M20 3v34" stroke="currentColor" stroke-width="1.3"/><circle cx="31" cy="30" r="3" fill="#ffcf6b"/></svg>'
WORDMARK = 'Namaste <b>Crystal Shop</b>'
BAR_TEXT = 'Crystal shop'
SEARCH_PLACEHOLDER = 'Search a stone: amethyst, pyrite, selenite'

QUIZ = {
 'slug': 'which-crystal', 'nav': 'Which crystal?', 'cta': 'Find my crystal',
 'title': 'Which Crystal Is Right for Me? A 3-Question Finder', 'desc': 'Answer three questions about intention, shape and budget and see crystals in stock today at Namaste Crystal Shop.',
 'h1': 'Which crystal is right for you?', 'lead': 'Choose an intention, a shape and a budget. We match them against stones in stock today. The intentions come from crystal folklore, shared for meaning, not as health advice. Your answers stay on this page.',
 'submit': 'Show my crystals',
 'questions': [
  {'q': 'What would you like more of?', 'options': [
    {'label': 'Calm and better rest', 'filter': {'fam': ['amethyst', 'lepidolite', 'selenite', 'howlite']}},
    {'label': 'Love and self-kindness', 'filter': {'fam': ['rose-quartz', 'rhodochrosite']}},
    {'label': 'Protection and grounding', 'filter': {'fam': ['black-tourmaline', 'obsidian', 'smoky-quartz', 'hematite', 'shungite', 'black-onyx']}},
    {'label': 'Money and opportunity', 'filter': {'fam': ['citrine', 'pyrite', 'aventurine', 'jade']}},
    {'label': 'Focus and clarity', 'filter': {'fam': ['clear-quartz', 'fluorite', 'quartz', 'sodalite']}},
    {'label': 'Intuition', 'filter': {'fam': ['labradorite', 'moonstone', 'lapis-lazuli', 'amethyst']}}]},
  {'q': 'What shape?', 'options': [
    {'label': 'Something to hold or carry', 'filter': {'aisle': ['tumbled']}}, {'label': 'A tower or point', 'filter': {'aisle': ['points']}},
    {'label': 'A sphere, heart or carving', 'filter': {'aisle': ['shapes']}}, {'label': 'Raw, clusters and specimens', 'filter': {'aisle': ['raw', 'clusters']}}]},
  {'q': 'Budget?', 'options': [{'label': 'Under $15', 'filter': {'maxp': 15}}, {'label': 'Under $50', 'filter': {'maxp': 50}}, {'label': 'Any price', 'filter': {}}]},
 ]}

def FOOTER_EXPLORE(S):
    return [('Crystal meanings A to Z', '/crystal-meanings/'), ('Crystals for beginners', '/guide/crystals-for-beginners/'), ('How to cleanse crystals', '/guide/how-to-cleanse-crystals/'),
            ('Crystal hardness chart', '/guide/crystal-hardness-chart/'), ('Which crystal?', '/which-crystal/'), ('Crystals under $10', '/crystals-under-10/'), ('Book a reading', READINGS)]
FOOT_BLURB = 'Every stone explained: what it is, what tradition says about it, how hard it is and how to look after it, with the crystals to match.'
HERO_BASES = ('points', 'shapes', 'clusters', 'tumbled')
def HERO(S):
    return {'eyebrow': 'Stones A&ndash;Z &middot; Meanings &middot; Beginner kits',
            'h1': 'Every crystal, <em>explained stone by stone.</em>',
            'lede': f'About {S.ABOUT_N:,} crystals across {len([k for k, _, _ in FAMILIES if S.fam_count[k] >= 3])} stones, each with what it is, its hardness, how to care for it and what crystal tradition says about it. Pocket stones from {S.money(S.MIN_PRICE)}.',
            'shop_cta': 'Shop crystals'}
def _az(S):
    keys = sorted([k for k, n, _ in FAMILIES if S.fam_count[k] >= 3], key=lambda k: S.FAM_NAME[k])
    chips = ''.join(f'<a class="chip" href="/crystal-meanings/{k}/">{E(S.FAM_NAME[k])} <small>{S.fam_count[k]}</small></a>' for k in keys)
    return f'<section class="wrap"><div class="sechead"><h2>Shop by stone, A to Z</h2><a href="/crystal-meanings/">Every meaning &rarr;</a></div><div class="chips">{chips}</div></section>'
STARTER = ['clear-quartz', 'amethyst', 'rose-quartz', 'citrine', 'black-tourmaline', 'selenite', 'tiger-s-eye', 'carnelian', 'aventurine', 'obsidian']
def starter_set(S, n=5):
    picks, seen = [], set()
    for fam in STARTER:
        for x in S.by_rank([y for y in S.leaders if y['family'] == fam and y['aisle'] in ('tumbled', 'raw', 'points') and not y['noimg'] and y['price'] <= 20]):
            av = [v for v in x['variants'] if v['available']]
            if len(x['group']) == 1 and len(av) == 1 and fam not in seen:
                picks.append((x, av[0])); seen.add(fam); break
        if len(picks) == n: break
    if len(picks) < 3: return ''
    data = [{'v': str(v['id']), 'h': x['handle'], 't': x['title'], 'p': f"{float(v['price']):.2f}", 'i': f"{x['images'][0]}{'&' if '?' in x['images'][0] else '?'}width=400", 'c': x['aisle'], 'k': x['base']} for x, v in picks]
    lis = ''.join(f'<li><label><input type="checkbox" checked aria-label="Include {E(x["title"])}"><img src="{E(d["i"].replace("width=400", "width=120"))}" alt="" width="56" height="56" loading="lazy">'
                  f'<span><b>{E(S.FAM_NAME[x["family"]])}:</b> {E(x["title"])}</span><b>{S.money(d["p"])}</b></label></li>' for (x, v), d in zip(picks, data))
    js = E(json.dumps(data))
    return (f'<div class="bundle"><h2>Build a first crystal set</h2><p class="small">One of each classic starter stone, picked from what is in stock today. Untick any you already own.</p><ul>{lis}</ul>'
            f'<div class="btot"><span>Together: <b data-bundle-total>{S.money(sum(float(d["p"]) for d in data))}</b></span><button type="button" class="btn" data-bundle="{js}" data-atc-items="{js}">Add the set to cart</button></div></div>')
def _starter(S):
    b = starter_set(S)
    return f'<section class="wrap"><div class="sechead"><h2>New to crystals?</h2><a href="/guide/crystals-for-beginners/">Beginner guide &rarr;</a></div>{b}</section>' if b else ''
def _best(S): return S.by_rank(S.leaders)[:8] if S.HAS_RANK else []
def _pocket(S): return [x for x in S.by_rank(S.leaders) if x['aisle'] == 'tumbled' and not x['noimg']][:8]
def _kits(S): return [x for x in S.by_rank(S.leaders) if x['aisle'] == 'kits' and not x['noimg']][:8]
def _whys(S):
    return [('Every stone explained', 'Meaning, hardness, what the stone actually is, and how to care for it, on every stone page.'),
            (f'About {S.ABOUT_N:,} crystals', 'Each with its own photos, price and live stock.'),
            ('Honest labels', 'We tell you when a stone is commonly dyed, coated, heat-treated or imitated.'),
            (('Free pickup in Manhattan', f'Collect inside Namaste Bookshop at 2 W 14th St. Orders are {S.READY.lower()}.') if S.PICKUP_ON else ('', '')),
            ('Secure checkout', 'Payment runs on Shopify through namastebookshop.com.'),
            ('Ships from NYC', 'Crystals are packed and shipped from New York City.')]
HOME_SECTIONS = [
 {'type': 'html', 'html': _az},
 {'type': 'html', 'html': _starter},
 {'type': 'collections', 'title': 'Shop by shape', 'items': [
   {'title': 'Tumbled & palm stones', 'blurb': 'Smooth, pocket-sized, easy to start with.', 'href': '/shop/tumbled-palm-worry-stones/', 'filter': {'aisle': ['tumbled']}},
   {'title': 'Towers & points', 'blurb': 'Stand them on a desk, shelf or altar.', 'href': '/shop/towers-points-wands/', 'filter': {'aisle': ['points']}},
   {'title': 'Spheres & hearts', 'blurb': 'Polished, tactile and giftable.', 'href': '/shop/spheres-hearts-carvings/', 'filter': {'aisle': ['shapes']}},
   {'title': 'Raw crystals', 'blurb': 'Rough and natural.', 'href': '/shop/raw-rough-crystals/', 'filter': {'aisle': ['raw']}},
   {'title': 'Clusters & geodes', 'blurb': 'Druzy, geodes and specimens.', 'href': '/shop/clusters-geodes-specimens/', 'filter': {'aisle': ['clusters']}},
   {'title': 'Kits & gem trees', 'blurb': 'Ready-made sets and starter kits.', 'href': '/shop/crystal-kits-sets/', 'filter': {'aisle': ['kits']}}]},
 {'type': 'grid', 'title': 'Pocket stones people start with', 'select': _pocket, 'href': '/shop/tumbled-palm-worry-stones/', 'link': 'All tumbled stones'},
 {'type': 'grid', 'title': 'Best sellers', 'select': _best, 'href': '/shop/', 'link': 'Shop all'},
 {'type': 'quiz', 'title': 'Which crystal is yours?', 'text': 'An intention, a shape and a budget: three taps to stones in stock today.'},
 {'type': 'grid', 'title': 'Kits, sets & gem trees', 'select': _kits, 'href': '/shop/crystal-kits-sets/', 'link': 'All kits'},
 {'type': 'whys', 'title': 'Why shop crystals here', 'items': _whys},
 {'type': 'visit'},
 {'type': 'brands', 'title': 'Named makers', 'n': 6},
 {'type': 'review'},
]
def HOME_TITLE(S): return 'Namaste Crystal Shop | Crystals A to Z with Meanings, Kits & Pocket Stones'
def HOME_DESC(S): return f'Shop about {S.ABOUT_N:,} crystals stone by stone, with meanings, hardness and care for each. Tumbled stones, towers, spheres, raw crystals and beginner kits. Ships from NYC or pick up at 2 W 14th St.'
def SHOP_TITLE(S): return 'Shop All Crystals Online | Namaste Crystal Shop'
def SHOP_DESC(S): return f'{S.N:,} crystals by stone, shape, size and price, from {S.money(S.MIN_PRICE)}. Ships from New York City or pick up inside Namaste Bookshop.'
SHOP_H1 = 'All crystals'
def SHOP_SUB(S): return f'{S.N:,} crystals in stock. Filter by stone, size, maker or price.'
def AISLE_TITLE(S, k): return f'{AISLES[k][0]} | Namaste Crystal Shop'
def AISLE_DESC(S, k): return f'{AISLES[k][3]} {S.cat_count[k]} in stock, every one with its stone explained. Ships from NYC or pick up at 2 W 14th St.'

def _meaning_html(S, k, n):
    tr, mohs, what, care = NOTES.get(k, ('', '', '', ''))
    if not tr: return ''
    return (f'<div class="stonefacts"><p><b>What it is:</b> {E(n)} is {E(what)}.</p><p><b>Hardness:</b> {E(mohs)} on the Mohs scale.</p>'
            f'<p><b>Care:</b> {E(care)}</p><p><b>In crystal tradition:</b> {E(n.lower())} is associated with {E(tr)}. This is folklore, shared for meaning, not a medical or scientific claim.</p></div>')
def LANDINGS(S):
    L = []
    for k, n, _ in FAMILIES:
        c = S.fam_count[k]
        if c < 3: continue
        kinds = [S.AISLES[a][1].lower() for a, _ in __import__('collections').Counter(x['aisle'] for x in S.products if x['family'] == k).most_common(3)]
        L.append({'path': f'/crystal-meanings/{k}/', 'title': f'{n} Meaning, Hardness & Care, plus {n} Crystals to Buy | Namaste Crystal Shop',
                  'desc': f'What {n.lower()} is, its Mohs hardness, how to care for it and what tradition says it means, with {c} {n.lower()} crystals in stock: {", ".join(kinds)}.',
                  'h1': f'{n}: meaning, care and crystals', 'sub': f'{c} {n.lower()} pieces in stock today.', 'filter': {'fam': [k]}, 'intro': _meaning_html(S, k, n)})
    L.append({'path': '/crystals-under-10/', 'title': 'Crystals Under $10 | Namaste Crystal Shop', 'desc': 'Tumbled stones, worry stones, small points and raw pieces under $10.',
              'h1': 'Crystals under $10', 'sub': 'The easiest way to start a collection.', 'filter': {'maxp': 10}})
    L.append({'path': '/crystals-under-25/', 'title': 'Crystals Under $25 | Namaste Crystal Shop', 'desc': 'Palm stones, small towers, hearts and raw specimens under $25.',
              'h1': 'Crystals under $25', 'sub': 'Bigger pieces that still make easy gifts.', 'filter': {'maxp': 25}})
    return L

def brand_intro(S, k, st):
    return (f'<p>{st["n"]} crystal{"s" if st["n"] != 1 else ""} from {E(S.BRAND_NAME[k])}, mainly {E(" and ".join(S.AISLES[a][0].lower() for a, _ in st["aisles"].most_common(2)))}, from {S.money(st["min"])}.</p>')
def brand_faq(S, k, st):
    name = S.BRAND_NAME[k]
    return [(f'Does Namaste Crystal Shop carry {name}?', f'Yes, {st["n"]} pieces are listed today.'), (f'What does {name} cost here?', (f'{S.money(st["min"])} to {S.money(st["max"])}' if st['max'] > st['min'] else S.money(st['min'])) + '; prices update daily.')]
def BRAND_H1(S, k): return f'{S.BRAND_NAME[k]} crystals'
def BRAND_TITLE(S, k, st): return f'{S.BRAND_NAME[k]} Crystals | Namaste Crystal Shop'
def BRAND_DESC(S, k, st): return f'{st["n"]} {S.BRAND_NAME[k]} crystals from {S.money(st["min"])}, shipped from NYC or picked up at 2 W 14th St.'
def BRANDS_TITLE(S): return 'Crystal Makers A to Z | Namaste Crystal Shop'
def BRANDS_DESC(S): return 'Named crystal makers we stock. Most crystals come from mineral suppliers, so browse them by stone.'
BRANDS_H1 = 'Crystal makers'
def BRANDS_LEAD(S, n): return f'{n} named makers. Most crystals come from mineral wholesalers rather than brands, so the best way to browse is <a href="/crystal-meanings/">by stone</a>.'

PAIR = {'points': ['tumbled', 'care'], 'shapes': ['care', 'tumbled'], 'clusters': ['tumbled'], 'raw': ['tumbled'], 'tumbled': ['care', 'tumbled'], 'kits': ['care'], 'care': ['tumbled']}
CART_PAIR_TITLE = 'Finish your collection'
REL_BRAND = 'More from {brand}'
REL_SCENT = 'More {scent}'
REL_PAIR = 'Pairs well with'
REL_MORE = 'More {aisle}'
_KIND = {'tumbled': 'smooth tumbled or palm stone', 'raw': 'raw, rough piece', 'points': 'tower, point or wand', 'shapes': 'polished carving', 'clusters': 'cluster or specimen', 'kits': 'kit or set', 'care': 'crystal stand, pouch or guide'}
def describe(S, x):
    k = x['family']; n = S.FAM_NAME.get(k, '')
    s = [f"{E(x['title'])}: a {_KIND[x['aisle']]} from Namaste Crystal Shop."]
    if k in NOTES:
        tr, mohs, what, care = NOTES[k]
        s.append(f'{E(n)} is {E(what)}, about {E(mohs)} on the Mohs hardness scale. {E(care)}')
        s.append(f'In crystal tradition it is linked with {E(tr)}; we share that as folklore, not as a health claim. <a href="/crystal-meanings/{k}/">More about {E(n.lower())}</a>.')
    if x['style']: s.append(f'Size class: {E(x["style"].lower())}, based on the measurement in the title.')
    s.append('Natural stones vary, so color, pattern and size can differ a little from the photo.' if x['aisle'] not in ('care', 'kits') else '')
    s.append('Ships from New York City, or reserve it for pickup inside Namaste Bookshop, 2 West 14th Street. Checkout is completed on Shopify.')
    return [t for t in s if t]
def PRODUCT_DESC(S, x, v0):
    n = S.FAM_NAME.get(x['family'], '')
    return f"{x['title']}, {S.money(v0['price'])}." + (f' {n} meaning, hardness and care included.' if n else '') + ' Ships from NYC or pick up at 2 W 14th St.'

def ABOUT_DESC(S): return 'About Namaste Crystal Shop: an online crystal shop that explains every stone, run by Wealth Edge Ventures Inc., owner of Namaste Bookshop.'
ABOUT_H1 = 'About Namaste Crystal Shop'
def ABOUT(S):
    return f'''<p class="lead">Namaste Crystal Shop is an online crystal shop built around one idea: you should know what a stone is before you buy it.</p>
<p>Every stone has its own page with what it actually is, its hardness, how to care for it, what crystal tradition says about it, and every piece we have in that stone. About {S.ABOUT_N:,} crystals are listed, from pocket stones to display towers, plus kits for beginners. We say so when a stone is commonly dyed, coated, heat-treated or imitated.</p>
<h2>Who runs it</h2><p>{S.LEGAL} Wealth Edge Ventures also owns Namaste Bookshop, and the crystals come from the same inventory. Orders are checked out on Shopify through <a href="{S.SHOP}" rel="noopener">namastebookshop.com</a>, which takes payment and ships from New York City.</p>
<h2>See them in person</h2><p>Every crystal can also be picked up, or seen, inside Namaste Bookshop at {S.STORE_ADDR}. Call <a href="tel:{S.TEL}">{S.PHONE}</a>.</p>{S.hours_html()}{S.visit_buttons()}
<h2>A note on meanings</h2><p>Crystal meanings come from folklore and modern crystal practice. We include them because people ask, always labeled as tradition. They are not medical advice or a substitute for professional care.</p>'''
def FAQ_DESC(S): return 'Questions about Namaste Crystal Shop: shipping, pickup, real vs treated stones, cleansing, hardness and choosing a first crystal.'
FAQ_H1 = 'Crystal shop FAQ'
def FAQ(S):
    return [('Are your crystals real?', 'Yes, they are natural minerals unless the listing says otherwise. Some popular materials are treated: aura quartz is coated, much citrine is heat-treated amethyst, and agate, howlite and onyx are often dyed. Our stone pages point this out.'),
            ('Which crystal should a beginner start with?', 'Clear quartz, amethyst and rose quartz are the classic first three. See <a href="/guide/crystals-for-beginners/">crystals for beginners</a> or build a first set on the home page.'),
            ('How do I cleanse a crystal?', 'People use moonlight, sound, smoke or a selenite plate. Avoid water for soft stones like selenite. Read <a href="/guide/how-to-cleanse-crystals/">how to cleanse crystals</a>.'),
            ('Which crystals can go in water?', 'Hard quartz-family stones are fine for a rinse. Selenite, malachite, lepidolite, calcite, pyrite and other soft or metallic stones should stay dry. See the <a href="/guide/crystal-hardness-chart/">hardness chart</a>.'),
            ('Do you ship?', 'Yes, from New York City. Checkout runs on Shopify through namastebookshop.com, and costs show before you pay.'),
            ('Can I pick up in person?', f'Yes, inside Namaste Bookshop at {S.STORE_ADDR}. Choose Pickup at checkout.' + (f' Orders are {S.READY.lower()}.' if S.READY else '')),
            ('Do crystals heal?', 'We share crystal traditions as meaning and folklore only. They are not medical advice.')]

def GUIDES(S):
    keys = sorted([k for k, n, _ in FAMILIES if S.fam_count[k] >= 3], key=lambda k: S.FAM_NAME[k])
    letters = {}
    for k in keys: letters.setdefault(S.FAM_NAME[k][0].upper(), []).append(k)
    az = '<nav class="az" aria-label="Jump to letter">' + ''.join(f'<a href="#m-{L}">{L}</a>' for L in sorted(letters)) + '</nav>' + ''.join(
        f'<h2 id="m-{L}">{L}</h2><ul class="dir">' + ''.join(f'<li><a href="/crystal-meanings/{k}/">{E(S.FAM_NAME[k])}</a>: <span class="small">{E(NOTES[k][0]) if k in NOTES else ""} &middot; {S.fam_count[k]} in stock</span></li>' for k in ks) + '</ul>' for L, ks in sorted(letters.items()))
    rows = ''.join(f'<tr><td><a href="/crystal-meanings/{k}/">{E(S.FAM_NAME[k])}</a></td><td>{E(NOTES[k][1])}</td><td>{E(NOTES[k][3])}</td></tr>' for k in keys if k in NOTES)
    starter = starter_set(S, 6)
    return [
     {'path': '/crystal-meanings/', 'title': 'Crystal Meanings A to Z', 'desc': f'Meanings, hardness and care for {len(keys)} crystals, A to Z, each linked to the stones in stock.', 'h1': 'Crystal meanings A to Z',
      'html': f'<p class="lead">Pick a stone to read what it is, how hard it is, how to look after it and what tradition says it means, then see every piece we have.</p>{az}<p class="small">Meanings are folklore, shared for interest, not medical advice.</p>'},
     {'path': '/guide/crystals-for-beginners/', 'title': 'Crystals for Beginners: Where to Start', 'desc': 'A plain-English start to crystals: the classic first stones, how to choose, shapes explained, care basics and a ready-made first set.', 'h1': 'Crystals for beginners',
      'html': f'''<p class="lead">You do not need a big collection, or any special knowledge, to start. Pick a few stones you like the look and feel of.</p>
<h2>The classic first stones</h2><ul><li><a href="/crystal-meanings/clear-quartz/">Clear quartz</a>: the all-rounder, tied to clarity.</li><li><a href="/crystal-meanings/amethyst/">Amethyst</a>: calm and rest.</li><li><a href="/crystal-meanings/rose-quartz/">Rose quartz</a>: love and kindness to yourself.</li>
<li><a href="/crystal-meanings/citrine/">Citrine</a>: optimism and abundance.</li><li><a href="/crystal-meanings/black-tourmaline/">Black tourmaline</a>: protection.</li><li><a href="/crystal-meanings/selenite/">Selenite</a>: often used to cleanse other stones (keep it dry).</li></ul>
<h2>Which shape?</h2><p><b>Tumbled stones</b> are smooth and cheap, good for a pocket or a bedside dish. <b>Points and towers</b> stand up on a shelf. <b>Spheres and hearts</b> are tactile and make easy gifts. <b>Raw pieces</b> show the stone as it formed.</p>
<h2>Care basics</h2><p>Know your stone's hardness: soft stones scratch and some dissolve. Our <a href="/guide/crystal-hardness-chart/">hardness chart</a> lists what can get wet.</p>
{starter}<p class="small">Crystal meanings are folklore, shared for interest only.</p><p><a class="btn" href="/shop/crystal-kits-sets/">Shop kits and sets</a></p>'''},
     {'path': '/guide/how-to-cleanse-crystals/', 'title': 'How to Cleanse Crystals (and Which Ones to Keep Dry)', 'desc': 'Common ways people cleanse crystals: moonlight, sound, smoke, selenite and earth, plus which stones should never get wet.', 'h1': 'How to cleanse crystals',
      'html': '''<p class="lead">"Cleansing" is a crystal tradition for resetting a stone. Physically, you only need to keep it dust-free; the ritual part is up to you.</p>
<h2>Popular methods</h2><ul><li><b>Moonlight:</b> leave stones on a windowsill overnight, especially at a full moon.</li><li><b>Sound:</b> a singing bowl, bell or tuning fork near the stones.</li><li><b>Smoke:</b> pass stones through incense or sage smoke in a ventilated room.</li><li><b>Selenite:</b> rest smaller stones on a selenite plate or next to a selenite tower.</li><li><b>Water:</b> only for hard, non-porous stones such as quartz.</li></ul>
<h2>Keep these dry</h2><p>Selenite, malachite, lepidolite, calcite, pyrite, hematite, rhodochrosite, kyanite, turquoise and other soft, porous or metallic stones.</p>
<h2>Keep these out of strong sun</h2><p>Amethyst, rose quartz, citrine, smoky quartz, fluorite and amazonite can fade.</p><p><a class="btn" href="/crystal-meanings/selenite/">Shop selenite</a></p>'''},
     {'path': '/guide/crystal-hardness-chart/', 'title': 'Crystal Hardness Chart (Mohs) and Care', 'desc': f'Mohs hardness and care notes for {len(keys)} crystals, including which stones can get wet and which scratch easily.', 'h1': 'Crystal hardness chart',
      'html': f'<p class="lead">Hardness tells you how easily a stone scratches. Below about 5, keep stones apart and dry.</p><div class="tablewrap"><table class="hard"><thead><tr><th>Stone</th><th>Mohs</th><th>Care</th></tr></thead><tbody>{rows}</tbody></table></div>'},
    ]
NOT_FOUND = 'That stone rolled away'
