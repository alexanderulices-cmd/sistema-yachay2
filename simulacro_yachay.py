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


def letras_sim(sim):
    """Alternativas válidas del simulacro: A-E (hoja nueva) o A-D (simulacros antiguos)."""
    return "ABCDE" if int(sim.get("opciones", 4)) == 5 else "ABCD"


def anula_sim(sim):
    """Símbolo de pregunta anulada en la clave: X en los simulacros nuevos (la E ya es una alternativa);
    E en los antiguos."""
    return "X" if int(sim.get("opciones", 4)) == 5 else "E"

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
# Todos los cursos que se pueden elegir (áreas del MINEDU + cursos de preuniversitario y refuerzo)
CURSOS_CATALOGO = [
    "Comunicación", "Matemática", "Personal Social", "Ciencia y Tecnología", "Ciencias Sociales",
    "Desarrollo Personal, Ciudadanía y Cívica", "Educación para el Trabajo", "Arte y Cultura", "Educación Física",
    "Educación Religiosa", "Inglés", "Castellano como segunda lengua", "Computación",
    "Razonamiento Matemático", "Razonamiento Verbal", "Aritmética", "Álgebra", "Geometría", "Trigonometría",
    "Lenguaje", "Literatura", "Competencia Comunicativa", "Física", "Química", "Biología", "Anatomía",
    "Historia", "Historia del Perú", "Historia Universal", "Geografía", "Economía", "Educación Cívica",
    "Filosofía y Lógica", "Psicología", "Cultura General",
]
MODALIDADES_NIVEL = {
    "🏫 Primaria (Comunicación, Matemática, Personal Social, Ciencia y Tecnología)": "PRIMARIA",
    "🏫 Secundaria (Comunicación, Matemática, C. Sociales, DPCC, Ciencia y Tec., Inglés)": "SECUNDARIA",
    "🏫 Otro nivel o ciclo (cursos a mi gusto, una sola clave)": "OTRO",
}
MOD_PERSONALIZADO = "✏️ Personalizado (cursos y rangos a mi gusto)"

# Nombres de evaluación ya listos (para que todos los docentes los escriban igual)
EVALUACIONES = ([f"Simulacro {i}" for i in range(1, 11)] + [f"Semana {i}" for i in range(1, 61)] +
                ["Primer bimestre", "Segundo bimestre", "Tercer bimestre", "Cuarto bimestre",
                 "Evaluación bimestral", "Evaluación final"])
OTRO_NOMBRE = "✏️ Otro nombre (escribir)"
PERIODOS = ["(sin periodo)", "Primer bimestre", "Segundo bimestre", "Tercer bimestre", "Cuarto bimestre"]

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
    "backup_archivo": None,       # (nombre, bytes, mime) -> id de Drive (guarda un archivo)
    "bajar_archivo": None,        # (nombre) -> bytes (recupera un archivo de Drive)
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


_ESTADO = {"backup_error": ""}


def guardar_datos(d):
    with open(ARCHIVO_SIM, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    if _HOOKS["backup_json"]:
        try:
            _HOOKS["backup_json"](ARCHIVO_SIM, d)
            _ESTADO["backup_error"] = ""
        except Exception as e:                       # antes se callaba: ahora se avisa en pantalla
            _ESTADO["backup_error"] = str(e)[:160]


def limpiar_clave(texto, n, permitidas="ABCDE"):
    """Acepta 'ABCD...', 'a b c d', '1A 2B 3C' o una por línea."""
    t = (texto or "").upper()
    t = re.sub(r"\d+\s*[\.\)\-:]?", " ", t)      # quitar numeración
    letras = [c for c in t if c in permitidas]
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


def _pmax(cursos, clave="", pol="buena", letras="ABCD", anula="E"):
    """Puntaje máximo. Una pregunta anulada (letra E en la clave) cuenta como buena para todos
    ('buena') o se quita del total ('descartar'); así un alumno perfecto siempre saca 20."""
    tot = 0.0
    for c in cursos:
        for q in range(c["desde"], c["hasta"] + 1):
            k = clave[q - 1] if q - 1 < len(clave) else ""
            if clave and not ((k in letras and k) or (k == anula and pol == "buena")):
                continue
            tot += float(c["correcta"])
    return tot


def puntaje_maximo(sim, grupo=None):
    ca = sim.get("cursos_area")
    pol = sim.get("anulada", "buena")
    L_, A_ = letras_sim(sim), anula_sim(sim)
    if not ca:
        return _pmax(sim["cursos"], clave_para(sim, grupo or "A"), pol, L_, A_)
    if grupo is not None:
        ge = grupo_efectivo(sim, grupo)
        if ge:
            return _pmax(ca[ge], clave_para(sim, ge), pol, L_, A_)
    return max((_pmax(v, clave_para(sim, g_), pol, L_, A_) for g_, v in ca.items()), default=0)


def calificar(sim, hoja):
    clave = clave_para(sim, hoja.get("grupo", ""))
    cursos = cursos_de(sim, hoja.get("grupo", ""))
    resp = hoja.get("respuestas", "")
    blanco = float(sim.get("puntaje_blanco", 0))
    out = {"correctas": 0, "incorrectas": 0, "blancos": 0, "puntaje": 0.0, "cursos": {}}
    pol = sim.get("anulada", "buena")
    L_, A_ = letras_sim(sim), anula_sim(sim)
    for c in cursos:
        cc = ci = cb = cn = 0
        for q in range(c["desde"] - 1, c["hasta"]):
            k = clave[q] if q < len(clave) else ""
            r = resp[q] if q < len(resp) else "_"
            if k == A_:                        # pregunta ANULADA
                if pol == "buena":
                    cc += 1                    # se da por buena a todos
                    cn += 1
                continue
            if not k or k not in L_:
                continue                       # sin clave
            cn += 1
            if r == k:
                cc += 1
            elif r in ("_", "", " ", "-"):
                cb += 1
            else:
                ci += 1                        # incluye doble marca '*'
        pts = cc * float(c["correcta"]) + ci * float(c["incorrecta"]) + cb * blanco
        maxc = cn * float(c["correcta"])
        out["cursos"][c["nombre"]] = {
            "correctas": cc, "incorrectas": ci, "blancos": cb, "puntaje": round(pts, 2),
            "nota": round(max(pts, 0) / maxc * 20, 2) if maxc else 0.0}
        out["correctas"] += cc
        out["incorrectas"] += ci
        out["blancos"] += cb
        out["puntaje"] += pts
    out["puntaje"] = round(out["puntaje"], 2)
    _notas = [v["nota"] for v in out["cursos"].values()]
    out["promedio"] = round(sum(_notas) / len(_notas), 2) if _notas else 0.0
    mx = puntaje_maximo(sim, hoja.get("grupo", ""))
    out["nota"] = round(max(out["puntaje"], 0) / mx * 20, 2) if mx else 0.0
    return out


def preguntas_sospechosas(sim, gsel=None, minimo=8):
    """Preguntas cuya CLAVE podría estar mal. Es el error más caro de un examen: se nota cuando
    (a) la gran mayoría marcó otra alternativa y casi nadie la de la clave, o (b) los alumnos más
    fuertes fallan más que los más débiles. Se necesitan al menos `minimo` alumnos."""
    L_ = letras_sim(sim)
    hojas = [h for h in sim.get("hojas", {}).values() if gsel is None or h.get("grupo") == gsel]
    if len(hojas) < minimo:
        return []
    orden = sorted(hojas, key=lambda h: calificar(sim, h)["puntaje"])
    k27 = max(2, int(len(orden) * 0.27))
    bajos, altos = orden[:k27], orden[-k27:]
    validas = preguntas_validas(sim, gsel or "")
    curso_de = {q: c["nombre"] for c in cursos_de(sim, gsel or "") for q in range(c["desde"], c["hasta"] + 1)}
    out = []
    for q in sorted(validas):
        def _resp(h):
            r_ = h.get("respuestas", "")
            return r_[q - 1] if q - 1 < len(r_) else "_"
        marcas = []
        for h in hojas:
            k_ = clave_para(sim, h.get("grupo", ""))
            k_ = k_[q - 1] if q - 1 < len(k_) else ""
            if k_ in L_ and k_:
                marcas.append((_resp(h), k_))
        if len(marcas) < minimo:
            continue
        k = marcas[0][1]
        resp_ok = [r for r, _k in marcas if r in L_ and r]
        if len(resp_ok) < minimo:
            continue
        pct_ok = sum(1 for r, k_ in marcas if r == k_) / len(marcas)
        top, top_n = max(((o, resp_ok.count(o)) for o in L_), key=lambda t: t[1])

        def _tasa(lista):
            v = [(_resp(h), clave_para(sim, h.get("grupo", ""))[q - 1:q]) for h in lista]
            v = [(r, k_) for r, k_ in v if r in L_ and r]
            return (sum(1 for r, k_ in v if r == k_) / len(v)) if v else 0.0
        disc = _tasa(altos) - _tasa(bajos)
        motivo = ""
        if top != k and top_n / len(resp_ok) >= 0.5 and pct_ok < 0.30:
            motivo = f"el {top_n / len(resp_ok) * 100:.0f}% marcó la {top} y solo el {pct_ok * 100:.0f}% la {k} (la clave)"
        elif disc < -0.15 and pct_ok < 0.5:
            motivo = "los alumnos más fuertes fallan esta pregunta más que los más débiles"
        if motivo:
            out.append({"Pregunta": q, "Curso": curso_de.get(q, "-"), "Clave": k, "Más marcada": top,
                        "% acierto": round(pct_ok * 100, 1), "Por qué": motivo})
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
            f[cn] = round(c["cursos"][cn]["nota"], 2) if cn in c["cursos"] else None     # nota del curso, base 20
        f.update({"Correctas": c["correctas"], "Incorrectas": c["incorrectas"],
                  "Blancos": c["blancos"], "Puntaje": c["puntaje"], "Nota": c["nota"],
                  "Promedio": c["promedio"]})
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
    cols += ["Correctas", "Incorrectas", "Puntaje", "Nota", "Promedio"]
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph
    est_cab = ParagraphStyle("cab", fontName="Helvetica-Bold", fontSize=6.5 if detalle_cursos else 8,
                             leading=7.5 if detalle_cursos else 9, alignment=1)
    cab = [Paragraph({"Puesto": "Pto", "Aula": "Grado", "Promedio": "Prom. /20", "Nota": "Nota /20"}.get(x, x), est_cab) for x in cols]

    def _fmt(x, v):
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return "-"
        if x in cursos:
            return f"{float(v):.1f}"                  # nota del curso sobre 20
        if x == "Apellidos y Nombres":
            return str(v)[:40]
        if x in ("Nota", "Promedio"):
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
    sub = f"{sim.get('fecha', '')}  ·  {titulo_extra}  ·  Notas por curso sobre 20 · Puntaje máximo: {puntaje_maximo(sim):g}"
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
    data.append(["TOTAL (puntaje sobre 20)", "", res["correctas"], res["incorrectas"], res["blancos"],
                 f"{res['puntaje']:g}", f"{res['nota']:.2f}"])
    data.append(["PROMEDIO GENERAL (de los cursos)", "", "", "", "", "", f"{res['promedio']:.2f}"])
    t = Table(data, colWidths=[170, 50, 60, 65, 60, 55, 55])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTNAME", (0, -2), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3d1e6")),
        ("BACKGROUND", (0, -2), (-1, -1), colors.HexColor("#fde68a")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("ALIGN", (1, 0), (-1, -1), "CENTER")]))
    tw, th = t.wrapOn(c, ancho, alto)
    t.drawOn(c, (ancho - tw) / 2, y - 25 - th)
    y = y - 45 - th

    # Detalle de respuestas
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, y, "Detalle por pregunta (marcada / clave):  ✔ correcta   ✘ incorrecta   — en blanco")
    y -= 14
    validas = sorted(preguntas_validas(sim, hoja.get("grupo", ""))) \
        or list(range(1, n_preguntas(sim, hoja.get("grupo", "")) + 1))
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
                "Puntaje": c["puntaje"], "Correctas": c["correctas"], "Promedio": c["promedio"], "Nota": c["nota"],
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
    rel(2350, 150, 91, 26, NEGRO)                      # barrita de versión 2 (hoja con alternativa E)
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
            for j, ch in enumerate("ABCDE"):
                cx = omr.RESP_X5[col][j]
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
        val = preguntas_validas(sim, grupo) or None
        if val is not None:
            c.saveState()
            c.setFillColor(colors.Color(.85, .85, .85))
            c.setFillAlpha(0.62)
            for i_ in range(100):
                if (i_ + 1) not in val:
                    col_, fila_ = divmod(i_, omr.RESP_FILAS)
                    yy_ = omr.RESP_Y0 + omr.RESP_DY * fila_
                    c.rect(X(omr.RESP_X[col_][0] - 75), Y(yy_ + 38), X(omr.RESP_X[col_][3] + 45 - (omr.RESP_X[col_][0] - 75)), X(76), stroke=0, fill=1)
            c.restoreState()
        resp = h.get("respuestas", "")
        res = calificar(sim, h)
        for i in range(len(resp)):
            if val is not None and (i + 1) not in val:
                continue
            r_ = resp[i]
            k_ = clave[i] if i < len(clave) else ""
            if r_ in "ABCDE" and r_:
                cx, cy = omr.posicion_respuesta(i, "ABCDE".index(r_))
                disco(cx, cy, 19, TINTA)
                if k_ in "ABCDE" and k_ and k_ != anula_sim(sim):
                    aro(cx, cy, 31, VERDE if r_ == k_ else ROJO)
                    if r_ != k_:
                        kx, ky = omr.posicion_respuesta(i, "ABCDE".index(k_))
                        disco(kx, ky, 11, VERDE)
            elif r_ == "*":
                for j in range(5):
                    aro(*omr.posicion_respuesta(i, j), 30, NARANJA)
            elif k_ in "ABCDE" and k_ and k_ != anula_sim(sim):
                aro(*omr.posicion_respuesta(i, "ABCDE".index(k_)), 31, VERDE, 4)
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
              f"Puntaje: {fila['Puntaje']:g}/{puntaje_maximo(sim, hoja.get('grupo', '')):g}",
              f"Promedio general: {res['promedio']:.2f}/20", f"Puesto: {int(fila['Puesto'])} de {total}", ""]
    for cn, cv in res["cursos"].items():
        lineas.append(f"• {cn}: {cv['nota']:.1f}/20 ({cv['correctas']} correctas)")
    lineas += ["", "Gracias por su apoyo. 📚"]
    return "\n".join(lineas)


