import json

with open("banco.json", "r", encoding="utf-8") as f:
    banco_str = f.read()

html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Atlas Musical Auditável — DEVO</title>
  <style>
    :root {
      --bg: #090b10;
      --surface: #121620;
      --surface-2: #1a202e;
      --surface-3: #232b3d;
      --text: #f8fafc;
      --muted: #94a3b8;
      --accent: #e11d48;
      --accent-glow: rgba(225, 29, 72, 0.25);
      --yellow: #facc15;
      --yellow-dim: rgba(250, 204, 21, 0.14);
      --border: #262f42;
      --ok: #22c55e;
      --warn: #f59e0b;
      --radius: 12px;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      background: radial-gradient(circle at top right, #1e1118 0%, var(--bg) 45%);
      color: var(--text);
      line-height: 1.55;
      overflow-x: hidden;
    }
    a { color: var(--yellow); text-decoration: none; }
    a:hover { text-decoration: underline; }
    a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible {
      outline: 2px solid var(--yellow);
      outline-offset: 2px;
    }
    header {
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(18, 22, 32, 0.88);
      backdrop-filter: blur(12px);
      border-bottom: 2px solid var(--accent);
      box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    }
    .container { max-width: 1320px; margin: 0 auto; padding: 1rem 1.25rem; }
    .brand-row { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 0.75rem; }
    .brand-title { display: flex; align-items: center; gap: 0.75rem; }
    .dome-icon {
      width: 34px; height: 28px;
      background: linear-gradient(180deg, #f43f5e 0%, #be123c 100%);
      clip-path: polygon(20% 0%, 80% 0%, 92% 35%, 100% 100%, 0% 100%, 8% 35%);
      box-shadow: 0 0 14px var(--accent-glow);
      flex-shrink: 0;
    }
    h1 { margin: 0; font-size: 1.45rem; letter-spacing: -0.02em; }
    .subtitle { color: var(--muted); font-size: 0.88rem; }
    nav {
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
      margin-top: 0.85rem;
    }
    .tab-btn {
      background: var(--surface-2);
      color: var(--muted);
      border: 1px solid var(--border);
      padding: 0.48rem 0.9rem;
      border-radius: 999px;
      cursor: pointer;
      font-size: 0.85rem;
      font-weight: 500;
      transition: all 0.18s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }
    .tab-btn:hover { color: var(--text); border-color: var(--muted); }
    .tab-btn[aria-selected="true"] {
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
      box-shadow: 0 0 14px var(--accent-glow);
      font-weight: 600;
    }
    .tab-count {
      background: rgba(0,0,0,0.28);
      padding: 0.1rem 0.45rem;
      border-radius: 999px;
      font-size: 0.72rem;
    }
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 0.9rem;
      margin: 1rem 0;
    }
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
      gap: 1rem;
      margin: 1rem 0;
    }
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.1rem;
      transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease;
    }
    .card:hover {
      border-color: #3b4761;
      box-shadow: 0 8px 24px rgba(0,0,0,0.28);
    }
    .metric-val { font-size: 2rem; font-weight: 800; color: var(--yellow); letter-spacing: -0.03em; }
    .metric-lbl { font-size: 0.82rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; }
    .filters {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 0.65rem;
      margin-bottom: 1rem;
      background: var(--surface);
      padding: 0.95rem;
      border-radius: var(--radius);
      border: 1px solid var(--border);
    }
    .filters input, .filters select, .filters button {
      width: 100%;
      padding: 0.52rem 0.75rem;
      background: var(--surface-2);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 0.88rem;
    }
    .filters button {
      cursor: pointer;
      background: var(--accent);
      border-color: var(--accent);
      font-weight: 600;
      transition: opacity 0.15s;
    }
    .filters button:hover { opacity: 0.9; }
    .table-wrap { overflow-x: auto; border: 1px solid var(--border); border-radius: var(--radius); background: var(--surface); }
    table { width: 100%; border-collapse: collapse; font-size: 0.86rem; }
    th, td { padding: 0.65rem 0.85rem; border-bottom: 1px solid var(--border); text-align: left; }
    th { background: var(--surface-2); position: sticky; top: 0; font-weight: 600; color: var(--muted); text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.04em; }
    tr:hover td { background: rgba(255,255,255,0.02); }
    .badge {
      display: inline-block;
      padding: 0.16rem 0.5rem;
      border-radius: 999px;
      font-size: 0.74rem;
      font-weight: 600;
      background: var(--surface-2);
      border: 1px solid var(--border);
    }
    .badge-ok { border-color: rgba(34,197,94,0.4); color: var(--ok); background: rgba(34,197,94,0.1); }
    .badge-warn { border-color: rgba(245,158,11,0.4); color: var(--warn); background: rgba(245,158,11,0.1); }
    .badge-type { border-color: rgba(250,204,21,0.4); color: var(--yellow); background: var(--yellow-dim); text-transform: uppercase; }
    .panel { display: none; animation: fadeIn 0.2s ease; }
    .panel.active { display: block; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
    .phase-box {
      margin-top: 0.75rem;
      padding-top: 0.75rem;
      border-top: 1px solid var(--border);
      display: grid;
      gap: 0.45rem;
      font-size: 0.83rem;
    }
    .phase-step {
      padding-left: 0.65rem;
      border-left: 2px solid var(--accent);
    }
    .phase-step strong { color: var(--yellow); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.03em; display: block; }
    .track-list {
      list-style: decimal;
      padding-left: 1.25rem;
      margin: 0.65rem 0 0;
      font-size: 0.83rem;
      max-height: 260px;
      overflow-y: auto;
    }
    .track-list li {
      padding: 0.25rem 0;
      border-bottom: 1px dashed rgba(255,255,255,0.06);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
    }
    .track-actions { display: inline-flex; gap: 0.35rem; flex-shrink: 0; }
    .pill-link {
      font-size: 0.72rem;
      padding: 0.14rem 0.45rem;
      border-radius: 6px;
      background: var(--surface-2);
      border: 1px solid var(--border);
      color: var(--text);
      text-decoration: none;
    }
    .pill-link:hover { border-color: var(--yellow); color: var(--yellow); text-decoration: none; }
    .pill-play { border-color: rgba(225,29,72,0.5); color: #fda4af; }
    .pill-play:hover { background: var(--accent); color: #fff; border-color: var(--accent); }
    .timeline-list { display: grid; gap: 0.75rem; }
    .timeline-item {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 4px solid var(--yellow);
      padding: 0.9rem 1.1rem;
      border-radius: var(--radius);
      cursor: pointer;
      transition: transform 0.15s, background 0.15s;
    }
    .timeline-item:hover { background: var(--surface-2); transform: translateX(4px); }
    #network-svg {
      width: 100%;
      height: 440px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
    }
    .empty-state {
      padding: 2.5rem;
      text-align: center;
      color: var(--muted);
      background: var(--surface);
      border: 1px dashed var(--border);
      border-radius: var(--radius);
    }
    .export-bar { display: flex; flex-wrap: wrap; gap: 0.55rem; margin-top: 0.75rem; }
    .btn-sec {
      background: var(--surface-2);
      color: var(--text);
      border: 1px solid var(--border);
      padding: 0.5rem 0.9rem;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.85rem;
      font-weight: 500;
      transition: border-color 0.15s;
    }
    .btn-sec:hover { border-color: var(--yellow); color: var(--yellow); }
  </style>
</head>
<body>
  <header>
    <div class="container">
      <div class="brand-row">
        <div class="brand-title">
          <div class="dome-icon" aria-hidden="true"></div>
          <div>
            <h1>Atlas Musical Auditável: DEVO</h1>
            <div class="subtitle" id="cutoff-label"></div>
          </div>
        </div>
      </div>
      <nav role="tablist" aria-label="Módulos do Atlas" id="main-tabs">
        <button class="tab-btn" role="tab" aria-selected="true" data-tab="overview">Visão Geral</button>
        <button class="tab-btn" role="tab" aria-selected="false" data-tab="releases">Discografia <span class="tab-count" id="cnt-releases"></span></button>
        <button class="tab-btn" role="tab" aria-selected="false" data-tab="people">Biografias <span class="tab-count" id="cnt-people"></span></button>
        <button class="tab-btn" role="tab" aria-selected="false" data-tab="relations">Relações &amp; Filtros <span class="tab-count" id="cnt-relations"></span></button>
        <button class="tab-btn" role="tab" aria-selected="false" data-tab="timeline">Linha do Tempo</button>
        <button class="tab-btn" role="tab" aria-selected="false" data-tab="network">Rede</button>
        <button class="tab-btn" role="tab" aria-selected="false" data-tab="links">Links &amp; Fontes <span class="tab-count" id="cnt-links"></span></button>
      </nav>
    </div>
  </header>

  <main class="container">
    <section id="panel-overview" class="panel active">
      <div class="metrics-grid" id="metrics-grid"></div>
      <div class="card">
        <h3>Exportações Reais (JSON / CSV)</h3>
        <p class="subtitle">Geradas diretamente a partir do banco de dados incorporado, com neutralização de fórmulas para planilhas.</p>
        <div class="export-bar">
          <button class="btn-sec" id="dl-json">⬇ Baixar banco.json</button>
          <button class="btn-sec" id="dl-rel-csv">⬇ Baixar relations.csv</button>
          <button class="btn-sec" id="dl-people-csv">⬇ Baixar people.csv</button>
          <button class="btn-sec" id="dl-links-csv">⬇ Baixar links.csv</button>
        </div>
      </div>
      <div class="card" style="margin-top: 1rem;">
        <h3>Limitações e Escopo</h3>
        <ul id="limitations-list" style="margin:0.5rem 0 0;padding-left:1.25rem;color:var(--muted);font-size:0.9rem;"></ul>
      </div>
    </section>

    <section id="panel-releases" class="panel">
      <div class="filters">
        <select id="r-kind" aria-label="Filtrar por tipo de lançamento">
          <option value="">Todos os tipos (Álbuns, EPs, Singles, Ao Vivo)</option>
          <option value="álbum">Álbuns de Estúdio</option>
          <option value="ep">EPs</option>
          <option value="single">Singles</option>
          <option value="ao_vivo">Ao Vivo</option>
          <option value="coletânea">Coletâneas</option>
        </select>
        <input type="text" id="r-search" placeholder="Buscar álbum, single, EP ou faixa..." aria-label="Buscar lançamento" />
      </div>
      <div class="cards-grid" id="releases-grid"></div>
    </section>

    <section id="panel-people" class="panel">
      <div class="cards-grid" id="people-grid"></div>
    </section>

    <section id="panel-relations" class="panel">
      <div class="filters">
        <input type="text" id="f-search" placeholder="Buscar pessoa, projeto, instrumento..." aria-label="Buscar" />
        <select id="f-person" aria-label="Filtrar por pessoa"><option value="">Todas as pessoas</option></select>
        <select id="f-grain" aria-label="Filtrar por granularidade"><option value="">Todas granularidades</option></select>
        <select id="f-status" aria-label="Filtrar por status"><option value="">Todos os status</option></select>
        <button id="f-clear">Limpar filtros</button>
      </div>
      <div id="rel-count" class="subtitle" style="margin-bottom: 0.5rem;"></div>
      <div class="table-wrap" id="rel-table-wrap">
        <table>
          <thead>
            <tr><th>Pessoa</th><th>Projeto/Objeto</th><th>Vínculo</th><th>Granularidade</th><th>Instrumento</th><th>Período</th><th>Status</th></tr>
          </thead>
          <tbody id="rel-tbody"></tbody>
        </table>
      </div>
      <div id="rel-empty" class="empty-state" style="display:none;">Nenhuma relação encontrada com os filtros atuais.</div>
    </section>

    <section id="panel-timeline" class="panel">
      <p class="subtitle">Clique em um marco histórico para filtrar as relações daquele ano.</p>
      <div class="timeline-list" id="timeline-list"></div>
    </section>

    <section id="panel-network" class="panel">
      <p class="subtitle">Rede interativa de integrantes e projetos. Clique em um nó para destacar conexões e filtrar.</p>
      <svg id="network-svg" viewBox="0 0 800 440" role="img" aria-label="Grafo de relações do Devo"></svg>
      <div id="network-info" class="card" style="margin-top:0.75rem;">Selecione um nó no grafo acima para ver detalhes.</div>
    </section>

    <section id="panel-links" class="panel">
      <h3>Fontes Consultadas</h3>
      <div class="table-wrap" style="margin-bottom:1.25rem;">
        <table>
          <thead><tr><th>ID</th><th>Título</th><th>Tipo</th><th>Consulta</th><th>Status</th></tr></thead>
          <tbody id="sources-tbody"></tbody>
        </table>
      </div>
      <h3>Links Diretos (YouTube)</h3>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Faixa</th><th>Recording ID</th><th>URL</th><th>Status</th></tr></thead>
          <tbody id="links-tbody"></tbody>
        </table>
      </div>
    </section>
  </main>

  <script id="banco-data" type="application/json">__BANCO_JSON__</script>
  <script>
    const DB = JSON.parse(document.getElementById("banco-data").textContent);
    const peopleMap = Object.fromEntries(DB.people.map(p => [p.id, p]));
    const projMap = Object.fromEntries(DB.projects.map(p => [p.id, p]));

    document.getElementById("cutoff-label").textContent = `Corte: ${DB.cutoff} · ${DB.people.length} pessoas · ${DB.releases.length} lançamentos · ${DB.relations.length} relações · ${DB.links.length} links diretos`;
    document.getElementById("cnt-releases").textContent = DB.releases.length;
    document.getElementById("cnt-people").textContent = DB.people.length;
    document.getElementById("cnt-relations").textContent = DB.relations.length;
    document.getElementById("cnt-links").textContent = DB.links.length;

    const tabs = document.querySelectorAll(".tab-btn");
    const panels = document.querySelectorAll(".panel");
    function activateTab(name) {
      tabs.forEach(t => t.setAttribute("aria-selected", t.dataset.tab === name ? "true" : "false"));
      panels.forEach(p => p.classList.toggle("active", p.id === "panel-" + name));
    }
    tabs.forEach(t => t.addEventListener("click", () => activateTab(t.dataset.tab)));

    const metrics = [
      { lbl: "Pessoas", val: DB.people.length },
      { lbl: "Lançamentos", val: DB.releases.length },
      { lbl: "Relações Confirmadas", val: DB.relations.filter(r => r.status === "confirmado").length },
      { lbl: "Links Diretos Únicos", val: DB.links.length },
      { lbl: "Letras Online", val: (DB.lyrics || []).length },
      { lbl: "Fontes Consultadas", val: DB.sources.length }
    ];
    document.getElementById("metrics-grid").innerHTML = metrics.map(m =>
      `<div class="card"><div class="metric-val">${m.val}</div><div class="metric-lbl">${m.lbl}</div></div>`
    ).join("");
    document.getElementById("limitations-list").innerHTML = (DB.limitations || []).map(l => `<li>${l}</li>`).join("");

    // Releases
    const linkByTitle = Object.fromEntries(DB.links.map(l => [l.title.split(" — ")[0].toLowerCase(), l.url]));
    const lyricByTitle = Object.fromEntries((DB.lyrics || []).map(l => [l.title.toLowerCase(), l.url]));
    const rKind = document.getElementById("r-kind");
    const rSearch = document.getElementById("r-search");

    function renderReleases() {
      const k = rKind.value;
      const q = rSearch.value.trim().toLowerCase();
      const filtered = DB.releases.filter(r => {
        if (k && r.kind !== k) return false;
        if (q && !r.title.toLowerCase().includes(q) && !r.tracks.some(t => t.toLowerCase().includes(q))) return false;
        return true;
      });
      document.getElementById("releases-grid").innerHTML = filtered.map(r => `
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:0.5rem;">
            <h3 style="margin:0;font-size:1.05rem;">${r.title}</h3>
            <span class="badge badge-type">${r.kind}</span>
          </div>
          <div class="subtitle" style="margin-top:0.25rem;">Data: ${r.date || r.year || "—"} · ${r.tracks.length} faixa(s)</div>
          <ol class="track-list">
            ${r.tracks.map(t => {
              const yt = linkByTitle[t.toLowerCase()];
              const lyr = lyricByTitle[t.toLowerCase()];
              const ytSearch = `https://www.youtube.com/results?search_query=${encodeURIComponent('Devo ' + t)}`;
              return `<li>
                <span>${t}</span>
                <span class="track-actions">
                  ${yt ? `<a class="pill-link pill-play" href="${yt}" target="_blank" rel="noopener">▶ Ouvir</a>` : `<a class="pill-link" href="${ytSearch}" target="_blank" rel="noopener">🔍 YT</a>`}
                  ${lyr ? `<a class="pill-link" href="${lyr}" target="_blank" rel="noopener">♫ Letra</a>` : ""}
                </span>
              </li>`;
            }).join("")}
          </ol>
        </div>
      `).join("");
    }
    rKind.addEventListener("change", renderReleases);
    rSearch.addEventListener("input", renderReleases);
    renderReleases();

    // People
    document.getElementById("people-grid").innerHTML = DB.people.map(p => `
      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:0.5rem;">
          <h3 style="margin:0;">${p.name}</h3>
          <span class="badge ${p.membership === 'oficial' ? 'badge-ok' : ''}">${p.membership}</span>
        </div>
        <div class="subtitle" style="margin-top:0.2rem;">${(p.roles || []).join(" · ")}</div>
        <p style="font-size:0.85rem;margin:0.5rem 0 0;color:#cbd5e1;">${p.bio}</p>
        ${p.career_phases ? `
          <div class="phase-box">
            <div class="phase-step"><strong>Antes do Devo</strong>${p.career_phases.antes}</div>
            <div class="phase-step"><strong>No Devo</strong>${p.career_phases.durante}</div>
            <div class="phase-step"><strong>Depois / Paralelos</strong>${p.career_phases.depois}</div>
          </div>
        ` : ""}
      </div>
    `).join("");

    // Relations
    const fPerson = document.getElementById("f-person");
    const fGrain = document.getElementById("f-grain");
    const fStatus = document.getElementById("f-status");
    const fSearch = document.getElementById("f-search");
    DB.people.forEach(p => fPerson.add(new Option(p.name, p.id)));
    [...new Set(DB.relations.map(r => r.grain))].forEach(g => fGrain.add(new Option(g, g)));
    [...new Set(DB.relations.map(r => r.status))].forEach(s => fStatus.add(new Option(s, s)));

    function renderRelations(yearFilter = null) {
      const q = fSearch.value.trim().toLowerCase();
      const pid = fPerson.value;
      const gr = fGrain.value;
      const st = fStatus.value;
      const filtered = DB.relations.filter(r => {
        if (pid && r.person_id !== pid) return false;
        if (gr && r.grain !== gr) return false;
        if (st && r.status !== st) return false;
        if (yearFilter !== null && (r.start > yearFilter || (r.end && r.end < yearFilter))) return false;
        if (q) {
          const pName = (peopleMap[r.person_id]?.name || "").toLowerCase();
          const prName = (projMap[r.project_id]?.name || "").toLowerCase();
          const inst = (r.instrument || "").toLowerCase();
          if (!pName.includes(q) && !prName.includes(q) && !inst.includes(q)) return false;
        }
        return true;
      });
      document.getElementById("rel-count").textContent = `Exibindo ${filtered.length} de ${DB.relations.length} relações`;
      const tbody = document.getElementById("rel-tbody");
      const wrap = document.getElementById("rel-table-wrap");
      const empty = document.getElementById("rel-empty");
      if (filtered.length === 0) {
        wrap.style.display = "none"; empty.style.display = "block";
      } else {
        wrap.style.display = "block"; empty.style.display = "none";
        tbody.innerHTML = filtered.slice(0, 200).map(r => `
          <tr>
            <td>${peopleMap[r.person_id]?.name || r.person_id}</td>
            <td>${projMap[r.project_id]?.name || r.project_id}</td>
            <td>${r.kind}</td>
            <td><span class="badge">${r.grain}</span></td>
            <td>${r.instrument || "—"}</td>
            <td>${r.start ?? "?"}–${r.end ?? "atual"}</td>
            <td><span class="badge ${r.status === 'confirmado' ? 'badge-ok' : 'badge-warn'}">${r.status}</span></td>
          </tr>
        `).join("");
      }
    }
    [fPerson, fGrain, fStatus].forEach(el => el.addEventListener("change", () => renderRelations()));
    fSearch.addEventListener("input", () => renderRelations());
    document.getElementById("f-clear").addEventListener("click", () => {
      fPerson.value = ""; fGrain.value = ""; fStatus.value = ""; fSearch.value = ""; renderRelations();
    });
    renderRelations();

    // Timeline
    document.getElementById("timeline-list").innerHTML = (DB.timeline || []).map(t => `
      <div class="timeline-item" tabindex="0" data-year="${t.year}">
        <strong>${t.year} — ${t.title}</strong>
        <div class="subtitle">${t.detail}</div>
      </div>
    `).join("");
    document.querySelectorAll(".timeline-item").forEach(el => {
      el.addEventListener("click", () => { activateTab("relations"); renderRelations(parseInt(el.dataset.year, 10)); });
    });

    // Network SVG
    const svg = document.getElementById("network-svg");
    const projNodes = DB.projects.filter(p => p.kind !== "álbum" && p.kind !== "faixa");
    const pplNodes = DB.people.slice(0, 12);
    const nodes = [
      ...pplNodes.map((p, i) => ({ id: p.id, label: p.name, type: "person", x: 170, y: 34 + i * 33 })),
      ...projNodes.map((p, i) => ({ id: p.id, label: p.name, type: "project", x: 590, y: 42 + i * 38 }))
    ];
    const nodeMap = Object.fromEntries(nodes.map(n => [n.id, n]));
    const edges = DB.relations.filter(r => r.grain === "projeto" && nodeMap[r.person_id] && nodeMap[r.project_id]);
    svg.innerHTML = [
      ...edges.map(e => `<line x1="${nodeMap[e.person_id].x}" y1="${nodeMap[e.person_id].y}" x2="${nodeMap[e.project_id].x}" y2="${nodeMap[e.project_id].y}" stroke="#334155" stroke-width="1.5" />`),
      ...nodes.map(n => `
        <g class="net-node" data-id="${n.id}" data-type="${n.type}" style="cursor:pointer;">
          <circle cx="${n.x}" cy="${n.y}" r="8" fill="${n.type === 'person' ? '#e11d48' : '#facc15'}" />
          <text x="${n.type === 'person' ? n.x - 14 : n.x + 14}" y="${n.y + 4}" fill="#f8fafc" font-size="11.5" text-anchor="${n.type === 'person' ? 'end' : 'start'}">${n.label}</text>
        </g>
      `)
    ].join("");
    svg.querySelectorAll(".net-node").forEach(el => {
      el.addEventListener("click", () => {
        const id = el.dataset.id; const n = nodeMap[id];
        document.getElementById("network-info").innerHTML = `<strong>${n.label}</strong> (${n.type}) — <button class="btn-sec" onclick="activateTab('relations')">Ver relações</button>`;
        if (n.type === "person") { fPerson.value = id; renderRelations(); }
      });
    });

    // Sources & Links
    document.getElementById("sources-tbody").innerHTML = DB.sources.map(s => `
      <tr><td>${s.id}</td><td><a href="${s.url}" target="_blank" rel="noopener">${s.title}</a></td><td>${s.type}</td><td>${s.consulted_on}</td><td><span class="badge badge-ok">${s.status}</span></td></tr>
    `).join("");
    document.getElementById("links-tbody").innerHTML = DB.links.map(l => `
      <tr><td>${l.title}</td><td><code>${l.recording_id || "—"}</code></td><td><a href="${l.url}" target="_blank" rel="noopener">${l.url}</a></td><td><span class="badge badge-warn">${l.status}</span></td></tr>
    `).join("");

    // Exports
    function downloadFile(filename, content, mime) {
      const blob = new Blob([content], { type: mime });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob); a.download = filename; a.click();
    }
    function toCSV(rows) {
      if (!rows.length) return "";
      const keys = Object.keys(rows[0]);
      const esc = v => {
        let s = Array.isArray(v) || (v && typeof v === "object") ? JSON.stringify(v) : (v ?? "").toString();
        if (s && ["=", "+", "-", "@"].includes(s[0])) s = "'" + s;
        return `"${s.replace(/"/g, '""')}"`;
      };
      return [keys.join(","), ...rows.map(r => keys.map(k => esc(r[k])).join(","))].join("\\n");
    }
    document.getElementById("dl-json").addEventListener("click", () => downloadFile("banco.json", JSON.stringify(DB, null, 2), "application/json"));
    document.getElementById("dl-rel-csv").addEventListener("click", () => downloadFile("relations.csv", toCSV(DB.relations), "text/csv;charset=utf-8"));
    document.getElementById("dl-people-csv").addEventListener("click", () => downloadFile("people.csv", toCSV(DB.people), "text/csv;charset=utf-8"));
    document.getElementById("dl-links-csv").addEventListener("click", () => downloadFile("links.csv", toCSV(DB.links), "text/csv;charset=utf-8"));
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template.replace("__BANCO_JSON__", banco_str))

print("Generated upgraded index.html successfully.")
