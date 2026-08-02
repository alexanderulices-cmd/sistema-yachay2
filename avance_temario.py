# ================================================================
# AVANCE DEL TEMARIO — ACADEMIA PREUNIVERSITARIA
# Módulo para SISTEMA YACHAY PRO
# Basado en el Temario de Admisión UNSAAC (Res. CU-575-2024-UNSAAC)
# ================================================================
"""
Cómo se integra en sistema_web.py (3 líneas, ver GUIA-AVANCE-TEMARIO.md):

    from avance_temario import tab_avance_docente, tab_avance_coordinacion

Este módulo no depende del resto del sistema: si google_sync existe lo usa,
si no, guarda todo en un archivo local avance_temario.json.
"""

import json
import io
from datetime import datetime, date, timedelta
from pathlib import Path

import streamlit as st
import pandas as pd

try:
    from google_sync import get_google_sync
except Exception:
    get_google_sync = None


# ================================================================
# 1. TEMARIO OFICIAL UNSAAC
# ================================================================
# Cada curso es una lista de temas. El nombre corto es lo que ve el
# docente; el número es el del temario oficial, para que cualquier
# reclamo se pueda contrastar con la resolución.

TEMARIO = {
    "Aritmética": [
        "Teoría de conjuntos",
        "Sistema de números naturales y enteros",
        "Sistema de números racionales",
        "Sucesiones y sumatorias notables",
        "Sistemas de numeración",
        "Divisibilidad",
        "Números primos",
        "Máximo común divisor y mínimo común múltiplo",
        "Razones y proporciones",
        "Magnitudes proporcionales",
        "Regla de tres y regla de tanto por ciento",
        "Regla de interés simple y compuesto",
        "Introducción a la estadística",
        "Introducción a las probabilidades",
    ],
    "Álgebra": [
        "Potenciación",
        "Polinomios",
        "Productos notables",
        "División de polinomios, teorema del resto y cocientes notables",
        "Factorización de polinomios",
        "Racionalización",
        "Ecuaciones de primer y segundo grado con una variable real",
        "Inecuaciones de primer y segundo grado",
        "Ecuaciones e inecuaciones con valor absoluto",
        "Matrices y determinantes",
        "Relaciones",
        "Función",
        "Funciones especiales",
        "Clases de funciones",
        "Operaciones con funciones",
        "Función exponencial",
        "Función logarítmica",
    ],
    "Geometría y Trigonometría": [
        "Nociones básicas de la geometría",
        "Segmento de recta",
        "Ángulos",
        "Triángulos",
        "Congruencia y semejanza de triángulos",
        "Relaciones métricas de triángulos rectángulos y oblicuángulos",
        "Cuadriláteros",
        "Circunferencia",
        "Polígonos",
        "Áreas de regiones",
        "Fundamentos de la trigonometría",
        "Razones trigonométricas de ángulos agudos",
        "Ángulo en posición normal",
        "Identidades trigonométricas",
        "Resolución de triángulos y ángulos verticales y horizontales",
        "Funciones trigonométricas",
    ],
    "Física": [
        "La física y magnitudes",
        "Vectores en el plano y el espacio",
        "Cinemática",
        "Dinámica lineal",
        "Estática",
        "Trabajo y energía",
        "Dinámica de rotación",
        "Movimiento oscilatorio",
        "Mecánica de fluidos",
        "Temperatura, dilatación y calor",
        "Termodinámica",
        "Electrostática",
        "Electrodinámica",
        "Electromagnetismo",
        "Movimiento ondulatorio",
        "Óptica",
        "Física moderna",
    ],
    "Química": [
        "Química y materia",
        "Estructura atómica",
        "Números cuánticos y configuración electrónica",
        "Tabla periódica moderna",
        "Enlace químico",
        "Nomenclatura de compuestos inorgánicos",
        "Masa atómica",
        "Reacciones químicas",
        "Reacciones de oxidación y reducción",
        "Estequiometría de las reacciones químicas",
        "Soluciones",
        "Equilibrio químico",
        "Hidrocarburos",
        "Alcoholes, fenoles y éteres",
        "Aldehídos y cetonas",
        "Ácidos carboxílicos y ésteres",
    ],
    "Biología": [
        "Concepto de biología y niveles de organización",
        "Composición química de la materia viviente",
        "Biomoléculas inorgánicas",
        "Biomoléculas orgánicas",
        "Célula",
        "Célula eucariota",
        "Nutrición",
        "Nivel sistémico",
        "Coordinación",
        "Reproducción",
        "Genética",
        "Evolución y origen de la vida",
        "Ecología, factores ecológicos y ecosistemas",
        "Flujo de energía y ciclos biogeoquímicos",
        "Diversidad biológica y deterioro de la flora y la fauna",
        "Contaminación, problemas ambientales y conservación",
    ],
    "Competencia Comunicativa": [
        "La comunicación",
        "El lenguaje",
        "Fonología y fonética",
        "Sílaba",
        "Acentuación gráfica o tildación",
        "Uso de las letras mayúsculas y minúsculas",
        "Signos de puntuación",
        "Sustantivo",
        "El pronombre",
        "El adjetivo",
        "El artículo y el adverbio",
        "El verbo",
        "Conectores lógico semánticos",
        "La sintaxis y oración gramatical",
        "El texto y la lectura",
        "Relaciones semánticas",
    ],
    "Historia": [
        "Ciencia histórica",
        "Hombre de la prehistoria",
        "Grandes culturas de la antigüedad",
        "Mundo greco romano",
        "Primeras culturas andinas",
        "Culturas preincas",
        "Civilización inca",
        "Mundo medieval y el tránsito al mundo moderno",
        "Expansión europea",
        "Conquista del Perú",
        "El periodo colonial peruano",
        "El mundo durante el siglo XVIII",
        "Movimientos sociales en el mundo colonial americano",
        "Tiempo de las revoluciones",
        "Crisis del orden colonial e independencia",
        "Construcción de la república peruana",
        "Estado peruano en transformación",
        "El mundo entre guerras",
        "Entre dictaduras y democracias: gobernantes del Perú siglos XX-XXI",
    ],
    "Geografía": [
        "Geografía y espacio geográfico",
        "Geosistema y espacio exterior",
        "Cartografía y sistemas de información geográfica",
        "Mapas: lectura e interpretación",
        "Relieve terrestre: origen y procesos dinámicos",
        "Espacio geográfico peruano: región andina",
        "Espacio geográfico peruano: región amazónica y costa",
        "Hidrografía del Perú: ríos y lagos",
        "Hidrografía del Perú: mar peruano",
        "Atmósfera y cambio climático",
        "Recursos naturales, conservación e impacto ambiental",
        "Riesgo de desastres en el Perú",
        "Dinámica poblacional en el Perú",
        "Actividades económicas extractivas en el Perú",
        "Actividades económicas reproductivas en el Perú",
        "Actividades del transporte en el Perú",
        "Geografía política del Perú y gestión territorial",
        "Espacio geográfico físico del Cusco",
        "Geografía de América",
        "Geografía de Europa, Asia, África, Oceanía y Antártida",
    ],
    "Economía": [
        "Conceptos generales",
        "Necesidades humanas",
        "Bienes y servicios",
        "Proceso económico",
        "Trabajo",
        "Capital",
        "Naturaleza",
        "Empresa",
        "Demanda",
        "Oferta",
        "Mercado",
        "Dinero e inflación",
        "Sistema financiero y crédito",
        "Distribución",
        "Sector público y presupuesto nacional",
        "Sector externo",
        "Crisis y ciclos",
        "Desarrollo y crecimiento económico",
    ],
    "Filosofía y Lógica": [
        "El problema del cosmos y concepciones de filosofía",
        "Historia de la filosofía: edad antigua",
        "Edad medieval y renacimiento",
        "La filosofía moderna y filosofía en el Perú",
        "Antropología filosófica: el problema del hombre",
        "Gnoseología: problema del conocimiento",
        "Corrientes del problema del conocimiento",
        "Problema de la ciencia: epistemología",
        "Problema del valor y la ética",
        "Lógica, lenguaje y pensamiento",
        "Falacias",
        "Pruebas formales en la lógica proposicional",
        "Tablas de verdad y razonamientos válidos",
        "Principios lógicos y lógica formal clásica",
        "Inferencias",
        "Lógica de clases",
        "Fórmulas booleanas y diagramas de Venn",
    ],
    "Educación Cívica": [
        "Derecho, ley y moral",
        "Valores cívicos sociales",
        "Persona y sociedad",
        "Familia",
        "Nación",
        "Estado",
        "Constitución política",
        "Derechos civiles y políticos",
        "Derechos económicos, sociales y culturales",
        "Poder legislativo",
        "Poder ejecutivo",
        "Poder judicial",
        "Organismos constitucionales autónomos",
        "Régimen económico",
        "Descentralización, gobiernos regionales y locales",
        "Derechos humanos",
        "Garantías constitucionales",
        "Sistemas de protección internacional de los DDHH",
    ],
}