# ================================================================
# EXAMEN EN WORD: dos columnas, portada, número de página y QR
# ================================================================
def _png_qr(texto, modulo=14):
    """Imagen PNG (bytes) del QR de `texto`."""
    from PIL import Image
    m = _matriz_qr(texto)
    n = m.shape[0]
    im = Image.new("L", (n * modulo, n * modulo), 255)
    px = im.load()
    for f in range(n):
        for c_ in range(n):
            if m[f, c_]:
                for dy in range(modulo):
                    for dx in range(modulo):
                        px[c_ * modulo + dx, f * modulo + dy] = 0
    b = io.BytesIO()
    im.save(b, format="PNG")
    return b.getvalue()


# ================================================================
# PORTADA DE ALTA CALIDAD: franjas de color con escudos y contactos
# ================================================================
INSTITUCION_DEFECTO = {"coordinador": "948572481", "colegio": "084750071", "direccion": "", "web": "",
                       "lema": "Pioneros en la educación de calidad"}
COL_VINO, COL_ROJO, COL_ORO, COL_CREMA = (122, 15, 42), (196, 22, 28), (242, 183, 5), (253, 246, 227)


def _fmt_tel(t):
    d = re.sub(r"\D", "", str(t or ""))
    if len(d) == 9:
        return f"{d[:3]} {d[3:6]} {d[6:]}"
    return d or str(t or "")


def _vcard_institucion(inst):
    """Contenido del QR: tarjeta de contacto (el celular ofrece «guardar contacto»)."""
    lin = ["BEGIN:VCARD", "VERSION:3.0", "N:;Alternativo Yachay;;;", "FN:I.E.P. Alternativo Yachay",
           "ORG:Academia Preuniversitaria Yachay"]
    if inst.get("colegio"):
        lin.append("TEL;TYPE=WORK,VOICE:" + re.sub(r"\D", "", inst["colegio"]))
    if inst.get("coordinador"):
        lin.append("TEL;TYPE=CELL:" + re.sub(r"\D", "", inst["coordinador"]))
    if inst.get("direccion"):
        lin.append("ADR;TYPE=WORK:;;" + inst["direccion"] + ";;;;")
    if inst.get("web"):
        lin.append("URL:" + inst["web"])
    lin.append("NOTE:Coordinador academico: " + _fmt_tel(inst.get("coordinador")) +
               " / Celular del colegio: " + _fmt_tel(inst.get("colegio")))
    lin.append("END:VCARD")
    return "\n".join(lin)


def _fuente_pil(px):
    f = omr._fuente(int(px))
    if f is not None:
        return f
    from PIL import ImageFont
    try:
        return ImageFont.load_default(int(px))
    except Exception:
        return ImageFont.load_default()


def _degradado(w, h, c1, c2, diagonal=True):
    import numpy as np
    from PIL import Image
    x = np.linspace(0, 1, w)[None, :]
    y = np.linspace(0, 1, h)[:, None]
    t = (x * 0.75 + (1 - y) * 0.25) if diagonal else (x + y * 0)
    arr = np.zeros((h, w, 3), np.float32)
    for k in range(3):
        arr[:, :, k] = c1[k] + (c2[k] - c1[k]) * t
    return Image.fromarray(arr.clip(0, 255).astype("uint8"), "RGB")


