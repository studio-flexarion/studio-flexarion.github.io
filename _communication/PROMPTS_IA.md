# Images et vidéos réalistes avec des outils d'IA gratuits

Ronin of the Black Sun · Studio Flexarion

> **Transparence obligatoire** : ces images montreront un jeu qui n'existe pas. Présentez-les comme des **« concept arts générés par IA »** ou des **« maquettes »**, jamais comme de vraies captures. Instagram, TikTok et YouTube demandent d'activer l'étiquette « contenu généré par IA » pour les images réalistes. Notez chaque prompt dans votre **journal d'usage de l'IA** (c'est noté au concours).

## 1. Outils gratuits (offres gratuites à vérifier, elles changent souvent)

### Images
| Outil | Points forts |
|---|---|
| **Google ImageFX / Gemini** | Gratuit avec un compte Google, très bon réalisme |
| **Microsoft Designer / Bing Image Creator** | Gratuit avec un compte Microsoft (DALL·E 3) |
| **Leonardo.ai** | Crédits gratuits chaque jour, styles « cinématique » et « jeu vidéo » |
| **Ideogram** | Offre gratuite, le meilleur pour écrire du texte dans l'image |
| **Adobe Firefly** | Crédits gratuits mensuels, droits d'usage clairs |
| **Draw Things** (Mac App Store) | Gratuit et **local** sur votre Mac M1 (Stable Diffusion), sans compte ni limite, mais plus lent avec 8 Go de RAM |

### Animer une image (image → vidéo)
| Outil | Points forts |
|---|---|
| **Kling AI** | Crédits gratuits quotidiens, très bon rendu cinématique |
| **Hailuo AI (MiniMax)** | Crédits gratuits, mouvements fluides |
| **Luma Dream Machine** | Offre gratuite limitée |
| **Pika** | Crédits gratuits, effets stylisés |

### Montage de l'« edit »
- **CapCut** (gratuit, ordinateur et téléphone) : modèles d'edit, synchronisation automatique sur le rythme, transitions. Le plus simple pour TikTok et les Reels.
- **DaVinci Resolve** (gratuit) : niveau professionnel, si quelqu'un veut aller plus loin.
- **Musique libre de droits** : Bibliothèque audio YouTube, Pixabay Music. Sur TikTok et Instagram, vous pouvez aussi utiliser un son tendance directement dans l'application.

### La solution la plus « vraie » : de vraies captures
**Unreal Engine 5** est gratuit, et la plateforme **Fab** propose des décors et personnages gratuits (environnements japonais, samouraïs, effets de particules). En une ou deux séances, vous pouvez poser un personnage dans un décor et faire de **vraies** captures et vidéos. C'est honnête, et c'est un excellent sujet de devlog.

## 2. Garder un style cohérent

Collez **toujours** ces deux blocs, en anglais (les outils comprennent mieux l'anglais).

**Le héros (à reprendre à l'identique dans chaque prompt)** :
```
a lone ronin samurai wearing a wide straw kasa hat, tattered black and crimson cloak, white sash, katana with a golden tsuba
```

**Le style** :
```
dark fantasy samurai science-fiction, giant black eclipse sun with a golden corona in the sky, color palette of ink black, deep crimson, vermilion red, old gold and ash white, cinematic volumetric lighting, floating embers, third-person action RPG gameplay screenshot, Unreal Engine 5 render, highly detailed, 16:9
```

**À éviter** (champ « negative prompt » quand il existe) :
```
text, watermark, logo, user interface, blurry, low quality, extra fingers, deformed hands, modern clothes, guns
```

## 3. Prompts d'images (« preview de gameplay »)

1. **Plan d'ouverture**
   > Third-person view from behind of [HÉROS] standing on a broken stone bridge in space, looking at a gigantic Japanese pagoda castle floating above a purple planet, [STYLE]

2. **Combat de boss**
   > [HÉROS] parrying the giant sword of a colossal armored samurai warlord with crescent-shaped kabuto horns and glowing red eyes, golden sparks exploding at the clash, ruined throne hall of a space station, [STYLE]

3. **Duel en apesanteur**
   > Two samurai fighting in zero gravity among floating metal debris and broken torii gates, one upside down, a bright arc of light from a katana slash, deep space background, [STYLE]

4. **Sanctuaire (point de sauvegarde)**
   > A glowing golden torii gate floating alone in deep space, [HÉROS] kneeling in meditation before it, embers rising like fireflies, peaceful and sacred atmosphere, [STYLE]

5. **Exploration**
   > [HÉROS] walking through a long abandoned corridor of an orbital Japanese temple, paper lanterns, shoji walls cracked open to reveal stars, ash falling like snow, [STYLE]

6. **Gros plan sur l'arme**
   > Extreme close-up of a katana forged from dead star metal, glowing golden cracks along the blade, reflection of a black eclipse sun, embers, macro shot, [STYLE]

7. **Affiche (format vertical 9:16)**
   > Epic vertical movie poster, [HÉROS] seen from behind facing a massive black eclipse sun with golden corona, seven pagoda castles floating in the sky, [STYLE], 9:16

## 4. Prompts vidéo (image → vidéo, 5 secondes chacun)

Importez une image générée, puis :

- **Plan 1** : `slow cinematic dolly-in toward the ronin, cloak fluttering in the wind, embers drifting upward, eclipse corona slowly pulsing`
- **Plan 2** : `the warlord raises his giant sword and strikes, the ronin parries at the last moment, burst of golden sparks, camera shake, slow motion`
- **Plan 3** : `camera orbits around the two fighters floating in zero gravity, debris rotating slowly, katana light trail`
- **Plan 4** : `the torii gate glows brighter, embers swirl around the kneeling ronin, gentle camera push-in`
- **Plan 6** : `slow camera pan along the katana blade, golden cracks glowing, sparks flying`

## 5. Montage de l'edit (15 à 25 s, format 9:16)

| Temps | Plan | Effet |
|---|---|---|
| 0–2 s | Écran noir, texte « Le Soleil Noir s'est éteint. » | Fondu, son grave |
| 2–5 s | Plan 1 (ronin face au château) | Zoom lent |
| 5–6 s | Plan 6 (gros plan du katana) | Coupe sèche sur le temps fort |
| 6–10 s | Plan 2 (boss, parade) | Flash blanc à l'impact, ralenti |
| 10–13 s | Plan 3 (duel en apesanteur) | Rotation, coupes rapides sur le rythme |
| 13–15 s | Écran « TOMBÉ AU COMBAT » (visuel 04) | Coupure du son, une seconde de silence |
| 15–18 s | Plan 4 (torii) | Retour de la musique |
| 18–22 s | Visuel 11 (titre « RONIN OF THE BLACK SUN ») | Texte « Un jeu du studio Flexarion · Lien en bio » |

Dans CapCut : *Nouveau projet* → importez les clips → *Beat* (synchronisation automatique) → *Transitions* : « Flash » ou « Glitch » → *Texte* : police serif dorée → exportez en 1080×1920, 30 i/s.
