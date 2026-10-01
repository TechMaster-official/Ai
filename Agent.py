#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ████████╗███████╗ ██████╗██╗  ██╗    ███╗   ███╗ █████╗ ███████╗   ║
║   ╚══██╔══╝██╔════╝██╔════╝██║  ██║    ████╗ ████║██╔══██╗██╔════╝   ║
║      ██║   █████╗  ██║     ███████║    ██╔████╔██║███████║███████╗   ║
║      ██║   ██╔══╝  ██║     ██╔══██║    ██║╚██╔╝██║██╔══██║╚════██║   ║
║      ██║   ███████╗╚██████╗██║  ██║    ██║ ╚═╝ ██║██║  ██║███████║   ║
║      ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ║
║                                                                      ║
║          TERMUX  AI  AGENT  •  3D  EDITION  •  v1.0.0                ║
║                                                                      ║
║   Developer : Tech Master                                            ║
║   Telegram  : https://t.me/tech_master_a2z                           ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

Run:
    python techmaster_ai.py                    # interactive mode
    python techmaster_ai.py -q "hello"         # one-shot
    python techmaster_ai.py --anim donut       # animation only
    python techmaster_ai.py --help
"""

import argparse
import json
import math
import os
import random
import shutil
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

# ══════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════
VERSION  = "1.0.0"
AUTHOR   = "Tech Master"
TELEGRAM = "https://t.me/tech_master_a2z"
API_URL  = "https://deep-ai-api-by-tech-master.vercel.app/api/deep-ai"
TIMEOUT  = 45


# ══════════════════════════════════════════════════════════════════════
#  COLORS
# ══════════════════════════════════════════════════════════════════════
class C:
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    DIM      = "\033[2m"
    ITALIC   = "\033[3m"
    UNDER    = "\033[4m"

    RED      = "\033[31m"
    GREEN    = "\033[32m"
    YELLOW   = "\033[33m"
    BLUE     = "\033[34m"
    MAGENTA  = "\033[35m"
    CYAN     = "\033[36m"
    WHITE    = "\033[37m"

    BRED     = "\033[91m"
    BGREEN   = "\033[92m"
    BYELLOW  = "\033[93m"
    BBLUE    = "\033[94m"
    BMAGENTA = "\033[95m"
    BCYAN    = "\033[96m"
    BWHITE   = "\033[97m"

    @staticmethod
    def fg(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"


NEON_PALETTE = [
    (0, 255, 255), (0, 180, 255), (120, 100, 255),
    (220, 60, 255), (255, 60, 180), (255, 100, 100),
    (255, 200, 0),
]


def gradient_text(text, palette=NEON_PALETTE):
    if not text or not palette:
        return text
    n = len(palette)
    L = max(1, len(text) - 1)
    out = []
    for i, ch in enumerate(text):
        r, g, b = palette[i * (n - 1) // L]
        out.append(f"\033[38;2;{r};{g};{b}m{ch}")
    return "".join(out) + C.RESET


# ══════════════════════════════════════════════════════════════════════
#  TERMINAL HELPERS
# ══════════════════════════════════════════════════════════════════════
def term_size():
    try:
        s = shutil.get_terminal_size((80, 24))
        return s.columns, s.lines
    except Exception:
        return 80, 24


def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def display_width(s):
    w = 0
    esc = False
    for ch in s:
        if ch == "\033":
            esc = True
            continue
        if esc:
            if ch.isalpha():
                esc = False
            continue
        if unicodedata.combining(ch):
            continue
        ea = unicodedata.east_asian_width(ch)
        w += 2 if ea in ("W", "F") else 1
    return w


def wrap_text(text, width):
    if width < 4:
        width = 4
    out = []
    for para in text.split("\n"):
        if not para:
            out.append("")
            continue
        words = para.split(" ")
        line = ""
        for w in words:
            while display_width(w) > width:
                if line:
                    out.append(line)
                    line = ""
                out.append(w[:width])
                w = w[width:]
            if not line:
                line = w
            elif display_width(line) + 1 + display_width(w) <= width:
                line += " " + w
            else:
                out.append(line)
                line = w
        out.append(line)
    return out


# ══════════════════════════════════════════════════════════════════════
#  UI PRIMITIVES
# ══════════════════════════════════════════════════════════════════════
BANNER = r"""
 ████████╗███████╗ ██████╗██╗  ██╗    ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗
 ╚══██╔══╝██╔════╝██╔════╝██║  ██║    ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
    ██║   █████╗  ██║     ███████║    ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝
    ██║   ██╔══╝  ██║     ██╔══██║    ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
    ██║   ███████╗╚██████╗██║  ██║    ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║
    ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
