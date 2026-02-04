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

# Estilos CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: #0d47a1; color: white; border-radius: 8px; font-weight: bold; border: none;
        height: 50px; font-size: 16px;
    }
    .stButton>button:hover { background-color: #1565c0; transform: scale(1.02); }
    
    /* Estilo para la frase del Login */
    .frase-login {
        font-size: 45px !important;
        font-weight: 900;
        color: #0d47a1;
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 10px;
        line-height: 1.2;
        font-family: 'Arial Black', sans-serif;
    }
    .subtitulo-login {
        font-size: 18px;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
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

def obtener_fuente_gigante(size):
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
    for i in range(5):
        if f"cn{i}" in st.session_state: st.session_state[f"cn{i}"] = ""

# --- 4. LOGIN DE SEGURIDAD (CON ESCUDO Y FRASE GRANDE) ---
if "rol" not in st.session_state: st.session_state.rol = None

if st.session_state.rol is None:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        # 1. Mostrar Escudo en el Login (Si existe)
        if os.path.exists("escudo_upload.png"):
            st.image("escudo_upload.png", width=150, use_container_width=False)
            st.markdown("""<style>div[data-testid="stImage"] {display: block; margin-left: auto; margin-right: auto; width: 50%;}</style>""", unsafe_allow_html=True)
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)

        # 2. Frase Grande Solicitada
        st.markdown('<div class="frase-login">EDUCAR PARA<br>LA VIDA</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-login">Sistema de Gestión Institucional Yachay</div>', unsafe_allow_html=True)

        # 3. Formulario
        pwd = st.text_input("🔑 Contraseña de Acceso:", type="password")
        
        if st.button("INGRESAR AL SISTEMA", use_container_width=True):
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

# --- 5. GENERADOR PDF (DOCUMENTOS) ---
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
    
    if os.path.exists("fondo.png"):
        try: c.drawImage("fondo.png", 0, 0, width=w, height=h)
        except: pass

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
        
        y = 80
        c.line(80,y,220,y); c.line(240,y,380,y); c.line(400,y,540,y); y-=10
        c.setFont("Helvetica",7)
        c.drawCentredString(150,y,"FIRMA PADRE/MADRE"); 
        c.drawCentredString(310,y,config['directora'].upper()); c.drawCentredString(310,y-10,"DIRECTORA"); 
        c.drawCentredString(470,y,config['promotor'].upper()); c.drawCentredString(470,y-10,"PROMOTOR")
        c.save(); buffer.seek(0); return buffer

    if tipo != "CARTA COMPROMISO PADRE DE FAMILIA":
        yf = 110
        c.line(200, yf, 395, yf)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(w/2, yf-15, config['directora'].upper())
        c.setFont("Helvetica", 9)
        c.drawCentredString(w/2, yf-28, "DIRECTORA")

        data_qr = f"✅ I.E. YACHAY - DOCUMENTO VÁLIDO\nTIPO: {tipo}\nALUMNO: {datos['alumno']}\nDNI: {datos['dni']}\nEMISIÓN: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
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

# --- 6. GENERADOR CARNET PNG (SOLUCIÓN NOMBRES LARGOS) ---
def generar_carnet_png(datos, anio, foto_bytes=None):
    W, H = 1012, 638 
    img = Image.new('RGB', (W, H), 'white')
    draw = ImageDraw.Draw(img)
    AZUL_INST = (0, 30, 120)

    # 1. Escudo de fondo
    if os.path.exists("escudo_upload.png"):
        try:
            escudo = Image.open("escudo_upload.png").convert("RGBA")
            escudo = escudo.resize((380, 380))
            capa = Image.new('RGBA', (W, H), (0,0,0,0))
            capa.paste(escudo, (int((W-380)/2), int((H-380)/2)))
            datos_p = capa.getdata()
            new_data = [(d[0], d[1], d[2], 35) if d[3]>0 else d for d in datos_p]
            capa.putdata(new_data)
            img.paste(capa, (0,0), mask=capa)
        except: pass

    # 2. Barras Azules
    draw.rectangle([(0, 0), (W, 125)], fill=AZUL_INST) 
    draw.rectangle([(0, H-80), (W, H)], fill=AZUL_INST) 

    # 3. Encabezado y Pie
    font_header = obtener_fuente_gigante(60) 
    font_motto = obtener_fuente_gigante(45) 
    
    draw.text((W/2, 62), "I.E. ALTERNATIVO YACHAY", font=font_header, fill="white", anchor="mm")
    draw.text((W/2, H-40), "EDUCAR PARA LA VIDA", font=font_motto, fill="white", anchor="mm")

    # 4. Marco de Foto
    x_foto, y_foto = 50, 160
    w_foto, h_foto = 280, 350
    if foto_bytes:
        try:
            foto_img = Image.open(foto_bytes).convert("RGB").resize((w_foto, h_foto))
            img.paste(foto_img, (x_foto, y_foto))
        except: pass
    else:
        draw.rectangle([(x_foto, y_foto), (x_foto+w_foto, y_foto+h_foto)], fill="#eeeeee")
    draw.rectangle([(x_foto, y_foto), (x_foto+w_foto, y_foto+h_foto)], outline="black", width=5)

    # 5. DATOS DEL ALUMNO (LÓGICA MEJORADA: APELLIDOS + NOMBRES)
    x_text = 360
    y_cursor = 165
    
    nom = datos['alumno'].upper()
    
    # REGLA: Si el nombre completo tiene más de 20 caracteres (Ej: Perez Rodriguez Juan Carlos)
    # se divide en 2 líneas y se reduce la letra para que encaje.
    if len(nom) > 20:
        # --- MODO NOMBRE LARGO (APELLIDOS + NOMBRES) ---
        wrapper = textwrap.TextWrapper(width=22) 
        lines = wrapper.wrap(nom)
        
        # Usamos fuente tamaño 45 (Grande pero manejable)
        font_n = obtener_fuente_gigante(45)
        
        # Imprimimos máximo 2 líneas para no invadir el DNI
        for line in lines[:2]: 
            draw.text((x_text, y_cursor), line, font=font_n, fill="black")
            y_cursor += 48 # Salto de línea ajustado
        
        if len(lines) == 1: y_cursor += 10 # Si por suerte entró en 1 linea siendo largo
    
    else:
        # --- MODO NOMBRE CORTO ---
        font_n = obtener_fuente_gigante(55) # Fuente Gigante Original
        draw.text((x_text, y_cursor), nom, font=font_n, fill="black")
        y_cursor += 65

    # Espacio extra de seguridad antes del DNI
    y_cursor = max(y_cursor, 275) 

    # DNI
    font_d = obtener_fuente_normal(42) 
    draw.text((x_text, y_cursor), f"DNI: {datos['dni']}", font=font_d, fill="black")
    y_cursor += 60

    # GRADO
    grado_txt = f"GRADO: {datos['grado'].upper()}"
    size_g = 42
    if len(grado_txt) > 25: size_g = 35 # Si el grado es muy largo, reduce
    font_g = obtener_fuente_normal(size_g)
    
    draw.text((x_text, y_cursor), grado_txt, font=font_g, fill="black")
    y_cursor += 60
    
    # VIGENCIA
    draw.text((x_text, y_cursor), f"VIGENCIA: {anio}", font=font_d, fill="black")

    # 6. CÓDIGO DE BARRAS
    if HAS_BARCODE:
        try:
            writer = ImageWriter()
            buffer_bar = io.BytesIO()
            Code128(datos['dni'], writer=writer).write(buffer_bar)
            buffer_bar.seek(0)
            img_bar = Image.open(buffer_bar).resize((420, 90)) # Ancho ajustado para no chocar
            img.paste(img_bar, (x_text, H - 185))
        except: pass

    # 7. QR CARNET
    try:
        qr_content = str(datos['dni'])
        qr = qrcode.QRCode(box_size=10, border=1)
        qr.add_data(qr_content)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white").resize((160, 160))
        img.paste(img_qr, (W - 190, 170)) 
    except Exception as e:
        print(f"Error QR: {e}")
    
    font_s = obtener_fuente_normal(18)
    draw.text((W - 155, 340), "ESCANEAR", font=font_s, fill="black")

    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output

# --- 7. BARRA LATERAL ---
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
        frase = st.text_area("Frase del Año", "AÑO DE LA ESPERANZA Y EL FORTALECIMIENTO DE LA DEMOCRACIA")
        directora = st.text_input("Directora", "Prof. Ana María CUSI INCA")
        promotor = st.text_input("Promotor", "Prof. Leandro CORDOVA TOCRE")
        with st.expander("🛠️ Calibración PDF"):
            y_frase = st.slider("Altura Frase", 600, 800, 700)
            y_titulo = st.slider("Altura Título", 500, 750, 631)
            qr_y = st.slider("Posición Y QR (PDF)", 0, 200, 47)
            
    else:
        st.info("Modo Docente")
        frase = "AÑO DE LA ESPERANZA Y EL FORTALECIMIENTO DE LA DEMOCRACIA"
        directora = "Prof. Ana María CUSI INCA"
        promotor = "Prof. Leandro CORDOVA TOCRE"
        y_frase, y_titulo, qr_y = 700, 631, 47

    st.markdown("---")
    anio_sel = st.number_input("Año Escolar", 2024, 2030, 2026)
    
    if st.button("🔴 CERRAR SESIÓN"):
        st.session_state.rol = None
        st.rerun()

# --- 8. ÁREA PRINCIPAL ---
tab1, tab2, tab3 = st.tabs(["📄 DOCUMENTOS PDF", "🪪 CARNETS HD", "📊 BASE DE DATOS"])

with tab1:
    c1, c2 = st.columns([1,2])
    with c1:
        st.markdown("### 1. Selección y Búsqueda")
        tipo_doc = st.selectbox("Tipo de Documento:", ["CONSTANCIA DE VACANTE", "CONSTANCIA DE NO DEUDOR", "CONSTANCIA DE ESTUDIOS", "CONSTANCIA DE CONDUCTA", "CONSTANCIA DE TRABAJO", "CARTA COMPROMISO PADRE DE FAMILIA"])
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
                st.success("✅ Datos Cargados")
            else: st.error("❌ DNI no encontrado")

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
            st.warning("⚠️ Ingrese notas de conducta:")
            cols = st.columns(5)
            for i in range(5):
                with cols[i]:
                    val = st.text_input(f"{i+1}°", key=f"cn{i}")
                    cond_list.append({'nota':val})

        st.markdown("---")
        if st.button("✨ GENERAR PDF", type="primary", use_container_width=True):
            if nom and doc_id:
                pack_d = {'alumno':nom, 'dni':doc_id, 'grado':grad, 'apoderado':apo, 'dni_apo':dni_apo, 'conducta':cond_list}
                pack_c = {'anio':anio_sel, 'frase':frase, 'y_frase':y_frase, 'y_titulo':y_titulo, 'qr_x':435, 'qr_y':qr_y, 'directora':directora, 'promotor':promotor}
                pdf_bytes = generar_pdf_doc(tipo_doc, pack_d, pack_c)
                st.balloons()
                st.download_button("⬇️ DESCARGAR PDF", pdf_bytes, f"{tipo_doc}_{doc_id}.pdf", "application/pdf", use_container_width=True)
            else: st.error("Faltan datos.")

with tab2:
    st.markdown("## 🎨 Centro de Carnetización")
    col_a, col_b = st.columns(2)
    with col_a:
        cn_nom = st.text_input("Alumno:", value=st.session_state.get('alumno',''))
        cn_dni = st.text_input("DNI:", value=st.session_state.get('dni',''))
        cn_gra = st.text_input("Grado:", value=st.session_state.get('grado',''))
        cn_foto = st.file_uploader("Subir Foto", type=['jpg','png','jpeg'])
    
    with col_b:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("👁️ PREVISUALIZAR CARNET", type="primary", use_container_width=True):
            if cn_nom and cn_dni:
                pack_carnet = {'alumno':cn_nom, 'dni':cn_dni, 'grado':cn_gra}
                img_final = generar_carnet_png(pack_carnet, anio_sel, cn_foto)
                st.image(img_final, caption="Vista Previa", use_container_width=True)
                st.download_button("⬇️ DESCARGAR CARNET", img_final, f"Carnet_{cn_dni}.png", "image/png", use_container_width=True)
            else: st.warning("Ingrese nombre y DNI.")

    st.markdown("### 📦 Generación Masiva (LOTE)")
    if st.button("🚀 GENERAR ZIP (TODOS)"):
        df_lote = cargar_bd()
        if df_lote is not None:
            zip_buffer = io.BytesIO()
            progreso = st.progress(0)
            total = len(df_lote)
            with zipfile.ZipFile(zip_buffer, "w") as zf:
                for idx, row in df_lote.iterrows():
                    if 'Alumno' in row and 'DNI' in row:
                        d_temp = {'alumno': str(row['Alumno']), 'dni': str(row['DNI']), 'grado': str(row.get('Grado',''))}
                        img_bytes = generar_carnet_png(d_temp, anio_sel, None)
                        zf.writestr(f"Carnet_{row['DNI']}.png", img_bytes.getvalue())
                        progreso.progress((idx + 1) / total)
            zip_buffer.seek(0)
            st.success(f"✅ {total} carnets generados.")
            st.download_button("⬇️ DESCARGAR ZIP", zip_buffer, "Carnets_Yachay_Lote.zip", "application/zip", use_container_width=True)
        else: st.error("Falta Base de Datos.")

with tab3:
    df = cargar_bd()
    if df is not None: st.dataframe(df, use_container_width=True)
    else: st.warning("⚠️ Cargue la base de datos en el menú lateral.")

if st.sidebar.button("Limpiar Campos"):
    limpiar_datos()
    st.rerun()
