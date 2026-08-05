# ================================================================
# FICHAS DE HISTORIA — CEPRU UNSAAC
# Basado en el material oficial «Historia del Perú en el proceso
# mundial», Área D, Ciclo Primera Oportunidad.
# ================================================================
"""Genera dos productos por cada balota del temario:

1. FICHA DE TEXTO PARA COMPLETAR, a dos columnas, con cuadros y
   espacios en blanco. El estudiante la llena mientras el docente
   explica: escribir la palabra clave fija más que subrayar un texto
   ya impreso.

2. BANCO DE 20 PREGUNTAS con cinco alternativas, en el formato del
   examen de admisión.

Cada contenido se escribe UNA sola vez, con las respuestas entre
llaves: "El padre de la historia es {Heródoto}". De ahí salen la
versión del alumno (con líneas) y la del docente (con las claves
resaltadas), sin riesgo de que se desincronicen.

Integración en sistema_web.py:
    from fichas_historia import tab_fichas_historia
"""

import io
import re
from datetime import datetime

import streamlit as st

ENCABEZADO_L1 = "I.E.P. YACHAY  ·  ACADEMIA YACHAY"
ENCABEZADO_L2 = "PIONEROS EN LA EDUCACIÓN DE CALIDAD"
def pie_legal(area, profesor="Prof. Alexander Córdova"):
    return (f"Derechos reservados — ACADEMIA YACHAY · Área: {area} · "
            f"{profesor} · "
            f"Uso exclusivo de estudiantes y docentes de la academia")


# Los logos van en la misma carpeta del repositorio que este archivo,
# junto a sistema_web.py y google_sync.py.
LOGO_PATH = "logo_academia.png"
LOGO_MARCA_AGUA = "logo_academia_marca_agua.png"

_PATRON = re.compile(r"\{([^}]+)\}")


def _partes(texto):
    """Divide un texto en fragmentos fijos y respuestas."""
    salida, pos = [], 0
    for m in _PATRON.finditer(texto):
        if m.start() > pos:
            salida.append(("fijo", texto[pos:m.start()]))
        salida.append(("resp", m.group(1)))
        pos = m.end()
    if pos < len(texto):
        salida.append(("fijo", texto[pos:]))
    return salida


def render_linea(texto, con_claves):
    """Devuelve el texto listo para el PDF.

    con_claves=False -> espacios en blanco proporcionales a la palabra
    con_claves=True  -> respuesta en negrita y color, para el docente
    """
    fuera = []
    for tipo, val in _partes(texto):
        if tipo == "fijo":
            fuera.append(val)
        elif con_claves:
            fuera.append(f'<b><font color="#B01C22">{val}</font></b>')
        else:
            # Longitud proporcional para que la línea invite a escribir
            # la palabra correcta y no cualquier cosa.
            n = max(6, min(int(len(val) * 1.5), 34))
            fuera.append(f'<font color="#94A3B8">{"_" * n}</font>')
    return "".join(fuera)


def contar_espacios(tema):
    n = 0
    for sec in tema.get("secciones", []):
        for it in sec.get("items", []):
            n += len(_PATRON.findall(it))
    for cu in tema.get("cuadros", []):
        for fila in cu.get("filas", []):
            for celda in fila:
                n += len(_PATRON.findall(celda))
    return n


# ================================================================
# GENERACIÓN DE LA FICHA DE TEXTO (DOS COLUMNAS)
# ================================================================

def _estilos():
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    from reportlab.lib import colors
    ss = getSampleStyleSheet()
    return {
        "marca": ParagraphStyle("m", parent=ss["Title"], fontSize=13,
                                textColor=colors.HexColor("#12307F"),
                                alignment=TA_CENTER, spaceAfter=0, leading=15),
        "lema": ParagraphStyle("l", parent=ss["Normal"], fontSize=7,
                               textColor=colors.HexColor("#B45309"),
                               alignment=TA_CENTER, spaceAfter=6),
        "titulo": ParagraphStyle("t", parent=ss["Title"], fontSize=13,
                                 textColor=colors.HexColor("#12307F"),
                                 alignment=TA_CENTER, spaceAfter=2,
                                 spaceBefore=2),
        "banda": ParagraphStyle("bn", parent=ss["Normal"], fontSize=11.5,
                                textColor=colors.white, leading=14,
                                alignment=TA_CENTER),
        "sub2": ParagraphStyle("s2", parent=ss["Normal"], fontSize=7.6,
                               textColor=colors.HexColor("#334155"),
                               alignment=TA_CENTER, leading=10),
        "sub": ParagraphStyle("s", parent=ss["Normal"], fontSize=8,
                              textColor=colors.HexColor("#4B5563"),
                              alignment=TA_CENTER, spaceAfter=8),
        "h": ParagraphStyle("h", parent=ss["Normal"], fontSize=9,
                            textColor=colors.white, spaceAfter=2,
                            spaceBefore=0, leading=11),
        "n": ParagraphStyle("n", parent=ss["Normal"], fontSize=9.6,
                            leading=17.5, alignment=TA_JUSTIFY, spaceAfter=5),
        "cel": ParagraphStyle("c", parent=ss["Normal"], fontSize=8.6,
                              leading=13),
        "preg": ParagraphStyle("p", parent=ss["Normal"], fontSize=8.6,
                               leading=12, spaceAfter=1),
        "alt": ParagraphStyle("a", parent=ss["Normal"], fontSize=8.2,
                              leading=11, leftIndent=14),
    }


def _banda_titulo(story, tema, subtitulo, est, ancho, con_claves=False):
    """Cabecera institucional: logo a un costado, marca y banda de color."""
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image as RLImage
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    import os

    _marca = [Paragraph(ENCABEZADO_L1, est["marca"]),
              Paragraph(ENCABEZADO_L2, est["lema"])]
    if os.path.exists(LOGO_PATH):
        try:
            _logo = RLImage(LOGO_PATH, width=1.55 * cm, height=1.55 * cm)
            _cab = Table([[_logo, _marca]], colWidths=[1.75 * cm, ancho - 1.75 * cm])
            _cab.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (0, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]))
            story.append(_cab)
        except Exception:
            story.extend(_marca)
    else:
        story.extend(_marca)

    acento = colors.HexColor("#B01C22" if con_claves else "#12307F")
    banda = Table([[Paragraph(
        f'<font color="#FFFFFF"><b>BALOTA {tema["num"]} · '
        f'{str(tema["titulo"]).upper()}</b></font>', est["banda"])]],
        colWidths=[ancho])
    banda.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), acento),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    story.append(banda)
    story.append(Spacer(1, 2))
    sub = Table([[Paragraph(subtitulo, est["sub2"])]], colWidths=[ancho])
    sub.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EEF2FA")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -1), 1.2, acento),
    ]))
    story.append(sub)
    story.append(Spacer(1, 6))


def _pie(canvas, doc):
    from reportlab.lib.units import cm
    import os
    area = getattr(doc, "area_actual", "Historia")
    profesor = getattr(doc, "profesor_actual", "Prof. Alexander Córdova")
    canvas.saveState()

    # Marca de agua tenue centrada en la hoja
    if os.path.exists(LOGO_MARCA_AGUA):
        try:
            lado = 11 * cm
            canvas.drawImage(
                LOGO_MARCA_AGUA,
                (doc.pagesize[0] - lado) / 2, (doc.pagesize[1] - lado) / 2,
                width=lado, height=lado, mask="auto",
                preserveAspectRatio=True)
        except Exception:
            pass

    canvas.setFont("Helvetica", 6)
    canvas.setFillColorRGB(0.42, 0.45, 0.50)
    canvas.drawCentredString(doc.pagesize[0] / 2, 0.7 * cm, pie_legal(area, profesor))
    canvas.drawRightString(doc.pagesize[0] - 1.2 * cm, 0.7 * cm,
                           f"Pág. {canvas.getPageNumber()}")
    canvas.setStrokeColorRGB(0.80, 0.83, 0.87)
    canvas.setLineWidth(0.4)
    canvas.line(1.2 * cm, 0.95 * cm, doc.pagesize[0] - 1.2 * cm, 0.95 * cm)
    canvas.restoreState()


def generar_ficha_texto(tema, con_claves=False, grado_txt="",
                        institucion="ACADEMIA YACHAY", area="Historia",
                        profesor="Prof. Alexander Córdova"):
    """Ficha de estudio a dos columnas con espacios para completar."""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                    Paragraph, Spacer, Table, TableStyle,
                                    NextPageTemplate)
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    est = _estilos()
    buf = io.BytesIO()

    MX, MY = 1.2 * cm, 1.3 * cm
    ancho_util = A4[0] - 2 * MX
    col_w = (ancho_util - 0.6 * cm) / 2

    doc = BaseDocTemplate(buf, pagesize=A4,
                          leftMargin=MX, rightMargin=MX,
                          topMargin=MY, bottomMargin=1.4 * cm)

    # Primera página: encabezado ancho arriba y dos columnas debajo
    alto_enc = 4.3 * cm
    f_enc = Frame(MX, A4[1] - MY - alto_enc, ancho_util, alto_enc, id="enc",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    alto_col1 = A4[1] - MY - alto_enc - 1.4 * cm
    f_c1 = Frame(MX, 1.4 * cm, col_w, alto_col1, id="c1",
                 leftPadding=0, rightPadding=6, topPadding=0, bottomPadding=0)
    f_c2 = Frame(MX + col_w + 0.6 * cm, 1.4 * cm, col_w, alto_col1, id="c2",
                 leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0)
    alto_full = A4[1] - MY - 1.4 * cm
    g_c1 = Frame(MX, 1.4 * cm, col_w, alto_full, id="g1",
                 leftPadding=0, rightPadding=6, topPadding=0, bottomPadding=0)
    g_c2 = Frame(MX + col_w + 0.6 * cm, 1.4 * cm, col_w, alto_full, id="g2",
                 leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0)

    doc.area_actual = area
    doc.profesor_actual = profesor
    doc.addPageTemplates([
        PageTemplate(id="primera", frames=[f_enc, f_c1, f_c2], onPage=_pie),
        PageTemplate(id="resto", frames=[g_c1, g_c2], onPage=_pie),
    ])

    st_ = []
    _banda_titulo(st_, tema,
                  "HISTORIA · Temario CEPRU-UNSAAC · " +
                  ("CLAVES PARA EL DOCENTE" if con_claves
                   else "Ficha de estudio para completar"),
                  est, ancho_util, con_claves)

    if not con_claves:
        datos = Table([[
            "Apellidos y Nombres: ___________________________________",
            f"Grupo: {grado_txt or '________'}",
            "Fecha: ____/____/______",
        ]], colWidths=[10.2 * cm, 3.6 * cm, 4.4 * cm])
        datos.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW", (0, 0), (-1, -1), 1, colors.HexColor("#12307F")),
        ]))
        st_.append(datos)
    else:
        st_.append(Table([[""]], colWidths=[ancho_util], rowHeights=[2],
                         style=[("LINEBELOW", (0, 0), (-1, -1), 1,
                                 colors.HexColor("#B01C22"))]))

    st_.append(NextPageTemplate("resto"))
    st_.append(Spacer(1, 1))

    def barra(txt):
        t = Table([[Paragraph(f"<b>{txt}</b>", est["h"])]],
                  colWidths=[col_w - 6])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#12307F")),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        return t

    for sec in tema.get("secciones", []):
        st_.append(Spacer(1, 5))
        st_.append(barra(sec["titulo"]))
        st_.append(Spacer(1, 3))
        for it in sec["items"]:
            st_.append(Paragraph("• " + render_linea(it, con_claves), est["n"]))

    for cu in tema.get("cuadros", []):
        st_.append(Spacer(1, 6))
        st_.append(barra(cu["titulo"]))
        st_.append(Spacer(1, 3))
        ncol = len(cu["encabezados"])
        cw = [(col_w - 8) / ncol] * ncol
        data = [[Paragraph(f"<b>{h}</b>", est["cel"]) for h in cu["encabezados"]]]
        for fila in cu["filas"]:
            data.append([Paragraph(render_linea(c, con_claves), est["cel"])
                         for c in fila])
        t = Table(data, colWidths=cw, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDE4F0")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#8894A8")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#F5F7FB")]),
        ]))
        st_.append(t)

    doc.build(st_)
    buf.seek(0)
    return buf.getvalue()


# ================================================================
# BANCO DE PREGUNTAS
# ================================================================

LETRAS = ["A", "B", "C", "D", "E"]


def balancear(preguntas, semilla=7):
    """Reparte la respuesta correcta entre las cinco letras.

    Al redactar preguntas es natural poner la correcta en la segunda
    posición una y otra vez. Sin este reparto, un postulante que marque
    siempre la misma letra aprueba sin saber nada, y el banco deja de
    medir. Rota las alternativas de cada pregunta hasta que la correcta
    caiga en la letra que toca por turno.
    """
    salida = []
    for i, p in enumerate(preguntas):
        alts = list(p["alternativas"])
        idx_ok = LETRAS.index(p["correcta"])
        correcta_txt = alts[idx_ok]
        destino = (i + semilla) % 5
        # La última alternativa suele ser un cierre tipo "N.A." o una
        # síntesis; si lo es, se respeta su posición final.
        fija_final = str(alts[-1]).lower().startswith(
            ("ninguna", "todas", "n.a", "t.a"))
        cuerpo = alts[:-1] if fija_final else alts
        if correcta_txt in cuerpo:
            cuerpo = [a for a in cuerpo if a != correcta_txt]
            destino = min(destino, len(cuerpo))
            cuerpo.insert(destino, correcta_txt)
            alts = cuerpo + ([alts[-1]] if fija_final else [])
        salida.append({**p, "alternativas": alts,
                       "correcta": LETRAS[alts.index(correcta_txt)]})
    return salida


def generar_qr_claves(tema, area, profesor):
    """QR con las claves del examen codificadas como texto plano.

    No apunta a ningún servidor: el propio código contiene el texto.
    Cualquier lector de QR del celular lo muestra de inmediato, sin
    internet ni nada externo, incluso años después de impreso.

    El contenido va sin tildes: muchos lectores de QR de celular no
    respetan la codificación UTF-8 y muestran caracteres corruptos
    («Perú» sale como «Per??»). Quitar los acentos es más legible que
    arriesgarse a que se vea mal en algún teléfono.
    """
    import qrcode
    import unicodedata

    def sin_tildes(s):
        return ''.join(c for c in unicodedata.normalize('NFD', str(s))
                       if unicodedata.category(c) != 'Mn')

    claves = " ".join(
        f"{i}-{p['correcta']}"
        for i, p in enumerate(tema.get("preguntas", []), start=1))
    contenido = sin_tildes(
        f"ACADEMIA YACHAY - PIONEROS EN LA EDUCACION DE CALIDAD\n"
        f"{area} - Balota {tema['num']}: {tema['titulo']}\n"
        f"{profesor}\n"
        f"CLAVES: {claves}"
    )
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=10, border=2)
    qr.add_data(contenido)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#12307F", back_color="white")
    buf_qr = io.BytesIO()
    img.save(buf_qr, format="PNG")
    buf_qr.seek(0)
    return buf_qr