def _sombra(im, desp=(10, 14), radio=18, alfa=120):
    from PIL import Image, ImageFilter
    a = im.getchannel("A").point(lambda v: v * alfa // 255)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(a)
    return sh.filter(ImageFilter.GaussianBlur(radio))


def _centrado(dib, txt, fuente, cx, y, color):
    w = dib.textlength(txt, font=fuente)
    dib.text((cx - w / 2.0, y), txt, font=fuente, fill=color)


def _franja_superior(inst=None, w=2480, h=830):
    """Franja de arriba: degradado vino→rojo, adornos dorados, los dos escudos, los nombres y la cinta del lema."""
    from PIL import Image, ImageDraw
    inst = inst or INSTITUCION_DEFECTO
    lema = str(inst.get("lema", "") or "").strip()
    cinta = 92 if lema else 0
    mh = h - 40 - cinta                                   # alto de la zona principal
    base = _degradado(w, h, COL_VINO, COL_ROJO).convert("RGBA")
    adorno = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(adorno)
    d.ellipse((w - 820, -480, w + 340, 640), fill=(242, 183, 5, 46))
    d.ellipse((w - 560, 250, w + 160, 940), fill=(255, 255, 255, 26))
    d.ellipse((-380, mh - 300, 460, mh + 440), fill=(255, 255, 255, 22))
    for k in range(-6, 26):
        x0 = k * 130
        d.line((x0, mh, x0 + mh * 0.58, 0), fill=(255, 255, 255, 14), width=3)
    base.alpha_composite(adorno)
    d = ImageDraw.Draw(base)
    aca = Image.open(io.BytesIO(base64.b64decode(_LOGO_ACA_HQ_B64))).convert("RGBA")
    col = Image.open(io.BytesIO(base64.b64decode(_LOGO_COL_HQ_B64))).convert("RGBA")
    aca = aca.resize((520, int(520 * aca.size[1] / aca.size[0])), Image.LANCZOS)
    col = col.resize((620, int(620 * col.size[1] / col.size[0])), Image.LANCZOS)
    ya, yc = (mh - aca.size[1]) // 2 + 6, (mh - col.size[1]) // 2 + 6
    base.alpha_composite(_sombra(aca), (150 + 8, ya + 12))
    base.alpha_composite(aca, (150, ya))
    xc = w - 150 - col.size[0]
    base.alpha_composite(_sombra(col), (xc + 8, yc + 12))
    base.alpha_composite(col, (xc, yc))
    d = ImageDraw.Draw(base)
    cx = (150 + 520 + xc) / 2.0
    y0 = (mh - 345) // 2 + 6
    _centrado(d, "ACADEMIA PREUNIVERSITARIA", _fuente_pil(44), cx, y0, (255, 255, 255))
    _centrado(d, "YACHAY", _fuente_pil(150), cx, y0 + 62, COL_ORO)
    d.rectangle((cx - 200, y0 + 262, cx + 200, y0 + 268), fill=(255, 255, 255, 230))
    _centrado(d, "I.E.P. ALTERNATIVO YACHAY", _fuente_pil(42), cx, y0 + 288, (255, 255, 255))
    if lema:                                                # cinta del lema, imponente, en dorado sobre vino
        c0 = mh
        cin = _degradado(w, cinta, (80, 8, 28), (122, 15, 42), diagonal=False).convert("RGBA")
        base.alpha_composite(cin, (0, c0))
        d = ImageDraw.Draw(base)
        d.rectangle((0, c0, w, c0 + 5), fill=COL_ORO + (255,))
        texto = lema.upper()
        f = _fuente_pil(54)
        sep = 14
        ancho_t = sum(d.textlength(ch, font=f) + sep for ch in texto) - sep
        x = (w - ancho_t) / 2.0
        for ch in texto:                                    # letras separadas = aspecto de lema institucional
            d.text((x, c0 + 14), ch, font=f, fill=COL_ORO)
            x += d.textlength(ch, font=f) + sep
        for lado in (-1, 1):                                # rombos dorados a los lados
            rx = (w / 2.0) + lado * (ancho_t / 2.0 + 70)
            d.polygon([(rx, c0 + cinta / 2 - 16), (rx + 16, c0 + cinta / 2), (rx, c0 + cinta / 2 + 16),
                       (rx - 16, c0 + cinta / 2)], fill=COL_ORO + (255,))
    d.rectangle((0, h - 40, w, h - 18), fill=COL_ORO + (255,))
    d.rectangle((0, h - 12, w, h), fill=(255, 255, 255, 255))
    b_ = io.BytesIO()
    base.convert("RGB").save(b_, format="PNG", optimize=True)
    return b_.getvalue()


def _franja_inferior(inst, w=2480, h=640):
    """Franja de abajo: QR con los datos del colegio y los teléfonos de contacto."""
    from PIL import Image, ImageDraw
    base = _degradado(w, h, COL_ROJO, COL_VINO).convert("RGBA")
    adorno = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(adorno)
    d.ellipse((w - 700, -280, w + 400, 760), fill=(242, 183, 5, 40))
    d.ellipse((-280, h - 240, 440, h + 380), fill=(255, 255, 255, 22))
    base.alpha_composite(adorno)
    d = ImageDraw.Draw(base)
    d.rectangle((0, 0, w, 12), fill=(255, 255, 255, 255))
    d.rectangle((0, 18, w, 40), fill=COL_ORO + (255,))
    qr = Image.open(io.BytesIO(_png_qr(_vcard_institucion(inst), modulo=12))).convert("RGBA")
    lado = 400
    qr = qr.resize((lado, lado), Image.NEAREST)
    cuadro = Image.new("RGBA", (lado + 60, lado + 60), (255, 255, 255, 255))
    mk = Image.new("L", cuadro.size, 0)
    ImageDraw.Draw(mk).rounded_rectangle((0, 0, cuadro.size[0] - 1, cuadro.size[1] - 1), radius=30, fill=255)
    cuadro.putalpha(mk)
    cuadro.alpha_composite(qr, (30, 30))
    qy = (h - cuadro.size[1]) // 2 + 22
    base.alpha_composite(_sombra(cuadro, (8, 12), 14, 110), (150 + 8, qy + 12))
    base.alpha_composite(cuadro, (150, qy))
    d = ImageDraw.Draw(base)
    x0 = 150 + cuadro.size[0] + 100
    d.text((x0, 112), "CONTÁCTANOS", font=_fuente_pil(54), fill=COL_ORO)
    d.rectangle((x0, 184, x0 + 290, 190), fill=(255, 255, 255, 230))
    y = 214
    for rot, val in (("Coordinador académico", inst.get("coordinador")), ("Celular del colegio", inst.get("colegio"))):
        if val:
            d.text((x0, y), rot, font=_fuente_pil(38), fill=(255, 224, 150))
            d.text((x0, y + 44), _fmt_tel(val), font=_fuente_pil(78), fill=(255, 255, 255))
            y += 160
    for extra in (inst.get("direccion"), inst.get("web")):
        if extra and y < h - 110:
            d.text((x0, y), str(extra)[:60], font=_fuente_pil(34), fill=(255, 255, 255))
            y += 48
    d.text((x0, h - 82), "Escanea el QR para guardar nuestros contactos", font=_fuente_pil(30), fill=(255, 224, 150))
    b_ = io.BytesIO()
    base.convert("RGB").save(b_, format="PNG", optimize=True)
    return b_.getvalue()


def _titulo_grande(titulo):
    """Título grande de la portada según el nombre de la evaluación."""
    t = str(titulo or "").lower()
    if t.startswith("semana"):
        return "EXAMEN SEMANAL"
    if t.startswith("simulacro"):
        return "SIMULACRO"
    if "bimestr" in t:
        return "EVALUACIÓN BIMESTRAL"
    if "final" in t:
        return "EVALUACIÓN FINAL"
    return "EXAMEN"


def formatear_examen_word(contenido, sim=None, portada=True, columnas=2, institucion=None,
                          titulo_grande=None, nivel_texto="", destino_texto=""):
    """Toma un examen en Word (.docx) y lo deja listo para imprimir, con calidad de academia de primer nivel:
    A4, dos columnas con línea separadora, imágenes ajustadas al ancho de la columna, cada pregunta junta,
    marco decorativo, encabezado con escudo, pie con contactos y número de página, y una portada a todo
    color con los dos escudos, título grande, cursos, datos del estudiante y QR con los contactos del colegio.
    Se edita el mismo documento (texto, fórmulas e imágenes se conservan). Devuelve (bytes, n_imágenes)."""
    import copy
    from docx import Document
    from docx.enum.table import WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Emu, Pt, RGBColor

    inst = {**INSTITUCION_DEFECTO, **(institucion or {})}
    doc = Document(io.BytesIO(contenido))
    titulo = (sim or {}).get("titulo") or "EXAMEN"
    fecha = (sim or {}).get("fecha", "")
    CRIMSON, VINO, DORADO = RGBColor(155, 27, 47), RGBColor(122, 15, 42), RGBColor(184, 134, 11)
    ESC = " · ".join(x for x in [f"Coordinación académica {_fmt_tel(inst.get('coordinador'))}" if inst.get("coordinador") else "",
                                 f"Colegio {_fmt_tel(inst.get('colegio'))}" if inst.get("colegio") else ""] if x)

    def _antes(sp, nuevo, antes_de):
        for tag in antes_de:
            e = sp.find(qn(tag))
            if e is not None:
                e.addprevious(nuevo)
                return
        sp.append(nuevo)

    def _columnas(sec, n):
        sp = sec._sectPr
        cols = sp.find(qn("w:cols"))
        if cols is None:
            cols = OxmlElement("w:cols")
            _antes(sp, cols, ["w:formProt", "w:vAlign", "w:noEndnote", "w:titlePg", "w:textDirection", "w:bidi",
                              "w:rtlGutter", "w:docGrid", "w:printerSettings"])
        for k in list(cols.attrib):
            del cols.attrib[k]
        for h in list(cols):
            cols.remove(h)
        cols.set(qn("w:num"), str(n))
        cols.set(qn("w:space"), "567")
        if n > 1:
            cols.set(qn("w:sep"), "1")

    # ---- 1) A4, márgenes y columnas ----
    for sec in doc.sections:
        sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
        sec.left_margin = sec.right_margin = Cm(1.8)
        sec.top_margin, sec.bottom_margin = Cm(2.5), Cm(2.1)
        sec.header_distance, sec.footer_distance = Cm(1.15), Cm(1.0)
        _columnas(sec, columnas)
    ancho_col = int((Cm(21.0) - Cm(3.6) - Cm(1.0) * (columnas - 1)) / columnas)

    # ---- 2) imágenes flotantes -> en línea ----
    WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
    for anc in list(doc.element.body.iter("{%s}anchor" % WP)):
        try:
            inl = OxmlElement("wp:inline")
            for k in ("distT", "distB", "distL", "distR"):
                inl.set(k, "0")
            for tag in ("wp:extent", "wp:effectExtent", "wp:docPr", "wp:cNvGraphicFramePr", "a:graphic"):
                e = anc.find(qn(tag))
                if e is not None:
                    inl.append(copy.deepcopy(e))
            anc.getparent().replace(anc, inl)
        except Exception:
            pass
    # ---- 3) imágenes y tablas al ancho de la columna ----
    n_img = 0
    for shp in doc.inline_shapes:
        n_img += 1
        if shp.width and shp.width > ancho_col:
            r_ = ancho_col / float(shp.width)
            shp.height = int(shp.height * r_)
            shp.width = ancho_col
    for tbl in doc.tables:
        tblPr = tbl._tbl.tblPr
        w = tblPr.find(qn("w:tblW"))
        if w is None:
            w = OxmlElement("w:tblW")
            _antes(tblPr, w, ["w:jc", "w:tblCellSpacing", "w:tblInd", "w:tblBorders", "w:shd", "w:tblLayout",
                              "w:tblCellMar", "w:tblLook", "w:tblCaption", "w:tblDescription"])
        w.set(qn("w:type"), "pct")
        w.set(qn("w:w"), "5000")
        tbl.autofit = True

    # ---- 3b) cada pregunta se mantiene junta ----
    ini_preg = re.compile(r"^\s*\d{1,3}\s*[\.\)\-]\s+")
    pars = list(doc.paragraphs)
    marcas_ini = [i for i, pa in enumerate(pars) if ini_preg.match(pa.text or "")]
    for a_, b_ in zip(marcas_ini, marcas_ini[1:] + [len(pars)]):
        bloque = pars[a_:b_]
        if len(bloque) > 14:
            continue
        for k_, pa in enumerate(bloque):
            pa.paragraph_format.keep_together = True
            if k_ < len(bloque) - 1:
                pa.paragraph_format.keep_with_next = True

    # ---- ayudantes de formato ----
    def _sombrear(cel, hexcolor):
        sh = OxmlElement("w:shd")
        sh.set(qn("w:val"), "clear")
        sh.set(qn("w:color"), "auto")
        sh.set(qn("w:fill"), hexcolor)
        cel._tc.get_or_add_tcPr().append(sh)

    def _bordes(tabla, **lados):
        tb = OxmlElement("w:tblBorders")
        for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
            b = OxmlElement("w:" + lado)
            val, sz, color = lados.get(lado, ("nil", "0", "auto"))
            b.set(qn("w:val"), val)
            b.set(qn("w:sz"), sz)
            b.set(qn("w:space"), "0")
            b.set(qn("w:color"), color)
            tb.append(b)
        _antes(tabla._tbl.tblPr, tb, ["w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook", "w:tblCaption", "w:tblDescription"])

    def _ancho_tabla(tabla, cm_total, cms):
        tblPr = tabla._tbl.tblPr
        w = tblPr.find(qn("w:tblW"))
        if w is None:
            w = OxmlElement("w:tblW")
            _antes(tblPr, w, ["w:jc", "w:tblCellSpacing", "w:tblInd", "w:tblBorders", "w:shd", "w:tblLayout",
                              "w:tblCellMar", "w:tblLook"])
        w.set(qn("w:type"), "dxa")
        w.set(qn("w:w"), str(int(Cm(cm_total).twips)))
        tabla.autofit = False
        for fila in tabla.rows:
            for c_, cm in zip(fila.cells, cms):
                c_.width = Cm(cm)

    def _espaciado(run, twips):
        rPr = run._r.get_or_add_rPr()
        e = OxmlElement("w:spacing")
        e.set(qn("w:val"), str(twips))
        _antes(rPr, e, ["w:w", "w:kern", "w:position", "w:sz", "w:szCs", "w:highlight", "w:u", "w:effect"])

    def _ancla_pagina(run, abajo=False):
        """Convierte la imagen del run en una imagen flotante pegada al borde de la página (detrás del texto)."""
        inl = run._r.find(".//" + qn("wp:inline"))
        anc = OxmlElement("wp:anchor")
        for k, v in (("distT", "0"), ("distB", "0"), ("distL", "0"), ("distR", "0"), ("simplePos", "0"),
                     ("relativeHeight", "1"), ("behindDoc", "1"), ("locked", "0"), ("layoutInCell", "1"),
                     ("allowOverlap", "1")):
            anc.set(k, v)
        sp = OxmlElement("wp:simplePos")
        sp.set("x", "0")
        sp.set("y", "0")
        anc.append(sp)
        ph = OxmlElement("wp:positionH")
        ph.set("relativeFrom", "page")
        o1 = OxmlElement("wp:posOffset")
        o1.text = "0"
        ph.append(o1)
        pv = OxmlElement("wp:positionV")
        pv.set("relativeFrom", "page")
        if abajo:
            al = OxmlElement("wp:align")
            al.text = "bottom"
            pv.append(al)
        else:
            o2 = OxmlElement("wp:posOffset")
            o2.text = "0"
            pv.append(o2)
        anc.append(ph)
        anc.append(pv)
        anc.append(copy.deepcopy(inl.find(qn("wp:extent"))))
        ee = OxmlElement("wp:effectExtent")
        for k in ("l", "t", "r", "b"):
            ee.set(k, "0")
        anc.append(ee)
        anc.append(OxmlElement("wp:wrapNone"))
        for tag in ("wp:docPr", "wp:cNvGraphicFramePr", "a:graphic"):
            e = inl.find(qn(tag))
            if e is not None:
                anc.append(copy.deepcopy(e))
        inl.getparent().replace(inl, anc)

    # ---- 4) PORTADA ----
    if portada:
        cuerpo = doc.element.body
        nuevos = []
        ancho_c = 17.0                                                     # ancho útil de la portada (cm)

        def _p(texto="", size=11, bold=False, color=None, alinea=WD_ALIGN_PARAGRAPH.CENTER, antes=0, despues=4,
               fuente="Arial", espaciado=0):
            p = doc.add_paragraph()
            p.alignment = alinea
            p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(antes), Pt(despues)
            if texto:
                r = p.add_run(texto)
                r.font.size, r.font.bold, r.font.name = Pt(size), bold, fuente
                if color is not None:
                    r.font.color.rgb = color
                if espaciado:
                    _espaciado(r, espaciado)
            nuevos.append(p._p)
            return p

        # franjas de color a página completa (arriba y abajo)
        p0 = _p("", despues=0)
        p0.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        p0.paragraph_format.line_spacing = Cm(6.55 if str(inst.get("lema", "")).strip() else 5.75)
        r_top = p0.add_run()
        r_top.add_picture(io.BytesIO(_franja_superior(inst)), width=Cm(21.0))
        _ancla_pagina(r_top, abajo=False)
        r_bot = p0.add_run()
        r_bot.add_picture(io.BytesIO(_franja_inferior(inst)), width=Cm(21.0))
        _ancla_pagina(r_bot, abajo=True)

        _p(titulo_grande or _titulo_grande(titulo), 40, True, CRIMSON, antes=8, despues=0, fuente="Arial Black")
        if nivel_texto:
            _p(str(nivel_texto).upper(), 22, True, DORADO, despues=4, espaciado=60)
        # barra de color
        bar = doc.add_table(rows=1, cols=3)
        bar.alignment = WD_TABLE_ALIGNMENT.CENTER
        bar.rows[0].height = Cm(0.22)
        bar.rows[0].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
        for cel, hexc in zip(bar.rows[0].cells, ("9B1B2F", "F2B705", "7A0F2A")):
            _sombrear(cel, hexc)
            cel.paragraphs[0].paragraph_format.space_after = Pt(0)
            rr = cel.paragraphs[0].add_run("")
            rr.font.size = Pt(1)
        _bordes(bar)
        _ancho_tabla(bar, ancho_c, (9.0, 5.0, 3.0))
        nuevos.append(bar._tbl)
        _p(str(titulo), 28, True, RGBColor(35, 35, 35), antes=8, despues=6)

        # datos clave: fecha / dirigido a / preguntas
        filas = []
        if sim:
            for c_ in cursos_union(sim):
                filas.append((c_["nombre"], f"{c_['desde']} – {c_['hasta']}", str(c_["hasta"] - c_["desde"] + 1)))
        chips = [("FECHA", fecha)] if fecha else []
        if destino_texto:
            chips.append(("DIRIGIDO A", destino_texto))
        if filas:
            chips.append(("PREGUNTAS", str(sum(int(f_[2]) for f_ in filas))))
        if chips:
            tc = doc.add_table(rows=1, cols=len(chips))
            tc.alignment = WD_TABLE_ALIGNMENT.CENTER
            for cel, (lab, val) in zip(tc.rows[0].cells, chips):
                _sombrear(cel, "FDF6E3")
                cel.text = ""
                p1 = cel.paragraphs[0]
                p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p1.paragraph_format.space_before, p1.paragraph_format.space_after = Pt(4), Pt(0)
                r1 = p1.add_run(lab)
                r1.font.size, r1.font.bold, r1.font.name = Pt(8.5), True, "Arial"
                r1.font.color.rgb = RGBColor(110, 110, 110)
                p2 = cel.add_paragraph()
                p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p2.paragraph_format.space_before, p2.paragraph_format.space_after = Pt(0), Pt(5)
                r2 = p2.add_run(str(val))
                r2.font.size, r2.font.bold, r2.font.name = Pt(17), True, "Arial"
                r2.font.color.rgb = CRIMSON
            _bordes(tc, insideV=("single", "36", "FFFFFF"))
            _ancho_tabla(tc, ancho_c, tuple(ancho_c / len(chips) for _ in chips))
            nuevos.append(tc._tbl)
        # cursos
        if filas:
            _p("CONTENIDO DEL EXAMEN", 10.5, True, CRIMSON, antes=10, despues=3, espaciado=40)
            datos_t = [("Curso", "Preguntas", "Cantidad")] + filas + [("TOTAL", "", str(sum(int(f_[2]) for f_ in filas)))]
            t = doc.add_table(rows=len(datos_t), cols=3)
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
            compacto = len(filas) > 6
            for i_, fila in enumerate(datos_t):
                for j_, val in enumerate(fila):
                    cel = t.cell(i_, j_)
                    cel.text = ""
                    pr = cel.paragraphs[0]
                    pr.alignment = WD_ALIGN_PARAGRAPH.LEFT if j_ == 0 else WD_ALIGN_PARAGRAPH.CENTER
                    pr.paragraph_format.space_before = pr.paragraph_format.space_after = Pt(1.5 if compacto else 2.5)
                    rr = pr.add_run(str(val))
                    rr.font.size, rr.font.name = Pt(9.5 if compacto else 10.5), "Arial"
                    if i_ == 0:
                        _sombrear(cel, "9B1B2F")
                        rr.font.bold, rr.font.color.rgb = True, RGBColor(255, 255, 255)
                    elif i_ == len(datos_t) - 1:
                        _sombrear(cel, "F2B705")
                        rr.font.bold = True
                    else:
                        _sombrear(cel, "FDF6E3" if i_ % 2 else "FFFFFF")
            _bordes(t, top=("single", "8", "9B1B2F"), bottom=("single", "8", "9B1B2F"), insideH=("single", "4", "E3D9C0"))
            _ancho_tabla(t, ancho_c, (9.0, 4.5, 3.5))
            nuevos.append(t._tbl)
        # datos del estudiante
        _p("DATOS DEL ESTUDIANTE", 10.5, True, CRIMSON, antes=10, despues=5, espaciado=40)
        for partes in ((("Apellidos y nombres:", 52),), (("DNI:", 18), ("Aula / Grado:", 22))):
            pp = _p("", alinea=WD_ALIGN_PARAGRAPH.LEFT, despues=7)
            for k_, (rot, largo) in enumerate(partes):
                r1 = pp.add_run(("      " if k_ else "") + rot + " ")
                r1.font.size, r1.font.name, r1.font.bold = Pt(10.5), "Arial", True
                r2 = pp.add_run("_" * largo)
                r2.font.size, r2.font.name = Pt(10.5), "Arial"
        # indicaciones (si hay espacio)
        if len(filas) <= 6:
            _p("INDICACIONES", 10.5, True, CRIMSON, antes=8, despues=3, espaciado=40)
            for txt in ("Usa lápiz 2B o lapicero negro y rellena el círculo por completo en la hoja de respuestas.",
                        "Marca una sola alternativa por pregunta. Si te equivocas, borra bien la marca anterior.",
                        "Marca tu DNI (8 dígitos), la fecha y tu área en la hoja de respuestas. No la dobles ni la manches."):
                pi = _p("", alinea=WD_ALIGN_PARAGRAPH.LEFT, despues=1.5)
                ri = pi.add_run("•  " + txt)
                ri.font.size, ri.font.name = Pt(9.5), "Arial"
        # fin de la portada: sección propia de una columna, sin numeración
        sp_fin = copy.deepcopy(doc.sections[-1]._sectPr)
        for tag in ("w:headerReference", "w:footerReference", "w:pgNumType", "w:pgBorders"):
            for e in sp_fin.findall(qn(tag)):
                sp_fin.remove(e)
        mar = sp_fin.find(qn("w:pgMar"))
        if mar is not None:
            for k, v in (("top", 0.8), ("bottom", 0.8), ("left", 2.0), ("right", 2.0), ("header", 0.4), ("footer", 0.4)):
                mar.set(qn("w:" + k), str(int(Cm(v).twips)))
        cols_ = sp_fin.find(qn("w:cols"))
        if cols_ is not None:
            for k in list(cols_.attrib):
                del cols_.attrib[k]
            for h in list(cols_):
                cols_.remove(h)
            cols_.set(qn("w:num"), "1")
            cols_.set(qn("w:space"), "567")
        pfin = OxmlElement("w:p")
        ppr = OxmlElement("w:pPr")
        ppr.append(sp_fin)
        pfin.append(ppr)
        nuevos.append(pfin)
        primero = cuerpo[0]
        for e in nuevos:
            primero.addprevious(e)

    # ---- 5) marco decorativo, encabezado y pie (páginas del examen) ----
    def _campo(run, instr):
        a = OxmlElement("w:fldChar")
        a.set(qn("w:fldCharType"), "begin")
        it = OxmlElement("w:instrText")
        it.set(qn("xml:space"), "preserve")
        it.text = instr
        b = OxmlElement("w:fldChar")
        b.set(qn("w:fldCharType"), "separate")
        t = OxmlElement("w:t")
        t.text = "1"
        c_ = OxmlElement("w:fldChar")
        c_.set(qn("w:fldCharType"), "end")
        for e in (a, it, b, t, c_):
            run._r.append(e)

    def _tabs(par, derecha):
        ts = par.paragraph_format.tab_stops
        for pos in (4680, 9360, 4513, 9026, 4252, 8504):
            ts.add_tab_stop(Emu(pos * 635), WD_TAB_ALIGNMENT.CLEAR)
        ts.add_tab_stop(Cm(derecha), WD_TAB_ALIGNMENT.RIGHT)

    def _borde_parrafo(par, lado, sz, color, space="2"):
        pb = OxmlElement("w:pBdr")
        bt = OxmlElement("w:" + lado)
        for k, v in (("val", "single"), ("sz", sz), ("space", space), ("color", color)):
            bt.set(qn("w:" + k), v)
        pb.append(bt)
        _antes(par._p.get_or_add_pPr(), pb, ["w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
                                             "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
                                             "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
                                             "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
                                             "w:textDirection", "w:textAlignment", "w:textboxTightWrap",
                                             "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr",
                                             "w:pPrChange"])

    sec = doc.sections[-1]
    # marco de la página
    pgb = OxmlElement("w:pgBorders")
    pgb.set(qn("w:offsetFrom"), "page")
    for lado in ("top", "left", "bottom", "right"):
        b = OxmlElement("w:" + lado)
        for k, v in (("val", "thickThinSmallGap"), ("sz", "18"), ("space", "22"), ("color", "9B1B2F")):
            b.set(qn("w:" + k), v)
        pgb.append(b)
    _antes(sec._sectPr, pgb, ["w:lnNumType", "w:pgNumType", "w:cols", "w:formProt", "w:vAlign", "w:noEndnote",
                              "w:titlePg", "w:textDirection", "w:bidi", "w:rtlGutter", "w:docGrid"])
    if portada:
        pg = OxmlElement("w:pgNumType")
        pg.set(qn("w:start"), "1")
        _antes(sec._sectPr, pg, ["w:cols", "w:formProt", "w:vAlign", "w:noEndnote", "w:titlePg", "w:textDirection",
                                 "w:bidi", "w:rtlGutter", "w:docGrid"])
    sec.header.is_linked_to_previous = False
    sec.footer.is_linked_to_previous = False
    ancho_txt = 17.4
    hp = sec.header.paragraphs[0]
    hp.text = ""
    _tabs(hp, ancho_txt)
    rl = hp.add_run()
    rl.add_picture(io.BytesIO(base64.b64decode(_LOGO_ACA_HQ_B64)), width=Cm(0.95))
    r_a = hp.add_run("  ACADEMIA PREUNIVERSITARIA YACHAY")
    r_a.font.size, r_a.font.name, r_a.font.bold = Pt(9), "Arial", True
    r_a.font.color.rgb = CRIMSON
    r_b = hp.add_run("\t" + str(titulo).upper() + (f"  ·  {destino_texto}" if destino_texto else ""))
    r_b.font.size, r_b.font.name, r_b.font.bold = Pt(9), "Arial", True
    r_b.font.color.rgb = RGBColor(90, 90, 90)
    _borde_parrafo(hp, "bottom", "18", "9B1B2F", "4")
    fp = sec.footer.paragraphs[0]
    fp.text = ""
    _tabs(fp, ancho_txt)
    r0 = fp.add_run(("I.E.P. Alternativo Yachay  ·  " + ESC) if ESC else "I.E.P. Alternativo Yachay")
    r0.font.size, r0.font.name = Pt(8), "Arial"
    r0.font.color.rgb = RGBColor(110, 110, 110)
    r1 = fp.add_run("\tPágina ")
    r1.font.size, r1.font.name, r1.font.bold = Pt(10), "Arial", True
    r1.font.color.rgb = CRIMSON
    r2 = fp.add_run()
    r2.font.size, r2.font.name, r2.font.bold = Pt(11), "Arial", True
    r2.font.color.rgb = CRIMSON
    _campo(r2, "PAGE")
    _borde_parrafo(fp, "top", "6", "F2B705", "4")
    if str(inst.get("lema", "")).strip():
        pl2 = sec.footer.add_paragraph()
        pl2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pl2.paragraph_format.space_before, pl2.paragraph_format.space_after = Pt(1), Pt(0)
        rl2 = pl2.add_run("◆  " + str(inst["lema"]).upper() + "  ◆")
        rl2.font.size, rl2.font.name, rl2.font.bold = Pt(7.5), "Arial", True
        rl2.font.color.rgb = DORADO
        _espaciado(rl2, 30)
    try:
        z = doc.settings.element.find(qn("w:zoom"))
        if z is not None and z.get(qn("w:percent")) is None:
            z.set(qn("w:percent"), "100")
    except Exception:
        pass
    out = io.BytesIO()
    doc.save(out)
    return out.getvalue(), n_img


# ================================================================
# ARCHIVO DE EXÁMENES (Word) por nivel y grupo / grado
# ================================================================
EXAMENES_DIR = "examenes_archivo"
NIVELES_EX = ["Preuniversitario", "Primaria", "Secundaria"]
DESTINOS_EX = {
    "Preuniversitario": ["Grupo AB", "Grupo CD", "Área A", "Área B", "Área C", "Área D", "Todos los grupos"],
    "Primaria": [f"{i}.° grado" for i in range(1, 7)] + ["Todos los grados"],
    "Secundaria": [f"{i}.° año" for i in range(1, 6)] + ["Todos los años"],
}
MIME_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def _slug(t, n=40):
    import unicodedata
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_")[:n] or "x"


def destino_defecto(sim):
    """(nivel, destino) sugeridos según cómo se configuró el simulacro."""
    mod = sim.get("modalidad", "")
    if sim.get("sin_area"):
        return {"PRIMARIA": "Primaria", "SECUNDARIA": "Secundaria"}.get(mod, "Preuniversitario"), None
    gs = set(grupos_sim(sim))
    if gs == {"A", "B"}:
        return "Preuniversitario", "Grupo AB"
    if gs == {"C", "D"}:
        return "Preuniversitario", "Grupo CD"
    if len(gs) == 1:
        return "Preuniversitario", f"Área {next(iter(gs))}"
    return "Preuniversitario", "Todos los grupos"


def guardar_en_archivo(datos, sim, nivel, destino, contenido, titulo=None, huella=None):
    """Guarda el examen en el archivo (carpeta local + copia en Drive) y lo registra en el índice.
    `huella` identifica el trabajo (archivo subido + opciones): el Word generado nunca es idéntico byte a
    byte, así que no sirve para saber si ya se guardó."""
    import hashlib
    sha = huella or hashlib.md5(contenido).hexdigest()
    sid = sim.get("id", "")
    nombre = (f"EXAMEN__{_slug(nivel)}__{_slug(destino)}__{_fecha_iso(sim.get('fecha', ''))}__"
              f"{_slug(titulo or sim.get('titulo', ''))}__{_slug(sid, 24)}.docx")
    idx = datos.setdefault("examenes", {})
    if idx.get(nombre, {}).get("sha") == sha:
        return nombre, False                               # ya está igual: no se vuelve a guardar
    Path(EXAMENES_DIR).mkdir(exist_ok=True)
    for nm, m in list(idx.items()):                         # una sola copia por simulacro
        if sid and m.get("simulacro_id") == sid and nm != nombre:
            try:
                (Path(EXAMENES_DIR) / nm).unlink()
            except Exception:
                pass
            idx.pop(nm, None)
    (Path(EXAMENES_DIR) / nombre).write_bytes(contenido)
    en_drive = False
    if _HOOKS.get("backup_archivo"):
        try:
            en_drive = bool(_HOOKS["backup_archivo"](nombre, contenido, MIME_DOCX))
        except Exception:
            en_drive = False
    idx[nombre] = {"titulo": titulo or sim.get("titulo", ""), "fecha": sim.get("fecha", ""), "nivel": nivel,
                   "destino": destino, "simulacro_id": sid, "sha": sha, "en_drive": en_drive,
                   "creado": datetime.now().isoformat(timespec="seconds"),
                   "creado_por": st.session_state.get("usuario_actual", "")}
    guardar_datos(datos)
    return nombre, True


def _bytes_examen(nombre):
    f = Path(EXAMENES_DIR) / nombre
    if f.exists():
        return f.read_bytes()
    if _HOOKS.get("bajar_archivo"):
        try:
            b = _HOOKS["bajar_archivo"](nombre)
            if b:
                Path(EXAMENES_DIR).mkdir(exist_ok=True)
                f.write_bytes(b)
                return b
        except Exception:
            pass
    return None


def _tab_examenes(datos):
    st.subheader("📁 Archivo de exámenes")
    st.caption("Cada examen que armas en Word queda guardado aquí, ordenado por nivel y por grupo o grado. "
               "También se guarda una copia en Drive.")
    idx = datos.get("examenes", {})
    f1, f2 = st.columns(2)
    niv = f1.selectbox("Nivel:", ["Todos"] + NIVELES_EX, key="simy_ex_niv")
    dests = ["Todos"] + (DESTINOS_EX[niv] if niv != "Todos" else sorted({d for v in DESTINOS_EX.values() for d in v}))
    des = f2.selectbox("Grupo o grado:", dests, key="simy_ex_des")
    items = [(n, m) for n, m in idx.items()
             if (niv == "Todos" or m.get("nivel") == niv) and (des == "Todos" or m.get("destino") == des)]
    items.sort(key=lambda t: (t[1].get("fecha_iso") or _fecha_iso(t[1].get("fecha", "")), t[1].get("creado", "")), reverse=True)
    if not items:
        st.info("Todavía no hay exámenes en esta lista. Arma uno en ⚙️ Configurar → «📝 Armar el examen en Word».")
    else:
        st.dataframe(pd.DataFrame([{"Evaluación": m.get("titulo", ""), "Nivel": m.get("nivel", ""),
                                    "Grupo o grado": m.get("destino", ""), "Fecha": m.get("fecha", ""),
                                    "En Drive": "☁️ Sí" if m.get("en_drive") else "—"} for _, m in items]),
                     use_container_width=True, hide_index=True)
        elegido = st.selectbox("Elige un examen:", [n for n, _ in items], key="simy_ex_sel",
                               format_func=lambda n: f"{idx[n].get('titulo', '')} — {idx[n].get('destino', '')} — {idx[n].get('fecha', '')}")
        b = _bytes_examen(elegido)
        c1, c2, c3 = st.columns(3)
        if b:
            c1.download_button("⬇️ Descargar (Word)", b, elegido.split("__")[-2] + ".docx" if False else
                               "Examen_" + _slug(idx[elegido].get("titulo", ""), 30) + "_" + _slug(idx[elegido].get("destino", ""), 20) + ".docx",
                               MIME_DOCX, key="simy_ex_dl", type="primary")
        else:
            c1.warning("No se encontró el archivo. Si se reinició el sistema, vuelve a armar el examen.")
        if len(items) > 1:
            import zipfile
            zb = io.BytesIO()
            with zipfile.ZipFile(zb, "w", zipfile.ZIP_DEFLATED) as z:
                for n, m in items:
                    bb = _bytes_examen(n)
                    if bb:
                        z.writestr(f"{m.get('nivel', '')}/{m.get('destino', '')}/{_slug(m.get('titulo', ''), 30)}_{_fecha_iso(m.get('fecha', ''))}.docx", bb)
            c2.download_button("📦 Todos los de esta lista (ZIP)", zb.getvalue(), "Examenes.zip", "application/zip", key="simy_ex_zip")
        if not _HOOKS["puede_borrar"] or _HOOKS["puede_borrar"]():
            ok = c3.checkbox("Confirmo que quiero quitarlo", key="simy_ex_ok")
            if ok and c3.button("🗑️ Quitar del archivo", key="simy_ex_del"):
                try:
                    (Path(EXAMENES_DIR) / elegido).unlink()
                except Exception:
                    pass
                idx.pop(elegido, None)
                guardar_datos(datos)
                st.success("Quitado del archivo.")
                st.rerun()
    with st.expander("➕ Guardar en el archivo un examen que ya tengo hecho (sin cambiarlo)"):
        up = st.file_uploader("Examen en Word (.docx):", type=["docx"], key="simy_ex_up")
        g1, g2, g3, g4 = st.columns(4)
        n2 = g1.selectbox("Nivel:", NIVELES_EX, key="simy_ex_n2")
        d2 = g2.selectbox("Grupo o grado:", DESTINOS_EX[n2], key="simy_ex_d2")
        t2 = g3.text_input("Nombre del examen:", key="simy_ex_t2")
        f2_ = g4.text_input("Fecha (dd/mm/aaaa):", datetime.now().strftime("%d/%m/%Y"), key="simy_ex_f2")
        if up is not None and t2.strip() and st.button("💾 Guardar en el archivo", key="simy_ex_save2"):
            fake = {"id": "manual_" + uuid.uuid4().hex[:6], "titulo": t2.strip(), "fecha": f2_}
            guardar_en_archivo(datos, fake, n2, d2, up.getvalue(), t2.strip())
            st.success("Guardado en el archivo.")
            st.rerun()


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


# ================================================================
# RECONOCIMIENTO DE NOMBRES ESCRITOS A MANO (para hojas sin DNI o con DNI mal marcado)
# ================================================================
_OCR = {"motor": None, "intentado": False}
_PROMPT_NOMBRE = ("La imagen muestra los recuadros APELLIDOS y NOMBRES de una hoja de respuestas, escritos a mano en "
                  "mayúsculas por un estudiante peruano. Transcríbelos tal como se leen; no inventes letras y, si una "
                  "es dudosa, da tu mejor lectura. Responde SOLO con JSON: {\"apellidos\": \"...\", \"nombres\": \"...\"}. "
                  "Si un recuadro está vacío, usa \"\".")


def ocr_instalado():
    import importlib.util
    return importlib.util.find_spec("rapidocr_onnxruntime") is not None


def _motor_ocr():
    """Motor de reconocimiento de letra (se carga una sola vez, la primera vez que se necesita)."""
    if not _OCR["intentado"]:
        _OCR["intentado"] = True
        try:
            from rapidocr_onnxruntime import RapidOCR
            _OCR["motor"] = RapidOCR()
        except Exception:
            _OCR["motor"] = None
    return _OCR["motor"]


def _clave_ia():
    """Clave de la API de Claude (opcional): en la variable ANTHROPIC_API_KEY o en los secretos de Streamlit."""
    import os
    k = os.environ.get("ANTHROPIC_API_KEY", "")
    if not k:
        try:
            k = str(st.secrets.get("ANTHROPIC_API_KEY", ""))
        except Exception:
            k = ""
    return k.strip()


def reconocimiento_disponible():
    return bool(_clave_ia()) or ocr_instalado()


def _tiene_tinta(c):
    """¿El recuadro tiene algo escrito? (distingue letras de la raya punteada y el borde)."""
    import cv2
    import numpy as np
    if c is None or c.size == 0:
        return False
    g = c if c.ndim == 2 else cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
    g = g[8:-8, 14:-14] if g.shape[0] > 30 and g.shape[1] > 60 else g
    fondo = cv2.medianBlur(g, 31)
    dif = cv2.subtract(fondo, g)
    return float((dif > 55).mean()) > 0.012


def _nombre_con_ia(crops):
    """Pide a Claude que lea los dos recuadros. Devuelve 'APELLIDOS NOMBRES' o ''."""
    import cv2
    import numpy as np
    import urllib.request
    key = _clave_ia()
    if not key:
        return ""
    apilado = np.vstack([c if c.ndim == 2 else cv2.cvtColor(c, cv2.COLOR_BGR2GRAY) for c in crops])
    apilado = cv2.resize(apilado, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_AREA)
    ok, buf = cv2.imencode(".jpg", apilado, [cv2.IMWRITE_JPEG_QUALITY, 82])
    cuerpo = {"model": "claude-haiku-4-5-20251001", "max_tokens": 200,
              "messages": [{"role": "user", "content": [
                  {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                               "data": base64.b64encode(buf.tobytes()).decode()}},
                  {"type": "text", "text": _PROMPT_NOMBRE}]}]}
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(cuerpo).encode(),
                                 headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                                          "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        resp = json.loads(r.read().decode())
    texto = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")
    m = re.search(r"\{.*\}", texto, re.S)
    if not m:
        return ""
    d = json.loads(m.group(0))
    return f"{d.get('apellidos', '')} {d.get('nombres', '')}".strip()


