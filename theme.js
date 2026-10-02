// Light/dark toggle. Follows the system setting until the button is pressed,
// then remembers the choice. The stored theme is applied by a small inline
// script in <head> so the page doesn't flash on load. The button's labels
// come from data attributes so each language can set its own.
(function () {
  var root = document.documentElement;
  var button = document.querySelector(".theme-toggle");
  if (!button) return;

  function current() {
    if (root.dataset.theme) return root.dataset.theme;
    return matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function updateLabel() {
    button.setAttribute(
      "aria-label",
      current() === "dark" ? button.dataset.toLight : button.dataset.toDark
    );
  }

  function apply(next) {
    root.dataset.theme = next;
    try {
      localStorage.setItem("theme", next);
    } catch (e) {}
    updateLabel();
  }

  // The new theme spreads out from the button as a growing circle. Browsers
  // without view transitions, and people who prefer less motion, get an
  // instant switch.
  button.addEventListener("click", function () {
    var next = current() === "dark" ? "light" : "dark";
    var still = matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!document.startViewTransition || still) {
      apply(next);
      return;
    }
    var box = button.getBoundingClientRect();
    var x = box.left + box.width / 2;
    var y = box.top + box.height / 2;
    var radius = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    var transition = document.startViewTransition(function () {
      apply(next);
    });
    transition.ready.then(function () {
      root.animate(
        { clipPath: ["circle(0 at " + x + "px " + y + "px)", "circle(" + radius + "px at " + x + "px " + y + "px)"] },
        { duration: 550, easing: "cubic-bezier(0.4, 0, 0.2, 1)", pseudoElement: "::view-transition-new(root)" }
      );
    }).catch(function () {}); // aborted, e.g. in a background tab; the theme is already switched
  });

  updateLabel();
})();
