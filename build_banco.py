import csv
import json
import os
import re

CUTOFF = "2026-11-24"

with open("devo_mb_tracks.json", "r", encoding="utf-8") as f:
    mb_albums = json.load(f)

with open("devo_mb_release_groups.json", "r", encoding="utf-8") as f:
    mb_rgs = json.load(f)

with open("devo_youtube_links.json", "r", encoding="utf-8") as f:
    yt_links = json.load(f)

yt_by_title = {lk["title"].lower(): lk["url"] for lk in yt_links}

def slugify(text):
    s = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    return re.sub(r"[\s_]+", "-", s)

sources = [
    {"id": "s_mb_artist", "url": "https://musicbrainz.org/artist/d2db1078-c170-4e22-b261-14f3ad60a690", "title": "MusicBrainz: Devo (Artist)", "type": "base_discografica", "consulted_on": CUTOFF, "status": "consultada"},
    {"id": "s_mb_rgs", "url": "https://musicbrainz.org/ws/2/release-group?artist=d2db1078-c170-4e22-b261-14f3ad60a690", "title": "MusicBrainz API: Devo Release Groups & Tracklists", "type": "base_discografica", "consulted_on": CUTOFF, "status": "consultada"},
    {"id": "s_wiki_devo", "url": "https://en.wikipedia.org/wiki/Devo", "title": "Wikipedia: Devo", "type": "enciclopedia", "consulted_on": CUTOFF, "status": "consultada"},
    {"id": "s_wiki_discog", "url": "https://en.wikipedia.org/wiki/Devo_discography", "title": "Wikipedia: Devo discography", "type": "enciclopedia", "consulted_on": CUTOFF, "status": "consultada"},
    {"id": "s_clubdevo", "url": "https://clubdevo.com/", "title": "Club Devo — Official Website", "type": "oficial", "consulted_on": CUTOFF, "status": "consultada"},
    {"id": "s_discogs", "url": "https://www.discogs.com/artist/12834-Devo", "title": "Discogs: Devo", "type": "base_discografica", "consulted_on": CUTOFF, "status": "consultada"},
    {"id": "s_yt_search", "url": "https://www.youtube.com/results?search_query=Devo", "title": "YouTube: Resultados de busca para faixas do Devo", "type": "plataforma_midia", "consulted_on": CUTOFF, "status": "consultada"},
]

