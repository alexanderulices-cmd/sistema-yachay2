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

import html as _html
import io
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
                      "nivel": nv, "grado0": g, "seccion": s}
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
        return "Áreas " + " + ".join(grupos_sim(sim))
    return "Personalizado"


def clave_para(sim, grupo):
    claves = sim.get("claves", {})
    if sim.get("cursos_area"):
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
    cab = [Paragraph("Pto" if x == "Puesto" else x, est_cab) for x in cols]

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
    filas = [[_fmt(x, r[x]) for x in cols] for _, r in df.iterrows()]
    por_pag = 22 if detalle_cursos else 34
    sub = f"{sim.get('fecha', '')}  ·  {titulo_extra}  ·  Puntaje máximo: {puntaje_maximo(sim):g}"
    for ini in range(0, max(len(filas), 1), por_pag):
        _encabezado(c, ancho, alto, f"RANKING — {sim['titulo']}", sub)
        data = [cab] + filas[ini:ini + por_pag]
        anchos = None
        if detalle_cursos:
            resto = ancho - 50 - 26 - 175 - 58 - 30 - 34
            otros = max(len(cols) - len(base_cols), 1)
            anchos = ([26, 175, 58, 30] + ([] if sim.get("sin_area") else [34])) + [resto / otros] * otros
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
    c.drawString(40, y, f"Aula: {hoja.get('aula', '') or '-'}     Grupo: {hoja.get('grupo', '') or '-'}")
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
    n = n_preguntas(sim, hoja.get("grupo", ""))
    resp = hoja.get("respuestas", "")
    c.setFont("Helvetica", 7.5)
    col_w, fil_h, por_col = 103, 11.2, 25
    for q in range(n):
        col, fil = divmod(q, por_col)
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
        "titulo": sim["titulo"], "fecha": sim.get("fecha", ""), "periodo": sim.get("periodo", ""),
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
BASE_HOJA = "hoja_yachay_base.jpg"       # hoja limpia (sin código de barras falso)
_PX = 595.2 / 2480.0                     # píxeles de la hoja (300 dpi) -> puntos PDF
_PINK = (240, 225, 255)                  # BGR del rosado de la hoja
_BASE_CACHE = {}


def _base_hoja_jpg():
    """Bytes JPG de la hoja base (2480 x 3508). Si no existe el archivo base, lo
    construye a partir de la hoja antigua Hoja_Yachay_en_blanco.pdf."""
    if "jpg" in _BASE_CACHE:
        return _BASE_CACHE["jpg"]
    if Path(BASE_HOJA).exists():
        _BASE_CACHE["jpg"] = Path(BASE_HOJA).read_bytes()
        return _BASE_CACHE["jpg"]
    import numpy as np
    import cv2
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz
    doc = fitz.open(HOJA_PDF)
    raw = doc.extract_image(doc[0].get_images()[0][0])["image"]
    if "yachay-v2" in str(doc.metadata.get("subject", "")):
        _BASE_CACHE["jpg"] = raw
        return raw
    im = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
    out = im.copy()
    out[3253:3328, 176:730] = _PINK             # código de barras que no servía
    out[3246:3328, 1860:2300] = _PINK           # número de serie
    out[3224:3252, 1395:1730] = _PINK           # "SIMULACRO BIMESTRAL"
    logo = im[176:326, 2076:2276].copy()         # logo derecho -> se corre a la izquierda
    out[176:326, 2076:2276] = _PINK
    out[176:326, 1850:2050] = logo
    ok, buf = cv2.imencode(".jpg", out, [cv2.IMWRITE_JPEG_QUALITY, 92])
    _BASE_CACHE["jpg"] = buf.tobytes()
    return _BASE_CACHE["jpg"]


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


