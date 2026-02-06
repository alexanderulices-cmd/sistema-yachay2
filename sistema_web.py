# ================================================================
# SISTEMA YACHAY PRO v3.0 — VERSIÓN DEFINITIVA COMPLETA
# ================================================================
# Módulos: Matrícula (Alumnos + Docentes), Documentos PDF,
#          Carnets (individual/lote PDF 8 por hoja),
#          Asistencia QR (Alumnos + Docentes),
#          Sistema de Calificación YACHAY (ZipGrade),
#          Registro Auxiliar (3 Cursos × 4 Competencias × Desempeños),
#          Registro Asistencia (sin sáb/dom, sin feriados)
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
# ZONA HORARIA PERÚ (UTC-5)
# ================================================================

PERU_TZ = timezone(timedelta(hours=-5))


def hora_peru():
    return datetime.now(PERU_TZ)


def hora_peru_str():
    return hora_peru().strftime('%H:%M:%S')


def fecha_peru_str():
    return hora_peru().strftime('%Y-%m-%d')


# ================================================================
# FERIADOS OFICIALES DE PERÚ
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
    """Retorna lista de días hábiles (L-V, sin feriados)"""
    dias = []
    _, ndays = calendar.monthrange(anio, mes)
    for d in range(1, ndays + 1):
        dt = date(anio, mes, d)
        es_laboral = dt.weekday() < 5
        es_feriado = (mes, d) in FERIADOS_PERU
        if es_laboral and not es_feriado:
            dias.append(d)
    return dias


def feriados_del_mes(mes):
    """Retorna lista de feriados de un mes específico"""
    resultado = []
    for (m, d), nombre in FERIADOS_PERU.items():
        if m == mes:
            resultado.append(f"{d} - {nombre}")
    return resultado


# ================================================================
# SISTEMA DE USUARIOS (Nombre + Contraseña — SEGURO)
# ================================================================

USUARIOS = {
    "administrador": {
        "password": "306020",
        "rol": "admin",
        "label": "⚙️ Administrador",
        "docente_info": None
    },
    "directora": {
        "password": "deyanira",
        "rol": "directivo",
        "label": "📋 Directiva",
        "docente_info": None
    },
    "auxiliar": {
        "password": "123456789",
        "rol": "auxiliar",
        "label": "👤 Auxiliar",
        "docente_info": None
    },
    "prof.inicial3": {
        "password": "docente3",
        "rol": "docente",
        "label": "Docente Inicial 3 años",
        "docente_info": {"label": "Inicial 3 años", "grado": "Inicial 3 años", "nivel": "INICIAL"}
    },
    "prof.inicial4": {
        "password": "docente4",
        "rol": "docente",
        "label": "Docente Inicial 4 años",
        "docente_info": {"label": "Inicial 4 años", "grado": "Inicial 4 años", "nivel": "INICIAL"}
    },
    "prof.inicial5": {
        "password": "docente5",
        "rol": "docente",
        "label": "Docente Inicial 5 años",
        "docente_info": {"label": "Inicial 5 años", "grado": "Inicial 5 años", "nivel": "INICIAL"}
    },
    "prof.primero": {
        "password": "primero2026",
        "rol": "docente",
        "label": "Docente 1° Primaria",
        "docente_info": {"label": "1° Primaria", "grado": "1° Primaria", "nivel": "PRIMARIA"}
    },
    "prof.segundo": {
        "password": "segundo2026",
        "rol": "docente",
        "label": "Docente 2° Primaria",
        "docente_info": {"label": "2° Primaria", "grado": "2° Primaria", "nivel": "PRIMARIA"}
    },
    "prof.tercero": {
        "password": "tercero2026",
        "rol": "docente",
        "label": "Docente 3° Primaria",
        "docente_info": {"label": "3° Primaria", "grado": "3° Primaria", "nivel": "PRIMARIA"}
    },
    "prof.cuarto": {
        "password": "cuarto2026",
        "rol": "docente",
        "label": "Docente 4° Primaria",
        "docente_info": {"label": "4° Primaria", "grado": "4° Primaria", "nivel": "PRIMARIA"}
    },
    "prof.quinto": {
        "password": "quinto2026",
        "rol": "docente",
        "label": "Docente 5° Primaria",
        "docente_info": {"label": "5° Primaria", "grado": "5° Primaria", "nivel": "PRIMARIA"}
    },
    "prof.sexto": {
        "password": "sexto2026",
        "rol": "docente",
        "label": "Docente 6° Primaria",
        "docente_info": {"label": "6° Primaria", "grado": "6° Primaria", "nivel": "PRIMARIA"}
    },
    "coordinador": {
        "password": "coord2026",
        "rol": "docente",
        "label": "Coordinador Secundaria",
        "docente_info": {"label": "Coordinador Secundaria", "grado": "ALL_SECUNDARIA", "nivel": "SECUNDARIA"}
    },
}


# ================================================================
# CONSTANTES EDUCATIVAS
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
    "PREUNIVERSITARIO": [
        "Ciclo Regular", "Ciclo Intensivo",
        "Ciclo Verano", "Reforzamiento Primaria"
    ]
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
ARCHIVO_DOCENTES = "docentes.xlsx"
ARCHIVO_ASISTENCIAS = "asistencias.json"
ARCHIVO_RESULTADOS = "resultados_examenes.json"


# ================================================================
# SESSION STATE
# ================================================================

