# Flexarion — site officiel

Site du studio **Flexarion** (studio de jeux vidéo indépendant, Aix-en-Provence) et de son jeu **Ronin of the Black Sun**, un souls-like de science-fiction où l'on incarne un ronin dans l'espace.

En ligne : https://studio-flexarion.github.io/

Projet du BUT Informatique (IUT d'Aix-Marseille) : Jean Damez, Wanis Said Boutabouzi, Rayan Keokham, Aymen El Mestari.

## Organisation

| Élément | Rôle |
|---|---|
| `_build/build.py` | Générateur : **tous les textes du site** (pages, devlogs, FAQ, équipe, Daimyō). |
| `_build/art.py` | Génère les illustrations SVG de `assets/img/`. |
| `assets/css/style.css` | Direction artistique « encre et braise » et animations. |
| `assets/js/main.js` | Braises, parallaxe, apparitions, liste des Daimyō, visionneuse. |
| `*.html`, `devlog/`, `sitemap.xml`, `robots.txt`, `devlog/feed.xml` | Fichiers générés : ne pas les modifier à la main. |
| `googlecc9ad28a92dc6802.html` | Validation Google Search Console : **ne jamais supprimer**. |

Le dossier `_build/` n'est pas publié par GitHub Pages (les dossiers commençant par `_` sont ignorés).

## Modifier le site

```bash
python3 _build/build.py
```

Puis `git add -A && git commit -m "…" && git push`. Le site est en ligne 1 à 2 minutes plus tard.

- **Ajouter un devlog** : ajoutez une entrée **en tête** de la liste `POSTS` dans `_build/build.py`. Le sitemap, le flux RSS, l'accueil et la navigation se mettent à jour seuls. Pensez ensuite à créer l'image de partage `assets/img/og-devlog-NN.png`, et à demander l'indexation de la nouvelle page dans Search Console.
- **Ajouter un réseau social** : renseignez son URL dans `SOCIALS`. Il apparaîtra dans le pied de page, la page contact et les données structurées.
- **Régénérer les illustrations** : `python3 _build/art.py`.

## SEO déjà en place

- « Flexarion » dans chaque titre, H1, meta description et texte alternatif, de façon naturelle (pas de bourrage).
- Mots-clés secondaires : souls-like, action-RPG, science-fiction, ronin, samouraï, studio de jeux vidéo indépendant, Aix-en-Provence.
- Données structurées : `Organization`, `WebSite`, `VideoGame`, `FAQPage` (accueil et jeu), `Blog`, `BlogPosting`, `BreadcrumbList`, `AboutPage`, `ContactPage`.
- Open Graph et Twitter, avec une image de partage par page.
- Sitemap, robots.txt, flux RSS, canonical, page 404 en `noindex`.
- Les anciennes adresses (Maestral) redirigent vers les nouvelles pages.