def hoja_pdf(sim=None):
    """PDF A4 de la hoja de respuestas. Con `sim`: lleva el QR del simulacro, su título
    y su fecha impresos. Sin `sim`: hoja genérica con líneas para escribir a mano."""
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.pdfgen import canvas
    Wp, Hp = 595.2, 841.92
    X = lambda px: px * _PX
    Y = lambda py: Hp - py * _PX
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(Wp, Hp))
    c.setTitle("Hoja de respuestas Yachay")
    c.setSubject("yachay-v2")
    c.drawImage(ImageReader(io.BytesIO(_base_hoja_jpg())), 0, 0, Wp, Hp)

    gris = colors.HexColor("#6b7280")
    negro = colors.HexColor("#111111")
    # ---- pie de hoja: título y fecha del simulacro ----
    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(X(232), Y(3266), "SIMULACRO")
    c.drawString(X(1600), Y(3266), "FECHA")
    if sim:
        titulo = _latin(sim.get("titulo"), 70).upper()
        tam = 12.5
        while tam > 8 and stringWidth(titulo, "Helvetica-Bold", tam) > X(1280):
            tam -= 0.5
        c.setFillColor(negro)
        c.setFont("Helvetica-Bold", tam)
        c.drawString(X(232), Y(3314), titulo)
        c.setFont("Helvetica-Bold", 12.5)
        c.drawString(X(1600), Y(3314), _latin(sim.get("fecha"), 16))
        c.setFillColor(gris)
        c.setFont("Helvetica", 6.5)
        c.drawRightString(X(2290), Y(3266), "Cód. " + _latin(sim.get("id"), 24))
    else:
        c.setStrokeColor(negro)
        c.setLineWidth(0.6)
        c.line(X(232), Y(3314), X(1480), Y(3314))
        c.line(X(1600), Y(3314), X(2090), Y(3314))

    # ---- QR (esquina derecha del encabezado) ----
    if sim and sim.get("id"):
        m = _matriz_qr(codigo_qr(sim))
        n = m.shape[0]
        mod = 7.6                                   # px por módulo -> QR de ~220 px (18.6 mm)
        x0, y0 = 2082, 142
        c.setFillColor(colors.white)
        c.rect(X(x0 - 6), Y(y0 + n * mod + 6), X(n * mod + 12), X(n * mod + 12), fill=1, stroke=0)
        c.setFillColor(colors.black)
        for f in range(n):                         # tramos horizontales: sin rendijas
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
    c.showPage()
    c.save()
    return buf.getvalue()


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
    st.download_button(etiqueta or ("🖨️ Hojas de ESTE simulacro (con QR)" if sim else
                                    "📄 Hoja en blanco (genérica)"),
                       data, nombre, "application/pdf", key=key)


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


