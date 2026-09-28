"""Apply the approved Catalan proper-noun mapping to translated <value> text.

Only values are touched (never keys). Whole-word, case-aware, longest-first.
Handles surrounding Catalan articles/prepositions, including through <color>/<i>
tags, and keeps elision (l', de l', a l') correct.
"""
import re

# (english patterns, catalan value WITHOUT leading article, article kind)
# kind: m, f, mp, fp, elision, None (literal, no article logic)
_ENTRIES = [
    # --- celestial ---
    (["Ash Twin Project"], "Projecte de la Bessona de Cendra", "m"),
    (["Hourglass Twins"], "Bessones del Rellotge de Sorra", "fp"),
    (["Ash Twin"], "Bessona de Cendra", "f"),
    (["Ember Twin"], "Bessona de Brases", "f"),
    (["Timber Hearth"], "Llar de Fusta", "f"),
    (["Brittle Hollow"], "Buit Trencadís", "m"),
    (["Hollow's Lantern", "Hollow’s Lantern"], "Far del Buit", "m"),
    (["Giant's Deep", "Giant’s Deep"], "Abisme del Gegant", "elision"),
    (["Dark Bramble"], "Esbarzer Fosc", "elision"),
    (["The Interloper", "Interloper"], "Intrús", "elision"),
    (["White Hole Station"], "Estació del Forat Blanc", "elision"),
    (["White Hole"], "Forat Blanc", "m"),
    (["Quantum Moon"], "Lluna Quàntica", "f"),
    (["The Eye of the universe", "The Eye of the Universe", "Eye of the universe",
      "Eye of the Universe"], "Ull de l'Univers", "elision"),
    (["The Stranger", "Stranger"], "Estranger", "elision"),
    (["The Vessel", "Vessel"], "Nau-Mare", "f"),
    (["Escape Pod"], "Càpsula de Salvament", "f"),
    (["Sun Station"], "Estació Solar", "elision"),
    (["Sun"], "Sol", "m"),
    # --- structures / tech ---
    (["Orbital Probe Cannon"], "Canó de Sondes Orbital", "m"),
    (["Probe Tracking Module"], "Mòdul de Rastreig de Sondes", "m"),
    (["Control Module"], "Mòdul de Control", "m"),
    (["Launch Module"], "Mòdul de Llançament", "m"),
    (["Black Hole Forge District"], "Districte de la Forja del Forat Negre", "m"),
    (["Eye Shrine District"], "Districte del Santuari de l'Ull", "m"),
    (["School District"], "Districte de l'Escola", "m"),
    (["Stepping Stone District"], "Districte de les Pedres de Pas", "m"),
    (["Anglerfish Overlook District"], "Districte del Mirador del Peix Llanterna", "m"),
    (["Meltwater District"], "Districte de l'Aigua Fosa", "m"),
    (["Crash Site Caves"], "Coves del Lloc de l'Accident", "fp"),
    (["Black Hole Forge"], "Forja del Forat Negre", "f"),
    (["High Energy Lab"], "Laboratori d'Alta Energia", "m"),
    (["Sunless City"], "Ciutat Sense Sol", "f"),
    (["Hanging City"], "Ciutat Penjada", "f"),
    (["Construction Yard"], "Pati de Construcció", "m"),
    (["Gravity Cannon"], "Canó Gravitacional", "m"),
    (["Tower of Quantum Knowledge"], "Torre del Coneixement Quàntic", "f"),
    (["Tower of Quantum Trials"], "Torre de les Proves Quàntiques", "f"),
    (["Quantum Shrine"], "Santuari Quàntic", "m"),
    (["Statue Workshop"], "Estudi de les Estàtues", "elision"),
    (["Southern Observatory"], "Observatori del Sud", "elision"),
    (["Meltwater District"], "Districte de l'Aigua Fosa", "m"),
    (["Crossroads"], "Cruïlla", "f"),
    (["Little Scout"], "Petit Explorador", "m"),
    # --- caves / sites ---
    (["Zero-G Cave"], "Cova de Gravetat Zero", "f"),
    (["Nomai Mines"], "Mines Nomai", "fp"),
    (["Quantum Grove"], "Bosc Quàntic", "m"),
    (["Radio Tower"], "Torre de Ràdio", "f"),
    (["Lakebed Cave"], "Cova del Llit del Llac", "f"),
    (["Fossil Fish Cave"], "Cova del Peix Fòssil", "f"),
    (["Stepping Stone Cave"], "Cova de les Pedres de Pas", "f"),
    (["Anglerfish Overlook"], "Mirador del Peix Llanterna", "m"),
    (["Old Settlement"], "Assentament Antic", "elision"),
    (["Northern Glacier"], "Glacera del Nord", "f"),
    (["Nomai Grave"], "Sepulcre Nomai", "m"),
    # --- Echoes of the Eye ---
    (["River Lowlands"], "Riberes Baixes", "fp"),
    (["Cinder Isles"], "Illes de Cendra", "fp"),
    (["Hidden Gorge"], "Gorga Amagada", "f"),
    (["Shrouded Woodlands"], "Boscos Tapats", "mp"),
    (["Starlit Cove"], "Cala Estelada", "f"),
    (["Endless Canyon"], "Congost Infinit", "m"),
    (["Reservoir"], "Presa", "f"),
    (["Submerged Structure"], "Estructura Submergida", "f"),
    (["Hollow Structure"], "Estructura Buida", "f"),
    (["Forbidden Archive"], "Arxiu Prohibit", "elision"),
    (["The Prisoner", "Prisoner"], "Presoner", "m"),
    (["Vision Torch"], "Torxa de Visions", "f"),
    (["Slide Reel"], "Bobina de Diapositives", "f"),
    (["Artifact"], "Artefacte", "elision"),
    (["Lantern"], "Llanterna", "f"),
    # --- species / misc ---
    (["Hearthians"], "llarins", "mp"),
    (["Hearthian"], "llarí", "m"),
    (["Nomaian"], "nomai", None),
    (["Anglerfish"], "peix-llanterna", "m"),
    (["Signalscope"], "Espectre de Senyals", "m"),
    (["Outer Wilds Ventures"], "Aventures Outer Wilds", "fp"),
]

