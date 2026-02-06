# ================================================================
# SISTEMA YACHAY PRO - VERSIÓN DEFINITIVA COMPLETA
# ================================================================
# Sistema completo de gestión educativa
# Módulos: Matrícula, Documentos, Carnets, Asistencia QR,
#          Sistema de Calificación Yachay (estilo ZipGrade)
# ================================================================

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
import io
import textwrap
import zipfile
import time
import json
import urllib.parse
import numpy as np
import calendar
from datetime import datetime, timedelta, timezone, date
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

st.set_page_config(page_title="SISTEMA YACHAY PRO", page_icon="🎓", layout="wide")

# ================================================================
# ZONA HORARIA PERÚ (UTC-5) — HORA CORRECTA SIEMPRE
# ================================================================

PERU_TZ = timezone(timedelta(hours=-5))


def hora_peru():
    """Retorna datetime actual en hora de Perú"""
    return datetime.now(PERU_TZ)


def hora_peru_str():
    """Retorna hora de Perú HH:MM:SS"""
    return hora_peru().strftime('%H:%M:%S')


def fecha_peru_str():
    """Retorna fecha de Perú YYYY-MM-DD"""
    return hora_peru().strftime('%Y-%m-%d')


# ================================================================
# FERIADOS OFICIALES DE PERÚ (mes, dia)
# ================================================================

FERIADOS_PERU = {
    (1, 1): "Año Nuevo",
    (5, 1): "Día del Trabajo",
    (6, 7): "Batalla de Arica",
    (6, 29): "San Pedro y San Pablo",
    (7, 23): "Fuerza Aérea del Perú",
    (7, 28): "Fiestas Patrias",
    (7, 29): "Fiestas Patrias",
    (8, 6): "Batalla de Junín",
    (8, 30): "Santa Rosa de Lima",
    (10, 8): "Combate de Angamos",
    (11, 1): "Día de Todos los Santos",
    (12, 8): "Inmaculada Concepción",
    (12, 9): "Batalla de Ayacucho",
    (12, 25): "Navidad",
}


def dias_habiles_mes(anio, mes):
    """Retorna lista de días hábiles (Lunes-Viernes, sin feriados) de un mes"""
    dias = []
    _, ndays = calendar.monthrange(anio, mes)
    for d in range(1, ndays + 1):
        dt = date(anio, mes, d)
        # weekday(): 0=Lunes, 4=Viernes, 5=Sábado, 6=Domingo
        es_laboral = dt.weekday() < 5
        es_feriado = (mes, d) in FERIADOS_PERU
        if es_laboral and not es_feriado:
            dias.append(d)
    return dias


# ================================================================
# CONTRASEÑAS POR DOCENTE (UNA POR GRADO)
# ================================================================

DOCENTES_PASSWORDS = {
    "inicial3": {"label": "Inicial 3 años", "grado": "Inicial 3 años", "nivel": "INICIAL"},
    "inicial4": {"label": "Inicial 4 años", "grado": "Inicial 4 años", "nivel": "INICIAL"},
    "inicial5": {"label": "Inicial 5 años", "grado": "Inicial 5 años", "nivel": "INICIAL"},
    "primero": {"label": "1° Primaria", "grado": "1° Primaria", "nivel": "PRIMARIA"},
    "segundo": {"label": "2° Primaria", "grado": "2° Primaria", "nivel": "PRIMARIA"},
    "tercero": {"label": "3° Primaria", "grado": "3° Primaria", "nivel": "PRIMARIA"},
    "cuarto": {"label": "4° Primaria", "grado": "4° Primaria", "nivel": "PRIMARIA"},
    "quinto": {"label": "5° Primaria", "grado": "5° Primaria", "nivel": "PRIMARIA"},
    "sexto": {"label": "6° Primaria", "grado": "6° Primaria", "nivel": "PRIMARIA"},
    "coordinador": {"label": "Coordinador Secundaria", "grado": "ALL_SECUNDARIA", "nivel": "SECUNDARIA"},
}

# ================================================================
# CONSTANTES
# ================================================================

NIVELES_GRADOS = {
    "INICIAL": ["Inicial 3 años", "Inicial 4 años", "Inicial 5 años"],
    "PRIMARIA": [
        "1° Primaria", "2° Primaria", "3° Primaria",
        "4° Primaria", "5° Primaria", "6° Primaria"
    ],
    "SECUNDARIA": [
        "1° Secundaria", "2° Secundaria", "3° Secundaria",
        "4° Secundaria", "5° Secundaria"
    ],
    "PREUNIVERSITARIO": ["Ciclo Regular", "Ciclo Intensivo", "Ciclo Verano"]
}

SECCIONES = ["Única", "A", "B"]

TODOS_LOS_GRADOS = []
for nivel_key, grados_list in NIVELES_GRADOS.items():
    for grado_item in grados_list:
        TODOS_LOS_GRADOS.append(grado_item)