people = [
    {
        "id": "p_mark", "name": "Mark Mothersbaugh", "roles": ["vocal", "teclados", "sintetizador", "guitarra"], "membership": "oficial",
        "bio": "Co-fundador do Devo (1973), vocalista principal, tecladista e compositor.",
        "career_phases": {"antes": "Flaming Youth (banda estudantil em Ohio, início dos anos 1970).", "durante": "Devo (1973–1991, 1996–presente).", "depois": "Fundador da Mutato Muzika (1989–presente); trilhas para cinema/TV (Wes Anderson, Rugrats); The Wipeouters (2001)."},
        "source_ids": ["s_wiki_devo", "s_mb_artist"]
    },
    {
        "id": "p_jerry", "name": "Gerald Casale", "roles": ["baixo", "vocal", "teclados"], "membership": "oficial",
        "bio": "Co-fundador do Devo (1973), baixista, vocalista, letrista e diretor de videoclipes.",
        "career_phases": {"antes": "15-60-75 (The Numbers Band) em Kent, Ohio (início dos anos 1970).", "durante": "Devo (1973–1991, 1996–presente).", "depois": "Jihad Jerry & the Evildoers (2006); direção de videoclipes e comerciais."},
        "source_ids": ["s_wiki_devo", "s_mb_artist"]
    },
    {
        "id": "p_bob1", "name": "Bob Mothersbaugh", "roles": ["guitarra solo", "vocal"], "membership": "oficial",
        "bio": "Conhecido como Bob 1; guitarrista solo do Devo desde 1974.",
        "career_phases": {"antes": "Bandas locais de Ohio antes de 1974.", "durante": "Devo (1974–1991, 1996–presente).", "depois": "The Wipeouters (2001); trabalhos de produção e trilhas na Mutato Muzika."},
        "source_ids": ["s_wiki_devo", "s_mb_artist"]
    },
    {
        "id": "p_bob2", "name": "Bob Casale", "roles": ["guitarra base", "teclados", "vocal de apoio"], "membership": "ex-integrante",
        "bio": "Conhecido como Bob 2; guitarrista e tecladista do Devo até seu falecimento em 2014.",
        "career_phases": {"antes": "Atuação técnica/musical em Ohio antes de 1973.", "durante": "Devo (1973–1974, 1976–1991, 1996–2014).", "depois": "The Wipeouters (2001); engenheiro de som e produtor (falecido em 2014)."},
        "source_ids": ["s_wiki_devo", "s_mb_artist"]
    },
    {
        "id": "p_alan", "name": "Alan Myers", "roles": ["bateria", "percussão"], "membership": "ex-integrante",
        "bio": "Baterista da formação clássica do Devo (1976–1986), falecido em 2013.",
        "career_phases": {"antes": "Cena de jazz-fusion em Ohio antes de 1976.", "durante": "Devo (1976–1986).", "depois": "Jean-Luc Ponty Band (1987–1989); Babooshka; Skyline Electric (falecido em 2013)."},
        "source_ids": ["s_wiki_devo", "s_mb_artist"]
    },
    {
        "id": "p_david", "name": "David Kendrick", "roles": ["bateria"], "membership": "ex-integrante",
        "bio": "Baterista do Devo (1987–1991, 1996–2004).",
        "career_phases": {"antes": "Gleaming Spires (1980–1988) e Sparks (1981–1986).", "durante": "Devo (1987–1991, 1996–2004).", "depois": "Projetos de estúdio e colaborações independentes."},
        "source_ids": ["s_wiki_devo", "s_mb_artist"]
    },
    {
        "id": "p_joshf", "name": "Josh Freese", "roles": ["bateria", "percussão"], "membership": "oficial",
        "bio": "Baterista do Devo desde 1996.",
        "career_phases": {"antes": "The Vandals (desde 1989); baterista de sessão em Los Angeles.", "durante": "Devo (1996–presente).", "depois": "A Perfect Circle (1999–2012), Nine Inch Nails, Weezer, Foo Fighters (2023–presente)."},
        "source_ids": ["s_wiki_devo", "s_mb_artist"]
    },
    {
        "id": "p_joshh", "name": "Josh Hager", "roles": ["guitarra base", "teclados"], "membership": "oficial",
        "bio": "Guitarrista e tecladista do Devo desde 2014.",
        "career_phases": {"antes": "The Elevator Drops (1994–2001); Garvy J.", "durante": "Devo (2014–presente).", "depois": "Ativo no Devo e em projetos de estúdio."},
        "source_ids": ["s_wiki_devo"]
    },
    {
        "id": "p_bobl", "name": "Bob Lewis", "roles": ["guitarra"], "membership": "ex-integrante",
        "bio": "Co-fundador conceitual do Devo em 1973 na Kent State University.",
        "career_phases": {"antes": "Estudante de arte na Kent State University.", "durante": "Devo (1973–1974).", "depois": "Carreira fora da banda após 1974."},
        "source_ids": ["s_wiki_devo"]
    },
    {
        "id": "p_jimm", "name": "Jim Mothersbaugh", "roles": ["bateria eletrônica"], "membership": "ex-integrante",
        "bio": "Baterista dos primeiros anos do Devo (1974–1975).",
        "career_phases": {"antes": "Irmão de Mark e Bob Mothersbaugh em Ohio.", "durante": "Devo (1974–1975).", "depois": "Engenheiro de áudio e desenvolvedor de tecnologia musical (Roland)."},
        "source_ids": ["s_wiki_devo"]
    },
    {
        "id": "p_rod", "name": "Rod Reisman", "roles": ["bateria"], "membership": "ex-integrante",
        "bio": "Baterista na formação inicial de 1973.",
        "career_phases": {"antes": "Cena universitária de Kent, Ohio.", "durante": "Devo (1973).", "depois": "Sem registros musicais posteriores ligados ao Devo."},
        "source_ids": ["s_wiki_devo"]
    },
    {
        "id": "p_fred", "name": "Fred Weber", "roles": ["vocal"], "membership": "ex-integrante",
        "bio": "Vocalista na formação inicial de 1973.",
        "career_phases": {"antes": "Cena universitária de Kent, Ohio.", "durante": "Devo (1973).", "depois": "Sem registros musicais posteriores ligados ao Devo."},
        "source_ids": ["s_wiki_devo"]
    },
    {"id": "p_eno", "name": "Brian Eno", "roles": ["produção"], "membership": "produtor", "bio": "Produtor do álbum de estreia Q: Are We Not Men? A: We Are Devo! (1978).", "career_phases": {"antes": "Roxy Music (1971–1973).", "durante": "Produção de Q: Are We Not Men? (1978).", "depois": "Carreira solo e produção (U2, Talking Heads, Coldplay)."}, "source_ids": ["s_wiki_devo", "s_discogs"]},
    {"id": "p_kenscott", "name": "Ken Scott", "roles": ["produção"], "membership": "produtor", "bio": "Produtor de Duty Now for the Future (1979).", "career_phases": {"antes": "Engenheiro dos Beatles e produtor de David Bowie.", "durante": "Produção de Duty Now for the Future (1979).", "depois": "Produção e engenharia de áudio."}, "source_ids": ["s_discogs"]},
    {"id": "p_margouleff", "name": "Robert Margouleff", "roles": ["produção"], "membership": "produtor", "bio": "Co-produtor de Freedom of Choice (1980).", "career_phases": {"antes": "Tonto's Expanding Head Band e Stevie Wonder.", "durante": "Co-produção de Freedom of Choice (1980).", "depois": "Produção musical e design de som."}, "source_ids": ["s_discogs"]},
    {"id": "p_rtb", "name": "Roy Thomas Baker", "roles": ["produção"], "membership": "produtor", "bio": "Produtor de Oh, No! It's Devo (1982).", "career_phases": {"antes": "Queen, The Cars.", "durante": "Produção de Oh, No! It's Devo (1982).", "depois": "Produção de rock/new wave."}, "source_ids": ["s_discogs"]},
]

