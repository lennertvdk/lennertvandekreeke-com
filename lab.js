// A few hundred dots wired up like neurons. Each dot collects input; when it
// crosses a threshold it fires, rests for a moment, and sends signals along its
// connections. Signals that arrive add input to the next dot, so activity can
// spread. The cursor (or a finger) excites dots nearby; a click or tap makes a
// whole cluster fire in a ripple. Colours come from the site's theme tokens.
(function () {
  var canvas = document.querySelector(".lab-canvas");
  if (!canvas) return;
  var ctx = canvas.getContext("2d");
  var counter = document.querySelector(".lab-count");
  var reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  var THRESHOLD = 1;
  var SIGNAL_WEIGHT = 0.46; // input a dot gets when a signal arrives
  var LEAK_MS = 420; // how fast collected input fades
  var REST_MS = 520; // refractory period after firing
  var SIGNAL_SPEED = 0.22; // pixels per millisecond
  var SPONTANEOUS = reduceMotion ? 0 : 0.015; // fires per dot per second
  var REACH = 110; // cursor radius
  var MAX_SIGNALS = 1600;

  var W, H, nodes, signals, colors = {}, spikes = 0, last = 0;
  var pointer = { x: -1e4, y: -1e4, speed: 0, inside: false };

  function readColors() {
    var style = getComputedStyle(document.documentElement);
    ["paper", "ink", "muted", "rule", "accent"].forEach(function (k) {
      colors[k] = style.getPropertyValue("--" + k).trim();
    });
  }

  function build() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = canvas.clientWidth;
    H = canvas.clientHeight;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    // A jittered grid spreads the dots evenly without looking like a grid.
    var target = Math.max(70, Math.min(420, Math.round((W * H) / 5000)));
    var cols = Math.max(4, Math.round(Math.sqrt((target * W) / H)));
    var rows = Math.max(4, Math.round(target / cols));
    var cw = W / cols, ch = H / rows;
    nodes = [];
    for (var r = 0; r < rows; r++) {
      for (var c = 0; c < cols; c++) {
        var ax = (c + 0.5 + (Math.random() - 0.5) * 0.85) * cw;
        var ay = (r + 0.5 + (Math.random() - 0.5) * 0.85) * ch;
        nodes.push({
          i: nodes.length, ax: ax, ay: ay, x: ax, y: ay,
          phase: Math.random() * Math.PI * 2,
          freq: 0.00015 + Math.random() * 0.0002,
          amp: reduceMotion ? 0 : 2 + Math.random() * 5,
          v: 0, restUntil: 0, glow: 0, due: 0, links: []
        });
      }
    }

    // Connect each dot to its three nearest neighbours (both ways).
    var maxDist = Math.max(cw, ch) * 2.2;
    nodes.forEach(function (n) {
      var near = nodes
        .filter(function (m) { return m !== n; })
        .map(function (m) { return { m: m, d: Math.hypot(m.ax - n.ax, m.ay - n.ay) }; })
        .filter(function (o) { return o.d < maxDist; })
        .sort(function (p, q) { return p.d - q.d; })
        .slice(0, 3);
      near.forEach(function (o) {
        if (n.links.indexOf(o.m) < 0) n.links.push(o.m);
        if (o.m.links.indexOf(n) < 0) o.m.links.push(n);
      });
    });
    signals = [];
  }

  function fire(n, now) {
    if (now < n.restUntil) return;
    n.restUntil = now + REST_MS;
    n.v = 0;
    n.glow = 1;
    spikes++;
    for (var k = 0; k < n.links.length && signals.length < MAX_SIGNALS; k++) {
      var m = n.links[k];
      signals.push({ a: n, b: m, t: 0, len: Math.hypot(m.x - n.x, m.y - n.y) || 1 });
    }
  }

  function step(now) {
    var dt = Math.min(now - (last || now), 50);
    last = now;
    var leak = Math.exp(-dt / LEAK_MS);

    nodes.forEach(function (n) {
      n.x = n.ax + Math.sin(now * n.freq + n.phase) * n.amp;
      n.y = n.ay + Math.cos(now * n.freq * 0.8 + n.phase * 1.3) * n.amp;
      n.v *= leak;
      n.glow = Math.max(0, n.glow - dt / 900);

      if (n.due && now >= n.due) {
        n.due = 0;
        fire(n, now);
      }
      if (pointer.inside) {
        var d = Math.hypot(n.x - pointer.x, n.y - pointer.y);
        if (d < REACH) {
          n.v += (1 - d / REACH) * (0.5 + Math.min(pointer.speed, 2.5)) * dt * 0.01;
        }
      }
      if (Math.random() < SPONTANEOUS * dt * 0.001) n.v += THRESHOLD;
      if (n.v >= THRESHOLD) fire(n, now);
    });
    pointer.speed *= Math.exp(-dt / 120);

    for (var i = signals.length - 1; i >= 0; i--) {
      var s = signals[i];
      s.t += (SIGNAL_SPEED * dt) / s.len;
      if (s.t >= 1) {
        if (now >= s.b.restUntil) s.b.v += SIGNAL_WEIGHT;
        signals.splice(i, 1);
      }
    }
  }

  function draw() {
    ctx.fillStyle = colors.paper;
    ctx.fillRect(0, 0, W, H);

    // Connections: faint everywhere, a little clearer around the cursor.
    ctx.lineWidth = 1;
    ctx.strokeStyle = colors.rule;
    ctx.beginPath();
    nodes.forEach(function (n) {
      n.links.forEach(function (m) {
        if (m.i > n.i) {
          ctx.moveTo(n.x, n.y);
          ctx.lineTo(m.x, m.y);
        }
      });
    });
    ctx.stroke();

    if (pointer.inside) {
      ctx.strokeStyle = colors.muted;
      nodes.forEach(function (n) {
        n.links.forEach(function (m) {
          if (m.i < n.i) return;
          var d = Math.hypot((n.x + m.x) / 2 - pointer.x, (n.y + m.y) / 2 - pointer.y);
          if (d > REACH * 1.6) return;
          ctx.globalAlpha = (1 - d / (REACH * 1.6)) * 0.55;
          ctx.beginPath();
          ctx.moveTo(n.x, n.y);
          ctx.lineTo(m.x, m.y);
          ctx.stroke();
        });
      });
      ctx.globalAlpha = 1;
    }

    // Signals travelling along connections, drawn as short streaks.
    ctx.strokeStyle = colors.accent;
    ctx.lineWidth = 1.6;
    ctx.lineCap = "round";
    ctx.beginPath();
    signals.forEach(function (s) {
      var t0 = Math.max(0, s.t - 18 / s.len);
      ctx.moveTo(s.a.x + (s.b.x - s.a.x) * t0, s.a.y + (s.b.y - s.a.y) * t0);
      ctx.lineTo(s.a.x + (s.b.x - s.a.x) * s.t, s.a.y + (s.b.y - s.a.y) * s.t);
    });
    ctx.stroke();

    // Dots, swelling slightly as they charge; a ring spreads out when one fires.
    nodes.forEach(function (n) {
      ctx.fillStyle = colors.muted;
      ctx.beginPath();
      ctx.arc(n.x, n.y, 1.5 + Math.min(n.v, 1) * 1.6, 0, Math.PI * 2);
      ctx.fill();
      if (n.glow > 0) {
        ctx.globalAlpha = n.glow;
        ctx.fillStyle = colors.accent;
        ctx.beginPath();
        ctx.arc(n.x, n.y, 3.2, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = colors.accent;
        ctx.lineWidth = 1;
        ctx.globalAlpha = n.glow * 0.6;
        ctx.beginPath();
        ctx.arc(n.x, n.y, 4 + (1 - n.glow) * 22, 0, Math.PI * 2);
        ctx.stroke();
        ctx.globalAlpha = 1;
      }
    });
  }

  function frame(now) {
    step(now);
    draw();
    requestAnimationFrame(frame);
  }

  // A click or tap fires every dot nearby, outward from the point like a ripple.
  function burst(x, y) {
    var now = performance.now();
    nodes.forEach(function (n) {
      var d = Math.hypot(n.x - x, n.y - y);
      if (d < REACH * 1.4) n.due = now + d * 2.2;
    });
  }

  function setPointer(e) {
    var rect = canvas.getBoundingClientRect();
    var x = e.clientX - rect.left, y = e.clientY - rect.top;
    if (pointer.inside) {
      var moved = Math.hypot(x - pointer.x, y - pointer.y);
      pointer.speed = Math.max(pointer.speed, moved / 16);
    }
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

  // Follow the theme toggle and the system setting.
  new MutationObserver(readColors).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", readColors);

  setInterval(function () {
    if (counter) counter.textContent = spikes.toLocaleString(document.documentElement.lang);
  }, 250);

  readColors();
  build();
  requestAnimationFrame(frame);
})();
