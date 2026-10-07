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
    "razon_social": "ELITE GUARD, S.A.",
    "ruc":          "155742060-2-2023  DV 50",
    "aviso_op":     "«No. DE AVISO DE OPERACIÓN»",
    "seguro_soc":   "«No. PATRONAL (CSS)»",
    "dirección":    "«DIRECCIÓN»",
    "teléfono":     "«TELÉFONO»",
    "correo":       "ventas@eliteguardsa.com",
    "representante":"MICHAEL ROSENTHAL",
    "cargo":        "«CARGO»",
}

LIC = {
    "número": "215088",
    "título": "GUANTES",
    "entidad": "AUTORIDAD DEL CANAL DE PANAMÁ",
    "cierre": "9 de octubre de 2026, 11:00 a.m. (enmienda 2 del 30-sep-2026)",
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
    """Solo la declaracion de veracidad: la firma va en la carta de
    presentacion, que es el documento que el proponente suscribe."""
    f = [Spacer(1, 18)]
    f.append(Paragraph(
        "El proponente declara que la información técnica aquí presentada es veraz y que el "
        "bien ofertado cumple al 100% con la descripción del renglón correspondiente del "
        "pliego de cargos.", ST["body"]))
    return f

def declaraciones_estandar():
    items = [
        "El bien ofertado es <b>nuevo</b>, sin uso y sin reconstruir (numeral 2.3 del pliego).",
        "Se otorga <b>garantía por un período no menor de un (1) año</b> contado desde la fecha "
        "de recepción del objeto del contrato (numeral 5).",
        "Plazo de entrega: <b>120 días calendario</b> o menos, contados a partir de la "
        "adjudicación de la orden de compra (numeral 3.1).",
        "Condiciones de entrega: <b>DAP Panamá</b>. El proponente asume el trámite y el costo "
        "de la declaración simplificada de aduanas, la descarga de los bienes y su colocación "
        "en sitio, en la Sección de Almacenes, Corozal Oeste, Edificio 652, área de recibo "
        "(numeral 3.2).",
        "Se adjunta la <b>evidencia documental vigente</b> de las certificaciones y normas "
        "exigidas en la descripción del renglón, junto con la <b>literatura descriptiva</b>, la "
        "<b>imagen del producto ofertado</b> y la <b>marcación del producto o de la "
        "certificación</b> (clase, fecha e identificación), conforme al numeral 9.1.",
        "El producto se entrega en la <b>presentación indicada en la descripción del renglón</b> "
        "(numeral 9.1).",
        "Se entrega <b>muestra física</b> del artículo ofertado, identificada con el nombre del "
        "proponente, el número de pliego 215088 y el número de propuesta, en Balboa, Ancón, "
        "Edificio 710, planta baja, antes de la fecha y hora de cierre (numeral 9.2).",
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

EVF = "Anexo A &mdash; ficha técnica del fabricante, característica resaltada"
EVI = "Anexo A &mdash; imagen del producto ofertado"
EVM = "Anexo B &mdash; marcación del producto / etiqueta del fabricante"
EVC = "Anexo C &mdash; certificación o declaración de conformidad vigente"
EVD = "Declaración del proponente (este documento)"

RENGLONES = [
 {
  "n": "2", "item": "PPE-GLO-00012",
  "título": "PROPUESTA TÉCNICA &mdash; Guante químico industrial, talla large",
  "archivo": "02-RENGLON-2-PPE-GLO-00012.pdf",
  "prod": {"marca": "Elite Guard", "modelo": "Guante de nitrilo corto J710",
           "pn": "J710 talla 9 (Large)", "cant": "1,500", "um": "Pr (par)",
           "ref_acp": "La descripción del renglón no indica producto de referencia ACP. Se oferta "
                      "producto que cumple con la descripción."},
  "matriz": [
    ("<b>Gloves, chemical</b>",
     "Guante de inmersión formulado para el contacto con sustancias químicas. Certificado "
     "<b>EN ISO 374-1 Tipo A</b> con el código de ensayo <b>AGJKLPT</b>, es decir, ensayado con "
     "éxito frente a <b>seis</b> de los grupos de productos químicos de la norma, que es el "
     "nivel más exigente de la clasificación. Categoría <b>CE CAT III</b> (riesgo mortal o "
     "irreversible), organismo notificado <b>0493</b>.", EVC),
    ("<b>Industrial</b>",
     "Guante de uso industrial, no de un solo uso: cuerpo de nitrilo con <b>superficie texturada</b> "
     "para agarre en mojado y <b>flocado interior</b> de algodón para jornada completa. Declara "
     "resistencia mecánica <b>EN 388 &mdash; 4102X</b> (abrasión 4, corte 1, desgarro 0, punción 2). "
     "Apto para industria química, petrolera y alimentaria.", EVF),
    ("<b>Large</b>",
     "Se oferta la <b>talla 9</b>, que es la que corresponde a <b>Large</b> en la escala "
     "dimensional de <b>ISO 21420</b>. El modelo se fabrica en tallas 8, 9 y 10.", EVD),
    ("Documentación exigida por el numeral 9.1",
     "Se adjuntan la ficha técnica del fabricante con las características resaltadas, la "
     "<b>imagen del producto</b> y la <b>marcación</b> que el guante lleva impresa en el puño "
     "(referencia, talla, pictogramas y marcado CE).", EVI),
  ],
  "nota": "<b>Prestaciones adicionales del producto ofertado</b>, por encima de lo exigido por el "
          "renglón: formulación <b>libre de proteínas</b>, que reduce el riesgo de reacción "
          "alérgica; <b>sin silicona</b>, apto para pintura, electrónica y manipulación de vidrio; "
          "<b>apto para contacto con alimentos</b>; y certificación <b>ISO 18889 nivel G2</b> para "
          "el manejo de plaguicidas.<br/><br/>"
          "El producto es de marca propia del proponente, lo que asegura la trazabilidad directa "
          "exigida por el numeral 9.7 y el control del plazo de entrega.",
 },
 {
  "n": "3", "item": "PPE-GLO-00020",
  "título": "PROPUESTA TÉCNICA &mdash; Guante punteado de Kevlar&reg;, hombre",
  "archivo": "03-RENGLON-3-PPE-GLO-00020.pdf",
  "prod": {"marca": "MCR Safety", "modelo": "CutPro&reg; serie 9366",
           "pn": "9366XL (talla 10 / X-Large)", "cant": "960", "um": "Pr (par)",
           "ref_acp": "MCR Safety CutPro 9366 &mdash; <b>se oferta el producto de referencia ACP</b>, "
                      "conforme al numeral 9.1.1 del pliego"},
  "matriz": [
    ("<b>Gloves, dotted</b>",
     "Guante <b>punteado</b>: tejido de punto con puntos de PVC negro aplicados sobre la trama.", EVF),
    ("<b>Kevlar</b>, with <b>PVC dots on both sides</b>",
     "Concha de aramida <b>Kevlar&reg;</b> con <b>puntos de PVC negro en ambas caras</b>. Al estar "
     "punteado por los dos lados, el guante se puede voltear y usar por el revés, lo que duplica "
     "su vida útil. Los puntos aportan agarre y resistencia a la abrasión. El guante es "
     "<b>lavable</b>.", EVF),
    ("Cut resistant level <b>ANSI A3 minimum</b>",
     "Nivel de resistencia al corte <b>ANSI A3</b> declarado por el fabricante, que satisface el "
     "mínimo exigido. Nivel de abrasión 2.", EVC),
    ("<b>Knit wrist cuff</b>",
     "<b>Puño tejido</b> (knit wrist) que ajusta a la muñeca e impide el ingreso de partículas.", EVF),
    ("<b>Men size: 10 X-Large</b> as required, shall be as <b>ISO 21420</b>",
     "Se oferta la <b>talla 10</b>, equivalente a <b>X-Large</b> en la escala dimensional de "
     "<b>ISO 21420</b>. Se entrega muestra para su verificación dimensional.", EVD),
    ("<b>100 percent Kevlar only by DuPont</b>",
     "Concha de <b>100% Kevlar&reg; de DuPont&trade;</b>, calibre 7, tejido de peso regular. "
     "El fabricante está <b>certificado por DuPont&reg; como fabricante licenciado de guantes</b>, "
     "lo que acredita el origen de la fibra. No se emplea aramida de otro fabricante ni mezcla "
     "con fibras sintéticas.", EVC),
    ("Gloves shall have <b>DuPont Kevlar label</b>",
     "Cada par lleva la <b>etiqueta DuPont&trade; Kevlar&reg;</b> del fabricante licenciado.", EVM),
    ("<b>Product references: MCR Safety CutPro 9366</b>",
     "<b>Se oferta exactamente el producto de referencia de la Autoridad</b>: MCR Safety "
     "CutPro&reg; 9366. Esta declaración se hace expresamente en la propuesta técnica cargada en "
     "el SLI, conforme lo exige el numeral 9.1.1.", EVD),
    ("<b>Sample shall be provided</b> for measurement as to verify compliance with ISO 21420",
     "Se entrega <b>muestra física</b> del artículo ofertado en Balboa, Ancón, Edificio 710, "
     "planta baja, identificada con el nombre del proponente, el número de pliego 215088 y el "
     "número de propuesta, antes de la fecha y hora de cierre.", EVD),
    ("Manufacturer&#39;s descriptive <b>literature and image</b> are required with bid",
     "Se adjuntan la <b>literatura descriptiva del fabricante</b> y la <b>imagen del producto "
     "ofertado</b>, identificadas con el renglón al que aplican.", EVI),
  ],
  "nota": "<b>Presentación:</b> caja de 12 pares (una docena), presentación estándar del fabricante "
          "para esta referencia.<br/><br/>"
          "<b>Declaración del numeral 9.1.1:</b> al ofertarse la marca y el modelo de referencia "
          "especificados por la Autoridad, el proponente deja constancia expresa de ello en esta "
          "propuesta técnica cargada en el SLI. Se adjunta igualmente la matriz de cumplimiento, "
          "la literatura del fabricante y la imagen del producto, y <b>se entrega la muestra "
          "física</b>, ya que el numeral 9.2 de este pliego exige la muestra sin excepción.",
 },
 {
  "n": "4", "item": "PPE-GLO-00022",
  "título": "PROPUESTA TÉCNICA &mdash; Guante de examen de nitrilo, mediano",
  "archivo": "04-RENGLON-4-PPE-GLO-00022.pdf",
  "prod": {"marca": "MCR Safety", "modelo": "Guante desechable de nitrilo 6008",
           "pn": "6008 talla mediana (M)", "cant": "1,000", "um": "Box (caja)",
           "ref_acp": "La descripción del renglón no indica producto de referencia ACP. Se oferta "
                      "producto que cumple con la descripción."},
  "matriz": [
    ("<b>Gloves, examination (exam) grade</b>",
     "El producto está certificado bajo la serie <b>EN 455</b>, que es la norma europea específica "
     "de <b>guantes médicos de un solo uso</b>: <b>EN 455-1:2000</b> (ausencia de agujeros), "
     "<b>EN 455-2:2015</b> (propiedades físicas) y <b>EN 455-3:2015</b> (evaluación biológica). "
     "Además cumple <b>ASTM D6319:2015</b>, que es precisamente la <i>especificación normalizada "
     "para guantes de examen de nitrilo para aplicación médica</i>. Ambas acreditan la condición "
     "de <b>grado examen</b>.", EVC),
    ("<b>Nitrile</b>",
     "Guante de <b>nitrilo</b> azul, <b>sin polvo</b>, espesor <b>8 mil</b> y longitud de "
     "<b>9,5 pulgadas</b> (24,13 cm), ambidiestro, con puño enrollado y acabado sin talco.", EVF),
    ("<b>Medium</b>",
     "Se oferta la <b>talla mediana (M)</b>.", EVD),
    ("<b>Presentation in box of 50 to 100</b>",
     "Se suministra en <b>caja dispensadora de 50 unidades</b>, conteo que queda dentro del "
     "rango de 50 a 100 unidades por caja exigido por el renglón. La caja máster agrupa 10 "
     "dispensadoras, 500 unidades en total.", EVF),
    ("Documentación exigida por el numeral 9.1",
     "Se adjuntan la ficha técnica del fabricante con las características resaltadas, la "
     "<b>imagen del producto</b> y la <b>marcación de la caja</b>, donde constan la referencia, "
     "la talla, el conteo y el marcado de certificación.", EVI),
  ],
  "nota": "<b>Prestaciones adicionales del producto ofertado</b>: además de la condición de grado "
          "examen, el guante está certificado como equipo de protección individual bajo el "
          "<b>Reglamento (UE) 2016/425</b> y cumple <b>EN ISO 374-1:2016</b> (riesgo químico) y "
          "<b>EN ISO 374-5:2016</b> (riesgo por microorganismos). Los materiales de sus componentes "
          "<b>cumplen las reglamentaciones federales para el contacto con alimentos</b>.<br/><br/>"
          "Es decir, el producto ofertado sirve a la vez como guante de examen y como barrera "
          "química y biológica, cosa que un guante de examen corriente no acredita.",
 },
 {
  "n": "5", "item": "PPE-GLO-00031",
  "título": "PROPUESTA TÉCNICA &mdash; Guante anticorte, talla 9",
  "archivo": "05-RENGLON-5-PPE-GLO-00031.pdf",
  "prod": {"marca": "MCR Safety", "modelo": "CutPro&reg; serie 92754BP",
           "pn": "92754BPL (talla 9 / Large)", "cant": "5,000", "um": "Each (par)",
           "ref_acp": "La descripción del renglón no indica producto de referencia ACP. Se oferta "
                      "producto que cumple con la descripción."},
  "matriz": [
    ("<b>Gloves, cut resistant</b>",
     "Guante anticorte con concha tejida de <b>HPPE HyperMax&reg;</b> de <b>calibre 13</b>, sin "
     "costuras, con palma y yemas recubiertas de <b>bi-polímero</b>.", EVF),
    ("Against <b>abrasion, cuts, tear and puncture</b>",
     "El producto declara desempeño en los cuatro riesgos citados: el tejido HPPE aporta la "
     "resistencia al <b>corte</b> y al <b>desgarro</b>, y el recubrimiento bi-polímero de palma y "
     "yemas aporta la resistencia a la <b>abrasión</b> y a la <b>punción</b>.", EVF),
    ("<b>EN 388:2016 &quot;4-X-4-2-C&quot; or ANSI cut level A4</b>",
     "Se acredita por la <b>segunda de las dos alternativas</b> que admite el renglón: el nivel "
     "de corte <b>ANSI/ISEA 105</b>. El fabricante publica para esta referencia corte <b>A5</b>, "
     "punción <b>3</b> y abrasión <b>6</b>. El nivel de corte <b>A5 supera el A4</b> exigido "
     "como mínimo por el renglón.", EVC),
    ("<b>Size 9 (Large)</b>",
     "Se oferta la <b>talla 9</b>, equivalente a <b>Large</b> en la escala dimensional de "
     "<b>ISO 21420</b>. La serie se fabrica de XS a 2XL.", EVD),
    ("Documentación exigida por el numeral 9.1",
     "Se adjuntan la ficha técnica del fabricante con los niveles de desempeño resaltados, la "
     "<b>imagen del producto</b> y la <b>marcación</b> impresa en el dorso del guante, donde "
     "constan la referencia, la talla y los pictogramas de certificación.", EVI),
  ],
  "nota": "<b>Prestaciones adicionales del producto ofertado</b>: <b>refuerzo entre el pulgar y el "
          "índice</b>, que es donde primero se rompe un guante anticorte y por tanto alarga la vida "
          "útil del lote; y <b>palma compatible con pantalla táctil</b>, que evita que el operario "
          "se quite el guante para usar un dispositivo.<br/><br/>"
          "<b>Presentación:</b> empaque interior de 12 docenas en bolsa de polietileno, caja de "
          "144 pares.<br/><br/>"
          "El renglón admite acreditar el desempeño por el código EN 388:2016 <b>o</b> por el "
          "nivel de corte ANSI. La presente propuesta se acoge a la segunda alternativa, que es "
          "la que el fabricante declara para esta referencia.",
 },
 {
  "n": "6", "item": "PPE-GLO-00033",
  "título": "PROPUESTA TÉCNICA &mdash; Guante tejido con palma de poliuretano, talla 11",
  "archivo": "06-RENGLON-6-PPE-GLO-00033.pdf",
  "prod": {"marca": "MCR Safety", "modelo": "CutPro&reg; serie 92852PU",
           "pn": "92852PUXXL (talla 11 / 2X-Large)", "cant": "900", "um": "Each (par)",
           "ref_acp": "La descripción del renglón no indica producto de referencia ACP. Se oferta "
                      "producto que cumple con la descripción."},
  "matriz": [
    ("<b>Gloves, synthetic knit</b>",
     "Guante <b>tejido sin costuras</b> con concha de <b>HPPE sintético</b> gris de "
     "<b>calibre 13</b>. Composición: HPPE, acero, poliéster, spandex y poliuretano.", EVF),
    ("With <b>PU covered palm and fingertips</b>",
     "Recubrimiento de <b>poliuretano (PU) en la palma y en los dedos</b>, aplicado para mejorar "
     "el agarre y la durabilidad del guante.", EVF),
    ("<b>Industrial</b>",
     "Guante de uso industrial, lavable y de fabricación ecológica. El fabricante declara "
     "<b>ANSI/ISEA 105: corte A4, abrasión 5, punción 3</b>, y <b>EN 388:2016: abrasión 4, "
     "corte 5, desgarro 4, punción 2, corte TDM D</b>. Son prestaciones por encima de lo que "
     "el renglón exige, que no pide nivel de corte.", EVC),
    ("<b>Size 11 (2X-Large)</b>",
     "Se oferta la <b>talla 11</b>, equivalente a <b>2X-Large</b> en la escala dimensional de "
     "<b>ISO 21420</b>. La disponibilidad del modelo en esta talla y sus niveles de desempeño "
     "están confirmados por el fabricante mediante la comunicación que se adjunta.", EVM),
    ("Documentación exigida por el numeral 9.1",
     "Se adjuntan la ficha técnica del fabricante con las características resaltadas, la "
     "<b>imagen del producto</b> y la <b>marcación</b> impresa en el guante.", EVI),
  ],
  "nota": "<b>Prestación adicional del producto ofertado</b>: el renglón pide un guante tejido "
          "sintético con palma de poliuretano, sin exigir nivel de corte. El producto ofertado "
          "pertenece a la línea <b>CutPro&reg;</b>, de modo que además del agarre entrega "
          "<b>resistencia al corte</b> sin costo adicional para la Autoridad.<br/><br/>"
          "<b>Presentación:</b> bolsa interior de 12 pares, caja de 144 pares.<br/><br/>"
"",
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

def revisar(rutas):
    """Avisa de cualquier campo sin llenar antes de subir al SLI."""
    import re
    from pypdf import PdfReader
    sucios = []
    for ruta in rutas:
        texto = " ".join((pg.extract_text() or "") for pg in PdfReader(ruta).pages)
        texto = re.sub(r"\s+", " ", texto)
        for hueco in dict.fromkeys(re.findall(r"«([^»]*)»", texto)):
            sucios.append((os.path.basename(ruta), hueco.strip()))
    if sucios:
        print("\n!!  NO SUBIR AL SLI TODAVÍA: hay campos sin llenar")
        for archivo, hueco in sucios:
            print("    %-42s «%s»" % (archivo, hueco[:70]))
    else:
        print("\nOK: ningún campo pendiente. Los PDF están listos para el SLI.")
    return not sucios

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    # La carta de presentación se mantiene solo en Word (word/CARTA-PRESENTACION-215088.docx)
    # para que no circulen dos versiones distintas del mismo documento.
    generados = [doc_renglon(r) for r in RENGLONES]
    for g in generados:
        print(g)
    revisar(generados)
