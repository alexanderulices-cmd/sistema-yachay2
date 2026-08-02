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
               "observacion", "evals", "actualizado"]

# Los exámenes se guardan con el nombre del área, que no siempre coincide
# exactamente con el nombre del curso en el temario oficial.
ALIAS_AREA = {
    "Geometría y Trigonometría": ["Geometría", "Trigonometría",
                                  "Geometria", "Trigonometria"],
    "Competencia Comunicativa": ["Competencia Lingüística", "Comunicación",
                                 "Lenguaje", "Razonamiento Verbal"],
    "Filosofía y Lógica": ["Filosofía", "Lógica"],
    "Educación Cívica": ["Cívica", "Educación Ciudadana"],
}

# Nota mínima vigesimal de aprobación usada en la academia.
# Archivo donde 'Registrar Notas → Nueva Evaluación' deja las notas.
NOTA_UMBRAL = 11.0
ARCHIVO_RESULTADOS_NOTAS = "resultados.json"


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

    st.markdown("---")
    with st.expander("🎯 Cruzar con las notas de mis exámenes", expanded=False):
        nt = notas_del_curso(grupo, curso)
        if nt["promedio"] is not None:
            etiqueta, color, lectura = cuadrante(res["pct"], nt["promedio"])
            k1, k2, k3 = st.columns(3)
            k1.metric("Promedio del curso", nt["promedio"])
            k2.metric(f"Sobre {NOTA_UMBRAL}", f"{nt['pct_aprob']}%")
            k3.markdown(
                f"<div style='background:{color};color:#fff;padding:12px;"
                f"border-radius:8px;text-align:center;font-weight:bold;'>"
                f"{etiqueta}</div>", unsafe_allow_html=True)
            st.caption(lectura)
            st.markdown("---")
        seccion_vincular_evaluaciones(avance, anio, ciclo, grupo, curso, docente)


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
        if st.button("💾 Guardar configuración", key="av_cfg_save",
                     type="primary", use_container_width=True):
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

    tab1, tab4, tab2, tab3 = st.tabs(
        ["🚦 Semáforo por curso", "🎯 Dictado vs Aprendido",
         "👤 Por docente", "📥 Reportes"])

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

    # ---------- Dictado vs Aprendido ----------
    with tab4:
        st.markdown("Cruza lo que **se dictó** con lo que los alumnos "
                    "**demostraron en los exámenes** que ya registras en el "
                    "sistema. Un curso puede ir al 90% de avance y aun así "
                    "ser el que más puntos te está costando.")
        hay_notas = False
        for grupo in GRUPOS:
            filas = tabla_dictado_vs_aprendido(avance, anio, ciclo, grupo)
            st.markdown(f"### {grupo}")
            for f in filas:
                if f["promedio"] is not None:
                    hay_notas = True
                prom_txt = "sin notas" if f["promedio"] is None else \
                    f"promedio {f['promedio']} · {f['pct_aprob']}% sobre {NOTA_UMBRAL}"
                st.markdown(
                    f"""<div style='padding:10px 14px;margin-bottom:6px;
                    border-radius:8px;background:#f8fafc;
                    border-left:6px solid {f['color']};'>
                    <div style='display:flex;justify-content:space-between;
                    align-items:center;'>
                    <div><b>{f['curso']}</b>
                    <span style='color:#64748b;font-size:.85rem;'>
                    · {int(f['peso'])} preguntas · avance {f['avance']}% ·
                    {prom_txt}</span></div>
                    <div style='color:{f['color']};font-weight:bold;'>
                    {f['estado']}</div></div>
                    <div style='color:#475569;font-size:.82rem;margin-top:4px;'>
                    {f['lectura']}</div></div>""", unsafe_allow_html=True)

            criticos = [f["curso"] for f in filas
                        if f["estado"] == "Dictado, no aprendido"]
            if criticos:
                st.error("**Se avanzó pero no se asimiló:** " +
                         ", ".join(criticos) +
                         ". Estos cursos no necesitan más velocidad, "
                         "necesitan repaso.")
            st.markdown("---")

        if not hay_notas:
            st.info("Todavía no hay notas registradas para los grupos "
                    "preuniversitarios. En cuanto apliques exámenes desde "
                    "Exámenes Semanales o YACHAY QAWAY, este panel se llena solo.")

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
        st.markdown("#### Planilla para marcar a mano")
        st.caption("Hoja impresa con todos los cursos y sus temas, con "
                   "casilleros vacíos para marcar con aspa y firmar.")
        pc1, pc2 = st.columns(2)
        for col, grupo_pl in zip([pc1, pc2], list(GRUPOS.keys())):
            with col:
                try:
                    pl = generar_pdf_planilla(grupo_pl, ciclo, anio)
                    st.download_button(
                        f"🖨️ Planilla {grupo_pl}",
                        data=pl,
                        file_name=(f"planilla_temario_{grupo_pl.replace(' ', '')}"
                                   f"_{anio}.pdf"),
                        mime="application/pdf", use_container_width=True,
                        key=f"av_planilla_{grupo_pl}")
                except Exception as e:
                    st.caption(f"No se pudo generar: {e}")

        st.markdown("---")
        st.markdown("#### Temario completo por área de postulación")
        st.caption("Una hoja por área con todos sus cursos, cuánto pesa cada "
                   "uno y sus temas. Sirve para entregar al postulante.")
        _ca = st.columns(4)
        for _col, _ar in zip(_ca, ["A", "B", "C", "D"]):
            with _col:
                try:
                    _pa = generar_pdf_area(_ar, ciclo, anio)
                    st.download_button(
                        f"📘 Área {_ar}", data=_pa,
                        file_name=f"temario_area_{_ar}_{anio}.pdf",
                        mime="application/pdf", use_container_width=True,
                        key=f"av_area_{_ar}")
                except Exception as e:
                    st.caption(f"Error: {e}")

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


