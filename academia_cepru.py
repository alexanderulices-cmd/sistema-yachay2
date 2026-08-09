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
                             balancear, muestrear, TAMANOS_EXAMEN,
                             contar_espacios, LETRAS, _PATRON)


_NOMBRES_CORTOS_CURSO = {
    "ceh": "Historia", "cef": "Filosofia", "ceg": "Geografia",
    "cec": "Civica", "cecc": "Comunicativa", "cee": "Economia",
    "cebi": "Biologia",
}


def _nombre_archivo(pfx, tema, tipo, version):
    """Arma un nombre de archivo corto y sistematizado para las descargas:
    Yachay_<Curso>_T<N>_<Ficha|Banco>_<A|D>.pdf
    en vez del nombre largo anterior que incluia el titulo completo del
    tema y no se entendia bien en pantallas de celular."""
    curso = _NOMBRES_CORTOS_CURSO.get(pfx, pfx.capitalize())
    tipo_corto = "Ficha" if tipo == "Ficha" else "Banco"
    version_corta = "A" if version == "Alumno" else "D"
    return f"Yachay_{curso}_T{tema['num']}_{tipo_corto}_{version_corta}.pdf"

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

try:
    from fichas_biologia import BIOLOGIA_TEMAS as _BAL_BIOLOGIA
    AREAS_CEPRU.append({
        "nombre": "🧬 Biología", "balotas": _BAL_BIOLOGIA,
        "area_pie": "Biología", "prefijo": "cebi",
        "completo": len(_BAL_BIOLOGIA) >= 16, "total_oficial": 16,
    })
except ImportError:
    pass

# Cursos anunciados pero aún no escritos: aparecen en el selector como
# "próximamente" en vez de desaparecer sin explicación.
PENDIENTES = ["🔢 Aritmética"]