def reconocer_nombre(crops):
    """Lee el nombre escrito a mano. `crops` = [recuadro de apellidos, recuadro de nombres] (imágenes grises).
    Usa la IA de Claude si hay clave configurada; si no (o si falla), el motor local. Devuelve (texto, motor)."""
    import cv2
    crops = [c for c in crops if _tiene_tinta(c)]
    if not crops:
        return "", ""
    if _clave_ia():
        try:
            t = _nombre_con_ia(crops)
            if t:
                return t, "ia"
        except Exception:
            pass
    m = _motor_ocr()
    if m is None:
        return "", ""
    partes = []
    for c in crops:
        try:
            res, _ = m(cv2.cvtColor(c, cv2.COLOR_GRAY2BGR) if c.ndim == 2 else c)
            if res:
                partes.append(" ".join(x[1] for x in res))
        except Exception:
            continue
    return " ".join(partes).strip(), "ocr"


_DIG2LET = str.maketrans({"0": "O", "1": "I", "2": "Z", "3": "E", "4": "A", "5": "S", "6": "G", "7": "T", "8": "B", "9": "G"})


def _norm_nombre(t):
    import unicodedata
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode().upper().translate(_DIG2LET)
    return re.sub(r"\s+", " ", re.sub(r"[^A-Z ]", " ", t)).strip()