MESES_ESCOLARES = {
    3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre",
    10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

MESES_ESP = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

BIMESTRES = {
    "Bimestre 1": [3, 4, 5],
    "Bimestre 2": [5, 6, 7],
    "Bimestre 3": [8, 9, 10],
    "Bimestre 4": [10, 11, 12]
}

# Archivos de datos
ARCHIVO_BD = "base_datos.xlsx"
ARCHIVO_MATRICULA = "matricula.xlsx"
ARCHIVO_ASISTENCIAS = "asistencias.json"
ARCHIVO_RESULTADOS = "resultados_examenes.json"


# ================================================================
# INICIALIZACIÓN SESSION STATE
# ================================================================

def init_session_state():
    defaults = {
        'rol': None,
        'docente_info': None,
        'cola_carnets': [],
        'alumno': '',
        'dni': '',
        'grado': '',
        'apoderado': '',
        'dni_apo': '',
        'busqueda_counter': 0,
        'asistencias_dia': [],
        'tipo_asistencia': 'Entrada',
        'matricula_data': {},
        'activar_camara_asist': False,
        'areas_examen': [],
        'resultados_examen': [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()

# ================================================================
# ESTILOS CSS
# ================================================================

st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, #001e7c 0%, #0052cc 100%);
    color: white;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.wa-btn {
    background: #25D366;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 15px;
    cursor: pointer;
    width: 100%;
    text-decoration: none;
    display: block;
    text-align: center;
    margin: 4px 0;
}
.wa-btn:hover {
    background: #1da851;
}
.ranking-gold {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: #000;
    padding: 10px 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
    margin: 5px 0;
}
.ranking-silver {
    background: linear-gradient(135deg, #C0C0C0, #A0A0A0);
    color: #000;
    padding: 10px 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
    margin: 5px 0;
}
.ranking-bronze {
    background: linear-gradient(135deg, #CD7F32, #B8860B);
    color: #fff;
    padding: 10px 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

# ================================================================
# IMPORTACIONES OPCIONALES (barcode, cv2, pyzbar)
# ================================================================

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


# ================================================================
# FUENTES
# ================================================================

class RecursoManager:
    @staticmethod
    def obtener_fuente(nombre, tamaño, bold=False):
        try:
            rutas = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
                else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "Roboto-Bold.ttf" if bold else "Roboto-Regular.ttf",
            ]
            for ruta in rutas:
                if Path(ruta).exists():
                    return ImageFont.truetype(ruta, int(tamaño))
            return ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()


# ================================================================
# BASE DE DATOS
# ================================================================

class BaseDatos:

    @staticmethod
    def cargar_matricula():
        """Carga la matrícula desde Excel"""
        try:
            if Path(ARCHIVO_MATRICULA).exists():
                df = pd.read_excel(ARCHIVO_MATRICULA, dtype=str, engine='openpyxl')
                df.columns = df.columns.str.strip()
                return df
        except Exception:
            pass
        return pd.DataFrame(columns=[
            'Nombre', 'DNI', 'Nivel', 'Grado', 'Seccion',
            'Apoderado', 'DNI_Apoderado', 'Celular_Apoderado'
        ])

    @staticmethod
    def guardar_matricula(df):
        """Guarda la matrícula en Excel"""
        df.to_excel(ARCHIVO_MATRICULA, index=False, engine='openpyxl')

    @staticmethod
    def registrar_estudiante(datos):
        """Registra o actualiza un estudiante"""
        df = BaseDatos.cargar_matricula()
        if not df.empty and 'DNI' in df.columns and datos['DNI'] in df['DNI'].values:
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
        """Busca un estudiante por DNI en matrícula y BD legacy"""
        df = BaseDatos.cargar_matricula()
        if df is not None and not df.empty and 'DNI' in df.columns:
            dni_str = str(dni).strip()
            df['DNI'] = df['DNI'].astype(str).str.strip()
            resultado = df[df['DNI'] == dni_str]
            if not resultado.empty:
                return resultado.iloc[0].to_dict()
        # Buscar en base_datos.xlsx (legacy)
        try:
            if Path(ARCHIVO_BD).exists():
                df2 = pd.read_excel(ARCHIVO_BD, dtype=str, engine='openpyxl')
                df2.columns = df2.columns.str.strip().str.title()
                if 'Dni' in df2.columns:
                    df2['Dni'] = df2['Dni'].astype(str).str.strip()
                    res2 = df2[df2['Dni'] == str(dni).strip()]
                    if not res2.empty:
                        row = res2.iloc[0].to_dict()
                        return {
                            'Nombre': row.get('Alumno', row.get('Nombre', '')),
                            'DNI': row.get('Dni', ''),
                            'Grado': row.get('Grado', ''),
                            'Nivel': row.get('Nivel', ''),
                            'Seccion': row.get('Seccion', ''),
                            'Apoderado': row.get('Apoderado', ''),
                            'DNI_Apoderado': row.get('Dni_Apoderado',
                                                      row.get('Dni Apoderado', '')),
                            'Celular_Apoderado': row.get('Celular',
                                                          row.get('Celular_Apoderado', ''))
                        }
        except Exception:
            pass
        return None

    @staticmethod
    def eliminar_estudiante(dni):
        """Elimina un estudiante por DNI"""
        df = BaseDatos.cargar_matricula()
        df['DNI'] = df['DNI'].astype(str).str.strip()
        df = df[df['DNI'] != str(dni).strip()]
        BaseDatos.guardar_matricula(df)
        return True

    @staticmethod
    def obtener_estudiantes_grado(grado, seccion=None):
        """Retorna DataFrame de estudiantes de un grado, orden ALFABÉTICO"""
        df = BaseDatos.cargar_matricula()
        if df.empty:
            return df
        if grado == "ALL_SECUNDARIA":
            if 'Nivel' in df.columns:
                df = df[df['Nivel'] == "SECUNDARIA"]
        elif 'Grado' in df.columns:
            df = df[df['Grado'] == grado]
        if seccion and seccion not in ["Todas", "Única"] and 'Seccion' in df.columns:
            df = df[df['Seccion'] == seccion]
        if 'Nombre' in df.columns:
            df = df.sort_values('Nombre', ascending=True).reset_index(drop=True)
        return df

    @staticmethod
    def guardar_asistencia(dni, nombre, tipo, hora):
        """Guarda registro de asistencia (entrada/salida)"""
        fecha_hoy = fecha_peru_str()
        asistencias = {}
        if Path(ARCHIVO_ASISTENCIAS).exists():
            with open(ARCHIVO_ASISTENCIAS, 'r', encoding='utf-8') as f:
                asistencias = json.load(f)
        if fecha_hoy not in asistencias:
            asistencias[fecha_hoy] = {}
        if dni not in asistencias[fecha_hoy]:
            asistencias[fecha_hoy][dni] = {
                'nombre': nombre,
                'entrada': '',
                'salida': ''
            }
        asistencias[fecha_hoy][dni][tipo] = hora
        asistencias[fecha_hoy][dni]['nombre'] = nombre
        with open(ARCHIVO_ASISTENCIAS, 'w', encoding='utf-8') as f:
            json.dump(asistencias, f, indent=2, ensure_ascii=False)
        return True

    @staticmethod
    def obtener_asistencias_hoy():
        """Obtiene asistencias del día actual"""
        fecha_hoy = fecha_peru_str()
        if Path(ARCHIVO_ASISTENCIAS).exists():
            with open(ARCHIVO_ASISTENCIAS, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get(fecha_hoy, {})
        return {}

    @staticmethod
    def borrar_asistencias_hoy():
        """Borra todas las asistencias del día (para limpiar al día siguiente)"""
        fecha_hoy = fecha_peru_str()
        if Path(ARCHIVO_ASISTENCIAS).exists():
            with open(ARCHIVO_ASISTENCIAS, 'r', encoding='utf-8') as f:
                asistencias = json.load(f)
            if fecha_hoy in asistencias:
                del asistencias[fecha_hoy]
            with open(ARCHIVO_ASISTENCIAS, 'w', encoding='utf-8') as f:
                json.dump(asistencias, f, indent=2, ensure_ascii=False)
        return True

    @staticmethod
    def obtener_estadisticas():
        """Estadísticas generales"""
        df = BaseDatos.cargar_matricula()
        if df is not None and not df.empty:
            return {
                'total_alumnos': len(df),
                'grados': df['Grado'].nunique() if 'Grado' in df.columns else 0,
                'con_apoderado': df['Apoderado'].notna().sum() if 'Apoderado' in df.columns else 0
            }
        return {'total_alumnos': 0, 'grados': 0, 'con_apoderado': 0}

    @staticmethod
    def guardar_resultados_examen(resultado):
        """Guarda resultados de examen para el ranking"""
        datos = []
        if Path(ARCHIVO_RESULTADOS).exists():
            with open(ARCHIVO_RESULTADOS, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        datos.append(resultado)
        with open(ARCHIVO_RESULTADOS, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    @staticmethod
    def cargar_resultados_examen():
        """Carga todos los resultados de exámenes"""
        if Path(ARCHIVO_RESULTADOS).exists():
            with open(ARCHIVO_RESULTADOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []


# ================================================================
# GENERADOR PDF - DOCUMENTOS OFICIALES
# ================================================================

class GeneradorPDF:
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

    def _marca_agua_escudo(self):
        """Coloca escudo como marca de agua semitransparente"""
        if Path("escudo_upload.png").exists():
            try:
                self.canvas.saveState()
                self.canvas.setFillAlpha(0.06)
                self.canvas.drawImage(
                    "escudo_upload.png",
                    self.width / 2 - 120,
                    self.height / 2 - 120,
                    width=240, height=240, mask='auto'
                )
                self.canvas.restoreState()
            except Exception:
                pass

    def _dibujar_encabezado(self, titulo):
        """Encabezado estándar con frase del año y título"""
        self.canvas.setFont("Helvetica-Oblique", 11)
        self.canvas.drawCentredString(
            self.width / 2, self.config['y_frase'],
            f'"{self.config["frase"]}"'
        )
        self.canvas.setFont("Helvetica", 11)
        hoy = hora_peru()
        fecha_esp = f"Chinchero, {hoy.day} de {MESES_ESP[hoy.month - 1]} de {self.config['anio']}"
        self.canvas.drawRightString(
            self.width - 60, self.config['y_frase'] - 25, fecha_esp
        )
        self.canvas.setFont("Helvetica-Bold", 16)
        self.canvas.drawCentredString(self.width / 2, self.config['y_titulo'], titulo)
        self.canvas.setLineWidth(1)
        self.canvas.line(
            100, self.config['y_titulo'] - 5,
            self.width - 100, self.config['y_titulo'] - 5
        )

    def _dibujar_parrafo(self, texto, x, y, ancho, estilo):
        """Dibuja un párrafo con reportlab y retorna nueva posición Y"""
        p = Paragraph(texto, estilo)
        w, h = p.wrap(ancho, 600)
        p.drawOn(self.canvas, x, y - h)
        return y - h - 15

    def _agregar_qr(self, datos, tipo_doc):
        """Agrega QR de verificación"""
        data_qr = (
            f"YACHAY|{tipo_doc}|"
            f"{datos.get('alumno', datos.get('Nombre', ''))}|"
            f"{datos.get('dni', datos.get('DNI', ''))}|"
            f"{hora_peru().strftime('%d/%m/%Y')}"
        )
        qr = qrcode.QRCode(box_size=10, border=1)
        qr.add_data(data_qr)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        temp_qr = "temp_qr.png"
        img_qr.save(temp_qr)
        self.canvas.drawImage(
            temp_qr,
            self.config['qr_x'], self.config['qr_y'],
            width=70, height=70
        )
        self.canvas.setFont("Helvetica", 6)
        self.canvas.drawCentredString(
            self.config['qr_x'] + 35,
            self.config['qr_y'] - 5,
            "CÓDIGO DE VERIFICACIÓN"
        )
        try:
            os.remove(temp_qr)
        except Exception:
            pass

    def _agregar_solicitante(self, datos, y):
        """Texto de solicitud del apoderado"""
        apoderado = datos.get('apoderado', datos.get('Apoderado', '')).upper()
        dni_apo = datos.get('dni_apo', datos.get('DNI_Apoderado', ''))
        estilo = ParagraphStyle(
            'Solicitud', parent=self.styles['Normal'],
            fontSize=10, leading=14, alignment=TA_JUSTIFY
        )
        texto = (
            f"Se expide el presente documento a solicitud del Sr(a). "
            f"<b>{apoderado}</b> con DNI N° <b>{dni_apo}</b>."
        )
        return self._dibujar_parrafo(texto, 60, y, self.width - 120, estilo)

    def _agregar_firmas(self):
        """Firma de la directora"""
        yf = 110
        self.canvas.line(200, yf, 395, yf)
        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawCentredString(
            self.width / 2, yf - 15,
            self.config['directora'].upper()
        )
        self.canvas.setFont("Helvetica", 9)
        self.canvas.drawCentredString(self.width / 2, yf - 28, "DIRECTORA")

    def _finalizar(self):
        """Guarda y retorna el PDF"""
        self.canvas.save()
        self.buffer.seek(0)
        return self.buffer

    # ---- CONSTANCIA DE VACANTE (con SIAGIE) ----
    def generar_constancia_vacante(self, datos):
        self._aplicar_fondo()
        self._marca_agua_escudo()
        self._dibujar_encabezado("CONSTANCIA DE VACANTE")

        y = self.config['y_titulo'] - 50
        mx = 60
        ancho = self.width - 120
        estilo = ParagraphStyle(
            'Normal', parent=self.styles['Normal'],
            fontSize=11, leading=15, alignment=TA_JUSTIFY
        )
        estilo_lista = ParagraphStyle(
            'Lista', parent=estilo, leftIndent=25
        )

        y = self._dibujar_parrafo(
            "La Dirección de la Institución Educativa Particular "
            "ALTERNATIVO YACHAY de Chinchero, debidamente representada "
            "por su Directora, suscribe la presente:",
            mx, y, ancho, estilo
        )

        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "CONSTANCIA DE VACANTE")
        y -= 25

        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        dni = datos.get('dni', datos.get('DNI', ''))
        grado = datos.get('grado', datos.get('Grado', '')).upper()

        y = self._dibujar_parrafo(
            f"Que, mediante el presente documento se hace constar que la "
            f"Institución Educativa cuenta con <b>VACANTE DISPONIBLE</b> "
            f"en el nivel de {grado}, para el/la estudiante "
            f"<b>{alumno}</b>, identificado(a) con DNI N° <b>{dni}</b>, "
            f"correspondiente al año escolar <b>{self.config['anio']}</b>.",
            mx, y, ancho, estilo
        )

        y = self._dibujar_parrafo(
            "Para formalizar la matrícula, el/la solicitante deberá "
            "presentar la siguiente documentación:",
            mx, y, ancho, estilo
        )

        requisitos = [
            "• Certificado Oficial de Estudios del SIAGIE (original).",
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

    # ---- CONSTANCIA DE NO ADEUDO ----
    def generar_constancia_no_deudor(self, datos):
        self._aplicar_fondo()
        self._marca_agua_escudo()
        self._dibujar_encabezado("CONSTANCIA DE NO ADEUDO")

        y = self.config['y_titulo'] - 50
        mx = 60
        ancho = self.width - 120
        estilo = ParagraphStyle(
            'Normal', parent=self.styles['Normal'],
            fontSize=11, leading=15, alignment=TA_JUSTIFY
        )

        y = self._dibujar_parrafo(
            "La Dirección de la Institución Educativa Particular "
            "ALTERNATIVO YACHAY, debidamente representada por su Directora:",
            mx, y, ancho, estilo
        )

        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "HACE CONSTAR:")
        y -= 25

        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        dni = datos.get('dni', datos.get('DNI', ''))

        y = self._dibujar_parrafo(
            f"Que el/la estudiante <b>{alumno}</b>, identificado(a) con "
            f"DNI N° <b>{dni}</b>, ha cumplido satisfactoriamente con todas "
            f"sus obligaciones económicas ante esta Institución Educativa, "
            f"no registrando deuda alguna.",
            mx, y, ancho, estilo
        )

        y = self._agregar_solicitante(datos, y)
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE NO ADEUDO")
        return self._finalizar()

    # ---- CONSTANCIA DE ESTUDIOS (con SIAGIE) ----
    def generar_constancia_estudios(self, datos):
        self._aplicar_fondo()
        self._marca_agua_escudo()
        self._dibujar_encabezado("CONSTANCIA DE ESTUDIOS")

        y = self.config['y_titulo'] - 50
        mx = 60
        ancho = self.width - 120
        estilo = ParagraphStyle(
            'Normal', parent=self.styles['Normal'],
            fontSize=11, leading=15, alignment=TA_JUSTIFY
        )

        y = self._dibujar_parrafo(
            "La Dirección de la Institución Educativa Particular "
            "ALTERNATIVO YACHAY, debidamente representada por su Directora:",
            mx, y, ancho, estilo
        )

        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "HACE CONSTAR:")
        y -= 25

        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        dni = datos.get('dni', datos.get('DNI', ''))
        grado = datos.get('grado', datos.get('Grado', '')).upper()

        y = self._dibujar_parrafo(
            f"Que el/la estudiante <b>{alumno}</b>, identificado(a) con "
            f"DNI N° <b>{dni}</b>, se encuentra <b>DEBIDAMENTE "
            f"MATRICULADO(A)</b> en esta Institución Educativa para el "
            f"año académico <b>{self.config['anio']}</b>, cursando estudios "
            f"en el nivel de <b>{grado}</b>, conforme consta en los "
            f"registros oficiales del plantel y el Sistema SIAGIE.",
            mx, y, ancho, estilo
        )

        y = self._agregar_solicitante(datos, y)
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE ESTUDIOS")
        return self._finalizar()

    # ---- CONSTANCIA DE CONDUCTA ----
    def generar_constancia_conducta(self, datos):
        self._aplicar_fondo()
        self._marca_agua_escudo()
        self._dibujar_encabezado("CONSTANCIA DE CONDUCTA")

        y = self.config['y_titulo'] - 50
        mx = 60
        ancho = self.width - 120
        estilo = ParagraphStyle(
            'Normal', parent=self.styles['Normal'],
            fontSize=10, leading=14, alignment=TA_JUSTIFY
        )

        y = self._dibujar_parrafo(
            "La Dirección de la Institución Educativa Particular "
            "ALTERNATIVO YACHAY, debidamente representada por su Directora:",
            mx, y, ancho, estilo
        )

        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.drawString(mx, y, "CERTIFICA:")
        y -= 25

        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        dni = datos.get('dni', datos.get('DNI', ''))

        y = self._dibujar_parrafo(
            f"Que el/la estudiante <b>{alumno}</b>, con DNI N° <b>{dni}</b>, "
            f"cursó estudios en esta institución, obteniendo las siguientes "
            f"calificaciones en <b>CONDUCTA</b>:",
            mx, y, ancho, estilo
        )

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
        grados_conducta = ["PRIMERO", "SEGUNDO", "TERCERO", "CUARTO", "QUINTO"]
        anio_base = int(self.config['anio']) - 5
        for i, grado_c in enumerate(grados_conducta):
            nota = datos.get(f'nota_conducta_{i + 1}', 'AD')
            self.canvas.drawString(tx, y, grado_c)
            self.canvas.drawString(tx + 120, y, str(anio_base + i + 1))
            self.canvas.drawString(tx + 280, y, nota)
            y -= 18

        y -= 10
        y = self._agregar_solicitante(datos, y)
        self._agregar_firmas()
        self._agregar_qr(datos, "CONSTANCIA DE CONDUCTA")
        return self._finalizar()

    # ---- CARTA DE COMPROMISO ----
    def generar_carta_compromiso(self, datos):
        self._aplicar_fondo()
        self._marca_agua_escudo()
        self._dibujar_encabezado("CARTA DE COMPROMISO DEL PADRE DE FAMILIA")

        y = self.config['y_titulo'] - 40
        mx = 50
        ancho = self.width - 100
        estilo = ParagraphStyle(
            'Comp', parent=self.styles['Normal'],
            fontSize=8.5, leading=11, alignment=TA_JUSTIFY
        )
        estilo_item = ParagraphStyle(
            'Item', parent=estilo, leftIndent=10
        )

        apoderado = datos.get('apoderado', datos.get('Apoderado', '')).upper()
        dni_apo = datos.get('dni_apo', datos.get('DNI_Apoderado', ''))
        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        grado = datos.get('grado', datos.get('Grado', '')).upper()

        y = self._dibujar_parrafo(
            f"Yo, <b>{apoderado}</b>, con DNI N° <b>{dni_apo}</b>, "
            f"padre/madre/apoderado(a) de <b>{alumno}</b>, estudiante "
            f"del <b>{grado}</b>, me comprometo formalmente a cumplir:",
            mx, y, ancho, estilo
        )
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
            "14. Respetar la autonomía pedagógica de la institución."
        ]
        for compromiso in compromisos:
            y = self._dibujar_parrafo(compromiso, mx, y, ancho, estilo_item)
            y += 2

        y -= 5
        y = self._dibujar_parrafo(
            "Declaro conocer y aceptar el cumplimiento de lo establecido.",
            mx, y, ancho, estilo
        )

        y = 120
        self.canvas.line(80, y, 200, y)
        self.canvas.line(220, y, 340, y)
        self.canvas.line(360, y, 480, y)
        y -= 10
        self.canvas.setFont("Helvetica-Bold", 7)
        self.canvas.drawCentredString(140, y, "FIRMA PADRE/MADRE")
        self.canvas.drawCentredString(280, y, self.config['directora'].upper())
        self.canvas.drawCentredString(280, y - 10, "DIRECTORA")
        self.canvas.drawCentredString(420, y, self.config['promotor'].upper())
        self.canvas.drawCentredString(420, y - 10, "PROMOTOR")
        return self._finalizar()

    # ---- RESOLUCIÓN DE TRASLADO ----
    def generar_resolucion_traslado(self, datos):
        self._aplicar_fondo()
        self._marca_agua_escudo()

        self.canvas.setFont("Helvetica-Oblique", 11)
        self.canvas.drawCentredString(
            self.width / 2, 700, f'"{self.config["frase"]}"'
        )

        y = 670
        self.canvas.setFont("Helvetica-Bold", 14)
        self.canvas.drawCentredString(
            self.width / 2, y,
            f"RESOLUCIÓN DIRECTORAL N° {datos.get('num_resolucion', '')}"
        )
        y -= 30
        self.canvas.setFont("Helvetica", 11)
        self.canvas.drawCentredString(
            self.width / 2, y,
            datos.get('fecha_resolucion', '')
        )
        y -= 40
        mx = 60
        ancho = self.width - 120
        estilo = ParagraphStyle(
            'Normal', parent=self.styles['Normal'],
            fontSize=11, leading=15, alignment=TA_JUSTIFY
        )

        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        nivel = datos.get('nivel', '').upper()

        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawString(mx, y, "VISTO:")
        y -= 20

        y = self._dibujar_parrafo(
            f"La solicitud del(a) apoderado(a), de <b>{alumno}</b> "
            f"y el informe de progreso de <b>{nivel}</b>.",
            mx, y, ancho, estilo
        )

        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawString(mx, y, "CONSIDERANDO:")
        y -= 20

        y = self._dibujar_parrafo(
            "Que, es procedente autorizar el traslado de matrícula "
            "a fin de garantizar la continuidad de estudios.",
            mx, y, ancho, estilo
        )

        y = self._dibujar_parrafo(
            "De conformidad con la Ley de Educación N°28044 y la "
            "RM 474-2022 MINEDU.",
            mx, y, ancho, estilo
        )

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


# ================================================================
# REGISTRO AUXILIAR PDF (5 Competencias x 4 Capacidades)
# ================================================================

def generar_registro_auxiliar_pdf(grado, seccion, anio, bimestre, estudiantes_df):
    """
    Genera PDF del registro auxiliar:
    - 5 Competencias (COMP 1 a COMP 5)
    - 4 Capacidades por competencia (C1, C2, C3, C4)
    - Orden alfabético
    - Nombres que encajan en la columna
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    w, h = landscape(A4)

    # Marca de agua
    if Path("escudo_upload.png").exists():
        try:
            c.saveState()
            c.setFillAlpha(0.05)
            c.drawImage("escudo_upload.png", w / 2 - 100, h / 2 - 100,
                        200, 200, mask='auto')
            c.restoreState()
        except Exception:
            pass

    # Título
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(w / 2, h - 25,
                        "I.E.P. ALTERNATIVO YACHAY - REGISTRO AUXILIAR DE EVALUACIÓN")
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, h - 40,
                        f"Grado: {grado} | Sección: {seccion} | {bimestre} | Año: {anio}")
    c.drawCentredString(w / 2, h - 53,
                        '"EDUCAR PARA LA VIDA - PIONEROS EN LA EDUCACIÓN DE CALIDAD"')

    # Encabezados: 2 filas
    # Fila 1: N° | NOMBRES | COMP1(span 4) | COMP2(span 4) | ... | COMP5(span 4)
    # Fila 2: (vacío) | (vacío) | C1 C2 C3 C4 | C1 C2 C3 C4 | ...
    header_row1 = ["N°", "APELLIDOS Y NOMBRES"]
    for i in range(1, 6):
        header_row1.append(f"COMPETENCIA {i}")
        header_row1.extend(["", "", ""])

    header_row2 = ["", ""]
    for i in range(5):
        header_row2.extend(["C1", "C2", "C3", "C4"])

    # Estudiantes ordenados alfabéticamente
    if not estudiantes_df.empty:
        est = estudiantes_df.sort_values('Nombre').reset_index(drop=True)
    else:
        est = pd.DataFrame()

    data = [header_row1, header_row2]
    num_estudiantes = len(est) if not est.empty else 25

    for idx in range(num_estudiantes):
        if idx < len(est):
            nombre = est.iloc[idx].get('Nombre', '')
        else:
            nombre = ""
        # Truncar nombre para que quepa
        if len(nombre) > 32:
            nombre = nombre[:32] + "."
        fila = [str(idx + 1), nombre] + [""] * 20
        data.append(fila)

    # Anchos de columna
    # N°=22, Nombre=148, 20 capacidades × 28 = 560
    # Total ≈ 730, landscape A4 ≈ 842
    col_widths = [22, 148] + [28] * 20

    tabla = Table(data, colWidths=col_widths, repeatRows=2)

    styles_list = [
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 1), 6),
        ('FONTSIZE', (0, 2), (-1, -1), 6.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 2), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 1), colors.Color(0, 0.2, 0.5)),
        ('TEXTCOLOR', (0, 0), (-1, 1), colors.white),
        ('ROWBACKGROUNDS', (0, 2), (-1, -1),
         [colors.white, colors.Color(0.95, 0.95, 1)]),
    ]

    # Merge competencia headers en fila 0
    for i in range(5):
        col_start = 2 + i * 4
        col_end = col_start + 3
        styles_list.append(('SPAN', (col_start, 0), (col_end, 0)))
        bg = colors.Color(0, 0.25, 0.55) if i % 2 == 0 else colors.Color(0, 0.15, 0.45)
        styles_list.append(('BACKGROUND', (col_start, 0), (col_end, 0), bg))
        styles_list.append(('BACKGROUND', (col_start, 1), (col_end, 1), bg))

    tabla.setStyle(TableStyle(styles_list))
    tw, th_t = tabla.wrap(w - 40, h - 80)
    tabla.drawOn(c, 20, h - 65 - th_t)

    # Pie de página
    c.setFont("Helvetica", 6)
    c.drawString(20, 15,
                 f"COMP=Competencia | C1-C4=Capacidades | "
                 f"AD(18-20) A(14-17) B(11-13) C(0-10) | "
                 f"Sistema YACHAY PRO - {anio}")

    c.save()
    buffer.seek(0)
    return buffer


# ================================================================
# REGISTRO DE ASISTENCIA PDF (Sin fines de semana, sin feriados)
# ================================================================

def generar_registro_asistencia_pdf(grado, seccion, anio, estudiantes_df, meses_sel):
    """
    Genera PDF de asistencia:
    - Solo días hábiles (L-V)
    - Excluye feriados de Perú
    - Cada día muestra número + día semana
    - Selección de meses específicos
    - Orden alfabético
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    w, h = landscape(A4)

    # Ordenar estudiantes alfabéticamente
    if not estudiantes_df.empty:
        est = estudiantes_df.sort_values('Nombre').reset_index(drop=True)
    else:
        est = pd.DataFrame()

    dias_semana = {0: "L", 1: "M", 2: "Mi", 3: "J", 4: "V"}

    for mi, mes_num in enumerate(meses_sel):
        if mi > 0:
            c.showPage()

        mes_nombre = MESES_ESCOLARES.get(mes_num, f"Mes {mes_num}")

        # Marca de agua
        if Path("escudo_upload.png").exists():
            try:
                c.saveState()
                c.setFillAlpha(0.05)
                c.drawImage("escudo_upload.png", w / 2 - 100, h / 2 - 100,
                            200, 200, mask='auto')
                c.restoreState()
            except Exception:
                pass

        # Encabezado
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(w / 2, h - 22,
                            "I.E.P. ALTERNATIVO YACHAY - REGISTRO DE ASISTENCIA")
        c.setFont("Helvetica", 8)
        c.drawCentredString(w / 2, h - 35,
                            f"Grado: {grado} | Sección: {seccion} | "
                            f"Mes: {mes_nombre} | Año: {anio}")

        # Obtener días hábiles del mes
        dias = dias_habiles_mes(int(anio), mes_num)
        ndias = len(dias)

        # Header con día + letra del día de la semana
        header = ["N°", "APELLIDOS Y NOMBRES"]
        for d in dias:
            dt = date(int(anio), mes_num, d)
            header.append(f"{d}\n{dias_semana[dt.weekday()]}")
        header.extend(["A", "T", "F", "J"])

        # Data
        data = [header]
        num_est = len(est) if not est.empty else 25
        for idx in range(num_est):
            if idx < len(est):
                nombre = est.iloc[idx].get('Nombre', '')
            else:
                nombre = ""
            if len(nombre) > 32:
                nombre = nombre[:32] + "."
            fila = [str(idx + 1), nombre] + [""] * ndias + ["", "", "", ""]
            data.append(fila)

        # Calcular anchos dinámicos
        dias_width = max(15, min(22, (w - 18 - 140 - 72 - 30) / max(ndias, 1)))
        col_widths = [18, 140] + [dias_width] * ndias + [18, 18, 18, 18]

        tabla = Table(data, colWidths=col_widths, repeatRows=1)
        tabla.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 5),
            ('FONTSIZE', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0, 0.3, 0.15)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
             [colors.white, colors.Color(0.95, 1, 0.95)]),
            ('BACKGROUND', (-4, 0), (-1, 0), colors.Color(0.6, 0, 0)),
        ]))

        tw, th_t = tabla.wrap(w - 20, h - 60)
        tabla.drawOn(c, 10, h - 48 - th_t)

        # Pie de página
        c.setFont("Helvetica", 5)
        c.drawString(10, 8,
                     f"A=Asistió | T=Tardanza | F=Falta | J=Justificada | "
                     f"Sin sábados/domingos ni feriados | {anio}")

    c.save()
    buffer.seek(0)
    return buffer


# ================================================================
# RANKING PDF
# ================================================================

def generar_ranking_pdf(resultados, anio):
    """Genera PDF completo del ranking con todos los estudiantes"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    # Marca de agua
    if Path("escudo_upload.png").exists():
        try:
            c.saveState()
            c.setFillAlpha(0.06)
            c.drawImage("escudo_upload.png", w / 2 - 100, h / 2 - 100,
                        200, 200, mask='auto')
            c.restoreState()
        except Exception:
            pass

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w / 2, h - 40, "I.E.P. ALTERNATIVO YACHAY")
    c.setFont("Helvetica", 11)
    c.drawCentredString(w / 2, h - 58,
                        '"EDUCAR PARA LA VIDA - PIONEROS EN LA EDUCACIÓN DE CALIDAD"')
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w / 2, h - 85,
                        f"RANKING DE RESULTADOS - {anio}")
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, h - 100,
                        f"Generado: {hora_peru().strftime('%d/%m/%Y %H:%M')}")

    # Ordenar por promedio
    ranking = sorted(resultados,
                     key=lambda r: r.get('promedio_general', 0),
                     reverse=True)

    # Áreas únicas
    all_areas = set()
    for r in ranking:
        for a in r.get('areas', []):
            all_areas.add(a['nombre'])
    all_areas = sorted(all_areas)

    # Tabla header
    header = ["#", "APELLIDOS Y NOMBRES", "DNI"]
    header.extend(all_areas)
    header.append("PROM.")

    data = [header]
    for idx, r in enumerate(ranking):
        fila = [str(idx + 1), r.get('nombre', ''), r.get('dni', '')]
        area_notas = {a['nombre']: str(a['nota']) for a in r.get('areas', [])}
        for area in all_areas:
            fila.append(area_notas.get(area, '-'))
        fila.append(str(r.get('promedio_general', 0)))
        data.append(fila)

    # Anchos
    n_areas = len(all_areas)
    col_widths = [25, 160, 60] + [45] * n_areas + [45]

    tabla = Table(data, colWidths=col_widths, repeatRows=1)

    style_list = [
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.1, 0.1, 0.4)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.white, colors.Color(0.95, 0.95, 1)]),
    ]

    # Highlight top 3
    bg_top = [
        colors.Color(1, 0.84, 0),      # Oro
        colors.Color(0.75, 0.75, 0.75), # Plata
        colors.Color(0.8, 0.5, 0.2),    # Bronce
    ]
    for i in range(min(3, len(ranking))):
        style_list.append(('BACKGROUND', (0, i + 1), (-1, i + 1), bg_top[i]))

    tabla.setStyle(TableStyle(style_list))
    tw, th_t = tabla.wrap(w - 60, h - 150)
    tabla.drawOn(c, 30, h - 120 - th_t)

    # Footer
    c.setFont("Helvetica", 7)
    c.drawCentredString(w / 2, 30,
                        f"Sistema YACHAY PRO - Ranking generado el "
                        f"{hora_peru().strftime('%d/%m/%Y %H:%M')}")

    c.save()
    buffer.seek(0)
    return buffer


# ================================================================
# GENERADOR DE CARNETS
# ================================================================

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

    def _aplicar_escudo_fondo(self):
        """Escudo como marca de agua semitransparente"""
        if Path("escudo_upload.png").exists():
            try:
                escudo = Image.open("escudo_upload.png").convert("RGBA")
                escudo = escudo.resize((280, 280), Image.LANCZOS)
                capa = Image.new('RGBA', (self.WIDTH, self.HEIGHT), (255, 255, 255, 0))
                x = (self.WIDTH - 280) // 2
                y = (self.HEIGHT - 280) // 2
                capa.paste(escudo, (x, y))
                datos_pixel = list(capa.getdata())
                nuevos = [(d[0], d[1], d[2], min(d[3], 28)) for d in datos_pixel]
                capa.putdata(nuevos)
                base = self.img.convert('RGBA')
                base = Image.alpha_composite(base, capa)
                self.img = base.convert('RGB')
                self.draw = ImageDraw.Draw(self.img)
            except Exception:
                pass

    def _dibujar_barras(self):
        """Barras azules superior e inferior con líneas doradas"""
        self.draw.rectangle([(0, 0), (self.WIDTH, 210)], fill=self.AZUL)
        self.draw.rectangle([(0, 207), (self.WIDTH, 213)], fill=self.DORADO)
        self.draw.rectangle([(0, self.HEIGHT - 65), (self.WIDTH, self.HEIGHT)],
                            fill=self.AZUL)
        self.draw.rectangle([(0, self.HEIGHT - 68), (self.WIDTH, self.HEIGHT - 63)],
                            fill=self.DORADO)

    def _dibujar_textos(self):
        """Textos del encabezado y pie dorado"""
        font_h = RecursoManager.obtener_fuente("", 36, bold=True)
        font_m = RecursoManager.obtener_fuente("", 19, bold=True)
        font_c = RecursoManager.obtener_fuente("", 17, bold=True)
        font_p = RecursoManager.obtener_fuente("", 13, bold=True)

        self.draw.text((self.WIDTH // 2, 65), "I.E. ALTERNATIVO YACHAY",
                       font=font_h, fill="white", anchor="mm")
        self.draw.text((self.WIDTH // 2, 115), '"EDUCAR PARA LA VIDA"',
                       font=font_m, fill=self.DORADO, anchor="mm")
        self.draw.text((self.WIDTH // 2, 160),
                       f"CARNET ESCOLAR {self.anio}",
                       font=font_c, fill="white", anchor="mm")
        # Texto pie dorado
        self.draw.text((self.WIDTH // 2, self.HEIGHT - 35),
                       "PIONEROS EN LA EDUCACIÓN DE CALIDAD",
                       font=font_p, fill=self.DORADO, anchor="mm")

    def _insertar_foto(self):
        """Inserta foto del estudiante o placeholder"""
        x, y_pos, w_f, h_f = 40, 228, 220, 280
        if self.foto_bytes:
            try:
                foto = Image.open(self.foto_bytes).convert("RGB")
                foto = foto.resize((w_f, h_f), Image.LANCZOS)
                self.img.paste(foto, (x, y_pos))
            except Exception:
                self._placeholder(x, y_pos, w_f, h_f)
        else:
            self._placeholder(x, y_pos, w_f, h_f)
        # Marco dorado
        self.draw.rectangle(
            [(x - 3, y_pos - 3), (x + w_f + 3, y_pos + h_f + 3)],
            outline=self.DORADO, width=4
        )

    def _placeholder(self, x, y, w, h):
        """Placeholder cuando no hay foto"""
        self.draw.rectangle([(x, y), (x + w, y + h)], fill="#eeeeee")
        font = RecursoManager.obtener_fuente("", 15)
        self.draw.text((x + w // 2, y + h // 2), "SIN FOTO",
                       font=font, fill="#999999", anchor="mm")

    def _dibujar_datos(self):
        """Datos del estudiante"""
        x_t = 290
        nombre = self.datos.get('alumno', self.datos.get('Nombre', '')).upper()
        dni = str(self.datos.get('dni', self.datos.get('DNI', '')))
        grado = self.datos.get('grado', self.datos.get('Grado', 'N/A')).upper()
        seccion = self.datos.get('seccion', self.datos.get('Seccion', ''))

        font_n = RecursoManager.obtener_fuente(
            "", 19 if len(nombre) > 25 else 22, bold=True
        )
        font_l = RecursoManager.obtener_fuente("", 14, bold=True)
        font_d = RecursoManager.obtener_fuente("", 14)

        y_cursor = 240
        if len(nombre) > 28:
            wrapper = textwrap.TextWrapper(width=28)
            for linea in wrapper.wrap(nombre)[:3]:
                self.draw.text((x_t, y_cursor), linea,
                               font=font_n, fill="black")
                y_cursor += 26
        else:
            self.draw.text((x_t, y_cursor), nombre,
                           font=font_n, fill="black")
            y_cursor += 30

        y_cursor += 8
        self.draw.text((x_t, y_cursor), "DNI:", font=font_l, fill="black")
        self.draw.text((x_t + 60, y_cursor), dni, font=font_d, fill="black")
        y_cursor += 28

        self.draw.text((x_t, y_cursor), "GRADO:", font=font_l, fill="black")
        self.draw.text((x_t + 90, y_cursor), grado, font=font_d, fill="black")
        y_cursor += 28

        if seccion:
            self.draw.text((x_t, y_cursor), "SECCIÓN:",
                           font=font_l, fill="black")
            self.draw.text((x_t + 110, y_cursor), str(seccion),
                           font=font_d, fill="black")
            y_cursor += 28

        self.draw.text((x_t, y_cursor), "VIGENCIA:",
                       font=font_l, fill="black")
        self.draw.text((x_t + 120, y_cursor), str(self.anio),
                       font=font_d, fill="black")

    def _agregar_qr(self):
        """QR con solo el DNI (para escaneo de asistencia)"""
        try:
            dni = str(self.datos.get('dni', self.datos.get('DNI', '')))
            qr = qrcode.QRCode(box_size=8, border=1)
            qr.add_data(dni)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="black", back_color="white")
            img_qr = img_qr.resize((140, 140), Image.LANCZOS)
            x_qr = self.WIDTH - 180
            y_qr = 240
            self.img.paste(img_qr, (x_qr, y_qr))
            font_s = RecursoManager.obtener_fuente("", 9, bold=True)
            self.draw.text((x_qr + 70, y_qr + 145), "ESCANEAR QR",
                           font=font_s, fill="black", anchor="mm")
        except Exception:
            pass

    def _agregar_barcode(self):
        """Código de barras SIN texto (evita choque con números)"""
        if not HAS_BARCODE:
            return
        try:
            dni = str(self.datos.get('dni', self.datos.get('DNI', '')))
            writer = ImageWriter()
            buf = io.BytesIO()
            Code128(dni, writer=writer).write(buf, options={
                'write_text': False,
                'module_width': 0.4,
                'module_height': 8,
                'quiet_zone': 2
            })
            buf.seek(0)
            img_bar = Image.open(buf)
            img_bar = img_bar.crop(img_bar.getbbox())
            img_bar = img_bar.resize((280, 45), Image.LANCZOS)
            x_bar = (self.WIDTH - 280) // 2
            y_bar = self.HEIGHT - 120
            self.img.paste(img_bar, (x_bar, y_bar))
            # DNI texto separado debajo del barcode
            font_bc = RecursoManager.obtener_fuente("", 10, bold=True)
            self.draw.text((self.WIDTH // 2, y_bar + 50),
                           f"DNI: {dni}",
                           font=font_bc, fill="black", anchor="mm")
        except Exception:
            pass

    def generar(self):
        """Genera el carnet completo"""
        self._aplicar_escudo_fondo()
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


# ================================================================
# UTILIDADES
# ================================================================

def generar_link_whatsapp(telefono, mensaje):
    """Genera link de WhatsApp con número peruano"""
    tel = str(telefono).strip().replace("+", "").replace(" ", "").replace("-", "")
    if len(tel) == 9:
        tel = "51" + tel
    elif not tel.startswith("51"):
        tel = "51" + tel
    return f"https://wa.me/{tel}?text={urllib.parse.quote(mensaje)}"


def generar_mensaje_asistencia(nombre, tipo, hora):
    """Genera mensaje de asistencia para WhatsApp"""
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
    """Decodifica QR/barcode desde imagen de cámara"""
    if not HAS_PYZBAR:
        return None
    try:
        img = Image.open(io.BytesIO(image_bytes))
        codigos = pyzbar_decode(img)
        if codigos:
            return codigos[0].data.decode('utf-8')
    except Exception:
        pass
    # Fallback con OpenCV preprocessing
    if HAS_CV2:
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            for method in [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV]:
                _, thresh = cv2.threshold(gray, 127, 255, method)
                pil_img = Image.fromarray(thresh)
                codigos = pyzbar_decode(pil_img)
                if codigos:
                    return codigos[0].data.decode('utf-8')
        except Exception:
            pass
    return None


# ================================================================
# PANTALLA DE LOGIN
# ================================================================

def pantalla_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Mostrar escudo grande si existe
        if Path("escudo_upload.png").exists():
            st.image("escudo_upload.png", width=220, use_container_width=False)

        st.markdown("""
        <div class='main-header'>
            <h1 style='color:white;margin:0;font-size:2.2rem;'>🎓 SISTEMA YACHAY PRO</h1>
            <p style='color:#ccc;margin:5px 0;'>Sistema Integral de Gestión Educativa</p>
            <p style='color:#FFD700;font-style:italic;font-size:1.1rem;'>"Educar para la Vida"</p>
            <p style='color:#FFD700;font-size:0.9rem;'>Pioneros en la Educación de Calidad</p>
            <hr style='border-color:#FFD700;margin:15px 50px;'>
            <p style='color:#aaa;font-size:0.85rem;'>📍 Chinchero, Cusco - Perú</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        pwd = st.text_input("🔑 Contraseña de acceso:", type="password", key="login_pwd")

        if st.button("🔐 INGRESAR AL SISTEMA", use_container_width=True, type="primary"):
            # Roles fijos
            if pwd == "306020":
                st.session_state.rol = "admin"
                st.session_state.docente_info = None
                st.rerun()
            elif pwd == "deyanira":
                st.session_state.rol = "directivo"
                st.session_state.docente_info = None
                st.rerun()
            elif pwd == "123456789":
                st.session_state.rol = "auxiliar"
                st.session_state.docente_info = None
                st.rerun()
            elif pwd in DOCENTES_PASSWORDS:
                st.session_state.rol = "docente"
                st.session_state.docente_info = DOCENTES_PASSWORDS[pwd]
                st.rerun()
            else:
                st.error("⛔ Contraseña incorrecta")

        with st.expander("ℹ️ Accesos al sistema"):
            st.caption("**Admin:** 306020 | **Directivo:** deyanira | **Auxiliar:** 123456789")
            st.caption("**Docentes por grado:**")
            for pw, info in DOCENTES_PASSWORDS.items():
                st.caption(f"  • {info['label']}: `{pw}`")


# ================================================================
# SIDEBAR
# ================================================================

def configurar_sidebar():
    with st.sidebar:
        st.title("🎓 YACHAY PRO")

        roles_nombres = {
            "admin": "⚙️ Administrador",
            "directivo": "📋 Directivo",
            "auxiliar": "👤 Auxiliar",
            "docente": "👨‍🏫 Docente"
        }
        label_rol = roles_nombres.get(st.session_state.rol, '')
        if st.session_state.rol == "docente" and st.session_state.docente_info:
            label_rol += f" - {st.session_state.docente_info['label']}"
        st.info(f"**{label_rol}**")

        st.caption(f"🕒 {hora_peru().strftime('%H:%M:%S')} | 📅 {hora_peru().strftime('%d/%m/%Y')}")
        st.markdown("---")

        directora = "Prof. Ana María CUSI INCA"
        promotor = "Prof. Leandro CORDOVA TOCRE"
        frase = "Año de la Esperanza y el Fortalecimiento de la Democracia"

        if st.session_state.rol == "admin":
            with st.expander("📂 Archivos", expanded=False):
                up_bd = st.file_uploader("📊 Base Datos (.xlsx)", type=["xlsx"], key="upload_bd")
                if up_bd:
                    with open(ARCHIVO_BD, "wb") as f:
                        f.write(up_bd.getbuffer())
                    st.success("✅ Base datos actualizada")
                    st.rerun()

                up_fondo = st.file_uploader("🖼️ Fondo docs (.png)", type=["png"], key="upload_fondo")
                if up_fondo:
                    with open("fondo.png", "wb") as f:
                        f.write(up_fondo.getbuffer())
                    st.success("✅ Fondo actualizado")

                up_escudo = st.file_uploader("🛡️ Escudo/Logo (.png)", type=["png"], key="upload_escudo")
                if up_escudo:
                    with open("escudo_upload.png", "wb") as f:
                        f.write(up_escudo.getbuffer())
                    st.success("✅ Escudo actualizado")

            with st.expander("👥 Autoridades", expanded=False):
                directora = st.text_input("Directora:", directora, key="dir_input")
                promotor = st.text_input("Promotor:", promotor, key="prom_input")

            with st.expander("🎯 Título del Año (Perú)", expanded=False):
                frase = st.text_input("Frase/Título del Año:", frase, key="frase_input")
                st.caption("Modifica cada año según decreto del gobierno peruano")

        st.markdown("---")
        anio_sel = st.number_input("📅 Año Escolar:", 2024, 2040, 2026, key="anio_input")

        stats = BaseDatos.obtener_estadisticas()
        st.metric("📚 Total Alumnos", stats['total_alumnos'])

        st.markdown("---")
        if st.button("🔴 CERRAR SESIÓN", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
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


# ================================================================
# TAB: MATRÍCULA
# ================================================================

def tab_matricula(config):
    st.header("📝 Matrícula de Estudiantes")
    tab_reg, tab_lista, tab_pdf = st.tabs([
        "➕ Registrar", "📋 Lista", "⬇️ Registros PDF"
    ])

    with tab_reg:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**👤 Datos del Estudiante**")
            nombre_est = st.text_input("Apellidos y Nombres:", key="mat_nombre")
            dni_est = st.text_input("DNI del Estudiante:", key="mat_dni", max_chars=8)
            nivel = st.selectbox("Nivel:", list(NIVELES_GRADOS.keys()), key="mat_nivel")
            grado = st.selectbox("Grado:", NIVELES_GRADOS[nivel], key="mat_grado")
            seccion = st.selectbox("Sección:", SECCIONES, key="mat_seccion")
        with col2:
            st.markdown("**👨‍👩‍👧 Datos del Apoderado**")
            nombre_apo = st.text_input("Nombres del Apoderado:", key="mat_apoderado")
            dni_apo = st.text_input("DNI del Apoderado:", key="mat_dni_apo", max_chars=8)
            celular_apo = st.text_input("Celular del Apoderado:", key="mat_celular",
                                        max_chars=9, placeholder="987654321")

        if st.button("✅ MATRICULAR", type="primary", use_container_width=True, key="btn_mat"):
            if nombre_est and dni_est and grado:
                BaseDatos.registrar_estudiante({
                    'Nombre': nombre_est.strip(),
                    'DNI': dni_est.strip(),
                    'Nivel': nivel,
                    'Grado': grado,
                    'Seccion': seccion,
                    'Apoderado': nombre_apo.strip(),
                    'DNI_Apoderado': dni_apo.strip(),
                    'Celular_Apoderado': celular_apo.strip()
                })
                st.success(f"✅ **{nombre_est}** matriculado en **{grado} - {seccion}**")
                st.balloons()
            else:
                st.error("⚠️ Complete: Nombre, DNI y Grado")

    with tab_lista:
        df = BaseDatos.cargar_matricula()
        if not df.empty:
            c1, c2, c3 = st.columns(3)
            with c1:
                fil_nivel = st.selectbox("Nivel:", ["Todos"] + list(NIVELES_GRADOS.keys()), key="fn")
            with c2:
                grados_opts = ["Todos"] + (
                    NIVELES_GRADOS[fil_nivel] if fil_nivel != "Todos" else TODOS_LOS_GRADOS
                )
                fil_grado = st.selectbox("Grado:", grados_opts, key="fg")
            with c3:
                busqueda = st.text_input("🔍 Buscar:", key="bq")

            df_filtrado = df.copy()
            if fil_nivel != "Todos" and 'Nivel' in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado['Nivel'] == fil_nivel]
            if fil_grado != "Todos" and 'Grado' in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado['Grado'] == fil_grado]
            if busqueda:
                df_filtrado = df_filtrado[
                    df_filtrado.apply(lambda r: busqueda.lower() in str(r).lower(), axis=1)
                ]
            if 'Nombre' in df_filtrado.columns:
                df_filtrado = df_filtrado.sort_values('Nombre')

            st.metric("Resultados", len(df_filtrado))
            st.dataframe(df_filtrado, use_container_width=True, hide_index=True, height=400)

            # Descargar Excel
            buf_excel = io.BytesIO()
            df_filtrado.to_excel(buf_excel, index=False, engine='openpyxl')
            buf_excel.seek(0)
            st.download_button("⬇️ Descargar Excel", buf_excel,
                               f"Matricula_{config['anio']}.xlsx",
                               key="dl_mat_excel")

            with st.expander("🗑️ Eliminar Estudiante"):
                dni_del = st.text_input("DNI a eliminar:", key="dni_del")
                if st.button("🗑️ Eliminar", key="btn_del"):
                    if dni_del:
                        BaseDatos.eliminar_estudiante(dni_del)
                        st.success("✅ Eliminado")
                        st.rerun()
        else:
            st.info("📝 No hay estudiantes matriculados.")

    with tab_pdf:
        _seccion_registros_pdf(config)


