#!/usr/bin/env python3
"""
Clip « edit » vertical (1080×1920, ~22 s) pour TikTok / Reels / Shorts.

    python3 _communication/generer_clip.py

Nécessite Google Chrome et ffmpeg (brew install ffmpeg). Le clip est muet :
ajoutez un son tendance directement dans TikTok, Instagram ou CapCut.
Sortie : _communication/visuels/clip-ronin-of-the-black-sun.mp4
"""
import subprocess
import tempfile
from pathlib import Path

from generer_visuels import CHROME, IMG, SORTIE, TETE, VISUELS, fond

FPS = 30
W, H = 1080, 1920
HD_W, HD_H = 2160, 3840  # images rendues en double définition pour des zooms nets


def carte_texte(texte, kanji):
    return (f'<div class="voile" style="background:#050407"></div>'
            f'<div class="kanji" style="position:absolute;left:0;right:0;top:620px;text-align:center;font-size:300px;color:rgba(184,50,42,.14)">{kanji}</div>'
            f'<div style="position:absolute;left:90px;right:90px;top:820px;text-align:center;font-style:italic;font-size:76px;line-height:1.2;color:#f4eee2">{texte}</div>'
            f'<div style="position:absolute;left:50%;top:1120px;width:260px;height:1px;margin-left:-130px;background:linear-gradient(90deg,transparent,#c9a45c,transparent)"></div>')


FIXES = {
    "s0": carte_texte("Le Soleil Noir<br>s'est éteint.", "蝕"),
    "s1": fond("flexarion-ronin-soleil-noir.svg", "52% 50%")
          + '<div class="voile" style="background:linear-gradient(180deg,rgba(8,7,11,.5),transparent 30%,transparent 70%,rgba(8,7,11,.7))"></div>',
    "s2": carte_texte("Le Shogun a fait<br>de sa lumière<br>une arme.", "刀"),
    "s3": fond("flexarion-shiro-chateau-orbital.svg", "50% 50%")
          + '<div class="cinzel or" style="position:absolute;left:0;right:0;top:300px;text-align:center;font-size:60px;font-weight:700;letter-spacing:.2em">LES SEPT SHIRO</div>',
    "s4": fond("flexarion-daimyo-du-vide-boss.svg", "50% 50%") + '''
<svg style="position:absolute;left:290px;top:620px;width:500px;height:500px" viewBox="0 0 200 200">
  <path d="M40 160 A80 80 0 0 1 160 40" fill="none" stroke="#fff8e6" stroke-width="7" stroke-linecap="round" style="filter:drop-shadow(0 0 16px #ecd9a4)"/></svg>
<div class="cinzel or" style="position:absolute;left:0;right:0;top:1300px;text-align:center;font-size:92px;font-weight:700;letter-spacing:.16em;filter:drop-shadow(0 4px 24px #b8322a)">CONTRE-LUNE</div>''',
    "s5a": fond("flexarion-duel-apesanteur-katana.svg", "28% 50%")
           + '<div class="cinzel" style="position:absolute;left:0;right:0;top:1500px;text-align:center;font-size:54px;letter-spacing:.3em;color:#ecd9a4">PAS DU VIDE</div>',
    "s5b": fond("flexarion-duel-apesanteur-katana.svg", "74% 50%"),
    "s6": fond("flexarion-ronin-soleil-noir.svg", "60% 50%") + '''
<div class="voile" style="background:rgba(5,4,7,.72)"></div>
<div class="kanji" style="position:absolute;left:0;right:0;top:520px;text-align:center;font-size:560px;line-height:1;color:rgba(184,50,42,.2)">死</div>
<div class="cinzel" style="position:absolute;left:0;right:0;top:760px;text-align:center;font-size:150px;line-height:1.05;font-weight:600;letter-spacing:.12em;color:#b8322a;text-shadow:0 0 50px rgba(217,71,59,.7)">TOMBÉ<br>AU COMBAT</div>''',
    "s7": fond("flexarion-torii-de-lumiere-sanctuaire.svg", "50% 50%")
          + '<div style="position:absolute;left:0;right:0;top:1460px;text-align:center;font-style:italic;font-size:80px;color:#f4eee2;text-shadow:0 4px 20px #000">Relevez-vous.</div>',
    "s8": VISUELS["11-story-tiktok-vertical.png"][2],
}

