"""
Illustrations SVG du site Flexarion (direction artistique « encre et braise »).

    python3 _build/art.py

Écrit les fichiers dans assets/img/. Tout est généré par du code : silhouettes,
dégradés et filtres SVG (aucune image externe).
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

# Palette
INK = "#08070b"
CHAR = "#121019"
ASH = "#e8e1d3"
GOLD = "#c9a45c"
GOLD_L = "#ecd9a4"
VERM = "#b8322a"
CRIM = "#5a0f14"
VOID = "#1a1530"


def write(name, body, w, h, title, desc):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
           f'role="img" aria-labelledby="t d"><title id="t">{title}</title><desc id="d">{desc}</desc>{body}</svg>\n')
    (OUT / name).write_text(svg, encoding="utf-8")


def stars(rng, w, h, n, rmax=1.3, ymax=None, color="#fff"):
    ymax = ymax or h
    return "".join(
        f'<circle cx="{rng.uniform(0, w):.0f}" cy="{rng.uniform(0, ymax):.0f}" r="{rng.uniform(.3, rmax):.1f}" '
        f'fill="{color}" opacity="{rng.uniform(.2, .9):.2f}"/>' for _ in range(n))


def embers(rng, w, h, n, y0=0):
    out = []
    for _ in range(n):
        x, y = rng.uniform(0, w), rng.uniform(y0, h)
        r = rng.uniform(.8, 2.6)
        c = rng.choice([GOLD_L, "#ff9a4a", VERM, GOLD])
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{c}" opacity="{rng.uniform(.35, .95):.2f}"/>')
    return "".join(out)


# Filtres communs : grain, encre (bords irréguliers), halo
FILTERS = f'''
<filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7" result="n"/>
  <feColorMatrix in="n" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .07 0"/>
  <feComposite in2="SourceGraphic" operator="in"/>
</filter>
<filter id="encre" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="3" seed="3" result="t"/>
  <feDisplacementMap in="SourceGraphic" in2="t" scale="18"/>
</filter>
<filter id="brume" filterUnits="userSpaceOnUse" x="-400" y="-400" width="2600" height="1800"><feGaussianBlur stdDeviation="18"/></filter>
<filter id="halo" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
'''


def black_sun(cx, cy, r, rng, rays=90, gid="sol"):
    """Éclipse : disque noir, couronne or/vermillon et rayons fins."""
    ray = []
    for i in range(rays):
        a = 2 * math.pi * i / rays + rng.uniform(-.02, .02)
        l = r * rng.uniform(1.15, 1.9 if i % 3 else 2.6)
        x1, y1 = cx + r * 1.02 * math.cos(a), cy + r * 1.02 * math.sin(a)
        x2, y2 = cx + l * math.cos(a), cy + l * math.sin(a)
        ray.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{GOLD_L}" '
                   f'stroke-width="{rng.uniform(.6, 2.2):.1f}" opacity="{rng.uniform(.12, .5):.2f}"/>')
    return f'''
<defs><radialGradient id="{gid}" cx="50%" cy="50%" r="50%">
  <stop offset=".42" stop-color="{GOLD_L}" stop-opacity=".95"/>
  <stop offset=".5" stop-color="{GOLD}" stop-opacity=".8"/>
  <stop offset=".65" stop-color="{VERM}" stop-opacity=".45"/>
  <stop offset="1" stop-color="{CRIM}" stop-opacity="0"/>
</radialGradient></defs>
<circle cx="{cx}" cy="{cy}" r="{r * 2.4:.0f}" fill="url(#{gid})"/>
<g filter="url(#brume)" opacity=".7">{''.join(ray[::2])}</g>
{''.join(ray)}
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{INK}"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GOLD_L}" stroke-width="2.5" opacity=".9"/>'''


def ronin(x, y, s, fill=INK, rim=GOLD, flip=False):
    """Silhouette de ronin (chapeau kasa, cape au vent, katana tenu bas)."""
    sx = -s if flip else s
    return f'''<g transform="translate({x} {y}) scale({sx} {s})">
  <path d="M100 96 C86 100 74 110 70 128 L58 210 C54 240 58 270 64 300 L50 392 L66 394 L86 306 L104 300 L126 392 L144 390 L124 300
           C150 296 178 290 214 262 C196 266 186 262 176 252 C196 252 206 244 216 232 C194 236 176 230 160 214 L140 130
           C136 112 122 100 100 96 Z" fill="{fill}"/>
  <path d="M12 86 L100 44 L190 86 C160 96 40 96 12 86 Z" fill="{fill}"/>
  <path d="M100 44 L190 86" stroke="{rim}" stroke-width="2" opacity=".8"/>
  <path d="M84 96 Q100 106 118 96 L114 112 Q100 118 88 112 Z" fill="{fill}"/>
  <path d="M120 214 L238 176" stroke="{fill}" stroke-width="9" stroke-linecap="round"/>
  <path d="M120 214 L238 176" stroke="{rim}" stroke-width="1.5" opacity=".6"/>
  <path d="M64 222 L76 232" stroke="{fill}" stroke-width="10" stroke-linecap="round"/>
  <path d="M70 228 L-118 372" stroke="{ASH}" stroke-width="4.5" stroke-linecap="round"/>
  <path d="M70 228 L-118 372" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity=".9" filter="url(#halo)"/>
  <path d="M140 130 L148 220" stroke="{rim}" stroke-width="1.6" opacity=".5"/>
  <path d="M70 128 L60 200" stroke="{rim}" stroke-width="1.6" opacity=".5"/>
</g>'''


def torii(x, y, s, fill=INK, broken=False, glow=None):
    top = (f'<path d="M-20 0 Q130 -26 280 0 L276 16 Q130 -6 -16 16 Z" fill="{fill}"/>'
           if not broken else
           f'<path d="M-20 0 Q60 -14 140 -18 L150 -4 L138 6 Q60 2 -16 16 Z" fill="{fill}"/>'
           f'<path d="M170 6 L280 0 L276 16 L172 22 Z" fill="{fill}" transform="rotate(14 220 10)"/>')
    g = f'<rect x="40" y="40" width="180" height="300" fill="{glow}" opacity=".18" filter="url(#brume)"/>' if glow else ""
    return f'''<g transform="translate({x} {y}) scale({s})">{g}{top}
  <rect x="10" y="34" width="240" height="12" fill="{fill}"/>
  <rect x="40" y="10" width="18" height="340" fill="{fill}"/>
  <rect x="202" y="10" width="18" height="{260 if broken else 340}" fill="{fill}"/>
  <rect x="122" y="16" width="16" height="20" fill="{fill}"/></g>'''


def pagoda(x, y, s, fill, light=GOLD_L, levels=5, rng=None):
    """Château orbital (shiro) : pagode à étages sur un socle de vaisseau."""
    parts = [f'<path d="M-140 0 L140 0 L100 60 L-100 60 Z" fill="{fill}"/>',
             f'<path d="M-60 60 L60 60 L20 120 L-20 120 Z" fill="{fill}"/>']
    w, yy = 120, 0
    for i in range(levels):
        h = 34 - i * 3
        parts.append(f'<rect x="{-w * .62:.0f}" y="{yy - h:.0f}" width="{w * 1.24:.0f}" height="{h}" fill="{fill}"/>')
        parts.append(f'<path d="M{-w - 18:.0f} {yy - h + 4:.0f} Q0 {yy - h - 22:.0f} {w + 18:.0f} {yy - h + 4:.0f} '
                     f'L{w:.0f} {yy - h - 6:.0f} Q0 {yy - h - 26:.0f} {-w:.0f} {yy - h - 6:.0f} Z" fill="{fill}"/>')
        if rng:
            for _ in range(int(w / 18)):
                lx = rng.uniform(-w * .55, w * .55)
                parts.append(f'<rect x="{lx:.0f}" y="{yy - h + 10:.0f}" width="4" height="7" fill="{light}" opacity="{rng.uniform(.4, 1):.2f}"/>')
        yy -= h + 14
        w *= .8
    parts.append(f'<path d="M0 {yy - 10:.0f} L0 {yy - 70:.0f}" stroke="{fill}" stroke-width="5"/>')
    parts.append(f'<circle cx="0" cy="{yy - 74:.0f}" r="5" fill="{VERM}"/>')
    return f'<g transform="translate({x} {y}) scale({s})">{"".join(parts)}</g>'


def mist(y, w, color, op, seed):
    rng = random.Random(seed)
    pts = " ".join(f"{x},{y + rng.uniform(-30, 30):.0f}" for x in range(-100, w + 101, 100))
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="70" opacity="{op}" filter="url(#brume)"/>'


# ===================================================================== key art
def key_art():
    rng = random.Random(1)
    W, H = 1600, 900
    sky = f'''<defs><linearGradient id="ciel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{INK}"/><stop offset=".45" stop-color="{VOID}"/>
      <stop offset=".78" stop-color="{CRIM}"/><stop offset="1" stop-color="#2a0709"/></linearGradient>
      <linearGradient id="sol-roche" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#17121c"/><stop offset="1" stop-color="{INK}"/></linearGradient>
    </defs>'''
    ring = (f'<ellipse cx="1060" cy="330" rx="760" ry="120" fill="none" stroke="{GOLD}" stroke-width="1.4" opacity=".35" transform="rotate(-9 1060 330)"/>'
            f'<ellipse cx="1060" cy="330" rx="820" ry="138" fill="none" stroke="{GOLD}" stroke-width=".8" opacity=".2" stroke-dasharray="2 10" transform="rotate(-9 1060 330)"/>')
    body = f'''{FILTERS}{sky}
<rect width="{W}" height="{H}" fill="url(#ciel)"/>
{stars(rng, W, H, 320, ymax=620)}
{ring}
{black_sun(1060, 330, 150, rng)}
{pagoda(300, 300, .55, "#1b1524", rng=rng)}
{pagoda(1430, 210, .38, "#1e1828", rng=rng)}
{pagoda(640, 160, .22, "#241d2e", rng=rng)}
{mist(560, W, VERM, .25, 2)}
{mist(640, W, "#000", .55, 3)}
<path d="M0 720 C200 690 380 700 560 735 C700 760 820 700 980 690 C1180 680 1380 720 1600 700 L1600 900 L0 900 Z" fill="url(#sol-roche)"/>
{torii(1130, 410, 1.05, "#0d0b12", broken=True, glow=VERM)}
<path d="M560 735 L700 700 L860 712 L900 760 L620 790 Z" fill="#0b0a10"/>
{ronin(640, 330, 1.05, rim=GOLD_L)}
<g opacity=".9">{embers(rng, W, H, 90, y0=380)}</g>
<path d="M0 860 Q800 820 1600 860" stroke="{GOLD}" stroke-width="1" opacity=".25" fill="none"/>
<rect width="{W}" height="{H}" filter="url(#grain)"/>'''
    write("flexarion-ronin-soleil-noir.svg", body, W, H,
          "Flexarion : le ronin face au soleil noir",
          "Key art du jeu Flexarion : un ronin au chapeau de paille, katana à la main, devant une éclipse dorée, un torii brisé et des châteaux orbitaux.")


# ===================================================================== shiro orbital
def shiro():
    rng = random.Random(2)
    W, H = 1200, 700
    body = f'''{FILTERS}
<defs><radialGradient id="planete" cx="35%" cy="30%" r="80%"><stop offset="0" stop-color="#3b2a4a"/><stop offset=".6" stop-color="{VOID}"/><stop offset="1" stop-color="{INK}"/></radialGradient></defs>
<rect width="{W}" height="{H}" fill="{INK}"/>
{stars(rng, W, H, 260)}
<circle cx="600" cy="1250" r="820" fill="url(#planete)"/>
<circle cx="600" cy="1250" r="820" fill="none" stroke="{VERM}" stroke-width="3" opacity=".6" filter="url(#halo)"/>
{mist(470, W, VERM, .18, 5)}
{pagoda(600, 400, 1.0, "#0e0c14", rng=rng, levels=6)}
<g stroke="{GOLD}" stroke-width="1.2" opacity=".45">
  <line x1="460" y1="400" x2="140" y2="520"/><line x1="740" y1="400" x2="1060" y2="520"/>
</g>
<rect x="120" y="512" width="60" height="16" fill="#0e0c14"/><rect x="1030" y="512" width="60" height="16" fill="#0e0c14"/>
<g fill="{GOLD_L}"><circle cx="150" cy="520" r="3"/><circle cx="1060" cy="520" r="3"/></g>
{pagoda(180, 220, .25, "#1a1522", rng=rng)}{pagoda(990, 170, .3, "#1a1522", rng=rng)}
<g opacity=".8">{embers(rng, W, H, 40, y0=300)}</g>
<rect width="{W}" height="{H}" filter="url(#grain)"/>'''
    write("flexarion-shiro-chateau-orbital.svg", body, W, H,
          "Le Shiro de Kurogane, château orbital du jeu Flexarion",
          "Concept art : une forteresse en forme de pagode flotte au-dessus d'une planète violette, reliée par des câbles dorés.")


# ===================================================================== daimyo du vide (boss)
def daimyo():
    rng = random.Random(3)
    W, H = 1200, 700
    body = f'''{FILTERS}
<defs><radialGradient id="aura" cx="50%" cy="45%" r="55%"><stop offset="0" stop-color="{VERM}" stop-opacity=".75"/><stop offset=".6" stop-color="{CRIM}" stop-opacity=".35"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient></defs>
<rect width="{W}" height="{H}" fill="{INK}"/>
{stars(rng, W, H, 140, ymax=500)}
<circle cx="600" cy="300" r="380" fill="url(#aura)"/>
<circle cx="600" cy="250" r="190" fill="none" stroke="{GOLD}" stroke-width="3" opacity=".8" filter="url(#halo)"/>
<circle cx="600" cy="250" r="210" fill="none" stroke="{GOLD}" stroke-width="1" opacity=".35" stroke-dasharray="4 12"/>
<g transform="translate(0 70)"><g fill="#050407">
  <path d="M600 120 C540 120 505 160 500 215 L480 240 L520 250 L530 300 L670 300 L680 250 L720 240 L700 215 C695 160 660 120 600 120 Z"/>
  <path d="M470 150 C420 90 400 40 430 -10 C440 60 480 110 540 140 Z"/>
  <path d="M730 150 C780 90 800 40 770 -10 C760 60 720 110 660 140 Z"/>
  <path d="M420 300 L780 300 L900 360 L960 470 L860 470 L800 400 L790 700 L410 700 L400 400 L340 470 L240 470 L300 360 Z"/>
  <path d="M300 360 L240 470 L170 480 L230 340 Z"/><path d="M900 360 L960 470 L1030 480 L970 340 Z"/>
</g>
<g stroke="{GOLD}" stroke-width="1.8" fill="none" opacity=".75">
  <path d="M470 150 C420 90 400 40 430 -10"/><path d="M730 150 C780 90 800 40 770 -10"/>
  <path d="M500 215 C505 160 540 120 600 120 C660 120 695 160 700 215"/>
  <path d="M420 330 L780 330 M425 360 L775 360 M430 390 L770 390"/>
</g>
<g fill="{VERM}" filter="url(#halo)"><path d="M555 232 L585 238 L580 246 L556 242 Z"/><path d="M645 232 L615 238 L620 246 L644 242 Z"/></g>
<path d="M880 470 L1120 120" stroke="{ASH}" stroke-width="6" stroke-linecap="round"/>
<path d="M880 470 L1120 120" stroke="#fff" stroke-width="2" filter="url(#halo)"/></g>
<ellipse cx="200" cy="600" rx="190" ry="140" fill="{GOLD}" opacity=".35" filter="url(#brume)"/>
{ronin(150, 410, .62, fill="#000", rim=GOLD_L)}
<g opacity=".9">{embers(rng, W, H, 60, y0=200)}</g>
<rect width="{W}" height="{H}" filter="url(#grain)"/>'''
    write("flexarion-daimyo-du-vide-boss.svg", body, W, H,
          "Un Daimyō du Vide, boss du jeu Flexarion",
          "Concept art : un samouraï géant en armure, casque à cornes en croissant et yeux rouges, domine un petit ronin.")


# ===================================================================== torii de lumière (sanctuaire)
def torii_lumiere():
    rng = random.Random(4)
    W, H = 1200, 700
    body = f'''{FILTERS}
<defs><linearGradient id="fond4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{VOID}"/></linearGradient>
<radialGradient id="lumiere" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{GOLD_L}" stop-opacity=".9"/><stop offset=".5" stop-color="{GOLD}" stop-opacity=".35"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>
<rect width="{W}" height="{H}" fill="url(#fond4)"/>
{stars(rng, W, H, 300)}
<ellipse cx="600" cy="360" rx="260" ry="300" fill="url(#lumiere)"/>
{torii(470, 200, 1.0, "#07060a")}
<path d="M440 560 L760 560 L720 600 L480 600 Z" fill="#07060a"/>
<g stroke="{GOLD_L}" stroke-width="1" opacity=".6">{''.join(f'<line x1="{600 + rng.uniform(-90, 90):.0f}" y1="{rng.uniform(240, 540):.0f}" x2="{600 + rng.uniform(-90, 90):.0f}" y2="{rng.uniform(240, 540) - 60:.0f}"/>' for _ in range(24))}</g>
{''.join(f'<rect x="{x}" y="{y}" width="40" height="{h}" rx="6" fill="#07060a" transform="rotate({r} {x + 20} {y})"/>' for x, y, h, r in [(130, 520, 80, -20), (980, 480, 110, 25), (300, 150, 50, 40), (880, 120, 60, -35)])}
<g fill="{VERM}">{''.join(f'<path d="M{x} {y} q8 -14 0 -26 q-8 12 0 26z" opacity=".9"/>' for x, y in [(520, 596), (680, 596)])}</g>
{ronin(560, 410, .4, rim=GOLD_L)}
<g opacity=".8">{embers(rng, W, H, 50)}</g>
<rect width="{W}" height="{H}" filter="url(#grain)"/>'''
    write("flexarion-torii-de-lumiere-sanctuaire.svg", body, W, H,
          "Un Torii de lumière, sanctuaire de repos dans Flexarion",
          "Concept art : un portail torii flotte dans l'espace, baigné d'une lumière dorée ; un ronin s'en approche.")


# ===================================================================== duel en apesanteur
def duel():
    rng = random.Random(5)
    W, H = 1200, 700
    debris = "".join(
        f'<polygon points="{x},{y} {x + rng.uniform(20, 70):.0f},{y + rng.uniform(-20, 20):.0f} {x + rng.uniform(10, 50):.0f},{y + rng.uniform(20, 60):.0f}" fill="#0c0a11" opacity=".95"/>'
        for x, y in [(rng.uniform(0, W), rng.uniform(0, H)) for _ in range(26)])
    body = f'''{FILTERS}
<rect width="{W}" height="{H}" fill="{INK}"/>
{stars(rng, W, H, 220)}
<ellipse cx="560" cy="380" rx="420" ry="230" fill="{VOID}" opacity=".9" filter="url(#brume)"/>
<ellipse cx="640" cy="360" rx="260" ry="150" fill="{CRIM}" opacity=".8" filter="url(#brume)"/>
<ellipse cx="420" cy="430" rx="160" ry="110" fill="{GOLD}" opacity=".22" filter="url(#brume)"/>
{black_sun(980, 160, 70, rng, rays=60, gid="sol2")}
{debris}
<path d="M120 560 C380 380 760 300 1120 140" stroke="{VERM}" stroke-width="26" fill="none" opacity=".35" filter="url(#brume)"/>
<path d="M120 560 C380 380 760 300 1120 140" stroke="{ASH}" stroke-width="5" fill="none" stroke-linecap="round" filter="url(#encre)"/>
<path d="M120 560 C380 380 760 300 1120 140" stroke="#fff" stroke-width="1.6" fill="none" filter="url(#halo)"/>
{ronin(330, 210, .75, fill="#000", rim=GOLD_L)}
<g transform="rotate(200 820 330)">{ronin(760, 200, .75, fill="#000", rim=VERM)}</g>
<g opacity=".95">{embers(rng, W, H, 70)}</g>
<rect width="{W}" height="{H}" filter="url(#grain)"/>'''
    write("flexarion-duel-apesanteur-katana.svg", body, W, H,
          "Duel au katana en apesanteur dans Flexarion",
          "Concept art : deux samouraïs, l'un la tête en bas, s'affrontent au milieu de débris flottants, tranchés par un arc de lumière.")


# ===================================================================== Sainte-Victoire à l'encre
def victoire():
    rng = random.Random(6)
    W, H = 1200, 600
    body = f'''{FILTERS}
<defs><linearGradient id="ciel6" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{INK}"/><stop offset=".7" stop-color="{CRIM}"/><stop offset="1" stop-color="{VERM}"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#ciel6)"/>
{stars(rng, W, H, 160, ymax=300)}
{black_sun(760, 330, 90, rng, rays=70, gid="sol3")}
<g filter="url(#encre)">
  <path d="M0 600 L0 470 L140 450 L260 420 L360 360 L420 280 L462 236 L500 230 L552 268 L640 300 L740 318 L860 344 L980 372 L1100 400 L1200 410 L1200 600 Z" fill="{INK}"/>
  <path d="M360 360 L420 280 L462 236 L500 230 L552 268 L640 300" stroke="{GOLD_L}" stroke-width="2" fill="none" opacity=".8"/>
</g>
{mist(500, W, "#000", .6, 9)}
<path d="M0 600 L0 540 Q300 510 600 530 T1200 520 L1200 600 Z" fill="#050407"/>
<g opacity=".8">{embers(rng, W, H, 30, y0=300)}</g>
<rect width="{W}" height="{H}" filter="url(#grain)"/>'''
    write("flexarion-aix-en-provence-sainte-victoire-encre.svg", body, W, H,
          "La Sainte-Victoire à l'encre, à Aix-en-Provence, berceau du studio Flexarion",
          "Illustration : la silhouette de la montagne Sainte-Victoire peinte à l'encre devant un soleil noir et un ciel vermillon.")


# ===================================================================== nuancier (devlog DA)
def nuancier():
    rng = random.Random(8)
    W, H = 1200, 630
    sw = [(INK, "ENCRE", "#08070b"), (VOID, "VIDE", "#1a1530"), (CRIM, "SANG SÉCHÉ", "#5a0f14"),
          (VERM, "VERMILLON", "#b8322a"), (GOLD, "OR ANCIEN", "#c9a45c"), (ASH, "CENDRE", "#e8e1d3")]
    bands = []
    for i, (c, n, hx) in enumerate(sw):
        x = 70 + i * 120
        bands.append(f'<rect x="{x}" y="70" width="96" height="400" fill="{c}" stroke="{GOLD}" stroke-opacity=".35" filter="url(#encre)"/>'
                     f'<text x="{x}" y="505" font-family="ui-monospace, Menlo, monospace" font-size="13" fill="{ASH}" letter-spacing="1.5">{n}</text>'
                     f'<text x="{x}" y="527" font-family="ui-monospace, Menlo, monospace" font-size="12" fill="{GOLD}">{hx}</text>')
    body = f'''{FILTERS}
<rect width="{W}" height="{H}" fill="{CHAR}"/>
{''.join(bands)}
<g transform="translate(930 330)">
  <circle r="200" fill="{INK}" stroke="{GOLD}" stroke-opacity=".3"/>
  <path d="M-150 -40 A160 160 0 1 1 -120 110" fill="none" stroke="{ASH}" stroke-width="26" stroke-linecap="round" filter="url(#encre)" opacity=".92"/>
  <circle cx="0" cy="0" r="38" fill="{VERM}"/>
  {ronin(-48, -40, .32, rim=GOLD_L)}
</g>
<rect width="{W}" height="{H}" filter="url(#grain)"/>'''
    write("flexarion-palette-encre-et-braise.svg", body, W, H,
          "La palette « encre et braise » du jeu Flexarion",
          "Nuancier de six couleurs (encre, vide, sang séché, vermillon, or ancien, cendre) à côté d'un ensō peint à l'encre et d'un ronin.")


# ===================================================================== logo du studio
ENSO_MARK = f'''<defs><linearGradient id="or" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GOLD_L}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient></defs>
<path d="M50 9 C74 9 92 28 91 52 C90 76 70 93 47 91 C24 89 8 70 10 47 C11 32 19 20 31 14" fill="none" stroke="url(#or)" stroke-width="8" stroke-linecap="round"/>
<path d="M38 74 L40 26" stroke="{ASH}" stroke-width="7" stroke-linecap="round"/>
<path d="M36 28 Q56 24 76 16 Q60 30 40 34 Z" fill="{ASH}"/>
<path d="M39 50 Q52 48 64 44 Q54 54 40 56 Z" fill="{ASH}"/>
<circle cx="67" cy="66" r="9" fill="{VERM}"/>'''


def logos():
    write("flexarion-logo.svg", ENSO_MARK, 100, 100, "Flexarion", "Logo du studio Flexarion : un ensō doré traversé d'un trait de katana et un soleil vermillon.")
    write("favicon.svg", f'<rect width="100" height="100" rx="20" fill="{INK}"/>{ENSO_MARK}', 100, 100, "Flexarion", "Icône Flexarion")
    write("flexarion-logo-carre.svg", f'<rect width="100" height="100" fill="{INK}"/><g transform="translate(15 15) scale(.7)">{ENSO_MARK}</g>', 100, 100, "Flexarion", "Logo Flexarion sur fond noir")


if __name__ == "__main__":
    key_art(); shiro(); daimyo(); torii_lumiere(); duel(); victoire(); nuancier(); logos()
    for p in sorted(OUT.glob("*.svg")):
        print(f"{p.stat().st_size // 1024:>4} Ko  {p.name}")
