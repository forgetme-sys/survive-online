const skinCanvas = document.querySelector("#skinCanvas");
const skinContext = skinCanvas.getContext("2d", { willReadFrequently: true });
const gridCanvas = document.querySelector("#gridCanvas");
const gridContext = gridCanvas.getContext("2d");
const previewCanvas = document.querySelector("#previewCanvas");
const previewContext = previewCanvas.getContext("2d");
const colorInput = document.querySelector("#colorInput");
const colorHex = document.querySelector("#colorHex");
const cursorPosition = document.querySelector("#cursorPosition");
const canvasWrap = document.querySelector("#canvasWrap");
const zoomLabel = document.querySelector("#zoomLabel");
const saveStatus = document.querySelector("#saveStatus");

const SIZE = 64;
const STORAGE_KEY = "pixelforge-skin-v2";
const pixels = new Uint8ClampedArray(SIZE * SIZE * 4);
let activeTool = "pencil";
let currentColor = "#68d391";
let drawing = false;
let gridVisible = true;
let zoom = 8;
let history = [];
let historyIndex = -1;
let animation = "idle";
let animationSpeed = 5;
let animationStart = performance.now();
let saveTimer;

function renderSkin() {
  const image = skinContext.createImageData(SIZE, SIZE);
  image.data.set(pixels);
  const smallCanvas = document.createElement("canvas");
  smallCanvas.width = SIZE;
  smallCanvas.height = SIZE;
  smallCanvas.getContext("2d").putImageData(image, 0, 0);
  skinContext.clearRect(0, 0, SIZE * 8, SIZE * 8);
  skinContext.imageSmoothingEnabled = false;
  skinContext.drawImage(smallCanvas, 0, 0, SIZE * 8, SIZE * 8);
  drawGrid();
}

function drawGrid() {
  gridContext.clearRect(0, 0, 512, 512);
  if (!gridVisible) return;
  gridContext.strokeStyle = "rgba(15, 20, 14, .32)";
  gridContext.lineWidth = 1;
  gridContext.beginPath();
  for (let i = 0; i <= SIZE; i++) {
    const coordinate = i * 8 + 0.5;
    gridContext.moveTo(coordinate, 0);
    gridContext.lineTo(coordinate, 512);
    gridContext.moveTo(0, coordinate);
    gridContext.lineTo(512, coordinate);
  }
  gridContext.stroke();
  drawUVRegions();
}

function drawUVRegions() {
  const regions = [
    ["TÊTE · CÔTÉ", 0, 8, 8, 8], ["TÊTE · FACE", 8, 8, 8, 8],
    ["TÊTE · CÔTÉ", 16, 8, 8, 8], ["TÊTE · DOS", 24, 8, 8, 8],
    ["TÊTE · DESSUS", 8, 0, 8, 8], ["TÊTE · DESSOUS", 16, 0, 8, 8],
    ["CORPS · CÔTÉ", 16, 20, 4, 12], ["CORPS · FACE", 20, 20, 8, 12],
    ["CORPS · CÔTÉ", 28, 20, 4, 12], ["CORPS · DOS", 32, 20, 8, 12],
    ["JAMBE · FACE", 4, 20, 4, 12], ["BRAS · FACE", 44, 20, 4, 12],
    ["JAMBE · FACE", 20, 52, 4, 12], ["BRAS · FACE", 36, 52, 4, 12],
    ["CHAPEAU", 40, 8, 8, 8], ["VESTE", 20, 36, 8, 12],
  ];
  gridContext.save();
  gridContext.font = "bold 7px DM Mono, monospace";
  gridContext.textAlign = "center";
  gridContext.textBaseline = "middle";
  for (const [label, x, y, width, height] of regions) {
    const isOuter = label === "CHAPEAU" || label === "VESTE" || (y >= 32 && x >= 32);
    gridContext.strokeStyle = isOuter ? "rgba(130,184,248,.58)" : "rgba(165,232,135,.62)";
    gridContext.lineWidth = 1;
    gridContext.strokeRect(x * 8 + 1.5, y * 8 + 1.5, width * 8 - 3, height * 8 - 3);
    if (width >= 8 && height >= 8) {
      gridContext.fillStyle = isOuter ? "rgba(130,184,248,.8)" : "rgba(165,232,135,.8)";
      gridContext.fillText(label, (x + width / 2) * 8, (y + height / 2) * 8);
    }
  }
  gridContext.restore();
}

function cssColorToRgba(color) {
  if (color === "transparent") return [0, 0, 0, 0];
  const hex = color.replace("#", "");
  return [parseInt(hex.slice(0, 2), 16), parseInt(hex.slice(2, 4), 16), parseInt(hex.slice(4, 6), 16), 255];
}

