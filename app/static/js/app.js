// AgendaFácil — validações e interações do front-end
(function () {
  "use strict";

  // Máscara de telefone: (61) 99999-9999
  document.querySelectorAll('[data-mascara="telefone"]').forEach(function (campo) {
    campo.addEventListener("input", function () {
      var d = campo.value.replace(/\D/g, "").slice(0, 11);
      var f = d;
      if (d.length > 2) f = "(" + d.slice(0, 2) + ") " + d.slice(2);
      if (d.length > 6) {
        var corte = d.length === 11 ? 7 : 6;
        f = "(" + d.slice(0, 2) + ") " + d.slice(2, corte) + "-" + d.slice(corte);
      }
      campo.value = f;
    });
  });

  // Confirmação antes de ações destrutivas
  document.querySelectorAll("form[data-confirmar]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!window.confirm(form.getAttribute("data-confirmar"))) e.preventDefault();
    });
  });

  // Validação no navegador com mensagens em português
  function mensagem(campo) {
    var v = campo.validity;
    if (v.valueMissing) return "Campo obrigatório.";
    if (v.typeMismatch && campo.type === "email") return "Informe um e-mail válido.";
    if (v.tooShort) return "Mínimo de " + campo.minLength + " caracteres.";
    if (v.rangeUnderflow) return "Valor mínimo: " + campo.min + ".";
    if (v.rangeOverflow) return "Valor máximo: " + campo.max + ".";
    if (campo.dataset.mascara === "telefone") {
      var n = campo.value.replace(/\D/g, "").length;
      if (n !== 10 && n !== 11) return "Telefone deve ter DDD + número.";
    }
    return "";
  }

  document.querySelectorAll("form[data-validar]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      var primeiro = null;
      form.querySelectorAll(".msg-campo").forEach(function (m) { m.remove(); });
      form.querySelectorAll("input, select, textarea").forEach(function (campo) {
        campo.classList.remove("invalido");
        if (campo.type === "hidden") return;
        var msg = mensagem(campo);
        if (msg) {
          campo.classList.add("invalido");
          var span = document.createElement("span");
          span.className = "msg-campo";
          span.textContent = msg;
          campo.insertAdjacentElement("afterend", span);
          primeiro = primeiro || campo;
        }
      });
      if (primeiro) { e.preventDefault(); primeiro.focus(); }
    });
  });

  // Alertas somem sozinhos após 6 segundos
  setTimeout(function () {
    document.querySelectorAll(".alerta-sucesso").forEach(function (a) { a.remove(); });
  }, 6000);
})();
