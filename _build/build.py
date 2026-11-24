#!/usr/bin/env python3
"""
Générateur du site Flexarion (studio + jeu).

    python3 _build/build.py

Écrit toutes les pages HTML, le sitemap, le robots.txt et le flux RSS à la racine
du dépôt (servi par GitHub Pages). Le dossier _build/ n'est pas publié.
Pour modifier un texte : changez-le ici, relancez la commande, puis poussez.
"""
import json
from datetime import date, datetime, timezone
from email.utils import format_datetime
from html import escape
from pathlib import Path

SITE = "https://studio-flexarion.github.io"
EMAIL = "flexarioncontact@gmail.com"
ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()

# Renseignez l'URL d'un réseau dès que le compte existe : il apparaîtra sur le site
# et dans les données structurées (sameAs).
SOCIALS = [
    ("Instagram", ""), ("TikTok", ""), ("X / Twitter", ""), ("YouTube", ""),
    ("Discord", ""), ("itch.io", ""), ("LinkedIn", ""),
]

TEAM = [
    ("麻", "Maëlle Roux", "Cofondatrice · Direction créative",
     "Ancienne illustratrice, elle écrit l'univers de Ronin of the Black Sun et sa mythologie du Soleil Noir. Elle dessine encore chaque Daimyō à l'encre avant qu'il ne passe en 3D.",
     "devlog/un-ronin-dans-l-espace-souls-like-science-fiction.html"),
    ("義", "Idriss Benhamou", "Cofondateur · Programmation",
     "Architecte du système de combat et de l'apesanteur. Refuse de livrer une attaque qui ne répond pas en moins de cent millisecondes.",
     "devlog/parade-posture-apesanteur-systeme-de-combat.html"),
    ("刀", "Clément Astier", "Cofondateur · Game design",
     "Pratiquant de kendo depuis l'adolescence, il règle chaque parade et chaque fenêtre d'esquive pour que la mort soit toujours méritée.",
     "devlog/parade-posture-apesanteur-systeme-de-combat.html"),
    ("墨", "Soraya Khelifi", "Direction artistique",
     "Elle a imposé l'encre, l'or et le vermillon. Peint les décors du jeu comme on peint un ensō : d'un seul geste, ou pas du tout.",
     "devlog/direction-artistique-encre-or-et-vide.html"),
    ("音", "Théo Vannier", "Musique · Design sonore",
     "Mêle shakuhachi, taiko et synthétiseurs modulaires. Il a enregistré le choc des lames dans une forge de la vallée de l'Arc.",
     None),
    ("道", "Lina Marchetti", "Production · Relations presse",
     "Garde le cap du planning sans jamais faire crunch l'équipe. Votre interlocutrice pour la presse, les partenariats et les playtests.",
     None),
]

DAIMYOS = [
    ("錆", "La Daimyō de la Rouille", "Maîtresse du Shiro-Ferraille, elle a fondu ses propres samouraïs pour en faire une armure qui ne cesse de grandir. Premier vrai mur du jeu : on apprend contre elle que la parade vaut mieux que la fuite."),
    ("潮", "Le Daimyō de la Marée stellaire", "Il combat en apesanteur, porté par des courants de poussière d'étoile. Son arène n'a ni sol ni plafond : chaque débris peut devenir un appui."),
    ("燈", "La Dame aux Mille Lanternes", "Elle éteint et rallume la lumière de son château à volonté. Dans le noir, seule la lueur de votre lame trahit sa position, et la vôtre."),
    ("響", "Le Daimyō de l'Écho", "Chacune de vos attaques lui revient en écho trois secondes plus tard. Pour le vaincre, il faut se battre contre soi-même."),
    ("霜", "La Daimyō du Givre", "Gardienne d'un shiro figé dans la glace du vide. Ses coups ralentissent le temps autour de vous, et votre propre posture se fige."),
    ("灰", "Le Daimyō des Cendres", "Ancien maître d'armes de votre clan. Il connaît vos techniques mieux que vous, et vous attend depuis trois cents ans."),
    ("蝕", "Le Shogun du Soleil Noir", "Il a scellé la lumière de l'étoile pour en faire une arme. Personne n'a vu son visage depuis la Grande Éclipse."),
]

