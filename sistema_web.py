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

# --- IMPORTACIÓN SEGURA DE BARCODE ---
# Si no está instalado, no romperá el programa, solo avisará.
try:
    from barcode import Code128
    from barcode.writer import ImageWriter
    HAS_BARCODE = True
except ImportError:
    HAS_BARCODE = False

# --- 1. CONFIGURACIÓN E INICIO ---
st.set_page_config(page_title="YACHAY DIGITAL PRO", page_icon="🎓", layout="wide")

# --- 2. VALIDACIÓN PÚBLICA (CUANDO SE ESCANEA EL QR) ---
query_params = st.query_params
if "validar" in query_params:
    dni_val = query_params["validar"]
    st.markdown(f"""
        <style>
        .valid-container {{
            text-align: center; 
            padding: 40px; 
            background-color: #e8f5e9; 
            border: 3px solid #2e7d32; 
            border-radius: 15px;
            font-family: Arial, sans-serif;
            margin-top: 50px;
        }}
        .title {{ color: #1b5e20; font-size: 30px; font-weight: bold; }}
        .info {{ font-size: 20px; color: #333; margin-top: 20px; }}
        </style>
        <div class="valid-container">
            <div class="title">✅ DOCUMENTO VÁLIDO</div>
            <h2 style="color: #0d47a1;">I.E. ALTERNATIVO YACHAY</h2>
            <div class="info">
                El documento o carnet asociado al DNI: <b>{dni_val}</b><br>
                ha sido emitido oficialmente por nuestra institución.
            </div>
            <p style="margin-top: 30px; color: #666;">Fecha de consulta: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# --- 3. FUNCIONES DE BASE DE DATOS ---
def cargar_bd():
    """Carga la base de datos Excel si existe"""
    try:
        if os.path.exists("base_datos.xlsx"):
            return pd.read_excel("base_datos.xlsx", dtype=str, engine='openpyxl')
        return None
    except Exception as e:
        st.error(f"Error cargando base de datos: {e}")
        return None

def buscar_alumno(dni_busqueda):
    """Busca un alumno por DNI"""
    df = cargar_bd()
    if df is not None:
        dni_busqueda = str(dni_busqueda).strip()
        # Asegurar que la columna DNI sea string y sin espacios
        df['DNI'] = df['DNI'].astype(str).str.strip()
        res = df[df['DNI'] == dni_busqueda]
        if not res.empty:
            return res.iloc[0]
    return None

def limpiar_datos():
    """Borra los campos de la sesión"""
    keys = ['alumno', 'dni', 'grado', 'apoderado', 'dni_apo']
    for k in keys: 
        if k in st.session_state:
            st.session_state[k] = ""
    # Limpiar notas de conducta
    for i in range(5):
        if f"cn{i}" in st.session_state: st.session_state[f"cn{i}"] = ""

# --- 4. LOGIN DE SEGURIDAD ---
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🔐 YACHAY DIGITAL</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Ingrese credenciales administrativas</p>", unsafe_allow_html=True)
        pwd = st.text_input("Contraseña:", type="password")
        if st.button("Ingresar al Sistema", use_container_width=True):
            if pwd == "yachay2026":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
    st.stop()

# --- 5. GENERADOR DE DOCUMENTOS PDF (NEGRITAS Y TEXTO COMPLETO) ---
def obtener_fecha(anio):
    meses = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
    hoy = datetime.now()
    return f"Chinchero, {hoy.day} de {meses[hoy.month]} del {anio}"

def dibujar_parrafo(c, texto, x, y, ancho, estilo):
    """Dibuja un párrafo respetando HTML tags como <b>"""
    p = Paragraph(texto, estilo)
    w, h = p.wrap(ancho, 600) # Altura max disponible grande para calcular
    p.drawOn(c, x, y - h)
    return y - h - 15  # Retorna la nueva posición Y con un margen

def generar_pdf_doc(tipo, datos, config):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4
    
    # Definir Estilos de Texto
    styles = getSampleStyleSheet()
    # Estilo Normal Justificado
    estilo_normal = ParagraphStyle(
        'NormalYachay', 
        parent=styles['Normal'], 
        fontSize=11, 
        leading=15, 
        fontName="Helvetica", 
        alignment=TA_JUSTIFY
    )
    # Estilo para Listas
    estilo_lista = ParagraphStyle(
        'ListaYachay', 
        parent=styles['Normal'], 
        fontSize=10, 
        leading=13, 
        fontName="Helvetica", 
        leftIndent=25,
        alignment=TA_JUSTIFY
    )
    
    # --- 1. FONDO (Opcional) ---
    if os.path.exists("fondo.png"):
        try: c.drawImage("fondo.png", 0, 0, width=w, height=h)
        except: pass

    # --- 2. ENCABEZADO ---
    c.setFont("Helvetica-Oblique", 8)
    # En Carta Compromiso a veces no va el encabezado gráfico si falta espacio, 
    # pero pondremos la frase si el tipo no es Compromiso, o si se desea.
    if tipo != "CARTA COMPROMISO PADRE DE FAMILIA":
        c.drawCentredString(w/2, config['y_frase'], f'"{config["frase"]}"')
    
    c.setFont("Helvetica", 11)
    c.drawRightString(w-60, config['y_frase']-20, obtener_fecha(config['anio']))

    # --- 3. TÍTULO DEL DOCUMENTO ---
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w/2, config['y_titulo'], tipo)
    c.setLineWidth(1)
    c.line(100, config['y_titulo']-5, w-100, config['y_titulo']-5)

    # Posición inicial del texto
    y = config['y_titulo'] - 50
    mx = 60            # Margen X izquierdo
    ancho = w - 120    # Ancho del bloque de texto

    # --- 4. CONTENIDO SEGÚN TIPO (CON NEGRITAS) ---
    
    if tipo == "CONSTANCIA DE VACANTE":
        y = dibujar_parrafo(c, "LA DIRECCIÓN DE LA INSTITUCIÓN EDUCATIVA PARTICULAR ALTERNATIVO YACHAY DE CHINCHERO, SUSCRIBE LA PRESENTE CONSTANCIA:", mx, y, ancho, estilo_normal)
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(mx, y, "HACE CONSTAR:")
        y -= 20
        
        txt_cuerpo = f"Que, existe vacante disponible en el NIVEL <b>{datos['grado'].upper()}</b> - Para el/la alumno(a) <b>{datos['alumno'].upper()}</b> CON DNI <b>{datos['dni']}</b>. Para el año escolar {config['anio']}."
        y = dibujar_parrafo(c, txt_cuerpo, mx, y, ancho, estilo_normal)
        
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
        for r in reqs:
            y = dibujar_parrafo(c, r, mx, y, ancho, estilo_lista)
        
        y -= 10
        c.setFont("Helvetica", 11)
        c.drawString(mx, y, "Se le expide el presente documento a solicitud de:")
        y -= 20
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(w/2, y, f"{datos['apoderado'].upper()} CON DNI {datos['dni_apo']}")

    elif tipo == "CONSTANCIA DE NO DEUDOR":
        y -= 10
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
        
        # Tabla manual
        tx = w/2 - 120
        c.setFont("Helvetica-Bold", 10)
        c.drawString(tx, y, "GRADO"); c.drawString(tx+100, y, "AÑO"); c.drawString(tx+200, y, "NOTA")
        y -= 5; c.line(tx-10, y, tx+250, y); y -= 20
        
        grados_txt = ["PRIMERO", "SEGUNDO", "TERCERO", "CUARTO", "QUINTO"]
        c.setFont("Helvetica", 10)
        hay_notas = False
        
        # Asumimos que datos['conducta'] es una lista de dicts
        for i in range(5):
            # Obtener datos de manera segura
            nota = ""
            if 'conducta' in datos and i < len(datos['conducta']):
                nota = datos['conducta'][i].get('nota', '')
            
            # Solo pintar si hay nota
            if nota:
                hay_notas = True
                c.drawString(tx, y, grados_txt[i])
                # Calculamos año aproximado restando
                anio_calc = int(config['anio']) - (5-i)
                c.drawString(tx+100, y, str(anio_calc))
                c.drawString(tx+200, y, nota)
                y -= 18
        
        if not hay_notas:
            c.drawString(tx, y, "-- No se registraron notas --"); y-=20

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
        # Usamos una fuente un poco más pequeña para que entren los 14 puntos
        estilo_comp = ParagraphStyle('Compromiso', parent=styles['Normal'], fontSize=9, leading=11, alignment=TA_JUSTIFY)
        
        intro = f"Por medio del presente Yo <b>{datos['apoderado'].upper()}</b> identificado con DNI N° <b>{datos['dni_apo']}</b>, padre o madre de familia de mi menor hijo(a), llamado(a) <b>{datos['alumno'].upper()}</b>."
        y = dibujar_parrafo(c, intro, mx, y, ancho, estilo_comp)
        
        consciente = "Consciente de las normas y disposiciones de la Dirección del Colegio y la importancia que tiene para la formación de los aprendizajes de mi hij@ en los valores de DISCIPLINA, respeto, puntualidad, responsabilidad y solidaridad. Me doy por enterado y me comprometo a contribuir como padre de familia a respetar y cumplir las siguientes disposiciones:"
        y = dibujar_parrafo(c, consciente, mx, y, ancho, estilo_comp)
        y -= 5

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
        
        # Imprimir puntos con un poco menos de espacio
        estilo_items = ParagraphStyle('ItemsComp', parent=styles['Normal'], fontSize=8.5, leading=10, leftIndent=10)
        for p in pts:
            y = dibujar_parrafo(c, p, mx, y, ancho, estilo_items)
            y += 5 # Corregir un poco el espaciado negativo del loop anterior

        y -= 10
        final = "Por su parte el Consejo Directivo del colegio seguirá mejorando el servicio educativo en base a: Disciplina, responsabilidad, seguridad de sus hijo@s... Confíe en su colegio y asegure la buena formación de su hij@. <i>La mejor herencia a los hijos es la educación.</i>"
        y = dibujar_parrafo(c, final, mx, y, ancho, estilo_comp)

        # FIRMAS DEL COMPROMISO
        y = 80
        c.setLineWidth(1)
        c.line(80,y,220,y); c.line(240,y,380,y); c.line(400,y,540,y); y-=10
        c.setFont("Helvetica",7)
        c.drawCentredString(150,y,"FIRMA PADRE/MADRE"); 
        c.drawCentredString(310,y,config['directora'].upper()); c.drawCentredString(310,y-10,"DIRECTORA"); 
        c.drawCentredString(470,y,config['promotor'].upper()); c.drawCentredString(470,y-10,"PROMOTOR")
        
        c.save(); buffer.seek(0); return buffer

    # --- 5. PIE DE PÁGINA (FIRMAS Y QR) PARA DOCUMENTOS NORMALES ---
    if tipo != "CARTA COMPROMISO PADRE DE FAMILIA":
        yf = 140
        c.line(200, yf, 395, yf)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(w/2, yf-15, config['directora'].upper())
        c.setFont("Helvetica", 9)
        c.drawCentredString(w/2, yf-28, "DIRECTORA")

        # QR Validación
        url_val = f"https://sistema-yachay2.streamlit.app/?validar={datos['dni']}"
        qr = qrcode.make(url_val)
        qr.save("temp_qr.png")
        c.drawImage("temp_qr.png", config['qr_x'], config['qr_y'], width=70, height=70)
        c.setFont("Helvetica", 6)
        c.drawCentredString(config['qr_x']+35, config['qr_y']-5, "ESCANEAR PARA VALIDAR")

    c.save()
    buffer.seek(0)
    return buffer

# --- 6. GENERADOR DE CARNET (IMAGEN PNG - DISEÑO GRÁFICO) ---
def generar_carnet_png(datos, anio, foto_bytes):
    # Dimensiones de alta calidad para imprimir
    W, H = 1012, 638 
    
    # Crear lienzo blanco
    img = Image.new('RGB', (W, H), 'white')
    draw = ImageDraw.Draw(img)

    # Colores
    AZUL_INST = (0, 30, 120)  # Azul oscuro
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    
    # --- A. MARCA DE AGUA (ESCUDO) ---
    # Buscamos si existe el archivo subido
    ruta_escudo = "escudo_upload.png" 
    if os.path.exists(ruta_escudo):
        try:
            escudo = Image.open(ruta_escudo).convert("RGBA")
            # Redimensionar para que quepa en el centro
            escudo = escudo.resize((350, 350))
            
            # Crear una imagen vacía del tamaño del carnet para componer
            capa_agua = Image.new('RGBA', (W, H), (0,0,0,0))
            
            # Pegar el escudo en el centro de la parte blanca (aprox)
            # Centro X = W/2, Centro Y = H/2. Ajustamos offset.
            offset_x = int((W - 350) / 2)
            offset_y = int((H - 350) / 2)
            capa_agua.paste(escudo, (offset_x, offset_y))
            
            # Ajustar transparencia (Alpha)
            # Obtenemos los datos de la imagen
            datos_img = capa_agua.getdata()
            nuevos_datos = []
            for item in datos_img:
                # item es (R, G, B, A). Si A > 0, lo bajamos a 40 (muy suave)
                if item[3] > 0:
                    nuevos_datos.append((item[0], item[1], item[2], 40))
                else:
                    nuevos_datos.append(item)
            capa_agua.putdata(nuevos_datos)
            
            # Pegar sobre el fondo blanco
            img.paste(capa_agua, (0,0), mask=capa_agua)
        except Exception as e:
            print(f"Error escudo: {e}")

    # --- B. CABECERA Y PIE ---
    draw.rectangle([(0, 0), (W, 130)], fill=AZUL_INST)     # Cabecera
    draw.rectangle([(0, H-60), (W, H)], fill=AZUL_INST)    # Pie

    # Fuentes (Intentar cargar fuentes del sistema o usar default)
    try:
        font_header = ImageFont.truetype("arialbd.ttf", 60) # Arial Bold
        font_data_bold = ImageFont.truetype("arialbd.ttf", 35)
        font_data = ImageFont.truetype("arial.ttf", 35)
        font_motto = ImageFont.truetype("arialbd.ttf", 30)
    except:
        # Fallback si no hay arial (linux/cloud)
        font_header = ImageFont.load_default()
        font_data_bold = ImageFont.load_default()
        font_data = ImageFont.load_default()
        font_motto = ImageFont.load_default()

    # Textos Institucionales
    draw.text((W/2, 65), "I.E. ALTERNATIVO YACHAY", font=font_header, fill=BLANCO, anchor="mm")
    draw.text((W/2, H-30), "EDUCAR PARA LA VIDA", font=font_motto, fill=BLANCO, anchor="mm")

    # --- C. FOTO DEL ALUMNO ---
    x_foto, y_foto = 50, 160
    w_foto, h_foto = 280, 350
    
    foto_pegada = False
    if foto_bytes:
        try:
            foto_img = Image.open(foto_bytes).convert("RGB")
            foto_img = foto_img.resize((w_foto, h_foto))
            img.paste(foto_img, (x_foto, y_foto))
            foto_pegada = True
        except: pass
    
    # Marco de la foto
    draw.rectangle([(x_foto, y_foto), (x_foto+w_foto, y_foto+h_foto)], outline=NEGRO, width=4)
    if not foto_pegada:
        draw.text((x_foto+70, y_foto+160), "SIN FOTO", fill=colors.grey, font=font_data)

    # --- D. DATOS DEL ALUMNO ---
    x_text = 360
    y_cursor = 170
    
    # Nombre (Lógica de auto-ajuste de tamaño)
    nombre = datos['alumno'].upper()
    size_nombre = 55
    if len(nombre) > 20: size_nombre = 45
    if len(nombre) > 30: size_nombre = 35
    
    try: font_nombre = ImageFont.truetype("arialbd.ttf", size_nombre)
    except: font_nombre = ImageFont.load_default()
    
    draw.text((x_text, y_cursor), nombre, font=font_nombre, fill=NEGRO)
    y_cursor += 80

    # DNI
    draw.text((x_text, y_cursor), f"DNI: {datos['dni']}", font=font_data, fill=NEGRO)
    y_cursor += 60
    
    # Grado (Auto-ajuste)
    grado_txt = f"GRADO: {datos['grado'].upper()}"
    size_grado = 35
    if len(grado_txt) > 25: size_grado = 28
    try: font_grado = ImageFont.truetype("arial.ttf", size_grado)
    except: font_grado = font_data
    draw.text((x_text, y_cursor), grado_txt, font=font_grado, fill=NEGRO)
    y_cursor += 60
    
    # Vigencia
    draw.text((x_text, y_cursor), f"VIGENCIA: {anio}", font=font_data, fill=NEGRO)

    # --- E. CÓDIGO DE BARRAS (DNI) ---
    if HAS_BARCODE:
        try:
            writer = ImageWriter()
            buffer_bar = io.BytesIO()
            # Crear código Code128 con el DNI
            Code128(datos['dni'], writer=writer).write(buffer_bar)
            buffer_bar.seek(0)
            
            img_bar = Image.open(buffer_bar)
            # Redimensionar (Ancho, Alto)
            img_bar = img_bar.resize((450, 100))
            
            # Pegar abajo a la derecha de la foto
            img.paste(img_bar, (x_text, H - 200))
        except Exception as e:
            draw.text((x_text, H-180), f"|| {datos['dni']} ||", fill=NEGRO, font=font_data)
    else:
        # Fallback si no hay librería
        draw.text((x_text, H-180), f"* {datos['dni']} *", fill=NEGRO, font=font_data)

    # --- F. CÓDIGO QR (VALIDACIÓN) ---
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(f"https://sistema-yachay2.streamlit.app/?validar={datos['dni']}")
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")
    img_qr = img_qr.resize((170, 170))
    
    # Pegar QR a la derecha
    x_qr = W - 200
    y_qr = 180
    img.paste(img_qr, (x_qr, y_qr))
    
    # Texto "Escanear"
    try: font_small = ImageFont.truetype("arial.ttf", 20)
    except: font_small = ImageFont.load_default()
    draw.text((x_qr + 35, y_qr + 175), "ESCANEAR", font=font_small, fill=NEGRO)

    # Guardar en memoria
    output = io.BytesIO()
    img.save(output, format='PNG', quality=100)
    output.seek(0)
    return output

# --- INTERFAZ PRINCIPAL ---
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # --- UPLOADERS (Guardado Inmediato) ---
    st.subheader("1. Base de Datos")
    up_bd = st.file_uploader("Subir Excel", type=["xlsx"], key="up_bd")
    if up_bd:
        with open("base_datos.xlsx", "wb") as f: f.write(up_bd.getbuffer())
        st.success("✅ BD Actualizada")

    st.subheader("2. Escudo del Colegio")
    st.info("Sube el escudo en PNG transparente.")
    up_escudo = st.file_uploader("Subir Escudo", type=["png"], key="up_escudo")
    
    # Lógica de guardado del escudo
    if up_escudo:
        with open("escudo_upload.png", "wb") as f:
            f.write(up_escudo.getbuffer())
        st.success("✅ Escudo Guardado")
        st.image(up_escudo, width=100, caption="Previsualización")
    elif os.path.exists("escudo_upload.png"):
        st.write("✅ Escudo cargado en memoria")
        st.image("escudo_upload.png", width=100)

    st.markdown("---")
    anio_sel = st.number_input("Año Escolar:", 2024, 2030, 2026)
    
    # Ajustes finos de PDF
    with st.expander("🛠️ Ajustar Posiciones PDF"):
        y_frase = st.slider("Altura Frase", 600, 800, 700)
        y_titulo = st.slider("Altura Título", 500, 750, 631)
        qr_x = st.slider("QR X", 0, 500, 435)
        qr_y = st.slider("QR Y", 0, 200, 47)
    
    frase = st.text_area("Frase del Año:", "AÑO DE LA ESPERANZA Y EL FORTALECIMIENTO DE LA DEMOCRACIA")
    directora = st.text_input("Nombre Directora:", "Prof. Ana María CUSI INCA")
    promotor = st.text_input("Nombre Promotor:", "Prof. Leandro CORDOVA TOCRE")
    
    if st.button("🔴 CERRAR SESIÓN"):
        st.session_state.autenticado = False
        st.rerun()

# --- PESTAÑAS DEL SISTEMA ---
tab1, tab2, tab3 = st.tabs(["📄 DOCUMENTOS (PDF)", "🪪 CARNETS (IMAGEN)", "📊 REGISTROS"])

# === PESTAÑA 1: DOCUMENTOS ===
with tab1:
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.markdown("### 1. Seleccionar Tipo")
        tipo_doc = st.radio("Documento a generar:", [
            "CONSTANCIA DE VACANTE", 
            "CONSTANCIA DE NO DEUDOR", 
            "CONSTANCIA DE ESTUDIOS", 
            "CONSTANCIA DE CONDUCTA", 
            "CONSTANCIA DE TRABAJO", 
            "CARTA COMPROMISO PADRE DE FAMILIA"
        ])
        
        st.markdown("---")
        st.markdown("### 2. Buscar Alumno")
        dni_search = st.text_input("🔍 DNI a buscar:", placeholder="Ingrese DNI")
        if st.button("Buscar en BD", key="btn_search_doc"):
            res = buscar_alumno(dni_search)
            if res is not None:
                st.session_state.alumno = res['Alumno']
                st.session_state.dni = res['DNI']
                st.session_state.grado = res['Grado']
                st.session_state.apoderado = res['Apoderado']
                st.session_state.dni_apo = res['DNI_Apoderado']
                st.success("Datos cargados")
            else:
                st.error("No encontrado")

    with col_b:
        st.markdown("### 3. Verificar y Editar Datos")
        c_1, c_2 = st.columns(2)
        with c_1:
            nom = st.text_input("Nombre Completo:", key="alumno")
            doc_id = st.text_input("DNI:", key="dni")
            grad = st.text_input("Grado/Nivel:", key="grado")
        with c_2:
            if tipo_doc != "CONSTANCIA DE TRABAJO":
                apo = st.text_input("Apoderado:", key="apoderado")
                dni_apo = st.text_input("DNI Apoderado:", key="dni_apo")
            else:
                apo, dni_apo = "", ""
                st.info("Docentes no requieren apoderado.")

        # Tabla de Conducta solo si es necesario
        cond_list = []
        if tipo_doc == "CONSTANCIA DE CONDUCTA":
            st.info("Ingrese notas de conducta:")
            cols_c = st.columns(5)
            for i in range(5):
                with cols_c[i]:
                    val = st.text_input(f"Nota {i+1}°", key=f"cn{i}")
                    cond_list.append({'nota': val})
        
        st.markdown("---")
        if st.button("🖨️ GENERAR DOCUMENTO PDF", type="primary", use_container_width=True):
            if nom and doc_id:
                # Empaquetar datos
                pack_datos = {
                    'alumno': nom, 'dni': doc_id, 'grado': grad, 
                    'apoderado': apo, 'dni_apo': dni_apo, 'conducta': cond_list
                }
                pack_cfg = {
                    'anio': anio_sel, 'frase': frase, 'y_frase': y_frase, 
                    'y_titulo': y_titulo, 'qr_x': qr_x, 'qr_y': qr_y, 
                    'directora': directora, 'promotor': promotor
                }
                
                pdf_bytes = generar_pdf_doc(tipo_doc, pack_datos, pack_cfg)
                st.download_button(
                    label="⬇️ DESCARGAR PDF FINAL", 
                    data=pdf_bytes, 
                    file_name=f"{tipo_doc}_{doc_id}.pdf", 
                    mime="application/pdf"
                )
            else:
                st.warning("Faltan datos obligatorios (Nombre, DNI)")

# === PESTAÑA 2: CARNETS ===
with tab2:
    st.markdown("## 🎓 Generador de Carnet (Alta Resolución)")
    st.info("Este módulo genera una IMAGEN (PNG) lista para imprimir o enviar por WhatsApp.")
    
    cc_1, cc_2 = st.columns(2)
    
    with cc_1:
        st.markdown("### Datos del Carnet")
        # Usamos los datos de session_state o vacíos
        cn_nom = st.text_input("Estudiante:", value=st.session_state.get('alumno', ''), key="c_nom")
        cn_dni = st.text_input("DNI:", value=st.session_state.get('dni', ''), key="c_dni")
        cn_gra = st.text_input("Grado:", value=st.session_state.get('grado', ''), key="c_gra")
        
        st.markdown("### Foto Digital")
        cn_foto = st.file_uploader("Subir Foto (JPG/PNG)", type=['jpg','png','jpeg'], key="c_foto")

    with cc_2:
        st.markdown("### Vista Previa")
        
        if st.button("🎨 CREAR CARNET", type="primary"):
            if cn_nom and cn_dni:
                # Llamar a la función generadora de PNG
                datos_carnet = {'alumno': cn_nom, 'dni': cn_dni, 'grado': cn_gra}
                
                # Generar imagen
                img_result = generar_carnet_png(datos_carnet, anio_sel, cn_foto)
                
                # Mostrar
                st.image(img_result, caption="Carnet Generado", use_container_width=True)
                
                # Botón descarga
                st.download_button(
                    label="⬇️ DESCARGAR IMAGEN (PNG)",
                    data=img_result,
                    file_name=f"Carnet_{cn_dni}.png",
                    mime="image/png"
                )
            else:
                st.error("Falta Nombre o DNI")

# === PESTAÑA 3: BD ===
with tab3:
    st.markdown("### Base de Datos Actual")
    df = cargar_bd()
    if df is not None:
        st.write(f"Total registros: {len(df)}")
        st.dataframe(df)
    else:
        st.warning("No se ha cargado ningún archivo Excel en la barra lateral.")

if st.sidebar.button("🧹 LIMPIAR TODO"):
    limpiar_datos()
    st.rerun()
