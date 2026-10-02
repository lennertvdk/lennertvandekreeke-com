// A few hundred dots wired up like neurons. Nothing happens on its own: dots
// only light up where the cursor (or a finger) passes. A lit dot glows in a
// colour that depends on where it sits, so the field forms a slow rainbow, and
// it passes a little light along its connections to its neighbours before
// everything fades back. A click or tap lights a whole patch in a ripple.
(function () {
  var canvas = document.querySelector(".lab-canvas");
  if (!canvas) return;
  var ctx = canvas.getContext("2d");
  var counter = document.querySelector(".lab-count");
  var reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  var FADE_MS = 4200; // how long a glow takes to fade
  var FIRE_AT = 0.55; // energy at which a dot passes light to its neighbours
  var REST_MS = 3000; // a dot passes light on at most once in this time
  var SIGNAL_SPEED = 0.045; // pixels per millisecond
  var SIGNAL_GIFT = 0.18; // energy a neighbour receives from an arriving signal
  var REACH = 120; // cursor radius
  var MAX_SIGNALS = 900;

  var W, H, nodes, signals, colors = {}, dark = false, lit = 0, last = 0;
  var pointer = { x: -1e4, y: -1e4, speed: 0, inside: false };

  function readColors() {
    var style = getComputedStyle(document.documentElement);
    ["paper", "ink", "muted", "rule", "accent"].forEach(function (k) {
      colors[k] = style.getPropertyValue("--" + k).trim();
    });
    dark = colors.paper.toLowerCase() !== "#f5f3ee";
  }

  // The hue comes from a dot's position and drifts very slowly over time.
  function hue(n, now) {
    return (n.ax / W) * 300 + (n.ay / H) * 60 + now * 0.002;
  }

  function hsla(h, a) {
    return "hsla(" + (h % 360) + "," + (dark ? "85%,64%," : "78%,52%,") + a + ")";
  }

  function build() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = canvas.clientWidth;
    H = canvas.clientHeight;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    var target = Math.max(70, Math.min(400, Math.round((W * H) / 5200)));
    var cols = Math.max(4, Math.round(Math.sqrt((target * W) / H)));
    var rows = Math.max(4, Math.round(target / cols));
    var cw = W / cols, ch = H / rows;
    nodes = [];
    for (var r = 0; r < rows; r++) {
      for (var c = 0; c < cols; c++) {
        var ax = (c + 0.5 + (Math.random() - 0.5) * 0.9) * cw;
        var ay = (r + 0.5 + (Math.random() - 0.5) * 0.9) * ch;
        nodes.push({
          i: nodes.length, ax: ax, ay: ay, x: ax, y: ay,
          size: 1.1 + Math.random() * 1.3,
          phase: Math.random() * Math.PI * 2,
          freq: 0.00003 + Math.random() * 0.00004,
          amp: reduceMotion ? 0 : 3 + Math.random() * 6,
          energy: 0, restUntil: 0, due: 0, links: [],
          bend: (Math.random() - 0.5) * 0.35
        });
      }
    }

    var maxDist = Math.max(cw, ch) * 2.2;
    nodes.forEach(function (n) {
      nodes
        .filter(function (m) { return m !== n; })
        .map(function (m) { return { m: m, d: Math.hypot(m.ax - n.ax, m.ay - n.ay) }; })
        .filter(function (o) { return o.d < maxDist; })
        .sort(function (p, q) { return p.d - q.d; })
        .slice(0, 3)
        .forEach(function (o) {
          if (n.links.indexOf(o.m) < 0) n.links.push(o.m);
          if (o.m.links.indexOf(n) < 0) o.m.links.push(n);
        });
    });
    signals = [];
  }

  // Connections are drawn as gentle curves rather than straight lines.
  function curvePoint(a, b, t) {
    var mx = (a.x + b.x) / 2 - (b.y - a.y) * a.bend;
    var my = (a.y + b.y) / 2 + (b.x - a.x) * a.bend;
    var u = 1 - t;
    return { x: u * u * a.x + 2 * u * t * mx + t * t * b.x, y: u * u * a.y + 2 * u * t * my + t * t * b.y };
  }

  function strokeCurve(a, b) {
    var mx = (a.x + b.x) / 2 - (b.y - a.y) * a.bend;
    var my = (a.y + b.y) / 2 + (b.x - a.x) * a.bend;
    ctx.moveTo(a.x, a.y);
    ctx.quadraticCurveTo(mx, my, b.x, b.y);
  }

  function passOn(n, now) {
    if (now < n.restUntil) return;
    n.restUntil = now + REST_MS;
    lit++;
    for (var k = 0; k < n.links.length && signals.length < MAX_SIGNALS; k++) {
      var m = n.links[k];
      signals.push({ a: n, b: m, t: 0, len: Math.hypot(m.x - n.x, m.y - n.y) * 1.1 || 1, hue: hue(n, now) });
    }
  }

  function step(now) {
    var dt = Math.min(now - (last || now), 50);
    last = now;
    var fade = Math.exp(-dt / FADE_MS);

    nodes.forEach(function (n) {
      n.x = n.ax + Math.sin(now * n.freq + n.phase) * n.amp;
      n.y = n.ay + Math.cos(now * n.freq * 0.8 + n.phase * 1.3) * n.amp;
      n.energy *= fade;

      if (n.due && now >= n.due) {
        n.due = 0;
        n.energy = Math.min(1, n.energy + 0.9);
      }
      if (pointer.inside) {
        var d = Math.hypot(n.x - pointer.x, n.y - pointer.y);
        if (d < REACH) {
          var closeness = 1 - d / REACH;
          n.energy = Math.min(1, n.energy + closeness * closeness * (0.3 + Math.min(pointer.speed, 2)) * dt * 0.0022);
        }
      }
      if (n.energy >= FIRE_AT) passOn(n, now);
    });
    pointer.speed *= Math.exp(-dt / 200);

    for (var i = signals.length - 1; i >= 0; i--) {
      var s = signals[i];
      s.t += (SIGNAL_SPEED * dt) / s.len;
      if (s.t >= 1) {
        s.b.energy = Math.min(1, s.b.energy + SIGNAL_GIFT);
        signals.splice(i, 1);
      }
    }
  }

  function draw(now) {
    ctx.globalCompositeOperation = "source-over";
    ctx.fillStyle = colors.paper;
    ctx.fillRect(0, 0, W, H);

    // Resting connections.
    ctx.lineWidth = 1;
    ctx.strokeStyle = colors.rule;
    ctx.beginPath();
    nodes.forEach(function (n) {
      n.links.forEach(function (m) {
        if (m.i > n.i) strokeCurve(n, m);
      });
    });
    ctx.stroke();

    // Soft glows first, so dots and lines sit on top of them.
    ctx.globalCompositeOperation = dark ? "lighter" : "multiply";
    nodes.forEach(function (n) {
      if (n.energy < 0.02) return;
      var radius = 8 + n.energy * 34;
      var g = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, radius);
      var h = hue(n, now);
      g.addColorStop(0, hsla(h, n.energy * (dark ? 0.45 : 0.35)));
      g.addColorStop(1, hsla(h, 0));
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(n.x, n.y, radius, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.globalCompositeOperation = "source-over";

    // Connections between lit dots take on their colour.
    ctx.lineWidth = 1.2;
    nodes.forEach(function (n) {
      n.links.forEach(function (m) {
        if (m.i < n.i) return;
        var e = (n.energy + m.energy) / 2;
        if (e < 0.05) return;
        ctx.strokeStyle = hsla(hue(n, now), Math.min(e * 1.2, 0.9));
        ctx.beginPath();
        strokeCurve(n, m);
        ctx.stroke();
      });
    });

    // Light travelling to neighbours, as short soft streaks along the curve.
    ctx.lineCap = "round";
    ctx.lineWidth = 2;
    signals.forEach(function (s) {
      var p0 = curvePoint(s.a, s.b, Math.max(0, s.t - 24 / s.len));
      var p1 = curvePoint(s.a, s.b, s.t);
      ctx.strokeStyle = hsla(s.hue, 0.85 * (1 - s.t * 0.5));
      ctx.beginPath();
      ctx.moveTo(p0.x, p0.y);
      ctx.lineTo(p1.x, p1.y);
      ctx.stroke();
    });

    // Dots: grey at rest, coloured and a little larger when lit.
    nodes.forEach(function (n) {
      ctx.fillStyle = n.energy > 0.05 ? hsla(hue(n, now), 0.4 + n.energy * 0.6) : colors.muted;
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.size + n.energy * 2.2, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  function frame(now) {
    step(now);
    draw(now);
    requestAnimationFrame(frame);
  }

  // A click or tap lights every dot nearby, outward from the point like a ripple.
  function burst(x, y) {
    var now = performance.now();
    nodes.forEach(function (n) {
      var d = Math.hypot(n.x - x, n.y - y);
      if (d < REACH * 1.6) n.due = now + d * 9;
    });
  }

  function setPointer(e) {
    var rect = canvas.getBoundingClientRect();
    var x = e.clientX - rect.left, y = e.clientY - rect.top;
    if (pointer.inside) pointer.speed = Math.max(pointer.speed, Math.hypot(x - pointer.x, y - pointer.y) / 16);
    pointer.x = x;
    pointer.y = y;
    pointer.inside = true;
  }

  canvas.addEventListener("pointermove", setPointer);
  canvas.addEventListener("pointerdown", function (e) {
    setPointer(e);
    burst(pointer.x, pointer.y);
  });
  canvas.addEventListener("pointerleave", function () { pointer.inside = false; });
  canvas.addEventListener("pointerup", function (e) {
    if (e.pointerType !== "mouse") pointer.inside = false;
  });

  var resizeTimer;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(build, 150);
  });

  new MutationObserver(readColors).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", readColors);

  setInterval(function () {
    if (counter) counter.textContent = lit.toLocaleString(document.documentElement.lang);
  }, 250);

  readColors();
  build();
  requestAnimationFrame(frame);
})();