def _seccion_registros_pdf(config):
    """Sección para generar PDFs de registro auxiliar y asistencia"""
    df = BaseDatos.cargar_matricula()
    if df.empty:
        st.info("📝 Registra estudiantes primero.")
        return

    col1, col2 = st.columns(2)
    with col1:
        np_sel = st.selectbox("Nivel:", list(NIVELES_GRADOS.keys()), key="pn")
        gp_sel = st.selectbox("Grado:", NIVELES_GRADOS[np_sel], key="pg")
    with col2:
        sp_sel = st.selectbox("Sección:", ["Todas"] + SECCIONES, key="ps")

    dg = BaseDatos.obtener_estudiantes_grado(gp_sel, sp_sel)
    st.info(f"📊 {len(dg)} estudiantes (orden alfabético)")

    st.markdown("---")
    st.markdown("**📝 Registro Auxiliar (5 Competencias × 4 Capacidades)**")
    bim_sel = st.selectbox("Bimestre:", list(BIMESTRES.keys()), key="bim_sel")
    if st.button("📝 Generar Registro Auxiliar PDF", type="primary",
                 use_container_width=True, key="btn_gen_aux"):
        sec_label = sp_sel if sp_sel != "Todas" else "Todas"
        pdf = generar_registro_auxiliar_pdf(gp_sel, sec_label, config['anio'], bim_sel, dg)
        st.download_button("⬇️ Descargar Registro Auxiliar", pdf,
                           f"RegAuxiliar_{gp_sel}_{bim_sel}.pdf",
                           "application/pdf", key="dl_aux")

    st.markdown("---")
    st.markdown("**📋 Registro de Asistencia (sin fines de semana ni feriados)**")
    meses_opciones = list(MESES_ESCOLARES.items())
    meses_sel = st.multiselect(
        "Selecciona meses:",
        [f"{v} ({k})" for k, v in meses_opciones],
        default=[f"{v} ({k})" for k, v in meses_opciones[:3]],
        key="meses_sel"
    )
    meses_nums = [int(m.split('(')[1].replace(')', '')) for m in meses_sel]

    if st.button("📋 Generar Registro Asistencia PDF", type="primary",
                 use_container_width=True, key="btn_gen_asist"):
        if meses_nums:
            sec_label = sp_sel if sp_sel != "Todas" else "Todas"
            pdf = generar_registro_asistencia_pdf(
                gp_sel, sec_label, config['anio'], dg, meses_nums
            )
            st.download_button("⬇️ Descargar Registro Asistencia", pdf,
                               f"RegAsist_{gp_sel}.pdf",
                               "application/pdf", key="dl_asist")
        else:
            st.warning("Selecciona al menos un mes")


