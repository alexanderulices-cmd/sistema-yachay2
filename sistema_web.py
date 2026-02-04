import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import qrcode
import os
from datetime import datetime
import io
from PIL import Image, ImageDraw, ImageFont
import requests
import textwrap
import zipfile
import time

# --- 1. CONFIGURACIÓN E INICIO ---
st.set_page_config(page_title="SISTEMA YACHAY 2026", page_icon="🎓", layout="wide")

# Inicializar Cola de Impresión
if 'cola_carnets' not in st.session_state:
    st.session_state.cola_carnets = []

# Estilos CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: #0d47a1; color: white; border-radius: 8px; font-weight: bold; border: none;
        height: 50px; font-size: 16px; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { 
        background-color: #1565c0; transform: translateY(-2px); box-shadow: 0 6px 8px rgba(0,0,0,0.2);
    }
    .frase-login {
        font-size: 45px !important; font-weight: 900; color: #0d47a1; text-align: center;
        text-transform: uppercase; margin-bottom: 15px; line-height: 1.1;
        font-family: 'Arial Black', sans-serif; animation: fadeIn 1.5s;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# Importación segura de código de barras
try:
    from barcode import Code128
    from barcode.writer import ImageWriter
    HAS_BARCODE = True
except ImportError:
    HAS_BARCODE = False

# --- 2. GESTIÓN DE FUENTES ---
def descargar_fuentes():
    urls = {
        "Roboto-Bold.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Bold.ttf",
        "Roboto-Regular.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf"
    }
    for nombre, url in urls.items():
        if not os.path.exists(nombre):
            try:
                r = requests.get(url)
                with open(nombre, 'wb') as f: f.write(r.content)
            except: pass

descargar_fuentes()

def obtener_fuente_bold(size):
    try: return ImageFont.truetype("Roboto-Bold.ttf", size)
    except: return ImageFont.load_default()

def obtener_fuente_normal(size):
    try: return ImageFont.truetype("Roboto-Regular.ttf", size)
    except: return ImageFont.load_default()

# --- 3. FUNCIONES DE BASE DE DATOS ---
def cargar_bd():
    try:
        if os.path.exists("base_datos.xlsx"):
            return pd.read_excel("base_datos.xlsx", dtype=str, engine='openpyxl')
        return None
    except: return None

def buscar_alumno(dni_busqueda):
    df = cargar_bd()
    if df is not None:
        dni_busqueda = str(dni_busqueda).strip()
        if 'DNI' in df.columns:
            df['DNI'] = df['DNI'].astype(str).str.strip()
            res = df[df['DNI'] == dni_busqueda]
            if not res.empty: return res.iloc[0]
    return None

def limpiar_datos():
    claves = ['alumno', 'dni', 'grado', 'apoderado', 'dni_apo']
    for k in claves:
        if k in st.session_state: st.session_state[k] = ""
    if 'cola_carnets' in st.session_state:
        st.session_state.cola_carnets = []

# --- 4. LOGIN DE SEGURIDAD ---
if "rol" not in st.session_state: st.session_state.rol = None

if st.session_state.rol is None:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if os.path.exists("escudo_upload.png"):
            st.image("escudo_upload.png", width=150)
            st.markdown("""<style>div[data-testid="stImage"]{display:block;margin-left:auto;margin-right:auto;width:50%;}</style>""", unsafe_allow_html=True)
        
        st.markdown('<div class="frase-login">EDUCAR PARA<br>LA VIDA</div>', unsafe_allow_html=True)
        
        pwd = st.text_input("🔑 Contraseña:", type="password")
        
        if st.button("INGRESAR AL SISTEMA", use_container_width=True):
            if pwd == "306020":
                st.session_state.rol = "admin"
                st.rerun()
            elif pwd == "deyanira":
                st.session_state.rol = "docente"
                st.rerun()
            else:
                st.error("⛔ Contraseña incorrecta")
    st.stop()

# --- 5. GENERADOR PDF (DOCUMENTOS COMPLETOS) ---
def obtener_fecha(anio):
    meses = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
    hoy = datetime.now()
    return f"Chinchero, {hoy.day} de {meses[hoy.month]} del {anio}"

def dibujar_parrafo(c, texto, x, y, ancho, estilo):
    p = Paragraph(texto, estilo)
    w, h = p.wrap(ancho, 600)
    p.drawOn(c, x, y - h)
    return y - h - 15

def generar_pdf_doc(tipo, datos, config):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4
    styles = getSampleStyleSheet()
    
    estilo_normal = ParagraphStyle('NormalY', parent=styles['Normal'], fontSize=11, leading=15, fontName="Helvetica", alignment=TA_JUSTIFY)
    estilo_lista = ParagraphStyle('ListaY', parent=styles['Normal'], fontSize=10, leading=13, fontName="Helvetica", leftIndent=25, alignment=TA_JUSTIFY)
    
    # Fondo
    if os.path.exists("fondo.png"):
        try: c.drawImage("fondo.png", 0, 0, width=w, height=h)
        except: pass

    # Encabezado genérico
    c.setFont("Helvetica-Oblique", 8)
    if tipo != "CARTA COMPROMISO PADRE DE FAMILIA":
        c.drawCentredString(w/2, config['y_frase'], f'"{config["frase"]}"')
    
    c.setFont("Helvetica", 11)
    c.drawRightString(w-60, config['y_frase']-25, obtener_fecha(config['anio']))

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w/2, config['y_titulo'], tipo)
    c.setLineWidth(1)
    c.line(100, config['y_titulo']-5, w-100, config['y_titulo']-5)

    y = config['y_titulo'] - 50
    mx = 60
    ancho = w - 120

    # --- LÓGICA DE CADA DOCUMENTO ---
    if tipo == "CONSTANCIA DE VACANTE":
        y = dibujar_parrafo(c, "LA DIRECCIÓN DE LA INSTITUCIÓN EDUCATIVA PARTICULAR ALTERNATIVO YACHAY DE CHINCHERO, SUSCRIBE LA PRESENTE CONSTANCIA:", mx, y, ancho, estilo_normal)
        c.setFont("Helvetica-Bold", 11); c.drawString(mx, y, "HACE CONSTAR:"); y -= 20
        txt = f"Que, existe vacante disponible en el NIVEL <b>{datos['grado'].upper()}</b> - Para el/la alumno(a) <b>{datos['alumno'].upper()}</b> CON DNI <b>{datos['dni']}</b>. Para el año escolar {config['anio']}."
        y = dibujar_parrafo(c, txt, mx, y, ancho, estilo_normal)
        y = dibujar_parrafo(c, "Por lo que se debe consignar los siguientes documentos:", mx, y, ancho, estilo_normal)
        reqs = ["• Certificado de Estudios original.", "• Resolución de traslado.", "• Libreta de SIAGIE.", "• Ficha única de matrícula de SIAGIE.", "• DNI (FOTOCOPIAS) del alumno y de los padres.", "• SIS O ESSALUD (Fotocopia).", "• Constancia de no Deudor.", "• Una mica para los documentos."]
        for r in reqs: y = dibujar_parrafo(c, r, mx, y, ancho, estilo_lista)
        y -= 10
        c.drawString(mx, y, "Se le expide el presente documento a solicitud de:")
        y -= 20
        c.drawCentredString(w/2, y, f"{datos['apoderado'].upper()} CON DNI {datos['dni_apo']}")

    elif tipo == "CONSTANCIA DE NO DEUDOR":
        y = dibujar_parrafo(c, "LA DIRECTORA DE LA INSTITUCIÓN EDUCATIVA ALTERNATIVO YACHAY DE CHINCHERO.", mx, y, ancho, estilo_normal)
        c.setFont("Helvetica-Bold", 12); c.drawString(mx, y, "HACE CONSTAR:"); y -= 25
        txt = f"Que el (la) estudiante: <b>{datos['alumno'].upper()}</b> CON DNI <b>{datos['dni']}</b>. No presenta ninguna deuda ni por matrícula ni por mensualidades a lo largo de sus estudios en nuestra Institución."
        y = dibujar_parrafo(c, txt, mx, y, ancho, estilo_normal)
        y -= 20
        y = dibujar_parrafo(c, "Se expide la presente constancia a petición escrita del apoderado para los fines que viera por conveniente.", mx, y, ancho, estilo_normal)

    elif tipo == "CONSTANCIA DE ESTUDIOS":
        y = dibujar_parrafo(c, "LA DIRECCIÓN DE LA INSTITUCIÓN EDUCATIVA PARTICULAR ALTERNATIVO YACHAY DE CHINCHERO, SUSCRIBE LA PRESENTE CONSTANCIA DE ESTUDIOS:", mx, y, ancho, estilo_normal)
        c.setFont("Helvetica-Bold", 12); c.drawString(mx, y, "HACE CONSTAR:"); y -= 25
        txt = f"Que, la alumna(o), <b>{datos['alumno'].upper()}</b> CON DNI <b>{datos['dni']}</b>. Se encuentra matriculado en esta institución para este año escolar {config['anio']} en el NIVEL <b>{datos['grado'].upper()}</b>."
        y = dibujar_parrafo(c, txt, mx, y, ancho, estilo_normal)
        txt2 = f"Demostrando puntualidad y responsabilidad en sus actividades escolares. Se le expide el presente documento a solicitud del Apoderado <b>{datos['apoderado'].upper()}</b> DNI <b>{datos['dni_apo']}</b>."
        y = dibujar_parrafo(c, txt2, mx, y, ancho, estilo_normal)

    elif tipo == "CONSTANCIA DE CONDUCTA":
        txt = f"Que, <b>{datos['alumno'].upper()}</b> CON DNI <b>{datos['dni']}</b>, CURSO ESTUDIOS SECUNDARIOS EN EL AÑO {int(config['anio'])-1} TENIENDO LAS SIGUIENTES CALIFICACIONES EN CONDUCTA:"
        y = dibujar_parrafo(c, txt, mx, y, ancho, estilo_normal)
        y -= 20
        tx = w/2 - 120
        c.setFont("Helvetica-Bold", 10)
        c.drawString(tx, y, "GRADO"); c.drawString(tx+100, y, "AÑO"); c.drawString(tx+200, y, "NOTA")
        y -= 5; c.line(tx-10, y, tx+250, y); y -= 20
        # Tabla simple
        c.setFont("Helvetica", 10)
        c.drawString(tx, y, datos['grado'].upper())
        c.drawString(tx+100, y, str(int(config['anio']) - 1))
        c.drawString(tx+200, y, "A (AD)")
        y -= 30
        y = dibujar_parrafo(c, "Se le expide el presente documento a solicitud del interesado para los fines que viera por conveniencia.", mx, y, ancho, estilo_normal)

    elif tipo == "CARTA COMPROMISO PADRE DE FAMILIA":
        estilo_comp = ParagraphStyle('Compromiso', parent=styles['Normal'], fontSize=9, leading=11, alignment=TA_JUSTIFY)
        intro = f"Por medio del presente Yo <b>{datos['apoderado'].upper()}</b> identificado con DNI N° <b>{datos['dni_apo']}</b>, padre o madre de familia de mi menor hijo(a), llamado(a) <b>{datos['alumno'].upper()}</b>."
        y = dibujar_parrafo(c, intro, mx, y, ancho, estilo_comp)
        consciente = "Consciente de las normas y disposiciones de la Dirección del Colegio y la importancia que tiene para la formación de los aprendizajes de mi hij@ en los valores de DISCIPLINA, respeto, puntualidad, responsabilidad y solidaridad. Me doy por enterado y me comprometo a contribuir como padre de familia a respetar y cumplir las siguientes disposiciones:"
        y = dibujar_parrafo(c, consciente, mx, y, ancho, estilo_comp)
        
        pts = [
            "1. Cuidaré que mi hij@ asista al colegio, con puntualidad en la hora de entrada y sin faltar los días laborables.",
            "2. Cuidaré que mi hijo cumpla diariamente con sus tareas escolares dándole el apoyo necesario.",
            "3. Enviaré a mi hij@ al colegio bien aseado, con cabello corto varones y con uniforme.",
            "4. Será mi responsabilidad, exigir permanentemente a mi hij@ que sea respetuoso.",
            "5. Colaboraré en las necesidades que el docente requiera en aula.",
            "6. Trataré bien y sin violencia física y verbal a mi hijo@.",
            "7. Atenderé los problemas de conducta y aprendizaje de mi hijo@.",
            "8. Me responsabilizaré de los daños que ocasione mi hija@ en el local escolar.",
            "9. Estaré comprometido a vigilar que mi hijo no use vocabulario inadecuado.",
            "10. Acudiré a la escuela en caso de llamado del docente.",
            "11. Asistiré puntualmente cuando sea convocado a reunión.",
            "12. Justificaré oportunamente las inasistencias.",
            "13. Pagaré oportunamente cada fin de mes la pensión mensual.",
            "14. Me comprometo a no interferir en las actividades pedagógicas."
        ]
        
        estilo_items = ParagraphStyle('ItemsComp', parent=styles['Normal'], fontSize=8.5, leading=10, leftIndent=10)
        for p in pts: 
            y = dibujar_parrafo(c, p, mx, y, ancho, estilo_items)
            y += 5
            
        y -= 10
        final = "Por su parte el Consejo Directivo del colegio seguirá mejorando el servicio educativo en base a: Disciplina, responsabilidad, seguridad de sus hijo@s... Confíe en su colegio y asegure la buena formación de su hij@. <i>La mejor herencia a los hijos es la educación.</i>"
        y = dibujar_parrafo(c, final, mx, y, ancho, estilo_comp)
        
        y = 80
        c.line(80,y,220,y); c.line(240,y,380,y); c.line(400,y,540,y); y-=10
        c.setFont("Helvetica",7)
        c.drawCentredString(150,y,"FIRMA PADRE/MADRE"); 
        c.drawCentredString(310,y,config['directora'].upper()); c.drawCentredString(310,y-10,"DIRECTORA"); 
        c.drawCentredString(470,y,"PROMOTOR"); c.drawCentredString(470,y-10,"PROMOTOR")
        c.save(); buffer.seek(0); return buffer

    # Firmas y QR para otros docs
    if tipo != "CARTA COMPROMISO PADRE DE FAMILIA":
        yf = 110
        c.line(200, yf, 395, yf)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(w/2, yf-15, config['directora'].upper())
        c.setFont("Helvetica", 9)
        c.drawCentredString(w/2, yf-28, "DIRECTORA")

        data_qr = f"✅ I.E. YACHAY\nTIPO: {tipo}\nALUMNO: {datos['alumno']}\nDNI: {datos['dni']}\nEMISIÓN: {datetime.now().strftime('%d/%m/%Y')}"
        qr = qrcode.QRCode(box_size=10, border=1)
        qr.add_data(data_qr)
        qr.make(fit=True)
        img_qr_doc = qr.make_image(fill_color="black", back_color="white")
        img_qr_doc.save("temp_qr.png")
        c.drawImage("temp_qr.png", config['qr_x'], config['qr_y'], width=70, height=70)
        c.setFont("Helvetica", 6)
        c.drawCentredString(config['qr_x']+35, config['qr_y']-5, "ESCANEAR PARA VALIDAR")

    c.save()
    buffer.seek(0)
    return buffer

