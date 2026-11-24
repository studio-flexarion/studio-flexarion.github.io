#!/usr/bin/env python3
"""
Visuels pour les réseaux sociaux de Ronin of the Black Sun (studio Flexarion).

    python3 _communication/generer_visuels.py

Chaque visuel est une page HTML (illustration du site + interface de jeu en CSS)
photographiée par Google Chrome en mode headless. Résultat : _communication/visuels/*.png
Le dossier _communication/ n'est pas publié sur le site (préfixe « _ »).
"""
import subprocess
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
IMG = ICI.parent / "assets" / "img"
SORTIE = ICI / "visuels"
SORTIE.mkdir(exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TETE = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Shippori+Mincho:wght@800&display=block" rel="stylesheet">
<style>
*{box-sizing:border-box}html,body{margin:0;overflow:hidden;background:#08070b;color:#e8e1d3;font-family:"Cormorant Garamond",serif}
.fond{position:absolute;inset:0;background-size:cover;background-position:center}
.voile{position:absolute;inset:0}
.cinzel{font-family:Cinzel,serif}.kanji{font-family:"Shippori Mincho",serif;font-weight:800}
.or{background:linear-gradient(180deg,#fff8e6 10%,#ecd9a4 45%,#c9a45c 85%);-webkit-background-clip:text;color:transparent}
.grain:after{content:"";position:absolute;inset:0;opacity:.07;pointer-events:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E")}
/* ---- interface de jeu ---- */
.barre{position:relative;height:12px;background:rgba(0,0,0,.6);border:1px solid rgba(201,164,92,.55)}
.barre i{position:absolute;inset:1px auto 1px 1px;display:block}
.vie i{background:linear-gradient(90deg,#7a1712,#d9473b)}
.ki i{background:linear-gradient(90deg,#8a6b2e,#ecd9a4)}
.posture i{background:linear-gradient(90deg,#c9a45c,#fff2c4);box-shadow:0 0 12px #ecd9a4}
.joueur{position:absolute;left:60px;top:54px;width:520px}
.joueur .nom{font-family:Cinzel;letter-spacing:.3em;font-size:18px;color:#ecd9a4;margin-bottom:10px}
.joueur .barre{margin-bottom:8px}
.boss{position:absolute;left:50%;bottom:92px;transform:translateX(-50%);width:1100px}
.boss .nom{font-family:Cinzel;font-size:26px;letter-spacing:.18em;color:#f4eee2;margin-bottom:10px;text-shadow:0 2px 10px #000}
.boss .vie{height:14px}
.boss .posture{height:8px;margin-top:8px;width:60%;margin-left:20%}
.cendres{position:absolute;right:64px;bottom:60px;font-family:Cinzel;font-size:30px;letter-spacing:.08em;color:#ecd9a4;display:flex;align-items:center;gap:14px;text-shadow:0 2px 12px #000}
.cendres b{width:16px;height:16px;transform:rotate(45deg);background:#d9473b;box-shadow:0 0 18px #ff7a3d}
.objets{position:absolute;left:60px;bottom:56px;display:flex;gap:12px}
.objets div{width:74px;height:74px;border:1px solid rgba(201,164,92,.6);background:rgba(8,7,11,.65);display:grid;place-items:center;font-family:"Shippori Mincho";font-weight:800;font-size:32px;color:#e8e1d3}
.objets div:first-child{border-color:#ecd9a4;box-shadow:inset 0 0 0 3px rgba(236,217,164,.2)}
.maquette{position:absolute;right:22px;top:18px;font-family:Cinzel;font-size:13px;letter-spacing:.2em;color:rgba(232,225,211,.55)}
.marque{position:absolute;display:flex;align-items:center;gap:14px}
.marque img{width:58px}
.marque span{font-family:Cinzel;font-weight:700;letter-spacing:.3em;font-size:22px;color:#fff}
.titre b{display:block;font-family:Cinzel;font-weight:700;letter-spacing:.12em;line-height:.92}
.titre span{display:block;font-family:Cinzel;font-weight:700;letter-spacing:.42em}
</style></head><body class="grain">"""


def fond(img, pos="center", taille="cover"):
    return f'<div class="fond" style="background-image:url(\'file://{IMG / img}\');background-position:{pos};background-size:{taille}"></div>'


def hud(boss=None, vie_boss=72, posture_boss=64, vie=81, ki=55, cendres="12 480"):
    h = f'''<div class="joueur"><div class="nom">KAÏEN</div>
      <div class="barre vie"><i style="width:{vie}%"></i></div>
      <div class="barre ki" style="height:8px;width:80%"><i style="width:{ki}%"></i></div></div>
    <div class="objets"><div>月</div><div>灯</div><div>薬</div><div>札</div></div>
    <div class="cendres"><b></b>{cendres}</div>
    <div class="maquette">MAQUETTE · PRÉ-ALPHA</div>'''
    if boss:
        h += f'''<div class="boss"><div class="nom">{boss}</div>
      <div class="barre vie"><i style="width:{vie_boss}%"></i></div>
      <div class="barre posture"><i style="width:{posture_boss}%"></i></div></div>'''
    return h


VISUELS = {}

# ---------------------------------------------------------------- captures « gameplay » 16:9
VISUELS["01-gameplay-combat-boss.png"] = (1920, 1080, fond("flexarion-daimyo-du-vide-boss.svg") + '''
<div class="voile" style="background:radial-gradient(ellipse at 50% 40%,transparent 40%,rgba(0,0,0,.55))"></div>
<svg style="position:absolute;left:880px;top:300px;width:420px;height:420px" viewBox="0 0 200 200">
  <path d="M40 160 A80 80 0 0 1 160 40" fill="none" stroke="#fff8e6" stroke-width="7" stroke-linecap="round" opacity=".95" style="filter:drop-shadow(0 0 14px #ecd9a4)"/>
  <path d="M55 150 A70 70 0 0 1 150 55" fill="none" stroke="#c9a45c" stroke-width="2" opacity=".7"/></svg>
<div class="cinzel or" style="position:absolute;left:0;right:0;top:250px;text-align:center;font-size:64px;font-weight:700;letter-spacing:.3em;filter:drop-shadow(0 4px 20px #b8322a)">CONTRE-LUNE</div>
''' + hud("La Daimyō de la Rouille", 58, 92))

VISUELS["02-gameplay-duel-apesanteur.png"] = (1920, 1080, fond("flexarion-duel-apesanteur-katana.svg") + '''
<div class="voile" style="background:radial-gradient(ellipse at 50% 45%,transparent 45%,rgba(0,0,0,.5))"></div>
<svg style="position:absolute;left:1120px;top:395px;width:90px;height:90px" viewBox="0 0 40 40"><path d="M20 2 L38 20 L20 38 L2 20 Z" fill="none" stroke="#d9473b" stroke-width="2"/><circle cx="20" cy="20" r="3" fill="#d9473b"/></svg>
<div class="cinzel" style="position:absolute;left:70px;top:190px;font-size:22px;letter-spacing:.3em;color:#ecd9a4">PAS DU VIDE <span style="color:#d9473b">×3</span></div>
<div class="cinzel" style="position:absolute;left:70px;top:226px;font-size:15px;letter-spacing:.24em;color:rgba(232,225,211,.7)">GRAVITÉ : NULLE</div>
''' + hud("Le Daimyō de la Marée stellaire", 81, 35, vie=63, ki=30, cendres="8 215"))

VISUELS["03-gameplay-exploration-torii.png"] = (1920, 1080, fond("flexarion-torii-de-lumiere-sanctuaire.svg") + '''
<div style="position:absolute;left:0;right:0;top:250px;text-align:center">
  <div style="height:1px;width:900px;margin:0 auto 22px;background:linear-gradient(90deg,transparent,#c9a45c,transparent)"></div>
  <div class="cinzel or" style="font-size:76px;font-weight:700;letter-spacing:.22em">SHIRO-FERRAILLE</div>
  <div style="font-style:italic;font-size:34px;color:#e8e1d3;margin-top:8px">Cimetière d'acier</div>
  <div style="height:1px;width:900px;margin:22px auto 0;background:linear-gradient(90deg,transparent,#c9a45c,transparent)"></div>
</div>
<div style="position:absolute;left:0;right:0;bottom:190px;text-align:center;font-family:Cinzel;font-size:24px;letter-spacing:.2em;color:#ecd9a4">
  <span style="display:inline-grid;place-items:center;width:44px;height:44px;border:1px solid #ecd9a4;margin-right:16px;color:#fff">E</span>Se reposer au Torii de lumière</div>
''' + hud(None, cendres="3 090"))

VISUELS["04-ecran-tombe-au-combat.png"] = (1920, 1080, fond("flexarion-ronin-soleil-noir.svg") + '''
<div class="voile" style="background:rgba(5,4,7,.55)"></div>
<div style="position:absolute;left:0;right:0;top:390px;height:300px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.85) 30%,rgba(0,0,0,.85) 70%,transparent)"></div>
<div class="kanji" style="position:absolute;left:0;right:0;top:330px;text-align:center;font-size:380px;line-height:1;color:rgba(184,50,42,.16)">死</div>
<div class="cinzel" style="position:absolute;left:0;right:0;top:470px;text-align:center;font-size:118px;font-weight:600;letter-spacing:.16em;color:#b8322a;text-shadow:0 0 40px rgba(217,71,59,.6)">TOMBÉ AU COMBAT</div>
<div style="position:absolute;left:0;right:0;top:640px;text-align:center;font-style:italic;font-size:32px;color:rgba(232,225,211,.75)">Vos Cendres d'étoile vous attendent là où vous êtes tombé.</div>
<div class="maquette">MAQUETTE · PRÉ-ALPHA</div>''')

# ---------------------------------------------------------------- formats réseaux sociaux
LOGO = f'<img src="file://{IMG / "flexarion-logo.svg"}">'

VISUELS["10-instagram-annonce-carre.png"] = (1080, 1080, fond("flexarion-ronin-soleil-noir.svg", "42% 50%") + f'''
<div class="voile" style="background:linear-gradient(180deg,rgba(8,7,11,.2) 30%,rgba(8,7,11,.95) 85%)"></div>
<div class="marque" style="left:60px;top:56px">{LOGO}<span>FLEXARION</span></div>
<div class="kanji" style="position:absolute;right:60px;top:60px;writing-mode:vertical-rl;font-size:44px;letter-spacing:.3em;color:#ecd9a4">星を斬る浪人</div>
<div style="position:absolute;left:60px;right:60px;bottom:70px">
  <div class="cinzel" style="font-size:20px;letter-spacing:.34em;color:#c9a45c;margin-bottom:16px">UN JEU DU STUDIO FLEXARION</div>
  <div class="titre or"><b style="font-size:150px">RONIN</b><span style="font-size:46px;margin-top:14px">OF THE BLACK SUN</span></div>
  <div style="font-style:italic;font-size:34px;margin-top:22px">Le souls-like de science-fiction où vous incarnez un ronin.</div>
  <div class="cinzel" style="font-size:18px;letter-spacing:.24em;color:#d9473b;margin-top:22px">DÉMO · PRINTEMPS 2027</div>
</div>''')

VISUELS["11-story-tiktok-vertical.png"] = (1080, 1920, fond("flexarion-ronin-soleil-noir.svg", "48% 50%") + f'''
<div class="voile" style="background:linear-gradient(180deg,rgba(8,7,11,.75) 0%,transparent 25%,transparent 50%,rgba(8,7,11,.96) 78%)"></div>
<div class="marque" style="left:70px;top:90px">{LOGO}<span>FLEXARION</span></div>
<div style="position:absolute;left:70px;right:70px;bottom:230px">
  <div class="kanji" style="font-size:48px;letter-spacing:.24em;color:#d9473b;margin-bottom:18px">星を斬る浪人</div>
  <div class="titre or"><b style="font-size:178px">RONIN</b><span style="font-size:54px;margin-top:16px">OF THE BLACK SUN</span></div>
  <div style="font-style:italic;font-size:44px;margin-top:30px;line-height:1.25">Le Soleil Noir s'est éteint.<br>Le Shogun a fait de sa lumière une arme.<br>Reprenez-la, lame à la main.</div>
</div>
<div class="cinzel" style="position:absolute;left:0;right:0;bottom:110px;text-align:center;font-size:24px;letter-spacing:.3em;color:#ecd9a4">LIEN DANS LA BIO</div>''')

VISUELS["12-banniere-x-twitter-1500x500.png"] = (1500, 500, fond("flexarion-ronin-soleil-noir.svg", "50% 55%") + '''
<div class="voile" style="background:linear-gradient(270deg,rgba(8,7,11,.92) 0%,rgba(8,7,11,.4) 45%,transparent 70%)"></div>
<div style="position:absolute;right:80px;top:50%;transform:translateY(-50%);text-align:right">
  <div class="titre or"><b style="font-size:96px">RONIN</b><span style="font-size:30px;margin-top:10px">OF THE BLACK SUN</span></div>
  <div class="cinzel" style="font-size:16px;letter-spacing:.3em;color:#c9a45c;margin-top:18px">STUDIO FLEXARION · AIX-EN-PROVENCE</div>
</div>''')

VISUELS["13-linkedin-1200x627.png"] = (1200, 627, fond("flexarion-aix-en-provence-sainte-victoire-encre.svg", "60% 50%") + f'''
<div class="voile" style="background:linear-gradient(90deg,rgba(8,7,11,.95) 0%,rgba(8,7,11,.6) 55%,transparent 85%)"></div>
<div class="marque" style="left:70px;top:60px">{LOGO}<span>FLEXARION</span></div>
<div style="position:absolute;left:70px;bottom:70px;width:640px">
  <div class="cinzel" style="font-size:44px;font-weight:600;line-height:1.15;color:#f4eee2">Studio de jeux vidéo indépendant à Aix-en-Provence</div>
  <div style="font-size:28px;margin-top:18px;color:#d9d2c3">Né d'un projet à l'IUT d'Aix. Nous développons <em>Ronin of the Black Sun</em>, un souls-like de science-fiction.</div>
</div>''')

# Carrousel Instagram (3 diapos) : les mécaniques
DIAPOS = [
    ("flexarion-daimyo-du-vide-boss.svg", "月", "LA CONTRE-LUNE", "Parez à la dernière seconde. La parade parfaite brise la garde des Daimyō plus vite que n'importe quelle attaque."),
    ("flexarion-duel-apesanteur-katana.svg", "空", "LE PAS DU VIDE", "Dans le vide, il n'y a ni haut ni bas. Prenez appui sur les débris et frappez depuis n'importe quel angle."),
    ("flexarion-torii-de-lumiere-sanctuaire.svg", "灰", "LES CENDRES D'ÉTOILE", "Mourez, et vos Cendres restent là où vous êtes tombé. Retournez les chercher… si vous l'osez."),
]
for i, (img, k, t, d) in enumerate(DIAPOS, 1):
    VISUELS[f"2{i}-carrousel-mecanique-{i}.png"] = (1080, 1350, fond(img, "50% 50%") + f'''
<div class="voile" style="background:linear-gradient(180deg,rgba(8,7,11,.35) 0%,transparent 30%,rgba(8,7,11,.97) 68%)"></div>
<div class="cinzel" style="position:absolute;right:60px;top:56px;font-size:20px;letter-spacing:.3em;color:#ecd9a4">{i} / 3</div>
<div style="position:absolute;left:70px;right:70px;bottom:90px">
  <div class="kanji" style="font-size:110px;line-height:1;color:#d9473b;text-shadow:0 0 30px rgba(184,50,42,.6)">{k}</div>
  <div class="cinzel or" style="font-size:66px;font-weight:700;letter-spacing:.1em;margin-top:18px">{t}</div>
  <div style="font-size:38px;line-height:1.3;margin-top:20px">{d}</div>
  <div class="cinzel" style="font-size:18px;letter-spacing:.3em;color:#c9a45c;margin-top:30px">RONIN OF THE BLACK SUN · STUDIO FLEXARION</div>
</div>''')


def main():
    with tempfile.TemporaryDirectory() as tmp:
        for nom, (w, h, corps) in VISUELS.items():
            page = Path(tmp) / (nom + ".html")
            page.write_text(TETE + corps + "</body></html>", encoding="utf-8")
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                            "--virtual-time-budget=6000", f"--window-size={w},{h}", f"--screenshot={SORTIE / nom}", page.as_uri()],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            print("✓", nom)


if __name__ == "__main__":
    main()