function colorAt(x, y) {
  const offset = (y * SIZE + x) * 4;
  return Array.from(pixels.slice(offset, offset + 4));
}

function setPixel(x, y, rgba) {
  if (x < 0 || y < 0 || x >= SIZE || y >= SIZE) return;
  const offset = (y * SIZE + x) * 4;
  pixels.set(rgba, offset);
  skinContext.clearRect(x * 8, y * 8, 8, 8);
  renderSkin();
}

function fillArea(startX, startY, replacement) {
  const target = colorAt(startX, startY);
  if (target.every((value, i) => value === replacement[i])) return;
  const queue = [[startX, startY]];
  const visited = new Uint8Array(SIZE * SIZE);
  while (queue.length) {
    const [x, y] = queue.pop();
    if (x < 0 || y < 0 || x >= SIZE || y >= SIZE) continue;
    const index = y * SIZE + x;
    if (visited[index]) continue;
    visited[index] = 1;
    const offset = index * 4;
    if (!target.every((value, i) => pixels[offset + i] === value)) continue;
    pixels.set(replacement, offset);
    queue.push([x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]);
  }
  renderSkin();
  pushHistory();
}

function getPixelCoordinates(event) {
  const rect = skinCanvas.getBoundingClientRect();
  return {
    x: Math.floor(((event.clientX - rect.left) / rect.width) * SIZE),
    y: Math.floor(((event.clientY - rect.top) / rect.height) * SIZE),
  };
}

function applyTool(x, y) {
  if (activeTool === "picker") {
    const rgba = colorAt(x, y);
    if (rgba[3] === 0) {
      currentColor = "transparent";
      colorInput.value = "#000000";
    } else {
      currentColor = `#${rgba.slice(0, 3).map((n) => n.toString(16).padStart(2, "0")).join("")}`;
      colorInput.value = currentColor;
    }
    updateColorLabel();
    setTool("pencil");
    return;
  }
  const rgba = activeTool === "eraser" ? [0, 0, 0, 0] : cssColorToRgba(currentColor);
  setPixel(x, y, rgba);
}

function drawPreview() {
  const ctx = previewContext;
  const now = performance.now();
  const elapsed = (now - animationStart) / 1000 * (animationSpeed / 5);
  const moving = animation !== "idle";
  const cycle = elapsed * (animation === "run" ? 12 : 7);
  const swing = moving ? Math.sin(cycle) : Math.sin(elapsed * 1.5) * 0.06;
  const bounce = animation === "run" ? Math.abs(Math.sin(cycle)) * 7 : moving ? Math.abs(Math.sin(cycle)) * 3 : Math.sin(elapsed * 1.5) * 1.5;
  ctx.clearRect(0, 0, 300, 370);
  ctx.save();
  ctx.translate(150, 320 - bounce);
  ctx.fillStyle = "rgba(0,0,0,.28)";
  ctx.beginPath();
  ctx.ellipse(0, 4 + bounce, 55 - bounce, 9, 0, 0, Math.PI * 2);
  ctx.fill();
  const drawPart = (sx, sy, sw, sh, dx, dy, dw, dh, angle = 0, pivotX = dw / 2, pivotY = 0, overlay = null) => {
    ctx.save();
    ctx.translate(dx + pivotX, dy + pivotY);
    ctx.rotate(angle);
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(skinCanvas, sx * 8, sy * 8, sw * 8, sh * 8, -pivotX, -pivotY, dw, dh);
    if (overlay) ctx.drawImage(skinCanvas, overlay[0] * 8, overlay[1] * 8, overlay[2] * 8, overlay[3] * 8, -pivotX, -pivotY, dw, dh);
    ctx.restore();
  };
  const legSwing = animation === "idle" ? 0 : swing * (animation === "run" ? .68 : .48);
  const armSwing = animation === "idle" ? Math.sin(elapsed * 1.5) * .035 : -swing * (animation === "run" ? .64 : .46);
  drawPart(4, 20, 4, 12, -27, -83, 27, 83, legSwing, 13, 0, [4, 36, 4, 12]);
  drawPart(20, 52, 4, 12, 0, -83, 27, 83, -legSwing, 13, 0, [4, 52, 4, 12]);
  drawPart(20, 20, 8, 12, -27, -186, 54, 103, 0, 27, 0, [20, 36, 8, 12]);
  drawPart(44, 20, 4, 12, -55, -183, 28, 98, armSwing, 14, 0, [44, 36, 4, 12]);
  drawPart(36, 52, 4, 12, 27, -183, 28, 98, -armSwing, 14, 0, [52, 52, 4, 12]);
  drawPart(8, 8, 8, 8, -37, -264, 74, 77, swing * .035, 37, 68, [40, 8, 8, 8]);
  ctx.restore();
  requestAnimationFrame(drawPreview);
}

