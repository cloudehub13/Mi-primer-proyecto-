# Elite Guard SA — Sitio web

Sitio web estático para Elite Guard SA (seguridad privada). Tres páginas en
español, diseño limpio y adaptado a celular (*mobile first*).

## Estructura

```
.
├── index.html        Inicio: presentación, ventajas, resumen de servicios
├── servicios.html    Detalle de los seis servicios y proceso de trabajo
├── contacto.html     Datos de contacto y formulario de cotización
├── css/
│   └── estilos.css   Todos los estilos (variables de color, mobile first)
└── js/
    └── principal.js  Menú de celular, año automático y validación del formulario
```

No usa frameworks ni dependencias: solo HTML, CSS y JavaScript.

## Cómo verlo

Abra `index.html` directamente en el navegador, o levante un servidor local:

```bash
python3 -m http.server 8000
# luego visite http://localhost:8000
```

## Formulario de contacto

El formulario valida los campos en el navegador (nombre, correo, teléfono y
mensaje) y tiene un campo trampa contra robots.

Como el sitio es estático, **todavía no envía correos por sí solo**. Funciona así:

- **Sin servicio configurado** (estado actual): al enviar, abre la aplicación de
  correo del visitante con el mensaje ya redactado hacia
  `michael@eliteguardsa.com`.
- **Con servicio configurado**: agregue el atributo `data-endpoint` al
  formulario en `contacto.html` y el envío se hará por `fetch` en segundo plano,
  sin salir de la página.

```html
<form id="formulario-contacto" data-endpoint="https://formspree.io/f/SU_CODIGO" ...>
```

Sirve cualquier servicio que reciba un `POST` con `FormData` (Formspree,
Formsubmit, Netlify Forms o una API propia).

## Pendientes por completar

Estos datos están con valores de ejemplo y deben reemplazarse:

- Teléfono: `+506 0000-0000` (en las tres páginas y en el pie)
- Dirección física en `contacto.html`
- Las cifras de la página de inicio (años de experiencia, agentes activos)
