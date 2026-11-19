#!/usr/bin/env python3.13
# make.fun entry: news-image-20261119  (style seed: ai-stack188)
# Deterministic 1024x768 newspaper front page PNG. stdlib only (zlib, struct).
import os, zlib, struct, random

W, H = 1024, 768
SEED = "ai-stack188"
rng = random.Random(SEED)

# ------------------------------------------------------------------ 5x7 font
# Each glyph: list of 7 in(5-bit rows), bit 4 = leftmost pixel.
def _g(s):
    return [int(r, 2) for r in s.split()]

_GLYPHS = {
'A': '01110 10001 10001 11111 10001 10001 10001',
'B': '11110 10001 11110 10001 10001 10001 11110',
'C': '01111 10000 10000 10000 10000 10000 01111',
'D': '11110 10001 10001 10001 10001 10001 11110',
'E': '11111 10000 11110 10000 10000 10000 11111',
'F': '11111 10000 11110 10000 10000 10000 10000',
'G': '01111 10000 10000 10111 10001 10001 01110',
'H': '10001 10001 11111 10001 10001 10001 10001',
'I': '11111 00100 00100 00100 00100 00100 11111',
'J': '00111 00010 00010 00010 00010 10010 01100',
'K': '10001 10010 11100 10010 10001 10001 10001',
'L': '10000 10000 10000 10000 10000 10000 11111',
'M': '10001 11011 10101 10101 10001 10001 10001',
'N': '10001 11001 10101 10011 10001 10001 10001',
'O': '01110 10001 10001 10001 10001 10001 01110',
'P': '11110 10001 10001 11110 10000 10000 10000',
'Q': '01110 10001 10001 10001 10101 10010 01101',
'R': '11110 10001 10001 11110 10010 10001 10001',
'S': '01111 10000 10000 01110 00001 00001 11110',
'T': '11111 00100 00100 00100 00100 00100 00100',
'U': '10001 10001 10001 10001 10001 10001 01110',
'V': '10001 10001 10001 10001 10001 01010 00100',
'W': '10001 10001 10001 10101 10101 11011 10001',
'X': '10001 01010 00100 00100 01010 10001 10001',
'Y': '10001 01010 00100 00100 00100 00100 00100',
'Z': '11111 00001 00010 00100 01000 10000 11111',
'0': '01110 10001 10011 10101 11001 10001 01110',
'1': '00100 01100 00100 00100 00100 00100 01110',
'2': '01110 10001 00001 00110 01000 10000 11111',
'3': '11110 00001 00001 01110 00001 00001 11110',
'4': '00010 00110 01010 10010 11111 00010 00010',
'5': '11111 10000 11110 00001 00001 10001 01110',
'6': '00110 01000 10000 11110 10001 10001 01110',
'7': '11111 00001 00010 00100 01000 01000 01000',
'8': '01110 10001 10001 01110 10001 10001 01110',
'9': '01110 10001 10001 01111 00001 00010 01100',
'.': '00000 00000 00000 00000 00000 00110 00110',
',': '00000 00000 00000 00000 00110 00110 01000',
'!': '00100 00100 00100 00100 00100 00000 00100',
'?': '01110 10001 00001 00110 00100 00000 00100',
"'": '00100 00100 01000 00000 00000 00000 00000',
'"': '01010 01010 00000 00000 00000 00000 00000',
'-': '00000 00000 00000 11111 00000 00000 00000',
':': '00000 00110 00110 00000 00110 00110 00000',
';': '00000 00110 00110 00000 00110 00110 01000',
'/': '00001 00010 00010 00100 01000 01000 10000',
'%': '11001 11010 00010 00100 01000 01011 10011',
'(': '00010 00100 01000 01000 01000 00100 00010',
')': '01000 00100 00010 00010 00010 00100 01000',
'+': '00000 00100 00100 11111 00100 00100 00000',
'=': '00000 00000 11111 00000 11111 00000 00000',
'$': '00100 01111 10100 01110 00101 11110 00100',
'&': '01100 10010 10100 01000 10101 10010 01101',
'#': '01010 11111 01010 01010 01010 11111 01010',
'*': '00000 10101 01110 11111 01110 10101 00000',
'@': '01110 10001 10111 10101 10111 10000 01110',
'>': '01000 00100 00010 00001 00010 00100 01000',
'<': '00010 00100 01000 10000 01000 00100 00010',
'|': '00100 00100 00100 00100 00100 00100 00100',
'_': '00000 00000 00000 00000 00000 00000 11111',
}
FONT = {ch: _g(p) for ch, p in _GLYPHS.items()}
FONT[' '] = [0]*7

