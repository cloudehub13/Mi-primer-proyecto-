# Checklist para ingresar la propuesta al SLI — Licitación ACP 215116

**Cierre: 25-sep-2026, 11:00 a.m.** · Todo lo que no esté cargado antes de esa hora, no existe.

---

## A. Antes de poner un precio (arrancar hoy)

- [ ] **MCR — confirmación escrita de lateral NO VENTILADA** en `OG110AF` y `OG112AF`.
      Sin esto no se ofertan los renglones 3 y 4 con MCR. Pedir que venga en la ficha técnica
      o en carta del fabricante, porque hay que adjuntarla como Anexo B.
- [ ] **MCR — precio en firme y lead time** para: 15,840 `BK110AF` + 10,800 `BK112AF` +
      5,200 `OG110AF` + 7,200 `OG112AF` + 60 `28550`.
      Exigir: **precio válido 60 días** y **entrega puesta en Panamá dentro de 90 días calendario**.
- [ ] **MCR — carta de distribuidor autorizado** a nombre de la razón social que va a facturar
      (Anexo C, numeral 9.7 de trazabilidad).
- [ ] **MCR — declaración de conformidad ANSI/ISEA Z87.1** de cada P/N (Anexo B).
- [ ] **Fichas técnicas oficiales del fabricante** de cada P/N, en PDF (Anexo A).
      Las fichas del catálogo Elite Guard **no sirven** para esto: la ACP pide literatura
      **del fabricante**.
- [ ] **Muestras físicas en Panamá** de los 4 modelos MCR. Si no hay muestra de un modelo,
      **ese renglón no se oferta**.
- [ ] Cotizar flete + seguro + **declaración simplificada de aduanas** + descarga y colocación
      en sitio en Corozal. Todo eso va dentro del precio unitario (DAP).
- [ ] **No cargar ITBMS** al precio (cláusula 4.28.6).
- [ ] Costo financiero: pago **neto 30 días** contra entrega. Meterlo en el margen.

## B. Consultas y protestas (vencen antes del cierre)

- [ ] **Enviar la consulta escrita** a JHernandez@pancanal.com — plantilla lista en
      `CONSULTA-ACP.md`. Mandarla cuanto antes: la ACP tiene que poder distribuir la
      respuesta a todos los interesados.
- [ ] Fecha límite para **protestar contra el pliego**: **23-sep-2026** (2 días hábiles antes
      del cierre). Solo si hay un requisito que amarre la licitación a una sola marca.

## C. Muestras — el paso que no se arregla a última hora

- [ ] Una muestra por cada renglón ofertado que no sea producto de referencia ACP.
- [ ] Rotular cada muestra con:
      **(1)** nombre del proponente · **(2)** número de pliego **215116** · **(3)** número de
      propuesta. **Sin este rótulo la propuesta no se considera.**
- [ ] Entregar en: **Balboa, Ancón, Edificio 710, planta baja, recepción.**
- [ ] Horario: **7:15–11:00 a.m.** y **12:15–3:15 p.m.**, antes de la fecha y hora de cierre.
- [ ] Guardar constancia de la entrega (nombre de quien recibe, fecha y hora).
- [ ] Recordatorio: las muestras se retiran dentro de **10 días hábiles** después de la
      adjudicación, o la ACP dispone de ellas.

## D. Armar los PDF de la propuesta técnica

- [ ] Abrir `generar-pdfs.py`, llenar el bloque `PROPONENTE` (razón social del RUC, RUC+DV,
      aviso de operación, CSS, representante, teléfono, correo).
- [ ] Borrar de la lista `RENGLONES` los renglones que **no** se vayan a ofertar.
- [ ] Si cambia el modelo ofertado, ajustar `marca`, `modelo`, `pn` y la matriz de ese renglón.
- [ ] Correr `python3 generar-pdfs.py`. Salen los PDF en `pdf/`.
- [ ] Revisar que **no quede ningún texto entre « »** en los PDF finales. Cada « » es un dato
      sin llenar.
- [ ] En la carta de presentación, **marcar la casilla** del numeral 9.1.1 (si se oferta o no
      el producto de referencia ACP, y en qué renglones).
- [ ] **Firmar** cada PDF (firma y nombre del proponente + fecha) antes de subirlo.

## E. Anexos del fabricante

- [ ] **Anexo A** — ficha técnica del fabricante por cada P/N ofertado,
      **con las características de cumplimiento resaltadas en amarillo** (numeral 9.1.3).
      Resaltar específicamente: policarbonato · Z87+ · antirrayado · antiempañante · 99% UV ·
      protección lateral (y **no ventilada** en los renglones 3 y 4).
- [ ] **Anexo B** — declaración de conformidad / certificado ANSI/ISEA Z87.1 del fabricante.
- [ ] **Anexo C** — carta de distribuidor autorizado (trazabilidad).
- [ ] Cada anexo debe **decir a qué renglón aplica** (numeral 9.1.2). Ponerlo en la portada o
      en el nombre del archivo.

## F. Carga en el SLI

- [ ] Ingresar con el **NOMBRE LEGAL del RUC**. No usar el nombre comercial del Aviso de
      Operación.
- [ ] Cargar el **precio unitario por renglón**. La adjudicación es por renglón: se puede
      ofertar solo en los renglones donde se es competitivo.
- [ ] Adjuntar la propuesta técnica **solo en formato .PDF**.
      Límite: **15 adjuntos de 15 MB cada uno**.
- [ ] Orden de carga sugerido:

      00-CARTA-DE-PRESENTACION.pdf
      01-RENGLON-1-PPE-EYE-00026.pdf
      02-RENGLON-2-PPE-EYE-00027.pdf
      03-RENGLON-3-PPE-EYE-00028.pdf
      04-RENGLON-4-PPE-EYE-00029.pdf
      05-RENGLON-5-PPE-EYE-00015.pdf
      ANEXO-A-R1-ficha-MCR-BK110AF.pdf
      ANEXO-A-R2-ficha-MCR-BK112AF.pdf
      ANEXO-A-R3-ficha-MCR-OG110AF.pdf
      ANEXO-A-R4-ficha-MCR-OG112AF.pdf
      ANEXO-A-R5-ficha-MCR-28550.pdf
      ANEXO-B-declaracion-conformidad-ANSI-Z87-MCR.pdf
      ANEXO-C-carta-distribuidor-autorizado-MCR.pdf

      (13 adjuntos — cabe dentro del límite de 15.)

- [ ] **Verificar que el nombre legal de la propuesta técnica sea idéntico al de la propuesta
      de precio.** Si no coinciden, se rechaza.
- [ ] Descargar el **acuse del SLI** y guardarlo.
- [ ] Cargar con **margen de horas**, no de minutos. La ACP no responde por fallas de
      transmisión del proponente.

## G. Si se gana

- [ ] Entrega: **90 días calendario** desde la orden de compra.
- [ ] Lugar: ACP, Sección de Almacenes, **Corozal Oeste, Edificio 652, área de recibo**.
- [ ] Entregas parciales permitidas **por renglón completo**, nunca fracciones de un renglón.
      La factura va igual: por renglón completo.
- [ ] Empaque y estiba que permitan la descarga (ASTM D5728); el transporte debe tener
      capacidad y accesibilidad para descargar.
- [ ] Incluir el **instructivo de uso del fabricante** con el producto.
- [ ] Garantía **mínima de 1 año** desde la recepción.
- [ ] Ojo con la multa: hasta **10% del valor no entregado por cada prórroga**.
- [ ] Retirar las muestras dentro de **10 días hábiles** desde la adjudicación.