POSTS = [
    {
        "slug": "direction-artistique-encre-or-et-vide",
        "num": "03", "date": "2026-11-24",
        "titre": "Direction artistique : l'encre, l'or et le vide",
        "title": "Direction artistique de Ronin of the Black Sun : l'encre, l'or et le vide — Devlog 03",
        "description": "Comment le studio Flexarion a créé la direction artistique de son souls-like de science-fiction : palette encre et braise, silhouettes de samouraïs et soleil noir.",
        "chapo": "Six couleurs, des silhouettes lisibles à dix mètres et un soleil qui ne brille plus : les règles qui donnent son identité visuelle à Ronin of the Black Sun.",
        "auteur": "Soraya Khelifi", "role": "Direction artistique", "sceau": "墨",
        "image": "flexarion-palette-encre-et-braise.svg", "w": 1200, "h": 630,
        "alt": "La palette encre et braise de Ronin of the Black Sun : six bandes de couleur à côté d'un ensō peint à l'encre et d'un ronin",
        "minutes": 6, "tags": ["Direction artistique", "Univers"],
        "corps": """
<p>Quand nous avons commencé <em>Ronin of the Black Sun</em>, la question n'était pas « à quoi ressemble un samouraï dans l'espace ? », mais « comment éviter qu'il ressemble à tous les autres ? ». La science-fiction a ses néons, la fantasy sombre ses cathédrales. Nous voulions autre chose : une estampe japonaise qu'on aurait laissée brûler au bord d'un trou noir.</p>

<h2>Six couleurs, pas une de plus</h2>
<p>Toute l'image du jeu tient dans une palette de six teintes, que nous appelons « encre et braise ». Chaque couleur a un rôle précis, et nous refusons d'en ajouter une septième.</p>
<div class="tableau"><table>
  <thead><tr><th scope="col">Couleur</th><th scope="col">Code</th><th scope="col">Rôle dans le jeu</th></tr></thead>
  <tbody>
    <tr><th scope="row">Encre</th><td>#08070b</td><td>Le vide, les silhouettes, tout ce qui menace</td></tr>
    <tr><th scope="row">Vide</th><td>#1a1530</td><td>La profondeur de l'espace, les zones sans gravité</td></tr>
    <tr><th scope="row">Sang séché</th><td>#5a0f14</td><td>Les terres du Shogunat, la corruption</td></tr>
    <tr><th scope="row">Vermillon</th><td>#b8322a</td><td>Le danger, les sceaux, les coups critiques</td></tr>
    <tr><th scope="row">Or ancien</th><td>#c9a45c</td><td>La lumière captive du Soleil Noir, les Torii de repos</td></tr>
    <tr><th scope="row">Cendre</th><td>#e8e1d3</td><td>La lame du ronin, l'interface, le texte</td></tr>
  </tbody>
  <caption>La palette « encre et braise » de Ronin of the Black Sun.</caption>
</table></div>
<p>La règle la plus importante : <strong>le vermillon signifie toujours le danger</strong>. Si un élément est rouge, il peut vous tuer. Les joueurs l'apprennent en quelques minutes, sans le moindre tutoriel.</p>

<h2>Lire une silhouette à dix mètres</h2>
<p>Dans un souls-like, comprendre un ennemi avant qu'il ne frappe est une question de survie. Chaque adversaire de Ronin of the Black Sun doit donc être reconnaissable <em>en silhouette pure</em>, en noir sur fond clair. Nous imprimons nos personnages en vignettes de deux centimètres : si l'équipe ne devine pas leur arme et leur attaque principale, le design repart à zéro.</p>
<p>C'est pour cela que les Daimyō du Vide portent des casques démesurés, des cornes en croissant et des bannières dans le dos : ce sont des formes qu'on lit de loin, même dans le chaos d'un combat en apesanteur.</p>

<figure class="cadre"><div class="cadre__img"><img src="../assets/img/flexarion-daimyo-du-vide-boss.svg" alt="Silhouette d'un Daimyō du Vide, casque à cornes en croissant et yeux rouges, devant un halo doré" width="1200" height="700" loading="lazy"></div>
<figcaption>Un Daimyō du Vide : une forme lisible avant d'être un personnage.</figcaption></figure>

<h2>L'encre comme matière</h2>
<p>Nos textures ne cherchent pas le réalisme. Les rochers, les armures et même les nébuleuses sont peints avec des coups de pinceau inspirés du <strong>sumi-e</strong>, la peinture japonaise à l'encre. Les bords sont irréguliers, l'encre « bave » légèrement : en jeu, cela donne l'impression de traverser un rouleau peint plutôt qu'une simulation spatiale.</p>
<p>Le motif central est le <strong>Soleil Noir</strong> : une éclipse permanente, un disque d'encre cerclé d'or. On le voit depuis presque tous les lieux du jeu, comme la Sainte-Victoire se voit depuis presque tout le pays d'Aix. Ce n'est pas un hasard.</p>

<h2>Ce que nous avons abandonné</h2>
<ul>
  <li><strong>Le bleu néon</strong> : trop associé à la science-fiction « cyberpunk », il effaçait le côté japonais ancien.</li>
  <li><strong>Les casques fermés pour le héros</strong> : le chapeau de paille du ronin raconte mieux sa solitude qu'une visière.</li>
  <li><strong>Le photoréalisme</strong> : hors de portée pour une équipe de six, et contraire à l'idée d'estampe.</li>
</ul>

<h2>Et ensuite ?</h2>
<p>Le prochain devlog sera consacré à la musique du jeu : shakuhachi, taiko et synthétiseurs. En attendant, découvrez <a href="../jeu.html#univers">l'univers complet du jeu</a> ou relisez <a href="parade-posture-apesanteur-systeme-de-combat.html">notre devlog sur le système de combat</a>.</p>
""",
    },
    {
        "slug": "parade-posture-apesanteur-systeme-de-combat",
        "num": "02", "date": "2026-11-05",
        "titre": "Parade, posture et apesanteur : le système de combat",
        "title": "Le système de combat de Ronin of the Black Sun : parade, posture et apesanteur — Devlog 02",
        "description": "Fenêtres de parade, barre de posture et duels au katana en apesanteur : le studio Flexarion détaille le système de combat de son souls-like de samouraï.",
        "chapo": "Dix images pour parer, une barre de posture à briser et des combats sans sol ni plafond : comment nous avons conçu les duels au katana de Ronin of the Black Sun.",
        "auteur": "Clément Astier", "role": "Game design", "sceau": "刀",
        "image": "flexarion-duel-apesanteur-katana.svg", "w": 1200, "h": 700,
        "alt": "Deux samouraïs s'affrontent au katana en apesanteur au milieu de débris, tranchés par un arc de lumière",
        "minutes": 7, "tags": ["Game design", "Programmation"],
        "corps": """
<p><em>Ronin of the Black Sun</em> est un jeu de duels. Pas de fusil, pas de vaisseau à piloter : un ronin, une lame et des adversaires qui en savent souvent plus que vous. Tout le jeu repose donc sur une question : <strong>qu'est-ce qui rend un coup de katana satisfaisant ?</strong> Après huit mois de prototypes, voici notre réponse.</p>

<h2>La parade parfaite : la « Contre-lune »</h2>
<p>Lever sa garde au bon moment ne protège pas seulement : cela renvoie l'énergie du coup vers l'attaquant. Nous appelons cette parade parfaite la <strong>Contre-lune</strong>, en référence à l'arc de lumière qu'elle dessine.</p>
<p>La fenêtre est volontairement courte, mais pas cruelle : <strong>10 images à 60 images par seconde</strong>, soit environ 167 millisecondes. En dessous de 8 images, nos testeurs avaient l'impression de jouer à la loterie ; au-dessus de 12, la parade devenait automatique.</p>
<div class="tableau"><table>
  <thead><tr><th scope="col">Action</th><th scope="col">Fenêtre</th><th scope="col">Effet</th></tr></thead>
  <tbody>
    <tr><th scope="row">Contre-lune (parade parfaite)</th><td>10 images (~167 ms)</td><td>Aucun dégât, forte perte de posture pour l'ennemi</td></tr>
    <tr><th scope="row">Garde simple</th><td>Maintenue</td><td>Dégâts réduits, mais votre posture baisse</td></tr>
    <tr><th scope="row">Pas du Vide (esquive)</th><td>14 images d'invulnérabilité</td><td>Repositionnement, coûte de l'endurance</td></tr>
    <tr><th scope="row">Coup de l'Éclipse</th><td>Posture ennemie brisée</td><td>Coup fatal ou très lourds dégâts sur un boss</td></tr>
  </tbody>
  <caption>Les fenêtres de combat de Ronin of the Black Sun, version de novembre 2026.</caption>
</table></div>

<h2>La posture : briser la garde plutôt que la vie</h2>
<p>Chaque combattant a une barre de vie et une <strong>barre de posture</strong>. Les parades parfaites, les coups lourds et les attaques dans le dos remplissent la posture adverse. Quand elle est pleine, la garde se brise et vous pouvez porter le <strong>Coup de l'Éclipse</strong>.</p>
<p>Dans le moteur, la résolution d'un coup reçu tient en quelques lignes :</p>
<pre><code><span class="c">// Résolution d'une attaque reçue pendant la garde</span>
<span class="k">EResultat</span> <span class="f">UComposantDuel::ResoudreCoup</span>(<span class="k">const</span> FCoup&amp; Coup)
{
    <span class="k">const float</span> Delai = Coup.InstantImpact - InstantDebutGarde;
    <span class="k">if</span> (Delai &gt;= <span class="n">0.f</span> &amp;&amp; Delai &lt;= FenetreContreLune)   <span class="c">// 10 images à 60 i/s</span>
    {
        Coup.Attaquant-&gt;AjouterPosture(Coup.Degats * <span class="n">1.5f</span>);
        <span class="k">return</span> EResultat::ContreLune;
    }
    Posture += Coup.Degats * <span class="n">0.6f</span>;                     <span class="c">// la garde simple use votre posture</span>
    <span class="k">return</span> Posture &gt;= PostureMax ? EResultat::GardeBrisee : EResultat::Bloque;
}</code></pre>
<p>Le détail important est le multiplicateur de 1,5 : une parade parfaite fait plus mal à la posture de l'ennemi que la plupart de vos attaques. Le jeu récompense la lecture de l'adversaire, pas l'agressivité.</p>

<h2>Se battre sans sol : l'apesanteur</h2>
<p>Plusieurs zones du jeu se déroulent dans le vide, entre les débris des châteaux orbitaux. Notre premier prototype de combat en apesanteur était injouable : les joueurs perdaient leurs repères en quelques secondes.</p>
<p>La solution est venue d'une règle simple : <strong>le ronin s'oriente toujours vers son adversaire</strong>. Le « haut » de l'écran devient la direction de la tête du personnage, et le verrouillage de cible garde l'ennemi au centre. Le joueur peut ensuite utiliser le <strong>Pas du Vide</strong> pour se propulser d'un débris à l'autre, et frapper depuis n'importe quel angle.</p>
<blockquote>« Dans le vide, il n'y a ni haut ni bas. Il n'y a que toi, et celui que tu dois vaincre. »</blockquote>

<h2>Difficile, mais jamais injuste</h2>
<p><em>Ronin of the Black Sun</em> est exigeant, et nous l'assumons. Mais nous avons fixé trois règles :</p>
<ul>
  <li>chaque attaque ennemie dangereuse est annoncée par un signal visuel <strong>et</strong> sonore ;</li>
  <li>aucun coup ne peut vous tuer en partant d'une barre de vie pleine, sauf dans les combats facultatifs ;</li>
  <li>des options d'accessibilité (ralentissement du jeu, fenêtres de parade élargies) sont disponibles sans pénalité.</li>
</ul>

<h2>Et ensuite ?</h2>
<p>Dans le prochain devlog, Soraya présentera <a href="direction-artistique-encre-or-et-vide.html">la direction artistique du jeu</a>. Vous pouvez aussi découvrir <a href="../jeu.html#mecaniques">toutes les mécaniques du jeu</a> ou <a href="../contact.html">vous inscrire au prochain playtest</a>.</p>
""",
    },
    {
        "slug": "un-ronin-dans-l-espace-souls-like-science-fiction",
        "num": "01", "date": "2026-10-12",
        "titre": "Un ronin dans l'espace : pourquoi un souls-like de science-fiction",
        "title": "Un ronin dans l'espace : pourquoi Flexarion fait un souls-like de science-fiction — Devlog 01",
        "description": "Premier devlog du studio Flexarion : pourquoi une équipe d'Aix-en-Provence a choisi de faire un souls-like de science-fiction où l'on incarne un ronin.",
        "chapo": "Un croquis à l'encre, une éclipse au-dessus de la Sainte-Victoire et une question : que devient l'honneur d'un samouraï quand son soleil s'éteint ?",
        "auteur": "Maëlle Roux", "role": "Direction créative", "sceau": "麻",
        "image": "flexarion-ronin-soleil-noir.svg", "w": 1600, "h": 900,
        "alt": "Un ronin au chapeau de paille, katana à la main, face à une éclipse dorée et à un torii brisé",
        "minutes": 6, "tags": ["Studio", "Univers"],
        "corps": """
<p>Bienvenue dans le premier devlog de <strong>Flexarion</strong> ! Chaque mois, l'équipe racontera ici la fabrication de notre jeu, <em>Ronin of the Black Sun</em>, avec ses réussites, ses impasses et ses chiffres. Pour commencer, il fallait répondre à la question qu'on nous pose le plus souvent : <em>pourquoi un samouraï dans l'espace ?</em></p>

<h2>Tout est parti d'un croquis</h2>
<p>Pendant une game jam à Aix-en-Provence, sur le thème « l'honneur », j'ai dessiné à l'encre un ronin de dos, face à un soleil éclipsé. Pas de décor, pas d'époque : juste un chapeau de paille, une lame et un disque noir cerclé d'or. Idriss a regardé le dessin et a dit : « Et si ce soleil était une étoile morte, et que le shogun l'avait éteinte lui-même ? » <em>Ronin of the Black Sun</em> venait de naître.</p>

<h2>Pourquoi un souls-like ?</h2>
<p>Parce que le genre raconte exactement ce que vit un ronin : la solitude, l'échec répété, et la maîtrise qui vient lentement. Dans un souls-like, mourir n'est pas une punition, c'est une leçon. Chaque duel perdu vous apprend quelque chose sur votre adversaire, et sur vous-même.</p>
<p>Nous voulions aussi des combats où la <strong>précision</strong> compte plus que les statistiques. Un bon joueur doit pouvoir vaincre un Daimyō du Vide avec l'équipement de départ. C'est difficile, mais c'est possible.</p>

<h2>Pourquoi l'espace ?</h2>
<p>Le Japon féodal et la science-fiction partagent un thème que nous aimons : <strong>la fin d'un monde</strong>. Les samouraïs ont vu disparaître leur ordre ; nos personnages voient s'éteindre leur étoile. L'espace nous offre aussi ce que la Terre ne peut pas donner : des duels en apesanteur, des châteaux qui flottent en orbite et un silence absolu entre deux coups de lame.</p>
<p>Dans <em>Ronin of the Black Sun</em>, le Shogunat de Kurogane a scellé la lumière du Soleil Noir pour en faire une arme. Vous incarnez <strong>Kaïen</strong>, le dernier samouraï du clan Hoshino, exécuté pour avoir refusé d'obéir, puis ramené à la vie trois siècles plus tard par un Torii de lumière.</p>

<figure class="cadre"><div class="cadre__img"><img src="../assets/img/flexarion-shiro-chateau-orbital.svg" alt="Un château orbital en forme de pagode flotte au-dessus d'une planète violette" width="1200" height="700" loading="lazy"></div>
<figcaption>Un Shiro, château orbital du Shogunat de Kurogane.</figcaption></figure>

<h2>Ce que nous ne ferons pas</h2>
<ul>
  <li><strong>Pas de difficulté gratuite</strong> : chaque mort doit être compréhensible.</li>
  <li><strong>Pas de monde ouvert vide</strong> : sept châteaux denses plutôt qu'une carte immense.</li>
  <li><strong>Pas de clichés</strong> : nous travaillons avec des pratiquants de kendo et relisons nos textes japonais avec une traductrice.</li>
</ul>

<h2>Pourquoi depuis Aix-en-Provence ?</h2>
<p>Parce que c'est ici que l'équipe s'est rencontrée, et parce que la Sainte-Victoire nous a donné notre image la plus forte. Un soir, en la regardant se découper sur un ciel rouge, nous avons compris que le Soleil Noir devait être visible depuis tout le jeu, comme la montagne l'est depuis toute la ville. Pour en savoir plus, lisez <a href="../studio.html">l'histoire du studio Flexarion</a>.</p>

<h2>Et ensuite ?</h2>
<p>Le prochain devlog détaillera <a href="parade-posture-apesanteur-systeme-de-combat.html">le système de combat du jeu</a> : parade, posture et apesanteur. D'ici là, découvrez <a href="../jeu.html">le jeu en détail</a>.</p>
""",
    },
]

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def fr_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {MOIS[d.month - 1]} {d.year}"


def url(p=""):
    return f"{SITE}/{p}"


