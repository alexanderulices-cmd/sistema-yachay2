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
    _generar_qr_bytes, _texto_qr_reto, _texto_qr_dato,
)

LETRAS = ["A", "B", "C", "D", "E"]


# ================================================================
# GENERADOR DE SUDOKU (2 niveles: medio y difícil)
# ================================================================

def _sudoku_resuelto():
    """Genera una grilla 9x9 de sudoku completamente resuelta y válida,
    usando backtracking con orden aleatorio (cada llamada da un
    resultado distinto)."""
    import random
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
        random.shuffle(numeros)
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
    """Genera un sudoku (grilla con huecos + su solución) según el
    nivel: 'medio' deja ~40 pistas, 'dificil' deja ~28 pistas."""
    import random
    if semilla is not None:
        random.seed(semilla)
    resuelto = _sudoku_resuelto()
    puzzle = [fila[:] for fila in resuelto]

    pistas_objetivo = 40 if nivel == "medio" else 28
    celdas = [(f, c) for f in range(9) for c in range(9)]
    random.shuffle(celdas)
    a_quitar = 81 - pistas_objetivo
    for f, c in celdas[:a_quitar]:
        puzzle[f][c] = 0

    if semilla is not None:
        random.seed()
    return puzzle, resuelto


def _tabla_sudoku(grilla, color_area, tam_celda=1.05):
    """Arma una tabla ReportLab 9x9 con estilo clásico de sudoku:
    bordes finos entre celdas, bordes gruesos cada 3 filas/columnas
    para marcar los bloques."""
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors

    datos = [[str(n) if n else "" for n in fila] for fila in grilla]
    t = Table(datos, colWidths=[tam_celda * cm] * 9,
             rowHeights=[tam_celda * cm] * 9)

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
                                    KeepTogether, NextPageTemplate, PageBreak)
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
            texto_renderizado = render_linea(it, True)
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

    # ------------------------------------------------------------
    # PARTE 3: DESAFÍO SUDOKU (nivel medio + nivel difícil)
    # Siempre en página nueva, para que nunca se corte por falta de
    # espacio en la columna donde terminaron los ejercicios.
    # ------------------------------------------------------------
    st_.append(PageBreak())
    st_.append(barra("DESAFÍO SUDOKU · ¡Ejercita tu lógica!"))
    st_.append(Spacer(1, 6))
    semilla_base = (tema.get("num", 1) if isinstance(tema.get("num"), int)
                    else 1) * 17
    puzzle_medio, sol_medio = _sudoku_puzzle("medio", semilla=semilla_base + 1)
    puzzle_dificil, sol_dificil = _sudoku_puzzle("dificil", semilla=semilla_base + 2)

    st_.append(Paragraph("<b>Nivel medio</b>", est["n"]))
    st_.append(Spacer(1, 3))
    st_.append(_tabla_sudoku(sol_medio if con_claves else puzzle_medio,
                             color_actual))
    st_.append(Spacer(1, 10))
    st_.append(Paragraph("<b>Nivel difícil</b>", est["n"]))
    st_.append(Spacer(1, 3))
    st_.append(_tabla_sudoku(sol_dificil if con_claves else puzzle_dificil,
                             color_actual))

    # ------------------------------------------------------------
    # QR: Reto Relámpago (3 preguntas con respuesta) + Dato Yachay
    # ------------------------------------------------------------
    qr_reto = tema.get("qr_reto")
    qr_dato = tema.get("qr_dato")
    if qr_reto or qr_dato:
        from reportlab.platypus import Image as RLImage
        st_.append(Spacer(1, 12))
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

    doc.build(st_)
    buf.seek(0)
    return _proteger_pdf(buf.getvalue())


# ================================================================
# TEMAS DE ÁLGEBRA (17, según temario oficial CU-575-2024-UNSAAC)
# ================================================================

