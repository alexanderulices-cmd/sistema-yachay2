# Sistema completo - Parte 1 de 2
# Copiar COMPLETO en archivo .py
import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
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
import json
import webbrowser
import urllib.parse

st.set_page_config(page_title="SISTEMA YACHAY PRO", page_icon="🎓", layout="wide")

def init_session_state():
    defaults = {
        'rol': None, 'cola_carnets': [], 'alumno': '', 'dni': '', 'grado': '',
        'apoderado': '', 'dni_apo': '', 'c_temp_nom': '', 'c_temp_dni': '',
        'c_temp_gra': '', 'busqueda_counter': 0, 'asistencias_hoy': {}
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

st.markdown("""
<style>
.main-header {text-align:center;padding:2rem;background:linear-gradient(135deg,#001e7c 0%,#0052cc 100%);
color:white;border-radius:10px;margin-bottom:2rem;box-shadow:0 4px 6px rgba(0,0,0,0.1);}
.success-msg {background:#d4edda;color:#155724;padding:1rem;border-radius:5px;
border-left:4px solid #28a745;margin:1rem 0;}
</style>
""", unsafe_allow_html=True)

try:
    from barcode import Code128
    from barcode.writer import ImageWriter
    HAS_BARCODE = True
except ImportError:
    HAS_BARCODE = False

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
                    r = requests.get(url, timeout=10)
                    r.raise_for_status()
                    with open(nombre, 'wb') as f:
                        f.write(r.content)
                except Exception:
                    pass
    
    @staticmethod
    def obtener_fuente(nombre, tamaño, bold=False):
        try:
            archivo = "Roboto-Bold.ttf" if bold else "Roboto-Regular.ttf"
            return ImageFont.truetype(archivo, int(tamaño))
        except Exception:
            return ImageFont.load_default()

RecursoManager.descargar_fuentes()

class BaseDatos:
    ARCHIVO = "base_datos.xlsx"
    ASISTENCIAS = "asistencias.json"
    
    @staticmethod
    @st.cache_data(ttl=300)
    def cargar():
        try:
            if Path(BaseDatos.ARCHIVO).exists():
                df = pd.read_excel(BaseDatos.ARCHIVO, dtype=str, engine='openpyxl')
                df.columns = df.columns.str.strip().str.title()
                return df
            return None
        except Exception as e:
            return None
    
    @staticmethod
    def buscar_por_dni(dni):
        df = BaseDatos.cargar()
        if df is not None and 'Dni' in df.columns:
            dni = str(dni).strip()
            df['Dni'] = df['Dni'].astype(str).str.strip()
            resultado = df[df['Dni'] == dni]
            if not resultado.empty:
                return resultado.iloc[0].to_dict()
        return None
    
    @staticmethod
    def registrar_estudiante(nombre, dni, grado):
        df = BaseDatos.cargar()
        if df is None:
            df = pd.DataFrame(columns=['Alumno', 'Dni', 'Grado'])
        nuevo = pd.DataFrame([{'Alumno': nombre, 'Dni': dni, 'Grado': grado}])
        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_excel(BaseDatos.ARCHIVO, index=False)
        BaseDatos.cargar.clear()
        return True
    
    @staticmethod
    def guardar_asistencia(dni, nombre, tipo, hora):
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        if Path(BaseDatos.ASISTENCIAS).exists():
            with open(BaseDatos.ASISTENCIAS, 'r') as f:
                asistencias = json.load(f)
        else:
            asistencias = {}
        if fecha_hoy not in asistencias:
            asistencias[fecha_hoy] = {}
        asistencias[fecha_hoy][dni] = {
            'nombre': nombre,
            'entrada': hora if tipo == 'entrada' else asistencias[fecha_hoy].get(dni, {}).get('entrada', ''),
            'salida': hora if tipo == 'salida' else asistencias[fecha_hoy].get(dni, {}).get('salida', '')
        }
        with open(BaseDatos.ASISTENCIAS, 'w') as f:
            json.dump(asistencias, f, indent=2)
        return True
    
    @staticmethod
    def obtener_estadisticas():
        df = BaseDatos.cargar()
        if df is not None:
            return {
                'total_alumnos': len(df),
                'grados': df['Grado'].nunique() if 'Grado' in df.columns else 0,
                'con_apoderado': df['Apoderado'].notna().sum() if 'Apoderado' in df.columns else 0
            }
        return {'total_alumnos': 0, 'grados': 0, 'con_apoderado': 0}

class GeneradorPDF:
    def __init__(self, config):
        self.config = config
        self.buffer = io.BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
    
    def _aplicar_fondo(self):
        if Path("fondo.png").exists():
            try:
                self.canvas.drawImage("fondo.png", 0, 0, width=self.width, height=self.height)
            except Exception:
                pass
    
    def _dibujar_encabezado(self, titulo):
        self.canvas.setFont("Helvetica-Oblique", 7)
        self.canvas.drawCentredString(self.width/2, self.config['y_frase'], 
                                     f'"{self.config["frase"]}"')
        self.canvas.setFont("Helvetica", 11)
        fecha = self._obtener_fecha()
        self.canvas.drawRightString(self.width - 60, self.config['y_frase'] - 25, fecha)
        self.canvas.setFont("Helvetica-Bold", 16)
        self.canvas.drawCentredString(self.width/2, self.config['y_titulo'], titulo)
        self.canvas.setLineWidth(1)
        self.canvas.line(100, self.config['y_titulo'] - 5, self.width - 100, self.config['y_titulo'] - 5)
    
    def _obtener_fecha(self):
        meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto",
                "septiembre","octubre","noviembre","diciembre"]
        hoy = datetime.now()
        return f"Chinchero, {hoy.day} de {meses[hoy.month - 1]} de {self.config['anio']}"
    
    def _dibujar_parrafo(self, texto, x, y, ancho, estilo):
        p = Paragraph(texto, estilo)
        w, h = p.wrap(ancho, 600)
        p.drawOn(self.canvas, x, y - h)
        return y - h - 15
    
    def _agregar_qr(self, datos_alumno, tipo_doc):
        data_qr = f"I.E. ALTERNATIVO YACHAY\nDOCUMENTO: {tipo_doc}\nESTUDIANTE: {datos_alumno['alumno']}\nDNI: {datos_alumno['dni']}\nFECHA EMISIÓN: {datetime.now().strftime('%d/%m/%Y')}\nVÁLIDO"
        qr = qrcode.QRCode(box_size=10, border=1)
        qr.add_data(data_qr)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        temp_qr = "temp_qr.png"
        img_qr.save(temp_qr)
        self.canvas.drawImage(temp_qr, self.config['qr_x'], self.config['qr_y'], width=70, height=70)
        self.canvas.setFont("Helvetica", 6)
        self.canvas.drawCentredString(self.config['qr_x'] + 35, self.config['qr_y'] - 5, "CÓDIGO DE VERIFICACIÓN")
        try:
            os.remove(temp_qr)
        except:
            pass
    
    def _agregar_solicitante(self, datos, y):
        texto_solicitud = f"Se expide el presente documento a solicitud del Padre/Madre <b>{datos['apoderado'].upper()}</b> con DNI N° <b>{datos['dni_apo']}</b>."
        estilo_solicitud = ParagraphStyle('Solicitud', parent=self.styles['Normal'], fontSize=10, leading=14, alignment=TA_JUSTIFY)
        mx, ancho = 60, self.width - 120
        return self._dibujar_parrafo(texto_solicitud, mx, y, ancho, estilo_solicitud)
    
    def generar_resolucion_traslado(self, datos):
        self._aplicar_fondo()
        self.canvas.setFont("Helvetica-Oblique", 8)
        self.canvas.drawCentredString(self.width/2, 700, f'"{self.config["frase"]}"')
        y = 670
        self.canvas.setFont("Helvetica-Bold", 14)
        self.canvas.drawCentredString(self.width/2, y, f"RESOLUCIÓN DIRECTORAL N° {datos['num_resolucion']}")
        y -= 30
        self.canvas.setFont("Helvetica", 11)
        fecha_resolucion = datos.get('fecha_resolucion', self._obtener_fecha())
        self.canvas.drawCentredString(self.width/2, y, fecha_resolucion)
        y -= 40
        mx, ancho = 60, self.width - 120
        estilo_normal = ParagraphStyle('Normal', parent=self.styles['Normal'], fontSize=11, leading=15, alignment=TA_JUSTIFY)
        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawString(mx, y, "VISTO:")
        y -= 20
        texto_visto = f"La solicitud del(a) apoderado(a), de <b>{datos['alumno'].upper()}</b> y el informe de progreso de <b>{datos['nivel'].upper()}</b>."
        y = self._dibujar_parrafo(texto_visto, mx, y, ancho, estilo_normal)
        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawString(mx, y, "CONSIDERANDO:")
        y -= 20
        texto_considerando = "Que, es procedente autorizar el traslado de matrícula de educandos cuyos padres o apoderados lo soliciten, a fin de garantizar la continuidad de estudios del educando."
        y = self._dibujar_parrafo(texto_considerando, mx, y, ancho, estilo_normal)
        texto_ley = "De conformidad con lo dispuesto por Ley de Educación N°28044, la RM 474-2022 MINEDU."
        y = self._dibujar_parrafo(texto_ley, mx, y, ancho, estilo_normal)
        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawString(mx, y, "SE RESUELVE:")
        y -= 20
        self.canvas.setFont("Helvetica-Bold", 10)
        self.canvas.drawString(mx, y, "PRIMERO:")
        y -= 15
        self.canvas.setFont("Helvetica", 10)
        self.canvas.drawString(mx, y, "Autorizar el traslado de matrícula del alumno(a):")
        y -= 25
        tabla_data = [
            ['APELLIDOS Y NOMBRE', datos['alumno'].upper()],
            ['NIVEL', datos['nivel'].upper()],
            ['IE PROCEDENCIA', 'IEP ALTERNATIVO YACHAY'],
            ['CÓDIGO DE LA IE', '1398841-0'],
            ['IE DE DESTINO', datos['ie_destino'].upper()],
            ['APTO PARA CONTINUAR EN', datos['nivel_destino'].upper()]
        ]
        tabla = Table(tabla_data, colWidths=[200, 280])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        tabla.wrapOn(self.canvas, ancho, 200)
        tabla.drawOn(self.canvas, mx, y - 110)
        y -= 130
        self.canvas.setFont("Helvetica-Bold", 10)
        self.canvas.drawString(mx, y, "SEGUNDO:")
        y -= 15
        self.canvas.setFont("Helvetica", 10)
        self.canvas.drawString(mx, y, "Disponer que se realice el traslado, vía SIAGIE al término de la distancia.")
        y -= 20
        self.canvas.setFont("Helvetica-Bold", 10)
        self.canvas.drawString(mx, y, "TERCERO:")
        y -= 15
        self.canvas.setFont("Helvetica", 10)
        self.canvas.drawString(mx, y, "Disponer la devolución de los documentos del menor en referencia.")
        y -= 30
        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawCentredString(self.width/2, y, "REGISTRE Y COMUNÍQUESE")
        self._agregar_firmas()
        self._agregar_qr(datos, "RESOLUCIÓN DE TRASLADO")
        return self._finalizar()
    
    def generar_constancia_vacante(self, datos):
        self._aplicar_fondo()
        self._dibujar_encabezado("CONSTANCIA DE VACANTE")
        y = self.config['y_titulo'] - 50
        mx, ancho = 60, self.width - 120
        estilo_normal = ParagraphStyle('Normal', parent=self.styles['Normal'], fontSize=11, leading=15, alignment=TA_JUSTIFY)
        estilo_lista = ParagraphStyle('Lista', parent=estilo_normal, leftIndent=25)
        y = self._dibujar_parrafo("La Dirección de la Institución Educativa Particular ALTERNATIVO YACHAY de Chinchero, debidamente representada por su Directora, suscribe la presente:", mx, y, ancho, estilo_normal)
        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "CONSTANCIA DE VACANTE")
        y -= 25
        texto = f"Que, mediante el presente documento se hace constar que la Institución Educativa cuenta con <b>VACANTE DISPONIBLE</b> en el nivel de {datos['grado'].upper()}, para el/la estudiante <b>{datos['alumno'].upper()}</b>, identificado(a) con Documento Nacional de Identidad (DNI) N° <b>{datos['dni']}</b>, correspondiente al año escolar <b>{self.config['anio']}</b>."
        y = self._dibujar_parrafo(texto, mx, y, ancho, estilo_normal)
        y = self._dibujar_parrafo("Asimismo, para efectos de formalizar la matrícula, el/la solicitante deberá presentar la siguiente documentación de manera obligatoria:", mx, y, ancho, estilo_normal)
        requisitos = ["• Certificado Oficial de Estudios (original).","• Resolución Directoral de Traslado de Matrícula.","• Libreta de Notas del Sistema SIAGIE.","• Ficha Única de Matrícula del Sistema SIAGIE.","• Copia del Documento Nacional de Identidad (DNI) del estudiante.","• Constancia de No Adeudo de la institución de procedencia.","• Folder o mica transparente para archivo de documentos."]
        for req in requisitos:
            y = self._dibujar_parrafo(req, mx, y, ancho, estilo_lista)
        y = self._agregar_solicitante(datos, y)
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE VACANTE")
        return self._finalizar()
    
    def generar_constancia_no_deudor(self, datos):
        self._aplicar_fondo()
        self._dibujar_encabezado("CONSTANCIA DE NO ADEUDO")
        y = self.config['y_titulo'] - 50
        mx, ancho = 60, self.width - 120
        estilo_normal = ParagraphStyle('Normal', parent=self.styles['Normal'], fontSize=11, leading=15, alignment=TA_JUSTIFY)
        y = self._dibujar_parrafo("La Dirección de la Institución Educativa Particular ALTERNATIVO YACHAY, debidamente representada por su Directora:", mx, y, ancho, estilo_normal)
        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "HACE CONSTAR:")
        y -= 25
        texto = f"Que el/la estudiante <b>{datos['alumno'].upper()}</b>, identificado(a) con Documento Nacional de Identidad (DNI) N° <b>{datos['dni']}</b>, ha cumplido satisfactoriamente con todas sus obligaciones económicas ante esta Institución Educativa, no registrando deuda alguna por concepto de matrícula, pensiones de enseñanza, ni cualquier otro compromiso pecuniario derivado de su permanencia en el plantel."
        y = self._dibujar_parrafo(texto, mx, y, ancho, estilo_normal)
        y = self._agregar_solicitante(datos, y)
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE NO ADEUDO")
        return self._finalizar()
    
    def generar_constancia_estudios(self, datos):
        self._aplicar_fondo()
        self._dibujar_encabezado("CONSTANCIA DE ESTUDIOS")
        y = self.config['y_titulo'] - 50
        mx, ancho = 60, self.width - 120
        estilo_normal = ParagraphStyle('Normal', parent=self.styles['Normal'], fontSize=11, leading=15, alignment=TA_JUSTIFY)
        y = self._dibujar_parrafo("La Dirección de la Institución Educativa Particular ALTERNATIVO YACHAY, debidamente representada por su Directora:", mx, y, ancho, estilo_normal)
        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "HACE CONSTAR:")
        y -= 25
        texto = f"Que el/la estudiante <b>{datos['alumno'].upper()}</b>, identificado(a) con Documento Nacional de Identidad (DNI) N° <b>{datos['dni']}</b>, se encuentra <b>DEBIDAMENTE MATRICULADO(A)</b> en esta Institución Educativa para el año académico <b>{self.config['anio']}</b>, cursando estudios en el nivel de <b>{datos['grado'].upper()}</b>, conforme consta en los registros oficiales del plantel."
        y = self._dibujar_parrafo(texto, mx, y, ancho, estilo_normal)
        y = self._agregar_solicitante(datos, y)
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE ESTUDIOS")
        return self._finalizar()
    
    def generar_constancia_conducta(self, datos):
        self._aplicar_fondo()
        self._dibujar_encabezado("CONSTANCIA DE CONDUCTA")
        y = self.config['y_titulo'] - 50
        mx, ancho = 60, self.width - 120
        estilo_normal = ParagraphStyle('Normal', parent=self.styles['Normal'], fontSize=10, leading=14, alignment=TA_JUSTIFY)
        y = self._dibujar_parrafo("La Dirección de la Institución Educativa Particular ALTERNATIVO YACHAY, debidamente representada por su Directora:", mx, y, ancho, estilo_normal)
        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "CERTIFICA:")
        y -= 25
        texto = f"Que el/la estudiante <b>{datos['alumno'].upper()}</b>, identificado(a) con DNI N° <b>{datos['dni']}</b>, cursó estudios de Educación Secundaria en esta institución, obteniendo las siguientes calificaciones en <b>CONDUCTA</b>:"
        y = self._dibujar_parrafo(texto, mx, y, ancho, estilo_normal)
        y -= 15
        tx = self.width/2 - 200
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
        y = self._agregar_solicitante(datos, y)
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE CONDUCTA")
        return self._finalizar()
    
    def generar_carta_compromiso(self, datos):
        self._aplicar_fondo()
        self._dibujar_encabezado("CARTA DE COMPROMISO DEL PADRE DE FAMILIA")
        y = self.config['y_titulo'] - 40
        mx, ancho = 50, self.width - 100
        estilo_comp = ParagraphStyle('Compromiso', parent=self.styles['Normal'], fontSize=8.5, leading=11, alignment=TA_JUSTIFY)
        intro = f"Yo, <b>{datos['apoderado'].upper()}</b>, con DNI N° <b>{datos['dni_apo']}</b>, padre/madre/apoderado(a) de <b>{datos['alumno'].upper()}</b>, estudiante del <b>{datos['grado'].upper()}</b>, me comprometo formalmente a cumplir las siguientes obligaciones establecidas por la I.E. ALTERNATIVO YACHAY:"
        y = self._dibujar_parrafo(intro, mx, y, ancho, estilo_comp)
        y -= 5
        compromisos = ["1. Velar por la asistencia puntual y regular de mi hijo(a) al centro educativo.","2. Supervisar el cumplimiento diario de tareas escolares y trabajos académicos.","3. Asegurar que asista correctamente uniformado(a) según el reglamento interno.","4. Inculcar respeto hacia docentes, personal, compañeros y normas de convivencia.","5. Participar en actividades del comité de aula y colaborar con los docentes.","6. Ejercer crianza positiva, libre de violencia, promoviendo desarrollo integral.","7. Atender oportunamente problemas de conducta, rendimiento o situaciones especiales.","8. Asumir responsabilidad por daños materiales que ocasione a la institución.","9. Vigilar que mantenga vocabulario apropiado y conducta respetuosa.","10. Acudir inmediatamente cuando sea requerida mi presencia.","11. Asistir puntualmente a reuniones, asambleas y citaciones programadas.","12. Justificar inasistencias de manera oportuna y documentada (24 horas).","13. Cumplir puntualmente con el pago de pensiones de enseñanza.","14. Respetar la autonomía pedagógica, sin interferir en metodologías educativas."]
        estilo_item = ParagraphStyle('Item', parent=estilo_comp, leftIndent=10)
        for compromiso in compromisos:
            y = self._dibujar_parrafo(compromiso, mx, y, ancho, estilo_item)
            y += 2
        y -= 5
        y = self._dibujar_parrafo("Declaro conocer y aceptar el estricto cumplimiento de lo establecido.", mx, y, ancho, estilo_comp)
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
        yf = 110
        self.canvas.line(200, yf, 395, yf)
        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawCentredString(self.width/2, yf - 15, self.config['directora'].upper())
        self.canvas.setFont("Helvetica", 9)
        self.canvas.drawCentredString(self.width/2, yf - 28, "DIRECTORA")
    
    def _finalizar(self):
        self.canvas.save()
        self.buffer.seek(0)
        return self.buffer

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
    
    def _aplicar_escudo_fondo(self):
        if Path("escudo_upload.png").exists():
            try:
                escudo = Image.open("escudo_upload.png").convert("RGBA")
                escudo = escudo.resize((400, 400), Image.LANCZOS)
                capa = Image.new('RGBA', (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))
                x = int((self.WIDTH - 400) / 2)
                y = int((self.HEIGHT - 400) / 2)
                capa.paste(escudo, (x, y))
                datos_pixel = capa.getdata()
                nuevos_datos = [(d[0], d[1], d[2], 30) if d[3] > 0 else d for d in datos_pixel]
                capa.putdata(nuevos_datos)
                self.img.paste(capa, (0, 0), mask=capa)
            except Exception:
                pass
    
    def _dibujar_barras_superiores(self):
        self.draw.rectangle([(0, 0), (self.WIDTH, 200)], fill=self.AZUL_INST)
        self.draw.rectangle([(0, self.HEIGHT - 170), (self.WIDTH, self.HEIGHT)], fill=self.AZUL_INST)
    
    def _dibujar_textos_institucionales(self):
        font_header = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 170, bold=True)
        font_motto = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 140, bold=True)
        self.draw.text((self.WIDTH/2, 100), "I.E. ALTERNATIVO YACHAY", font=font_header, fill="white", anchor="mm")
        self.draw.text((self.WIDTH/2, self.HEIGHT - 85), "EDUCAR PARA LA VIDA", font=font_motto, fill="white", anchor="mm")
    
    def _insertar_foto(self):
        x_foto, y_foto = 50, 220
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
        self.draw.rectangle([(x_foto, y_foto), (x_foto + w_foto, y_foto + h_foto)], outline="black", width=6)
    
    def _dibujar_placeholder_foto(self, x, y, w, h):
        self.draw.rectangle([(x, y), (x + w, y + h)], fill="#eeeeee")
        font = RecursoManager.obtener_fuente("Roboto-Regular.ttf", 35)
        self.draw.text((x + w/2, y + h/2), "SIN FOTO", font=font, fill="#666666", anchor="mm")
    
    def _dibujar_datos_alumno(self):
        x_text = 370
        y_nombre = 220
        y_dni = 320
        y_grado = 400
        y_vigencia = 480
        nombre = self.datos['alumno'].upper()
        if len(nombre) > 22:
            font_nombre = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 60, bold=True)
            wrapper = textwrap.TextWrapper(width=25)
            lineas = wrapper.wrap(nombre)
            y_cursor = y_nombre - 10
            for linea in lineas[:2]:
                self.draw.text((x_text, y_cursor), linea, font=font_nombre, fill="black")
                y_cursor += 65
        else:
            font_nombre = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 85, bold=True)
            self.draw.text((x_text, y_nombre), nombre, font=font_nombre, fill="black")
        font_label = RecursoManager.obtener_fuente("Roboto-Bold.ttf", 70, bold=True)
        font_data = RecursoManager.obtener_fuente("Roboto-Regular.ttf", 70)
        self.draw.text((x_text, y_dni), "DNI:", font=font_label, fill="black")
        self.draw.text((x_text + 130, y_dni), self.datos['dni'], font=font_data, fill="black")
        self.draw.text((x_text, y_grado), "GRADO:", font=font_label, fill="black")
        grado_text = self.datos.get('grado', 'N/A').upper()
        font_grado = font_data if len(grado_text) <= 15 else RecursoManager.obtener_fuente("Roboto-Regular.ttf", 50)
        self.draw.text((x_text + 220, y_grado), grado_text, font=font_grado, fill="black")
        self.draw.text((x_text, y_vigencia), "VIGENCIA:", font=font_label, fill="black")
        self.draw.text((x_text + 280, y_vigencia), str(self.anio), font=font_data, fill="black")
    
    def _agregar_codigo_barras(self):
        if not HAS_BARCODE:
            return
        try:
            writer = ImageWriter()
            buffer_bar = io.BytesIO()
            Code128(self.datos['dni'], writer=writer).write(buffer_bar, options={'write_text': False})
            buffer_bar.seek(0)
            img_bar = Image.open(buffer_bar).resize((520, 120), Image.LANCZOS)
            self.img.paste(img_bar, (340, self.HEIGHT - 280))
        except Exception:
            pass
    
    def _agregar_qr(self):
        try:
            qr = qrcode.QRCode(box_size=10, border=1)
            qr.add_data(self.datos['dni'])
            qr.make(fit=True)
            img_qr_pil = qr.make_image(fill_color="black", back_color="white")
            img_qr = img_qr_pil.resize((240, 240), Image.LANCZOS)
            self.img.paste(img_qr, (self.WIDTH - 260, 220))
            font_small = RecursoManager.obtener_fuente("Roboto-Regular.ttf", 32)
            self.draw.text((self.WIDTH - 140, 470), "ESCANEAR", font=font_small, fill="black", anchor="mm")
        except Exception:
            pass
    
    def generar(self):
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