# possessives / special literal replacements (applied first)
_LITERAL = [
    (r"Vessel['’]s", "de la Nau-Mare"),
    (r"Stranger['’]s", "de l'Estranger"),
    (r"Interloper['’]s", "de l'Intrús"),
    (r"Eye['’]s", "de l'Ull"),
    (r"Attlerock['’]s", "de l'Attlerock"),
]

_ARTICLES = {
    "del": "de", "dels": "de", "de la": "de", "de les": "de", "de l'": "de", "de l’": "de",
    "al": "a", "als": "a", "a la": "a", "a les": "a", "a l'": "a", "a l’": "a",
    "el": "bare", "la": "bare", "els": "bare", "les": "bare", "l'": "bare", "l’": "bare",
    "de": "de", "a": "a", "d'": "de",
}
_PRE_FORMS = {
    "m": {"bare": "el", "de": "del", "a": "al"},
    "f": {"bare": "la", "de": "de la", "a": "a la"},
    "mp": {"bare": "els", "de": "dels", "a": "als"},
    "fp": {"bare": "les", "de": "de les", "a": "a les"},
}


def _analytic(kind, pre):
    if kind == "elision":
        return {"bare": "l'", "de": "de l'", "a": "a l'"}[pre]
    return _PRE_FORMS[kind][pre]


def _build():
    pats = []
    for englishes, value, kind in _ENTRIES:
        for e in englishes:
            pats.append((e, value, kind))
    pats.sort(key=lambda t: len(t[0]), reverse=True)

    alts = "|".join(re.escape(e) for e, _, _ in pats)
    lookup = {e.lower(): (v, k) for e, v, k in pats}
    art = "d['’]|de la|de les|de l['’]|a la|a les|a l['’]|dels|del|als|al|els|les|l['’]|la|el|de|a"
    rx = re.compile(
        r"(?<![A-Za-zÀ-ÿ'’])"
        r"(?:(?P<art>" + art + r")\s*)?"
        r"(?P<open>(?:<[^>]+>)*)(?P<name>" + alts + r")(?P<close>(?:</?[^>]+>)*)",
        re.IGNORECASE,
    )
    return rx, lookup


_RX, _LOOKUP = _build()
_LIT_RX = [(re.compile(p, re.IGNORECASE), r) for p, r in _LITERAL]

# targeted grammar fixes after name substitution (feminine agreement, etc.)
_CLEANUPS = [
    (re.compile(r"ha estat ferit de mort", re.IGNORECASE), "ha estat ferida de mort"),
    (re.compile(r"Bessona de Brases és ple de", re.IGNORECASE), "La Bessona de Brases és plena de"),
    (re.compile(r"Nau-Mare nomai abandonat", re.IGNORECASE), "Nau-Mare nomai abandonada"),
    (re.compile(r"El lloc ara és inhòspit", re.IGNORECASE), "El lloc ara és inhabitable"),
]


def apply_names(text):
    if not text:
        return text
    for rx, rep in _LIT_RX:
        text = rx.sub(rep, text)

    def repl(m):
        name = m.group("name")
        value, kind = _LOOKUP[name.lower()]
        if name.isupper():
            value = value.upper()
        open_tags = m.group("open") or ""
        close_tags = m.group("close") or ""
        art = m.group("art")
        if art is not None and kind is not None:
            art_l = art.lower().replace("’", "'")
            pre = _ARTICLES[art_l]
            form = _analytic(kind, pre)
            if m.start() == 0 or text[m.start() - 1] == "\n" or (
                m.start() >= 2 and text[m.start() - 2] in ".!?"
            ):
                if form and form[0].islower():
                    form = form[0].upper() + form[1:]
            sep = "" if form.endswith("'") else " "
            return form + sep + open_tags + value + close_tags
        return open_tags + value + close_tags

    text = _RX.sub(repl, text)
    for rx, rep in _CLEANUPS:
        text = rx.sub(rep, text)
    return text