# --- 6. GENERADOR CARNET PNG (FINAL) ---
def generar_carnet_png(datos, anio, foto_bytes=None):
    W, H = 1012, 638 
    img = Image.new('RGB', (W, H), 'white')
    draw = ImageDraw.Draw(img)
    AZUL_INST = (0, 30, 120)

    # 1. Escudo de fondo
    if os.path.exists("escudo_upload.png"):
        try:
            escudo = Image.open("escudo_upload.png").convert("RGBA")
            escudo = escudo.resize((400, 400))
            capa = Image.new('RGBA', (W, H), (0,0,0,0))
            capa.paste(escudo, (int((W-400)/2), int((H-400)/2)))
            datos_p = capa.getdata()
            new_data = [(d[0], d[1], d[2], 30) if d[3]>0 else d for d in datos_p]
            capa.putdata(new_data)
            img.paste(capa, (0,0), mask=capa)
        except: pass

    # 2. Barras Azules
    draw.rectangle([(0, 0), (W, 130)], fill=AZUL_INST) 
    draw.rectangle([(0, H-100), (W, H)], fill=AZUL_INST) 

    # 3. Encabezado y Pie
    font_header = obtener_fuente_bold(65) 
    font_motto = obtener_fuente_bold(50) 
    
    draw.text((W/2, 65), "I.E. ALTERNATIVO YACHAY", font=font_header, fill="white", anchor="mm")
    draw.text((W/2, H-50), "EDUCAR PARA LA VIDA", font=font_motto, fill="white", anchor="mm")

    # 4. Foto
    x_foto, y_foto = 50, 160
    w_foto, h_foto = 290, 360
    if foto_bytes:
        try:
            foto_img = Image.open(foto_bytes).convert("RGB").resize((w_foto, h_foto))
            img.paste(foto_img, (x_foto, y_foto))
        except: pass
    else:
        draw.rectangle([(x_foto, y_foto), (x_foto+w_foto, y_foto+h_foto)], fill="#eeeeee")
    draw.rectangle([(x_foto, y_foto), (x_foto+w_foto, y_foto+h_foto)], outline="black", width=6)

    # 5. DATOS DEL ALUMNO (Lógica Dinámica)
    x_text = 370
    y_nombre_base = 170
    y_dni = 290
    y_grado = 360
    y_vigencia = 430
    
    nom = datos['alumno'].upper()
    
    # REGLA: Si es largo, sube y se divide. Si es corto, grande y normal.
    if len(nom) > 22:
        font_n = obtener_fuente_bold(40)
        wrapper = textwrap.TextWrapper(width=25) 
        lines = wrapper.wrap(nom)
        y_cursor = y_nombre_base - 10 
        for line in lines[:2]: 
            draw.text((x_text, y_cursor), line, font=font_n, fill="black")
            y_cursor += 45
    else:
        font_n = obtener_fuente_bold(55) 
        draw.text((x_text, y_nombre_base), nom, font=font_n, fill="black")

    # DNI
    font_lbl = obtener_fuente_normal(45) 
    draw.text((x_text, y_dni), f"DNI: {datos['dni']}", font=font_lbl, fill="black")

    # GRADO
    grado_txt = f"GRADO: {datos['grado'].upper()}"
    font_g = obtener_fuente_normal(45)
    if len(grado_txt) > 22: font_g = obtener_fuente_normal(35)
    draw.text((x_text, y_grado), grado_txt, font=font_g, fill="black")
    
    # VIGENCIA
    draw.text((x_text, y_vigencia), f"VIGENCIA: {anio}", font=font_lbl, fill="black")

    # 6. CÓDIGO DE BARRAS
    if HAS_BARCODE:
        try:
            writer = ImageWriter()
            buffer_bar = io.BytesIO()
            Code128(datos['dni'], writer=writer).write(buffer_bar, options={'write_text': False})
            buffer_bar.seek(0)
            img_bar = Image.open(buffer_bar).resize((450, 100))
            img.paste(img_bar, (x_text, H - 210))
        except: pass

    # 7. QR CARNET
    try:
        qr = qrcode.QRCode(box_size=10, border=1)
        qr.add_data(str(datos['dni']))
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white").resize((180, 180))
        img.paste(img_qr, (W - 200, 170)) 
    except: pass
    
    font_s = obtener_fuente_normal(20)
    draw.text((W - 110, 360), "ESCANEAR", font=font_s, fill="black", anchor="mm")

    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output