# ================================================================
# TAB: DOCUMENTOS
# ================================================================

def tab_documentos(config):
    st.header("📄 Emisión de Documentos")
    col1, col2 = st.columns([1, 2])

    with col1:
        tipo_doc = st.selectbox("📑 Tipo de Documento:", [
            "CONSTANCIA DE VACANTE", "CONSTANCIA DE NO DEUDOR",
            "CONSTANCIA DE ESTUDIOS", "CONSTANCIA DE CONDUCTA",
            "CARTA COMPROMISO", "RESOLUCIÓN DE TRASLADO"
        ], key="tipo_doc")
        st.markdown("---")
        dni_buscar = st.text_input("🔍 Buscar por DNI:", key="doc_buscar_dni")
        if st.button("🔎 Buscar", use_container_width=True, key="btn_buscar_doc"):
            resultado = BaseDatos.buscar_por_dni(dni_buscar)
            if resultado:
                st.session_state.alumno = resultado.get('Nombre', '')
                st.session_state.dni = resultado.get('DNI', '')
                st.session_state.grado = resultado.get('Grado', '')
                st.session_state.apoderado = resultado.get('Apoderado', '')
                st.session_state.dni_apo = resultado.get('DNI_Apoderado', '')
                st.success("✅ Encontrado")
                st.rerun()
            else:
                st.error("❌ No encontrado")

    with col2:
        with st.container(border=True):
            nombre = st.text_input("👤 Nombre del Estudiante:", key="alumno")
            dni = st.text_input("🆔 DNI:", key="dni")
            grado = st.text_input("📚 Grado:", key="grado")
            apoderado = st.text_input("👨‍👩‍👧 Apoderado:", key="apoderado")
            dni_apo = st.text_input("🆔 DNI Apoderado:", key="dni_apo")

            notas_conducta = {}
            if tipo_doc == "CONSTANCIA DE CONDUCTA":
                cols_notas = st.columns(5)
                for i, col in enumerate(cols_notas):
                    with col:
                        notas_conducta[f'nota_conducta_{i+1}'] = st.selectbox(
                            f"{i+1}° Año", ["AD", "A", "B", "C"], key=f"nota_{i}"
                        )

            extras = {}
            if tipo_doc == "RESOLUCIÓN DE TRASLADO":
                extras['num_resolucion'] = st.text_input("N° Resolución:", key="num_res")
                extras['fecha_resolucion'] = st.text_input("Fecha:", key="fecha_res")
                extras['nivel'] = st.selectbox("Nivel:", ["INICIAL", "PRIMARIA", "SECUNDARIA"], key="nivel_t")
                extras['ie_destino'] = st.text_input("IE Destino:", key="ie_dest")
                extras['nivel_destino'] = st.text_input("Nivel Destino:", key="nivel_dest")

        if st.button("✨ GENERAR DOCUMENTO", type="primary",
                     use_container_width=True, key="btn_gen_doc"):
            if nombre and dni:
                datos = {
                    'alumno': nombre, 'dni': dni, 'grado': grado,
                    'apoderado': apoderado, 'dni_apo': dni_apo,
                    **notas_conducta, **extras
                }
                gen = GeneradorPDF(config)
                metodos = {
                    "CONSTANCIA DE VACANTE": gen.generar_constancia_vacante,
                    "CONSTANCIA DE NO DEUDOR": gen.generar_constancia_no_deudor,
                    "CONSTANCIA DE ESTUDIOS": gen.generar_constancia_estudios,
                    "CONSTANCIA DE CONDUCTA": gen.generar_constancia_conducta,
                    "CARTA COMPROMISO": gen.generar_carta_compromiso,
                    "RESOLUCIÓN DE TRASLADO": gen.generar_resolucion_traslado,
                }
                pdf = metodos[tipo_doc](datos)
                st.success("✅ Documento generado")
                st.download_button("⬇️ DESCARGAR PDF", pdf,
                                   f"{nombre.replace(' ', '_')}_{tipo_doc}.pdf",
                                   "application/pdf", use_container_width=True,
                                   key="dl_doc")
            else:
                st.error("⚠️ Complete nombre y DNI")