BALOTAS_ALGEBRA = [{'num': 1,
  'titulo': 'Potenciación',
  'secciones': [{'titulo': '1.1 POTENCIACIÓN: DEFINICIÓN',
                 'items': ['La {potenciación} es la operación que consiste '
                           'en multiplicar un número llamado base «a» tantas '
                           'veces como indica otro número llamado exponente '
                           '«n».',
                           'La potencia n-ésima de «a» se define: '
                           'a<super>n</super> = a.a.a...a (n veces), con a ∈ '
                           'R y n ∈ {Z<super>+</super>}.',
                           '«a» es la {base}; «n» es el {exponente}; '
                           '«a<super>n</super>» es la {potencia}.']},
                {'titulo': '1.2 PROPIEDADES DE LA POTENCIACIÓN (I)',
                 'items': ['Producto de bases iguales: a<super>m</super> . '
                           'a<super>n</super> = a<super>{m+n}</super>.',
                           'Cociente de bases iguales: a<super>m</super> ÷ '
                           'a<super>n</super> = a<super>{m-n}</super>, con a '
                           '≠ 0.',
                           'Exponente {nulo o cero}: a<super>0</super> = 1, '
                           'con a ≠ 0.',
                           'Exponente {negativo}: a<super>-n</super> = '
                           '1/a<super>n</super>, con a ≠ 0.',
                           'Potencia de potencia: '
                           '(a<super>m</super>)<super>n</super> = '
                           'a<super>{m.n}</super>.']},
                {'titulo': '1.3 PROPIEDADES DE LA POTENCIACIÓN (II)',
                 'items': ['Potencia de un producto: (a.b)<super>n</super> = '
                           'a<super>n</super> . {b<super>n</super>}.',
                           'Potencia de un cociente: (a/b)<super>n</super> = '
                           'a<super>n</super>/{b<super>n</super>}, con a,b ≠ '
                           '0.',
                           'Exponente negativo de un cociente: '
                           '(a/b)<super>-n</super> = '
                           '({b/a})<super>n</super>, con a,b ≠ 0.',
                           'Exponente fraccionario: a<super>m/n</super> = '
                           '{<super>n</super>√(a<super>m</super>)}.']},
                {'titulo': '1.4 RADICACIÓN: DEFINICIÓN Y ELEMENTOS',
                 'items': ['Una {radicación} se define: <super>n</super>√a = '
                           'b &#8660; b<super>n</super> = a.',
                           '«a» es el {radicando}; «n» es el {índice} del '
                           'radical (n ∈ N, n ≥ 2); «b» es la raíz n-ésima '
                           'de «a».']},
                {'titulo': '1.5 PROPIEDADES DE LA RADICACIÓN',
                 'items': ['(<super>n</super>√a)<super>n</super> = {a}, con '
                           'n ∈ N, n ≥ 2.',
                           '<super>n</super>√(a<super>n</super>) = a si n es '
                           '{par} (a≥0) o si n es {impar} (cualquier a).',
                           '<super>n</super>√(a.b) = <super>n</super>√a . '
                           '{<super>n</super>√b}, con n ∈ N.',
                           '<super>n</super>√(a/b) = <super>n</super>√a / '
                           '{<super>n</super>√b}, con b ≠ 0.',
                           'Raíz de raíz: '
                           '<super>m</super>√(<super>n</super>√a) = '
                           '{<super>m.n</super>√a}, con m,n ∈ N.',
                           '<super>k.n</super>√(b<super>k.m</super>) = '
                           '<super>n</super>√(b<super>m</super>) = '
                           '{b<super>m/n</super>}, donde k ∈ N.']},
                {'titulo': '1.6 ECUACIONES EXPONENCIALES: DEFINICIÓN Y '
                           'PROPIEDADES',
                 'items': ['Las {ecuaciones exponenciales} son aquellas que '
                           'contienen la incógnita en el exponente, y en '
                           'otros casos como exponente y base a la vez.',
                           'Si a<super>x</super> = a<super>y</super>, '
                           'entonces {x = y}, para todo a ∈ '
                           'R<super>+</super>-{1}.',
                           'Si x<super>n</super> = y<super>n</super>, '
                           'entonces {x = y}, para todo x,y ∈ '
                           'R<super>+</super>, n ∈ Z<super>+</super>.',
                           'Si x<super>x</super> = a<super>a</super>, '
                           'entonces {x = a}, para todo x,a ∈ '
                           'R<super>+</super>.',
                           'Si x<super>n</super> = b, entonces {x = '
                           '<super>n</super>√b}, con x ≥ 0, n ∈ '
                           'Z<super>+</super>.']}],
  'ejercicios': [{'enunciado': 'Al simplificar la expresión Q = '
                               '(3<super>a+4</super>·9<super>a+2b</super>) / '
                               '(27<super>a-1</super>·81<super>b+1</super>), '
                               'se obtiene:',
                  'alternativas': ['27', '28', '23', '3', '9'],
                  'correcta': 'A'},
                 {'enunciado': 'El valor de «k» en la expresión k = '
                               '(5<super>2n/(n-1)</super> + '
                               '35·5<super>2/(n-1)</super>) / '
                               '<super>n-1</super>√(5<super>n+1</super>); n '
                               '≠ 1, es:',
                  'alternativas': ['10', '5', '12', '7', '2'],
                  'correcta': 'A'},
                 {'enunciado': 'Si se cumple que 3<super>n-1</super> = '
                               '2<super>2n</super>, el valor de la expresión '
                               'A = (3<super>n+1</super> + '
                               '2<super>2n+1</super>) / (3<super>n</super> + '
                               '2<super>2n+3</super>), es:',
                  'alternativas': ['1', '5', '21', '10', '3'],
                  'correcta': 'A'},
                 {'enunciado': 'Si x<super>x</super> = 2, luego el valor de '
                               'J = x<super>x·(x^x+1)</super>, es:',
                  'alternativas': ['2', '4', '√2', '1/2', '8'],
                  'correcta': 'E'},
                 {'enunciado': 'Al simplificar la expresión N = '
                               '(2<super>n+3</super> - 2<super>n+1</super>) '
                               '/ (2<super>n+2</super> + 2<super>n</super>), '
                               'se obtiene:',
                  'alternativas': ['6/5', '5/6', '8/5', '1', '2'],
                  'correcta': 'A'},
                 {'enunciado': 'Si 3<super>x</super> = 5, el valor de '
                               '3<super>2x</super> es:',
                  'alternativas': ['10', '15', '25', '5', '9'],
                  'correcta': 'C'},
                 {'enunciado': 'Al simplificar √8 · √2, se obtiene:',
                  'alternativas': ['2', '3', '4', '6', '8'],
                  'correcta': 'C'},
                 {'enunciado': 'Si x<super>1/2</super> = 3, el valor de «x» '
                               'es:',
                  'alternativas': ['3', '6', '9', '1/9', '1/3'],
                  'correcta': 'C'},
                 {'enunciado': 'Al simplificar (2<super>5</super> · '
                               '2<super>3</super>) / 2<super>6</super>, se '
                               'obtiene:',
                  'alternativas': ['2', '4', '8', '16', '1'],
                  'correcta': 'B'},
                 {'enunciado': 'Si 5<super>x-1</super> = 25, el valor de «x» '
                               'es:',
                  'alternativas': ['1', '2', '3', '4', '5'],
                  'correcta': 'C'},
                 {'enunciado': 'El valor de <super>3</super>√27 + √16 es:',
                  'alternativas': ['5', '6', '7', '8', '9'],
                  'correcta': 'C'},
                 {'enunciado': 'Al simplificar '
                               '(a<super>3</super>)<super>2</super> / '
                               'a<super>4</super>, con a ≠ 0, se obtiene:',
                  'alternativas': ['a',
                                   'a<super>2</super>',
                                   'a<super>3</super>',
                                   'a<super>4</super>',
                                   'a<super>6</super>'],
                  'correcta': 'B'},
                 {'enunciado': 'Si 2<super>x</super> · 2<super>3</super> = '
                               '2<super>10</super>, el valor de «x» es:',
                  'alternativas': ['5', '6', '7', '8', '13'],
                  'correcta': 'C'},
                 {'enunciado': 'Al resolver √(x+7) = 4, el valor de «x» es:',
                  'alternativas': ['7', '8', '9', '16', '23'],
                  'correcta': 'C'},
                 {'enunciado': 'El valor de √9 + √4 es:',
                  'alternativas': ['3', '4', '5', '6', '13'],
                  'correcta': 'C'},
                 {'enunciado': 'Si x,y ∈ R, x,y ≠ 0, el valor de k = '
                               'x<super>0</super> + y<super>0</super> es:',
                  'alternativas': ['0', '1', '2', 'x+y', 'xy'],
                  'correcta': 'C'},
                 {'enunciado': 'Si 2<super>3x</super> = 64, el valor de «x» '
                               'es:',
                  'alternativas': ['1', '2', '3', '4', '6'],
                  'correcta': 'B'},
                 {'enunciado': 'Al simplificar √3 · √27, se obtiene:',
                  'alternativas': ['3', '6', '9', '27', '81'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a<super>n</super> = 8 y a<super>m</super> '
                               '= 2, el valor de a<super>n-m</super> es:',
                  'alternativas': ['2', '4', '6', '10', '16'],
                  'correcta': 'B'},
                 {'enunciado': 'El valor de «x» en la ecuación '
                               '4<super>x</super> = 8<super>2</super> es:',
                  'alternativas': ['2', '3', '4', '6', '8'],
                  'correcta': 'B'},
                 {'enunciado': 'Al simplificar '
                               '(x<super>2</super>)<super>3</super> · x / '
                               'x<super>6</super>, con x ≠ 0, se obtiene:',
                  'alternativas': ['1',
                                   'x',
                                   'x<super>2</super>',
                                   'x<super>3</super>',
                                   'x<super>6</super>'],
                  'correcta': 'B'},
                 {'enunciado': 'Si 7<super>2x+1</super> = 7<super>9</super>, '
                               'el valor de «x» es:',
                  'alternativas': ['2', '3', '4', '5', '9'],
                  'correcta': 'C'},
                 {'enunciado': 'El valor de <super>4</super>√16 es:',
                  'alternativas': ['2', '4', '8', '16', '1'],
                  'correcta': 'A'},
                 {'enunciado': 'Al simplificar 3<super>5</super> ÷ '
                               '3<super>2</super>, se obtiene:',
                  'alternativas': ['3', '9', '27', '81', '243'],
                  'correcta': 'C'},
                 {'enunciado': 'Si x<super>3</super> = 27, el valor de '
                               'x<super>2</super> es:',
                  'alternativas': ['3', '6', '9', '18', '81'],
                  'correcta': 'C'},
                 {'enunciado': 'El valor de (0,5)<super>-2</super> es:',
                  'alternativas': ['0,25', '0,5', '1', '2', '4'],
                  'correcta': 'E'},
                 {'enunciado': 'Al simplificar √50 / √2, se obtiene:',
                  'alternativas': ['2', '5', '10', '25', '100'],
                  'correcta': 'B'},
                 {'enunciado': 'Si x<super>1/3</super> = 2, el valor de «x» '
                               'es:',
                  'alternativas': ['2/3', '2', '4', '6', '8'],
                  'correcta': 'E'},
                 {'enunciado': 'El valor de 5<super>0</super> + '
                               '5<super>1</super> es:',
                  'alternativas': ['1', '5', '6', '10', '25'],
                  'correcta': 'C'},
                 {'enunciado': 'Si 3<super>x</super> = 1/9, el valor de «x» '
                               'es:',
                  'alternativas': ['-3', '-2', '1/2', '2', '3'],
                  'correcta': 'B'},
                 {'enunciado': 'Al simplificar '
                               '(2<super>-1</super>)<super>-3</super>, se '
                               'obtiene:',
                  'alternativas': ['1/8', '1/2', '2', '4', '8'],
                  'correcta': 'E'},
                 {'enunciado': 'El valor de √(1/4) es:',
                  'alternativas': ['1/16', '1/4', '1/2', '2', '4'],
                  'correcta': 'C'},
                 {'enunciado': 'Si x<super>2</super> = 49, el valor positivo '
                               'de «x» es:',
                  'alternativas': ['3', '5', '7', '9', '49'],
                  'correcta': 'C'},
                 {'enunciado': 'Al simplificar 10<super>3</super> · '
                               '10<super>-1</super>, se obtiene:',
                  'alternativas': ['10', '100', '1000', '0,1', '1'],
                  'correcta': 'B'},
                 {'enunciado': 'Si <super>3</super>√x = 4, el valor de «x» '
                               'es:',
                  'alternativas': ['12', '16', '48', '64', '4/3'],
                  'correcta': 'D'},
                 {'enunciado': 'Al simplificar '
                               '(a<super>2</super>·b<super>3</super>)<super>2</super>, '
                               'se obtiene:',
                  'alternativas': ['a<super>2</super>b<super>3</super>',
                                   'a<super>4</super>b<super>5</super>',
                                   'a<super>4</super>b<super>6</super>',
                                   'a<super>4</super>b<super>3</super>',
                                   'a<super>2</super>b<super>6</super>'],
                  'correcta': 'C'},
                 {'enunciado': 'Si 6<super>x</super> = 1, el valor de «x» '
                               'es:',
                  'alternativas': ['-1', '0', '1', '6', '1/6'],
                  'correcta': 'B'},
                 {'enunciado': 'El valor de √64 - √16 es:',
                  'alternativas': ['2', '3', '4', '6', '8'],
                  'correcta': 'C'},
                 {'enunciado': 'Al simplificar 2<super>4</super> · '
                               '2<super>-2</super>, se obtiene:',
                  'alternativas': ['2', '4', '6', '8', '16'],
                  'correcta': 'B'},
                 {'enunciado': 'Si 9<super>x</super> = 3, el valor de «x» '
                               'es:',
                  'alternativas': ['1/3', '1/2', '2', '3', '9'],
                  'correcta': 'B'},
                 {'enunciado': 'Al simplificar √5 · √5, se obtiene:',
                  'alternativas': ['5', '10', '25', '√5', '√10'],
                  'correcta': 'A'},
                 {'enunciado': 'Si m<super>3</super> = 64, el valor de «m» '
                               'es:',
                  'alternativas': ['2', '4', '6', '8', '16'],
                  'correcta': 'B'},
                 {'enunciado': 'El valor de 2<super>-3</super> es:',
                  'alternativas': ['-8', '-6', '1/8', '1/6', '8'],
                  'correcta': 'C'},
                 {'enunciado': 'Al simplificar '
                               '(3<super>2</super>)<super>0</super>, se '
                               'obtiene:',
                  'alternativas': ['0', '1', '3', '6', '9'],
                  'correcta': 'B'},
                 {'enunciado': 'Si a<super>5</super> ÷ a<super>2</super> = '
                               'a<super>k</super>, con a ≠ 0, el valor de '
                               '«k» es:',
                  'alternativas': ['1', '2', '3', '7', '10'],
                  'correcta': 'C'},
                 {'enunciado': 'El valor de √0,09 es:',
                  'alternativas': ['0,03', '0,09', '0,3', '0,9', '3'],
                  'correcta': 'C'},
                 {'enunciado': 'Al simplificar 4<super>1/2</super> · '
                               '9<super>1/2</super>, se obtiene:',
                  'alternativas': ['3', '4', '5', '6', '9'],
                  'correcta': 'D'},
                 {'enunciado': 'Si x<super>-2</super> = 1/25, el valor '
                               'positivo de «x» es:',
                  'alternativas': ['1/5', '5', '10', '25', '125'],
                  'correcta': 'B'}],
  'qr_reto': [{'pregunta': '¿Cuánto es a⁰ para a≠0?', 'respuesta': '1'},
              {'pregunta': '¿Cuánto es 2³ · 2²?', 'respuesta': '32 (2⁵)'},
              {'pregunta': '¿Cuánto es √25?', 'respuesta': '5'}],
  'qr_dato': 'El símbolo del exponente como lo usamos hoy fue introducido '
             'por René Descartes en 1637. Antes, los matemáticos escribían '
             '«x·x·x» en vez de «x³».'},
 {'num': 2,
  'titulo': 'Polinomios',
  'secciones': [{'titulo': '2.1 POLINOMIO: DEFINICIÓN Y ELEMENTOS',
                 'items': ['Un <b>polinomio</b> es una expresión algebraica '
                           'racional entera, donde los exponentes de las '
                           'variables son números enteros positivos mayores '
                           'o iguales a cero.',
                           'El polinomio en la variable «x» se define: P(x) '
                           '= a<super>n</super>x<super>n</super> + '
                           'a<super>n-1</super>x<super>n-1</super> + ... + '
                           'a<super>1</super>x + a<super>0</super>, con '
                           'a<super>n</super> ≠ 0.',
                           '«x» es la <b>variable</b>; «n» es el '
                           '<b>grado</b> del polinomio; «a<super>n</super>» '
                           'es el <b>coeficiente principal</b>; '
                           '«a<super>0</super>» es el <b>término '
                           'independiente</b>.',
                           'El número de <b>términos</b> de P(x) es n + 1.']},
                {'titulo': '2.2 VALOR NUMÉRICO DE UN POLINOMIO',
                 'items': ['El <b>valor numérico</b> es el valor real que '
                           'adquiere un polinomio cuando se asignan valores '
                           'reales a sus variables.',
                           'Si P(x) es un polinomio de una variable: la '
                           '<b>suma de coeficientes</b> es P(1); el '
                           '<b>término independiente</b> es P(0).',
                           'Si P(x,y) es un polinomio de dos variables: la '
                           '<b>suma de coeficientes</b> es P(1,1); el '
                           '<b>término independiente</b> es P(0,0).']},
                {'titulo': '2.3 GRADO RELATIVO (G.R.)',
                 'items': ['El <b>grado relativo</b> de un monomio, respecto '
                           'a una variable, es el exponente de dicha '
                           'variable.',
                           'Ejemplo: en '
                           '7x<super>8</super>y<super>10</super>z<super>5</super>, '
                           'GR(x)=8, GR(y)=10, GR(z)=5.',
                           'El <b>grado relativo</b> de un polinomio, '
                           'respecto a una variable, es el mayor exponente '
                           'de esa variable en cualquiera de sus términos.']},
                {'titulo': '2.4 GRADO ABSOLUTO (G.A.)',
                 'items': ['El <b>grado absoluto</b> de un monomio es la '
                           'suma de los exponentes de todas sus variables.',
                           'Ejemplo: en '
                           '2x<super>7</super>y<super>13</super>z<super>9</super>, '
                           'GA = 7+13+9 = 29.',
                           'El <b>grado absoluto</b> de un polinomio es el '
                           'mayor grado absoluto entre todos sus términos.']},
                {'titulo': '2.5 GRADOS EN OPERACIONES DE POLINOMIOS',
                 'items': ['Si P(x) y Q(x) tienen grados m y n (m &gt; n), '
                           'el grado de P(x)±Q(x) es <b>m</b>.',
                           'El grado del producto P(x)·Q(x) es <b>m+n</b>.',
                           'El grado del cociente P(x)÷Q(x) es <b>m-n</b>.',
                           'El grado de [P(x)]<super>k</super> es '
                           '<b>m·k</b>.',
                           'El grado de <super>k</super>√[P(x)] es '
                           '<b>m/k</b>, siempre que sea un polinomio.']},
                {'titulo': '2.6 POLINOMIOS ESPECIALES (I): HOMOGÉNEO, '
                           'ORDENADO, COMPLETO',
                 'items': ['Un polinomio <b>homogéneo</b> es aquel en el que '
                           'todos sus términos tienen el mismo grado '
                           'absoluto.',
                           'Un polinomio <b>ordenado</b>, respecto a una '
                           'variable, tiene los exponentes de dicha variable '
                           'aumentando (ascendente) o disminuyendo '
                           '(descendente).',
                           'Un polinomio <b>completo</b>, respecto a una '
                           'variable, contiene todos los exponentes '
                           'consecutivos desde el mayor hasta el término '
                           'independiente (exponente cero).',
                           'En un polinomio completo (de una variable): '
                           'número de términos = Grado Absoluto + 1.']},
                {'titulo': '2.7 POLINOMIOS ESPECIALES (II): IDÉNTICOS, NULO, '
                           'MÓNICO, CONSTANTE',
                 'items': ['Dos polinomios son <b>idénticos</b> cuando los '
                           'coeficientes de sus términos semejantes son '
                           'iguales.',
                           'Un polinomio <b>idénticamente nulo</b> (o '
                           'polinomio cero) tiene todos sus coeficientes '
                           'iguales a cero; su grado no está definido, y se '
                           'anula para cualquier valor numérico.',
                           'Un polinomio <b>mónico</b> es aquel en una '
                           'variable cuyo coeficiente principal es 1.',
                           'Un polinomio <b>constante</b> es igual a un '
                           'número real distinto de cero, y es de grado '
                           'cero; su valor numérico es siempre el mismo, sin '
                           'importar el valor de la variable.']}],
  'ejercicios': [{'enunciado': 'Si P(x) = x + 3, el valor de P(2) es:',
                  'alternativas': ['3', '4', '5', '6', '7'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = 2x<super>2</super> - x + 1, la '
                               'suma de coeficientes de P(x) es:',
                  'alternativas': ['0', '1', '2', '3', '4'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = 3x<super>3</super> - 2x + 7, el '
                               'término independiente de P(x) es:',
                  'alternativas': ['3', '-2', '5', '7', '9'],
                  'correcta': 'D'},
                 {'enunciado': 'En P(x,y) = '
                               '5x<super>2</super>y<super>3</super> - 2xy + '
                               '8, el grado relativo a «x» es:',
                  'alternativas': ['1', '2', '3', '5', '8'],
                  'correcta': 'B'},
                 {'enunciado': 'En P(x,y) = '
                               '5x<super>2</super>y<super>3</super> - 2xy + '
                               '8, el grado relativo a «y» es:',
                  'alternativas': ['1', '2', '3', '5', '8'],
                  'correcta': 'C'},
                 {'enunciado': 'En el monomio '
                               '4x<super>5</super>y<super>7</super>, el '
                               'grado absoluto es:',
                  'alternativas': ['5', '7', '10', '12', '35'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) = 3x<super>4</super> - '
                               '2x<super>7</super> + 5x, el grado absoluto '
                               'de P(x) es:',
                  'alternativas': ['1', '4', '5', '7', '11'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) es de grado 4 y Q(x) es de grado 6, '
                               'el grado de P(x)·Q(x) es:',
                  'alternativas': ['2', '4', '6', '10', '24'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) es de grado 8 y Q(x) es de grado 3, '
                               'el grado de P(x)÷Q(x) es:',
                  'alternativas': ['3', '5', '8', '11', '24'],
                  'correcta': 'B'},
                 {'enunciado': 'Si P(x) es de grado 3, el grado de '
                               '[P(x)]<super>4</super> es:',
                  'alternativas': ['1', '4', '7', '12', '81'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) = x<super>3</super> - '
                               '2x<super>2</super> + x - 5, la suma de '
                               'coeficientes de P(x) es:',
                  'alternativas': ['-9', '-7', '-5', '-3', '5'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x,y) = 3x<super>2</super>y + '
                               '2xy<super>2</super> - 5, el valor de P(1,1) '
                               'es:',
                  'alternativas': ['-5', '-2', '0', '2', '5'],
                  'correcta': 'C'},
                 {'enunciado': 'Un polinomio completo de grado 5 (en una '
                               'variable) tiene un número de términos igual '
                               'a:',
                  'alternativas': ['4', '5', '6', '10', '15'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = ax<super>3</super> + 5 es mónico, '
                               'el valor de «a» es:',
                  'alternativas': ['0', '1', '3', '5', '-1'],
                  'correcta': 'B'},
                 {'enunciado': 'Si P(x) = k es un polinomio constante y P(7) '
                               '= 9, el valor de «k» es:',
                  'alternativas': ['0', '7', '9', '16', '63'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = 2x<super>2</super> - 3x + 1, el '
                               'valor de P(-1) es:',
                  'alternativas': ['0', '2', '4', '6', '8'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) es de grado 5 y Q(x) es de grado 5, '
                               'el grado máximo de P(x)+Q(x) es:',
                  'alternativas': ['0', '5', '10', '15', '25'],
                  'correcta': 'B'},
                 {'enunciado': 'Si P(x) es de grado 8, el grado de √[P(x)] '
                               'es:',
                  'alternativas': ['2', '4', '8', '16', '64'],
                  'correcta': 'B'},
                 {'enunciado': 'En el monomio P(x,y,z) = '
                               '2x<super>3</super>y<super>4</super>z<super>2</super>, '
                               'el grado absoluto es:',
                  'alternativas': ['2', '3', '4', '9', '24'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) = 7 es un polinomio constante, el '
                               'valor de P(100) es:',
                  'alternativas': ['0', '1', '7', '100', '700'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = 5x<super>4</super> - '
                               '3x<super>2</super> + 2x - 8, el número de '
                               'términos de P(x) es:',
                  'alternativas': ['2', '3', '4', '5', '8'],
                  'correcta': 'C'},
                 {'enunciado': 'Un polinomio completo y ordenado en forma '
                               'descendente de grado 2 tiene un número de '
                               'términos igual a:',
                  'alternativas': ['1', '2', '3', '4', '5'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = 2x<super>3</super> - '
                               '5x<super>2</super> + x - 3, el valor de P(1) '
                               '+ P(0) es:',
                  'alternativas': ['-11', '-8', '-5', '-3', '0'],
                  'correcta': 'B'},
                 {'enunciado': 'En el monomio '
                               '8x<super>6</super>y<super>9</super>, el '
                               'valor de GA - GR(x) es:',
                  'alternativas': ['3', '6', '9', '12', '15'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) es de grado 7 y Q(x) es de grado 2, '
                               'el grado de P(x)·[Q(x)]<super>2</super> es:',
                  'alternativas': ['9', '11', '13', '14', '28'],
                  'correcta': 'B'},
                 {'enunciado': 'Si P(x) = (a-3)x<super>2</super> + 5x + 1 no '
                               'es un polinomio cuadrático, el valor de «a» '
                               'es:',
                  'alternativas': ['-3', '0', '1', '3', '5'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x,y) = '
                               '4x<super>3</super>y<super>2</super> - '
                               '7x<super>2</super>y<super>3</super> + '
                               'xy<super>4</super> es homogéneo, su grado de '
                               'homogeneidad es:',
                  'alternativas': ['3', '4', '5', '6', '7'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = 3x<super>2</super> - 5x + 2, el '
                               'valor de P(2) es:',
                  'alternativas': ['0', '2', '4', '6', '8'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = mx<super>3</super> + 5 es mónico, '
                               'el valor de «m» es:',
                  'alternativas': ['-1', '0', '1', '3', '5'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = 2ax<super>2</super> + 3bx + c es '
                               'idénticamente nulo, el valor de a+b+c es:',
                  'alternativas': ['-1', '0', '1', '3', '6'],
                  'correcta': 'B'},
                 {'enunciado': 'Si P(x) = 2x<super>5</super> - '
                               '3x<super>3</super> + x - 7, el coeficiente '
                               'principal de P(x) es:',
                  'alternativas': ['-7', '-3', '1', '2', '5'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) = (k-5)x<super>4</super> + 3x - 2 '
                               'debe ser de grado 4, el valor de «k» debe '
                               'ser distinto de:',
                  'alternativas': ['0', '3', '4', '5', '-2'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) = x<super>3</super> + '
                               '2x<super>2</super> - x + 5, el valor de P(2) '
                               'es:',
                  'alternativas': ['15', '17', '19', '21', '23'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = 3x - 1 y Q(x) = x + 2, el grado de '
                               'P(x) + Q(x) es:',
                  'alternativas': ['0', '1', '2', '3', '4'],
                  'correcta': 'B'},
                 {'enunciado': 'Si P(x) = ax<super>2</super> + bx + c es '
                               'idéntico a Q(x) = 5x<super>2</super> - 3x + '
                               '7, el valor de a+b+c es:',
                  'alternativas': ['1', '5', '7', '9', '15'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) = x<super>6</super> - '
                               '4x<super>3</super> + 2x - 9, la suma de sus '
                               'exponentes distintos es:',
                  'alternativas': ['6', '7', '9', '10', '12'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) = 2x<super>2</super>(x-1) + 3, el '
                               'valor de P(0) es:',
                  'alternativas': ['-2', '0', '1', '3', '5'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) = (x+1)<super>2</super>, la suma de '
                               'coeficientes de P(x) es:',
                  'alternativas': ['1', '2', '3', '4', '5'],
                  'correcta': 'D'},
                 {'enunciado': 'En el monomio '
                               '7x<super>4</super>y<super>6</super>, el '
                               'valor de GA - GR(y) es:',
                  'alternativas': ['2', '4', '6', '8', '10'],
                  'correcta': 'B'},
                 {'enunciado': 'Si P(x) = x<super>4</super> - '
                               '2x<super>2</super> + 5, el término '
                               'independiente de P(x) es:',
                  'alternativas': ['-2', '0', '2', '4', '5'],
                  'correcta': 'E'},
                 {'enunciado': 'Si P(x) = 4x<super>6</super> - '
                               '3x<super>4</super> + x<super>2</super> - 1, '
                               'el número de términos de P(x) es:',
                  'alternativas': ['2', '3', '4', '5', '6'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = 2x<super>3</super> - 5, el valor '
                               'de P(1) - P(0) es:',
                  'alternativas': ['-3', '-2', '0', '2', '3'],
                  'correcta': 'D'},
                 {'enunciado': 'En el monomio '
                               '6x<super>2</super>y<super>3</super>z, el '
                               'grado absoluto es:',
                  'alternativas': ['3', '4', '5', '6', '7'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) es de grado 4, el grado de '
                               '√([P(x)]<super>2</super>) es:',
                  'alternativas': ['1', '2', '4', '8', '16'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = 9 y Q(x) = x<super>2</super> + 1, '
                               'el valor de P(5) + Q(2) es:',
                  'alternativas': ['9', '10', '13', '14', '15'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) = ax<super>2</super> + bx + c y P(0) '
                               '= 5, el valor de «c» es:',
                  'alternativas': ['0', '1', '3', '5', 'a'],
                  'correcta': 'D'},
                 {'enunciado': 'Si P(x) = 2x - 7, el valor de «x» para que '
                               'P(x) = 0 es:',
                  'alternativas': ['2', '3', '3,5', '5', '7'],
                  'correcta': 'C'},
                 {'enunciado': 'Si P(x) = (k-5)x<super>4</super> + 3x - 2 '
                               'debe ser de grado 4, «k» no puede ser igual '
                               'a:',
                  'alternativas': ['-2', '0', '2', '3', '5'],
                  'correcta': 'E'}],
  'qr_reto': [{'pregunta': '¿Cuál es el término independiente de '
                           'P(x)=3x²-5x+8?',
               'respuesta': '8'},
              {'pregunta': '¿Cómo se calcula la suma de coeficientes de '
                           'P(x)?',
               'respuesta': 'Evaluando P(1)'},
              {'pregunta': '¿Cuál es el grado absoluto del monomio 5x³y⁴?',
               'respuesta': '7'}],
  'qr_dato': 'La palabra «polinomio» viene del griego «poly» (muchos) y del '
             'latín «nomen» (nombre/término) — literalmente, «muchos '
             'términos». René Descartes fue quien popularizó la notación con '
             'exponentes que usamos hoy.'},
 {'num': 3,
  'titulo': 'Productos Notables',
  'secciones': [{'titulo': '3.1.A BINOMIO AL CUADRADO Y DIFERENCIA DE '
                           'CUADRADOS',
                 'items': ['Los <b>productos notables</b> son casos '
                           'especiales de la multiplicación de polinomios, '
                           'que dan el resultado en forma directa sin '
                           'efectuar la multiplicación.',
                           '<b>Binomio al cuadrado</b> (trinomio cuadrado '
                           'perfecto): (a+b)<super>2</super> = '
                           'a<super>2</super> + 2ab + b<super>2</super>.',
                           '(a-b)<super>2</super> = a<super>2</super> - 2ab '
                           '+ b<super>2</super>.',
                           '<b>Diferencia de cuadrados</b>: (a+b)(a-b) = '
                           'a<super>2</super> - b<super>2</super>.']},
                {'titulo': '3.1.B PRODUCTO DE BINOMIOS CON TÉRMINO COMÚN',
                 'items': ['(x+a)(x+b) = x<super>2</super> + (a+b)x + ab.',
                           '(x-a)(x-b) = x<super>2</super> - (a+b)x + ab.',
                           '(x+a)(x-b) = x<super>2</super> + (a-b)x - ab.']},
                {'titulo': '3.1.C IDENTIDAD DE LEGENDRE',
                 'items': ['(a+b)<super>2</super> + (a-b)<super>2</super> = '
                           '2(a<super>2</super>+b<super>2</super>).',
                           '(a+b)<super>2</super> - (a-b)<super>2</super> = '
                           '4ab.',
                           '(a+b)<super>4</super> - (a-b)<super>4</super> = '
                           '8ab(a<super>2</super>+b<super>2</super>).']},
                {'titulo': '3.1.D IDENTIDAD DE LAGRANGE',
                 'items': ['(a<super>2</super>+b<super>2</super>)(x<super>2</super>+y<super>2</super>) '
                           '= (ax+by)<super>2</super> + '
                           '(ay-bx)<super>2</super>.',
                           '(a<super>2</super>+b<super>2</super>)(c<super>2</super>+d<super>2</super>) '
                           '= (ac+bd)<super>2</super> + '
                           '(ad-bc)<super>2</super>.']},
                {'titulo': '3.2.A SUMA Y DIFERENCIA DE CUBOS',
                 'items': ['<b>Suma de cubos</b>: '
                           '(a+b)(a<super>2</super>-ab+b<super>2</super>) = '
                           'a<super>3</super> + b<super>3</super>.',
                           '<b>Diferencia de cubos</b>: '
                           '(a-b)(a<super>2</super>+ab+b<super>2</super>) = '
                           'a<super>3</super> - b<super>3</super>.']},
                {'titulo': '3.2.B BINOMIO AL CUBO',
                 'items': ['(a+b)<super>3</super> = a<super>3</super> + '
                           '3a<super>2</super>b + 3ab<super>2</super> + '
                           'b<super>3</super>.',
                           '(a-b)<super>3</super> = a<super>3</super> - '
                           '3a<super>2</super>b + 3ab<super>2</super> - '
                           'b<super>3</super>.',
                           'Forma reducida: (a+b)<super>3</super> = '
                           'a<super>3</super> + b<super>3</super> + '
                           '3ab(a+b).',
                           'Forma reducida: (a-b)<super>3</super> = '
                           'a<super>3</super> - b<super>3</super> - '
                           '3ab(a-b).']},
                {'titulo': '3.2.C IDENTIDADES DE ARGAND',
                 'items': ['(a<super>2</super>+a+1)(a<super>2</super>-a+1) = '
                           'a<super>4</super>+a<super>2</super>+1.',
                           '(a<super>2</super>+ab+b<super>2</super>)(a<super>2</super>-ab+b<super>2</super>) '
                           '= '
                           'a<super>4</super>+a<super>2</super>b<super>2</super>+b<super>4</super>.']},
                {'titulo': '3.2.D TRINOMIO AL CUADRADO',
                 'items': ['(a+b+c)<super>2</super> = '
                           'a<super>2</super>+b<super>2</super>+c<super>2</super> '
                           '+ 2ab+2ac+2bc.',
                           '(a-b-c)<super>2</super> = '
                           'a<super>2</super>+b<super>2</super>+c<super>2</super> '
                           '- 2ab-2ac+2bc.']},
                {'titulo': '3.2.E TRINOMIO AL CUBO',
                 'items': ['(a+b+c)<super>3</super> = '
                           'a<super>3</super>+b<super>3</super>+c<super>3</super> '
                           '+ 3(a+b+c)(ab+ac+bc) - 3abc.',
                           'Forma equivalente: (a+b+c)<super>3</super> = '
                           'a<super>3</super>+b<super>3</super>+c<super>3</super> '
                           '+ 3(a+b)(a+c)(b+c).']}],
  'ejercicios': [{'enunciado': 'El valor de (3+2)<super>2</super> es:',
                  'alternativas': ['20', '23', '25', '27', '30'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a=5 y b=1, el valor de '
                               'a<super>2</super>+2ab+b<super>2</super> es:',
                  'alternativas': ['25', '30', '36', '40', '46'],
                  'correcta': 'C'},
                 {'enunciado': 'El valor de (7-3)<super>2</super> es:',
                  'alternativas': ['9', '12', '16', '20', '24'],
                  'correcta': 'C'},
                 {'enunciado': 'El valor de (6+4)(6-4) es:',
                  'alternativas': ['10', '16', '20', '24', '36'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a+b=8 y a-b=2, el valor de '
                               'a<super>2</super>-b<super>2</super> es:',
                  'alternativas': ['6', '10', '16', '20', '32'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a+b=5 y ab=6, el valor de '
                               'a<super>2</super>+b<super>2</super> es:',
                  'alternativas': ['6', '8', '11', '13', '19'],
                  'correcta': 'D'},
                 {'enunciado': 'Si a-b=3 y ab=4, el valor de '
                               'a<super>2</super>+b<super>2</super> es:',
                  'alternativas': ['9', '13', '17', '21', '25'],
                  'correcta': 'C'},
                 {'enunciado': 'El valor de (1+2)(1+3) es:',
                  'alternativas': ['6', '8', '10', '12', '15'],
                  'correcta': 'D'},
                 {'enunciado': 'Si a+b=6 y a-b=2, el valor de '
                               '(a+b)<super>2</super>+(a-b)<super>2</super> '
                               'es:',
                  'alternativas': ['20', '30', '40', '50', '60'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a=5 y b=3, el valor de '
                               '(a+b)<super>2</super>-(a-b)<super>2</super> '
                               'es:',
                  'alternativas': ['30', '45', '60', '75', '90'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a=2 y b=1, el valor de '
                               'a<super>3</super>+b<super>3</super> es:',
                  'alternativas': ['6', '7', '8', '9', '10'],
                  'correcta': 'D'},
                 {'enunciado': 'Si a=3 y b=1, el valor de '
                               'a<super>3</super>-b<super>3</super> es:',
                  'alternativas': ['20', '23', '26', '29', '32'],
                  'correcta': 'C'},
                 {'enunciado': 'El valor de (1+1)<super>3</super> es:',
                  'alternativas': ['2', '4', '6', '8', '10'],
                  'correcta': 'D'},
                 {'enunciado': 'El valor de (2+1)<super>3</super> es:',
                  'alternativas': ['9', '18', '24', '27', '30'],
                  'correcta': 'D'},
                 {'enunciado': 'El valor de (4-2)<super>3</super> es:',
                  'alternativas': ['2', '4', '6', '8', '10'],
                  'correcta': 'D'},
                 {'enunciado': 'Si a=2, el valor de '
                               'a<super>4</super>+a<super>2</super>+1 '
                               '(Identidad de Argand) es:',
                  'alternativas': ['15', '18', '21', '24', '27'],
                  'correcta': 'C'},
                 {'enunciado': 'El valor de (1+2+3)<super>2</super> es:',
                  'alternativas': ['24', '30', '36', '42', '48'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a=b=c=1, el valor de '
                               'a<super>2</super>+b<super>2</super>+c<super>2</super>+2ab+2ac+2bc '
                               'es:',
                  'alternativas': ['3', '6', '9', '12', '15'],
                  'correcta': 'C'},
                 {'enunciado': 'Al expandir (x+3)(x+5), el término '
                               'independiente es:',
                  'alternativas': ['3', '5', '8', '15', '20'],
                  'correcta': 'D'},
                 {'enunciado': 'Al expandir (x-4)(x+2), el coeficiente de '
                               '«x» es:',
                  'alternativas': ['-8', '-2', '2', '4', '6'],
                  'correcta': 'B'},
                 {'enunciado': 'Al expandir '
                               '(a-b)(a<super>2</super>+ab+b<super>2</super>), '
                               'se obtiene:',
                  'alternativas': ['a²-b²',
                                   'a³+b³',
                                   'a³-b³',
                                   '(a-b)²',
                                   '(a-b)³'],
                  'correcta': 'C'},
                 {'enunciado': 'Al expandir '
                               '(a+b)(a<super>2</super>-ab+b<super>2</super>), '
                               'se obtiene:',
                  'alternativas': ['a²+b²',
                                   'a³-b³',
                                   'a³+b³',
                                   '(a+b)²',
                                   '(a+b)³'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a+b=10 y ab=21, el valor de '
                               'a<super>2</super>+b<super>2</super> es:',
                  'alternativas': ['42', '50', '58', '64', '79'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a-b=4 y '
                               'a<super>2</super>+b<super>2</super>=20, el '
                               'valor de 2ab es:',
                  'alternativas': ['2', '4', '6', '8', '10'],
                  'correcta': 'B'},
                 {'enunciado': 'El valor de (3+5)<super>2</super> es:',
                  'alternativas': ['49', '56', '64', '72', '81'],
                  'correcta': 'C'},
                 {'enunciado': 'Si x=2, el valor de (2x+1)<super>2</super> '
                               'es:',
                  'alternativas': ['16', '20', '25', '30', '36'],
                  'correcta': 'C'},
                 {'enunciado': 'El valor de 7<super>2</super> - '
                               '3<super>2</super> es:',
                  'alternativas': ['16', '28', '34', '40', '46'],
                  'correcta': 'D'},
                 {'enunciado': 'Si x=10, el valor de (x+7)(x-7) es:',
                  'alternativas': ['37', '44', '51', '58', '65'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a=3 y b=2, el valor de '
                               'a<super>3</super>+b<super>3</super> es:',
                  'alternativas': ['25', '30', '35', '40', '45'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a=1, el valor de (a+2)<super>3</super> '
                               'es:',
                  'alternativas': ['9', '18', '24', '27', '30'],
                  'correcta': 'D'},
                 {'enunciado': 'Si m=3 y n=2, el valor de '
                               '(m+n)<super>2</super>+(m-n)<super>2</super> '
                               'es:',
                  'alternativas': ['16', '20', '23', '26', '30'],
                  'correcta': 'D'},
                 {'enunciado': 'Si x=8, el valor de (x-3)(x-3) es:',
                  'alternativas': ['15', '20', '25', '30', '35'],
                  'correcta': 'C'},
                 {'enunciado': 'Si x=11, el valor de (x+9)(x-9) es:',
                  'alternativas': ['22', '31', '40', '49', '58'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a=6, el valor de (a+4)<super>2</super> '
                               'es:',
                  'alternativas': ['80', '90', '100', '110', '120'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a=6, el valor de (a-4)<super>2</super> '
                               'es:',
                  'alternativas': ['0', '2', '4', '6', '8'],
                  'correcta': 'C'},
                 {'enunciado': 'El valor de (5+2)(5-2) es:',
                  'alternativas': ['15', '18', '21', '24', '27'],
                  'correcta': 'C'},
                 {'enunciado': 'Si x=2, el valor de (x+1)(x+4) es:',
                  'alternativas': ['10', '14', '18', '22', '26'],
                  'correcta': 'C'},
                 {'enunciado': 'Si x=10, el valor de (x-2)(x-6) es:',
                  'alternativas': ['16', '24', '32', '40', '48'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a=4 y b=2, el valor de '
                               'a<super>3</super>-b<super>3</super> es:',
                  'alternativas': ['40', '48', '56', '64', '72'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a=3, el valor de (a-1)<super>3</super> '
                               'es:',
                  'alternativas': ['4', '6', '8', '10', '12'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a+b=7 y a-b=3, el valor de '
                               'a<super>2</super>-b<super>2</super> es:',
                  'alternativas': ['10', '14', '17', '21', '24'],
                  'correcta': 'D'},
                 {'enunciado': 'Si a=6, el valor de (a+6)<super>2</super> es '
                               '(con «a» reemplazando la base):',
                  'alternativas': ['100', '121', '144', '169', '196'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a=1 y b=1, el valor de '
                               'a<super>4</super>+a<super>2</super>b<super>2</super>+b<super>4</super> '
                               '(Identidad de Argand) es:',
                  'alternativas': ['1', '2', '3', '4', '5'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a+b+c=0, entonces '
                               'a<super>3</super>+b<super>3</super>+c<super>3</super>=3abc. '
                               'Con a=1, b=2, c=-3, el valor es:',
                  'alternativas': ['-18', '-12', '0', '12', '18'],
                  'correcta': 'A'},
                 {'enunciado': 'Si a=1 y b=1, el valor de '
                               '(2a+3b)<super>2</super> es:',
                  'alternativas': ['16', '20', '25', '30', '36'],
                  'correcta': 'C'},
                 {'enunciado': 'Si a=2, b=0, c=1, el valor de '
                               '(a+b+c)<super>2</super> es:',
                  'alternativas': ['4', '6', '9', '12', '16'],
                  'correcta': 'C'},
                 {'enunciado': 'Si (a+b)<super>2</super>=49 y ab=10, el '
                               'valor de a<super>2</super>+b<super>2</super> '
                               'es:',
                  'alternativas': ['19', '24', '29', '34', '39'],
                  'correcta': 'C'},
                 {'enunciado': 'Si x=8, el valor de (x-5)<super>2</super> '
                               'es:',
                  'alternativas': ['4', '6', '9', '12', '16'],
                  'correcta': 'C'}],
  'qr_reto': [{'pregunta': '¿Cuánto es (a+b)²?',
               'respuesta': 'a² + 2ab + b²'},
              {'pregunta': '¿Cómo se llama (a+b)(a-b)=a²-b²?',
               'respuesta': 'Diferencia de cuadrados'},
              {'pregunta': '¿Cuánto es a³+b³ factorizado?',
               'respuesta': '(a+b)(a²-ab+b²)'}],
  'qr_dato': 'Los productos notables se llaman así porque son "notables" — '
             'es decir, dignos de notarse — por lo frecuente que aparecen en '
             'matemáticas. La identidad de Legendre lleva el nombre de '
             'Adrien-Marie Legendre, matemático francés del siglo XVIII.'},
 {'num': 4,
  'titulo': 'División de Polinomios, Teorema del Resto y Cocientes Notables',
  'secciones': [{'titulo': '4.1.A DIVISIÓN DE POLINOMIOS: ALGORITMO',
                 'items': ['Dados los polinomios D(x) (<b>dividendo</b>) y '
                           'd(x) (<b>divisor</b>), existen únicos q(x) '
                           '(<b>cociente</b>) y r(x) (<b>residuo</b>) tales '
                           'que: D(x) = d(x)·q(x) + r(x).',
                           'La división es <b>exacta</b> cuando el residuo '
                           'es idénticamente nulo (r(x) ≡ 0), entonces D(x) '
                           '= d(x)·q(x).',
                           'La división es <b>inexacta</b> cuando el residuo '
                           'no es idénticamente nulo (r(x) no es 0).',
                           '<b>Propiedad de grados</b>: G.A.(q) = G.A.(D) - '
                           'G.A.(d); el grado máximo del residuo es G.A.(d) '
                           '- 1.']},
                {'titulo': '4.1.B MÉTODO DE HORNER',
                 'items': ['El <b>método de Horner</b> se utiliza cuando el '
                           'divisor es de <b>segundo grado o mayor</b>.',
                           'Se ordenan y completan el dividendo y el '
                           'divisor; se anotan los coeficientes del '
                           'dividendo arriba y los del divisor a la '
                           'izquierda (con el primer coeficiente con su '
                           'signo, y los demás con signo opuesto).',
                           'Se traza una línea vertical que separa el '
                           'cociente del residuo, contando desde la derecha '
                           'tantos espacios como el grado máximo del '
                           'residuo.',
                           'El cociente se obtiene al final dividiendo cada '
                           'columna (excepto la del residuo) entre el primer '
                           'coeficiente del divisor.']},
                {'titulo': '4.1.C MÉTODO DE RUFFINI',
                 'items': ['El <b>método de Ruffini</b> se utiliza cuando el '
                           'divisor es de <b>primer grado</b>: d(x) = ax + '
                           'b.',
                           'Se iguala el divisor a cero y se despeja «x» (x '
                           '= -b/a), anotando ese valor a la izquierda del '
                           'cuadro.',
                           'Se baja el primer coeficiente del dividendo, se '
                           'multiplica por x = -b/a, y el resultado se suma '
                           'con el siguiente coeficiente; así sucesivamente.',
                           'El resto es la suma de la última columna; el '
                           'cociente se obtiene dividiendo el resto de las '
                           'columnas entre el coeficiente principal del '
                           'divisor.']},
                {'titulo': '4.2 TEOREMA DEL RESTO',
                 'items': ['El <b>Teorema del Resto</b> permite calcular el '
                           'residuo de una división de manera directa, sin '
                           'dividir.',
                           'Dada la división P(x) ÷ (ax+b), el resto viene '
                           'dado por: <b>Resto = P(-b/a)</b>.',
                           'Ejemplo: para hallar el resto de '
                           '(2x<super>4</super>-2x<super>2</super>+9)÷(2x-4), '
                           'se iguala 2x-4=0, x=2; resto = P(2) = '
                           '2(2)<super>4</super>-2(2)<super>2</super>+9 = '
                           '33.']},
                {'titulo': '4.3.A COCIENTES NOTABLES: DEFINICIÓN',
                 'items': ['Un <b>cociente notable</b> es la división '
                           '(x<super>n</super>-y<super>n</super>)/(x±y), '
                           'cuando es una división exacta y su cociente se '
                           'puede obtener por simple inspección, sin '
                           'dividir.',
                           'Ejemplo: '
                           '(x<super>3</super>-y<super>3</super>)/(x-y) = '
                           'x<super>2</super>+xy+y<super>2</super>.']},
                {'titulo': '4.3.B LOS 4 CASOS DE COCIENTES NOTABLES',
                 'items': ['<b>Primer caso</b>: '
                           '(x<super>n</super>-y<super>n</super>)/(x-y) — es '
                           'cociente notable para «n» par o impar; '
                           'desarrollo: '
                           'x<super>n-1</super>+x<super>n-2</super>y+...+xy<super>n-2</super>+y<super>n-1</super> '
                           '(todos los signos positivos).',
                           '<b>Segundo caso</b>: '
                           '(x<super>n</super>+y<super>n</super>)/(x+y) — es '
                           'cociente notable solo para «n» impar; desarrollo '
                           'con signos alternados, empezando en positivo.',
                           '<b>Tercer caso</b>: '
                           '(x<super>n</super>-y<super>n</super>)/(x+y) — es '
                           'cociente notable solo para «n» par; desarrollo '
                           'con signos alternados, empezando en positivo.',
                           '<b>Cuarto caso</b>: '
                           '(x<super>n</super>+y<super>n</super>)/(x-y) — '
                           '<b>nunca</b> es cociente notable.']},
                {'titulo': '4.3.C NÚMERO DE TÉRMINOS Y TÉRMINO GENERAL',
                 'items': ['El número de términos de un cociente notable '
                           '(x<super>n</super>±y<super>n</super>)/(x±y) es '
                           '<b>n</b>.',
                           'El <b>término general</b> T<super>k</super> de '
                           'lugar «k» es: T<super>k</super> = '
                           'x<super>n-k</super>y<super>k-1</super>, con '
                           'signo según el caso.',
                           'Signo del término: en (x-y), todos los términos '
                           'son <b>positivos</b>. En (x+y), el signo es '
                           '<b>negativo</b> si «k» es par, y <b>positivo</b> '
                           'si «k» es impar.']}],
  'ejercicios': [{'enunciado': 'El resto de dividir '
                               'P(x)=x<super>2</super>+3x-1 entre (x-2) es:',
                  'alternativas': ['5', '7', '9', '11', '13'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>3</super>-2x+5 entre (x+1) es:',
                  'alternativas': ['2', '4', '6', '8', '10'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=2x<super>2</super>-x+3 entre (x-1) es:',
                  'alternativas': ['2', '3', '4', '5', '6'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>3</super>+x<super>2</super>-4 '
                               'entre (x-2) es:',
                  'alternativas': ['4', '6', '8', '10', '12'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=3x<super>2</super>+2x-5 entre (x+2) es:',
                  'alternativas': ['-1', '1', '3', '5', '7'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>4</super>-3x<super>2</super>+2 '
                               'entre (x-1) es:',
                  'alternativas': ['-2', '-1', '0', '1', '2'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>2</super>-5x+6 entre (x-3) es:',
                  'alternativas': ['-2', '-1', '0', '1', '2'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=2x<super>3</super>-x+1 entre (2x-2) es:',
                  'alternativas': ['0', '1', '2', '3', '4'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir P(x)=x<super>3</super>-8 '
                               'entre (x-2) es:',
                  'alternativas': ['-2', '0', '2', '4', '6'],
                  'correcta': 'B'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>2</super>+4x+4 entre (x+2) es:',
                  'alternativas': ['-2', '0', '2', '4', '6'],
                  'correcta': 'B'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>3</super>+2x<super>2</super>-x+3 '
                               'entre (x-1) es:',
                  'alternativas': ['3', '4', '5', '6', '7'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>4</super>+x<super>3</super>-x-1 '
                               'entre (x+1) es:',
                  'alternativas': ['-2', '-1', '0', '1', '2'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir P(x)=x<super>2</super>-9 '
                               'entre (x-3) es:',
                  'alternativas': ['-3', '-1', '0', '1', '3'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>3</super>+27 entre (x+3) es:',
                  'alternativas': ['-3', '-1', '0', '1', '3'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=3x<super>3</super>-2x<super>2</super>+x-4 '
                               'entre (x-2) es:',
                  'alternativas': ['8', '10', '12', '14', '16'],
                  'correcta': 'D'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>2</super>+2x+3 entre (x-1) es:',
                  'alternativas': ['2', '4', '6', '8', '10'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>3</super>-x+4 entre (x-2) es:',
                  'alternativas': ['6', '8', '10', '12', '14'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=2x<super>2</super>-3x+1 entre (x-2) es:',
                  'alternativas': ['1', '2', '3', '4', '5'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>3</super>+2x-1 entre (x+2) es:',
                  'alternativas': ['-15', '-13', '-11', '-9', '-7'],
                  'correcta': 'B'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>2</super>-3x+5 entre (x-4) es:',
                  'alternativas': ['5', '7', '9', '11', '13'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>4</super>+x-3 entre (x-1) es:',
                  'alternativas': ['-3', '-2', '-1', '0', '1'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=2x<super>3</super>-5 entre (x-1) es:',
                  'alternativas': ['-5', '-3', '-1', '1', '3'],
                  'correcta': 'B'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>2</super>+x+1 entre (x-2) es:',
                  'alternativas': ['3', '5', '7', '9', '11'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>3</super>-4x+2 entre (x-3) es:',
                  'alternativas': ['11', '13', '15', '17', '19'],
                  'correcta': 'D'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=3x<super>2</super>-2x+1 entre (3x-3) '
                               'es:',
                  'alternativas': ['0', '1', '2', '3', '4'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=4x<super>3</super>-x+2 entre (2x-2) es:',
                  'alternativas': ['3', '4', '5', '6', '7'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>2</super>+5x-1 entre (x-1) es:',
                  'alternativas': ['3', '4', '5', '6', '7'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=2x<super>2</super>+7x-3 entre (x+3) es:',
                  'alternativas': ['-8', '-6', '-4', '-2', '0'],
                  'correcta': 'B'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>3</super>+3x<super>2</super>-2 '
                               'entre (x+2) es:',
                  'alternativas': ['-2', '0', '2', '4', '6'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=5x<super>2</super>-3x+2 entre (x-1) es:',
                  'alternativas': ['2', '3', '4', '5', '6'],
                  'correcta': 'C'},
                 {'enunciado': 'El resto de dividir '
                               'P(x)=x<super>4</super>-2x<super>3</super>+1 '
                               'entre (x-2) es:',
                  'alternativas': ['-1', '0', '1', '2', '3'],
                  'correcta': 'C'},
                 {'enunciado': 'El número de términos del cociente notable '
                               '(x<super>9</super>-y<super>9</super>)/(x-y) '
                               'es:',
                  'alternativas': ['7', '8', '9', '10', '11'],
                  'correcta': 'C'},
                 {'enunciado': 'El número de términos del cociente notable '
                               '(x<super>11</super>+y<super>11</super>)/(x+y) '
                               'es:',
                  'alternativas': ['9', '10', '11', '12', '13'],
                  'correcta': 'C'},
                 {'enunciado': 'El cuarto término del cociente notable '
                               '(x<super>7</super>-y<super>7</super>)/(x-y) '
                               'es:',
                  'alternativas': ['x²y⁴', 'x³y³', 'x⁴y²', 'x⁵y', 'xy⁵'],
                  'correcta': 'B'},
                 {'enunciado': 'El quinto término del cociente notable '
                               '(x<super>8</super>-y<super>8</super>)/(x-y) '
                               'es:',
                  'alternativas': ['x²y⁵', 'x³y⁴', 'x⁴y³', 'x⁵y²', 'x⁶y'],
                  'correcta': 'B'},
                 {'enunciado': 'El último término del cociente notable '
                               '(x<super>6</super>-y<super>6</super>)/(x-y) '
                               'es:',
                  'alternativas': ['y²', 'y³', 'y⁴', 'y⁵', 'y⁶'],
                  'correcta': 'D'},
                 {'enunciado': 'El primer término del cociente notable '
                               '(x<super>n</super>-y<super>n</super>)/(x-y), '
                               'para cualquier «n», es:',
                  'alternativas': ['x',
                                   'x<super>n</super>',
                                   'x<super>n-1</super>',
                                   'xy',
                                   'y<super>n-1</super>'],
                  'correcta': 'C'},
                 {'enunciado': 'El cociente '
                               '(x<super>5</super>-y<super>5</super>)/(x+y) '
                               'NO es un cociente notable porque «n»=5 es:',
                  'alternativas': ['par',
                                   'impar',
                                   'cero',
                                   'negativo',
                                   'fraccionario'],
                  'correcta': 'B'},
                 {'enunciado': 'El cociente '
                               '(x<super>6</super>-y<super>6</super>)/(x+y) '
                               'SÍ es cociente notable (tercer caso) porque '
                               '«n»=6 es:',
                  'alternativas': ['impar',
                                   'negativo',
                                   'par',
                                   'cero',
                                   'fraccionario'],
                  'correcta': 'C'},
                 {'enunciado': 'El cociente '
                               '(x<super>7</super>+y<super>7</super>)/(x+y) '
                               'SÍ es cociente notable (segundo caso) porque '
                               '«n»=7 es:',
                  'alternativas': ['par',
                                   'cero',
                                   'fraccionario',
                                   'impar',
                                   'negativo'],
                  'correcta': 'D'},
                 {'enunciado': 'El cociente '
                               '(x<super>4</super>+y<super>4</super>)/(x+y) '
                               'NO es cociente notable porque el segundo '
                               'caso requiere que «n» sea:',
                  'alternativas': ['par',
                                   'impar',
                                   'cero',
                                   'negativo',
                                   'cualquiera'],
                  'correcta': 'B'},
                 {'enunciado': 'El cociente '
                               '(x<super>n</super>+y<super>n</super>)/(x-y) '
                               'nunca es un cociente notable. Esto '
                               'corresponde al:',
                  'alternativas': ['Primer caso',
                                   'Segundo caso',
                                   'Tercer caso',
                                   'Cuarto caso',
                                   'Ningún caso'],
                  'correcta': 'D'},
                 {'enunciado': 'El número de términos del cociente notable '
                               '(x<super>13</super>-y<super>13</super>)/(x-y) '
                               'es:',
                  'alternativas': ['11', '12', '13', '14', '15'],
                  'correcta': 'C'},
                 {'enunciado': 'El sexto término del cociente notable '
                               '(x<super>9</super>-y<super>9</super>)/(x-y) '
                               'es:',
                  'alternativas': ['x²y⁶', 'x³y⁵', 'x⁴y⁴', 'x⁵y³', 'x⁶y²'],
                  'correcta': 'B'},
                 {'enunciado': 'El método para dividir polinomios cuando el '
                               'divisor es de segundo grado o mayor se llama '
                               'método de:',
                  'alternativas': ['Ruffini',
                                   'Horner',
                                   'Gauss',
                                   'Newton',
                                   'Descartes'],
                  'correcta': 'B'},
                 {'enunciado': 'El método para dividir polinomios cuando el '
                               'divisor es de primer grado (ax+b) se llama '
                               'método de:',
                  'alternativas': ['Horner',
                                   'Gauss',
                                   'Ruffini',
                                   'Newton',
                                   'Descartes'],
                  'correcta': 'C'},
                 {'enunciado': 'Según el Teorema del Resto, al dividir P(x) '
                               'entre (ax+b), el resto es igual a:',
                  'alternativas': ['P(a/b)',
                                   'P(-a/b)',
                                   'P(b/a)',
                                   'P(-b/a)',
                                   'P(ab)'],
                  'correcta': 'D'},
                 {'enunciado': 'Si al dividir P(x) entre (x-3) el residuo es '
                               '0, entonces la división es:',
                  'alternativas': ['Inexacta',
                                   'Imposible',
                                   'Exacta',
                                   'Indeterminada',
                                   'Negativa'],
                  'correcta': 'C'}],
  'qr_reto': [{'pregunta': '¿Cómo se calcula el resto de P(x)÷(ax+b)?',
               'respuesta': 'Resto = P(-b/a)'},
              {'pregunta': '¿Cuándo se usa el método de Ruffini?',
               'respuesta': 'Cuando el divisor es de primer grado'},
              {'pregunta': '¿Cuántos términos tiene (x⁵-y⁵)/(x-y)?',
               'respuesta': '5'}],
  'qr_dato': 'El Teorema del Resto también se conoce como "Teorema del '
             'Residuo", y es un caso particular de un principio más general '
             'usado en la división sintética. Paolo Ruffini, matemático '
             'italiano, publicó su método en 1809 — casi 200 años antes de '
             'que se enseñara en las escuelas de hoy.'}]
