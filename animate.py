"""
animate.py — Girl with a Pearl Earring
Smooth breathing wave effect, runs forever until Ctrl-C.
"""

import sys, time, math, signal, shutil
from PIL import Image

Image.MAX_IMAGE_PIXELS = 200_000_000

# ── terminal size ─────────────────────────────────────────────────────────────
TERM_W, _ = shutil.get_terminal_size((120, 40))
WIDTH     = min(TERM_W - 4, 160)
HEIGHT    = int(WIDTH * 0.45)

# ── ANSI ──────────────────────────────────────────────────────────────────────
def fg(r,g,b): return f"\033[38;2;{r};{g};{b}m"
def bg(r,g,b): return f"\033[48;2;{r};{g};{b}m"
RST  = "\033[0m"
BOLD = "\033[1m"
HOME = "\033[H"
HIDE = "\033[?25l"
SHOW = "\033[?25h"

signal.signal(signal.SIGINT, lambda s,f: (
    sys.stdout.write(SHOW + RST + "\n"), sys.exit(0)
))

# ── load ──────────────────────────────────────────────────────────────────────
CHARS = " ·:+*=%@#█"

def brightness(r,g,b):
    return 0.299*r + 0.587*g + 0.114*b

def load():
    img = Image.open("1665_Girl_with_a_Pearl_Earring.jpg").convert("RGB")
    img = img.resize((WIDTH, HEIGHT), Image.LANCZOS)
    px  = [[img.getpixel((x,y)) for x in range(WIDTH)] for y in range(HEIGHT)]
    return px

# ── render one frame ──────────────────────────────────────────────────────────
def frame(pixels, t):
    out = [HOME]
    for y in range(HEIGHT):
        line = "  "
        for x in range(WIDTH):
            # gentle horizontal ripple
            ox = x + int(1.8 * math.sin((y * 0.18) + t))
            ox = max(0, min(WIDTH-1, ox))

            r,g,b = pixels[y][ox]

            # soft brightness pulse — like candlelight
            pulse = 0.92 + 0.08 * math.sin((x * 0.08) + (y * 0.05) + t * 0.9)
            r = min(255, int(r * pulse))
            g = min(255, int(g * pulse))
            b = min(255, int(b * pulse))

            br  = brightness(r,g,b)
            ch  = CHARS[int(br / 255 * (len(CHARS)-1))]
            dr,dg,db = max(0,r-25), max(0,g-25), max(0,b-25)
            line += f"{fg(r,g,b)}{bg(dr,dg,db)}{ch}{RST}"

        out.append(line)

    gold = fg(210,165,65)
    grey = fg(110,110,110)
    out.append(f"\n  {gold}{BOLD}🎨  Girl with a Pearl Earring{RST}  "
               f"{grey}— Johannes Vermeer, c.1665   [Ctrl-C]{RST}")
    return "\n".join(out)

# ── fade in ───────────────────────────────────────────────────────────────────
def fade_in(pixels, steps=30):
    for step in range(steps):
        alpha = step / steps
        out   = [HOME]
        for y in range(HEIGHT):
            line = "  "
            for x in range(WIDTH):
                r,g,b = pixels[y][x]
                r2 = int(r * alpha)
                g2 = int(g * alpha)
                b2 = int(b * alpha)
                br = brightness(r2,g2,b2)
                ch = CHARS[int(br / 255 * (len(CHARS)-1))]
                dr,dg,db = max(0,r2-25), max(0,g2-25), max(0,b2-25)
                line += f"{fg(r2,g2,b2)}{bg(dr,dg,db)}{ch}{RST}"
            out.append(line)
        sys.stdout.write("\n".join(out))
        sys.stdout.flush()
        time.sleep(0.04)

# ── main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sys.stdout.write("\033[2J" + HOME + HIDE)
    sys.stdout.flush()

    # loading
    gold = fg(210,165,65)
    print(f"\n  {gold}{BOLD}loading...{RST}\n")
    pixels = load()

    # fade in
    fade_in(pixels)

    # wave loop
    t = 0.0
    while True:
        t0 = time.time()
        sys.stdout.write(frame(pixels, t))
        sys.stdout.flush()
        t += 0.08
        elapsed = time.time() - t0
        time.sleep(max(0, 0.05 - elapsed))   # ~20 fps
