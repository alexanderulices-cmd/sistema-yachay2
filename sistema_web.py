import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY
import qrcode
import os
from datetime import datetime
import io
from PIL import Image, ImageDraw, ImageFont
import requests
import textwrap
import zipfile
import time
from pathlib import Path

# ========================================
# CONFIGURACIÓN INICIAL
# ========================================

st.set_page_config(
    page_title="SISTEMA YACHAY PRO",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estados de sesión
def init_session_state():
    defaults = {
        'rol': None,
        'cola_carnets': [],
        'alumno': '',
        'dni': '',
        'grado': '',
        'apoderado': '',
        'dni_apo': '',
        'c_temp_nom': '',
        'c_temp_dni': '',
        'c_temp_gra': ''
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Estilos CSS
st.markdown("""
<style>
    .main-header {
        text-align: center; padding: 2rem; background: linear-gradient(135deg, #001e7c 0%, #0052cc 100%);
        color: white; border-radius: 10px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #0d47a1; color: white; border-radius: 8px; font-weight: bold; border: none;
        height: 50px; font-size: 16px; transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #1565c0; transform: translateY(-2px); }
</style>
""", unsafe_allow_html=True)

# Importación segura de código de barras
try:
    from barcode import Code128
    from barcode.writer import ImageWriter
    HAS_BARCODE = True
except ImportError:
    HAS_BARCODE = False

# ========================================
# GESTIÓN DE RECURSOS (FUENTES)
# ========================================

class RecursoManager:
    FUENTES = {
        "Roboto-Bold.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Bold.ttf",
        "Roboto-Regular.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf"
    }
    
    @staticmethod
    def descargar_fuentes():
        for nombre, url in RecursoManager.FUENTES.items():
            if not Path(nombre).exists():
                try:
                    r = requests.get(url, timeout=5)
                    with open(nombre, 'wb') as f: f.write(r.content)
                except: pass
    
    @staticmethod
    def obtener_fuente(nombre, tamaño, bold=False):
        try:
            archivo = "Roboto-Bold.ttf" if bold else "Roboto-Regular.ttf"
            return ImageFont.truetype(archivo, int(tamaño))
        except: return ImageFont.load_default()

RecursoManager.descargar_fuentes()

# ========================================
# BASE DE DATOS
# ========================================

class BaseDatos:
    ARCHIVO = "base_datos.xlsx"
    
    @staticmethod
    def cargar():
        try:
            if Path(BaseDatos.ARCHIVO).exists():
                return pd.read_excel(BaseDatos.ARCHIVO, dtype=str, engine='openpyxl')
            return None
        except: return None
    
    @staticmethod
    def buscar_por_dni(dni):
        df = BaseDatos.cargar()
        if df is not None and 'DNI' in df.columns:
            dni = str(dni).strip()
            df['DNI'] = df['DNI'].astype(str).str.strip()
            res = df[df['DNI'] == dni]
            if not res.empty: return res.iloc[0].to_dict()
        return None

# ========================================
# GENERADOR DE PDFs (DOCUMENTOS)
# ========================================

class GeneradorPDF:
    def __init__(self, config):
        self.config = config
        self.buffer = io.BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        
    def _dibujar_parrafo(self, texto, x, y, ancho, estilo):
        p = Paragraph(texto, estilo)
        w, h = p.wrap(ancho, 600)
        p.drawOn(self.canvas, x, y - h)
        return y - h - 15

    def generar_doc(self, tipo, datos):
        c = self.canvas
        w, h = self.width, self.height
        
        # Fondo
        if Path("fondo.png").exists():
            try: c.drawImage("fondo.png", 0, 0, width=w, height=h)
            except: pass

        # Encabezado
        c.setFont("Helvetica-Oblique", 8)
        if tipo != "CARTA COMPROMISO PADRE DE FAMILIA":
            c.drawCentredString(w/2, self.config['y_frase'], f'"{self.config["frase"]}"')
        
        c.setFont("Helvetica", 11)
        c.drawRightString(w-60, self.config['y_frase']-25, f"Chinchero, {datetime.now().strftime('%d/%m/%Y')}")

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(w/2, self.config['y_titulo'], tipo)
        c.line(100, self.config['y_titulo']-5, w-100, self.config['y_titulo']-5)

        y = self.config['y_titulo'] - 50
        mx, ancho = 60, w - 120
        estilo = ParagraphStyle('N', parent=self.styles['Normal'], fontSize=11, leading=15, alignment=TA_JUSTIFY)
        estilo_l = ParagraphStyle('L', parent=estilo, leftIndent=25)

        # Lógica por tipo
        if tipo == "CONSTANCIA DE VACANTE":
            y = self._dibujar_parrafo("LA DIRECCIÓN DE LA I.E. ALTERNATIVO YACHAY HACE CONSTAR:", mx, y, ancho, estilo)
            txt = f"Que existe vacante para el alumno <b>{datos['alumno']}</b> con DNI <b>{datos['dni']}</b> en el grado <b>{datos['grado']}</b> para el año {self.config['anio']}."
            y = self._dibujar_parrafo(txt, mx, y, ancho, estilo)
            y = self._dibujar_parrafo("Requisitos:", mx, y, ancho, estilo)
            for r in ["• Certificado de Estudios", "• DNI Copia", "• Ficha SIAGIE"]:
                y = self._dibujar_parrafo(r, mx, y, ancho, estilo_l)
                
        elif tipo == "CONSTANCIA DE NO DEUDOR":
            y = self._dibujar_parrafo("LA DIRECCIÓN HACE CONSTAR:", mx, y, ancho, estilo)
            txt = f"Que el alumno <b>{datos['alumno']}</b> con DNI <b>{datos['dni']}</b>, NO ADEUDA pensiones ni matrícula."
            y = self._dibujar_parrafo(txt, mx, y, ancho, estilo)

        elif tipo == "CONSTANCIA DE ESTUDIOS":
            y = self._dibujar_parrafo("LA DIRECCIÓN HACE CONSTAR:", mx, y, ancho, estilo)
            txt = f"Que <b>{datos['alumno']}</b> con DNI <b>{datos['dni']}</b> se encuentra matriculado en el grado <b>{datos['grado']}</b> en el año {self.config['anio']}."
            y = self._dibujar_parrafo(txt, mx, y, ancho, estilo)

        elif tipo == "CONSTANCIA DE CONDUCTA":
            txt = f"Que <b>{datos['alumno']}</b> con DNI <b>{datos['dni']}</b> cursó estudios obteniendo las siguientes notas de conducta:"
            y = self._dibujar_parrafo(txt, mx, y, ancho, estilo)
            y -= 20
            c.drawString(mx, y, "GRADO"); c.drawString(mx+200, y, "NOTA")
            y -= 20; c.drawString(mx, y, datos['grado']); c.drawString(mx+200, y, datos.get('nota_conducta','A'))
            
        elif tipo == "CARTA COMPROMISO PADRE DE FAMILIA":
            estilo_s = ParagraphStyle('S', parent=estilo, fontSize=9, leading=11)
            intro = f"Yo, <b>{datos['apoderado']}</b> con DNI <b>{datos['dni_apo']}</b>, padre de <b>{datos['alumno']}</b>, me comprometo a cumplir las normas de la I.E."
            y = self._dibujar_parrafo(intro, mx, y, ancho, estilo_s)
            pts = ["1. Asistencia puntual.", "2. Cumplimiento de tareas.", "3. Uso del uniforme.", "4. Respeto a normas.", "5. Pago puntual de pensiones."]
            for p in pts: y = self._dibujar_parrafo(p, mx, y, ancho, estilo_s)
            
            # Firmas Carta
            y = 100
            c.line(80,y,200,y); c.drawCentredString(140,y-10,"PADRE/MADRE")
            c.line(220,y,340,y); c.drawCentredString(280,y-10,"DIRECTORA")
            c.line(360,y,480,y); c.drawCentredString(420,y-10,"PROMOTOR")
            c.save(); self.buffer.seek(0); return self.buffer

        # Firmas y QR para otros docs
        if tipo != "CARTA COMPROMISO PADRE DE FAMILIA":
            yf = 110
            c.line(200, yf, 395, yf)
            c.drawCentredString(w/2, yf-15, self.config['directora'])
            c.setFont("Helvetica", 9); c.drawCentredString(w/2, yf-28, "DIRECTORA")
            
            # QR Doc
            qr = qrcode.QRCode(box_size=10, border=1)
            qr.add_data(f"{tipo}|{datos['dni']}")
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("temp_qr_doc.png")
            c.drawImage("temp_qr_doc.png", self.config['qr_x'], self.config['qr_y'], 70, 70)

        c.save()
        self.buffer.seek(0)
        return self.buffer

# ========================================
# GENERADOR DE CARNETS (CORREGIDO Y AJUSTADO)
# ========================================

class GeneradorCarnet:
    WIDTH = 1012
    HEIGHT = 638
    AZUL_INST = (0, 30, 120)
    
    def __init__(self, datos, anio, foto_bytes=None):
        self.datos = datos
        self.anio = anio
        self.foto_bytes = foto_bytes
        self.img = Image.new('RGB', (self.WIDTH, self.HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.img)

    def generar(self):
        W, H = self.WIDTH, self.HEIGHT
        
        # 1. Escudo Fondo
        if Path("escudo_upload.png").exists():
            try:
                escudo = Image.open("escudo_upload.png").convert("RGBA").resize((400, 400))
                capa = Image.new('RGBA', (W, H), (0,0,0,0))
                capa.paste(escudo, (int((W-400)/2), int((H-400)/2)))
                new_data = [(d[0], d[1], d[2], 30) if d[3]>0 else d for d in capa.getdata()]
                capa.putdata(new_data)
                self.img.paste(capa, (0,0), mask=capa)
            except: pass

        # 2. Barras Azules (ALTAS para textos gigantes)
        self.draw.rectangle([(0, 0), (W, 160)], fill=self.AZUL_INST)
        self.draw.rectangle([(0, H-140), (W, H)], fill=self.AZUL_INST)

        # 3. Textos GIGANTES (Ajustados)
        f_head = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 110, True) # Tamaño 110
        f_pie = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 90, True)   # Tamaño 90
        
        self.draw.text((W/2, 80), "I.E. ALTERNATIVO YACHAY", font=f_head, fill="white", anchor="mm")
        self.draw.text((W/2, H-70), "EDUCAR PARA LA VIDA", font=f_pie, fill="white", anchor="mm")

        # 4. Foto
        x_foto, y_foto = 50, 190
        w_foto, h_foto = 290, 350
        if self.foto_bytes:
            try:
                foto = Image.open(self.foto_bytes).convert("RGB").resize((w_foto, h_foto))
                self.img.paste(foto, (x_foto, y_foto))
            except: self.draw.rectangle([(x_foto,y_foto),(x_foto+w_foto,y_foto+h_foto)], fill="#eee")
        else: self.draw.rectangle([(x_foto,y_foto),(x_foto+w_foto,y_foto+h_foto)], fill="#eee")
        self.draw.rectangle([(x_foto,y_foto),(x_foto+w_foto,y_foto+h_foto)], outline="black", width=6)

        # 5. Datos
        x_txt = 370
        nom = self.datos['alumno'].upper()
        
        # Nombre (Grande)
        if len(nom) > 22:
            f_nom = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 55, True)
            lines = textwrap.wrap(nom, 25)
            y = 190
            for l in lines[:2]:
                self.draw.text((x_txt, y), l, font=f_nom, fill="black")
                y += 60
        else:
            f_nom = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 75, True)
            self.draw.text((x_txt, 200), nom, font=f_nom, fill="black")

        # Etiquetas y Valores
        f_lbl = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 55, True)
        f_val = RecursoManager.obtener_fuente("Roboto-Regular.ttf", 55)
        
        self.draw.text((x_txt, 340), "DNI:", font=f_lbl, fill="black")
        self.draw.text((x_txt+130, 340), self.datos['dni'], font=f_val, fill="black")
        
        self.draw.text((x_txt, 420), "GRADO:", font=f_lbl, fill="black")
        self.draw.text((x_txt+210, 420), self.datos['grado'].upper(), font=f_val, fill="black")
        
        self.draw.text((x_txt, 500), "VIGENCIA:", font=f_lbl, fill="black")
        self.draw.text((x_txt+280, 500), str(self.anio), font=f_val, fill="black")

        # 6. CÓDIGO DE BARRAS (SOLO DNI - MÁS GRANDE)
        if HAS_BARCODE:
            try:
                writer = ImageWriter()
                buf = io.BytesIO()
                # SOLO DNI EN EL CODIGO
                Code128(self.datos['dni'], writer=writer).write(buf, options={'write_text':False})
                buf.seek(0)
                # Redimensionar a 600x130 (Mas grande)
                img_bar = Image.open(buf).resize((600, 130), Image.LANCZOS)
                self.img.paste(img_bar, (360, H - 260))
            except: pass

        # 7. QR (SOLO DNI - MÁS GRANDE)
        try:
            qr = qrcode.QRCode(box_size=10, border=1)
            # SOLO DNI EN EL QR
            qr.add_data(self.datos['dni']) 
            qr.make(fit=True)
            img_qr_pil = qr.make_image(fill_color="black", back_color="white")
            # Redimensionar a 260x260 (Mas grande)
            img_qr = img_qr_pil.resize((260, 260), Image.LANCZOS)
            self.img.paste(img_qr, (W - 280, 190))
            
            f_esc = RecursoManager.obtener_fuente("Roboto-Regular.ttf", 25)
            self.draw.text((W - 150, 460), "ESCANEAR", font=f_esc, fill="black", anchor="mm")
        except: pass

        out = io.BytesIO()
        self.img.save(out, format='PNG')
        out.seek(0)
        return out

