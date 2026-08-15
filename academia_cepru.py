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

try:
    from fichas_algebra import generar_ficha_algebra
except ImportError:
    generar_ficha_algebra = None


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

try:
    from fichas_algebra import BALOTAS_ALGEBRA as _BAL_ALGEBRA
    AREAS_CEPRU.append({
        "nombre": "📐 Álgebra", "balotas": _BAL_ALGEBRA,
        "area_pie": "Álgebra", "prefijo": "cea",
        "completo": len(_BAL_ALGEBRA) >= 17, "total_oficial": 17,
        # Formato distinto: una sola ficha con teoría + ejercicios,
        # no ficha+banco separados. _render_curso lo detecta con esto.
        "combinado": True,
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


def _generar_paquete_admin(area, tipos, grado_txt, profesor_txt,
                           reportar_progreso=None):
    """Genera un ZIP con TODO lo que el administrador haya marcado para
    un curso: fichas en blanco, fichas completas, examenes de 20/40
    preguntas (alumno y docente), y el banco completo del curso.
    'reportar_progreso' es una funcion opcional callback(fraccion, texto)
    para actualizar una barra de progreso en la interfaz."""
    import zipfile, io as _io

    balotas = area["balotas"]
    pfx = area["prefijo"]
    area_pie = area["area_pie"]
    buf = _io.BytesIO()
    total_pasos = len(balotas) + (1 if tipos.get("banco_completo") else 0)
    paso_actual = 0

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for tema in balotas:
            paso_actual += 1
            if reportar_progreso:
                reportar_progreso(paso_actual / total_pasos,
                                  f"{area_pie} · Tema {tema['num']}")
            if tipos.get("ficha_blanco"):
                try:
                    pdf = generar_ficha_texto(tema, False, grado_txt,
                                              area=area_pie, profesor=profesor_txt)
                    zf.writestr(_nombre_archivo(pfx, tema, "Ficha", "Alumno"), pdf)
                except Exception:
                    pass
            if tipos.get("ficha_completa"):
                try:
                    pdf = generar_ficha_texto(tema, True, grado_txt,
                                              area=area_pie, profesor=profesor_txt)
                    zf.writestr(_nombre_archivo(pfx, tema, "Ficha", "Docente"), pdf)
                except Exception:
                    pass
            for tam, etiqueta in [(20, "Ex20"), (40, "Ex40")]:
                if tipos.get(f"examen{tam}"):
                    try:
                        cantidad = min(tam, len(tema["preguntas"]))
                        muestra = muestrear(tema["preguntas"], cantidad, semilla=tam)
                        preg = balancear(muestra)
                        tema_b = {**tema, "preguntas": preg}
                        curso_corto = _NOMBRES_CORTOS_CURSO.get(pfx, pfx)
                        pdf_a = generar_banco_preguntas(
                            tema_b, False, grado_txt, area=area_pie, profesor=profesor_txt)
                        zf.writestr(
                            f"Yachay_{curso_corto}_T{tema['num']}_{etiqueta}_A.pdf", pdf_a)
                        pdf_d = generar_banco_preguntas(
                            tema_b, True, grado_txt, area=area_pie, profesor=profesor_txt)
                        zf.writestr(
                            f"Yachay_{curso_corto}_T{tema['num']}_{etiqueta}_D.pdf", pdf_d)
                    except Exception:
                        pass

        if tipos.get("banco_completo"):
            paso_actual += 1
            if reportar_progreso:
                reportar_progreso(paso_actual / total_pasos,
                                  f"{area_pie} · Banco completo del curso")
            try:
                todas_preguntas = []
                for t in balotas:
                    todas_preguntas.extend(t["preguntas"])
                todas_balanceadas = balancear(todas_preguntas)
                tema_mega = {"num": "TODOS", "titulo": "Banco Completo del Curso",
                            "preguntas": todas_balanceadas, "secciones": [],
                            "cuadros": []}
                curso_corto = _NOMBRES_CORTOS_CURSO.get(pfx, pfx)
                pdf_a = generar_banco_preguntas(tema_mega, False, grado_txt,
                                                area=area_pie, profesor=profesor_txt)
                zf.writestr(f"Yachay_{curso_corto}_BANCO_COMPLETO_A.pdf", pdf_a)
                pdf_d = generar_banco_preguntas(tema_mega, True, grado_txt,
                                                area=area_pie, profesor=profesor_txt)
                zf.writestr(f"Yachay_{curso_corto}_BANCO_COMPLETO_D.pdf", pdf_d)
            except Exception:
                pass

    buf.seek(0)
    return buf.getvalue()


def _seccion_descarga_masiva_admin():
    """Panel para que el administrador descargue en un solo lote todo
    el material de uno o varios cursos: fichas, exámenes y bancos
    completos, alumno y docente."""
    st.markdown("### 🗂️ Descarga Masiva — Administrador")
    st.caption("Genera un solo ZIP con todo el material que marques, "
              "de uno o de todos los cursos a la vez.")

    with st.expander("📦 Abrir panel de descarga masiva", expanded=False):
        nombres_todos = [a["nombre"] for a in AREAS_CEPRU]
        alcance = st.radio("¿Qué cursos incluir?",
                           ["Un solo curso", "Todos los cursos (más lento)"],
                           key="admin_dm_alcance", horizontal=True)

        if alcance == "Un solo curso":
            sel_curso_dm = st.selectbox("Curso:", nombres_todos, key="admin_dm_curso")
            cursos_incluir = [a for a in AREAS_CEPRU if a["nombre"] == sel_curso_dm]
        else:
            cursos_incluir = AREAS_CEPRU
            st.warning("⏱️ Con los 7 cursos, esto puede tardar varios minutos "
                      "según cuánto marques abajo. No cierres la página "
                      "mientras genera.")

        st.markdown("**¿Qué incluir por cada tema?**")
        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            inc_ficha_blanco = st.checkbox("Ficha para llenar", value=True,
                                           key="admin_dm_fb")
            inc_ficha_completa = st.checkbox("Ficha ya llenada (con respuestas)",
                                             value=True, key="admin_dm_fc")
        with cc2:
            inc_ex20 = st.checkbox("Examen de 20 preguntas (alumno + docente)",
                                   value=True, key="admin_dm_e20")
            inc_ex40 = st.checkbox("Examen de 40 preguntas (alumno + docente)",
                                   value=False, key="admin_dm_e40")
        with cc3:
            inc_banco = st.checkbox("Banco COMPLETO del curso (todas las "
                                    "preguntas en un PDF)", value=True,
                                    key="admin_dm_banco")

        tipos_sel = {
            "ficha_blanco": inc_ficha_blanco, "ficha_completa": inc_ficha_completa,
            "examen20": inc_ex20, "examen40": inc_ex40,
            "banco_completo": inc_banco,
        }

        c_gr, c_pr = st.columns(2)
        with c_gr:
            grado_dm = st.text_input("Grupo (se imprime en las fichas):",
                                     value="GRUPO CD", key="admin_dm_grado")
        with c_pr:
            profesor_dm = st.text_input("Profesor:",
                                        value="Prof. Alexander Córdova",
                                        key="admin_dm_profesor")

        if not any(tipos_sel.values()):
            st.info("Marca al menos una opción arriba para generar el paquete.")
        elif st.button("🚀 GENERAR PAQUETE MASIVO", type="primary",
                       use_container_width=True, key="admin_dm_generar"):
            import zipfile, io as _io_mega

            barra = st.progress(0.0, text="Iniciando…")
            buf_mega = _io_mega.BytesIO()
            with zipfile.ZipFile(buf_mega, "w", zipfile.ZIP_DEFLATED) as zf_mega:
                for idx_curso, area_dm in enumerate(cursos_incluir):
                    def _callback(frac, texto, idx=idx_curso, n=len(cursos_incluir)):
                        frac_global = (idx + frac) / n
                        barra.progress(min(frac_global, 1.0), text=texto)

                    zip_curso_bytes = _generar_paquete_admin(
                        area_dm, tipos_sel, grado_dm, profesor_dm,
                        reportar_progreso=_callback)
                    zf_mega.writestr(
                        f"{area_dm['prefijo']}_{area_dm['area_pie'].strip()}.zip",
                        zip_curso_bytes)
            barra.progress(1.0, text="¡Listo!")
            buf_mega.seek(0)

            nombre_zip = ("Yachay_TODO_PREU.zip" if alcance != "Un solo curso"
                         else f"Yachay_{cursos_incluir[0]['prefijo']}_PAQUETE.zip")
            st.success("✅ Paquete generado. Descárgalo abajo antes de salir "
                      "de esta página.")
            st.download_button("⬇️ Descargar paquete completo",
                              data=buf_mega.getvalue(), file_name=nombre_zip,
                              mime="application/zip", use_container_width=True,
                              type="primary", key="admin_dm_descargar")


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

    _seccion_descarga_masiva_admin()
    st.markdown("---")

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

    _render_curso(area["balotas"], area["area_pie"], area["prefijo"],
                  combinado=area.get("combinado", False))


def _render_curso(balotas, area_pie, pfx, combinado=False):
    """Interfaz de un curso: idéntica para todas las áreas, cambiando
    solo la fuente de datos y el prefijo de claves de sesión.
    Los cursos 'combinados' (Álgebra, Aritmética: una sola ficha con
    teoría + ejercicios, no ficha+banco separados) usan su propia
    interfaz más simple, _render_curso_combinado."""
    if combinado:
        _render_curso_combinado(balotas, area_pie, pfx)
        return

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


def _render_curso_combinado(balotas, area_pie, pfx):
    """Interfaz simplificada para cursos de formato 'combinado' (una
    sola ficha con teoría + ejercicios, como Álgebra y, más adelante,
    Aritmética). No hay ficha+banco separados ni ZIP masivo todavía
    (se agrega cuando haya más temas escritos)."""
    if generar_ficha_algebra is None:
        st.error("No se pudo cargar el generador de fichas de Álgebra "
                 "(fichas_algebra.py). Revisa que el archivo esté en "
                 "el repositorio.")
        return

    opciones = {f"Tema {t['num']} — {t['titulo']}": t for t in balotas}
    sel = st.selectbox("Tema:", list(opciones.keys()), key=f"{pfx}_sel")
    tema = opciones[sel]

    c1, c2 = st.columns(2)
    c1.metric("Secciones de teoría", len(tema.get("secciones", [])))
    c2.metric("Ejercicios propuestos", len(tema.get("ejercicios", [])))

    c_g, c_p = st.columns(2)
    with c_g:
        grado_txt = st.text_input("Grupo (se imprime en la ficha):",
                                  placeholder="GRUPO CD", key=f"{pfx}_grado")
    with c_p:
        profesor_txt = st.text_input(
            "Profesor (aparece en el pie de página):",
            value="Prof. Alexander Córdova", key=f"{pfx}_prof")

    st.markdown("---")
    st.caption("Esta ficha combina teoría (para completar) y ejercicios "
              "propuestos en un solo documento de máximo 2 hojas — no "
              "hay banco de preguntas separado en este curso.")

    d1, d2 = st.columns(2)
    with d1:
        try:
            st.download_button(
                "📄 Versión del alumno (para completar)",
                data=generar_ficha_algebra(tema, False, grado_txt,
                                           area=area_pie, profesor=profesor_txt),
                file_name=_nombre_archivo(pfx, tema, "Ficha", "Alumno"),
                mime="application/pdf", use_container_width=True,
                type="primary", key=f"{pfx}_fa")
        except Exception as e:
            st.error(f"No se pudo generar la ficha del alumno: {e}")
    with d2:
        try:
            st.download_button(
                "🔑 Versión del docente (con respuestas)",
                data=generar_ficha_algebra(tema, True, grado_txt,
                                           area=area_pie, profesor=profesor_txt),
                file_name=_nombre_archivo(pfx, tema, "Ficha", "Docente"),
                mime="application/pdf", use_container_width=True,
                key=f"{pfx}_fd")
        except Exception as e:
            st.error(f"No se pudo generar la ficha del docente: {e}")

    with st.expander("Ver el contenido de este tema"):
        for sec in tema.get("secciones", []):
            st.markdown(f"**{sec['titulo']}**")
            for it in sec.get("items", []):
                st.markdown(f"- {it}")
        if tema.get("ejercicios"):
            st.markdown("**Ejercicios propuestos:**")
            for i, ej in enumerate(tema["ejercicios"], start=1):
                st.markdown(f"{i}. {ej['enunciado']}")
