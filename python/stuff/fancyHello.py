#!/usr/bin/env python3
# Fancy "HELLO WORLD" Terminal Art (no external libs)
import sys, time, math, os, random, shutil

MSG = "HELLO WORLD"
DURATION = 6.0        # Sekunden für die Hauptanimation
FPS = 35              # Ziel-FPS
WAVE_H = 3            # Wellenhöhe in Zeilen
SPARKLES = 28         # Anzahl gleichzeitiger Funken
GHOST_TRAIL = 0.55    # 0..1 Nachleuchten
REFLECTION_OFFSET = 2 # Zeilen unter dem Text
FINALE = True         # Am Ende ein Banner + Feuerwerk

# --- ANSI helpers -------------------------------------------------------------
CSI = "\033["
RESET = "\033[0m"
HIDE = "\033[?25l"
SHOW = "\033[?25h"
CLEAR = "\033[2J"
ERASE = "\033[0m"

def goto(y, x):  # 1-based terminal coords
    return f"{CSI}{max(1,y)};{max(1,x)}H"

def rgb256(i):
    # i in [16..231] ist 6x6x6 Farbraum; wir mappen sinusförmig hinein
    i = max(16, min(231, int(i)))
    return f"{CSI}38;5;{i}m"

def dim():   return f"{CSI}2m"
def bold():  return f"{CSI}1m"
def italic():return f"{CSI}3m"  # wird nicht überall unterstützt
def invert():return f"{CSI}7m"

def enable_ansi_on_windows():
    # Windows 10+: os.system("") triggert ANSI-Support in vielen Terminals
    if os.name == "nt":
        os.system("")

# --- Layout helpers -----------------------------------------------------------
def term_size():
    try:
        size = shutil.get_terminal_size()
        return size.lines, size.columns
    except:
        return 24, 80

def center_coords(lines, cols, width):
    y = lines // 2
    x = (cols - width) // 2 + 1
    return y, x

# --- Funken (Sparkles) --------------------------------------------------------
class Sparkle:
    def __init__(self, lines, cols):
        self.lines, self.cols = lines, cols
        self.reset()

    def reset(self):
        self.y = random.randint(2, self.lines-2)
        self.x = random.randint(3, self.cols-3)
        self.life = random.uniform(0.2, 0.8)
        self.t0 = time.perf_counter()
        self.ch = random.choice(["·","•","*","✦","✧","⁕","˚","᛫","·"])
        self.hue = random.randint(16, 231)

    def alive(self, t):
        return (t - self.t0) < self.life

    def draw(self, t):
        fade = 1.0 - (t - self.t0)/self.life
        if fade <= 0:
            self.reset()
            return ""
        c = int(self.hue * 0.6 + 16)
        style = dim() if fade < 0.5 else ""
        return goto(int(self.y), int(self.x)) + rgb256(c) + style + self.ch + RESET

