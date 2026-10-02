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

  button.addEventListener("click", function () {
    var next = current() === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try {
      localStorage.setItem("theme", next);
    } catch (e) {}
    updateLabel();
  });

  updateLabel();
})();
