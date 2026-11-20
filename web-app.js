(() => {
  "use strict";

  const STORE_KEY = "windows12ultimate-web-v1";
  const defaults = {
    profile: { username: "Guest", avatar: "W" },
    settings: { theme: "dark", wallpaper: "Aurora", volume: 45, language: "Français" },
    creator: "admine wind12",
    projects: [],
    playStoreIds: [],
    installed: [],
    adminPassword: null,
  };
  const cloneDefaults = () => JSON.parse(JSON.stringify(defaults));
  const state = loadState();
  const desktop = document.querySelector("#desktop");
  const windowsRoot = document.querySelector("#windows");
  const startMenu = document.querySelector("#start-menu");
  const apps = [
    ["explorer", "Explorateur", "▤"], ["browser", "Firefox", "◉"],
    ["calculator", "Calculatrice", "＋"], ["settings", "Paramètres", "⚙"],
    ["profile", "Profil", "♟"], ["games", "Jeux", "◇"],
    ["roblox", "Roblox", "◈"], ["roblox-studio", "Roblox Studio", "✎"],
    ["skins", "Roblox Skins", "♙"], ["admin", "Admin Roblox", "♜"],
    ["store", "Play Store", "▶"], ["play-store-studio", "Play Store Studio", "▣"],
    ["terminal", "Terminal", ">_"], ["music", "Musique", "♫"], ["glitches", "Glitch Lab", "✦"],
    ["horror", "Night Shift", "☾"],
  ];
  const gameCards = [
    { id: "obby-normal", name: "Roblox Obby", description: "Parcours de plateformes et pièces à récupérer.", color: "#58afe8" },
    { id: "obby-hard", name: "Obby Impossible", description: "Sauts précis, plateformes étroites et trois vies.", color: "#a83551" },
    { id: "night-shift", name: "Night Shift", description: "Explore la maison mystérieuse et cherche la sortie.", color: "#45345d" },
    { id: "matrix-runner", name: "Matrix Runner", description: "Plonge dans une animation de code futuriste.", color: "#117d53" },
  ];
  const glitches = [
    ["shake", "Tremblement d’écran"], ["glitch", "Glitch RGB"], ["pixels", "Pixels disparus"], ["red", "Écran rouge"],
    ["bsod", "Faux écran bleu"], ["distortion", "Distorsion"], ["matrix", "Animation Matrix"], ["jumpscare", "Jumpscare surprise"],
    ["rgb_split", "Décalage RGB"], ["chromatic_aberration", "Aberration chromatique"], ["cyan_shadow", "Ombre cyan"],
    ["red_shadow", "Ombre rouge"], ["neon_edges", "Contours néon"], ["prism_echo", "Écho prismatique"],
    ["horizontal_tearing", "Déchirure horizontale"], ["vertical_tearing", "Déchirure verticale"],
    ["rolling_bands", "Bandes déroulantes"], ["analog_dropout", "Perte analogique"], ["tracking_error", "Erreur de tracking"],
    ["tv_static", "Neige télévisuelle"], ["pixel_rain", "Pluie de pixels"], ["pixel_burst", "Explosion de pixels"],
    ["dead_pixel_map", "Carte de pixels morts"], ["pixel_mosaic", "Mosaïque corrompue"], ["block_corruption", "Blocs corrompus"],
    ["tile_shuffle", "Tuiles mélangées"], ["wave_warp", "Vagues déformantes"], ["ripple_field", "Champ d’ondulations"],
    ["tunnel_warp", "Tunnel numérique"], ["wobble_grid", "Grille vacillante"], ["mirror_split", "Miroir fracturé"],
    ["perspective_fold", "Pli de perspective"], ["code_rain", "Pluie de code"], ["glyph_scramble", "Glyphes brouillés"],
    ["cursor_storm", "Tempête de curseurs"], ["hex_cascade", "Cascade hexadécimale"], ["corrupted_text", "Texte corrompu"],
    ["symbol_rain", "Pluie de symboles"], ["red_alert", "Alerte écarlate"], ["blue_shift", "Décalage bleu"],
    ["green_phosphor", "Phosphore vert"], ["purple_haze", "Brume violette"], ["amber_warning", "Avertissement ambre"],
    ["negative_tint", "Teinte négative"], ["ghost_frames", "Images fantômes"], ["double_vision", "Vision double"],
    ["shadow_trails", "Traînées d’ombre"], ["outline_echo", "Écho de contours"], ["fractured_screen", "Écran fracturé"],
    ["afterimage", "Rémanence numérique"], ["horizontal_bars", "Barres horizontales"], ["vertical_blinds", "Stores verticaux"],
    ["broken_bars", "Barres cassées"], ["data_stripes", "Rayures de données"], ["signal_ladder", "Échelle de signal"],
    ["moving_slits", "Fentes mouvantes"], ["white_noise", "Bruit blanc"], ["static_specks", "Grésillement"],
    ["scanline_drift", "Lignes de balayage"], ["analog_fuzz", "Parasites analogiques"],
    ["frequency_bleed", "Bavure de fréquence"], ["signal_loss", "Perte de signal"], ["radial_burst", "Rayonnement radial"],
    ["glitch_sweep", "Balayage glitch"], ["data_vortex", "Vortex de données"], ["split_screen", "Écran divisé"],
    ["digital_shards", "Éclats numériques"], ["portal_noise", "Portail parasité"],
  ];
  const palette = {
    dark: { bg: "#101827", panel: "#18263a", raised: "#223650", fg: "#edf4ff", muted: "#9db0ca", accent: "#55c8ff" },
    light: { bg: "#edf3fb", panel: "#ffffff", raised: "#dfe8f4", fg: "#17243a", muted: "#5e708a", accent: "#087fcb" },
  };
  let zIndex = 3;
  let noticeTimer;

  function loadState() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORE_KEY) || "{}");
      return {
        ...cloneDefaults(),
        ...saved,
        profile: { ...defaults.profile, ...(saved.profile || {}) },
        settings: { ...defaults.settings, ...(saved.settings || {}) },
        projects: Array.isArray(saved.projects) ? saved.projects : [],
        playStoreIds: Array.isArray(saved.playStoreIds) ? saved.playStoreIds : [],
        installed: Array.isArray(saved.installed) ? saved.installed : [],
      };
    } catch (error) {
      console.error("Chargement de la sauvegarde locale impossible.", error);
      return cloneDefaults();
    }
  }
  function save() {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify(state));
    } catch (error) {
      toast("Impossible de sauvegarder sur cet appareil.");
      console.error("Sauvegarde locale impossible.", error);
    }
    updateProfile();
  }
  function esc(value) {
    return String(value ?? "").replace(/[&<>"']/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[ch]);
  }
  function toast(message) {
    const node = document.querySelector("#notice");
    node.textContent = message;
    node.classList.remove("hidden");
    clearTimeout(noticeTimer);
    noticeTimer = setTimeout(() => node.classList.add("hidden"), 2400);
  }
  function updateProfile() {
    const name = state.profile.username || "Guest";
    document.querySelector("#desktop-user").textContent = name.toLowerCase() === "hacker" ? "H A C K E R" : "";
    document.querySelector("#task-user").textContent = `${state.profile.avatar || "W"}  ${name}`;
  }
  function applySettings() {
    desktop.classList.toggle("light", state.settings.theme === "light");
    desktop.dataset.wallpaper = state.settings.wallpaper || "Aurora";
    document.documentElement.style.setProperty("--accent", state.settings.theme === "light" ? "#087fcb" : "#55c8ff");
  }
  function button(text, action, cls = "") {
    const node = document.createElement("button");
    node.type = "button";
    node.className = `btn ${cls}`;
    node.textContent = text;
    node.addEventListener("click", action);
    return node;
  }
  function makeWindow(key, title, size = "760px") {
    const existing = document.querySelector(`[data-window="${CSS.escape(key)}"]`);
    if (existing) {
      existing.classList.remove("hidden");
      existing.style.zIndex = String(++zIndex);
      return existing.querySelector(".window-body");
    }
    const win = document.createElement("section");
    win.className = "app-window";
    win.dataset.window = key;
    win.style.maxWidth = `min(${size}, calc(100vw - 18px))`;
    win.style.zIndex = String(++zIndex);
    win.innerHTML = `<header class="window-titlebar"><span class="window-title">${esc(title)}</span><button class="window-close" aria-label="Fermer">×</button></header><div class="window-body"></div>`;
    windowsRoot.append(win);
    const close = () => {
      win.remove();
      const task = document.querySelector(`[data-task="${CSS.escape(key)}"]`);
      if (task) task.remove();
    };
    win.querySelector(".window-close").addEventListener("click", close);
    win.addEventListener("pointerdown", () => { win.style.zIndex = String(++zIndex); });
    const bar = win.querySelector(".window-titlebar");
    let drag;
    bar.addEventListener("pointerdown", event => {
      if (event.target.closest("button")) return;
      const rect = win.getBoundingClientRect();
      drag = { x: event.clientX - rect.left, y: event.clientY - rect.top };
      bar.setPointerCapture(event.pointerId);
    });
    bar.addEventListener("pointermove", event => {
      if (!drag || matchMedia("(max-width: 650px)").matches) return;
      win.style.left = `${Math.max(0, Math.min(innerWidth - win.offsetWidth, event.clientX - drag.x))}px`;
      win.style.top = `${Math.max(0, Math.min(innerHeight - 80, event.clientY - drag.y))}px`;
      win.style.transform = "none";
    });
    bar.addEventListener("pointerup", () => { drag = null; });
    const task = document.createElement("button");
    task.className = "task-app";
    task.dataset.task = key;
    task.textContent = title;
    task.addEventListener("click", () => {
      if (win.classList.contains("hidden")) win.classList.remove("hidden");
      win.style.zIndex = String(++zIndex);
    });
    document.querySelector("#task-apps").append(task);
    return win.querySelector(".window-body");
  }
  function openApp(key) {
    startMenu.classList.add("hidden");
    const route = {
      explorer: openExplorer, browser: openBrowser, calculator: openCalculator, settings: openSettings,
      profile: openProfile, games: openGames, roblox: openRoblox, "roblox-studio": openStudio,
      skins: openSkins, admin: openAdmin, store: openStore, "play-store-studio": openPlayStoreStudio,
      terminal: openTerminal, music: openMusic, glitches: openGlitches, horror: openHorror,
    }[key];
    if (route) route();
  }
  function initDesktop() {
    const icons = document.querySelector("#desktop-icons");
    apps.forEach(([key, name, glyph]) => {
      const item = document.createElement("button");
      item.className = "desktop-icon";
      item.innerHTML = `<span class="icon-glyph">${glyph}</span><span>${esc(name)}</span>`;
      item.addEventListener("click", () => openApp(key));
      icons.append(item);
    });
    document.querySelector("#start-button").addEventListener("click", () => {
      startMenu.classList.toggle("hidden");
      if (!startMenu.classList.contains("hidden")) renderStart();
    });
    document.addEventListener("click", event => {
      if (!startMenu.contains(event.target) && event.target.id !== "start-button" && !event.target.closest("#start-button")) startMenu.classList.add("hidden");
    });
    setInterval(() => {
      const now = new Date();
      document.querySelector("#clock").textContent = `${now.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })}\n${now.toLocaleDateString("fr-FR")}`;
    }, 1000);
    applySettings();
    updateProfile();
  }
  function renderStart(filter = "") {
    startMenu.innerHTML = `<h2>WINDOWS 12 ULTIMATE</h2><input class="field" id="start-search" placeholder="Rechercher une application ou commande…"><div class="start-grid" id="start-grid"></div><p class="muted">Simulateur web local • commandes système désactivées</p>`;
    const search = startMenu.querySelector("#start-search");
    search.value = filter;
    const grid = startMenu.querySelector("#start-grid");
    const draw = () => {
      grid.replaceChildren();
      const query = search.value.toLowerCase().trim();
      apps.filter(([, name]) => name.toLowerCase().includes(query)).forEach(([key, name]) => grid.append(button(name, () => openApp(key))));
    };
    search.addEventListener("input", draw);
    search.addEventListener("keydown", event => {
      if (event.key === "Enter") runSecret(search.value);
    });
    draw();
  }
  function addSection(body, title, text = "") {
    const heading = document.createElement("h1");
    heading.textContent = title;
    body.append(heading);
    if (text) {
      const p = document.createElement("p");
      p.className = "muted";
      p.textContent = text;
      body.append(p);
    }
  }
  function openExplorer() {
    const body = makeWindow("explorer", "Explorateur de fichiers");
    body.innerHTML = `<h1>Accueil　›　Ce PC</h1><div class="grid">${["Bureau", "Documents", "Images", "Musique", "Téléchargements", "Disque virtuel"].map(x => `<article class="card"><h3>▣　${x}</h3><p class="muted">Dossier virtuel du simulateur</p></article>`).join("")}</div><p class="muted">Aucun fichier Windows réel n’est lu ou modifié.</p>`;
  }
  function openBrowser() {
    const body = makeWindow("browser", "Firefox • Nova Browser");
    body.innerHTML = `<h1>Firefox　<span class="muted">simulation</span></h1><form class="row" id="browser-form"><input class="field" id="browser-query" placeholder="Rechercher ou saisir une adresse"><button class="btn primary">Aller</button></form><section class="card" id="browser-result"><h2>Bienvenue</h2><p class="muted">Ce navigateur de démonstration n’accède pas à Internet. Les pages de la simulation sont locales.</p></section>`;
    body.querySelector("#browser-form").addEventListener("submit", event => {
      event.preventDefault();
      const term = body.querySelector("#browser-query").value.trim();
      body.querySelector("#browser-result").innerHTML = `<h2>${esc(term || "Recherche")}</h2><p class="muted">Aperçu de navigation simulé. Le site public WINDOWS 12 peut être ouvert dans le vrai Firefox après son hébergement.</p>`;
    });
  }
  function openCalculator() {
    const body = makeWindow("calculator", "Calculatrice");
    body.innerHTML = `<h1>Calculatrice</h1><input class="field" id="calc-display" inputmode="decimal" placeholder="0"><div class="grid" id="calc-keys"></div>`;
    const display = body.querySelector("#calc-display");
    const keys = ["7", "8", "9", "÷", "4", "5", "6", "×", "1", "2", "3", "−", "C", "0", "=", "+"];
    keys.forEach(k => body.querySelector("#calc-keys").append(button(k, () => {
      if (k === "C") display.value = "";
      else if (k === "=") {
        try { display.value = calculate(display.value); } catch { display.value = "Expression invalide"; }
      } else display.value += ({ "÷": "/", "×": "*", "−": "-" })[k] || k;
    })));
  }
  function calculate(source) {
    const tokens = source.match(/\d+(?:\.\d+)?|[()+\-*/%]/g) || [];
    if (tokens.join("") !== source.replace(/\s+/g, "")) throw Error("Invalid expression");
    let i = 0;
    function atom() {
      const token = tokens[i++];
      if (token === "(") {
        const value = expr();
        if (tokens[i++] !== ")") throw Error("Missing )");
        return value;
      }
      if (token === "-") return -atom();
      const n = Number(token);
      if (!Number.isFinite(n)) throw Error("Invalid number");
      return n;
    }
    function term() {
      let n = atom();
      while (["*", "/", "%"].includes(tokens[i])) {
        const op = tokens[i++];
        const rhs = atom();
        n = op === "*" ? n * rhs : op === "/" ? n / rhs : n % rhs;
      }
      return n;
    }
    function expr() {
      let n = term();
      while (["+", "-"].includes(tokens[i])) {
        const op = tokens[i++];
        const rhs = term();
        n = op === "+" ? n + rhs : n - rhs;
      }
      return n;
    }
    const result = expr();
    if (i !== tokens.length || !Number.isFinite(result)) throw Error("Invalid result");
    return String(result);
  }
  function openSettings() {
    const body = makeWindow("settings", "Paramètres");
    body.innerHTML = `<h1>Paramètres</h1><div class="stack">
      <label class="card">Thème <select class="field" id="setting-theme"><option value="dark">Sombre</option><option value="light">Clair</option></select></label>
      <label class="card">Fond d’écran <select class="field" id="setting-wall"><option>Aurora</option><option>Nebula</option><option>Ocean</option><option>Graphite</option></select></label>
      <label class="card">Volume simulé <input id="setting-volume" type="range" min="0" max="100"></label>
      <label class="card">Langue <select class="field" id="setting-language"><option>Français</option><option>English</option></select></label>
      <button class="btn" id="setting-full">Plein écran</button>
      <p class="muted">Les préférences sont enregistrées dans le navigateur de cet appareil.</p></div>`;
    const theme = body.querySelector("#setting-theme");
    const wall = body.querySelector("#setting-wall");
    const volume = body.querySelector("#setting-volume");
    const language = body.querySelector("#setting-language");
    theme.value = state.settings.theme;
    wall.value = state.settings.wallpaper;
    volume.value = state.settings.volume;
    language.value = state.settings.language;
    [theme, wall, volume, language].forEach(control => control.addEventListener("change", () => {
      state.settings.theme = theme.value;
      state.settings.wallpaper = wall.value;
      state.settings.volume = Number(volume.value);
      state.settings.language = language.value;
      save();
      applySettings();
    }));
    body.querySelector("#setting-full").addEventListener("click", async () => {
      try {
        if (!document.fullscreenElement) await desktop.requestFullscreen();
        else await document.exitFullscreen();
      } catch { toast("Le mode plein écran n’est pas disponible dans ce navigateur."); }
    });
  }
  function openProfile() {
    const body = makeWindow("profile", "Profil local");
    body.innerHTML = `<h1>Mon profil</h1><p class="muted">Profil local, enregistré sur cet appareil.</p><div class="stack"><label>Nom d’utilisateur<input class="field" id="profile-name" maxlength="24"></label><label>Avatar (une lettre ou un emoji)<input class="field" id="profile-avatar" maxlength="4"></label><label>Nom du créateur Roblox<input class="field" id="creator-name" maxlength="32"></label><button class="btn primary" id="profile-save">Enregistrer le profil</button></div>`;
    body.querySelector("#profile-name").value = state.profile.username;
    body.querySelector("#profile-avatar").value = state.profile.avatar;
    body.querySelector("#creator-name").value = state.creator;
    body.querySelector("#profile-save").addEventListener("click", () => {
      state.profile.username = body.querySelector("#profile-name").value.trim() || "Guest";
      state.profile.avatar = body.querySelector("#profile-avatar").value.trim() || "W";
      state.creator = body.querySelector("#creator-name").value.trim() || "Créateur";
      save();
      toast("Profil enregistré.");
    });
  }
  function openGames() {
    const body = makeWindow("games", "Jeux installés");
    body.innerHTML = `<h1>Mes jeux</h1><div id="installed-games" class="grid"></div>`;
    const list = body.querySelector("#installed-games");
    const known = [...gameCards, ...state.projects.map(p => ({ id: `project:${p.id}`, name: p.name, description: `Créé par ${p.creator}`, color: "#4563a8", project: p }))];
    const items = known.filter(g => state.installed.includes(g.id));
    if (!items.length) list.innerHTML = `<p class="muted">Aucun jeu installé. Ouvre le Play Store pour en choisir.</p>`;
    items.forEach(item => {
      const card = document.createElement("article");
      card.className = "card";
      card.innerHTML = `<h3>${esc(item.name)}</h3><p class="muted">${esc(item.description)}</p>`;
      card.append(button("Jouer", () => launchGame(item), "primary"));
      list.append(card);
    });
    body.append(button("Ouvrir Play Store", openStore));
  }
  function allCatalogItems() {
    const builtIns = [
      ...apps.filter(([key]) => ["roblox", "roblox-studio", "skins", "store", "play-store-studio"].includes(key)).map(([id, name]) => ({ id: `app:${id}`, name, kind: "app", description: "Application locale du simulateur." })),
      ...gameCards.map(g => ({ ...g, kind: "game" })),
    ];
    const published = state.projects.filter(p => state.playStoreIds.includes(p.id)).map(p => ({
      id: `project:${p.id}`, name: p.name, kind: "game", description: `Créé par ${p.creator} • jeu publié localement`, project: p,
    }));
    return [...builtIns, ...published];
  }
  function catalogOpen(item) {
    if (item.project) launchGame(item);
    else if (item.kind === "game") launchGame(item);
    else openApp(item.id.slice(4));
  }
  function openStore() {
    const body = makeWindow("store", "Play Store • Catalogue local");
    body.innerHTML = `<div class="row" style="justify-content:space-between"><h1>PLAY STORE</h1><button class="btn" id="store-studio">Play Store Studio</button></div><p class="muted">Catalogue de démonstration. Les installations ne téléchargent aucun fichier et sont conservées sur cet appareil.</p><input class="field" id="store-search" placeholder="Rechercher…"><div id="store-list" class="grid" style="margin-top:12px"></div>`;
    body.querySelector("#store-studio").addEventListener("click", openPlayStoreStudio);
    const search = body.querySelector("#store-search");
    const list = body.querySelector("#store-list");
    const render = () => {
      list.replaceChildren();
      allCatalogItems().filter(item => `${item.name} ${item.description}`.toLowerCase().includes(search.value.toLowerCase())).forEach(item => {
        const card = document.createElement("article");
        card.className = "card";
        card.innerHTML = `<h3>${esc(item.name)}</h3><p class="muted">${esc(item.description)}</p>`;
        if (state.installed.includes(item.id)) card.append(button(item.kind === "app" ? "Ouvrir" : "Jouer", () => catalogOpen(item), "primary"));
        else card.append(button("Installer", () => {
          state.installed.push(item.id);
          save();
          toast(`${item.name} installé sur cet appareil.`);
          render();
        }));
        list.append(card);
      });
    };
    search.addEventListener("input", render);
    render();
  }
  function openPlayStoreStudio() {
    const body = makeWindow("play-store-studio", "Play Store Studio");
    body.innerHTML = `<h1>Play Store Studio</h1><p class="muted">Publie ou retire du catalogue local les jeux créés dans Roblox Studio. Aucune publication vers Google ou Roblox.</p><div id="ps-projects" class="grid"></div>`;
    const list = body.querySelector("#ps-projects");
    if (!state.projects.length) list.innerHTML = `<p class="muted">Pas encore de jeu. Crée un jeu dans Roblox Studio.</p>`;
    state.projects.forEach(project => {
      const listed = state.playStoreIds.includes(project.id);
      const card = document.createElement("article");
      card.className = "card";
      card.innerHTML = `<h3>${esc(project.name)}</h3><p class="muted">Créateur : ${esc(project.creator)} • ${project.objects?.length || 0} éléments • ${listed ? "Publié" : "Brouillon Play Store"}</p>`;
      card.append(button(listed ? "Retirer du Play Store" : "Publier dans Play Store", () => {
        state.playStoreIds = listed ? state.playStoreIds.filter(id => id !== project.id) : [...state.playStoreIds, project.id];
        save();
        openPlayStoreStudio();
        toast(listed ? "Jeu retiré du catalogue." : "Jeu publié dans le catalogue local.");
      }, listed ? "" : "primary"));
      list.append(card);
    });
  }
  function openRoblox() {
    const body = makeWindow("roblox", "Roblox • Accueil");
    body.innerHTML = `<div class="row" style="justify-content:space-between"><h1>ROBLOX</h1><span class="muted">Créateur : ${esc(state.creator)}</span></div><div class="row" style="margin:10px 0"><button class="btn" id="rb-studio">＋ Studio</button><button class="btn" id="rb-profile">Mon profil</button><button class="btn" id="rb-games">Mes jeux</button></div><h2>Recommandé pour toi</h2><div class="grid" id="roblox-games"></div>`;
    body.querySelector("#rb-studio").addEventListener("click", openStudio);
    body.querySelector("#rb-profile").addEventListener("click", openProfile);
    body.querySelector("#rb-games").addEventListener("click", openGames);
    const games = body.querySelector("#roblox-games");
    const items = [...gameCards, ...state.projects.map(project => ({ id: `project:${project.id}`, name: project.name, description: `Jeu créé localement • ${project.objects?.length || 0} objets`, color: "#4563a8", project }))];
    items.forEach(item => {
      const card = document.createElement("article");
      card.className = "card";
      card.innerHTML = `<div style="background:${item.color || "#4563a8"};padding:22px;border-radius:8px;font-weight:800">${esc(item.name.toUpperCase())}</div><h3>${esc(item.name)}</h3><p class="muted">${esc(item.description)}</p>`;
      card.append(button("▶ Jouer", () => launchGame(item), "primary"));
      games.append(card);
    });
  }
  function openStudio() {
    const body = makeWindow("roblox-studio", "Roblox Studio • Créateur local");
    body.innerHTML = `<h1>Roblox Studio</h1><p class="muted">Crée un niveau simple, sauvegardé localement sur cet appareil.</p><div class="stack"><label>Nom du jeu<input class="field" id="studio-name" maxlength="48" value="Mon jeu"></label><label>Créateur<input class="field" id="studio-creator" maxlength="32"></label><div class="row"><button class="btn" id="studio-platform">＋ Ajouter une plateforme</button><span id="studio-count" class="muted">0 objets</span></div><div id="studio-objects" class="muted"></div><button class="btn primary" id="studio-publish">Publier dans Roblox local</button></div>`;
    const creator = body.querySelector("#studio-creator");
    creator.value = state.creator;
    let objects = [];
    const show = () => {
      body.querySelector("#studio-count").textContent = `${objects.length} objets`;
      body.querySelector("#studio-objects").textContent = objects.map((_, i) => `Plateforme ${i + 1}`).join(" • ") || "Aucune plateforme ajoutée.";
    };
    body.querySelector("#studio-platform").addEventListener("click", () => { objects.push({ type: "platform" }); show(); });
    body.querySelector("#studio-publish").addEventListener("click", () => {
      const name = body.querySelector("#studio-name").value.trim();
      const author = creator.value.trim();
      if (!name || !author) { toast("Le nom du jeu et du créateur sont requis."); return; }
      state.creator = author;
      const project = { id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`, name, creator: author, objects, publishedAt: new Date().toISOString() };
      state.projects.unshift(project);
      save();
      toast(`« ${name} » publié dans Roblox local.`);
      openRoblox();
    });
  }
  function launchGame(item) {
    if (item.id === "night-shift") return openHorrorGame();
    if (item.id === "matrix-runner") return startGlitch("matrix", "Matrix Runner");
    const body = makeWindow(`game-${item.id}`, `Jouer • ${item.name}`, "800px");
    body.innerHTML = `<h1>${esc(item.name)}</h1><p class="muted">Utilise ◀ ▶ pour courir et ▲ pour sauter. Sur ordinateur, flèches/A-D et espace fonctionnent aussi.</p><canvas class="game-canvas" width="780" height="410"></canvas><div class="game-controls"><button class="btn" data-dir="left">◀</button><button class="btn" data-jump>▲ Sauter</button><button class="btn" data-dir="right">▶</button><button class="btn" data-reset>Recommencer</button></div>`;
    startPlatformGame(body.querySelector("canvas"), body, item);
  }
  function startPlatformGame(canvas, body, item) {
    const ctx = canvas.getContext("2d");
    const hard = item.id === "obby-hard";
    const platforms = item.project?.objects?.length
      ? item.project.objects.map((_, i) => [120 + (i % 5) * 145, 360 - (i % 4) * 65, 110])
      : hard ? [[0, 370, 132], [195, 318, 44], [280, 265, 44], [365, 310, 40], [455, 238, 42], [545, 288, 40], [635, 220, 42], [710, 190, 130]]
        : [[0, 370, 170], [255, 316, 140], [450, 258, 135], [650, 200, 190]];
    const player = { x: 25, y: 330, vy: 0, left: false, right: false, ground: false, lives: 3, coins: 0, won: false };
    const keysDown = event => {
      if (["ArrowLeft", "a", "A"].includes(event.key)) player.left = true;
      if (["ArrowRight", "d", "D"].includes(event.key)) player.right = true;
      if ([" ", "ArrowUp", "w", "W"].includes(event.key) && player.ground) { player.vy = -12; player.ground = false; }
    };
    const keysUp = event => {
      if (["ArrowLeft", "a", "A"].includes(event.key)) player.left = false;
      if (["ArrowRight", "d", "D"].includes(event.key)) player.right = false;
    };
    document.addEventListener("keydown", keysDown);
    document.addEventListener("keyup", keysUp);
    body.querySelectorAll("[data-dir]").forEach(control => {
      const dir = control.dataset.dir;
      control.addEventListener("pointerdown", event => { event.preventDefault(); player[dir] = true; control.setPointerCapture(event.pointerId); });
      ["pointerup", "pointercancel", "lostpointercapture"].forEach(type => control.addEventListener(type, () => { player[dir] = false; }));
    });
    body.querySelector("[data-jump]").addEventListener("click", () => {
      if (player.ground) { player.vy = -12; player.ground = false; }
    });
    body.querySelector("[data-reset]").addEventListener("click", () => Object.assign(player, { x: 25, y: 330, vy: 0, lives: 3, coins: 0, won: false }));
    function frame() {
      if (!canvas.isConnected) {
        document.removeEventListener("keydown", keysDown);
        document.removeEventListener("keyup", keysUp);
        return;
      }
      player.x = Math.max(0, Math.min(750, player.x + (Number(player.right) - Number(player.left)) * (hard ? 3.2 : 4)));
      const oldBottom = player.y + 35;
      player.vy = Math.min(14, player.vy + .65);
      let nextY = player.y + player.vy;
      player.ground = false;
      for (const [x, y, width] of platforms) {
        if (player.x + 25 > x && player.x < x + width && player.vy >= 0 && oldBottom <= y && nextY + 35 >= y) {
          nextY = y - 35; player.vy = 0; player.ground = true; break;
        }
      }
      player.y = nextY;
      if (player.y > 430) {
        player.lives--;
        player.x = 25; player.y = 330; player.vy = 0;
        if (player.lives <= 0) player.won = true;
      }
      if (player.x > 710 && player.y < 190) player.won = true;
      ctx.clearRect(0, 0, 780, 410);
      ctx.fillStyle = "#83c9f5"; ctx.fillRect(0, 0, 780, 410);
      ctx.fillStyle = "#ffe58b"; ctx.beginPath(); ctx.arc(670, 62, 38, 0, Math.PI * 2); ctx.fill();
      platforms.forEach(([x, y, w]) => { ctx.fillStyle = "#287d46"; ctx.fillRect(x, y, w, 14); ctx.fillStyle = "#72d657"; ctx.fillRect(x, y, w, 5); });
      ctx.fillStyle = "#ff475d"; ctx.fillRect(735, 140, 28, 18);
      ctx.fillStyle = "#ffd43b";
      for (let i = 0; i < 5; i++) { ctx.beginPath(); ctx.arc(175 + i * 120, 285 - i * 35, 7, 0, Math.PI * 2); ctx.fill(); }
      ctx.fillStyle = "#ffd1a6"; ctx.fillRect(player.x + 5, player.y, 18, 18);
      ctx.fillStyle = "#1687e8"; ctx.fillRect(player.x + 2, player.y + 18, 24, 16);
      ctx.fillStyle = "#303847"; ctx.fillRect(player.x + 3, player.y + 34, 9, 5); ctx.fillRect(player.x + 16, player.y + 34, 9, 5);
      ctx.fillStyle = "#17344a"; ctx.font = "bold 15px Segoe UI"; ctx.fillText(`VIES : ${Math.max(0, player.lives)}`, 12, 24);
      if (player.won) { ctx.fillStyle = "#091426cc"; ctx.fillRect(0, 0, 780, 410); ctx.fillStyle = "white"; ctx.font = "bold 30px Segoe UI"; ctx.fillText(player.lives > 0 ? "PARCOURS TERMINÉ !" : "PARTIE TERMINÉE", 210, 205); }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  function openSkins() {
    const body = makeWindow("skins", "Roblox Skins Studio");
    body.innerHTML = `<h1>Roblox Skins Studio</h1><p class="muted">Choisis les couleurs de ton avatar local.</p><div class="skin-preview" id="skin-preview"></div><div class="grid"><label class="card">Tête <input class="field" id="skin-head" type="color" value="#f0c58c"></label><label class="card">Tenue <input class="field" id="skin-shirt" type="color" value="#2789ec"></label></div><button class="btn primary" id="skin-save">Enregistrer mon skin</button>`;
    const update = () => body.querySelector("#skin-preview").style.setProperty("--skin", body.querySelector("#skin-head").value);
    body.querySelectorAll('input[type="color"]').forEach(input => input.addEventListener("input", update));
    body.querySelector("#skin-save").addEventListener("click", () => { localStorage.setItem(`${STORE_KEY}-skin`, JSON.stringify({ head: body.querySelector("#skin-head").value, shirt: body.querySelector("#skin-shirt").value })); toast("Skin enregistré localement."); });
    update();
  }
  function openAdmin() {
    const body = makeWindow("admin", "Admin Roblox • Joueurs fictifs");
    body.innerHTML = `<h1>Admin local</h1><p class="muted">Liste de démonstration : ces joueurs ne sont pas connectés à Roblox.</p><form class="row" id="admin-form"><input class="field" id="admin-password" type="password" placeholder="${state.adminPassword ? "Mot de passe administrateur" : "Créer un mot de passe"}" required><button class="btn primary">Déverrouiller</button></form><div id="admin-result"></div>`;
    body.querySelector("#admin-form").addEventListener("submit", event => {
      event.preventDefault();
      authenticateAdmin(body.querySelector("#admin-password").value, body.querySelector("#admin-result")).catch(error => {
        console.error("Échec de l’authentification locale.", error);
        toast("L’authentification locale a échoué.");
      });
    });
  }
  async function authenticateAdmin(password, result) {
    if (!globalThis.crypto?.subtle) {
      toast("L’authentification nécessite un site HTTPS ou localhost.");
      return;
    }
    const encode = bytes => btoa(String.fromCharCode(...new Uint8Array(bytes)));
    const digest = async salt => {
      const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(password), "PBKDF2", false, ["deriveBits"]);
      return encode(await crypto.subtle.deriveBits({ name: "PBKDF2", salt, iterations: 210000, hash: "SHA-256" }, key, 256));
    };
    const current = state.adminPassword;
    if (!current) {
      const salt = crypto.getRandomValues(new Uint8Array(16));
      state.adminPassword = { salt: encode(salt), hash: await digest(salt) };
      save();
    } else if (typeof current === "string") {
      if (password !== current) { toast("Mot de passe incorrect."); return; }
      const salt = crypto.getRandomValues(new Uint8Array(16));
      state.adminPassword = { salt: encode(salt), hash: await digest(salt) };
      save();
    } else {
      if (typeof current.salt !== "string" || typeof current.hash !== "string") {
        toast("Sauvegarde du mot de passe invalide; réinitialise les données locales.");
        return;
      }
      const salt = Uint8Array.from(atob(current.salt), ch => ch.charCodeAt(0));
      if (await digest(salt) !== current.hash) { toast("Mot de passe incorrect."); return; }
    }
    result.innerHTML = `<h2>Joueurs simulés</h2>${["admine wind12 • En ligne • Studio", "PixelNova • En ligne • Obby", "LunaBuilds • Absente", "Max_Runner • En ligne • Obby"].map(x => `<article class="card">${esc(x)}</article>`).join("")}`;
  }
  function openTerminal() {
    const body = makeWindow("terminal", "Terminal de simulation");
    body.innerHTML = `<h1>Terminal X</h1><pre id="terminal-output" class="terminal-output">WINDOWS 12 ULTIMATE • terminal simulé\nAucune commande Windows n’est exécutée.\nTape help pour la liste des commandes.</pre><form class="terminal-line"><span>guest@w12 $</span><input id="terminal-input" autocomplete="off" aria-label="Commande"></form>`;
    const output = body.querySelector("#terminal-output");
    body.querySelector("form").addEventListener("submit", event => {
      event.preventDefault();
      const input = body.querySelector("#terminal-input");
      const command = input.value.trim();
      input.value = "";
      output.textContent += `\nguest@w12 $ ${command}\n${terminalCommand(command)}`;
      output.scrollTop = output.scrollHeight;
    });
  }
  function terminalCommand(source) {
    const key = source.toLowerCase();
    if (runSecret(source)) return "Commande secrète activée.";
    const commands = {
      help: "help | clear | date | whoami | dir | sysinfo | about | matrix | firefox",
      date: new Date().toLocaleString(),
      whoami: state.profile.username,
      dir: "Desktop  Documents  Pictures  Music (dossiers virtuels)",
      sysinfo: "OS: WINDOWS 12 ULTIMATE web • Build: 12.0.999 simulé • Réseau: navigateur",
      about: "Simulateur web isolé. Aucun accès au shell de l’appareil.",
      firefox: "Ouvre Firefox/Nova Browser dans le simulateur.",
      matrix: "Animation Matrix activée.",
    };
    if (key === "clear") { document.querySelector("#terminal-output").textContent = ""; return ""; }
    if (key === "matrix") startGlitch("matrix", "Terminal");
    if (key === "firefox") openBrowser();
    return commands[key] || "Commande inconnue. Tape help.";
  }
  function openMusic() {
    const body = makeWindow("music", "Soundwave • Lecteur musical");
    body.innerHTML = `<h1>SOUNDWAVE</h1><p class="muted">Lecteur de démonstration, sans musique externe.</p><select class="field"><option>Aurora Protocol</option><option>Neon Skyline</option><option>Deep Space</option><option>Midnight Circuit</option></select><p id="music-state" class="muted">Prêt</p>`;
    const toggle = button("▶ Lecture simulée", () => {
      const on = toggle.textContent.includes("Lecture");
      toggle.textContent = on ? "Ⅱ Pause" : "▶ Lecture simulée";
      body.querySelector("#music-state").textContent = on ? "Lecture simulée…" : "En pause";
    }, "primary");
    body.append(toggle);
  }
  function openGlitches() {
    const body = makeWindow("glitches", "Glitch Lab • 68 effets");
    body.innerHTML = `<h1>GLITCH LAB</h1><p class="muted">${glitches.length} effets visuels simulés • bouton d’arrêt disponible.</p><input class="field" id="glitch-search" placeholder="Filtrer les effets…"><div id="glitch-list" class="grid" style="margin-top:12px"></div>`;
    const search = body.querySelector("#glitch-search");
    const list = body.querySelector("#glitch-list");
    const render = () => {
      list.replaceChildren();
      glitches.filter(([, name]) => name.toLowerCase().includes(search.value.toLowerCase())).forEach(([id, name]) => list.append(button(name, () => startGlitch(id, name))));
    };
    search.addEventListener("input", render);
    render();
  }
  function startGlitch(id, name) {
    const overlay = document.createElement("div");
    overlay.className = `glitch-screen ${id === "matrix" ? "matrix" : ["red", "red_alert"].includes(id) ? "red" : id === "bsod" ? "bsod" : ""}`;
    overlay.innerHTML = `<span>${id === "bsod" ? ":(<br><small>Écran bleu simulé — rien n’a été modifié.</small>" : esc(name.toUpperCase())}</span>`;
    overlay.append(button("ARRÊTER L’EFFET", () => overlay.remove(), "danger"));
    document.body.append(overlay);
    if (!["red", "red_alert", "bsod"].includes(id)) {
      const interval = setInterval(() => {
        if (!overlay.isConnected) { clearInterval(interval); return; }
        overlay.style.filter = `hue-rotate(${Math.random() * 360}deg)`;
        overlay.style.transform = id === "shake" ? `translate(${Math.random() * 10 - 5}px, ${Math.random() * 10 - 5}px)` : "none";
      }, 120);
    }
  }
  function openHorror() {
    const body = makeWindow("horror", "Night Shift • Menu");
    body.innerHTML = `<h1>NIGHT SHIFT</h1><p class="muted">Jeu d’exploration fictif. Trouve la sortie et évite le monstre.</p><label>Difficulté <select id="horror-level" class="field"><option>Calme</option><option selected>Normal</option><option>Intense</option></select></label><p><button class="btn primary" id="horror-play">PLAY</button></p>`;
    body.querySelector("#horror-play").addEventListener("click", openHorrorGame);
  }
  function openHorrorGame() {
    const body = makeWindow("horror-game", "Night Shift • Partie");
    const rooms = [["Hall", "Study", "Bedroom"], ["Kitchen", "Foyer", "Attic"], ["Cellar", "Garden", "Exit"]];
    const stateGame = { x: 1, y: 1, monster: [2, 0], moves: 0, light: false, ended: false };
    body.innerHTML = `<h1 id="horror-room"></h1><div class="card" id="horror-scene" style="min-height:180px;display:grid;place-items:center;background:#080d16;font-size:30px"></div><p id="horror-status" class="muted">Explore les pièces et trouve la sortie.</p><div class="horror-grid" id="horror-controls"></div><button id="flashlight" class="btn">Lampe : OFF</button>`;
    const redraw = () => {
      body.querySelector("#horror-room").textContent = `PIÈCE : ${rooms[stateGame.y][stateGame.x].toUpperCase()}`;
      body.querySelector("#horror-scene").textContent = stateGame.monster[0] === stateGame.x && stateGame.monster[1] === stateGame.y ? "◉　◉\n　▽" : stateGame.light ? "La pièce est éclairée…" : "La pièce est sombre…";
    };
    const move = (dx, dy) => {
      if (stateGame.ended) return;
      const nx = stateGame.x + dx, ny = stateGame.y + dy;
      if (nx < 0 || nx > 2 || ny < 0 || ny > 2) { body.querySelector("#horror-status").textContent = "Cette porte est verrouillée."; return; }
      stateGame.x = nx; stateGame.y = ny; stateGame.moves++;
      if (stateGame.moves % 2 === 0) {
        if (stateGame.monster[0] > 0) stateGame.monster[0]--;
        else stateGame.monster[1] = Math.min(2, stateGame.monster[1] + 1);
      }
      if (rooms[ny][nx] === "Exit") {
        stateGame.ended = true; body.querySelector("#horror-status").textContent = "Bravo, tu as trouvé la sortie !";
      } else if (stateGame.monster[0] === nx && stateGame.monster[1] === ny) {
        stateGame.ended = true; body.querySelector("#horror-status").textContent = "Jumpscare simulé — partie terminée.";
      } else body.querySelector("#horror-status").textContent = "Porte franchie.";
      redraw();
    };
    [["↑ Nord", 0, -1], ["← Ouest", -1, 0], ["→ Est", 1, 0], ["↓ Sud", 0, 1]].forEach(([label, dx, dy]) => {
      const control = button(label, () => move(dx, dy));
      body.querySelector("#horror-controls").append(control);
    });
    body.querySelector("#flashlight").addEventListener("click", event => {
      stateGame.light = !stateGame.light;
      event.currentTarget.textContent = `Lampe : ${stateGame.light ? "ON" : "OFF"}`;
      redraw();
    });
    redraw();
  }
  function runSecret(value) {
    const secret = value.trim().toLowerCase().replace(/\s+/g, " ");
    const actions = {
      "profile : admine": () => openProfile(),
      "glitch : 999": () => startGlitch("glitch", "Glitch RGB"),
      "matrix : secret": () => startGlitch("matrix", "Matrix"),
      "hacker : ultimate": () => { state.profile.username = "HACKER"; save(); toast("Mode Hacker activé."); },
      "system : unlock": () => toast("WINDOWS 12 • Build fictif • simulation isolée"),
      "ghost : 666": () => openHorror(),
      "windows : 12": () => toast("Bienvenue dans WINDOWS 12 ULTIMATE"),
    };
    if (!actions[secret]) return false;
    actions[secret]();
    return true;
  }
  initDesktop();
})();
