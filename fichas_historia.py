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


def _proteger_pdf(pdf_bytes):
    """Cifra el PDF para impedir su edición: se abre y se imprime sin
    ninguna contraseña, pero programas como Adobe Acrobat o Word no
    permiten modificar el contenido, agregar/quitar páginas ni rellenar
    formularios sin la contraseña de propietario (que solo tiene la
    academia). Protege el material contra copias editadas o revendidas.
    Si algo falla al cifrar, se entrega el PDF sin proteger antes que
    fallar la descarga completa.
    """
    try:
        from pypdf import PdfReader, PdfWriter
        from pypdf.constants import UserAccessPermissions as _UAP

        reader = PdfReader(io.BytesIO(pdf_bytes))
        writer = PdfWriter()
        for pagina in reader.pages:
            writer.add_page(pagina)

        permisos = _UAP.PRINT | _UAP.PRINT_TO_REPRESENTATION
        writer.encrypt(user_password="", owner_password="YachayCepru2026Seguro",
                       permissions_flag=permisos)

        salida = io.BytesIO()
        writer.write(salida)
        return salida.getvalue()
    except Exception:
        return pdf_bytes


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


def _generar_qr_bytes(texto):
    """Genera un código QR a partir de texto plano y devuelve los bytes
    PNG de la imagen. El QR contiene el texto directamente (no una URL),
    para que funcione sin conexión al escanearlo con cualquier lector."""
    import qrcode
    import io as _io
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(texto)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#12307F", back_color="white")
    buf = _io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _texto_qr_reto(tema, reto):
    """Arma el texto plano del QR de 'Reto Relámpago': 3 preguntas con
    sus respuestas, para autoevaluación instantánea sin internet."""
    lineas = ["🎓 ACADEMIA YACHAY", "Pioneros en la Educación de Calidad", "",
              f"⚡ RETO RELÁMPAGO · {tema['titulo']}", ""]
    for i, pr in enumerate(reto, start=1):
        lineas.append(f"{i}. {pr['pregunta']}")
        lineas.append(f"   ✅ {pr['respuesta']}")
        lineas.append("")
    return "\n".join(lineas).strip()


def _texto_qr_dato(tema, dato):
    """Arma el texto plano del QR de 'Dato Yachay': un dato adicional
    curioso o motivador relacionado con el tema."""
    return (
        "🎓 ACADEMIA YACHAY\nPioneros en la Educación de Calidad\n\n"
        f"✨ DATO YACHAY · {tema['titulo']}\n\n{dato}"
    )


def render_linea(texto, con_claves):
    """Devuelve el texto listo para el PDF.

    con_claves=False -> espacios en blanco proporcionales a la palabra,
                         con la inicial de cada palabra como pista si el
                         hueco tiene varias palabras (ej. "D.......... E..........").
    con_claves=True  -> respuesta en negrita y color, para el docente
    """
    fuera = []
    for tipo, val in _partes(texto):
        if tipo == "fijo":
            fuera.append(val)
        elif con_claves:
            fuera.append(f'<b><font color="#B01C22">{val}</font></b>')
        else:
            palabras = val.split()
            trozos = []
            for palabra in palabras:
                n = max(4, min(int(len(palabra) * 1.5), 20))
                inicial = palabra[0].upper() if palabra[0].isalpha() else ""
                trozos.append(inicial + "." * n)
            fuera.append(f'<font color="#94A3B8">{" ".join(trozos)}</font>')
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
        "marca": ParagraphStyle("m", parent=ss["Title"], fontSize=17,
                                textColor=colors.HexColor("#12307F"),
                                alignment=TA_CENTER, spaceAfter=1, leading=19),
        "lema": ParagraphStyle("l", parent=ss["Normal"], fontSize=9,
                               textColor=colors.HexColor("#B45309"),
                               alignment=TA_CENTER, spaceAfter=6,
                               fontName="Helvetica-Bold"),
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

    _titulo_encabezado = (
        '<font color="#12307F">I.E.P. YACHAY</font>'
        '<font color="#B01C22">  ·  </font>'
        '<font color="#12307F">ACADEMIA YACHAY</font>'
    )
    _lema_espaciado = "&nbsp;&nbsp;".join(" ".join(w) for w in ENCABEZADO_L2.split(" "))
    _marca = [Paragraph(_titulo_encabezado, est["marca"]),
              Paragraph(_lema_espaciado, est["lema"])]
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
            lado = 14 * cm
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
    f_ancho = Frame(MX, 1.4 * cm, ancho_util, alto_full, id="fw",
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    doc.area_actual = area
    doc.profesor_actual = profesor
    doc.addPageTemplates([
        PageTemplate(id="primera", frames=[f_enc, f_c1, f_c2], onPage=_pie),
        PageTemplate(id="resto", frames=[g_c1, g_c2], onPage=_pie),
        PageTemplate(id="ancho", frames=[f_ancho], onPage=_pie),
    ])

    st_ = []
    _banda_titulo(st_, tema,
                  f"{area.upper()} · Temario CEPRU-UNSAAC · " +
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

    def _render_cuadro(cu):
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

    def _auto_ubicar_cuadro(cu, secciones):
        """Si un cuadro no tiene 'despues_de' explícito, intenta ubicarlo
        junto a la sección cuyo número coincide con el prefijo numérico
        del título del cuadro (ej. tabla "4.2 CONSTITUYENTES..." se ubica
        después de la sección "4.2 ..."). Si no hay número o no coincide
        ninguna sección, devuelve None (se mostrará al final, como antes).
        Esto evita cuadros huérfanos que dejan páginas casi vacías.
        """
        m = re.match(r"^(\d+(?:\.\d+)*)", cu.get("titulo", "").strip())
        if not m:
            return None
        numero = m.group(1)
        exactas = [s for s in secciones
                   if re.match(r"^(\d+(?:\.\d+)*)\b", s["titulo"])
                   and re.match(r"^(\d+(?:\.\d+)*)\b", s["titulo"]).group(1) == numero]
        if exactas:
            return exactas[-1]["titulo"]
        prefijo = numero.split(".")[0]
        candidatas = [s for s in secciones
                      if re.match(rf"^{re.escape(prefijo)}\.", s["titulo"])
                      or s["titulo"].startswith(prefijo + " ")]
        if candidatas:
            return candidatas[-1]["titulo"]
        return None

    _cuadros_todos = tema.get("cuadros", [])
    _secciones_tema = tema.get("secciones", [])
    for cu in _cuadros_todos:
        if not cu.get("despues_de"):
            auto = _auto_ubicar_cuadro(cu, _secciones_tema)
            if auto:
                cu["despues_de"] = auto
    _cuadros_intercalados = {id(cu) for cu in _cuadros_todos if cu.get("despues_de")}

    for sec in tema.get("secciones", []):
        st_.append(Spacer(1, 5))
        st_.append(barra(sec["titulo"]))
        st_.append(Spacer(1, 3))
        for it in sec["items"]:
            st_.append(Paragraph("• " + render_linea(it, con_claves), est["n"]))
        # Cuadro(s) que pertenecen justo después de esta sección
        for cu in _cuadros_todos:
            if cu.get("despues_de") == sec["titulo"]:
                _render_cuadro(cu)

    # Cuadros sin posición asignada (o cuyo 'despues_de' no coincidió con
    # ninguna sección): se muestran al final, como antes.
    for cu in _cuadros_todos:
        if id(cu) not in _cuadros_intercalados:
            _render_cuadro(cu)

    # ------------------------------------------------------------------
    # Página final: resumen visual (cuadro sinóptico), si el tema lo trae.
    # Va SIEMPRE con la información completa (sin espacios en blanco),
    # como página de repaso rápido antes del examen — en ambas versiones
    # (alumno y docente), porque no es una pregunta, es un resumen.
    # ------------------------------------------------------------------
    from reportlab.platypus import PageBreak

    def _tinte_claro(hex_color, mezcla_blanco=0.90):
        """Aclara un color hexadecimal mezclándolo con blanco, para usar
        como fondo de fila suave a juego con el color del bloque."""
        c = colors.HexColor(hex_color)
        r = c.red + (1 - c.red) * mezcla_blanco
        g = c.green + (1 - c.green) * mezcla_blanco
        b = c.blue + (1 - c.blue) * mezcla_blanco
        return colors.Color(r, g, b)

    resumen = tema.get("resumen_visual")
    if resumen:
        st_.append(NextPageTemplate("ancho"))
        st_.append(PageBreak())
        st_.append(Spacer(1, 4))
        titulo_resumen = Table(
            [[Paragraph(f"<b>RESUMEN VISUAL · {tema['titulo'].upper()}</b>", est["h"])]],
            colWidths=[ancho_util])
        titulo_resumen.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#B01C22")),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        st_.append(titulo_resumen)
        st_.append(Spacer(1, 8))

        n_bloques = len(resumen)
        ancho_bloque = (ancho_util - 0.6 * cm * (min(n_bloques, 2) - 1)) / min(n_bloques, 2) \
            if n_bloques > 1 else ancho_util
        _paleta_bloques = [
            "#4A6FA5",  # azul
            "#5B8C5A",  # verde
            "#9B5FA8",  # morado
            "#C97A3D",  # naranja/terracota
            "#3D8C8C",  # turquesa
            "#B85C7A",  # rosa/coral
            "#6B7FBF",  # índigo
            "#A8874A",  # dorado/mostaza
        ]
        fila_actual = []
        for _idx_bloque, bloque in enumerate(resumen):
            _color_bloque = _paleta_bloques[_idx_bloque % len(_paleta_bloques)]
            cab = Table([[Paragraph(f"<b>{bloque['titulo']}</b>", est["cel"])]],
                       colWidths=[ancho_bloque - 8])
            cab.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(_color_bloque)),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ]))
            # Construir filas: cada item puede ser "texto" simple o (etiqueta, contenido)
            data_rows = []
            for item in bloque["items"]:
                if isinstance(item, (list, tuple)):
                    data_rows.append([Paragraph(f"<b>{item[0]}</b>", est["cel"]),
                                      Paragraph(item[1], est["cel"])])
                else:
                    data_rows.append([Paragraph("• " + item, est["cel"])])
            if data_rows and len(data_rows[0]) == 2:
                cw = [ancho_bloque * 0.4, ancho_bloque * 0.6 - 8]
            else:
                cw = [ancho_bloque - 8]
            tbl = Table(data_rows, colWidths=cw)
            tbl.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#8894A8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1),
                 [colors.white, _tinte_claro(_color_bloque)]),
            ]))
            celda = [cab, Spacer(1, 0), tbl]
            fila_actual.append(celda)
            if len(fila_actual) == 2 or bloque is resumen[-1]:
                if len(fila_actual) == 1:
                    grid = Table([[fila_actual[0], ""]],
                                 colWidths=[ancho_bloque, ancho_bloque])
                else:
                    grid = Table([fila_actual], colWidths=[ancho_bloque, ancho_bloque])
                grid.setStyle(TableStyle([
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (0, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]))
                st_.append(grid)
                fila_actual = []

        qr_reto = tema.get("qr_reto")
        qr_dato = tema.get("qr_dato")
        if qr_reto or qr_dato:
            from reportlab.platypus import Image as RLImage
            st_.append(Spacer(1, 14))
            celdas_qr = []
            ancho_qr = 3.2 * cm
            if qr_reto:
                png = _generar_qr_bytes(_texto_qr_reto(tema, qr_reto))
                img = RLImage(io.BytesIO(png), width=ancho_qr, height=ancho_qr)
                celdas_qr.append([
                    img,
                    Paragraph("<b>⚡ Reto Relámpago</b><br/>Escanea y autoevalúate", est["cel"]),
                ])
            if qr_dato:
                png = _generar_qr_bytes(_texto_qr_dato(tema, qr_dato))
                img = RLImage(io.BytesIO(png), width=ancho_qr, height=ancho_qr)
                celdas_qr.append([
                    img,
                    Paragraph("<b>✨ Dato Yachay</b><br/>Un dato extra para recordar", est["cel"]),
                ])
            fila_qr = []
            for img, etiqueta in celdas_qr:
                fila_qr.append(img)
                fila_qr.append(etiqueta)
            tabla_qr = Table([fila_qr],
                              colWidths=[ancho_qr, 4.5 * cm] * len(celdas_qr))
            tabla_qr.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]))
            st_.append(tabla_qr)

    doc.build(st_)
    buf.seek(0)
    return _proteger_pdf(buf.getvalue())


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


TAMANOS_EXAMEN = {
    "2 páginas (≈20 preguntas)": 20,
    "4 páginas (≈55 preguntas)": 55,
}


def muestrear(preguntas, cantidad, semilla=None):
    """Elige al azar `cantidad` preguntas del banco completo.

    Sirve para que el examen no sea siempre exactamente el mismo aun
    cuando el banco tenga muchas más preguntas de las que caben en el
    tamaño elegido (2 o 4 hojas): cada vez que se pide "otra
    combinación" (semilla distinta), sale una selección distinta,
    manteniendo la misma cantidad de preguntas y el mismo reparto de
    letras al pasar después por balancear().

    Si el banco tiene menos preguntas que `cantidad`, se devuelven
    todas (no se puede pedir más de las que hay).
    """
    import random
    if len(preguntas) <= cantidad:
        return list(preguntas)
    rng = random.Random(semilla)
    return rng.sample(list(preguntas), cantidad)


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

    alto_enc = 4.4 * cm
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
    return _proteger_pdf(buf.getvalue())


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
                {'titulo': '1.4 FUENTES DE LA HISTORIA: CONCEPTO Y '
                           'CLASIFICACIÓN',
                 'items': ['Las {fuentes de la historia} son restos, '
                           'huellas, evidencias y testimonios que dan cuenta '
                           'del pasado y sirven para reconstruir la '
                           'historia.',
                           'Las fuentes {materiales} o monumentales incluyen '
                           'construcciones arquitectónicas, cerámica, '
                           'textiles, tumbas, esculturas y {herramientas}.',
                           'Las fuentes {orales} o tradicionales son relatos '
                           'verbales transmitidos de generación en '
                           'generación: topónimos, leyendas, mitos y '
                           '{costumbres}.',
                           'Las fuentes {escritas}, o documentales, son '
                           'testimonios dejados por medio de la escritura, '
                           'en piedra, papiros, manuscritos y {crónicas}.',
                           'Las fuentes {antroposomáticas} son restos '
                           'físicos humanos —cabellos, uñas, huesos, momias— '
                           'que revelan el desarrollo físico y étnico del '
                           'hombre.',
                           'Las fuentes {audiovisuales} son testimonios '
                           'tecnológicos que registran voces, sonidos e '
                           'imágenes, como los «vladivideos» y '
                           '«{petroaudios}».']}],
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
                          'Audios, videos, fotografías, «{vladivideos}»']]},
              {'titulo': '1.4 CLASIFICACIÓN DE LAS FUENTES HISTÓRICAS',
               'encabezados': ['Tipo de fuente', 'Ejemplo'],
               'filas': [['{Materiales}', 'Cerámica, {tumbas}, esculturas'],
                         ['{Orales}', 'Leyendas, mitos, {costumbres}'],
                         ['{Escritas}', 'Crónicas, {manuscritos}, libros'],
                         ['{Antroposomáticas}', 'Momias, {huesos}, cabellos'],
                         ['{Audiovisuales}',
                          'Fotografías, {videos}, audios']]}],
  'preguntas': [{'pregunta': 'La historia como ciencia estudia los hechos y '
                             'procesos sociales del pasado en función de '
                             'sus:',
                 'alternativas': ['Restos arqueológicos',
                                  'Mitos y leyendas',
                                  'Causas y consecuencias',
                                  'Fechas y personajes',
                                  'Fuentes escritas únicamente'],
                 'correcta': 'C'},
                {'pregunta': 'Según Heródoto, los dos ojos de la historia '
                             'son:',
                 'alternativas': ['La sociedad y la cultura',
                                  'El hecho y la fuente',
                                  'La causa y el efecto',
                                  'El tiempo y el espacio',
                                  'El mito y la razón'],
                 'correcta': 'D'},
                {'pregunta': '¿Cuál NO es un componente esencial del '
                             'acontecimiento histórico?',
                 'alternativas': ['La tecnología',
                                  'Ninguno, los tres primeros lo son',
                                  'La sociedad',
                                  'El espacio',
                                  'El tiempo'],
                 'correcta': 'A'},
                {'pregunta': 'Los topónimos, las leyendas y los cantos '
                             'corresponden a fuentes:',
                 'alternativas': ['Antroposomáticas',
                                  'Materiales',
                                  'Audiovisuales',
                                  'Escritas',
                                  'Orales o tradicionales'],
                 'correcta': 'E'},
                {'pregunta': 'Las momias, los cabellos y los huesos son '
                             'fuentes:',
                 'alternativas': ['Audiovisuales',
                                  'Antroposomáticas',
                                  'Orales',
                                  'Monumentales',
                                  'Documentales'],
                 'correcta': 'B'},
                {'pregunta': 'Los llamados «vladivideos» y «petroaudios» '
                             'constituyen fuentes:',
                 'alternativas': ['Audiovisuales',
                                  'Antroposomáticas',
                                  'Escritas',
                                  'Materiales',
                                  'Tradicionales'],
                 'correcta': 'A'},
                {'pregunta': 'La institución encargada de la preservación '
                             'del patrimonio cultural peruano es:',
                 'alternativas': ['El Congreso de la República',
                                  'El INC',
                                  'La UNESCO',
                                  'El Ministerio de Cultura',
                                  'El Ministerio de Educación'],
                 'correcta': 'D'},
                {'pregunta': 'El fondo documental del Estado peruano es '
                             'custodiado por:',
                 'alternativas': ['El Ministerio de Cultura',
                                  'El Archivo Regional del Cusco',
                                  'El Archivo General de la Nación',
                                  'La UNSAAC',
                                  'La Biblioteca Nacional'],
                 'correcta': 'C'},
                {'pregunta': 'El folclore, la tradición y la cultura viva de '
                             'los pueblos forman parte de la cultura:',
                 'alternativas': ['Inmaterial',
                                  'Monumental',
                                  'Material',
                                  'Documental',
                                  'Arqueológica'],
                 'correcta': 'A'},
                {'pregunta': 'Las crónicas y los manuscritos coloniales son '
                             'fuentes:',
                 'alternativas': ['Escritas',
                                  'Orales',
                                  'Antroposomáticas',
                                  'Audiovisuales',
                                  'Materiales'],
                 'correcta': 'A'},
                {'pregunta': 'La historia «como hecho» se refiere a:',
                 'alternativas': ['Los acontecimientos y procesos sociales '
                                  'del pasado',
                                  'La conservación del patrimonio',
                                  'La crítica de las fuentes',
                                  'El método de estudio del pasado',
                                  'La periodificación cronológica'],
                 'correcta': 'A'},
                {'pregunta': 'El propósito final del estudio de la historia, '
                             'según el texto, es:',
                 'alternativas': ['Memorizar fechas exactas',
                                  'Escribir crónicas',
                                  'Coleccionar restos arqueológicos',
                                  'Comprender el presente y proyectarse al '
                                  'futuro',
                                  'Defender una ideología'],
                 'correcta': 'D'},
                {'pregunta': 'Las construcciones arquitectónicas, la '
                             'cerámica y los textiles corresponden a '
                             'fuentes:',
                 'alternativas': ['Escritas',
                                  'Audiovisuales',
                                  'Antroposomáticas',
                                  'Orales',
                                  'Materiales o monumentales'],
                 'correcta': 'E'},
                {'pregunta': 'La dimensión temporal de larga duración se '
                             'refiere a:',
                 'alternativas': ['Un hecho puntual',
                                  'La cronología absoluta',
                                  'Un acontecimiento anual',
                                  'La biografía de un personaje',
                                  'Procesos que abarcan siglos'],
                 'correcta': 'E'},
                {'pregunta': 'El Archivo Regional del Cusco (A.R.C.) es una '
                             'institución de:',
                 'alternativas': ['Gobierno regional exclusivo',
                                  'Educación básica regular',
                                  'Recaudación tributaria',
                                  'Investigación y difusión del patrimonio '
                                  'cultural',
                                  'Turismo receptivo'],
                 'correcta': 'D'},
                {'pregunta': 'El estudio sistemático, verídico y metódico '
                             'corresponde a la historia entendida como:',
                 'alternativas': ['Ciencia',
                                  'Patrimonio',
                                  'Tradición',
                                  'Hecho',
                                  'Mito'],
                 'correcta': 'A'},
                {'pregunta': 'El espacio como componente histórico puede '
                             'ser:',
                 'alternativas': ['Únicamente continental',
                                  'Solo local',
                                  'Solo nacional',
                                  'Solo urbano',
                                  'Local, regional, nacional, continental o '
                                  'mundial'],
                 'correcta': 'E'},
                {'pregunta': 'La obligación de cuidar y conservar el '
                             'patrimonio cultural corresponde a:',
                 'alternativas': ['Solo a los arqueólogos',
                                  'La UNESCO',
                                  'Los gobiernos regionales únicamente',
                                  'Solo al Ministerio de Cultura',
                                  'El Estado y la comunidad nacional'],
                 'correcta': 'E'},
                {'pregunta': 'Los idiomas y las creencias transmitidas de '
                             'padres a hijos son fuentes:',
                 'alternativas': ['Monumentales',
                                  'Somáticas',
                                  'Orales',
                                  'Escritas',
                                  'Audiovisuales'],
                 'correcta': 'C'},
                {'pregunta': 'Señale la afirmación CORRECTA sobre las '
                             'fuentes históricas:',
                 'alternativas': ['Son restos, huellas y testimonios '
                                  'materiales e inmateriales',
                                  'Únicamente las produce el Estado',
                                  'Se limitan a los restos arqueológicos',
                                  'Solo existen desde la invención de la '
                                  'imprenta',
                                  'Solo las escritas son válidas'],
                 'correcta': 'A'},
                {'pregunta': 'Las inscripciones dejadas por el hombre en '
                             'diversos materiales como piedras, metales, '
                             'telas, manuscritos y textos se denominan '
                             'fuentes: (UNSAAC 2010)',
                 'alternativas': ['Secundarias',
                                  'Materiales o monumentales',
                                  'Orales o tradicionales',
                                  'Primarias',
                                  'Escritas'],
                 'correcta': 'E'},
                {'pregunta': 'Los fragmentos de restos óseos humanos que '
                             'sirven para conocer el grado de desarrollo '
                             'físico del hombre son fuentes: (UNSAAC 2010)',
                 'alternativas': ['Escritas',
                                  'Audiovisuales',
                                  'Orales',
                                  'Antroposomáticas',
                                  'Monumentales'],
                 'correcta': 'D'},
                {'pregunta': 'Un video sobre Sacsayhuamán es una fuente: '
                             '(UNSAAC 2011)',
                 'alternativas': ['Material',
                                  'Oral',
                                  'Tradicional',
                                  'Audiovisual',
                                  'Escrita'],
                 'correcta': 'D'},
                {'pregunta': 'El enunciado «la Universidad Nacional de San '
                             'Antonio del Cusco fue fundada el 1 de marzo de '
                             '1692» corresponde a la cronología: (UNSAAC '
                             '2013)',
                 'alternativas': ['Verdadera',
                                  'Absoluta',
                                  'Relativa',
                                  'Válida',
                                  'Aproximada'],
                 'correcta': 'B'},
                {'pregunta': 'El mito de los Hermanos Ayar y la Crónica de '
                             'Inca Garcilaso de la Vega representan, '
                             'respectivamente, a las fuentes históricas: '
                             '(UNSAAC 2013)',
                 'alternativas': ['Oral - Tradicional',
                                  'Tradicional - Material',
                                  'Cronística - Escrita',
                                  'Antroposomática - Documental',
                                  'Oral - Escrita'],
                 'correcta': 'E'},
                {'pregunta': 'Los mitos y las crónicas pertenecen '
                             'respectivamente a las fuentes históricas: '
                             '(UNSAAC 2015)',
                 'alternativas': ['Monumentales y tradicionales',
                                  'Tradicionales y materiales',
                                  'Orales y escritas',
                                  'Antroposomáticas y etnológicas',
                                  'Abstractas y concretas'],
                 'correcta': 'C'},
                {'pregunta': 'Los restos físicos humanos que sirven para '
                             'estudiar el grado de desarrollo étnico del '
                             'hombre corresponden a las fuentes: (UNSAAC '
                             '2016)',
                 'alternativas': ['Biológicas',
                                  'Escritas',
                                  'Tradicionales',
                                  'Antroposomáticas',
                                  'Culturales'],
                 'correcta': 'D'},
                {'pregunta': 'Los testimonios tradicionales, costumbres y '
                             'creencias de los grupos humanos son una '
                             'fuente: (UNSAAC 2018)',
                 'alternativas': ['Monumental',
                                  'Oral',
                                  'Escrita',
                                  'Antroposomática',
                                  'Audiovisual'],
                 'correcta': 'B'},
                {'pregunta': 'La institución encargada de cuidar y conservar '
                             'el patrimonio histórico del Perú es el '
                             'Ministerio de: (UNSAAC 2022)',
                 'alternativas': ['Justicia',
                                  'Cultura',
                                  'Industria y Turismo',
                                  'Economía',
                                  'Educación'],
                 'correcta': 'B'},
                {'pregunta': 'Las crónicas y los periódicos son fuentes de '
                             'tipo: (UNSAAC 2023)',
                 'alternativas': ['Antroposomático',
                                  'Material',
                                  'Monumental',
                                  'Documental',
                                  'Audiovisual'],
                 'correcta': 'D'},
                {'pregunta': 'La ciencia que estudia el pasado, a partir del '
                             'presente con proyección al futuro, es la: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Arqueología',
                                  'Etnología',
                                  'Astrología',
                                  'Cronología',
                                  'Historia'],
                 'correcta': 'E'},
                {'pregunta': 'El folclore es una fuente histórica: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Tradicional',
                                  'Audiovisual',
                                  'Tecnológica',
                                  'Monumental',
                                  'Cronística'],
                 'correcta': 'A'},
                {'pregunta': 'Los restos humanos como esqueletos y huesos '
                             'fosilizados corresponden a las fuentes '
                             'históricas: (UNSAAC Ordinario)',
                 'alternativas': ['Orales',
                                  'Materiales',
                                  'Audiovisuales',
                                  'Antroposomáticas',
                                  'Monumentales'],
                 'correcta': 'D'},
                {'pregunta': 'Los restos físicos humanos como cabellos, '
                             'uñas, huesos y momias, corresponden a las '
                             'fuentes: (UNSAAC Ordinario)',
                 'alternativas': ['Orales',
                                  'Audiovisuales',
                                  'Antroposomáticas',
                                  'Tradicionales',
                                  'Numismática'],
                 'correcta': 'C'},
                {'pregunta': 'Al periodo carente de documentos escritos, se '
                             'conoce como: (I CEPRU 2010)',
                 'alternativas': ['Cronología',
                                  'Historiografía',
                                  'Poshistoria',
                                  'Prehistoria',
                                  'Historia'],
                 'correcta': 'D'},
                {'pregunta': 'El estudio de los fragmentos que permite '
                             'conocer el grado de desarrollo físico y étnico '
                             'del hombre, corresponde a las fuentes: (I '
                             'CEPRU 2011)',
                 'alternativas': ['Escritas',
                                  'Orales',
                                  'Antroposomáticas',
                                  'Materiales',
                                  'Audiovisuales'],
                 'correcta': 'C'},
                {'pregunta': 'Los restos óseos humanos son fuentes: (I CEPRU '
                             '2012)',
                 'alternativas': ['Materiales',
                                  'Monumentales',
                                  'Culturales',
                                  'Antroposomáticas',
                                  'Tradicionales'],
                 'correcta': 'D'},
                {'pregunta': 'La paleontología es una ciencia que estudia: '
                             '(I CEPRU 2012)',
                 'alternativas': ['Los restos fósiles',
                                  'Los manuscritos antiguos',
                                  'Al hombre en la sociedad',
                                  'Los escudos y blasones',
                                  'La superficie terrestre'],
                 'correcta': 'A'},
                {'pregunta': 'Los testimonios de carácter tecnológico, '
                             'corresponde a las fuentes: (I CEPRU 2013)',
                 'alternativas': ['Naturales',
                                  'Materiales o monumentales',
                                  'Escritas',
                                  'Audiovisuales',
                                  'Culturales'],
                 'correcta': 'B'},
                {'pregunta': 'La ciencia que ubica, describe y explica la '
                             'superficie terrestre donde se producen los '
                             'acontecimientos históricos es la: (I CEPRU '
                             '2013)',
                 'alternativas': ['Geografía',
                                  'Cronología',
                                  'Teología',
                                  'Paleografía',
                                  'Historia'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'CONCEPTO',
                      'items': ['La historia como ciencia estudia en forma '
                                'sistemática, verídica y metódica los hechos '
                                'y procesos sociales del pasado, a través '
                                'del análisis e interpretación de diversos '
                                'tipos de fuentes.',
                                'Estudia los hechos en función de sus causas '
                                'y consecuencias, con el propósito de '
                                'comprender el presente y proyectarse al '
                                'futuro.',
                                'La historia como hecho se refiere a todos '
                                'los acontecimientos y procesos sociales del '
                                'pasado, desde el origen de la humanidad '
                                'hasta la actualidad.']},
                     {'titulo': 'COMPONENTES DE LA HISTORIA',
                      'items': ['Heródoto, padre de la historia, decía que '
                                'los dos ojos de la historia son el tiempo y '
                                'el espacio.',
                                'La Sociedad: comprende a hombres y mujeres '
                                'como actores de la historia.',
                                'El Tiempo: cronología absoluta o relativa, '
                                'y dimensiones de corta, mediana y larga '
                                'duración.',
                                'El Espacio: área geográfica local, '
                                'regional, nacional, continental o mundial '
                                'que sirve de escenario.']},
                     {'titulo': 'LA HISTORIA COMO PATRIMONIO',
                      'items': ['Patrimonio histórico es todo el legado '
                                'social y cultural dejado por nuestros '
                                'ancestros a lo largo del proceso histórico '
                                'peruano.',
                                'Comprende la cultura material (restos '
                                'arqueológicos, patrimonio natural, legado '
                                'artístico) y la cultura inmaterial '
                                '(folclore, tradición, cultura viva).',
                                'La institución encargada de su preservación '
                                'es el Ministerio de Cultura.',
                                'La Biblioteca Nacional del Perú custodia el '
                                'fondo bibliográfico y el Archivo General de '
                                'la Nación el fondo documental.']},
                     {'titulo': 'FUENTES DE LA HISTORIA: CONCEPTO Y '
                                'CLASIFICACIÓN',
                      'items': ['Las fuentes de la historia son restos, '
                                'huellas, evidencias y testimonios que dan '
                                'cuenta del pasado y sirven para reconstruir '
                                'la historia.',
                                'Las fuentes materiales o monumentales '
                                'incluyen construcciones arquitectónicas, '
                                'cerámica, textiles, tumbas, esculturas y '
                                'herramientas.',
                                'Las fuentes orales o tradicionales son '
                                'relatos verbales transmitidos de generación '
                                'en generación: topónimos, leyendas, mitos y '
                                'costumbres.',
                                'Las fuentes escritas, o documentales, son '
                                'testimonios dejados por medio de la '
                                'escritura, en piedra, papiros, manuscritos '
                                'y crónicas.',
                                'Las fuentes antroposomáticas son restos '
                                'físicos humanos —cabellos, uñas, huesos, '
                                'momias— que revelan el desarrollo físico y '
                                'étnico del hombre.',
                                'Las fuentes audiovisuales son testimonios '
                                'tecnológicos que registran voces, sonidos e '
                                'imágenes, como los «vladivideos» y '
                                '«petroaudios».']}],
  'qr_reto': [{'pregunta': 'La historia «como hecho» se refiere a:',
               'respuesta': 'Los acontecimientos y procesos sociales del '
                            'pasado'},
              {'pregunta': 'El fondo documental del Estado peruano es '
                           'custodiado por:',
               'respuesta': 'El Archivo General de la Nación'},
              {'pregunta': 'El folclore es una fuente histórica:',
               'respuesta': 'Tradicional'}],
  'qr_dato': 'Las fuentes de la historia son restos, huellas, evidencias y '
             'testimonios que dan cuenta del pasado y sirven para '
             'reconstruir la historia.'},
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
                {'titulo': '2.4 LA EDAD DE LOS METALES',
                 'items': ['La Edad de los Metales se caracteriza por el '
                           'abandono gradual de instrumentos de {piedra}, '
                           'reemplazados por metales fundidos.',
                           'La Edad del {Cobre} o Calcolítico (5000-3000 '
                           'a.C.) es la transición entre la Edad de Piedra y '
                           'la Edad de los Metales.',
                           'El uso del cobre fundido se inició en '
                           '{Çatalhöyük}, actual Turquía, hacia el 5000 a.C.',
                           'La Edad del {Bronce} (3000-1500 a.C.) comenzó en '
                           'Sumeria; el bronce es la aleación de cobre y '
                           '{estaño}.',
                           'El bronce se usó para fabricar armas como '
                           'espadas y {escudos}, y utensilios agrícolas como '
                           'hoces.',
                           'La Edad del {Hierro} (1500-18 a.C.) fue iniciada '
                           'por los {hititas} de Turquía.',
                           'El hierro tenía dos ventajas sobre el bronce: '
                           'mayor {abundancia} del mineral, y mayor {dureza} '
                           'de las armas.']}],
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
                 'alternativas': ['La aparición de la escritura',
                                  'La capacidad de fabricar objetos',
                                  'La vida sedentaria',
                                  'El descubrimiento del fuego',
                                  'La domesticación de animales'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría evolucionista fue formulada por:',
                 'alternativas': ['Daniel Wilson',
                                  'Christian Thomsen',
                                  'Boucher de Perthes',
                                  'Heródoto',
                                  'Charles Darwin'],
                 'correcta': 'E'},
                {'pregunta': 'El término «prehistoria» se refiere al periodo '
                             'anterior a la aparición de:',
                 'alternativas': ['La rueda',
                                  'Los metales',
                                  'La cerámica',
                                  'La agricultura',
                                  'La escritura'],
                 'correcta': 'E'},
                {'pregunta': 'Christian Thomsen dividió la prehistoria '
                             'observando:',
                 'alternativas': ['Los restos óseos',
                                  'Los materiales de las herramientas',
                                  'Los enterramientos',
                                  'Las pinturas rupestres',
                                  'Las glaciaciones'],
                 'correcta': 'B'},
                {'pregunta': 'La técnica osteodontoquerática consistió en el '
                             'uso de:',
                 'alternativas': ['Fibras vegetales',
                                  'Metales fundidos',
                                  'Piedra pulimentada',
                                  'Arcilla cocida',
                                  'Huesos de mandíbula de animales'],
                 'correcta': 'E'},
                {'pregunta': 'Altamira y Lascaux son famosas por su:',
                 'alternativas': ['Escritura cuneiforme',
                                  'Arquitectura megalítica',
                                  'Cerámica policroma',
                                  'Arte rupestre',
                                  'Metalurgia del bronce'],
                 'correcta': 'D'},
                {'pregunta': 'El hombre del Paleolítico se caracterizó por '
                             'ser:',
                 'alternativas': ['Nómada y cavernícola',
                                  'Ganadero y alfarero',
                                  'Comerciante y navegante',
                                  'Sedentario y agricultor',
                                  'Urbano y estatal'],
                 'correcta': 'A'},
                {'pregunta': 'La organización social del Paleolítico '
                             'comprendió:',
                 'alternativas': ['Imperios centralizados',
                                  'Ayllus y curacazgos',
                                  'Ciudades-Estado',
                                  'Hordas, clanes y gens',
                                  'Reinos hereditarios'],
                 'correcta': 'D'},
                {'pregunta': 'El tótem en el Paleolítico era:',
                 'alternativas': ['Un instrumento musical',
                                  'Un antepasado común sacralizado',
                                  'Una herramienta de sílex',
                                  'Un tipo de sepultura',
                                  'Una vivienda sobre pilotes'],
                 'correcta': 'B'},
                {'pregunta': 'El Mesolítico es el periodo de transición '
                             'entre:',
                 'alternativas': ['Edad del Bronce y del Hierro',
                                  'Neolítico y Edad de los Metales',
                                  'Holoceno y Pleistoceno',
                                  'Pleistoceno y Holoceno',
                                  'Paleolítico y Edad del Cobre'],
                 'correcta': 'D'},
                {'pregunta': 'La primera gran revolución agrícola y ganadera '
                             'corresponde al:',
                 'alternativas': ['Calcolítico',
                                  'Edad del Hierro',
                                  'Mesolítico',
                                  'Neolítico',
                                  'Paleolítico'],
                 'correcta': 'D'},
                {'pregunta': 'Los palafitos fueron:',
                 'alternativas': ['Vasijas rituales',
                                  'Templos escalonados',
                                  'Tumbas colectivas',
                                  'Casas de madera sobre pilotes',
                                  'Herramientas de sílex'],
                 'correcta': 'D'},
                {'pregunta': 'Los dólmenes, menhires y crómlech son '
                             'expresiones de arquitectura:',
                 'alternativas': ['Militar',
                                  'Palaciega',
                                  'Funeraria y religiosa',
                                  'Doméstica',
                                  'Hidráulica'],
                 'correcta': 'C'},
                {'pregunta': 'Stonehenge, importante monumento megalítico, '
                             'se ubica en:',
                 'alternativas': ['España',
                                  'Turquía',
                                  'Inglaterra',
                                  'Suiza',
                                  'Francia'],
                 'correcta': 'C'},
                {'pregunta': 'En el Neolítico surgen por primera vez:',
                 'alternativas': ['La osteodontoquerática',
                                  'El nomadismo y la caza',
                                  'El arte rupestre',
                                  'La propiedad privada, las clases sociales '
                                  'y el Estado',
                                  'Las glaciaciones'],
                 'correcta': 'D'},
                {'pregunta': 'El uso del cobre fundido se inició en:',
                 'alternativas': ['Babilonia',
                                  'Nínive',
                                  'Menfis',
                                  'Çatalhöyük (Turquía)',
                                  'Ur'],
                 'correcta': 'D'},
                {'pregunta': 'El bronce es una aleación de cobre con:',
                 'alternativas': ['Plomo',
                                  'Estaño',
                                  'Zinc',
                                  'Hierro',
                                  'Plata'],
                 'correcta': 'B'},
                {'pregunta': 'Etimológicamente, «Neolítico» significa:',
                 'alternativas': ['Piedra media',
                                  'Edad del hielo',
                                  'Edad del metal',
                                  'Piedra nueva o pulimentada',
                                  'Piedra antigua'],
                 'correcta': 'D'},
                {'pregunta': 'La bipedación trajo como consecuencia directa:',
                 'alternativas': ['La aparición del lenguaje escrito',
                                  'La construcción de ciudades',
                                  'La domesticación del perro',
                                  'El uso exclusivo de las extremidades '
                                  'inferiores para desplazarse',
                                  'El aumento del cráneo'],
                 'correcta': 'D'},
                {'pregunta': 'La primera ciudad prehistórica construida '
                             'sobre un lago se descubrió en:',
                 'alternativas': ['El lago Titicaca',
                                  'El lago Zúrich, Suiza',
                                  'El lago Ness',
                                  'El lago Van',
                                  'El mar Muerto'],
                 'correcta': 'B'},
                {'pregunta': 'La Edad de los Metales se caracteriza por el '
                             'abandono gradual de instrumentos de:',
                 'alternativas': ['Bronce',
                                  'Piedra',
                                  'Hierro',
                                  'Cobre',
                                  'Barro'],
                 'correcta': 'B'},
                {'pregunta': 'La primera etapa de la Edad de los Metales, '
                             'transición desde la Edad de Piedra, se llama:',
                 'alternativas': ['Edad del Bronce',
                                  'Edad del Cobre o Calcolítico',
                                  'Edad del Hierro',
                                  'Edad del Estaño',
                                  'Edad del Oro'],
                 'correcta': 'B'},
                {'pregunta': 'El uso del cobre fundido se inició hacia el '
                             '5000 a.C. en:',
                 'alternativas': ['Mesopotamia',
                                  'Çatalhöyük, actual Turquía',
                                  'Egipto',
                                  'Grecia',
                                  'China'],
                 'correcta': 'B'},
                {'pregunta': 'El bronce es la aleación de cobre y:',
                 'alternativas': ['Hierro',
                                  'Estaño',
                                  'Plata',
                                  'Oro',
                                  'Plomo'],
                 'correcta': 'B'},
                {'pregunta': 'El uso del bronce comenzó hacia el 3000 a.C. '
                             'en:',
                 'alternativas': ['Egipto',
                                  'Sumeria (Mesopotamia)',
                                  'Grecia',
                                  'Roma',
                                  'China'],
                 'correcta': 'B'},
                {'pregunta': 'Con bronce se fabricaron armas como espadas, '
                             'dagas y:',
                 'alternativas': ['Solo ollas',
                                  'Escudos',
                                  'Solo joyas',
                                  'Solo herramientas agrícolas',
                                  'Ruedas'],
                 'correcta': 'B'},
                {'pregunta': 'El pueblo que primero utilizó el hierro '
                             'fundido, hacia 1500 a.C., fue:',
                 'alternativas': ['Los sumerios',
                                  'Los hititas de Turquía',
                                  'Los egipcios',
                                  'Los fenicios',
                                  'Los griegos'],
                 'correcta': 'B'},
                {'pregunta': 'Una de las ventajas del hierro frente al '
                             'bronce es su mayor:',
                 'alternativas': ['Escasez',
                                  'Abundancia como mineral',
                                  'Fragilidad',
                                  'Costo',
                                  'Peso'],
                 'correcta': 'B'},
                {'pregunta': 'Otra ventaja del hierro frente al bronce es '
                             'que sus armas son más:',
                 'alternativas': ['Frágiles',
                                  'Duras',
                                  'Livianas exclusivamente',
                                  'Costosas exclusivamente',
                                  'Difíciles de fabricar'],
                 'correcta': 'B'},
                {'pregunta': 'En Europa, el uso del hierro comenzó con la '
                             'cultura de Hallstatt, ubicada en:',
                 'alternativas': ['Turquía',
                                  'Austria',
                                  'Grecia',
                                  'Italia',
                                  'España'],
                 'correcta': 'B'},
                {'pregunta': 'El hombre del paleolítico se expresó mediante '
                             'el: (UNSAAC 2010)',
                 'alternativas': ['Intercambio de productos',
                                  'Cultivo',
                                  'Arte rupestre',
                                  'Culto religioso',
                                  'Arte textil'],
                 'correcta': 'C'},
                {'pregunta': 'Una de las características del hombre del '
                             'neolítico fue ser: (UNSAAC 2010)',
                 'alternativas': ['Pescador',
                                  'Nómada',
                                  'Cazador, pescador y recolector',
                                  'Sedentario',
                                  'Antropólogo'],
                 'correcta': 'D'},
                {'pregunta': 'Se conoce como troglodita al hombre del: '
                             '(UNSAAC 2011)',
                 'alternativas': ['Neolítico',
                                  'Paleolítico',
                                  'Mesolítico',
                                  'Palafítico',
                                  'Epipaleolítico'],
                 'correcta': 'B'},
                {'pregunta': 'El hombre del Neolítico se caracteriza por '
                             'ser: (UNSAAC 2011)',
                 'alternativas': ['Sedentario, agricultor, ganadero',
                                  'Cazador, recolector, pescador',
                                  'Horticultor, recolector, pescador',
                                  'Nómade, ganadero, horticultor',
                                  'Agricultor, nómade, pescador'],
                 'correcta': 'A'},
                {'pregunta': 'Los raspadores y machacadores son considerados '
                             'objetos líticos más antiguos que pertenecieron '
                             'al hombre de: (UNSAAC 2011)',
                 'alternativas': ['Toquepala',
                                  'Paccaicasa',
                                  'Lauricocha',
                                  'Paiján',
                                  'Chivateros'],
                 'correcta': 'B'},
                {'pregunta': 'Los rasgos fundamentales de la Hominización '
                             'son la: (UNSAAC 2013)',
                 'alternativas': ['Bipedación y fabricación de objetos',
                                  'Sedentarización y domesticación',
                                  'Culturización y civilización',
                                  'Sociabilización y diferenciación social',
                                  'Semisedentarización y totemización'],
                 'correcta': 'A'},
                {'pregunta': 'El descubrimiento del fuego ocurrió en: '
                             '(UNSAAC 2013)',
                 'alternativas': ['El neolítico',
                                  'La Edad Antigua',
                                  'La Edad Histórica',
                                  'El paleolítico',
                                  'El mesolítico'],
                 'correcta': 'D'},
                {'pregunta': 'El periodo mesolítico de la Edad de Piedra se '
                             'caracterizó por: (UNSAAC 2014)',
                 'alternativas': ['El surgimiento de la familia y la '
                                  'propiedad privada',
                                  'El descubrimiento del fuego',
                                  'Una economía exclusivamente recolectora',
                                  'La finalización de las glaciaciones',
                                  'La práctica del culto al muerto'],
                 'correcta': 'D'},
                {'pregunta': 'Los rasgos característicos del proceso de '
                             'hominización fue la: (UNSAAC 2015)',
                 'alternativas': ['Capacidad de fabricar objetos',
                                  'Noción de la existencia de Dios',
                                  'Domesticación de plantas',
                                  'Vida sedentaria del hombre',
                                  'Construcción de las primeras viviendas'],
                 'correcta': 'A'},
                {'pregunta': 'La hominización se refiere: (UNSAAC 2015)',
                 'alternativas': ['A la sedentarización del hombre',
                                  'A la evolución de la especie humana',
                                  'Al surgimiento de las primeras '
                                  'manifestaciones agrícolas',
                                  'A la evolución de las especies animales y '
                                  'plantas',
                                  'Al desarrollo de la civilización humana'],
                 'correcta': 'B'},
                {'pregunta': 'El hombre del Paleolítico se caracterizó por: '
                             '(UNSAAC 2015)',
                 'alternativas': ['Su iniciación en la organización familiar',
                                  'Iniciar la sedentarización',
                                  'Rendir culto a sus muertos',
                                  'Su notable desarrollo en la pesca con '
                                  'arpón',
                                  'Desconocer la agricultura'],
                 'correcta': 'E'},
                {'pregunta': 'El periodo del Neolítico se caracterizó por: '
                             '(UNSAAC 2016)',
                 'alternativas': ['El desarrollo de la industria microlítica',
                                  'El desconocimiento de la agricultura, '
                                  'ganadería y cerámica',
                                  'La manifestación de arte rupestre en las '
                                  'cavernas',
                                  'Surgimiento de la familia, la propiedad '
                                  'privada, clases sociales y estado',
                                  'El nomadismo del hombre primitivo'],
                 'correcta': 'D'},
                {'pregunta': 'El proceso de Hominización fue explicado por '
                             'Charles Darwin en su libro: (UNSAAC 2016)',
                 'alternativas': ['Origen de la Civilización',
                                  'Evolución de las culturas',
                                  'Primeras poblaciones',
                                  'Transformaciones humanas',
                                  'Origen de las especies'],
                 'correcta': 'E'},
                {'pregunta': 'Un rasgo fundamental del proceso de '
                             'hominización fue: (UNSAAC 2018)',
                 'alternativas': ['El comienzo de la agrupación familiar del '
                                  'hombre',
                                  'El proceso de la civilización',
                                  'La vida sedentaria de los primates',
                                  'La bipedación y postura erguida del '
                                  'hombre primitivo',
                                  'El proceso de la migración peruana'],
                 'correcta': 'D'},
                {'pregunta': 'Después del periodo Mesolítico, surge el '
                             'Neolítico caracterizado por: (UNSAAC 2018)',
                 'alternativas': ['El desarrollo de la industria microlítica',
                                  'La construcción de viviendas llamadas '
                                  'Palafitos',
                                  'La pintura rupestre en las cavernas',
                                  'La caza y la recolección de frutos',
                                  'El descubrimiento del fuego'],
                 'correcta': 'E'},
                {'pregunta': 'El descubrimiento de la agricultura determinó '
                             'que el hombre primitivo pasara a ser: (UNSAAC '
                             '2018)',
                 'alternativas': ['Pescador',
                                  'Cavernario',
                                  'Troglodita',
                                  'Nómada',
                                  'Sedentario'],
                 'correcta': 'E'},
                {'pregunta': 'El científico más representativo que planteó '
                             'la Teoría Evolucionista del origen humano es: '
                             '(UNSAAC 2022)',
                 'alternativas': ['Charles Darwin',
                                  'Jacobo Boucher',
                                  'Cristóbal Keller',
                                  'Daniel Wilson',
                                  'Cristhian Thomsen'],
                 'correcta': 'A'},
                {'pregunta': 'Una característica principal del Periodo '
                             'Neolítico es: (UNSAAC 2023)',
                 'alternativas': ['El nomadismo del hombre',
                                  'El sedentarismo del hombre',
                                  'La culminación de las glaciaciones',
                                  'El descubrimiento del fuego',
                                  'La invención del arco y la flecha'],
                 'correcta': 'B'},
                {'pregunta': 'El hombre del periodo Neolítico fue: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Troglodita',
                                  'Recolector',
                                  'Nómada',
                                  'Pintor rupestre',
                                  'Agricultor'],
                 'correcta': 'E'},
                {'pregunta': 'El hombre primitivo logra la domesticación de '
                             'los animales e inventó la agricultura '
                             'incipiente en el periodo: (UNSAAC Ordinario)',
                 'alternativas': ['Mesolítico',
                                  'Neolítico',
                                  'Paleolítico',
                                  'La Tène',
                                  'Hallstatt'],
                 'correcta': 'B'},
                {'pregunta': 'El hombre del neolítico fue: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Ceramista',
                                  'Errante',
                                  'Troglodita',
                                  'Recolector',
                                  'Cazador'],
                 'correcta': 'A'},
                {'pregunta': 'La división de la prehistoria la propuso: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Charles Darwin',
                                  'Ferdinand Leakey',
                                  'Antoni Greman',
                                  'Christian Thomsen',
                                  'Donald Latrap'],
                 'correcta': 'D'},
                {'pregunta': 'Una característica propia del Neolítico '
                             'prehistórico es el: (UNSAAC Ordinario)',
                 'alternativas': ['Surgimiento del Lenguaje y el Tótem',
                                  'Descubrimiento del fuego, la flecha y el '
                                  'arco',
                                  'Desarrollo de la industria microlítica y '
                                  'la osteodontoquerática',
                                  'Desconocimiento de la agricultura y el '
                                  'pastoreo',
                                  'Surgimiento de la propiedad privada y de '
                                  'las clases sociales'],
                 'correcta': 'E'},
                {'pregunta': 'El alejamiento de las glaciaciones se dio en '
                             'el periodo geológico denominado: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Mesolítico',
                                  'Paleolítico',
                                  'Neolítico',
                                  'Calcolítico',
                                  'Pleistocénico'],
                 'correcta': 'A'},
                {'pregunta': 'En el proceso de hominización fue fundamental: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['La selección natural de las especies no '
                                  'humanas',
                                  'El desarrollo de la civilización humana',
                                  'La capacidad de fabricar objetos',
                                  'La práctica inicial del culto a los '
                                  'muertos',
                                  'El inicio de la organización familiar'],
                 'correcta': 'C'},
                {'pregunta': 'En el periodo cultural del Mesolítico, la '
                             'humanidad primitiva: (UNSAAC Ordinario)',
                 'alternativas': ['Descubrió simultáneamente la cerámica y '
                                  'la textilería',
                                  'Fue exclusivamente cazadora, pescadora y '
                                  'recolectora',
                                  'Inició la práctica del culto a sus '
                                  'muertos',
                                  'Conoció la propiedad privada y '
                                  'consiguientemente la diferenciación '
                                  'social',
                                  'Empezó a diferenciarse racialmente'],
                 'correcta': 'B'},
                {'pregunta': 'Lograda la revolución Neolítica, el hombre '
                             'paulatinamente cambió a otro proceso en el que '
                             'fabricaron sus herramientas y utensilios con '
                             'materiales más resistentes; a este cambio se '
                             'conoce como: (UNSAAC Ordinario)',
                 'alternativas': ['La edad de piedra',
                                  'Al periodo del Mesolítico',
                                  'Periodo del Neolítico',
                                  'Periodo del Paleolítico superior',
                                  'La edad de los metales'],
                 'correcta': 'E'},
                {'pregunta': 'El investigador que utilizó el término Pre '
                             'Historia fue: (UNSAAC Ordinario)',
                 'alternativas': ['Fernando Brundel',
                                  'Christian Thomsen',
                                  'Pablo Macera',
                                  'Charles Darwin',
                                  'Daniel Wilson'],
                 'correcta': 'E'},
                {'pregunta': 'El investigador que planteó el proceso de la '
                             'hominización, como proceso evolutivo, fue: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Fernand Braudel',
                                  'Charles Darwin',
                                  'Pablo Macera',
                                  'Daniel Wilson',
                                  'Christian Thomsen'],
                 'correcta': 'B'},
                {'pregunta': 'En qué periodo apareció la domesticación de '
                             'plantas y animales: (UNSAAC Ordinario)',
                 'alternativas': ['Mesolítico',
                                  'Paleolítico',
                                  'Neolítico',
                                  'Edad de los metales (Cobre)',
                                  'Edad de los metales (bronce)'],
                 'correcta': 'C'},
                {'pregunta': 'El científico que dividió la prehistoria '
                             'observando los materiales utilizados por el '
                             'hombre, fue: (UNSAAC Ordinario)',
                 'alternativas': ['Donald Johanson',
                                  'Jacobo Boucher de Perthes',
                                  'Christian Thomsen',
                                  'Daniel Wilson',
                                  'Charles Darwin'],
                 'correcta': 'C'},
                {'pregunta': 'La prehistoria se divide en: (I CEPRU 2010)',
                 'alternativas': ['Edad de los metales - edad media',
                                  'Edad antigua - edad media',
                                  'Edad de piedra - edad de los metales',
                                  'Edad de piedra - edad de cobre',
                                  'Edad de piedra - edad contemporánea'],
                 'correcta': 'C'},
                {'pregunta': 'La característica del hombre del paleolítico: '
                             '(I CEPRU 2010)',
                 'alternativas': ['Arquitecto',
                                  'Troglodita',
                                  'Sedentario',
                                  'Ceramista',
                                  'Tejedor'],
                 'correcta': 'B'},
                {'pregunta': 'En la edad de los metales el hombre descubre: '
                             '(I CEPRU 2011)',
                 'alternativas': ['Oro - Plata - Cobre',
                                  'Plata - Hierro - Mercurio',
                                  'Bronce - Plata - Oro',
                                  'Hierro - Plata - Mercurio',
                                  'Cobre - Bronce - Hierro'],
                 'correcta': 'E'},
                {'pregunta': 'En el periodo Paleolítico, el hombre se '
                             'caracterizó por ser: (I CEPRU 2011)',
                 'alternativas': ['Nómada',
                                  'Sedentario',
                                  'Agricultor',
                                  'Ceramista',
                                  'Textilero'],
                 'correcta': 'A'},
                {'pregunta': 'En el neolítico el hombre fue: (I CEPRU 2011)',
                 'alternativas': ['Pescador',
                                  'Cazador',
                                  'Nómada',
                                  'Sedentario',
                                  'Troglodita'],
                 'correcta': 'D'},
                {'pregunta': 'El desconocimiento de la producción agrícola, '
                             'es una de las características que corresponde '
                             'al periodo: (I CEPRU 2012)',
                 'alternativas': ['Mesolítico',
                                  'Paleolítico',
                                  'Neolítico',
                                  'Microlítico',
                                  'Edad de los metales'],
                 'correcta': 'B'},
                {'pregunta': 'Las estructuras funerarias de Dólmenes, '
                             'Menhires y Crómlech corresponden al periodo '
                             'de: (I CEPRU 2012)',
                 'alternativas': ['Paleolítico',
                                  'Mesolítico',
                                  'Neolítico',
                                  'Eneolítico',
                                  'Calcolítico'],
                 'correcta': 'C'},
                {'pregunta': 'La etapa que abarca desde la aparición del '
                             'hombre hasta la invención de la escritura se '
                             'denomina: (I CEPRU 2013)',
                 'alternativas': ['Protohistoria',
                                  'Poshistoria',
                                  'Historia',
                                  'Prehistoria',
                                  'Mesohistoria'],
                 'correcta': 'D'},
                {'pregunta': 'Se considera como el inicio de la cultura, a '
                             'la capacidad de fabricar objetos, siendo este '
                             'uno de los rasgos de la: (I CEPRU 2013)',
                 'alternativas': ['Aculturación',
                                  'Socialización',
                                  'Hominización',
                                  'Creación',
                                  'Adaptación'],
                 'correcta': 'C'},
                {'pregunta': 'La primera gran revolución agrícola, ganadera '
                             'e industrial, que experimentaron los grupos '
                             'humanos ocurrió en el periodo: (I CEPRU 2013)',
                 'alternativas': ['Tardío',
                                  'Temprano',
                                  'Mesolítico',
                                  'Neolítico',
                                  'Paleolítico'],
                 'correcta': 'D'},
                {'pregunta': 'El autor del Origen de las especies fue: (I '
                             'CEPRU 2014)',
                 'alternativas': ['Cristian Thomsen',
                                  'Jacobo Boucher',
                                  'Francis Champollion',
                                  'Charles Darwin',
                                  'Henry Raulinson'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'PROCESO DE HOMINIZACIÓN',
                      'items': ['Es el conjunto de modificaciones biológicas '
                                'y anatómicas, así como de logros '
                                'culturales, desarrollados durante millones '
                                'de años.',
                                '1° La bipedación y la postura erguida, que '
                                'liberó las extremidades superiores.',
                                '2° La capacidad de fabricar objetos, que '
                                'marcó el paso de los hominoides a los '
                                'homínidos y se considera el inicio de la '
                                'cultura.',
                                'La teoría evolucionista fue formulada por '
                                'Charles Darwin en su libro «El origen de '
                                'las especies por medio de la selección '
                                'natural».']},
                     {'titulo': 'LA PREHISTORIA: CONCEPTO',
                      'items': ['El concepto fue propuesto por Jacobo '
                                'Boucher de Perthes y utilizado por el '
                                'inglés Daniel Wilson en 1851.',
                                'Se refiere al periodo anterior a la '
                                'aparición de la escritura.',
                                'Christian Thomsen dividió esta etapa '
                                'observando los materiales con que el hombre '
                                'fabricaba sus herramientas.']},
                     {'titulo': 'PALEOLÍTICO (HASTA 10 000 A.C.)',
                      'items': ['Del griego palaios = antiguo y lithos = '
                                'piedra. Es el periodo de la piedra tallada '
                                'y de mayor duración.',
                                'Fueron nómadas, cavernícolas y errantes; '
                                'recolectores de piedras, preferentemente el '
                                'sílex.',
                                'Usaron la técnica osteodontoquerática, con '
                                'huesos de mandíbula de animales.',
                                'Se organizaron en hordas, clanes y gens; '
                                'practicaron el incesto y veneraron un '
                                'antepasado común llamado tótem.',
                                'Descubrieron el fuego y crearon el arte '
                                'rupestre: Altamira en España y Lascaux en '
                                'Francia.']},
                     {'titulo': 'MESOLÍTICO (10 000 – 7000 A.C.)',
                      'items': ['Periodo de transición del Pleistoceno al '
                                'Holoceno.',
                                'Se desarrolló la industria microlítica y la '
                                'pesca con arpón.',
                                'Se practicó la horticultura y se inició la '
                                'domesticación de animales.']},
                     {'titulo': 'NEOLÍTICO (7000 – 3000 A.C.)',
                      'items': ['Del griego neo = nuevo: periodo de la '
                                'piedra pulimentada.',
                                'Fueron sedentarios y practicaron la '
                                'agricultura y la ganadería: primera gran '
                                'revolución agrícola.',
                                'Iniciaron la alfarería y la textilería con '
                                'algodón, lana y lino.',
                                'Construyeron viviendas sobre pilotes '
                                'llamadas palafitos; la primera ciudad '
                                'prehistórica se halló en el lago Zúrich.',
                                'Desarrollaron arquitectura funeraria: '
                                'dólmenes, menhires y crómlech. Destaca '
                                'Stonehenge en Inglaterra.',
                                'Surgen la propiedad privada, las clases '
                                'sociales y el Estado.']},
                     {'titulo': 'LA EDAD DE LOS METALES',
                      'items': ['La Edad de los Metales se caracteriza por '
                                'el abandono gradual de instrumentos de '
                                'piedra, reemplazados por metales fundidos.',
                                'La Edad del Cobre o Calcolítico (5000-3000 '
                                'a.C.) es la transición entre la Edad de '
                                'Piedra y la Edad de los Metales.',
                                'El uso del cobre fundido se inició en '
                                'Çatalhöyük, actual Turquía, hacia el 5000 '
                                'a.C.',
                                'La Edad del Bronce (3000-1500 a.C.) comenzó '
                                'en Sumeria; el bronce es la aleación de '
                                'cobre y estaño.',
                                'El bronce se usó para fabricar armas como '
                                'espadas y escudos, y utensilios agrícolas '
                                'como hoces.',
                                'La Edad del Hierro (1500-18 a.C.) fue '
                                'iniciada por los hititas de Turquía.',
                                'El hierro tenía dos ventajas sobre el '
                                'bronce: mayor abundancia del mineral, y '
                                'mayor dureza de las armas.']}],
  'qr_reto': [{'pregunta': 'En la edad de los metales el hombre descubre:',
               'respuesta': 'Cobre - Bronce - Hierro'},
              {'pregunta': 'La división de la prehistoria la propuso:',
               'respuesta': 'Christian Thomsen'},
              {'pregunta': 'En el proceso de hominización fue fundamental:',
               'respuesta': 'La capacidad de fabricar objetos'}],
  'qr_dato': 'Se desarrolló la industria microlítica y la pesca con arpón.'},
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
                {'titulo': '3.1.2 MESOPOTAMIA: PROCESO HISTÓRICO',
                 'items': ['Los {sumerios} (3000 a.C.) crearon las primeras '
                           'Ciudades-Estado: Kish, Uruk, Ur y {Lagash}. '
                           'Inventaron la escritura cuneiforme y conocieron '
                           'la rueda.',
                           'Los acadios, dirigidos por {Sargón}, '
                           'conquistaron las ciudades sumerias y fijaron su '
                           'capital en {Akkad}.',
                           'En el Primer Imperio Babilónico, el rey '
                           '{Hammurabi} unificó las ciudades sumerias y '
                           'estableció su famoso código jurídico.',
                           'En el Imperio Asirio destacó {Asurbanipal}, '
                           'quien mandó construir la biblioteca de {Nínive}.',
                           'En el Segundo Imperio Babilónico, {Nabopolasar} '
                           'fue el artífice de la caída del imperio asirio.',
                           '{Nabucodonosor II} forjó la grandeza de '
                           'Babilonia, conquistó Jerusalén —el «{cautiverio '
                           'babilónico}» de los judíos— y mandó construir '
                           'los jardines {colgantes}.']},
                {'titulo': '3.1.3 MESOPOTAMIA: ORGANIZACIÓN POLÍTICA Y '
                           'SOCIAL',
                 'items': ['A diferencia de Egipto, Mesopotamia no tenía '
                           'fronteras {naturales}, lo que generó constantes '
                           'invasiones semitas, indoeuropeas y asiáticas.',
                           'Las primeras unidades políticas se organizaron '
                           'bajo el modelo de {Ciudad-Estado}, con gobiernos '
                           'autónomos, leyes y dioses propios.',
                           'En las ciudades-estado gobernaron inicialmente '
                           'los {reyes-sacerdotes}, elegidos por los '
                           'pobladores; con el tiempo el cargo se volvió '
                           '{hereditario}.']},
                {'titulo': '3.1.4 MESOPOTAMIA: EXPRESIONES CULTURALES',
                 'items': ['Arquitectura: destacó el {zigurat}. Fueron los '
                           'primeros en construir el arco, la bóveda y la '
                           '{cúpula}, desconocidos por los egipcios.',
                           'Escultura: los toros {alados} con cabeza humana '
                           'del palacio de Sargón II en Korsabad; la estatua '
                           'en mármol del príncipe {Gudea}.',
                           'También destaca la estatua del rey {Hammurabi}, '
                           'guerrero y conquistador, célebre por su código '
                           '{moral}.',
                           'Escritura: la {cuneiforme}, con signos en forma '
                           'de cuña. La roca de {Behistún} fue descifrada '
                           'por {Henry Rawlinson}.']},
                {'titulo': '3.2 EGIPTO — UBICACIÓN',
                 'items': ['Situado al {noreste} del continente africano, en '
                           'torno al río {Nilo}, llamado por Heródoto «don '
                           'del Nilo».',
                           'Limitaba al norte con el mar {Mediterráneo}, al '
                           'este con el istmo de {Suez}, al sur con Nubia y '
                           'al oeste con el desierto de {Libia}.']},
                {'titulo': '3.2.2 EGIPTO: LOS TRES IMPERIOS',
                 'items': ['El {Imperio Antiguo} (2600-2150 a.C.) consolidó '
                           'el poder del Estado en la figura del Faraón.',
                           'En la tercera dinastía destacó {Dyeser} (Zocer), '
                           'por el dominio del arte y la arquitectura '
                           'monumental en piedra.',
                           'De esta época datan las tres pirámides de '
                           '{Seneferu}, y la Gran Pirámide de Guiza, '
                           'atribuida a {Keops} por Heródoto, junto con las '
                           'de Kefrén y Micerino.',
                           'La capital del Imperio Antiguo se estableció en '
                           '{Menfis}.',
                           'El {Imperio Medio} (2150-1785 a.C.) reunificó '
                           'Egipto con capital en {Tebas}, y sufrió la '
                           'invasión de los {Hicsos}.',
                           'El {Imperio Nuevo} (1551-1080 a.C.) logró '
                           'expulsar a los Hicsos; destacaron los faraones '
                           '{Tutmosis III} y Ramsés II.',
                           'El faraón {Amenofis IV} intentó imponer el culto '
                           'monoteísta al dios {Atón}, el sol.']},
                {'titulo': '3.2.3 EGIPTO: ORGANIZACIÓN POLÍTICO-SOCIAL',
                 'items': ['Egipto fue una monarquía {teocrática}: el Faraón '
                           'era considerado de origen {divino}.',
                           'La administración del Estado la ejercían los '
                           '{escribas}.',
                           'Las clases sociales de Egipto eran: sacerdotes, '
                           'escribas, comerciantes, el pueblo y los '
                           '{esclavos}.']},
                {'titulo': '3.2.4 EGIPTO: ARQUITECTURA Y ESCULTURA',
                 'items': ['Las tumbas fueron de tres tipos: {pirámides} '
                           '(faraones), {mastabas} (nobles, pirámides '
                           'truncas) e {hipogeos} (pueblo, excavadas en '
                           'roca).',
                           'Los templos más representativos, en Tebas, son '
                           'los de {Karnak} y Luxor.',
                           'Los {capiteles} florales de las columnas '
                           'tuvieron motivos palmiformes, {lotiformes}, '
                           'papiriformes y atónicas (dios Atón).',
                           'Los {Colosos de Memnón} son estatuas gigantescas '
                           'de faraones sentados, en la entrada de templos.',
                           'La {Esfinge} de Gizeh representa el rostro del '
                           'faraón {Kefrén} con cuerpo de león.',
                           'El {Escriba Sentado} es una escultura de un '
                           'funcionario dedicado a anotar los ingresos del '
                           'reino desde la {IV} dinastía.',
                           'Otras esculturas representan a la reina '
                           '{Nefertiti} y al faraón {Amenofis}.']},
                {'titulo': '3.2.4.3 EGIPTO: LA ESCRITURA',
                 'items': ['La escritura {jeroglífica}, la más antigua, '
                           'formada por imágenes de objetos, se usaba en '
                           'tumbas y templos.',
                           'La piedra {Rosetta}, escrita en jeroglífico, fue '
                           'descifrada por el francés {Champollion} en 1822.',
                           'La escritura {hierática}, más sencilla, era '
                           'empleada por escribas y sacerdotes.',
                           'La escritura {demótica} era la escritura '
                           'popular, más simple, utilizada por el pueblo.']}],
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
                                  'Danubio y Rin',
                                  'Tigris y Éufrates',
                                  'Indo y Ganges',
                                  'Amarillo y Azul'],
                 'correcta': 'C'},
                {'pregunta': 'La capital del Imperio Asirio fue:',
                 'alternativas': ['Uruk',
                                  'Babilonia',
                                  'Ur',
                                  'Akkad',
                                  'Nínive'],
                 'correcta': 'E'},
                {'pregunta': 'Las primeras Ciudades-Estado de Mesopotamia '
                             'fueron creadas por los:',
                 'alternativas': ['Sumerios',
                                  'Persas',
                                  'Acadios',
                                  'Hititas',
                                  'Caldeos'],
                 'correcta': 'A'},
                {'pregunta': 'El rey acadio que conquistó las ciudades '
                             'sumerias fue:',
                 'alternativas': ['Nabopolasar',
                                  'Gudea',
                                  'Hammurabi',
                                  'Asurbanipal',
                                  'Sargón'],
                 'correcta': 'E'},
                {'pregunta': 'El primer código jurídico escrito de '
                             'Mesopotamia se atribuye a:',
                 'alternativas': ['Hammurabi',
                                  'Asurbanipal',
                                  'Nabucodonosor II',
                                  'Rawlinson',
                                  'Sargón'],
                 'correcta': 'A'},
                {'pregunta': 'La biblioteca de Nínive fue mandada construir '
                             'por:',
                 'alternativas': ['Asurbanipal',
                                  'Sargón II',
                                  'Hammurabi',
                                  'Nabucodonosor II',
                                  'Nabopolasar'],
                 'correcta': 'A'},
                {'pregunta': 'Los jardines colgantes de Babilonia se '
                             'atribuyen a:',
                 'alternativas': ['Hammurabi',
                                  'Gudea',
                                  'Sargón',
                                  'Nabucodonosor II',
                                  'Asurbanipal'],
                 'correcta': 'D'},
                {'pregunta': 'El «cautiverio babilónico» afectó al pueblo:',
                 'alternativas': ['Acadio',
                                  'Hitita',
                                  'Judío',
                                  'Asirio',
                                  'Persa'],
                 'correcta': 'C'},
                {'pregunta': 'El templo escalonado característico de '
                             'Mesopotamia se denomina:',
                 'alternativas': ['Ziggurat egipcio',
                                  'Partenón',
                                  'Zigurat',
                                  'Mastaba',
                                  'Pirámide'],
                 'correcta': 'C'},
                {'pregunta': 'Fueron los primeros en construir el arco, la '
                             'bóveda y la cúpula:',
                 'alternativas': ['Los griegos',
                                  'Los persas',
                                  'Los romanos',
                                  'Los egipcios',
                                  'Los mesopotámicos'],
                 'correcta': 'E'},
                {'pregunta': 'La escritura cuneiforme recibe ese nombre por:',
                 'alternativas': ['Su uso comercial',
                                  'Su soporte de papiro',
                                  'Su carácter jeroglífico',
                                  'Su origen sacerdotal',
                                  'Sus signos en forma de cuña'],
                 'correcta': 'E'},
                {'pregunta': 'La inscripción de la roca de Behistún fue '
                             'descifrada por:',
                 'alternativas': ['Heródoto',
                                  'Schliemann',
                                  'Boucher de Perthes',
                                  'Henry Rawlinson',
                                  'Champollion'],
                 'correcta': 'D'},
                {'pregunta': 'Los toros alados con cabeza humana se hallaron '
                             'en el palacio de:',
                 'alternativas': ['Ciro en Persépolis',
                                  'Hammurabi en Babilonia',
                                  'Sargón II en Korsabad',
                                  'Gudea en Lagash',
                                  'Asurbanipal en Nínive'],
                 'correcta': 'C'},
                {'pregunta': 'La Baja Mesopotamia fue la región donde se '
                             'desarrolló la civilización:',
                 'alternativas': ['Hitita',
                                  'Persa',
                                  'Elamita',
                                  'Asiria',
                                  'Caldea'],
                 'correcta': 'E'},
                {'pregunta': 'Actualmente el territorio de Mesopotamia '
                             'corresponde principalmente a:',
                 'alternativas': ['Irán',
                                  'Siria',
                                  'Turquía',
                                  'Irak',
                                  'Egipto'],
                 'correcta': 'D'},
                {'pregunta': 'Egipto se ubica en el continente:',
                 'alternativas': ['Oceánico',
                                  'Americano',
                                  'Asiático',
                                  'Europeo',
                                  'Africano'],
                 'correcta': 'E'},
                {'pregunta': 'El límite norte del antiguo Egipto era:',
                 'alternativas': ['El istmo de Suez',
                                  'Nubia',
                                  'El desierto de Libia',
                                  'El mar Mediterráneo',
                                  'El Mar Rojo'],
                 'correcta': 'D'},
                {'pregunta': 'El artífice de la caída del Imperio Asirio '
                             'fue:',
                 'alternativas': ['Nabopolasar',
                                  'Hammurabi',
                                  'Sargón',
                                  'Nabucodonosor II',
                                  'Ciro'],
                 'correcta': 'A'},
                {'pregunta': 'La estatua del príncipe Gudea se conserva '
                             'actualmente en:',
                 'alternativas': ['El Museo del Louvre',
                                  'El Museo Británico',
                                  'El Metropolitan',
                                  'El Museo de Berlín',
                                  'El Museo de El Cairo'],
                 'correcta': 'A'},
                {'pregunta': 'Un factor que explica las constantes '
                             'invasiones a Mesopotamia fue:',
                 'alternativas': ['Su clima glacial',
                                  'Su aislamiento total',
                                  'La ausencia de fronteras naturales',
                                  'La falta de ríos',
                                  'Su escasa población'],
                 'correcta': 'C'},
                {'pregunta': 'A diferencia de Egipto, Mesopotamia no tenía '
                             'fronteras naturales, lo que generó constantes:',
                 'alternativas': ['Sequías',
                                  'Invasiones',
                                  'Terremotos',
                                  'Hambrunas',
                                  'Migraciones internas'],
                 'correcta': 'B'},
                {'pregunta': 'Las primeras unidades políticas de Mesopotamia '
                             'se organizaron bajo el modelo de:',
                 'alternativas': ['Imperio centralizado',
                                  'Ciudad-Estado',
                                  'Monarquía absoluta única',
                                  'República federal',
                                  'Confederación tribal'],
                 'correcta': 'B'},
                {'pregunta': 'En las ciudades-estado mesopotámicas '
                             'gobernaron inicialmente los:',
                 'alternativas': ['Faraones',
                                  'Reyes-sacerdotes',
                                  'Cónsules',
                                  'Senadores',
                                  'Emperadores'],
                 'correcta': 'B'},
                {'pregunta': 'En arquitectura, los mesopotámicos fueron '
                             'pioneros en construir el arco, la bóveda y:',
                 'alternativas': ['La columna dórica',
                                  'La cúpula',
                                  'El obelisco',
                                  'La pirámide escalonada',
                                  'El zigurat exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'Las estatuas de toros alados con cabeza humana '
                             'se hallaron en el palacio de:',
                 'alternativas': ['Hammurabi',
                                  'Sargón II',
                                  'Nabucodonosor',
                                  'Gudea',
                                  'Assurbanipal'],
                 'correcta': 'B'},
                {'pregunta': 'La escritura mesopotámica, con signos en forma '
                             'de cuñas, se llama escritura:',
                 'alternativas': ['Jeroglífica',
                                  'Cuneiforme',
                                  'Demótica',
                                  'Lineal B',
                                  'Rúnica'],
                 'correcta': 'B'},
                {'pregunta': 'La escritura de la roca de Behistún fue '
                             'descifrada por:',
                 'alternativas': ['Champollion',
                                  'Henry Rawlinson',
                                  'Heinrich Schliemann',
                                  'Howard Carter',
                                  'Flinders Petrie'],
                 'correcta': 'B'},
                {'pregunta': 'El Imperio Antiguo de Egipto (2600-2150 a.C.) '
                             'consolidó el poder del Estado en la figura de:',
                 'alternativas': ['El sumo sacerdote',
                                  'El Faraón',
                                  'El senado',
                                  'El escriba mayor',
                                  'El visir exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'La Gran Pirámide de Guiza es atribuida por '
                             'Heródoto a:',
                 'alternativas': ['Kefrén',
                                  'Keops',
                                  'Micerino',
                                  'Dyeser',
                                  'Tutmosis III'],
                 'correcta': 'B'},
                {'pregunta': 'La capital del Imperio Antiguo de Egipto se '
                             'estableció en:',
                 'alternativas': ['Tebas',
                                  'Menfis',
                                  'Alejandría',
                                  'Luxor',
                                  'Karnak'],
                 'correcta': 'B'},
                {'pregunta': 'El Imperio Medio de Egipto (2150-1785 a.C.) '
                             'tuvo como capital a:',
                 'alternativas': ['Menfis',
                                  'Tebas',
                                  'Alejandría',
                                  'Guiza',
                                  'Karnak'],
                 'correcta': 'B'},
                {'pregunta': 'Durante el Imperio Medio, Egipto sufrió la '
                             'invasión de un pueblo nómada de Asia llamado:',
                 'alternativas': ['Los persas',
                                  'Los Hicsos',
                                  'Los asirios',
                                  'Los babilonios',
                                  'Los fenicios'],
                 'correcta': 'B'},
                {'pregunta': 'El Imperio Nuevo de Egipto logró expulsar a '
                             'los Hicsos, destacando los faraones Ramsés II '
                             'y:',
                 'alternativas': ['Amenofis IV',
                                  'Tutmosis III',
                                  'Keops',
                                  'Kefrén',
                                  'Micerino'],
                 'correcta': 'B'},
                {'pregunta': 'El faraón que intentó imponer el culto '
                             'monoteísta al dios Atón fue:',
                 'alternativas': ['Ramsés II',
                                  'Amenofis IV',
                                  'Tutmosis III',
                                  'Keops',
                                  'Kefrén'],
                 'correcta': 'B'},
                {'pregunta': 'Egipto fue una monarquía de tipo:',
                 'alternativas': ['Parlamentaria',
                                  'Teocrática',
                                  'Constitucional',
                                  'Federal',
                                  'Oligárquica'],
                 'correcta': 'B'},
                {'pregunta': 'La administración del Estado egipcio la '
                             'ejercían los:',
                 'alternativas': ['Sacerdotes exclusivamente',
                                  'Escribas',
                                  'Esclavos',
                                  'Comerciantes exclusivamente',
                                  'Faraones directamente sin ayuda'],
                 'correcta': 'B'},
                {'pregunta': 'Las clases sociales de Egipto incluían '
                             'sacerdotes, escribas, comerciantes, el pueblo '
                             'y:',
                 'alternativas': ['Los extranjeros',
                                  'Los esclavos',
                                  'Los militares exclusivamente',
                                  'Los artesanos exclusivamente',
                                  'Los nómadas'],
                 'correcta': 'B'},
                {'pregunta': 'Los sepulcros para nobles, con forma de '
                             'pequeñas pirámides truncas, se llaman:',
                 'alternativas': ['Hipogeos',
                                  'Mastabas',
                                  'Zigurats',
                                  'Obeliscos',
                                  'Cenotafios'],
                 'correcta': 'B'},
                {'pregunta': 'Las tumbas subterráneas excavadas en roca '
                             'donde se enterraba al pueblo egipcio se '
                             'llaman:',
                 'alternativas': ['Mastabas',
                                  'Hipogeos',
                                  'Pirámides',
                                  'Zigurats',
                                  'Sarcófagos'],
                 'correcta': 'B'},
                {'pregunta': 'Los templos más representativos de Egipto, '
                             'ubicados en Tebas, son los de Karnak y:',
                 'alternativas': ['Menfis',
                                  'Luxor',
                                  'Guiza',
                                  'Alejandría',
                                  'Abu Simbel exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'La Esfinge de Gizeh representa el rostro del '
                             'faraón:',
                 'alternativas': ['Keops',
                                  'Kefrén',
                                  'Micerino',
                                  'Tutmosis III',
                                  'Ramsés II'],
                 'correcta': 'B'},
                {'pregunta': 'La escultura del «Escriba Sentado» representa '
                             'a un funcionario dedicado a:',
                 'alternativas': ['Cobrar impuestos exclusivamente',
                                  'Anotar los ingresos del reino',
                                  'Custodiar tumbas',
                                  'Dirigir el ejército',
                                  'Presidir ceremonias religiosas'],
                 'correcta': 'B'},
                {'pregunta': 'El artífice de la caída del Imperio Asirio, '
                             'gobernante del Segundo Imperio Babilónico, '
                             'fue:',
                 'alternativas': ['Nabucodonosor II',
                                  'Nabopolasar',
                                  'Sargón',
                                  'Hammurabi',
                                  'Asurbanipal'],
                 'correcta': 'B'},
                {'pregunta': 'Además de los toros alados y el príncipe '
                             'Gudea, la escultura mesopotámica destacó con '
                             'la estatua de:',
                 'alternativas': ['Sargón II',
                                  'El rey Hammurabi',
                                  'Nabucodonosor',
                                  'Asurbanipal',
                                  'Nabopolasar'],
                 'correcta': 'B'},
                {'pregunta': 'El faraón de la tercera dinastía, destacado '
                             'por el dominio del arte y la arquitectura '
                             'monumental en piedra, fue:',
                 'alternativas': ['Keops',
                                  'Dyeser (Zocer)',
                                  'Kefrén',
                                  'Micerino',
                                  'Amenofis IV'],
                 'correcta': 'B'},
                {'pregunta': 'Las tres pirámides colosales que datan del '
                             'Imperio Antiguo, previas a las de Guiza, '
                             'fueron construidas por:',
                 'alternativas': ['Keops',
                                  'Seneferu',
                                  'Kefrén',
                                  'Micerino',
                                  'Tutmosis III'],
                 'correcta': 'B'},
                {'pregunta': 'Los motivos florales esculpidos en los '
                             'capiteles egipcios incluían palmiformes, '
                             'papiriformes, atónicas y:',
                 'alternativas': ['Rosáceos',
                                  'Lotiformes (hoja de loto)',
                                  'Espinosos',
                                  'Cactiformes',
                                  'Ramiformes'],
                 'correcta': 'B'},
                {'pregunta': 'El motivo de capitel llamado «atónicas» hace '
                             'referencia al dios:',
                 'alternativas': ['Osiris', 'Atón', 'Ra', 'Anubis', 'Horus'],
                 'correcta': 'B'},
                {'pregunta': 'Además del Escriba Sentado, otras esculturas '
                             'egipcias representan a la reina Nefertiti y al '
                             'faraón:',
                 'alternativas': ['Keops',
                                  'Amenofis',
                                  'Kefrén',
                                  'Micerino',
                                  'Tutmosis III'],
                 'correcta': 'B'},
                {'pregunta': 'La escritura egipcia más antigua, usada en '
                             'tumbas y templos con imágenes de objetos, es '
                             'la escritura:',
                 'alternativas': ['Hierática',
                                  'Jeroglífica',
                                  'Demótica',
                                  'Cuneiforme',
                                  'Rúnica'],
                 'correcta': 'B'},
                {'pregunta': 'La piedra Rosetta, escrita en jeroglífico '
                             'egipcio, fue descifrada por el francés '
                             'Champollion en el año:',
                 'alternativas': ['1799', '1822', '1453', '1900', '1750'],
                 'correcta': 'B'},
                {'pregunta': 'La escritura egipcia empleada por escribas y '
                             'sacerdotes, más sencilla que la jeroglífica, '
                             'se llama escritura:',
                 'alternativas': ['Demótica',
                                  'Hierática',
                                  'Cuneiforme',
                                  'Rúnica',
                                  'Jeroglífica'],
                 'correcta': 'B'},
                {'pregunta': 'La escritura egipcia popular, la más simple, '
                             'utilizada por el pueblo, se llama escritura:',
                 'alternativas': ['Hierática',
                                  'Demótica',
                                  'Jeroglífica',
                                  'Cuneiforme',
                                  'Ideográfica'],
                 'correcta': 'B'},
                {'pregunta': 'En arquitectura, la cultura Mesopotámica '
                             'aportó: (UNSAAC 2010)',
                 'alternativas': ['La edificación de templos y tumbas',
                                  'La bóveda, la columna y cúpula',
                                  'La cúpula, el capitel y el arco',
                                  'La pirámide y las moradas de dioses',
                                  'El arco, la bóveda y la cúpula'],
                 'correcta': 'E'},
                {'pregunta': 'El teatro de planta circular y gradería '
                             'semicircular corresponde a la cultura: (UNSAAC '
                             '2010)',
                 'alternativas': ['Caldeo Asiria',
                                  'Romana',
                                  'Griega',
                                  'Mesopotámica',
                                  'Persa'],
                 'correcta': 'B'},
                {'pregunta': 'El Toro Alado con cabeza humana es una '
                             'expresión artística de la cultura: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Egipcia',
                                  'Mesopotámica',
                                  'Griega',
                                  'Romana',
                                  'China'],
                 'correcta': 'B'},
                {'pregunta': 'El arco, la bóveda y la cúpula son los aportes '
                             'arquitectónicos más importantes de la cultura: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Hindú',
                                  'Griega',
                                  'Egipcia',
                                  'Mesopotámica',
                                  'Hebrea'],
                 'correcta': 'D'},
                {'pregunta': 'El desciframiento de la escritura cuneiforme '
                             'mesopotámica de la Roca de Behistum '
                             'corresponde a: (UNSAAC Ordinario)',
                 'alternativas': ['Boucher de Perthes',
                                  'Henry Rawlinson',
                                  'Christian Thomsen',
                                  'Francois Champollion',
                                  'Jean Poirier'],
                 'correcta': 'B'},
                {'pregunta': 'Una de las características de la arquitectura '
                             'egipcia es que: (UNSAAC Ordinario)',
                 'alternativas': ['Representan solidez y rigidez',
                                  'Expresan tristeza',
                                  'Exteriorizan afectos',
                                  'Expresan fielmente los sentimientos',
                                  'Poseen demasiado decorado'],
                 'correcta': 'A'},
                {'pregunta': 'El testimonio arquitectónico que identifica a '
                             'la Cultura Egipcia, se evidencia por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['La escultura de los reyes Sargón y '
                                  'Hammurabi',
                                  'Los Monumentos arquitectónicos como el '
                                  'Zigurat',
                                  'La construcción de Hemiciclos, teatros e '
                                  'hipódromos',
                                  'Las estatuas, el discóbolo, Atenea y '
                                  'Marxias',
                                  'Las edificaciones de monumentos '
                                  'funerarios como hipogeos y mastabas'],
                 'correcta': 'E'},
                {'pregunta': 'En la cultura egipcia, el culto al Dios Atón '
                             'se implantó en el periodo: (UNSAAC Ordinario)',
                 'alternativas': ['Imperio Antiguo',
                                  'Imperio Nuevo',
                                  'Imperio Medio',
                                  'Bajo Imperio',
                                  'Predinástico'],
                 'correcta': 'B'},
                {'pregunta': 'La arquitectura funeraria egipcia que sirvió '
                             'para el entierro de nobles y sacerdotes se '
                             'denomina: (UNSAAC Ordinario)',
                 'alternativas': ['Hipogeo',
                                  'Mastaba',
                                  'Pirámide',
                                  'Zigurat',
                                  'Templo'],
                 'correcta': 'B'},
                {'pregunta': 'Las ciudades de Kish, Ur y Uruk pertenecen a: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Acadio - Nínive',
                                  'Sumeria',
                                  'Nínive - Babilonio',
                                  'Babilonio - Caldeo',
                                  'Sumerio - Babilonio'],
                 'correcta': 'B'},
                {'pregunta': 'El Código de Hammurabi se desarrolló en el '
                             'proceso histórico de la Civilización '
                             'Mesopotámica, denominado: (UNSAAC Ordinario)',
                 'alternativas': ['Imperio Caldeo - Asirio',
                                  'Primer Imperio Babilónico',
                                  'Imperio Antiguo',
                                  'Imperio Medo - Persa',
                                  'Segundo Imperio Babilónico'],
                 'correcta': 'B'},
                {'pregunta': 'En la cultura mesopotámica, durante el Primer '
                             'Imperio Babilónico, el rey que unificó las '
                             'ciudades sumerias fue: (UNSAAC Ordinario)',
                 'alternativas': ['Amenofis IV',
                                  'Asurbanipal',
                                  'Nabucodonosor II',
                                  'Nabopolasar',
                                  'Hammurabi'],
                 'correcta': 'E'},
                {'pregunta': 'Mesopotamia significa región entre ríos según '
                             'los: (I CEPRU 2010)',
                 'alternativas': ['Griegos',
                                  'Mesopotámicos',
                                  'Hebreos',
                                  'Romanos',
                                  'Egipcios'],
                 'correcta': 'A'},
                {'pregunta': 'La escritura de Mesopotamia es: (I CEPRU 2010)',
                 'alternativas': ['Cuneiforme',
                                  'Jeroglífica',
                                  'Demótica',
                                  'Hierática',
                                  'Pallariforme'],
                 'correcta': 'A'},
                {'pregunta': 'En arquitectura la cultura mesopotámica aportó '
                             'al mundo: (I CEPRU 2011)',
                 'alternativas': ['Figuras humanas - la rueda - hojas de '
                                  'papiro',
                                  'Arco - bóveda - cúpula',
                                  'Dórico - jónico - corintio',
                                  'Capiteles - palmiformes - lotiformes',
                                  'Mastabas - Hipogeos - Pirámides'],
                 'correcta': 'B'},
                {'pregunta': 'La escritura caldeo-asiria fue: (I CEPRU 2011)',
                 'alternativas': ['Jeroglífica',
                                  'Hierática',
                                  'Demótica',
                                  'Cursiva',
                                  'Cuneiforme'],
                 'correcta': 'E'},
                {'pregunta': 'La edificación arquitectónica del Zigurat '
                             'corresponde a la cultura: (I CEPRU 2012)',
                 'alternativas': ['Romana',
                                  'Griega',
                                  'Egipcia',
                                  'Mesopotámica',
                                  'China'],
                 'correcta': 'D'},
                {'pregunta': 'En el periodo histórico del Imperio Medio de '
                             'Egipto los territorios conquistados fueron: (I '
                             'CEPRU 2012)',
                 'alternativas': ['Creta, Delos y Samos',
                                  'Mileto y Éfeso',
                                  'Irak e Irán',
                                  'Nubia, Libia y Siria',
                                  'Etolia y Tesalia'],
                 'correcta': 'D'},
                {'pregunta': 'La alta Mesopotamia se utilizó para fines '
                             'ganaderos y fue ocupada por la civilización: '
                             '(I CEPRU 2013)',
                 'alternativas': ['Asiria',
                                  'Babilonia',
                                  'Sumeria',
                                  'Acadia',
                                  'Caldea'],
                 'correcta': 'A'},
                {'pregunta': 'Las primeras unidades políticas de Mesopotamia '
                             'con gobierno autónomo se llamaban: (I CEPRU '
                             '2013)',
                 'alternativas': ['Estados consulados',
                                  'Ciudades estado',
                                  'Monarquías imperiales',
                                  'Aldeas tribales',
                                  'Burgos citadinos'],
                 'correcta': 'B'},
                {'pregunta': 'La escultura desarrollada por los '
                             'Mesopotámicos fue: (I CEPRU 2013)',
                 'alternativas': ['Religiosa',
                                  'Naturalista',
                                  'Colosal',
                                  'Realista',
                                  'Monumental'],
                 'correcta': 'C'},
                {'pregunta': 'Los egipcios realizaron grandes incursiones '
                             'militares conquistando Nubia, Libia y Siria '
                             'durante el imperio: (I CEPRU 2013)',
                 'alternativas': ['Nuevo',
                                  'Semita',
                                  'Babilónico',
                                  'Medio',
                                  'Antiguo'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'MESOPOTAMIA — UBICACIÓN / MESOPOTAMIA: '
                                'PROCESO HISTÓRICO',
                      'items': ['Se desarrolló entre los ríos Tigris y '
                                'Éufrates, al suroeste de Asia. Hoy '
                                'corresponde principalmente a Irak.',
                                'La Alta Mesopotamia, al norte, fue sede de '
                                'la civilización Asiria, con capital en '
                                'Nínive, a orillas del Tigris.',
                                'La Baja Mesopotamia, al sur, fue sede de la '
                                'civilización Caldea, con capital en '
                                'Babilonia, junto al Éufrates.',
                                'Pueblos que la habitaron: sumerios, '
                                'acadios, babilonios, hititas, caldeos, '
                                'medos y persas.',
                                'Los sumerios (3000 a.C.) crearon las '
                                'primeras Ciudades-Estado: Kish, Uruk, Ur y '
                                'Lagash. Inventaron la escritura cuneiforme '
                                'y conocieron la rueda.',
                                'Los acadios, dirigidos por Sargón, '
                                'conquistaron las ciudades sumerias y '
                                'fijaron su capital en Akkad.',
                                'En el Primer Imperio Babilónico, el rey '
                                'Hammurabi unificó las ciudades sumerias y '
                                'estableció su famoso código jurídico.',
                                'En el Imperio Asirio destacó Asurbanipal, '
                                'quien mandó construir la biblioteca de '
                                'Nínive.',
                                'En el Segundo Imperio Babilónico, '
                                'Nabopolasar fue el artífice de la caída del '
                                'imperio asirio.',
                                'Nabucodonosor II forjó la grandeza de '
                                'Babilonia, conquistó Jerusalén —el '
                                '«cautiverio babilónico» de los judíos— y '
                                'mandó construir los jardines colgantes.']},
                     {'titulo': 'MESOPOTAMIA: ORGANIZACIÓN POLÍTICA Y SOCIAL '
                                '/ MESOPOTAMIA: EXPRESIONES CULT',
                      'items': ['A diferencia de Egipto, Mesopotamia no '
                                'tenía fronteras naturales, lo que generó '
                                'constantes invasiones semitas, indoeuropeas '
                                'y asiáticas.',
                                'Las primeras unidades políticas se '
                                'organizaron bajo el modelo de '
                                'Ciudad-Estado, con gobiernos autónomos, '
                                'leyes y dioses propios.',
                                'En las ciudades-estado gobernaron '
                                'inicialmente los reyes-sacerdotes, elegidos '
                                'por los pobladores; con el tiempo el cargo '
                                'se volvió hereditario.',
                                'Arquitectura: destacó el zigurat. Fueron '
                                'los primeros en construir el arco, la '
                                'bóveda y la cúpula, desconocidos por los '
                                'egipcios.',
                                'Escultura: los toros alados con cabeza '
                                'humana del palacio de Sargón II en '
                                'Korsabad; la estatua en mármol del príncipe '
                                'Gudea.',
                                'También destaca la estatua del rey '
                                'Hammurabi, guerrero y conquistador, célebre '
                                'por su código moral.',
                                'Escritura: la cuneiforme, con signos en '
                                'forma de cuña. La roca de Behistún fue '
                                'descifrada por Henry Rawlinson.']},
                     {'titulo': 'EGIPTO — UBICACIÓN / EGIPTO: LOS TRES '
                                'IMPERIOS',
                      'items': ['Situado al noreste del continente africano, '
                                'en torno al río Nilo, llamado por Heródoto '
                                '«don del Nilo».',
                                'Limitaba al norte con el mar Mediterráneo, '
                                'al este con el istmo de Suez, al sur con '
                                'Nubia y al oeste con el desierto de Libia.',
                                'El Imperio Antiguo (2600-2150 a.C.) '
                                'consolidó el poder del Estado en la figura '
                                'del Faraón.',
                                'En la tercera dinastía destacó Dyeser '
                                '(Zocer), por el dominio del arte y la '
                                'arquitectura monumental en piedra.',
                                'De esta época datan las tres pirámides de '
                                'Seneferu, y la Gran Pirámide de Guiza, '
                                'atribuida a Keops por Heródoto, junto con '
                                'las de Kefrén y Micerino.',
                                'La capital del Imperio Antiguo se '
                                'estableció en Menfis.',
                                'El Imperio Medio (2150-1785 a.C.) reunificó '
                                'Egipto con capital en Tebas, y sufrió la '
                                'invasión de los Hicsos.',
                                'El Imperio Nuevo (1551-1080 a.C.) logró '
                                'expulsar a los Hicsos; destacaron los '
                                'faraones Tutmosis III y Ramsés II.']},
                     {'titulo': 'EGIPTO: ORGANIZACIÓN POLÍTICO-SOCIAL / '
                                'EGIPTO: ARQUITECTURA Y ESCULTURA',
                      'items': ['Egipto fue una monarquía teocrática: el '
                                'Faraón era considerado de origen divino.',
                                'La administración del Estado la ejercían '
                                'los escribas.',
                                'Las clases sociales de Egipto eran: '
                                'sacerdotes, escribas, comerciantes, el '
                                'pueblo y los esclavos.',
                                'Las tumbas fueron de tres tipos: pirámides '
                                '(faraones), mastabas (nobles, pirámides '
                                'truncas) e hipogeos (pueblo, excavadas en '
                                'roca).',
                                'Los templos más representativos, en Tebas, '
                                'son los de Karnak y Luxor.',
                                'Los capiteles florales de las columnas '
                                'tuvieron motivos palmiformes, lotiformes, '
                                'papiriformes y atónicas (dios Atón).',
                                'Los Colosos de Memnón son estatuas '
                                'gigantescas de faraones sentados, en la '
                                'entrada de templos.',
                                'La Esfinge de Gizeh representa el rostro '
                                'del faraón Kefrén con cuerpo de león.',
                                'El Escriba Sentado es una escultura de un '
                                'funcionario dedicado a anotar los ingresos '
                                'del reino desde la IV dinastía.']},
                     {'titulo': 'EGIPTO: LA ESCRITURA',
                      'items': ['La escritura jeroglífica, la más antigua, '
                                'formada por imágenes de objetos, se usaba '
                                'en tumbas y templos.',
                                'La piedra Rosetta, escrita en jeroglífico, '
                                'fue descifrada por el francés Champollion '
                                'en 1822.',
                                'La escritura hierática, más sencilla, era '
                                'empleada por escribas y sacerdotes.',
                                'La escritura demótica era la escritura '
                                'popular, más simple, utilizada por el '
                                'pueblo.']}],
  'qr_reto': [{'pregunta': 'Además de los toros alados y el príncipe Gudea, '
                           'la escultura mesopotámica destacó con la estatua '
                           'de:',
               'respuesta': 'El rey Hammurabi'},
              {'pregunta': 'En el periodo histórico del Imperio Medio de '
                           'Egipto los territorios conquistados fueron:',
               'respuesta': 'Nubia, Libia y Siria'},
              {'pregunta': 'Las tres pirámides colosales que datan del '
                           'Imperio Antiguo, previas a las de Guiza, fueron '
                           'construidas por:',
               'respuesta': 'Seneferu'}],
  'qr_dato': 'La escritura jeroglífica, la más antigua, formada por imágenes '
             'de objetos, se usaba en tumbas y templos.'},
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
                {'titulo': '4.2.3 ROMA: EXPRESIONES CULTURALES',
                 'items': ['El {derecho romano} es la compilación de leyes, '
                           'tratados y normativas establecidas en distintas '
                           'épocas de Roma.',
                           'La Ley de las {12 Tablas} fue, según Tito Livio, '
                           'la fuente de todo el derecho romano, público y '
                           'privado.',
                           'El derecho romano es considerado el aporte más '
                           'grande de Roma a la {humanidad}, inspirando las '
                           'legislaciones de casi todos los países.',
                           'El emperador {Justiniano} es considerado el '
                           'padre del derecho romano por su gran labor '
                           'legislativa.',
                           'En arquitectura, los romanos introdujeron de '
                           'mesopotámicos y etruscos el {arco}, la bóveda y '
                           'la cúpula.',
                           'Los romanos utilizaron materiales como piedra, '
                           'ladrillo y {hormigón} con cal como argamasa.',
                           'Entre las construcciones romanas más '
                           'representativas están el {Coliseo} (Anfiteatro '
                           'de Flavio), el Arco de Tito y el Arco de '
                           '{Trajano}.']}],
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
                 'alternativas': ['Clístenes',
                                  'Dracón',
                                  'Solón',
                                  'Licurgo',
                                  'Pericles'],
                 'correcta': 'C'},
                {'pregunta': 'El «Siglo de Oro» de Atenas corresponde al '
                             'gobierno de:',
                 'alternativas': ['Alejandro Magno',
                                  'Pericles',
                                  'Licurgo',
                                  'Solón',
                                  'Fidias'],
                 'correcta': 'B'},
                {'pregunta': 'Quien sistematizó la organización política de '
                             'Esparta fue:',
                 'alternativas': ['Dracón',
                                  'Pericles',
                                  'Licurgo',
                                  'Solón',
                                  'Rómulo'],
                 'correcta': 'C'},
                {'pregunta': 'Alejandro Magno extendió la cultura griega '
                             'hasta:',
                 'alternativas': ['Hispania',
                                  'La India',
                                  'Egipto',
                                  'China',
                                  'Britania'],
                 'correcta': 'B'},
                {'pregunta': 'Las ciudades-Estado griegas recibían el nombre '
                             'de:',
                 'alternativas': ['Civitas',
                                  'Nomos',
                                  'Ayllus',
                                  'Polis',
                                  'Demos'],
                 'correcta': 'D'},
                {'pregunta': 'El Partenón fue erigido en:',
                 'alternativas': ['La Acrópolis de Atenas',
                                  'Delfos',
                                  'Corinto',
                                  'Esparta',
                                  'Olimpia'],
                 'correcta': 'A'},
                {'pregunta': 'El autor de los relieves y metopas del '
                             'Partenón fue:',
                 'alternativas': ['Mirón',
                                  'Policleto',
                                  'Fidias',
                                  'Escopas',
                                  'Praxíteles'],
                 'correcta': 'C'},
                {'pregunta': 'A la muerte de Alejandro Magno, su imperio fue '
                             'repartido entre:',
                 'alternativas': ['Los persas',
                                  'El Senado',
                                  'Sus generales',
                                  'Sus hijos',
                                  'Los romanos'],
                 'correcta': 'C'},
                {'pregunta': 'Roma fue fundada, según la tradición, el año:',
                 'alternativas': ['27 a.C.',
                                  '146 a.C.',
                                  '753 a.C.',
                                  '509 a.C.',
                                  '476 d.C.'],
                 'correcta': 'C'},
                {'pregunta': 'El fundador legendario de Roma fue:',
                 'alternativas': ['Julio César',
                                  'Numa Pompilio',
                                  'Octavio Augusto',
                                  'Tarquino el Soberbio',
                                  'Rómulo'],
                 'correcta': 'E'},
                {'pregunta': 'Durante la monarquía romana, el cargo del rey '
                             'era:',
                 'alternativas': ['Electivo anual',
                                  'Temporal por cinco años',
                                  'Hereditario por línea femenina',
                                  'Vitalicio',
                                  'Rotativo'],
                 'correcta': 'D'},
                {'pregunta': 'Los últimos reyes de Roma fueron de origen:',
                 'alternativas': ['Galo',
                                  'Griego',
                                  'Cartaginés',
                                  'Sabino',
                                  'Etrusco'],
                 'correcta': 'E'},
                {'pregunta': 'El primer emperador romano fue:',
                 'alternativas': ['Constantino',
                                  'Nerón',
                                  'Julio César',
                                  'Trajano',
                                  'Octavio Augusto'],
                 'correcta': 'E'},
                {'pregunta': 'El periodo de estabilidad del Imperio Romano '
                             'se conoce como:',
                 'alternativas': ['Pax romana',
                                  'Imperium',
                                  'Pax deorum',
                                  'Res publica',
                                  'Pax augusta'],
                 'correcta': 'A'},
                {'pregunta': 'La República romana comprende el periodo:',
                 'alternativas': ['509–27 a.C.',
                                  '359–146 a.C.',
                                  '800–494 a.C.',
                                  '27 a.C.–476 d.C.',
                                  '753–509 a.C.'],
                 'correcta': 'A'},
                {'pregunta': 'Con Rómulo se iniciaron en Roma dos '
                             'instituciones:',
                 'alternativas': ['La pretura y la edilidad',
                                  'El imperio y la provincia',
                                  'El consulado y la dictadura',
                                  'El tribunado y la censura',
                                  'La asamblea y el Senado'],
                 'correcta': 'E'},
                {'pregunta': 'La crisis del Imperio Romano, desde el siglo '
                             'III d.C., incluyó un proceso de:',
                 'alternativas': ['Urbanización acelerada',
                                  'Ruralización',
                                  'Helenización',
                                  'Democratización',
                                  'Expansión territorial'],
                 'correcta': 'B'},
                {'pregunta': 'Grecia se desarrolló en el sur de la '
                             'península:',
                 'alternativas': ['Ibérica',
                                  'De Anatolia',
                                  'De los Balcanes',
                                  'Itálica',
                                  'Escandinava'],
                 'correcta': 'C'},
                {'pregunta': 'La caída del Imperio Romano de Occidente se '
                             'fija en el año:',
                 'alternativas': ['146 a.C.',
                                  '509 a.C.',
                                  '476 d.C.',
                                  '27 a.C.',
                                  '1453 d.C.'],
                 'correcta': 'C'},
                {'pregunta': 'El periodo helenístico de Grecia abarca los '
                             'años:',
                 'alternativas': ['753–509 a.C.',
                                  '494–359 a.C.',
                                  '800–494 a.C.',
                                  '359–146 a.C.',
                                  '146 a.C.–27 a.C.'],
                 'correcta': 'D'},
                {'pregunta': 'El derecho romano se define como una '
                             'compilación de leyes, tratados y:',
                 'alternativas': ['Religiones',
                                  'Normativas',
                                  'Idiomas',
                                  'Monedas',
                                  'Territorios'],
                 'correcta': 'B'},
                {'pregunta': 'Según Tito Livio, la fuente de todo el derecho '
                             'romano fue:',
                 'alternativas': ['El Código de Justiniano',
                                  'La Ley de las 12 Tablas',
                                  'El Edicto de Milán',
                                  'La Lex Canuleia',
                                  'El Derecho Pretorio'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho romano es considerado el aporte más '
                             'grande de Roma a:',
                 'alternativas': ['Solo Europa',
                                  'La humanidad',
                                  'Solo Italia',
                                  'Solo el Imperio',
                                  'Solo la Iglesia'],
                 'correcta': 'B'},
                {'pregunta': 'El emperador considerado el padre del derecho '
                             'romano por su labor legislativa fue:',
                 'alternativas': ['Augusto',
                                  'Justiniano',
                                  'Trajano',
                                  'Nerón',
                                  'Adriano'],
                 'correcta': 'B'},
                {'pregunta': 'En arquitectura, los romanos introdujeron de '
                             'mesopotámicos y etruscos el arco, la bóveda y:',
                 'alternativas': ['El obelisco',
                                  'La cúpula',
                                  'La pirámide',
                                  'El zigurat',
                                  'El capitel dórico exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'Los romanos utilizaron como materiales de '
                             'construcción piedra, ladrillo y:',
                 'alternativas': ['Madera exclusivamente',
                                  'Hormigón con cal como argamasa',
                                  'Barro cocido exclusivamente',
                                  'Vidrio',
                                  'Bronce exclusivo'],
                 'correcta': 'B'},
                {'pregunta': 'El Coliseo Romano también es conocido como:',
                 'alternativas': ['El Foro Romano',
                                  'El Anfiteatro de Flavio',
                                  'El Panteón',
                                  'La Basílica de Majencio',
                                  'El Circo Máximo'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las construcciones romanas más '
                             'representativas, además del Coliseo, están el '
                             'Arco de Tito y el Arco de:',
                 'alternativas': ['Constantino exclusivamente',
                                  'Trajano',
                                  'Adriano',
                                  'Vespasiano',
                                  'Domiciano'],
                 'correcta': 'B'},
                {'pregunta': 'En la arquitectura griega, la riqueza '
                             'ornamental con flores de acanto pertenece al '
                             'orden: (UNSAAC 2011)',
                 'alternativas': ['Corintio',
                                  'Dórico',
                                  'Jónico',
                                  'Mixto',
                                  'Compuesto'],
                 'correcta': 'A'},
                {'pregunta': 'La obra escultórica el Discóbolo, de la '
                             'antigua Grecia, fue obra del artista: (UNSAAC '
                             '2013)',
                 'alternativas': ['Mirón',
                                  'Lisipo',
                                  'Praxiteles',
                                  'Policleto',
                                  'Fidias'],
                 'correcta': 'A'},
                {'pregunta': 'En la cultura romana antigua, Cerdeña formaba '
                             'parte de la zona: (UNSAAC 2013)',
                 'alternativas': ['Meridional',
                                  'Peninsular',
                                  'Insular',
                                  'Septentrional',
                                  'Continental'],
                 'correcta': 'C'},
                {'pregunta': 'El último emperador romano, Rómulo Augústulo, '
                             'fue destronado por Odoacro, rey de los '
                             'bárbaros: (UNSAAC 2013)',
                 'alternativas': ['Hérulos',
                                  'Hunos',
                                  'Vándalos',
                                  'Visigodos',
                                  'Ostrogodos'],
                 'correcta': 'A'},
                {'pregunta': 'El Derecho Romano, uno de los logros y aportes '
                             'más importantes a la humanidad, se caracteriza '
                             'por ser: (UNSAAC 2013)',
                 'alternativas': ['Elitista y racista',
                                  'Democrático y bondadoso',
                                  'Coercitivo y liberal',
                                  'Humanitario y generoso',
                                  'Consuetudinario y elemental'],
                 'correcta': 'D'},
                {'pregunta': 'Los gobernantes del Periodo Republicano de '
                             'Roma Antigua se denominaron: (UNSAAC 2016)',
                 'alternativas': ['Gobernadores',
                                  'Presidentes',
                                  'Reyes',
                                  'Cónsules',
                                  'Emperadores'],
                 'correcta': 'D'},
                {'pregunta': 'En el periodo histórico de Grecia Clásica, '
                             'Atenas se caracterizó por ser: (UNSAAC 2016)',
                 'alternativas': ['Gerontocrática',
                                  'Militarizada',
                                  'Democrática',
                                  'Autoritaria',
                                  'Plutocrática'],
                 'correcta': 'C'},
                {'pregunta': 'La Ley de las doce tablas fue la base del '
                             'Derecho Romano, según el historiador: (UNSAAC '
                             '2016)',
                 'alternativas': ['Tácito',
                                  'Tito Livio',
                                  'Jenofonte',
                                  'Tucídides',
                                  'Heródoto'],
                 'correcta': 'B'},
                {'pregunta': 'Los tres poderes: el Senado, las Asambleas y '
                             'la Magistratura, en la Roma Antigua, '
                             'correspondieron a la forma de gobierno: '
                             '(UNSAAC 2018)',
                 'alternativas': ['Imperial',
                                  'Autocrático',
                                  'Monárquico',
                                  'Republicano',
                                  'Autónomo'],
                 'correcta': 'D'},
                {'pregunta': 'En la arquitectura griega, el teatro de planta '
                             'circular, el estadio y el hipódromo '
                             'correspondieron al tipo de construcción: '
                             '(UNSAAC 2018)',
                 'alternativas': ['Civil',
                                  'Familiar',
                                  'Religioso',
                                  'Individual',
                                  'Militar'],
                 'correcta': 'A'},
                {'pregunta': 'Después de su máximo esplendor y poder, la '
                             'Roma Republicana pasó al periodo imperial, '
                             'cuyo primer emperador fue: (UNSAAC 2022)',
                 'alternativas': ['César Augusto',
                                  'Marco Antonio',
                                  'Rómulo Augústulo',
                                  'Teodosio',
                                  'Julio César'],
                 'correcta': 'A'},
                {'pregunta': 'Las ciudades de Mileto, Éfeso y otras, fueron '
                             'constituidas en la región de la Grecia: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Balcánica',
                                  'Continental',
                                  'Jónica',
                                  'Insular',
                                  'Peninsular'],
                 'correcta': 'C'},
                {'pregunta': 'Uno de los aportes de Roma Antigua a la '
                             'humanidad, es: (UNSAAC Ordinario)',
                 'alternativas': ['La democracia',
                                  'La astronomía',
                                  'La cerámica',
                                  'El derecho',
                                  'La biología'],
                 'correcta': 'D'},
                {'pregunta': 'En el periodo republicano de Roma antigua, los '
                             'gobernantes se denominaron: (UNSAAC Ordinario)',
                 'alternativas': ['Presidentes',
                                  'Cónsules',
                                  'Reyes',
                                  'Monarcas',
                                  'Emperadores'],
                 'correcta': 'B'},
                {'pregunta': 'El origen del pueblo griego se encuentra en '
                             'los: (UNSAAC Ordinario)',
                 'alternativas': ['Corintios',
                                  'Cretenses',
                                  'Jónicos',
                                  'Atenienses',
                                  'Pelasgos'],
                 'correcta': 'E'},
                {'pregunta': 'El Rey Minos representó al proceso histórico '
                             'de la civilización correspondiente a: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Grecia Clásica o de Apogeo',
                                  'La Cretense o Minoica',
                                  'La época oscura de la Cultura Griega',
                                  'Grecia Arcaica o Heroica',
                                  'Grecia Helenística o decadente'],
                 'correcta': 'B'},
                {'pregunta': 'En el proceso histórico de Roma imperial, la '
                             'muerte del emperador Teodosio trajo como '
                             'consecuencia la división del imperio entre sus '
                             'hijos: (UNSAAC Ordinario)',
                 'alternativas': ['Pericles - Hugo Hostilio',
                                  'Servio Tulio - Tarquino el Soberbio',
                                  'Rómulo - Numa Pompilio',
                                  'Anco Marcio - Tarquino el Soberbio',
                                  'Honorio - Arcadio'],
                 'correcta': 'E'},
                {'pregunta': 'Las ciudades de Mileto, Éfeso y Halicarnaso se '
                             'ubicaron en la región de la Grecia: (I CEPRU '
                             '2010)',
                 'alternativas': ['Helénica',
                                  'Jónica',
                                  'Insular',
                                  'Dórica',
                                  'Continental'],
                 'correcta': 'B'},
                {'pregunta': 'En la Grecia Jónica, los griegos fundaron '
                             'ciudades como: (I CEPRU 2011)',
                 'alternativas': ['Delos - Etolia',
                                  'Samos - Etolia',
                                  'Mileto - Éfeso',
                                  'Etolia - Tesalia',
                                  'Creta - Delos'],
                 'correcta': 'C'},
                {'pregunta': 'En la Cultura Griega, Mirón fue autor de la '
                             'obra: (I CEPRU 2011)',
                 'alternativas': ['Figuras más esbeltas',
                                  'Curvo de los cuerpos',
                                  'Relieves de los frontones',
                                  'Discóbolo',
                                  'Proporciones ideales del cuerpo'],
                 'correcta': 'D'},
                {'pregunta': 'En la escultura griega el autor del Discóbolo '
                             'es: (I CEPRU 2012)',
                 'alternativas': ['Mirón',
                                  'Fidias',
                                  'Praxíteles',
                                  'Policleto',
                                  'Lisipo'],
                 'correcta': 'A'},
                {'pregunta': 'La cultura romana se desarrolló en la '
                             'península: (I CEPRU 2012)',
                 'alternativas': ['De los Balcanes',
                                  'De Peloponeso',
                                  'Griega',
                                  'Itálica',
                                  'Ibérica'],
                 'correcta': 'D'},
                {'pregunta': 'En el periodo republicano de Roma fue '
                             'gobernada por: (I CEPRU 2012)',
                 'alternativas': ['Reyes',
                                  'Cónsules',
                                  'Emperadores',
                                  'Condes',
                                  'Monarcas'],
                 'correcta': 'B'},
                {'pregunta': 'La cultura que incorporó en sus construcciones '
                             'arquitectónicas, las columnas y capiteles '
                             'griegos: (I CEPRU 2014)',
                 'alternativas': ['Egipcia',
                                  'Babilónica',
                                  'Mesopotámica',
                                  'Romana',
                                  'Hebrea'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'GRECIA — PROCESO HISTÓRICO',
                      'items': ['Se desarrolló en el sur de la península de '
                                'los Balcanes, en torno al mar Egeo.',
                                'Grecia Arcaica o Heroica (800–494 a.C.): se '
                                'formaron las polis o ciudades-Estado.',
                                'Grecia Clásica o del Apogeo (494–359 a.C.): '
                                'destacaron Atenas y Esparta.',
                                'La democracia —gobierno del pueblo— fue '
                                'introducida por el legislador Solón y se '
                                'consolidó en Atenas.',
                                'Con el gobierno de Pericles, Atenas vivió '
                                'su máximo esplendor, llamado Siglo de Oro.',
                                'Grecia Decadente y Helenística (359–146 '
                                'a.C.): Alejandro Magno extendió la cultura '
                                'griega hasta la India; a su muerte el '
                                'imperio se repartió entre sus generales.']},
                     {'titulo': 'ORGANIZACIÓN POLÍTICA',
                      'items': ['Quien sistematizó la organización política '
                                'de Esparta fue Licurgo.',
                                'Quien organizó políticamente Atenas fue '
                                'Solón, considerado el más amable y '
                                'bondadoso de los legisladores.']},
                     {'titulo': 'EXPRESIONES CULTURALES',
                      'items': ['Arquitectura: destaca el Partenón, erigido '
                                'en la Acrópolis de Atenas.',
                                'Escultura: Fidias fue autor de los relieves '
                                'de los frontones y las metopas del '
                                'Partenón.']},
                     {'titulo': 'ROMA — PROCESO HISTÓRICO',
                      'items': ['Se desarrolló en la península Itálica. La '
                                'historia de Roma se inicia el año 753 a.C. '
                                'con su fundación por Rómulo.',
                                'Roma Monárquica (753–509 a.C.): el cargo '
                                'del rey era vitalicio. Con Rómulo se '
                                'iniciaron la asamblea y el Senado. Los '
                                'últimos reyes fueron de origen etrusco.',
                                'Roma Republicana (509–27 a.C.): gobierno de '
                                'cónsules, Senado y asambleas.',
                                'Roma Imperial (27 a.C.–476 d.C.): el primer '
                                'emperador fue Octavio Augusto. Este periodo '
                                'se conoce como la pax romana.',
                                'Desde el siglo III d.C. el imperio sufrió '
                                'crisis militares, políticas y económicas, y '
                                'un proceso de ruralización.']},
                     {'titulo': 'ROMA: EXPRESIONES CULTURALES',
                      'items': ['El derecho romano es la compilación de '
                                'leyes, tratados y normativas establecidas '
                                'en distintas épocas de Roma.',
                                'La Ley de las 12 Tablas fue, según Tito '
                                'Livio, la fuente de todo el derecho romano, '
                                'público y privado.',
                                'El derecho romano es considerado el aporte '
                                'más grande de Roma a la humanidad, '
                                'inspirando las legislaciones de casi todos '
                                'los países.',
                                'El emperador Justiniano es considerado el '
                                'padre del derecho romano por su gran labor '
                                'legislativa.',
                                'En arquitectura, los romanos introdujeron '
                                'de mesopotámicos y etruscos el arco, la '
                                'bóveda y la cúpula.',
                                'Los romanos utilizaron materiales como '
                                'piedra, ladrillo y hormigón con cal como '
                                'argamasa.',
                                'Entre las construcciones romanas más '
                                'representativas están el Coliseo '
                                '(Anfiteatro de Flavio), el Arco de Tito y '
                                'el Arco de Trajano.']}],
  'qr_reto': [{'pregunta': 'Las ciudades de Mileto, Éfeso y otras, fueron '
                           'constituidas en la región de la Grecia:',
               'respuesta': 'Jónica'},
              {'pregunta': 'La cultura que incorporó en sus construcciones '
                           'arquitectónicas, las columnas y capiteles '
                           'griegos:',
               'respuesta': 'Romana'},
              {'pregunta': 'Alejandro Magno extendió la cultura griega '
                           'hasta:',
               'respuesta': 'La India'}],
  'qr_dato': 'Escultura: Fidias fue autor de los relieves de los frontones y '
             'las metopas del Partenón.'},
 {'num': 5,
  'titulo': 'Primeras culturas andinas',
  'secciones': [{'titulo': '5.1 EL POBLAMIENTO DE AMÉRICA',
                 'items': ['El poblamiento de América ocurrió por el antiguo '
                           'proceso de {migración} humana, debido a cambios '
                           'climáticos del periodo {pleistoceno}.',
                           'Cronológicamente, el poblamiento de América se '
                           'remonta a aproximadamente {60 000} a.C.',
                           'De las culturas americanas surgidas del '
                           'poblamiento destacaron aztecas, mayas e {incas}.',
                           'El asunto del origen del hombre americano es '
                           'explicado, desde fines del siglo XIX, por '
                           'diversas {teorías}.']},
                {'titulo': '5.2 TEORÍAS SOBRE EL POBLAMIENTO DE AMÉRICA',
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
                           'no se conocía la {cerámica}.']}],
  'cuadros': [{'titulo': '5.2 TEORÍAS Y AUTORES',
               'encabezados': ['Teoría', 'Autor', 'Año'],
               'filas': [['Autoctonista', '{Florentino Ameghino}', '{1879}'],
                         ['Origen asiático', '{Alex Hrdlicka}', '1908'],
                         ['Origen oceánico', '{Paul Rivet}', '{1943}'],
                         ['Origen australiano', '{Mendes Correa}', '—']]},
              {'titulo': '5.3 PERIODOS PRECERÁMICOS DEL PERÚ',
               'encabezados': ['Periodo', 'Sitio clave', 'Aporte'],
               'filas': [['{Nómadas}',
                          '{Paccaicasa}, Toquepala, Lauricocha',
                          'Caza y {recolección}'],
                         ['{Seminómadas}',
                          '{Guitarrero}, Paracas',
                          'Primera {agricultura}'],
                         ['{Sedentarios}',
                          '{Kotosh}',
                          'Aldeas antes de la {cerámica}']]}],
  'preguntas': [{'pregunta': 'La teoría autoctonista del poblamiento '
                             'americano fue sostenida por:',
                 'alternativas': ['Julio C. Tello',
                                  'Paul Rivet',
                                  'Florentino Ameghino',
                                  'Alex Hrdlicka',
                                  'Mendes Correa'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría autoctonista fue rebatida en 1908 '
                             'por:',
                 'alternativas': ['Richard MacNeish',
                                  'Alex Hrdlicka',
                                  'Augusto Cardich',
                                  'Thomas Lynch',
                                  'Paul Rivet'],
                 'correcta': 'B'},
                {'pregunta': 'Según Hrdlicka, el poblamiento de América se '
                             'produjo a través del:',
                 'alternativas': ['Estrecho de Bering',
                                  'Océano Pacífico',
                                  'Mar de Behring meridional',
                                  'Istmo de Panamá',
                                  'Océano Atlántico'],
                 'correcta': 'A'},
                {'pregunta': 'La teoría de origen oceánico fue sustentada '
                             'por:',
                 'alternativas': ['Ameghino',
                                  'Hrdlicka',
                                  'Mendes Correa',
                                  'Uhle',
                                  'Paul Rivet'],
                 'correcta': 'E'},
                {'pregunta': 'La teoría de origen australiano se atribuye a:',
                 'alternativas': ['Hrdlicka',
                                  'Paul Rivet',
                                  'Lynch',
                                  'Mendes Correa',
                                  'Ameghino'],
                 'correcta': 'D'},
                {'pregunta': 'Los restos líticos más antiguos del Perú se '
                             'hallaron en:',
                 'alternativas': ['Guitarrero',
                                  'Paccaicasa',
                                  'Lauricocha',
                                  'Toquepala',
                                  'Kotosh'],
                 'correcta': 'B'},
                {'pregunta': 'El arte rupestre más antiguo del Perú '
                             'corresponde a:',
                 'alternativas': ['Paccaicasa',
                                  'Kotosh',
                                  'Paracas',
                                  'Toquepala',
                                  'Lauricocha'],
                 'correcta': 'D'},
                {'pregunta': 'Los primeros restos óseos humanos del Perú se '
                             'encontraron en:',
                 'alternativas': ['Lauricocha',
                                  'Chilca',
                                  'Toquepala',
                                  'Guitarrero',
                                  'Paccaicasa'],
                 'correcta': 'A'},
                {'pregunta': 'Los primeros indicios de agricultura en el '
                             'Perú se hallaron en:',
                 'alternativas': ['Guitarrero',
                                  'Toquepala',
                                  'Kotosh',
                                  'Lauricocha',
                                  'Paccaicasa'],
                 'correcta': 'A'},
                {'pregunta': 'El Templo de las Manos Cruzadas pertenece a:',
                 'alternativas': ['Paracas',
                                  'Caral',
                                  'Sechín',
                                  'Chavín',
                                  'Kotosh'],
                 'correcta': 'E'},
                {'pregunta': 'Kotosh fue estudiado por:',
                 'alternativas': ['Ruth Shady',
                                  'Federico Kauffmann',
                                  'Rafael Larco',
                                  'Julio C. Tello',
                                  'Max Uhle'],
                 'correcta': 'D'},
                {'pregunta': 'El periodo se denomina precerámico porque:',
                 'alternativas': ['No se domesticaban animales',
                                  'No había arquitectura',
                                  'No se conocía la agricultura',
                                  'Aún no se conocía la cerámica',
                                  'No existía la textilería'],
                 'correcta': 'D'},
                {'pregunta': 'El chaco representado en Toquepala consistía '
                             'en:',
                 'alternativas': ['Una caza ritual colectiva',
                                  'Una danza guerrera',
                                  'Una ceremonia funeraria',
                                  'Un ritual de siembra',
                                  'Un intercambio comercial'],
                 'correcta': 'A'},
                {'pregunta': 'Ameghino sostuvo que los restos fósiles '
                             'correspondían a la Era:',
                 'alternativas': ['Cuaternaria',
                                  'Terciaria',
                                  'Secundaria',
                                  'Precámbrica',
                                  'Primaria'],
                 'correcta': 'B'},
                {'pregunta': 'El periodo de los nómadas andinos se '
                             'caracterizó por ser:',
                 'alternativas': ['Agricultores sedentarios',
                                  'Recolectores, cazadores y pescadores',
                                  'Metalurgistas',
                                  'Ganaderos y alfareros',
                                  'Comerciantes'],
                 'correcta': 'B'},
                {'pregunta': 'Guitarrero se ubica en el actual departamento '
                             'de:',
                 'alternativas': ['Tacna',
                                  'Áncash',
                                  'Huánuco',
                                  'Ayacucho',
                                  'Ica'],
                 'correcta': 'B'},
                {'pregunta': 'Paccaicasa se ubica en:',
                 'alternativas': ['Tacna',
                                  'Áncash',
                                  'Lima',
                                  'Ayacucho',
                                  'Huánuco'],
                 'correcta': 'D'},
                {'pregunta': 'La teoría de Paul Rivet propone una '
                             'procedencia melanésica y:',
                 'alternativas': ['Africana',
                                  'Australiana',
                                  'Polinésica',
                                  'Europea',
                                  'Asiática'],
                 'correcta': 'C'},
                {'pregunta': 'Toquepala se ubica en el departamento de:',
                 'alternativas': ['Arequipa',
                                  'Ica',
                                  'Tacna',
                                  'Puno',
                                  'Moquegua'],
                 'correcta': 'C'},
                {'pregunta': 'En Paracas, durante el precerámico, se '
                             'registró la recolección de:',
                 'alternativas': ['Coca y ají únicamente',
                                  'Tomatillos, yuca y algodón',
                                  'Papa y oca',
                                  'Maíz y quinua',
                                  'Trigo y cebada'],
                 'correcta': 'B'},
                {'pregunta': 'El poblamiento de América ocurrió como '
                             'consecuencia del antiguo proceso de:',
                 'alternativas': ['Comercio marítimo',
                                  'Migración de la especie humana',
                                  'Colonización europea',
                                  'Intercambio cultural',
                                  'Guerra intercontinental'],
                 'correcta': 'B'},
                {'pregunta': 'Los drásticos cambios climáticos que '
                             'influyeron en el poblamiento de América '
                             'ocurrieron durante el periodo:',
                 'alternativas': ['Holoceno',
                                  'Pleistoceno',
                                  'Mioceno',
                                  'Cuaternario tardío exclusivo',
                                  'Terciario'],
                 'correcta': 'B'},
                {'pregunta': 'El poblamiento del continente americano se '
                             'remonta cronológicamente a aproximadamente:',
                 'alternativas': ['10 000 a.C.',
                                  '60 000 a.C.',
                                  '100 000 a.C.',
                                  '5000 a.C.',
                                  '1000 a.C.'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las altas culturas que se desarrollaron '
                             'en América tras el poblamiento destacan '
                             'aztecas, mayas e:',
                 'alternativas': ['Egipcios',
                                  'Incas',
                                  'Fenicios',
                                  'Sumerios',
                                  'Persas'],
                 'correcta': 'B'},
                {'pregunta': 'El interés por conocer el origen del hombre '
                             'americano surgió especialmente tras:',
                 'alternativas': ['La independencia de las colonias',
                                  'La llegada de los europeos a fines del '
                                  'siglo XV',
                                  'La Segunda Guerra Mundial',
                                  'La Revolución Industrial',
                                  'El descubrimiento del petróleo'],
                 'correcta': 'B'},
                {'pregunta': 'Al poblar América, los melanesios llegaron a: '
                             '(UNSAAC 2010)',
                 'alternativas': ['Sudamérica',
                                  'Norteamérica',
                                  'Centroamérica',
                                  'La isla de Pascua',
                                  'Las islas Aleutianas'],
                 'correcta': 'A'},
                {'pregunta': 'En su viaje hacia América, los australianos '
                             'cruzaron: (UNSAAC 2010)',
                 'alternativas': ['Alaska, Canadá y Centroamérica',
                                  'La Antártida, Tierra del Fuego y '
                                  'Patagonia',
                                  'El estrecho de Bering',
                                  'Centroamérica y la Antártica',
                                  'Isla de Puna y América del Norte'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría que sostiene que se utilizó la Isla '
                             'de Pascua para llegar a Sudamérica corresponde '
                             'a la teoría: (UNSAAC 2011)',
                 'alternativas': ['Melanésica',
                                  'Polinésica',
                                  'Australiana',
                                  'Autoctonista',
                                  'Asiática'],
                 'correcta': 'B'},
                {'pregunta': 'El descubridor del Protohomo Pampeanus fue: '
                             '(UNSAAC 2013)',
                 'alternativas': ['Thor Heyerdahl',
                                  'Florentino Ameghino',
                                  'Paul Rivet',
                                  'Alex Hrdlicka',
                                  'José Imbelloni'],
                 'correcta': 'B'},
                {'pregunta': 'La posible inmigración humana a Sudamérica, '
                             'por la corriente Sur-Ecuatorial, es de '
                             'procedencia: (UNSAAC 2013)',
                 'alternativas': ['Asiática',
                                  'Melanésica',
                                  'Polinésica',
                                  'Australiana',
                                  'Oceánica'],
                 'correcta': 'B'},
                {'pregunta': 'Los restos fósiles hallados por Florentino '
                             'Ameghino para sustentar la teoría autoctonista '
                             'del poblamiento americano se encontraban en el '
                             'estrato subterráneo del: (UNSAAC 2013)',
                 'alternativas': ['Mioceno',
                                  'Plioceno',
                                  'Eoceno',
                                  'Holoceno',
                                  'Pleistoceno'],
                 'correcta': 'B'},
                {'pregunta': 'La hamaca, la cerbatana y la pachamanca son '
                             'elementos culturales demostrativos de la '
                             'presencia en América de los: (UNSAAC 2013)',
                 'alternativas': ['Mongoles',
                                  'Australianos',
                                  'Asiáticos',
                                  'Siberianos',
                                  'Oceánicos'],
                 'correcta': 'C'},
                {'pregunta': 'Según Florentino Ameghino, el origen del '
                             'hombre americano se inició en: (UNSAAC 2016)',
                 'alternativas': ['América y Asia',
                                  'Europa y América',
                                  'América del Norte',
                                  'América del Sur',
                                  'Asia y Europa'],
                 'correcta': 'A'},
                {'pregunta': 'La teoría del Origen Asiático planteada por '
                             'Alex Hrdlicka está sustentada en pruebas: '
                             '(UNSAAC 2016)',
                 'alternativas': ['Climáticas y metalúrgicas',
                                  'Metalúrgicas y antroposomáticas',
                                  'Geográficas y metalúrgicas',
                                  'Minerológicas y cerámicas',
                                  'Antroposomáticas y Geográficas'],
                 'correcta': 'E'},
                {'pregunta': 'La constitución de las chozas en forma de '
                             'colmena y el uso del boomerang se reconocen '
                             'como elementos probatorios de la presencia en '
                             'América de los: (UNSAAC 2016)',
                 'alternativas': ['Africanos',
                                  'Polinesios',
                                  'Australianos',
                                  'Melanesios',
                                  'Asiáticos'],
                 'correcta': 'D'},
                {'pregunta': 'La Teoría Autoctonista del Poblamiento de '
                             'América fue planteada por: (UNSAAC 2018)',
                 'alternativas': ['Julio César Tello',
                                  'Luis Guillermo Lumbreras',
                                  'Paul Rivet',
                                  'Antonio Méndez Correa',
                                  'Florentino Ameghino'],
                 'correcta': 'E'},
                {'pregunta': 'Sobre el Poblamiento de América, los elementos '
                             'culturales como la construcción de chozas en '
                             'forma de colmena, el boomerang y el churinga '
                             'corresponden a la Teoría sustentada por: '
                             '(UNSAAC 2018)',
                 'alternativas': ['Julio César Tello',
                                  'Antonio Méndez Correa',
                                  'Florentino Ameghino',
                                  'Paul Rivet',
                                  'Alex Hrdlicka'],
                 'correcta': 'B'},
                {'pregunta': 'La Teoría de Origen Asiático del Hombre '
                             'Americano fue planteada por: (UNSAAC 2018)',
                 'alternativas': ['Ruth Shady',
                                  'Antonio Méndez Correa',
                                  'Max Uhle',
                                  'Paul Rivet',
                                  'Alex Hrdlicka'],
                 'correcta': 'E'},
                {'pregunta': 'La teoría Inmigracionista de origen Oceánico, '
                             'Melanésica y Polinésica fue propuesta por: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Florentino Ameghino',
                                  'Alex Hrdlicka',
                                  'Paul Rivet',
                                  'Antonio Méndez Correa',
                                  'José Imbelloni'],
                 'correcta': 'C'},
                {'pregunta': 'La Teoría del Homo Pampeanus (Hombre de la '
                             'Pampa) es sustentada por el investigador: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Thomas Linch',
                                  'Florentino Ameghino',
                                  'Alex Hrdlicka',
                                  'Paul Rivet',
                                  'Méndez Correa'],
                 'correcta': 'B'},
                {'pregunta': 'El autor de la Teoría del Origen Polinésico '
                             'del hombre americano es: (UNSAAC Ordinario)',
                 'alternativas': ['Joseph de Acosta',
                                  'Alex Hrdlicka',
                                  'Antonio Méndez',
                                  'Paul Rivet',
                                  'Florentino Ameghino'],
                 'correcta': 'D'},
                {'pregunta': 'La Teoría de la Inmigración de grupos '
                             'paleomongoloides a través del estrecho de '
                             'Bering corresponde a: (UNSAAC Ordinario)',
                 'alternativas': ['Paul Rivet',
                                  'Antonio Méndez Correa',
                                  'Alex Hrdlicka',
                                  'Julio C. Tello',
                                  'Max Uhle'],
                 'correcta': 'C'},
                {'pregunta': 'En el proceso del poblamiento de América, los '
                             'polinesios llegaron por la: (UNSAAC Ordinario)',
                 'alternativas': ['Ruta de Bering',
                                  'Corriente sur ecuatorial',
                                  'Corriente de Kuro Shiwo',
                                  'Antártida',
                                  'Corriente nor ecuatorial'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría de origen asiático sustentada por '
                             'Alex Hrdlicka está basada en pruebas de '
                             'carácter: (UNSAAC Ordinario)',
                 'alternativas': ['Paleontológico y arqueológico',
                                  'Lingüístico y Cultural',
                                  'Antroposomático y geográfico',
                                  'Físico y cultural',
                                  'Antroposomático y cultural'],
                 'correcta': 'C'},
                {'pregunta': 'El testimonio sobre el origen evolutivo del '
                             'hombre americano según Florentino Ameghino es: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['La migración de pueblos asiáticos por el '
                                  'estrecho de Bering hacia las costas '
                                  'occidentales de Canadá',
                                  'La semejanza física entre asiáticos y '
                                  'americanos',
                                  'La migración de melanesios de Nueva '
                                  'Guinea a Lagoa Santa en Brasil',
                                  'La presencia del grupo sanguíneo RHO+ '
                                  'australiano en las poblaciones de '
                                  'Patagonia',
                                  'La existencia de elementos óseos del '
                                  'Protohomo Pampeanus'],
                 'correcta': 'E'},
                {'pregunta': 'La Teoría Inmigracionista de Origen '
                             'Australiano sostiene: (UNSAAC Ordinario)',
                 'alternativas': ['La traslación de expertos navegantes de '
                                  'Polinesia a través de Isla de Pascua '
                                  'llegó a Sudamérica',
                                  'El paso de hombres primitivos por '
                                  'Tasmania que llegaron a la Patagonia',
                                  'La traslación de hombres primitivos de '
                                  'Melanesia hacia América Central',
                                  'El paso de hombres primitivos del Asia '
                                  'por el estrecho de Bering',
                                  'La formación del Homo Pampeanus en la '
                                  'comarca de Chapalmalal'],
                 'correcta': 'B'},
                {'pregunta': 'La oleada expansiva asiática a América se '
                             'produjo en la glaciación de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Nebraska',
                                  'Kansas',
                                  'Wisconsin',
                                  'Illinois',
                                  'Mindel'],
                 'correcta': 'C'},
                {'pregunta': 'En el poblamiento americano, llegaron a la '
                             'Tierra del Fuego y la Patagonia Argentina, '
                             'los: (UNSAAC Ordinario)',
                 'alternativas': ['Australianos',
                                  'Melanesios',
                                  'Asiáticos',
                                  'Oceánicos',
                                  'Polinesios'],
                 'correcta': 'A'},
                {'pregunta': 'De acuerdo a la Teoría del Poblamiento '
                             'Americano, los navegantes que llegaron al '
                             'extremo sur de Sudamérica, pasando por la isla '
                             'de Pascua, fueron los: (UNSAAC Ordinario)',
                 'alternativas': ['Polinesios',
                                  'Melanesios',
                                  'Asiáticos',
                                  'La Antártida',
                                  'Australianos'],
                 'correcta': 'A'},
                {'pregunta': 'En el Poblamiento de América, la Teoría '
                             'Poligenista fue sustentada por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Pablo Macera',
                                  'Alex Hrdlicka',
                                  'Florentino Ameghino',
                                  'Paul Rivet',
                                  'Antonio Méndez Correa'],
                 'correcta': 'D'},
                {'pregunta': 'El poblamiento de américa se dio en la era: (I '
                             'CEPRU 2010)',
                 'alternativas': ['Terciaria',
                                  'Cuaternaria',
                                  'Superior',
                                  'Primario',
                                  'Secundaria'],
                 'correcta': 'B'},
                {'pregunta': 'La Teoría inmigracionista sobre el poblamiento '
                             'americano, basada en la posición poliracial, '
                             'es sustentada por: (I CEPRU 2011)',
                 'alternativas': ['Antonio Mendez Correa',
                                  'Paul Rivet',
                                  'Alex Hrdlicka',
                                  'Federico Max Uhle',
                                  'Florentino Ameghino'],
                 'correcta': 'B'},
                {'pregunta': 'La Teoría inmigracionista de origen asiático '
                             'sobre el poblamiento de américa, fue '
                             'sustentada por: (I CEPRU 2011)',
                 'alternativas': ['Luis Guillermo Lumbreras',
                                  'Antonio Mendez Correa',
                                  'Alex Hrdlicka',
                                  'Florentino Ameghino',
                                  'Paul Rivet'],
                 'correcta': 'C'},
                {'pregunta': 'Según Florentino Ameghino, el hombre americano '
                             'se habría dispersado desde la comarca de '
                             'Chapalmalal por el resto del mundo a través: '
                             '(II CEPRU 2012)',
                 'alternativas': ['De puentes intercontinentales',
                                  'Del cabo de hornos',
                                  'De la Tierra del Fuego',
                                  'Del estrecho de Bering',
                                  'De las corrientes nor ecuatoriales'],
                 'correcta': 'D'},
                {'pregunta': 'Los pobladores de Lagoa Santa «Brasil» poseen '
                             'cráneos muy semejantes a los negros de nueva '
                             'Guinea; esta afirmación es recogida en la '
                             'teoría: (II CEPRU 2012)',
                 'alternativas': ['Autoctonista',
                                  'Polinésica',
                                  'Melanésica',
                                  'Australiana',
                                  'Asiática'],
                 'correcta': 'C'},
                {'pregunta': 'La Teoría de Origen Asiático sobre el '
                             'poblamiento americano, sostiene los: (II CEPRU '
                             '2013)',
                 'alternativas': ['Grupos humanos paleomongoloides '
                                  'inmigraron a américa por el estrecho de '
                                  'Bering',
                                  'Pobladores de Lagoa Santa y de Nueva '
                                  'Guinea tienen semejanzas físicas',
                                  'Protohomo Pampeanus emigraron de américa '
                                  'a Europa',
                                  'Polinesios llegaron al extremo sur de '
                                  'América',
                                  'Asiáticos llegaron a la Tierra del Fuego '
                                  'y a la Patagonia'],
                 'correcta': 'A'},
                {'pregunta': 'El origen del hombre se originó en las pampas '
                             'argentinas, es una teoría sostenida por: (I '
                             'CEPRU 2014)',
                 'alternativas': ['Florentino Ameghino',
                                  'Alex Hrdlicka',
                                  'Paul Rivet',
                                  'Antonio Méndez Correa',
                                  'Max Uhle'],
                 'correcta': 'A'},
                {'pregunta': 'Según Antonio Méndez Correa el hombre proviene '
                             'de: (I CEPRU 2014)',
                 'alternativas': ['Oceanía',
                                  'Australia',
                                  'Asia',
                                  'Melanesia',
                                  'Polinesia'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'EL POBLAMIENTO DE AMÉRICA',
                      'items': ['El poblamiento de América ocurrió por el '
                                'antiguo proceso de migración humana, debido '
                                'a cambios climáticos del periodo '
                                'pleistoceno.',
                                'Cronológicamente, el poblamiento de América '
                                'se remonta a aproximadamente 60 000 a.C.',
                                'De las culturas americanas surgidas del '
                                'poblamiento destacaron aztecas, mayas e '
                                'incas.',
                                'El asunto del origen del hombre americano '
                                'es explicado, desde fines del siglo XIX, '
                                'por diversas teorías.']},
                     {'titulo': 'TEORÍAS SOBRE EL POBLAMIENTO DE AMÉRICA',
                      'items': ['Teoría autoctonista: sostenida por el '
                                'paleontólogo argentino Florentino Ameghino '
                                'en 1879; afirmaba que el hombre americano '
                                'era originario del continente.',
                                'Fue rebatida en 1908 por Alex Hrdlicka, '
                                'quien demostró que los restos fósiles no '
                                'correspondían a la Era Terciaria.',
                                'Teoría de origen asiático: sustentada por '
                                'Alex Hrdlicka; el poblamiento se habría '
                                'dado por el estrecho de Bering.',
                                'Teoría de origen oceánico (poligenista o '
                                'polirracial): sustentada por el francés '
                                'Paul Rivet en 1943, con procedencia '
                                'melanésica y polinésica.',
                                'Teoría de origen australiano: sostenida por '
                                'Mendes Correa.']},
                     {'titulo': 'NÓMADAS: RECOLECTORES, CAZADORES Y '
                                'PESCADORES',
                      'items': ['Paccaicasa (Ayacucho): los restos líticos '
                                'más antiguos del Perú, hallados por Richard '
                                'MacNeish.',
                                'Toquepala (Tacna): arte rupestre más '
                                'antiguo; representa el chaco o caza ritual.',
                                'Lauricocha (Huánuco): primeros restos óseos '
                                'humanos, hallados por Augusto Cardich.']},
                     {'titulo': 'SEMINÓMADAS: HORTICULTORES',
                      'items': ['Guitarrero (Áncash): primeros indicios de '
                                'agricultura en el Perú, estudiados por '
                                'Thomas Lynch.',
                                'Paracas (Ica): recolectores; se registran '
                                'tomatillos, yuca y algodón.']},
                     {'titulo': 'SEDENTARIOS: AGRICULTORES',
                      'items': ['Kotosh (Huánuco): hacia 2200 a.C., '
                                'estudiado por Julio C. Tello. Destaca el '
                                'Templo de las Manos Cruzadas, considerado '
                                'el primer monumento religioso.',
                                'El periodo se denomina precerámico porque '
                                'aún no se conocía la cerámica.']}],
  'qr_reto': [{'pregunta': 'Según Antonio Méndez Correa el hombre proviene '
                           'de:',
               'respuesta': 'Australia'},
              {'pregunta': 'La Teoría de Origen Asiático del Hombre '
                           'Americano fue planteada por:',
               'respuesta': 'Alex Hrdlicka'},
              {'pregunta': 'Según Florentino Ameghino, el hombre americano '
                           'se habría dispersado desde la comarca de '
                           'Chapalmalal por el resto del mundo a través:',
               'respuesta': 'Del estrecho de Bering'}],
  'qr_dato': 'El periodo se denomina precerámico porque aún no se conocía la '
             'cerámica.'},
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
                           'derrotados por los {incas}.']}],
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
                 'alternativas': ['Paracas',
                                  'Tiahuanaco',
                                  'Mochica',
                                  'Chavín',
                                  'Caral'],
                 'correcta': 'E'},
                {'pregunta': 'Caral fue investigada principalmente por:',
                 'alternativas': ['Rafael Larco',
                                  'Ruth Shady',
                                  'María Reiche',
                                  'Max Uhle',
                                  'Julio C. Tello'],
                 'correcta': 'B'},
                {'pregunta': 'Chavín de Huántar se ubica en el departamento '
                             'de:',
                 'alternativas': ['Ayacucho',
                                  'Huánuco',
                                  'Ica',
                                  'La Libertad',
                                  'Áncash'],
                 'correcta': 'E'},
                {'pregunta': 'Julio C. Tello denominó a Chavín como la '
                             'cultura:',
                 'alternativas': ['Imperial',
                                  'Síntesis',
                                  'Matriz de la civilización andina',
                                  'Local',
                                  'Fusionante'],
                 'correcta': 'C'},
                {'pregunta': 'La organización política de Chavín fue:',
                 'alternativas': ['Democrática',
                                  'Republicana',
                                  'Federal',
                                  'Teocrática',
                                  'Militarista'],
                 'correcta': 'D'},
                {'pregunta': 'Las cabezas clavas eran consideradas:',
                 'alternativas': ['Sellos de propiedad',
                                  'Guardianes del templo',
                                  'Marcadores astronómicos',
                                  'Instrumentos musicales',
                                  'Ofrendas funerarias'],
                 'correcta': 'B'},
                {'pregunta': 'La cerámica de Paracas Cavernas es:',
                 'alternativas': ['Monocroma en pre-cocción',
                                  'Bicroma',
                                  'Escultórica realista',
                                  'Polícroma en post-cocción',
                                  'Vidriada'],
                 'correcta': 'D'},
                {'pregunta': 'La capital de Paracas Necrópolis fue:',
                 'alternativas': ['Topará',
                                  'Tajahuana',
                                  'Pachacamac',
                                  'Cahuachi',
                                  'Sechín'],
                 'correcta': 'A'},
                {'pregunta': 'Paracas destacó notablemente por sus:',
                 'alternativas': ['Trepanaciones craneanas y mantos bordados',
                                  'Acueductos subterráneos',
                                  'Ciudades de barro',
                                  'Quipus',
                                  'Portadas monolíticas'],
                 'correcta': 'A'},
                {'pregunta': 'Las líneas de Nasca fueron estudiadas durante '
                             'décadas por:',
                 'alternativas': ['Rafael Larco',
                                  'María Reiche',
                                  'Ruth Shady',
                                  'Julio C. Tello',
                                  'Max Uhle'],
                 'correcta': 'B'},
                {'pregunta': 'Los acueductos de Cantalloc pertenecen a la '
                             'cultura:',
                 'alternativas': ['Chimú',
                                  'Paracas',
                                  'Mochica',
                                  'Nasca',
                                  'Wari'],
                 'correcta': 'D'},
                {'pregunta': 'La cerámica retrato o realista es '
                             'característica de:',
                 'alternativas': ['Mochica',
                                  'Nasca',
                                  'Chimú',
                                  'Chavín',
                                  'Tiahuanaco'],
                 'correcta': 'A'},
                {'pregunta': 'El Señor de Sipán pertenece a la cultura:',
                 'alternativas': ['Mochica',
                                  'Lambayeque',
                                  'Chimú',
                                  'Nasca',
                                  'Wari'],
                 'correcta': 'A'},
                {'pregunta': 'La Portada del Sol corresponde a la cultura:',
                 'alternativas': ['Nasca',
                                  'Chimú',
                                  'Chavín',
                                  'Wari',
                                  'Tiahuanaco'],
                 'correcta': 'E'},
                {'pregunta': 'El primer imperio andino, con capital en '
                             'Ayacucho, fue:',
                 'alternativas': ['Chimú',
                                  'Tiahuanaco',
                                  'Inca',
                                  'Wari',
                                  'Chavín'],
                 'correcta': 'D'},
                {'pregunta': 'Chan Chan, la ciudad de barro más grande de '
                             'América, perteneció a:',
                 'alternativas': ['Lambayeque',
                                  'Wari',
                                  'Mochica',
                                  'Nasca',
                                  'Chimú'],
                 'correcta': 'E'},
                {'pregunta': 'Los chancas se desarrollaron principalmente '
                             'en:',
                 'alternativas': ['Apurímac y Ayacucho',
                                  'Costa norte',
                                  'Valle de Supe',
                                  'Costa sur',
                                  'Altiplano del Titicaca'],
                 'correcta': 'A'},
                {'pregunta': 'Tiahuanaco se desarrolló en el altiplano del '
                             'lago:',
                 'alternativas': ['Junín',
                                  'Titicaca',
                                  'Chinchaycocha',
                                  'Parinacochas',
                                  'Poopó'],
                 'correcta': 'B'},
                {'pregunta': 'Paracas se ubicó en la provincia de Pisco, '
                             'departamento de:',
                 'alternativas': ['Tacna',
                                  'Arequipa',
                                  'Ica',
                                  'Moquegua',
                                  'Lima'],
                 'correcta': 'C'},
                {'pregunta': 'El Lanzón monolítico y la estela Raimondi '
                             'pertenecen a:',
                 'alternativas': ['Wari',
                                  'Chavín',
                                  'Tiahuanaco',
                                  'Paracas',
                                  'Caral'],
                 'correcta': 'B'},
                {'pregunta': 'En la formación de la cultura andina, el '
                             'primer resto óseo hallado perteneció al hombre '
                             'de: (UNSAAC 2013)',
                 'alternativas': ['Toquepala',
                                  'Chivateros',
                                  'Lauricocha',
                                  'Kotosh',
                                  'Lurín'],
                 'correcta': 'D'},
                {'pregunta': 'La primera evidencia sobre la domesticación '
                             'del perro fue hallada en: (UNSAAC 2013)',
                 'alternativas': ['Kotosh',
                                  'Santo Domingo',
                                  'Lurín',
                                  'Guitarreros',
                                  'Chilca'],
                 'correcta': 'E'},
                {'pregunta': 'El yacimiento arqueológico de Haldas fue '
                             'descubierto por: (UNSAAC 2013)',
                 'alternativas': ['Junius Bird',
                                  'Josefina Ramos de Cox',
                                  'Federico Engel',
                                  'Rosa Fung Pineda',
                                  'Rafael Larco Hoyle'],
                 'correcta': 'C'},
                {'pregunta': 'Los restos arqueológicos de Pumapunku, '
                             'Willcaswain y Pacatnamú corresponden '
                             'respectivamente a las culturas: (UNSAAC 2013)',
                 'alternativas': ['Wari - Inca - Caral',
                                  'Wari - Chimú - Paracas',
                                  'Tiahuanaco - Wari - Chimú',
                                  'Mochica - Wari - Chavín',
                                  'Chimú - Chanca - Nazca'],
                 'correcta': 'C'},
                {'pregunta': 'La importancia y la particularidad del hombre '
                             'de Paccaicasa se expresan en haber: (UNSAAC '
                             '2013)',
                 'alternativas': ['Practicado el arte rupestre más antiguo '
                                  'del Perú',
                                  'Originado a la gran cultura andina',
                                  'Dejado los primeros restos físicos del '
                                  'hombre',
                                  'Domesticado por primera vez al perro',
                                  'Iniciado la fabricación de objetos de '
                                  'arcilla'],
                 'correcta': 'C'},
                {'pregunta': 'El hombre de Huaca Prieta se caracterizó por: '
                             '(UNSAAC 2013)',
                 'alternativas': ['Domesticar a la alpaca, al cuy y al perro',
                                  'Construir el primer monumento religioso '
                                  'de América',
                                  'Representar el inicio de la primera etapa '
                                  'alfarera',
                                  'Presentar el taller lítico más grande del '
                                  'Perú antiguo',
                                  'Ser él primer tejedor del Perú antiguo'],
                 'correcta': 'E'},
                {'pregunta': 'La cultura Chavín tiene relación en los '
                             'centros arquitectónicos de: (UNSAAC 2013)',
                 'alternativas': ['Garagay y Chongoyape',
                                  'Topara y Tajahuana',
                                  'Cahuachi y Ocucaje',
                                  'Kalasasaya y Sillustani',
                                  'Wariwillca y Pachacamac'],
                 'correcta': 'A'},
                {'pregunta': 'Los chimús se desarrollaron en el periodo '
                             'cultural: (UNSAAC 2013)',
                 'alternativas': ['Horizonte Medio',
                                  'Horizonte Temprano',
                                  'Intermedio Tardío',
                                  'Intermedio Temprano',
                                  'Horizonte Medio tardío'],
                 'correcta': 'C'},
                {'pregunta': 'Augusto Cardich descubrió en la cueva de '
                             'Lauricocha los primeros restos físicos del '
                             'hombre peruano, los cuales corresponden a las '
                             'fuentes: (UNSAAC 2015)',
                 'alternativas': ['Antroposomáticas',
                                  'Materiales',
                                  'Etnográficas',
                                  'Biológicas',
                                  'Monumentales'],
                 'correcta': 'A'},
                {'pregunta': 'Los primeros restos humanos en el Perú antiguo '
                             'corresponden al hombre de: (UNSAAC 2016)',
                 'alternativas': ['Paccaicasa',
                                  'Chivateros',
                                  'Paiján',
                                  'Lauricocha',
                                  'Toquepala'],
                 'correcta': 'A'},
                {'pregunta': 'La organización política de la cultura Caral '
                             'fue de carácter: (UNSAAC 2016)',
                 'alternativas': ['Militarizado y gerontocrático',
                                  'Religioso y burocrático',
                                  'Militarizado y religioso',
                                  'Burocrático y militarizado',
                                  'Teocrático no militarista'],
                 'correcta': 'E'},
                {'pregunta': 'Cronológicamente los Chancas se desarrollaron '
                             'en el periodo del: (UNSAAC 2016)',
                 'alternativas': ['Intermedio tardío',
                                  'Horizonte temprano',
                                  'Intermedio temprano',
                                  'Horizonte medio',
                                  'Horizonte tardío'],
                 'correcta': 'A'},
                {'pregunta': 'El segundo agricultor del Perú fue descubierto '
                             'por Thomas Linch, en el departamento de: '
                             '(UNSAAC 2018)',
                 'alternativas': ['Huánuco',
                                  'Lima',
                                  'Ancash',
                                  'Tacna',
                                  'Ilo'],
                 'correcta': 'A'},
                {'pregunta': 'Las primeras evidencias del hombre en el Perú '
                             'fueron descubiertas en el actual departamento '
                             'de La Libertad por el científico: (UNSAAC '
                             '2018)',
                 'alternativas': ['Junius Bird',
                                  'Richard Mac Neish',
                                  'Augusto Cardich',
                                  'Miomir Bojovich',
                                  'Edward Lanning'],
                 'correcta': 'A'},
                {'pregunta': 'El conjunto arquitectónico que identifica a la '
                             'civilización de Caral es: (UNSAAC 2022)',
                 'alternativas': ['El templo de Garagay',
                                  'La Huaca del Sol',
                                  'La huaca de la Luna',
                                  'El templo de Kotosh',
                                  'El templo del Anfiteatro'],
                 'correcta': 'E'},
                {'pregunta': 'Por los hallazgos líticos, el primer poblador '
                             'del Perú fue el hombre de: (UNSAAC Ordinario)',
                 'alternativas': ['Guitarrero',
                                  'Kotosh',
                                  'Lauricocha',
                                  'Chilca',
                                  'Paccaicasa'],
                 'correcta': 'E'},
                {'pregunta': 'Del asentamiento humano de Paracas, los mantos '
                             'fueron de carácter: (UNSAAC Ordinario)',
                 'alternativas': ['Religioso y ritual',
                                  'Político',
                                  'Económico',
                                  'Artístico',
                                  'Socio económico'],
                 'correcta': 'A'},
                {'pregunta': 'La cultura Caral se ubica en el departamento '
                             'de: (UNSAAC Ordinario)',
                 'alternativas': ['Ancash',
                                  'Lima',
                                  'Ica',
                                  'Lambayeque',
                                  'La Libertad'],
                 'correcta': 'B'},
                {'pregunta': 'El hombre de Lauricocha fue descubierto por: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Thomas Linch',
                                  'Frederic Engel',
                                  'Richard Mac Neish',
                                  'Frederic Engel',
                                  'Augusto Cardich'],
                 'correcta': 'E'},
                {'pregunta': 'El asentamiento humano de Paracas fue '
                             'descubierto por: (UNSAAC Ordinario)',
                 'alternativas': ['Julio Cesar Tello Rojas',
                                  'Federico Max Uhle',
                                  'Federico Kauffman Doig',
                                  'Federico Larco Hoyle',
                                  'Ruth Shady Solís'],
                 'correcta': 'A'},
                {'pregunta': 'La construcción arquitectónica de Cahuachi '
                             'perteneció al asentamiento humano de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Paracas',
                                  'Wari',
                                  'Nazca',
                                  'Tiahuanaco',
                                  'Chavín'],
                 'correcta': 'C'},
                {'pregunta': 'La construcción del Complejo Arqueológico de '
                             'Puma Punku y las Chullpas de Sillustani '
                             'pertenecieron a: (UNSAAC Ordinario)',
                 'alternativas': ['Nazca',
                                  'Chavín',
                                  'Mochica',
                                  'Chimú',
                                  'Tiahuanaco'],
                 'correcta': 'E'},
                {'pregunta': 'La cerámica Chimú tuvo influencia de la '
                             'Cultura: (UNSAAC Ordinario)',
                 'alternativas': ['Chavín',
                                  'Paracas',
                                  'Mochica',
                                  'Nazca',
                                  'Wari'],
                 'correcta': 'C'},
                {'pregunta': 'El Altar del Fuego Sagrado, en el Perú '
                             'prehispánico, fue una manifestación '
                             'arquitectónica de la sociedad: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Caral',
                                  'Wari',
                                  'Chimú',
                                  'Paracas',
                                  'Tiahuanaco'],
                 'correcta': 'A'},
                {'pregunta': 'El hombre de Toquepala es importante en la '
                             'evolución de la cultura andina, por ser el: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Impulsor de la domesticación de camélidos',
                                  'Primer pintor rupestre peruano',
                                  'Tallador fino más antiguo y fino',
                                  'Primer horticultor alto andino',
                                  'Iniciador de la domesticación del perro'],
                 'correcta': 'B'},
                {'pregunta': 'En el proceso evolutivo de la Cultura Andina, '
                             'son consideradas culturas sedentarias: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Kotosh - Santo Domingo - Lauricocha',
                                  'Guitarrero - Chilca - Kotosh',
                                  'Lurín - Huaca Prieta - Kotosh',
                                  'Lurín - Pikimachay - Guitarrero',
                                  'Huaca Prieta - Lurín - Chivateros'],
                 'correcta': 'C'},
                {'pregunta': 'La primera manifestación arquitectónica '
                             'monumental de tipo religioso en el Perú '
                             'antiguo corresponde al hombre de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Kotosh',
                                  'Huaca Prieta',
                                  'Paccaicasa',
                                  'Las Aldas',
                                  'Guitarrero'],
                 'correcta': 'A'},
                {'pregunta': 'La manifestación arquitectónica que representa '
                             'a la cultura Chanca es: (UNSAAC Ordinario)',
                 'alternativas': ['El conjunto arquitectónico de la Huaca '
                                  'Rajada',
                                  'El conjunto arqueológico de Tarahuasi',
                                  'La fortaleza de Paramonga',
                                  'La fortificación de Pachacamac',
                                  'El conjunto arqueológico de Sóndor'],
                 'correcta': 'E'},
                {'pregunta': 'La característica que corresponde a los '
                             'primeros hombres de la Cultura Andina, en su '
                             'condición de seminómadas: (UNSAAC Ordinario)',
                 'alternativas': ['La domesticación de los primeros cultivos '
                                  'y animales',
                                  'Que no producen sus alimentos, los '
                                  'consiguen a través de la caza, la pesca y '
                                  'la recolección',
                                  'Que conviven con la megafauna de '
                                  'mastodontes y megaterios',
                                  'El desarrollo de las actividades '
                                  'artesanales como la textilería y cerámica',
                                  'El predominio de la vida aldeana y '
                                  'construcción de las primeras ciudades '
                                  'urbanas'],
                 'correcta': 'B'},
                {'pregunta': 'La civilización que es considerada como la más '
                             'antigua del Perú y América es: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Paracas',
                                  'Valdivia',
                                  'Caral',
                                  'Maya',
                                  'Chavín'],
                 'correcta': 'C'},
                {'pregunta': 'En el origen de la Cultura Andina, los '
                             'pobladores del asentamiento de Huaca Prieta se '
                             'caracterizaron por ser: (UNSAAC Ordinario)',
                 'alternativas': ['Los primeros horticultores del Perú',
                                  'Constructores del primer monumento '
                                  'religioso',
                                  'Maestros del arte textil',
                                  'Los domesticadores de la llama, alpaca y '
                                  'el cuy',
                                  'Los primeros domesticadores del perro'],
                 'correcta': 'C'},
                {'pregunta': 'De acuerdo a la periodización de Horizontes, '
                             'propuesta por John Rowe, el desarrollo de la '
                             'cultura de Wari y Tiahuanaco, corresponde al: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Horizonte formativo',
                                  'Horizonte temprano',
                                  'Horizonte del intermedio tardío',
                                  'Horizonte medio',
                                  'Intermedio temprano'],
                 'correcta': 'D'},
                {'pregunta': 'El taller lítico más grande del Perú hace '
                             'referencia al hombre de: (UNSAAC Ordinario)',
                 'alternativas': ['Complejo de Paccaicasa',
                                  'Toquepala',
                                  'Lauricocha',
                                  'Paiján',
                                  'Chivateros'],
                 'correcta': 'E'},
                {'pregunta': 'El historiador Pablo Macera considera que la '
                             'cerámica que mejor se aprecia con los ojos que '
                             'con la yema de los dedos, corresponde a la '
                             'Cultura: (UNSAAC Ordinario)',
                 'alternativas': ['Chavín',
                                  'Mochica',
                                  'Nazca',
                                  'Wari',
                                  'Tiahuanaco'],
                 'correcta': 'B'},
                {'pregunta': 'El hombre de Paccaicasa se caracteriza por: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Ser el primer músico peruano, al fabricar '
                                  'las primeras flautas',
                                  'Representar al primer resto fósil humano '
                                  'del Perú',
                                  'Domesticar la llama y la alpaca',
                                  'Ser el Iniciador de la Cultura Andina',
                                  'Practicar ritos y ceremonias a la tierra'],
                 'correcta': 'B'},
                {'pregunta': 'La pintura rupestre más antigua del Perú, '
                             'pertenece al hombre de: (I CEPRU 2010)',
                 'alternativas': ['Paiján',
                                  'Toquepala',
                                  'Lauricocha',
                                  'Chilca',
                                  'Santo domingo'],
                 'correcta': 'B'},
                {'pregunta': 'El textil Cóndor Andino pertenece al hombre '
                             'sedentario de: (I CEPRU 2010)',
                 'alternativas': ['Chilca',
                                  'Cerro Paloma',
                                  'Kotosh',
                                  'Huaca Prieta',
                                  'Lurín'],
                 'correcta': 'D'},
                {'pregunta': 'El primer pescador con red en el Perú, durante '
                             'el periodo de los horticultores fue: (II CEPRU '
                             '2012)',
                 'alternativas': ['Paiján',
                                  'Guitarrero',
                                  'Santo Domingo',
                                  'Lurín',
                                  'Chilca'],
                 'correcta': 'E'},
                {'pregunta': 'Las tumbas subterráneas en forma de copa '
                             'invertida o de botella pertenecieron a la '
                             'sociedad: (II CEPRU 2012)',
                 'alternativas': ['Paracas Cavernas',
                                  'Mochica Chicama',
                                  'Tiahuanaco Kalasasaya',
                                  'Paracas Necrópolis',
                                  'Nazca Cahuachi'],
                 'correcta': 'D'},
                {'pregunta': 'La Huaca del Sol fue dedicada al culto del '
                             'Dios: (II CEPRU 2012)',
                 'alternativas': ['Cie Quich',
                                  'Señora de Cao',
                                  'Señor de Sipán',
                                  'Aiapaec',
                                  'Naylamp'],
                 'correcta': 'D'},
                {'pregunta': 'Uno de los fundadores de la sociedad Chanca, '
                             'fue: (II CEPRU 2012)',
                 'alternativas': ['Uscovilca',
                                  'Astowaranca',
                                  'Uranmarca',
                                  'Sondor',
                                  'Curamba'],
                 'correcta': 'A'},
                {'pregunta': 'El hombre de Santo Domingo se caracteriza por: '
                             '(II CEPRU 2013)',
                 'alternativas': ['Domesticar a la llama y al cuy',
                                  'Practicar la primera agricultura andina',
                                  'Ser uno de los primeros músicos del Perú',
                                  'Representar la primera etapa alfarera en '
                                  'el Perú',
                                  'Desarrollar el taller lítico más grande '
                                  'del Perú antiguo'],
                 'correcta': 'D'},
                {'pregunta': 'Según los últimos avances arqueológicos, '
                             'Caral: (I CEPRU 2014)',
                 'alternativas': ['Se desarrolló en el periodo cultural '
                                  'formativo',
                                  'Tuvo un estado exclusivamente militarista',
                                  'Fue una civilización con expansión '
                                  'cultural pan peruana',
                                  'Representa el primer imperio andino',
                                  'Es la civilización más antigua del Perú y '
                                  'América'],
                 'correcta': 'E'},
                {'pregunta': 'A la cultura Nazca se le atribuye: (I CEPRU '
                             '2014)',
                 'alternativas': ['Las pinturas murales de Pañamarca',
                                  'El centro arqueológico de Wariwilca',
                                  'La construcción de ciudades cabeza de '
                                  'región',
                                  'El gigantesco calendario astronómico',
                                  'La organización del primer estado '
                                  'teocrático en el Perú'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'CIVILIZACIÓN CARAL',
                      'items': ['Considerada la civilización más antigua de '
                                'América, ubicada en el valle de Supe '
                                '(Barranca, Lima).',
                                'Fue investigada por la arqueóloga Ruth '
                                'Shady. Corresponde al periodo precerámico '
                                'tardío.']},
                     {'titulo': 'CHAVÍN (HORIZONTE TEMPRANO)',
                      'items': ['Su capital, Chavín de Huántar, se ubica en '
                                'Áncash, a orillas del río Mosna, en el '
                                'flanco oriental de la Cordillera Blanca.',
                                'Fue descubierta y estudiada por Julio C. '
                                'Tello, quien la llamó «cultura matriz de la '
                                'civilización andina».',
                                'Su organización política fue teocrática: la '
                                'autoridad política derivaba de lo '
                                'religioso. Su sociedad fue clasista.',
                                'Monumentos líticos: el Lanzón monolítico, '
                                'la estela Raimondi, el obelisco Tello y las '
                                'cabezas clavas, guardianes del templo.']},
                     {'titulo': 'PARACAS',
                      'items': ['Se ubicó en el departamento de Ica, '
                                'provincia de Pisco, en la bahía de Paracas. '
                                'Fue descubierta por Julio C. Tello.',
                                'Paracas Cavernas: cuenca del río Ica, '
                                'capital Tajahuana, con influencia Chavín. '
                                'Cerámica polícroma, pintada en '
                                'post-cocción.',
                                'Paracas Necrópolis: valle de Pisco, capital '
                                'Topará. Cerámica monocroma, pintada en '
                                'pre-cocción.',
                                'Destacaron por sus mantos bordados y por '
                                'las trepanaciones craneanas.']},
                     {'titulo': 'INTERMEDIO TEMPRANO',
                      'items': ['Nasca (300 a.C. – 600 d.C.): departamento '
                                'de Ica. Destacan las líneas de Nasca, '
                                'estudiadas por María Reiche, y los '
                                'acueductos de Cantalloc.',
                                'Mochica: costa norte, valles de Moche y '
                                'Chicama. Cerámica realista o retrato y '
                                'escultórica. Destaca el Señor de Sipán.']},
                     {'titulo': 'Y 6.5 HORIZONTE MEDIO E INTERMEDIO TARDÍO',
                      'items': ['Tiahuanaco: altiplano del lago Titicaca. '
                                'Destaca la Portada del Sol.',
                                'Wari: primer imperio andino, con capital en '
                                'Ayacucho. Impuso el urbanismo planificado.',
                                'Chimú: costa norte, capital Chan Chan, la '
                                'ciudad de barro más grande de América. '
                                'Destacaron en orfebrería.',
                                'Chanca: región de Apurímac y Ayacucho; '
                                'fueron derrotados por los incas.']}],
  'qr_reto': [{'pregunta': 'El Lanzón monolítico y la estela Raimondi '
                           'pertenecen a:',
               'respuesta': 'Chavín'},
              {'pregunta': 'Del asentamiento humano de Paracas, los mantos '
                           'fueron de carácter:',
               'respuesta': 'Religioso y ritual'},
              {'pregunta': 'Según los últimos avances arqueológicos, Caral:',
               'respuesta': 'Es la civilización más antigua del Perú y '
                            'América'}],
  'qr_dato': 'Nasca (300 a.C. – 600 d.C.): departamento de Ica. Destacan las '
             'líneas de Nasca, estudiadas por María Reiche, y los acueductos '
             'de Cantalloc.'},
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
                {'titulo': '7.4 ADMINISTRACIÓN Y CONTROL DE PISOS ECOLÓGICOS',
                 'items': ['El {curaca} era el jefe del ayllu, encargado de '
                           'la administración directa del territorio '
                           'comunal.',
                           'El {Tucuyricuy}, «el que todo lo ve», actuaba '
                           'como inspector del Inca en las provincias.',
                           'El Tahuantinsuyo, como institución consolidada, '
                           'fue obra del inca {Pachacútec}.',
                           'Solo las {acllas}, mujeres escogidas, estaban '
                           'autorizadas para tejer los ropajes destinados al '
                           'Inca.',
                           'Los {collcas} y tambos eran los depósitos '
                           'estatales donde se almacenaban productos del '
                           'Tahuantinsuyo.',
                           'El {control de pisos ecológicos} consistía en '
                           'que un mismo ayllu cultivara tierras en '
                           'distintas zonas climáticas, como hicieron los '
                           '{lupacas} del altiplano con tierras en la costa.',
                           'Los andenes tuvieron como finalidad ampliar y '
                           'proteger la frontera {agrícola}.']},
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
                           '{quipus}, a cargo de los {quipucamayocs}.']}],
  'cuadros': [{'titulo': '7. FORMAS DE TRABAJO',
               'encabezados': ['Forma', 'Definición'],
               'filas': [['{Ayni}',
                          'Ayuda mutua y {recíproca} entre familias'],
                         ['{Minka}',
                          'Trabajo {comunal} en beneficio del ayllu'],
                         ['{Mita}',
                          'Trabajo por {turnos} al servicio del Estado']]}],
  'preguntas': [{'pregunta': 'La célula básica de la sociedad andina fue:',
                 'alternativas': ['El tambo',
                                  'El ayllu',
                                  'La marka',
                                  'El curacazgo',
                                  'La panaca'],
                 'correcta': 'B'},
                {'pregunta': 'La ayuda mutua y recíproca entre familias se '
                             'denominaba:',
                 'alternativas': ['Camayoc',
                                  'Chunca',
                                  'Mita',
                                  'Ayni',
                                  'Minka'],
                 'correcta': 'D'},
                {'pregunta': 'El trabajo por turnos al servicio del Estado '
                             'inca se llamaba:',
                 'alternativas': ['Yanaconaje',
                                  'Minka',
                                  'Chaco',
                                  'Mita',
                                  'Ayni'],
                 'correcta': 'D'},
                {'pregunta': 'El trabajo comunal en beneficio del propio '
                             'ayllu se denominaba:',
                 'alternativas': ['Mita',
                                  'Faena estatal',
                                  'Tributo',
                                  'Minka',
                                  'Ayni'],
                 'correcta': 'D'},
                {'pregunta': 'La esposa principal del Inca recibía el nombre '
                             'de:',
                 'alternativas': ['Coya',
                                  'Aclla',
                                  'Palla',
                                  'Mamacona',
                                  'Ñusta'],
                 'correcta': 'A'},
                {'pregunta': 'El funcionario inspector llamado «el que todo '
                             'lo ve» fue:',
                 'alternativas': ['Quipucamayoc',
                                  'Curaca',
                                  'Amauta',
                                  'Apunchic',
                                  'Tucuyricuy'],
                 'correcta': 'E'},
                {'pregunta': 'El gobernador provincial en el Tahuantinsuyo '
                             'fue:',
                 'alternativas': ['Sinchi',
                                  'Curaca',
                                  'Willac Umu',
                                  'Apunchic',
                                  'Tucuyricuy'],
                 'correcta': 'D'},
                {'pregunta': '«Tahuantinsuyo» significa:',
                 'alternativas': ['Las cuatro regiones unidas',
                                  'El gran camino',
                                  'Tierra del Sol',
                                  'Casa del Inca',
                                  'Ombligo del mundo'],
                 'correcta': 'A'},
                {'pregunta': 'NO es una de las cuatro regiones del '
                             'Tahuantinsuyo:',
                 'alternativas': ['Collasuyo',
                                  'Chinchaysuyo',
                                  'Contisuyo',
                                  'Chimusuyo',
                                  'Antisuyo'],
                 'correcta': 'D'},
                {'pregunta': 'El principio por el cual el Estado repartía lo '
                             'acumulado se denomina:',
                 'alternativas': ['Redistribución',
                                  'Mita',
                                  'Ayni',
                                  'Reciprocidad',
                                  'Tributación'],
                 'correcta': 'A'},
                {'pregunta': 'Los depósitos estatales incas donde se '
                             'almacenaban productos se llamaban:',
                 'alternativas': ['Cancha',
                                  'Ushnu',
                                  'Collcas y tambos',
                                  'Kallanka',
                                  'Pucaras'],
                 'correcta': 'C'},
                {'pregunta': 'La tierra en el Tahuantinsuyo se dividía en '
                             'tierras del Sol, del Inca y:',
                 'alternativas': ['De los yanaconas',
                                  'Del pueblo o ayllu',
                                  'De los curacas',
                                  'Del ejército',
                                  'De los sacerdotes'],
                 'correcta': 'B'},
                {'pregunta': 'El recipiente cerámico de base cónica usado '
                             'para la chicha fue:',
                 'alternativas': ['El paccha',
                                  'El kero',
                                  'El huaco retrato',
                                  'El cántaro',
                                  'El aríbalo'],
                 'correcta': 'E'},
                {'pregunta': 'El tejido más fino de los incas se denominaba:',
                 'alternativas': ['Abasca',
                                  'Llicllia',
                                  'Unku',
                                  'Cumbi',
                                  'Chusi'],
                 'correcta': 'D'},
                {'pregunta': 'Los encargados de leer y elaborar los quipus '
                             'fueron los:',
                 'alternativas': ['Camayocs',
                                  'Amautas',
                                  'Haravicus',
                                  'Quipucamayocs',
                                  'Chasquis'],
                 'correcta': 'D'},
                {'pregunta': 'El templo principal del Cusco, dedicado al '
                             'Sol, fue:',
                 'alternativas': ['Ollantaytambo',
                                  'Tambomachay',
                                  'El Coricancha',
                                  'Sacsayhuamán',
                                  "Q'enqo"],
                 'correcta': 'C'},
                {'pregunta': 'La base de la economía inca fue:',
                 'alternativas': ['La ganadería exclusivamente',
                                  'El comercio',
                                  'La pesca',
                                  'La agricultura',
                                  'La minería'],
                 'correcta': 'D'},
                {'pregunta': 'Los andenes tuvieron como finalidad principal:',
                 'alternativas': ['Fines militares',
                                  'Ampliar y proteger la frontera agrícola',
                                  'Uso ceremonial',
                                  'Funciones funerarias',
                                  'Control astronómico'],
                 'correcta': 'B'},
                {'pregunta': 'La nobleza inca se dividía en nobleza de '
                             'sangre y nobleza de:',
                 'alternativas': ['Territorio',
                                  'Privilegio',
                                  'Comercio',
                                  'Guerra',
                                  'Religión'],
                 'correcta': 'B'},
                {'pregunta': 'El Consejo Imperial que asesoraba al Inca se '
                             'denominaba:',
                 'alternativas': ['Willac Umu',
                                  'Apunchic',
                                  'Panaca',
                                  'Tahuantinsuyo Camachic',
                                  'Curacazgo'],
                 'correcta': 'D'},
                {'pregunta': 'El jefe del ayllu, encargado de la '
                             'administración directa del territorio comunal, '
                             'era el:',
                 'alternativas': ['Apunchic',
                                  'Curaca',
                                  'Tucuyricuy',
                                  'Coya',
                                  'Quipucamayoc'],
                 'correcta': 'B'},
                {'pregunta': 'El funcionario inca conocido como «el que todo '
                             'lo ve», inspector en las provincias, era el:',
                 'alternativas': ['Curaca',
                                  'Tucuyricuy',
                                  'Apunchic',
                                  'Sinchi',
                                  'Villac Umu'],
                 'correcta': 'B'},
                {'pregunta': 'El Tahuantinsuyo, como institución '
                             'consolidada, fue obra principalmente del inca:',
                 'alternativas': ['Manco Cápac',
                                  'Pachacútec',
                                  'Huayna Cápac',
                                  'Túpac Yupanqui',
                                  'Huáscar'],
                 'correcta': 'B'},
                {'pregunta': 'Las mujeres escogidas, autorizadas '
                             'exclusivamente para tejer los ropajes del '
                             'Inca, se llamaban:',
                 'alternativas': ['Coyas',
                                  'Acllas',
                                  'Ñustas',
                                  'Pallas',
                                  'Mamaconas exclusivas'],
                 'correcta': 'B'},
                {'pregunta': 'Los depósitos estatales incas donde se '
                             'almacenaban productos del Tahuantinsuyo se '
                             'llamaban:',
                 'alternativas': ['Andenes',
                                  'Collcas y tambos',
                                  'Kanchas',
                                  'Ushnus',
                                  'Chullpas'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema por el cual un mismo ayllu '
                             'cultivaba tierras en distintas zonas '
                             'climáticas se llama:',
                 'alternativas': ['Reciprocidad',
                                  'Control de pisos ecológicos',
                                  'Redistribución',
                                  'Mitmaq exclusivo',
                                  'Ayni'],
                 'correcta': 'B'},
                {'pregunta': 'Los lupacas, pobladores del altiplano, '
                             'ejemplificaron el control de pisos ecológicos '
                             'al mantener tierras cultivadas también en:',
                 'alternativas': ['La selva',
                                  'La costa',
                                  'La sierra alta exclusivamente',
                                  'Otro país',
                                  'El desierto de Atacama'],
                 'correcta': 'B'},
                {'pregunta': 'Los andenes incas tuvieron como finalidad '
                             'principal:',
                 'alternativas': ['Solo la defensa militar',
                                  'Ampliar y proteger la frontera agrícola',
                                  'Solo el almacenamiento de agua',
                                  'Solo la vivienda',
                                  'Solo el culto religioso'],
                 'correcta': 'B'},
                {'pregunta': 'En la evolución histórica de los incas, el '
                             'periodo de la Confederación Cusqueña fue '
                             'gobernado entre otros por: (UNSAAC 2010)',
                 'alternativas': ['Huáscar y Manco Cápac',
                                  'Huayna Cápac y Atahualpa',
                                  'Pachacútec y Huayna Cápac',
                                  'Huayna Cápac y Sinchi Roca',
                                  'Yahuar Huacac y Huiracocha'],
                 'correcta': 'E'},
                {'pregunta': 'En la historia de la evolución incaica, en el '
                             'Periodo Legendario gobernaron: (UNSAAC 2010)',
                 'alternativas': ['Pachacútec y Huayna Cápac',
                                  'Manco Cápac y Sinchi Roca',
                                  'Lloque Yupanqui y Mayta Cápac',
                                  'Inca Roca y Yahuar Huacac',
                                  'Huiracocha y Cápac Yupanqui'],
                 'correcta': 'C'},
                {'pregunta': 'En la organización social inca, el Phiwichuri '
                             'era el: (UNSAAC 2011)',
                 'alternativas': ['Jefe militar',
                                  'Príncipe heredero',
                                  'Gobernador de provincias',
                                  'Hijo primogénito',
                                  'Jefe de ayllu'],
                 'correcta': 'E'},
                {'pregunta': 'En el Tahuantinsuyo, el organismo asesor del '
                             'inca lo constituía el: (UNSAAC 2011)',
                 'alternativas': ['Sinchi',
                                  'Consejo de suyos',
                                  'Auqui',
                                  'Apunchic',
                                  'Curaca'],
                 'correcta': 'B'},
                {'pregunta': 'En la organización económica inca, en las '
                             'tierras comunales se trabajaba a través del '
                             'sistema denominado: (UNSAAC 2011)',
                 'alternativas': ['Huaki', 'Minka', 'Ayni', 'Mita', 'Chunca'],
                 'correcta': 'C'},
                {'pregunta': 'El inca Pachacútec derrotó a los Chancas en el '
                             'periodo: (UNSAAC 2011)',
                 'alternativas': ['Imperial o de la Expansión',
                                  'Legendario, Curacal',
                                  'Regional o de la Confederación Cusqueña',
                                  'Localista',
                                  'De la decadencia'],
                 'correcta': 'A'},
                {'pregunta': 'El Qhapaq que institucionalizó el '
                             'Tahuantinsuyo fue: (UNSAAC 2013)',
                 'alternativas': ['Manco Cápac',
                                  'Inca Roca',
                                  'Wiracocha',
                                  'Wayna Cápac',
                                  'Pachacútec'],
                 'correcta': 'E'},
                {'pregunta': 'Los jefes de los pueblos incorporados al '
                             'Tahuantinsuyo constituyeron la nobleza: '
                             '(UNSAAC 2013)',
                 'alternativas': ['Regional',
                                  'Por privilegio',
                                  'De Sangre',
                                  'De Parentesco',
                                  'Provincial'],
                 'correcta': 'B'},
                {'pregunta': 'En el gobierno de las provincias, el que '
                             'representaba al Qhapaq como autoridad fue el: '
                             '(UNSAAC 2013)',
                 'alternativas': ['Auqui',
                                  'Tukuy Rikuc',
                                  'Apunchic',
                                  'Kuraka',
                                  'Sinchi'],
                 'correcta': 'C'},
                {'pregunta': 'En la evolución histórica de los incas, son '
                             'considerados sinchis los gobernantes: (UNSAAC '
                             '2013)',
                 'alternativas': ['Sinchi Roca - Inca Roca',
                                  'Pachacútec - Tupac Inca Yupanqui',
                                  'Lloque Yupanqui - Mayta Cápac',
                                  'Huáscar - Toparpa',
                                  'Sayri Tupac - Titu Cusi Yupanqui'],
                 'correcta': 'A'},
                {'pregunta': 'En la Guerra Civil, Huáscar y Atahualpa se '
                             'disputaron el trono de: (UNSAAC 2013)',
                 'alternativas': ['Tupac Inca Yupanqui',
                                  'Huayna Cápac',
                                  'Cápac Yupanqui',
                                  'Inca Yupanqui',
                                  'Pachacútec'],
                 'correcta': 'B'},
                {'pregunta': 'En el desarrollo del Tahuantinsuyo, los '
                             'pueblos que se trasladaban a lugares '
                             'despoblados eran mitimaes de: (UNSAAC 2013)',
                 'alternativas': ['Invasión',
                                  'Ocupación',
                                  'Conquista',
                                  'Colonización',
                                  'Castigo'],
                 'correcta': 'D'},
                {'pregunta': 'En la administración de la población del '
                             'Tahuantinsuyo, el Hunu Camayoc era el jefe de: '
                             '(UNSAAC 2013)',
                 'alternativas': ['10 000 familias',
                                  '1 000 familias',
                                  '100 familias',
                                  '10 familias',
                                  '1 familia'],
                 'correcta': 'D'},
                {'pregunta': 'El periodo regional de la historia de los '
                             'incas está marcado por: (UNSAAC 2013)',
                 'alternativas': ['La expansión territorial regional',
                                  'La confederación de ayllus quechuas',
                                  'El sometimiento de los Chancas',
                                  'El gobierno de curacas',
                                  'La conquista del oriente peruano'],
                 'correcta': 'C'},
                {'pregunta': 'En la sociedad Inca, los Yanáconas: (UNSAAC '
                             '2013)',
                 'alternativas': ['No tenían el derecho de ascender '
                                  'socialmente',
                                  'Eran personas encargadas de colonizar '
                                  'tierras',
                                  'Poblaron las zonas fronterizas del '
                                  'territorio',
                                  'Se trasladaban de un lugar a otro',
                                  'Representaban una forma de servidumbre'],
                 'correcta': 'A'},
                {'pregunta': 'La redistribución, como una forma económica de '
                             'los incas, consistía en: (UNSAAC 2013)',
                 'alternativas': ['La asignación de tareas por parte del '
                                  'Inca y sus funcionarios',
                                  'La ocupación constante de tierras '
                                  'dispersas y crianzas',
                                  'El disfrute de bienes según sus '
                                  'necesidades',
                                  'La repartición de alimentos excedentes en '
                                  'tiempos de crisis',
                                  'La circulación de bienes en el mercado '
                                  'regional'],
                 'correcta': 'D'},
                {'pregunta': 'Los gobernantes del Incario o Legendario '
                             'corresponden al periodo: (UNSAAC 2016)',
                 'alternativas': ['Manco Cápac y Huayna Cápac',
                                  'Manco Cápac y Lloque Yupanqui',
                                  'Manco Cápac y Mayta Cápac',
                                  'Manco Cápac y Sinchi Roca',
                                  'Manco Cápac y Yahuar Huacac'],
                 'correcta': 'D'},
                {'pregunta': 'Lloque Yupanqui y Mayta Cápac corresponden al '
                             'periodo: (UNSAAC 2016)',
                 'alternativas': ['De la resistencia de Vilcabamba',
                                  'Regional o de la Confederación cusqueña',
                                  'Legendario o de los comienzos del Incario',
                                  'De la expansión y el apogeo',
                                  'De la decadencia o crisis'],
                 'correcta': 'C'},
                {'pregunta': 'El Ayllu, que fue la unidad básica de la '
                             'organización Inca, surgió: (UNSAAC 2016)',
                 'alternativas': ['En el gobierno de Pachacútec',
                                  'Después de los Incas',
                                  'Antes de los Incas',
                                  'Durante el gobierno de los Incas',
                                  'En el periodo de los Chancas'],
                 'correcta': 'C'},
                {'pregunta': 'En la organización administrativa del Incario, '
                             'el Pisqa Chunca Camayoc era el jefe de: '
                             '(UNSAAC 2016)',
                 'alternativas': ['5 familias',
                                  '100 familias',
                                  '50 familias',
                                  '10 familias',
                                  '500 familias'],
                 'correcta': 'C'},
                {'pregunta': 'En el periodo de la confederación cusqueña o '
                             'quechua, los gobernantes se denominaron: '
                             '(UNSAAC 2016)',
                 'alternativas': ['Curacas',
                                  'Sinchis',
                                  'Phiwichuris',
                                  'Apunchic',
                                  'Auqui'],
                 'correcta': 'A'},
                {'pregunta': 'El príncipe heredero del trono en el incanato '
                             'se llamaba: (UNSAAC 2016)',
                 'alternativas': ['Tucuyricuy',
                                  'Apunchic',
                                  'Auqui',
                                  'Sinchi',
                                  'Qhapac'],
                 'correcta': 'C'},
                {'pregunta': 'Sacsayhuamán y Ollantaytambo corresponden '
                             'respectivamente a tipo de arquitectura: '
                             '(UNSAAC 2018)',
                 'alternativas': ['Religioso - Militar',
                                  'Militar - Religioso',
                                  'Militar - Civil',
                                  'Civil - Militar',
                                  'Civil - Religioso'],
                 'correcta': 'B'},
                {'pregunta': 'El Inca Pachacútec gobernó en el periodo '
                             'histórico: (UNSAAC 2018)',
                 'alternativas': ['Inicial',
                                  'Imperial',
                                  'Legendario',
                                  'Regional',
                                  'Curacal'],
                 'correcta': 'B'},
                {'pregunta': 'El gobernador de las provincias en la época '
                             'inca se denominaba: (UNSAAC 2018)',
                 'alternativas': ['Apunchic',
                                  'Curaca',
                                  'Auqui',
                                  'Sinchi',
                                  'Tucuyricuq'],
                 'correcta': 'A'},
                {'pregunta': 'El monumento arqueológico de Ollantaytambo fue '
                             'una construcción de tipo: (UNSAAC 2018)',
                 'alternativas': ['Recreacional',
                                  'Militar',
                                  'Civil',
                                  'Económico',
                                  'Religioso'],
                 'correcta': 'B'},
                {'pregunta': 'En la evolución histórica de los '
                             'Incas-quechuas, el periodo legendario de los '
                             'comienzos o curacal fue gobernado por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Lloque Yupanqui y Mayta Cápac',
                                  'Manco Cápac y Sinchi Roca',
                                  'Inca Roca y Wiracocha',
                                  'Pachacútec y Túpac Inca Yupanqui',
                                  'Cápac Yupanqui y Huayna Cápac'],
                 'correcta': 'B'},
                {'pregunta': 'El capital en la época incaica lo constituía: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['El almacenamiento de productos',
                                  'La producción de la tierra',
                                  'La técnica para deshidratar la papa',
                                  'La redistribución de los depósitos',
                                  'La fuerza humana de sus habitantes'],
                 'correcta': 'A'},
                {'pregunta': 'El inca que perteneció al periodo de la '
                             'Expansión y apogeo del Tahuantinsuyo es: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Sinchi Roca',
                                  'Mayta Cápac',
                                  'Tupac Inca Yupanqui',
                                  'Wiracocha',
                                  'Inca Roca'],
                 'correcta': 'C'},
                {'pregunta': 'El proceso histórico Inca, en el periodo de la '
                             'decadencia, se caracterizó por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['La guerra civil entre los hermanos '
                                  'Huáscar y Atahualpa',
                                  'La resistencia de los incas desde '
                                  'Vilcabamba',
                                  'El ataque de los Chancas al Cusco',
                                  'La muerte de Huayna Cápac y Ninan Cuyuchi '
                                  'en el Ecuador',
                                  'La fundación de Qosqo con Manco Cápac y '
                                  'Mama Ocllo'],
                 'correcta': 'A'},
                {'pregunta': 'Wiracocha gobernó en el periodo: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['De resistencia y supervivencia',
                                  'Legendario o de los inicios',
                                  'Imperial o de la expansión política',
                                  'Regional o de la confederación quechua',
                                  'Decadente o de la descomposición'],
                 'correcta': 'D'},
                {'pregunta': 'El reconocimiento de un antepasado común por '
                             'los miembros del ayllu inca se refiere al '
                             'vínculo por: (UNSAAC Ordinario)',
                 'alternativas': ['Parentesco',
                                  'Tótem',
                                  'Territorio',
                                  'Origen',
                                  'Religión'],
                 'correcta': 'A'},
                {'pregunta': 'Uno de los incas de la resistencia, refugiado '
                             'en Vilcabamba, que finalmente reconoció al Rey '
                             'de España fue: (UNSAAC Ordinario)',
                 'alternativas': ['Huáscar',
                                  'Tupac Amaru I',
                                  'Manco Inca',
                                  'Sayri Tupac',
                                  'Huayna Cápac'],
                 'correcta': 'D'},
                {'pregunta': 'El periodo de la resistencia andina de '
                             'Vilcabamba culminó con la muerte de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['José Gabriel Tupac Amaru',
                                  'Fernando Tupac Amaru',
                                  'Felipe Tupac Amaru',
                                  'Sayri Tupac',
                                  'Titu Cusi Yupanqui'],
                 'correcta': 'C'},
                {'pregunta': 'En el proceso histórico de los incas, Titu '
                             'Cusi Yupanqui gobernó el periodo: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Imperial o de la expansión',
                                  'De resistencia de Vilcabamba',
                                  'Legendario o de los orígenes',
                                  'Decadente o crítico',
                                  'Regional o de la Confederación Cusqueña'],
                 'correcta': 'B'},
                {'pregunta': 'En el incanato, el gobernante de las '
                             'provincias encargado de mantener el orden en '
                             'el interior del territorio fue el: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Inca',
                                  'Curaca',
                                  'Apunchik',
                                  'Consejo de Suyos',
                                  'Cacique'],
                 'correcta': 'C'},
                {'pregunta': 'El futuro gobernante del Tahuantinsuyo fue '
                             'conocido como: (UNSAAC Ordinario)',
                 'alternativas': ['Auqui',
                                  'Phiwichuri',
                                  'Apuskipa',
                                  'Tucuy Ricuj',
                                  'Kipukamayoc'],
                 'correcta': 'A'},
                {'pregunta': 'El Ayni, como sistema de trabajo en el '
                             'Tahuantinsuyo, consistía en: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['El trabajo obligatorio para la '
                                  'construcción de obras públicas',
                                  'La prestación de servicios en forma '
                                  'recíproca entre las personas de un Ayllu',
                                  'La forma de trabajo de una comunidad en '
                                  'las tierras del Inca',
                                  'El trabajo obligatorio para la '
                                  'explotación de recursos',
                                  'El trabajo gratuito en las tierras del '
                                  'curaca'],
                 'correcta': 'B'},
                {'pregunta': 'La derrota de los Chancas, en la batalla de '
                             'Yawarpampa, corresponde al periodo: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Legendario',
                                  'De la confederación quechua',
                                  'De la resistencia',
                                  'De la Decadencia',
                                  'De la expansión y Apogeo'],
                 'correcta': 'E'},
                {'pregunta': 'En la resistencia de Manco Inca, el capitán '
                             'que se inmoló antes de caer en manos españolas '
                             'fue: (UNSAAC Ordinario)',
                 'alternativas': ['Titu Yupanki',
                                  'Tupac Huallpa',
                                  'Suruhuamán',
                                  'Calcuchimac',
                                  'Quisquis'],
                 'correcta': 'C'},
                {'pregunta': 'En el Tahuantinsuyo, la unidad de medida de '
                             'las tierras comunales del ayllu se denominaba: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Mita',
                                  'Chala',
                                  'Trueque',
                                  'Marca',
                                  'Topo'],
                 'correcta': 'E'},
                {'pregunta': 'En el Ayllu, reconocían una Pacarina común, '
                             'como vínculo: (UNSAAC Ordinario)',
                 'alternativas': ['Territorio',
                                  'Origen',
                                  'Parentesco',
                                  'Tótem',
                                  'Idioma'],
                 'correcta': 'B'},
                {'pregunta': 'En el Tahuantinsuyo, los ciudadanos obligados '
                             'a tributar fueron los: (UNSAAC Ordinario)',
                 'alternativas': ['Hatun Runas',
                                  'Chasquis',
                                  'Mitmacunas',
                                  'Orejones',
                                  'Curacas'],
                 'correcta': 'A'},
                {'pregunta': 'Para tener un mejor control de la población en '
                             'términos de cumplimiento de la Mita en el '
                             'Tahuantinsuyo, la división de 5000 familias '
                             'estaba controlado por: (UNSAAC Ordinario)',
                 'alternativas': ['Pisca Pachac Camayoc',
                                  'Pisca Camayoc',
                                  'Pisca Chunca Camayoc',
                                  'Pisca Huaranca Camayoc',
                                  'Pisca Pachac Camayoc'],
                 'correcta': 'D'},
                {'pregunta': 'El Ayllu fue la unidad esencial y básica de la '
                             'organización social inca, teniendo como '
                             'responsable al: (UNSAAC Ordinario)',
                 'alternativas': ['Curaca',
                                  'Sinchi',
                                  'Apunchic',
                                  'Tucuy Ricuc',
                                  'Auqui'],
                 'correcta': 'A'},
                {'pregunta': 'El urpu o aríbalo es la manifestación '
                             'ceramística más representativa de la Cultura: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Chimú',
                                  'Inca',
                                  'Wari',
                                  'Mochica',
                                  'Chavín'],
                 'correcta': 'B'},
                {'pregunta': 'En la Organización Política Inca, el Apunchic '
                             'representó: (UNSAAC Ordinario)',
                 'alternativas': ['A la máxima autoridad del Inca',
                                  'A los cuatro jefes de suyos',
                                  'Al gobernador de las provincias',
                                  'A funcionarios incógnitos',
                                  'Al príncipe heredero'],
                 'correcta': 'C'},
                {'pregunta': 'En la evolución histórica de los incas, el '
                             'periodo Legendario fue gobernado por: (II '
                             'CEPRU 2011)',
                 'alternativas': ['Huáscar - Atahuallpa',
                                  'Lloque Yupanki - Mayta Capac',
                                  'Inca Roca - Wiracocha',
                                  'Manco Cápac - Sinchi Roca',
                                  'Pachacútec - Tupac Inca Yupanki'],
                 'correcta': 'D'},
                {'pregunta': 'En la organización Social Inca, la nobleza de '
                             'sangre estuvo integrada por: (II CEPRU 2011)',
                 'alternativas': ['Los Hatunrunas o miembros del Ayllu',
                                  'Jefes incorporados de pueblos vencidos',
                                  'Los yanaconas o servidores domésticos',
                                  'Los mitimaes o pueblos trasladados',
                                  'Ascendientes del inca y la coya'],
                 'correcta': 'E'},
                {'pregunta': 'Las características más importantes de la '
                             'arquitectura inca fueron: (II CEPRU 2011)',
                 'alternativas': ['Administrativa - militar - polícroma',
                                  'Simetría - ciclópea - asimétrica',
                                  'Sencillez - funcional - administrativa',
                                  'Solidez - sencillez - simetría',
                                  'Solidez - almohadillado - funcional'],
                 'correcta': 'D'},
                {'pregunta': 'En el Ayllu, las relaciones de parentesco se '
                             'establecían a través del vínculo de: (II CEPRU '
                             '2012)',
                 'alternativas': ['Territorio',
                                  'Tótem',
                                  'Sangre',
                                  'Economía',
                                  'Marka'],
                 'correcta': 'C'},
                {'pregunta': 'En la época inca, el capital lo constituía: '
                             '(II CEPRU 2012)',
                 'alternativas': ['El comercio',
                                  'La fuerza humana',
                                  'La distribución',
                                  'El consumo',
                                  'La circulación'],
                 'correcta': 'B'},
                {'pregunta': 'Los jefes de los pueblos incorporados al '
                             'Tahuantinsuyo, pasaron a conformar la: (I '
                             'CEPRU 2014)',
                 'alternativas': ['Nobleza de privilegio',
                                  'Nobleza regional',
                                  'Clase de los militares',
                                  'Clase de pueblo',
                                  'Nobleza de sangre'],
                 'correcta': 'A'},
                {'pregunta': 'En la economía inca, la redistribución '
                             'significó: (I CEPRU 2014)',
                 'alternativas': ['El intercambio de productos por otros '
                                  'productos',
                                  'La repartición anual de tierras por parte '
                                  'de la coya',
                                  'La asignación de labores agrícolas por '
                                  'parte del inca',
                                  'La repartición de alimentos excedentes en '
                                  'épocas de crisis',
                                  'El disfrute, según las necesidades de '
                                  'cada uno'],
                 'correcta': 'D'},
                {'pregunta': 'La Leyenda de la fundación del Cusco por Manco '
                             'Cápac y Mama Ocllo, pertenece a la fuente: (I '
                             'CEPRU 2014)',
                 'alternativas': ['Oral',
                                  'Documental',
                                  'Escrita',
                                  'Material',
                                  'Antroposomática'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'EL AYLLU',
                      'items': ['Fue la célula básica de la sociedad andina: '
                                'un conjunto de familias unidas por vínculos '
                                'de parentesco, territorio y culto a un '
                                'ancestro común.',
                                'Sus formas de trabajo colectivo fueron el '
                                'ayni (ayuda mutua y recíproca entre '
                                'familias), la minka (trabajo comunal en '
                                'beneficio del ayllu) y la mita (trabajo por '
                                'turnos al servicio del Estado).']},
                     {'titulo': 'Y 7.3 LO SOCIAL Y LO POLÍTICO',
                      'items': ['La sociedad inca fue clasista. La nobleza '
                                'se dividía en nobleza de sangre y nobleza '
                                'de privilegio.',
                                'El Inca era la máxima autoridad; su esposa '
                                'principal era la Coya.',
                                'El Consejo Imperial o Tahuantinsuyo '
                                'Camachic asesoraba al Inca. El Apunchic era '
                                'gobernador provincial y el Tucuyricuy el '
                                '«que todo lo ve», inspector del imperio.',
                                'El imperio se llamó Tahuantinsuyo, «las '
                                'cuatro regiones unidas»: Chinchaysuyo, '
                                'Antisuyo, Collasuyo y Contisuyo.']},
                     {'titulo': 'ADMINISTRACIÓN Y CONTROL DE PISOS '
                                'ECOLÓGICOS',
                      'items': ['El curaca era el jefe del ayllu, encargado '
                                'de la administración directa del territorio '
                                'comunal.',
                                'El Tucuyricuy, «el que todo lo ve», actuaba '
                                'como inspector del Inca en las provincias.',
                                'El Tahuantinsuyo, como institución '
                                'consolidada, fue obra del inca Pachacútec.',
                                'Solo las acllas, mujeres escogidas, estaban '
                                'autorizadas para tejer los ropajes '
                                'destinados al Inca.',
                                'Los collcas y tambos eran los depósitos '
                                'estatales donde se almacenaban productos '
                                'del Tahuantinsuyo.',
                                'El control de pisos ecológicos consistía en '
                                'que un mismo ayllu cultivara tierras en '
                                'distintas zonas climáticas, como hicieron '
                                'los lupacas del altiplano con tierras en la '
                                'costa.',
                                'Los andenes tuvieron como finalidad ampliar '
                                'y proteger la frontera agrícola.']},
                     {'titulo': 'LO ECONÓMICO',
                      'items': ['La base económica fue la agricultura, '
                                'apoyada en los andenes y en obras de '
                                'irrigación.',
                                'Principios que la rigieron: la reciprocidad '
                                '(intercambio de trabajo y favores) y la '
                                'redistribución (el Estado repartía lo '
                                'acumulado en los tambos y collcas).',
                                'La propiedad de la tierra se dividía en '
                                'tierras del Sol, del Inca y del pueblo o '
                                'ayllu.']},
                     {'titulo': 'EXPRESIONES ARTÍSTICAS',
                      'items': ['Arquitectura: sólida, sencilla y simétrica. '
                                'Destacan Machupicchu, Sacsayhuamán y el '
                                'Coricancha.',
                                'Cerámica: destaca el aríbalo, de base '
                                'cónica, usado para transportar chicha.',
                                'Textilería: los tejidos finos se llamaban '
                                'cumbi y los toscos abasca.',
                                'El registro de información se hacía '
                                'mediante los quipus, a cargo de los '
                                'quipucamayocs.']}],
  'qr_reto': [{'pregunta': 'Los jefes de los pueblos incorporados al '
                           'Tahuantinsuyo constituyeron la nobleza:',
               'respuesta': 'Por privilegio'},
              {'pregunta': 'En el proceso histórico de los incas, Titu Cusi '
                           'Yupanqui gobernó el periodo:',
               'respuesta': 'De resistencia de Vilcabamba'},
              {'pregunta': 'Lloque Yupanqui y Mayta Cápac corresponden al '
                           'periodo:',
               'respuesta': 'Legendario o de los comienzos del Incario'}],
  'qr_dato': 'El registro de información se hacía mediante los quipus, a '
             'cargo de los quipucamayocs.'},
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
                {'titulo': '8.5 EL SURGIMIENTO DE LA BURGUESÍA',
                 'items': ['El origen de la burguesía se remonta al siglo '
                           '{XII}, con villanos o campesinos libres que '
                           'residían en los {burgos} o ciudades.',
                           'La actividad comercial burguesa no era bien '
                           'vista por la {Iglesia}, por su fin de lucro.',
                           'Los burgueses enriquecidos obtuvieron de los '
                           'señores feudales permisos de autogobierno, '
                           'escritos en las llamadas «{cartas de '
                           'franquicia}».']},
                {'titulo': '8.6 EL CAPITALISMO MERCANTIL',
                 'items': ['El capitalismo mercantil se basaba en la premisa '
                           'de que la riqueza de una nación aumentaba '
                           'exportando más y recibiendo {metales preciosos}.',
                           'Bajo este sistema, el {Estado} ejerció mucho '
                           'control sobre la vida económica, compañías y '
                           'colonias.',
                           'El capitalismo mercantil impulsó los viajes de '
                           '{descubrimiento} e invasión de las metrópolis '
                           'europeas sobre América y África.']},
                {'titulo': '8.7 EL RENACIMIENTO: REPRESENTANTES',
                 'items': ['El Renacimiento sustituyó la concepción '
                           '{teocentrista} medieval por el '
                           '{antropocentrismo}.',
                           'La huida de eruditos bizantinos a Occidente se '
                           'debió a la captura de {Constantinopla} por los '
                           'turcos, en {1453}.',
                           '{Nicolás Maquiavelo}, considerado padre de la '
                           'ciencia política, escribió «El Príncipe».',
                           '{Tomás Moro}, autor de «Utopía», idealizó una '
                           'república con propiedad común de los bienes.',
                           '{Leonardo Da Vinci} destacó por sus pinturas La '
                           'Última Cena y la Gioconda, y el dibujo El Hombre '
                           'de {Vitruvio}.',
                           '{Miguel Ángel} destacó por la escultura de '
                           'David, Moisés y la Piedad.']}],
  'cuadros': [{'titulo': '8. SOCIEDAD FEUDAL',
               'encabezados': ['Estamento', 'Función'],
               'filas': [['{Nobleza}', 'Guerrear y {proteger}'],
                         ['{Clero}', 'Orar y administrar lo {religioso}'],
                         ['{Siervos} y campesinos',
                          '{Trabajar} la tierra']]}],
  'preguntas': [{'pregunta': 'El feudalismo predominó en Europa entre los '
                             'siglos:',
                 'alternativas': ['XVI y XVIII',
                                  'XV y XVIII',
                                  'III y VI',
                                  'IX y XV',
                                  'V y VIII'],
                 'correcta': 'D'},
                {'pregunta': 'La base fundamental del sistema feudal fue:',
                 'alternativas': ['La industria textil',
                                  'La posesión de la tierra',
                                  'La banca',
                                  'La minería',
                                  'El comercio marítimo'],
                 'correcta': 'B'},
                {'pregunta': 'El feudalismo surgió principalmente tras:',
                 'alternativas': ['El descubrimiento de América',
                                  'La peste negra',
                                  'Las Cruzadas',
                                  'La Revolución Francesa',
                                  'La caída del Imperio Romano de Occidente '
                                  'y las invasiones bárbaras'],
                 'correcta': 'E'},
                {'pregunta': 'La economía feudal se caracterizó por ser:',
                 'alternativas': ['Financiera',
                                  'Industrial y urbana',
                                  'Rural y autosuficiente',
                                  'Comercial y monetaria',
                                  'Colonial'],
                 'correcta': 'C'},
                {'pregunta': 'El campesino adscrito a la tierra, que no '
                             'podía abandonarla, era el:',
                 'alternativas': ['Artesano',
                                  'Vasallo',
                                  'Burgués',
                                  'Siervo de la gleba',
                                  'Caballero'],
                 'correcta': 'D'},
                {'pregunta': 'El acto por el cual el vasallo juraba '
                             'fidelidad al señor se llamaba:',
                 'alternativas': ['Tributo',
                                  'Homenaje',
                                  'Censo',
                                  'Diezmo',
                                  'Investidura'],
                 'correcta': 'B'},
                {'pregunta': 'La extensión de tierra entregada a cambio de '
                             'servicios se denominaba:',
                 'alternativas': ['Burgo',
                                  'Solar',
                                  'Villa',
                                  'Manso',
                                  'Feudo'],
                 'correcta': 'E'},
                {'pregunta': 'El poder político durante el feudalismo se '
                             'caracterizó por estar:',
                 'alternativas': ['Concentrado en las ciudades',
                                  'Fragmentado o descentralizado',
                                  'Centralizado',
                                  'En manos del pueblo',
                                  'Bajo control imperial único'],
                 'correcta': 'B'},
                {'pregunta': 'La nueva clase social surgida con el renacer '
                             'del comercio y las ciudades fue:',
                 'alternativas': ['Los caballeros',
                                  'La burguesía',
                                  'La nobleza',
                                  'El clero',
                                  'Los siervos'],
                 'correcta': 'B'},
                {'pregunta': 'La sociedad feudal se caracterizó por ser:',
                 'alternativas': ['Igualitaria',
                                  'De alta movilidad social',
                                  'Estamental y rígida',
                                  'Sin clases',
                                  'Democrática'],
                 'correcta': 'C'},
                {'pregunta': 'El movimiento cultural que recuperó la cultura '
                             'grecolatina fue:',
                 'alternativas': ['El Barroco',
                                  'El Romanticismo',
                                  'El Renacimiento',
                                  'La Ilustración',
                                  'La Escolástica'],
                 'correcta': 'C'},
                {'pregunta': 'La corriente que colocó al ser humano en el '
                             'centro del pensamiento fue:',
                 'alternativas': ['El escolasticismo',
                                  'El positivismo',
                                  'El empirismo',
                                  'El teocentrismo',
                                  'El humanismo'],
                 'correcta': 'E'},
                {'pregunta': 'El capitalismo mercantil se basó '
                             'principalmente en:',
                 'alternativas': ['El trueque',
                                  'La servidumbre',
                                  'La agricultura de subsistencia',
                                  'El comercio, la banca y la acumulación de '
                                  'capital',
                                  'La producción artesanal doméstica'],
                 'correcta': 'D'},
                {'pregunta': 'La función social de la nobleza feudal era:',
                 'alternativas': ['Comerciar',
                                  'Trabajar la tierra',
                                  'Orar',
                                  'Guerrear y proteger',
                                  'Administrar justicia eclesiástica'],
                 'correcta': 'D'},
                {'pregunta': 'La función social del clero en la sociedad '
                             'feudal era:',
                 'alternativas': ['Gobernar el feudo',
                                  'Trabajar la tierra',
                                  'Recaudar impuestos',
                                  'Guerrear',
                                  'Orar y administrar lo religioso'],
                 'correcta': 'E'},
                {'pregunta': 'El señor feudal otorgaba a sus vasallos '
                             'principalmente:',
                 'alternativas': ['Títulos nobiliarios exclusivamente',
                                  'Educación',
                                  'Protección y tierras',
                                  'Naves comerciales',
                                  'Dinero'],
                 'correcta': 'C'},
                {'pregunta': 'Las parcelas del feudo trabajadas por los '
                             'campesinos se llamaban:',
                 'alternativas': ['Villas',
                                  'Mansos',
                                  'Reserva señorial',
                                  'Burgos',
                                  'Ejidos'],
                 'correcta': 'B'},
                {'pregunta': 'El feudalismo fue un sistema:',
                 'alternativas': ['Únicamente militar',
                                  'Solo económico',
                                  'Exclusivamente religioso',
                                  'Político, económico y social',
                                  'Solo jurídico'],
                 'correcta': 'D'},
                {'pregunta': 'La burguesía estuvo formada principalmente '
                             'por:',
                 'alternativas': ['Clero regular',
                                  'Comerciantes y artesanos',
                                  'Siervos de la gleba',
                                  'Militares',
                                  'Nobles y caballeros'],
                 'correcta': 'B'},
                {'pregunta': 'El renacer de las ciudades en la Baja Edad '
                             'Media se relaciona directamente con:',
                 'alternativas': ['El aislamiento de los feudos',
                                  'Las invasiones bárbaras',
                                  'La reactivación del comercio',
                                  'La expansión de la servidumbre',
                                  'El fin del comercio'],
                 'correcta': 'C'},
                {'pregunta': 'El origen de la burguesía se remonta al siglo '
                             'XII, con villanos que residían en:',
                 'alternativas': ['Los feudos',
                                  'Los burgos o ciudades',
                                  'Los monasterios',
                                  'Los castillos',
                                  'Las cortes reales'],
                 'correcta': 'B'},
                {'pregunta': 'La actividad comercial de los burgueses no era '
                             'bien vista por:',
                 'alternativas': ['Los reyes',
                                  'La Iglesia',
                                  'Los artesanos',
                                  'Los campesinos',
                                  'Los mercaderes'],
                 'correcta': 'B'},
                {'pregunta': 'Los permisos de autogobierno que obtenían los '
                             'burgueses se escribían en documentos llamados:',
                 'alternativas': ['Bulas papales',
                                  'Cartas de franquicia',
                                  'Tratados de paz',
                                  'Códigos civiles',
                                  'Decretos reales'],
                 'correcta': 'B'},
                {'pregunta': 'El capitalismo mercantil se basaba en la '
                             'premisa de que la riqueza de una nación '
                             'aumentaba al exportar más y recibir:',
                 'alternativas': ['Esclavos',
                                  'Metales preciosos',
                                  'Tierras',
                                  'Alimentos exclusivamente',
                                  'Armas'],
                 'correcta': 'B'},
                {'pregunta': 'Bajo el capitalismo mercantil, el control '
                             'sobre la vida económica lo ejercía '
                             'principalmente:',
                 'alternativas': ['La Iglesia',
                                  'El Estado',
                                  'Los gremios exclusivamente',
                                  'Los burgueses exclusivamente',
                                  'Los campesinos'],
                 'correcta': 'B'},
                {'pregunta': 'El capitalismo mercantil impulsó los viajes de '
                             'descubrimiento e invasión sobre América y:',
                 'alternativas': ['Oceanía',
                                  'África',
                                  'La Antártida',
                                  'El Ártico',
                                  'Ninguna otra región'],
                 'correcta': 'B'},
                {'pregunta': 'El Renacimiento sustituyó la concepción '
                             'teocentrista medieval por:',
                 'alternativas': ['El feudalismo',
                                  'El antropocentrismo',
                                  'El mercantilismo',
                                  'El absolutismo',
                                  'El escolasticismo'],
                 'correcta': 'B'},
                {'pregunta': 'La huida de eruditos bizantinos a Occidente se '
                             'debió a la captura de Constantinopla por los '
                             'turcos en:',
                 'alternativas': ['1453', '1492', '1517', '1400', '1600'],
                 'correcta': 'A'},
                {'pregunta': 'El autor de «El Príncipe», considerado padre '
                             'de la ciencia política, fue:',
                 'alternativas': ['Tomás Moro',
                                  'Nicolás Maquiavelo',
                                  'Leonardo Da Vinci',
                                  'Miguel Ángel',
                                  'Botticelli'],
                 'correcta': 'B'},
                {'pregunta': 'El autor de «Utopía», que idealizó una '
                             'república con propiedad común de los bienes, '
                             'fue:',
                 'alternativas': ['Maquiavelo',
                                  'Tomás Moro',
                                  'Da Vinci',
                                  'Botticelli',
                                  'Miguel Ángel'],
                 'correcta': 'B'},
                {'pregunta': 'Leonardo Da Vinci destacó por pinturas como la '
                             'Gioconda y el dibujo:',
                 'alternativas': ['El Nacimiento de Venus',
                                  'El Hombre de Vitruvio',
                                  'La Piedad',
                                  'El Juicio Final',
                                  'David'],
                 'correcta': 'B'},
                {'pregunta': 'Miguel Ángel destacó por esculturas como '
                             'David, Moisés y:',
                 'alternativas': ['El Hombre de Vitruvio',
                                  'La Piedad',
                                  'La Gioconda',
                                  'La Primavera',
                                  'El Nacimiento de Venus'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema económico, social y político de la '
                             'Edad Media, basado en la gran propiedad '
                             'territorial, tuvo como elementos básicos al: '
                             '(UNSAAC 2013)',
                 'alternativas': ['Propietario, trabajador y parcela',
                                  'Terrateniente, esclavo y beneficio',
                                  'Hacendado, siervo y latifundio',
                                  'Latifundista, colono y hacienda',
                                  'Señor feudal, vasallo y feudo'],
                 'correcta': 'E'},
                {'pregunta': 'La burguesía, como una nueva clase social en '
                             'el mundo, surgió en la Europa: (UNSAAC 2013)',
                 'alternativas': ['Contemporánea industrial',
                                  'Medieval Media',
                                  'Medieval Tardía',
                                  'Medieval Temprana',
                                  'Moderna comercial'],
                 'correcta': 'B'},
                {'pregunta': 'Los elementos del feudalismo son: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Señor Feudal - Feudo - Siervo',
                                  'Feudo - Hacienda - Villanos',
                                  'Señor Feudal - Siervos - Repartimientos',
                                  'Burgos - Villanos - Hacendados',
                                  'Encomienda - Siervos - Latifundios'],
                 'correcta': 'A'},
                {'pregunta': 'La nueva clase social que surgió en Europa en '
                             'el Siglo XII fue de los: (UNSAAC Ordinario)',
                 'alternativas': ['Esclavos',
                                  'Siervos',
                                  'Nobles',
                                  'Señores',
                                  'Burgueses'],
                 'correcta': 'E'},
                {'pregunta': 'Uno de los elementos característicos del '
                             'feudalismo fue: (UNSAAC Ordinario)',
                 'alternativas': ['El ateísmo',
                                  'La industria',
                                  'La democracia',
                                  'La tierra',
                                  'La medicina'],
                 'correcta': 'D'},
                {'pregunta': 'Los miembros de la burguesía medieval tenían '
                             'como principal actividad: (UNSAAC Ordinario)',
                 'alternativas': ['La ganadería',
                                  'La agricultura',
                                  'La minería',
                                  'El comercio',
                                  'La política'],
                 'correcta': 'D'},
                {'pregunta': 'El acto por el cual un vasallo adquiría '
                             'derechos sobre el feudo se llamaba: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Inquisición',
                                  'Vestidura',
                                  'Vasallaje - Investidura',
                                  'Franquicia',
                                  'Sumisión'],
                 'correcta': 'C'},
                {'pregunta': 'En el medioevo medio, el sistema que tuvo '
                             'origen en el declive romano se denomina: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Burguesía',
                                  'Capitalismo',
                                  'Primitivismo',
                                  'Feudalismo',
                                  'Socialismo'],
                 'correcta': 'D'},
                {'pregunta': 'La base principal del sistema feudal fue: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['La tierra',
                                  'El dinero',
                                  'El siervo',
                                  'El esclavo',
                                  'El comercio'],
                 'correcta': 'A'},
                {'pregunta': 'La autorización o concesión que otorgaba el '
                             'rey a los burgueses para su autogobierno, se '
                             'denomina: (UNSAAC Ordinario)',
                 'alternativas': ['Carta de Franquicia',
                                  'Reforma jurídica',
                                  'Bula alejandrina',
                                  'Concordato',
                                  'Regio patronato'],
                 'correcta': 'A'},
                {'pregunta': 'En el medioevo, surgió una nueva clase social '
                             'dedicada a la actividad de comercio en las '
                             'ciudades, denominadas: (II CEPRU 2012)',
                 'alternativas': ['Burguesía',
                                  'Villanos',
                                  'Siervos',
                                  'Proletario',
                                  'Clase media'],
                 'correcta': 'A'},
                {'pregunta': 'El feudalismo, fue un sistema económico, '
                             'social y político que rigió durante la edad: '
                             '(I CEPRU 2014)',
                 'alternativas': ['Antigua',
                                  'Contemporánea',
                                  'Media',
                                  'Moderna',
                                  'Primitiva'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'EL FEUDALISMO: CONCEPTO',
                      'items': ['Sistema político, económico y social que '
                                'predominó en Europa entre los siglos IX y '
                                'XV.',
                                'Se basó en la posesión de la tierra y en '
                                'relaciones personales de dependencia entre '
                                'señores y vasallos.']},
                     {'titulo': 'Y 8.3 ANTECEDENTES Y CARACTERÍSTICAS',
                      'items': ['Surgió tras la caída del Imperio Romano de '
                                'Occidente y las invasiones bárbaras, que '
                                'obligaron a buscar protección.',
                                'Economía rural y autosuficiente: el feudo '
                                'producía casi todo lo que consumía.',
                                'Sociedad estamental y rígida, con escasa '
                                'movilidad social.',
                                'El poder político quedó fragmentado o '
                                'descentralizado entre los señores '
                                'feudales.']},
                     {'titulo': 'ELEMENTOS DEL FEUDALISMO',
                      'items': ['El señor feudal: propietario del feudo, '
                                'otorgaba protección y tierras.',
                                'Los vasallos: prestaban fidelidad y '
                                'servicio militar mediante el homenaje.',
                                'El feudo: extensión de tierra entregada a '
                                'cambio de servicios; comprendía la reserva '
                                'señorial y los mansos.',
                                'Los siervos de la gleba estaban adscritos a '
                                'la tierra y no podían abandonarla.']},
                     {'titulo': 'EL SURGIMIENTO DE LA BURGUESÍA',
                      'items': ['El origen de la burguesía se remonta al '
                                'siglo XII, con villanos o campesinos libres '
                                'que residían en los burgos o ciudades.',
                                'La actividad comercial burguesa no era bien '
                                'vista por la Iglesia, por su fin de lucro.',
                                'Los burgueses enriquecidos obtuvieron de '
                                'los señores feudales permisos de '
                                'autogobierno, escritos en las llamadas '
                                '«cartas de franquicia».']},
                     {'titulo': 'EL CAPITALISMO MERCANTIL',
                      'items': ['El capitalismo mercantil se basaba en la '
                                'premisa de que la riqueza de una nación '
                                'aumentaba exportando más y recibiendo '
                                'metales preciosos.',
                                'Bajo este sistema, el Estado ejerció mucho '
                                'control sobre la vida económica, compañías '
                                'y colonias.',
                                'El capitalismo mercantil impulsó los viajes '
                                'de descubrimiento e invasión de las '
                                'metrópolis europeas sobre América y '
                                'África.']},
                     {'titulo': 'EL RENACIMIENTO: REPRESENTANTES',
                      'items': ['El Renacimiento sustituyó la concepción '
                                'teocentrista medieval por el '
                                'antropocentrismo.',
                                'La huida de eruditos bizantinos a Occidente '
                                'se debió a la captura de Constantinopla por '
                                'los turcos, en 1453.',
                                'Nicolás Maquiavelo, considerado padre de la '
                                'ciencia política, escribió «El Príncipe».',
                                'Tomás Moro, autor de «Utopía», idealizó una '
                                'república con propiedad común de los '
                                'bienes.',
                                'Leonardo Da Vinci destacó por sus pinturas '
                                'La Última Cena y la Gioconda, y el dibujo '
                                'El Hombre de Vitruvio.',
                                'Miguel Ángel destacó por la escultura de '
                                'David, Moisés y la Piedad.']}],
  'qr_reto': [{'pregunta': 'El movimiento cultural que recuperó la cultura '
                           'grecolatina fue:',
               'respuesta': 'El Renacimiento'},
              {'pregunta': 'La nueva clase social surgida con el renacer del '
                           'comercio y las ciudades fue:',
               'respuesta': 'La burguesía'},
              {'pregunta': 'El origen de la burguesía se remonta al siglo '
                           'XII, con villanos que residían en:',
               'respuesta': 'Los burgos o ciudades'}],
  'qr_dato': 'Se basó en la posesión de la tierra y en relaciones personales '
             'de dependencia entre señores y vasallos.'},
 {'num': 9,
  'titulo': 'Expansión europea',
  'secciones': [{'titulo': '9.1 DESCUBRIMIENTOS GEOGRÁFICOS',
                 'items': ['Causas: la búsqueda de una nueva ruta hacia las '
                           '{Indias} tras la caída de {Constantinopla} en '
                           '{1453} a manos de los turcos.',
                           'Avances técnicos que lo hicieron posible: la '
                           '{brújula}, el {astrolabio} y la carabela.',
                           '{Portugal} y {España} encabezaron la expansión '
                           'ultramarina.',
                           'Los navegantes portugueses llegaron a las Indias '
                           'bordeando África: {Vasco de Gama} en {1499}.']},
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
                           'América {Central}.',
                           'El nombre «{América}» proviene del navegante '
                           'italiano {Américo Vespucio}, quien reconoció que '
                           'se trataba de un nuevo continente.']}],
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
                 'alternativas': ['1498', '1492', '1532', '1521', '1453'],
                 'correcta': 'E'},
                {'pregunta': 'El documento que fijó los títulos y beneficios '
                             'de Colón fue:',
                 'alternativas': ['La Capitulación de Santa Fe',
                                  'El Tratado de Tordesillas',
                                  'Las Leyes de Burgos',
                                  'El Requerimiento',
                                  'La Bula Inter Caetera'],
                 'correcta': 'A'},
                {'pregunta': 'La Capitulación de Santa Fe se firmó en el '
                             'año:',
                 'alternativas': ['1494', '1492', '1453', '1498', '1502'],
                 'correcta': 'B'},
                {'pregunta': 'Colón zarpó en su primer viaje desde el puerto '
                             'de:',
                 'alternativas': ['Cádiz',
                                  'Sanlúcar',
                                  'Sevilla',
                                  'Lisboa',
                                  'Palos'],
                 'correcta': 'E'},
                {'pregunta': 'La primera isla a la que llegó Colón fue:',
                 'alternativas': ['Cuba',
                                  'Trinidad',
                                  'La Española',
                                  'Jamaica',
                                  'Guanahaní'],
                 'correcta': 'E'},
                {'pregunta': 'Las naves del primer viaje de Colón fueron:',
                 'alternativas': ['Nao, Carabela y Galeón',
                                  'Pinta, Niña y Santa María',
                                  'La Isabela, La Gallega y La Niña',
                                  'Victoria, Trinidad y Concepción',
                                  'Santiago, San Antonio y Victoria'],
                 'correcta': 'B'},
                {'pregunta': 'Colón sostenía, para justificar su proyecto, '
                             'la:',
                 'alternativas': ['Cercanía de África',
                                  'Esfericidad de la Tierra',
                                  'Ruta del Cabo de Buena Esperanza',
                                  'Existencia de un continente intermedio',
                                  'Planitud del mundo'],
                 'correcta': 'B'},
                {'pregunta': 'Los Reyes Católicos que apoyaron a Colón '
                             'fueron:',
                 'alternativas': ['Juan II y Beatriz',
                                  'Felipe II y María',
                                  'Carlos V e Isabel de Portugal',
                                  'Isabel de Castilla y Fernando de Aragón',
                                  'Carlos I y Juana'],
                 'correcta': 'D'},
                {'pregunta': 'En su tercer viaje, Colón llegó a la '
                             'desembocadura del río:',
                 'alternativas': ['Amazonas',
                                  'Orinoco',
                                  'Misisipi',
                                  'Magdalena',
                                  'Paraná'],
                 'correcta': 'B'},
                {'pregunta': 'El título que recibió Colón según la '
                             'Capitulación fue:',
                 'alternativas': ['Adelantado',
                                  'Corregidor',
                                  'Capitán general',
                                  'Encomendero',
                                  'Almirante, virrey y gobernador'],
                 'correcta': 'E'},
                {'pregunta': 'Instrumento náutico fundamental para la '
                             'orientación en alta mar:',
                 'alternativas': ['La brújula',
                                  'El telescopio',
                                  'El barómetro',
                                  'El sextante moderno',
                                  'El cronómetro'],
                 'correcta': 'A'},
                {'pregunta': 'En su segundo viaje, Colón fundó:',
                 'alternativas': ['Veracruz',
                                  'La Navidad',
                                  'Santo Domingo',
                                  'Panamá',
                                  'La Isabela'],
                 'correcta': 'E'},
                {'pregunta': 'El cuarto viaje de Colón se realizó en:',
                 'alternativas': ['1519', '1492', '1498', '1493', '1502'],
                 'correcta': 'E'},
                {'pregunta': 'Los países que encabezaron la expansión '
                             'ultramarina europea fueron:',
                 'alternativas': ['Inglaterra y Francia',
                                  'Holanda e Italia',
                                  'Francia y España',
                                  'Alemania y Suecia',
                                  'Portugal y España'],
                 'correcta': 'E'},
                {'pregunta': 'Colón llamó a la isla de Guanahaní:',
                 'alternativas': ['La Española',
                                  'La Isabela',
                                  'San Salvador',
                                  'Juana',
                                  'Trinidad'],
                 'correcta': 'C'},
                {'pregunta': 'La causa económica principal de los '
                             'descubrimientos geográficos fue:',
                 'alternativas': ['La búsqueda de una nueva ruta a las '
                                  'Indias',
                                  'La expansión del feudalismo',
                                  'La difusión del cristianismo únicamente',
                                  'El exceso de población',
                                  'La escasez de tierras agrícolas'],
                 'correcta': 'A'},
                {'pregunta': 'El astrolabio servía para:',
                 'alternativas': ['Medir la temperatura',
                                  'Determinar la latitud mediante los astros',
                                  'Medir la profundidad del mar',
                                  'Orientar el timón',
                                  'Calcular la velocidad'],
                 'correcta': 'B'},
                {'pregunta': 'La embarcación ligera y maniobrable usada en '
                             'los viajes de exploración fue:',
                 'alternativas': ['La carabela',
                                  'La goleta',
                                  'La fragata',
                                  'El bergantín',
                                  'El galeón'],
                 'correcta': 'A'},
                {'pregunta': 'El primer viaje de Colón se realizó en el año:',
                 'alternativas': ['1493', '1453', '1492', '1498', '1502'],
                 'correcta': 'C'},
                {'pregunta': 'En su cuarto viaje, Colón recorrió '
                             'principalmente:',
                 'alternativas': ['Las costas de América Central',
                                  'La costa de Brasil',
                                  'El Río de la Plata',
                                  'La costa del Pacífico',
                                  'Las Antillas Mayores'],
                 'correcta': 'A'},
                {'pregunta': 'El nombre «América» proviene del navegante '
                             'italiano:',
                 'alternativas': ['Cristóbal Colón',
                                  'Américo Vespucio',
                                  'Fernando de Magallanes',
                                  'Vasco da Gama',
                                  'Hernán Cortés'],
                 'correcta': 'B'},
                {'pregunta': 'El navegante portugués que llegó a la India '
                             'bordeando las costas de África en 1499 fue:',
                 'alternativas': ['Cristóbal Colón',
                                  'Vasco de Gama',
                                  'Fernando de Magallanes',
                                  'Américo Vespucio',
                                  'Enrique el Navegante'],
                 'correcta': 'B'},
                {'pregunta': 'Cristóbal Colón, en su primer viaje a América, '
                             'bautizó con el nombre de Juana a la isla de: '
                             '(UNSAAC 2018)',
                 'alternativas': ['Trinidad',
                                  'Haití',
                                  'Guanahaní',
                                  'Cuba',
                                  'Jamaica'],
                 'correcta': 'D'},
                {'pregunta': 'El acontecimiento que caracteriza al cuarto '
                             'viaje de Cristóbal Colón es: (UNSAAC 2022)',
                 'alternativas': ['El descubrimiento de las costas de '
                                  'Honduras, Nicaragua y de Panamá',
                                  'La llegada a la Isla Guanahaní llamándola '
                                  'San Salvador',
                                  'El arribo de 17 carabelas y 1500 hombres',
                                  'La llegada a la isla Martinica y Dominica',
                                  'La fundación de la primera ciudad '
                                  'denominada Isabela'],
                 'correcta': 'A'},
                {'pregunta': 'En los enfrentamientos de la resistencia, en '
                             'la batalla de Sacsayhuamán en 1536, destacó el '
                             'valeroso capitán: (UNSAAC 2022)',
                 'alternativas': ['Manco Inca',
                                  'Huayna Cápac',
                                  'Suruhuamán',
                                  'Sayri Túpac',
                                  'Titu Yupanqui'],
                 'correcta': 'C'},
                {'pregunta': 'Cristóbal Colón, en su segundo viaje, salió '
                             'del puerto de: (UNSAAC Ordinario)',
                 'alternativas': ['Trinidad',
                                  'San Lucar',
                                  'Palos',
                                  'Cádiz',
                                  'Valladolid'],
                 'correcta': 'D'},
                {'pregunta': 'Francisco Pizarro descubrió el Tahuantinsuyo, '
                             'en el: (UNSAAC Ordinario)',
                 'alternativas': ['Segundo viaje',
                                  'Primer viaje',
                                  'Tercer viaje',
                                  'Quinto viaje',
                                  'Cuarto viaje'],
                 'correcta': 'A'},
                {'pregunta': 'Cristóbal Colón descubrió Panamá en el: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Primer viaje',
                                  'Segundo viaje',
                                  'Quinto viaje',
                                  'Cuarto viaje',
                                  'Tercer viaje'],
                 'correcta': 'D'},
                {'pregunta': 'En el convento franciscano de la Rábida '
                             '(España), la empresa de Cristóbal Colón '
                             'encontró el apoyo del religioso: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Vicente de Valverde',
                                  'Hernando de Luque',
                                  'Bartolomé de las Casas',
                                  'Joseph de Acosta',
                                  'Juan Pérez'],
                 'correcta': 'E'},
                {'pregunta': 'Por la Capitulación de Santa Fe, Cristóbal '
                             'Colón tendría derecho a: (UNSAAC Ordinario)',
                 'alternativas': ['Ser gobernador de España',
                                  'El título de adelantado',
                                  'Fundar la ciudad de Panamá',
                                  'La décima parte de las riquezas',
                                  'La mitad de oro de las indias'],
                 'correcta': 'D'},
                {'pregunta': 'En su tercer viaje, Francisco Pizarro: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Descubrió el gran Mar del Sur',
                                  'Llegó hasta la desembocadura del río '
                                  'Santa',
                                  'Fundó la primera ciudad española en el '
                                  'Perú',
                                  'Se limitó a explorar las costas del norte '
                                  'peruano',
                                  'Protagonizó el incidente de los trece del '
                                  'gallo'],
                 'correcta': 'C'},
                {'pregunta': 'Por sus efectos, la tercera expedición de '
                             'Francisco Pizarro al Perú se conoce como '
                             'viaje: (UNSAAC Ordinario)',
                 'alternativas': ['Experimental',
                                  'Invasor',
                                  'Descubridor',
                                  'Exploración',
                                  'Pionero'],
                 'correcta': 'B'},
                {'pregunta': 'La primera ciudad fundada en América por '
                             'Cristóbal Colón fue: (UNSAAC Ordinario)',
                 'alternativas': ['La Habana',
                                  'Panamá',
                                  'Juana',
                                  'La Isabela',
                                  'La Dominica'],
                 'correcta': 'D'},
                {'pregunta': 'En su segundo viaje, Cristóbal Colón, en 1493, '
                             'llegó a las islas de: (UNSAAC Ordinario)',
                 'alternativas': ['Haití - Trinidad - Tobago',
                                  'Guanahaní - Cuba y Martinica',
                                  'Las Antillas - Puerto Rico y Jamaica',
                                  'Canarias y Trinidad',
                                  'Canarias y las Antillas'],
                 'correcta': 'C'},
                {'pregunta': 'La Reina Isabel de Castilla accedió a la '
                             'aprobación del Proyecto Colombino, debido a: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['La influencia de los frailes Juan Pérez y '
                                  'Antonio Marchena',
                                  'Los aportes geográficos y mapas de '
                                  'Ptolomeo',
                                  'La recomendación del rey Juan II de '
                                  'Portugal',
                                  'Los consejos de Pablo Toscanelli',
                                  'Los datos alcanzados por su suegro '
                                  'Nicolás de Perestrello'],
                 'correcta': 'A'},
                {'pregunta': 'El contrato mediante el cual se autorizó el '
                             'viaje de Cristóbal Colón, por la Corona '
                             'Española, se conoce como: (UNSAAC Ordinario)',
                 'alternativas': ['El reparto de América por el Papa '
                                  'Alejandro VI',
                                  'La Capitulación de Toledo',
                                  'El Tratado de Tordesillas',
                                  'La Capitulación de Santa Fe',
                                  'La Bula de Partición del Mundo'],
                 'correcta': 'D'},
                {'pregunta': 'Después del tercer viaje de Colón, el cuarto '
                             'viaje no llegó hasta: (UNSAAC Ordinario)',
                 'alternativas': ['Honduras',
                                  'Panamá',
                                  'México',
                                  'Nicaragua',
                                  'Costa Rica'],
                 'correcta': 'C'},
                {'pregunta': 'Cristóbal Colón realizó varios viajes de '
                             'descubrimiento; el cuarto y último viaje de '
                             'exploración, se caracterizó por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['La llegada a las islas de Guanahaní y '
                                  'Cuba',
                                  'Haber recorrido por las costas de la '
                                  'actual Honduras, Nicaragua y Panamá',
                                  'Arribar a las islas de Trinidad y la '
                                  'desembocadura del río Orinoco de '
                                  'Venezuela',
                                  'La llegada a las pequeñas islas de '
                                  'Antillas y Puerto Rico',
                                  'La fundación de la primera ciudad llamada '
                                  'Isabela en la española (Haití)'],
                 'correcta': 'B'},
                {'pregunta': 'En la capitulación de Santa Fe, la reina '
                             'Isabel de Castilla y Cristóbal Colón acordaron '
                             'realizar los preparativos para la expedición '
                             'en el puerto de: (UNSAAC Ordinario)',
                 'alternativas': ['Miraflores',
                                  'Cádiz',
                                  'Palos',
                                  'Barrameda',
                                  'Atacama'],
                 'correcta': 'C'},
                {'pregunta': 'Cristóbal Colón fundó la primera ciudad '
                             'española en América, bautizada con el nombre '
                             'de: (UNSAAC Ordinario)',
                 'alternativas': ['Dominica',
                                  'Juana',
                                  'San Salvador',
                                  'Isabela',
                                  'Española'],
                 'correcta': 'D'},
                {'pregunta': 'Cristóbal Colón llegó a América cuando en '
                             'España reinaba: (UNSAAC Ordinario)',
                 'alternativas': ['Felipe II',
                                  'Fernando VII',
                                  'Fernando de Aragón',
                                  'Carlos III',
                                  'Carlos V'],
                 'correcta': 'C'},
                {'pregunta': 'La primera ciudad fundada por Francisco '
                             'Pizarro en el Perú fue: (II CEPRU 2011)',
                 'alternativas': ['Huaura',
                                  'Jauja',
                                  'San Miguel de Piura',
                                  'Cusco',
                                  'Lima'],
                 'correcta': 'C'},
                {'pregunta': 'Para realizar el viaje de Cajamarca a Cusco, '
                             'Francisco Pizarro nombró como Inca figurativo '
                             'o títere a: (II CEPRU 2011)',
                 'alternativas': ['Yahuar Huacac',
                                  'Túpac Huallpa',
                                  'Inca Roca',
                                  'Sinchi Roca',
                                  'Wiracocha'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'DESCUBRIMIENTOS GEOGRÁFICOS',
                      'items': ['Causas: la búsqueda de una nueva ruta hacia '
                                'las Indias tras la caída de Constantinopla '
                                'en 1453 a manos de los turcos.',
                                'Avances técnicos que lo hicieron posible: '
                                'la brújula, el astrolabio y la carabela.',
                                'Portugal y España encabezaron la expansión '
                                'ultramarina.',
                                'Los navegantes portugueses llegaron a las '
                                'Indias bordeando África: Vasco de Gama en '
                                '1499.']},
                     {'titulo': 'Y 9.3 COLÓN Y LA CAPITULACIÓN',
                      'items': ['Cristóbal Colón propuso llegar a las Indias '
                                'navegando hacia el occidente, sosteniendo '
                                'la esfericidad de la Tierra.',
                                'Su proyecto fue aceptado por los Reyes '
                                'Católicos Isabel de Castilla y Fernando de '
                                'Aragón.',
                                'La Capitulación de Santa Fe (1492) fue el '
                                'documento que fijó los títulos y beneficios '
                                'de Colón: Almirante, virrey y gobernador.']},
                     {'titulo': 'LOS VIAJES DE COLÓN',
                      'items': ['Primer viaje (1492): zarpó del puerto de '
                                'Palos con las naves Pinta, Niña y Santa '
                                'María. Llegó a la isla Guanahaní, a la que '
                                'llamó San Salvador.',
                                'Segundo viaje (1493): llevó colonos y '
                                'animales; fundó La Isabela.',
                                'Tercer viaje (1498): llegó a la '
                                'desembocadura del Orinoco, tierra firme del '
                                'continente.',
                                'Cuarto viaje (1502): recorrió las costas de '
                                'América Central.',
                                'El nombre «América» proviene del navegante '
                                'italiano Américo Vespucio, quien reconoció '
                                'que se trataba de un nuevo continente.']}],
  'qr_reto': [{'pregunta': 'La embarcación ligera y maniobrable usada en los '
                           'viajes de exploración fue:',
               'respuesta': 'La carabela'},
              {'pregunta': 'En su cuarto viaje, Colón recorrió '
                           'principalmente:',
               'respuesta': 'Las costas de América Central'},
              {'pregunta': 'Cristóbal Colón descubrió Panamá en el:',
               'respuesta': 'Cuarto viaje'}],
  'qr_dato': 'Los navegantes portugueses llegaron a las Indias bordeando '
             'África: Vasco de Gama en 1499.'},
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
                           'ejecución de Gonzalo {Pizarro}.']}],
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
                 'alternativas': ['Pizarro, Valverde y Soto',
                                  'Pizarro, Almagro y Luque',
                                  'Pizarro, Cortés y Luque',
                                  'Pizarro, Alvarado y Belalcázar',
                                  'Almagro, Toledo y Luque'],
                 'correcta': 'B'},
                {'pregunta': 'El episodio de los Trece del Gallo ocurrió '
                             'durante el:',
                 'alternativas': ['Primer viaje',
                                  'Viaje de regreso',
                                  'Segundo viaje',
                                  'Tercer viaje',
                                  'Cuarto viaje'],
                 'correcta': 'C'},
                {'pregunta': 'La Capitulación de Toledo se firmó en el año:',
                 'alternativas': ['1524', '1531', '1529', '1532', '1535'],
                 'correcta': 'C'},
                {'pregunta': 'La Capitulación de Toledo nombró a Pizarro:',
                 'alternativas': ['Gobernador y capitán general',
                                  'Adelantado de Nueva Toledo',
                                  'Corregidor',
                                  'Virrey del Perú',
                                  'Almirante'],
                 'correcta': 'A'},
                {'pregunta': 'La captura de Atahualpa se produjo el:',
                 'alternativas': ['16 de noviembre de 1532',
                                  '18 de enero de 1535',
                                  '26 de julio de 1533',
                                  '15 de agosto de 1536',
                                  '6 de diciembre de 1534'],
                 'correcta': 'A'},
                {'pregunta': 'La captura del Inca ocurrió en la plaza de:',
                 'alternativas': ['Cusco',
                                  'Cajamarca',
                                  'Piura',
                                  'Jauja',
                                  'Tumbes'],
                 'correcta': 'B'},
                {'pregunta': 'El sacerdote que entregó la Biblia a Atahualpa '
                             'fue:',
                 'alternativas': ['Hernando de Luque',
                                  'Vicente Valverde',
                                  'Toribio de Mogrovejo',
                                  'Bartolomé de las Casas',
                                  'Jerónimo de Loayza'],
                 'correcta': 'B'},
                {'pregunta': 'La primera ciudad española fundada en el Perú '
                             'fue:',
                 'alternativas': ['San Miguel de Tangarará',
                                  'Lima',
                                  'Cusco español',
                                  'Jauja',
                                  'Trujillo'],
                 'correcta': 'A'},
                {'pregunta': 'Lima fue fundada por Pizarro el:',
                 'alternativas': ['9 de diciembre de 1824',
                                  '18 de enero de 1535',
                                  '6 de abril de 1538',
                                  '16 de noviembre de 1532',
                                  '26 de junio de 1541'],
                 'correcta': 'B'},
                {'pregunta': 'El Inca que encabezó la resistencia y sitió el '
                             'Cusco en 1536 fue:',
                 'alternativas': ['Túpac Amaru I',
                                  'Atahualpa',
                                  'Manco Inca',
                                  'Sayri Túpac',
                                  'Huáscar'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado neoinca de resistencia se estableció '
                             'en:',
                 'alternativas': ['Chachapoyas',
                                  'Cajamarca',
                                  'Ollantaytambo',
                                  'Vilcabamba',
                                  'Vitcos únicamente'],
                 'correcta': 'D'},
                {'pregunta': 'El último inca de Vilcabamba, ejecutado en '
                             '1572, fue:',
                 'alternativas': ['Manco Inca',
                                  'Paullu Inca',
                                  'Túpac Amaru I',
                                  'Titu Cusi Yupanqui',
                                  'Sayri Túpac'],
                 'correcta': 'C'},
                {'pregunta': 'La ejecución de Túpac Amaru I fue ordenada por '
                             'el virrey:',
                 'alternativas': ['Andrés Hurtado de Mendoza',
                                  'Francisco de Toledo',
                                  'Pedro de la Gasca',
                                  'Blasco Núñez de Vela',
                                  'Antonio de Mendoza'],
                 'correcta': 'B'},
                {'pregunta': 'En la batalla de las Salinas (1538) fue '
                             'derrotado:',
                 'alternativas': ['Diego de Almagro',
                                  'Hernando Pizarro',
                                  'Almagro el Mozo',
                                  'Gonzalo Pizarro',
                                  'Núñez de Vela'],
                 'correcta': 'A'},
                {'pregunta': 'El primer virrey del Perú, muerto en la '
                             'batalla de Añaquito, fue:',
                 'alternativas': ['Andrés Hurtado de Mendoza',
                                  'Antonio de Mendoza',
                                  'Pedro de la Gasca',
                                  'Blasco Núñez de Vela',
                                  'Francisco de Toledo'],
                 'correcta': 'D'},
                {'pregunta': 'En la batalla de Jaquijahuana (1548) fue '
                             'derrotado:',
                 'alternativas': ['Francisco Pizarro',
                                  'Almagro el Mozo',
                                  'Hernando de Soto',
                                  'Diego de Almagro',
                                  'Gonzalo Pizarro'],
                 'correcta': 'E'},
                {'pregunta': 'El primer viaje de la conquista llegó hasta:',
                 'alternativas': ['Isla del Gallo',
                                  'Cajamarca',
                                  'Tumbes',
                                  'Puerto del Hambre',
                                  'Panamá'],
                 'correcta': 'D'},
                {'pregunta': 'El rescate ofrecido por Atahualpa consistió '
                             'en:',
                 'alternativas': ['Naves y armas',
                                  'Un cuarto de plata solamente',
                                  'Un cuarto de oro y dos de plata',
                                  'Tributos anuales',
                                  'Tierras y siervos'],
                 'correcta': 'C'},
                {'pregunta': 'El tercer viaje de la conquista partió de '
                             'Panamá en el año:',
                 'alternativas': ['1532', '1529', '1524', '1531', '1526'],
                 'correcta': 'D'},
                {'pregunta': 'El acto formal de sometimiento leído a '
                             'Atahualpa se conoce como:',
                 'alternativas': ['Las Ordenanzas',
                                  'La Capitulación',
                                  'La Bula',
                                  'El Testamento',
                                  'El Requerimiento'],
                 'correcta': 'E'},
                {'pregunta': 'La capitulación de Toledo fue firmada por '
                             'Isabel de Portugal; dicho acto dio inicio a '
                             'la: (UNSAAC Ordinario)',
                 'alternativas': ['Creación del Virreinato en el Perú',
                                  'Institucionalización colonial en el Perú',
                                  'Pacificación del Perú',
                                  'Dominación y dependencia del Perú',
                                  'Invasión española al Perú'],
                 'correcta': 'E'},
                {'pregunta': 'En la Batalla de Salinas, las tropas '
                             'almagristas estuvieron al mando de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Almagro el Mozo',
                                  'Fray Tomas de Berlanga',
                                  'Rodrigo de Ordoñez',
                                  'Diego de Centeno',
                                  'Cristóbal Baca de Castro'],
                 'correcta': 'C'},
                {'pregunta': 'En la Guerra de los Encomenderos, en la '
                             'batalla de Jaquijahuana, se enfrentaron los '
                             'bandos de: (UNSAAC Ordinario)',
                 'alternativas': ['Gonzalo Pizarro y Diego Centeno',
                                  'Gonzalo Pizarro y Cristóbal Baca de '
                                  'Castro',
                                  'Almagro el Mozo y Blasco Núñez de Vela',
                                  'Gonzalo Pizarro y el Pacificador Pedro de '
                                  'la Gasca',
                                  'Francisco Pizarro y Fray Tomas de '
                                  'Berlanga'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'Y 10.2 LA EMPRESA DE CONQUISTA',
                      'items': ['La empresa la formaron Francisco Pizarro, '
                                'Diego de Almagro y el sacerdote Hernando de '
                                'Luque.',
                                'Primer viaje (1524–1525): llegó hasta '
                                'Puerto del Hambre; fue un fracaso.',
                                'Segundo viaje (1526–1528): episodio de los '
                                'Trece del Gallo en la isla del Gallo; se '
                                'llegó hasta Tumbes.',
                                'La Capitulación de Toledo (1529) fue '
                                'firmada por Pizarro con la reina Isabel de '
                                'Portugal; lo nombró gobernador y capitán '
                                'general.',
                                'Tercer viaje (1531): partió de Panamá; '
                                'fundó San Miguel de Tangarará, primera '
                                'ciudad española en el Perú.']},
                     {'titulo': 'LA CAPTURA DEL INCA',
                      'items': ['El 16 de noviembre de 1532 se produjo la '
                                'captura de Atahualpa en la plaza de '
                                'Cajamarca.',
                                'El sacerdote Vicente Valverde le entregó la '
                                'Biblia en el llamado Requerimiento.',
                                'Atahualpa ofreció un cuarto lleno de oro y '
                                'dos de plata como rescate; fue ejecutado en '
                                '1533.']},
                     {'titulo': 'Y 10.4 FUNDACIONES Y RESISTENCIA',
                      'items': ['Pizarro fundó Lima el 18 de enero de 1535, '
                                'llamada Ciudad de los Reyes.',
                                'Manco Inca encabezó la resistencia y sitió '
                                'el Cusco en 1536. Se replegó a Vilcabamba, '
                                'donde se formó el Estado neoinca.',
                                'El último inca de Vilcabamba fue Túpac '
                                'Amaru I, ejecutado en 1572 por orden del '
                                'virrey Toledo.']},
                     {'titulo': 'GUERRA CIVIL ENTRE LOS INVASORES',
                      'items': ['Batalla de las Salinas (1538): Pizarro '
                                'venció a Almagro.',
                                'Batalla de Chupas (1542): derrota de '
                                'Almagro «el Mozo».',
                                'Batalla de Añaquito (1546): muerte del '
                                'primer virrey Blasco Núñez de Vela.',
                                'Batalla de Jaquijahuana (1548): derrota y '
                                'ejecución de Gonzalo Pizarro.']}],
  'qr_reto': [{'pregunta': 'El tercer viaje de la conquista partió de Panamá '
                           'en el año:',
               'respuesta': '1531'},
              {'pregunta': 'La captura del Inca ocurrió en la plaza de:',
               'respuesta': 'Cajamarca'},
              {'pregunta': 'La Capitulación de Toledo se firmó en el año:',
               'respuesta': '1529'}],
  'qr_dato': 'Batalla de las Salinas (1538): Pizarro venció a Almagro.'},
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
                           'La Universidad de San Marcos fue fundada en '
                           '{1551} como Real y Pontificia Universidad, '
                           'nombrada así por el papa {Pío V}.',
                           'La Universidad de San Antonio Abad del Cusco se '
                           'originó en el seminario creado por el obispo '
                           '{Antonio de la Raya}.',
                           'El gestor de la creación de la Universidad de '
                           'San Antonio Abad fue el obispo {Manuel de '
                           'Mollinedo y Angulo}.',
                           'El papa {Inocencio XII} emitió en {1692} el '
                           'breve pontificio que creó la Universidad de San '
                           'Antonio Abad del Cusco.',
                           'El primer rector de la Universidad de San '
                           'Antonio Abad del Cusco fue el Dr. {Juan Cárdenas '
                           'y Céspedes}.']}],
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
                 'alternativas': ['Encomienda',
                                  'Mita',
                                  'Reducción',
                                  'Yanaconaje',
                                  'Repartimiento'],
                 'correcta': 'A'},
                {'pregunta': 'La encomienda otorgaba al encomendero el '
                             'derecho a recibir:',
                 'alternativas': ['El tributo de los indígenas',
                                  'La propiedad de la tierra',
                                  'Las minas del lugar',
                                  'Títulos nobiliarios',
                                  'El gobierno provincial'],
                 'correcta': 'A'},
                {'pregunta': 'El organismo con sede en España encargado de '
                             'legislar sobre América fue:',
                 'alternativas': ['El Consejo de Indias',
                                  'El Consulado',
                                  'El Cabildo',
                                  'La Casa de Contratación',
                                  'La Audiencia'],
                 'correcta': 'A'},
                {'pregunta': 'La institución que controlaba el comercio con '
                             'América, con sede en Sevilla, fue:',
                 'alternativas': ['La Real Hacienda',
                                  'La Audiencia',
                                  'El Tribunal del Consulado',
                                  'El Consejo de Indias',
                                  'La Casa de Contratación'],
                 'correcta': 'E'},
                {'pregunta': 'El máximo tribunal de justicia en América '
                             'colonial fue:',
                 'alternativas': ['El Cabildo',
                                  'La Audiencia',
                                  'La Intendencia',
                                  'El Consulado',
                                  'El Corregimiento'],
                 'correcta': 'B'},
                {'pregunta': 'El virrey que organizó el virreinato peruano y '
                             'creó las reducciones fue:',
                 'alternativas': ['Andrés Hurtado de Mendoza',
                                  'Francisco de Toledo',
                                  'Blasco Núñez de Vela',
                                  'Pedro de la Gasca',
                                  'Manuel de Amat'],
                 'correcta': 'B'},
                {'pregunta': 'El principal centro minero de plata en el '
                             'virreinato fue:',
                 'alternativas': ['Cerro de Pasco',
                                  'Potosí',
                                  'Hualgayoc',
                                  'Castrovirreyna',
                                  'Huancavelica'],
                 'correcta': 'B'},
                {'pregunta': 'Huancavelica fue famosa por la producción de:',
                 'alternativas': ['Estaño',
                                  'Oro',
                                  'Cobre',
                                  'Plata',
                                  'Mercurio o azogue'],
                 'correcta': 'E'},
                {'pregunta': 'El impuesto sobre la producción minera '
                             'entregado a la Corona fue:',
                 'alternativas': ['El quinto real',
                                  'El almojarifazgo',
                                  'El diezmo',
                                  'La alcabala',
                                  'El tributo indígena'],
                 'correcta': 'A'},
                {'pregunta': 'El comercio colonial se caracterizó por ser:',
                 'alternativas': ['Descentralizado',
                                  'Libre',
                                  'De trueque',
                                  'Monopólico',
                                  'Regional'],
                 'correcta': 'D'},
                {'pregunta': 'Los pueblos donde se concentró a la población '
                             'indígena para controlarla se llamaron:',
                 'alternativas': ['Corregimientos',
                                  'Reducciones',
                                  'Encomiendas',
                                  'Obrajes',
                                  'Haciendas'],
                 'correcta': 'B'},
                {'pregunta': 'La sociedad colonial se organizó de manera:',
                 'alternativas': ['Sin distinciones legales',
                                  'Igualitaria',
                                  'Estamental según el origen étnico',
                                  'Democrática',
                                  'Meritocrática'],
                 'correcta': 'C'},
                {'pregunta': 'El colegio colonial destinado a los hijos de '
                             'caciques en el Cusco fue:',
                 'alternativas': ['Santo Tomás',
                                  'San Borja',
                                  'San Bernardo',
                                  'San Marcos',
                                  'San Pablo'],
                 'correcta': 'B'},
                {'pregunta': 'La Universidad Nacional de San Antonio Abad '
                             'del Cusco fue fundada en:',
                 'alternativas': ['1571', '1821', '1551', '1692', '1620'],
                 'correcta': 'D'},
                {'pregunta': 'La Universidad Nacional Mayor de San Marcos '
                             'fue fundada en:',
                 'alternativas': ['1572', '1692', '1492', '1551', '1821'],
                 'correcta': 'D'},
                {'pregunta': 'La mita minera colonial consistió en:',
                 'alternativas': ['Un servicio doméstico',
                                  'Un tributo en especies',
                                  'Trabajo obligatorio por turnos en las '
                                  'minas',
                                  'Una encomienda de indios',
                                  'Un préstamo forzoso'],
                 'correcta': 'C'},
                {'pregunta': 'El funcionario encargado de cobrar tributos en '
                             'las provincias fue:',
                 'alternativas': ['El corregidor',
                                  'El alcalde mayor',
                                  'El oidor',
                                  'El visitador',
                                  'El virrey'],
                 'correcta': 'A'},
                {'pregunta': 'La educación colonial se caracterizó por ser:',
                 'alternativas': ['Universal y gratuita',
                                  'Laica',
                                  'Técnica',
                                  'Elitista',
                                  'Obligatoria'],
                 'correcta': 'D'},
                {'pregunta': 'El repartimiento consistió principalmente en:',
                 'alternativas': ['El reparto de indígenas entre los '
                                  'conquistadores',
                                  'La creación de cabildos',
                                  'La fundación de ciudades',
                                  'La distribución de tierras entre '
                                  'indígenas',
                                  'La entrega de minas'],
                 'correcta': 'A'},
                {'pregunta': 'El sistema de transporte comercial entre '
                             'España y América se basó en:',
                 'alternativas': ['Naves individuales libres',
                                  'Barcos de vapor',
                                  'Caravanas terrestres',
                                  'Flotas y galeones',
                                  'Compañías privadas holandesas'],
                 'correcta': 'D'},
                {'pregunta': 'La Universidad de San Marcos fue fundada en el '
                             'año:',
                 'alternativas': ['1538', '1551', '1600', '1692', '1492'],
                 'correcta': 'B'},
                {'pregunta': 'El obispo que creó el seminario del que se '
                             'originó la Universidad de San Antonio Abad del '
                             'Cusco fue:',
                 'alternativas': ['Manuel de Mollinedo y Angulo',
                                  'Antonio de la Raya',
                                  'Juan Cárdenas y Céspedes',
                                  'Vicente de Valverde',
                                  'Jerónimo de Loayza'],
                 'correcta': 'B'},
                {'pregunta': 'El gestor de la creación de la Universidad de '
                             'San Antonio Abad del Cusco como universidad '
                             'fue el obispo:',
                 'alternativas': ['Antonio de la Raya',
                                  'Manuel de Mollinedo y Angulo',
                                  'Juan Cárdenas y Céspedes',
                                  'Vicente de Valverde',
                                  'Jerónimo de Loayza'],
                 'correcta': 'B'},
                {'pregunta': 'El papa que emitió el breve pontificio de '
                             'creación de la Universidad de San Antonio Abad '
                             'del Cusco, en 1692, fue:',
                 'alternativas': ['Pío V',
                                  'Inocencio XII',
                                  'Pío VII',
                                  'Gregorio XIII',
                                  'León X'],
                 'correcta': 'B'},
                {'pregunta': 'El primer rector de la Universidad de San '
                             'Antonio Abad del Cusco fue:',
                 'alternativas': ['Antonio de la Raya',
                                  'Juan Cárdenas y Céspedes',
                                  'Manuel de Mollinedo',
                                  'Juan Bautista de la Roca',
                                  'Fray Vicente de Valverde'],
                 'correcta': 'B'},
                {'pregunta': 'La encomienda fue abolida por la Real Cédula, '
                             'provocando la: (UNSAAC Ordinario)',
                 'alternativas': ['Protesta de los caciques',
                                  'Rebelión de Manco Inca',
                                  'Rebelión de los encomenderos',
                                  'Revolución de Tupac Amaru',
                                  'Caída del Virrey'],
                 'correcta': 'C'},
                {'pregunta': 'La institución colonial caracterizada por el '
                             'vasallaje ideológico en lo político, económico '
                             'y social fue: (UNSAAC Ordinario)',
                 'alternativas': ['El repartimiento',
                                  'La intendencia',
                                  'La encomienda',
                                  'El corregimiento',
                                  'La Real Audiencia'],
                 'correcta': 'C'},
                {'pregunta': 'La primera institución de explotación en el '
                             'Perú fue: (UNSAAC Ordinario)',
                 'alternativas': ['La mita',
                                  'El corregimiento',
                                  'El repartimiento',
                                  'La Audiencia',
                                  'La intendencia'],
                 'correcta': 'C'},
                {'pregunta': 'Dentro de las instituciones coloniales, la '
                             'institución más antigua fue: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Repartimientos',
                                  'Encomiendas',
                                  'Intendencias',
                                  'Corregimientos',
                                  'Mita minera'],
                 'correcta': 'B'},
                {'pregunta': 'En la Colonia, la institución que cumplió la '
                             'función de vasallaje ideológico, político, '
                             'económico y social fue: (UNSAAC Ordinario)',
                 'alternativas': ['La Corona',
                                  'El Consejo de Indias',
                                  'Los Repartimientos',
                                  'La Encomienda',
                                  'La Real Audiencia'],
                 'correcta': 'D'},
                {'pregunta': 'El gestor de la creación de la Universidad '
                             'Nacional de San Antonio Abad del Cusco en 1692 '
                             'fue: (UNSAAC Ordinario)',
                 'alternativas': ['Manuel Mollinedo y Angulo',
                                  'Jerónimo de Aliaga',
                                  'Juan Cárdenas y Céspedes',
                                  'Juan Bautista de la Roca',
                                  'Tomas de San Martín'],
                 'correcta': 'A'},
                {'pregunta': 'El impuesto que la Corona Española exigía a '
                             'sus colonias, conocido como la Media Anata, '
                             'consistía en el: (UNSAAC Ordinario)',
                 'alternativas': ['Pago proporcional de los comerciantes por '
                                  'la custodia de sus cargamentos',
                                  'Cobro por los diezmos y primicias a las '
                                  'autoridades eclesiásticas',
                                  'Impuestos que afectaban a las '
                                  'transacciones comerciales internas',
                                  'Pago de impuesto por el salario que '
                                  'percibían las autoridades',
                                  'Recojo de los impuestos aduaneros en los '
                                  'puertos americanos'],
                 'correcta': 'D'},
                {'pregunta': 'La organización social del Perú Colonial que '
                             'correspondió al sector de la clase del bajo '
                             'pueblo estuvo conformada por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Españoles y criollos dedicados a pequeñas '
                                  'actividades comerciales y artesanos',
                                  'Españoles y criollos carentes de título '
                                  'nobiliario poseedores de fortuna y '
                                  'profesionales',
                                  'Indios descendientes de los incas, que se '
                                  'desarrollaron en un ambiente comunitario',
                                  'Españoles y criollos con títulos '
                                  'nobiliarios, funcionarios públicos y '
                                  'eclesiásticos',
                                  'Esclavos negros que servían en las casas '
                                  'señoriales y haciendas'],
                 'correcta': 'A'},
                {'pregunta': 'El Rey que dispuso la supresión de las '
                             'encomiendas, fue: (UNSAAC Ordinario)',
                 'alternativas': ['Felipe III',
                                  'Felipe II',
                                  'Carlos V',
                                  'Carlos II',
                                  'Carlos III'],
                 'correcta': 'C'},
                {'pregunta': 'La institución que se creó por los excesivos '
                             'abusos que cometían los encomenderos fue: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['El Virreinato',
                                  'El Corregimiento',
                                  'La Intendencia',
                                  'El Cacicazgo',
                                  'El Cabildo'],
                 'correcta': 'B'},
                {'pregunta': 'La Institución Educativa de origen colonial, '
                             'que fue fundada para los hijos de los caciques '
                             'en el Cusco, fue el colegio de San: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Ignacio de Loyola',
                                  'Francisco de Borja',
                                  'Antonio Abad',
                                  'Bernardo',
                                  'Felipe'],
                 'correcta': 'B'},
                {'pregunta': 'En el Periodo Colonial, el impuesto denominado '
                             'Diezmo, fue el: (UNSAAC Ordinario)',
                 'alternativas': ['Pago a las aduanas por compra de '
                                  'productos mercantiles de exportación',
                                  'Tributo que se cobraba a la compra y '
                                  'venta de los bienes muebles e inmuebles',
                                  'Pago a los jornaleros por su trabajo en '
                                  'las haciendas cañaverales',
                                  'Pago de la décima parte de la producción '
                                  'agrícola y obrajera en favor de la '
                                  'iglesia',
                                  'Tributo de la quinta parte de la '
                                  'producción minera'],
                 'correcta': 'D'},
                {'pregunta': 'Sobre la educación Colonial del Perú, se '
                             'afirma que: (UNSAAC Ordinario)',
                 'alternativas': ['La universidad fue una institución '
                                  'elitista',
                                  'Los colegios mayores fueron centros de '
                                  'formación de los caciques',
                                  'La universidad estaba regentada por '
                                  'autoridades civiles',
                                  'Los colegios mayores fueron equivalentes '
                                  'a las universidades',
                                  'La primera universidad del Perú fue la de '
                                  'San Antonio Abad del Cusco'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'Y 11.2 REPARTIMIENTO Y ENCOMIENDA',
                      'items': ['El repartimiento fue el reparto de '
                                'indígenas entre los conquistadores para '
                                'trabajos y servicios.',
                                'La encomienda consistió en la entrega de un '
                                'grupo de indígenas a un encomendero, quien '
                                'recibía su tributo a cambio de protegerlos '
                                'y evangelizarlos.',
                                'No otorgaba propiedad sobre la tierra ni '
                                'sobre las personas, aunque en la práctica '
                                'derivó en abusos.']},
                     {'titulo': 'ORDENAMIENTO POLÍTICO',
                      'items': ['En España: el Rey, el Consejo de Indias y '
                                'la Casa de Contratación de Sevilla, que '
                                'controlaba el comercio.',
                                'En América: el Virrey, las Audiencias '
                                '(máximo tribunal de justicia), los '
                                'corregidores y los cabildos.',
                                'El virrey Francisco de Toledo organizó el '
                                'virreinato y creó las reducciones de '
                                'indios.']},
                     {'titulo': 'ORDENAMIENTO ECONÓMICO',
                      'items': ['La actividad principal fue la minería, '
                                'destacando Potosí (plata) y Huancavelica '
                                '(mercurio o azogue).',
                                'La mita minera colonial obligaba a los '
                                'indígenas a trabajar por turnos en las '
                                'minas.',
                                'El comercio fue monopólico: solo a través '
                                'de los puertos autorizados y el sistema de '
                                'flotas y galeones.',
                                'El principal impuesto sobre la producción '
                                'minera fue el quinto real.']},
                     {'titulo': 'Y 11.3.4 LO SOCIAL Y LO EDUCATIVO',
                      'items': ['Sociedad estamental basada en el origen '
                                'étnico: españoles, criollos, mestizos, '
                                'indígenas y negros.',
                                'La educación fue elitista. Se crearon '
                                'colegios especiales para hijos de caciques, '
                                'como el Colegio de San Borja en el Cusco.',
                                'La Universidad de San Marcos fue fundada en '
                                '1551 como Real y Pontificia Universidad, '
                                'nombrada así por el papa Pío V.',
                                'La Universidad de San Antonio Abad del '
                                'Cusco se originó en el seminario creado por '
                                'el obispo Antonio de la Raya.',
                                'El gestor de la creación de la Universidad '
                                'de San Antonio Abad fue el obispo Manuel de '
                                'Mollinedo y Angulo.',
                                'El papa Inocencio XII emitió en 1692 el '
                                'breve pontificio que creó la Universidad de '
                                'San Antonio Abad del Cusco.',
                                'El primer rector de la Universidad de San '
                                'Antonio Abad del Cusco fue el Dr. Juan '
                                'Cárdenas y Céspedes.']}],
  'qr_reto': [{'pregunta': 'El obispo que creó el seminario del que se '
                           'originó la Universidad de San Antonio Abad del '
                           'Cusco fue:',
               'respuesta': 'Antonio de la Raya'},
              {'pregunta': 'El principal centro minero de plata en el '
                           'virreinato fue:',
               'respuesta': 'Potosí'},
              {'pregunta': 'El primer rector de la Universidad de San '
                           'Antonio Abad del Cusco fue:',
               'respuesta': 'Juan Cárdenas y Céspedes'}],
  'qr_dato': 'El virrey Francisco de Toledo organizó el virreinato y creó '
             'las reducciones de indios.'},
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
                           'poder {absoluto}.']}],
  'cuadros': [{'titulo': '12.1 PENSADORES DE LA ILUSTRACIÓN',
               'encabezados': ['Pensador', 'Aporte principal'],
               'filas': [['{Montesquieu}', 'División de {poderes}'],
                         ['{Rousseau}',
                          '«El contrato social», {soberanía} popular'],
                         ['{Voltaire}',
                          'Defensa de la {tolerancia} religiosa']]}],
  'preguntas': [{'pregunta': 'La Ilustración corresponde al siglo:',
                 'alternativas': ['XVIII', 'XVI', 'XIX', 'XV', 'XVII'],
                 'correcta': 'A'},
                {'pregunta': 'La Ilustración es conocida también como:',
                 'alternativas': ['Barroco',
                                  'Siglo de las Luces',
                                  'Siglo de Oro',
                                  'Renacimiento',
                                  'Edad Moderna'],
                 'correcta': 'B'},
                {'pregunta': 'Para los ilustrados, la vida humana debía '
                             'guiarse por:',
                 'alternativas': ['La autoridad divina',
                                  'La tradición',
                                  'La costumbre',
                                  'La razón',
                                  'La fe'],
                 'correcta': 'D'},
                {'pregunta': 'La teoría de la división de poderes fue '
                             'formulada por:',
                 'alternativas': ['Rousseau',
                                  'Montesquieu',
                                  'Voltaire',
                                  'Locke',
                                  'Diderot'],
                 'correcta': 'B'},
                {'pregunta': 'El autor de «El contrato social» fue:',
                 'alternativas': ['Hume',
                                  'Montesquieu',
                                  'Kant',
                                  'Rousseau',
                                  'Voltaire'],
                 'correcta': 'D'},
                {'pregunta': 'El principio de la soberanía popular se '
                             'atribuye a:',
                 'alternativas': ['Bossuet',
                                  'Voltaire',
                                  'Montesquieu',
                                  'Adam Smith',
                                  'Rousseau'],
                 'correcta': 'E'},
                {'pregunta': 'Voltaire destacó especialmente por su defensa '
                             'de:',
                 'alternativas': ['La monarquía absoluta',
                                  'La tolerancia',
                                  'La censura',
                                  'El feudalismo',
                                  'El derecho divino'],
                 'correcta': 'B'},
                {'pregunta': 'El despotismo ilustrado se resume en la frase:',
                 'alternativas': ['«Dios lo quiere»',
                                  '«Todo para el pueblo, pero sin el pueblo»',
                                  '«Libertad, igualdad, fraternidad»',
                                  '«El Estado soy yo»',
                                  '«El poder al pueblo»'],
                 'correcta': 'B'},
                {'pregunta': 'El despotismo ilustrado mantuvo:',
                 'alternativas': ['La teocracia',
                                  'La república',
                                  'El poder absoluto del monarca',
                                  'La democracia parlamentaria',
                                  'El gobierno del pueblo'],
                 'correcta': 'C'},
                {'pregunta': 'Las ideas ilustradas influyeron directamente '
                             'en:',
                 'alternativas': ['La Independencia de Estados Unidos y la '
                                  'Revolución Francesa',
                                  'El feudalismo',
                                  'La caída de Constantinopla',
                                  'Las Cruzadas',
                                  'El descubrimiento de América'],
                 'correcta': 'A'},
                {'pregunta': 'Los ilustrados se opusieron principalmente a:',
                 'alternativas': ['La superstición y la tradición irracional',
                                  'La educación',
                                  'El comercio',
                                  'El progreso',
                                  'La razón y la ciencia'],
                 'correcta': 'A'},
                {'pregunta': 'Los monarcas del despotismo ilustrado '
                             'impulsaron reformas en:',
                 'alternativas': ['La creación de repúblicas',
                                  'El sistema electoral',
                                  'La separación Iglesia-Estado plena',
                                  'La abolición de la monarquía',
                                  'Educación, economía y administración'],
                 'correcta': 'E'},
                {'pregunta': 'La Ilustración cuestionó fundamentalmente el '
                             'poder basado en:',
                 'alternativas': ['Los tratados internacionales',
                                  'Los parlamentos',
                                  'El derecho divino de los reyes',
                                  'El voto popular',
                                  'Las constituciones'],
                 'correcta': 'C'},
                {'pregunta': 'El despotismo ilustrado puede definirse como '
                             'una forma de:',
                 'alternativas': ['Absolutismo con reformas ilustradas',
                                  'Democracia directa',
                                  'Federalismo',
                                  'Anarquía',
                                  'República parlamentaria'],
                 'correcta': 'A'},
                {'pregunta': 'La división de poderes propuesta comprende:',
                 'alternativas': ['Real, nobiliario y popular',
                                  'Central, regional y local',
                                  'Militar, civil y religioso',
                                  'Ejecutivo, legislativo y judicial',
                                  'Económico, político y social'],
                 'correcta': 'D'},
                {'pregunta': 'La Ilustración se desarrolló principalmente '
                             'en:',
                 'alternativas': ['Europa',
                                  'Oceanía',
                                  'África',
                                  'América',
                                  'Asia'],
                 'correcta': 'A'},
                {'pregunta': 'Los ilustrados confiaron en el progreso a '
                             'través de:',
                 'alternativas': ['La tradición',
                                  'La guerra',
                                  'La conquista',
                                  'La educación y la ciencia',
                                  'El aislamiento'],
                 'correcta': 'D'},
                {'pregunta': 'Una consecuencia política de la Ilustración '
                             'fue:',
                 'alternativas': ['El fortalecimiento del feudalismo',
                                  'El fin del comercio',
                                  'El retorno al imperio romano',
                                  'El cuestionamiento del absolutismo',
                                  'La expansión de la servidumbre'],
                 'correcta': 'D'},
                {'pregunta': '«El contrato social» plantea que el poder '
                             'emana de:',
                 'alternativas': ['El pueblo',
                                  'Dios',
                                  'La Iglesia',
                                  'La nobleza',
                                  'El ejército'],
                 'correcta': 'A'},
                {'pregunta': 'El pensamiento ilustrado se difundió '
                             'principalmente a través de:',
                 'alternativas': ['Los torneos',
                                  'Los gremios',
                                  'Los libros, salones y la Enciclopedia',
                                  'Las cruzadas',
                                  'Los sermones'],
                 'correcta': 'C'},
                {'pregunta': 'Las intendencias en la Colonia fueron creadas '
                             'en el reinado de: (UNSAAC Ordinario)',
                 'alternativas': ['Carlos III',
                                  'Carlos IV',
                                  'Carlos V',
                                  'Carlos VII',
                                  'Carlos I'],
                 'correcta': 'A'},
                {'pregunta': 'Una de las reformas político-administrativas '
                             'más importantes de Carlos III en '
                             'hispanoamérica fue: (UNSAAC Ordinario)',
                 'alternativas': ['El censo de la población de Mitaya',
                                  'La implementación de la aduana',
                                  'La creación del Virreinato de Río de la '
                                  'Plata',
                                  'El incremento de la alcabala',
                                  'La extensión del tributo a los caciques'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'LA ILUSTRACIÓN',
                      'items': ['Movimiento intelectual del siglo XVIII, '
                                'llamado también «Siglo de las Luces».',
                                'Sostuvo que la razón debía guiar la vida '
                                'humana, por encima de la tradición y la '
                                'superstición.',
                                'Principales pensadores: Montesquieu, autor '
                                'de la división de poderes; Rousseau, autor '
                                'de «El contrato social» y la soberanía '
                                'popular; Voltaire, defensor de la '
                                'tolerancia.',
                                'Sus ideas influyeron directamente en la '
                                'Independencia de Estados Unidos y en la '
                                'Revolución Francesa.']},
                     {'titulo': 'EL DESPOTISMO ILUSTRADO',
                      'items': ['Forma de gobierno absolutista que adoptó '
                                'algunas ideas ilustradas sin ceder el '
                                'poder.',
                                'Se resume en la frase: «Todo para el '
                                'pueblo, pero sin el pueblo».',
                                'Los monarcas impulsaron reformas en '
                                'educación, economía y administración, pero '
                                'mantuvieron el poder absoluto.']}],
  'qr_reto': [{'pregunta': 'El autor de «El contrato social» fue:',
               'respuesta': 'Rousseau'},
              {'pregunta': 'Las intendencias en la Colonia fueron creadas en '
                           'el reinado de:',
               'respuesta': 'Carlos III'},
              {'pregunta': 'La teoría de la división de poderes fue '
                           'formulada por:',
               'respuesta': 'Montesquieu'}],
  'qr_dato': 'Se resume en la frase: «Todo para el pueblo, pero sin el '
             'pueblo».'},
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
                {'titulo': '13.3 LA REVOLUCIÓN DE TÚPAC AMARU II: OTROS '
                           'DATOS',
                 'items': ['{Micaela Bastidas} fue esposa y colíder de Túpac '
                           'Amaru II; fue traicionada por {Ventura '
                           'Landaeta}.',
                           'El corregidor {Antonio de Arriaga}, capturado al '
                           'inicio de la rebelión, fue ejecutado por el '
                           'zambo {Antonio Oblitas}, su antiguo esclavo.',
                           'Túpac Amaru II proclamó la libertad de los '
                           'esclavos negros el {16} de noviembre de {1780}.',
                           'Tras la rebelión, se prohibió la difusión de los '
                           '{Comentarios Reales} del Inca Garcilaso de la '
                           'Vega.',
                           'Túpac Amaru II era descendiente de {Felipe Túpac '
                           'Amaru}, el último inca de {Vilcabamba}.']}],
  'cuadros': [{'titulo': '13.2 ETAPAS DE LA REVOLUCIÓN DE TÚPAC AMARU II',
               'encabezados': ['Etapa', 'Hecho'],
               'filas': [['Inicio',
                          'Captura del corregidor {Arriaga} ({1780})'],
                         ['Triunfo', 'Batalla de {Sangarará}'],
                         ['Derrota', 'Batallas de {Checacupe} y Tinta'],
                         ['Final', 'Ejecución en el Cusco ({1781})']]}],
  'preguntas': [{'pregunta': 'Las reformas borbónicas fueron aplicadas por '
                             'la dinastía de los:',
                 'alternativas': ['Borbones',
                                  'Saboya',
                                  'Braganza',
                                  'Trastámara',
                                  'Habsburgo'],
                 'correcta': 'A'},
                {'pregunta': 'Las intendencias reemplazaron a:',
                 'alternativas': ['Los corregimientos',
                                  'Las audiencias',
                                  'Las encomiendas',
                                  'Los virreinatos',
                                  'Los cabildos'],
                 'correcta': 'A'},
                {'pregunta': 'Una consecuencia territorial de las reformas '
                             'borbónicas fue:',
                 'alternativas': ['La creación de los virreinatos de Nueva '
                                  'Granada y del Río de la Plata',
                                  'La ampliación del virreinato peruano',
                                  'La anexión de Chile',
                                  'La creación de la Capitanía de Cuba',
                                  'La independencia de México'],
                 'correcta': 'A'},
                {'pregunta': 'Las reformas borbónicas desplazaron de los '
                             'cargos públicos a los:',
                 'alternativas': ['Peninsulares',
                                  'Criollos',
                                  'Indígenas',
                                  'Esclavos',
                                  'Mestizos'],
                 'correcta': 'B'},
                {'pregunta': 'La rebelión de Juan Santos Atahualpa se inició '
                             'en el año:',
                 'alternativas': ['1780', '1781', '1814', '1821', '1742'],
                 'correcta': 'E'},
                {'pregunta': 'Juan Santos Atahualpa desarrolló su rebelión '
                             'en:',
                 'alternativas': ['Lima',
                                  'La selva central',
                                  'El altiplano',
                                  'La costa norte',
                                  'El Cusco'],
                 'correcta': 'B'},
                {'pregunta': 'Un rasgo singular de la rebelión de Juan '
                             'Santos Atahualpa fue que:',
                 'alternativas': ['Fue pacífica',
                                  'Nunca fue derrotada militarmente',
                                  'Contó con apoyo español',
                                  'Fue rápidamente sofocada',
                                  'Se limitó a la costa'],
                 'correcta': 'B'},
                {'pregunta': 'El verdadero nombre de Túpac Amaru II fue:',
                 'alternativas': ['Mateo Pumacahua',
                                  'Francisco Santa Cruz',
                                  'José Gabriel Condorcanqui',
                                  'Juan Santos Atahualpa',
                                  'Diego Cristóbal Túpac Amaru'],
                 'correcta': 'C'},
                {'pregunta': 'La revolución de Túpac Amaru II se inició con '
                             'la captura del corregidor:',
                 'alternativas': ['Antonio de Arriaga',
                                  "Ambrosio O'Higgins",
                                  'Francisco Santa Cruz',
                                  'José Antonio de Areche',
                                  'Agustín de Jáuregui'],
                 'correcta': 'A'},
                {'pregunta': 'La revolución de Túpac Amaru II se inició el:',
                 'alternativas': ['1 de agosto de 1814',
                                  '28 de julio de 1821',
                                  '4 de noviembre de 1780',
                                  '18 de mayo de 1781',
                                  '9 de diciembre de 1824'],
                 'correcta': 'C'},
                {'pregunta': 'Túpac Amaru II obtuvo su principal victoria en '
                             'la batalla de:',
                 'alternativas': ['Ayacucho',
                                  'Sangarará',
                                  'Checacupe',
                                  'Junín',
                                  'Tinta'],
                 'correcta': 'B'},
                {'pregunta': 'Túpac Amaru II fue ejecutado en la plaza del '
                             'Cusco el:',
                 'alternativas': ['6 de agosto de 1824',
                                  '28 de julio de 1821',
                                  '2 de enero de 1782',
                                  '4 de noviembre de 1780',
                                  '18 de mayo de 1781'],
                 'correcta': 'E'},
                {'pregunta': 'Entre las causas de la revolución de Túpac '
                             'Amaru II NO figura:',
                 'alternativas': ['La abolición de la esclavitud',
                                  'Los abusos de los corregidores',
                                  'Las reformas borbónicas',
                                  'Los repartos mercantiles',
                                  'La mita de Potosí'],
                 'correcta': 'A'},
                {'pregunta': 'Una consecuencia cultural de la derrota de '
                             'Túpac Amaru II fue:',
                 'alternativas': ['La difusión del quechua',
                                  'La prohibición del quechua en documentos '
                                  'y de los Comentarios Reales',
                                  'El reconocimiento de la nobleza inca',
                                  'La creación de escuelas indígenas',
                                  'La libertad de imprenta'],
                 'correcta': 'B'},
                {'pregunta': 'Túpac Amaru II era cacique de:',
                 'alternativas': ['Acos',
                                  'Tungasuca',
                                  'Azángaro',
                                  'Lampa',
                                  'Chincheros'],
                 'correcta': 'B'},
                {'pregunta': 'La obra prohibida tras la rebelión, escrita '
                             'por el Inca Garcilaso, fue:',
                 'alternativas': ['Los Comentarios Reales',
                                  'Relación de antigüedades',
                                  'Historia del Nuevo Mundo',
                                  'Nueva Crónica y Buen Gobierno',
                                  'La Crónica del Perú'],
                 'correcta': 'A'},
                {'pregunta': 'El impuesto colonial incrementado por las '
                             'reformas borbónicas fue:',
                 'alternativas': ['La alcabala',
                                  'El diezmo',
                                  'El almojarifazgo',
                                  'La primicia',
                                  'El quinto real'],
                 'correcta': 'A'},
                {'pregunta': 'Túpac Amaru II fue entregado a los españoles '
                             'por la traición de:',
                 'alternativas': ['Diego Cristóbal',
                                  'Mateo Pumacahua',
                                  'Micaela Bastidas',
                                  'Francisco Santa Cruz',
                                  'Antonio de Arriaga'],
                 'correcta': 'D'},
                {'pregunta': 'Las reformas borbónicas tuvieron como objetivo '
                             'principal:',
                 'alternativas': ['Recuperar el control económico y político '
                                  'de las colonias',
                                  'Fundar universidades',
                                  'Otorgar autonomía a las colonias',
                                  'Promover la independencia',
                                  'Abolir la esclavitud'],
                 'correcta': 'A'},
                {'pregunta': 'Juan Santos Atahualpa se proclamó descendiente '
                             'de:',
                 'alternativas': ['Los curacas costeños',
                                  'Los chimúes',
                                  'Los incas',
                                  'Los chancas',
                                  'Los reyes españoles'],
                 'correcta': 'C'},
                {'pregunta': 'La esposa y colíder de Túpac Amaru II en la '
                             'revolución fue:',
                 'alternativas': ['Cecilia Túpac Amaru',
                                  'Micaela Bastidas',
                                  'Bartolina Sisa',
                                  'Tomasa Titu Condemayta',
                                  'Marcela Castro'],
                 'correcta': 'B'},
                {'pregunta': 'Micaela Bastidas fue traicionada y capturada '
                             'por:',
                 'alternativas': ['Francisco Santa Cruz',
                                  'Ventura Landaeta',
                                  'Antonio de Arriaga',
                                  'Antonio Oblitas',
                                  'José Antonio de Areche'],
                 'correcta': 'B'},
                {'pregunta': 'El corregidor Antonio de Arriaga fue ejecutado '
                             'por:',
                 'alternativas': ['Micaela Bastidas',
                                  'Antonio Oblitas, su antiguo esclavo',
                                  'Francisco Santa Cruz',
                                  'Ventura Landaeta',
                                  'Diego Cristóbal Túpac Amaru'],
                 'correcta': 'B'},
                {'pregunta': 'Túpac Amaru II proclamó la libertad de los '
                             'esclavos negros el 16 de noviembre de:',
                 'alternativas': ['1778', '1780', '1781', '1783', '1776'],
                 'correcta': 'B'},
                {'pregunta': 'Tras la rebelión de Túpac Amaru II, la Corona '
                             'prohibió la difusión de una obra escrita por '
                             'el Inca Garcilaso de la Vega llamada:',
                 'alternativas': ['La Florida del Inca',
                                  'Los Comentarios Reales',
                                  'Historia General del Perú',
                                  'Suma y Narración de los Incas',
                                  'Nueva Corónica'],
                 'correcta': 'B'},
                {'pregunta': 'Túpac Amaru II era descendiente del último '
                             'inca de Vilcabamba, llamado:',
                 'alternativas': ['Manco Inca',
                                  'Felipe Túpac Amaru',
                                  'Sayri Túpac',
                                  'Titu Cusi Yupanqui',
                                  'Huáscar'],
                 'correcta': 'B'},
                {'pregunta': 'El movimiento liderado por Túpac Amaru II se '
                             'produjo en el siglo: (UNSAAC Ordinario)',
                 'alternativas': ['XVI', 'XVIII', 'XVII', 'XV', 'XIX'],
                 'correcta': 'B'},
                {'pregunta': 'Una consecuencia de la Revolución de Tupac '
                             'Amaru II fue la creación de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Las Juntas de Gobierno',
                                  'Los corregimientos',
                                  'Los nuevos virreinatos',
                                  'Los departamentos',
                                  'Las intendencias'],
                 'correcta': 'E'},
                {'pregunta': 'La revolución de José Gabriel Túpac Amaru '
                             'inició como: (UNSAAC Ordinario)',
                 'alternativas': ['Independentista - Separatista',
                                  'Emancipacionista - Reformista',
                                  'Separatista - Emancipacionista',
                                  'Reformista - Independentista',
                                  'Reformista - Separatista'],
                 'correcta': 'D'},
                {'pregunta': 'Durante la fase cusqueña, Túpac Amaru II '
                             'venció a los españoles en la batalla de: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Quiquijana',
                                  'Sangarará',
                                  'Checacupe',
                                  'Combapata',
                                  'Tinta'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'LAS REFORMAS BORBÓNICAS',
                      'items': ['Conjunto de medidas aplicadas por la '
                                'dinastía de los Borbones en el siglo XVIII '
                                'para recuperar el control económico y '
                                'político de las colonias.',
                                'Se crearon las intendencias, que '
                                'reemplazaron a los corregimientos.',
                                'Se crearon los virreinatos de Nueva Granada '
                                'y del Río de la Plata, reduciendo el '
                                'territorio del virreinato peruano.',
                                'Se incrementaron los impuestos, como la '
                                'alcabala, y se estableció el libre comercio '
                                'entre puertos españoles.',
                                'Se desplazó a los criollos de los cargos '
                                'públicos, prefiriendo a los peninsulares, '
                                'lo que generó gran descontento.']},
                     {'titulo': 'REBELIÓN DE JUAN SANTOS ATAHUALPA',
                      'items': ['Se desarrolló desde 1742 en la selva '
                                'central (Gran Pajonal, Chanchamayo).',
                                'Se proclamó descendiente de los incas y '
                                'buscó expulsar a los españoles y restaurar '
                                'el Tahuantinsuyo.',
                                'Su rebelión nunca fue derrotada '
                                'militarmente; su desaparición sigue siendo '
                                'un misterio.']},
                     {'titulo': 'LA REVOLUCIÓN DE TÚPAC AMARU II',
                      'items': ['José Gabriel Condorcanqui, cacique de '
                                'Tungasuca, inició la rebelión el 4 de '
                                'noviembre de 1780 con la captura del '
                                'corregidor Antonio de Arriaga.',
                                'Causas: los repartos mercantiles, la mita '
                                'de Potosí, los abusos de los corregidores y '
                                'las reformas borbónicas.',
                                'Triunfó en la batalla de Sangarará, pero '
                                'fue derrotado en Checacupe y Tinta.',
                                'Fue traicionado por Francisco Santa Cruz y '
                                'ejecutado en la plaza del Cusco el 18 de '
                                'mayo de 1781.',
                                'Consecuencias: se prohibió el uso del '
                                'quechua en documentos, los títulos de '
                                'nobleza indígena y los Comentarios Reales '
                                'del Inca Garcilaso.']},
                     {'titulo': 'LA REVOLUCIÓN DE TÚPAC AMARU II: OTROS '
                                'DATOS',
                      'items': ['Micaela Bastidas fue esposa y colíder de '
                                'Túpac Amaru II; fue traicionada por Ventura '
                                'Landaeta.',
                                'El corregidor Antonio de Arriaga, capturado '
                                'al inicio de la rebelión, fue ejecutado por '
                                'el zambo Antonio Oblitas, su antiguo '
                                'esclavo.',
                                'Túpac Amaru II proclamó la libertad de los '
                                'esclavos negros el 16 de noviembre de 1780.',
                                'Tras la rebelión, se prohibió la difusión '
                                'de los Comentarios Reales del Inca '
                                'Garcilaso de la Vega.',
                                'Túpac Amaru II era descendiente de Felipe '
                                'Túpac Amaru, el último inca de '
                                'Vilcabamba.']}],
  'qr_reto': [{'pregunta': 'Micaela Bastidas fue traicionada y capturada '
                           'por:',
               'respuesta': 'Ventura Landaeta'},
              {'pregunta': 'Las reformas borbónicas tuvieron como objetivo '
                           'principal:',
               'respuesta': 'Recuperar el control económico y político de '
                            'las colonias'},
              {'pregunta': 'Una consecuencia cultural de la derrota de Túpac '
                           'Amaru II fue:',
               'respuesta': 'La prohibición del quechua en documentos y de '
                            'los Comentarios Reales'}],
  'qr_dato': 'Micaela Bastidas fue esposa y colíder de Túpac Amaru II; fue '
             'traicionada por Ventura Landaeta.'},
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
                           '{liberales} por Europa y América.']}],
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
                 'alternativas': ['Diez', 'Quince', 'Once', 'Trece', 'Doce'],
                 'correcta': 'D'},
                {'pregunta': 'La Declaración de Independencia de Estados '
                             'Unidos se firmó el:',
                 'alternativas': ['1 de enero de 1800',
                                  '28 de julio de 1821',
                                  '14 de julio de 1789',
                                  '9 de diciembre de 1824',
                                  '4 de julio de 1776'],
                 'correcta': 'E'},
                {'pregunta': 'El principal redactor de la Declaración de '
                             'Independencia norteamericana fue:',
                 'alternativas': ['George Washington',
                                  'Thomas Jefferson',
                                  'Benjamin Franklin',
                                  'Alexander Hamilton',
                                  'John Adams'],
                 'correcta': 'B'},
                {'pregunta': 'El primer presidente de Estados Unidos fue:',
                 'alternativas': ['Thomas Jefferson',
                                  'John Adams',
                                  'James Madison',
                                  'George Washington',
                                  'Benjamin Franklin'],
                 'correcta': 'D'},
                {'pregunta': 'El lema «no hay impuestos sin representación» '
                             'corresponde a:',
                 'alternativas': ['La Revolución Francesa',
                                  'La independencia de Estados Unidos',
                                  'La Ilustración',
                                  'La independencia del Perú',
                                  'Las reformas borbónicas'],
                 'correcta': 'B'},
                {'pregunta': 'El hecho que precipitó la rebelión de las '
                             'colonias inglesas fue:',
                 'alternativas': ['La batalla de Waterloo',
                                  'El Motín del Té de Boston',
                                  'La Paz de Westfalia',
                                  'La toma de la Bastilla',
                                  'El bloqueo continental'],
                 'correcta': 'B'},
                {'pregunta': 'La Revolución Francesa se inició en el año:',
                 'alternativas': ['1810', '1804', '1789', '1799', '1776'],
                 'correcta': 'C'},
                {'pregunta': 'El hecho simbólico del inicio de la Revolución '
                             'Francesa fue:',
                 'alternativas': ['La ejecución de Luis XVI',
                                  'El golpe de Napoleón',
                                  'La huida a Varennes',
                                  'La reunión de los Estados Generales',
                                  'La toma de la Bastilla'],
                 'correcta': 'E'},
                {'pregunta': 'El lema de la Revolución Francesa fue:',
                 'alternativas': ['«Paz, orden y progreso»',
                                  '«No hay impuestos sin representación»',
                                  '«Libertad, igualdad, fraternidad»',
                                  '«El Estado soy yo»',
                                  '«Todo para el pueblo, sin el pueblo»'],
                 'correcta': 'C'},
                {'pregunta': 'El documento fundamental proclamado por la '
                             'Revolución Francesa fue:',
                 'alternativas': ['Las Siete Partidas',
                                  'La Declaración de los Derechos del Hombre '
                                  'y del Ciudadano',
                                  'El Bill of Rights',
                                  'La Carta Magna',
                                  'El Código de Hammurabi'],
                 'correcta': 'B'},
                {'pregunta': 'La etapa del Terror durante la Revolución '
                             'Francesa estuvo dirigida por:',
                 'alternativas': ['Lafayette',
                                  'Robespierre',
                                  'Napoleón',
                                  'Danton exclusivamente',
                                  'Luis XVI'],
                 'correcta': 'B'},
                {'pregunta': 'El Directorio francés terminó con:',
                 'alternativas': ['La restauración borbónica',
                                  'La ejecución de Robespierre',
                                  'La toma de la Bastilla',
                                  'El golpe de Estado de Napoleón',
                                  'La batalla de Waterloo'],
                 'correcta': 'D'},
                {'pregunta': 'Una consecuencia política central de la '
                             'Revolución Francesa fue:',
                 'alternativas': ['El retorno de la monarquía absoluta '
                                  'permanente',
                                  'La expansión de la servidumbre',
                                  'El fin del absolutismo y del régimen '
                                  'feudal',
                                  'El fortalecimiento del absolutismo',
                                  'La restauración del feudalismo'],
                 'correcta': 'C'},
                {'pregunta': 'La independencia de Estados Unidos influyó en '
                             'Hispanoamérica al:',
                 'alternativas': ['Abolir la esclavitud',
                                  'Financiar los ejércitos libertadores',
                                  'Enviar tropas al Perú',
                                  'Firmar tratados de alianza',
                                  'Servir de ejemplo a los movimientos '
                                  'independentistas'],
                 'correcta': 'E'},
                {'pregunta': 'El sistema de gobierno adoptado por Estados '
                             'Unidos fue:',
                 'alternativas': ['Confederación monárquica',
                                  'Imperio',
                                  'República federal y presidencialista',
                                  'Monarquía constitucional',
                                  'República parlamentaria'],
                 'correcta': 'C'},
                {'pregunta': 'Entre las causas de la Revolución Francesa '
                             'figura:',
                 'alternativas': ['La expansión colonial',
                                  'La ausencia de impuestos',
                                  'La desigualdad entre los estamentos',
                                  'La unidad social',
                                  'La abundancia económica'],
                 'correcta': 'C'},
                {'pregunta': 'La corriente de pensamiento que influyó '
                             'decisivamente en ambas revoluciones fue:',
                 'alternativas': ['El Romanticismo',
                                  'El Positivismo',
                                  'La Escolástica',
                                  'La Ilustración',
                                  'El Renacimiento'],
                 'correcta': 'D'},
                {'pregunta': 'La toma de la Bastilla ocurrió el:',
                 'alternativas': ['9 de diciembre',
                                  '14 de julio',
                                  '4 de julio',
                                  '28 de julio',
                                  '1 de mayo'],
                 'correcta': 'B'},
                {'pregunta': 'El órgano revolucionario francés que juzgó y '
                             'ejecutó al rey fue:',
                 'alternativas': ['El Consulado',
                                  'El Directorio',
                                  'La Asamblea Nacional',
                                  'Los Estados Generales',
                                  'La Convención'],
                 'correcta': 'E'},
                {'pregunta': 'La sociedad francesa previa a la revolución '
                             'estaba dividida en:',
                 'alternativas': ['Tres estamentos',
                                  'Sin divisiones legales',
                                  'Cinco estamentos',
                                  'Dos clases',
                                  'Cuatro castas'],
                 'correcta': 'A'},
                {'pregunta': 'El reconocimiento de la independencia de las '
                             'Trece Colonias de Norte América, por el Rey '
                             'Jorge III, se estableció en el Tratado de: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Lexington',
                                  'Filadelfia',
                                  'Yorktown',
                                  'Saratoga',
                                  'Versalles'],
                 'correcta': 'E'},
                {'pregunta': 'La búsqueda de igualdad de poderes: Ejecutivo, '
                             'Legislativo y Judicial surge a consecuencia '
                             'de: (UNSAAC Ordinario)',
                 'alternativas': ['Independencia de las Trece Colonias',
                                  'Tratado de Versalles',
                                  'Revolución Francesa',
                                  'Primera guerra mundial',
                                  'Segunda guerra mundial'],
                 'correcta': 'C'},
                {'pregunta': 'Una de las consecuencias de la Revolución '
                             'Francesa fue: (UNSAAC Ordinario)',
                 'alternativas': ['El desarrollo económico del imperialismo '
                                  'inglés',
                                  'La destrucción del régimen feudal en '
                                  'Francia',
                                  'La creación de los estados independistas '
                                  'en Europa del Norte',
                                  'El triunfo en la Batalla de Saratoga',
                                  'La creación del sistema de gobierno '
                                  'dictatorial'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'INDEPENDENCIA DE ESTADOS UNIDOS',
                      'items': ['Las trece colonias inglesas de Norteamérica '
                                'se rebelaron contra la metrópoli.',
                                'Causas: los impuestos sin representación '
                                'política —«no hay impuestos sin '
                                'representación»— y el Motín del Té de '
                                'Boston.',
                                'La Declaración de Independencia se firmó el '
                                '4 de julio de 1776; su principal redactor '
                                'fue Thomas Jefferson.',
                                'El primer presidente fue George Washington. '
                                'Se estableció una república federal y '
                                'presidencialista.',
                                'Consecuencia: sirvió de ejemplo a los '
                                'movimientos independentistas de '
                                'Hispanoamérica.']},
                     {'titulo': 'LA REVOLUCIÓN FRANCESA',
                      'items': ['Se inició en 1789 con la toma de la '
                                'Bastilla el 14 de julio.',
                                'Causas: la crisis económica, la desigualdad '
                                'de los estamentos y la influencia de la '
                                'Ilustración.',
                                'Etapas: la Asamblea Nacional, la Convención '
                                '(con el Terror y Robespierre) y el '
                                'Directorio, que terminó con el golpe de '
                                'Napoleón.',
                                'Su lema fue «Libertad, igualdad, '
                                'fraternidad» y proclamó la Declaración de '
                                'los Derechos del Hombre y del Ciudadano.',
                                'Consecuencias: fin del absolutismo y del '
                                'régimen feudal, y difusión de las ideas '
                                'liberales por Europa y América.']}],
  'qr_reto': [{'pregunta': 'El número de colonias inglesas que se '
                           'independizaron en Norteamérica fue:',
               'respuesta': 'Trece'},
              {'pregunta': 'La Revolución Francesa se inició en el año:',
               'respuesta': '1789'},
              {'pregunta': 'El Directorio francés terminó con:',
               'respuesta': 'El golpe de Estado de Napoleón'}],
  'qr_dato': 'Causas: los impuestos sin representación política —«no hay '
             'impuestos sin representación»— y el Motín del Té de Boston.'},
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
                           'virrey {José de la Serna}.']}],
  'cuadros': [{'titulo': '15. BATALLAS DECISIVAS',
               'encabezados': ['Batalla', 'Fecha', 'Jefe patriota'],
               'filas': [['{Junín}', '{6} agosto 1824', '{Bolívar}'],
                         ['{Ayacucho}', '{9} diciembre 1824', '{Sucre}']]}],
  'preguntas': [{'pregunta': 'La invasión napoleónica a España se produjo '
                             'en:',
                 'alternativas': ['1820', '1812', '1789', '1808', '1824'],
                 'correcta': 'D'},
                {'pregunta': 'Napoleón colocó en el trono español a:',
                 'alternativas': ['Fernando VII',
                                  'Carlos IV',
                                  'Godoy',
                                  'José Bonaparte',
                                  'Luis XVIII'],
                 'correcta': 'D'},
                {'pregunta': 'La Constitución liberal española de 1812 se '
                             'conoce como Constitución de:',
                 'alternativas': ['Madrid',
                                  'Cádiz',
                                  'Sevilla',
                                  'Aranjuez',
                                  'Bayona'],
                 'correcta': 'B'},
                {'pregunta': 'San Martín desembarcó en el Perú en la bahía '
                             'de:',
                 'alternativas': ['Pisco',
                                  'Ancón',
                                  'Callao',
                                  'Paracas',
                                  'Huacho'],
                 'correcta': 'D'},
                {'pregunta': 'El desembarco de San Martín en el Perú ocurrió '
                             'el:',
                 'alternativas': ['28 de julio de 1821',
                                  '9 de diciembre de 1824',
                                  '8 de septiembre de 1820',
                                  '20 de septiembre de 1822',
                                  '6 de agosto de 1824'],
                 'correcta': 'C'},
                {'pregunta': 'La Independencia del Perú fue proclamada el:',
                 'alternativas': ['9 de diciembre de 1824',
                                  '6 de agosto de 1824',
                                  '8 de septiembre de 1820',
                                  '4 de julio de 1776',
                                  '28 de julio de 1821'],
                 'correcta': 'E'},
                {'pregunta': 'San Martín asumió el gobierno del Perú con el '
                             'título de:',
                 'alternativas': ['Libertador',
                                  'Dictador',
                                  'Protector',
                                  'Presidente',
                                  'Virrey'],
                 'correcta': 'C'},
                {'pregunta': 'Institución cultural creada por San Martín:',
                 'alternativas': ['El Museo Nacional',
                                  'La Biblioteca Nacional',
                                  'El Archivo General',
                                  'La Universidad de San Marcos',
                                  'La Academia de la Lengua'],
                 'correcta': 'B'},
                {'pregunta': 'La conferencia entre San Martín y Bolívar se '
                             'realizó en:',
                 'alternativas': ['Quito',
                                  'Lima',
                                  'Guayaquil',
                                  'Trujillo',
                                  'Bogotá'],
                 'correcta': 'C'},
                {'pregunta': 'Bolívar llegó al Perú en el año:',
                 'alternativas': ['1820', '1821', '1822', '1824', '1823'],
                 'correcta': 'E'},
                {'pregunta': 'La batalla de Junín se libró el:',
                 'alternativas': ['28 de julio de 1821',
                                  '2 de mayo de 1866',
                                  '8 de septiembre de 1820',
                                  '9 de diciembre de 1824',
                                  '6 de agosto de 1824'],
                 'correcta': 'E'},
                {'pregunta': 'Un rasgo distintivo de la batalla de Junín fue '
                             'que:',
                 'alternativas': ['Duró tres días',
                                  'Participó la marina',
                                  'Se libró sin usar armas de fuego',
                                  'Se realizó de noche',
                                  'Intervino artillería pesada'],
                 'correcta': 'C'},
                {'pregunta': 'La batalla de Ayacucho fue dirigida por:',
                 'alternativas': ['Simón Bolívar',
                                  'La Mar',
                                  'San Martín',
                                  'Santa Cruz',
                                  'Antonio José de Sucre'],
                 'correcta': 'E'},
                {'pregunta': 'La batalla de Ayacucho se libró el:',
                 'alternativas': ['6 de agosto de 1824',
                                  '9 de diciembre de 1824',
                                  '28 de julio de 1821',
                                  '20 de enero de 1825',
                                  '3 de octubre de 1824'],
                 'correcta': 'B'},
                {'pregunta': 'La Capitulación de Ayacucho fue firmada por el '
                             'virrey:',
                 'alternativas': ['José de la Serna',
                                  "O'Higgins",
                                  'Abascal',
                                  'Toledo',
                                  'Pezuela'],
                 'correcta': 'A'},
                {'pregunta': 'Antes de llegar al Perú, San Martín liberó:',
                 'alternativas': ['Chile',
                                  'Bolivia',
                                  'Venezuela',
                                  'Colombia',
                                  'Ecuador'],
                 'correcta': 'A'},
                {'pregunta': 'Ante el vacío de poder por la invasión '
                             'napoleónica se formaron:',
                 'alternativas': ['Los virreinatos',
                                  'Las audiencias',
                                  'Las juntas de gobierno',
                                  'Los cabildos abiertos únicamente',
                                  'Las intendencias'],
                 'correcta': 'C'},
                {'pregunta': 'Bolívar recibió en el Perú poderes de:',
                 'alternativas': ['Regente',
                                  'Gobernador',
                                  'Protector',
                                  'Dictador',
                                  'Presidente constitucional'],
                 'correcta': 'D'},
                {'pregunta': 'La proclamación de la Independencia se realizó '
                             'en:',
                 'alternativas': ['Huaura',
                                  'La plaza de armas de Lima',
                                  'El Cusco',
                                  'Pisco',
                                  'Trujillo'],
                 'correcta': 'B'},
                {'pregunta': 'La batalla que selló definitivamente la '
                             'independencia del Perú fue:',
                 'alternativas': ['Chacabuco',
                                  'Maipú',
                                  'Ayacucho',
                                  'Junín',
                                  'Pichincha'],
                 'correcta': 'C'},
                {'pregunta': 'El Acta de la Independencia del Perú en 1821 '
                             'fue redactada por: (UNSAAC Ordinario)',
                 'alternativas': ['Manuel Pérez de Tudela',
                                  'José de San Martín',
                                  'Francisco Javier de Luna Pizarro',
                                  'Faustino Sánchez Carrión',
                                  'Francisco Javier Mariátegui'],
                 'correcta': 'A'},
                {'pregunta': 'Simón Bolívar, antes de llegar al Perú, '
                             'independizó Venezuela con la Batalla de: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Pichincha',
                                  'Cancha Rayada',
                                  'Boyacá',
                                  'Carabobo',
                                  'Chacabuco'],
                 'correcta': 'D'},
                {'pregunta': 'Las juntas de Gobierno en América Hispana se '
                             'formaron a consecuencia de: (UNSAAC Ordinario)',
                 'alternativas': ['La vuelta del rey derrotado al trono de '
                                  'España',
                                  'El cautiverio del Rey de España',
                                  'La promulgación de la constitución de '
                                  'Cádiz en 1812',
                                  'Las guerras de independencia del Perú',
                                  'El pronunciamiento del virrey Francisco '
                                  'de Abascal'],
                 'correcta': 'B'},
                {'pregunta': 'La independencia de Venezuela se logró en la '
                             'batalla de: (UNSAAC Ordinario)',
                 'alternativas': ['Maipú',
                                  'Boyacá',
                                  'Cancha Rayada',
                                  'Pichincha',
                                  'Carabobo'],
                 'correcta': 'E'},
                {'pregunta': 'El establecimiento de la Junta de Gobierno en '
                             'Lima no fue posible, debido a la acción del '
                             'Virrey: (UNSAAC Ordinario)',
                 'alternativas': ['José de la Serna',
                                  'Francisco de Toledo',
                                  'Joaquín de La Pezuela',
                                  'Agustín de Jáuregui',
                                  'Fernando de Abascal y Sousa'],
                 'correcta': 'E'},
                {'pregunta': 'En la coyuntura internacional que España '
                             'afrontó para la formación de las Juntas de '
                             'Gobierno en Hispanoamérica, fue debido a: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['La declaración de guerra de Napoleón '
                                  'Bonaparte',
                                  'La revolución burguesa en España',
                                  'La invasión de Napoleón a España',
                                  'Inicios de la Primera Revolución '
                                  'Industrial',
                                  'La invasión de Napoleón a Portugal'],
                 'correcta': 'C'},
                {'pregunta': 'Simón Bolívar llegó al Perú el año 1823 y '
                             'estableció su cuartel general en: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Pativilca',
                                  'Huaura',
                                  'Cajamarca',
                                  'Chota',
                                  'Cutervo'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'AL 15.4 LA CRISIS DE ESPAÑA',
                      'items': ['En 1808 Napoleón invadió España y colocó en '
                                'el trono a su hermano José Bonaparte.',
                                'Ante el vacío de poder se formaron las '
                                'juntas de gobierno, primero en España y '
                                'luego en América.',
                                'En 1812 se promulgó la Constitución de '
                                'Cádiz, de carácter liberal.']},
                     {'titulo': 'LA CORRIENTE LIBERTADORA DEL SUR',
                      'items': ['José de San Martín desembarcó en la bahía '
                                'de Paracas el 8 de septiembre de 1820.',
                                'Antes realizó el cruce de los Andes y '
                                'liberó Chile con la batalla de Maipú.',
                                'Proclamó la Independencia del Perú en la '
                                'plaza de armas de Lima el 28 de julio de '
                                '1821.',
                                'Asumió el gobierno con el título de '
                                'Protector y creó la Biblioteca Nacional y '
                                'la Sociedad Patriótica.']},
                     {'titulo': 'LA CONSOLIDACIÓN CON BOLÍVAR',
                      'items': ['Tras la Conferencia de Guayaquil (1822) '
                                'entre San Martín y Bolívar, el primero se '
                                'retiró.',
                                'Simón Bolívar llegó al Perú en 1823 y '
                                'recibió poderes de dictador.',
                                'Batalla de Junín (6 de agosto de 1824): '
                                'victoria de la caballería patriota, sin uso '
                                'de armas de fuego.',
                                'Batalla de Ayacucho (9 de diciembre de '
                                '1824): dirigida por Antonio José de Sucre; '
                                'selló la independencia.',
                                'La Capitulación de Ayacucho fue firmada por '
                                'el virrey José de la Serna.']}],
  'qr_reto': [{'pregunta': 'La batalla de Ayacucho se libró el:',
               'respuesta': '9 de diciembre de 1824'},
              {'pregunta': 'Antes de llegar al Perú, San Martín liberó:',
               'respuesta': 'Chile'},
              {'pregunta': 'La independencia de Venezuela se logró en la '
                           'batalla de:',
               'respuesta': 'Carabobo'}],
  'qr_dato': 'Proclamó la Independencia del Perú en la plaza de armas de '
             'Lima el 28 de julio de 1821.'},
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
                           'Arica quedaron en poder chileno por 10 años.']}],
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
                 'alternativas': ['El gobierno de Riva Agüero',
                                  'La Junta Gubernativa',
                                  'La dictadura de Bolívar',
                                  'El Protectorado de San Martín',
                                  'El Congreso Constituyente'],
                 'correcta': 'D'},
                {'pregunta': 'La primera Constitución del Perú fue '
                             'promulgada en:',
                 'alternativas': ['1834', '1823', '1821', '1828', '1826'],
                 'correcta': 'B'},
                {'pregunta': 'El primer presidente del Perú fue:',
                 'alternativas': ['José de la Riva Agüero',
                                  'Ramón Castilla',
                                  'San Martín',
                                  'Simón Bolívar',
                                  'La Mar'],
                 'correcta': 'A'},
                {'pregunta': 'La Confederación Perú-Boliviana fue creada '
                             'por:',
                 'alternativas': ['Andrés de Santa Cruz',
                                  'Agustín Gamarra',
                                  'José de la Mar',
                                  'Ramón Castilla',
                                  'Felipe Salaverry'],
                 'correcta': 'A'},
                {'pregunta': 'La Confederación Perú-Boliviana fue disuelta '
                             'tras la batalla de:',
                 'alternativas': ['Ingavi',
                                  'Portada de Guías',
                                  'Ayacucho',
                                  'Socabaya',
                                  'Yungay'],
                 'correcta': 'E'},
                {'pregunta': 'Los Estados que integraron la Confederación '
                             'fueron Nor Peruano, Sur Peruano y:',
                 'alternativas': ['Argentino',
                                  'Boliviano',
                                  'Ecuatoriano',
                                  'Colombiano',
                                  'Chileno'],
                 'correcta': 'B'},
                {'pregunta': 'La principal fuente de ingresos del Estado '
                             'peruano desde 1840 fue:',
                 'alternativas': ['El azúcar',
                                  'El caucho',
                                  'El salitre',
                                  'El guano',
                                  'La plata'],
                 'correcta': 'D'},
                {'pregunta': 'El contrato Dreyfus se firmó en 1869 durante '
                             'el gobierno de:',
                 'alternativas': ['José Balta',
                                  'Echenique',
                                  'Nicolás de Piérola',
                                  'Ramón Castilla',
                                  'Manuel Pardo'],
                 'correcta': 'A'},
                {'pregunta': 'La abolición de la esclavitud y del tributo '
                             'indígena se produjo bajo el gobierno de:',
                 'alternativas': ['José Balta',
                                  'Ramón Castilla',
                                  'Gamarra',
                                  'Santa Cruz',
                                  'Manuel Pardo'],
                 'correcta': 'B'},
                {'pregunta': 'El primer ferrocarril de Sudamérica unió:',
                 'alternativas': ['Lima y Callao',
                                  'Cusco y Puno',
                                  'Tacna y Arica',
                                  'Lima y Huancayo',
                                  'Mollendo y Arequipa'],
                 'correcta': 'A'},
                {'pregunta': 'La causa inmediata de la Guerra del Pacífico '
                             'fue:',
                 'alternativas': ['La toma de Antofagasta por Perú',
                                  'El tratado de 1873',
                                  'El bloqueo del Callao',
                                  'La invasión de Tarapacá',
                                  'El impuesto de los 10 centavos al '
                                  'salitre'],
                 'correcta': 'E'},
                {'pregunta': 'El tratado que unía a Perú y Bolivia era de '
                             'alianza:',
                 'alternativas': ['Defensiva',
                                  'Cultural',
                                  'Comercial',
                                  'Ofensiva',
                                  'Aduanera'],
                 'correcta': 'A'},
                {'pregunta': 'Miguel Grau murió heroicamente en el combate '
                             'de:',
                 'alternativas': ['Angamos',
                                  'Arica',
                                  'Tarapacá',
                                  'Iquique',
                                  'San Juan'],
                 'correcta': 'A'},
                {'pregunta': 'Francisco Bolognesi murió en la batalla de:',
                 'alternativas': ['Tacna',
                                  'Miraflores',
                                  'Huamachuco',
                                  'Angamos',
                                  'Arica'],
                 'correcta': 'E'},
                {'pregunta': 'El combate de Angamos se produjo el:',
                 'alternativas': ['13 de enero de 1881',
                                  '8 de octubre de 1879',
                                  '7 de junio de 1880',
                                  '10 de julio de 1883',
                                  '21 de mayo de 1879'],
                 'correcta': 'B'},
                {'pregunta': 'La Guerra del Pacífico terminó con el Tratado '
                             'de:',
                 'alternativas': ['Tordesillas',
                                  'Santiago',
                                  'Ginebra',
                                  'Lima',
                                  'Ancón'],
                 'correcta': 'E'},
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
                 'alternativas': ['Francisco Bolognesi',
                                  'Lizardo Montero',
                                  'Nicolás de Piérola',
                                  'Miguel Iglesias',
                                  'Andrés A. Cáceres'],
                 'correcta': 'E'},
                {'pregunta': 'El caudillismo militar se caracterizó porque '
                             'el poder fue disputado por:',
                 'alternativas': ['Los jefes militares de la independencia',
                                  'Los comerciantes',
                                  'El clero',
                                  'Los indígenas',
                                  'Los extranjeros'],
                 'correcta': 'A'},
                {'pregunta': 'El sistema de comercialización del guano '
                             'previo al contrato Dreyfus fue:',
                 'alternativas': ['El monopolio estatal',
                                  'Las consignaciones',
                                  'La concesión minera',
                                  'La libre competencia',
                                  'El arrendamiento'],
                 'correcta': 'B'},
                {'pregunta': 'La Constitución de 1823, promulgada por el '
                             'Primer Congreso Constituyente, fue considerada '
                             'de carácter: (UNSAAC Ordinario)',
                 'alternativas': ['Militar',
                                  'Neoliberal',
                                  'Ideológico',
                                  'Clásico',
                                  'Liberal'],
                 'correcta': 'E'},
                {'pregunta': 'Para el negocio del guano de islas del Perú, '
                             'el Contrato Dreyfus fue suscrito en el '
                             'gobierno de: (UNSAAC Ordinario)',
                 'alternativas': ['José Balta',
                                  'Ramón Castilla',
                                  'Agustín Gamarra',
                                  'José de la Riva Agüero',
                                  'Felipe Santiago Salaverry'],
                 'correcta': 'A'},
                {'pregunta': 'En la Guerra del Pacífico, el presidente del '
                             'Perú fue: (UNSAAC Ordinario)',
                 'alternativas': ['Mariano Ignacio Prado',
                                  'Andrés Avelino Cáceres',
                                  'Aníbal Pinto',
                                  'Augusto B. Leguía',
                                  'Hilarión Daza'],
                 'correcta': 'A'},
                {'pregunta': 'El incendio y saqueo de la Biblioteca Nacional '
                             'y del Congreso Peruano fue durante: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['La dictadura de Simón Bolívar',
                                  'La expedición restauradora de Manuel '
                                  'Bulnes',
                                  'El Motín de Aznapuquio',
                                  'La invasión chilena durante la guerra del '
                                  'Pacífico',
                                  'El primer caudillismo militar'],
                 'correcta': 'D'},
                {'pregunta': 'Una de las consecuencias de la Guerra del '
                             'Pacífico fue la pérdida de las provincias de: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Tarapacá y Tacna',
                                  'Moquegua y Tarapacá',
                                  'Chorrillos y Miraflores',
                                  'Arica y Arequipa',
                                  'Tarapacá y Arica'],
                 'correcta': 'E'},
                {'pregunta': 'Al iniciarse la República, la creación de la '
                             'Biblioteca Nacional ocurrió durante: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['La Confederación Peruano-boliviana',
                                  'El gobierno de Torre Tagle',
                                  'El Primer Congreso Constituyente',
                                  'El Protectorado',
                                  'El Gobierno de Ramón Castilla'],
                 'correcta': 'D'},
                {'pregunta': 'La apropiación de los recursos naturales que '
                             'desencadenó la Guerra del Pacífico fueron el: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Salitre y Guano',
                                  'Cobre y petróleo',
                                  'Salitre y gas',
                                  'Oro y plata',
                                  'Gas y petróleo'],
                 'correcta': 'A'},
                {'pregunta': 'Una forma de la comercialización del guano por '
                             'medio del sistema de consignaciones fue '
                             'implantado por el gobierno de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Andrés Avelino Cáceres',
                                  'José Balta',
                                  'José Rufino Echenique',
                                  'Ramón Castilla',
                                  'Mariano Ignacio Prado'],
                 'correcta': 'C'},
                {'pregunta': 'Como consecuencia de la infausta Guerra del '
                             'Pacífico, después del Tratado de Ancón, el '
                             'gobierno de Andrés Avelino Cáceres decidió '
                             'encausar: (UNSAAC Ordinario)',
                 'alternativas': ['La resistencia del ejército en la sierra '
                                  'peruana',
                                  'La recuperación económica y la '
                                  'reconstrucción nacional',
                                  'El Contrato Dreyfus para la reventa del '
                                  'Guano',
                                  'La declaración de Guerra a Chile para '
                                  'recuperar Tacna y Arica',
                                  'La organización de la defensa de Lima '
                                  'contra Patricio Linch'],
                 'correcta': 'B'},
                {'pregunta': 'El pretexto que involucró al Perú en la '
                             'infausta guerra con Chile fue por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['La negativa de pagar el impuesto de diez '
                                  'centavos por quintal de Salitre',
                                  'La entrega a perpetuidad de los '
                                  'territorios de Tarapacá',
                                  'Problemas de límites de bolivianos y '
                                  'chilenos',
                                  'La Alianza secreta de Defensa entre Perú '
                                  'y Bolivia',
                                  'La ambición de Chile de los recursos de '
                                  'guano y salitre en Tarapacá'],
                 'correcta': 'A'},
                {'pregunta': 'Es considerada como causa principal de la '
                             'Guerra del Pacífico: (UNSAAC Ordinario)',
                 'alternativas': ['El algodón de Perú',
                                  'El cobre de Chile',
                                  'El salitre del Perú y Bolivia',
                                  'El mar del pacífico',
                                  'La sal de Bolivia'],
                 'correcta': 'C'},
                {'pregunta': 'Uno de los pretextos de la Guerra del Pacífico '
                             'entre Perú y Chile, fue la: (UNSAAC Ordinario)',
                 'alternativas': ['Paralización de la actividad comercial '
                                  'internacional',
                                  'Crisis Psicológica y depresión colectiva',
                                  'Alianza Secreta de defensa entre Perú y '
                                  'Bolivia',
                                  'Destrucción de las obras públicas',
                                  'Pérdida de los ingenios azucareros del '
                                  'norte del País'],
                 'correcta': 'C'},
                {'pregunta': 'La causa más importante de la Guerra del '
                             'Pacífico fue: (UNSAAC Ordinario)',
                 'alternativas': ['La disputa entre Chile y Perú por fijar '
                                  'límites territoriales',
                                  'La Alianza Secreta de Defensa entre Perú '
                                  'y Bolivia en el contexto sudamericano',
                                  'La intromisión del imperialismo '
                                  'capitalista inglés en asuntos políticos '
                                  'de Sudamérica',
                                  'La enemistad secular de Chile con Perú y '
                                  'Bolivia',
                                  'La codicia y ambición de Chile por las '
                                  'riquezas del guano y salitre del Perú y '
                                  'Bolivia'],
                 'correcta': 'E'},
                {'pregunta': 'La constitución política de 1823 no llegó a '
                             'entrar en vigencia por: (II CEPRU 2011)',
                 'alternativas': ['El Oncenio de Augusto B. Leguía',
                                  'La dictadura de Simón Bolívar',
                                  'La Monarquía Constitucional de San Martín',
                                  'El protectorado de San Martín',
                                  'La Confederación Perú-boliviana'],
                 'correcta': 'B'},
                {'pregunta': 'En la Guerra Internacional del Pacífico, el '
                             'plenipotenciario chileno que firmó el Tratado '
                             'de Paz de Ancón fue: (II CEPRU 2011)',
                 'alternativas': ['Jovino Novoa',
                                  'Miguel Iglesias',
                                  'Andrés A. Cáceres',
                                  'Hilarión Daza',
                                  'Aníbal Pinto'],
                 'correcta': 'A'},
                {'pregunta': 'Después de la Guerra con Chile, la '
                             'reconstrucción nacional tuvo un carácter: (II '
                             'CEPRU 2011)',
                 'alternativas': ['Religioso',
                                  'Educativo',
                                  'Económico',
                                  'Literario',
                                  'Académico'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'AL 16.3 LOS PRIMEROS AÑOS',
                      'items': ['El Protectorado de San Martín (1821–1822) '
                                'fue el primer gobierno del Perú '
                                'independiente.',
                                'El primer Congreso Constituyente se instaló '
                                'en 1822 y promulgó la Constitución de 1823, '
                                'de carácter liberal.',
                                'El primer presidente del Perú fue José de '
                                'la Riva Agüero.']},
                     {'titulo': 'Y 16.5 CAUDILLISMO Y CONFEDERACIÓN',
                      'items': ['El caudillismo militar dominó las primeras '
                                'décadas: los jefes militares de las guerras '
                                'de independencia se disputaron el poder.',
                                'La Confederación Perú-Boliviana (1836–1839) '
                                'fue creada por Andrés de Santa Cruz; '
                                'comprendía los Estados Nor Peruano, Sur '
                                'Peruano y Boliviano.',
                                'Fue disuelta tras la batalla de Yungay '
                                '(1839), por la oposición de Chile y '
                                'Argentina.']},
                     {'titulo': 'LA ERA DEL GUANO',
                      'items': ['El guano de las islas se convirtió en la '
                                'principal fuente de ingresos del Estado '
                                'desde 1840.',
                                'Se aplicó el sistema de consignaciones y '
                                'luego el contrato Dreyfus (1869), firmado '
                                'durante el gobierno de Balta.',
                                'Con el guano se abolió la esclavitud y el '
                                'tributo indígena durante el gobierno de '
                                'Ramón Castilla.',
                                'También se construyó el primer ferrocarril '
                                'de Sudamérica: Lima–Callao.']},
                     {'titulo': 'LA GUERRA DEL PACÍFICO',
                      'items': ['Causa inmediata: el impuesto de los 10 '
                                'centavos al salitre aplicado por Bolivia a '
                                'una empresa chilena.',
                                'Perú y Bolivia estaban unidos por un '
                                'tratado de alianza defensiva de 1873.',
                                'Combate de Angamos (8 de octubre de 1879): '
                                'muerte de Miguel Grau.',
                                'Batalla de Arica (7 de junio de 1880): '
                                'muerte de Francisco Bolognesi.',
                                'La guerra terminó con el Tratado de Ancón '
                                '(1883): el Perú cedió Tarapacá y Tacna y '
                                'Arica quedaron en poder chileno por 10 '
                                'años.']}],
  'qr_reto': [{'pregunta': 'La Confederación Perú-Boliviana fue creada por:',
               'respuesta': 'Andrés de Santa Cruz'},
              {'pregunta': 'La apropiación de los recursos naturales que '
                           'desencadenó la Guerra del Pacífico fueron el:',
               'respuesta': 'Salitre y Guano'},
              {'pregunta': 'Es considerada como causa principal de la Guerra '
                           'del Pacífico:',
               'respuesta': 'El salitre del Perú y Bolivia'}],
  'qr_dato': 'El guano de las islas se convirtió en la principal fuente de '
             'ingresos del Estado desde 1840.'},
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
                           'M. {Sánchez Cerro} en Arequipa.',
                           'El Oncenio de Leguía terminó con el golpe de '
                           'Estado del teniente coronel {Luis Sánchez Cerro} '
                           'en {1930}.']}],
  'cuadros': [{'titulo': '17.3 TRATADOS LIMÍTROFES DEL ONCENIO',
               'encabezados': ['Tratado', 'Año', 'País'],
               'filas': [['{Salomón-Lozano}', '{1922}', '{Colombia}'],
                         ['Tratado de {Lima}', '{1929}', '{Chile}']]}],
  'preguntas': [{'pregunta': 'El periodo posterior a la Guerra del Pacífico '
                             'se conoce como:',
                 'alternativas': ['Oncenio',
                                  'Primer Militarismo',
                                  'República Aristocrática',
                                  'Reconstrucción Nacional o Segundo '
                                  'Militarismo',
                                  'Patria Nueva'],
                 'correcta': 'D'},
                {'pregunta': 'Por el Contrato Grace el Perú entregó por 66 '
                             'años:',
                 'alternativas': ['Las aduanas',
                                  'Las minas',
                                  'Los ferrocarriles',
                                  'Los puertos',
                                  'Las islas guaneras únicamente'],
                 'correcta': 'C'},
                {'pregunta': 'El Contrato Grace se firmó en el año:',
                 'alternativas': ['1929', '1889', '1895', '1883', '1919'],
                 'correcta': 'B'},
                {'pregunta': 'La República Aristocrática se inició con el '
                             'gobierno de:',
                 'alternativas': ['José Pardo',
                                  'Augusto B. Leguía',
                                  'Andrés A. Cáceres',
                                  'Miguel Iglesias',
                                  'Nicolás de Piérola'],
                 'correcta': 'E'},
                {'pregunta': 'La República Aristocrática abarca los años:',
                 'alternativas': ['1919-1930',
                                  '1845-1862',
                                  '1883-1895',
                                  '1895-1919',
                                  '1930-1945'],
                 'correcta': 'D'},
                {'pregunta': 'El grupo social que ejerció el poder durante '
                             'la República Aristocrática fue:',
                 'alternativas': ['El proletariado',
                                  'El campesinado',
                                  'La oligarquía civilista',
                                  'La Iglesia',
                                  'Los militares'],
                 'correcta': 'C'},
                {'pregunta': 'La economía de la República Aristocrática se '
                             'basó en:',
                 'alternativas': ['La exportación de materias primas',
                                  'La minería estatal',
                                  'La industria pesada',
                                  'El turismo',
                                  'El comercio interno'],
                 'correcta': 'A'},
                {'pregunta': 'El gobierno de Leguía entre 1919 y 1930 se '
                             'conoce como:',
                 'alternativas': ['La Patria Nueva u Oncenio',
                                  'El Ochenio',
                                  'La República Aristocrática',
                                  'La Reconstrucción',
                                  'El Novenio'],
                 'correcta': 'A'},
                {'pregunta': 'La Constitución promulgada durante el Oncenio '
                             'fue la de:',
                 'alternativas': ['1920', '1993', '1979', '1860', '1933'],
                 'correcta': 'A'},
                {'pregunta': 'El trabajo obligatorio para construir '
                             'carreteras durante el Oncenio se llamó:',
                 'alternativas': ['Conscripción vial',
                                  'Mita republicana',
                                  'Faena',
                                  'Yanaconaje',
                                  'Enganche'],
                 'correcta': 'A'},
                {'pregunta': 'El Tratado Salomón-Lozano se firmó con:',
                 'alternativas': ['Colombia',
                                  'Brasil',
                                  'Chile',
                                  'Ecuador',
                                  'Bolivia'],
                 'correcta': 'A'},
                {'pregunta': 'El Tratado de Lima de 1929 se firmó con:',
                 'alternativas': ['Bolivia',
                                  'Chile',
                                  'Ecuador',
                                  'Argentina',
                                  'Colombia'],
                 'correcta': 'B'},
                {'pregunta': 'Por el Tratado de Lima de 1929, Tacna:',
                 'alternativas': ['Pasó a Bolivia',
                                  'Se dividió',
                                  'Volvió al Perú',
                                  'Quedó en Chile',
                                  'Se declaró neutral'],
                 'correcta': 'C'},
                {'pregunta': 'Por el Tratado de Lima de 1929, Arica quedó en '
                             'poder de:',
                 'alternativas': ['Administración internacional',
                                  'Ninguno',
                                  'Bolivia',
                                  'Chile',
                                  'Perú'],
                 'correcta': 'D'},
                {'pregunta': 'Leguía fue derrocado en 1930 por:',
                 'alternativas': ['Óscar R. Benavides',
                                  'Luis M. Sánchez Cerro',
                                  'Manuel Prado',
                                  'Odría',
                                  'Bustamante y Rivero'],
                 'correcta': 'B'},
                {'pregunta': 'Durante la República Aristocrática se produjo '
                             'el auge de la explotación del:',
                 'alternativas': ['Salitre',
                                  'Petróleo',
                                  'Caucho',
                                  'Estaño',
                                  'Guano'],
                 'correcta': 'C'},
                {'pregunta': 'El endeudamiento externo del Oncenio se dio '
                             'principalmente con:',
                 'alternativas': ['Inglaterra',
                                  'Alemania',
                                  'Francia',
                                  'España',
                                  'Estados Unidos'],
                 'correcta': 'E'},
                {'pregunta': 'Los enclaves económicos se caracterizaron por:',
                 'alternativas': ['Pertenecer a comunidades campesinas',
                                  'Ser talleres artesanales',
                                  'Ser empresas estatales',
                                  'Ser cooperativas',
                                  'Ser empresas extranjeras con escasa '
                                  'integración a la economía nacional'],
                 'correcta': 'E'},
                {'pregunta': 'El primer presidente del Segundo Militarismo '
                             'fue:',
                 'alternativas': ['Nicolás de Piérola',
                                  'Andrés A. Cáceres',
                                  'Remigio Morales Bermúdez',
                                  'Lizardo Montero',
                                  'Miguel Iglesias'],
                 'correcta': 'E'},
                {'pregunta': 'La explotación del caucho tuvo como '
                             'consecuencia principal:',
                 'alternativas': ['La construcción de ferrocarriles',
                                  'El desarrollo industrial',
                                  'La modernización agrícola',
                                  'El auge del guano',
                                  'Graves abusos contra las poblaciones '
                                  'indígenas amazónicas'],
                 'correcta': 'E'},
                {'pregunta': 'El Oncenio de Leguía terminó con el golpe de '
                             'Estado dirigido por:',
                 'alternativas': ['Manuel A. Odría',
                                  'Luis Sánchez Cerro',
                                  'Óscar R. Benavides',
                                  'Juan Velasco Alvarado',
                                  'Andrés A. Cáceres'],
                 'correcta': 'B'},
                {'pregunta': 'El régimen de gobierno de Augusto B. Leguía '
                             'fue conocido como: (UNSAAC Ordinario)',
                 'alternativas': ['El Oncenio',
                                  'Conservador',
                                  'El Ochenio',
                                  'Militar',
                                  'Reformista'],
                 'correcta': 'A'},
                {'pregunta': 'El territorio de Tacna fue reincorporado a la '
                             'soberanía del Perú, en el gobierno de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['José Pardo',
                                  'Manuel Prado Ugarteche',
                                  'Juan Velasco Alvarado',
                                  'Augusto B. Leguía',
                                  'Manuel A. Odría'],
                 'correcta': 'D'},
                {'pregunta': 'El gobierno del Oncenio de Augusto B. Leguía '
                             'terminó con el golpe de estado del general: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Nicolás de Piérola',
                                  'Eduardo López de Romaña',
                                  'José Pardo y Barreda',
                                  'Guillermo Billinghurst',
                                  'Luis M. Sánchez Cerro'],
                 'correcta': 'E'},
                {'pregunta': 'La reconstrucción de la ciudad del Cusco, '
                             'después del terremoto de 1950, fue durante el '
                             'gobierno de: (UNSAAC Ordinario)',
                 'alternativas': ['José Luis Bustamante y Rivero',
                                  'Manuel Prado',
                                  'Fernando Belaunde',
                                  'Manuel A. Odría',
                                  'Ricardo Pérez Godoy'],
                 'correcta': 'D'},
                {'pregunta': 'En el gobierno del Oncenio de Leguía, se: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Cedió a Chile, definitivamente, Tarapacá',
                                  'Entregó a Ecuador 1km2 del territorio '
                                  'nacional',
                                  'Ejecutó la expropiación de las salitreras '
                                  'de Tarapacá',
                                  'Perdió la página once del Acta de Talara',
                                  'Recuperó Tacna de la posesión chilena'],
                 'correcta': 'E'},
                {'pregunta': 'El peruano a quien designaban Amauta y que '
                             'tuvo como lema «Peruanicemos al Perú», fue: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['José Carlos Mariátegui La Chira',
                                  'José de la Riva Agüero o Osma',
                                  'Víctor Raúl Haya de la Torre',
                                  'Víctor Andrés Belaúnde',
                                  'Manuel Gonzáles Prada'],
                 'correcta': 'D'},
                {'pregunta': 'El periodo gubernamental de Manuel A. Odría, '
                             'en relación al Cusco, se caracteriza por: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['La reconstrucción del Cusco debido al '
                                  'terremoto de 1950',
                                  'Dictar las bases de la primera reforma '
                                  'agraria',
                                  'Decretar el día del campesino, el 24 de '
                                  'junio de 1969',
                                  'Reprimir el levantamiento campesino en el '
                                  'Valle de la Convención',
                                  'Asumir el poder con el nombre de Gobierno '
                                  'Revolucionario de las Fuerzas Armadas'],
                 'correcta': 'A'},
                {'pregunta': 'Característica del Segundo Gobierno de '
                             'Belaunde Terry: (UNSAAC Ordinario)',
                 'alternativas': ['Comienzo de la hiperinflación',
                                  'Finalización del terrorismo',
                                  'Masacre de Uchuraccay',
                                  'Pérdida de la democracia',
                                  'Aumento de la población en la capital'],
                 'correcta': 'A'},
                {'pregunta': 'El periodo denominado República Aristocrática '
                             'fue sustentado por: (UNSAAC Ordinario)',
                 'alternativas': ['Humberto Vidal',
                                  'Pablo Macera',
                                  'Alberto Flores',
                                  'José Tamayo',
                                  'Jorge Basadre'],
                 'correcta': 'E'},
                {'pregunta': 'El Partido Socialista fue fundado en 1928 por: '
                             '(II CEPRU 2011)',
                 'alternativas': ['Jorge Basadre',
                                  'Víctor Raúl Haya de la Torre',
                                  'José Carlos Mariátegui',
                                  'Augusto B. Leguía',
                                  'Nicolás de Piérola'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'LA RECONSTRUCCIÓN NACIONAL',
                      'items': ['Tras la Guerra del Pacífico, el Perú vivió '
                                'el llamado Segundo Militarismo, dirigido '
                                'por Miguel Iglesias y luego Andrés A. '
                                'Cáceres.',
                                'Se firmó el Contrato Grace (1889): el Perú '
                                'entregó los ferrocarriles por 66 años y el '
                                'guano a cambio de cancelar la deuda '
                                'externa.']},
                     {'titulo': 'LA REPÚBLICA ARISTOCRÁTICA (1895–1919)',
                      'items': ['Se inició con el gobierno de Nicolás de '
                                'Piérola. El poder lo ejerció una oligarquía '
                                'civilista.',
                                'La economía se basó en la exportación de '
                                'materias primas: azúcar, algodón, caucho, '
                                'lana y minerales.',
                                'Fue el periodo del auge del caucho en la '
                                'Amazonía, con graves abusos contra las '
                                'poblaciones indígenas.']},
                     {'titulo': 'EL ONCENIO DE LEGUÍA (1919–1930)',
                      'items': ['Augusto B. Leguía llamó a su gobierno la '
                                '«Patria Nueva».',
                                'Promulgó la Constitución de 1920 y '
                                'estableció la conscripción vial, trabajo '
                                'obligatorio para construir carreteras.',
                                'Aspectos limítrofes: el Tratado '
                                'Salomón-Lozano con Colombia (1922) y el '
                                'Tratado de Lima con Chile (1929), por el '
                                'cual Tacna volvió al Perú y Arica quedó en '
                                'Chile.',
                                'Impulsó los enclaves económicos y el '
                                'endeudamiento con Estados Unidos.',
                                'Fue derrocado en 1930 por la rebelión de '
                                'Luis M. Sánchez Cerro en Arequipa.',
                                'El Oncenio de Leguía terminó con el golpe '
                                'de Estado del teniente coronel Luis Sánchez '
                                'Cerro en 1930.']}],
  'qr_reto': [{'pregunta': 'El Tratado Salomón-Lozano se firmó con:',
               'respuesta': 'Colombia'},
              {'pregunta': 'Por el Contrato Grace el Perú entregó por 66 '
                           'años:',
               'respuesta': 'Los ferrocarriles'},
              {'pregunta': 'El Oncenio de Leguía terminó con el golpe de '
                           'Estado dirigido por:',
               'respuesta': 'Luis Sánchez Cerro'}],
  'qr_dato': 'Fue el periodo del auge del caucho en la Amazonía, con graves '
             'abusos contra las poblaciones indígenas.'},
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
                           'mundo en dos {bloques}.']}],
  'cuadros': [{'titulo': '18. LAS DOS GUERRAS MUNDIALES',
               'encabezados': ['Guerra', 'Años', 'Fin'],
               'filas': [['Primera', '{1914}–1918', 'Tratado de {Versalles}'],
                         ['Segunda',
                          '{1939}–{1945}',
                          'Bombas de {Hiroshima} y Nagasaki']]}],
  'preguntas': [{'pregunta': 'La causa inmediata de la Primera Guerra '
                             'Mundial fue:',
                 'alternativas': ['El hundimiento del Lusitania',
                                  'La invasión de Polonia',
                                  'El crac de 1929',
                                  'La toma de la Bastilla',
                                  'El asesinato del archiduque Francisco '
                                  'Fernando'],
                 'correcta': 'E'},
                {'pregunta': 'El asesinato que desencadenó la Primera Guerra '
                             'Mundial ocurrió en:',
                 'alternativas': ['Viena',
                                  'París',
                                  'Sarajevo',
                                  'Berlín',
                                  'Múnich'],
                 'correcta': 'C'},
                {'pregunta': 'La Primera Guerra Mundial se desarrolló entre:',
                 'alternativas': ['1939-1945',
                                  '1918-1922',
                                  '1910-1914',
                                  '1914-1918',
                                  '1929-1933'],
                 'correcta': 'D'},
                {'pregunta': 'El tratado que puso fin a la Primera Guerra '
                             'Mundial fue:',
                 'alternativas': ['Tratado de Roma',
                                  'Tratado de Versalles',
                                  'Tratado de Lima',
                                  'Pacto de Varsovia',
                                  'Tratado de Ancón'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo creado tras la Primera Guerra '
                             'Mundial para preservar la paz fue:',
                 'alternativas': ['La Cruz Roja',
                                  'El Pacto de Varsovia',
                                  'La ONU',
                                  'La Sociedad de Naciones',
                                  'La OTAN'],
                 'correcta': 'D'},
                {'pregunta': 'El país más perjudicado por el Tratado de '
                             'Versalles fue:',
                 'alternativas': ['Francia',
                                  'Rusia',
                                  'Alemania',
                                  'Inglaterra',
                                  'Italia'],
                 'correcta': 'C'},
                {'pregunta': 'La Gran Depresión se inició con el crac de la '
                             'bolsa de:',
                 'alternativas': ['Berlín',
                                  'Nueva York',
                                  'Londres',
                                  'Tokio',
                                  'París'],
                 'correcta': 'B'},
                {'pregunta': 'La Gran Depresión mundial se inició en el año:',
                 'alternativas': ['1945', '1929', '1914', '1939', '1919'],
                 'correcta': 'B'},
                {'pregunta': 'El programa aplicado en Estados Unidos para '
                             'superar la crisis fue:',
                 'alternativas': ['El Plan Cóndor',
                                  'El Plan Marshall',
                                  'La Alianza para el Progreso',
                                  'La Doctrina Monroe',
                                  'El New Deal'],
                 'correcta': 'E'},
                {'pregunta': 'El presidente que aplicó el New Deal fue:',
                 'alternativas': ['Herbert Hoover',
                                  'Franklin D. Roosevelt',
                                  'Theodore Roosevelt',
                                  'Woodrow Wilson',
                                  'Harry Truman'],
                 'correcta': 'B'},
                {'pregunta': 'La Segunda Guerra Mundial se inició con la '
                             'invasión alemana a:',
                 'alternativas': ['Austria',
                                  'Francia',
                                  'Checoslovaquia',
                                  'La URSS',
                                  'Polonia'],
                 'correcta': 'E'},
                {'pregunta': 'Las potencias del Eje fueron:',
                 'alternativas': ['URSS, China y EE.UU.',
                                  'Francia, Rusia e Inglaterra',
                                  'Alemania, Italia y Japón',
                                  'Inglaterra, Francia y EE.UU.',
                                  'Alemania, Austria y Turquía'],
                 'correcta': 'C'},
                {'pregunta': 'La Segunda Guerra Mundial terminó con:',
                 'alternativas': ['El crac de 1929',
                                  'La Revolución Rusa',
                                  'El Tratado de Versalles',
                                  'La caída del Muro de Berlín',
                                  'Las bombas atómicas sobre Hiroshima y '
                                  'Nagasaki'],
                 'correcta': 'E'},
                {'pregunta': 'El organismo internacional creado en 1945 fue:',
                 'alternativas': ['El FMI',
                                  'La ONU',
                                  'La Sociedad de Naciones',
                                  'La OEA',
                                  'La OTAN'],
                 'correcta': 'B'},
                {'pregunta': 'La Guerra Fría enfrentó a:',
                 'alternativas': ['China y Japón',
                                  'Estados Unidos y la URSS',
                                  'Alemania y Francia',
                                  'India y Pakistán',
                                  'Inglaterra y España'],
                 'correcta': 'B'},
                {'pregunta': 'Un rasgo característico de la Guerra Fría fue:',
                 'alternativas': ['La desaparición de los bloques',
                                  'El combate directo entre las potencias',
                                  'La ausencia de enfrentamiento militar '
                                  'directo entre las potencias',
                                  'La alianza militar entre EE.UU. y la URSS',
                                  'El desarme total'],
                 'correcta': 'C'},
                {'pregunta': 'Entre las causas de la Primera Guerra Mundial '
                             'NO figura:',
                 'alternativas': ['El nacionalismo',
                                  'Los sistemas de alianzas',
                                  'La carrera armamentista',
                                  'El imperialismo',
                                  'La caída del Muro de Berlín'],
                 'correcta': 'E'},
                {'pregunta': 'Los bandos de la Primera Guerra Mundial '
                             'fueron:',
                 'alternativas': ['Triple Alianza y Triple Entente',
                                  'Unión y Confederación',
                                  'Aliados y Neutrales',
                                  'OTAN y Pacto de Varsovia',
                                  'Eje y Aliados'],
                 'correcta': 'A'},
                {'pregunta': 'Una consecuencia social de la Gran Depresión '
                             'fue:',
                 'alternativas': ['El aumento de salarios',
                                  'La estabilidad bancaria',
                                  'El desempleo masivo',
                                  'El pleno empleo',
                                  'El auge del comercio'],
                 'correcta': 'C'},
                {'pregunta': 'La Segunda Guerra Mundial se desarrolló entre '
                             'los años:',
                 'alternativas': ['1939-1945',
                                  '1929-1933',
                                  '1945-1991',
                                  '1936-1939',
                                  '1914-1918'],
                 'correcta': 'A'},
                {'pregunta': 'El surgimiento de la Organización de las '
                             'Naciones Unidas para velar la paz mundial, fue '
                             'a consecuencia de la: (UNSAAC Ordinario)',
                 'alternativas': ['Segunda Guerra Mundial de 1939',
                                  'Gran Depresión Económica de 1929',
                                  'Primera Guerra Mundial de 1914',
                                  'Revolución Rusa de 1917',
                                  'Rivalidad entre Estados Unidos y Rusia'],
                 'correcta': 'A'},
                {'pregunta': 'En la Segunda Guerra Mundial, los países que '
                             'se consolidan como las grandes potencias '
                             'mundiales, son: (UNSAAC Ordinario)',
                 'alternativas': ['Estados Unidos - Unión Soviética',
                                  'Alemania - Hungría',
                                  'Francia - Ucrania',
                                  'Holanda - Bélgica',
                                  'Inglaterra - Irán'],
                 'correcta': 'A'}],
  'resumen_visual': [{'titulo': 'PRIMERA GUERRA MUNDIAL (1914–1918)',
                      'items': ['Causas: el imperialismo, el nacionalismo, '
                                'la carrera armamentista y los sistemas de '
                                'alianzas.',
                                'Causa inmediata: el asesinato del '
                                'archiduque Francisco Fernando en Sarajevo.',
                                'Bandos: la Triple Alianza y la Triple '
                                'Entente.',
                                'Terminó con el Tratado de Versalles (1919), '
                                'que impuso duras condiciones a Alemania.',
                                'Se creó la Sociedad de Naciones para '
                                'preservar la paz.']},
                     {'titulo': 'LA DEPRESIÓN MUNDIAL DE 1929',
                      'items': ['Se inició con el crac de la bolsa de Nueva '
                                'York el «jueves negro».',
                                'Consecuencias: quiebra de bancos, desempleo '
                                'masivo y caída del comercio mundial.',
                                'En Estados Unidos se aplicó el New Deal de '
                                'Franklin D. Roosevelt.']},
                     {'titulo': 'Y 18.4 SEGUNDA GUERRA MUNDIAL Y GUERRA FRÍA',
                      'items': ['La Segunda Guerra Mundial (1939–1945) se '
                                'inició con la invasión alemana a Polonia.',
                                'Bandos: las potencias del Eje (Alemania, '
                                'Italia, Japón) y los Aliados.',
                                'Terminó con las bombas atómicas sobre '
                                'Hiroshima y Nagasaki en 1945. Se creó la '
                                'ONU.',
                                'La Guerra Fría enfrentó a Estados Unidos y '
                                'la URSS sin combate directo, dividiendo el '
                                'mundo en dos bloques.']}],
  'qr_reto': [{'pregunta': 'Entre las causas de la Primera Guerra Mundial NO '
                           'figura:',
               'respuesta': 'La caída del Muro de Berlín'},
              {'pregunta': 'La causa inmediata de la Primera Guerra Mundial '
                           'fue:',
               'respuesta': 'El asesinato del archiduque Francisco Fernando'},
              {'pregunta': 'El organismo creado tras la Primera Guerra '
                           'Mundial para preservar la paz fue:',
               'respuesta': 'La Sociedad de Naciones'}],
  'qr_dato': 'La Segunda Guerra Mundial (1939–1945) se inició con la '
             'invasión alemana a Polonia.'},
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
                           'gobierno de Ollanta {Humala} (2011–2016).']}],
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
                 'alternativas': ['Velasco',
                                  'Prado',
                                  'Odría',
                                  'Manuel A. Odría',
                                  'Leguía'],
                 'correcta': 'D'},
                {'pregunta': 'El voto a la mujer en el Perú se otorgó '
                             'durante el gobierno de:',
                 'alternativas': ['Bustamante',
                                  'Belaunde',
                                  'Leguía',
                                  'Odría',
                                  'Prado'],
                 'correcta': 'D'},
                {'pregunta': 'El primer gobierno de Belaunde fue derrocado '
                             'por el escándalo de:',
                 'alternativas': ['Los vladivideos',
                                  'Los petroaudios',
                                  'El caso Dreyfus',
                                  'La página once',
                                  'El contrato Grace'],
                 'correcta': 'D'},
                {'pregunta': 'La Reforma Agraria fue aplicada en 1969 por:',
                 'alternativas': ['Juan Velasco Alvarado',
                                  'Prado',
                                  'Belaunde',
                                  'Odría',
                                  'Morales Bermúdez'],
                 'correcta': 'A'},
                {'pregunta': 'El gobierno de Velasco reconoció como lengua '
                             'oficial al:',
                 'alternativas': ['Castellano únicamente',
                                  'Ashaninka',
                                  'Quechua',
                                  'Aimara',
                                  'Inglés'],
                 'correcta': 'C'},
                {'pregunta': 'La Asamblea Constituyente de 1978 fue '
                             'presidida por:',
                 'alternativas': ['Belaunde',
                                  'Morales Bermúdez',
                                  'Alan García',
                                  'Víctor Raúl Haya de la Torre',
                                  'Bedoya Reyes'],
                 'correcta': 'D'},
                {'pregunta': 'La Constitución promulgada durante el segundo '
                             'gobierno de Belaunde fue la de:',
                 'alternativas': ['1867', '1920', '1933', '1979', '1993'],
                 'correcta': 'D'},
                {'pregunta': 'La violencia de Sendero Luminoso se inició en '
                             '1980 en:',
                 'alternativas': ['Lima',
                                  'Cusco',
                                  'Chuschi, Ayacucho',
                                  'Huancayo',
                                  'Huánuco'],
                 'correcta': 'C'},
                {'pregunta': 'El primer gobierno de Alan García se '
                             'caracterizó por:',
                 'alternativas': ['La hiperinflación',
                                  'El superávit fiscal',
                                  'El pleno empleo',
                                  'La estabilidad monetaria',
                                  'El auge exportador'],
                 'correcta': 'A'},
                {'pregunta': 'El autogolpe de Estado de Fujimori se produjo '
                             'el:',
                 'alternativas': ['5 de abril de 1992',
                                  '9 de diciembre de 2000',
                                  '3 de octubre de 1968',
                                  '28 de julio de 1990',
                                  '12 de septiembre de 1992'],
                 'correcta': 'A'},
                {'pregunta': 'El líder de Sendero Luminoso capturado en 1992 '
                             'fue:',
                 'alternativas': ['Abimael Guzmán',
                                  'Nelson Cerpa',
                                  'Víctor Polay',
                                  'Óscar Ramírez',
                                  'Feliciano'],
                 'correcta': 'A'},
                {'pregunta': 'La Constitución vigente del Perú fue '
                             'promulgada en:',
                 'alternativas': ['1920', '2001', '1933', '1993', '1979'],
                 'correcta': 'D'},
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
                 'alternativas': ['Vladivideos',
                                  'Los cuellos blancos',
                                  'Cocteles',
                                  'Narcoaudios',
                                  'Petroaudios'],
                 'correcta': 'A'},
                {'pregunta': 'El gobierno transitorio del año 2000-2001 fue '
                             'presidido por:',
                 'alternativas': ['Ollanta Humala',
                                  'Paniagua Corazao hijo',
                                  'Alejandro Toledo',
                                  'Alan García',
                                  'Valentín Paniagua'],
                 'correcta': 'E'},
                {'pregunta': 'La Comisión de la Verdad y Reconciliación fue '
                             'creada durante el gobierno de:',
                 'alternativas': ['Fujimori',
                                  'Toledo',
                                  'Humala',
                                  'Valentín Paniagua',
                                  'Alan García'],
                 'correcta': 'D'},
                {'pregunta': 'El gobierno de Alejandro Toledo impulsó '
                             'principalmente:',
                 'alternativas': ['La estatización de la banca',
                                  'La descentralización y los gobiernos '
                                  'regionales',
                                  'La Reforma Agraria',
                                  'El autogolpe',
                                  'La nacionalización del petróleo'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno militar de la segunda fase '
                             '(1975-1980) estuvo encabezado por:',
                 'alternativas': ['Nicolás Lindley',
                                  'Francisco Morales Bermúdez',
                                  'Manuel A. Odría',
                                  'Juan Velasco Alvarado',
                                  'Ricardo Pérez Godoy'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno de Ollanta Humala corresponde al '
                             'periodo:',
                 'alternativas': ['2006-2011',
                                  '1990-1995',
                                  '2011-2016',
                                  '2016-2018',
                                  '2001-2006'],
                 'correcta': 'C'},
                {'pregunta': 'Una medida económica central del primer '
                             'gobierno de Alan García fue:',
                 'alternativas': ['La firma del contrato Grace',
                                  'La privatización de empresas',
                                  'La dolarización',
                                  'La estatización de la banca',
                                  'La apertura comercial total'],
                 'correcta': 'D'},
                {'pregunta': 'La sesión del llamado Trapecio Amazónico, '
                             'corresponde al gobierno de: (UNSAAC Ordinario)',
                 'alternativas': ['Luis M. Sánchez Cerro',
                                  'Manuel A. Odría',
                                  'Manuel Prado Ugarteche',
                                  'Oscar R. Benavides',
                                  'Augusto B. Leguía'],
                 'correcta': 'D'},
                {'pregunta': 'Julio Cotler considera al gobierno de Alberto '
                             'Fujimori como: (UNSAAC Ordinario)',
                 'alternativas': ['Golpista',
                                  'Democradura',
                                  'De facto',
                                  'Neoliberal',
                                  'Populista'],
                 'correcta': 'B'},
                {'pregunta': 'El sociólogo Julio Cotler considera al '
                             'gobierno de Fujimori como: (UNSAAC Ordinario)',
                 'alternativas': ['Populista',
                                  'Democradura',
                                  'Dictadura',
                                  'Democrático',
                                  'De facto'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno de transición de Valentín Paniagua '
                             'Corazao, se dio luego de la renuncia por '
                             'corrupción de: (UNSAAC Ordinario)',
                 'alternativas': ['Manuel Odría',
                                  'Alan García',
                                  'Alberto Fujimori',
                                  'Ollanta Humala',
                                  'Fernando Belaunde'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'AL 19.4 DE ODRÍA A VELASCO',
                      'items': ['El Ochenio de Manuel A. Odría (1948–1956) '
                                'fue una dictadura militar que impulsó '
                                'grandes obras públicas y otorgó el voto a '
                                'la mujer (1955).',
                                'Primer gobierno de Fernando Belaunde '
                                '(1963–1968): impulsó Cooperación Popular y '
                                'fue derrocado por el escándalo de la página '
                                'once del contrato con la IPC.',
                                'Gobierno militar de Juan Velasco Alvarado '
                                '(1968–1975): aplicó la Reforma Agraria '
                                '(1969), nacionalizó el petróleo y la banca, '
                                'y reconoció el quechua como lengua oficial.',
                                'Segunda fase, de Francisco Morales Bermúdez '
                                '(1975–1980): convocó a la Asamblea '
                                'Constituyente de 1978, presidida por Víctor '
                                'Raúl Haya de la Torre.']},
                     {'titulo': 'AL 19.7 RETORNO A LA DEMOCRACIA',
                      'items': ['Segundo gobierno de Belaunde (1980–1985): '
                                'se promulgó la Constitución de 1979 y se '
                                'inició la violencia de Sendero Luminoso en '
                                'Chuschi, Ayacucho (1980).',
                                'Primer gobierno de Alan García (1985–1990): '
                                'crisis económica con hiperinflación y '
                                'estatización de la banca.',
                                'Década del fujimorismo (1990–2000): '
                                'autogolpe del 5 de abril de 1992, captura '
                                'de Abimael Guzmán el mismo año, y '
                                'Constitución de 1993.',
                                'En 2000 Fujimori renunció por fax desde '
                                'Japón, tras los vladivideos.']},
                     {'titulo': 'AL 19.11 SIGLO XXI',
                      'items': ['Gobierno transitorio de Valentín Paniagua '
                                '(2000–2001): creó la Comisión de la Verdad '
                                'y Reconciliación.',
                                'Alejandro Toledo (2001–2006): impulsó la '
                                'descentralización y los gobiernos '
                                'regionales.',
                                'Segundo gobierno de Alan García (2006–2011) '
                                'y gobierno de Ollanta Humala '
                                '(2011–2016).']}],
  'qr_reto': [{'pregunta': 'El primer gobierno de Belaunde fue derrocado por '
                           'el escándalo de:',
               'respuesta': 'La página once'},
              {'pregunta': 'El gobierno de Ollanta Humala corresponde al '
                           'periodo:',
               'respuesta': '2011-2016'},
              {'pregunta': 'La Asamblea Constituyente de 1978 fue presidida '
                           'por:',
               'respuesta': 'Víctor Raúl Haya de la Torre'}],
  'qr_dato': 'Segundo gobierno de Alan García (2006–2011) y gobierno de '
             'Ollanta Humala (2011–2016).'}]