def resolver_dni(leido, mat):
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
                cands.append((dif, k))
        cands.sort()
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
        boton_hoja(sim, pfx + "dl_hoja_cfg")
        st.caption("Estas hojas llevan el QR de este simulacro, su título y su fecha.")
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
    if len(grupos) > 1:
        previas = [sim.get("claves", {}).get(g, "") for g in grupos]
        ya_igual = bool(sid) and all(previas) and len(set(previas)) == 1
        compartida = st.checkbox(f"🔑 La clave de respuestas es la MISMA para las áreas {_unir(grupos)}",
                                 value=True if not sid else ya_igual, key=pfx + "misma_clave",
                                 help="Márcalo si las áreas rinden las mismas 80 respuestas: pegas la clave una sola vez. "
                                      "Desmárcalo si cada área tiene su propia clave.")

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
        if guardado and ver == 0:
            base = [(c["nombre"], c["hasta"] - c["desde"] + 1) for c in guardado]
        else:
            base = plantilla if unico else PLANTILLAS_AREA[g]
        ca, cb = st.columns([1.2, 1])
        with ca:
            st.markdown("**1️⃣ Cursos y n.º de preguntas**")
            df = pd.DataFrame(base, columns=["Curso", "Preguntas"])
            df_e = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True,
                                  key=pfx + f"cur_{mk}_{g}_{ver}",
                                  column_config={"Preguntas": st.column_config.NumberColumn(
                                      min_value=1, max_value=100, step=1)})
            if st.button("↩️ Restaurar cursos originales" if unico else "↩️ Restaurar temario oficial",
                         key=pfx + f"rstb_{mk}_{g}"):
                st.session_state[rk] = ver + 1
                st.rerun()
        cursos_g, err_g = _cursos_desde_df(df_e, float(p_ok), float(p_mal))
        pre = "" if unico else f"Área {g}: "
        errores.extend(pre + e for e in err_g)
        with cb:
            st.markdown(_html_area(g, cursos_g, "CURSOS DEL SIMULACRO" if unico else None), unsafe_allow_html=True)
        cursos_area[g] = cursos_g
        n_g = cursos_g[-1]["hasta"] if cursos_g else 0
        if not cursos_g:
            errores.append(pre + "no tiene cursos.")
        if n_g > 100:
            errores.append(pre + f"tiene {n_g} preguntas y la hoja solo admite 100.")
        if len({c["nombre"] for c in cursos_g}) != len(cursos_g):
            errores.append(pre + "hay cursos con el mismo nombre.")
        if not compartida:
            claves[g] = _bloque_clave(g, "2️⃣ Clave de respuestas" if unico else f"2️⃣ Clave de respuestas del Área {g}",
                                      n_g, sim.get("claves", {}).get(g, ""))

    if unico:
        _bloque_area(grupos[0])
    else:
        for g, tg in zip(grupos, st.tabs([f"Área {g}" for g in grupos])):
            with tg:
                _bloque_area(g)
        if compartida:
            st.markdown("---")
            n_ref = max((c[-1]["hasta"] for c in cursos_area.values() if c), default=80)
            ini = next((sim.get("claves", {}).get(g) for g in grupos if sim.get("claves", {}).get(g)), "")
            k = _bloque_clave("comun", f"🔑 Clave de respuestas (la misma para las áreas {_unir(grupos)})", n_ref, ini)
            for g in grupos:
                claves[g] = k

    for e in errores:
        st.error(e)
    if st.button("💾 Guardar simulacro", type="primary", disabled=bool(errores), key=pfx + "save"):
        nuevo = dict(sim)
        n_max = max(c[-1]["hasta"] for c in cursos_area.values())
        nuevo.update({"titulo": titulo.strip() or "Simulacro", "fecha": fecha, "periodo": periodo,
                      "num_preguntas": int(n_max), "puntaje_blanco": p_bl,
                      "claves": {g: claves.get(g, "") for g in grupos},
                      "grupos": list(grupos), "cursos_area": cursos_area,
                      "cursos": cursos_area[grupos[0]], "modalidad": mk, "clave_comun": bool(compartida)})
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



