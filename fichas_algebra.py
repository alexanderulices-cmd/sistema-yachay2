# -*- coding: utf-8 -*-
"""
FICHAS DE ÁLGEBRA — CEPRU UNSAAC
Basado en el temario oficial (Resolución CU-575-2024-UNSAAC) y en los
exámenes reales de CEPRU Ordinario 2022-I (Área D).

FORMATO DISTINTO a Historia/Geografía/etc.: NO son dos documentos
separados (ficha + banco). Es UNA sola ficha por tema, con dos partes:
  1. Texto: conceptos y fórmulas clave (para completar espacios, igual
     estilo que las demás áreas).
  2. Ejercicios propuestos: preguntas reales de examen con 5
     alternativas cada una (sin espacio para resolver — son de opción
     múltiple, como el material fuente).

Reutiliza el motor visual de fichas_historia.py (colores, encabezado,
pie de página, marca de agua) pero con su propio generador de PDF,
_generar_ficha_algebra(), adaptado a contenido matemático.

ESTADO: 0 de 17 temas — recién iniciado.
Integración: se usa a través de academia_cepru.py, no directamente.
"""

from fichas_historia import (
    _color_area, _PATRON, _proteger_pdf, _partes, render_linea,
    _estilos, _banda_titulo, _logo_marca_agua_reader, _pie,
    balancear, muestrear, ENCABEZADO_L1, ENCABEZADO_L2, pie_legal,
)

LETRAS = ["A", "B", "C", "D", "E"]


def generar_ficha_algebra(tema, con_claves=False, grado_txt="",
                          area="Álgebra", profesor="Prof. Alexander Córdova"):
    """Genera la ficha combinada de Álgebra: teoría (para completar) +
    ejercicios propuestos con alternativas, en un solo PDF de máximo
    2 hojas."""
    import io
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                    Paragraph, Spacer, Table, TableStyle,
                                    KeepTogether, NextPageTemplate)
    from reportlab.lib import colors

    buf = io.BytesIO()
    MX, MY = 1.2 * cm, 1.3 * cm
    ancho_util = A4[0] - 2 * MX
    col_w = (ancho_util - 0.6 * cm) / 2

    doc = BaseDocTemplate(buf, pagesize=A4,
                          leftMargin=MX, rightMargin=MX,
                          topMargin=MY, bottomMargin=1.4 * cm)
    doc.area_actual = area

    alto_enc = 5.1 * cm
    f_enc = Frame(MX, A4[1] - MY - alto_enc, ancho_util, alto_enc, id="enc",
                 leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    alto_col = A4[1] - MY - alto_enc - 1.4 * cm
    f1 = Frame(MX, 1.4 * cm, col_w, alto_col, id="c1",
              leftPadding=0, rightPadding=6, topPadding=0, bottomPadding=0)
    f2 = Frame(MX + col_w + 0.6 * cm, 1.4 * cm, col_w, alto_col, id="c2",
              leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0)
    alto_full = A4[1] - MY - 1.4 * cm
    g1 = Frame(MX, 1.4 * cm, col_w, alto_full, id="g1",
              leftPadding=0, rightPadding=6, topPadding=0, bottomPadding=0)
    g2 = Frame(MX + col_w + 0.6 * cm, 1.4 * cm, col_w, alto_full, id="g2",
              leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0)

    doc.addPageTemplates([
        PageTemplate(id="p1", frames=[f_enc, f1, f2], onPage=_pie),
        PageTemplate(id="pn", frames=[g1, g2], onPage=_pie),
    ])

    est = _estilos()
    color_actual = _color_area(area)

    def barra(txt):
        t = Table([[Paragraph(f"<b>{txt}</b>", est["h"])]],
                  colWidths=[col_w - 6])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(color_actual)),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        return t

    st_ = []
    _banda_titulo(st_, tema,
                  f"{area.upper()} · Temario CEPRU-UNSAAC · " +
                  ("CLAVES PARA EL DOCENTE" if con_claves
                   else "Teoría + ejercicios propuestos"),
                  est, ancho_util, con_claves, area)

    if not con_claves:
        datos = Table([[
            "Apellidos y Nombres: ___________________________________",
            f"Grupo: {grado_txt}      Fecha: ____/____/______",
        ]], colWidths=[ancho_util * 0.62, ancho_util * 0.38])
        datos.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        st_.append(datos)

    st_.append(NextPageTemplate("pn"))
    st_.append(Spacer(1, 1))

    # ------------------------------------------------------------
    # PARTE 1: TEORÍA (conceptos y fórmulas, para completar)
    # ------------------------------------------------------------
    for sec in tema.get("secciones", []):
        st_.append(barra(sec["titulo"]))
        st_.append(Spacer(1, 3))
        for it in sec.get("items", []):
            texto_renderizado = render_linea(it, con_claves)
            st_.append(Paragraph(f"• {texto_renderizado}", est["n"]))
        st_.append(Spacer(1, 6))

    # ------------------------------------------------------------
    # PARTE 2: EJERCICIOS PROPUESTOS (opción múltiple, sin espacio
    # de resolución — son preguntas reales de examen CEPRU)
    # ------------------------------------------------------------
    ejercicios = tema.get("ejercicios", [])
    if ejercicios:
        st_.append(barra("EJERCICIOS PROPUESTOS"))
        st_.append(Spacer(1, 4))
        for i, ej in enumerate(ejercicios, start=1):
            bloque = [Paragraph(f"<b>{i}.</b> {ej['enunciado']}", est["preg"])]
            for j, alt in enumerate(ej["alternativas"]):
                letra = LETRAS[j]
                if con_claves and letra == ej["correcta"]:
                    txt_alt = (f'<font color="{color_actual}">'
                              f'<b>{letra}) {alt}</b></font>')
                else:
                    txt_alt = f"{letra}) {alt}"
                bloque.append(Paragraph(txt_alt, est["alt"]))
            st_.append(KeepTogether(bloque))
            st_.append(Spacer(1, 5))

    doc.build(st_)
    buf.seek(0)
    return _proteger_pdf(buf.getvalue())


