"""Road model for the Greater Neptune Region atlas.
Every mileage and drive time in the atlas comes from this one graph, so they agree.
Usage: python3 atlas.py
"""
import heapq, itertools

E = []  # (a, b, miles, mph, note)
def road(a, b, mi, mph, note=""):
    E.append((a, b, mi, mph, note))

# --- The Causeway, by milepost -------------------------------------------
CAUSEWAY = [  # (milepost, node, mph for the stretch ending here)
    (0,   "Neptune (Mile 0)", None),
    (15,  "Loki's Weir", 45),
    (23,  "Lake Creek Turn", 45),
    (47,  "Camp Nine turn", 45),
    (50,  "Low Pass", 45),
    (62,  "Cheshire Fork", 45),
    (66,  "Airport Road", 50),
    (73,  "Amity Gate", 50),
    (76,  "I-5 Interchange", 50),
    (112, "Sweetbriar (west)", 55),
    (117, "Sweetbriar (east)", 50),
    (129, "Five Fords (Blue River end)", 50),
    (133, "Saltlick Grade turn", 50),
    (140, "Five Fords (ranger station)", 50),
    (159, "Lake Varuna", 45),
    (164, "Santiam Junction", 45),
    (168, "Santiam Pass", 50),
    (178, "Cadence (west, UGNC)", 50),
    (181, "Cadence", 45),
    (189, "Eastern sign", 50),
]
for (m0, a, _), (m1, b, mph) in zip(CAUSEWAY, CAUSEWAY[1:]):
    road(a, b, m1 - m0, mph, "Causeway")
road("Eastern sign", "Sisters (outside)", 1, 45)

# --- Coast ----------------------------------------------------------------
road("Neptune (Mile 0)", "Ichabod's Eye", 13, 45, "US 101")
road("Ichabod's Eye", "Wrack", 13, 45, "US 101")
road("Wrack", "Newport (outside)", 24, 45, "US 101")
road("Neptune (Mile 0)", "Reedsport (outside)", 21, 50, "US 101")
road("Reedsport (outside)", "Coos Bay (outside)", 27, 50, "US 101")
road("Neptune (Mile 0)", "Neptune Municipal Airport", 3, 30, "city streets")

# --- Valley Waist and outside anchors -------------------------------------
road("Camp Nine turn", "Camp Nine", 5, 25, "Forest Road 14")
road("Amity Gate", "Honey Hills", 15, 45, "OR 99E and the bench road")
road("Airport Road", "Eugene Airport (outside)", 9, 40, "Airport Road")
road("I-5 Interchange", "Eugene (outside)", 18, 65, "I-5")
road("I-5 Interchange", "Albany (outside)", 24, 65, "I-5")
road("Albany (outside)", "Salem (outside)", 25, 65, "I-5")
road("Salem (outside)", "Portland Airport (outside)", 60, 60, "I-5 and I-205")
road("Amity Gate", "Corvallis (outside)", 26, 50, "county roads and OR 99W")
road("Eugene (outside)", "Springfield (outside)", 4, 40, "city")
road("Eugene (outside)", "Eugene Airport (outside)", 8, 40, "city")
road("Loki's Weir", "Eugene (outside)", 47, 50, "the Old Grade (OR 126)")
road("Springfield (outside)", "Sweetbriar (west)", 20, 50, "OR 126")
road("Eugene (outside)", "OR 58 junction (outside)", 7, 65, "I-5")

# --- High Country ---------------------------------------------------------
road("Santiam Junction", "Sump Creek Settlement", 32, 45, "OR 22")
road("Sump Creek Settlement", "Salem (outside)", 50, 50, "OR 22")
road("Santiam Junction", "Mirth", 40, 50, "US 20")
road("Mirth", "Sweet Home (outside)", 14, 50, "US 20")
road("Sweet Home (outside)", "Amity Gate", 31, 50, "OR 228 through Brownsville")
road("Sisters (outside)", "Redmond Airport (outside)", 23, 55, "OR 126")
road("Sisters (outside)", "Bend (outside)", 22, 55, "US 20")

