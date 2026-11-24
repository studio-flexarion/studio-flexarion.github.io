#!/usr/bin/env python3
"""
Bande-son originale du clip (synthèse sonore en Python pur, sans échantillon ni droits d'auteur).

    python3 _communication/generer_son.py

Taiko, gong, flûte façon shakuhachi (gamme japonaise miyako-bushi), chocs de katana,
souffles et impacts, calés sur les coupes du clip généré par generer_clip.py.
Sortie : visuels/bande-son.wav puis visuels/clip-ronin-of-the-black-sun-son.mp4 (clip + son).
"""
import math
import random
import subprocess
import wave
from array import array
from pathlib import Path

ICI = Path(__file__).resolve().parent
SORTIE = ICI / "visuels"
SR = 44100
DUREE = 19.3
N = int(SR * DUREE)
buf = array("f", bytes(4 * N))
rng = random.Random(7)
TAU = 2 * math.pi


def ajouter(t0, duree, gen, gain=1.0):
    """Ajoute gen(t) (t en secondes depuis t0) au mixage."""
    i0 = int(t0 * SR)
    for k in range(int(duree * SR)):
        i = i0 + k
        if i >= N:
            break
        if i >= 0:
            buf[i] += gain * gen(k / SR)


def bruit_filtre(fc_de_t, gain_de_t):
    """Bruit blanc passé dans un passe-bas à une pôle dont la coupure varie dans le temps."""
    etat = [0.0]

    def g(t):
        a = 1 - math.exp(-TAU * fc_de_t(t) / SR)
        etat[0] += a * (rng.uniform(-1, 1) - etat[0])
        return etat[0] * gain_de_t(t)
    return g


# ---------------------------------------------------------------- instruments
def taiko(t0, gain=1.0, hauteur=1.0):
    phase = [0.0]
    frappe = bruit_filtre(lambda t: 1800, lambda t: math.exp(-t * 55))

    def g(t):
        f = (48 + 95 * math.exp(-t * 28)) * hauteur
        phase[0] += TAU * f / SR
        corps = math.sin(phase[0]) * math.exp(-t * 5.5)
        peau = math.sin(phase[0] * 2.3) * 0.25 * math.exp(-t * 18)
        return corps + peau + 1.4 * frappe(t)
    ajouter(t0, 1.2, g, gain)


def gong(t0, gain=1.0, base=98.0, duree=5.5):
    partiels = [(1.0, 1.0, .9), (1.483, .7, 1.3), (2.09, .55, 1.8), (2.56, .4, 2.4), (3.18, .3, 3.1), (4.13, .22, 4.0)]

    def g(t):
        att = min(1.0, t / .012)
        s = 0.0
        for r, a, d in partiels:
            s += a * math.sin(TAU * base * r * t + .6 * math.sin(TAU * .9 * t)) * math.exp(-t * d)
        return att * s * .45
    ajouter(t0, duree, g, gain)


def choc_katana(t0, gain=1.0):
    partiels = [(1870, 1.0, 7), (2530, .8, 9), (3310, .7, 6), (4420, .5, 12), (5940, .35, 15), (7210, .25, 18)]
    eclat = bruit_filtre(lambda t: 6000, lambda t: math.exp(-t * 45))

    def g(t):
        s = sum(a * math.sin(TAU * f * t) * math.exp(-t * d) for f, a, d in partiels)
        return s * .3 + eclat(t) * 1.2
    ajouter(t0, 1.6, g, gain)


def lame(t0, gain=1.0):
    """« Shing » d'une lame qu'on dégaine : tonalité aiguë qui monte."""
    souffle = bruit_filtre(lambda t: 3000 + 5000 * t, lambda t: math.sin(math.pi * min(t / .35, 1)) * .6)
    phase = [0.0]

    def g(t):
        f = 2900 + 1400 * min(t / .25, 1)
        phase[0] += TAU * f / SR
        env = min(1, t / .02) * math.exp(-t * 6)
        return (math.sin(phase[0]) + .4 * math.sin(phase[0] * 1.51)) * env * .35 + souffle(t) * .5
    ajouter(t0, .9, g, gain)


def souffle(t0, duree, gain=1.0):
    g = bruit_filtre(lambda t: 300 + 2600 * math.sin(math.pi * t / duree),
                     lambda t: math.sin(math.pi * t / duree) ** 2)
    ajouter(t0, duree, g, gain)


def montee(t0, duree, gain=1.0):
    b = bruit_filtre(lambda t: 200 + 7000 * (t / duree) ** 2, lambda t: (t / duree) ** 2)
    phase = [0.0]

    def g(t):
        phase[0] += TAU * (110 + 330 * (t / duree) ** 2) / SR
        return b(t) * .8 + math.sin(phase[0]) * .25 * (t / duree) ** 2
    ajouter(t0, duree, g, gain)


def impact(t0, gain=1.0, duree=2.6):
    phase = [0.0]

    def g(t):
        phase[0] += TAU * (30 + 40 * math.exp(-t * 6)) / SR
        return math.sin(phase[0]) * math.exp(-t * 1.6) * min(1, t / .004)
    ajouter(t0, duree, g, gain)