"""


def print_banner():
    cols, _ = term_size()
    print()
    for line in BANNER.strip("\n").split("\n"):
        if not line.strip():
            continue
        if cols >= 90:
            print(gradient_text(line))
        else:
            print(f"{C.BCYAN}{line}{C.RESET}")
    print()


def print_tagline():
    cols, _ = term_size()
    t1 = f"{C.BCYAN}Termux AI Agent  •  3D Edition  •  Deep AI Powered{C.RESET}"
    t2 = f"{C.BMAGENTA}Developer: Tech Master  •  t.me/tech_master_a2z{C.RESET}"
    for t in (t1, t2):
        pad = max(0, (cols - display_width(t)) // 2)
        print(" " * pad + t)
    print()


def rule(char="─", color=C.BCYAN):
    cols, _ = term_size()
    print(f"{color}{char * cols}{C.RESET}")


def box(title, body, border_color=C.BCYAN, title_color=C.BYELLOW,
        max_width=None, pad=1):
    cols, _ = term_size()
    if max_width is None:
        max_width = min(cols - 2, 100)
    if max_width < 14:
        max_width = 14

    inner = max_width - 2 - 2 * pad
    if inner < 1:
        inner = 1

    body_lines = []
    for raw in body.split("\n"):
        if not raw:
            body_lines.append("")
            continue
        for w in wrap_text(raw, inner):
            body_lines.append(w)

    title_str = f" {title} " if title else ""
    N = max_width - 3 - display_width(title_str)
    if N < 0:
        title_str = title_str[: max(0, max_width - 5)]
        N = max(0, max_width - 3 - display_width(title_str))

    out = [
        f"{border_color}╭─{title_color}{C.BOLD}{title_str}{C.RESET}"
        f"{border_color}{'─' * N}╮{C.RESET}"
    ]
    for line in body_lines:
        v = display_width(line)
        fill = max(0, inner - v)
        out.append(
            f"{border_color}│{C.RESET}"
            f"{' ' * pad}{line}{' ' * fill}{' ' * pad}"
            f"{border_color}│{C.RESET}"
        )
    out.append(f"{border_color}╰{'─' * (max_width - 2)}╯{C.RESET}")
    return "\n".join(out)


def spinner_ask(query):
    """Show animated spinner while calling API."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    label = f"{C.BMAGENTA}⚡ AI is thinking{C.RESET}"

    result = {"ans": None, "err": None}
    import threading

    def worker():
        try:
            result["ans"] = DeepAI.ask(query)
        except Exception as e:
            result["err"] = str(e)

    t = threading.Thread(target=worker, daemon=True)
    t.start()

    i = 0
    start = time.time()
    try:
        while t.is_alive():
            frame = frames[i % len(frames)]
            elapsed = time.time() - start
            sys.stdout.write(f"\r  {C.BCYAN}{frame}{C.RESET}  {label}  "
                             f"{C.DIM}{elapsed:.1f}s{C.RESET}   ")
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1
    finally:
        sys.stdout.write("\r" + " " * 70 + "\r")
        sys.stdout.flush()

    return result["ans"], result["err"], time.time() - start


# ══════════════════════════════════════════════════════════════════════
#  API CLIENT
# ══════════════════════════════════════════════════════════════════════
class APIError(Exception):
    pass


class DeepAI:
    base = API_URL
    timeout = TIMEOUT

    @classmethod
    def ask(cls, query):
        if not query or not query.strip():
            raise APIError("Empty query")
        url = f"{cls.base}?query={urllib.parse.quote_plus(query.strip())}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": f"TechMaster-AI/{VERSION}",
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=cls.timeout) as r:
                raw = r.read().decode("utf-8", errors="replace")
        except Exception as e:
            raise APIError(f"Network error: {e}")

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            raise APIError(f"Invalid JSON: {raw[:200]}")

        if not data.get("status", False):
            raise APIError("API returned status=false")

        res = data.get("results")
        if res is None:
            raise APIError("Missing 'results' field")
        if isinstance(res, (dict, list)):
            res = json.dumps(res, indent=2, ensure_ascii=False)
        return str(res)


