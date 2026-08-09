/* ==========================================================================
   Elite Guard SA — Comportamiento del sitio
   1. Menú desplegable en celular
   2. Año automático en el pie de página
   3. Validación del formulario de contacto
   ========================================================================== */

(function () {
  "use strict";

  /* ----------------------------------------------------------------------
     1. Menú desplegable (solo se muestra en pantallas pequeñas)
     ---------------------------------------------------------------------- */

  var botonMenu = document.querySelector(".menu-boton");
  var menu = document.getElementById("menu-principal");

  if (botonMenu && menu) {
    botonMenu.addEventListener("click", function () {
      var estaAbierto = botonMenu.getAttribute("aria-expanded") === "true";
      botonMenu.setAttribute("aria-expanded", String(!estaAbierto));
      botonMenu.setAttribute(
        "aria-label",
        estaAbierto ? "Abrir menú de navegación" : "Cerrar menú de navegación"
      );
      menu.classList.toggle("esta-abierto", !estaAbierto);
    });

    // Cerrar el menú con la tecla Escape
    document.addEventListener("keydown", function (evento) {
      if (evento.key === "Escape" && menu.classList.contains("esta-abierto")) {
        botonMenu.setAttribute("aria-expanded", "false");
        botonMenu.setAttribute("aria-label", "Abrir menú de navegación");
        menu.classList.remove("esta-abierto");
        botonMenu.focus();
      }
    });
  }

  /* ----------------------------------------------------------------------
     2. Año actual en el pie de página
     ---------------------------------------------------------------------- */

  var anio = document.getElementById("anio");
  if (anio) {
    anio.textContent = String(new Date().getFullYear());
  }

  /* ----------------------------------------------------------------------
     3. Formulario de contacto
     ---------------------------------------------------------------------- */

  var formulario = document.getElementById("formulario-contacto");
  if (!formulario) {
    return;
  }

  var mensajeEnvio = document.getElementById("mensaje-envio");

  // Reglas de validación por campo
  var reglas = {
    nombre: function (valor) {
      if (valor.length === 0) return "Escriba su nombre completo.";
      if (valor.length < 3) return "El nombre debe tener al menos 3 caracteres.";
      return "";
    },
    correo: function (valor) {
      if (valor.length === 0) return "Escriba su correo electrónico.";
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(valor)) {
        return "El correo no tiene un formato válido.";
      }
      return "";
    },
    telefono: function (valor) {
      if (valor.length === 0) return ""; // campo opcional
      if (!/^[\d\s()+-]{8,20}$/.test(valor)) {
        return "Use solo números, espacios y los signos + ( ) -";
      }
      return "";
    },
    mensaje: function (valor) {
      if (valor.length === 0) return "Escriba su mensaje.";
      if (valor.length < 10) return "El mensaje debe tener al menos 10 caracteres.";
      return "";
    }
  };

  /**
   * Valida un campo y pinta u oculta su mensaje de error.
   * Devuelve true si el campo es válido.
   */
  function validarCampo(campo) {
    var regla = reglas[campo.name];
    if (!regla) return true;

    var error = regla(campo.value.trim());
    var contenedorError = document.getElementById("error-" + campo.name);

    if (contenedorError) {
      contenedorError.textContent = error;
    }
    campo.setAttribute("aria-invalid", error ? "true" : "false");

    return error === "";
  }

  // Al salir de un campo, se valida de inmediato
  Object.keys(reglas).forEach(function (nombre) {
    var campo = formulario.elements[nombre];
    if (!campo) return;

    campo.addEventListener("blur", function () {
      validarCampo(campo);
    });

    // Una vez marcado como inválido, se revalida mientras se escribe
    campo.addEventListener("input", function () {
      if (campo.getAttribute("aria-invalid") === "true") {
        validarCampo(campo);
      }
    });
  });

  function mostrarMensaje(texto, tipo) {
    if (!mensajeEnvio) return;
    mensajeEnvio.textContent = texto;
    mensajeEnvio.className = "mensaje-envio mensaje-envio--" + tipo;
    mensajeEnvio.hidden = false;
  }

  formulario.addEventListener("submit", function (evento) {
    evento.preventDefault();

    // Si el campo trampa viene lleno, es un robot: se ignora en silencio
    if (formulario.elements["sitio-web"] && formulario.elements["sitio-web"].value) {
      return;
    }

    var primerInvalido = null;
    var todoValido = true;

    Object.keys(reglas).forEach(function (nombre) {
      var campo = formulario.elements[nombre];
      if (!campo) return;

      if (!validarCampo(campo)) {
        todoValido = false;
        if (!primerInvalido) primerInvalido = campo;
      }
    });

    if (!todoValido) {
      mostrarMensaje("Revise los campos marcados en rojo.", "error");
      if (primerInvalido) primerInvalido.focus();
      return;
    }

    enviar();
  });

  /**
   * Envía el formulario.
   *
   * Si el atributo data-endpoint del formulario apunta a un servicio real
   * (por ejemplo Formspree o una API propia), se envía por fetch. Mientras
   * no exista ese servicio, se abre el cliente de correo del visitante con
   * el mensaje ya redactado.
   */
  function enviar() {
    var datos = new FormData(formulario);
    var endpoint = formulario.dataset.endpoint;

    if (endpoint) {
      mostrarMensaje("Enviando su solicitud…", "exito");

      fetch(endpoint, {
        method: "POST",
        body: datos,
        headers: { Accept: "application/json" }
      })
        .then(function (respuesta) {
          if (!respuesta.ok) throw new Error("Respuesta no válida del servidor");
          formulario.reset();
          mostrarMensaje(
            "¡Gracias! Recibimos su solicitud y le responderemos en un plazo máximo de 24 horas hábiles.",
            "exito"
          );
        })
        .catch(function () {
          mostrarMensaje(
            "No pudimos enviar el formulario. Escríbanos directamente a michael@eliteguardsa.com.",
            "error"
          );
        });

      return;
    }

    // Alternativa sin servidor: abrir el correo con los datos ya escritos
    var cuerpo =
      "Nombre: " + datos.get("nombre") + "\n" +
      "Correo: " + datos.get("correo") + "\n" +
      "Teléfono: " + (datos.get("telefono") || "No indicado") + "\n" +
      "Servicio: " + (datos.get("servicio") || "No indicado") + "\n\n" +
      "Mensaje:\n" + datos.get("mensaje");

    var enlace =
      "mailto:michael@eliteguardsa.com" +
      "?subject=" + encodeURIComponent("Solicitud de cotización — sitio web") +
      "&body=" + encodeURIComponent(cuerpo);

    window.location.href = enlace;

    mostrarMensaje(
      "Se abrió su aplicación de correo con la solicitud lista para enviar. " +
        "Si no se abrió, escríbanos a michael@eliteguardsa.com.",
      "exito"
    );
  }
})();