def _ratio(a, b):
    import difflib
    return difflib.SequenceMatcher(None, a, b).ratio()


def _score_nombre(o_tok, o_all, c_tok, c_all):
    if not o_tok or not c_tok:
        return 0.0
    lo = float(sum(len(t) for t in o_tok))
    lc = float(sum(len(t) for t in c_tok))
    P = sum(max(_ratio(ot, ct) for ct in c_tok) * len(ot) for ot in o_tok) / lo      # lo escrito está en la matrícula
    C = sum(max(_ratio(ct, ot) for ot in o_tok) * len(ct) for ct in c_tok) / lc      # lo de la matrícula está en lo escrito
    return 0.55 * P + 0.25 * C + 0.20 * _ratio(o_all, c_all)


def sugerir_por_nombre(texto, mat, pref=None, top=3):
    """Compara el nombre leído con la matrícula. Devuelve [(seguridad 0-1, dni, nombre)], de mejor a peor.
    Se busca primero entre los alumnos del grupo (`pref`) y, si ahí no hay una coincidencia clara, en todos."""
    o_all = _norm_nombre(texto)
    o_tok = [t for t in o_all.split() if len(t) >= 2]
    if sum(len(t) for t in o_tok) < 4:
        return []

    def _buscar(pool):
        cand = []
        for d in pool:
            c_all = _norm_nombre(mat[d]["nombre"])
            cand.append((d, c_all, c_all.split()))
        # filtro rápido para no comparar a todos con todo
        pre = sorted(cand, key=lambda t: -__import__("difflib").SequenceMatcher(None, o_all, t[1]).quick_ratio())[:60]
        sc = [(_score_nombre(o_tok, o_all, c_tok, c_all), d) for d, c_all, c_tok in pre]
        sc.sort(reverse=True)
        return [(round(s, 3), d, mat[d]["nombre"]) for s, d in sc[:top]]

    res = []
    if pref:
        res = _buscar([d for d in mat if d in pref])
    if not res or res[0][0] < 0.62:
        res_all = _buscar(list(mat))
        if res_all and (not res or res_all[0][0] > res[0][0] + 0.02):
            res = res_all
    return res


def veredicto_nombre(res):
    """('alta' | 'media' | None, mejor) según la seguridad y la distancia con el segundo candidato."""
    if not res:
        return None, None
    s1 = res[0][0]
    s2 = res[1][0] if len(res) > 1 else 0.0
    if s1 >= 0.74 and s1 - s2 >= 0.08:
        return "alta", res[0]
    if s1 >= 0.62 and s1 - s2 >= 0.05:
        return "media", res[0]
    return None, None



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
    if len(leido or "") == 8 and sum(ch.isdigit() for ch in leido) >= 5:   # 1 dígito mal leído (o ilegible '?' / '_')
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


