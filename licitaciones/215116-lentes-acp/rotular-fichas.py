#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rotula las fichas técnicas del fabricante con el número de renglón (numeral 9.1.2 del
pliego) y resalta en la propia ficha cada característica que demuestra cumplimiento
(numeral 9.1.3), con una leyenda numerada al pie.

La página original se reduce y se libera una banda arriba: no se tapa nada del documento.
"""
import io, os, sys
import pymupdf
from reportlab.pdfgen import canvas
from reportlab.lib import colors

NARANJA = colors.HexColor("#EB5A2D")
NEGRO   = colors.HexColor("#1A1A1A")
BANDA   = 44
LEYENDA = 58          # banda inferior para la leyenda de resaltados
AMARILLO = (1, 0.92, 0.23)

RENGLONES = {
 1: ("PPE-EYE-00026", "Lente de seguridad, claro"),
 2: ("PPE-EYE-00027", "Lente de seguridad, oscuro"),
}

def capa(w, h, renglon, producto, marcas):
    """Banda superior con el renglón y banda inferior con la leyenda de resaltados."""
    cod, desc = RENGLONES[renglon]
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))

    y = h - BANDA
    c.setFillColor(NEGRO);   c.rect(0, y, w, BANDA, stroke=0, fill=1)
    c.setFillColor(NARANJA); c.rect(0, y - 3, w, 3, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 7.5)
    c.drawString(14, y + BANDA - 13, "LICITACIÓN ACP 215116  —  LENTES DE PROTECCIÓN PERSONAL")
    c.drawRightString(w - 14, y + BANDA - 13, "Ficha técnica del fabricante  —  %s" % producto)
    linea = "APLICA AL RENGLÓN %d   ·   CÓDIGO ACP %s   ·   %s" % (renglon, cod, desc)
    cuerpo = 12.0
    while c.stringWidth(linea, "Helvetica-Bold", cuerpo) > w - 28 and cuerpo > 7:
        cuerpo -= 0.25
    c.setFont("Helvetica-Bold", cuerpo)
    c.drawString(14, y + 10, linea)

    # leyenda de resaltados al pie
    c.setFillColor(colors.HexColor("#F2F2F2")); c.rect(0, 0, w, LEYENDA, stroke=0, fill=1)
    c.setFillColor(NARANJA); c.rect(0, LEYENDA - 2, w, 2, stroke=0, fill=1)
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(14, LEYENDA - 15, "REQUISITOS DEL RENGLÓN RESALTADOS EN ESTA FICHA (numeral 9.1.3)")
    c.setFont("Helvetica", 7)
    fila, col, ancho = 0, 0, (w - 28) / 2
    for n, (_, titulo) in enumerate(marcas, 1):
        px = 14 + col * ancho
        py = LEYENDA - 27 - fila * 9.5
        c.drawString(px, py, "[%d]  %s" % (n, titulo))
        fila += 1
        if fila == 3:
            fila, col = 0, col + 1
    c.save(); buf.seek(0)
    return buf.getvalue()

def rotular(origen, destino, renglon, producto, marcas, paginas=None):
    doc = pymupdf.open(origen)
    if paginas:                      # quedarse solo con las paginas del fabricante
        doc.select(list(range(paginas[0], paginas[1] + 1)))
    for pg in doc:
        # El resaltado va dibujado en el contenido de la pagina, no como anotacion:
        # show_pdf_page no arrastra anotaciones y se perderian al recomponer.
        for n, (frases, _) in enumerate(marcas, 1):
            puesto = False
            for frase in frases:
                for area in pg.search_for(frase):
                    caja = pymupdf.Rect(area.x0 - 1, area.y0 - 1, area.x1 + 1, area.y1 + 1)
                    # encima y translucido: algunas fichas traen un fondo opaco
                    # que taparia un resaltado dibujado por debajo.
                    pg.draw_rect(caja, color=None, fill=AMARILLO,
                                 fill_opacity=0.38, overlay=True)
                    if not puesto:
                        pg.insert_text((caja.x1 + 2, caja.y1 - 1), "[%d]" % n,
                                       fontsize=6.5, color=(0.92, 0.35, 0.18))
                        puesto = True
    doc.save(destino, garbage=3); doc.close()

    # reducir la página y pegar las bandas
    doc = pymupdf.open(destino)
    salida = pymupdf.open()
    for pg in doc:
        w, h = pg.rect.width, pg.rect.height
        nueva = salida.new_page(width=w, height=h)
        esc = (h - BANDA - LEYENDA - 8) / h
        destino_rect = pymupdf.Rect((w - w*esc)/2, BANDA + 4,
                                    (w - w*esc)/2 + w*esc, BANDA + 4 + h*esc)
        nueva.show_pdf_page(destino_rect, doc, pg.number)
        cap = pymupdf.open("pdf", capa(w, h, renglon, producto, marcas))
        nueva.show_pdf_page(nueva.rect, cap, 0, overlay=True)
    salida.save(destino + ".tmp"); salida.close(); doc.close()
    os.replace(destino + ".tmp", destino)
    return destino

# --- qué resaltar en cada ficha -------------------------------------------------
U = "/root/.claude/uploads/b972f6c3-b2d6-54d0-9bfc-fe7f33aae5b5/"

MARCAS_MP110AF = [
  (["Policarbonato", "policarbonato"],
   "Ocular y montura de policarbonato"),
  (["ANSI Z87+", "Estándares de Alto Impacto"],
   "ANSI Z87+ 1 2020 — alto impacto"),
  (["UV-AF", "Anti Empaño"],
   "Recubrimiento antiempañante UV-AF"),
  (["Resistencia a\nrayaduras", "Resistencia a"],
   "Resistencia a rayaduras"),
  (["Rayos Ultravioleta", "99%"],
   "Filtra el 99% de la radiación ultravioleta"),
  (["Envolvente", "lente única"],
   "Diseño envolvente de lente única: protección lateral integral"),
]

MARCAS_MP112PF = [
  (["MAX6", "Anti-Fog"],
   "Recubrimiento antiempañante MAX6"),
  (["Gray", "Memphis (MP1)"],
   "Ocular gris, serie Memphis MP1"),
  (["Polycarbonate", "Wrap Around Lens Design"],
   "Policarbonato, diseño envolvente de lente única"),
  (["Z87", "ANSI"],
   "Certificación ANSI Z87+"),
  (["13", "VLT"],
   "VLT 13%: ocular oscuro"),
]

TRABAJOS = [
 (U+"d49b56fc-ficha_MP110AF_merged_1.pdf", 1, "MCR Safety Memphis MP110AF", MARCAS_MP110AF, None,
  "fichas-rotuladas/ANEXO-A-R1-PPE-EYE-00026-MCR-MP110AF.pdf"),
 (U+"0aff1fa8-MP112PF_merged_1.pdf", 2, "MCR Safety Memphis MP112PF", MARCAS_MP112PF, None,
  "fichas-rotuladas/ANEXO-A-R2-PPE-EYE-00027-MCR-MP112PF.pdf"),
]

if __name__ == "__main__":
    os.makedirs("fichas-rotuladas", exist_ok=True)
    for origen, renglon, producto, marcas, paginas, salida in TRABAJOS:
        print(rotular(origen, salida, renglon, producto, marcas, paginas))
