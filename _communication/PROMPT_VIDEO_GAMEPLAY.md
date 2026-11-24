# Prompt vidéo « gameplay » — Ronin of the Black Sun · Studio Flexarion

Pour générer une fausse vidéo de gameplay façon souls-like avec une IA vidéo (Kling, Hailuo, Veo dans Gemini, Runway, Luma…).

> ⚠️ Le résultat montrera un jeu qui n'existe pas. Publiez-le comme **« concept vidéo généré par IA »**, activez l'étiquette « contenu IA » des réseaux, et notez les prompts dans votre **journal d'usage de l'IA**.

## 1. Méthode recommandée (meilleur résultat)

1. **Images d'abord** : générez une image fixe par plan (Google ImageFX / Gemini, Leonardo…) avec les prompts de la partie 4. Joignez la planche de référence pour garder le style.
2. **Puis animation** : importez chaque image dans un outil **image → vidéo** (Kling ou Hailuo, crédits gratuits) avec le prompt de mouvement du même plan. Comptez 5 à 10 s par plan.
3. **Montage** dans CapCut : enchaînez les plans, ajoutez `bande-son.wav` ou un son tendance.
4. **Interface de jeu** : les IA dessinent mal les barres de vie. Générez la vidéo **sans interface**, puis envoyez-la-moi : j'y ajoute l'interface du jeu (barres de vie et de posture, nom du boss, Cendres d'étoile) avec ffmpeg.

Méthode rapide : un seul **prompt maître** (partie 3) dans un outil texte → vidéo (Veo dans Gemini, Kling, Hailuo).

## 2. Images de référence à joindre

Toutes ces images sont dans `_communication/visuels/` et `assets/img/`.

| Fichier | À utiliser comme |
|---|---|
| `30-planche-reference-ia.png` | **Référence de style** (palette, ambiance, cadrage) : toujours la joindre |
| `assets/img/flexarion-ronin-soleil-noir.svg` (ou `10-instagram-annonce-carre.png` si l'outil refuse le SVG) | **Référence personnage** (le ronin et le soleil noir) |
| `01-gameplay-combat-boss.png` | **Référence boss et cadrage de combat** |
| `02-gameplay-duel-apesanteur.png` | **Référence du combat en apesanteur** |
| `03-gameplay-exploration-torii.png` | **Référence du sanctuaire** (torii doré) |

Selon l'outil : Kling (« Elements » ou « Image reference »), Hailuo (« Subject reference »), Gemini (joindre les images au message), Runway (« References »).

Ajoutez cette phrase au début du prompt quand vous joignez la planche :
```
Use the attached reference board for the art direction, color palette and character design. Keep the same character in every shot.
```

## 3. Prompt maître (texte → vidéo, 8 à 10 s)

```
Gameplay footage of a dark fantasy souls-like third-person action RPG set in outer space.
The over-the-shoulder camera follows a lone ronin samurai — wide straw kasa hat, tattered black and crimson cloak, white sash, katana with a golden tsuba — walking slowly across a shattered stone bridge floating in deep space, toward a colossal Japanese pagoda castle orbiting a purple planet. A giant black eclipse sun with a blazing golden corona dominates the sky. Embers and ash drift weightlessly.
Suddenly a colossal armored samurai warlord lands in front of him, shaking the ground: crescent-shaped kabuto horns, glowing red eyes, a golden halo behind his back. The boss raises a massive sword that glows red to telegraph the attack. The ronin parries at the very last moment: a burst of golden sparks and a bright crescent of light, a brief slow motion, then he dodge-rolls behind the boss and slashes.
Camera lock-on on the boss, subtle camera shake on impacts, motion blur, cinematic volumetric lighting.
Color palette: ink black, deep crimson, vermilion red, old gold, ash white.
Looks like a real Unreal Engine 5 gameplay capture, 60 fps, highly detailed, realistic materials, no text, no user interface.
Audio: deep taiko drums, howling wind, metallic katana clash, distant temple gong.
```

**Prompt négatif** (champ « negative prompt » quand il existe) :
```
text, subtitles, watermark, logo, user interface, health bar, blurry, low resolution, distorted face, extra limbs, extra fingers, broken sword, modern clothing, guns, cartoon, anime style, flickering, morphing
```

## 4. Plan par plan (pour un trailer de 30 à 45 s)

À chaque plan, **recopiez la description du héros mot pour mot** :
`a lone ronin samurai wearing a wide straw kasa hat, tattered black and crimson cloak, white sash, katana with a golden tsuba`

**Plan 1 — Exploration (6 s)**
- Image : `Third-person gameplay view from behind of [HÉROS] walking on a broken stone bridge floating in space, a gigantic pagoda castle orbiting a purple planet ahead, black eclipse sun with golden corona, ash drifting, dark fantasy samurai sci-fi, Unreal Engine 5 gameplay screenshot`
- Mouvement : `slow over-the-shoulder tracking shot, the ronin walks forward, cloak fluttering in the wind, embers floating upward, camera slightly bobbing like a third-person game camera`

**Plan 2 — Apparition du boss (6 s)**
- Image : `Low angle shot of a colossal armored samurai warlord with crescent-shaped kabuto horns and glowing red eyes landing in a ruined orbital throne hall, golden halo behind him, the small ronin in the foreground seen from behind`
- Mouvement : `the giant boss lands heavily, dust and sparks explode, camera shakes, the boss slowly raises his head and his eyes ignite red, the camera pushes in slowly`

**Plan 3 — Parade parfaite « Contre-lune » (5 s)**
- Image : `Close combat moment, the ronin parrying the giant red glowing sword of the warlord with his katana, explosion of golden sparks, bright crescent arc of light`
- Mouvement : `the boss strikes down, the ronin parries at the last frame, slow motion for one second, golden sparks burst in all directions, then normal speed as the ronin counterattacks`

**Plan 4 — Duel en apesanteur (6 s)**
- Image : `Two samurai fighting in zero gravity among floating metal debris and broken torii gates, one upside down, bright katana light trails, deep space and black eclipse sun`
- Mouvement : `the ronin pushes off a floating debris and dashes toward the enemy, the camera orbits around them, debris rotating slowly, blades clash with a flash of light`

**Plan 5 — La mort, façon souls-like (5 s)**
- Image : `The ronin kneeling and defeated in front of the giant boss, his katana planted in the ground, his body slowly turning into glowing embers, dark red atmosphere`
- Mouvement : `the ronin falls to one knee, his body dissolves into golden embers that float away, the screen slowly darkens to red`

**Plan 6 — Le sanctuaire (5 s)**
- Image : `A glowing golden torii gate floating alone in deep space, the ronin kneeling in meditation before it, embers rising like fireflies, sacred and peaceful atmosphere`
- Mouvement : `gentle camera push-in, the torii glows brighter, embers swirl around the kneeling ronin, he slowly stands up and grips his katana`

**Plan 7 — Plan final pour le titre (5 s)**
- Image : `Epic wide shot from behind, the ronin standing on a cliff facing a massive black eclipse sun with a golden corona, seven pagoda castles floating in the sky, large empty dark area at the top of the frame for a title`
- Mouvement : `very slow camera rise, cloak and hat ribbons moving in the wind, the eclipse corona pulsing, embers drifting`

Ajoutez à la fin de chaque prompt :
`dark fantasy samurai science-fiction, color palette of ink black, deep crimson, vermilion red, old gold and ash white, cinematic volumetric lighting, Unreal Engine 5 gameplay capture, highly detailed, no text, no UI`

## 5. Conseils pour un rendu vraiment « gameplay »

- **Mots qui font « jeu vidéo »** : `third-person over-the-shoulder camera`, `lock-on`, `dodge roll`, `gameplay capture`, `video game footage`, `60 fps`, `motion blur`. Sans eux, l'IA fait plutôt un film.
- **N'écrivez pas de noms de jeux** (Elden Ring, Sekiro…) : beaucoup d'outils bloquent les marques, et le résultat ressemblerait trop à un jeu existant. Décrivez plutôt le style : *souls-like, dark fantasy, third-person action RPG*.
- **Formats** : 16:9 pour YouTube et X ; 9:16 pour TikTok et les Reels (ajoutez `vertical 9:16 composition`).
- **Générez 3 ou 4 variantes** par plan et gardez la meilleure : les IA vidéo ratent souvent les mains et les sabres.
- **Cohérence** : même description du héros, même planche de référence et même graine (« seed ») quand l'outil le permet.
- **Durée** : 5 à 6 s par plan, c'est ce qui marche le mieux ; au-delà, l'image se déforme.

## 6. Légende de publication

> 🎬 Concept vidéo de *Ronin of the Black Sun*, le souls-like de science-fiction du studio Flexarion (images et animations générées par IA à partir de nos concept arts). Le vrai jeu est en développement : suivez le devlog, lien en bio.
> #Flexarion #RoninOfTheBlackSun #Soulslike #IndieGame #JeuIndé #AIart #ConceptArt
