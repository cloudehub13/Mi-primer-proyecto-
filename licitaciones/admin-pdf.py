#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arma, por licitacion, UN solo PDF con:
   carta de presentacion + propuesta economica + Aviso de Operacion.
   Uso: python3 admin.py
"""
import os, pymupdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether)

RAIZ  = "/home/user/Mi-primer-proyecto-/licitaciones"
LOGO  = RAIZ + "/215088-guantes-acp/word/logo-elite-guard.png"
AVISO = "/root/.claude/uploads/b972f6c3-b2d6-54d0-9bfc-fe7f33aae5b5/a72ccaf6-AVISO_DE_OPERACION_EG_2026.pdf"

PROP = {
    "razon":  "ELITE GUARD, S.A.",
    "ruc":    "155742060-2-2023   DV 50",
    "aviso":  "155742060-2-2023-2023-574345230",
    "dir":    "Calle Ramón H. Jurado, Edificio RBS Tower, departamento PB 103C, "
              "urbanización Paitilla, corregimiento de San Francisco, distrito y provincia de Panamá",
    "tel":    "(507) 6796-9787",
    "correo": "ventas@eliteguardsa.com",
    "rep":    "MICHAEL ROSENTHAL COHEN",
    "cip":    "PE-12-1335",
}

NEG  = colors.HexColor("#1a1a1a")
NAR  = colors.HexColor("#eb5a2d")
GRIS = colors.HexColor("#5a5a5a")
LIN  = colors.HexColor("#c9c9c9")
FON  = colors.HexColor("#f2f2f2")
AMB  = colors.HexColor("#fff8e1")

def S(n, s, l, **k):
    return ParagraphStyle(n, fontName=k.pop("font", "Helvetica"), fontSize=s,
                          leading=l, textColor=k.pop("color", NEG), **k)
ST = {
 "h1":   S("h1", 15, 19, font="Helvetica-Bold"),
 "h2":   S("h2", 10.5, 14, font="Helvetica-Bold", color=NAR, spaceBefore=9, spaceAfter=4),
 "sub":  S("sub", 8.5, 11.5, color=GRIS),
 "body": S("body", 8.8, 12.5, alignment=TA_JUSTIFY, spaceAfter=4),
 "cell": S("cell", 8, 10.5),
 "cellb":S("cellb", 8, 10.5, font="Helvetica-Bold"),
 "cellh":S("cellh", 7.5, 10, font="Helvetica-Bold", color=colors.white),
 "small":S("small", 7.5, 10, color=GRIS),
}

def est_tabla(extra=()):
    return TableStyle([("GRID",(0,0),(-1,-1),0.4,LIN),
                       ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                       ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
                       ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]
                      + list(extra))

def vinetas(txts, ancho=176*mm):
    f = [[Paragraph("<font color='#eb5a2d'>&#9632;</font>", ST["cell"]),
          Paragraph(t, ST["cell"])] for t in txts]
    t = Table(f, colWidths=[6*mm, ancho-6*mm])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),3),
        ("TOPPADDING",(0,0),(-1,-1),2.5),("BOTTOMPADDING",(0,0),(-1,-1),2.5)]))
    return t

def firma(fecha):
    t = Table([[Paragraph("_______________________________________________<br/>"
                 "<b>%s &mdash; %s</b><br/>"
                 "<font color='#5a5a5a' size=7.5>Firma y nombre del proponente &middot; C.I.P. %s</font>"
                 % (PROP["rep"], PROP["razon"], PROP["cip"]), ST["cell"]),
                Paragraph("_______________________________<br/><b>%s</b><br/>"
                 "<font color='#5a5a5a' size=7.5>Fecha</font>" % fecha, ST["cell"])]],
              colWidths=[106*mm, 70*mm])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                           ("LEFTPADDING",(0,0),(-1,-1),0)]))
    return t

# ------------------------------------------------------------------ carátula
def banda(lic, titulo):
    def dibuja(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7); canvas.setFillColor(GRIS)
        canvas.drawString(20*mm, 12*mm, "Licitación ACP %s · %s · Proponente: %s"
                          % (lic["n"], lic["obj"], PROP["razon"]))
        canvas.drawRightString(196*mm, 12*mm, "Página %d" % doc.page)
        canvas.setStrokeColor(LIN); canvas.line(20*mm, 15*mm, 196*mm, 15*mm)
        canvas.restoreState()
    return dibuja

def cabecera(lic, titulo):
    f = [Table([[ImageReader(LOGO) and "", ""]], colWidths=[1,1])] if False else []
    from reportlab.platypus import Image
    img = Image(LOGO, width=34*mm, height=18.6*mm)
    enc = Table([[img, Paragraph(
        "<font size=8.5 color='#5a5a5a'>AUTORIDAD DEL CANAL DE PANAMÁ</font><br/>"
        "<font size=8.5 color='#5a5a5a'>Licitación pública N.° %s &middot; %s</font><br/>"
        "<font size=8.5 color='#5a5a5a'>Cierre: %s</font><br/><br/>"
        "<font size=14><b>%s</b></font>" % (lic["n"], lic["obj"], lic["cierre"], titulo),
        ST["cell"])]], colWidths=[40*mm, 136*mm])
    enc.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                             ("LEFTPADDING",(0,0),(0,0),0)]))
    f.append(enc)
    f.append(Spacer(1, 4))
    f.append(Table([[""]], colWidths=[176*mm], rowHeights=[1.8],
                   style=TableStyle([("BACKGROUND",(0,0),(-1,-1),NEG)])))
    f.append(Spacer(1, 8))
    return f

# -------------------------------------------------------------------- carta
def carta(lic):
    f = cabecera(lic, "Carta de presentación de la propuesta técnica")
    f.append(Paragraph("1.  Identificación del proponente", ST["h2"]))
    datos = [("Razón social (nombre legal registrado en el RUC)", PROP["razon"]),
             ("RUC y dígito verificador (DV)", PROP["ruc"]),
             ("N.° de Aviso de Operación", PROP["aviso"]),
             ("Dirección", PROP["dir"]),
             ("Persona autorizada", PROP["rep"]),
             ("Teléfono", PROP["tel"]),
             ("Correo electrónico", PROP["correo"])]
    t = Table([[Paragraph(a, ST["cellb"]), Paragraph(b, ST["cell"])] for a, b in datos],
              colWidths=[58*mm, 118*mm])
    t.setStyle(est_tabla([("BACKGROUND",(0,0),(0,-1),FON)]))
    f += [t, Spacer(1, 5)]
    f.append(Paragraph("El nombre legal indicado es el que consta en el Registro Único de "
        "Contribuyente ante la Dirección General de Ingresos, y es el mismo nombre legal "
        "utilizado en la propuesta de precio presentada en el Sistema de Licitaciones por "
        "Internet (SLI). No se utiliza nombre comercial. Se adjunta al final de este "
        "documento copia del Aviso de Operación vigente.", ST["body"]))

    f.append(Paragraph("2.  Renglones ofertados", ST["h2"]))
    cab = [Paragraph(x, ST["cellh"]) for x in
           ("Renglón","Código ACP","Descripción","Cantidad","Marca, modelo y N.° de parte ofertado")]
    filas = [cab] + [[Paragraph("<b>%s</b>" % r["n"], ST["cell"]),
                      Paragraph(r["cod"], ST["cell"]),
                      Paragraph(r["desc"], ST["cell"]),
                      Paragraph("%s %s" % (r["cant"], r["umc"]), ST["cell"]),
                      Paragraph("<b>%s</b> %s<br/>Talla %s" % (r["marca"], r["mod"], r["talla"]),
                                ST["cell"])] for r in lic["reng"]]
    t = Table(filas, colWidths=[17*mm, 25*mm, 48*mm, 19*mm, 67*mm], repeatRows=1)
    t.setStyle(est_tabla([("BACKGROUND",(0,0),(-1,0),NEG),
                          ("VALIGN",(0,0),(-1,-1),"TOP")]))
    f += [t, Spacer(1, 5), Paragraph(lic["nota_reng"], ST["body"])]

    f.append(Paragraph("3.  Declaración sobre productos de referencia (numeral 9.1.1)", ST["h2"]))
    for x in lic["ref"]:
        f.append(Paragraph(x, ST["body"]))

    f.append(Paragraph("4.  Declaraciones del proponente", ST["h2"]))
    f.append(vinetas(DECL(lic)))

    f.append(Paragraph("5.  Documentos que conforman esta propuesta técnica", ST["h2"]))
    f.append(vinetas(lic["docs"]))
    f.append(Spacer(1, 6))
    f.append(Paragraph("El proponente declara que la información técnica aquí presentada es "
        "veraz y que el bien ofertado cumple al 100% con la descripción del renglón "
        "correspondiente del pliego de cargos.", ST["body"]))
    f += [Spacer(1, 14), firma(lic["fecha"])]
    return f

def DECL(lic):
    return [
 "El bien ofertado es nuevo, sin uso y sin reconstruir (numeral 2.3 del pliego).",
 "Se otorga garantía por un período no menor de un (1) año, contado desde la fecha de recepción del objeto del contrato (numeral 5).",
 "Plazo de entrega: 120 días calendario o menos, contados a partir de la adjudicación de la orden de compra (numeral 3.1).",
 "Condiciones de entrega: DAP Panamá. El proponente asume el trámite y el costo de la declaración simplificada de aduanas, la descarga de los bienes y su colocación en sitio, en la Sección de Almacenes, Corozal Oeste, Edificio 652, área de recibo (numeral 3.2).",
 "Se adjunta la evidencia documental vigente de las certificaciones y normas exigidas en la descripción de cada renglón, junto con la literatura descriptiva, la imagen del producto ofertado y la marcación del producto o de la certificación (clase, fecha e identificación), conforme al numeral 9.1.",
 "El producto se entrega en la presentación indicada en la descripción del renglón (numeral 9.1).",
 "Se entrega muestra física de cada artículo ofertado, identificada con el nombre del proponente, el número de pliego %s y el número de propuesta, en Balboa, Ancón, Edificio 710, planta baja, antes de la fecha y hora de cierre (numeral 9.2)." % lic["n"],
 "Empaque, embalaje, estiba y entrega conforme a las mejores prácticas comerciales (referencia ASTM D5728), garantizando la facilidad de descarga en el punto de entrega (numeral 9.8).",
 "El proponente es distribuidor autorizado del fabricante y puede acreditar la trazabilidad de los bienes hasta el fabricante, a requerimiento de la Autoridad (numeral 9.7).",
 "La presente propuesta tiene una validez de 60 días calendario, contados a partir del acto de conocimiento de propuestas (numeral 1.3).",
 "El precio ofertado no incluye ITBMS ni impuestos de importación, conforme a la cláusula 4.28.6 del pliego de cargos único.",
 lic["enmiendas"],
]

# --------------------------------------------------------------- económica
def economica(lic):
    f = [PageBreak()]
    f += cabecera(lic, "Propuesta económica")
    f.append(Paragraph(lic["intro_econ"], ST["body"]))
    f.append(Spacer(1, 4))
    for r in lic["reng"]:
        cab = Table([[Paragraph("RENGLÓN<br/><font size=16><b>%s</b></font>" % r["n"],
                       ParagraphStyle("x", fontName="Helvetica-Bold", fontSize=7.5,
                                      leading=10, textColor=colors.white, alignment=TA_CENTER)),
                      Paragraph("<b><font size=10>%s</font></b><br/>"
                                "<font size=7.5 color='#5a5a5a'>Código ACP %s</font>"
                                % (r["desc"], r["cod"]), ST["cell"])]],
                    colWidths=[20*mm, 156*mm])
        cab.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0),NEG),
                                 ("BOX",(0,0),(-1,-1),0.8,NEG),
                                 ("LINEBELOW",(0,0),(-1,-1),1.4,NAR),
                                 ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                                 ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
        filas = [("Marca", r["marca"]),
                 ("Modelo y N.° de parte", "%s   ·   P/N %s" % (r["mod"], r["pn"])),
                 ("Talla ofertada", r["talla"]),
                 ("Cantidad solicitada", "%s   %s" % (r["cant"], r["um"])),
                 ("Precio unitario (USD)", "<b>US$ %s</b>" % r["pu"]),
                 ("Monto total del renglón (USD)", "<b>US$ %s</b>" % r["tot"]),
                 ("Validez de la oferta", "60 días calendario, contados a partir del acto de conocimiento de propuestas (numeral 1.3)"),
                 ("Plazo de entrega", lic["plazo"]),
                 ("Términos de entrega", "DAP Panamá. Incluye el trámite y el costo de la declaración simplificada de aduanas, la descarga de los bienes y su colocación en sitio, en la Sección de Almacenes, Corozal Oeste, Edificio 652, área de recibo (numeral 3.2)"),
                 ("Garantía", "Un (1) año contado desde la fecha de recepción del objeto del contrato (numeral 5)")]
        cu = Table([[Paragraph(a.upper(), ST["cellb"]), Paragraph(b, ST["cell"])] for a, b in filas],
                   colWidths=[48*mm, 128*mm])
        cu.setStyle(est_tabla([("BACKGROUND",(0,0),(0,-1),FON),
                               ("BACKGROUND",(1,4),(1,5),AMB),
                               ("VALIGN",(0,0),(-1,-1),"TOP")]))
        f += [KeepTogether([cab, cu]), Spacer(1, 7)]
    f.append(Paragraph("Nota sobre el precio ofertado", ST["h2"]))
    f.append(vinetas(["El precio ofertado NO incluye ITBMS ni impuestos de importación, "
        "conforme a la cláusula 4.28.6 del pliego de cargos único: la Autoridad del Canal "
        "de Panamá está exenta de dichos tributos."]))
    f += [Spacer(1, 16), firma(lic["fecha"])]
    return f

# ---------------------------------------------------------------- licitaciones
R88 = [
 dict(n="2", cod="PPE-GLO-00012", desc="Guante químico industrial, talla 9 (large)",
      marca="Elite Guard", mod="Guante de nitrilo corto J710", pn="J710 talla 9",
      talla="9 (Large)", cant="1,500", um="Pr (par)", umc="Pr", pu="1.14", tot="1,710.00"),
 dict(n="3", cod="PPE-GLO-00020", desc="Guante punteado de Kevlar®, hombre, talla 10 X-Large",
      marca="MCR Safety", mod="CutPro® 9366", pn="9366XL",
      talla="10 (X-Large)", cant="960", um="Pr (par)", umc="Pr", pu="7.69", tot="7,382.40"),
 dict(n="4", cod="PPE-GLO-00022", desc="Guante de examen de nitrilo, mediano, caja de 50 a 100",
      marca="MCR Safety", mod="NitriShield® 6008", pn="6008M",
      talla="Mediana (M)", cant="1,000", um="Box (caja)", umc="Box", pu="9.60", tot="9,600.00"),
 dict(n="5", cod="PPE-GLO-00031", desc="Guante anticorte ANSI A4 / EN 388 4-X-4-2-C, talla 9",
      marca="MCR Safety", mod="CutPro® 92754BP", pn="92754BPL",
      talla="9 (Large)", cant="5,000", um="Each (par)", umc="Each", pu="4.69", tot="23,450.00"),
 dict(n="6", cod="PPE-GLO-00033", desc="Guante tejido con palma y yemas de PU, talla 11",
      marca="MCR Safety", mod="CutPro® 92852PU", pn="92852PU",
      talla="11 (2X-Large)", cant="900", um="Each (par)", umc="Each", pu="2.89", tot="2,601.00"),
]
R16 = [
 dict(n="1", cod="PPE-EYE-00026", desc="Lente de seguridad, claro",
      marca="MCR Safety", mod="Memphis® MP1 — MP110AF", pn="MP110AF",
      talla="única", cant="15,840", um="Pr (par/unidad)", umc="Pr", pu="4.59", tot="72,705.60"),
 dict(n="2", cod="PPE-EYE-00027", desc="Lente de seguridad, oscuro",
      marca="MCR Safety", mod="Memphis® MP1 — MP112PF", pn="MP112PF",
      talla="única", cant="10,800", um="Pr (par/unidad)", umc="Pr", pu="4.59", tot="49,572.00"),
]
DOCS88 = [
 "Carta de presentación de la propuesta técnica y propuesta económica (este documento), con el Aviso de Operación del proponente.",
 "Un documento por renglón ofertado, identificado con el número de renglón y el código ACP, que contiene la matriz de cumplimiento técnico (numeral 9.1.2) y, anexa, la literatura descriptiva del fabricante con las características de cumplimiento resaltadas e imagen del producto (numeral 9.1.3).",
 "Para el renglón 3, la marcación del producto: etiqueta DuPont™ Kevlar®.",
]
DOCS16 = [
 "Carta de presentación de la propuesta técnica y propuesta económica (este documento), con el Aviso de Operación del proponente.",
 "Un documento por renglón ofertado, identificado con el número de renglón y el código ACP, que contiene la matriz de cumplimiento técnico (numeral 9.1.2) y, anexa, la literatura descriptiva del fabricante con las características de cumplimiento resaltadas e imagen del producto (numeral 9.1.3).",
]

LICS = [
 dict(n="215088", obj="Guantes", cierre="9 de octubre de 2026, 11:00 a.m.",
      fecha="7 de octubre de 2026", reng=R88, docs=DOCS88,
      nota_reng="No se oferta el renglón 1 (guante dieléctrico de baja tensión), por no contar "
        "el proponente con producto que cumpla la descripción. La adjudicación es por precio "
        "más bajo POR RENGLÓN (numeral 1.5), por lo que la propuesta se presenta sobre los "
        "cinco renglones restantes.",
      ref=["[ X ]&nbsp;&nbsp; El proponente <b>SÍ</b> oferta la marca y el modelo de referencia "
           "especificados por la Autoridad en el renglón <b>3</b>. Conforme al numeral 9.1.1 del "
           "pliego, se deja constancia expresa de este hecho en la presente propuesta técnica, "
           "cargada en el SLI.",
           "[ X ]&nbsp;&nbsp; El proponente <b>NO</b> oferta el producto de referencia en los "
           "renglones <b>2, 4, 5 y 6</b>; oferta producto equivalente que cumple al 100% con la "
           "descripción del renglón, adjunta literatura descriptiva del fabricante, imagen del "
           "producto y entrega muestra física.",
           "<font color='#5a5a5a'>Nota: el numeral 9.2 de este pliego exige la entrega de muestra "
           "sin excepción, aun en los renglones donde se oferte el producto de referencia de la "
           "Autoridad.</font>"],
      enmiendas="El proponente acusa recibo de las enmiendas N.° 1 (22-sep-2026) y N.° 2 (30-sep-2026) emitidas por la Autoridad.",
      plazo="120 días calendario, contados a partir de la adjudicación de la orden de compra (numeral 3.1)",
      intro_econ="La presente propuesta económica se formula renglón por renglón. La adjudicación "
        "de esta licitación es por precio más bajo POR RENGLÓN (numeral 1.5), por lo que cada "
        "renglón se cotiza de forma independiente. No se oferta el renglón 1.",
      salida=RAIZ+"/215088-guantes-acp/final/00-CARTA-Y-PROPUESTA-ECONOMICA-215088.pdf"),
 dict(n="215116", obj="Lentes de protección personal", cierre="9 de octubre de 2026, 9:00 a.m.",
      fecha="7 de octubre de 2026", reng=R16, docs=DOCS16,
      nota_reng="El proponente concurre únicamente a los renglones 1 y 2. La adjudicación es por "
        "precio más bajo POR RENGLÓN (numeral 1.5), por lo que la propuesta se presenta sobre "
        "esos dos renglones.",
      ref=["[ X ]&nbsp;&nbsp; El proponente <b>NO</b> oferta el producto de referencia en los "
           "renglones <b>1 y 2</b>; oferta producto equivalente que cumple al 100% con la "
           "descripción del renglón, adjunta literatura descriptiva del fabricante, imagen del "
           "producto y entrega muestra física.",
           "<font color='#5a5a5a'>Al no ofertarse el producto de referencia de la Autoridad, no "
           "aplica la excepción del numeral 9.2: se entrega muestra física de ambos renglones.</font>"],
      enmiendas="El proponente acusa recibo de la enmienda N.° 1 del 23 de septiembre de 2026 emitida por la Autoridad.",
      plazo="120 días calendario, contados a partir de la adjudicación de la orden de compra (numeral 3.1, según enmienda N.° 1)",
      intro_econ="La presente propuesta económica se formula renglón por renglón. La adjudicación "
        "de esta licitación es por precio más bajo POR RENGLÓN (numeral 1.5), por lo que cada "
        "renglón se cotiza de forma independiente.",
      salida=RAIZ+"/215116-lentes-acp/final/00-CARTA-Y-PROPUESTA-ECONOMICA-215116.pdf"),
]

for lic in LICS:
    tmp = "/tmp/_%s.pdf" % lic["n"]
    d = SimpleDocTemplate(tmp, pagesize=letter,
                          leftMargin=20*mm, rightMargin=16*mm,
                          topMargin=16*mm, bottomMargin=20*mm,
                          title="Licitación ACP %s — Carta y propuesta económica" % lic["n"],
                          author=PROP["razon"])
    d.build(carta(lic) + economica(lic),
            onFirstPage=banda(lic, ""), onLaterPages=banda(lic, ""))
    doc = pymupdf.open(tmp)
    doc.insert_file(AVISO)
    os.makedirs(os.path.dirname(lic["salida"]), exist_ok=True)
    doc.save(lic["salida"], garbage=3, deflate=True)
    print("%-72s %d páginas" % (lic["salida"].split("/")[-1], doc.page_count))
    doc.close(); os.remove(tmp)