# ================================================================
# TEMAS DE ÁLGEBRA (17, según temario oficial CU-575-2024-UNSAAC)
# ================================================================

BALOTAS_ALGEBRA = [
    {'num': 1, 'titulo': 'Potenciación', 'secciones': [{'titulo': '1.1 POTENCIACIÓN: DEFINICIÓN', 'items': ['La {potenciación} es la operación que consiste en multiplicar un número llamado base «a» tantas veces como indica otro número llamado exponente «n».', 'La potencia n-ésima de «a» se define: a<super>n</super> = a.a.a...a (n veces), con a ∈ R y n ∈ {Z<super>+</super>}.', '«a» es la {base}; «n» es el {exponente}; «a<super>n</super>» es la {potencia}.']}, {'titulo': '1.2 PROPIEDADES DE LA POTENCIACIÓN (I)', 'items': ['Producto de bases iguales: a<super>m</super> . a<super>n</super> = a<super>{m+n}</super>.', 'Cociente de bases iguales: a<super>m</super> ÷ a<super>n</super> = a<super>{m-n}</super>, con a ≠ 0.', 'Exponente {nulo o cero}: a<super>0</super> = 1, con a ≠ 0.', 'Exponente {negativo}: a<super>-n</super> = 1/a<super>n</super>, con a ≠ 0.', 'Potencia de potencia: (a<super>m</super>)<super>n</super> = a<super>{m.n}</super>.']}, {'titulo': '1.3 PROPIEDADES DE LA POTENCIACIÓN (II)', 'items': ['Potencia de un producto: (a.b)<super>n</super> = a<super>n</super> . {b<super>n</super>}.', 'Potencia de un cociente: (a/b)<super>n</super> = a<super>n</super>/{b<super>n</super>}, con a,b ≠ 0.', 'Exponente negativo de un cociente: (a/b)<super>-n</super> = ({b/a})<super>n</super>, con a,b ≠ 0.', 'Exponente fraccionario: a<super>m/n</super> = {<super>n</super>√(a<super>m</super>)}.']}, {'titulo': '1.4 RADICACIÓN: DEFINICIÓN Y ELEMENTOS', 'items': ['Una {radicación} se define: <super>n</super>√a = b &#8660; b<super>n</super> = a.', '«a» es el {radicando}; «n» es el {índice} del radical (n ∈ N, n ≥ 2); «b» es la raíz n-ésima de «a».']}, {'titulo': '1.5 PROPIEDADES DE LA RADICACIÓN', 'items': ['(<super>n</super>√a)<super>n</super> = {a}, con n ∈ N, n ≥ 2.', '<super>n</super>√(a<super>n</super>) = a si n es {par} (a≥0) o si n es {impar} (cualquier a).', '<super>n</super>√(a.b) = <super>n</super>√a . {<super>n</super>√b}, con n ∈ N.', '<super>n</super>√(a/b) = <super>n</super>√a / {<super>n</super>√b}, con b ≠ 0.', 'Raíz de raíz: <super>m</super>√(<super>n</super>√a) = {<super>m.n</super>√a}, con m,n ∈ N.', '<super>k.n</super>√(b<super>k.m</super>) = <super>n</super>√(b<super>m</super>) = {b<super>m/n</super>}, donde k ∈ N.']}, {'titulo': '1.6 ECUACIONES EXPONENCIALES: DEFINICIÓN Y PROPIEDADES', 'items': ['Las {ecuaciones exponenciales} son aquellas que contienen la incógnita en el exponente, y en otros casos como exponente y base a la vez.', 'Si a<super>x</super> = a<super>y</super>, entonces {x = y}, para todo a ∈ R<super>+</super>-{1}.', 'Si x<super>n</super> = y<super>n</super>, entonces {x = y}, para todo x,y ∈ R<super>+</super>, n ∈ Z<super>+</super>.', 'Si x<super>x</super> = a<super>a</super>, entonces {x = a}, para todo x,a ∈ R<super>+</super>.', 'Si x<super>n</super> = b, entonces {x = <super>n</super>√b}, con x ≥ 0, n ∈ Z<super>+</super>.']}], 'ejercicios': [{'enunciado': 'Al simplificar la expresión Q = (3<super>a+4</super>·9<super>a+2b</super>) / (27<super>a-1</super>·81<super>b+1</super>), se obtiene:', 'alternativas': ['27', '28', '23', '3', '9'], 'correcta': 'A'}, {'enunciado': 'El valor de «k» en la expresión k = (5<super>2n/(n-1)</super> + 35·5<super>2/(n-1)</super>) / <super>n-1</super>√(5<super>n+1</super>); n ≠ 1, es:', 'alternativas': ['10', '5', '12', '7', '2'], 'correcta': 'A'}, {'enunciado': 'Si se cumple que 3<super>n-1</super> = 2<super>2n</super>, el valor de la expresión A = (3<super>n+1</super> + 2<super>2n+1</super>) / (3<super>n</super> + 2<super>2n+3</super>), es:', 'alternativas': ['1', '5', '21', '10', '3'], 'correcta': 'B'}, {'enunciado': 'Si x<super>x</super> = 2, luego el valor de J = x<super>x·(x^x+1)</super>, es:', 'alternativas': ['2', '4', '√2', '1/2', '8'], 'correcta': 'B'}]},
]
