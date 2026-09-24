# Estado del catálogo Elite Guard

> Punto de guardado. Este archivo dice dónde quedó el trabajo, qué falta y qué
> decisiones están abiertas, para poder retomar sin volver a reconstruir el contexto.

## El catálogo está publicado

```
https://cloudehub13.github.io/Mi-primer-proyecto-/
```

Ese es el enlace que se le manda al cliente. Se actualiza con `./publicar.sh`.

## Cómo está montado

- `docs/` **es** el sitio. `index.html` + `datos.js` + `img/` + `fichas/`.
- GitHub Pages sirve la rama **`gh-pages`**, que es una copia de `docs/` en la raíz.
  La genera `./publicar.sh`; no se edita a mano.
- `catalogo-elite-guard.html` es el **artifact viejo**. Está en su tope de 16 MB
  y ya no admite productos nuevos: le faltan H440, H444 y la foto del MCR 2003,
  y conserva datos que ya se corrigieron. **El bueno es el sitio.**
- Detalle de operación y reglas de edición: `docs/LEEME.md`.

## Avance

**184 productos · 79 completos** (referencia, foto, ficha y sector)

El desglose por rubro y el listado de lo que falta están en **`REPORTE.md`**,
que se regenera solo a partir de `docs/datos.js`. No copiar cifras a mano aquí:
se desactualizan a la primera tanda de productos nuevos.

Pendiente grueso, en orden de impacto:

1. **104 sin ficha técnica descargable** — es la brecha más grande.
2. **60 con varios colores y una sola foto** — falta la foto por color.
3. **20 sin fotografía.**
4. **18 con referencia mala** (quedó texto de extracción en vez de la referencia real).
5. **14 sin sector asignado.**

## Referencias que hoy salen mal al cliente

- `(vacía)` — Guante químico de inmersión · Protección para las manos
- `MCR` — Guante tejido calibre 7 · Protección para las manos
- `por` — Manga anticorte HPPE / Kevlar® · Protección para las manos
- `(vacía)` — Manga anticorte HPPE · Protección para las manos
- `Overol` — Peto y chaqueta química reutilizable · Ropa de protección química y desechable
- `por` — Traje de respuesta a materiales peligrosos · Ropa de protección química y desechable
- `por` — Mandil, polainas y accesorios de cuero para soldadura · Ignífugos y arco eléctrico
- `por` — Eslinga de posicionamiento regulable · Protección anticaídas (trabajo en altura)
- `cinta` — Cinta de anclaje + mosquetón · Protección anticaídas (trabajo en altura)
- `Kondor` — Bota de seguridad de cuero · Protección para los pies
- `Kondor` — Bota de seguridad premium · Protección para los pies
- `por` — Bota dieléctrica · Protección para los pies
- `Kondor` — Bota Jumbo Seguridad Tridensidad Blindada · Protección para los pies
- `por` — Bota muslera (hip boot) de PVC · Protección para los pies
- `por` — Sobrecalzado impermeable · Protección para los pies
- `por` — Paleta y banderola de señalero hi-vis · Señalización y seguridad vial
- `por` — Kit de quemaduras · Primeros auxilios y control de derrames
- `ALTA` — Rodillera profesional con cap de goma · Ergonomía: rodilleras y coderas
- `ALTA` — Rodillera de alto impacto con D3O® · Ergonomía: rodilleras y coderas
- `ALTA` — Codera de protección · Ergonomía: rodilleras y coderas
- `por` — Chaleco refrescante evaporativo · Confort térmico y estrés por calor
- `por` — Banda antisudor / refrescante para casco · Confort térmico y estrés por calor

## Notas internas visibles al cliente

