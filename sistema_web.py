import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
import qrcode
import io
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sistema YACHAY - Dirección", page_icon="🎓", layout="wide")

# ==========================================
# 🔐 1. SISTEMA DE SEGURIDAD (LOGIN)
# ==========================================
if 'usuario_valido' not in st.session_state:
    st.session_state['usuario_valido'] = False

def login():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>🔒 ACCESO DIRECCIÓN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Sistema de Gestión Documental YACHAY</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Contraseña de Director:", type="password")
        if st.button("INGRESAR AL SISTEMA", use_container_width=True):
            if password == "456789":
                st.session_state['usuario_valido'] = True
                st.rerun()
            else:
                st.error("🚫 CONTRASEÑA INCORRECTA")

if not st.session_state['usuario_valido']:
    login()
    st.stop()

# ==========================================
# 🤖 2. CONEXIÓN A GOOGLE SHEETS
# ==========================================
@st.cache_resource
def conectar_google():
    try:
        gc = gspread.service_account(filename='credenciales.json')
        sh = gc.open("Sistema de Asistencia")
        return sh
    except Exception as e:
        return None # Si falla, permitiremos ingreso manual

def buscar_alumno(dni):
    sh = conectar_google()
    if sh:
        try:
            hoja = sh.worksheet("Alumnos")
            df = pd.DataFrame(hoja.get_all_records())
            df['DNI'] = df['DNI'].astype(str)
            res = df[df['DNI'] == str(dni)]
            if not res.empty:
                return res.iloc[0]
        except:
            pass
    return None

