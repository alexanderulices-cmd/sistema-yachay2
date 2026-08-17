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

# Paleta de color por curso: cada área tiene su propio color distintivo,
# usado en las barras de sección, el título de la balota, y el borde de
# cada hoja. La búsqueda es por palabra clave (no exige coincidencia
# exacta), para que funcione igual con o sin emoji en el nombre del área.
_PALETA_AREAS = {
    "historia": "#8B3A3A",       # rojo terracota / vino
    "filosof": "#6B4C9A",        # púrpura
    "geograf": "#2F7A4F",        # verde bosque
    "civic": "#1F5C8B",          # azul marino (cívica)
    "cívic": "#1F5C8B",          # azul marino (cívica, con tilde)
    "comunicat": "#1E8A8A",      # turquesa / teal
    "linguist": "#1E8A8A",       # turquesa / teal (alias)
    "economi": "#B8790F",        # ámbar / dorado
    "biolog": "#4F8B2A",         # verde hoja
}
_COLOR_AREA_DEFECTO = "#12307F"  # azul original, para áreas no reconocidas


def _color_area(area):
    """Devuelve el color hexadecimal distintivo de un área/curso, buscando
    por palabra clave dentro del nombre (sin exigir coincidencia exacta,
    ni tildes, para que funcione con o sin emoji y con o sin acentos:
    '📜 Historia', 'Economía' o 'Economia' resuelven igual)."""
    import unicodedata

    def _sin_tildes(s):
        return "".join(c for c in unicodedata.normalize("NFD", s)
                       if unicodedata.category(c) != "Mn")

    area_normal = _sin_tildes((area or "").lower())
    for clave, color in _PALETA_AREAS.items():
        if _sin_tildes(clave) in area_normal:
            return color
    return _COLOR_AREA_DEFECTO

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


def _banda_titulo(story, tema, subtitulo, est, ancho, con_claves=False, area=""):
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

    acento = colors.HexColor(_color_area(area))
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


_LOGO_MARCA_AGUA_CACHE = None


def _logo_marca_agua_reader():
    """Carga el logo de marca de agua UNA sola vez y lo reutiliza en
    todas las paginas del PDF, en vez de incrustarlo de nuevo por cada
    pagina (eso multiplicaba el peso del PDF por el numero de paginas)."""
    global _LOGO_MARCA_AGUA_CACHE
    if _LOGO_MARCA_AGUA_CACHE is None:
        import os
        from reportlab.lib.utils import ImageReader
        if os.path.exists(LOGO_MARCA_AGUA):
            try:
                _LOGO_MARCA_AGUA_CACHE = ImageReader(LOGO_MARCA_AGUA)
            except Exception:
                _LOGO_MARCA_AGUA_CACHE = False
        else:
            _LOGO_MARCA_AGUA_CACHE = False
    return _LOGO_MARCA_AGUA_CACHE


def _pie(canvas, doc):
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    import os
    area = getattr(doc, "area_actual", "Historia")
    profesor = getattr(doc, "profesor_actual", "Prof. Alexander Córdova")
    canvas.saveState()

    # Borde de página del color de la ficha (color del área actual)
    _color_borde = colors.HexColor(_color_area(area))
    canvas.setStrokeColor(_color_borde)
    canvas.setLineWidth(1.3)
    _margen_borde = 0.5 * cm
    canvas.rect(_margen_borde, _margen_borde,
                doc.pagesize[0] - 2 * _margen_borde,
                doc.pagesize[1] - 2 * _margen_borde)

    # Marca de agua tenue centrada en la hoja
    _logo_reader = _logo_marca_agua_reader()
    if _logo_reader:
        try:
            lado = 14 * cm
            canvas.drawImage(
                _logo_reader,
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
    alto_enc = 5.1 * cm
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
                  est, ancho_util, con_claves, area)

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

    _color_actual = _color_area(area)

    def barra(txt):
        t = Table([[Paragraph(f"<b>{txt}</b>", est["h"])]],
                  colWidths=[col_w - 6])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(_color_actual)),
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
    # QR al final del contenido de la ficha para completar (no en el
    # resumen visual), para que el estudiante los vea junto a las
    # preguntas que acaba de completar.
    # ------------------------------------------------------------------
    qr_reto = tema.get("qr_reto")
    qr_dato = tema.get("qr_dato")
    if qr_reto or qr_dato:
        from reportlab.platypus import Image as RLImage
        st_.append(Spacer(1, 10))
        ancho_qr = 2.3 * cm
        filas_qr = []
        if qr_reto:
            png = _generar_qr_bytes(_texto_qr_reto(tema, qr_reto))
            img = RLImage(io.BytesIO(png), width=ancho_qr, height=ancho_qr)
            filas_qr.append([
                img,
                Paragraph('<b><font color="#B01C22">Reto Relámpago</font></b><br/>Escanea y autoevalúate', est["cel"]),
            ])
        if qr_dato:
            png = _generar_qr_bytes(_texto_qr_dato(tema, qr_dato))
            img = RLImage(io.BytesIO(png), width=ancho_qr, height=ancho_qr)
            filas_qr.append([
                img,
                Paragraph('<b><font color="#12307F">Dato Yachay</font></b><br/>Un dato extra para recordar', est["cel"]),
            ])
        tabla_qr = Table(filas_qr, colWidths=[ancho_qr + 4, col_w - ancho_qr - 4])
        tabla_qr.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        st_.append(tabla_qr)

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

    doc.build(st_)
    buf.seek(0)
    return _proteger_pdf(buf.getvalue())


# ================================================================
# BANCO DE PREGUNTAS
# ================================================================

# ================================================================
# JUEGOS EDUCATIVOS (Sudoku 3 niveles + Sopa de Letras)
# Solo para Historia y Filosofía por ahora — se agregan después del
# resumen visual, en páginas nuevas, para no cortarse a media página.
# ================================================================

def _sudoku_resuelto():
    """Genera una grilla 9x9 de sudoku completamente resuelta y válida."""
    import random as _random_sudoku
    grilla = [[0] * 9 for _ in range(9)]

    def valido(g, fila, col, num):
        if num in g[fila]:
            return False
        if num in [g[r][col] for r in range(9)]:
            return False
        br, bc = 3 * (fila // 3), 3 * (col // 3)
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if g[r][c] == num:
                    return False
        return True

    def resolver(g, pos=0):
        if pos == 81:
            return True
        fila, col = divmod(pos, 9)
        numeros = list(range(1, 10))
        _random_sudoku.shuffle(numeros)
        for num in numeros:
            if valido(g, fila, col, num):
                g[fila][col] = num
                if resolver(g, pos + 1):
                    return True
                g[fila][col] = 0
        return False

    resolver(grilla)
    return grilla


def _sudoku_puzzle(nivel="medio", semilla=None):
    """Genera un sudoku (grilla con huecos + su solución). Niveles:
    'facil' ~44 pistas, 'medio' ~35 pistas, 'dificil' ~26 pistas."""
    import random as _random_sudoku
    if semilla is not None:
        _random_sudoku.seed(semilla)
    resuelto = _sudoku_resuelto()
    puzzle = [fila[:] for fila in resuelto]

    pistas_por_nivel = {"facil": 44, "medio": 35, "dificil": 26}
    pistas_objetivo = pistas_por_nivel.get(nivel, 35)
    celdas = [(f, c) for f in range(9) for c in range(9)]
    _random_sudoku.shuffle(celdas)
    a_quitar = 81 - pistas_objetivo
    for f, c in celdas[:a_quitar]:
        puzzle[f][c] = 0

    if semilla is not None:
        _random_sudoku.seed()
    return puzzle, resuelto


def _tabla_sudoku(grilla, color_area, tam_celda=1.0):
    """Arma una tabla ReportLab 9x9 con estilo clásico de sudoku."""
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    t = Table([[str(n) if n else "" for n in fila] for fila in grilla],
              colWidths=[tam_celda * cm] * 9, rowHeights=[tam_celda * cm] * 9)
    color_grueso = colors.HexColor(color_area)
    estilo = [
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#AAAAAA")),
        ("BOX", (0, 0), (-1, -1), 1.8, color_grueso),
    ]
    for fila in (2, 5):
        estilo.append(("LINEBELOW", (0, fila), (-1, fila), 1.6, color_grueso))
    for col in (2, 5):
        estilo.append(("LINEAFTER", (col, 0), (col, -1), 1.6, color_grueso))
    t.setStyle(TableStyle(estilo))
    return t


def _extraer_palabras_clave(tema, minimo=8, maximo=10):
    """Extrae los terminos {entre llaves} del tema (los mismos que se
    usan como blancos a completar) para armar la sopa de letras — asi
    las palabras siempre son relevantes al tema, sin trabajo manual."""
    import re as _re_extraer
    palabras = []
    for sec in tema.get("secciones", []):
        for it in sec.get("items", []):
            for m in _PATRON.findall(it):
                m_limpio = _re_extraer.sub(r"<[^>]+>", "", m).strip()
                if m_limpio and " " not in m_limpio and m_limpio.isalpha():
                    palabras.append(m_limpio)
    # Unicas, mas largas primero (dan mejor sopa de letras), tope de 10
    vistas = set()
    unicas = []
    for p in sorted(palabras, key=len, reverse=True):
        p_mayus = p.upper()
        if p_mayus not in vistas:
            vistas.add(p_mayus)
            unicas.append(p)
    return unicas[:maximo]


def _generar_sopa_letras(palabras, tamano=14, semilla=None):
    """Genera una sopa de letras con las palabras dadas, colocadas en
    horizontal, vertical o diagonal, sin superponerse en conflicto."""
    import random as _random_sopa
    if semilla is not None:
        _random_sopa.seed(semilla)

    palabras_limpias = []
    for p in palabras:
        p_limpia = p.upper().strip()
        for viejo, nuevo in [("Á","A"),("É","E"),("Í","I"),("Ó","O"),
                             ("Ú","U"),("Ñ","N")]:
            p_limpia = p_limpia.replace(viejo, nuevo)
        p_limpia = "".join(c for c in p_limpia if c.isalpha())
        if 3 <= len(p_limpia) <= tamano:
            palabras_limpias.append(p_limpia)
    palabras_limpias = sorted(set(palabras_limpias), key=len, reverse=True)[:10]

    grilla = [[None] * tamano for _ in range(tamano)]
    direcciones = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    palabras_colocadas = []

    for palabra in palabras_limpias:
        colocada = False
        intentos = 0
        while not colocada and intentos < 100:
            intentos += 1
            dr, dc = _random_sopa.choice(direcciones)
            fila_ini = _random_sopa.randint(0, tamano - 1)
            col_ini = _random_sopa.randint(0, tamano - 1)
            fila_fin = fila_ini + dr * (len(palabra) - 1)
            col_fin = col_ini + dc * (len(palabra) - 1)
            if not (0 <= fila_fin < tamano and 0 <= col_fin < tamano):
                continue
            conflicto = False
            for i, letra in enumerate(palabra):
                f, c = fila_ini + dr * i, col_ini + dc * i
                if grilla[f][c] is not None and grilla[f][c] != letra:
                    conflicto = True
                    break
            if conflicto:
                continue
            for i, letra in enumerate(palabra):
                f, c = fila_ini + dr * i, col_ini + dc * i
                grilla[f][c] = letra
            palabras_colocadas.append(palabra)
            colocada = True

    import string as _string_sopa
    letras_disponibles = _string_sopa.ascii_uppercase + "AEIOU" * 3
    for f in range(tamano):
        for c in range(tamano):
            if grilla[f][c] is None:
                grilla[f][c] = _random_sopa.choice(letras_disponibles)

    if semilla is not None:
        _random_sopa.seed()
    return grilla, palabras_colocadas


def _tabla_sopa_letras(grilla, color_area, tam_celda=0.62):
    """Arma una tabla ReportLab con la sopa de letras."""
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    t = Table(grilla, colWidths=[tam_celda * cm] * len(grilla[0]),
              rowHeights=[tam_celda * cm] * len(grilla))
    t.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#AAAAAA")),
        ("BOX", (0, 0), (-1, -1), 1.5, colors.HexColor(color_area)),
    ]))
    return t


def _armar_ramas_mapa_mental(tema, max_ramas=5, sub_por_rama=2):
    """Arma la estructura de ramas para el mapa mental: cada sección
    del tema es una rama, y sus términos clave ({entre llaves}) son
    sub-ramas — la mitad se muestran, la otra mitad quedan en blanco
    para que el estudiante las complete de memoria."""
    import re as _re_mapa
    ramas = []
    for i, sec in enumerate(tema.get("secciones", [])[:max_ramas]):
        terminos = []
        for it in sec.get("items", []):
            for m in _PATRON.finditer(it):
                palabra = _re_mapa.sub(r"<[^>]+>", "", m.group(1)).strip()
                if palabra and " " not in palabra and palabra.isalpha():
                    terminos.append(palabra)
        terminos_unicos = list(dict.fromkeys(terminos))[:sub_por_rama]
        if terminos_unicos:
            sub_con_visibilidad = [(t, j == 0) for j, t in enumerate(terminos_unicos)]
            ramas.append((sec["titulo"], sub_con_visibilidad))
    return ramas


def _dibujo_mapa_mental(titulo_central, ramas, color_area, con_claves=False,
                        ancho=None, alto=None):
    """Dibuja un mapa mental radial (técnica de Tony Buzan, usada en
    todo el mundo para repaso y memorización): el tema al centro, sus
    secciones como ramas, y términos clave como sub-ramas — algunos
    ocultos para completar."""
    import math as _math_mapa
    from reportlab.graphics.shapes import Drawing, Circle, String, Line, Rect
    from reportlab.lib import colors as _colors_mapa
    from reportlab.lib.units import cm as _cm_mapa

    if ancho is None:
        ancho = 17.5 * _cm_mapa
    if alto is None:
        alto = 15 * _cm_mapa
    cm = _cm_mapa

    d = Drawing(ancho, alto)
    cx, cy = ancho / 2, alto / 2
    color_base = _colors_mapa.HexColor(color_area)

    radio_centro = 2.0 * cm
    d.add(Circle(cx, cy, radio_centro, fillColor=color_base, strokeColor=color_base))
    palabras = titulo_central.split()
    mitad = max(1, len(palabras) // 2) if len(palabras) > 2 else len(palabras)
    linea1 = " ".join(palabras[:mitad])
    linea2 = " ".join(palabras[mitad:])
    d.add(String(cx, cy + 3, linea1[:20], fillColor=_colors_mapa.white,
                fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle"))
    if linea2:
        d.add(String(cx, cy - 8, linea2[:20], fillColor=_colors_mapa.white,
                    fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle"))

    n_ramas = max(len(ramas), 1)
    radio_rama = min(ancho, alto) / 2 - 2.6 * cm

    for i, (nombre_rama, subterminos) in enumerate(ramas):
        angulo = (2 * _math_mapa.pi / n_ramas) * i - _math_mapa.pi / 2
        rx = cx + radio_rama * _math_mapa.cos(angulo)
        ry = cy + radio_rama * _math_mapa.sin(angulo)

        d.add(Line(cx + radio_centro * _math_mapa.cos(angulo),
                   cy + radio_centro * _math_mapa.sin(angulo),
                   rx, ry, strokeColor=color_base, strokeWidth=1.5))

        ancho_caja = 4.0 * cm
        alto_caja = 0.8 * cm
        d.add(Rect(rx - ancho_caja / 2, ry - alto_caja / 2, ancho_caja, alto_caja,
                   fillColor=_colors_mapa.HexColor("#F0F0F0"), strokeColor=color_base,
                   strokeWidth=1))
        texto_rama = nombre_rama if len(nombre_rama) < 30 else nombre_rama[:28] + "…"
        d.add(String(rx, ry - 3, texto_rama, fillColor=_colors_mapa.HexColor("#333333"),
                     fontName="Helvetica-Bold", fontSize=6, textAnchor="middle"))

        for j, (termino, mostrar) in enumerate(subterminos):
            offset = (j - (len(subterminos) - 1) / 2) * 0.4
            angulo_sub = angulo + offset
            radio_sub = radio_rama + 1.9 * cm
            sx = cx + radio_sub * _math_mapa.cos(angulo_sub)
            sy = cy + radio_sub * _math_mapa.sin(angulo_sub)
            d.add(Line(rx, ry, sx, sy, strokeColor=_colors_mapa.HexColor("#AAAAAA"),
                       strokeWidth=0.7))
            texto_sub = termino if (mostrar or con_claves) else "___________"
            d.add(String(sx, sy, texto_sub, fillColor=_colors_mapa.HexColor("#555555"),
                         fontName="Helvetica", fontSize=6, textAnchor="middle"))
    return d


def _extraer_palabras_con_pista(tema, maximo=10):
    """Extrae pares (palabra, pista) de los items que tienen UNA sola
    palabra clave entre llaves — la pista es la oración con esa palabra
    reemplazada por un espacio, así el estudiante debe recordar/entender
    el concepto, no solo buscar una palabra suelta.

    Se descartan los items donde el término está justo al inicio
    seguido de dos puntos (ej. 'El {Término}: se refiere a...') — al
    reemplazar el término, la frase queda sin sujeto y se lee mal
    ('Se refiere a...'). Solo se usan pistas donde el término queda
    en medio de una oración completa."""
    import re as _re_pistas
    resultado = []
    for sec in tema.get("secciones", []):
        for it in sec.get("items", []):
            matches = list(_PATRON.finditer(it))
            if len(matches) != 1:
                continue
            palabra = _re_pistas.sub(r"<[^>]+>", "", matches[0].group(1)).strip()
            if not palabra or " " in palabra or not palabra.isalpha():
                continue
            pista = _PATRON.sub("___", it)
            pista = _re_pistas.sub(r"<[^>]+>", "", pista).strip().rstrip(".")
            if len(pista) <= 10:
                continue
            # Descartar si el termino esta muy al inicio (posicion < 15
            # caracteres) Y le sigue ":" -- eso rompe la frase al swappear.
            pos_blank = pista.find("___")
            texto_despues = pista[pos_blank + 3:pos_blank + 5].strip()
            if pos_blank < 15 and texto_despues.startswith(":"):
                continue
            resultado.append((palabra, pista))
    return resultado[:maximo]


def _generar_crucigrama(palabras_con_pistas, tamano=16, semilla=None):
    """Coloca palabras en una grilla cruzándolas donde sea posible."""
    import random as _random_cruci
    if semilla is not None:
        _random_cruci.seed(semilla)

    items = []
    for palabra, pista in palabras_con_pistas:
        p = palabra.upper().strip()
        for viejo, nuevo in [("Á","A"),("É","E"),("Í","I"),("Ó","O"),("Ú","U"),("Ñ","N")]:
            p = p.replace(viejo, nuevo)
        p = "".join(c for c in p if c.isalpha())
        if 3 <= len(p) <= tamano:
            items.append((p, pista))
    items.sort(key=lambda x: len(x[0]), reverse=True)
    items = items[:10]
    if not items:
        return None, []

    grilla = [[None] * tamano for _ in range(tamano)]
    colocadas = []

    def puede_colocar(palabra, fila, col, direccion):
        dr, dc = (0, 1) if direccion == "H" else (1, 0)
        fila_fin = fila + dr * (len(palabra) - 1)
        col_fin = col + dc * (len(palabra) - 1)
        if not (0 <= fila_fin < tamano and 0 <= col_fin < tamano):
            return False
        for i, letra in enumerate(palabra):
            f, c = fila + dr * i, col + dc * i
            if grilla[f][c] is not None and grilla[f][c] != letra:
                return False
        return True

    def colocar(palabra, fila, col, direccion):
        dr, dc = (0, 1) if direccion == "H" else (1, 0)
        for i, letra in enumerate(palabra):
            f, c = fila + dr * i, col + dc * i
            grilla[f][c] = letra

    primera, pista1 = items[0]
    fila_centro = tamano // 2
    col_inicio = max(0, (tamano - len(primera)) // 2)
    colocar(primera, fila_centro, col_inicio, "H")
    colocadas.append((primera, pista1, fila_centro, col_inicio, "H"))

    for palabra, pista in items[1:]:
        mejor = None
        for letra_idx, letra in enumerate(palabra):
            for f in range(tamano):
                for c in range(tamano):
                    if grilla[f][c] == letra:
                        fila_ini = f - letra_idx
                        if puede_colocar(palabra, fila_ini, c, "V"):
                            mejor = (fila_ini, c, "V")
                            break
                if mejor:
                    break
            if mejor:
                break
        if mejor:
            fila_ini, col_ini, direccion = mejor
            colocar(palabra, fila_ini, col_ini, direccion)
            colocadas.append((palabra, pista, fila_ini, col_ini, direccion))
        else:
            intentos = 0
            while intentos < 50:
                intentos += 1
                f = _random_cruci.randint(0, tamano - 1)
                c = _random_cruci.randint(0, tamano - 1)
                direccion = _random_cruci.choice(["H", "V"])
                if puede_colocar(palabra, f, c, direccion):
                    colocar(palabra, f, c, direccion)
                    colocadas.append((palabra, pista, f, c, direccion))
                    break

    if semilla is not None:
        _random_cruci.seed()
    return grilla, colocadas


def _recortar_grilla_crucigrama(grilla, colocadas):
    """Recorta la grilla al área mínima que contiene todas las palabras."""
    filas_usadas, cols_usadas = set(), set()
    for palabra, pista, f, c, direccion in colocadas:
        dr, dc = (0, 1) if direccion == "H" else (1, 0)
        for i in range(len(palabra)):
            filas_usadas.add(f + dr * i)
            cols_usadas.add(c + dc * i)
    f_min, f_max = min(filas_usadas), max(filas_usadas)
    c_min, c_max = min(cols_usadas), max(cols_usadas)
    nueva_grilla = [fila[c_min:c_max + 1] for fila in grilla[f_min:f_max + 1]]
    nuevas_colocadas = [(p, pista, f - f_min, c - c_min, d)
                        for p, pista, f, c, d in colocadas]
    return nueva_grilla, nuevas_colocadas


def _numerar_crucigrama(colocadas):
    """Asigna números a las celdas donde inicia una palabra."""
    posiciones = sorted(set((f, c) for palabra, pista, f, c, direccion in colocadas))
    numero_por_pos = {pos: i for i, pos in enumerate(posiciones, start=1)}
    return [(numero_por_pos[(f, c)], palabra, pista, f, c, direccion)
           for palabra, pista, f, c, direccion in colocadas]


def _tabla_crucigrama(grilla, colocadas_numeradas, color_area, mostrar_letras=False, tam_celda=0.72):
    """Arma la tabla del crucigrama: celdas vacías SIN relleno (blancas,
    ahorra tinta al imprimir), celdas de palabras con borde y número
    donde inicia una palabra. La forma del crucigrama se distingue
    solo por dónde hay líneas, no por un fondo negro sólido."""
    from reportlab.platypus import Table, TableStyle, Paragraph
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle

    numeros_por_celda = {(f, c): num for num, p, pista, f, c, d in colocadas_numeradas}
    filas_tabla = []
    for f, fila in enumerate(grilla):
        fila_render = []
        for c, letra in enumerate(fila):
            if letra is None:
                fila_render.append("")
            else:
                contenido = letra if mostrar_letras else ""
                numero = numeros_por_celda.get((f, c), "")
                if numero:
                    texto_celda = f'<font size="5">{numero}</font><br/><font size="9"><b>{contenido}</b></font>'
                else:
                    texto_celda = f'<font size="9"><b>{contenido}</b></font>'
                fila_render.append(Paragraph(texto_celda,
                    ParagraphStyle("celda_cruci", fontSize=9, leading=9, alignment=1)))
        filas_tabla.append(fila_render)

    t = Table(filas_tabla, colWidths=[tam_celda * cm] * len(grilla[0]),
             rowHeights=[tam_celda * cm] * len(grilla))
    estilo = [
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 1.5, colors.HexColor(color_area)),
        ("LEFTPADDING", (0, 0), (-1, -1), 1),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]
    for f, fila in enumerate(grilla):
        for c, letra in enumerate(fila):
            if letra is not None:
                estilo.append(("GRID", (c, f), (c, f), 0.6, colors.HexColor("#888888")))
    t.setStyle(TableStyle(estilo))
    return t


def _generar_verdadero_falso(pares, cantidad=8, semilla=None):
    """Genera afirmaciones V/F: la mitad verdaderas (término correcto en
    su lugar), la mitad falsas (se cambia el término por otro del mismo
    tema, creando una afirmación 'casi correcta' — el mismo tipo de
    trampa que aparece en exámenes reales de admisión, y que obliga a
    conocer el concepto con precisión, no solo reconocerlo)."""
    import random as _random_vf
    if semilla is not None:
        _random_vf.seed(semilla)

    pares_disponibles = pares[:cantidad] if len(pares) >= cantidad else pares
    afirmaciones = []
    palabras_todas = [p for p, pista in pares]

    for i, (palabra_correcta, pista) in enumerate(pares_disponibles):
        es_verdadera = (i % 2 == 0)
        if es_verdadera:
            texto = pista.replace("___", palabra_correcta)
        else:
            candidatos = [p for p in palabras_todas if p.lower() != palabra_correcta.lower()]
            if candidatos:
                palabra_falsa = _random_vf.choice(candidatos)
                texto = pista.replace("___", palabra_falsa)
            else:
                texto = pista.replace("___", palabra_correcta)
                es_verdadera = True
        afirmaciones.append((texto, es_verdadera))

    _random_vf.shuffle(afirmaciones)
    if semilla is not None:
        _random_vf.seed()
    return afirmaciones


def _tabla_relacion_columnas(pares, color_area):
    """Arma el juego 'Relaciona la columna A con la B': términos
    numerados a la izquierda, definiciones desordenadas y con letra a
    la derecha — obliga a entender el concepto, no solo ubicar letras."""
    import random as _random_relacion
    from reportlab.platypus import Table, TableStyle, Paragraph
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle

    estilo_celda = ParagraphStyle("rc", fontSize=9, leading=11.5)
    letras_id = "ABCDEFGHIJ"

    columna_a = [(i + 1, palabra) for i, (palabra, pista) in enumerate(pares)]
    indices_b = list(range(len(pares)))
    _random_relacion.shuffle(indices_b)
    columna_b = [(letras_id[j], pares[idx][1]) for j, idx in enumerate(indices_b)]

    filas = [[Paragraph("<b>Columna A</b>", estilo_celda),
             Paragraph("<b>Columna B</b>", estilo_celda)]]
    for i in range(len(pares)):
        izq = f"{columna_a[i][0]}. {columna_a[i][1]}   (    )"
        der = f"{columna_b[i][0]}. {columna_b[i][1]}"
        filas.append([Paragraph(izq, estilo_celda), Paragraph(der, estilo_celda)])

    t = Table(filas, colWidths=[6.8 * cm, 9.7 * cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#AAAAAA")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(color_area)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


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

    alto_enc = 5.2 * cm
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
                  est, ancho_util, con_claves, area)

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
                                  'Fuentes escritas únicamente',
                                  'Causas y consecuencias',
                                  'Mitos y leyendas',
                                  'Fechas y personajes'],
                 'correcta': 'C'},
                {'pregunta': 'Según Heródoto, los dos ojos de la historia '
                             'son:',
                 'alternativas': ['El tiempo y el espacio',
                                  'La causa y el efecto',
                                  'El mito y la razón',
                                  'El hecho y la fuente',
                                  'La sociedad y la cultura'],
                 'correcta': 'A'},
                {'pregunta': '¿Cuál NO es un componente esencial del '
                             'acontecimiento histórico?',
                 'alternativas': ['Ninguno, los tres primeros lo son',
                                  'La sociedad',
                                  'La tecnología',
                                  'El tiempo',
                                  'El espacio'],
                 'correcta': 'C'},
                {'pregunta': 'Los topónimos, las leyendas y los cantos '
                             'corresponden a fuentes:',
                 'alternativas': ['Escritas',
                                  'Materiales',
                                  'Orales o tradicionales',
                                  'Antroposomáticas',
                                  'Audiovisuales'],
                 'correcta': 'C'},
                {'pregunta': 'Las momias, los cabellos y los huesos son '
                             'fuentes:',
                 'alternativas': ['Antroposomáticas',
                                  'Documentales',
                                  'Orales',
                                  'Audiovisuales',
                                  'Monumentales'],
                 'correcta': 'A'},
                {'pregunta': 'Los llamados «vladivideos» y «petroaudios» '
                             'constituyen fuentes:',
                 'alternativas': ['Antroposomáticas',
                                  'Audiovisuales',
                                  'Materiales',
                                  'Escritas',
                                  'Tradicionales'],
                 'correcta': 'B'},
                {'pregunta': 'La institución encargada de la preservación '
                             'del patrimonio cultural peruano es:',
                 'alternativas': ['El INC',
                                  'El Ministerio de Cultura',
                                  'La UNESCO',
                                  'El Congreso de la República',
                                  'El Ministerio de Educación'],
                 'correcta': 'B'},
                {'pregunta': 'El fondo documental del Estado peruano es '
                             'custodiado por:',
                 'alternativas': ['El Archivo Regional del Cusco',
                                  'El Archivo General de la Nación',
                                  'La Biblioteca Nacional',
                                  'El Ministerio de Cultura',
                                  'La UNSAAC'],
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
                                  'Antroposomáticas',
                                  'Escritas',
                                  'Audiovisuales',
                                  'Materiales'],
                 'correcta': 'C'},
                {'pregunta': 'La historia «como hecho» se refiere a:',
                 'alternativas': ['La conservación del patrimonio',
                                  'Los acontecimientos y procesos sociales '
                                  'del pasado',
                                  'El método de estudio del pasado',
                                  'La crítica de las fuentes',
                                  'La periodificación cronológica'],
                 'correcta': 'B'},
                {'pregunta': 'El propósito final del estudio de la historia, '
                             'según el texto, es:',
                 'alternativas': ['Defender una ideología',
                                  'Comprender el presente y proyectarse al '
                                  'futuro',
                                  'Memorizar fechas exactas',
                                  'Escribir crónicas',
                                  'Coleccionar restos arqueológicos'],
                 'correcta': 'B'},
                {'pregunta': 'Las construcciones arquitectónicas, la '
                             'cerámica y los textiles corresponden a '
                             'fuentes:',
                 'alternativas': ['Escritas',
                                  'Audiovisuales',
                                  'Orales',
                                  'Materiales o monumentales',
                                  'Antroposomáticas'],
                 'correcta': 'D'},
                {'pregunta': 'La dimensión temporal de larga duración se '
                             'refiere a:',
                 'alternativas': ['Un hecho puntual',
                                  'La cronología absoluta',
                                  'Un acontecimiento anual',
                                  'Procesos que abarcan siglos',
                                  'La biografía de un personaje'],
                 'correcta': 'D'},
                {'pregunta': 'El Archivo Regional del Cusco (A.R.C.) es una '
                             'institución de:',
                 'alternativas': ['Educación básica regular',
                                  'Turismo receptivo',
                                  'Gobierno regional exclusivo',
                                  'Recaudación tributaria',
                                  'Investigación y difusión del patrimonio '
                                  'cultural'],
                 'correcta': 'E'},
                {'pregunta': 'El estudio sistemático, verídico y metódico '
                             'corresponde a la historia entendida como:',
                 'alternativas': ['Tradición',
                                  'Patrimonio',
                                  'Hecho',
                                  'Mito',
                                  'Ciencia'],
                 'correcta': 'E'},
                {'pregunta': 'El espacio como componente histórico puede '
                             'ser:',
                 'alternativas': ['Únicamente continental',
                                  'Solo nacional',
                                  'Local, regional, nacional, continental o '
                                  'mundial',
                                  'Solo local',
                                  'Solo urbano'],
                 'correcta': 'C'},
                {'pregunta': 'La obligación de cuidar y conservar el '
                             'patrimonio cultural corresponde a:',
                 'alternativas': ['La UNESCO',
                                  'Los gobiernos regionales únicamente',
                                  'Solo a los arqueólogos',
                                  'El Estado y la comunidad nacional',
                                  'Solo al Ministerio de Cultura'],
                 'correcta': 'D'},
                {'pregunta': 'Los idiomas y las creencias transmitidas de '
                             'padres a hijos son fuentes:',
                 'alternativas': ['Orales',
                                  'Somáticas',
                                  'Monumentales',
                                  'Audiovisuales',
                                  'Escritas'],
                 'correcta': 'A'},
                {'pregunta': 'Señale la afirmación CORRECTA sobre las '
                             'fuentes históricas:',
                 'alternativas': ['Son restos, huellas y testimonios '
                                  'materiales e inmateriales',
                                  'Solo las escritas son válidas',
                                  'Únicamente las produce el Estado',
                                  'Se limitan a los restos arqueológicos',
                                  'Solo existen desde la invención de la '
                                  'imprenta'],
                 'correcta': 'A'},
                {'pregunta': 'Las inscripciones dejadas por el hombre en '
                             'diversos materiales como piedras, metales, '
                             'telas, manuscritos y textos se denominan '
                             'fuentes: (UNSAAC 2010)',
                 'alternativas': ['Materiales o monumentales',
                                  'Primarias',
                                  'Secundarias',
                                  'Escritas',
                                  'Orales o tradicionales'],
                 'correcta': 'D'},
                {'pregunta': 'Los fragmentos de restos óseos humanos que '
                             'sirven para conocer el grado de desarrollo '
                             'físico del hombre son fuentes: (UNSAAC 2010)',
                 'alternativas': ['Monumentales',
                                  'Antroposomáticas',
                                  'Audiovisuales',
                                  'Escritas',
                                  'Orales'],
                 'correcta': 'B'},
                {'pregunta': 'Un video sobre Sacsayhuamán es una fuente: '
                             '(UNSAAC 2011)',
                 'alternativas': ['Oral',
                                  'Escrita',
                                  'Tradicional',
                                  'Material',
                                  'Audiovisual'],
                 'correcta': 'E'},
                {'pregunta': 'El enunciado «la Universidad Nacional de San '
                             'Antonio del Cusco fue fundada el 1 de marzo de '
                             '1692» corresponde a la cronología: (UNSAAC '
                             '2013)',
                 'alternativas': ['Relativa',
                                  'Aproximada',
                                  'Absoluta',
                                  'Verdadera',
                                  'Válida'],
                 'correcta': 'C'},
                {'pregunta': 'El mito de los Hermanos Ayar y la Crónica de '
                             'Inca Garcilaso de la Vega representan, '
                             'respectivamente, a las fuentes históricas: '
                             '(UNSAAC 2013)',
                 'alternativas': ['Oral - Tradicional',
                                  'Antroposomática - Documental',
                                  'Tradicional - Material',
                                  'Cronística - Escrita',
                                  'Oral - Escrita'],
                 'correcta': 'E'},
                {'pregunta': 'Los mitos y las crónicas pertenecen '
                             'respectivamente a las fuentes históricas: '
                             '(UNSAAC 2015)',
                 'alternativas': ['Tradicionales y materiales',
                                  'Abstractas y concretas',
                                  'Monumentales y tradicionales',
                                  'Antroposomáticas y etnológicas',
                                  'Orales y escritas'],
                 'correcta': 'E'},
                {'pregunta': 'Los restos físicos humanos que sirven para '
                             'estudiar el grado de desarrollo étnico del '
                             'hombre corresponden a las fuentes: (UNSAAC '
                             '2016)',
                 'alternativas': ['Biológicas',
                                  'Antroposomáticas',
                                  'Tradicionales',
                                  'Culturales',
                                  'Escritas'],
                 'correcta': 'B'},
                {'pregunta': 'Los testimonios tradicionales, costumbres y '
                             'creencias de los grupos humanos son una '
                             'fuente: (UNSAAC 2018)',
                 'alternativas': ['Antroposomática',
                                  'Oral',
                                  'Monumental',
                                  'Audiovisual',
                                  'Escrita'],
                 'correcta': 'B'},
                {'pregunta': 'La institución encargada de cuidar y conservar '
                             'el patrimonio histórico del Perú es el '
                             'Ministerio de: (UNSAAC 2022)',
                 'alternativas': ['Industria y Turismo',
                                  'Cultura',
                                  'Educación',
                                  'Economía',
                                  'Justicia'],
                 'correcta': 'B'},
                {'pregunta': 'Las crónicas y los periódicos son fuentes de '
                             'tipo: (UNSAAC 2023)',
                 'alternativas': ['Documental',
                                  'Monumental',
                                  'Antroposomático',
                                  'Material',
                                  'Audiovisual'],
                 'correcta': 'A'},
                {'pregunta': 'La ciencia que estudia el pasado, a partir del '
                             'presente con proyección al futuro, es la: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Astrología',
                                  'Cronología',
                                  'Arqueología',
                                  'Historia',
                                  'Etnología'],
                 'correcta': 'D'},
                {'pregunta': 'El folclore es una fuente histórica: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Monumental',
                                  'Tecnológica',
                                  'Audiovisual',
                                  'Tradicional',
                                  'Cronística'],
                 'correcta': 'D'},
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
                 'alternativas': ['Tradicionales',
                                  'Numismática',
                                  'Orales',
                                  'Antroposomáticas',
                                  'Audiovisuales'],
                 'correcta': 'D'},
                {'pregunta': 'Al periodo carente de documentos escritos, se '
                             'conoce como: (I CEPRU 2010)',
                 'alternativas': ['Historiografía',
                                  'Prehistoria',
                                  'Cronología',
                                  'Poshistoria',
                                  'Historia'],
                 'correcta': 'B'},
                {'pregunta': 'El estudio de los fragmentos que permite '
                             'conocer el grado de desarrollo físico y étnico '
                             'del hombre, corresponde a las fuentes: (I '
                             'CEPRU 2011)',
                 'alternativas': ['Materiales',
                                  'Audiovisuales',
                                  'Antroposomáticas',
                                  'Orales',
                                  'Escritas'],
                 'correcta': 'C'},
                {'pregunta': 'Los restos óseos humanos son fuentes: (I CEPRU '
                             '2012)',
                 'alternativas': ['Tradicionales',
                                  'Materiales',
                                  'Antroposomáticas',
                                  'Culturales',
                                  'Monumentales'],
                 'correcta': 'C'},
                {'pregunta': 'La paleontología es una ciencia que estudia: '
                             '(I CEPRU 2012)',
                 'alternativas': ['Al hombre en la sociedad',
                                  'La superficie terrestre',
                                  'Los manuscritos antiguos',
                                  'Los escudos y blasones',
                                  'Los restos fósiles'],
                 'correcta': 'E'},
                {'pregunta': 'Los testimonios de carácter tecnológico, '
                             'corresponde a las fuentes: (I CEPRU 2013)',
                 'alternativas': ['Culturales',
                                  'Escritas',
                                  'Naturales',
                                  'Audiovisuales',
                                  'Materiales o monumentales'],
                 'correcta': 'E'},
                {'pregunta': 'La ciencia que ubica, describe y explica la '
                             'superficie terrestre donde se producen los '
                             'acontecimientos históricos es la: (I CEPRU '
                             '2013)',
                 'alternativas': ['Historia',
                                  'Cronología',
                                  'Geografía',
                                  'Paleografía',
                                  'Teología'],
                 'correcta': 'C'}],
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
                 'alternativas': ['La capacidad de fabricar objetos',
                                  'El descubrimiento del fuego',
                                  'La aparición de la escritura',
                                  'La vida sedentaria',
                                  'La domesticación de animales'],
                 'correcta': 'A'},
                {'pregunta': 'La teoría evolucionista fue formulada por:',
                 'alternativas': ['Boucher de Perthes',
                                  'Daniel Wilson',
                                  'Heródoto',
                                  'Charles Darwin',
                                  'Christian Thomsen'],
                 'correcta': 'D'},
                {'pregunta': 'El término «prehistoria» se refiere al periodo '
                             'anterior a la aparición de:',
                 'alternativas': ['Los metales',
                                  'La escritura',
                                  'La rueda',
                                  'La agricultura',
                                  'La cerámica'],
                 'correcta': 'B'},
                {'pregunta': 'Christian Thomsen dividió la prehistoria '
                             'observando:',
                 'alternativas': ['Los restos óseos',
                                  'Las glaciaciones',
                                  'Los enterramientos',
                                  'Los materiales de las herramientas',
                                  'Las pinturas rupestres'],
                 'correcta': 'D'},
                {'pregunta': 'La técnica osteodontoquerática consistió en el '
                             'uso de:',
                 'alternativas': ['Huesos de mandíbula de animales',
                                  'Piedra pulimentada',
                                  'Metales fundidos',
                                  'Fibras vegetales',
                                  'Arcilla cocida'],
                 'correcta': 'A'},
                {'pregunta': 'Altamira y Lascaux son famosas por su:',
                 'alternativas': ['Metalurgia del bronce',
                                  'Escritura cuneiforme',
                                  'Cerámica policroma',
                                  'Arte rupestre',
                                  'Arquitectura megalítica'],
                 'correcta': 'D'},
                {'pregunta': 'El hombre del Paleolítico se caracterizó por '
                             'ser:',
                 'alternativas': ['Urbano y estatal',
                                  'Sedentario y agricultor',
                                  'Ganadero y alfarero',
                                  'Nómada y cavernícola',
                                  'Comerciante y navegante'],
                 'correcta': 'D'},
                {'pregunta': 'La organización social del Paleolítico '
                             'comprendió:',
                 'alternativas': ['Ayllus y curacazgos',
                                  'Reinos hereditarios',
                                  'Ciudades-Estado',
                                  'Imperios centralizados',
                                  'Hordas, clanes y gens'],
                 'correcta': 'E'},
                {'pregunta': 'El tótem en el Paleolítico era:',
                 'alternativas': ['Una vivienda sobre pilotes',
                                  'Un instrumento musical',
                                  'Una herramienta de sílex',
                                  'Un antepasado común sacralizado',
                                  'Un tipo de sepultura'],
                 'correcta': 'D'},
                {'pregunta': 'El Mesolítico es el periodo de transición '
                             'entre:',
                 'alternativas': ['Holoceno y Pleistoceno',
                                  'Paleolítico y Edad del Cobre',
                                  'Pleistoceno y Holoceno',
                                  'Edad del Bronce y del Hierro',
                                  'Neolítico y Edad de los Metales'],
                 'correcta': 'C'},
                {'pregunta': 'La primera gran revolución agrícola y ganadera '
                             'corresponde al:',
                 'alternativas': ['Mesolítico',
                                  'Edad del Hierro',
                                  'Paleolítico',
                                  'Calcolítico',
                                  'Neolítico'],
                 'correcta': 'E'},
                {'pregunta': 'Los palafitos fueron:',
                 'alternativas': ['Vasijas rituales',
                                  'Templos escalonados',
                                  'Casas de madera sobre pilotes',
                                  'Herramientas de sílex',
                                  'Tumbas colectivas'],
                 'correcta': 'C'},
                {'pregunta': 'Los dólmenes, menhires y crómlech son '
                             'expresiones de arquitectura:',
                 'alternativas': ['Hidráulica',
                                  'Doméstica',
                                  'Palaciega',
                                  'Militar',
                                  'Funeraria y religiosa'],
                 'correcta': 'E'},
                {'pregunta': 'Stonehenge, importante monumento megalítico, '
                             'se ubica en:',
                 'alternativas': ['Inglaterra',
                                  'Suiza',
                                  'España',
                                  'Turquía',
                                  'Francia'],
                 'correcta': 'A'},
                {'pregunta': 'En el Neolítico surgen por primera vez:',
                 'alternativas': ['La osteodontoquerática',
                                  'Las glaciaciones',
                                  'El arte rupestre',
                                  'El nomadismo y la caza',
                                  'La propiedad privada, las clases sociales '
                                  'y el Estado'],
                 'correcta': 'E'},
                {'pregunta': 'El uso del cobre fundido se inició en:',
                 'alternativas': ['Babilonia',
                                  'Menfis',
                                  'Ur',
                                  'Nínive',
                                  'Çatalhöyük (Turquía)'],
                 'correcta': 'E'},
                {'pregunta': 'El bronce es una aleación de cobre con:',
                 'alternativas': ['Hierro',
                                  'Plata',
                                  'Zinc',
                                  'Plomo',
                                  'Estaño'],
                 'correcta': 'E'},
                {'pregunta': 'Etimológicamente, «Neolítico» significa:',
                 'alternativas': ['Edad del hielo',
                                  'Piedra nueva o pulimentada',
                                  'Piedra antigua',
                                  'Edad del metal',
                                  'Piedra media'],
                 'correcta': 'B'},
                {'pregunta': 'La bipedación trajo como consecuencia directa:',
                 'alternativas': ['La aparición del lenguaje escrito',
                                  'El aumento del cráneo',
                                  'El uso exclusivo de las extremidades '
                                  'inferiores para desplazarse',
                                  'La domesticación del perro',
                                  'La construcción de ciudades'],
                 'correcta': 'C'},
                {'pregunta': 'La primera ciudad prehistórica construida '
                             'sobre un lago se descubrió en:',
                 'alternativas': ['El mar Muerto',
                                  'El lago Zúrich, Suiza',
                                  'El lago Van',
                                  'El lago Ness',
                                  'El lago Titicaca'],
                 'correcta': 'B'},
                {'pregunta': 'La Edad de los Metales se caracteriza por el '
                             'abandono gradual de instrumentos de:',
                 'alternativas': ['Barro',
                                  'Bronce',
                                  'Cobre',
                                  'Piedra',
                                  'Hierro'],
                 'correcta': 'D'},
                {'pregunta': 'La primera etapa de la Edad de los Metales, '
                             'transición desde la Edad de Piedra, se llama:',
                 'alternativas': ['Edad del Bronce',
                                  'Edad del Hierro',
                                  'Edad del Estaño',
                                  'Edad del Cobre o Calcolítico',
                                  'Edad del Oro'],
                 'correcta': 'D'},
                {'pregunta': 'El uso del cobre fundido se inició hacia el '
                             '5000 a.C. en:',
                 'alternativas': ['Çatalhöyük, actual Turquía',
                                  'China',
                                  'Egipto',
                                  'Grecia',
                                  'Mesopotamia'],
                 'correcta': 'A'},
                {'pregunta': 'El bronce es la aleación de cobre y:',
                 'alternativas': ['Plomo',
                                  'Plata',
                                  'Hierro',
                                  'Estaño',
                                  'Oro'],
                 'correcta': 'D'},
                {'pregunta': 'El uso del bronce comenzó hacia el 3000 a.C. '
                             'en:',
                 'alternativas': ['Sumeria (Mesopotamia)',
                                  'Roma',
                                  'Grecia',
                                  'Egipto',
                                  'China'],
                 'correcta': 'A'},
                {'pregunta': 'Con bronce se fabricaron armas como espadas, '
                             'dagas y:',
                 'alternativas': ['Solo ollas',
                                  'Solo joyas',
                                  'Escudos',
                                  'Solo herramientas agrícolas',
                                  'Ruedas'],
                 'correcta': 'C'},
                {'pregunta': 'El pueblo que primero utilizó el hierro '
                             'fundido, hacia 1500 a.C., fue:',
                 'alternativas': ['Los hititas de Turquía',
                                  'Los fenicios',
                                  'Los sumerios',
                                  'Los griegos',
                                  'Los egipcios'],
                 'correcta': 'A'},
                {'pregunta': 'Una de las ventajas del hierro frente al '
                             'bronce es su mayor:',
                 'alternativas': ['Fragilidad',
                                  'Abundancia como mineral',
                                  'Peso',
                                  'Escasez',
                                  'Costo'],
                 'correcta': 'B'},
                {'pregunta': 'Otra ventaja del hierro frente al bronce es '
                             'que sus armas son más:',
                 'alternativas': ['Duras',
                                  'Costosas exclusivamente',
                                  'Difíciles de fabricar',
                                  'Frágiles',
                                  'Livianas exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'En Europa, el uso del hierro comenzó con la '
                             'cultura de Hallstatt, ubicada en:',
                 'alternativas': ['Turquía',
                                  'Grecia',
                                  'Austria',
                                  'Italia',
                                  'España'],
                 'correcta': 'C'},
                {'pregunta': 'El hombre del paleolítico se expresó mediante '
                             'el: (UNSAAC 2010)',
                 'alternativas': ['Arte textil',
                                  'Culto religioso',
                                  'Cultivo',
                                  'Arte rupestre',
                                  'Intercambio de productos'],
                 'correcta': 'D'},
                {'pregunta': 'Una de las características del hombre del '
                             'neolítico fue ser: (UNSAAC 2010)',
                 'alternativas': ['Nómada',
                                  'Antropólogo',
                                  'Pescador',
                                  'Sedentario',
                                  'Cazador, pescador y recolector'],
                 'correcta': 'D'},
                {'pregunta': 'Se conoce como troglodita al hombre del: '
                             '(UNSAAC 2011)',
                 'alternativas': ['Paleolítico',
                                  'Epipaleolítico',
                                  'Mesolítico',
                                  'Palafítico',
                                  'Neolítico'],
                 'correcta': 'A'},
                {'pregunta': 'El hombre del Neolítico se caracteriza por '
                             'ser: (UNSAAC 2011)',
                 'alternativas': ['Horticultor, recolector, pescador',
                                  'Sedentario, agricultor, ganadero',
                                  'Agricultor, nómade, pescador',
                                  'Cazador, recolector, pescador',
                                  'Nómade, ganadero, horticultor'],
                 'correcta': 'B'},
                {'pregunta': 'Los raspadores y machacadores son considerados '
                             'objetos líticos más antiguos que pertenecieron '
                             'al hombre de: (UNSAAC 2011)',
                 'alternativas': ['Lauricocha',
                                  'Chivateros',
                                  'Toquepala',
                                  'Paccaicasa',
                                  'Paiján'],
                 'correcta': 'D'},
                {'pregunta': 'Los rasgos fundamentales de la Hominización '
                             'son la: (UNSAAC 2013)',
                 'alternativas': ['Semisedentarización y totemización',
                                  'Culturización y civilización',
                                  'Sociabilización y diferenciación social',
                                  'Bipedación y fabricación de objetos',
                                  'Sedentarización y domesticación'],
                 'correcta': 'D'},
                {'pregunta': 'El descubrimiento del fuego ocurrió en: '
                             '(UNSAAC 2013)',
                 'alternativas': ['El mesolítico',
                                  'El neolítico',
                                  'El paleolítico',
                                  'La Edad Histórica',
                                  'La Edad Antigua'],
                 'correcta': 'C'},
                {'pregunta': 'El periodo mesolítico de la Edad de Piedra se '
                             'caracterizó por: (UNSAAC 2014)',
                 'alternativas': ['La finalización de las glaciaciones',
                                  'La práctica del culto al muerto',
                                  'Una economía exclusivamente recolectora',
                                  'El surgimiento de la familia y la '
                                  'propiedad privada',
                                  'El descubrimiento del fuego'],
                 'correcta': 'A'},
                {'pregunta': 'Los rasgos característicos del proceso de '
                             'hominización fue la: (UNSAAC 2015)',
                 'alternativas': ['Vida sedentaria del hombre',
                                  'Construcción de las primeras viviendas',
                                  'Domesticación de plantas',
                                  'Noción de la existencia de Dios',
                                  'Capacidad de fabricar objetos'],
                 'correcta': 'E'},
                {'pregunta': 'La hominización se refiere: (UNSAAC 2015)',
                 'alternativas': ['A la sedentarización del hombre',
                                  'A la evolución de las especies animales y '
                                  'plantas',
                                  'A la evolución de la especie humana',
                                  'Al surgimiento de las primeras '
                                  'manifestaciones agrícolas',
                                  'Al desarrollo de la civilización humana'],
                 'correcta': 'C'},
                {'pregunta': 'El hombre del Paleolítico se caracterizó por: '
                             '(UNSAAC 2015)',
                 'alternativas': ['Su iniciación en la organización familiar',
                                  'Su notable desarrollo en la pesca con '
                                  'arpón',
                                  'Desconocer la agricultura',
                                  'Iniciar la sedentarización',
                                  'Rendir culto a sus muertos'],
                 'correcta': 'C'},
                {'pregunta': 'El periodo del Neolítico se caracterizó por: '
                             '(UNSAAC 2016)',
                 'alternativas': ['El desconocimiento de la agricultura, '
                                  'ganadería y cerámica',
                                  'El desarrollo de la industria microlítica',
                                  'La manifestación de arte rupestre en las '
                                  'cavernas',
                                  'Surgimiento de la familia, la propiedad '
                                  'privada, clases sociales y estado',
                                  'El nomadismo del hombre primitivo'],
                 'correcta': 'D'},
                {'pregunta': 'El proceso de Hominización fue explicado por '
                             'Charles Darwin en su libro: (UNSAAC 2016)',
                 'alternativas': ['Evolución de las culturas',
                                  'Primeras poblaciones',
                                  'Origen de las especies',
                                  'Transformaciones humanas',
                                  'Origen de la Civilización'],
                 'correcta': 'C'},
                {'pregunta': 'Un rasgo fundamental del proceso de '
                             'hominización fue: (UNSAAC 2018)',
                 'alternativas': ['El comienzo de la agrupación familiar del '
                                  'hombre',
                                  'El proceso de la migración peruana',
                                  'El proceso de la civilización',
                                  'La vida sedentaria de los primates',
                                  'La bipedación y postura erguida del '
                                  'hombre primitivo'],
                 'correcta': 'E'},
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
                 'alternativas': ['Sedentario',
                                  'Pescador',
                                  'Nómada',
                                  'Cavernario',
                                  'Troglodita'],
                 'correcta': 'A'},
                {'pregunta': 'El científico más representativo que planteó '
                             'la Teoría Evolucionista del origen humano es: '
                             '(UNSAAC 2022)',
                 'alternativas': ['Cristhian Thomsen',
                                  'Jacobo Boucher',
                                  'Daniel Wilson',
                                  'Charles Darwin',
                                  'Cristóbal Keller'],
                 'correcta': 'D'},
                {'pregunta': 'Una característica principal del Periodo '
                             'Neolítico es: (UNSAAC 2023)',
                 'alternativas': ['La culminación de las glaciaciones',
                                  'La invención del arco y la flecha',
                                  'El sedentarismo del hombre',
                                  'El descubrimiento del fuego',
                                  'El nomadismo del hombre'],
                 'correcta': 'C'},
                {'pregunta': 'El hombre del periodo Neolítico fue: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Agricultor',
                                  'Recolector',
                                  'Nómada',
                                  'Pintor rupestre',
                                  'Troglodita'],
                 'correcta': 'A'},
                {'pregunta': 'El hombre primitivo logra la domesticación de '
                             'los animales e inventó la agricultura '
                             'incipiente en el periodo: (UNSAAC Ordinario)',
                 'alternativas': ['Hallstatt',
                                  'Neolítico',
                                  'Mesolítico',
                                  'La Tène',
                                  'Paleolítico'],
                 'correcta': 'B'},
                {'pregunta': 'El hombre del neolítico fue: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Troglodita',
                                  'Cazador',
                                  'Recolector',
                                  'Ceramista',
                                  'Errante'],
                 'correcta': 'D'},
                {'pregunta': 'La división de la prehistoria la propuso: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Antoni Greman',
                                  'Ferdinand Leakey',
                                  'Charles Darwin',
                                  'Donald Latrap',
                                  'Christian Thomsen'],
                 'correcta': 'E'},
                {'pregunta': 'Una característica propia del Neolítico '
                             'prehistórico es el: (UNSAAC Ordinario)',
                 'alternativas': ['Surgimiento del Lenguaje y el Tótem',
                                  'Desarrollo de la industria microlítica y '
                                  'la osteodontoquerática',
                                  'Desconocimiento de la agricultura y el '
                                  'pastoreo',
                                  'Surgimiento de la propiedad privada y de '
                                  'las clases sociales',
                                  'Descubrimiento del fuego, la flecha y el '
                                  'arco'],
                 'correcta': 'D'},
                {'pregunta': 'El alejamiento de las glaciaciones se dio en '
                             'el periodo geológico denominado: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Neolítico',
                                  'Calcolítico',
                                  'Pleistocénico',
                                  'Mesolítico',
                                  'Paleolítico'],
                 'correcta': 'D'},
                {'pregunta': 'En el proceso de hominización fue fundamental: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['El inicio de la organización familiar',
                                  'El desarrollo de la civilización humana',
                                  'La selección natural de las especies no '
                                  'humanas',
                                  'La práctica inicial del culto a los '
                                  'muertos',
                                  'La capacidad de fabricar objetos'],
                 'correcta': 'E'},
                {'pregunta': 'En el periodo cultural del Mesolítico, la '
                             'humanidad primitiva: (UNSAAC Ordinario)',
                 'alternativas': ['Inició la práctica del culto a sus '
                                  'muertos',
                                  'Empezó a diferenciarse racialmente',
                                  'Fue exclusivamente cazadora, pescadora y '
                                  'recolectora',
                                  'Conoció la propiedad privada y '
                                  'consiguientemente la diferenciación '
                                  'social',
                                  'Descubrió simultáneamente la cerámica y '
                                  'la textilería'],
                 'correcta': 'C'},
                {'pregunta': 'Lograda la revolución Neolítica, el hombre '
                             'paulatinamente cambió a otro proceso en el que '
                             'fabricaron sus herramientas y utensilios con '
                             'materiales más resistentes; a este cambio se '
                             'conoce como: (UNSAAC Ordinario)',
                 'alternativas': ['Periodo del Neolítico',
                                  'La edad de los metales',
                                  'La edad de piedra',
                                  'Al periodo del Mesolítico',
                                  'Periodo del Paleolítico superior'],
                 'correcta': 'B'},
                {'pregunta': 'El investigador que utilizó el término Pre '
                             'Historia fue: (UNSAAC Ordinario)',
                 'alternativas': ['Charles Darwin',
                                  'Fernando Brundel',
                                  'Pablo Macera',
                                  'Daniel Wilson',
                                  'Christian Thomsen'],
                 'correcta': 'D'},
                {'pregunta': 'El investigador que planteó el proceso de la '
                             'hominización, como proceso evolutivo, fue: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Fernand Braudel',
                                  'Christian Thomsen',
                                  'Charles Darwin',
                                  'Pablo Macera',
                                  'Daniel Wilson'],
                 'correcta': 'C'},
                {'pregunta': 'En qué periodo apareció la domesticación de '
                             'plantas y animales: (UNSAAC Ordinario)',
                 'alternativas': ['Neolítico',
                                  'Mesolítico',
                                  'Edad de los metales (bronce)',
                                  'Paleolítico',
                                  'Edad de los metales (Cobre)'],
                 'correcta': 'A'},
                {'pregunta': 'El científico que dividió la prehistoria '
                             'observando los materiales utilizados por el '
                             'hombre, fue: (UNSAAC Ordinario)',
                 'alternativas': ['Daniel Wilson',
                                  'Christian Thomsen',
                                  'Donald Johanson',
                                  'Jacobo Boucher de Perthes',
                                  'Charles Darwin'],
                 'correcta': 'B'},
                {'pregunta': 'La prehistoria se divide en: (I CEPRU 2010)',
                 'alternativas': ['Edad de piedra - edad de los metales',
                                  'Edad de piedra - edad de cobre',
                                  'Edad de piedra - edad contemporánea',
                                  'Edad de los metales - edad media',
                                  'Edad antigua - edad media'],
                 'correcta': 'A'},
                {'pregunta': 'La característica del hombre del paleolítico: '
                             '(I CEPRU 2010)',
                 'alternativas': ['Sedentario',
                                  'Ceramista',
                                  'Troglodita',
                                  'Arquitecto',
                                  'Tejedor'],
                 'correcta': 'C'},
                {'pregunta': 'En la edad de los metales el hombre descubre: '
                             '(I CEPRU 2011)',
                 'alternativas': ['Hierro - Plata - Mercurio',
                                  'Plata - Hierro - Mercurio',
                                  'Cobre - Bronce - Hierro',
                                  'Oro - Plata - Cobre',
                                  'Bronce - Plata - Oro'],
                 'correcta': 'C'},
                {'pregunta': 'En el periodo Paleolítico, el hombre se '
                             'caracterizó por ser: (I CEPRU 2011)',
                 'alternativas': ['Ceramista',
                                  'Nómada',
                                  'Agricultor',
                                  'Textilero',
                                  'Sedentario'],
                 'correcta': 'B'},
                {'pregunta': 'En el neolítico el hombre fue: (I CEPRU 2011)',
                 'alternativas': ['Nómada',
                                  'Cazador',
                                  'Troglodita',
                                  'Sedentario',
                                  'Pescador'],
                 'correcta': 'D'},
                {'pregunta': 'El desconocimiento de la producción agrícola, '
                             'es una de las características que corresponde '
                             'al periodo: (I CEPRU 2012)',
                 'alternativas': ['Edad de los metales',
                                  'Paleolítico',
                                  'Neolítico',
                                  'Mesolítico',
                                  'Microlítico'],
                 'correcta': 'B'},
                {'pregunta': 'Las estructuras funerarias de Dólmenes, '
                             'Menhires y Crómlech corresponden al periodo '
                             'de: (I CEPRU 2012)',
                 'alternativas': ['Mesolítico',
                                  'Paleolítico',
                                  'Eneolítico',
                                  'Neolítico',
                                  'Calcolítico'],
                 'correcta': 'D'},
                {'pregunta': 'La etapa que abarca desde la aparición del '
                             'hombre hasta la invención de la escritura se '
                             'denomina: (I CEPRU 2013)',
                 'alternativas': ['Mesohistoria',
                                  'Historia',
                                  'Prehistoria',
                                  'Protohistoria',
                                  'Poshistoria'],
                 'correcta': 'C'},
                {'pregunta': 'Se considera como el inicio de la cultura, a '
                             'la capacidad de fabricar objetos, siendo este '
                             'uno de los rasgos de la: (I CEPRU 2013)',
                 'alternativas': ['Hominización',
                                  'Creación',
                                  'Socialización',
                                  'Adaptación',
                                  'Aculturación'],
                 'correcta': 'A'},
                {'pregunta': 'La primera gran revolución agrícola, ganadera '
                             'e industrial, que experimentaron los grupos '
                             'humanos ocurrió en el periodo: (I CEPRU 2013)',
                 'alternativas': ['Neolítico',
                                  'Paleolítico',
                                  'Tardío',
                                  'Mesolítico',
                                  'Temprano'],
                 'correcta': 'A'},
                {'pregunta': 'El autor del Origen de las especies fue: (I '
                             'CEPRU 2014)',
                 'alternativas': ['Charles Darwin',
                                  'Cristian Thomsen',
                                  'Henry Raulinson',
                                  'Jacobo Boucher',
                                  'Francis Champollion'],
                 'correcta': 'A'}],
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
                 'alternativas': ['Indo y Ganges',
                                  'Tigris y Éufrates',
                                  'Amarillo y Azul',
                                  'Danubio y Rin',
                                  'Nilo y Éufrates'],
                 'correcta': 'B'},
                {'pregunta': 'La capital del Imperio Asirio fue:',
                 'alternativas': ['Babilonia',
                                  'Uruk',
                                  'Ur',
                                  'Nínive',
                                  'Akkad'],
                 'correcta': 'D'},
                {'pregunta': 'Las primeras Ciudades-Estado de Mesopotamia '
                             'fueron creadas por los:',
                 'alternativas': ['Caldeos',
                                  'Sumerios',
                                  'Acadios',
                                  'Hititas',
                                  'Persas'],
                 'correcta': 'B'},
                {'pregunta': 'El rey acadio que conquistó las ciudades '
                             'sumerias fue:',
                 'alternativas': ['Nabopolasar',
                                  'Hammurabi',
                                  'Sargón',
                                  'Gudea',
                                  'Asurbanipal'],
                 'correcta': 'C'},
                {'pregunta': 'El primer código jurídico escrito de '
                             'Mesopotamia se atribuye a:',
                 'alternativas': ['Hammurabi',
                                  'Asurbanipal',
                                  'Rawlinson',
                                  'Sargón',
                                  'Nabucodonosor II'],
                 'correcta': 'A'},
                {'pregunta': 'La biblioteca de Nínive fue mandada construir '
                             'por:',
                 'alternativas': ['Nabucodonosor II',
                                  'Asurbanipal',
                                  'Hammurabi',
                                  'Sargón II',
                                  'Nabopolasar'],
                 'correcta': 'B'},
                {'pregunta': 'Los jardines colgantes de Babilonia se '
                             'atribuyen a:',
                 'alternativas': ['Nabucodonosor II',
                                  'Sargón',
                                  'Gudea',
                                  'Asurbanipal',
                                  'Hammurabi'],
                 'correcta': 'A'},
                {'pregunta': 'El «cautiverio babilónico» afectó al pueblo:',
                 'alternativas': ['Persa',
                                  'Asirio',
                                  'Acadio',
                                  'Hitita',
                                  'Judío'],
                 'correcta': 'E'},
                {'pregunta': 'El templo escalonado característico de '
                             'Mesopotamia se denomina:',
                 'alternativas': ['Partenón',
                                  'Zigurat',
                                  'Ziggurat egipcio',
                                  'Pirámide',
                                  'Mastaba'],
                 'correcta': 'B'},
                {'pregunta': 'Fueron los primeros en construir el arco, la '
                             'bóveda y la cúpula:',
                 'alternativas': ['Los griegos',
                                  'Los persas',
                                  'Los mesopotámicos',
                                  'Los egipcios',
                                  'Los romanos'],
                 'correcta': 'C'},
                {'pregunta': 'La escritura cuneiforme recibe ese nombre por:',
                 'alternativas': ['Su carácter jeroglífico',
                                  'Su soporte de papiro',
                                  'Su origen sacerdotal',
                                  'Sus signos en forma de cuña',
                                  'Su uso comercial'],
                 'correcta': 'D'},
                {'pregunta': 'La inscripción de la roca de Behistún fue '
                             'descifrada por:',
                 'alternativas': ['Heródoto',
                                  'Schliemann',
                                  'Champollion',
                                  'Henry Rawlinson',
                                  'Boucher de Perthes'],
                 'correcta': 'D'},
                {'pregunta': 'Los toros alados con cabeza humana se hallaron '
                             'en el palacio de:',
                 'alternativas': ['Gudea en Lagash',
                                  'Asurbanipal en Nínive',
                                  'Hammurabi en Babilonia',
                                  'Ciro en Persépolis',
                                  'Sargón II en Korsabad'],
                 'correcta': 'E'},
                {'pregunta': 'La Baja Mesopotamia fue la región donde se '
                             'desarrolló la civilización:',
                 'alternativas': ['Caldea',
                                  'Elamita',
                                  'Hitita',
                                  'Asiria',
                                  'Persa'],
                 'correcta': 'A'},
                {'pregunta': 'Actualmente el territorio de Mesopotamia '
                             'corresponde principalmente a:',
                 'alternativas': ['Siria',
                                  'Egipto',
                                  'Irán',
                                  'Irak',
                                  'Turquía'],
                 'correcta': 'D'},
                {'pregunta': 'Egipto se ubica en el continente:',
                 'alternativas': ['Oceánico',
                                  'Africano',
                                  'Americano',
                                  'Europeo',
                                  'Asiático'],
                 'correcta': 'B'},
                {'pregunta': 'El límite norte del antiguo Egipto era:',
                 'alternativas': ['Nubia',
                                  'El desierto de Libia',
                                  'El istmo de Suez',
                                  'El Mar Rojo',
                                  'El mar Mediterráneo'],
                 'correcta': 'E'},
                {'pregunta': 'El artífice de la caída del Imperio Asirio '
                             'fue:',
                 'alternativas': ['Nabopolasar',
                                  'Hammurabi',
                                  'Ciro',
                                  'Sargón',
                                  'Nabucodonosor II'],
                 'correcta': 'A'},
                {'pregunta': 'La estatua del príncipe Gudea se conserva '
                             'actualmente en:',
                 'alternativas': ['El Museo Británico',
                                  'El Museo de El Cairo',
                                  'El Museo del Louvre',
                                  'El Museo de Berlín',
                                  'El Metropolitan'],
                 'correcta': 'C'},
                {'pregunta': 'Un factor que explica las constantes '
                             'invasiones a Mesopotamia fue:',
                 'alternativas': ['Su escasa población',
                                  'Su clima glacial',
                                  'La ausencia de fronteras naturales',
                                  'Su aislamiento total',
                                  'La falta de ríos'],
                 'correcta': 'C'},
                {'pregunta': 'A diferencia de Egipto, Mesopotamia no tenía '
                             'fronteras naturales, lo que generó constantes:',
                 'alternativas': ['Invasiones',
                                  'Sequías',
                                  'Migraciones internas',
                                  'Hambrunas',
                                  'Terremotos'],
                 'correcta': 'A'},
                {'pregunta': 'Las primeras unidades políticas de Mesopotamia '
                             'se organizaron bajo el modelo de:',
                 'alternativas': ['Imperio centralizado',
                                  'República federal',
                                  'Confederación tribal',
                                  'Monarquía absoluta única',
                                  'Ciudad-Estado'],
                 'correcta': 'E'},
                {'pregunta': 'En las ciudades-estado mesopotámicas '
                             'gobernaron inicialmente los:',
                 'alternativas': ['Senadores',
                                  'Cónsules',
                                  'Faraones',
                                  'Reyes-sacerdotes',
                                  'Emperadores'],
                 'correcta': 'D'},
                {'pregunta': 'En arquitectura, los mesopotámicos fueron '
                             'pioneros en construir el arco, la bóveda y:',
                 'alternativas': ['La pirámide escalonada',
                                  'El zigurat exclusivamente',
                                  'El obelisco',
                                  'La cúpula',
                                  'La columna dórica'],
                 'correcta': 'D'},
                {'pregunta': 'Las estatuas de toros alados con cabeza humana '
                             'se hallaron en el palacio de:',
                 'alternativas': ['Nabucodonosor',
                                  'Sargón II',
                                  'Hammurabi',
                                  'Assurbanipal',
                                  'Gudea'],
                 'correcta': 'B'},
                {'pregunta': 'La escritura mesopotámica, con signos en forma '
                             'de cuñas, se llama escritura:',
                 'alternativas': ['Jeroglífica',
                                  'Rúnica',
                                  'Demótica',
                                  'Lineal B',
                                  'Cuneiforme'],
                 'correcta': 'E'},
                {'pregunta': 'La escritura de la roca de Behistún fue '
                             'descifrada por:',
                 'alternativas': ['Champollion',
                                  'Flinders Petrie',
                                  'Henry Rawlinson',
                                  'Heinrich Schliemann',
                                  'Howard Carter'],
                 'correcta': 'C'},
                {'pregunta': 'El Imperio Antiguo de Egipto (2600-2150 a.C.) '
                             'consolidó el poder del Estado en la figura de:',
                 'alternativas': ['El sumo sacerdote',
                                  'El visir exclusivo',
                                  'El escriba mayor',
                                  'El Faraón',
                                  'El senado'],
                 'correcta': 'D'},
                {'pregunta': 'La Gran Pirámide de Guiza es atribuida por '
                             'Heródoto a:',
                 'alternativas': ['Dyeser',
                                  'Tutmosis III',
                                  'Keops',
                                  'Kefrén',
                                  'Micerino'],
                 'correcta': 'C'},
                {'pregunta': 'La capital del Imperio Antiguo de Egipto se '
                             'estableció en:',
                 'alternativas': ['Tebas',
                                  'Menfis',
                                  'Luxor',
                                  'Alejandría',
                                  'Karnak'],
                 'correcta': 'B'},
                {'pregunta': 'El Imperio Medio de Egipto (2150-1785 a.C.) '
                             'tuvo como capital a:',
                 'alternativas': ['Alejandría',
                                  'Karnak',
                                  'Tebas',
                                  'Guiza',
                                  'Menfis'],
                 'correcta': 'C'},
                {'pregunta': 'Durante el Imperio Medio, Egipto sufrió la '
                             'invasión de un pueblo nómada de Asia llamado:',
                 'alternativas': ['Los fenicios',
                                  'Los persas',
                                  'Los Hicsos',
                                  'Los asirios',
                                  'Los babilonios'],
                 'correcta': 'C'},
                {'pregunta': 'El Imperio Nuevo de Egipto logró expulsar a '
                             'los Hicsos, destacando los faraones Ramsés II '
                             'y:',
                 'alternativas': ['Micerino',
                                  'Kefrén',
                                  'Keops',
                                  'Tutmosis III',
                                  'Amenofis IV'],
                 'correcta': 'D'},
                {'pregunta': 'El faraón que intentó imponer el culto '
                             'monoteísta al dios Atón fue:',
                 'alternativas': ['Kefrén',
                                  'Keops',
                                  'Ramsés II',
                                  'Amenofis IV',
                                  'Tutmosis III'],
                 'correcta': 'D'},
                {'pregunta': 'Egipto fue una monarquía de tipo:',
                 'alternativas': ['Constitucional',
                                  'Teocrática',
                                  'Federal',
                                  'Oligárquica',
                                  'Parlamentaria'],
                 'correcta': 'B'},
                {'pregunta': 'La administración del Estado egipcio la '
                             'ejercían los:',
                 'alternativas': ['Escribas',
                                  'Comerciantes exclusivamente',
                                  'Esclavos',
                                  'Faraones directamente sin ayuda',
                                  'Sacerdotes exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'Las clases sociales de Egipto incluían '
                             'sacerdotes, escribas, comerciantes, el pueblo '
                             'y:',
                 'alternativas': ['Los nómadas',
                                  'Los extranjeros',
                                  'Los militares exclusivamente',
                                  'Los artesanos exclusivamente',
                                  'Los esclavos'],
                 'correcta': 'E'},
                {'pregunta': 'Los sepulcros para nobles, con forma de '
                             'pequeñas pirámides truncas, se llaman:',
                 'alternativas': ['Obeliscos',
                                  'Mastabas',
                                  'Zigurats',
                                  'Hipogeos',
                                  'Cenotafios'],
                 'correcta': 'B'},
                {'pregunta': 'Las tumbas subterráneas excavadas en roca '
                             'donde se enterraba al pueblo egipcio se '
                             'llaman:',
                 'alternativas': ['Hipogeos',
                                  'Pirámides',
                                  'Sarcófagos',
                                  'Zigurats',
                                  'Mastabas'],
                 'correcta': 'A'},
                {'pregunta': 'Los templos más representativos de Egipto, '
                             'ubicados en Tebas, son los de Karnak y:',
                 'alternativas': ['Menfis',
                                  'Guiza',
                                  'Abu Simbel exclusivo',
                                  'Luxor',
                                  'Alejandría'],
                 'correcta': 'D'},
                {'pregunta': 'La Esfinge de Gizeh representa el rostro del '
                             'faraón:',
                 'alternativas': ['Keops',
                                  'Micerino',
                                  'Tutmosis III',
                                  'Kefrén',
                                  'Ramsés II'],
                 'correcta': 'D'},
                {'pregunta': 'La escultura del «Escriba Sentado» representa '
                             'a un funcionario dedicado a:',
                 'alternativas': ['Cobrar impuestos exclusivamente',
                                  'Anotar los ingresos del reino',
                                  'Dirigir el ejército',
                                  'Presidir ceremonias religiosas',
                                  'Custodiar tumbas'],
                 'correcta': 'B'},
                {'pregunta': 'El artífice de la caída del Imperio Asirio, '
                             'gobernante del Segundo Imperio Babilónico, '
                             'fue:',
                 'alternativas': ['Nabucodonosor II',
                                  'Hammurabi',
                                  'Nabopolasar',
                                  'Asurbanipal',
                                  'Sargón'],
                 'correcta': 'C'},
                {'pregunta': 'Además de los toros alados y el príncipe '
                             'Gudea, la escultura mesopotámica destacó con '
                             'la estatua de:',
                 'alternativas': ['Nabopolasar',
                                  'Asurbanipal',
                                  'Nabucodonosor',
                                  'Sargón II',
                                  'El rey Hammurabi'],
                 'correcta': 'E'},
                {'pregunta': 'El faraón de la tercera dinastía, destacado '
                             'por el dominio del arte y la arquitectura '
                             'monumental en piedra, fue:',
                 'alternativas': ['Keops',
                                  'Dyeser (Zocer)',
                                  'Amenofis IV',
                                  'Kefrén',
                                  'Micerino'],
                 'correcta': 'B'},
                {'pregunta': 'Las tres pirámides colosales que datan del '
                             'Imperio Antiguo, previas a las de Guiza, '
                             'fueron construidas por:',
                 'alternativas': ['Keops',
                                  'Kefrén',
                                  'Tutmosis III',
                                  'Micerino',
                                  'Seneferu'],
                 'correcta': 'E'},
                {'pregunta': 'Los motivos florales esculpidos en los '
                             'capiteles egipcios incluían palmiformes, '
                             'papiriformes, atónicas y:',
                 'alternativas': ['Cactiformes',
                                  'Lotiformes (hoja de loto)',
                                  'Espinosos',
                                  'Rosáceos',
                                  'Ramiformes'],
                 'correcta': 'B'},
                {'pregunta': 'El motivo de capitel llamado «atónicas» hace '
                             'referencia al dios:',
                 'alternativas': ['Anubis', 'Atón', 'Ra', 'Osiris', 'Horus'],
                 'correcta': 'B'},
                {'pregunta': 'Además del Escriba Sentado, otras esculturas '
                             'egipcias representan a la reina Nefertiti y al '
                             'faraón:',
                 'alternativas': ['Micerino',
                                  'Keops',
                                  'Kefrén',
                                  'Amenofis',
                                  'Tutmosis III'],
                 'correcta': 'D'},
                {'pregunta': 'La escritura egipcia más antigua, usada en '
                             'tumbas y templos con imágenes de objetos, es '
                             'la escritura:',
                 'alternativas': ['Hierática',
                                  'Jeroglífica',
                                  'Cuneiforme',
                                  'Demótica',
                                  'Rúnica'],
                 'correcta': 'B'},
                {'pregunta': 'La piedra Rosetta, escrita en jeroglífico '
                             'egipcio, fue descifrada por el francés '
                             'Champollion en el año:',
                 'alternativas': ['1750', '1822', '1799', '1453', '1900'],
                 'correcta': 'B'},
                {'pregunta': 'La escritura egipcia empleada por escribas y '
                             'sacerdotes, más sencilla que la jeroglífica, '
                             'se llama escritura:',
                 'alternativas': ['Demótica',
                                  'Rúnica',
                                  'Jeroglífica',
                                  'Hierática',
                                  'Cuneiforme'],
                 'correcta': 'D'},
                {'pregunta': 'La escritura egipcia popular, la más simple, '
                             'utilizada por el pueblo, se llama escritura:',
                 'alternativas': ['Cuneiforme',
                                  'Jeroglífica',
                                  'Demótica',
                                  'Ideográfica',
                                  'Hierática'],
                 'correcta': 'C'},
                {'pregunta': 'En arquitectura, la cultura Mesopotámica '
                             'aportó: (UNSAAC 2010)',
                 'alternativas': ['La edificación de templos y tumbas',
                                  'La cúpula, el capitel y el arco',
                                  'La pirámide y las moradas de dioses',
                                  'La bóveda, la columna y cúpula',
                                  'El arco, la bóveda y la cúpula'],
                 'correcta': 'E'},
                {'pregunta': 'El teatro de planta circular y gradería '
                             'semicircular corresponde a la cultura: (UNSAAC '
                             '2010)',
                 'alternativas': ['Mesopotámica',
                                  'Griega',
                                  'Persa',
                                  'Caldeo Asiria',
                                  'Romana'],
                 'correcta': 'E'},
                {'pregunta': 'El Toro Alado con cabeza humana es una '
                             'expresión artística de la cultura: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Griega',
                                  'Mesopotámica',
                                  'Egipcia',
                                  'Romana',
                                  'China'],
                 'correcta': 'B'},
                {'pregunta': 'El arco, la bóveda y la cúpula son los aportes '
                             'arquitectónicos más importantes de la cultura: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Hindú',
                                  'Egipcia',
                                  'Griega',
                                  'Hebrea',
                                  'Mesopotámica'],
                 'correcta': 'E'},
                {'pregunta': 'El desciframiento de la escritura cuneiforme '
                             'mesopotámica de la Roca de Behistum '
                             'corresponde a: (UNSAAC Ordinario)',
                 'alternativas': ['Christian Thomsen',
                                  'Henry Rawlinson',
                                  'Francois Champollion',
                                  'Boucher de Perthes',
                                  'Jean Poirier'],
                 'correcta': 'B'},
                {'pregunta': 'Una de las características de la arquitectura '
                             'egipcia es que: (UNSAAC Ordinario)',
                 'alternativas': ['Exteriorizan afectos',
                                  'Expresan tristeza',
                                  'Expresan fielmente los sentimientos',
                                  'Poseen demasiado decorado',
                                  'Representan solidez y rigidez'],
                 'correcta': 'E'},
                {'pregunta': 'El testimonio arquitectónico que identifica a '
                             'la Cultura Egipcia, se evidencia por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Las estatuas, el discóbolo, Atenea y '
                                  'Marxias',
                                  'La construcción de Hemiciclos, teatros e '
                                  'hipódromos',
                                  'Las edificaciones de monumentos '
                                  'funerarios como hipogeos y mastabas',
                                  'La escultura de los reyes Sargón y '
                                  'Hammurabi',
                                  'Los Monumentos arquitectónicos como el '
                                  'Zigurat'],
                 'correcta': 'C'},
                {'pregunta': 'En la cultura egipcia, el culto al Dios Atón '
                             'se implantó en el periodo: (UNSAAC Ordinario)',
                 'alternativas': ['Bajo Imperio',
                                  'Imperio Medio',
                                  'Predinástico',
                                  'Imperio Nuevo',
                                  'Imperio Antiguo'],
                 'correcta': 'D'},
                {'pregunta': 'La arquitectura funeraria egipcia que sirvió '
                             'para el entierro de nobles y sacerdotes se '
                             'denomina: (UNSAAC Ordinario)',
                 'alternativas': ['Hipogeo',
                                  'Mastaba',
                                  'Templo',
                                  'Zigurat',
                                  'Pirámide'],
                 'correcta': 'B'},
                {'pregunta': 'Las ciudades de Kish, Ur y Uruk pertenecen a: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Sumeria',
                                  'Sumerio - Babilonio',
                                  'Babilonio - Caldeo',
                                  'Acadio - Nínive',
                                  'Nínive - Babilonio'],
                 'correcta': 'A'},
                {'pregunta': 'El Código de Hammurabi se desarrolló en el '
                             'proceso histórico de la Civilización '
                             'Mesopotámica, denominado: (UNSAAC Ordinario)',
                 'alternativas': ['Segundo Imperio Babilónico',
                                  'Primer Imperio Babilónico',
                                  'Imperio Caldeo - Asirio',
                                  'Imperio Antiguo',
                                  'Imperio Medo - Persa'],
                 'correcta': 'B'},
                {'pregunta': 'En la cultura mesopotámica, durante el Primer '
                             'Imperio Babilónico, el rey que unificó las '
                             'ciudades sumerias fue: (UNSAAC Ordinario)',
                 'alternativas': ['Asurbanipal',
                                  'Amenofis IV',
                                  'Nabopolasar',
                                  'Hammurabi',
                                  'Nabucodonosor II'],
                 'correcta': 'D'},
                {'pregunta': 'Mesopotamia significa región entre ríos según '
                             'los: (I CEPRU 2010)',
                 'alternativas': ['Mesopotámicos',
                                  'Griegos',
                                  'Egipcios',
                                  'Hebreos',
                                  'Romanos'],
                 'correcta': 'B'},
                {'pregunta': 'La escritura de Mesopotamia es: (I CEPRU 2010)',
                 'alternativas': ['Hierática',
                                  'Jeroglífica',
                                  'Cuneiforme',
                                  'Demótica',
                                  'Pallariforme'],
                 'correcta': 'C'},
                {'pregunta': 'En arquitectura la cultura mesopotámica aportó '
                             'al mundo: (I CEPRU 2011)',
                 'alternativas': ['Mastabas - Hipogeos - Pirámides',
                                  'Capiteles - palmiformes - lotiformes',
                                  'Dórico - jónico - corintio',
                                  'Arco - bóveda - cúpula',
                                  'Figuras humanas - la rueda - hojas de '
                                  'papiro'],
                 'correcta': 'D'},
                {'pregunta': 'La escritura caldeo-asiria fue: (I CEPRU 2011)',
                 'alternativas': ['Jeroglífica',
                                  'Cursiva',
                                  'Cuneiforme',
                                  'Demótica',
                                  'Hierática'],
                 'correcta': 'C'},
                {'pregunta': 'La edificación arquitectónica del Zigurat '
                             'corresponde a la cultura: (I CEPRU 2012)',
                 'alternativas': ['Griega',
                                  'Mesopotámica',
                                  'China',
                                  'Romana',
                                  'Egipcia'],
                 'correcta': 'B'},
                {'pregunta': 'En el periodo histórico del Imperio Medio de '
                             'Egipto los territorios conquistados fueron: (I '
                             'CEPRU 2012)',
                 'alternativas': ['Nubia, Libia y Siria',
                                  'Etolia y Tesalia',
                                  'Irak e Irán',
                                  'Mileto y Éfeso',
                                  'Creta, Delos y Samos'],
                 'correcta': 'A'},
                {'pregunta': 'La alta Mesopotamia se utilizó para fines '
                             'ganaderos y fue ocupada por la civilización: '
                             '(I CEPRU 2013)',
                 'alternativas': ['Acadia',
                                  'Sumeria',
                                  'Caldea',
                                  'Babilonia',
                                  'Asiria'],
                 'correcta': 'E'},
                {'pregunta': 'Las primeras unidades políticas de Mesopotamia '
                             'con gobierno autónomo se llamaban: (I CEPRU '
                             '2013)',
                 'alternativas': ['Estados consulados',
                                  'Burgos citadinos',
                                  'Aldeas tribales',
                                  'Ciudades estado',
                                  'Monarquías imperiales'],
                 'correcta': 'D'},
                {'pregunta': 'La escultura desarrollada por los '
                             'Mesopotámicos fue: (I CEPRU 2013)',
                 'alternativas': ['Monumental',
                                  'Colosal',
                                  'Religiosa',
                                  'Naturalista',
                                  'Realista'],
                 'correcta': 'B'},
                {'pregunta': 'Los egipcios realizaron grandes incursiones '
                             'militares conquistando Nubia, Libia y Siria '
                             'durante el imperio: (I CEPRU 2013)',
                 'alternativas': ['Babilónico',
                                  'Medio',
                                  'Nuevo',
                                  'Antiguo',
                                  'Semita'],
                 'correcta': 'B'}],
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
                {'titulo': '4.2 ORGANIZACIÓN POLÍTICA DE ESPARTA',
                 'items': ['{Esparta} y Atenas fueron llamadas por los '
                           'latinos «los ojos de {Grecia}».',
                           'Esparta era gobernada por una {diarquía} (dos '
                           'reyes) y un senado de 28 miembros llamado '
                           '{Gerusia}.',
                           'Los {éforos}, en número de 5, controlaban a los '
                           'reyes y votaban la guerra o la paz.',
                           '{Licurgo} fue quien sistematizó la organización '
                           'política espartana.']},
                {'titulo': '4.3 ORGANIZACIÓN POLÍTICA DE ATENAS',
                 'items': ['Atenas era gobernada por una {asamblea popular}, '
                           'que se reunía en el ágora para elegir arcontes.',
                           'El senado ateniense, llamado {Consejo de los '
                           'Cuatrocientos}, era presidido por un arconte.',
                           'El {areópago} tenía función judicial, integrado '
                           'por 9 arcontes que habían terminado su mandato.',
                           '{Solón} sistematizó la organización política '
                           'ateniense, legando a la humanidad el gobierno '
                           '{democrático}.']},
                {'titulo': '4.4 ORGANIZACIÓN SOCIAL GRIEGA',
                 'items': ['En Esparta, los {ilotas} eran siervos del Estado '
                           'sometidos a trato cruel; los {periecos} eran '
                           'habitantes sometidos pacíficamente.',
                           'En Atenas, los {metecos} eran extranjeros '
                           'radicados por negocios; los esclavos eran '
                           'prisioneros de guerra.']},
                {'titulo': '4.5 ARQUITECTURA GRIEGA',
                 'items': ['El {Partenón} fue erigido en honor a la diosa '
                           '{Atenea Pártenos}, tras la victoria en las '
                           'Guerras Médicas.',
                           'El orden {dórico} tiene columna sin base y '
                           'capitel cuadrado; es el más sobrio.',
                           'El orden {jónico} tiene columna con base y '
                           'capitel con dos {volutas}, más elegante.',
                           'El orden {corintio} es una variante del jónico, '
                           'con mayor ornamentación de hojas de {acanto}.']},
                {'titulo': '4.6 ESCULTURA GRIEGA',
                 'items': ['Las características de la escultura griega '
                           'fueron el {movimiento}, la proporción y la '
                           'belleza.',
                           '{Mirón} fue autor del Discóbolo; {Fidias}, autor '
                           'de los relieves del Partenón.',
                           '{Policleto} fijó las proporciones ideales del '
                           'cuerpo humano; Praxíteles delineó la curva de '
                           'los cuerpos.']},
                {'titulo': '4.7 ROMA — PROCESO HISTÓRICO',
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
                {'titulo': '4.8 ROMA: EXPRESIONES CULTURALES',
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
                 'alternativas': ['Solón',
                                  'Licurgo',
                                  'Pericles',
                                  'Clístenes',
                                  'Dracón'],
                 'correcta': 'A'},
                {'pregunta': 'El «Siglo de Oro» de Atenas corresponde al '
                             'gobierno de:',
                 'alternativas': ['Alejandro Magno',
                                  'Fidias',
                                  'Solón',
                                  'Pericles',
                                  'Licurgo'],
                 'correcta': 'D'},
                {'pregunta': 'Quien sistematizó la organización política de '
                             'Esparta fue:',
                 'alternativas': ['Solón',
                                  'Licurgo',
                                  'Dracón',
                                  'Rómulo',
                                  'Pericles'],
                 'correcta': 'B'},
                {'pregunta': 'Alejandro Magno extendió la cultura griega '
                             'hasta:',
                 'alternativas': ['Egipto',
                                  'China',
                                  'Hispania',
                                  'Britania',
                                  'La India'],
                 'correcta': 'E'},
                {'pregunta': 'Las ciudades-Estado griegas recibían el nombre '
                             'de:',
                 'alternativas': ['Demos',
                                  'Nomos',
                                  'Ayllus',
                                  'Civitas',
                                  'Polis'],
                 'correcta': 'E'},
                {'pregunta': 'El Partenón fue erigido en:',
                 'alternativas': ['La Acrópolis de Atenas',
                                  'Delfos',
                                  'Esparta',
                                  'Corinto',
                                  'Olimpia'],
                 'correcta': 'A'},
                {'pregunta': 'El autor de los relieves y metopas del '
                             'Partenón fue:',
                 'alternativas': ['Escopas',
                                  'Mirón',
                                  'Fidias',
                                  'Praxíteles',
                                  'Policleto'],
                 'correcta': 'C'},
                {'pregunta': 'A la muerte de Alejandro Magno, su imperio fue '
                             'repartido entre:',
                 'alternativas': ['Sus generales',
                                  'Sus hijos',
                                  'Los romanos',
                                  'Los persas',
                                  'El Senado'],
                 'correcta': 'A'},
                {'pregunta': 'Roma fue fundada, según la tradición, el año:',
                 'alternativas': ['509 a.C.',
                                  '27 a.C.',
                                  '476 d.C.',
                                  '753 a.C.',
                                  '146 a.C.'],
                 'correcta': 'D'},
                {'pregunta': 'El fundador legendario de Roma fue:',
                 'alternativas': ['Rómulo',
                                  'Tarquino el Soberbio',
                                  'Julio César',
                                  'Numa Pompilio',
                                  'Octavio Augusto'],
                 'correcta': 'A'},
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
                                  'Sabino',
                                  'Etrusco',
                                  'Cartaginés',
                                  'Galo'],
                 'correcta': 'C'},
                {'pregunta': 'El primer emperador romano fue:',
                 'alternativas': ['Octavio Augusto',
                                  'Constantino',
                                  'Nerón',
                                  'Julio César',
                                  'Trajano'],
                 'correcta': 'A'},
                {'pregunta': 'El periodo de estabilidad del Imperio Romano '
                             'se conoce como:',
                 'alternativas': ['Pax deorum',
                                  'Pax romana',
                                  'Pax augusta',
                                  'Imperium',
                                  'Res publica'],
                 'correcta': 'B'},
                {'pregunta': 'La República romana comprende el periodo:',
                 'alternativas': ['753–509 a.C.',
                                  '800–494 a.C.',
                                  '359–146 a.C.',
                                  '27 a.C.–476 d.C.',
                                  '509–27 a.C.'],
                 'correcta': 'E'},
                {'pregunta': 'Con Rómulo se iniciaron en Roma dos '
                             'instituciones:',
                 'alternativas': ['El consulado y la dictadura',
                                  'La asamblea y el Senado',
                                  'El tribunado y la censura',
                                  'El imperio y la provincia',
                                  'La pretura y la edilidad'],
                 'correcta': 'B'},
                {'pregunta': 'La crisis del Imperio Romano, desde el siglo '
                             'III d.C., incluyó un proceso de:',
                 'alternativas': ['Expansión territorial',
                                  'Urbanización acelerada',
                                  'Helenización',
                                  'Democratización',
                                  'Ruralización'],
                 'correcta': 'E'},
                {'pregunta': 'Grecia se desarrolló en el sur de la '
                             'península:',
                 'alternativas': ['Ibérica',
                                  'De Anatolia',
                                  'De los Balcanes',
                                  'Escandinava',
                                  'Itálica'],
                 'correcta': 'C'},
                {'pregunta': 'La caída del Imperio Romano de Occidente se '
                             'fija en el año:',
                 'alternativas': ['27 a.C.',
                                  '1453 d.C.',
                                  '146 a.C.',
                                  '476 d.C.',
                                  '509 a.C.'],
                 'correcta': 'D'},
                {'pregunta': 'El periodo helenístico de Grecia abarca los '
                             'años:',
                 'alternativas': ['359–146 a.C.',
                                  '800–494 a.C.',
                                  '146 a.C.–27 a.C.',
                                  '494–359 a.C.',
                                  '753–509 a.C.'],
                 'correcta': 'A'},
                {'pregunta': 'El derecho romano se define como una '
                             'compilación de leyes, tratados y:',
                 'alternativas': ['Monedas',
                                  'Normativas',
                                  'Religiones',
                                  'Territorios',
                                  'Idiomas'],
                 'correcta': 'B'},
                {'pregunta': 'Según Tito Livio, la fuente de todo el derecho '
                             'romano fue:',
                 'alternativas': ['El Edicto de Milán',
                                  'La Ley de las 12 Tablas',
                                  'El Derecho Pretorio',
                                  'El Código de Justiniano',
                                  'La Lex Canuleia'],
                 'correcta': 'B'},
                {'pregunta': 'El derecho romano es considerado el aporte más '
                             'grande de Roma a:',
                 'alternativas': ['Solo el Imperio',
                                  'La humanidad',
                                  'Solo la Iglesia',
                                  'Solo Europa',
                                  'Solo Italia'],
                 'correcta': 'B'},
                {'pregunta': 'El emperador considerado el padre del derecho '
                             'romano por su labor legislativa fue:',
                 'alternativas': ['Trajano',
                                  'Nerón',
                                  'Augusto',
                                  'Justiniano',
                                  'Adriano'],
                 'correcta': 'D'},
                {'pregunta': 'En arquitectura, los romanos introdujeron de '
                             'mesopotámicos y etruscos el arco, la bóveda y:',
                 'alternativas': ['La cúpula',
                                  'El obelisco',
                                  'El capitel dórico exclusivo',
                                  'La pirámide',
                                  'El zigurat'],
                 'correcta': 'A'},
                {'pregunta': 'Los romanos utilizaron como materiales de '
                             'construcción piedra, ladrillo y:',
                 'alternativas': ['Barro cocido exclusivamente',
                                  'Bronce exclusivo',
                                  'Madera exclusivamente',
                                  'Vidrio',
                                  'Hormigón con cal como argamasa'],
                 'correcta': 'E'},
                {'pregunta': 'El Coliseo Romano también es conocido como:',
                 'alternativas': ['El Anfiteatro de Flavio',
                                  'El Foro Romano',
                                  'El Circo Máximo',
                                  'La Basílica de Majencio',
                                  'El Panteón'],
                 'correcta': 'A'},
                {'pregunta': 'Entre las construcciones romanas más '
                             'representativas, además del Coliseo, están el '
                             'Arco de Tito y el Arco de:',
                 'alternativas': ['Trajano',
                                  'Vespasiano',
                                  'Domiciano',
                                  'Adriano',
                                  'Constantino exclusivamente'],
                 'correcta': 'A'},
                {'pregunta': 'En la arquitectura griega, la riqueza '
                             'ornamental con flores de acanto pertenece al '
                             'orden: (UNSAAC 2011)',
                 'alternativas': ['Dórico',
                                  'Compuesto',
                                  'Mixto',
                                  'Jónico',
                                  'Corintio'],
                 'correcta': 'E'},
                {'pregunta': 'La obra escultórica el Discóbolo, de la '
                             'antigua Grecia, fue obra del artista: (UNSAAC '
                             '2013)',
                 'alternativas': ['Praxiteles',
                                  'Policleto',
                                  'Mirón',
                                  'Fidias',
                                  'Lisipo'],
                 'correcta': 'C'},
                {'pregunta': 'En la cultura romana antigua, Cerdeña formaba '
                             'parte de la zona: (UNSAAC 2013)',
                 'alternativas': ['Septentrional',
                                  'Insular',
                                  'Continental',
                                  'Meridional',
                                  'Peninsular'],
                 'correcta': 'B'},
                {'pregunta': 'El último emperador romano, Rómulo Augústulo, '
                             'fue destronado por Odoacro, rey de los '
                             'bárbaros: (UNSAAC 2013)',
                 'alternativas': ['Vándalos',
                                  'Visigodos',
                                  'Hérulos',
                                  'Ostrogodos',
                                  'Hunos'],
                 'correcta': 'C'},
                {'pregunta': 'El Derecho Romano, uno de los logros y aportes '
                             'más importantes a la humanidad, se caracteriza '
                             'por ser: (UNSAAC 2013)',
                 'alternativas': ['Consuetudinario y elemental',
                                  'Democrático y bondadoso',
                                  'Humanitario y generoso',
                                  'Coercitivo y liberal',
                                  'Elitista y racista'],
                 'correcta': 'C'},
                {'pregunta': 'Los gobernantes del Periodo Republicano de '
                             'Roma Antigua se denominaron: (UNSAAC 2016)',
                 'alternativas': ['Cónsules',
                                  'Reyes',
                                  'Presidentes',
                                  'Emperadores',
                                  'Gobernadores'],
                 'correcta': 'A'},
                {'pregunta': 'En el periodo histórico de Grecia Clásica, '
                             'Atenas se caracterizó por ser: (UNSAAC 2016)',
                 'alternativas': ['Democrática',
                                  'Autoritaria',
                                  'Militarizada',
                                  'Plutocrática',
                                  'Gerontocrática'],
                 'correcta': 'A'},
                {'pregunta': 'La Ley de las doce tablas fue la base del '
                             'Derecho Romano, según el historiador: (UNSAAC '
                             '2016)',
                 'alternativas': ['Jenofonte',
                                  'Tito Livio',
                                  'Tácito',
                                  'Heródoto',
                                  'Tucídides'],
                 'correcta': 'B'},
                {'pregunta': 'Los tres poderes: el Senado, las Asambleas y '
                             'la Magistratura, en la Roma Antigua, '
                             'correspondieron a la forma de gobierno: '
                             '(UNSAAC 2018)',
                 'alternativas': ['Monárquico',
                                  'Imperial',
                                  'Autónomo',
                                  'Autocrático',
                                  'Republicano'],
                 'correcta': 'E'},
                {'pregunta': 'En la arquitectura griega, el teatro de planta '
                             'circular, el estadio y el hipódromo '
                             'correspondieron al tipo de construcción: '
                             '(UNSAAC 2018)',
                 'alternativas': ['Familiar',
                                  'Militar',
                                  'Civil',
                                  'Individual',
                                  'Religioso'],
                 'correcta': 'C'},
                {'pregunta': 'Después de su máximo esplendor y poder, la '
                             'Roma Republicana pasó al periodo imperial, '
                             'cuyo primer emperador fue: (UNSAAC 2022)',
                 'alternativas': ['Marco Antonio',
                                  'Rómulo Augústulo',
                                  'Teodosio',
                                  'César Augusto',
                                  'Julio César'],
                 'correcta': 'D'},
                {'pregunta': 'Las ciudades de Mileto, Éfeso y otras, fueron '
                             'constituidas en la región de la Grecia: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Jónica',
                                  'Peninsular',
                                  'Balcánica',
                                  'Insular',
                                  'Continental'],
                 'correcta': 'A'},
                {'pregunta': 'Uno de los aportes de Roma Antigua a la '
                             'humanidad, es: (UNSAAC Ordinario)',
                 'alternativas': ['La cerámica',
                                  'La biología',
                                  'La astronomía',
                                  'El derecho',
                                  'La democracia'],
                 'correcta': 'D'},
                {'pregunta': 'En el periodo republicano de Roma antigua, los '
                             'gobernantes se denominaron: (UNSAAC Ordinario)',
                 'alternativas': ['Reyes',
                                  'Monarcas',
                                  'Cónsules',
                                  'Emperadores',
                                  'Presidentes'],
                 'correcta': 'C'},
                {'pregunta': 'El origen del pueblo griego se encuentra en '
                             'los: (UNSAAC Ordinario)',
                 'alternativas': ['Pelasgos',
                                  'Cretenses',
                                  'Corintios',
                                  'Atenienses',
                                  'Jónicos'],
                 'correcta': 'A'},
                {'pregunta': 'El Rey Minos representó al proceso histórico '
                             'de la civilización correspondiente a: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Grecia Arcaica o Heroica',
                                  'La época oscura de la Cultura Griega',
                                  'Grecia Helenística o decadente',
                                  'Grecia Clásica o de Apogeo',
                                  'La Cretense o Minoica'],
                 'correcta': 'E'},
                {'pregunta': 'En el proceso histórico de Roma imperial, la '
                             'muerte del emperador Teodosio trajo como '
                             'consecuencia la división del imperio entre sus '
                             'hijos: (UNSAAC Ordinario)',
                 'alternativas': ['Servio Tulio - Tarquino el Soberbio',
                                  'Pericles - Hugo Hostilio',
                                  'Anco Marcio - Tarquino el Soberbio',
                                  'Rómulo - Numa Pompilio',
                                  'Honorio - Arcadio'],
                 'correcta': 'E'},
                {'pregunta': 'Las ciudades de Mileto, Éfeso y Halicarnaso se '
                             'ubicaron en la región de la Grecia: (I CEPRU '
                             '2010)',
                 'alternativas': ['Continental',
                                  'Jónica',
                                  'Insular',
                                  'Dórica',
                                  'Helénica'],
                 'correcta': 'B'},
                {'pregunta': 'En la Grecia Jónica, los griegos fundaron '
                             'ciudades como: (I CEPRU 2011)',
                 'alternativas': ['Delos - Etolia',
                                  'Creta - Delos',
                                  'Etolia - Tesalia',
                                  'Mileto - Éfeso',
                                  'Samos - Etolia'],
                 'correcta': 'D'},
                {'pregunta': 'En la Cultura Griega, Mirón fue autor de la '
                             'obra: (I CEPRU 2011)',
                 'alternativas': ['Figuras más esbeltas',
                                  'Curvo de los cuerpos',
                                  'Relieves de los frontones',
                                  'Proporciones ideales del cuerpo',
                                  'Discóbolo'],
                 'correcta': 'E'},
                {'pregunta': 'En la escultura griega el autor del Discóbolo '
                             'es: (I CEPRU 2012)',
                 'alternativas': ['Lisipo',
                                  'Policleto',
                                  'Mirón',
                                  'Fidias',
                                  'Praxíteles'],
                 'correcta': 'C'},
                {'pregunta': 'La cultura romana se desarrolló en la '
                             'península: (I CEPRU 2012)',
                 'alternativas': ['De los Balcanes',
                                  'Itálica',
                                  'Griega',
                                  'De Peloponeso',
                                  'Ibérica'],
                 'correcta': 'B'},
                {'pregunta': 'En el periodo republicano de Roma fue '
                             'gobernada por: (I CEPRU 2012)',
                 'alternativas': ['Condes',
                                  'Emperadores',
                                  'Monarcas',
                                  'Reyes',
                                  'Cónsules'],
                 'correcta': 'E'},
                {'pregunta': 'La cultura que incorporó en sus construcciones '
                             'arquitectónicas, las columnas y capiteles '
                             'griegos: (I CEPRU 2014)',
                 'alternativas': ['Babilónica',
                                  'Romana',
                                  'Egipcia',
                                  'Hebrea',
                                  'Mesopotámica'],
                 'correcta': 'B'},
                {'pregunta': 'Las dos ciudades-Estado griegas más '
                             'importantes, llamadas por los latinos «los '
                             'ojos de Grecia», fueron:',
                 'alternativas': ['Atenas y Tebas',
                                  'Corinto y Esparta',
                                  'Esparta y Atenas',
                                  'Esparta y Tebas',
                                  'Atenas y Corinto'],
                 'correcta': 'C'},
                {'pregunta': 'Esparta era gobernada por una diarquía y un '
                             'senado de 28 miembros llamado:',
                 'alternativas': ['Boulé',
                                  'Ecclesia',
                                  'Ágora',
                                  'Gerusia',
                                  'Areópago'],
                 'correcta': 'D'},
                {'pregunta': 'Los funcionarios espartanos, en número de 5, '
                             'que controlaban a los reyes y votaban la '
                             'guerra o la paz, eran los:',
                 'alternativas': ['Senadores',
                                  'Arcontes',
                                  'Éforos',
                                  'Estrategas',
                                  'Cónsules'],
                 'correcta': 'C'},
                {'pregunta': 'Quien sistematizó la organización política de '
                             'Esparta fue:',
                 'alternativas': ['Solón',
                                  'Licurgo',
                                  'Pericles',
                                  'Dracón',
                                  'Clístenes'],
                 'correcta': 'B'},
                {'pregunta': 'El senado ateniense, presidido por un arconte, '
                             'se llamaba:',
                 'alternativas': ['Ágora',
                                  'Ecclesia',
                                  'Gerusia',
                                  'Areópago',
                                  'Consejo de los Cuatrocientos'],
                 'correcta': 'E'},
                {'pregunta': 'Quien sistematizó la organización política '
                             'ateniense, legando el gobierno democrático, '
                             'fue:',
                 'alternativas': ['Licurgo',
                                  'Solón',
                                  'Temístocles',
                                  'Dracón',
                                  'Pericles'],
                 'correcta': 'B'},
                {'pregunta': 'En Esparta, los siervos del Estado sometidos a '
                             'trato cruel e inhumano se llamaban:',
                 'alternativas': ['Metecos',
                                  'Ilotas',
                                  'Espartanos',
                                  'Periecos',
                                  'Hilotas libres'],
                 'correcta': 'B'},
                {'pregunta': 'En Atenas, los extranjeros radicados por '
                             'poseer negocios o industria se llamaban:',
                 'alternativas': ['Metecos',
                                  'Ciudadanos',
                                  'Periecos',
                                  'Ilotas',
                                  'Esclavos'],
                 'correcta': 'A'},
                {'pregunta': 'El templo griego erigido en honor a la diosa '
                             'Atenea, tras la victoria en las Guerras '
                             'Médicas, fue:',
                 'alternativas': ['El templo de Zeus',
                                  'La Basílica',
                                  'El Poseidonion',
                                  'El Partenón',
                                  'El Erecteión'],
                 'correcta': 'D'},
                {'pregunta': 'El orden arquitectónico griego con columna sin '
                             'base y capitel de forma cuadrada es el:',
                 'alternativas': ['Dórico',
                                  'Compuesto',
                                  'Toscano',
                                  'Corintio',
                                  'Jónico'],
                 'correcta': 'A'},
                {'pregunta': 'El orden arquitectónico griego más '
                             'ornamentado, con hojas de acanto superpuestas, '
                             'es el:',
                 'alternativas': ['Dórico',
                                  'Jónico',
                                  'Toscano',
                                  'Compuesto',
                                  'Corintio'],
                 'correcta': 'E'},
                {'pregunta': 'El escultor griego autor del Discóbolo fue:',
                 'alternativas': ['Policleto',
                                  'Fidias',
                                  'Lisipo',
                                  'Praxíteles',
                                  'Mirón'],
                 'correcta': 'E'},
                {'pregunta': 'El escultor griego que fijó las proporciones '
                             'ideales del cuerpo humano fue:',
                 'alternativas': ['Escopas',
                                  'Fidias',
                                  'Praxíteles',
                                  'Policleto',
                                  'Mirón'],
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
                     {'titulo': 'ORGANIZACIÓN POLÍTICA DE ESPARTA',
                      'items': ['Esparta y Atenas fueron llamadas por los '
                                'latinos «los ojos de Grecia».',
                                'Esparta era gobernada por una diarquía (dos '
                                'reyes) y un senado de 28 miembros llamado '
                                'Gerusia.',
                                'Los éforos, en número de 5, controlaban a '
                                'los reyes y votaban la guerra o la paz.',
                                'Licurgo fue quien sistematizó la '
                                'organización política espartana.']},
                     {'titulo': 'ORGANIZACIÓN POLÍTICA DE ATENAS',
                      'items': ['Atenas era gobernada por una asamblea '
                                'popular, que se reunía en el ágora para '
                                'elegir arcontes.',
                                'El senado ateniense, llamado Consejo de los '
                                'Cuatrocientos, era presidido por un '
                                'arconte.',
                                'El areópago tenía función judicial, '
                                'integrado por 9 arcontes que habían '
                                'terminado su mandato.',
                                'Solón sistematizó la organización política '
                                'ateniense, legando a la humanidad el '
                                'gobierno democrático.']},
                     {'titulo': 'ORGANIZACIÓN SOCIAL GRIEGA',
                      'items': ['En Esparta, los ilotas eran siervos del '
                                'Estado sometidos a trato cruel; los '
                                'periecos eran habitantes sometidos '
                                'pacíficamente.',
                                'En Atenas, los metecos eran extranjeros '
                                'radicados por negocios; los esclavos eran '
                                'prisioneros de guerra.']},
                     {'titulo': 'ARQUITECTURA GRIEGA',
                      'items': ['El Partenón fue erigido en honor a la diosa '
                                'Atenea Pártenos, tras la victoria en las '
                                'Guerras Médicas.',
                                'El orden dórico tiene columna sin base y '
                                'capitel cuadrado; es el más sobrio.',
                                'El orden jónico tiene columna con base y '
                                'capitel con dos volutas, más elegante.',
                                'El orden corintio es una variante del '
                                'jónico, con mayor ornamentación de hojas de '
                                'acanto.']},
                     {'titulo': 'ESCULTURA GRIEGA',
                      'items': ['Las características de la escultura griega '
                                'fueron el movimiento, la proporción y la '
                                'belleza.',
                                'Mirón fue autor del Discóbolo; Fidias, '
                                'autor de los relieves del Partenón.',
                                'Policleto fijó las proporciones ideales del '
                                'cuerpo humano; Praxíteles delineó la curva '
                                'de los cuerpos.']},
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
                                'argamasa.']}],
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
                {'titulo': '5.2 TEORÍA AUTOCTONISTA',
                 'items': ['La teoría {autoctonista} fue planteada por el '
                           'argentino {Florentino Ameghino} en 1879.',
                           'Sostenía que el hombre americano se originó en '
                           'las {Pampas Argentinas}, en Chapalmalal, '
                           'dispersándose por «puentes intercontinentales».',
                           'Ameghino basó su teoría en fósiles que llamó '
                           '«{Protohomo Pampeanus}» (Hombre de la Pampa).',
                           'Fue rebatida en 1908 por {Alex Hrdlicka}, quien '
                           'demostró que los fósiles eran de animales de la '
                           'era Cuaternaria, no Terciaria.']},
                {'titulo': '5.3 TEORÍA DEL ORIGEN ASIÁTICO',
                 'items': ['La teoría del {origen asiático}, monogenista, '
                           'fue sustentada en 1917 por {Alex Hrdlicka}.',
                           'Sostuvo que grupos paleomongoloides inmigraron a '
                           'América por el Estrecho de {Behring}.',
                           'Su prueba geográfica es la glaciación de '
                           '{Wisconsin} y el corredor natural del Estrecho '
                           'de Behring.',
                           'Sus pruebas antroposomáticas incluyen el cabello '
                           'grueso y negro, los ojos {rasgados}, y la mancha '
                           'mongólica en el coxis.']},
                {'titulo': '5.4 TEORÍA DEL ORIGEN OCEÁNICO',
                 'items': ['La teoría del {origen oceánico}, poligenista, '
                           'fue sustentada por el francés {Paul Rivet} en '
                           '1943.',
                           'La procedencia {melanésica} cruzó el Pacífico '
                           'por las corrientes nor ecuatoriales; sus pruebas '
                           'incluyen semejanzas con cráneos de Lagoa Santa '
                           '(Brasil).',
                           'La procedencia {polinésica} pasó por la Isla de '
                           'Pascua, impulsada por la corriente Sur '
                           'Ecuatorial.',
                           'Entre las pruebas polinésicas están semejanzas '
                           'lingüísticas con el quechua y el uso compartido '
                           'de la {pachamanca}.']},
                {'titulo': '5.5 TEORÍA DEL ORIGEN AUSTRALIANO',
                 'items': ['La teoría del {origen australiano} fue sostenida '
                           'por el portugués {Antonio Méndez Correa} en '
                           '1925.',
                           'Los australianos habrían viajado en balsas por '
                           'Tasmania y la {Antártida} hasta llegar a Tierra '
                           'del Fuego y la Patagonia.',
                           'Sus pruebas incluyen semejanza craneal '
                           '{dolicocéfalo}, tipo sanguíneo O+, y palabras '
                           'similares entre fueguinos y australianos.',
                           'Entre sus elementos culturales compartidos están '
                           'el {boomerang} y el churinga o zumbador '
                           'ritual.']},
                {'titulo': '5.6 NÓMADAS: PACCAICASA Y CHIVATEROS',
                 'items': ['{Paccaicasa}, en Ayacucho, estudiado por Richard '
                           'Mac Neish, data de 20 000 años a.C.; da inicio a '
                           'la gran cultura andina.',
                           '{Chivateros}, en el río Chillón (Lima), '
                           'estudiado por Edward Lanning y Patterson, data '
                           'de 10 000 años a.C.',
                           'Chivateros representa al poblador más antiguo de '
                           'la {costa} peruana, con el taller lítico más '
                           'grande del Perú antiguo.']},
                {'titulo': '5.7 NÓMADAS: TOQUEPALA Y LAURICOCHA',
                 'items': ['{Toquepala}, en Tacna, estudiado por Miomir '
                           'Bojovich y Emilio González, data de 9525 años '
                           'a.C.',
                           'Toquepala presenta el {arte rupestre} más '
                           'antiguo del Perú, con pinturas de caza de '
                           'vicuñas y guanacos.',
                           '{Lauricocha}, en Huánuco, estudiado por Augusto '
                           'Cardich, data de 9500 años a.C.',
                           'En Lauricocha se hallaron los primeros restos '
                           'óseos humanos del Perú: {11} esqueletos, de '
                           'cráneo dolicocéfalo.']},
                {'titulo': '5.8 NÓMADAS: PAIJÁN',
                 'items': ['{Paiján}, en La Libertad, estudiado por Rafael '
                           'Larco Hoyle, data de 8000 años a.C.',
                           'En Paiján se encontraron esqueletos completos: '
                           'una mujer de {25} años y un niño de 12.',
                           'Los pobladores de Paiján fueron {pescadores} y '
                           'rendían culto a sus muertos.']},
                {'titulo': '5.9 SEMINÓMADAS: NANCHOC Y GUITARRERO',
                 'items': ['{Nanchoc}, en Cajamarca, estudiado por Tom '
                           'Dillehay, data de 8000-7000 años a.C.; primer '
                           'horticultor del Perú, de calabaza y algodón.',
                           '{Guitarrero}, en Áncash, estudiado por Thomas '
                           'Lynch, es el segundo horticultor del Perú, de '
                           'leguminosas y frijoles.',
                           'Los pobladores de Guitarrero son considerados '
                           '{precursores} de la agricultura en el Perú; '
                           'sepultaban a sus muertos.']},
                {'titulo': '5.10 SEMINÓMADAS: SANTO DOMINGO Y CHILCA',
                 'items': ['{Santo Domingo}, en Paracas (Ica), estudiado por '
                           'Frederic Engel, data de 6000 años a.C.; tercer '
                           'horticultor del Perú.',
                           'En Santo Domingo se halló al primer {pescador '
                           'con red} y primer músico del Perú, con las '
                           'flautas más antiguas.',
                           '{Chilca}, al sur de Lima, estudiado por Frederic '
                           'Engel, data de 5500 años a.C.',
                           'En Chilca se domesticó al {perro}, y los muertos '
                           'eran atados con cuerdas y envueltos en '
                           'esteras.']},
                {'titulo': '5.11 SEMINÓMADAS: PIQUIMACHAY Y TELARMACHAY',
                 'items': ['{Piquimachay}, en Ayacucho, estudiado por '
                           'Richard Mac Neish, data de 3300 años a.C.',
                           'Piquimachay evidencia la primera domesticación '
                           'de la {llama}, alpaca y cuy.',
                           '{Telarmachay}, en Junín, estudiado por Danielle '
                           'Lavallée, data de 3000 años a.C.',
                           'En Telarmachay se evidencia el paso de cazadores '
                           'a {pastores}, y la primera domesticación de la '
                           'papa y oca.']},
                {'titulo': '5.12 SEDENTARIOS: LURÍN Y HUACA PRIETA',
                 'items': ['{Lurín}, al sur de Lima, estudiado por Josefina '
                           'Ramos de Cox, data de 3000 años a.C.; primer '
                           'arquitecto del Perú.',
                           '{Huaca Prieta}, en Chicama (La Libertad), '
                           'estudiado por Junius Bird, data de 2500 años '
                           'a.C.',
                           'Los pobladores de Huaca Prieta fueron los '
                           'primeros maestros del {arte textil}, con la '
                           'figura del «primer cóndor andino».']},
                {'titulo': '5.13 SEDENTARIOS: KOTOSH',
                 'items': ['{Kotosh}, en Huánuco, fue estudiado por Julio C. '
                           'Tello y Seichi Izumi; data de 2200 años a.C.',
                           'Es considerado el primer {monumento religioso} '
                           'de América, pionero en construir templos sobre '
                           'templos más antiguos.',
                           'En Kotosh se construyó el {Templo de las Manos '
                           'Cruzadas}, recinto con dos manos esculpidas en '
                           'arcilla.',
                           'Fue una sociedad agrícola cultivadora de '
                           '{algodón}, que practicaba ritos a la tierra.']},
                {'titulo': '5.14 SEDENTARIOS: LAS HALDAS Y CERRO PALOMA',
                 'items': ['{Las Haldas}, en Casma (Áncash), estudiado por '
                           'Rosa Fung Pineda, data de 1600 años a.C.; inicio '
                           'de la primera etapa alfarera.',
                           '{Cerro Paloma}, en Lima, estudiado por Frederic '
                           'Engel, data de 1500 años a.C.',
                           'En Cerro Paloma se hallaron las primeras {redes '
                           'de pescar} hechas de algodón, junto con anzuelos '
                           'y cordeles.']}],
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
                 'alternativas': ['Paul Rivet',
                                  'Florentino Ameghino',
                                  'Mendes Correa',
                                  'Alex Hrdlicka',
                                  'Julio C. Tello'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría autoctonista fue rebatida en 1908 '
                             'por:',
                 'alternativas': ['Thomas Lynch',
                                  'Richard MacNeish',
                                  'Paul Rivet',
                                  'Alex Hrdlicka',
                                  'Augusto Cardich'],
                 'correcta': 'D'},
                {'pregunta': 'Según Hrdlicka, el poblamiento de América se '
                             'produjo a través del:',
                 'alternativas': ['Estrecho de Bering',
                                  'Océano Atlántico',
                                  'Mar de Behring meridional',
                                  'Istmo de Panamá',
                                  'Océano Pacífico'],
                 'correcta': 'A'},
                {'pregunta': 'La teoría de origen oceánico fue sustentada '
                             'por:',
                 'alternativas': ['Hrdlicka',
                                  'Paul Rivet',
                                  'Mendes Correa',
                                  'Uhle',
                                  'Ameghino'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de origen australiano se atribuye a:',
                 'alternativas': ['Mendes Correa',
                                  'Lynch',
                                  'Paul Rivet',
                                  'Ameghino',
                                  'Hrdlicka'],
                 'correcta': 'A'},
                {'pregunta': 'Los restos líticos más antiguos del Perú se '
                             'hallaron en:',
                 'alternativas': ['Guitarrero',
                                  'Lauricocha',
                                  'Toquepala',
                                  'Paccaicasa',
                                  'Kotosh'],
                 'correcta': 'D'},
                {'pregunta': 'El arte rupestre más antiguo del Perú '
                             'corresponde a:',
                 'alternativas': ['Lauricocha',
                                  'Toquepala',
                                  'Paccaicasa',
                                  'Kotosh',
                                  'Paracas'],
                 'correcta': 'B'},
                {'pregunta': 'Los primeros restos óseos humanos del Perú se '
                             'encontraron en:',
                 'alternativas': ['Toquepala',
                                  'Chilca',
                                  'Lauricocha',
                                  'Guitarrero',
                                  'Paccaicasa'],
                 'correcta': 'C'},
                {'pregunta': 'Los primeros indicios de agricultura en el '
                             'Perú se hallaron en:',
                 'alternativas': ['Paccaicasa',
                                  'Toquepala',
                                  'Guitarrero',
                                  'Lauricocha',
                                  'Kotosh'],
                 'correcta': 'C'},
                {'pregunta': 'El Templo de las Manos Cruzadas pertenece a:',
                 'alternativas': ['Caral',
                                  'Chavín',
                                  'Kotosh',
                                  'Sechín',
                                  'Paracas'],
                 'correcta': 'C'},
                {'pregunta': 'Kotosh fue estudiado por:',
                 'alternativas': ['Julio C. Tello',
                                  'Rafael Larco',
                                  'Ruth Shady',
                                  'Federico Kauffmann',
                                  'Max Uhle'],
                 'correcta': 'A'},
                {'pregunta': 'El periodo se denomina precerámico porque:',
                 'alternativas': ['No se conocía la agricultura',
                                  'No existía la textilería',
                                  'No se domesticaban animales',
                                  'Aún no se conocía la cerámica',
                                  'No había arquitectura'],
                 'correcta': 'D'},
                {'pregunta': 'El chaco representado en Toquepala consistía '
                             'en:',
                 'alternativas': ['Un intercambio comercial',
                                  'Una caza ritual colectiva',
                                  'Una ceremonia funeraria',
                                  'Una danza guerrera',
                                  'Un ritual de siembra'],
                 'correcta': 'B'},
                {'pregunta': 'Ameghino sostuvo que los restos fósiles '
                             'correspondían a la Era:',
                 'alternativas': ['Secundaria',
                                  'Primaria',
                                  'Terciaria',
                                  'Cuaternaria',
                                  'Precámbrica'],
                 'correcta': 'C'},
                {'pregunta': 'El periodo de los nómadas andinos se '
                             'caracterizó por ser:',
                 'alternativas': ['Metalurgistas',
                                  'Recolectores, cazadores y pescadores',
                                  'Comerciantes',
                                  'Agricultores sedentarios',
                                  'Ganaderos y alfareros'],
                 'correcta': 'B'},
                {'pregunta': 'Guitarrero se ubica en el actual departamento '
                             'de:',
                 'alternativas': ['Huánuco',
                                  'Ica',
                                  'Tacna',
                                  'Áncash',
                                  'Ayacucho'],
                 'correcta': 'D'},
                {'pregunta': 'Paccaicasa se ubica en:',
                 'alternativas': ['Tacna',
                                  'Ayacucho',
                                  'Lima',
                                  'Huánuco',
                                  'Áncash'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de Paul Rivet propone una '
                             'procedencia melanésica y:',
                 'alternativas': ['Africana',
                                  'Polinésica',
                                  'Europea',
                                  'Asiática',
                                  'Australiana'],
                 'correcta': 'B'},
                {'pregunta': 'Toquepala se ubica en el departamento de:',
                 'alternativas': ['Tacna',
                                  'Arequipa',
                                  'Ica',
                                  'Moquegua',
                                  'Puno'],
                 'correcta': 'A'},
                {'pregunta': 'En Paracas, durante el precerámico, se '
                             'registró la recolección de:',
                 'alternativas': ['Coca y ají únicamente',
                                  'Tomatillos, yuca y algodón',
                                  'Trigo y cebada',
                                  'Papa y oca',
                                  'Maíz y quinua'],
                 'correcta': 'B'},
                {'pregunta': 'El poblamiento de América ocurrió como '
                             'consecuencia del antiguo proceso de:',
                 'alternativas': ['Comercio marítimo',
                                  'Intercambio cultural',
                                  'Migración de la especie humana',
                                  'Guerra intercontinental',
                                  'Colonización europea'],
                 'correcta': 'C'},
                {'pregunta': 'Los drásticos cambios climáticos que '
                             'influyeron en el poblamiento de América '
                             'ocurrieron durante el periodo:',
                 'alternativas': ['Holoceno',
                                  'Cuaternario tardío exclusivo',
                                  'Pleistoceno',
                                  'Terciario',
                                  'Mioceno'],
                 'correcta': 'C'},
                {'pregunta': 'El poblamiento del continente americano se '
                             'remonta cronológicamente a aproximadamente:',
                 'alternativas': ['5000 a.C.',
                                  '60 000 a.C.',
                                  '10 000 a.C.',
                                  '1000 a.C.',
                                  '100 000 a.C.'],
                 'correcta': 'B'},
                {'pregunta': 'Entre las altas culturas que se desarrollaron '
                             'en América tras el poblamiento destacan '
                             'aztecas, mayas e:',
                 'alternativas': ['Incas',
                                  'Sumerios',
                                  'Egipcios',
                                  'Persas',
                                  'Fenicios'],
                 'correcta': 'A'},
                {'pregunta': 'El interés por conocer el origen del hombre '
                             'americano surgió especialmente tras:',
                 'alternativas': ['El descubrimiento del petróleo',
                                  'La llegada de los europeos a fines del '
                                  'siglo XV',
                                  'La Revolución Industrial',
                                  'La Segunda Guerra Mundial',
                                  'La independencia de las colonias'],
                 'correcta': 'B'},
                {'pregunta': 'Al poblar América, los melanesios llegaron a: '
                             '(UNSAAC 2010)',
                 'alternativas': ['Norteamérica',
                                  'Centroamérica',
                                  'Las islas Aleutianas',
                                  'Sudamérica',
                                  'La isla de Pascua'],
                 'correcta': 'D'},
                {'pregunta': 'En su viaje hacia América, los australianos '
                             'cruzaron: (UNSAAC 2010)',
                 'alternativas': ['Isla de Puna y América del Norte',
                                  'El estrecho de Bering',
                                  'Centroamérica y la Antártica',
                                  'La Antártida, Tierra del Fuego y '
                                  'Patagonia',
                                  'Alaska, Canadá y Centroamérica'],
                 'correcta': 'D'},
                {'pregunta': 'La teoría que sostiene que se utilizó la Isla '
                             'de Pascua para llegar a Sudamérica corresponde '
                             'a la teoría: (UNSAAC 2011)',
                 'alternativas': ['Autoctonista',
                                  'Asiática',
                                  'Melanésica',
                                  'Polinésica',
                                  'Australiana'],
                 'correcta': 'D'},
                {'pregunta': 'El descubridor del Protohomo Pampeanus fue: '
                             '(UNSAAC 2013)',
                 'alternativas': ['Thor Heyerdahl',
                                  'José Imbelloni',
                                  'Florentino Ameghino',
                                  'Alex Hrdlicka',
                                  'Paul Rivet'],
                 'correcta': 'C'},
                {'pregunta': 'La posible inmigración humana a Sudamérica, '
                             'por la corriente Sur-Ecuatorial, es de '
                             'procedencia: (UNSAAC 2013)',
                 'alternativas': ['Polinésica',
                                  'Melanésica',
                                  'Australiana',
                                  'Asiática',
                                  'Oceánica'],
                 'correcta': 'B'},
                {'pregunta': 'Los restos fósiles hallados por Florentino '
                             'Ameghino para sustentar la teoría autoctonista '
                             'del poblamiento americano se encontraban en el '
                             'estrato subterráneo del: (UNSAAC 2013)',
                 'alternativas': ['Eoceno',
                                  'Pleistoceno',
                                  'Holoceno',
                                  'Plioceno',
                                  'Mioceno'],
                 'correcta': 'D'},
                {'pregunta': 'La hamaca, la cerbatana y la pachamanca son '
                             'elementos culturales demostrativos de la '
                             'presencia en América de los: (UNSAAC 2013)',
                 'alternativas': ['Australianos',
                                  'Siberianos',
                                  'Mongoles',
                                  'Oceánicos',
                                  'Asiáticos'],
                 'correcta': 'E'},
                {'pregunta': 'Según Florentino Ameghino, el origen del '
                             'hombre americano se inició en: (UNSAAC 2016)',
                 'alternativas': ['América del Sur',
                                  'América y Asia',
                                  'Europa y América',
                                  'América del Norte',
                                  'Asia y Europa'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría del Origen Asiático planteada por '
                             'Alex Hrdlicka está sustentada en pruebas: '
                             '(UNSAAC 2016)',
                 'alternativas': ['Metalúrgicas y antroposomáticas',
                                  'Geográficas y metalúrgicas',
                                  'Minerológicas y cerámicas',
                                  'Climáticas y metalúrgicas',
                                  'Antroposomáticas y Geográficas'],
                 'correcta': 'E'},
                {'pregunta': 'La constitución de las chozas en forma de '
                             'colmena y el uso del boomerang se reconocen '
                             'como elementos probatorios de la presencia en '
                             'América de los: (UNSAAC 2016)',
                 'alternativas': ['Polinesios',
                                  'Asiáticos',
                                  'Melanesios',
                                  'Africanos',
                                  'Australianos'],
                 'correcta': 'C'},
                {'pregunta': 'La Teoría Autoctonista del Poblamiento de '
                             'América fue planteada por: (UNSAAC 2018)',
                 'alternativas': ['Paul Rivet',
                                  'Luis Guillermo Lumbreras',
                                  'Julio César Tello',
                                  'Antonio Méndez Correa',
                                  'Florentino Ameghino'],
                 'correcta': 'E'},
                {'pregunta': 'Sobre el Poblamiento de América, los elementos '
                             'culturales como la construcción de chozas en '
                             'forma de colmena, el boomerang y el churinga '
                             'corresponden a la Teoría sustentada por: '
                             '(UNSAAC 2018)',
                 'alternativas': ['Paul Rivet',
                                  'Alex Hrdlicka',
                                  'Florentino Ameghino',
                                  'Antonio Méndez Correa',
                                  'Julio César Tello'],
                 'correcta': 'D'},
                {'pregunta': 'La Teoría de Origen Asiático del Hombre '
                             'Americano fue planteada por: (UNSAAC 2018)',
                 'alternativas': ['Ruth Shady',
                                  'Max Uhle',
                                  'Alex Hrdlicka',
                                  'Paul Rivet',
                                  'Antonio Méndez Correa'],
                 'correcta': 'C'},
                {'pregunta': 'La teoría Inmigracionista de origen Oceánico, '
                             'Melanésica y Polinésica fue propuesta por: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Alex Hrdlicka',
                                  'Florentino Ameghino',
                                  'Antonio Méndez Correa',
                                  'Paul Rivet',
                                  'José Imbelloni'],
                 'correcta': 'D'},
                {'pregunta': 'La Teoría del Homo Pampeanus (Hombre de la '
                             'Pampa) es sustentada por el investigador: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Thomas Linch',
                                  'Méndez Correa',
                                  'Florentino Ameghino',
                                  'Paul Rivet',
                                  'Alex Hrdlicka'],
                 'correcta': 'C'},
                {'pregunta': 'El autor de la Teoría del Origen Polinésico '
                             'del hombre americano es: (UNSAAC Ordinario)',
                 'alternativas': ['Antonio Méndez',
                                  'Paul Rivet',
                                  'Joseph de Acosta',
                                  'Alex Hrdlicka',
                                  'Florentino Ameghino'],
                 'correcta': 'B'},
                {'pregunta': 'La Teoría de la Inmigración de grupos '
                             'paleomongoloides a través del estrecho de '
                             'Bering corresponde a: (UNSAAC Ordinario)',
                 'alternativas': ['Antonio Méndez Correa',
                                  'Alex Hrdlicka',
                                  'Paul Rivet',
                                  'Max Uhle',
                                  'Julio C. Tello'],
                 'correcta': 'B'},
                {'pregunta': 'En el proceso del poblamiento de América, los '
                             'polinesios llegaron por la: (UNSAAC Ordinario)',
                 'alternativas': ['Corriente nor ecuatorial',
                                  'Corriente de Kuro Shiwo',
                                  'Corriente sur ecuatorial',
                                  'Ruta de Bering',
                                  'Antártida'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de origen asiático sustentada por '
                             'Alex Hrdlicka está basada en pruebas de '
                             'carácter: (UNSAAC Ordinario)',
                 'alternativas': ['Paleontológico y arqueológico',
                                  'Lingüístico y Cultural',
                                  'Físico y cultural',
                                  'Antroposomático y cultural',
                                  'Antroposomático y geográfico'],
                 'correcta': 'E'},
                {'pregunta': 'El testimonio sobre el origen evolutivo del '
                             'hombre americano según Florentino Ameghino es: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['La semejanza física entre asiáticos y '
                                  'americanos',
                                  'La existencia de elementos óseos del '
                                  'Protohomo Pampeanus',
                                  'La presencia del grupo sanguíneo RHO+ '
                                  'australiano en las poblaciones de '
                                  'Patagonia',
                                  'La migración de pueblos asiáticos por el '
                                  'estrecho de Bering hacia las costas '
                                  'occidentales de Canadá',
                                  'La migración de melanesios de Nueva '
                                  'Guinea a Lagoa Santa en Brasil'],
                 'correcta': 'B'},
                {'pregunta': 'La Teoría Inmigracionista de Origen '
                             'Australiano sostiene: (UNSAAC Ordinario)',
                 'alternativas': ['La traslación de hombres primitivos de '
                                  'Melanesia hacia América Central',
                                  'La traslación de expertos navegantes de '
                                  'Polinesia a través de Isla de Pascua '
                                  'llegó a Sudamérica',
                                  'El paso de hombres primitivos del Asia '
                                  'por el estrecho de Bering',
                                  'La formación del Homo Pampeanus en la '
                                  'comarca de Chapalmalal',
                                  'El paso de hombres primitivos por '
                                  'Tasmania que llegaron a la Patagonia'],
                 'correcta': 'E'},
                {'pregunta': 'La oleada expansiva asiática a América se '
                             'produjo en la glaciación de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Illinois',
                                  'Mindel',
                                  'Kansas',
                                  'Nebraska',
                                  'Wisconsin'],
                 'correcta': 'E'},
                {'pregunta': 'En el poblamiento americano, llegaron a la '
                             'Tierra del Fuego y la Patagonia Argentina, '
                             'los: (UNSAAC Ordinario)',
                 'alternativas': ['Melanesios',
                                  'Asiáticos',
                                  'Oceánicos',
                                  'Australianos',
                                  'Polinesios'],
                 'correcta': 'D'},
                {'pregunta': 'De acuerdo a la Teoría del Poblamiento '
                             'Americano, los navegantes que llegaron al '
                             'extremo sur de Sudamérica, pasando por la isla '
                             'de Pascua, fueron los: (UNSAAC Ordinario)',
                 'alternativas': ['Asiáticos',
                                  'Melanesios',
                                  'La Antártida',
                                  'Australianos',
                                  'Polinesios'],
                 'correcta': 'E'},
                {'pregunta': 'En el Poblamiento de América, la Teoría '
                             'Poligenista fue sustentada por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Antonio Méndez Correa',
                                  'Pablo Macera',
                                  'Alex Hrdlicka',
                                  'Florentino Ameghino',
                                  'Paul Rivet'],
                 'correcta': 'E'},
                {'pregunta': 'El poblamiento de américa se dio en la era: (I '
                             'CEPRU 2010)',
                 'alternativas': ['Superior',
                                  'Terciaria',
                                  'Cuaternaria',
                                  'Primario',
                                  'Secundaria'],
                 'correcta': 'C'},
                {'pregunta': 'La Teoría inmigracionista sobre el poblamiento '
                             'americano, basada en la posición poliracial, '
                             'es sustentada por: (I CEPRU 2011)',
                 'alternativas': ['Florentino Ameghino',
                                  'Alex Hrdlicka',
                                  'Federico Max Uhle',
                                  'Antonio Mendez Correa',
                                  'Paul Rivet'],
                 'correcta': 'E'},
                {'pregunta': 'La Teoría inmigracionista de origen asiático '
                             'sobre el poblamiento de américa, fue '
                             'sustentada por: (I CEPRU 2011)',
                 'alternativas': ['Florentino Ameghino',
                                  'Paul Rivet',
                                  'Luis Guillermo Lumbreras',
                                  'Antonio Mendez Correa',
                                  'Alex Hrdlicka'],
                 'correcta': 'E'},
                {'pregunta': 'Según Florentino Ameghino, el hombre americano '
                             'se habría dispersado desde la comarca de '
                             'Chapalmalal por el resto del mundo a través: '
                             '(II CEPRU 2012)',
                 'alternativas': ['De las corrientes nor ecuatoriales',
                                  'De puentes intercontinentales',
                                  'Del estrecho de Bering',
                                  'De la Tierra del Fuego',
                                  'Del cabo de hornos'],
                 'correcta': 'C'},
                {'pregunta': 'Los pobladores de Lagoa Santa «Brasil» poseen '
                             'cráneos muy semejantes a los negros de nueva '
                             'Guinea; esta afirmación es recogida en la '
                             'teoría: (II CEPRU 2012)',
                 'alternativas': ['Australiana',
                                  'Melanésica',
                                  'Autoctonista',
                                  'Polinésica',
                                  'Asiática'],
                 'correcta': 'B'},
                {'pregunta': 'La Teoría de Origen Asiático sobre el '
                             'poblamiento americano, sostiene los: (II CEPRU '
                             '2013)',
                 'alternativas': ['Pobladores de Lagoa Santa y de Nueva '
                                  'Guinea tienen semejanzas físicas',
                                  'Protohomo Pampeanus emigraron de américa '
                                  'a Europa',
                                  'Grupos humanos paleomongoloides '
                                  'inmigraron a américa por el estrecho de '
                                  'Bering',
                                  'Asiáticos llegaron a la Tierra del Fuego '
                                  'y a la Patagonia',
                                  'Polinesios llegaron al extremo sur de '
                                  'América'],
                 'correcta': 'C'},
                {'pregunta': 'El origen del hombre se originó en las pampas '
                             'argentinas, es una teoría sostenida por: (I '
                             'CEPRU 2014)',
                 'alternativas': ['Paul Rivet',
                                  'Max Uhle',
                                  'Antonio Méndez Correa',
                                  'Alex Hrdlicka',
                                  'Florentino Ameghino'],
                 'correcta': 'E'},
                {'pregunta': 'Según Antonio Méndez Correa el hombre proviene '
                             'de: (I CEPRU 2014)',
                 'alternativas': ['Melanesia',
                                  'Asia',
                                  'Oceanía',
                                  'Australia',
                                  'Polinesia'],
                 'correcta': 'D'},
                {'pregunta': 'La teoría autoctonista sobre el origen del '
                             'hombre americano fue planteada por:',
                 'alternativas': ['Julio C. Tello',
                                  'Antonio Méndez Correa',
                                  'Florentino Ameghino',
                                  'Alex Hrdlicka',
                                  'Paul Rivet'],
                 'correcta': 'C'},
                {'pregunta': 'Ameghino sostenía que el hombre americano se '
                             'originó en las Pampas Argentinas, basándose en '
                             'fósiles que llamó:',
                 'alternativas': ['Pampanthropus',
                                  'Protohomo Pampeanus',
                                  'Homo Argentinus',
                                  'Ameghinantropus',
                                  'Homo Pampeanus Sapiens'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría autoctonista de Ameghino fue '
                             'rebatida en 1908 por:',
                 'alternativas': ['Max Uhle',
                                  'Alex Hrdlicka',
                                  'Julio C. Tello',
                                  'Paul Rivet',
                                  'Méndez Correa'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría del origen asiático del hombre '
                             'americano, sustentada en 1917, plantea el '
                             'ingreso por el:',
                 'alternativas': ['Océano Atlántico',
                                  'Canal de Panamá',
                                  'Estrecho de Behring',
                                  'Océano Pacífico',
                                  'Estrecho de Magallanes'],
                 'correcta': 'C'},
                {'pregunta': 'El antropólogo que sustentó la teoría del '
                             'origen asiático (monogenista) fue:',
                 'alternativas': ['Paul Rivet',
                                  'Max Uhle',
                                  'Florentino Ameghino',
                                  'Méndez Correa',
                                  'Alex Hrdlicka'],
                 'correcta': 'E'},
                {'pregunta': 'La teoría del origen oceánico, poligenista, '
                             'con procedencia melanésica y polinésica, fue '
                             'sustentada por:',
                 'alternativas': ['Paul Rivet',
                                  'Julio C. Tello',
                                  'Florentino Ameghino',
                                  'Alex Hrdlicka',
                                  'Méndez Correa'],
                 'correcta': 'A'},
                {'pregunta': 'La procedencia polinésica de la teoría '
                             'oceánica se sustenta en semejanzas '
                             'lingüísticas con el:',
                 'alternativas': ['Quechua',
                                  'Cauqui',
                                  'Aimara',
                                  'Puquina',
                                  'Mochica'],
                 'correcta': 'A'},
                {'pregunta': 'La teoría del origen australiano del hombre '
                             'americano fue sostenida por:',
                 'alternativas': ['Florentino Ameghino',
                                  'Alex Hrdlicka',
                                  'Paul Rivet',
                                  'Antonio Méndez Correa',
                                  'Max Uhle'],
                 'correcta': 'D'},
                {'pregunta': 'El sitio arqueológico de Paccaicasa, en '
                             'Ayacucho, que da inicio a la gran cultura '
                             'andina, fue estudiado por:',
                 'alternativas': ['Rafael Larco Hoyle',
                                  'Augusto Cardich',
                                  'Richard Mac Neish',
                                  'Edward Lanning',
                                  'Julio C. Tello'],
                 'correcta': 'C'},
                {'pregunta': 'El sitio de Chivateros, considerado el '
                             'poblador más antiguo de la costa peruana, se '
                             'ubica en el río:',
                 'alternativas': ['Chillón',
                                  'Rímac',
                                  'Zaña',
                                  'Chicama',
                                  'Ica'],
                 'correcta': 'A'},
                {'pregunta': 'El sitio de Toquepala, en Tacna, es célebre '
                             'por presentar el más antiguo:',
                 'alternativas': ['Complejo textil',
                                  'Arte rupestre',
                                  'Cementerio',
                                  'Sistema de riego',
                                  'Templo religioso'],
                 'correcta': 'B'},
                {'pregunta': 'En el sitio de Lauricocha, estudiado por '
                             'Augusto Cardich, se hallaron los primeros:',
                 'alternativas': ['Textiles del Perú',
                                  'Sistemas de irrigación',
                                  'Instrumentos musicales',
                                  'Objetos de cerámica',
                                  'Restos óseos humanos del Perú'],
                 'correcta': 'E'},
                {'pregunta': 'El sitio de Paiján, en La Libertad, fue '
                             'estudiado por:',
                 'alternativas': ['Frederic Engel',
                                  'Thomas Lynch',
                                  'Rafael Larco Hoyle',
                                  'Tom Dillehay',
                                  'Julio C. Tello'],
                 'correcta': 'C'},
                {'pregunta': 'El sitio de Nanchoc, en Cajamarca, es '
                             'considerado el primer:',
                 'alternativas': ['Textilero del Perú',
                                  'Horticultor del Perú',
                                  'Ganadero del Perú',
                                  'Alfarero del Perú',
                                  'Pescador del Perú'],
                 'correcta': 'B'},
                {'pregunta': 'El sitio de Guitarrero, en Áncash, estudiado '
                             'por Thomas Lynch, es considerado precursor de '
                             'la:',
                 'alternativas': ['Agricultura en el Perú',
                                  'Pesca en el Perú',
                                  'Arquitectura en el Perú',
                                  'Cerámica en el Perú',
                                  'Metalurgia en el Perú'],
                 'correcta': 'A'},
                {'pregunta': 'En el sitio de Santo Domingo, en Paracas, se '
                             'encontró evidencia del primer:',
                 'alternativas': ['Pescador con red y músico del Perú',
                                  'Alfarero del Perú',
                                  'Orfebre del Perú',
                                  'Textilero del Perú',
                                  'Escultor del Perú'],
                 'correcta': 'A'},
                {'pregunta': 'En el sitio de Chilca, al sur de Lima, se '
                             'evidencia la domesticación de:',
                 'alternativas': ['El pato',
                                  'El perro',
                                  'El cuy',
                                  'La llama',
                                  'La alpaca'],
                 'correcta': 'B'},
                {'pregunta': 'El sitio de Piquimachay, en Ayacucho, '
                             'evidencia la primera domesticación de:',
                 'alternativas': ['Las abejas',
                                  'Los peces',
                                  'El perro',
                                  'Las aves de corral',
                                  'La llama, alpaca y cuy'],
                 'correcta': 'E'},
                {'pregunta': 'En el sitio de Telarmachay, en Junín, se '
                             'evidencia el paso de cazadores a:',
                 'alternativas': ['Pescadores',
                                  'Agricultores',
                                  'Artesanos',
                                  'Comerciantes',
                                  'Pastores'],
                 'correcta': 'E'},
                {'pregunta': 'El sitio de Lurín, al sur de Lima, estudiado '
                             'por Josefina Ramos de Cox, es considerado como '
                             'el del primer:',
                 'alternativas': ['Textilero del Perú',
                                  'Arquitecto del Perú',
                                  'Alfarero del Perú',
                                  'Escultor del Perú',
                                  'Metalúrgico del Perú'],
                 'correcta': 'B'},
                {'pregunta': 'El sitio de Huaca Prieta, en Chicama, '
                             'estudiado por Junius Bird, destaca por ser '
                             'sede de los primeros maestros del:',
                 'alternativas': ['Arte textil',
                                  'Arte arquitectónico',
                                  'Arte lítico',
                                  'Arte metalúrgico',
                                  'Arte cerámico'],
                 'correcta': 'A'},
                {'pregunta': 'El sitio de Kotosh, en Huánuco, es considerado '
                             'el primer monumento religioso de:',
                 'alternativas': ['Sudamérica exclusivamente',
                                  'América',
                                  'El Perú',
                                  'Los Andes centrales exclusivamente',
                                  'La costa peruana exclusivamente'],
                 'correcta': 'B'},
                {'pregunta': 'En Kotosh se construyó un famoso recinto con '
                             'dos manos esculpidas en arcilla, llamado:',
                 'alternativas': ['Templo del Jaguar',
                                  'Templo de las Manos Cruzadas',
                                  'Templo de la Luna',
                                  'Templo de las Serpientes',
                                  'Templo del Sol'],
                 'correcta': 'B'},
                {'pregunta': 'El sitio de Las Haldas, en Casma, estudiado '
                             'por Rosa Fung Pineda, representa el inicio de '
                             'la primera etapa:',
                 'alternativas': ['Ganadera',
                                  'Alfarera',
                                  'Metalúrgica',
                                  'Agrícola',
                                  'Textil'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'EL POBLAMIENTO DE AMÉRICA / TEORÍA '
                                'AUTOCTONISTA',
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
                                'por diversas teorías.',
                                'La teoría autoctonista fue planteada por el '
                                'argentino Florentino Ameghino en 1879.',
                                'Sostenía que el hombre americano se originó '
                                'en las Pampas Argentinas, en Chapalmalal, '
                                'dispersándose por «puentes '
                                'intercontinentales».',
                                'Ameghino basó su teoría en fósiles que '
                                'llamó «Protohomo Pampeanus» (Hombre de la '
                                'Pampa).',
                                'Fue rebatida en 1908 por Alex Hrdlicka, '
                                'quien demostró que los fósiles eran de '
                                'animales de la era Cuaternaria, no '
                                'Terciaria.']},
                     {'titulo': 'TEORÍA DEL ORIGEN ASIÁTICO / TEORÍA DEL '
                                'ORIGEN OCEÁNICO',
                      'items': ['La teoría del origen asiático, monogenista, '
                                'fue sustentada en 1917 por Alex Hrdlicka.',
                                'Sostuvo que grupos paleomongoloides '
                                'inmigraron a América por el Estrecho de '
                                'Behring.',
                                'Su prueba geográfica es la glaciación de '
                                'Wisconsin y el corredor natural del '
                                'Estrecho de Behring.',
                                'Sus pruebas antroposomáticas incluyen el '
                                'cabello grueso y negro, los ojos rasgados, '
                                'y la mancha mongólica en el coxis.',
                                'La teoría del origen oceánico, poligenista, '
                                'fue sustentada por el francés Paul Rivet en '
                                '1943.',
                                'La procedencia melanésica cruzó el Pacífico '
                                'por las corrientes nor ecuatoriales; sus '
                                'pruebas incluyen semejanzas con cráneos de '
                                'Lagoa Santa (Brasil).',
                                'La procedencia polinésica pasó por la Isla '
                                'de Pascua, impulsada por la corriente Sur '
                                'Ecuatorial.',
                                'Entre las pruebas polinésicas están '
                                'semejanzas lingüísticas con el quechua y el '
                                'uso compartido de la pachamanca.']},
                     {'titulo': 'TEORÍA DEL ORIGEN AUSTRALIANO / NÓMADAS: '
                                'PACCAICASA Y CHIVATEROS',
                      'items': ['La teoría del origen australiano fue '
                                'sostenida por el portugués Antonio Méndez '
                                'Correa en 1925.',
                                'Los australianos habrían viajado en balsas '
                                'por Tasmania y la Antártida hasta llegar a '
                                'Tierra del Fuego y la Patagonia.',
                                'Sus pruebas incluyen semejanza craneal '
                                'dolicocéfalo, tipo sanguíneo O+, y palabras '
                                'similares entre fueguinos y australianos.',
                                'Entre sus elementos culturales compartidos '
                                'están el boomerang y el churinga o zumbador '
                                'ritual.',
                                'Paccaicasa, en Ayacucho, estudiado por '
                                'Richard Mac Neish, data de 20 000 años '
                                'a.C.; da inicio a la gran cultura andina.',
                                'Chivateros, en el río Chillón (Lima), '
                                'estudiado por Edward Lanning y Patterson, '
                                'data de 10 000 años a.C.',
                                'Chivateros representa al poblador más '
                                'antiguo de la costa peruana, con el taller '
                                'lítico más grande del Perú antiguo.']},
                     {'titulo': 'NÓMADAS: TOQUEPALA Y LAURICOCHA / NÓMADAS: '
                                'PAIJÁN',
                      'items': ['Toquepala, en Tacna, estudiado por Miomir '
                                'Bojovich y Emilio González, data de 9525 '
                                'años a.C.',
                                'Toquepala presenta el arte rupestre más '
                                'antiguo del Perú, con pinturas de caza de '
                                'vicuñas y guanacos.',
                                'Lauricocha, en Huánuco, estudiado por '
                                'Augusto Cardich, data de 9500 años a.C.',
                                'En Lauricocha se hallaron los primeros '
                                'restos óseos humanos del Perú: 11 '
                                'esqueletos, de cráneo dolicocéfalo.',
                                'Paiján, en La Libertad, estudiado por '
                                'Rafael Larco Hoyle, data de 8000 años a.C.',
                                'En Paiján se encontraron esqueletos '
                                'completos: una mujer de 25 años y un niño '
                                'de 12.',
                                'Los pobladores de Paiján fueron pescadores '
                                'y rendían culto a sus muertos.']},
                     {'titulo': 'SEMINÓMADAS: NANCHOC Y GUITARRERO / '
                                'SEMINÓMADAS: SANTO DOMINGO Y CHILCA',
                      'items': ['Nanchoc, en Cajamarca, estudiado por Tom '
                                'Dillehay, data de 8000-7000 años a.C.; '
                                'primer horticultor del Perú, de calabaza y '
                                'algodón.',
                                'Guitarrero, en Áncash, estudiado por Thomas '
                                'Lynch, es el segundo horticultor del Perú, '
                                'de leguminosas y frijoles.',
                                'Los pobladores de Guitarrero son '
                                'considerados precursores de la agricultura '
                                'en el Perú; sepultaban a sus muertos.',
                                'Santo Domingo, en Paracas (Ica), estudiado '
                                'por Frederic Engel, data de 6000 años a.C.; '
                                'tercer horticultor del Perú.',
                                'En Santo Domingo se halló al primer '
                                'pescador con red y primer músico del Perú, '
                                'con las flautas más antiguas.',
                                'Chilca, al sur de Lima, estudiado por '
                                'Frederic Engel, data de 5500 años a.C.',
                                'En Chilca se domesticó al perro, y los '
                                'muertos eran atados con cuerdas y envueltos '
                                'en esteras.']},
                     {'titulo': 'SEMINÓMADAS: PIQUIMACHAY Y TELARMACHAY / '
                                'SEDENTARIOS: LURÍN Y HUACA PRIETA',
                      'items': ['Piquimachay, en Ayacucho, estudiado por '
                                'Richard Mac Neish, data de 3300 años a.C.',
                                'Piquimachay evidencia la primera '
                                'domesticación de la llama, alpaca y cuy.',
                                'Telarmachay, en Junín, estudiado por '
                                'Danielle Lavallée, data de 3000 años a.C.',
                                'En Telarmachay se evidencia el paso de '
                                'cazadores a pastores, y la primera '
                                'domesticación de la papa y oca.',
                                'Lurín, al sur de Lima, estudiado por '
                                'Josefina Ramos de Cox, data de 3000 años '
                                'a.C.; primer arquitecto del Perú.',
                                'Huaca Prieta, en Chicama (La Libertad), '
                                'estudiado por Junius Bird, data de 2500 '
                                'años a.C.',
                                'Los pobladores de Huaca Prieta fueron los '
                                'primeros maestros del arte textil, con la '
                                'figura del «primer cóndor andino».']},
                     {'titulo': 'SEDENTARIOS: KOTOSH / SEDENTARIOS: LAS '
                                'HALDAS Y CERRO PALOMA',
                      'items': ['Kotosh, en Huánuco, fue estudiado por Julio '
                                'C. Tello y Seichi Izumi; data de 2200 años '
                                'a.C.',
                                'Es considerado el primer monumento '
                                'religioso de América, pionero en construir '
                                'templos sobre templos más antiguos.',
                                'En Kotosh se construyó el Templo de las '
                                'Manos Cruzadas, recinto con dos manos '
                                'esculpidas en arcilla.',
                                'Fue una sociedad agrícola cultivadora de '
                                'algodón, que practicaba ritos a la tierra.',
                                'Las Haldas, en Casma (Áncash), estudiado '
                                'por Rosa Fung Pineda, data de 1600 años '
                                'a.C.; inicio de la primera etapa alfarera.',
                                'Cerro Paloma, en Lima, estudiado por '
                                'Frederic Engel, data de 1500 años a.C.',
                                'En Cerro Paloma se hallaron las primeras '
                                'redes de pescar hechas de algodón, junto '
                                'con anzuelos y cordeles.']}],
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
  'secciones': [{'titulo': '6.1 CIVILIZACIÓN CARAL: UBICACIÓN Y '
                           'DESCUBRIMIENTO',
                 'items': ['{Caral} se ubica en la región Lima, provincia de '
                           'Barranca, distrito de Supe, en el valle medio '
                           'del río {Supe}.',
                           'La antigüedad de Caral es de {2800} a.C., '
                           'posterior a Egipto (2900 a.C.) y Mesopotamia '
                           '(3000 a.C.).',
                           'Fue declarada Patrimonio Cultural de la '
                           'Humanidad por la {UNESCO} en Sevilla, el 28 de '
                           'junio de 2009.',
                           'La arqueóloga {Ruth Shady Solís} inició en 1994 '
                           'el reconocimiento detallado de la zona, y en '
                           '1996 descubrió la ciudadela sagrada.',
                           'El Complejo Arqueológico del valle de Supe está '
                           'dividido en cuatro zonas: Lurihuasi, {Miraya}, '
                           'Chupacigarro y Caral.']},
                {'titulo': '6.2 CIVILIZACIÓN CARAL: SOCIEDAD Y '
                           'CARACTERÍSTICAS',
                 'items': ['Caral es considerada la civilización más antigua '
                           'del {Perú} y de América.',
                           'Tuvo un gobierno de carácter {teocrático}, no '
                           'militarizado, dirigido por sacerdotes '
                           'astrónomos.',
                           'Su economía se basó en una agricultura variada: '
                           'calabaza, algodón, camote, frijol, {maíz} y ají.',
                           'Practicaron la pesca de moluscos, {anchovetas} y '
                           'sardinas, e intercambiaron productos de costa, '
                           'sierra y selva.',
                           'Se halló en Caral el {quipu} más antiguo '
                           'conocido, y hasta 84 flautas de hueso decoradas '
                           'con figuras de aves.']},
                {'titulo': '6.3 CIVILIZACIÓN CARAL: ARQUITECTURA',
                 'items': ['Caral está conformada por 32 conjuntos '
                           'arquitectónicos: pirámides, templos, sectores '
                           'residenciales, {anfiteatro}, almacenes y '
                           'altares.',
                           'Entre sus construcciones destacan el {Templo '
                           'Anfiteatro}, el Templo Mayor, la Pirámide de la '
                           'Cantera y el Altar del Fuego Sagrado.',
                           'Predominan construcciones ceremoniales '
                           '{piramidales}, con plataformas superpuestas y '
                           'plazas circulares hundidas.']},
                {'titulo': '6.4 CHAVÍN: UBICACIÓN Y SOCIEDAD (Horizonte '
                           'Temprano)',
                 'items': ['{Chavín} se ubica en el distrito de Huántar, '
                           'provincia de Huari, región Áncash, a orillas de '
                           'los ríos Mosna y Huachecsa.',
                           'Chavín es considerada una cultura {panperuana} '
                           'por su amplia influencia en sierra, costa y ceja '
                           'de selva.',
                           'Fue descubierta por {Julio C. Tello} en 1919.',
                           'Su gobierno fue {teocrático}, ejercido por '
                           'sacerdotes astrónomos que controlaban tierras y '
                           'producción.',
                           'La sociedad se dividía en sacerdotes astrónomos, '
                           '{artesanos} (escultores, ceramistas, orfebres) y '
                           'el pueblo (agricultores, pastores, '
                           'pescadores).']},
                {'titulo': '6.5 CHAVÍN: ARQUITECTURA Y ESCULTURA',
                 'items': ['El templo principal, de forma piramidal trunca '
                           'con patios en forma de {U}, se ubica en Chavín '
                           'de Huántar.',
                           'El {Lanzón Monolítico} y las cabezas clavas son '
                           'monolitos que representan guardianes del templo.',
                           'La {Estela de Raimondi}, descubierta por Timoteo '
                           'Espinoza, representa al dios Viracocha en forma '
                           'de jaguar.',
                           'El {Obelisco de Tello} tiene grabados de '
                           'serpiente, caimán, ají y yuca.',
                           'Chavín rindió culto a tres deidades zoomorfas: '
                           'el {jaguar}, el cóndor y la serpiente.']},
                {'titulo': '6.6 PARACAS: UBICACIÓN Y ETAPAS (Horizonte '
                           'Temprano)',
                 'items': ['{Paracas} se ubica en el departamento de Ica, '
                           'provincia de Pisco, entre Cañete y Yauca.',
                           'Fue descubierta por {Julio C. Tello} en 1925, y '
                           'estudiada también por Toribio Mejía Xesspe.',
                           'La etapa {Paracas Cavernas} tuvo su capital en '
                           'Tajahuana, con tumbas subterráneas en forma de '
                           'copa invertida.',
                           'La etapa {Paracas Necrópolis} tuvo su capital en '
                           'Topara, con tumbas subterráneas cuadrangulares y '
                           'mejor calidad textil.']},
                {'titulo': '6.7 PARACAS: MOMIFICACIÓN, TREPANACIONES Y '
                           'TEJIDOS',
                 'items': ['Los paracas practicaron la {momificación}, con '
                           'alto conocimiento de anatomía y fisiología.',
                           'Practicaron {trepanaciones craneanas}, usando '
                           'coca como anestésico e instrumentos como el '
                           'cincel tumi.',
                           'Según Tello, un {40}% de los cráneos de las '
                           'momias muestran señales de trepanación en vida.',
                           'El {tejido} paracas destaca por su finura y '
                           'policromía; sobresalen los mantos ceremoniales '
                           'con diseños geométricos y zoomorfos.']},
                {'titulo': '6.8 NASCA: UBICACIÓN Y SOCIEDAD (Intermedio '
                           'Temprano)',
                 'items': ['{Nasca} tuvo su centro en el valle de Río '
                           'Grande, provincia de Nasca, departamento de Ica; '
                           'es cultura {regional}.',
                           'Fue descubierta por {Federico Max Uhle} en 1901.',
                           'Su Estado fue de carácter '
                           '{teocrático-militarista}, gobernado por '
                           'sacerdotes-militares.',
                           'Desarrollaron los {puquios}, tecnología de '
                           'canales de riego subterráneo para aprovechar '
                           'aguas del subsuelo.']},
                {'titulo': '6.9 NASCA: CERÁMICA Y LÍNEAS DE NASCA',
                 'items': ['La cerámica nasca es {pictórica} (con temor al '
                           'vacío), {policroma} (8 colores), realista y '
                           'fantástica.',
                           'Su capital fue {Cahuachi}; otras ciudades fueron '
                           'Estaquería, Tambo Viejo y Ocucaje.',
                           'Las {Líneas de Nasca} fueron descubiertas en '
                           '1927 por {Toribio Mejía Xesspe}, y estudiadas '
                           'por María Reiche.',
                           'María Reiche concluyó que las líneas constituían '
                           'un gigantesco {calendario astronómico} '
                           'agrícola.']},
                {'titulo': '6.10 MOCHICA: UBICACIÓN Y SOCIEDAD (Intermedio '
                           'Temprano)',
                 'items': ['{Mochica} se desarrolló en los valles de Moche, '
                           'Chicama y Virú, en La Libertad; su capital fue '
                           '{Moche}.',
                           'Fue descubierta por {Federico Max Uhle} en 1902; '
                           'es cultura regional.',
                           'La aristocracia militar estaba representada por '
                           'el {Cie Quich}, rey o máxima autoridad.',
                           'La casta sacerdotal rendía culto a la divinidad '
                           '{Aiapaec}, y también ejercía la medicina.']},
                {'titulo': '6.11 MOCHICA: CERÁMICA Y ARQUITECTURA',
                 'items': ['La cerámica mochica alcanzó el nivel más alto '
                           'del Perú Antiguo, destacando los {huacos '
                           'retratos}, que expresan estados psicológicos.',
                           'Es de forma globular con asa {estribo} y un solo '
                           'pico; predominó la bicromía rojo ocre y blanco '
                           'crema.',
                           'La {Huaca del Sol} estaba dedicada al culto de '
                           'Aiapaec; la {Huaca de la Luna}, a la diosa Shi.',
                           'La {Huaca Rajada} del Señor de Sipán fue '
                           'descubierta por {Walter Alva} en 1987, en '
                           'Chiclayo.']},
                {'titulo': '6.12 TIAHUANACO: UBICACIÓN Y SOCIEDAD (Horizonte '
                           'Medio)',
                 'items': ['{Tiahuanaco} se ubica a 21 km al sureste del '
                           'lago Titicaca (Bolivia); es cultura '
                           '{panperuana}.',
                           'Fue descubierta por el cronista {Pedro Cieza de '
                           'León} en 1551.',
                           'Tuvo un sistema {teocrático} de carácter '
                           'pacífico, sin recurrir a acciones bélicas.',
                           'Su dios principal fue {Wiracocha}, creador del '
                           'mundo andino, representado con caracteres '
                           'antropomorfos y felínicos.']},
                {'titulo': '6.13 TIAHUANACO: TECNOLOGÍA Y ARTE',
                 'items': ['Construyeron {camellones} o waru waru, suelos '
                           'elevados alrededor de lagos, y elaboraron chuño '
                           'y moraya.',
                           'En arquitectura usaron grandes bloques de piedra '
                           'con {grapas de cobre}; destacan Kalasasaya, '
                           'Akapana y Pumapunku.',
                           'La {Portada del Sol}, en Kalasasaya, está '
                           'tallada en una sola piedra con la imagen de '
                           'Wiracocha.',
                           'Su cerámica es policroma; destaca el {kero} '
                           '(vaso ceremonial) y el pebetero.']},
                {'titulo': '6.14 WARI: UBICACIÓN Y ORIGEN (Horizonte Medio)',
                 'items': ['{Wari} se ubica a 12 km al noroeste de Ayacucho; '
                           'es cultura {panperuana}, con capital en la '
                           'ciudad de Wari o Viñaque.',
                           'Fue descubierta por {Luis Guillermo Lumbreras}.',
                           'Los antecesores de los Waris fueron los '
                           '{Huarpas}, de Chaquipampa, entre Ayacucho y '
                           'Huanta.',
                           'Según Pablo Macera, los Waris son producto de 4 '
                           'pueblos: Huarpa, Nasca, {Tiahuanaco} y '
                           'Pachacamac.']},
                {'titulo': '6.15 WARI: ORGANIZACIÓN Y EXPANSIÓN',
                 'items': ['Constituyeron un gran Estado '
                           '{militarista-teocrático} de tipo imperial, '
                           'dirigido por una élite militar.',
                           'Construyeron una importante red de {caminos} '
                           'para comunicar a los pueblos sometidos.',
                           'Fundaron ciudades capitales de región como '
                           '{Pikillacta} (Cusco), Cajamarquilla (Lima) y '
                           'Cerro Baúl (Moquegua).',
                           'Su caída se debió a contradicciones internas: '
                           'rebelión de ciudades, división de clases '
                           'dirigentes y falta de {producción}.']},
                {'titulo': '6.16 CHIMÚ: UBICACIÓN Y ARQUITECTURA (Intermedio '
                           'Tardío)',
                 'items': ['{Chimú} se originó en el valle de Chimor, La '
                           'Libertad; su capital fue {Chan Chan}, la ciudad '
                           'de barro más grande.',
                           'Es cultura {regional}, descubierta por Federico '
                           'Max Uhle en 1902.',
                           'Otras ciudades chimú fueron Pacatnamú y las '
                           'fortalezas de {Paramonga} y Pativilca.',
                           'Su cerámica es {monocroma}, de color negro '
                           'lustroso, producida en serie mediante moldes.']},
                {'titulo': '6.17 CHIMÚ: METALURGIA Y CONQUISTA INCA',
                 'items': ['Los chimú fueron los más grandes {joyeros} del '
                           'Perú antiguo, dominando el martillado, soldadura '
                           'y fundición.',
                           'Fabricaron el {Tumi}, cuchillo ceremonial, y '
                           'vasos con incrustaciones de piedras preciosas.',
                           'El último gobernante chimú, {Minchancamán}, fue '
                           'derrotado por Túpac Inca Yupanqui.',
                           'Los chimú quedaron incorporados al Estado Inca '
                           'como principal población del {Chinchaysuyo}.']},
                {'titulo': '6.18 CHANCA: UBICACIÓN Y SOCIEDAD (Intermedio '
                           'Tardío)',
                 'items': ['{Chanca} se desarrolló en Huancavelica, '
                           'Ayacucho, Apurímac (río Pampas) y parte del '
                           'Cusco.',
                           'Sus fundadores míticos fueron {Uscovilca} y '
                           'Ancovilca.',
                           'El reino chanca surgió tras la caída del imperio '
                           '{Wari}, formando un Estado militarista.',
                           'Su arquitectura destaca en {Sondor}, Curamba y '
                           'el Inti Huatana de Uranmarca, en Andahuaylas.',
                           'Chancas e incas lucharon por la supremacía '
                           'andina, hecho recordado en el mito de los '
                           '{Pururaucas}.']}],
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
                 'alternativas': ['Tiahuanaco',
                                  'Paracas',
                                  'Caral',
                                  'Mochica',
                                  'Chavín'],
                 'correcta': 'C'},
                {'pregunta': 'Caral fue investigada principalmente por:',
                 'alternativas': ['María Reiche',
                                  'Max Uhle',
                                  'Julio C. Tello',
                                  'Rafael Larco',
                                  'Ruth Shady'],
                 'correcta': 'E'},
                {'pregunta': 'Chavín de Huántar se ubica en el departamento '
                             'de:',
                 'alternativas': ['Áncash',
                                  'Ica',
                                  'La Libertad',
                                  'Huánuco',
                                  'Ayacucho'],
                 'correcta': 'A'},
                {'pregunta': 'Julio C. Tello denominó a Chavín como la '
                             'cultura:',
                 'alternativas': ['Síntesis',
                                  'Local',
                                  'Imperial',
                                  'Fusionante',
                                  'Matriz de la civilización andina'],
                 'correcta': 'E'},
                {'pregunta': 'La organización política de Chavín fue:',
                 'alternativas': ['Militarista',
                                  'Federal',
                                  'Democrática',
                                  'Republicana',
                                  'Teocrática'],
                 'correcta': 'E'},
                {'pregunta': 'Las cabezas clavas eran consideradas:',
                 'alternativas': ['Sellos de propiedad',
                                  'Instrumentos musicales',
                                  'Ofrendas funerarias',
                                  'Marcadores astronómicos',
                                  'Guardianes del templo'],
                 'correcta': 'E'},
                {'pregunta': 'La cerámica de Paracas Cavernas es:',
                 'alternativas': ['Escultórica realista',
                                  'Monocroma en pre-cocción',
                                  'Vidriada',
                                  'Bicroma',
                                  'Polícroma en post-cocción'],
                 'correcta': 'E'},
                {'pregunta': 'La capital de Paracas Necrópolis fue:',
                 'alternativas': ['Cahuachi',
                                  'Sechín',
                                  'Pachacamac',
                                  'Topará',
                                  'Tajahuana'],
                 'correcta': 'D'},
                {'pregunta': 'Paracas destacó notablemente por sus:',
                 'alternativas': ['Ciudades de barro',
                                  'Acueductos subterráneos',
                                  'Portadas monolíticas',
                                  'Quipus',
                                  'Trepanaciones craneanas y mantos '
                                  'bordados'],
                 'correcta': 'E'},
                {'pregunta': 'Las líneas de Nasca fueron estudiadas durante '
                             'décadas por:',
                 'alternativas': ['Max Uhle',
                                  'María Reiche',
                                  'Rafael Larco',
                                  'Julio C. Tello',
                                  'Ruth Shady'],
                 'correcta': 'B'},
                {'pregunta': 'Los acueductos de Cantalloc pertenecen a la '
                             'cultura:',
                 'alternativas': ['Mochica',
                                  'Paracas',
                                  'Nasca',
                                  'Chimú',
                                  'Wari'],
                 'correcta': 'C'},
                {'pregunta': 'La cerámica retrato o realista es '
                             'característica de:',
                 'alternativas': ['Mochica',
                                  'Chimú',
                                  'Chavín',
                                  'Tiahuanaco',
                                  'Nasca'],
                 'correcta': 'A'},
                {'pregunta': 'El Señor de Sipán pertenece a la cultura:',
                 'alternativas': ['Nasca',
                                  'Mochica',
                                  'Wari',
                                  'Lambayeque',
                                  'Chimú'],
                 'correcta': 'B'},
                {'pregunta': 'La Portada del Sol corresponde a la cultura:',
                 'alternativas': ['Nasca',
                                  'Tiahuanaco',
                                  'Chimú',
                                  'Chavín',
                                  'Wari'],
                 'correcta': 'B'},
                {'pregunta': 'El primer imperio andino, con capital en '
                             'Ayacucho, fue:',
                 'alternativas': ['Inca',
                                  'Chimú',
                                  'Chavín',
                                  'Tiahuanaco',
                                  'Wari'],
                 'correcta': 'E'},
                {'pregunta': 'Chan Chan, la ciudad de barro más grande de '
                             'América, perteneció a:',
                 'alternativas': ['Mochica',
                                  'Lambayeque',
                                  'Wari',
                                  'Chimú',
                                  'Nasca'],
                 'correcta': 'D'},
                {'pregunta': 'Los chancas se desarrollaron principalmente '
                             'en:',
                 'alternativas': ['Costa norte',
                                  'Costa sur',
                                  'Apurímac y Ayacucho',
                                  'Valle de Supe',
                                  'Altiplano del Titicaca'],
                 'correcta': 'C'},
                {'pregunta': 'Tiahuanaco se desarrolló en el altiplano del '
                             'lago:',
                 'alternativas': ['Junín',
                                  'Titicaca',
                                  'Parinacochas',
                                  'Poopó',
                                  'Chinchaycocha'],
                 'correcta': 'B'},
                {'pregunta': 'Paracas se ubicó en la provincia de Pisco, '
                             'departamento de:',
                 'alternativas': ['Arequipa',
                                  'Moquegua',
                                  'Lima',
                                  'Ica',
                                  'Tacna'],
                 'correcta': 'D'},
                {'pregunta': 'El Lanzón monolítico y la estela Raimondi '
                             'pertenecen a:',
                 'alternativas': ['Wari',
                                  'Paracas',
                                  'Tiahuanaco',
                                  'Chavín',
                                  'Caral'],
                 'correcta': 'D'},
                {'pregunta': 'En la formación de la cultura andina, el '
                             'primer resto óseo hallado perteneció al hombre '
                             'de: (UNSAAC 2013)',
                 'alternativas': ['Lauricocha',
                                  'Kotosh',
                                  'Toquepala',
                                  'Chivateros',
                                  'Lurín'],
                 'correcta': 'B'},
                {'pregunta': 'La primera evidencia sobre la domesticación '
                             'del perro fue hallada en: (UNSAAC 2013)',
                 'alternativas': ['Guitarreros',
                                  'Chilca',
                                  'Lurín',
                                  'Santo Domingo',
                                  'Kotosh'],
                 'correcta': 'B'},
                {'pregunta': 'El yacimiento arqueológico de Haldas fue '
                             'descubierto por: (UNSAAC 2013)',
                 'alternativas': ['Rosa Fung Pineda',
                                  'Federico Engel',
                                  'Josefina Ramos de Cox',
                                  'Rafael Larco Hoyle',
                                  'Junius Bird'],
                 'correcta': 'B'},
                {'pregunta': 'Los restos arqueológicos de Pumapunku, '
                             'Willcaswain y Pacatnamú corresponden '
                             'respectivamente a las culturas: (UNSAAC 2013)',
                 'alternativas': ['Chimú - Chanca - Nazca',
                                  'Tiahuanaco - Wari - Chimú',
                                  'Wari - Chimú - Paracas',
                                  'Mochica - Wari - Chavín',
                                  'Wari - Inca - Caral'],
                 'correcta': 'B'},
                {'pregunta': 'La importancia y la particularidad del hombre '
                             'de Paccaicasa se expresan en haber: (UNSAAC '
                             '2013)',
                 'alternativas': ['Iniciado la fabricación de objetos de '
                                  'arcilla',
                                  'Originado a la gran cultura andina',
                                  'Practicado el arte rupestre más antiguo '
                                  'del Perú',
                                  'Domesticado por primera vez al perro',
                                  'Dejado los primeros restos físicos del '
                                  'hombre'],
                 'correcta': 'E'},
                {'pregunta': 'El hombre de Huaca Prieta se caracterizó por: '
                             '(UNSAAC 2013)',
                 'alternativas': ['Domesticar a la alpaca, al cuy y al perro',
                                  'Ser él primer tejedor del Perú antiguo',
                                  'Presentar el taller lítico más grande del '
                                  'Perú antiguo',
                                  'Representar el inicio de la primera etapa '
                                  'alfarera',
                                  'Construir el primer monumento religioso '
                                  'de América'],
                 'correcta': 'B'},
                {'pregunta': 'La cultura Chavín tiene relación en los '
                             'centros arquitectónicos de: (UNSAAC 2013)',
                 'alternativas': ['Garagay y Chongoyape',
                                  'Wariwillca y Pachacamac',
                                  'Kalasasaya y Sillustani',
                                  'Topara y Tajahuana',
                                  'Cahuachi y Ocucaje'],
                 'correcta': 'A'},
                {'pregunta': 'Los chimús se desarrollaron en el periodo '
                             'cultural: (UNSAAC 2013)',
                 'alternativas': ['Intermedio Temprano',
                                  'Horizonte Medio',
                                  'Horizonte Medio tardío',
                                  'Intermedio Tardío',
                                  'Horizonte Temprano'],
                 'correcta': 'D'},
                {'pregunta': 'Augusto Cardich descubrió en la cueva de '
                             'Lauricocha los primeros restos físicos del '
                             'hombre peruano, los cuales corresponden a las '
                             'fuentes: (UNSAAC 2015)',
                 'alternativas': ['Monumentales',
                                  'Etnográficas',
                                  'Biológicas',
                                  'Antroposomáticas',
                                  'Materiales'],
                 'correcta': 'D'},
                {'pregunta': 'Los primeros restos humanos en el Perú antiguo '
                             'corresponden al hombre de: (UNSAAC 2016)',
                 'alternativas': ['Lauricocha',
                                  'Paccaicasa',
                                  'Chivateros',
                                  'Paiján',
                                  'Toquepala'],
                 'correcta': 'B'},
                {'pregunta': 'La organización política de la cultura Caral '
                             'fue de carácter: (UNSAAC 2016)',
                 'alternativas': ['Religioso y burocrático',
                                  'Militarizado y gerontocrático',
                                  'Militarizado y religioso',
                                  'Burocrático y militarizado',
                                  'Teocrático no militarista'],
                 'correcta': 'E'},
                {'pregunta': 'Cronológicamente los Chancas se desarrollaron '
                             'en el periodo del: (UNSAAC 2016)',
                 'alternativas': ['Horizonte temprano',
                                  'Horizonte tardío',
                                  'Intermedio tardío',
                                  'Intermedio temprano',
                                  'Horizonte medio'],
                 'correcta': 'C'},
                {'pregunta': 'El segundo agricultor del Perú fue descubierto '
                             'por Thomas Linch, en el departamento de: '
                             '(UNSAAC 2018)',
                 'alternativas': ['Huánuco',
                                  'Ilo',
                                  'Lima',
                                  'Tacna',
                                  'Ancash'],
                 'correcta': 'A'},
                {'pregunta': 'Las primeras evidencias del hombre en el Perú '
                             'fueron descubiertas en el actual departamento '
                             'de La Libertad por el científico: (UNSAAC '
                             '2018)',
                 'alternativas': ['Richard Mac Neish',
                                  'Augusto Cardich',
                                  'Edward Lanning',
                                  'Junius Bird',
                                  'Miomir Bojovich'],
                 'correcta': 'D'},
                {'pregunta': 'El conjunto arquitectónico que identifica a la '
                             'civilización de Caral es: (UNSAAC 2022)',
                 'alternativas': ['La huaca de la Luna',
                                  'El templo de Kotosh',
                                  'La Huaca del Sol',
                                  'El templo de Garagay',
                                  'El templo del Anfiteatro'],
                 'correcta': 'E'},
                {'pregunta': 'Por los hallazgos líticos, el primer poblador '
                             'del Perú fue el hombre de: (UNSAAC Ordinario)',
                 'alternativas': ['Guitarrero',
                                  'Kotosh',
                                  'Paccaicasa',
                                  'Chilca',
                                  'Lauricocha'],
                 'correcta': 'C'},
                {'pregunta': 'Del asentamiento humano de Paracas, los mantos '
                             'fueron de carácter: (UNSAAC Ordinario)',
                 'alternativas': ['Socio económico',
                                  'Económico',
                                  'Artístico',
                                  'Religioso y ritual',
                                  'Político'],
                 'correcta': 'D'},
                {'pregunta': 'La cultura Caral se ubica en el departamento '
                             'de: (UNSAAC Ordinario)',
                 'alternativas': ['Lima',
                                  'Ancash',
                                  'Ica',
                                  'La Libertad',
                                  'Lambayeque'],
                 'correcta': 'A'},
                {'pregunta': 'El hombre de Lauricocha fue descubierto por: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Richard Mac Neish',
                                  'Augusto Cardich',
                                  'Thomas Linch',
                                  'Frederic Engel',
                                  'Frederic Engel'],
                 'correcta': 'B'},
                {'pregunta': 'El asentamiento humano de Paracas fue '
                             'descubierto por: (UNSAAC Ordinario)',
                 'alternativas': ['Federico Max Uhle',
                                  'Julio Cesar Tello Rojas',
                                  'Federico Kauffman Doig',
                                  'Ruth Shady Solís',
                                  'Federico Larco Hoyle'],
                 'correcta': 'B'},
                {'pregunta': 'La construcción arquitectónica de Cahuachi '
                             'perteneció al asentamiento humano de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Nazca',
                                  'Paracas',
                                  'Tiahuanaco',
                                  'Chavín',
                                  'Wari'],
                 'correcta': 'A'},
                {'pregunta': 'La construcción del Complejo Arqueológico de '
                             'Puma Punku y las Chullpas de Sillustani '
                             'pertenecieron a: (UNSAAC Ordinario)',
                 'alternativas': ['Chavín',
                                  'Chimú',
                                  'Mochica',
                                  'Tiahuanaco',
                                  'Nazca'],
                 'correcta': 'D'},
                {'pregunta': 'La cerámica Chimú tuvo influencia de la '
                             'Cultura: (UNSAAC Ordinario)',
                 'alternativas': ['Wari',
                                  'Nazca',
                                  'Mochica',
                                  'Paracas',
                                  'Chavín'],
                 'correcta': 'C'},
                {'pregunta': 'El Altar del Fuego Sagrado, en el Perú '
                             'prehispánico, fue una manifestación '
                             'arquitectónica de la sociedad: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Chimú',
                                  'Wari',
                                  'Caral',
                                  'Paracas',
                                  'Tiahuanaco'],
                 'correcta': 'C'},
                {'pregunta': 'El hombre de Toquepala es importante en la '
                             'evolución de la cultura andina, por ser el: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Impulsor de la domesticación de camélidos',
                                  'Primer horticultor alto andino',
                                  'Primer pintor rupestre peruano',
                                  'Iniciador de la domesticación del perro',
                                  'Tallador fino más antiguo y fino'],
                 'correcta': 'C'},
                {'pregunta': 'En el proceso evolutivo de la Cultura Andina, '
                             'son consideradas culturas sedentarias: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Guitarrero - Chilca - Kotosh',
                                  'Kotosh - Santo Domingo - Lauricocha',
                                  'Huaca Prieta - Lurín - Chivateros',
                                  'Lurín - Huaca Prieta - Kotosh',
                                  'Lurín - Pikimachay - Guitarrero'],
                 'correcta': 'D'},
                {'pregunta': 'La primera manifestación arquitectónica '
                             'monumental de tipo religioso en el Perú '
                             'antiguo corresponde al hombre de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Las Aldas',
                                  'Kotosh',
                                  'Paccaicasa',
                                  'Guitarrero',
                                  'Huaca Prieta'],
                 'correcta': 'B'},
                {'pregunta': 'La manifestación arquitectónica que representa '
                             'a la cultura Chanca es: (UNSAAC Ordinario)',
                 'alternativas': ['El conjunto arqueológico de Sóndor',
                                  'El conjunto arquitectónico de la Huaca '
                                  'Rajada',
                                  'La fortificación de Pachacamac',
                                  'El conjunto arqueológico de Tarahuasi',
                                  'La fortaleza de Paramonga'],
                 'correcta': 'A'},
                {'pregunta': 'La característica que corresponde a los '
                             'primeros hombres de la Cultura Andina, en su '
                             'condición de seminómadas: (UNSAAC Ordinario)',
                 'alternativas': ['Que no producen sus alimentos, los '
                                  'consiguen a través de la caza, la pesca y '
                                  'la recolección',
                                  'La domesticación de los primeros cultivos '
                                  'y animales',
                                  'El predominio de la vida aldeana y '
                                  'construcción de las primeras ciudades '
                                  'urbanas',
                                  'El desarrollo de las actividades '
                                  'artesanales como la textilería y cerámica',
                                  'Que conviven con la megafauna de '
                                  'mastodontes y megaterios'],
                 'correcta': 'A'},
                {'pregunta': 'La civilización que es considerada como la más '
                             'antigua del Perú y América es: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Maya',
                                  'Valdivia',
                                  'Chavín',
                                  'Paracas',
                                  'Caral'],
                 'correcta': 'E'},
                {'pregunta': 'En el origen de la Cultura Andina, los '
                             'pobladores del asentamiento de Huaca Prieta se '
                             'caracterizaron por ser: (UNSAAC Ordinario)',
                 'alternativas': ['Los primeros domesticadores del perro',
                                  'Los primeros horticultores del Perú',
                                  'Maestros del arte textil',
                                  'Constructores del primer monumento '
                                  'religioso',
                                  'Los domesticadores de la llama, alpaca y '
                                  'el cuy'],
                 'correcta': 'C'},
                {'pregunta': 'De acuerdo a la periodización de Horizontes, '
                             'propuesta por John Rowe, el desarrollo de la '
                             'cultura de Wari y Tiahuanaco, corresponde al: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Horizonte del intermedio tardío',
                                  'Horizonte temprano',
                                  'Horizonte formativo',
                                  'Horizonte medio',
                                  'Intermedio temprano'],
                 'correcta': 'D'},
                {'pregunta': 'El taller lítico más grande del Perú hace '
                             'referencia al hombre de: (UNSAAC Ordinario)',
                 'alternativas': ['Paiján',
                                  'Lauricocha',
                                  'Toquepala',
                                  'Chivateros',
                                  'Complejo de Paccaicasa'],
                 'correcta': 'D'},
                {'pregunta': 'El historiador Pablo Macera considera que la '
                             'cerámica que mejor se aprecia con los ojos que '
                             'con la yema de los dedos, corresponde a la '
                             'Cultura: (UNSAAC Ordinario)',
                 'alternativas': ['Chavín',
                                  'Wari',
                                  'Tiahuanaco',
                                  'Mochica',
                                  'Nazca'],
                 'correcta': 'D'},
                {'pregunta': 'El hombre de Paccaicasa se caracteriza por: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Domesticar la llama y la alpaca',
                                  'Ser el primer músico peruano, al fabricar '
                                  'las primeras flautas',
                                  'Representar al primer resto fósil humano '
                                  'del Perú',
                                  'Ser el Iniciador de la Cultura Andina',
                                  'Practicar ritos y ceremonias a la tierra'],
                 'correcta': 'C'},
                {'pregunta': 'La pintura rupestre más antigua del Perú, '
                             'pertenece al hombre de: (I CEPRU 2010)',
                 'alternativas': ['Paiján',
                                  'Toquepala',
                                  'Santo domingo',
                                  'Lauricocha',
                                  'Chilca'],
                 'correcta': 'B'},
                {'pregunta': 'El textil Cóndor Andino pertenece al hombre '
                             'sedentario de: (I CEPRU 2010)',
                 'alternativas': ['Cerro Paloma',
                                  'Chilca',
                                  'Lurín',
                                  'Kotosh',
                                  'Huaca Prieta'],
                 'correcta': 'E'},
                {'pregunta': 'El primer pescador con red en el Perú, durante '
                             'el periodo de los horticultores fue: (II CEPRU '
                             '2012)',
                 'alternativas': ['Paiján',
                                  'Lurín',
                                  'Santo Domingo',
                                  'Chilca',
                                  'Guitarrero'],
                 'correcta': 'D'},
                {'pregunta': 'Las tumbas subterráneas en forma de copa '
                             'invertida o de botella pertenecieron a la '
                             'sociedad: (II CEPRU 2012)',
                 'alternativas': ['Mochica Chicama',
                                  'Paracas Cavernas',
                                  'Nazca Cahuachi',
                                  'Paracas Necrópolis',
                                  'Tiahuanaco Kalasasaya'],
                 'correcta': 'D'},
                {'pregunta': 'La Huaca del Sol fue dedicada al culto del '
                             'Dios: (II CEPRU 2012)',
                 'alternativas': ['Señora de Cao',
                                  'Señor de Sipán',
                                  'Naylamp',
                                  'Cie Quich',
                                  'Aiapaec'],
                 'correcta': 'E'},
                {'pregunta': 'Uno de los fundadores de la sociedad Chanca, '
                             'fue: (II CEPRU 2012)',
                 'alternativas': ['Sondor',
                                  'Uranmarca',
                                  'Curamba',
                                  'Uscovilca',
                                  'Astowaranca'],
                 'correcta': 'D'},
                {'pregunta': 'El hombre de Santo Domingo se caracteriza por: '
                             '(II CEPRU 2013)',
                 'alternativas': ['Desarrollar el taller lítico más grande '
                                  'del Perú antiguo',
                                  'Ser uno de los primeros músicos del Perú',
                                  'Domesticar a la llama y al cuy',
                                  'Representar la primera etapa alfarera en '
                                  'el Perú',
                                  'Practicar la primera agricultura andina'],
                 'correcta': 'D'},
                {'pregunta': 'Según los últimos avances arqueológicos, '
                             'Caral: (I CEPRU 2014)',
                 'alternativas': ['Representa el primer imperio andino',
                                  'Se desarrolló en el periodo cultural '
                                  'formativo',
                                  'Tuvo un estado exclusivamente militarista',
                                  'Es la civilización más antigua del Perú y '
                                  'América',
                                  'Fue una civilización con expansión '
                                  'cultural pan peruana'],
                 'correcta': 'D'},
                {'pregunta': 'A la cultura Nazca se le atribuye: (I CEPRU '
                             '2014)',
                 'alternativas': ['El gigantesco calendario astronómico',
                                  'Las pinturas murales de Pañamarca',
                                  'La construcción de ciudades cabeza de '
                                  'región',
                                  'La organización del primer estado '
                                  'teocrático en el Perú',
                                  'El centro arqueológico de Wariwilca'],
                 'correcta': 'A'},
                {'pregunta': 'La civilización Caral se ubica en el valle '
                             'medio del río:',
                 'alternativas': ['Pativilca',
                                  'Supe',
                                  'Chillón',
                                  'Huaura',
                                  'Chancay'],
                 'correcta': 'B'},
                {'pregunta': 'La arqueóloga que descubrió la ciudadela '
                             'sagrada de Caral en 1996 fue:',
                 'alternativas': ['Ruth Shady Solís',
                                  'Julio C. Tello',
                                  'María Reiche',
                                  'Rebeca Carrión Cachot',
                                  'Elena Pardo'],
                 'correcta': 'A'},
                {'pregunta': 'Caral fue declarada Patrimonio Cultural de la '
                             'Humanidad por la UNESCO en:',
                 'alternativas': ['1979', '2000', '1994', '1996', '2009'],
                 'correcta': 'E'},
                {'pregunta': 'En Caral se encontró el más antiguo elemento '
                             'de registro numérico conocido en el Perú, '
                             'llamado:',
                 'alternativas': ['Tocapu',
                                  'Kero',
                                  'Chuspa',
                                  'Quipu',
                                  'Yupana'],
                 'correcta': 'D'},
                {'pregunta': 'La cultura Chavín se ubica en el distrito de '
                             'Huántar, provincia de Huari, en la región:',
                 'alternativas': ['Junín',
                                  'La Libertad',
                                  'Huánuco',
                                  'Cajamarca',
                                  'Áncash'],
                 'correcta': 'E'},
                {'pregunta': 'Chavín fue descubierta por el arqueólogo:',
                 'alternativas': ['Luis Lumbreras',
                                  'Julio C. Tello',
                                  'Ruth Shady',
                                  'Max Uhle',
                                  'Federico Kauffmann'],
                 'correcta': 'B'},
                {'pregunta': 'El monolito de Chavín que representa al dios '
                             'Viracocha en forma de jaguar, descubierto por '
                             'Timoteo Espinoza, se llama:',
                 'alternativas': ['Estela de Raimondi',
                                  'Portada del Sol',
                                  'Cabeza Clava',
                                  'Lanzón Monolítico',
                                  'Obelisco de Tello'],
                 'correcta': 'A'},
                {'pregunta': 'La cultura Paracas fue descubierta por Julio '
                             'C. Tello en:',
                 'alternativas': ['1919', '1902', '1901', '1937', '1925'],
                 'correcta': 'E'},
                {'pregunta': 'La etapa de Paracas caracterizada por tumbas '
                             'subterráneas cuadrangulares, con capital en '
                             'Topara, se llama:',
                 'alternativas': ['Paracas Formativo',
                                  'Paracas Clásico',
                                  'Paracas Cavernas',
                                  'Paracas Necrópolis',
                                  'Paracas Tardío'],
                 'correcta': 'D'},
                {'pregunta': 'Según Tello, el porcentaje de cráneos de '
                             'momias paracas con señales de trepanación en '
                             'vida fue de:',
                 'alternativas': ['10%', '80%', '40%', '20%', '60%'],
                 'correcta': 'C'},
                {'pregunta': 'La cultura Nasca fue descubierta por:',
                 'alternativas': ['María Reiche',
                                  'Federico Max Uhle',
                                  'Toribio Mejía Xesspe',
                                  'Paul Kosok',
                                  'Julio C. Tello'],
                 'correcta': 'B'},
                {'pregunta': 'La tecnología de canales de riego subterráneo '
                             'desarrollada por los nasca para aprovechar '
                             'aguas del subsuelo se llama:',
                 'alternativas': ['Cochas',
                                  'Andenes',
                                  'Waru waru',
                                  'Camellones',
                                  'Puquios'],
                 'correcta': 'E'},
                {'pregunta': 'Las Líneas de Nasca fueron descubiertas en '
                             '1927 por:',
                 'alternativas': ['Federico Max Uhle',
                                  'Julio C. Tello',
                                  'Toribio Mejía Xesspe',
                                  'Paul Kosok',
                                  'María Reiche'],
                 'correcta': 'C'},
                {'pregunta': 'La capital de la cultura Nasca fue la ciudad '
                             'de:',
                 'alternativas': ['Cahuachi',
                                  'Tambo Viejo',
                                  'Estaquería',
                                  'Ocucaje',
                                  'Paredones'],
                 'correcta': 'A'},
                {'pregunta': 'La cultura Mochica tuvo su capital en la '
                             'ciudad de:',
                 'alternativas': ['Pachacamac',
                                  'Moche',
                                  'Chan Chan',
                                  'Cajamarquilla',
                                  'Sipán'],
                 'correcta': 'B'},
                {'pregunta': 'La máxima autoridad o rey de la sociedad '
                             'mochica era llamado:',
                 'alternativas': ['Curaca',
                                  'Cie Quich',
                                  'Inca',
                                  'Naylamp',
                                  'Aiapaec'],
                 'correcta': 'B'},
                {'pregunta': 'La Huaca Rajada del Señor de Sipán fue '
                             'descubierta por Walter Alva en el año:',
                 'alternativas': ['1979', '1937', '1987', '1994', '1901'],
                 'correcta': 'C'},
                {'pregunta': 'Los ceramios mochica que expresan estados '
                             'psicológicos de las personas se llaman:',
                 'alternativas': ['Tumis',
                                  'Keros',
                                  'Pebeteros',
                                  'Huacos retratos',
                                  'Ídolos'],
                 'correcta': 'D'},
                {'pregunta': 'La cultura Tiahuanaco se ubica al sureste del '
                             'lago Titicaca, en el actual territorio de:',
                 'alternativas': ['Bolivia',
                                  'Perú',
                                  'Ecuador',
                                  'Chile',
                                  'Argentina'],
                 'correcta': 'A'},
                {'pregunta': 'El dios principal de Tiahuanaco, creador del '
                             'mundo andino, fue:',
                 'alternativas': ['Pachacámac',
                                  'Wiracocha',
                                  'Inti',
                                  'Aiapaec',
                                  'Ai Apaec'],
                 'correcta': 'B'},
                {'pregunta': 'La escultura de Tiahuanaco tallada en una sola '
                             'piedra, ubicada en el complejo de Kalasasaya, '
                             'se llama:',
                 'alternativas': ['Lanzón Monolítico',
                                  'Estela de Raimondi',
                                  'Monolito Bennett',
                                  'Obelisco de Tello',
                                  'Portada del Sol'],
                 'correcta': 'E'},
                {'pregunta': 'La cultura Wari fue descubierta por el '
                             'arqueólogo:',
                 'alternativas': ['Max Uhle',
                                  'Federico Max Uhle',
                                  'Julio C. Tello',
                                  'Ruth Shady',
                                  'Luis Guillermo Lumbreras'],
                 'correcta': 'E'},
                {'pregunta': 'Según Pablo Macera, los waris son producto de '
                             'la fusión de 4 pueblos: Huarpa, Nasca, '
                             'Pachacamac y:',
                 'alternativas': ['Paracas',
                                  'Tiahuanaco',
                                  'Chavín',
                                  'Mochica',
                                  'Chimú'],
                 'correcta': 'B'},
                {'pregunta': 'La ciudad Wari ubicada en Cusco, importante '
                             'centro administrativo, fue:',
                 'alternativas': ['Wariwillca',
                                  'Pikillacta',
                                  'Cajamarquilla',
                                  'Cerro Baúl',
                                  'Willkawain'],
                 'correcta': 'B'},
                {'pregunta': 'La capital de la cultura Chimú, considerada la '
                             'ciudad de barro más grande, fue:',
                 'alternativas': ['Purgatorio',
                                  'Apurlec',
                                  'Pacatnamú',
                                  'Chan Chan',
                                  'Sipán'],
                 'correcta': 'D'},
                {'pregunta': 'El último gobernante chimú, derrotado por '
                             'Túpac Inca Yupanqui, fue:',
                 'alternativas': ['Cie Quich',
                                  'Naylamp',
                                  'Uscovilca',
                                  'Minchancamán',
                                  'Cuismancu'],
                 'correcta': 'D'},
                {'pregunta': 'Tras su conquista, los chimú fueron '
                             'incorporados al Estado Inca como principal '
                             'población del:',
                 'alternativas': ['Collasuyo',
                                  'Contisuyo',
                                  'Antisuyo',
                                  'Chinchaysuyo',
                                  'Cuntisuyo'],
                 'correcta': 'D'},
                {'pregunta': 'El reino Chanca surgió en el territorio de '
                             'Huancavelica, Ayacucho y Apurímac tras la '
                             'caída de la cultura:',
                 'alternativas': ['Mochica',
                                  'Tiahuanaco',
                                  'Chimú',
                                  'Wari',
                                  'Nasca'],
                 'correcta': 'D'},
                {'pregunta': 'Los fundadores míticos del reino Chanca fueron '
                             'Uscovilca y:',
                 'alternativas': ['Sinchi Roca',
                                  'Ancovilca',
                                  'Manco Cápac',
                                  'Cápac Yupanqui',
                                  'Pachacútec'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'CIVILIZACIÓN CARAL: UBICACIÓN Y '
                                'DESCUBRIMIENTO / CIVILIZACIÓN CARAL: SOCIED',
                      'items': ['Caral se ubica en la región Lima, provincia '
                                'de Barranca, distrito de Supe, en el valle '
                                'medio del río Supe.',
                                'La antigüedad de Caral es de 2800 a.C., '
                                'posterior a Egipto (2900 a.C.) y '
                                'Mesopotamia (3000 a.C.).',
                                'Caral es considerada la civilización más '
                                'antigua del Perú y de América.',
                                'Tuvo un gobierno de carácter teocrático, no '
                                'militarizado, dirigido por sacerdotes '
                                'astrónomos.',
                                'Caral está conformada por 32 conjuntos '
                                'arquitectónicos: pirámides, templos, '
                                'sectores residenciales, anfiteatro, '
                                'almacenes y altares.',
                                'Entre sus construcciones destacan el Templo '
                                'Anfiteatro, el Templo Mayor, la Pirámide de '
                                'la Cantera y el Altar del Fuego Sagrado.']},
                     {'titulo': 'CHAVÍN: UBICACIÓN Y SOCIEDAD (HORIZONTE '
                                'TEMPRANO) / CHAVÍN: ARQUITECTURA Y ',
                      'items': ['Chavín se ubica en el distrito de Huántar, '
                                'provincia de Huari, región Áncash, a '
                                'orillas de los ríos Mosna y Huachecsa.',
                                'Chavín es considerada una cultura '
                                'panperuana por su amplia influencia en '
                                'sierra, costa y ceja de selva.',
                                'El templo principal, de forma piramidal '
                                'trunca con patios en forma de U, se ubica '
                                'en Chavín de Huántar.',
                                'El Lanzón Monolítico y las cabezas clavas '
                                'son monolitos que representan guardianes '
                                'del templo.',
                                'Paracas se ubica en el departamento de Ica, '
                                'provincia de Pisco, entre Cañete y Yauca.',
                                'Fue descubierta por Julio C. Tello en 1925, '
                                'y estudiada también por Toribio Mejía '
                                'Xesspe.']},
                     {'titulo': 'PARACAS: MOMIFICACIÓN, TREPANACIONES Y '
                                'TEJIDOS / NASCA: UBICACIÓN Y SOCIEDA',
                      'items': ['Los paracas practicaron la momificación, '
                                'con alto conocimiento de anatomía y '
                                'fisiología.',
                                'Practicaron trepanaciones craneanas, usando '
                                'coca como anestésico e instrumentos como el '
                                'cincel tumi.',
                                'Nasca tuvo su centro en el valle de Río '
                                'Grande, provincia de Nasca, departamento de '
                                'Ica; es cultura regional.',
                                'Fue descubierta por Federico Max Uhle en '
                                '1901.',
                                'La cerámica nasca es pictórica (con temor '
                                'al vacío), policroma (8 colores), realista '
                                'y fantástica.',
                                'Su capital fue Cahuachi; otras ciudades '
                                'fueron Estaquería, Tambo Viejo y Ocucaje.']},
                     {'titulo': 'MOCHICA: UBICACIÓN Y SOCIEDAD (INTERMEDIO '
                                'TEMPRANO) / MOCHICA: CERÁMICA Y A',
                      'items': ['Mochica se desarrolló en los valles de '
                                'Moche, Chicama y Virú, en La Libertad; su '
                                'capital fue Moche.',
                                'Fue descubierta por Federico Max Uhle en '
                                '1902; es cultura regional.',
                                'La cerámica mochica alcanzó el nivel más '
                                'alto del Perú Antiguo, destacando los '
                                'huacos retratos, que expresan estados '
                                'psicológicos.',
                                'Es de forma globular con asa estribo y un '
                                'solo pico; predominó la bicromía rojo ocre '
                                'y blanco crema.',
                                'Tiahuanaco se ubica a 21 km al sureste del '
                                'lago Titicaca (Bolivia); es cultura '
                                'panperuana.',
                                'Fue descubierta por el cronista Pedro Cieza '
                                'de León en 1551.']},
                     {'titulo': 'TIAHUANACO: TECNOLOGÍA Y ARTE / WARI: '
                                'UBICACIÓN Y ORIGEN (HORIZONTE MEDIO) ',
                      'items': ['Construyeron camellones o waru waru, suelos '
                                'elevados alrededor de lagos, y elaboraron '
                                'chuño y moraya.',
                                'En arquitectura usaron grandes bloques de '
                                'piedra con grapas de cobre; destacan '
                                'Kalasasaya, Akapana y Pumapunku.',
                                'Wari se ubica a 12 km al noroeste de '
                                'Ayacucho; es cultura panperuana, con '
                                'capital en la ciudad de Wari o Viñaque.',
                                'Fue descubierta por Luis Guillermo '
                                'Lumbreras.',
                                'Constituyeron un gran Estado '
                                'militarista-teocrático de tipo imperial, '
                                'dirigido por una élite militar.',
                                'Construyeron una importante red de caminos '
                                'para comunicar a los pueblos sometidos.']},
                     {'titulo': 'CHIMÚ: UBICACIÓN Y ARQUITECTURA (INTERMEDIO '
                                'TARDÍO) / CHIMÚ: METALURGIA Y C',
                      'items': ['Chimú se originó en el valle de Chimor, La '
                                'Libertad; su capital fue Chan Chan, la '
                                'ciudad de barro más grande.',
                                'Es cultura regional, descubierta por '
                                'Federico Max Uhle en 1902.',
                                'Los chimú fueron los más grandes joyeros '
                                'del Perú antiguo, dominando el martillado, '
                                'soldadura y fundición.',
                                'Fabricaron el Tumi, cuchillo ceremonial, y '
                                'vasos con incrustaciones de piedras '
                                'preciosas.',
                                'Chanca se desarrolló en Huancavelica, '
                                'Ayacucho, Apurímac (río Pampas) y parte del '
                                'Cusco.',
                                'Sus fundadores míticos fueron Uscovilca y '
                                'Ancovilca.']}],
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
  'secciones': [{'titulo': '7.1 EL AYLLU: LOS SIETE VÍNCULOS',
                 'items': ['El {ayllu} fue la unidad esencial de la '
                           'organización social inca, con jefe llamado '
                           '{curaca}.',
                           'Vínculo de {territorio}: los miembros del ayllu '
                           'compartían un mismo espacio geográfico llamado '
                           'marka.',
                           'Vínculo de {economía}: trabajaban colectivamente '
                           'las tierras de todos.',
                           'Vínculo de {tótem}: reconocían un antepasado '
                           'común sacralizado; vínculo de {origen}: '
                           'reconocían una Pacarina común.']},
                {'titulo': '7.2 LO SOCIAL: ETNIAS Y CLASES',
                 'items': ['La sociedad inca fue {multiétnica}: incluía '
                           'collas y lupacas (altiplano), chinchas (costa '
                           'sur), chancas (Apurímac) y huancas (Junín).',
                           'La {nobleza de sangre} descendía del Qhapaq y la '
                           'Qoya; la nobleza por {privilegio} ascendía por '
                           'méritos.',
                           'Los {hatun runas} eran los ciudadanos del '
                           'Tahuantinsuyo en pleno ejercicio de sus '
                           'obligaciones.',
                           'Los {yanacunas} eran prisioneros de guerra '
                           'sometidos a servidumbre perpetua, condición '
                           'heredable.',
                           'Los {mitimaes} eran de tres clases: de '
                           'conquista, de {colonización}, y de castigo por '
                           'rebeldía.']},
                {'titulo': '7.3 ESTRUCTURA POLÍTICA DEL ESTADO INCA',
                 'items': ['El Estado Inca fue una monarquía {absolutista}, '
                           'teocrática, militarista, hereditaria y '
                           'centralista.',
                           'El {Qhapaq} (Inca) era la máxima autoridad, '
                           'considerado hijo del Sol; el trono se heredaba '
                           'de padre a hijo.',
                           'El {Consejo de Suyos} (Suyuyuc Apu) estaba '
                           'conformado por los cuatro jefes de suyo.',
                           'El {Apunchic} era el gobernante de las '
                           'provincias o guamaníes, representando al Qhapaq.',
                           'El {Tukuy Rikuq}, «el que todo lo ve», '
                           'supervisaba política, militar y económicamente '
                           'el Tahuantinsuyo.',
                           'El {Sinchi} era el jefe militar, con función '
                           'principal en tiempos de guerra.']},
                {'titulo': '7.4 ORGANIZACIÓN ADMINISTRATIVA: SISTEMA DECIMAL',
                 'items': ['El idioma oficial del Tahuantinsuyo fue el {Runa '
                           'Simi} o quechua.',
                           'La red de caminos que unía el Tahuantinsuyo se '
                           'llamó {Qhapac Ñan}.',
                           'El sistema de contabilidad y registro estatal se '
                           'realizaba mediante los {quipus}.',
                           'La población se organizó bajo el sistema '
                           'decimal: {Purej} (jefe de familia), Pisca '
                           'Camayoc (5 familias), Chunca Camayoc (10 '
                           'familias).',
                           'El {Huno Camayoc} era jefe de 10 000 familias; '
                           'el Suyuyuc Apu, jefe de un suyo.']},
                {'titulo': '7.5 ADMINISTRACIÓN Y CONTROL DE PISOS ECOLÓGICOS',
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
                {'titulo': '7.6 LO ECONÓMICO',
                 'items': ['La base económica fue la {agricultura}, apoyada '
                           'en los {andenes} y en obras de irrigación.',
                           'Principios que la rigieron: la {reciprocidad} '
                           '(intercambio de trabajo y favores) y la '
                           '{redistribución} (el Estado repartía lo '
                           'acumulado en los {tambos} y collcas).',
                           'La propiedad de la tierra se dividía en tierras '
                           'del {Sol}, del {Inca} y del {pueblo} o ayllu.']},
                {'titulo': '7.7 LAS FORMAS DE TRABAJO INCA',
                 'items': ['El {ayni} era una forma de trabajo colectivo, de '
                           'ayuda mutua entre familias del ayllu.',
                           'La {mita} era una forma de trabajo obligatorio, '
                           'rotativo, en beneficio del Estado.',
                           'El {minka} era una forma de trabajo limitado o '
                           'comunal para obras de interés colectivo.',
                           'El {chunka} era una forma de trabajo equitativo, '
                           'general y alternable.',
                           'La {redistribución} era el sistema por el cual '
                           'el Inca hacía llegar a los ayllus beneficios '
                           'como ropa y herramientas.']},
                {'titulo': '7.8 EXPRESIONES ARTÍSTICAS',
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
                                  'La panaca',
                                  'El ayllu',
                                  'El curacazgo',
                                  'La marka'],
                 'correcta': 'C'},
                {'pregunta': 'La ayuda mutua y recíproca entre familias se '
                             'denominaba:',
                 'alternativas': ['Chunca',
                                  'Mita',
                                  'Camayoc',
                                  'Minka',
                                  'Ayni'],
                 'correcta': 'E'},
                {'pregunta': 'El trabajo por turnos al servicio del Estado '
                             'inca se llamaba:',
                 'alternativas': ['Minka',
                                  'Chaco',
                                  'Ayni',
                                  'Mita',
                                  'Yanaconaje'],
                 'correcta': 'D'},
                {'pregunta': 'El trabajo comunal en beneficio del propio '
                             'ayllu se denominaba:',
                 'alternativas': ['Mita',
                                  'Ayni',
                                  'Faena estatal',
                                  'Minka',
                                  'Tributo'],
                 'correcta': 'D'},
                {'pregunta': 'La esposa principal del Inca recibía el nombre '
                             'de:',
                 'alternativas': ['Palla',
                                  'Aclla',
                                  'Ñusta',
                                  'Mamacona',
                                  'Coya'],
                 'correcta': 'E'},
                {'pregunta': 'El funcionario inspector llamado «el que todo '
                             'lo ve» fue:',
                 'alternativas': ['Amauta',
                                  'Apunchic',
                                  'Quipucamayoc',
                                  'Curaca',
                                  'Tucuyricuy'],
                 'correcta': 'E'},
                {'pregunta': 'El gobernador provincial en el Tahuantinsuyo '
                             'fue:',
                 'alternativas': ['Tucuyricuy',
                                  'Apunchic',
                                  'Curaca',
                                  'Willac Umu',
                                  'Sinchi'],
                 'correcta': 'B'},
                {'pregunta': '«Tahuantinsuyo» significa:',
                 'alternativas': ['Casa del Inca',
                                  'Tierra del Sol',
                                  'Las cuatro regiones unidas',
                                  'El gran camino',
                                  'Ombligo del mundo'],
                 'correcta': 'C'},
                {'pregunta': 'NO es una de las cuatro regiones del '
                             'Tahuantinsuyo:',
                 'alternativas': ['Contisuyo',
                                  'Chimusuyo',
                                  'Chinchaysuyo',
                                  'Collasuyo',
                                  'Antisuyo'],
                 'correcta': 'B'},
                {'pregunta': 'El principio por el cual el Estado repartía lo '
                             'acumulado se denomina:',
                 'alternativas': ['Ayni',
                                  'Tributación',
                                  'Reciprocidad',
                                  'Redistribución',
                                  'Mita'],
                 'correcta': 'D'},
                {'pregunta': 'Los depósitos estatales incas donde se '
                             'almacenaban productos se llamaban:',
                 'alternativas': ['Pucaras',
                                  'Ushnu',
                                  'Kallanka',
                                  'Cancha',
                                  'Collcas y tambos'],
                 'correcta': 'E'},
                {'pregunta': 'La tierra en el Tahuantinsuyo se dividía en '
                             'tierras del Sol, del Inca y:',
                 'alternativas': ['De los sacerdotes',
                                  'De los curacas',
                                  'Del ejército',
                                  'Del pueblo o ayllu',
                                  'De los yanaconas'],
                 'correcta': 'D'},
                {'pregunta': 'El recipiente cerámico de base cónica usado '
                             'para la chicha fue:',
                 'alternativas': ['El cántaro',
                                  'El kero',
                                  'El aríbalo',
                                  'El huaco retrato',
                                  'El paccha'],
                 'correcta': 'C'},
                {'pregunta': 'El tejido más fino de los incas se denominaba:',
                 'alternativas': ['Abasca',
                                  'Cumbi',
                                  'Llicllia',
                                  'Unku',
                                  'Chusi'],
                 'correcta': 'B'},
                {'pregunta': 'Los encargados de leer y elaborar los quipus '
                             'fueron los:',
                 'alternativas': ['Quipucamayocs',
                                  'Chasquis',
                                  'Amautas',
                                  'Camayocs',
                                  'Haravicus'],
                 'correcta': 'A'},
                {'pregunta': 'El templo principal del Cusco, dedicado al '
                             'Sol, fue:',
                 'alternativas': ['Sacsayhuamán',
                                  "Q'enqo",
                                  'Ollantaytambo',
                                  'Tambomachay',
                                  'El Coricancha'],
                 'correcta': 'E'},
                {'pregunta': 'La base de la economía inca fue:',
                 'alternativas': ['La pesca',
                                  'La ganadería exclusivamente',
                                  'La minería',
                                  'La agricultura',
                                  'El comercio'],
                 'correcta': 'D'},
                {'pregunta': 'Los andenes tuvieron como finalidad principal:',
                 'alternativas': ['Uso ceremonial',
                                  'Control astronómico',
                                  'Ampliar y proteger la frontera agrícola',
                                  'Funciones funerarias',
                                  'Fines militares'],
                 'correcta': 'C'},
                {'pregunta': 'La nobleza inca se dividía en nobleza de '
                             'sangre y nobleza de:',
                 'alternativas': ['Privilegio',
                                  'Territorio',
                                  'Comercio',
                                  'Guerra',
                                  'Religión'],
                 'correcta': 'A'},
                {'pregunta': 'El Consejo Imperial que asesoraba al Inca se '
                             'denominaba:',
                 'alternativas': ['Willac Umu',
                                  'Apunchic',
                                  'Tahuantinsuyo Camachic',
                                  'Curacazgo',
                                  'Panaca'],
                 'correcta': 'C'},
                {'pregunta': 'El jefe del ayllu, encargado de la '
                             'administración directa del territorio comunal, '
                             'era el:',
                 'alternativas': ['Coya',
                                  'Apunchic',
                                  'Tucuyricuy',
                                  'Quipucamayoc',
                                  'Curaca'],
                 'correcta': 'E'},
                {'pregunta': 'El funcionario inca conocido como «el que todo '
                             'lo ve», inspector en las provincias, era el:',
                 'alternativas': ['Apunchic',
                                  'Tucuyricuy',
                                  'Villac Umu',
                                  'Curaca',
                                  'Sinchi'],
                 'correcta': 'B'},
                {'pregunta': 'El Tahuantinsuyo, como institución '
                             'consolidada, fue obra principalmente del inca:',
                 'alternativas': ['Túpac Yupanqui',
                                  'Huayna Cápac',
                                  'Huáscar',
                                  'Manco Cápac',
                                  'Pachacútec'],
                 'correcta': 'E'},
                {'pregunta': 'Las mujeres escogidas, autorizadas '
                             'exclusivamente para tejer los ropajes del '
                             'Inca, se llamaban:',
                 'alternativas': ['Acllas',
                                  'Mamaconas exclusivas',
                                  'Pallas',
                                  'Coyas',
                                  'Ñustas'],
                 'correcta': 'A'},
                {'pregunta': 'Los depósitos estatales incas donde se '
                             'almacenaban productos del Tahuantinsuyo se '
                             'llamaban:',
                 'alternativas': ['Chullpas',
                                  'Collcas y tambos',
                                  'Kanchas',
                                  'Ushnus',
                                  'Andenes'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema por el cual un mismo ayllu '
                             'cultivaba tierras en distintas zonas '
                             'climáticas se llama:',
                 'alternativas': ['Control de pisos ecológicos',
                                  'Mitmaq exclusivo',
                                  'Redistribución',
                                  'Ayni',
                                  'Reciprocidad'],
                 'correcta': 'A'},
                {'pregunta': 'Los lupacas, pobladores del altiplano, '
                             'ejemplificaron el control de pisos ecológicos '
                             'al mantener tierras cultivadas también en:',
                 'alternativas': ['La sierra alta exclusivamente',
                                  'El desierto de Atacama',
                                  'La selva',
                                  'La costa',
                                  'Otro país'],
                 'correcta': 'D'},
                {'pregunta': 'Los andenes incas tuvieron como finalidad '
                             'principal:',
                 'alternativas': ['Solo la vivienda',
                                  'Ampliar y proteger la frontera agrícola',
                                  'Solo el culto religioso',
                                  'Solo la defensa militar',
                                  'Solo el almacenamiento de agua'],
                 'correcta': 'B'},
                {'pregunta': 'En la evolución histórica de los incas, el '
                             'periodo de la Confederación Cusqueña fue '
                             'gobernado entre otros por: (UNSAAC 2010)',
                 'alternativas': ['Pachacútec y Huayna Cápac',
                                  'Huayna Cápac y Sinchi Roca',
                                  'Yahuar Huacac y Huiracocha',
                                  'Huáscar y Manco Cápac',
                                  'Huayna Cápac y Atahualpa'],
                 'correcta': 'C'},
                {'pregunta': 'En la historia de la evolución incaica, en el '
                             'Periodo Legendario gobernaron: (UNSAAC 2010)',
                 'alternativas': ['Manco Cápac y Sinchi Roca',
                                  'Huiracocha y Cápac Yupanqui',
                                  'Lloque Yupanqui y Mayta Cápac',
                                  'Pachacútec y Huayna Cápac',
                                  'Inca Roca y Yahuar Huacac'],
                 'correcta': 'C'},
                {'pregunta': 'En la organización social inca, el Phiwichuri '
                             'era el: (UNSAAC 2011)',
                 'alternativas': ['Jefe militar',
                                  'Jefe de ayllu',
                                  'Gobernador de provincias',
                                  'Hijo primogénito',
                                  'Príncipe heredero'],
                 'correcta': 'B'},
                {'pregunta': 'En el Tahuantinsuyo, el organismo asesor del '
                             'inca lo constituía el: (UNSAAC 2011)',
                 'alternativas': ['Auqui',
                                  'Curaca',
                                  'Sinchi',
                                  'Consejo de suyos',
                                  'Apunchic'],
                 'correcta': 'D'},
                {'pregunta': 'En la organización económica inca, en las '
                             'tierras comunales se trabajaba a través del '
                             'sistema denominado: (UNSAAC 2011)',
                 'alternativas': ['Ayni', 'Mita', 'Huaki', 'Minka', 'Chunca'],
                 'correcta': 'A'},
                {'pregunta': 'El inca Pachacútec derrotó a los Chancas en el '
                             'periodo: (UNSAAC 2011)',
                 'alternativas': ['De la decadencia',
                                  'Imperial o de la Expansión',
                                  'Regional o de la Confederación Cusqueña',
                                  'Localista',
                                  'Legendario, Curacal'],
                 'correcta': 'B'},
                {'pregunta': 'El Qhapaq que institucionalizó el '
                             'Tahuantinsuyo fue: (UNSAAC 2013)',
                 'alternativas': ['Wayna Cápac',
                                  'Inca Roca',
                                  'Manco Cápac',
                                  'Pachacútec',
                                  'Wiracocha'],
                 'correcta': 'D'},
                {'pregunta': 'Los jefes de los pueblos incorporados al '
                             'Tahuantinsuyo constituyeron la nobleza: '
                             '(UNSAAC 2013)',
                 'alternativas': ['De Parentesco',
                                  'Por privilegio',
                                  'Provincial',
                                  'Regional',
                                  'De Sangre'],
                 'correcta': 'B'},
                {'pregunta': 'En el gobierno de las provincias, el que '
                             'representaba al Qhapaq como autoridad fue el: '
                             '(UNSAAC 2013)',
                 'alternativas': ['Tukuy Rikuc',
                                  'Kuraka',
                                  'Apunchic',
                                  'Auqui',
                                  'Sinchi'],
                 'correcta': 'C'},
                {'pregunta': 'En la evolución histórica de los incas, son '
                             'considerados sinchis los gobernantes: (UNSAAC '
                             '2013)',
                 'alternativas': ['Pachacútec - Tupac Inca Yupanqui',
                                  'Sayri Tupac - Titu Cusi Yupanqui',
                                  'Sinchi Roca - Inca Roca',
                                  'Lloque Yupanqui - Mayta Cápac',
                                  'Huáscar - Toparpa'],
                 'correcta': 'C'},
                {'pregunta': 'En la Guerra Civil, Huáscar y Atahualpa se '
                             'disputaron el trono de: (UNSAAC 2013)',
                 'alternativas': ['Inca Yupanqui',
                                  'Tupac Inca Yupanqui',
                                  'Cápac Yupanqui',
                                  'Pachacútec',
                                  'Huayna Cápac'],
                 'correcta': 'E'},
                {'pregunta': 'En el desarrollo del Tahuantinsuyo, los '
                             'pueblos que se trasladaban a lugares '
                             'despoblados eran mitimaes de: (UNSAAC 2013)',
                 'alternativas': ['Castigo',
                                  'Conquista',
                                  'Ocupación',
                                  'Colonización',
                                  'Invasión'],
                 'correcta': 'D'},
                {'pregunta': 'En la administración de la población del '
                             'Tahuantinsuyo, el Hunu Camayoc era el jefe de: '
                             '(UNSAAC 2013)',
                 'alternativas': ['100 familias',
                                  '10 000 familias',
                                  '1 familia',
                                  '1 000 familias',
                                  '10 familias'],
                 'correcta': 'E'},
                {'pregunta': 'El periodo regional de la historia de los '
                             'incas está marcado por: (UNSAAC 2013)',
                 'alternativas': ['El sometimiento de los Chancas',
                                  'La expansión territorial regional',
                                  'La conquista del oriente peruano',
                                  'El gobierno de curacas',
                                  'La confederación de ayllus quechuas'],
                 'correcta': 'A'},
                {'pregunta': 'En la sociedad Inca, los Yanáconas: (UNSAAC '
                             '2013)',
                 'alternativas': ['Eran personas encargadas de colonizar '
                                  'tierras',
                                  'Representaban una forma de servidumbre',
                                  'Poblaron las zonas fronterizas del '
                                  'territorio',
                                  'No tenían el derecho de ascender '
                                  'socialmente',
                                  'Se trasladaban de un lugar a otro'],
                 'correcta': 'D'},
                {'pregunta': 'La redistribución, como una forma económica de '
                             'los incas, consistía en: (UNSAAC 2013)',
                 'alternativas': ['La ocupación constante de tierras '
                                  'dispersas y crianzas',
                                  'La asignación de tareas por parte del '
                                  'Inca y sus funcionarios',
                                  'La repartición de alimentos excedentes en '
                                  'tiempos de crisis',
                                  'El disfrute de bienes según sus '
                                  'necesidades',
                                  'La circulación de bienes en el mercado '
                                  'regional'],
                 'correcta': 'C'},
                {'pregunta': 'Los gobernantes del Incario o Legendario '
                             'corresponden al periodo: (UNSAAC 2016)',
                 'alternativas': ['Manco Cápac y Yahuar Huacac',
                                  'Manco Cápac y Mayta Cápac',
                                  'Manco Cápac y Lloque Yupanqui',
                                  'Manco Cápac y Huayna Cápac',
                                  'Manco Cápac y Sinchi Roca'],
                 'correcta': 'E'},
                {'pregunta': 'Lloque Yupanqui y Mayta Cápac corresponden al '
                             'periodo: (UNSAAC 2016)',
                 'alternativas': ['Legendario o de los comienzos del Incario',
                                  'Regional o de la Confederación cusqueña',
                                  'De la resistencia de Vilcabamba',
                                  'De la decadencia o crisis',
                                  'De la expansión y el apogeo'],
                 'correcta': 'A'},
                {'pregunta': 'El Ayllu, que fue la unidad básica de la '
                             'organización Inca, surgió: (UNSAAC 2016)',
                 'alternativas': ['En el periodo de los Chancas',
                                  'Antes de los Incas',
                                  'Durante el gobierno de los Incas',
                                  'Después de los Incas',
                                  'En el gobierno de Pachacútec'],
                 'correcta': 'B'},
                {'pregunta': 'En la organización administrativa del Incario, '
                             'el Pisqa Chunca Camayoc era el jefe de: '
                             '(UNSAAC 2016)',
                 'alternativas': ['10 familias',
                                  '50 familias',
                                  '100 familias',
                                  '500 familias',
                                  '5 familias'],
                 'correcta': 'B'},
                {'pregunta': 'En el periodo de la confederación cusqueña o '
                             'quechua, los gobernantes se denominaron: '
                             '(UNSAAC 2016)',
                 'alternativas': ['Auqui',
                                  'Phiwichuris',
                                  'Curacas',
                                  'Sinchis',
                                  'Apunchic'],
                 'correcta': 'C'},
                {'pregunta': 'El príncipe heredero del trono en el incanato '
                             'se llamaba: (UNSAAC 2016)',
                 'alternativas': ['Tucuyricuy',
                                  'Qhapac',
                                  'Sinchi',
                                  'Apunchic',
                                  'Auqui'],
                 'correcta': 'E'},
                {'pregunta': 'Sacsayhuamán y Ollantaytambo corresponden '
                             'respectivamente a tipo de arquitectura: '
                             '(UNSAAC 2018)',
                 'alternativas': ['Militar - Civil',
                                  'Militar - Religioso',
                                  'Civil - Militar',
                                  'Religioso - Militar',
                                  'Civil - Religioso'],
                 'correcta': 'B'},
                {'pregunta': 'El Inca Pachacútec gobernó en el periodo '
                             'histórico: (UNSAAC 2018)',
                 'alternativas': ['Regional',
                                  'Legendario',
                                  'Imperial',
                                  'Inicial',
                                  'Curacal'],
                 'correcta': 'C'},
                {'pregunta': 'El gobernador de las provincias en la época '
                             'inca se denominaba: (UNSAAC 2018)',
                 'alternativas': ['Apunchic',
                                  'Sinchi',
                                  'Auqui',
                                  'Tucuyricuq',
                                  'Curaca'],
                 'correcta': 'A'},
                {'pregunta': 'El monumento arqueológico de Ollantaytambo fue '
                             'una construcción de tipo: (UNSAAC 2018)',
                 'alternativas': ['Civil',
                                  'Económico',
                                  'Militar',
                                  'Recreacional',
                                  'Religioso'],
                 'correcta': 'C'},
                {'pregunta': 'En la evolución histórica de los '
                             'Incas-quechuas, el periodo legendario de los '
                             'comienzos o curacal fue gobernado por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Lloque Yupanqui y Mayta Cápac',
                                  'Inca Roca y Wiracocha',
                                  'Manco Cápac y Sinchi Roca',
                                  'Cápac Yupanqui y Huayna Cápac',
                                  'Pachacútec y Túpac Inca Yupanqui'],
                 'correcta': 'C'},
                {'pregunta': 'El capital en la época incaica lo constituía: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['El almacenamiento de productos',
                                  'La técnica para deshidratar la papa',
                                  'La producción de la tierra',
                                  'La redistribución de los depósitos',
                                  'La fuerza humana de sus habitantes'],
                 'correcta': 'A'},
                {'pregunta': 'El inca que perteneció al periodo de la '
                             'Expansión y apogeo del Tahuantinsuyo es: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Tupac Inca Yupanqui',
                                  'Mayta Cápac',
                                  'Inca Roca',
                                  'Sinchi Roca',
                                  'Wiracocha'],
                 'correcta': 'A'},
                {'pregunta': 'El proceso histórico Inca, en el periodo de la '
                             'decadencia, se caracterizó por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['El ataque de los Chancas al Cusco',
                                  'La fundación de Qosqo con Manco Cápac y '
                                  'Mama Ocllo',
                                  'La resistencia de los incas desde '
                                  'Vilcabamba',
                                  'La guerra civil entre los hermanos '
                                  'Huáscar y Atahualpa',
                                  'La muerte de Huayna Cápac y Ninan Cuyuchi '
                                  'en el Ecuador'],
                 'correcta': 'D'},
                {'pregunta': 'Wiracocha gobernó en el periodo: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Decadente o de la descomposición',
                                  'Imperial o de la expansión política',
                                  'De resistencia y supervivencia',
                                  'Regional o de la confederación quechua',
                                  'Legendario o de los inicios'],
                 'correcta': 'D'},
                {'pregunta': 'El reconocimiento de un antepasado común por '
                             'los miembros del ayllu inca se refiere al '
                             'vínculo por: (UNSAAC Ordinario)',
                 'alternativas': ['Origen',
                                  'Tótem',
                                  'Religión',
                                  'Territorio',
                                  'Parentesco'],
                 'correcta': 'E'},
                {'pregunta': 'Uno de los incas de la resistencia, refugiado '
                             'en Vilcabamba, que finalmente reconoció al Rey '
                             'de España fue: (UNSAAC Ordinario)',
                 'alternativas': ['Tupac Amaru I',
                                  'Huáscar',
                                  'Manco Inca',
                                  'Sayri Tupac',
                                  'Huayna Cápac'],
                 'correcta': 'D'},
                {'pregunta': 'El periodo de la resistencia andina de '
                             'Vilcabamba culminó con la muerte de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Fernando Tupac Amaru',
                                  'Sayri Tupac',
                                  'Titu Cusi Yupanqui',
                                  'Felipe Tupac Amaru',
                                  'José Gabriel Tupac Amaru'],
                 'correcta': 'D'},
                {'pregunta': 'En el proceso histórico de los incas, Titu '
                             'Cusi Yupanqui gobernó el periodo: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Regional o de la Confederación Cusqueña',
                                  'Imperial o de la expansión',
                                  'De resistencia de Vilcabamba',
                                  'Legendario o de los orígenes',
                                  'Decadente o crítico'],
                 'correcta': 'C'},
                {'pregunta': 'En el incanato, el gobernante de las '
                             'provincias encargado de mantener el orden en '
                             'el interior del territorio fue el: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Cacique',
                                  'Consejo de Suyos',
                                  'Inca',
                                  'Apunchik',
                                  'Curaca'],
                 'correcta': 'D'},
                {'pregunta': 'El futuro gobernante del Tahuantinsuyo fue '
                             'conocido como: (UNSAAC Ordinario)',
                 'alternativas': ['Kipukamayoc',
                                  'Tucuy Ricuj',
                                  'Apuskipa',
                                  'Auqui',
                                  'Phiwichuri'],
                 'correcta': 'D'},
                {'pregunta': 'El Ayni, como sistema de trabajo en el '
                             'Tahuantinsuyo, consistía en: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['La prestación de servicios en forma '
                                  'recíproca entre las personas de un Ayllu',
                                  'El trabajo obligatorio para la '
                                  'construcción de obras públicas',
                                  'El trabajo gratuito en las tierras del '
                                  'curaca',
                                  'El trabajo obligatorio para la '
                                  'explotación de recursos',
                                  'La forma de trabajo de una comunidad en '
                                  'las tierras del Inca'],
                 'correcta': 'A'},
                {'pregunta': 'La derrota de los Chancas, en la batalla de '
                             'Yawarpampa, corresponde al periodo: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['De la resistencia',
                                  'De la expansión y Apogeo',
                                  'De la Decadencia',
                                  'Legendario',
                                  'De la confederación quechua'],
                 'correcta': 'B'},
                {'pregunta': 'En la resistencia de Manco Inca, el capitán '
                             'que se inmoló antes de caer en manos españolas '
                             'fue: (UNSAAC Ordinario)',
                 'alternativas': ['Tupac Huallpa',
                                  'Calcuchimac',
                                  'Quisquis',
                                  'Titu Yupanki',
                                  'Suruhuamán'],
                 'correcta': 'E'},
                {'pregunta': 'En el Tahuantinsuyo, la unidad de medida de '
                             'las tierras comunales del ayllu se denominaba: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Chala',
                                  'Trueque',
                                  'Topo',
                                  'Mita',
                                  'Marca'],
                 'correcta': 'C'},
                {'pregunta': 'En el Ayllu, reconocían una Pacarina común, '
                             'como vínculo: (UNSAAC Ordinario)',
                 'alternativas': ['Origen',
                                  'Parentesco',
                                  'Idioma',
                                  'Tótem',
                                  'Territorio'],
                 'correcta': 'A'},
                {'pregunta': 'En el Tahuantinsuyo, los ciudadanos obligados '
                             'a tributar fueron los: (UNSAAC Ordinario)',
                 'alternativas': ['Orejones',
                                  'Chasquis',
                                  'Mitmacunas',
                                  'Hatun Runas',
                                  'Curacas'],
                 'correcta': 'D'},
                {'pregunta': 'Para tener un mejor control de la población en '
                             'términos de cumplimiento de la Mita en el '
                             'Tahuantinsuyo, la división de 5000 familias '
                             'estaba controlado por: (UNSAAC Ordinario)',
                 'alternativas': ['Pisca Pachac Camayoc',
                                  'Pisca Camayoc',
                                  'Pisca Pachac Camayoc',
                                  'Pisca Huaranca Camayoc',
                                  'Pisca Chunca Camayoc'],
                 'correcta': 'D'},
                {'pregunta': 'El Ayllu fue la unidad esencial y básica de la '
                             'organización social inca, teniendo como '
                             'responsable al: (UNSAAC Ordinario)',
                 'alternativas': ['Sinchi',
                                  'Tucuy Ricuc',
                                  'Curaca',
                                  'Auqui',
                                  'Apunchic'],
                 'correcta': 'C'},
                {'pregunta': 'El urpu o aríbalo es la manifestación '
                             'ceramística más representativa de la Cultura: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Chavín',
                                  'Chimú',
                                  'Wari',
                                  'Inca',
                                  'Mochica'],
                 'correcta': 'D'},
                {'pregunta': 'En la Organización Política Inca, el Apunchic '
                             'representó: (UNSAAC Ordinario)',
                 'alternativas': ['Al príncipe heredero',
                                  'Al gobernador de las provincias',
                                  'A funcionarios incógnitos',
                                  'A los cuatro jefes de suyos',
                                  'A la máxima autoridad del Inca'],
                 'correcta': 'B'},
                {'pregunta': 'En la evolución histórica de los incas, el '
                             'periodo Legendario fue gobernado por: (II '
                             'CEPRU 2011)',
                 'alternativas': ['Pachacútec - Tupac Inca Yupanki',
                                  'Lloque Yupanki - Mayta Capac',
                                  'Manco Cápac - Sinchi Roca',
                                  'Huáscar - Atahuallpa',
                                  'Inca Roca - Wiracocha'],
                 'correcta': 'C'},
                {'pregunta': 'En la organización Social Inca, la nobleza de '
                             'sangre estuvo integrada por: (II CEPRU 2011)',
                 'alternativas': ['Los yanaconas o servidores domésticos',
                                  'Los Hatunrunas o miembros del Ayllu',
                                  'Los mitimaes o pueblos trasladados',
                                  'Ascendientes del inca y la coya',
                                  'Jefes incorporados de pueblos vencidos'],
                 'correcta': 'D'},
                {'pregunta': 'Las características más importantes de la '
                             'arquitectura inca fueron: (II CEPRU 2011)',
                 'alternativas': ['Simetría - ciclópea - asimétrica',
                                  'Administrativa - militar - polícroma',
                                  'Solidez - almohadillado - funcional',
                                  'Sencillez - funcional - administrativa',
                                  'Solidez - sencillez - simetría'],
                 'correcta': 'E'},
                {'pregunta': 'En el Ayllu, las relaciones de parentesco se '
                             'establecían a través del vínculo de: (II CEPRU '
                             '2012)',
                 'alternativas': ['Tótem',
                                  'Marka',
                                  'Economía',
                                  'Sangre',
                                  'Territorio'],
                 'correcta': 'D'},
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
                 'alternativas': ['Clase de pueblo',
                                  'Nobleza regional',
                                  'Clase de los militares',
                                  'Nobleza de sangre',
                                  'Nobleza de privilegio'],
                 'correcta': 'E'},
                {'pregunta': 'En la economía inca, la redistribución '
                             'significó: (I CEPRU 2014)',
                 'alternativas': ['La repartición anual de tierras por parte '
                                  'de la coya',
                                  'El disfrute, según las necesidades de '
                                  'cada uno',
                                  'La asignación de labores agrícolas por '
                                  'parte del inca',
                                  'El intercambio de productos por otros '
                                  'productos',
                                  'La repartición de alimentos excedentes en '
                                  'épocas de crisis'],
                 'correcta': 'E'},
                {'pregunta': 'La Leyenda de la fundación del Cusco por Manco '
                             'Cápac y Mama Ocllo, pertenece a la fuente: (I '
                             'CEPRU 2014)',
                 'alternativas': ['Escrita',
                                  'Material',
                                  'Oral',
                                  'Documental',
                                  'Antroposomática'],
                 'correcta': 'C'},
                {'pregunta': 'El vínculo del ayllu por el cual sus miembros '
                             'reconocían un lugar de origen común se llama '
                             'vínculo de:',
                 'alternativas': ['Territorio',
                                  'Idioma',
                                  'Pacarina u origen',
                                  'Religión',
                                  'Tótem'],
                 'correcta': 'C'},
                {'pregunta': 'Los prisioneros de guerra sometidos a '
                             'servidumbre perpetua en la sociedad inca se '
                             'llamaban:',
                 'alternativas': ['Mitimaes',
                                  'Yanacunas',
                                  'Hatun runas',
                                  'Curacas',
                                  'Auquis'],
                 'correcta': 'B'},
                {'pregunta': 'Los mitimaes trasladados a tierras despobladas '
                             'para poblarlas e integrarlas a la economía se '
                             'llamaban mitimaes de:',
                 'alternativas': ['Frontera',
                                  'Castigo',
                                  'Colonización',
                                  'Conquista',
                                  'Guerra'],
                 'correcta': 'C'},
                {'pregunta': 'El Estado Inca, de tipo hereditario, '
                             'teocrático y militarista, era una monarquía:',
                 'alternativas': ['Constitucional',
                                  'Confederada',
                                  'Absolutista',
                                  'Federal',
                                  'Parlamentaria'],
                 'correcta': 'C'},
                {'pregunta': 'El funcionario inca considerado «el que todo '
                             'lo ve», que supervisaba política, militar y '
                             'económicamente el Tahuantinsuyo, era el:',
                 'alternativas': ['Tukuy Rikuq',
                                  'Auqui',
                                  'Curaca',
                                  'Apunchic',
                                  'Sinchi'],
                 'correcta': 'A'},
                {'pregunta': 'El gobernante de las provincias o guamaníes, '
                             'que representaba la autoridad del Qhapaq, era '
                             'el:',
                 'alternativas': ['Curaca',
                                  'Auqui',
                                  'Apunchic',
                                  'Tukuy Rikuq',
                                  'Sinchi'],
                 'correcta': 'C'},
                {'pregunta': 'El idioma oficial establecido en todo el '
                             'Tahuantinsuyo fue el:',
                 'alternativas': ['Runa Simi o quechua',
                                  'Puquina',
                                  'Culle',
                                  'Aimara',
                                  'Mochica'],
                 'correcta': 'A'},
                {'pregunta': 'La red de caminos que aseguraba las '
                             'comunicaciones en todo el Tahuantinsuyo se '
                             'llamó:',
                 'alternativas': ['Chaski Ñan',
                                  'Qhapac Ñan',
                                  'Tawa Ñan',
                                  'Suyu Ñan',
                                  'Inca Ñan'],
                 'correcta': 'B'},
                {'pregunta': 'En el sistema decimal inca, el jefe de 10 000 '
                             'familias era llamado:',
                 'alternativas': ['Pachac Camayoc',
                                  'Huno Camayoc',
                                  'Chunca Camayoc',
                                  'Piscca Camayoc',
                                  'Suyuyuc Apu'],
                 'correcta': 'B'},
                {'pregunta': 'La forma de trabajo inca de carácter '
                             'colectivo, de ayuda mutua entre familias del '
                             'ayllu, se llamaba:',
                 'alternativas': ['Chunka',
                                  'Reciprocidad estatal',
                                  'Minka',
                                  'Ayni',
                                  'Mita'],
                 'correcta': 'D'},
                {'pregunta': 'La forma de trabajo inca de carácter '
                             'obligatorio y rotativo, en beneficio del '
                             'Estado, se llamaba:',
                 'alternativas': ['Minka',
                                  'Mita',
                                  'Chunka',
                                  'Redistribución',
                                  'Ayni'],
                 'correcta': 'B'},
                {'pregunta': 'La forma de trabajo inca limitado o comunal '
                             'para obras de interés colectivo se llamaba:',
                 'alternativas': ['Ayllu', 'Chunka', 'Ayni', 'Mita', 'Minka'],
                 'correcta': 'E'},
                {'pregunta': 'El sistema por el cual el Inca hacía llegar a '
                             'los ayllus beneficios como ropa y '
                             'herramientas, a cambio de mano de obra, se '
                             'llamaba:',
                 'alternativas': ['Consumo',
                                  'Circulación',
                                  'Trueque',
                                  'Redistribución',
                                  'Producción'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'EL AYLLU: LOS SIETE VÍNCULOS',
                      'items': ['El ayllu fue la unidad esencial de la '
                                'organización social inca, con jefe llamado '
                                'curaca.',
                                'Vínculo de territorio: los miembros del '
                                'ayllu compartían un mismo espacio '
                                'geográfico llamado marka.',
                                'Vínculo de economía: trabajaban '
                                'colectivamente las tierras de todos.',
                                'Vínculo de tótem: reconocían un antepasado '
                                'común sacralizado; vínculo de origen: '
                                'reconocían una Pacarina común.']},
                     {'titulo': 'LO SOCIAL: ETNIAS Y CLASES',
                      'items': ['La sociedad inca fue multiétnica: incluía '
                                'collas y lupacas (altiplano), chinchas '
                                '(costa sur), chancas (Apurímac) y huancas '
                                '(Junín).',
                                'La nobleza de sangre descendía del Qhapaq y '
                                'la Qoya; la nobleza por privilegio ascendía '
                                'por méritos.',
                                'Los hatun runas eran los ciudadanos del '
                                'Tahuantinsuyo en pleno ejercicio de sus '
                                'obligaciones.',
                                'Los yanacunas eran prisioneros de guerra '
                                'sometidos a servidumbre perpetua, condición '
                                'heredable.',
                                'Los mitimaes eran de tres clases: de '
                                'conquista, de colonización, y de castigo '
                                'por rebeldía.']},
                     {'titulo': 'ESTRUCTURA POLÍTICA DEL ESTADO INCA',
                      'items': ['El Estado Inca fue una monarquía '
                                'absolutista, teocrática, militarista, '
                                'hereditaria y centralista.',
                                'El Qhapaq (Inca) era la máxima autoridad, '
                                'considerado hijo del Sol; el trono se '
                                'heredaba de padre a hijo.',
                                'El Consejo de Suyos (Suyuyuc Apu) estaba '
                                'conformado por los cuatro jefes de suyo.',
                                'El Apunchic era el gobernante de las '
                                'provincias o guamaníes, representando al '
                                'Qhapaq.',
                                'El Tukuy Rikuq, «el que todo lo ve», '
                                'supervisaba política, militar y '
                                'económicamente el Tahuantinsuyo.',
                                'El Sinchi era el jefe militar, con función '
                                'principal en tiempos de guerra.']},
                     {'titulo': 'ORGANIZACIÓN ADMINISTRATIVA: SISTEMA '
                                'DECIMAL',
                      'items': ['El idioma oficial del Tahuantinsuyo fue el '
                                'Runa Simi o quechua.',
                                'La red de caminos que unía el Tahuantinsuyo '
                                'se llamó Qhapac Ñan.',
                                'El sistema de contabilidad y registro '
                                'estatal se realizaba mediante los quipus.',
                                'La población se organizó bajo el sistema '
                                'decimal: Purej (jefe de familia), Pisca '
                                'Camayoc (5 familias), Chunca Camayoc (10 '
                                'familias).',
                                'El Huno Camayoc era jefe de 10 000 '
                                'familias; el Suyuyuc Apu, jefe de un '
                                'suyo.']},
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
                                'costa.']},
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
                     {'titulo': 'LAS FORMAS DE TRABAJO INCA',
                      'items': ['El ayni era una forma de trabajo colectivo, '
                                'de ayuda mutua entre familias del ayllu.',
                                'La mita era una forma de trabajo '
                                'obligatorio, rotativo, en beneficio del '
                                'Estado.',
                                'El minka era una forma de trabajo limitado '
                                'o comunal para obras de interés colectivo.',
                                'El chunka era una forma de trabajo '
                                'equitativo, general y alternable.',
                                'La redistribución era el sistema por el '
                                'cual el Inca hacía llegar a los ayllus '
                                'beneficios como ropa y herramientas.']},
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
                 'alternativas': ['IX y XV',
                                  'V y VIII',
                                  'III y VI',
                                  'XV y XVIII',
                                  'XVI y XVIII'],
                 'correcta': 'A'},
                {'pregunta': 'La base fundamental del sistema feudal fue:',
                 'alternativas': ['La industria textil',
                                  'La posesión de la tierra',
                                  'La banca',
                                  'La minería',
                                  'El comercio marítimo'],
                 'correcta': 'B'},
                {'pregunta': 'El feudalismo surgió principalmente tras:',
                 'alternativas': ['Las Cruzadas',
                                  'La caída del Imperio Romano de Occidente '
                                  'y las invasiones bárbaras',
                                  'La Revolución Francesa',
                                  'El descubrimiento de América',
                                  'La peste negra'],
                 'correcta': 'B'},
                {'pregunta': 'La economía feudal se caracterizó por ser:',
                 'alternativas': ['Comercial y monetaria',
                                  'Industrial y urbana',
                                  'Rural y autosuficiente',
                                  'Colonial',
                                  'Financiera'],
                 'correcta': 'C'},
                {'pregunta': 'El campesino adscrito a la tierra, que no '
                             'podía abandonarla, era el:',
                 'alternativas': ['Siervo de la gleba',
                                  'Vasallo',
                                  'Artesano',
                                  'Burgués',
                                  'Caballero'],
                 'correcta': 'A'},
                {'pregunta': 'El acto por el cual el vasallo juraba '
                             'fidelidad al señor se llamaba:',
                 'alternativas': ['Diezmo',
                                  'Investidura',
                                  'Censo',
                                  'Homenaje',
                                  'Tributo'],
                 'correcta': 'D'},
                {'pregunta': 'La extensión de tierra entregada a cambio de '
                             'servicios se denominaba:',
                 'alternativas': ['Manso',
                                  'Solar',
                                  'Feudo',
                                  'Villa',
                                  'Burgo'],
                 'correcta': 'C'},
                {'pregunta': 'El poder político durante el feudalismo se '
                             'caracterizó por estar:',
                 'alternativas': ['Concentrado en las ciudades',
                                  'Centralizado',
                                  'Fragmentado o descentralizado',
                                  'Bajo control imperial único',
                                  'En manos del pueblo'],
                 'correcta': 'C'},
                {'pregunta': 'La nueva clase social surgida con el renacer '
                             'del comercio y las ciudades fue:',
                 'alternativas': ['El clero',
                                  'La burguesía',
                                  'La nobleza',
                                  'Los siervos',
                                  'Los caballeros'],
                 'correcta': 'B'},
                {'pregunta': 'La sociedad feudal se caracterizó por ser:',
                 'alternativas': ['Estamental y rígida',
                                  'Democrática',
                                  'De alta movilidad social',
                                  'Sin clases',
                                  'Igualitaria'],
                 'correcta': 'A'},
                {'pregunta': 'El movimiento cultural que recuperó la cultura '
                             'grecolatina fue:',
                 'alternativas': ['La Ilustración',
                                  'La Escolástica',
                                  'El Barroco',
                                  'El Romanticismo',
                                  'El Renacimiento'],
                 'correcta': 'E'},
                {'pregunta': 'La corriente que colocó al ser humano en el '
                             'centro del pensamiento fue:',
                 'alternativas': ['El humanismo',
                                  'El escolasticismo',
                                  'El teocentrismo',
                                  'El empirismo',
                                  'El positivismo'],
                 'correcta': 'A'},
                {'pregunta': 'El capitalismo mercantil se basó '
                             'principalmente en:',
                 'alternativas': ['El trueque',
                                  'La servidumbre',
                                  'La agricultura de subsistencia',
                                  'La producción artesanal doméstica',
                                  'El comercio, la banca y la acumulación de '
                                  'capital'],
                 'correcta': 'E'},
                {'pregunta': 'La función social de la nobleza feudal era:',
                 'alternativas': ['Orar',
                                  'Trabajar la tierra',
                                  'Guerrear y proteger',
                                  'Administrar justicia eclesiástica',
                                  'Comerciar'],
                 'correcta': 'C'},
                {'pregunta': 'La función social del clero en la sociedad '
                             'feudal era:',
                 'alternativas': ['Gobernar el feudo',
                                  'Recaudar impuestos',
                                  'Guerrear',
                                  'Orar y administrar lo religioso',
                                  'Trabajar la tierra'],
                 'correcta': 'D'},
                {'pregunta': 'El señor feudal otorgaba a sus vasallos '
                             'principalmente:',
                 'alternativas': ['Educación',
                                  'Dinero',
                                  'Títulos nobiliarios exclusivamente',
                                  'Naves comerciales',
                                  'Protección y tierras'],
                 'correcta': 'E'},
                {'pregunta': 'Las parcelas del feudo trabajadas por los '
                             'campesinos se llamaban:',
                 'alternativas': ['Villas',
                                  'Mansos',
                                  'Ejidos',
                                  'Burgos',
                                  'Reserva señorial'],
                 'correcta': 'B'},
                {'pregunta': 'El feudalismo fue un sistema:',
                 'alternativas': ['Exclusivamente religioso',
                                  'Solo jurídico',
                                  'Únicamente militar',
                                  'Político, económico y social',
                                  'Solo económico'],
                 'correcta': 'D'},
                {'pregunta': 'La burguesía estuvo formada principalmente '
                             'por:',
                 'alternativas': ['Siervos de la gleba',
                                  'Nobles y caballeros',
                                  'Militares',
                                  'Comerciantes y artesanos',
                                  'Clero regular'],
                 'correcta': 'D'},
                {'pregunta': 'El renacer de las ciudades en la Baja Edad '
                             'Media se relaciona directamente con:',
                 'alternativas': ['La expansión de la servidumbre',
                                  'El aislamiento de los feudos',
                                  'El fin del comercio',
                                  'La reactivación del comercio',
                                  'Las invasiones bárbaras'],
                 'correcta': 'D'},
                {'pregunta': 'El origen de la burguesía se remonta al siglo '
                             'XII, con villanos que residían en:',
                 'alternativas': ['Los burgos o ciudades',
                                  'Las cortes reales',
                                  'Los monasterios',
                                  'Los feudos',
                                  'Los castillos'],
                 'correcta': 'A'},
                {'pregunta': 'La actividad comercial de los burgueses no era '
                             'bien vista por:',
                 'alternativas': ['La Iglesia',
                                  'Los reyes',
                                  'Los campesinos',
                                  'Los artesanos',
                                  'Los mercaderes'],
                 'correcta': 'A'},
                {'pregunta': 'Los permisos de autogobierno que obtenían los '
                             'burgueses se escribían en documentos llamados:',
                 'alternativas': ['Códigos civiles',
                                  'Cartas de franquicia',
                                  'Bulas papales',
                                  'Tratados de paz',
                                  'Decretos reales'],
                 'correcta': 'B'},
                {'pregunta': 'El capitalismo mercantil se basaba en la '
                             'premisa de que la riqueza de una nación '
                             'aumentaba al exportar más y recibir:',
                 'alternativas': ['Tierras',
                                  'Armas',
                                  'Esclavos',
                                  'Metales preciosos',
                                  'Alimentos exclusivamente'],
                 'correcta': 'D'},
                {'pregunta': 'Bajo el capitalismo mercantil, el control '
                             'sobre la vida económica lo ejercía '
                             'principalmente:',
                 'alternativas': ['El Estado',
                                  'La Iglesia',
                                  'Los gremios exclusivamente',
                                  'Los burgueses exclusivamente',
                                  'Los campesinos'],
                 'correcta': 'A'},
                {'pregunta': 'El capitalismo mercantil impulsó los viajes de '
                             'descubrimiento e invasión sobre América y:',
                 'alternativas': ['Ninguna otra región',
                                  'El Ártico',
                                  'La Antártida',
                                  'África',
                                  'Oceanía'],
                 'correcta': 'D'},
                {'pregunta': 'El Renacimiento sustituyó la concepción '
                             'teocentrista medieval por:',
                 'alternativas': ['El mercantilismo',
                                  'El escolasticismo',
                                  'El antropocentrismo',
                                  'El absolutismo',
                                  'El feudalismo'],
                 'correcta': 'C'},
                {'pregunta': 'La huida de eruditos bizantinos a Occidente se '
                             'debió a la captura de Constantinopla por los '
                             'turcos en:',
                 'alternativas': ['1453', '1600', '1517', '1400', '1492'],
                 'correcta': 'A'},
                {'pregunta': 'El autor de «El Príncipe», considerado padre '
                             'de la ciencia política, fue:',
                 'alternativas': ['Botticelli',
                                  'Tomás Moro',
                                  'Miguel Ángel',
                                  'Nicolás Maquiavelo',
                                  'Leonardo Da Vinci'],
                 'correcta': 'D'},
                {'pregunta': 'El autor de «Utopía», que idealizó una '
                             'república con propiedad común de los bienes, '
                             'fue:',
                 'alternativas': ['Da Vinci',
                                  'Tomás Moro',
                                  'Miguel Ángel',
                                  'Maquiavelo',
                                  'Botticelli'],
                 'correcta': 'B'},
                {'pregunta': 'Leonardo Da Vinci destacó por pinturas como la '
                             'Gioconda y el dibujo:',
                 'alternativas': ['El Hombre de Vitruvio',
                                  'David',
                                  'El Juicio Final',
                                  'El Nacimiento de Venus',
                                  'La Piedad'],
                 'correcta': 'A'},
                {'pregunta': 'Miguel Ángel destacó por esculturas como '
                             'David, Moisés y:',
                 'alternativas': ['La Piedad',
                                  'El Hombre de Vitruvio',
                                  'El Nacimiento de Venus',
                                  'La Gioconda',
                                  'La Primavera'],
                 'correcta': 'A'},
                {'pregunta': 'El sistema económico, social y político de la '
                             'Edad Media, basado en la gran propiedad '
                             'territorial, tuvo como elementos básicos al: '
                             '(UNSAAC 2013)',
                 'alternativas': ['Latifundista, colono y hacienda',
                                  'Señor feudal, vasallo y feudo',
                                  'Terrateniente, esclavo y beneficio',
                                  'Hacendado, siervo y latifundio',
                                  'Propietario, trabajador y parcela'],
                 'correcta': 'B'},
                {'pregunta': 'La burguesía, como una nueva clase social en '
                             'el mundo, surgió en la Europa: (UNSAAC 2013)',
                 'alternativas': ['Contemporánea industrial',
                                  'Moderna comercial',
                                  'Medieval Temprana',
                                  'Medieval Tardía',
                                  'Medieval Media'],
                 'correcta': 'E'},
                {'pregunta': 'Los elementos del feudalismo son: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Señor Feudal - Siervos - Repartimientos',
                                  'Encomienda - Siervos - Latifundios',
                                  'Burgos - Villanos - Hacendados',
                                  'Señor Feudal - Feudo - Siervo',
                                  'Feudo - Hacienda - Villanos'],
                 'correcta': 'D'},
                {'pregunta': 'La nueva clase social que surgió en Europa en '
                             'el Siglo XII fue de los: (UNSAAC Ordinario)',
                 'alternativas': ['Nobles',
                                  'Esclavos',
                                  'Burgueses',
                                  'Siervos',
                                  'Señores'],
                 'correcta': 'C'},
                {'pregunta': 'Uno de los elementos característicos del '
                             'feudalismo fue: (UNSAAC Ordinario)',
                 'alternativas': ['El ateísmo',
                                  'La industria',
                                  'La democracia',
                                  'La medicina',
                                  'La tierra'],
                 'correcta': 'E'},
                {'pregunta': 'Los miembros de la burguesía medieval tenían '
                             'como principal actividad: (UNSAAC Ordinario)',
                 'alternativas': ['El comercio',
                                  'La minería',
                                  'La política',
                                  'La ganadería',
                                  'La agricultura'],
                 'correcta': 'A'},
                {'pregunta': 'El acto por el cual un vasallo adquiría '
                             'derechos sobre el feudo se llamaba: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Inquisición',
                                  'Sumisión',
                                  'Vasallaje - Investidura',
                                  'Franquicia',
                                  'Vestidura'],
                 'correcta': 'C'},
                {'pregunta': 'En el medioevo medio, el sistema que tuvo '
                             'origen en el declive romano se denomina: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Feudalismo',
                                  'Socialismo',
                                  'Capitalismo',
                                  'Burguesía',
                                  'Primitivismo'],
                 'correcta': 'A'},
                {'pregunta': 'La base principal del sistema feudal fue: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['El siervo',
                                  'El dinero',
                                  'El comercio',
                                  'El esclavo',
                                  'La tierra'],
                 'correcta': 'E'},
                {'pregunta': 'La autorización o concesión que otorgaba el '
                             'rey a los burgueses para su autogobierno, se '
                             'denomina: (UNSAAC Ordinario)',
                 'alternativas': ['Reforma jurídica',
                                  'Concordato',
                                  'Bula alejandrina',
                                  'Regio patronato',
                                  'Carta de Franquicia'],
                 'correcta': 'E'},
                {'pregunta': 'En el medioevo, surgió una nueva clase social '
                             'dedicada a la actividad de comercio en las '
                             'ciudades, denominadas: (II CEPRU 2012)',
                 'alternativas': ['Proletario',
                                  'Villanos',
                                  'Burguesía',
                                  'Clase media',
                                  'Siervos'],
                 'correcta': 'C'},
                {'pregunta': 'El feudalismo, fue un sistema económico, '
                             'social y político que rigió durante la edad: '
                             '(I CEPRU 2014)',
                 'alternativas': ['Moderna',
                                  'Contemporánea',
                                  'Media',
                                  'Primitiva',
                                  'Antigua'],
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
  'secciones': [{'titulo': '9.1 CONTEXTO DE LOS DESCUBRIMIENTOS GEOGRÁFICOS',
                 'items': ['La toma de {Constantinopla} por los turcos en '
                           '1453 impulsó la búsqueda de nuevas rutas '
                           'comerciales hacia las Indias.',
                           'Los navegantes {portugueses} llegaron a las '
                           'Indias bordeando África: {Vasco de Gama} en '
                           '1499.',
                           'Los españoles siguieron la ruta del oeste, '
                           'atravesando el Atlántico: {Cristóbal Colón} en '
                           '1492.']},
                {'titulo': '9.2 CRISTÓBAL COLÓN: FORMACIÓN Y PROYECTO',
                 'items': ['{Cristóbal Colón} nació en el puerto italiano de '
                           '{Génova} en 1451.',
                           'Su proyecto se inspiró en el «Imago Mundi», las '
                           'cartas de Paolo de {Toscanelli}, y la tesis de '
                           'Ptolomeo sobre la redondez de la Tierra.',
                           'El proyecto de Colón fue desechado por los '
                           'sabios de la Universidad de {Salamanca}, y '
                           'rechazado por el rey Juan II de Portugal.',
                           'Colón recibió apoyo en el convento de {La '
                           'Rábida}, de los religiosos Juan Pérez y Antonio '
                           'Marchena.']},
                {'titulo': '9.3 LA CAPITULACIÓN DE SANTA FE (1492)',
                 'items': ['La {Capitulación de Santa Fe} se firmó el 17 de '
                           'abril de 1492, entre la reina Isabel, Juan Pérez '
                           'y Colón.',
                           'Se concedió a Colón los títulos de {Almirante}, '
                           'Virrey y Gobernador de las tierras que '
                           'encontrara.',
                           'Colón tendría derecho a la {décima parte} de las '
                           'riquezas, y se le otorgó el título de Don.',
                           'El {puerto de Palos} se fijó como lugar de los '
                           'preparativos del viaje.',
                           'Los verdaderos financistas fueron los hermanos '
                           '{Pinzón} y el judío portugués Luis de '
                           'Santángel.']},
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
                 'alternativas': ['1492', '1521', '1453', '1498', '1532'],
                 'correcta': 'C'},
                {'pregunta': 'El documento que fijó los títulos y beneficios '
                             'de Colón fue:',
                 'alternativas': ['La Bula Inter Caetera',
                                  'Las Leyes de Burgos',
                                  'El Requerimiento',
                                  'La Capitulación de Santa Fe',
                                  'El Tratado de Tordesillas'],
                 'correcta': 'D'},
                {'pregunta': 'La Capitulación de Santa Fe se firmó en el '
                             'año:',
                 'alternativas': ['1492', '1453', '1494', '1498', '1502'],
                 'correcta': 'A'},
                {'pregunta': 'Colón zarpó en su primer viaje desde el puerto '
                             'de:',
                 'alternativas': ['Palos',
                                  'Cádiz',
                                  'Sevilla',
                                  'Sanlúcar',
                                  'Lisboa'],
                 'correcta': 'A'},
                {'pregunta': 'La primera isla a la que llegó Colón fue:',
                 'alternativas': ['Jamaica',
                                  'Trinidad',
                                  'Guanahaní',
                                  'Cuba',
                                  'La Española'],
                 'correcta': 'C'},
                {'pregunta': 'Las naves del primer viaje de Colón fueron:',
                 'alternativas': ['Santiago, San Antonio y Victoria',
                                  'Victoria, Trinidad y Concepción',
                                  'Pinta, Niña y Santa María',
                                  'Nao, Carabela y Galeón',
                                  'La Isabela, La Gallega y La Niña'],
                 'correcta': 'C'},
                {'pregunta': 'Colón sostenía, para justificar su proyecto, '
                             'la:',
                 'alternativas': ['Cercanía de África',
                                  'Planitud del mundo',
                                  'Ruta del Cabo de Buena Esperanza',
                                  'Esfericidad de la Tierra',
                                  'Existencia de un continente intermedio'],
                 'correcta': 'D'},
                {'pregunta': 'Los Reyes Católicos que apoyaron a Colón '
                             'fueron:',
                 'alternativas': ['Isabel de Castilla y Fernando de Aragón',
                                  'Felipe II y María',
                                  'Carlos I y Juana',
                                  'Carlos V e Isabel de Portugal',
                                  'Juan II y Beatriz'],
                 'correcta': 'A'},
                {'pregunta': 'En su tercer viaje, Colón llegó a la '
                             'desembocadura del río:',
                 'alternativas': ['Orinoco',
                                  'Amazonas',
                                  'Paraná',
                                  'Misisipi',
                                  'Magdalena'],
                 'correcta': 'A'},
                {'pregunta': 'El título que recibió Colón según la '
                             'Capitulación fue:',
                 'alternativas': ['Almirante, virrey y gobernador',
                                  'Capitán general',
                                  'Encomendero',
                                  'Corregidor',
                                  'Adelantado'],
                 'correcta': 'A'},
                {'pregunta': 'Instrumento náutico fundamental para la '
                             'orientación en alta mar:',
                 'alternativas': ['El sextante moderno',
                                  'El barómetro',
                                  'El telescopio',
                                  'El cronómetro',
                                  'La brújula'],
                 'correcta': 'E'},
                {'pregunta': 'En su segundo viaje, Colón fundó:',
                 'alternativas': ['La Isabela',
                                  'Santo Domingo',
                                  'La Navidad',
                                  'Veracruz',
                                  'Panamá'],
                 'correcta': 'A'},
                {'pregunta': 'El cuarto viaje de Colón se realizó en:',
                 'alternativas': ['1519', '1492', '1502', '1493', '1498'],
                 'correcta': 'C'},
                {'pregunta': 'Los países que encabezaron la expansión '
                             'ultramarina europea fueron:',
                 'alternativas': ['Inglaterra y Francia',
                                  'Francia y España',
                                  'Holanda e Italia',
                                  'Alemania y Suecia',
                                  'Portugal y España'],
                 'correcta': 'E'},
                {'pregunta': 'Colón llamó a la isla de Guanahaní:',
                 'alternativas': ['Juana',
                                  'Trinidad',
                                  'San Salvador',
                                  'La Española',
                                  'La Isabela'],
                 'correcta': 'C'},
                {'pregunta': 'La causa económica principal de los '
                             'descubrimientos geográficos fue:',
                 'alternativas': ['La búsqueda de una nueva ruta a las '
                                  'Indias',
                                  'El exceso de población',
                                  'La expansión del feudalismo',
                                  'La escasez de tierras agrícolas',
                                  'La difusión del cristianismo únicamente'],
                 'correcta': 'A'},
                {'pregunta': 'El astrolabio servía para:',
                 'alternativas': ['Medir la temperatura',
                                  'Orientar el timón',
                                  'Calcular la velocidad',
                                  'Determinar la latitud mediante los astros',
                                  'Medir la profundidad del mar'],
                 'correcta': 'D'},
                {'pregunta': 'La embarcación ligera y maniobrable usada en '
                             'los viajes de exploración fue:',
                 'alternativas': ['La carabela',
                                  'La goleta',
                                  'El galeón',
                                  'La fragata',
                                  'El bergantín'],
                 'correcta': 'A'},
                {'pregunta': 'El primer viaje de Colón se realizó en el año:',
                 'alternativas': ['1493', '1502', '1453', '1498', '1492'],
                 'correcta': 'E'},
                {'pregunta': 'En su cuarto viaje, Colón recorrió '
                             'principalmente:',
                 'alternativas': ['El Río de la Plata',
                                  'Las costas de América Central',
                                  'La costa de Brasil',
                                  'La costa del Pacífico',
                                  'Las Antillas Mayores'],
                 'correcta': 'B'},
                {'pregunta': 'El nombre «América» proviene del navegante '
                             'italiano:',
                 'alternativas': ['Cristóbal Colón',
                                  'Vasco da Gama',
                                  'Hernán Cortés',
                                  'Fernando de Magallanes',
                                  'Américo Vespucio'],
                 'correcta': 'E'},
                {'pregunta': 'El navegante portugués que llegó a la India '
                             'bordeando las costas de África en 1499 fue:',
                 'alternativas': ['Fernando de Magallanes',
                                  'Américo Vespucio',
                                  'Enrique el Navegante',
                                  'Vasco de Gama',
                                  'Cristóbal Colón'],
                 'correcta': 'D'},
                {'pregunta': 'Cristóbal Colón, en su primer viaje a América, '
                             'bautizó con el nombre de Juana a la isla de: '
                             '(UNSAAC 2018)',
                 'alternativas': ['Cuba',
                                  'Haití',
                                  'Trinidad',
                                  'Guanahaní',
                                  'Jamaica'],
                 'correcta': 'A'},
                {'pregunta': 'El acontecimiento que caracteriza al cuarto '
                             'viaje de Cristóbal Colón es: (UNSAAC 2022)',
                 'alternativas': ['El descubrimiento de las costas de '
                                  'Honduras, Nicaragua y de Panamá',
                                  'La llegada a la Isla Guanahaní llamándola '
                                  'San Salvador',
                                  'La llegada a la isla Martinica y Dominica',
                                  'La fundación de la primera ciudad '
                                  'denominada Isabela',
                                  'El arribo de 17 carabelas y 1500 hombres'],
                 'correcta': 'A'},
                {'pregunta': 'En los enfrentamientos de la resistencia, en '
                             'la batalla de Sacsayhuamán en 1536, destacó el '
                             'valeroso capitán: (UNSAAC 2022)',
                 'alternativas': ['Manco Inca',
                                  'Sayri Túpac',
                                  'Titu Yupanqui',
                                  'Suruhuamán',
                                  'Huayna Cápac'],
                 'correcta': 'D'},
                {'pregunta': 'Cristóbal Colón, en su segundo viaje, salió '
                             'del puerto de: (UNSAAC Ordinario)',
                 'alternativas': ['Valladolid',
                                  'Palos',
                                  'Cádiz',
                                  'San Lucar',
                                  'Trinidad'],
                 'correcta': 'C'},
                {'pregunta': 'Francisco Pizarro descubrió el Tahuantinsuyo, '
                             'en el: (UNSAAC Ordinario)',
                 'alternativas': ['Tercer viaje',
                                  'Primer viaje',
                                  'Quinto viaje',
                                  'Cuarto viaje',
                                  'Segundo viaje'],
                 'correcta': 'E'},
                {'pregunta': 'Cristóbal Colón descubrió Panamá en el: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Cuarto viaje',
                                  'Primer viaje',
                                  'Tercer viaje',
                                  'Quinto viaje',
                                  'Segundo viaje'],
                 'correcta': 'A'},
                {'pregunta': 'En el convento franciscano de la Rábida '
                             '(España), la empresa de Cristóbal Colón '
                             'encontró el apoyo del religioso: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Bartolomé de las Casas',
                                  'Juan Pérez',
                                  'Hernando de Luque',
                                  'Vicente de Valverde',
                                  'Joseph de Acosta'],
                 'correcta': 'B'},
                {'pregunta': 'Por la Capitulación de Santa Fe, Cristóbal '
                             'Colón tendría derecho a: (UNSAAC Ordinario)',
                 'alternativas': ['El título de adelantado',
                                  'La mitad de oro de las indias',
                                  'La décima parte de las riquezas',
                                  'Ser gobernador de España',
                                  'Fundar la ciudad de Panamá'],
                 'correcta': 'C'},
                {'pregunta': 'En su tercer viaje, Francisco Pizarro: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Se limitó a explorar las costas del norte '
                                  'peruano',
                                  'Llegó hasta la desembocadura del río '
                                  'Santa',
                                  'Protagonizó el incidente de los trece del '
                                  'gallo',
                                  'Descubrió el gran Mar del Sur',
                                  'Fundó la primera ciudad española en el '
                                  'Perú'],
                 'correcta': 'E'},
                {'pregunta': 'Por sus efectos, la tercera expedición de '
                             'Francisco Pizarro al Perú se conoce como '
                             'viaje: (UNSAAC Ordinario)',
                 'alternativas': ['Experimental',
                                  'Pionero',
                                  'Exploración',
                                  'Descubridor',
                                  'Invasor'],
                 'correcta': 'E'},
                {'pregunta': 'La primera ciudad fundada en América por '
                             'Cristóbal Colón fue: (UNSAAC Ordinario)',
                 'alternativas': ['Juana',
                                  'La Habana',
                                  'La Dominica',
                                  'Panamá',
                                  'La Isabela'],
                 'correcta': 'E'},
                {'pregunta': 'En su segundo viaje, Cristóbal Colón, en 1493, '
                             'llegó a las islas de: (UNSAAC Ordinario)',
                 'alternativas': ['Las Antillas - Puerto Rico y Jamaica',
                                  'Canarias y las Antillas',
                                  'Guanahaní - Cuba y Martinica',
                                  'Canarias y Trinidad',
                                  'Haití - Trinidad - Tobago'],
                 'correcta': 'A'},
                {'pregunta': 'La Reina Isabel de Castilla accedió a la '
                             'aprobación del Proyecto Colombino, debido a: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Los aportes geográficos y mapas de '
                                  'Ptolomeo',
                                  'Los datos alcanzados por su suegro '
                                  'Nicolás de Perestrello',
                                  'La recomendación del rey Juan II de '
                                  'Portugal',
                                  'Los consejos de Pablo Toscanelli',
                                  'La influencia de los frailes Juan Pérez y '
                                  'Antonio Marchena'],
                 'correcta': 'E'},
                {'pregunta': 'El contrato mediante el cual se autorizó el '
                             'viaje de Cristóbal Colón, por la Corona '
                             'Española, se conoce como: (UNSAAC Ordinario)',
                 'alternativas': ['La Bula de Partición del Mundo',
                                  'El reparto de América por el Papa '
                                  'Alejandro VI',
                                  'El Tratado de Tordesillas',
                                  'La Capitulación de Toledo',
                                  'La Capitulación de Santa Fe'],
                 'correcta': 'E'},
                {'pregunta': 'Después del tercer viaje de Colón, el cuarto '
                             'viaje no llegó hasta: (UNSAAC Ordinario)',
                 'alternativas': ['Honduras',
                                  'Nicaragua',
                                  'Costa Rica',
                                  'México',
                                  'Panamá'],
                 'correcta': 'D'},
                {'pregunta': 'Cristóbal Colón realizó varios viajes de '
                             'descubrimiento; el cuarto y último viaje de '
                             'exploración, se caracterizó por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Haber recorrido por las costas de la '
                                  'actual Honduras, Nicaragua y Panamá',
                                  'Arribar a las islas de Trinidad y la '
                                  'desembocadura del río Orinoco de '
                                  'Venezuela',
                                  'La llegada a las islas de Guanahaní y '
                                  'Cuba',
                                  'La fundación de la primera ciudad llamada '
                                  'Isabela en la española (Haití)',
                                  'La llegada a las pequeñas islas de '
                                  'Antillas y Puerto Rico'],
                 'correcta': 'A'},
                {'pregunta': 'En la capitulación de Santa Fe, la reina '
                             'Isabel de Castilla y Cristóbal Colón acordaron '
                             'realizar los preparativos para la expedición '
                             'en el puerto de: (UNSAAC Ordinario)',
                 'alternativas': ['Cádiz',
                                  'Palos',
                                  'Atacama',
                                  'Miraflores',
                                  'Barrameda'],
                 'correcta': 'B'},
                {'pregunta': 'Cristóbal Colón fundó la primera ciudad '
                             'española en América, bautizada con el nombre '
                             'de: (UNSAAC Ordinario)',
                 'alternativas': ['San Salvador',
                                  'Dominica',
                                  'Isabela',
                                  'Española',
                                  'Juana'],
                 'correcta': 'C'},
                {'pregunta': 'Cristóbal Colón llegó a América cuando en '
                             'España reinaba: (UNSAAC Ordinario)',
                 'alternativas': ['Fernando de Aragón',
                                  'Fernando VII',
                                  'Felipe II',
                                  'Carlos III',
                                  'Carlos V'],
                 'correcta': 'A'},
                {'pregunta': 'La primera ciudad fundada por Francisco '
                             'Pizarro en el Perú fue: (II CEPRU 2011)',
                 'alternativas': ['Cusco',
                                  'San Miguel de Piura',
                                  'Huaura',
                                  'Lima',
                                  'Jauja'],
                 'correcta': 'B'},
                {'pregunta': 'Para realizar el viaje de Cajamarca a Cusco, '
                             'Francisco Pizarro nombró como Inca figurativo '
                             'o títere a: (II CEPRU 2011)',
                 'alternativas': ['Túpac Huallpa',
                                  'Yahuar Huacac',
                                  'Inca Roca',
                                  'Wiracocha',
                                  'Sinchi Roca'],
                 'correcta': 'A'},
                {'pregunta': 'La toma de Constantinopla por los turcos, que '
                             'impulsó la búsqueda de nuevas rutas '
                             'comerciales, ocurrió en:',
                 'alternativas': ['1492', '1499', '1453', '1500', '1440'],
                 'correcta': 'C'},
                {'pregunta': 'El navegante portugués que llegó a las Indias '
                             'bordeando las costas de África en 1499 fue:',
                 'alternativas': ['Cristóbal Colón',
                                  'Fernando de Magallanes',
                                  'Vasco de Gama',
                                  'Américo Vespucio',
                                  'Bartolomé Díaz'],
                 'correcta': 'C'},
                {'pregunta': 'Cristóbal Colón nació en el puerto italiano '
                             'de:',
                 'alternativas': ['Venecia',
                                  'Génova',
                                  'Nápoles',
                                  'Pisa',
                                  'Florencia'],
                 'correcta': 'B'},
                {'pregunta': 'El proyecto de Colón se inspiró, entre otras '
                             'fuentes, en las cartas geográficas de:',
                 'alternativas': ['Ptolomeo',
                                  'Paolo de Toscanelli',
                                  'Marco Polo',
                                  'Américo Vespucio',
                                  'Enrique el Navegante'],
                 'correcta': 'B'},
                {'pregunta': 'El proyecto de Colón fue desechado por los '
                             'sabios de la Universidad de:',
                 'alternativas': ['Salamanca',
                                  'Sevilla',
                                  'Alcalá',
                                  'Coímbra',
                                  'Valladolid'],
                 'correcta': 'A'},
                {'pregunta': 'Colón recibió apoyo para su proyecto en el '
                             'convento de:',
                 'alternativas': ['Montserrat',
                                  'La Rábida',
                                  'San Marcos',
                                  'El Escorial',
                                  'Guadalupe'],
                 'correcta': 'B'},
                {'pregunta': 'La Capitulación de Santa Fe, que autorizó el '
                             'viaje de Colón, se firmó el 17 de abril de:',
                 'alternativas': ['1493', '1491', '1489', '1492', '1490'],
                 'correcta': 'D'},
                {'pregunta': 'Por la Capitulación de Santa Fe, Colón obtuvo '
                             'derecho a qué parte de las riquezas '
                             'encontradas:',
                 'alternativas': ['La quinta parte',
                                  'La cuarta parte',
                                  'La tercera parte',
                                  'La décima parte',
                                  'La mitad'],
                 'correcta': 'D'},
                {'pregunta': 'El puerto fijado como lugar de los '
                             'preparativos del primer viaje de Colón fue:',
                 'alternativas': ['Sevilla',
                                  'Huelva',
                                  'Cádiz',
                                  'Palos',
                                  'Barcelona'],
                 'correcta': 'D'},
                {'pregunta': 'Los verdaderos financistas de la expedición de '
                             'Colón, además de la Corona, fueron los '
                             'hermanos Pinzón y:',
                 'alternativas': ['El Duque de Medinaceli',
                                  'Los Fugger',
                                  'Américo Vespucio',
                                  'Luis de Santángel',
                                  'Alonso de Quintanilla'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'CONTEXTO DE LOS DESCUBRIMIENTOS GEOGRÁFICOS',
                      'items': ['La toma de Constantinopla por los turcos en '
                                '1453 impulsó la búsqueda de nuevas rutas '
                                'comerciales hacia las Indias.',
                                'Los navegantes portugueses llegaron a las '
                                'Indias bordeando África: Vasco de Gama en '
                                '1499.',
                                'Los españoles siguieron la ruta del oeste, '
                                'atravesando el Atlántico: Cristóbal Colón '
                                'en 1492.']},
                     {'titulo': 'CRISTÓBAL COLÓN: FORMACIÓN Y PROYECTO',
                      'items': ['Cristóbal Colón nació en el puerto italiano '
                                'de Génova en 1451.',
                                'Su proyecto se inspiró en el «Imago Mundi», '
                                'las cartas de Paolo de Toscanelli, y la '
                                'tesis de Ptolomeo sobre la redondez de la '
                                'Tierra.',
                                'El proyecto de Colón fue desechado por los '
                                'sabios de la Universidad de Salamanca, y '
                                'rechazado por el rey Juan II de Portugal.',
                                'Colón recibió apoyo en el convento de La '
                                'Rábida, de los religiosos Juan Pérez y '
                                'Antonio Marchena.']},
                     {'titulo': 'LA CAPITULACIÓN DE SANTA FE (1492)',
                      'items': ['La Capitulación de Santa Fe se firmó el 17 '
                                'de abril de 1492, entre la reina Isabel, '
                                'Juan Pérez y Colón.',
                                'Se concedió a Colón los títulos de '
                                'Almirante, Virrey y Gobernador de las '
                                'tierras que encontrara.',
                                'Colón tendría derecho a la décima parte de '
                                'las riquezas, y se le otorgó el título de '
                                'Don.',
                                'El puerto de Palos se fijó como lugar de '
                                'los preparativos del viaje.',
                                'Los verdaderos financistas fueron los '
                                'hermanos Pinzón y el judío portugués Luis '
                                'de Santángel.']},
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
  'secciones': [{'titulo': '10.1 LA EMPRESA DE CONQUISTA: SOCIOS Y PRIMER '
                           'VIAJE',
                 'items': ['{Francisco Pizarro}, Diego de Almagro y Hernando '
                           'de Luque fundaron en Panamá, en 1524, la '
                           '«{Compañía del Levante}».',
                           'El primer viaje (1524-1525) partió el 14 de '
                           'noviembre de 1524; llegó hasta {Pueblo Quemado}, '
                           'donde Almagro perdió un ojo en combate.',
                           'El primer viaje, de {exploración}, fue un '
                           'fracaso.']},
                {'titulo': '10.2 SEGUNDO VIAJE Y LA ISLA DEL GALLO',
                 'items': ['El segundo viaje (1526-1527) partió el 10 de '
                           'marzo de 1526, con el piloto {Bartolomé Ruiz}.',
                           'En la {Isla del Gallo}, Pizarro trazó una línea '
                           'en la arena, invitando a elegir entre volver '
                           'pobres o continuar al sur para hacerse ricos.',
                           'Trece hombres cruzaron la línea con Pizarro, '
                           'conocidos como «{los trece del Gallo}».',
                           'Este segundo viaje llegó hasta {Tumbes}; se le '
                           'conoce como el viaje {descubridor}.']},
                {'titulo': '10.3 LA CAPITULACIÓN DE TOLEDO (1529)',
                 'items': ['La {Capitulación de Toledo} fue firmada el 26 de '
                           'julio de 1529 por la reina Isabel de Portugal.',
                           'Por esta capitulación, {Francisco Pizarro} fue '
                           'nombrado Gobernador, Capitán General y '
                           'Adelantado.',
                           '{Diego de Almagro} fue nombrado gobernador de la '
                           'Fortaleza de Tumbes; Hernando de Luque, vicario '
                           'y Protector de los indios.']},
                {'titulo': '10.4 LA CAPTURA DEL INCA',
                 'items': ['El {16} de noviembre de {1532} se produjo la '
                           'captura de {Atahualpa} en la plaza de '
                           '{Cajamarca}.',
                           'El sacerdote {Vicente Valverde} le entregó la '
                           'Biblia en el llamado {Requerimiento}.',
                           'Atahualpa ofreció un cuarto lleno de {oro} y dos '
                           'de {plata} como {rescate}; fue ejecutado en '
                           '{1533}.']},
                {'titulo': '10.5 FUNDACIÓN DE CIUDADES',
                 'items': ['{San Miguel de Piura}, en Tangarará, fue la '
                           'primera ciudad fundada por Pizarro (1532).',
                           '{Cusco} fue fundada el 23 de marzo de 1534; '
                           '{Jauja}, el 25 de abril de 1534, como capital de '
                           'Nueva Castilla.',
                           '{Lima}, la Ciudad de los Reyes, fue fundada el '
                           '18 de enero de {1535}.',
                           '{Arequipa} fue fundada en 1540 por García Manuel '
                           'de Carbajal.']},
                {'titulo': '10.6 RESISTENCIA DE MANCO INCA Y LA DINASTÍA DE '
                           'VILCABAMBA',
                 'items': ['{Manco Inca} inició la sublevación en mayo de '
                           '1536, apoderándose de {Sacsayhuamán}.',
                           'El capitán inca {Cahuide} (Suruwamán) se inmoló '
                           'antes de caer en manos españolas; también murió '
                           'Juan Pizarro.',
                           'Tras el fracaso, Manco Inca se replegó a '
                           '{Vilcabamba}, donde fue asesinado en 1544 por '
                           'soldados almagristas.',
                           'Le sucedieron {Sayri Túpac} (sometido '
                           'pacíficamente), Titu Cusi Yupanqui, y finalmente '
                           '{Túpac Amaru I}.',
                           '{Túpac Amaru I} fue el último inca de '
                           'Vilcabamba, ejecutado en 1572 por orden del '
                           'virrey Francisco de Toledo.']},
                {'titulo': '10.7 GUERRA CIVIL ENTRE LOS INVASORES',
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
                 'alternativas': ['Pizarro, Alvarado y Belalcázar',
                                  'Pizarro, Almagro y Luque',
                                  'Almagro, Toledo y Luque',
                                  'Pizarro, Valverde y Soto',
                                  'Pizarro, Cortés y Luque'],
                 'correcta': 'B'},
                {'pregunta': 'El episodio de los Trece del Gallo ocurrió '
                             'durante el:',
                 'alternativas': ['Primer viaje',
                                  'Tercer viaje',
                                  'Cuarto viaje',
                                  'Segundo viaje',
                                  'Viaje de regreso'],
                 'correcta': 'D'},
                {'pregunta': 'La Capitulación de Toledo se firmó en el año:',
                 'alternativas': ['1531', '1535', '1524', '1529', '1532'],
                 'correcta': 'D'},
                {'pregunta': 'La Capitulación de Toledo nombró a Pizarro:',
                 'alternativas': ['Virrey del Perú',
                                  'Gobernador y capitán general',
                                  'Almirante',
                                  'Adelantado de Nueva Toledo',
                                  'Corregidor'],
                 'correcta': 'B'},
                {'pregunta': 'La captura de Atahualpa se produjo el:',
                 'alternativas': ['6 de diciembre de 1534',
                                  '18 de enero de 1535',
                                  '26 de julio de 1533',
                                  '16 de noviembre de 1532',
                                  '15 de agosto de 1536'],
                 'correcta': 'D'},
                {'pregunta': 'La captura del Inca ocurrió en la plaza de:',
                 'alternativas': ['Cajamarca',
                                  'Cusco',
                                  'Tumbes',
                                  'Piura',
                                  'Jauja'],
                 'correcta': 'A'},
                {'pregunta': 'El sacerdote que entregó la Biblia a Atahualpa '
                             'fue:',
                 'alternativas': ['Bartolomé de las Casas',
                                  'Hernando de Luque',
                                  'Toribio de Mogrovejo',
                                  'Jerónimo de Loayza',
                                  'Vicente Valverde'],
                 'correcta': 'E'},
                {'pregunta': 'La primera ciudad española fundada en el Perú '
                             'fue:',
                 'alternativas': ['Trujillo',
                                  'Lima',
                                  'Jauja',
                                  'San Miguel de Tangarará',
                                  'Cusco español'],
                 'correcta': 'D'},
                {'pregunta': 'Lima fue fundada por Pizarro el:',
                 'alternativas': ['16 de noviembre de 1532',
                                  '6 de abril de 1538',
                                  '18 de enero de 1535',
                                  '26 de junio de 1541',
                                  '9 de diciembre de 1824'],
                 'correcta': 'C'},
                {'pregunta': 'El Inca que encabezó la resistencia y sitió el '
                             'Cusco en 1536 fue:',
                 'alternativas': ['Atahualpa',
                                  'Sayri Túpac',
                                  'Túpac Amaru I',
                                  'Manco Inca',
                                  'Huáscar'],
                 'correcta': 'D'},
                {'pregunta': 'El Estado neoinca de resistencia se estableció '
                             'en:',
                 'alternativas': ['Ollantaytambo',
                                  'Vilcabamba',
                                  'Cajamarca',
                                  'Chachapoyas',
                                  'Vitcos únicamente'],
                 'correcta': 'B'},
                {'pregunta': 'El último inca de Vilcabamba, ejecutado en '
                             '1572, fue:',
                 'alternativas': ['Manco Inca',
                                  'Titu Cusi Yupanqui',
                                  'Paullu Inca',
                                  'Túpac Amaru I',
                                  'Sayri Túpac'],
                 'correcta': 'D'},
                {'pregunta': 'La ejecución de Túpac Amaru I fue ordenada por '
                             'el virrey:',
                 'alternativas': ['Blasco Núñez de Vela',
                                  'Antonio de Mendoza',
                                  'Francisco de Toledo',
                                  'Andrés Hurtado de Mendoza',
                                  'Pedro de la Gasca'],
                 'correcta': 'C'},
                {'pregunta': 'En la batalla de las Salinas (1538) fue '
                             'derrotado:',
                 'alternativas': ['Gonzalo Pizarro',
                                  'Almagro el Mozo',
                                  'Núñez de Vela',
                                  'Diego de Almagro',
                                  'Hernando Pizarro'],
                 'correcta': 'D'},
                {'pregunta': 'El primer virrey del Perú, muerto en la '
                             'batalla de Añaquito, fue:',
                 'alternativas': ['Antonio de Mendoza',
                                  'Andrés Hurtado de Mendoza',
                                  'Francisco de Toledo',
                                  'Pedro de la Gasca',
                                  'Blasco Núñez de Vela'],
                 'correcta': 'E'},
                {'pregunta': 'En la batalla de Jaquijahuana (1548) fue '
                             'derrotado:',
                 'alternativas': ['Gonzalo Pizarro',
                                  'Francisco Pizarro',
                                  'Almagro el Mozo',
                                  'Hernando de Soto',
                                  'Diego de Almagro'],
                 'correcta': 'A'},
                {'pregunta': 'El primer viaje de la conquista llegó hasta:',
                 'alternativas': ['Isla del Gallo',
                                  'Puerto del Hambre',
                                  'Panamá',
                                  'Cajamarca',
                                  'Tumbes'],
                 'correcta': 'B'},
                {'pregunta': 'El rescate ofrecido por Atahualpa consistió '
                             'en:',
                 'alternativas': ['Tributos anuales',
                                  'Naves y armas',
                                  'Tierras y siervos',
                                  'Un cuarto de oro y dos de plata',
                                  'Un cuarto de plata solamente'],
                 'correcta': 'D'},
                {'pregunta': 'El tercer viaje de la conquista partió de '
                             'Panamá en el año:',
                 'alternativas': ['1529', '1526', '1532', '1524', '1531'],
                 'correcta': 'E'},
                {'pregunta': 'El acto formal de sometimiento leído a '
                             'Atahualpa se conoce como:',
                 'alternativas': ['La Capitulación',
                                  'La Bula',
                                  'El Testamento',
                                  'El Requerimiento',
                                  'Las Ordenanzas'],
                 'correcta': 'D'},
                {'pregunta': 'La capitulación de Toledo fue firmada por '
                             'Isabel de Portugal; dicho acto dio inicio a '
                             'la: (UNSAAC Ordinario)',
                 'alternativas': ['Dominación y dependencia del Perú',
                                  'Invasión española al Perú',
                                  'Institucionalización colonial en el Perú',
                                  'Creación del Virreinato en el Perú',
                                  'Pacificación del Perú'],
                 'correcta': 'B'},
                {'pregunta': 'En la Batalla de Salinas, las tropas '
                             'almagristas estuvieron al mando de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Almagro el Mozo',
                                  'Diego de Centeno',
                                  'Cristóbal Baca de Castro',
                                  'Rodrigo de Ordoñez',
                                  'Fray Tomas de Berlanga'],
                 'correcta': 'D'},
                {'pregunta': 'En la Guerra de los Encomenderos, en la '
                             'batalla de Jaquijahuana, se enfrentaron los '
                             'bandos de: (UNSAAC Ordinario)',
                 'alternativas': ['Gonzalo Pizarro y Diego Centeno',
                                  'Gonzalo Pizarro y el Pacificador Pedro de '
                                  'la Gasca',
                                  'Gonzalo Pizarro y Cristóbal Baca de '
                                  'Castro',
                                  'Francisco Pizarro y Fray Tomas de '
                                  'Berlanga',
                                  'Almagro el Mozo y Blasco Núñez de Vela'],
                 'correcta': 'B'},
                {'pregunta': 'La sociedad fundada en Panamá en 1524 por '
                             'Pizarro, Almagro y Luque para la conquista se '
                             'llamó:',
                 'alternativas': ['Empresa de Tumbes',
                                  'Compañía de Indias',
                                  'Sociedad del Sur',
                                  'Compañía del Levante',
                                  'Hermandad de Panamá'],
                 'correcta': 'D'},
                {'pregunta': 'En el primer viaje de Pizarro (1524-1525), '
                             'Diego de Almagro perdió un ojo en combate en:',
                 'alternativas': ['Tumbes',
                                  'Isla del Gallo',
                                  'Isla de la Gorgona',
                                  'Coaque',
                                  'Pueblo Quemado'],
                 'correcta': 'E'},
                {'pregunta': 'En la Isla del Gallo, Pizarro trazó una línea '
                             'en la arena; los hombres que la cruzaron con '
                             'él se conocen como:',
                 'alternativas': ['Los trece del Gallo',
                                  'Los fieles de Panamá',
                                  'Los trece de la fama',
                                  'Los conquistadores de Tumbes',
                                  'Los caballeros de Cajamarca'],
                 'correcta': 'A'},
                {'pregunta': 'El segundo viaje de Pizarro, conocido como el '
                             'viaje descubridor, contó con el piloto '
                             'profesional:',
                 'alternativas': ['Diego de Almagro',
                                  'Sebastián de Belalcázar',
                                  'Hernando de Soto',
                                  'Bartolomé Ruiz',
                                  'Pedro de Candía'],
                 'correcta': 'D'},
                {'pregunta': 'La Capitulación de Toledo, que autorizó la '
                             'invasión al Perú, fue firmada el 26 de julio '
                             'de:',
                 'alternativas': ['1524', '1526', '1529', '1532', '1534'],
                 'correcta': 'C'},
                {'pregunta': 'Por la Capitulación de Toledo, Francisco '
                             'Pizarro fue nombrado Gobernador, Capitán '
                             'General y:',
                 'alternativas': ['Adelantado',
                                  'Oidor',
                                  'Virrey',
                                  'Corregidor',
                                  'Arzobispo'],
                 'correcta': 'A'},
                {'pregunta': 'La primera ciudad fundada por los españoles en '
                             'el Perú, en 1532, fue:',
                 'alternativas': ['Trujillo',
                                  'Jauja',
                                  'San Miguel de Piura',
                                  'Lima',
                                  'Cusco'],
                 'correcta': 'C'},
                {'pregunta': 'La ciudad del Cusco fue fundada por los '
                             'españoles el 23 de marzo de:',
                 'alternativas': ['1535', '1536', '1534', '1533', '1532'],
                 'correcta': 'C'},
                {'pregunta': 'Lima, la Ciudad de los Reyes, fue fundada por '
                             'Francisco Pizarro el 18 de enero de:',
                 'alternativas': ['1533', '1534', '1537', '1535', '1536'],
                 'correcta': 'D'},
                {'pregunta': 'Manco Inca inició su sublevación contra los '
                             'españoles apoderándose de:',
                 'alternativas': ['Sacsayhuamán',
                                  'Ollantaytambo',
                                  'Písac',
                                  'Machupicchu',
                                  'El Coricancha'],
                 'correcta': 'A'},
                {'pregunta': 'El capitán inca que se inmoló antes de caer en '
                             'manos de los españoles durante el sitio del '
                             'Cusco fue:',
                 'alternativas': ['Quisquis',
                                  'Cahuide (Suruwamán)',
                                  'Rumiñahui',
                                  'Calcuchímac',
                                  'Titu Yupanqui'],
                 'correcta': 'B'},
                {'pregunta': 'Manco Inca, tras el fracaso de su sublevación, '
                             'se replegó a la región de:',
                 'alternativas': ['Vilcabamba',
                                  'Machupicchu',
                                  'Espíritu Pampa',
                                  'Vitcos',
                                  'Choquequirao'],
                 'correcta': 'A'},
                {'pregunta': 'El último inca de la dinastía rebelde de '
                             'Vilcabamba, ejecutado en 1572, fue:',
                 'alternativas': ['Sayri Túpac',
                                  'Titu Cusi Yupanqui',
                                  'Manco Inca',
                                  'Túpac Amaru I',
                                  'Cahuide'],
                 'correcta': 'D'},
                {'pregunta': 'El inca de Vilcabamba que se sometió '
                             'pacíficamente al virrey Hurtado de Mendoza '
                             'fue:',
                 'alternativas': ['Túpac Amaru I',
                                  'Manco Inca',
                                  'Sayri Túpac',
                                  'Cahuide',
                                  'Titu Cusi Yupanqui'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'LA EMPRESA DE CONQUISTA: SOCIOS Y PRIMER '
                                'VIAJE',
                      'items': ['Francisco Pizarro, Diego de Almagro y '
                                'Hernando de Luque fundaron en Panamá, en '
                                '1524, la «Compañía del Levante».',
                                'El primer viaje (1524-1525) partió el 14 de '
                                'noviembre de 1524; llegó hasta Pueblo '
                                'Quemado, donde Almagro perdió un ojo en '
                                'combate.',
                                'El primer viaje, de exploración, fue un '
                                'fracaso.']},
                     {'titulo': 'SEGUNDO VIAJE Y LA ISLA DEL GALLO',
                      'items': ['El segundo viaje (1526-1527) partió el 10 '
                                'de marzo de 1526, con el piloto Bartolomé '
                                'Ruiz.',
                                'En la Isla del Gallo, Pizarro trazó una '
                                'línea en la arena, invitando a elegir entre '
                                'volver pobres o continuar al sur para '
                                'hacerse ricos.',
                                'Trece hombres cruzaron la línea con '
                                'Pizarro, conocidos como «los trece del '
                                'Gallo».',
                                'Este segundo viaje llegó hasta Tumbes; se '
                                'le conoce como el viaje descubridor.']},
                     {'titulo': 'LA CAPITULACIÓN DE TOLEDO (1529)',
                      'items': ['La Capitulación de Toledo fue firmada el 26 '
                                'de julio de 1529 por la reina Isabel de '
                                'Portugal.',
                                'Por esta capitulación, Francisco Pizarro '
                                'fue nombrado Gobernador, Capitán General y '
                                'Adelantado.',
                                'Diego de Almagro fue nombrado gobernador de '
                                'la Fortaleza de Tumbes; Hernando de Luque, '
                                'vicario y Protector de los indios.']},
                     {'titulo': 'LA CAPTURA DEL INCA',
                      'items': ['El 16 de noviembre de 1532 se produjo la '
                                'captura de Atahualpa en la plaza de '
                                'Cajamarca.',
                                'El sacerdote Vicente Valverde le entregó la '
                                'Biblia en el llamado Requerimiento.',
                                'Atahualpa ofreció un cuarto lleno de oro y '
                                'dos de plata como rescate; fue ejecutado en '
                                '1533.']},
                     {'titulo': 'FUNDACIÓN DE CIUDADES',
                      'items': ['San Miguel de Piura, en Tangarará, fue la '
                                'primera ciudad fundada por Pizarro (1532).',
                                'Cusco fue fundada el 23 de marzo de 1534; '
                                'Jauja, el 25 de abril de 1534, como capital '
                                'de Nueva Castilla.',
                                'Lima, la Ciudad de los Reyes, fue fundada '
                                'el 18 de enero de 1535.',
                                'Arequipa fue fundada en 1540 por García '
                                'Manuel de Carbajal.']},
                     {'titulo': 'RESISTENCIA DE MANCO INCA Y LA DINASTÍA DE '
                                'VILCABAMBA',
                      'items': ['Manco Inca inició la sublevación en mayo de '
                                '1536, apoderándose de Sacsayhuamán.',
                                'El capitán inca Cahuide (Suruwamán) se '
                                'inmoló antes de caer en manos españolas; '
                                'también murió Juan Pizarro.',
                                'Tras el fracaso, Manco Inca se replegó a '
                                'Vilcabamba, donde fue asesinado en 1544 por '
                                'soldados almagristas.',
                                'Le sucedieron Sayri Túpac (sometido '
                                'pacíficamente), Titu Cusi Yupanqui, y '
                                'finalmente Túpac Amaru I.',
                                'Túpac Amaru I fue el último inca de '
                                'Vilcabamba, ejecutado en 1572 por orden del '
                                'virrey Francisco de Toledo.']},
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
                {'titulo': '11.2 LA CORONA Y EL CONSEJO DE INDIAS',
                 'items': ['El {rey} era la suprema autoridad, encabezando '
                           'una monarquía absoluta sustentada en el derecho '
                           'divino.',
                           'Entre 1532 y 1824 gobernaron dos dinastías: los '
                           '{Habsburgo} (Carlos I a Carlos II) y los Borbón '
                           '(Felipe V a Fernando VII).',
                           'El {Real y Supremo Consejo de Indias} fue creado '
                           'en 1524 por Carlos V, como organismo supremo de '
                           'gobierno para las colonias.',
                           'El Consejo de Indias proponía al rey el '
                           'nombramiento de {virreyes} y, mediante el Regio '
                           'Patronato, de arzobispos y obispos.']},
                {'titulo': '11.3 LA CASA DE CONTRATACIÓN Y EL VIRREINATO',
                 'items': ['La {Casa de Contratación} de Sevilla, creada en '
                           '1503, controlaba el comercio entre España y sus '
                           'colonias.',
                           'El único puerto autorizado en América del Sur '
                           'para el comercio con España era el puerto del '
                           '{Callao}.',
                           'El {virrey} era el representante del rey, jefe '
                           'del poder político con residencia en Lima.',
                           'Al finalizar su mandato, el virrey remitía el '
                           'informe de su gestión llamado «{Pliego de '
                           'Mortaja}».',
                           'Durante la colonia gobernaron {40} virreyes en '
                           'el Perú; el primero fue Blasco Núñez de Vela y '
                           'el último, José de la Serna.']},
                {'titulo': '11.4 LA REAL AUDIENCIA Y EL CORREGIMIENTO',
                 'items': ['La {Real Audiencia} era un tribunal colegiado '
                           'integrado por oidores, fiscales y escribanos; '
                           'asumía el gobierno ante ausencia del virrey.',
                           'Existieron audiencias {virreinales} (Perú y '
                           'México), pretoriales y subordinadas (Cusco).',
                           'El {corregimiento} fue creado para amparar a los '
                           'aborígenes de los abusos de los encomenderos; el '
                           'Perú tuvo 52 corregimientos.',
                           'Los corregidores obligaban a los aborígenes a '
                           'recibir mercancías mediante el sistema llamado '
                           '«{Reparto}».']},
                {'titulo': '11.5 LA INTENDENCIA, EL CABILDO Y EL CACICAZGO',
                 'items': ['La {Intendencia}, de origen francés, fue '
                           'establecida por Carlos III en 1784 tras la '
                           'rebelión de Túpac Amaru.',
                           'El Perú se dividió en {8} intendencias: Lima, '
                           'Trujillo, Arequipa, Huancavelica, Tarma, '
                           'Huamanga, Puno y Cusco.',
                           'El {Cabildo} o Ayuntamiento cumplía funciones '
                           'similares a las municipalidades actuales.',
                           'El {Cacicazgo} estaba representado por los '
                           'caciques, antiguos curacas, encargados de cobrar '
                           'tributos.']},
                {'titulo': '11.6 CARACTERÍSTICAS DE LA ECONOMÍA COLONIAL',
                 'items': ['El {intervencionismo} fue el sistema impuesto '
                           'por la Corona para acentuar la dominación y '
                           'dependencia.',
                           'El {mercantilismo} buscaba que el Estado '
                           'consiguiera la mayor cantidad de oro y plata '
                           'mediante comercio monopólico.',
                           'El {monopolio comercial} prohibía a las colonias '
                           'comerciar con otros países; era controlado por '
                           'la Casa de Contratación.']},
                {'titulo': '11.7 LA MINERÍA COLONIAL',
                 'items': ['La {minería} fue la actividad económica más '
                           'importante de la colonia.',
                           'El {Cerro Rico de Potosí}, descubierto en 1545, '
                           'fue la mina más importante de plata.',
                           '{Huancavelica} fue la principal fuente de azogue '
                           '(mercurio), usado para el beneficio de la plata.',
                           'La {mita minera} fue implantada por el virrey '
                           'Francisco de Toledo.',
                           'Los métodos de extracción incluían tajo abierto '
                           '(azogue), socavones ({plata}) y lavaderos '
                           '(oro).']},
                {'titulo': '11.8 OTRAS ACTIVIDADES ECONÓMICAS',
                 'items': ['En la {agricultura}, la tierra se hizo '
                           'individual y privada, formando grandes '
                           'haciendas; se incorporó el trigo y la vid.',
                           'La {industria} textil colonial se expresó en los '
                           'obrajes, que producían la «ropa de la tierra».',
                           'En la colonia se acuñaron monedas como pesos de '
                           'oro, ducados, {escudos} y doblones.']},
                {'titulo': '11.9 LOS IMPUESTOS COLONIALES',
                 'items': ['El {Almojarifazgo} era el impuesto de aduanas '
                           'sobre productos importados y exportados.',
                           'La {Alcabala} se cobraba sobre las compras y '
                           'ventas de bienes.',
                           'El {Tributo} era una contribución exclusiva de '
                           'los aborígenes, en señal de vasallaje al rey.',
                           'El {Quinto Real} consistía en el pago de la '
                           'quinta parte de la producción minera.',
                           'El {Diezmo} era la décima parte de la producción '
                           'entregada a la Iglesia.']},
                {'titulo': '11.10 y 11.3.4 LO SOCIAL Y LO EDUCATIVO',
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
                                  'Repartimiento',
                                  'Mita',
                                  'Reducción',
                                  'Yanaconaje'],
                 'correcta': 'A'},
                {'pregunta': 'La encomienda otorgaba al encomendero el '
                             'derecho a recibir:',
                 'alternativas': ['El tributo de los indígenas',
                                  'Las minas del lugar',
                                  'Títulos nobiliarios',
                                  'El gobierno provincial',
                                  'La propiedad de la tierra'],
                 'correcta': 'A'},
                {'pregunta': 'El organismo con sede en España encargado de '
                             'legislar sobre América fue:',
                 'alternativas': ['La Audiencia',
                                  'La Casa de Contratación',
                                  'El Cabildo',
                                  'El Consulado',
                                  'El Consejo de Indias'],
                 'correcta': 'E'},
                {'pregunta': 'La institución que controlaba el comercio con '
                             'América, con sede en Sevilla, fue:',
                 'alternativas': ['La Casa de Contratación',
                                  'La Audiencia',
                                  'El Tribunal del Consulado',
                                  'El Consejo de Indias',
                                  'La Real Hacienda'],
                 'correcta': 'A'},
                {'pregunta': 'El máximo tribunal de justicia en América '
                             'colonial fue:',
                 'alternativas': ['La Intendencia',
                                  'El Consulado',
                                  'El Cabildo',
                                  'El Corregimiento',
                                  'La Audiencia'],
                 'correcta': 'E'},
                {'pregunta': 'El virrey que organizó el virreinato peruano y '
                             'creó las reducciones fue:',
                 'alternativas': ['Manuel de Amat',
                                  'Blasco Núñez de Vela',
                                  'Andrés Hurtado de Mendoza',
                                  'Francisco de Toledo',
                                  'Pedro de la Gasca'],
                 'correcta': 'D'},
                {'pregunta': 'El principal centro minero de plata en el '
                             'virreinato fue:',
                 'alternativas': ['Cerro de Pasco',
                                  'Huancavelica',
                                  'Hualgayoc',
                                  'Castrovirreyna',
                                  'Potosí'],
                 'correcta': 'E'},
                {'pregunta': 'Huancavelica fue famosa por la producción de:',
                 'alternativas': ['Estaño',
                                  'Oro',
                                  'Cobre',
                                  'Mercurio o azogue',
                                  'Plata'],
                 'correcta': 'D'},
                {'pregunta': 'El impuesto sobre la producción minera '
                             'entregado a la Corona fue:',
                 'alternativas': ['El almojarifazgo',
                                  'El quinto real',
                                  'La alcabala',
                                  'El tributo indígena',
                                  'El diezmo'],
                 'correcta': 'B'},
                {'pregunta': 'El comercio colonial se caracterizó por ser:',
                 'alternativas': ['Libre',
                                  'Regional',
                                  'Monopólico',
                                  'Descentralizado',
                                  'De trueque'],
                 'correcta': 'C'},
                {'pregunta': 'Los pueblos donde se concentró a la población '
                             'indígena para controlarla se llamaron:',
                 'alternativas': ['Corregimientos',
                                  'Obrajes',
                                  'Reducciones',
                                  'Encomiendas',
                                  'Haciendas'],
                 'correcta': 'C'},
                {'pregunta': 'La sociedad colonial se organizó de manera:',
                 'alternativas': ['Estamental según el origen étnico',
                                  'Sin distinciones legales',
                                  'Democrática',
                                  'Meritocrática',
                                  'Igualitaria'],
                 'correcta': 'A'},
                {'pregunta': 'El colegio colonial destinado a los hijos de '
                             'caciques en el Cusco fue:',
                 'alternativas': ['San Borja',
                                  'Santo Tomás',
                                  'San Bernardo',
                                  'San Pablo',
                                  'San Marcos'],
                 'correcta': 'A'},
                {'pregunta': 'La Universidad Nacional de San Antonio Abad '
                             'del Cusco fue fundada en:',
                 'alternativas': ['1620', '1821', '1571', '1692', '1551'],
                 'correcta': 'D'},
                {'pregunta': 'La Universidad Nacional Mayor de San Marcos '
                             'fue fundada en:',
                 'alternativas': ['1572', '1692', '1551', '1821', '1492'],
                 'correcta': 'C'},
                {'pregunta': 'La mita minera colonial consistió en:',
                 'alternativas': ['Una encomienda de indios',
                                  'Un servicio doméstico',
                                  'Un tributo en especies',
                                  'Trabajo obligatorio por turnos en las '
                                  'minas',
                                  'Un préstamo forzoso'],
                 'correcta': 'D'},
                {'pregunta': 'El funcionario encargado de cobrar tributos en '
                             'las provincias fue:',
                 'alternativas': ['El visitador',
                                  'El alcalde mayor',
                                  'El corregidor',
                                  'El oidor',
                                  'El virrey'],
                 'correcta': 'C'},
                {'pregunta': 'La educación colonial se caracterizó por ser:',
                 'alternativas': ['Universal y gratuita',
                                  'Técnica',
                                  'Obligatoria',
                                  'Laica',
                                  'Elitista'],
                 'correcta': 'E'},
                {'pregunta': 'El repartimiento consistió principalmente en:',
                 'alternativas': ['La distribución de tierras entre '
                                  'indígenas',
                                  'El reparto de indígenas entre los '
                                  'conquistadores',
                                  'La entrega de minas',
                                  'La fundación de ciudades',
                                  'La creación de cabildos'],
                 'correcta': 'B'},
                {'pregunta': 'El sistema de transporte comercial entre '
                             'España y América se basó en:',
                 'alternativas': ['Naves individuales libres',
                                  'Flotas y galeones',
                                  'Barcos de vapor',
                                  'Caravanas terrestres',
                                  'Compañías privadas holandesas'],
                 'correcta': 'B'},
                {'pregunta': 'La Universidad de San Marcos fue fundada en el '
                             'año:',
                 'alternativas': ['1600', '1538', '1492', '1551', '1692'],
                 'correcta': 'D'},
                {'pregunta': 'El obispo que creó el seminario del que se '
                             'originó la Universidad de San Antonio Abad del '
                             'Cusco fue:',
                 'alternativas': ['Vicente de Valverde',
                                  'Manuel de Mollinedo y Angulo',
                                  'Jerónimo de Loayza',
                                  'Antonio de la Raya',
                                  'Juan Cárdenas y Céspedes'],
                 'correcta': 'D'},
                {'pregunta': 'El gestor de la creación de la Universidad de '
                             'San Antonio Abad del Cusco como universidad '
                             'fue el obispo:',
                 'alternativas': ['Antonio de la Raya',
                                  'Juan Cárdenas y Céspedes',
                                  'Manuel de Mollinedo y Angulo',
                                  'Jerónimo de Loayza',
                                  'Vicente de Valverde'],
                 'correcta': 'C'},
                {'pregunta': 'El papa que emitió el breve pontificio de '
                             'creación de la Universidad de San Antonio Abad '
                             'del Cusco, en 1692, fue:',
                 'alternativas': ['Inocencio XII',
                                  'Pío VII',
                                  'Gregorio XIII',
                                  'Pío V',
                                  'León X'],
                 'correcta': 'A'},
                {'pregunta': 'El primer rector de la Universidad de San '
                             'Antonio Abad del Cusco fue:',
                 'alternativas': ['Juan Cárdenas y Céspedes',
                                  'Manuel de Mollinedo',
                                  'Juan Bautista de la Roca',
                                  'Antonio de la Raya',
                                  'Fray Vicente de Valverde'],
                 'correcta': 'A'},
                {'pregunta': 'La encomienda fue abolida por la Real Cédula, '
                             'provocando la: (UNSAAC Ordinario)',
                 'alternativas': ['Caída del Virrey',
                                  'Revolución de Tupac Amaru',
                                  'Protesta de los caciques',
                                  'Rebelión de los encomenderos',
                                  'Rebelión de Manco Inca'],
                 'correcta': 'D'},
                {'pregunta': 'La institución colonial caracterizada por el '
                             'vasallaje ideológico en lo político, económico '
                             'y social fue: (UNSAAC Ordinario)',
                 'alternativas': ['La Real Audiencia',
                                  'El corregimiento',
                                  'La intendencia',
                                  'El repartimiento',
                                  'La encomienda'],
                 'correcta': 'E'},
                {'pregunta': 'La primera institución de explotación en el '
                             'Perú fue: (UNSAAC Ordinario)',
                 'alternativas': ['El corregimiento',
                                  'El repartimiento',
                                  'La Audiencia',
                                  'La intendencia',
                                  'La mita'],
                 'correcta': 'B'},
                {'pregunta': 'Dentro de las instituciones coloniales, la '
                             'institución más antigua fue: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Intendencias',
                                  'Repartimientos',
                                  'Corregimientos',
                                  'Mita minera',
                                  'Encomiendas'],
                 'correcta': 'E'},
                {'pregunta': 'En la Colonia, la institución que cumplió la '
                             'función de vasallaje ideológico, político, '
                             'económico y social fue: (UNSAAC Ordinario)',
                 'alternativas': ['La Real Audiencia',
                                  'La Encomienda',
                                  'Los Repartimientos',
                                  'El Consejo de Indias',
                                  'La Corona'],
                 'correcta': 'B'},
                {'pregunta': 'El gestor de la creación de la Universidad '
                             'Nacional de San Antonio Abad del Cusco en 1692 '
                             'fue: (UNSAAC Ordinario)',
                 'alternativas': ['Jerónimo de Aliaga',
                                  'Juan Bautista de la Roca',
                                  'Manuel Mollinedo y Angulo',
                                  'Tomas de San Martín',
                                  'Juan Cárdenas y Céspedes'],
                 'correcta': 'C'},
                {'pregunta': 'El impuesto que la Corona Española exigía a '
                             'sus colonias, conocido como la Media Anata, '
                             'consistía en el: (UNSAAC Ordinario)',
                 'alternativas': ['Recojo de los impuestos aduaneros en los '
                                  'puertos americanos',
                                  'Pago proporcional de los comerciantes por '
                                  'la custodia de sus cargamentos',
                                  'Pago de impuesto por el salario que '
                                  'percibían las autoridades',
                                  'Impuestos que afectaban a las '
                                  'transacciones comerciales internas',
                                  'Cobro por los diezmos y primicias a las '
                                  'autoridades eclesiásticas'],
                 'correcta': 'C'},
                {'pregunta': 'La organización social del Perú Colonial que '
                             'correspondió al sector de la clase del bajo '
                             'pueblo estuvo conformada por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Españoles y criollos carentes de título '
                                  'nobiliario poseedores de fortuna y '
                                  'profesionales',
                                  'Españoles y criollos con títulos '
                                  'nobiliarios, funcionarios públicos y '
                                  'eclesiásticos',
                                  'Españoles y criollos dedicados a pequeñas '
                                  'actividades comerciales y artesanos',
                                  'Indios descendientes de los incas, que se '
                                  'desarrollaron en un ambiente comunitario',
                                  'Esclavos negros que servían en las casas '
                                  'señoriales y haciendas'],
                 'correcta': 'C'},
                {'pregunta': 'El Rey que dispuso la supresión de las '
                             'encomiendas, fue: (UNSAAC Ordinario)',
                 'alternativas': ['Carlos III',
                                  'Felipe III',
                                  'Felipe II',
                                  'Carlos V',
                                  'Carlos II'],
                 'correcta': 'D'},
                {'pregunta': 'La institución que se creó por los excesivos '
                             'abusos que cometían los encomenderos fue: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['El Virreinato',
                                  'La Intendencia',
                                  'El Cabildo',
                                  'El Cacicazgo',
                                  'El Corregimiento'],
                 'correcta': 'E'},
                {'pregunta': 'La Institución Educativa de origen colonial, '
                             'que fue fundada para los hijos de los caciques '
                             'en el Cusco, fue el colegio de San: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Bernardo',
                                  'Antonio Abad',
                                  'Francisco de Borja',
                                  'Ignacio de Loyola',
                                  'Felipe'],
                 'correcta': 'C'},
                {'pregunta': 'En el Periodo Colonial, el impuesto denominado '
                             'Diezmo, fue el: (UNSAAC Ordinario)',
                 'alternativas': ['Pago a las aduanas por compra de '
                                  'productos mercantiles de exportación',
                                  'Pago a los jornaleros por su trabajo en '
                                  'las haciendas cañaverales',
                                  'Tributo que se cobraba a la compra y '
                                  'venta de los bienes muebles e inmuebles',
                                  'Pago de la décima parte de la producción '
                                  'agrícola y obrajera en favor de la '
                                  'iglesia',
                                  'Tributo de la quinta parte de la '
                                  'producción minera'],
                 'correcta': 'D'},
                {'pregunta': 'Sobre la educación Colonial del Perú, se '
                             'afirma que: (UNSAAC Ordinario)',
                 'alternativas': ['La primera universidad del Perú fue la de '
                                  'San Antonio Abad del Cusco',
                                  'Los colegios mayores fueron centros de '
                                  'formación de los caciques',
                                  'Los colegios mayores fueron equivalentes '
                                  'a las universidades',
                                  'La universidad estaba regentada por '
                                  'autoridades civiles',
                                  'La universidad fue una institución '
                                  'elitista'],
                 'correcta': 'B'},
                {'pregunta': 'El Real y Supremo Consejo de Indias, organismo '
                             'supremo de gobierno colonial, fue constituido '
                             'por Carlos V en:',
                 'alternativas': ['1532', '1524', '1503', '1550', '1511'],
                 'correcta': 'B'},
                {'pregunta': 'La institución colonial más antigua, creada en '
                             '1503 para controlar el comercio con América, '
                             'fue:',
                 'alternativas': ['La Real Audiencia',
                                  'El Consejo de Indias',
                                  'La Intendencia',
                                  'El Virreinato',
                                  'La Casa de Contratación de Sevilla'],
                 'correcta': 'E'},
                {'pregunta': 'En el Virreinato del Perú, el puerto exclusivo '
                             'del monopolio comercial fue el puerto:',
                 'alternativas': ['De Cartagena',
                                  'De Veracruz',
                                  'De Guayaquil',
                                  'Del Callao',
                                  'De Valparaíso'],
                 'correcta': 'D'},
                {'pregunta': 'El primer virrey del Perú fue:',
                 'alternativas': ['Francisco de Toledo',
                                  'Antonio de Mendoza',
                                  'Blasco Núñez de Vela',
                                  'José de la Serna',
                                  'Andrés Hurtado de Mendoza'],
                 'correcta': 'C'},
                {'pregunta': 'El informe final que un virrey remitía al '
                             'finalizar su mandato se llamaba:',
                 'alternativas': ['Pliego de Mortaja',
                                  'Juicio de Residencia',
                                  'Cédula Real',
                                  'Memoria de Gobierno',
                                  'Auto de Visita'],
                 'correcta': 'A'},
                {'pregunta': 'La Real Audiencia asumía funciones de gobierno '
                             'en caso de incapacidad, ausencia o muerte del:',
                 'alternativas': ['Corregidor',
                                  'Papa',
                                  'Rey',
                                  'Consejo de Indias',
                                  'Virrey'],
                 'correcta': 'E'},
                {'pregunta': 'El corregimiento fue creado en respuesta a los '
                             'abusos cometidos por:',
                 'alternativas': ['Los caciques',
                                  'Los oidores',
                                  'Los encomenderos',
                                  'Los intendentes',
                                  'Los virreyes'],
                 'correcta': 'C'},
                {'pregunta': 'El Perú colonial estuvo dividido en un número '
                             'de corregimientos igual a:',
                 'alternativas': ['8', '52', '100', '25', '40'],
                 'correcta': 'B'},
                {'pregunta': 'La Intendencia, de origen francés, fue '
                             'establecida en el Perú por Carlos III en:',
                 'alternativas': ['1750', '1650', '1810', '1784', '1700'],
                 'correcta': 'D'},
                {'pregunta': 'El Perú colonial se dividió en un número de '
                             'intendencias igual a:',
                 'alternativas': ['52', '40', '12', '8', '4'],
                 'correcta': 'D'},
                {'pregunta': 'El sistema mediante el cual el Estado buscaba '
                             'conseguir la mayor cantidad de oro y plata a '
                             'través del comercio monopólico se llamó:',
                 'alternativas': ['Mercantilismo',
                                  'Fisiocracia',
                                  'Proteccionismo',
                                  'Intervencionismo',
                                  'Monopolio comercial'],
                 'correcta': 'A'},
                {'pregunta': 'El cerro rico de plata más importante de la '
                             'minería colonial, descubierto en 1545, fue:',
                 'alternativas': ['Potosí',
                                  'Laicacota',
                                  'Cerro de Pasco',
                                  'Castrovirreyna',
                                  'Caylloma'],
                 'correcta': 'A'},
                {'pregunta': 'La principal fuente de azogue (mercurio) en el '
                             'virreinato peruano se ubicaba en:',
                 'alternativas': ['Huancavelica',
                                  'Cajamarca',
                                  'Arequipa',
                                  'Puno',
                                  'Cusco'],
                 'correcta': 'A'},
                {'pregunta': 'La mita minera colonial fue implantada por el '
                             'virrey:',
                 'alternativas': ['Blasco Núñez de Vela',
                                  'Manuel de Amat',
                                  'José de la Serna',
                                  'Francisco de Toledo',
                                  'Antonio de Mendoza'],
                 'correcta': 'D'},
                {'pregunta': 'Las fábricas textiles coloniales que producían '
                             'la «ropa de la tierra» para los aborígenes se '
                             'llamaban:',
                 'alternativas': ['Estancias',
                                  'Obrajes',
                                  'Chacras',
                                  'Haciendas',
                                  'Ingenios'],
                 'correcta': 'B'},
                {'pregunta': 'El impuesto colonial que consistía en el pago '
                             'de la quinta parte de la producción minera se '
                             'llamaba:',
                 'alternativas': ['Quinto Real',
                                  'Alcabala',
                                  'Media Anata',
                                  'Almojarifazgo',
                                  'Diezmo'],
                 'correcta': 'A'},
                {'pregunta': 'El impuesto colonial que constituía '
                             'contribución exclusiva de los aborígenes, en '
                             'señal de vasallaje al rey, era:',
                 'alternativas': ['El Diezmo',
                                  'La Alcabala',
                                  'El Tributo',
                                  'La Media Anata',
                                  'La Avería'],
                 'correcta': 'C'},
                {'pregunta': 'El impuesto colonial correspondiente a la '
                             'décima parte de la producción, entregada a la '
                             'Iglesia, era:',
                 'alternativas': ['La Media Anata',
                                  'El Almojarifazgo',
                                  'El Quinto Real',
                                  'El Diezmo',
                                  'El Tributo'],
                 'correcta': 'D'}],
  'resumen_visual': [{'titulo': 'Y 11.2 REPARTIMIENTO Y ENCOMIENDA / LA '
                                'CORONA Y EL CONSEJO DE INDIAS',
                      'items': ['El repartimiento fue el reparto de '
                                'indígenas entre los conquistadores para '
                                'trabajos y servicios.',
                                'La encomienda consistió en la entrega de un '
                                'grupo de indígenas a un encomendero, quien '
                                'recibía su tributo a cambio de protegerlos '
                                'y evangelizarlos.',
                                'No otorgaba propiedad sobre la tierra ni '
                                'sobre las personas, aunque en la práctica '
                                'derivó en abusos.',
                                'El rey era la suprema autoridad, '
                                'encabezando una monarquía absoluta '
                                'sustentada en el derecho divino.',
                                'Entre 1532 y 1824 gobernaron dos dinastías: '
                                'los Habsburgo (Carlos I a Carlos II) y los '
                                'Borbón (Felipe V a Fernando VII).',
                                'El Real y Supremo Consejo de Indias fue '
                                'creado en 1524 por Carlos V, como organismo '
                                'supremo de gobierno para las colonias.',
                                'El Consejo de Indias proponía al rey el '
                                'nombramiento de virreyes y, mediante el '
                                'Regio Patronato, de arzobispos y obispos.']},
                     {'titulo': 'LA CASA DE CONTRATACIÓN Y EL VIRREINATO / '
                                'LA REAL AUDIENCIA Y EL CORREGIMIE',
                      'items': ['La Casa de Contratación de Sevilla, creada '
                                'en 1503, controlaba el comercio entre '
                                'España y sus colonias.',
                                'El único puerto autorizado en América del '
                                'Sur para el comercio con España era el '
                                'puerto del Callao.',
                                'El virrey era el representante del rey, '
                                'jefe del poder político con residencia en '
                                'Lima.',
                                'Al finalizar su mandato, el virrey remitía '
                                'el informe de su gestión llamado «Pliego de '
                                'Mortaja».',
                                'Durante la colonia gobernaron 40 virreyes '
                                'en el Perú; el primero fue Blasco Núñez de '
                                'Vela y el último, José de la Serna.',
                                'La Real Audiencia era un tribunal colegiado '
                                'integrado por oidores, fiscales y '
                                'escribanos; asumía el gobierno ante '
                                'ausencia del virrey.',
                                'Existieron audiencias virreinales (Perú y '
                                'México), pretoriales y subordinadas '
                                '(Cusco).',
                                'El corregimiento fue creado para amparar a '
                                'los aborígenes de los abusos de los '
                                'encomenderos; el Perú tuvo 52 '
                                'corregimientos.',
                                'Los corregidores obligaban a los aborígenes '
                                'a recibir mercancías mediante el sistema '
                                'llamado «Reparto».']},
                     {'titulo': 'LA INTENDENCIA, EL CABILDO Y EL CACICAZGO / '
                                'CARACTERÍSTICAS DE LA ECONOMÍA ',
                      'items': ['La Intendencia, de origen francés, fue '
                                'establecida por Carlos III en 1784 tras la '
                                'rebelión de Túpac Amaru.',
                                'El Perú se dividió en 8 intendencias: Lima, '
                                'Trujillo, Arequipa, Huancavelica, Tarma, '
                                'Huamanga, Puno y Cusco.',
                                'El Cabildo o Ayuntamiento cumplía funciones '
                                'similares a las municipalidades actuales.',
                                'El Cacicazgo estaba representado por los '
                                'caciques, antiguos curacas, encargados de '
                                'cobrar tributos.',
                                'El intervencionismo fue el sistema impuesto '
                                'por la Corona para acentuar la dominación y '
                                'dependencia.',
                                'El mercantilismo buscaba que el Estado '
                                'consiguiera la mayor cantidad de oro y '
                                'plata mediante comercio monopólico.',
                                'El monopolio comercial prohibía a las '
                                'colonias comerciar con otros países; era '
                                'controlado por la Casa de Contratación.']},
                     {'titulo': 'LA MINERÍA COLONIAL / OTRAS ACTIVIDADES '
                                'ECONÓMICAS',
                      'items': ['La minería fue la actividad económica más '
                                'importante de la colonia.',
                                'El Cerro Rico de Potosí, descubierto en '
                                '1545, fue la mina más importante de plata.',
                                'Huancavelica fue la principal fuente de '
                                'azogue (mercurio), usado para el beneficio '
                                'de la plata.',
                                'La mita minera fue implantada por el virrey '
                                'Francisco de Toledo.',
                                'Los métodos de extracción incluían tajo '
                                'abierto (azogue), socavones (plata) y '
                                'lavaderos (oro).',
                                'En la agricultura, la tierra se hizo '
                                'individual y privada, formando grandes '
                                'haciendas; se incorporó el trigo y la vid.',
                                'La industria textil colonial se expresó en '
                                'los obrajes, que producían la «ropa de la '
                                'tierra».',
                                'En la colonia se acuñaron monedas como '
                                'pesos de oro, ducados, escudos y '
                                'doblones.']},
                     {'titulo': 'LOS IMPUESTOS COLONIALES / Y 11.3.4 LO '
                                'SOCIAL Y LO EDUCATIVO',
                      'items': ['El Almojarifazgo era el impuesto de aduanas '
                                'sobre productos importados y exportados.',
                                'La Alcabala se cobraba sobre las compras y '
                                'ventas de bienes.',
                                'El Tributo era una contribución exclusiva '
                                'de los aborígenes, en señal de vasallaje al '
                                'rey.',
                                'El Quinto Real consistía en el pago de la '
                                'quinta parte de la producción minera.',
                                'El Diezmo era la décima parte de la '
                                'producción entregada a la Iglesia.',
                                'Sociedad estamental basada en el origen '
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
                                'San Antonio Abad del Cusco.']}],
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
                 'alternativas': ['XVIII', 'XIX', 'XV', 'XVI', 'XVII'],
                 'correcta': 'A'},
                {'pregunta': 'La Ilustración es conocida también como:',
                 'alternativas': ['Barroco',
                                  'Edad Moderna',
                                  'Siglo de Oro',
                                  'Renacimiento',
                                  'Siglo de las Luces'],
                 'correcta': 'E'},
                {'pregunta': 'Para los ilustrados, la vida humana debía '
                             'guiarse por:',
                 'alternativas': ['La costumbre',
                                  'La razón',
                                  'La autoridad divina',
                                  'La fe',
                                  'La tradición'],
                 'correcta': 'B'},
                {'pregunta': 'La teoría de la división de poderes fue '
                             'formulada por:',
                 'alternativas': ['Diderot',
                                  'Voltaire',
                                  'Rousseau',
                                  'Locke',
                                  'Montesquieu'],
                 'correcta': 'E'},
                {'pregunta': 'El autor de «El contrato social» fue:',
                 'alternativas': ['Kant',
                                  'Hume',
                                  'Voltaire',
                                  'Rousseau',
                                  'Montesquieu'],
                 'correcta': 'D'},
                {'pregunta': 'El principio de la soberanía popular se '
                             'atribuye a:',
                 'alternativas': ['Adam Smith',
                                  'Rousseau',
                                  'Montesquieu',
                                  'Voltaire',
                                  'Bossuet'],
                 'correcta': 'B'},
                {'pregunta': 'Voltaire destacó especialmente por su defensa '
                             'de:',
                 'alternativas': ['La censura',
                                  'El feudalismo',
                                  'La monarquía absoluta',
                                  'La tolerancia',
                                  'El derecho divino'],
                 'correcta': 'D'},
                {'pregunta': 'El despotismo ilustrado se resume en la frase:',
                 'alternativas': ['«El poder al pueblo»',
                                  '«Dios lo quiere»',
                                  '«Libertad, igualdad, fraternidad»',
                                  '«El Estado soy yo»',
                                  '«Todo para el pueblo, pero sin el '
                                  'pueblo»'],
                 'correcta': 'E'},
                {'pregunta': 'El despotismo ilustrado mantuvo:',
                 'alternativas': ['La teocracia',
                                  'La democracia parlamentaria',
                                  'El poder absoluto del monarca',
                                  'La república',
                                  'El gobierno del pueblo'],
                 'correcta': 'C'},
                {'pregunta': 'Las ideas ilustradas influyeron directamente '
                             'en:',
                 'alternativas': ['El descubrimiento de América',
                                  'La caída de Constantinopla',
                                  'La Independencia de Estados Unidos y la '
                                  'Revolución Francesa',
                                  'El feudalismo',
                                  'Las Cruzadas'],
                 'correcta': 'C'},
                {'pregunta': 'Los ilustrados se opusieron principalmente a:',
                 'alternativas': ['La superstición y la tradición irracional',
                                  'El progreso',
                                  'La educación',
                                  'El comercio',
                                  'La razón y la ciencia'],
                 'correcta': 'A'},
                {'pregunta': 'Los monarcas del despotismo ilustrado '
                             'impulsaron reformas en:',
                 'alternativas': ['La abolición de la monarquía',
                                  'Educación, economía y administración',
                                  'La separación Iglesia-Estado plena',
                                  'La creación de repúblicas',
                                  'El sistema electoral'],
                 'correcta': 'B'},
                {'pregunta': 'La Ilustración cuestionó fundamentalmente el '
                             'poder basado en:',
                 'alternativas': ['Los parlamentos',
                                  'El voto popular',
                                  'El derecho divino de los reyes',
                                  'Las constituciones',
                                  'Los tratados internacionales'],
                 'correcta': 'C'},
                {'pregunta': 'El despotismo ilustrado puede definirse como '
                             'una forma de:',
                 'alternativas': ['República parlamentaria',
                                  'Democracia directa',
                                  'Anarquía',
                                  'Federalismo',
                                  'Absolutismo con reformas ilustradas'],
                 'correcta': 'E'},
                {'pregunta': 'La división de poderes propuesta comprende:',
                 'alternativas': ['Militar, civil y religioso',
                                  'Ejecutivo, legislativo y judicial',
                                  'Económico, político y social',
                                  'Central, regional y local',
                                  'Real, nobiliario y popular'],
                 'correcta': 'B'},
                {'pregunta': 'La Ilustración se desarrolló principalmente '
                             'en:',
                 'alternativas': ['Oceanía',
                                  'Europa',
                                  'África',
                                  'América',
                                  'Asia'],
                 'correcta': 'B'},
                {'pregunta': 'Los ilustrados confiaron en el progreso a '
                             'través de:',
                 'alternativas': ['El aislamiento',
                                  'La tradición',
                                  'La conquista',
                                  'La educación y la ciencia',
                                  'La guerra'],
                 'correcta': 'D'},
                {'pregunta': 'Una consecuencia política de la Ilustración '
                             'fue:',
                 'alternativas': ['El fortalecimiento del feudalismo',
                                  'El fin del comercio',
                                  'La expansión de la servidumbre',
                                  'El cuestionamiento del absolutismo',
                                  'El retorno al imperio romano'],
                 'correcta': 'D'},
                {'pregunta': '«El contrato social» plantea que el poder '
                             'emana de:',
                 'alternativas': ['La Iglesia',
                                  'El pueblo',
                                  'El ejército',
                                  'La nobleza',
                                  'Dios'],
                 'correcta': 'B'},
                {'pregunta': 'El pensamiento ilustrado se difundió '
                             'principalmente a través de:',
                 'alternativas': ['Los gremios',
                                  'Los torneos',
                                  'Los sermones',
                                  'Las cruzadas',
                                  'Los libros, salones y la Enciclopedia'],
                 'correcta': 'E'},
                {'pregunta': 'Las intendencias en la Colonia fueron creadas '
                             'en el reinado de: (UNSAAC Ordinario)',
                 'alternativas': ['Carlos VII',
                                  'Carlos V',
                                  'Carlos I',
                                  'Carlos IV',
                                  'Carlos III'],
                 'correcta': 'E'},
                {'pregunta': 'Una de las reformas político-administrativas '
                             'más importantes de Carlos III en '
                             'hispanoamérica fue: (UNSAAC Ordinario)',
                 'alternativas': ['La extensión del tributo a los caciques',
                                  'El censo de la población de Mitaya',
                                  'La implementación de la aduana',
                                  'La creación del Virreinato de Río de la '
                                  'Plata',
                                  'El incremento de la alcabala'],
                 'correcta': 'D'}],
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
                                  'Braganza',
                                  'Trastámara',
                                  'Habsburgo',
                                  'Saboya'],
                 'correcta': 'A'},
                {'pregunta': 'Las intendencias reemplazaron a:',
                 'alternativas': ['Los virreinatos',
                                  'Las audiencias',
                                  'Los corregimientos',
                                  'Los cabildos',
                                  'Las encomiendas'],
                 'correcta': 'C'},
                {'pregunta': 'Una consecuencia territorial de las reformas '
                             'borbónicas fue:',
                 'alternativas': ['La creación de la Capitanía de Cuba',
                                  'La anexión de Chile',
                                  'La independencia de México',
                                  'La ampliación del virreinato peruano',
                                  'La creación de los virreinatos de Nueva '
                                  'Granada y del Río de la Plata'],
                 'correcta': 'E'},
                {'pregunta': 'Las reformas borbónicas desplazaron de los '
                             'cargos públicos a los:',
                 'alternativas': ['Criollos',
                                  'Mestizos',
                                  'Esclavos',
                                  'Peninsulares',
                                  'Indígenas'],
                 'correcta': 'A'},
                {'pregunta': 'La rebelión de Juan Santos Atahualpa se inició '
                             'en el año:',
                 'alternativas': ['1742', '1780', '1814', '1781', '1821'],
                 'correcta': 'A'},
                {'pregunta': 'Juan Santos Atahualpa desarrolló su rebelión '
                             'en:',
                 'alternativas': ['El Cusco',
                                  'El altiplano',
                                  'La costa norte',
                                  'La selva central',
                                  'Lima'],
                 'correcta': 'D'},
                {'pregunta': 'Un rasgo singular de la rebelión de Juan '
                             'Santos Atahualpa fue que:',
                 'alternativas': ['Nunca fue derrotada militarmente',
                                  'Fue pacífica',
                                  'Se limitó a la costa',
                                  'Contó con apoyo español',
                                  'Fue rápidamente sofocada'],
                 'correcta': 'A'},
                {'pregunta': 'El verdadero nombre de Túpac Amaru II fue:',
                 'alternativas': ['Juan Santos Atahualpa',
                                  'José Gabriel Condorcanqui',
                                  'Mateo Pumacahua',
                                  'Francisco Santa Cruz',
                                  'Diego Cristóbal Túpac Amaru'],
                 'correcta': 'B'},
                {'pregunta': 'La revolución de Túpac Amaru II se inició con '
                             'la captura del corregidor:',
                 'alternativas': ['Antonio de Arriaga',
                                  "Ambrosio O'Higgins",
                                  'Francisco Santa Cruz',
                                  'Agustín de Jáuregui',
                                  'José Antonio de Areche'],
                 'correcta': 'A'},
                {'pregunta': 'La revolución de Túpac Amaru II se inició el:',
                 'alternativas': ['18 de mayo de 1781',
                                  '9 de diciembre de 1824',
                                  '28 de julio de 1821',
                                  '1 de agosto de 1814',
                                  '4 de noviembre de 1780'],
                 'correcta': 'E'},
                {'pregunta': 'Túpac Amaru II obtuvo su principal victoria en '
                             'la batalla de:',
                 'alternativas': ['Tinta',
                                  'Checacupe',
                                  'Junín',
                                  'Ayacucho',
                                  'Sangarará'],
                 'correcta': 'E'},
                {'pregunta': 'Túpac Amaru II fue ejecutado en la plaza del '
                             'Cusco el:',
                 'alternativas': ['2 de enero de 1782',
                                  '6 de agosto de 1824',
                                  '4 de noviembre de 1780',
                                  '18 de mayo de 1781',
                                  '28 de julio de 1821'],
                 'correcta': 'D'},
                {'pregunta': 'Entre las causas de la revolución de Túpac '
                             'Amaru II NO figura:',
                 'alternativas': ['Los repartos mercantiles',
                                  'La mita de Potosí',
                                  'Las reformas borbónicas',
                                  'La abolición de la esclavitud',
                                  'Los abusos de los corregidores'],
                 'correcta': 'D'},
                {'pregunta': 'Una consecuencia cultural de la derrota de '
                             'Túpac Amaru II fue:',
                 'alternativas': ['La creación de escuelas indígenas',
                                  'El reconocimiento de la nobleza inca',
                                  'La prohibición del quechua en documentos '
                                  'y de los Comentarios Reales',
                                  'La difusión del quechua',
                                  'La libertad de imprenta'],
                 'correcta': 'C'},
                {'pregunta': 'Túpac Amaru II era cacique de:',
                 'alternativas': ['Azángaro',
                                  'Tungasuca',
                                  'Acos',
                                  'Lampa',
                                  'Chincheros'],
                 'correcta': 'B'},
                {'pregunta': 'La obra prohibida tras la rebelión, escrita '
                             'por el Inca Garcilaso, fue:',
                 'alternativas': ['La Crónica del Perú',
                                  'Nueva Crónica y Buen Gobierno',
                                  'Los Comentarios Reales',
                                  'Historia del Nuevo Mundo',
                                  'Relación de antigüedades'],
                 'correcta': 'C'},
                {'pregunta': 'El impuesto colonial incrementado por las '
                             'reformas borbónicas fue:',
                 'alternativas': ['El quinto real',
                                  'La primicia',
                                  'La alcabala',
                                  'El diezmo',
                                  'El almojarifazgo'],
                 'correcta': 'C'},
                {'pregunta': 'Túpac Amaru II fue entregado a los españoles '
                             'por la traición de:',
                 'alternativas': ['Antonio de Arriaga',
                                  'Micaela Bastidas',
                                  'Diego Cristóbal',
                                  'Mateo Pumacahua',
                                  'Francisco Santa Cruz'],
                 'correcta': 'E'},
                {'pregunta': 'Las reformas borbónicas tuvieron como objetivo '
                             'principal:',
                 'alternativas': ['Fundar universidades',
                                  'Abolir la esclavitud',
                                  'Recuperar el control económico y político '
                                  'de las colonias',
                                  'Promover la independencia',
                                  'Otorgar autonomía a las colonias'],
                 'correcta': 'C'},
                {'pregunta': 'Juan Santos Atahualpa se proclamó descendiente '
                             'de:',
                 'alternativas': ['Los curacas costeños',
                                  'Los chancas',
                                  'Los chimúes',
                                  'Los reyes españoles',
                                  'Los incas'],
                 'correcta': 'E'},
                {'pregunta': 'La esposa y colíder de Túpac Amaru II en la '
                             'revolución fue:',
                 'alternativas': ['Tomasa Titu Condemayta',
                                  'Micaela Bastidas',
                                  'Cecilia Túpac Amaru',
                                  'Bartolina Sisa',
                                  'Marcela Castro'],
                 'correcta': 'B'},
                {'pregunta': 'Micaela Bastidas fue traicionada y capturada '
                             'por:',
                 'alternativas': ['Ventura Landaeta',
                                  'Antonio de Arriaga',
                                  'Antonio Oblitas',
                                  'José Antonio de Areche',
                                  'Francisco Santa Cruz'],
                 'correcta': 'A'},
                {'pregunta': 'El corregidor Antonio de Arriaga fue ejecutado '
                             'por:',
                 'alternativas': ['Diego Cristóbal Túpac Amaru',
                                  'Micaela Bastidas',
                                  'Antonio Oblitas, su antiguo esclavo',
                                  'Ventura Landaeta',
                                  'Francisco Santa Cruz'],
                 'correcta': 'C'},
                {'pregunta': 'Túpac Amaru II proclamó la libertad de los '
                             'esclavos negros el 16 de noviembre de:',
                 'alternativas': ['1781', '1783', '1776', '1780', '1778'],
                 'correcta': 'D'},
                {'pregunta': 'Tras la rebelión de Túpac Amaru II, la Corona '
                             'prohibió la difusión de una obra escrita por '
                             'el Inca Garcilaso de la Vega llamada:',
                 'alternativas': ['Historia General del Perú',
                                  'La Florida del Inca',
                                  'Los Comentarios Reales',
                                  'Suma y Narración de los Incas',
                                  'Nueva Corónica'],
                 'correcta': 'C'},
                {'pregunta': 'Túpac Amaru II era descendiente del último '
                             'inca de Vilcabamba, llamado:',
                 'alternativas': ['Huáscar',
                                  'Manco Inca',
                                  'Sayri Túpac',
                                  'Felipe Túpac Amaru',
                                  'Titu Cusi Yupanqui'],
                 'correcta': 'D'},
                {'pregunta': 'El movimiento liderado por Túpac Amaru II se '
                             'produjo en el siglo: (UNSAAC Ordinario)',
                 'alternativas': ['XVI', 'XVII', 'XVIII', 'XIX', 'XV'],
                 'correcta': 'C'},
                {'pregunta': 'Una consecuencia de la Revolución de Tupac '
                             'Amaru II fue la creación de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Los corregimientos',
                                  'Los departamentos',
                                  'Las intendencias',
                                  'Los nuevos virreinatos',
                                  'Las Juntas de Gobierno'],
                 'correcta': 'C'},
                {'pregunta': 'La revolución de José Gabriel Túpac Amaru '
                             'inició como: (UNSAAC Ordinario)',
                 'alternativas': ['Separatista - Emancipacionista',
                                  'Reformista - Independentista',
                                  'Reformista - Separatista',
                                  'Independentista - Separatista',
                                  'Emancipacionista - Reformista'],
                 'correcta': 'B'},
                {'pregunta': 'Durante la fase cusqueña, Túpac Amaru II '
                             'venció a los españoles en la batalla de: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Tinta',
                                  'Quiquijana',
                                  'Combapata',
                                  'Sangarará',
                                  'Checacupe'],
                 'correcta': 'D'}],
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
                {'titulo': '14.2 BATALLAS Y TRATADO DE VERSALLES (EE.UU.)',
                 'items': ['El Segundo Congreso Continental de {Filadelfia} '
                           '(1776) proclamó la independencia; el acta fue '
                           'redactada por {Thomas Jefferson}.',
                           'La batalla de {Saratoga} (1777) fue el primer '
                           'triunfo colono, motivando el apoyo de Francia, '
                           'España y los Países Bajos.',
                           'La batalla de {Yorktown} (1781), con apoyo '
                           'francés del mariscal Lafayette, selló la derrota '
                           'británica.',
                           'El {Tratado de Versalles} (noviembre de 1783) '
                           'fue el reconocimiento británico de la '
                           'independencia de las 13 colonias.',
                           'Entre las consecuencias está la creación de la '
                           'doctrina {Monroe}: «América para los '
                           'americanos».']},
                {'titulo': '14.3 LA REVOLUCIÓN FRANCESA',
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
                           '{liberales} por Europa y América.',
                           'El rey {Luis XVI} y su esposa {María Antonieta} '
                           'fueron ejecutados durante la etapa republicana '
                           'de la Revolución.']}],
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
                 'alternativas': ['Diez', 'Quince', 'Doce', 'Once', 'Trece'],
                 'correcta': 'E'},
                {'pregunta': 'La Declaración de Independencia de Estados '
                             'Unidos se firmó el:',
                 'alternativas': ['1 de enero de 1800',
                                  '28 de julio de 1821',
                                  '9 de diciembre de 1824',
                                  '14 de julio de 1789',
                                  '4 de julio de 1776'],
                 'correcta': 'E'},
                {'pregunta': 'El principal redactor de la Declaración de '
                             'Independencia norteamericana fue:',
                 'alternativas': ['Alexander Hamilton',
                                  'George Washington',
                                  'Benjamin Franklin',
                                  'Thomas Jefferson',
                                  'John Adams'],
                 'correcta': 'D'},
                {'pregunta': 'El primer presidente de Estados Unidos fue:',
                 'alternativas': ['James Madison',
                                  'Thomas Jefferson',
                                  'George Washington',
                                  'Benjamin Franklin',
                                  'John Adams'],
                 'correcta': 'C'},
                {'pregunta': 'El lema «no hay impuestos sin representación» '
                             'corresponde a:',
                 'alternativas': ['La Ilustración',
                                  'La Revolución Francesa',
                                  'La independencia del Perú',
                                  'Las reformas borbónicas',
                                  'La independencia de Estados Unidos'],
                 'correcta': 'E'},
                {'pregunta': 'El hecho que precipitó la rebelión de las '
                             'colonias inglesas fue:',
                 'alternativas': ['El bloqueo continental',
                                  'La Paz de Westfalia',
                                  'La batalla de Waterloo',
                                  'La toma de la Bastilla',
                                  'El Motín del Té de Boston'],
                 'correcta': 'E'},
                {'pregunta': 'La Revolución Francesa se inició en el año:',
                 'alternativas': ['1804', '1799', '1776', '1810', '1789'],
                 'correcta': 'E'},
                {'pregunta': 'El hecho simbólico del inicio de la Revolución '
                             'Francesa fue:',
                 'alternativas': ['El golpe de Napoleón',
                                  'La huida a Varennes',
                                  'La reunión de los Estados Generales',
                                  'La toma de la Bastilla',
                                  'La ejecución de Luis XVI'],
                 'correcta': 'D'},
                {'pregunta': 'El lema de la Revolución Francesa fue:',
                 'alternativas': ['«Todo para el pueblo, sin el pueblo»',
                                  '«Libertad, igualdad, fraternidad»',
                                  '«El Estado soy yo»',
                                  '«No hay impuestos sin representación»',
                                  '«Paz, orden y progreso»'],
                 'correcta': 'B'},
                {'pregunta': 'El documento fundamental proclamado por la '
                             'Revolución Francesa fue:',
                 'alternativas': ['La Carta Magna',
                                  'Las Siete Partidas',
                                  'El Bill of Rights',
                                  'La Declaración de los Derechos del Hombre '
                                  'y del Ciudadano',
                                  'El Código de Hammurabi'],
                 'correcta': 'D'},
                {'pregunta': 'La etapa del Terror durante la Revolución '
                             'Francesa estuvo dirigida por:',
                 'alternativas': ['Robespierre',
                                  'Lafayette',
                                  'Napoleón',
                                  'Danton exclusivamente',
                                  'Luis XVI'],
                 'correcta': 'A'},
                {'pregunta': 'El Directorio francés terminó con:',
                 'alternativas': ['La batalla de Waterloo',
                                  'La restauración borbónica',
                                  'La toma de la Bastilla',
                                  'La ejecución de Robespierre',
                                  'El golpe de Estado de Napoleón'],
                 'correcta': 'E'},
                {'pregunta': 'Una consecuencia política central de la '
                             'Revolución Francesa fue:',
                 'alternativas': ['La expansión de la servidumbre',
                                  'La restauración del feudalismo',
                                  'El fin del absolutismo y del régimen '
                                  'feudal',
                                  'El fortalecimiento del absolutismo',
                                  'El retorno de la monarquía absoluta '
                                  'permanente'],
                 'correcta': 'C'},
                {'pregunta': 'La independencia de Estados Unidos influyó en '
                             'Hispanoamérica al:',
                 'alternativas': ['Enviar tropas al Perú',
                                  'Firmar tratados de alianza',
                                  'Servir de ejemplo a los movimientos '
                                  'independentistas',
                                  'Abolir la esclavitud',
                                  'Financiar los ejércitos libertadores'],
                 'correcta': 'C'},
                {'pregunta': 'El sistema de gobierno adoptado por Estados '
                             'Unidos fue:',
                 'alternativas': ['Monarquía constitucional',
                                  'Imperio',
                                  'República parlamentaria',
                                  'República federal y presidencialista',
                                  'Confederación monárquica'],
                 'correcta': 'D'},
                {'pregunta': 'Entre las causas de la Revolución Francesa '
                             'figura:',
                 'alternativas': ['La abundancia económica',
                                  'La desigualdad entre los estamentos',
                                  'La ausencia de impuestos',
                                  'La unidad social',
                                  'La expansión colonial'],
                 'correcta': 'B'},
                {'pregunta': 'La corriente de pensamiento que influyó '
                             'decisivamente en ambas revoluciones fue:',
                 'alternativas': ['El Renacimiento',
                                  'La Ilustración',
                                  'El Romanticismo',
                                  'El Positivismo',
                                  'La Escolástica'],
                 'correcta': 'B'},
                {'pregunta': 'La toma de la Bastilla ocurrió el:',
                 'alternativas': ['9 de diciembre',
                                  '4 de julio',
                                  '1 de mayo',
                                  '14 de julio',
                                  '28 de julio'],
                 'correcta': 'D'},
                {'pregunta': 'El órgano revolucionario francés que juzgó y '
                             'ejecutó al rey fue:',
                 'alternativas': ['El Directorio',
                                  'La Asamblea Nacional',
                                  'El Consulado',
                                  'Los Estados Generales',
                                  'La Convención'],
                 'correcta': 'E'},
                {'pregunta': 'La sociedad francesa previa a la revolución '
                             'estaba dividida en:',
                 'alternativas': ['Cuatro castas',
                                  'Sin divisiones legales',
                                  'Cinco estamentos',
                                  'Tres estamentos',
                                  'Dos clases'],
                 'correcta': 'D'},
                {'pregunta': 'El reconocimiento de la independencia de las '
                             'Trece Colonias de Norte América, por el Rey '
                             'Jorge III, se estableció en el Tratado de: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Versalles',
                                  'Saratoga',
                                  'Yorktown',
                                  'Filadelfia',
                                  'Lexington'],
                 'correcta': 'A'},
                {'pregunta': 'La búsqueda de igualdad de poderes: Ejecutivo, '
                             'Legislativo y Judicial surge a consecuencia '
                             'de: (UNSAAC Ordinario)',
                 'alternativas': ['Revolución Francesa',
                                  'Tratado de Versalles',
                                  'Independencia de las Trece Colonias',
                                  'Primera guerra mundial',
                                  'Segunda guerra mundial'],
                 'correcta': 'A'},
                {'pregunta': 'Una de las consecuencias de la Revolución '
                             'Francesa fue: (UNSAAC Ordinario)',
                 'alternativas': ['La destrucción del régimen feudal en '
                                  'Francia',
                                  'El triunfo en la Batalla de Saratoga',
                                  'La creación del sistema de gobierno '
                                  'dictatorial',
                                  'El desarrollo económico del imperialismo '
                                  'inglés',
                                  'La creación de los estados independistas '
                                  'en Europa del Norte'],
                 'correcta': 'A'},
                {'pregunta': 'El Segundo Congreso Continental de Filadelfia, '
                             'que proclamó la independencia en 1776, tuvo su '
                             'acta redactada por:',
                 'alternativas': ['George Washington',
                                  'Alexander Hamilton',
                                  'Benjamin Franklin',
                                  'Thomas Jefferson',
                                  'John Adams'],
                 'correcta': 'D'},
                {'pregunta': 'La batalla que constituyó el primer triunfo de '
                             'los colonos norteamericanos, motivando el '
                             'apoyo de Francia y España, fue:',
                 'alternativas': ['Yorktown',
                                  'Trenton',
                                  'Bunker Hill',
                                  'Saratoga',
                                  'Lexington'],
                 'correcta': 'D'},
                {'pregunta': 'La batalla que selló la derrota británica '
                             'definitiva en la independencia de Estados '
                             'Unidos fue:',
                 'alternativas': ['Trenton',
                                  'Lexington',
                                  'Yorktown',
                                  'Concord',
                                  'Saratoga'],
                 'correcta': 'C'},
                {'pregunta': 'El tratado por el cual Inglaterra reconoció la '
                             'independencia de las Trece Colonias, en 1783, '
                             'fue el Tratado de:',
                 'alternativas': ['Amiens',
                                  'Westfalia',
                                  'París',
                                  'Versalles',
                                  'Utrecht'],
                 'correcta': 'D'},
                {'pregunta': 'La doctrina que estableció el principio '
                             '«América para los americanos», como '
                             'consecuencia de la independencia de EE.UU., '
                             'fue la doctrina:',
                 'alternativas': ['Monroe',
                                  'Roosevelt',
                                  'Wilson',
                                  'Truman',
                                  'Taft'],
                 'correcta': 'A'},
                {'pregunta': 'Durante la Revolución Francesa, el rey Luis '
                             'XVI y su esposa fueron ejecutados en la etapa:',
                 'alternativas': ['Napoleónica',
                                  'Monárquica',
                                  'Consular',
                                  'Termidoriana exclusiva',
                                  'Republicana'],
                 'correcta': 'E'},
                {'pregunta': 'La esposa del rey Luis XVI, ejecutada durante '
                             'la Revolución Francesa, se llamaba:',
                 'alternativas': ['María Antonieta',
                                  'Josefina de Beauharnais',
                                  'Isabel de Borbón',
                                  'María Teresa',
                                  'Ana de Austria'],
                 'correcta': 'A'}],
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
                     {'titulo': 'BATALLAS Y TRATADO DE VERSALLES (EE.UU.)',
                      'items': ['El Segundo Congreso Continental de '
                                'Filadelfia (1776) proclamó la '
                                'independencia; el acta fue redactada por '
                                'Thomas Jefferson.',
                                'La batalla de Saratoga (1777) fue el primer '
                                'triunfo colono, motivando el apoyo de '
                                'Francia, España y los Países Bajos.',
                                'La batalla de Yorktown (1781), con apoyo '
                                'francés del mariscal Lafayette, selló la '
                                'derrota británica.',
                                'El Tratado de Versalles (noviembre de 1783) '
                                'fue el reconocimiento británico de la '
                                'independencia de las 13 colonias.',
                                'Entre las consecuencias está la creación de '
                                'la doctrina Monroe: «América para los '
                                'americanos».']},
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
                                'liberales por Europa y América.',
                                'El rey Luis XVI y su esposa María Antonieta '
                                'fueron ejecutados durante la etapa '
                                'republicana de la Revolución.']}],
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
  'secciones': [{'titulo': '15.1 FACTORES EXTERNOS E INTERNOS DE LA '
                           'INDEPENDENCIA',
                 'items': ['Entre los factores {externos} están la '
                           'Independencia de las Trece Colonias, la '
                           'Revolución Francesa, y la crisis de la monarquía '
                           'absolutista española.',
                           'Entre los factores {internos} están la '
                           'explotación del sistema feudal colonial y las '
                           '{Reformas Borbónicas}.',
                           'Otro factor interno fueron las contradicciones '
                           'entre españoles, {criollos}, mestizos y '
                           'aborígenes.']},
                {'titulo': '15.2 LA INVASIÓN NAPOLEÓNICA A ESPAÑA '
                           '(1808-1813)',
                 'items': ['Tras la derrota de {Trafalgar} en 1805, Napoleón '
                           'bloqueó los puertos europeos contra Inglaterra.',
                           'En Bayona, {Napoleón} obligó a Carlos IV a '
                           'abdicar en favor de Fernando VII, y luego en '
                           'favor de su hermano {José Bonaparte}.',
                           'Este episodio se conoció como la «{farsa de '
                           'Bayona}», que dio inicio a la Guerra de '
                           'Independencia española (1808-1814).',
                           'La invasión napoleónica generó un {vacío de '
                           'poder} en las colonias, facilitando la '
                           'instauración de las Juntas de Gobierno '
                           'criollas.']},
                {'titulo': '15.3 LAS JUNTAS DE GOBIERNO EN AMÉRICA '
                           '(1809-1810)',
                 'items': ['La {Constitución de Cádiz} fue jurada el 19 de '
                           'marzo de 1812, bajo el título de Constitución de '
                           'la Monarquía Española.',
                           'La Junta de {Chuquisaca} (25 de mayo de 1809) '
                           'fue dirigida por Domingo Murillo.',
                           'La Junta de {Caracas} (19 de abril de 1810) fue '
                           'dirigida por Francisco de Miranda; la de Buenos '
                           'Aires (25 de mayo de 1810), por Cornelio '
                           'Saavedra.',
                           'La Junta de {Santiago} (18 de setiembre de 1810) '
                           "fue dirigida por Bernardo de O'Higgins; el "
                           'virreinato del Perú fue la excepción sin junta '
                           'propia.']},
                {'titulo': '15.4 SAN MARTÍN: LIBERACIÓN DE ARGENTINA Y CHILE',
                 'items': ['En 1817, San Martín organizó el «{Ejército de '
                           'los Andes}» en Mendoza, atravesando la '
                           'cordillera por el abra de {Uspallata}.',
                           'En la batalla de {Chacabuco} (12 de febrero de '
                           '1817) venció al capitán Marco de Pont.',
                           'Tras la derrota parcial en Cancha Rayada, la '
                           'batalla de {Maipú} (5 de abril de 1818) selló la '
                           'independencia de Chile.']},
                {'titulo': '15.5 SAN MARTÍN: EXPEDICIÓN AL PERÚ',
                 'items': ['San Martín contrató al mercenario inglés {Lord '
                           'Thomas Cochrane} para operaciones navales.',
                           'Las tropas patriotas desembarcaron en la Bahía '
                           'de {Paracas} el 8 de setiembre de 1820.',
                           'El general {Álvarez de Arenales} dirigió la '
                           'expedición a la sierra (Huamanga, Huancavelica, '
                           'Tarma, Junín).',
                           'En el {Motín de Aznapuquio}, oficiales españoles '
                           'destituyeron al virrey Joaquín de la Pezuela.',
                           '{José de la Serna}, nombrado virrey, se retiró '
                           'al Cusco tras la fracasada Conferencia de '
                           'Punchauca.']},
                {'titulo': '15.6 PROCLAMACIÓN DE LA INDEPENDENCIA (1821)',
                 'items': ['El 9 de julio de 1821, San Martín ingresó a '
                           '{Lima}.',
                           'El 15 de julio de 1821 se redactó el Acta de '
                           'Independencia, a cargo de {Manuel Pérez de '
                           'Tudela}.',
                           'El {28 de julio} de 1821, San Martín proclamó '
                           'formalmente la independencia del Perú.',
                           'San Martín encargó el diseño de la primera '
                           'bandera peruana a {Charles Wood Taylor}.']},
                {'titulo': '15.7 BOLÍVAR: LLEGADA Y FEDERACIÓN DE LOS ANDES',
                 'items': ['Antes de llegar al Perú, {Bolívar} dirigió las '
                           'independencias de Nueva Granada (Boyacá, 1819), '
                           'Venezuela (Carabobo, 1821) y Quito (Pichincha, '
                           '1822).',
                           '{Simón Bolívar} llegó al Perú el 1 de setiembre '
                           'de 1823, siendo presidente Bernardo de Torre '
                           'Tagle.',
                           'Nombró como su secretario a {Faustino Sánchez '
                           'Carrión}, «el solitario de Sayán».',
                           'Bolívar intentó crear la {Federación de los '
                           'Andes} con Gran Colombia, Perú y Bolivia.',
                           'Promulgó la {Constitución Vitalicia} de 1826, '
                           'rechazada por los criollos de los tres países.']},
                {'titulo': '15.8 LAS BATALLAS DE JUNÍN Y AYACUCHO',
                 'items': ['La batalla de {Junín} (6 de agosto de 1824) fue '
                           'un choque de caballería sin disparos, llamada la '
                           '«{batalla sin humo}».',
                           'En Junín, el patriota {Necochea} enfrentó al '
                           'realista Canterac.',
                           'La batalla de {Ayacucho} (9 de diciembre de '
                           '1824) se libró en las pampas al pie del cerro '
                           '{Condorcunca}.',
                           'En Ayacucho, el patriota {Antonio José de Sucre} '
                           '(con Agustín Gamarra como Jefe de Estado Mayor) '
                           'venció al virrey La Serna.']},
                {'titulo': '15.9 LA CAPITULACIÓN DE AYACUCHO',
                 'items': ['La {Capitulación de Ayacucho}, que consolidó la '
                           'independencia, se firmó el 9 de diciembre de '
                           '1824 en el mismo campo de batalla.',
                           'Fue suscrita entre {Antonio José de Sucre} '
                           '(Perú) y José de Canterac (bando realista).',
                           'La capitulación constaba de {18} cláusulas; '
                           'España reconoció la independencia del Perú.']}],
  'cuadros': [{'titulo': '15. BATALLAS DECISIVAS',
               'encabezados': ['Batalla', 'Fecha', 'Jefe patriota'],
               'filas': [['{Junín}', '{6} agosto 1824', '{Bolívar}'],
                         ['{Ayacucho}', '{9} diciembre 1824', '{Sucre}']]}],
  'preguntas': [{'pregunta': 'La invasión napoleónica a España se produjo '
                             'en:',
                 'alternativas': ['1789', '1824', '1812', '1808', '1820'],
                 'correcta': 'D'},
                {'pregunta': 'Napoleón colocó en el trono español a:',
                 'alternativas': ['José Bonaparte',
                                  'Fernando VII',
                                  'Luis XVIII',
                                  'Godoy',
                                  'Carlos IV'],
                 'correcta': 'A'},
                {'pregunta': 'La Constitución liberal española de 1812 se '
                             'conoce como Constitución de:',
                 'alternativas': ['Aranjuez',
                                  'Madrid',
                                  'Bayona',
                                  'Cádiz',
                                  'Sevilla'],
                 'correcta': 'D'},
                {'pregunta': 'San Martín desembarcó en el Perú en la bahía '
                             'de:',
                 'alternativas': ['Paracas',
                                  'Ancón',
                                  'Callao',
                                  'Pisco',
                                  'Huacho'],
                 'correcta': 'A'},
                {'pregunta': 'El desembarco de San Martín en el Perú ocurrió '
                             'el:',
                 'alternativas': ['28 de julio de 1821',
                                  '6 de agosto de 1824',
                                  '8 de septiembre de 1820',
                                  '20 de septiembre de 1822',
                                  '9 de diciembre de 1824'],
                 'correcta': 'C'},
                {'pregunta': 'La Independencia del Perú fue proclamada el:',
                 'alternativas': ['4 de julio de 1776',
                                  '8 de septiembre de 1820',
                                  '28 de julio de 1821',
                                  '9 de diciembre de 1824',
                                  '6 de agosto de 1824'],
                 'correcta': 'C'},
                {'pregunta': 'San Martín asumió el gobierno del Perú con el '
                             'título de:',
                 'alternativas': ['Virrey',
                                  'Presidente',
                                  'Libertador',
                                  'Protector',
                                  'Dictador'],
                 'correcta': 'D'},
                {'pregunta': 'Institución cultural creada por San Martín:',
                 'alternativas': ['La Biblioteca Nacional',
                                  'El Museo Nacional',
                                  'La Universidad de San Marcos',
                                  'La Academia de la Lengua',
                                  'El Archivo General'],
                 'correcta': 'A'},
                {'pregunta': 'La conferencia entre San Martín y Bolívar se '
                             'realizó en:',
                 'alternativas': ['Quito',
                                  'Lima',
                                  'Bogotá',
                                  'Guayaquil',
                                  'Trujillo'],
                 'correcta': 'D'},
                {'pregunta': 'Bolívar llegó al Perú en el año:',
                 'alternativas': ['1823', '1822', '1824', '1821', '1820'],
                 'correcta': 'A'},
                {'pregunta': 'La batalla de Junín se libró el:',
                 'alternativas': ['2 de mayo de 1866',
                                  '6 de agosto de 1824',
                                  '8 de septiembre de 1820',
                                  '9 de diciembre de 1824',
                                  '28 de julio de 1821'],
                 'correcta': 'B'},
                {'pregunta': 'Un rasgo distintivo de la batalla de Junín fue '
                             'que:',
                 'alternativas': ['Duró tres días',
                                  'Participó la marina',
                                  'Se libró sin usar armas de fuego',
                                  'Intervino artillería pesada',
                                  'Se realizó de noche'],
                 'correcta': 'C'},
                {'pregunta': 'La batalla de Ayacucho fue dirigida por:',
                 'alternativas': ['La Mar',
                                  'Antonio José de Sucre',
                                  'San Martín',
                                  'Santa Cruz',
                                  'Simón Bolívar'],
                 'correcta': 'B'},
                {'pregunta': 'La batalla de Ayacucho se libró el:',
                 'alternativas': ['3 de octubre de 1824',
                                  '6 de agosto de 1824',
                                  '9 de diciembre de 1824',
                                  '28 de julio de 1821',
                                  '20 de enero de 1825'],
                 'correcta': 'C'},
                {'pregunta': 'La Capitulación de Ayacucho fue firmada por el '
                             'virrey:',
                 'alternativas': ['Abascal',
                                  'Pezuela',
                                  'José de la Serna',
                                  "O'Higgins",
                                  'Toledo'],
                 'correcta': 'C'},
                {'pregunta': 'Antes de llegar al Perú, San Martín liberó:',
                 'alternativas': ['Venezuela',
                                  'Ecuador',
                                  'Chile',
                                  'Colombia',
                                  'Bolivia'],
                 'correcta': 'C'},
                {'pregunta': 'Ante el vacío de poder por la invasión '
                             'napoleónica se formaron:',
                 'alternativas': ['Las juntas de gobierno',
                                  'Las intendencias',
                                  'Las audiencias',
                                  'Los cabildos abiertos únicamente',
                                  'Los virreinatos'],
                 'correcta': 'A'},
                {'pregunta': 'Bolívar recibió en el Perú poderes de:',
                 'alternativas': ['Gobernador',
                                  'Protector',
                                  'Dictador',
                                  'Regente',
                                  'Presidente constitucional'],
                 'correcta': 'C'},
                {'pregunta': 'La proclamación de la Independencia se realizó '
                             'en:',
                 'alternativas': ['Trujillo',
                                  'El Cusco',
                                  'Pisco',
                                  'La plaza de armas de Lima',
                                  'Huaura'],
                 'correcta': 'D'},
                {'pregunta': 'La batalla que selló definitivamente la '
                             'independencia del Perú fue:',
                 'alternativas': ['Pichincha',
                                  'Chacabuco',
                                  'Maipú',
                                  'Junín',
                                  'Ayacucho'],
                 'correcta': 'E'},
                {'pregunta': 'El Acta de la Independencia del Perú en 1821 '
                             'fue redactada por: (UNSAAC Ordinario)',
                 'alternativas': ['Francisco Javier Mariátegui',
                                  'Faustino Sánchez Carrión',
                                  'José de San Martín',
                                  'Francisco Javier de Luna Pizarro',
                                  'Manuel Pérez de Tudela'],
                 'correcta': 'E'},
                {'pregunta': 'Simón Bolívar, antes de llegar al Perú, '
                             'independizó Venezuela con la Batalla de: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Boyacá',
                                  'Cancha Rayada',
                                  'Chacabuco',
                                  'Carabobo',
                                  'Pichincha'],
                 'correcta': 'D'},
                {'pregunta': 'Las juntas de Gobierno en América Hispana se '
                             'formaron a consecuencia de: (UNSAAC Ordinario)',
                 'alternativas': ['El cautiverio del Rey de España',
                                  'La vuelta del rey derrotado al trono de '
                                  'España',
                                  'El pronunciamiento del virrey Francisco '
                                  'de Abascal',
                                  'Las guerras de independencia del Perú',
                                  'La promulgación de la constitución de '
                                  'Cádiz en 1812'],
                 'correcta': 'A'},
                {'pregunta': 'La independencia de Venezuela se logró en la '
                             'batalla de: (UNSAAC Ordinario)',
                 'alternativas': ['Pichincha',
                                  'Carabobo',
                                  'Boyacá',
                                  'Maipú',
                                  'Cancha Rayada'],
                 'correcta': 'B'},
                {'pregunta': 'El establecimiento de la Junta de Gobierno en '
                             'Lima no fue posible, debido a la acción del '
                             'Virrey: (UNSAAC Ordinario)',
                 'alternativas': ['Francisco de Toledo',
                                  'Joaquín de La Pezuela',
                                  'José de la Serna',
                                  'Fernando de Abascal y Sousa',
                                  'Agustín de Jáuregui'],
                 'correcta': 'D'},
                {'pregunta': 'En la coyuntura internacional que España '
                             'afrontó para la formación de las Juntas de '
                             'Gobierno en Hispanoamérica, fue debido a: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Inicios de la Primera Revolución '
                                  'Industrial',
                                  'La revolución burguesa en España',
                                  'La invasión de Napoleón a España',
                                  'La invasión de Napoleón a Portugal',
                                  'La declaración de guerra de Napoleón '
                                  'Bonaparte'],
                 'correcta': 'C'},
                {'pregunta': 'Simón Bolívar llegó al Perú el año 1823 y '
                             'estableció su cuartel general en: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Cajamarca',
                                  'Pativilca',
                                  'Huaura',
                                  'Chota',
                                  'Cutervo'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los factores externos de la '
                             'independencia hispanoamericana está la '
                             'Independencia de las Trece Colonias y:',
                 'alternativas': ['Las Reformas Borbónicas',
                                  'La Revolución Francesa',
                                  'La explotación feudal colonial',
                                  'La crisis social interna',
                                  'El sistema de castas'],
                 'correcta': 'B'},
                {'pregunta': 'En Bayona, Napoleón obligó a Carlos IV a '
                             'abdicar en favor de Fernando VII, y luego en '
                             'favor de:',
                 'alternativas': ['El almirante Nelson',
                                  'José Bonaparte',
                                  'Carlos III',
                                  'El general Wellington',
                                  'El almirante Villeneuve'],
                 'correcta': 'B'},
                {'pregunta': 'El episodio en que Napoleón usurpó la corona '
                             'española para su hermano se conoció como:',
                 'alternativas': ['La farsa de Bayona',
                                  'La conjura de El Escorial',
                                  'La crisis de Madrid',
                                  'El motín de Aranjuez',
                                  'El pacto de familia'],
                 'correcta': 'A'},
                {'pregunta': 'La Constitución de Cádiz fue jurada el 19 de '
                             'marzo de:',
                 'alternativas': ['1814', '1810', '1820', '1812', '1808'],
                 'correcta': 'D'},
                {'pregunta': 'La Junta de Gobierno de Caracas, formada en '
                             '1810, fue dirigida por:',
                 'alternativas': ['Domingo Murillo',
                                  'Francisco de Miranda',
                                  "Bernardo de O'Higgins",
                                  'Cornelio Saavedra',
                                  'Antonio Nariño'],
                 'correcta': 'B'},
                {'pregunta': 'El único virreinato sudamericano que no formó '
                             'junta de gobierno propia entre 1809 y 1810 '
                             'fue:',
                 'alternativas': ['Nueva Granada',
                                  'Venezuela',
                                  'Río de la Plata',
                                  'El Perú',
                                  'Chile'],
                 'correcta': 'D'},
                {'pregunta': 'El Ejército de los Andes, organizado por San '
                             'Martín en Mendoza, atravesó la cordillera por '
                             'el abra de:',
                 'alternativas': ['Anticona',
                                  'Málaga',
                                  'Uspallata',
                                  'Porculla',
                                  'La Raya'],
                 'correcta': 'C'},
                {'pregunta': 'La batalla que selló definitivamente la '
                             'independencia de Chile, el 5 de abril de 1818, '
                             'fue la de:',
                 'alternativas': ['Talcahuano',
                                  'Rancagua',
                                  'Cancha Rayada',
                                  'Maipú',
                                  'Chacabuco'],
                 'correcta': 'D'},
                {'pregunta': 'El mercenario inglés contratado por San Martín '
                             'para realizar operaciones navales en la '
                             'expedición al Perú fue:',
                 'alternativas': ['Lord Byron',
                                  'Lord Cochrane',
                                  'Lord Wellington',
                                  'Lord Nelson',
                                  'Lord Canning'],
                 'correcta': 'B'},
                {'pregunta': 'Las tropas patriotas de San Martín '
                             'desembarcaron en la Bahía de Paracas el 8 de '
                             'setiembre de:',
                 'alternativas': ['1818', '1817', '1822', '1820', '1821'],
                 'correcta': 'D'},
                {'pregunta': 'El motín en el cual oficiales del ejército '
                             'español destituyeron al virrey Joaquín de la '
                             'Pezuela se llamó:',
                 'alternativas': ['Motín de Cañete',
                                  'Sublevación de La Serna',
                                  'Conferencia de Punchauca',
                                  'Capitulación de Ayacucho',
                                  'Motín de Aznapuquio'],
                 'correcta': 'E'},
                {'pregunta': 'El Acta de Independencia del Perú fue '
                             'redactada por:',
                 'alternativas': ['José de la Riva Agüero',
                                  'Bernardo de Torre Tagle',
                                  'Faustino Sánchez Carrión',
                                  'José de San Martín',
                                  'Manuel Pérez de Tudela'],
                 'correcta': 'E'},
                {'pregunta': 'San Martín encargó el diseño de la primera '
                             'bandera del Perú a:',
                 'alternativas': ['José Bernardo de Tagle',
                                  'Bernardo de Monteagudo',
                                  'Manuel Pérez de Tudela',
                                  'José de la Serna',
                                  'Charles Wood Taylor'],
                 'correcta': 'E'},
                {'pregunta': 'Antes de llegar al Perú, Simón Bolívar dirigió '
                             'la independencia de Nueva Granada en la '
                             'batalla de:',
                 'alternativas': ['Carabobo',
                                  'Pichincha',
                                  'Boyacá',
                                  'Junín',
                                  'Ayacucho'],
                 'correcta': 'C'},
                {'pregunta': 'El secretario de Bolívar, conocido como «el '
                             'solitario de Sayán», fue:',
                 'alternativas': ['Antonio José de Sucre',
                                  'Agustín Gamarra',
                                  'José de la Riva Agüero',
                                  'Bernardo de Torre Tagle',
                                  'Faustino Sánchez Carrión'],
                 'correcta': 'E'},
                {'pregunta': 'El proyecto de Bolívar de unir Gran Colombia, '
                             'Perú y Bolivia bajo un solo Estado se llamó:',
                 'alternativas': ['Unión Bolivariana',
                                  'Confederación Perú-Boliviana',
                                  'Federación de los Andes',
                                  'Estados Unidos de los Andes',
                                  'Gran Colombia Andina'],
                 'correcta': 'C'},
                {'pregunta': 'La batalla de Junín, llamada «la batalla sin '
                             'humo» por ser un choque solo de sable y lanza, '
                             'ocurrió el:',
                 'alternativas': ['7 de agosto de 1819',
                                  '9 de diciembre de 1824',
                                  '24 de junio de 1821',
                                  '28 de julio de 1821',
                                  '6 de agosto de 1824'],
                 'correcta': 'E'},
                {'pregunta': 'El general patriota que comandó a las tropas '
                             'en la batalla de Ayacucho fue:',
                 'alternativas': ['Andrés de Santa Cruz',
                                  'Agustín Gamarra',
                                  'José de San Martín',
                                  'Antonio José de Sucre',
                                  'Simón Bolívar'],
                 'correcta': 'D'},
                {'pregunta': 'La batalla de Ayacucho se libró en las pampas '
                             'al pie del cerro:',
                 'alternativas': ['Condorcunca',
                                  'Coropuna',
                                  'Huascarán',
                                  'Misti',
                                  'Salkantay'],
                 'correcta': 'A'},
                {'pregunta': 'La Capitulación de Ayacucho, que consolidó la '
                             'independencia del Perú, fue suscrita entre '
                             'Antonio José de Sucre y:',
                 'alternativas': ['Joaquín de la Pezuela',
                                  'José de la Serna',
                                  'Agustín Gamarra',
                                  'Simón Bolívar',
                                  'José Canterac'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'FACTORES EXTERNOS E INTERNOS DE LA '
                                'INDEPENDENCIA / LA INVASIÓN NAPOLEÓNICA ',
                      'items': ['Entre los factores externos están la '
                                'Independencia de las Trece Colonias, la '
                                'Revolución Francesa, y la crisis de la '
                                'monarquía absolutista española.',
                                'Entre los factores internos están la '
                                'explotación del sistema feudal colonial y '
                                'las Reformas Borbónicas.',
                                'Otro factor interno fueron las '
                                'contradicciones entre españoles, criollos, '
                                'mestizos y aborígenes.',
                                'Tras la derrota de Trafalgar en 1805, '
                                'Napoleón bloqueó los puertos europeos '
                                'contra Inglaterra.',
                                'En Bayona, Napoleón obligó a Carlos IV a '
                                'abdicar en favor de Fernando VII, y luego '
                                'en favor de su hermano José Bonaparte.',
                                'Este episodio se conoció como la «farsa de '
                                'Bayona», que dio inicio a la Guerra de '
                                'Independencia española (1808-1814).',
                                'La invasión napoleónica generó un vacío de '
                                'poder en las colonias, facilitando la '
                                'instauración de las Juntas de Gobierno '
                                'criollas.']},
                     {'titulo': 'LAS JUNTAS DE GOBIERNO EN AMÉRICA '
                                '(1809-1810) / SAN MARTÍN: LIBERACIÓN DE A',
                      'items': ['La Constitución de Cádiz fue jurada el 19 '
                                'de marzo de 1812, bajo el título de '
                                'Constitución de la Monarquía Española.',
                                'La Junta de Chuquisaca (25 de mayo de 1809) '
                                'fue dirigida por Domingo Murillo.',
                                'La Junta de Caracas (19 de abril de 1810) '
                                'fue dirigida por Francisco de Miranda; la '
                                'de Buenos Aires (25 de mayo de 1810), por '
                                'Cornelio Saavedra.',
                                'La Junta de Santiago (18 de setiembre de '
                                '1810) fue dirigida por Bernardo de '
                                "O'Higgins; el virreinato del Perú fue la "
                                'excepción sin junta propia.',
                                'En 1817, San Martín organizó el «Ejército '
                                'de los Andes» en Mendoza, atravesando la '
                                'cordillera por el abra de Uspallata.',
                                'En la batalla de Chacabuco (12 de febrero '
                                'de 1817) venció al capitán Marco de Pont.',
                                'Tras la derrota parcial en Cancha Rayada, '
                                'la batalla de Maipú (5 de abril de 1818) '
                                'selló la independencia de Chile.']},
                     {'titulo': 'SAN MARTÍN: EXPEDICIÓN AL PERÚ / '
                                'PROCLAMACIÓN DE LA INDEPENDENCIA (1821)',
                      'items': ['San Martín contrató al mercenario inglés '
                                'Lord Thomas Cochrane para operaciones '
                                'navales.',
                                'Las tropas patriotas desembarcaron en la '
                                'Bahía de Paracas el 8 de setiembre de 1820.',
                                'El general Álvarez de Arenales dirigió la '
                                'expedición a la sierra (Huamanga, '
                                'Huancavelica, Tarma, Junín).',
                                'En el Motín de Aznapuquio, oficiales '
                                'españoles destituyeron al virrey Joaquín de '
                                'la Pezuela.',
                                'José de la Serna, nombrado virrey, se '
                                'retiró al Cusco tras la fracasada '
                                'Conferencia de Punchauca.',
                                'El 9 de julio de 1821, San Martín ingresó a '
                                'Lima.',
                                'El 15 de julio de 1821 se redactó el Acta '
                                'de Independencia, a cargo de Manuel Pérez '
                                'de Tudela.',
                                'El 28 de julio de 1821, San Martín proclamó '
                                'formalmente la independencia del Perú.',
                                'San Martín encargó el diseño de la primera '
                                'bandera peruana a Charles Wood Taylor.']},
                     {'titulo': 'BOLÍVAR: LLEGADA Y FEDERACIÓN DE LOS ANDES '
                                '/ LAS BATALLAS DE JUNÍN Y AYACUC',
                      'items': ['Antes de llegar al Perú, Bolívar dirigió '
                                'las independencias de Nueva Granada '
                                '(Boyacá, 1819), Venezuela (Carabobo, 1821) '
                                'y Quito (Pichincha, 1822).',
                                'Simón Bolívar llegó al Perú el 1 de '
                                'setiembre de 1823, siendo presidente '
                                'Bernardo de Torre Tagle.',
                                'Nombró como su secretario a Faustino '
                                'Sánchez Carrión, «el solitario de Sayán».',
                                'Bolívar intentó crear la Federación de los '
                                'Andes con Gran Colombia, Perú y Bolivia.',
                                'Promulgó la Constitución Vitalicia de 1826, '
                                'rechazada por los criollos de los tres '
                                'países.',
                                'La batalla de Junín (6 de agosto de 1824) '
                                'fue un choque de caballería sin disparos, '
                                'llamada la «batalla sin humo».',
                                'En Junín, el patriota Necochea enfrentó al '
                                'realista Canterac.',
                                'La batalla de Ayacucho (9 de diciembre de '
                                '1824) se libró en las pampas al pie del '
                                'cerro Condorcunca.',
                                'En Ayacucho, el patriota Antonio José de '
                                'Sucre (con Agustín Gamarra como Jefe de '
                                'Estado Mayor) venció al virrey La Serna.']},
                     {'titulo': 'LA CAPITULACIÓN DE AYACUCHO',
                      'items': ['La Capitulación de Ayacucho, que consolidó '
                                'la independencia, se firmó el 9 de '
                                'diciembre de 1824 en el mismo campo de '
                                'batalla.',
                                'Fue suscrita entre Antonio José de Sucre '
                                '(Perú) y José de Canterac (bando realista).',
                                'La capitulación constaba de 18 cláusulas; '
                                'España reconoció la independencia del '
                                'Perú.']}],
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
  'secciones': [{'titulo': '16.1 EL PROTECTORADO DE SAN MARTÍN',
                 'items': ['San Martín asumió el cargo de {Protector} del '
                           'Perú el 3 de agosto de 1821, durante un año y 17 '
                           'días.',
                           'Creó la {Biblioteca Nacional}, la Escuela Normal '
                           'para varones, y estableció la moneda del {Sol de '
                           'Oro}.',
                           'Promulgó la «{Ley de Vientres}», que reconocía '
                           'la libertad limitada de los hijos de esclavos.',
                           'Abolió el {tributo indígena} y el trabajo '
                           'forzado, declarando que todos los indios serían '
                           'llamados peruanos.',
                           'Creó los tres primeros ministerios: Hacienda '
                           '({Hipólito Unanue}), Relaciones Exteriores y '
                           'Guerra y Marina (Bernardo de Monteagudo).']},
                {'titulo': '16.2 EL CONGRESO CONSTITUYENTE Y LA CONSTITUCIÓN '
                           'DE 1823',
                 'items': ['El Congreso Constituyente, instalado el {20 de '
                           'setiembre} de 1822, fue la primera institución '
                           'elegida democráticamente en el Perú.',
                           'Su primer presidente fue {Francisco Javier de '
                           'Luna Pizarro}.',
                           'Ante el retiro de San Martín, se conformó la '
                           '{Suprema Junta Gubernativa}, encabezada por José '
                           'de la Mar.',
                           'La primera Constitución del Perú, de carácter '
                           '{liberal}, fue promulgada el 12 de noviembre de '
                           '1823.',
                           'Estableció que el Perú se dividiría en tres '
                           'poderes: {Legislativo}, Ejecutivo y Judicial.']},
                {'titulo': '16.3 EL CAUDILLISMO MILITAR POST INDEPENDENCIA',
                 'items': ['{Jorge Basadre} identificó tres «militarismos» '
                           'en el Perú: el primero (1827-1872), el segundo '
                           '(1884-1895) y el tercero (1930-1939).',
                           'Los caudillos militares tomaban el poder '
                           'mediante {golpes de estado}, luego legitimados '
                           'con elecciones.',
                           'Los caudillos típicos post independencia fueron '
                           '{Andrés de Santa Cruz}, Agustín Gamarra, Felipe '
                           'Santiago Salaverry y Luis José de Orbegoso.']},
                {'titulo': '16.4 LA CONFEDERACIÓN PERÚ-BOLIVIANA: FORMACIÓN',
                 'items': ['La {Confederación Perú-Boliviana} (1836-1839) '
                           'buscaba superar la competencia comercial de '
                           'Chile y Argentina.',
                           'Estuvo constituida por tres Estados: '
                           '{Nor-peruano} (Orbegoso), Sur-peruano (Herrera y '
                           'Tristán), y Boliviano.',
                           '{Andrés de Santa Cruz} fue el Protector de toda '
                           'la Confederación.',
                           'Fue aprobada por el {Congreso de Tacna} el 9 de '
                           'mayo de 1837.']},
                {'titulo': '16.5 LA CONFEDERACIÓN PERÚ-BOLIVIANA: CAÍDA',
                 'items': ['La primera expedición restauradora, al mando de '
                           '{Blanco Encalada}, fue derrotada, firmando el '
                           'Tratado de {Paucarpata} (1837).',
                           'La segunda expedición, el «Ejército Unido '
                           'Restaurador», fue comandada por {Manuel Bulnes} '
                           'y Agustín Gamarra.',
                           'La Confederación cayó tras la derrota en la '
                           'batalla de {Yungay}, el 20 de enero de 1839.',
                           'Tras la caída, {Agustín Gamarra} se convirtió en '
                           'presidente del Perú por segunda vez '
                           '(1839-1841).']},
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
                 'alternativas': ['El Congreso Constituyente',
                                  'La dictadura de Bolívar',
                                  'El gobierno de Riva Agüero',
                                  'La Junta Gubernativa',
                                  'El Protectorado de San Martín'],
                 'correcta': 'E'},
                {'pregunta': 'La primera Constitución del Perú fue '
                             'promulgada en:',
                 'alternativas': ['1828', '1834', '1821', '1823', '1826'],
                 'correcta': 'D'},
                {'pregunta': 'El primer presidente del Perú fue:',
                 'alternativas': ['José de la Riva Agüero',
                                  'Ramón Castilla',
                                  'San Martín',
                                  'Simón Bolívar',
                                  'La Mar'],
                 'correcta': 'A'},
                {'pregunta': 'La Confederación Perú-Boliviana fue creada '
                             'por:',
                 'alternativas': ['Felipe Salaverry',
                                  'Ramón Castilla',
                                  'José de la Mar',
                                  'Agustín Gamarra',
                                  'Andrés de Santa Cruz'],
                 'correcta': 'E'},
                {'pregunta': 'La Confederación Perú-Boliviana fue disuelta '
                             'tras la batalla de:',
                 'alternativas': ['Yungay',
                                  'Ayacucho',
                                  'Ingavi',
                                  'Socabaya',
                                  'Portada de Guías'],
                 'correcta': 'A'},
                {'pregunta': 'Los Estados que integraron la Confederación '
                             'fueron Nor Peruano, Sur Peruano y:',
                 'alternativas': ['Boliviano',
                                  'Chileno',
                                  'Argentino',
                                  'Colombiano',
                                  'Ecuatoriano'],
                 'correcta': 'A'},
                {'pregunta': 'La principal fuente de ingresos del Estado '
                             'peruano desde 1840 fue:',
                 'alternativas': ['El salitre',
                                  'El azúcar',
                                  'El caucho',
                                  'El guano',
                                  'La plata'],
                 'correcta': 'D'},
                {'pregunta': 'El contrato Dreyfus se firmó en 1869 durante '
                             'el gobierno de:',
                 'alternativas': ['José Balta',
                                  'Echenique',
                                  'Manuel Pardo',
                                  'Nicolás de Piérola',
                                  'Ramón Castilla'],
                 'correcta': 'A'},
                {'pregunta': 'La abolición de la esclavitud y del tributo '
                             'indígena se produjo bajo el gobierno de:',
                 'alternativas': ['Manuel Pardo',
                                  'Gamarra',
                                  'Santa Cruz',
                                  'José Balta',
                                  'Ramón Castilla'],
                 'correcta': 'E'},
                {'pregunta': 'El primer ferrocarril de Sudamérica unió:',
                 'alternativas': ['Cusco y Puno',
                                  'Mollendo y Arequipa',
                                  'Tacna y Arica',
                                  'Lima y Callao',
                                  'Lima y Huancayo'],
                 'correcta': 'D'},
                {'pregunta': 'La causa inmediata de la Guerra del Pacífico '
                             'fue:',
                 'alternativas': ['La toma de Antofagasta por Perú',
                                  'El bloqueo del Callao',
                                  'El impuesto de los 10 centavos al salitre',
                                  'La invasión de Tarapacá',
                                  'El tratado de 1873'],
                 'correcta': 'C'},
                {'pregunta': 'El tratado que unía a Perú y Bolivia era de '
                             'alianza:',
                 'alternativas': ['Comercial',
                                  'Ofensiva',
                                  'Cultural',
                                  'Aduanera',
                                  'Defensiva'],
                 'correcta': 'E'},
                {'pregunta': 'Miguel Grau murió heroicamente en el combate '
                             'de:',
                 'alternativas': ['Arica',
                                  'San Juan',
                                  'Iquique',
                                  'Tarapacá',
                                  'Angamos'],
                 'correcta': 'E'},
                {'pregunta': 'Francisco Bolognesi murió en la batalla de:',
                 'alternativas': ['Arica',
                                  'Tacna',
                                  'Miraflores',
                                  'Huamachuco',
                                  'Angamos'],
                 'correcta': 'A'},
                {'pregunta': 'El combate de Angamos se produjo el:',
                 'alternativas': ['7 de junio de 1880',
                                  '13 de enero de 1881',
                                  '10 de julio de 1883',
                                  '21 de mayo de 1879',
                                  '8 de octubre de 1879'],
                 'correcta': 'E'},
                {'pregunta': 'La Guerra del Pacífico terminó con el Tratado '
                             'de:',
                 'alternativas': ['Ginebra',
                                  'Santiago',
                                  'Ancón',
                                  'Tordesillas',
                                  'Lima'],
                 'correcta': 'C'},
                {'pregunta': 'Por el Tratado de Ancón el Perú cedió '
                             'definitivamente:',
                 'alternativas': ['Tacna',
                                  'Antofagasta',
                                  'Arica',
                                  'Iquique y Tacna',
                                  'Tarapacá'],
                 'correcta': 'E'},
                {'pregunta': 'La campaña de resistencia en la sierra central '
                             'fue dirigida por:',
                 'alternativas': ['Miguel Iglesias',
                                  'Francisco Bolognesi',
                                  'Lizardo Montero',
                                  'Nicolás de Piérola',
                                  'Andrés A. Cáceres'],
                 'correcta': 'E'},
                {'pregunta': 'El caudillismo militar se caracterizó porque '
                             'el poder fue disputado por:',
                 'alternativas': ['Los indígenas',
                                  'Los comerciantes',
                                  'Los extranjeros',
                                  'Los jefes militares de la independencia',
                                  'El clero'],
                 'correcta': 'D'},
                {'pregunta': 'El sistema de comercialización del guano '
                             'previo al contrato Dreyfus fue:',
                 'alternativas': ['El arrendamiento',
                                  'El monopolio estatal',
                                  'La libre competencia',
                                  'La concesión minera',
                                  'Las consignaciones'],
                 'correcta': 'E'},
                {'pregunta': 'La Constitución de 1823, promulgada por el '
                             'Primer Congreso Constituyente, fue considerada '
                             'de carácter: (UNSAAC Ordinario)',
                 'alternativas': ['Neoliberal',
                                  'Liberal',
                                  'Clásico',
                                  'Militar',
                                  'Ideológico'],
                 'correcta': 'B'},
                {'pregunta': 'Para el negocio del guano de islas del Perú, '
                             'el Contrato Dreyfus fue suscrito en el '
                             'gobierno de: (UNSAAC Ordinario)',
                 'alternativas': ['Felipe Santiago Salaverry',
                                  'José Balta',
                                  'Agustín Gamarra',
                                  'Ramón Castilla',
                                  'José de la Riva Agüero'],
                 'correcta': 'B'},
                {'pregunta': 'En la Guerra del Pacífico, el presidente del '
                             'Perú fue: (UNSAAC Ordinario)',
                 'alternativas': ['Hilarión Daza',
                                  'Aníbal Pinto',
                                  'Augusto B. Leguía',
                                  'Andrés Avelino Cáceres',
                                  'Mariano Ignacio Prado'],
                 'correcta': 'E'},
                {'pregunta': 'El incendio y saqueo de la Biblioteca Nacional '
                             'y del Congreso Peruano fue durante: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['El primer caudillismo militar',
                                  'La expedición restauradora de Manuel '
                                  'Bulnes',
                                  'El Motín de Aznapuquio',
                                  'La dictadura de Simón Bolívar',
                                  'La invasión chilena durante la guerra del '
                                  'Pacífico'],
                 'correcta': 'E'},
                {'pregunta': 'Una de las consecuencias de la Guerra del '
                             'Pacífico fue la pérdida de las provincias de: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Moquegua y Tarapacá',
                                  'Tarapacá y Arica',
                                  'Arica y Arequipa',
                                  'Tarapacá y Tacna',
                                  'Chorrillos y Miraflores'],
                 'correcta': 'B'},
                {'pregunta': 'Al iniciarse la República, la creación de la '
                             'Biblioteca Nacional ocurrió durante: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['El Protectorado',
                                  'El Gobierno de Ramón Castilla',
                                  'El gobierno de Torre Tagle',
                                  'La Confederación Peruano-boliviana',
                                  'El Primer Congreso Constituyente'],
                 'correcta': 'A'},
                {'pregunta': 'La apropiación de los recursos naturales que '
                             'desencadenó la Guerra del Pacífico fueron el: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Cobre y petróleo',
                                  'Salitre y Guano',
                                  'Gas y petróleo',
                                  'Salitre y gas',
                                  'Oro y plata'],
                 'correcta': 'B'},
                {'pregunta': 'Una forma de la comercialización del guano por '
                             'medio del sistema de consignaciones fue '
                             'implantado por el gobierno de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['José Balta',
                                  'Ramón Castilla',
                                  'Mariano Ignacio Prado',
                                  'José Rufino Echenique',
                                  'Andrés Avelino Cáceres'],
                 'correcta': 'D'},
                {'pregunta': 'Como consecuencia de la infausta Guerra del '
                             'Pacífico, después del Tratado de Ancón, el '
                             'gobierno de Andrés Avelino Cáceres decidió '
                             'encausar: (UNSAAC Ordinario)',
                 'alternativas': ['La organización de la defensa de Lima '
                                  'contra Patricio Linch',
                                  'La recuperación económica y la '
                                  'reconstrucción nacional',
                                  'La declaración de Guerra a Chile para '
                                  'recuperar Tacna y Arica',
                                  'El Contrato Dreyfus para la reventa del '
                                  'Guano',
                                  'La resistencia del ejército en la sierra '
                                  'peruana'],
                 'correcta': 'B'},
                {'pregunta': 'El pretexto que involucró al Perú en la '
                             'infausta guerra con Chile fue por: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['La negativa de pagar el impuesto de diez '
                                  'centavos por quintal de Salitre',
                                  'Problemas de límites de bolivianos y '
                                  'chilenos',
                                  'La ambición de Chile de los recursos de '
                                  'guano y salitre en Tarapacá',
                                  'La Alianza secreta de Defensa entre Perú '
                                  'y Bolivia',
                                  'La entrega a perpetuidad de los '
                                  'territorios de Tarapacá'],
                 'correcta': 'A'},
                {'pregunta': 'Es considerada como causa principal de la '
                             'Guerra del Pacífico: (UNSAAC Ordinario)',
                 'alternativas': ['El cobre de Chile',
                                  'La sal de Bolivia',
                                  'El algodón de Perú',
                                  'El salitre del Perú y Bolivia',
                                  'El mar del pacífico'],
                 'correcta': 'D'},
                {'pregunta': 'Uno de los pretextos de la Guerra del Pacífico '
                             'entre Perú y Chile, fue la: (UNSAAC Ordinario)',
                 'alternativas': ['Pérdida de los ingenios azucareros del '
                                  'norte del País',
                                  'Alianza Secreta de defensa entre Perú y '
                                  'Bolivia',
                                  'Destrucción de las obras públicas',
                                  'Paralización de la actividad comercial '
                                  'internacional',
                                  'Crisis Psicológica y depresión colectiva'],
                 'correcta': 'B'},
                {'pregunta': 'La causa más importante de la Guerra del '
                             'Pacífico fue: (UNSAAC Ordinario)',
                 'alternativas': ['La Alianza Secreta de Defensa entre Perú '
                                  'y Bolivia en el contexto sudamericano',
                                  'La disputa entre Chile y Perú por fijar '
                                  'límites territoriales',
                                  'La codicia y ambición de Chile por las '
                                  'riquezas del guano y salitre del Perú y '
                                  'Bolivia',
                                  'La intromisión del imperialismo '
                                  'capitalista inglés en asuntos políticos '
                                  'de Sudamérica',
                                  'La enemistad secular de Chile con Perú y '
                                  'Bolivia'],
                 'correcta': 'C'},
                {'pregunta': 'La constitución política de 1823 no llegó a '
                             'entrar en vigencia por: (II CEPRU 2011)',
                 'alternativas': ['El protectorado de San Martín',
                                  'La Monarquía Constitucional de San Martín',
                                  'La Confederación Perú-boliviana',
                                  'La dictadura de Simón Bolívar',
                                  'El Oncenio de Augusto B. Leguía'],
                 'correcta': 'D'},
                {'pregunta': 'En la Guerra Internacional del Pacífico, el '
                             'plenipotenciario chileno que firmó el Tratado '
                             'de Paz de Ancón fue: (II CEPRU 2011)',
                 'alternativas': ['Aníbal Pinto',
                                  'Hilarión Daza',
                                  'Miguel Iglesias',
                                  'Jovino Novoa',
                                  'Andrés A. Cáceres'],
                 'correcta': 'D'},
                {'pregunta': 'Después de la Guerra con Chile, la '
                             'reconstrucción nacional tuvo un carácter: (II '
                             'CEPRU 2011)',
                 'alternativas': ['Literario',
                                  'Educativo',
                                  'Académico',
                                  'Económico',
                                  'Religioso'],
                 'correcta': 'D'},
                {'pregunta': 'San Martín asumió el cargo de Protector del '
                             'Perú el 3 de agosto de:',
                 'alternativas': ['1821', '1824', '1823', '1820', '1822'],
                 'correcta': 'A'},
                {'pregunta': 'La ley promulgada por San Martín que reconocía '
                             'la libertad limitada de los hijos de esclavos '
                             'se llamó:',
                 'alternativas': ['Ley de Vientres',
                                  'Ley de Manumisión',
                                  'Ley de Libertad',
                                  'Ley de Redención',
                                  'Ley de Abolición'],
                 'correcta': 'A'},
                {'pregunta': 'El ministro de Hacienda en el gabinete del '
                             'Protectorado de San Martín fue:',
                 'alternativas': ['Juan García del Río',
                                  'José de la Riva Agüero',
                                  'Hipólito Unanue',
                                  'Bernardo de Monteagudo',
                                  'Faustino Sánchez Carrión'],
                 'correcta': 'C'},
                {'pregunta': 'El Congreso Constituyente del Perú fue '
                             'instalado por San Martín el 20 de setiembre '
                             'de:',
                 'alternativas': ['1823', '1820', '1821', '1824', '1822'],
                 'correcta': 'E'},
                {'pregunta': 'El primer presidente del Congreso '
                             'Constituyente de 1822 fue:',
                 'alternativas': ['Faustino Sánchez Carrión',
                                  'José de la Mar',
                                  'Francisco Javier de Luna Pizarro',
                                  'José Bernardo de Tagle',
                                  'José de la Riva Agüero'],
                 'correcta': 'C'},
                {'pregunta': 'Ante el retiro de San Martín, el Poder '
                             'Ejecutivo fue entregado a un cuerpo colegiado '
                             'llamado:',
                 'alternativas': ['Consejo de Estado',
                                  'Congreso Ejecutivo',
                                  'Triunvirato Peruano',
                                  'Suprema Junta Gubernativa',
                                  'Directorio Nacional'],
                 'correcta': 'D'},
                {'pregunta': 'La primera Constitución del Perú '
                             'independiente, de carácter liberal, fue '
                             'promulgada el 12 de noviembre de:',
                 'alternativas': ['1822', '1828', '1823', '1821', '1824'],
                 'correcta': 'C'},
                {'pregunta': 'El historiador que identificó los tres '
                             '«militarismos» en la historia republicana del '
                             'Perú fue:',
                 'alternativas': ['Raúl Porras Barrenechea',
                                  'Pablo Macera',
                                  'Carlos Contreras',
                                  'Marcos Cueto',
                                  'Jorge Basadre'],
                 'correcta': 'E'},
                {'pregunta': 'Los caudillos militares post independencia '
                             'tomaban el poder principalmente mediante:',
                 'alternativas': ['Designación del Congreso',
                                  'Golpes de estado',
                                  'Herencia familiar',
                                  'Elecciones democráticas',
                                  'Sorteo público'],
                 'correcta': 'B'},
                {'pregunta': 'La Confederación Perú-Boliviana buscaba '
                             'principalmente superar la competencia '
                             'comercial de:',
                 'alternativas': ['Colombia y Venezuela',
                                  'Bolivia y Paraguay',
                                  'Brasil y Ecuador',
                                  'Chile y Argentina',
                                  'México y Panamá'],
                 'correcta': 'D'},
                {'pregunta': 'El Protector de toda la Confederación '
                             'Perú-Boliviana fue:',
                 'alternativas': ['Pío Tristán',
                                  'Ramón Herrera',
                                  'Agustín Gamarra',
                                  'Luis José de Orbegoso',
                                  'Andrés de Santa Cruz'],
                 'correcta': 'E'},
                {'pregunta': 'La Confederación Perú-Boliviana fue aprobada '
                             'por el Congreso de Tacna el 9 de mayo de:',
                 'alternativas': ['1837', '1839', '1835', '1836', '1838'],
                 'correcta': 'A'},
                {'pregunta': 'La primera expedición restauradora chilena '
                             'contra la Confederación, al mando de Blanco '
                             'Encalada, culminó con la firma del Tratado de:',
                 'alternativas': ['Paucarpata',
                                  'Tacna',
                                  'Sicuani',
                                  'Yungay',
                                  'Ancón'],
                 'correcta': 'A'},
                {'pregunta': 'La Confederación Perú-Boliviana cayó '
                             'definitivamente tras la derrota en la batalla '
                             'de:',
                 'alternativas': ['Ayacucho',
                                  'Ingavi',
                                  'Yungay',
                                  'Zepita',
                                  'Junín'],
                 'correcta': 'C'},
                {'pregunta': 'Tras la caída de la Confederación '
                             'Perú-Boliviana, se convirtió en presidente del '
                             'Perú por segunda vez:',
                 'alternativas': ['Luis José de Orbegoso',
                                  'Ramón Castilla',
                                  'Agustín Gamarra',
                                  'Felipe Santiago Salaverry',
                                  'Andrés de Santa Cruz'],
                 'correcta': 'C'}],
  'resumen_visual': [{'titulo': 'EL PROTECTORADO DE SAN MARTÍN',
                      'items': ['San Martín asumió el cargo de Protector del '
                                'Perú el 3 de agosto de 1821, durante un año '
                                'y 17 días.',
                                'Creó la Biblioteca Nacional, la Escuela '
                                'Normal para varones, y estableció la moneda '
                                'del Sol de Oro.',
                                'Promulgó la «Ley de Vientres», que '
                                'reconocía la libertad limitada de los hijos '
                                'de esclavos.',
                                'Abolió el tributo indígena y el trabajo '
                                'forzado, declarando que todos los indios '
                                'serían llamados peruanos.',
                                'Creó los tres primeros ministerios: '
                                'Hacienda (Hipólito Unanue), Relaciones '
                                'Exteriores y Guerra y Marina (Bernardo de '
                                'Monteagudo).']},
                     {'titulo': 'EL CONGRESO CONSTITUYENTE Y LA CONSTITUCIÓN '
                                'DE 1823',
                      'items': ['El Congreso Constituyente, instalado el 20 '
                                'de setiembre de 1822, fue la primera '
                                'institución elegida democráticamente en el '
                                'Perú.',
                                'Su primer presidente fue Francisco Javier '
                                'de Luna Pizarro.',
                                'Ante el retiro de San Martín, se conformó '
                                'la Suprema Junta Gubernativa, encabezada '
                                'por José de la Mar.',
                                'La primera Constitución del Perú, de '
                                'carácter liberal, fue promulgada el 12 de '
                                'noviembre de 1823.',
                                'Estableció que el Perú se dividiría en tres '
                                'poderes: Legislativo, Ejecutivo y '
                                'Judicial.']},
                     {'titulo': 'EL CAUDILLISMO MILITAR POST INDEPENDENCIA',
                      'items': ['Jorge Basadre identificó tres '
                                '«militarismos» en el Perú: el primero '
                                '(1827-1872), el segundo (1884-1895) y el '
                                'tercero (1930-1939).',
                                'Los caudillos militares tomaban el poder '
                                'mediante golpes de estado, luego '
                                'legitimados con elecciones.',
                                'Los caudillos típicos post independencia '
                                'fueron Andrés de Santa Cruz, Agustín '
                                'Gamarra, Felipe Santiago Salaverry y Luis '
                                'José de Orbegoso.']},
                     {'titulo': 'LA CONFEDERACIÓN PERÚ-BOLIVIANA: FORMACIÓN',
                      'items': ['La Confederación Perú-Boliviana (1836-1839) '
                                'buscaba superar la competencia comercial de '
                                'Chile y Argentina.',
                                'Estuvo constituida por tres Estados: '
                                'Nor-peruano (Orbegoso), Sur-peruano '
                                '(Herrera y Tristán), y Boliviano.',
                                'Andrés de Santa Cruz fue el Protector de '
                                'toda la Confederación.',
                                'Fue aprobada por el Congreso de Tacna el 9 '
                                'de mayo de 1837.']},
                     {'titulo': 'LA CONFEDERACIÓN PERÚ-BOLIVIANA: CAÍDA',
                      'items': ['La primera expedición restauradora, al '
                                'mando de Blanco Encalada, fue derrotada, '
                                'firmando el Tratado de Paucarpata (1837).',
                                'La segunda expedición, el «Ejército Unido '
                                'Restaurador», fue comandada por Manuel '
                                'Bulnes y Agustín Gamarra.',
                                'La Confederación cayó tras la derrota en la '
                                'batalla de Yungay, el 20 de enero de 1839.',
                                'Tras la caída, Agustín Gamarra se convirtió '
                                'en presidente del Perú por segunda vez '
                                '(1839-1841).']},
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
  'secciones': [{'titulo': '17.1 LA RECONSTRUCCIÓN NACIONAL: PRESIDENTES',
                 'items': ['La {reconstrucción nacional} se extendió desde '
                           'el Tratado de Ancón (1884) hasta {1919}.',
                           'El principal problema del periodo fue el orden '
                           '{económico}, representado por la deuda externa.',
                           '{Miguel Iglesias} gobernó de 1884 a 1886; le '
                           'sucedió {Andrés Avelino Cáceres} (1886-1890).',
                           '{Remigio Morales Bermúdez} gobernó de 1890 a '
                           '1894; Cáceres asumió un segundo gobierno en '
                           '1894.']},
                {'titulo': '17.2 LA REPÚBLICA ARISTOCRÁTICA: CARACTERÍSTICAS',
                 'items': ['La {República Aristocrática} (1895-1919) fue '
                           'denominada así por el historiador {Jorge '
                           'Basadre}.',
                           'El poder fue ejercido por la {oligarquía '
                           'civilista}, familias adineradas de la costa.',
                           'Se estableció un Estado aparentemente '
                           '{democrático}, con elecciones reducidas y casi '
                           'sin participación popular.',
                           'El pueblo protestó mediante paros y {rebeliones '
                           'campesinas} contra gamonales y terratenientes.']},
                {'titulo': '17.3 PRESIDENTES DE LA REPÚBLICA ARISTOCRÁTICA',
                 'items': ['{Nicolás de Piérola} gobernó de 1895 a 1899; le '
                           'siguió Eduardo López de Romaña (1899-1903).',
                           '{José Pardo y Barreda} tuvo dos gobiernos: el '
                           'primero en 1904-1908, el segundo en {1915}-1919.',
                           '{Augusto B. Leguía} tuvo su primer gobierno '
                           'entre 1908 y 1912.',
                           '{Guillermo Billinghurst} gobernó de 1912 a 1914; '
                           'Óscar R. Benavides, de 1914 a 1915.']},
                {'titulo': '17.4 EL ONCENIO DE LEGUÍA (1919–1930)',
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
                                  'República Aristocrática',
                                  'Reconstrucción Nacional o Segundo '
                                  'Militarismo',
                                  'Patria Nueva',
                                  'Primer Militarismo'],
                 'correcta': 'C'},
                {'pregunta': 'Por el Contrato Grace el Perú entregó por 66 '
                             'años:',
                 'alternativas': ['Los ferrocarriles',
                                  'Los puertos',
                                  'Las minas',
                                  'Las aduanas',
                                  'Las islas guaneras únicamente'],
                 'correcta': 'A'},
                {'pregunta': 'El Contrato Grace se firmó en el año:',
                 'alternativas': ['1895', '1889', '1929', '1883', '1919'],
                 'correcta': 'B'},
                {'pregunta': 'La República Aristocrática se inició con el '
                             'gobierno de:',
                 'alternativas': ['Nicolás de Piérola',
                                  'Augusto B. Leguía',
                                  'José Pardo',
                                  'Andrés A. Cáceres',
                                  'Miguel Iglesias'],
                 'correcta': 'A'},
                {'pregunta': 'La República Aristocrática abarca los años:',
                 'alternativas': ['1845-1862',
                                  '1930-1945',
                                  '1883-1895',
                                  '1919-1930',
                                  '1895-1919'],
                 'correcta': 'E'},
                {'pregunta': 'El grupo social que ejerció el poder durante '
                             'la República Aristocrática fue:',
                 'alternativas': ['La oligarquía civilista',
                                  'La Iglesia',
                                  'El proletariado',
                                  'Los militares',
                                  'El campesinado'],
                 'correcta': 'A'},
                {'pregunta': 'La economía de la República Aristocrática se '
                             'basó en:',
                 'alternativas': ['La minería estatal',
                                  'La exportación de materias primas',
                                  'El turismo',
                                  'El comercio interno',
                                  'La industria pesada'],
                 'correcta': 'B'},
                {'pregunta': 'El gobierno de Leguía entre 1919 y 1930 se '
                             'conoce como:',
                 'alternativas': ['La Patria Nueva u Oncenio',
                                  'La República Aristocrática',
                                  'El Ochenio',
                                  'La Reconstrucción',
                                  'El Novenio'],
                 'correcta': 'A'},
                {'pregunta': 'La Constitución promulgada durante el Oncenio '
                             'fue la de:',
                 'alternativas': ['1860', '1979', '1933', '1993', '1920'],
                 'correcta': 'E'},
                {'pregunta': 'El trabajo obligatorio para construir '
                             'carreteras durante el Oncenio se llamó:',
                 'alternativas': ['Yanaconaje',
                                  'Enganche',
                                  'Conscripción vial',
                                  'Faena',
                                  'Mita republicana'],
                 'correcta': 'C'},
                {'pregunta': 'El Tratado Salomón-Lozano se firmó con:',
                 'alternativas': ['Colombia',
                                  'Ecuador',
                                  'Chile',
                                  'Brasil',
                                  'Bolivia'],
                 'correcta': 'A'},
                {'pregunta': 'El Tratado de Lima de 1929 se firmó con:',
                 'alternativas': ['Bolivia',
                                  'Argentina',
                                  'Ecuador',
                                  'Chile',
                                  'Colombia'],
                 'correcta': 'D'},
                {'pregunta': 'Por el Tratado de Lima de 1929, Tacna:',
                 'alternativas': ['Se dividió',
                                  'Pasó a Bolivia',
                                  'Quedó en Chile',
                                  'Se declaró neutral',
                                  'Volvió al Perú'],
                 'correcta': 'E'},
                {'pregunta': 'Por el Tratado de Lima de 1929, Arica quedó en '
                             'poder de:',
                 'alternativas': ['Bolivia',
                                  'Perú',
                                  'Chile',
                                  'Administración internacional',
                                  'Ninguno'],
                 'correcta': 'C'},
                {'pregunta': 'Leguía fue derrocado en 1930 por:',
                 'alternativas': ['Óscar R. Benavides',
                                  'Bustamante y Rivero',
                                  'Manuel Prado',
                                  'Luis M. Sánchez Cerro',
                                  'Odría'],
                 'correcta': 'D'},
                {'pregunta': 'Durante la República Aristocrática se produjo '
                             'el auge de la explotación del:',
                 'alternativas': ['Estaño',
                                  'Petróleo',
                                  'Salitre',
                                  'Caucho',
                                  'Guano'],
                 'correcta': 'D'},
                {'pregunta': 'El endeudamiento externo del Oncenio se dio '
                             'principalmente con:',
                 'alternativas': ['Inglaterra',
                                  'Alemania',
                                  'Francia',
                                  'Estados Unidos',
                                  'España'],
                 'correcta': 'D'},
                {'pregunta': 'Los enclaves económicos se caracterizaron por:',
                 'alternativas': ['Ser empresas estatales',
                                  'Ser empresas extranjeras con escasa '
                                  'integración a la economía nacional',
                                  'Ser talleres artesanales',
                                  'Ser cooperativas',
                                  'Pertenecer a comunidades campesinas'],
                 'correcta': 'B'},
                {'pregunta': 'El primer presidente del Segundo Militarismo '
                             'fue:',
                 'alternativas': ['Nicolás de Piérola',
                                  'Miguel Iglesias',
                                  'Remigio Morales Bermúdez',
                                  'Lizardo Montero',
                                  'Andrés A. Cáceres'],
                 'correcta': 'B'},
                {'pregunta': 'La explotación del caucho tuvo como '
                             'consecuencia principal:',
                 'alternativas': ['La construcción de ferrocarriles',
                                  'El auge del guano',
                                  'Graves abusos contra las poblaciones '
                                  'indígenas amazónicas',
                                  'El desarrollo industrial',
                                  'La modernización agrícola'],
                 'correcta': 'C'},
                {'pregunta': 'El Oncenio de Leguía terminó con el golpe de '
                             'Estado dirigido por:',
                 'alternativas': ['Juan Velasco Alvarado',
                                  'Luis Sánchez Cerro',
                                  'Manuel A. Odría',
                                  'Óscar R. Benavides',
                                  'Andrés A. Cáceres'],
                 'correcta': 'B'},
                {'pregunta': 'El régimen de gobierno de Augusto B. Leguía '
                             'fue conocido como: (UNSAAC Ordinario)',
                 'alternativas': ['Conservador',
                                  'Militar',
                                  'El Ochenio',
                                  'Reformista',
                                  'El Oncenio'],
                 'correcta': 'E'},
                {'pregunta': 'El territorio de Tacna fue reincorporado a la '
                             'soberanía del Perú, en el gobierno de: (UNSAAC '
                             'Ordinario)',
                 'alternativas': ['Juan Velasco Alvarado',
                                  'Manuel A. Odría',
                                  'José Pardo',
                                  'Manuel Prado Ugarteche',
                                  'Augusto B. Leguía'],
                 'correcta': 'E'},
                {'pregunta': 'El gobierno del Oncenio de Augusto B. Leguía '
                             'terminó con el golpe de estado del general: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Nicolás de Piérola',
                                  'Luis M. Sánchez Cerro',
                                  'Guillermo Billinghurst',
                                  'Eduardo López de Romaña',
                                  'José Pardo y Barreda'],
                 'correcta': 'B'},
                {'pregunta': 'La reconstrucción de la ciudad del Cusco, '
                             'después del terremoto de 1950, fue durante el '
                             'gobierno de: (UNSAAC Ordinario)',
                 'alternativas': ['Fernando Belaunde',
                                  'Manuel Prado',
                                  'Manuel A. Odría',
                                  'José Luis Bustamante y Rivero',
                                  'Ricardo Pérez Godoy'],
                 'correcta': 'C'},
                {'pregunta': 'En el gobierno del Oncenio de Leguía, se: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Cedió a Chile, definitivamente, Tarapacá',
                                  'Ejecutó la expropiación de las salitreras '
                                  'de Tarapacá',
                                  'Perdió la página once del Acta de Talara',
                                  'Recuperó Tacna de la posesión chilena',
                                  'Entregó a Ecuador 1km2 del territorio '
                                  'nacional'],
                 'correcta': 'D'},
                {'pregunta': 'El peruano a quien designaban Amauta y que '
                             'tuvo como lema «Peruanicemos al Perú», fue: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['José de la Riva Agüero o Osma',
                                  'Víctor Raúl Haya de la Torre',
                                  'Víctor Andrés Belaúnde',
                                  'Manuel Gonzáles Prada',
                                  'José Carlos Mariátegui La Chira'],
                 'correcta': 'C'},
                {'pregunta': 'El periodo gubernamental de Manuel A. Odría, '
                             'en relación al Cusco, se caracteriza por: '
                             '(UNSAAC Ordinario)',
                 'alternativas': ['Asumir el poder con el nombre de Gobierno '
                                  'Revolucionario de las Fuerzas Armadas',
                                  'Reprimir el levantamiento campesino en el '
                                  'Valle de la Convención',
                                  'Decretar el día del campesino, el 24 de '
                                  'junio de 1969',
                                  'La reconstrucción del Cusco debido al '
                                  'terremoto de 1950',
                                  'Dictar las bases de la primera reforma '
                                  'agraria'],
                 'correcta': 'D'},
                {'pregunta': 'Característica del Segundo Gobierno de '
                             'Belaunde Terry: (UNSAAC Ordinario)',
                 'alternativas': ['Pérdida de la democracia',
                                  'Finalización del terrorismo',
                                  'Masacre de Uchuraccay',
                                  'Comienzo de la hiperinflación',
                                  'Aumento de la población en la capital'],
                 'correcta': 'D'},
                {'pregunta': 'El periodo denominado República Aristocrática '
                             'fue sustentado por: (UNSAAC Ordinario)',
                 'alternativas': ['José Tamayo',
                                  'Pablo Macera',
                                  'Alberto Flores',
                                  'Jorge Basadre',
                                  'Humberto Vidal'],
                 'correcta': 'D'},
                {'pregunta': 'El Partido Socialista fue fundado en 1928 por: '
                             '(II CEPRU 2011)',
                 'alternativas': ['Víctor Raúl Haya de la Torre',
                                  'Augusto B. Leguía',
                                  'José Carlos Mariátegui',
                                  'Jorge Basadre',
                                  'Nicolás de Piérola'],
                 'correcta': 'C'},
                {'pregunta': 'El periodo de la Reconstrucción Nacional se '
                             'extendió desde el Tratado de Ancón (1884) '
                             'hasta:',
                 'alternativas': ['1919', '1895', '1930', '1900', '1910'],
                 'correcta': 'A'},
                {'pregunta': 'El principal problema que debía afrontar el '
                             'país durante la Reconstrucción Nacional fue de '
                             'orden:',
                 'alternativas': ['Territorial',
                                  'Militar',
                                  'Diplomático',
                                  'Económico',
                                  'Religioso'],
                 'correcta': 'D'},
                {'pregunta': 'El primer presidente del periodo de '
                             'Reconstrucción Nacional, tras la Guerra del '
                             'Pacífico, fue:',
                 'alternativas': ['Miguel Iglesias',
                                  'Remigio Morales Bermúdez',
                                  'Andrés Avelino Cáceres',
                                  'José Pardo',
                                  'Nicolás de Piérola'],
                 'correcta': 'A'},
                {'pregunta': 'El historiador que denominó al periodo '
                             '1895-1919 como «República Aristocrática» fue:',
                 'alternativas': ['Manuel Burga',
                                  'Jorge Basadre',
                                  'Raúl Porras Barrenechea',
                                  'Pablo Macera',
                                  'Carlos Contreras'],
                 'correcta': 'B'},
                {'pregunta': 'Durante la República Aristocrática, el poder '
                             'fue ejercido principalmente por:',
                 'alternativas': ['Los militares',
                                  'Los indígenas',
                                  'Los obreros',
                                  'La oligarquía civilista',
                                  'El clero'],
                 'correcta': 'D'},
                {'pregunta': 'El primer presidente de la República '
                             'Aristocrática, que gobernó de 1895 a 1899, '
                             'fue:',
                 'alternativas': ['Augusto B. Leguía',
                                  'Eduardo López de Romaña',
                                  'José Pardo y Barreda',
                                  'Nicolás de Piérola',
                                  'Guillermo Billinghurst'],
                 'correcta': 'D'},
                {'pregunta': 'El presidente que tuvo dos gobiernos durante '
                             'la República Aristocrática (1904-1908 y '
                             '1915-1919) fue:',
                 'alternativas': ['Augusto B. Leguía',
                                  'Nicolás de Piérola',
                                  'Óscar R. Benavides',
                                  'Guillermo Billinghurst',
                                  'José Pardo y Barreda'],
                 'correcta': 'E'},
                {'pregunta': 'El primer gobierno de Augusto B. Leguía, '
                             'dentro de la República Aristocrática, se dio '
                             'entre:',
                 'alternativas': ['1908-1912',
                                  '1914-1915',
                                  '1895-1899',
                                  '1904-1908',
                                  '1912-1914'],
                 'correcta': 'A'},
                {'pregunta': 'El presidente de la República Aristocrática '
                             'derrocado por un golpe militar en 1914 fue:',
                 'alternativas': ['Eduardo López de Romaña',
                                  'Guillermo Billinghurst',
                                  'Nicolás de Piérola',
                                  'Augusto B. Leguía',
                                  'José Pardo'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'LA RECONSTRUCCIÓN NACIONAL: PRESIDENTES',
                      'items': ['La reconstrucción nacional se extendió '
                                'desde el Tratado de Ancón (1884) hasta '
                                '1919.',
                                'El principal problema del periodo fue el '
                                'orden económico, representado por la deuda '
                                'externa.',
                                'Miguel Iglesias gobernó de 1884 a 1886; le '
                                'sucedió Andrés Avelino Cáceres (1886-1890).',
                                'Remigio Morales Bermúdez gobernó de 1890 a '
                                '1894; Cáceres asumió un segundo gobierno en '
                                '1894.']},
                     {'titulo': 'LA REPÚBLICA ARISTOCRÁTICA: CARACTERÍSTICAS',
                      'items': ['La República Aristocrática (1895-1919) fue '
                                'denominada así por el historiador Jorge '
                                'Basadre.',
                                'El poder fue ejercido por la oligarquía '
                                'civilista, familias adineradas de la costa.',
                                'Se estableció un Estado aparentemente '
                                'democrático, con elecciones reducidas y '
                                'casi sin participación popular.',
                                'El pueblo protestó mediante paros y '
                                'rebeliones campesinas contra gamonales y '
                                'terratenientes.']},
                     {'titulo': 'PRESIDENTES DE LA REPÚBLICA ARISTOCRÁTICA',
                      'items': ['Nicolás de Piérola gobernó de 1895 a 1899; '
                                'le siguió Eduardo López de Romaña '
                                '(1899-1903).',
                                'José Pardo y Barreda tuvo dos gobiernos: el '
                                'primero en 1904-1908, el segundo en '
                                '1915-1919.',
                                'Augusto B. Leguía tuvo su primer gobierno '
                                'entre 1908 y 1912.',
                                'Guillermo Billinghurst gobernó de 1912 a '
                                '1914; Óscar R. Benavides, de 1914 a 1915.']},
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
  'secciones': [{'titulo': '18.1 PRIMERA GUERRA MUNDIAL: CONTEXTO Y BLOQUES',
                 'items': ['Entre 1871 y 1914, Europa vivió la llamada «{Paz '
                           'Armada}», periodo de desarrollo económico pero '
                           'de creciente rivalidad y armamentismo entre '
                           'potencias.',
                           'El pretexto de la guerra fue el asesinato del '
                           'archiduque {Francisco Fernando}, heredero '
                           'austro-húngaro, en Sarajevo, a manos del '
                           'nacionalista serbio {Gavrilo Princip}.',
                           'La {Triple Entente} (1907) agrupó a Francia, '
                           'Gran Bretaña y Rusia, luego Serbia; también '
                           'llamada los «{aliados}».',
                           'La {Triple Alianza} agrupó a Alemania, '
                           'Austria-Hungría e Italia; Italia luego se pasó '
                           'al bando de la {Entente}.',
                           'Los {imperios centrales} (Alemania y '
                           'Austria-Hungría) perdieron finalmente la '
                           'guerra.']},
                {'titulo': '18.2 PRIMERA GUERRA MUNDIAL: CAUSAS Y '
                           'CONSECUENCIAS',
                 'items': ['Entre las causas están la agresiva política '
                           '{alemana} por el predominio europeo, el '
                           'desarrollo industrial con expansión {colonial}, '
                           'y el acentuado {nacionalismo}.',
                           'La guerra causó la pérdida de más de {10} '
                           'millones de vidas humanas y 30 millones de '
                           'heridos y desaparecidos.',
                           'Surgieron {Estados Unidos} y Japón como nuevas '
                           'potencias mundiales tras la guerra.',
                           'En {Rusia} se estableció el primer Estado '
                           'autodenominado comunista de la historia, tras la '
                           'caída de la monarquía de los {zares}.']},
                {'titulo': '18.3 LA DEPRESIÓN MUNDIAL DE 1929',
                 'items': ['El «{jueves negro}» ocurrió el 24 de octubre de '
                           '1929, día del inicio del desplome de la bolsa de '
                           'valores de {Nueva York}.',
                           'Cinco días después llegó el «{martes negro}», la '
                           'jornada más sombría de Wall Street, extendiendo '
                           'la crisis a casi todo el mundo.',
                           'Hacia 1932, más de {5000} bancos habían quebrado '
                           'en Estados Unidos.',
                           'En 1932, tres años después del crac, la '
                           'producción mundial había descendido casi un '
                           '{40}%, y el comercio internacional se redujo a '
                           'un tercio.',
                           'Los trabajadores urbanos vieron reducidos sus '
                           'ingresos a casi la {mitad}, y muchos '
                           'agricultores emigraron a las ciudades en busca '
                           'de empleo.']},
                {'titulo': '18.4 SEGUNDA GUERRA MUNDIAL: CONTEXTO Y LÍDERES',
                 'items': ['La Segunda Guerra Mundial se inició en {1939} y '
                           'culminó en 1945, enfrentando a los bloques del '
                           '{Eje} y los Aliados.',
                           'Líderes del Eje: {Adolfo Hitler} (Alemania), '
                           '{Benito Mussolini} (Italia, fundador del '
                           'fascismo), y Hideki Tojo (primer ministro '
                           'japonés).',
                           'Líderes aliados: {Winston Churchill} (Gran '
                           'Bretaña), Franklin Roosevelt (EE.UU.), y {José '
                           'Stalin} (Unión Soviética).',
                           'El genocidio nazi, dirigido principalmente '
                           'contra los {judíos}, y el empleo de la {bomba '
                           'atómica} marcaron un hito macabro en la '
                           'historia.']},
                {'titulo': '18.5 SEGUNDA GUERRA MUNDIAL: CAUSAS',
                 'items': ['Alemania había sido humillada tras la Primera '
                           'Guerra por el Tratado de {Versalles}.',
                           'Fracasó la {Sociedad de Naciones}, creada en '
                           '1920, al no contar con países como Estados '
                           'Unidos, Alemania, Italia y Japón.',
                           'El ascenso del {fascismo} aprovechó las crisis '
                           'económicas de las débiles democracias europeas.',
                           'Hitler reclamó el «{espacio vital}» para '
                           'Alemania, armó un ejército poderoso y formó el '
                           'eje {Roma-Berlín-Tokio}.',
                           'El {imperialismo japonés} buscó apropiarse de '
                           'Asia, teniendo a China como principal víctima.']},
                {'titulo': '18.6 SEGUNDA GUERRA MUNDIAL: CONSECUENCIAS',
                 'items': ['La guerra causó la pérdida de más de {55} '
                           'millones de vidas humanas, entre civiles y '
                           'militares.',
                           'Se consolidaron {Estados Unidos} y la {Unión '
                           'Soviética} como las dos grandes potencias '
                           'mundiales.',
                           'Alemania fue dividida en {cuatro} zonas de '
                           'ocupación, dando origen luego a la República '
                           'Federal Alemana y la República Democrática '
                           'Alemana.',
                           'Se creó la {Organización de las Naciones Unidas} '
                           '(ONU) en 1945, sustituyendo a la Sociedad de '
                           'Naciones.']},
                {'titulo': '18.7 LA GUERRA FRÍA: CAUSAS Y CONSECUENCIAS',
                 'items': ['La {Guerra Fría} fue el conflicto indirecto '
                           'entre Estados Unidos y la Unión Soviética, entre '
                           '1947 y {1991}.',
                           'Se caracterizó por el intento de ambas '
                           'superpotencias de extender sus modelos '
                           'ideológicos sin llegar al enfrentamiento '
                           '{directo}.',
                           'Entre sus episodios más sonados están la '
                           'división de Alemania y el {Muro de Berlín}, la '
                           'Guerra de Corea, la crisis de los misiles '
                           'cubanos y la Guerra de {Vietnam}.',
                           'La causa principal fue la incompatibilidad entre '
                           'el modelo {capitalista} estadounidense y el '
                           'modelo {comunista} soviético.',
                           'La Guerra Fría terminó en 1989 con la '
                           'declaración de {Malta}, entre George Bush y '
                           'Mijaíl Gorbachov.',
                           'Como consecuencia, se dio el desmantelamiento de '
                           'la {Unión Soviética}, la consolidación de EE.UU. '
                           'como única potencia, y el nacimiento de la '
                           '{globalización}.']}],
  'cuadros': [{'titulo': '18. LAS DOS GUERRAS MUNDIALES',
               'encabezados': ['Guerra', 'Años', 'Fin'],
               'filas': [['Primera', '{1914}–1918', 'Tratado de {Versalles}'],
                         ['Segunda',
                          '{1939}–{1945}',
                          'Bombas de {Hiroshima} y Nagasaki']]}],
  'preguntas': [{'pregunta': 'El periodo entre 1871 y 1914 en Europa, de '
                             'desarrollo económico pero creciente '
                             'armamentismo entre potencias, se conoció como:',
                 'alternativas': ['El Concierto Europeo',
                                  'La Belle Époque',
                                  'La Era Victoriana',
                                  'El Equilibrio de Poderes',
                                  'La Paz Armada'],
                 'correcta': 'E'},
                {'pregunta': 'El asesinato que sirvió de pretexto para el '
                             'inicio de la Primera Guerra Mundial fue el del '
                             'archiduque:',
                 'alternativas': ['Nicolás II',
                                  'Otto von Bismarck',
                                  'Francisco José',
                                  'Francisco Fernando',
                                  'Guillermo II'],
                 'correcta': 'D'},
                {'pregunta': 'La Triple Entente, formada en 1907, agrupó a '
                             'Francia, Gran Bretaña y:',
                 'alternativas': ['Estados Unidos',
                                  'Italia',
                                  'Rusia',
                                  'Serbia exclusivamente',
                                  'Bélgica'],
                 'correcta': 'C'},
                {'pregunta': 'La Primera Guerra Mundial causó la pérdida de '
                             'más de 10 millones de vidas y el surgimiento '
                             'de nuevas potencias como Estados Unidos y:',
                 'alternativas': ['Alemania',
                                  'Japón',
                                  'China',
                                  'Italia',
                                  'España'],
                 'correcta': 'B'},
                {'pregunta': 'Tras la Primera Guerra Mundial, en Rusia se '
                             'estableció el primer Estado autodenominado:',
                 'alternativas': ['Fascista',
                                  'Democrático liberal',
                                  'Monárquico constitucional',
                                  'Comunista',
                                  'Republicano'],
                 'correcta': 'D'},
                {'pregunta': 'El día del inicio del desplome de la bolsa de '
                             'valores de Nueva York en 1929 se conoció como:',
                 'alternativas': ['Jueves negro',
                                  'Miércoles negro',
                                  'Viernes negro',
                                  'Lunes negro',
                                  'Martes negro'],
                 'correcta': 'A'},
                {'pregunta': 'Hacia 1932, la cantidad de bancos que habían '
                             'quebrado en Estados Unidos como consecuencia '
                             'de la crisis de 1929 fue de más de:',
                 'alternativas': ['10000', '1000', '2000', '5000', '500'],
                 'correcta': 'D'},
                {'pregunta': 'La Segunda Guerra Mundial se inició en 1939 y '
                             'culminó en:',
                 'alternativas': ['1945', '1941', '1947', '1943', '1944'],
                 'correcta': 'A'},
                {'pregunta': 'El dictador italiano, fundador del fascismo, '
                             'que se alió con Hitler durante la Segunda '
                             'Guerra Mundial fue:',
                 'alternativas': ['Miklós Horthy',
                                  'Ion Antonescu',
                                  'Benito Mussolini',
                                  'Francisco Franco',
                                  'Hideki Tojo'],
                 'correcta': 'C'},
                {'pregunta': 'El primer ministro inglés que animó a los '
                             'ingleses a enfrentarse a la Alemania de Hitler '
                             'fue:',
                 'alternativas': ['Neville Chamberlain',
                                  'Anthony Eden',
                                  'Winston Churchill',
                                  'Stanley Baldwin',
                                  'Clement Attlee'],
                 'correcta': 'C'},
                {'pregunta': 'El tratado que humilló a Alemania tras la '
                             'Primera Guerra Mundial, generando '
                             'resentimiento que contribuyó a la Segunda, fue '
                             'el Tratado de:',
                 'alternativas': ['Versalles',
                                  'Brest-Litovsk',
                                  'Rapallo',
                                  'Neuilly',
                                  'Locarno'],
                 'correcta': 'A'},
                {'pregunta': 'El organismo internacional creado en 1920 que '
                             'fracasó en evitar la Segunda Guerra Mundial '
                             'fue:',
                 'alternativas': ['La Liga Panamericana',
                                  'La ONU',
                                  'El Pacto de Varsovia',
                                  'La OTAN',
                                  'La Sociedad de Naciones'],
                 'correcta': 'E'},
                {'pregunta': 'El eje de alianza formado por Alemania, Italia '
                             'y Japón durante la Segunda Guerra Mundial se '
                             'conoció como el eje:',
                 'alternativas': ['Tokio-Roma-Berlín',
                                  'Roma-Tokio-Berlín',
                                  'Roma-Berlín-Tokio',
                                  'Berlín-Tokio-Roma',
                                  'Berlín-Roma-Tokio'],
                 'correcta': 'C'},
                {'pregunta': 'La Segunda Guerra Mundial causó la pérdida de '
                             'más de 55 millones de vidas humanas, entre:',
                 'alternativas': ['Solo prisioneros de guerra',
                                  'Solo combatientes europeos',
                                  'Solo civiles',
                                  'Civiles y militares',
                                  'Solo militares'],
                 'correcta': 'D'},
                {'pregunta': 'Tras la Segunda Guerra Mundial, Alemania fue '
                             'dividida en un número de zonas de ocupación '
                             'igual a:',
                 'alternativas': ['Seis', 'Cuatro', 'Ocho', 'Tres', 'Dos'],
                 'correcta': 'B'},
                {'pregunta': 'El organismo internacional creado en 1945 que '
                             'sustituyó a la Sociedad de Naciones fue:',
                 'alternativas': ['La Unión Europea',
                                  'El Pacto de Varsovia',
                                  'La Liga Árabe',
                                  'La OTAN',
                                  'La Organización de las Naciones Unidas '
                                  '(ONU)'],
                 'correcta': 'E'},
                {'pregunta': 'La Guerra Fría, conflicto indirecto entre '
                             'Estados Unidos y la Unión Soviética, se '
                             'desarrolló entre 1947 y:',
                 'alternativas': ['1989', '1991', '2000', '1995', '1985'],
                 'correcta': 'B'},
                {'pregunta': 'Entre los episodios más sonados de la Guerra '
                             'Fría están la crisis de los misiles cubanos y '
                             'la Guerra de:',
                 'alternativas': ['Afganistán exclusivamente',
                                  'Corea exclusivamente',
                                  'Independencia de la India',
                                  'Vietnam',
                                  'Las Malvinas'],
                 'correcta': 'D'},
                {'pregunta': 'La causa principal de la Guerra Fría fue la '
                             'incompatibilidad entre el modelo capitalista '
                             'estadounidense y el modelo:',
                 'alternativas': ['Monárquico soviético',
                                  'Anarquista soviético',
                                  'Comunista soviético',
                                  'Socialdemócrata soviético',
                                  'Fascista soviético'],
                 'correcta': 'C'},
                {'pregunta': 'La Guerra Fría terminó en 1989 con la '
                             'declaración de Malta, entre George Bush y:',
                 'alternativas': ['Nikita Jrushchov',
                                  'Vladimir Putin',
                                  'Leonid Brézhnev',
                                  'Boris Yeltsin',
                                  'Mijaíl Gorbachov'],
                 'correcta': 'E'}],
  'resumen_visual': [{'titulo': 'PRIMERA GUERRA MUNDIAL: CONTEXTO Y BLOQUES',
                      'items': ['Entre 1871 y 1914, Europa vivió la llamada '
                                '«Paz Armada», periodo de desarrollo '
                                'económico pero de creciente rivalidad y '
                                'armamentismo entre potencias.',
                                'El pretexto de la guerra fue el asesinato '
                                'del archiduque Francisco Fernando, heredero '
                                'austro-húngaro, en Sarajevo, a manos del '
                                'nacionalista serbio Gavrilo Princip.',
                                'La Triple Entente (1907) agrupó a Francia, '
                                'Gran Bretaña y Rusia, luego Serbia; también '
                                'llamada los «aliados».',
                                'La Triple Alianza agrupó a Alemania, '
                                'Austria-Hungría e Italia; Italia luego se '
                                'pasó al bando de la Entente.',
                                'Los imperios centrales (Alemania y '
                                'Austria-Hungría) perdieron finalmente la '
                                'guerra.']},
                     {'titulo': 'PRIMERA GUERRA MUNDIAL: CAUSAS Y '
                                'CONSECUENCIAS',
                      'items': ['Entre las causas están la agresiva política '
                                'alemana por el predominio europeo, el '
                                'desarrollo industrial con expansión '
                                'colonial, y el acentuado nacionalismo.',
                                'La guerra causó la pérdida de más de 10 '
                                'millones de vidas humanas y 30 millones de '
                                'heridos y desaparecidos.',
                                'Surgieron Estados Unidos y Japón como '
                                'nuevas potencias mundiales tras la guerra.',
                                'En Rusia se estableció el primer Estado '
                                'autodenominado comunista de la historia, '
                                'tras la caída de la monarquía de los '
                                'zares.']},
                     {'titulo': 'LA DEPRESIÓN MUNDIAL DE 1929',
                      'items': ['El «jueves negro» ocurrió el 24 de octubre '
                                'de 1929, día del inicio del desplome de la '
                                'bolsa de valores de Nueva York.',
                                'Cinco días después llegó el «martes negro», '
                                'la jornada más sombría de Wall Street, '
                                'extendiendo la crisis a casi todo el mundo.',
                                'Hacia 1932, más de 5000 bancos habían '
                                'quebrado en Estados Unidos.',
                                'En 1932, tres años después del crac, la '
                                'producción mundial había descendido casi un '
                                '40%, y el comercio internacional se redujo '
                                'a un tercio.',
                                'Los trabajadores urbanos vieron reducidos '
                                'sus ingresos a casi la mitad, y muchos '
                                'agricultores emigraron a las ciudades en '
                                'busca de empleo.']},
                     {'titulo': 'SEGUNDA GUERRA MUNDIAL: CONTEXTO Y LÍDERES',
                      'items': ['La Segunda Guerra Mundial se inició en 1939 '
                                'y culminó en 1945, enfrentando a los '
                                'bloques del Eje y los Aliados.',
                                'Líderes del Eje: Adolfo Hitler (Alemania), '
                                'Benito Mussolini (Italia, fundador del '
                                'fascismo), y Hideki Tojo (primer ministro '
                                'japonés).',
                                'Líderes aliados: Winston Churchill (Gran '
                                'Bretaña), Franklin Roosevelt (EE.UU.), y '
                                'José Stalin (Unión Soviética).',
                                'El genocidio nazi, dirigido principalmente '
                                'contra los judíos, y el empleo de la bomba '
                                'atómica marcaron un hito macabro en la '
                                'historia.']},
                     {'titulo': 'SEGUNDA GUERRA MUNDIAL: CAUSAS',
                      'items': ['Alemania había sido humillada tras la '
                                'Primera Guerra por el Tratado de Versalles.',
                                'Fracasó la Sociedad de Naciones, creada en '
                                '1920, al no contar con países como Estados '
                                'Unidos, Alemania, Italia y Japón.',
                                'El ascenso del fascismo aprovechó las '
                                'crisis económicas de las débiles '
                                'democracias europeas.',
                                'Hitler reclamó el «espacio vital» para '
                                'Alemania, armó un ejército poderoso y formó '
                                'el eje Roma-Berlín-Tokio.',
                                'El imperialismo japonés buscó apropiarse de '
                                'Asia, teniendo a China como principal '
                                'víctima.']},
                     {'titulo': 'SEGUNDA GUERRA MUNDIAL: CONSECUENCIAS',
                      'items': ['La guerra causó la pérdida de más de 55 '
                                'millones de vidas humanas, entre civiles y '
                                'militares.',
                                'Se consolidaron Estados Unidos y la Unión '
                                'Soviética como las dos grandes potencias '
                                'mundiales.',
                                'Alemania fue dividida en cuatro zonas de '
                                'ocupación, dando origen luego a la '
                                'República Federal Alemana y la República '
                                'Democrática Alemana.',
                                'Se creó la Organización de las Naciones '
                                'Unidas (ONU) en 1945, sustituyendo a la '
                                'Sociedad de Naciones.']},
                     {'titulo': 'LA GUERRA FRÍA: CAUSAS Y CONSECUENCIAS',
                      'items': ['La Guerra Fría fue el conflicto indirecto '
                                'entre Estados Unidos y la Unión Soviética, '
                                'entre 1947 y 1991.',
                                'Se caracterizó por el intento de ambas '
                                'superpotencias de extender sus modelos '
                                'ideológicos sin llegar al enfrentamiento '
                                'directo.',
                                'Entre sus episodios más sonados están la '
                                'división de Alemania y el Muro de Berlín, '
                                'la Guerra de Corea, la crisis de los '
                                'misiles cubanos y la Guerra de Vietnam.',
                                'La causa principal fue la incompatibilidad '
                                'entre el modelo capitalista estadounidense '
                                'y el modelo comunista soviético.',
                                'La Guerra Fría terminó en 1989 con la '
                                'declaración de Malta, entre George Bush y '
                                'Mijaíl Gorbachov.',
                                'Como consecuencia, se dio el '
                                'desmantelamiento de la Unión Soviética, la '
                                'consolidación de EE.UU. como única '
                                'potencia, y el nacimiento de la '
                                'globalización.']}],
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
  'secciones': [{'titulo': '19.1 EL OCHENIO DE MANUEL A. ODRÍA (1948-1956)',
                 'items': ['El 27 de octubre de 1948, el general {Manuel A. '
                           'Odría} se pronunció desde Arequipa contra el '
                           'gobierno de {José Luis Bustamante y Rivero}, en '
                           'la «Revolución Restauradora de Arequipa».',
                           'Odría gobernó bajo el lema político «{Salud, '
                           'Educación y Trabajo}».',
                           'Reconstruyó la ciudad del {Cusco}, destruida por '
                           'el terremoto del 21 de mayo de 1950.',
                           'El 5 de setiembre de 1955 se estableció el '
                           '{sufragio femenino} en las elecciones políticas, '
                           'mediante decreto ley 12391.',
                           'Se construyeron las {Grandes Unidades Escolares} '
                           'en todo el país, y unidades vecinales como '
                           'Matute para obreros y empleados.']},
                {'titulo': '19.2 PRIMER GOBIERNO DE FERNANDO BELAÚNDE TERRY '
                           '(1963-1968)',
                 'items': ['El gobierno firmó con la petrolera IPC '
                           '(International Petroleum Company) el {Acta de '
                           'Talara}, cuya página once, con privilegios a la '
                           'empresa, misteriosamente se extravió.',
                           'Este escándalo, conocido como la «{página '
                           'once}», precipitó el golpe de Estado del 3 de '
                           'octubre de 1968 liderado por el general {Juan '
                           'Velasco Alvarado}.',
                           'Se construyó la carretera «{Marginal de la '
                           'Selva}» y el aeropuerto internacional {Jorge '
                           'Chávez}.',
                           'Se emitió la Ley de {Cooperativas} (15260) y se '
                           'decretó la gratuidad de la enseñanza en todos '
                           'los niveles.']},
                {'titulo': '19.3 GOBIERNO MILITAR DE JUAN VELASCO ALVARADO '
                           '(1968-1975)',
                 'items': ['Velasco asumió como jefe del «{Gobierno '
                           'Revolucionario} de las Fuerzas Armadas», dejando '
                           'de lado la Constitución de 1933 y redactando el '
                           '«{Plan Inca}».',
                           'El 9 de octubre de 1968 estatizó el petróleo, '
                           'nacionalizando la {IPC} y llamando a esa fecha '
                           'el «Día de la {Dignidad Nacional}».',
                           'Implementó la {Reforma Agraria} mediante el '
                           'Decreto Ley N.º {17716}, del 24 de junio de '
                           '1969, expropiando latifundios.',
                           'La Reforma Educativa, bajo el lema «Un hombre '
                           'nuevo para una nueva sociedad», oficializó el '
                           '{quechua}.',
                           'Nacionalizó empresas mineras creando {HIERRO '
                           'PERÚ}, y la empresa eléctrica creando {ELECTRO '
                           'PERÚ}.',
                           'En 1975, Francisco Morales Bermúdez dio un '
                           'contragolpe de Estado contra Velasco en {Tacna}, '
                           'frustrando una posible invasión militar a '
                           'Chile.']},
                {'titulo': '19.4 SEGUNDA FASE MILITAR: FRANCISCO MORALES '
                           'BERMÚDEZ (1975-1980)',
                 'items': ['Morales Bermúdez llevó a cabo la contrarreforma '
                           'con el «Plan {Túpac Amaru}».',
                           'Convocó a una Asamblea Constituyente en 1978, '
                           'presidida por {Víctor Raúl Haya de la Torre}.',
                           'Esta Asamblea redactó la nueva {Constitución de '
                           '1979}, que derogó la de 1933.',
                           'Su gobierno restituyó el poder a los {civiles}, '
                           'iniciando la transición a la democracia.']},
                {'titulo': '19.5 SEGUNDO GOBIERNO DE BELAÚNDE: REGRESO A LA '
                           'DEMOCRACIA (1980-1985)',
                 'items': ['Belaúnde regresó al poder tras vencer en las '
                           'elecciones de 1980 a {Armando Villanueva del '
                           'Campo}.',
                           'Se produjo el conflicto con {Ecuador} en la '
                           'Cordillera del Cóndor (el «falso {Paquisha}»); '
                           'las tropas peruanas fueron comandadas por Rafael '
                           'Hoyos Rubio.',
                           'Aparecieron los movimientos alzados en armas '
                           '{Sendero Luminoso} y el MRTA.',
                           'Ocurrió la masacre de {Uchuraccay}, en Ayacucho, '
                           'donde fueron asesinados varios periodistas.',
                           'El papa {Juan Pablo II} visitó el Perú en '
                           'febrero de 1985 y coronó a la Virgen del Carmen '
                           'de Paucartambo en Sacsayhuamán.']},
                {'titulo': '19.6 PRIMER GOBIERNO DE ALAN GARCÍA (1985-1990): '
                           'LA DÉCADA DE LA CRISIS',
                 'items': ['Alan García fue el presidente electo más joven '
                           'del Perú, con {35} años; representó la primera '
                           'llegada al poder del {APRA} desde su fundación '
                           'en 1924.',
                           'Se descubrió el reservorio de gas de {Camisea}, '
                           'en el Cusco, y petróleo en Ucayali.',
                           'Promovió la ley de {Estatización de la Banca}, '
                           'lo que originó el surgimiento del Movimiento '
                           'Libertad, liderado por {Mario Vargas Llosa}.',
                           'García se negó a pagar más del {10}% de la deuda '
                           'externa, lo que aisló al Perú del crédito '
                           'financiero internacional.',
                           'Cambió la moneda del Sol al {Inti}, lo que '
                           'ocasionó una fuerte devaluación monetaria en '
                           'medio de hiperinflación.']},
                {'titulo': '19.7 PRIMER GOBIERNO DE ALBERTO FUJIMORI '
                           '(1990-1995)',
                 'items': ['Fujimori llegó al poder con su movimiento '
                           '{Cambio 90}, derrotando en elecciones al '
                           'novelista {Mario Vargas Llosa}.',
                           'Dio un {autogolpe} de Estado en abril de 1992, '
                           'disolviendo el Congreso.',
                           'En agosto de 1990 decretó el «{fujishock}» '
                           '(paquetazo económico), a través de su premier '
                           'Juan Carlos Hurtado Miller.',
                           'Se elaboró una nueva {Constitución}, neoliberal '
                           'y reeleccionista, vigente desde 1993.',
                           'Creó el {RENIEC}, la SUNAT, el INDECOPI, '
                           'FONCODES y la ONPE.',
                           'El grupo paramilitar «{Colina}» ejecutó la '
                           'masacre de Barrios Altos y el asesinato de '
                           'estudiantes y un profesor de La Cantuta.',
                           'Se capturó a {Abimael Guzmán}, jefe de Sendero '
                           'Luminoso, y se cambió la moneda de Inti a {Nuevo '
                           'Sol}.']},
                {'titulo': '19.8 SEGUNDO Y TERCER GOBIERNO DE FUJIMORI '
                           '(1995-2000)',
                 'items': ['En su segundo gobierno, Fujimori derrotó a '
                           '{Javier Pérez de Cuéllar} en las elecciones de '
                           '1995.',
                           'Se firmó la paz definitiva con {Ecuador} en '
                           '1998, cediendo 1 km² de territorio en {Tiwinza}.',
                           'El grupo {MRTA} tomó la residencia del embajador '
                           'de Japón; los rehenes fueron liberados por el '
                           'comando «{Chavín de Huántar}».',
                           'En el 2000, Fujimori venció en elecciones '
                           'fraudulentas a {Alejandro Toledo}, iniciando su '
                           'tercer gobierno.',
                           'Se descubrieron los «{Vladivideos}», que '
                           'evidenciaron la corrupción del régimen a través '
                           'de Vladimiro Montesinos.',
                           'Fujimori renunció por fax desde {Japón}; el '
                           'Congreso, presidido por Valentín Paniagua, lo '
                           'vacó por incapacidad moral.']},
                {'titulo': '19.9 GOBIERNO TRANSITORIO DE VALENTÍN PANIAGUA '
                           '(2000-2001)',
                 'items': ['{Valentín Paniagua} asumió la presidencia '
                           'provisional tras la renuncia de Fujimori y de '
                           'ambos vicepresidentes.',
                           'Se dio el contrato de concesión del {Lote 88} de '
                           'Camisea, firmado en diciembre de 2000.',
                           'Su gobierno inició la investigación de los actos '
                           'de {corrupción} de la década fujimorista.',
                           'Entregó el mando el 28 de julio a {Alejandro '
                           'Toledo}, ganador de la segunda vuelta electoral '
                           'del 2001.']},
                {'titulo': '19.10 GOBIERNO DE ALEJANDRO TOLEDO (2001-2006)',
                 'items': ['En 2003 se presentó el informe final de la '
                           '{Comisión de la Verdad y Reconciliación}, '
                           'responsabilizando al Estado y a la subversión.',
                           'En 2005 ocurrió el «{Andahuaylazo}», cuando '
                           'Antauro Humala y los etnocaceristas tomaron una '
                           'comisaría.',
                           'Se capturó a {Alberto Fujimori} el 7 de '
                           'noviembre de 2005 en Chile, y se gestionó su '
                           'extradición.',
                           'Toledo impulsó el proyecto del gas de {Camisea} '
                           'y acuerdos de libre comercio con Estados '
                           'Unidos.']},
                {'titulo': '19.11 SEGUNDO GOBIERNO DE ALAN GARCÍA '
                           '(2006-2011)',
                 'items': ['García derrotó en segunda vuelta a {Ollanta '
                           'Humala} y se aprobaron TLC con EE.UU., China y '
                           'la Unión Europea.',
                           'En 2008 se creó el {Ministerio del Medio '
                           'Ambiente}, siendo su primer titular {Antonio '
                           'Brack Egg}.',
                           'Surgió el escándalo de los «{Petroaudios}» o '
                           'caso Business (2008), que provocó la caída del '
                           'gabinete de Jorge del Castillo.',
                           'Ocurrió «{El Baguazo}» en 2009, un conflicto '
                           'social que causó la caída del gabinete de Yehude '
                           'Simon.',
                           'En 2008, el Perú presentó una demanda contra '
                           '{Chile} ante la Corte Internacional de La Haya '
                           'por límites marítimos.']},
                {'titulo': '19.12 GOBIERNO DE OLLANTA HUMALA TASSO '
                           '(2011-2016)',
                 'items': ['Humala, líder del {Partido Nacionalista '
                           'Peruano}, derrotó en segunda vuelta a {Keiko '
                           'Fujimori}, con el apoyo de Mario Vargas Llosa.',
                           'Amplió y creó programas sociales como {Beca 18}, '
                           'Pensión 65 y Qali Warma.',
                           'Se desarrolló el conflicto minero de {Conga}, en '
                           'Cajamarca.',
                           'Promulgó la ley de {consulta previa} a los '
                           'pueblos indígenas.']}],
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
  'preguntas': [{'pregunta': 'El movimiento militar que depuso a José Luis '
                             'Bustamante y Rivero en 1948, liderado por '
                             'Manuel A. Odría, se llamó:',
                 'alternativas': ['Plan Túpac Amaru',
                                  'Plan Inca',
                                  'Contragolpe de Tacna',
                                  'Estatuto Revolucionario',
                                  'Revolución Restauradora de Arequipa'],
                 'correcta': 'E'},
                {'pregunta': 'El lema político bajo el cual gobernó Manuel '
                             'A. Odría fue:',
                 'alternativas': ['Un hombre nuevo para una nueva sociedad',
                                  'Paz y Desarrollo',
                                  'Orden y Progreso',
                                  'Pan, Tierra y Libertad',
                                  'Salud, Educación y Trabajo'],
                 'correcta': 'E'},
                {'pregunta': 'El escándalo de la «página once» extraviada, '
                             'referida al Acta de Talara, precipitó la caída '
                             'de:',
                 'alternativas': ['El gobierno de Fujimori',
                                  'El gobierno de García',
                                  'El gobierno de Odría',
                                  'El primer gobierno de Belaúnde Terry',
                                  'El gobierno de Morales Bermúdez'],
                 'correcta': 'D'},
                {'pregunta': 'El documento que estableció los lineamientos '
                             'del gobierno revolucionario de Juan Velasco '
                             'Alvarado se llamó:',
                 'alternativas': ['Estatuto de 1979',
                                  'Plan Inca',
                                  'Plan Restaurador',
                                  'Plan Túpac Amaru',
                                  'Acta de Talara'],
                 'correcta': 'B'},
                {'pregunta': 'El Decreto Ley N.º 17716, promulgado por '
                             'Velasco Alvarado en 1969, estableció la:',
                 'alternativas': ['Nacionalización eléctrica',
                                  'Ley de Regionalización',
                                  'Reforma Agraria',
                                  'Estatización de la Banca',
                                  'Reforma Educativa'],
                 'correcta': 'C'},
                {'pregunta': 'El general que dio un contragolpe de Estado '
                             'contra Velasco Alvarado en 1975, iniciando la '
                             'segunda fase del gobierno militar, fue:',
                 'alternativas': ['Valentín Paniagua',
                                  'Juan Velasco',
                                  'Manuel Odría',
                                  'Alberto Fujimori',
                                  'Francisco Morales Bermúdez'],
                 'correcta': 'E'},
                {'pregunta': 'La Asamblea Constituyente convocada por '
                             'Morales Bermúdez en 1978, que redactó la '
                             'Constitución de 1979, fue presidida por:',
                 'alternativas': ['Víctor Raúl Haya de la Torre',
                                  'Fernando Belaúnde',
                                  'Valentín Paniagua',
                                  'Manuel Odría',
                                  'Alan García'],
                 'correcta': 'A'},
                {'pregunta': 'Durante el segundo gobierno de Belaúnde Terry '
                             '(1980-1985), ocurrió el conflicto fronterizo '
                             'con Ecuador conocido como:',
                 'alternativas': ['La Guerra del Pacífico',
                                  'El Andahuaylazo',
                                  'El Baguazo',
                                  'El Cenepa',
                                  'El falso Paquisha'],
                 'correcta': 'E'},
                {'pregunta': 'La matanza de periodistas ocurrida en Ayacucho '
                             'durante el segundo gobierno de Belaúnde se '
                             'conoce como la masacre de:',
                 'alternativas': ['Barrios Altos',
                                  'Accomarca',
                                  'Uchuraccay',
                                  'Cayara',
                                  'La Cantuta'],
                 'correcta': 'C'},
                {'pregunta': 'El presidente electo más joven en la historia '
                             'del Perú, con 35 años de edad, fue:',
                 'alternativas': ['Ollanta Humala',
                                  'Alberto Fujimori',
                                  'Alejandro Toledo',
                                  'Alan García',
                                  'Fernando Belaúnde'],
                 'correcta': 'D'},
                {'pregunta': 'Durante el primer gobierno de Alan García se '
                             'descubrió el reservorio de gas natural de:',
                 'alternativas': ['Talara',
                                  'Sechura',
                                  'Zorritos',
                                  'Aguaytía',
                                  'Camisea'],
                 'correcta': 'E'},
                {'pregunta': 'La ley de Estatización de la Banca, promovida '
                             'por Alan García, propició el surgimiento del '
                             'movimiento liderado por:',
                 'alternativas': ['Alberto Fujimori',
                                  'Rafael Belaúnde',
                                  'Alfonso Barrantes',
                                  'Mario Vargas Llosa',
                                  'Javier Pérez de Cuéllar'],
                 'correcta': 'D'},
                {'pregunta': 'Durante el primer gobierno de García, la '
                             'moneda peruana cambió del Sol al:',
                 'alternativas': ['Nuevo Sol',
                                  'Real',
                                  'Inti',
                                  'Dólar',
                                  'Sucre'],
                 'correcta': 'C'},
                {'pregunta': 'Alberto Fujimori derrotó en las elecciones de '
                             '1990 al candidato:',
                 'alternativas': ['Alejandro Toledo',
                                  'Alfonso Barrantes',
                                  'Mario Vargas Llosa',
                                  'Alan García',
                                  'Javier Pérez de Cuéllar'],
                 'correcta': 'C'},
                {'pregunta': 'El paquete de medidas económicas de shock '
                             'aplicado por Fujimori en agosto de 1990 se '
                             'conoció popularmente como:',
                 'alternativas': ['El garcishock',
                                  'El fujishock',
                                  'El ajuste toledista',
                                  'La dolarización',
                                  'La estabilización'],
                 'correcta': 'B'},
                {'pregunta': 'El grupo paramilitar responsable de la masacre '
                             'de Barrios Altos y La Cantuta durante el '
                             'gobierno de Fujimori se llamó:',
                 'alternativas': ['Los Notables',
                                  'MRTA',
                                  'Sendero Luminoso',
                                  'Grupo Colina',
                                  'Comando Rodrigo Franco'],
                 'correcta': 'D'},
                {'pregunta': 'El territorio cedido a Ecuador tras la firma '
                             'de la paz definitiva en 1998, durante el '
                             'segundo gobierno de Fujimori, fue:',
                 'alternativas': ['Tiwinza',
                                  'La Cordillera del Cóndor completa',
                                  'Zarumilla',
                                  'El falso Paquisha',
                                  'Jaén'],
                 'correcta': 'A'},
                {'pregunta': 'Los documentos que evidenciaron la red de '
                             'corrupción de Vladimiro Montesinos durante el '
                             'fujimorismo se conocieron como:',
                 'alternativas': ['Wikileaks Perú',
                                  'Panama Papers',
                                  'Petroaudios',
                                  'Vladivideos',
                                  'BTR'],
                 'correcta': 'D'},
                {'pregunta': 'El presidente que asumió el gobierno '
                             'transitorio del Perú entre el 2000 y el 2001, '
                             'tras la renuncia de Fujimori, fue:',
                 'alternativas': ['Francisco Tudela',
                                  'Alan García',
                                  'Alejandro Toledo',
                                  'Valentín Paniagua',
                                  'Ricardo Márquez'],
                 'correcta': 'D'},
                {'pregunta': 'El informe final de la Comisión de la Verdad y '
                             'Reconciliación Nacional se presentó durante el '
                             'gobierno de:',
                 'alternativas': ['Alan García',
                                  'Ollanta Humala',
                                  'Valentín Paniagua',
                                  'Alejandro Toledo',
                                  'Alberto Fujimori'],
                 'correcta': 'D'},
                {'pregunta': 'El levantamiento de Antauro Humala y los '
                             'etnocaceristas en una comisaría, ocurrido en '
                             '2005, se conoce como:',
                 'alternativas': ['El Andahuaylazo',
                                  'El Baguazo',
                                  'La Marcha de los Cuatro Suyos',
                                  'El Conga',
                                  'El Cenepazo'],
                 'correcta': 'A'},
                {'pregunta': 'El primer titular del Ministerio del Ambiente, '
                             'creado en 2008 durante el segundo gobierno de '
                             'García, fue:',
                 'alternativas': ['Jorge del Castillo',
                                  'Manuel Pulgar-Vidal',
                                  'José Serra',
                                  'Antonio Brack Egg',
                                  'Yehude Simon'],
                 'correcta': 'D'},
                {'pregunta': 'El conflicto social ocurrido en 2009 que '
                             'provocó la caída del gabinete de Yehude Simon '
                             'se conoce como:',
                 'alternativas': ['El Andahuaylazo',
                                  'El Baguazo',
                                  'El Tía María',
                                  'El Conga',
                                  'El Espinar'],
                 'correcta': 'B'},
                {'pregunta': 'Los programas sociales Beca 18, Pensión 65 y '
                             'Qali Warma fueron ampliados o creados durante '
                             'el gobierno de:',
                 'alternativas': ['Valentín Paniagua',
                                  'Ollanta Humala',
                                  'Alberto Fujimori',
                                  'Alan García',
                                  'Alejandro Toledo'],
                 'correcta': 'B'}],
  'resumen_visual': [{'titulo': 'EL OCHENIO DE MANUEL A. ODRÍA (1948-1956) / '
                                'PRIMER GOBIERNO DE FERNANDO BEL',
                      'items': ['El 27 de octubre de 1948, el general Manuel '
                                'A. Odría se pronunció desde Arequipa contra '
                                'el gobierno de José Luis Bustamante y '
                                'Rivero, en la «Revolución Restauradora de '
                                'Arequipa».',
                                'Odría gobernó bajo el lema político «Salud, '
                                'Educación y Trabajo».',
                                'Reconstruyó la ciudad del Cusco, destruida '
                                'por el terremoto del 21 de mayo de 1950.',
                                'El 5 de setiembre de 1955 se estableció el '
                                'sufragio femenino en las elecciones '
                                'políticas, mediante decreto ley 12391.',
                                'El gobierno firmó con la petrolera IPC '
                                '(International Petroleum Company) el Acta '
                                'de Talara, cuya página once, con '
                                'privilegios a la empresa, misteriosamente '
                                'se extravió.',
                                'Este escándalo, conocido como la «página '
                                'once», precipitó el golpe de Estado del 3 '
                                'de octubre de 1968 liderado por el general '
                                'Juan Velasco Alvarado.',
                                'Se construyó la carretera «Marginal de la '
                                'Selva» y el aeropuerto internacional Jorge '
                                'Chávez.',
                                'Se emitió la Ley de Cooperativas (15260) y '
                                'se decretó la gratuidad de la enseñanza en '
                                'todos los niveles.']},
                     {'titulo': 'GOBIERNO MILITAR DE JUAN VELASCO ALVARADO '
                                '(1968-1975) / SEGUNDA FASE MILITA',
                      'items': ['Velasco asumió como jefe del «Gobierno '
                                'Revolucionario de las Fuerzas Armadas», '
                                'dejando de lado la Constitución de 1933 y '
                                'redactando el «Plan Inca».',
                                'El 9 de octubre de 1968 estatizó el '
                                'petróleo, nacionalizando la IPC y llamando '
                                'a esa fecha el «Día de la Dignidad '
                                'Nacional».',
                                'Implementó la Reforma Agraria mediante el '
                                'Decreto Ley N.º 17716, del 24 de junio de '
                                '1969, expropiando latifundios.',
                                'La Reforma Educativa, bajo el lema «Un '
                                'hombre nuevo para una nueva sociedad», '
                                'oficializó el quechua.',
                                'Morales Bermúdez llevó a cabo la '
                                'contrarreforma con el «Plan Túpac Amaru».',
                                'Convocó a una Asamblea Constituyente en '
                                '1978, presidida por Víctor Raúl Haya de la '
                                'Torre.',
                                'Esta Asamblea redactó la nueva Constitución '
                                'de 1979, que derogó la de 1933.',
                                'Su gobierno restituyó el poder a los '
                                'civiles, iniciando la transición a la '
                                'democracia.']},
                     {'titulo': 'SEGUNDO GOBIERNO DE BELAÚNDE: REGRESO A LA '
                                'DEMOCRACIA (1980-1985) / PRIMER ',
                      'items': ['Belaúnde regresó al poder tras vencer en '
                                'las elecciones de 1980 a Armando Villanueva '
                                'del Campo.',
                                'Se produjo el conflicto con Ecuador en la '
                                'Cordillera del Cóndor (el «falso '
                                'Paquisha»); las tropas peruanas fueron '
                                'comandadas por Rafael Hoyos Rubio.',
                                'Aparecieron los movimientos alzados en '
                                'armas Sendero Luminoso y el MRTA.',
                                'Ocurrió la masacre de Uchuraccay, en '
                                'Ayacucho, donde fueron asesinados varios '
                                'periodistas.',
                                'Alan García fue el presidente electo más '
                                'joven del Perú, con 35 años; representó la '
                                'primera llegada al poder del APRA desde su '
                                'fundación en 1924.',
                                'Se descubrió el reservorio de gas de '
                                'Camisea, en el Cusco, y petróleo en '
                                'Ucayali.',
                                'Promovió la ley de Estatización de la '
                                'Banca, lo que originó el surgimiento del '
                                'Movimiento Libertad, liderado por Mario '
                                'Vargas Llosa.',
                                'García se negó a pagar más del 10% de la '
                                'deuda externa, lo que aisló al Perú del '
                                'crédito financiero internacional.']},
                     {'titulo': 'PRIMER GOBIERNO DE ALBERTO FUJIMORI '
                                '(1990-1995) / SEGUNDO Y TERCER GOBIERNO',
                      'items': ['Fujimori llegó al poder con su movimiento '
                                'Cambio 90, derrotando en elecciones al '
                                'novelista Mario Vargas Llosa.',
                                'Dio un autogolpe de Estado en abril de '
                                '1992, disolviendo el Congreso.',
                                'En agosto de 1990 decretó el «fujishock» '
                                '(paquetazo económico), a través de su '
                                'premier Juan Carlos Hurtado Miller.',
                                'Se elaboró una nueva Constitución, '
                                'neoliberal y reeleccionista, vigente desde '
                                '1993.',
                                'En su segundo gobierno, Fujimori derrotó a '
                                'Javier Pérez de Cuéllar en las elecciones '
                                'de 1995.',
                                'Se firmó la paz definitiva con Ecuador en '
                                '1998, cediendo 1 km² de territorio en '
                                'Tiwinza.',
                                'El grupo MRTA tomó la residencia del '
                                'embajador de Japón; los rehenes fueron '
                                'liberados por el comando «Chavín de '
                                'Huántar».',
                                'En el 2000, Fujimori venció en elecciones '
                                'fraudulentas a Alejandro Toledo, iniciando '
                                'su tercer gobierno.']},
                     {'titulo': 'GOBIERNO TRANSITORIO DE VALENTÍN PANIAGUA '
                                '(2000-2001) / GOBIERNO DE ALEJAND',
                      'items': ['Valentín Paniagua asumió la presidencia '
                                'provisional tras la renuncia de Fujimori y '
                                'de ambos vicepresidentes.',
                                'Se dio el contrato de concesión del Lote 88 '
                                'de Camisea, firmado en diciembre de 2000.',
                                'Su gobierno inició la investigación de los '
                                'actos de corrupción de la década '
                                'fujimorista.',
                                'Entregó el mando el 28 de julio a Alejandro '
                                'Toledo, ganador de la segunda vuelta '
                                'electoral del 2001.',
                                'En 2003 se presentó el informe final de la '
                                'Comisión de la Verdad y Reconciliación, '
                                'responsabilizando al Estado y a la '
                                'subversión.',
                                'En 2005 ocurrió el «Andahuaylazo», cuando '
                                'Antauro Humala y los etnocaceristas tomaron '
                                'una comisaría.',
                                'Se capturó a Alberto Fujimori el 7 de '
                                'noviembre de 2005 en Chile, y se gestionó '
                                'su extradición.',
                                'Toledo impulsó el proyecto del gas de '
                                'Camisea y acuerdos de libre comercio con '
                                'Estados Unidos.']},
                     {'titulo': 'SEGUNDO GOBIERNO DE ALAN GARCÍA (2006-2011) '
                                '/ GOBIERNO DE OLLANTA HUMALA TA',
                      'items': ['García derrotó en segunda vuelta a Ollanta '
                                'Humala y se aprobaron TLC con EE.UU., China '
                                'y la Unión Europea.',
                                'En 2008 se creó el Ministerio del Medio '
                                'Ambiente, siendo su primer titular Antonio '
                                'Brack Egg.',
                                'Surgió el escándalo de los «Petroaudios» o '
                                'caso Business (2008), que provocó la caída '
                                'del gabinete de Jorge del Castillo.',
                                'Ocurrió «El Baguazo» en 2009, un conflicto '
                                'social que causó la caída del gabinete de '
                                'Yehude Simon.',
                                'Humala, líder del Partido Nacionalista '
                                'Peruano, derrotó en segunda vuelta a Keiko '
                                'Fujimori, con el apoyo de Mario Vargas '
                                'Llosa.',
                                'Amplió y creó programas sociales como Beca '
                                '18, Pensión 65 y Qali Warma.',
                                'Se desarrolló el conflicto minero de Conga, '
                                'en Cajamarca.',
                                'Promulgó la ley de consulta previa a los '
                                'pueblos indígenas.']}],
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


def generar_juegos_educativos(tema, con_claves=False, grado_txt="",
                              institucion="ACADEMIA YACHAY", area="Historia",
                              profesor="Prof. Alexander Córdova"):
    """PDF independiente con los juegos educativos del tema (Sudoku,
    Sopa de Letras, Mapa Mental, Crucigrama, Relación de Columnas,
    Verdadero o Falso) — descarga aparte, opcional, para no inflar la
    ficha principal. Solo tiene contenido real para Historia, Filosofía
    y Educación Cívica; para las demás áreas devuelve None."""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                    Paragraph, Spacer, Table, TableStyle,
                                    NextPageTemplate, PageBreak, KeepTogether)
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    _area_check = (area or "").lower()
    if not ("historia" in _area_check or "filosof" in _area_check
            or "civic" in _area_check or "cívic" in _area_check):
        return None

    est = _estilos()
    buf = io.BytesIO()

    MX, MY = 1.3 * cm, 1.3 * cm
    ancho_util = A4[0] - 2 * MX
    col_w = (ancho_util - 0.7 * cm) / 2

    doc = BaseDocTemplate(buf, pagesize=A4, leftMargin=MX, rightMargin=MX,
                          topMargin=MY, bottomMargin=1.4 * cm)

    f_ancho = Frame(MX, 1.4 * cm, ancho_util, A4[1] - MY - 1.4 * cm, id="fa",
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    g_c1 = Frame(MX, 1.4 * cm, col_w, A4[1] - MY - 1.4 * cm, id="gc1",
                leftPadding=0, rightPadding=8, topPadding=0, bottomPadding=0)
    g_c2 = Frame(MX + col_w + 0.7 * cm, 1.4 * cm, col_w, A4[1] - MY - 1.4 * cm, id="gc2",
                leftPadding=8, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.area_actual = area
    doc.profesor_actual = profesor
    doc.addPageTemplates([
        PageTemplate(id="ancho", frames=[f_ancho], onPage=_pie),
        PageTemplate(id="resto", frames=[g_c1, g_c2], onPage=_pie)])

    st_ = []
    _banda_titulo(st_, tema,
                  "JUEGOS EDUCATIVOS · Sudoku · Sopa de Letras · Mapa Mental · "
                  "Crucigrama · Relación de Columnas · Verdadero o Falso"
                  + ("  ·  CON CLAVES" if con_claves else ""),
                  est, ancho_util, con_claves, area)

    # ------------------------------------------------------------------
    # JUEGOS EDUCATIVOS: solo para Historia y Filosofía por ahora.
    # Van SIEMPRE en página(s) nueva(s) para no cortarse a media hoja
    # (misma lección aprendida con el sudoku de Álgebra).
    # ------------------------------------------------------------------
    _area_normal = (area or "").lower()
    if ("historia" in _area_normal or "filosof" in _area_normal
            or "civic" in _area_normal or "cívic" in _area_normal):
        color_juegos = _color_area(area)
        semilla_juegos = (tema.get("num", 1) if isinstance(tema.get("num"), int) else 1) * 23

        st_.append(Spacer(1, 4))

        def _titulo_juego(texto):
            t = Table([[Paragraph(f"<b>{texto}</b>", est["h"])]], colWidths=[ancho_util])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(color_juegos)),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            return t

        from reportlab.platypus import KeepTogether

        # --- Sudoku: 3 niveles, celdas mas chicas para que quepa mas ---
        st_.append(_titulo_juego(f"🧩 DESAFÍO SUDOKU · {tema['titulo'].upper()}"))
        st_.append(Spacer(1, 8))
        for nivel_nombre, nivel_clave in [("Fácil", "facil"), ("Medio", "medio"),
                                          ("Difícil", "dificil")]:
            puzzle, solucion = _sudoku_puzzle(nivel_clave, semilla=semilla_juegos)
            semilla_juegos += 1
            bloque_sudoku = [
                Paragraph(f"<b>Nivel {nivel_nombre}</b>", est["n"]),
                Spacer(1, 3),
                _tabla_sudoku(solucion if con_claves else puzzle, color_juegos,
                             tam_celda=0.8),
            ]
            st_.append(KeepTogether(bloque_sudoku))
            st_.append(Spacer(1, 8))

        # --- Sopa de letras: 2 niveles de dificultad ---
        st_.append(PageBreak())
        st_.append(Spacer(1, 4))
        st_.append(_titulo_juego(f"🔤 SOPA DE LETRAS · {tema['titulo'].upper()}"))
        st_.append(Spacer(1, 8))
        palabras_clave = _extraer_palabras_clave(tema, minimo=6, maximo=10)
        if palabras_clave:
            # Nivel 1: mas facil (menos palabras, grilla mas grande y despejada)
            st_.append(Paragraph("<b>Nivel 1 (más fácil)</b>", est["n"]))
            st_.append(Spacer(1, 3))
            grilla_facil, colocadas_facil = _generar_sopa_letras(
                palabras_clave[:6], tamano=15, semilla=semilla_juegos)
            st_.append(_tabla_sopa_letras(grilla_facil, color_juegos))
            st_.append(Spacer(1, 4))
            st_.append(Paragraph("Encuentra: " + " · ".join(colocadas_facil), est["n"]))
            st_.append(Spacer(1, 12))

            # Nivel 2: mas dificil (mas palabras, grilla mas apretada)
            st_.append(Paragraph("<b>Nivel 2 (más difícil)</b>", est["n"]))
            st_.append(Spacer(1, 3))
            grilla_dificil, colocadas_dificil = _generar_sopa_letras(
                palabras_clave, tamano=12, semilla=semilla_juegos + 1)
            st_.append(_tabla_sopa_letras(grilla_dificil, color_juegos, tam_celda=0.55))
            st_.append(Spacer(1, 4))
            st_.append(Paragraph("Encuentra: " + " · ".join(colocadas_dificil), est["n"]))

        # --- Mapa Mental para completar (técnica de Tony Buzan, usada
        # en todo el mundo para repaso y memorización visual) ---
        ramas_mapa = _armar_ramas_mapa_mental(tema, max_ramas=5, sub_por_rama=2)
        if len(ramas_mapa) >= 3:
            st_.append(PageBreak())
            st_.append(Spacer(1, 4))
            st_.append(_titulo_juego(f"🧠 MAPA MENTAL PARA COMPLETAR · {tema['titulo'].upper()}"))
            st_.append(Spacer(1, 6))
            st_.append(Paragraph(
                "Completa los espacios en blanco con los términos que faltan, "
                "usando lo que recuerdas del tema.", est["n"]))
            st_.append(Spacer(1, 8))
            dibujo_mapa = _dibujo_mapa_mental(tema["titulo"], ramas_mapa, color_juegos,
                                              con_claves=con_claves)
            st_.append(dibujo_mapa)

        # --- Crucigrama (pistas basadas en el contenido real) ---
        pares_cruci = _extraer_palabras_con_pista(tema, maximo=10)
        if len(pares_cruci) >= 4:
            st_.append(PageBreak())
            st_.append(Spacer(1, 4))
            st_.append(_titulo_juego(f"✏️ CRUCIGRAMA · {tema['titulo'].upper()}"))
            st_.append(Spacer(1, 8))
            grilla_cruci, colocadas_cruci = _generar_crucigrama(
                pares_cruci, tamano=16, semilla=semilla_juegos + 2)
            if grilla_cruci:
                grilla_cruci, colocadas_cruci = _recortar_grilla_crucigrama(
                    grilla_cruci, colocadas_cruci)
                numeradas = _numerar_crucigrama(colocadas_cruci)
                st_.append(_tabla_crucigrama(grilla_cruci, numeradas, color_juegos,
                                             mostrar_letras=con_claves))
                st_.append(Spacer(1, 10))
                horizontales = [f"{n}. {pista}" for n, p, pista, f, c, d in numeradas if d == "H"]
                verticales = [f"{n}. {pista}" for n, p, pista, f, c, d in numeradas if d == "V"]
                if horizontales:
                    st_.append(Paragraph("<b>HORIZONTALES</b>", est["n"]))
                    for h in horizontales:
                        st_.append(Paragraph(h, est["n"]))
                    st_.append(Spacer(1, 6))
                if verticales:
                    st_.append(Paragraph("<b>VERTICALES</b>", est["n"]))
                    for v in verticales:
                        st_.append(Paragraph(v, est["n"]))

        # --- Relación de columnas (termino <-> definicion real) ---
        # Cambia a plantilla de 2 columnas (como el cuerpo de la ficha)
        # para que quepa mas contenido por pagina, en vez de la ancha.
        if len(pares_cruci) >= 4:
            st_.append(NextPageTemplate("resto"))
            st_.append(PageBreak())
            st_.append(Spacer(1, 4))
            titulo_rc = Table([[Paragraph(f"<b>🔗 RELACIONA LAS COLUMNAS</b>", est["h"])]],
                              colWidths=[col_w - 6])
            titulo_rc.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(color_juegos)),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            st_.append(titulo_rc)
            st_.append(Spacer(1, 6))
            for num, (palabra, pista) in enumerate(pares_cruci[:10], start=1):
                st_.append(Paragraph(f"{num}. {palabra} → ______", est["n"]))
            st_.append(Spacer(1, 4))
            letras_op = "ABCDEFGHIJ"
            import random as _random_rc
            _indices_rc = list(range(len(pares_cruci[:10])))
            _random_rc.shuffle(_indices_rc)
            for j, idx in enumerate(_indices_rc):
                st_.append(Paragraph(f"{letras_op[j]}) {pares_cruci[idx][1]}", est["n"]))

            # --- Verdadero o Falso: afirmaciones "casi correctas" ---
            st_.append(Spacer(1, 10))
            titulo_vf = Table([[Paragraph(f"<b>✅❌ VERDADERO O FALSO</b>", est["h"])]],
                              colWidths=[col_w - 6])
            titulo_vf.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(color_juegos)),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            st_.append(titulo_vf)
            st_.append(Spacer(1, 6))
            afirmaciones_vf = _generar_verdadero_falso(
                pares_cruci, cantidad=8, semilla=semilla_juegos + 3)
            for i, (texto_afirmacion, es_verdadera) in enumerate(afirmaciones_vf, start=1):
                if con_claves:
                    marca = ("<font color='#2F7A4F'><b>[V]</b></font>" if es_verdadera
                            else "<font color='#B8390F'><b>[F]</b></font>")
                    st_.append(Paragraph(f"{i}. {marca} {texto_afirmacion}", est["n"]))
                else:
                    st_.append(Paragraph(f"{i}. (  V  /  F  ) {texto_afirmacion}", est["n"]))


    doc.build(st_)
    buf.seek(0)
    return _proteger_pdf(buf.getvalue())
