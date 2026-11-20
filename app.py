"""WINDOWS 12 ULTIMATE - fictional desktop simulator, standard library only."""

from __future__ import annotations

import ast
import hashlib
import hmac
import json
import math
import operator
import random
import re
import secrets
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


APP_NAME = "WINDOWS 12 ULTIMATE"
ROBLOX_IMAGE_PATH = Path(
    r"C:\Users\Labtop\AppData\Roaming\Code\agentSessionData"
    r"\fead3ee1-a8cb-42ca-9a38-af20ebc716b6\attachments"
    r"\e0678ec2-335e-43b1-ad6e-4ed40730534b\Sans titre-1.jpg"
)
STATE_PATH = Path.home() / "AppData" / "Local" / "WINDOWS12ULTIMATE" / "state.json"
DEFAULT_STATE = {
    "profile": {"username": "Guest", "avatar": "W", "photo": "", "hacker_skin": False},
    "roblox": {
        "creator_name": "admine wind12",
        "published_games": [],
        "play_store_games": [],
        "published_skins": [],
        "updates": [],
        "active_skin": None,
        "skin_draft": {},
        "installed_games": [],
        "installed_apps": [],
    },
    "settings": {
        "theme": "dark",
        "wallpaper": "Aurora",
        "resolution": "1280x800",
        "fullscreen": False,
        "volume": 45,
        "language": "Français",
    },
}
SIMULATED_PLAYERS = [
    ("admine wind12", "En ligne", "Roblox Obby"),
    ("PixelNova", "En ligne", "OBBY IMPOSSIBLE"),
    ("LunaBuilds", "En ligne", "Studio"),
    ("Max_Runner", "En ligne", "Roblox Obby"),
    ("CloudyFox", "En ligne", "Night Shift"),
    ("BlueComet", "Absent", "—"),
    ("CraftyMilo", "En ligne", "Studio"),
    ("StarGamer42", "Absent", "—"),
    ("NinjaPanda", "En ligne", "Matrix Runner"),
    ("EchoBuilder", "En ligne", "Roblox Obby"),
    ("MapleCat", "Absent", "—"),
    ("TurboPixel", "En ligne", "OBBY IMPOSSIBLE"),
]
SKIN_COLORS = {
    "Peau dorée": "#f0c58c",
    "Peau claire": "#f4d2b1",
    "Peau brune": "#a96e48",
    "Peau foncée": "#69432f",
    "Rouge": "#eb4b5c",
    "Bleu": "#2789ec",
    "Vert": "#32a675",
    "Violet": "#8757d6",
    "Noir": "#252b38",
    "Blanc": "#f4f6fb",
    "Jaune": "#f2c94c",
    "Rose": "#ee7eb5",
}

BASE_EFFECTS = [
    ("shake", "Tremblement d’écran", "shake"),
    ("glitch", "Glitch RGB", "rgb"),
    ("pixels", "Pixels disparus", "pixels"),
    ("red", "Écran rouge", "color"),
    ("bsod", "Faux écran bleu", "signal"),
    ("distortion", "Distorsion", "geometry"),
    ("matrix", "Animation Matrix", "terminal"),
    ("jumpscare", "Jumpscare surprise", "ghost"),
]

GLITCH_ADDITIONS = [
    ("rgb_split", "Décalage RGB", "rgb"),
    ("chromatic_aberration", "Aberration chromatique", "rgb"),
    ("cyan_shadow", "Ombre cyan", "rgb"),
    ("red_shadow", "Ombre rouge", "rgb"),
    ("neon_edges", "Contours néon", "rgb"),
    ("prism_echo", "Écho prismatique", "rgb"),
    ("horizontal_tearing", "Déchirure horizontale", "signal"),
    ("vertical_tearing", "Déchirure verticale", "signal"),
    ("rolling_bands", "Bandes déroulantes", "signal"),
    ("analog_dropout", "Perte analogique", "signal"),
    ("tracking_error", "Erreur de tracking", "signal"),
    ("tv_static", "Neige télévisuelle", "signal"),
    ("pixel_rain", "Pluie de pixels", "pixels"),
    ("pixel_burst", "Explosion de pixels", "pixels"),
    ("dead_pixel_map", "Carte de pixels morts", "pixels"),
    ("pixel_mosaic", "Mosaïque corrompue", "pixels"),
    ("block_corruption", "Blocs corrompus", "pixels"),
    ("tile_shuffle", "Tuiles mélangées", "pixels"),
    ("wave_warp", "Vagues déformantes", "geometry"),
    ("ripple_field", "Champ d’ondulations", "geometry"),
    ("tunnel_warp", "Tunnel numérique", "geometry"),
    ("wobble_grid", "Grille vacillante", "geometry"),
    ("mirror_split", "Miroir fracturé", "geometry"),
    ("perspective_fold", "Pli de perspective", "geometry"),
    ("code_rain", "Pluie de code", "terminal"),
    ("glyph_scramble", "Glyphes brouillés", "terminal"),
    ("cursor_storm", "Tempête de curseurs", "terminal"),
    ("hex_cascade", "Cascade hexadécimale", "terminal"),
    ("corrupted_text", "Texte corrompu", "terminal"),
    ("symbol_rain", "Pluie de symboles", "terminal"),
    ("red_alert", "Alerte écarlate", "color"),
    ("blue_shift", "Décalage bleu", "color"),
    ("green_phosphor", "Phosphore vert", "color"),
    ("purple_haze", "Brume violette", "color"),
    ("amber_warning", "Avertissement ambre", "color"),
    ("negative_tint", "Teinte négative", "color"),
    ("ghost_frames", "Images fantômes", "ghost"),
    ("double_vision", "Vision double", "ghost"),
    ("shadow_trails", "Traînées d’ombre", "ghost"),
    ("outline_echo", "Écho de contours", "ghost"),
    ("fractured_screen", "Écran fracturé", "ghost"),
    ("afterimage", "Rémanence numérique", "ghost"),
    ("horizontal_bars", "Barres horizontales", "bars"),
    ("vertical_blinds", "Stores verticaux", "bars"),
    ("broken_bars", "Barres cassées", "bars"),
    ("data_stripes", "Rayures de données", "bars"),
    ("signal_ladder", "Échelle de signal", "bars"),
    ("moving_slits", "Fentes mouvantes", "bars"),
    ("white_noise", "Bruit blanc", "interference"),
    ("static_specks", "Grésillement", "interference"),
    ("scanline_drift", "Lignes de balayage", "interference"),
    ("analog_fuzz", "Parasites analogiques", "interference"),
    ("frequency_bleed", "Bavure de fréquence", "interference"),
    ("signal_loss", "Perte de signal", "interference"),
    ("radial_burst", "Rayonnement radial", "special"),
    ("glitch_sweep", "Balayage glitch", "special"),
    ("data_vortex", "Vortex de données", "special"),
    ("split_screen", "Écran divisé", "special"),
    ("digital_shards", "Éclats numériques", "special"),
    ("portal_noise", "Portail parasité", "special"),
]
EFFECTS = BASE_EFFECTS + GLITCH_ADDITIONS
EFFECT_DETAILS = {effect_id: (label, family) for effect_id, label, family in EFFECTS}
EFFECT_INDEX = {effect_id: index for index, (effect_id, _, _) in enumerate(EFFECTS)}

PALETTES = {
    "dark": {"bg": "#101827", "panel": "#18263a", "raised": "#223650", "fg": "#edf4ff", "muted": "#9db0ca", "accent": "#55c8ff"},
    "light": {"bg": "#edf3fb", "panel": "#ffffff", "raised": "#dfe8f4", "fg": "#17243a", "muted": "#5e708a", "accent": "#087fcb"},
}
WALLPAPERS = {
    "Aurora": ("#091426", "#173e71", "#34245f"),
    "Nebula": ("#180e2f", "#663170", "#18244c"),
    "Ocean": ("#061e28", "#087082", "#164378"),
    "Graphite": ("#11141d", "#303847", "#171b2a"),
}
SECRET_COMMANDS = {
    "profile : admine": "profile",
    "glitch : 999": "glitch",
    "matrix : secret": "matrix",
    "hacker : ultimate": "hacker",
    "system : unlock": "system",
    "ghost : 666": "ghost",
    "windows : 12": "windows",
}


def load_state() -> dict:
    state = json.loads(json.dumps(DEFAULT_STATE))
    if not STATE_PATH.exists():
        return state
    with STATE_PATH.open("r", encoding="utf-8") as file:
        saved = json.load(file)
    if not isinstance(saved, dict):
        raise ValueError("Le fichier de configuration doit être un objet JSON.")
    for section in ("profile", "settings", "roblox"):
        if isinstance(saved.get(section), dict):
            state[section].update(saved[section])
    if not isinstance(state["roblox"].get("published_games"), list):
        state["roblox"]["published_games"] = []
    for key in ("installed_games", "installed_apps", "published_skins", "updates", "play_store_games"):
        if not isinstance(state["roblox"].get(key), list):
            state["roblox"][key] = []
    return state