# ══════════════════════════════════════════════════════════════════════
#  ANIMATIONS
# ══════════════════════════════════════════════════════════════════════
def _anim_setup():
    sys.stdout.write("\033[?25l\033[2J\033[H")
    sys.stdout.flush()


def _anim_teardown():
    sys.stdout.write(C.RESET + "\033[2J\033[H")
    show_cursor()


def _draw_line(canvas, x1, y1, x2, y2, ch="#"):
    H = len(canvas)
    W = len(canvas[0]) if H else 0
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        if 0 <= y1 < H and 0 <= x1 < W:
            canvas[y1][x1] = ch
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


# ── DONUT ─────────────────────────────────────────────────────────
_DONUT_CHARS = ".,-~:;=!*#$@"
_DONUT_PAL = [196, 202, 208, 214, 220, 226, 190, 154, 118, 82, 46, 51]


def anim_donut(duration=8.0, fps=24):
    W, H = 80, 24
    A = B = 0.0
    dt = 1.0 / fps
    t0 = time.time()
    _anim_setup()
    try:
        while time.time() - t0 < duration:
            zbuf = [0.0] * (W * H)
            buf = [" "] * (W * H)
            o_buf = [0] * (W * H)
            A += 0.09
            B += 0.045
            for j in range(0, 628, 7):
                for i in range(0, 628, 2):
                    c = math.sin(i / 100)
                    d = math.cos(j / 100)
                    e = math.sin(A)
                    f = math.sin(j / 100)
                    g = math.cos(A)
                    h = d + 2
                    D = 1 / (c * h * e + f * g + 5)
                    l = math.cos(i / 100)
                    m = math.cos(B)
                    n = math.sin(B)
                    t = c * h * g - f * e
                    x = int(W / 2 + 30 * D * (l * h * m - t * n))
                    y = int(H / 2 + 15 * D * (l * h * n + t * m))
                    o = int(8 + 8 * (f * e - c * d * g))
                    if 0 <= x < W and 0 <= y < H:
                        idx = y * W + x
                        if D > zbuf[idx]:
                            zbuf[idx] = D
                            buf[idx] = _DONUT_CHARS[max(0, min(11, o))]
                            o_buf[idx] = max(0, min(11, o))
            out = ["\033[H"]
            for row in range(H):
                last = -1
                parts = []
                for col in range(W):
                    ch = buf[row * W + col]
                    if ch == " ":
                        parts.append(" ")
                        last = -1
                        continue
                    o = o_buf[row * W + col]
                    if o != last:
                        parts.append(f"\033[38;5;{_DONUT_PAL[o]}m")
                        last = o
                    parts.append(ch)
                out.append("".join(parts) + C.RESET + "\n")
            sys.stdout.write("".join(out))
            sys.stdout.flush()
            time.sleep(dt)
    finally:
        _anim_teardown()


# ── CUBE ──────────────────────────────────────────────────────────
def _rot(p, ax, ay, az):
    x, y, z = p
    cx, sx = math.cos(ax), math.sin(ax)
    y, z = y * cx - z * sx, y * sx + z * cx
    cy, sy = math.cos(ay), math.sin(ay)
    x, z = x * cy + z * sy, -x * sy + z * cy
    cz, sz = math.cos(az), math.sin(az)
    x, y = x * cz - y * sz, x * sz + y * cz
    return x, y, z