# ================================================================
# 2. PESO DE CADA CURSO EN EL EXAMEN (nº de preguntas por área)
# ================================================================
# Esto es lo que convierte el módulo en algo útil: no es lo mismo
# atrasarse en Aritmética (14 preguntas) que en Cívica (8).

PESOS = {
    "A": {"Aritmética": 14, "Álgebra": 10, "Geometría y Trigonometría": 14,
          "Competencia Comunicativa": 14, "Física": 14, "Química": 14},
    "B": {"Aritmética": 14, "Álgebra": 10, "Competencia Comunicativa": 14,
          "Biología": 14, "Física": 14, "Química": 14},
    "C": {"Aritmética": 14, "Álgebra": 10, "Competencia Comunicativa": 14,
          "Historia": 12, "Geografía": 12, "Economía": 10, "Educación Cívica": 8},
    "D": {"Aritmética": 14, "Álgebra": 10, "Competencia Comunicativa": 14,
          "Historia": 12, "Geografía": 12, "Filosofía y Lógica": 10,
          "Educación Cívica": 8},
}

GRUPOS = {
    "GRUPO AB": ["A", "B"],
    "GRUPO CD": ["C", "D"],
}

ESTADOS = ["Pendiente", "En avance", "Concluido", "Reforzado"]

ESTADO_PCT = {"Pendiente": 0, "En avance": 50, "Concluido": 100, "Reforzado": 100}