# ================================================================
# 9. CRUCE CON LAS NOTAS YA REGISTRADAS
# ================================================================
# Responde la pregunta que un checklist no puede responder:
# el tema se dictó, ¿pero el alumno lo entendió?

def _coincide_area(curso, area_examen):
    """Compara el curso del temario con el área con que se guardó el examen."""
    a = str(area_examen).strip().lower()
    if not a:
        return False
    if a == curso.lower():
        return True
    for alias in ALIAS_AREA.get(curso, []):
        if a == alias.lower():
            return True
    return curso.lower().startswith(a) or a.startswith(curso.lower()[:8])


def _coincide_grupo(grupo, grado_examen):
    """GRUPO AB coincide con 'GRUPO AB — CEPRE UNSAAC' y variantes."""
    g = str(grado_examen).upper().replace("—", "-")
    return grupo.upper().replace("GRUPO ", "").strip() in g


@st.cache_data(ttl=120, show_spinner=False)
def _leer_resultados():
    """Aplana todas las notas registradas a filas comparables.

    Fuente principal: resultados.json, que es donde "Registrar Notas →
    Nueva Evaluación" deja cada estudiante con sus áreas anidadas.
    Si no está en disco, se recupera del blob 'resultados_json' que el
    sistema guarda en la hoja Config.
    Fuente secundaria: la hoja Resultados (YACHAY QAWAY / exámenes por clave).
    """
    filas = []

    # --- Fuente 1: notas de Nueva Evaluación ---
    data = []
    p = Path(ARCHIVO_RESULTADOS_NOTAS)
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
    if not data:
        gs = _gs()
        if gs is not None:
            try:
                ws = gs._get_hoja("config")
                if ws:
                    for row in ws.get_all_values():
                        if row and row[0] == "resultados_json":
                            data = json.loads(row[1])
                            break
            except Exception:
                data = []

    for r in data or []:
        periodo = str(r.get("periodo", ""))
        titulo = str(r.get("titulo", ""))
        fecha = str(r.get("fecha", ""))
        eval_id = f"{fecha}|{periodo}|{titulo}"
        for a in r.get("areas", []) or []:
            try:
                nota = float(a.get("nota") or 0)
            except (TypeError, ValueError):
                continue
            if nota <= 0:
                continue
            filas.append({
                "eval_id": eval_id,
                "eval_titulo": titulo or periodo or "Evaluación",
                "periodo": periodo,
                "fecha": fecha,
                "grado": r.get("grado", ""),
                "area": a.get("nombre", ""),
                "nota": nota,
                "docente": r.get("docente_nombre") or r.get("docente", ""),
            })

    # --- Fuente 2: hoja Resultados (formato plano) ---
    gs = _gs()
    if gs is not None:
        try:
            for r in gs.leer_resultados():
                try:
                    nota = float(r.get("nota") or 0)
                except (TypeError, ValueError):
                    continue
                if nota <= 0:
                    continue
                filas.append({
                    "eval_id": str(r.get("eval_id", "")),
                    "eval_titulo": r.get("eval_titulo", ""),
                    "periodo": "",
                    "fecha": r.get("fecha", ""),
                    "grado": r.get("grado", ""),
                    "area": r.get("area", ""),
                    "nota": nota,
                    "docente": r.get("docente", ""),
                })
        except Exception:
            pass

    return filas