def pantalla_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='main-header'>", unsafe_allow_html=True)
        if Path("escudo_upload.png").exists():
            st.image("escudo_upload.png", width=150)
        st.markdown("<h1 style='color: white; margin: 0;'>SISTEMA YACHAY PRO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>Sistema Integral de Gestión Educativa</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.container():
            pwd = st.text_input("🔑 Contraseña de acceso:", type="password", key="login_pwd")
            if st.button("🔐 INGRESAR AL SISTEMA", use_container_width=True, type="primary"):
                if pwd == "306020":
                    st.session_state.rol = "admin"
                    st.success("✅ Acceso Administrativo")
                    time.sleep(0.5)
                    st.rerun()
                elif pwd == "deyanira":
                    st.session_state.rol = "directivo"
                    st.success("✅ Acceso Directivo")
                    time.sleep(0.5)
                    st.rerun()
                elif pwd == "123456789":
                    st.session_state.rol = "auxiliar"
                    st.success("✅ Acceso Auxiliar")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("⛔ Contraseña incorrecta")

def enviar_whatsapp(telefono, mensaje):
    mensaje_encoded = urllib.parse.quote(mensaje)
    url = f"https://wa.me/{telefono}?text={mensaje_encoded}"
    webbrowser.open(url)

def generar_mensaje_asistencia(nombre, tipo, hora):
    saludo = "Buenos días" if int(hora.split(':')[0]) < 12 else "Buenas tardes"
    if tipo == "entrada":
        emoji_tipo = "✅"
        tipo_texto = "ENTRADA"
        mensaje_extra = "💡 Ejemplo de puntualidad."
    else:
        emoji_tipo = "🏁"
        tipo_texto = "SALIDA"
        mensaje_extra = "👋 Hasta mañana."
    mensaje = f"""{saludo} {nombre},
🏫 El Colegio Yachay informa:
{emoji_tipo} Registro de {tipo_texto} exitoso.
🕒 Hora: {hora}
{mensaje_extra}"""
    return mensaje

def tab_asistencias():
    st.header("📋 Sistema de Registro de Asistencias")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📸 Escanear QR")
        tipo_registro = st.radio("Tipo de registro:", ["Entrada", "Salida"])
        dni_manual = st.text_input("O ingresa DNI manualmente:")
        if st.button("🔍 REGISTRAR ASISTENCIA"):
            if dni_manual:
                alumno = BaseDatos.buscar_por_dni(dni_manual)
                if alumno:
                    hora_actual = datetime.now().strftime('%H:%M:%S')
                    BaseDatos.guardar_asistencia(dni_manual, alumno['Alumno'], tipo_registro.lower(), hora_actual)
                    st.success(f"✅ {alumno['Alumno']}")
                    st.info(f"🕒 Hora: {hora_actual}")
                    mensaje = generar_mensaje_asistencia(alumno['Alumno'], tipo_registro.lower(), hora_actual)
                    st.text_area("Mensaje para WhatsApp:", mensaje, height=150)
                    telefono = st.text_input("Teléfono (con código país, ej: 51987654321):")
                    if telefono and st.button("📱 ENVIAR POR WHATSAPP"):
                        enviar_whatsapp(telefono, mensaje)
                        st.success("✅ Abriendo WhatsApp...")
                else:
                    st.error("❌ DNI no encontrado")
    with col2:
        st.subheader("➕ Registrar Nuevo Estudiante")
        with st.container(border=True):
            nuevo_nombre = st.text_input("Nombre completo:")
            nuevo_dni = st.text_input("DNI:")
            nuevo_grado = st.text_input("Grado:")
            if st.button("💾 GUARDAR ESTUDIANTE"):
                if nuevo_nombre and nuevo_dni and nuevo_grado:
                    BaseDatos.registrar_estudiante(nuevo_nombre, nuevo_dni, nuevo_grado)
                    st.success("✅ Estudiante registrado")
                else:
                    st.error("⚠️ Complete todos los campos")

def configurar_sidebar():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
        st.title("🎓 YACHAY PRO")
        rol_emoji = {"admin": "⚙️", "directivo": "📋", "auxiliar": "👤"}
        st.info(f"{rol_emoji.get(st.session_state.rol, '🔐')} **Sesión:** {st.session_state.rol.upper()}")
        st.markdown("---")
        if st.session_state.rol == "admin":
            st.markdown("### ⚙️ Configuración")
            with st.expander("📂 Archivos", expanded=False):
                up_bd = st.file_uploader("📊 Base de Datos", type=["xlsx"], key="upload_bd")
                if up_bd:
                    with open(BaseDatos.ARCHIVO, "wb") as f:
                        f.write(up_bd.getbuffer())
                    st.success("✅ BD actualizada")
                    BaseDatos.cargar.clear()
                    time.sleep(0.5)
                    st.rerun()
                up_escudo = st.file_uploader("🛡️ Escudo", type=["png"], key="upload_escudo")
                if up_escudo:
                    with open("escudo_upload.png", "wb") as f:
                        f.write(up_escudo.getbuffer())
                    st.success("✅ Escudo actualizado")
            with st.expander("👥 Autoridades", expanded=False):
                directora = st.text_input("Directora:", "Prof. Ana María CUSI INCA", key="dir_i")
                promotor = st.text_input("Promotor:", "Prof. Leandro CORDOVA TOCRE", key="pro_i")
            with st.expander("🎯 Personalización", expanded=False):
                frase = st.text_input("Frase del Año:", "Año de la Esperanza y el Fortalecimiento de la Democracia", key="fr_i")
        else:
            directora = "Prof. Ana María CUSI INCA"
            promotor = "Prof. Leandro CORDOVA TOCRE"
            frase = "Año de la Esperanza y el Fortalecimiento de la Democracia"
        st.markdown("---")
        anio_sel = st.number_input("📅 Año:", 2024, 2030, 2026, key="anio_i")
        stats = BaseDatos.obtener_estadisticas()
        st.markdown("### 📊 Estadísticas")
        st.metric("Total Alumnos", stats['total_alumnos'])
        st.metric("Grados", stats['grados'])
        st.markdown("---")
        if st.button("🔴 CERRAR SESIÓN", use_container_width=True):
            st.session_state.rol = None
            st.rerun()
    return {'anio': anio_sel, 'directora': directora, 'promotor': promotor, 'frase': frase, 'y_frase': 700, 'y_titulo': 630, 'qr_x': 435, 'qr_y': 47}

def tab_documentos(config):
    st.header("📄 Emisión de Documentos")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Configuración")
        tipo_doc = st.selectbox("📑 Tipo:", ["CONSTANCIA DE VACANTE", "CONSTANCIA DE NO DEUDOR", "CONSTANCIA DE ESTUDIOS", "CONSTANCIA DE CONDUCTA", "CARTA COMPROMISO PADRE DE FAMILIA", "RESOLUCIÓN DE TRASLADO"], key="tipo_doc_sel")
        st.markdown("---")
        dni_busqueda = st.text_input("🔍 Buscar DNI:", key="dni_bus_doc")
        if st.button("🔎 Buscar", use_container_width=True, key="btn_bus_doc"):
            resultado = BaseDatos.buscar_por_dni(dni_busqueda)
            if resultado:
                st.session_state.alumno = resultado.get('Alumno', '')
                st.session_state.dni = resultado.get('Dni', '')
                st.session_state.grado = resultado.get('Grado', '')
                st.session_state.apoderado = resultado.get('Apoderado', '')
                st.session_state.dni_apo = resultado.get('Dni_Apoderado', '')
                st.success("✅ Datos cargados")
            else:
                st.error("❌ No encontrado")
    with col2:
        st.subheader("Datos del Documento")
        with st.container(border=True):
            nombre = st.text_input("👤 Nombre:", key="alumno")
            dni = st.text_input("🆔 DNI:", key="dni")
            grado = st.text_input("📚 Grado:", key="grado")
            apoderado = st.text_input("👨‍👩‍👧 Apoderado:", key="apoderado")
            dni_apo = st.text_input("🆔 DNI Apoderado:", key="dni_apo")
            notas_conducta = {}
            if tipo_doc == "CONSTANCIA DE CONDUCTA":
                st.markdown("**📊 Calificaciones (5 años):**")
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
            elif tipo_doc == "RESOLUCIÓN DE TRASLADO":
                num_resolucion = st.text_input("N° Resolución (ej: 011 DREC/UGEL-U/IEPYACHAY/2026):", key="num_res")
                fecha_resolucion = st.text_input("Fecha resolución:", value=datetime.now().strftime("Chinchero, %d de %B del %Y"), key="fec_res")
                nivel = st.selectbox("Nivel:", ["INICIAL", "PRIMARIA", "SECUNDARIA"], key="nivel_res")
                ie_destino = st.text_input("IE de Destino:", key="ie_dest")
                nivel_destino = st.text_input("Nivel de Continuidad (ej: PRIMER GRADO - PRIMARIA):", key="niv_dest")
        st.markdown("---")
        if st.button("✨ GENERAR DOCUMENTO", type="primary", use_container_width=True, key="btn_gen_doc"):
            if nombre and dni and apoderado and dni_apo:
                with st.spinner("Generando..."):
                    datos = {'alumno': nombre, 'dni': dni, 'grado': grado, 'apoderado': apoderado, 'dni_apo': dni_apo, **notas_conducta}
                    if tipo_doc == "RESOLUCIÓN DE TRASLADO":
                        datos.update({'num_resolucion': num_resolucion, 'fecha_resolucion': fecha_resolucion, 'nivel': nivel, 'ie_destino': ie_destino, 'nivel_destino': nivel_destino})
                    gen = GeneradorPDF(config)
                    if tipo_doc == "CONSTANCIA DE VACANTE":
                        pdf = gen.generar_constancia_vacante(datos)
                    elif tipo_doc == "CONSTANCIA DE NO DEUDOR":
                        pdf = gen.generar_constancia_no_deudor(datos)
                    elif tipo_doc == "CONSTANCIA DE ESTUDIOS":
                        pdf = gen.generar_constancia_estudios(datos)
                    elif tipo_doc == "CONSTANCIA DE CONDUCTA":
                        pdf = gen.generar_constancia_conducta(datos)
                    elif tipo_doc == "RESOLUCIÓN DE TRASLADO":
                        pdf = gen.generar_resolucion_traslado(datos)
                    else:
                        pdf = gen.generar_carta_compromiso(datos)
                    st.balloons()
                    st.success("✅ Documento generado")
                    st.download_button("⬇️ DESCARGAR", pdf, f"{tipo_doc}_{dni}.pdf", "application/pdf", use_container_width=True, key="btn_desc_pdf")
            else:
                st.error("⚠️ Complete todos los datos")

def tab_carnets(config):
    st.markdown("## 🪪 Centro de Carnetización")
    col_individual, col_lote = st.columns([1, 1])
    with col_individual:
        st.subheader("⚡ Carnet Individual")
        with st.container(border=True):
            i_nom = st.text_input("👤 Nombre:", key="i_nom")
            i_dni = st.text_input("🆔 DNI:", key="i_dni")
            i_gra = st.text_input("📚 Grado:", key="i_gra")
            i_foto = st.file_uploader("📸 Foto:", type=['jpg', 'png', 'jpeg'], key="i_foto")
            if st.button("👁️ GENERAR", type="primary", use_container_width=True, key="btn_gen_ind"):
                if i_nom and i_dni:
                    with st.spinner("Generando..."):
                        foto_bytes = io.BytesIO(i_foto.getvalue()) if i_foto else None
                        datos = {'alumno': i_nom, 'dni': i_dni, 'grado': i_gra}
                        gen = GeneradorCarnet(datos, config['anio'], foto_bytes)
                        carnet = gen.generar()
                        st.image(carnet, use_container_width=True)
                        st.download_button("⬇️ DESCARGAR", carnet, f"Carnet_{i_dni}.png", "image/png", use_container_width=True, key="btn_desc_ind")
                else:
                    st.error("⚠️ Complete nombre y DNI")
    with col_lote:
        st.subheader("🛒 Generación en Lote")
        with st.expander("➕ Agregar", expanded=True):
            st.session_state.busqueda_counter += 1
            s_dni = st.text_input("🔍 DNI:", key=f"s_dni_{st.session_state.busqueda_counter}")
            if st.button("Buscar", key=f"btn_bus_{st.session_state.busqueda_counter}"):
                resultado = BaseDatos.buscar_por_dni(s_dni)
                if resultado:
                    st.session_state.c_temp_nom = resultado.get('Alumno', '')
                    st.session_state.c_temp_dni = resultado.get('Dni', '')
                    st.session_state.c_temp_gra = resultado.get('Grado', '')
                    st.success("✅ Encontrado")
                    st.rerun()
                else:
                    st.warning("No encontrado")
            c_nom = st.text_input("Nombre:", value=st.session_state.get('c_temp_nom', ''), key=f"c_nom_{st.session_state.busqueda_counter}")
            c_dni = st.text_input("DNI:", value=st.session_state.get('c_temp_dni', ''), key=f"c_dni_{st.session_state.busqueda_counter}")
            c_gra = st.text_input("Grado:", value=st.session_state.get('c_temp_gra', ''), key=f"c_gra_{st.session_state.busqueda_counter}")
            c_foto = st.file_uploader("Foto:", type=['jpg', 'png', 'jpeg'], key=f"c_foto_{st.session_state.busqueda_counter}")
            if st.button("➕ AGREGAR", use_container_width=True, key=f"btn_agr_{st.session_state.busqueda_counter}"):
                if c_nom and c_dni:
                    if c_dni not in [x['dni'] for x in st.session_state.cola_carnets]:
                        item = {'alumno': c_nom, 'dni': c_dni, 'grado': c_gra, 'foto_bytes': c_foto.getvalue() if c_foto else None}
                        st.session_state.cola_carnets.append(item)
                        st.success(f"✅ {c_nom} agregado")
                        st.session_state.c_temp_nom = ""
                        st.session_state.c_temp_dni = ""
                        st.session_state.c_temp_gra = ""
                        st.session_state.busqueda_counter += 1
                        st.rerun()
                    else:
                        st.warning("⚠️ DNI duplicado")
                else:
                    st.error("⚠️ Complete datos")
        st.markdown("---")
        cantidad = len(st.session_state.cola_carnets)
        st.markdown(f"### 📦 Carrito: **{cantidad}** carnets")
        if cantidad > 0:
            df_carrito = pd.DataFrame([{'Alumno': item['alumno'], 'DNI': item['dni'], 'Grado': item['grado']} for item in st.session_state.cola_carnets])
            st.dataframe(df_carrito, use_container_width=True, hide_index=True)
            col_desc, col_vac = st.columns([2, 1])
            with col_desc:
                if st.button("🚀 DESCARGAR ZIP", type="primary", use_container_width=True, key="btn_desc_zip"):
                    with st.spinner("Generando..."):
                        buffer_zip = io.BytesIO()
                        progreso = st.progress(0)
                        with zipfile.ZipFile(buffer_zip, "w") as zf:
                            for i, item in enumerate(st.session_state.cola_carnets):
                                foto_io = io.BytesIO(item['foto_bytes']) if item['foto_bytes'] else None
                                gen = GeneradorCarnet(item, config['anio'], foto_io)
                                carnet = gen.generar()
                                zf.writestr(f"Carnet_{item['dni']}_{item['alumno']}.png", carnet.getvalue())
                                progreso.progress((i + 1) / cantidad)
                        buffer_zip.seek(0)
                        st.balloons()
                        st.download_button("⬇️ GUARDAR ZIP", buffer_zip, f"Pack_Carnets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip", "application/zip", use_container_width=True, key="btn_sav_zip")
            with col_vac:
                if st.button("🗑️ Vaciar", use_container_width=True, key="btn_vac"):
                    st.session_state.cola_carnets = []
                    st.rerun()
        else:
            st.info("Carrito vacío")

def tab_base_datos():
    st.header("📊 Base de Datos")
    df = BaseDatos.cargar()
    if df is not None:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📚 Total", len(df))
        with col2:
            if 'Grado' in df.columns:
                st.metric("🎓 Grados", df['Grado'].nunique())
        with col3:
            if 'Apoderado' in df.columns:
                st.metric("👨‍👩‍👧 Con Apoderado", df['Apoderado'].notna().sum())
        with col4:
            if 'Dni' in df.columns:
                st.metric("🆔 Completos", df['Dni'].notna().sum())
        st.markdown("---")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            if 'Grado' in df.columns:
                grados = ['Todos'] + sorted(df['Grado'].dropna().unique().tolist())
                filtro_grado = st.selectbox("Filtrar por Grado:", grados, key="filtro_g")
        with col_f2:
            busqueda = st.text_input("🔍 Buscar:", key="busq_bd")
        df_filtrado = df.copy()
        if filtro_grado != 'Todos' and 'Grado' in df.columns:
            df_filtrado = df_filtrado[df_filtrado['Grado'] == filtro_grado]
        if busqueda:
            mascara = df_filtrado.apply(lambda row: busqueda.lower() in str(row).lower(), axis=1)
            df_filtrado = df_filtrado[mascara]
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True, height=500)
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Descargar CSV", csv, f"base_datos_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", key="btn_desc_csv")
    else:
        st.warning("⚠️ No hay BD cargada")