# ================================================================
# TAB: CARNETS
# ================================================================

def tab_carnets(config):
    st.header("🪪 Centro de Carnetización")
    tab_ind, tab_mat, tab_lote = st.tabs([
        "⚡ Individual", "📋 Desde Matrícula", "📦 Lote"
    ])

    with tab_ind:
        col1, col2 = st.columns(2)
        with col1:
            c_nombre = st.text_input("👤 Nombre completo:", key="c_nombre")
            c_dni = st.text_input("🆔 DNI:", key="c_dni")
            c_grado = st.selectbox("📚 Grado:", TODOS_LOS_GRADOS, key="c_grado")
            c_seccion = st.selectbox("📂 Sección:", SECCIONES, key="c_seccion")
        with col2:
            c_foto = st.file_uploader("📸 Foto del estudiante:",
                                       type=['jpg', 'png', 'jpeg'], key="c_foto")
            if c_foto:
                st.image(c_foto, width=180)

        if st.button("🪪 GENERAR CARNET", type="primary",
                     use_container_width=True, key="btn_gen_carnet"):
            if c_nombre and c_dni:
                foto_io = io.BytesIO(c_foto.getvalue()) if c_foto else None
                gen = GeneradorCarnet(
                    {'alumno': c_nombre, 'dni': c_dni,
                     'grado': c_grado, 'seccion': c_seccion},
                    config['anio'], foto_io
                )
                carnet = gen.generar()
                st.image(carnet, use_container_width=True)
                st.download_button("⬇️ DESCARGAR CARNET", carnet,
                                   f"Carnet_{c_nombre.replace(' ', '_')}.png",
                                   "image/png", use_container_width=True,
                                   key="dl_carnet")
            else:
                st.error("⚠️ Complete nombre y DNI")

    with tab_mat:
        dni_buscar = st.text_input("🔍 DNI del matriculado:", key="c_buscar_dni")
        if st.button("🔎 Buscar", key="btn_buscar_carnet"):
            alumno = BaseDatos.buscar_por_dni(dni_buscar)
            if alumno:
                st.session_state['carnet_encontrado'] = alumno
                st.success(f"✅ {alumno.get('Nombre', '')}")
            else:
                st.error("❌ No encontrado en matrícula")

        if st.session_state.get('carnet_encontrado'):
            al = st.session_state['carnet_encontrado']
            st.markdown(
                f"**{al.get('Nombre', '')}** | DNI: {al.get('DNI', '')} | "
                f"{al.get('Grado', '')} {al.get('Seccion', '')}"
            )
            foto_mat = st.file_uploader("📸 Foto:", type=['jpg', 'png', 'jpeg'],
                                         key="c_foto_mat")
            if st.button("🪪 GENERAR", type="primary",
                         use_container_width=True, key="btn_gen_carnet_mat"):
                foto_io = io.BytesIO(foto_mat.getvalue()) if foto_mat else None
                gen = GeneradorCarnet(al, config['anio'], foto_io)
                carnet = gen.generar()
                st.image(carnet, use_container_width=True)
                st.download_button("⬇️ DESCARGAR", carnet,
                                   f"Carnet_{al.get('Nombre', '').replace(' ', '_')}.png",
                                   "image/png", use_container_width=True,
                                   key="dl_carnet_mat")

    with tab_lote:
        df = BaseDatos.cargar_matricula()
        if not df.empty:
            nivel_lote = st.selectbox("Nivel:", ["Todos"] + list(NIVELES_GRADOS.keys()),
                                       key="lote_nivel")
            df_lote = df.copy()
            if nivel_lote != "Todos" and 'Nivel' in df_lote.columns:
                df_lote = df_lote[df_lote['Nivel'] == nivel_lote]
            st.info(f"📊 Se generarán **{len(df_lote)}** carnets")

            if st.button("🚀 GENERAR ZIP DE CARNETS", type="primary",
                         use_container_width=True, key="btn_gen_lote"):
                if not df_lote.empty:
                    buf_zip = io.BytesIO()
                    progreso = st.progress(0)
                    with zipfile.ZipFile(buf_zip, "w", zipfile.ZIP_DEFLATED) as zf:
                        for i, (_, row) in enumerate(df_lote.iterrows()):
                            gen = GeneradorCarnet(row.to_dict(), config['anio'])
                            carnet_bytes = gen.generar()
                            nombre_archivo = f"Carnet_{row.get('Nombre', '').replace(' ', '_')}.png"
                            zf.writestr(nombre_archivo, carnet_bytes.getvalue())
                            progreso.progress((i + 1) / len(df_lote))
                    buf_zip.seek(0)
                    st.balloons()
                    st.download_button("⬇️ DESCARGAR ZIP", buf_zip,
                                       f"Carnets_{config['anio']}.zip",
                                       "application/zip", use_container_width=True,
                                       key="dl_lote")
        else:
            st.info("📝 Registra estudiantes primero.")


