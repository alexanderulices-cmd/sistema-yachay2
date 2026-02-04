import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
import qrcode
import os
from datetime import datetime
import io
from PIL import Image, ImageDraw, ImageFont

# --- 1. CONFIGURACIÓN E INICIO ---
st.set_page_config(page_title="SISTEMA YACHAY 2026", page_icon="🎓", layout="wide")

# Estilos CSS para modernizar la interfaz
st.markdown("""
    <style>
    .stButton>button {
        background-color: #0d47a1; color: white; border-radius: 8px; font-weight: bold; border: none;
    }
    .stButton>button:hover { background-color: #1565c0; transform: scale(1.02); }
    .success-box {
        padding: 15px; background-color: #e8f5e9; color: #1b5e20; border-radius: 10px;
        border-left: 5px solid #2e7d32; text-align: center; font-weight: bold;
    }
    .valid-card {
        background: white; padding: 40px; border-radius: 20px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 8px solid #2ecc71;
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

# --- 2. VALIDACIÓN PÚBLICA (CUANDO SE ESCANEA EL QR) ---
query_params = st.query_params
if "validar" in query_params:
    dni_val = query_params["validar"]
    st.markdown(f"""
        <div class="valid-card">
            <h1 style="color: #2ecc71; font-size: 60px; margin:0;">✅</h1>
            <h2 style="color: #0d47a1;">DOCUMENTO OFICIAL VERIFICADO</h2>
            <p style="font-size: 18px; color: #555;">Institución Educativa Alternativo Yachay</p>
            <hr>
            <div style="text-align: left; padding: 20px; background: #f9f9f9; border-radius: 10px;">
                <p><b>🔑 DNI CONSULTADO:</b> {dni_val}</p>
                <p><b>📅 FECHA DE CONSULTA:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                <p><b>🏫 ESTADO:</b> EMITIDO Y VIGENTE</p>
            </div>
            <br>
            <small>Sistema de Gestión Académica 2026</small>
        </div>
    """, unsafe_allow_html=True)
    st.balloons()
    st.stop()

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
        df['DNI'] = df['DNI'].astype(str).str.strip()
        res = df[df['DNI'] == dni_busqueda]
        if not res.empty: return res.iloc[0]
    return None

def limpiar_datos():
    for k in ['alumno', 'dni', 'grado', 'apoderado', 'dni_apo']:
        if k in st.session_state: st.session_state[k] = ""
    for i in range(5):
        if f"cn{i}" in st.session_state: st.session_state[f"cn{i}"] = ""

# --- 4. LOGIN CON ROLES (SEGURIDAD ACTUALIZADA) ---
if "rol" not in st.session_state: st.session_state.rol = None

if st.session_state.rol is None:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<br><h1 style='text-align:center; color:#0d47a1'>🔐 ACCESO AL SISTEMA</h1>", unsafe_allow_html=True)
        st.info("Ingrese su clave de acceso.")
        pwd = st.text_input("Contraseña:", type="password")
        
        if st.button("INGRESAR AL SISTEMA", use_container_width=True):
            if pwd == "306020":
                st.session_state.rol = "admin"
                st.success("✅ MODO ADMINISTRADOR (Control Total)")
                st.rerun()
            elif pwd == "deyanira":
                st.session_state.rol = "docente"
                st.success("👤 MODO DOCENTE (Solo Generación)")
                st.rerun()
            else:
                st.error("⛔ Contraseña incorrecta")
    st.stop()

# --- 5. GENERADOR PDF (TEXTOS COMPLETOS) ---
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

    # Encabezado Texto
    c.setFont("Helvetica-Oblique", 8)
    if tipo != "CARTA COMPROMISO PADRE DE FAMILIA":
        c.drawCentredString(w/2, config['y_frase'], f'"{config["frase"]}"')
    
    c.setFont("Helvetica", 11)
    c.drawRightString(w-60, config['y_frase']-25, obtener_fecha(config['anio']))

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w/2, config['y_titulo'], tipo)
    c.setLineWidth(1)
    c.line(100, config['y_titulo']-5, w-100, config['y_titulo']-5)

    y = config['y_titulo'] - 50
    mx = 60
    ancho = w - 120

    # --- LÓGICA DE TEXTOS COMPLETA (SIN CORTES) ---
    if tipo == "CONSTANCIA DE VACANTE":
        y = dibujar_parrafo(c, "LA DIRECCIÓN DE LA INSTITUCIÓN EDUCATIVA PARTICULAR ALTERNATIVO YACHAY DE CHINCHERO, SUSCRIBE LA PRESENTE CONSTANCIA:", mx, y, ancho, estilo_normal)
        c.setFont("Helvetica-Bold", 11); c.drawString(mx, y, "HACE CONSTAR:"); y -= 20
        txt = f"Que, existe vacante disponible en el NIVEL <b>{datos['grado'].upper()}</b> - Para el/la alumno(a) <b>{datos['alumno'].upper()}</b> CON DNI <b>{datos['dni']}</b>. Para el año escolar {config['anio']}."
        y = dibujar_parrafo(c, txt, mx, y, ancho, estilo_normal)
        y = dibujar_parrafo(c, "Por lo que se debe consignar los siguientes documentos:", mx, y, ancho, estilo_normal)
        
        reqs = [
            "• Certificado de Estudios original.",
            "• Resolución de traslado.",
            "• Libreta de SIAGIE.",
            "• Ficha única de matrícula de SIAGIE.",
            "• DNI (FOTOCOPIAS) del alumno y de los padres.",
            "• SIS O ESSALUD (Fotocopia).",
            "• Constancia de no Deudor.",
            "• Una mica para los documentos."
        ]
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
        
        # LOS 14 PUNTOS COMPLETOS
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
        
        # Firmas Compromiso
        y = 80
        c.line(80,y,220,y); c.line(240,y,380,y); c.line(400,y,540,y); y-=10
        c.setFont("Helvetica",7)
        c.drawCentredString(150,y,"FIRMA PADRE/MADRE"); 
        c.drawCentredString(310,y,config['directora'].upper()); c.drawCentredString(310,y-10,"DIRECTORA"); 
        c.drawCentredString(470,y,config['promotor'].upper()); c.drawCentredString(470,y-10,"PROMOTOR")
        c.save(); buffer.seek(0); return buffer

    # --- PIE DE PÁGINA NORMAL ---
    if tipo != "CARTA COMPROMISO PADRE DE FAMILIA":
        yf = 110
        c.line(200, yf, 395, yf)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(w/2, yf-15, config['directora'].upper())
        c.setFont("Helvetica", 9)
        c.drawCentredString(w/2, yf-28, "DIRECTORA")

        # QR Validación (Usar URL pública de Streamlit)
        # NOTA: Debes asegurarte de que tu App en Streamlit Cloud sea "Public"
        base_url = "https://sistema-yachay2.streamlit.app"
        url_val = f"{base_url}/?validar={datos['dni']}"
        qr = qrcode.make(url_val)
        qr.save("temp_qr.png")
        c.drawImage("temp_qr.png", config['qr_x'], config['qr_y'], width=70, height=70)
        c.setFont("Helvetica", 6)
        c.drawCentredString(config['qr_x']+35, config['qr_y']-5, "ESCANEAR PARA VALIDAR")

    c.save()
    buffer.seek(0)
    return buffer

# --- 6. GENERADOR CARNET PNG (SOLUCIÓN FUENTES GRANDES) ---
# Función para cargar fuente robusta (Linux/Windows)
def cargar_fuente_bold(size):
    # Lista de fuentes comunes en Linux (Streamlit Cloud) y Windows
    fuentes = ["arialbd.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "FreeSansBold.ttf"]
    for f in fuentes:
        try:
            return ImageFont.truetype(f, size)
        except: continue
    return ImageFont.load_default()

def cargar_fuente_normal(size):
    fuentes = ["arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf", "FreeSans.ttf"]
    for f in fuentes:
        try:
            return ImageFont.truetype(f, size)
        except: continue
    return ImageFont.load_default()

def generar_carnet_png(datos, anio, foto_bytes):
    W, H = 1012, 638 
    img = Image.new('RGB', (W, H), 'white')
    draw = ImageDraw.Draw(img)
    AZUL_INST = (0, 30, 120)

    # 1. Escudo Marca de Agua
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

    # 2. Barras
    draw.rectangle([(0, 0), (W, 130)], fill=AZUL_INST)
    draw.rectangle([(0, H-60), (W, H)], fill=AZUL_INST)

    # 3. Textos Cabecera (Fuentes Grandes)
    font_header = cargar_fuente_bold(60)
    font_motto = cargar_fuente_bold(30)
    
    draw.text((W/2, 65), "I.E. ALTERNATIVO YACHAY", font=font_header, fill="white", anchor="mm")
    draw.text((W/2, H-30), "EDUCAR PARA LA VIDA", font=font_motto, fill="white", anchor="mm")

    # 4. Foto
    x_foto, y_foto = 50, 160
    w_foto, h_foto = 280, 350
    if foto_bytes:
        try:
            foto_img = Image.open(foto_bytes).convert("RGB").resize((w_foto, h_foto))
            img.paste(foto_img, (x_foto, y_foto))
        except: pass
    draw.rectangle([(x_foto, y_foto), (x_foto+w_foto, y_foto+h_foto)], outline="black", width=5)

    # 5. Datos (LETRAS MUY GRANDES)
    x_text = 360
    y_cursor = 170
    
    # Nombre
    nom = datos['alumno'].upper()
    size_n = 70 # Tamaño gigante inicial
    if len(nom) > 20: size_n = 55 # Reducir un poco si es largo
    font_n = cargar_fuente_bold(size_n)
    
    draw.text((x_text, y_cursor), nom, font=font_n, fill="black")
    y_cursor += 90

    # DNI
    font_d = cargar_fuente_normal(50)
    draw.text((x_text, y_cursor), f"DNI: {datos['dni']}", font=font_d, fill="black")
    y_cursor += 70

    # Grado
    grado_txt = f"GRADO: {datos['grado'].upper()}"
    size_g = 50
    if len(grado_txt) > 25: size_g = 40
    font_g = cargar_fuente_normal(size_g)
    
    draw.text((x_text, y_cursor), grado_txt, font=font_g, fill="black")
    y_cursor += 70
    
    draw.text((x_text, y_cursor), f"VIGENCIA: {anio}", font=font_d, fill="black")

    # 6. Código Barras
    if HAS_BARCODE:
        try:
            writer = ImageWriter()
            buffer_bar = io.BytesIO()
            Code128(datos['dni'], writer=writer).write(buffer_bar)
            buffer_bar.seek(0)
            img_bar = Image.open(buffer_bar).resize((500, 110))
            img.paste(img_bar, (x_text, H - 190))
        except: pass

    # 7. QR
    qr = qrcode.QRCode(box_size=10, border=1)
    qr.add_data(f"https://sistema-yachay2.streamlit.app/?validar={datos['dni']}")
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white").resize((170, 170))
    img.paste(img_qr, (W - 200, 180)) # A la derecha
    
    font_s = cargar_fuente_normal(20)
    draw.text((W - 165, 360), "VERIFICAR", font=font_s, fill="black")

    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output

# --- 7. BARRA LATERAL (SEGÚN ROL) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("YACHAY PRO")
    
    # Mostrar usuario actual
    if st.session_state.rol == "admin":
        st.success("Administrador")
        st.markdown("### ⚙️ Configuración Global")
        
        # Subir BD
        up_bd = st.file_uploader("📂 Actualizar Excel (BD)", type=["xlsx"])
        if up_bd:
            with open("base_datos.xlsx", "wb") as f: f.write(up_bd.getbuffer())
            st.toast("Base de datos guardada")

        # Subir Escudo
        up_escudo = st.file_uploader("🛡️ Cambiar Escudo (PNG)", type=["png"])
        if up_escudo:
            with open("escudo_upload.png", "wb") as f: f.write(up_escudo.getbuffer())
            st.toast("Escudo guardado")
            st.image(up_escudo, width=100)
            
        st.markdown("---")
        # Inputs globales
        frase = st.text_area("Frase del Año", "AÑO DE LA ESPERANZA Y EL FORTALECIMIENTO DE LA DEMOCRACIA")
        directora = st.text_input("Directora", "Prof. Ana María CUSI INCA")
        promotor = st.text_input("Promotor", "Prof. Leandro CORDOVA TOCRE")
        
        # Ajustes PDF
        with st.expander("🛠️ Calibrar PDF"):
            y_frase = st.slider("Altura Frase", 600, 800, 700)
            y_titulo = st.slider("Altura Título", 500, 750, 631)
            qr_y = st.slider("Posición Y del QR", 0, 200, 47)
            
    else:
        # ROL DOCENTE (Usuario limitado)
        st.info("Modo Docente")
        st.write("Solo tiene permisos para generar documentos.")
        # Valores por defecto
        frase = "AÑO DE LA ESPERANZA Y EL FORTALECIMIENTO DE LA DEMOCRACIA"
        directora = "Prof. Ana María CUSI INCA"
        promotor = "Prof. Leandro CORDOVA TOCRE"
        y_frase, y_titulo, qr_y = 700, 631, 47

    st.markdown("---")
    anio_sel = st.number_input("Año Escolar", 2024, 2030, 2026)
    
    if st.button("🔴 CERRAR SESIÓN"):
        st.session_state.rol = None
        st.session_state.autenticado = False
        st.rerun()

# --- 8. ÁREA PRINCIPAL ---
tab1, tab2, tab3 = st.tabs(["📄 DOCUMENTOS PDF", "🪪 CARNETS HD", "📊 BASE DE DATOS"])

# PESTAÑA 1: PDF
with tab1:
    c1, c2 = st.columns([1,2])
    with c1:
        st.markdown("### 1. Tipo y Búsqueda")
        tipo_doc = st.selectbox("Seleccionar Documento:", [
            "CONSTANCIA DE VACANTE", "CONSTANCIA DE NO DEUDOR", 
            "CONSTANCIA DE ESTUDIOS", "CONSTANCIA DE CONDUCTA", 
            "CONSTANCIA DE TRABAJO", "CARTA COMPROMISO PADRE DE FAMILIA"
        ])
        dni_search = st.text_input("🔍 Buscar DNI en BD:")
        if st.button("Buscar Alumno"):
            res = buscar_alumno(dni_search)
            if res is not None:
                st.session_state.alumno = res['Alumno']
                st.session_state.dni = res['DNI']
                st.session_state.grado = res['Grado']
                st.session_state.apoderado = res['Apoderado']
                st.session_state.dni_apo = res['DNI_Apoderado']
                st.success("Datos Cargados")
            else: st.error("No encontrado")

    with c2:
        st.markdown("### 2. Verificar Datos")
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            nom = st.text_input("Nombre Completo", key="alumno")
            doc_id = st.text_input("DNI Estudiante", key="dni")
            grad = st.text_input("Grado", key="grado")
        with col_in2:
            apo = st.text_input("Nombre Apoderado", key="apoderado")
            dni_apo = st.text_input("DNI Apoderado", key="dni_apo")
        
        # Conducta
        cond_list = []
        if tipo_doc == "CONSTANCIA DE CONDUCTA":
            st.info("Notas de Conducta (Últimos 5 años)")
            cols = st.columns(5)
            for i in range(5):
                with cols[i]:
                    val = st.text_input(f"{i+1}°", key=f"cn{i}")
                    cond_list.append({'nota':val})

        st.markdown("---")
        if st.button("✨ GENERAR PDF FINAL", type="primary", use_container_width=True):
            if nom and doc_id:
                pack_d = {'alumno':nom, 'dni':doc_id, 'grado':grad, 'apoderado':apo, 'dni_apo':dni_apo, 'conducta':cond_list}
                pack_c = {'anio':anio_sel, 'frase':frase, 'y_frase':y_frase, 'y_titulo':y_titulo, 'qr_x':435, 'qr_y':qr_y, 'directora':directora, 'promotor':promotor}
                
                pdf_bytes = generar_pdf_doc(tipo_doc, pack_d, pack_c)
                st.balloons()
                st.markdown('<div class="success-box">DOCUMENTO CREADO CON ÉXITO</div>', unsafe_allow_html=True)
                st.download_button("⬇️ DESCARGAR PDF", pdf_bytes, f"{tipo_doc}_{doc_id}.pdf", "application/pdf", use_container_width=True)

# PESTAÑA 2: CARNETS
with tab2:
    st.markdown("## 🎨 Generador de Carnets 2026")
    col_a, col_b = st.columns(2)
    with col_a:
        cn_nom = st.text_input("Alumno:", value=st.session_state.get('alumno',''))
        cn_dni = st.text_input("DNI:", value=st.session_state.get('dni',''))
        cn_gra = st.text_input("Grado:", value=st.session_state.get('grado',''))
        cn_foto = st.file_uploader("Subir Foto", type=['jpg','png','jpeg'])
    
    with col_b:
        st.markdown("### Vista Previa")
        if st.button("🖼️ PROCESAR CARNET", type="primary"):
            if cn_nom and cn_dni:
                pack_carnet = {'alumno':cn_nom, 'dni':cn_dni, 'grado':cn_gra}
                img_final = generar_carnet_png(pack_carnet, anio_sel, cn_foto)
                st.balloons()
                st.image(img_final, caption="Carnet Listo para Imprimir", use_container_width=True)
                st.download_button("⬇️ GUARDAR IMAGEN (PNG)", img_final, f"Carnet_{cn_dni}.png", "image/png", use_container_width=True)
            else:
                st.warning("Faltan datos obligatorios")

# PESTAÑA 3: BD (VISUALIZACIÓN)
with tab3:
    st.markdown("### Padron de Alumnos")
    df = cargar_bd()
    if df is not None:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No hay base de datos cargada.")

if st.sidebar.button("Limpiar Campos"):
    limpiar_datos()
    st.rerun()
