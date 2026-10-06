# ================================================================
# SIMULACROS YACHAY — Calificación con la Hoja de Respuestas oficial
# ================================================================
#  1. ⚙️ Configurar : claves por grupo (A-B-C-D), cursos por rango de
#                     preguntas y puntaje por correcta / incorrecta.
#  2. 📸 Escanear   : lote de fotos / PDF escaneado o cámara hoja por hoja.
#  3. 🏆 Ranking    : general, por aula o grupo. PDF, Excel, imagen para
#                     redes y publicación al historial del estudiante.
#  4. 📚 Historial  : evolución de cada estudiante en todos los simulacros.
#  5. 📊 Análisis   : % de acierto por pregunta y por curso.
#
# Datos: simulacros_yachay.json (las notas se recalculan siempre a
# partir de las respuestas guardadas, así que si corriges una clave
# todo el ranking se actualiza solo).
# ================================================================

import base64
import html as _html
import io
import urllib.parse
import json
import re
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

import omr_yachay as omr

ARCHIVO_SIM = "simulacros_yachay.json"
HOJA_PDF = "Hoja_Yachay_en_blanco.pdf"
LOGO = "logo_academia.png"
GRUPOS = ["A", "B", "C", "D"]

# ----------------------------------------------------------------
# TEMARIO OFICIAL POR ÁREA (igual que el examen de admisión UNSAAC)
# (curso, n.º de preguntas) — el orden es el orden del examen
# ----------------------------------------------------------------
PLANTILLAS_AREA = {
    "A": [("Aritmética", 14), ("Álgebra", 10), ("Geometría y Trigonometría", 14),
          ("Competencia Comunicativa", 14), ("Física", 14), ("Química", 14)],
    "B": [("Aritmética", 14), ("Álgebra", 10), ("Competencia Comunicativa", 14),
          ("Biología", 14), ("Física", 14), ("Química", 14)],
    "C": [("Aritmética", 14), ("Álgebra", 10), ("Competencia Comunicativa", 14),
          ("Historia", 12), ("Geografía", 12), ("Economía", 10), ("Educación Cívica", 8)],
    "D": [("Aritmética", 14), ("Álgebra", 10), ("Competencia Comunicativa", 14),
          ("Historia", 12), ("Geografía", 12), ("Filosofía y Lógica", 10), ("Educación Cívica", 8)],
}
MODALIDADES = {
    "Grupo AB  (áreas A y B juntas)": ["A", "B"],
    "Grupo CD  (áreas C y D juntas)": ["C", "D"],
    "Solo Área A": ["A"],
    "Solo Área B": ["B"],
    "Solo Área C": ["C"],
    "Solo Área D": ["D"],
    "Las 4 áreas (A, B, C y D)": ["A", "B", "C", "D"],
}
# Colegio (Primaria / Secundaria / otros ciclos): una sola prueba y una sola clave.
# Los cursos salen de las áreas oficiales del sistema; el n.º de preguntas se puede cambiar.
PLANTILLAS_NIVEL = {
    "PRIMARIA": [("Comunicación", 10), ("Matemática", 10), ("Personal Social", 10),
                 ("Ciencia y Tecnología", 10)],
    "SECUNDARIA": [("Comunicación", 10), ("Matemática", 10), ("Ciencias Sociales", 10),
                   ("Desarrollo Personal, Ciudadanía y Cívica", 10), ("Ciencia y Tecnología", 10),
                   ("Inglés", 10)],
    "OTRO": [("Matemática", 20), ("Comunicación", 20)],
}
MODALIDADES_NIVEL = {
    "🏫 Primaria (Comunicación, Matemática, Personal Social, Ciencia y Tecnología)": "PRIMARIA",
    "🏫 Secundaria (Comunicación, Matemática, C. Sociales, DPCC, Ciencia y Tec., Inglés)": "SECUNDARIA",
    "🏫 Otro nivel o ciclo (cursos a mi gusto, una sola clave)": "OTRO",
}
MOD_PERSONALIZADO = "✏️ Personalizado (cursos y rangos a mi gusto)"

CURSOS_EJEMPLO = [
    ("Razonamiento Matemático", 1, 10), ("Aritmética y Álgebra", 11, 20),
    ("Geometría y Trigonometría", 21, 30), ("Física", 31, 40),
    ("Química", 41, 50), ("Biología", 51, 60),
    ("Razonamiento Verbal", 61, 70), ("Lenguaje y Literatura", 71, 80),
    ("Historia y Geografía", 81, 90), ("Economía y Cívica", 91, 100),
]

# ----------------------------------------------------------------
# Ganchos hacia sistema_web.py (se rellenan en tab_simulacros_yachay)
# ----------------------------------------------------------------
_HOOKS = {
    "cargar_matricula": None,     # -> DataFrame con DNI, Nombre, Grado, Seccion
    "cargar_historial": None,     # -> dict historial_evaluaciones.json
    "guardar_historial": None,    # (dict) -> bool
    "backup_json": None,          # (nombre, dict) -> respaldo Drive
    "puede_borrar": None,         # () -> bool
}


# ================================================================
# DATOS
# ================================================================
def cargar_datos():
    if Path(ARCHIVO_SIM).exists():
        try:
            with open(ARCHIVO_SIM, "r", encoding="utf-8") as f:
                d = json.load(f)
            if isinstance(d, dict) and "simulacros" in d:
                return d
        except Exception:
            pass
    return {"simulacros": {}}


def guardar_datos(d):
    with open(ARCHIVO_SIM, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    if _HOOKS["backup_json"]:
        try:
            _HOOKS["backup_json"](ARCHIVO_SIM, d)
        except Exception:
            pass


def limpiar_clave(texto, n):
    """Acepta 'ABCD...', 'a b c d', '1A 2B 3C' o una por línea."""
    t = (texto or "").upper()
    t = re.sub(r"\d+\s*[\.\)\-:]?", " ", t)      # quitar numeración
    letras = [c for c in t if c in "ABCDE"]
    return "".join(letras)[:n]


def norm_dni(v):
    s = re.sub(r"\D", "", str(v or ""))
    return s.zfill(8) if s else ""


def _matricula():
    f = _HOOKS["cargar_matricula"]
    if not f:
        return {}
    try:
        df = f()
    except Exception:
        return {}
    if df is None or df.empty:
        return {}
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    col_n = "Nombre" if "Nombre" in df.columns else ("Alumno" if "Alumno" in df.columns else None)
    if "DNI" not in df.columns or not col_n:
        return {}
    out = {}
    for _, r in df.iterrows():
        d = norm_dni(r.get("DNI"))
        if d:
            g = str(r.get("Grado", "") or "").strip()
            s = str(r.get("Seccion", "") or "").strip()
            nv = str(r.get("Nivel", "") or "").strip().upper()
            nv = "" if nv in ("NAN", "NONE") else nv
            g = "" if g.lower() == "nan" else g
            s = "" if s.lower() == "nan" else s
            out[d] = {"nombre": str(r.get(col_n, "")).strip().upper(),
                      "grado": (g + (" " + s if s else "")).strip(),
                      "nivel": nv, "grado0": g, "seccion": s,
                      "celular": next((re.sub(r"\D", "", str(r.get(c) or "")) for c in
                                       ("Celular_Apoderado", "celular_apoderado", "Celular", "Telefono", "WhatsApp")
                                       if re.sub(r"\D", "", str(r.get(c) or ""))), "")}
    return out


# ================================================================
# CALIFICACIÓN
# ================================================================
def grupos_sim(sim):
    """Áreas/grupos que participan en este simulacro (['A','B'], ['C'], ...)."""
    g = sim.get("grupos")
    if g:
        return list(g)
    ca = sim.get("cursos_area")
    if ca:
        return [x for x in GRUPOS if x in ca]
    return list(GRUPOS)


def grupo_efectivo(sim, grupo):
    """Área con la que se califica una hoja. None = no se pudo determinar."""
    ca = sim.get("cursos_area")
    if not ca:
        return grupo                      # simulacros antiguos: un solo esquema
    if grupo in ca:
        return grupo
    if len(ca) == 1:
        return next(iter(ca))
    return None


def cursos_union(sim):
    """Todos los cursos del simulacro (sin repetir nombres), en orden."""
    ca = sim.get("cursos_area")
    if not ca:
        return sim.get("cursos", [])
    vistos, out = set(), []
    for g in grupos_sim(sim):
        for c in ca.get(g, []):
            if c["nombre"] not in vistos:
                vistos.add(c["nombre"])
                out.append(c)
    return out


def cursos_de(sim, grupo):
    ca = sim.get("cursos_area")
    if not ca:
        return sim.get("cursos", [])
    ge = grupo_efectivo(sim, grupo)
    return ca[ge] if ge else cursos_union(sim)


def preguntas_validas(sim, grupo):
    """Números de pregunta (1..n) que rinde esa área. En el examen unificado hay preguntas
    de otras áreas que no cuentan (p. ej. Filosofía para el Área C)."""
    v = set()
    for c in cursos_de(sim, grupo):
        v.update(range(c["desde"], c["hasta"] + 1))
    return v


def n_preguntas(sim, grupo=None):
    ca = sim.get("cursos_area")
    if not ca:
        return int(sim.get("num_preguntas", 100))
    cs = cursos_de(sim, grupo)
    return max((c["hasta"] for c in cs), default=int(sim.get("num_preguntas", 80)))


def etiqueta_modalidad(sim):
    if sim.get("sin_area"):
        return {"PRIMARIA": "Primaria", "SECUNDARIA": "Secundaria"}.get(sim.get("modalidad"), "Cursos libres")
    if sim.get("cursos_area"):
        return "Áreas " + " + ".join(grupos_sim(sim)) + (" · todos los cursos" if sim.get("todos_cursos") else "")
    return "Personalizado"


def clave_para(sim, grupo):
    claves = sim.get("claves", {})
    if sim.get("cursos_area"):
        if sim.get("clave_comun"):
            return next((claves[g] for g in grupos_sim(sim) if claves.get(g)), "")
        ge = grupo_efectivo(sim, grupo)
        return claves.get(ge, "") if ge else ""
    if grupo in claves and claves[grupo]:
        return claves[grupo]
    for g in GRUPOS:
        if claves.get(g):
            return claves[g]
    return ""


def _pmax(cursos):
    return sum((c["hasta"] - c["desde"] + 1) * float(c["correcta"]) for c in cursos)


def puntaje_maximo(sim, grupo=None):
    ca = sim.get("cursos_area")
    if not ca:
        return _pmax(sim["cursos"])
    if grupo is not None:
        ge = grupo_efectivo(sim, grupo)
        if ge:
            return _pmax(ca[ge])
    return max((_pmax(v) for v in ca.values()), default=0)


def calificar(sim, hoja):
    clave = clave_para(sim, hoja.get("grupo", ""))
    cursos = cursos_de(sim, hoja.get("grupo", ""))
    resp = hoja.get("respuestas", "")
    blanco = float(sim.get("puntaje_blanco", 0))
    out = {"correctas": 0, "incorrectas": 0, "blancos": 0, "puntaje": 0.0, "cursos": {}}
    for c in cursos:
        cc = ci = cb = 0
        for q in range(c["desde"] - 1, c["hasta"]):
            k = clave[q] if q < len(clave) else ""
            r = resp[q] if q < len(resp) else "_"
            if not k or k not in "ABCD":
                continue                       # pregunta anulada / sin clave
            if r == k:
                cc += 1
            elif r in ("_", "", " ", "-"):
                cb += 1
            else:
                ci += 1                        # incluye doble marca '*'
        pts = cc * float(c["correcta"]) + ci * float(c["incorrecta"]) + cb * blanco
        maxc = (c["hasta"] - c["desde"] + 1) * float(c["correcta"])
        out["cursos"][c["nombre"]] = {
            "correctas": cc, "incorrectas": ci, "blancos": cb, "puntaje": round(pts, 2),
            "nota": round(max(pts, 0) / maxc * 20, 2) if maxc else 0.0}
        out["correctas"] += cc
        out["incorrectas"] += ci
        out["blancos"] += cb
        out["puntaje"] += pts
    out["puntaje"] = round(out["puntaje"], 2)
    mx = puntaje_maximo(sim, hoja.get("grupo", ""))
    out["nota"] = round(max(out["puntaje"], 0) / mx * 20, 2) if mx else 0.0
    return out


def tabla_ranking(sim, filtro_aula=None, filtro_grupo=None):
    filas = []
    nombres_c = [x["nombre"] for x in cursos_union(sim)]
    for hid, h in sim.get("hojas", {}).items():
        if filtro_aula and h.get("aula") != filtro_aula:
            continue
        if filtro_grupo and h.get("grupo") != filtro_grupo:
            continue
        c = calificar(sim, h)
        f = {"ID": hid, "DNI": h.get("dni", ""), "Apellidos y Nombres": h.get("nombre", "") or "(sin nombre)",
             "Aula": h.get("aula", ""), "Grupo": "" if sim.get("sin_area") else h.get("grupo", "")}
        for cn in nombres_c:
            f[cn] = c["cursos"][cn]["correctas"] if cn in c["cursos"] else None
        f.update({"Correctas": c["correctas"], "Incorrectas": c["incorrectas"],
                  "Blancos": c["blancos"], "Puntaje": c["puntaje"], "Nota": c["nota"]})
        filas.append(f)
    if not filas:
        return pd.DataFrame()
    df = pd.DataFrame(filas).sort_values(
        ["Puntaje", "Correctas", "Incorrectas", "Apellidos y Nombres"],
        ascending=[False, False, True, True]).reset_index(drop=True)
    # Puesto con empates (1, 1, 3 ...)
    puestos, prev, pos = [], None, 0
    for i, p in enumerate(df["Puntaje"]):
        if p != prev:
            pos = i + 1
            prev = p
        puestos.append(pos)
    df.insert(0, "Puesto", puestos)
    return df


# ================================================================
# PDF / IMAGEN
# ================================================================
def _logo_reader():
    try:
        from reportlab.lib.utils import ImageReader
        if Path(LOGO).exists():
            return ImageReader(LOGO)
    except Exception:
        pass
    return None


def _encabezado(c, ancho, alto, titulo, subtitulo):
    from reportlab.lib import colors
    c.setFillColor(colors.HexColor("#7a1f5c"))
    c.rect(0, alto - 70, ancho, 70, fill=1, stroke=0)
    lg = _logo_reader()
    if lg:
        c.drawImage(lg, 18, alto - 64, 58, 58, mask="auto", preserveAspectRatio=True)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(ancho / 2, alto - 28, "ACADEMIA PREUNIVERSITARIA YACHAY")
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(ancho / 2, alto - 45, titulo.upper())
    c.setFont("Helvetica", 9)
    c.drawCentredString(ancho / 2, alto - 60, subtitulo)
    c.setFillColor(colors.black)


def pdf_ranking(sim, df, titulo_extra="", detalle_cursos=True):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Table, TableStyle

    pag = landscape(A4) if detalle_cursos else A4
    ancho, alto = pag
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=pag)
    cursos = [x["nombre"] for x in cursos_union(sim)]
    base_cols = ["Puesto", "Apellidos y Nombres", "DNI", "Aula"] + ([] if sim.get("sin_area") else ["Grupo"])
    cols = list(base_cols)
    if detalle_cursos:
        cols += cursos
    cols += ["Correctas", "Incorrectas", "Puntaje", "Nota"]
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph
    est_cab = ParagraphStyle("cab", fontName="Helvetica-Bold", fontSize=6.5 if detalle_cursos else 8,
                             leading=7.5 if detalle_cursos else 9, alignment=1)
    cab = [Paragraph({"Puesto": "Pto", "Aula": "Grado"}.get(x, x), est_cab) for x in cols]

    def _fmt(x, v):
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return "-"
        if x in cursos:
            return str(int(v))
        if x == "Apellidos y Nombres":
            return str(v)[:40]
        if x == "Nota":
            return f"{float(v):.2f}"
        if x == "Puntaje":
            return f"{float(v):g}"
        return str(v)
    from reportlab.platypus import Image as RLImage

    def _celda_nombre(r):
        h = sim["hojas"].get(r["ID"], {})
        if (not h.get("nombre")) and h.get("nombre_img"):
            try:
                return RLImage(io.BytesIO(base64.b64decode(h["nombre_img"])), width=150, height=34)
            except Exception:
                pass
        return _fmt("Apellidos y Nombres", r["Apellidos y Nombres"])
    filas = [[(_celda_nombre(r) if x == "Apellidos y Nombres" else _fmt(x, r[x])) for x in cols] for _, r in df.iterrows()]
    por_pag = 22 if detalle_cursos else 34
    sub = f"{sim.get('fecha', '')}  ·  {titulo_extra}  ·  Puntaje máximo: {puntaje_maximo(sim):g}"
    for ini in range(0, max(len(filas), 1), por_pag):
        _encabezado(c, ancho, alto, f"RANKING — {sim['titulo']}", sub)
        data = [cab] + filas[ini:ini + por_pag]
        anchos = None
        if detalle_cursos:
            resto = ancho - 50 - 26 - 160 - 58 - 62 - (0 if sim.get("sin_area") else 34)
            otros = max(len(cols) - len(base_cols), 1)
            anchos = ([26, 160, 58, 62] + ([] if sim.get("sin_area") else [34])) + [resto / otros] * otros
        t = Table(data, colWidths=anchos, repeatRows=1)
        est = [
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7 if detalle_cursos else 8),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3d1e6")),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("ALIGN", (1, 1), (1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fbf0f7")]),
        ]
        for k, fila in enumerate(data[1:], start=1):
            if str(fila[0]) in ("1", "2", "3"):
                col = {"1": "#ffe08a", "2": "#e5e7eb", "3": "#f5c9a0"}[str(fila[0])]
                est.append(("BACKGROUND", (0, k), (-1, k), colors.HexColor(col)))
                est.append(("FONTNAME", (0, k), (-1, k), "Helvetica-Bold"))
        t.setStyle(TableStyle(est))
        tw, th = t.wrapOn(c, ancho - 40, alto - 120)
        t.drawOn(c, (ancho - tw) / 2, alto - 85 - th)
        c.setFont("Helvetica-Oblique", 7)
        c.drawString(20, 15, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')} — Sistema Yachay")
        c.showPage()
    c.save()
    return buf.getvalue()


def _boleta_en_canvas(c, sim, hoja, fila_rank, total):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import Table, TableStyle
    ancho, alto = A4
    res = calificar(sim, hoja)
    clave = clave_para(sim, hoja.get("grupo", ""))
    _encabezado(c, ancho, alto, f"Resultado individual — {sim['titulo']}", sim.get("fecha", ""))
    y = alto - 95
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, f"Estudiante: {hoja.get('nombre', '')}")
    c.drawString(400, y, f"DNI: {hoja.get('dni', '')}")
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Grado: {hoja.get('aula', '') or '-'}" +
                 ("" if sim.get("sin_area") else f"     Área: {hoja.get('grupo', '') or '-'}"))
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#7a1f5c"))
    c.drawString(330, y - 2, f"PUESTO {fila_rank} de {total}   ·   NOTA {res['nota']:.2f}")
    c.setFillColor(colors.black)

    data = [["Curso", "Preg.", "Correctas", "Incorrectas", "En blanco", "Puntaje", "Nota /20"]]
    for cu in cursos_de(sim, hoja.get("grupo", "")):
        r = res["cursos"][cu["nombre"]]
        data.append([cu["nombre"], f"{cu['desde']}-{cu['hasta']}", r["correctas"], r["incorrectas"],
                     r["blancos"], f"{r['puntaje']:g}", f"{r['nota']:.2f}"])
    data.append(["TOTAL", "", res["correctas"], res["incorrectas"], res["blancos"],
                 f"{res['puntaje']:g}", f"{res['nota']:.2f}"])
    t = Table(data, colWidths=[170, 50, 60, 65, 60, 55, 55])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3d1e6")),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#fde68a")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("ALIGN", (1, 0), (-1, -1), "CENTER")]))
    tw, th = t.wrapOn(c, ancho, alto)
    t.drawOn(c, (ancho - tw) / 2, y - 25 - th)
    y = y - 45 - th

    # Detalle de respuestas
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, y, "Detalle por pregunta (marcada / clave):  ✔ correcta   ✘ incorrecta   — en blanco")
    y -= 14
    validas = sorted(preguntas_validas(sim, hoja.get("grupo", ""))) if sim.get("cursos_area") \
        else list(range(1, n_preguntas(sim, hoja.get("grupo", "")) + 1))
    resp = hoja.get("respuestas", "")
    c.setFont("Helvetica", 7.5)
    col_w, fil_h, por_col = 103, 11.2, 25
    for pos, qn in enumerate(validas):
        q = qn - 1
        col, fil = divmod(pos, por_col)
        x0, y0 = 40 + col * col_w, y - fil * fil_h
        r = resp[q] if q < len(resp) else "_"
        k = clave[q] if q < len(clave) else "?"
        marca = "—" if r in "_ -" else r
        if r == k:
            c.setFillColor(colors.HexColor("#15803d")); simb = "✔"
        elif r in "_ -":
            c.setFillColor(colors.HexColor("#6b7280")); simb = "—"
        else:
            c.setFillColor(colors.HexColor("#b91c1c")); simb = "✘"
        c.drawString(x0, y0, f"{q + 1:>3}.  {marca} / {k}  {simb}")
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Oblique", 7)
    c.drawString(40, 20, "Documento generado por el Sistema Yachay — Lectura óptica automática")