# (image, durée, zoom début, zoom fin, tremblement)
PLANS = [
    ("s0", 2.2, 1.00, 1.04, False),
    ("s1", 3.0, 1.00, 1.14, False),
    ("s2", 2.0, 1.00, 1.04, False),
    ("s3", 2.4, 1.12, 1.00, False),
    ("s4", 2.2, 1.18, 1.04, True),
    ("s5a", 1.1, 1.00, 1.10, False),
    ("s5b", 1.1, 1.10, 1.00, False),
    ("s6", 2.2, 1.06, 1.00, True),
    ("s7", 2.4, 1.00, 1.10, False),
    ("s8", 3.6, 1.04, 1.00, False),
]
# transitions entre plans successifs : (type xfade, durée)
TRANSITIONS = [("fadeblack", .5), ("fadeblack", .4), ("fadeblack", .4), ("fadewhite", .25), ("fadewhite", .12),
               ("fadewhite", .08), ("fadeblack", .15), ("fadeblack", .6), ("fadewhite", .45)]


def rendre_fixes(tmp):
    for nom, corps in FIXES.items():
        page = tmp / f"{nom}.html"
        page.write_text(TETE + corps + "</body></html>", encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        "--virtual-time-budget=6000", "--force-device-scale-factor=2", f"--window-size={W},{H}",
                        f"--screenshot={tmp / (nom + '.png')}", page.as_uri()],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("image", nom)


def plan_video(tmp, i, nom, duree, z0, z1, tremble):
    """Zoom progressif (Ken Burns) + tremblement amorti éventuel."""
    zoom = f"({z0}+({z1}-{z0})*t/{duree})"
    sx = "if(lt(t,0.6),28*sin(t*70)*exp(-t*5),0)" if tremble else "0"
    sy = "if(lt(t,0.6),22*cos(t*83)*exp(-t*5),0)" if tremble else "0"
    filtre = (f"scale=w='trunc({HD_W}*{zoom}*1.04/2)*2':h=-2:eval=frame:flags=lanczos,"
              f"crop={HD_W}:{HD_H}:x='(iw-{HD_W})/2+{sx}':y='(ih-{HD_H})/2+{sy}',"
              f"scale={W}:{H}:flags=lanczos,format=yuv420p")
    sortie = tmp / f"plan{i:02d}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS), "-t", str(duree),
                    "-i", str(tmp / f"{nom}.png"), "-vf", filtre, "-r", str(FPS), "-c:v", "libx264", "-crf", "16",
                    "-preset", "medium", str(sortie)], check=True)
    print("plan", i, nom)
    return sortie


def assembler(plans, sortie):
    entrees, chaine, etiquette = [], [], "[0:v]"
    for p in plans:
        entrees += ["-i", str(p)]
    t = PLANS[0][1]
    for k, (typ, d) in enumerate(TRANSITIONS, start=1):
        offset = t - d
        nouvelle = f"[x{k}]"
        chaine.append(f"{etiquette}[{k}:v]xfade=transition={typ}:duration={d}:offset={offset:.3f}{nouvelle}")
        etiquette = nouvelle
        t = offset + PLANS[k][1]
    total = t
    chaine.append(f"{etiquette}noise=alls=3:allf=t,vignette=PI/5,fade=t=in:st=0:d=0.4,fade=t=out:st={total - 0.6:.2f}:d=0.6,format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *entrees, "-filter_complex", ";".join(chaine), "-map", "[v]",
                    "-r", str(FPS), "-c:v", "libx264", "-crf", "23", "-preset", "slow", "-maxrate", "12M", "-bufsize", "24M", "-movflags", "+faststart",
                    str(sortie)], check=True)
    print(f"Clip : {sortie} ({total:.1f} s)")


def main():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        rendre_fixes(tmp)
        plans = [plan_video(tmp, i, *p) for i, p in enumerate(PLANS)]
        assembler(plans, SORTIE / "clip-ronin-of-the-black-sun.mp4")


if __name__ == "__main__":
    main()
