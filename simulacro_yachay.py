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
            out[d] = {"nombre": str(r.get(col_n, "")).strip().upper(),
                      "grado": (g + (" " + s if s and s.lower() != "nan" else "")).strip()}
    return out


# ================================================================
# CALIFICACIÓN
# ================================================================
def clave_para(sim, grupo):
    claves = sim.get("claves", {})
    if grupo in claves and claves[grupo]:
        return claves[grupo]
    for g in GRUPOS:
        if claves.get(g):
            return claves[g]
    return ""


def puntaje_maximo(sim):
    return sum((c["hasta"] - c["desde"] + 1) * float(c["correcta"]) for c in sim["cursos"])


def calificar(sim, hoja):
    clave = clave_para(sim, hoja.get("grupo", ""))
    resp = hoja.get("respuestas", "")
    blanco = float(sim.get("puntaje_blanco", 0))
    out = {"correctas": 0, "incorrectas": 0, "blancos": 0, "puntaje": 0.0, "cursos": {}}
    for c in sim["cursos"]:
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
    mx = puntaje_maximo(sim)
    out["nota"] = round(max(out["puntaje"], 0) / mx * 20, 2) if mx else 0.0
    return out


def tabla_ranking(sim, filtro_aula=None, filtro_grupo=None):
    filas = []
    for hid, h in sim.get("hojas", {}).items():
        if filtro_aula and h.get("aula") != filtro_aula:
            continue
        if filtro_grupo and h.get("grupo") != filtro_grupo:
            continue
        c = calificar(sim, h)
        f = {"ID": hid, "DNI": h.get("dni", ""), "Apellidos y Nombres": h.get("nombre", "") or "(sin nombre)",
             "Aula": h.get("aula", ""), "Grupo": h.get("grupo", "")}
        for cn, cv in c["cursos"].items():
            f[cn] = cv["correctas"]
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
    cursos = [x["nombre"] for x in sim["cursos"]]
    cols = ["Puesto", "Apellidos y Nombres", "DNI", "Aula", "Grupo"]
    if detalle_cursos:
        cols += cursos
    cols += ["Correctas", "Incorrectas", "Puntaje", "Nota"]
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph
    est_cab = ParagraphStyle("cab", fontName="Helvetica-Bold", fontSize=6.5 if detalle_cursos else 8,
                             leading=7.5 if detalle_cursos else 9, alignment=1)
    cab = [Paragraph("Pto" if x == "Puesto" else x, est_cab) for x in cols]

    def _fmt(x, v):
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
            otros = len(cols) - 5
            anchos = [26, 175, 58, 30, 34] + [resto / otros] * otros
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
    for cu in sim["cursos"]:
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
    n = sim["num_preguntas"]
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
            fila = {"DNI": h.get("dni"), "Nombre": h.get("nombre"), "Grupo": h.get("grupo")}
            for cn, cv in c["cursos"].items():
                fila[f"{cn} (nota)"] = cv["nota"]
                fila[f"{cn} (pts)"] = cv["puntaje"]
            fila["Respuestas"] = h.get("respuestas", "")
            filas.append(fila)
        pd.DataFrame(filas).to_excel(w, sheet_name="Detalle", index=False)
        pd.DataFrame([{"Grupo": g, "Clave": sim["claves"].get(g, "")} for g in GRUPOS]).to_excel(
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
                "Aula": h.get("aula", ""), "Grupo": h.get("grupo", ""),
                "Puntaje": c["puntaje"], "Correctas": c["correctas"], "Promedio": c["nota"],
                "Medalla": {1: "🥇", 2: "🥈", 3: "🥉"}.get(int(r["Puesto"]), "")}
        for cn, cv in c["cursos"].items():
            fila[cn] = cv["nota"]
        ranking.append(fila)
    hist[f"SIMYACHAY_{sim['id']}"] = {
        "titulo": sim["titulo"], "fecha": sim.get("fecha", ""), "periodo": sim.get("periodo", ""),
        "tipo": "simulacro_yachay", "areas": [{"nombre": c["nombre"]} for c in sim["cursos"]],
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
# INTERFAZ
# ================================================================
def _selector_simulacro(datos, key):
    sims = datos["simulacros"]
    if not sims:
        st.info("Aún no hay simulacros. Créalo en la pestaña ⚙️ Configurar.")
        return None
    ids = sorted(sims, key=lambda i: sims[i].get("creado", ""), reverse=True)
    etiqueta = {i: f"{sims[i]['titulo']} — {sims[i].get('fecha', '')} ({len(sims[i].get('hojas', {}))} hojas)"
                for i in ids}
    return st.selectbox("Simulacro:", ids, format_func=lambda i: etiqueta[i], key=key)


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
               "periodo": "", "num_preguntas": 100, "puntaje_blanco": 0, "claves": {},
               "cursos": [{"nombre": n, "desde": a, "hasta": b, "correcta": 1.0, "incorrecta": 0.0}
                          for n, a, b in CURSOS_EJEMPLO], "hojas": {}}
    pfx = f"simy_{sid or 'nuevo'}_"

    c1, c2, c3 = st.columns([2, 1, 1])
    titulo = c1.text_input("Nombre del simulacro:", sim["titulo"], key=pfx + "tit")
    fecha = c2.text_input("Fecha:", sim.get("fecha", ""), key=pfx + "fec")
    periodo = c3.text_input("Periodo / Bimestre:", sim.get("periodo", ""), key=pfx + "per")
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
                      "num_preguntas": int(n), "puntaje_blanco": p_bl, "claves": claves, "cursos": cursos})
        if not sid:
            sid = datetime.now().strftime("%Y%m%d") + "_" + uuid.uuid4().hex[:5]
            nuevo.update({"id": sid, "creado": datetime.now().isoformat(),
                          "creado_por": st.session_state.get("usuario_actual", ""), "hojas": {}})
        datos["simulacros"][sid] = nuevo
        guardar_datos(datos)
        if nuevo.get("publicado"):
            publicar_en_historial(nuevo)       # mantener el historial al día
        st.success(f"Simulacro guardado. Puntaje máximo: {puntaje_maximo(nuevo):g}")

    if sid and (not _HOOKS["puede_borrar"] or _HOOKS["puede_borrar"]()):
        with st.expander("🗑️ Eliminar simulacro"):
            if st.checkbox("Confirmo que quiero borrarlo con todas sus hojas", key=pfx + "delok"):
                if st.button("Eliminar definitivamente", key=pfx + "del"):
                    quitar_de_historial(sim)
                    datos["simulacros"].pop(sid, None)
                    guardar_datos(datos)
                    st.success("Eliminado.")
                    st.rerun()

    if Path(HOJA_PDF).exists():
        st.markdown("---")
        st.download_button("📄 Descargar hoja de respuestas en blanco (PDF para imprimir)",
                           Path(HOJA_PDF).read_bytes(), "Hoja_Yachay.pdf", "application/pdf")