def pdf_boletas(sim, hids):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    df = tabla_ranking(sim)
    puesto = dict(zip(df["ID"], df["Puesto"])) if not df.empty else {}
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    for hid in hids:
        h = sim["hojas"].get(hid)
        if h:
            _boleta_en_canvas(c, sim, h, puesto.get(hid, "-"), len(df))
            c.showPage()
    c.save()
    return buf.getvalue()


def png_publicar(sim, df, top=10, titulo_extra=""):
    from PIL import Image, ImageDraw, ImageFont
    W, Hh = 1080, 1350
    img = Image.new("RGB", (W, Hh), "#fdf2f8")
    d = ImageDraw.Draw(img)

    def f(sz, b=False):
        try:
            return ImageFont.truetype(
                f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf", sz)
        except Exception:
            return ImageFont.load_default()
    d.rectangle([0, 0, W, 230], fill="#7a1f5c")
    if Path(LOGO).exists():
        try:
            lg = Image.open(LOGO).convert("RGBA")
            lg.thumbnail((170, 170))
            img.paste(lg, (30, 30), lg)
        except Exception:
            pass
    d.text((W // 2 + 60, 60), "ACADEMIA YACHAY", font=f(52, True), fill="white", anchor="mm")
    d.text((W // 2 + 60, 125), sim["titulo"].upper()[:34], font=f(34, True), fill="#fde68a", anchor="mm")
    d.text((W // 2 + 60, 180), f"{sim.get('fecha', '')} {titulo_extra}"[:50], font=f(26), fill="white", anchor="mm")
    d.text((W // 2, 290), f"TOP {top}", font=f(46, True), fill="#7a1f5c", anchor="mm")
    y = 350
    medal = {1: "#f59e0b", 2: "#9ca3af", 3: "#b45309"}
    for _, r in df.head(top).iterrows():
        p = int(r["Puesto"])
        d.rounded_rectangle([60, y, W - 60, y + 82], 18, fill="white", outline="#f3d1e6", width=3)
        d.ellipse([80, y + 11, 140, y + 71], fill=medal.get(p, "#7a1f5c"))
        d.text((110, y + 41), str(p), font=f(30, True), fill="white", anchor="mm")
        d.text((165, y + 41), str(r["Apellidos y Nombres"])[:30], font=f(30, True), fill="#111827", anchor="lm")
        d.text((W - 85, y + 41), f"{r['Puntaje']:g}", font=f(32, True), fill="#7a1f5c", anchor="rm")
        y += 94
    d.text((W // 2, Hh - 40), "¡Felicitaciones a todos los participantes!", font=f(28, True),
           fill="#7a1f5c", anchor="mm")
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def excel_ranking(sim, df):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.drop(columns=["ID"], errors="ignore").to_excel(w, sheet_name="Ranking", index=False)
        filas = []
        for hid, h in sim.get("hojas", {}).items():
            c = calificar(sim, h)
            fila = {"DNI": h.get("dni"), "Nombre": h.get("nombre"), "Grupo": "" if sim.get("sin_area") else h.get("grupo")}
            for cn, cv in c["cursos"].items():
                fila[f"{cn} (nota)"] = cv["nota"]
                fila[f"{cn} (pts)"] = cv["puntaje"]
            fila["Respuestas"] = h.get("respuestas", "")
            filas.append(fila)
        pd.DataFrame(filas).to_excel(w, sheet_name="Detalle", index=False)
        pd.DataFrame([{"Grupo": g, "Clave": sim["claves"].get(g, "")} for g in grupos_sim(sim)]).to_excel(
            w, sheet_name="Claves", index=False)
    return buf.getvalue()


# ================================================================
# PUBLICAR EN HISTORIAL (historial_evaluaciones.json → portal estudiante)
# ================================================================
def _fecha_iso(txt):
    """'02/10/2026' -> '2026-10-02' (formato del historial de evaluaciones del sistema)."""
    m = re.search(r"(\d{1,2})\D+(\d{1,2})\D+(\d{4})", str(txt or ""))
    return f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}" if m else str(txt or "")


def publicar_en_historial(sim):
    cargar, guardar = _HOOKS["cargar_historial"], _HOOKS["guardar_historial"]
    if not (cargar and guardar):
        return False
    hist = cargar() or {}
    hist = dict(hist)
    df = tabla_ranking(sim)
    ranking = []
    for _, r in df.iterrows():
        h = sim["hojas"][r["ID"]]
        c = calificar(sim, h)
        fila = {"Puesto": int(r["Puesto"]), "DNI": h.get("dni", ""), "Nombre": h.get("nombre", ""),
                "Aula": h.get("aula", ""), "Grupo": "" if sim.get("sin_area") else h.get("grupo", ""),
                "Puntaje": c["puntaje"], "Correctas": c["correctas"], "Promedio": c["nota"],
                "Medalla": {1: "🥇", 2: "🥈", 3: "🥉"}.get(int(r["Puesto"]), "")}
        for cn, cv in c["cursos"].items():
            fila[cn] = cv["nota"]
        ranking.append(fila)
    hist[f"SIMYACHAY_{sim['id']}"] = {
        "titulo": sim["titulo"], "fecha": _fecha_iso(sim.get("fecha", "")), "periodo": sim.get("periodo", ""),
        "tipo": "simulacro_yachay", "areas": [{"nombre": c["nombre"]} for c in cursos_union(sim)],
        "ranking": ranking, "total": len(ranking), "puntaje_maximo": puntaje_maximo(sim)}
    return bool(guardar(hist))


def quitar_de_historial(sim):
    cargar, guardar = _HOOKS["cargar_historial"], _HOOKS["guardar_historial"]
    if not (cargar and guardar):
        return False
    hist = dict(cargar() or {})
    hist.pop(f"SIMYACHAY_{sim['id']}", None)
    return bool(guardar(hist))


# ================================================================
# HOJA DE RESPUESTAS CON QR (una hoja por simulacro)
# ================================================================
# ================================================================
# HOJA DE RESPUESTAS CON QR — dibujada en VECTORES (nítida al imprimir)
# ================================================================
# Todo (cuadros, burbujas, textos) se dibuja con trazos vectoriales, no con una foto:
# queda perfectamente nítido a cualquier tamaño. Las posiciones son las mismas que lee
# el lector óptico (omr_yachay.py), medidas a 300 dpi sobre una hoja de 2480 x 3508 px.
_K = 0.24                   # puntos PDF por píxel de la hoja
_PAG_H = 841.92
_BASE_CACHE = {}


def _matriz_qr(texto):
    """Matriz de módulos del QR (True = oscuro), con 2 módulos de margen."""
    try:
        import cv2
        enc = cv2.QRCodeEncoder.create() if hasattr(cv2.QRCodeEncoder, "create") else cv2.QRCodeEncoder_create()
        return enc.encode(texto) < 128
    except Exception:
        import numpy as np
        import qrcode                      # respaldo (ya está en requirements.txt)
        qr = qrcode.QRCode(border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(texto)
        qr.make(fit=True)
        return np.array(qr.get_matrix(), dtype=bool)


def codigo_qr(sim):
    return omr.QR_PREFIJO + str(sim.get("id", ""))


def _latin(t, n=60):
    t = str(t or "").replace("\n", " ").replace("—", "-").replace("–", "-").replace("·", "-").strip()
    return "".join(ch if ord(ch) < 256 else "?" for ch in t)[:n]


def _logo(b64):
    from reportlab.lib.utils import ImageReader
    return ImageReader(io.BytesIO(base64.b64decode(b64)))


def _dibujar_hoja(c, sim=None):
    from reportlab.lib import colors
    from reportlab.pdfbase.pdfmetrics import stringWidth
    K, PH = _K, _PAG_H
    X = lambda v: v * K
    Y = lambda v: PH - v * K
    rgb = lambda r, g, b: colors.Color(r / 255.0, g / 255.0, b / 255.0)
    NEGRO, BLANCO = colors.black, colors.white
    ROSA, ROSA_CAB, ROSA_CLARO = rgb(255, 225, 240), rgb(252, 204, 230), rgb(253, 236, 246)
    MORADO, MORADO2, GLIFO = rgb(139, 36, 91), rgb(150, 42, 104), rgb(138, 100, 122)
    TINTA, GRIS = rgb(20, 20, 22), rgb(107, 114, 128)

    def rel(x, y, w, h, color):                       # rectángulo (origen arriba-izquierda, en px)
        c.setFillColor(color)
        c.rect(X(x), Y(y + h), X(w), X(h), stroke=0, fill=1)

    def caja(x, y, w, h, bw, fondo=BLANCO):           # marco negro + relleno
        rel(x, y, w, h, NEGRO)
        rel(x + bw, y + bw, w - 2 * bw, h - 2 * bw, fondo)

    def anillo(cx, cy, ro, sw, borde, fondo=BLANCO):
        c.setFillColor(borde)
        c.circle(X(cx), Y(cy), X(ro), stroke=0, fill=1)
        c.setFillColor(fondo)
        c.circle(X(cx), Y(cy), X(ro - sw), stroke=0, fill=1)

    def ancho_nat(t, cap, fuente="Helvetica-Bold"):
        return stringWidth(t, fuente, cap * K / 0.718) / K

    def texto(t, x, base, cap, ancho=None, color=TINTA, alinea="l", fuente="Helvetica-Bold"):
        size = cap * K / 0.718
        w0 = stringWidth(t, fuente, size)
        sx = (ancho * K / w0) if ancho else 1.0
        wf = w0 * sx
        x0 = X(x) - (0 if alinea == "l" else (wf / 2 if alinea == "c" else wf))
        c.saveState()
        c.translate(x0, Y(base))
        c.scale(sx, 1)
        c.setFillColor(color)
        c.setFont(fuente, size)
        c.drawString(0, 0, t)
        c.restoreState()

    def puntos(x0, x1, y):                             # línea punteada para escribir
        c.setFillColor(rgb(60, 60, 60))
        x = x0
        while x <= x1:
            c.circle(X(x + 2), Y(y), X(2), stroke=0, fill=1)
            x += 14

    # ---------- marcas de las 4 esquinas (alinean la hoja al escanear) ----------
    for (mx, my) in ((40, 40), (2350, 40), (40, 3378), (2350, 3378)):
        rel(mx, my, 91, 91, NEGRO)
    rel(40, 150, 91, 26, NEGRO)                        # marca de orientación (arriba-izquierda)
    h = omr.AJ_TAM
    for (mx, my, _g) in omr.marcas_ajuste():           # cuadraditos de ajuste (como ZipGrade)
        rel(mx - h / 2.0, my - h / 2.0, h, h, NEGRO)

    # ---------- encabezado ----------
    caja(160, 110, 2161, 281, 5, ROSA)
    c.drawImage(_logo(_LOGO_IZQ_B64), X(184), Y(124 + 252), X(252), X(252), mask="auto")
    xl = 1857 if (sim and sim.get("id")) else 2092   # con QR el logo se corre a la izquierda
    c.drawImage(_logo(_LOGO_DER_B64), X(xl), Y(188 + 124), X(176), X(124), mask="auto")
    texto("INSTITUCIÓN EDUCATIVA", 673, 207, 69, 1140)
    texto("ALTERNATIVO YACHAY", 734, 302, 69, 1012)
    texto("ACADEMIA PREUNIVERSITARIA YACHAY", 672, 370, 44, 1136)

    # ---------- apellidos y nombres ----------
    caja(160, 420, 1128, 401, 4)
    texto("APELLIDOS", 190, 458, 26, 190)
    rel(190, 470, 1068, 115, MORADO)
    rel(193, 473, 1062, 109, BLANCO)
    puntos(205, 1240, 560)
    texto("NOMBRES", 190, 636, 26, 160)
    rel(190, 645, 1068, 115, MORADO)
    rel(193, 648, 1062, 109, BLANCO)
    puntos(205, 1240, 735)
    texto("Si no recuerdas tu DNI, escribe con letra clara tus apellidos y nombres.", 190, 800, 17, 1000,
          color=GRIS, fuente="Helvetica")

    # ---------- datos del estudiante (grupo) ----------
    caja(160, 850, 1128, 251, 4)
    rel(164, 854, 1120, 67, ROSA_CAB)
    rel(164, 922, 1120, 4, NEGRO)
    texto("DATOS DEL ESTUDIANTE", 407, 906, 40, 633)
    texto("GRUPO:", 193, 1035, 41, 220)
    for cx, ch in zip(omr.GRUPO_X, "ABCD"):
        anillo(cx + 0.5, 1015.5, 36.5, 4, NEGRO)
        texto(ch, cx + 0.5, 1030, 31, color=TINTA, alinea="c")
    texto("MARCA SOLO", 1160, 1000, 19, 205, alinea="c")
    texto("UNA LETRA:", 1160, 1030, 19, 205, alinea="c")
    texto("TU ÁREA", 1160, 1060, 19, 150, alinea="c")

    # ---------- bloque Día / Mes / Año / DNI ----------
    caja(1317, 420, 1004, 681, 4, ROSA_CLARO)
    rel(1321, 424, 996, 53, ROSA_CAB)
    rel(1321, 477, 996, 4, NEGRO)
    for xd in (1457, 1597, 1827):
        rel(xd, 424, 7, 673, NEGRO)
    for t, x0, x1 in (("Día", 1356, 1425), ("Mes", 1487, 1574),
                      ("Año", 1671, 1757), ("DNI", 2037, 2112)):
        texto(t, x0, 465, 32, x1 - x0)

    def cuadro(cx):
        rel(cx - 25, 488, 50, 51, MORADO)
        rel(cx - 22, 491, 44, 45, BLANCO)
    for cx in (1360.5, 1420.5, 1500.5, 1560.5):
        cuadro(cx)
    for k in range(8):
        cuadro(omr.DNI_X[k])

    def burbuja(cx, cy, ch):
        anillo(cx, cy, 19.5, 3, MORADO)
        texto(ch, cx, cy + 7.5, 16.5, color=GLIFO, alinea="c")

    cy0, dy = omr.CAB_Y0, omr.CAB_DY
    for r in range(10):                                # Día (decenas 0-3, unidades 0-9) y Mes (0-1, 0-9)
        cy = cy0 + dy * r
        if r <= 3:
            burbuja(omr.DIA_X[0], cy, str(r))
        burbuja(omr.DIA_X[1], cy, str(r))
        if r <= 1:
            burbuja(omr.MES_X[0], cy, str(r))
        burbuja(omr.MES_X[1], cy, str(r))
    for r in range(10):                                # DNI: 8 dígitos
        cy = cy0 + dy * r
        texto(str(r), 1856, cy + 8.5, 22, alinea="c")
        for k in range(8):
            burbuja(omr.DNI_X[k], cy, str(r))
    for yy, an in zip(omr.ANIO_Y, omr.ANIOS):          # Año
        anillo(1645.5, yy, 22.5, 3, MORADO)
        texto(str(an), 1688, yy + 13.5, 29.5, 94)

    # ---------- las 100 respuestas ----------
    for col, bx in enumerate((160, 700, 1240, 1780)):
        caja(bx, 1165, 521, 2011, 3)
        for k in range(0, 25, 2):
            y = 1175 + 80 * k
            rel(bx + 3, y, 515, min(81, 3173 - y), ROSA_CLARO)
        for fil in range(25):
            q = col * 25 + fil
            cy = omr.RESP_Y0 + omr.RESP_DY * fil
            texto(str(q + 1), bx + 86, cy + 12.5, 29, alinea="r")
            for j, ch in enumerate("ABCD"):
                cx = omr.RESP_X[col][j]
                anillo(cx, cy, 27.5, 4, MORADO2)
                texto(ch, cx, cy + 8.5, 22, color=GLIFO, alinea="c")

    # ---------- pie 1: datos del simulacro ----------
    caja(160, 3215, 2161, 121, 4, ROSA)
    if sim:
        titulo = _latin(sim.get("titulo"), 80).upper()
        cap = 40
        while cap > 26 and ancho_nat(titulo, cap) > 1130:
            cap -= 1
        texto("SIMULACRO", 200, 3252, 15, color=GRIS)
        texto(titulo, 200, 3312, cap, min(ancho_nat(titulo, cap), 1130))
        if sim.get("sin_area"):
            area = etiqueta_modalidad(sim).upper()
        elif sim.get("cursos_area"):
            area = " + ".join(grupos_sim(sim))
        else:
            area = ""
        if area:
            texto("ÁREAS" if not sim.get("sin_area") else "NIVEL", 1380, 3252, 15, color=GRIS)
            texto(_latin(area, 18), 1380, 3312, 40)
        texto("FECHA", 1760, 3252, 15, color=GRIS)
        texto(_latin(sim.get("fecha"), 16), 1760, 3312, 40)
        texto("Cód. " + _latin(sim.get("id"), 24), 2290, 3252, 13, color=GRIS, alinea="r", fuente="Helvetica")
    else:
        # Hoja genérica (impresión por millares): nada que dependa de un examen concreto.
        texto("SIGE  -  SISTEMA INTEGRAL DE GESTIÓN EDUCATIVA", 1240.5, 3276, 36, 1900, alinea="c")
        texto("I.E.P. ALTERNATIVO YACHAY   ·   ACADEMIA PREUNIVERSITARIA YACHAY   ·   HOJA DE RESPUESTAS CON LECTURA ÓPTICA",
              1240.5, 3314, 19, 1900, color=GRIS, alinea="c", fuente="Helvetica")

    # ---------- QR del simulacro (esquina derecha del encabezado) ----------
    if sim and sim.get("id"):
        m = _matriz_qr(codigo_qr(sim))
        n = m.shape[0]
        mod, x0, y0 = 7.6, 2082, 142                   # QR de ~220 px (18.6 mm)
        rel(x0 - 6, y0 - 6, n * mod + 12, n * mod + 12, BLANCO)
        c.setFillColor(colors.black)
        for f in range(n):                             # tramos horizontales: sin rendijas
            j = 0
            while j < n:
                if m[f, j]:
                    k = j
                    while k + 1 < n and m[f, k + 1]:
                        k += 1
                    c.rect(X(x0 + j * mod), Y(y0 + (f + 1) * mod + 0.4),
                           X((k - j + 1) * mod + 0.4), X(mod + 0.4), fill=1, stroke=0)
                    j = k + 1
                else:
                    j += 1

    # ---------- pie 2: instrucciones ----------
    caja(160, 3350, 2161, 121, 4)
    rel(1009, 3354, 3, 113, NEGRO)
    rel(1450, 3354, 3, 113, NEGRO)
    lapiz = [(259, 3410), (253, 3427), (242, 3456), (238, 3461), (233, 3460), (217, 3455),
             (219, 3445), (234, 3400), (238, 3397), (247, 3400), (258, 3405)]
    p = c.beginPath()
    p.moveTo(X(lapiz[0][0]), Y(lapiz[0][1]))
    for (px, py) in lapiz[1:]:
        p.lineTo(X(px), Y(py))
    p.close()
    c.setFillColor(rgb(249, 221, 121))
    c.setStrokeColor(rgb(60, 45, 0))
    c.setLineWidth(3 * K)
    c.drawPath(p, fill=1, stroke=1)
    texto("UTILIZAR ÚNICAMENTE:", 303, 3396, 24.5, 400)
    texto("LÁPIZ 2B  O  LAPICERO NEGRO", 303, 3449, 27, 580)
    # marcas incorrectas / correcta (ejemplos)
    cyi = 3398.5
    for cx in (1070.5, 1148.5):                        # círculo tachado con X
        anillo(cx, cyi, 26.5, 4, NEGRO)
        c.setStrokeColor(NEGRO)
        c.setLineWidth(4 * K)
        c.line(X(cx - 18.5), Y(cyi - 18.5), X(cx + 18.5), Y(cyi + 18.5))
        c.line(X(cx - 18.5), Y(cyi + 18.5), X(cx + 18.5), Y(cyi - 18.5))
    anillo(1226.5, cyi, 26.5, 4, NEGRO)                # punto pequeño dentro del círculo
    c.setFillColor(rgb(80, 80, 80))
    c.circle(X(1226.5), Y(cyi), X(16.5), stroke=0, fill=1)
    anillo(1304.5, cyi, 26.5, 4, NEGRO)                # visto
    c.setStrokeColor(NEGRO)
    c.setLineWidth(5 * K)
    c.setLineCap(1)
    c.setLineJoin(1)
    pv = c.beginPath()
    pv.moveTo(X(1304.5 - 17), Y(cyi + 1))
    pv.lineTo(X(1304.5 - 7), Y(cyi + 16))
    pv.lineTo(X(1304.5 + 22), Y(cyi - 24))
    c.drawPath(pv, fill=0, stroke=1)
    texto("MARCAS INCORRECTAS", 1029, 3454, 20, 321)
    texto("Rellene el círculo", 1530, 3392, 19.5, 240)
    texto("completamente", 1540, 3422, 20, 219)
    c.setFillColor(NEGRO)
    c.circle(X(1860.5), Y(cyi), X(28.5), stroke=0, fill=1)
    texto("MARCA CORRECTA", 1732, 3454, 20, 256)


def hoja_pdf(sim=None):
    """PDF A4 de la hoja de respuestas (vectorial, nítido). Con `sim`: lleva el QR del simulacro,
    su título, áreas y fecha impresos. Sin `sim`: hoja genérica con líneas para escribir a mano."""
    from reportlab.pdfgen import canvas
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(595.2, _PAG_H))
    c.setTitle("Hoja de respuestas Yachay")
    c.setSubject("yachay-v3-vector")
    _dibujar_hoja(c, sim)
    c.showPage()
    c.save()
    return buf.getvalue()


def pdf_hojas_corregidas(sim, ids):
    """PDF con una página por alumno: la hoja de respuestas con sus marcas y la corrección
    (verde = correcta, rojo = incorrecta, punto verde = la correcta), más su nota abajo."""
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.pdfgen import canvas
    K, PH = _K, _PAG_H
    X, Y = (lambda v: v * K), (lambda v: PH - v * K)
    puestos = {r["ID"]: (int(r["Puesto"]), len(tabla_ranking(sim))) for _, r in tabla_ranking(sim).iterrows()}
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(595.2, PH))
    c.setTitle("Hojas corregidas - " + str(sim.get("titulo", "")))
    c.beginForm("hojabase")
    _dibujar_hoja(c, None)
    c.endForm()
    VERDE, ROJO, NARANJA = colors.Color(0, .62, .25), colors.Color(.85, .1, .1), colors.Color(1, .55, 0)
    TINTA = colors.Color(.1, .1, .45)

    def disco(cx, cy, r, col):
        c.setFillColor(col)
        c.circle(X(cx), Y(cy), X(r), stroke=0, fill=1)

    def aro(cx, cy, r, col, w=5):
        c.setStrokeColor(col)
        c.setLineWidth(X(w))
        c.circle(X(cx), Y(cy), X(r), stroke=1, fill=0)

    def txt(t, x, base, cap, ancho=None, color=colors.black, centro=False):
        size = cap * K / 0.718
        w0 = stringWidth(t, "Helvetica-Bold", size)
        sx = min(1.0, ancho * K / w0) if ancho else 1.0
        c.saveState()
        c.translate(X(x) - (w0 * sx / 2 if centro else 0), Y(base))
        c.scale(sx, 1)
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", size)
        c.drawString(0, 0, t)
        c.restoreState()

    for hid in ids:
        h = sim["hojas"].get(hid)
        if not h:
            continue
        c.doForm("hojabase")
        grupo = h.get("grupo", "")
        clave = clave_para(sim, grupo)
        val = preguntas_validas(sim, grupo) if sim.get("cursos_area") else None
        resp = h.get("respuestas", "")
        res = calificar(sim, h)
        for i in range(len(resp)):
            if val is not None and (i + 1) not in val:
                continue
            r_ = resp[i]
            k_ = clave[i] if i < len(clave) else ""
            if r_ in "ABCD" and r_:
                cx, cy = omr.posicion_respuesta(i, "ABCD".index(r_))
                disco(cx, cy, 19, TINTA)
                if k_ in "ABCD" and k_:
                    aro(cx, cy, 31, VERDE if r_ == k_ else ROJO)
                    if r_ != k_:
                        kx, ky = omr.posicion_respuesta(i, "ABCD".index(k_))
                        disco(kx, ky, 11, VERDE)
            elif r_ == "*":
                for j in range(4):
                    aro(*omr.posicion_respuesta(i, j), 30, NARANJA)
            elif k_ in "ABCD" and k_:
                aro(*omr.posicion_respuesta(i, "ABCD".index(k_)), 31, VERDE, 4)
        dni = str(h.get("dni", ""))
        for k, ch in enumerate(dni[:8]):
            if ch.isdigit():
                disco(omr.DNI_X[k], omr.CAB_Y0 + int(ch) * omr.CAB_DY, 11, TINTA)
        if grupo in omr.OPCIONES and not sim.get("sin_area"):
            disco(omr.GRUPO_X[omr.OPCIONES.index(grupo)], omr.GRUPO_Y, 20, TINTA)
        # franja inferior con la nota
        c.setFillColor(colors.white)
        c.rect(X(164), Y(3332), X(2153), X(113), stroke=0, fill=1)
        nombre = h.get("nombre") or ""
        if (not nombre) and h.get("nombre_img"):
            try:
                c.drawImage(ImageReader(io.BytesIO(base64.b64decode(h["nombre_img"]))), X(190), Y(3274), X(1250), X(50),
                            preserveAspectRatio=True, anchor="sw")
            except Exception:
                pass
        else:
            txt(_latin(nombre or "SIN NOMBRE", 60).upper(), 190, 3262, 36, 1250)
        pto, tot = puestos.get(hid, ("-", "-"))
        mx = puntaje_maximo(sim, grupo)
        txt(f"DNI {dni or '-'}", 1480, 3262, 28, 800)
        txt(f"PUNTAJE {res['puntaje']:g}/{mx:g}   NOTA {res['nota']:.2f}   PUESTO {pto} de {tot}", 190, 3302, 26, 1950,
            VERDE if res["nota"] >= 10.5 else ROJO)
        det = "  |  ".join(f"{cn[:16]} {cv['correctas']}/{cv['correctas'] + cv['incorrectas'] + cv['blancos']}"
                           for cn, cv in res["cursos"].items())
        txt(_latin(det, 220), 190, 3326, 16, 1950, colors.Color(.3, .3, .3))
        c.showPage()
    c.save()
    return buf.getvalue()


def _num_wa(cel):
    n = re.sub(r"\D", "", str(cel or ""))
    if len(n) == 9:
        n = "51" + n
    return n if len(n) >= 11 else ""


def mensaje_whatsapp(sim, fila, hoja, total):
    res = calificar(sim, hoja)
    lineas = [f"*I.E.P. ALTERNATIVO YACHAY*", f"*{sim['titulo']}* ({sim.get('fecha', '')})", "",
              f"Alumno: {fila['Apellidos y Nombres']}",
              f"Puntaje: {fila['Puntaje']:g}/{puntaje_maximo(sim, hoja.get('grupo', '')):g}  |  Nota: {fila['Nota']:.2f}/20",
              f"Puesto: {int(fila['Puesto'])} de {total}", ""]
    for cn, cv in res["cursos"].items():
        lineas.append(f"• {cn}: {cv['nota']:.1f}/20 ({cv['correctas']} correctas)")
    lineas += ["", "Gracias por su apoyo. 📚"]
    return "\n".join(lineas)


def boton_hoja(sim, key, etiqueta=None):
    """Botón de descarga de la hoja (con QR si hay simulacro guardado)."""
    try:
        ck = ("pdf", (sim or {}).get("id"), (sim or {}).get("titulo"), (sim or {}).get("fecha"))
        if ck not in _BASE_CACHE:
            _BASE_CACHE[ck] = hoja_pdf(sim)
        data = _BASE_CACHE[ck]
    except Exception as e:
        st.error(f"No se pudo generar la hoja: {e}")
        return
    nombre = "Hoja_Yachay_" + re.sub(r"\W+", "_", sim["titulo"]) + ".pdf" if sim else "Hoja_Yachay.pdf"
    st.download_button(etiqueta or ("🏷️ Hoja de ESTE simulacro (opcional, con QR)" if sim else
                                    "📄 Hoja genérica (para imprimir por millares)"),
                       data, nombre, "application/pdf", key=key, type="secondary" if sim else "primary")


# ================================================================
# VERIFICACIÓN DE DNI
# ================================================================
def analizar_dnis_matricula(df):
    """Detecta DNI mal escritos en la matrícula: más de 8 dígitos (celular, dígito
    verificador), menos de 8, vacíos o repetidos. Devuelve un DataFrame."""
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    col_n = "Nombre" if "Nombre" in df.columns else ("Alumno" if "Alumno" in df.columns else None)
    if "DNI" not in df.columns or not col_n:
        return pd.DataFrame()
    filas, vistos = [], {}
    for _, r in df.iterrows():
        crudo = str(r.get("DNI") or "").strip()
        if crudo.lower() in ("nan", "none"):
            crudo = ""
        dig = re.sub(r"\D", "", crudo)
        nom = str(r.get(col_n, "") or "").strip().upper()
        grado = (str(r.get("Grado", "") or "").strip() + " " + str(r.get("Seccion", "") or "").strip()).strip()
        grado = grado.replace("nan", "").strip()
        prob, sug = "", ""
        if not dig:
            prob = "Sin DNI"
        elif len(dig) == 8:
            vistos.setdefault(dig, []).append(nom)
            if crudo != dig:
                prob, sug = "Tiene espacios o símbolos", dig
        elif len(dig) < 8:
            prob, sug = f"Faltan dígitos ({len(dig)})", dig.zfill(8)
        elif len(dig) == 9 and dig[0] == "9":
            prob = "9 dígitos que empieza con 9: parece un CELULAR, no un DNI"
        elif len(dig) == 9:
            prob, sug = "9 dígitos: sobra el dígito verificador (el del guion en el DNI)", dig[:8]
        else:
            prob = f"{len(dig)} dígitos: demasiado largo (¿celular o dos números juntos?)"
        if prob:
            filas.append({"Alumno": nom, "Grado": grado, "DNI en matrícula": crudo, "Dígitos": len(dig),
                          "Problema": prob, "DNI sugerido": sug})
    for dig, noms in vistos.items():
        if len(noms) > 1:
            for nom in noms:
                filas.append({"Alumno": nom, "Grado": "", "DNI en matrícula": dig, "Dígitos": 8,
                              "Problema": f"DNI repetido en {len(noms)} alumnos", "DNI sugerido": ""})
    return pd.DataFrame(filas)


def resolver_dni(leido, mat, pref=None):
    """Cruza el DNI leído de la hoja con la matrícula.
    Devuelve dict: dni (el que se guarda), info (datos del alumno), avisos, sug (DNI sugerido)."""
    r = {"dni": leido, "info": mat.get(leido, {}), "avisos": [], "sug": None}
    if r["info"]:
        return r
    d8 = leido if re.fullmatch(r"\d{8}", leido or "") else ""
    if d8:                                    # matrícula con 9 dígitos = 8 + verificador
        largos = [k for k in mat if len(k) > 8 and k[:8] == d8]
        if len(largos) == 1:
            k = largos[0]
            r.update({"dni": k, "info": mat[k]})
            r["avisos"].append(f"En la matrícula su DNI figura como {k} ({len(k)} dígitos); "
                               "corrígelo a 8 dígitos")
            return r
    if len(leido or "") == 8:                 # 1 dígito mal leído (o ilegible '?' / '_')
        cands = []
        for k in mat:
            if len(k) < 8:
                continue
            dif = sum(1 for a, b in zip(leido, k[:8]) if a.isdigit() and a != b)
            if dif <= 1:
                cands.append((dif, 0 if (not pref or k in pref) else 1, k))
        cands.sort(key=lambda t: (t[1], t[0]))
        cands = [(t[0], t[2]) for t in cands]
        if cands and (len(cands) == 1 or cands[0][0] < cands[1][0]):
            r["sug"] = cands[0][1]
    return r


# ================================================================
# INTERFAZ
# ================================================================
def _selector_simulacro(datos, key):
    sims = datos["simulacros"]
    if not sims:
        st.info("Aún no hay simulacros. Créalo en la pestaña ⚙️ Configurar.")
        return None
    ids = sorted(sims, key=lambda i: sims[i].get("creado", ""), reverse=True)
    etiqueta = {i: f"{sims[i]['titulo']} — {etiqueta_modalidad(sims[i])} — {sims[i].get('fecha', '')} ({len(sims[i].get('hojas', {}))} hojas)"
                for i in ids}
    # Se recuerda el simulacro elegido: al cambiar de pestaña no hay que elegirlo otra vez.
    actual = st.session_state.get("simy_sid_actual")
    if actual in ids and st.session_state.get(key) != actual:
        st.session_state[key] = actual
    return st.selectbox("Simulacro:", ids, format_func=lambda i: etiqueta[i], key=key,
                        on_change=lambda: st.session_state.update(simy_sid_actual=st.session_state.get(key)))


def _html_area(g, cursos, titulo=None):
    """Tabla de un área con el mismo aspecto que el temario del examen UNSAAC."""
    filas, tot = "", 0
    for i, c in enumerate(cursos):
        n = c["hasta"] - c["desde"] + 1
        tot += n
        bg = "#f1f1f1" if i % 2 == 0 else "#ffffff"
        filas += (f"<tr style='background:{bg}'><td style='padding:5px 10px'>{_html.escape(c['nombre'])}</td>"
                  f"<td style='text-align:center'>{n}</td>"
                  f"<td style='text-align:center;color:#666'>{c['desde']}–{c['hasta']}</td></tr>")
    return (f"<table style='width:100%;border-collapse:collapse;font-size:13.5px;color:#111;background:#fff'>"
            f"<tr><th colspan=3 style='background:#9b1b2f;color:#fff;padding:7px;text-align:center'>"
            f"{titulo or 'ÁREA «' + g + '»'}</th></tr>"
            f"<tr style='background:#f4f4f4;font-weight:700;font-size:12px'><td style='padding:5px 10px'>ASIGNATURA</td>"
            f"<td style='text-align:center'>N.º DE PREGUNTAS</td><td style='text-align:center'>PREGUNTAS</td></tr>"
            f"{filas}<tr style='font-weight:800;background:#f4f4f4'><td style='padding:5px 10px'>TOTAL</td>"
            f"<td style='text-align:center'>{tot}</td><td></td></tr></table>")


def _cursos_desde_rangos(df, correcta, incorrecta):
    """Cursos escritos como «Curso | Desde | Hasta» (para Primaria, Secundaria y otros)."""
    cursos, errores, usadas = [], [], {}
    for _, r in df.iterrows():
        nom = str(r.get("Curso") or "").strip()
        if not nom or nom.lower() == "nan":
            continue
        try:
            d, h = int(r.get("Desde")), int(r.get("Hasta"))
        except Exception:
            errores.append(f"'{nom}': escribe de qué pregunta a qué pregunta va.")
            continue
        if d < 1 or h < d:
            errores.append(f"'{nom}': el «Desde» debe ser menor o igual que el «Hasta».")
            continue
        if h > 100:
            errores.append(f"'{nom}': la hoja solo tiene 100 preguntas.")
            continue
        choque = [usadas[q] for q in range(d, h + 1) if q in usadas]
        if choque:
            errores.append(f"'{nom}' se cruza con '{choque[0]}': una pregunta no puede ser de dos cursos.")
            continue
        for q in range(d, h + 1):
            usadas[q] = nom
        cursos.append({"nombre": nom, "desde": d, "hasta": h, "correcta": correcta, "incorrecta": incorrecta})
    cursos.sort(key=lambda c: c["desde"])
    return cursos, errores


def _cursos_desde_df(df, correcta, incorrecta):
    cursos, pos, errores = [], 1, []
    for _, r in df.iterrows():
        nom = str(r.get("Curso") or "").strip()
        if not nom or nom.lower() == "nan":
            continue
        try:
            k = int(r.get("Preguntas") or 0)
        except Exception:
            errores.append(f"Preguntas inválidas en '{nom}'.")
            continue
        if k <= 0:
            continue
        cursos.append({"nombre": nom, "desde": pos, "hasta": pos + k - 1,
                       "correcta": correcta, "incorrecta": incorrecta})
        pos += k
    return cursos, errores


def _bloque_final_config(datos, sim, sid, pfx):
    if sid and (not _HOOKS["puede_borrar"] or _HOOKS["puede_borrar"]()):
        with st.expander("🗑️ Eliminar simulacro"):
            if st.checkbox("Confirmo que quiero borrarlo con todas sus hojas", key=pfx + "delok"):
                if st.button("Eliminar definitivamente", key=pfx + "del"):
                    quitar_de_historial(sim)
                    datos["simulacros"].pop(sid, None)
                    guardar_datos(datos)
                    st.success("Eliminado.")
                    st.rerun()

    st.markdown("---")
    if sid:
        c_h1, c_h2 = st.columns(2)
        with c_h1:
            boton_hoja(None, pfx + "dl_hoja_gen")
            st.caption("Sirve para todos los simulacros: imprímela por millares.")
        with c_h2:
            boton_hoja(sim, pfx + "dl_hoja_cfg")
            st.caption("Solo si imprimes pocas hojas para este examen: lleva su QR, título y fecha.")
    else:
        st.caption("Guarda el simulacro y aquí aparecerá la hoja con su QR para imprimir.")


def _tab_configurar(datos):
    st.subheader("⚙️ Configurar simulacro")
    modo = st.radio("Acción:", ["➕ Nuevo simulacro", "✏️ Editar existente"], horizontal=True, key="simy_modo_cfg")
    if modo.startswith("✏️"):
        sid = _selector_simulacro(datos, "simy_sel_cfg")
        if not sid:
            return
        sim = datos["simulacros"][sid]
    else:
        sid = None
        sim = {"titulo": "Simulacro Bimestral", "fecha": datetime.now().strftime("%d/%m/%Y"),
               "periodo": "", "num_preguntas": 80, "puntaje_blanco": 0, "claves": {},
               "cursos": [], "hojas": {}}
    pfx = f"simy_{sid or 'nuevo'}_"

    c1, c2, c3 = st.columns([2, 1, 1])
    titulo = c1.text_input("Nombre del simulacro:", sim["titulo"], key=pfx + "tit")
    fecha = c2.text_input("Fecha:", sim.get("fecha", ""), key=pfx + "fec")
    periodo = c3.text_input("Periodo / Bimestre:", sim.get("periodo", ""), key=pfx + "per")

    # ---- ¿Qué se evalúa? (igual que al postular a la UNSAAC) ----
    st.markdown("#### 🎯 ¿Qué vas a evaluar?")
    opciones = list(MODALIDADES) + list(MODALIDADES_NIVEL) + [MOD_PERSONALIZADO]
    es_legacy = bool(sid and not sim.get("cursos_area"))
    if es_legacy:
        idx = len(opciones) - 1
    elif sid and sim.get("sin_area"):
        _k = sim.get("modalidad", "OTRO")
        idx = len(MODALIDADES) + (list(MODALIDADES_NIVEL.values()).index(_k) if _k in MODALIDADES_NIVEL.values() else 2)
    elif sid:
        actual = list(grupos_sim(sim))
        idx = next((k for k, (_, v) in enumerate(MODALIDADES.items()) if v == actual), 0)
    else:
        idx = 0
    bloqueado = bool(sid and sim.get("hojas"))
    eleccion = st.selectbox("Modalidad:", opciones, index=idx, key=pfx + "modalidad", disabled=bloqueado,
                            help="Preu: cada área ya trae sus cursos y su número de preguntas del temario UNSAAC; "
                                 "'Grupo AB' califica a los alumnos de las áreas A y B en un mismo ranking. "
                                 "Primaria / Secundaria: una sola prueba con los cursos del colegio.")
    if bloqueado:
        st.caption("🔒 La modalidad no se puede cambiar porque el simulacro ya tiene hojas calificadas. "
                   "Si necesitas otra, crea un simulacro nuevo.")

    if eleccion == MOD_PERSONALIZADO:
        _config_personalizado(datos, sim, sid, pfx, titulo, fecha, periodo)
    elif eleccion in MODALIDADES_NIVEL:
        k_niv = MODALIDADES_NIVEL[eleccion]
        _config_areas(datos, sim, sid, pfx, titulo, fecha, periodo, ["A"],
                      plantilla=PLANTILLAS_NIVEL[k_niv], modal=k_niv)
    else:
        _config_areas(datos, sim, sid, pfx, titulo, fecha, periodo, MODALIDADES[eleccion])
    _bloque_final_config(datos, sim, sid, pfx)


def _union_default(grupos):
    """Examen único con clave común: cursos de todas las áreas, sin repetir, en el orden del
    temario. Devuelve [(curso, n.º de preguntas, áreas que lo rinden)]."""
    orden, info = [], {}
    for g in grupos:
        prev = None
        for nom, n in PLANTILLAS_AREA[g]:
            if nom not in info:
                info[nom] = {"n": n, "g": set()}
                orden.insert(orden.index(prev) + 1 if prev in orden else len(orden), nom)
            info[nom]["g"].add(g)
            prev = nom
    return [(nom, info[nom]["n"], "".join(x for x in grupos if x in info[nom]["g"])) for nom in orden]


def _etiquetas_areas(grupos):
    """{etiqueta visible: 'CD'} para la columna «Áreas» del examen unificado."""
    todas = "".join(grupos)
    et = {f"{_unir(list(todas))} (todas)": todas}
    for g in grupos:
        et[f"Solo {g}"] = g
    return et


def _union_desde_df(df, grupos, p_ok, p_mal):
    et = _etiquetas_areas(grupos)
    cursos_area = {g: [] for g in grupos}
    union, errores, pos = [], [], 1
    for _, r in df.iterrows():
        nom = str(r.get("Curso") or "").strip()
        if not nom or nom.lower() == "nan":
            continue
        try:
            n = int(r.get("Preguntas") or 0)
        except Exception:
            errores.append(f"Preguntas inválidas en '{nom}'.")
            continue
        if n <= 0:
            continue
        a = et.get(r.get("Áreas"), "".join(grupos))
        c = {"nombre": nom, "desde": pos, "hasta": pos + n - 1, "correcta": p_ok, "incorrecta": p_mal}
        for g in grupos:
            if g in a:
                cursos_area[g].append(dict(c))
        union.append({"nombre": nom, "preguntas": n, "areas": a})
        pos += n
    return cursos_area, union, pos - 1, errores


def _unir(grupos):
    return grupos[0] if len(grupos) == 1 else ", ".join(grupos[:-1]) + " y " + grupos[-1]


def _config_areas(datos, sim, sid, pfx, titulo, fecha, periodo, grupos, plantilla=None, modal=None):
    unico = plantilla is not None            # colegio: una sola prueba, sin áreas
    mk = modal or "".join(grupos)            # evita mezclar lo escrito al cambiar de modalidad
    prev = sim.get("cursos_area") or {}
    pc = next((c for c in sim.get("cursos", []) if prev), None) if prev else None
    st.markdown("#### 🧮 Puntaje")
    p1, p2, p3 = st.columns(3)
    p_ok = p1.number_input("Por respuesta correcta:", -100.0, 100.0, float(pc["correcta"]) if pc else 1.0,
                           0.25, key=pfx + "p_ok")
    p_mal = p2.number_input("Por respuesta incorrecta:", -100.0, 100.0, float(pc["incorrecta"]) if pc else 0.0,
                            0.25, key=pfx + "p_mal")
    p_bl = p3.number_input("Por pregunta en blanco:", -100.0, 100.0, float(sim.get("puntaje_blanco", 0)),
                           0.25, key=pfx + "p_bl")
    st.caption("Estos puntajes valen para todos los cursos. La nota /20 se calcula sobre el puntaje máximo.")

    st.markdown("#### 📚 Cursos y clave" if unico else "#### 📚 Cursos y claves por área")
    if unico:
        st.caption("Los cursos son los del sistema para este nivel; cambia el n.º de preguntas de cada uno, agrega o borra "
                   "filas. Los rangos de preguntas se calculan solos. Usa la letra E en la clave para anular una pregunta.")
    else:
        st.caption("Los cursos ya vienen del temario oficial. Si el simulacro tiene menos preguntas de algún curso, "
                   "solo cambia el número: los rangos de preguntas se calculan solos. "
                   "Usa la letra E en la clave para anular una pregunta.")

    # ---- ¿una sola clave para todas las áreas del grupo? ----
    compartida = False
    if len(grupos) == 2:
        previas = [sim.get("claves", {}).get(g, "") for g in grupos]
        ya_igual = bool(sid) and all(previas) and len(set(previas)) == 1
        compartida = st.checkbox(f"🔑 La clave de respuestas es la MISMA para las áreas {_unir(grupos)}",
                                 value=True if not sid else (ya_igual and bool(sim.get("cursos_union"))),
                                 key=pfx + "misma_clave",
                                 help="Márcalo si las áreas rinden UN SOLO examen con una sola clave: los cursos que "
                                      "no comparten (por ejemplo Economía y Filosofía) se suman como preguntas extra y "
                                      "cada área se califica solo sobre sus propias preguntas. "
                                      "Desmárcalo si cada área tiene su propia clave.")

    todos = False
    if compartida:
        todas_ar = "".join(grupos)
        ya_todos = bool(sim.get("cursos_union")) and all(u["areas"] == todas_ar for u in sim["cursos_union"])
        extra_n = {"AB": "Geometría y Trigonometría y Biología", "CD": "Economía y Filosofía y Lógica"}.get(todas_ar, "los cursos de cada área")
        todos = st.checkbox(f"👥 TODOS los alumnos rinden TODOS los cursos ({extra_n}, los dos)",
                            value=True if not sid else ya_todos, key=pfx + "todos_cursos",
                            help="Marcado: cada alumno, sea del área que sea, se califica sobre todas las preguntas del examen y "
                                 "no hace falta que marque bien su área. Desmarcado: cada área se califica solo sobre sus "
                                 "propios cursos (80 preguntas).")

    claves, cursos_area, errores = {}, {}, []

    def _bloque_clave(suf, rotulo, n_ref, inicial):
        kk = pfx + f"clave_{mk}_{suf}"
        if kk + "_pend" in st.session_state:
            st.session_state[kk] = st.session_state.pop(kk + "_pend")
        kw = {} if kk in st.session_state else {"value": inicial}
        st.markdown(f"**{rotulo}**  ·  {n_ref} preguntas")
        txt = st.text_area("Pega la clave (ABCD… seguida, con espacios o numerada 1A 2B…):",
                           height=90, key=kk, **kw)
        k = limpiar_clave(txt, n_ref or 100)
        if k:
            (st.success if len(k) == n_ref else st.warning)(f"{len(k)} de {n_ref} respuestas leídas.")
            st.code("  ".join(k[i:i + 10] for i in range(0, len(k), 10)), language=None)
        else:
            errores.append("Falta la clave de respuestas." if (unico or suf == "comun") else f"Falta la clave del Área {suf}.")
        with st.expander("📸 Leer esta clave desde una hoja rellenada"):
            st.caption("Rellena una hoja Yachay con las respuestas correctas, tómale foto y súbela.")
            fk = st.file_uploader("Hoja clave:", type=["jpg", "jpeg", "png", "pdf"], key=pfx + f"fk_{mk}_{suf}")
            if fk is not None and st.button("Leer clave", key=pfx + f"lk_{mk}_{suf}"):
                imgs = omr.imagenes_desde_archivo(fk.name, fk.getvalue())
                if imgs:
                    r = omr.leer_hoja(imgs[0], n_ref or 80)
                    leida = "".join(x if x in "ABCD" else "E" for x in r["respuestas"])
                    st.session_state[kk + "_pend"] = leida
                    st.success("Clave leída. Revisa: las preguntas sin marca quedaron como E (anuladas).")
                    st.rerun()
        return k

    def _bloque_area(g):
        nom = "los cursos" if unico else f"el Área {g}"
        guardado = prev.get(g)
        rk = pfx + f"rst_{mk}_{g}"
        ver = st.session_state.get(rk, 0)
        if unico:
            if guardado and ver == 0:
                base = [(c["nombre"], c["desde"], c["hasta"]) for c in guardado]
            else:
                base, pos = [], 1
                for nm_, n_ in plantilla:
                    base.append((nm_, pos, pos + n_ - 1))
                    pos += n_
        elif guardado and ver == 0:
            base = [(c["nombre"], c["hasta"] - c["desde"] + 1) for c in guardado]
        else:
            base = PLANTILLAS_AREA[g]
        ca, cb = st.columns([1.2, 1])
        with ca:
            if unico:
                st.markdown("**1️⃣ Cursos: escribe de qué pregunta a qué pregunta va cada uno**")
                st.caption("Agrega todos los cursos que necesites con el **+** al final de la tabla.")
                df = pd.DataFrame(base, columns=["Curso", "Desde", "Hasta"])
                cfg_cur = {"Desde": st.column_config.NumberColumn(min_value=1, max_value=100, step=1),
                           "Hasta": st.column_config.NumberColumn(min_value=1, max_value=100, step=1)}
            else:
                st.markdown("**1️⃣ Cursos y n.º de preguntas**")
                df = pd.DataFrame(base, columns=["Curso", "Preguntas"])
                cfg_cur = {"Preguntas": st.column_config.NumberColumn(min_value=1, max_value=100, step=1)}
            df_e = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True,
                                  key=pfx + f"cur_{mk}_{g}_{ver}", column_config=cfg_cur)
            if st.button("↩️ Restaurar cursos originales" if unico else "↩️ Restaurar temario oficial",
                         key=pfx + f"rstb_{mk}_{g}"):
                st.session_state[rk] = ver + 1
                st.rerun()
        if unico:
            cursos_g, err_g = _cursos_desde_rangos(df_e, float(p_ok), float(p_mal))
        else:
            cursos_g, err_g = _cursos_desde_df(df_e, float(p_ok), float(p_mal))
        pre = "" if unico else f"Área {g}: "
        errores.extend(pre + e for e in err_g)
        with cb:
            st.markdown(_html_area(g, cursos_g, "CURSOS DEL SIMULACRO" if unico else None), unsafe_allow_html=True)
        cursos_area[g] = cursos_g
        n_g = max((c["hasta"] for c in cursos_g), default=0)
        if not cursos_g:
            errores.append(pre + "no tiene cursos.")
        if n_g > 100:
            errores.append(pre + f"tiene {n_g} preguntas y la hoja solo admite 100.")
        if len({c["nombre"] for c in cursos_g}) != len(cursos_g):
            errores.append(pre + "hay cursos con el mismo nombre.")
        if not compartida:
            claves[g] = _bloque_clave(g, "2️⃣ Clave de respuestas" if unico else f"2️⃣ Clave de respuestas del Área {g}",
                                      n_g, sim.get("claves", {}).get(g, ""))

    union_guardar = None
    if unico:
        _bloque_area(grupos[0])
    elif compartida:
        # Un solo examen: cursos de todas las áreas; cada área rinde los suyos.
        et = _etiquetas_areas(grupos)
        inv = {v: k for k, v in et.items()}
        rk = pfx + f"rst_uni_{mk}"
        ver = st.session_state.get(rk, 0)
        if sim.get("cursos_union") and ver == 0:
            base = [(u["nombre"], u["preguntas"], inv.get(u["areas"], list(et)[0])) for u in sim["cursos_union"]]
        else:
            base = [(n, q, inv[a]) for n, q, a in _union_default(grupos)]
        st.markdown("**1️⃣ Cursos del examen**" + ("" if todos else " (la columna «Áreas» dice quién rinde cada curso)"))
        ca, cb = st.columns([1.15, 1])
        with ca:
            if todos:
                df_u = pd.DataFrame([(n, q) for n, q, _a in base], columns=["Curso", "Preguntas"])
                cfg = {"Preguntas": st.column_config.NumberColumn(min_value=1, max_value=100, step=1)}
            else:
                df_u = pd.DataFrame(base, columns=["Curso", "Preguntas", "Áreas"])
                cfg = {"Preguntas": st.column_config.NumberColumn(min_value=1, max_value=100, step=1),
                       "Áreas": st.column_config.SelectboxColumn("Áreas", options=list(et), required=False)}
            df_ue = st.data_editor(df_u, num_rows="dynamic", use_container_width=True, hide_index=True,
                                   key=pfx + f"uni_{mk}_{ver}_{int(todos)}", column_config=cfg)
            if st.button("↩️ Restaurar temario oficial", key=pfx + f"rstb_uni_{mk}"):
                st.session_state[rk] = ver + 1
                st.rerun()
        cursos_area, union_guardar, n_total, err_u = _union_desde_df(df_ue, grupos, float(p_ok), float(p_mal))
        errores.extend(err_u)
        with cb:
            for g in grupos:
                st.markdown(_html_area(g, cursos_area[g]), unsafe_allow_html=True)
                st.write("")
        tot = {g: sum(c["hasta"] - c["desde"] + 1 for c in cursos_area[g]) for g in grupos}
        if todos:
            st.info(f"📄 El examen tiene **{n_total} preguntas** y **todos los alumnos se califican sobre las {n_total}**, "
                    "sin importar el área que marquen.")
        else:
            st.info(f"📄 El examen tiene **{n_total} preguntas** en total. "
                    + " · ".join(f"Área {g}: {tot[g]} preguntas" for g in grupos)
                    + ". Cada área se califica solo sobre las suyas.")
        if n_total > 100:
            errores.append(f"El examen tiene {n_total} preguntas y la hoja solo admite 100.")
        for g in grupos:
            if not cursos_area[g]:
                errores.append(f"Área {g}: no tiene cursos (revisa la columna «Áreas»).")
            if len({c["nombre"] for c in cursos_area[g]}) != len(cursos_area[g]):
                errores.append(f"Área {g}: hay cursos con el mismo nombre.")
        st.markdown("---")
        ini = next((sim.get("claves", {}).get(g) for g in grupos if sim.get("claves", {}).get(g)), "")
        k = _bloque_clave("comun", f"2️⃣ 🔑 Clave de respuestas (la misma para las áreas {_unir(grupos)})",
                          n_total, ini)
        for g in grupos:
            claves[g] = k
    else:
        for g, tg in zip(grupos, st.tabs([f"Área {g}" for g in grupos])):
            with tg:
                _bloque_area(g)

    for e in errores:
        st.error(e)
    if st.button("💾 Guardar simulacro", type="primary", disabled=bool(errores), key=pfx + "save"):
        nuevo = dict(sim)
        n_max = max(c["hasta"] for cs_ in cursos_area.values() for c in cs_)
        nuevo.update({"titulo": titulo.strip() or "Simulacro", "fecha": fecha, "periodo": periodo,
                      "num_preguntas": int(n_max), "puntaje_blanco": p_bl,
                      "claves": {g: claves.get(g, "") for g in grupos},
                      "grupos": list(grupos), "cursos_area": cursos_area,
                      "cursos": cursos_area[grupos[0]], "modalidad": mk, "clave_comun": bool(compartida)})
        if compartida and union_guardar:
            nuevo["cursos_union"] = union_guardar
            nuevo["todos_cursos"] = bool(todos)
        else:
            nuevo.pop("cursos_union", None)
            nuevo.pop("todos_cursos", None)
        if unico:
            nuevo["sin_area"] = True
        else:
            nuevo.pop("sin_area", None)
        if not sid:
            sid = datetime.now().strftime("%Y%m%d") + "_" + uuid.uuid4().hex[:5]
            nuevo.update({"id": sid, "creado": datetime.now().isoformat(),
                          "creado_por": st.session_state.get("usuario_actual", ""), "hojas": {}})
        datos["simulacros"][sid] = nuevo
        guardar_datos(datos)
        if nuevo.get("publicado"):
            publicar_en_historial(nuevo)       # mantener el historial al día
        mx = f"{puntaje_maximo(nuevo, grupos[0]):g}" if unico else " · ".join(
            f"Área {g}: {puntaje_maximo(nuevo, g):g}" for g in grupos)
        st.success(f"Simulacro guardado. Puntaje máximo → {mx}. Ya puedes ir a 📸 Escanear.")


def _config_personalizado(datos, sim, sid, pfx, titulo, fecha, periodo):
    if not sim.get("cursos"):
        sim = dict(sim)
        sim["num_preguntas"] = 100
        sim["cursos"] = [{"nombre": n, "desde": a, "hasta": b, "correcta": 1.0, "incorrecta": 0.0}
                         for n, a, b in CURSOS_EJEMPLO]
    st.caption("Modo libre: tú defines los cursos y los rangos de preguntas (un solo esquema para todos los grupos).")
    c4, c5 = st.columns(2)
    n = c4.number_input("N.º de preguntas:", 1, 100, int(sim.get("num_preguntas", 100)), key=pfx + "n")
    p_bl = c5.number_input("Puntaje por pregunta en blanco:", -10.0, 10.0,
                           float(sim.get("puntaje_blanco", 0)), 0.25, key=pfx + "bl")

    st.markdown("#### 📚 Cursos por rango de preguntas")
    st.caption("Indica de qué pregunta a qué pregunta va cada curso y cuánto vale cada correcta e "
               "incorrecta (ej.: correcta 4, incorrecta -1). Puedes agregar o borrar filas.")
    df_c = pd.DataFrame([{"Curso": c["nombre"], "Desde": c["desde"], "Hasta": c["hasta"],
                          "Correcta": c["correcta"], "Incorrecta": c["incorrecta"]} for c in sim["cursos"]])
    df_c = st.data_editor(df_c, num_rows="dynamic", use_container_width=True, key=pfx + "cursos",
                          column_config={
                              "Desde": st.column_config.NumberColumn(min_value=1, max_value=100, step=1),
                              "Hasta": st.column_config.NumberColumn(min_value=1, max_value=100, step=1),
                              "Correcta": st.column_config.NumberColumn(step=0.25, format="%.2f"),
                              "Incorrecta": st.column_config.NumberColumn(step=0.25, format="%.2f")})

    st.markdown("#### 🔑 Claves de respuestas")
    st.caption("Escribe la clave seguida (ABCDABCD…), con espacios, o numerada (1A 2B 3C…). "
               "Si todos los grupos tienen la misma prueba, llena solo el Grupo A. "
               "Usa la letra E para anular una pregunta (no se califica).")
    claves = {}
    tabs_g = st.tabs([f"Grupo {g}" for g in GRUPOS])
    for g, tg in zip(GRUPOS, tabs_g):
        with tg:
            kk = pfx + "clave_" + g
            if kk + "_pend" in st.session_state:
                st.session_state[kk] = st.session_state.pop(kk + "_pend")
            kw = {} if kk in st.session_state else {"value": sim.get("claves", {}).get(g, "")}
            txt = st.text_area(f"Clave del grupo {g}:", height=90, key=kk, **kw)
            k = limpiar_clave(txt, int(n))
            claves[g] = k
            if k:
                (st.success if len(k) == n else st.warning)(f"{len(k)} de {int(n)} respuestas leídas.")
                st.code("  ".join(k[i:i + 10] for i in range(0, len(k), 10)), language=None)
            with st.expander("📸 Leer esta clave desde una hoja rellenada"):
                st.caption("Rellena una hoja Yachay con las respuestas correctas, tómale foto y súbela.")
                fk = st.file_uploader("Hoja clave:", type=["jpg", "jpeg", "png", "pdf"], key=pfx + "fk_" + g)
                if fk is not None and st.button("Leer clave", key=pfx + "lk_" + g):
                    imgs = omr.imagenes_desde_archivo(fk.name, fk.getvalue())
                    if imgs:
                        r = omr.leer_hoja(imgs[0], int(n))
                        leida = "".join(x if x in "ABCD" else "E" for x in r["respuestas"])
                        st.session_state[kk + "_pend"] = leida
                        st.success("Clave leída. Revisa: las preguntas sin marca quedaron como E (anuladas).")
                        st.rerun()

    errores = []
    cursos = []
    for _, r in df_c.dropna(subset=["Curso"]).iterrows():
        try:
            cursos.append({"nombre": str(r["Curso"]).strip(), "desde": int(r["Desde"]),
                           "hasta": int(r["Hasta"]), "correcta": float(r["Correcta"] or 0),
                           "incorrecta": float(r["Incorrecta"] or 0)})
        except Exception:
            errores.append(f"Fila incompleta: {r['Curso']}")
    usadas = {}
    for c in cursos:
        if c["desde"] > c["hasta"]:
            errores.append(f"{c['nombre']}: 'Desde' es mayor que 'Hasta'.")
        if c["hasta"] > n:
            errores.append(f"{c['nombre']}: llega a la pregunta {c['hasta']} pero el examen tiene {int(n)}.")
        for q in range(c["desde"], c["hasta"] + 1):
            if q in usadas:
                errores.append(f"Pregunta {q} está en '{usadas[q]}' y en '{c['nombre']}'.")
                break
            usadas[q] = c["nombre"]
    if len({c["nombre"] for c in cursos}) != len(cursos):
        errores.append("Hay cursos con el mismo nombre.")
    sin_curso = [q for q in range(1, int(n) + 1) if q not in usadas]
    if sin_curso:
        st.warning(f"Preguntas sin curso asignado (no se califican): {sin_curso[:15]}"
                   f"{' …' if len(sin_curso) > 15 else ''}")
    if not any(claves.values()):
        errores.append("Falta al menos una clave (Grupo A).")
    for e in errores:
        st.error(e)

    if st.button("💾 Guardar simulacro", type="primary", disabled=bool(errores), key=pfx + "save"):
        nuevo = dict(sim)
        nuevo.update({"titulo": titulo.strip() or "Simulacro", "fecha": fecha, "periodo": periodo,
                      "num_preguntas": int(n), "puntaje_blanco": p_bl, "claves": claves, "cursos": cursos,
                      "modalidad": "PERSONALIZADO"})
        nuevo.pop("cursos_area", None)
        nuevo.pop("grupos", None)
        if not sid:
            sid = datetime.now().strftime("%Y%m%d") + "_" + uuid.uuid4().hex[:5]
            nuevo.update({"id": sid, "creado": datetime.now().isoformat(),
                          "creado_por": st.session_state.get("usuario_actual", ""), "hojas": {}})
        datos["simulacros"][sid] = nuevo
        guardar_datos(datos)
        if nuevo.get("publicado"):
            publicar_en_historial(nuevo)       # mantener el historial al día
        st.success(f"Simulacro guardado. Puntaje máximo: {puntaje_maximo(nuevo):g}")



def _area_por_respuestas(sim, resp):
    """En un examen unificado (AB o CD con clave única) cada área tiene cursos propios
    (Economía vs Filosofía, Geometría vs Biología). Si el alumno respondió los de un área y dejó
    en blanco los de la otra, ese es su área. Devuelve (área o None, {área: proporción respondida})."""
    gs = grupos_sim(sim)
    if sim.get("sin_area") or not sim.get("cursos_area") or len(gs) < 2:
        return None, {}
    val = {g: preguntas_validas(sim, g) for g in gs}
    excl = {}
    for g in gs:
        otros = set()
        for o in gs:
            if o != g:
                otros |= val[o]
        excl[g] = val[g] - otros
        if not excl[g]:
            return None, {}                  # no hay preguntas exclusivas: no se puede deducir
    share = {g: sum(1 for q in excl[g] if q - 1 < len(resp) and resp[q - 1] in ("A", "B", "C", "D", "*")) / len(excl[g])
             for g in gs}
    best = max(share, key=share.get)
    if share[best] >= 0.5 and all(share[g] <= 0.2 for g in gs if g != best):
        return best, share
    return None, share


def _areas_previas(datos, sim):
    """{dni: área} según simulacros anteriores con las mismas áreas (la más reciente gana)."""
    gs = set(grupos_sim(sim))
    out = {}
    otros = sorted((x for x in datos.get("simulacros", {}).values() if x.get("id") != sim.get("id")),
                   key=lambda x: str(x.get("creado", "")))
    for x in otros:
        for h in x.get("hojas", {}).values():
            d, g = norm_dni(h.get("dni")), h.get("grupo")
            if d and g in gs:
                out[d] = g
    return out


def _aula_de(info):
    """Grado/aula del alumno según la matrícula (la hoja ya no trae el campo Aula).
    Ej.: 'GRUPO AB', '5° Primaria A', '3° Secundaria B'."""
    if not info:
        return ""
    g = str(info.get("grado0") or info.get("grado") or "").split("—")[0].strip()
    se = str(info.get("seccion") or "").strip()
    if se and se.lower() not in ("única", "unica"):
        g = f"{g} {se}".strip()
    return g


def _fecha_tupla(txt):
    m = re.search(r"(\d{1,2})\D+(\d{1,2})\D+(\d{4})", str(txt or ""))
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def _procesar_imagen(sim, img, mat, origen, previas=None):
    r = omr.leer_hoja(img, sim["num_preguntas"])
    resp = "".join({"": "_"}.get(x, x) for x in r["respuestas"])
    dni_leido = r["dni"]
    _an = _lista_auto_nombre(sim)
    _del_grupo = set(_alumnos_de_lista(mat, "auto", sim)) if _an else set()
    rr = resolver_dni(dni_leido, mat, _del_grupo)
    dni, info = rr["dni"], rr["info"]
    grupo = r["grupo"]
    gs = grupos_sim(sim)
    alertas = list(r["alertas"]) + rr["avisos"]
    if sim.get("sin_area"):
        grupo = gs[0]                         # colegio: se ignora el casillero de grupo de la hoja
    elif sim.get("cursos_area"):
        ded, _share = _area_por_respuestas(sim, resp)
        if sim.get("todos_cursos"):
            pass                              # todos se califican igual: el área solo sirve para el filtro del ranking
        elif not grupo and len(gs) == 1:
            grupo = gs[0]
        elif not grupo:
            prev = (previas or {}).get(norm_dni(dni))
            if ded:
                grupo = ded
                alertas.append(f"No marcó el área (o marcó más de una): se dedujo el Área {ded} por los cursos que "
                               "respondió. Verifícala")
            elif prev in gs:
                grupo = prev
                alertas.append(f"No marcó el área: se usó el Área {prev} de un simulacro anterior. Verifícala")
            else:
                alertas.append("No se leyó el ÁREA (marcó más de una o ninguna): elígela en la tabla")
        elif grupo not in gs:
            alertas.append(f"El área {grupo} no pertenece a este simulacro ({', '.join(gs)})")
        elif ded and ded != grupo:
            alertas.append(f"⚠️ Marcó el Área {grupo}, pero respondió los cursos del Área {ded}: "
                           "¿se equivocó de área? Corrígela en la tabla")

    # ---- ¿Es la hoja de ESTE simulacro? (QR; si no hay QR, se compara la fecha marcada) ----
    otro_sim = False
    qr = (r.get("qr") or "").strip()
    if qr.startswith(omr.QR_PREFIJO):
        sid_q = qr[len(omr.QR_PREFIJO):].strip()
        if sid_q != sim.get("id"):
            otro_sim = True
            ot = cargar_datos()["simulacros"].get(sid_q)
            alertas.insert(0, "⛔ HOJA DE OTRO SIMULACRO: " +
                           (f"'{ot['titulo']}' ({ot.get('fecha', '')})" if ot else f"código {sid_q}") +
                           " — no corresponde al seleccionado")
    else:                                      # hoja genérica: se verifica con la fecha marcada
        ft_hoja = (r.get("dia"), r.get("mes"), r.get("anio"))
        ft_sim = _fecha_tupla(sim.get("fecha"))
        if None not in ft_hoja and ft_sim and tuple(ft_hoja) != ft_sim:
            alertas.append(f"La fecha marcada en la hoja ({ft_hoja[0]:02d}/{ft_hoja[1]:02d}/{ft_hoja[2]}) "
                           f"no coincide con la del simulacro ({sim.get('fecha')}): ¿es de otro examen?")

    sug = rr["sug"]
    if info and _del_grupo and rr["dni"] not in _del_grupo:
        alertas.append(f"Este alumno es de otro grupo ({_aula_de(info) or info.get('grado', '')}), "
                       f"no de {_an}: verifica")
    if not info:
        alertas.append("DNI no encontrado en matrícula" if re.fullmatch(r"\d{8}", dni_leido or "")
                       else "Sin DNI válido: escribe el nombre mirando la imagen «Nombre escrito»")
        if sug:
            alertas.append(f"¿Será {mat[sug]['nombre']} (DNI {sug})? Usa «Aceptar sugerencias» si es correcto")
    clave = clave_para(sim, grupo)
    validas = preguntas_validas(sim, grupo) if sim.get("cursos_area") and grupo else None
    if validas is not None:               # preguntas de otras áreas: no se pintan ni se marcan como dudosas
        clave = "".join(k if (i + 1) in validas else "E" for i, k in enumerate(clave))
    return {"tmp_id": uuid.uuid4().hex[:8], "dni": dni, "nombre": info.get("nombre", ""),
            "grado": info.get("grado", ""), "aula": _aula_de(info), "grupo": grupo,
            "respuestas": resp, "dudosas": [i + 1 for i, e in enumerate(r["estados"])
                        if e in ("duda", "doble") and (validas is None or (i + 1) in validas)],
            "alertas": alertas, "otro_sim": otro_sim, "sug_dni": sug if not info else None,
            "dni_leido": dni_leido,
            "origen": origen, "fecha_examen": f"{r['dia'] or ''}/{r['mes'] or ''}/{r['anio'] or ''}",
            "nombre_img": (base64.b64encode(omr.recorte_nombre(r)).decode() if (not info and omr.recorte_nombre(r)) else ""),
            "img": omr.imagen_revision(r, clave, nombre=info.get("nombre", ""))}


def _guardar_lote(datos, sid, lote):
    sim = datos["simulacros"][sid]
    sim.setdefault("hojas", {})
    por_dni = {h.get("dni"): k for k, h in sim["hojas"].items()}
    nuevos = reemplazados = 0
    for h in lote:
        dni = norm_dni(h["dni"]) if re.fullmatch(r"\d{1,8}", str(h["dni"])) else str(h["dni"])
        hid = por_dni.get(dni) if re.fullmatch(r"\d{8,9}", dni) else None
        if hid:
            reemplazados += 1
        else:
            hid = uuid.uuid4().hex[:10]
            nuevos += 1
        nombre_h = (h.get("nombre") or "").strip().upper()
        sim["hojas"][hid] = {"dni": dni, "nombre": nombre_h,
                             "nombre_img": "" if nombre_h else h.get("nombre_img", ""),
                             "grado": h.get("grado", ""), "aula": h.get("aula", ""),
                             "grupo": h.get("grupo") or (grupos_sim(sim)[0] if sim.get("cursos_area") and len(grupos_sim(sim)) == 1 else ""),
                             "respuestas": h["respuestas"],
                             "origen": h.get("origen", ""), "leido": datetime.now().isoformat()}
    guardar_datos(datos)
    if sim.get("publicado"):
        publicar_en_historial(sim)
    return nuevos, reemplazados


def _tab_escanear(datos):
    st.subheader("📸 Escanear hojas de respuestas")
    sid = _selector_simulacro(datos, "simy_sel_scan")
    if not sid:
        return
    sim = datos["simulacros"][sid]
    if not omr.HAS_CV2:
        st.error("Falta OpenCV en el servidor (opencv-python-headless).")
        return
    mat = _matricula()
    lote_key = f"simy_lote_{sid}"
    st.session_state.setdefault(lote_key, [])
    ver_key = f"simy_ver_{sid}"
    st.session_state.setdefault(ver_key, 0)

    # ---- Avance de la lista de control (siempre a la vista) ----
    if mat:
        _an = _lista_auto_nombre(sim)
        _al = _alumnos_de_lista(mat, "auto", sim) if _an else {}
        if not _al:
            _al, _an = dict(mat), None
        _r = _resumen_control(_tabla_control(sim, mat, st.session_state[lote_key], _al))
        if _r["total"]:
            _txt = (f"📋 **Lista — {_an or 'toda la matrícula'}:** "
                    f"✅ {_r['ok']} registrados de {_r['total']} · ⏳ faltan {_r['falta'] + _r['lote']}")
            if _r["falto"]:
                _txt += f" · 🚫 {_r['falto']} faltaron"
            st.markdown(_txt + "  \n_Mira quiénes faltan en la pestaña **📋 Lista de control**._")
            st.progress(min(1.0, (_r["ok"] + _r["falto"]) / _r["total"]))

    # ---- Antes de escanear: hojas del simulacro y verificación de DNI ----
    b_h, b_v = st.columns(2)
    with b_h:
        boton_hoja(None, "simy_dl_hoja_scan")
        st.caption("Hoja genérica para imprimir. El sistema comprueba la fecha que el alumno marca "
                   "para avisarte si una hoja es de otro examen.")
    try:
        df_prob = analizar_dnis_matricula(_HOOKS["cargar_matricula"]() if _HOOKS["cargar_matricula"] else None)
    except Exception:
        df_prob = pd.DataFrame()
    with b_v:
        if len(df_prob):
            st.warning(f"⚠️ {df_prob['Alumno'].nunique()} alumno(s) con DNI mal escrito en la matrícula "
                       "(no se podrán reconocer solos al escanear).")
        else:
            st.success("✅ Todos los DNI de la matrícula tienen 8 dígitos.")
    if len(df_prob):
        with st.expander("🔎 Ver y corregir los DNI de la matrícula", expanded=False):
            st.caption("El DNI tiene 8 dígitos; la hoja lee exactamente 8. El noveno número que aparece junto al DNI "
                       "(después del guion) es el dígito verificador y NO va. Los que empiezan con 9 y tienen 9 dígitos "
                       "suelen ser celulares. Corrígelos en Matrícula; aquí tienes la lista para hacerlo rápido.")
            st.dataframe(df_prob, use_container_width=True, hide_index=True)
            buf_x = io.BytesIO()
            df_prob.to_excel(buf_x, index=False)
            st.download_button("📊 Descargar lista (Excel)", buf_x.getvalue(), "DNI_a_corregir.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               key="simy_dl_dni_prob")

    fuente = st.radio("¿Cómo vas a cargar las hojas?",
                      ["📁 Varias fotos o PDF escaneado (lote)", "📷 Cámara (hoja por hoja)", "⌨️ Digitar a mano"],
                      horizontal=True, key="simy_fuente")
    st.caption("Consejo: foto de frente, con buena luz, que se vean los 4 cuadrados negros de las esquinas.")

    if fuente.startswith("📁"):
        archivos = st.file_uploader("Sube las hojas (JPG, PNG o PDF con varias páginas):",
                                    type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True,
                                    key=f"simy_up_{sid}")
        if archivos:
            st.caption("💡 Para muchas hojas: escanea todo en **un solo PDF** (en escala de grises, 200 dpi) "
                       "y súbelo aquí. Lo ideal son lotes de hasta 100-150 hojas por PDF.")
        if archivos and st.button("🔍 Leer hojas", type="primary", key="simy_leer"):
            barra = st.progress(0.0, "Leyendo…")
            previas = _areas_previas(datos, sim)
            total = sum(omr.contar_paginas(a.name, a.getvalue()) for a in archivos)
            hechas, fallos = 0, []
            for a in archivos:
                es_pdf = a.name.lower().endswith(".pdf")
                try:
                    for p, img in enumerate(omr.iterar_imagenes(a.name, a.getvalue())):
                        org = f"{a.name}" + (f" pág.{p + 1}" if es_pdf else "")
                        try:
                            st.session_state[lote_key].append(_procesar_imagen(sim, img, mat, org, previas))
                        except Exception as e:                 # una página dañada no detiene el lote
                            fallos.append(f"{org}: no se pudo leer ({e})")
                        del img
                        hechas += 1
                        barra.progress(min(hechas / max(total, 1), 1.0), f"Hoja {hechas} de {total}")
                except Exception as e:
                    fallos.append(f"{a.name}: {e}")
            # las hojas con problemas van primero, para revisarlas sin buscar
            st.session_state[lote_key].sort(key=lambda h: 0 if (h["alertas"] or h["dudosas"]) else 1)
            st.session_state["simy_fallos"] = fallos
            st.rerun()

    elif fuente.startswith("📷"):
        foto = st.camera_input("Toma la foto de la hoja", key=f"simy_cam_{sid}")
        if foto is not None and st.button("➕ Leer y agregar al lote", type="primary", key="simy_cam_ok"):
            img = omr.imagenes_desde_archivo("cam.jpg", foto.getvalue())[0]
            st.session_state[lote_key].append(_procesar_imagen(sim, img, mat, "cámara"))
            st.rerun()

    else:
        with st.form("simy_manual", clear_on_submit=True):
            m1, m2, m3 = st.columns([1, 2, 1])
            dni = m1.text_input("DNI:")
            nom = m2.text_input("Apellidos y nombres (si no está matriculado):")
            grp = grupos_sim(sim)[0] if sim.get("sin_area") else m3.selectbox("Área / Grupo:", [""] + grupos_sim(sim))
            txt = st.text_area("Respuestas marcadas (usa _ para blanco):", height=80)
            if st.form_submit_button("➕ Agregar al lote"):
                d = norm_dni(dni)
                resp = "".join(ch if ch in "ABCD*_" else "_" for ch in re.sub(r"[\s\d\.\)\-:]", "", txt.upper()))
                resp = resp.ljust(sim["num_preguntas"], "_")[:sim["num_preguntas"]]
                st.session_state[lote_key].append({
                    "tmp_id": uuid.uuid4().hex[:8], "dni": d, "nombre": nom.upper() or mat.get(d, {}).get("nombre", ""),
                    "grado": mat.get(d, {}).get("grado", ""), "aula": _aula_de(mat.get(d)), "grupo": grp, "respuestas": resp,
                    "dudosas": [], "alertas": [], "origen": "manual", "img": None})
                st.rerun()

    lote = st.session_state[lote_key]
    if not lote:
        return
    st.markdown("---")
    st.markdown(f"### 🧾 Revisión del lote ({len(lote)} hojas sin guardar)")
    _n_prob = sum(1 for h in lote if h["alertas"] or h["dudosas"])
    st.caption(f"✅ {len(lote) - _n_prob} sin problemas · ⚠️ {_n_prob} para revisar (aparecen primero). "
               "Revisa lo marcado y luego guarda.")
    for _f in st.session_state.get("simy_fallos", []):
        st.error(_f)

    # Tabla editable de cabeceras
    ya = {h.get("dni") for h in sim.get("hojas", {}).values()}
    cuenta = {}
    for h in lote:
        cuenta[h["dni"]] = cuenta.get(h["dni"], 0) + 1

    def _extra(h):
        e = []
        if h["dni"] and cuenta.get(h["dni"], 0) > 1 and re.fullmatch(r"\d{8,9}", h["dni"] or ""):
            e.append(f"DNI repetido en el lote ({cuenta[h['dni']]} hojas)")
        if h["dni"] in ya:
            e.append("ya tiene hoja en este simulacro (se actualizará)")
        return e
    _sa = bool(sim.get("sin_area"))
    vista = pd.DataFrame([{
        "Quitar": bool(h.get("otro_sim")), "DNI": h["dni"], "Apellidos y Nombres": h["nombre"], "Grado": h["aula"],
        "Grupo": h["grupo"], "Correctas": calificar(sim, h)["correctas"], "Puntaje": calificar(sim, h)["puntaje"],
        "Sugerencia DNI": (f"{h['sug_dni']} – {mat[h['sug_dni']]['nombre'][:28]}" if h.get("sug_dni") in mat else ""),
        "Revisar": ", ".join(h["alertas"] + _extra(h)), "Origen": h["origen"]} for h in lote])
    if _sa:
        vista = vista.drop(columns=["Grupo"])
    if any(h.get("nombre_img") and not h.get("nombre") for h in lote):
        vista.insert(2, "Nombre escrito", ["data:image/jpeg;base64," + h["nombre_img"] if (h.get("nombre_img") and not h.get("nombre")) else None for h in lote])
        st.info("✍️ Las hojas sin DNI muestran el nombre que el alumno escribió: léelo y escríbelo en «Apellidos y Nombres».")
    ed = st.data_editor(vista, use_container_width=True, hide_index=True,
                        key=f"simy_ed_{sid}_{len(lote)}_{st.session_state[ver_key]}",
                        disabled=["Correctas", "Puntaje", "Sugerencia DNI", "Revisar", "Origen", "Nombre escrito"],
                        column_config={**({} if _sa else
                                          {"Grupo": st.column_config.SelectboxColumn("Área", options=[""] + grupos_sim(sim))}),
                                       "Nombre escrito": st.column_config.ImageColumn("Nombre escrito", width="large")})
    for h, (_, fila) in zip(lote, ed.iterrows()):
        nd = str(fila["DNI"]).strip()
        if nd != h["dni"]:
            h["dni"] = nd
            if norm_dni(nd) in mat and not str(fila["Apellidos y Nombres"]).strip():
                h["nombre"] = mat[norm_dni(nd)]["nombre"]
        if str(fila["Apellidos y Nombres"]).strip() and fila["Apellidos y Nombres"] != h["nombre"]:
            h["nombre"] = str(fila["Apellidos y Nombres"]).strip().upper()
        h["aula"] = str(fila["Grado"] or "")
        if not _sa:
            h["grupo"] = str(fila["Grupo"] or "")
        h["_quitar"] = bool(fila["Quitar"])

    def _limpiar_alertas_dni(h):
        h["alertas"] = [a for a in h["alertas"] if not a.startswith(("DNI no encontrado", "¿Será"))]

    n_sug = sum(1 for h in lote if h.get("sug_dni") in mat)
    if n_sug and st.button(f"✅ Aceptar las {n_sug} sugerencia(s) de DNI (revísalas en la columna «Sugerencia DNI»)",
                           key="simy_acepta_sug"):
        for h in lote:
            k = h.get("sug_dni")
            if k in mat:
                h.update({"dni": k, "nombre": mat[k]["nombre"], "grado": mat[k]["grado"],
                          "aula": _aula_de(mat[k]), "sug_dni": None})
                _limpiar_alertas_dni(h)
        st.session_state[ver_key] += 1
        st.rerun()

    # Detalle de cada hoja (con cientos de hojas se muestran solo las que necesitan revisión)
    prob_idx = [i for i, h in enumerate(lote) if h["alertas"] or h["dudosas"]]
    modo_det = st.radio("Ver el detalle de:", [f"⚠️ Solo las que necesitan revisión ({len(prob_idx)})",
                                               f"📄 Todas ({len(lote)})"], horizontal=True, key=f"simy_detmodo_{sid}")
    idxs = prob_idx if modo_det.startswith("⚠️") else list(range(len(lote)))
    POR_PAG, pag = 20, 0
    if len(idxs) > POR_PAG:
        npag = (len(idxs) + POR_PAG - 1) // POR_PAG
        pag = int(st.number_input(f"Página del detalle (de {npag})", 1, npag, 1, key=f"simy_detpag_{sid}")) - 1
    if not idxs:
        st.success("Ninguna hoja necesita revisión. Puedes guardar el lote.")
    for i in idxs[pag * POR_PAG:(pag + 1) * POR_PAG]:
        h = lote[i]
        icono = "⚠️" if h["alertas"] or h["dudosas"] else "✅"
        with st.expander(f"{icono} {i + 1}. {h['nombre'] or '(sin nombre)'} — DNI {h['dni']} — {h['origen']}"):
            ca, cb = st.columns([1, 1])
            if h.get("img"):
                ca.image(h["img"], caption="Verde=correcta · Rojo=incorrecta · Naranja=revisar · punto verde=clave")
            with cb:
                if h["dudosas"]:
                    st.warning(f"Revisa las preguntas: {h['dudosas']}")
                for a in h["alertas"]:
                    st.caption("• " + a)
                nueva = st.text_area("Respuestas leídas (corrige si hace falta; _ = blanco, * = doble marca):",
                                     " ".join(h["respuestas"][k:k + 10] for k in range(0, len(h["respuestas"]), 10)),
                                     height=150, key=f"simy_resp_{h['tmp_id']}")
                limpio = "".join(ch for ch in nueva.upper() if ch in "ABCD*_")
                if len(limpio) == sim["num_preguntas"]:
                    h["respuestas"] = limpio
                else:
                    st.error(f"Debe haber {sim['num_preguntas']} respuestas (hay {len(limpio)}).")
                cal = calificar(sim, h)
                st.metric("Puntaje", f"{cal['puntaje']:g}", f"Nota {cal['nota']:.2f}")
                if mat and h["dni"] not in mat:
                    st.markdown("**🔗 Este DNI no está en la matrícula. Búscalo por nombre:**")
                    q = st.text_input("Apellido o nombre:", key=f"simy_bq_{h['tmp_id']}").strip().upper()
                    if q:
                        op = [k for k, v in mat.items() if q in v["nombre"]][:20]
                        if op:
                            sel = st.selectbox("Alumno:", op, format_func=lambda k: f"{mat[k]['nombre']} — {k}",
                                               key=f"simy_bs_{h['tmp_id']}")
                            if st.button("Vincular con este alumno", key=f"simy_bb_{h['tmp_id']}"):
                                h.update({"dni": sel, "nombre": mat[sel]["nombre"], "grado": mat[sel]["grado"],
                                          "aula": _aula_de(mat[sel]), "sug_dni": None})
                                _limpiar_alertas_dni(h)
                                st.session_state[ver_key] += 1
                                st.rerun()
                        else:
                            st.caption("Sin coincidencias en la matrícula.")

    b1, b2 = st.columns(2)
    if b1.button("💾 Guardar hojas en el simulacro", type="primary", key="simy_guardar_lote"):
        validos = [h for h in lote if not h.get("_quitar")]
        sin_dni = [h for h in validos if not re.fullmatch(r"\d{8,9}", norm_dni(h["dni"]) or "")]
        sin_nom = [h for h in sin_dni if not (h.get("nombre") or "").strip()]
        if sin_dni:
            st.warning(f"{len(sin_dni)} hoja(s) sin DNI válido se guardan igual"
                       + (f"; {len(sin_nom)} sin nombre escrito: en el ranking saldrá la imagen del nombre." if sin_nom else "."))
        nuevos, reemp = _guardar_lote(datos, sid, validos)
        st.session_state[lote_key] = []
        st.session_state["simy_fallos"] = []
        st.success(f"Guardado: {nuevos} hojas nuevas, {reemp} actualizadas (mismo DNI).")
    if b2.button("🗑️ Vaciar lote sin guardar", key="simy_vaciar"):
        st.session_state[lote_key] = []
        st.session_state["simy_fallos"] = []
        st.rerun()


def _tab_ranking(datos):
    st.subheader("🏆 Ranking y resultados")
    sid = _selector_simulacro(datos, "simy_sel_rank")
    if not sid:
        return
    sim = datos["simulacros"][sid]
    if not sim.get("hojas"):
        st.info("Este simulacro todavía no tiene hojas calificadas.")
        return
    aulas = sorted({h.get("aula", "") for h in sim["hojas"].values() if h.get("aula")})
    f1, f2, f3 = st.columns(3)
    fa = f1.selectbox("Grado / aula:", ["Todas"] + aulas, key="simy_fa")
    fg = "Todos" if sim.get("sin_area") else f2.selectbox("Área / Grupo:", ["Todos"] + grupos_sim(sim), key="simy_fg")
    top = f3.number_input("Top para publicar:", 3, 30, 10, key="simy_top")
    df = tabla_ranking(sim, None if fa == "Todas" else fa, None if fg == "Todos" else fg)
    if df.empty:
        st.info("No hay resultados con ese filtro.")
        return
    extra = " · ".join(x for x in [f"{fa}" if fa != "Todas" else "", f"Área {fg}" if fg != "Todos" else ""] if x) \
        or ("Ranking general " + etiqueta_modalidad(sim))

    if sim.get("cursos_area") and len(grupos_sim(sim)) > 1 and not sim.get("todos_cursos"):
        sin_area = [h for h in sim["hojas"].values() if h.get("grupo") not in grupos_sim(sim)]
        if sin_area:
            st.warning(f"{len(sin_area)} hoja(s) sin área válida (obtienen 0). Corrígelas abajo en "
                       "'Boleta de un estudiante / corregir o eliminar hoja'.")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Participantes", len(df))
    m2.metric("Puntaje promedio", f"{df['Puntaje'].mean():.2f}")
    m3.metric("Puntaje más alto", f"{df['Puntaje'].max():g}")
    m4.metric("Nota promedio /20", f"{df['Nota'].mean():.2f}")
    _vr = df.drop(columns=["ID"])
    _con_img = [bool((not sim["hojas"][i].get("nombre")) and sim["hojas"][i].get("nombre_img")) for i in df["ID"]]
    if any(_con_img):
        _vr.insert(2, "Nombre escrito", ["data:image/jpeg;base64," + sim["hojas"][i]["nombre_img"] if ok_ else None
                                         for i, ok_ in zip(df["ID"], _con_img)])
    st.dataframe(_vr, use_container_width=True, hide_index=True,
                 column_config={"Nombre escrito": st.column_config.ImageColumn("Nombre escrito", width="large")})

    st.markdown("#### 📥 Descargar / imprimir")
    d1, d2, d3, d4, d5 = st.columns(5)
    det = d1.checkbox("Incluir cursos en el PDF", True, key="simy_det")
    nombre_base = re.sub(r"\W+", "_", sim["titulo"])
    d1.download_button("🖨️ Ranking PDF", pdf_ranking(sim, df, extra, det),
                       f"Ranking_{nombre_base}.pdf", "application/pdf", key="simy_dl_pdf")
    d2.download_button("📊 Excel completo", excel_ranking(sim, df), f"Ranking_{nombre_base}.xlsx",
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="simy_dl_xls")
    d3.download_button("📱 Imagen para publicar", png_publicar(sim, df, int(top), extra),
                       f"Top_{nombre_base}.png", "image/png", key="simy_dl_png")
    d4.download_button("🧾 Boletas de todos (PDF)", pdf_boletas(sim, list(df["ID"])),
                       f"Boletas_{nombre_base}.pdf", "application/pdf", key="simy_dl_bol")
    try:
        d5.download_button("🗂️ Hojas corregidas (PDF)", pdf_hojas_corregidas(sim, list(df["ID"])),
                           f"Hojas_corregidas_{nombre_base}.pdf", "application/pdf", key="simy_dl_hc")
    except Exception as e:
        d5.error(f"No se pudo generar: {e}")

    with st.expander("📲 Enviar notas por WhatsApp a los padres"):
        mat_wa = _matricula()
        enlaces, sin_cel = [], 0
        for _, fila in df.iterrows():
            hoja = sim["hojas"][fila["ID"]]
            num = _num_wa((mat_wa.get(norm_dni(hoja.get("dni")), {}) or {}).get("celular", ""))
            if not num:
                sin_cel += 1
                continue
            url = f"https://wa.me/{num}?text={urllib.parse.quote(mensaje_whatsapp(sim, fila, hoja, len(df)))}"
            enlaces.append(f'<a href="{url}" target="_blank" style="display:inline-block;margin:3px;padding:6px 12px;'
                           f'background:#25D366;color:#fff;border-radius:18px;text-decoration:none;font-size:13px;">'
                           f'📱 {_html.escape(str(fila["Apellidos y Nombres"])[:30] or "Alumno")}</a>')
        if enlaces:
            st.caption(f"Toca el nombre y se abre WhatsApp con la nota lista para enviar al apoderado "
                       f"({len(enlaces)} con celular" + (f", {sin_cel} sin celular en la matrícula" if sin_cel else "") + ").")
            st.markdown("".join(enlaces), unsafe_allow_html=True)
        else:
            st.info("Ningún alumno de este ranking tiene celular del apoderado en la matrícula.")

    with st.expander("🧾 Boleta de un estudiante / corregir o eliminar hoja"):
        opc = {r["ID"]: f"{r['Puesto']}. {r['Apellidos y Nombres']} ({r['DNI']})" for _, r in df.iterrows()}
        hid = st.selectbox("Estudiante:", list(opc), format_func=lambda k: opc[k], key="simy_bol_sel")
        st.download_button("🖨️ Descargar su boleta", pdf_boletas(sim, [hid]),
                           f"Boleta_{sim['hojas'][hid].get('dni', '')}.pdf", "application/pdf", key="simy_bol_dl")
        h = sim["hojas"][hid]
        if (not h.get("nombre")) and h.get("nombre_img"):
            st.image(base64.b64decode(h["nombre_img"]), caption="Nombre escrito por el alumno")
        e1, e2, e3 = st.columns([1, 2, 1])
        n_dni = e1.text_input("DNI:", h.get("dni", ""), key=f"simy_edni_{hid}")
        n_nom = e2.text_input("Nombre:", h.get("nombre", ""), key=f"simy_enom_{hid}")
        opc_g = [""] + grupos_sim(sim)
        if sim.get("sin_area"):
            n_grp = h.get("grupo") or grupos_sim(sim)[0]
        else:
            n_grp = e3.selectbox("Área / Grupo:", opc_g, index=opc_g.index(h.get("grupo", "")) if h.get("grupo", "") in opc_g else 0,
                                 key=f"simy_egrp_{hid}")
        if st.button("💾 Guardar cambios", key=f"simy_esave_{hid}"):
            h.update({"dni": norm_dni(n_dni) or n_dni, "nombre": n_nom.strip().upper(), "grupo": n_grp})
            guardar_datos(datos)
            if sim.get("publicado"):
                publicar_en_historial(sim)
            st.success("Actualizado.")
            st.rerun()
        if not _HOOKS["puede_borrar"] or _HOOKS["puede_borrar"]():
            if st.button("🗑️ Eliminar esta hoja", key=f"simy_edel_{hid}"):
                sim["hojas"].pop(hid, None)
                guardar_datos(datos)
                if sim.get("publicado"):
                    publicar_en_historial(sim)
                st.rerun()

    st.markdown("#### 📢 Publicar")
    if sim.get("publicado"):
        st.success("✅ Publicado: cada estudiante lo ve en su historial / portal.")
        p1, p2 = st.columns(2)
        if p1.button("🔄 Actualizar publicación", key="simy_repub"):
            publicar_en_historial(sim)
            st.success("Actualizado.")
        if p2.button("🙈 Retirar publicación", key="simy_unpub"):
            quitar_de_historial(sim)
            sim["publicado"] = False
            guardar_datos(datos)
            st.rerun()
    else:
        st.caption("Al publicar, las notas por curso y el puesto pasan al historial de cada estudiante "
                   "(Portal del Estudiante y Portal de Padres).")
        if st.button("📢 Publicar resultados en el historial", type="primary", key="simy_pub"):
            if publicar_en_historial(sim):
                sim["publicado"] = True
                guardar_datos(datos)
                st.success("¡Publicado!")
                st.rerun()
            else:
                st.error("No se pudo escribir el historial.")


def historial_estudiante(datos, dni):
    filas = []
    for sid, sim in datos["simulacros"].items():
        for hid, h in sim.get("hojas", {}).items():
            if h.get("dni") != dni:
                continue
            df = tabla_ranking(sim)
            fila_r = df[df["ID"] == hid]
            c = calificar(sim, h)
            f = {"Fecha": sim.get("fecha", ""), "Simulacro": sim["titulo"],
                 "Puesto": int(fila_r["Puesto"].iloc[0]) if not fila_r.empty else None,
                 "De": len(df), "Correctas": c["correctas"], "Puntaje": c["puntaje"],
                 "Máximo": puntaje_maximo(sim, h.get("grupo", "")), "Nota": c["nota"], "_creado": sim.get("creado", "")}
            for cn, cv in c["cursos"].items():
                f[cn] = cv["nota"]
            filas.append(f)
    if not filas:
        return pd.DataFrame()
    return pd.DataFrame(filas).sort_values("_creado").drop(columns=["_creado"]).reset_index(drop=True)


def pdf_historial(nombre, dni, df):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Table, TableStyle
    pag = landscape(A4)
    ancho, alto = pag
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=pag)
    _encabezado(c, ancho, alto, "Historial de simulacros", f"{nombre} — DNI {dni}")
    cols = [x for x in df.columns]
    data = [[x[:14] for x in cols]] + [[("" if pd.isna(v) else (f"{v:g}" if isinstance(v, float) else str(v)))[:30]
                                        for v in r] for _, r in df.iterrows()]
    t = Table(data, repeatRows=1)
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 7),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3d1e6")),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    tw, th = t.wrapOn(c, ancho - 40, alto - 120)
    t.drawOn(c, (ancho - tw) / 2, alto - 90 - th)
    c.showPage()
    c.save()
    return buf.getvalue()


def _tab_historial(datos):
    st.subheader("📚 Historial del estudiante")
    personas = {}
    for sim in datos["simulacros"].values():
        for h in sim.get("hojas", {}).values():
            if h.get("dni"):
                personas[h["dni"]] = h.get("nombre") or personas.get(h["dni"], "")
    if not personas:
        st.info("Aún no hay estudiantes calificados.")
        return
    busc = st.text_input("Buscar por DNI o apellido:", key="simy_hbus").strip().upper()
    opciones = [d for d, n in sorted(personas.items(), key=lambda x: x[1])
                if not busc or busc in d or busc in (n or "")]
    if not opciones:
        st.warning("Sin coincidencias.")
        return
    dni = st.selectbox("Estudiante:", opciones, format_func=lambda d: f"{personas[d]} — {d}", key="simy_hsel")
    df = historial_estudiante(datos, dni)
    if df.empty:
        st.info("Sin resultados.")
        return
    a, b, c = st.columns(3)
    a.metric("Simulacros rendidos", len(df))
    b.metric("Mejor puesto", int(df["Puesto"].min()))
    if len(df) > 1:
        c.metric("Última nota", f"{df['Nota'].iloc[-1]:.2f}", f"{df['Nota'].iloc[-1] - df['Nota'].iloc[-2]:+.2f}")
    else:
        c.metric("Última nota", f"{df['Nota'].iloc[-1]:.2f}")
    st.dataframe(df, use_container_width=True, hide_index=True)
    if len(df) > 1:
        st.markdown("**Evolución de la nota (/20)**")
        st.line_chart(df.set_index("Simulacro")[["Nota"]])
    st.download_button("🖨️ Imprimir historial (PDF)", pdf_historial(personas[dni], dni, df),
                       f"Historial_{dni}.pdf", "application/pdf", key="simy_hpdf")


def _tab_analisis(datos):
    st.subheader("📊 Análisis por pregunta y por curso")
    sid = _selector_simulacro(datos, "simy_sel_an")
    if not sid:
        return
    sim = datos["simulacros"][sid]
    hojas = list(sim.get("hojas", {}).values())
    if not hojas:
        st.info("Sin hojas calificadas.")
        return
    gs = grupos_sim(sim)
    gsel = None
    if sim.get("cursos_area") and not sim.get("todos_cursos"):
        if len(gs) > 1:
            gsel = st.selectbox("Área a analizar:", gs, format_func=lambda g: f"Área {g}", key="simy_an_area")
            hojas = [h for h in hojas if h.get("grupo") == gsel]
            if not hojas:
                st.info(f"No hay hojas del Área {gsel}.")
                return
        else:
            gsel = gs[0]
    curso_de = {}
    for c in cursos_de(sim, gsel or ""):
        for q in range(c["desde"], c["hasta"] + 1):
            curso_de[q] = c["nombre"]
    nq = n_preguntas(sim, gsel or "")
    clave_ref = clave_para(sim, gsel or "A")
    validas = preguntas_validas(sim, gsel or "") if sim.get("cursos_area") and gsel else None
    filas = []
    for q in range(nq):
        if validas is not None and (q + 1) not in validas:
            continue
        cont = {"A": 0, "B": 0, "C": 0, "D": 0, "Blanco": 0}
        ok = tot = 0
        for h in hojas:
            k = clave_para(sim, h.get("grupo", ""))
            k = k[q] if q < len(k) else ""
            r = h["respuestas"][q] if q < len(h["respuestas"]) else "_"
            cont[r if r in "ABCD" else "Blanco"] += 1
            if k in "ABCD" and k:
                tot += 1
                ok += r == k
        filas.append({"Pregunta": q + 1, "Curso": curso_de.get(q + 1, "-"),
                      "Clave": (clave_ref + " " * 100)[q].strip(),
                      "% acierto": round(ok / tot * 100, 1) if tot else None, **cont})
    dfp = pd.DataFrame(filas)
    dfp["% acierto"] = pd.to_numeric(dfp["% acierto"], errors="coerce")
    dfc = dfp.groupby("Curso", sort=False)["% acierto"].mean().round(1).reset_index()
    st.markdown("**Promedio de acierto por curso**")
    st.bar_chart(dfc.set_index("Curso"))
    st.markdown("**Las 10 preguntas más difíciles**")
    st.dataframe(dfp.sort_values("% acierto").head(10), hide_index=True, use_container_width=True)
    with st.expander("Ver todas las preguntas"):
        st.dataframe(dfp, hide_index=True, use_container_width=True)


# ================================================================
# LISTA DE CONTROL (quién ya rindió / quién falta)
# ================================================================
def _lista_auto(sim):
    """'AB' o 'CD' si el simulacro es de un solo grupo CEPRE; None en otro caso."""
    if sim.get("sin_area") or not sim.get("cursos_area"):
        return None
    gs = set(grupos_sim(sim))
    ab, cd = bool(gs & {"A", "B"}), bool(gs & {"C", "D"})
    return "AB" if ab and not cd else ("CD" if cd and not ab else None)


def _nivel_auto(sim):
    if sim.get("sin_area"):
        return {"PRIMARIA": "PRIMARIA", "SECUNDARIA": "SECUNDARIA"}.get(sim.get("modalidad"))
    return None


def _lista_auto_nombre(sim):
    g = _lista_auto(sim)
    if g:
        return f"Grupo {g}"
    n = _nivel_auto(sim)
    return n.title() if n else None


def _es_grupo(grado, grp):
    g = str(grado or "").upper()
    return bool(re.search(rf"GRUPO\s*{grp}\b|PREU[\s-]*{grp}\b", g))


def _tabla_control(sim, mat, lote, alumnos):
    """Una fila por alumno de la lista con su estado. `alumnos` = {dni: {nombre, grado}}."""
    hojas = {}
    for h in sim.get("hojas", {}).values():
        d = norm_dni(h.get("dni"))
        if d:
            hojas[d] = h
    en_lote = {norm_dni(h.get("dni")) for h in lote}
    ausentes = set(sim.get("ausentes", []))
    filas = []
    for dni, a in alumnos.items():
        h = hojas.get(dni) or (hojas.get(dni[:8]) if len(dni) > 8 else None)
        if h:
            cal = calificar(sim, h)
            est, pts, nota = "✅ Registrado", cal["puntaje"], cal["nota"]
        elif dni in en_lote or dni[:8] in en_lote:
            est, pts, nota = "🟡 Leída, falta guardar", None, None
        elif dni in ausentes:
            est, pts, nota = "🚫 Faltó", None, None
        else:
            est, pts, nota = "⏳ Falta", None, None
        filas.append({"DNI": dni, "Alumno": a["nombre"], "Grado": a["grado"], "Estado": est,
                      "Puntaje": pts, "Nota": nota})
    df = pd.DataFrame(filas, columns=["DNI", "Alumno", "Grado", "Estado", "Puntaje", "Nota"])
    if len(df):
        orden = {"⏳ Falta": 0, "🟡 Leída, falta guardar": 1, "🚫 Faltó": 2, "✅ Registrado": 3}
        df["_o"] = df["Estado"].map(orden)
        df = df.sort_values(["_o", "Alumno"]).drop(columns="_o").reset_index(drop=True)
    return df


def _alumnos_de_lista(mat, opcion, sim=None):
    """Alumnos de la lista elegida: 'auto' (según el simulacro), 'todos', 'nivel:X' o 'gs:nivel|grado|sección'."""
    if opcion == "auto":
        g = _lista_auto(sim or {})
        n = _nivel_auto(sim or {})
        if g:
            return {d: a for d, a in mat.items() if _es_grupo(a["grado"], g)}
        if n:
            return {d: a for d, a in mat.items() if a.get("nivel", "") == n}
        return dict(mat)
    if opcion == "todos":
        return dict(mat)
    if opcion.startswith("nivel:"):
        n = opcion[6:]
        return {d: a for d, a in mat.items() if a.get("nivel", "") == n}
    if opcion.startswith("gs:"):
        niv, gr, se = (opcion[3:].split("|") + ["", ""])[:3]
        return {d: a for d, a in mat.items()
                if a.get("nivel", "") == niv and a.get("grado0", "") == gr and a.get("seccion", "") == se}
    return {d: a for d, a in mat.items() if a["grado"] == opcion}


def _opciones_lista(sim, mat):
    """[(clave, texto)] para el selector «Lista de»: primero la que corresponde al simulacro."""
    ops = []
    nom = _lista_auto_nombre(sim)
    if nom:
        n_auto = len(_alumnos_de_lista(mat, "auto", sim))
        if n_auto:
            ops.append(("auto", f"{nom} — {n_auto} alumnos"))
    ops.append(("todos", f"Toda la matrícula — {len(mat)} alumnos"))
    orden = ["INICIAL", "PRIMARIA", "SECUNDARIA", "PREUNIVERSITARIO", ""]
    por_nivel, por_gs = {}, {}
    for a in mat.values():
        n = a.get("nivel", "")
        por_nivel[n] = por_nivel.get(n, 0) + 1
        k = (n, a.get("grado0", ""), a.get("seccion", ""))
        por_gs[k] = por_gs.get(k, 0) + 1
    rk = lambda n: orden.index(n) if n in orden else len(orden)
    for n in sorted(por_nivel, key=rk):
        if n:
            ops.append((f"nivel:{n}", f"Todo {n.title()} — {por_nivel[n]} alumnos"))
    nat = lambda t: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", t)]
    for (n, g, se) in sorted(por_gs, key=lambda k: (rk(k[0]), nat(k[1]), k[2])):
        if not g:
            continue
        sec = f" {se}" if se and se.lower() not in ("única", "unica") else ""
        ops.append((f"gs:{n}|{g}|{se}", f"{(n.title() + ' › ') if n else ''}{g}{sec} — {por_gs[(n, g, se)]} alumnos"))
    return ops


def _resumen_control(df):
    c = df["Estado"].value_counts() if len(df) else {}
    g = lambda k: int(c.get(k, 0)) if len(df) else 0
    return {"total": len(df), "ok": g("✅ Registrado"), "lote": g("🟡 Leída, falta guardar"),
            "falto": g("🚫 Faltó"), "falta": g("⏳ Falta")}


def pdf_lista_control(sim, df, titulo_lista):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm,
                            topMargin=1.5 * cm, bottomMargin=1.4 * cm)
    st_ = getSampleStyleSheet()
    r = _resumen_control(df)
    el = [Paragraph(f"<b>LISTA DE CONTROL — {_latin(sim.get('titulo'), 70)}</b>", st_["Title"]),
          Paragraph(f"{_latin(titulo_lista, 60)} · Fecha del examen: {_latin(sim.get('fecha'), 16)} · "
                    f"Registrados {r['ok']} de {r['total']} · Faltan {r['falta'] + r['lote']}", st_["Normal"]),
          Spacer(1, 8)]
    d2 = df.sort_values("Alumno").reset_index(drop=True)
    data = [["N.º", "Alumno", "DNI", "Estado", "✓"]]
    for i, f in d2.iterrows():
        est = {"✅ Registrado": "REGISTRADO", "🟡 Leída, falta guardar": "LEÍDA (sin guardar)",
               "🚫 Faltó": "FALTÓ", "⏳ Falta": "FALTA"}[f["Estado"]]
        data.append([str(i + 1), _latin(f["Alumno"], 46), f["DNI"], est, "X" if f["Estado"] == "✅ Registrado" else ""])
    t = Table(data, colWidths=[1.1 * cm, 8.4 * cm, 2.6 * cm, 3.8 * cm, 1.2 * cm], repeatRows=1)
    sty = [("FONT", (0, 0), (-1, -1), "Helvetica", 9), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#9b1b2f")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")), ("ALIGN", (0, 0), (0, -1), "CENTER"),
           ("ALIGN", (4, 0), (4, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    for i in range(1, len(data)):
        if data[i][3] == "FALTA":
            sty.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#fff1f1")))
        elif data[i][3] == "REGISTRADO":
            sty.append(("TEXTCOLOR", (3, i), (3, i), colors.HexColor("#15803d")))
    t.setStyle(TableStyle(sty))
    el.append(t)
    doc.build(el)
    return buf.getvalue()


def _tab_lista(datos):
    st.subheader("📋 Lista de control: ¿quién ya rindió?")
    sid = _selector_simulacro(datos, "simy_sel_lista")
    if not sid:
        return
    sim = datos["simulacros"][sid]
    mat = _matricula()
    if not mat:
        st.warning("No hay alumnos en la matrícula, así que no se puede armar la lista.")
        return
    lote = st.session_state.get(f"simy_lote_{sid}", [])
    auto = _lista_auto(sim)

    # ---- ¿de qué grupo / grado es la lista? (se elige sola; se puede cambiar) ----
    nom_auto = _lista_auto_nombre(sim)
    if nom_auto and not _alumnos_de_lista(mat, "auto", sim):
        st.info(f"No encontré alumnos de «{nom_auto}» en la matrícula; elige el grado o grupo en la lista de abajo.")
    opciones = _opciones_lista(sim, mat)
    sel = st.selectbox("Lista de (nivel › grado › sección):", [o[0] for o in opciones],
                       format_func=dict(opciones).get, key=f"simy_lista_sel_{sid}")
    alumnos = _alumnos_de_lista(mat, sel, sim)
    df = _tabla_control(sim, mat, lote, alumnos)
    if df.empty:
        st.info("Esta lista no tiene alumnos.")
        return
    r = _resumen_control(df)
    pend = r["falta"] + r["lote"]

    # ---- resumen grande ----
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("👥 En la lista", r["total"])
    m2.metric("✅ Ya registrados", r["ok"])
    m3.metric("⏳ Faltan", pend)
    m4.metric("🚫 Faltaron", r["falto"])
    st.progress(min(1.0, (r["ok"] + r["falto"]) / r["total"]))
    if r["lote"]:
        st.warning(f"🟡 {r['lote']} alumno(s) ya fueron leídos pero **no los has guardado**. "
                   "Ve a 📸 Escanear y pulsa «Guardar hojas en el simulacro».")
    if pend == 0:
        st.success("🎉 ¡Lista completa! Todos están registrados o marcados como que faltaron. Ya puedes ir a 🏆 Ranking.")
    else:
        st.info(f"Faltan {pend} alumno(s). Escanea sus hojas en 📸 Escanear, o márcalos como «Faltó» si no vinieron.")

    # ---- filtros simples ----
    f1, f2 = st.columns([2, 1])
    ver = f1.radio("Mostrar:", ["⏳ Solo los que faltan", "✅ Ya registrados", "📋 Todos"], horizontal=True,
                   key=f"simy_lista_ver_{sid}")
    buscar = f2.text_input("🔎 Buscar por nombre o DNI:", key=f"simy_lista_buscar_{sid}").strip().upper()
    v = df
    if ver.startswith("⏳"):
        v = v[v["Estado"].isin(["⏳ Falta", "🟡 Leída, falta guardar"])]
    elif ver.startswith("✅"):
        v = v[v["Estado"] == "✅ Registrado"]
    if buscar:
        v = v[v["Alumno"].str.contains(buscar, regex=False) | v["DNI"].str.contains(buscar, regex=False)]
    v = v.reset_index(drop=True)

    ausentes = set(sim.get("ausentes", []))
    vista = pd.DataFrame({"Estado": v["Estado"], "Alumno": v["Alumno"], "DNI": v["DNI"],
                          "Puntaje": v["Puntaje"], "Nota": v["Nota"],
                          "Faltó al examen": v["DNI"].isin(ausentes)})
    vkey = f"simy_lista_v_{sid}"
    st.session_state.setdefault(vkey, 0)
    if vista.empty:
        st.caption("No hay nadie en esta vista.")
        ed = vista
    else:
        st.caption("Marca la casilla «Faltó al examen» en los alumnos que no vinieron y pulsa Guardar.")
        ed = st.data_editor(vista, use_container_width=True, hide_index=True,
                            disabled=["Estado", "Alumno", "DNI", "Puntaje", "Nota"],
                            key=f"simy_lista_ed_{sid}_{ver}_{buscar}_{st.session_state[vkey]}",
                            height=min(560, 38 * (len(vista) + 1) + 4))
        if st.button("💾 Guardar «Faltó al examen»", type="primary", key=f"simy_lista_save_{sid}"):
            registrados = set(df.loc[df["Estado"] == "✅ Registrado", "DNI"])
            visibles = set(v["DNI"])
            marcados = {d for d, f in zip(ed["DNI"], ed["Faltó al examen"]) if f and d not in registrados}
            sim["ausentes"] = sorted((ausentes - visibles) | marcados)
            guardar_datos(datos)
            st.session_state[vkey] += 1
            st.success("Guardado.")
            st.rerun()

    # ---- hojas guardadas de personas que no están en esta lista ----
    dnis_lista = set(df["DNI"]) | {d[:8] for d in df["DNI"] if len(d) > 8}
    fuera = [h for h in sim.get("hojas", {}).values() if norm_dni(h.get("dni")) not in dnis_lista]
    if fuera:
        with st.expander(f"⚠️ {len(fuera)} hoja(s) guardada(s) de alumnos que NO están en esta lista"):
            st.caption("Pueden ser de otro grupo o tener el DNI mal leído. Revísalas en 🏆 Ranking → corregir hoja.")
            st.dataframe(pd.DataFrame([{"DNI": h.get("dni", ""), "Alumno": h.get("nombre", ""),
                                        "Grupo": h.get("grupo", "")} for h in fuera]),
                         use_container_width=True, hide_index=True)

    # ---- descargas ----
    st.markdown("---")
    d1, d2 = st.columns(2)
    titulo_lista = dict(opciones)[sel]
    try:
        d1.download_button("🖨️ Lista para imprimir (PDF)", pdf_lista_control(sim, df, titulo_lista),
                           "Lista_de_control.pdf", "application/pdf", key=f"simy_lista_pdf_{sid}")
    except Exception as e:
        d1.error(f"No se pudo generar el PDF: {e}")
    bx = io.BytesIO()
    df.to_excel(bx, index=False)
    d2.download_button("📊 Descargar en Excel", bx.getvalue(), "Lista_de_control.xlsx",
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       key=f"simy_lista_xls_{sid}")


def tab_simulacros_yachay(config=None, cargar_matricula=None, cargar_historial=None,
                          guardar_historial=None, backup_json=None, puede_borrar=None):
    _HOOKS.update({"cargar_matricula": cargar_matricula, "cargar_historial": cargar_historial,
                   "guardar_historial": guardar_historial, "backup_json": backup_json,
                   "puede_borrar": puede_borrar})
    st.header("🧾 Simulacros Yachay — Lectura de hojas y ranking")
    boton_hoja(None, "simy_dl_hoja_top")
    st.caption("Flujo: 1) ⚙️ Configurar el examen (elige Área A/B/C/D o Grupo AB/CD, pega las claves) → 2) 📸 Escanear las hojas → "
               "3) 📋 Lista de control (¿falta alguien?) → 4) 🏆 Ranking (imprimir / publicar) → 5) 📚 Historial del estudiante.")
    datos = cargar_datos()
    t = st.tabs(["⚙️ Configurar", "📸 Escanear", "📋 Lista de control", "🏆 Ranking", "📚 Historial", "📊 Análisis"])
    with t[0]:
        _tab_configurar(datos)
    with t[1]:
        _tab_escanear(datos)
    with t[2]:
        _tab_lista(datos)
    with t[3]:
        _tab_ranking(datos)
    with t[4]:
        _tab_historial(datos)
    with t[5]:
        _tab_analisis(datos)


# ================================================================
# LOGOS DE LA HOJA (PNG con fondo transparente, incrustados para no depender de más archivos)
# ================================================================
_LOGO_IZQ_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAPwAAAD8CAMAAABkdTlVAAACf1BMVEXun6SnYVnVY1jgppSoWyEfZ5Wn0+esmV5hkqnVmHCZoKSYtM/QTifd2eT919tnq84jUGfn25sth6dTb5LlJSV2JBxTYWWtjSenOUUhNVfeozL+xsj+2OAWJjTQa3HWe4OwXGFkWzKgISzeeYX+usPf1WDbxDb5ucNzxeLINkWsxq4sj8iqdob9wr27e4h7OkB1gk2KOz6+wFLWgX794+36+/iuFRDOGRaUFAuUCwnoJCXRqEjPJBeoCw3RJifw1mzXtk7GmDW0iC2wJinpxlXOpjfwyWn76evQGiTpuFGzJBbmGRnrHCT76NS6lDP++NbmJBuwGiSQJQnOmUf819DrqFCRJyl4FQqvNjHWtTPLDBF2CQTIiTTV+f6seijq1FjqmFKzlk7NNCz2t7D1uGn+2+T243TMNRfQ5/n7yMkuZ42peRnktzariUkWR27+2+UvVnTx1owqSWuSGiTt2K+TNjSwR0nLZzCWdzARKU3/4+cwdpPaxFLQdnIVNlXMdzTOtm3+2NuyV1LZx2+VNgbvl5H2xrbUiEfmxTjz5rP/5OnzqKmxNhPSlpDpiU3KV1KrRxH3qWlOiKv/1df+2+X+y9NPdpPXxo+x1u/QiInNaGrNWCxxlrD1yIoQOWavRS8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUyIh/AAAAoHRSTlOw8/P9/v/////+///+/xz////////5///0//+hWP+7u7n/4/Ck//////j///+vt///v/+/AP/+//7///////7//////f////////7////////+/v////v9/f///v////////7//0L///////////8Q/////P/7/f///0b///7///9F/v////////8w//////3///9gMGD//////v/////+4JyNBQAAYf9JREFUeNrdvQdDG8myNqwEQgQbTHTcXXvD2XPufb9kjUZpEBqhBEIo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"
)
_LOGO_DER_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAALAAAAB8CAMAAAD+Q8qjAAACf1BMVEXWmxtToGKeXgsmWyLi26Omnlueo5T63t6ikCDW29LZ0l2b3KxcZVddXiffawX857MdnE8imzL939raslIbMR9RzWyy58lv24385cebLxJNKgSfIhySdFTXGCF2oottiRMuZUbKtp+4xBHc9w83zFrJFyNuJByoymJEM12wRwA9PkLrlCv+4e/4+vf2+ArmAwTXBQPz6A/05y35+Cz22S0OBwLNFQT12RLz5074+EwvJgDu6u772+3x2UwPhy2zFwP45242NgFORwFRBAD957MoFwD86I1wBQANeSpuaQRIOAAWFgL5+dWOhwf95df6yCv959WOCABWVgISljDW1y795sfLJgKyJgH+5ehoWAHY+uuRFgK0CgHU1w51dQT2yBSJeQSupwbOxy7qFQgFdxUvBgD75Oj+58VvFQCWlgkGZhL92un46K0vp0yzNgDKOAD02Wz96ar3lw3s59Iul0vOyQ3V2Ez6tyz+2tgFVw/LRgDRVwH69W30hgn3pxD9thQphzSqmAja5wq1t7QGhhmztgbJuDAOaCmOJgGwqS0wtlBwNwCzti/RaAXreQMPJwRRFgDvykr8840vhUmOZwXKtw7a5C376JX99q4VpDZtJwAIRw1xdXTQ+dcteElxRgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADMfO6PAAAAoHRSTlP+////8f//Jf/9/P////+q//9U//////+l//+/////////////v7///7//vwD///////7//v////3///8Q/v//+f///7L/8v////////9O/2D/////nf//Sv////////////////8wsf///0j3////9M////////9M////+f///////////////////////////PH/////z/b/////////c8kwngAAIi9JREFUeNrNfIdDGunW/lBFEHtJclN29+73u19ZkWkwM0qZQaSJBEQN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"
)