ESTADO_COLOR = {
    "Pendiente": "#94a3b8",
    "En avance": "#f59e0b",
    "Concluido": "#16a34a",
    "Reforzado": "#2563eb",
}

ARCHIVO_AVANCE = "avance_temario.json"
ARCHIVO_CONFIG_CICLO = "ciclo_academia.json"

HOJA_AVANCE = "AvanceTemario"
COLS_AVANCE = ["clave", "anio", "ciclo", "grupo", "curso", "tema_num",
               "tema", "estado", "fecha", "sesion", "docente",
               "observacion", "actualizado"]


# ================================================================
# 3. CURSOS SEGÚN GRUPO
# ================================================================

def cursos_de_grupo(grupo):
    """Devuelve la lista de cursos que se dictan en un grupo."""
    areas = GRUPOS.get(grupo, [])
    cursos = []
    for a in areas:
        for c in PESOS.get(a, {}):
            if c not in cursos:
                cursos.append(c)
    return cursos


def peso_curso(grupo, curso):
    """Promedio de preguntas del curso en las áreas del grupo."""
    areas = GRUPOS.get(grupo, [])
    vals = [PESOS[a].get(curso, 0) for a in areas]
    vals = [v for v in vals if v > 0]
    return round(sum(vals) / len(vals), 1) if vals else 0


# ================================================================
# 4. PERSISTENCIA
# ================================================================

def _gs():
    if get_google_sync is None:
        return None
    try:
        return get_google_sync()
    except Exception:
        return None


def _clave(anio, ciclo, grupo, curso, tema_num):
    return f"{anio}|{ciclo}|{grupo}|{curso}|{tema_num}"