def _cursos_por_conteo(df, correcta, incorrecta):
    """Cursos con «Preguntas» y un «Empieza en» opcional (si está vacío, sigue a continuación del anterior)."""
    cursos, errores, usadas, pos = [], [], {}, 1
    for _, r in df.iterrows():
        nom = str(r.get("Curso") or "").strip()
        if not nom or nom.lower() == "nan":
            continue
        try:
            n = int(r.get("Preguntas"))
        except Exception:
            errores.append(f"'{nom}': escribe cuántas preguntas tiene.")
            continue
        if n < 1:
            errores.append(f"'{nom}': debe tener al menos 1 pregunta.")
            continue
        emp = r.get("Empieza en")
        try:
            ini = int(emp) if emp is not None and not pd.isna(emp) else pos
        except Exception:
            ini = pos
        fin = ini + n - 1
        if fin > 100:
            errores.append(f"'{nom}': llega hasta la pregunta {fin} y la hoja solo tiene 100.")
            continue
        choque = [usadas[q] for q in range(ini, fin + 1) if q in usadas]
        if choque:
            errores.append(f"'{nom}' se cruza con '{choque[0]}': una pregunta no puede ser de dos cursos.")
            continue
        for q in range(ini, fin + 1):
            usadas[q] = nom
        cursos.append({"nombre": nom, "desde": ini, "hasta": fin, "correcta": correcta, "incorrecta": incorrecta})
        pos = fin + 1
    cursos.sort(key=lambda c: c["desde"])
    return cursos, errores


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
        with st.expander("📝 Armar el examen en Word: dos columnas, portada, número de página y QR"):
            st.caption("Sube tu examen en Word (.docx) con las preguntas y sus imágenes o gráficos. El sistema te devuelve "
                       "el mismo examen listo para imprimir: hoja A4, dos columnas, imágenes ajustadas, portada con los "
                       "cursos de este simulacro, número de página y QR. Cada pregunta se mantiene junta.")
            inst0 = {**INSTITUCION_DEFECTO, **datos.get("institucion", {})}
            st.markdown("**Datos del colegio** (salen en la portada, en el QR y en el pie de página)")
            i1, i2 = st.columns(2)
            coord = i1.text_input("Coordinador académico (celular):", inst0["coordinador"], key=pfx + "w_coord")
            cole = i2.text_input("Celular o teléfono del colegio:", inst0["colegio"], key=pfx + "w_cole")
            i3, i4 = st.columns(2)
            direc = i3.text_input("Dirección (opcional):", inst0.get("direccion", ""), key=pfx + "w_dir")
            webs = i4.text_input("Web o Facebook (opcional):", inst0.get("web", ""), key=pfx + "w_web")
            lema_t = st.text_input("Lema de la portada (déjalo vacío si no quieres lema):", inst0.get("lema", ""), key=pfx + "w_lema")
            inst_n = {"coordinador": coord.strip(), "colegio": cole.strip(), "direccion": direc.strip(), "web": webs.strip(),
                      "lema": lema_t.strip()}
            if inst_n != {k: datos.get("institucion", {}).get(k, INSTITUCION_DEFECTO.get(k, "")) for k in inst_n}:
                datos["institucion"] = inst_n
                guardar_datos(datos)
            niv0, des0 = destino_defecto(sim)
            j1, j2, j3 = st.columns(3)
            nivel_w = j1.selectbox("Nivel:", NIVELES_EX, index=NIVELES_EX.index(niv0), key=pfx + "w_niv")
            ops_d = DESTINOS_EX[nivel_w]
            destino_w = j2.selectbox("Dirigido a (grupo o grado):", ops_d,
                                     index=ops_d.index(des0) if des0 in ops_d else len(ops_d) - 1, key=pfx + "w_des")
            tg = j3.text_input("Título grande de la portada:", _titulo_grande(sim["titulo"]), key=pfx + "w_tg")
            up_w = st.file_uploader("Tu examen en Word (.docx):", type=["docx"], key=pfx + "word_up")
            w1, w2 = st.columns(2)
            con_portada = w1.checkbox("Con portada", value=True, key=pfx + "word_portada")
            dos_cols = w2.checkbox("En dos columnas", value=True, key=pfx + "word_cols")
            if up_w is not None:
                try:
                    out_w, n_im = formatear_examen_word(up_w.getvalue(), sim, portada=con_portada,
                                                        columnas=2 if dos_cols else 1, institucion=inst_n,
                                                        titulo_grande=tg.strip() or None, nivel_texto=nivel_w,
                                                        destino_texto=destino_w)
                    import hashlib
                    huella = hashlib.md5(up_w.getvalue() + repr((nivel_w, destino_w, tg, inst_n, con_portada, dos_cols,
                                                                  sim["titulo"], sim.get("fecha"))).encode()).hexdigest()
                    if st.session_state.get(pfx + "ex_huella") != huella:      # solo cuando cambia el archivo u opciones
                        guardar_en_archivo(datos, sim, nivel_w, destino_w, out_w, huella=huella)
                        st.session_state[pfx + "ex_huella"] = huella
                    st.success(f"✅ Examen listo ({n_im} imagen(es) ajustada(s)). Guardado en 📁 Exámenes: {nivel_w} · {destino_w}.")
                    st.download_button("⬇️ Descargar el examen listo para imprimir (Word)", out_w,
                                       "Examen_" + re.sub(r"\W+", "_", sim["titulo"]) + ".docx", MIME_DOCX,
                                       key=pfx + "word_dl", type="primary")
                    st.caption("Ábrelo en Word y revisa la vista de impresión. Todo el texto sigue siendo editable.")
                except ImportError:
                    st.error("Falta instalar python-docx en el servidor (agrégalo a requirements.txt).")
                except Exception as e:
                    st.error(f"No se pudo leer el archivo ({e}). Guarda tu examen como «Documento de Word (.docx)» "
                             "y vuelve a subirlo.")
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
    _ops_n = [OTRO_NOMBRE] + EVALUACIONES
    _ini_n = sim["titulo"] if sim["titulo"] in EVALUACIONES else (OTRO_NOMBRE if (sid and sim["titulo"]) else EVALUACIONES[0])
    _elec = c1.selectbox("Evaluación (elige de la lista o escribe otro nombre):", _ops_n,
                         index=_ops_n.index(_ini_n), key=pfx + "tit_sel")
    if _elec == OTRO_NOMBRE:
        titulo = c1.text_input("Escribe el nombre:", sim["titulo"] if sid and sim["titulo"] not in EVALUACIONES else "",
                               key=pfx + "tit")
    else:
        titulo = _elec
    fecha = c2.text_input("Fecha:", sim.get("fecha", ""), key=pfx + "fec")
    _pops = PERIODOS + ([sim["periodo"]] if sim.get("periodo") and sim["periodo"] not in PERIODOS else [])
    _per = c3.selectbox("Periodo / Bimestre:", _pops, index=_pops.index(sim["periodo"]) if sim.get("periodo") in _pops else 0,
                        key=pfx + "per_sel")
    periodo = "" if _per == PERIODOS[0] else _per
    if not sid and any(x.get("titulo") == titulo and x.get("fecha") == fecha for x in datos["simulacros"].values()):
        st.warning("⚠️ Ya existe un simulacro con este mismo nombre y fecha. Cámbialo si no quieres duplicarlo.")

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
    opc_n = int(sim.get("opciones", 5 if not sid else 4))      # nuevos: A-E; antiguos: se respetan (A-D)
    L_n = "ABCDE" if opc_n == 5 else "ABCD"
    A_n = "X" if opc_n == 5 else "E"                           # símbolo de pregunta anulada
    mk = modal or "".join(grupos)            # evita mezclar lo escrito al cambiar de modalidad
    prev = sim.get("cursos_area") or {}
    pc = next((c for c in sim.get("cursos", []) if prev), None) if prev else None
    st.markdown("#### 🧮 Puntaje")
    p1, p2, p3, p4 = st.columns(4)
    p_ok = p1.number_input("Por respuesta correcta:", -100.0, 100.0, float(pc["correcta"]) if pc else 1.0,
                           0.25, key=pfx + "p_ok")
    p_mal = p2.number_input("Por respuesta incorrecta:", -100.0, 100.0, float(pc["incorrecta"]) if pc else 0.0,
                            0.25, key=pfx + "p_mal")
    p_bl = p3.number_input("Por pregunta en blanco:", -100.0, 100.0, float(sim.get("puntaje_blanco", 0)),
                           0.25, key=pfx + "p_bl")
    _opc_an = ["Se da por buena a todos", "No cuenta (se quita del total)"]
    _an = p4.selectbox("Si una pregunta se ANULA:", _opc_an, index=1 if sim.get("anulada") == "descartar" else 0,
                       key=pfx + "anulada",
                       help="Para anular una pregunta elige «Anulada» en la clave (en la caja de pegar, escribe X). Con la primera opción "
                            "todos reciben el punto; con la segunda se quita del total. En ambos casos un alumno que "
                            "contesta todo bien saca 20.")
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

    def _bloque_clave(suf, rotulo, n_ref, inicial, cursos_ref=None):
        """Clave de respuestas en TABLA: cada pregunta con su número y su curso, y la respuesta se elige de una
        lista. Para ir rápido se puede pegar la clave completa; la tabla sirve para comprobarla y corregir."""
        kk = pfx + f"clave_{mk}_{suf}"
        kv, kver = kk + "_val", kk + "_ver"
        preg = sorted({q for c_ in (cursos_ref or []) for q in range(c_["desde"], c_["hasta"] + 1)}) \
            or list(range(1, int(n_ref or 0) + 1))
        curso_q = {q: c_["nombre"] for c_ in (cursos_ref or []) for q in range(c_["desde"], c_["hasta"] + 1)}
        top = max(preg) if preg else 0
        sig = tuple((c_["nombre"], c_["desde"], c_["hasta"]) for c_ in (cursos_ref or [])) or (int(n_ref or 0),)
        ksig = kk + "_sig"
        if kv not in st.session_state:
            st.session_state[kv] = inicial or ""
        elif st.session_state.get(ksig) not in (None, sig):
            # cambiaron los cursos o el número de preguntas: las respuestas de antes ya no corresponden
            st.session_state[kv] = ""
            st.session_state[kver] = st.session_state.get(kver, 0) + 1
            st.info("Cambiaste los cursos o el número de preguntas: vuelve a pegar la clave o elígela en la tabla.")
        st.session_state[ksig] = sig
        canon = st.session_state[kv]
        ver = st.session_state.get(kver, 0)

        def _pegado():
            k_ = limpiar_clave(st.session_state.get(kk, ""), len(preg),
                               "ABCDEX" if opc_n == 5 else "ABCDE")             # una letra por pregunta del examen
            if k_:
                full_ = [A_n] * top                      # números que no son del examen: anulados
                for q_ in preg:
                    full_[q_ - 1] = "?"                  # preguntas del examen: vacías hasta tener respuesta
                for q_, ch_ in zip(preg, k_):
                    full_[q_ - 1] = ch_
                st.session_state[kv] = "".join(full_)
                st.session_state[kver] = st.session_state.get(kver, 0) + 1

        st.markdown(f"**{rotulo}**  ·  {len(preg)} preguntas")
        st.text_area("Pega la clave (" + L_n + "… seguida, con espacios o numerada 1A 2B…):", height=70, key=kk,
                     on_change=_pegado,
                     help="Pega aquí la clave completa y haz clic fuera de la caja: se llena la tabla de abajo. "
                          "Después comprueba cada respuesta en la tabla y corrige la que haga falta.")
        kdf = f"{kk}_df_{ver}"
        if kdf not in st.session_state:
            filas = []
            for q in preg:
                ch = canon[q - 1] if q - 1 < len(canon) else "?"
                filas.append({"N.º": q, "Curso": curso_q.get(q, ""),
                              "Respuesta": "Anulada" if ch == A_n else (ch if ch in L_n else None)})
            st.session_state[kdf] = pd.DataFrame(filas, columns=["N.º", "Curso", "Respuesta"])
        ed = st.data_editor(st.session_state[kdf], hide_index=True, use_container_width=True, num_rows="fixed",
                            disabled=["N.º", "Curso"], key=f"{kk}_tab_{ver}",
                            height=int(min(430, 36 * len(preg) + 42)),
                            column_config={"Respuesta": st.column_config.SelectboxColumn(
                                "Respuesta correcta", options=list(L_n) + ["Anulada"], required=False)})
        full = [A_n] * top
        faltan = []
        for q, v_ in zip(preg, ed["Respuesta"]):
            if v_ in tuple(L_n):
                full[q - 1] = v_
            elif v_ == "Anulada":
                full[q - 1] = A_n
            else:
                full[q - 1] = "?"
                faltan.append(q)
        k = "".join(full)
        st.session_state[kv] = k
        puestas = len(preg) - len(faltan)
        if not faltan:
            st.success(f"✅ Clave completa: {puestas} de {len(preg)} respuestas.")
        elif puestas == 0:
            errores.append("Falta la clave de respuestas." if (unico or suf == "comun") else f"Falta la clave del Área {suf}.")
        else:
            st.warning(f"Faltan {len(faltan)} respuestas (preguntas {', '.join(map(str, faltan[:12]))}"
                       + ("…" if len(faltan) > 12 else "") + "). Elígelas en la tabla.")
            errores.append(f"Falta completar la clave ({len(faltan)} preguntas sin respuesta).")
        with st.expander("📸 Leer esta clave desde una hoja rellenada"):
            st.caption("Rellena una hoja Yachay con las respuestas correctas, tómale foto y súbela.")
            fk = st.file_uploader("Hoja clave:", type=["jpg", "jpeg", "png", "pdf"], key=pfx + f"fk_{mk}_{suf}")
            if fk is not None and st.button("Leer clave", key=pfx + f"lk_{mk}_{suf}"):
                imgs = omr.imagenes_desde_archivo(fk.name, fk.getvalue())
                if imgs:
                    r = omr.leer_hoja(imgs[0], top or 80)
                    leida = [A_n] * top
                    for q_ in preg:
                        x_ = r["respuestas"][q_ - 1] if q_ - 1 < len(r["respuestas"]) else ""
                        leida[q_ - 1] = x_ if x_ in tuple(L_n) else "?"
                    st.session_state[kv] = "".join(leida)
                    st.session_state[kver] = ver + 1
                    st.rerun()
        return k

    def _bloque_area(g):
        nom = "los cursos" if unico else f"el Área {g}"
        guardado = prev.get(g)
        rk = pfx + f"rst_{mk}_{g}"
        ver = st.session_state.get(rk, 0)
        if unico:
            guard_u = {c["nombre"]: c for c in (guardado or [])} if (guardado and ver == 0) else {}
            op_c = list(CURSOS_CATALOGO) + [n for n in guard_u if n not in CURSOS_CATALOGO]
            ini_c = sorted(guard_u, key=lambda n: guard_u[n]["desde"]) if guard_u else [n for n, _q in plantilla]
            sel_c = st.multiselect("✅ Elige los cursos de este examen (puedes buscar escribiendo)", op_c, default=ini_c,
                                   key=pfx + f"selc_{mk}_{ver}")
            otro_c = st.text_input("¿Falta un curso? Escríbelo aquí y pulsa Enter:", key=pfx + f"otroc_{mk}_{ver}").strip()
            if otro_c and otro_c not in sel_c:
                sel_c = sel_c + [otro_c]
            pl = dict(plantilla)
            base, fin_prev = [], 0
            for nm_ in sel_c:
                if nm_ in guard_u:
                    c_ = guard_u[nm_]
                    npg = c_["hasta"] - c_["desde"] + 1
                    emp = c_["desde"] if c_["desde"] != fin_prev + 1 else None
                    fin_prev = c_["hasta"]
                else:
                    npg, emp = pl.get(nm_, 10), None
                    fin_prev = fin_prev + npg
                base.append((nm_, npg, emp))
        else:
            plant_g = list(PLANTILLAS_AREA[g])
            guard_g = ({c["nombre"]: c["hasta"] - c["desde"] + 1 for c in guardado} if (guardado and ver == 0) else {})
            op_g = [n for n, _q in plant_g] + [n for n in guard_g if n not in {x[0] for x in plant_g}]
            pn_g = dict(plant_g)
            pn_g.update(guard_g)
            sel_g = st.multiselect(f"✅ Cursos que vas a evaluar en el Área {g} (quita los que no entran)", op_g,
                                   default=[n for n in op_g if n in guard_g] if guard_g else op_g,
                                   key=pfx + f"sel_{mk}_{g}_{ver}")
            if not sel_g:
                errores.append(f"Área {g}: elige al menos un curso.")
            base = [(n, pn_g[n]) for n in op_g if n in sel_g]
        ca, cb = st.columns([1.2, 1])
        with ca:
            if unico:
                st.markdown("**1️⃣ ¿Cuántas preguntas tiene cada curso?**")
                st.caption("Las preguntas se numeran seguidas (1, 2, 3…) en el orden de la tabla. Si un curso debe empezar "
                           "en otro número, escríbelo en «Empieza en»; si no, déjalo vacío.")
                df = pd.DataFrame(base, columns=["Curso", "Preguntas", "Empieza en"])
                cfg_cur = {"Preguntas": st.column_config.NumberColumn(min_value=1, max_value=100, step=1),
                           "Empieza en": st.column_config.NumberColumn(min_value=1, max_value=100, step=1,
                                                                        help="Opcional: n.º de la primera pregunta")}
            else:
                st.markdown("**1️⃣ Cursos y n.º de preguntas**")
                df = pd.DataFrame(base, columns=["Curso", "Preguntas"])
                cfg_cur = {"Preguntas": st.column_config.NumberColumn(min_value=1, max_value=100, step=1)}
            df_e = st.data_editor(df, num_rows="fixed" if unico else "dynamic", use_container_width=True, hide_index=True,
                                  disabled=["Curso"] if unico else False,
                                  key=pfx + f"cur_{mk}_{g}_{ver}_{abs(hash(tuple(x[0] for x in base)))}", column_config=cfg_cur)
            if st.button("↩️ Restaurar cursos originales" if unico else "↩️ Restaurar temario oficial",
                         key=pfx + f"rstb_{mk}_{g}"):
                st.session_state[rk] = ver + 1
                st.rerun()
        if unico:
            cursos_g, err_g = _cursos_por_conteo(df_e, float(p_ok), float(p_mal))
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
                                      n_g, sim.get("claves", {}).get(g, ""), cursos_ref=cursos_g)

    union_guardar = None
    if unico:
        _bloque_area(grupos[0])
    elif compartida:
        # Un solo examen: cursos de todas las áreas; cada área rinde los suyos.
        et = _etiquetas_areas(grupos)
        inv = {v: k for k, v in et.items()}
        rk = pfx + f"rst_uni_{mk}"
        ver = st.session_state.get(rk, 0)
        plant_u = [(n, q, inv[a]) for n, q, a in _union_default(grupos)]
        guard_u = ({u["nombre"]: (u["nombre"], u["preguntas"], inv.get(u["areas"], list(et)[0]))
                    for u in sim["cursos_union"]} if (sim.get("cursos_union") and ver == 0) else {})
        op_u = [x[0] for x in plant_u] + [n for n in guard_u if n not in {x[0] for x in plant_u}]
        por_u = {x[0]: x for x in plant_u}
        por_u.update(guard_u)
        elegidos_u = st.multiselect("✅ Cursos que vas a evaluar (quita los que no entran en este examen)", op_u,
                                    default=[n for n in op_u if n in guard_u] if guard_u else op_u,
                                    key=pfx + f"sel_{mk}_{ver}")
        if not elegidos_u:
            errores.append("Elige al menos un curso para evaluar.")
        base = [por_u[n] for n in op_u if n in elegidos_u]
        sig_u = abs(hash(tuple(elegidos_u)))
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
                                   key=pfx + f"uni_{mk}_{ver}_{int(todos)}_{sig_u}", column_config=cfg)
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
                          n_total, ini, cursos_ref=[c_ for g_ in grupos for c_ in cursos_area[g_]])
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
                      "num_preguntas": int(n_max), "puntaje_blanco": p_bl, "opciones": opc_n,
                      "anulada": "descartar" if _an == _opc_an[1] else "buena",
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
    share = {g: sum(1 for q in excl[g] if q - 1 < len(resp) and resp[q - 1] in (tuple(letras_sim(sim)) + ("*",))) / len(excl[g])
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


def ya_dnis(sim):
    """DNI que ya tienen hoja en este simulacro."""
    return {norm_dni(h.get("dni")) for h in sim.get("hojas", {}).values()}


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
    _union_v = set()
    for _c in cursos_union(sim):
        _union_v.update(range(_c["desde"], _c["hasta"] + 1))
    nlee = max(_union_v) if _union_v else int(sim["num_preguntas"])
    r = omr.leer_hoja(img, nlee)
    for _i in range(len(r["respuestas"])):          # preguntas que no son de ningún curso: se ignoran
        if (_i + 1) not in _union_v:
            r["respuestas"][_i] = ""
            r["estados"][_i] = "blanco"
    resp = "".join({"": "_"}.get(x, x) for x in r["respuestas"])
    dni_leido = r["dni"]
    _an = _lista_auto_nombre(sim)
    _del_grupo = set(_alumnos_de_lista(mat, "auto", sim)) if _an else set()
    rr = resolver_dni(dni_leido, mat, _del_grupo)
    dni, info = rr["dni"], rr["info"]
    grupo = r["grupo"]
    gs = grupos_sim(sim)
    alertas = list(r["alertas"]) + rr["avisos"]
    if not any(ch.isdigit() for ch in (dni_leido or "")):        # DNI totalmente en blanco: un solo aviso, claro
        alertas = [a for a in alertas if not a.startswith("DNI incompleto")]
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
    nombre_ocr = ""
    if not info and mat and reconocimiento_disponible():
        # Sin DNI válido: se lee el nombre escrito y se compara con la matrícula
        try:
            nombre_ocr, _motor = reconocer_nombre(omr.recortes_campos_nombre(r))
        except Exception:
            nombre_ocr = ""
        if nombre_ocr:
            res_n = sugerir_por_nombre(nombre_ocr, mat, _del_grupo)
            niv_n, mj_n = veredicto_nombre(res_n)
            if niv_n and mj_n[1] not in ya_dnis(sim):
                sug = mj_n[1]
                alertas.append(f"Nombre leído «{nombre_ocr[:40]}» → ¿será {mj_n[2]}? ({mj_n[0] * 100:.0f} %, "
                               f"seguridad {niv_n})")
            else:
                alertas.append(f"Nombre leído «{nombre_ocr[:40]}»: no se identificó con seguridad; mira la imagen y "
                               "búscalo por nombre")
    if info and _del_grupo and rr["dni"] not in _del_grupo:
        alertas.append(f"Este alumno es de otro grupo ({_aula_de(info) or info.get('grado', '')}), "
                       f"no de {_an}: verifica")
    if not info:
        alertas.append("DNI no encontrado en matrícula" if re.fullmatch(r"\d{8}", dni_leido or "")
                       else ("No marcó el DNI: escribe el nombre mirando la imagen «Nombre escrito»"
                             if not any(ch.isdigit() for ch in (dni_leido or ""))
                             else "DNI incompleto: escribe el nombre mirando la imagen «Nombre escrito»"))
        if sug:
            alertas.append(f"¿Será {mat[sug]['nombre']} (DNI {sug})? Usa «Aceptar sugerencias» si es correcto")
    clave = clave_para(sim, grupo)
    validas = preguntas_validas(sim, grupo) or _union_v
    clave = "".join(k if (i + 1) in validas else "-" for i, k in enumerate(clave))
    return {"tmp_id": uuid.uuid4().hex[:8], "dni": dni, "nombre": info.get("nombre", ""),
            "grado": info.get("grado", ""), "aula": _aula_de(info), "grupo": grupo,
            "respuestas": resp, "dudosas": [i + 1 for i, e in enumerate(r["estados"])
                        if e in ("duda", "doble") and (validas is None or (i + 1) in validas)],
            "alertas": alertas, "otro_sim": otro_sim, "sug_dni": sug if not info else None,
            "dni_leido": dni_leido, "nombre_ocr": nombre_ocr,
            "origen": origen, "fecha_examen": f"{r['dia'] or ''}/{r['mes'] or ''}/{r['anio'] or ''}",
            "nombre_img": (base64.b64encode(omr.recorte_nombre(r)).decode() if (not info and omr.recorte_nombre(r)) else ""),
            "img": omr.imagen_revision(r, clave, nombre=info.get("nombre", ""), validas=validas)}


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
                             "nombre_ocr": "" if nombre_h else h.get("nombre_ocr", ""),
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

    if st.session_state.get("simy_msg_ok"):
        st.success(st.session_state.pop("simy_msg_ok"))

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

    # ---- Aviso de DNI mal escritos en la matrícula (solo aparece si los hay) ----
    try:
        df_prob = analizar_dnis_matricula(_HOOKS["cargar_matricula"]() if _HOOKS["cargar_matricula"] else None)
    except Exception:
        df_prob = pd.DataFrame()
    if len(df_prob):
        st.warning(f"⚠️ {df_prob['Alumno'].nunique()} alumno(s) tienen el DNI mal escrito en la matrícula "
                   "(no se reconocerán solos al escanear).")
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

    # ---- Subir las hojas: se leen SOLAS al subirlas (sin botón) ----
    up_key, firma_key = f"simy_upver_{sid}", f"simy_firma_{sid}"
    st.session_state.setdefault(up_key, 0)
    st.markdown("#### 📸 Sube las hojas escaneadas")
    archivos = st.file_uploader("Arrastra aquí el PDF con todas las hojas (o fotos sueltas). Se leen solas.",
                                type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True,
                                key=f"simy_up_{sid}_{st.session_state[up_key]}")
    st.caption("💡 Lo más fácil: escanea todas las hojas en **un solo PDF** (grises, 200 dpi), de hasta 100-150 hojas. "
               "Si usas fotos: de frente, con buena luz y con los 4 cuadrados negros de las esquinas a la vista.")
    firmas = tuple((a_.name, a_.size) for a_ in (archivos or []))
    if archivos and firmas != st.session_state.get(firma_key):
        st.session_state[firma_key] = firmas
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

    with st.expander("🛠️ Otras opciones: cámara, digitar a mano, hoja en blanco para imprimir"):
        otra = st.radio("¿Una sola hoja o no tienes PDF?",
                        ["Solo con el PDF o las fotos de arriba", "📷 Cámara (hoja por hoja)", "⌨️ Digitar a mano"],
                        key="simy_fuente2")
        boton_hoja(None, "simy_dl_hoja_scan")
        st.caption("Hoja genérica para imprimir. El sistema comprueba la fecha que el alumno marca "
                   "para avisarte si una hoja es de otro examen.")
    fuente = "📁" if otra.startswith("Solo") else otra

    if fuente.startswith("📷"):
        foto = st.camera_input("Toma la foto de la hoja", key=f"simy_cam_{sid}")
        if foto is not None and st.button("➕ Leer y agregar al lote", type="primary", key="simy_cam_ok"):
            img = omr.imagenes_desde_archivo("cam.jpg", foto.getvalue())[0]
            st.session_state[lote_key].append(_procesar_imagen(sim, img, mat, "cámara"))
            st.rerun()

    elif fuente.startswith("⌨️"):
        with st.form("simy_manual", clear_on_submit=True):
            m1, m2, m3 = st.columns([1, 2, 1])
            dni = m1.text_input("DNI:")
            nom = m2.text_input("Apellidos y nombres (si no está matriculado):")
            grp = grupos_sim(sim)[0] if sim.get("sin_area") else m3.selectbox("Área / Grupo:", [""] + grupos_sim(sim))
            txt = st.text_area("Respuestas marcadas (usa _ para blanco):", height=80)
            if st.form_submit_button("➕ Agregar al lote"):
                d = norm_dni(dni)
                resp = "".join(ch if ch in (letras_sim(sim) + "*_") else "_" for ch in re.sub(r"[\s\d\.\)\-:]", "", txt.upper()))
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
        h["alertas"] = [a for a in h["alertas"] if not a.startswith(
            ("DNI no encontrado", "¿Será", "Nombre leído", "No marcó el DNI", "DNI incompleto"))]

    n_sug = sum(1 for h in lote if h.get("sug_dni") in mat)
    if n_sug and st.button(f"✅ Aceptar las {n_sug} sugerencia(s) de DNI (revísalas en la columna «Sugerencia DNI»)",
                           key="simy_acepta_sug"):
        for h in lote:
            k = h.get("sug_dni")
            if k in mat:
                h.update({"dni": k, "nombre": mat[k]["nombre"], "grado": mat[k]["grado"],
                          "aula": _aula_de(mat[k]), "sug_dni": None, "nombre_img": "", "nombre_ocr": ""})
                _limpiar_alertas_dni(h)
        st.session_state[ver_key] += 1
        st.rerun()

    # Detalle de cada hoja (con cientos de hojas se muestran solo las que necesitan revisión)
    prob_idx = [i for i, h in enumerate(lote) if h["alertas"] or h["dudosas"]]
    if len(lote) > 6:
        modo_det = st.radio("Ver el detalle de:", [f"⚠️ Solo las que necesitan revisión ({len(prob_idx)})",
                                                   f"📄 Todas ({len(lote)})"], horizontal=True, key=f"simy_detmodo_{sid}")
    else:
        modo_det = "📄 Todas"                      # pocas hojas: se muestran todas, sin preguntar
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
                limpio = "".join(ch for ch in nueva.upper() if ch in (letras_sim(sim) + "*_"))
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
                                          "aula": _aula_de(mat[sel]), "sug_dni": None, "nombre_img": "", "nombre_ocr": ""})
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
        st.session_state[up_key] += 1
        st.session_state.pop(firma_key, None)
        st.session_state["simy_msg_ok"] = (f"✅ Guardado: {nuevos} hojas nuevas y {reemp} actualizadas (mismo DNI). "
                                           "Siguiente paso: mira quién falta en 📋 Lista de control o ve a 🏆 Ranking.")
        st.rerun()
    if b2.button("🗑️ Vaciar lote sin guardar", key="simy_vaciar"):
        st.session_state[lote_key] = []
        st.session_state["simy_fallos"] = []
        st.session_state[up_key] += 1
        st.session_state.pop(firma_key, None)
        st.rerun()