def socials():
    return [(n, u) for n, u in SOCIALS if u]


ORG_ID = url("#organisation")
GAME_ID = url("jeu.html#jeu")
ORGANISATION = {
    "@type": "Organization", "@id": ORG_ID, "name": "Flexarion",
    "alternateName": ["Studio Flexarion", "Flexarion Studio"],
    "url": url(), "logo": url("icon-512.png"), "image": url("assets/img/og-flexarion.png"),
    "description": "Flexarion est un studio de développement de jeux vidéo indépendant spécialisé dans la science-fiction, basé à Aix-en-Provence. Il développe Ronin of the Black Sun, un souls-like où l'on incarne un ronin dans l'espace.",
    "slogan": "Plier sans rompre.", "foundingDate": "2023", "email": EMAIL,
    "address": {"@type": "PostalAddress", "addressLocality": "Aix-en-Provence", "postalCode": "13100",
                "addressRegion": "Provence-Alpes-Côte d'Azur", "addressCountry": "FR"},
    "areaServed": "FR", "numberOfEmployees": {"@type": "QuantitativeValue", "value": 6},
    "knowsAbout": ["Jeu vidéo indépendant", "Science-fiction", "Souls-like", "Action-RPG", "Game design"],
    "sameAs": [u for _, u in socials()],
}
JEU = {
    "@type": "VideoGame", "@id": GAME_ID, "name": "Ronin of the Black Sun", "alternateName": "Ronin of the Black Sun — un jeu du studio Flexarion",
    "url": url("jeu.html"), "image": url("assets/img/og-flexarion.png"),
    "description": "Ronin of the Black Sun, du studio Flexarion, est un action-RPG souls-like de science-fiction : incarnez Kaïen, un ronin ressuscité, et affrontez au katana les Sept Daimyō du Vide pour libérer la lumière du Soleil Noir.",
    "genre": ["Action-RPG", "Souls-like", "Science-fiction", "Samouraï"],
    "gamePlatform": ["PC", "Windows", "Steam Deck"], "playMode": "SinglePlayer",
    "applicationCategory": "Game", "operatingSystem": "Windows",
    "inLanguage": ["fr", "en", "ja"], "contentRating": "PEGI 16 (visé)",
    "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "creator": {"@id": ORG_ID},
    "gameLocation": "Le système de Yomi et les Sept Shiro, en orbite du Soleil Noir",
    "characterAttribute": "Kaïen, ronin du clan Hoshino",
}


def ld(*items):
    return ('<script type="application/ld+json">'
            + json.dumps({"@context": "https://schema.org", "@graph": list(items)}, ensure_ascii=False, separators=(",", ":"))
            + "</script>")


def fil(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)]}


def ariane(items, pre):
    lis = [f'<li><a href="{pre}{p or "index.html"}">{escape(n)}</a></li>' for n, p in items[:-1]]
    lis.append(f'<li aria-current="page">{escape(items[-1][0])}</li>')
    return f'<nav class="ariane revele" aria-label="Fil d\'Ariane"><ol>{"".join(lis)}</ol></nav>'


NAV = [("index.html", "Accueil"), ("jeu.html", "Le jeu"), ("studio.html", "Le studio"),
       ("devlog/index.html", "Devlog"), ("contact.html", "Contact &amp; presse")]

ENTAILLE = ('<div class="entaille" aria-hidden="true"><svg viewBox="0 0 1600 90" preserveAspectRatio="none">'
            '<path d="M-20 74 L1620 14" style="stroke:#b8322a;stroke-width:12;opacity:.25;fill:none"/>'
            '<path d="M-20 74 L1620 14" style="stroke:#e8e1d3;stroke-width:1.6;fill:none"/></svg></div>')


def ornement():
    return '<div class="ornement" aria-hidden="true"><i></i></div>'


def etiquette(kanji, texte):
    return f'<p class="etiquette"><span class="kanji" aria-hidden="true">{kanji}</span>{texte}</p>'


def page(chemin, titre, description, corps, schemas, *, og="assets/img/og-flexarion.png", og_alt=None,
         type_og="website", head_extra="", noindex=False):
    pre = "../" * chemin.count("/")
    courant = ' aria-current="page"'
    nav = "".join(
        f'<li><a href="{pre}{p}"{courant if (p == chemin or (p.startswith("devlog") and chemin.startswith("devlog"))) else ""}>{lbl}</a></li>'
        for p, lbl in NAV)
    reseaux = "".join(f'<li><a href="{escape(u)}" rel="me noopener" target="_blank">{escape(n)}</a></li>' for n, u in socials())
    canon = url("" if chemin == "index.html" else chemin)
    og_alt = og_alt or "Ronin of the Black Sun, le souls-like de science-fiction du studio Flexarion"
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(titre)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="{'noindex, follow' if noindex else 'index, follow, max-image-preview:large'}">
<meta name="author" content="Flexarion">
<meta name="theme-color" content="#08070b">
<meta property="og:site_name" content="Flexarion">
<meta property="og:locale" content="fr_FR">
<meta property="og:type" content="{type_og}">
<meta property="og:title" content="{escape(titre)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{url(og)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{escape(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(titre)}">
<meta name="twitter:description" content="{escape(description)}">
<meta name="twitter:image" content="{url(og)}">
{head_extra}<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{pre}icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="Devlog Flexarion" href="{url('devlog/feed.xml')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&amp;family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&amp;family=Shippori+Mincho:wght@800&amp;display=swap">
<link rel="stylesheet" href="{pre}assets/css/style.css">
<script>document.documentElement.classList.add("js")</script>
{schemas}
</head>
<body>
<a class="skip-link" href="#contenu">Aller au contenu</a>
<header class="entete">
  <div class="container entete__in">
    <a class="marque" href="{pre}index.html" aria-label="Flexarion, retour à l'accueil">
      <img src="{pre}assets/img/flexarion-logo.svg" alt="" width="40" height="40"><span>FLEXARION</span>
    </a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu"><span></span><b class="sr-only">Menu</b></button>
    <nav class="nav" id="menu" aria-label="Navigation principale"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="contenu">
{corps}
</main>
<footer class="pied">
  <div class="container">
    <div class="pied__grille">
      <div>
        <a class="marque" href="{pre}index.html"><img src="{pre}assets/img/flexarion-logo.svg" alt="" width="40" height="40"><span>FLEXARION</span></a>
        <p style="margin-top:18px"><strong>Flexarion</strong> est un studio de jeux vidéo indépendant de science-fiction, installé à Aix-en-Provence. Il développe Ronin of the Black Sun, un souls-like où l'on incarne un ronin dans l'espace.</p>
      </div>
      <nav aria-label="Plan du site">
        <h2>Explorer</h2>
        <ul><li><a href="{pre}jeu.html">Ronin of the Black Sun</a></li><li><a href="{pre}studio.html">Le studio</a></li><li><a href="{pre}devlog/index.html">Devlog</a></li><li><a href="{pre}contact.html">Contact &amp; presse</a></li></ul>
      </nav>
      <nav aria-label="Le jeu">
        <h2>Le jeu</h2>
        <ul><li><a href="{pre}jeu.html#univers">L'univers</a></li><li><a href="{pre}jeu.html#mecaniques">Le combat</a></li><li><a href="{pre}jeu.html#daimyos">Les Sept Daimyō</a></li><li><a href="{pre}jeu.html#faq">FAQ du jeu</a></li></ul>
      </nav>
      <div>
        <h2>Le studio</h2>
        <address>Flexarion<br>13100 Aix-en-Provence<br>Provence, France<br><a href="mailto:{EMAIL}">{EMAIL}</a></address>
        <ul style="margin-top:14px">{reseaux}<li><a href="{pre}devlog/feed.xml">Flux RSS du devlog</a></li></ul>
      </div>
    </div>
    <div class="pied__bas">
      <span>© {date.today().year} Flexarion — studio fictif imaginé pour un projet du BUT Informatique d'Aix-en-Provence.</span>
      <a href="{pre}mentions-legales.html">Mentions légales</a>
    </div>
  </div>