def notas_del_curso(grupo, curso, eval_ids=None):
    """Promedio y detalle de las evaluaciones de un curso en un grupo."""
    filas = []
    for r in _leer_resultados():
        if not _coincide_grupo(grupo, r.get("grado", "")):
            continue
        if not _coincide_area(curso, r.get("area", "")):
            continue
        if eval_ids and str(r.get("eval_id")) not in eval_ids:
            continue
        try:
            filas.append(float(r.get("nota") or 0))
        except (TypeError, ValueError):
            continue
    if not filas:
        return {"promedio": None, "alumnos": 0, "aprobados": 0, "pct_aprob": None}
    aprob = sum(1 for n in filas if n >= NOTA_UMBRAL)
    return {
        "promedio": round(sum(filas) / len(filas), 1),
        "alumnos": len(filas),
        "aprobados": aprob,
        "pct_aprob": round(100 * aprob / len(filas), 1),
    }


def evaluaciones_disponibles(grupo, curso):
    """Lista de exámenes ya aplicados que corresponden a este curso."""
    vistos, salida = set(), []
    for r in _leer_resultados():
        if not _coincide_grupo(grupo, r.get("grado", "")):
            continue
        if not _coincide_area(curso, r.get("area", "")):
            continue
        eid = str(r.get("eval_id", ""))
        if eid and eid not in vistos:
            vistos.add(eid)
            periodo = r.get("periodo", "")
            titulo = r.get("eval_titulo", "Sin título")
            salida.append({
                "eval_id": eid,
                "titulo": f"{periodo} · {titulo}" if periodo else titulo,
                "fecha": r.get("fecha", ""),
            })
    return sorted(salida, key=lambda x: str(x["fecha"]), reverse=True)


def cuadrante(pct_avance, promedio):
    """Cruza cobertura con resultados. Devuelve (etiqueta, color, lectura)."""
    if promedio is None:
        return ("Sin evaluar", "#94a3b8",
                "Se dictó pero todavía no hay notas que lo respalden.")
    alto_av = pct_avance >= 60
    alto_no = promedio >= NOTA_UMBRAL
    if alto_av and alto_no:
        return ("Consolidado", "#16a34a",
                "Buen avance y los alumnos responden. Mantener el ritmo.")
    if alto_av and not alto_no:
        return ("Dictado, no aprendido", "#dc2626",
                "Se avanzó rápido pero las notas no acompañan. "
                "Conviene frenar y reforzar antes de seguir.")
    if not alto_av and alto_no:
        return ("En ruta", "#2563eb",
                "Poco avance, pero lo dictado quedó claro. "
                "El problema es de tiempo, no de método.")
    return ("Crítico", "#ea580c",
            "Poco avance y notas bajas. Requiere intervención directa.")


def tabla_dictado_vs_aprendido(avance, anio, ciclo, grupo):
    filas = []
    for curso in cursos_de_grupo(grupo):
        res = resumen_curso(avance, anio, ciclo, grupo, curso)
        nt = notas_del_curso(grupo, curso)
        etiqueta, color, lectura = cuadrante(res["pct"], nt["promedio"])
        filas.append({
            "curso": curso,
            "peso": res["peso"],
            "avance": res["pct"],
            "promedio": nt["promedio"],
            "alumnos": nt["alumnos"],
            "pct_aprob": nt["pct_aprob"],
            "estado": etiqueta,
            "color": color,
            "lectura": lectura,
        })
    return filas


# ================================================================
# 10. VINCULAR TEMAS CON EVALUACIONES (para análisis por tema)
# ================================================================

