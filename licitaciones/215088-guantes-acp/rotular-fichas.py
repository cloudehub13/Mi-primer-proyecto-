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
 2: ("PPE-GLO-00012", "Guante químico industrial, talla 9"),
 3: ("PPE-GLO-00020", "Guante punteado de Kevlar, talla 10"),
 4: ("PPE-GLO-00022", "Guante de examen de nitrilo, mediano"),
 5: ("PPE-GLO-00031", "Guante anticorte, talla 9"),
 6: ("PPE-GLO-00033", "Guante tejido con palma de PU, talla 11"),
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
    c.drawString(14, y + BANDA - 13, "LICITACIÓN ACP 215088  —  GUANTES")
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

MARCAS_J710 = [
  (["EN ISO 374-1", "Type A", "AGJKLPT"],
   "Protección química: EN ISO 374-1 Tipo A, código AGJKLPT"),
  (["CE-CAT III", "Certificada CE", "0493"],
   "Categoría CE CAT III, organismo notificado 0493"),
  (["EN388", "4102X"],
   "Resistencia mecánica EN 388 — 4102X"),
  (["Superficie texturada", "Flocado interior", "Resistente a productos químicos"],
   "Construcción de uso industrial: texturado y flocado"),
  (["industrias químicas, petrolíferas y alimentarias", "CE apto para alimentos"],
   "Apto para uso industrial químico, petrolero y alimentario"),
  (["ISO 18889"],
   "Prestación adicional: ISO 18889 G2 (plaguicidas)"),
]

MARCAS_9366 = [
  (["Kevlar® Aramid Shell", "7-Gauge Kevlar"],
   "Concha de aramida Kevlar® de DuPont™, calibre 7"),
  (["PVC Dots on 2 Sides", "PVC"],
   "Puntos de PVC en ambas caras (guante reversible)"),
  (["Cut Resistant Work Gloves"],
   "Guante resistente al corte (ANSI A3 mínimo exigido)"),
  (["Regular Weight"],
   "Tejido de peso regular"),
  (["9366XL", "X - Large"],
   "Talla 10 (X-Large), la exigida por el renglón"),
  (["Polybag 12"],
   "Presentación: bolsa de 12 pares"),
]

MARCAS_6008 = [
  (["EN455", "ASTM D6319"],
   "Grado examen: EN 455 partes 1, 2 y 3 y ASTM D6319"),
  (["Nitrilo", "nitrilo"],
   "Material: nitrilo"),
  (["8 mil"],
   "Espesor 8 mil, longitud 9,5 pulgadas"),
  (["Paquete interior: 50 por dispensador", "50 por dispensador"],
   "Presentación: caja de 50 unidades (el renglón exige 50 a 100)"),
  (["6008M", "Mediano"],
   "Talla mediana, la exigida por el renglón"),
  (["EN374-1", "EN 374-1:2016", "EN374-5"],
   "Prestación adicional: barrera química y biológica"),
]

MARCAS_92754BP = [
  (["HyperMax® HPPE Shell", "Fibra HyperMax"],
   "Concha tejida de HPPE HyperMax®, resistente a corte y desgarro"),
  (["Bi-Polymer Coated Palm and Fingertips", "bipolímero"],
   "Palma y yemas recubiertas: abrasión y punción"),
  (["13-Gauge", "13 Galgas"],
   "Calibre 13"),
  (["92754BPL", "L (9)"],
   "Talla 9 (Large), la exigida por el renglón"),
  (["Reinforced thumb crotch", "entrepierna reforzada"],
   "Prestación adicional: refuerzo entre pulgar e índice"),
]

MARCAS_92852PU = [
  (["Puntuación de corte (ANSI):", "A4"],
   "Resistencia al corte ANSI A4"),
  (["EN 388: Puntuación CE - Abrasión:", "EN 388: Puntuación CE - Corte TDM100:"],
   "EN 388:2016 — abrasión 4, corte 5, desgarro 4, punción 2, corte TDM D"),
  (["poliuretano (PU) en la palma", "Poliuretano (PU)"],
   "Recubrimiento de poliuretano en palma y dedos"),
  (["HPPE gris sintético", "calibre 13"],
   "Carcasa sin costuras de HPPE sintético, calibre 13"),
  (["Puntuación de abrasión (ANSI):", "Puntuación de pinchazo (ANSI):"],
   "Abrasión ANSI 5 y punción ANSI 3"),
]

TRABAJOS = [
 (U+"17a7281f-J710.pdf", 2, "Elite Guard J710", MARCAS_J710, None,
  "fichas-rotuladas/ANEXO-A-R2-PPE-GLO-00012-ELITE-GUARD-J710.pdf"),
 (U+"1f65657d-9366.pdf", 3, "MCR Safety CutPro 9366", MARCAS_9366, (2, 3),
  "fichas-rotuladas/ANEXO-A-R3-PPE-GLO-00020-MCR-9366.pdf"),
 (U+"f3432d3c-6008_Nitrishield.pdf", 4, "MCR Safety NitriShield 6008", MARCAS_6008, None,
  "fichas-rotuladas/ANEXO-A-R4-PPE-GLO-00022-MCR-6008.pdf"),
 (U+"1871ffb4-ficha_92754BP.pdf", 5, "MCR Safety CutPro 92754BP", MARCAS_92754BP, None,
  "fichas-rotuladas/ANEXO-A-R5-PPE-GLO-00031-MCR-92754BP.pdf"),
 (U+"a83cfb49-92852PU.pdf", 6, "MCR Safety CutPro 92852PU", MARCAS_92852PU, None,
  "fichas-rotuladas/ANEXO-A-R6-PPE-GLO-00033-MCR-92852PU.pdf"),
]

if __name__ == "__main__":
    os.makedirs("fichas-rotuladas", exist_ok=True)
    for origen, renglon, producto, marcas, paginas, salida in TRABAJOS:
        print(rotular(origen, salida, renglon, producto, marcas, paginas))