# ================================================================
# TAB: ASISTENCIAS (cámara solo bajo demanda + borrar día)
# ================================================================

def tab_asistencias():
    st.header("📋 Control de Asistencia")
    st.caption(f"🕒 Hora Perú: **{hora_peru().strftime('%H:%M:%S')}** | "
               f"📅 {hora_peru().strftime('%d/%m/%Y')}")

    # Toggle Entrada/Salida
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌅 ENTRADA", use_container_width=True,
                      type="primary" if st.session_state.tipo_asistencia == "Entrada" else "secondary",
                      key="btn_entrada"):
            st.session_state.tipo_asistencia = "Entrada"
            st.rerun()
    with col2:
        if st.button("🌙 SALIDA", use_container_width=True,
                      type="primary" if st.session_state.tipo_asistencia == "Salida" else "secondary",
                      key="btn_salida"):
            st.session_state.tipo_asistencia = "Salida"
            st.rerun()

    st.info(f"📌 **Modo: {st.session_state.tipo_asistencia}**")
    st.markdown("---")

    col_cam, col_man = st.columns(2)

    with col_cam:
        st.markdown("### 📸 Escanear QR / Código de Barras")
        activar = st.checkbox("📷 Activar cámara para escanear", key="chk_cam_asist",
                              value=st.session_state.get('activar_camara_asist', False))
        st.session_state.activar_camara_asist = activar

        if activar:
            if HAS_PYZBAR:
                st.success("✅ Escáner QR/Barcode listo")
            else:
                st.warning("⚠️ pyzbar no disponible. Use registro manual.")

            foto = st.camera_input("Apunta al QR del carnet:", key="cam_asist")
            if foto:
                dni_detectado = decodificar_qr_imagen(foto.getvalue())
                if dni_detectado:
                    _registrar_asistencia_ui(dni_detectado)
                else:
                    st.warning("⚠️ No se detectó QR. Intente de nuevo o use registro manual.")
        else:
            st.info("💡 Activa la cámara cuando necesites escanear un carnet.")

    with col_man:
        st.markdown("### ✏️ Registro Manual")
        dni_manual = st.text_input("Ingrese DNI:", key="dni_manual",
                                    placeholder="Escriba o pegue el DNI")
        if st.button("✅ REGISTRAR", type="primary",
                     use_container_width=True, key="btn_registrar_man"):
            if dni_manual:
                _registrar_asistencia_ui(dni_manual.strip())
            else:
                st.warning("⚠️ Ingrese un DNI")

    # Tabla del día
    st.markdown("---")
    st.subheader("📊 Registros de Hoy")
    asistencias_hoy = BaseDatos.obtener_asistencias_hoy()

    if asistencias_hoy:
        df_asist = pd.DataFrame([
            {
                'DNI': d,
                'Nombre': v['nombre'],
                'Entrada': v.get('entrada', '—'),
                'Salida': v.get('salida', '—')
            }
            for d, v in asistencias_hoy.items()
        ])
        st.dataframe(df_asist, use_container_width=True, hide_index=True)

        # WhatsApp por cada uno
        st.markdown("### 📱 Enviar por WhatsApp")
        for dni, datos_a in asistencias_hoy.items():
            alumno = BaseDatos.buscar_por_dni(dni)
            if alumno:
                celular = alumno.get('Celular_Apoderado', alumno.get('Celular', ''))
                if celular and celular.strip():
                    entrada = datos_a.get('entrada', '')
                    salida = datos_a.get('salida', '')
                    msg = (
                        f"🏫 I.E. ALTERNATIVO YACHAY\n"
                        f"👤 {datos_a['nombre']}\n"
                        f"✅ Entrada: {entrada or '—'}\n"
                        f"🏁 Salida: {salida or '—'}"
                    )
                    link = generar_link_whatsapp(celular, msg)
                    st.markdown(
                        f'<a href="{link}" target="_blank" class="wa-btn">'
                        f'📱 {datos_a["nombre"]} → WhatsApp ({celular})</a>',
                        unsafe_allow_html=True
                    )

        # Botón borrar asistencias del día
        st.markdown("---")
        if st.button("🗑️ BORRAR ASISTENCIAS DEL DÍA", type="secondary",
                     use_container_width=True, key="btn_borrar_asist"):
            BaseDatos.borrar_asistencias_hoy()
            st.success("✅ Asistencias del día eliminadas")
            st.rerun()
    else:
        st.info("📝 No hay registros hoy.")


def _registrar_asistencia_ui(dni):
    """Registra asistencia y muestra resultado + botón WhatsApp"""
    alumno = BaseDatos.buscar_por_dni(dni)
    if alumno:
        hora = hora_peru_str()
        tipo = st.session_state.tipo_asistencia.lower()
        nombre = alumno.get('Nombre', alumno.get('Alumno', ''))
        BaseDatos.guardar_asistencia(dni, nombre, tipo, hora)
        st.success(f"✅ **{nombre}** — {st.session_state.tipo_asistencia}: **{hora}**")
        st.balloons()

        celular = alumno.get('Celular_Apoderado', alumno.get('Celular', ''))
        if celular and celular.strip():
            msg = generar_mensaje_asistencia(nombre, tipo, hora)
            link = generar_link_whatsapp(celular, msg)
            st.markdown(
                f'<a href="{link}" target="_blank" class="wa-btn">'
                f'📱 ENVIAR WhatsApp a {celular}</a>',
                unsafe_allow_html=True
            )
        else:
            st.warning("⚠️ Sin celular registrado para este estudiante")
    else:
        st.error(f"❌ DNI {dni} no encontrado en el sistema")


# ================================================================
# TAB: SISTEMA DE CALIFICACIÓN YACHAY (DOCENTES)
# ================================================================

