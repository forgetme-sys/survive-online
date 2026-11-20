const STORAGE_KEY = "keyquest-game-v1";
const POINTS_PER_LEVEL = 25;

const worlds = [
  { id: "meadow", name: "Prairie paisible", requirement: 0, icon: "✦" },
  { id: "desert", name: "Désert doré", requirement: 50, icon: "☼" },
  { id: "neon", name: "Néon nocturne", requirement: 150, icon: "✧" },
];

const skins = [
  { id: "steve", name: "Steve", requirement: 0 },
  { id: "creeper", name: "Creeper", requirement: 20 },
  { id: "enderman", name: "Enderman", requirement: 60 },
  { id: "astronaut", name: "Astronaute", requirement: 120 },
];

const scoreLabel = document.querySelector("#score");
const levelLabel = document.querySelector("#level-label");
const nextLevelLabel = document.querySelector("#next-level-label");
const progressLabel = document.querySelector("#level-progress-label");
const progressTrack = document.querySelector("#progress-track");
const progressFill = document.querySelector("#progress-fill");
const worldList = document.querySelector("#world-list");
const skinList = document.querySelector("#skin-list");
const currentWorldLabel = document.querySelector("#current-world");
const worldIcon = document.querySelector("#world-icon");
const arena = document.querySelector("#arena");
const avatar = document.querySelector("#avatar");
const skinTotal = document.querySelector("#skin-total");
const saveStatus = document.querySelector("#save-status");
const tapButton = document.querySelector("#tap-button");

function readProgress() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return { points: 0, world: "meadow", skin: "steve" };

    const parsed = JSON.parse(saved);
    const points = Number.isSafeInteger(parsed.points) && parsed.points >= 0 ? parsed.points : 0;
    const selectedWorld = worlds.find((world) => world.id === parsed.world);
    const selectedSkin = skins.find((skin) => skin.id === parsed.skin);
    return {
      points,
      world: selectedWorld && selectedWorld.requirement <= points ? selectedWorld.id : "meadow",
      skin: selectedSkin && selectedSkin.requirement <= points ? selectedSkin.id : "steve",
    };
  } catch (error) {
    console.error("Impossible de charger la progression.", error);
    saveStatus.textContent = "Chargement impossible : la progression n’a pas pu être lue.";
    return { points: 0, world: "meadow", skin: "steve" };
  }
}

const progress = readProgress();

function saveProgress() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
    saveStatus.textContent = "Ta progression est sauvegardée sur cet appareil.";
  } catch (error) {
    console.error("Impossible d’enregistrer la progression.", error);
    saveStatus.textContent = "Sauvegarde impossible : vérifie l’espace disponible de ton navigateur.";
  }
}

function renderWorlds() {
  let highestUnlocked = worlds[0];

  for (const world of worlds) {
    const button = worldList.querySelector(`[data-world="${world.id}"]`);
    const unlocked = progress.points >= world.requirement;
    const selected = progress.world === world.id && unlocked;
    if (unlocked) highestUnlocked = world;

    button.disabled = !unlocked;
    button.classList.toggle("is-locked", !unlocked);
    button.classList.toggle("is-selected", selected);
    button.setAttribute("aria-pressed", String(selected));
    button.querySelector("small").textContent = unlocked
      ? `MONDE ${String(worlds.indexOf(world) + 1).padStart(2, "0")} · DÉBLOQUÉ`
      : `MONDE ${String(worlds.indexOf(world) + 1).padStart(2, "0")} · ${world.requirement} POINTS`;
    button.querySelector(".world-status").textContent = unlocked ? (selected ? "✓" : "↗") : "⌑";
  }

  if (progress.points >= worlds.find((world) => world.id === progress.world).requirement) {
    return;
  }

  progress.world = highestUnlocked.id;
}

function renderSkins() {
  let unlockedCount = 0;
  const selectedSkin = skins.find((skin) => skin.id === progress.skin);

  for (const skin of skins) {
    const button = skinList.querySelector(`[data-skin="${skin.id}"]`);
    const unlocked = progress.points >= skin.requirement;
    const selected = progress.skin === skin.id && unlocked;
    if (unlocked) unlockedCount += 1;

    button.disabled = !unlocked;
    button.classList.toggle("is-locked", !unlocked);
    button.classList.toggle("is-selected", selected);
    button.setAttribute("aria-pressed", String(selected));
    button.querySelector(".skin-requirement").textContent = unlocked ? "✓" : String(skin.requirement);
    button.querySelector(".skin-requirement").classList.toggle("skin-lock", unlocked);
    button.setAttribute(
      "aria-label",
      unlocked ? `Choisir ${skin.name}` : `Skin ${skin.name}, débloqué à ${skin.requirement} points`,
    );
  }

  skinTotal.textContent = `${unlockedCount} / ${skins.length}`;
  avatar.className = `avatar avatar-${selectedSkin.id}`;
}

function render() {
  const level = Math.floor(progress.points / POINTS_PER_LEVEL) + 1;
  const levelProgress = progress.points % POINTS_PER_LEVEL;
  const activeWorld = worlds.find((world) => world.id === progress.world);

  scoreLabel.textContent = progress.points.toLocaleString("fr-FR");
  levelLabel.textContent = String(level);
  nextLevelLabel.textContent = `Niveau ${level + 1}`;
  progressLabel.textContent = `${levelProgress} / ${POINTS_PER_LEVEL} XP`;
  progressFill.style.width = `${(levelProgress / POINTS_PER_LEVEL) * 100}%`;
  progressTrack.setAttribute("aria-valuenow", String(levelProgress));
  progressTrack.setAttribute("aria-valuemax", String(POINTS_PER_LEVEL));
  currentWorldLabel.textContent = activeWorld.name;
  worldIcon.textContent = activeWorld.icon;
  arena.dataset.world = activeWorld.id;

  renderWorlds();
  renderSkins();
}

function earnPoint() {
  progress.points += 1;
  render();
  saveProgress();

  tapButton.classList.remove("is-tapping");
  requestAnimationFrame(() => {
    tapButton.classList.add("is-tapping");
    window.setTimeout(() => tapButton.classList.remove("is-tapping"), 160);
  });
}

tapButton.addEventListener("click", earnPoint);

worldList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-world]");
  if (!button || button.disabled) return;

  progress.world = button.dataset.world;
  render();
  saveProgress();
});

skinList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-skin]");
  if (!button || button.disabled) return;

  progress.skin = button.dataset.skin;
  render();
  saveProgress();
});

window.addEventListener("keydown", (event) => {
  if (
    event.repeat ||
    event.ctrlKey ||
    event.metaKey ||
    event.altKey ||
    ["Shift", "Control", "Alt", "Meta", "Tab", "CapsLock", "Escape"].includes(event.key) ||
    (event.target instanceof Element && event.target.closest("button, input, textarea, select, [contenteditable='true']"))
  ) {
    return;
  }

  if (event.code === "Space") event.preventDefault();
  earnPoint();
});

render();