def generar_banco_preguntas(tema, con_claves=False, grado_txt="",
                            institucion="ACADEMIA YACHAY", area="Historia",
                            profesor="Prof. Alexander Córdova"):
    """20 preguntas con cinco alternativas, impresas a DOS COLUMNAS.

    A una columna, un banco de 20 preguntas ocupaba tres hojas. A dos
    columnas entra en una o dos: con 380 preguntas en el temario, eso es
    la diferencia entre un taco de papel y un cuadernillo manejable.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                    Paragraph, Spacer, Table, TableStyle,
                                    NextPageTemplate)
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    est = _estilos()
    buf = io.BytesIO()

    MX, MY = 1.3 * cm, 1.3 * cm
    ancho_util = A4[0] - 2 * MX
    col_w = (ancho_util - 0.7 * cm) / 2

    doc = BaseDocTemplate(buf, pagesize=A4, leftMargin=MX, rightMargin=MX,
                          topMargin=MY, bottomMargin=1.4 * cm)

    alto_enc = 4.4 * cm if not con_claves else 3.3 * cm
    f_enc = Frame(MX, A4[1] - MY - alto_enc, ancho_util, alto_enc, id="e",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    alto1 = A4[1] - MY - alto_enc - 1.4 * cm
    f1 = Frame(MX, 1.4 * cm, col_w, alto1, id="a", leftPadding=0,
               rightPadding=8, topPadding=0, bottomPadding=0)
    f2 = Frame(MX + col_w + 0.7 * cm, 1.4 * cm, col_w, alto1, id="b",
               leftPadding=8, rightPadding=0, topPadding=0, bottomPadding=0)
    altoF = A4[1] - MY - 1.4 * cm
    g1 = Frame(MX, 1.4 * cm, col_w, altoF, id="c", leftPadding=0,
               rightPadding=8, topPadding=0, bottomPadding=0)
    g2 = Frame(MX + col_w + 0.7 * cm, 1.4 * cm, col_w, altoF, id="d",
               leftPadding=8, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.area_actual = area
    doc.profesor_actual = profesor
    doc.addPageTemplates([
        PageTemplate(id="p1", frames=[f_enc, f1, f2], onPage=_pie),
        PageTemplate(id="pn", frames=[g1, g2], onPage=_pie)])

    story = []
    _banda_titulo(story, tema,
                  "BANCO DE 20 PREGUNTAS · cinco alternativas · formato "
                  "admisión UNSAAC" + ("  ·  CON CLAVES" if con_claves else ""),
                  est, ancho_util, con_claves)

    if not con_claves:
        datos = Table([[
            "Apellidos y Nombres: ___________________________________",
            f"Grupo: {grado_txt or '________'}",
            "Nota: ______",
        ]], colWidths=[10.4 * cm, 4.0 * cm, 3.6 * cm])
        datos.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LINEBELOW", (0, 0), (-1, -1), 0.8, colors.HexColor("#8894A8")),
        ]))
        story.append(datos)

    story.append(NextPageTemplate("pn"))
    story.append(Spacer(1, 1))

    for i, p in enumerate(tema.get("preguntas", []), start=1):
        story.append(Paragraph(f"<b>{i}.</b> {p['pregunta']}", est["preg"]))
        for k2, alt in enumerate(p["alternativas"]):
            es_ok = con_claves and LETRAS[k2] == p["correcta"]
            color = "#B01C22" if es_ok else "#0F1115"
            neg = "<b>" if es_ok else ""
            cie = "</b>" if es_ok else ""
            story.append(Paragraph(
                f'<font color="{color}">{neg}{LETRAS[k2]}) {alt}{cie}</font>',
                est["alt"]))
        story.append(Spacer(1, 4))

    if not con_claves:
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>HOJA DE RESPUESTAS</b>", est["preg"]))
        story.append(Spacer(1, 3))
        estilo_t = TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#8894A8")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#DDE4F0")),
            ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
        n_pre = len(tema.get("preguntas", []))
        for ini in range(1, n_pre + 1, 5):
            fin = min(ini + 4, n_pre)
            t = Table([["N°"] + [str(x) for x in range(ini, fin + 1)],
                       ["Rpta."] + [""] * (fin - ini + 1)],
                      colWidths=[1.3 * cm] +
                                [(col_w - 1.3 * cm - 10) / (fin - ini + 1)] * (fin - ini + 1),
                      rowHeights=[0.5 * cm, 0.75 * cm])
            t.setStyle(estilo_t)
            story.append(t)
            story.append(Spacer(1, 3))

        # QR con las claves, solo en la version del alumno: no aparece
        # en la version del docente porque ahi las claves ya estan
        # impresas en rojo, y duplicarlas en un QR seria redundante.
        try:
            from reportlab.platypus import Image as RLImage
            qr_buf = generar_qr_claves(tema, area, profesor)
            story.append(Spacer(1, 6))
            qr_tabla = Table([[
                RLImage(qr_buf, width=2.1 * cm, height=2.1 * cm),
                Paragraph(
                    "<b>Escanea para ver las claves</b><br/>"
                    "(revisa tu examen en casa)<br/>"
                    "<font size=6.5 color='#64748B'>ACADEMIA YACHAY · "
                    "PIONEROS EN LA EDUCACIÓN DE CALIDAD<br/>"
                    f"{profesor}</font>", est["cel"]),
            ]], colWidths=[2.3 * cm, col_w - 2.3 * cm])
            qr_tabla.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ]))
            story.append(qr_tabla)
        except Exception:
            pass
    else:
        story.append(Spacer(1, 6))
        claves = " · ".join(
            f"{i}-{p['correcta']}"
            for i, p in enumerate(tema.get("preguntas", []), start=1))
        story.append(Paragraph(f"<b>CLAVES:</b> {claves}", est["preg"]))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()


# ================================================================
# CONTENIDO: LAS 19 BALOTAS
# ================================================================

BALOTAS = [{'num': 1,
  'titulo': 'Ciencia histórica',
  'secciones': [{'titulo': '1.1 CONCEPTO',
                 'items': ['La historia como {ciencia} estudia en forma '
                           'sistemática, verídica y metódica los hechos y '
                           'procesos sociales del {pasado}, a través del '
                           'análisis e interpretación de diversos tipos de '
                           '{fuentes}.',
                           'Estudia los hechos en función de sus {causas} y '
                           '{consecuencias}, con el propósito de comprender '
                           'el {presente} y proyectarse al {futuro}.',
                           'La historia como {hecho} se refiere a todos los '
                           'acontecimientos y procesos sociales del pasado, '
                           'desde el origen de la humanidad hasta la '
                           'actualidad.']},
                {'titulo': '1.2 COMPONENTES DE LA HISTORIA',
                 'items': ['{Heródoto}, padre de la historia, decía que los '
                           'dos ojos de la historia son el {tiempo} y el '
                           '{espacio}.',
                           'La {Sociedad}: comprende a hombres y mujeres '
                           'como actores de la historia.',
                           'El {Tiempo}: cronología absoluta o relativa, y '
                           'dimensiones de corta, mediana y larga '
                           '{duración}.',
                           'El {Espacio}: área geográfica local, regional, '
                           'nacional, continental o mundial que sirve de '
                           'escenario.']},
                {'titulo': '1.3 LA HISTORIA COMO PATRIMONIO',
                 'items': ['Patrimonio histórico es todo el {legado} social '
                           'y cultural dejado por nuestros ancestros a lo '
                           'largo del proceso histórico peruano.',
                           'Comprende la cultura {material} (restos '
                           'arqueológicos, patrimonio natural, legado '
                           'artístico) y la cultura {inmaterial} (folclore, '
                           'tradición, cultura viva).',
                           'La institución encargada de su preservación es '
                           'el Ministerio de {Cultura}.',
                           'La {Biblioteca} Nacional del Perú custodia el '
                           'fondo bibliográfico y el {Archivo} General de la '
                           'Nación el fondo documental.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La historia como ciencia estudia los hechos y '
                           'procesos sociales del pasado en función de sus '
                           '{Causas y consecuencias}.',
                           'Según Heródoto, los dos ojos de la historia son '
                           '{El tiempo y el espacio}.',
                           'Los topónimos, las leyendas y los cantos '
                           'corresponden a fuentes {Orales o tradicionales}.',
                           'Las momias, los cabellos y los huesos son '
                           'fuentes {Antroposomáticas}.',
                           'Los llamados «vladivideos» y «petroaudios» '
                           'constituyen fuentes {Audiovisuales}.',
                           'La institución encargada de la preservación del '
                           'patrimonio cultural peruano es {El Ministerio de '
                           'Cultura}.',
                           'El fondo documental del Estado peruano es '
                           'custodiado por {El Archivo General de la '
                           'Nación}.',
                           'Las crónicas y los manuscritos coloniales son '
                           'fuentes {Escritas}.',
                           'El propósito final del estudio de la historia, '
                           'según el texto, es {Comprender el presente y '
                           'proyectarse al futuro}.',
                           'Las construcciones arquitectónicas, la cerámica '
                           'y los textiles corresponden a fuentes '
                           '{Materiales o monumentales}.',
                           'La dimensión temporal de larga duración se '
                           'refiere a {Procesos que abarcan siglos}.',
                           'El Archivo Regional del Cusco (A.R.C.) es una '
                           'institución de {Investigación y difusión del '
                           'patrimonio cultural}.',
                           'La obligación de cuidar y conservar el '
                           'patrimonio cultural corresponde a {El Estado y '
                           'la comunidad nacional}.',
                           'Los idiomas y las creencias transmitidas de '
                           'padres a hijos son fuentes {Orales}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El folclore, la tradición y la cultura viva de '
                           'los pueblos forman parte de la cultura '
                           '{Inmaterial}.',
                           'La historia «como hecho» se refiere a {Los '
                           'acontecimientos y procesos sociales del pasado}.',
                           'El estudio sistemático, verídico y metódico '
                           'corresponde a la historia entendida como '
                           '{Ciencia}.',
                           'El espacio como componente histórico puede ser '
                           '{Local, regional, nacional, continental o '
                           'mundial}.',
                           'Señale la afirmación CORRECTA sobre las fuentes '
                           'históricas {Son restos, huellas y testimonios '
                           'materiales e inmateriales}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['El concepto formal de fuente histórica abarca '
                           'todos los {restos}, huellas y testimonios, '
                           'materiales e inmateriales, dejados por los '
                           'pueblos a lo largo de su desarrollo.',
                           'Entre las fuentes materiales se cuentan las '
                           'construcciones arquitectónicas, la cerámica, los '
                           'textiles, las tumbas, las esculturas, las '
                           '{pinturas} y las herramientas.',
                           'El Ministerio de Cultura cuenta con '
                           'instituciones {desconcentradas} en todas las '
                           'regiones del país para la preservación del '
                           'patrimonio.',
                           'Las fuentes escritas, también llamadas '
                           'documentales, incluyen testimonios dejados en '
                           'piedra, ladrillos, papiros, tablillas y '
                           '{metales}.']}],
  'cuadros': [{'titulo': '1.4 CLASIFICACIÓN DE LAS FUENTES',
               'encabezados': ['Tipo de fuente', 'Ejemplos'],
               'filas': [['Materiales o {monumentales}',
                          'Cerámica, textiles, tumbas, esculturas, armas'],
                         ['{Orales} o tradicionales',
                          '{Topónimos}, idiomas, leyendas, mitos, cantos'],
                         ['{Escritas} o documentales',
                          'Manuscritos, {crónicas}, libros, tablillas'],
                         ['{Antroposomáticas}',
                          'Cabellos, uñas, huesos, {momias}'],
                         ['{Audiovisuales}',
                          'Audios, videos, fotografías, «{vladivideos}»']]}],
  'preguntas': [{'pregunta': 'La historia como ciencia estudia los hechos y '
                             'procesos sociales del pasado en función de '
                             'sus:',
                 'alternativas': ['Fechas y personajes',
                                  'Causas y consecuencias',
                                  'Mitos y leyendas',
                                  'Fuentes escritas únicamente',
                                  'Restos arqueológicos'],
                 'correcta': 'B'},
                {'pregunta': 'Según Heródoto, los dos ojos de la historia '
                             'son:',
                 'alternativas': ['La sociedad y la cultura',
                                  'El mito y la razón',
                                  'El tiempo y el espacio',
                                  'La causa y el efecto',
                                  'El hecho y la fuente'],
                 'correcta': 'C'},
                {'pregunta': '¿Cuál NO es un componente esencial del '
                             'acontecimiento histórico?',
                 'alternativas': ['La sociedad',
                                  'El tiempo',
                                  'El espacio',
                                  'La tecnología',
                                  'Ninguno, los tres primeros lo son'],
                 'correcta': 'D'},
                {'pregunta': 'Los topónimos, las leyendas y los cantos '
                             'corresponden a fuentes:',
                 'alternativas': ['Materiales',
                                  'Escritas',
                                  'Orales o tradicionales',
                                  'Antroposomáticas',
                                  'Audiovisuales'],
                 'correcta': 'C'},
                {'pregunta': 'Las momias, los cabellos y los huesos son '
                             'fuentes:',
                 'alternativas': ['Monumentales',
                                  'Antroposomáticas',
                                  'Documentales',
                                  'Audiovisuales',
                                  'Orales'],
                 'correcta': 'B'},
                {'pregunta': 'Los llamados «vladivideos» y «petroaudios» '
                             'constituyen fuentes:',
                 'alternativas': ['Escritas',
                                  'Materiales',
                                  'Antroposomáticas',
                                  'Audiovisuales',
                                  'Tradicionales'],
                 'correcta': 'D'},
                {'pregunta': 'La institución encargada de la preservación '
                             'del patrimonio cultural peruano es:',
                 'alternativas': ['El Ministerio de Educación',
                                  'El Ministerio de Cultura',
                                  'El INC',
                                  'La UNESCO',
                                  'El Congreso de la República'],
                 'correcta': 'B'},
                {'pregunta': 'El fondo documental del Estado peruano es '
                             'custodiado por:',
                 'alternativas': ['La Biblioteca Nacional',
                                  'El Archivo General de la Nación',
                                  'El Ministerio de Cultura',
                                  'La UNSAAC',
                                  'El Archivo Regional del Cusco'],
                 'correcta': 'B'},
                {'pregunta': 'El folclore, la tradición y la cultura viva de '
                             'los pueblos forman parte de la cultura:',
                 'alternativas': ['Material',
                                  'Inmaterial',
                                  'Monumental',
                                  'Documental',
                                  'Arqueológica'],
                 'correcta': 'B'},
                {'pregunta': 'Las crónicas y los manuscritos coloniales son '
                             'fuentes:',
                 'alternativas': ['Orales',
                                  'Materiales',
                                  'Escritas',
                                  'Antroposomáticas',
                                  'Audiovisuales'],
                 'correcta': 'C'},
                {'pregunta': 'La historia «como hecho» se refiere a:',
                 'alternativas': ['El método de estudio del pasado',
                                  'Los acontecimientos y procesos sociales '
                                  'del pasado',
                                  'La crítica de las fuentes',
                                  'La periodificación cronológica',
                                  'La conservación del patrimonio'],
                 'correcta': 'B'},
                {'pregunta': 'El propósito final del estudio de la historia, '
                             'según el texto, es:',
                 'alternativas': ['Memorizar fechas exactas',
                                  'Comprender el presente y proyectarse al '
                                  'futuro',
                                  'Coleccionar restos arqueológicos',
                                  'Defender una ideología',
                                  'Escribir crónicas'],
                 'correcta': 'B'},
                {'pregunta': 'Las construcciones arquitectónicas, la '
                             'cerámica y los textiles corresponden a '
                             'fuentes:',
                 'alternativas': ['Materiales o monumentales',
                                  'Orales',
                                  'Escritas',
                                  'Audiovisuales',
                                  'Antroposomáticas'],
                 'correcta': 'A'},
                {'pregunta': 'La dimensión temporal de larga duración se '
                             'refiere a:',
                 'alternativas': ['Un hecho puntual',
                                  'Procesos que abarcan siglos',
                                  'La cronología absoluta',
                                  'Un acontecimiento anual',
                                  'La biografía de un personaje'],
                 'correcta': 'B'},
                {'pregunta': 'El Archivo Regional del Cusco (A.R.C.) es una '
                             'institución de:',
                 'alternativas': ['Recaudación tributaria',
                                  'Investigación y difusión del patrimonio '
                                  'cultural',
                                  'Educación básica regular',
                                  'Gobierno regional exclusivo',
                                  'Turismo receptivo'],
                 'correcta': 'B'},
                {'pregunta': 'El estudio sistemático, verídico y metódico '
                             'corresponde a la historia entendida como:',
                 'alternativas': ['Hecho',
                                  'Ciencia',
                                  'Mito',
                                  'Tradición',
                                  'Patrimonio'],
                 'correcta': 'B'},
                {'pregunta': 'El espacio como componente histórico puede '
                             'ser:',
                 'alternativas': ['Solo nacional',
                                  'Solo local',
                                  'Local, regional, nacional, continental o '
                                  'mundial',
                                  'Únicamente continental',
                                  'Solo urbano'],
                 'correcta': 'C'},
                {'pregunta': 'La obligación de cuidar y conservar el '
                             'patrimonio cultural corresponde a:',
                 'alternativas': ['Solo al Ministerio de Cultura',
                                  'Solo a los arqueólogos',
                                  'El Estado y la comunidad nacional',
                                  'Los gobiernos regionales únicamente',
                                  'La UNESCO'],
                 'correcta': 'C'},
                {'pregunta': 'Los idiomas y las creencias transmitidas de '
                             'padres a hijos son fuentes:',
                 'alternativas': ['Escritas',
                                  'Orales',
                                  'Monumentales',
                                  'Audiovisuales',
                                  'Somáticas'],
                 'correcta': 'B'},
                {'pregunta': 'Señale la afirmación CORRECTA sobre las '
                             'fuentes históricas:',
                 'alternativas': ['Solo las escritas son válidas',
                                  'Son restos, huellas y testimonios '
                                  'materiales e inmateriales',
                                  'Solo existen desde la invención de la '
                                  'imprenta',
                                  'Únicamente las produce el Estado',
                                  'Se limitan a los restos arqueológicos'],
                 'correcta': 'B'}]},
 {'num': 2,
  'titulo': 'Hombre de la prehistoria',
  'secciones': [{'titulo': '2.1 PROCESO DE HOMINIZACIÓN',
                 'items': ['Es el conjunto de modificaciones {biológicas} y '
                           'anatómicas, así como de logros {culturales}, '
                           'desarrollados durante millones de años.',
                           '1° La {bipedación} y la postura erguida, que '
                           'liberó las extremidades superiores.',
                           '2° La capacidad de fabricar {objetos}, que marcó '
                           'el paso de los hominoides a los {homínidos} y se '
                           'considera el inicio de la {cultura}.',
                           'La teoría {evolucionista} fue formulada por '
                           '{Charles Darwin} en su libro «El origen de las '
                           'especies por medio de la selección natural».']},
                {'titulo': '2.2 LA PREHISTORIA: CONCEPTO',
                 'items': ['El concepto fue propuesto por Jacobo Boucher de '
                           'Perthes y utilizado por el inglés {Daniel '
                           'Wilson} en {1851}.',
                           'Se refiere al periodo anterior a la aparición de '
                           'la {escritura}.',
                           '{Christian Thomsen} dividió esta etapa '
                           'observando los {materiales} con que el hombre '
                           'fabricaba sus herramientas.']},
                {'titulo': '2.3.1 PALEOLÍTICO (hasta 10 000 a.C.)',
                 'items': ['Del griego palaios = {antiguo} y lithos = '
                           '{piedra}. Es el periodo de la piedra {tallada} y '
                           'de mayor duración.',
                           'Fueron {nómadas}, cavernícolas y errantes; '
                           'recolectores de piedras, preferentemente el '
                           '{sílex}.',
                           'Usaron la técnica {osteodontoquerática}, con '
                           'huesos de mandíbula de animales.',
                           'Se organizaron en {hordas}, clanes y gens; '
                           'practicaron el incesto y veneraron un antepasado '
                           'común llamado {tótem}.',
                           'Descubrieron el {fuego} y crearon el arte '
                           '{rupestre}: {Altamira} en España y {Lascaux} en '
                           'Francia.']},
                {'titulo': '2.3.2 MESOLÍTICO (10 000 – 7000 a.C.)',
                 'items': ['Periodo de transición del {Pleistoceno} al '
                           '{Holoceno}.',
                           'Se desarrolló la industria {microlítica} y la '
                           'pesca con {arpón}.',
                           'Se practicó la {horticultura} y se inició la '
                           '{domesticación} de animales.']},
                {'titulo': '2.3.3 NEOLÍTICO (7000 – 3000 a.C.)',
                 'items': ['Del griego neo = {nuevo}: periodo de la piedra '
                           '{pulimentada}.',
                           'Fueron {sedentarios} y practicaron la '
                           '{agricultura} y la ganadería: primera gran '
                           '{revolución} agrícola.',
                           'Iniciaron la {alfarería} y la textilería con '
                           'algodón, lana y lino.',
                           'Construyeron viviendas sobre pilotes llamadas '
                           '{palafitos}; la primera ciudad prehistórica se '
                           'halló en el lago {Zúrich}.',
                           'Desarrollaron arquitectura funeraria: '
                           '{dólmenes}, menhires y crómlech. Destaca '
                           '{Stonehenge} en Inglaterra.',
                           'Surgen la {propiedad privada}, las clases '
                           'sociales y el {Estado}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El paso de los hominoides a los homínidos quedó '
                           'marcado por {La capacidad de fabricar objetos}.',
                           'El término «prehistoria» se refiere al periodo '
                           'anterior a la aparición de {La escritura}.',
                           'Christian Thomsen dividió la prehistoria '
                           'observando {Los materiales de las herramientas}.',
                           'Altamira y Lascaux son famosas por su {Arte '
                           'rupestre}.',
                           'El hombre del Paleolítico se caracterizó por ser '
                           '{Nómada y cavernícola}.',
                           'La organización social del Paleolítico '
                           'comprendió {Hordas, clanes y gens}.',
                           'El tótem en el Paleolítico era {Un antepasado '
                           'común sacralizado}.',
                           'El Mesolítico es el periodo de transición entre '
                           '{Pleistoceno y Holoceno}.',
                           'La primera gran revolución agrícola y ganadera '
                           'corresponde al {Neolítico}.',
                           'Los palafitos fueron {Casas de madera sobre '
                           'pilotes}.',
                           'Los dólmenes, menhires y crómlech son '
                           'expresiones de arquitectura {Funeraria y '
                           'religiosa}.',
                           'En el Neolítico surgen por primera vez {La '
                           'propiedad privada, las clases sociales y el '
                           'Estado}.',
                           'El uso del cobre fundido se inició en '
                           '{Çatalhöyük (Turquía)}.',
                           'El bronce es una aleación de cobre con {Estaño}.',
                           'Etimológicamente, «Neolítico» significa {Piedra '
                           'nueva o pulimentada}.',
                           'La bipedación trajo como consecuencia directa '
                           '{El uso exclusivo de las extremidades inferiores '
                           'para desplazarse}.',
                           'La primera ciudad prehistórica construida sobre '
                           'un lago se descubrió en {El lago Zúrich, '
                           'Suiza}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La teoría evolucionista fue formulada por '
                           '{Charles Darwin}.',
                           'La técnica osteodontoquerática consistió en el '
                           'uso de {Huesos de mandíbula de animales}.',
                           'Stonehenge, importante monumento megalítico, se '
                           'ubica en {Inglaterra}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['El Paleolítico abarca desde el origen del hombre '
                           'hasta aproximadamente {10 000} a.C.',
                           'El Mesolítico se ubica entre 10 000 y {7000} '
                           'a.C., y el Neolítico entre 7000 y {3000} a.C.',
                           'En el Mesolítico se desarrolló la industria '
                           '{microlítica}, de la que son ejemplo las venus '
                           'de Willendorf.',
                           'La Edad del Cobre o Calcolítico se ubica entre '
                           '5000 y {3000} a.C.',
                           'El bronce comenzó a usarse en {Sumeria} '
                           '(Mesopotamia) hace unos 3000 años, y luego se '
                           'extendió al Cercano Oriente y Europa.',
                           'El hierro fundido fue utilizado primero por los '
                           '{hititas} de Turquía, hace unos 1500 años.',
                           'En Europa, el uso del hierro comenzó con la '
                           'cultura de {Hallstatt} en Austria y continuó con '
                           'la cultura de La Tène en Suiza.']}],
  'cuadros': [{'titulo': '2.3.4 EDAD DE LOS METALES',
               'encabezados': ['Periodo', 'Cronología', 'Dato clave'],
               'filas': [['{Cobre} o Calcolítico',
                          '5000 – 3000 a.C.',
                          'Se inició en {Çatalhöyük} (Turquía)'],
                         ['{Bronce}',
                          '3000 – 1500 a.C.',
                          'Aleación de cobre y {estaño}'],
                         ['{Hierro}',
                          'desde 1500 a.C.',
                          'Metal más {duro} y resistente']]}],
  'preguntas': [{'pregunta': 'El paso de los hominoides a los homínidos '
                             'quedó marcado por:',
                 'alternativas': ['El descubrimiento del fuego',
                                  'La capacidad de fabricar objetos',
                                  'La aparición de la escritura',
                                  'La domesticación de animales',
                                  'La vida sedentaria'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría evolucionista fue formulada por:',
                 'alternativas': ['Christian Thomsen',
                                  'Daniel Wilson',
                                  'Charles Darwin',
                                  'Heródoto',
                                  'Boucher de Perthes'],
                 'correcta': 'C'},
                {'pregunta': 'El término «prehistoria» se refiere al periodo '
                             'anterior a la aparición de:',
                 'alternativas': ['La agricultura',
                                  'La rueda',
                                  'La escritura',
                                  'Los metales',
                                  'La cerámica'],
                 'correcta': 'C'},
                {'pregunta': 'Christian Thomsen dividió la prehistoria '
                             'observando:',
                 'alternativas': ['Las glaciaciones',
                                  'Los materiales de las herramientas',
                                  'Los restos óseos',
                                  'Las pinturas rupestres',
                                  'Los enterramientos'],
                 'correcta': 'B'},
                {'pregunta': 'La técnica osteodontoquerática consistió en el '
                             'uso de:',
                 'alternativas': ['Piedra pulimentada',
                                  'Huesos de mandíbula de animales',
                                  'Metales fundidos',
                                  'Fibras vegetales',
                                  'Arcilla cocida'],
                 'correcta': 'B'},
                {'pregunta': 'Altamira y Lascaux son famosas por su:',
                 'alternativas': ['Arquitectura megalítica',
                                  'Arte rupestre',
                                  'Metalurgia del bronce',
                                  'Escritura cuneiforme',
                                  'Cerámica policroma'],
                 'correcta': 'B'},
                {'pregunta': 'El hombre del Paleolítico se caracterizó por '
                             'ser:',
                 'alternativas': ['Sedentario y agricultor',
                                  'Nómada y cavernícola',
                                  'Ganadero y alfarero',
                                  'Comerciante y navegante',
                                  'Urbano y estatal'],
                 'correcta': 'B'},
                {'pregunta': 'La organización social del Paleolítico '
                             'comprendió:',
                 'alternativas': ['Ayllus y curacazgos',
                                  'Hordas, clanes y gens',
                                  'Ciudades-Estado',
                                  'Reinos hereditarios',
                                  'Imperios centralizados'],
                 'correcta': 'B'},
                {'pregunta': 'El tótem en el Paleolítico era:',
                 'alternativas': ['Una herramienta de sílex',
                                  'Un antepasado común sacralizado',
                                  'Una vivienda sobre pilotes',
                                  'Un tipo de sepultura',
                                  'Un instrumento musical'],
                 'correcta': 'B'},
                {'pregunta': 'El Mesolítico es el periodo de transición '
                             'entre:',
                 'alternativas': ['Holoceno y Pleistoceno',
                                  'Pleistoceno y Holoceno',
                                  'Neolítico y Edad de los Metales',
                                  'Paleolítico y Edad del Cobre',
                                  'Edad del Bronce y del Hierro'],
                 'correcta': 'B'},
                {'pregunta': 'La primera gran revolución agrícola y ganadera '
                             'corresponde al:',
                 'alternativas': ['Paleolítico',
                                  'Mesolítico',
                                  'Neolítico',
                                  'Calcolítico',
                                  'Edad del Hierro'],
                 'correcta': 'C'},
                {'pregunta': 'Los palafitos fueron:',
                 'alternativas': ['Tumbas colectivas',
                                  'Casas de madera sobre pilotes',
                                  'Templos escalonados',
                                  'Herramientas de sílex',
                                  'Vasijas rituales'],
                 'correcta': 'B'},
                {'pregunta': 'Los dólmenes, menhires y crómlech son '
                             'expresiones de arquitectura:',
                 'alternativas': ['Palaciega',
                                  'Funeraria y religiosa',
                                  'Militar',
                                  'Hidráulica',
                                  'Doméstica'],
                 'correcta': 'B'},
                {'pregunta': 'Stonehenge, importante monumento megalítico, '
                             'se ubica en:',
                 'alternativas': ['Francia',
                                  'España',
                                  'Inglaterra',
                                  'Suiza',
                                  'Turquía'],
                 'correcta': 'C'},
                {'pregunta': 'En el Neolítico surgen por primera vez:',
                 'alternativas': ['El nomadismo y la caza',
                                  'La propiedad privada, las clases sociales '
                                  'y el Estado',
                                  'El arte rupestre',
                                  'La osteodontoquerática',
                                  'Las glaciaciones'],
                 'correcta': 'B'},
                {'pregunta': 'El uso del cobre fundido se inició en:',
                 'alternativas': ['Babilonia',
                                  'Çatalhöyük (Turquía)',
                                  'Nínive',
                                  'Menfis',
                                  'Ur'],
                 'correcta': 'B'},
                {'pregunta': 'El bronce es una aleación de cobre con:',
                 'alternativas': ['Hierro',
                                  'Plata',
                                  'Estaño',
                                  'Plomo',
                                  'Zinc'],
                 'correcta': 'C'},
                {'pregunta': 'Etimológicamente, «Neolítico» significa:',
                 'alternativas': ['Piedra antigua',
                                  'Piedra media',
                                  'Piedra nueva o pulimentada',
                                  'Edad del metal',
                                  'Edad del hielo'],
                 'correcta': 'C'},
                {'pregunta': 'La bipedación trajo como consecuencia directa:',
                 'alternativas': ['El aumento del cráneo',
                                  'El uso exclusivo de las extremidades '
                                  'inferiores para desplazarse',
                                  'La aparición del lenguaje escrito',
                                  'La domesticación del perro',
                                  'La construcción de ciudades'],
                 'correcta': 'B'},
                {'pregunta': 'La primera ciudad prehistórica construida '
                             'sobre un lago se descubrió en:',
                 'alternativas': ['El lago Titicaca',
                                  'El lago Zúrich, Suiza',
                                  'El mar Muerto',
                                  'El lago Van',
                                  'El lago Ness'],
                 'correcta': 'B'}]},
 {'num': 3,
  'titulo': 'Grandes culturas de la antigüedad',
  'secciones': [{'titulo': '3.1 MESOPOTAMIA — UBICACIÓN',
                 'items': ['Se desarrolló entre los ríos {Tigris} y '
                           '{Éufrates}, al suroeste de Asia. Hoy corresponde '
                           'principalmente a {Irak}.',
                           'La Alta Mesopotamia, al norte, fue sede de la '
                           'civilización {Asiria}, con capital en {Nínive}, '
                           'a orillas del Tigris.',
                           'La Baja Mesopotamia, al sur, fue sede de la '
                           'civilización {Caldea}, con capital en '
                           '{Babilonia}, junto al Éufrates.',
                           'Pueblos que la habitaron: sumerios, acadios, '
                           'babilonios, {hititas}, caldeos, medos y '
                           '{persas}.']},
                {'titulo': '3.1.2 PROCESO HISTÓRICO',
                 'items': ['Los {sumerios} (3000 a.C.) crearon las primeras '
                           '{Ciudades-Estado}: Kish, Uruk, Ur y Lagash. '
                           'Inventaron la escritura {cuneiforme} y '
                           'conocieron la {rueda}.',
                           'Los acadios, dirigidos por {Sargón}, '
                           'conquistaron las ciudades sumerias y fijaron su '
                           'capital en {Akkad}.',
                           'En el Primer Imperio Babilónico, el rey '
                           '{Hammurabi} unificó las ciudades sumerias y '
                           'estableció su famoso {código} jurídico.',
                           'En el Imperio Asirio destacó {Asurbanipal}, '
                           'quien mandó construir la biblioteca de {Nínive}.',
                           'En el Segundo Imperio Babilónico, {Nabucodonosor '
                           'II} conquistó Jerusalén —hecho conocido como el '
                           '{cautiverio} babilónico— y mandó construir los '
                           '{jardines colgantes}.']},
                {'titulo': '3.1.4 EXPRESIONES CULTURALES',
                 'items': ['Arquitectura: el {zigurat}. Fueron los primeros '
                           'en construir el {arco}, la bóveda y la {cúpula}.',
                           'Escultura: los toros {alados} con cabeza humana '
                           'del palacio de Sargón II en Korsabad; la estatua '
                           'del príncipe {Gudea}.',
                           'Escritura: la {cuneiforme}, con signos en forma '
                           'de cuña. La roca de {Behistún} fue descifrada '
                           'por {Henry Rawlinson}.']},
                {'titulo': '3.2 EGIPTO',
                 'items': ['Situado al {noreste} del continente africano, en '
                           'torno al río {Nilo}, llamado por Heródoto «don '
                           'del Nilo».',
                           'Limitaba al norte con el mar {Mediterráneo}, al '
                           'este con el istmo de {Suez}, al sur con Nubia y '
                           'al oeste con el desierto de {Libia}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Mesopotamia se desarrolló entre los ríos {Tigris '
                           'y Éufrates}.',
                           'El «cautiverio babilónico» afectó al pueblo '
                           '{Judío}.',
                           'Fueron los primeros en construir el arco, la '
                           'bóveda y la cúpula {Los mesopotámicos}.',
                           'La escritura cuneiforme recibe ese nombre por '
                           '{Sus signos en forma de cuña}.',
                           'El límite norte del antiguo Egipto era {El mar '
                           'Mediterráneo}.',
                           'El artífice de la caída del Imperio Asirio fue '
                           '{Nabopolasar}.',
                           'La estatua del príncipe Gudea se conserva '
                           'actualmente en {El Museo del Louvre}.',
                           'Un factor que explica las constantes invasiones '
                           'a Mesopotamia fue {La ausencia de fronteras '
                           'naturales}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La capital del Imperio Asirio fue {Nínive}.',
                           'Las primeras Ciudades-Estado de Mesopotamia '
                           'fueron creadas por los {Sumerios}.',
                           'El rey acadio que conquistó las ciudades '
                           'sumerias fue {Sargón}.',
                           'El primer código jurídico escrito de Mesopotamia '
                           'se atribuye a {Hammurabi}.',
                           'La biblioteca de Nínive fue mandada construir '
                           'por {Asurbanipal}.',
                           'Los jardines colgantes de Babilonia se atribuyen '
                           'a {Nabucodonosor II}.',
                           'El templo escalonado característico de '
                           'Mesopotamia se denomina {Zigurat}.',
                           'La inscripción de la roca de Behistún fue '
                           'descifrada por {Henry Rawlinson}.',
                           'Los toros alados con cabeza humana se hallaron '
                           'en el palacio de {Sargón II en Korsabad}.',
                           'La Baja Mesopotamia fue la región donde se '
                           'desarrolló la civilización {Caldea}.',
                           'Actualmente el territorio de Mesopotamia '
                           'corresponde principalmente a {Irak}.',
                           'Egipto se ubica en el continente {Africano}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['Actualmente el territorio de Mesopotamia '
                           'corresponde a varios países del Medio Oriente, '
                           'entre los que destaca {Irak}.',
                           'Los amoritas, procedentes de {Arabia}, '
                           'establecieron el Imperio Babilónico, cuyo rey '
                           'Hammurabi unificó las ciudades sumerias.',
                           'La estatua del príncipe Gudea, en mármol y '
                           'diorita, se conserva en el Museo del {Louvre} en '
                           'París.',
                           'Egipto limitaba por el sur con Nubia, región que '
                           'hoy corresponde a {Etiopía}.',
                           'Durante el Imperio Antiguo egipcio destacó la '
                           'tercera dinastía con el faraón {Dyeser} (Zocer), '
                           'por su dominio de la arquitectura monumental en '
                           'piedra.',
                           'En el Imperio Nuevo egipcio, los faraones '
                           '{Tutmosis III} y Ramsés II extendieron el '
                           'dominio hasta Palestina y Siria.',
                           'El faraón {Amenofis IV} intentó imponer el culto '
                           'a un solo dios, Atón, rompiendo con la tradición '
                           'politeísta egipcia.',
                           'La escritura jeroglífica egipcia era la más '
                           'antigua y compleja; existía también una '
                           'escritura más simple llamada {demótica}, usada '
                           'por el pueblo.']}],
  'cuadros': [{'titulo': '3.1 ETAPAS DE MESOPOTAMIA',
               'encabezados': ['Etapa', 'Personaje / Aporte'],
               'filas': [['Sumerios',
                          'Ciudades-Estado, escritura {cuneiforme}'],
                         ['Acadios', '{Sargón}, capital en Akkad'],
                         ['1er Imperio Babilónico',
                          '{Hammurabi} y su código'],
                         ['Imperio Asirio',
                          '{Asurbanipal}, biblioteca de Nínive'],
                         ['2do Imperio Babilónico',
                          '{Nabucodonosor II}, jardines colgantes']]}],
  'preguntas': [{'pregunta': 'Mesopotamia se desarrolló entre los ríos:',
                 'alternativas': ['Nilo y Éufrates',
                                  'Tigris y Éufrates',
                                  'Indo y Ganges',
                                  'Amarillo y Azul',
                                  'Danubio y Rin'],
                 'correcta': 'B'},
                {'pregunta': 'La capital del Imperio Asirio fue:',
                 'alternativas': ['Babilonia',
                                  'Ur',
                                  'Nínive',
                                  'Akkad',
                                  'Uruk'],
                 'correcta': 'C'},
                {'pregunta': 'Las primeras Ciudades-Estado de Mesopotamia '
                             'fueron creadas por los:',
                 'alternativas': ['Acadios',
                                  'Sumerios',
                                  'Caldeos',
                                  'Hititas',
                                  'Persas'],
                 'correcta': 'B'},
                {'pregunta': 'El rey acadio que conquistó las ciudades '
                             'sumerias fue:',
                 'alternativas': ['Hammurabi',
                                  'Asurbanipal',
                                  'Sargón',
                                  'Nabopolasar',
                                  'Gudea'],
                 'correcta': 'C'},
                {'pregunta': 'El primer código jurídico escrito de '
                             'Mesopotamia se atribuye a:',
                 'alternativas': ['Sargón',
                                  'Hammurabi',
                                  'Nabucodonosor II',
                                  'Asurbanipal',
                                  'Rawlinson'],
                 'correcta': 'B'},
                {'pregunta': 'La biblioteca de Nínive fue mandada construir '
                             'por:',
                 'alternativas': ['Hammurabi',
                                  'Sargón II',
                                  'Asurbanipal',
                                  'Nabopolasar',
                                  'Nabucodonosor II'],
                 'correcta': 'C'},
                {'pregunta': 'Los jardines colgantes de Babilonia se '
                             'atribuyen a:',
                 'alternativas': ['Hammurabi',
                                  'Nabucodonosor II',
                                  'Asurbanipal',
                                  'Sargón',
                                  'Gudea'],
                 'correcta': 'B'},
                {'pregunta': 'El «cautiverio babilónico» afectó al pueblo:',
                 'alternativas': ['Asirio',
                                  'Hitita',
                                  'Judío',
                                  'Persa',
                                  'Acadio'],
                 'correcta': 'C'},
                {'pregunta': 'El templo escalonado característico de '
                             'Mesopotamia se denomina:',
                 'alternativas': ['Mastaba',
                                  'Zigurat',
                                  'Pirámide',
                                  'Partenón',
                                  'Ziggurat egipcio'],
                 'correcta': 'B'},
                {'pregunta': 'Fueron los primeros en construir el arco, la '
                             'bóveda y la cúpula:',
                 'alternativas': ['Los egipcios',
                                  'Los mesopotámicos',
                                  'Los griegos',
                                  'Los romanos',
                                  'Los persas'],
                 'correcta': 'B'},
                {'pregunta': 'La escritura cuneiforme recibe ese nombre por:',
                 'alternativas': ['Su soporte de papiro',
                                  'Sus signos en forma de cuña',
                                  'Su origen sacerdotal',
                                  'Su uso comercial',
                                  'Su carácter jeroglífico'],
                 'correcta': 'B'},
                {'pregunta': 'La inscripción de la roca de Behistún fue '
                             'descifrada por:',
                 'alternativas': ['Champollion',
                                  'Henry Rawlinson',
                                  'Schliemann',
                                  'Heródoto',
                                  'Boucher de Perthes'],
                 'correcta': 'B'},
                {'pregunta': 'Los toros alados con cabeza humana se hallaron '
                             'en el palacio de:',
                 'alternativas': ['Hammurabi en Babilonia',
                                  'Sargón II en Korsabad',
                                  'Asurbanipal en Nínive',
                                  'Gudea en Lagash',
                                  'Ciro en Persépolis'],
                 'correcta': 'B'},
                {'pregunta': 'La Baja Mesopotamia fue la región donde se '
                             'desarrolló la civilización:',
                 'alternativas': ['Asiria',
                                  'Caldea',
                                  'Hitita',
                                  'Persa',
                                  'Elamita'],
                 'correcta': 'B'},
                {'pregunta': 'Actualmente el territorio de Mesopotamia '
                             'corresponde principalmente a:',
                 'alternativas': ['Irán',
                                  'Irak',
                                  'Siria',
                                  'Turquía',
                                  'Egipto'],
                 'correcta': 'B'},
                {'pregunta': 'Egipto se ubica en el continente:',
                 'alternativas': ['Asiático',
                                  'Africano',
                                  'Europeo',
                                  'Americano',
                                  'Oceánico'],
                 'correcta': 'B'},
                {'pregunta': 'El límite norte del antiguo Egipto era:',
                 'alternativas': ['El Mar Rojo',
                                  'El mar Mediterráneo',
                                  'El desierto de Libia',
                                  'Nubia',
                                  'El istmo de Suez'],
                 'correcta': 'B'},
                {'pregunta': 'El artífice de la caída del Imperio Asirio '
                             'fue:',
                 'alternativas': ['Nabucodonosor II',
                                  'Nabopolasar',
                                  'Sargón',
                                  'Hammurabi',
                                  'Ciro'],
                 'correcta': 'B'},
                {'pregunta': 'La estatua del príncipe Gudea se conserva '
                             'actualmente en:',
                 'alternativas': ['El Museo Británico',
                                  'El Museo del Louvre',
                                  'El Museo de Berlín',
                                  'El Metropolitan',
                                  'El Museo de El Cairo'],
                 'correcta': 'B'},
                {'pregunta': 'Un factor que explica las constantes '
                             'invasiones a Mesopotamia fue:',
                 'alternativas': ['Su aislamiento total',
                                  'La ausencia de fronteras naturales',
                                  'Su clima glacial',
                                  'Su escasa población',
                                  'La falta de ríos'],
                 'correcta': 'B'}]},
 {'num': 4,
  'titulo': 'Mundo greco romano',
  'secciones': [{'titulo': '4.1 GRECIA — PROCESO HISTÓRICO',
                 'items': ['Se desarrolló en el sur de la península de los '
                           '{Balcanes}, en torno al mar {Egeo}.',
                           'Grecia {Arcaica} o Heroica (800–494 a.C.): se '
                           'formaron las {polis} o ciudades-Estado.',
                           'Grecia {Clásica} o del Apogeo (494–359 a.C.): '
                           'destacaron {Atenas} y {Esparta}.',
                           'La {democracia} —gobierno del pueblo— fue '
                           'introducida por el legislador {Solón} y se '
                           'consolidó en {Atenas}.',
                           'Con el gobierno de {Pericles}, Atenas vivió su '
                           'máximo esplendor, llamado {Siglo de Oro}.',
                           'Grecia Decadente y {Helenística} (359–146 a.C.): '
                           '{Alejandro Magno} extendió la cultura griega '
                           'hasta la {India}; a su muerte el imperio se '
                           'repartió entre sus {generales}.']},
                {'titulo': '4.1.3 ORGANIZACIÓN POLÍTICA',
                 'items': ['Quien sistematizó la organización política de '
                           '{Esparta} fue {Licurgo}.',
                           'Quien organizó políticamente {Atenas} fue '
                           '{Solón}, considerado el más amable y bondadoso '
                           'de los legisladores.']},
                {'titulo': '4.1.4 EXPRESIONES CULTURALES',
                 'items': ['Arquitectura: destaca el {Partenón}, erigido en '
                           'la {Acrópolis} de Atenas.',
                           'Escultura: {Fidias} fue autor de los relieves de '
                           'los frontones y las {metopas} del Partenón.']},
                {'titulo': '4.2 ROMA — PROCESO HISTÓRICO',
                 'items': ['Se desarrolló en la península {Itálica}. La '
                           'historia de Roma se inicia el año {753} a.C. con '
                           'su fundación por {Rómulo}.',
                           'Roma {Monárquica} (753–509 a.C.): el cargo del '
                           'rey era {vitalicio}. Con Rómulo se iniciaron la '
                           'asamblea y el {Senado}. Los últimos reyes fueron '
                           'de origen {etrusco}.',
                           'Roma {Republicana} (509–27 a.C.): gobierno de '
                           'cónsules, Senado y asambleas.',
                           'Roma {Imperial} (27 a.C.–476 d.C.): el primer '
                           'emperador fue {Octavio Augusto}. Este periodo se '
                           'conoce como la {pax romana}.',
                           'Desde el siglo {III} d.C. el imperio sufrió '
                           'crisis militares, políticas y económicas, y un '
                           'proceso de {ruralización}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Alejandro Magno extendió la cultura griega hasta '
                           '{La India}.',
                           'El Partenón fue erigido en {La Acrópolis de '
                           'Atenas}.',
                           'A la muerte de Alejandro Magno, su imperio fue '
                           'repartido entre {Sus generales}.',
                           'Roma fue fundada, según la tradición, el año '
                           '{753 a.C.}.',
                           'Con Rómulo se iniciaron en Roma dos '
                           'instituciones {La asamblea y el Senado}.',
                           'Grecia se desarrolló en el sur de la península '
                           '{De los Balcanes}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La democracia fue introducida en Atenas por el '
                           'legislador {Solón}.',
                           'El «Siglo de Oro» de Atenas corresponde al '
                           'gobierno de {Pericles}.',
                           'Quien sistematizó la organización política de '
                           'Esparta fue {Licurgo}.',
                           'Las ciudades-Estado griegas recibían el nombre '
                           'de {Polis}.',
                           'El autor de los relieves y metopas del Partenón '
                           'fue {Fidias}.',
                           'El fundador legendario de Roma fue {Rómulo}.',
                           'Durante la monarquía romana, el cargo del rey '
                           'era {Vitalicio}.',
                           'Los últimos reyes de Roma fueron de origen '
                           '{Etrusco}.',
                           'El primer emperador romano fue {Octavio '
                           'Augusto}.',
                           'El periodo de estabilidad del Imperio Romano se '
                           'conoce como {Pax romana}.',
                           'La República romana comprende el periodo {509–27 '
                           'a.C.}.',
                           'La crisis del Imperio Romano, desde el siglo III '
                           'd.C., incluyó un proceso de {Ruralización}.',
                           'La caída del Imperio Romano de Occidente se fija '
                           'en el año {476 d.C.}.',
                           'El periodo helenístico de Grecia abarca los años '
                           '{359–146 a.C.}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['Grecia se desarrolló entre el sur de la '
                           'península de los Balcanes, las costas de {Asia '
                           'Menor} y las islas del mar Egeo.',
                           'Las Guerras Médicas enfrentaron a los griegos '
                           'contra los persas, comandados por {Darío I} y '
                           'Jerjes.',
                           'El ejército de Macedonia, al mando de {Filipo '
                           'II}, conquistó las polis griegas dando inicio al '
                           'periodo helenístico.',
                           'En la escultura griega, {Policleto} fijó las '
                           'proporciones ideales del cuerpo humano, mientras '
                           'Praxíteles delineó la curva de los cuerpos.',
                           'La Península Itálica se dividió en tres zonas: '
                           'continental, peninsular e {insular}.',
                           'Los excesos de {Tarquino el Soberbio}, el último '
                           'rey, originaron la rebelión que dio inicio a la '
                           'República romana.',
                           'Roma se enfrentó a Cartago en tres guerras '
                           'conocidas como {guerras púnicas}; en la tercera, '
                           'en el año 146 a.C., Cartago fue destruida.',
                           'Tras el asesinato de {Julio César} en el año 44 '
                           'a.C. se formó un triunvirato que llevaría al fin '
                           'de la República.']}],
  'cuadros': [{'titulo': '4.2 ETAPAS DE ROMA',
               'encabezados': ['Etapa', 'Años', 'Rasgo'],
               'filas': [['{Monárquica}',
                          '{753} – 509 a.C.',
                          'Reyes vitalicios; {Rómulo}'],
                         ['{Republicana}',
                          '509 – {27} a.C.',
                          'Cónsules y {Senado}'],
                         ['{Imperial}',
                          '27 a.C. – {476} d.C.',
                          '{Octavio Augusto}; pax romana']]}],
  'preguntas': [{'pregunta': 'La democracia fue introducida en Atenas por el '
                             'legislador:',
                 'alternativas': ['Licurgo',
                                  'Solón',
                                  'Pericles',
                                  'Clístenes',
                                  'Dracón'],
                 'correcta': 'B'},
                {'pregunta': 'El «Siglo de Oro» de Atenas corresponde al '
                             'gobierno de:',
                 'alternativas': ['Solón',
                                  'Licurgo',
                                  'Pericles',
                                  'Alejandro Magno',
                                  'Fidias'],
                 'correcta': 'C'},
                {'pregunta': 'Quien sistematizó la organización política de '
                             'Esparta fue:',
                 'alternativas': ['Solón',
                                  'Licurgo',
                                  'Pericles',
                                  'Rómulo',
                                  'Dracón'],
                 'correcta': 'B'},
                {'pregunta': 'Alejandro Magno extendió la cultura griega '
                             'hasta:',
                 'alternativas': ['Egipto',
                                  'La India',
                                  'China',
                                  'Britania',
                                  'Hispania'],
                 'correcta': 'B'},
                {'pregunta': 'Las ciudades-Estado griegas recibían el nombre '
                             'de:',
                 'alternativas': ['Polis',
                                  'Civitas',
                                  'Ayllus',
                                  'Nomos',
                                  'Demos'],
                 'correcta': 'A'},
                {'pregunta': 'El Partenón fue erigido en:',
                 'alternativas': ['Esparta',
                                  'La Acrópolis de Atenas',
                                  'Delfos',
                                  'Olimpia',
                                  'Corinto'],
                 'correcta': 'B'},
                {'pregunta': 'El autor de los relieves y metopas del '
                             'Partenón fue:',
                 'alternativas': ['Praxíteles',
                                  'Fidias',
                                  'Mirón',
                                  'Policleto',
                                  'Escopas'],
                 'correcta': 'B'},
                {'pregunta': 'A la muerte de Alejandro Magno, su imperio fue '
                             'repartido entre:',
                 'alternativas': ['Sus hijos',
                                  'Sus generales',
                                  'El Senado',
                                  'Los persas',
                                  'Los romanos'],
                 'correcta': 'B'},
                {'pregunta': 'Roma fue fundada, según la tradición, el año:',
                 'alternativas': ['509 a.C.',
                                  '753 a.C.',
                                  '27 a.C.',
                                  '476 d.C.',
                                  '146 a.C.'],
                 'correcta': 'B'},
                {'pregunta': 'El fundador legendario de Roma fue:',
                 'alternativas': ['Numa Pompilio',
                                  'Rómulo',
                                  'Tarquino el Soberbio',
                                  'Octavio Augusto',
                                  'Julio César'],
                 'correcta': 'B'},
                {'pregunta': 'Durante la monarquía romana, el cargo del rey '
                             'era:',
                 'alternativas': ['Electivo anual',
                                  'Vitalicio',
                                  'Hereditario por línea femenina',
                                  'Rotativo',
                                  'Temporal por cinco años'],
                 'correcta': 'B'},
                {'pregunta': 'Los últimos reyes de Roma fueron de origen:',
                 'alternativas': ['Griego',
                                  'Etrusco',
                                  'Cartaginés',
                                  'Galo',
                                  'Sabino'],
                 'correcta': 'B'},
                {'pregunta': 'El primer emperador romano fue:',
                 'alternativas': ['Julio César',
                                  'Octavio Augusto',
                                  'Nerón',
                                  'Trajano',
                                  'Constantino'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo de estabilidad del Imperio Romano '
                             'se conoce como:',
                 'alternativas': ['Pax augusta',
                                  'Pax romana',
                                  'Pax deorum',
                                  'Imperium',
                                  'Res publica'],
                 'correcta': 'B'},
                {'pregunta': 'La República romana comprende el periodo:',
                 'alternativas': ['753–509 a.C.',
                                  '509–27 a.C.',
                                  '27 a.C.–476 d.C.',
                                  '800–494 a.C.',
                                  '359–146 a.C.'],
                 'correcta': 'B'},
                {'pregunta': 'Con Rómulo se iniciaron en Roma dos '
                             'instituciones:',
                 'alternativas': ['El consulado y la dictadura',
                                  'La asamblea y el Senado',
                                  'El tribunado y la censura',
                                  'La pretura y la edilidad',
                                  'El imperio y la provincia'],
                 'correcta': 'B'},
                {'pregunta': 'La crisis del Imperio Romano, desde el siglo '
                             'III d.C., incluyó un proceso de:',
                 'alternativas': ['Urbanización acelerada',
                                  'Ruralización',
                                  'Expansión territorial',
                                  'Democratización',
                                  'Helenización'],
                 'correcta': 'B'},
                {'pregunta': 'Grecia se desarrolló en el sur de la '
                             'península:',
                 'alternativas': ['Ibérica',
                                  'Itálica',
                                  'De los Balcanes',
                                  'De Anatolia',
                                  'Escandinava'],
                 'correcta': 'C'},
                {'pregunta': 'La caída del Imperio Romano de Occidente se '
                             'fija en el año:',
                 'alternativas': ['27 a.C.',
                                  '146 a.C.',
                                  '476 d.C.',
                                  '509 a.C.',
                                  '1453 d.C.'],
                 'correcta': 'C'},
                {'pregunta': 'El periodo helenístico de Grecia abarca los '
                             'años:',
                 'alternativas': ['800–494 a.C.',
                                  '494–359 a.C.',
                                  '359–146 a.C.',
                                  '753–509 a.C.',
                                  '146 a.C.–27 a.C.'],
                 'correcta': 'C'}]},
 {'num': 5,
  'titulo': 'Primeras culturas andinas',
  'secciones': [{'titulo': '5.2 TEORÍAS SOBRE EL POBLAMIENTO DE AMÉRICA',
                 'items': ['Teoría {autoctonista}: sostenida por el '
                           'paleontólogo argentino {Florentino Ameghino} en '
                           '{1879}; afirmaba que el hombre americano era '
                           'originario del continente.',
                           'Fue rebatida en {1908} por {Alex Hrdlicka}, '
                           'quien demostró que los restos fósiles no '
                           'correspondían a la Era {Terciaria}.',
                           'Teoría de origen {asiático}: sustentada por '
                           '{Alex Hrdlicka}; el poblamiento se habría dado '
                           'por el estrecho de {Bering}.',
                           'Teoría de origen {oceánico} (poligenista o '
                           'polirracial): sustentada por el francés {Paul '
                           'Rivet} en {1943}, con procedencia {melanésica} y '
                           '{polinésica}.',
                           'Teoría de origen {australiano}: sostenida por '
                           '{Mendes Correa}.']},
                {'titulo': '5.3.1 NÓMADAS: RECOLECTORES, CAZADORES Y '
                           'PESCADORES',
                 'items': ['{Paccaicasa} (Ayacucho): los restos líticos más '
                           'antiguos del Perú, hallados por Richard '
                           '{MacNeish}.',
                           '{Toquepala} (Tacna): arte {rupestre} más '
                           'antiguo; representa el chaco o caza ritual.',
                           '{Lauricocha} (Huánuco): primeros restos {óseos} '
                           'humanos, hallados por Augusto {Cardich}.']},
                {'titulo': '5.3.2 SEMINÓMADAS: HORTICULTORES',
                 'items': ['{Guitarrero} (Áncash): primeros indicios de '
                           '{agricultura} en el Perú, estudiados por Thomas '
                           '{Lynch}.',
                           '{Paracas} (Ica): recolectores; se registran '
                           'tomatillos, yuca y {algodón}.']},
                {'titulo': '5.3.3 SEDENTARIOS: AGRICULTORES',
                 'items': ['{Kotosh} (Huánuco): hacia {2200} a.C., estudiado '
                           'por Julio C. {Tello}. Destaca el Templo de las '
                           'Manos {Cruzadas}, considerado el primer '
                           'monumento religioso.',
                           'El periodo se denomina {precerámico} porque aún '
                           'no se conocía la {cerámica}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Según Hrdlicka, el poblamiento de América se '
                           'produjo a través del {Estrecho de Bering}.',
                           'Kotosh fue estudiado por {Julio C. Tello}.',
                           'El periodo se denomina precerámico porque {Aún '
                           'no se conocía la cerámica}.',
                           'El chaco representado en Toquepala consistía en '
                           '{Una caza ritual colectiva}.',
                           'El periodo de los nómadas andinos se caracterizó '
                           'por ser {Recolectores, cazadores y pescadores}.',
                           'En Paracas, durante el precerámico, se registró '
                           'la recolección de {Tomatillos, yuca y '
                           'algodón}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La teoría autoctonista del poblamiento americano '
                           'fue sostenida por {Florentino Ameghino}.',
                           'La teoría autoctonista fue rebatida en 1908 por '
                           '{Alex Hrdlicka}.',
                           'La teoría de origen oceánico fue sustentada por '
                           '{Paul Rivet}.',
                           'La teoría de origen australiano se atribuye a '
                           '{Mendes Correa}.',
                           'Los restos líticos más antiguos del Perú se '
                           'hallaron en {Paccaicasa}.',
                           'El arte rupestre más antiguo del Perú '
                           'corresponde a {Toquepala}.',
                           'Los primeros restos óseos humanos del Perú se '
                           'encontraron en {Lauricocha}.',
                           'Los primeros indicios de agricultura en el Perú '
                           'se hallaron en {Guitarrero}.',
                           'El Templo de las Manos Cruzadas pertenece a '
                           '{Kotosh}.',
                           'Ameghino sostuvo que los restos fósiles '
                           'correspondían a la Era {Terciaria}.',
                           'Guitarrero se ubica en el actual departamento de '
                           '{Áncash}.',
                           'Paccaicasa se ubica en {Ayacucho}.',
                           'La teoría de Paul Rivet propone una procedencia '
                           'melanésica y {Polinésica}.',
                           'Toquepala se ubica en el departamento de '
                           '{Tacna}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['El poblamiento del continente americano se '
                           'remonta, según algunas teorías, hasta '
                           'aproximadamente {60 000} a.C.',
                           'Paul Rivet planteó que los navegantes '
                           'polinésicos llegaron a Sudamérica pasando por la '
                           'isla de {Pascua}, impulsados por la corriente '
                           'Sur Ecuatorial.',
                           'En Lauricocha se hallaron los restos óseos de '
                           'once esqueletos humanos, con una antigüedad '
                           'aproximada de {9500} años a.C.',
                           'El sitio de Guitarrero se ubica en el Callejón '
                           'de Huaylas, cerca de {Yungay}.']}],
  'cuadros': [{'titulo': '5.2 TEORÍAS Y AUTORES',
               'encabezados': ['Teoría', 'Autor', 'Año'],
               'filas': [['Autoctonista', '{Florentino Ameghino}', '{1879}'],
                         ['Origen asiático', '{Alex Hrdlicka}', '1908'],
                         ['Origen oceánico', '{Paul Rivet}', '{1943}'],
                         ['Origen australiano', '{Mendes Correa}', '—']]}],
  'preguntas': [{'pregunta': 'La teoría autoctonista del poblamiento '
                             'americano fue sostenida por:',
                 'alternativas': ['Alex Hrdlicka',
                                  'Florentino Ameghino',
                                  'Paul Rivet',
                                  'Mendes Correa',
                                  'Julio C. Tello'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría autoctonista fue rebatida en 1908 '
                             'por:',
                 'alternativas': ['Paul Rivet',
                                  'Alex Hrdlicka',
                                  'Thomas Lynch',
                                  'Richard MacNeish',
                                  'Augusto Cardich'],
                 'correcta': 'B'},
                {'pregunta': 'Según Hrdlicka, el poblamiento de América se '
                             'produjo a través del:',
                 'alternativas': ['Océano Pacífico',
                                  'Estrecho de Bering',
                                  'Océano Atlántico',
                                  'Istmo de Panamá',
                                  'Mar de Behring meridional'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de origen oceánico fue sustentada '
                             'por:',
                 'alternativas': ['Ameghino',
                                  'Paul Rivet',
                                  'Mendes Correa',
                                  'Hrdlicka',
                                  'Uhle'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de origen australiano se atribuye a:',
                 'alternativas': ['Paul Rivet',
                                  'Mendes Correa',
                                  'Ameghino',
                                  'Hrdlicka',
                                  'Lynch'],
                 'correcta': 'B'},
                {'pregunta': 'Los restos líticos más antiguos del Perú se '
                             'hallaron en:',
                 'alternativas': ['Lauricocha',
                                  'Paccaicasa',
                                  'Toquepala',
                                  'Guitarrero',
                                  'Kotosh'],
                 'correcta': 'B'},
                {'pregunta': 'El arte rupestre más antiguo del Perú '
                             'corresponde a:',
                 'alternativas': ['Paccaicasa',
                                  'Toquepala',
                                  'Lauricocha',
                                  'Kotosh',
                                  'Paracas'],
                 'correcta': 'B'},
                {'pregunta': 'Los primeros restos óseos humanos del Perú se '
                             'encontraron en:',
                 'alternativas': ['Paccaicasa',
                                  'Toquepala',
                                  'Lauricocha',
                                  'Guitarrero',
                                  'Chilca'],
                 'correcta': 'C'},
                {'pregunta': 'Los primeros indicios de agricultura en el '
                             'Perú se hallaron en:',
                 'alternativas': ['Kotosh',
                                  'Guitarrero',
                                  'Lauricocha',
                                  'Toquepala',
                                  'Paccaicasa'],
                 'correcta': 'B'},
                {'pregunta': 'El Templo de las Manos Cruzadas pertenece a:',
                 'alternativas': ['Caral',
                                  'Kotosh',
                                  'Chavín',
                                  'Sechín',
                                  'Paracas'],
                 'correcta': 'B'},
                {'pregunta': 'Kotosh fue estudiado por:',
                 'alternativas': ['Max Uhle',
                                  'Julio C. Tello',
                                  'Rafael Larco',
                                  'Ruth Shady',
                                  'Federico Kauffmann'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo se denomina precerámico porque:',
                 'alternativas': ['No se conocía la agricultura',
                                  'Aún no se conocía la cerámica',
                                  'No existía la textilería',
                                  'No había arquitectura',
                                  'No se domesticaban animales'],
                 'correcta': 'B'},
                {'pregunta': 'El chaco representado en Toquepala consistía '
                             'en:',
                 'alternativas': ['Una ceremonia funeraria',
                                  'Una caza ritual colectiva',
                                  'Un ritual de siembra',
                                  'Una danza guerrera',
                                  'Un intercambio comercial'],
                 'correcta': 'B'},
                {'pregunta': 'Ameghino sostuvo que los restos fósiles '
                             'correspondían a la Era:',
                 'alternativas': ['Cuaternaria',
                                  'Terciaria',
                                  'Secundaria',
                                  'Primaria',
                                  'Precámbrica'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo de los nómadas andinos se '
                             'caracterizó por ser:',
                 'alternativas': ['Agricultores sedentarios',
                                  'Recolectores, cazadores y pescadores',
                                  'Ganaderos y alfareros',
                                  'Comerciantes',
                                  'Metalurgistas'],
                 'correcta': 'B'},
                {'pregunta': 'Guitarrero se ubica en el actual departamento '
                             'de:',
                 'alternativas': ['Ayacucho',
                                  'Áncash',
                                  'Huánuco',
                                  'Tacna',
                                  'Ica'],
                 'correcta': 'B'},
                {'pregunta': 'Paccaicasa se ubica en:',
                 'alternativas': ['Áncash',
                                  'Ayacucho',
                                  'Tacna',
                                  'Huánuco',
                                  'Lima'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de Paul Rivet propone una '
                             'procedencia melanésica y:',
                 'alternativas': ['Asiática',
                                  'Polinésica',
                                  'Australiana',
                                  'Africana',
                                  'Europea'],
                 'correcta': 'B'},
                {'pregunta': 'Toquepala se ubica en el departamento de:',
                 'alternativas': ['Ica',
                                  'Tacna',
                                  'Arequipa',
                                  'Moquegua',
                                  'Puno'],
                 'correcta': 'B'},
                {'pregunta': 'En Paracas, durante el precerámico, se '
                             'registró la recolección de:',
                 'alternativas': ['Maíz y quinua',
                                  'Tomatillos, yuca y algodón',
                                  'Papa y oca',
                                  'Trigo y cebada',
                                  'Coca y ají únicamente'],
                 'correcta': 'B'}]},
 {'num': 6,
  'titulo': 'Culturas preincas',
  'secciones': [{'titulo': '6.1 CIVILIZACIÓN CARAL',
                 'items': ['Considerada la civilización más {antigua} de '
                           'América, ubicada en el valle de {Supe} '
                           '(Barranca, Lima).',
                           'Fue investigada por la arqueóloga {Ruth Shady}. '
                           'Corresponde al periodo {precerámico} tardío.']},
                {'titulo': '6.2.1 CHAVÍN (Horizonte Temprano)',
                 'items': ['Su capital, {Chavín de Huántar}, se ubica en '
                           'Áncash, a orillas del río {Mosna}, en el flanco '
                           'oriental de la Cordillera {Blanca}.',
                           'Fue descubierta y estudiada por Julio C. '
                           '{Tello}, quien la llamó «cultura {matriz} de la '
                           'civilización andina».',
                           'Su organización política fue {teocrática}: la '
                           'autoridad política derivaba de lo {religioso}. '
                           'Su sociedad fue {clasista}.',
                           'Monumentos líticos: el {Lanzón} monolítico, la '
                           'estela {Raimondi}, el obelisco {Tello} y las '
                           'cabezas {clavas}, guardianes del templo.']},
                {'titulo': '6.2.2 PARACAS',
                 'items': ['Se ubicó en el departamento de {Ica}, provincia '
                           'de Pisco, en la bahía de {Paracas}. Fue '
                           'descubierta por Julio C. {Tello}.',
                           'Paracas {Cavernas}: cuenca del río Ica, capital '
                           '{Tajahuana}, con influencia {Chavín}. Cerámica '
                           '{polícroma}, pintada en {post-cocción}.',
                           'Paracas {Necrópolis}: valle de Pisco, capital '
                           '{Topará}. Cerámica {monocroma}, pintada en '
                           '{pre-cocción}.',
                           'Destacaron por sus {mantos} bordados y por las '
                           '{trepanaciones} craneanas.']},
                {'titulo': '6.3 INTERMEDIO TEMPRANO',
                 'items': ['{Nasca} (300 a.C. – 600 d.C.): departamento de '
                           'Ica. Destacan las {líneas} de Nasca, estudiadas '
                           'por María {Reiche}, y los acueductos de '
                           '{Cantalloc}.',
                           '{Mochica}: costa norte, valles de Moche y '
                           'Chicama. Cerámica {realista} o retrato y '
                           '{escultórica}. Destaca el Señor de {Sipán}.']},
                {'titulo': '6.4 y 6.5 HORIZONTE MEDIO E INTERMEDIO TARDÍO',
                 'items': ['{Tiahuanaco}: altiplano del lago {Titicaca}. '
                           'Destaca la Portada del {Sol}.',
                           '{Wari}: primer {imperio} andino, con capital en '
                           'Ayacucho. Impuso el urbanismo planificado.',
                           '{Chimú}: costa norte, capital {Chan Chan}, la '
                           'ciudad de {barro} más grande de América. '
                           'Destacaron en {orfebrería}.',
                           '{Chanca}: región de Apurímac y Ayacucho; fueron '
                           'derrotados por los {incas}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La civilización más antigua de América es '
                           '{Caral}.',
                           'Julio C. Tello denominó a Chavín como la cultura '
                           '{Matriz de la civilización andina}.',
                           'La cerámica de Paracas Cavernas es {Polícroma en '
                           'post-cocción}.',
                           'Paracas destacó notablemente por sus '
                           '{Trepanaciones craneanas y mantos bordados}.',
                           'Las líneas de Nasca fueron estudiadas durante '
                           'décadas por {María Reiche}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['Caral fue investigada principalmente por {Ruth '
                           'Shady}.',
                           'Chavín de Huántar se ubica en el departamento de '
                           '{Áncash}.',
                           'La organización política de Chavín fue '
                           '{Teocrática}.',
                           'Las cabezas clavas eran consideradas {Guardianes '
                           'del templo}.',
                           'La capital de Paracas Necrópolis fue {Topará}.',
                           'Los acueductos de Cantalloc pertenecen a la '
                           'cultura {Nasca}.',
                           'La cerámica retrato o realista es característica '
                           'de {Mochica}.',
                           'El Señor de Sipán pertenece a la cultura '
                           '{Mochica}.',
                           'La Portada del Sol corresponde a la cultura '
                           '{Tiahuanaco}.',
                           'El primer imperio andino, con capital en '
                           'Ayacucho, fue {Wari}.',
                           'Chan Chan, la ciudad de barro más grande de '
                           'América, perteneció a {Chimú}.',
                           'Los chancas se desarrollaron principalmente en '
                           '{Apurímac y Ayacucho}.',
                           'Tiahuanaco se desarrolló en el altiplano del '
                           'lago {Titicaca}.',
                           'Paracas se ubicó en la provincia de Pisco, '
                           'departamento de {Ica}.',
                           'El Lanzón monolítico y la estela Raimondi '
                           'pertenecen a {Chavín}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['Caral fue declarada Patrimonio Cultural de la '
                           'Humanidad por la UNESCO en Sevilla, el 28 de '
                           'junio del {2009}.',
                           'En Chavín, Julio C. Tello interpretó la estela '
                           'Raimondi como una imagen del dios {Viracocha} en '
                           'forma de jaguar coronado.',
                           'Paracas se ubicó entre Cañete por el norte y '
                           '{Yauca} por el sur, en la bahía de Paracas, '
                           'departamento de Ica.',
                           'La cultura Mochica se desarrolló en los valles '
                           'de Moche, Chicama y Virú, en el departamento de '
                           '{La Libertad}.',
                           'La capital del imperio Wari, también llamada '
                           'Viñaque, se ubicó cerca de la actual ciudad de '
                           '{Ayacucho}.',
                           'El Estado chimú tuvo su capital en Chan Chan y '
                           'llegó a extenderse desde Tumbes por el norte '
                           'hasta {Carabayllo}, en Lima, por el sur.',
                           'La confederación chanca surgió tras la caída del '
                           'imperio Wari, y sus fundadores míticos fueron '
                           '{Uscovilca} y Ancovilca.']}],
  'cuadros': [{'titulo': '6. CULTURAS Y SUS RASGOS',
               'encabezados': ['Cultura', 'Ubicación', 'Rasgo distintivo'],
               'filas': [['Caral',
                          'Valle de {Supe}',
                          'Civilización más {antigua} de América'],
                         ['Chavín',
                          '{Áncash}',
                          'Cultura {matriz}; cabezas clavas'],
                         ['Paracas',
                          '{Ica}',
                          '{Trepanaciones} craneanas y mantos'],
                         ['Nasca',
                          'Ica',
                          '{Líneas} y acueductos de Cantalloc'],
                         ['Mochica',
                          'Costa {norte}',
                          'Cerámica {retrato}; Señor de Sipán'],
                         ['Tiahuanaco', '{Titicaca}', 'Portada del {Sol}'],
                         ['Wari', '{Ayacucho}', 'Primer {imperio} andino'],
                         ['Chimú',
                          'Costa norte',
                          '{Chan Chan}, ciudad de barro']]}],
  'preguntas': [{'pregunta': 'La civilización más antigua de América es:',
                 'alternativas': ['Chavín',
                                  'Caral',
                                  'Paracas',
                                  'Tiahuanaco',
                                  'Mochica'],
                 'correcta': 'B'},
                {'pregunta': 'Caral fue investigada principalmente por:',
                 'alternativas': ['Julio C. Tello',
                                  'Ruth Shady',
                                  'Max Uhle',
                                  'Rafael Larco',
                                  'María Reiche'],
                 'correcta': 'B'},
                {'pregunta': 'Chavín de Huántar se ubica en el departamento '
                             'de:',
                 'alternativas': ['Ica',
                                  'Áncash',
                                  'Ayacucho',
                                  'La Libertad',
                                  'Huánuco'],
                 'correcta': 'B'},
                {'pregunta': 'Julio C. Tello denominó a Chavín como la '
                             'cultura:',
                 'alternativas': ['Síntesis',
                                  'Matriz de la civilización andina',
                                  'Fusionante',
                                  'Imperial',
                                  'Local'],
                 'correcta': 'B'},
                {'pregunta': 'La organización política de Chavín fue:',
                 'alternativas': ['Democrática',
                                  'Teocrática',
                                  'Militarista',
                                  'Republicana',
                                  'Federal'],
                 'correcta': 'B'},
                {'pregunta': 'Las cabezas clavas eran consideradas:',
                 'alternativas': ['Ofrendas funerarias',
                                  'Guardianes del templo',
                                  'Instrumentos musicales',
                                  'Marcadores astronómicos',
                                  'Sellos de propiedad'],
                 'correcta': 'B'},
                {'pregunta': 'La cerámica de Paracas Cavernas es:',
                 'alternativas': ['Monocroma en pre-cocción',
                                  'Polícroma en post-cocción',
                                  'Escultórica realista',
                                  'Vidriada',
                                  'Bicroma'],
                 'correcta': 'B'},
                {'pregunta': 'La capital de Paracas Necrópolis fue:',
                 'alternativas': ['Tajahuana',
                                  'Topará',
                                  'Cahuachi',
                                  'Pachacamac',
                                  'Sechín'],
                 'correcta': 'B'},
                {'pregunta': 'Paracas destacó notablemente por sus:',
                 'alternativas': ['Acueductos subterráneos',
                                  'Trepanaciones craneanas y mantos bordados',
                                  'Ciudades de barro',
                                  'Portadas monolíticas',
                                  'Quipus'],
                 'correcta': 'B'},
                {'pregunta': 'Las líneas de Nasca fueron estudiadas durante '
                             'décadas por:',
                 'alternativas': ['Ruth Shady',
                                  'María Reiche',
                                  'Julio C. Tello',
                                  'Max Uhle',
                                  'Rafael Larco'],
                 'correcta': 'B'},
                {'pregunta': 'Los acueductos de Cantalloc pertenecen a la '
                             'cultura:',
                 'alternativas': ['Chimú',
                                  'Nasca',
                                  'Mochica',
                                  'Wari',
                                  'Paracas'],
                 'correcta': 'B'},
                {'pregunta': 'La cerámica retrato o realista es '
                             'característica de:',
                 'alternativas': ['Nasca',
                                  'Mochica',
                                  'Chavín',
                                  'Tiahuanaco',
                                  'Chimú'],
                 'correcta': 'B'},
                {'pregunta': 'El Señor de Sipán pertenece a la cultura:',
                 'alternativas': ['Chimú',
                                  'Mochica',
                                  'Nasca',
                                  'Wari',
                                  'Lambayeque'],
                 'correcta': 'B'},
                {'pregunta': 'La Portada del Sol corresponde a la cultura:',
                 'alternativas': ['Wari',
                                  'Tiahuanaco',
                                  'Chavín',
                                  'Chimú',
                                  'Nasca'],
                 'correcta': 'B'},
                {'pregunta': 'El primer imperio andino, con capital en '
                             'Ayacucho, fue:',
                 'alternativas': ['Tiahuanaco',
                                  'Wari',
                                  'Chimú',
                                  'Chavín',
                                  'Inca'],
                 'correcta': 'B'},
                {'pregunta': 'Chan Chan, la ciudad de barro más grande de '
                             'América, perteneció a:',
                 'alternativas': ['Mochica',
                                  'Chimú',
                                  'Wari',
                                  'Lambayeque',
                                  'Nasca'],
                 'correcta': 'B'},
                {'pregunta': 'Los chancas se desarrollaron principalmente '
                             'en:',
                 'alternativas': ['Costa norte',
                                  'Apurímac y Ayacucho',
                                  'Altiplano del Titicaca',
                                  'Valle de Supe',
                                  'Costa sur'],
                 'correcta': 'B'},
                {'pregunta': 'Tiahuanaco se desarrolló en el altiplano del '
                             'lago:',
                 'alternativas': ['Junín',
                                  'Titicaca',
                                  'Parinacochas',
                                  'Chinchaycocha',
                                  'Poopó'],
                 'correcta': 'B'},
                {'pregunta': 'Paracas se ubicó en la provincia de Pisco, '
                             'departamento de:',
                 'alternativas': ['Arequipa',
                                  'Ica',
                                  'Lima',
                                  'Tacna',
                                  'Moquegua'],
                 'correcta': 'B'},
                {'pregunta': 'El Lanzón monolítico y la estela Raimondi '
                             'pertenecen a:',
                 'alternativas': ['Paracas',
                                  'Chavín',
                                  'Tiahuanaco',
                                  'Wari',
                                  'Caral'],
                 'correcta': 'B'}]},
 {'num': 7,
  'titulo': 'Civilización inca',
  'secciones': [{'titulo': '7.1 EL AYLLU',
                 'items': ['Fue la célula básica de la sociedad andina: un '
                           'conjunto de familias unidas por vínculos de '
                           '{parentesco}, territorio y culto a un {ancestro} '
                           'común.',
                           'Sus formas de trabajo colectivo fueron el {ayni} '
                           '(ayuda mutua y recíproca entre familias), la '
                           '{minka} (trabajo comunal en beneficio del ayllu) '
                           'y la {mita} (trabajo por turnos al servicio del '
                           'Estado).']},
                {'titulo': '7.2 y 7.3 LO SOCIAL Y LO POLÍTICO',
                 'items': ['La sociedad inca fue {clasista}. La nobleza se '
                           'dividía en nobleza de {sangre} y nobleza de '
                           '{privilegio}.',
                           'El {Inca} era la máxima autoridad; su esposa '
                           'principal era la {Coya}.',
                           'El {Consejo Imperial} o Tahuantinsuyo Camachic '
                           'asesoraba al Inca. El {Apunchic} era gobernador '
                           'provincial y el {Tucuyricuy} el «que todo lo '
                           've», inspector del imperio.',
                           'El imperio se llamó {Tahuantinsuyo}, «las cuatro '
                           'regiones unidas»: Chinchaysuyo, {Antisuyo}, '
                           'Collasuyo y {Contisuyo}.']},
                {'titulo': '7.5 LO ECONÓMICO',
                 'items': ['La base económica fue la {agricultura}, apoyada '
                           'en los {andenes} y en obras de irrigación.',
                           'Principios que la rigieron: la {reciprocidad} '
                           '(intercambio de trabajo y favores) y la '
                           '{redistribución} (el Estado repartía lo '
                           'acumulado en los {tambos} y collcas).',
                           'La propiedad de la tierra se dividía en tierras '
                           'del {Sol}, del {Inca} y del {pueblo} o ayllu.']},
                {'titulo': '7.6 EXPRESIONES ARTÍSTICAS',
                 'items': ['Arquitectura: sólida, sencilla y {simétrica}. '
                           'Destacan {Machupicchu}, Sacsayhuamán y el '
                           '{Coricancha}.',
                           'Cerámica: destaca el {aríbalo}, de base cónica, '
                           'usado para transportar {chicha}.',
                           'Textilería: los tejidos finos se llamaban '
                           '{cumbi} y los toscos {abasca}.',
                           'El registro de información se hacía mediante los '
                           '{quipus}, a cargo de los {quipucamayocs}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Los depósitos estatales incas donde se '
                           'almacenaban productos se llamaban {Collcas y '
                           'tambos}.',
                           'La tierra en el Tahuantinsuyo se dividía en '
                           'tierras del Sol, del Inca y {Del pueblo o '
                           'ayllu}.',
                           'El recipiente cerámico de base cónica usado para '
                           'la chicha fue {El aríbalo}.',
                           'El templo principal del Cusco, dedicado al Sol, '
                           'fue {El Coricancha}.',
                           'La base de la economía inca fue {La '
                           'agricultura}.',
                           'Los andenes tuvieron como finalidad principal '
                           '{Ampliar y proteger la frontera agrícola}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La célula básica de la sociedad andina fue {El '
                           'ayllu}.',
                           'La ayuda mutua y recíproca entre familias se '
                           'denominaba {Ayni}.',
                           'El trabajo por turnos al servicio del Estado '
                           'inca se llamaba {Mita}.',
                           'El trabajo comunal en beneficio del propio ayllu '
                           'se denominaba {Minka}.',
                           'La esposa principal del Inca recibía el nombre '
                           'de {Coya}.',
                           'El funcionario inspector llamado «el que todo lo '
                           've» fue {Tucuyricuy}.',
                           'El gobernador provincial en el Tahuantinsuyo fue '
                           '{Apunchic}.',
                           'El principio por el cual el Estado repartía lo '
                           'acumulado se denomina {Redistribución}.',
                           'El tejido más fino de los incas se denominaba '
                           '{Cumbi}.',
                           'Los encargados de leer y elaborar los quipus '
                           'fueron los {Quipucamayocs}.',
                           'La nobleza inca se dividía en nobleza de sangre '
                           'y nobleza de {Privilegio}.',
                           'El Consejo Imperial que asesoraba al Inca se '
                           'denominaba {Tahuantinsuyo Camachic}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['La sociedad inca reconocía cinco periodos en su '
                           'evolución histórica, comenzando por uno conocido '
                           'a través de la {tradición oral}.',
                           'El Tahuantinsuyo, como institución, fue '
                           'consolidado por el inca {Pachacútec}.',
                           'El Tucuyricuy, «el que todo lo ve», actuaba como '
                           'los ojos y oídos del {Qhapaq} Inca en las '
                           'provincias.',
                           'El ayllu tenía como jefe al {curaca}, encargado '
                           'de la administración directa del territorio '
                           'comunal.',
                           'Los pueblos como los lupacas, del altiplano, '
                           'mantenían tierras cultivadas también en la '
                           'costa, lo que se conoce como control de {pisos '
                           'ecológicos}.',
                           'La vestimenta de la nobleza inca se llamaba '
                           '{cumbi}, confeccionada con fina lana de vicuña, '
                           'mientras la del pueblo se llamaba abasca.',
                           'Solo las {acllas} estaban autorizadas para tejer '
                           'los ropajes destinados al Inca.']}],
  'cuadros': [{'titulo': '7. FORMAS DE TRABAJO',
               'encabezados': ['Forma', 'Definición'],
               'filas': [['{Ayni}',
                          'Ayuda mutua y {recíproca} entre familias'],
                         ['{Minka}',
                          'Trabajo {comunal} en beneficio del ayllu'],
                         ['{Mita}',
                          'Trabajo por {turnos} al servicio del Estado']]}],
  'preguntas': [{'pregunta': 'La célula básica de la sociedad andina fue:',
                 'alternativas': ['La marka',
                                  'El ayllu',
                                  'El curacazgo',
                                  'La panaca',
                                  'El tambo'],
                 'correcta': 'B'},
                {'pregunta': 'La ayuda mutua y recíproca entre familias se '
                             'denominaba:',
                 'alternativas': ['Minka',
                                  'Ayni',
                                  'Mita',
                                  'Chunca',
                                  'Camayoc'],
                 'correcta': 'B'},
                {'pregunta': 'El trabajo por turnos al servicio del Estado '
                             'inca se llamaba:',
                 'alternativas': ['Ayni',
                                  'Mita',
                                  'Minka',
                                  'Yanaconaje',
                                  'Chaco'],
                 'correcta': 'B'},
                {'pregunta': 'El trabajo comunal en beneficio del propio '
                             'ayllu se denominaba:',
                 'alternativas': ['Mita',
                                  'Minka',
                                  'Ayni',
                                  'Tributo',
                                  'Faena estatal'],
                 'correcta': 'B'},
                {'pregunta': 'La esposa principal del Inca recibía el nombre '
                             'de:',
                 'alternativas': ['Ñusta',
                                  'Coya',
                                  'Palla',
                                  'Aclla',
                                  'Mamacona'],
                 'correcta': 'B'},
                {'pregunta': 'El funcionario inspector llamado «el que todo '
                             'lo ve» fue:',
                 'alternativas': ['Apunchic',
                                  'Tucuyricuy',
                                  'Curaca',
                                  'Amauta',
                                  'Quipucamayoc'],
                 'correcta': 'B'},
                {'pregunta': 'El gobernador provincial en el Tahuantinsuyo '
                             'fue:',
                 'alternativas': ['Tucuyricuy',
                                  'Apunchic',
                                  'Curaca',
                                  'Willac Umu',
                                  'Sinchi'],
                 'correcta': 'B'},
                {'pregunta': '«Tahuantinsuyo» significa:',
                 'alternativas': ['Tierra del Sol',
                                  'Las cuatro regiones unidas',
                                  'El gran camino',
                                  'Casa del Inca',
                                  'Ombligo del mundo'],
                 'correcta': 'B'},
                {'pregunta': 'NO es una de las cuatro regiones del '
                             'Tahuantinsuyo:',
                 'alternativas': ['Chinchaysuyo',
                                  'Antisuyo',
                                  'Collasuyo',
                                  'Contisuyo',
                                  'Chimusuyo'],
                 'correcta': 'E'},
                {'pregunta': 'El principio por el cual el Estado repartía lo '
                             'acumulado se denomina:',
                 'alternativas': ['Reciprocidad',
                                  'Redistribución',
                                  'Tributación',
                                  'Mita',
                                  'Ayni'],
                 'correcta': 'B'},
                {'pregunta': 'Los depósitos estatales incas donde se '
                             'almacenaban productos se llamaban:',
                 'alternativas': ['Pucaras',
                                  'Collcas y tambos',
                                  'Cancha',
                                  'Ushnu',
                                  'Kallanka'],
                 'correcta': 'B'},
                {'pregunta': 'La tierra en el Tahuantinsuyo se dividía en '
                             'tierras del Sol, del Inca y:',
                 'alternativas': ['De los curacas',
                                  'Del pueblo o ayllu',
                                  'De los sacerdotes',
                                  'De los yanaconas',
                                  'Del ejército'],
                 'correcta': 'B'},
                {'pregunta': 'El recipiente cerámico de base cónica usado '
                             'para la chicha fue:',
                 'alternativas': ['El kero',
                                  'El aríbalo',
                                  'El cántaro',
                                  'El paccha',
                                  'El huaco retrato'],
                 'correcta': 'B'},
                {'pregunta': 'El tejido más fino de los incas se denominaba:',
                 'alternativas': ['Abasca',
                                  'Cumbi',
                                  'Chusi',
                                  'Unku',
                                  'Llicllia'],
                 'correcta': 'B'},
                {'pregunta': 'Los encargados de leer y elaborar los quipus '
                             'fueron los:',
                 'alternativas': ['Amautas',
                                  'Quipucamayocs',
                                  'Haravicus',
                                  'Camayocs',
                                  'Chasquis'],
                 'correcta': 'B'},
                {'pregunta': 'El templo principal del Cusco, dedicado al '
                             'Sol, fue:',
                 'alternativas': ['Sacsayhuamán',
                                  'El Coricancha',
                                  'Ollantaytambo',
                                  "Q'enqo",
                                  'Tambomachay'],
                 'correcta': 'B'},
                {'pregunta': 'La base de la economía inca fue:',
                 'alternativas': ['El comercio',
                                  'La agricultura',
                                  'La minería',
                                  'La ganadería exclusivamente',
                                  'La pesca'],
                 'correcta': 'B'},
                {'pregunta': 'Los andenes tuvieron como finalidad principal:',
                 'alternativas': ['Fines militares',
                                  'Ampliar y proteger la frontera agrícola',
                                  'Funciones funerarias',
                                  'Uso ceremonial',
                                  'Control astronómico'],
                 'correcta': 'B'},
                {'pregunta': 'La nobleza inca se dividía en nobleza de '
                             'sangre y nobleza de:',
                 'alternativas': ['Guerra',
                                  'Privilegio',
                                  'Religión',
                                  'Territorio',
                                  'Comercio'],
                 'correcta': 'B'},
                {'pregunta': 'El Consejo Imperial que asesoraba al Inca se '
                             'denominaba:',
                 'alternativas': ['Apunchic',
                                  'Tahuantinsuyo Camachic',
                                  'Willac Umu',
                                  'Curacazgo',
                                  'Panaca'],
                 'correcta': 'B'}]},
 {'num': 8,
  'titulo': 'Mundo medieval y el tránsito al mundo moderno',
  'secciones': [{'titulo': '8.1 EL FEUDALISMO: CONCEPTO',
                 'items': ['Sistema {político}, económico y social que '
                           'predominó en Europa entre los siglos {IX} y '
                           '{XV}.',
                           'Se basó en la posesión de la {tierra} y en '
                           'relaciones personales de dependencia entre '
                           'señores y {vasallos}.']},
                {'titulo': '8.2 y 8.3 ANTECEDENTES Y CARACTERÍSTICAS',
                 'items': ['Surgió tras la caída del Imperio {Romano} de '
                           'Occidente y las invasiones {bárbaras}, que '
                           'obligaron a buscar protección.',
                           'Economía {rural} y {autosuficiente}: el feudo '
                           'producía casi todo lo que consumía.',
                           'Sociedad {estamental} y rígida, con escasa '
                           'movilidad social.',
                           'El poder político quedó {fragmentado} o '
                           'descentralizado entre los señores feudales.']},
                {'titulo': '8.4 ELEMENTOS DEL FEUDALISMO',
                 'items': ['El {señor feudal}: propietario del feudo, '
                           'otorgaba protección y tierras.',
                           'Los {vasallos}: prestaban fidelidad y servicio '
                           'militar mediante el {homenaje}.',
                           'El {feudo}: extensión de tierra entregada a '
                           'cambio de servicios; comprendía la reserva '
                           'señorial y los {mansos}.',
                           'Los {siervos} de la gleba estaban {adscritos} a '
                           'la tierra y no podían abandonarla.']},
                {'titulo': '8.5 al 8.7 EL TRÁNSITO AL MUNDO MODERNO',
                 'items': ['El renacer del comercio y de las ciudades '
                           'favoreció el surgimiento de la {burguesía}, '
                           'formada por comerciantes y artesanos.',
                           'El {capitalismo} mercantil se basó en el '
                           'comercio, la banca y la acumulación de '
                           '{capital}.',
                           'El {Renacimiento} fue el movimiento cultural que '
                           'recuperó la cultura {grecolatina} y colocó al '
                           'ser humano en el centro: el {humanismo}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El feudalismo predominó en Europa entre los '
                           'siglos {IX y XV}.',
                           'La base fundamental del sistema feudal fue {La '
                           'posesión de la tierra}.',
                           'El feudalismo surgió principalmente tras {La '
                           'caída del Imperio Romano de Occidente y las '
                           'invasiones bárbaras}.',
                           'La economía feudal se caracterizó por ser {Rural '
                           'y autosuficiente}.',
                           'El campesino adscrito a la tierra, que no podía '
                           'abandonarla, era el {Siervo de la gleba}.',
                           'El poder político durante el feudalismo se '
                           'caracterizó por estar {Fragmentado o '
                           'descentralizado}.',
                           'La nueva clase social surgida con el renacer del '
                           'comercio y las ciudades fue {La burguesía}.',
                           'La sociedad feudal se caracterizó por ser '
                           '{Estamental y rígida}.',
                           'El movimiento cultural que recuperó la cultura '
                           'grecolatina fue {El Renacimiento}.',
                           'La corriente que colocó al ser humano en el '
                           'centro del pensamiento fue {El humanismo}.',
                           'El capitalismo mercantil se basó principalmente '
                           'en {El comercio, la banca y la acumulación de '
                           'capital}.',
                           'La función social de la nobleza feudal era '
                           '{Guerrear y proteger}.',
                           'La función social del clero en la sociedad '
                           'feudal era {Orar y administrar lo religioso}.',
                           'El feudalismo fue un sistema {Político, '
                           'económico y social}.',
                           'El renacer de las ciudades en la Baja Edad Media '
                           'se relaciona directamente con {La reactivación '
                           'del comercio}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El acto por el cual el vasallo juraba fidelidad '
                           'al señor se llamaba {Homenaje}.',
                           'La extensión de tierra entregada a cambio de '
                           'servicios se denominaba {Feudo}.',
                           'El señor feudal otorgaba a sus vasallos '
                           'principalmente {Protección y tierras}.',
                           'Las parcelas del feudo trabajadas por los '
                           'campesinos se llamaban {Mansos}.',
                           'La burguesía estuvo formada principalmente por '
                           '{Comerciantes y artesanos}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['Económicamente, el feudalismo se caracterizó por '
                           'el {monopolio} de la tierra en manos de los '
                           'señores feudales.',
                           'El señor feudal era dueño absoluto del feudo y '
                           'brindaba protección a sus vasallos a cambio de '
                           'un vínculo de {fidelidad}.',
                           'Los siervos carecían de medios de producción '
                           'propios; poseían solo su {fuerza de trabajo} '
                           'para servir en el feudo.',
                           'En el Renacimiento, Sandro Botticelli es '
                           'reconocido por «El nacimiento de la Venus» y «La '
                           'Primavera», y Miguel Ángel por «El Juicio '
                           'Final», Moisés, David y la {Piedad}.',
                           'Leonardo da Vinci destacó como ingeniero, '
                           'naturalista, pintor e {inventor} del '
                           'Renacimiento.']}],
  'cuadros': [{'titulo': '8. SOCIEDAD FEUDAL',
               'encabezados': ['Estamento', 'Función'],
               'filas': [['{Nobleza}', 'Guerrear y {proteger}'],
                         ['{Clero}', 'Orar y administrar lo {religioso}'],
                         ['{Siervos} y campesinos',
                          '{Trabajar} la tierra']]}],
  'preguntas': [{'pregunta': 'El feudalismo predominó en Europa entre los '
                             'siglos:',
                 'alternativas': ['V y VIII',
                                  'IX y XV',
                                  'XVI y XVIII',
                                  'III y VI',
                                  'XV y XVIII'],
                 'correcta': 'B'},
                {'pregunta': 'La base fundamental del sistema feudal fue:',
                 'alternativas': ['El comercio marítimo',
                                  'La posesión de la tierra',
                                  'La industria textil',
                                  'La banca',
                                  'La minería'],
                 'correcta': 'B'},
                {'pregunta': 'El feudalismo surgió principalmente tras:',
                 'alternativas': ['La Revolución Francesa',
                                  'La caída del Imperio Romano de Occidente '
                                  'y las invasiones bárbaras',
                                  'El descubrimiento de América',
                                  'La peste negra',
                                  'Las Cruzadas'],
                 'correcta': 'B'},
                {'pregunta': 'La economía feudal se caracterizó por ser:',
                 'alternativas': ['Industrial y urbana',
                                  'Rural y autosuficiente',
                                  'Comercial y monetaria',
                                  'Colonial',
                                  'Financiera'],
                 'correcta': 'B'},
                {'pregunta': 'El campesino adscrito a la tierra, que no '
                             'podía abandonarla, era el:',
                 'alternativas': ['Vasallo',
                                  'Siervo de la gleba',
                                  'Burgués',
                                  'Artesano',
                                  'Caballero'],
                 'correcta': 'B'},
                {'pregunta': 'El acto por el cual el vasallo juraba '
                             'fidelidad al señor se llamaba:',
                 'alternativas': ['Investidura',
                                  'Homenaje',
                                  'Tributo',
                                  'Diezmo',
                                  'Censo'],
                 'correcta': 'B'},
                {'pregunta': 'La extensión de tierra entregada a cambio de '
                             'servicios se denominaba:',
                 'alternativas': ['Manso',
                                  'Feudo',
                                  'Villa',
                                  'Burgo',
                                  'Solar'],
                 'correcta': 'B'},
                {'pregunta': 'El poder político durante el feudalismo se '
                             'caracterizó por estar:',
                 'alternativas': ['Centralizado',
                                  'Fragmentado o descentralizado',
                                  'En manos del pueblo',
                                  'Bajo control imperial único',
                                  'Concentrado en las ciudades'],
                 'correcta': 'B'},
                {'pregunta': 'La nueva clase social surgida con el renacer '
                             'del comercio y las ciudades fue:',
                 'alternativas': ['La nobleza',
                                  'La burguesía',
                                  'El clero',
                                  'Los siervos',
                                  'Los caballeros'],
                 'correcta': 'B'},
                {'pregunta': 'La sociedad feudal se caracterizó por ser:',
                 'alternativas': ['Igualitaria',
                                  'Estamental y rígida',
                                  'De alta movilidad social',
                                  'Sin clases',
                                  'Democrática'],
                 'correcta': 'B'},
                {'pregunta': 'El movimiento cultural que recuperó la cultura '
                             'grecolatina fue:',
                 'alternativas': ['La Ilustración',
                                  'El Renacimiento',
                                  'El Romanticismo',
                                  'La Escolástica',
                                  'El Barroco'],
                 'correcta': 'B'},
                {'pregunta': 'La corriente que colocó al ser humano en el '
                             'centro del pensamiento fue:',
                 'alternativas': ['El teocentrismo',
                                  'El humanismo',
                                  'El escolasticismo',
                                  'El positivismo',
                                  'El empirismo'],
                 'correcta': 'B'},
                {'pregunta': 'El capitalismo mercantil se basó '
                             'principalmente en:',
                 'alternativas': ['La agricultura de subsistencia',
                                  'El comercio, la banca y la acumulación de '
                                  'capital',
                                  'La servidumbre',
                                  'El trueque',
                                  'La producción artesanal doméstica'],
                 'correcta': 'B'},
                {'pregunta': 'La función social de la nobleza feudal era:',
                 'alternativas': ['Orar',
                                  'Guerrear y proteger',
                                  'Trabajar la tierra',
                                  'Comerciar',
                                  'Administrar justicia eclesiástica'],
                 'correcta': 'B'},
                {'pregunta': 'La función social del clero en la sociedad '
                             'feudal era:',
                 'alternativas': ['Guerrear',
                                  'Orar y administrar lo religioso',
                                  'Trabajar la tierra',
                                  'Recaudar impuestos',
                                  'Gobernar el feudo'],
                 'correcta': 'B'},
                {'pregunta': 'El señor feudal otorgaba a sus vasallos '
                             'principalmente:',
                 'alternativas': ['Dinero',
                                  'Protección y tierras',
                                  'Títulos nobiliarios exclusivamente',
                                  'Educación',
                                  'Naves comerciales'],
                 'correcta': 'B'},
                {'pregunta': 'Las parcelas del feudo trabajadas por los '
                             'campesinos se llamaban:',
                 'alternativas': ['Reserva señorial',
                                  'Mansos',
                                  'Burgos',
                                  'Villas',
                                  'Ejidos'],
                 'correcta': 'B'},
                {'pregunta': 'El feudalismo fue un sistema:',
                 'alternativas': ['Solo económico',
                                  'Político, económico y social',
                                  'Únicamente militar',
                                  'Exclusivamente religioso',
                                  'Solo jurídico'],
                 'correcta': 'B'},
                {'pregunta': 'La burguesía estuvo formada principalmente '
                             'por:',
                 'alternativas': ['Nobles y caballeros',
                                  'Comerciantes y artesanos',
                                  'Siervos de la gleba',
                                  'Clero regular',
                                  'Militares'],
                 'correcta': 'B'},
                {'pregunta': 'El renacer de las ciudades en la Baja Edad '
                             'Media se relaciona directamente con:',
                 'alternativas': ['El fin del comercio',
                                  'La reactivación del comercio',
                                  'La expansión de la servidumbre',
                                  'El aislamiento de los feudos',
                                  'Las invasiones bárbaras'],
                 'correcta': 'B'}]},
 {'num': 9,
  'titulo': 'Expansión europea',
  'secciones': [{'titulo': '9.1 DESCUBRIMIENTOS GEOGRÁFICOS',
                 'items': ['Causas: la búsqueda de una nueva ruta hacia las '
                           '{Indias} tras la caída de {Constantinopla} en '
                           '{1453} a manos de los turcos.',
                           'Avances técnicos que lo hicieron posible: la '
                           '{brújula}, el {astrolabio} y la carabela.',
                           '{Portugal} y {España} encabezaron la expansión '
                           'ultramarina.']},
                {'titulo': '9.2 y 9.3 COLÓN Y LA CAPITULACIÓN',
                 'items': ['{Cristóbal Colón} propuso llegar a las Indias '
                           'navegando hacia el {occidente}, sosteniendo la '
                           '{esfericidad} de la Tierra.',
                           'Su proyecto fue aceptado por los Reyes Católicos '
                           '{Isabel} de Castilla y {Fernando} de Aragón.',
                           'La {Capitulación} de Santa Fe ({1492}) fue el '
                           'documento que fijó los títulos y beneficios de '
                           'Colón: {Almirante}, virrey y gobernador.']},
                {'titulo': '9.4 LOS VIAJES DE COLÓN',
                 'items': ['Primer viaje ({1492}): zarpó del puerto de '
                           '{Palos} con las naves {Pinta}, Niña y {Santa '
                           'María}. Llegó a la isla {Guanahaní}, a la que '
                           'llamó San Salvador.',
                           'Segundo viaje (1493): llevó colonos y animales; '
                           'fundó {La Isabela}.',
                           'Tercer viaje (1498): llegó a la desembocadura '
                           'del {Orinoco}, tierra firme del continente.',
                           'Cuarto viaje (1502): recorrió las costas de '
                           'América {Central}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El documento que fijó los títulos y beneficios '
                           'de Colón fue {La Capitulación de Santa Fe}.',
                           'Las naves del primer viaje de Colón fueron '
                           '{Pinta, Niña y Santa María}.',
                           'Colón sostenía, para justificar su proyecto, la '
                           '{Esfericidad de la Tierra}.',
                           'Los Reyes Católicos que apoyaron a Colón fueron '
                           '{Isabel de Castilla y Fernando de Aragón}.',
                           'El título que recibió Colón según la '
                           'Capitulación fue {Almirante, virrey y '
                           'gobernador}.',
                           'Instrumento náutico fundamental para la '
                           'orientación en alta mar {La brújula}.',
                           'Los países que encabezaron la expansión '
                           'ultramarina europea fueron {Portugal y España}.',
                           'La causa económica principal de los '
                           'descubrimientos geográficos fue {La búsqueda de '
                           'una nueva ruta a las Indias}.',
                           'El astrolabio servía para {Determinar la latitud '
                           'mediante los astros}.',
                           'En su cuarto viaje, Colón recorrió '
                           'principalmente {Las costas de América '
                           'Central}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La caída de Constantinopla en manos de los '
                           'turcos ocurrió en {1453}.',
                           'La Capitulación de Santa Fe se firmó en el año '
                           '{1492}.',
                           'Colón zarpó en su primer viaje desde el puerto '
                           'de {Palos}.',
                           'La primera isla a la que llegó Colón fue '
                           '{Guanahaní}.',
                           'En su tercer viaje, Colón llegó a la '
                           'desembocadura del río {Orinoco}.',
                           'En su segundo viaje, Colón fundó {La Isabela}.',
                           'El cuarto viaje de Colón se realizó en {1502}.',
                           'Colón llamó a la isla de Guanahaní {San '
                           'Salvador}.',
                           'La embarcación ligera y maniobrable usada en los '
                           'viajes de exploración fue {La carabela}.',
                           'El primer viaje de Colón se realizó en el año '
                           '{1492}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['La toma de Constantinopla por los turcos en 1453 '
                           'interrumpió el comercio con el sureste de Europa '
                           'y Asia, obligando a buscar {rutas alternas}.',
                           'El financiamiento del proyecto de Colón contó '
                           'con el apoyo de los banqueros {Pinzón} y del '
                           'judío portugués Luis de Santángel.',
                           'Colón partió el 3 de agosto de 1492 desde el '
                           'puerto de Palos, en la ciudad de {Moguer}.',
                           'La nao Santa María iba al mando de Colón; la '
                           'Pinta, al mando de Martín Alonso Pinzón; y la '
                           'Niña, conducida por {Vicente Yáñez Pinzón}.',
                           'En su segundo viaje, Colón fundó la ciudad de La '
                           'Isabela en homenaje a la reina {Isabel de '
                           'Castilla}.',
                           'El nombre «América» proviene de otro navegante '
                           'italiano, {Américo Vespucio}, quien llegó al '
                           'continente después del segundo viaje de '
                           'Colón.']}],
  'cuadros': [{'titulo': '9.4 LOS CUATRO VIAJES',
               'encabezados': ['Viaje', 'Año', 'Hecho principal'],
               'filas': [['Primero', '{1492}', 'Llegó a {Guanahaní}'],
                         ['Segundo', '{1493}', 'Fundó {La Isabela}'],
                         ['Tercero', '{1498}', 'Desembocadura del {Orinoco}'],
                         ['Cuarto',
                          '{1502}',
                          'Costas de América {Central}']]}],
  'preguntas': [{'pregunta': 'La caída de Constantinopla en manos de los '
                             'turcos ocurrió en:',
                 'alternativas': ['1453', '1492', '1498', '1521', '1532'],
                 'correcta': 'A'},
                {'pregunta': 'El documento que fijó los títulos y beneficios '
                             'de Colón fue:',
                 'alternativas': ['El Tratado de Tordesillas',
                                  'La Capitulación de Santa Fe',
                                  'La Bula Inter Caetera',
                                  'El Requerimiento',
                                  'Las Leyes de Burgos'],
                 'correcta': 'B'},
                {'pregunta': 'La Capitulación de Santa Fe se firmó en el '
                             'año:',
                 'alternativas': ['1453', '1492', '1494', '1498', '1502'],
                 'correcta': 'B'},
                {'pregunta': 'Colón zarpó en su primer viaje desde el puerto '
                             'de:',
                 'alternativas': ['Cádiz',
                                  'Palos',
                                  'Sevilla',
                                  'Lisboa',
                                  'Sanlúcar'],
                 'correcta': 'B'},
                {'pregunta': 'La primera isla a la que llegó Colón fue:',
                 'alternativas': ['La Española',
                                  'Guanahaní',
                                  'Cuba',
                                  'Jamaica',
                                  'Trinidad'],
                 'correcta': 'B'},
                {'pregunta': 'Las naves del primer viaje de Colón fueron:',
                 'alternativas': ['Victoria, Trinidad y Concepción',
                                  'Pinta, Niña y Santa María',
                                  'Santiago, San Antonio y Victoria',
                                  'Nao, Carabela y Galeón',
                                  'La Isabela, La Gallega y La Niña'],
                 'correcta': 'B'},
                {'pregunta': 'Colón sostenía, para justificar su proyecto, '
                             'la:',
                 'alternativas': ['Existencia de un continente intermedio',
                                  'Esfericidad de la Tierra',
                                  'Planitud del mundo',
                                  'Cercanía de África',
                                  'Ruta del Cabo de Buena Esperanza'],
                 'correcta': 'B'},
                {'pregunta': 'Los Reyes Católicos que apoyaron a Colón '
                             'fueron:',
                 'alternativas': ['Carlos I y Juana',
                                  'Isabel de Castilla y Fernando de Aragón',
                                  'Felipe II y María',
                                  'Juan II y Beatriz',
                                  'Carlos V e Isabel de Portugal'],
                 'correcta': 'B'},
                {'pregunta': 'En su tercer viaje, Colón llegó a la '
                             'desembocadura del río:',
                 'alternativas': ['Amazonas',
                                  'Orinoco',
                                  'Magdalena',
                                  'Paraná',
                                  'Misisipi'],
                 'correcta': 'B'},
                {'pregunta': 'El título que recibió Colón según la '
                             'Capitulación fue:',
                 'alternativas': ['Adelantado',
                                  'Almirante, virrey y gobernador',
                                  'Capitán general',
                                  'Corregidor',
                                  'Encomendero'],
                 'correcta': 'B'},
                {'pregunta': 'Instrumento náutico fundamental para la '
                             'orientación en alta mar:',
                 'alternativas': ['El sextante moderno',
                                  'La brújula',
                                  'El telescopio',
                                  'El cronómetro',
                                  'El barómetro'],
                 'correcta': 'B'},
                {'pregunta': 'En su segundo viaje, Colón fundó:',
                 'alternativas': ['Santo Domingo',
                                  'La Isabela',
                                  'La Navidad',
                                  'Panamá',
                                  'Veracruz'],
                 'correcta': 'B'},
                {'pregunta': 'El cuarto viaje de Colón se realizó en:',
                 'alternativas': ['1492', '1502', '1498', '1493', '1519'],
                 'correcta': 'B'},
                {'pregunta': 'Los países que encabezaron la expansión '
                             'ultramarina europea fueron:',
                 'alternativas': ['Inglaterra y Francia',
                                  'Portugal y España',
                                  'Holanda e Italia',
                                  'Alemania y Suecia',
                                  'Francia y España'],
                 'correcta': 'B'},
                {'pregunta': 'Colón llamó a la isla de Guanahaní:',
                 'alternativas': ['La Española',
                                  'San Salvador',
                                  'La Isabela',
                                  'Juana',
                                  'Trinidad'],
                 'correcta': 'B'},
                {'pregunta': 'La causa económica principal de los '
                             'descubrimientos geográficos fue:',
                 'alternativas': ['El exceso de población',
                                  'La búsqueda de una nueva ruta a las '
                                  'Indias',
                                  'La expansión del feudalismo',
                                  'La escasez de tierras agrícolas',
                                  'La difusión del cristianismo únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'El astrolabio servía para:',
                 'alternativas': ['Medir la profundidad del mar',
                                  'Determinar la latitud mediante los astros',
                                  'Calcular la velocidad',
                                  'Orientar el timón',
                                  'Medir la temperatura'],
                 'correcta': 'B'},
                {'pregunta': 'La embarcación ligera y maniobrable usada en '
                             'los viajes de exploración fue:',
                 'alternativas': ['El galeón',
                                  'La carabela',
                                  'La fragata',
                                  'El bergantín',
                                  'La goleta'],
                 'correcta': 'B'},
                {'pregunta': 'El primer viaje de Colón se realizó en el año:',
                 'alternativas': ['1453', '1492', '1493', '1498', '1502'],
                 'correcta': 'B'},
                {'pregunta': 'En su cuarto viaje, Colón recorrió '
                             'principalmente:',
                 'alternativas': ['Las Antillas Mayores',
                                  'Las costas de América Central',
                                  'La costa de Brasil',
                                  'El Río de la Plata',
                                  'La costa del Pacífico'],
                 'correcta': 'B'}]},
 {'num': 10,
  'titulo': 'Conquista del Perú',
  'secciones': [{'titulo': '10.1 y 10.2 LA EMPRESA DE CONQUISTA',
                 'items': ['La empresa la formaron {Francisco Pizarro}, '
                           '{Diego de Almagro} y el sacerdote Hernando de '
                           '{Luque}.',
                           'Primer viaje ({1524}–1525): llegó hasta Puerto '
                           'del {Hambre}; fue un fracaso.',
                           'Segundo viaje (1526–1528): episodio de los '
                           '{Trece} del Gallo en la isla del {Gallo}; se '
                           'llegó hasta {Tumbes}.',
                           'La {Capitulación} de Toledo ({1529}) fue firmada '
                           'por Pizarro con la reina {Isabel} de Portugal; '
                           'lo nombró {gobernador} y capitán general.',
                           'Tercer viaje ({1531}): partió de Panamá; fundó '
                           'San Miguel de {Tangarará}, primera ciudad '
                           'española en el Perú.']},
                {'titulo': '10.2.4 LA CAPTURA DEL INCA',
                 'items': ['El {16} de noviembre de {1532} se produjo la '
                           'captura de {Atahualpa} en la plaza de '
                           '{Cajamarca}.',
                           'El sacerdote {Vicente Valverde} le entregó la '
                           'Biblia en el llamado {Requerimiento}.',
                           'Atahualpa ofreció un cuarto lleno de {oro} y dos '
                           'de {plata} como {rescate}; fue ejecutado en '
                           '{1533}.']},
                {'titulo': '10.3 y 10.4 FUNDACIONES Y RESISTENCIA',
                 'items': ['Pizarro fundó {Lima} el {18} de enero de 1535, '
                           'llamada Ciudad de los {Reyes}.',
                           '{Manco Inca} encabezó la resistencia y sitió el '
                           'Cusco en {1536}. Se replegó a {Vilcabamba}, '
                           'donde se formó el Estado neoinca.',
                           'El último inca de Vilcabamba fue {Túpac Amaru '
                           'I}, ejecutado en {1572} por orden del virrey '
                           '{Toledo}.']},
                {'titulo': '10.5 GUERRA CIVIL ENTRE LOS INVASORES',
                 'items': ['Batalla de las {Salinas} (1538): Pizarro venció '
                           'a {Almagro}.',
                           'Batalla de {Chupas} (1542): derrota de Almagro '
                           '«el Mozo».',
                           'Batalla de {Añaquito} (1546): muerte del primer '
                           'virrey {Blasco Núñez de Vela}.',
                           'Batalla de {Jaquijahuana} (1548): derrota y '
                           'ejecución de Gonzalo {Pizarro}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Los socios de la empresa de conquista del Perú '
                           'fueron {Pizarro, Almagro y Luque}.',
                           'La Capitulación de Toledo nombró a Pizarro '
                           '{Gobernador y capitán general}.',
                           'La captura de Atahualpa se produjo el {16 de '
                           'noviembre de 1532}.',
                           'La primera ciudad española fundada en el Perú '
                           'fue {San Miguel de Tangarará}.',
                           'Lima fue fundada por Pizarro el {18 de enero de '
                           '1535}.',
                           'La ejecución de Túpac Amaru I fue ordenada por '
                           'el virrey {Francisco de Toledo}.',
                           'En la batalla de Jaquijahuana (1548) fue '
                           'derrotado {Gonzalo Pizarro}.',
                           'El primer viaje de la conquista llegó hasta '
                           '{Puerto del Hambre}.',
                           'El rescate ofrecido por Atahualpa consistió en '
                           '{Un cuarto de oro y dos de plata}.',
                           'El acto formal de sometimiento leído a Atahualpa '
                           'se conoce como {El Requerimiento}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El episodio de los Trece del Gallo ocurrió '
                           'durante el {Segundo viaje}.',
                           'La Capitulación de Toledo se firmó en el año '
                           '{1529}.',
                           'La captura del Inca ocurrió en la plaza de '
                           '{Cajamarca}.',
                           'El sacerdote que entregó la Biblia a Atahualpa '
                           'fue {Vicente Valverde}.',
                           'El Inca que encabezó la resistencia y sitió el '
                           'Cusco en 1536 fue {Manco Inca}.',
                           'El Estado neoinca de resistencia se estableció '
                           'en {Vilcabamba}.',
                           'El último inca de Vilcabamba, ejecutado en 1572, '
                           'fue {Túpac Amaru I}.',
                           'En la batalla de las Salinas (1538) fue '
                           'derrotado {Diego de Almagro}.',
                           'El primer virrey del Perú, muerto en la batalla '
                           'de Añaquito, fue {Blasco Núñez de Vela}.',
                           'El tercer viaje de la conquista partió de Panamá '
                           'en el año {1531}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['En el primer viaje de la conquista, Pizarro '
                           'partió de Panamá el 14 de noviembre de 1524 con '
                           'permiso del gobernador {Pedrarias} Dávila.',
                           'En el segundo viaje participó el piloto '
                           'profesional {Bartolomé Ruiz}, quien guio la '
                           'expedición por la costa.',
                           'La Capitulación de Toledo asignó a Pizarro un '
                           'sueldo anual de 725 000 maravedíes, y a Diego de '
                           'Almagro el título de gobernador de la {Fortaleza '
                           'de Tumbes}.',
                           'Hernando de Luque fue nombrado vicario de Tumbes '
                           'y {Protector} de los indios en la Capitulación '
                           'de Toledo.',
                           'La primera ciudad española en el Perú, San '
                           'Miguel, se fundó en 1532 a orillas del río '
                           '{Chira}, en el valle de Tangarará.',
                           'Antes de ser ejecutado, Atahualpa aceptó el '
                           'bautismo cristiano, adoptando el nombre de {Juan '
                           'Francisco Atahuallpa}.',
                           'Tras la captura del Inca, los españoles fueron '
                           'hostilizados en su avance por las fuerzas del '
                           'general atahualpista {Quisquis}.',
                           'El Virreinato del Perú fue creado el 20 de '
                           'noviembre de 1542 mediante las llamadas {Nuevas '
                           'Leyes} del rey Carlos V.',
                           'La Capitulación de Ayacucho puso fin a la guerra '
                           'civil entre Gonzalo Pizarro y el sacerdote '
                           '{Pedro de la Gasca}, enviado por el rey con el '
                           'título de Pacificador.']}],
  'cuadros': [{'titulo': '10.5 BATALLAS DE LAS GUERRAS CIVILES',
               'encabezados': ['Batalla', 'Año', 'Resultado'],
               'filas': [['Las {Salinas}', '{1538}', 'Derrota de {Almagro}'],
                         ['{Chupas}',
                          '1542',
                          'Derrota de Almagro «el {Mozo}»'],
                         ['{Añaquito}',
                          '1546',
                          'Muerte del virrey {Núñez de Vela}'],
                         ['{Jaquijahuana}',
                          '{1548}',
                          'Derrota de {Gonzalo Pizarro}']]}],
  'preguntas': [{'pregunta': 'Los socios de la empresa de conquista del Perú '
                             'fueron:',
                 'alternativas': ['Pizarro, Cortés y Luque',
                                  'Pizarro, Almagro y Luque',
                                  'Pizarro, Valverde y Soto',
                                  'Almagro, Toledo y Luque',
                                  'Pizarro, Alvarado y Belalcázar'],
                 'correcta': 'B'},
                {'pregunta': 'El episodio de los Trece del Gallo ocurrió '
                             'durante el:',
                 'alternativas': ['Primer viaje',
                                  'Segundo viaje',
                                  'Tercer viaje',
                                  'Cuarto viaje',
                                  'Viaje de regreso'],
                 'correcta': 'B'},
                {'pregunta': 'La Capitulación de Toledo se firmó en el año:',
                 'alternativas': ['1524', '1529', '1531', '1532', '1535'],
                 'correcta': 'B'},
                {'pregunta': 'La Capitulación de Toledo nombró a Pizarro:',
                 'alternativas': ['Virrey del Perú',
                                  'Gobernador y capitán general',
                                  'Adelantado de Nueva Toledo',
                                  'Almirante',
                                  'Corregidor'],
                 'correcta': 'B'},
                {'pregunta': 'La captura de Atahualpa se produjo el:',
                 'alternativas': ['18 de enero de 1535',
                                  '16 de noviembre de 1532',
                                  '26 de julio de 1533',
                                  '6 de diciembre de 1534',
                                  '15 de agosto de 1536'],
                 'correcta': 'B'},
                {'pregunta': 'La captura del Inca ocurrió en la plaza de:',
                 'alternativas': ['Cusco',
                                  'Cajamarca',
                                  'Tumbes',
                                  'Piura',
                                  'Jauja'],
                 'correcta': 'B'},
                {'pregunta': 'El sacerdote que entregó la Biblia a Atahualpa '
                             'fue:',
                 'alternativas': ['Hernando de Luque',
                                  'Vicente Valverde',
                                  'Bartolomé de las Casas',
                                  'Jerónimo de Loayza',
                                  'Toribio de Mogrovejo'],
                 'correcta': 'B'},
                {'pregunta': 'La primera ciudad española fundada en el Perú '
                             'fue:',
                 'alternativas': ['Lima',
                                  'San Miguel de Tangarará',
                                  'Jauja',
                                  'Cusco español',
                                  'Trujillo'],
                 'correcta': 'B'},
                {'pregunta': 'Lima fue fundada por Pizarro el:',
                 'alternativas': ['16 de noviembre de 1532',
                                  '18 de enero de 1535',
                                  '26 de junio de 1541',
                                  '6 de abril de 1538',
                                  '9 de diciembre de 1824'],
                 'correcta': 'B'},
                {'pregunta': 'El Inca que encabezó la resistencia y sitió el '
                             'Cusco en 1536 fue:',
                 'alternativas': ['Atahualpa',
                                  'Manco Inca',
                                  'Túpac Amaru I',
                                  'Huáscar',
                                  'Sayri Túpac'],
                 'correcta': 'B'},
                {'pregunta': 'El Estado neoinca de resistencia se estableció '
                             'en:',
                 'alternativas': ['Cajamarca',
                                  'Vilcabamba',
                                  'Ollantaytambo',
                                  'Vitcos únicamente',
                                  'Chachapoyas'],
                 'correcta': 'B'},
                {'pregunta': 'El último inca de Vilcabamba, ejecutado en '
                             '1572, fue:',
                 'alternativas': ['Manco Inca',
                                  'Túpac Amaru I',
                                  'Sayri Túpac',
                                  'Titu Cusi Yupanqui',
                                  'Paullu Inca'],
                 'correcta': 'B'},
                {'pregunta': 'La ejecución de Túpac Amaru I fue ordenada por '
                             'el virrey:',
                 'alternativas': ['Blasco Núñez de Vela',
                                  'Francisco de Toledo',
                                  'Andrés Hurtado de Mendoza',
                                  'Antonio de Mendoza',
                                  'Pedro de la Gasca'],
                 'correcta': 'B'},
                {'pregunta': 'En la batalla de las Salinas (1538) fue '
                             'derrotado:',
                 'alternativas': ['Gonzalo Pizarro',
                                  'Diego de Almagro',
                                  'Almagro el Mozo',
                                  'Núñez de Vela',
                                  'Hernando Pizarro'],
                 'correcta': 'B'},
                {'pregunta': 'El primer virrey del Perú, muerto en la '
                             'batalla de Añaquito, fue:',
                 'alternativas': ['Francisco de Toledo',
                                  'Blasco Núñez de Vela',
                                  'Andrés Hurtado de Mendoza',
                                  'Pedro de la Gasca',
                                  'Antonio de Mendoza'],
                 'correcta': 'B'},
                {'pregunta': 'En la batalla de Jaquijahuana (1548) fue '
                             'derrotado:',
                 'alternativas': ['Diego de Almagro',
                                  'Gonzalo Pizarro',
                                  'Almagro el Mozo',
                                  'Francisco Pizarro',
                                  'Hernando de Soto'],
                 'correcta': 'B'},
                {'pregunta': 'El primer viaje de la conquista llegó hasta:',
                 'alternativas': ['Tumbes',
                                  'Puerto del Hambre',
                                  'Isla del Gallo',
                                  'Cajamarca',
                                  'Panamá'],
                 'correcta': 'B'},
                {'pregunta': 'El rescate ofrecido por Atahualpa consistió '
                             'en:',
                 'alternativas': ['Un cuarto de plata solamente',
                                  'Un cuarto de oro y dos de plata',
                                  'Tierras y siervos',
                                  'Naves y armas',
                                  'Tributos anuales'],
                 'correcta': 'B'},
                {'pregunta': 'El tercer viaje de la conquista partió de '
                             'Panamá en el año:',
                 'alternativas': ['1524', '1526', '1529', '1531', '1532'],
                 'correcta': 'D'},
                {'pregunta': 'El acto formal de sometimiento leído a '
                             'Atahualpa se conoce como:',
                 'alternativas': ['La Capitulación',
                                  'El Requerimiento',
                                  'Las Ordenanzas',
                                  'La Bula',
                                  'El Testamento'],
                 'correcta': 'B'}]},
 {'num': 11,
  'titulo': 'El periodo colonial peruano',
  'secciones': [{'titulo': '11.1 y 11.2 REPARTIMIENTO Y ENCOMIENDA',
                 'items': ['El {repartimiento} fue el reparto de indígenas '
                           'entre los conquistadores para trabajos y '
                           'servicios.',
                           'La {encomienda} consistió en la entrega de un '
                           'grupo de indígenas a un {encomendero}, quien '
                           'recibía su {tributo} a cambio de protegerlos y '
                           '{evangelizarlos}.',
                           'No otorgaba propiedad sobre la {tierra} ni sobre '
                           'las personas, aunque en la práctica derivó en '
                           'abusos.']},
                {'titulo': '11.3.1 ORDENAMIENTO POLÍTICO',
                 'items': ['En España: el {Rey}, el Consejo de {Indias} y la '
                           'Casa de {Contratación} de Sevilla, que '
                           'controlaba el comercio.',
                           'En América: el {Virrey}, las {Audiencias} '
                           '(máximo tribunal de justicia), los '
                           '{corregidores} y los cabildos.',
                           'El virrey {Francisco de Toledo} organizó el '
                           'virreinato y creó las {reducciones} de indios.']},
                {'titulo': '11.3.2 ORDENAMIENTO ECONÓMICO',
                 'items': ['La actividad principal fue la {minería}, '
                           'destacando {Potosí} (plata) y {Huancavelica} '
                           '(mercurio o azogue).',
                           'La {mita} minera colonial obligaba a los '
                           'indígenas a trabajar por turnos en las minas.',
                           'El comercio fue {monopólico}: solo a través de '
                           'los puertos autorizados y el sistema de {flotas} '
                           'y galeones.',
                           'El principal impuesto sobre la producción minera '
                           'fue el {quinto real}.']},
                {'titulo': '11.3.3 y 11.3.4 LO SOCIAL Y LO EDUCATIVO',
                 'items': ['Sociedad {estamental} basada en el origen '
                           'étnico: españoles, {criollos}, mestizos, '
                           'indígenas y {negros}.',
                           'La educación fue {elitista}. Se crearon colegios '
                           'especiales para hijos de {caciques}, como el '
                           'Colegio de San {Borja} en el Cusco.',
                           'La educación superior estuvo a cargo de las '
                           '{universidades}, como San Marcos ({1551}) y San '
                           'Antonio Abad del Cusco ({1692}).']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La encomienda otorgaba al encomendero el derecho '
                           'a recibir {El tributo de los indígenas}.',
                           'El organismo con sede en España encargado de '
                           'legislar sobre América fue {El Consejo de '
                           'Indias}.',
                           'La institución que controlaba el comercio con '
                           'América, con sede en Sevilla, fue {La Casa de '
                           'Contratación}.',
                           'El máximo tribunal de justicia en América '
                           'colonial fue {La Audiencia}.',
                           'El impuesto sobre la producción minera entregado '
                           'a la Corona fue {El quinto real}.',
                           'La sociedad colonial se organizó de manera '
                           '{Estamental según el origen étnico}.',
                           'El colegio colonial destinado a los hijos de '
                           'caciques en el Cusco fue {San Borja}.',
                           'La mita minera colonial consistió en {Trabajo '
                           'obligatorio por turnos en las minas}.',
                           'El funcionario encargado de cobrar tributos en '
                           'las provincias fue {El corregidor}.',
                           'El sistema de transporte comercial entre España '
                           'y América se basó en {Flotas y galeones}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La entrega de un grupo de indígenas a un español '
                           'a cambio de protegerlos y evangelizarlos se '
                           'llamó {Encomienda}.',
                           'El virrey que organizó el virreinato peruano y '
                           'creó las reducciones fue {Francisco de Toledo}.',
                           'El principal centro minero de plata en el '
                           'virreinato fue {Potosí}.',
                           'Huancavelica fue famosa por la producción de '
                           '{Mercurio o azogue}.',
                           'El comercio colonial se caracterizó por ser '
                           '{Monopólico}.',
                           'Los pueblos donde se concentró a la población '
                           'indígena para controlarla se llamaron '
                           '{Reducciones}.',
                           'La Universidad Nacional de San Antonio Abad del '
                           'Cusco fue fundada en {1692}.',
                           'La Universidad Nacional Mayor de San Marcos fue '
                           'fundada en {1551}.',
                           'La educación colonial se caracterizó por ser '
                           '{Elitista}.',
                           'El repartimiento consistió principalmente en {El '
                           'reparto de indígenas entre los '
                           'conquistadores}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['Entre 1532 y 1824 gobernaron las colonias '
                           'americanas reyes de dos dinastías distintas, '
                           'sucesivamente.',
                           'Al término de su mandato, los virreyes se '
                           'sometían a un proceso llamado {Juicio de '
                           'Residencia} ante el Consejo de Indias.',
                           'La Real Audiencia era un tribunal colegiado '
                           'integrado por oidores, jueces, fiscales y '
                           '{escribanos}.',
                           'Las intendencias reemplazaron a los corregidores '
                           'por decisión de los monarcas {Borbones}, ante el '
                           'descrédito de estos últimos.',
                           'El Perú virreinal estuvo dividido en ocho '
                           '{intendencias}.',
                           'En circunstancias excepcionales se convocaba a '
                           'un Cabildo Abierto, donde los vecinos expresaban '
                           'libremente sus puntos de vista.',
                           'El cerro rico de Potosí, corazón de la minería '
                           'colonial, fue descubierto en el año {1545}.',
                           'La mita minera colonial fue implantada por el '
                           'virrey {Francisco de Toledo}.',
                           'Entre los principales impuestos coloniales '
                           'figuraban el almojarifazgo, la alcabala, el '
                           'diezmo, la media anata y la {avería}.',
                           'La sociedad virreinal se organizó en estratos: '
                           'nobleza, clase media, bajo pueblo y '
                           '{aborígenes}, cada uno con derechos distintos.',
                           'Desde 1552, una disposición eclesiástica ordenó '
                           'la creación de escuelas primarias en todas las '
                           '{catedrales}.',
                           'La Universidad de San Marcos fue fundada '
                           'originalmente como Real y Pontificia '
                           'Universidad, tomando su nombre actual en {1574}.',
                           'La Universidad San Antonio Abad del Cusco se '
                           'originó en el seminario cusqueño creado por el '
                           'obispo {Antonio de la Raya}.']}],
  'cuadros': [{'titulo': '11.3 INSTITUCIONES COLONIALES',
               'encabezados': ['Institución', 'Sede', 'Función'],
               'filas': [['Consejo de {Indias}',
                          'España',
                          'Legislar sobre {América}'],
                         ['Casa de {Contratación}',
                          '{Sevilla}',
                          'Controlar el {comercio}'],
                         ['{Virrey}',
                          'Lima',
                          'Máxima autoridad en {América}'],
                         ['{Audiencia}',
                          'Lima, Cusco',
                          'Máximo tribunal de {justicia}'],
                         ['{Corregidor}',
                          'Provincias',
                          'Cobrar {tributos} y gobernar']]}],
  'preguntas': [{'pregunta': 'La entrega de un grupo de indígenas a un '
                             'español a cambio de protegerlos y '
                             'evangelizarlos se llamó:',
                 'alternativas': ['Repartimiento',
                                  'Encomienda',
                                  'Mita',
                                  'Yanaconaje',
                                  'Reducción'],
                 'correcta': 'B'},
                {'pregunta': 'La encomienda otorgaba al encomendero el '
                             'derecho a recibir:',
                 'alternativas': ['La propiedad de la tierra',
                                  'El tributo de los indígenas',
                                  'Títulos nobiliarios',
                                  'El gobierno provincial',
                                  'Las minas del lugar'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo con sede en España encargado de '
                             'legislar sobre América fue:',
                 'alternativas': ['La Casa de Contratación',
                                  'El Consejo de Indias',
                                  'La Audiencia',
                                  'El Cabildo',
                                  'El Consulado'],
                 'correcta': 'B'},
                {'pregunta': 'La institución que controlaba el comercio con '
                             'América, con sede en Sevilla, fue:',
                 'alternativas': ['El Consejo de Indias',
                                  'La Casa de Contratación',
                                  'El Tribunal del Consulado',
                                  'La Audiencia',
                                  'La Real Hacienda'],
                 'correcta': 'B'},
                {'pregunta': 'El máximo tribunal de justicia en América '
                             'colonial fue:',
                 'alternativas': ['El Cabildo',
                                  'La Audiencia',
                                  'El Corregimiento',
                                  'El Consulado',
                                  'La Intendencia'],
                 'correcta': 'B'},
                {'pregunta': 'El virrey que organizó el virreinato peruano y '
                             'creó las reducciones fue:',
                 'alternativas': ['Blasco Núñez de Vela',
                                  'Francisco de Toledo',
                                  'Pedro de la Gasca',
                                  'Andrés Hurtado de Mendoza',
                                  'Manuel de Amat'],
                 'correcta': 'B'},
                {'pregunta': 'El principal centro minero de plata en el '
                             'virreinato fue:',
                 'alternativas': ['Huancavelica',
                                  'Potosí',
                                  'Cerro de Pasco',
                                  'Castrovirreyna',
                                  'Hualgayoc'],
                 'correcta': 'B'},
                {'pregunta': 'Huancavelica fue famosa por la producción de:',
                 'alternativas': ['Plata',
                                  'Mercurio o azogue',
                                  'Oro',
                                  'Cobre',
                                  'Estaño'],
                 'correcta': 'B'},
                {'pregunta': 'El impuesto sobre la producción minera '
                             'entregado a la Corona fue:',
                 'alternativas': ['El diezmo',
                                  'El quinto real',
                                  'La alcabala',
                                  'El almojarifazgo',
                                  'El tributo indígena'],
                 'correcta': 'B'},
                {'pregunta': 'El comercio colonial se caracterizó por ser:',
                 'alternativas': ['Libre',
                                  'Monopólico',
                                  'Regional',
                                  'De trueque',
                                  'Descentralizado'],
                 'correcta': 'B'},
                {'pregunta': 'Los pueblos donde se concentró a la población '
                             'indígena para controlarla se llamaron:',
                 'alternativas': ['Encomiendas',
                                  'Reducciones',
                                  'Corregimientos',
                                  'Obrajes',
                                  'Haciendas'],
                 'correcta': 'B'},
                {'pregunta': 'La sociedad colonial se organizó de manera:',
                 'alternativas': ['Igualitaria',
                                  'Estamental según el origen étnico',
                                  'Meritocrática',
                                  'Democrática',
                                  'Sin distinciones legales'],
                 'correcta': 'B'},
                {'pregunta': 'El colegio colonial destinado a los hijos de '
                             'caciques en el Cusco fue:',
                 'alternativas': ['San Marcos',
                                  'San Borja',
                                  'San Pablo',
                                  'Santo Tomás',
                                  'San Bernardo'],
                 'correcta': 'B'},
                {'pregunta': 'La Universidad Nacional de San Antonio Abad '
                             'del Cusco fue fundada en:',
                 'alternativas': ['1551', '1692', '1821', '1571', '1620'],
                 'correcta': 'B'},
                {'pregunta': 'La Universidad Nacional Mayor de San Marcos '
                             'fue fundada en:',
                 'alternativas': ['1492', '1551', '1572', '1692', '1821'],
                 'correcta': 'B'},
                {'pregunta': 'La mita minera colonial consistió en:',
                 'alternativas': ['Un tributo en especies',
                                  'Trabajo obligatorio por turnos en las '
                                  'minas',
                                  'Un préstamo forzoso',
                                  'Una encomienda de indios',
                                  'Un servicio doméstico'],
                 'correcta': 'B'},
                {'pregunta': 'El funcionario encargado de cobrar tributos en '
                             'las provincias fue:',
                 'alternativas': ['El virrey',
                                  'El corregidor',
                                  'El oidor',
                                  'El alcalde mayor',
                                  'El visitador'],
                 'correcta': 'B'},
                {'pregunta': 'La educación colonial se caracterizó por ser:',
                 'alternativas': ['Universal y gratuita',
                                  'Elitista',
                                  'Obligatoria',
                                  'Laica',
                                  'Técnica'],
                 'correcta': 'B'},
                {'pregunta': 'El repartimiento consistió principalmente en:',
                 'alternativas': ['La distribución de tierras entre '
                                  'indígenas',
                                  'El reparto de indígenas entre los '
                                  'conquistadores',
                                  'La entrega de minas',
                                  'La creación de cabildos',
                                  'La fundación de ciudades'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema de transporte comercial entre '
                             'España y América se basó en:',
                 'alternativas': ['Naves individuales libres',
                                  'Flotas y galeones',
                                  'Caravanas terrestres',
                                  'Barcos de vapor',
                                  'Compañías privadas holandesas'],
                 'correcta': 'B'}]},
 {'num': 12,
  'titulo': 'El mundo durante el siglo XVIII',
  'secciones': [{'titulo': '12.1 LA ILUSTRACIÓN',
                 'items': ['Movimiento intelectual del siglo {XVIII}, '
                           'llamado también «Siglo de las {Luces}».',
                           'Sostuvo que la {razón} debía guiar la vida '
                           'humana, por encima de la tradición y la '
                           '{superstición}.',
                           'Principales pensadores: {Montesquieu}, autor de '
                           'la división de {poderes}; {Rousseau}, autor de '
                           '«El contrato social» y la {soberanía} popular; '
                           '{Voltaire}, defensor de la {tolerancia}.',
                           'Sus ideas influyeron directamente en la '
                           'Independencia de {Estados Unidos} y en la '
                           'Revolución {Francesa}.']},
                {'titulo': '12.2 EL DESPOTISMO ILUSTRADO',
                 'items': ['Forma de gobierno {absolutista} que adoptó '
                           'algunas ideas ilustradas sin ceder el {poder}.',
                           'Se resume en la frase: «Todo para el pueblo, '
                           'pero {sin} el pueblo».',
                           'Los monarcas impulsaron reformas en {educación}, '
                           'economía y administración, pero mantuvieron el '
                           'poder {absoluto}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La Ilustración es conocida también como {Siglo '
                           'de las Luces}.',
                           'Para los ilustrados, la vida humana debía '
                           'guiarse por {La razón}.',
                           'Voltaire destacó especialmente por su defensa de '
                           '{La tolerancia}.',
                           'El despotismo ilustrado se resume en la frase '
                           '{«Todo para el pueblo, pero sin el pueblo»}.',
                           'El despotismo ilustrado mantuvo {El poder '
                           'absoluto del monarca}.',
                           'Las ideas ilustradas influyeron directamente en '
                           '{La Independencia de Estados Unidos y la '
                           'Revolución Francesa}.',
                           'Los ilustrados se opusieron principalmente a {La '
                           'superstición y la tradición irracional}.',
                           'Los monarcas del despotismo ilustrado impulsaron '
                           'reformas en {Educación, economía y '
                           'administración}.',
                           'La Ilustración cuestionó fundamentalmente el '
                           'poder basado en {El derecho divino de los '
                           'reyes}.',
                           'El despotismo ilustrado puede definirse como una '
                           'forma de {Absolutismo con reformas ilustradas}.',
                           'La división de poderes propuesta comprende '
                           '{Ejecutivo, legislativo y judicial}.',
                           'La Ilustración se desarrolló principalmente en '
                           '{Europa}.',
                           'Los ilustrados confiaron en el progreso a través '
                           'de {La educación y la ciencia}.',
                           'Una consecuencia política de la Ilustración fue '
                           '{El cuestionamiento del absolutismo}.',
                           'El pensamiento ilustrado se difundió '
                           'principalmente a través de {Los libros, salones '
                           'y la Enciclopedia}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La Ilustración corresponde al siglo {XVIII}.',
                           'La teoría de la división de poderes fue '
                           'formulada por {Montesquieu}.',
                           'El autor de «El contrato social» fue {Rousseau}.',
                           'El principio de la soberanía popular se atribuye '
                           'a {Rousseau}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['La Ilustración fue un movimiento cultural y '
                           'filosófico surgido en Europa durante el {siglo '
                           'XVIII}.',
                           'Los ilustrados exaltaban el poder de la razón '
                           'frente al absolutismo dogmático y confiaban en '
                           'el {progreso}.',
                           'A pesar de su espíritu crítico, los filósofos '
                           'ilustrados no proponían abiertamente cambios '
                           '{revolucionarios} políticos o sociales.']}],
  'cuadros': [{'titulo': '12.1 PENSADORES DE LA ILUSTRACIÓN',
               'encabezados': ['Pensador', 'Aporte principal'],
               'filas': [['{Montesquieu}', 'División de {poderes}'],
                         ['{Rousseau}',
                          '«El contrato social», {soberanía} popular'],
                         ['{Voltaire}',
                          'Defensa de la {tolerancia} religiosa']]}],
  'preguntas': [{'pregunta': 'La Ilustración corresponde al siglo:',
                 'alternativas': ['XVI', 'XVII', 'XVIII', 'XIX', 'XV'],
                 'correcta': 'C'},
                {'pregunta': 'La Ilustración es conocida también como:',
                 'alternativas': ['Siglo de Oro',
                                  'Siglo de las Luces',
                                  'Renacimiento',
                                  'Edad Moderna',
                                  'Barroco'],
                 'correcta': 'B'},
                {'pregunta': 'Para los ilustrados, la vida humana debía '
                             'guiarse por:',
                 'alternativas': ['La tradición',
                                  'La razón',
                                  'La fe',
                                  'La costumbre',
                                  'La autoridad divina'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de la división de poderes fue '
                             'formulada por:',
                 'alternativas': ['Rousseau',
                                  'Montesquieu',
                                  'Voltaire',
                                  'Diderot',
                                  'Locke'],
                 'correcta': 'B'},
                {'pregunta': 'El autor de «El contrato social» fue:',
                 'alternativas': ['Montesquieu',
                                  'Rousseau',
                                  'Voltaire',
                                  'Kant',
                                  'Hume'],
                 'correcta': 'B'},
                {'pregunta': 'El principio de la soberanía popular se '
                             'atribuye a:',
                 'alternativas': ['Montesquieu',
                                  'Rousseau',
                                  'Voltaire',
                                  'Adam Smith',
                                  'Bossuet'],
                 'correcta': 'B'},
                {'pregunta': 'Voltaire destacó especialmente por su defensa '
                             'de:',
                 'alternativas': ['La monarquía absoluta',
                                  'La tolerancia',
                                  'El feudalismo',
                                  'La censura',
                                  'El derecho divino'],
                 'correcta': 'B'},
                {'pregunta': 'El despotismo ilustrado se resume en la frase:',
                 'alternativas': ['«El Estado soy yo»',
                                  '«Todo para el pueblo, pero sin el pueblo»',
                                  '«Libertad, igualdad, fraternidad»',
                                  '«El poder al pueblo»',
                                  '«Dios lo quiere»'],
                 'correcta': 'B'},
                {'pregunta': 'El despotismo ilustrado mantuvo:',
                 'alternativas': ['La república',
                                  'El poder absoluto del monarca',
                                  'La democracia parlamentaria',
                                  'El gobierno del pueblo',
                                  'La teocracia'],
                 'correcta': 'B'},
                {'pregunta': 'Las ideas ilustradas influyeron directamente '
                             'en:',
                 'alternativas': ['La caída de Constantinopla',
                                  'La Independencia de Estados Unidos y la '
                                  'Revolución Francesa',
                                  'El descubrimiento de América',
                                  'El feudalismo',
                                  'Las Cruzadas'],
                 'correcta': 'B'},
                {'pregunta': 'Los ilustrados se opusieron principalmente a:',
                 'alternativas': ['La razón y la ciencia',
                                  'La superstición y la tradición irracional',
                                  'El progreso',
                                  'La educación',
                                  'El comercio'],
                 'correcta': 'B'},
                {'pregunta': 'Los monarcas del despotismo ilustrado '
                             'impulsaron reformas en:',
                 'alternativas': ['El sistema electoral',
                                  'Educación, economía y administración',
                                  'La abolición de la monarquía',
                                  'La creación de repúblicas',
                                  'La separación Iglesia-Estado plena'],
                 'correcta': 'B'},
                {'pregunta': 'La Ilustración cuestionó fundamentalmente el '
                             'poder basado en:',
                 'alternativas': ['El voto popular',
                                  'El derecho divino de los reyes',
                                  'Los parlamentos',
                                  'Las constituciones',
                                  'Los tratados internacionales'],
                 'correcta': 'B'},
                {'pregunta': 'El despotismo ilustrado puede definirse como '
                             'una forma de:',
                 'alternativas': ['República parlamentaria',
                                  'Absolutismo con reformas ilustradas',
                                  'Democracia directa',
                                  'Anarquía',
                                  'Federalismo'],
                 'correcta': 'B'},
                {'pregunta': 'La división de poderes propuesta comprende:',
                 'alternativas': ['Militar, civil y religioso',
                                  'Ejecutivo, legislativo y judicial',
                                  'Central, regional y local',
                                  'Real, nobiliario y popular',
                                  'Económico, político y social'],
                 'correcta': 'B'},
                {'pregunta': 'La Ilustración se desarrolló principalmente '
                             'en:',
                 'alternativas': ['América',
                                  'Europa',
                                  'Asia',
                                  'África',
                                  'Oceanía'],
                 'correcta': 'B'},
                {'pregunta': 'Los ilustrados confiaron en el progreso a '
                             'través de:',
                 'alternativas': ['La guerra',
                                  'La educación y la ciencia',
                                  'La conquista',
                                  'La tradición',
                                  'El aislamiento'],
                 'correcta': 'B'},
                {'pregunta': 'Una consecuencia política de la Ilustración '
                             'fue:',
                 'alternativas': ['El fortalecimiento del feudalismo',
                                  'El cuestionamiento del absolutismo',
                                  'El retorno al imperio romano',
                                  'La expansión de la servidumbre',
                                  'El fin del comercio'],
                 'correcta': 'B'},
                {'pregunta': '«El contrato social» plantea que el poder '
                             'emana de:',
                 'alternativas': ['Dios',
                                  'El pueblo',
                                  'La nobleza',
                                  'El ejército',
                                  'La Iglesia'],
                 'correcta': 'B'},
                {'pregunta': 'El pensamiento ilustrado se difundió '
                             'principalmente a través de:',
                 'alternativas': ['Los sermones',
                                  'Los libros, salones y la Enciclopedia',
                                  'Las cruzadas',
                                  'Los gremios',
                                  'Los torneos'],
                 'correcta': 'B'}]},
 {'num': 13,
  'titulo': 'Movimientos sociales en el mundo colonial americano',
  'secciones': [{'titulo': '13.1 LAS REFORMAS BORBÓNICAS',
                 'items': ['Conjunto de medidas aplicadas por la dinastía de '
                           'los {Borbones} en el siglo {XVIII} para '
                           'recuperar el control económico y político de las '
                           'colonias.',
                           'Se crearon las {intendencias}, que reemplazaron '
                           'a los {corregimientos}.',
                           'Se crearon los virreinatos de Nueva {Granada} y '
                           'del Río de la {Plata}, reduciendo el territorio '
                           'del virreinato peruano.',
                           'Se incrementaron los {impuestos}, como la '
                           '{alcabala}, y se estableció el {libre} comercio '
                           'entre puertos españoles.',
                           'Se desplazó a los {criollos} de los cargos '
                           'públicos, prefiriendo a los {peninsulares}, lo '
                           'que generó gran descontento.']},
                {'titulo': '13.2.1 REBELIÓN DE JUAN SANTOS ATAHUALPA',
                 'items': ['Se desarrolló desde {1742} en la selva central '
                           '({Gran Pajonal}, Chanchamayo).',
                           'Se proclamó descendiente de los {incas} y buscó '
                           'expulsar a los españoles y restaurar el '
                           '{Tahuantinsuyo}.',
                           'Su rebelión nunca fue {derrotada} militarmente; '
                           'su desaparición sigue siendo un misterio.']},
                {'titulo': '13.2.2 LA REVOLUCIÓN DE TÚPAC AMARU II',
                 'items': ['{José Gabriel Condorcanqui}, cacique de '
                           'Tungasuca, inició la rebelión el {4} de '
                           'noviembre de {1780} con la captura del '
                           'corregidor {Antonio de Arriaga}.',
                           'Causas: los {repartos} mercantiles, la {mita} de '
                           'Potosí, los abusos de los corregidores y las '
                           'reformas {borbónicas}.',
                           'Triunfó en la batalla de {Sangarará}, pero fue '
                           'derrotado en {Checacupe} y Tinta.',
                           'Fue traicionado por {Francisco Santa Cruz} y '
                           'ejecutado en la plaza del Cusco el {18} de mayo '
                           'de {1781}.',
                           'Consecuencias: se prohibió el uso del {quechua} '
                           'en documentos, los títulos de nobleza indígena y '
                           'los Comentarios Reales del Inca {Garcilaso}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Las intendencias reemplazaron a {Los '
                           'corregimientos}.',
                           'Una consecuencia territorial de las reformas '
                           'borbónicas fue {La creación de los virreinatos '
                           'de Nueva Granada y del Río de la Plata}.',
                           'Un rasgo singular de la rebelión de Juan Santos '
                           'Atahualpa fue que {Nunca fue derrotada '
                           'militarmente}.',
                           'La revolución de Túpac Amaru II se inició el {4 '
                           'de noviembre de 1780}.',
                           'Túpac Amaru II fue ejecutado en la plaza del '
                           'Cusco el {18 de mayo de 1781}.',
                           'Una consecuencia cultural de la derrota de Túpac '
                           'Amaru II fue {La prohibición del quechua en '
                           'documentos y de los Comentarios Reales}.',
                           'El impuesto colonial incrementado por las '
                           'reformas borbónicas fue {La alcabala}.',
                           'Juan Santos Atahualpa se proclamó descendiente '
                           'de {Los incas}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['Las reformas borbónicas fueron aplicadas por la '
                           'dinastía de los {Borbones}.',
                           'Las reformas borbónicas desplazaron de los '
                           'cargos públicos a los {Criollos}.',
                           'La rebelión de Juan Santos Atahualpa se inició '
                           'en el año {1742}.',
                           'Juan Santos Atahualpa desarrolló su rebelión en '
                           '{La selva central}.',
                           'El verdadero nombre de Túpac Amaru II fue {José '
                           'Gabriel Condorcanqui}.',
                           'La revolución de Túpac Amaru II se inició con la '
                           'captura del corregidor {Antonio de Arriaga}.',
                           'Túpac Amaru II obtuvo su principal victoria en '
                           'la batalla de {Sangarará}.',
                           'Túpac Amaru II era cacique de {Tungasuca}.',
                           'La obra prohibida tras la rebelión, escrita por '
                           'el Inca Garcilaso, fue {Los Comentarios Reales}.',
                           'Túpac Amaru II fue entregado a los españoles por '
                           'la traición de {Francisco Santa Cruz}.',
                           'Las reformas borbónicas tuvieron como objetivo '
                           'principal {Recuperar el control económico y '
                           'político de las colonias}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['Una de las medidas más importantes de las '
                           'reformas borbónicas fue la creación del '
                           'virreinato del Río de la Plata, en la actual '
                           '{Argentina}.',
                           'Juan Santos Atahualpa se proclamó sucesor del '
                           'último inca del Tahuantinsuyo y extendió su '
                           'rebelión por la {selva central}.',
                           'La rebelión de Juan Santos Atahualpa nunca fue '
                           'derrotada; su líder murió, sin vencer ni ser '
                           'vencido, alrededor del año {1756}.',
                           'Túpac Amaru II fue descendiente de Felipe Túpac '
                           'Amaru, el último inca de {Vilcabamba}, y estudió '
                           'en el Colegio San Francisco de Borja.',
                           'El corregidor Antonio de Arriaga fue ejecutado '
                           'por el zambo {Antonio Oblitas}, su antiguo '
                           'esclavo.',
                           'Túpac Amaru II proclamó la libertad de los '
                           'esclavos negros el {16} de noviembre de 1780.',
                           'Micaela Bastidas fue traicionada por {Ventura '
                           'Landaeta} y conducida junto a Túpac Amaru ante '
                           'el visitador Areche.']}],
  'cuadros': [{'titulo': '13.2 ETAPAS DE LA REVOLUCIÓN DE TÚPAC AMARU II',
               'encabezados': ['Etapa', 'Hecho'],
               'filas': [['Inicio',
                          'Captura del corregidor {Arriaga} ({1780})'],
                         ['Triunfo', 'Batalla de {Sangarará}'],
                         ['Derrota', 'Batallas de {Checacupe} y Tinta'],
                         ['Final', 'Ejecución en el Cusco ({1781})']]}],
  'preguntas': [{'pregunta': 'Las reformas borbónicas fueron aplicadas por '
                             'la dinastía de los:',
                 'alternativas': ['Habsburgo',
                                  'Borbones',
                                  'Trastámara',
                                  'Saboya',
                                  'Braganza'],
                 'correcta': 'B'},
                {'pregunta': 'Las intendencias reemplazaron a:',
                 'alternativas': ['Las audiencias',
                                  'Los corregimientos',
                                  'Los cabildos',
                                  'Las encomiendas',
                                  'Los virreinatos'],
                 'correcta': 'B'},
                {'pregunta': 'Una consecuencia territorial de las reformas '
                             'borbónicas fue:',
                 'alternativas': ['La ampliación del virreinato peruano',
                                  'La creación de los virreinatos de Nueva '
                                  'Granada y del Río de la Plata',
                                  'La independencia de México',
                                  'La anexión de Chile',
                                  'La creación de la Capitanía de Cuba'],
                 'correcta': 'B'},
                {'pregunta': 'Las reformas borbónicas desplazaron de los '
                             'cargos públicos a los:',
                 'alternativas': ['Peninsulares',
                                  'Criollos',
                                  'Indígenas',
                                  'Mestizos',
                                  'Esclavos'],
                 'correcta': 'B'},
                {'pregunta': 'La rebelión de Juan Santos Atahualpa se inició '
                             'en el año:',
                 'alternativas': ['1742', '1780', '1781', '1814', '1821'],
                 'correcta': 'A'},
                {'pregunta': 'Juan Santos Atahualpa desarrolló su rebelión '
                             'en:',
                 'alternativas': ['El altiplano',
                                  'La selva central',
                                  'La costa norte',
                                  'El Cusco',
                                  'Lima'],
                 'correcta': 'B'},
                {'pregunta': 'Un rasgo singular de la rebelión de Juan '
                             'Santos Atahualpa fue que:',
                 'alternativas': ['Fue rápidamente sofocada',
                                  'Nunca fue derrotada militarmente',
                                  'Contó con apoyo español',
                                  'Se limitó a la costa',
                                  'Fue pacífica'],
                 'correcta': 'B'},
                {'pregunta': 'El verdadero nombre de Túpac Amaru II fue:',
                 'alternativas': ['Juan Santos Atahualpa',
                                  'José Gabriel Condorcanqui',
                                  'Mateo Pumacahua',
                                  'Diego Cristóbal Túpac Amaru',
                                  'Francisco Santa Cruz'],
                 'correcta': 'B'},
                {'pregunta': 'La revolución de Túpac Amaru II se inició con '
                             'la captura del corregidor:',
                 'alternativas': ['Francisco Santa Cruz',
                                  'Antonio de Arriaga',
                                  'José Antonio de Areche',
                                  "Ambrosio O'Higgins",
                                  'Agustín de Jáuregui'],
                 'correcta': 'B'},
                {'pregunta': 'La revolución de Túpac Amaru II se inició el:',
                 'alternativas': ['18 de mayo de 1781',
                                  '4 de noviembre de 1780',
                                  '28 de julio de 1821',
                                  '9 de diciembre de 1824',
                                  '1 de agosto de 1814'],
                 'correcta': 'B'},
                {'pregunta': 'Túpac Amaru II obtuvo su principal victoria en '
                             'la batalla de:',
                 'alternativas': ['Checacupe',
                                  'Sangarará',
                                  'Tinta',
                                  'Ayacucho',
                                  'Junín'],
                 'correcta': 'B'},
                {'pregunta': 'Túpac Amaru II fue ejecutado en la plaza del '
                             'Cusco el:',
                 'alternativas': ['4 de noviembre de 1780',
                                  '18 de mayo de 1781',
                                  '28 de julio de 1821',
                                  '6 de agosto de 1824',
                                  '2 de enero de 1782'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las causas de la revolución de Túpac '
                             'Amaru II NO figura:',
                 'alternativas': ['Los repartos mercantiles',
                                  'La mita de Potosí',
                                  'Los abusos de los corregidores',
                                  'Las reformas borbónicas',
                                  'La abolición de la esclavitud'],
                 'correcta': 'E'},
                {'pregunta': 'Una consecuencia cultural de la derrota de '
                             'Túpac Amaru II fue:',
                 'alternativas': ['La difusión del quechua',
                                  'La prohibición del quechua en documentos '
                                  'y de los Comentarios Reales',
                                  'La creación de escuelas indígenas',
                                  'El reconocimiento de la nobleza inca',
                                  'La libertad de imprenta'],
                 'correcta': 'B'},
                {'pregunta': 'Túpac Amaru II era cacique de:',
                 'alternativas': ['Chincheros',
                                  'Tungasuca',
                                  'Azángaro',
                                  'Lampa',
                                  'Acos'],
                 'correcta': 'B'},
                {'pregunta': 'La obra prohibida tras la rebelión, escrita '
                             'por el Inca Garcilaso, fue:',
                 'alternativas': ['Nueva Crónica y Buen Gobierno',
                                  'Los Comentarios Reales',
                                  'La Crónica del Perú',
                                  'Historia del Nuevo Mundo',
                                  'Relación de antigüedades'],
                 'correcta': 'B'},
                {'pregunta': 'El impuesto colonial incrementado por las '
                             'reformas borbónicas fue:',
                 'alternativas': ['El quinto real',
                                  'La alcabala',
                                  'El diezmo',
                                  'El almojarifazgo',
                                  'La primicia'],
                 'correcta': 'B'},
                {'pregunta': 'Túpac Amaru II fue entregado a los españoles '
                             'por la traición de:',
                 'alternativas': ['Antonio de Arriaga',
                                  'Francisco Santa Cruz',
                                  'Mateo Pumacahua',
                                  'Diego Cristóbal',
                                  'Micaela Bastidas'],
                 'correcta': 'B'},
                {'pregunta': 'Las reformas borbónicas tuvieron como objetivo '
                             'principal:',
                 'alternativas': ['Otorgar autonomía a las colonias',
                                  'Recuperar el control económico y político '
                                  'de las colonias',
                                  'Abolir la esclavitud',
                                  'Fundar universidades',
                                  'Promover la independencia'],
                 'correcta': 'B'},
                {'pregunta': 'Juan Santos Atahualpa se proclamó descendiente '
                             'de:',
                 'alternativas': ['Los reyes españoles',
                                  'Los incas',
                                  'Los curacas costeños',
                                  'Los chancas',
                                  'Los chimúes'],
                 'correcta': 'B'}]},
 {'num': 14,
  'titulo': 'Tiempo de las revoluciones',
  'secciones': [{'titulo': '14.1 INDEPENDENCIA DE ESTADOS UNIDOS',
                 'items': ['Las {trece} colonias inglesas de Norteamérica se '
                           'rebelaron contra la metrópoli.',
                           'Causas: los {impuestos} sin representación '
                           'política —«no hay impuestos sin '
                           '{representación}»— y el {Motín} del Té de '
                           'Boston.',
                           'La Declaración de {Independencia} se firmó el '
                           '{4} de julio de {1776}; su principal redactor '
                           'fue Thomas {Jefferson}.',
                           'El primer presidente fue {George Washington}. Se '
                           'estableció una {república} federal y '
                           'presidencialista.',
                           'Consecuencia: sirvió de {ejemplo} a los '
                           'movimientos independentistas de '
                           'Hispanoamérica.']},
                {'titulo': '14.2 LA REVOLUCIÓN FRANCESA',
                 'items': ['Se inició en {1789} con la toma de la {Bastilla} '
                           'el {14} de julio.',
                           'Causas: la crisis {económica}, la desigualdad de '
                           'los {estamentos} y la influencia de la '
                           '{Ilustración}.',
                           'Etapas: la Asamblea {Nacional}, la Convención '
                           '(con el {Terror} y Robespierre) y el '
                           '{Directorio}, que terminó con el golpe de '
                           '{Napoleón}.',
                           'Su lema fue «{Libertad}, igualdad, '
                           '{fraternidad}» y proclamó la Declaración de los '
                           'Derechos del {Hombre} y del Ciudadano.',
                           'Consecuencias: fin del {absolutismo} y del '
                           'régimen feudal, y difusión de las ideas '
                           '{liberales} por Europa y América.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La Declaración de Independencia de Estados '
                           'Unidos se firmó el {4 de julio de 1776}.',
                           'El principal redactor de la Declaración de '
                           'Independencia norteamericana fue {Thomas '
                           'Jefferson}.',
                           'El lema «no hay impuestos sin representación» '
                           'corresponde a {La independencia de Estados '
                           'Unidos}.',
                           'El hecho que precipitó la rebelión de las '
                           'colonias inglesas fue {El Motín del Té de '
                           'Boston}.',
                           'El hecho simbólico del inicio de la Revolución '
                           'Francesa fue {La toma de la Bastilla}.',
                           'El lema de la Revolución Francesa fue '
                           '{«Libertad, igualdad, fraternidad»}.',
                           'El documento fundamental proclamado por la '
                           'Revolución Francesa fue {La Declaración de los '
                           'Derechos del Hombre y del Ciudadano}.',
                           'El Directorio francés terminó con {El golpe de '
                           'Estado de Napoleón}.',
                           'Una consecuencia política central de la '
                           'Revolución Francesa fue {El fin del absolutismo '
                           'y del régimen feudal}.',
                           'La independencia de Estados Unidos influyó en '
                           'Hispanoamérica al {Servir de ejemplo a los '
                           'movimientos independentistas}.',
                           'El sistema de gobierno adoptado por Estados '
                           'Unidos fue {República federal y '
                           'presidencialista}.',
                           'La corriente de pensamiento que influyó '
                           'decisivamente en ambas revoluciones fue {La '
                           'Ilustración}.',
                           'La toma de la Bastilla ocurrió el {14 de julio}.',
                           'La sociedad francesa previa a la revolución '
                           'estaba dividida en {Tres estamentos}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El número de colonias inglesas que se '
                           'independizaron en Norteamérica fue {Trece}.',
                           'El primer presidente de Estados Unidos fue '
                           '{George Washington}.',
                           'La Revolución Francesa se inició en el año '
                           '{1789}.',
                           'La etapa del Terror durante la Revolución '
                           'Francesa estuvo dirigida por {Robespierre}.',
                           'Entre las causas de la Revolución Francesa '
                           'figura {La desigualdad entre los estamentos}.',
                           'El órgano revolucionario francés que juzgó y '
                           'ejecutó al rey fue {La Convención}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['La colonización británica de Norteamérica se '
                           'inició en 1607 con la fundación de {Jamestown}, '
                           'en la actual Virginia.',
                           'El Segundo Congreso Continental, reunido en '
                           'Filadelfia, proclamó la independencia de las '
                           'trece colonias el {4 de julio} de 1776.',
                           'La primera victoria de los colonos '
                           'norteamericanos fue en {Saratoga}, en 1777.',
                           'La batalla de {Yorktown}, en 1781, con apoyo del '
                           'mariscal francés Lafayette, selló la derrota '
                           'británica.',
                           'En 1788 se aprobó la Constitución de la nueva '
                           'república de Estados Unidos, siendo su primer '
                           'presidente {George Washington}.',
                           'La Revolución Francesa estableció la monarquía '
                           'constitucional en 1791, y recién en 1792 se '
                           'abolió la monarquía y se proclamó la '
                           '{República}.',
                           'El periodo revolucionario francés terminó cuando '
                           '{Napoleón Bonaparte} dio un golpe de Estado en '
                           '1799.']}],
  'cuadros': [{'titulo': '14. DOS REVOLUCIONES',
               'encabezados': ['Revolución', 'Año de inicio', 'Aporte'],
               'filas': [['Independencia de {EE.UU.}',
                          '{1776}',
                          'Primera {república} moderna'],
                         ['Revolución {Francesa}',
                          '{1789}',
                          'Derechos del {Hombre} y del Ciudadano']]}],
  'preguntas': [{'pregunta': 'El número de colonias inglesas que se '
                             'independizaron en Norteamérica fue:',
                 'alternativas': ['Diez', 'Trece', 'Quince', 'Doce', 'Once'],
                 'correcta': 'B'},
                {'pregunta': 'La Declaración de Independencia de Estados '
                             'Unidos se firmó el:',
                 'alternativas': ['14 de julio de 1789',
                                  '4 de julio de 1776',
                                  '28 de julio de 1821',
                                  '9 de diciembre de 1824',
                                  '1 de enero de 1800'],
                 'correcta': 'B'},
                {'pregunta': 'El principal redactor de la Declaración de '
                             'Independencia norteamericana fue:',
                 'alternativas': ['George Washington',
                                  'Thomas Jefferson',
                                  'Benjamin Franklin',
                                  'John Adams',
                                  'Alexander Hamilton'],
                 'correcta': 'B'},
                {'pregunta': 'El primer presidente de Estados Unidos fue:',
                 'alternativas': ['Thomas Jefferson',
                                  'George Washington',
                                  'John Adams',
                                  'Benjamin Franklin',
                                  'James Madison'],
                 'correcta': 'B'},
                {'pregunta': 'El lema «no hay impuestos sin representación» '
                             'corresponde a:',
                 'alternativas': ['La Revolución Francesa',
                                  'La independencia de Estados Unidos',
                                  'La independencia del Perú',
                                  'La Ilustración',
                                  'Las reformas borbónicas'],
                 'correcta': 'B'},
                {'pregunta': 'El hecho que precipitó la rebelión de las '
                             'colonias inglesas fue:',
                 'alternativas': ['La toma de la Bastilla',
                                  'El Motín del Té de Boston',
                                  'La batalla de Waterloo',
                                  'El bloqueo continental',
                                  'La Paz de Westfalia'],
                 'correcta': 'B'},
                {'pregunta': 'La Revolución Francesa se inició en el año:',
                 'alternativas': ['1776', '1789', '1799', '1804', '1810'],
                 'correcta': 'B'},
                {'pregunta': 'El hecho simbólico del inicio de la Revolución '
                             'Francesa fue:',
                 'alternativas': ['La ejecución de Luis XVI',
                                  'La toma de la Bastilla',
                                  'El golpe de Napoleón',
                                  'La reunión de los Estados Generales',
                                  'La huida a Varennes'],
                 'correcta': 'B'},
                {'pregunta': 'El lema de la Revolución Francesa fue:',
                 'alternativas': ['«Todo para el pueblo, sin el pueblo»',
                                  '«Libertad, igualdad, fraternidad»',
                                  '«No hay impuestos sin representación»',
                                  '«El Estado soy yo»',
                                  '«Paz, orden y progreso»'],
                 'correcta': 'B'},
                {'pregunta': 'El documento fundamental proclamado por la '
                             'Revolución Francesa fue:',
                 'alternativas': ['La Carta Magna',
                                  'La Declaración de los Derechos del Hombre '
                                  'y del Ciudadano',
                                  'El Bill of Rights',
                                  'El Código de Hammurabi',
                                  'Las Siete Partidas'],
                 'correcta': 'B'},
                {'pregunta': 'La etapa del Terror durante la Revolución '
                             'Francesa estuvo dirigida por:',
                 'alternativas': ['Napoleón',
                                  'Robespierre',
                                  'Danton exclusivamente',
                                  'Luis XVI',
                                  'Lafayette'],
                 'correcta': 'B'},
                {'pregunta': 'El Directorio francés terminó con:',
                 'alternativas': ['La toma de la Bastilla',
                                  'El golpe de Estado de Napoleón',
                                  'La ejecución de Robespierre',
                                  'La restauración borbónica',
                                  'La batalla de Waterloo'],
                 'correcta': 'B'},
                {'pregunta': 'Una consecuencia política central de la '
                             'Revolución Francesa fue:',
                 'alternativas': ['El fortalecimiento del absolutismo',
                                  'El fin del absolutismo y del régimen '
                                  'feudal',
                                  'La restauración del feudalismo',
                                  'La expansión de la servidumbre',
                                  'El retorno de la monarquía absoluta '
                                  'permanente'],
                 'correcta': 'B'},
                {'pregunta': 'La independencia de Estados Unidos influyó en '
                             'Hispanoamérica al:',
                 'alternativas': ['Financiar los ejércitos libertadores',
                                  'Servir de ejemplo a los movimientos '
                                  'independentistas',
                                  'Enviar tropas al Perú',
                                  'Firmar tratados de alianza',
                                  'Abolir la esclavitud'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema de gobierno adoptado por Estados '
                             'Unidos fue:',
                 'alternativas': ['Monarquía constitucional',
                                  'República federal y presidencialista',
                                  'República parlamentaria',
                                  'Confederación monárquica',
                                  'Imperio'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las causas de la Revolución Francesa '
                             'figura:',
                 'alternativas': ['La abundancia económica',
                                  'La desigualdad entre los estamentos',
                                  'La ausencia de impuestos',
                                  'La expansión colonial',
                                  'La unidad social'],
                 'correcta': 'B'},
                {'pregunta': 'La corriente de pensamiento que influyó '
                             'decisivamente en ambas revoluciones fue:',
                 'alternativas': ['El Renacimiento',
                                  'La Ilustración',
                                  'El Romanticismo',
                                  'La Escolástica',
                                  'El Positivismo'],
                 'correcta': 'B'},
                {'pregunta': 'La toma de la Bastilla ocurrió el:',
                 'alternativas': ['4 de julio',
                                  '14 de julio',
                                  '28 de julio',
                                  '9 de diciembre',
                                  '1 de mayo'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano revolucionario francés que juzgó y '
                             'ejecutó al rey fue:',
                 'alternativas': ['La Asamblea Nacional',
                                  'La Convención',
                                  'El Directorio',
                                  'Los Estados Generales',
                                  'El Consulado'],
                 'correcta': 'B'},
                {'pregunta': 'La sociedad francesa previa a la revolución '
                             'estaba dividida en:',
                 'alternativas': ['Dos clases',
                                  'Tres estamentos',
                                  'Cuatro castas',
                                  'Cinco estamentos',
                                  'Sin divisiones legales'],
                 'correcta': 'B'}]},
 {'num': 15,
  'titulo': 'Crisis del orden colonial e independencia',
  'secciones': [{'titulo': '15.1 al 15.4 LA CRISIS DE ESPAÑA',
                 'items': ['En {1808} {Napoleón} invadió España y colocó en '
                           'el trono a su hermano José {Bonaparte}.',
                           'Ante el vacío de poder se formaron las {juntas} '
                           'de gobierno, primero en España y luego en '
                           '{América}.',
                           'En {1812} se promulgó la Constitución de '
                           '{Cádiz}, de carácter {liberal}.']},
                {'titulo': '15.5 LA CORRIENTE LIBERTADORA DEL SUR',
                 'items': ['{José de San Martín} desembarcó en la bahía de '
                           '{Paracas} el {8} de septiembre de {1820}.',
                           'Antes realizó el cruce de los {Andes} y liberó '
                           '{Chile} con la batalla de Maipú.',
                           'Proclamó la Independencia del Perú en la plaza '
                           'de armas de Lima el {28} de julio de {1821}.',
                           'Asumió el gobierno con el título de {Protector} '
                           'y creó la {Biblioteca} Nacional y la Sociedad '
                           '{Patriótica}.']},
                {'titulo': '15.6 LA CONSOLIDACIÓN CON BOLÍVAR',
                 'items': ['Tras la Conferencia de {Guayaquil} (1822) entre '
                           'San Martín y {Bolívar}, el primero se retiró.',
                           '{Simón Bolívar} llegó al Perú en {1823} y '
                           'recibió poderes de {dictador}.',
                           'Batalla de {Junín} ({6} de agosto de 1824): '
                           'victoria de la caballería patriota, sin uso de '
                           'armas de fuego.',
                           'Batalla de {Ayacucho} ({9} de diciembre de '
                           '1824): dirigida por {Antonio José de Sucre}; '
                           'selló la independencia.',
                           'La {Capitulación} de Ayacucho fue firmada por el '
                           'virrey {José de la Serna}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['Napoleón colocó en el trono español a {José '
                           'Bonaparte}.',
                           'El desembarco de San Martín en el Perú ocurrió '
                           'el {8 de septiembre de 1820}.',
                           'La Independencia del Perú fue proclamada el {28 '
                           'de julio de 1821}.',
                           'Institución cultural creada por San Martín {La '
                           'Biblioteca Nacional}.',
                           'La batalla de Junín se libró el {6 de agosto de '
                           '1824}.',
                           'Un rasgo distintivo de la batalla de Junín fue '
                           'que {Se libró sin usar armas de fuego}.',
                           'La batalla de Ayacucho se libró el {9 de '
                           'diciembre de 1824}.',
                           'Ante el vacío de poder por la invasión '
                           'napoleónica se formaron {Las juntas de '
                           'gobierno}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La invasión napoleónica a España se produjo en '
                           '{1808}.',
                           'La Constitución liberal española de 1812 se '
                           'conoce como Constitución de {Cádiz}.',
                           'San Martín desembarcó en el Perú en la bahía de '
                           '{Paracas}.',
                           'San Martín asumió el gobierno del Perú con el '
                           'título de {Protector}.',
                           'La conferencia entre San Martín y Bolívar se '
                           'realizó en {Guayaquil}.',
                           'Bolívar llegó al Perú en el año {1823}.',
                           'La batalla de Ayacucho fue dirigida por {Antonio '
                           'José de Sucre}.',
                           'La Capitulación de Ayacucho fue firmada por el '
                           'virrey {José de la Serna}.',
                           'Antes de llegar al Perú, San Martín liberó '
                           '{Chile}.',
                           'Bolívar recibió en el Perú poderes de '
                           '{Dictador}.',
                           'La proclamación de la Independencia se realizó '
                           'en {La plaza de armas de Lima}.',
                           'La batalla que selló definitivamente la '
                           'independencia del Perú fue {Ayacucho}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['La invasión de Napoleón a España, entre 1808 y '
                           '1813, es un factor externo clave del proceso de '
                           'independencia hispanoamericana.',
                           'Ante la ausencia del poder monárquico español, '
                           'los criollos instauraron {Juntas de Gobierno} '
                           'que reclamaban autogobierno.',
                           'La Constitución de Cádiz fue jurada el {19 de '
                           'marzo} de 1812 bajo el título de Constitución '
                           'Política de la Monarquía Española.',
                           'Entre 1809 y 1810 se formaron juntas '
                           'gubernativas en casi todos los virreinatos '
                           'sudamericanos, excepto en el del {Perú}.',
                           'La proclamación de la Independencia se decidió '
                           'el 15 de julio de 1821, cuando San Martín '
                           'convocó al {Cabildo} de Lima.',
                           'En enero de 1824, Bolívar estableció su cuartel '
                           'general en Pativilca y nombró secretario a '
                           '{Faustino Sánchez Carrión}.']}],
  'cuadros': [{'titulo': '15. BATALLAS DECISIVAS',
               'encabezados': ['Batalla', 'Fecha', 'Jefe patriota'],
               'filas': [['{Junín}', '{6} agosto 1824', '{Bolívar}'],
                         ['{Ayacucho}', '{9} diciembre 1824', '{Sucre}']]}],
  'preguntas': [{'pregunta': 'La invasión napoleónica a España se produjo '
                             'en:',
                 'alternativas': ['1789', '1808', '1812', '1820', '1824'],
                 'correcta': 'B'},
                {'pregunta': 'Napoleón colocó en el trono español a:',
                 'alternativas': ['Fernando VII',
                                  'José Bonaparte',
                                  'Carlos IV',
                                  'Godoy',
                                  'Luis XVIII'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución liberal española de 1812 se '
                             'conoce como Constitución de:',
                 'alternativas': ['Bayona',
                                  'Cádiz',
                                  'Madrid',
                                  'Sevilla',
                                  'Aranjuez'],
                 'correcta': 'B'},
                {'pregunta': 'San Martín desembarcó en el Perú en la bahía '
                             'de:',
                 'alternativas': ['Pisco',
                                  'Paracas',
                                  'Ancón',
                                  'Huacho',
                                  'Callao'],
                 'correcta': 'B'},
                {'pregunta': 'El desembarco de San Martín en el Perú ocurrió '
                             'el:',
                 'alternativas': ['28 de julio de 1821',
                                  '8 de septiembre de 1820',
                                  '9 de diciembre de 1824',
                                  '6 de agosto de 1824',
                                  '20 de septiembre de 1822'],
                 'correcta': 'B'},
                {'pregunta': 'La Independencia del Perú fue proclamada el:',
                 'alternativas': ['8 de septiembre de 1820',
                                  '28 de julio de 1821',
                                  '9 de diciembre de 1824',
                                  '6 de agosto de 1824',
                                  '4 de julio de 1776'],
                 'correcta': 'B'},
                {'pregunta': 'San Martín asumió el gobierno del Perú con el '
                             'título de:',
                 'alternativas': ['Libertador',
                                  'Protector',
                                  'Dictador',
                                  'Presidente',
                                  'Virrey'],
                 'correcta': 'B'},
                {'pregunta': 'Institución cultural creada por San Martín:',
                 'alternativas': ['La Universidad de San Marcos',
                                  'La Biblioteca Nacional',
                                  'El Museo Nacional',
                                  'La Academia de la Lengua',
                                  'El Archivo General'],
                 'correcta': 'B'},
                {'pregunta': 'La conferencia entre San Martín y Bolívar se '
                             'realizó en:',
                 'alternativas': ['Lima',
                                  'Guayaquil',
                                  'Trujillo',
                                  'Quito',
                                  'Bogotá'],
                 'correcta': 'B'},
                {'pregunta': 'Bolívar llegó al Perú en el año:',
                 'alternativas': ['1820', '1823', '1821', '1824', '1822'],
                 'correcta': 'B'},
                {'pregunta': 'La batalla de Junín se libró el:',
                 'alternativas': ['9 de diciembre de 1824',
                                  '6 de agosto de 1824',
                                  '28 de julio de 1821',
                                  '8 de septiembre de 1820',
                                  '2 de mayo de 1866'],
                 'correcta': 'B'},
                {'pregunta': 'Un rasgo distintivo de la batalla de Junín fue '
                             'que:',
                 'alternativas': ['Duró tres días',
                                  'Se libró sin usar armas de fuego',
                                  'Participó la marina',
                                  'Se realizó de noche',
                                  'Intervino artillería pesada'],
                 'correcta': 'B'},
                {'pregunta': 'La batalla de Ayacucho fue dirigida por:',
                 'alternativas': ['Simón Bolívar',
                                  'Antonio José de Sucre',
                                  'San Martín',
                                  'La Mar',
                                  'Santa Cruz'],
                 'correcta': 'B'},
                {'pregunta': 'La batalla de Ayacucho se libró el:',
                 'alternativas': ['6 de agosto de 1824',
                                  '9 de diciembre de 1824',
                                  '28 de julio de 1821',
                                  '20 de enero de 1825',
                                  '3 de octubre de 1824'],
                 'correcta': 'B'},
                {'pregunta': 'La Capitulación de Ayacucho fue firmada por el '
                             'virrey:',
                 'alternativas': ['Pezuela',
                                  'José de la Serna',
                                  'Abascal',
                                  'Toledo',
                                  "O'Higgins"],
                 'correcta': 'B'},
                {'pregunta': 'Antes de llegar al Perú, San Martín liberó:',
                 'alternativas': ['Colombia',
                                  'Chile',
                                  'Ecuador',
                                  'Bolivia',
                                  'Venezuela'],
                 'correcta': 'B'},
                {'pregunta': 'Ante el vacío de poder por la invasión '
                             'napoleónica se formaron:',
                 'alternativas': ['Los cabildos abiertos únicamente',
                                  'Las juntas de gobierno',
                                  'Los virreinatos',
                                  'Las intendencias',
                                  'Las audiencias'],
                 'correcta': 'B'},
                {'pregunta': 'Bolívar recibió en el Perú poderes de:',
                 'alternativas': ['Protector',
                                  'Dictador',
                                  'Presidente constitucional',
                                  'Regente',
                                  'Gobernador'],
                 'correcta': 'B'},
                {'pregunta': 'La proclamación de la Independencia se realizó '
                             'en:',
                 'alternativas': ['El Cusco',
                                  'La plaza de armas de Lima',
                                  'Trujillo',
                                  'Huaura',
                                  'Pisco'],
                 'correcta': 'B'},
                {'pregunta': 'La batalla que selló definitivamente la '
                             'independencia del Perú fue:',
                 'alternativas': ['Junín',
                                  'Ayacucho',
                                  'Maipú',
                                  'Chacabuco',
                                  'Pichincha'],
                 'correcta': 'B'}]},
 {'num': 16,
  'titulo': 'Construcción de la república peruana',
  'secciones': [{'titulo': '16.1 al 16.3 LOS PRIMEROS AÑOS',
                 'items': ['El {Protectorado} de San Martín (1821–1822) fue '
                           'el primer gobierno del Perú independiente.',
                           'El primer Congreso {Constituyente} se instaló en '
                           '{1822} y promulgó la Constitución de {1823}, de '
                           'carácter {liberal}.',
                           'El primer presidente del Perú fue José de la '
                           '{Riva Agüero}.']},
                {'titulo': '16.4 y 16.5 CAUDILLISMO Y CONFEDERACIÓN',
                 'items': ['El {caudillismo} militar dominó las primeras '
                           'décadas: los jefes {militares} de las guerras de '
                           'independencia se disputaron el poder.',
                           'La Confederación {Perú-Boliviana} ({1836}–1839) '
                           'fue creada por Andrés de {Santa Cruz}; '
                           'comprendía los Estados Nor Peruano, Sur Peruano '
                           'y {Boliviano}.',
                           'Fue disuelta tras la batalla de {Yungay} '
                           '({1839}), por la oposición de {Chile} y '
                           'Argentina.']},
                {'titulo': '16.6 LA ERA DEL GUANO',
                 'items': ['El {guano} de las islas se convirtió en la '
                           'principal fuente de ingresos del Estado desde '
                           '{1840}.',
                           'Se aplicó el sistema de {consignaciones} y luego '
                           'el contrato {Dreyfus} (1869), firmado durante el '
                           'gobierno de {Balta}.',
                           'Con el guano se abolió la {esclavitud} y el '
                           '{tributo} indígena durante el gobierno de Ramón '
                           '{Castilla}.',
                           'También se construyó el primer {ferrocarril} de '
                           'Sudamérica: Lima–{Callao}.']},
                {'titulo': '16.7 LA GUERRA DEL PACÍFICO',
                 'items': ['Causa inmediata: el impuesto de los {10} '
                           'centavos al salitre aplicado por {Bolivia} a una '
                           'empresa chilena.',
                           'Perú y Bolivia estaban unidos por un tratado de '
                           'alianza {defensiva} de 1873.',
                           'Combate de {Angamos} ({8} de octubre de 1879): '
                           'muerte de Miguel {Grau}.',
                           'Batalla de {Arica} (7 de junio de 1880): muerte '
                           'de Francisco {Bolognesi}.',
                           'La guerra terminó con el Tratado de {Ancón} '
                           '({1883}): el Perú cedió {Tarapacá} y Tacna y '
                           'Arica quedaron en poder chileno por 10 años.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El primer gobierno del Perú independiente fue '
                           '{El Protectorado de San Martín}.',
                           'El primer presidente del Perú fue {José de la '
                           'Riva Agüero}.',
                           'La Confederación Perú-Boliviana fue creada por '
                           '{Andrés de Santa Cruz}.',
                           'El contrato Dreyfus se firmó en 1869 durante el '
                           'gobierno de {José Balta}.',
                           'La abolición de la esclavitud y del tributo '
                           'indígena se produjo bajo el gobierno de {Ramón '
                           'Castilla}.',
                           'El primer ferrocarril de Sudamérica unió {Lima y '
                           'Callao}.',
                           'La causa inmediata de la Guerra del Pacífico fue '
                           '{El impuesto de los 10 centavos al salitre}.',
                           'El combate de Angamos se produjo el {8 de '
                           'octubre de 1879}.',
                           'La campaña de resistencia en la sierra central '
                           'fue dirigida por {Andrés A. Cáceres}.',
                           'El caudillismo militar se caracterizó porque el '
                           'poder fue disputado por {Los jefes militares de '
                           'la independencia}.',
                           'El sistema de comercialización del guano previo '
                           'al contrato Dreyfus fue {Las consignaciones}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['La primera Constitución del Perú fue promulgada '
                           'en {1823}.',
                           'La Confederación Perú-Boliviana fue disuelta '
                           'tras la batalla de {Yungay}.',
                           'Los Estados que integraron la Confederación '
                           'fueron Nor Peruano, Sur Peruano y {Boliviano}.',
                           'La principal fuente de ingresos del Estado '
                           'peruano desde 1840 fue {El guano}.',
                           'El tratado que unía a Perú y Bolivia era de '
                           'alianza {Defensiva}.',
                           'Miguel Grau murió heroicamente en el combate de '
                           '{Angamos}.',
                           'Francisco Bolognesi murió en la batalla de '
                           '{Arica}.',
                           'La Guerra del Pacífico terminó con el Tratado de '
                           '{Ancón}.',
                           'Por el Tratado de Ancón el Perú cedió '
                           'definitivamente {Tarapacá}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['El primer Congreso Constituyente del Perú, '
                           'instalado el 20 de setiembre de 1822, fue la '
                           'primera institución elegida {democráticamente} '
                           'en el país.',
                           'La primera Constitución del Perú independiente, '
                           'de carácter liberal, fue promulgada por el '
                           'presidente {Torre Tagle} el 12 de noviembre de '
                           '1823.',
                           'La Constitución de 1823 fue restaurada el 11 de '
                           'junio de {1827}, tras la caída del régimen '
                           'vitalicio bolivariano.',
                           'El historiador Jorge Basadre denominó '
                           '«Prosperidad falaz» al periodo económico '
                           'sostenido por el auge del {guano}.',
                           'La Guerra del Pacífico se precipitó cuando, en '
                           '1841, se descubrieron yacimientos de salitre en '
                           'el territorio boliviano de {Antofagasta}.',
                           'Por el Tratado de Ancón, el Perú cedió a '
                           'perpetuidad la provincia de {Tarapacá}, y Tacna '
                           'y Arica quedaron en poder chileno por diez '
                           'años.']}],
  'cuadros': [{'titulo': '16.7 HÉROES Y BATALLAS',
               'encabezados': ['Combate/Batalla', 'Fecha', 'Héroe'],
               'filas': [['{Angamos}', '{8} oct. 1879', 'Miguel {Grau}'],
                         ['{Arica}',
                          '7 jun. {1880}',
                          'Francisco {Bolognesi}'],
                         ['{San Juan} y Miraflores',
                          '1881',
                          'Defensa de {Lima}'],
                         ['Campaña de la {Breña}',
                          '1881-1883',
                          'Andrés A. {Cáceres}']]}],
  'preguntas': [{'pregunta': 'El primer gobierno del Perú independiente fue:',
                 'alternativas': ['La Junta Gubernativa',
                                  'El Protectorado de San Martín',
                                  'La dictadura de Bolívar',
                                  'El gobierno de Riva Agüero',
                                  'El Congreso Constituyente'],
                 'correcta': 'B'},
                {'pregunta': 'La primera Constitución del Perú fue '
                             'promulgada en:',
                 'alternativas': ['1821', '1823', '1826', '1828', '1834'],
                 'correcta': 'B'},
                {'pregunta': 'El primer presidente del Perú fue:',
                 'alternativas': ['San Martín',
                                  'José de la Riva Agüero',
                                  'Simón Bolívar',
                                  'Ramón Castilla',
                                  'La Mar'],
                 'correcta': 'B'},
                {'pregunta': 'La Confederación Perú-Boliviana fue creada '
                             'por:',
                 'alternativas': ['Ramón Castilla',
                                  'Andrés de Santa Cruz',
                                  'Agustín Gamarra',
                                  'Felipe Salaverry',
                                  'José de la Mar'],
                 'correcta': 'B'},
                {'pregunta': 'La Confederación Perú-Boliviana fue disuelta '
                             'tras la batalla de:',
                 'alternativas': ['Ingavi',
                                  'Yungay',
                                  'Socabaya',
                                  'Portada de Guías',
                                  'Ayacucho'],
                 'correcta': 'B'},
                {'pregunta': 'Los Estados que integraron la Confederación '
                             'fueron Nor Peruano, Sur Peruano y:',
                 'alternativas': ['Ecuatoriano',
                                  'Boliviano',
                                  'Chileno',
                                  'Argentino',
                                  'Colombiano'],
                 'correcta': 'B'},
                {'pregunta': 'La principal fuente de ingresos del Estado '
                             'peruano desde 1840 fue:',
                 'alternativas': ['El salitre',
                                  'El guano',
                                  'El caucho',
                                  'La plata',
                                  'El azúcar'],
                 'correcta': 'B'},
                {'pregunta': 'El contrato Dreyfus se firmó en 1869 durante '
                             'el gobierno de:',
                 'alternativas': ['Ramón Castilla',
                                  'José Balta',
                                  'Manuel Pardo',
                                  'Echenique',
                                  'Nicolás de Piérola'],
                 'correcta': 'B'},
                {'pregunta': 'La abolición de la esclavitud y del tributo '
                             'indígena se produjo bajo el gobierno de:',
                 'alternativas': ['José Balta',
                                  'Ramón Castilla',
                                  'Manuel Pardo',
                                  'Santa Cruz',
                                  'Gamarra'],
                 'correcta': 'B'},
                {'pregunta': 'El primer ferrocarril de Sudamérica unió:',
                 'alternativas': ['Lima y Huancayo',
                                  'Lima y Callao',
                                  'Tacna y Arica',
                                  'Cusco y Puno',
                                  'Mollendo y Arequipa'],
                 'correcta': 'B'},
                {'pregunta': 'La causa inmediata de la Guerra del Pacífico '
                             'fue:',
                 'alternativas': ['La invasión de Tarapacá',
                                  'El impuesto de los 10 centavos al salitre',
                                  'El bloqueo del Callao',
                                  'La toma de Antofagasta por Perú',
                                  'El tratado de 1873'],
                 'correcta': 'B'},
                {'pregunta': 'El tratado que unía a Perú y Bolivia era de '
                             'alianza:',
                 'alternativas': ['Ofensiva',
                                  'Defensiva',
                                  'Comercial',
                                  'Aduanera',
                                  'Cultural'],
                 'correcta': 'B'},
                {'pregunta': 'Miguel Grau murió heroicamente en el combate '
                             'de:',
                 'alternativas': ['Iquique',
                                  'Angamos',
                                  'Arica',
                                  'San Juan',
                                  'Tarapacá'],
                 'correcta': 'B'},
                {'pregunta': 'Francisco Bolognesi murió en la batalla de:',
                 'alternativas': ['Angamos',
                                  'Arica',
                                  'Tacna',
                                  'Miraflores',
                                  'Huamachuco'],
                 'correcta': 'B'},
                {'pregunta': 'El combate de Angamos se produjo el:',
                 'alternativas': ['7 de junio de 1880',
                                  '8 de octubre de 1879',
                                  '21 de mayo de 1879',
                                  '13 de enero de 1881',
                                  '10 de julio de 1883'],
                 'correcta': 'B'},
                {'pregunta': 'La Guerra del Pacífico terminó con el Tratado '
                             'de:',
                 'alternativas': ['Ancón',
                                  'Lima',
                                  'Santiago',
                                  'Tordesillas',
                                  'Ginebra'],
                 'correcta': 'A'},
                {'pregunta': 'Por el Tratado de Ancón el Perú cedió '
                             'definitivamente:',
                 'alternativas': ['Tacna',
                                  'Tarapacá',
                                  'Arica',
                                  'Antofagasta',
                                  'Iquique y Tacna'],
                 'correcta': 'B'},
                {'pregunta': 'La campaña de resistencia en la sierra central '
                             'fue dirigida por:',
                 'alternativas': ['Miguel Iglesias',
                                  'Andrés A. Cáceres',
                                  'Nicolás de Piérola',
                                  'Lizardo Montero',
                                  'Francisco Bolognesi'],
                 'correcta': 'B'},
                {'pregunta': 'El caudillismo militar se caracterizó porque '
                             'el poder fue disputado por:',
                 'alternativas': ['Los comerciantes',
                                  'Los jefes militares de la independencia',
                                  'El clero',
                                  'Los indígenas',
                                  'Los extranjeros'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema de comercialización del guano '
                             'previo al contrato Dreyfus fue:',
                 'alternativas': ['El monopolio estatal',
                                  'Las consignaciones',
                                  'La libre competencia',
                                  'El arrendamiento',
                                  'La concesión minera'],
                 'correcta': 'B'}]},
 {'num': 17,
  'titulo': 'Estado peruano en transformación',
  'secciones': [{'titulo': '17.1 LA RECONSTRUCCIÓN NACIONAL',
                 'items': ['Tras la Guerra del Pacífico, el Perú vivió el '
                           'llamado {Segundo} Militarismo, dirigido por '
                           'Miguel {Iglesias} y luego Andrés A. {Cáceres}.',
                           'Se firmó el Contrato {Grace} ({1889}): el Perú '
                           'entregó los {ferrocarriles} por 66 años y el '
                           'guano a cambio de cancelar la deuda {externa}.']},
                {'titulo': '17.2 LA REPÚBLICA ARISTOCRÁTICA (1895–1919)',
                 'items': ['Se inició con el gobierno de Nicolás de '
                           '{Piérola}. El poder lo ejerció una {oligarquía} '
                           'civilista.',
                           'La economía se basó en la {exportación} de '
                           'materias primas: azúcar, algodón, {caucho}, lana '
                           'y minerales.',
                           'Fue el periodo del auge del {caucho} en la '
                           'Amazonía, con graves abusos contra las '
                           'poblaciones {indígenas}.']},
                {'titulo': '17.3 EL ONCENIO DE LEGUÍA (1919–1930)',
                 'items': ['Augusto B. {Leguía} llamó a su gobierno la '
                           '«{Patria} Nueva».',
                           'Promulgó la Constitución de {1920} y estableció '
                           'la {conscripción} vial, trabajo obligatorio para '
                           'construir carreteras.',
                           'Aspectos limítrofes: el Tratado {Salomón-Lozano} '
                           'con {Colombia} (1922) y el Tratado de {Lima} con '
                           '{Chile} (1929), por el cual {Tacna} volvió al '
                           'Perú y {Arica} quedó en Chile.',
                           'Impulsó los {enclaves} económicos y el '
                           'endeudamiento con {Estados Unidos}.',
                           'Fue derrocado en {1930} por la rebelión de Luis '
                           'M. {Sánchez Cerro} en Arequipa.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El periodo posterior a la Guerra del Pacífico se '
                           'conoce como {Reconstrucción Nacional o Segundo '
                           'Militarismo}.',
                           'Por el Contrato Grace el Perú entregó por 66 '
                           'años {Los ferrocarriles}.',
                           'La República Aristocrática se inició con el '
                           'gobierno de {Nicolás de Piérola}.',
                           'La República Aristocrática abarca los años '
                           '{1895-1919}.',
                           'El grupo social que ejerció el poder durante la '
                           'República Aristocrática fue {La oligarquía '
                           'civilista}.',
                           'La economía de la República Aristocrática se '
                           'basó en {La exportación de materias primas}.',
                           'El gobierno de Leguía entre 1919 y 1930 se '
                           'conoce como {La Patria Nueva u Oncenio}.',
                           'El trabajo obligatorio para construir carreteras '
                           'durante el Oncenio se llamó {Conscripción vial}.',
                           'Leguía fue derrocado en 1930 por {Luis M. '
                           'Sánchez Cerro}.',
                           'Los enclaves económicos se caracterizaron por '
                           '{Ser empresas extranjeras con escasa integración '
                           'a la economía nacional}.',
                           'El primer presidente del Segundo Militarismo fue '
                           '{Miguel Iglesias}.',
                           'La explotación del caucho tuvo como consecuencia '
                           'principal {Graves abusos contra las poblaciones '
                           'indígenas amazónicas}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El Contrato Grace se firmó en el año {1889}.',
                           'La Constitución promulgada durante el Oncenio '
                           'fue la de {1920}.',
                           'El Tratado Salomón-Lozano se firmó con '
                           '{Colombia}.',
                           'El Tratado de Lima de 1929 se firmó con {Chile}.',
                           'Por el Tratado de Lima de 1929, Tacna {Volvió al '
                           'Perú}.',
                           'Por el Tratado de Lima de 1929, Arica quedó en '
                           'poder de {Chile}.',
                           'Durante la República Aristocrática se produjo el '
                           'auge de la explotación del {Caucho}.',
                           'El endeudamiento externo del Oncenio se dio '
                           'principalmente con {Estados Unidos}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['El historiador peruano {Jorge Basadre} denominó '
                           '«República Aristocrática» al periodo dominado '
                           'por la oligarquía civilista.',
                           'Durante la República Aristocrática se creó la '
                           '{Policía Nacional} para reprimir los movimientos '
                           'sociales, y surgió el movimiento indigenista.',
                           'El Oncenio de Leguía coincidió con el Crack de '
                           '1929 en Estados Unidos, conocido como el {jueves '
                           'negro}.',
                           'El endeudamiento del Oncenio con banqueros '
                           'estadounidenses les permitió a estos exigir el '
                           'control de la {administración aduanera}.',
                           'Leguía fue derrocado por el golpe de Estado del '
                           'teniente coronel Luis {Sánchez Cerro} en 1930.',
                           'Sánchez Cerro fue elegido presidente por voto '
                           'popular en 1931, derrotando al APRA y al '
                           '{Partido Comunista}.',
                           'Durante el gobierno de Sánchez Cerro se produjo '
                           'el conflicto internacional con Colombia por '
                           '{Leticia} y el Trapecio Amazónico.']}],
  'cuadros': [{'titulo': '17.3 TRATADOS LIMÍTROFES DEL ONCENIO',
               'encabezados': ['Tratado', 'Año', 'País'],
               'filas': [['{Salomón-Lozano}', '{1922}', '{Colombia}'],
                         ['Tratado de {Lima}', '{1929}', '{Chile}']]}],
  'preguntas': [{'pregunta': 'El periodo posterior a la Guerra del Pacífico '
                             'se conoce como:',
                 'alternativas': ['Primer Militarismo',
                                  'Reconstrucción Nacional o Segundo '
                                  'Militarismo',
                                  'República Aristocrática',
                                  'Oncenio',
                                  'Patria Nueva'],
                 'correcta': 'B'},
                {'pregunta': 'Por el Contrato Grace el Perú entregó por 66 '
                             'años:',
                 'alternativas': ['Las minas',
                                  'Los ferrocarriles',
                                  'Los puertos',
                                  'Las islas guaneras únicamente',
                                  'Las aduanas'],
                 'correcta': 'B'},
                {'pregunta': 'El Contrato Grace se firmó en el año:',
                 'alternativas': ['1883', '1889', '1895', '1919', '1929'],
                 'correcta': 'B'},
                {'pregunta': 'La República Aristocrática se inició con el '
                             'gobierno de:',
                 'alternativas': ['Andrés A. Cáceres',
                                  'Nicolás de Piérola',
                                  'Miguel Iglesias',
                                  'Augusto B. Leguía',
                                  'José Pardo'],
                 'correcta': 'B'},
                {'pregunta': 'La República Aristocrática abarca los años:',
                 'alternativas': ['1883-1895',
                                  '1895-1919',
                                  '1919-1930',
                                  '1930-1945',
                                  '1845-1862'],
                 'correcta': 'B'},
                {'pregunta': 'El grupo social que ejerció el poder durante '
                             'la República Aristocrática fue:',
                 'alternativas': ['El proletariado',
                                  'La oligarquía civilista',
                                  'Los militares',
                                  'El campesinado',
                                  'La Iglesia'],
                 'correcta': 'B'},
                {'pregunta': 'La economía de la República Aristocrática se '
                             'basó en:',
                 'alternativas': ['La industria pesada',
                                  'La exportación de materias primas',
                                  'El comercio interno',
                                  'La minería estatal',
                                  'El turismo'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno de Leguía entre 1919 y 1930 se '
                             'conoce como:',
                 'alternativas': ['La Patria Nueva u Oncenio',
                                  'El Novenio',
                                  'La República Aristocrática',
                                  'El Ochenio',
                                  'La Reconstrucción'],
                 'correcta': 'A'},
                {'pregunta': 'La Constitución promulgada durante el Oncenio '
                             'fue la de:',
                 'alternativas': ['1860', '1920', '1933', '1979', '1993'],
                 'correcta': 'B'},
                {'pregunta': 'El trabajo obligatorio para construir '
                             'carreteras durante el Oncenio se llamó:',
                 'alternativas': ['Mita republicana',
                                  'Conscripción vial',
                                  'Enganche',
                                  'Yanaconaje',
                                  'Faena'],
                 'correcta': 'B'},
                {'pregunta': 'El Tratado Salomón-Lozano se firmó con:',
                 'alternativas': ['Chile',
                                  'Colombia',
                                  'Ecuador',
                                  'Bolivia',
                                  'Brasil'],
                 'correcta': 'B'},
                {'pregunta': 'El Tratado de Lima de 1929 se firmó con:',
                 'alternativas': ['Colombia',
                                  'Chile',
                                  'Ecuador',
                                  'Bolivia',
                                  'Argentina'],
                 'correcta': 'B'},
                {'pregunta': 'Por el Tratado de Lima de 1929, Tacna:',
                 'alternativas': ['Quedó en Chile',
                                  'Volvió al Perú',
                                  'Se declaró neutral',
                                  'Pasó a Bolivia',
                                  'Se dividió'],
                 'correcta': 'B'},
                {'pregunta': 'Por el Tratado de Lima de 1929, Arica quedó en '
                             'poder de:',
                 'alternativas': ['Perú',
                                  'Chile',
                                  'Bolivia',
                                  'Administración internacional',
                                  'Ninguno'],
                 'correcta': 'B'},
                {'pregunta': 'Leguía fue derrocado en 1930 por:',
                 'alternativas': ['Óscar R. Benavides',
                                  'Luis M. Sánchez Cerro',
                                  'Manuel Prado',
                                  'Odría',
                                  'Bustamante y Rivero'],
                 'correcta': 'B'},
                {'pregunta': 'Durante la República Aristocrática se produjo '
                             'el auge de la explotación del:',
                 'alternativas': ['Guano',
                                  'Caucho',
                                  'Salitre',
                                  'Petróleo',
                                  'Estaño'],
                 'correcta': 'B'},
                {'pregunta': 'El endeudamiento externo del Oncenio se dio '
                             'principalmente con:',
                 'alternativas': ['Inglaterra',
                                  'Estados Unidos',
                                  'Francia',
                                  'Alemania',
                                  'España'],
                 'correcta': 'B'},
                {'pregunta': 'Los enclaves económicos se caracterizaron por:',
                 'alternativas': ['Ser empresas estatales',
                                  'Ser empresas extranjeras con escasa '
                                  'integración a la economía nacional',
                                  'Pertenecer a comunidades campesinas',
                                  'Ser cooperativas',
                                  'Ser talleres artesanales'],
                 'correcta': 'B'},
                {'pregunta': 'El primer presidente del Segundo Militarismo '
                             'fue:',
                 'alternativas': ['Andrés A. Cáceres',
                                  'Miguel Iglesias',
                                  'Nicolás de Piérola',
                                  'Remigio Morales Bermúdez',
                                  'Lizardo Montero'],
                 'correcta': 'B'},
                {'pregunta': 'La explotación del caucho tuvo como '
                             'consecuencia principal:',
                 'alternativas': ['El desarrollo industrial',
                                  'Graves abusos contra las poblaciones '
                                  'indígenas amazónicas',
                                  'La modernización agrícola',
                                  'El auge del guano',
                                  'La construcción de ferrocarriles'],
                 'correcta': 'B'}]},
 {'num': 18,
  'titulo': 'El mundo entre guerras',
  'secciones': [{'titulo': '18.1 PRIMERA GUERRA MUNDIAL (1914–1918)',
                 'items': ['Causas: el {imperialismo}, el {nacionalismo}, la '
                           'carrera {armamentista} y los sistemas de '
                           '{alianzas}.',
                           'Causa inmediata: el asesinato del archiduque '
                           '{Francisco Fernando} en {Sarajevo}.',
                           'Bandos: la {Triple Alianza} y la {Triple '
                           'Entente}.',
                           'Terminó con el Tratado de {Versalles} ({1919}), '
                           'que impuso duras condiciones a {Alemania}.',
                           'Se creó la Sociedad de {Naciones} para preservar '
                           'la paz.']},
                {'titulo': '18.2 LA DEPRESIÓN MUNDIAL DE 1929',
                 'items': ['Se inició con el {crac} de la bolsa de {Nueva '
                           'York} el «jueves {negro}».',
                           'Consecuencias: quiebra de bancos, {desempleo} '
                           'masivo y caída del {comercio} mundial.',
                           'En Estados Unidos se aplicó el {New Deal} de '
                           'Franklin D. {Roosevelt}.']},
                {'titulo': '18.3 y 18.4 SEGUNDA GUERRA MUNDIAL Y GUERRA FRÍA',
                 'items': ['La Segunda Guerra Mundial ({1939}–1945) se '
                           'inició con la invasión alemana a {Polonia}.',
                           'Bandos: las potencias del {Eje} (Alemania, '
                           'Italia, Japón) y los {Aliados}.',
                           'Terminó con las bombas atómicas sobre '
                           '{Hiroshima} y {Nagasaki} en {1945}. Se creó la '
                           '{ONU}.',
                           'La Guerra {Fría} enfrentó a {Estados Unidos} y '
                           'la {URSS} sin combate directo, dividiendo el '
                           'mundo en dos {bloques}.']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['La causa inmediata de la Primera Guerra Mundial '
                           'fue {El asesinato del archiduque Francisco '
                           'Fernando}.',
                           'La Primera Guerra Mundial se desarrolló entre '
                           '{1914-1918}.',
                           'El tratado que puso fin a la Primera Guerra '
                           'Mundial fue {Tratado de Versalles}.',
                           'El organismo creado tras la Primera Guerra '
                           'Mundial para preservar la paz fue {La Sociedad '
                           'de Naciones}.',
                           'La Gran Depresión mundial se inició en el año '
                           '{1929}.',
                           'El programa aplicado en Estados Unidos para '
                           'superar la crisis fue {El New Deal}.',
                           'El presidente que aplicó el New Deal fue '
                           '{Franklin D. Roosevelt}.',
                           'Las potencias del Eje fueron {Alemania, Italia y '
                           'Japón}.',
                           'La Segunda Guerra Mundial terminó con {Las '
                           'bombas atómicas sobre Hiroshima y Nagasaki}.',
                           'El organismo internacional creado en 1945 fue '
                           '{La ONU}.',
                           'La Guerra Fría enfrentó a {Estados Unidos y la '
                           'URSS}.',
                           'Un rasgo característico de la Guerra Fría fue '
                           '{La ausencia de enfrentamiento militar directo '
                           'entre las potencias}.',
                           'Los bandos de la Primera Guerra Mundial fueron '
                           '{Triple Alianza y Triple Entente}.',
                           'Una consecuencia social de la Gran Depresión fue '
                           '{El desempleo masivo}.',
                           'La Segunda Guerra Mundial se desarrolló entre '
                           'los años {1939-1945}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El asesinato que desencadenó la Primera Guerra '
                           'Mundial ocurrió en {Sarajevo}.',
                           'El país más perjudicado por el Tratado de '
                           'Versalles fue {Alemania}.',
                           'La Gran Depresión se inició con el crac de la '
                           'bolsa de {Nueva York}.',
                           'La Segunda Guerra Mundial se inició con la '
                           'invasión alemana a {Polonia}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['El archiduque Francisco Fernando fue asesinado '
                           'en Sarajevo por el nacionalista serbio {Gavrilo '
                           'Princip}.',
                           'La Triple Alianza agrupó a Alemania, '
                           'Austria-Hungría e Italia; esta última luego se '
                           'pasó al bando de la {Triple Entente}.',
                           'Hacia 1932, más de cinco mil bancos habían '
                           'quebrado en Estados Unidos como consecuencia de '
                           'la {Gran Depresión}.',
                           'El régimen nazi reclamó un «espacio vital» para '
                           'el pueblo alemán y la devolución de sus antiguas '
                           '{colonias}.',
                           'Tras renunciar a las restricciones de desarme '
                           'del Tratado de Versalles, {Hitler} armó un '
                           'ejército poderoso e inició su expansión.',
                           'La Guerra Fría incluyó conflictos como la '
                           'división de Alemania, el Muro de Berlín, la '
                           'Guerra de Corea y la Guerra de {Vietnam}.']}],
  'cuadros': [{'titulo': '18. LAS DOS GUERRAS MUNDIALES',
               'encabezados': ['Guerra', 'Años', 'Fin'],
               'filas': [['Primera', '{1914}–1918', 'Tratado de {Versalles}'],
                         ['Segunda',
                          '{1939}–{1945}',
                          'Bombas de {Hiroshima} y Nagasaki']]}],
  'preguntas': [{'pregunta': 'La causa inmediata de la Primera Guerra '
                             'Mundial fue:',
                 'alternativas': ['La invasión de Polonia',
                                  'El asesinato del archiduque Francisco '
                                  'Fernando',
                                  'El crac de 1929',
                                  'El hundimiento del Lusitania',
                                  'La toma de la Bastilla'],
                 'correcta': 'B'},
                {'pregunta': 'El asesinato que desencadenó la Primera Guerra '
                             'Mundial ocurrió en:',
                 'alternativas': ['Berlín',
                                  'Sarajevo',
                                  'Viena',
                                  'París',
                                  'Múnich'],
                 'correcta': 'B'},
                {'pregunta': 'La Primera Guerra Mundial se desarrolló entre:',
                 'alternativas': ['1910-1914',
                                  '1914-1918',
                                  '1918-1922',
                                  '1929-1933',
                                  '1939-1945'],
                 'correcta': 'B'},
                {'pregunta': 'El tratado que puso fin a la Primera Guerra '
                             'Mundial fue:',
                 'alternativas': ['Tratado de Ancón',
                                  'Tratado de Versalles',
                                  'Tratado de Lima',
                                  'Pacto de Varsovia',
                                  'Tratado de Roma'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo creado tras la Primera Guerra '
                             'Mundial para preservar la paz fue:',
                 'alternativas': ['La ONU',
                                  'La Sociedad de Naciones',
                                  'La OTAN',
                                  'La Cruz Roja',
                                  'El Pacto de Varsovia'],
                 'correcta': 'B'},
                {'pregunta': 'El país más perjudicado por el Tratado de '
                             'Versalles fue:',
                 'alternativas': ['Francia',
                                  'Alemania',
                                  'Rusia',
                                  'Italia',
                                  'Inglaterra'],
                 'correcta': 'B'},
                {'pregunta': 'La Gran Depresión se inició con el crac de la '
                             'bolsa de:',
                 'alternativas': ['Londres',
                                  'Nueva York',
                                  'París',
                                  'Tokio',
                                  'Berlín'],
                 'correcta': 'B'},
                {'pregunta': 'La Gran Depresión mundial se inició en el año:',
                 'alternativas': ['1914', '1929', '1939', '1945', '1919'],
                 'correcta': 'B'},
                {'pregunta': 'El programa aplicado en Estados Unidos para '
                             'superar la crisis fue:',
                 'alternativas': ['El Plan Marshall',
                                  'El New Deal',
                                  'La Doctrina Monroe',
                                  'El Plan Cóndor',
                                  'La Alianza para el Progreso'],
                 'correcta': 'B'},
                {'pregunta': 'El presidente que aplicó el New Deal fue:',
                 'alternativas': ['Woodrow Wilson',
                                  'Franklin D. Roosevelt',
                                  'Herbert Hoover',
                                  'Harry Truman',
                                  'Theodore Roosevelt'],
                 'correcta': 'B'},
                {'pregunta': 'La Segunda Guerra Mundial se inició con la '
                             'invasión alemana a:',
                 'alternativas': ['Francia',
                                  'Polonia',
                                  'Checoslovaquia',
                                  'Austria',
                                  'La URSS'],
                 'correcta': 'B'},
                {'pregunta': 'Las potencias del Eje fueron:',
                 'alternativas': ['Inglaterra, Francia y EE.UU.',
                                  'Alemania, Italia y Japón',
                                  'URSS, China y EE.UU.',
                                  'Alemania, Austria y Turquía',
                                  'Francia, Rusia e Inglaterra'],
                 'correcta': 'B'},
                {'pregunta': 'La Segunda Guerra Mundial terminó con:',
                 'alternativas': ['El Tratado de Versalles',
                                  'Las bombas atómicas sobre Hiroshima y '
                                  'Nagasaki',
                                  'La caída del Muro de Berlín',
                                  'El crac de 1929',
                                  'La Revolución Rusa'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo internacional creado en 1945 fue:',
                 'alternativas': ['La Sociedad de Naciones',
                                  'La ONU',
                                  'La OTAN',
                                  'La OEA',
                                  'El FMI'],
                 'correcta': 'B'},
                {'pregunta': 'La Guerra Fría enfrentó a:',
                 'alternativas': ['Alemania y Francia',
                                  'Estados Unidos y la URSS',
                                  'China y Japón',
                                  'Inglaterra y España',
                                  'India y Pakistán'],
                 'correcta': 'B'},
                {'pregunta': 'Un rasgo característico de la Guerra Fría fue:',
                 'alternativas': ['El combate directo entre las potencias',
                                  'La ausencia de enfrentamiento militar '
                                  'directo entre las potencias',
                                  'La alianza militar entre EE.UU. y la URSS',
                                  'La desaparición de los bloques',
                                  'El desarme total'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las causas de la Primera Guerra Mundial '
                             'NO figura:',
                 'alternativas': ['El imperialismo',
                                  'El nacionalismo',
                                  'La carrera armamentista',
                                  'Los sistemas de alianzas',
                                  'La caída del Muro de Berlín'],
                 'correcta': 'E'},
                {'pregunta': 'Los bandos de la Primera Guerra Mundial '
                             'fueron:',
                 'alternativas': ['Eje y Aliados',
                                  'Triple Alianza y Triple Entente',
                                  'OTAN y Pacto de Varsovia',
                                  'Unión y Confederación',
                                  'Aliados y Neutrales'],
                 'correcta': 'B'},
                {'pregunta': 'Una consecuencia social de la Gran Depresión '
                             'fue:',
                 'alternativas': ['El pleno empleo',
                                  'El desempleo masivo',
                                  'El auge del comercio',
                                  'La estabilidad bancaria',
                                  'El aumento de salarios'],
                 'correcta': 'B'},
                {'pregunta': 'La Segunda Guerra Mundial se desarrolló entre '
                             'los años:',
                 'alternativas': ['1914-1918',
                                  '1939-1945',
                                  '1929-1933',
                                  '1945-1991',
                                  '1936-1939'],
                 'correcta': 'B'}]},
 {'num': 19,
  'titulo': 'Entre dictaduras y democracias: gobernantes del Perú siglos '
            'XX-XXI',
  'secciones': [{'titulo': '19.1 al 19.4 DE ODRÍA A VELASCO',
                 'items': ['El {Ochenio} de Manuel A. {Odría} (1948–1956) '
                           'fue una dictadura militar que impulsó grandes '
                           'obras {públicas} y otorgó el voto a la {mujer} '
                           '(1955).',
                           'Primer gobierno de Fernando {Belaunde} '
                           '(1963–1968): impulsó Cooperación {Popular} y fue '
                           'derrocado por el escándalo de la página {once} '
                           'del contrato con la IPC.',
                           'Gobierno militar de Juan {Velasco Alvarado} '
                           '(1968–1975): aplicó la {Reforma} Agraria '
                           '({1969}), nacionalizó el {petróleo} y la banca, '
                           'y reconoció el {quechua} como lengua oficial.',
                           'Segunda fase, de Francisco {Morales Bermúdez} '
                           '(1975–1980): convocó a la Asamblea '
                           '{Constituyente} de 1978, presidida por Víctor '
                           'Raúl {Haya de la Torre}.']},
                {'titulo': '19.5 al 19.7 RETORNO A LA DEMOCRACIA',
                 'items': ['Segundo gobierno de Belaunde (1980–1985): se '
                           'promulgó la Constitución de {1979} y se inició '
                           'la violencia de {Sendero Luminoso} en Chuschi, '
                           'Ayacucho ({1980}).',
                           'Primer gobierno de Alan {García} (1985–1990): '
                           'crisis económica con {hiperinflación} y '
                           'estatización de la {banca}.',
                           'Década del {fujimorismo} (1990–2000): '
                           '{autogolpe} del {5} de abril de 1992, captura de '
                           'Abimael {Guzmán} el mismo año, y Constitución de '
                           '{1993}.',
                           'En 2000 Fujimori renunció por {fax} desde Japón, '
                           'tras los {vladivideos}.']},
                {'titulo': '19.8 al 19.11 SIGLO XXI',
                 'items': ['Gobierno transitorio de Valentín {Paniagua} '
                           '(2000–2001): creó la Comisión de la {Verdad} y '
                           'Reconciliación.',
                           'Alejandro {Toledo} (2001–2006): impulsó la '
                           '{descentralización} y los gobiernos '
                           '{regionales}.',
                           'Segundo gobierno de Alan García (2006–2011) y '
                           'gobierno de Ollanta {Humala} (2011–2016).']},
                {'titulo': 'DATOS COMPLEMENTARIOS',
                 'items': ['El «Ochenio» corresponde al gobierno de {Manuel '
                           'A. Odría}.',
                           'El primer gobierno de Belaunde fue derrocado por '
                           'el escándalo de {La página once}.',
                           'La Reforma Agraria fue aplicada en 1969 por '
                           '{Juan Velasco Alvarado}.',
                           'La Asamblea Constituyente de 1978 fue presidida '
                           'por {Víctor Raúl Haya de la Torre}.',
                           'El primer gobierno de Alan García se caracterizó '
                           'por {La hiperinflación}.',
                           'El autogolpe de Estado de Fujimori se produjo el '
                           '{5 de abril de 1992}.',
                           'El líder de Sendero Luminoso capturado en 1992 '
                           'fue {Abimael Guzmán}.',
                           'Fujimori renunció a la presidencia en el año '
                           '2000 mediante {Un fax desde Japón}.',
                           'El gobierno transitorio del año 2000-2001 fue '
                           'presidido por {Valentín Paniagua}.',
                           'El gobierno de Alejandro Toledo impulsó '
                           'principalmente {La descentralización y los '
                           'gobiernos regionales}.',
                           'El gobierno militar de la segunda fase '
                           '(1975-1980) estuvo encabezado por {Francisco '
                           'Morales Bermúdez}.',
                           'El gobierno de Ollanta Humala corresponde al '
                           'periodo {2011-2016}.',
                           'Una medida económica central del primer gobierno '
                           'de Alan García fue {La estatización de la '
                           'banca}.']},
                {'titulo': 'MÁS DATOS PARA REPASAR',
                 'items': ['El voto a la mujer en el Perú se otorgó durante '
                           'el gobierno de {Odría}.',
                           'El gobierno de Velasco reconoció como lengua '
                           'oficial al {Quechua}.',
                           'La Constitución promulgada durante el segundo '
                           'gobierno de Belaunde fue la de {1979}.',
                           'La violencia de Sendero Luminoso se inició en '
                           '1980 en {Chuschi, Ayacucho}.',
                           'La Constitución vigente del Perú fue promulgada '
                           'en {1993}.',
                           'Los videos que evidenciaron la corrupción del '
                           'régimen fujimorista se conocen como '
                           '{Vladivideos}.',
                           'La Comisión de la Verdad y Reconciliación fue '
                           'creada durante el gobierno de {Valentín '
                           'Paniagua}.']},
                {'titulo': 'AMPLIACIÓN — MÁS DATOS DEL TEMARIO',
                 'items': ['El general Manuel A. Odría se pronunció desde '
                           'Arequipa contra el gobierno de {José Luis '
                           'Bustamante y Rivero}, a quien acusó de debilidad '
                           'frente al APRA.',
                           'El golpe de Estado que derrocó a Belaunde en '
                           '1968 fue encabezado por el general {Juan Velasco '
                           'Alvarado}.',
                           'Durante el primer gobierno de Belaunde se '
                           'construyeron la carretera Marginal de la Selva y '
                           'el Aeropuerto Internacional {Jorge Chávez}.',
                           'Francisco Morales Bermúdez, jefe de la segunda '
                           'fase del gobierno militar, era nieto del '
                           'expresidente {Remigio Morales Bermúdez}.',
                           'Alan García llegó al poder en 1985 representando '
                           'al APRA, fundado en {1924}, en su primer acceso '
                           'a la presidencia.',
                           'Alan García derrotó en las elecciones de 1985 al '
                           'candidato de Izquierda Unida, {Alfonso Barrantes '
                           'Lingán}.',
                           'Fujimori derrotó en 1990 al novelista {Mario '
                           'Vargas Llosa}, con su movimiento Cambio 90.',
                           'El sociólogo peruano {Julio Cotler} calificó al '
                           'gobierno de Alan García como una «democradura», '
                           'por su carácter dictatorial.',
                           'En su segundo gobierno, Alan García derrotó en '
                           'segunda vuelta al candidato {Ollanta Humala}.',
                           'Ollanta Humala derrotó a Keiko Fujimori en '
                           'segunda vuelta, con el respaldo público de '
                           '{Mario Vargas Llosa}.']}],
  'cuadros': [{'titulo': '19. GOBIERNOS Y HECHOS CLAVE',
               'encabezados': ['Gobernante', 'Periodo', 'Hecho principal'],
               'filas': [['Manuel A. {Odría}',
                          '{1948}-1956',
                          'Voto a la {mujer}'],
                         ['Juan {Velasco}',
                          '1968-{1975}',
                          '{Reforma} Agraria'],
                         ['Alan {García} (1°)',
                          '1985-{1990}',
                          '{Hiperinflación}'],
                         ['Alberto {Fujimori}',
                          '1990-{2000}',
                          '{Autogolpe} de 1992'],
                         ['Valentín {Paniagua}',
                          '2000-2001',
                          'Comisión de la {Verdad}']]}],
  'preguntas': [{'pregunta': 'El «Ochenio» corresponde al gobierno de:',
                 'alternativas': ['Odría',
                                  'Manuel A. Odría',
                                  'Velasco',
                                  'Leguía',
                                  'Prado'],
                 'correcta': 'B'},
                {'pregunta': 'El voto a la mujer en el Perú se otorgó '
                             'durante el gobierno de:',
                 'alternativas': ['Leguía',
                                  'Odría',
                                  'Prado',
                                  'Bustamante',
                                  'Belaunde'],
                 'correcta': 'B'},
                {'pregunta': 'El primer gobierno de Belaunde fue derrocado '
                             'por el escándalo de:',
                 'alternativas': ['Los vladivideos',
                                  'La página once',
                                  'El contrato Grace',
                                  'Los petroaudios',
                                  'El caso Dreyfus'],
                 'correcta': 'B'},
                {'pregunta': 'La Reforma Agraria fue aplicada en 1969 por:',
                 'alternativas': ['Belaunde',
                                  'Juan Velasco Alvarado',
                                  'Morales Bermúdez',
                                  'Odría',
                                  'Prado'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno de Velasco reconoció como lengua '
                             'oficial al:',
                 'alternativas': ['Aimara',
                                  'Quechua',
                                  'Ashaninka',
                                  'Castellano únicamente',
                                  'Inglés'],
                 'correcta': 'B'},
                {'pregunta': 'La Asamblea Constituyente de 1978 fue '
                             'presidida por:',
                 'alternativas': ['Belaunde',
                                  'Víctor Raúl Haya de la Torre',
                                  'Morales Bermúdez',
                                  'Alan García',
                                  'Bedoya Reyes'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución promulgada durante el segundo '
                             'gobierno de Belaunde fue la de:',
                 'alternativas': ['1933', '1979', '1993', '1920', '1867'],
                 'correcta': 'B'},
                {'pregunta': 'La violencia de Sendero Luminoso se inició en '
                             '1980 en:',
                 'alternativas': ['Lima',
                                  'Chuschi, Ayacucho',
                                  'Huancayo',
                                  'Cusco',
                                  'Huánuco'],
                 'correcta': 'B'},
                {'pregunta': 'El primer gobierno de Alan García se '
                             'caracterizó por:',
                 'alternativas': ['El auge exportador',
                                  'La hiperinflación',
                                  'La estabilidad monetaria',
                                  'El pleno empleo',
                                  'El superávit fiscal'],
                 'correcta': 'B'},
                {'pregunta': 'El autogolpe de Estado de Fujimori se produjo '
                             'el:',
                 'alternativas': ['28 de julio de 1990',
                                  '5 de abril de 1992',
                                  '12 de septiembre de 1992',
                                  '3 de octubre de 1968',
                                  '9 de diciembre de 2000'],
                 'correcta': 'B'},
                {'pregunta': 'El líder de Sendero Luminoso capturado en 1992 '
                             'fue:',
                 'alternativas': ['Víctor Polay',
                                  'Abimael Guzmán',
                                  'Óscar Ramírez',
                                  'Feliciano',
                                  'Nelson Cerpa'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución vigente del Perú fue '
                             'promulgada en:',
                 'alternativas': ['1979', '1993', '1933', '2001', '1920'],
                 'correcta': 'B'},
                {'pregunta': 'Fujimori renunció a la presidencia en el año '
                             '2000 mediante:',
                 'alternativas': ['Un discurso en el Congreso',
                                  'Un fax desde Japón',
                                  'Una carta al Papa',
                                  'Un mensaje a la nación',
                                  'Un referéndum'],
                 'correcta': 'B'},
                {'pregunta': 'Los videos que evidenciaron la corrupción del '
                             'régimen fujimorista se conocen como:',
                 'alternativas': ['Petroaudios',
                                  'Vladivideos',
                                  'Narcoaudios',
                                  'Cocteles',
                                  'Los cuellos blancos'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno transitorio del año 2000-2001 fue '
                             'presidido por:',
                 'alternativas': ['Alejandro Toledo',
                                  'Valentín Paniagua',
                                  'Alan García',
                                  'Ollanta Humala',
                                  'Paniagua Corazao hijo'],
                 'correcta': 'B'},
                {'pregunta': 'La Comisión de la Verdad y Reconciliación fue '
                             'creada durante el gobierno de:',
                 'alternativas': ['Fujimori',
                                  'Valentín Paniagua',
                                  'Toledo',
                                  'Alan García',
                                  'Humala'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno de Alejandro Toledo impulsó '
                             'principalmente:',
                 'alternativas': ['La Reforma Agraria',
                                  'La descentralización y los gobiernos '
                                  'regionales',
                                  'La estatización de la banca',
                                  'El autogolpe',
                                  'La nacionalización del petróleo'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno militar de la segunda fase '
                             '(1975-1980) estuvo encabezado por:',
                 'alternativas': ['Juan Velasco Alvarado',
                                  'Francisco Morales Bermúdez',
                                  'Manuel A. Odría',
                                  'Nicolás Lindley',
                                  'Ricardo Pérez Godoy'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno de Ollanta Humala corresponde al '
                             'periodo:',
                 'alternativas': ['2001-2006',
                                  '2011-2016',
                                  '2006-2011',
                                  '2016-2018',
                                  '1990-1995'],
                 'correcta': 'B'},
                {'pregunta': 'Una medida económica central del primer '
                             'gobierno de Alan García fue:',
                 'alternativas': ['La privatización de empresas',
                                  'La estatización de la banca',
                                  'La firma del contrato Grace',
                                  'La dolarización',
                                  'La apertura comercial total'],
                 'correcta': 'B'}]}]

# ================================================================
# INTERFAZ
# ================================================================

def tab_fichas_historia(config=None):
    st.subheader("📜 Historia — Fichas y banco de preguntas (CEPRU)")
    st.caption("Las 19 balotas del temario oficial de Historia, Área D. "
               "Cada una genera cuatro documentos: ficha para completar y "
               "banco de 20 preguntas, en versión alumno y versión docente.")

    opciones = {f"Balota {t['num']} — {t['titulo']}": t for t in BALOTAS}
    sel = st.selectbox("Balota:", list(opciones.keys()), key="fh_sel")
    tema = opciones[sel]

    c1, c2, c3 = st.columns(3)
    c1.metric("Espacios para completar", contar_espacios(tema))
    c2.metric("Preguntas", len(tema["preguntas"]))
    c3.metric("Cuadros", len(tema.get("cuadros", [])))

    grado_txt = st.text_input("Grupo (se imprime en la ficha):",
                              placeholder="GRUPO CD", key="fh_grado")

    st.markdown("##### Descargar")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("**Ficha de texto para completar**")
        try:
            st.download_button(
                "📄 Versión del alumno",
                data=generar_ficha_texto(tema, False, grado_txt),
                file_name=f"ficha_balota{tema['num']}_alumno.pdf",
                mime="application/pdf", use_container_width=True,
                type="primary", key="fh_fa")
            st.download_button(
                "🔑 Versión del docente (con claves)",
                data=generar_ficha_texto(tema, True, grado_txt),
                file_name=f"ficha_balota{tema['num']}_docente.pdf",
                mime="application/pdf", use_container_width=True, key="fh_fd")
        except Exception as e:
            st.error(f"No se pudo generar la ficha: {e}")
    with d2:
        st.markdown("**Banco de 20 preguntas**")
        try:
            preg = balancear(tema["preguntas"])
            tema_b = {**tema, "preguntas": preg}
            st.download_button(
                "📝 Examen para el alumno",
                data=generar_banco_preguntas(tema_b, False, grado_txt),
                file_name=f"preguntas_balota{tema['num']}_alumno.pdf",
                mime="application/pdf", use_container_width=True,
                type="primary", key="fh_pa")
            st.download_button(
                "🔑 Con claves para el docente",
                data=generar_banco_preguntas(tema_b, True, grado_txt),
                file_name=f"preguntas_balota{tema['num']}_claves.pdf",
                mime="application/pdf", use_container_width=True, key="fh_pd")
        except Exception as e:
            st.error(f"No se pudo generar el banco: {e}")

    st.markdown("---")
    st.markdown("##### Descargar el temario completo")
    st.caption("Genera un solo PDF con las 19 balotas. Tarda unos segundos.")
    g1, g2 = st.columns(2)
    with g1:
        if st.button("📚 Todas las fichas (19 balotas)",
                     use_container_width=True, key="fh_todas_f"):
            with st.spinner("Generando 19 fichas..."):
                try:
                    st.session_state["fh_pdf_todas"] = generar_ficha_texto(
                        _tema_completo(), False, grado_txt)
                    st.session_state["fh_nombre"] = "fichas_historia_completo.pdf"
                except Exception as e:
                    st.error(f"Error: {e}")
    with g2:
        if st.button("📚 Todos los bancos (380 preguntas)",
                     use_container_width=True, key="fh_todas_p"):
            with st.spinner("Generando 380 preguntas..."):
                try:
                    st.session_state["fh_pdf_todas"] = generar_banco_preguntas(
                        _tema_completo(preguntas=True), False, grado_txt)
                    st.session_state["fh_nombre"] = "preguntas_historia_completo.pdf"
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.session_state.get("fh_pdf_todas"):
        st.download_button(
            "⬇️ Descargar documento completo",
            data=st.session_state["fh_pdf_todas"],
            file_name=st.session_state.get("fh_nombre", "historia.pdf"),
            mime="application/pdf", use_container_width=True, key="fh_dl_all")

    with st.expander("Ver el contenido de esta balota"):
        for sec in tema["secciones"]:
            st.markdown(f"**{sec['titulo']}**")
            for it in sec["items"]:
                st.markdown("- " + _PATRON.sub(r"**\1**", it))
        st.markdown("**Primeras cinco preguntas:**")
        for i, p in enumerate(tema["preguntas"][:5], start=1):
            st.markdown(f"{i}. {p['pregunta']}")
            for k, a in enumerate(p["alternativas"]):
                marca = " ✅" if LETRAS[k] == p["correcta"] else ""
                st.markdown(f"   {LETRAS[k]}) {a}{marca}")


def _tema_completo(preguntas=False):
    """Fusiona las 19 balotas en un solo «tema» para imprimir de corrido.

    Se hace así en vez de unir PDFs con una librería externa: el servidor
    no tiene pypdf instalado y no vale la pena agregar una dependencia
    solo para esto.
    """
    secs, cuadros, pregs = [], [], []
    for t in BALOTAS:
        for s in t.get("secciones", []):
            secs.append({"titulo": f"B{t['num']}. {s['titulo']}",
                         "items": s["items"]})
        for c in t.get("cuadros", []):
            cuadros.append({"titulo": f"B{t['num']}. {c['titulo']}",
                            "encabezados": c["encabezados"],
                            "filas": c["filas"]})
        if preguntas:
            for p in balancear(t["preguntas"]):
                pregs.append({**p,
                              "pregunta": f"(B{t['num']}) {p['pregunta']}"})
    return {"num": "1–19", "titulo": "TEMARIO COMPLETO DE HISTORIA",
            "secciones": secs, "cuadros": cuadros, "preguntas": pregs}


def _unir_pdfs(lista):
    """Une varios PDF en uno solo, si hay librería disponible."""
    try:
        from pypdf import PdfWriter, PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfWriter, PdfReader
        except ImportError:
            return None
    w = PdfWriter()
    for b in lista:
        for pag in PdfReader(io.BytesIO(b)).pages:
            w.add_page(pag)
    out = io.BytesIO()
    w.write(out)
    out.seek(0)
    return out.getvalue()