def anim_cube(duration=8.0, fps=24):
    W, H = 64, 30
    verts = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
             (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0),
             (4, 5), (5, 6), (6, 7), (7, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)]
    ax = ay = az = 0.0
    dt = 1.0 / fps
    t0 = time.time()
    _anim_setup()
    try:
        while time.time() - t0 < duration:
            ax += 0.035
            ay += 0.052
            az += 0.024
            canvas = [[" "] * W for _ in range(H)]
            proj = []
            for v in verts:
                x, y, z = _rot(v, ax, ay, az)
                d = 3.5
                f = d / (d + z)
                px = int(W / 2 + x * f * 20)
                py = int(H / 2 + y * f * 10)
                proj.append((px, py))
            for a, b in edges:
                _draw_line(canvas, proj[a][0], proj[a][1],
                           proj[b][0], proj[b][1], "█")
            out = ["\033[H"]
            for row in range(H):
                r = int(127 + 127 * math.sin(ay + row * 0.22))
                g = int(127 + 127 * math.sin(ay + 2 + row * 0.13))
                bb = int(127 + 127 * math.sin(ay + 4 + row * 0.17))
                line = "".join(canvas[row])
                out.append(f"\033[38;2;{r};{g};{bb}m{line}{C.RESET}\n")
            sys.stdout.write("".join(out))
            sys.stdout.flush()
            time.sleep(dt)
    finally:
        _anim_teardown()


# ── MATRIX ────────────────────────────────────────────────────────
def anim_matrix(duration=8.0, fps=18):
    cols, rows = term_size()
    W = max(20, min(cols, 140))
    H = max(10, rows - 1)
    drops = [random.randint(-H, 0) for _ in range(W)]
    speeds = [random.choice([1, 1, 1, 2]) for _ in range(W)]
    chars = "アイウエオカキクケコサシスセソタチツテトナニヌネノ0123456789ABCDEF"
    dt = 1.0 / fps
    t0 = time.time()
    _anim_setup()
    try:
        while time.time() - t0 < duration:
            for x in range(W):
                drops[x] += speeds[x]
                if drops[x] - 12 > H:
                    drops[x] = random.randint(-15, 0)
                    speeds[x] = random.choice([1, 1, 1, 2])
            out = ["\033[H"]
            for y in range(H):
                parts = []
                for x in range(W):
                    d = drops[x]
                    if y == d:
                        parts.append(f"\033[1;97m{random.choice(chars)}{C.RESET}")
                    elif 0 < d - y <= 11:
                        shade = 22 + (d - y) * 2
                        parts.append(f"\033[38;5;{shade}m{random.choice(chars)}{C.RESET}")
                    else:
                        parts.append(" ")
                out.append("".join(parts) + "\n")
            sys.stdout.write("".join(out))
            sys.stdout.flush()
            time.sleep(dt)
    finally:
        _anim_teardown()