def _crops_de_imagen_guardada(b64):
    """Recuadros de apellidos y nombres a partir de la imagen reducida que se guarda con la hoja."""
    import cv2
    import numpy as np
    try:
        g = cv2.imdecode(np.frombuffer(base64.b64decode(b64), np.uint8), cv2.IMREAD_GRAYSCALE)
        if g is None:
            return []
        h = g.shape[0]
        crops = [g[int(h * 0.02):int(h * 0.40)], g[int(h * 0.60):int(h * 0.98)]]
        return [cv2.resize(c, None, fx=1.8, fy=1.8, interpolation=cv2.INTER_CUBIC) for c in crops]
    except Exception:
        return []


def _resolver_sin_identificar(datos, sim):
    """Alumnos cuya hoja no coincide con la matrícula (DNI mal marcado o sin DNI): se lee el nombre escrito y se
    propone vincularlos con el alumno de la matrícula."""
    mat = _matricula()
    if not mat:
        return
    sin = [(hid, h) for hid, h in sim.get("hojas", {}).items()
           if h.get("nombre_img") and not any(k in mat for k in (norm_dni(h.get("dni")),))
           and not (len(norm_dni(h.get("dni"))) > 8 and norm_dni(h.get("dni"))[:8] in {k[:8] for k in mat})]
    if not sin:
        return
    with st.expander(f"🧩 Alumnos sin identificar ({len(sin)}): vincular con la matrícula por su nombre escrito"):
        st.caption("Estas hojas no coincidieron con la matrícula por el DNI. El sistema lee el nombre que escribió el "
                   "alumno y lo compara con la matrícula. **Mira la imagen antes de vincular.**")
        pendientes = [hid for hid, h in sin if not h.get("nombre_ocr")]
        if pendientes and reconocimiento_disponible():
            if st.button(f"🔎 Leer los nombres escritos a mano ({len(pendientes)})", key="simy_res_leer"):
                barra = st.progress(0.0, "Leyendo nombres…")
                for k, hid in enumerate(pendientes):
                    h = sim["hojas"][hid]
                    try:
                        h["nombre_ocr"], _m = reconocer_nombre(_crops_de_imagen_guardada(h["nombre_img"]))
                    except Exception:
                        h["nombre_ocr"] = ""
                    h["nombre_ocr"] = h["nombre_ocr"] or "-"
                    barra.progress((k + 1) / len(pendientes))
                guardar_datos(datos)
                st.rerun()
        elif pendientes:
            st.info("Para que el sistema lea los nombres escritos a mano hay que activar el lector: instala "
                    "`rapidocr-onnxruntime` (gratis) o configura `ANTHROPIC_API_KEY` (IA, mucho más preciso).")
        pref = set(_alumnos_de_lista(mat, "auto", sim)) if _lista_auto_nombre(sim) else set()
        usados = ya_dnis(sim)
        filas, info = [], {}
        for hid, h in sin:
            txt = h.get("nombre_ocr", "")
            txt = "" if txt == "-" else txt
            res = sugerir_por_nombre(txt, mat, pref) if txt else []
            niv, mj = veredicto_nombre(res)
            dni_s = mj[1] if mj else ""
            dup = bool(dni_s) and dni_s in usados
            info[hid] = dni_s
            filas.append({"hid": hid, "Nombre escrito": "data:image/jpeg;base64," + h["nombre_img"], "Leído": txt or "—",
                          "Alumno sugerido": (f"{mj[2]} — {_aula_de(mat[dni_s])}" if mj else "(sin coincidencia clara)")
                                             + (" · YA TIENE HOJA" if dup else ""),
                          "Seguridad": (f"{mj[0] * 100:.0f} % ({niv})" if mj else ""),
                          "Vincular": bool(mj) and not dup and niv in ("alta", "media")})
        dfv = pd.DataFrame(filas)
        ed = st.data_editor(dfv.drop(columns=["hid"]), hide_index=True, use_container_width=True,
                            disabled=["Nombre escrito", "Leído", "Alumno sugerido", "Seguridad"],
                            key=f"simy_res_ed_{sim['id']}_{len(sin)}",
                            column_config={"Nombre escrito": st.column_config.ImageColumn("Nombre escrito", width="large")})
        marcar = [dfv.iloc[i]["hid"] for i, v in enumerate(ed["Vincular"]) if v and info.get(dfv.iloc[i]["hid"])]
        if marcar and st.button(f"✅ Vincular los {len(marcar)} marcado(s) con la matrícula", type="primary",
                                key="simy_res_vincular"):
            for hid in marcar:
                d = info[hid]
                sim["hojas"][hid].update({"dni": d, "nombre": mat[d]["nombre"], "aula": _aula_de(mat[d]),
                                          "grado": mat[d]["grado"], "nombre_img": "", "nombre_ocr": ""})
            guardar_datos(datos)
            if sim.get("publicado"):
                publicar_en_historial(sim)
            st.session_state["simy_msg_rank"] = f"✅ {len(marcar)} alumno(s) vinculados con la matrícula."
            st.rerun()
        st.caption("Si el sistema no reconoce a alguien, corrígelo a mano en «🧾 Boleta de un estudiante / corregir o "
                   "eliminar hoja» (el DNI y el nombre).")


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

    if st.session_state.get("simy_msg_rank"):
        st.success(st.session_state.pop("simy_msg_rank"))
    _resolver_sin_identificar(datos, sim)

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

    _sosp = []
    for _g in ([None] if (sim.get("todos_cursos") or sim.get("sin_area") or len(grupos_sim(sim)) < 2) else grupos_sim(sim)):
        _sosp += preguntas_sospechosas(sim, _g)
    if _sosp:
        st.warning("⚠️ Antes de publicar, revisa la clave de las preguntas: "
                   + ", ".join(sorted({str(x["Pregunta"]) for x in _sosp}, key=int))
                   + ". Mira el detalle en 📊 Análisis.")

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


def _administrar_simulacros(datos):
    """Lista de todos los simulacros guardados, con opción de retirarlos de las familias o borrarlos."""
    with st.expander("🗂️ Administrar simulacros guardados (retirar de padres o borrar)"):
        st.download_button("💾 Descargar copia de seguridad de todos los simulacros (JSON)",
                           json.dumps(datos, ensure_ascii=False).encode("utf-8"),
                           f"respaldo_simulacros_{datetime.now().strftime('%Y%m%d_%H%M')}.json", "application/json",
                           key="simy_dl_respaldo")
        sims = sorted(datos["simulacros"].values(), key=lambda x: str(x.get("creado", "")), reverse=True)
        if not sims:
            st.caption("No hay simulacros guardados.")
            return
        st.dataframe(pd.DataFrame([{"Evaluación": x["titulo"], "Fecha": x.get("fecha", ""), "Hojas": len(x.get("hojas", {})),
                                    "Tipo": etiqueta_modalidad(x),
                                    "Visible para padres": "Sí" if x.get("publicado") else "No"} for x in sims]),
                     use_container_width=True, hide_index=True)
        ids = [x["id"] for x in sims]
        sid = st.selectbox("Elige un simulacro:", ids, key="simy_adm_sel",
                           format_func=lambda i: f"{datos['simulacros'][i]['titulo']} — {datos['simulacros'][i].get('fecha', '')}")
        sim = datos["simulacros"][sid]
        a, b = st.columns(2)
        if sim.get("publicado") and a.button("🙈 Quitar de la vista de padres y alumnos", key="simy_adm_unpub"):
            quitar_de_historial(sim)
            sim["publicado"] = False
            guardar_datos(datos)
            st.success("Ya no lo ven los padres ni los estudiantes. Se conserva en el sistema.")
            st.rerun()
        if not _HOOKS["puede_borrar"] or _HOOKS["puede_borrar"]():
            ok = b.checkbox("Confirmo que quiero borrarlo con todas sus hojas", key="simy_adm_ok")
            if ok and b.button("🗑️ Borrar este simulacro definitivamente", key="simy_adm_del"):
                quitar_de_historial(sim)
                datos["simulacros"].pop(sid, None)
                guardar_datos(datos)
                st.success("Simulacro borrado.")
                st.rerun()
        else:
            b.caption("Solo la administración puede borrar simulacros.")


def _tab_historial(datos):
    st.subheader("📚 Historial del estudiante")
    _administrar_simulacros(datos)
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
    validas = preguntas_validas(sim, gsel or "") or None
    filas = []
    for q in range(nq):
        if validas is not None and (q + 1) not in validas:
            continue
        L_ = letras_sim(sim)
        cont = {**{l_: 0 for l_ in L_}, "Blanco": 0}
        ok = tot = 0
        for h in hojas:
            k = clave_para(sim, h.get("grupo", ""))
            k = k[q] if q < len(k) else ""
            r = h["respuestas"][q] if q < len(h["respuestas"]) else "_"
            cont[r if r in L_ else "Blanco"] += 1
            if k in L_ and k:
                tot += 1
                ok += r == k
        filas.append({"Pregunta": q + 1, "Curso": curso_de.get(q + 1, "-"),
                      "Clave": (clave_ref + " " * 100)[q].strip(),
                      "% acierto": round(ok / tot * 100, 1) if tot else None, **cont})
    sosp = preguntas_sospechosas(sim, gsel)
    if sosp:
        st.warning("⚠️ **Revisa la clave de estas preguntas** (puede estar mal): "
                   + ", ".join(str(x["Pregunta"]) for x in sosp)
                   + ". Si corriges la clave en ⚙️ Configurar, todas las notas se recalculan solas.")
        st.dataframe(pd.DataFrame(sosp), hide_index=True, use_container_width=True)
    elif len(hojas) >= 8:
        st.success("✅ Ninguna pregunta parece tener la clave mal (con las respuestas de los alumnos).")
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
                          guardar_historial=None, backup_json=None, puede_borrar=None,
                          backup_archivo=None, bajar_archivo=None):
    _HOOKS.update({"cargar_matricula": cargar_matricula, "cargar_historial": cargar_historial,
                   "guardar_historial": guardar_historial, "backup_json": backup_json,
                   "puede_borrar": puede_borrar, "backup_archivo": backup_archivo,
                   "bajar_archivo": bajar_archivo})
    st.header("🧾 Simulacros Yachay — Lectura de hojas y ranking")
    boton_hoja(None, "simy_dl_hoja_top")
    st.caption("Flujo: 1) ⚙️ Configurar el examen (elige Área A/B/C/D o Grupo AB/CD, pega las claves) → 2) 📸 Escanear las hojas → "
               "3) 📋 Lista de control (¿falta alguien?) → 4) 🏆 Ranking (imprimir / publicar) → 5) 📚 Historial del estudiante.")
    datos = cargar_datos()
    if _ESTADO["backup_error"]:
        st.error("⚠️ No se pudo hacer la copia de seguridad en Drive (" + _ESTADO["backup_error"] + "). Tus datos están "
                 "guardados en el sistema, pero descarga una copia en 📚 Historial → «Administrar simulacros guardados».")
    t = st.tabs(["⚙️ Configurar", "📸 Escanear", "📋 Lista de control", "🏆 Ranking", "📚 Historial", "📊 Análisis",
                 "📁 Exámenes"])
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
    with t[6]:
        _tab_examenes(datos)


