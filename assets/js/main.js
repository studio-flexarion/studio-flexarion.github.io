/* Flexarion — animations et interactions (sans dépendance) */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var calme = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- En-tête : fond au défilement, masqué en descendant ---------- */
  var entete = document.querySelector(".entete");
  var dernierY = 0;
  function surDefilement() {
    var y = window.scrollY;
    if (entete) {
      entete.classList.toggle("est-solide", y > 40);
      entete.classList.toggle("est-cache", y > 400 && y > dernierY && !document.body.classList.contains("menu-ouvert"));
    }
    dernierY = y;
  }
  window.addEventListener("scroll", surDefilement, { passive: true });
  surDefilement();

  /* ---------- Menu mobile ---------- */
  var burger = document.querySelector(".burger");
  if (burger) {
    burger.addEventListener("click", function () {
      var ouvert = document.body.classList.toggle("menu-ouvert");
      burger.setAttribute("aria-expanded", ouvert ? "true" : "false");
    });
    document.querySelectorAll(".nav a").forEach(function (a) {
      a.addEventListener("click", function () { document.body.classList.remove("menu-ouvert"); });
    });
  }

  /* ---------- Titre lettre par lettre ---------- */
  document.querySelectorAll(".titre-lettres").forEach(function (el) {
    var texte = el.textContent;
    el.setAttribute("aria-label", texte);
    el.textContent = "";
    Array.prototype.forEach.call(texte, function (c, i) {
      var s = document.createElement("span");
      s.className = "l";
      s.setAttribute("aria-hidden", "true");
      s.style.setProperty("--i", i);
      s.textContent = c === " " ? " " : c; // une espace seule dans un inline-block s'effondrerait
      el.appendChild(s);
    });
  });

  /* ---------- Apparitions au défilement ---------- */
  var cibles = document.querySelectorAll(".revele, .revele-encre, .entaille, .enso, [data-compteur]");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("est-vu");
        if (e.target.hasAttribute("data-compteur")) compter(e.target);
        io.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: .12 });
    cibles.forEach(function (c) { io.observe(c); });
  } else {
    cibles.forEach(function (c) { c.classList.add("est-vu"); });
  }

  /* ---------- Compteurs ---------- */
  function compter(el) {
    var fin = parseInt(el.getAttribute("data-compteur"), 10);
    if (calme || isNaN(fin)) { el.textContent = fin; return; }
    var debut = fin > 1000 ? fin - 30 : 0, t0 = null, duree = 1600;
    function pas(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / duree, 1);
      el.textContent = Math.round(debut + (fin - debut) * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(pas);
    }
    requestAnimationFrame(pas);
  }

  /* ---------- Parallaxe du héros + lueur sous la souris ---------- */
  var fond = document.querySelector(".heros__fond");
  var heros = document.querySelector(".heros, .heros-page--image");
  if (fond && heros && !calme) {
    var sx = 0, sy = 0, cx = 0, cy = 0, sc = 0;
    window.addEventListener("scroll", function () { sc = window.scrollY; }, { passive: true });
    heros.addEventListener("pointermove", function (e) {
      var r = heros.getBoundingClientRect();
      sx = (e.clientX - r.left) / r.width - .5;
      sy = (e.clientY - r.top) / r.height - .5;
      var lueur = heros.querySelector(".lueur");
      if (lueur) { lueur.style.left = (e.clientX - r.left) + "px"; lueur.style.top = (e.clientY - r.top) + "px"; }
    });
    (function boucle() {
      cx += (sx - cx) * .05; cy += (sy - cy) * .05;
      if (sc < window.innerHeight * 1.2) {
        fond.style.transform = "translate3d(" + (cx * -24) + "px," + (cy * -16 + sc * .25) + "px,0)";
      }
      requestAnimationFrame(boucle);
    })();
  }

  /* ---------- Braises (particules) ---------- */
  var toile = document.querySelector(".braises");
  if (toile && !calme) {
    var ctx = toile.getContext("2d"), W, H, dpr = Math.min(window.devicePixelRatio || 1, 2), braises = [];
    var couleurs = ["236,217,164", "255,154,74", "217,71,59", "201,164,92"];
    function taille() {
      W = toile.clientWidth; H = toile.clientHeight;
      toile.width = W * dpr; toile.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function nouvelle(bas) {
      return {
        x: Math.random() * W, y: bas ? H + 10 : Math.random() * H,
        r: Math.random() * 1.8 + .4, vy: Math.random() * .6 + .25, vx: (Math.random() - .5) * .3,
        a: Math.random() * .7 + .25, phase: Math.random() * 6.28, c: couleurs[(Math.random() * couleurs.length) | 0]
      };
    }
    taille();
    var nb = Math.min(110, Math.round(W / 12));
    for (var i = 0; i < nb; i++) braises.push(nouvelle(false));
    window.addEventListener("resize", taille);
    var visible = true;
    new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(toile);
    (function anim(t) {
      if (visible) {
        ctx.clearRect(0, 0, W, H);
        ctx.globalCompositeOperation = "lighter";
        for (var j = 0; j < braises.length; j++) {
          var b = braises[j];
          b.y -= b.vy; b.x += b.vx + Math.sin(t / 1400 + b.phase) * .35;
          if (b.y < -10) braises[j] = b = nouvelle(true);
          var scint = b.a * (.6 + .4 * Math.sin(t / 300 + b.phase));
          var g = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, b.r * 4);
          g.addColorStop(0, "rgba(" + b.c + "," + scint + ")");
          g.addColorStop(1, "rgba(" + b.c + ",0)");
          ctx.fillStyle = g;
          ctx.beginPath(); ctx.arc(b.x, b.y, b.r * 4, 0, 6.283); ctx.fill();
        }
      }
      requestAnimationFrame(anim);
    })(0);
  }

  /* ---------- Les Sept Daimyō ---------- */
  var liste = document.querySelector("[data-daimyos]");
  if (liste) {
    var desc = document.querySelector("[data-daimyo-desc]");
    var boutons = liste.querySelectorAll("button");
    boutons.forEach(function (b) {
      function choisir() {
        boutons.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        desc.style.opacity = 0;
        setTimeout(function () { desc.textContent = b.getAttribute("data-desc"); desc.style.opacity = 1; }, 180);
      }
      b.addEventListener("click", choisir);
      b.addEventListener("mouseenter", choisir);
    });
  }

  /* ---------- Visionneuse d'images ---------- */
  var liens = document.querySelectorAll("[data-visionneuse]");
  if (liens.length) {
    var v = document.createElement("div");
    v.className = "visionneuse";
    v.setAttribute("role", "dialog");
    v.setAttribute("aria-modal", "true");
    v.setAttribute("aria-label", "Illustration agrandie");
    v.innerHTML = '<figure><img alt=""><p></p></figure><button type="button" aria-label="Fermer">×</button>';
    document.body.appendChild(v);
    var vImg = v.querySelector("img"), vTxt = v.querySelector("p"), vBtn = v.querySelector("button"), origine;
    function fermer() { v.classList.remove("ouverte"); if (origine) origine.focus(); }
    liens.forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        origine = a;
        var img = a.querySelector("img");
        vImg.src = a.getAttribute("href"); vImg.alt = img ? img.alt : "";
        vTxt.textContent = a.getAttribute("data-legende") || "";
        v.classList.add("ouverte");
        vBtn.focus();
      });
    });
    vBtn.addEventListener("click", fermer);
    v.addEventListener("click", function (e) { if (e.target === v) fermer(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && v.classList.contains("ouverte")) fermer(); });
  }
})();