projects = [
    {"id": "proj_devo", "name": "Devo", "kind": "banda"},
    {"id": "proj_mutato", "name": "Mutato Muzika", "kind": "produtora"},
    {"id": "proj_jihad", "name": "Jihad Jerry & the Evildoers", "kind": "solo"},
    {"id": "proj_wipeouters", "name": "The Wipeouters", "kind": "projeto_paralelo"},
    {"id": "proj_vandals", "name": "The Vandals", "kind": "banda"},
    {"id": "proj_apc", "name": "A Perfect Circle", "kind": "banda"},
    {"id": "proj_sparks", "name": "Sparks", "kind": "banda"},
    {"id": "proj_gleaming", "name": "Gleaming Spires", "kind": "banda"},
    {"id": "proj_ponty", "name": "Jean-Luc Ponty Band", "kind": "banda"},
    {"id": "proj_elevator", "name": "The Elevator Drops", "kind": "banda"},
]

relations = []
rel_idx = 1

def add_rel(person_id, project_id, kind, grain, instrument, start, end, source_ids, evidence, status="confirmado"):
    global rel_idx
    relations.append({
        "id": f"r_{rel_idx:04d}",
        "person_id": person_id,
        "project_id": project_id,
        "kind": kind,
        "grain": grain,
        "instrument": instrument,
        "start": start,
        "end": end,
        "source_ids": source_ids,
        "evidence": evidence,
        "status": status,
    })
    rel_idx += 1

band_periods = [
    ("p_mark", "vocal/teclados", 1973, 1991), ("p_mark", "vocal/teclados", 1996, 2026),
    ("p_jerry", "baixo/vocal", 1973, 1991), ("p_jerry", "baixo/vocal", 1996, 2026),
    ("p_bob1", "guitarra solo", 1974, 1991), ("p_bob1", "guitarra solo", 1996, 2026),
    ("p_bob2", "guitarra base/teclados", 1973, 1974), ("p_bob2", "guitarra base/teclados", 1976, 1991), ("p_bob2", "guitarra base/teclados", 1996, 2014),
    ("p_alan", "bateria", 1976, 1986),
    ("p_david", "bateria", 1987, 1991), ("p_david", "bateria", 1996, 2004),
    ("p_joshf", "bateria", 1996, 2026),
    ("p_joshh", "guitarra base/teclados", 2014, 2026),
    ("p_bobl", "guitarra", 1973, 1974),
    ("p_jimm", "bateria eletrônica", 1974, 1975),
    ("p_rod", "bateria", 1973, 1973),
    ("p_fred", "vocal", 1973, 1973),
]
for pid, inst, s, e in band_periods:
    add_rel(pid, "proj_devo", "integrante", "projeto", inst, s, e, ["s_wiki_devo", "s_mb_artist"], f"Período oficial documentado ({s}–{e}) na formação do Devo.")