# ========================================
# LÓGICA DE INTERFAZ Y PESTAÑAS
# ========================================

# Login
if st.session_state.rol is None:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<div class='main-header'><h1>SISTEMA YACHAY</h1></div>", unsafe_allow_html=True)
        if Path("escudo_upload.png").exists():
            st.image("escudo_upload.png", width=150)
            st.markdown("""<style>div[data-testid="stImage"]{display:block;margin-left:auto;margin-right:auto;width:50%;}</style>""", unsafe_allow_html=True)
        
        pwd = st.text_input("Contraseña:", type="password")
        c_a, c_b = st.columns(2)
        if c_a.button("ADMIN"):
            if pwd == "306020": st.session_state.rol = "admin"; st.rerun()
            else: st.error("Error")
        if c_b.button("DOCENTE"):
            if pwd == "deyanira": st.session_state.rol = "docente"; st.rerun()
            else: st.error("Error")
    st.stop()

# Sidebar
with st.sidebar:
    st.title("YACHAY PRO")
    if st.session_state.rol == "admin":
        st.markdown("### Configuración")
        up_bd = st.file_uploader("Base Datos (Excel)", ["xlsx"])
        if up_bd:
            with open("base_datos.xlsx", "wb") as f: f.write(up_bd.getbuffer())
            st.success("BD Actualizada")
        
        up_esc = st.file_uploader("Escudo (PNG)", ["png"])
        if up_esc:
            with open("escudo_upload.png", "wb") as f: f.write(up_esc.getbuffer())
            st.success("Escudo Actualizado")
            
        dir_name = st.text_input("Directora", "Prof. Ana María CUSI INCA")
        pro_name = st.text_input("Promotor", "Prof. Leandro CORDOVA TOCRE")
        frase = st.text_input("Frase", "AÑO DE LA INTEGRACIÓN")
    else:
        dir_name = "Prof. Ana María CUSI INCA"
        pro_name = "Prof. Leandro CORDOVA TOCRE"
        frase = "AÑO DE LA INTEGRACIÓN"
    
    anio_sel = st.number_input("Año", 2024, 2030, 2026)
    if st.button("Cerrar Sesión"):
        st.session_state.rol = None
        st.rerun()