def bourdon(t0, t1, gain=1.0, entree=1.5, sortie=.03):
    vent = bruit_filtre(lambda t: 260 + 120 * math.sin(TAU * .13 * t), lambda t: .12)
    d = t1 - t0

    def g(t):
        env = min(1, t / entree) * min(1, (d - t) / sortie)
        lfo = .75 + .25 * math.sin(TAU * .21 * t)
        s = (math.sin(TAU * 55 * t) + .8 * math.sin(TAU * 55.35 * t) + .45 * math.sin(TAU * 82.4 * t)
             + .2 * math.sin(TAU * 110.2 * t))
        return env * (s * .28 * lfo + vent(t))
    ajouter(t0, d, g, gain)


def flute(t0, notes, gain=1.0):
    """Flûte de bambou façon shakuhachi : attaque soufflée, glissé vers la note, vibrato tardif."""
    t = t0
    for f, d in notes:
        phase = [0.0]
        souffle_n = bruit_filtre(lambda x, f=f: f * 3, lambda x: .35)

        def g(x, f=f, d=d):
            glisse = f * (2 ** (-1 / 12 * math.exp(-x * 14)))  # monte d'un demi-ton vers la note
            vib = 1 + .006 * min(1, x / (d * .6)) * math.sin(TAU * 5.2 * x)
            phase[0] += TAU * glisse * vib / SR
            env = min(1, x / .07) * min(1, max(0, (d - x) / .12))
            ton = math.sin(phase[0]) + .18 * math.sin(2 * phase[0]) + .06 * math.sin(3 * phase[0])
            return env * (ton * .5 + souffle_n(x) * (.5 if x < .1 else .22))
        ajouter(t, d + .05, g, gain)
        t += d


def acouphene(t0, duree, gain=1.0):
    ajouter(t0, duree, lambda t: math.sin(TAU * 2750 * t) * math.exp(-t * 1.2) * min(1, t / .05), gain)


# Gamme miyako-bushi sur ré
RE4, MIB4, SOL4, LA4, SIB4, RE5 = 293.66, 311.13, 392.0, 440.0, 466.16, 587.33

# ---------------------------------------------------------------- partition calée sur le clip
# Coupes du clip : s1 1.70 · s2 4.30 · s3 5.90 · s4 8.05 · s5a 10.13 · s5b 11.15 · s6 12.10 · s7 13.70 · s8 15.65
bourdon(0.0, 12.10, .5)
gong(0.25, .55)
flute(1.9, [(LA4, .75), (SIB4, .4), (LA4, .35), (SOL4, 1.0)], .55)
taiko(4.30, 1.0)
gong(4.30, .3, base=73)
souffle(5.6, .5, .5)
for t, g in [(5.90, .9), (6.50, .6), (6.95, .65), (7.25, .7), (7.48, .75), (7.66, .8), (7.80, .85), (7.92, .9)]:
    taiko(t, g)
montee(6.4, 1.65, .55)
impact(8.05, 1.1)
choc_katana(8.05, .9)
taiko(8.05, 1.0, .9)
for t, g in [(8.60, .7), (8.95, .55), (9.15, .7), (9.50, .55), (9.70, .75), (9.90, .85)]:
    taiko(t, g)
souffle(9.85, .35, .7)
lame(10.13, .8)
taiko(10.13, .8)
souffle(10.85, .35, .7)
lame(11.15, .8)
choc_katana(11.18, .5)
taiko(11.15, .7)
taiko(11.55, .6)
taiko(11.80, .8)
impact(12.10, 1.2, 1.8)
taiko(12.10, 1.0, .8)
acouphene(12.25, 1.4, .06)
taiko(12.75, .35, .7)
taiko(13.05, .3, .7)
bourdon(13.70, DUREE, .4, entree=1.2, sortie=.8)
gong(13.70, .35, base=130)
flute(13.95, [(RE5, .5), (SIB4, .45), (LA4, .9)], .5)
impact(15.65, 1.0)
taiko(15.65, 1.0)
choc_katana(15.65, .6)
gong(15.65, .6, duree=3.7)
taiko(16.20, .5)
taiko(16.45, .6)

# ---------------------------------------------------------------- normalisation + fondu final
crete = max(abs(x) for x in buf) or 1.0
fin = int((DUREE - .8) * SR)
for i in range(N):
    v = buf[i] / crete * .89
    if i > fin:
        v *= (N - i) / (N - fin)
    buf[i] = v


def main():
    SORTIE.mkdir(exist_ok=True)
    wav = SORTIE / "bande-son.wav"
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(array("h", (int(max(-1, min(1, x)) * 32767) for x in buf)).tobytes())
    print("Son :", wav)
    clip = SORTIE / "clip-ronin-of-the-black-sun.mp4"
    if clip.exists():
        sortie = SORTIE / "clip-ronin-of-the-black-sun-son.mp4"
        # Réverbération (échos multiples), stéréo légèrement élargie, volume normalisé pour les réseaux
        filtre = ("aecho=0.8:0.6:43|89|157|263:0.32|0.22|0.15|0.1,"
                  "pan=stereo|c0=c0|c1=c0,aformat=channel_layouts=stereo,"
                  "adelay=0|11,loudnorm=I=-14:TP=-1.5:LRA=18")  # 11 ms de décalage à droite : effet stéréo
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip), "-i", str(wav), "-af", filtre,
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                        "-movflags", "+faststart", str(sortie)], check=True)
        print("Clip avec son :", sortie)


if __name__ == "__main__":
    main()