def _fecha_tupla(txt):
    m = re.search(r"(\d{1,2})\D+(\d{1,2})\D+(\d{4})", str(txt or ""))
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def _procesar_imagen(sim, img, mat, origen):
    r = omr.leer_hoja(img, sim["num_preguntas"])
    resp = "".join({"": "_"}.get(x, x) for x in r["respuestas"])
    dni_leido = r["dni"]
    rr = resolver_dni(dni_leido, mat)
    dni, info = rr["dni"], rr["info"]
    grupo = r["grupo"]
    gs = grupos_sim(sim)
    alertas = list(r["alertas"]) + rr["avisos"]
    if sim.get("sin_area"):
        grupo = gs[0]                         # colegio: se ignora el casillero de grupo de la hoja
    elif sim.get("cursos_area"):
        if not grupo and len(gs) == 1:
            grupo = gs[0]
        elif not grupo:
            alertas.append("No se leyó el ÁREA (A-D): elígela en la tabla")
        elif grupo not in gs:
            alertas.append(f"El área {grupo} no pertenece a este simulacro ({', '.join(gs)})")

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
    elif qr:
        alertas.append("QR no reconocido (no es de una hoja Yachay)")
    else:
        ft_hoja = (r.get("dia"), r.get("mes"), r.get("anio"))
        ft_sim = _fecha_tupla(sim.get("fecha"))
        if None not in ft_hoja and ft_sim and tuple(ft_hoja) != ft_sim:
            alertas.append(f"La fecha marcada en la hoja ({ft_hoja[0]:02d}/{ft_hoja[1]:02d}/{ft_hoja[2]}) "
                           f"no coincide con la del simulacro ({sim.get('fecha')})")

    sug = rr["sug"]
    if not info:
        alertas.append("DNI no encontrado en matrícula")
        if sug:
            alertas.append(f"¿Será {mat[sug]['nombre']} (DNI {sug})? Usa «Aceptar sugerencias» si es correcto")
    clave = clave_para(sim, grupo)
    return {"tmp_id": uuid.uuid4().hex[:8], "dni": dni, "nombre": info.get("nombre", ""),
            "grado": info.get("grado", ""), "aula": r["aula"], "grupo": grupo,
            "respuestas": resp, "dudosas": [i + 1 for i, e in enumerate(r["estados"]) if e in ("duda", "doble")],
            "alertas": alertas, "otro_sim": otro_sim, "sug_dni": sug if not info else None,
            "dni_leido": dni_leido,
            "origen": origen, "fecha_examen": f"{r['dia'] or ''}/{r['mes'] or ''}/{r['anio'] or ''}",
            "img": omr.imagen_revision(r, clave)}


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
        sim["hojas"][hid] = {"dni": dni, "nombre": (h.get("nombre") or "").strip().upper(),
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
        boton_hoja(sim, "simy_dl_hoja_scan")
        st.caption("Imprime estas hojas: llevan el QR del simulacro y su título/fecha, "
                   "así el sistema detecta si te equivocas de examen.")
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
        if archivos and st.button("🔍 Leer hojas", type="primary", key="simy_leer"):
            barra = st.progress(0.0, "Leyendo…")
            todas = []
            for a in archivos:
                try:
                    for p, img in enumerate(omr.imagenes_desde_archivo(a.name, a.getvalue())):
                        todas.append((img, f"{a.name}" + (f" pág.{p + 1}" if a.name.lower().endswith('.pdf') else "")))
                except Exception as e:
                    st.error(f"{a.name}: {e}")
            for i, (img, org) in enumerate(todas):
                st.session_state[lote_key].append(_procesar_imagen(sim, img, mat, org))
                barra.progress((i + 1) / max(len(todas), 1), f"Hoja {i + 1} de {len(todas)}")
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
                    "grado": mat.get(d, {}).get("grado", ""), "aula": "", "grupo": grp, "respuestas": resp,
                    "dudosas": [], "alertas": [], "origen": "manual", "img": None})
                st.rerun()

    lote = st.session_state[lote_key]
    if not lote:
        return
    st.markdown("---")
    st.markdown(f"### 🧾 Revisión del lote ({len(lote)} hojas sin guardar)")

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
        "Quitar": bool(h.get("otro_sim")), "DNI": h["dni"], "Apellidos y Nombres": h["nombre"], "Aula": h["aula"],
        "Grupo": h["grupo"], "Correctas": calificar(sim, h)["correctas"], "Puntaje": calificar(sim, h)["puntaje"],
        "Sugerencia DNI": (f"{h['sug_dni']} – {mat[h['sug_dni']]['nombre'][:28]}" if h.get("sug_dni") in mat else ""),
        "Revisar": ", ".join(h["alertas"] + _extra(h)), "Origen": h["origen"]} for h in lote])
    if _sa:
        vista = vista.drop(columns=["Grupo"])
    ed = st.data_editor(vista, use_container_width=True, hide_index=True,
                        key=f"simy_ed_{sid}_{len(lote)}_{st.session_state[ver_key]}",
                        disabled=["Correctas", "Puntaje", "Sugerencia DNI", "Revisar", "Origen"],
                        column_config=({} if _sa else
                                       {"Grupo": st.column_config.SelectboxColumn("Área", options=[""] + grupos_sim(sim))}))
    for h, (_, fila) in zip(lote, ed.iterrows()):
        nd = str(fila["DNI"]).strip()
        if nd != h["dni"]:
            h["dni"] = nd
            if norm_dni(nd) in mat and not str(fila["Apellidos y Nombres"]).strip():
                h["nombre"] = mat[norm_dni(nd)]["nombre"]
        if str(fila["Apellidos y Nombres"]).strip() and fila["Apellidos y Nombres"] != h["nombre"]:
            h["nombre"] = str(fila["Apellidos y Nombres"]).strip().upper()
        h["aula"] = str(fila["Aula"] or "")
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
                h.update({"dni": k, "nombre": mat[k]["nombre"], "grado": mat[k]["grado"], "sug_dni": None})
                _limpiar_alertas_dni(h)
        st.session_state[ver_key] += 1
        st.rerun()

    # Detalle de cada hoja
    for i, h in enumerate(lote):
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
                                          "sug_dni": None})
                                _limpiar_alertas_dni(h)
                                st.session_state[ver_key] += 1
                                st.rerun()
                        else:
                            st.caption("Sin coincidencias en la matrícula.")

    b1, b2 = st.columns(2)
    if b1.button("💾 Guardar hojas en el simulacro", type="primary", key="simy_guardar_lote"):
        validos = [h for h in lote if not h.get("_quitar")]
        sin_dni = [h for h in validos if not re.fullmatch(r"\d{8,9}", norm_dni(h["dni"]) or "")]
        if sin_dni:
            st.warning(f"{len(sin_dni)} hoja(s) sin DNI válido se guardan igual; corrígelas luego desde el ranking.")
        nuevos, reemp = _guardar_lote(datos, sid, validos)
        st.session_state[lote_key] = []
        st.success(f"Guardado: {nuevos} hojas nuevas, {reemp} actualizadas (mismo DNI).")
    if b2.button("🗑️ Vaciar lote sin guardar", key="simy_vaciar"):
        st.session_state[lote_key] = []
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
    fa = f1.selectbox("Aula:", ["Todas"] + aulas, key="simy_fa")
    fg = "Todos" if sim.get("sin_area") else f2.selectbox("Área / Grupo:", ["Todos"] + grupos_sim(sim), key="simy_fg")
    top = f3.number_input("Top para publicar:", 3, 30, 10, key="simy_top")
    df = tabla_ranking(sim, None if fa == "Todas" else fa, None if fg == "Todos" else fg)
    if df.empty:
        st.info("No hay resultados con ese filtro.")
        return
    extra = " · ".join(x for x in [f"Aula {fa}" if fa != "Todas" else "", f"Área {fg}" if fg != "Todos" else ""] if x) \
        or ("Ranking general " + etiqueta_modalidad(sim))

    if sim.get("cursos_area") and len(grupos_sim(sim)) > 1:
        sin_area = [h for h in sim["hojas"].values() if h.get("grupo") not in grupos_sim(sim)]
        if sin_area:
            st.warning(f"{len(sin_area)} hoja(s) sin área válida (obtienen 0). Corrígelas abajo en "
                       "'Boleta de un estudiante / corregir o eliminar hoja'.")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Participantes", len(df))
    m2.metric("Puntaje promedio", f"{df['Puntaje'].mean():.2f}")
    m3.metric("Puntaje más alto", f"{df['Puntaje'].max():g}")
    m4.metric("Nota promedio /20", f"{df['Nota'].mean():.2f}")
    st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)

    st.markdown("#### 📥 Descargar / imprimir")
    d1, d2, d3, d4 = st.columns(4)
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

    with st.expander("🧾 Boleta de un estudiante / corregir o eliminar hoja"):
        opc = {r["ID"]: f"{r['Puesto']}. {r['Apellidos y Nombres']} ({r['DNI']})" for _, r in df.iterrows()}
        hid = st.selectbox("Estudiante:", list(opc), format_func=lambda k: opc[k], key="simy_bol_sel")
        st.download_button("🖨️ Descargar su boleta", pdf_boletas(sim, [hid]),
                           f"Boleta_{sim['hojas'][hid].get('dni', '')}.pdf", "application/pdf", key="simy_bol_dl")
        h = sim["hojas"][hid]
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
    if sim.get("cursos_area"):
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
    filas = []
    for q in range(nq):
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
    boton_hoja(None, "simy_dl_hoja_top", "📄 Hoja de respuestas en blanco (genérica, para imprimir)")
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
