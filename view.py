"""
view.py — convert Girl with a Pearl Earring jadi ASCII art berwarna di terminal
"""

import sys, time
from PIL import Image, ImageFile
Image.MAX_IMAGE_PIXELS = 200_000_000  # allow large painting file

# ── config ────────────────────────────────────────────────────────────────────
IMAGE_PATH  = "1665_Girl_with_a_Pearl_Earring.jpg"
WIDTH       = 120       # karakter per baris (sesuaikan sama lebar terminal kamu)
ANIMATE     = True      # fade-in baris per baris
DELAY       = 0.015     # detik per baris

# Karakter dari gelap ke terang — makin terang pixel, makin "padat" karakternya
CHARS = " ·:+*=%@#█"

# ── helpers ───────────────────────────────────────────────────────────────────
def ansi_fg(r, g, b):  return f"\033[38;2;{r};{g};{b}m"
def ansi_bg(r, g, b):  return f"\033[48;2;{r};{g};{b}m"
def reset():           return "\033[0m"
def clear():           sys.stdout.write("\033[2J\033[H"); sys.stdout.flush()

def brightness(r, g, b):
    # persepsi manusia: hijau paling terang, biru paling gelap
    return 0.299*r + 0.587*g + 0.114*b

# ── load & resize ─────────────────────────────────────────────────────────────
def load_image(path, width):
    img = Image.open(path).convert("RGB")
    # terminal font tingginya ~2x lebarnya, jadi height dikali 0.45
    aspect = img.height / img.width
    height = int(width * aspect * 0.45)
    img = img.resize((width, height), Image.LANCZOS)
    return img

# ── render ────────────────────────────────────────────────────────────────────
def render(img):
    rows = []
    pixels = img.load()
    for y in range(img.height):
        line = ""
        for x in range(img.width):
            r, g, b = pixels[x, y]
            bright  = brightness(r, g, b)
            # pilih karakter berdasarkan kecerahan
            char_idx = int(bright / 255 * (len(CHARS) - 1))
            char     = CHARS[char_idx]
            # warna foreground = warna pixel asli, background = sedikit lebih gelap
            dr, dg, db = max(0, r-40), max(0, g-40), max(0, b-40)
            line += f"{ansi_fg(r,g,b)}{ansi_bg(dr,dg,db)}{char}{reset()}"
        rows.append(line)
    return rows

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    clear()

    # title
    gold  = ansi_fg(220, 175, 70)
    grey  = ansi_fg(160, 160, 160)
    bold  = "\033[1m"
    rst   = reset()
    print(f"\n{gold}{bold}  🎨  Girl with a Pearl Earring  —  Johannes Vermeer, c. 1665{rst}\n")

    print(f"{grey}  loading...{rst}", end="\r")
    img  = load_image(IMAGE_PATH, WIDTH)
    rows = render(img)
    print(" " * 20, end="\r")  # hapus "loading..."

    for row in rows:
        print("  " + row)
        if ANIMATE:
            time.sleep(DELAY)

    print(f"\n{grey}  {IMAGE_PATH}  •  {img.width}×{img.height} chars  •  pure python + pillow{rst}\n")

if __name__ == "__main__":
    main()