# Tabs Principales
tab1, tab2, tab3 = st.tabs(["📄 DOCUMENTOS", "🪪 CARNETS", "📊 BASE DATOS"])

with tab1:
    st.header("Generar Documentos")
    c1, c2 = st.columns([1,2])
    with c1:
        tipo = st.selectbox("Tipo", ["CONSTANCIA DE VACANTE", "CONSTANCIA DE NO DEUDOR", "CONSTANCIA DE ESTUDIOS", "CONSTANCIA DE CONDUCTA", "CARTA COMPROMISO PADRE DE FAMILIA"])
        sdni = st.text_input("Buscar DNI Doc:")
        if st.button("Buscar"):
            r = BaseDatos.buscar_por_dni(sdni)
            if r:
                st.session_state.alumno = r['Alumno']
                st.session_state.dni = r['DNI']
                st.session_state.grado = r['Grado']
                st.session_state.apoderado = r.get('Apoderado','')
                st.session_state.dni_apo = r.get('DNI_Apoderado','')
                st.success("Encontrado")
    with c2:
        with st.container(border=True):
            n = st.text_input("Alumno", key="alumno")
            d = st.text_input("DNI", key="dni")
            g = st.text_input("Grado", key="grado")
            a = st.text_input("Apoderado", key="apoderado")
            da = st.text_input("DNI Apoderado", key="dni_apo")
            nc = st.text_input("Nota Conducta (Opcional)")
            
            if st.button("GENERAR PDF", type="primary", use_container_width=True):
                if n and d:
                    dat = {'alumno':n, 'dni':d, 'grado':g, 'apoderado':a, 'dni_apo':da, 'nota_conducta':nc}
                    conf = {'anio':anio_sel, 'frase':frase, 'directora':dir_name, 'y_frase':700, 'y_titulo':630, 'qr_x':435, 'qr_y':47}
                    gen = GeneradorPDF(conf)
                    pdf = gen.generar_doc(tipo, dat)
                    st.download_button("DESCARGAR PDF", pdf, f"{tipo}.pdf", "application/pdf", use_container_width=True)