- **PS54** (Protección para la cabeza): Barboquejo incluido de fábrica.
- **PW52** (Protección para la cabeza): Vida útil hasta 7 años desde fabricación si no sufre daño. ⚠️ Clase C, no eléctrico.
- **EP10** (Protección auditiva): Confirmar SNR exacto de cada modelo. Cordova también maneja orejeras. Higiene: kit de recambio de almohadillas cada 6 meses.
- **MCR** (Protección para las manos): Muy alta rotación por precio. Confirmar SKU exacto y presentación de bulto.
- **por** (Protección para las manos): Confirmar 2 modelos: uno Kevlar (calor + corte) y uno HPPE (corte + costo).
- **UC491** (Chalecos de alta visibilidad): Versión aún más económica sin certificación: MCR **HS200V** (≈ US$6). Marca propia Elite Guard: definir chaleco básico.
- **ST40** (Ropa de protección química y desechable): Antiestático obligatorio en refinería / zona ATEX → confirmar que el lote lleva EN 1149-5.
- **5012** (Ignífugos y arco eléctrico): Producto de nicho, alto valor. Confirmar talla y tipo de puño con el cliente.
- **FP40** (Protección anticaídas (trabajo en altura)): SRL corto de 2 colas para andamio (100% tie-off con frenado corto): confirmar disponibilidad Portwest.
- **cinta** (Protección anticaídas (trabajo en altura)): Confirmar con Portwest: anclaje para concreto (perno + argolla), anclaje para puerta/vano y trípode para espacio confinado.
- **Kondor** (Protección para los pies): Gama Kondor de cuero: **Dakar** (premium, puntera de nanocarbono), **Mundial**, **Master**, **Sport**, **Urban**. Confirmar cuáles se importan.
- **por** (Protección para los pies): Confirmar con Kondor / catálogo Portwest **Compositelite** (FC-series) como alternativa.
- **31261** (Protección para los pies): Económica: **Pulsar** (≈ US$23–25). Para frío/flexibilidad: **Profile** (aditivo Frigiflex®).
- **CINTA-PELIGRO** (Señalización y seguridad vial): Alta rotación y bajo costo — buen producto de "carrito". Postes separadores con cinta retráctil (tipo banco) para oficinas/recepción: evaluar si se agregan. _(Imagen de referencia.)_
- **FA21** (Primeros auxilios y control de derrames): Bolso/pouch de primeros auxilios para llevar al cinturón (primer respondiente) — confirmar código Portwest.
- **KP30** (Ergonomía: rodilleras y coderas): Gama de mejor margen. Producto "de recompra" (el gel dura más pero la concha se raya).
- **por** (Confort térmico y estrés por calor): Confirmar referencia y modalidad (evaporativo vs. packs de gel).

## Rubros cerrados en esta ronda

**Impermeables (capotes)** — CERRADO: 6 de 6 completos. Se sacaron los dos de MCR y los dos de Tingley; entraron S440 y S441 de Portwest.

| REF | Producto | Marca | Tallas | Colores |
|---|---|---|---|---|
| RCOAT-27 | Capote impermeable de 1 pieza con capucha | Elite Guard | S a 3XL | Amarillo lima fluorescente |
| RCOAT-26 | Conjunto impermeable de 2 piezas | Elite Guard | S a 3XL | Amarillo lima fluorescente |
| H440 | Chubasquero hi-vis Clase 3 Essentials 190T | Portwest | XS a 6XL | Naranja, amarillo |
| H444 | Pantalón hi-vis para lluvia Classic Contrast | Portwest | XS a 3XL | Naranja, amarillo |
| S440 | Chubasquero impermeable Classic | Portwest | S a 6XL | Amarillo |
| S441 | Pantalón impermeable Classic | Portwest | S a 6XL | Amarillo |
Pendiente: confirmar si el S440/S441 llega a 7XL (la ficha de Portwest dice 6XL) y qué colores se traen además del amarillo.

## Decisiones abiertas

1. **Qué se hace con el artifact.** Sigue circulando con datos equivocados.
   Propuesta: convertirlo en una página que redirija al sitio, para que quien
   tenga el enlace viejo llegue al catálogo correcto.
2. **Sacar las notas internas** del catálogo a un archivo aparte.
3. **Renombrar el repositorio** a `catalogo-elite-guard`
   (Settings → General → Repository name). Hoy el enlace dice
   "Mi-primer-proyecto-", que no sirve para mandarle a un cliente.
4. **Dominio propio** `catalogo.eliteguardsa.com`: hace falta un registro DNS
   CNAME `catalogo` → `cloudehub13.github.io.` Cuando esté puesto, se agrega un
   archivo `CNAME` dentro de `docs/`. **No agregarlo antes**, porque tumba el
   enlace actual.

## Cómo se agrega información

Portwest, MCR, Tingley y las tiendas de EPP están bloqueadas desde el entorno de
trabajo por política de red: no se pueden consultar. La vía que sí funciona es
**adjuntar el PDF de la ficha**. De ahí salen texto, normas, tallas, colores y la
fotografía del producto.

Regla que no se puede romper: el `id` de cada producto es su posición en la lista
y `featured` guarda esas mismas posiciones. Al insertar, borrar o reordenar hay que
renumerar todos los `id` y remapear `featured`.