</footer>
<script src="{pre}assets/js/main.js" defer></script>
</body>
</html>
"""


def carte_billet(p, pre, h="h3", delai=0):
    return f'''<article class="carte revele" style="--delai:{delai}s"><a class="billet" href="{pre}devlog/{p["slug"]}.html">
  <div class="billet__img"><img src="{pre}assets/img/{p["image"]}" alt="{escape(p["alt"])}" width="{p["w"]}" height="{p["h"]}" loading="lazy"></div>
  <p class="meta"><span>Devlog {p["num"]}</span><time datetime="{p["date"]}">{fr_date(p["date"])}</time></p>
  <{h}>{escape(p["titre"])}</{h}>
  <p>{escape(p["chapo"])}</p>
  <span class="lire">Lire le devlog →</span>
</a></article>'''


def faq_bloc(items, ident):
    html = "".join(f'<details class="revele"><summary><h3>{escape(q)}</h3></summary><div><p>{a}</p></div></details>' for q, a in items)
    schema = {"@type": "FAQPage", "@id": url(ident), "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": _txt(a)}} for q, a in items]}
    return html, schema


def _txt(h):
    import re
    return re.sub(r"<[^>]+>", "", h)


BANDEAU = ('<div class="bandeau" aria-hidden="true"><div class="bandeau__piste">'
           + "".join('<span><b>Flexarion</b><span class="kanji">浪人</span>Souls-like<span class="kanji">刀</span>Science-fiction'
                     '<span class="kanji">星</span>Ronin of the Black Sun<span class="kanji">蝕</span>Aix-en-Provence<span class="kanji">墨</span></span>'
                     for _ in range(4))
           + '</div></div>')


# =====================================================================
# ACCUEIL
# =====================================================================
def accueil():
    faq = [
        ("Qu'est-ce que Flexarion ?", "Flexarion est un studio de jeux vidéo indépendant basé à Aix-en-Provence. Son premier jeu, Ronin of the Black Sun, est un souls-like de science-fiction où vous incarnez un ronin, un samouraï sans maître, dans un empire spatial inspiré du Japon féodal."),
        ("Quel jeu développe le studio Flexarion ?", "Flexarion développe Ronin of the Black Sun, un action-RPG exigeant de type souls-like. On y combat au katana, avec un système de parade et de posture, y compris dans des zones en apesanteur. <a href=\"jeu.html\">Découvrir le jeu</a>."),
        ("Où se trouve le studio Flexarion ?", "Le studio Flexarion est installé à Aix-en-Provence (13100), dans les Bouches-du-Rhône, en Provence-Alpes-Côte d'Azur, dans un ancien atelier d'imprimeur près du cours Mirabeau."),
        ("Quand sortira Ronin of the Black Sun ?", "Une démo jouable est prévue au printemps 2027, suivie d'un accès anticipé sur PC (Windows, Steam Deck visé) à la fin de l'année 2027."),
        ("D'où vient le nom Flexarion ?", "« Flex » vient du latin <em>flectere</em>, fléchir : comme l'acier d'un katana, replié des dizaines de fois, qui plie sans rompre. « Arion » est le poète grec sauvé des flots par un dauphin charmé par son chant. <a href=\"studio.html\">Lire l'histoire du studio</a>."),
        ("Comment suivre le développement de Flexarion ?", "L'équipe publie chaque mois un devlog sur les coulisses du jeu. Vous pouvez aussi vous abonner au flux RSS ou écrire au studio pour rejoindre les playtests. <a href=\"devlog/index.html\">Lire le devlog</a>."),
    ]
    faq_html, faq_ld = faq_bloc(faq, "#faq")
    site_ld = {"@type": "WebSite", "@id": url("#site"), "url": url(), "name": "Flexarion", "inLanguage": "fr-FR", "publisher": {"@id": ORG_ID}}
    corps = f'''
<section class="heros" aria-labelledby="titre">
  <div class="heros__fond" aria-hidden="true"><img src="assets/img/flexarion-ronin-soleil-noir.svg" alt="" width="1600" height="900" fetchpriority="high"></div>
  <canvas class="braises" aria-hidden="true"></canvas>
  <div class="lueur" aria-hidden="true"></div>
  <p class="heros__kanji" aria-hidden="true">星を斬る浪人</p>
  <div class="container">
    <div class="heros__contenu">
      <p class="heros__sur entree">Studio Flexarion · Aix-en-Provence</p>
      <h1 id="titre"><span class="titre-jeu"><span class="titre-lettres">RONIN</span><span class="titre-lettres titre-jeu__suite">OF THE BLACK SUN</span></span><span class="sous-titre entree" style="--delai:.9s">Le souls-like de science-fiction du studio Flexarion</span></h1>
      <p class="chapeau entree" style="--delai:1.1s">Le Soleil Noir s'est éteint. Le Shogun a fait de sa lumière une arme. Vous êtes Kaïen, dernier samouraï du clan Hoshino, ramené à la vie trois siècles trop tard pour sauver les vôtres, mais juste à temps pour les venger.</p>
      <div class="actions entree" style="--delai:1.3s">
        <a class="btn btn--plein" href="jeu.html">Découvrir le jeu <span class="fleche" aria-hidden="true">→</span></a>
        <a class="btn" href="devlog/index.html">Lire le devlog</a>
      </div>
    </div>
  </div>
  <a class="defiler" href="#univers">Défiler</a>
</section>

{BANDEAU}

<section class="section" id="univers" aria-labelledby="t-univers">
  <div class="container duo">
    <div>
      {etiquette("壱", "L'univers")}
      <h2 class="revele" id="t-univers">Quand le soleil s'est éteint, l'honneur s'est éteint avec lui</h2>
      {ornement()}
      <p class="revele">Au-delà de la Bordure, le <strong>Shogunat de Kurogane</strong> règne sur le système de Yomi. Sept châteaux orbitaux, les <strong>Shiro</strong>, gravitent autour d'une étoile éclipsée : le <strong>Soleil Noir</strong>. Depuis la Grande Éclipse, sa lumière est captive, et ceux qui la gardent sont devenus des monstres.</p>
      <p class="revele"><em>Ronin of the Black Sun</em> est un jeu de <strong>science-fiction</strong> qui emprunte au Japon féodal ses codes, ses armures et ses légendes, et les projette dans l'espace : des pagodes en orbite, des torii flottants, des duels au katana dans le silence du vide.</p>
      <div class="actions revele"><a class="btn" href="jeu.html#univers">Explorer l'univers <span class="fleche" aria-hidden="true">→</span></a></div>
    </div>
    <figure class="cadre revele-encre"><div class="cadre__img"><img src="assets/img/flexarion-shiro-chateau-orbital.svg" alt="Un Shiro, château orbital en forme de pagode, flotte au-dessus d'une planète violette dans Ronin of the Black Sun" width="1200" height="700" loading="lazy"></div>
      <figcaption>Un Shiro du Shogunat de Kurogane</figcaption></figure>
  </div>
</section>

{ENTAILLE}

<section class="section section--panneau" aria-labelledby="t-jeu">
  <div class="container">
    <div class="tete-section centre">
      {etiquette("弐", "Le jeu")}
      <h2 class="revele" id="t-jeu">Un souls-like où chaque duel se mérite</h2>
      {ornement()}
      <p class="revele">Action-RPG exigeant, Ronin of the Black Sun vous demande d'observer, de parer et de frapper au bon moment. Mourir fait partie du chemin du ronin.</p>
    </div>
    <div class="grille grille--3">
      <article class="carte revele"><span class="carte__num">I</span><span class="carte__kanji" aria-hidden="true">刀</span><h3>Le duel au katana</h3><p>Parez à la dernière seconde pour déclencher la Contre-lune, brisez la posture adverse et portez le Coup de l'Éclipse.</p></article>
      <article class="carte revele" style="--delai:.12s"><span class="carte__num">II</span><span class="carte__kanji" aria-hidden="true">空</span><h3>Le combat en apesanteur</h3><p>Entre les débris des châteaux orbitaux, il n'y a ni haut ni bas. Prenez appui sur le vide et frappez depuis n'importe quel angle.</p></article>
      <article class="carte revele" style="--delai:.24s"><span class="carte__num">III</span><span class="carte__kanji" aria-hidden="true">灰</span><h3>Un monde de cendres</h3><p>Reposez-vous aux Torii de lumière, récupérez vos Cendres d'étoile là où vous êtes tombé, et choisissez l'ordre de vos combats.</p></article>
    </div>
    <div class="actions revele" style="justify-content:center;margin-top:44px"><a class="btn btn--plein" href="jeu.html#mecaniques">Toutes les mécaniques <span class="fleche" aria-hidden="true">→</span></a></div>
  </div>
</section>

<section class="section" aria-labelledby="t-daimyo">
  <div class="container duo duo--inverse">
    <div>
      {etiquette("参", "Les ennemis")}
      <h2 class="revele" id="t-daimyo">Sept Daimyō du Vide vous attendent</h2>
      {ornement()}
      <p class="revele">Chaque Shiro est gardé par un seigneur corrompu par la lumière du Soleil Noir. Armures démesurées, techniques interdites, arènes sans gravité : chaque Daimyō est un combat que vous n'oublierez pas.</p>
      <div class="actions revele"><a class="btn" href="jeu.html#daimyos">Rencontrer les Daimyō <span class="fleche" aria-hidden="true">→</span></a></div>
    </div>
    <figure class="cadre revele-encre"><div class="cadre__img"><img src="assets/img/flexarion-daimyo-du-vide-boss.svg" alt="Un Daimyō du Vide, samouraï géant en armure au casque à cornes, face à un petit ronin" width="1200" height="700" loading="lazy"></div>
      <figcaption>Un Daimyō du Vide, boss de Ronin of the Black Sun</figcaption></figure>
  </div>
</section>

<section class="section--serre" aria-label="Flexarion en chiffres">
  <div class="container">
    <dl class="chiffres revele">
      <div><dt>année de fondation du studio, à Aix-en-Provence</dt><dd data-compteur="2023">2023</dd></div>
      <div><dt>artisans du jeu vidéo à plein temps</dt><dd data-compteur="6">6</dd></div>
      <div><dt>Daimyō du Vide à affronter</dt><dd data-compteur="7">7</dd></div>
      <div><dt>fins possibles selon votre code d'honneur</dt><dd data-compteur="3">3</dd></div>
    </dl>
  </div>
</section>

<section class="section" aria-labelledby="t-studio">
  <div class="container duo">
    <figure class="cadre revele-encre"><div class="cadre__img"><img src="assets/img/flexarion-aix-en-provence-sainte-victoire-encre.svg" alt="La montagne Sainte-Victoire à Aix-en-Provence peinte à l'encre devant un soleil noir" width="1200" height="600" loading="lazy"></div>
      <figcaption>La Sainte-Victoire, notre premier Soleil Noir</figcaption></figure>
    <div>
      {etiquette("肆", "Le studio")}
      <h2 class="revele" id="t-studio">Flexarion, studio de jeux vidéo indépendant à Aix-en-Provence</h2>
      {ornement()}
      <p class="revele"><strong>Flexarion</strong> est un studio indé de six personnes fondé en 2023 à Aix-en-Provence. Nous faisons des jeux de science-fiction exigeants et beaux, à taille humaine, sans crunch et en racontant notre travail en toute transparence.</p>
      <p class="revele">Notre premier jeu, <a href="jeu.html">Ronin of the Black Sun</a>, porte notre devise : comme l'acier d'un katana, plier sans jamais rompre.</p>
      <div class="actions revele"><a class="btn" href="studio.html">Rencontrer l'équipe <span class="fleche" aria-hidden="true">→</span></a></div>
    </div>
  </div>
</section>

{ENTAILLE}

<section class="section section--panneau" aria-labelledby="t-devlog">
  <div class="container">
    <div class="tete-section">
      {etiquette("伍", "Journal de développement")}
      <h2 class="revele" id="t-devlog">Les derniers devlogs de Flexarion</h2>
      {ornement()}
    </div>
    <div class="grille grille--3">{"".join(carte_billet(p, "", "h3", i * .12) for i, p in enumerate(POSTS[:3]))}</div>
  </div>
</section>

<section class="section" id="faq" aria-labelledby="t-faq">
  <div class="container--etroit">
    <div class="tete-section centre">
      {etiquette("陸", "Questions fréquentes")}
      <h2 class="revele" id="t-faq">Questions fréquentes sur Flexarion</h2>
      {ornement()}
    </div>
    <div class="faq">{faq_html}</div>
  </div>
</section>

<section class="section--serre" style="padding-bottom:110px">
  <div class="container">
    <div class="appel revele">
      {etiquette("七", "Rejoindre la voie")}
      <h2>Prenez la lame avant tout le monde</h2>
      <p>Presse, créateurs de contenu ou joueurs : écrivez-nous pour recevoir le kit presse ou rejoindre le prochain playtest de Ronin of the Black Sun.</p>
      <div class="actions"><a class="btn btn--plein" href="contact.html">Contacter le studio <span class="fleche" aria-hidden="true">→</span></a></div>
    </div>
  </div>
</section>'''
    return page("index.html",
                "Flexarion — Ronin of the Black Sun, souls-like de science-fiction",
                "Flexarion, studio de jeux vidéo indépendant à Aix-en-Provence, développe Ronin of the Black Sun : un souls-like de science-fiction où vous incarnez un ronin face aux Daimyō du Vide.",
                corps, ld(ORGANISATION, site_ld, JEU, faq_ld))


# =====================================================================
# LE JEU
# =====================================================================
def jeu():
    crumbs = [("Accueil", ""), ("Le jeu", "jeu.html")]
    faq = [
        ("Qui développe Ronin of the Black Sun ?", "Ronin of the Black Sun est développé par Flexarion, un studio de jeux vidéo indépendant de six personnes basé à Aix-en-Provence."),
        ("Ronin of the Black Sun est-il un souls-like ?", "Oui. C'est un action-RPG exigeant : les combats demandent d'observer l'adversaire, de parer au bon moment et d'apprendre de ses morts. Des options d'accessibilité permettent d'ajuster la difficulté sans pénalité."),
        ("Sur quelles plateformes pourra-t-on jouer à Ronin of the Black Sun ?", "D'abord sur PC (Windows), avec la compatibilité Steam Deck en ligne de mire. Des versions consoles sont à l'étude pour la version 1.0."),
        ("Quand sortira Ronin of the Black Sun ?", "Une démo est prévue au printemps 2027, puis un accès anticipé sur PC à la fin de l'année 2027. Les dates précises seront annoncées dans le devlog."),
        ("Combien de temps dure le jeu ?", "Comptez 25 à 35 heures pour terminer l'aventure principale, davantage pour vaincre les sept Daimyō et découvrir les trois fins."),
        ("Le jeu sera-t-il traduit en français ?", "Le jeu est développé en français. Les textes seront disponibles en français, en anglais et en japonais, avec un doublage japonais."),
    ]
    faq_html, faq_ld = faq_bloc(faq, "jeu.html#faq")
    page_ld = {"@type": "WebPage", "@id": url("jeu.html#page"), "url": url("jeu.html"), "name": "Ronin of the Black Sun", "about": {"@id": GAME_ID}, "isPartOf": {"@id": url("#site")}}
    meca = [
        ("刀", "Le duel au katana", "Chaque combat est un échange de lecture. Attaques légères et lourdes, techniques de iaijutsu et coups chargés : votre lame répond au moindre geste."),
        ("月", "La Contre-lune", "Parez à la dernière seconde pour renvoyer la force du coup. La parade parfaite épuise la posture de l'ennemi plus vite que n'importe quelle attaque."),
        ("空", "Le Pas du Vide", "Dans les zones sans gravité, propulsez-vous de débris en débris. Le ronin s'oriente toujours vers son adversaire : le vide devient votre arène."),
        ("鳥", "Les Torii de lumière", "Ces portails sacrés sont vos sanctuaires. Reposez-vous pour reprendre des forces, au prix du retour des ennemis, et méditez pour progresser."),
        ("灰", "Les Cendres d'étoile", "Chaque ennemi vaincu vous donne des Cendres d'étoile. Mourez, et elles restent là où vous êtes tombé : retournez les chercher, si vous l'osez."),
        ("義", "Le Code du ronin", "Épargner un ennemi à genoux ou l'achever ? Vos choix d'honneur façonnent le monde, vos alliés et l'une des trois fins du jeu."),
    ]
    meca_html = "".join(f'<article class="carte revele" style="--delai:{(i % 3) * .1:.1f}s"><span class="carte__num">{["I","II","III","IV","V","VI"][i]}</span><span class="carte__kanji" aria-hidden="true">{k}</span><h3>{t}</h3><p>{d}</p></article>' for i, (k, t, d) in enumerate(meca))
    lexique = [
        ("Le Soleil Noir", "Une étoile éclipsée depuis trois siècles. Sa lumière n'a pas disparu : le Shogun l'a scellée."),
        ("Les Sept Shiro", "Sept châteaux orbitaux, sept seigneurs, sept sceaux à briser."),
        ("Kaïen", "Le ronin que vous incarnez. Dernier du clan Hoshino, exécuté pour avoir refusé un ordre."),
        ("Hoshikiri", "« Celle qui tranche les étoiles » : la lame de Kaïen, forgée dans le cœur d'une étoile morte."),
    ]
    lex_html = "".join(f'<article class="carte revele" style="--delai:{i * .1:.1f}s"><h3>{t}</h3><p>{d}</p></article>' for i, (t, d) in enumerate(lexique))
    daimyo_html = "".join(
        f'<li><button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-desc="{escape(d)}"><span class="nom">{escape(n)}</span><span class="kanji" aria-hidden="true">{k}</span></button></li>'
        for i, (k, n, d) in enumerate(DAIMYOS))
    galerie = [
        ("flexarion-ronin-soleil-noir.svg", 1600, 900, "Kaïen, le héros de Ronin of the Black Sun, face au Soleil Noir et à un torii brisé", "Kaïen face au Soleil Noir"),
        ("flexarion-torii-de-lumiere-sanctuaire.svg", 1200, 700, "Un Torii de lumière, sanctuaire flottant dans l'espace où le ronin se repose", "Un Torii de lumière"),
        ("flexarion-duel-apesanteur-katana.svg", 1200, 700, "Duel au katana en apesanteur entre deux samouraïs au milieu de débris", "Duel en apesanteur"),
        ("flexarion-daimyo-du-vide-boss.svg", 1200, 700, "Un Daimyō du Vide, boss géant en armure de samouraï", "Un Daimyō du Vide"),
        ("flexarion-shiro-chateau-orbital.svg", 1200, 700, "Un Shiro, château orbital en forme de pagode au-dessus d'une planète", "Un Shiro orbital"),
    ]
    gal_html = "".join(
        f'<figure class="cadre revele" style="--delai:{(i % 3) * .1:.1f}s"><a href="assets/img/{f}" data-visionneuse data-legende="{escape(c)}"><div class="cadre__img"><img src="assets/img/{f}" alt="{escape(a)}" width="{w}" height="{h}" loading="lazy"></div></a><figcaption>{escape(c)}</figcaption></figure>'
        for i, (f, w, h, a, c) in enumerate(galerie))
    corps = f'''
<section class="heros heros-page--image" aria-labelledby="titre">
  <div class="heros__fond" aria-hidden="true"><img src="assets/img/flexarion-duel-apesanteur-katana.svg" alt="" width="1200" height="700" fetchpriority="high"></div>
  <canvas class="braises" aria-hidden="true"></canvas>
  <div class="lueur" aria-hidden="true"></div>
  <p class="heros__kanji" aria-hidden="true">浪人の道</p>
  <div class="container">
    {ariane(crumbs, "")}
    <p class="heros__sur entree">Le jeu · Action-RPG · Science-fiction</p>
    <h1 id="titre"><span class="titre-jeu"><span class="titre-lettres">RONIN</span><span class="titre-lettres titre-jeu__suite">OF THE BLACK SUN</span></span><span class="sous-titre entree" style="--delai:.9s">Un souls-like de samouraï dans l'espace, par le studio Flexarion</span></h1>
    <p class="chapeau entree" style="--delai:1.1s">Incarnez Kaïen, ronin ressuscité, et tranchez votre chemin à travers les Sept Shiro du Shogunat de Kurogane pour libérer la lumière du Soleil Noir.</p>
    <div class="actions entree" style="--delai:1.3s"><a class="btn btn--plein" href="#mecaniques">Le combat <span class="fleche" aria-hidden="true">→</span></a><a class="btn" href="#fiche">Fiche du jeu</a></div>
  </div>
</section>

{BANDEAU}

<section class="section" id="univers" aria-labelledby="t-univers">
  <div class="container">
    <div class="duo">
      <div>
        {etiquette("壱", "L'univers")}
        <h2 class="revele" id="t-univers">Trois siècles après la Grande Éclipse</h2>
        {ornement()}
        <p class="revele">Il y a trois cents ans, le Shogun de Kurogane a éclipsé l'étoile de Yomi pour capturer sa lumière. Les clans qui ont refusé de s'agenouiller ont été effacés. Le clan Hoshino fut le dernier.</p>
        <p class="revele">Aujourd'hui, un Torii de lumière s'allume au milieu d'un cimetière de vaisseaux, et un samouraï que tout le monde croyait mort ouvre les yeux. Sans maître, sans clan, sans soleil : un <strong>ronin</strong>. Il lui reste une lame, et une dette.</p>
      </div>
      <blockquote class="citation revele"><p>Un samouraï sert son seigneur. Un ronin ne sert que sa lame.</p><cite>— Proverbe du clan Hoshino</cite></blockquote>
    </div>
    <div class="grille grille--4" style="margin-top:60px">{lex_html}</div>
  </div>
</section>

{ENTAILLE}

<section class="section section--panneau" id="mecaniques" aria-labelledby="t-meca">
  <div class="container">
    <div class="tete-section centre">
      {etiquette("弐", "Mécaniques de jeu")}
      <h2 class="revele" id="t-meca">Comment on joue à Ronin of the Black Sun</h2>
      {ornement()}
      <p class="revele">Un action-RPG souls-like centré sur le duel : observer, parer, punir. Puis recommencer, un peu meilleur.</p>
    </div>
    <div class="grille grille--3">{meca_html}</div>
    <p class="revele centre" style="margin-top:40px"><a href="devlog/parade-posture-apesanteur-systeme-de-combat.html">Lire le devlog sur le système de combat →</a></p>
  </div>
</section>

<section class="section" id="daimyos" aria-labelledby="t-daimyos">
  <div class="container">
    <div class="tete-section">
      {etiquette("参", "Les boss")}
      <h2 class="revele" id="t-daimyos">Les Sept Daimyō du Vide</h2>
      {ornement()}
      <p class="revele">Survolez ou sélectionnez un nom pour découvrir chaque seigneur. Vous les affronterez dans l'ordre de votre choix, sauf le dernier.</p>
    </div>
    <div class="daimyos">
      <div><ol data-daimyos>{daimyo_html}</ol><p class="daimyos__desc" data-daimyo-desc aria-live="polite">{escape(DAIMYOS[0][2])}</p></div>
      <figure class="cadre revele-encre"><div class="cadre__img"><img src="assets/img/flexarion-daimyo-du-vide-boss.svg" alt="Silhouette d'un Daimyō du Vide aux yeux rouges devant un halo doré" width="1200" height="700" loading="lazy"></div><figcaption>Un Daimyō du Vide</figcaption></figure>
    </div>
  </div>
</section>

{ENTAILLE}

<section class="section section--panneau" id="visuels" aria-labelledby="t-visuels">
  <div class="container">
    <div class="tete-section">
      {etiquette("肆", "Visuels")}
      <h2 class="revele" id="t-visuels">Concept arts de Ronin of the Black Sun</h2>
      {ornement()}
      <p class="revele">Recherches graphiques de l'équipe artistique. Le jeu est en développement : tout peut encore évoluer. Cliquez sur une image pour l'agrandir.</p>
    </div>
    <div class="galerie">{gal_html}</div>
    <p class="revele" style="margin-top:30px"><a href="devlog/direction-artistique-encre-or-et-vide.html">Lire le devlog sur la direction artistique →</a></p>
  </div>
</section>

<section class="section" id="fiche" aria-labelledby="t-fiche">
  <div class="container duo" style="align-items:start">
    <div>
      {etiquette("伍", "Fiche technique")}
      <h2 class="revele" id="t-fiche">Ronin of the Black Sun en bref</h2>
      {ornement()}
      <div class="tableau revele"><table class="fiche">
        <tr><th scope="row">Studio</th><td>Flexarion (Aix-en-Provence)</td></tr>
        <tr><th scope="row">Genre</th><td>Action-RPG, souls-like</td></tr>
        <tr><th scope="row">Univers</th><td>Science-fiction, Japon féodal</td></tr>
        <tr><th scope="row">Mode</th><td>Solo</td></tr>
        <tr><th scope="row">Plateformes</th><td>PC (Windows), Steam Deck visé</td></tr>
        <tr><th scope="row">Moteur</th><td>Unreal Engine 5</td></tr>
        <tr><th scope="row">Durée</th><td>25 à 35 heures, trois fins</td></tr>
        <tr><th scope="row">Langues</th><td>Français, anglais, japonais ; doublage japonais</td></tr>
        <tr><th scope="row">Classification</th><td>PEGI 16 visé</td></tr>
        <tr><th scope="row">Modèle</th><td>Jeu premium, environ 25 €, sans microtransaction</td></tr>
      </table></div>
    </div>
    <div>
      {etiquette("陸", "Feuille de route")}
      <h2 class="revele">Le chemin du ronin</h2>
      {ornement()}
      <ol class="frise revele">
        <li><span class="annee">2024</span><h3>Prototype « Lame-Lune »</h3><p>Validation de la parade parfaite et de la posture.</p></li>
        <li><span class="annee">2025</span><h3>Premier Shiro jouable</h3><p>Le Shiro-Ferraille et sa Daimyō, testés en interne.</p></li>
        <li><span class="annee">Automne 2026</span><h3>Annonce et devlog public</h3><p>Ronin of the Black Sun se dévoile.</p></li>
        <li class="avenir"><span class="annee">Printemps 2027</span><h3>Démo jouable</h3><p>Deux Shiro, trois Daimyō et le combat en apesanteur.</p></li>
        <li class="avenir"><span class="annee">Fin 2027</span><h3>Accès anticipé sur PC</h3><p>Les Shiro s'ouvrent un à un, avec la communauté.</p></li>
      </ol>
    </div>
  </div>
</section>

<section class="section section--panneau" id="faq" aria-labelledby="t-faq">
  <div class="container--etroit">
    <div class="tete-section centre">
      {etiquette("七", "FAQ")}
      <h2 class="revele" id="t-faq">Questions fréquentes sur Ronin of the Black Sun</h2>
      {ornement()}
    </div>
    <div class="faq">{faq_html}</div>
  </div>
</section>

<section class="section--serre" style="padding:110px 0">
  <div class="container"><div class="appel revele">
    <h2>Suivez la voie du ronin</h2>
    <p>Chaque mois, l'équipe de Flexarion raconte les coulisses du jeu. Et les inscriptions au prochain playtest sont ouvertes.</p>
    <div class="actions"><a class="btn btn--plein" href="devlog/index.html">Lire le devlog <span class="fleche" aria-hidden="true">→</span></a><a class="btn" href="contact.html">Rejoindre le playtest</a></div>
  </div></div>
</section>'''
    return page("jeu.html",
                "Ronin of the Black Sun — Souls-like de samouraï du studio Flexarion",
                "Ronin of the Black Sun, du studio Flexarion, est un action-RPG souls-like de science-fiction : incarnez un ronin, maîtrisez le katana et la parade, et affrontez les Sept Daimyō du Vide. Univers, combat, visuels.",
                corps, ld(JEU, page_ld, faq_ld, fil(crumbs)))


# =====================================================================
# LE STUDIO
# =====================================================================
def lien(l):
    return f' <a href="{l}">Lire son devlog</a>.' if l else ""


def studio():
    crumbs = [("Accueil", ""), ("Le studio", "studio.html")]
    equipe = "".join(
        f'<article class="carte membre revele" style="--delai:{(i % 3) * .1:.1f}s"><div class="sceau" aria-hidden="true">{k}</div><h3>{escape(n)}</h3><span class="role">{escape(r)}</span><p>{escape(b)}{lien(l)}</p></article>'
        for i, (k, n, r, b, l) in enumerate(TEAM))
    org = dict(ORGANISATION)
    org["founder"] = [{"@type": "Person", "name": n, "jobTitle": r} for _, n, r, _, _ in TEAM[:3]]
    org["member"] = [{"@type": "Person", "name": n, "jobTitle": r} for _, n, r, _, _ in TEAM]
    about = {"@type": "AboutPage", "@id": url("studio.html#page"), "url": url("studio.html"), "name": "Le studio Flexarion", "about": {"@id": ORG_ID}}
    corps = f'''
<section class="heros-page" aria-labelledby="titre">
  <span class="heros-page__kanji" aria-hidden="true">道場</span>
  <div class="container">
    {ariane(crumbs, "")}
    <p class="heros__sur revele">Studio indépendant · fondé en 2023 · Aix-en-Provence</p>
    <h1 class="revele" id="titre">Le studio Flexarion : des jeux de science-fiction forgés à Aix-en-Provence</h1>
    <p class="chapeau revele">Six artisans du jeu vidéo, un ancien atelier d'imprimeur près du cours Mirabeau et une conviction : on peut raconter les étoiles, et les samouraïs, depuis la Provence.</p>
  </div>
</section>

<section class="section" id="histoire" aria-labelledby="t-histoire">
  <div class="container duo" style="align-items:start">
    <div>
      {etiquette("壱", "Notre histoire")}
      <h2 class="revele" id="t-histoire">D'une game jam à un studio de six personnes</h2>
      {ornement()}
      <p class="revele">Flexarion n'est pas né dans un garage, mais dans une salle de cours surchauffée d'Aix-en-Provence, un week-end de juin. Trois étudiants, quarante-huit heures, un thème imposé, « l'honneur », et un croquis à l'encre qui ne les a plus quittés.</p>
      <blockquote class="citation revele" style="text-align:left;margin-top:40px"><p>Plier sans rompre : c'est le katana, et c'est tout le programme du studio.</p><cite>— Maëlle Roux, directrice créative</cite></blockquote>
    </div>
    <ol class="frise revele">
      <li><span class="annee">2021</span><h3>Une game jam, trois inconnus</h3><p>Maëlle, Idriss et Clément se rencontrent et créent un duel de samouraïs face à une éclipse.</p></li>
      <li><span class="annee">2023</span><h3>Naissance de Flexarion</h3><p>Diplômes en poche, ils fondent le studio à Aix-en-Provence, dans un ancien atelier d'imprimeur.</p></li>
      <li><span class="annee">2024</span><h3>Le prototype « Lame-Lune »</h3><p>Un an de recherche sur la parade parfaite, testé dans les bars à jeux du pays d'Aix.</p></li>
      <li><span class="annee">2025</span><h3>L'équipe passe à six</h3><p>Soraya, Théo et Lina rejoignent l'aventure. Le studio adopte la semaine de quatre jours.</p></li>
      <li><span class="annee">2026</span><h3>Ronin of the Black Sun se dévoile</h3><p>Le jeu est annoncé et le devlog public ouvre ses portes.</p></li>
      <li class="avenir"><span class="annee">2027</span><h3>Accès anticipé</h3><p>Prochaine étape : la démo, puis la sortie en accès anticipé sur PC.</p></li>
    </ol>
  </div>
</section>

{ENTAILLE}

<section class="section section--panneau" id="nom" aria-labelledby="t-nom">
  <div class="container--etroit centre">
    {etiquette("弐", "Le nom")}
    <h2 class="revele" id="t-nom">Pourquoi « Flexarion » ?</h2>
    {ornement()}
    <p class="revele"><strong>Flex</strong>, du latin <em>flectere</em>, « fléchir » : comme l'acier d'un katana, replié et martelé des dizaines de fois, qui plie sans jamais rompre.</p>
    <p class="revele"><strong>Arion</strong>, du nom du poète grec que la légende dit sauvé des flots par un dauphin charmé par son chant : la preuve qu'une belle histoire peut vous tirer des pires tempêtes.</p>
    <p class="revele">Un studio souple, des récits qui portent. Et un premier jeu qui porte ces valeurs : <a href="jeu.html">Ronin of the Black Sun</a>.</p>
  </div>
</section>

<section class="section" id="equipe" aria-labelledby="t-equipe">
  <div class="container">
    <div class="tete-section">
      {etiquette("参", "L'équipe")}
      <h2 class="revele" id="t-equipe">L'équipe de Flexarion</h2>
      {ornement()}
      <p class="revele">Six métiers, un seul atelier et une règle : chaque vendredi, tout le monde joue au jeu de tout le monde.</p>
    </div>
    <div class="grille grille--3">{equipe}</div>
  </div>
</section>

<section class="section section--panneau" aria-labelledby="t-methode">
  <div class="container">
    <div class="tete-section centre">
      {etiquette("肆", "Notre méthode")}
      <h2 class="revele" id="t-methode">Un studio indépendant, à taille humaine</h2>
      {ornement()}
    </div>
    <div class="grille grille--4">
      <article class="carte revele"><span class="carte__kanji" aria-hidden="true">和</span><h3>Zéro crunch</h3><p>Semaine de quatre jours, pas d'heures cachées. Un jeu en retard se rattrape ; une équipe épuisée, non.</p></article>
      <article class="carte revele" style="--delai:.1s"><span class="carte__kanji" aria-hidden="true">誠</span><h3>Développement ouvert</h3><p>Un devlog par mois, chiffres et échecs compris.</p></article>
      <article class="carte revele" style="--delai:.2s"><span class="carte__kanji" aria-hidden="true">心</span><h3>Accessibilité</h3><p>Exigeant ne veut pas dire fermé : options de confort pensées dès le prototype.</p></article>
      <article class="carte revele" style="--delai:.3s"><span class="carte__kanji" aria-hidden="true">礼</span><h3>Respect des cultures</h3><p>Relectures par une traductrice et conseils de pratiquants d'arts martiaux.</p></article>
    </div>
  </div>
</section>

<section class="section" id="aix-en-provence" aria-labelledby="t-aix">
  <div class="container duo">
    <figure class="cadre revele-encre"><div class="cadre__img"><img src="assets/img/flexarion-aix-en-provence-sainte-victoire-encre.svg" alt="La Sainte-Victoire, montagne d'Aix-en-Provence, peinte à l'encre devant un soleil noir" width="1200" height="600" loading="lazy"></div><figcaption>La Sainte-Victoire, vue depuis l'atelier (ou presque)</figcaption></figure>
    <div>
      {etiquette("伍", "Notre port d'attache")}
      <h2 class="revele" id="t-aix">Un studio de jeux vidéo ancré à Aix-en-Provence</h2>
      {ornement()}
      <p class="revele">Aix-en-Provence n'est pas un décor : c'est notre matière première. La Sainte-Victoire, que Cézanne a peinte des dizaines de fois, nous a donné le Soleil Noir, visible depuis tout le jeu. Le mistral, qui nettoie le ciel en une nuit, souffle dans nos arènes en apesanteur.</p>
      <p class="revele">La ville est aussi un vivier : université, écoles d'art et d'informatique, associations de créateurs. Nous y recrutons nos stagiaires et y testons nos prototypes.</p>
      <p class="revele" style="color:var(--cendre-sourde)">Flexarion — 13100 Aix-en-Provence, Bouches-du-Rhône, Provence-Alpes-Côte d'Azur</p>
    </div>
  </div>
</section>

<section class="section--serre" style="padding-bottom:110px">
  <div class="container"><div class="appel revele">
    <h2>Une idée, une question, une candidature ?</h2>
    <p>Stage, collaboration, intervention dans une école ou simple envie de parler de samouraïs et de science-fiction : la porte de l'atelier est ouverte.</p>
    <div class="actions"><a class="btn btn--plein" href="contact.html">Écrire à l'équipe <span class="fleche" aria-hidden="true">→</span></a><a class="btn" href="jeu.html">Découvrir le jeu</a></div>
  </div></div>
</section>'''
    return page("studio.html",
                "Le studio Flexarion — Studio de jeux vidéo indépendant à Aix-en-Provence",
                "Découvrez Flexarion, studio de jeux vidéo indépendant fondé en 2023 à Aix-en-Provence : son histoire, l'origine de son nom et l'équipe de six qui crée un souls-like de science-fiction.",
                corps, ld(org, about, fil(crumbs)))


# =====================================================================
# DEVLOG
# =====================================================================
def devlog_index():
    crumbs = [("Accueil", ""), ("Devlog", "devlog/index.html")]
    blog = {"@type": "Blog", "@id": url("devlog/#blog"), "url": url("devlog/index.html"), "name": "Devlog Flexarion",
            "description": "Le journal de développement de Ronin of the Black Sun, souls-like de science-fiction.",
            "inLanguage": "fr-FR", "publisher": {"@id": ORG_ID},
            "blogPost": [{"@type": "BlogPosting", "headline": p["titre"], "url": url(f"devlog/{p['slug']}.html"),
                          "datePublished": p["date"], "author": {"@type": "Person", "name": p["auteur"]}} for p in POSTS]}
    corps = f'''
<section class="heros-page" aria-labelledby="titre">
  <span class="heros-page__kanji" aria-hidden="true">日誌</span>
  <div class="container">
    {ariane(crumbs, "../")}
    <p class="heros__sur revele">Journal de développement</p>
    <h1 class="revele" id="titre">Le devlog de Flexarion</h1>
    <p class="chapeau revele">Combat, direction artistique, univers : chaque mois, l'équipe du studio raconte la fabrication de son souls-like de science-fiction, sans filtre.</p>
  </div>
</section>
<section class="section" aria-label="Articles">
  <div class="container"><div class="grille grille--3">{"".join(carte_billet(p, "../", "h2", i * .1) for i, p in enumerate(POSTS))}</div></div>
</section>
<section class="section--serre" style="padding-bottom:110px">
  <div class="container"><div class="appel revele">
    <h2>Ne manquez aucun devlog</h2>
    <p>Abonnez-vous au flux RSS ou proposez-nous un sujet : nous y répondrons dans un prochain article.</p>
    <div class="actions"><a class="btn btn--plein" href="feed.xml">Flux RSS</a><a class="btn" href="../contact.html">Proposer un sujet</a></div>
  </div></div>
</section>'''
    return page("devlog/index.html",
                "Devlog Flexarion — Journal de développement du souls-like de science-fiction",
                "Le devlog du studio Flexarion : coulisses du développement de Ronin of the Black Sun, souls-like de samouraï dans l'espace. Système de combat, direction artistique et univers.",
                corps, ld(blog, fil(crumbs)))


def billet(p, i):
    crumbs = [("Accueil", ""), ("Devlog", "devlog/index.html"), (f"Devlog {p['num']}", f"devlog/{p['slug']}.html")]
    import re
    mots = len(re.findall(r"\w+", _txt(p["corps"])))
    art = {"@type": "BlogPosting", "@id": url(f"devlog/{p['slug']}.html#article"),
           "headline": f"Devlog {p['num']} — {p['titre']}", "description": p["description"],
           "image": url(f"assets/img/og-devlog-{p['num']}.png"), "datePublished": p["date"], "dateModified": p.get("maj", p["date"]),
           "inLanguage": "fr-FR", "wordCount": mots, "keywords": ", ".join(["Flexarion", "Ronin of the Black Sun", "souls-like", "science-fiction"] + p["tags"]),
           "isPartOf": {"@id": url("devlog/#blog")}, "mainEntityOfPage": url(f"devlog/{p['slug']}.html"),
           "author": {"@type": "Person", "name": p["auteur"], "jobTitle": p["role"], "worksFor": {"@id": ORG_ID}},
           "publisher": {"@id": ORG_ID}, "about": {"@id": GAME_ID}}
    prec = POSTS[i + 1] if i + 1 < len(POSTS) else None
    suiv = POSTS[i - 1] if i > 0 else None
    nav = '<nav class="nav-billets" aria-label="Autres devlogs">'
    if prec:
        nav += f'<a href="{prec["slug"]}.html" rel="prev"><small>← Devlog précédent</small>{escape(prec["titre"])}</a>'
    if suiv:
        nav += f'<a class="suivant" href="{suiv["slug"]}.html" rel="next"><small>Devlog suivant →</small>{escape(suiv["titre"])}</a>'
    nav += "</nav>"
    tags = " · ".join(escape(t) for t in p["tags"])
    corps = f'''
<article>
  <header class="heros-page" style="padding-bottom:50px">
    <span class="heros-page__kanji" aria-hidden="true">{p["sceau"]}</span>
    <div class="container--etroit">
      {ariane(crumbs, "../")}
      <p class="meta revele"><span>Devlog {p["num"]}</span><span>{tags}</span></p>
      <h1 class="revele" style="font-size:clamp(1.9rem,4.4vw,3.1rem)">Devlog {p["num"]} — {escape(p["titre"])}</h1>
      <p class="chapeau revele">{escape(p["chapo"])}</p>
      <p class="meta revele"><span>Par <a href="../studio.html#equipe">{escape(p["auteur"])}</a></span><time datetime="{p["date"]}">{fr_date(p["date"])}</time><span>{p["minutes"]} min de lecture</span></p>
    </div>
  </header>
  <div class="container" style="max-width:1000px;margin-top:50px">
    <figure class="cadre revele-encre"><div class="cadre__img"><img src="../assets/img/{p["image"]}" alt="{escape(p["alt"])}" width="{p["w"]}" height="{p["h"]}" fetchpriority="high"></div></figure>
  </div>
  <div class="container--etroit prose" style="margin-top:50px">{p["corps"]}
    <div class="auteur"><div class="sceau" aria-hidden="true" style="margin:0">{p["sceau"]}</div><p><strong>{escape(p["auteur"])}</strong> · {escape(p["role"])}<br>Membre de l'équipe <a href="../studio.html">Flexarion</a>, studio de jeux vidéo indépendant à Aix-en-Provence.</p></div>
    {nav}
  </div>
</article>
<section class="section--serre" style="padding:100px 0 110px">
  <div class="container"><div class="appel revele">
    <h2>Envie de prendre la lame ?</h2>
    <p>Les inscriptions au prochain playtest de Ronin of the Black Sun sont ouvertes. Écrivez-nous, nous vous gardons une place.</p>
    <div class="actions"><a class="btn btn--plein" href="../contact.html">Rejoindre le playtest <span class="fleche" aria-hidden="true">→</span></a><a class="btn" href="index.html">Tous les devlogs</a></div>
  </div></div>
</section>'''
    return page(f"devlog/{p['slug']}.html", p["title"] + " | Flexarion", p["description"], corps,
                ld(art, fil(crumbs)), og=f"assets/img/og-devlog-{p['num']}.png", og_alt=p["alt"], type_og="article",
                head_extra=f'<meta property="article:published_time" content="{p["date"]}">\n<meta property="article:author" content="{escape(p["auteur"])}">\n')


# =====================================================================
# CONTACT, MENTIONS, 404
# =====================================================================
def contact():
    crumbs = [("Accueil", ""), ("Contact & presse", "contact.html")]
    res = socials()
    res_html = ('<ul class="telechargements">' + "".join(f'<li><span>{escape(n)}</span><a href="{escape(u)}" rel="me noopener" target="_blank">Suivre</a></li>' for n, u in res) + "</ul>"
                if res else "<p>Nos comptes officiels arrivent très bientôt. En attendant, le devlog et son flux RSS restent le meilleur moyen de suivre Flexarion.</p>")
    cp = {"@type": "ContactPage", "@id": url("contact.html#page"), "url": url("contact.html"), "name": "Contacter le studio Flexarion",
          "about": {"@id": ORG_ID}}
    org = dict(ORGANISATION)
    org["contactPoint"] = [{"@type": "ContactPoint", "contactType": "press", "email": EMAIL, "availableLanguage": ["French", "English"]}]
    dl = [("Logo Flexarion (SVG)", "assets/img/flexarion-logo.svg"), ("Logo Flexarion (PNG 512 px)", "icon-512.png"),
          ("Visuel clé Ronin of the Black Sun (PNG 1200 × 630)", "assets/img/og-flexarion.png"), ("Key art : le ronin et le Soleil Noir", "assets/img/flexarion-ronin-soleil-noir.svg"),
          ("Concept art : un Daimyō du Vide", "assets/img/flexarion-daimyo-du-vide-boss.svg"), ("Concept art : duel en apesanteur", "assets/img/flexarion-duel-apesanteur-katana.svg"),
          ("Concept art : Torii de lumière", "assets/img/flexarion-torii-de-lumiere-sanctuaire.svg"), ("Concept art : Shiro orbital", "assets/img/flexarion-shiro-chateau-orbital.svg")]
    dl_html = "".join(f'<li><span>{escape(n)}</span><a href="{f}" download>Télécharger</a></li>' for n, f in dl)
    corps = f'''
<section class="heros-page" aria-labelledby="titre">
  <span class="heros-page__kanji" aria-hidden="true">文</span>
  <div class="container">
    {ariane(crumbs, "")}
    <p class="heros__sur revele">Contact &amp; presse</p>
    <h1 class="revele" id="titre">Contacter le studio Flexarion</h1>
    <p class="chapeau revele">Presse, créateurs de contenu, festivals, partenaires ou joueurs : l'équipe lit et répond elle-même à tous les messages, en français ou en anglais.</p>
  </div>
</section>
<section class="section">
  <div class="container grille grille--2">
    <article class="carte revele"><span class="carte__kanji" aria-hidden="true">信</span><h2 style="font-size:1.5rem">Écrire au studio</h2>
      <p>Interview, clé de test, playtest, collaboration ou candidature spontanée :</p>
      <p class="courriel"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p style="color:var(--cendre-sourde)">Réponse sous 72 heures ouvrées. Studio basé à Aix-en-Provence (13100). Rencontres sur rendez-vous.</p></article>
    <article class="carte revele" style="--delai:.12s"><span class="carte__kanji" aria-hidden="true">縁</span><h2 style="font-size:1.5rem">Suivre Flexarion</h2>
      {res_html}<p style="margin-top:16px"><a href="devlog/feed.xml">S'abonner au flux RSS du devlog</a></p></article>
  </div>
</section>
{ENTAILLE}
<section class="section section--panneau" id="presse" aria-labelledby="t-presse">
  <div class="container">
    <div class="tete-section">
      {etiquette("報", "Kit presse")}
      <h2 class="revele" id="t-presse">Kit presse Flexarion</h2>
      {ornement()}
      <p class="revele">Tous les éléments ci-dessous sont libres d'utilisation pour parler du studio et du jeu.</p>
    </div>
    <div class="duo" style="align-items:start">
      <div class="revele">
        <h3>Fiche d'identité</h3>
        <div class="tableau"><table class="fiche">
          <tr><th scope="row">Studio</th><td>Flexarion, studio de jeux vidéo indépendant</td></tr>
          <tr><th scope="row">Fondation</th><td>2023, Aix-en-Provence (France)</td></tr>
          <tr><th scope="row">Équipe</th><td>6 personnes</td></tr>
          <tr><th scope="row">Jeu</th><td><a href="jeu.html">Ronin of the Black Sun</a>, souls-like de science-fiction</td></tr>
          <tr><th scope="row">Plateforme</th><td>PC (Windows), Steam Deck visé</td></tr>
          <tr><th scope="row">Sortie</th><td>Démo printemps 2027, accès anticipé fin 2027</td></tr>
          <tr><th scope="row">Contact presse</th><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
        </table></div>
        <h3 style="margin-top:36px">Présentation courte</h3>
        <p>Flexarion est un studio de jeux vidéo indépendant d'Aix-en-Provence. Son premier jeu, Ronin of the Black Sun, est un souls-like de science-fiction où l'on incarne un ronin dans un shogunat spatial.</p>
        <h3>Présentation longue</h3>
        <p>Fondé en 2023 par trois anciens étudiants aixois, rejoints en 2025 par une directrice artistique, un compositeur et une productrice, Flexarion développe des jeux de science-fiction exigeants et esthétiques. Son premier titre, Ronin of the Black Sun, est un action-RPG souls-like : le joueur incarne Kaïen, ronin ressuscité trois siècles après la Grande Éclipse, et affronte au katana les Sept Daimyō du Vide pour libérer la lumière du Soleil Noir. Le jeu mêle duels de précision, combat en apesanteur et une direction artistique inspirée de la peinture à l'encre japonaise.</p>
      </div>
      <div class="revele">
        <h3>Logos et visuels</h3>
        <ul class="telechargements">{dl_html}</ul>
      </div>
    </div>
  </div>
</section>'''
    return page("contact.html", "Contact & kit presse — Flexarion, studio de jeux vidéo à Aix-en-Provence",
                "Contactez Flexarion, studio de jeux vidéo indépendant à Aix-en-Provence. Kit presse du souls-like de science-fiction Ronin of the Black Sun : fiche, logos et visuels à télécharger.",
                corps, ld(org, cp, fil(crumbs)))


def mentions():
    crumbs = [("Accueil", ""), ("Mentions légales", "mentions-legales.html")]
    corps = f'''
<section class="heros-page" aria-labelledby="titre"><div class="container--etroit">
  {ariane(crumbs, "")}<h1 class="revele" id="titre">Mentions légales</h1></div></section>
<section class="section"><div class="container--etroit prose">
  <h2>Éditeur du site</h2>
  <p>Site conçu, rédigé et développé par <strong>Jean Damez, Wanis Said Boutabouzi, Rayan Keokham et Aymen El Mestari</strong>, étudiants en BUT Informatique à l'IUT d'Aix-Marseille, site d'Aix-en-Provence, dans le cadre d'un projet pédagogique de communication et de webmarketing.</p>
  <p>Flexarion, son équipe et son jeu sont <strong>fictifs</strong>. Contact : <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <h2>Hébergement</h2>
  <p>GitHub Pages — GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
  <h2>Données personnelles et cookies</h2>
  <p>Ce site ne dépose aucun cookie et ne collecte aucune donnée personnelle. Les polices d'écriture sont chargées depuis Google Fonts. Les messages envoyés par courriel ne servent qu'à vous répondre.</p>
  <h2>Propriété intellectuelle</h2>
  <p>Les textes et illustrations ont été créés pour ce projet, avec l'aide d'outils d'intelligence artificielle dont l'usage est documenté par le groupe. Les éléments du kit presse peuvent être librement réutilisés pour parler de Flexarion.</p>
</div></section>'''
    return page("mentions-legales.html", "Mentions légales | Flexarion",
                "Mentions légales du site de Flexarion, studio de jeux vidéo indépendant à Aix-en-Provence.", corps, ld(fil(crumbs)))


def erreur():
    corps = f'''
<section class="heros-page" style="min-height:80svh;display:grid;align-items:center" aria-labelledby="titre">
  <span class="heros-page__kanji" aria-hidden="true">無</span>
  <div class="container--etroit centre">
    <p class="heros__sur">Erreur 404</p>
    <h1 id="titre">Cette page s'est perdue dans le vide</h1>
    <p class="chapeau" style="margin-inline:auto">Même un ronin ne peut trancher ce qui n'existe pas.</p>
    <div class="actions" style="justify-content:center"><a class="btn btn--plein" href="{SITE}/">Retour à l'accueil</a><a class="btn" href="{SITE}/jeu.html">Découvrir le jeu</a></div>
  </div>
</section>'''
    html = page("404.html", "Page introuvable | Flexarion", "Cette page du site Flexarion n'existe pas.", corps, "", noindex=True)
    # La 404 peut s'afficher à n'importe quelle profondeur : ressources en chemins absolus
    for a in ['href="favicon.svg"', 'href="icon-192.png"', 'href="apple-touch-icon.png"', 'href="site.webmanifest"',
              'href="assets/', 'src="assets/', 'href="index.html"', 'href="jeu.html', 'href="studio.html"',
              'href="devlog/', 'href="contact.html"', 'href="mentions-legales.html"']:
        html = html.replace(a, a.replace('="', '="/'))
    return html


REDIRECTIONS = {
    "maestral.html": "jeu.html",
    "devlog/simuler-le-vent-solaire.html": "devlog/parade-posture-apesanteur-systeme-de-combat.html",
    "devlog/direction-artistique-science-fiction-provence.html": "devlog/direction-artistique-encre-or-et-vide.html",
    "devlog/premiere-demo-maestral-bilan-playtest.html": "devlog/index.html",
    "devlog/bande-son-maestral-enregistrer-le-mistral.html": "devlog/index.html",
}


def redirection(cible):
    u = url(cible)
    return (f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Flexarion</title>'
            f'<link rel="canonical" href="{u}"><meta http-equiv="refresh" content="0; url={u}">'
            f'<script>location.replace("{u}")</script></head><body><p><a href="{u}">Flexarion</a></p></body></html>\n')


def ecrire(chemin, contenu):
    f = ROOT / chemin
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(contenu, encoding="utf-8")


def main():
    ecrire("index.html", accueil())
    ecrire("jeu.html", jeu())
    ecrire("studio.html", studio())
    ecrire("devlog/index.html", devlog_index())
    for i, p in enumerate(POSTS):
        ecrire(f"devlog/{p['slug']}.html", billet(p, i))
    ecrire("contact.html", contact())
    ecrire("mentions-legales.html", mentions())
    ecrire("404.html", erreur())
    for src, cible in REDIRECTIONS.items():
        ecrire(src, redirection(cible))

    pages = [("", "1.0", TODAY), ("jeu.html", "0.9", TODAY), ("studio.html", "0.8", TODAY),
             ("devlog/index.html", "0.8", POSTS[0]["date"]), ("contact.html", "0.6", TODAY)]
    pages += [(f"devlog/{p['slug']}.html", "0.7", p.get("maj", p["date"])) for p in POSTS]
    pages += [("mentions-legales.html", "0.2", TODAY)]
    ecrire("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "".join(f"  <url><loc>{url(p)}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>\n" for p, pr, d in pages)
           + "</urlset>\n")
    ecrire("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {url('sitemap.xml')}\n")

    items = "".join(f"""  <item>
    <title>{escape(f"Devlog {p['num']} — {p['titre']}")}</title>
    <link>{url(f"devlog/{p['slug']}.html")}</link>
    <guid isPermaLink="true">{url(f"devlog/{p['slug']}.html")}</guid>
    <pubDate>{format_datetime(datetime.fromisoformat(p['date']).replace(hour=9, tzinfo=timezone.utc))}</pubDate>
    <description>{escape(p['chapo'])}</description>
  </item>
""" for p in POSTS)
    ecrire("devlog/feed.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Devlog Flexarion</title>
  <link>{url('devlog/index.html')}</link>
  <atom:link href="{url('devlog/feed.xml')}" rel="self" type="application/rss+xml"/>
  <description>Le journal de développement de Ronin of the Black Sun, souls-like de science-fiction du studio Flexarion (Aix-en-Provence).</description>
  <language>fr-FR</language>
{items}</channel>
</rss>
""")
    ecrire("site.webmanifest", json.dumps({
        "name": "Flexarion — studio de jeux vidéo indépendant", "short_name": "Flexarion", "lang": "fr", "start_url": "./",
        "display": "browser", "background_color": "#08070b", "theme_color": "#08070b",
        "icons": [{"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"},
                  {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=2) + "\n")
    print("Site généré.")


if __name__ == "__main__":
    main()