# --- Deschutes Rim (Rim Line Road closes in winter) ------------------------
road("Cadence", "Shale", 34, 45, "Forest Road 51, the Rim Line Road", )
road("Shale", "Bend (outside)", 12, 45, "Century Drive")
road("Shale", "Faust", 44, 45, "Forest Road 51, the Rim Line Road")
road("Faust", "Willamette Pass", 18, 50, "county road and OR 58")
road("Faust", "Chemult (outside)", 24, 55, "county road, OR 58 and US 97")
road("Chemult (outside)", "Bend (outside)", 62, 60, "US 97")
road("Willamette Pass", "Chemult (outside)", 26, 55, "OR 58 and US 97")

# --- South Divide -----------------------------------------------------------
road("OR 58 junction (outside)", "West Wild", 30, 55, "OR 58")
road("West Wild", "Nela Junction", 4, 45, "OR 58")
road("Nela Junction", "East Wild", 2, 40, "OR 58")
road("East Wild", "Willamette Pass", 25, 50, "OR 58")
road("Nela Junction", "Veilwood", 11, 30, "Forest Road 42, Nela Road")
road("Nela Junction", "Saltlick Grade turn", 58, 30, "Forest Road 41, Saltlick Grade")
road("East Wild", "Divide Road fork", 9, 40, "Forest Road 44, the Divide Road")
road("Divide Road fork", "Fold Creek", 6, 30, "Fold Creek Road (Nation road)")
road("Divide Road fork", "Isalune's Hush", 39, 35, "Forest Road 44, the Divide Road")
road("Isalune's Hush", "Faust", 34, 30, "Forest Road 45, over Windigo Pass")

SUMMER_ONLY = {"Forest Road 41, Saltlick Grade", "Forest Road 51, the Rim Line Road",
               "Forest Road 45, over Windigo Pass"}
FLOODS = {"the Old Grade (OR 126)"}

def graph(season="summer", outside=True, old_grade=True):
    g = {}
    for a, b, mi, mph, note in E:
        if season == "winter" and note in SUMMER_ONLY:
            continue
        if not old_grade and note in FLOODS:
            continue
        if not outside and ("(outside)" in a or "(outside)" in b):
            continue
        t = mi / mph * 60
        g.setdefault(a, []).append((b, mi, t))
        g.setdefault(b, []).append((a, mi, t))
    return g

def route(g, s, d):
    pq, seen = [(0, 0, s, [s])], set()
    while pq:
        t, mi, n, path = heapq.heappop(pq)
        if n == d:
            return t, mi, path
        if n in seen:
            continue
        seen.add(n)
        for m, dm, dt in g.get(n, []):
            if m not in seen:
                heapq.heappush(pq, (t + dt, mi + dm, m, path + [m]))
    return None

def r5(t):  # round to 5 minutes, written the way people say it
    t = int(5 * round(t / 5))
    h, m = divmod(t, 60)
    return f"{h} hr {m:02d} min" if h else f"{m} min"

TOWNS = ["Neptune (Mile 0)", "Ichabod's Eye", "Wrack", "Loki's Weir", "Camp Nine", "Amity Gate",
         "Honey Hills", "Sweetbriar (west)", "Five Fords (ranger station)", "Lake Varuna",
         "Sump Creek Settlement", "Mirth", "Cadence", "Shale", "Faust", "West Wild", "East Wild",
         "Nela Junction", "Veilwood", "Fold Creek", "Isalune's Hush"]
HUBS = ["Neptune (Mile 0)", "Amity Gate", "Cadence", "East Wild"]