def _generar_zip_curso(balotas, area_pie, pfx, grado_txt, profesor_txt,
                       con_claves):
    """Genera un ZIP en memoria con la ficha y el banco de preguntas de
    TODOS los temas de un curso, listo para subir a una carpeta."""
    import zipfile, io as _io

    buf = _io.BytesIO()
    version = "Docente" if con_claves else "Alumno"
    _, tamano_defecto = list(TAMANOS_EXAMEN.items())[0]  # 20 preguntas

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for tema in balotas:
            try:
                ficha_pdf = generar_ficha_texto(
                    tema, con_claves, grado_txt,
                    area=area_pie, profesor=profesor_txt)
                nombre_ficha = _nombre_archivo(pfx, tema, "Ficha", version)
                zf.writestr(nombre_ficha, ficha_pdf)
            except Exception:
                pass
            try:
                cantidad = min(tamano_defecto, len(tema["preguntas"]))
                muestra = muestrear(tema["preguntas"], cantidad, semilla=0)
                preg = balancear(muestra)
                tema_b = {**tema, "preguntas": preg}
                banco_pdf = generar_banco_preguntas(
                    tema_b, con_claves, grado_txt,
                    area=area_pie, profesor=profesor_txt)
                nombre_banco = _nombre_archivo(pfx, tema, "Banco", version)
                zf.writestr(nombre_banco, banco_pdf)
            except Exception:
                pass

    buf.seek(0)
    return buf.getvalue()


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
    _usa_tema = area_pie in ("Geografía", "Competencia Comunicativa", "Economía", "Biología")
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

    st.markdown("##### Descargar TODO el curso de una vez")
    st.caption(
        "Genera un único archivo ZIP con la ficha y el banco de "
        "preguntas de **todos los temas** de este curso, listo para "
        "subir a una carpeta. Usa un examen de 20 preguntas por tema "
        "para que el ZIP no sea demasiado pesado."
    )
    zc1, zc2 = st.columns(2)
    with zc1:
        if st.button("📦 ZIP completo — Alumnos", key=f"{pfx}_zip_alu",
                     use_container_width=True):
            with st.spinner(f"Generando {len(balotas)} temas × 2 documentos…"):
                zip_bytes = _generar_zip_curso(
                    balotas, area_pie, pfx, grado_txt, profesor_txt,
                    con_claves=False)
            st.session_state[f"{pfx}_zip_alu_bytes"] = zip_bytes
        if st.session_state.get(f"{pfx}_zip_alu_bytes"):
            st.download_button(
                "⬇️ Descargar ZIP — Alumnos",
                data=st.session_state[f"{pfx}_zip_alu_bytes"],
                file_name=f"Yachay_{_NOMBRES_CORTOS_CURSO.get(pfx, pfx)}_TODO_Alumnos.zip",
                mime="application/zip", use_container_width=True,
                type="primary", key=f"{pfx}_zip_alu_dl")
    with zc2:
        if st.button("📦 ZIP completo — Docentes (con claves)",
                     key=f"{pfx}_zip_doc", use_container_width=True):
            with st.spinner(f"Generando {len(balotas)} temas × 2 documentos…"):
                zip_bytes = _generar_zip_curso(
                    balotas, area_pie, pfx, grado_txt, profesor_txt,
                    con_claves=True)
            st.session_state[f"{pfx}_zip_doc_bytes"] = zip_bytes
        if st.session_state.get(f"{pfx}_zip_doc_bytes"):
            st.download_button(
                "⬇️ Descargar ZIP — Docentes",
                data=st.session_state[f"{pfx}_zip_doc_bytes"],
                file_name=f"Yachay_{_NOMBRES_CORTOS_CURSO.get(pfx, pfx)}_TODO_Docentes.zip",
                mime="application/zip", use_container_width=True,
                type="primary", key=f"{pfx}_zip_doc_dl")

    st.markdown("---")
    st.markdown("##### O descarga un tema a la vez")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("**Ficha de texto para completar**")
        try:
            st.download_button(
                "📄 Versión del alumno",
                data=generar_ficha_texto(tema, False, grado_txt,
                                         area=area_pie, profesor=profesor_txt),
                file_name=_nombre_archivo(pfx, tema, "Ficha", "Alumno"),
                mime="application/pdf", use_container_width=True,
                type="primary", key=f"{pfx}_fa")
            st.download_button(
                "🔑 Versión del docente (con claves)",
                data=generar_ficha_texto(tema, True, grado_txt,
                                         area=area_pie, profesor=profesor_txt),
                file_name=_nombre_archivo(pfx, tema, "Ficha", "Docente"),
                mime="application/pdf", use_container_width=True,
                key=f"{pfx}_fd")
        except Exception as e:
            st.error(f"No se pudo generar la ficha: {e}")
    with d2:
        st.markdown("**Banco de preguntas**")
        try:
            total_banco = len(tema["preguntas"])
            tamano_txt = st.radio(
                "Tamaño del examen:", list(TAMANOS_EXAMEN.keys()),
                horizontal=True, key=f"{pfx}_tam")
            cantidad = min(TAMANOS_EXAMEN[tamano_txt], total_banco)

            _clave_semilla = f"{pfx}_semilla_examen"
            if _clave_semilla not in st.session_state:
                st.session_state[_clave_semilla] = 0

            c_info, c_btn = st.columns([3, 1])
            with c_info:
                st.caption(
                    f"Banco con {total_banco} preguntas disponibles · "
                    f"este examen usa {cantidad}."
                    + (" Puedes generar otra combinación distinta cada vez."
                       if total_banco > cantidad else ""))
            with c_btn:
                if total_banco > cantidad:
                    if st.button("🔀 Otra combinación", key=f"{pfx}_mezclar",
                                 use_container_width=True):
                        st.session_state[_clave_semilla] += 1

            _muestra = muestrear(tema["preguntas"], cantidad,
                                 semilla=st.session_state[_clave_semilla])
            preg = balancear(_muestra)
            tema_b = {**tema, "preguntas": preg}
            st.download_button(
                "📝 Examen para el alumno",
                data=generar_banco_preguntas(tema_b, False, grado_txt,
                                             area=area_pie, profesor=profesor_txt),
                file_name=_nombre_archivo(pfx, tema, "Banco", "Alumno"),
                mime="application/pdf", use_container_width=True,
                type="primary", key=f"{pfx}_pa")
            st.download_button(
                "🔑 Con claves para el docente",
                data=generar_banco_preguntas(tema_b, True, grado_txt,
                                             area=area_pie, profesor=profesor_txt),
                file_name=_nombre_archivo(pfx, tema, "Banco", "Docente"),
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