with tab2:
    st.header("Centro de Carnetización")
    col_u, col_c = st.columns(2)
    
    # 1. INDIVIDUAL
    with col_u:
        st.subheader("⚡ Individual (Rápido)")
        in_n = st.text_input("Nombre:", key="in_n")
        in_d = st.text_input("DNI:", key="in_d")
        in_g = st.text_input("Grado:", key="in_g")
        in_f = st.file_uploader("Foto", type=['jpg','png'], key="in_f")
        
        if st.button("VER Y DESCARGAR", type="primary", use_container_width=True):
            if in_n and in_d:
                fb = in_f.getvalue() if in_f else None
                gen = GeneradorCarnet({'alumno':in_n, 'dni':in_d, 'grado':in_g}, anio_sel, fb)
                img = gen.generar()
                st.image(img, caption="Vista Previa")
                st.download_button("DESCARGAR PNG", img, f"Carnet_{in_d}.png", "image/png", use_container_width=True)

    # 2. CARRITO
    with col_c:
        st.subheader("🛒 Carrito (Lote)")
        sdni_c = st.text_input("Buscar DNI para Carrito:")
        if st.button("Buscar para Carrito"):
            r = BaseDatos.buscar_por_dni(sdni_c)
            if r:
                st.session_state.c_temp_nom = r['Alumno']
                st.session_state.c_temp_dni = r['DNI']
                st.session_state.c_temp_gra = r['Grado']
        
        cn = st.text_input("Nombre Carrito", key="c_temp_nom")
        cd = st.text_input("DNI Carrito", key="c_temp_dni")
        cg = st.text_input("Grado Carrito", key="c_temp_gra")
        cf = st.file_uploader("Foto Carrito", key="c_temp_foto")
        
        if st.button("➕ AGREGAR"):
            if cn and cd:
                fb = cf.getvalue() if cf else None
                st.session_state.cola_carnets.append({'alumno':cn, 'dni':cd, 'grado':cg, 'foto_bytes':fb})
                st.success("Agregado")
                st.session_state.c_temp_nom = ""
                st.session_state.c_temp_dni = ""
                st.session_state.c_temp_gra = ""
                st.rerun()

        st.markdown("---")
        st.write(f"En cola: {len(st.session_state.cola_carnets)}")
        if len(st.session_state.cola_carnets) > 0:
            st.dataframe(pd.DataFrame(st.session_state.cola_carnets)[['alumno','dni']], hide_index=True)
            if st.button("DESCARGAR ZIP TODOS", type="primary"):
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, "w") as zf:
                    for i in st.session_state.cola_carnets:
                        fb = io.BytesIO(i['foto_bytes']) if i['foto_bytes'] else None
                        gen = GeneradorCarnet(i, anio_sel, fb)
                        img = gen.generar()
                        zf.writestr(f"Carnet_{i['dni']}.png", img.getvalue())
                buf.seek(0)
                st.download_button("BAJAR ZIP", buf, "Carnets.zip", "application/zip", use_container_width=True)
            
            if st.button("Vaciar"):
                st.session_state.cola_carnets = []
                st.rerun()

with tab3:
    st.header("Base de Datos")
    df = BaseDatos.cargar()
    if df is not None: st.dataframe(df, use_container_width=True)
    else: st.info("Sube un Excel en el menú lateral (Admin)")
