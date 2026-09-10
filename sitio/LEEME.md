# Catálogo Elite Guard — sitio web

Catálogo estático: no necesita servidor, base de datos ni compilación.
Se publica subiendo esta carpeta tal cual.

## Qué hay aquí

| | |
|---|---|
| `index.html` | El catálogo. Estructura, estilos y código. |
| `datos.js` | Los 138 productos: textos, tallas, normas y rutas a las fotos. |
| `img/` | 126 fotos en WebP con fondo transparente. |
| `fichas/` | 17 fichas técnicas en PDF. |
| `netlify.toml` | Reglas de publicación y de caché. |

## Publicarlo en Netlify sin hacer público el repositorio

1. Entra a **netlify.com** y crea una cuenta (el plan gratuito basta).
2. **Add new site → Import an existing project → GitHub**.
3. Autoriza Netlify y elige el repositorio. Puede seguir siendo **privado**.
4. En la configuración de compilación:
   - **Base directory:** `sitio`
   - **Build command:** dejar vacío
   - **Publish directory:** `sitio`
5. **Deploy**. En un minuto queda en una dirección tipo
   `elite-guard.netlify.app`.

Cada vez que se suba un cambio al repositorio, Netlify vuelve a publicar solo.

## Dominio propio

En **Domain settings → Add a custom domain**, escribe por ejemplo
`catalogo.eliteguardsa.com`. Netlify indica qué registro CNAME agregar donde
tengas el dominio. El certificado HTTPS lo emite y lo renueva Netlify.

## Cómo agregar o cambiar un producto

Todo vive en `datos.js`, dentro de `products`. Cada producto es un bloque con
esta forma:

    {"id":0,"ref":"EG-178","name":"Camiseta reflectiva de poliéster",
     "brand":"eg","brandLabel":"Elite Guard",
     "cat":"A.1 Camisetas y polos reflectivos",
     "material":"...","tallas":"S a 5XL","colores":"Naranja, amarillo, azul marino",
     "normas":["..."],"lavado":"... · ...","img":"img/EG-178.webp",
     "imgs":[{"c":"Naranja","hex":"#f4641c","src":""}],
     "pdf":{"name":"...","url":"fichas/EG-178.pdf"}}

Reglas que hay que respetar:

- **`id` tiene que coincidir con la posición del producto en la lista.** El
  código los usa como índice. Si se inserta uno en medio, hay que renumerar y
  revisar la lista `featured`.
- **Una foto por color:** cada entrada de `imgs` necesita que su `c` coincida
  con un color escrito en `colores`; así la muestra cambia la imagen al tocarla.
- **`src` vacío** en una entrada de `imgs` significa "usa la foto principal".
  Evita guardar la misma imagen dos veces.
- **Las fotos** van en WebP con fondo transparente, cuadradas, 620 u 820 px.
- **Las fichas** son enlaces (`url`), no archivos incrustados.

## Verificar antes de publicar

    cd sitio && python3 -m http.server 8899

y abrir `http://127.0.0.1:8899`.