# ================================================================
# LOGOS DE LA HOJA (PNG con fondo transparente, incrustados para no depender de más archivos)
# ================================================================
_LOGO_IZQ_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAPwAAAD8CAMAAABkdTlVAAACf1BMVEXun6SnYVnVY1jgppSoWyEfZ5Wn0+esmV5hkqnVmHCZoKSYtM/QTifd2eT919tnq84jUGfn25sth6dTb5LlJSV2JBxTYWWtjSenOUUhNVfeozL+xsj+2OAWJjTQa3HWe4OwXGFkWzKgISzeeYX+usPf1WDbxDb5ucNzxeLINkWsxq4sj8iqdob9wr27e4h7OkB1gk2KOz6+wFLWgX794+36+/iuFRDOGRaUFAuUCwnoJCXRqEjPJBeoCw3RJifw1mzXtk7GmDW0iC2wJinpxlXOpjfwyWn76evQGiTpuFGzJBbmGRnrHCT76NS6lDP++NbmJBuwGiSQJQnOmUf819DrqFCRJyl4FQqvNjHWtTPLDBF2CQTIiTTV+f6seijq1FjqmFKzlk7NNCz2t7D1uGn+2+T243TMNRfQ5/n7yMkuZ42peRnktzariUkWR27+2+UvVnTx1owqSWuSGiTt2K+TNjSwR0nLZzCWdzARKU3/4+cwdpPaxFLQdnIVNlXMdzTOtm3+2NuyV1LZx2+VNgbvl5H2xrbUiEfmxTjz5rP/5OnzqKmxNhPSlpDpiU3KV1KrRxH3qWlOiKv/1df+2+X+y9NPdpPXxo+x1u/QiInNaGrNWCxxlrD1yIoQOWavRS8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUyIh/AAAAoHRSTlOw8/P9/v/////+///+/xz////////5///0//+hWP+7u7n/4/Ck//////j///+vt///v/+/AP/+//7///////7//////f////////7////////+/v////v9/f///v////////7//0L///////////8Q/////P/7/f///0b///7///9F/v////////8w//////3///9gMGD//////v/////+4JyNBQAAYf9JREFUeNrdvQdDG8myNqwEQgQbTHTcXXvD2XPufb9kjUZpEBqhBEIo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"
)
_LOGO_DER_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAALAAAAB8CAMAAAD+Q8qjAAACf1BMVEXWmxtToGKeXgsmWyLi26Omnlueo5T63t6ikCDW29LZ0l2b3KxcZVddXiffawX857MdnE8imzL939raslIbMR9RzWyy58lv24385cebLxJNKgSfIhySdFTXGCF2oottiRMuZUbKtp+4xBHc9w83zFrJFyNuJByoymJEM12wRwA9PkLrlCv+4e/4+vf2+ArmAwTXBQPz6A/05y35+Cz22S0OBwLNFQT12RLz5074+EwvJgDu6u772+3x2UwPhy2zFwP45242NgFORwFRBAD957MoFwD86I1wBQANeSpuaQRIOAAWFgL5+dWOhwf95df6yCv959WOCABWVgISljDW1y795sfLJgKyJgH+5ehoWAHY+uuRFgK0CgHU1w51dQT2yBSJeQSupwbOxy7qFQgFdxUvBgD75Oj+58VvFQCWlgkGZhL92un46K0vp0yzNgDKOAD02Wz96ar3lw3s59Iul0vOyQ3V2Ez6tyz+2tgFVw/LRgDRVwH69W30hgn3pxD9thQphzSqmAja5wq1t7QGhhmztgbJuDAOaCmOJgGwqS0wtlBwNwCzti/RaAXreQMPJwRRFgDvykr8840vhUmOZwXKtw7a5C376JX99q4VpDZtJwAIRw1xdXTQ+dcteElxRgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADMfO6PAAAAoHRSTlP+////8f//Jf/9/P////+q//9U//////+l//+/////////////v7///7//vwD///////7//v////3///8Q/v//+f///7L/8v////////9O/2D/////nf//Sv////////////////8wsf///0j3////9M////////9M////+f///////////////////////////PH/////z/b/////////c8kwngAAIi9JREFUeNrNfIdDGunW/lBFEHtJclN29+73u19ZkWkwM0qZQaSJBEQN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"
)

_LOGO_ACA_HQ_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAggAAAIUCAMAAABINiSxAAADAFBMVEXXoJqaJR+sIx6k1ui1Zl6plFvfzK2XpaOxUEqVaCJOcJPEMS/LWVXp29dZZ2HcmFBtk6PLaWOdNCwucJpQp88hj8S1a2IoUGisRDuOrMJxx+bfo6A3kLhjVjTFIB/YbkrNh3t/AAAjO1jn5OPk0LXDPDThTzjJRUStSDx2hnS8iny4m5a2x7LFQzzfvsDhqDifOzDt5uWzQzzGQTzVfoKq///Top4yODq9O0CigCzCPkHFPkL19PK2SELOmpT//wA+Qj8A//9/EA9/f/+7P0G//7/DPUDOfILiuMYAAAD8/PuuFBDOGhiVDArnIyKaEQvv1mnZtk3RqUXFmDe1iC7QIhrnxlPQpTqreiXoy2Tu6+nkujXRJyO9kTQWV4vbsjIROGoURXakDg3t0lqyIxnmHSEad63lIR7n2NTivE8nhrfNNi714nQYZZjKm0Ts5tP9/v7owTsahLmpeB7/AADTl5PW5evKV1O1KCTjHBzNd3Pjyccneaq0Ny7atrMUTILJiDXYqKYqZ5PRiYbISUbLaWa5lkuxx9PNRTLJdzMMKlnUHCHRt28vlcWyRiy2VyfL2+MRNlmqNxrewViPtssZa6Pl2a9Ph6ooWoi1Zyrq2I6SFxJxlrHw5bDYxZGnucix2ObLZzCOprhRdZX389XhuLVQp856BgTHqWtzttLlMinWx8i3SUW3VVDL1NiaIxQMLGKRxdnPg3vWx65rqcckjMHOuYjKY1zPWC4nSXKYdCjVo5tQlbeyNTGwRRzMd3KzKSbEJST15I7bwm3HWFSqOTMtVXdqiacAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD9FeoAAAAyHRSTlMYn93/KP///1T//6FbDP///ytn//////9f///7///d/CAC//MOdf+IJ/8cDP9o//81q4yJ/wOe////cf9bg2oB/wH/AnEEki8SAP7+/v7//v///////v/////+//7///////7//v///v7///7////+BP///wH+//7+//7+//7+///+//7+/////////f///v///////////////9D////////////+//7////+///////////////+/////v+O/y6wzv//UHD//wmGMpsAAMp5SURBVHja7f2HY1NX2ugLCwdMb4GQ5E2d9s7b6znnnnLvd+/XP3tLltUsW2wBFjKWLZBNglyxcS+xsYkhlECogYHQQoeQAJkU/q1vPavttfZea+8t2SaQmTUTmmXZ1vrp6SVQ9as/+9DRfazdOm6f/+t/kaoCv3IC9llXHiDn6dM1P/74z//8hz/84bvVq1cvWb0E/r/kO/gL+rc//POaH9esefoheexagY99v24gAr96KfD//selH374Ibr9t35a8uzZswp0ugzFCaL/suj/XV3wEPTIJd/9hKB4+iGi4h8ZEb9eGn59IOz7P3/zGyoENm7c+HTNmjWr8e3T6w7SOw96HIoH+sTvn333RyQknm78cO2vmIbAr1IOtK9FDPy45j9Xf/+9ORVcgDMVrPh+9WqkUzZu/H37r9Jy+PWAQO8FGFiz5o+AgOn/orv9Pcz8/vvV/7nmx40fEk3xa4Ih8CsRBdQeJAwQKZAogQN0/DNhvr/6j2s2Pg38qmAI/GoEQeDHf169+nt+W4mEdNHusqDbRoAHDObUlPn9+6v/8M8bA78aPfErkAjtAAFi4H3OQHNzsLm5Gd0+fqN346OBQeCgO5FI+BIe6LlratBDE0g0rP7DmgANQuz7Kwi/5Pcf+PDHPyCvQLwqgAA4oIdK/m5PmZ/wqUTgC6ATJOCAEbkmEHjVWXhFQcCiGEmCD9d8B46h260RBLq7uxfMZHQegOHDAPYuX1UlEXhVKagKPF3zx2cuEBApnmimCHQHFxEEcDC/R4Jh46vLwqsHApYFgY0//vFZ15SHECd/aA4u7EnYjvWR91ev+fEpNhj2/RWEFyAM1iIKIEqQ8FT4CQRDItHs962emC8JSDAgFja+imIh8CpBgIXBxjV/fN/Ex9XITwSJMYd9AV8Wgv/Ag54DRMJUcPXqf376yrHwyoBAQkZP/+fq9wkDCW9njzwk4csr9B1qlkkIap674ru3Aq8WC6+QRFgbWIFchKmg9s3o8tb1vlt/DHAQgowDzVMb2Wffrfn9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"
)
_LOGO_COL_HQ_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAtAAAAHgCAMAAAC7G6qeAAADAFBMVEXiYR6amluaHx5gpV4jZBrgKR/a27Lk39qgophlY1ZhGiEjkyXOpRyh2qBgjCxcWhzXqlL48ePdqaPf2GKcXCKcoCSNdFm6xCj27c87lEMcIhjdXmC648TjI0T69N6Ux2x7qoS5tsR6doSFfIhhyWNHO0f+/bZ6x4PHvMYyK0L//3///wCsKEL48Ls7a0PleYP/AAAA/wD/f3+2/7b/tLSxsbH/f///uP/b9R0A//9///+q////AP9/f3+qqv8AAADtGiX6+/j16Qv78gns2hHu5yvpGRr+/vrsIigMhw3r2SkMeA339CkLBwovJw3r6erZ1xIYFhHX1izMyC1PRw/s504oGQ2tpy1tZxLu6G7nIxkOlA9IOA63ti3V19KOhyvWJhTSJSr49a38+e04NQ7w6o7Q6M71xyqMhxTYGRX29JCXlixvZypXVREtJygNaQ0uhy/NyBXUGihORy37+OZmWRHz99T59sv0tyv69tXwyRa1trOPx493dRLT9dOv2K5WVVJMSUqpp6rVNxKspxYaFSdwt3AlGSr183DKyMo4Ni7zpyp3ditQplAwljBOl05PFhHEui+VlpKXlhT0806GeRNLJxEseSzwlyqlmi3WRxKFeSr49beLiIvy66v799tuqG7p59e3theuGSqz5bNsaGuQGCmyJS13dnVYVivthykvCQhGOiztDCloWSmNuIxuFhfX1krb4w/59sVMCQ7Mx0nqeCmS1pFwFyfWVhPvphZLiEvm20zxtxYWCyfqhxftlxZzxXGuya379+Klmhbc4i23t0nXZhMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC1eXHVAAAAyHRSTlP////////0+v///////////g7//v////+k//////9Z/////////wP///8CAf+5//8BAQIDAwMCA/8BAgMBAgMA///////+/wn//////////////////v////7///////////Au//n/////+f///////////03//q7/kP///////////////////f///////////////v/////////U/+9x//7////////////////////+/8v//v////////7///////9p/////1og72gAAQAASURBVHja7P2JXxPptv+LpwiEhNERW9tu7e7du3uP95xzv/fe7+t17+u3MaQQQ6iEJCSRTghojMEMEmIcIGESsUEGAQERUUBQURpERVQcacV/6/es56mqVGVAUHHops7ZLbORvLNqPWt91mdJ/rN+re21d+/Bb69+e/Dgxr3oWv91rPUlWf8VrDXPx07du3z5xKlTV48d3Pu/1pFeB/pL5/nElStHjhy5cgVBfWzjepBeB/qLxnnvwaupVw7th+vQldGvju3duE70OtBfcPp89ZQM8VwC1/5Dh658dfXgeoxeB/pL5XnjsVOXj+zfX0KTqwRF6X99u3Hvxr+v/27Wgf4Cs429mGfAWQkXRvpQ6lfobLhe71gH+kvMnk8gnlmaI0TLTpyCvGOd6HWgv6zsGcLzryURnAnSkHYcuHfq2HoqvQ70lxaeD0R4VomQPnTgwIn1IL0O9BfFMwrPh4TphiBKQ5C+cu/Ueia9DvSXchg8+Pupy4f28+mGShUn77h86veD61F6HegvIXv+HWfPHM80HQU0l3dcJqfD9V/ZOtCfNc/oMIizZ8SxClCm4yQeanXJ/iNHDhy4t55KrwP9WeP8V1x7/vUCQMwCHXvBx9V0ya8I6Xunvt341/Xf2zrQnynPG0Fad4AUN2J45t4ln8CZ9JEDx08cWw/R60B/tqdBvvisUkUDrYpcXLkD5R1Qk0bf+N/rv791oD8/mn8/9a/LRy5coFl4BeVnlejCH7qLiYaz4e/rifQ60J/ZtXHvt1dPnbh85Mj+kkh8ToCzStQK33/oSup643Ad6M8tQH974vIBTDNNK6PIRSfAw4cPq9EVk4fQ9JMnm2WHrkDjcF0ovQ7053L9fe+xEwewTlQQjiPRuebkucePnz49zBEtSqzVCGloHB47uE70OtCfR3TeuPfgV/cO8K3BKJzVh89dlLyRSDIen2SRjirgqZ/sP3ToAAnS60yvA/0ZnAZ/P0V4jgCN/sjDb9YcPnnu1oNHly49epNxDhEthl2FY7SaHA7X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"
)