def seccion_vincular_evaluaciones(avance, anio, ciclo, grupo, curso, docente):
    """Permite decir qué temas cubrió cada examen ya aplicado."""
    st.markdown("#### 🎯 ¿Qué temas evaluó cada examen?")
    st.caption("Al vincularlos, el sistema puede decirte si un tema se dictó "
               "pero no se entendió, en vez de solo si se dictó.")

    evals = evaluaciones_disponibles(grupo, curso)
    if not evals:
        st.info("Todavía no hay exámenes registrados para este curso y grupo. "
                "Aparecerán aquí en cuanto apliques uno desde Exámenes "
                "Semanales o YACHAY QAWAY.")
        return

    etiquetas = {f"{e['fecha']} — {e['titulo']}": e["eval_id"] for e in evals}
    sel = st.selectbox("Examen aplicado", list(etiquetas.keys()),
                       key=f"av_ev_sel_{grupo}_{curso}")
    eid = etiquetas[sel]

    temas = TEMARIO.get(curso, [])
    ya = []
    for i, tema in enumerate(temas, start=1):
        r = avance.get(_clave(anio, ciclo, grupo, curso, i), {})
        if eid in str(r.get("evals", "")).split(","):
            ya.append(f"{i}. {tema}")

    elegidos = st.multiselect(
        "Temas que entraron en este examen",
        [f"{i}. {t}" for i, t in enumerate(temas, start=1)],
        default=ya, key=f"av_ev_temas_{grupo}_{curso}_{eid}")

    if st.button("🔗 Vincular examen con estos temas",
                 key=f"av_ev_btn_{grupo}_{curso}_{eid}",
                 use_container_width=True):
        cambios = []
        indices = {int(x.split(".")[0]) for x in elegidos}
        for i, tema in enumerate(temas, start=1):
            clave = _clave(anio, ciclo, grupo, curso, i)
            r = dict(avance.get(clave, {}))
            actuales = [x for x in str(r.get("evals", "")).split(",") if x]
            nuevo = list(actuales)
            if i in indices and eid not in nuevo:
                nuevo.append(eid)
            elif i not in indices and eid in nuevo:
                nuevo.remove(eid)
            if nuevo != actuales:
                r.update({
                    "clave": clave, "anio": anio, "ciclo": ciclo,
                    "grupo": grupo, "curso": curso, "tema_num": i,
                    "tema": tema,
                    "estado": r.get("estado", "Pendiente"),
                    "fecha": r.get("fecha", ""),
                    "sesion": r.get("sesion", ""),
                    "docente": r.get("docente", docente),
                    "observacion": r.get("observacion", ""),
                    "evals": ",".join(nuevo),
                })
                cambios.append(r)
        if cambios:
            ok, msg = guardar_avance(cambios)
            (st.success if ok else st.warning)(msg)
            st.rerun()
        else:
            st.info("No hubo cambios que guardar.")

    # --- Resultado por tema vinculado ---
    st.markdown("##### Cómo les fue en los temas ya evaluados")
    hubo = False
    for i, tema in enumerate(temas, start=1):
        r = avance.get(_clave(anio, ciclo, grupo, curso, i), {})
        ids = [x for x in str(r.get("evals", "")).split(",") if x]
        if not ids:
            continue
        hubo = True
        nt = notas_del_curso(grupo, curso, eval_ids=set(ids))
        prom = nt["promedio"]
        if prom is None:
            continue
        color = "#16a34a" if prom >= NOTA_UMBRAL else "#dc2626"
        aviso = "" if prom >= NOTA_UMBRAL else " · conviene reforzar"
        st.markdown(
            f"<div style='padding:6px 10px;margin-bottom:4px;border-radius:6px;"
            f"background:#f8fafc;border-left:5px solid {color};font-size:.9rem;'>"
            f"<b>{i}. {tema}</b> — promedio "
            f"<b style='color:{color};'>{prom}</b> "
            f"({nt['alumnos']} notas, {nt['pct_aprob']}% sobre {NOTA_UMBRAL})"
            f"<span style='color:{color};'>{aviso}</span></div>",
            unsafe_allow_html=True)
    if not hubo:
        st.caption("Vincula al menos un examen arriba para ver esta sección.")


# ================================================================
# 11. PLANILLA IMPRESA PARA MARCAR A MANO
# ================================================================

