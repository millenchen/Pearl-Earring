"""
run.py — jalankan file ini untuk melihat ASCII art-nya.

pearl_earring.py adalah "shaped code" — kode yang bentuknya
adalah siluet lukisan. Karena indentasinya sengaja dibentuk
seperti gambar, Python perlu sedikit trik untuk menjalankannya.
"""

import sys, re

# Baca source code pearl_earring.py
with open("pearl_earring.py", "r") as f:
    source = f.read()

# Hapus leading whitespace di tiap baris (yang membentuk "shape"-nya)
# tapi pertahankan indentasi RELATIF antar baris
lines = source.split("\n")

# Cari indentasi minimum (selain baris kosong)
min_indent = float("inf")
for line in lines:
    stripped = line.lstrip()
    if stripped:  # bukan baris kosong
        indent = len(line) - len(stripped)
        min_indent = min(min_indent, indent)

if min_indent == float("inf"):
    min_indent = 0

# Kurangi indentasi minimum dari semua baris
cleaned = "\n".join(
    line[min_indent:] if len(line) >= min_indent else line
    for line in lines
)

# Jalankan kodenya
exec(compile(cleaned, "pearl_earring.py", "exec"))