if __name__ == "__main__":
    inside = graph("summer", outside=False)
    print("== In-region drive (summer, never leaving the region) ==")
    for t in TOWNS:
        row = []
        for h in HUBS:
            r = route(inside, t, h)
            row.append(f"{r5(r[0])} ({round(r[1])} mi)" if r else "—")
        print(t, "|", " | ".join(row))
    print("\n== Fastest, any road, summer / winter ==")
    for season in ("summer", "winter"):
        g = graph(season)
        for t in TOWNS:
            row = []
            for h in HUBS:
                r = route(g, t, h)
                row.append(f"{r5(r[0])} ({round(r[1])})")
            print(season, t, "|", " | ".join(row))
    g = graph("summer")
    print("\n== Key checks ==")
    for a, b in [("Loki's Weir", "Five Fords (Blue River end)"), ("Mirth", "Cadence (west, UGNC)"),
                 ("Mirth", "Amity Gate"), ("Neptune (Mile 0)", "Cadence"),
                 ("Neptune (Mile 0)", "Eugene (outside)"), ("East Wild", "Five Fords (ranger station)"),
                 ("Amity Gate", "Portland Airport (outside)"), ("Cadence", "Portland Airport (outside)"),
                 ("Amity Gate", "Eugene Airport (outside)"), ("Cadence", "Redmond Airport (outside)"),
                 ("Neptune (Mile 0)", "Eugene Airport (outside)"), ("East Wild", "Eugene Airport (outside)"),
                 ("Neptune (Mile 0)", "Portland Airport (outside)"), ("Cadence", "Eugene Airport (outside)"), ("East Wild", "Chemult (outside)"), ("Mirth", "Eugene Airport (outside)"), ("Mirth", "Portland Airport (outside)"), ("Shale", "Redmond Airport (outside)"), ("Faust", "Redmond Airport (outside)"), ("Sump Creek Settlement", "Portland Airport (outside)"), ("Cadence", "Bend (outside)"), ("Neptune (Mile 0)", "Newport (outside)"), ("Neptune (Mile 0)", "Coos Bay (outside)")]:
        for label, gg in (("any road", g), ("in-region", graph("summer", outside=False))):
            r = route(gg, a, b)
            print(f"{a} -> {b} [{label}]:", (r5(r[0]), round(r[1]), " > ".join(r[2])) if r else "no in-region road")
    w = graph("winter")
    for a, b in [("East Wild", "Five Fords (ranger station)"), ("Faust", "Cadence"), ("Isalune's Hush", "Cadence"), ("Faust", "East Wild"), ("Shale", "East Wild")]:
        r = route(w, a, b)
        print("WINTER", a, "->", b, r5(r[0]), round(r[1]), " > ".join(r[2]))
    nog = graph("winter", old_grade=False)
    r = route(nog, "Neptune (Mile 0)", "Eugene (outside)")
    print("Old Grade flooded: Neptune -> Eugene", r5(r[0]), round(r[1]), " > ".join(r[2]))

def md_table():
    names = {"Neptune (Mile 0)": "The city of Neptune", "Sweetbriar (west)": "Sweetbriar",
             "Five Fords (ranger station)": "Five Fords", "Sump Creek Settlement": "Sump Creek Settlement",
             "East Wild": "East Wild"}
    g = graph("summer")
    lines = ["| **From** | **To the city of Neptune** | **To Amity Gate** | **To Cadence** | **To East Wild** |",
             "| --- | --- | --- | --- | --- |"]
    for t in TOWNS:
        cells = []
        for h in HUBS:
            if t == h:
                cells.append("—")
                continue
            tm, mi, path = route(g, t, h)
            out = any("(outside)" in p for p in path)
            cells.append(f"{r5(tm)}, {round(mi)} mi{' †' if out else ''}")
        lines.append(f"| {names.get(t, t)} | " + " | ".join(cells) + " |")
    return "\n".join(lines)

if __name__ == "__main__" and len(__import__('sys').argv) > 1:
    print(md_table())