# --- 7. BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("YACHAY PRO")
    
    if st.session_state.rol == "admin":
        st.success("Modo Admin")
        st.markdown("### ⚙️ Datos")
        up_bd = st.file_uploader("📂 Excel Alumnos", type=["xlsx"])
        if up_bd:
            with open("base_datos.xlsx", "wb") as f: f.write(up_bd.getbuffer())
            st.toast("Datos Actualizados")

        up_escudo = st.file_uploader("🛡️ Escudo", type=["png"])
        if up_escudo:
            with open("escudo_upload.png", "wb") as f: f.write(up_escudo.getbuffer())
            
        st.markdown("---")
        directora = st.text_input("Directora", "Prof. Ana María CUSI INCA")
        frase = st.text_area("Frase", "AÑO DE LA ESPERANZA Y EL FORTALECIMIENTO DE LA DEMOCRACIA")
    else:
        st.info("Modo Docente")
        directora = "Prof. Ana María CUSI INCA"
        frase = "AÑO DE LA INTEGRACIÓN"

    st.markdown("---")
    anio_sel = st.number_input("Año", 2024, 2030, 2026)
    
    if st.button("🔴 SALIR"):
        st.session_state.rol = None
        st.rerun()

# --- 8. TABS PRINCIPALES ---
tab1, tab2, tab3 = st.tabs(["📄 DOCUMENTOS", "🪪 CARNETS (ACUMULAR)", "📊 BASE DATOS"])