def init_session_state():
    defaults = {
        'rol': None,
        'docente_info': None,
        'usuario_actual': '',
        'alumno': '',
        'dni': '',
        'grado': '',
        'apoderado': '',
        'dni_apo': '',
        'tipo_asistencia': 'Entrada',
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
    color: white !important;
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
.wa-btn:hover { background: #1da851; }
.ranking-gold {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: #000; padding: 12px 15px; border-radius: 8px;
    font-weight: bold; text-align: center; margin: 5px 0;
}
.ranking-silver {
    background: linear-gradient(135deg, #C0C0C0, #A0A0A0);
    color: #000; padding: 12px 15px; border-radius: 8px;
    font-weight: bold; text-align: center; margin: 5px 0;
}
.ranking-bronze {
    background: linear-gradient(135deg, #CD7F32, #B8860B);
    color: #fff; padding: 12px 15px; border-radius: 8px;
    font-weight: bold; text-align: center; margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)


# ================================================================
# IMPORTACIONES OPCIONALES
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
    def obtener_fuente(nombre, tamanio, bold=False):
        try:
            if bold:
                ruta = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            else:
                ruta = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            if Path(ruta).exists():
                return ImageFont.truetype(ruta, int(tamanio))
            return ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()


# ================================================================
# BASE DE DATOS — ALUMNOS Y DOCENTES
# ================================================================

class BaseDatos:

    # ---- MATRÍCULA ALUMNOS ----

    @staticmethod
    def cargar_matricula():
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
        df.to_excel(ARCHIVO_MATRICULA, index=False, engine='openpyxl')

    @staticmethod
    def registrar_estudiante(datos):
        df = BaseDatos.cargar_matricula()
        if not df.empty and 'DNI' in df.columns and datos['DNI'] in df['DNI'].values:
            idx = df[df['DNI'] == datos['DNI']].index[0]
            for key, value in datos.items():
                df.at[idx, key] = value
        else:
            df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)
        BaseDatos.guardar_matricula(df)
        return True

    @staticmethod
    def buscar_por_dni(dni):
        """Busca en matrícula alumnos, luego en docentes, luego en BD legacy"""
        dni_str = str(dni).strip()
        # Buscar en alumnos
        df = BaseDatos.cargar_matricula()
        if df is not None and not df.empty and 'DNI' in df.columns:
            df['DNI'] = df['DNI'].astype(str).str.strip()
            resultado = df[df['DNI'] == dni_str]
            if not resultado.empty:
                r = resultado.iloc[0].to_dict()
                r['_tipo'] = 'alumno'
                return r
        # Buscar en docentes
        df_doc = BaseDatos.cargar_docentes()
        if not df_doc.empty and 'DNI' in df_doc.columns:
            df_doc['DNI'] = df_doc['DNI'].astype(str).str.strip()
            res_doc = df_doc[df_doc['DNI'] == dni_str]
            if not res_doc.empty:
                r = res_doc.iloc[0].to_dict()
                r['_tipo'] = 'docente'
                return r
        # Buscar en BD legacy
        try:
            if Path(ARCHIVO_BD).exists():
                df2 = pd.read_excel(ARCHIVO_BD, dtype=str, engine='openpyxl')
                df2.columns = df2.columns.str.strip().str.title()
                if 'Dni' in df2.columns:
                    df2['Dni'] = df2['Dni'].astype(str).str.strip()
                    res2 = df2[df2['Dni'] == dni_str]
                    if not res2.empty:
                        row = res2.iloc[0].to_dict()
                        return {
                            'Nombre': row.get('Alumno', row.get('Nombre', '')),
                            'DNI': row.get('Dni', ''),
                            'Grado': row.get('Grado', ''),
                            'Nivel': row.get('Nivel', ''),
                            'Seccion': row.get('Seccion', ''),
                            'Apoderado': row.get('Apoderado', ''),
                            'DNI_Apoderado': row.get('Dni_Apoderado', ''),
                            'Celular_Apoderado': row.get('Celular', ''),
                            '_tipo': 'alumno'
                        }
        except Exception:
            pass
        return None

    @staticmethod
    def eliminar_estudiante(dni):
        df = BaseDatos.cargar_matricula()
        df['DNI'] = df['DNI'].astype(str).str.strip()
        df = df[df['DNI'] != str(dni).strip()]
        BaseDatos.guardar_matricula(df)

    @staticmethod
    def obtener_estudiantes_grado(grado, seccion=None):
        """Retorna DF de estudiantes de un grado, orden ALFABÉTICO"""
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

    # ---- DOCENTES ----

    @staticmethod
    def cargar_docentes():
        try:
            if Path(ARCHIVO_DOCENTES).exists():
                df = pd.read_excel(ARCHIVO_DOCENTES, dtype=str, engine='openpyxl')
                df.columns = df.columns.str.strip()
                return df
        except Exception:
            pass
        return pd.DataFrame(columns=[
            'Nombre', 'DNI', 'Cargo', 'Especialidad', 'Celular', 'Grado_Asignado'
        ])

    @staticmethod
    def guardar_docentes(df):
        df.to_excel(ARCHIVO_DOCENTES, index=False, engine='openpyxl')

    @staticmethod
    def registrar_docente(datos):
        df = BaseDatos.cargar_docentes()
        if not df.empty and 'DNI' in df.columns and datos['DNI'] in df['DNI'].values:
            idx = df[df['DNI'] == datos['DNI']].index[0]
            for key, value in datos.items():
                df.at[idx, key] = value
        else:
            df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)
        BaseDatos.guardar_docentes(df)

    @staticmethod
    def eliminar_docente(dni):
        df = BaseDatos.cargar_docentes()
        df['DNI'] = df['DNI'].astype(str).str.strip()
        df = df[df['DNI'] != str(dni).strip()]
        BaseDatos.guardar_docentes(df)

    # ---- ASISTENCIA (alumnos + docentes) ----

    @staticmethod
    def guardar_asistencia(dni, nombre, tipo, hora, es_docente=False):
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
                'salida': '',
                'es_docente': es_docente
            }
        asistencias[fecha_hoy][dni][tipo] = hora
        asistencias[fecha_hoy][dni]['nombre'] = nombre
        with open(ARCHIVO_ASISTENCIAS, 'w', encoding='utf-8') as f:
            json.dump(asistencias, f, indent=2, ensure_ascii=False)

    @staticmethod
    def obtener_asistencias_hoy():
        fecha_hoy = fecha_peru_str()
        if Path(ARCHIVO_ASISTENCIAS).exists():
            with open(ARCHIVO_ASISTENCIAS, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get(fecha_hoy, {})
        return {}

    @staticmethod
    def borrar_asistencias_hoy():
        fecha_hoy = fecha_peru_str()
        if Path(ARCHIVO_ASISTENCIAS).exists():
            with open(ARCHIVO_ASISTENCIAS, 'r', encoding='utf-8') as f:
                asistencias = json.load(f)
            if fecha_hoy in asistencias:
                del asistencias[fecha_hoy]
            with open(ARCHIVO_ASISTENCIAS, 'w', encoding='utf-8') as f:
                json.dump(asistencias, f, indent=2, ensure_ascii=False)

    # ---- ESTADÍSTICAS ----

    @staticmethod
    def obtener_estadisticas():
        df = BaseDatos.cargar_matricula()
        df_doc = BaseDatos.cargar_docentes()
        total_alumnos = len(df) if df is not None and not df.empty else 0
        total_docentes = len(df_doc) if df_doc is not None and not df_doc.empty else 0
        return {
            'total_alumnos': total_alumnos,
            'total_docentes': total_docentes,
            'grados': df['Grado'].nunique() if not df.empty and 'Grado' in df.columns else 0
        }

    # ---- RESULTADOS EXÁMENES ----

    @staticmethod
    def guardar_resultados_examen(resultado):
        datos = []
        if Path(ARCHIVO_RESULTADOS).exists():
            with open(ARCHIVO_RESULTADOS, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        datos.append(resultado)
        with open(ARCHIVO_RESULTADOS, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    @staticmethod
    def cargar_resultados_examen():
        if Path(ARCHIVO_RESULTADOS).exists():
            with open(ARCHIVO_RESULTADOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []


# ================================================================
# GENERADOR PDF — DOCUMENTOS OFICIALES (6 tipos)
# ================================================================

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
                self.canvas.drawImage("fondo.png", 0, 0,
                                       width=self.width, height=self.height)
            except Exception:
                pass

    def _marca_agua_escudo(self):
        if Path("escudo_upload.png").exists():
            try:
                self.canvas.saveState()
                self.canvas.setFillAlpha(0.06)
                self.canvas.drawImage("escudo_upload.png",
                                       self.width / 2 - 120, self.height / 2 - 120,
                                       width=240, height=240, mask='auto')
                self.canvas.restoreState()
            except Exception:
                pass

    def _dibujar_encabezado(self, titulo):
        self.canvas.setFont("Helvetica-Oblique", 11)
        self.canvas.drawCentredString(
            self.width / 2, self.config['y_frase'],
            f'"{self.config["frase"]}"'
        )
        hoy = hora_peru()
        self.canvas.setFont("Helvetica", 11)
        self.canvas.drawRightString(
            self.width - 60, self.config['y_frase'] - 25,
            f"Chinchero, {hoy.day} de {MESES_ESP[hoy.month - 1]} de {self.config['anio']}"
        )
        self.canvas.setFont("Helvetica-Bold", 16)
        self.canvas.drawCentredString(self.width / 2, self.config['y_titulo'], titulo)
        self.canvas.line(100, self.config['y_titulo'] - 5,
                         self.width - 100, self.config['y_titulo'] - 5)

    def _parrafo(self, texto, x, y, ancho, estilo):
        p = Paragraph(texto, estilo)
        w, h = p.wrap(ancho, 600)
        p.drawOn(self.canvas, x, y - h)
        return y - h - 15

    def _agregar_qr(self, datos, tipo_doc):
        data_qr = (f"YACHAY|{tipo_doc}|"
                    f"{datos.get('alumno', datos.get('Nombre', ''))}|"
                    f"{datos.get('dni', datos.get('DNI', ''))}|"
                    f"{hora_peru().strftime('%d/%m/%Y')}")
        qr = qrcode.QRCode(box_size=10, border=1)
        qr.add_data(data_qr)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        temp = "temp_qr.png"
        img_qr.save(temp)
        self.canvas.drawImage(temp, self.config['qr_x'], self.config['qr_y'],
                               width=70, height=70)
        self.canvas.setFont("Helvetica", 6)
        self.canvas.drawCentredString(self.config['qr_x'] + 35,
                                       self.config['qr_y'] - 5,
                                       "VERIFICACIÓN")
        try:
            os.remove(temp)
        except Exception:
            pass

    def _solicitante(self, datos, y):
        apoderado = datos.get('apoderado', datos.get('Apoderado', '')).upper()
        dni_apo = datos.get('dni_apo', datos.get('DNI_Apoderado', ''))
        est = ParagraphStyle('S', parent=self.styles['Normal'],
                              fontSize=10, leading=14, alignment=TA_JUSTIFY)
        return self._parrafo(
            f"Se expide a solicitud del Sr(a). <b>{apoderado}</b> "
            f"con DNI N° <b>{dni_apo}</b>.", 60, y, self.width - 120, est
        )

    def _firmas(self):
        yf = 110
        self.canvas.line(200, yf, 395, yf)
        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawCentredString(self.width / 2, yf - 15,
                                       self.config['directora'].upper())
        self.canvas.setFont("Helvetica", 9)
        self.canvas.drawCentredString(self.width / 2, yf - 28, "DIRECTORA")

    def _fin(self):
        self.canvas.save()
        self.buffer.seek(0)
        return self.buffer

    # ---- 1. CONSTANCIA DE VACANTE ----
    def generar_constancia_vacante(self, d):
        self._aplicar_fondo()
        self._marca_agua_escudo()
        self._dibujar_encabezado("CONSTANCIA DE VACANTE")
        y = self.config['y_titulo'] - 50
        mx, an = 60, self.width - 120
        e = ParagraphStyle('N', parent=self.styles['Normal'],
                            fontSize=11, leading=15, alignment=TA_JUSTIFY)
        el = ParagraphStyle('L', parent=e, leftIndent=25)
        y = self._parrafo(
            "La Dirección de la I.E.P. ALTERNATIVO YACHAY de Chinchero, "
            "debidamente representada por su Directora, certifica:", mx, y, an, e
        )
        al = d.get('alumno', d.get('Nombre', '')).upper()
        dni = d.get('dni', d.get('DNI', ''))
        gr = d.get('grado', d.get('Grado', '')).upper()
        y = self._parrafo(
            f"Que la I.E. cuenta con <b>VACANTE DISPONIBLE</b> en <b>{gr}</b> "
            f"para el/la estudiante <b>{al}</b>, DNI N° <b>{dni}</b>, "
            f"año escolar <b>{self.config['anio']}</b>.", mx, y, an, e
        )
        y = self._parrafo("Para formalizar la matrícula, presentar:", mx, y, an, e)
        for r in [
            "• Certificado Oficial de Estudios del SIAGIE (original).",
            "• Resolución Directoral de Traslado de Matrícula.",
            "• Libreta de Notas del Sistema SIAGIE.",
            "• Ficha Única de Matrícula del Sistema SIAGIE.",
            "• Copia del DNI del estudiante.",
            "• Constancia de No Adeudo de la IE de procedencia.",
            "• Folder o mica transparente."
        ]:
            y = self._parrafo(r, mx, y, an, el)
        y = self._solicitante(d, y)
        self._firmas()
        self._agregar_qr(d, "VACANTE")
        return self._fin()

    # ---- 2. CONSTANCIA DE NO ADEUDO ----
    def generar_constancia_no_deudor(self, d):
        self._aplicar_fondo()
        self._marca_agua_escudo()
        self._dibujar_encabezado("CONSTANCIA DE NO ADEUDO")
        y = self.config['y_titulo'] - 50
        mx, an = 60, self.width - 120
        e = ParagraphStyle('N', parent=self.styles['Normal'],
                            fontSize=11, leading=15, alignment=TA_JUSTIFY)
        y = self._parrafo(
            "La Dirección de la I.E.P. ALTERNATIVO YACHAY:", mx, y, an, e
        )
        al = d.get('alumno', d.get('Nombre', '')).upper()
        dni = d.get('dni', d.get('DNI', ''))
        y = self._parrafo(
            f"Que el/la estudiante <b>{al}</b>, DNI N° <b>{dni}</b>, "
            f"ha cumplido satisfactoriamente con todas sus obligaciones "
            f"económicas, no registrando deuda alguna.", mx, y, an, e
        )
        y = self._solicitante(d, y)
        self._firmas()
        self._agregar_qr(d, "NO ADEUDO")
        return self._fin()

    # ---- 3. CONSTANCIA DE ESTUDIOS ----
    def generar_constancia_estudios(self, d):
        self._aplicar_fondo()
        self._marca_agua_escudo()
        self._dibujar_encabezado("CONSTANCIA DE ESTUDIOS")
        y = self.config['y_titulo'] - 50
        mx, an = 60, self.width - 120
        e = ParagraphStyle('N', parent=self.styles['Normal'],
                            fontSize=11, leading=15, alignment=TA_JUSTIFY)
        al = d.get('alumno', d.get('Nombre', '')).upper()
        dni = d.get('dni', d.get('DNI', ''))
        gr = d.get('grado', d.get('Grado', '')).upper()
        y = self._parrafo(
            "La Dirección de la I.E.P. ALTERNATIVO YACHAY:", mx, y, an, e
        )
        y = self._parrafo(
            f"Que <b>{al}</b>, DNI N° <b>{dni}</b>, se encuentra "
            f"<b>MATRICULADO(A)</b> año <b>{self.config['anio']}</b>, "
            f"cursando <b>{gr}</b>, conforme consta en los registros "
            f"oficiales del plantel y el Sistema SIAGIE.", mx, y, an, e
        )
        y = self._solicitante(d, y)
        self._firmas()
        self._agregar_qr(d, "ESTUDIOS")
        return self._fin()

    # ---- 4. CONSTANCIA DE CONDUCTA ----
    def generar_constancia_conducta(self, d):
        self._aplicar_fondo()
        self._marca_agua_escudo()
        self._dibujar_encabezado("CONSTANCIA DE CONDUCTA")
        y = self.config['y_titulo'] - 50
        mx, an = 60, self.width - 120
        e = ParagraphStyle('N', parent=self.styles['Normal'],
                            fontSize=10, leading=14, alignment=TA_JUSTIFY)
        al = d.get('alumno', d.get('Nombre', '')).upper()
        dni = d.get('dni', d.get('DNI', ''))
        y = self._parrafo(
            f"Que <b>{al}</b>, DNI N° <b>{dni}</b>, obtuvo en "
            f"<b>CONDUCTA</b>:", mx, y, an, e
        )
        y -= 15
        tx = self.width / 2 - 200
        self.canvas.setFont("Helvetica-Bold", 10)
        self.canvas.drawString(tx, y, "GRADO")
        self.canvas.drawString(tx + 120, y, "AÑO")
        self.canvas.drawString(tx + 280, y, "CALIFICACIÓN")
        y -= 5
        self.canvas.line(tx - 10, y, tx + 380, y)
        y -= 20
        self.canvas.setFont("Helvetica", 9)
        ab = int(self.config['anio']) - 5
        for i, g in enumerate(["PRIMERO", "SEGUNDO", "TERCERO", "CUARTO", "QUINTO"]):
            n = d.get(f'nota_conducta_{i+1}', 'AD')
            self.canvas.drawString(tx, y, g)
            self.canvas.drawString(tx + 120, y, str(ab + i + 1))
            self.canvas.drawString(tx + 280, y, n)
            y -= 18
        y -= 10
        y = self._solicitante(d, y)
        self._firmas()
        self._agregar_qr(d, "CONDUCTA")
        return self._fin()

    # ---- 5. CARTA DE COMPROMISO ----
    def generar_carta_compromiso(self, d):
        self._aplicar_fondo()
        self._marca_agua_escudo()
        self._dibujar_encabezado("CARTA DE COMPROMISO")
        y = self.config['y_titulo'] - 40
        mx, an = 50, self.width - 100
        e = ParagraphStyle('C', parent=self.styles['Normal'],
                            fontSize=8.5, leading=11, alignment=TA_JUSTIFY)
        ei = ParagraphStyle('I', parent=e, leftIndent=10)
        apo = d.get('apoderado', d.get('Apoderado', '')).upper()
        dapo = d.get('dni_apo', d.get('DNI_Apoderado', ''))
        al = d.get('alumno', d.get('Nombre', '')).upper()
        gr = d.get('grado', d.get('Grado', '')).upper()
        y = self._parrafo(
            f"Yo, <b>{apo}</b>, DNI N° <b>{dapo}</b>, apoderado de "
            f"<b>{al}</b>, del <b>{gr}</b>, me comprometo a:", mx, y, an, e
        )
        compromisos = [
            "1. Velar por la asistencia puntual de mi hijo(a).",
            "2. Supervisar el cumplimiento de tareas.",
            "3. Asegurar asistencia uniformado(a).",
            "4. Inculcar respeto hacia docentes y compañeros.",
            "5. Participar en actividades del comité de aula.",
            "6. Ejercer crianza positiva, libre de violencia.",
            "7. Atender problemas de conducta oportunamente.",
            "8. Asumir responsabilidad por daños materiales.",
            "9. Vigilar vocabulario apropiado.",
            "10. Acudir cuando sea requerido(a).",
            "11. Asistir puntualmente a reuniones.",
            "12. Justificar inasistencias en 24 horas.",
            "13. Cumplir pagos de pensiones.",
            "14. Respetar la autonomía pedagógica."
        ]
        for c in compromisos:
            y = self._parrafo(c, mx, y, an, ei)
            y += 2
        y = 120
        self.canvas.line(80, y, 200, y)
        self.canvas.line(220, y, 340, y)
        self.canvas.line(360, y, 480, y)
        y -= 10
        self.canvas.setFont("Helvetica-Bold", 7)
        self.canvas.drawCentredString(140, y, "FIRMA APODERADO")
        self.canvas.drawCentredString(280, y, self.config['directora'].upper())
        self.canvas.drawCentredString(280, y - 10, "DIRECTORA")
        self.canvas.drawCentredString(420, y, self.config['promotor'].upper())
        self.canvas.drawCentredString(420, y - 10, "PROMOTOR")
        return self._fin()

    # ---- 6. RESOLUCIÓN DE TRASLADO ----
    def generar_resolucion_traslado(self, d):
        self._aplicar_fondo()
        self._marca_agua_escudo()
        self.canvas.setFont("Helvetica-Oblique", 11)
        self.canvas.drawCentredString(self.width / 2, 700,
                                       f'"{self.config["frase"]}"')
        self.canvas.setFont("Helvetica-Bold", 14)
        self.canvas.drawCentredString(
            self.width / 2, 670,
            f"RESOLUCIÓN DIRECTORAL N° {d.get('num_resolucion', '')}"
        )
        self.canvas.setFont("Helvetica", 11)
        self.canvas.drawCentredString(self.width / 2, 640,
                                       d.get('fecha_resolucion', ''))
        mx, an = 60, self.width - 120
        e = ParagraphStyle('N', parent=self.styles['Normal'],
                            fontSize=11, leading=15, alignment=TA_JUSTIFY)
        al = d.get('alumno', d.get('Nombre', '')).upper()
        niv = d.get('nivel', '').upper()
        y = 600
        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawString(mx, y, "SE RESUELVE:")
        y -= 20
        tabla_data = [
            ['ALUMNO', al],
            ['NIVEL', niv],
            ['IE PROCEDENCIA', 'IEP ALTERNATIVO YACHAY'],
            ['IE DESTINO', d.get('ie_destino', '').upper()]
        ]
        tabla = Table(tabla_data, colWidths=[200, 280])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        tabla.wrapOn(self.canvas, an, 200)
        tabla.drawOn(self.canvas, mx, y - 80)
        self._firmas()
        self._agregar_qr(d, "TRASLADO")
        return self._fin()


# ================================================================
# REGISTRO AUXILIAR PDF — 3 Cursos × 4 Competencias × Desempeños
# ================================================================

def generar_registro_auxiliar_pdf(grado, seccion, anio, bimestre,
                                  estudiantes_df, cursos=None):
    """
    Genera registro auxiliar MINEDU:
    - Hasta 3 cursos por hoja
    - Cada curso: 4 competencias
    - Cada competencia: 3 desempeños (D1, D2, D3)
    - Orden alfabético
    - Marca de agua escudo
    """
    if cursos is None:
        cursos = ["Matemática", "Comunicación", "Ciencia y Tec."]

    num_cursos = len(cursos)
    desempenios_por_comp = 3
    comps_por_curso = 4
    total_cols_data = num_cursos * comps_por_curso * desempenios_por_comp

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
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(w / 2, h - 22,
                        "I.E.P. ALTERNATIVO YACHAY - REGISTRO AUXILIAR DE EVALUACIÓN")
    c.setFont("Helvetica", 8)
    c.drawCentredString(w / 2, h - 35,
                        f"Grado: {grado} | Sección: {seccion} | "
                        f"{bimestre} | Año: {anio}")
    c.setFont("Helvetica-Oblique", 7)
    c.drawCentredString(w / 2, h - 47,
                        '"Educar para la Vida — Pioneros en la Educación de Calidad"')

    # === CONSTRUIR ENCABEZADO DE 3 FILAS ===
    # Fila 0: N° | NOMBRE | CURSO1 (span) | CURSO2 (span) | CURSO3 (span)
    # Fila 1: | | C1(span) C2(span) C3(span) C4(span) | ... (por curso)
    # Fila 2: | | D1 D2 D3 | D1 D2 D3 | ... (por competencia)

    cols_per_curso = comps_por_curso * desempenios_por_comp  # 4*3=12

    header_row0 = ["N°", "APELLIDOS Y NOMBRES"]
    for curso in cursos:
        header_row0.append(curso.upper())
        header_row0.extend([""] * (cols_per_curso - 1))

    header_row1 = ["", ""]
    for _ in range(num_cursos):
        for ci in range(1, comps_por_curso + 1):
            header_row1.append(f"C{ci}")
            header_row1.extend([""] * (desempenios_por_comp - 1))

    header_row2 = ["", ""]
    for _ in range(num_cursos):
        for _ in range(comps_por_curso):
            for di in range(1, desempenios_por_comp + 1):
                header_row2.append(f"D{di}")

    # Estudiantes
    if not estudiantes_df.empty:
        est = estudiantes_df.sort_values('Nombre').reset_index(drop=True)
    else:
        est = pd.DataFrame()

    data = [header_row0, header_row1, header_row2]
    num_est = len(est) if not est.empty else 25
    for idx in range(num_est):
        nombre = est.iloc[idx].get('Nombre', '') if idx < len(est) else ""
        if len(nombre) > 28:
            nombre = nombre[:28] + "."
        fila = [str(idx + 1), nombre] + [""] * total_cols_data
        data.append(fila)

    # Anchos
    available = w - 30
    w_num = 16
    w_name = 115
    w_data = (available - w_num - w_name) / total_cols_data
    w_data = max(16, min(25, w_data))
    col_widths = [w_num, w_name] + [w_data] * total_cols_data

    tabla = Table(data, colWidths=col_widths, repeatRows=3)

    style_list = [
        ('FONTNAME', (0, 0), (-1, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 2), 5),
        ('FONTSIZE', (0, 3), (-1, -1), 5.5),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 3), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (1, 2), colors.Color(0.1, 0.1, 0.35)),
        ('TEXTCOLOR', (0, 0), (1, 2), colors.white),
        ('ROWBACKGROUNDS', (0, 3), (-1, -1),
         [colors.white, colors.Color(0.95, 0.95, 1)]),
    ]

    # Spans y colores para cursos (fila 0)
    colores_cursos = [
        colors.Color(0, 0.2, 0.5),
        colors.Color(0.15, 0.35, 0.15),
        colors.Color(0.4, 0.15, 0.15)
    ]
    for ci, curso in enumerate(cursos):
        col_start = 2 + ci * cols_per_curso
        col_end = col_start + cols_per_curso - 1
        style_list.append(('SPAN', (col_start, 0), (col_end, 0)))
        bg = colores_cursos[ci % len(colores_cursos)]
        style_list.append(('BACKGROUND', (col_start, 0), (col_end, 0), bg))
        style_list.append(('TEXTCOLOR', (col_start, 0), (col_end, 0), colors.white))

        # Spans para competencias (fila 1)
        for comp_i in range(comps_por_curso):
            cs = col_start + comp_i * desempenios_por_comp
            ce = cs + desempenios_por_comp - 1
            style_list.append(('SPAN', (cs, 1), (ce, 1)))
            bg2 = colors.Color(bg.red + 0.1, bg.green + 0.1, bg.blue + 0.1)
            style_list.append(('BACKGROUND', (cs, 1), (ce, 1), bg2))
            style_list.append(('TEXTCOLOR', (cs, 1), (ce, 1), colors.white))
            # Desempeños fila 2
            style_list.append(('BACKGROUND', (cs, 2), (ce, 2), bg2))
            style_list.append(('TEXTCOLOR', (cs, 2), (ce, 2), colors.white))

    tabla.setStyle(TableStyle(style_list))
    tw, th_t = tabla.wrap(w - 20, h - 70)
    tabla.drawOn(c, 10, h - 58 - th_t)

    # Pie
    c.setFont("Helvetica", 5)
    c.drawString(10, 12,
                 f"C=Competencia | D=Desempeño | AD(18-20) A(14-17) "
                 f"B(11-13) C(0-10) | {bimestre} | Sistema YACHAY PRO — {anio}")

    c.save()
    buffer.seek(0)
    return buffer


# ================================================================
# REGISTRO ASISTENCIA PDF (sin sáb/dom, sin feriados, muestra cuáles)
# ================================================================

def generar_registro_asistencia_pdf(grado, seccion, anio, estudiantes_df,
                                     meses_sel):
    """
    Genera registro asistencia:
    - Solo días hábiles (L-V)
    - Excluye feriados de Perú
    - Al pie indica qué feriados se excluyeron
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    w, h = landscape(A4)

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

        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(w / 2, h - 22,
                            "I.E.P. ALTERNATIVO YACHAY - REGISTRO DE ASISTENCIA")
        c.setFont("Helvetica", 8)
        c.drawCentredString(w / 2, h - 35,
                            f"Grado: {grado} | Sección: {seccion} | "
                            f"Mes: {mes_nombre} | Año: {anio}")

        dias = dias_habiles_mes(int(anio), mes_num)
        ndias = len(dias)

        header = ["N°", "APELLIDOS Y NOMBRES"]
        for d in dias:
            dt = date(int(anio), mes_num, d)
            header.append(f"{d}\n{dias_semana[dt.weekday()]}")
        header.extend(["A", "T", "F", "J"])

        data = [header]
        num_est = len(est) if not est.empty else 25
        for idx in range(num_est):
            nombre = est.iloc[idx].get('Nombre', '') if idx < len(est) else ""
            if len(nombre) > 32:
                nombre = nombre[:32] + "."
            fila = [str(idx + 1), nombre] + [""] * ndias + ["", "", "", ""]
            data.append(fila)

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

        # Pie: Mostrar feriados del mes que se excluyeron
        feriados_mes = feriados_del_mes(mes_num)
        c.setFont("Helvetica", 5)
        pie_texto = (f"A=Asistió | T=Tardanza | F=Falta | J=Justificada | "
                     f"Sin sábados, domingos ni feriados")
        if feriados_mes:
            pie_texto += f" | FERIADOS EXCLUIDOS: {', '.join(feriados_mes)}"
        c.drawString(10, 8, pie_texto)

    c.save()
    buffer.seek(0)
    return buffer


# ================================================================
# RANKING PDF COMPLETO
# ================================================================

def generar_ranking_pdf(resultados, anio):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    if Path("escudo_upload.png").exists():
        try:
            c.saveState()
            c.setFillAlpha(0.06)
            c.drawImage("escudo_upload.png", w / 2 - 100, h / 2 - 100,
                        200, 200, mask='auto')
            c.restoreState()
        except Exception:
            pass

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w / 2, h - 40, "I.E.P. ALTERNATIVO YACHAY")
    c.setFont("Helvetica", 11)
    c.drawCentredString(w / 2, h - 58,
                        '"Pioneros en la Educación de Calidad"')
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w / 2, h - 85,
                        f"RANKING DE RESULTADOS — {anio}")
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, h - 100,
                        f"Generado: {hora_peru().strftime('%d/%m/%Y %H:%M')}")

    ranking = sorted(resultados,
                     key=lambda r: r.get('promedio_general', 0),
                     reverse=True)

    all_areas = set()
    for r in ranking:
        for a in r.get('areas', []):
            all_areas.add(a['nombre'])
    all_areas = sorted(all_areas)

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

    n_areas = len(all_areas)
    col_widths = [25, 160, 60] + [45] * n_areas + [45]

    tabla = Table(data, colWidths=col_widths, repeatRows=1)
    st_list = [
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
    bg_top = [
        colors.Color(1, 0.84, 0),
        colors.Color(0.75, 0.75, 0.75),
        colors.Color(0.8, 0.5, 0.2),
    ]
    for i in range(min(3, len(ranking))):
        st_list.append(('BACKGROUND', (0, i + 1), (-1, i + 1), bg_top[i]))
    tabla.setStyle(TableStyle(st_list))
    tw, th_t = tabla.wrap(w - 60, h - 150)
    tabla.drawOn(c, 30, h - 120 - th_t)

    c.setFont("Helvetica", 7)
    c.drawCentredString(w / 2, 30,
                        f"Sistema YACHAY PRO — {hora_peru().strftime('%d/%m/%Y %H:%M')}")
    c.save()
    buffer.seek(0)
    return buffer


# ================================================================
# GENERADOR DE CARNETS (Alumno + Docente)
# ================================================================

class GeneradorCarnet:
    WIDTH = 1012
    HEIGHT = 638
    AZUL = (0, 30, 120)
    DORADO = (255, 215, 0)

    def __init__(self, datos, anio, foto_bytes=None, es_docente=False):
        self.datos = datos
        self.anio = anio
        self.foto_bytes = foto_bytes
        self.es_docente = es_docente
        self.img = Image.new('RGB', (self.WIDTH, self.HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.img)

    def _escudo_fondo(self):
        if Path("escudo_upload.png").exists():
            try:
                escudo = Image.open("escudo_upload.png").convert("RGBA")
                escudo = escudo.resize((280, 280), Image.LANCZOS)
                capa = Image.new('RGBA', (self.WIDTH, self.HEIGHT), (255, 255, 255, 0))
                x = (self.WIDTH - 280) // 2
                y = (self.HEIGHT - 280) // 2
                capa.paste(escudo, (x, y))
                px = list(capa.getdata())
                px = [(d[0], d[1], d[2], min(d[3], 28)) for d in px]
                capa.putdata(px)
                base = self.img.convert('RGBA')
                self.img = Image.alpha_composite(base, capa).convert('RGB')
                self.draw = ImageDraw.Draw(self.img)
            except Exception:
                pass

    def _barras(self):
        self.draw.rectangle([(0, 0), (self.WIDTH, 210)], fill=self.AZUL)
        self.draw.rectangle([(0, 207), (self.WIDTH, 213)], fill=self.DORADO)
        self.draw.rectangle([(0, self.HEIGHT - 65), (self.WIDTH, self.HEIGHT)],
                            fill=self.AZUL)
        self.draw.rectangle([(0, self.HEIGHT - 68), (self.WIDTH, self.HEIGHT - 63)],
                            fill=self.DORADO)

    def _textos(self):
        fh = RecursoManager.obtener_fuente("", 36, bold=True)
        fm = RecursoManager.obtener_fuente("", 19, bold=True)
        fc = RecursoManager.obtener_fuente("", 17, bold=True)
        fp = RecursoManager.obtener_fuente("", 13, bold=True)
        self.draw.text((self.WIDTH // 2, 65), "I.E. ALTERNATIVO YACHAY",
                       font=fh, fill="white", anchor="mm")
        self.draw.text((self.WIDTH // 2, 115), '"EDUCAR PARA LA VIDA"',
                       font=fm, fill=self.DORADO, anchor="mm")
        tipo_txt = "CARNET DOCENTE" if self.es_docente else "CARNET ESCOLAR"
        self.draw.text((self.WIDTH // 2, 160),
                       f"{tipo_txt} {self.anio}",
                       font=fc, fill="white", anchor="mm")
        self.draw.text((self.WIDTH // 2, self.HEIGHT - 35),
                       "PIONEROS EN LA EDUCACIÓN DE CALIDAD",
                       font=fp, fill=self.DORADO, anchor="mm")

    def _foto(self):
        x, y, wf, hf = 40, 228, 220, 280
        if self.foto_bytes:
            try:
                f = Image.open(self.foto_bytes).convert("RGB")
                f = f.resize((wf, hf), Image.LANCZOS)
                self.img.paste(f, (x, y))
            except Exception:
                self._placeholder(x, y, wf, hf)
        else:
            self._placeholder(x, y, wf, hf)
        self.draw.rectangle([(x - 3, y - 3), (x + wf + 3, y + hf + 3)],
                            outline=self.DORADO, width=4)

    def _placeholder(self, x, y, w, h):
        self.draw.rectangle([(x, y), (x + w, y + h)], fill="#eeeeee")
        font = RecursoManager.obtener_fuente("", 15)
        self.draw.text((x + w // 2, y + h // 2), "SIN FOTO",
                       font=font, fill="#999", anchor="mm")

    def _datos(self):
        xt = 290
        nombre = self.datos.get('Nombre', self.datos.get('alumno', '')).upper()
        dni = str(self.datos.get('DNI', self.datos.get('dni', '')))
        fn = RecursoManager.obtener_fuente("", 19 if len(nombre) > 25 else 22,
                                           bold=True)
        fl = RecursoManager.obtener_fuente("", 14, bold=True)
        fd = RecursoManager.obtener_fuente("", 14)
        yc = 240
        if len(nombre) > 28:
            for linea in textwrap.TextWrapper(width=28).wrap(nombre)[:3]:
                self.draw.text((xt, yc), linea, font=fn, fill="black")
                yc += 26
        else:
            self.draw.text((xt, yc), nombre, font=fn, fill="black")
            yc += 30
        yc += 8
        self.draw.text((xt, yc), "DNI:", font=fl, fill="black")
        self.draw.text((xt + 60, yc), dni, font=fd, fill="black")
        yc += 28
        if self.es_docente:
            cargo = self.datos.get('Cargo', 'DOCENTE').upper()
            esp = self.datos.get('Especialidad', '').upper()
            self.draw.text((xt, yc), "CARGO:", font=fl, fill="black")
            self.draw.text((xt + 90, yc), cargo, font=fd, fill="black")
            yc += 28
            if esp:
                self.draw.text((xt, yc), "ESPEC.:", font=fl, fill="black")
                self.draw.text((xt + 100, yc), esp[:20], font=fd, fill="black")
                yc += 28
        else:
            grado = self.datos.get('Grado', self.datos.get('grado', 'N/A')).upper()
            seccion = self.datos.get('Seccion', self.datos.get('seccion', ''))
            self.draw.text((xt, yc), "GRADO:", font=fl, fill="black")
            self.draw.text((xt + 90, yc), grado, font=fd, fill="black")
            yc += 28
            if seccion:
                self.draw.text((xt, yc), "SECCIÓN:", font=fl, fill="black")
                self.draw.text((xt + 110, yc), str(seccion), font=fd, fill="black")
                yc += 28
        self.draw.text((xt, yc), "VIGENCIA:", font=fl, fill="black")
        self.draw.text((xt + 120, yc), str(self.anio), font=fd, fill="black")

    def _qr(self):
        try:
            dni = str(self.datos.get('DNI', self.datos.get('dni', '')))
            q = qrcode.QRCode(box_size=8, border=1)
            q.add_data(dni)
            q.make(fit=True)
            iq = q.make_image(fill_color="black", back_color="white")
            iq = iq.resize((140, 140), Image.LANCZOS)
            xq = self.WIDTH - 180
            yq = 240
            self.img.paste(iq, (xq, yq))
            fs = RecursoManager.obtener_fuente("", 9, bold=True)
            self.draw.text((xq + 70, yq + 145), "ESCANEAR QR",
                           font=fs, fill="black", anchor="mm")
        except Exception:
            pass

    def _barcode(self):
        if not HAS_BARCODE:
            return
        try:
            dni = str(self.datos.get('DNI', self.datos.get('dni', '')))
            writer = ImageWriter()
            buf2 = io.BytesIO()
            Code128(dni, writer=writer).write(buf2, options={
                'write_text': False,
                'module_width': 0.4,
                'module_height': 8,
                'quiet_zone': 2
            })
            buf2.seek(0)
            ib = Image.open(buf2)
            ib = ib.crop(ib.getbbox())
            ib = ib.resize((280, 45), Image.LANCZOS)
            xb = (self.WIDTH - 280) // 2
            yb = self.HEIGHT - 120
            self.img.paste(ib, (xb, yb))
            fbc = RecursoManager.obtener_fuente("", 10, bold=True)
            self.draw.text((self.WIDTH // 2, yb + 50),
                           f"DNI: {dni}",
                           font=fbc, fill="black", anchor="mm")
        except Exception:
            pass

    def generar(self):
        self._escudo_fondo()
        self._barras()
        self._textos()
        self._foto()
        self._datos()
        self._qr()
        self._barcode()
        output = io.BytesIO()
        self.img.save(output, format='PNG', optimize=True, quality=95)
        output.seek(0)
        return output


# ================================================================
# CARNETS EN LOTE PDF — 8 POR HOJA (tamaño fotocheck)
# ================================================================

def generar_carnets_lote_pdf(lista_datos, anio, es_docente=False):
    """
    Genera PDF con 8 carnets por página A4 portrait.
    Layout: 2 columnas × 4 filas con líneas de corte.
    Tamaño por carnet: ~90mm × 57mm (fotocheck estándar).
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    # Dimensiones en puntos (1mm = 2.835pt)
    margen_x = 15 * mm
    margen_y = 10 * mm
    card_w = (w - 2 * margen_x - 5 * mm) / 2  # 2 columnas, 5mm gap
    card_h = (h - 2 * margen_y - 15 * mm) / 4  # 4 filas, gaps
    gap_x = 5 * mm
    gap_y = 3.5 * mm

    por_pagina = 8
    total = len(lista_datos)
    num_paginas = (total + por_pagina - 1) // por_pagina

    for pag in range(num_paginas):
        if pag > 0:
            c.showPage()

        inicio = pag * por_pagina
        fin = min(inicio + por_pagina, total)

        for idx in range(inicio, fin):
            pos = idx - inicio
            col = pos % 2
            fila = pos // 2
            x = margen_x + col * (card_w + gap_x)
            y = h - margen_y - (fila + 1) * card_h - fila * gap_y

            # Generar carnet como imagen
            datos_carnet = lista_datos[idx]
            gen = GeneradorCarnet(datos_carnet, anio, es_docente=es_docente)
            img_bytes = gen.generar()

            # Guardar temporalmente
            tmp = f"tmp_carnet_{idx}.png"
            with open(tmp, 'wb') as f:
                f.write(img_bytes.getvalue())

            try:
                c.drawImage(tmp, x, y, width=card_w, height=card_h,
                            preserveAspectRatio=True)
                # Líneas de corte (punteadas)
                c.setStrokeColor(colors.grey)
                c.setDash(3, 3)
                c.setLineWidth(0.3)
                c.rect(x, y, card_w, card_h)
                c.setDash()
            except Exception:
                pass

            try:
                os.remove(tmp)
            except Exception:
                pass

        # Pie de página
        c.setFont("Helvetica", 6)
        c.setFillColor(colors.grey)
        c.drawCentredString(w / 2, 10,
                            f"I.E.P. ALTERNATIVO YACHAY — Carnets {anio} — "
                            f"Página {pag + 1}/{num_paginas} — "
                            f"Cortar por las líneas punteadas")
        c.setFillColor(colors.black)

    c.save()
    buffer.seek(0)
    return buffer


# ================================================================
# UTILIDADES
# ================================================================

def generar_link_whatsapp(telefono, mensaje):
    tel = str(telefono).strip().replace("+", "").replace(" ", "").replace("-", "")
    if len(tel) == 9:
        tel = "51" + tel
    elif not tel.startswith("51"):
        tel = "51" + tel
    return f"https://wa.me/{tel}?text={urllib.parse.quote(mensaje)}"


def generar_mensaje_asistencia(nombre, tipo, hora):
    saludo = "Buenos días" if int(hora.split(':')[0]) < 12 else "Buenas tardes"
    if tipo == "entrada":
        emoji, txt = "✅", "ENTRADA"
    else:
        emoji, txt = "🏁", "SALIDA"
    return (f"{saludo}\n🏫 I.E. ALTERNATIVO YACHAY informa:\n"
            f"{emoji} *{txt}* registrada\n👤 {nombre}\n🕒 Hora: {hora}")


def decodificar_qr_imagen(image_bytes):
    if not HAS_PYZBAR:
        return None
    try:
        img = Image.open(io.BytesIO(image_bytes))
        codigos = pyzbar_decode(img)
        if codigos:
            return codigos[0].data.decode('utf-8')
    except Exception:
        pass
    if HAS_CV2:
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            for method in [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV]:
                _, thresh = cv2.threshold(gray, 127, 255, method)
                codigos = pyzbar_decode(Image.fromarray(thresh))
                if codigos:
                    return codigos[0].data.decode('utf-8')
        except Exception:
            pass
    return None


# ================================================================
# HOJA DE RESPUESTAS (IMAGEN) Y PROCESAMIENTO
# ================================================================

def generar_hoja_respuestas(num_preguntas, titulo):
    width, height = 2480, 3508
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    try:
        ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 45)
        fn = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        fl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
    except Exception:
        ft = fs = fn = fl = ImageFont.load_default()

    # Marcadores de alineación
    sz = 80
    for pos in [(50, 50), (width - 130, 50),
                (50, height - 130), (width - 130, height - 130)]:
        draw.rectangle([pos, (pos[0] + sz, pos[1] + sz)], fill="black")

    draw.text((width // 2, 200), "I.E.P. ALTERNATIVO YACHAY",
              font=ft, fill="black", anchor="mm")
    draw.text((width // 2, 280),
              f"HOJA DE RESPUESTAS — {titulo.upper()}",
              font=fs, fill="black", anchor="mm")
    draw.text((width // 2, 350),
              "SISTEMA DE CALIFICACIÓN YACHAY",
              font=fs, fill="gray", anchor="mm")
    draw.text((200, 480),
              "Nombre: ________________________________________",
              font=fs, fill="black")
    draw.text((200, 560),
              "DNI: ________________  Grado: ________________",
              font=fs, fill="black")
    draw.text((200, 640),
              f"Fecha: ________________  Preguntas: {num_preguntas}",
              font=fs, fill="black")
    draw.text((200, 740),
              "Rellene completamente el círculo de la alternativa.",
              font=fl, fill="gray")

    sy, sx = 900, 300
    sp = 100
    csp = 700
    ppc = min(25, (height - sy - 200) // sp)
    for i in range(num_preguntas):
        col = i // ppc
        fi = i % ppc
        xb = sx + (col * csp)
        yb = sy + (fi * sp)
        draw.text((xb - 100, yb), f"{i + 1}.",
                  font=fn, fill="black", anchor="rm")
        for j, letra in enumerate(['A', 'B', 'C', 'D']):
            cx = xb + (j * 130)
            draw.ellipse([(cx - 35, yb - 35), (cx + 35, yb + 35)],
                         outline="black", width=4)
            draw.text((cx, yb), letra, font=fl, fill="black", anchor="mm")

    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output


def procesar_examen(img_bytes, num_preguntas):
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
        burbujas = []
        for ct in contours:
            x, y, w_c, h_c = cv2.boundingRect(ct)
            ar = w_c / float(h_c) if h_c > 0 else 0
            area = cv2.contourArea(ct)
            if 0.7 <= ar <= 1.3 and 15 <= w_c <= 120 and 15 <= h_c <= 120 and area > 200:
                burbujas.append((ct, x, y, w_c, h_c))
        if not burbujas:
            return None
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
        respuestas = []
        for fila in filas[:num_preguntas]:
            opciones = fila[:4]
            intensidades = []
            for (ct, x, y, w_c, h_c) in opciones:
                mask = np.zeros(gray.shape, dtype="uint8")
                cv2.drawContours(mask, [ct], -1, 255, -1)
                masked = cv2.bitwise_and(thresh, thresh, mask=mask)
                intensidades.append(cv2.countNonZero(masked))
            if intensidades:
                mi = intensidades.index(max(intensidades))
                respuestas.append(['A', 'B', 'C', 'D'][min(mi, 3)])
            else:
                respuestas.append('?')
        return respuestas if respuestas else None
    except Exception:
        return None


# ================================================================
# PANTALLA DE LOGIN (Nombre de usuario + Contraseña — SEGURO)
# ================================================================

def pantalla_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if Path("escudo_upload.png").exists():
            st.image("escudo_upload.png", width=220, use_container_width=False)

        st.markdown("""
        <div class='main-header'>
            <h1 style='color:white;margin:0;font-size:2.2rem;'>🎓 SISTEMA YACHAY PRO</h1>
            <p style='color:#ccc;margin:5px 0;'>Sistema Integral de Gestión Educativa</p>
            <p style='color:#FFD700;font-style:italic;font-size:1.1rem;'>"Educar para la Vida"</p>
            <p style='color:#FFD700;font-size:0.9rem;'>Pioneros en la Educación de Calidad</p>
            <hr style='border-color:#FFD700;margin:15px 50px;'>
            <p style='color:#aaa;font-size:0.85rem;'>📍 Chinchero, Cusco — Perú</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        usuario = st.text_input("👤 Nombre de usuario:", key="login_user",
                                placeholder="Ingrese su usuario")
        contrasena = st.text_input("🔑 Contraseña:", type="password",
                                    key="login_pwd",
                                    placeholder="Ingrese su contraseña")

        if st.button("🔐 INGRESAR AL SISTEMA", use_container_width=True,
                     type="primary"):
            usuario_lower = usuario.strip().lower()
            if usuario_lower in USUARIOS:
                datos_usuario = USUARIOS[usuario_lower]
                if contrasena == datos_usuario['password']:
                    st.session_state.rol = datos_usuario['rol']
                    st.session_state.docente_info = datos_usuario.get('docente_info')
                    st.session_state.usuario_actual = usuario_lower
                    st.rerun()
                else:
                    st.error("⛔ Contraseña incorrecta")
            else:
                st.error("⛔ Usuario no encontrado")

        st.caption("💡 Ingrese su nombre de usuario y contraseña asignados "
                   "por el administrador.")


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
        label = roles_nombres.get(st.session_state.rol, '')
        if st.session_state.rol == "docente" and st.session_state.docente_info:
            label += f" — {st.session_state.docente_info['label']}"
        st.info(f"**{label}**")
        st.caption(f"🕒 {hora_peru().strftime('%H:%M:%S')} | "
                   f"📅 {hora_peru().strftime('%d/%m/%Y')}")
        st.markdown("---")

        directora = "Prof. Ana María CUSI INCA"
        promotor = "Prof. Leandro CORDOVA TOCRE"
        frase = "Año de la Esperanza y el Fortalecimiento de la Democracia"

        if st.session_state.rol == "admin":
            with st.expander("📂 Archivos"):
                ub = st.file_uploader("📊 Base Datos", type=["xlsx"], key="ub")
                if ub:
                    with open(ARCHIVO_BD, "wb") as f:
                        f.write(ub.getbuffer())
                    st.success("✅")
                    st.rerun()
                uf = st.file_uploader("🖼️ Fondo docs", type=["png"], key="uf")
                if uf:
                    with open("fondo.png", "wb") as f:
                        f.write(uf.getbuffer())
                    st.success("✅")
                ue = st.file_uploader("🛡️ Escudo/Logo", type=["png"], key="ue")
                if ue:
                    with open("escudo_upload.png", "wb") as f:
                        f.write(ue.getbuffer())
                    st.success("✅")

            with st.expander("👥 Autoridades"):
                directora = st.text_input("Directora:", directora, key="di")
                promotor = st.text_input("Promotor:", promotor, key="pi")

            with st.expander("🎯 Título del Año"):
                frase = st.text_input("Frase:", frase, key="fi")

            with st.expander("🔐 Usuarios del Sistema"):
                st.caption("**Lista de usuarios registrados:**")
                for usr, datos in USUARIOS.items():
                    st.caption(f"• **{usr}** → {datos.get('label', datos['rol'])}")

        st.markdown("---")
        anio = st.number_input("📅 Año:", 2024, 2040, 2026, key="ai")
        stats = BaseDatos.obtener_estadisticas()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📚 Alumnos", stats['total_alumnos'])
        with col2:
            st.metric("👨‍🏫 Docentes", stats['total_docentes'])
        st.markdown("---")
        if st.button("🔴 CERRAR SESIÓN", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    return {
        'anio': anio,
        'directora': directora,
        'promotor': promotor,
        'frase': frase,
        'y_frase': 700,
        'y_titulo': 630,
        'qr_x': 435,
        'qr_y': 47
    }


# ================================================================
# TAB: MATRÍCULA (Alumnos + Docentes)
# ================================================================

def tab_matricula(config):
    st.header("📝 Matrícula")
    tab_est, tab_doc, tab_lista, tab_pdf = st.tabs([
        "➕ Registrar Alumno", "👨‍🏫 Registrar Docente",
        "📋 Listas", "⬇️ Registros PDF"
    ])

    # ---- REGISTRAR ALUMNO ----
    with tab_est:
        st.subheader("📝 Matrícula de Estudiante")
        c1, c2 = st.columns(2)
        with c1:
            nm = st.text_input("Apellidos y Nombres:", key="mn")
            dn = st.text_input("DNI:", key="md", max_chars=8)
            nv = st.selectbox("Nivel:", list(NIVELES_GRADOS.keys()), key="mnv")
            gr = st.selectbox("Grado:", NIVELES_GRADOS[nv], key="mg")
            sc = st.selectbox("Sección:", SECCIONES, key="ms")
        with c2:
            ap = st.text_input("Apoderado:", key="ma")
            da = st.text_input("DNI Apoderado:", key="mda", max_chars=8)
            ce = st.text_input("Celular Apoderado:", key="mc", max_chars=9)
        if st.button("✅ MATRICULAR", type="primary", use_container_width=True, key="bm"):
            if nm and dn:
                BaseDatos.registrar_estudiante({
                    'Nombre': nm.strip(), 'DNI': dn.strip(), 'Nivel': nv,
                    'Grado': gr, 'Seccion': sc, 'Apoderado': ap.strip(),
                    'DNI_Apoderado': da.strip(), 'Celular_Apoderado': ce.strip()
                })
                st.success(f"✅ {nm} → {gr} {sc}")
                st.balloons()
            else:
                st.error("⚠️ Nombre y DNI requeridos")

    # ---- REGISTRAR DOCENTE ----
    with tab_doc:
        st.subheader("👨‍🏫 Registro de Docente / Personal")
        c1, c2 = st.columns(2)
        with c1:
            nd = st.text_input("Apellidos y Nombres:", key="dn_nom")
            dd = st.text_input("DNI:", key="dn_dni", max_chars=8)
            cd = st.selectbox("Cargo:", [
                "Docente", "Directora", "Auxiliar", "Coordinador",
                "Secretaria", "Personal de Limpieza", "Otro"
            ], key="dn_cargo")
        with c2:
            ed = st.text_input("Especialidad:", key="dn_esp",
                               placeholder="Ej: Educación Primaria")
            td = st.text_input("Celular:", key="dn_cel", max_chars=9)
            gd = st.selectbox("Grado Asignado:",
                              ["N/A"] + TODOS_LOS_GRADOS, key="dn_grado")
        if st.button("✅ REGISTRAR DOCENTE", type="primary",
                     use_container_width=True, key="bd"):
            if nd and dd:
                BaseDatos.registrar_docente({
                    'Nombre': nd.strip(), 'DNI': dd.strip(),
                    'Cargo': cd, 'Especialidad': ed.strip(),
                    'Celular': td.strip(), 'Grado_Asignado': gd
                })
                st.success(f"✅ {nd} registrado como {cd}")
                st.balloons()
            else:
                st.error("⚠️ Nombre y DNI requeridos")

    # ---- LISTAS ----
    with tab_lista:
        st.subheader("📋 Alumnos Matriculados")
        df = BaseDatos.cargar_matricula()
        if not df.empty:
            c1, c2, c3 = st.columns(3)
            with c1:
                fn = st.selectbox("Nivel:", ["Todos"] + list(NIVELES_GRADOS.keys()),
                                  key="fn")
            with c2:
                go = ["Todos"] + (NIVELES_GRADOS[fn] if fn != "Todos"
                                  else TODOS_LOS_GRADOS)
                fg = st.selectbox("Grado:", go, key="fg")
            with c3:
                bq = st.text_input("🔍", key="bq")
            d = df.copy()
            if fn != "Todos" and 'Nivel' in d.columns:
                d = d[d['Nivel'] == fn]
            if fg != "Todos" and 'Grado' in d.columns:
                d = d[d['Grado'] == fg]
            if bq:
                d = d[d.apply(lambda r: bq.lower() in str(r).lower(), axis=1)]
            if 'Nombre' in d.columns:
                d = d.sort_values('Nombre')
            st.metric("Resultados", len(d))
            st.dataframe(d, use_container_width=True, hide_index=True, height=400)
            buf = io.BytesIO()
            d.to_excel(buf, index=False, engine='openpyxl')
            buf.seek(0)
            st.download_button("⬇️ Excel", buf,
                               f"Matricula_{config['anio']}.xlsx", key="dme")
            with st.expander("🗑️ Eliminar Alumno"):
                deld = st.text_input("DNI:", key="dd")
                if st.button("🗑️", key="bdel"):
                    if deld:
                        BaseDatos.eliminar_estudiante(deld)
                        st.rerun()
        else:
            st.info("📝 Sin alumnos.")

        st.markdown("---")
        st.subheader("👨‍🏫 Docentes Registrados")
        df_doc = BaseDatos.cargar_docentes()
        if not df_doc.empty:
            if 'Nombre' in df_doc.columns:
                df_doc = df_doc.sort_values('Nombre')
            st.dataframe(df_doc, use_container_width=True, hide_index=True)
            buf2 = io.BytesIO()
            df_doc.to_excel(buf2, index=False, engine='openpyxl')
            buf2.seek(0)
            st.download_button("⬇️ Excel Docentes", buf2,
                               "docentes.xlsx", key="dmedoc")
            with st.expander("🗑️ Eliminar Docente"):
                deld2 = st.text_input("DNI:", key="dddoc")
                if st.button("🗑️", key="bdeldoc"):
                    if deld2:
                        BaseDatos.eliminar_docente(deld2)
                        st.rerun()
        else:
            st.info("📝 Sin docentes registrados.")

    # ---- REGISTROS PDF ----
    with tab_pdf:
        _seccion_registros_pdf(config)


def _seccion_registros_pdf(config):
    """Genera PDFs de registro auxiliar y asistencia"""
    df = BaseDatos.cargar_matricula()
    if df.empty:
        st.info("📝 Registra estudiantes primero.")
        return

    c1, c2 = st.columns(2)
    with c1:
        np_ = st.selectbox("Nivel:", list(NIVELES_GRADOS.keys()), key="pn")
        gp = st.selectbox("Grado:", NIVELES_GRADOS[np_], key="pg")
    with c2:
        sp = st.selectbox("Sección:", ["Todas"] + SECCIONES, key="ps")
    dg = BaseDatos.obtener_estudiantes_grado(gp, sp)
    st.info(f"📊 {len(dg)} estudiantes (orden alfabético)")

    # ---- REGISTRO AUXILIAR ----
    st.markdown("---")
    st.markdown("**📝 Registro Auxiliar (Cursos × Competencias × Desempeños)**")
    bim = st.selectbox("Bimestre:", list(BIMESTRES.keys()), key="bim_sel")
    st.markdown("**Cursos (hasta 3 por hoja):**")
    c1, c2, c3 = st.columns(3)
    with c1:
        curso1 = st.text_input("Curso 1:", "Matemática", key="c1")
    with c2:
        curso2 = st.text_input("Curso 2:", "Comunicación", key="c2")
    with c3:
        curso3 = st.text_input("Curso 3:", "Ciencia y Tec.", key="c3")

    cursos = [c for c in [curso1, curso2, curso3] if c.strip()]
    st.caption(f"Se generarán {len(cursos)} cursos × 4 competencias × "
               f"3 desempeños cada una")

    if st.button("📝 Generar Registro Auxiliar PDF", type="primary",
                 use_container_width=True, key="gra"):
        sl = sp if sp != "Todas" else "Todas"
        pdf = generar_registro_auxiliar_pdf(gp, sl, config['anio'], bim, dg, cursos)
        st.download_button("⬇️ Descargar Registro Auxiliar", pdf,
                           f"RegAux_{gp}_{bim}.pdf",
                           "application/pdf", key="dra")

    # ---- REGISTRO ASISTENCIA ----
    st.markdown("---")
    st.markdown("**📋 Registro Asistencia (sin sáb/dom, sin feriados)**")
    meses_opts = list(MESES_ESCOLARES.items())
    meses_sel = st.multiselect(
        "Meses:",
        [f"{v} ({k})" for k, v in meses_opts],
        default=[f"{v} ({k})" for k, v in meses_opts[:3]],
        key="msel"
    )
    meses_nums = [int(m.split('(')[1].replace(')', '')) for m in meses_sel]
    if st.button("📋 Generar Registro Asistencia PDF", type="primary",
                 use_container_width=True, key="gras"):
        if meses_nums:
            sl = sp if sp != "Todas" else "Todas"
            pdf = generar_registro_asistencia_pdf(
                gp, sl, config['anio'], dg, meses_nums
            )
            st.download_button("⬇️ Descargar", pdf,
                               f"RegAsist_{gp}.pdf",
                               "application/pdf", key="dras")


# ================================================================
# TAB: DOCUMENTOS
# ================================================================

def tab_documentos(config):
    st.header("📄 Documentos")
    c1, c2 = st.columns([1, 2])
    with c1:
        td = st.selectbox("📑 Tipo:", [
            "CONSTANCIA DE VACANTE", "CONSTANCIA DE NO DEUDOR",
            "CONSTANCIA DE ESTUDIOS", "CONSTANCIA DE CONDUCTA",
            "CARTA COMPROMISO", "RESOLUCIÓN DE TRASLADO"
        ], key="td")
        st.markdown("---")
        db = st.text_input("🔍 DNI:", key="db")
        if st.button("🔎", use_container_width=True, key="bb"):
            r = BaseDatos.buscar_por_dni(db)
            if r:
                st.session_state.alumno = r.get('Nombre', '')
                st.session_state.dni = r.get('DNI', '')
                st.session_state.grado = r.get('Grado', '')
                st.session_state.apoderado = r.get('Apoderado', '')
                st.session_state.dni_apo = r.get('DNI_Apoderado', '')
                st.success("✅")
                st.rerun()
            else:
                st.error("❌")
    with c2:
        with st.container(border=True):
            nm = st.text_input("👤 Nombre:", key="alumno")
            dn = st.text_input("🆔 DNI:", key="dni")
            gr = st.text_input("📚 Grado:", key="grado")
            ap = st.text_input("👨‍👩‍👧 Apoderado:", key="apoderado")
            da = st.text_input("🆔 DNI Apo:", key="dni_apo")
            nc = {}
            if td == "CONSTANCIA DE CONDUCTA":
                cols = st.columns(5)
                for i, col in enumerate(cols):
                    with col:
                        nc[f'nota_conducta_{i+1}'] = st.selectbox(
                            f"{i+1}°", ["AD", "A", "B", "C"], key=f"n{i}"
                        )
            ex = {}
            if td == "RESOLUCIÓN DE TRASLADO":
                ex['num_resolucion'] = st.text_input("N° Res:", key="nr")
                ex['fecha_resolucion'] = st.text_input("Fecha:", key="fr2")
                ex['nivel'] = st.selectbox("Nivel:",
                                           ["INICIAL", "PRIMARIA", "SECUNDARIA"],
                                           key="nl")
                ex['ie_destino'] = st.text_input("IE Dest:", key="ie")
        if st.button("✨ GENERAR", type="primary", use_container_width=True,
                     key="gd"):
            if nm and dn:
                d = {'alumno': nm, 'dni': dn, 'grado': gr,
                     'apoderado': ap, 'dni_apo': da, **nc, **ex}
                g = GeneradorPDF(config)
                metodos = {
                    "CONSTANCIA DE VACANTE": g.generar_constancia_vacante,
                    "CONSTANCIA DE NO DEUDOR": g.generar_constancia_no_deudor,
                    "CONSTANCIA DE ESTUDIOS": g.generar_constancia_estudios,
                    "CONSTANCIA DE CONDUCTA": g.generar_constancia_conducta,
                    "CARTA COMPROMISO": g.generar_carta_compromiso,
                    "RESOLUCIÓN DE TRASLADO": g.generar_resolucion_traslado,
                }
                pdf = metodos[td](d)
                st.success("✅")
                st.download_button("⬇️ PDF", pdf,
                                   f"{nm}_{td}.pdf", "application/pdf",
                                   use_container_width=True, key="dd2")


# ================================================================
# TAB: CARNETS (Individual, Matrícula, Lote PDF 8 por hoja)
# ================================================================

def tab_carnets(config):
    st.header("🪪 Centro de Carnetización")
    t1, t2, t3, t4 = st.tabs([
        "⚡ Individual", "📋 Desde Matrícula",
        "📦 Lote Alumnos (PDF)", "👨‍🏫 Lote Docentes (PDF)"
    ])

    with t1:
        c1, c2 = st.columns(2)
        with c1:
            cn = st.text_input("👤 Nombre:", key="cn")
            cd = st.text_input("🆔 DNI:", key="cd")
            cg = st.selectbox("📚 Grado:", TODOS_LOS_GRADOS, key="cg")
            cs = st.selectbox("📂 Sección:", SECCIONES, key="cs")
        with c2:
            cf = st.file_uploader("📸 Foto:", type=['jpg', 'png', 'jpeg'], key="cf")
            if cf:
                st.image(cf, width=180)
        if st.button("🪪 GENERAR", type="primary", use_container_width=True,
                     key="gc"):
            if cn and cd:
                fi = io.BytesIO(cf.getvalue()) if cf else None
                cr = GeneradorCarnet(
                    {'Nombre': cn, 'DNI': cd, 'Grado': cg, 'Seccion': cs},
                    config['anio'], fi
                ).generar()
                st.image(cr, use_container_width=True)
                st.download_button("⬇️", cr,
                                   f"Carnet_{cn.replace(' ', '_')}.png",
                                   "image/png", use_container_width=True,
                                   key="dc")

    with t2:
        dbs = st.text_input("🔍 DNI:", key="cbd")
        if st.button("🔎", key="cbb"):
            a = BaseDatos.buscar_por_dni(dbs)
            if a:
                st.session_state['ce'] = a
                st.success(f"✅ {a.get('Nombre', '')}")
            else:
                st.error("❌")
        if st.session_state.get('ce'):
            a = st.session_state['ce']
            es_doc = a.get('_tipo', '') == 'docente'
            tipo_txt = "DOCENTE" if es_doc else "ALUMNO"
            st.markdown(f"**[{tipo_txt}]** {a.get('Nombre', '')} | "
                        f"DNI: {a.get('DNI', '')}")
            fm = st.file_uploader("📸", type=['jpg', 'png', 'jpeg'], key="cfm")
            if st.button("🪪 GENERAR", type="primary",
                         use_container_width=True, key="gcm"):
                fi = io.BytesIO(fm.getvalue()) if fm else None
                cr = GeneradorCarnet(a, config['anio'], fi,
                                     es_docente=es_doc).generar()
                st.image(cr, use_container_width=True)
                st.download_button("⬇️", cr, "Carnet.png", "image/png",
                                   use_container_width=True, key="dcm")

    with t3:
        st.subheader("📦 Carnets Alumnos — PDF (8 por hoja)")
        st.caption("Tamaño fotocheck con líneas de corte para plastificar")
        df = BaseDatos.cargar_matricula()
        if not df.empty:
            nl = st.selectbox("Nivel:", ["Todos"] + list(NIVELES_GRADOS.keys()),
                              key="ln")
            d = df.copy()
            if nl != "Todos" and 'Nivel' in d.columns:
                d = d[d['Nivel'] == nl]
            if 'Nombre' in d.columns:
                d = d.sort_values('Nombre')
            st.info(f"📊 {len(d)} carnets de alumnos")
            if st.button("🚀 GENERAR PDF CARNETS", type="primary",
                         use_container_width=True, key="gl"):
                progreso = st.progress(0)
                st.info("Generando carnets...")
                lista = d.to_dict('records')
                pdf = generar_carnets_lote_pdf(lista, config['anio'],
                                               es_docente=False)
                progreso.progress(100)
                st.balloons()
                st.download_button("⬇️ DESCARGAR PDF", pdf,
                                   f"Carnets_Alumnos_{config['anio']}.pdf",
                                   "application/pdf",
                                   use_container_width=True, key="dlz")
        else:
            st.info("📝 Registra estudiantes.")

    with t4:
        st.subheader("👨‍🏫 Carnets Docentes — PDF (8 por hoja)")
        st.caption("Tamaño fotocheck con líneas de corte para plastificar")
        df_doc = BaseDatos.cargar_docentes()
        if not df_doc.empty:
            if 'Nombre' in df_doc.columns:
                df_doc = df_doc.sort_values('Nombre')
            st.info(f"📊 {len(df_doc)} carnets de docentes")
            st.dataframe(df_doc[['Nombre', 'DNI', 'Cargo']],
                         use_container_width=True, hide_index=True)
            if st.button("🚀 GENERAR PDF CARNETS DOCENTES", type="primary",
                         use_container_width=True, key="gld"):
                lista = df_doc.to_dict('records')
                pdf = generar_carnets_lote_pdf(lista, config['anio'],
                                               es_docente=True)
                st.balloons()
                st.download_button("⬇️ DESCARGAR PDF", pdf,
                                   f"Carnets_Docentes_{config['anio']}.pdf",
                                   "application/pdf",
                                   use_container_width=True, key="dlzd")
        else:
            st.info("📝 Registra docentes en la pestaña Matrícula.")


# ================================================================
# TAB: ASISTENCIAS (Alumnos + Docentes, borrar día)
# ================================================================

def tab_asistencias():
    st.header("📋 Control de Asistencia")
    st.caption(f"🕒 **{hora_peru().strftime('%H:%M:%S')}** | "
               f"📅 {hora_peru().strftime('%d/%m/%Y')}")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🌅 ENTRADA", use_container_width=True,
                      type="primary" if st.session_state.tipo_asistencia == "Entrada"
                      else "secondary", key="be"):
            st.session_state.tipo_asistencia = "Entrada"
            st.rerun()
    with c2:
        if st.button("🌙 SALIDA", use_container_width=True,
                      type="primary" if st.session_state.tipo_asistencia == "Salida"
                      else "secondary", key="bs"):
            st.session_state.tipo_asistencia = "Salida"
            st.rerun()

    st.info(f"📌 **Modo: {st.session_state.tipo_asistencia}** — "
            f"Registra alumnos y docentes")
    st.markdown("---")

    cc, cm = st.columns(2)
    with cc:
        st.markdown("### 📸 Escanear QR / Código")
        act = st.checkbox("📷 Activar cámara", key="chkc",
                          value=st.session_state.get('activar_camara_asist', False))
        st.session_state.activar_camara_asist = act
        if act:
            foto = st.camera_input("Apunta al QR:", key="ca")
            if foto:
                d = decodificar_qr_imagen(foto.getvalue())
                if d:
                    _registrar_asistencia_ui(d)
                else:
                    st.warning("⚠️ No detectado. Intente de nuevo o use manual.")
        else:
            st.info("💡 Activa la cámara para escanear.")

    with cm:
        st.markdown("### ✏️ Registro Manual")
        dm = st.text_input("DNI:", key="dm")
        if st.button("✅ REGISTRAR", type="primary",
                     use_container_width=True, key="rm"):
            if dm:
                _registrar_asistencia_ui(dm.strip())

    st.markdown("---")
    st.subheader("📊 Registros de Hoy")
    asis = BaseDatos.obtener_asistencias_hoy()
    if asis:
        # Separar alumnos y docentes
        alumnos_hoy = []
        docentes_hoy = []
        for dni_k, v in asis.items():
            registro = {
                'DNI': dni_k,
                'Nombre': v['nombre'],
                'Entrada': v.get('entrada', '—'),
                'Salida': v.get('salida', '—'),
            }
            if v.get('es_docente', False):
                docentes_hoy.append(registro)
            else:
                alumnos_hoy.append(registro)

        if alumnos_hoy:
            st.markdown("**📚 Alumnos:**")
            st.dataframe(pd.DataFrame(alumnos_hoy),
                         use_container_width=True, hide_index=True)
        if docentes_hoy:
            st.markdown("**👨‍🏫 Docentes:**")
            st.dataframe(pd.DataFrame(docentes_hoy),
                         use_container_width=True, hide_index=True)

        # WhatsApp
        st.markdown("### 📱 Enviar por WhatsApp")
        for dni_k, dat in asis.items():
            al = BaseDatos.buscar_por_dni(dni_k)
            if al:
                cel = al.get('Celular_Apoderado', al.get('Celular', ''))
                if cel and cel.strip():
                    msg = (f"🏫 YACHAY\n👤 {dat['nombre']}\n"
                           f"✅ Entrada: {dat.get('entrada', '—')}\n"
                           f"🏁 Salida: {dat.get('salida', '—')}")
                    link = generar_link_whatsapp(cel, msg)
                    st.markdown(
                        f'<a href="{link}" target="_blank" class="wa-btn">'
                        f'📱 {dat["nombre"]} → {cel}</a>',
                        unsafe_allow_html=True
                    )

        st.markdown("---")
        if st.button("🗑️ BORRAR ASISTENCIAS DEL DÍA", type="secondary",
                     use_container_width=True, key="borrar_asist"):
            BaseDatos.borrar_asistencias_hoy()
            st.success("✅ Asistencias del día eliminadas")
            st.rerun()
    else:
        st.info("📝 No hay registros hoy.")


def _registrar_asistencia_ui(dni):
    """Registra asistencia de alumno o docente"""
    persona = BaseDatos.buscar_por_dni(dni)
    if persona:
        hora = hora_peru_str()
        tipo = st.session_state.tipo_asistencia.lower()
        nombre = persona.get('Nombre', '')
        es_doc = persona.get('_tipo', '') == 'docente'
        tipo_persona = "👨‍🏫 DOCENTE" if es_doc else "📚 ALUMNO"
        BaseDatos.guardar_asistencia(dni, nombre, tipo, hora, es_docente=es_doc)
        st.success(f"✅ [{tipo_persona}] **{nombre}** — "
                   f"{st.session_state.tipo_asistencia}: **{hora}**")
        st.balloons()
        cel = persona.get('Celular_Apoderado', persona.get('Celular', ''))
        if cel and cel.strip():
            msg = generar_mensaje_asistencia(nombre, tipo, hora)
            link = generar_link_whatsapp(cel, msg)
            st.markdown(
                f'<a href="{link}" target="_blank" class="wa-btn">'
                f'📱 WhatsApp → {cel}</a>',
                unsafe_allow_html=True
            )
    else:
        st.error(f"❌ DNI {dni} no encontrado")


# ================================================================
# TAB: CALIFICACIÓN YACHAY
# ================================================================

def tab_calificacion_yachay(config):
    st.header("📝 Sistema de Calificación YACHAY")
    tg, tc, tr = st.tabs([
        "📄 Generar Hoja", "✅ Calificar", "🏆 Ranking"
    ])

    with tg:
        st.subheader("📄 Hoja de Respuestas")
        st.markdown("""
        **¿Cómo funciona?**
        1. Genera e imprime la hoja de respuestas
        2. Los alumnos rellenan los círculos
        3. Toma foto o ingresa manualmente
        4. El sistema califica cada área sobre 20 puntos
        """)
        c1, c2 = st.columns(2)
        with c1:
            np_ = st.selectbox("Preguntas:", [10, 20, 30, 40, 50],
                               index=1, key="npg")
        with c2:
            th = st.text_input("Título:", "EVALUACIÓN BIMESTRAL", key="th")
        if st.button("📄 GENERAR", type="primary",
                     use_container_width=True, key="gh"):
            hoja = generar_hoja_respuestas(np_, th)
            st.image(hoja, use_container_width=True)
            st.download_button("⬇️", hoja,
                               f"Hoja_{np_}p.png", "image/png",
                               use_container_width=True, key="dh")

    with tc:
        st.subheader("✅ Calificar Examen")
        st.markdown("**1️⃣ Áreas** (cada una sobre 20 puntos)")
        if 'areas_examen' not in st.session_state:
            st.session_state.areas_examen = []
        ca, cn_, cb = st.columns([2, 1, 1])
        with ca:
            na = st.text_input("Área:", key="na")
        with cn_:
            nn = st.selectbox("Preguntas:", [5, 10, 15, 20, 25, 30],
                              index=1, key="nn")
        with cb:
            st.markdown("###")
            if st.button("➕", key="aa"):
                if na:
                    st.session_state.areas_examen.append({
                        'nombre': na, 'num': nn, 'claves': ''
                    })
                    st.rerun()

        tp = 0
        tc_ = []
        ia = []
        for i, a in enumerate(st.session_state.areas_examen):
            with st.expander(
                f"📚 {a['nombre']} ({a['num']}p → sobre 20)", expanded=True
            ):
                cl = st.text_input(f"Claves:", value=a.get('claves', ''),
                                   key=f"cl{i}", max_chars=a['num'])
                st.session_state.areas_examen[i]['claves'] = cl.upper()
                ia.append({
                    'nombre': a['nombre'],
                    'num': a['num'],
                    'claves': list(cl.upper())
                })
                tc_.extend(list(cl.upper()))
                tp += a['num']
                if len(st.session_state.areas_examen) > 1:
                    if st.button("🗑️", key=f"d{i}"):
                        st.session_state.areas_examen.pop(i)
                        st.rerun()

        if ia:
            st.info(f"📊 {tp} preguntas en {len(ia)} áreas")

        st.markdown("---")
        st.markdown("**2️⃣ Alumno:**")
        de = st.text_input("DNI:", key="de")
        if de:
            ae = BaseDatos.buscar_por_dni(de)
            if ae:
                st.success(f"👤 {ae.get('Nombre', '')}")

        st.markdown("**3️⃣ Respuestas:**")
        met = st.radio("Método:", ["✏️ Manual", "📸 Cámara"],
                       horizontal=True, key="met")
        ra = []
        if met == "✏️ Manual":
            for i, a in enumerate(ia):
                r = st.text_input(f"{a['nombre']} ({a['num']}):",
                                  key=f"r{i}", max_chars=a['num'])
                ra.extend(list(r.upper()))
        else:
            ac = st.checkbox("📷 Activar cámara", key="chce")
            if ac:
                fe = st.camera_input("📷", key="ce")
                if fe:
                    det = procesar_examen(fe.getvalue(), tp)
                    if det:
                        ra = det
                        st.success(f"✅ {len(det)} detectadas")
                    else:
                        st.warning("⚠️ No detectadas, use manual")

        st.markdown("---")
        if st.button("📊 CALIFICAR", type="primary",
                     use_container_width=True, key="cal"):
            if tc_ and ra:
                ad = BaseDatos.buscar_por_dni(de) if de else None
                nm = ad.get('Nombre', '') if ad else "Sin nombre"
                res = {
                    'fecha': hora_peru().strftime('%d/%m/%Y %H:%M'),
                    'dni': de,
                    'nombre': nm,
                    'areas': [],
                    'promedio_general': 0
                }
                idx = 0
                sn = 0
                mw = (f"📝 *RESULTADOS*\n🏫 YACHAY\n👤 {nm}\n"
                      f"📅 {hora_peru().strftime('%d/%m/%Y')}\n\n")
                for a in ia:
                    n = a['num']
                    ck = a['claves'][:n]
                    rk = ra[idx:idx + n]
                    ok = sum(1 for j in range(min(len(ck), len(rk)))
                             if ck[j] == rk[j])
                    nota = round((ok / n) * 20, 1) if n else 0
                    lt = ("AD" if nota >= 18 else "A" if nota >= 14
                          else "B" if nota >= 11 else "C")
                    detalle = []
                    for j in range(n):
                        cj = ck[j] if j < len(ck) else '?'
                        rj = rk[j] if j < len(rk) else '?'
                        ok_j = (j < len(ck) and j < len(rk) and ck[j] == rk[j])
                        detalle.append({
                            'p': idx + j + 1,
                            'c': cj,
                            'r': rj,
                            'ok': ok_j
                        })
                    res['areas'].append({
                        'nombre': a['nombre'],
                        'correctas': ok,
                        'total': n,
                        'nota': nota,
                        'letra': lt,
                        'detalle': detalle
                    })
                    sn += nota
                    mw += f"📚 *{a['nombre']}:* {nota}/20 ({lt})\n"
                    idx += n

                pm = round(sn / len(ia), 1) if ia else 0
                lp = ("AD" if pm >= 18 else "A" if pm >= 14
                      else "B" if pm >= 11 else "C")
                res['promedio_general'] = pm
                mw += f"\n📊 *PROMEDIO: {pm}/20 ({lp})*"

                BaseDatos.guardar_resultados_examen(res)

                st.markdown("### 📊 Resultados")
                cols = st.columns(len(ia) + 1)
                for i, ar in enumerate(res['areas']):
                    with cols[i]:
                        st.metric(f"📚 {ar['nombre']}",
                                  f"{ar['nota']}/20", f"{ar['letra']}")
                with cols[-1]:
                    st.metric("📊 PROMEDIO", f"{pm}/20", lp)

                for ar in res['areas']:
                    with st.expander(f"📋 {ar['nombre']}"):
                        st.dataframe(pd.DataFrame([
                            {'#': d['p'], 'Clave': d['c'], 'Resp': d['r'],
                             '': ('✅' if d['ok'] else '❌')}
                            for d in ar['detalle']
                        ]), use_container_width=True, hide_index=True)

                if ad:
                    cel = ad.get('Celular_Apoderado', '')
                    if cel and cel.strip():
                        link = generar_link_whatsapp(cel, mw)
                        st.markdown(
                            f'<a href="{link}" target="_blank" class="wa-btn">'
                            f'📱 Enviar → {cel}</a>',
                            unsafe_allow_html=True
                        )
                st.balloons()
            else:
                st.error("⚠️ Configure claves y respuestas")

    with tr:
        st.subheader("🏆 Ranking")
        rs = BaseDatos.cargar_resultados_examen()
        if rs:
            df = pd.DataFrame([{
                'Fecha': r.get('fecha', ''),
                'Nombre': r.get('nombre', ''),
                'DNI': r.get('dni', ''),
                'Promedio': r.get('promedio_general', 0),
                'Áreas': ', '.join([
                    f"{a['nombre']}:{a['nota']}"
                    for a in r.get('areas', [])
                ])
            } for r in rs])
            df = df.sort_values('Promedio', ascending=False).reset_index(drop=True)
            df.insert(0, '#', range(1, len(df) + 1))
            st.dataframe(df, use_container_width=True, hide_index=True)

            if len(df) >= 1:
                cols = st.columns(min(3, len(df)))
                medallas = ["🥇", "🥈", "🥉"]
                estilos = ["ranking-gold", "ranking-silver", "ranking-bronze"]
                for i in range(min(3, len(df))):
                    with cols[i]:
                        r = df.iloc[i]
                        st.markdown(
                            f'<div class="{estilos[i]}">'
                            f'{medallas[i]} {r["Nombre"]}<br>'
                            f'{r["Promedio"]}/20</div>',
                            unsafe_allow_html=True
                        )

            st.markdown("---")
            if st.button("📥 GENERAR RANKING PDF", type="primary",
                         use_container_width=True, key="grpdf"):
                pdf = generar_ranking_pdf(rs, config['anio'])
                st.download_button("⬇️ PDF", pdf,
                                   f"Ranking_{config['anio']}.pdf",
                                   "application/pdf", key="drpdf")

            st.markdown("---")
            st.markdown("### 📱 Enviar Individual")
            for _, row in df.iterrows():
                al = BaseDatos.buscar_por_dni(row['DNI']) if row['DNI'] else None
                if al:
                    cel = al.get('Celular_Apoderado', '')
                    if cel and cel.strip():
                        ro = next(
                            (r for r in rs if r.get('dni') == row['DNI']), None
                        )
                        if ro:
                            msg = (f"📝 *RANKING YACHAY*\n"
                                   f"👤 {row['Nombre']}\n"
                                   f"🏆 Puesto: {row['#']}°/{len(df)}\n")
                            for a in ro.get('areas', []):
                                msg += f"📚 {a['nombre']}: {a['nota']}/20\n"
                            msg += f"\n📊 *PROMEDIO: {row['Promedio']}/20*"
                            link = generar_link_whatsapp(cel, msg)
                            st.markdown(
                                f'<a href="{link}" target="_blank" class="wa-btn">'
                                f'📱 #{row["#"]} {row["Nombre"]} — '
                                f'{row["Promedio"]}/20</a>',
                                unsafe_allow_html=True
                            )

            st.markdown("---")
            if st.button("🗑️ Limpiar Ranking", key="lr"):
                if Path(ARCHIVO_RESULTADOS).exists():
                    os.remove(ARCHIVO_RESULTADOS)
                st.success("✅")
                st.rerun()
        else:
            st.info("📝 Corrige exámenes para ver ranking.")


# ================================================================
# TAB: BASE DE DATOS
# ================================================================

def tab_base_datos():
    st.header("📊 Base de Datos")
    df = BaseDatos.cargar_matricula()
    df_doc = BaseDatos.cargar_docentes()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📚 Alumnos", len(df) if not df.empty else 0)
    with c2:
        st.metric("👨‍🏫 Docentes", len(df_doc) if not df_doc.empty else 0)
    with c3:
        st.metric("🎓 Grados",
                   df['Grado'].nunique() if not df.empty and 'Grado' in df.columns
                   else 0)
    with c4:
        st.metric("📱 Con Celular",
                   df['Celular_Apoderado'].notna().sum()
                   if not df.empty and 'Celular_Apoderado' in df.columns else 0)

    tab_al, tab_dc = st.tabs(["📚 Alumnos", "👨‍🏫 Docentes"])

    with tab_al:
        if not df.empty:
            c1, c2 = st.columns(2)
            with c1:
                opts = ['Todos'] + (
                    sorted(df['Grado'].dropna().unique().tolist())
                    if 'Grado' in df.columns else []
                )
                fg = st.selectbox("Filtrar:", opts, key="fbd")
            with c2:
                bq = st.text_input("🔍", key="bbd")
            d = df.copy()
            if fg != 'Todos' and 'Grado' in d.columns:
                d = d[d['Grado'] == fg]
            if bq:
                d = d[d.apply(lambda r: bq.lower() in str(r).lower(), axis=1)]
            if 'Nombre' in d.columns:
                d = d.sort_values('Nombre')
            st.dataframe(d, use_container_width=True, hide_index=True, height=500)
            c1, c2 = st.columns(2)
            with c1:
                st.download_button("⬇️ CSV",
                                   d.to_csv(index=False).encode('utf-8'),
                                   "alumnos.csv", "text/csv", key="dcsv")
            with c2:
                buf = io.BytesIO()
                d.to_excel(buf, index=False, engine='openpyxl')
                buf.seek(0)
                st.download_button("⬇️ Excel", buf, "alumnos.xlsx", key="dxlsx")
        else:
            st.info("📝 Sin alumnos.")

    with tab_dc:
        if not df_doc.empty:
            if 'Nombre' in df_doc.columns:
                df_doc = df_doc.sort_values('Nombre')
            st.dataframe(df_doc, use_container_width=True, hide_index=True)
            buf2 = io.BytesIO()
            df_doc.to_excel(buf2, index=False, engine='openpyxl')
            buf2.seek(0)
            st.download_button("⬇️ Excel Docentes", buf2,
                               "docentes_export.xlsx", key="dxlsxd")
        else:
            st.info("📝 Sin docentes.")


# ================================================================
# VISTA DOCENTE (Registro Auxiliar + Asistencia + Calificación)
# ================================================================

def vista_docente(config):
    info = st.session_state.docente_info
    grado = info['grado']
    st.markdown(f"### 👨‍🏫 {info['label']}")

    tabs = st.tabs([
        "📝 Registro Auxiliar",
        "📋 Registro Asistencia",
        "📝 Calificación YACHAY"
    ])

    with tabs[0]:
        st.subheader("📝 Registro Auxiliar de Evaluación")
        st.caption("Cursos × 4 Competencias × 3 Desempeños")
        sec = st.selectbox("Sección:", ["Todas"] + SECCIONES, key="ds")
        bim = st.selectbox("Bimestre:", list(BIMESTRES.keys()), key="dbim")
        st.markdown("**Cursos:**")
        c1, c2, c3 = st.columns(3)
        with c1:
            dc1 = st.text_input("Curso 1:", "Matemática", key="dc1")
        with c2:
            dc2 = st.text_input("Curso 2:", "Comunicación", key="dc2")
        with c3:
            dc3 = st.text_input("Curso 3:", "Ciencia y Tec.", key="dc3")
        cursos_doc = [c for c in [dc1, dc2, dc3] if c.strip()]
        dg = BaseDatos.obtener_estudiantes_grado(grado, sec)
        st.info(f"📊 {len(dg)} estudiantes (alfabético)")
        if not dg.empty:
            st.dataframe(dg[['Nombre', 'DNI', 'Grado', 'Seccion']],
                         use_container_width=True, hide_index=True)
        if st.button("📥 Descargar Registro Auxiliar PDF", type="primary",
                     use_container_width=True, key="ddra"):
            if not dg.empty:
                lg = grado if grado != "ALL_SECUNDARIA" else "Secundaria"
                sl = sec if sec != "Todas" else "Todas"
                pdf = generar_registro_auxiliar_pdf(
                    lg, sl, config['anio'], bim, dg, cursos_doc
                )
                st.download_button("⬇️ PDF", pdf,
                                   f"RegAux_{lg}_{bim}.pdf",
                                   "application/pdf", key="ddra2")

    with tabs[1]:
        st.subheader("📋 Registro de Asistencia")
        sec2 = st.selectbox("Sección:", ["Todas"] + SECCIONES, key="ds2")
        meses_opts = list(MESES_ESCOLARES.items())
        meses_sel = st.multiselect(
            "Meses:",
            [f"{v} ({k})" for k, v in meses_opts],
            default=[f"{v} ({k})" for k, v in meses_opts[:1]],
            key="dmsel"
        )
        meses_nums = [int(m.split('(')[1].replace(')', '')) for m in meses_sel]
        dg2 = BaseDatos.obtener_estudiantes_grado(grado, sec2)
        st.info(f"📊 {len(dg2)} estudiantes")
        if st.button("📥 Descargar Registro Asistencia PDF", type="primary",
                     use_container_width=True, key="ddas"):
            if not dg2.empty and meses_nums:
                lg = grado if grado != "ALL_SECUNDARIA" else "Secundaria"
                sl = sec2 if sec2 != "Todas" else "Todas"
                pdf = generar_registro_asistencia_pdf(
                    lg, sl, config['anio'], dg2, meses_nums
                )
                st.download_button("⬇️ PDF", pdf,
                                   f"RegAsist_{lg}.pdf",
                                   "application/pdf", key="ddas2")

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
