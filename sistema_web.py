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
    """Inicializa todos los estados de sesión necesarios"""
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
        'c_temp_gra': '',
        'busqueda_counter': 0,
        'agregar_counter': 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Estilos CSS mejorados
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #001e7c 0%, #0052cc 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-box {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #0052cc;
        margin: 1rem 0;
    }
    .success-msg {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .error-msg {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    .separator {
        height: 2px;
        background: linear-gradient(to right, transparent, #0052cc, transparent);
        margin: 2rem 0;
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

# ========================================
# GESTIÓN DE ARCHIVOS Y RECURSOS
# ========================================

class RecursoManager:
    """Gestiona la descarga y carga de recursos externos"""
    
    FUENTES = {
        "Roboto-Bold.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Bold.ttf",
        "Roboto-Regular.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf"
    }
    
    @staticmethod
    def descargar_fuentes():
        """Descarga fuentes si no existen"""
        for nombre, url in RecursoManager.FUENTES.items():
            if not Path(nombre).exists():
                try:
                    r = requests.get(url, timeout=10)
                    r.raise_for_status()
                    with open(nombre, 'wb') as f:
                        f.write(r.content)
                except Exception:
                    pass
    
    @staticmethod
    def obtener_fuente(nombre, tamaño, bold=False):
        """Obtiene una fuente con fallback seguro"""
        try:
            archivo = "Roboto-Bold.ttf" if bold else "Roboto-Regular.ttf"
            return ImageFont.truetype(archivo, int(tamaño))
        except Exception:
            return ImageFont.load_default()

RecursoManager.descargar_fuentes()

# ========================================
# BASE DE DATOS
# ========================================

class BaseDatos:
    """Gestiona todas las operaciones con la base de datos"""
    
    ARCHIVO = "base_datos.xlsx"
    
    @staticmethod
    @st.cache_data(ttl=300)
    def cargar():
        """Carga la base de datos desde Excel"""
        try:
            if Path(BaseDatos.ARCHIVO).exists():
                df = pd.read_excel(BaseDatos.ARCHIVO, dtype=str, engine='openpyxl')
                df.columns = df.columns.str.strip().str.title()
                return df
            return None
        except Exception as e:
            st.error(f"Error al cargar BD: {e}")
            return None
    
    @staticmethod
    def buscar_por_dni(dni):
        """Busca un alumno por DNI"""
        df = BaseDatos.cargar()
        if df is not None and 'Dni' in df.columns:
            dni = str(dni).strip()
            df['Dni'] = df['Dni'].astype(str).str.strip()
            resultado = df[df['Dni'] == dni]
            if not resultado.empty:
                return resultado.iloc[0].to_dict()
        return None
    
    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas de la base de datos"""
        df = BaseDatos.cargar()
        if df is not None:
            return {
                'total_alumnos': len(df),
                'grados': df['Grado'].nunique() if 'Grado' in df.columns else 0,
                'con_apoderado': df['Apoderado'].notna().sum() if 'Apoderado' in df.columns else 0
            }
        return {'total_alumnos': 0, 'grados': 0, 'con_apoderado': 0}

# ========================================
# GENERADOR DE PDFs CORREGIDO
# ========================================

class GeneradorPDF:
    """Genera documentos PDF profesionales"""
    
    def __init__(self, config):
        self.config = config
        self.buffer = io.BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        
    def _aplicar_fondo(self):
        """Aplica imagen de fondo si existe"""
        if Path("fondo.png").exists():
            try:
                self.canvas.drawImage("fondo.png", 0, 0, 
                                    width=self.width, height=self.height)
            except Exception:
                pass
    
    def _dibujar_encabezado(self, titulo):
        """Dibuja el encabezado del documento"""
        self.canvas.setFont("Helvetica-Oblique", 8)
        self.canvas.drawCentredString(
            self.width/2, 
            self.config['y_frase'], 
            f'"{self.config["frase"]}"'
        )
        
        self.canvas.setFont("Helvetica", 11)
        fecha = self._obtener_fecha()
        self.canvas.drawRightString(self.width - 60, self.config['y_frase'] - 25, fecha)
        
        self.canvas.setFont("Helvetica-Bold", 16)
        self.canvas.drawCentredString(self.width/2, self.config['y_titulo'], titulo)
        
        self.canvas.setLineWidth(1)
        self.canvas.line(100, self.config['y_titulo'] - 5, 
                        self.width - 100, self.config['y_titulo'] - 5)
    
    def _obtener_fecha(self):
        """Genera la fecha formateada"""
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        hoy = datetime.now()
        return f"Chinchero, {hoy.day} de {meses[hoy.month - 1]} de {self.config['anio']}"
    
    def _dibujar_parrafo(self, texto, x, y, ancho, estilo):
        """Dibuja un párrafo de texto"""
        p = Paragraph(texto, estilo)
        w, h = p.wrap(ancho, 600)
        p.drawOn(self.canvas, x, y - h)
        return y - h - 15
    
    def _agregar_qr(self, datos_alumno, tipo_doc):
        """Agrega código QR de validación"""
        data_qr = (
            f"I.E. ALTERNATIVO YACHAY\n"
            f"DOCUMENTO: {tipo_doc}\n"
            f"ESTUDIANTE: {datos_alumno['alumno']}\n"
            f"DNI: {datos_alumno['dni']}\n"
            f"FECHA EMISIÓN: {datetime.now().strftime('%d/%m/%Y')}\n"
            f"VÁLIDO"
        )
        
        qr = qrcode.QRCode(box_size=10, border=1)
        qr.add_data(data_qr)
        qr.make(fit=True)
        
        img_qr = qr.make_image(fill_color="black", back_color="white")
        temp_qr = "temp_qr.png"
        img_qr.save(temp_qr)
        
        self.canvas.drawImage(temp_qr, self.config['qr_x'], self.config['qr_y'], 
                            width=70, height=70)
        self.canvas.setFont("Helvetica", 6)
        self.canvas.drawCentredString(
            self.config['qr_x'] + 35, 
            self.config['qr_y'] - 5, 
            "CÓDIGO DE VERIFICACIÓN"
        )
        
        try:
            os.remove(temp_qr)
        except:
            pass
    
    def generar_constancia_vacante(self, datos):
        """Genera constancia de vacante CON APODERADO"""
        self._aplicar_fondo()
        self._dibujar_encabezado("CONSTANCIA DE VACANTE")
        
        y = self.config['y_titulo'] - 50
        mx, ancho = 60, self.width - 120
        
        estilo_normal = ParagraphStyle(
            'Normal', parent=self.styles['Normal'],
            fontSize=11, leading=15, alignment=TA_JUSTIFY
        )
        estilo_lista = ParagraphStyle(
            'Lista', parent=estilo_normal, leftIndent=25
        )
        
        y = self._dibujar_parrafo(
            "La Dirección de la Institución Educativa Particular ALTERNATIVO YACHAY de Chinchero, "
            "debidamente representada por su Directora, suscribe la presente:",
            mx, y, ancho, estilo_normal
        )
        
        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "CONSTANCIA DE VACANTE")
        y -= 25
        
        # CORREGIDO: SIEMPRE incluir apoderado
        texto = (
            f"Que, mediante el presente documento se hace constar que la Institución Educativa cuenta "
            f"con <b>VACANTE DISPONIBLE</b> en el nivel de {datos['grado'].upper()}, para el/la estudiante "
            f"<b>{datos['alumno'].upper()}</b>, identificado(a) con Documento Nacional de Identidad (DNI) "
            f"N° <b>{datos['dni']}</b>, hijo(a) de <b>{datos['apoderado'].upper()}</b> con DNI N° "
            f"<b>{datos['dni_apo']}</b>, correspondiente al año escolar <b>{self.config['anio']}</b>."
        )
        y = self._dibujar_parrafo(texto, mx, y, ancho, estilo_normal)
        
        y = self._dibujar_parrafo(
            "Asimismo, para efectos de formalizar la matrícula, el/la solicitante deberá presentar "
            "la siguiente documentación de manera obligatoria:",
            mx, y, ancho, estilo_normal
        )
        
        requisitos = [
            "• Certificado Oficial de Estudios (original).",
            "• Resolución Directoral de Traslado de Matrícula.",
            "• Libreta de Notas del Sistema SIAGIE.",
            "• Ficha Única de Matrícula del Sistema SIAGIE.",
            "• Copia del Documento Nacional de Identidad (DNI) del estudiante.",
            "• Constancia de No Adeudo de la institución de procedencia.",
            "• Folder o mica transparente para archivo de documentos."
        ]
        
        for req in requisitos:
            y = self._dibujar_parrafo(req, mx, y, ancho, estilo_lista)
        
        y = self._dibujar_parrafo(
            "Se expide la presente constancia a solicitud de la parte interesada, para los fines que "
            "estime conveniente.",
            mx, y, ancho, estilo_normal
        )
        
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE VACANTE")
        
        return self._finalizar()
    
    def generar_constancia_no_deudor(self, datos):
        """Genera constancia de no adeudo CON APODERADO"""
        self._aplicar_fondo()
        self._dibujar_encabezado("CONSTANCIA DE NO ADEUDO")
        
        y = self.config['y_titulo'] - 50
        mx, ancho = 60, self.width - 120
        
        estilo_normal = ParagraphStyle(
            'Normal', parent=self.styles['Normal'],
            fontSize=11, leading=15, alignment=TA_JUSTIFY
        )
        
        y = self._dibujar_parrafo(
            "La Dirección de la Institución Educativa Particular ALTERNATIVO YACHAY, "
            "debidamente representada por su Directora:",
            mx, y, ancho, estilo_normal
        )
        
        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "HACE CONSTAR:")
        y -= 25
        
        # CORREGIDO: SIEMPRE incluir apoderado
        texto = (
            f"Que el/la estudiante <b>{datos['alumno'].upper()}</b>, identificado(a) con Documento Nacional "
            f"de Identidad (DNI) N° <b>{datos['dni']}</b>, hijo(a) de <b>{datos['apoderado'].upper()}</b> "
            f"con DNI N° <b>{datos['dni_apo']}</b>, ha cumplido satisfactoriamente con todas sus "
            f"obligaciones económicas ante esta Institución Educativa, no registrando deuda alguna por concepto "
            f"de matrícula, pensiones de enseñanza, ni cualquier otro compromiso pecuniario derivado de su "
            f"permanencia en el plantel."
        )
        y = self._dibujar_parrafo(texto, mx, y, ancho, estilo_normal)
        
        y = self._dibujar_parrafo(
            "Se expide la presente constancia a solicitud del interesado(a), para los fines que estime conveniente.",
            mx, y, ancho, estilo_normal
        )
        
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE NO ADEUDO")
        
        return self._finalizar()
    
    def generar_constancia_estudios(self, datos):
        """Genera constancia de estudios CON APODERADO"""
        self._aplicar_fondo()
        self._dibujar_encabezado("CONSTANCIA DE ESTUDIOS")
        
        y = self.config['y_titulo'] - 50
        mx, ancho = 60, self.width - 120
        
        estilo_normal = ParagraphStyle(
            'Normal', parent=self.styles['Normal'],
            fontSize=11, leading=15, alignment=TA_JUSTIFY
        )
        
        y = self._dibujar_parrafo(
            "La Dirección de la Institución Educativa Particular ALTERNATIVO YACHAY, "
            "debidamente representada por su Directora:",
            mx, y, ancho, estilo_normal
        )
        
        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "HACE CONSTAR:")
        y -= 25
        
        # CORREGIDO: SIEMPRE incluir apoderado
        texto = (
            f"Que el/la estudiante <b>{datos['alumno'].upper()}</b>, identificado(a) con Documento Nacional "
            f"de Identidad (DNI) N° <b>{datos['dni']}</b>, hijo(a) de <b>{datos['apoderado'].upper()}</b> "
            f"con DNI N° <b>{datos['dni_apo']}</b>, se encuentra <b>DEBIDAMENTE MATRICULADO(A)</b> "
            f"en esta Institución Educativa para el año académico <b>{self.config['anio']}</b>, cursando "
            f"estudios en el nivel de <b>{datos['grado'].upper()}</b>, conforme consta en los registros "
            f"oficiales del plantel."
        )
        y = self._dibujar_parrafo(texto, mx, y, ancho, estilo_normal)
        
        y = self._dibujar_parrafo(
            "Se expide la presente constancia a petición de la parte interesada, para los fines que "
            "estime conveniente.",
            mx, y, ancho, estilo_normal
        )
        
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE ESTUDIOS")
        
        return self._finalizar()
    
    def generar_constancia_conducta(self, datos):
        """Genera constancia de conducta CON APODERADO y SOLO 'CONDUCTA'"""
        self._aplicar_fondo()
        self._dibujar_encabezado("CONSTANCIA DE CONDUCTA")
        
        y = self.config['y_titulo'] - 50
        mx, ancho = 60, self.width - 120
        
        estilo_normal = ParagraphStyle(
            'Normal', parent=self.styles['Normal'],
            fontSize=10, leading=14, alignment=TA_JUSTIFY
        )
        
        y = self._dibujar_parrafo(
            "La Dirección de la Institución Educativa Particular ALTERNATIVO YACHAY, "
            "debidamente representada por su Directora:",
            mx, y, ancho, estilo_normal
        )
        
        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "CERTIFICA:")
        y -= 25
        
        # CORREGIDO: SIEMPRE incluir apoderado y SOLO "CONDUCTA"
        texto = (
            f"Que el/la estudiante <b>{datos['alumno'].upper()}</b>, identificado(a) con DNI N° <b>{datos['dni']}</b>, "
            f"hijo(a) de <b>{datos['apoderado'].upper()}</b> con DNI N° <b>{datos['dni_apo']}</b>, "
            f"cursó estudios de Educación Secundaria en esta institución, obteniendo las siguientes "
            f"calificaciones en <b>CONDUCTA</b>:"
        )
        y = self._dibujar_parrafo(texto, mx, y, ancho, estilo_normal)
        
        y -= 15
        tx = self.width/2 - 200
        
        # Tabla de 5 años
        self.canvas.setFont("Helvetica-Bold", 10)
        self.canvas.drawString(tx, y, "GRADO")
        self.canvas.drawString(tx + 120, y, "AÑO ACADÉMICO")
        self.canvas.drawString(tx + 280, y, "CALIFICACIÓN")
        
        y -= 5
        self.canvas.line(tx - 10, y, tx + 380, y)
        y -= 20
        
        self.canvas.setFont("Helvetica", 9)
        
        grados = ["PRIMERO", "SEGUNDO", "TERCERO", "CUARTO", "QUINTO"]
        anio_base = int(self.config['anio']) - 5
        
        for i, grado in enumerate(grados):
            anio_actual = anio_base + i + 1
            nota = datos.get(f'nota_conducta_{i+1}', 'AD')
            
            self.canvas.drawString(tx, y, grado)
            self.canvas.drawString(tx + 120, y, str(anio_actual))
            self.canvas.drawString(tx + 280, y, nota)
            y -= 18
        
        y -= 10
        y = self._dibujar_parrafo(
            "Se expide la presente certificación a solicitud del interesado(a), para los fines que "
            "estime por conveniente.",
            mx, y, ancho, estilo_normal
        )
        
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE CONDUCTA")
        
        return self._finalizar()
    
    def generar_carta_compromiso(self, datos):
        """Genera carta compromiso AJUSTADA A UNA PÁGINA"""
        self._aplicar_fondo()
        self._dibujar_encabezado("CARTA DE COMPROMISO DEL PADRE DE FAMILIA")
        
        y = self.config['y_titulo'] - 40
        mx, ancho = 50, self.width - 100
        
        estilo_comp = ParagraphStyle(
            'Compromiso', parent=self.styles['Normal'],
            fontSize=8.5, leading=11, alignment=TA_JUSTIFY
        )
        
        intro = (
            f"Yo, <b>{datos['apoderado'].upper()}</b>, con DNI N° <b>{datos['dni_apo']}</b>, "
            f"padre/madre/apoderado(a) de <b>{datos['alumno'].upper()}</b>, me comprometo formalmente "
            f"a cumplir las siguientes obligaciones establecidas por la I.E. ALTERNATIVO YACHAY:"
        )
        y = self._dibujar_parrafo(intro, mx, y, ancho, estilo_comp)
        
        y -= 5
        
        compromisos = [
            "1. Velar por la asistencia puntual y regular de mi hijo(a) al centro educativo.",
            "2. Supervisar el cumplimiento diario de tareas escolares y trabajos académicos.",
            "3. Asegurar que asista correctamente uniformado(a) según el reglamento interno.",
            "4. Inculcar respeto hacia docentes, personal, compañeros y normas de convivencia.",
            "5. Participar en actividades del comité de aula y colaborar con los docentes.",
            "6. Ejercer crianza positiva, libre de violencia, promoviendo desarrollo integral.",
            "7. Atender oportunamente problemas de conducta, rendimiento o situaciones especiales.",
            "8. Asumir responsabilidad por daños materiales que ocasione a la institución.",
            "9. Vigilar que mantenga vocabulario apropiado y conducta respetuosa.",
            "10. Acudir inmediatamente cuando sea requerida mi presencia.",
            "11. Asistir puntualmente a reuniones, asambleas y citaciones programadas.",
            "12. Justificar inasistencias de manera oportuna y documentada (24 horas).",
            "13. Cumplir puntualmente con el pago de pensiones de enseñanza.",
            "14. Respetar la autonomía pedagógica, sin interferir en metodologías educativas."
        ]
        
        estilo_item = ParagraphStyle(
            'Item', parent=estilo_comp, leftIndent=10
        )
        
        for compromiso in compromisos:
            y = self._dibujar_parrafo(compromiso, mx, y, ancho, estilo_item)
            y += 2
        
        y -= 5
        y = self._dibujar_parrafo(
            "Declaro conocer y aceptar el estricto cumplimiento de lo establecido.",
            mx, y, ancho, estilo_comp
        )
        
        # Firmas
        y = 120
        self.canvas.line(80, y, 200, y)
        self.canvas.line(220, y, 340, y)
        self.canvas.line(360, y, 480, y)
        
        y -= 10
        self.canvas.setFont("Helvetica-Bold", 7)
        self.canvas.drawCentredString(140, y, "FIRMA PADRE/MADRE/APODERADO")
        self.canvas.drawCentredString(280, y, self.config['directora'].upper())
        self.canvas.drawCentredString(280, y - 10, "DIRECTORA")
        self.canvas.drawCentredString(420, y, self.config['promotor'].upper())
        self.canvas.drawCentredString(420, y - 10, "PROMOTOR")
        
        return self._finalizar()
    
    def _agregar_firmas(self):
        """Agrega firma de la directora"""
        yf = 110
        self.canvas.line(200, yf, 395, yf)
        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawCentredString(self.width/2, yf - 15, 
                                     self.config['directora'].upper())
        self.canvas.setFont("Helvetica", 9)
        self.canvas.drawCentredString(self.width/2, yf - 28, "DIRECTORA")
    
    def _finalizar(self):
        """Finaliza el PDF y retorna el buffer"""
        self.canvas.save()
        self.buffer.seek(0)
        return self.buffer

# ========================================
# GENERADOR DE CARNETS ULTRA MEJORADO
# ========================================

class GeneradorCarnet:
    """Genera carnets con LETRAS GIGANTESCAS y VIGENCIA MARZO-DICIEMBRE"""
    
    WIDTH = 1012
    HEIGHT = 638
    AZUL_INST = (0, 30, 120)
    
    def __init__(self, datos, anio, foto_bytes=None):
        self.datos = datos
        self.anio = anio
        self.foto_bytes = foto_bytes
        self.img = Image.new('RGB', (self.WIDTH, self.HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.img)
    
    def _aplicar_escudo_fondo(self):
        """Aplica escudo como marca de agua"""
        if Path("escudo_upload.png").exists():
            try:
                escudo = Image.open("escudo_upload.png").convert("RGBA")
                escudo = escudo.resize((400, 400), Image.LANCZOS)
                
                capa = Image.new('RGBA', (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))
                x = int((self.WIDTH - 400) / 2)
                y = int((self.HEIGHT - 400) / 2)
                capa.paste(escudo, (x, y))
                
                datos_pixel = capa.getdata()
                nuevos_datos = [
                    (d[0], d[1], d[2], 30) if d[3] > 0 else d 
                    for d in datos_pixel
                ]
                capa.putdata(nuevos_datos)
                
                self.img.paste(capa, (0, 0), mask=capa)
            except Exception:
                pass
    
    def _dibujar_barras_superiores(self):
        """Dibuja barras GIGANTES"""
        # Barra superior: 200px (antes 180)
        self.draw.rectangle([(0, 0), (self.WIDTH, 200)], fill=self.AZUL_INST)
        # Barra inferior: 170px (antes 150)
        self.draw.rectangle(
            [(0, self.HEIGHT - 170), (self.WIDTH, self.HEIGHT)], 
            fill=self.AZUL_INST
        )
    
    def _dibujar_textos_institucionales(self):
        """Dibuja textos GIGANTESCOS"""
        # ENCABEZADO ULTRA GRANDE: 150px (antes 130)
        font_header = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 150, bold=True)
        # PIE ULTRA GRANDE: 120px (antes 100)
        font_motto = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 120, bold=True)
        
        self.draw.text(
            (self.WIDTH/2, 100), 
            "I.E. ALTERNATIVO YACHAY",
            font=font_header, fill="white", anchor="mm"
        )
        
        self.draw.text(
            (self.WIDTH/2, self.HEIGHT - 85),
            "EDUCAR PARA LA VIDA",
            font=font_motto, fill="white", anchor="mm"
        )
    
    def _insertar_foto(self):
        """Inserta foto del alumno"""
        x_foto, y_foto = 50, 220  # Ajustado por barra más alta
        w_foto, h_foto = 290, 350
        
        if self.foto_bytes:
            try:
                foto_img = Image.open(self.foto_bytes).convert("RGB")
                foto_img = foto_img.resize((w_foto, h_foto), Image.LANCZOS)
                self.img.paste(foto_img, (x_foto, y_foto))
            except Exception:
                self._dibujar_placeholder_foto(x_foto, y_foto, w_foto, h_foto)
        else:
            self._dibujar_placeholder_foto(x_foto, y_foto, w_foto, h_foto)
        
        self.draw.rectangle(
            [(x_foto, y_foto), (x_foto + w_foto, y_foto + h_foto)],
            outline="black", width=6
        )
    
    def _dibujar_placeholder_foto(self, x, y, w, h):
        """Dibuja placeholder cuando no hay foto"""
        self.draw.rectangle([(x, y), (x + w, y + h)], fill="#eeeeee")
        font = RecursoManager.obtener_fuente("Roboto-Regular.ttf", 35)
        self.draw.text(
            (x + w/2, y + h/2),
            "SIN FOTO",
            font=font, fill="#666666", anchor="mm"
        )
    
    def _dibujar_datos_alumno(self):
        """Dibuja SOLO NOMBRE, DNI y VIGENCIA (sin grado ni año)"""
        x_text = 370
        y_nombre = 220
        y_dni = 360
        y_vigencia = 480
        
        nombre = self.datos['alumno'].upper()
        
        # NOMBRE: 95px corto, 70px largo (MÁS GRANDE)
        if len(nombre) > 22:
            font_nombre = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 70, bold=True)
            wrapper = textwrap.TextWrapper(width=25)
            lineas = wrapper.wrap(nombre)
            y_cursor = y_nombre - 10
            for linea in lineas[:2]:
                self.draw.text((x_text, y_cursor), linea, font=font_nombre, fill="black")
                y_cursor += 75
        else:
            font_nombre = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 95, bold=True)
            self.draw.text((x_text, y_nombre), nombre, font=font_nombre, fill="black")
        
        # ETIQUETAS Y DATOS: 75px (MÁS GRANDE)
        font_label = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 75, bold=True)
        font_data = RecursoManager.obtener_fuente("Roboto-Regular.ttf", 75)
        
        # DNI
        self.draw.text((x_text, y_dni), "DNI:", font=font_label, fill="black")
        self.draw.text((x_text + 140, y_dni), self.datos['dni'], font=font_data, fill="black")
        
        # VIGENCIA: MARZO - DICIEMBRE (sin año ni grado)
        self.draw.text((x_text, y_vigencia), "VIGENCIA:", font=font_label, fill="black")
        
        # Texto de vigencia
        font_vigencia = RecursoManager.obtener_fuente("Roboto-Regular.ttf", 60)
        self.draw.text((x_text + 300, y_vigencia + 5), "MARZO - DICIEMBRE", font=font_vigencia, fill="black")
    
    def _agregar_codigo_barras(self):
        """Agrega código de barras SOLO CON DNI"""
        if not HAS_BARCODE:
            return
        
        try:
            writer = ImageWriter()
            buffer_bar = io.BytesIO()
            Code128(self.datos['dni'], writer=writer).write(
                buffer_bar, 
                options={'write_text': False}
            )
            buffer_bar.seek(0)
            
            img_bar = Image.open(buffer_bar).resize((520, 120), Image.LANCZOS)
            self.img.paste(img_bar, (340, self.HEIGHT - 280))
        except Exception:
            pass
    
    def _agregar_qr(self):
        """Agrega código QR SOLO CON DNI"""
        try:
            qr = qrcode.QRCode(box_size=10, border=1)
            qr.add_data(self.datos['dni'])
            qr.make(fit=True)
            
            img_qr_pil = qr.make_image(fill_color="black", back_color="white")
            # QR ULTRA GRANDE: 240x240 (antes 220)
            img_qr = img_qr_pil.resize((240, 240), Image.LANCZOS)
            self.img.paste(img_qr, (self.WIDTH - 260, 220))
            
            # Texto: 32px (antes 28)
            font_small = RecursoManager.obtener_fuente("Roboto-Regular.ttf", 32)
            self.draw.text(
                (self.WIDTH - 140, 470),
                "ESCANEAR",
                font=font_small, fill="black", anchor="mm"
            )
        except Exception:
            pass
    
    def generar(self):
        """Genera el carnet completo"""
        self._aplicar_escudo_fondo()
        self._dibujar_barras_superiores()
        self._dibujar_textos_institucionales()
        self._insertar_foto()
        self._dibujar_datos_alumno()
        self._agregar_codigo_barras()
        self._agregar_qr()
        
        output = io.BytesIO()
        self.img.save(output, format='PNG', optimize=True)
        output.seek(0)
        return output

# ========================================
# SISTEMA DE LOGIN
# ========================================

def pantalla_login():
    """Pantalla de inicio de sesión"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='main-header'>", unsafe_allow_html=True)
        
        if Path("escudo_upload.png").exists():
            st.image("escudo_upload.png", width=150)
        
        st.markdown("<h1 style='color: white; margin: 0;'>SISTEMA YACHAY PRO</h1>", 
                   unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>Sistema Integral de Gestión Educativa</p>", 
                   unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
        
        with st.container():
            pwd = st.text_input("🔑 Contraseña de acceso:", type="password", key="login_pwd")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🔐 INGRESAR ADMIN", use_container_width=True, type="primary"):
                    if pwd == "306020":
                        st.session_state.rol = "admin"
                        st.success("✅ Acceso administrativo concedido")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("⛔ Contraseña incorrecta")
            
            with col_btn2:
                if st.button("👨‍🏫 INGRESAR DOCENTE", use_container_width=True):
                    if pwd == "deyanira":
                        st.session_state.rol = "docente"
                        st.success("✅ Acceso docente concedido")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("⛔ Contraseña incorrecta")

# ========================================
# CONFIGURACIÓN SIDEBAR
# ========================================

def configurar_sidebar():
    """Configura la barra lateral"""
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
        st.title("🎓 YACHAY PRO")
        
        rol_emoji = "⚙️" if st.session_state.rol == "admin" else "👨‍🏫"
        st.info(f"{rol_emoji} **Sesión:** {st.session_state.rol.upper()}")
        
        st.markdown("---")
        
        if st.session_state.rol == "admin":
            st.markdown("### ⚙️ Configuración del Sistema")
            
            with st.expander("📂 Archivos del Sistema", expanded=False):
                up_bd = st.file_uploader("📊 Base de Datos (Excel)", type=["xlsx"], key="upload_bd")
                if up_bd:
                    with open(BaseDatos.ARCHIVO, "wb") as f:
                        f.write(up_bd.getbuffer())
                    st.success("✅ Base de datos actualizada")
                    BaseDatos.cargar.clear()
                    time.sleep(0.5)
                    st.rerun()
                
                up_escudo = st.file_uploader("🛡️ Escudo Institucional (PNG)", type=["png"], key="upload_escudo")
                if up_escudo:
                    with open("escudo_upload.png", "wb") as f:
                        f.write(up_escudo.getbuffer())
                    st.success("✅ Escudo actualizado")
            
            with st.expander("👥 Autoridades", expanded=False):
                directora = st.text_input("Directora:", "Prof. Ana María CUSI INCA", key="directora_input")
                promotor = st.text_input("Promotor:", "Prof. Leandro CORDOVA TOCRE", key="promotor_input")
            
            with st.expander("🎯 Personalización", expanded=False):
                frase = st.text_input("Frase del Año:", "AÑO DE LA INTEGRACIÓN", key="frase_input")
        else:
            directora = "Prof. Ana María CUSI INCA"
            promotor = "Prof. Leandro CORDOVA TOCRE"
            frase = "AÑO DE LA INTEGRACIÓN"
        
        st.markdown("---")
        
        anio_sel = st.number_input("📅 Año Escolar:", 2024, 2030, 2026, key="anio_input")
        
        stats = BaseDatos.obtener_estadisticas()
        st.markdown("### 📊 Estadísticas")
        st.metric("Total Alumnos", stats['total_alumnos'])
        st.metric("Grados Registrados", stats['grados'])
        
        st.markdown("---")
        
        if st.button("🔴 CERRAR SESIÓN", use_container_width=True):
            st.session_state.rol = None
            st.rerun()
    
    return {
        'anio': anio_sel,
        'directora': directora,
        'promotor': promotor,
        'frase': frase,
        'y_frase': 700,
        'y_titulo': 630,
        'qr_x': 435,
        'qr_y': 47
    }

# ========================================
# TAB DOCUMENTOS
# ========================================

def tab_documentos(config):
    """Tab de generación de documentos"""
    st.header("📄 Emisión de Documentos Oficiales")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Configuración")
        
        tipo_doc = st.selectbox(
            "📑 Tipo de Documento:",
            [
                "CONSTANCIA DE VACANTE",
                "CONSTANCIA DE NO DEUDOR",
                "CONSTANCIA DE ESTUDIOS",
                "CONSTANCIA DE CONDUCTA",
                "CARTA COMPROMISO PADRE DE FAMILIA"
            ],
            key="tipo_doc_select"
        )
        
        st.markdown("---")
        
        dni_busqueda = st.text_input("🔍 Buscar por DNI:", key="dni_buscar_doc")
        
        if st.button("🔎 Buscar Alumno", use_container_width=True, key="btn_buscar_doc"):
            resultado = BaseDatos.buscar_por_dni(dni_busqueda)
            if resultado:
                st.session_state.alumno = resultado.get('Alumno', '')
                st.session_state.dni = resultado.get('Dni', '')
                st.session_state.grado = resultado.get('Grado', '')
                st.session_state.apoderado = resultado.get('Apoderado', '')
                st.session_state.dni_apo = resultado.get('Dni_Apoderado', '')
                st.success("✅ Datos cargados correctamente")
            else:
                st.error("❌ No se encontró alumno con ese DNI")
    
    with col2:
        st.subheader("Datos del Documento")
        
        with st.container(border=True):
            nombre = st.text_input("👤 Nombre Completo:", key="alumno")
            dni = st.text_input("🆔 DNI del Alumno:", key="dni")
            grado = st.text_input("📚 Grado:", key="grado")
            apoderado = st.text_input("👨‍👩‍👧 Apoderado:", key="apoderado")
            dni_apo = st.text_input("🆔 DNI Apoderado:", key="dni_apo")
            
            notas_conducta = {}
            if tipo_doc == "CONSTANCIA DE CONDUCTA":
                st.markdown("**📊 Calificaciones de Conducta (5 años):**")
                col_n1, col_n2, col_n3, col_n4, col_n5 = st.columns(5)
                
                with col_n1:
                    notas_conducta['nota_conducta_1'] = st.selectbox("1°", ["AD", "A", "B", "C"], key="nota1")
                with col_n2:
                    notas_conducta['nota_conducta_2'] = st.selectbox("2°", ["AD", "A", "B", "C"], key="nota2")
                with col_n3:
                    notas_conducta['nota_conducta_3'] = st.selectbox("3°", ["AD", "A", "B", "C"], key="nota3")
                with col_n4:
                    notas_conducta['nota_conducta_4'] = st.selectbox("4°", ["AD", "A", "B", "C"], key="nota4")
                with col_n5:
                    notas_conducta['nota_conducta_5'] = st.selectbox("5°", ["AD", "A", "B", "C"], key="nota5")
        
        st.markdown("---")
        
        if st.button("✨ GENERAR DOCUMENTO", type="primary", use_container_width=True, key="btn_generar_doc"):
            if nombre and dni and apoderado and dni_apo:
                with st.spinner("Generando documento..."):
                    datos = {
                        'alumno': nombre,
                        'dni': dni,
                        'grado': grado,
                        'apoderado': apoderado,
                        'dni_apo': dni_apo,
                        **notas_conducta
                    }
                    
                    gen = GeneradorPDF(config)
                    
                    if tipo_doc == "CONSTANCIA DE VACANTE":
                        pdf = gen.generar_constancia_vacante(datos)
                    elif tipo_doc == "CONSTANCIA DE NO DEUDOR":
                        pdf = gen.generar_constancia_no_deudor(datos)
                    elif tipo_doc == "CONSTANCIA DE ESTUDIOS":
                        pdf = gen.generar_constancia_estudios(datos)
                    elif tipo_doc == "CONSTANCIA DE CONDUCTA":
                        pdf = gen.generar_constancia_conducta(datos)
                    else:
                        pdf = gen.generar_carta_compromiso(datos)
                    
                    st.balloons()
                    st.success("✅ Documento generado exitosamente")
                    
                    st.download_button(
                        "⬇️ DESCARGAR DOCUMENTO",
                        pdf,
                        f"{tipo_doc}_{dni}.pdf",
                        "application/pdf",
                        use_container_width=True,
                        key="btn_descargar_pdf"
                    )
            else:
                st.error("⚠️ Complete todos los datos requeridos (alumno, DNI, apoderado y DNI apoderado)")

# ========================================
# TAB CARNETS
# ========================================

def tab_carnets(config):
    """Tab de generación de carnets"""
    st.markdown("## 🪪 Centro de Carnetización")
    st.markdown("---")
    
    col_individual, col_lote = st.columns([1, 1])
    
    with col_individual:
        st.subheader("⚡ Carnet Individual")
        st.caption("Genera un carnet rápidamente")
        
        with st.container(border=True):
            i_nom = st.text_input("👤 Nombre Completo:", key="i_nom")
            i_dni = st.text_input("🆔 DNI:", key="i_dni")
            i_foto = st.file_uploader(
                "📸 Foto (Opcional):", 
                type=['jpg', 'png', 'jpeg'],
                key="i_foto"
            )
            
            if st.button("👁️ GENERAR Y DESCARGAR", 
                        type="primary", 
                        use_container_width=True,
                        key="btn_generar_individual"):
                if i_nom and i_dni:
                    with st.spinner("Generando carnet..."):
                        foto_bytes = io.BytesIO(i_foto.getvalue()) if i_foto else None
                        datos = {
                            'alumno': i_nom,
                            'dni': i_dni,
                            'grado': ''  # No se usa
                        }
                        
                        gen = GeneradorCarnet(datos, config['anio'], foto_bytes)
                        carnet = gen.generar()
                        
                        st.image(carnet, caption="Vista Previa", use_container_width=True)
                        st.download_button(
                            "⬇️ DESCARGAR CARNET",
                            carnet,
                            f"Carnet_{i_dni}.png",
                            "image/png",
                            use_container_width=True,
                            key="btn_descargar_individual"
                        )
                else:
                    st.error("⚠️ Complete nombre y DNI")
    
    with col_lote:
        st.subheader("🛒 Generación en Lote")
        st.caption("Agrega múltiples alumnos y descarga en ZIP")
        
        with st.expander("➕ Agregar al Carrito", expanded=True):
            st.session_state.busqueda_counter += 1
            s_dni = st.text_input("🔍 Buscar por DNI:", key=f"s_dni_{st.session_state.busqueda_counter}")
            
            if st.button("Buscar en BD", key=f"btn_buscar_{st.session_state.busqueda_counter}"):
                resultado = BaseDatos.buscar_por_dni(s_dni)
                if resultado:
                    st.session_state.c_temp_nom = resultado.get('Alumno', '')
                    st.session_state.c_temp_dni = resultado.get('Dni', '')
                    st.success("✅ Datos encontrados")
                    st.rerun()
                else:
                    st.warning("No encontrado en la base de datos")
            
            c_nom = st.text_input(
                "Nombre:", 
                value=st.session_state.get('c_temp_nom', ''),
                key=f"c_nom_input_{st.session_state.busqueda_counter}"
            )
            c_dni = st.text_input(
                "DNI:", 
                value=st.session_state.get('c_temp_dni', ''),
                key=f"c_dni_input_{st.session_state.busqueda_counter}"
            )
            c_foto = st.file_uploader(
                "Foto:", 
                type=['jpg', 'png', 'jpeg'],
                key=f"c_foto_input_{st.session_state.busqueda_counter}"
            )
            
            if st.button("➕ AGREGAR", use_container_width=True, key=f"btn_agregar_{st.session_state.busqueda_counter}"):
                if c_nom and c_dni:
                    if c_dni not in [x['dni'] for x in st.session_state.cola_carnets]:
                        item = {
                            'alumno': c_nom,
                            'dni': c_dni,
                            'grado': '',
                            'foto_bytes': c_foto.getvalue() if c_foto else None
                        }
                        st.session_state.cola_carnets.append(item)
                        st.success(f"✅ {c_nom} agregado al carrito")
                        
                        st.session_state.c_temp_nom = ""
                        st.session_state.c_temp_dni = ""
                        st.session_state.busqueda_counter += 1
                        st.rerun()
                    else:
                        st.warning("⚠️ Este DNI ya está en el carrito")
                else:
                    st.error("⚠️ Complete nombre y DNI")
        
        st.markdown("---")
        cantidad = len(st.session_state.cola_carnets)
        st.markdown(f"### 📦 Carrito: **{cantidad}** carnets")
        
        if cantidad > 0:
            df_carrito = pd.DataFrame([
                {
                    'Alumno': item['alumno'],
                    'DNI': item['dni']
                }
                for item in st.session_state.cola_carnets
            ])
            st.dataframe(df_carrito, use_container_width=True, hide_index=True)
            
            col_desc, col_vac = st.columns([2, 1])
            
            with col_desc:
                if st.button("🚀 DESCARGAR PACK ZIP", 
                           type="primary", 
                           use_container_width=True,
                           key="btn_descargar_zip"):
                    with st.spinner("Generando carnets..."):
                        buffer_zip = io.BytesIO()
                        progreso = st.progress(0)
                        
                        with zipfile.ZipFile(buffer_zip, "w") as zf:
                            for i, item in enumerate(st.session_state.cola_carnets):
                                foto_io = io.BytesIO(item['foto_bytes']) if item['foto_bytes'] else None
                                gen = GeneradorCarnet(item, config['anio'], foto_io)
                                carnet = gen.generar()
                                
                                zf.writestr(
                                    f"Carnet_{item['dni']}_{item['alumno']}.png",
                                    carnet.getvalue()
                                )
                                progreso.progress((i + 1) / cantidad)
                        
                        buffer_zip.seek(0)
                        st.balloons()
                        
                        st.download_button(
                            "⬇️ GUARDAR ARCHIVO ZIP",
                            buffer_zip,
                            f"Pack_Carnets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                            "application/zip",
                            use_container_width=True,
                            key="btn_save_zip"
                        )
            
            with col_vac:
                if st.button("🗑️ Vaciar", use_container_width=True, key="btn_vaciar"):
                    st.session_state.cola_carnets = []
                    st.rerun()
        else:
            st.info("El carrito está vacío. Agrega alumnos para comenzar.")

# ========================================
# TAB BASE DE DATOS
# ========================================

def tab_base_datos():
    """Tab de visualización de base de datos"""
    st.header("📊 Base de Datos de Alumnos")
    
    df = BaseDatos.cargar()
    
    if df is not None:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📚 Total Alumnos", len(df))
        
        with col2:
            if 'Grado' in df.columns:
                st.metric("🎓 Grados", df['Grado'].nunique())
        
        with col3:
            if 'Apoderado' in df.columns:
                st.metric("👨‍👩‍👧 Con Apoderado", df['Apoderado'].notna().sum())
        
        with col4:
            if 'Dni' in df.columns:
                st.metric("🆔 Registros Completos", df['Dni'].notna().sum())
        
        st.markdown("---")
        
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            if 'Grado' in df.columns:
                grados = ['Todos'] + sorted(df['Grado'].dropna().unique().tolist())
                filtro_grado = st.selectbox("Filtrar por Grado:", grados, key="filtro_grado")
        
        with col_f2:
            busqueda = st.text_input("🔍 Buscar por nombre o DNI:", key="busqueda_bd")
        
        df_filtrado = df.copy()
        
        if filtro_grado != 'Todos' and 'Grado' in df.columns:
            df_filtrado = df_filtrado[df_filtrado['Grado'] == filtro_grado]
        
        if busqueda:
            mascara = df_filtrado.apply(
                lambda row: busqueda.lower() in str(row).lower(), 
                axis=1
            )
            df_filtrado = df_filtrado[mascara]
        
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            height=500
        )
        
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            "⬇️ Descargar CSV Filtrado",
            csv,
            f"base_datos_filtrada_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            key="btn_descargar_csv"
        )
    else:
        st.warning("⚠️ No hay base de datos cargada")
        st.info("💡 Carga un archivo Excel desde la barra lateral (solo administradores)")

# ========================================
# APLICACIÓN PRINCIPAL
# ========================================

def main():
    """Función principal de la aplicación"""
    
    if st.session_state.rol is None:
        pantalla_login()
        st.stop()
    
    config = configurar_sidebar()
    
    tab1, tab2, tab3 = st.tabs([
        "📄 DOCUMENTOS",
        "🪪 CARNETS",
        "📊 BASE DE DATOS"
    ])
    
    with tab1:
        tab_documentos(config)
    
    with tab2:
        tab_carnets(config)
    
    with tab3:
        tab_base_datos()

if __name__ == "__main__":
    main()
