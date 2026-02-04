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

# --- 1. CONFIGURACIÓN E INICIO ---
st.set_page_config(page_title="SISTEMA YACHAY 2026", page_icon="🎓", layout="wide")

# Estilos CSS (Botones y alertas)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #0d47a1; color: white; border-radius: 8px; font-weight: bold; border: none;
        height: 50px; font-size: 16px;
    }
    .stButton>button:hover { background-color: #1565c0; transform: scale(1.02); }
    .success-box {
        padding: 15px; background-color: #e8f5e9; color: #1b5e20; border-radius: 10px;
        border-left: 5px solid #2e7d32; text-align: center; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Importación segura de código de barras
try:
    from barcode import Code128
    from barcode.writer import ImageWriter
    HAS_BARCODE = True
except ImportError:
    HAS_BARCODE = False

# --- 2. FUNCIONES DE BASE DE DATOS ---
def cargar_bd():
    try:
        if os.path.exists("base_datos.xlsx"):
            # Leemos todo como texto (dtype=str) para evitar que el DNI pierda ceros
            return pd.read_excel("base_datos.xlsx", dtype=str, engine='openpyxl')
        return None
    except: return None

def buscar_alumno(dni_busqueda):
    df = cargar_bd()
    if df is not None:
        dni_busqueda = str(dni_busqueda).strip()
        # Aseguramos que la columna DNI sea string y sin espacios
        if 'DNI' in df.columns:
            df['DNI'] = df['DNI'].astype(str).str.strip()
            res = df[df['DNI'] == dni_busqueda]
            if not res.empty: return res.iloc[0]
    return None

def limpiar_datos():
    claves = ['alumno', 'dni', 'grado', 'apoderado', 'dni_apo']
    for k in claves:
        if k in st.session_state: st.session_state[k] = ""
    for i in range(5):
        if f"cn{i}" in st.session_state: st.session_state[f"cn{i}"] = ""

# --- 3. LOGIN DE SEGURIDAD ---
if "rol" not in st.session_state: st.session_state.rol = None

if st.session_state.rol is None:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<br><h1 style='text-align:center; color:#0d47a1'>🔐 ACCESO AL SISTEMA</h1>", unsafe_allow_html=True)
        st.info("Sistema de Gestión Documental Yachay")
        pwd = st.text_input("Ingrese Contraseña:", type="password")
        
        if st.button("INGRESAR", use_container_width=True):
            if pwd == "306020":
                st.session_state.rol = "admin"
                st.success("✅ BIENVENIDO ADMINISTRADOR")
                st.rerun()
            elif pwd == "deyanira":
                st.session_state.rol = "docente"
                st.success("👤 BIENVENIDA DOCENTE")
                st.rerun()
            else:
                st.error("⛔ Contraseña incorrecta")
    st.stop()

# --- 4. GESTOR DE FUENTES (LETRAS GIGANTES) ---
def obtener_fuente_gigante(size):
    font_path = "Roboto-Bold.ttf"
    if not os.path.exists(font_path):
        url = "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Bold.ttf"
        try:
            r = requests.get(url)
            with open(font_path, 'wb') as f: f.write(r.content)
        except: pass
    try: return ImageFont.truetype(font_path, size)
    except: return ImageFont.load_default()

def obtener_fuente_normal(size):
    font_path = "Roboto-Regular.ttf"
    if not os.path.exists(font_path):
        url = "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf"
        try:
            r = requests.get(url)
            with open(font_path, 'wb') as f: f.write(r.content)
        except: pass
    try: return ImageFont.truetype(font_path, size)
    except: return ImageFont.load_default()

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
    
    # Estilos de texto
    estilo_normal = ParagraphStyle('NormalY', parent=styles['Normal'], fontSize=11, leading=15, fontName="Helvetica", alignment=TA_JUSTIFY)
    estilo_lista = ParagraphStyle('ListaY', parent=styles['Normal'], fontSize=10, leading=13, fontName="Helvetica", leftIndent=25, alignment=TA_JUSTIFY)
    
    # 1. Fondo (Marca de agua)
    if os.path.exists("fondo.png"):
        try: c.drawImage("fondo.png", 0, 0, width=w, height=h)
        except: pass

    # 2. Encabezado
    c.setFont("Helvetica-Oblique", 8)
    # En Carta Compromiso no va la frase arriba
    if tipo != "CARTA COMPROMISO PADRE DE FAMILIA":
        c.drawCentredString(w/2, config['y_frase'], f'"{config["frase"]}"')
    
    c.setFont("Helvetica", 11)
    c.drawRightString(w-60, config['y_frase']-25, obtener_fecha(config['anio']))

    # 3. Título del Documento
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w/2, config['y_titulo'], tipo)
    c.setLineWidth(1)
    c.line(100, config['y_titulo']-5, w-100, config['y_titulo']-5)

    y = config['y_titulo'] - 50
    mx = 60
    ancho = w - 120

    # --- LÓGICA DE CONTENIDO POR TIPO ---
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
        txt = f"Que, <b>{datos['alumno'].upper()}</b> CON DNI <b>{datos['dni']}</b>, CURSO ESTUDIOS SECUNDARIOS EN EL AÑO {int(config['anio'])-5} AL {int(config['anio'])-1} TENIENDO LAS SIGUIENTES CALIFICACIONES EN CONDUCTA:"
        y = dibujar_parrafo(c, txt, mx, y, ancho, estilo_normal)
        y -= 20
        tx = w/2 - 120
        c.setFont("Helvetica-Bold", 10)
        c.drawString(tx, y, "GRADO"); c.drawString(tx+100, y, "AÑO"); c.drawString(tx+200, y, "NOTA")
        y -= 5; c.line(tx-10, y, tx+250, y); y -= 20
        grados_txt = ["PRIMERO", "SEGUNDO", "TERCERO", "CUARTO", "QUINTO"]
        c.setFont("Helvetica", 10)
        hay_notas = False
        for i in range(5):
            nota = datos['conducta'][i].get('nota', '') if 'conducta' in datos and i < len(datos['conducta']) else ""
            if nota:
                hay_notas = True
                c.drawString(tx, y, grados_txt[i])
                c.drawString(tx+100, y, str(int(config['anio']) - (5-i)))
                c.drawString(tx+200, y, nota)
                y -= 18
        if not hay_notas: c.drawString(tx, y, "-- No se registraron notas --"); y-=20
        y -= 30
        y = dibujar_parrafo(c, "Se le expide el presente documento a solicitud del interesado para los fines que viera por conveniencia.", mx, y, ancho, estilo_normal)

    elif tipo == "CONSTANCIA DE TRABAJO":
        c.setFont("Helvetica-Bold", 12); c.drawString(mx, y, "HACE CONSTAR:"); y -= 30
        txt = f"Que, la Profesora/Profesor: <b>{datos['alumno'].upper()}</b> CON DNI <b>{datos['dni']}</b>, con domicilio legal en Cusco. Ha desarrollado su Trabajo como Docente de aula en el nivel <b>{datos['grado'].upper()}</b>, durante el año escolar {int(config['anio'])-1} en la INSTITUCIÓN EDUCATIVA ALTERNATIVO YACHAY."
        y = dibujar_parrafo(c, txt, mx, y, ancho, estilo_normal)
        y -= 10
        c.drawString(mx, y, "Demostrando puntualidad, liderazgo y responsabilidad.")
        y -= 30
        c.drawString(mx, y, "Se le expide la presente constancia a solicitud del interesado.")

    elif tipo == "CARTA COMPROMISO PADRE DE FAMILIA":
        # Texto COMPLETO de 14 PUNTOS
        estilo_comp = ParagraphStyle('Compromiso', parent=styles['Normal'], fontSize=9, leading=11, alignment=TA_JUSTIFY)
        intro = f"Por medio del presente Yo <b>{datos['apoderado'].upper()}</b> identificado con DNI N° <b>{datos['dni_apo']}</b>, padre o madre de familia de mi menor hijo(a), llamado(a) <b>{datos['alumno'].upper()}</b>."
        y = dibujar_parrafo(c, intro, mx, y, ancho, estilo_comp)
        consciente = "Consciente de las normas y disposiciones de la Dirección del Colegio y la importancia que tiene para la formación de los aprendizajes de mi hij@ en los valores de DISCIPLINA, respeto, puntualidad, responsabilidad y solidaridad. Me doy por enterado y me comprometo a contribuir como padre de familia a respetar y cumplir las siguientes disposiciones:"
        y = dibujar_parrafo(c, consciente, mx, y, ancho, estilo_comp)
        
        pts = [
            "1. Cuidaré que mi hij@ asista al colegio, con puntualidad en la hora de entrada y sin faltar los días laborables y con mayor razón en las actividades que programe el colegio.",
            "2. Cuidaré que mi hijo cumpla diariamente con sus tareas escolares dándole el apoyo necesario para que las realice satisfactoriamente, haré que lea 20 minutos algún texto cada día y estoy en pleno conocimiento que de no ser así ello impactaría en sus aprendizajes y evaluaciones.",
            "3. Enviaré a mi hij@ al colegio bien aseado, con cabello corto varones y con uniforme o buzo del colegio en los días que corresponda asistir, con mayor énfasis en los desfiles y actividades importantes que programe el colegio.",
            "4. Será mi responsabilidad, exigir permanentemente a mi hij@ que sea respetuoso (saludar, agradecer, pedir favor y pedir disculpas) en la casa en la calle y en el colegio, hasta que le sea un hábito.",
            "5. Colaboraré en las necesidades que el docente requiera en aula, así como cumplir con los acuerdos del comité de aula así como del colegio.",
            "6. Trataré bien y sin violencia física y verbal a mi hijo@ a fin de que se encuentre en condiciones de dar un buen rendimiento escolar.",
            "7. Atenderé los problemas de conducta y aprendizaje de mi hijo@, manteniendo comunicación con su maestr@, tomando en cuenta sus sugerencia, indicaciones u observaciones. Todo esto lo haré cuando su maestr@ solicite mi presencia en la institución Educativa.",
            "8. Me responsabilizaré de los daños que ocasione mi hija@ en el local escolar, mobiliario y otros enseres del aula, reparándolo o reponiendo según corresponda.",
            "9. Estaré comprometido a vigilar que mi hijo no use vocabulario inadecuado, conductas impropias, agresiones físicas o verbales a sus compañeros o adultos que laboran en esta institución y fuera de ella.",
            "10. Acudiré a la escuela en caso de llamado del docente, Auxiliar de Educación o Directora, así como cumpliré con las medidas disciplinarias adoptadas por la dirección del colegio o docente.",
            "11. Asistiré puntualmente cuando sea convocado a la reunión o llamado por parte del docente o Directora de la institución.",
            "12. Justificaré oportunamente llamando o por escrito las inasistencia de mi hijo@, ya que el 30% de inasistencias da lugar al retiro por inasistencia de la Institución Educativa.",
            "13. Pagaré oportunamente cada fin de mes la pensión mensual de enseñanza a la Dirección del Colegio, conforme lo acordado.",
            "14. Me comprometo a no interferir en las actividades pedagógicas y administrativas de la Institución Educativa y/o interrumpir a los profesores en horas de clase."
        ]
        
        estilo_items = ParagraphStyle('ItemsComp', parent=styles['Normal'], fontSize=8.5, leading=10, leftIndent=10)
        for p in pts: 
            y = dibujar_parrafo(c, p, mx, y, ancho, estilo_items)
            y += 5
            
        y -= 10
        final = "Por su parte el Consejo Directivo del colegio seguirá mejorando el servicio educativo en base a: Disciplina, responsabilidad, seguridad de sus hijo@s... Confíe en su colegio y asegure la buena formación de su hij@. <i>La mejor herencia a los hijos es la educación.</i>"
        y = dibujar_parrafo(c, final, mx, y, ancho, estilo_comp)
        
        # Firmas para el compromiso
        y = 80
        c.line(80,y,220,y); c.line(240,y,380,y); c.line(400,y,540,y); y-=10
        c.setFont("Helvetica",7)
        c.drawCentredString(150,y,"FIRMA PADRE/MADRE"); 
        c.drawCentredString(310,y,config['directora'].upper()); c.drawCentredString(310,y-10,"DIRECTORA"); 
        c.drawCentredString(470,y,config['promotor'].upper()); c.drawCentredString(470,y-10,"PROMOTOR")
        c.save(); buffer.seek(0); return buffer

    # PIE DE PÁGINA (SOLO PARA EL RESTO DE DOCUMENTOS)
    if tipo != "CARTA COMPROMISO PADRE DE FAMILIA":
        yf = 110
        c.line(200, yf, 395, yf)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(w/2, yf-15, config['directora'].upper())
        c.setFont("Helvetica", 9)
        c.drawCentredString(w/2, yf-28, "DIRECTORA")

        # --- QR DE DOCUMENTO (SEGURIDAD COMPLETA) ---
        # Contiene: Check verde, Nombre, DNI, Fecha y Hora exacta.
        data_qr = f"✅ I.E. YACHAY - DOCUMENTO VÁLIDO\nTIPO: {tipo}\nALUMNO: {datos['alumno']}\nDNI: {datos['dni']}\nEMISIÓN: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        qr = qrcode.make(data_qr)
        qr.save("temp_qr.png")
        c.drawImage("temp_qr.png", config['qr_x'], config['qr_y'], width=70, height=70)
        c.setFont("Helvetica", 6)
        c.drawCentredString(config['qr_x']+35, config['qr_y']-5, "ESCANEAR PARA VALIDAR")

    c.save()
    buffer.seek(0)
    return buffer

# --- 6. GENERADOR CARNET PNG (CON QR DE SOLO DNI) ---
def generar_carnet_png(datos, anio, foto_bytes=None):
    W, H = 1012, 638 
    img = Image.new('RGB', (W, H), 'white')
    draw = ImageDraw.Draw(img)
    AZUL_INST = (0, 30, 120)

    # 1. Escudo (Marca de agua)
    if os.path.exists("escudo_upload.png"):
        try:
            escudo = Image.open("escudo_upload.png").convert("RGBA")
            escudo = escudo.resize((380, 380))
            capa = Image.new('RGBA', (W, H), (0,0,0,0))
            capa.paste(escudo, (int((W-380)/2), int((H-380)/2)))
            # Transparencia
            datos_p = capa.getdata()
            new_data = [(d[0], d[1], d[2], 35) if d[3]>0 else d for d in datos_p]
            capa.putdata(new_data)
            img.paste(capa, (0,0), mask=capa)
        except: pass

    # 2. Barras Azules
    draw.rectangle([(0, 0), (W, 130)], fill=AZUL_INST)
    draw.rectangle([(0, H-60), (W, H)], fill=AZUL_INST)

    # 3. Texto Institucional (Gigante)
    font_header = obtener_fuente_gigante(60)
    font_motto = obtener_fuente_gigante(30)
    
    draw.text((W/2, 65), "I.E. ALTERNATIVO YACHAY", font=font_header, fill="white", anchor="mm")
    draw.text((W/2, H-30), "EDUCAR PARA LA VIDA", font=font_motto, fill="white", anchor="mm")

    # 4. Marco de Foto
    x_foto, y_foto = 50, 160
    w_foto, h_foto = 280, 350
    if foto_bytes:
        try:
            foto_img = Image.open(foto_bytes).convert("RGB").resize((w_foto, h_foto))
            img.paste(foto_img, (x_foto, y_foto))
        except: pass
    else:
        # Placeholder gris
        draw.rectangle([(x_foto, y_foto), (x_foto+w_foto, y_foto+h_foto)], fill="#eeeeee")
        
    draw.rectangle([(x_foto, y_foto), (x_foto+w_foto, y_foto+h_foto)], outline="black", width=5)

    # 5. DATOS DEL ALUMNO
    x_text = 360
    y_cursor = 170
    
    nom = datos['alumno'].upper()
    
    # Lógica de ajuste de nombre largo
    wrapper = textwrap.TextWrapper(width=22) 
    lines = wrapper.wrap(nom)
    
    if len(lines) > 1:
        font_n = obtener_fuente_gigante(55)
        for line in lines[:2]: # Max 2 lineas
            draw.text((x_text, y_cursor), line, font=font_n, fill="black")
            y_cursor += 65
    else:
        font_n = obtener_fuente_gigante(65)
        draw.text((x_text, y_cursor), nom, font=font_n, fill="black")
        y_cursor += 80 

    y_cursor += 15

    # DNI y Grado
    font_d = obtener_fuente_normal(50)
    draw.text((x_text, y_cursor), f"DNI: {datos['dni']}", font=font_d, fill="black")
    y_cursor += 70

    grado_txt = f"GRADO: {datos['grado'].upper()}"
    size_g = 50
    if len(grado_txt) > 25: size_g = 40
    font_g = obtener_fuente_normal(size_g)
    
    draw.text((x_text, y_cursor), grado_txt, font=font_g, fill="black")
    y_cursor += 70
    draw.text((x_text, y_cursor), f"VIGENCIA: {anio}", font=font_d, fill="black")

    # 6. CÓDIGO DE BARRAS (Funcional)
    if HAS_BARCODE:
        try:
            writer = ImageWriter()
            buffer_bar = io.BytesIO()
            # El código de barras contiene el DNI
            Code128(datos['dni'], writer=writer).write(buffer_bar)
            buffer_bar.seek(0)
            img_bar = Image.open(buffer_bar).resize((500, 110))
            img.paste(img_bar, (x_text, H - 190))
        except: pass

    # 7. QR CARNET (SOLO NÚMERO DE DNI)
    # Esto permite lectura rápida con pistola o celular
    qr_content = str(datos['dni']) 
    qr = qrcode.make(qr_content)
    img_qr = qr.make_image(fill_color="black", back_color="white").resize((170, 170))
    img.paste(img_qr, (W - 200, 180)) 
    
    font_s = obtener_fuente_normal(20)
    draw.text((W - 165, 360), "ESCANEAR", font=font_s, fill="black")

    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output

# --- 7. BARRA LATERAL (CONFIGURACIÓN) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("YACHAY PRO")
    
    if st.session_state.rol == "admin":
        st.success("Modo Administrador")
        st.markdown("### ⚙️ Carga de Archivos")
        
        up_bd = st.file_uploader("📂 Base de Datos (Excel)", type=["xlsx"])
        if up_bd:
            with open("base_datos.xlsx", "wb") as f: f.write(up_bd.getbuffer())
            st.toast("Base de datos actualizada correctamente")

        up_escudo = st.file_uploader("🛡️ Escudo (PNG)", type=["png"])
        if up_escudo:
            with open("escudo_upload.png", "wb") as f: f.write(up_escudo.getbuffer())
            st.toast("Escudo cargado")
            
        st.markdown("---")
        st.markdown("### ⚙️ Textos")
        frase = st.text_area("Frase del Año", "AÑO DE LA ESPERANZA Y EL FORTALECIMIENTO DE LA DEMOCRACIA")
        directora = st.text_input("Directora", "Prof. Ana María CUSI INCA")
        promotor = st.text_input("Promotor", "Prof. Leandro CORDOVA TOCRE")
        
        with st.expander("🛠️ Calibración Avanzada PDF"):
            y_frase = st.slider("Altura Frase", 600, 800, 700)
            y_titulo = st.slider("Altura Título", 500, 750, 631)
            qr_y = st.slider("Posición Y QR (PDF)", 0, 200, 47)
            
    else:
        st.info("Modo Docente")
        # Valores por defecto para docente
        frase = "AÑO DE LA ESPERANZA Y EL FORTALECIMIENTO DE LA DEMOCRACIA"
        directora = "Prof. Ana María CUSI INCA"
        promotor = "Prof. Leandro CORDOVA TOCRE"
        y_frase, y_titulo, qr_y = 700, 631, 47

    st.markdown("---")
    anio_sel = st.number_input("Año Escolar", 2024, 2030, 2026)
    
    if st.button("🔴 CERRAR SESIÓN"):
        st.session_state.rol = None
        st.rerun()

# --- 8. ÁREA PRINCIPAL (TABS) ---
tab1, tab2, tab3 = st.tabs(["📄 DOCUMENTOS PDF", "🪪 CARNETS HD", "📊 BASE DE DATOS"])

# --- PESTAÑA 1: DOCUMENTOS ---
with tab1:
    c1, c2 = st.columns([1,2])
    with c1:
        st.markdown("### 1. Selección y Búsqueda")
        tipo_doc = st.selectbox("Tipo de Documento:", [
            "CONSTANCIA DE VACANTE", "CONSTANCIA DE NO DEUDOR", 
            "CONSTANCIA DE ESTUDIOS", "CONSTANCIA DE CONDUCTA", 
            "CONSTANCIA DE TRABAJO", "CARTA COMPROMISO PADRE DE FAMILIA"
        ])
        st.info("Ingrese DNI para autocompletar:")
        dni_search = st.text_input("🔍 Buscar DNI:")
        if st.button("Buscar Alumno", use_container_width=True):
            res = buscar_alumno(dni_search)
            if res is not None:
                st.session_state.alumno = res['Alumno']
                st.session_state.dni = res['DNI']
                st.session_state.grado = res['Grado']
                st.session_state.apoderado = res['Apoderado']
                st.session_state.dni_apo = res['DNI_Apoderado']
                st.success("✅ Datos Cargados Exitosamente")
            else: st.error("❌ DNI no encontrado en Base de Datos")

    with c2:
        st.markdown("### 2. Edición y Emisión")
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            nom = st.text_input("Nombre Estudiante", key="alumno")
            doc_id = st.text_input("DNI Estudiante", key="dni")
            grad = st.text_input("Grado", key="grado")
        with col_in2:
            apo = st.text_input("Nombre Apoderado", key="apoderado")
            dni_apo = st.text_input("DNI Apoderado", key="dni_apo")
        
        cond_list = []
        if tipo_doc == "CONSTANCIA DE CONDUCTA":
            st.warning("⚠️ Ingrese las notas de conducta manualmente:")
            cols = st.columns(5)
            for i in range(5):
                with cols[i]:
                    val = st.text_input(f"{i+1}°", key=f"cn{i}")
                    cond_list.append({'nota':val})

        st.markdown("---")
        if st.button("✨ GENERAR DOCUMENTO PDF", type="primary", use_container_width=True):
            if nom and doc_id:
                pack_d = {'alumno':nom, 'dni':doc_id, 'grado':grad, 'apoderado':apo, 'dni_apo':dni_apo, 'conducta':cond_list}
                pack_c = {'anio':anio_sel, 'frase':frase, 'y_frase':y_frase, 'y_titulo':y_titulo, 'qr_x':435, 'qr_y':qr_y, 'directora':directora, 'promotor':promotor}
                
                pdf_bytes = generar_pdf_doc(tipo_doc, pack_d, pack_c)
                st.balloons()
                st.markdown('<div class="success-box">DOCUMENTO GENERADO CORRECTAMENTE</div>', unsafe_allow_html=True)
                st.download_button("⬇️ DESCARGAR PDF", pdf_bytes, f"{tipo_doc}_{doc_id}.pdf", "application/pdf", use_container_width=True)
            else:
                st.error("Faltan datos del alumno.")

# --- PESTAÑA 2: CARNETS (INDIVIDUAL Y MASIVO) ---
with tab2:
    st.markdown("## 🎨 Centro de Carnetización")
    
    # SECCION A: Generación Individual
    st.markdown("### 👤 Generar Un Solo Carnet")
    col_a, col_b = st.columns(2)
    with col_a:
        cn_nom = st.text_input("Alumno:", value=st.session_state.get('alumno',''))
        cn_dni = st.text_input("DNI:", value=st.session_state.get('dni',''))
        cn_gra = st.text_input("Grado:", value=st.session_state.get('grado',''))
        cn_foto = st.file_uploader("Subir Foto Alumno (Opcional)", type=['jpg','png','jpeg'])
    
    with col_b:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("👁️ PREVISUALIZAR CARNET", type="primary", use_container_width=True):
            if cn_nom and cn_dni:
                pack_carnet = {'alumno':cn_nom, 'dni':cn_dni, 'grado':cn_gra}
                img_final = generar_carnet_png(pack_carnet, anio_sel, cn_foto)
                st.image(img_final, caption="Vista Previa", use_container_width=True)
                st.download_button("⬇️ DESCARGAR CARNET (PNG)", img_final, f"Carnet_{cn_dni}.png", "image/png", use_container_width=True)
            else:
                st.warning("Ingrese nombre y DNI para generar.")

    st.markdown("---")
    
    # SECCION B: Generación Masiva (ZIP)
    st.markdown("### 📦 Generación Masiva (LOTE)")
    st.info("Esta opción generará carnets para TODOS los alumnos en la base de datos y los descargará en un archivo ZIP comprimido.")
    
    if st.button("🚀 GENERAR Y DESCARGAR ZIP (TODOS)"):
        df_lote = cargar_bd()
        if df_lote is not None:
            zip_buffer = io.BytesIO()
            progreso = st.progress(0)
            status_text = st.empty()
            total = len(df_lote)
            
            with zipfile.ZipFile(zip_buffer, "w") as zf:
                for idx, row in df_lote.iterrows():
                    # Verificar que existan las columnas
                    if 'Alumno' in row and 'DNI' in row:
                        d_temp = {'alumno': str(row['Alumno']), 'dni': str(row['DNI']), 'grado': str(row.get('Grado',''))}
                        # Generar carnet (sin foto personal en lote)
                        img_bytes = generar_carnet_png(d_temp, anio_sel, None)
                        zf.writestr(f"Carnet_{row['DNI']}.png", img_bytes.getvalue())
                        
                        # Actualizar barra
                        progreso.progress((idx + 1) / total)
                        status_text.text(f"Procesando: {row['Alumno']}")
            
            zip_buffer.seek(0)
            progreso.empty()
            status_text.empty()
            st.balloons()
            st.success(f"✅ Proceso completado. Se generaron {total} carnets.")
            st.download_button("⬇️ DESCARGAR ARCHIVO ZIP", zip_buffer, "Carnets_Yachay_Lote.zip", "application/zip", use_container_width=True)
        else:
            st.error("❌ No se encontró la Base de Datos. Por favor cárguela en el menú lateral.")

# --- PESTAÑA 3: VER BASE DE DATOS ---
with tab3:
    st.markdown("### 📊 Padrón General de Estudiantes")
    df = cargar_bd()
    if df is not None:
        st.dataframe(df, use_container_width=True)
        st.caption(f"Total de registros: {len(df)}")
    else:
        st.warning("⚠️ No hay base de datos cargada. Suba el archivo 'base_datos.xlsx' en el menú lateral.")

if st.sidebar.button("Limpiar Campos"):
    limpiar_datos()
    st.rerun()
