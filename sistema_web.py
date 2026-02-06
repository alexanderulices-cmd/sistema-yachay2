# ========================================
# SISTEMA YACHAY PRO - VERSIÓN COMPLETA FUNCIONAL
# ========================================
# Sistema completo de gestión educativa
# Módulos: Matrícula, Documentos, Carnets, Asistencia QR, Corrector Exámenes
# ========================================

import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
import qrcode
import os
from datetime import datetime
import io
from PIL import Image, ImageDraw, ImageFont
import textwrap
import zipfile
import time
from pathlib import Path
import json
import urllib.parse
import numpy as np

st.set_page_config(page_title="SISTEMA YACHAY PRO", page_icon="🎓", layout="wide")

# ========================================
# INICIALIZACIÓN
# ========================================

def init_session_state():
    defaults = {
        'rol': None,
        'cola_carnets': [],
        'alumno': '', 'dni': '', 'grado': '',
        'apoderado': '', 'dni_apo': '',
        'c_temp_nom': '', 'c_temp_dni': '', 'c_temp_gra': '', 'c_temp_cel': '',
        'busqueda_counter': 0,
        'registro_counter': 0,
        'asistencias_dia': [],
        'tipo_asistencia': 'Entrada',
        'ultimo_dni_escaneado': '',
        'matricula_data': {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Estilos CSS
st.markdown("""
<style>
.main-header {
    text-align:center; padding:2rem;
    background:linear-gradient(135deg,#001e7c 0%,#0052cc 100%);
    color:white; border-radius:10px; margin-bottom:2rem;
    box-shadow:0 4px 6px rgba(0,0,0,0.1);
}
.scanner-box {
    border: 3px solid #0052cc; border-radius: 10px;
    padding: 1.5rem; background: #f0f4ff;
}
.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem; border-radius: 10px; color: white; text-align: center;
}
.success-box {
    background: #d4edda; border: 2px solid #28a745;
    border-radius: 10px; padding: 1rem; margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Importaciones opcionales
try:
    from barcode import Code128
    from barcode.writer import ImageWriter
    HAS_BARCODE = True
except ImportError:
    HAS_BARCODE = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    from pyzbar.pyzbar import decode as pyzbar_decode
    HAS_PYZBAR = True
except ImportError:
    HAS_PYZBAR = False

# ========================================
# CONSTANTES DE GRADOS
# ========================================

NIVELES_GRADOS = {
    "INICIAL": ["Inicial 3 años", "Inicial 4 años", "Inicial 5 años"],
    "PRIMARIA": ["1° Primaria", "2° Primaria", "3° Primaria", "4° Primaria", "5° Primaria", "6° Primaria"],
    "SECUNDARIA": ["1° Secundaria", "2° Secundaria", "3° Secundaria", "4° Secundaria", "5° Secundaria"]
}

SECCIONES = ["Única", "A", "B"]

TODOS_LOS_GRADOS = []
for nivel, grados in NIVELES_GRADOS.items():
    for grado in grados:
        TODOS_LOS_GRADOS.append(grado)

MESES_ASISTENCIA = ["Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                     "Septiembre", "Octubre", "Noviembre", "Diciembre"]

MESES_ESP = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

# ========================================
# FUENTES
# ========================================

class RecursoManager:
    @staticmethod
    def obtener_fuente(nombre, tamaño, bold=False):
        try:
            # Intentar fuentes del sistema
            posibles = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "Roboto-Bold.ttf" if bold else "Roboto-Regular.ttf",
            ]
            for f in posibles:
                if Path(f).exists():
                    return ImageFont.truetype(f, int(tamaño))
            return ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()

# ========================================
# BASE DE DATOS
# ========================================

ARCHIVO_BD = "base_datos.xlsx"
ARCHIVO_MATRICULA = "matricula.xlsx"
ARCHIVO_ASISTENCIAS = "asistencias.json"

class BaseDatos:

    @staticmethod
    def cargar_matricula():
        """Carga la base de datos de matrícula"""
        try:
            if Path(ARCHIVO_MATRICULA).exists():
                df = pd.read_excel(ARCHIVO_MATRICULA, dtype=str, engine='openpyxl')
                df.columns = df.columns.str.strip()
                return df
            return pd.DataFrame(columns=[
                'Nombre', 'DNI', 'Nivel', 'Grado', 'Seccion',
                'Apoderado', 'DNI_Apoderado', 'Celular_Apoderado'
            ])
        except Exception:
            return pd.DataFrame(columns=[
                'Nombre', 'DNI', 'Nivel', 'Grado', 'Seccion',
                'Apoderado', 'DNI_Apoderado', 'Celular_Apoderado'
            ])

    @staticmethod
    def guardar_matricula(df):
        """Guarda la base de datos de matrícula"""
        df.to_excel(ARCHIVO_MATRICULA, index=False, engine='openpyxl')

    @staticmethod
    def registrar_estudiante(datos):
        """Registra un nuevo estudiante en matrícula"""
        df = BaseDatos.cargar_matricula()
        # Verificar si el DNI ya existe
        if not df.empty and datos['DNI'] in df['DNI'].values:
            # Actualizar datos existentes
            idx = df[df['DNI'] == datos['DNI']].index[0]
            for key, value in datos.items():
                df.at[idx, key] = value
        else:
            nuevo = pd.DataFrame([datos])
            df = pd.concat([df, nuevo], ignore_index=True)
        BaseDatos.guardar_matricula(df)
        return True

    @staticmethod
    def buscar_por_dni(dni):
        """Busca estudiante por DNI en matrícula"""
        df = BaseDatos.cargar_matricula()
        if df is not None and not df.empty and 'DNI' in df.columns:
            dni = str(dni).strip()
            df['DNI'] = df['DNI'].astype(str).str.strip()
            resultado = df[df['DNI'] == dni]
            if not resultado.empty:
                return resultado.iloc[0].to_dict()
        # Buscar también en base_datos.xlsx legacy
        try:
            if Path(ARCHIVO_BD).exists():
                df2 = pd.read_excel(ARCHIVO_BD, dtype=str, engine='openpyxl')
                df2.columns = df2.columns.str.strip().str.title()
                if 'Dni' in df2.columns:
                    df2['Dni'] = df2['Dni'].astype(str).str.strip()
                    res = df2[df2['Dni'] == str(dni).strip()]
                    if not res.empty:
                        row = res.iloc[0].to_dict()
                        return {
                            'Nombre': row.get('Alumno', row.get('Nombre', '')),
                            'DNI': row.get('Dni', ''),
                            'Grado': row.get('Grado', ''),
                            'Nivel': row.get('Nivel', ''),
                            'Seccion': row.get('Seccion', ''),
                            'Apoderado': row.get('Apoderado', ''),
                            'DNI_Apoderado': row.get('Dni_Apoderado', row.get('Dni Apoderado', '')),
                            'Celular_Apoderado': row.get('Celular', row.get('Celular_Apoderado', ''))
                        }
        except Exception:
            pass
        return None

    @staticmethod
    def eliminar_estudiante(dni):
        """Elimina estudiante por DNI"""
        df = BaseDatos.cargar_matricula()
        df['DNI'] = df['DNI'].astype(str).str.strip()
        df = df[df['DNI'] != str(dni).strip()]
        BaseDatos.guardar_matricula(df)
        return True

    @staticmethod
    def guardar_asistencia(dni, nombre, tipo, hora):
        """Guarda registro de asistencia"""
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        if Path(ARCHIVO_ASISTENCIAS).exists():
            with open(ARCHIVO_ASISTENCIAS, 'r', encoding='utf-8') as f:
                asistencias = json.load(f)
        else:
            asistencias = {}
        if fecha_hoy not in asistencias:
            asistencias[fecha_hoy] = {}
        if dni not in asistencias[fecha_hoy]:
            asistencias[fecha_hoy][dni] = {'nombre': nombre, 'entrada': '', 'salida': ''}

        if tipo == 'entrada':
            asistencias[fecha_hoy][dni]['entrada'] = hora
        else:
            asistencias[fecha_hoy][dni]['salida'] = hora
        asistencias[fecha_hoy][dni]['nombre'] = nombre

        with open(ARCHIVO_ASISTENCIAS, 'w', encoding='utf-8') as f:
            json.dump(asistencias, f, indent=2, ensure_ascii=False)
        return True

    @staticmethod
    def obtener_asistencias_hoy():
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        if Path(ARCHIVO_ASISTENCIAS).exists():
            with open(ARCHIVO_ASISTENCIAS, 'r', encoding='utf-8') as f:
                asistencias = json.load(f)
            return asistencias.get(fecha_hoy, {})
        return {}

    @staticmethod
    def obtener_estadisticas():
        df = BaseDatos.cargar_matricula()
        if df is not None and not df.empty:
            return {
                'total_alumnos': len(df),
                'grados': df['Grado'].nunique() if 'Grado' in df.columns else 0,
                'con_apoderado': df['Apoderado'].notna().sum() if 'Apoderado' in df.columns else 0
            }
        return {'total_alumnos': 0, 'grados': 0, 'con_apoderado': 0}


# ========================================
# GENERADOR DE PDFs
# ========================================

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
        self.canvas.setFont("Helvetica-Oblique", 11)
        self.canvas.drawCentredString(self.width / 2, self.config['y_frase'],
                                      f'"{self.config["frase"]}"')
        self.canvas.setFont("Helvetica", 11)
        fecha = self._obtener_fecha_espanol()
        self.canvas.drawRightString(self.width - 60, self.config['y_frase'] - 25, fecha)
        self.canvas.setFont("Helvetica-Bold", 16)
        self.canvas.drawCentredString(self.width / 2, self.config['y_titulo'], titulo)
        self.canvas.setLineWidth(1)
        self.canvas.line(100, self.config['y_titulo'] - 5,
                         self.width - 100, self.config['y_titulo'] - 5)

    def _obtener_fecha_espanol(self):
        hoy = datetime.now()
        return f"Chinchero, {hoy.day} de {MESES_ESP[hoy.month - 1]} de {self.config['anio']}"

    def _dibujar_parrafo(self, texto, x, y, ancho, estilo):
        p = Paragraph(texto, estilo)
        w, h = p.wrap(ancho, 600)
        p.drawOn(self.canvas, x, y - h)
        return y - h - 15

    def _agregar_qr(self, datos_alumno, tipo_doc):
        data_qr = (
            f"I.E. ALTERNATIVO YACHAY\n"
            f"DOCUMENTO: {tipo_doc}\n"
            f"ESTUDIANTE: {datos_alumno.get('alumno', datos_alumno.get('Nombre', ''))}\n"
            f"DNI: {datos_alumno.get('dni', datos_alumno.get('DNI', ''))}\n"
            f"FECHA: {datetime.now().strftime('%d/%m/%Y')}"
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
        self.canvas.drawCentredString(self.config['qr_x'] + 35, self.config['qr_y'] - 5,
                                      "CÓDIGO DE VERIFICACIÓN")
        try:
            os.remove(temp_qr)
        except:
            pass

    def _agregar_solicitante(self, datos, y):
        apoderado = datos.get('apoderado', datos.get('Apoderado', ''))
        dni_apo = datos.get('dni_apo', datos.get('DNI_Apoderado', ''))
        texto = (
            f"Se expide el presente documento a solicitud del Padre/Madre "
            f"<b>{apoderado.upper()}</b> con DNI N° <b>{dni_apo}</b>."
        )
        estilo = ParagraphStyle('Solicitud', parent=self.styles['Normal'],
                                fontSize=10, leading=14, alignment=TA_JUSTIFY)
        return self._dibujar_parrafo(texto, 60, y, self.width - 120, estilo)

    def _agregar_firmas(self):
        yf = 110
        self.canvas.line(200, yf, 395, yf)
        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawCentredString(self.width / 2, yf - 15,
                                      self.config['directora'].upper())
        self.canvas.setFont("Helvetica", 9)
        self.canvas.drawCentredString(self.width / 2, yf - 28, "DIRECTORA")

    def _finalizar(self):
        self.canvas.save()
        self.buffer.seek(0)
        return self.buffer

    # ---- DOCUMENTOS ----

    def generar_constancia_vacante(self, datos):
        self._aplicar_fondo()
        self._dibujar_encabezado("CONSTANCIA DE VACANTE")
        y = self.config['y_titulo'] - 50
        mx, ancho = 60, self.width - 120
        estilo = ParagraphStyle('Normal', parent=self.styles['Normal'],
                                fontSize=11, leading=15, alignment=TA_JUSTIFY)
        estilo_lista = ParagraphStyle('Lista', parent=estilo, leftIndent=25)

        y = self._dibujar_parrafo(
            "La Dirección de la Institución Educativa Particular ALTERNATIVO YACHAY de Chinchero, "
            "debidamente representada por su Directora, suscribe la presente:", mx, y, ancho, estilo)

        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "CONSTANCIA DE VACANTE")
        y -= 25

        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        dni = datos.get('dni', datos.get('DNI', ''))
        grado = datos.get('grado', datos.get('Grado', '')).upper()

        texto = (
            f"Que, mediante el presente documento se hace constar que la Institución Educativa cuenta "
            f"con <b>VACANTE DISPONIBLE</b> en el nivel de {grado}, para el/la estudiante "
            f"<b>{alumno}</b>, identificado(a) con DNI N° <b>{dni}</b>, "
            f"correspondiente al año escolar <b>{self.config['anio']}</b>."
        )
        y = self._dibujar_parrafo(texto, mx, y, ancho, estilo)

        y = self._dibujar_parrafo(
            "Asimismo, para efectos de formalizar la matrícula, el/la solicitante deberá presentar "
            "la siguiente documentación:", mx, y, ancho, estilo)

        requisitos = [
            "• Certificado Oficial de Estudios (original).",
            "• Resolución Directoral de Traslado de Matrícula.",
            "• Libreta de Notas del Sistema SIAGIE.",
            "• Ficha Única de Matrícula del Sistema SIAGIE.",
            "• Copia del DNI del estudiante.",
            "• Constancia de No Adeudo de la institución de procedencia.",
            "• Folder o mica transparente."
        ]
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
        estilo = ParagraphStyle('Normal', parent=self.styles['Normal'],
                                fontSize=11, leading=15, alignment=TA_JUSTIFY)

        y = self._dibujar_parrafo(
            "La Dirección de la Institución Educativa Particular ALTERNATIVO YACHAY, "
            "debidamente representada por su Directora:", mx, y, ancho, estilo)

        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "HACE CONSTAR:")
        y -= 25

        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        dni = datos.get('dni', datos.get('DNI', ''))

        texto = (
            f"Que el/la estudiante <b>{alumno}</b>, identificado(a) con DNI "
            f"N° <b>{dni}</b>, ha cumplido satisfactoriamente con todas sus "
            f"obligaciones económicas ante esta Institución Educativa, no registrando deuda alguna."
        )
        y = self._dibujar_parrafo(texto, mx, y, ancho, estilo)
        y = self._agregar_solicitante(datos, y)
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE NO ADEUDO")
        return self._finalizar()

    def generar_constancia_estudios(self, datos):
        self._aplicar_fondo()
        self._dibujar_encabezado("CONSTANCIA DE ESTUDIOS")
        y = self.config['y_titulo'] - 50
        mx, ancho = 60, self.width - 120
        estilo = ParagraphStyle('Normal', parent=self.styles['Normal'],
                                fontSize=11, leading=15, alignment=TA_JUSTIFY)

        y = self._dibujar_parrafo(
            "La Dirección de la Institución Educativa Particular ALTERNATIVO YACHAY, "
            "debidamente representada por su Directora:", mx, y, ancho, estilo)

        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "HACE CONSTAR:")
        y -= 25

        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        dni = datos.get('dni', datos.get('DNI', ''))
        grado = datos.get('grado', datos.get('Grado', '')).upper()

        texto = (
            f"Que el/la estudiante <b>{alumno}</b>, identificado(a) con DNI "
            f"N° <b>{dni}</b>, se encuentra <b>DEBIDAMENTE MATRICULADO(A)</b> "
            f"en esta Institución Educativa para el año académico <b>{self.config['anio']}</b>, "
            f"cursando estudios en el nivel de <b>{grado}</b>."
        )
        y = self._dibujar_parrafo(texto, mx, y, ancho, estilo)
        y = self._agregar_solicitante(datos, y)
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE ESTUDIOS")
        return self._finalizar()

    def generar_constancia_conducta(self, datos):
        self._aplicar_fondo()
        self._dibujar_encabezado("CONSTANCIA DE CONDUCTA")
        y = self.config['y_titulo'] - 50
        mx, ancho = 60, self.width - 120
        estilo = ParagraphStyle('Normal', parent=self.styles['Normal'],
                                fontSize=10, leading=14, alignment=TA_JUSTIFY)

        y = self._dibujar_parrafo(
            "La Dirección de la Institución Educativa Particular ALTERNATIVO YACHAY, "
            "debidamente representada por su Directora:", mx, y, ancho, estilo)

        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "CERTIFICA:")
        y -= 25

        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        dni = datos.get('dni', datos.get('DNI', ''))

        texto = (
            f"Que el/la estudiante <b>{alumno}</b>, identificado(a) con DNI N° <b>{dni}</b>, "
            f"cursó estudios en esta institución, obteniendo las siguientes calificaciones en <b>CONDUCTA</b>:"
        )
        y = self._dibujar_parrafo(texto, mx, y, ancho, estilo)

        y -= 15
        tx = self.width / 2 - 200
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
            nota = datos.get(f'nota_conducta_{i + 1}', 'AD')
            self.canvas.drawString(tx, y, grado)
            self.canvas.drawString(tx + 120, y, str(anio_base + i + 1))
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
        estilo = ParagraphStyle('Compromiso', parent=self.styles['Normal'],
                                fontSize=8.5, leading=11, alignment=TA_JUSTIFY)

        apoderado = datos.get('apoderado', datos.get('Apoderado', '')).upper()
        dni_apo = datos.get('dni_apo', datos.get('DNI_Apoderado', ''))
        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        grado = datos.get('grado', datos.get('Grado', '')).upper()

        intro = (
            f"Yo, <b>{apoderado}</b>, con DNI N° <b>{dni_apo}</b>, "
            f"padre/madre/apoderado(a) de <b>{alumno}</b>, estudiante del "
            f"<b>{grado}</b>, me comprometo formalmente a cumplir:"
        )
        y = self._dibujar_parrafo(intro, mx, y, ancho, estilo)
        y -= 5

        compromisos = [
            "1. Velar por la asistencia puntual y regular de mi hijo(a).",
            "2. Supervisar el cumplimiento diario de tareas escolares.",
            "3. Asegurar que asista correctamente uniformado(a).",
            "4. Inculcar respeto hacia docentes, personal y compañeros.",
            "5. Participar en actividades del comité de aula.",
            "6. Ejercer crianza positiva, libre de violencia.",
            "7. Atender oportunamente problemas de conducta o rendimiento.",
            "8. Asumir responsabilidad por daños materiales.",
            "9. Vigilar vocabulario apropiado y conducta respetuosa.",
            "10. Acudir cuando sea requerida mi presencia.",
            "11. Asistir puntualmente a reuniones y citaciones.",
            "12. Justificar inasistencias oportunamente (24 horas).",
            "13. Cumplir con el pago de pensiones de enseñanza.",
            "14. Respetar la autonomía pedagógica."
        ]
        estilo_item = ParagraphStyle('Item', parent=estilo, leftIndent=10)
        for c in compromisos:
            y = self._dibujar_parrafo(c, mx, y, ancho, estilo_item)
            y += 2

        y -= 5
        y = self._dibujar_parrafo(
            "Declaro conocer y aceptar el estricto cumplimiento de lo establecido.",
            mx, y, ancho, estilo)

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

    def generar_resolucion_traslado(self, datos):
        self._aplicar_fondo()
        self.canvas.setFont("Helvetica-Oblique", 11)
        self.canvas.drawCentredString(self.width / 2, 700, f'"{self.config["frase"]}"')
        y = 670
        self.canvas.setFont("Helvetica-Bold", 14)
        self.canvas.drawCentredString(self.width / 2, y,
                                      f"RESOLUCIÓN DIRECTORAL N° {datos.get('num_resolucion', '')}")
        y -= 30
        self.canvas.setFont("Helvetica", 11)
        self.canvas.drawCentredString(self.width / 2, y,
                                      datos.get('fecha_resolucion', self._obtener_fecha_espanol()))
        y -= 40
        mx, ancho = 60, self.width - 120
        estilo = ParagraphStyle('Normal', parent=self.styles['Normal'],
                                fontSize=11, leading=15, alignment=TA_JUSTIFY)

        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawString(mx, y, "VISTO:")
        y -= 20
        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        nivel = datos.get('nivel', '').upper()
        y = self._dibujar_parrafo(
            f"La solicitud del(a) apoderado(a), de <b>{alumno}</b> y el informe "
            f"de progreso de <b>{nivel}</b>.", mx, y, ancho, estilo)

        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawString(mx, y, "CONSIDERANDO:")
        y -= 20
        y = self._dibujar_parrafo(
            "Que, es procedente autorizar el traslado de matrícula de educandos cuyos padres o "
            "apoderados lo soliciten, a fin de garantizar la continuidad de estudios.",
            mx, y, ancho, estilo)
        y = self._dibujar_parrafo(
            "De conformidad con lo dispuesto por Ley de Educación N°28044, la RM 474-2022 MINEDU.",
            mx, y, ancho, estilo)

        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawString(mx, y, "SE RESUELVE:")
        y -= 20

        tabla_data = [
            ['APELLIDOS Y NOMBRE', alumno],
            ['NIVEL', nivel],
            ['IE PROCEDENCIA', 'IEP ALTERNATIVO YACHAY'],
            ['CÓDIGO DE LA IE', '1398841-0'],
            ['IE DE DESTINO', datos.get('ie_destino', '').upper()],
            ['APTO PARA CONTINUAR EN', datos.get('nivel_destino', '').upper()]
        ]
        tabla = Table(tabla_data, colWidths=[200, 280])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        tabla.wrapOn(self.canvas, ancho, 200)
        tabla.drawOn(self.canvas, mx, y - 110)

        y -= 150
        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawCentredString(self.width / 2, y, "REGISTRE Y COMUNÍQUESE")
        self._agregar_firmas()
        self._agregar_qr(datos, "RESOLUCIÓN DE TRASLADO")
        return self._finalizar()


# ========================================
# GENERADOR DE REGISTRO DE NOTAS PDF (ESTILO MINEDU)
# ========================================

def generar_registro_notas_pdf(grado, seccion, anio, estudiantes_df):
    """Genera registro de notas estilo MINEDU en PDF landscape"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    w, h = landscape(A4)

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w / 2, h - 30, "I.E.P. ALTERNATIVO YACHAY - REGISTRO DE EVALUACIÓN")
    c.setFont("Helvetica", 10)
    c.drawCentredString(w / 2, h - 45, f"Grado: {grado} | Sección: {seccion} | Año: {anio}")
    c.drawCentredString(w / 2, h - 58, '"EDUCAR PARA LA VIDA"')

    # Columnas: N°, Nombre, DNI, luego áreas con Bimestres 1-4 y Promedio
    areas_cortas = ["MAT", "COM", "CT", "PS", "EF", "ART", "ING", "REL", "TUT"]
    areas_nombres = ["Matemática", "Comunicación", "Ciencia y Tec.", "Personal Social",
                     "Educación Física", "Arte y Cultura", "Inglés", "Religión", "Tutoría"]

    # Header row
    header = ["N°", "APELLIDOS Y NOMBRES", "DNI"]
    for area in areas_cortas:
        for b in ["B1", "B2", "B3", "B4"]:
            header.append(f"{area}\n{b}")
        header.append(f"{area}\nPF")

    num_estudiantes = len(estudiantes_df) if not estudiantes_df.empty else 15
    data = [header]

    if not estudiantes_df.empty:
        for idx, row in estudiantes_df.iterrows():
            fila = [str(idx + 1), row.get('Nombre', ''), row.get('DNI', '')]
            for _ in areas_cortas:
                fila.extend(["", "", "", "", ""])  # B1-B4 + PF vacíos
            data.append(fila)
    else:
        for i in range(15):
            fila = [str(i + 1), "", ""]
            for _ in areas_cortas:
                fila.extend(["", "", "", "", ""])
            data.append(fila)

    # Calcular anchos
    col_widths = [25, 160, 65]
    for _ in areas_cortas:
        col_widths.extend([18, 18, 18, 18, 20])

    tabla = Table(data, colWidths=col_widths, repeatRows=1)
    estilo_tabla = [
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 5),
        ('FONTSIZE', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0, 0.2, 0.5)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 1)]),
    ]

    # Colorear encabezados de áreas
    col_idx = 3
    area_colors = [
        colors.Color(0.8, 0.9, 1), colors.Color(0.9, 1, 0.9),
        colors.Color(1, 0.95, 0.8), colors.Color(1, 0.9, 0.9),
        colors.Color(0.9, 0.9, 1), colors.Color(1, 0.9, 1),
        colors.Color(0.85, 1, 1), colors.Color(1, 1, 0.85),
        colors.Color(0.95, 0.95, 0.95)
    ]
    for i, area in enumerate(areas_cortas):
        for j in range(5):
            estilo_tabla.append(('BACKGROUND', (col_idx + j, 0), (col_idx + j, 0),
                                 colors.Color(0, 0.2, 0.5)))
        col_idx += 5

    tabla.setStyle(TableStyle(estilo_tabla))

    tabla_w, tabla_h = tabla.wrap(w - 40, h - 100)
    tabla.drawOn(c, 20, h - 75 - tabla_h)

    c.setFont("Helvetica", 7)
    c.drawString(20, 20, f"Generado por Sistema YACHAY PRO - {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    c.save()
    buffer.seek(0)
    return buffer


# ========================================
# GENERADOR DE REGISTRO DE ASISTENCIA PDF
# ========================================

def generar_registro_asistencia_pdf(grado, seccion, anio, estudiantes_df):
    """Genera registro de asistencia mensual estilo MINEDU (Marzo a Diciembre)"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    w, h = landscape(A4)

    for mes_idx, mes in enumerate(MESES_ASISTENCIA):
        if mes_idx > 0:
            c.showPage()

        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(w / 2, h - 25, "I.E.P. ALTERNATIVO YACHAY - REGISTRO DE ASISTENCIA")
        c.setFont("Helvetica", 9)
        c.drawCentredString(w / 2, h - 40,
                            f"Grado: {grado} | Sección: {seccion} | Mes: {mes} | Año: {anio}")

        # Header: N°, Nombre, días 1-31
        header = ["N°", "APELLIDOS Y NOMBRES"]
        dias_en_mes = 31
        for d in range(1, dias_en_mes + 1):
            header.append(str(d))
        header.extend(["A", "T", "F", "J"])  # Asistencias, Tardanzas, Faltas, Justificadas

        data = [header]

        num_est = len(estudiantes_df) if not estudiantes_df.empty else 20
        if not estudiantes_df.empty:
            for idx, row in estudiantes_df.iterrows():
                fila = [str(idx + 1), row.get('Nombre', '')]
                fila.extend([""] * dias_en_mes)
                fila.extend(["", "", "", ""])
                data.append(fila)
        else:
            for i in range(20):
                fila = [str(i + 1), ""]
                fila.extend([""] * dias_en_mes)
                fila.extend(["", "", "", ""])
                data.append(fila)

        col_widths = [20, 130]
        col_widths.extend([17] * dias_en_mes)
        col_widths.extend([20, 20, 20, 20])

        tabla = Table(data, colWidths=col_widths, repeatRows=1)
        tabla.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 5.5),
            ('FONTSIZE', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0, 0.3, 0.15)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 1, 0.95)]),
            # Resumen columnas
            ('BACKGROUND', (-4, 0), (-1, 0), colors.Color(0.6, 0, 0)),
        ]))

        tabla_w, tabla_h = tabla.wrap(w - 30, h - 80)
        tabla.drawOn(c, 15, h - 55 - tabla_h)

        c.setFont("Helvetica", 6)
        c.drawString(15, 12, "A=Asistió | T=Tardanza | F=Falta | J=Justificada")
        c.drawRightString(w - 15, 12, f"Sistema YACHAY PRO - {anio}")

    c.save()
    buffer.seek(0)
    return buffer


# ========================================
# GENERADOR DE CARNETS
# ========================================

class GeneradorCarnet:
    WIDTH = 1012
    HEIGHT = 638
    AZUL = (0, 30, 120)
    DORADO = (255, 215, 0)

    def __init__(self, datos, anio, foto_bytes=None):
        self.datos = datos
        self.anio = anio
        self.foto_bytes = foto_bytes
        self.img = Image.new('RGB', (self.WIDTH, self.HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.img)

    def _dibujar_barras(self):
        self.draw.rectangle([(0, 0), (self.WIDTH, 220)], fill=self.AZUL)
        self.draw.rectangle([(0, 215), (self.WIDTH, 222)], fill=self.DORADO)
        self.draw.rectangle([(0, self.HEIGHT - 180), (self.WIDTH, self.HEIGHT)], fill=self.AZUL)
        self.draw.rectangle([(0, self.HEIGHT - 182), (self.WIDTH, self.HEIGHT - 177)], fill=self.DORADO)

    def _dibujar_textos(self):
        font_h = RecursoManager.obtener_fuente("", 38, bold=True)
        font_m = RecursoManager.obtener_fuente("", 22, bold=True)
        self.draw.text((self.WIDTH // 2, 80), "I.E. ALTERNATIVO YACHAY",
                       font=font_h, fill="white", anchor="mm")
        self.draw.text((self.WIDTH // 2, 130), '"EDUCAR PARA LA VIDA"',
                       font=font_m, fill=self.DORADO, anchor="mm")
        self.draw.text((self.WIDTH // 2, 175), f"CARNET ESCOLAR {self.anio}",
                       font=RecursoManager.obtener_fuente("", 20, bold=True),
                       fill="white", anchor="mm")

    def _insertar_foto(self):
        x, y_pos, w_f, h_f = 40, 240, 240, 300
        if self.foto_bytes:
            try:
                foto = Image.open(self.foto_bytes).convert("RGB").resize((w_f, h_f), Image.LANCZOS)
                self.img.paste(foto, (x, y_pos))
            except Exception:
                self._placeholder(x, y_pos, w_f, h_f)
        else:
            self._placeholder(x, y_pos, w_f, h_f)
        self.draw.rectangle([(x - 3, y_pos - 3), (x + w_f + 3, y_pos + h_f + 3)],
                            outline=self.DORADO, width=4)

    def _placeholder(self, x, y, w, h):
        self.draw.rectangle([(x, y), (x + w, y + h)], fill="#eeeeee")
        font = RecursoManager.obtener_fuente("", 18)
        self.draw.text((x + w // 2, y + h // 2), "SIN FOTO", font=font, fill="#999", anchor="mm")

    def _dibujar_datos(self):
        x_t = 310
        nombre = self.datos.get('alumno', self.datos.get('Nombre', '')).upper()
        dni = self.datos.get('dni', self.datos.get('DNI', ''))
        grado = self.datos.get('grado', self.datos.get('Grado', 'N/A')).upper()

        font_n = RecursoManager.obtener_fuente("", 22 if len(nombre) > 22 else 26, bold=True)
        font_l = RecursoManager.obtener_fuente("", 16, bold=True)
        font_d = RecursoManager.obtener_fuente("", 16)

        # Nombre (con wrap si es largo)
        y_cursor = 250
        if len(nombre) > 28:
            wrapper = textwrap.TextWrapper(width=28)
            for linea in wrapper.wrap(nombre)[:2]:
                self.draw.text((x_t, y_cursor), linea, font=font_n, fill="black")
                y_cursor += 30
        else:
            self.draw.text((x_t, y_cursor), nombre, font=font_n, fill="black")
            y_cursor += 35

        y_cursor += 10
        self.draw.text((x_t, y_cursor), "DNI:", font=font_l, fill="black")
        self.draw.text((x_t + 60, y_cursor), str(dni), font=font_d, fill="black")

        y_cursor += 35
        self.draw.text((x_t, y_cursor), "GRADO:", font=font_l, fill="black")
        self.draw.text((x_t + 100, y_cursor), grado, font=font_d, fill="black")

        y_cursor += 35
        seccion = self.datos.get('seccion', self.datos.get('Seccion', ''))
        if seccion:
            self.draw.text((x_t, y_cursor), "SECCIÓN:", font=font_l, fill="black")
            self.draw.text((x_t + 120, y_cursor), str(seccion), font=font_d, fill="black")
            y_cursor += 35

        self.draw.text((x_t, y_cursor), "VIGENCIA:", font=font_l, fill="black")
        self.draw.text((x_t + 130, y_cursor), str(self.anio), font=font_d, fill="black")

        # Texto inferior
        font_s = RecursoManager.obtener_fuente("", 14, bold=True)
        self.draw.text((self.WIDTH // 2, self.HEIGHT - 120), "EDUCAR PARA LA VIDA",
                       font=font_s, fill="white", anchor="mm")

    def _agregar_qr(self):
        """QR con solo el DNI para escaneo de asistencia"""
        try:
            dni = str(self.datos.get('dni', self.datos.get('DNI', '')))
            qr = qrcode.QRCode(box_size=8, border=1)
            qr.add_data(dni)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="black", back_color="white")
            img_qr = img_qr.resize((150, 150), Image.LANCZOS)
            x_qr = self.WIDTH - 190
            y_qr = 250
            self.img.paste(img_qr, (x_qr, y_qr))
            font_s = RecursoManager.obtener_fuente("", 10, bold=True)
            self.draw.text((x_qr + 75, y_qr + 155), "ESCANEAR QR", font=font_s, fill="black", anchor="mm")
        except Exception:
            pass

    def _agregar_barcode(self):
        """Código de barras con solo el DNI"""
        if not HAS_BARCODE:
            return
        try:
            dni = str(self.datos.get('dni', self.datos.get('DNI', '')))
            writer = ImageWriter()
            buf = io.BytesIO()
            Code128(dni, writer=writer).write(buf, options={
                'write_text': True, 'text_distance': 2, 'font_size': 20,
                'module_width': 0.4, 'module_height': 12
            })
            buf.seek(0)
            img_bar = Image.open(buf).resize((350, 70), Image.LANCZOS)
            x_bar = (self.WIDTH - 350) // 2
            y_bar = self.HEIGHT - 165
            self.img.paste(img_bar, (x_bar, y_bar))
        except Exception:
            pass

    def generar(self):
        self._dibujar_barras()
        self._dibujar_textos()
        self._insertar_foto()
        self._dibujar_datos()
        self._agregar_qr()
        self._agregar_barcode()
        output = io.BytesIO()
        self.img.save(output, format='PNG', optimize=True, quality=95)
        output.seek(0)
        return output


# ========================================
# FUNCIONES DE UTILIDAD
# ========================================

def generar_link_whatsapp(telefono, mensaje):
    """Genera link de WhatsApp Web/App"""
    tel = str(telefono).strip().replace("+", "").replace(" ", "")
    if not tel.startswith("51"):
        tel = "51" + tel
    msg = urllib.parse.quote(mensaje)
    return f"https://wa.me/{tel}?text={msg}"


def generar_mensaje_asistencia(nombre, tipo, hora):
    saludo = "Buenos días" if int(hora.split(':')[0]) < 12 else "Buenas tardes"
    if tipo == "entrada":
        return (f"{saludo}\n🏫 I.E. ALTERNATIVO YACHAY informa:\n"
                f"✅ *ENTRADA* registrada\n👤 {nombre}\n🕒 Hora: {hora}\n"
                f"💡 Su hijo(a) ingresó al colegio.")
    else:
        return (f"{saludo}\n🏫 I.E. ALTERNATIVO YACHAY informa:\n"
                f"🏁 *SALIDA* registrada\n👤 {nombre}\n🕒 Hora: {hora}\n"
                f"👋 Su hijo(a) salió del colegio.")


def decodificar_qr_imagen(image_bytes):
    """Decodifica QR/barcode de una imagen capturada"""
    if not HAS_PYZBAR:
        return None
    try:
        img = Image.open(io.BytesIO(image_bytes))
        codigos = pyzbar_decode(img)
        if codigos:
            return codigos[0].data.decode('utf-8')
    except Exception:
        pass

    # Intentar con OpenCV si disponible
    if HAS_CV2:
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            # Intentar con diferentes procesamientos
            for thresh_method in [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV]:
                _, thresh = cv2.threshold(gray, 127, 255, thresh_method)
                pil_img = Image.fromarray(thresh)
                codigos = pyzbar_decode(pil_img)
                if codigos:
                    return codigos[0].data.decode('utf-8')
        except Exception:
            pass
    return None


# ========================================
# PANTALLA DE LOGIN
# ========================================

def pantalla_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='main-header'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color:white;margin:0;'>🎓 SISTEMA YACHAY PRO</h1>",
                    unsafe_allow_html=True)
        st.markdown("<p style='color:white;'>Sistema Integral de Gestión Educativa</p>",
                    unsafe_allow_html=True)
        st.markdown("<p style='color:#FFD700;font-style:italic;'>\"Educar para la Vida\"</p>",
                    unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        pwd = st.text_input("🔑 Contraseña de acceso:", type="password", key="login_pwd")
        if st.button("🔐 INGRESAR AL SISTEMA", use_container_width=True, type="primary"):
            if pwd == "306020":
                st.session_state.rol = "admin"
                st.rerun()
            elif pwd == "deyanira":
                st.session_state.rol = "directivo"
                st.rerun()
            elif pwd == "123456789":
                st.session_state.rol = "auxiliar"
                st.rerun()
            else:
                st.error("⛔ Contraseña incorrecta")


# ========================================
# SIDEBAR
# ========================================

def configurar_sidebar():
    with st.sidebar:
        st.title("🎓 YACHAY PRO")
        rol_emoji = {"admin": "⚙️ Admin", "directivo": "📋 Directivo", "auxiliar": "👤 Auxiliar"}
        st.info(f"**Sesión:** {rol_emoji.get(st.session_state.rol, '🔐')}")
        st.markdown("---")

        if st.session_state.rol == "admin":
            with st.expander("📂 Archivos", expanded=False):
                up_bd = st.file_uploader("📊 Base Datos (.xlsx)", type=["xlsx"], key="upload_bd")
                if up_bd:
                    with open(ARCHIVO_BD, "wb") as f:
                        f.write(up_bd.getbuffer())
                    st.success("✅ BD actualizada")
                    time.sleep(0.5)
                    st.rerun()
                up_fondo = st.file_uploader("🖼️ Fondo docs (.png)", type=["png"], key="upload_fondo")
                if up_fondo:
                    with open("fondo.png", "wb") as f:
                        f.write(up_fondo.getbuffer())
                    st.success("✅ Fondo actualizado")

            with st.expander("👥 Autoridades", expanded=False):
                directora = st.text_input("Directora:", "Prof. Ana María CUSI INCA", key="dir_i")
                promotor = st.text_input("Promotor:", "Prof. Leandro CORDOVA TOCRE", key="pro_i")

            with st.expander("🎯 Personalización", expanded=False):
                frase = st.text_input("Frase del Año:",
                                      "Año de la Esperanza y el Fortalecimiento de la Democracia",
                                      key="fr_i")
        else:
            directora = "Prof. Ana María CUSI INCA"
            promotor = "Prof. Leandro CORDOVA TOCRE"
            frase = "Año de la Esperanza y el Fortalecimiento de la Democracia"

        st.markdown("---")
        anio_sel = st.number_input("📅 Año:", 2024, 2035, 2026, key="anio_i")

        stats = BaseDatos.obtener_estadisticas()
        st.metric("📚 Total Alumnos", stats['total_alumnos'])

        st.markdown("---")
        if st.button("🔴 CERRAR SESIÓN", use_container_width=True):
            st.session_state.rol = None
            st.rerun()

    return {
        'anio': anio_sel,
        'directora': directora if st.session_state.rol == "admin" else "Prof. Ana María CUSI INCA",
        'promotor': promotor if st.session_state.rol == "admin" else "Prof. Leandro CORDOVA TOCRE",
        'frase': frase if st.session_state.rol == "admin" else "Año de la Esperanza y el Fortalecimiento de la Democracia",
        'y_frase': 700, 'y_titulo': 630, 'qr_x': 435, 'qr_y': 47
    }


# ========================================
# TAB: MATRÍCULA
# ========================================

def tab_matricula(config):
    st.header("📝 Matrícula de Estudiantes")

    tab_reg, tab_lista, tab_descargar = st.tabs([
        "➕ Registrar Estudiante", "📋 Lista de Matriculados", "⬇️ Descargar Registros"
    ])

    with tab_reg:
        st.subheader("Registrar Nuevo Estudiante")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**👤 Datos del Estudiante**")
            nombre_est = st.text_input("Apellidos y Nombres:", key="mat_nombre")
            dni_est = st.text_input("DNI del Estudiante:", key="mat_dni", max_chars=8)

            nivel = st.selectbox("Nivel:", list(NIVELES_GRADOS.keys()), key="mat_nivel")
            grados_nivel = NIVELES_GRADOS[nivel]
            grado = st.selectbox("Grado:", grados_nivel, key="mat_grado")
            seccion = st.selectbox("Sección:", SECCIONES, key="mat_seccion")

        with col2:
            st.markdown("**👨‍👩‍👧 Datos del Apoderado**")
            nombre_apo = st.text_input("Nombres del Apoderado:", key="mat_apoderado")
            dni_apo = st.text_input("DNI del Apoderado:", key="mat_dni_apo", max_chars=8)
            celular_apo = st.text_input("Celular del Apoderado:", key="mat_celular",
                                        max_chars=9, placeholder="987654321")

        st.markdown("---")
        if st.button("✅ REGISTRAR ESTUDIANTE", type="primary", use_container_width=True, key="btn_matricular"):
            if nombre_est and dni_est and grado:
                datos = {
                    'Nombre': nombre_est.strip(),
                    'DNI': dni_est.strip(),
                    'Nivel': nivel,
                    'Grado': grado,
                    'Seccion': seccion,
                    'Apoderado': nombre_apo.strip(),
                    'DNI_Apoderado': dni_apo.strip(),
                    'Celular_Apoderado': celular_apo.strip()
                }
                BaseDatos.registrar_estudiante(datos)
                st.success(f"✅ Estudiante **{nombre_est}** matriculado correctamente en **{grado} - {seccion}**")
                st.balloons()
            else:
                st.error("⚠️ Complete al menos: Nombre, DNI y Grado")

    with tab_lista:
        st.subheader("📋 Estudiantes Matriculados")
        df = BaseDatos.cargar_matricula()

        if not df.empty:
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                filtro_nivel = st.selectbox("Filtrar Nivel:", ["Todos"] + list(NIVELES_GRADOS.keys()),
                                            key="filt_nivel")
            with col_f2:
                if filtro_nivel != "Todos":
                    grados_f = ["Todos"] + NIVELES_GRADOS[filtro_nivel]
                else:
                    grados_f = ["Todos"] + TODOS_LOS_GRADOS
                filtro_grado = st.selectbox("Filtrar Grado:", grados_f, key="filt_grado")
            with col_f3:
                busq = st.text_input("🔍 Buscar:", key="busq_mat")

            df_f = df.copy()
            if filtro_nivel != "Todos" and 'Nivel' in df_f.columns:
                df_f = df_f[df_f['Nivel'] == filtro_nivel]
            if filtro_grado != "Todos" and 'Grado' in df_f.columns:
                df_f = df_f[df_f['Grado'] == filtro_grado]
            if busq:
                mask = df_f.apply(lambda r: busq.lower() in str(r).lower(), axis=1)
                df_f = df_f[mask]

            # Métricas
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Total Filtrados", len(df_f))
            with c2:
                if 'Grado' in df_f.columns:
                    st.metric("Grados", df_f['Grado'].nunique())
            with c3:
                st.metric("Total General", len(df))

            st.dataframe(df_f, use_container_width=True, hide_index=True, height=400)

            # Eliminar estudiante
            st.markdown("---")
            with st.expander("🗑️ Eliminar Estudiante"):
                dni_eliminar = st.text_input("DNI a eliminar:", key="dni_elim")
                if st.button("🗑️ ELIMINAR", key="btn_elim"):
                    if dni_eliminar:
                        BaseDatos.eliminar_estudiante(dni_eliminar)
                        st.success("✅ Estudiante eliminado")
                        st.rerun()
        else:
            st.info("📝 No hay estudiantes matriculados aún.")

    with tab_descargar:
        st.subheader("⬇️ Descargar Registros")
        df = BaseDatos.cargar_matricula()

        if not df.empty:
            # Descargar Excel de matrícula
            buf_xlsx = io.BytesIO()
            df.to_excel(buf_xlsx, index=False, engine='openpyxl')
            buf_xlsx.seek(0)
            st.download_button("📊 Descargar Matrícula (Excel)", buf_xlsx,
                               f"Matricula_{config['anio']}.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True, key="dl_mat_xlsx")

            st.markdown("---")
            st.markdown("**📄 Generar PDFs por Grado**")

            col_g1, col_g2 = st.columns(2)
            with col_g1:
                nivel_pdf = st.selectbox("Nivel:", list(NIVELES_GRADOS.keys()), key="pdf_nivel")
                grado_pdf = st.selectbox("Grado:", NIVELES_GRADOS[nivel_pdf], key="pdf_grado")
            with col_g2:
                seccion_pdf = st.selectbox("Sección:", SECCIONES, key="pdf_seccion")
                anio_pdf = config['anio']

            # Filtrar estudiantes del grado
            df_grado = df.copy()
            if 'Grado' in df_grado.columns:
                df_grado = df_grado[df_grado['Grado'] == grado_pdf]
            if 'Seccion' in df_grado.columns and seccion_pdf != "Única":
                df_grado = df_grado[df_grado['Seccion'] == seccion_pdf]

            st.info(f"📊 Estudiantes encontrados: **{len(df_grado)}**")

            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                if st.button("📝 Generar Registro de NOTAS", type="primary",
                             use_container_width=True, key="gen_notas"):
                    with st.spinner("Generando registro de notas..."):
                        pdf = generar_registro_notas_pdf(grado_pdf, seccion_pdf, anio_pdf, df_grado)
                        st.download_button("⬇️ Descargar Registro Notas",
                                           pdf, f"Registro_Notas_{grado_pdf}_{seccion_pdf}_{anio_pdf}.pdf",
                                           "application/pdf", use_container_width=True, key="dl_notas")

            with col_btn2:
                if st.button("📋 Generar Registro de ASISTENCIA", type="primary",
                             use_container_width=True, key="gen_asist"):
                    with st.spinner("Generando registro de asistencia (Marzo-Diciembre)..."):
                        pdf = generar_registro_asistencia_pdf(grado_pdf, seccion_pdf, anio_pdf, df_grado)
                        st.download_button("⬇️ Descargar Registro Asistencia",
                                           pdf, f"Registro_Asistencia_{grado_pdf}_{seccion_pdf}_{anio_pdf}.pdf",
                                           "application/pdf", use_container_width=True, key="dl_asist")
        else:
            st.info("📝 No hay estudiantes para generar registros.")


# ========================================
# TAB: DOCUMENTOS
# ========================================

def tab_documentos(config):
    st.header("📄 Emisión de Documentos")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Configuración")
        tipo_doc = st.selectbox("📑 Tipo:", [
            "CONSTANCIA DE VACANTE", "CONSTANCIA DE NO DEUDOR",
            "CONSTANCIA DE ESTUDIOS", "CONSTANCIA DE CONDUCTA",
            "CARTA COMPROMISO PADRE DE FAMILIA", "RESOLUCIÓN DE TRASLADO"
        ], key="tipo_doc_sel")

        st.markdown("---")
        dni_busq = st.text_input("🔍 Buscar por DNI:", key="dni_bus_doc")
        if st.button("🔎 Buscar", use_container_width=True, key="btn_bus_doc"):
            res = BaseDatos.buscar_por_dni(dni_busq)
            if res:
                st.session_state.alumno = res.get('Nombre', res.get('Alumno', ''))
                st.session_state.dni = res.get('DNI', res.get('Dni', ''))
                st.session_state.grado = res.get('Grado', '')
                st.session_state.apoderado = res.get('Apoderado', '')
                st.session_state.dni_apo = res.get('DNI_Apoderado', res.get('Dni_Apoderado', ''))
                st.success("✅ Datos cargados")
                st.rerun()
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
                cols = st.columns(5)
                for i, c in enumerate(cols):
                    with c:
                        notas_conducta[f'nota_conducta_{i + 1}'] = st.selectbox(
                            f"{i + 1}°", ["AD", "A", "B", "C"], key=f"nota{i + 1}")

            extras = {}
            if tipo_doc == "RESOLUCIÓN DE TRASLADO":
                extras['num_resolucion'] = st.text_input("N° Resolución:", key="num_res")
                extras['fecha_resolucion'] = st.text_input("Fecha:", key="fec_res")
                extras['nivel'] = st.selectbox("Nivel:", ["INICIAL", "PRIMARIA", "SECUNDARIA"], key="nivel_res")
                extras['ie_destino'] = st.text_input("IE de Destino:", key="ie_dest")
                extras['nivel_destino'] = st.text_input("Nivel de Continuidad:", key="niv_dest")

        st.markdown("---")
        if st.button("✨ GENERAR DOCUMENTO", type="primary", use_container_width=True, key="btn_gen_doc"):
            if nombre and dni:
                with st.spinner("Generando..."):
                    datos = {'alumno': nombre, 'dni': dni, 'grado': grado,
                             'apoderado': apoderado, 'dni_apo': dni_apo,
                             **notas_conducta, **extras}
                    gen = GeneradorPDF(config)
                    metodos = {
                        "CONSTANCIA DE VACANTE": gen.generar_constancia_vacante,
                        "CONSTANCIA DE NO DEUDOR": gen.generar_constancia_no_deudor,
                        "CONSTANCIA DE ESTUDIOS": gen.generar_constancia_estudios,
                        "CONSTANCIA DE CONDUCTA": gen.generar_constancia_conducta,
                        "CARTA COMPROMISO PADRE DE FAMILIA": gen.generar_carta_compromiso,
                        "RESOLUCIÓN DE TRASLADO": gen.generar_resolucion_traslado,
                    }
                    pdf = metodos[tipo_doc](datos)
                    st.success("✅ Documento generado")
                    st.download_button("⬇️ DESCARGAR PDF", pdf,
                                       f"{nombre.replace(' ', '_')}_{tipo_doc.replace(' ', '_')}.pdf",
                                       "application/pdf", use_container_width=True, key="dl_doc")
            else:
                st.error("⚠️ Complete al menos nombre y DNI")


# ========================================
# TAB: CARNETS
# ========================================

def tab_carnets(config):
    st.header("🪪 Centro de Carnetización")
    tab_ind, tab_desde_mat, tab_lote = st.tabs([
        "⚡ Carnet Individual", "📋 Desde Matrícula", "📦 Generación en Lote"
    ])

    with tab_ind:
        st.subheader("Crear Carnet Individual")
        col1, col2 = st.columns(2)
        with col1:
            i_nom = st.text_input("👤 Nombre:", key="ci_nom")
            i_dni = st.text_input("🆔 DNI:", key="ci_dni")
            i_gra = st.selectbox("📚 Grado:", TODOS_LOS_GRADOS, key="ci_gra")
            i_sec = st.selectbox("📂 Sección:", SECCIONES, key="ci_sec")
        with col2:
            i_foto = st.file_uploader("📸 Foto del estudiante:", type=['jpg', 'png', 'jpeg'], key="ci_foto")
            if i_foto:
                st.image(i_foto, width=200, caption="Vista previa")

        if st.button("🪪 GENERAR CARNET", type="primary", use_container_width=True, key="btn_ci"):
            if i_nom and i_dni:
                with st.spinner("Generando carnet..."):
                    foto_io = io.BytesIO(i_foto.getvalue()) if i_foto else None
                    datos = {'alumno': i_nom, 'dni': i_dni, 'grado': i_gra, 'seccion': i_sec}
                    gen = GeneradorCarnet(datos, config['anio'], foto_io)
                    carnet = gen.generar()
                    st.image(carnet, use_container_width=True)
                    st.download_button("⬇️ DESCARGAR CARNET", carnet,
                                       f"Carnet_{i_nom.replace(' ', '_')}.png",
                                       "image/png", use_container_width=True, key="dl_ci")
            else:
                st.error("⚠️ Complete nombre y DNI")

    with tab_desde_mat:
        st.subheader("Crear Carnet desde Matrícula")
        dni_buscar = st.text_input("🔍 Buscar DNI del estudiante matriculado:", key="ci_buscar_dni")

        if st.button("🔎 Buscar Estudiante", key="btn_buscar_carnet"):
            alumno = BaseDatos.buscar_por_dni(dni_buscar)
            if alumno:
                st.session_state['carnet_datos_encontrados'] = alumno
                st.success(f"✅ Encontrado: {alumno.get('Nombre', '')}")
            else:
                st.error("❌ DNI no encontrado en matrícula")

        if 'carnet_datos_encontrados' in st.session_state and st.session_state['carnet_datos_encontrados']:
            alumno = st.session_state['carnet_datos_encontrados']
            st.markdown(f"""
            **Datos encontrados:**
            - **Nombre:** {alumno.get('Nombre', '')}
            - **DNI:** {alumno.get('DNI', '')}
            - **Grado:** {alumno.get('Grado', '')}
            - **Sección:** {alumno.get('Seccion', '')}
            """)

            foto_mat = st.file_uploader("📸 Agregar foto:", type=['jpg', 'png', 'jpeg'], key="foto_mat_carnet")

            if st.button("🪪 GENERAR CARNET", type="primary", use_container_width=True, key="btn_gen_mat_carnet"):
                with st.spinner("Generando..."):
                    foto_io = io.BytesIO(foto_mat.getvalue()) if foto_mat else None
                    datos = {
                        'alumno': alumno.get('Nombre', ''),
                        'dni': alumno.get('DNI', ''),
                        'grado': alumno.get('Grado', ''),
                        'seccion': alumno.get('Seccion', ''),
                    }
                    gen = GeneradorCarnet(datos, config['anio'], foto_io)
                    carnet = gen.generar()
                    st.image(carnet, use_container_width=True)
                    st.download_button("⬇️ DESCARGAR", carnet,
                                       f"Carnet_{alumno.get('Nombre', '').replace(' ', '_')}.png",
                                       "image/png", use_container_width=True, key="dl_mat_carnet")

    with tab_lote:
        st.subheader("Generación Masiva de Carnets")

        df = BaseDatos.cargar_matricula()
        if not df.empty:
            nivel_lote = st.selectbox("Filtrar por Nivel:", ["Todos"] + list(NIVELES_GRADOS.keys()), key="lote_nivel")
            if nivel_lote != "Todos":
                grado_lote = st.selectbox("Grado:", ["Todos"] + NIVELES_GRADOS[nivel_lote], key="lote_grado")
            else:
                grado_lote = "Todos"

            df_filtrado = df.copy()
            if nivel_lote != "Todos" and 'Nivel' in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado['Nivel'] == nivel_lote]
            if grado_lote != "Todos" and 'Grado' in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado['Grado'] == grado_lote]

            st.info(f"📊 Se generarán **{len(df_filtrado)}** carnets")
            st.dataframe(df_filtrado[['Nombre', 'DNI', 'Grado', 'Seccion']].head(20),
                         use_container_width=True, hide_index=True)

            if st.button("🚀 GENERAR TODOS LOS CARNETS (ZIP)", type="primary",
                         use_container_width=True, key="btn_lote"):
                if not df_filtrado.empty:
                    with st.spinner("Generando carnets..."):
                        buf_zip = io.BytesIO()
                        prog = st.progress(0)
                        total = len(df_filtrado)

                        with zipfile.ZipFile(buf_zip, "w", zipfile.ZIP_DEFLATED) as zf:
                            for i, (_, row) in enumerate(df_filtrado.iterrows()):
                                datos = {
                                    'alumno': row.get('Nombre', ''),
                                    'dni': row.get('DNI', ''),
                                    'grado': row.get('Grado', ''),
                                    'seccion': row.get('Seccion', ''),
                                }
                                gen = GeneradorCarnet(datos, config['anio'])
                                carnet = gen.generar()
                                fname = f"Carnet_{row.get('Nombre', '').replace(' ', '_')}.png"
                                zf.writestr(fname, carnet.getvalue())
                                prog.progress((i + 1) / total)

                        buf_zip.seek(0)
                        st.balloons()
                        st.download_button("⬇️ DESCARGAR ZIP", buf_zip,
                                           f"Carnets_{config['anio']}.zip",
                                           "application/zip", use_container_width=True, key="dl_zip")
                else:
                    st.warning("No hay estudiantes para generar carnets")
        else:
            st.info("📝 Registra estudiantes en Matrícula primero.")


# ========================================
# TAB: CONTROL DE ASISTENCIA CON CÁMARA
# ========================================

def tab_asistencias():
    st.header("📋 Control de Asistencia")

    # Selector Entrada/Salida
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.button("🌅 ENTRADA",
                      use_container_width=True,
                      type="primary" if st.session_state.tipo_asistencia == "Entrada" else "secondary",
                      key="btn_entrada"):
            st.session_state.tipo_asistencia = "Entrada"
            st.rerun()
    with col_t2:
        if st.button("🌙 SALIDA",
                      use_container_width=True,
                      type="primary" if st.session_state.tipo_asistencia == "Salida" else "secondary",
                      key="btn_salida"):
            st.session_state.tipo_asistencia = "Salida"
            st.rerun()

    st.info(f"📌 **Modo actual:** {st.session_state.tipo_asistencia} | 📅 {datetime.now().strftime('%d/%m/%Y')}")

    st.markdown("---")
    col_cam, col_man = st.columns([1, 1])

    # ---- ESCANEO CON CÁMARA ----
    with col_cam:
        st.markdown("### 📸 Escanear QR / Código de Barras")

        if HAS_PYZBAR:
            st.success("✅ Escáner de QR/Barcode disponible")
        else:
            st.warning("⚠️ Módulo pyzbar no disponible. Use registro manual.")

        # Cámara de Streamlit
        foto_camara = st.camera_input("📷 Activa la cámara y escanea el carnet:", key="cam_asist")

        if foto_camara:
            # Procesar imagen capturada
            img_bytes = foto_camara.getvalue()
            dni_detectado = decodificar_qr_imagen(img_bytes)

            if dni_detectado:
                st.success(f"📱 **DNI detectado:** {dni_detectado}")
                alumno = BaseDatos.buscar_por_dni(dni_detectado)

                if alumno:
                    hora_exacta = datetime.now().strftime('%H:%M:%S')
                    tipo = st.session_state.tipo_asistencia.lower()
                    nombre = alumno.get('Nombre', alumno.get('Alumno', ''))

                    BaseDatos.guardar_asistencia(dni_detectado, nombre, tipo, hora_exacta)

                    st.markdown(f"""
                    <div class='success-box'>
                        <h3>✅ {nombre}</h3>
                        <p>🕒 {st.session_state.tipo_asistencia}: {hora_exacta}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # WhatsApp
                    celular = alumno.get('Celular_Apoderado', alumno.get('Celular', ''))
                    if celular and celular.strip():
                        mensaje = generar_mensaje_asistencia(nombre, tipo, hora_exacta)
                        link = generar_link_whatsapp(celular, mensaje)
                        st.markdown(f'<a href="{link}" target="_blank">'
                                    f'<button style="background:#25D366;color:white;padding:10px 20px;'
                                    f'border:none;border-radius:8px;font-size:16px;cursor:pointer;width:100%">'
                                    f'📱 ENVIAR WhatsApp a {celular}</button></a>',
                                    unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ No tiene celular de apoderado registrado")
                else:
                    st.error(f"❌ DNI {dni_detectado} no encontrado en la base de datos")
            else:
                st.warning("⚠️ No se pudo detectar QR/código de barras. Intente de nuevo o use registro manual.")

    # ---- REGISTRO MANUAL ----
    with col_man:
        st.markdown("### ✏️ Registro Manual por DNI")
        dni_manual = st.text_input("Ingrese el DNI:", key="dni_manual_asist",
                                   placeholder="Escriba o pegue el DNI aquí")

        if st.button("✅ REGISTRAR", type="primary", use_container_width=True, key="btn_reg_manual"):
            if dni_manual:
                alumno = BaseDatos.buscar_por_dni(dni_manual.strip())
                if alumno:
                    hora_exacta = datetime.now().strftime('%H:%M:%S')
                    tipo = st.session_state.tipo_asistencia.lower()
                    nombre = alumno.get('Nombre', alumno.get('Alumno', ''))

                    BaseDatos.guardar_asistencia(dni_manual.strip(), nombre, tipo, hora_exacta)
                    st.success(f"✅ **{nombre}** - {st.session_state.tipo_asistencia}: {hora_exacta}")
                    st.balloons()

                    celular = alumno.get('Celular_Apoderado', alumno.get('Celular', ''))
                    if celular and celular.strip():
                        mensaje = generar_mensaje_asistencia(nombre, tipo, hora_exacta)
                        link = generar_link_whatsapp(celular, mensaje)
                        st.markdown(f'<a href="{link}" target="_blank">'
                                    f'<button style="background:#25D366;color:white;padding:10px 20px;'
                                    f'border:none;border-radius:8px;font-size:16px;cursor:pointer;width:100%">'
                                    f'📱 ENVIAR WhatsApp a {celular}</button></a>',
                                    unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Sin celular registrado")
                else:
                    st.error("❌ DNI no encontrado")
            else:
                st.warning("⚠️ Ingrese un DNI")

    # ---- TABLA DE ASISTENCIAS DEL DÍA ----
    st.markdown("---")
    st.subheader("📊 Registros de Asistencia - Hoy")

    asistencias_hoy = BaseDatos.obtener_asistencias_hoy()

    if asistencias_hoy:
        df_asist = pd.DataFrame([
            {
                'DNI': dni,
                'Nombre': datos['nombre'],
                'Entrada': datos.get('entrada', '—'),
                'Salida': datos.get('salida', '—')
            }
            for dni, datos in asistencias_hoy.items()
        ])
        st.dataframe(df_asist, use_container_width=True, hide_index=True)

        # Envío masivo por WhatsApp
        st.markdown("---")
        st.markdown("### 📱 Enviar Notificaciones por WhatsApp")
        st.caption("Haz clic en cada botón para abrir WhatsApp con el mensaje listo para enviar.")

        for dni, datos in asistencias_hoy.items():
            alumno = BaseDatos.buscar_por_dni(dni)
            if alumno:
                celular = alumno.get('Celular_Apoderado', alumno.get('Celular', ''))
                if celular and celular.strip():
                    nombre = datos['nombre']
                    entrada = datos.get('entrada', '')
                    salida = datos.get('salida', '')

                    if entrada and salida:
                        msg = (f"🏫 I.E. ALTERNATIVO YACHAY\n👤 {nombre}\n"
                               f"✅ Entrada: {entrada}\n🏁 Salida: {salida}")
                    elif entrada:
                        msg = generar_mensaje_asistencia(nombre, 'entrada', entrada)
                    elif salida:
                        msg = generar_mensaje_asistencia(nombre, 'salida', salida)
                    else:
                        continue

                    link = generar_link_whatsapp(celular, msg)
                    st.markdown(
                        f'<a href="{link}" target="_blank" style="text-decoration:none;">'
                        f'<div style="background:#f0f0f0;padding:8px 15px;border-radius:8px;'
                        f'margin:3px 0;display:flex;align-items:center;justify-content:space-between;">'
                        f'<span>👤 {nombre} | E: {entrada or "—"} | S: {salida or "—"}</span>'
                        f'<span style="background:#25D366;color:white;padding:4px 12px;border-radius:5px;">'
                        f'📱 WhatsApp</span></div></a>',
                        unsafe_allow_html=True
                    )
    else:
        st.info("📝 No hay registros de asistencia hoy.")


# ========================================
# TAB: CORRECTOR DE EXÁMENES
# ========================================

def tab_corrector_examenes():
    st.header("📝 Corrector de Exámenes")

    tab_gen, tab_corr = st.tabs(["📄 Generar Hoja de Respuestas", "✅ Corregir Examen"])

    with tab_gen:
        st.subheader("Generar Hoja de Respuestas Imprimible")

        col1, col2 = st.columns(2)
        with col1:
            num_preguntas = st.selectbox("Número de preguntas:", [10, 20, 30, 40, 50], index=1, key="num_preg_gen")
        with col2:
            titulo_examen = st.text_input("Título/Área:", "EVALUACIÓN", key="titulo_exam")

        if st.button("📄 GENERAR HOJA DE RESPUESTAS", type="primary", use_container_width=True, key="btn_gen_hoja"):
            with st.spinner("Generando hoja..."):
                hoja = _generar_hoja_respuestas_img(num_preguntas, titulo_examen)
                st.image(hoja, use_container_width=True, caption="Hoja de Respuestas")
                st.download_button("⬇️ DESCARGAR HOJA (PNG)", hoja,
                                   f"Hoja_Respuestas_{titulo_examen}_{num_preguntas}p.png",
                                   "image/png", use_container_width=True, key="dl_hoja")

    with tab_corr:
        st.subheader("Corregir Examen")

        st.markdown("**1️⃣ Configura las respuestas correctas por área:**")

        # Múltiples áreas
        if 'areas_examen' not in st.session_state:
            st.session_state.areas_examen = [{'nombre': 'Matemática', 'num': 10, 'claves': ''}]

        # Agregar área
        col_a1, col_a2, col_a3 = st.columns([2, 1, 1])
        with col_a1:
            nueva_area = st.text_input("Nombre del área:", key="nueva_area_nombre")
        with col_a2:
            nueva_num = st.selectbox("N° preguntas:", [5, 10, 15, 20, 25], key="nueva_area_num")
        with col_a3:
            st.markdown("###")
            if st.button("➕ Agregar Área", key="btn_add_area"):
                if nueva_area:
                    st.session_state.areas_examen.append({
                        'nombre': nueva_area, 'num': nueva_num, 'claves': ''
                    })
                    st.rerun()

        # Mostrar áreas y capturar claves
        total_preguntas = 0
        todas_claves = []

        for i, area in enumerate(st.session_state.areas_examen):
            with st.expander(f"📚 {area['nombre']} ({area['num']} preguntas)", expanded=True):
                claves = st.text_input(
                    f"Claves de respuesta (ej: ABCDABCDAB):",
                    value=area.get('claves', ''),
                    key=f"claves_{i}",
                    max_chars=area['num'],
                    placeholder="A" * area['num']
                )
                st.session_state.areas_examen[i]['claves'] = claves.upper()
                todas_claves.extend(list(claves.upper()))
                total_preguntas += area['num']

                col_del, _ = st.columns([1, 3])
                with col_del:
                    if len(st.session_state.areas_examen) > 1:
                        if st.button(f"🗑️ Eliminar", key=f"del_area_{i}"):
                            st.session_state.areas_examen.pop(i)
                            st.rerun()

        st.info(f"📊 Total de preguntas: **{total_preguntas}** | Claves ingresadas: **{len(todas_claves)}**")

        st.markdown("---")
        st.markdown("**2️⃣ Captura o sube la hoja de respuestas del alumno:**")

        metodo = st.radio("Método:", ["📸 Usar cámara", "📎 Subir imagen"], horizontal=True, key="metodo_corr")

        archivo_img = None
        if metodo == "📸 Usar cámara":
            foto = st.camera_input("📷 Toma foto de la hoja:", key="cam_exam")
            if foto:
                archivo_img = foto.getvalue()
        else:
            upload = st.file_uploader("📎 Sube foto de la hoja:", type=['jpg', 'png', 'jpeg'], key="up_exam")
            if upload:
                archivo_img = upload.getvalue()

        if archivo_img and todas_claves:
            if st.button("✅ CORREGIR EXAMEN", type="primary", use_container_width=True, key="btn_corregir"):
                with st.spinner("Procesando examen..."):
                    respuestas = _procesar_examen(archivo_img, len(todas_claves))

                    if respuestas and len(respuestas) > 0:
                        # Calcular resultados
                        correctas = sum(1 for i, r in enumerate(respuestas)
                                        if i < len(todas_claves) and r == todas_claves[i])
                        nota = (correctas / len(todas_claves)) * 20
                        letra = "AD" if nota >= 18 else "A" if nota >= 14 else "B" if nota >= 11 else "C"

                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            st.metric("✅ Correctas", f"{correctas}/{len(todas_claves)}")
                        with c2:
                            st.metric("❌ Incorrectas", f"{len(todas_claves) - correctas}")
                        with c3:
                            st.metric("📊 Nota", f"{nota:.1f}")
                        with c4:
                            st.metric("📝 Calificación", letra)

                        # Detalle por área
                        idx_global = 0
                        for area in st.session_state.areas_examen:
                            n = area['num']
                            claves_area = list(area.get('claves', '').upper())[:n]
                            resp_area = respuestas[idx_global:idx_global + n]

                            correctas_area = sum(1 for j in range(min(len(claves_area), len(resp_area)))
                                                 if claves_area[j] == resp_area[j])

                            st.markdown(f"**📚 {area['nombre']}:** {correctas_area}/{n}")

                            data = []
                            for j in range(n):
                                clave = claves_area[j] if j < len(claves_area) else "?"
                                resp = resp_area[j] if j < len(resp_area) else "?"
                                estado = "✅" if clave == resp else "❌"
                                data.append({
                                    'Pregunta': idx_global + j + 1,
                                    'Correcta': clave,
                                    'Marcada': resp,
                                    'Estado': estado
                                })
                            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
                            idx_global += n
                    else:
                        st.error("⚠️ No se pudieron detectar respuestas. Intente con mejor iluminación o ingrese manualmente.")

                        # Opción manual
                        st.markdown("**Ingreso manual de respuestas del alumno:**")
                        resp_manual = st.text_input("Respuestas marcadas (ej: ABCDABCD...):",
                                                     key="resp_manual", max_chars=total_preguntas)
                        if resp_manual and st.button("📊 Calcular Nota Manual", key="btn_manual_nota"):
                            resp_list = list(resp_manual.upper())
                            correctas = sum(1 for i in range(min(len(resp_list), len(todas_claves)))
                                            if resp_list[i] == todas_claves[i])
                            nota = (correctas / len(todas_claves)) * 20
                            st.metric("📊 Nota", f"{nota:.1f}/20")
                            st.metric("✅ Correctas", f"{correctas}/{len(todas_claves)}")


def _generar_hoja_respuestas_img(num_preguntas, titulo):
    """Genera hoja de respuestas como imagen PNG"""
    width, height = 2480, 3508
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # Fuentes
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 45)
        font_num = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        font_letra = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
    except:
        font_title = font_sub = font_num = font_letra = ImageFont.load_default()

    # Marcadores de alineación (esquinas)
    sz = 80
    for pos in [(50, 50), (width - 130, 50), (50, height - 130), (width - 130, height - 130)]:
        draw.rectangle([pos, (pos[0] + sz, pos[1] + sz)], fill="black")

    # Encabezado
    draw.text((width // 2, 200), "I.E.P. ALTERNATIVO YACHAY", font=font_title, fill="black", anchor="mm")
    draw.text((width // 2, 280), f"HOJA DE RESPUESTAS - {titulo.upper()}", font=font_sub, fill="black", anchor="mm")
    draw.text((width // 2, 350), '"EDUCAR PARA LA VIDA"', font=font_sub, fill="gray", anchor="mm")

    # Campos
    draw.text((200, 480), "Nombre: ________________________________________", font=font_sub, fill="black")
    draw.text((200, 560), "DNI: ________________  Grado: ________________", font=font_sub, fill="black")
    draw.text((200, 640), f"Fecha: ________________  N° Preguntas: {num_preguntas}", font=font_sub, fill="black")

    # Instrucciones
    draw.text((200, 740), "INSTRUCCIONES: Rellene completamente el círculo de la alternativa correcta.",
              font=font_letra, fill="gray")

    # Preguntas
    start_y = 900
    start_x = 300
    spacing_y = 100
    col_spacing = 700
    preguntas_por_col = min(25, (height - start_y - 200) // spacing_y)
    letras = ['A', 'B', 'C', 'D']

    for i in range(num_preguntas):
        col = i // preguntas_por_col
        fila = i % preguntas_por_col
        x_base = start_x + (col * col_spacing)
        y_base = start_y + (fila * spacing_y)

        # Número de pregunta
        draw.text((x_base - 100, y_base), f"{i + 1}.", font=font_num, fill="black", anchor="rm")

        # Burbujas
        for j, letra in enumerate(letras):
            cx = x_base + (j * 130)
            cy = y_base
            r = 35
            draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline="black", width=4)
            draw.text((cx, cy), letra, font=font_letra, fill="black", anchor="mm")

    # Guardar
    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output


def _procesar_examen(img_bytes, num_preguntas):
    """Procesa imagen de examen y detecta respuestas"""
    if not HAS_CV2:
        return None

    try:
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Detectar burbujas (círculos)
        burbujas = []
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h) if h > 0 else 0
            area = cv2.contourArea(c)
            if 0.7 <= ar <= 1.3 and 15 <= w <= 120 and 15 <= h <= 120 and area > 200:
                burbujas.append((c, x, y, w, h))

        if not burbujas:
            return None

        # Agrupar por filas (tolerancia en Y)
        burbujas = sorted(burbujas, key=lambda b: b[2])
        filas = []
        fila_actual = [burbujas[0]]
        for b in burbujas[1:]:
            if abs(b[2] - fila_actual[-1][2]) <= 30:
                fila_actual.append(b)
            else:
                if len(fila_actual) >= 3:
                    filas.append(sorted(fila_actual, key=lambda b: b[1]))
                fila_actual = [b]
        if len(fila_actual) >= 3:
            filas.append(sorted(fila_actual, key=lambda b: b[1]))

        # Detectar respuestas
        respuestas = []
        for fila in filas[:num_preguntas]:
            opciones = fila[:4]  # Máximo 4 opciones
            intensidades = []
            for (contour, x, y, w, h) in opciones:
                mask = np.zeros(gray.shape, dtype="uint8")
                cv2.drawContours(mask, [contour], -1, 255, -1)
                masked = cv2.bitwise_and(thresh, thresh, mask=mask)
                total = cv2.countNonZero(masked)
                intensidades.append(total)

            if intensidades:
                max_idx = intensidades.index(max(intensidades))
                if max_idx < 4:
                    respuestas.append(['A', 'B', 'C', 'D'][max_idx])
                else:
                    respuestas.append('?')
            else:
                respuestas.append('?')

        return respuestas if respuestas else None
    except Exception:
        return None


# ========================================
# TAB: BASE DE DATOS
# ========================================

def tab_base_datos():
    st.header("📊 Base de Datos General")
    df = BaseDatos.cargar_matricula()

    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("📚 Total", len(df))
        with c2:
            if 'Grado' in df.columns:
                st.metric("🎓 Grados", df['Grado'].nunique())
        with c3:
            if 'Nivel' in df.columns:
                st.metric("📋 Niveles", df['Nivel'].nunique())
        with c4:
            if 'Celular_Apoderado' in df.columns:
                st.metric("📱 Con Celular", df['Celular_Apoderado'].notna().sum())

        st.markdown("---")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            if 'Grado' in df.columns:
                grados = ['Todos'] + sorted(df['Grado'].dropna().unique().tolist())
                filtro = st.selectbox("Filtrar por Grado:", grados, key="filtro_bd")
        with col_f2:
            busqueda = st.text_input("🔍 Buscar:", key="busq_bd")

        df_f = df.copy()
        if filtro != 'Todos' and 'Grado' in df.columns:
            df_f = df_f[df_f['Grado'] == filtro]
        if busqueda:
            mask = df_f.apply(lambda r: busqueda.lower() in str(r).lower(), axis=1)
            df_f = df_f[mask]

        st.dataframe(df_f, use_container_width=True, hide_index=True, height=500)

        # Descargas
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            csv = df_f.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Descargar CSV", csv,
                               f"base_datos_{datetime.now().strftime('%Y%m%d')}.csv",
                               "text/csv", use_container_width=True, key="dl_csv")
        with col_d2:
            buf = io.BytesIO()
            df_f.to_excel(buf, index=False, engine='openpyxl')
            buf.seek(0)
            st.download_button("⬇️ Descargar Excel", buf,
                               f"base_datos_{datetime.now().strftime('%Y%m%d')}.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True, key="dl_xlsx")
    else:
        st.info("📝 No hay datos. Registra estudiantes en la pestaña Matrícula.")


# ========================================
# FUNCIÓN PRINCIPAL
# ========================================

def main():
    if st.session_state.rol is None:
        pantalla_login()
        st.stop()

    config = configurar_sidebar()

    if st.session_state.rol == "auxiliar":
        tab1, tab2 = st.tabs(["📋 ASISTENCIAS", "📝 CORRECTOR EXÁMENES"])
        with tab1:
            tab_asistencias()
        with tab2:
            tab_corrector_examenes()

    elif st.session_state.rol in ["directivo", "admin"]:
        tabs = st.tabs([
            "📝 MATRÍCULA",
            "📄 DOCUMENTOS",
            "🪪 CARNETS",
            "📋 ASISTENCIAS",
            "📊 BASE DATOS",
            "📝 CORRECTOR EXÁMENES"
        ])
        with tabs[0]:
            tab_matricula(config)
        with tabs[1]:
            tab_documentos(config)
        with tabs[2]:
            tab_carnets(config)
        with tabs[3]:
            tab_asistencias()
        with tabs[4]:
            tab_base_datos()
        with tabs[5]:
            tab_corrector_examenes()


if __name__ == "__main__":
    main()
