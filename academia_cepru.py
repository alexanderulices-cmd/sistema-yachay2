# ================================================================
# ACADEMIA CEPRU — CARPETA ÚNICA CON SELECTOR DE ÁREA
# ================================================================
"""Punto de entrada único para todas las fichas y bancos de preguntas
de la academia preuniversitaria. En vez de un botón por curso en el
menú (Historia CEPRU, Filosofía CEPRU, ...), hay un solo botón
«Academia CEPRU» y aquí dentro se elige el área.

Añadir un curso nuevo es agregar una línea a AREAS_CEPRU: no hace
falta tocar el menú de sistema_web.py otra vez.

Integración en sistema_web.py:
    from academia_cepru import tab_academia_cepru
"""

import streamlit as st

from fichas_historia import (generar_ficha_texto, generar_banco_preguntas,
                             balancear, contar_espacios, LETRAS, _PATRON)

# ---------------------------------------------------------------
# Registro de áreas disponibles. Cada entrada: (nombre para mostrar,
# lista de balotas, nombre de área para el pie de página, prefijo de
# claves de sesión —debe ser único por curso—, estado).
# ---------------------------------------------------------------
AREAS_CEPRU = []

try:
    from fichas_historia import BALOTAS as _BAL_HISTORIA
    AREAS_CEPRU.append({
        "nombre": "📜 Historia", "balotas": _BAL_HISTORIA,
        "area_pie": "Historia", "prefijo": "ceh", "completo": True,
        "total_oficial": 19,
    })
except ImportError:
    pass

try:
    from fichas_filosofia import BALOTAS_FILO as _BAL_FILOSOFIA
    AREAS_CEPRU.append({
        "nombre": "🧠 Filosofía y Lógica", "balotas": _BAL_FILOSOFIA,
        "area_pie": "Filosofía y Lógica", "prefijo": "cef", "completo": True,
        "total_oficial": 17,
    })
except ImportError:
    pass

try:
    from fichas_geografia import GEOGRAFIA_TEMAS as _BAL_GEOGRAFIA
    AREAS_CEPRU.append({
        "nombre": "🌎 Geografía", "balotas": _BAL_GEOGRAFIA,
        "area_pie": "Geografía", "prefijo": "ceg",
        # El temario oficial tiene 20 temas; el material fuente
        # disponible solo cubre 18 (faltan Transporte y Geografía de
        # otros continentes, sin PDF fuente todavía).
        "completo": len(_BAL_GEOGRAFIA) >= 20,
        "total_oficial": 20,
    })
except ImportError:
    pass

try:
    from fichas_civica import BALOTAS_CIVICA as _BAL_CIVICA
    AREAS_CEPRU.append({
        "nombre": "⚖️ Educación Cívica", "balotas": _BAL_CIVICA,
        "area_pie": "Educación Cívica", "prefijo": "cec",
        "completo": len(_BAL_CIVICA) >= 18,
        "total_oficial": 18,
    })
except ImportError:
    pass

try:
    from fichas_comunicativa import COMUNICATIVA_TEMAS as _BAL_COMUNI
    AREAS_CEPRU.append({
        "nombre": "🗣️ Competencia Comunicativa", "balotas": _BAL_COMUNI,
        "area_pie": "Competencia Comunicativa", "prefijo": "cecc",
        "completo": len(_BAL_COMUNI) >= 16, "total_oficial": 16,
    })
except ImportError:
    pass

try:
    from fichas_economia import ECONOMIA_TEMAS as _BAL_ECONOMIA
    AREAS_CEPRU.append({
        "nombre": "💰 Economía", "balotas": _BAL_ECONOMIA,
        "area_pie": "Economía", "prefijo": "cee",
        "completo": len(_BAL_ECONOMIA) >= 18, "total_oficial": 18,
    })
except ImportError:
    pass

# Cursos anunciados pero aún no escritos: aparecen en el selector como
# "próximamente" en vez de desaparecer sin explicación.
PENDIENTES = ["🔢 Aritmética"]