def _procesar_imagen(sim, img, mat, origen):
    r = omr.leer_hoja(img, sim["num_preguntas"])
    resp = "".join({"": "_"}.get(x, x) for x in r["respuestas"])
    dni = r["dni"] if re.fullmatch(r"\d{8}", r["dni"]) else r["dni"]
    info = mat.get(dni, {})
    clave = clave_para(sim, r["grupo"])
    return {"tmp_id": uuid.uuid4().hex[:8], "dni": dni, "nombre": info.get("nombre", ""),
            "grado": info.get("grado", ""), "aula": r["aula"], "grupo": r["grupo"],
            "respuestas": resp, "dudosas": [i + 1 for i, e in enumerate(r["estados"]) if e in ("duda", "doble")],
            "alertas": r["alertas"] + ([] if info else ["DNI no encontrado en matrícula"]),
            "origen": origen, "fecha_examen": f"{r['dia'] or ''}/{r['mes'] or ''}/{r['anio'] or ''}",
            "img": omr.imagen_revision(r, clave)}


def _guardar_lote(datos, sid, lote):
    sim = datos["simulacros"][sid]
    sim.setdefault("hojas", {})
    por_dni = {h.get("dni"): k for k, h in sim["hojas"].items()}
    nuevos = reemplazados = 0
    for h in lote:
        dni = norm_dni(h["dni"]) if re.fullmatch(r"\d{1,8}", str(h["dni"])) else str(h["dni"])
        hid = por_dni.get(dni) if re.fullmatch(r"\d{8}", dni) else None
        if hid:
            reemplazados += 1
        else:
            hid = uuid.uuid4().hex[:10]
            nuevos += 1
        sim["hojas"][hid] = {"dni": dni, "nombre": (h.get("nombre") or "").strip().upper(),
                             "grado": h.get("grado", ""), "aula": h.get("aula", ""),
                             "grupo": h.get("grupo", ""), "respuestas": h["respuestas"],
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
            grp = m3.selectbox("Grupo:", [""] + GRUPOS)
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
    vista = pd.DataFrame([{
        "Quitar": False, "DNI": h["dni"], "Apellidos y Nombres": h["nombre"], "Aula": h["aula"],
        "Grupo": h["grupo"], "Correctas": calificar(sim, h)["correctas"], "Puntaje": calificar(sim, h)["puntaje"],
        "Revisar": ", ".join(h["alertas"]), "Origen": h["origen"]} for h in lote])
    ed = st.data_editor(vista, use_container_width=True, hide_index=True, key=f"simy_ed_{sid}_{len(lote)}",
                        disabled=["Correctas", "Puntaje", "Revisar", "Origen"],
                        column_config={"Grupo": st.column_config.SelectboxColumn(options=[""] + GRUPOS)})
    for h, (_, fila) in zip(lote, ed.iterrows()):
        nd = str(fila["DNI"]).strip()
        if nd != h["dni"]:
            h["dni"] = nd
            if norm_dni(nd) in mat and not str(fila["Apellidos y Nombres"]).strip():
                h["nombre"] = mat[norm_dni(nd)]["nombre"]
        if str(fila["Apellidos y Nombres"]).strip() and fila["Apellidos y Nombres"] != h["nombre"]:
            h["nombre"] = str(fila["Apellidos y Nombres"]).strip().upper()
        h["aula"] = str(fila["Aula"] or "")
        h["grupo"] = str(fila["Grupo"] or "")
        h["_quitar"] = bool(fila["Quitar"])

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

    b1, b2 = st.columns(2)
    if b1.button("💾 Guardar hojas en el simulacro", type="primary", key="simy_guardar_lote"):
        validos = [h for h in lote if not h.get("_quitar")]
        sin_dni = [h for h in validos if not re.fullmatch(r"\d{8}", norm_dni(h["dni"]) or "")]
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
    fg = f2.selectbox("Grupo:", ["Todos"] + GRUPOS, key="simy_fg")
    top = f3.number_input("Top para publicar:", 3, 30, 10, key="simy_top")
    df = tabla_ranking(sim, None if fa == "Todas" else fa, None if fg == "Todos" else fg)
    if df.empty:
        st.info("No hay resultados con ese filtro.")
        return
    extra = " · ".join(x for x in [f"Aula {fa}" if fa != "Todas" else "", f"Grupo {fg}" if fg != "Todos" else ""] if x) \
        or "Ranking general"

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
        n_grp = e3.selectbox("Grupo:", [""] + GRUPOS, index=([""] + GRUPOS).index(h.get("grupo", "")) if h.get("grupo", "") in GRUPOS else 0,
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
                 "Máximo": puntaje_maximo(sim), "Nota": c["nota"], "_creado": sim.get("creado", "")}
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
    curso_de = {}
    for c in sim["cursos"]:
        for q in range(c["desde"], c["hasta"] + 1):
            curso_de[q] = c["nombre"]
    filas = []
    for q in range(sim["num_preguntas"]):
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
                      "Clave (A)": (sim["claves"].get("A", "") + " " * 100)[q].strip(),
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


def tab_simulacros_yachay(config=None, cargar_matricula=None, cargar_historial=None,
                          guardar_historial=None, backup_json=None, puede_borrar=None):
    _HOOKS.update({"cargar_matricula": cargar_matricula, "cargar_historial": cargar_historial,
                   "guardar_historial": guardar_historial, "backup_json": backup_json,
                   "puede_borrar": puede_borrar})
    st.header("🧾 Simulacros Yachay — Lectura de hojas y ranking")
    if Path(HOJA_PDF).exists():
        st.download_button("📄 Descargar HOJA DE RESPUESTAS en blanco (PDF para imprimir)",
                           Path(HOJA_PDF).read_bytes(), "Hoja_Yachay.pdf", "application/pdf",
                           key="simy_dl_hoja_top", type="primary")
    st.caption("Flujo: 1) ⚙️ Configurar el examen (claves y cursos) → 2) 📸 Escanear las hojas → "
               "3) 🏆 Ranking (imprimir / publicar) → 4) 📚 Historial del estudiante.")
    datos = cargar_datos()
    t = st.tabs(["⚙️ Configurar", "📸 Escanear", "🏆 Ranking", "📚 Historial", "📊 Análisis"])
    with t[0]:
        _tab_configurar(datos)
    with t[1]:
        _tab_escanear(datos)
    with t[2]:
        _tab_ranking(datos)
    with t[3]:
        _tab_historial(datos)
    with t[4]:
        _tab_analisis(datos)