SW, SH = 5, 7          # glyph cell

def draw_char(buf, ch, x, y, color, scale=1):
    rows = FONT.get(ch.upper(), FONT['?'])
    for ry, bit in enumerate(rows):
        for rx in range(SW):
            if bit & (1 << (SW-1-rx)):
                for sy in range(scale):
                    yy = y + ry*scale + sy
                    if 0 <= yy < H:
                        base = (yy*W + x + rx*scale)*3
                        for sx in range(scale):
                            xx = x + rx*scale + sx
                            if 0 <= xx < W:
                                buf[base:base+3] = color

def text_w(s, scale=1):
    return len(s) * (SW+1) * scale

def draw_text(buf, s, x, y, color, scale=1):
    for ch in s:
        draw_char(buf, ch, x, y, color, scale)
        x += (SW+1)*scale
    return x

def draw_text_center(buf, s, y, color, scale=1, x0=0, x1=W):
    w = text_w(s, scale)
    draw_text(buf, s, x0 + max(0,(x1-x0-w)//2), y, color, scale)

# ------------------------------------------------------------------ raster ops
def rect(buf, x0, y0, x1, y1, color):
    x0=max(0,x0); y0=max(0,y0); x1=min(W,x1); y1=min(H,y1)
    row = bytes(color)*(x1-x0)
    for y in range(y0, y1):
        o = y*W*3
        buf[o+x0*3:o+x1*3] = row

def rect_outline(buf, x0, y0, x1, y1, color, t=1):
    rect(buf, x0, y0, x1, y0+t, color)
    rect(buf, x0, y1-t, x1, y1, color)
    rect(buf, x0, y0, x0+t, y1, color)
    rect(buf, x1-t, y0, x1, y1, color)

# ------------------------------------------------------------------ palette (seeded)
def _hue(h):
    import colorsys
    r,g,b = colorsys.hsv_to_rgb(h, 0.45, 0.92)
    return int(r*255), int(g*255), int(b*255)

ACCENT   = _hue(0.05 + rng.random()*0.06)     # masthead red/orange family
ACCENT2  = _hue(0.55 + rng.random()*0.08)     # kicker blue family
INK      = (24, 24, 28)
PAPER    = (246, 243, 235)
PAPER2   = (238, 234, 224)
GREY     = (110, 110, 118)

# ------------------------------------------------------------------ content
DATELINE = 'WORLD NEWS - Thursday 19 November 2026'

# Big banner headline for the day's top story
BANNER_HEAD = 'MARS GATEWAY OPENS: FIRST 1,000 PIONEERS TOUCH DOWN'
BANNER_SUB  = "Settlement programme milestone as world leaders hail 'a giant leap for cooperation'"

# ticker strip (deterministic values)
TICKER = ('MARKETS  DOW +0.4%  FTSE -0.2%  NIKKEI +0.9%     '
          'WEATHER  LONDON 8C RAIN  TOKYO 14C CLEAR  NEW YORK 11C SUNNY')

# secondary stories: kicker, headline, body
STORIES = [
 ("GAMING",
  "GTA VI LAUNCH: STORES SELL OUT WORLDWIDE AS GAMERS QUEUE FOR MIDNIGHT OPENINGS",
  "Rockstar's long-awaited sequel hit consoles at midnight; first-week sales are on pace to break every record in entertainment history."),
 ("MARKETS",
  "FED MINUTES SIGNAL SLOWER RATE PATH; STOCKS END MIXED",
  "Dow and Nikkei edge higher while the FTSE slips; traders weigh fresh inflation data as bond yields ease for a third straight session."),
 ("COPENHAGEN",
  "CLIMATE SUMMIT ADOPTS CLEAN-GRID PLEDGE AS FOSSIL ROW SIMMERS",
  "Delegates agree to triple clean-power capacity by 2035; talks on a coal and oil phase-out run past the deadline and into the night."),
 ("SPORT",
  "CHAMPIONS LEAGUE: 94TH-MINUTE WINNER SENDS UNDERDOGS THROUGH",
  "A stoppage-time header caps a stunning comeback night across Europe as the group standings are rewritten in the final minutes."),
]

def fit_text(buf, s, x, y, color, scale, max_w, max_lines, line_h):
    words = s.split()
    lines, cur = [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if text_w(t, scale) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur: lines.append(cur)
    lines = lines[:max_lines]
    for i, ln in enumerate(lines):
        draw_text(buf, ln, x, y + i*line_h, color, scale)

# ------------------------------------------------------------------ layout
def render():
    buf = bytearray(W*H*3)
    rect(buf, 0, 0, W, H, PAPER)  # paper bg
    # ---- masthead
    rect(buf, 0, 0, W, 8, INK)
    rect(buf, 0, 88, W, 92, ACCENT)
    draw_text_center(buf, DATELINE, 22, INK, 2)
    draw_text_center(buf, 'MADE.FUN FRONT PAGE DESK  -  EDITION No. ' + str(100 + (len(SEED)*7) % 400), 58, GREY, 1)
    rect(buf, 0, 92, W, 102, PAPER2)
    draw_text(buf, 'VOL. ' + str(2026 - 1900) + '  -  NO. ' + str(320 + len(SEED) % 20), 16, 95, GREY, 1)
    draw_text(buf, 'LATE CITY FINAL  -  PRICE $2.50', W-16-text_w('LATE CITY FINAL  -  PRICE $2.50',1), 95, GREY, 1)
    # double rule under masthead
    rect(buf, 0, 104, W, 106, INK)
    rect(buf, 0, 108, W, 109, INK)

    # ---- banner headline (top story, big type)
    draw_text_center(buf, 'EXCLUSIVE', 116, ACCENT, 1)
    draw_text_center(buf, BANNER_HEAD, 130, INK, 3)
    draw_text_center(buf, BANNER_SUB, 156, GREY, 1)
    rect(buf, 0, 172, W, 175, ACCENT)

    # ---- ticker strip
    rect(buf, 0, 178, W, 202, PAPER2)
    draw_text(buf, TICKER, 16, 187, INK, 1)
    rect(buf, 0, 204, W, 205, INK)

    # ---- story grid: 2 columns x 2 rows
    y = 216
    col_w = (W - 3*20)//2
    x_left, x_right = 20, 40 + col_w
    row_h = 256
    box_h = row_h - 16
    for i, (kicker, head, body) in enumerate(STORIES[:4]):
        col = i % 2
        row = i // 2
        bx = x_left if col == 0 else x_right
        by = y + row*row_h
        rect(buf, bx, by, bx+col_w, by+box_h, PAPER2)
        rect_outline(buf, bx, by, bx+col_w, by+box_h, GREY, 1)
        rect(buf, bx, by, bx+col_w, by+16, ACCENT2 if col == 0 else ACCENT)
        draw_text(buf, kicker, bx+6, by+4, PAPER, 1)
        fit_text(buf, head, bx+6, by+26, INK, 2, col_w-12, 3, 18)
        fit_text(buf, body, bx+6, by+92, GREY, 1, col_w-12, 7, 12)
    # center column rule between grid columns
    rect(buf, W//2 - 1, y, W//2, y + 2*row_h - 16, GREY)

    # ---- footer
    rect(buf, 0, H-24, W, H, INK)
    draw_text_center(buf, 'SUMMARY OF THE WORLD  -  ' + DATELINE + '  -  PAGE 1', H-16, PAPER, 1)
    return buf

def write_png(path, buf):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += buf[y*W*3:(y+1)*W*3]
    def chunk(tag, data):
        c = tag + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c))
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)

def main():
    out = os.environ.get('MAKEFUN_OUTPUT_DIR') or 'out'
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, 'entry.png')
    write_png(path, render())
    print('wrote', path)

if __name__ == '__main__':
    main()