def tab_academia_cepru(config=None):
    st.subheader("🎓 Academia CEPRU — Fichas y bancos de preguntas")
    st.caption("Todas las áreas de la academia preuniversitaria en un "
               "solo lugar. Elige el área y luego la balota o tema.")

    if not AREAS_CEPRU:
        st.error("No se pudo cargar ningún curso. Revisa que los archivos "
                 "fichas_historia.py, fichas_filosofia.py, "
                 "fichas_geografia.py y fichas_civica.py estén en el "
                 "repositorio.")
        return

    nombres = [a["nombre"] for a in AREAS_CEPRU]
    sel_area = st.selectbox("Área:", nombres, key="cepru_area")
    area = next(a for a in AREAS_CEPRU if a["nombre"] == sel_area)

    if not area["completo"]:
        total = area.get("total_oficial", len(area["balotas"]))
        st.warning(
            f"⚠️ {sel_area} está en construcción: por ahora tiene "
            f"{len(area['balotas'])} de {total} temas. Los demás se irán "
            f"agregando — lo que ya está aquí funciona normalmente.")

    if PENDIENTES:
        st.caption("Próximamente en esta misma carpeta: " +
                   " · ".join(PENDIENTES))

    _render_curso(area["balotas"], area["area_pie"], area["prefijo"])


def _render_curso(balotas, area_pie, pfx):
    """Interfaz de un curso: idéntica para todas las áreas, cambiando
    solo la fuente de datos y el prefijo de claves de sesión."""
    _usa_tema = area_pie in ("Geografía", "Competencia Comunicativa", "Economía")
    opciones = {f"{'Tema' if _usa_tema else 'Balota'} "
                f"{t['num']} — {t['titulo']}": t for t in balotas}
    sel = st.selectbox("Balota / Tema:", list(opciones.keys()),
                       key=f"{pfx}_sel")
    tema = opciones[sel]

    c1, c2, c3 = st.columns(3)
    c1.metric("Espacios para completar", contar_espacios(tema))
    c2.metric("Preguntas", len(tema["preguntas"]))
    c3.metric("Cuadros", len(tema.get("cuadros", [])))

    c_g, c_p = st.columns(2)
    with c_g:
        grado_txt = st.text_input("Grupo (se imprime en la ficha):",
                                  placeholder="GRUPO CD", key=f"{pfx}_grado")
    with c_p:
        profesor_txt = st.text_input(
            "Profesor (aparece en el pie y en el QR del examen):",
            value="Prof. Alexander Córdova", key=f"{pfx}_prof")

    st.markdown("##### Descargar")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("**Ficha de texto para completar**")
        try:
            st.download_button(
                "📄 Versión del alumno",
                data=generar_ficha_texto(tema, False, grado_txt,
                                         area=area_pie, profesor=profesor_txt),
                file_name=f"ficha_{pfx}_{tema['num']}_alumno.pdf",
                mime="application/pdf", use_container_width=True,
                type="primary", key=f"{pfx}_fa")
            st.download_button(
                "🔑 Versión del docente (con claves)",
                data=generar_ficha_texto(tema, True, grado_txt,
                                         area=area_pie, profesor=profesor_txt),
                file_name=f"ficha_{pfx}_{tema['num']}_docente.pdf",
                mime="application/pdf", use_container_width=True,
                key=f"{pfx}_fd")
        except Exception as e:
            st.error(f"No se pudo generar la ficha: {e}")
    with d2:
        st.markdown("**Banco de 20 preguntas**")
        try:
            preg = balancear(tema["preguntas"])
            tema_b = {**tema, "preguntas": preg}
            st.download_button(
                "📝 Examen para el alumno",
                data=generar_banco_preguntas(tema_b, False, grado_txt,
                                             area=area_pie, profesor=profesor_txt),
                file_name=f"preguntas_{pfx}_{tema['num']}_alumno.pdf",
                mime="application/pdf", use_container_width=True,
                type="primary", key=f"{pfx}_pa")
            st.download_button(
                "🔑 Con claves para el docente",
                data=generar_banco_preguntas(tema_b, True, grado_txt,
                                             area=area_pie, profesor=profesor_txt),
                file_name=f"preguntas_{pfx}_{tema['num']}_claves.pdf",
                mime="application/pdf", use_container_width=True,
                key=f"{pfx}_pd")
        except Exception as e:
            st.error(f"No se pudo generar el banco: {e}")

    with st.expander("Ver el contenido de esta balota / tema"):
        for sec in tema["secciones"]:
            st.markdown(f"**{sec['titulo']}**")
            for it in sec["items"]:
                st.markdown("- " + _PATRON.sub(r"**\1**", it))
        st.markdown("**Primeras cinco preguntas:**")
        for i, p in enumerate(tema["preguntas"][:5], start=1):
            st.markdown(f"{i}. {p['pregunta']}")
            for k, a in enumerate(p["alternativas"]):
                marca = " ✅" if LETRAS[k] == p["correcta"] else ""
                st.markdown(f"   {LETRAS[k]}) {a}{marca}")
