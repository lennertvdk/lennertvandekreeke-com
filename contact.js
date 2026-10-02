// Sends the contact form to Formspree in the background, so visitors stay on
// the page. Without JavaScript the form still posts normally and Formspree
// shows its own confirmation page. Messages come from data attributes on the
// form so each language can set its own.
(function () {
  var form = document.querySelector(".contact-form");
  if (!form) return;
  var status = form.querySelector(".form-status");
  var button = form.querySelector("button");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    button.disabled = true;
    status.textContent = form.dataset.sending;

    fetch(form.action, {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "application/json" }
    })
      .then(function (response) {
        if (!response.ok) throw new Error(response.status);
        form.reset();
        status.textContent = form.dataset.success;
      })
      .catch(function () {
        status.textContent = form.dataset.error;
      })
      .finally(function () {
        button.disabled = false;
      });
  });
})();