function pushHistory() {
  history = history.slice(0, historyIndex + 1);
  history.push(pixels.slice());
  if (history.length > 40) history.shift();
  historyIndex = history.length - 1;
  updateHistoryButtons();
  scheduleSave();
}

function restoreHistory(index) {
  if (index < 0 || index >= history.length) return;
  historyIndex = index;
  pixels.set(history[index]);
  renderSkin();
  updateHistoryButtons();
  scheduleSave();
}

function updateHistoryButtons() {
  document.querySelector("#undoButton").disabled = historyIndex <= 0;
  document.querySelector("#redoButton").disabled = historyIndex >= history.length - 1;
}

function setTool(tool) {
  activeTool = tool;
  document.querySelectorAll(".tool-button").forEach((button) => button.classList.toggle("active", button.dataset.tool === tool));
  skinCanvas.style.cursor = tool === "picker" ? "copy" : tool === "eraser" ? "cell" : "crosshair";
}

function updateColorLabel() {
  colorHex.textContent = currentColor === "transparent" ? "VIDE" : currentColor.toUpperCase();
}

function setZoom(nextZoom) {
  zoom = Math.max(4, Math.min(14, nextZoom));
  canvasWrap.style.width = `${SIZE * zoom}px`;
  canvasWrap.style.height = `${SIZE * zoom}px`;
  zoomLabel.textContent = `${zoom * 100}%`;
}

function scheduleSave() {
  saveStatus.textContent = "Modifications…";
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        pixels: Array.from(pixels),
      }));
      saveStatus.textContent = "Enregistré localement";
    } catch (error) {
      console.error("Impossible d’enregistrer le skin localement.", error);
      saveStatus.textContent = "Enregistrement indisponible";
    }
  }, 300);
}

function paintRect(x, y, width, height, color) {
  const rgba = cssColorToRgba(color);
  for (let py = y; py < y + height; py++) {
    for (let px = x; px < x + width; px++) {
      pixels.set(rgba, (py * SIZE + px) * 4);
    }
  }
}

function createStarterSkin() {
  const skin = "#d9a47d";
  const hair = "#49372d";
  const shirt = "#4f86c6";
  const shirtLight = "#72a7e6";
  const pants = "#344c72";
  const boots = "#49372d";
  paintRect(8, 8, 8, 8, skin);
  paintRect(9, 11, 1, 1, "#392c27");
  paintRect(14, 11, 1, 1, "#392c27");
  paintRect(11, 13, 2, 1, "#bf7e61");
  paintRect(40, 8, 8, 2, hair);
  paintRect(40, 10, 1, 3, hair);
  paintRect(47, 10, 1, 3, hair);
  paintRect(20, 20, 8, 12, shirt);
  paintRect(20, 20, 8, 2, shirtLight);
  paintRect(23, 20, 2, 12, "#4075b3");
  paintRect(44, 20, 4, 12, skin);
  paintRect(44, 20, 4, 4, shirt);
  paintRect(36, 52, 4, 12, skin);
  paintRect(36, 52, 4, 4, shirt);
  paintRect(4, 20, 4, 12, pants);
  paintRect(4, 30, 4, 2, boots);
  paintRect(20, 52, 4, 12, pants);
  paintRect(20, 62, 4, 2, boots);
}

function saveAsPng() {
  const output = document.createElement("canvas");
  output.width = SIZE;
  output.height = SIZE;
  const ctx = output.getContext("2d");
  const image = ctx.createImageData(SIZE, SIZE);
  image.data.set(pixels);
  ctx.putImageData(image, 0, 0);
  output.toBlob((blob) => {
    if (!blob) {
      console.error("La création du fichier PNG a échoué.");
      saveStatus.textContent = "Échec de l’export";
      return;
    }
    const link = document.createElement("a");
    const objectUrl = URL.createObjectURL(blob);
    link.href = objectUrl;
    link.download = "mon-skin-minecraft.png";
    link.click();
    setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
  }, "image/png");
}

function importPng(file) {
  const image = new Image();
  image.onload = () => {
    if (image.width !== 64 || image.height !== 64) {
      alert("Le fichier doit être une texture Minecraft de 64 × 64 pixels.");
      URL.revokeObjectURL(image.src);
      return;
    }
    const source = document.createElement("canvas");
    source.width = SIZE;
    source.height = SIZE;
    const ctx = source.getContext("2d", { willReadFrequently: true });
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(image, 0, 0);
    pixels.set(ctx.getImageData(0, 0, SIZE, SIZE).data);
    renderSkin();
    pushHistory();
    URL.revokeObjectURL(image.src);
  };
  image.onerror = () => {
    console.error("Le fichier image n’a pas pu être lu.");
    alert("Impossible de lire cette image. Choisis un fichier PNG valide.");
    URL.revokeObjectURL(image.src);
  };
  image.src = URL.createObjectURL(file);
}