def main():
    if st.session_state.rol is None:
        pantalla_login()
        st.stop()
    config = configurar_sidebar()
    if st.session_state.rol == "auxiliar":
        tab1, tab2 = st.tabs(["📋 ASISTENCIAS", "➕ REGISTRAR"])
        with tab1:
            tab_asistencias()
        with tab2:
            st.subheader("➕ Registrar Estudiante")
            nuevo_nombre = st.text_input("Nombre completo:", key="reg_nombre_estudiante")
            nuevo_dni = st.text_input("DNI:", key="reg_dni_estudiante")
            nuevo_grado = st.text_input("Grado:", key="reg_grado_estudiante")
            if st.button("💾 GUARDAR", key="btn_guardar_estudiante"):
                if nuevo_nombre and nuevo_dni and nuevo_grado:
                    BaseDatos.registrar_estudiante(nuevo_nombre, nuevo_dni, nuevo_grado)
                    st.success("✅ Estudiante registrado")
                else:
                    st.error("⚠️ Complete todos los campos")
    elif st.session_state.rol == "directivo":
        tab1, tab2 = st.tabs(["📄 DOCUMENTOS", "🪪 CARNETS"])
        with tab1:
            tab_documentos(config)
        with tab2:
            tab_carnets(config)
    elif st.session_state.rol == "admin":
        tab1, tab2, tab3, tab4 = st.tabs(["📄 DOCUMENTOS", "🪪 CARNETS", "📊 BASE DATOS", "📋 ASISTENCIAS"])
        with tab1:
            tab_documentos(config)
        with tab2:
            tab_carnets(config)
        with tab3:
            tab_base_datos()
        with tab4:
            tab_asistencias()

if __name__ == "__main__":
    main()