def tab_calificacion_yachay(config):
    st.header("📝 Sistema de Calificación YACHAY")
    st.caption("Estilo ZipGrade — Genera hojas, define claves por área, "
               "corrige y genera ranking")

    tab_gen, tab_corr, tab_rank = st.tabs([
        "📄 Generar Hoja", "✅ Calificar Examen", "🏆 Ranking y Resultados"
    ])

    # ---- GENERAR HOJA ----
    with tab_gen:
        st.subheader("📄 Generar Hoja de Respuestas Imprimible")
        st.markdown("""
        **¿Cómo funciona el Sistema de Calificación YACHAY?**
        1. **Genera** la hoja de respuestas e **imprímela**
        2. Los alumnos **rellenan** los círculos con lápiz
        3. **Toma foto** con la cámara o ingresa las respuestas manualmente
        4. El sistema **califica automáticamente** cada área sobre **20 puntos**
        5. Se genera un **ranking** con todos los resultados

        💡 **Tip:** Para mejor detección por cámara, usa buena iluminación
        y que la hoja esté completamente plana.
        """)

        col1, col2 = st.columns(2)
        with col1:
            num_preguntas = st.selectbox("N° de preguntas:",
                                          [10, 20, 30, 40, 50], index=1,
                                          key="num_preg_gen")
        with col2:
            titulo_hoja = st.text_input("Título/Área:",
                                         "EVALUACIÓN BIMESTRAL",
                                         key="titulo_hoja")

        if st.button("📄 GENERAR HOJA", type="primary",
                     use_container_width=True, key="btn_gen_hoja"):
            hoja = _generar_hoja_respuestas(num_preguntas, titulo_hoja)
            st.image(hoja, use_container_width=True)
            st.download_button("⬇️ DESCARGAR PNG", hoja,
                               f"Hoja_{titulo_hoja}_{num_preguntas}p.png",
                               "image/png", use_container_width=True,
                               key="dl_hoja")

    # ---- CALIFICAR EXAMEN ----
    with tab_corr:
        st.subheader("✅ Calificar Examen")

        st.markdown("**1️⃣ Configura las áreas y claves de respuesta:**")
        st.caption("Cada área se califica sobre 20 puntos automáticamente")

        if 'areas_examen' not in st.session_state:
            st.session_state.areas_examen = []

        col_a, col_n, col_b = st.columns([2, 1, 1])
        with col_a:
            nueva_area = st.text_input("Nombre del área:", key="nueva_area")
        with col_n:
            nueva_num = st.selectbox("N° preguntas:",
                                      [5, 10, 15, 20, 25, 30], index=1,
                                      key="nueva_num")
        with col_b:
            st.markdown("###")
            if st.button("➕ Agregar Área", key="btn_agregar_area"):
                if nueva_area:
                    st.session_state.areas_examen.append({
                        'nombre': nueva_area,
                        'num': nueva_num,
                        'claves': ''
                    })
                    st.rerun()

        total_preguntas = 0
        todas_claves = []
        info_areas = []

        for i, area in enumerate(st.session_state.areas_examen):
            with st.expander(f"📚 {area['nombre']} ({area['num']} preguntas → Nota sobre 20)",
                             expanded=True):
                claves = st.text_input(
                    f"Claves (ej: {'ABCDABCDAB'[:area['num']]}):",
                    value=area.get('claves', ''),
                    key=f"claves_{i}",
                    max_chars=area['num']
                )
                st.session_state.areas_examen[i]['claves'] = claves.upper()
                info_areas.append({
                    'nombre': area['nombre'],
                    'num': area['num'],
                    'claves': list(claves.upper())
                })
                todas_claves.extend(list(claves.upper()))
                total_preguntas += area['num']

                if len(st.session_state.areas_examen) > 1:
                    if st.button(f"🗑️ Quitar área", key=f"del_area_{i}"):
                        st.session_state.areas_examen.pop(i)
                        st.rerun()

        if info_areas:
            st.info(f"📊 Total: **{total_preguntas}** preguntas en "
                    f"**{len(info_areas)}** áreas")

        st.markdown("---")
        st.markdown("**2️⃣ Datos del alumno:**")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            dni_exam = st.text_input("DNI del alumno:", key="dni_exam")
        with col_d2:
            if dni_exam:
                alumno_exam = BaseDatos.buscar_por_dni(dni_exam)
                if alumno_exam:
                    st.success(f"👤 {alumno_exam.get('Nombre', '')}")
                else:
                    st.warning("DNI no encontrado en matrícula")

        st.markdown("---")
        st.markdown("**3️⃣ Respuestas del alumno:**")
        metodo = st.radio("Método de ingreso:",
                          ["✏️ Ingresar manualmente", "📸 Tomar foto con cámara"],
                          horizontal=True, key="metodo_resp")

        respuestas_alumno = []

        if metodo == "✏️ Ingresar manualmente":
            st.caption("Ingresa las respuestas marcadas por el alumno")
            for i, area in enumerate(info_areas):
                resp = st.text_input(
                    f"{area['nombre']} ({area['num']} respuestas):",
                    key=f"resp_man_{i}",
                    max_chars=area['num'],
                    placeholder="Ej: " + "ABCD" * (area['num'] // 4)
                )
                respuestas_alumno.extend(list(resp.upper()))
        else:
            activar_cam_exam = st.checkbox("📷 Activar cámara", key="chk_cam_exam")
            if activar_cam_exam:
                foto_exam = st.camera_input("📷 Foto de la hoja:", key="cam_exam")
                if foto_exam:
                    detectadas = _procesar_examen(foto_exam.getvalue(), total_preguntas)
                    if detectadas:
                        respuestas_alumno = detectadas
                        st.success(f"✅ Detectadas {len(detectadas)} respuestas")
                    else:
                        st.warning("⚠️ No se detectaron respuestas. Ingrese manualmente.")

        st.markdown("---")
        if st.button("📊 CALIFICAR EXAMEN", type="primary",
                     use_container_width=True, key="btn_calificar"):
            if todas_claves and respuestas_alumno:
                alumno_data = BaseDatos.buscar_por_dni(dni_exam) if dni_exam else None
                nombre_alumno = alumno_data.get('Nombre', '') if alumno_data else "Sin nombre"

                resultado = {
                    'fecha': hora_peru().strftime('%d/%m/%Y %H:%M'),
                    'dni': dni_exam,
                    'nombre': nombre_alumno,
                    'areas': [],
                    'promedio_general': 0
                }

                idx = 0
                suma_notas = 0
                msg_wa = (
                    f"📝 *RESULTADOS DE EVALUACIÓN*\n"
                    f"🏫 I.E. ALTERNATIVO YACHAY\n"
                    f"👤 {nombre_alumno}\n"
                    f"📅 {hora_peru().strftime('%d/%m/%Y')}\n\n"
                )

                for area in info_areas:
                    n = area['num']
                    claves_area = area['claves'][:n]
                    resp_area = respuestas_alumno[idx:idx + n]

                    correctas = sum(
                        1 for j in range(min(len(claves_area), len(resp_area)))
                        if j < len(claves_area) and j < len(resp_area)
                        and claves_area[j] == resp_area[j]
                    )
                    nota_20 = round((correctas / n) * 20, 1) if n > 0 else 0
                    letra = ("AD" if nota_20 >= 18 else
                             "A" if nota_20 >= 14 else
                             "B" if nota_20 >= 11 else "C")

                    detalle = []
                    for j in range(n):
                        clave_j = claves_area[j] if j < len(claves_area) else '?'
                        resp_j = resp_area[j] if j < len(resp_area) else '?'
                        ok = (j < len(claves_area) and j < len(resp_area)
                              and claves_area[j] == resp_area[j])
                        detalle.append({
                            'pregunta': idx + j + 1,
                            'clave': clave_j,
                            'respuesta': resp_j,
                            'correcto': ok
                        })

                    resultado['areas'].append({
                        'nombre': area['nombre'],
                        'correctas': correctas,
                        'total': n,
                        'nota': nota_20,
                        'letra': letra,
                        'detalle': detalle
                    })

                    suma_notas += nota_20
                    msg_wa += (f"📚 *{area['nombre']}:* {nota_20}/20 ({letra}) "
                               f"— {correctas}/{n} correctas\n")
                    idx += n

                promedio = round(suma_notas / len(info_areas), 1) if info_areas else 0
                resultado['promedio_general'] = promedio
                letra_prom = ("AD" if promedio >= 18 else
                              "A" if promedio >= 14 else
                              "B" if promedio >= 11 else "C")
                msg_wa += (f"\n📊 *PROMEDIO GENERAL: {promedio}/20 ({letra_prom})*\n"
                           f"\n✨ Sistema de Calificación YACHAY")

                # Guardar
                BaseDatos.guardar_resultados_examen(resultado)

                # Mostrar resultados
                st.markdown("### 📊 Resultados")
                cols_res = st.columns(len(info_areas) + 1)
                for i, area_r in enumerate(resultado['areas']):
                    with cols_res[i]:
                        st.metric(
                            f"📚 {area_r['nombre']}",
                            f"{area_r['nota']}/20",
                            f"{area_r['letra']} ({area_r['correctas']}/{area_r['total']})"
                        )
                with cols_res[-1]:
                    st.metric("📊 PROMEDIO", f"{promedio}/20", letra_prom)

                # Detalle por área
                for area_r in resultado['areas']:
                    with st.expander(f"📋 Detalle {area_r['nombre']}"):
                        df_detalle = pd.DataFrame([
                            {
                                '#': d['pregunta'],
                                'Correcta': d['clave'],
                                'Marcada': d['respuesta'],
                                'Estado': '✅' if d['correcto'] else '❌'
                            }
                            for d in area_r['detalle']
                        ])
                        st.dataframe(df_detalle, use_container_width=True,
                                     hide_index=True)

                # WhatsApp individual
                if alumno_data:
                    celular = alumno_data.get('Celular_Apoderado', '')
                    if celular and celular.strip():
                        link = generar_link_whatsapp(celular, msg_wa)
                        st.markdown(
                            f'<a href="{link}" target="_blank" class="wa-btn">'
                            f'📱 Enviar resultados por WhatsApp a {celular}</a>',
                            unsafe_allow_html=True
                        )

                st.balloons()
            else:
                st.error("⚠️ Configure las claves y las respuestas del alumno")

    # ---- RANKING ----
    with tab_rank:
        st.subheader("🏆 Ranking de Resultados")
        resultados = BaseDatos.cargar_resultados_examen()

        if resultados:
            # Tabla de ranking
            ranking_data = []
            for r in resultados:
                ranking_data.append({
                    'Fecha': r.get('fecha', ''),
                    'Nombre': r.get('nombre', ''),
                    'DNI': r.get('dni', ''),
                    'Promedio': r.get('promedio_general', 0),
                    'Áreas': ', '.join([
                        f"{a['nombre']}:{a['nota']}"
                        for a in r.get('areas', [])
                    ])
                })

            df_rank = pd.DataFrame(ranking_data)
            df_rank = df_rank.sort_values('Promedio', ascending=False).reset_index(drop=True)
            df_rank.insert(0, 'Puesto', range(1, len(df_rank) + 1))

            st.dataframe(df_rank, use_container_width=True, hide_index=True)

            # Podio top 3
            if len(df_rank) >= 1:
                st.markdown("### 🏆 Podio")
                cols_podio = st.columns(min(3, len(df_rank)))
                medallas = ["🥇", "🥈", "🥉"]
                estilos_podio = ["ranking-gold", "ranking-silver", "ranking-bronze"]
                for i in range(min(3, len(df_rank))):
                    with cols_podio[i]:
                        r = df_rank.iloc[i]
                        st.markdown(
                            f'<div class="{estilos_podio[i]}">'
                            f'{medallas[i]} {r["Nombre"]}<br>'
                            f'Promedio: {r["Promedio"]}/20</div>',
                            unsafe_allow_html=True
                        )

            # Descargar ranking PDF
            st.markdown("---")
            st.markdown("**📥 Descargar Ranking completo en PDF**")
            if st.button("📥 GENERAR RANKING PDF", type="primary",
                         use_container_width=True, key="btn_gen_ranking_pdf"):
                pdf_ranking = generar_ranking_pdf(resultados, config['anio'])
                st.download_button("⬇️ Descargar PDF", pdf_ranking,
                                   f"Ranking_{config['anio']}.pdf",
                                   "application/pdf", key="dl_ranking_pdf")

            # Enviar individual por WhatsApp
            st.markdown("---")
            st.markdown("### 📱 Enviar Resultados Individuales por WhatsApp")
            for _, row in df_rank.iterrows():
                alumno = BaseDatos.buscar_por_dni(row['DNI']) if row['DNI'] else None
                if alumno:
                    celular = alumno.get('Celular_Apoderado', '')
                    if celular and celular.strip():
                        r_orig = next(
                            (r for r in resultados if r.get('dni') == row['DNI']),
                            None
                        )
                        if r_orig:
                            msg = (
                                f"📝 *RESULTADOS - I.E. ALTERNATIVO YACHAY*\n"
                                f"👤 {row['Nombre']}\n"
                                f"🏆 Puesto: {row['Puesto']}° de {len(df_rank)}\n"
                            )
                            for a in r_orig.get('areas', []):
                                msg += f"📚 {a['nombre']}: {a['nota']}/20 ({a['letra']})\n"
                            msg += f"\n📊 *PROMEDIO: {row['Promedio']}/20*\n✨ Sistema YACHAY"
                            link = generar_link_whatsapp(celular, msg)
                            st.markdown(
                                f'<a href="{link}" target="_blank" class="wa-btn">'
                                f'📱 #{row["Puesto"]} {row["Nombre"]} — '
                                f'{row["Promedio"]}/20 → WhatsApp</a>',
                                unsafe_allow_html=True
                            )

            # Limpiar ranking
            st.markdown("---")
            if st.button("🗑️ Limpiar Ranking", key="btn_limpiar_ranking"):
                if Path(ARCHIVO_RESULTADOS).exists():
                    os.remove(ARCHIVO_RESULTADOS)
                st.success("✅ Ranking limpiado")
                st.rerun()
        else:
            st.info("📝 No hay resultados aún. Corrige exámenes para ver el ranking.")


# ================================================================
# TAB: BASE DE DATOS
# ================================================================

def tab_base_datos():
    st.header("📊 Base de Datos General")
    df = BaseDatos.cargar_matricula()

    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📚 Total", len(df))
        with col2:
            st.metric("🎓 Grados",
                       df['Grado'].nunique() if 'Grado' in df.columns else 0)
        with col3:
            st.metric("📋 Niveles",
                       df['Nivel'].nunique() if 'Nivel' in df.columns else 0)
        with col4:
            st.metric("📱 Con Celular",
                       df['Celular_Apoderado'].notna().sum()
                       if 'Celular_Apoderado' in df.columns else 0)

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            opciones_grado = ['Todos'] + (
                sorted(df['Grado'].dropna().unique().tolist())
                if 'Grado' in df.columns else []
            )
            filtro_grado = st.selectbox("Filtrar por grado:", opciones_grado,
                                         key="filtro_bd_grado")
        with col2:
            busqueda = st.text_input("🔍 Buscar:", key="busqueda_bd")

        df_filtrado = df.copy()
        if filtro_grado != 'Todos' and 'Grado' in df.columns:
            df_filtrado = df_filtrado[df_filtrado['Grado'] == filtro_grado]
        if busqueda:
            df_filtrado = df_filtrado[
                df_filtrado.apply(lambda r: busqueda.lower() in str(r).lower(), axis=1)
            ]
        if 'Nombre' in df_filtrado.columns:
            df_filtrado = df_filtrado.sort_values('Nombre')

        st.dataframe(df_filtrado, use_container_width=True, hide_index=True, height=500)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇️ Descargar CSV",
                               df_filtrado.to_csv(index=False).encode('utf-8'),
                               "datos.csv", "text/csv", key="dl_csv")
        with col2:
            buf_excel = io.BytesIO()
            df_filtrado.to_excel(buf_excel, index=False, engine='openpyxl')
            buf_excel.seek(0)
            st.download_button("⬇️ Descargar Excel", buf_excel, "datos.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               key="dl_xlsx")
    else:
        st.info("📝 Registra estudiantes en Matrícula.")


# ================================================================
# HOJA DE RESPUESTAS (IMAGEN)
# ================================================================

def _generar_hoja_respuestas(num_preguntas, titulo):
    """Genera imagen de hoja de respuestas estilo ZipGrade"""
    width, height = 2480, 3508
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    try:
        font_titulo = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70
        )
        font_sub = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 45
        )
        font_num = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40
        )
        font_letra = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35
        )
    except Exception:
        font_titulo = font_sub = font_num = font_letra = ImageFont.load_default()

    # Marcadores de alineación (4 esquinas)
    tamaño_marcador = 80
    posiciones_marcador = [
        (50, 50), (width - 130, 50),
        (50, height - 130), (width - 130, height - 130)
    ]
    for pos in posiciones_marcador:
        draw.rectangle([pos, (pos[0] + tamaño_marcador, pos[1] + tamaño_marcador)],
                       fill="black")

    # Encabezado
    draw.text((width // 2, 200), "I.E.P. ALTERNATIVO YACHAY",
              font=font_titulo, fill="black", anchor="mm")
    draw.text((width // 2, 280),
              f"HOJA DE RESPUESTAS - {titulo.upper()}",
              font=font_sub, fill="black", anchor="mm")
    draw.text((width // 2, 350),
              "SISTEMA DE CALIFICACIÓN YACHAY",
              font=font_sub, fill="gray", anchor="mm")

    # Campos de datos
    draw.text((200, 480),
              "Nombre: ________________________________________",
              font=font_sub, fill="black")
    draw.text((200, 560),
              "DNI: ________________  Grado: ________________",
              font=font_sub, fill="black")
    draw.text((200, 640),
              f"Fecha: ________________  Preguntas: {num_preguntas}",
              font=font_sub, fill="black")
    draw.text((200, 740),
              "Rellene completamente el círculo de la alternativa correcta.",
              font=font_letra, fill="gray")

    # Grilla de burbujas
    start_y = 900
    start_x = 300
    spacing_y = 100
    col_spacing = 700
    preguntas_por_columna = min(25, (height - start_y - 200) // spacing_y)

    for i in range(num_preguntas):
        col = i // preguntas_por_columna
        fila = i % preguntas_por_columna
        x_base = start_x + (col * col_spacing)
        y_base = start_y + (fila * spacing_y)

        # Número de pregunta
        draw.text((x_base - 100, y_base), f"{i + 1}.",
                  font=font_num, fill="black", anchor="rm")

        # 4 opciones (A, B, C, D)
        for j, letra in enumerate(['A', 'B', 'C', 'D']):
            cx = x_base + (j * 130)
            draw.ellipse(
                [(cx - 35, y_base - 35), (cx + 35, y_base + 35)],
                outline="black", width=4
            )
            draw.text((cx, y_base), letra,
                      font=font_letra, fill="black", anchor="mm")

    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output


# ================================================================
# PROCESAMIENTO DE EXAMEN (DETECCIÓN BURBUJAS)
# ================================================================

def _procesar_examen(img_bytes, num_preguntas):
    """Procesa imagen de hoja de examen para detectar respuestas"""
    if not HAS_CV2:
        return None
    try:
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255,
                                  cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        # Filtrar burbujas (relación aspecto ~1, tamaño moderado)
        burbujas = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            aspect_ratio = w / float(h) if h > 0 else 0
            area = cv2.contourArea(c)
            if 0.7 <= aspect_ratio <= 1.3 and 15 <= w <= 120 and 15 <= h <= 120 and area > 200:
                burbujas.append((c, x, y, w, h))

        if not burbujas:
            return None

        # Ordenar por Y (vertical)
        burbujas = sorted(burbujas, key=lambda b: b[2])

        # Agrupar en filas
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

        # Determinar respuesta más marcada por fila
        respuestas = []
        for fila in filas[:num_preguntas]:
            opciones = fila[:4]
            intensidades = []
            for (contour, x, y, w, h) in opciones:
                mask = np.zeros(gray.shape, dtype="uint8")
                cv2.drawContours(mask, [contour], -1, 255, -1)
                masked = cv2.bitwise_and(thresh, thresh, mask=mask)
                intensidades.append(cv2.countNonZero(masked))
            if intensidades:
                max_idx = intensidades.index(max(intensidades))
                respuestas.append(['A', 'B', 'C', 'D'][min(max_idx, 3)])
            else:
                respuestas.append('?')

        return respuestas if respuestas else None
    except Exception:
        return None


# ================================================================
# VISTA DOCENTE (registro auxiliar + asistencia + calificación)
# ================================================================

def vista_docente(config):
    """Vista completa para docentes con sus 3 tabs"""
    info = st.session_state.docente_info
    grado = info['grado']
    st.markdown(f"### 👨‍🏫 Docente: {info['label']}")

    tabs = st.tabs([
        "📝 Registro Auxiliar",
        "📋 Registro Asistencia",
        "📝 Calificación YACHAY"
    ])

    with tabs[0]:
        st.subheader("📝 Registro Auxiliar de Evaluación")
        st.caption("5 Competencias × 4 Capacidades cada una")
        seccion = st.selectbox("Sección:", ["Todas"] + SECCIONES, key="doc_seccion")
        bimestre = st.selectbox("Bimestre:", list(BIMESTRES.keys()), key="doc_bimestre")
        dg = BaseDatos.obtener_estudiantes_grado(grado, seccion)
        st.info(f"📊 {len(dg)} estudiantes (orden alfabético)")

        if not dg.empty:
            st.dataframe(
                dg[['Nombre', 'DNI', 'Grado', 'Seccion']],
                use_container_width=True, hide_index=True
            )

        if st.button("📥 Descargar Registro Auxiliar PDF", type="primary",
                     use_container_width=True, key="btn_doc_aux"):
            if not dg.empty:
                label_grado = grado if grado != "ALL_SECUNDARIA" else "Secundaria"
                sec_label = seccion if seccion != "Todas" else "Todas"
                pdf = generar_registro_auxiliar_pdf(
                    label_grado, sec_label, config['anio'], bimestre, dg
                )
                st.download_button("⬇️ PDF", pdf,
                                   f"RegAux_{label_grado}_{bimestre}.pdf",
                                   "application/pdf", key="dl_doc_aux")
            else:
                st.warning("No hay estudiantes en este grado")

    with tabs[1]:
        st.subheader("📋 Registro de Asistencia")
        seccion2 = st.selectbox("Sección:", ["Todas"] + SECCIONES, key="doc_seccion2")
        meses_opciones = list(MESES_ESCOLARES.items())
        meses_sel = st.multiselect(
            "Meses:",
            [f"{v} ({k})" for k, v in meses_opciones],
            default=[f"{v} ({k})" for k, v in meses_opciones[:1]],
            key="doc_meses_sel"
        )
        meses_nums = [int(m.split('(')[1].replace(')', '')) for m in meses_sel]
        dg2 = BaseDatos.obtener_estudiantes_grado(grado, seccion2)
        st.info(f"📊 {len(dg2)} estudiantes")

        if st.button("📥 Descargar Registro Asistencia PDF", type="primary",
                     use_container_width=True, key="btn_doc_asist"):
            if not dg2.empty and meses_nums:
                label_grado = grado if grado != "ALL_SECUNDARIA" else "Secundaria"
                sec_label = seccion2 if seccion2 != "Todas" else "Todas"
                pdf = generar_registro_asistencia_pdf(
                    label_grado, sec_label, config['anio'], dg2, meses_nums
                )
                st.download_button("⬇️ PDF", pdf,
                                   f"RegAsist_{label_grado}.pdf",
                                   "application/pdf", key="dl_doc_asist")
            else:
                st.warning("Sin datos o meses seleccionados")

    with tabs[2]:
        tab_calificacion_yachay(config)


# ================================================================
# FUNCIÓN PRINCIPAL
# ================================================================

def main():
    if st.session_state.rol is None:
        pantalla_login()
        st.stop()

    config = configurar_sidebar()

    if st.session_state.rol == "auxiliar":
        tab_asistencias()

    elif st.session_state.rol == "docente":
        vista_docente(config)

    elif st.session_state.rol in ["directivo", "admin"]:
        tabs = st.tabs([
            "📝 MATRÍCULA",
            "📄 DOCUMENTOS",
            "🪪 CARNETS",
            "📋 ASISTENCIAS",
            "📊 BASE DATOS",
            "📝 CALIFICACIÓN YACHAY"
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
            tab_calificacion_yachay(config)


if __name__ == "__main__":
    main()
