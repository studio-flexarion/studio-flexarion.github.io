#!/usr/bin/env python3
"""
Planche de référence (moodboard) à joindre aux IA vidéo / image.

    python3 _communication/generer_planche.py

Sortie : _communication/visuels/30-planche-reference-ia.png (1920×1080)
"""
import subprocess
import tempfile
from pathlib import Path

from generer_visuels import CHROME, IMG, SORTIE, TETE

V = SORTIE
CASES = f'''
<style>
.g{{position:absolute;inset:40px;display:grid;grid-template-columns:1.35fr 1fr 1fr;grid-template-rows:1fr 1fr;gap:18px}}
.c{{position:relative;overflow:hidden;border:1px solid rgba(201,164,92,.5);background:#0e0d13}}
.c img{{width:100%;height:100%;object-fit:cover;display:block}}
.l{{position:absolute;left:0;right:0;bottom:0;padding:12px 16px;background:linear-gradient(transparent,rgba(5,4,7,.92));font-family:Cinzel;font-size:17px;letter-spacing:.14em;color:#ecd9a4}}
.l small{{display:block;font-family:"Cormorant Garamond";font-size:19px;letter-spacing:0;color:#e8e1d3;margin-top:2px}}
.p{{display:grid;grid-template-columns:repeat(6,1fr);height:100%}}
.p div{{position:relative}}
.p span{{position:absolute;left:8px;bottom:56px;font-family:Cinzel;font-size:13px;color:#e8e1d3;writing-mode:vertical-rl;letter-spacing:.1em;text-shadow:0 1px 4px #000}}
</style>
<div class="g">
  <div class="c" style="grid-row:span 2"><img src="file://{IMG / 'flexarion-ronin-soleil-noir.svg'}" style="object-position:45% 50%">
    <div class="l">HERO · LONE RONIN<small>Wide straw kasa hat, tattered black &amp; crimson cloak, katana held low. Black eclipse sun with golden corona.</small></div></div>
  <div class="c"><img src="file://{IMG / 'flexarion-daimyo-du-vide-boss.svg'}">
    <div class="l">BOSS · VOID DAIMYŌ<small>Colossal armored samurai, crescent kabuto horns, red glowing eyes, golden halo.</small></div></div>
  <div class="c"><img src="file://{V / '01-gameplay-combat-boss.png'}">
    <div class="l">CAMERA &amp; GAMEPLAY<small>Third-person, boss fight framing, parry flash. HUD added in post.</small></div></div>
  <div class="c"><img src="file://{IMG / 'flexarion-duel-apesanteur-katana.svg'}">
    <div class="l">ZERO-G DUEL<small>Floating debris, no up or down, katana light trails.</small></div></div>
  <div class="c"><div class="p">
      <div style="background:#08070b"><span>INK #08070b</span></div><div style="background:#1a1530"><span>VOID #1a1530</span></div>
      <div style="background:#5a0f14"><span>CRIMSON #5a0f14</span></div><div style="background:#b8322a"><span>VERMILION #b8322a</span></div>
      <div style="background:#c9a45c"><span>OLD GOLD #c9a45c</span></div><div style="background:#e8e1d3"><span style="color:#08070b;text-shadow:none">ASH #e8e1d3</span></div></div>
    <div class="l">COLOR PALETTE · « INK &amp; EMBERS »<small>Red always means danger. Gold = sacred light.</small></div></div>
</div>
<div style="position:absolute;right:52px;top:6px;font-family:Cinzel;font-size:14px;letter-spacing:.3em;color:rgba(236,217,164,.7)">RONIN OF THE BLACK SUN · STUDIO FLEXARION · REFERENCE BOARD</div>'''


def main():
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "planche.html"
        page.write_text(TETE + CASES + "</body></html>", encoding="utf-8")
        sortie = V / "30-planche-reference-ia.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        "--virtual-time-budget=6000", "--window-size=1920,1080", f"--screenshot={sortie}", page.as_uri()],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("✓", sortie)


if __name__ == "__main__":
    main()
