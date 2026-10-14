# Auditoría previa a la carga en el SLI — Licitación ACP 215088

Revisión del **8-oct-2026**. Cierre: **viernes 9-oct-2026, 11:00 a.m.**

## Veredicto

**Todavía no se puede subir.** Los documentos están escritos y correctos en su redacción,
pero hay **4 datos sin llenar** y **4 anexos que no existen**. Subir así es rechazo seguro,
porque el numeral 9.1 exige cumplimiento al 100% y el 9.1 pide evidencia documental.

---

## 1. Lo que exige el pliego, requisito por requisito

| Numeral | Qué exige | Estado |
|---|---|---|
| **1.3** | Validez de la propuesta: **60 días** calendario desde el acto | ✅ declarado en carta y en económica |
| **1.5** | Adjudicación por **precio más bajo por renglón** | ✅ la económica cotiza renglón por renglón |
| **1.6** | Propuesta técnica obligatoria, **solo .PDF**, por SLI | ✅ cinco PDF, uno por renglón |
| **2.2** | Enviar propuesta técnica, **certificaciones** y económica por el SLI | ⚠️ faltan las certificaciones |
| **2.3** | Bienes nuevos | ✅ declarado |
| **3.1** | Entrega **120 días** calendario | ✅ declarado en ambas propuestas |
| **3.2** | **DAP Panamá** con aduana, descarga y colocación en sitio | ✅ declarado |
| **5** | Garantía **1 año** desde la recepción | ✅ declarado |
| **9.1** | Cumplimiento 100% + evidencia de certificaciones + literatura + **imagen** + **marcación** + presentación de empaque | ⚠️ falta imagen, marcación y certificaciones |
| **9.1.1** | Declarar si se oferta el producto de referencia | ✅ marcado: SÍ el renglón 3, NO los renglones 2, 4, 5 y 6 |
| **9.1.2** | Cada documento dice a qué renglón aplica · **sin copy-paste** | ✅ los cinco PDF lo dicen en el encabezado; la redacción es propia |
| **9.1.3** | **Resaltar** cada característica que demuestra cumplimiento | ⚠️ hecho solo en la ficha del J710 |
| **9.1.4** | Pr y Each significan par | ✅ respetado; el renglón 4 va por caja |
| **9.1.5** | Si el fabricante reemplazó el P/N de referencia, declararlo | ✅ no aplica: el 9366 sigue vigente |
| **9.2** | **Muestra** de cada artículo, rotulada, en Balboa antes del cierre | ❌ pendiente, es física |
| **9.6** | Entregas parciales por renglón completo | ✅ declarado en la económica |
| **9.7** | Trazabilidad hasta el fabricante | ⚠️ falta la carta de distribuidor autorizado |
| **9.8** | Empaque y estiba ASTM D5728 | ✅ declarado |
| — | Nombre legal del RUC, idéntico en precio y técnica | ❌ sin llenar |

---

## 2. Datos que faltan (sin esto no se sube)

| # | Dato | Dónde se usa |
|---|---|---|
| 1 | **Los 8 datos legales del proponente** — razón social del RUC, RUC+DV, aviso de operación, patronal CSS, dirección, representante y cargo, teléfono, correo | Carta, los cinco PDF de renglón y la económica |
| 2 | **Conteo exacto de la caja del 6008** talla mediana | Renglón 4 — el renglón exige caja de 50 a 100 |
| 3 | **Código EN 388:2016 completo del 92754BP** | Renglón 5 — el renglón cita primero el código europeo |
| 4 | **Cantidad del renglón 6** | Renglón 6 y la económica |

Más, para la económica: **país de origen** de cada producto y los **precios**.

## 3. Anexos que no existen todavía

| Anexo | Qué es | Estado |
|---|---|---|
| **A** | Ficha del fabricante por renglón, **resaltada** | solo está la del **J710** (renglón 2). Faltan 9366, 6008, 92754BP y 92852PU |
| **A bis** | **Imagen** del producto ofertado | faltan las cinco |
| **B** | **Marcación** del producto o de la certificación. En el renglón 3, la etiqueta DuPont™ Kevlar® | faltan las cinco |
| **C** | **Evidencia documental vigente** de certificaciones y normas (EN 455, ASTM D6319, ANSI/ISEA 105, EN ISO 374, EN 388, ISO 21420) | faltan |
| **D** | Carta de **distribuidor autorizado** de MCR Safety | falta |

El numeral 9.1 nombra la imagen y la marcación de forma expresa, y el renglón 3 repite que la
literatura y la imagen son requeridas con la propuesta. No son opcionales.

## 4. Correcciones aplicadas en esta revisión

1. **Se eliminó el PDF de la carta de presentación.** Tenía texto interno que no debe ver la
   ACP («ELIMINAR DE ESTA TABLA CUALQUIER RENGLÓN QUE NO SE VAYA A OFERTAR», «MARCAR LA OPCIÓN
   QUE CORRESPONDA») y además seguía listando el renglón 1, que ya no se oferta. La carta queda
   **solo en Word**, que es la versión al día, para que no circulen dos versiones distintas.
2. **`generar-pdfs.py` ahora revisa su propia salida** y avisa en pantalla de cada campo que
   quede entre « ». Mientras imprima "NO SUBIR AL SLI TODAVÍA", los PDF no están listos.

## 5. Orden para cerrar

1. Llenar los 8 datos legales en `generar-pdfs.py` y en la carta y la económica de Word.
2. Pedir a MCR los 3 datos técnicos y los anexos A, A bis, B, C y D.
3. Volver a correr `python3 generar-pdfs.py` hasta que imprima **"OK: ningún campo pendiente"**.
4. Rotular y resaltar las cuatro fichas que faltan con `rotular-fichas.py`.
5. Poner precios y país de origen en la económica; exportarla a PDF.
6. Exportar la carta de Word a PDF y firmarla.
7. Entregar las muestras rotuladas en Balboa.
8. Cargar en el SLI con el nombre legal del RUC.