document.querySelectorAll(".tool-button").forEach((button) => button.addEventListener("click", () => setTool(button.dataset.tool)));
document.querySelectorAll(".swatch").forEach((button) => button.addEventListener("click", () => {
  currentColor = button.dataset.color;
  if (currentColor !== "transparent") colorInput.value = currentColor;
  updateColorLabel();
  document.querySelectorAll(".swatch").forEach((swatch) => swatch.classList.toggle("selected", swatch === button));
}));
colorInput.addEventListener("input", () => {
  currentColor = colorInput.value;
  document.querySelectorAll(".swatch").forEach((swatch) => swatch.classList.remove("selected"));
  updateColorLabel();
});
document.querySelector("#resetColor").addEventListener("click", () => {
  currentColor = "#68d391";
  colorInput.value = currentColor;
  updateColorLabel();
});
skinCanvas.addEventListener("pointerdown", (event) => {
  event.preventDefault();
  const { x, y } = getPixelCoordinates(event);
  if (activeTool === "fill") {
    fillArea(x, y, cssColorToRgba(currentColor));
    return;
  }
  drawing = true;
  skinCanvas.setPointerCapture(event.pointerId);
  applyTool(x, y);
});
skinCanvas.addEventListener("pointermove", (event) => {
  const { x, y } = getPixelCoordinates(event);
  if (x >= 0 && x < SIZE && y >= 0 && y < SIZE) {
    cursorPosition.textContent = `X : ${x}   Y : ${y}`;
    if (drawing) applyTool(x, y);
  } else cursorPosition.textContent = "Survole la grille pour voir les coordonnées";
});
skinCanvas.addEventListener("pointerup", () => {
  if (!drawing) return;
  drawing = false;
  pushHistory();
});
skinCanvas.addEventListener("pointercancel", () => { drawing = false; });
document.querySelector("#zoomIn").addEventListener("click", () => setZoom(zoom + 1));
document.querySelector("#zoomOut").addEventListener("click", () => setZoom(zoom - 1));
document.querySelector("#gridToggle").addEventListener("click", (event) => {
  gridVisible = !gridVisible;
  event.currentTarget.classList.toggle("active", gridVisible);
  drawGrid();
});
document.querySelector("#undoButton").addEventListener("click", () => restoreHistory(historyIndex - 1));
document.querySelector("#redoButton").addEventListener("click", () => restoreHistory(historyIndex + 1));
document.querySelector("#exportButton").addEventListener("click", saveAsPng);
document.querySelector("#importButton").addEventListener("click", () => document.querySelector("#importInput").click());
document.querySelector("#importInput").addEventListener("change", (event) => {
  if (event.target.files[0]) importPng(event.target.files[0]);
  event.target.value = "";
});
document.querySelectorAll(".animation-tab").forEach((button) => button.addEventListener("click", () => {
  animation = button.dataset.animation;
  animationStart = performance.now();
  document.querySelectorAll(".animation-tab").forEach((tab) => {
    const active = tab === button;
    tab.classList.toggle("active", active);
    tab.setAttribute("aria-selected", String(active));
  });
}));
document.querySelector("#speedInput").addEventListener("input", (event) => {
  animationSpeed = Number(event.target.value);
  document.querySelector("#speedValue").textContent = event.target.value;
});
document.querySelector("#resetPreview").addEventListener("click", () => { animationStart = performance.now(); });
document.addEventListener("keydown", (event) => {
  if (event.target.matches("input")) return;
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "z") {
    event.preventDefault();
    restoreHistory(historyIndex + (event.shiftKey ? 1 : -1));
    return;
  }
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "y") {
    event.preventDefault();
    restoreHistory(historyIndex + 1);
    return;
  }
  const shortcuts = { b: "pencil", e: "eraser", g: "fill", i: "picker" };
  if (shortcuts[event.key.toLowerCase()]) setTool(shortcuts[event.key.toLowerCase()]);
});

try {
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
  if (saved?.pixels?.length === SIZE * SIZE * 4) {
    pixels.set(saved.pixels);
  } else {
    createStarterSkin();
  }
} catch (error) {
  console.error("Les données locales du skin n’ont pas pu être chargées.", error);
  createStarterSkin();
}
setZoom(zoom);
renderSkin();
pushHistory();
drawPreview();