external_rels = [
    ("p_mark", "proj_mutato", "fundador", "projeto", "composição/produção", 1989, 2026, "Fundador da produtora Mutato Muzika."),
    ("p_jerry", "proj_jihad", "solo", "projeto", "vocal/baixo", 2006, 2006, "Projeto solo Jihad Jerry & the Evildoers (2006)."),
    ("p_mark", "proj_wipeouters", "integrante", "projeto", "teclados/guitarra", 2001, 2001, "Projeto paralelo surf-rock The Wipeouters (2001)."),
    ("p_bob1", "proj_wipeouters", "integrante", "projeto", "guitarra", 2001, 2001, "Projeto paralelo surf-rock The Wipeouters (2001)."),
    ("p_bob2", "proj_wipeouters", "integrante", "projeto", "guitarra", 2001, 2001, "Projeto paralelo surf-rock The Wipeouters (2001)."),
    ("p_joshf", "proj_vandals", "integrante", "projeto", "bateria", 1989, 2026, "Baterista de longa data do The Vandals."),
    ("p_joshf", "proj_apc", "integrante", "projeto", "bateria", 1999, 2012, "Baterista do A Perfect Circle."),
    ("p_david", "proj_sparks", "integrante", "projeto", "bateria", 1981, 1986, "Baterista do Sparks antes de ingressar no Devo."),
    ("p_david", "proj_gleaming", "integrante", "projeto", "bateria", 1980, 1988, "Integrante do Gleaming Spires."),
    ("p_alan", "proj_ponty", "integrante", "projeto", "bateria", 1987, 1989, "Colaboração com Jean-Luc Ponty após saída do Devo."),
    ("p_joshh", "proj_elevator", "integrante", "projeto", "guitarra/vocal", 1994, 2001, "Integrante do The Elevator Drops."),
]
for pid, prj, kind, grain, inst, s, e, ev in external_rels:
    add_rel(pid, prj, kind, grain, inst, s, e, ["s_wiki_devo"], ev)

releases = []
lyrics = []
producers_by_album = {
    "Q: Are We Not Men? A: We Are Devo!": ("p_eno", 1978),
    "Duty Now for the Future": ("p_kenscott", 1979),
    "Freedom of Choice": ("p_margouleff", 1980),
    "Oh, No! It's Devo": ("p_rtb", 1982),
}

lyr_idx = 1
for idx, alb in enumerate(mb_albums, start=1):
    alb_id = f"proj_alb_{idx}"
    rel_id = f"rel_{idx}"
    year = int(alb["date"][:4])
    projects.append({"id": alb_id, "name": alb["title"], "kind": "álbum"})
    releases.append({
        "id": rel_id,
        "project_id": "proj_devo",
        "title": alb["title"],
        "kind": alb["kind"],
        "year": year,
        "date": alb["date"],
        "tracks": [t["title"] for t in alb["tracks"]],
        "source_ids": ["s_mb_rgs", "s_wiki_discog"],
        "status": "confirmado",
    })
    if alb["title"] in producers_by_album:
        prod_id, py = producers_by_album[alb["title"]]
        add_rel(prod_id, alb_id, "produção", "lançamento", "produção", py, py, ["s_discogs", "s_wiki_discog"], f"Produção creditada no álbum {alb['title']} ({py}).")

    for tidx, tr in enumerate(alb["tracks"], start=1):
        trk_id = f"proj_trk_{idx}_{tidx}"
        projects.append({"id": trk_id, "name": f"{tr['title']} ({alb['title']})", "kind": "faixa"})
        add_rel("p_mark", trk_id, "intérprete", "faixa", "vocal/teclados", year, year, ["s_mb_rgs"], f"Faixa de {alb['title']} ({year}) registrada no MusicBrainz.")
        add_rel("p_jerry", trk_id, "intérprete", "faixa", "baixo/vocal", year, year, ["s_mb_rgs"], f"Faixa de {alb['title']} ({year}) registrada no MusicBrainz.")
        lyrics.append({
            "id": f"lyr_{lyr_idx:03d}",
            "title": tr["title"],
            "url": f"https://genius.com/Devo-{slugify(tr['title'])}-lyrics",
            "license_status": "desconhecido",
            "source_ids": ["s_wiki_discog"],
        })
        lyr_idx += 1