# --- Haupt-Animation ----------------------------------------------------------
def animate():
    enable_ansi_on_windows()
    lines, cols = term_size()
    msg = MSG
    width = len(msg)
    base_y, base_x = center_coords(lines, cols, width)

    # pre-create sparkles
    sparkles = [Sparkle(lines, cols) for _ in range(SPARKLES)]

    # Cursor verstecken & Bildschirm leeren
    sys.stdout.write(HIDE + CLEAR)
    sys.stdout.flush()

    t0 = time.perf_counter()
    frame_time = 1.0 / FPS
    try:
        while True:
            now = time.perf_counter()
            t = now - t0
            if t > DURATION: break

            # sanftes Clear (nur löschen, was wir überschreiben)
            sys.stdout.write(CSI + "0m")  # reset styles
            # Hauptrender
            for i, ch in enumerate(msg):
                # Wellenbewegung pro Zeichen
                y = base_y + int(math.sin(t*2.0 + i*0.8) * WAVE_H)
                # horizontaler "Schwung"
                x = base_x + i + int(math.sin(t*0.7 + i*0.3) * 2)

                # Regenbogen-Farben
                hue = 16 + (math.sin(t*1.6 + i*0.75)+1)/2 * 215  # 16..231
                # Glitch / Ghost-Trail
                ghost = (math.sin(t*4 + i)*0.5 + 0.5) * GHOST_TRAIL
                hue_ghost = max(16, min(231, hue*0.75+40))

                # abwechselnd Groß/Klein in Bewegung
                show_ch = ch.swapcase() if (int(t*10)+i)%2==0 else ch

                # leichte Zufallsverzerrung
                if random.random() < 0.015:
                    show_ch = random.choice(["#", "░", "▒", "▓", "Ø", "@", "§", "¤"])

                # Hauptzeichen
                sys.stdout.write(goto(y, x) + rgb256(hue) + bold() + show_ch + RESET)

                # Ghost-Trail (Nachleuchten)
                if ghost > 0.08:
                    gy = y + 1
                    sys.stdout.write(goto(gy, x) + rgb256(hue_ghost) + dim() + show_ch + RESET)

                # Spiegelung (Reflexion unten, gedimmt & invertiertes Case)
                ry = y + REFLECTION_OFFSET
                if 2 <= ry <= lines-1:
                    ref_ch = ch.lower() if ch != " " else " "
                    fade = max(0.0, 1.0 - (ry - y) * 0.35)
                    if fade > 0.1:
                        shade = int(232 + (1.0-fade)*20)  # Graustufen 232..252
                        sys.stdout.write(goto(ry, x) + f"{CSI}38;5;{shade}m" + dim() + ref_ch + RESET)

            # Sparkles
            for s in sparkles:
                sys.stdout.write(s.draw(time.perf_counter()))

            sys.stdout.flush()
            # Frame-Pacing
            slept = time.perf_counter() - now
            if slept < frame_time:
                time.sleep(frame_time - slept)

        # Finale: Banner + Mini-Feuerwerk
        if FINALE:
            banner(MSG, lines, cols)
            fireworks(lines, cols, 1.6)

    finally:
        sys.stdout.write(RESET + SHOW + goto(lines, 1) + "\n")
        sys.stdout.flush()

# --- Finale Effekte -----------------------------------------------------------
def banner(text, lines, cols):
    w = len(text) + 12
    h = 7
    y0 = max(2, lines//2 - h//2)
    x0 = max(2, (cols - w)//2)
    top = "╭" + "─"* (w-2) + "╮"
    mid = "│" + " "*(w-2) + "│"
    bot = "╰" + "─"* (w-2) + "╯"

    # Rahmen
    sys.stdout.write(rgb256(51) + bold())
    sys.stdout.write(goto(y0,   x0) + top)
    for i in range(1, h-1):
        sys.stdout.write(goto(y0+i, x0) + mid)
    sys.stdout.write(goto(y0+h-1, x0) + bot + RESET)

    # Text mit Regenbogenverlauf
    tx = x0 + (w - len(text))//2
    ty = y0 + h//2
    for i,ch in enumerate(text):
        hue = 16 + (i/ max(1,len(text)-1)) * 215
        sys.stdout.write(goto(ty, tx+i) + rgb256(hue) + bold() + ch + RESET)
    sys.stdout.flush()
    time.sleep(0.6)

def fireworks(lines, cols, seconds=1.5):
    t0 = time.perf_counter()
    bursts = []
    while time.perf_counter() - t0 < seconds:
        # neue Explosionen hinzufügen
        if random.random() < 0.3:
            y = random.randint(3, max(3, lines-6))
            x = random.randint(6, max(6, cols-6))
            color = random.randint(16, 231)
            bursts.append((y, x, color, time.perf_counter()))
        # zeichnen
        for (y,x,color,tb) in bursts:
            phase = time.perf_counter() - tb
            r = int(phase * 8)
            if r > 5: continue
            for a in range(0, 360, 30):
                rad = math.radians(a)
                yy = int(y + math.sin(rad)*r)
                xx = int(x + math.cos(rad)*r)
                if 2 <= yy <= lines-1 and 2 <= xx <= cols-1:
                    sys.stdout.write(goto(yy, xx) + rgb256(color) + ("*" if r%2==0 else "·") + RESET)
        sys.stdout.flush()
        time.sleep(1/45)

# --- run ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        animate()
    except KeyboardInterrupt:
        pass
