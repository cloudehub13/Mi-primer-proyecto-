# Catálogo Elite Guard — sitio web

Esta carpeta **es** el sitio. No hay nada que compilar: son archivos estáticos.

```
docs/
  index.html      la página del catálogo
  datos.js        los productos (el archivo que se edita para agregar cosas)
  img/            fotos de producto (.webp)
  fichas/         fichas técnicas (.pdf)
  netlify.toml    reglas de caché (solo si se publica en Netlify)
  .nojekyll       necesario para GitHub Pages
```

## Por qué el sitio y no el artifact

El artifact lleva todas las fotos y todos los PDF metidos dentro del mismo
archivo HTML, y ese archivo **no puede pasar de 16 MB**. Ya está en el tope.
Aquí las fotos y las fichas son archivos aparte: no hay tope, y el cliente solo
descarga la foto que mira, no las 140. La primera visita pesa ~0,3 MB en vez
de 15,5 MB.

## Publicarlo (una sola vez)

### Opción A — GitHub Pages (recomendada, gratis, sin cuenta nueva)

1. Que esta rama se fusione a `main`.
2. En GitHub: **Settings → Pages**.
3. En *Source* elegir **Deploy from a branch**, rama **main**, carpeta **/docs**.
4. **Save**.

A los 1–2 minutos el catálogo queda en:

```
https://cloudehub13.github.io/Mi-primer-proyecto-/
```

Ese es el enlace que se le manda al cliente. Cada vez que se haga push a `main`
el sitio se actualiza solo.

### Opción B — Netlify (si después se quiere dominio propio)

Conectar el repositorio en Netlify con:

- Base directory: `docs`
- Build command: *(vacío)*
- Publish directory: `docs`

`netlify.toml` ya trae las reglas de caché.

### Dominio propio

Con cualquiera de las dos opciones se le puede poner
`catalogo.eliteguardsa.com` apuntando un CNAME desde el proveedor del dominio.

## Cómo se agrega un producto

1. La foto va en `img/` como `.webp`, cuadrada, 820×820, fondo transparente.
2. La ficha va en `fichas/` como `.pdf`.
3. En `datos.js` se agrega el objeto del producto.

**Regla que no se puede romper:** cada producto tiene un `id` que es su posición
en la lista, empezando en 0. La lista `featured` guarda esos mismos números.
Si se inserta, se borra o se reordena un producto hay que **renumerar todos los
`id` y corregir `featured`**, o el catálogo abre el producto equivocado al
hacer clic.

Campos de un producto:

| campo | para qué sirve |
|---|---|
| `id` | posición en la lista (0, 1, 2, …) |
| `name`, `ref`, `brand`, `brandLabel` | identificación |
| `cat`, `catShort`, `sub` | dónde aparece en el menú |
| `desc`, `material`, `tallas`, `colores`, `pres` | ficha visible |
| `usos`, `sectors`, `normas`, `notas`, `lavado` | detalles |
| `img` | ruta a la foto, p. ej. `img/EG-178.webp` |
| `imgs` | galería por color: `[{"c":"negro","src":"img/EG-178-negro.webp"}]` |
| `pdf` | `{"name":"…pdf","url":"fichas/….pdf"}` |

En `imgs`, si el primer color usa la misma foto que `img`, se deja `"src":""`
y el catálogo reutiliza la principal sin duplicar el archivo.
