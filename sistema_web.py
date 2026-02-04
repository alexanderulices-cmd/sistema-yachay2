import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.lib import colors
import qrcode
import os
from datetime import datetime
import io
# Importación segura del generador de barras
try:
    from barcode import Code128
    from barcode.writer import ImageWriter
except ImportError:
    st.error("Error: Falta instalar python-barcode. Revisa requirements.txt")

# --- 1. CONFIGURACIÓN E INICIO ---
st.set_page_config(page_title="YACHAY DIGITAL PRO", page_icon="🎓", layout="wide")

# --- 2. LÓGICA DE VALIDACIÓN QR (MODO PÚBLICO) ---
query_params = st.query_params
if "validar" in query_params:
    dni_val = query_params["validar"]
    st.markdown("""
        <style>
        .stApp {background-color: #e8f5e9;}
        .valid-box {
            border: 2px solid #2e7d32;
            padding: 20px;
            border-radius: 10px;
            background-color: white;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if os.path.exists("fondo.png"):
            st.image("fondo.png", use_container_width=True)
        st.markdown('<div class="valid-box">', unsafe_allow_html=True)
        st.title("✅ DOCUMENTO VÁLIDO")
        st.success(f"El documento asociado al DNI {dni_val} ha sido emitido por la I.E. YACHAY.")
        st.write(f"Fecha de consulta: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        st.caption("Institución Educativa Oficial - Chinchero")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 3. GESTIÓN DE ESTADO Y BASE DE DATOS ---
def cargar_bd():
    try:
        if os.path.exists("base_datos.xlsx"):
            # IMPORTANTE: Especificamos engine='openpyxl' para evitar fallos en Linux
            return pd.read_excel("base_datos.xlsx", dtype=str, engine='openpyxl')
        return None
    except Exception as e:
        st.error(f"Error leyendo Base de Datos: {e}")
        return None

def buscar_alumno(dni_busqueda):
    df = cargar_bd()
    if df is not None:
        # Limpiamos espacios en blanco por si acaso
        dni_busqueda = dni_busqueda.strip()
        resultado = df[df['DNI'].astype(str).str.strip() == dni_busqueda]
        if not resultado.empty:
            return resultado.iloc[0]
    return None

def limpiar_datos():
    keys = ['alumno', 'dni', 'grado', 'apoderado', 'dni_apo']
    for k in keys: st.session_state[k] = ""
    for i in range(1, 6):
        if f"cond_anio_{i}" in st.session_state: st.session_state[f"cond_anio_{i}"] = ""
        if f"cond_nota_{i}" in st.session_state: st.session_state[f"cond_nota_{i}"] = ""

# --- 4. LOGIN ---
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔐 Acceso Administrativo")
        password = st.text_input("Contraseña:", type="password")
        if st.button("Ingresar"):
            if password == "yachay2026":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Acceso Denegado")
    st.stop()

# --- 5. FUNCIONES GENERADORAS ---
def obtener_fecha_espanol(anio_doc):
    meses = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
    hoy = datetime.now()
    return f"Chinchero, {hoy.day} de {meses[hoy.month]} del {anio_doc}"

def poner_fondo(c, width, height):
    if os.path.exists("fondo.png"):
        try: c.drawImage("fondo.png", 0, 0, width=width, height=height)
        except: pass

def escribir_parrafo(c, texto, x, y, ancho_max, fuente, tamano, interlineado=14):
    lines = simpleSplit(texto, fuente, tamano, ancho_max)
    for line in lines:
        c.setFont(fuente, tamano)
        c.drawString(x, y, line)
        y -= interlineado
    return y

# --- GENERADOR PDF DOCUMENTOS ---
def generar_pdf_doc(tipo_doc, datos, config):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    frase_anio, anio_doc = config['frase'], config['anio']
    poner_fondo(c, width, height)
    
    if tipo_doc != "CARTA COMPROMISO PADRE DE FAMILIA":
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(width/2, config['y_frase'], f'"{frase_anio}"')

    c.setFont("Helvetica", 11)
    c.drawRightString(width - 60, config['y_frase'] - 20, obtener_fecha_espanol(anio_doc))

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, config['y_titulo'], tipo_doc)
    c.line(100, config['y_titulo']-3, width-100, config['y_titulo']-3) 

    y = config['y_titulo'] - 45
    margen_x = 60
    ancho_texto = width - 120

    if tipo_doc == "CONSTANCIA DE VACANTE":
        y = escribir_parrafo(c, "LA DIRECCIÓN DE LA INSTITUCIÓN EDUCATIVA PARTICULAR ALTERNATIVO YACHAY DE CHINCHERO, SUSCRIBE LA PRESENTE CONSTANCIA:", margen_x, y, ancho_texto, "Helvetica", 11)
        y -= 20
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margen_x, y, "HACE CONSTAR:")
        y -= 20
        texto = f"Que, existe vacante disponible en el NIVEL {datos['grado'].upper()} - Para el/la alumno(a) {datos['alumno'].upper()} CON DNI {datos['dni']}. Para el año escolar {anio_doc}."
        y = escribir_parrafo(c, texto, margen_x, y, ancho_texto, "Helvetica", 11)
        y -= 15
        y = escribir_parrafo(c, "Por lo que se debe consignar los siguientes documentos:", margen_x, y, ancho_texto, "Helvetica", 11)
        y -= 15
        reqs = ["• Certificado de Estudios original.", "• Resolución de traslado.", "• Libreta de SIAGIE.", "• Ficha única de matrícula.", "• Copia DNI (Alumno y Padres).", "• Constancia de no Deudor."]
        for r in reqs:
            c.drawString(margen_x+20, y, r)
            y -= 15
        y -= 20
        c.drawString(margen_x, y, "Se expide a solicitud del Padre/Madre:")
        y -= 15
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(width/2, y, f"{datos['apoderado'].upper()} CON DNI {datos['dni_apo']}")

    elif tipo_doc == "CONSTANCIA DE NO DEUDOR":
        y -= 20
        y = escribir_parrafo(c, "LA DIRECCIÓN DE LA INSTITUCIÓN EDUCATIVA ALTERNATIVO YACHAY DE CHINCHERO.", margen_x, y, ancho_texto, "Helvetica", 12)
        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen_x, y, "HACE CONSTAR:")
        y -= 30
        texto = f"Que el (la) estudiante: {datos['alumno'].upper()} CON DNI {datos['dni']}. No presenta ninguna deuda ni por matrícula ni por mensualidades."
        y = escribir_parrafo(c, texto, margen_x, y, ancho_texto, "Helvetica", 12, 16)
        y -= 40
        y = escribir_parrafo(c, "Se expide a petición escrita del apoderado.", margen_x, y, ancho_texto, "Helvetica", 12)

    elif tipo_doc == "CONSTANCIA DE ESTUDIOS":
        y -= 20
        y = escribir_parrafo(c, "LA DIRECCIÓN DE LA INSTITUCIÓN EDUCATIVA PARTICULAR ALTERNATIVO YACHAY DE CHINCHERO, SUSCRIBE LA PRESENTE CONSTANCIA DE ESTUDIOS:", margen_x, y, ancho_texto, "Helvetica", 12)
        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen_x, y, "HACE CONSTAR:")
        y -= 20
        texto = f"Que, la alumna(o), {datos['alumno'].upper()} CON DNI {datos['dni']}. Se encuentra matriculado en esta institución para este año escolar {anio_doc} en el NIVEL {datos['grado'].upper()}."
        y = escribir_parrafo(c, texto, margen_x, y, ancho_texto, "Helvetica", 12, 16)
        y -= 20
        texto2 = f"Demostrando puntualidad y responsabilidad. Se expide a solicitud del Apoderado {datos['apoderado'].upper()} DNI {datos['dni_apo']}."
        y = escribir_parrafo(c, texto2, margen_x, y, ancho_texto, "Helvetica", 12, 16)

    elif tipo_doc == "CONSTANCIA DE CONDUCTA":
        y -= 20
        texto = f"Que, {datos['alumno'].upper()} CON DNI {datos['dni']}, ha cursado estudios obteniendo las siguientes calificaciones:"
        y = escribir_parrafo(c, texto, margen_x, y, ancho_texto, "Helvetica", 11, 14)
        y -= 30
        tx = width/2 - 120
        c.setFont("Helvetica-Bold", 10)
        c.drawString(tx, y, "GRADO"); c.drawString(tx+100, y, "AÑO"); c.drawString(tx+200, y, "NOTA")
        y -= 5; c.line(tx-10, y, tx+250, y); y -= 20
        grados = ["PRIMERO", "SEGUNDO", "TERCERO", "CUARTO", "QUINTO"]
        c.setFont("Helvetica", 10)
        hay_datos = False
        for i in range(5):
            av, nv = datos['conducta'][i]['anio'], datos['conducta'][i]['nota']
            if av or nv:
                hay_datos = True
                c.drawString(tx, y, grados[i]); c.drawString(tx+100, y, av); c.drawString(tx+200, y, nv)
                y -= 18
        if not hay_datos: c.drawString(tx, y, "-- Sin información --"); y-=20
        y -= 30
        y = escribir_parrafo(c, "Se expide a solicitud del interesado.", margen_x, y, ancho_texto, "Helvetica", 11)

    elif tipo_doc == "CONSTANCIA DE TRABAJO":
        y -= 20
        c.setFont("Helvetica-Bold", 12); c.drawString(margen_x, y, "HACE CONSTAR:"); y -= 30
        texto = f"Que, el/la Docente: {datos['alumno'].upper()} CON DNI {datos['dni']}, ha laborado en el nivel {datos['grado'].upper()}, durante el año escolar {anio_doc-1}."
        y = escribir_parrafo(c, texto, margen_x, y, ancho_texto, "Helvetica", 12, 18)
        y -= 20; c.drawString(margen_x, y, "Demostrando puntualidad, liderazgo y responsabilidad."); y -= 30
        c.drawString(margen_x, y, "Se expide a solicitud del interesado.")

    elif tipo_doc == "CARTA COMPROMISO PADRE DE FAMILIA":
        c.setFont("Helvetica", 10.5)
        intro = f"Yo {datos['apoderado'].upper()} con DNI N° {datos['dni_apo']}, padre/madre de {datos['alumno'].upper()}."
        y = escribir_parrafo(c, intro, margen_x, y, ancho_texto, "Helvetica", 10.5, 14); y -= 12
        y = escribir_parrafo(c, "Me comprometo a cumplir las siguientes disposiciones:", margen_x, y, ancho_texto, "Helvetica", 10.5, 14); y -= 18
        pts = ["1. Asistencia puntual.", "2. Cumplimiento de tareas.", "3. Uso correcto del uniforme y aseo.", "4. Respeto a compañeros y docentes.", "5. Apoyo en actividades escolares.", "6. Trato sin violencia.", "7. Atención a problemas de conducta.", "8. Responsabilidad por daños materiales.", "9. Control de vocabulario.", "10. Asistencia a citaciones.", "11. Asistencia a reuniones.", "12. Justificación de faltas.", "13. Pago puntual de pensiones.", "14. No interferencia pedagógica."]
        for p in pts: y = escribir_parrafo(c, p, margen_x, y, ancho_texto, "Helvetica", 10, 13)
        y -= 15; y = escribir_parrafo(c, "La mejor herencia es la educación.", margen_x, y, ancho_texto, "Helvetica-Oblique", 10)
        y = 90; c.line(80,y,220,y); c.line(240,y,380,y); c.line(400,y,540,y); y-=15
        c.setFont("Helvetica",7)
        c.drawCentredString(150,y,"PADRE/MADRE"); c.drawCentredString(310,y,config['directora'].upper()); c.drawCentredString(310,y-10,"DIRECTORA"); c.drawCentredString(470,y,config['promotor'].upper()); c.drawCentredString(470,y-10,"PROMOTOR")
        c.save(); buffer.seek(0); return buffer

    if tipo_doc != "CARTA COMPROMISO PADRE DE FAMILIA":
        yf = 140; c.line(200,yf,395,yf); c.setFont("Helvetica-Bold",10)
        c.drawCentredString(width/2, yf-15, config['directora'].upper())
        c.setFont("Helvetica",9); c.drawCentredString(width/2, yf-28, "DIRECTORA")

        url_validacion = f"https://sistema-yachay2.streamlit.app/?validar={datos['dni']}"
        qr = qrcode.make(url_validacion)
        qr.save("temp_qr.png")
        c.drawImage("temp_qr.png", config['qr_x'], config['qr_y'], width=70, height=70)
        c.setFont("Helvetica",6); c.drawCentredString(config['qr_x']+35, config['qr_y']-5, "ESCANEAR PARA VALIDAR")

    c.save(); buffer.seek(0); return buffer

# --- GENERADOR CARNETS CON CÓDIGO DE BARRAS ---
def generar_carnet(datos, anio):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(241, 155))
    w, h = 241, 155
    
    # Marco y Encabezado
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(2)
    c.rect(2, 2, w-4, h-4)
    c.setFillColor(colors.darkblue)
    c.rect(2, h-30, w-4, 28, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(w/2, h-20, "I.E. ALTERNATIVO YACHAY")
    
    # Foto Placeholder
    c.setFillColor(colors.lightgrey)
    c.rect(10, 35, 70, 80, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 6); c.drawCentredString(45, 75, "FOTO")
    
    # Datos Texto
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(90, 105, datos['alumno'].upper())
    c.setFont("Helvetica", 9)
    c.drawString(90, 88, f"DNI: {datos['dni']}")
    c.drawString(90, 73, f"GRADO: {datos['grado']}")
    c.drawString(90, 58, f"VIGENCIA: {anio}")
    
    # QR Validación (Lado derecho superior)
    url_val = f"https://sistema-yachay2.streamlit.app/?validar={datos['dni']}"
    qr = qrcode.make(url_val)
    qr.save("temp_carnet_qr.png")
    c.drawImage("temp_carnet_qr.png", 185, 55, width=45, height=45)
    c.setFont("Helvetica", 5); c.drawCentredString(207, 50, "ESCANEAR")

    # CÓDIGO DE BARRAS (BLINDADO)
    try:
        # Generamos el código de barras 128 (estándar DNI)
        # IMPORTANTE: ImageWriter a veces falla en Linux por fuentes, usamos try/except
        bar_code = Code128(str(datos['dni']), writer=ImageWriter())
        bar_code.save("temp_barcode") 
        # Si se guardó correctamente, lo dibujamos
        if os.path.exists("temp_barcode.png"):
            c.drawImage("temp_barcode.png", 90, 10, width=130, height=35)
    except Exception as e:
        # Si falla el barcode (por fuentes del servidor), ponemos el texto como respaldo
        print(f"Error barcode: {e}") 
        c.setFont("Helvetica", 8)
        c.drawString(90, 20, f"||| {datos['dni']} |||")

    c.save(); buffer.seek(0); return buffer

# --- INTERFAZ ---
with st.sidebar:
    if os.path.exists("fondo.png"):
        st.image("fondo.png", use_container_width=True)
    st.header("⚙️ Configuración")
    
    st.subheader("📂 Base de Datos")
    uploaded_bd = st.file_uploader("Actualizar Lista Alumnos (Excel)", type=["xlsx"])
    if uploaded_bd:
        with open("base_datos.xlsx", "wb") as f:
            f.write(uploaded_bd.getbuffer())
        st.success("¡Base de datos actualizada!")
        st.rerun()

    anio_sel = st.number_input("Año:", 2024, 2030, 2026)
    
    with st.expander("🛠️ Calibración Docs"):
        y_frase = st.slider("Altura Frase:", 600, 800, 700)
        y_titulo = st.slider("Altura Título:", 500, 750, 631)
        qr_x = st.slider("QR X:", 0, 500, 435)
        qr_y = st.slider("QR Y:", 0, 200, 47)
    
    frase_sel = st.text_area("Frase:", "AÑO DE LA ESPERANZA Y EL FORTALECIMIENTO DE LA DEMOCRACIA")
    directora = st.text_input("Directora:", "Prof. Ana María CUSI INCA")
    promotor = st.text_input("Promotor:", "Prof. Leandro CORDOVA TOCRE")
    
    if st.button("🔒 CERRAR SESIÓN", type="primary"):
        st.session_state.autenticado = False
        st.rerun()

tab1, tab2, tab3 = st.tabs(["📄 DOCUMENTOS", "🪪 CARNETS", "📊 ESTADO"])

with tab1:
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("### 🔍 Buscador de Alumnos")
        col_b1, col_b2 = st.columns([3,1])
        with col_b1:
            dni_buscar = st.text_input("Ingrese DNI para buscar:", placeholder="Ej: 73840561")
        with col_b2:
            if st.button("🔎 Buscar"):
                res = buscar_alumno(dni_buscar)
                if res is not None:
                    # Guardamos en Session State
                    st.session_state.alumno = res['Alumno']
                    st.session_state.dni = res['DNI']
                    st.session_state.grado = res['Grado']
                    st.session_state.apoderado = res['Apoderado']
                    st.session_state.dni_apo = res['DNI_Apoderado']
                    st.success("¡Datos encontrados!")
                else:
                    st.error("DNI no encontrado.")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        tipo = st.selectbox("Documento:", ["CONSTANCIA DE VACANTE", "CONSTANCIA DE NO DEUDOR", "CONSTANCIA DE ESTUDIOS", "CONSTANCIA DE CONDUCTA", "CONSTANCIA DE TRABAJO", "CARTA COMPROMISO PADRE DE FAMILIA"])
        alumno = st.text_input("Alumno/Docente:", key="alumno")
        dni = st.text_input("DNI:", key="dni")
        grado = st.text_input("Grado/Nivel:", key="grado")
    with c2:
        if tipo != "CONSTANCIA DE TRABAJO":
            apoderado = st.text_input("Apoderado:", key="apoderado")
            dni_apo = st.text_input("DNI Apoderado:", key="dni_apo")
        else:
            apoderado, dni_apo = "", ""
            st.info("No requiere apoderado")

    cond_data = []
    if tipo == "CONSTANCIA DE CONDUCTA":
        st.caption("Notas de Conducta:")
        cc = st.columns(5)
        for i in range(5):
            with cc[i]:
                a = st.text_input(f"{i+1}° Año", key=f"cond_anio_{i+1}")
                n = st.text_input(f"Nota", key=f"cond_nota_{i+1}")
                cond_data.append({"anio": a, "nota": n})
    else:
        for i in range(5): cond_data.append({"anio":"", "nota":""})

    if st.button("🖨️ GENERAR PDF DOC", use_container_width=True):
        if alumno and dni:
            datos = {"alumno":alumno, "dni":dni, "grado":grado, "apoderado":apoderado, "dni_apo":dni_apo, "conducta":cond_data}
            config = {"frase":frase_sel, "anio":anio_sel, "y_frase":y_frase, "y_titulo":y_titulo, "qr_x":qr_x, "qr_y":qr_y, "directora":directora, "promotor":promotor}
            pdf = generar_pdf_doc(tipo, datos, config)
            st.success("✅ Generado")
            st.download_button("⬇️ Descargar PDF", pdf, file_name=f"{tipo}_{dni}.pdf", mime="application/pdf")

with tab2:
    st.subheader("Generador de Carnets (Con Código de Barras)")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.write(f"**Alumno:** {st.session_state.alumno}")
        st.write(f"**DNI:** {st.session_state.dni}")
    with col_c2:
        if st.session_state.dni:
            if st.button("💳 Generar Carnet"):
                datos_c = {"alumno":st.session_state.alumno, "dni":st.session_state.dni, "grado":st.session_state.grado}
                carnet_pdf = generar_carnet(datos_c, anio_sel)
                st.download_button("⬇️ Descargar Carnet", carnet_pdf, file_name=f"Carnet_{st.session_state.dni}.pdf", mime="application/pdf")

with tab3:
    st.subheader("Estado del Sistema")
    bd = cargar_bd()
    if bd is not None:
        st.success(f"Base de Datos conectada: {len(bd)} alumnos registrados.")
        st.dataframe(bd)
    else:
        st.warning("⚠️ No hay Base de Datos cargada.")

if st.sidebar.button("🧹 Limpiar Campos"):
    limpiar_datos()
    st.rerun()
