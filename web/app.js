// Analog Finder front end (Member 3).
// Loads results.json (real data from merge.py); falls back to mock_results.json.
// Shape of both files: see CONTRACTS.md.

const state = { data: null, weights: { slope: 1, roughness: 1, low_sun: 1 }, markers: {}, chart: null, selected: null };

const ROLE_LABEL = { baseline: "Famous analog", candidate: "Candidate", egypt: "Egypt" };
const fmt = (v, d = 2) => (v === null || v === undefined ? "n/a" : Number(v).toFixed(d));

async function loadData() {
  for (const [file, mock] of [["results.json", false], ["mock_results.json", true]]) {
    try {
      const r = await fetch(file, { cache: "no-store" });
      if (r.ok) {
        document.getElementById("mock-banner").hidden = !mock;
        return r.json();
      }
    } catch (e) { /* try the next file */ }
  }
  throw new Error("No results.json or mock_results.json found");
}

function overall(scores) {
  let num = 0, den = 0;
  for (const k of ["slope", "roughness", "low_sun"]) {
    const v = scores[k], w = state.weights[k];
    if (v !== null && v !== undefined && w > 0) { num += w * v; den += w; }
  }
  return den ? num / den : null;
}

function colour(score) {
  if (score === null) return "#6b7280";
  const t = Math.max(0, Math.min(1, score / 0.6));      // 0.6+ = full green
  const r = Math.round(242 - t * 166), g = Math.round(85 + t * 110), b = Math.round(90 - t * 10);
  return `rgb(${r},${g},${b})`;
}

function initMap() {
  const map = L.map("map", { worldCopyJump: true }).setView([30, 0], 2);
  L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    attribution: "&copy; OpenStreetMap &copy; CARTO", maxZoom: 12,
  }).addTo(map);
  for (const s of state.data.sites) {
    const m = L.circleMarker([s.lat, s.lon], { radius: 9, weight: 2, color: "#0e1116", fillOpacity: 0.95 })
      .addTo(map).bindTooltip(s.name).on("click", () => select(s.id));
    state.markers[s.id] = m;
  }
}

function refresh() {
  const sites = state.data.sites.map(s => ({ ...s, _overall: overall(s.scores) }));
  for (const s of sites) state.markers[s.id].setStyle({ fillColor: colour(s._overall) });
  const ranked = [...sites].sort((a, b) => (b._overall ?? -1) - (a._overall ?? -1));
  document.getElementById("rank-list").innerHTML = ranked.map(s =>
    `<li data-id="${s.id}">${s.name} <span class="quiet">${fmt(s._overall)}</span></li>`).join("");
  document.querySelectorAll("#rank-list li").forEach(li => li.onclick = () => select(li.dataset.id));
  if (state.selected) select(state.selected);
}

function tempRow(label, min, max, colourHex) {
  const lo = -260, hi = 130, pct = v => ((v - lo) / (hi - lo)) * 100;
  if (min === null || min === undefined || max === null || max === undefined) {
    return `<div class="temp-row"><span>${label}</span><div class="temp-track"></div><span class="quiet">n/a</span></div>`;
  }
  return `<div class="temp-row"><span>${label}</span><div class="temp-track">
      <div class="temp-bar" style="left:${pct(min)}%;width:${Math.max(pct(max) - pct(min), 1)}%;background:${colourHex}"></div>
    </div><span>${fmt(min, 0)} to ${fmt(max, 0)} &deg;C</span></div>`;
}

function select(id) {
  state.selected = id;
  const s = state.data.sites.find(x => x.id === id);
  const sc = s.scores, sun = s.sun || {}, w = s.best_window;
  const moonTemp = (state.data.moon && state.data.moon.temp) || {};
  const list = (items, cls) => items && items.length
    ? `<ul class="${cls}">${items.map(t => `<li>${t}</li>`).join("")}</ul>` : `<p class="quiet">Not written yet.</p>`;

  document.getElementById("site-detail").innerHTML = `
    <span class="role">${ROLE_LABEL[s.role] || s.role}</span>
    <h2>${s.name}</h2>
    <div class="big">${fmt(overall(sc))} <span class="quiet">overall match (0 to 1)</span></div>
    <div style="position:relative;height:240px"><canvas id="radar"></canvas></div>
    <h3>Low-sun lighting</h3>
    <p class="quiet">Sun moves through the 0-5&deg; band at <b>${fmt(sun.band_speed_deg_per_hr, 1)}&deg;/h</b>
      (lunar south pole: almost still). Best test window:
      <b>${w ? `${w.start} to ${w.end} (${w.days} days)` : "none - no run of days with 2+ h of low sun"}</b>.</p>
    <h3>Temperature</h3>
    ${tempRow("Earth", s.temp && s.temp.min_c, s.temp && s.temp.max_c, "#4f9cf7")}
    ${tempRow("Moon", moonTemp.min_c, moonTemp.max_c, "#c084fc")}
    <p class="quiet">Shown for honesty, not scored: no Earth site comes close.</p>
    <div class="cols">
      <div><h3>Where it works</h3>${list(s.works, "works")}</div>
      <div><h3>Where it breaks</h3>${list(s.breaks, "breaks")}</div>
    </div>
    ${s.why ? `<p class="quiet"><b>Why it's here:</b> ${s.why}</p>` : ""}
    ${s.access ? `<p class="quiet"><b>Access:</b> ${s.access}</p>` : ""}`;

  if (state.chart) state.chart.destroy();
  state.chart = new Chart(document.getElementById("radar"), {
    type: "radar",
    data: {
      labels: ["Slope", "Roughness", "Low sun"],
      datasets: [{ label: s.name, data: [sc.slope, sc.roughness, sc.low_sun].map(v => v ?? 0),
        backgroundColor: "rgba(79,156,247,0.2)", borderColor: "#4f9cf7" }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { r: { min: 0, max: 1, ticks: { display: false }, grid: { color: "#2a303a" },
        angleLines: { color: "#2a303a" }, pointLabels: { color: "#e8eaed" } } },
    },
  });
}

function initWeights() {
  document.querySelectorAll("#weights input").forEach(inp => {
    inp.oninput = () => {
      state.weights[inp.dataset.key] = Number(inp.value);
      inp.nextElementSibling.textContent = inp.value;
      refresh();
    };
  });
}

(async () => {
  state.data = await loadData();
  Object.assign(state.weights, state.data.weights || {});
  document.querySelectorAll("#weights input").forEach(inp => {
    inp.value = state.weights[inp.dataset.key]; inp.nextElementSibling.textContent = inp.value;
  });
  document.getElementById("cannot-list").innerHTML =
    (state.data.cannot_reproduce || []).map(t => `<li>${t}</li>`).join("");
  initMap();
  initWeights();
  refresh();
})();
