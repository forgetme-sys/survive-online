"use strict";

(() => {
  const { games, launchers, categories } = window.NexusCatalog;
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const storage = window.localStorage;
  const translations = {
    fr: {
      workspace: "ESPACE DE JEU", navHome: "Accueil", navStore: "Game store", navDownloads: "Téléchargements", navProfile: "Profil", systemReady: "SYSTÈME OPÉRATIONNEL", navSettings: "Paramètres",
      heroEyebrow: "LE GAMING, SANS FRONTIÈRES", heroTitle: "VOTRE PROCHAIN<br><span class=\"gradient-text\">UNIVERS</span> VOUS ATTEND.", heroDescription: "Découvrez vos prochains jeux favoris. Installez les lanceurs officiels, explorez le catalogue et gardez votre bibliothèque à portée de main.",
      exploreGames: "EXPLORER LES JEUX", openDownloads: "TÉLÉCHARGEMENTS", officialSources: "LIENS OFFICIELS UNIQUEMENT", gamesAvailable: "JEUX AU CATALOGUE", platformsSupported: "PLATEFORMES", officialLinks: "LIENS OFFICIELS", curatedCatalog: "CATALOGUE SÉLECTIONNÉ AVEC SOIN",
      featuredGames: "À LA UNE", viewAll: "TOUT LE CATALOGUE", popularGames: "POPULAIRES", discover: "DÉCOUVRIR", footerDisclaimer: "Plateforme indépendante — chaque jeu reste la propriété de son éditeur.",
      storeTitle: "TROUVEZ VOTRE<br><span class=\"gradient-text\">PROCHAIN JEU.</span>", storeDescription: "Des univers à explorer, sélectionnés auprès de leurs éditeurs et boutiques officielles.", searchPlaceholder: "Rechercher un jeu...", allPlatforms: "TOUT", filterBy: "FILTRER PAR", allGenres: "TOUS", officialStoreLinks: "LIENS VERS LES BOUTIQUES OFFICIELLES",
      downloadsTitle: "CENTRE DE<br><span class=\"gradient-text\">TÉLÉCHARGEMENT.</span>", downloadsDescription: "Installez les lanceurs officiels ou suivez vos téléchargements effectués depuis NEXUS.", secureConnection: "CONNEXION SÉCURISÉE", downloadNotice: "NEXUS télécharge uniquement des lanceurs officiels. Les jeux s'installent depuis leurs boutiques. Aucun fichier ne sera lancé sans votre accord.", officialLaunchers: "LANCEURS OFFICIELS", transferHistory: "TRANSFERTS", refresh: "ACTUALISER",
      androidTitle: "DANS VOTRE POCHE.", androidDescription: "Installez NEXUS comme application Web ou accédez aux pages Google Play des éditeurs.", installNexus: "INSTALLER NEXUS SUR VOTRE APPAREIL", pwaInstructions: "Sur Android, ouvrez ce site dans Chrome, puis choisissez « Installer l'application » ou « Ajouter à l'écran d'accueil » dans le menu.", installApp: "INSTALLER", androidGames: "JEUX ANDROID",
      profileTitle: "VOTRE PROFIL<br><span class=\"gradient-text\">VOTRE UNIVERS.</span>", profileDescription: "Votre identité joueur et votre progression restent enregistrées sur cet appareil.", localProfile: "PROFIL LOCAL · CET APPAREIL", editProfile: "MODIFIER", nexusCoins: "NEXUS COINS", games: "JEUX", accountAccess: "ACCÈS AU PROFIL", accountDescription: "Créez ou restaurez un profil local avec un nom d'utilisateur. Aucun mot de passe de boutique n'est demandé.", username: "NOM D'UTILISATEUR", chooseAvatar: "CHOISIR UN AVATAR", register: "CRÉER / ENREGISTRER", login: "CHARGER LE PROFIL",
      settingsTitle: "VOTRE ESPACE.<br><span class=\"gradient-text\">VOS RÈGLES.</span>", settingsDescription: "Personnalisez votre expérience NEXUS.", colorTheme: "Thème de couleur", colorThemeDescription: "Choisissez l'accent lumineux de votre interface.", animations: "Animations", animationsDescription: "Réduire les mouvements et particules animées.", volume: "Volume des effets", volumeDescription: "Ajustez le niveau du signal sonore d'interface.", language: "Langue", languageDescription: "Langue de l'interface.", securityFirst: "SÉCURITÉ AVANT TOUT", securityNote: "NEXUS ne collecte aucun identifiant de boutique, ne lance aucun installateur automatiquement et ouvre exclusivement les sources officielles enregistrées."
    },
    en: {
      workspace: "GAMING SPACE", navHome: "Home", navStore: "Game store", navDownloads: "Downloads", navProfile: "Profile", systemReady: "SYSTEM OPERATIONAL", navSettings: "Settings",
      heroEyebrow: "GAMING WITHOUT BORDERS", heroTitle: "YOUR NEXT<br><span class=\"gradient-text\">UNIVERSE</span> AWAITS.", heroDescription: "Discover your next favorite games. Install official launchers, explore the catalog, and keep your library close at hand.",
      exploreGames: "EXPLORE GAMES", openDownloads: "DOWNLOADS", officialSources: "OFFICIAL LINKS ONLY", gamesAvailable: "GAMES IN CATALOG", platformsSupported: "PLATFORMS", officialLinks: "OFFICIAL LINKS", curatedCatalog: "CAREFULLY CURATED CATALOG",
      featuredGames: "FEATURED", viewAll: "VIEW ALL GAMES", popularGames: "POPULAR", discover: "DISCOVER", footerDisclaimer: "Independent platform — each game remains the property of its publisher.",
      storeTitle: "FIND YOUR<br><span class=\"gradient-text\">NEXT GAME.</span>", storeDescription: "Worlds to explore, selected from official publishers and stores.", searchPlaceholder: "Search games...", allPlatforms: "ALL", filterBy: "FILTER BY", allGenres: "ALL", officialStoreLinks: "LINKS TO OFFICIAL STORES",
      downloadsTitle: "DOWNLOAD<br><span class=\"gradient-text\">CENTER.</span>", downloadsDescription: "Install official launchers or track downloads managed by NEXUS.", secureConnection: "SECURE CONNECTION", downloadNotice: "NEXUS downloads official launchers only. Games are installed from their stores. No file is launched without your consent.", officialLaunchers: "OFFICIAL LAUNCHERS", transferHistory: "TRANSFERS", refresh: "REFRESH",
      androidTitle: "IN YOUR POCKET.", androidDescription: "Install NEXUS as a web app or visit publishers' Google Play pages.", installNexus: "INSTALL NEXUS ON YOUR DEVICE", pwaInstructions: "On Android, open this site in Chrome, then choose “Install app” or “Add to Home screen” from the menu.", installApp: "INSTALL", androidGames: "ANDROID GAMES",
      profileTitle: "YOUR PROFILE<br><span class=\"gradient-text\">YOUR UNIVERSE.</span>", profileDescription: "Your player identity and progress stay on this device.", localProfile: "LOCAL PROFILE · THIS DEVICE", editProfile: "EDIT", nexusCoins: "NEXUS COINS", games: "GAMES", accountAccess: "PROFILE ACCESS", accountDescription: "Create or restore a local profile with a username. No store password is requested.", username: "USERNAME", chooseAvatar: "CHOOSE AN AVATAR", register: "CREATE / SAVE", login: "LOAD PROFILE",
      settingsTitle: "YOUR SPACE.<br><span class=\"gradient-text\">YOUR RULES.</span>", settingsDescription: "Personalize your NEXUS experience.", colorTheme: "Color theme", colorThemeDescription: "Choose your interface accent color.", animations: "Animations", animationsDescription: "Reduce motion and animated particles.", volume: "Effects volume", volumeDescription: "Adjust interface sound level.", language: "Language", languageDescription: "Interface language.", securityFirst: "SECURITY FIRST", securityNote: "NEXUS collects no store credentials, never launches installers automatically, and opens only registered official sources."
    }
  };
  const state = {
    page: "home",
    genre: "ALL",
    platform: "all",
    search: "",
    avatar: "N",
    downloads: [],
    secretClicks: 0,
    secretTimer: null,
    pwaPrompt: null,
    audioContext: null
  };

  function readJSON(key, fallback) {
    try {
      const value = storage.getItem(key);
      return value ? JSON.parse(value) : fallback;
    } catch (error) {
      console.error(`Unable to read ${key} from local storage`, error);
      return fallback;
    }
  }

  function writeJSON(key, value) {
    try {
      storage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(`Unable to save ${key} to local storage`, error);
      toast("Impossible d'enregistrer les données locales de cette application.", true);
    }
  }

  function toast(message, error = false) {
    const element = document.createElement("div");
    element.className = `toast${error ? " error" : ""}`;
    element.textContent = message;
    $("#toast-region").append(element);
    window.setTimeout(() => element.remove(), 4200);
  }

  function confirmAction(title, message, actionLabel = "CONFIRMER") {
    return new Promise(resolve => {
      const backdrop = $("#modal-backdrop");
      $("#modal-title").textContent = title;
      $("#modal-message").textContent = message;
      $("#modal-confirm").textContent = actionLabel;
      backdrop.hidden = false;
      const finish = result => {
        backdrop.hidden = true;
        $("#modal-confirm").removeEventListener("click", onConfirm);
        $("#modal-cancel").removeEventListener("click", onCancel);
        $("#modal-close").removeEventListener("click", onCancel);
        backdrop.removeEventListener("click", onBackdrop);
        document.removeEventListener("keydown", onKey);
        resolve(result);
      };
      const onConfirm = () => finish(true);
      const onCancel = () => finish(false);
      const onBackdrop = event => { if (event.target === backdrop) finish(false); };
      const onKey = event => { if (event.key === "Escape") finish(false); };
      $("#modal-confirm").addEventListener("click", onConfirm, { once: true });
      $("#modal-cancel").addEventListener("click", onCancel, { once: true });
      $("#modal-close").addEventListener("click", onCancel, { once: true });
      backdrop.addEventListener("click", onBackdrop);
      document.addEventListener("keydown", onKey);
    });
  }

  function navigate(page) {
    if (!document.getElementById(`page-${page}`)) return;
    state.page = page;
    $$(".page").forEach(element => element.classList.toggle("active", element.id === `page-${page}`));
    $$(".nav-link[data-page]").forEach(element => element.classList.toggle("active", element.dataset.page === page));
    $("#page-title").textContent = ({ home: "ACCUEIL", store: "GAME STORE", downloads: "DOWNLOADS", android: "ANDROID", profile: "PROFILE", settings: "SETTINGS", secret: "SECRET GLITCH" })[page] || page.toUpperCase();
    $("#sidebar").classList.remove("open");
    if (page === "downloads") refreshDownloads();
    if (page === "profile") renderProfile();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function makeCard(game, compact = false) {
    const card = document.createElement("article");
    card.className = "game-card";
    const art = document.createElement("div");
    art.className = "game-art";
    art.style.backgroundImage = `linear-gradient(0deg,rgba(14,15,25,.15),rgba(14,15,25,.03)),url("${game.image}")`;
    const badge = document.createElement("span");
    badge.className = `game-badge${game.price.startsWith("Gratuit") ? " free" : ""}`;
    badge.textContent = game.price.startsWith("Gratuit") ? "FREE TO PLAY" : "PAID";
    art.append(badge);
    const info = document.createElement("div");
    info.className = "game-info";
    const meta = document.createElement("div");
    meta.className = "game-meta";
    const platform = document.createElement("span");
    platform.textContent = game.platform;
    const genre = document.createElement("span");
    genre.className = "genre-mark";
    genre.textContent = game.genre;
    meta.append(platform, genre);
    const heading = document.createElement("h3");
    heading.textContent = game.title;
    const description = document.createElement("p");
    description.textContent = game.description;
    const bottom = document.createElement("div");
    bottom.className = "game-card-bottom";
    const version = document.createElement("span");
    version.className = "game-version";
    version.textContent = `${game.developer} · ${game.version}`;
    const actions = document.createElement("div");
    actions.className = "game-actions";
    const storeButton = document.createElement("button");
    storeButton.className = "card-action";
    storeButton.textContent = "BOUTIQUE ↗";
    storeButton.addEventListener("click", () => openGame(game, false));
    actions.append(storeButton);
    if (game.androidUrl) {
      const androidButton = document.createElement("button");
      androidButton.className = "card-action";
      androidButton.textContent = "ANDROID ↗";
      androidButton.addEventListener("click", () => openGame(game, true));
      actions.append(androidButton);
    }
    bottom.append(version, actions);
    info.append(meta, heading, description, bottom);
    card.append(art, info);
    if (compact) card.classList.add("compact-card");
    return card;
  }

  async function openGame(game, android = false) {
    const url = android && game.androidUrl ? game.androidUrl : game.url;
    if (window.nexus) {
      try {
        await window.nexus.openGame(game.id, android);
      } catch (error) {
        toast(error.message || "Impossible d'ouvrir la boutique officielle.", true);
        return;
      }
    } else {
      const opened = window.open(url, "_blank", "noopener,noreferrer");
      if (!opened) toast("Autorisez les fenêtres contextuelles pour ouvrir la boutique officielle.", true);
    }
    const visited = readJSON("nexus-visited-games", []);
    if (!visited.includes(game.id)) {
      visited.push(game.id);
      writeJSON("nexus-visited-games", visited);
      const profile = readJSON("nexus-profile", defaultProfile());
      profile.xp = (Number(profile.xp) || 0) + 25;
      profile.coins = (Number(profile.coins) || 0) + 10;
      writeJSON("nexus-profile", profile);
      renderProfile();
    }
  }

  function renderGames() {
    $("#featured-games").replaceChildren(...games.filter(game => game.featured).slice(0, 4).map(game => makeCard(game)));
    $("#popular-games").replaceChildren(...games.filter(game => game.popular).slice(0, 4).map(game => makeCard(game, true)));
    $("#stat-games").textContent = String(games.length).padStart(2, "0");
    $("#genre-filters").replaceChildren($("#genre-filters").firstElementChild);
    const allButton = document.createElement("button");
    allButton.className = `filter-chip${state.genre === "ALL" ? " active" : ""}`;
    allButton.dataset.genre = "ALL";
    allButton.dataset.i18n = "allGenres";
    allButton.textContent = translations[storage.getItem("nexus-language") || "fr"].allGenres;
    $("#genre-filters").append(allButton);
    for (const category of categories) {
      const button = document.createElement("button");
      button.className = `filter-chip${state.genre === category ? " active" : ""}`;
      button.dataset.genre = category;
      button.textContent = category;
      $("#genre-filters").append(button);
    }
    renderStore();
    $("#android-games").replaceChildren(...games.filter(game => game.androidUrl).map(game => makeCard(game)));
  }

  function renderStore() {
    const filtered = games.filter(game => {
      const matchesSearch = `${game.title} ${game.developer} ${game.genre} ${game.description}`.toLowerCase().includes(state.search.toLowerCase());
      const matchesGenre = state.genre === "ALL" || game.genre === state.genre;
      const matchesPlatform = state.platform === "all" || game.platform.includes(state.platform);
      return matchesSearch && matchesGenre && matchesPlatform;
    });
    $("#store-games").replaceChildren(...(filtered.length ? filtered.map(game => makeCard(game)) : []));
    if (!filtered.length) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.innerHTML = "<b>Aucun jeu trouvé.</b>Essayez un autre nom ou filtre.";
      $("#store-games").append(empty);
    }
    $("#result-count").textContent = `${filtered.length} JEU${filtered.length > 1 ? "X" : ""} TROUVÉ${filtered.length > 1 ? "S" : ""}`;
  }

  function renderLaunchers() {
    $("#launcher-list").replaceChildren(...launchers.map(launcher => {
      const card = document.createElement("article");
      card.className = "launcher-card";
      const top = document.createElement("div");
      top.className = "launcher-card-top";
      const icon = document.createElement("div");
      icon.className = "launcher-icon";
      icon.textContent = launcher.title === "Steam" ? "S" : launcher.title === "Riot Client" ? "R" : "E";
      const verified = document.createElement("span");
      verified.className = "verified-mark";
      verified.textContent = "✓ OFFICIEL";
      top.append(icon, verified);
      const title = document.createElement("h3");
      title.textContent = launcher.title;
      const description = document.createElement("p");
      description.textContent = launcher.description;
      const version = document.createElement("div");
      version.className = "launcher-version";
      version.textContent = `${launcher.publisher} · ${launcher.version}`;
      const button = document.createElement("button");
      button.className = "button button-ghost launcher-download";
      button.textContent = launcher.extension ? "TÉLÉCHARGER L'INSTALLATEUR ⇩" : "OUVRIR LA PAGE OFFICIELLE ↗";
      button.addEventListener("click", () => startLauncherDownload(launcher));
      card.append(top, title, description, version, button);
      return card;
    }));
  }

  async function startLauncherDownload(launcher) {
    if (!launcher.extension) {
      if (window.nexus) {
        try { await window.nexus.openLauncher(launcher.id); }
        catch (error) { toast(error.message || "Impossible d'ouvrir le site officiel.", true); }
      } else {
        const opened = window.open(launcher.url, "_blank", "noopener,noreferrer");
        if (!opened) toast("Autorisez les fenêtres contextuelles pour ouvrir le téléchargement officiel.", true);
      }
      return;
    }
    if (!window.nexus) {
      toast("Le téléchargement avec progression et reprise est disponible dans l'application Windows. Consultez le site officiel pour télécharger ce lanceur.", true);
      const opened = window.open(launcher.url, "_blank", "noopener,noreferrer");
      if (!opened) toast("Autorisez les fenêtres contextuelles pour ouvrir le site officiel.", true);
      return;
    }
    const accepted = await confirmAction("TÉLÉCHARGER UN INSTALLATEUR", `${launcher.title} sera téléchargé depuis son serveur officiel.\n\nLe fichier ne sera pas lancé automatiquement. Sa signature pourra être vérifiée après le téléchargement.`, "TÉLÉCHARGER");
    if (!accepted) return;
    try {
      await window.nexus.startDownload(launcher.id);
      toast(`Téléchargement de ${launcher.title} démarré.`);
    } catch (error) {
      toast(error.message || "Le téléchargement n'a pas pu démarrer.", true);
    }
  }

  function defaultProfile() {
    return { username: "PLAYER ONE", avatar: "N", xp: 0, coins: 100 };
  }

  const avatars = ["N", "✦", "◈", "⚡", "☾", "✳"];

  function renderProfile() {
    const profile = readJSON("nexus-profile", defaultProfile());
    const username = (typeof profile.username === "string" && profile.username.trim() ? profile.username.trim() : "PLAYER ONE").slice(0, 24);
    const avatar = avatars.includes(profile.avatar) ? profile.avatar : "N";
    const xp = Math.max(0, Number(profile.xp) || 0);
    const coins = Math.max(0, Number(profile.coins) || 0);
    const level = Math.floor(xp / 500) + 1;
    const nextLevelXp = xp % 500;
    $("#top-username").textContent = username.toUpperCase();
    $("#top-avatar").textContent = avatar;
    $("#profile-name").textContent = username.toUpperCase();
    $("#profile-avatar").textContent = avatar;
    $("#profile-level").textContent = `NIVEAU ${String(level).padStart(2, "0")}`;
    $("#profile-xp").textContent = String(xp);
    $("#profile-coins").textContent = String(coins);
    $("#profile-games-count").textContent = String(readJSON("nexus-visited-games", []).length);
    $("#xp-progress-text").textContent = `${nextLevelXp} / 500 XP`;
    $("#xp-progress").style.width = `${(nextLevelXp / 500) * 100}%`;
    $("#username-input").value = username;
    state.avatar = avatar;
    $$(".avatar-option").forEach(button => button.classList.toggle("active", button.dataset.avatar === avatar));
  }

  function saveProfile(messageKey) {
    const name = $("#username-input").value.trim();
    const message = $("#account-message");
    if (!name || name.length < 2) {
      message.textContent = "Le nom d'utilisateur doit contenir au moins 2 caractères.";
      message.style.color = "var(--danger)";
      return;
    }
    const current = readJSON("nexus-profile", defaultProfile());
    const profile = {
      username: name.slice(0, 24),
      avatar: state.avatar,
      xp: Math.max(0, Number(current.xp) || 0),
      coins: Math.max(0, Number(current.coins) || 100)
    };
    writeJSON("nexus-profile", profile);
    message.style.color = "var(--green)";
    message.textContent = messageKey === "register" ? "Profil enregistré sur cet appareil." : "Profil local chargé.";
    renderProfile();
  }

  function applyLanguage(language) {
    const lang = language === "en" ? "en" : "fr";
    storage.setItem("nexus-language", lang);
    document.documentElement.lang = lang;
    for (const element of $$("[data-i18n]")) {
      const value = translations[lang][element.dataset.i18n];
      if (value) element.textContent = value;
    }
    for (const element of $$("[data-i18n-html]")) {
      const value = translations[lang][element.dataset.i18nHtml];
      if (value) element.innerHTML = value;
    }
    for (const element of $$("[data-i18n-placeholder]")) {
      const value = translations[lang][element.dataset.i18nPlaceholder];
      if (value) element.placeholder = value;
    }
    $("#language-select").value = lang;
    renderGames();
    renderProfile();
  }

  function saveSettings() {
    const settings = {
      theme: $("#theme-select").value,
      reducedMotion: $("#animations-toggle").checked,
      volume: Number($("#volume-slider").value),
      language: $("#language-select").value
    };
    writeJSON("nexus-settings", settings);
    document.documentElement.dataset.theme = settings.theme;
    document.body.classList.toggle("no-animations", settings.reducedMotion);
    $("#volume-value").textContent = `${settings.volume}%`;
  }

  function playSound() {
    const volume = Number($("#volume-slider").value);
    if (!volume) {
      toast("Le volume est réglé sur 0 %.");
      return;
    }
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) throw new Error("Audio non pris en charge par ce navigateur.");
      state.audioContext ||= new AudioContext();
      const oscillator = state.audioContext.createOscillator();
      const gain = state.audioContext.createGain();
      oscillator.type = "sine";
      oscillator.frequency.setValueAtTime(660, state.audioContext.currentTime);
      oscillator.frequency.exponentialRampToValueAtTime(990, state.audioContext.currentTime + 0.13);
      gain.gain.setValueAtTime(volume / 100 * 0.08, state.audioContext.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, state.audioContext.currentTime + 0.2);
      oscillator.connect(gain);
      gain.connect(state.audioContext.destination);
      oscillator.start();
      oscillator.stop(state.audioContext.currentTime + 0.2);
    } catch (error) {
      toast(error.message || "Impossible de jouer le son de test.", true);
    }
  }

  async function downloadAction(id, action) {
    if (!window.nexus) {
      toast("Le gestionnaire natif est disponible dans l'application Windows.", true);
      return;
    }
    try {
      if (action === "install") {
        const verification = await window.nexus.verifyDownload(id);
        if (verification.sha256) {
          const signer = verification.signer ? `\nÉditeur : ${verification.signer}` : "";
          const signature = verification.signatureValid ? "Signature Authenticode valide." : `Signature Authenticode : ${verification.signature || "invalide"}.\nL'éditeur de ce fichier n'a pas pu être vérifié.`;
          const proceed = await confirmAction("INSTALLER — DERNIÈRE VÉRIFICATION", `${signature}${signer}\nSHA-256 calculé : ${verification.sha256}\n\nVérifiez que l'éditeur correspond à la source officielle. L'installation ne démarre qu'après cette confirmation.`, "LANCER L'INSTALLATEUR");
          if (!proceed) return;
          if (!verification.signatureValid) {
            const acknowledge = await confirmAction("SIGNATURE NON VALIDÉE", "Le certificat de signature ne peut pas être confirmé comme valide. Voulez-vous vraiment lancer ce fichier téléchargé depuis la source officielle ?", "JE COMPRENDS — CONTINUER");
            if (!acknowledge) return;
          }
          await window.nexus.installDownload(id);
          toast("Installateur lancé après votre confirmation.");
        } else {
          toast("Le fichier n'est pas terminé ou sa vérification a échoué.", true);
        }
        return;
      }
      if (action === "verify") {
        const result = await window.nexus.verifyDownload(id);
        const details = [`SHA-256 : ${result.sha256 || "indisponible"}`, `Signature Authenticode : ${result.signature || "inconnue"}`, result.signer ? `Éditeur : ${result.signer}` : "Éditeur non identifié"];
        toast(details.join(" · "), !result.signatureValid);
        return;
      }
      if (action === "open") {
        await window.nexus.showDownload(id);
        return;
      }
      if (action === "pause" || action === "resume" || action === "cancel") {
        await window.nexus.controlDownload(id, action);
      }
    } catch (error) {
      toast(error.message || "L'action sur le téléchargement a échoué.", true);
    }
  }

  function formatBytes(bytes) {
    if (!Number.isFinite(bytes) || bytes < 0) return "0 B";
    const units = ["B", "KB", "MB", "GB"];
    let value = bytes;
    let index = 0;
    while (value >= 1024 && index < units.length - 1) {
      value /= 1024;
      index++;
    }
    return `${value.toFixed(index ? 1 : 0)} ${units[index]}`;
  }

  function renderDownloads(downloads = state.downloads) {
    state.downloads = downloads;
    $("#download-count").textContent = String(downloads.filter(item => item.status === "downloading").length);
    const list = $("#downloads-list");
    if (!downloads.length) {
      list.innerHTML = '<div class="empty-downloads">Aucun transfert pour le moment.<br>Choisissez un lanceur officiel ci-dessus pour commencer.</div>';
      return;
    }
    list.replaceChildren(...downloads.map(item => {
      const row = document.createElement("article");
      row.className = "download-item";
      const icon = document.createElement("div");
      icon.className = "download-file-icon";
      icon.textContent = "⇩";
      const details = document.createElement("div");
      details.className = "download-details";
      const title = document.createElement("h3");
      title.textContent = item.title;
      const subtitle = document.createElement("p");
      subtitle.textContent = `${item.filename || item.id} · ${formatBytes(item.received || 0)}${item.total ? ` / ${formatBytes(item.total)}` : ""}${item.speed ? ` · ${formatBytes(item.speed)}/s` : ""}`;
      details.append(title, subtitle);
      const progress = document.createElement("div");
      progress.className = "download-progress";
      const fill = document.createElement("span");
      fill.style.width = `${Math.max(0, Math.min(100, Number(item.progress) || 0))}%`;
      progress.append(fill);
      details.append(progress);
      const status = document.createElement("div");
      status.className = "download-status";
      status.textContent = item.error || ({ queued: "EN ATTENTE", downloading: "TÉLÉCHARGEMENT EN COURS", paused: "EN PAUSE", completed: "TÉLÉCHARGEMENT TERMINÉ — NON EXÉCUTÉ", error: "ÉCHEC", cancelled: "ANNULÉ" })[item.status] || item.status;
      details.append(status);
      const actions = document.createElement("div");
      actions.className = "download-actions";
      const addAction = (label, action) => {
        const button = document.createElement("button");
        button.className = "download-action";
        button.textContent = label;
        button.addEventListener("click", () => downloadAction(item.id, action));
        actions.append(button);
      };
      if (item.status === "downloading") addAction("PAUSE", "pause");
      if (item.status === "paused") addAction("REPRENDRE", "resume");
      if (item.status === "completed") {
        addAction("VÉRIFIER", "verify");
        addAction("INSTALLER", "install");
        addAction("EMPLACEMENT", "open");
      }
      if (["downloading", "paused", "queued", "error"].includes(item.status)) addAction("ANNULER", "cancel");
      row.append(icon, details, actions);
      return row;
    }));
  }

  async function refreshDownloads() {
    if (!window.nexus) {
      renderDownloads([]);
      return;
    }
    try {
      renderDownloads(await window.nexus.getDownloads());
    } catch (error) {
      toast(error.message || "Impossible de lire l'historique des téléchargements.", true);
    }
  }

  function appendTerminal(message, isError = false) {
    const line = document.createElement("span");
    line.textContent = `> ${message}`;
    if (isError) line.style.color = "var(--danger)";
    $("#terminal-output").append(line);
    $("#terminal-output").scrollTop = $("#terminal-output").scrollHeight;
  }

  function setupSecretPanel() {
    const brand = $(".brand");
    const triggerSecret = event => {
      event.preventDefault();
      state.secretClicks++;
      window.clearTimeout(state.secretTimer);
      state.secretTimer = window.setTimeout(() => { state.secretClicks = 0; }, 2500);
      if (state.secretClicks >= 5) {
        state.secretClicks = 0;
        navigate("secret");
        appendTerminal("SECRET CHANNEL OPEN — WELCOME, PLAYER.");
      } else if (brand) {
        navigate("home");
      }
    };
    brand.addEventListener("click", triggerSecret);
    $("#secret-logo").addEventListener("click", () => {
      state.secretClicks++;
      window.clearTimeout(state.secretTimer);
      state.secretTimer = window.setTimeout(() => { state.secretClicks = 0; }, 2500);
      if (state.secretClicks >= 5) {
        state.secretClicks = 0;
        navigate("secret");
      } else {
        toast(`${5 - state.secretClicks} clic${state.secretClicks === 4 ? "" : "s"} restant${state.secretClicks === 4 ? "" : "s"} pour détecter le signal.`);
      }
    });
    $("#secret-code-form").addEventListener("submit", event => {
      event.preventDefault();
      const input = $("#secret-code");
      const code = input.value.trim().toUpperCase();
      if (code === "NEXUS777") {
        appendTerminal("ACCESS GRANTED — EASTER EGG UNLOCKED.");
        document.body.classList.add("glitch-active");
        toast("Code secret valide. Bienvenue dans SECRET GLITCH.");
      } else {
        appendTerminal("ACCESS DENIED — UNKNOWN ACCESS CODE.", true);
      }
      input.value = "";
    });
    $("#glitch-toggle").addEventListener("click", event => {
      const active = document.body.classList.toggle("glitch-active");
      event.currentTarget.textContent = active ? "DÉSACTIVER GLITCH MODE" : "ACTIVER GLITCH MODE";
    });
    $("#matrix-toggle").addEventListener("click", event => {
      const active = document.body.classList.toggle("matrix-active");
      event.currentTarget.textContent = active ? "DÉSACTIVER MATRIX" : "MATRIX EFFECT";
    });
    $("#nightmare-toggle").addEventListener("click", event => {
      const active = document.body.classList.toggle("nightmare-mode");
      event.currentTarget.textContent = active ? "DÉSACTIVER NIGHTMARE" : "NIGHTMARE MODE";
    });
    $("#terminal-clear").addEventListener("click", () => {
      $("#terminal-output").replaceChildren();
      appendTerminal("NEXUS SYSTEM ONLINE");
      appendTerminal("CHANNEL ENCRYPTION: ACTIVE");
      appendTerminal("ENTER ACCESS CODE:");
    });
  }

  function setupParticles() {
    const canvas = $("#particles");
    const context = canvas.getContext("2d");
    if (!context) return;
    let points = [];
    let frame;
    const resize = () => {
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = window.innerWidth * ratio;
      canvas.height = window.innerHeight * ratio;
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      const count = document.body.classList.contains("no-animations") ? 0 : Math.min(45, Math.floor(window.innerWidth / 29));
      points = Array.from({ length: count }, () => ({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        radius: Math.random() * 1.5 + 0.4,
        speed: Math.random() * 0.24 + 0.05,
        alpha: Math.random() * 0.35 + 0.1
      }));
    };
    const draw = () => {
      context.clearRect(0, 0, window.innerWidth, window.innerHeight);
      for (const point of points) {
        context.beginPath();
        context.arc(point.x, point.y, point.radius, 0, Math.PI * 2);
        context.fillStyle = `rgba(174,151,255,${point.alpha})`;
        context.fill();
        point.y -= point.speed;
        if (point.y < -2) {
          point.y = window.innerHeight + 2;
          point.x = Math.random() * window.innerWidth;
        }
      }
      frame = window.requestAnimationFrame(draw);
    };
    resize();
    draw();
    window.addEventListener("resize", resize);
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) window.cancelAnimationFrame(frame);
      else draw();
    });
  }

  function init() {
    const initialSettings = readJSON("nexus-settings", { theme: "violet", reducedMotion: false, volume: 18, language: "fr" });
    $("#theme-select").value = ["violet", "blue", "cyan"].includes(initialSettings.theme) ? initialSettings.theme : "violet";
    $("#animations-toggle").checked = Boolean(initialSettings.reducedMotion);
    $("#volume-slider").value = Math.max(0, Math.min(100, Number(initialSettings.volume) || 0));
    document.documentElement.dataset.theme = $("#theme-select").value;
    document.body.classList.toggle("no-animations", $("#animations-toggle").checked);
    $("#volume-value").textContent = `${$("#volume-slider").value}%`;

    for (const avatar of avatars) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "avatar-option";
      button.dataset.avatar = avatar;
      button.textContent = avatar;
      button.setAttribute("aria-label", `Avatar ${avatar}`);
      button.addEventListener("click", () => {
        state.avatar = avatar;
        $$(".avatar-option").forEach(option => option.classList.toggle("active", option === button));
      });
      $("#avatar-options").append(button);
    }

    renderGames();
    renderLaunchers();
    renderProfile();
    for (const button of $$("[data-page]")) {
      button.addEventListener("click", () => navigate(button.dataset.page));
    }
    $("#game-search").addEventListener("input", event => {
      state.search = event.target.value.trim();
      renderStore();
    });
    $("#genre-filters").addEventListener("click", event => {
      const button = event.target.closest("[data-genre]");
      if (!button) return;
      state.genre = button.dataset.genre;
      $$(".filter-chip", $("#genre-filters")).forEach(chip => chip.classList.toggle("active", chip === button));
      renderStore();
    });
    $$(".platform-filter").forEach(button => button.addEventListener("click", () => {
      state.platform = button.dataset.platform;
      $$(".platform-filter").forEach(item => item.classList.toggle("active", item === button));
      renderStore();
    }));
    $("#mobile-menu").addEventListener("click", () => $("#sidebar").classList.toggle("open"));
    $("#edit-profile").addEventListener("click", () => {
      $("#username-input").focus();
      $("#username-input").scrollIntoView({ behavior: "smooth", block: "center" });
    });
    $("#register-profile").addEventListener("click", () => saveProfile("register"));
    $("#login-profile").addEventListener("click", () => {
      const profile = readJSON("nexus-profile", null);
      if (!profile) {
        $("#account-message").textContent = "Aucun profil local enregistré. Créez-en un avec votre nom d'utilisateur.";
        $("#account-message").style.color = "var(--danger)";
        return;
      }
      $("#username-input").value = profile.username;
      state.avatar = profile.avatar;
      renderProfile();
      $("#account-message").textContent = "Profil local chargé sur cet appareil.";
      $("#account-message").style.color = "var(--green)";
    });
    $("#theme-select").addEventListener("change", saveSettings);
    $("#animations-toggle").addEventListener("change", () => {
      saveSettings();
      setupParticles();
    });
    $("#volume-slider").addEventListener("input", saveSettings);
    $("#language-select").addEventListener("change", event => {
      saveSettings();
      applyLanguage(event.target.value);
    });
    $("#test-sound").addEventListener("click", playSound);
    $("#refresh-downloads").addEventListener("click", refreshDownloads);
    setupSecretPanel();
    setupParticles();
    applyLanguage(storage.getItem("nexus-language") || initialSettings.language || "fr");

    if (window.nexus) {
      window.nexus.onDownloadsChanged(renderDownloads);
      refreshDownloads();
    } else {
      renderDownloads([]);
      const notice = $("#download-notice");
      const paragraph = notice.querySelector("p");
      paragraph.textContent = "Sur le site Web, les téléchargements de jeux sont fournis par leurs boutiques officielles. Le gestionnaire avec progression réelle est disponible dans l'application Windows.";
    }

    window.addEventListener("beforeinstallprompt", event => {
      event.preventDefault();
      state.pwaPrompt = event;
      $("#install-pwa").hidden = false;
    });
    $("#install-pwa").addEventListener("click", async () => {
      if (!state.pwaPrompt) {
        toast("Sur Chrome Android, utilisez le menu ⋮ puis « Installer l'application ».");
        return;
      }
      state.pwaPrompt.prompt();
      const result = await state.pwaPrompt.userChoice;
      if (result.outcome === "accepted") toast("Installation de NEXUS confirmée.");
      state.pwaPrompt = null;
      $("#install-pwa").hidden = true;
    });
    if ("serviceWorker" in navigator && location.protocol !== "file:") {
      navigator.serviceWorker.register("./service-worker.js").catch(error => {
        console.error("Service worker registration failed", error);
        toast("Le mode hors ligne n'a pas pu être activé.", true);
      });
    }
    document.addEventListener("keydown", event => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        navigate("store");
        $("#game-search").focus();
      }
    });
  }

  init();
})();