with tab1:
    st.header("Emisión de Documentos")
    col1, col2 = st.columns([1,2])
    with col1:
        tipo_doc = st.selectbox("Tipo:", ["CONSTANCIA DE VACANTE", "CONSTANCIA DE NO DEUDOR", "CONSTANCIA DE ESTUDIOS", "CONSTANCIA DE CONDUCTA", "CARTA COMPROMISO PADRE DE FAMILIA"])
        dni_doc = st.text_input("🔍 Buscar DNI (Docs):")
        if st.button("Buscar Doc"):
            res = buscar_alumno(dni_doc)
            if res is not None:
                st.session_state.alumno = res['Alumno']
                st.session_state.dni = res['DNI']
                st.session_state.grado = res['Grado']
                st.session_state.apoderado = res['Apoderado']
                st.session_state.dni_apo = res['DNI_Apoderado']
                st.toast("Datos cargados")
            else: st.error("No encontrado")

    with col2:
        with st.container(border=True):
            nom = st.text_input("Alumno", key="alumno")
            did = st.text_input("DNI", key="dni")
            gra = st.text_input("Grado", key="grado")
            apo = st.text_input("Apoderado", key="apoderado")
            dap = st.text_input("DNI Apoderado", key="dni_apo")

            if st.button("✨ GENERAR PDF", type="primary", use_container_width=True):
                if nom and did:
                    pack = {'alumno':nom, 'dni':did, 'grado':gra, 'apoderado':apo, 'dni_apo':dap}
                    conf = {'anio':anio_sel, 'frase':frase, 'y_frase':700, 'y_titulo':630, 'qr_x':435, 'qr_y':47, 'directora':directora}
                    pdf = generar_pdf_doc(tipo_doc, pack, conf)
                    st.balloons()
                    st.download_button("⬇️ DESCARGAR PDF", pdf, f"{tipo_doc}.pdf", "application/pdf", use_container_width=True)
                else: st.error("Faltan datos")

