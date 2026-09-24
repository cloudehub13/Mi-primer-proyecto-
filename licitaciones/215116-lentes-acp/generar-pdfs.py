#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera los PDF de la propuesta técnica de la licitación ACP 215116
(Lentes de protección personal), listos para subir al SLI.

Uso:  python3 generar-pdfs.py
Salida: ./pdf/*.pdf

Antes de generar, edita el bloque PROPONENTE y, en cada renglón, la columna
"ofertado" si cambias de modelo. Todo lo que quede entre « » son datos que
hay que llenar antes de subir al SLI.
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                               TableStyle, PageBreak)

# ---------------------------------------------------------------- proponente
PROPONENTE = {
    "razon_social": "«RAZÓN SOCIAL LEGAL SEGÚN RUC»",
    "ruc":          "«RUC + DV»",
    "aviso_op":     "«No. DE AVISO DE OPERACIÓN»",
    "seguro_soc":   "«No. PATRONAL (CSS)»",
    "dirección":    "«DIRECCIÓN»",
    "teléfono":     "«TELÉFONO»",
    "correo":       "«CORREO ELECTRÓNICO»",
    "representante":"«NOMBRE DEL REPRESENTANTE / PERSONA AUTORIZADA»",
    "cargo":        "«CARGO»",
}

LIC = {
    "número": "215116",
    "título": "LENTES DE PROTECCIÓN PERSONAL",
    "entidad": "AUTORIDAD DEL CANAL DE PANAMÁ",
    "cierre": "25 de septiembre de 2026, 11:00 a.m.",
    "agente": "Joseline I. Hernández N.",
}

# ------------------------------------------------------------------- estilos
NEGRO  = colors.HexColor("#1a1a1a")
GRIS   = colors.HexColor("#5a5a5a")
LINEA  = colors.HexColor("#c9c9c9")
FONDO  = colors.HexColor("#f2f2f2")

def S(name, size, leading, **kw):
    return ParagraphStyle(name, fontName=kw.pop("font", "Helvetica"),
                          fontSize=size, leading=leading,
                          textColor=kw.pop("color", NEGRO), **kw)

ST = {
    "h1":    S("h1", 15, 19, font="Helvetica-Bold", spaceAfter=2),
    "h2":    S("h2", 11, 14, font="Helvetica-Bold", spaceBefore=10, spaceAfter=4),
    "sub":   S("sub", 9, 12, color=GRIS),
    "body":  S("body", 9, 13, alignment=TA_JUSTIFY, spaceAfter=5),
    "cell":  S("cell", 8, 10.5),
    "cellb": S("cellb", 8, 10.5, font="Helvetica-Bold"),
    "cellh": S("cellh", 8, 10.5, font="Helvetica-Bold", color=colors.white),
    "small": S("small", 7.5, 10, color=GRIS),
    "cent":  S("cent", 9, 12, alignment=TA_CENTER),
}

def pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GRIS)
    canvas.drawString(20*mm, 12*mm,
        "Licitación ACP %s - %s | Proponente: %s"
        % (LIC["número"], LIC["título"], PROPONENTE["razon_social"]))
    canvas.drawRightString(196*mm, 12*mm, "Página %d" % doc.page)
    canvas.setStrokeColor(LINEA)
    canvas.line(20*mm, 15*mm, 196*mm, 15*mm)
    canvas.restoreState()

def encabezado(tit_doc, rgl=None, cod=None):
    f = []
    f.append(Paragraph(LIC["entidad"], ST["sub"]))
    f.append(Paragraph("Licitación pública No. %s &mdash; %s"
                       % (LIC["número"], LIC["título"]), ST["sub"]))
    f.append(Spacer(1, 6))
    f.append(Paragraph(tit_doc, ST["h1"]))
    if rgl:
        f.append(Paragraph("<b>Aplica al RENGLÓN %s</b> &mdash; código ACP <b>%s</b>"
                           % (rgl, cod), ST["body"]))
    f.append(Spacer(1, 2))
    f.append(Table([[""]], colWidths=[176*mm], rowHeights=[1.6],
                   style=TableStyle([("BACKGROUND", (0,0), (-1,-1), NEGRO)])))
    f.append(Spacer(1, 8))
    return f

def bloque_proponente():
    p = PROPONENTE
    datos = [
        ["Razón social (nombre legal según RUC)", p["razon_social"]],
        ["RUC y dígito verificador", p["ruc"]],
        ["Aviso de operación", p["aviso_op"]],
        ["No. patronal (CSS)", p["seguro_soc"]],
        ["Persona autorizada", "%s &mdash; %s" % (p["representante"], p["cargo"])],
        ["Teléfono / correo", "%s &nbsp;&middot;&nbsp; %s" % (p["teléfono"], p["correo"])],
    ]
    filas = [[Paragraph(a, ST["cellb"]), Paragraph(b, ST["cell"])] for a, b in datos]
    t = Table(filas, colWidths=[58*mm, 118*mm])
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.4, LINEA),
        ("BACKGROUND", (0,0), (0,-1), FONDO),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    return t

def tabla_producto(d):
    datos = [
        ["Marca", d["marca"]],
        ["Modelo / serie", d["modelo"]],
        ["Número de parte ofertado", "<b>%s</b>" % d["pn"]],
        ["Cantidad ofertada", "%s %s" % (d["cant"], d["um"])],
        ["Producto de referencia ACP", d["ref_acp"]],
        ["Condición", "Bien nuevo, sin uso, de fabricación reciente"],
    ]
    filas = [[Paragraph(a, ST["cellb"]), Paragraph(b, ST["cell"])] for a, b in datos]
    t = Table(filas, colWidths=[58*mm, 118*mm])
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.4, LINEA),
        ("BACKGROUND", (0,0), (0,-1), FONDO),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    return t

def matriz(filas):
    head = [Paragraph("Requisito del pliego (renglón)", ST["cellh"]),
            Paragraph("Característica del producto ofertado", ST["cellh"]),
            Paragraph("Evidencia", ST["cellh"])]
    data = [head]
    for req, ofr, ev in filas:
        data.append([Paragraph(req, ST["cell"]),
                     Paragraph(ofr, ST["cell"]),
                     Paragraph(ev, ST["small"])])
    t = Table(data, colWidths=[56*mm, 82*mm, 38*mm], repeatRows=1)
    estilo = [
        ("GRID", (0,0), (-1,-1), 0.4, LINEA),
        ("BACKGROUND", (0,0), (-1,0), NEGRO),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            estilo.append(("BACKGROUND", (0,i), (-1,i), FONDO))
    t.setStyle(TableStyle(estilo))
    return t

def firma():
    f = [Spacer(1, 18)]
    f.append(Paragraph(
        "El proponente declara que la información técnica aquí presentada es veraz y que el "
        "bien ofertado cumple al 100% con la descripción del renglón correspondiente del "
        "pliego de cargos.", ST["body"]))
    f.append(Spacer(1, 22))
    t = Table([["_" * 46, "", "_" * 34]], colWidths=[82*mm, 12*mm, 72*mm])
    t.setStyle(TableStyle([("LINEBELOW", (0,0), (-1,-1), 0, colors.white),
                           ("BOTTOMPADDING", (0,0), (-1,-1), 2)]))
    f.append(t)
    t2 = Table([[Paragraph("Firma y nombre del proponente<br/>%s<br/>%s"
                           % (PROPONENTE["representante"], PROPONENTE["razon_social"]), ST["small"]),
                 "",
                 Paragraph("Fecha", ST["small"])]],
               colWidths=[82*mm, 12*mm, 72*mm])
    f.append(t2)
    return f

def declaraciones_estandar():
    items = [
        "El bien ofertado es <b>nuevo</b>, sin uso y sin reconstruir (numeral 2.3 del pliego).",
        "Se otorga <b>garantía por un período no menor de un (1) año</b> contado desde la fecha "
        "de recepcion del objeto del contrato (numeral 5).",
        "Plazo de entrega: <b>90 días calendario</b> o menos, contados a partir de la "
        "adjudicación de la orden de compra (numeral 3.1).",
        "Condiciones de entrega: <b>DAP Panamá</b>. El proponente asume el trámite y el costo "
        "de la declaración simplificada de aduanas, la descarga de los bienes y su colocación "
        "en sitio, en la Sección de Almacenes, Corozal Oeste, Edificio 652, área de recibo "
        "(numeral 3.2).",
        "<b>El instructivo de uso del fabricante se incluye con el producto</b>, conforme lo "
        "exige la descripción del renglón.",
        "Empaque, embalaje, estiba y entrega conforme a las mejores prácticas comerciales "
        "(referencia ASTM D5728), garantizando la facilidad de descarga en el punto de entrega "
        "(numeral 9.8).",
        "El proponente es distribuidor autorizado del fabricante y puede acreditar la "
        "<b>trazabilidad</b> de los bienes hasta el fabricante, a requerimiento de la "
        "Autoridad (numeral 9.7).",
        "La presente propuesta tiene una <b>validez de 60 días calendario</b> contados a partir "
        "del acto de conocimiento de propuestas (numeral 1.3).",
        "El precio ofertado <b>no incluye ITBMS ni impuestos de importación</b>, conforme a la "
        "cláusula 4.28.6 del pliego de cargos único.",
    ]
    filas = [[Paragraph("&bull;", ST["cell"]), Paragraph(x, ST["cell"])] for x in items]
    t = Table(filas, colWidths=[6*mm, 170*mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
    ]))
    return t

# ------------------------------------------------------------------ contenido
EV_FICHA = "Anexo A &mdash; ficha técnica del fabricante, sección resaltada"
EV_CERT  = "Anexo B &mdash; declaración de conformidad / certificado del fabricante"
EV_DECL  = "Declaración del proponente (este documento)"

EVF = "Anexo A &mdash; ficha técnica MCR Safety MP110AF (serie Memphis MP1), sección resaltada"
EVT = "Anexo A &mdash; ficha MP1, tabla &quot;Tintes Disponibles&quot;, fila del P/N ofertado"
EVC = "Anexo A &mdash; ficha MP1, sección &quot;Certificaciones&quot;"
EVD = "Declaración del proponente (este documento)"

RENGLONES = [
 {
  "n": "1", "item": "PPE-EYE-00026",
  "título": "PROPUESTA TÉCNICA &mdash; Lente de seguridad, claro",
  "archivo": "01-RENGLON-1-PPE-EYE-00026.pdf",
  "prod": {"marca": "MCR Safety", "modelo": "Memphis&reg; serie MP1",
           "pn": "MP110AF", "cant": "15,840", "um": "Pr (par/unidad)",
           "ref_acp": "SureWerx / Jackson SG Classic P/N 50001 &mdash; no se oferta el producto de referencia; se oferta producto equivalente que cumple al 100%"},
  "matriz": [
    ("Spectacle, safety, <b>clear</b>",
     "Lente de seguridad tipo spectacle con ocular <b>claro</b> (VLT 90%), montura y patillas negras, "
     "patilla tipo bayoneta de TPR y puente nasal de TPR.", EVF),
    ("<b>Polycarbonate lens</b>",
     "Ocular de <b>policarbonato</b>; montura de policarbonato. Diseño <b>envolvente de lente única</b>.", EVF),
    ("Shall comply with <b>ANSI Z87.1 high impact</b> or EN 166:2001 mechanical strength &quot;F&quot;",
     "Certificado <b>ANSI Z87+ 1 2020 &mdash; Estándares de Alto Impacto</b>, según consta en la ficha "
     "técnica del fabricante.", EVC),
    ("<b>Scratch resistant</b>",
     "<b>Resistencia a rayaduras</b> declarada por el fabricante para el P/N MP110AF.", EVT),
    ("<b>Antifog coating</b>",
     "Recubrimiento antiempañante <b>UV-AF&trade; Eco-Amigable Anti Empaño</b>, aplicado en fábrica.", EVT),
    ("Provides <b>99% UV protection</b>",
     "Ficha del fabricante: <b>rayos ultravioleta 0&ndash;385 nm: 99%</b>. El ocular de policarbonato "
     "bloquea el <b>99.9% de los rayos UVA, UVB y UVC</b>.", EVF),
    ("<b>With sideshields</b> to protect from airborne particles",
     "Diseño <b>envolvente de lente única</b>: el ocular se extiende de forma continua hacia la zona "
     "temporal y entrega cobertura lateral sin abertura entre el ocular y la sien, lo que bloquea el "
     "ingreso lateral de partículas en suspensión.", EVF),
    ("Shall provide <b>non-distorsion vision</b>",
     "Lente única envolvente, sin uniones ni marco frontal, que ofrece <b>vista sin obstrucciones</b> "
     "y libre de distorsión óptica.", EVF),
    ("Manufacturer&#39;s descriptive literature and <b>product sample required with bid</b>",
     "Se adjunta la literatura descriptiva del fabricante (Anexo A) y se entrega <b>muestra física</b> "
     "del artículo ofertado, rotulada con el nombre del proponente, el número de pliego 215116 y el "
     "número de propuesta, en Balboa, Ancón, Edificio 710, planta baja, antes de la fecha y hora de cierre.", EVD),
    ("<b>Use instructions shall be included with product</b>",
     "Cada unidad se entrega con el instructivo de uso del fabricante. El producto incluye además "
     "cordón portalentes modelo 219.", EVD),
  ],
  "nota": None,
 },
 {
  "n": "2", "item": "PPE-EYE-00027",
  "título": "PROPUESTA TÉCNICA &mdash; Lente de seguridad, oscuro",
  "archivo": "02-RENGLON-2-PPE-EYE-00027.pdf",
  "prod": {"marca": "MCR Safety", "modelo": "Memphis&reg; serie MP1",
           "pn": "MP112PF", "cant": "10,800", "um": "Pr (par/unidad)",
           "ref_acp": "SureWerx / Jackson SG Classic P/N 50007 &mdash; no se oferta el producto de referencia; se oferta producto equivalente que cumple al 100%"},
  "matriz": [
    ("Spectacle, safety, <b>dark</b>",
     "Lente de seguridad tipo spectacle con ocular <b>gris (oscuro)</b>, VLT 13%, montura y patillas "
     "negras. Misma plataforma Memphis MP1 del P/N MP110AF.", EVT),
    ("<b>Polycarbonate lens</b>",
     "Ocular de <b>policarbonato</b>, diseño <b>envolvente de lente única</b> (serie Memphis MP1).", EVF),
    ("Shall comply with <b>ANSI Z87.1 high impact</b> or EN 166:2001 mechanical strength &quot;F&quot;",
     "La serie Memphis MP1 está certificada <b>ANSI Z87+ 1 2020 &mdash; Estándares de Alto Impacto</b>.", EVC),
    ("<b>Scratch resistant</b>",
     "<b>Resistencia a rayaduras</b> declarada por el fabricante para los P/N de la serie MP1.", EVT),
    ("<b>Antifog coating</b>",
     "Recubrimiento antiempañante <b>MAX6&trade; Anti-Fog</b>, el de mayor desempeño antiempañante de "
     "MCR Safety, aplicado en fábrica.", EVT),
    ("Provides <b>99% UV protection</b>",
     "Ocular de policarbonato de la serie MP1: <b>99% de filtrado en 0&ndash;385 nm</b> y bloqueo del "
     "<b>99.9% de los rayos UVA, UVB y UVC</b>.", EVF),
    ("<b>With sideshields</b> to protect from airborne particles",
     "Diseño <b>envolvente de lente única</b> con cobertura lateral continua, sin abertura entre el "
     "ocular y la sien.", EVF),
    ("Shall provide <b>non-distorsion vision</b>",
     "Lente única envolvente, sin uniones ni marco frontal, con vista sin obstrucciones y libre de "
     "distorsión óptica.", EVF),
    ("Manufacturer&#39;s descriptive literature and <b>product sample required with bid</b>",
     "Se adjunta la literatura descriptiva del fabricante (Anexo A) y se entrega <b>muestra física</b> "
     "del artículo ofertado, debidamente rotulada, antes de la fecha y hora de cierre.", EVD),
    ("<b>Use instructions shall be included with product</b>",
     "Cada unidad se entrega con el instructivo de uso del fabricante. Incluye cordón portalentes "
     "modelo 219.", EVD),
  ],
  "nota": "El renglón requiere ocular <b>oscuro (dark)</b>. El ocular ofertado es gris de tinte sólido "
          "(VLT 13%), no espejado. El producto de referencia citado por la Autoridad (Jackson 50007) "
          "corresponde a un ocular humo espejado; la descripción del renglón no exige acabado espejado, "
          "por lo que el ocular gris sólido ofertado cumple el requisito de oscurecimiento con la "
          "ventaja de no generar reflejo hacia terceros.<br/><br/>"
          "El MP110AF y el MP112PF son el mismo modelo de la serie Memphis MP1 en dos tintes, por lo "
          "que la literatura del fabricante de la serie sustenta ambos renglones.",
 },
]

# ------------------------------------------------------------------ generador
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf")

def doc(path):
    return SimpleDocTemplate(path, pagesize=letter,
                             leftMargin=20*mm, rightMargin=19*mm,
                             topMargin=18*mm, bottomMargin=22*mm,
                             title="Licitación ACP %s" % LIC["número"],
                             author=PROPONENTE["razon_social"])

def carta():
    path = os.path.join(OUT, "00-CARTA-DE-PRESENTACION.pdf")
    f = encabezado("CARTA DE PRESENTACIÓN DE LA PROPUESTA TÉCNICA")
    f.append(Paragraph("1. Identificación del proponente", ST["h2"]))
    f.append(bloque_proponente())
    f.append(Paragraph(
        "El nombre legal indicado es el que consta en el Registro Único de Contribuyente (RUC) "
        "ante la Dirección General de Ingresos y es <b>el mismo nombre legal utilizado en la "
        "propuesta de precio presentada en el Sistema de Licitaciones por Internet (SLI)</b>. "
        "No se utiliza nombre comercial.", ST["small"]))

    f.append(Paragraph("2. Renglones ofertados", ST["h2"]))
    filas = [[Paragraph(x, ST["cellh"]) for x in
              ("Renglón", "Código ACP", "Descripción", "Cantidad", "Producto ofertado")]]
    for r in RENGLONES:
        p = r["prod"]
        filas.append([Paragraph(r["n"], ST["cellb"]),
                      Paragraph(r["item"], ST["cell"]),
                      Paragraph(r["título"].split("&mdash;")[-1].strip(), ST["cell"]),
                      Paragraph("%s %s" % (p["cant"], "Pr"), ST["cell"]),
                      Paragraph("%s %s<br/>P/N <b>%s</b>" % (p["marca"], p["modelo"], p["pn"]), ST["cell"])])
    t = Table(filas, colWidths=[17*mm, 26*mm, 53*mm, 18*mm, 62*mm], repeatRows=1)
    est = [("GRID", (0,0), (-1,-1), 0.4, LINEA),
           ("BACKGROUND", (0,0), (-1,0), NEGRO),
           ("VALIGN", (0,0), (-1,-1), "TOP"),
           ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
           ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4)]
    for i in range(1, len(filas)):
        if i % 2 == 0:
            est.append(("BACKGROUND", (0,i), (-1,i), FONDO))
    t.setStyle(TableStyle(est))
    f.append(t)
    f.append(Spacer(1, 4))
    f.append(Paragraph(
        "«ELIMINAR DE ESTA TABLA CUALQUIER RENGLÓN QUE NO SE VAYA A OFERTAR. La "
        "adjudicación es por precio más bajo POR RENGLÓN, de modo que se puede ofertar "
        "parcialmente.»", ST["small"]))

    f.append(Paragraph("3. Declaración sobre productos de referencia (numeral 9.1.1)", ST["h2"]))
    f.append(Paragraph(
        "«MARCAR LA OPCIÓN QUE CORRESPONDA POR RENGLÓN»<br/><br/>"
        "[ ] El proponente <b>SI</b> oferta la marca y modelo de referencia especificados por la "
        "Autoridad en el(los) renglón(es): ____________. Conforme al numeral 9.1.1 del pliego, "
        "se deja constancia expresa de este hecho en la propuesta técnica presentada por el SLI, "
        "por lo que no se requiere propuesta técnica adicional ni muestra para dicho(s) "
        "renglón(es).<br/><br/>"
        "[ ] El proponente <b>NO</b> oferta el producto de referencia en el(los) renglón(es): "
        "____________; oferta producto equivalente que cumple al 100% con la descripción del "
        "renglón, adjunta literatura descriptiva del fabricante y entrega muestra física.",
        ST["body"]))

    f.append(Paragraph("4. Declaraciones del proponente", ST["h2"]))
    f.append(declaraciones_estandar())

    f.append(Paragraph("5. Documentos que conforman esta propuesta técnica", ST["h2"]))
    docs = [
        "00 &mdash; Carta de presentación de la propuesta técnica (este documento).",
        "01 a 05 &mdash; Matriz de cumplimiento técnico, <b>un documento por renglón</b>, "
        "identificado con el número de renglón y el código ACP al que aplica (numeral 9.1.2).",
        "Anexo A &mdash; Literatura descriptiva del fabricante por cada artículo ofertado, "
        "<b>con las características de cumplimiento resaltadas</b> (numeral 9.1.3).",
        "Anexo B &mdash; Declaración de conformidad / certificado de cumplimiento ANSI/ISEA "
        "Z87.1 emitido por el fabricante.",
        "Anexo C &mdash; Carta de distribuidor autorizado del fabricante (trazabilidad, "
        "numeral 9.7).",
    ]
    filas = [[Paragraph("&bull;", ST["cell"]), Paragraph(x, ST["cell"])] for x in docs]
    t = Table(filas, colWidths=[6*mm, 170*mm])
    t.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"),
                           ("LEFTPADDING", (0,0), (-1,-1), 0),
                           ("TOPPADDING", (0,0), (-1,-1), 2),
                           ("BOTTOMPADDING", (0,0), (-1,-1), 2)]))
    f.append(t)
    f += firma()
    doc(path).build(f, onFirstPage=pie, onLaterPages=pie)
    return path

def doc_renglon(r):
    path = os.path.join(OUT, r["archivo"])
    f = encabezado(r["título"], r["n"], r["item"])
    f.append(Paragraph("1. Artículo ofertado", ST["h2"]))
    f.append(tabla_producto(r["prod"]))
    f.append(Paragraph("2. Matriz de cumplimiento técnico", ST["h2"]))
    f.append(Paragraph(
        "La columna izquierda transcribe el requisito tal como aparece en la descripción del "
        "renglón; la columna central indica la característica concreta del artículo ofertado que "
        "lo satisface; la columna derecha indica el documento donde la Autoridad puede verificarla.",
        ST["small"]))
    f.append(Spacer(1, 5))
    f.append(matriz(r["matriz"]))
    if r["nota"]:
        f.append(Paragraph("3. Nota técnica", ST["h2"]))
        f.append(Paragraph(r["nota"], ST["body"]))
    f.append(Paragraph("%d. Declaraciones aplicables a este renglón" % (4 if r["nota"] else 3), ST["h2"]))
    f.append(declaraciones_estandar())
    f += firma()
    doc(path).build(f, onFirstPage=pie, onLaterPages=pie)
    return path

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(carta())
    for r in RENGLONES:
        print(doc_renglon(r))