def _leer_local():
    p = Path(ARCHIVO_AVANCE)
    if not p.exists():
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _escribir_local(data):
    try:
        with open(ARCHIVO_AVANCE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


@st.cache_data(ttl=60, show_spinner=False)
def _leer_hoja_avance():
    """Lee la hoja de Google Sheets. Cacheado 60s para no saturar la API."""
    gs = _gs()
    if gs is None:
        return {}
    try:
        hojas = [w.title for w in gs.spreadsheet.worksheets()]
        if HOJA_AVANCE not in hojas:
            ws = gs.spreadsheet.add_worksheet(title=HOJA_AVANCE, rows=2000,
                                              cols=len(COLS_AVANCE))
            ws.append_row(COLS_AVANCE)
            return {}
        ws = gs.spreadsheet.worksheet(HOJA_AVANCE)
        registros = ws.get_all_records()
        return {str(r.get("clave", "")): r for r in registros if r.get("clave")}
    except Exception:
        return {}


def cargar_avance():
    """Google Sheets manda; el archivo local es respaldo."""
    remoto = _leer_hoja_avance()
    if remoto:
        local = _leer_local()
        local.update(remoto)
        _escribir_local(local)
        return local
    return _leer_local()


def guardar_avance(registros):
    """Guarda una lista de registros. Escribe local siempre y sube a Sheets."""
    data = _leer_local()
    for r in registros:
        r["actualizado"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        data[r["clave"]] = r
    _escribir_local(data)

    gs = _gs()
    if gs is None:
        return False, "Guardado solo en este equipo (sin conexión a la nube)."

    try:
        hojas = [w.title for w in gs.spreadsheet.worksheets()]
        if HOJA_AVANCE not in hojas:
            ws = gs.spreadsheet.add_worksheet(title=HOJA_AVANCE, rows=2000,
                                              cols=len(COLS_AVANCE))
            ws.append_row(COLS_AVANCE)
        else:
            ws = gs.spreadsheet.worksheet(HOJA_AVANCE)

        claves_existentes = ws.col_values(1)
        nuevas, actualizaciones = [], []
        for r in registros:
            fila = [str(r.get(c, "")) for c in COLS_AVANCE]
            if r["clave"] in claves_existentes:
                idx = claves_existentes.index(r["clave"]) + 1
                actualizaciones.append((idx, fila))
            else:
                nuevas.append(fila)

        for idx, fila in actualizaciones:
            ws.update(f"A{idx}:M{idx}", [fila])
        if nuevas:
            ws.append_rows(nuevas)

        _leer_hoja_avance.clear()
        return True, f"{len(registros)} tema(s) guardado(s) y sincronizado(s)."
    except Exception as e:
        return False, f"Guardado local. La nube no respondió: {e}"


def cargar_config_ciclo():
    p = Path(ARCHIVO_CONFIG_CICLO)
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"ciclo": "Ciclo Regular", "inicio": "", "examen": ""}


def guardar_config_ciclo(cfg):
    with open(ARCHIVO_CONFIG_CICLO, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


# ================================================================
# 5. CÁLCULO DEL AVANCE
# ================================================================

def resumen_curso(avance, anio, ciclo, grupo, curso):
    """Devuelve el estado agregado de un curso."""
    temas = TEMARIO.get(curso, [])
    total = len(temas)
    conteo = {e: 0 for e in ESTADOS}
    puntos = 0
    for i in range(total):
        r = avance.get(_clave(anio, ciclo, grupo, curso, i + 1))
        estado = (r or {}).get("estado", "Pendiente")
        if estado not in ESTADOS:
            estado = "Pendiente"
        conteo[estado] += 1
        puntos += ESTADO_PCT[estado]
    pct = round(puntos / total, 1) if total else 0.0
    return {
        "curso": curso,
        "total": total,
        "pct": pct,
        "peso": peso_curso(grupo, curso),
        **conteo,
    }


def tabla_grupo(avance, anio, ciclo, grupo):
    filas = [resumen_curso(avance, anio, ciclo, grupo, c)
             for c in cursos_de_grupo(grupo)]
    return pd.DataFrame(filas)


def dias_restantes(cfg):
    try:
        f = datetime.strptime(cfg.get("examen", ""), "%Y-%m-%d").date()
        return (f - date.today()).days
    except Exception:
        return None


def diagnostico(pct, dias):
    """Semáforo: cruza avance con tiempo restante hasta el examen."""
    if dias is None:
        return "—", "#94a3b8"
    if dias <= 0:
        return "Ciclo cerrado", "#64748b"
    # Referencia: a 30 días del examen se espera 80%; a 60 días, 60%.
    if dias <= 15:
        esperado = 95
    elif dias <= 30:
        esperado = 85
    elif dias <= 60:
        esperado = 65
    elif dias <= 90:
        esperado = 45
    else:
        esperado = 25
    brecha = pct - esperado
    if brecha >= 0:
        return "Al día", "#16a34a"
    if brecha >= -15:
        return "Ajustado", "#f59e0b"
    return "Atrasado", "#dc2626"


# ================================================================
# 6. VISTA DEL DOCENTE — marcar avance
# ================================================================

def tab_avance_docente(config=None):
    st.subheader("📚 Avance del Temario — UNSAAC")
    st.caption("Temario oficial aprobado por Res. CU-575-2024-UNSAAC")

    info = st.session_state.get("docente_info", {}) or {}
    docente = info.get("label") or st.session_state.get("usuario_actual", "—")
    cfg = cargar_config_ciclo()
    anio = date.today().year

    c1, c2 = st.columns(2)
    with c1:
        grupo = st.selectbox("Grupo", list(GRUPOS.keys()), key="av_doc_grupo")
    with c2:
        cursos = cursos_de_grupo(grupo)
        curso = st.selectbox("Curso que dictas", cursos, key="av_doc_curso")

    ciclo = cfg.get("ciclo", "Ciclo Regular")
    avance = cargar_avance()
    temas = TEMARIO.get(curso, [])

    res = resumen_curso(avance, anio, ciclo, grupo, curso)
    dias = dias_restantes(cfg)
    etiqueta, color = diagnostico(res["pct"], dias)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Avance", f"{res['pct']}%")
    m2.metric("Temas concluidos", f"{res['Concluido'] + res['Reforzado']}/{res['total']}")
    m3.metric("Peso en el examen", f"{res['peso']} preguntas")
    m4.markdown(
        f"<div style='background:{color};color:#fff;padding:14px;border-radius:10px;"
        f"text-align:center;font-weight:bold;'>{etiqueta}"
        f"<div style='font-size:.8rem;font-weight:normal;'>"
        f"{'' if dias is None else f'{dias} días para el examen'}</div></div>",
        unsafe_allow_html=True)

    st.progress(min(res["pct"] / 100, 1.0))
    st.markdown("---")

    st.markdown("#### Marca lo que ya dictaste")
    st.caption("Solo cambia lo que avanzaste hoy y pulsa guardar al final.")

    fecha_sesion = st.date_input("Fecha de la sesión", value=date.today(),
                                 key="av_doc_fecha")

    cambios = []
    for i, tema in enumerate(temas, start=1):
        clave = _clave(anio, ciclo, grupo, curso, i)
        actual = avance.get(clave, {})
        estado_prev = actual.get("estado", "Pendiente")
        if estado_prev not in ESTADOS:
            estado_prev = "Pendiente"

        col_t, col_e, col_o = st.columns([5, 2, 3])
        with col_t:
            punto = ESTADO_COLOR[estado_prev]
            st.markdown(
                f"<div style='padding:6px 0;'>"
                f"<span style='display:inline-block;width:10px;height:10px;"
                f"border-radius:50%;background:{punto};margin-right:8px;'></span>"
                f"<b>{i}.</b> {tema}</div>", unsafe_allow_html=True)
        with col_e:
            nuevo = st.selectbox("Estado", ESTADOS,
                                 index=ESTADOS.index(estado_prev),
                                 key=f"av_est_{clave}",
                                 label_visibility="collapsed")
        with col_o:
            obs = st.text_input("Observación", value=actual.get("observacion", ""),
                                key=f"av_obs_{clave}",
                                placeholder="Sesión, dificultad, pendiente…",
                                label_visibility="collapsed")

        if nuevo != estado_prev or obs != actual.get("observacion", ""):
            cambios.append({
                "clave": clave,
                "anio": anio,
                "ciclo": ciclo,
                "grupo": grupo,
                "curso": curso,
                "tema_num": i,
                "tema": tema,
                "estado": nuevo,
                "fecha": fecha_sesion.strftime("%Y-%m-%d"),
                "sesion": actual.get("sesion", ""),
                "docente": docente,
                "observacion": obs,
            })

    st.markdown("---")
    if cambios:
        st.info(f"Tienes {len(cambios)} cambio(s) sin guardar.")
    cg1, cg2 = st.columns(2)
    with cg1:
        if st.button("💾 GUARDAR AVANCE", type="primary", use_container_width=True,
                     disabled=not cambios, key="av_doc_guardar"):
            ok, msg = guardar_avance(cambios)
            (st.success if ok else st.warning)(msg)
            st.rerun()
    with cg2:
        try:
            pdf = generar_pdf_docente(avance, anio, ciclo, grupo, curso,
                                      docente, dias)
            st.download_button(
                "📄 Descargar mi avance en PDF",
                data=pdf,
                file_name=(f"avance_{curso.replace(' ', '_')}_"
                           f"{grupo.replace(' ', '')}_{anio}.pdf"),
                mime="application/pdf", use_container_width=True,
                key="av_doc_pdf")
        except Exception as e:
            st.caption(f"No se pudo preparar el PDF: {e}")


# ================================================================
# 7. VISTA DE COORDINACIÓN — panel de control
# ================================================================

def tab_avance_coordinacion(config=None):
    st.subheader("📊 Control de Avance — Academia Preuniversitaria")

    cfg = cargar_config_ciclo()
    anio = date.today().year

    with st.expander("⚙️ Configurar el ciclo", expanded=not cfg.get("examen")):
        c1, c2, c3 = st.columns(3)
        with c1:
            nciclo = st.text_input("Nombre del ciclo", value=cfg.get("ciclo", ""))
        with c2:
            ini = st.date_input(
                "Inicio de clases",
                value=datetime.strptime(cfg["inicio"], "%Y-%m-%d").date()
                if cfg.get("inicio") else date.today())
        with c3:
            exa = st.date_input(
                "Fecha del examen",
                value=datetime.strptime(cfg["examen"], "%Y-%m-%d").date()
                if cfg.get("examen") else date.today() + timedelta(days=90))
        if st.button("Guardar configuración", key="av_cfg_save"):
            guardar_config_ciclo({
                "ciclo": nciclo,
                "inicio": ini.strftime("%Y-%m-%d"),
                "examen": exa.strftime("%Y-%m-%d"),
            })
            st.success("Configuración guardada.")
            st.rerun()

    ciclo = cfg.get("ciclo", "Ciclo Regular")
    dias = dias_restantes(cfg)
    avance = cargar_avance()

    if dias is not None:
        if dias > 0:
            st.info(f"**{ciclo}** — faltan **{dias} días** para el examen de admisión.")
        else:
            st.warning(f"**{ciclo}** — la fecha del examen ya pasó.")

    tab1, tab2, tab3 = st.tabs(
        ["🚦 Semáforo por curso", "👤 Por docente", "📥 Reportes"])

    # ---------- Semáforo ----------
    with tab1:
        for grupo in GRUPOS:
            df = tabla_grupo(avance, anio, ciclo, grupo)
            if df.empty:
                continue
            pct_grupo = round((df["pct"] * df["peso"]).sum() / df["peso"].sum(), 1) \
                if df["peso"].sum() else 0
            st.markdown(f"### {grupo} — avance ponderado: **{pct_grupo}%**")
            st.caption("Ponderado por número de preguntas del examen, "
                       "no por cantidad de temas.")

            for _, r in df.sort_values("pct").iterrows():
                etiqueta, color = diagnostico(r["pct"], dias)
                st.markdown(
                    f"""<div style='display:flex;align-items:center;gap:12px;
                    padding:10px 14px;margin-bottom:6px;border-radius:8px;
                    background:#f8fafc;border-left:6px solid {color};'>
                    <div style='flex:3;'><b>{r['curso']}</b>
                    <span style='color:#64748b;font-size:.85rem;'>
                    · {r['peso']} preguntas</span></div>
                    <div style='flex:4;background:#e2e8f0;border-radius:20px;height:14px;'>
                    <div style='width:{min(r['pct'],100)}%;background:{color};
                    height:14px;border-radius:20px;'></div></div>
                    <div style='flex:1;text-align:right;'><b>{r['pct']}%</b></div>
                    <div style='flex:1;text-align:right;color:{color};
                    font-weight:bold;font-size:.85rem;'>{etiqueta}</div>
                    </div>""", unsafe_allow_html=True)

            atrasados = [r["curso"] for _, r in df.iterrows()
                         if diagnostico(r["pct"], dias)[0] == "Atrasado"]
            if atrasados:
                st.error("Requieren intervención inmediata: " + ", ".join(atrasados))
            st.markdown("---")

    # ---------- Por docente ----------
    with tab2:
        filas = []
        for r in avance.values():
            if str(r.get("anio")) != str(anio):
                continue
            filas.append(r)
        if not filas:
            st.info("Todavía no hay registros de avance.")
        else:
            df = pd.DataFrame(filas)
            df["concluido"] = df["estado"].isin(["Concluido", "Reforzado"])
            resumen = (df.groupby(["docente", "grupo", "curso"])
                         .agg(temas_registrados=("tema", "count"),
                              concluidos=("concluido", "sum"),
                              ultima_actualizacion=("actualizado", "max"))
                         .reset_index())
            resumen["% del curso"] = resumen.apply(
                lambda x: round(100 * x["concluidos"] /
                                max(len(TEMARIO.get(x["curso"], [])), 1), 1), axis=1)
            st.dataframe(resumen, use_container_width=True, hide_index=True)

            st.markdown("#### Docentes sin registrar en los últimos 14 días")
            limite = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
            inactivos = resumen[
                resumen["ultima_actualizacion"].astype(str) < limite]
            if inactivos.empty:
                st.success("Todos los docentes registraron avance recientemente.")
            else:
                for _, r in inactivos.iterrows():
                    st.warning(f"**{r['docente']}** — {r['curso']} ({r['grupo']}) · "
                               f"último registro: {r['ultima_actualizacion']}")

    # ---------- Reportes ----------
    with tab3:
        filas = []
        for grupo in GRUPOS:
            for curso in cursos_de_grupo(grupo):
                for i, tema in enumerate(TEMARIO.get(curso, []), start=1):
                    r = avance.get(_clave(anio, ciclo, grupo, curso, i), {})
                    filas.append({
                        "Grupo": grupo,
                        "Curso": curso,
                        "N°": i,
                        "Tema": tema,
                        "Estado": r.get("estado", "Pendiente"),
                        "Fecha": r.get("fecha", ""),
                        "Docente": r.get("docente", ""),
                        "Observación": r.get("observacion", ""),
                    })
        df_full = pd.DataFrame(filas)
        st.dataframe(df_full, use_container_width=True, hide_index=True,
                     height=400)

        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_full.to_excel(w, sheet_name="Avance detallado", index=False)
            for grupo in GRUPOS:
                tabla_grupo(avance, anio, ciclo, grupo).to_excel(
                    w, sheet_name=grupo.replace(" ", "_")[:30], index=False)
        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                "📥 Descargar reporte en Excel",
                data=buf.getvalue(),
                file_name=f"avance_temario_{ciclo.replace(' ', '_')}_{anio}.xlsx",
                mime=("application/vnd.openxmlformats-officedocument."
                      "spreadsheetml.sheet"),
                use_container_width=True, key="av_coord_xlsx")
        with d2:
            try:
                pdf = generar_pdf_coordinacion(avance, anio, ciclo, dias)
                st.download_button(
                    "📄 Informe de seguimiento en PDF",
                    data=pdf,
                    file_name=f"informe_avance_{ciclo.replace(' ', '_')}_{anio}.pdf",
                    mime="application/pdf", use_container_width=True,
                    type="primary", key="av_coord_pdf")
            except Exception as e:
                st.caption(f"No se pudo preparar el PDF: {e}")

        st.markdown("---")
        st.markdown("#### Reporte individual por docente")
        cc1, cc2 = st.columns(2)
        with cc1:
            g_sel = st.selectbox("Grupo", list(GRUPOS.keys()), key="av_rep_grupo")
        with cc2:
            c_sel = st.selectbox("Curso", cursos_de_grupo(g_sel),
                                 key="av_rep_curso")
        doc_nom = ""
        for i in range(len(TEMARIO.get(c_sel, []))):
            r = avance.get(_clave(anio, ciclo, g_sel, c_sel, i + 1), {})
            if r.get("docente"):
                doc_nom = r["docente"]
                break
        try:
            pdf_ind = generar_pdf_docente(avance, anio, ciclo, g_sel, c_sel,
                                          doc_nom or "—", dias)
            st.download_button(
                f"📄 Descargar detalle de {c_sel}",
                data=pdf_ind,
                file_name=(f"avance_{c_sel.replace(' ', '_')}_"
                           f"{g_sel.replace(' ', '')}_{anio}.pdf"),
                mime="application/pdf", use_container_width=True,
                key="av_rep_pdf_ind")
        except Exception as e:
            st.caption(f"No se pudo preparar el PDF: {e}")


# ================================================================
# 8. REPORTES EN PDF
# ================================================================

def _estilos_pdf():
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib import colors
    ss = getSampleStyleSheet()
    return {
        "titulo": ParagraphStyle("t", parent=ss["Title"], fontSize=15,
                                 textColor=colors.HexColor("#001e7c"),
                                 spaceAfter=2, alignment=TA_CENTER),
        "sub": ParagraphStyle("s", parent=ss["Normal"], fontSize=9,
                              textColor=colors.HexColor("#475569"),
                              alignment=TA_CENTER, spaceAfter=10),
        "h2": ParagraphStyle("h", parent=ss["Heading2"], fontSize=11,
                             textColor=colors.HexColor("#001e7c"),
                             spaceBefore=10, spaceAfter=4),
        "n": ParagraphStyle("n", parent=ss["Normal"], fontSize=8.5,
                            leading=11),
        "pie": ParagraphStyle("p", parent=ss["Normal"], fontSize=7.5,
                              textColor=colors.HexColor("#64748b"),
                              alignment=TA_CENTER),
    }


def _encabezado(story, titulo, subtitulo, est):
    from reportlab.platypus import Paragraph, Spacer
    story.append(Paragraph(titulo, est["titulo"]))
    story.append(Paragraph(subtitulo, est["sub"]))
    story.append(Spacer(1, 4))


def generar_pdf_coordinacion(avance, anio, ciclo, dias, institucion="ACADEMIA YACHAY"):
    """Informe de seguimiento del avance de todos los docentes."""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle)
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    est = _estilos_pdf()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=1.6 * cm, rightMargin=1.6 * cm,
                            topMargin=1.4 * cm, bottomMargin=1.4 * cm)
    story = []

    hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
    sub = f"{ciclo} {anio} &nbsp;·&nbsp; Emitido el {hoy}"
    if dias is not None and dias > 0:
        sub += f" &nbsp;·&nbsp; Faltan {dias} días para el examen"
    _encabezado(story, f"{institucion}<br/>INFORME DE AVANCE DEL TEMARIO", sub, est)
    story.append(Paragraph(
        "Temario de Admisión UNSAAC aprobado por Res. CU-575-2024-UNSAAC. "
        "El porcentaje del grupo está ponderado por el número de preguntas "
        "que cada curso tiene en el examen.", est["n"]))
    story.append(Spacer(1, 8))

    for grupo in GRUPOS:
        df = tabla_grupo(avance, anio, ciclo, grupo)
        if df.empty:
            continue
        pond = round((df["pct"] * df["peso"]).sum() / df["peso"].sum(), 1) \
            if df["peso"].sum() else 0
        story.append(Paragraph(
            f"{grupo} — avance ponderado: {pond}%", est["h2"]))

        data = [["Curso", "Preg.", "Temas", "Concl.", "En avance",
                 "Pend.", "Avance", "Estado"]]
        estilos_fila = []
        for i, (_, r) in enumerate(df.sort_values("pct").iterrows(), start=1):
            etiqueta, color = diagnostico(r["pct"], dias)
            data.append([
                Paragraph(str(r["curso"]), est["n"]),
                str(int(r["peso"])), str(int(r["total"])),
                str(int(r["Concluido"] + r["Reforzado"])),
                str(int(r["En avance"])), str(int(r["Pendiente"])),
                f"{r['pct']}%", etiqueta,
            ])
            estilos_fila.append(
                ("TEXTCOLOR", (7, i), (7, i), colors.HexColor(color)))

        t = Table(data, colWidths=[5.2 * cm, 1.3 * cm, 1.3 * cm, 1.5 * cm,
                                   1.9 * cm, 1.4 * cm, 1.7 * cm, 2.2 * cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#001e7c")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#f8fafc")]),
            ("FONTNAME", (7, 1), (7, -1), "Helvetica-Bold"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ] + estilos_fila))
        story.append(t)

        atras = [r["curso"] for _, r in df.iterrows()
                 if diagnostico(r["pct"], dias)[0] == "Atrasado"]
        if atras:
            story.append(Spacer(1, 4))
            story.append(Paragraph(
                f"<b>Requieren intervención:</b> {', '.join(atras)}", est["n"]))
        story.append(Spacer(1, 6))

    # --- Responsables por curso ---
    filas = [r for r in avance.values() if str(r.get("anio")) == str(anio)]
    if filas:
        df = pd.DataFrame(filas)
        df["concl"] = df["estado"].isin(["Concluido", "Reforzado"])
        res = (df.groupby(["docente", "grupo", "curso"])
                 .agg(concl=("concl", "sum"), ult=("actualizado", "max"))
                 .reset_index())
        story.append(Paragraph("Registro por docente", est["h2"]))
        data = [["Docente", "Grupo", "Curso", "Temas concluidos",
                 "Último registro"]]
        for _, r in res.sort_values(["grupo", "curso"]).iterrows():
            tot = len(TEMARIO.get(r["curso"], [])) or 1
            data.append([
                Paragraph(str(r["docente"]), est["n"]),
                str(r["grupo"]).replace("GRUPO ", ""),
                Paragraph(str(r["curso"]), est["n"]),
                f"{int(r['concl'])}/{tot}",
                str(r["ult"])[:16],
            ])
        t = Table(data, colWidths=[4.8 * cm, 1.6 * cm, 4.6 * cm,
                                   2.8 * cm, 3.0 * cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0891b2")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#f0f9ff")]),
        ]))
        story.append(t)

    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "_______________________________<br/>"
        "Coordinación Académica", est["pie"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Documento generado automáticamente por SISTEMA YACHAY PRO", est["pie"]))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()


def generar_pdf_docente(avance, anio, ciclo, grupo, curso, docente, dias,
                        institucion="ACADEMIA YACHAY"):
    """Detalle tema por tema del curso de un docente."""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle)
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    est = _estilos_pdf()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=1.6 * cm, rightMargin=1.6 * cm,
                            topMargin=1.4 * cm, bottomMargin=1.4 * cm)
    story = []

    res = resumen_curso(avance, anio, ciclo, grupo, curso)
    etiqueta, color = diagnostico(res["pct"], dias)
    hoy = datetime.now().strftime("%d/%m/%Y")

    _encabezado(story, f"{institucion}<br/>AVANCE DEL TEMARIO — {curso.upper()}",
                f"{grupo} &nbsp;·&nbsp; {ciclo} {anio} &nbsp;·&nbsp; "
                f"Docente: {docente} &nbsp;·&nbsp; {hoy}", est)

    resumen = Table([[
        f"Avance\n{res['pct']}%",
        f"Concluidos\n{res['Concluido'] + res['Reforzado']}/{res['total']}",
        f"Peso en el examen\n{int(res['peso'])} preguntas",
        f"Estado\n{etiqueta}",
    ]], colWidths=[4.2 * cm] * 4)
    resumen.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("TEXTCOLOR", (3, 0), (3, 0), colors.HexColor(color)),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(resumen)
    story.append(Spacer(1, 10))

    data = [["N°", "Tema del temario oficial", "Estado", "Fecha", "Observación"]]
    estilos_fila = []
    for i, tema in enumerate(TEMARIO.get(curso, []), start=1):
        r = avance.get(_clave(anio, ciclo, grupo, curso, i), {})
        estado = r.get("estado", "Pendiente")
        if estado not in ESTADOS:
            estado = "Pendiente"
        data.append([
            str(i),
            Paragraph(tema, est["n"]),
            estado,
            str(r.get("fecha", "—")),
            Paragraph(str(r.get("observacion", "")), est["n"]),
        ])
        estilos_fila.append(
            ("TEXTCOLOR", (2, i), (2, i), colors.HexColor(ESTADO_COLOR[estado])))

    t = Table(data, colWidths=[1.0 * cm, 7.0 * cm, 2.2 * cm, 2.2 * cm, 5.4 * cm],
              repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#001e7c")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (2, 1), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (3, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ] + estilos_fila))
    story.append(t)

    story.append(Spacer(1, 20))
    firmas = Table([[
        "_______________________________\nDocente del curso",
        "_______________________________\nCoordinación Académica",
    ]], colWidths=[8.4 * cm, 8.4 * cm])
    firmas.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#334155")),
    ]))
    story.append(firmas)

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()