with tab2:
    st.markdown("## 🏭 Fábrica de Carnets (Acumulador)")
    
    col_izq, col_der = st.columns([1, 1.2])
    
    # LADO IZQUIERDO: BUSCAR Y AGREGAR
    with col_izq:
        st.info("1. Busca al alumno y agrégalo a la cola:")
        search_dni = st.text_input("🔍 Buscar DNI para Carnet:")
        if st.button("Buscar Alumno"):
            res = buscar_alumno(search_dni)
            if res is not None:
                st.session_state.temp_alumno = res['Alumno']
                st.session_state.temp_dni = res['DNI']
                st.session_state.temp_grado = res['Grado']
                st.success("Encontrado")
            else: st.error("No encontrado")

        c_nom = st.text_input("Nombre:", value=st.session_state.get('temp_alumno',''))
        c_dni = st.text_input("DNI:", value=st.session_state.get('temp_dni',''))
        c_gra = st.text_input("Grado:", value=st.session_state.get('temp_grado',''))
        c_foto = st.file_uploader("Foto (Opcional)", type=['jpg','png','jpeg'], key="foto_up")

        if st.button("➕ AGREGAR A LA COLA", type="primary"):
            if c_nom and c_dni:
                f_bytes = c_foto.getvalue() if c_foto else None
                item = {'alumno': c_nom, 'dni': c_dni, 'grado': c_gra, 'foto_bytes': f_bytes}
                
                # Evitar duplicados
                if c_dni not in [x['dni'] for x in st.session_state.cola_carnets]:
                    st.session_state.cola_carnets.append(item)
                    st.toast(f"Agregado: {c_nom}")
                else: st.warning("Ya está en la lista")
            else: st.error("Faltan datos")

    # LADO DERECHO: LISTA Y DESCARGA
    with col_der:
        cantidad = len(st.session_state.cola_carnets)
        st.warning(f"📦 EN COLA: {cantidad} CARNETS")
        
        if cantidad > 0:
            df_c = pd.DataFrame(st.session_state.cola_carnets)
            st.dataframe(df_c[['alumno', 'dni', 'grado']], hide_index=True, use_container_width=True)
            
            if st.button("🚀 DESCARGAR PACK ZIP", type="primary", use_container_width=True):
                z_buf = io.BytesIO()
                prog = st.progress(0)
                with zipfile.ZipFile(z_buf, "w") as zf:
                    for i, it in enumerate(st.session_state.cola_carnets):
                        f_io = io.BytesIO(it['foto_bytes']) if it['foto_bytes'] else None
                        img = generar_carnet_png(it, anio_sel, f_io)
                        zf.writestr(f"Carnet_{it['dni']}.png", img.getvalue())
                        prog.progress((i+1)/cantidad)
                z_buf.seek(0)
                st.balloons()
                st.download_button("⬇️ GUARDAR ZIP", z_buf, "Pack_Carnets.zip", "application/zip", use_container_width=True)
            
            if st.button("🗑️ VACIAR LISTA"):
                st.session_state.cola_carnets = []
                st.rerun()
        else:
            st.info("La lista está vacía.")

with tab3:
    st.dataframe(cargar_bd(), use_container_width=True)