def generar_pdf_planilla(grupo, ciclo, anio, institucion="ACADEMIA YACHAY"):
    """Hoja con todos los cursos y sus temas, con casilleros vacíos.

    Sirve para que dirección o el propio docente marque con aspa sobre
    papel durante la clase y luego lo pase al sistema, o para archivar
    la evidencia firmada.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, KeepTogether)
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    est = _estilos_pdf()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=1.3 * cm, rightMargin=1.3 * cm,
                            topMargin=1.2 * cm, bottomMargin=1.2 * cm)
    story = []

    _encabezado(story, f"{institucion}<br/>PLANILLA DE CONTROL DEL TEMARIO",
                f"{grupo} &nbsp;·&nbsp; {ciclo} {anio} &nbsp;·&nbsp; "
                f"Temario UNSAAC (Res. CU-575-2024)", est)
    story.append(Paragraph(
        "Marque con una <b>X</b> el estado de cada tema. "
        "<b>P</b> = pendiente &nbsp; <b>A</b> = en avance &nbsp; "
        "<b>C</b> = concluido &nbsp; <b>R</b> = reforzado.", est["n"]))
    story.append(Spacer(1, 8))

    for curso in cursos_de_grupo(grupo):
        temas = TEMARIO.get(curso, [])
        bloque = [Paragraph(
            f"{curso} &nbsp;<font size=8 color='#64748b'>"
            f"({int(peso_curso(grupo, curso))} preguntas en el examen · "
            f"{len(temas)} temas)</font>", est["h2"])]

        data = [["N°", "Tema", "P", "A", "C", "R", "Fecha", "Observación"]]
        for i, tema in enumerate(temas, start=1):
            data.append([str(i), Paragraph(tema, est["n"]),
                         "", "", "", "", "", ""])

        t = Table(data, colWidths=[0.9 * cm, 7.2 * cm, 0.75 * cm, 0.75 * cm,
                                   0.75 * cm, 0.75 * cm, 2.0 * cm, 5.0 * cm],
                  repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#001e7c")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("ALIGN", (2, 0), (6, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#94a3b8")),
            # Casilleros de marcado resaltados
            ("BACKGROUND", (2, 1), (5, -1), colors.HexColor("#f1f5f9")),
            ("ROWBACKGROUNDS", (0, 1), (1, -1),
             [colors.white, colors.HexColor("#fafafa")]),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        bloque.append(t)
        bloque.append(Spacer(1, 4))
        bloque.append(Paragraph(
            "Docente: _______________________________ &nbsp;&nbsp; "
            "Firma: _______________________ &nbsp;&nbsp; "
            "V°B° Dirección: _______________________", est["n"]))
        bloque.append(Spacer(1, 12))
        story.append(KeepTogether(bloque) if len(temas) <= 18
                     else bloque[0])
        if len(temas) > 18:
            for x in bloque[1:]:
                story.append(x)

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()


# ================================================================
# 12. TEMARIO COMPLETO POR ÁREA (A, B, C, D)
# ================================================================

def generar_pdf_area(area, ciclo, anio, institucion="ACADEMIA YACHAY"):
    """Temario completo de un área de postulación, curso por curso.

    Sirve para entregar al postulante y al docente: en una sola hoja
    saben exactamente qué cursos les tocan, cuánto pesa cada uno y
    todos los temas que entran en el examen.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle)
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    est = _estilos_pdf()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                            topMargin=1.2 * cm, bottomMargin=1.2 * cm)
    story = []

    pesos = PESOS.get(area, {})
    total_preg = sum(pesos.values())

    _encabezado(story, f"{institucion}<br/>TEMARIO DE ADMISIÓN — ÁREA «{area}»",
                f"{ciclo} {anio} &nbsp;·&nbsp; {total_preg} preguntas &nbsp;·&nbsp; "
                f"Res. CU-575-2024-UNSAAC", est)

    # Resumen de la distribución
    data = [["Curso", "Preguntas", "% del examen", "N° de temas"]]
    for curso, np_ in sorted(pesos.items(), key=lambda x: -x[1]):
        data.append([
            Paragraph(curso, est["n"]), str(np_),
            f"{round(100*np_/total_preg, 1)}%",
            str(len(TEMARIO.get(curso, []))),
        ])
    data.append(["TOTAL", str(total_preg), "100%",
                 str(sum(len(TEMARIO.get(c, [])) for c in pesos))])
    t = Table(data, colWidths=[8.5 * cm, 2.6 * cm, 3.0 * cm, 3.0 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#001e7c")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e2e8f0")),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#94a3b8")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2),
         [colors.white, colors.HexColor("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Los cursos con más preguntas son los que más deciden el ingreso. "
        "Prioriza tu estudio en ese orden.", est["n"]))
    story.append(Spacer(1, 10))

    # Temario curso por curso
    for curso, np_ in sorted(pesos.items(), key=lambda x: -x[1]):
        temas = TEMARIO.get(curso, [])
        story.append(Paragraph(
            f"{curso} &nbsp;<font size=8 color='#64748b'>"
            f"({np_} preguntas · {len(temas)} temas)</font>", est["h2"]))
        filas, mitad = [], -(-len(temas) // 2)
        for i in range(mitad):
            izq = f"{i+1}. {temas[i]}"
            j = i + mitad
            der = f"{j+1}. {temas[j]}" if j < len(temas) else ""
            filas.append([Paragraph(izq, est["n"]), Paragraph(der, est["n"])])
        t = Table(filas, colWidths=[8.85 * cm, 8.85 * cm])
        t.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 1.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
            ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#e2e8f0")),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()
