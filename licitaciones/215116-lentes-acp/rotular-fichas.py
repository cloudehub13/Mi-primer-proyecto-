#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estampa el número de renglón en las fichas técnicas del fabricante,
como exige el numeral 9.1.2 del pliego de la licitación ACP 215116:
"Cada documento de la propuesta técnica presentado debe definir a qué renglón aplica."

No tapa nada del original: reduce cada página y libera una banda arriba.
Uso: python3 rotular-fichas.py
"""
import io, os
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib import colors

NARANJA = colors.HexColor("#EB5A2D")
NEGRO   = colors.HexColor("#1A1A1A")
BANDA   = 42          # alto de la banda en puntos
SALIDA  = "fichas-rotuladas"

RENGLONES = {
 1: ("PPE-EYE-00026", "Lente de seguridad, claro"),
 2: ("PPE-EYE-00027", "Lente de seguridad, oscuro"),
 3: ("PPE-EYE-00028", "Sobrelente OTG, claro"),
 4: ("PPE-EYE-00029", "Sobrelente OTG, gris / humo"),
 5: ("PPE-EYE-00015", "Goggle de soldadura 50 mm, tono 5"),
}

def banda(w, h, renglon, producto):
    cod, desc = RENGLONES[renglon]
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    y = h - BANDA
    c.setFillColor(NEGRO);   c.rect(0, y, w, BANDA, stroke=0, fill=1)
    c.setFillColor(NARANJA); c.rect(0, y - 3, w, 3, stroke=0, fill=1)

    c.setFillColor(colors.white)
    # linea superior pequena: licitacion (izq) y ficha (der)
    c.setFont("Helvetica", 7.5)
    c.drawString(14, y + BANDA - 13,
                 "LICITACIÓN ACP 215116  —  LENTES DE PROTECCIÓN PERSONAL")
    c.drawRightString(w - 14, y + BANDA - 13,
                      "Ficha técnica del fabricante  —  %s" % producto)
    # linea principal: el renglon
    linea = "APLICA AL RENGLÓN %d   ·   CÓDIGO ACP %s   ·   %s" % (renglon, cod, desc)
    cuerpo = 12.0
    while c.stringWidth(linea, "Helvetica-Bold", cuerpo) > w - 28 and cuerpo > 7:
        cuerpo -= 0.25
    c.setFont("Helvetica-Bold", cuerpo)
    c.drawString(14, y + 9, linea)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]

def rotular(origen, destino, renglon, producto):
    r = PdfReader(origen)
    w_out = PdfWriter()
    for pg in r.pages:
        w = float(pg.mediabox.width); h = float(pg.mediabox.height)
        s = (h - BANDA - 6) / h                       # deja libre la banda superior
        nueva = PageObject.create_blank_page(width=w, height=h)
        nueva.merge_transformed_page(
            pg, Transformation().scale(s).translate((w - w * s) / 2, 0))
        nueva.merge_page(banda(w, h, renglon, producto))
        w_out.add_page(nueva)
    with open(destino, "wb") as f:
        w_out.write(f)
    return destino

U = "/root/.claude/uploads/b972f6c3-b2d6-54d0-9bfc-fe7f33aae5b5/"
TRABAJOS = [
 (U+"d49b56fc-ficha_MP110AF_merged_1.pdf", 1, "MCR Safety Memphis MP1 — MP110AF",
  "ANEXO-A-R1-PPE-EYE-00026-MCR-MP110AF.pdf"),
 (U+"0aff1fa8-MP112PF_merged_1.pdf",       2, "MCR Safety Memphis MP1 — MP112PF",
  "ANEXO-A-R2-PPE-EYE-00027-MCR-MP112PF.pdf"),
 (U+"30cb1272-OG210PF_-_Specsheet.pdf",    3, "MCR Safety Klondike OTG — OG210PF",
  "ANEXO-A-R3-PPE-EYE-00028-MCR-OG210PF.pdf"),
 (U+"fb07ddff-OG212PF_-_Specsheet.pdf",    4, "MCR Safety Klondike OTG — OG212PF",
  "ANEXO-A-R4-PPE-EYE-00029-MCR-OG212PF.pdf"),
 (U+"3d07cec0-PS24.pdf",                   3, "Portwest Peak OTG — PS24",
  "ANEXO-A-R3-PPE-EYE-00028-PORTWEST-PS24.pdf"),
 (U+"4e446dc0-PS20.pdf",                   1, "Portwest Dynamic Plus KN — PS20",
  "ANEXO-A-R1-PPE-EYE-00026-PORTWEST-PS20.pdf"),
 (U+"4e446dc0-PS20.pdf",                   2, "Portwest Dynamic Plus KN — PS20",
  "ANEXO-A-R2-PPE-EYE-00027-PORTWEST-PS20.pdf"),
 (U+"0ed74f52-PS27.pdf",                   1, "Portwest Tech Look Lite KN — PS27",
  "ANEXO-A-R1-PPE-EYE-00026-PORTWEST-PS27.pdf"),
 (U+"0ed74f52-PS27.pdf",                   2, "Portwest Tech Look Lite KN — PS27",
  "ANEXO-A-R2-PPE-EYE-00027-PORTWEST-PS27.pdf"),
]

if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    for origen, renglon, producto, nombre in TRABAJOS:
        print(rotular(origen, os.path.join(SALIDA, nombre), renglon, producto))