def safe_calculate(source: str) -> float:
    operators = {
        ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod, ast.Pow: operator.pow,
        ast.UAdd: operator.pos, ast.USub: operator.neg,
    }

    def visit(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow):
                if abs(right) > 10:
                    raise ValueError("Exposant trop grand.")
                return left**right
            return operators[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
            return operators[type(node.op)](visit(node.operand))
        raise ValueError("Expression non autorisée.")

    if len(source) > 100:
        raise ValueError("Expression trop longue.")
    return visit(ast.parse(source, mode="eval"))


class DesktopApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_NAME)
        self.root.minsize(900, 600)
        try:
            self.state = load_state()
        except (OSError, ValueError, json.JSONDecodeError) as error:
            self.state = json.loads(json.dumps(DEFAULT_STATE))
            root.after(300, lambda: messagebox.showwarning(APP_NAME, f"Configuration illisible : {error}", parent=root))
        self.profile = self.state["profile"]
        self.roblox = self.state["roblox"]
        self.settings = self.state["settings"]
        self.colors = PALETTES.get(self.settings.get("theme"), PALETTES["dark"])
        self.windows: dict[str, tk.Toplevel] = {}
        self.effect_overlay: tk.Frame | None = None
        self.effect_job: str | None = None
        self.effect_active: str | None = None
        self.hacker_mode = bool(self.profile.get("hacker_skin"))
        self.roblox_logo = self._load_roblox_logo()

        width, height = self._resolution(self.settings.get("resolution", "1280x800"))
        root.geometry(f"{width}x{height}+0+0")
        root.configure(bg=self.colors["bg"])
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.desktop = tk.Canvas(root, bg="#091426", highlightthickness=0)
        self.desktop.pack(fill="both", expand=True)
        self._draw_wallpaper()
        self._draw_icons()
        self.desktop.bind("<Configure>", lambda event: self._draw_wallpaper())
        self.taskbar = tk.Frame(root, bg="#101827", height=56)
        self.taskbar.pack(side="bottom", fill="x")
        self.taskbar.pack_propagate(False)
        self._build_taskbar()
        self.clock_tick()
        self._animate_wallpaper()
        if self.settings.get("fullscreen"):
            self.root.after(150, lambda: self.root.attributes("-fullscreen", True))

    def _resolution(self, value: str) -> tuple[int, int]:
        match = re.fullmatch(r"(\d{3,4})x(\d{3,4})", str(value))
        if not match:
            return 1280, 800
        return max(900, int(match.group(1))), max(600, int(match.group(2)))

    def save_state(self) -> None:
        self.state.update(profile=self.profile, settings=self.settings)
        try:
            STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            temporary = STATE_PATH.with_suffix(".tmp")
            temporary.write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8")
            temporary.replace(STATE_PATH)
        except OSError as error:
            messagebox.showerror(APP_NAME, f"Sauvegarde impossible :\n{error}", parent=self.root)

    def _draw_wallpaper(self) -> None:
        if not hasattr(self, "desktop") or not self.desktop.winfo_exists():
            return
        self.desktop.delete("wallpaper")
        width = max(self.desktop.winfo_width(), 900)
        height = max(self.desktop.winfo_height(), 500)
        colors = WALLPAPERS.get(self.settings.get("wallpaper"), WALLPAPERS["Aurora"])
        rgb = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in colors]
        steps = 42
        for n in range(steps):
            ratio = n / (steps - 1)
            first, second, amount = (0, 1, ratio / 0.6) if ratio < 0.6 else (1, 2, (ratio - 0.6) / 0.4)
            color = "#" + "".join(f"{round(a + (b-a)*amount):02x}" for a, b in zip(rgb[first], rgb[second]))
            y0, y1 = height * n / steps, height * (n + 1) / steps + 1
            self.desktop.create_rectangle(0, y0, width, y1, fill=color, outline=color, tags="wallpaper")
        self.desktop.create_oval(width * .53, -height * .5, width * 1.15, height * .7, fill="#ffffff", stipple="gray75", outline="", tags="wallpaper")
        self.desktop.tag_lower("wallpaper")
        self.desktop.tag_raise("banner")

    def _animate_wallpaper(self) -> None:
        if not self.root.winfo_exists():
            return
        width, height = max(self.desktop.winfo_width(), 900), max(self.desktop.winfo_height(), 500)
        phase = time.monotonic() * .24
        self.desktop.delete("glow")
        x = width * (.55 + .025 * math.sin(phase))
        self.desktop.create_oval(x, height * .15, x + 110, height * .15 + 110, fill="#b3edff", stipple="gray75", outline="", tags="glow")
        self.desktop.tag_raise("glow")
        self.desktop.tag_raise("icon")
        self.desktop.tag_raise("banner")
        self.root.after(90, self._animate_wallpaper)

    def _draw_icons(self) -> None:
        icons = [
            ("▤", "Explorer", self.open_explorer),
            ("◉", "Browser", self.open_browser),
            ("▦", "Calculator", self.open_calculator),
            ("⚙", "Settings", self.open_settings),
            ("♟", "Profile", self.open_profile),
            ("◇", "Games", self.open_games),
            ("▷", "Terminal", self.open_terminal),
            ("♫", "Music", self.open_music),
            ("✦", "Glitches", self.open_effects),
        ]
        for index, (glyph, name, callback) in enumerate(icons):
            x, y = 55, 60 + index * 82
            self.desktop.create_text(x, y, text=f"{glyph}\n{name}", fill="#f3f7ff", font=("Segoe UI", 10), justify="center", tags=("icon", f"icon{index}"))
            self.desktop.tag_bind(f"icon{index}", "<Button-1>", lambda event, fn=callback: fn())
            self.desktop.tag_bind(f"icon{index}", "<Enter>", lambda event: self.desktop.configure(cursor="hand2"))
            self.desktop.tag_bind(f"icon{index}", "<Leave>", lambda event: self.desktop.configure(cursor=""))
        for tag, x, y, label, callback in (
            ("roblox_icon", 160, 60, "Roblox", self.open_roblox_home),
            ("studio_icon", 160, 150, "Roblox Studio", self.open_roblox_studio),
            ("skins_icon", 160, 240, "Roblox Skins", self.open_roblox_skins),
        ):
            if self.roblox_logo:
                self.desktop.create_image(x, y, image=self.roblox_logo, tags=(tag,))
            else:
                self.desktop.create_rectangle(x - 29, y - 29, x + 29, y + 29, fill="#10151c" if tag == "roblox_icon" else "#1687e8", outline="", tags=(tag,))
                self.desktop.create_polygon(x - 17, y - 18, x + 20, y - 9, x + 12, y + 19, x - 21, y + 10, fill="#e6edf5", outline="", tags=(tag,))
                self.desktop.create_polygon(x - 2, y - 7, x + 12, y - 3, x + 9, y + 11, x - 6, y + 7, fill="#10151c", outline="", tags=(tag,))
            self.desktop.create_text(x, y + 43, text=label, fill="#f3f7ff", font=("Segoe UI", 9), tags=(tag,))
            self.desktop.tag_bind(tag, "<Button-1>", lambda event, fn=callback: fn())
            self.desktop.tag_bind(tag, "<Enter>", lambda event: self.desktop.configure(cursor="hand2"))
            self.desktop.tag_bind(tag, "<Leave>", lambda event: self.desktop.configure(cursor=""))
        for tag, y, label, callback, color in (
            ("play_store_icon", 60, "Play Store", self.open_store, "#27a96b"),
            ("play_store_studio_icon", 150, "Play Store Studio", self.open_play_store_studio, "#1687e8"),
        ):
            self.desktop.create_rectangle(241, y - 25, 291, y + 25, fill=color, outline="", tags=(tag,))
            self.desktop.create_text(266, y, text="▶" if tag == "play_store_icon" else "✎", fill="#ffffff", font=("Segoe UI", 20, "bold"), tags=(tag,))
            self.desktop.create_text(266, y + 42, text=label, fill="#f3f7ff", font=("Segoe UI", 9), tags=(tag,))
            self.desktop.tag_bind(tag, "<Button-1>", lambda event, fn=callback: fn())
            self.desktop.tag_bind(tag, "<Enter>", lambda event: self.desktop.configure(cursor="hand2"))
            self.desktop.tag_bind(tag, "<Leave>", lambda event: self.desktop.configure(cursor=""))
        self.desktop.create_text(self.root.winfo_screenwidth() // 2, 38, text="H A C K E R" if self.profile.get("username", "").lower() == "hacker" or self.hacker_mode else "", fill="#71ff9f", font=("Consolas", 19, "bold"), tags="banner")

    def _load_roblox_logo(self) -> tk.PhotoImage | None:
        image_path = Path(__file__).with_name("roblox_logo.jpg")
        if not image_path.is_file():
            image_path = ROBLOX_IMAGE_PATH
        if not image_path.is_file():
            return None
        try:
            image = tk.PhotoImage(file=str(image_path))
            scale = max(1, max(image.width(), image.height()) // 52)
            return image.subsample(scale, scale)
        except tk.TclError:
            try:
                from PIL import Image, ImageTk
            except ImportError:
                return None
            try:
                image = Image.open(image_path).convert("RGB")
                image.thumbnail((52, 52))
                return ImageTk.PhotoImage(image)
            except OSError:
                return None

    def _build_taskbar(self) -> None:
        self.start_button = tk.Button(self.taskbar, text="◈  Démarrer", command=self.toggle_start, bg="#1c2a40", fg="#ffffff", bd=0, padx=14, font=("Segoe UI", 10, "bold"))
        self.start_button.pack(side="left", padx=10, pady=8)
        self.task_windows = tk.Frame(self.taskbar, bg="#101827")
        self.task_windows.pack(side="left", fill="both", expand=True)
        self.clock = tk.Label(self.taskbar, text="", bg="#101827", fg="#ffffff", justify="right", font=("Segoe UI", 9))
        self.clock.pack(side="right", padx=16)
        self.user_badge = tk.Label(self.taskbar, text=f"{self.profile.get('avatar','W')}  {self.profile.get('username','Guest')}", bg="#101827", fg="#dce8f8", font=("Segoe UI", 9))
        self.user_badge.pack(side="right", padx=12)

    def clock_tick(self) -> None:
        if self.root.winfo_exists():
            self.clock.configure(text=time.strftime("%H:%M\n%d/%m/%Y"))
            self.root.after(1000, self.clock_tick)

    def _window(self, key: str, title: str, size: str = "680x480") -> tuple[tk.Toplevel, tk.Frame]:
        window = self.windows.get(key)
        if window and window.winfo_exists():
            window.deiconify()
            window.lift()
            return window, window.body
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(size)
        window.minsize(400, 280)
        window.configure(bg=self.colors["bg"])
        body = tk.Frame(window, bg=self.colors["bg"], padx=16, pady=14)
        body.pack(fill="both", expand=True)
        window.body = body
        self.windows[key] = window
        task = tk.Button(self.task_windows, text=title[:16], command=lambda w=window: (w.deiconify(), w.lift()), bg="#1a2a40", fg="#ffffff", bd=0, padx=8)
        task.pack(side="left", padx=3, pady=8)
        window.protocol("WM_DELETE_WINDOW", lambda w=window, t=task, k=key: self._close_window(w, t, k))
        return window, body

    def _close_window(self, window: tk.Toplevel, task: tk.Button, key: str) -> None:
        self.windows.pop(key, None)
        if task.winfo_exists():
            task.destroy()
        if window.winfo_exists():
            window.destroy()

    def _label(self, parent: tk.Widget, text: str, **kwargs) -> tk.Label:
        return tk.Label(parent, text=text, bg=kwargs.pop("bg", self.colors["bg"]), fg=kwargs.pop("fg", self.colors["fg"]), font=kwargs.pop("font", ("Segoe UI", 10)), **kwargs)

    def _button(self, parent: tk.Widget, text: str, command, **kwargs) -> tk.Button:
        return tk.Button(parent, text=text, command=command, bg=kwargs.pop("bg", self.colors["raised"]), fg=kwargs.pop("fg", self.colors["fg"]), activebackground=self.colors["accent"], activeforeground="#ffffff", bd=0, padx=kwargs.pop("padx", 10), pady=kwargs.pop("pady", 7), font=kwargs.pop("font", ("Segoe UI", 10)), cursor="hand2", **kwargs)

    def _entry(self, parent: tk.Widget, **kwargs) -> tk.Entry:
        return tk.Entry(parent, bg=self.colors["raised"], fg=self.colors["fg"], insertbackground=self.colors["fg"], relief="flat", font=kwargs.pop("font", ("Segoe UI", 11)), **kwargs)

    def toggle_start(self) -> None:
        if getattr(self, "start_menu", None) and self.start_menu.winfo_exists():
            self.start_menu.destroy()
            return
        menu = tk.Toplevel(self.root)
        menu.overrideredirect(True)
        menu.geometry(f"390x580+10+{max(20,self.root.winfo_height()-640)}")
        menu.configure(bg=self.colors["panel"])
        self.start_menu = menu
        self._label(menu, "WINDOWS 12 ULTIMATE", bg=self.colors["panel"], font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=16, pady=(16, 5))
        search = self._entry(menu)
        search.insert(0, "Application ou commande secrète…")
        search.pack(fill="x", padx=14, pady=10, ipady=7)
        search.bind("<FocusIn>", lambda event: search.delete(0, "end") if search.get().startswith("Application") else None)
        search.bind("<Return>", lambda event: self._launch_search(search.get()))
        apps = [
            ("Explorateur", self.open_explorer), ("Navigateur", self.open_browser),
            ("Calculatrice", self.open_calculator), ("Paramètres", self.open_settings),
            ("Profil", self.open_profile), ("Jeux", self.open_games),
            ("Roblox", self.open_roblox_home), ("Roblox Studio", self.open_roblox_studio),
            ("Roblox Skins", self.open_roblox_skins),
            ("Admin Roblox", self.open_roblox_admin),
            ("Play Store", self.open_store),
            ("Play Store Studio", self.open_play_store_studio),
            ("Terminal", self.open_terminal),
            ("Musique", self.open_music), ("Effets visuels", self.open_effects),
            ("Jeu d'horreur", self.open_horror),
        ]
        grid = tk.Frame(menu, bg=self.colors["panel"])
        grid.pack(fill="both", expand=True, padx=10)
        for i, (name, action) in enumerate(apps):
            self._button(grid, name, action).grid(row=i // 2, column=i % 2, sticky="ew", padx=4, pady=4)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        self._button(menu, "Quitter", self.close, bg="#472532").pack(fill="x", padx=14, pady=12)

    def _launch_search(self, text: str) -> None:
        if self.start_menu and self.start_menu.winfo_exists():
            self.start_menu.destroy()
        if self.handle_secret(text):
            return
        query = text.strip().lower()
        if query in {"roblox", "jeux roblox"}:
            self.open_roblox_home()
        elif query in {"roblox studio", "studio"}:
            self.open_roblox_studio()
        elif query in {"roblox skins", "skins roblox", "skin"}:
            self.open_roblox_skins()
        elif query in {"mises à jour roblox", "roblox updates", "updates"}:
            self.open_roblox_updates()
        elif query in {"play store", "playstore", "store", "app store"}:
            self.open_store()
        elif query in {"play store studio", "playstore studio"}:
            self.open_play_store_studio()
        elif query in {"admin roblox", "administrateur", "admin"}:
            self.open_roblox_admin()
        elif query in {"roblox obby", "obby", "mode impossible"}:
            self.open_roblox_game("Impossible" if query == "mode impossible" else "Normal")
        elif text.strip():
            self.open_browser()
            self._notice(f"Recherche locale simulée : {text}")

    def open_explorer(self) -> None:
        _, body = self._window("explorer", "File Explorer")
        for child in body.winfo_children():
            child.destroy()
        self._label(body, "Accueil  ›  Ce PC", font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(0, 10))
        folders = ["Bureau", "Documents", "Images", "Musique", "Téléchargements", "Disque virtuel"]
        listing = tk.Listbox(body, bg=self.colors["panel"], fg=self.colors["fg"], selectbackground=self.colors["accent"], relief="flat", font=("Segoe UI", 11))
        for name in folders:
            listing.insert("end", f"  ▣   {name}")
        listing.pack(fill="both", expand=True)
        self._label(body, "Explorateur fictif : aucun fichier Windows n’est lu ou modifié.", fg=self.colors["muted"]).pack(anchor="w", pady=8)

    def open_browser(self) -> None:
        _, body = self._window("browser", "Nova Browser", "760x520")
        for child in body.winfo_children():
            child.destroy()
        bar = tk.Frame(body, bg=self.colors["bg"])
        bar.pack(fill="x", pady=(0, 10))
        address = self._entry(bar)
        address.insert(0, "https://")
        address.pack(side="left", fill="x", expand=True, ipady=7)
        page = tk.Frame(body, bg=self.colors["panel"], padx=26, pady=22)
        page.pack(fill="both", expand=True)

        def search(event=None) -> None:
            query = address.get().replace("https://", "").replace("http://", "").strip()
            for child in page.winfo_children():
                child.destroy()
            self._label(page, "NOVA", bg=self.colors["panel"], fg=self.colors["accent"], font=("Segoe UI", 28, "bold")).pack(anchor="w", pady=20)
            self._label(page, f"Résultats simulés pour : {query}\n\nCe navigateur de démonstration reste hors ligne.", bg=self.colors["panel"], justify="left").pack(anchor="w")
        address.bind("<Return>", search)
        self._button(bar, "Rechercher", search).pack(side="left", padx=8)
        search()

    def open_calculator(self) -> None:
        _, body = self._window("calculator", "Calculator", "370x460")
        for child in body.winfo_children():
            child.destroy()
        display = self._entry(body, justify="right", font=("Segoe UI", 24))
        display.pack(fill="x", pady=10, ipady=8)
        grid = tk.Frame(body, bg=self.colors["bg"])
        grid.pack(fill="both", expand=True)
        values = ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "C", "0", ".", "+", "(", ")", "%", "="]

        def press(value: str) -> None:
            if value == "C":
                display.delete(0, "end")
            elif value == "=":
                try:
                    result = safe_calculate(display.get())
                    display.delete(0, "end")
                    display.insert(0, str(result))
                except (ValueError, SyntaxError, ZeroDivisionError, OverflowError) as error:
                    messagebox.showerror("Calculatrice", f"Calcul impossible : {error}", parent=body.winfo_toplevel())
            else:
                display.insert("end", value)

        for i, value in enumerate(values):
            self._button(grid, value, lambda v=value: press(v), font=("Segoe UI", 14, "bold")).grid(row=i // 4, column=i % 4, sticky="nsew", padx=3, pady=3)
            grid.columnconfigure(i % 4, weight=1)
            grid.rowconfigure(i // 4, weight=1)

    def open_profile(self) -> None:
        _, body = self._window("profile", "Profil", "500x400")
        for child in body.winfo_children():
            child.destroy()
        self._label(body, "PROFIL PERSONNEL", font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=8)
        self._label(body, "Nom d’utilisateur").pack(anchor="w", pady=(8, 3))
        username = self._entry(body)
        username.insert(0, self.profile.get("username", "Guest"))
        username.pack(fill="x", ipady=6)
        avatar = tk.StringVar(value=self.profile.get("avatar", "W"))
        self._label(body, "Avatar").pack(anchor="w", pady=(10, 3))
        ttk.Combobox(body, textvariable=avatar, values=["W", "A", "H", "★", "●", "◆"], state="readonly").pack(anchor="w")
        photo_label = self._label(body, Path(self.profile.get("photo", "")).name or "Aucune photo")
        photo_label.pack(anchor="w", pady=8)

        def select_photo() -> None:
            photo = filedialog.askopenfilename(title="Choisir une image", filetypes=[("PNG/GIF", "*.png *.gif"), ("Tous les fichiers", "*.*")], parent=body.winfo_toplevel())
            if photo:
                self.profile["photo"] = photo
                photo_label.configure(text=Path(photo).name)

        self._button(body, "Choisir une photo", select_photo).pack(anchor="w")
        hacker_skin = tk.BooleanVar(value=bool(self.profile.get("hacker_skin")))
        tk.Checkbutton(body, text="Skin Hacker", variable=hacker_skin, bg=self.colors["bg"], fg=self.colors["fg"], selectcolor=self.colors["raised"]).pack(anchor="w", pady=8)

        def save() -> None:
            name = username.get().strip()
            if not name or len(name) > 32:
                messagebox.showerror("Profil", "Le nom doit contenir de 1 à 32 caractères.", parent=body.winfo_toplevel())
                return
            self.profile.update(username=name, avatar=avatar.get(), hacker_skin=hacker_skin.get())
            self.hacker_mode = hacker_skin.get()
            self.user_badge.configure(text=f"{avatar.get()}  {name}", fg="#71ff9f" if name.lower() == "hacker" or self.hacker_mode else self.colors["fg"])
            self.desktop.itemconfigure("banner", text="H A C K E R" if name.lower() == "hacker" or self.hacker_mode else "")
            self.save_state()

        self._button(body, "Enregistrer le profil", save, bg=self.colors["accent"]).pack(anchor="e", pady=12)

    def open_settings(self) -> None:
        _, body = self._window("settings", "Paramètres", "590x520")
        for child in body.winfo_children():
            child.destroy()
        self._label(body, "PERSONNALISATION", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 10))

        def row(label: str, value: str, options: list[str], callback) -> None:
            frame = tk.Frame(body, bg=self.colors["bg"])
            frame.pack(fill="x", pady=6)
            self._label(frame, label, width=20, anchor="w").pack(side="left")
            selected = tk.StringVar(value=value)
            combo = ttk.Combobox(frame, textvariable=selected, values=options, state="readonly", width=22)
            combo.pack(side="left", fill="x", expand=True)
            combo.bind("<<ComboboxSelected>>", lambda event: callback(selected.get()))

        row("Thème", self.settings.get("theme", "dark"), ["dark", "light"], self._theme)
        row("Fond d’écran", self.settings.get("wallpaper", "Aurora"), list(WALLPAPERS), self._wallpaper)
        row("Résolution", self.settings.get("resolution", "1280x800"), ["1024x768", "1280x800", "1366x768", "1600x900", "1920x1080"], self._resolution_setting)
        row("Langue", self.settings.get("language", "Français"), ["Français", "English"], self._language)
        volume = tk.IntVar(value=int(self.settings.get("volume", 45)))
        self._label(body, "Volume simulé").pack(anchor="w", pady=(12, 0))
        tk.Scale(body, from_=0, to=100, orient="horizontal", variable=volume, command=lambda value: self.settings.update(volume=int(float(value))), bg=self.colors["bg"], fg=self.colors["fg"], troughcolor=self.colors["raised"], highlightthickness=0).pack(fill="x")
        fullscreen = tk.BooleanVar(value=bool(self.settings.get("fullscreen")))
        tk.Checkbutton(body, text="Plein écran", variable=fullscreen, command=lambda: self._fullscreen(fullscreen.get()), bg=self.colors["bg"], fg=self.colors["fg"], selectcolor=self.colors["raised"]).pack(anchor="w", pady=7)
        self._button(body, "Enregistrer les paramètres", self.save_state, bg=self.colors["accent"]).pack(anchor="e", pady=8)

    def _theme(self, value: str) -> None:
        self.settings["theme"] = value
        self.colors = PALETTES[value]
        self.root.configure(bg=self.colors["bg"])
        self.save_state()
        self._notice("Thème enregistré. Rouvrez les fenêtres pour appliquer partout.")

    def _wallpaper(self, value: str) -> None:
        self.settings["wallpaper"] = value
        self._draw_wallpaper()
        self.save_state()

    def _resolution_setting(self, value: str) -> None:
        self.settings["resolution"] = value
        if not self.settings.get("fullscreen"):
            width, height = self._resolution(value)
            self.root.geometry(f"{width}x{height}")
        self.save_state()

    def _language(self, value: str) -> None:
        self.settings["language"] = value
        self.start_button.configure(text="◈  Start" if value == "English" else "◈  Démarrer")
        self.save_state()

    def _fullscreen(self, value: bool) -> None:
        self.settings["fullscreen"] = value
        self.root.attributes("-fullscreen", value)
        self.save_state()

    def open_roblox_home(self) -> None:
        _, body = self._window("roblox_home", "Roblox • Accueil", "1120x720")
        for child in body.winfo_children():
            child.destroy()

        page_bg = "#f4f5f7"
        header = tk.Frame(body, bg="#ffffff", height=58)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="ROBLOX", bg="#ffffff", fg="#202127", font=("Segoe UI", 18, "bold")).pack(side="left", padx=16)
        tk.Label(header, text="WINDOWS 12", bg="#ffffff", fg="#6b7280", font=("Segoe UI", 9, "bold")).pack(side="left")
        search = tk.Entry(header, bg="#eff0f2", fg="#25262a", insertbackground="#25262a", relief="flat", font=("Segoe UI", 10))
        search.insert(0, "Rechercher des jeux")
        search.pack(side="left", padx=22, ipady=8, fill="x", expand=True)
        creator_button = tk.Button(
            header,
            text=f"👤  {self.roblox.get('creator_name', 'admine wind12')}",
            command=self.open_roblox_account,
            bg="#ffffff",
            fg="#202127",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        creator_button.pack(side="right", padx=(6, 14))
        tk.Button(
            header,
            text="♙  Admin",
            command=self.open_roblox_admin,
            bg="#f0f1f3",
            fg="#202127",
            relief="flat",
            padx=10,
            pady=6,
            cursor="hand2",
        ).pack(side="right", padx=5)
        tk.Button(
            header,
            text="＋ Studio",
            command=self.open_roblox_studio,
            bg="#202127",
            fg="#ffffff",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
        ).pack(side="right", padx=6)
        tk.Button(
            header,
            text="👕 Skins",
            command=self.open_roblox_skins,
            bg="#f0f1f3",
            fg="#202127",
            relief="flat",
            padx=10,
            pady=6,
            cursor="hand2",
        ).pack(side="right", padx=5)

        layout = tk.Frame(body, bg=page_bg)
        layout.pack(fill="both", expand=True)
        sidebar = tk.Frame(layout, bg="#ffffff", width=140)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        content = tk.Frame(layout, bg=page_bg, padx=16, pady=14)
        content.pack(side="left", fill="both", expand=True)
        for label, action in (
            ("⌂   Accueil", self.open_roblox_home),
            ("◇   Découvrir", self.open_roblox_home),
            ("▶   Mes jeux", self.open_games),
            ("♙   Mon profil", self.open_roblox_account),
            ("👕  Mes skins", self.open_roblox_skins),
            ("↻   Mises à jour", self.open_roblox_updates),
        ):
            tk.Button(
                sidebar,
                text=label,
                command=action,
                anchor="w",
                bg="#ffffff",
                fg="#26272c",
                activebackground="#e9edf3",
                activeforeground="#202127",
                relief="flat",
                font=("Segoe UI", 10, "bold"),
                padx=15,
                pady=13,
                cursor="hand2",
            ).pack(fill="x")

        tk.Label(content, text="Recommandé pour toi", bg=page_bg, fg="#202127", font=("Segoe UI", 19, "bold")).pack(anchor="w", pady=(0, 10))
        card_area = tk.Frame(content, bg=page_bg)
        card_area.pack(fill="both", expand=True)
        built_in_games = [
            {"name": "Roblox Obby", "creator": "Windows 12", "description": "Un parcours de plateformes et des pièces à récupérer.", "color": "#58afe8", "action": lambda: self.open_roblox_game("Normal")},
            {"name": "OBBY IMPOSSIBLE", "creator": "Windows 12", "description": "Mode extrêmement difficile : sauts précis et seulement 3 vies.", "color": "#a83551", "action": lambda: self.open_roblox_game("Impossible")},
            {"name": "Night Shift", "creator": "Windows 12", "description": "Explore la maison mystérieuse et cherche la sortie.", "color": "#45345d", "action": self.open_horror},
            {"name": "Matrix Runner", "creator": "Windows 12", "description": "Plonge dans une animation de code futuriste.", "color": "#117d53", "action": lambda: self.start_effect("matrix")},
        ]
        published = []
        for item in self.roblox.get("published_games", []):
            if isinstance(item, dict):
                published.append({
                    "name": item.get("name", "Jeu sans titre"),
                    "creator": item.get("creator", "Créateur"),
                    "description": f"Jeu créé localement • {len(item.get('objects', []))} objets",
                    "color": "#4563a8",
                    "action": lambda project=item: self._play_published_game(project),
                })
        all_games = built_in_games + published
        cards_frame = tk.Frame(card_area, bg=page_bg)
        cards_frame.pack(fill="both", expand=True)

        def display_games(filter_value: str = "") -> None:
            for child in cards_frame.winfo_children():
                child.destroy()
            filtered = [item for item in all_games if filter_value.lower() in item["name"].lower() or filter_value.lower() in item["creator"].lower()]
            if not filtered:
                tk.Label(cards_frame, text="Aucun jeu trouvé.", bg=page_bg, fg="#525866", font=("Segoe UI", 12)).pack(anchor="w", pady=16)
            for index, item in enumerate(filtered):
                row, column = divmod(index, 3)
                card = tk.Frame(cards_frame, bg="#ffffff", highlightbackground="#e2e4e9", highlightthickness=1, padx=8, pady=8)
                card.grid(row=row, column=column, sticky="nsew", padx=6, pady=6)
                thumb = tk.Canvas(card, height=112, bg=item["color"], highlightthickness=0)
                thumb.pack(fill="x")
                thumb.create_oval(thumb.winfo_reqwidth() - 112, 12, thumb.winfo_reqwidth() - 20, 104, fill="#ffffff", stipple="gray75", outline="")
                thumb.create_text(15, 16, anchor="nw", text="▶", fill="#ffffff", font=("Segoe UI", 31, "bold"))
                thumb.create_text(12, 86, anchor="sw", text=item["name"].upper()[:25], fill="#ffffff", font=("Segoe UI", 11, "bold"))
                tk.Label(card, text=item["name"], bg="#ffffff", fg="#23252a", anchor="w", font=("Segoe UI", 11, "bold")).pack(fill="x", pady=(8, 1))
                tk.Label(card, text=f"Par {item['creator']}", bg="#ffffff", fg="#646b76", anchor="w", font=("Segoe UI", 9)).pack(fill="x")
                tk.Label(card, text=item["description"], bg="#ffffff", fg="#4c515a", anchor="w", justify="left", wraplength=250, font=("Segoe UI", 9)).pack(fill="x", pady=(5, 6))
                tk.Button(card, text="▶  Jouer", command=item["action"], bg="#202127", fg="#ffffff", relief="flat", padx=12, pady=5, cursor="hand2").pack(anchor="w")
            for column in range(3):
                cards_frame.columnconfigure(column, weight=1)

        search.bind("<FocusIn>", lambda event: search.delete(0, "end") if search.get() == "Rechercher des jeux" else None)
        search.bind("<KeyRelease>", lambda event: display_games(search.get().strip()))
        display_games()

        bottom = tk.Frame(content, bg=page_bg)
        bottom.pack(fill="x", pady=(8, 0))
        tk.Button(bottom, text="Créer un jeu dans Roblox Studio", command=self.open_roblox_studio, bg="#1687e8", fg="#ffffff", relief="flat", padx=12, pady=7, cursor="hand2").pack(side="left")
        tk.Button(bottom, text="Créer un skin", command=self.open_roblox_skins, bg="#ffffff", fg="#202127", relief="flat", padx=12, pady=7, cursor="hand2").pack(side="left", padx=8)
        tk.Button(bottom, text=f"Mises à jour ({len(self.roblox.get('updates', []))})", command=self.open_roblox_updates, bg="#ffffff", fg="#202127", relief="flat", padx=12, pady=7, cursor="hand2").pack(side="left", padx=4)

    def open_roblox_account(self) -> None:
        _, body = self._window("roblox_account", "Profil Roblox • local", "520x460")
        for child in body.winfo_children():
            child.destroy()
        self._label(body, "MON PROFIL ROBLOX", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(2, 8))
        self._label(body, "Profil local du simulateur — ne demande aucun mot de passe Roblox.", fg=self.colors["muted"], wraplength=420, justify="left").pack(anchor="w", pady=(0, 18))
        self._label(body, "Nom du créateur / joueur").pack(anchor="w")
        creator = self._entry(body)
        creator.insert(0, self.roblox.get("creator_name", "admine wind12"))
        creator.pack(fill="x", pady=(5, 14), ipady=7)
        status = self._label(body, "")
        status.pack(anchor="w")
        active_skin = self.roblox.get("active_skin")
        self._label(
            body,
            f"Skin équipé : {active_skin.get('name', 'Aucun')} " if isinstance(active_skin, dict) else "Skin équipé : aucun",
            fg=self.colors["accent"],
        ).pack(anchor="w", pady=(10, 4))
        self._label(body, f"Skins publiés : {len(self.roblox.get('published_skins', []))}").pack(anchor="w")

        self._button(body, "Créer ou publier un skin", self.open_roblox_skins).pack(anchor="w", pady=(8, 0))

        def save_name() -> None:
            name = creator.get().strip()
            if not name or len(name) > 32:
                status.configure(text="Entre 1 et 32 caractères.", fg="#db455b")
                return
            self.roblox["creator_name"] = name
            self.save_state()
            status.configure(text="Nom enregistré sur cet appareil.", fg="#1c935a")

        self._button(body, "Enregistrer le nom", save_name, bg=self.colors["accent"]).pack(anchor="e", pady=10)

    def _record_roblox_update(self, title: str, details: str) -> None:
        updates = self.roblox.setdefault("updates", [])
        updates.insert(
            0,
            {
                "title": title,
                "details": details,
                "date": time.strftime("%d/%m/%Y %H:%M"),
            },
        )
        del updates[50:]
        self.save_state()

    def open_roblox_updates(self) -> None:
        _, body = self._window("roblox_updates", "Roblox • Mises à jour", "680x510")
        for child in body.winfo_children():
            child.destroy()
        header = tk.Frame(body, bg=self.colors["bg"])
        header.pack(fill="x")
        self._label(header, "MISES À JOUR ROBLOX", font=("Segoe UI", 18, "bold")).pack(side="left")
        self._button(header, "Accueil", self.open_roblox_home).pack(side="right")
        self._label(
            body,
            "Historique local des jeux et skins publiés dans le simulateur.",
            fg=self.colors["muted"],
        ).pack(anchor="w", pady=(5, 12))
        feed = tk.Frame(body, bg=self.colors["bg"])
        feed.pack(fill="both", expand=True)
        updates = self.roblox.get("updates", [])
        if not updates:
            self._label(feed, "Aucune mise à jour pour le moment.\nPublie un jeu ou un skin pour le voir ici.", justify="left").pack(anchor="w", pady=12)
        for update in updates:
            if not isinstance(update, dict):
                continue
            card = tk.Frame(feed, bg=self.colors["panel"], padx=12, pady=10)
            card.pack(fill="x", pady=5)
            self._label(card, update.get("title", "Mise à jour"), bg=self.colors["panel"], font=("Segoe UI", 11, "bold")).pack(anchor="w")
            self._label(card, update.get("details", ""), bg=self.colors["panel"], fg=self.colors["muted"], wraplength=570, justify="left").pack(anchor="w", pady=(3, 5))
            self._label(card, update.get("date", ""), bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 8)).pack(anchor="w")

    def open_roblox_skins(self) -> None:
        _, body = self._window("roblox_skins", "Roblox Skins • Studio", "780x650")
        for child in body.winfo_children():
            child.destroy()
        draft = self.roblox.get("skin_draft", {})
        if not isinstance(draft, dict):
            draft = {}
        self._label(body, "ROBLOX SKINS STUDIO", font=("Segoe UI", 19, "bold")).pack(anchor="w")
        self._label(
            body,
            "Crée un skin, prévisualise-le, équipe-le ou publie-le dans le catalogue local.",
            fg=self.colors["muted"],
        ).pack(anchor="w", pady=(2, 10))

        name_row = tk.Frame(body, bg=self.colors["bg"])
        name_row.pack(fill="x", pady=(0, 9))
        self._label(name_row, "Nom du skin").pack(side="left")
        skin_name = self._entry(name_row)
        skin_name.insert(0, draft.get("name", "Mon skin"))
        skin_name.pack(side="left", fill="x", expand=True, padx=(8, 14), ipady=5)
        self._label(name_row, f"Créateur : {self.roblox.get('creator_name', 'admine wind12')}", fg=self.colors["accent"]).pack(side="right")

        editor = tk.Frame(body, bg=self.colors["bg"])
        editor.pack(fill="both", expand=True)
        preview = tk.Canvas(editor, width=350, height=365, bg="#b8e3ff", highlightthickness=0)
        preview.pack(side="left", fill="both", expand=True, padx=(0, 10))
        controls = tk.Frame(editor, bg=self.colors["panel"], padx=12, pady=10)
        controls.pack(side="right", fill="y")
        initial_colors = draft.get("colors", {})
        if not isinstance(initial_colors, dict):
            initial_colors = {}
        color_vars: dict[str, tk.StringVar] = {}
        color_rows = (
            ("Tête / peau", "head", "Peau dorée"),
            ("Chemise", "shirt", "Bleu"),
            ("Pantalon", "pants", "Noir"),
        )
        for label, key, default in color_rows:
            self._label(controls, label, bg=self.colors["panel"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(6, 2))
            stored = initial_colors.get(key, default)
            if stored not in SKIN_COLORS:
                stored = default
            variable = tk.StringVar(value=stored)
            color_vars[key] = variable
            ttk.Combobox(
                controls,
                textvariable=variable,
                values=list(SKIN_COLORS),
                state="readonly",
                width=18,
            ).pack(anchor="w")

        self._label(controls, "Accessoire (facultatif)", bg=self.colors["panel"]).pack(anchor="w", pady=(10, 3))
        accessory = self._entry(controls)
        accessory.insert(0, draft.get("accessory", ""))
        accessory.pack(fill="x", ipady=5)
        self._label(
            controls,
            "Astuce : sélectionne les couleurs,\npuis utilise l’aperçu.",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            justify="left",
        ).pack(anchor="w", pady=(10, 0))

        status = self._label(body, "")
        status.pack(anchor="w", pady=(5, 4))
        gallery = tk.Frame(body, bg=self.colors["bg"])
        gallery.pack(fill="x", pady=(2, 0))
        self._label(gallery, "MES SKINS PUBLIÉS", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        skin_list = tk.Listbox(
            gallery,
            bg=self.colors["panel"],
            fg=self.colors["fg"],
            selectbackground=self.colors["accent"],
            relief="flat",
            height=3,
            font=("Segoe UI", 9),
        )
        skin_list.pack(side="left", fill="x", expand=True, pady=(4, 0))

        def refresh_skins() -> None:
            skin_list.delete(0, "end")
            for skin in self.roblox.get("published_skins", []):
                if isinstance(skin, dict):
                    skin_list.insert("end", f"{skin.get('name', 'Skin')} — {skin.get('creator', 'Créateur')}")

        def equip_selected() -> None:
            selected = skin_list.curselection()
            published = [skin for skin in self.roblox.get("published_skins", []) if isinstance(skin, dict)]
            if selected and selected[0] < len(published):
                equip_skin(published[selected[0]])
            else:
                status.configure(text="Sélectionne d’abord un skin publié.", fg="#db455b")

        self._button(gallery, "Équiper", equip_selected).pack(side="right", padx=(8, 0), pady=(4, 0))

        def draw_preview() -> None:
            preview.delete("all")
            width = max(preview.winfo_width(), 350)
            preview.create_rectangle(0, 0, width, 365, fill="#b8e3ff", outline="")
            preview.create_oval(width - 95, 18, width - 35, 78, fill="#ffe58b", outline="")
            cx = width // 2
            head = SKIN_COLORS[color_vars["head"].get()]
            shirt = SKIN_COLORS[color_vars["shirt"].get()]
            pants = SKIN_COLORS[color_vars["pants"].get()]
            preview.create_rectangle(cx - 42, 87, cx + 42, 170, fill=head, outline="#455267", width=2)
            preview.create_oval(cx - 22, 113, cx - 15, 120, fill="#202630", outline="")
            preview.create_oval(cx + 15, 113, cx + 22, 120, fill="#202630", outline="")
            preview.create_line(cx - 12, 144, cx + 12, 144, fill="#754c3b", width=2)
            preview.create_rectangle(cx - 56, 176, cx + 56, 275, fill=shirt, outline="#455267", width=2)
            preview.create_rectangle(cx - 86, 181, cx - 58, 264, fill=shirt, outline="#455267", width=2)
            preview.create_rectangle(cx + 58, 181, cx + 86, 264, fill=shirt, outline="#455267", width=2)
            preview.create_rectangle(cx - 54, 280, cx - 6, 345, fill=pants, outline="#455267", width=2)
            preview.create_rectangle(cx + 6, 280, cx + 54, 345, fill=pants, outline="#455267", width=2)
            if accessory.get().strip():
                preview.create_rectangle(cx - 48, 73, cx + 48, 91, fill="#6745a6", outline="#39246b", width=2)
                preview.create_text(cx, 50, text=accessory.get().strip()[:18], fill="#273447", font=("Segoe UI", 9, "bold"))
            preview.create_text(12, 12, anchor="nw", text=skin_name.get().strip() or "Aperçu du skin", fill="#263849", font=("Segoe UI", 10, "bold"))

        def skin_data() -> dict:
            return {
                "name": skin_name.get().strip(),
                "creator": self.roblox.get("creator_name", "admine wind12"),
                "colors": {key: value.get() for key, value in color_vars.items()},
                "accessory": accessory.get().strip(),
            }

        def save_draft() -> None:
            skin = skin_data()
            if not skin["name"] or len(skin["name"]) > 32:
                status.configure(text="Le nom du skin doit contenir de 1 à 32 caractères.", fg="#db455b")
                return
            self.roblox["skin_draft"] = skin
            self.save_state()
            status.configure(text="Brouillon du skin enregistré sur cet appareil.", fg="#1c935a")

        def equip_skin(skin: dict) -> None:
            self.roblox["active_skin"] = skin
            self.save_state()
            status.configure(text=f"Skin équipé : {skin.get('name', 'Skin')}", fg="#1c935a")

        def publish_skin() -> None:
            skin = skin_data()
            if not skin["name"] or len(skin["name"]) > 32:
                status.configure(text="Le nom du skin doit contenir de 1 à 32 caractères.", fg="#db455b")
                return
            skin.update(id=str(time.time_ns()), published_at=time.strftime("%d/%m/%Y %H:%M"))
            self.roblox.setdefault("published_skins", []).insert(0, skin)
            self.roblox["active_skin"] = skin
            self.roblox["skin_draft"] = skin_data()
            refresh_skins()
            self._record_roblox_update("Nouveau skin publié", f"{skin['name']} par {skin['creator']} est disponible dans tes skins locaux.")
            status.configure(text=f"« {skin['name']} » publié et équipé !", fg="#1c935a")
            self.open_roblox_updates()

        for variable in color_vars.values():
            variable.trace_add("write", lambda *_: draw_preview())
        skin_name.bind("<KeyRelease>", lambda event: draw_preview())
        accessory.bind("<KeyRelease>", lambda event: draw_preview())
        self._button(controls, "Aperçu", draw_preview, bg=self.colors["raised"]).pack(fill="x", pady=(15, 4))
        self._button(controls, "Équiper ce skin", lambda: equip_skin(skin_data()), bg=self.colors["raised"]).pack(fill="x", pady=4)
        self._button(controls, "Enregistrer", save_draft).pack(fill="x", pady=4)
        self._button(controls, "Publier le skin", publish_skin, bg=self.colors["accent"]).pack(fill="x", pady=4)
        refresh_skins()
        draw_preview()

    @staticmethod
    def _admin_password_digest(password: str, salt_hex: str) -> str:
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            200_000,
        ).hex()

    def open_roblox_admin(self) -> None:
        """Set up or locally authenticate the simulated Roblox administrator."""
        is_setup = not self.roblox.get("admin_password_hash") or not self.roblox.get("admin_salt")
        dialog = tk.Toplevel(self.root)
        dialog.title("Créer l’accès administrateur" if is_setup else "Connexion administrateur")
        dialog.geometry("440x390" if is_setup else "440x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.configure(bg=self.colors["bg"])
        dialog.grab_set()
        frame = tk.Frame(dialog, bg=self.colors["bg"], padx=22, pady=18)
        frame.pack(fill="both", expand=True)
        title = "Créer le mode administrateur" if is_setup else "Mode administrateur"
        self._label(frame, title, font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(0, 7))
        self._label(
            frame,
            "Accès local au simulateur uniquement. Le mot de passe n’est pas envoyé à Roblox.",
            fg=self.colors["muted"],
            wraplength=390,
            justify="left",
        ).pack(anchor="w", pady=(0, 14))

        self._label(frame, "Nom administrateur").pack(anchor="w")
        admin_name = self._entry(frame)
        admin_name.insert(0, self.roblox.get("admin_name", self.roblox.get("creator_name", "admine wind12")))
        admin_name.pack(fill="x", pady=(4, 10), ipady=6)

        self._label(frame, "Mot de passe" if is_setup else "Mot de passe administrateur").pack(anchor="w")
        password = self._entry(frame, show="•")
        password.pack(fill="x", pady=(4, 10), ipady=6)
        confirmation = None
        if is_setup:
            self._label(frame, "Confirmer le mot de passe").pack(anchor="w")
            confirmation = self._entry(frame, show="•")
            confirmation.pack(fill="x", pady=(4, 10), ipady=6)
        status = self._label(frame, "", fg="#db455b", wraplength=390, justify="left")
        status.pack(anchor="w")

        def finish_login() -> None:
            if is_setup:
                pass_value = password.get()
                if len(pass_value) < 8:
                    status.configure(text="Choisis un mot de passe d’au moins 8 caractères.")
                    return
                if pass_value != confirmation.get():
                    status.configure(text="Les deux mots de passe ne correspondent pas.")
                    return
                salt = secrets.token_bytes(16).hex()
                self.roblox["admin_salt"] = salt
                self.roblox["admin_password_hash"] = self._admin_password_digest(pass_value, salt)
                self.roblox["admin_name"] = admin_name.get().strip() or "admine wind12"
                if not self.roblox.get("creator_name"):
                    self.roblox["creator_name"] = self.roblox["admin_name"]
                self.save_state()
            else:
                salt = self.roblox.get("admin_salt", "")
                expected = self.roblox.get("admin_password_hash", "")
                try:
                    actual = self._admin_password_digest(password.get(), salt)
                except (ValueError, TypeError):
                    status.configure(text="Configuration du mode administrateur invalide.")
                    return
                if not hmac.compare_digest(actual, expected):
                    status.configure(text="Mot de passe incorrect.")
                    password.delete(0, "end")
                    return
            name = admin_name.get().strip()
            if name:
                self.roblox["admin_name"] = name
                self.save_state()
            dialog.destroy()
            self._show_roblox_admin()

        actions = tk.Frame(frame, bg=self.colors["bg"])
        actions.pack(fill="x", pady=(14, 0))
        self._button(actions, "Annuler", dialog.destroy).pack(side="left")
        self._button(actions, "Créer l’accès" if is_setup else "Se connecter", finish_login, bg=self.colors["accent"]).pack(side="right")
        password.bind("<Return>", lambda event: finish_login())
        dialog.bind("<Escape>", lambda event: dialog.destroy())
        password.focus_set()

    def _show_roblox_admin(self) -> None:
        _, body = self._window("roblox_admin", "Roblox • Admin", "860x590")
        for child in body.winfo_children():
            child.destroy()
        admin_name = self.roblox.get("admin_name", "admine wind12")
        self._label(body, "PANNEAU ADMINISTRATEUR", font=("Segoe UI", 19, "bold")).pack(anchor="w")
        self._label(body, f"Connecté en tant que {admin_name}", fg=self.colors["muted"]).pack(anchor="w", pady=(2, 4))
        self._label(
            body,
            "Joueurs fictifs du simulateur — aucune donnée de compte ou de serveur Roblox réel.",
            fg="#d28a24",
            wraplength=800,
            justify="left",
        ).pack(anchor="w", pady=(0, 12))

        toolbar = tk.Frame(body, bg=self.colors["bg"])
        toolbar.pack(fill="x", pady=(0, 8))
        self._label(toolbar, "Tous les joueurs", font=("Segoe UI", 13, "bold")).pack(side="left")
        search = self._entry(toolbar)
        search.insert(0, "Filtrer par joueur ou jeu")
        search.pack(side="left", fill="x", expand=True, padx=12, ipady=5)
        table_frame = tk.Frame(body, bg=self.colors["bg"])
        table_frame.pack(fill="both", expand=True)
        columns = ("player", "status", "game")
        table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        table.heading("player", text="Nom du joueur")
        table.heading("status", text="Statut simulé")
        table.heading("game", text="Expérience")
        table.column("player", width=220, anchor="w")
        table.column("status", width=150, anchor="center")
        table.column("game", width=300, anchor="w")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        summary = self._label(body, "", fg=self.colors["muted"])
        summary.pack(anchor="w", pady=(8, 0))

        def refresh(filter_text: str = "") -> None:
            table.delete(*table.get_children())
            filtered = [
                (name, status, game)
                for name, status, game in SIMULATED_PLAYERS
                if filter_text.lower() in name.lower() or filter_text.lower() in game.lower()
            ]
            for name, status, game in filtered:
                table.insert("", "end", values=(name, status, game))
            online = sum(status == "En ligne" for _, status, _ in filtered)
            summary.configure(text=f"{len(filtered)} joueur(s) simulé(s) • {online} en ligne dans la démonstration")

        search.bind("<FocusIn>", lambda event: search.delete(0, "end") if search.get().startswith("Filtrer") else None)
        search.bind("<KeyRelease>", lambda event: refresh(search.get().strip()))
        self._button(toolbar, "Actualiser", lambda: refresh(search.get().strip())).pack(side="right")
        refresh()

    def open_roblox_studio(self) -> None:
        studio, body = self._window("roblox_studio", "Roblox Studio • créateur local", "1120x720")
        for child in body.winfo_children():
            child.destroy()
        draft = self.roblox.get("draft", {})
        if not isinstance(draft, dict):
            draft = {}
        self._label(body, "ROBLOX STUDIO", font=("Segoe UI", 19, "bold")).pack(anchor="w")
        self._label(body, "Carte sans limite fixe : clic droit-glisser pour explorer, clic gauche pour construire. Teste ou publie localement.", fg=self.colors["muted"]).pack(anchor="w", pady=(0, 9))
        metadata = tk.Frame(body, bg=self.colors["bg"])
        metadata.pack(fill="x", pady=(0, 8))
        self._label(metadata, "Nom du jeu").pack(side="left")
        game_name = self._entry(metadata)
        game_name.insert(0, draft.get("name", "Mon premier jeu"))
        game_name.pack(side="left", fill="x", expand=True, padx=(6, 14), ipady=5)
        self._label(metadata, "Créateur").pack(side="left")
        creator_name = self._entry(metadata)
        creator_name.insert(0, draft.get("creator", self.roblox.get("creator_name", "admine wind12")))
        creator_name.pack(side="left", fill="x", expand=True, padx=(6, 0), ipady=5)

        workspace = tk.Frame(body, bg=self.colors["bg"])
        workspace.pack(fill="both", expand=True)
        object_panel = tk.Frame(workspace, bg=self.colors["panel"], width=155)
        object_panel.pack(side="left", fill="y", padx=(0, 7))
        object_panel.pack_propagate(False)
        self._label(object_panel, "OUTILS", bg=self.colors["panel"], font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=9, pady=(8, 4))
        selected_tool = tk.StringVar(value="platform")
        tools = [("Plateforme", "platform"), ("Bloc", "block"), ("Pièce", "coin"), ("Point départ", "spawn"), ("Gomme", "erase")]
        for label, tool in tools:
            tk.Radiobutton(object_panel, text=label, variable=selected_tool, value=tool, bg=self.colors["panel"], fg=self.colors["fg"], selectcolor=self.colors["raised"], activebackground=self.colors["panel"], anchor="w").pack(fill="x", padx=5, pady=2)
        self._label(object_panel, "OBJETS", bg=self.colors["panel"], font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=9, pady=(15, 4))
        object_list = tk.Listbox(object_panel, bg=self.colors["raised"], fg=self.colors["fg"], relief="flat", font=("Segoe UI", 9), height=12)
        object_list.pack(fill="both", expand=True, padx=6, pady=(0, 7))

        scene = tk.Canvas(workspace, bg="#b8e3ff", highlightthickness=0, width=740, height=510, takefocus=True)
        scene.pack(side="left", fill="both", expand=True)
        properties = tk.Frame(workspace, bg=self.colors["panel"], width=155)
        properties.pack(side="right", fill="y", padx=(7, 0))
        properties.pack_propagate(False)
        self._label(properties, "PROPRIÉTÉS", bg=self.colors["panel"], font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=8, pady=8)
        self._label(properties, "Clique dans la scène\npour placer l’objet\nsélectionné.", bg=self.colors["panel"], fg=self.colors["muted"], justify="left").pack(anchor="w", padx=8)
        status = self._label(body, "Outils clavier : clique sur la scène pour y construire.")
        status.pack(anchor="w", pady=(7, 0))

        objects = draft.get("objects", [])
        if not isinstance(objects, list):
            objects = []
        objects = [dict(item) for item in objects if isinstance(item, dict)]
        saved_camera = draft.get("camera", {})
        if not isinstance(saved_camera, dict):
            saved_camera = {}
        camera = {
            "x": float(saved_camera.get("x", 0)),
            "y": float(saved_camera.get("y", 0)),
        }
        if not objects:
            objects = [
                {"type": "spawn", "x": 85, "y": 420},
                {"type": "platform", "x": 240, "y": 440},
                {"type": "platform", "x": 470, "y": 360},
                {"type": "coin", "x": 470, "y": 320},
            ]
        def redraw_scene() -> None:
            scene.delete("all")
            viewport_width = max(scene.winfo_width(), 740)
            viewport_height = max(scene.winfo_height(), 510)
            scene.create_rectangle(0, 0, viewport_width, viewport_height, fill="#b8e3ff", outline="")
            grid_size = 32
            start_x = math.floor(camera["x"] / grid_size) * grid_size
            start_y = math.floor(camera["y"] / grid_size) * grid_size
            for world_x in range(start_x, int(camera["x"] + viewport_width) + grid_size, grid_size):
                screen_x = world_x - camera["x"]
                scene.create_line(screen_x, 0, screen_x, viewport_height, fill="#a8d7f0")
            for world_y in range(start_y, int(camera["y"] + viewport_height) + grid_size, grid_size):
                screen_y = world_y - camera["y"]
                scene.create_line(0, screen_y, viewport_width, screen_y, fill="#a8d7f0")
            for index, item in enumerate(objects):
                x, y = item["x"] - camera["x"], item["y"] - camera["y"]
                if x < -100 or y < -100 or x > viewport_width + 100 or y > viewport_height + 100:
                    continue
                kind = item["type"]
                if kind == "platform":
                    scene.create_rectangle(x - 70, y - 10, x + 70, y + 10, fill="#319647", outline="#14592d", width=2, tags=f"object{index}")
                elif kind == "block":
                    scene.create_rectangle(x - 25, y - 25, x + 25, y + 25, fill="#e58a42", outline="#8b4a1f", width=2, tags=f"object{index}")
                elif kind == "coin":
                    scene.create_oval(x - 12, y - 12, x + 12, y + 12, fill="#ffd43b", outline="#a77800", width=2, tags=f"object{index}")
                elif kind == "spawn":
                    scene.create_rectangle(x - 12, y - 28, x + 12, y + 28, fill="#2587e8", outline="#144a82", width=2, tags=f"object{index}")
                    scene.create_text(x, y - 39, text="SPAWN", fill="#17344a", font=("Segoe UI", 8, "bold"), tags=f"object{index}")
            object_list.delete(0, "end")
            for index, item in enumerate(objects, start=1):
                object_list.insert("end", f"{index}. {item['type']}  ({item['x']}, {item['y']})")

        def place_object(event: tk.Event) -> None:
            x = round(event.x + camera["x"])
            y = round(event.y + camera["y"])
            tool = selected_tool.get()
            if tool == "erase":
                if objects:
                    nearest = min(range(len(objects)), key=lambda i: (objects[i]["x"] - x) ** 2 + (objects[i]["y"] - y) ** 2)
                    if (objects[nearest]["x"] - x) ** 2 + (objects[nearest]["y"] - y) ** 2 < 75**2:
                        objects.pop(nearest)
            else:
                objects.append({"type": tool, "x": x, "y": y})
            redraw_scene()
            status.configure(text=f"{len(objects)} objet(s) • position monde : {x}, {y}")

        pan_start: dict[str, float] = {}

        def begin_pan(event: tk.Event) -> None:
            pan_start.update(pointer_x=event.x, pointer_y=event.y, camera_x=camera["x"], camera_y=camera["y"])
            scene.configure(cursor="fleur")

        def move_pan(event: tk.Event) -> None:
            if not pan_start:
                return
            camera["x"] = max(-1_000_000_000, min(1_000_000_000, pan_start["camera_x"] + pan_start["pointer_x"] - event.x))
            camera["y"] = max(-1_000_000_000, min(1_000_000_000, pan_start["camera_y"] + pan_start["pointer_y"] - event.y))
            redraw_scene()
            status.configure(text=f"Carte infinie • caméra : {round(camera['x'])}, {round(camera['y'])}")

        def end_pan(event: tk.Event) -> None:
            pan_start.clear()
            scene.configure(cursor="")

        def delete_selected(event=None) -> None:
            selection = object_list.curselection()
            if selection:
                objects.pop(selection[0])
                redraw_scene()

        def project_data() -> dict:
            return {
                "name": game_name.get().strip(),
                "creator": creator_name.get().strip(),
                "objects": [dict(item) for item in objects],
                "camera": dict(camera),
            }

        def save_draft() -> None:
            project = project_data()
            if not project["name"] or not project["creator"]:
                status.configure(text="Le nom du jeu et celui du créateur sont requis.", fg="#db455b")
                return
            self.roblox["creator_name"] = project["creator"]
            self.roblox["draft"] = project
            self.save_state()
            status.configure(text="Brouillon enregistré sur cet appareil.", fg="#1c935a")

        def publish_game() -> None:
            project = project_data()
            if not project["name"] or len(project["name"]) > 48:
                status.configure(text="Donne un nom de jeu (1 à 48 caractères).", fg="#db455b")
                return
            if not project["creator"] or len(project["creator"]) > 32:
                status.configure(text="Le nom du créateur doit contenir 1 à 32 caractères.", fg="#db455b")
                return
            project.update(
                id=str(time.time_ns()),
                published_at=time.strftime("%Y-%m-%d %H:%M"),
            )
            self.roblox["creator_name"] = project["creator"]
            self.roblox.setdefault("published_games", []).insert(0, project)
            self.roblox["draft"] = project_data()
            self._record_roblox_update(
                "Nouveau jeu publié",
                f"{project['name']} par {project['creator']} est disponible dans tes jeux locaux.",
            )
            status.configure(text=f"« {project['name']} » publié dans le catalogue local !", fg="#1c935a")
            self.open_roblox_updates()

        toolbar = tk.Frame(body, bg=self.colors["bg"])
        toolbar.pack(fill="x", pady=(0, 8))
        self._button(toolbar, "Enregistrer", save_draft).pack(side="left", padx=(0, 6))
        self._button(toolbar, "Tester", lambda: self._play_published_game(project_data())).pack(side="left", padx=6)
        self._button(toolbar, "Publier localement", publish_game, bg="#1687e8").pack(side="right")
        self._button(properties, "Supprimer objet", delete_selected).pack(side="bottom", padx=7, pady=8, fill="x")
        scene.bind("<Button-1>", place_object)
        scene.bind("<ButtonPress-3>", begin_pan)
        scene.bind("<B3-Motion>", move_pan)
        scene.bind("<ButtonRelease-3>", end_pan)
        scene.bind("<Configure>", lambda event: redraw_scene())
        object_list.bind("<Delete>", delete_selected)
        redraw_scene()

    def _play_published_game(self, project: dict) -> None:
        title = project.get("name", "Jeu publié")
        game, body = self._window(f"published_{project.get('id', title)}", f"Jouer • {title}", "800x580")
        for child in body.winfo_children():
            child.destroy()
        self._label(body, f"{title}  •  par {project.get('creator', 'Créateur')}", font=("Segoe UI", 15, "bold")).pack(anchor="w")
        self._label(body, "Aperçu local • utilise les flèches à l’écran ou le clavier : ←/→ pour courir, ↑ pour sauter.", fg=self.colors["muted"]).pack(anchor="w", pady=(0, 8))
        scene = tk.Canvas(body, width=740, height=455, bg="#a9ddff", highlightthickness=0, takefocus=True)
        scene.pack(fill="both", expand=True)
        controls = tk.Frame(body, bg=self.colors["bg"])
        controls.pack(fill="x", pady=(8, 0))
        objects = [item for item in project.get("objects", []) if isinstance(item, dict)]
        spawn = next((item for item in objects if item.get("type") == "spawn"), {"x": 48, "y": 425})
        camera_x = float(spawn.get("x", 48)) - 48
        camera_y = float(spawn.get("y", 425)) - 425
        state = {
            "x": 36.0,
            "y": 397.0,
            "vy": 0.0,
            "left": False,
            "right": False,
            "ground": False,
        }
        platforms = [
            (item["x"] - camera_x, item["y"] - camera_y)
            for item in objects
            if item.get("type") == "platform"
        ]
        platforms.append((390, 442))

        def draw() -> None:
            scene.delete("all")
            scene.create_rectangle(0, 0, 780, 455, fill="#a9ddff", outline="")
            scene.create_rectangle(0, 432, 780, 455, fill="#52a44c", outline="")
            for item in objects:
                x = item.get("x", 0) - camera_x
                y = item.get("y", 0) - camera_y
                kind = item.get("type")
                if kind == "platform":
                    scene.create_rectangle(x - 70, y - 10, x + 70, y + 10, fill="#319647", outline="#14592d", width=2)
                elif kind == "block":
                    scene.create_rectangle(x - 25, y - 25, x + 25, y + 25, fill="#e58a42", outline="#8b4a1f", width=2)
                elif kind == "coin":
                    scene.create_oval(x - 12, y - 12, x + 12, y + 12, fill="#ffd43b", outline="#a77800", width=2)
                elif kind == "spawn":
                    scene.create_rectangle(x - 12, y - 28, x + 12, y + 28, fill="#2587e8", outline="#144a82", width=2)
            scene.create_rectangle(state["x"], state["y"], state["x"] + 25, state["y"] + 35, fill="#1687e8", outline="#07549b", width=2)

        def key_down(event: tk.Event) -> str:
            key = event.keysym.lower()
            if key in {"left", "a"}:
                state["left"] = True
            elif key in {"right", "d"}:
                state["right"] = True
            elif key in {"space", "up", "w"} and state["ground"]:
                state["vy"] = -11.5
                state["ground"] = False
            return "break"

        def key_up(event: tk.Event) -> str:
            if event.keysym.lower() in {"left", "a"}:
                state["left"] = False
            elif event.keysym.lower() in {"right", "d"}:
                state["right"] = False
            return "break"

        def set_direction(direction: str, pressed: bool) -> None:
            state[direction] = pressed
            if not pressed:
                scene.after_idle(scene.focus_set)

        def jump() -> None:
            if state["ground"] and state["y"] < 420:
                state["vy"] = -11.5
                state["ground"] = False

        for label, direction in (("◀", "left"), ("▶", "right")):
            button = self._button(controls, label, lambda: None, font=("Segoe UI", 14, "bold"), padx=18, takefocus=False)
            button.pack(side="left", padx=4)
            button.bind("<ButtonPress-1>", lambda event, key=direction: set_direction(key, True))
            button.bind("<ButtonRelease-1>", lambda event, key=direction: set_direction(key, False))
            button.bind("<Leave>", lambda event, key=direction: set_direction(key, False))
        self._button(controls, "▲ Sauter", jump, bg=self.colors["accent"], takefocus=False).pack(side="left", padx=4)

        scene.bind("<KeyPress>", key_down)
        scene.bind("<KeyRelease>", key_up)
        scene.focus_set()

        def tick() -> None:
            if not game.winfo_exists():
                return
            old_bottom = state["y"] + 35
            state["x"] = max(0, min(750, state["x"] + (int(state["right"]) - int(state["left"])) * 4))
            state["vy"] = min(13, state["vy"] + .65)
            next_y = state["y"] + state["vy"]
            state["ground"] = False
            for x, y in platforms:
                if state["x"] + 25 > x - 70 and state["x"] < x + 70 and state["vy"] >= 0 and old_bottom <= y - 10 <= next_y + 35:
                    next_y = y - 45
                    state["vy"] = 0
                    state["ground"] = True
                    break
            state["y"] = next_y
            if state["y"] > 455:
                state.update(
                    x=max(0.0, min(750.0, float(spawn.get("x", 48)) - 12)),
                    y=max(0.0, float(spawn.get("y", 425)) - 28),
                    vy=0.0,
                )
            draw()
            game.after(30, tick)

        draw()
        game.after(30, tick)

    def open_games(self) -> None:
        _, body = self._window("games", "Jeux installés", "620x520")
        for child in body.winfo_children():
            child.destroy()
        self._label(body, "MES JEUX", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        self._label(body, "Lance les jeux installés ou ouvre le catalogue.", fg=self.colors["muted"]).pack(anchor="w", pady=(2, 10))
        self._button(body, "Ouvrir le catalogue de jeux", self.open_store, bg="#1687e8").pack(anchor="w", pady=(0, 10))
        list_area = tk.Frame(body, bg=self.colors["bg"])
        list_area.pack(fill="both", expand=True)
        canvas = tk.Canvas(list_area, bg=self.colors["bg"], highlightthickness=0)
        scroll = ttk.Scrollbar(list_area, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        rows = tk.Frame(canvas, bg=self.colors["bg"])
        window_id = canvas.create_window((0, 0), window=rows, anchor="nw")
        rows.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window_id, width=event.width))
        available = self._store_catalog()
        installed_apps = set(self.roblox.get("installed_apps", []))
        installed_games = set(self.roblox.get("installed_games", []))
        installed_items = [item for item in available if item["id"] in (installed_apps if item["kind"] == "app" else installed_games)]
        if not installed_items:
            self._label(rows, "Aucun jeu installé pour le moment. Choisis-en dans le catalogue.", fg=self.colors["muted"], wraplength=480).pack(anchor="w", pady=12)
        for item in installed_items:
            card = tk.Frame(rows, bg=self.colors["panel"], padx=10, pady=8)
            card.pack(fill="x", pady=4)
            self._label(card, item["name"], bg=self.colors["panel"], font=("Segoe UI", 11, "bold")).pack(side="left")
            self._button(card, "Ouvrir" if item["kind"] == "app" else "Jouer", item["action"], bg=self.colors["accent"]).pack(side="right")

    def _store_catalog(self) -> list[dict]:
        items = [
            {"id": "roblox", "kind": "app", "name": "Roblox", "description": "Explorer les jeux et ton catalogue local.", "action": self.open_roblox_home},
            {"id": "roblox_studio", "kind": "app", "name": "Roblox Studio", "description": "Créer des mondes et publier des jeux dans ce simulateur.", "action": self.open_roblox_studio},
            {"id": "roblox_skins", "kind": "app", "name": "Roblox Skins Studio", "description": "Créer, prévisualiser et publier des skins locaux.", "action": self.open_roblox_skins},
            {"id": "play_store", "kind": "app", "name": "Play Store", "description": "Installer et lancer des jeux dans le catalogue local.", "action": self.open_store},
            {"id": "play_store_studio", "kind": "app", "name": "Play Store Studio", "description": "Gérer et publier les jeux Roblox Studio dans le Play Store local.", "action": self.open_play_store_studio},
            {"id": "roblox_obby", "kind": "game", "name": "Roblox Obby", "description": "Parcours de plateformes et pièces à récupérer.", "action": lambda: self.open_roblox_game("Normal")},
            {"id": "obby_impossible", "kind": "game", "name": "Obby Impossible", "description": "Plateformes étroites et trois vies.", "action": lambda: self.open_roblox_game("Impossible")},
            {"id": "night_shift", "kind": "game", "name": "Night Shift", "description": "Jeu d’exploration et d’horreur simulé.", "action": self.open_horror},
            {"id": "matrix_runner", "kind": "game", "name": "Matrix Runner", "description": "Animation interactive de code.", "action": lambda: self.start_effect("matrix")},
        ]
        listed_games = set(self.roblox.get("play_store_games", []))
        for index, project in enumerate(self.roblox.get("published_games", [])):
            if isinstance(project, dict):
                project_id = str(project.get("id", f"local-{index}"))
                if project_id not in listed_games:
                    continue
                items.append({
                    "id": f"published:{project_id}",
                    "kind": "game",
                    "name": project.get("name", "Jeu créé"),
                    "description": f"Créé par {project.get('creator', 'Créateur')} • publié localement dans Play Store",
                    "action": lambda game=project: self._play_published_game(game),
                })
        return items

    def open_store(self) -> None:
        _, body = self._window("store", "Play Store • Jeux et applications", "760x620")
        for child in body.winfo_children():
            child.destroy()
        header = tk.Frame(body, bg=self.colors["bg"])
        header.pack(fill="x")
        self._label(header, "PLAY STORE", font=("Segoe UI", 18, "bold")).pack(side="left")
        self._button(header, "Play Store Studio", self.open_play_store_studio, bg=self.colors["accent"]).pack(side="right")
        self._label(body, "CATALOGUE • INSTALLER ET JOUER", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(5, 0))
        self._label(body, "Catalogue et installations simulés localement; aucun fichier Windows ni service Google ou Roblox n’est modifié.", fg=self.colors["muted"], wraplength=700, justify="left").pack(anchor="w", pady=(2, 9))
        search = self._entry(body)
        search.insert(0, "Rechercher un jeu ou une application…")
        search.pack(fill="x", pady=(0, 8), ipady=6)
        search.bind("<FocusIn>", lambda event: search.delete(0, "end") if search.get().startswith("Rechercher") else None)
        status = self._label(body, "")
        status.pack(anchor="w", pady=(0, 5))
        area = tk.Frame(body, bg=self.colors["bg"])
        area.pack(fill="both", expand=True)
        canvas = tk.Canvas(area, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(area, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        catalog_frame = tk.Frame(canvas, bg=self.colors["bg"])
        window_id = canvas.create_window((0, 0), window=catalog_frame, anchor="nw")
        catalog_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window_id, width=event.width))

        def render(filter_text: str = "") -> None:
            for child in catalog_frame.winfo_children():
                child.destroy()
            apps = set(self.roblox.get("installed_apps", []))
            games = set(self.roblox.get("installed_games", []))
            items = [
                item for item in self._store_catalog()
                if filter_text.lower() in item["name"].lower() or filter_text.lower() in item["description"].lower()
            ]
            if not items:
                self._label(catalog_frame, "Aucun résultat dans le catalogue.", fg=self.colors["muted"]).pack(anchor="w", pady=10)
                return
            for item in items:
                installed = item["id"] in (apps if item["kind"] == "app" else games)
                row = tk.Frame(catalog_frame, bg=self.colors["panel"], padx=11, pady=8)
                row.pack(fill="x", pady=4)
                details = tk.Frame(row, bg=self.colors["panel"])
                details.pack(side="left", fill="x", expand=True)
                self._label(details, item["name"], bg=self.colors["panel"], font=("Segoe UI", 11, "bold")).pack(anchor="w")
                self._label(details, item["description"], bg=self.colors["panel"], fg=self.colors["muted"], wraplength=470, justify="left").pack(anchor="w", pady=(2, 0))
                button_text = ("Ouvrir" if item["kind"] == "app" else "Jouer") if installed else "Installer"

                def activate(entry=item, is_installed=installed) -> None:
                    if is_installed:
                        entry["action"]()
                        return
                    target = self.roblox.setdefault("installed_apps" if entry["kind"] == "app" else "installed_games", [])
                    target.append(entry["id"])
                    self.save_state()
                    status.configure(text=f"{entry['name']} installé dans le simulateur.")
                    render(search.get().strip())

                self._button(row, button_text, activate, bg=self.colors["accent"] if installed else self.colors["raised"]).pack(side="right", padx=(8, 0))

        search.bind("<KeyRelease>", lambda event: render(search.get().strip()))
        render()

    def open_play_store_studio(self) -> None:
        _, body = self._window("play_store_studio", "Play Store Studio • Publications locales", "760x600")
        for child in body.winfo_children():
            child.destroy()
        header = tk.Frame(body, bg=self.colors["bg"])
        header.pack(fill="x")
        self._label(header, "PLAY STORE STUDIO", font=("Segoe UI", 19, "bold")).pack(side="left")
        self._button(header, "Ouvrir Play Store", self.open_store, bg=self.colors["accent"]).pack(side="right")
        self._label(
            body,
            "Publie ici les jeux déjà publiés dans Roblox Studio. Ils apparaîtront dans le catalogue local; cette action ne publie rien sur les vrais services Roblox ou Google.",
            fg=self.colors["muted"],
            wraplength=700,
            justify="left",
        ).pack(anchor="w", pady=(4, 10))
        toolbar = tk.Frame(body, bg=self.colors["bg"])
        toolbar.pack(fill="x", pady=(0, 8))
        self._button(toolbar, "Créer un jeu dans Roblox Studio", self.open_roblox_studio, bg="#1687e8").pack(side="left")
        status = self._label(toolbar, "")
        status.pack(side="right")

        area = tk.Frame(body, bg=self.colors["bg"])
        area.pack(fill="both", expand=True)
        canvas = tk.Canvas(area, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(area, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        rows = tk.Frame(canvas, bg=self.colors["bg"])
        window_id = canvas.create_window((0, 0), window=rows, anchor="nw")
        rows.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window_id, width=event.width))

        def render() -> None:
            for child in rows.winfo_children():
                child.destroy()
            projects = [
                (index, project)
                for index, project in enumerate(self.roblox.get("published_games", []))
                if isinstance(project, dict)
            ]
            if not projects:
                self._label(
                    rows,
                    "Aucun jeu Roblox Studio publié pour le moment.\nCrée un monde dans Roblox Studio, puis clique sur « Publier localement ».",
                    fg=self.colors["muted"],
                    wraplength=620,
                    justify="left",
                ).pack(anchor="w", pady=12)
                return
            listed_games = set(self.roblox.get("play_store_games", []))
            for index, project in projects:
                project_id = str(project.get("id", f"local-{index}"))
                is_listed = project_id in listed_games
                card = tk.Frame(rows, bg=self.colors["panel"], padx=12, pady=10)
                card.pack(fill="x", pady=4)
                details = tk.Frame(card, bg=self.colors["panel"])
                details.pack(side="left", fill="x", expand=True)
                self._label(details, project.get("name", "Jeu sans titre"), bg=self.colors["panel"], font=("Segoe UI", 11, "bold")).pack(anchor="w")
                object_count = len(project.get("objects", [])) if isinstance(project.get("objects", []), list) else 0
                self._label(
                    details,
                    f"Créateur : {project.get('creator', 'Créateur')} • {object_count} objets • {'Dans Play Store' if is_listed else 'Non publié dans Play Store'}",
                    bg=self.colors["panel"],
                    fg=self.colors["muted"],
                ).pack(anchor="w", pady=(2, 0))

                def toggle_listing(game_id=project_id, game=project, listed=is_listed) -> None:
                    stored = self.roblox.setdefault("play_store_games", [])
                    if listed:
                        stored[:] = [item for item in stored if str(item) != game_id]
                        self.save_state()
                        status.configure(text="Retiré du Play Store local.")
                    else:
                        if game_id not in [str(item) for item in stored]:
                            stored.append(game_id)
                        self._record_roblox_update(
                            "Jeu publié sur Play Store",
                            f"{game.get('name', 'Jeu sans titre')} par {game.get('creator', 'Créateur')} est maintenant disponible dans le catalogue local.",
                        )
                        status.configure(text="Jeu publié dans le Play Store local.")
                    render()

                self._button(
                    card,
                    "Retirer" if is_listed else "Publier dans Play Store",
                    toggle_listing,
                    bg=self.colors["raised"] if is_listed else self.colors["accent"],
                ).pack(side="right", padx=(8, 0))

        render()

    def open_roblox_game(self, difficulty: str = "Normal") -> None:
        game, body = self._window("roblox_obby", f"Roblox Obby • {difficulty}", "820x610")
        previous_job = getattr(game, "_roblox_job", None)
        if previous_job:
            try:
                game.after_cancel(previous_job)
            except tk.TclError:
                pass
        game._roblox_job = None
        for child in body.winfo_children():
            child.destroy()
        header = tk.Frame(body, bg=self.colors["bg"])
        header.pack(fill="x", pady=(0, 8))
        if self.roblox_logo:
            tk.Label(header, image=self.roblox_logo, bg=self.colors["bg"]).pack(side="left", padx=(0, 12))
        self._label(header, "ROBLOX OBBY", font=("Segoe UI", 19, "bold")).pack(side="left")
        difficulty_tip = "MODE IMPOSSIBLE : plateformes étroites, sauts précis, 3 vies" if difficulty == "Impossible" else "Mode normal"
        self._label(body, f"{difficulty_tip} • boutons à l’écran ou ←/→ • ↑/Espace pour sauter • R pour recommencer", fg=self.colors["muted"]).pack(anchor="w", pady=(0, 8))
        scene = tk.Canvas(body, width=780, height=410, bg="#83c9f5", highlightthickness=0, takefocus=True)
        scene.pack(fill="both", expand=True)
        controls = tk.Frame(body, bg=self.colors["bg"])
        controls.pack(fill="x", pady=(8, 0))
        footer = tk.Frame(body, bg=self.colors["bg"])
        footer.pack(fill="x", pady=(8, 0))
        status = self._label(footer, "Ramasse les 5 pièces puis rejoins le drapeau !")
        status.pack(side="left")
        self._button(footer, "Recommencer", lambda: reset_game(), bg=self.colors["accent"]).pack(side="right")

        canvas_width, canvas_height = 780, 410
        player_w, player_h = 28, 38
        if difficulty == "Impossible":
            platforms = [
                (0, 370, 132, 410), (175, 318, 215, 334), (260, 265, 300, 281),
                (345, 310, 382, 326), (426, 238, 464, 254), (510, 288, 548, 304),
                (590, 220, 628, 236), (673, 190, 780, 206),
            ]
            coins = [(187, 294), (272, 241), (357, 286), (438, 214), (522, 264), (602, 196), (720, 166)]
        else:
            platforms = [
                (0, 370, 160, 410),
                (205, 316, 340, 332),
                (385, 258, 515, 274),
                (555, 200, 780, 216),
            ]
            coins = [(245, 292), (420, 234), (475, 234), (590, 176), (680, 176)]
        state = {
            "x": 28.0,
            "y": 332.0,
            "vy": 0.0,
            "grounded": False,
            "left": False,
            "right": False,
            "collected": set(),
            "won": False,
            "lives": 3,
        }

        def reset_game() -> None:
            state.update(x=28.0, y=332.0, vy=0.0, grounded=False, left=False, right=False, collected=set(), won=False, lives=3)
            status.configure(text="Ramasse les 5 pièces puis rejoins le drapeau !")
            draw_scene()
            if not game._roblox_job:
                game._roblox_job = game.after(30, tick)

        def key_down(event: tk.Event) -> str:
            key = event.keysym.lower()
            if key in {"left", "a"}:
                state["left"] = True
            elif key in {"right", "d"}:
                state["right"] = True
            elif key in {"space", "up", "w"} and state["grounded"] and not state["won"]:
                state["vy"] = -12.5
                state["grounded"] = False
            elif key == "r":
                reset_game()
            return "break"

        def key_up(event: tk.Event) -> str:
            key = event.keysym.lower()
            if key in {"left", "a"}:
                state["left"] = False
            elif key in {"right", "d"}:
                state["right"] = False
            return "break"

        def set_direction(direction: str, pressed: bool) -> None:
            state[direction] = pressed
            if not pressed:
                scene.after_idle(scene.focus_set)

        def jump() -> None:
            if state["grounded"] and not state["won"]:
                state["vy"] = -12.5
                state["grounded"] = False

        for label, direction in (("◀", "left"), ("▶", "right")):
            button = self._button(controls, label, lambda: None, font=("Segoe UI", 14, "bold"), padx=18, takefocus=False)
            button.pack(side="left", padx=4)
            button.bind("<ButtonPress-1>", lambda event, key=direction: set_direction(key, True))
            button.bind("<ButtonRelease-1>", lambda event, key=direction: set_direction(key, False))
            button.bind("<Leave>", lambda event, key=direction: set_direction(key, False))
        self._button(controls, "▲ Sauter", jump, bg=self.colors["accent"], takefocus=False).pack(side="left", padx=4)

        scene.bind("<KeyPress>", key_down)
        scene.bind("<KeyRelease>", key_up)
        scene.bind("<Button-1>", lambda event: scene.focus_set())
        scene.focus_set()

        def draw_scene() -> None:
            scene.delete("all")
            scene.create_rectangle(0, 0, canvas_width, canvas_height, fill="#83c9f5", outline="")
            scene.create_oval(625, 24, 705, 104, fill="#ffe58b", outline="")
            scene.create_oval(42, 48, 91, 73, fill="#e9f8ff", outline="")
            scene.create_oval(76, 43, 126, 74, fill="#e9f8ff", outline="")
            scene.create_oval(650, 114, 697, 140, fill="#e9f8ff", outline="")
            scene.create_oval(681, 108, 732, 141, fill="#e9f8ff", outline="")
            for x1, y1, x2, y2 in platforms:
                scene.create_rectangle(x1, y1, x2, y2, fill="#287d46", outline="#14592d", width=2)
                scene.create_rectangle(x1, y1, x2, y1 + 6, fill="#72d657", outline="")
            scene.create_line(729, 200, 729, 143, fill="#5a3822", width=5)
            scene.create_polygon(731, 144, 770, 156, 731, 168, fill="#ff475d", outline="")
            for index, (coin_x, coin_y) in enumerate(coins):
                if index not in state["collected"]:
                    scene.create_oval(coin_x - 9, coin_y - 9, coin_x + 9, coin_y + 9, fill="#ffd43b", outline="#fff3a8", width=2)
                    scene.create_text(coin_x, coin_y, text="$", fill="#8c5c00", font=("Segoe UI", 9, "bold"))
            x, y = state["x"], state["y"]
            scene.create_rectangle(x + 5, y, x + 23, y + 18, fill="#ffd1a6", outline="#744a38")
            scene.create_rectangle(x + 2, y + 18, x + 26, y + 33, fill="#1687e8", outline="#07549b")
            scene.create_rectangle(x + 3, y + 33, x + 12, y + 38, fill="#303847", outline="")
            scene.create_rectangle(x + 16, y + 33, x + 25, y + 38, fill="#303847", outline="")
            scene.create_oval(x + 9, y + 6, x + 11, y + 8, fill="#1d2733", outline="")
            scene.create_oval(x + 17, y + 6, x + 19, y + 8, fill="#1d2733", outline="")
            scene.create_text(10, 12, anchor="nw", text=f"PIÈCES : {len(state['collected'])}/{len(coins)}   VIES : {state['lives']}", fill="#17344a", font=("Segoe UI", 11, "bold"))

        def tick() -> None:
            game._roblox_job = None
            if not game.winfo_exists():
                return
            if state["won"] or state["lives"] <= 0:
                return
            else:
                old_bottom = state["y"] + player_h
                direction = int(state["right"]) - int(state["left"])
                move_speed = 3.3 if difficulty == "Impossible" else 4.2
                gravity = 0.78 if difficulty == "Impossible" else 0.65
                state["x"] = min(canvas_width - player_w, max(0, state["x"] + direction * move_speed))
                state["vy"] = min(14.5, state["vy"] + gravity)
                next_y = state["y"] + state["vy"]
                state["grounded"] = False
                if state["vy"] >= 0:
                    for x1, top, x2, _ in platforms:
                        overlaps = state["x"] + player_w > x1 and state["x"] < x2
                        if overlaps and old_bottom <= top and next_y + player_h >= top:
                            next_y = top - player_h
                            state["vy"] = 0.0
                            state["grounded"] = True
                            break
                state["y"] = next_y
                for index, (coin_x, coin_y) in enumerate(coins):
                    if index not in state["collected"] and abs(state["x"] + player_w / 2 - coin_x) < 23 and abs(state["y"] + player_h / 2 - coin_y) < 28:
                        state["collected"].add(index)
                        status.configure(text=f"Pièce récupérée : {len(state['collected'])}/5")
                if state["y"] > canvas_height + 20:
                    state["lives"] -= 1
                    state["x"], state["y"], state["vy"] = 28.0, 332.0, 0.0
                    if state["lives"] <= 0:
                        status.configure(text="Partie terminée ! Appuie sur R pour retenter le parcours.")
                    else:
                        status.configure(text=f"Chute ! Il te reste {state['lives']} vie(s).")
                if state["x"] > 700 and state["y"] + player_h <= 220:
                    if len(state["collected"]) == len(coins):
                        state["won"] = True
                        status.configure(text="Bravo ! Tu as terminé le parcours Roblox Obby !")
                    else:
                        state["x"] = 675.0
                        status.configure(text="Il te manque des pièces pour atteindre le drapeau.")
                draw_scene()
            game._roblox_job = game.after(30, tick)

        draw_scene()
        game._roblox_job = game.after(30, tick)

    def open_music(self) -> None:
        _, body = self._window("music", "Soundwave", "480x370")
        for child in body.winfo_children():
            child.destroy()
        self._label(body, "SOUNDWAVE", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tracks = tk.Listbox(body, bg=self.colors["panel"], fg=self.colors["fg"], selectbackground=self.colors["accent"], relief="flat")
        for track in ("Aurora Protocol", "Neon Skyline", "Deep Space", "Midnight Circuit"):
            tracks.insert("end", track)
        tracks.selection_set(0)
        tracks.pack(fill="both", expand=True, pady=10)
        status = self._label(body, "Prêt — pistes de démonstration")
        status.pack(anchor="w")
        playing = {"value": False}
        button = self._button(body, "Lecture simulée", lambda: None, bg=self.colors["accent"])

        def toggle() -> None:
            playing["value"] = not playing["value"]
            status.configure(text="Lecture simulée…" if playing["value"] else "En pause")
            button.configure(text="Pause" if playing["value"] else "Lecture simulée")

        button.configure(command=toggle)
        button.pack(anchor="e", pady=8)

    def open_horror(self) -> None:
        _, body = self._window("horror", "NIGHT SHIFT", "600x440")
        for child in body.winfo_children():
            child.destroy()
        self._label(body, "NIGHT SHIFT", font=("Segoe UI", 23, "bold")).pack(anchor="w")
        self._label(body, "Jeu d’exploration fictif • aucun son ni fichier externe.", fg=self.colors["muted"]).pack(anchor="w", pady=8)
        difficulty = tk.StringVar(value="Normal")
        ttk.Combobox(body, textvariable=difficulty, values=["Calme", "Normal", "Intense"], state="readonly").pack(anchor="w", pady=10)
        self._button(body, "PLAY", lambda: self._play_horror(difficulty.get()), bg=self.colors["accent"], font=("Segoe UI", 14, "bold")).pack(anchor="e", pady=15)

    def _play_horror(self, difficulty: str) -> None:
        game, body = self._window("horror_game", "NIGHT SHIFT • " + difficulty)
        for child in body.winfo_children():
            child.destroy()
        rooms = [["Hall", "Study", "Bedroom"], ["Kitchen", "Foyer", "Attic"], ["Cellar", "Garden", "Exit"]]
        state = {"x": 1, "y": 1, "monster": (2, 0), "light": False, "ended": False, "moves": 0}
        title = self._label(body, "", font=("Segoe UI", 16, "bold"))
        title.pack(anchor="w")
        scene = tk.Canvas(body, bg="#080d16", height=190, highlightthickness=0)
        scene.pack(fill="both", expand=True, pady=8)
        status = self._label(body, "Explorez les pièces et trouvez la sortie.")
        status.pack(anchor="w")
        controls = tk.Frame(body, bg=self.colors["bg"])
        controls.pack(fill="x", pady=7)

        def redraw() -> None:
            title.configure(text="PIÈCE : " + rooms[state["y"]][state["x"]].upper())
            scene.delete("all")
            scene.create_rectangle(0, 0, 900, 240, fill="#111a2a", outline="#263249")
            scene.create_rectangle(370, 45, 530, 220, fill="#080d16", outline="#687991", width=2)
            if state["light"]:
                scene.create_oval(190, 25, 710, 235, fill="#829dbb", stipple="gray75", outline="")
            if state["monster"] == (state["x"], state["y"]):
                scene.create_text(450, 120, text="◉     ◉\n  ▽", fill="#ff344e", font=("Consolas", 38, "bold"))
            else:
                scene.create_text(450, 120, text="La pièce est sombre…", fill="#bdc9d8", font=("Segoe UI", 12))

        def move(dx: int, dy: int) -> None:
            if state["ended"]:
                return
            nx, ny = state["x"] + dx, state["y"] + dy
            if not (0 <= nx < 3 and 0 <= ny < 3):
                status.configure(text="Cette porte est verrouillée.")
                return
            state.update(x=nx, y=ny)
            state["moves"] += 1
            if state["moves"] % 2 == 0:
                mx, my = state["monster"]
                state["monster"] = (mx - 1, my) if mx > 0 else (mx, min(2, my + 1))
            if state["monster"] == (nx, ny):
                state["ended"] = True
                scene.configure(bg="#270811")
                scene.delete("all")
                scene.create_text(450, 100, text="FIN DE PARTIE", fill="#ff3655", font=("Segoe UI", 24, "bold"))
                status.configure(text="Jumpscare simulé — recommencez si vous le souhaitez.")
                self._button(controls, "Recommencer", lambda: self._play_horror(difficulty)).pack(side="right")
            elif rooms[ny][nx] == "Exit":
                state["ended"] = True
                scene.delete("all")
                scene.create_text(450, 100, text="VOUS ÊTES LIBRE", fill="#78ffae", font=("Segoe UI", 24, "bold"))
                status.configure(text="Bravo, vous avez trouvé la sortie !")
            else:
                status.configure(text=f"Porte franchie • {difficulty}")
                redraw()

        for label, dx, dy in (("↑ Nord", 0, -1), ("↓ Sud", 0, 1), ("← Ouest", -1, 0), ("→ Est", 1, 0)):
            self._button(controls, label, lambda x=dx, y=dy: move(x, y)).pack(side="left", padx=2)
        light = self._button(controls, "Lampe : OFF", lambda: None, bg="#735929")
        light.pack(side="right")

        def toggle_light() -> None:
            state["light"] = not state["light"]
            light.configure(text=f"Lampe : {'ON' if state['light'] else 'OFF'}")
            redraw()

        light.configure(command=toggle_light)
        redraw()

    def open_terminal(self) -> None:
        _, body = self._window("terminal", "Terminal X", "700x460")
        for child in body.winfo_children():
            child.destroy()
        output = tk.Text(body, bg="#050d10", fg="#75ff9a", insertbackground="#75ff9a", relief="flat", font=("Consolas", 10), wrap="word")
        output.pack(fill="both", expand=True)
        output.insert("end", "WINDOWS 12 ULTIMATE // TERMINAL DE SIMULATION\nAucune commande système réelle n’est exécutée.\nTapez help.\n\n")
        output.configure(state="disabled")
        entry = tk.Entry(body, bg="#050d10", fg="#75ff9a", insertbackground="#75ff9a", relief="flat", font=("Consolas", 11))
        entry.pack(fill="x", pady=(8, 0), ipady=6)

        def write(text: str) -> None:
            output.configure(state="normal")
            if text == "\0clear":
                output.delete("1.0", "end")
            else:
                output.insert("end", text + "\n")
            output.see("end")
            output.configure(state="disabled")

        def submit(event=None) -> None:
            command = entry.get().strip()
            entry.delete(0, "end")
            if not command:
                return
            write(f"guest@w12 $ {command}")
            self._terminal_command(command, write)

        entry.bind("<Return>", submit)
        entry.focus_set()

    def _terminal_command(self, command: str, write) -> None:
        if self.handle_secret(command):
            write("Commande secrète activée.")
            return
        key = command.lower().strip()
        commands = {
            "help": "help | clear | date | whoami | dir | sysinfo | about | matrix",
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "whoami": self.profile.get("username", "Guest"),
            "dir": "Desktop  Documents  Pictures  Music (dossiers virtuels)",
            "sysinfo": "OS: WINDOWS 12 ULTIMATE (simulé) | Build: 12.0.999 | RAM: 16 GB fictifs | Réseau: hors ligne",
            "about": "Simulateur Python isolé. Aucun accès au shell Windows.",
        }
        if key == "clear":
            write("\0clear")
            write("WINDOWS 12 ULTIMATE // TERMINAL DE SIMULATION")
        elif key == "matrix":
            self.start_effect("matrix")
            write("Matrix activée. Utilisez le bouton Arrêter.")
        else:
            write(commands.get(key, "Commande inconnue. Tapez help."))

    def open_effects(self) -> None:
        _, body = self._window("effects", "Glitch Lab", "650x560")
        for child in body.winfo_children():
            child.destroy()
        self._label(body, "LABORATOIRE GLITCH", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        self._label(body, f"{len(EFFECTS)} effets simulés • bouton Arrêter toujours disponible", fg=self.colors["muted"]).pack(anchor="w", pady=(2, 8))
        search = self._entry(body)
        search.insert(0, "Filtrer les effets…")
        search.pack(fill="x", pady=(0, 8), ipady=6)
        search.bind("<FocusIn>", lambda event: search.delete(0, "end") if search.get().startswith("Filtrer") else None)
        area = tk.Frame(body, bg=self.colors["bg"])
        area.pack(fill="both", expand=True)
        canvas = tk.Canvas(area, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(area, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        grid = tk.Frame(canvas, bg=self.colors["bg"])
        canvas_window = canvas.create_window((0, 0), window=grid, anchor="nw")
        grid.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(canvas_window, width=event.width))

        def populate(filter_text: str = "") -> None:
            for child in grid.winfo_children():
                child.destroy()
            filtered = [(effect_id, label, family) for effect_id, label, family in EFFECTS if filter_text.lower() in label.lower() or filter_text.lower() in effect_id.lower()]
            for index, (effect_id, label, _) in enumerate(filtered):
                self._button(grid, label, lambda name=effect_id: self.start_effect(name), padx=6, pady=6).grid(row=index // 3, column=index % 3, sticky="ew", padx=3, pady=3)
            for column in range(3):
                grid.columnconfigure(column, weight=1)
            canvas.configure(scrollregion=canvas.bbox("all"))

        search.bind("<KeyRelease>", lambda event: populate(search.get()))
        populate()

    def handle_secret(self, command: str) -> bool:
        normalized = re.sub(r"\s+", " ", command.strip().lower())
        secret = SECRET_COMMANDS.get(normalized)
        if not secret:
            return False
        if secret == "profile":
            self.open_profile()
        elif secret == "glitch":
            self.start_effect("glitch")
        elif secret == "matrix":
            self.start_effect("matrix")
        elif secret == "hacker":
            self.hacker_mode = True
            self.profile["hacker_skin"] = True
            self.desktop.itemconfigure("banner", text="H A C K E R")
            self.user_badge.configure(fg="#71ff9f")
            self.save_state()
            self._notice("HACKER MODE DÉBLOQUÉ")
        elif secret == "system":
            self._info_window("system", "SYSTEM UNLOCK", "WINDOWS 12 ULTIMATE • Build fictif 12.0.999\nSimulation isolée • aucun accès système")
        elif secret == "ghost":
            self.open_horror()
        elif secret == "windows":
            self._info_window("about", "WINDOWS 12", "Bienvenue dans le futur.\nWINDOWS 12 ULTIMATE — simulateur Python.")
        return True

    def _info_window(self, key: str, title: str, text: str) -> None:
        _, body = self._window(key, title, "440x260")
        for child in body.winfo_children():
            child.destroy()
        self._label(body, text, justify="left").pack(anchor="w", pady=22)

    def _notice(self, text: str) -> None:
        notice = tk.Label(self.root, text=text, bg="#172a3d", fg="#ffffff", padx=14, pady=9, font=("Segoe UI", 10, "bold"))
        notice.place(relx=.5, rely=.12, anchor="n")
        self.root.after(2200, lambda: notice.destroy() if notice.winfo_exists() else None)

    def start_effect(self, effect_id: str) -> None:
        self.stop_effect()
        overlay = tk.Frame(self.root, bg="#05070c")
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        overlay.lift()
        self.effect_overlay = overlay
        self.effect_active = effect_id
        canvas = tk.Canvas(overlay, bg="#05070c", highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        stop = tk.Button(overlay, text="ARRÊTER L’EFFET", command=self.stop_effect, bg="#ff405a", fg="#ffffff", activebackground="#ff7587", bd=0, padx=16, pady=10, font=("Segoe UI", 10, "bold"), cursor="hand2")
        stop.place(relx=.5, rely=.93, anchor="center")
        if effect_id == "bsod":
            canvas.configure(bg="#0875cc")
            canvas.create_text(90, 75, text=":(", fill="white", font=("Segoe UI", 52), anchor="nw")
            canvas.create_text(95, 175, text="Erreur simulée uniquement.\nAucun problème réel n’est survenu.\nCliquez sur ARRÊTER L’EFFET pour revenir.", fill="white", font=("Segoe UI", 15), anchor="nw", justify="left")
        elif effect_id == "red":
            canvas.configure(bg="#8d0717")
            canvas.create_text(500, 250, text="ALERTE SYSTÈME SIMULÉE", fill="white", font=("Consolas", 25, "bold"))
        elif effect_id == "jumpscare":
            canvas.create_text(500, 250, text="…", fill="#ff334d", font=("Consolas", 34), tags="intro")

        frame = {"n": 0}
        symbols = "01アイウエオカキクケコ#$%&"

        def animate() -> None:
            if not overlay.winfo_exists() or self.effect_active != effect_id:
                return
            frame["n"] += 1
            canvas.delete("moving")
            width, height = max(canvas.winfo_width(), 900), max(canvas.winfo_height(), 600)
            if effect_id == "matrix":
                for _ in range(46):
                    canvas.create_text(random.randrange(width), random.randrange(height), text=random.choice(symbols), fill=random.choice(("#00ff78", "#16b95f", "#83ffc2")), font=("Consolas", random.randint(12, 24)), tags="moving")
                canvas.create_text(width // 2, 75, text="M A T R I X   M O D E", fill="#8affb6", font=("Consolas", 20, "bold"), tags="moving")
            elif effect_id == "glitch":
                for _ in range(20):
                    y = random.randrange(height)
                    x = random.randrange(width)
                    canvas.create_rectangle(x, y, min(width, x + random.randint(25, 300)), y + random.randint(2, 18), fill=random.choice(("#ff1744", "#00e5ff", "#ffffff")), stipple="gray50", outline="", tags="moving")
                canvas.create_text(width // 2, height // 2, text="SIGNAL DISRUPTED", fill="white", font=("Consolas", 24, "bold"), tags="moving")
            elif effect_id == "pixels":
                for _ in range(90):
                    x, y = random.randrange(width), random.randrange(height)
                    canvas.create_rectangle(x, y, x + random.randint(3, 24), y + random.randint(3, 24), fill="black", outline="", tags="moving")
            elif effect_id == "distortion":
                for y in range(0, height, 7):
                    canvas.create_line(0, y + random.randint(-4, 4), width, y + random.randint(-4, 4), fill=random.choice(("#173a53", "#7c2d67", "#15212f")), tags="moving")
                canvas.create_text(width // 2, height // 2, text="VISUAL DISTORTION", fill="#e1f7ff", font=("Consolas", 24, "bold"), tags="moving")
            elif effect_id == "shake":
                overlay.place_configure(x=random.randint(-9, 9), y=random.randint(-7, 7), relwidth=1, relheight=1)
                canvas.create_rectangle(5, 5, width - 5, height - 5, outline="#ff5871", width=3, tags="moving")
            elif effect_id == "jumpscare":
                if frame["n"] > 4:
                    canvas.delete("intro")
                    canvas.create_text(width // 2, height // 2, text="◉      ◉\n\n      ▽", fill="#ff1d40", font=("Consolas", 72, "bold"), tags="moving")
                    canvas.create_text(width // 2, height // 2 + 145, text="SURPRISE • SIMULATION", fill="white", font=("Consolas", 16, "bold"), tags="moving")
            elif effect_id not in {"bsod", "red"}:
                self._draw_variant(canvas, effect_id, width, height, frame["n"])
            if effect_id not in {"bsod", "red"}:
                self.effect_job = self.root.after(100, animate)

        if effect_id not in {"bsod", "red"}:
            self.effect_job = self.root.after(120, animate)

    def _draw_variant(self, canvas: tk.Canvas, effect_id: str, width: int, height: int, frame: int) -> None:
        label, family = EFFECT_DETAILS[effect_id]
        index = EFFECT_INDEX[effect_id]
        colors = ("#ff3158", "#19e6ff", "#9d63ff", "#60ff9e", "#ffe36e", "#f7f8ff")
        symbols = "01アイウエオカキクケコ#$%&"
        speed = 1 + index % 5
        phase = frame * speed
        canvas.create_text(width // 2, 48, text=label.upper(), fill="#f0f7ff", font=("Consolas", 16, "bold"), tags="moving")
        if family == "rgb":
            for row in range(10 + index % 8):
                y = (row * height // 12 + phase * (row % 3 + 1)) % height
                x = random.randrange(max(1, width // 3))
                span = random.randint(width // 8, max(width // 8 + 1, width // 2))
                for offset, color in ((-7, colors[index % 6]), (0, colors[(index + 1) % 6])):
                    canvas.create_rectangle(x + offset, y, min(width, x + span + offset), y + random.randint(3, 20), fill=color, stipple="gray50", outline="", tags="moving")
        elif family == "signal":
            step = 5 + index % 9
            for y in range(0, height, step):
                offset = math.sin((y + phase) / 19) * (4 + index % 15)
                canvas.create_line(offset, y, width - offset, y + math.sin(y / 11) * 4, fill=colors[(y // step + index) % 6], width=1 + (y // step % 2), tags="moving")
            for _ in range(45):
                x, y = random.randrange(width), random.randrange(height)
                canvas.create_line(x, y, min(width, x + random.randint(2, 28)), y, fill=random.choice(colors), tags="moving")
        elif family == "pixels":
            size = 8 + index % 27
            for _ in range(60):
                x = random.randrange(width)
                y = random.randrange(height)
                side = random.choice((size, size * 2, size // 2 + 2))
                color = random.choice(("#05070c", "#ffffff", colors[index % 6], colors[(index + 2) % 6]))
                canvas.create_rectangle(x, y, x + side, y + side, fill=color, stipple="gray50" if index % 2 else "", outline="", tags="moving")
        elif family == "geometry":
            for line in range(6 + index % 8):
                points = []
                y_base = (line + 1) * height / (8 + index % 8)
                for x in range(0, width + 1, 18):
                    y = y_base + math.sin((x + phase * 3 + line * 24) / (20 + index % 31)) * (12 + index % 36)
                    points.extend((x, y))
                canvas.create_line(*points, fill=colors[(line + index) % 6], width=1 + line % 2, smooth=True, tags="moving")
        elif family == "terminal":
            for column in range(26):
                x = column * width // 26
                y = (phase * 3 + column * 41) % height
                text = "\n".join(random.choice(symbols) for _ in range(5 + index % 10))
                canvas.create_text(x, y, text=text, fill=colors[(column + index) % 6], font=("Consolas", 13), anchor="n", tags="moving")
        elif family == "color":
            tint = colors[(index + frame // 8) % 6]
            canvas.configure(bg=tint)
            canvas.create_rectangle(0, 0, width, height, fill=tint, stipple="gray50", outline="", tags="moving")
            for y in range(0, height, 18 + index % 12):
                canvas.create_line(0, y, width, y, fill=colors[(index + y // 18) % 6], tags="moving")
        elif family == "ghost":
            for echo in range(5 + index % 5):
                offset = int(math.sin((frame + echo * 13) / 5) * (8 + index % 19))
                canvas.create_text(width // 2 + offset, height // 2 + echo * 8, text="◉      ◉\n      ▽", fill=colors[(echo + index) % 6], font=("Consolas", 43 + index % 20, "bold"), tags="moving")
            for _ in range(12):
                x, y = random.randrange(width), random.randrange(height)
                canvas.create_oval(x, y, x + 45, y + 45, outline=random.choice(colors), width=2, tags="moving")
        elif family == "bars":
            for bar in range(24):
                position = (bar * 37 + phase * 4) % (width if index % 2 else height)
                if index % 2:
                    canvas.create_rectangle(position, 0, position + 5 + index % 13, height, fill=colors[(bar + index) % 6], stipple="gray50", outline="", tags="moving")
                else:
                    canvas.create_rectangle(0, position, width, position + 3 + index % 11, fill=colors[(bar + index) % 6], stipple="gray50", outline="", tags="moving")
        elif family == "interference":
            for _ in range(160):
                x, y = random.randrange(width), random.randrange(height)
                length = random.randint(1, 5 + index % 20)
                canvas.create_rectangle(x, y, x + length, y + 1 + index % 3, fill=random.choice(colors), outline="", tags="moving")
            for y in range(0, height, 13):
                canvas.create_line(0, y + (phase % 13), width, y + (phase % 13), fill="#263346", tags="moving")
        elif family == "special":
            cx, cy = width // 2, height // 2
            if index % 3 == 0:
                for ray in range(36):
                    angle = (ray + phase / 8) * math.tau / 36
                    radius = max(width, height)
                    canvas.create_line(cx, cy, cx + math.cos(angle) * radius, cy + math.sin(angle) * radius, fill=colors[(ray + index) % 6], tags="moving")
            elif index % 3 == 1:
                y = (phase * 4) % height
                canvas.create_rectangle(0, y, width, min(height, y + 70), fill=colors[index % 6], stipple="gray50", outline="", tags="moving")
                canvas.create_line(0, y, width, y, fill="#ffffff", width=3, tags="moving")
            else:
                for ring in range(14):
                    radius = ((ring * 47 + phase * 3) % max(width, height)) // 2
                    canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, outline=colors[(ring + index) % 6], width=2, tags="moving")
            for _ in range(20):
                x, y = random.randrange(width), random.randrange(height)
                canvas.create_polygon(x, y, x + 15, y - 25, x + 60, y + 8, fill=random.choice(colors), stipple="gray50", outline="", tags="moving")

    def stop_effect(self) -> None:
        if self.effect_job:
            try:
                self.root.after_cancel(self.effect_job)
            except tk.TclError:
                pass
        self.effect_job = None
        self.effect_active = None
        if self.effect_overlay and self.effect_overlay.winfo_exists():
            self.effect_overlay.destroy()
        self.effect_overlay = None

    def close(self) -> None:
        self.stop_effect()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    DesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