# ==========================================
# 🛡️ 3. GENERADOR DE CÓDIGO QR
# ==========================================
def generar_qr_html(texto_data):
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(texto_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<img src="data:image/png;base64,{img_str}" style="width: 100px; height: 100px; border: 1px solid #ccc;">'

# ==========================================
# 🖥️ 4. INTERFAZ PRINCIPAL
# ==========================================
st.sidebar.title("🏫 Panel Director")
st.sidebar.success("✅ Conectado como Director")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state['usuario_valido'] = False
    st.rerun()

st.title("📄 Emisión de Documentos Oficiales")
st.markdown("---")

col_datos, col_vista = st.columns([1, 2])

with col_datos:
    st.subheader("1. Buscar Estudiante")
    dni_input = st.text_input("Ingrese DNI:", max_chars=8)
    
    # Variables iniciales vacías
    nombre = ""
    grado = ""
    apoderado = ""
    dni_apo = ""

    # Intentar buscar automático
    if dni_input:
        alumno = buscar_alumno(dni_input)
        if alumno is not None:
            st.success("✅ Alumno Encontrado en Base de Datos")
            nombre = alumno['NOMBRE']
            grado = alumno['GRADO']
            apoderado = alumno.get('APODERADO', '') # .get por si la columna no existe
            dni_apo = str(alumno.get('DNI_APO', ''))
        else:
            st.warning("⚠️ No encontrado en Excel. Ingrese manual:")
    
    # Campos editables (se llenan solos si encuentra, o manual si no)
    nombre = st.text_input("Nombre Completo:", value=nombre)
    grado = st.text_input("Grado / Año:", value=grado)
    apoderado = st.text_input("Nombre Apoderado:", value=apoderado)
    dni_apo = st.text_input("DNI Apoderado:", value=dni_apo)

    st.markdown("---")
    st.subheader("2. Tipo de Documento")
    tipo_doc = st.radio("Seleccione el documento a generar:", 
        ["Constancia de Vacante", 
         "Constancia de No Deudor", 
         "Constancia de Estudios", 
         "Constancia de Dirimencia",
         "Compromiso Padre de Familia"])
    
    # CAMPOS EXTRA SEGÚN EL DOCUMENTO
    promedio = ""
    puesto = ""
    anios_text = ""
    
    if tipo_doc == "Constancia de Dirimencia":
        st.info("🔸 Datos Académicos:")
        promedio = st.text_input("Promedio General:", "18.5")
        puesto = st.text_input("Puesto Ocupado:", "PRIMER LUGAR")
        anios_text = st.text_input("Años Cursados:", "2021 al 2025")

with col_vista:
    st.subheader("3. Documento Oficial")
    
    if st.button("🖨️ GENERAR DOCUMENTO ORIGINAL"):
        if not nombre:
            st.error("Por favor ingresa el nombre del alumno.")
        else:
            fecha_hoy = datetime.now().strftime("%d de %B del %Y")
            anio_actual = datetime.now().year
            hora_emision = datetime.now().strftime("%H:%M:%S")

            # --- GENERAR QR ÚNICO ---
            texto_seguridad = f"""
            I.E. ALTERNATIVO YACHAY - ORIGINAL
            Alumno: {nombre}
            DNI: {dni_input}
            Documento: {tipo_doc}
            Emisión: {fecha_hoy} {hora_emision}
            Firma: VALIDADA
            """
            qr_html = generar_qr_html(texto_seguridad)

            # --- CABECERA COMÚN ---
            encabezado = f"""
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid black; padding-bottom: 15px; margin-bottom: 20px;">
                <div style="width: 75%;">
                    <p style="font-size: 14px; font-weight: bold; margin: 0;">“AÑO DE LA RECUPERACIÓN Y CONSOLIDACIÓN DE LA ECONOMÍA PERUANA”</p>
                    <p style="font-size: 18px; font-weight: bold; margin: 5px 0;">INSTITUCIÓN EDUCATIVA "YACHAY"</p>
                </div>
                <div style="text-align: center;">
                    {qr_html}
                    <p style="font-size: 8px; margin: 0;">ESCANEAR PARA VALIDAR</p>
                </div>
            </div>
            """

            cuerpo = ""

            # --- 1. CONSTANCIA DE VACANTE ---
            if tipo_doc == "Constancia de Vacante":
                cuerpo = f"""
                <h2 style="text-align: center; text-decoration: underline;">CONSTANCIA DE VACANTE</h2>
                <br>
                <p style="text-align: justify;">LA DIRECCIÓN DE LA INSTITUCIÓN EDUCATIVA PARTICULAR ALTERNATIVO <b>YACHAY</b> DE CHINCHERO, SUSCRIBE LA PRESENTE CONSTANCIA:</p>
                <p><b>HACE CONSTAR:</b></p>
                <p style="text-align: justify;">Que, existe vacante disponible en el <b>{grado.upper()}</b> para el/la alumno(a):</p>
                <h2 style="text-align: center;">{nombre.upper()}</h2>
                <p style="text-align: justify;">Identificado con DNI <b>{dni_input}</b>. Para el año escolar <b>{anio_actual}</b>.</p>
                <p>Por lo que se debe consignar los siguientes documentos:</p>
                <ul>
                    <li>Certificado de Estudios original.</li>
                    <li>Resolución de traslado.</li>
                    <li>Ficha única de matrícula de SIAGIE.</li>
                    <li>DNI (FOTOCOPIAS) del alumno y de los padres.</li>
                    <li>Constancia de no Deudor.</li>
                </ul>
                <p>Se le expide el presente documento a solicitud del interesado.</p>
                """

            # --- 2. CONSTANCIA DE NO DEUDOR ---
            elif tipo_doc == "Constancia de No Deudor":
                cuerpo = f"""
                <h2 style="text-align: center; text-decoration: underline;">CONSTANCIA DE NO DEUDOR</h2>
                <br>
                <p>LA DIRECTORA DE LA INSTITUCIÓN EDUCATIVA ALTERNATIVO YACHAY DE CHINCHERO.</p>
                <p><b>HACE CONSTAR:</b></p>
                <p style="text-align: justify;">Que el (la) estudiante: <b>{nombre.upper()}</b> con DNI <b>{dni_input}</b>.</p>
                <p style="text-align: justify; font-size: 18px;"><b>NO PRESENTA DEUDA PENDIENTE</b></p>
                <p style="text-align: justify;">Ni por matrícula ni por mensualidades a lo largo de sus estudios en nuestra Institución.</p>
                <p style="text-align: justify;">Se expide la presente constancia a petición escrita del apoderado para los fines que viera por conveniente.</p>
                """

            # --- 3. CONSTANCIA DE ESTUDIOS ---
            elif tipo_doc == "Constancia de Estudios":
                cuerpo = f"""
                <h2 style="text-align: center; text-decoration: underline;">CONSTANCIA DE ESTUDIOS</h2>
                <br>
                <p>LA DIRECCIÓN DE LA INSTITUCIÓN EDUCATIVA PARTICULAR ALTERNATIVO YACHAY DE CHINCHERO.</p>
                <p><b>HACE CONSTAR:</b></p>
                <p style="text-align: justify;">PRIMERO: El estudiante <b>{nombre.upper()}</b> ha culminado satisfactoriamente el año escolar anterior en el nivel <b>{grado.upper()}</b> de esta institución.</p>
                <p style="text-align: justify;">El mencionado estudiante ha observado buena conducta y puntualidad durante su permanencia en la institución.</p>
                <p style="text-align: justify;">Se expide para los trámites correspondientes.</p>
                """

            # --- 4. CONSTANCIA DE DIRIMENCIA ---
            elif tipo_doc == "Constancia de Dirimencia":
                cuerpo = f"""
                <h2 style="text-align: center; text-decoration: underline;">CONSTANCIA DE DIRIMENCIA</h2>
                <br>
                <p>LA DIRECTORA DE LA INSTITUCIÓN EDUCATIVA ALTERNATIVO YACHAY DE CHINCHERO.</p>
                <p><b>HACE CONSTAR:</b></p>
                <p style="text-align: justify;">Que el alumno(a): <b>{nombre.upper()}</b> identificado con DNI N° <b>{dni_input}</b>.</p>
                <p style="text-align: justify;">Ha concluido satisfactoriamente la Educación Básica Regular durante los años <b>{anios_text}</b> respectivamente, ocupando el:</p>
                <h2 style="text-align: center;">{puesto.upper()}</h2>
                <p style="text-align: center; font-size: 18px;">Con un promedio general ponderado de: <b>{promedio}</b></p>
                <br>
                <p style="text-align: justify;">Se expide la presente constancia a petición escrita del interesado para que sea reconocida como tal y participar en el proceso de examen de DIRIMENCIA UNSAAC {anio_actual}.</p>
                """

            # --- 5. COMPROMISO PADRES ---
            elif tipo_doc == "Compromiso Padre de Familia":
                cuerpo = f"""
                <h3 style="text-align: center; text-decoration: underline;">CARTA COMPROMISO DEL PADRE DE FAMILIA</h3>
                <br>
                <p style="text-align: justify;">Por medio del presente Yo, <b>{apoderado.upper()}</b> identificado con DNI N° <b>{dni_apo}</b>, padre o madre de familia de mi menor hijo(a): <b>{nombre.upper()}</b>.</p>
                <p style="text-align: justify;">Consciente de las normas del Colegio YACHAY, me comprometo a respetar y cumplir las siguientes disposiciones:</p>
                <ul style="text-align: justify;">
                    <li>Cuidaré que mi hijo(a) asista al colegio con puntualidad.</li>
                    <li>Cuidaré que cumpla diariamente con sus tareas escolares.</li>
                    <li>Enviaré a mi hijo(a) bien aseado y con el uniforme correcto.</li>
                    <li>Asumiré los costos de cualquier desperfecto que mi hijo ocasione.</li>
                    <li>Asistiré obligatoriamente a las reuniones convocadas.</li>
                    <li>Cumpliré puntualmente con el pago de las pensiones de enseñanza.</li>
                </ul>
                <p style="text-align: justify;">Firmo la presente en señal de conformidad.</p>
                """

            # --- ENSAMBLAJE FINAL HTML ---
            html_final = f"""
            <div style="font-family: 'Times New Roman', Times, serif; padding: 50px; background: white; color: black; border: 1px solid #ddd; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                {encabezado}
                <div style="line-height: 1.6; font-size: 16px;">
                    {cuerpo}
                </div>
                <br><br><br>
                <p style="text-align: right;">Chinchero, {fecha_hoy}</p>
                <br><br><br><br>
                <div style="display: flex; justify-content: space-around;">
                    <div style="text-align: center;">
                        ____________________________________<br>
                        <b>DIRECCIÓN YACHAY</b>
                    </div>
                    {f'<div style="text-align: center;">____________________________________<br><b>{apoderado.upper()}</b><br>DNI: {dni_apo}</div>' if tipo_doc == "Compromiso Padre de Familia" else ""}
                </div>
            </div>
            """

            st.markdown(html_final, unsafe_allow_html=True)
            st.success("✅ Documento Generado Exitosamente")