# Add Live/Compilation
extra_releases = [
    ("rel_10", "DEV-O Live", "ao_vivo", 1981, "1981", ["Freedom of Choice", "Whip It", "Girl U Want", "Gates of Steel"]),
    ("rel_11", "Now It Can Be Told: DEVO at the Palace", "ao_vivo", 1989, "1989", ["Jerkin' Back 'n' Forth", "Jocko Homo", "Mongoloid"]),
    ("rel_12", "Hardcore Devo, Vol. 1", "coletânea", 1990, "1990", ["Mechanical Man", "Auto Modown", "Space Girl Blues"]),
    ("rel_13", "50 Years of De-Evolution (1973–2023)", "coletânea", 2023, "2023-10-20", ["Jocko Homo", "Whip It", "Beautiful World", "Fresh"]),
]
for rid, title, kind, y, d, trs in extra_releases:
    releases.append({"id": rid, "project_id": "proj_devo", "title": title, "kind": kind, "year": y, "date": d, "tracks": trs, "source_ids": ["s_clubdevo", "s_wiki_discog"], "status": "confirmado"})

# Add EPs & Singles from MusicBrainz
rel_counter = 14
for rg in sorted(mb_rgs, key=lambda x: x.get("first-release-date", "") or "9999"):
    ptype = rg.get("primary-type")
    if ptype not in ("EP", "Single"):
        continue
    d = rg.get("first-release-date", "")
    y = int(d[:4]) if d and d[:4].isdigit() else None
    releases.append({
        "id": f"rel_{rel_counter}",
        "project_id": "proj_devo",
        "title": rg["title"],
        "kind": "ep" if ptype == "EP" else "single",
        "year": y,
        "date": d or None,
        "tracks": [rg["title"]],
        "source_ids": ["s_mb_rgs"],
        "status": "confirmado",
    })
    rel_counter += 1

links = []
for idx, lk in enumerate(yt_links, start=1):
    links.append({
        "id": f"lk_{idx:03d}",
        "title": f"{lk['title']} — {lk['album']}",
        "url": lk["url"],
        "direct": True,
        "recording_id": lk["recording_id"],
        "source_ids": ["s_yt_search", "s_mb_rgs"],
        "status": "não_verificado",
    })

timeline = [
    {"year": 1973, "title": "Formação na Kent State University", "detail": "Gerald Casale, Mark Mothersbaugh e Bob Lewis formam o Devo em Akron/Kent, Ohio."},
    {"year": 1978, "title": "Álbum de estreia produzido por Brian Eno", "detail": "Lançamento de Q: Are We Not Men? A: We Are Devo! pela Warner Bros."},
    {"year": 1980, "title": "Freedom of Choice e Whip It", "detail": "Maior sucesso comercial da banda, alcançando platina nos EUA."},
    {"year": 1991, "title": "Hiato da banda", "detail": "Encerramento temporário das atividades após Smooth Noodle Maps."},
    {"year": 1996, "title": "Retorno com Josh Freese", "detail": "Reunião para turnês e projetos multimídia."},
    {"year": 2010, "title": "Something for Everybody", "detail": "Primeiro álbum de estúdio em 20 anos."},
    {"year": 2014, "title": "Falecimento de Bob Casale (Bob 2)", "detail": "Josh Hager assume guitarra base e teclados."},
    {"year": 2023, "title": "50 Years of De-Evolution", "detail": "Lançamento comemorativo dos 50 anos da banda."},
]

limitations = [
    "Links diretos do YouTube obtidos por busca automatizada sem verificação manual de reprodução/disponibilidade regional.",
    "Créditos em nível de faixa atribuídos aos membros nucleares da respectiva era com base nos álbuns oficiais do MusicBrainz.",
    "Letras integrais protegidas não são distribuídas; apenas links externos com licença marcada como desconhecida.",
]

banco = {
    "cutoff": CUTOFF,
    "people": people,
    "projects": projects,
    "relations": relations,
    "releases": releases,
    "links": links,
    "sources": sources,
    "lyrics": lyrics,
    "timeline": timeline,
    "limitations": limitations,
}

with open("banco.json", "w", encoding="utf-8") as f:
    json.dump(banco, f, ensure_ascii=False, indent=2)

os.makedirs("csv", exist_ok=True)
def safe_cell(val):
    if isinstance(val, (list, dict)):
        s = json.dumps(val, ensure_ascii=False)
    elif val is None:
        s = ""
    else:
        s = str(val)
    if s and s[0] in ("=", "+", "-", "@"):
        s = "'" + s
    return s

for col in ["people", "projects", "relations", "releases", "links", "sources", "lyrics"]:
    rows = banco[col]
    if not rows:
        continue
    fieldnames = list(rows[0].keys())
    with open(f"csv/{col}.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: safe_cell(r.get(k)) for k in fieldnames})

print(f"Generated banco.json: {len(people)} people, {len(projects)} projects, {len(relations)} relations, {len(releases)} releases, {len(links)} links, {len(lyrics)} lyrics.")