# ── PLASMA ────────────────────────────────────────────────────────
def anim_plasma(duration=8.0, fps=18):
    cols, rows = term_size()
    W = min(cols, 110)
    H = min(rows - 1, 32)
    chars = " .:-=+*#%@"
    dt = 1.0 / fps
    t0 = time.time()
    tt = 0.0
    _anim_setup()
    try:
        while time.time() - t0 < duration:
            tt += 0.18
            out = ["\033[H"]
            for y in range(H):
                parts = []
                last = None
                for x in range(W):
                    v = (math.sin(x * 0.11 + tt)
                         + math.sin(y * 0.19 - tt)
                         + math.sin((x + y) * 0.09 + tt * 0.7)
                         + math.sin(math.hypot(x - W / 2, y - H / 2) * 0.16 - tt))
                    v = (v + 4) / 8
                    idx = int(v * (len(chars) - 1))
                    ch = chars[idx]
                    r = int(127 + 127 * math.sin(tt + x * 0.05))
                    g = int(127 + 127 * math.sin(tt + 2 + y * 0.06))
                    b = int(127 + 127 * math.sin(tt + 4 + (x + y) * 0.04))
                    key = (r // 32, g // 32, b // 32)
                    if key != last:
                        parts.append(f"\033[38;2;{r};{g};{b}m")
                        last = key
                    parts.append(ch)
                out.append("".join(parts) + C.RESET + "\n")
            sys.stdout.write("".join(out))
            sys.stdout.flush()
            time.sleep(dt)
    finally:
        _anim_teardown()


# ── SPLASH ────────────────────────────────────────────────────────
def splash():
    clear_screen()
    print()
    print_banner()
    print_tagline()
    cols, _ = term_size()
    width = min(52, max(20, cols - 10))
    sys.stdout.write("\n")
    for i in range(width + 1):
        pct = int(i * 100 / width)
        filled = "█" * i
        empty = "░" * (width - i)
        r = int(255 * i / width)
        g = int(255 * (1 - abs(i / width - 0.5) * 2))
        b = int(255 * (1 - i / width))
        bar = (f"\r  {C.BMAGENTA}▸ {C.RESET}"
               f"\033[38;2;{r};{g};{b}m{filled}"
               f"\033[38;5;238m{empty}{C.RESET}"
               f"  {C.BYELLOW}{pct:3d}%{C.RESET}  "
               f"{C.DIM}loading engine...{C.RESET}")
        sys.stdout.write(bar)
        sys.stdout.flush()
        time.sleep(0.012)
    print("\n")
    time.sleep(0.35)


# ══════════════════════════════════════════════════════════════════════
#  AGENT
# ══════════════════════════════════════════════════════════════════════
HELP_TEXT = """Available commands
  /help            show this help
  /anim <name>     play animation : donut | cube | matrix | plasma | all
  /clear           clear the screen
  /banner          print banner again
  /about           about this tool
  /api             show API endpoint
  /history         show current session history
  /save <file>     save chat history to file
  /quit  /exit     exit

Type any question to talk with the AI."""


class Agent:
    def __init__(self, no_splash=False, no_anim=False, api_base=None):
        self.no_splash = no_splash
        self.no_anim = no_anim
        if api_base:
            DeepAI.base = api_base
        self.history = []

    # ── animation dispatcher ──
    def play_animation(self, name):
        if self.no_anim:
            print(f"{C.DIM}animations disabled (--no-anim){C.RESET}")
            return
        name = (name or "donut").lower()
        try:
            if name == "donut":
                anim_donut()
            elif name == "cube":
                anim_cube()
            elif name == "matrix":
                anim_matrix()
            elif name == "plasma":
                anim_plasma()
            elif name == "all":
                anim_donut(4)
                anim_cube(4)
                anim_matrix(4)
                anim_plasma(4)
            else:
                print(f"{C.BRED}Unknown animation: {name}{C.RESET}")
        except KeyboardInterrupt:
            _anim_teardown()

    # ── ask ──
    def ask(self, query):
        ans, err, dt = spinner_ask(query)
        if err:
            return None, err, dt
        self.history.append({"q": query, "a": ans, "t": dt})
        return ans, None, dt

    # ── render answer ──
    def render(self, answer):
        body = (answer or "").strip() or "(empty response)"
        print(box("AI  •  Tech Master", body,
                  border_color=C.BCYAN,
                  title_color=C.BMAGENTA))

    # ── one-shot ──
    def one_shot(self, q):
        ans, err, dt = self.ask(q)
        if err:
            print(f"{C.BRED}✗ {err}{C.RESET}")
            return
        print(f"{C.DIM}⏱  {dt:.2f}s{C.RESET}\n")
        self.render(ans)
        print()

    # ── interactive ──
    def run(self):
        if not self.no_splash and not self.no_anim:
            try:
                splash()
            except Exception:
                pass

        clear_screen()
        print_banner()
        print_tagline()
        rule("═", C.BCYAN)
        print(f"  {C.BGREEN}Type {C.BYELLOW}/help{C.BGREEN} for commands"
              f"  •  {C.BMAGENTA}Ctrl+C{C.BGREEN} to exit{C.RESET}")
        rule("═", C.BCYAN)
        print()

        while True:
            try:
                q = input(f"{C.BGREEN}❯ {C.BCYAN}You {C.BWHITE}›{C.RESET} ").strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n{C.BMAGENTA}⚡ Goodbye — stay awesome!{C.RESET}")
                show_cursor()
                return

            if not q:
                continue

            if q.startswith("/"):
                cmd, _, arg = q.partition(" ")
                cmd = cmd.lower()

                if cmd in ("/quit", "/exit", "/q"):
                    print(f"{C.BMAGENTA}⚡ Goodbye — stay awesome!{C.RESET}")
                    return

                if cmd == "/help":
                    print(box("Help", HELP_TEXT,
                              border_color=C.BMAGENTA,
                              title_color=C.BYELLOW))

                elif cmd == "/clear":
                    clear_screen()
                    print_banner()
                    print_tagline()

                elif cmd == "/banner":
                    print_banner()
                    print_tagline()

                elif cmd == "/about":
                    info = (f"Tech Master AI   v{VERSION}\n"
                            f"Developer : {AUTHOR}\n"
                            f"Telegram  : {TELEGRAM}\n"
                            f"Engine    : 3D Termux Agent\n"
                            f"API       : deep-ai-api-by-tech-master.vercel.app")
                    print(box("About", info,
                              border_color=C.BCYAN,
                              title_color=C.BMAGENTA))

                elif cmd == "/api":
                    print(box("API Endpoint",
                              f"{API_URL}\n\nMethod : GET\n"
                              f"Param  : ?query=<your+question>",
                              border_color=C.BCYAN,
                              title_color=C.BYELLOW))

                elif cmd == "/history":
                    if not self.history:
                        print(f"{C.DIM}No history in this session.{C.RESET}")
                    else:
                        lines = []
                        for i, h in enumerate(self.history, 1):
                            lines.append(f"[{i}] Q: {h['q'][:70]}")
                        print(box("Session History", "\n".join(lines),
                                  border_color=C.BMAGENTA,
                                  title_color=C.BYELLOW))

                elif cmd == "/save":
                    if not arg:
                        print(f"{C.BRED}Usage: /save <filename>{C.RESET}")
                    elif not self.history:
                        print(f"{C.DIM}Nothing to save.{C.RESET}")
                    else:
                        try:
                            with open(arg, "w", encoding="utf-8") as f:
                                for h in self.history:
                                    f.write(f"Q: {h['q']}\n")
                                    f.write(f"A: {h['a']}\n")
                                    f.write("-" * 60 + "\n")
                            print(f"{C.BGREEN}✓ Saved {len(self.history)} "
                                  f"entries to {arg}{C.RESET}")
                        except Exception as e:
                            print(f"{C.BRED}✗ {e}{C.RESET}")

                elif cmd == "/anim":
                    try:
                        self.play_animation(arg or "donut")
                    except Exception as e:
                        print(f"{C.BRED}✗ {e}{C.RESET}")
                    clear_screen()
                    print_banner()
                    print_tagline()

                else:
                    print(f"{C.BRED}Unknown command: {cmd}{C.RESET}")

                print()
                continue

            # ── ask AI ──
            print()
            ans, err, dt = self.ask(q)
            if err:
                print(f"{C.BRED}✗ {err}{C.RESET}\n")
                continue
            print(f"{C.DIM}⏱  {dt:.2f}s{C.RESET}")
            self.render(ans)
            print()


# ══════════════════════════════════════════════════════════════════════
#  CLI
# ══════════════════════════════════════════════════════════════════════
def parse_args():
    p = argparse.ArgumentParser(
        prog="techmaster-ai",
        description="Tech Master AI — Termux AI Agent (3D Edition)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python techmaster_ai.py                     # interactive chat\n"
            "  python techmaster_ai.py -q \"hello\"          # one-shot\n"
            "  python techmaster_ai.py --anim donut        # 3D donut\n"
            "  python techmaster_ai.py --anim all          # all animations\n"
            "  python techmaster_ai.py --no-splash         # skip splash\n"
        ),
    )
    p.add_argument("-q", "--query", help="one-shot question and exit")
    p.add_argument("--no-splash", action="store_true", help="skip splash screen")
    p.add_argument("--no-anim", action="store_true", help="disable animations")
    p.add_argument("--anim",
                   choices=["donut", "cube", "matrix", "plasma", "all"],
                   help="play an animation and exit")
    p.add_argument("--api", help="override API endpoint")
    p.add_argument("--version", action="version",
                   version=f"Tech Master AI v{VERSION}")
    return p.parse_args()


def main():
    args = parse_args()
    agent = Agent(no_splash=args.no_splash,
                  no_anim=args.no_anim,
                  api_base=args.api)

    if args.anim:
        agent.play_animation(args.anim)
        return
    if args.query:
        agent.one_shot(args.query)
        return
    agent.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write(
            "\033[?25h\033[0m\n\033[38;5;213m⚡ Session terminated.\033[0m\n"
        )
        sys.exit(0)
