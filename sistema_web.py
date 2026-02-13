# ================================================================
# SISTEMA YACHAY PRO v4.0 — VERSIÓN DEFINITIVA FINAL COMPLETA
# ================================================================
# Módulos: Matrícula (Alumnos + Docentes), Documentos PDF (6 tipos),
#          Carnets (individual/lote PDF 8 por hoja fotocheck),
#          Asistencia QR (Alumnos + Docentes),
#          Sistema de Calificación YACHAY (ZipGrade) — RANKING POR DOCENTE,
#          Registro Auxiliar (3 Cursos × 4 Competencias × 3 Desempeños),
#          Registro Asistencia (sin sáb/dom, sin feriados + pie feriados),
#          Gestión de Usuarios dinámicos desde Admin,
#          Protección: solo Admin puede borrar datos,
#          Links SIAGIE y Google Institucional
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
import hashlib
from datetime import datetime, timedelta, timezone, date
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Google Sheets sync
try:
    from google_sync import GoogleSync, get_google_sync
    GOOGLE_SYNC_DISPONIBLE = True
except ImportError:
    GOOGLE_SYNC_DISPONIBLE = False

st.set_page_config(page_title="SISTEMA YACHAY PRO", page_icon="🎓", layout="wide")

# ================================================================
# INICIALIZAR GOOGLE SHEETS
# ================================================================
def _gs():
    """Obtener instancia de Google Sync (o None si no está disponible)"""
    if not GOOGLE_SYNC_DISPONIBLE:
        return None
    try:
        gs = get_google_sync()
        return gs if gs.conectado else None
    except Exception:
        return None

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
    dias = []
    _, ndays = calendar.monthrange(anio, mes)
    for d in range(1, ndays + 1):
        dt = date(anio, mes, d)
        if dt.weekday() < 5 and (mes, d) not in FERIADOS_PERU:
            dias.append(d)
    return dias


def feriados_del_mes(mes):
    resultado = []
    for (m, d), nombre in FERIADOS_PERU.items():
        if m == mes:
            resultado.append(f"{d} - {nombre}")
    return resultado


# ================================================================
# LINKS INSTITUCIONALES
# ================================================================

LINK_SIAGIE = "https://sistemas10.minedu.gob.pe/siagie3/"
LINK_GOOGLE = ("https://accounts.google.com/v3/signin/identifier?"
               "continue=https%3A%2F%2Fmail.google.com%2Fmail%2F"
               "&hd=ieyachay.org&osid=1&sacu=1&service=mail"
               "&flowName=GlifWebSignIn&flowEntry=AddSession"
               "&dsh=S386112432%3A1698624419248117&theme=glif")

# ================================================================
# SISTEMA DE USUARIOS — DINÁMICO (archivo JSON)
# ================================================================

ARCHIVO_USUARIOS = "usuarios.json"

USUARIOS_DEFAULT = {
    "administrador": {
        "password": "306020",
        "rol": "admin",
        "label": "Administrador",
        "docente_info": None
    },
    "directora": {
        "password": "directora2026",
        "rol": "directivo",
        "label": "Directora",
        "docente_info": None
    },
    "leandro": {
        "password": "leandro2026",
        "rol": "directivo",
        "label": "Promotor — Leandro",
        "docente_info": None
    },
    "deyanira": {
        "password": "deyanira",
        "rol": "directivo",
        "label": "Deyanira",
        "docente_info": None
    },
    "auxiliar": {
        "password": "123456789",
        "rol": "auxiliar",
        "label": "Auxiliar",
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


def cargar_usuarios():
    # Intentar cargar de Google Sheets primero
    gs = _gs()
    usuarios_final = USUARIOS_DEFAULT.copy()
    
    if gs:
        usuarios_gs = gs.leer_usuarios()
        if usuarios_gs:
            # Agregar usuarios creados dinámicamente (que no están en defaults)
            for uname, datos in usuarios_gs.items():
                if uname not in usuarios_final:
                    # Reconstruir docente_info si falta
                    if 'docente_info' not in datos and datos.get('grado'):
                        datos['docente_info'] = {
                            'label': datos.get('grado', ''),
                            'grado': datos.get('grado', ''),
                            'nivel': datos.get('nivel', ''),
                        }
                    usuarios_final[uname] = datos
                else:
                    # Para usuarios built-in: SIEMPRE mantener password y rol del default
                    # pero actualizar docente_info si GS tiene mejor data
                    if usuarios_gs[uname].get('docente_info'):
                        usuarios_final[uname]['docente_info'] = usuarios_gs[uname]['docente_info']
    
    # Fallback: cargar usuarios extra de archivo local
    if Path(ARCHIVO_USUARIOS).exists():
        try:
            with open(ARCHIVO_USUARIOS, 'r', encoding='utf-8') as f:
                usuarios_local = json.load(f)
            for uname, datos in usuarios_local.items():
                if uname not in usuarios_final:
                    usuarios_final[uname] = datos
        except Exception:
            pass
    
    guardar_usuarios_local(usuarios_final)
    return usuarios_final


def guardar_usuarios_local(usuarios):
    """Solo guarda localmente (sin Google Sheets)"""
    with open(ARCHIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)


def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)
    # Sincronizar con Google Sheets
    gs = _gs()
    if gs:
        gs.sync_usuarios_completo(usuarios)


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
        "GRUPO AB — CEPRE UNSAAC", "GRUPO CD — CEPRE UNSAAC",
        "Ciclo Verano", "Ciclo Regular", "Ciclo Intensivo",
        "Reforzamiento Primaria"
    ]
}

# Áreas CEPRE UNSAAC por grupo
AREAS_CEPRE_UNSAAC = {
    'GRUPO AB': [
        'Aritmética', 'Álgebra', 'Geometría', 'Trigonometría',
        'Física', 'Química', 'Biología',
        'Competencia Comunicativa',
    ],
    'GRUPO CD': [
        'Aritmética', 'Álgebra', 'Competencia Comunicativa',
        'Historia', 'Geografía', 'Educación Cívica',
        'Economía', 'Filosofía y Lógica',
    ],
}

SECCIONES = ["Única", "A", "B"]

TODOS_LOS_GRADOS = []
for nk, gl in NIVELES_GRADOS.items():
    for gi in gl:
        TODOS_LOS_GRADOS.append(gi)

NIVELES_LIST = list(NIVELES_GRADOS.keys())
GRADOS_OPCIONES = TODOS_LOS_GRADOS.copy()

MESES_ESCOLARES = {
    1: "Enero", 2: "Febrero",
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
        'modulo_activo': None,
        'cola_asistencia': [],
        'wa_enviados': set(),
        'evaluaciones_guardadas': {},
        'ultimo_pdf_incidencia': None,
        'ultimo_codigo_incidencia': '',
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ================================================================
# ESTILOS CSS + ANIMACIONES + SONIDO
# ================================================================

st.markdown("""
<style>
/* === ANIMACIÓN DE ENTRADA === */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes slideIn {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}

/* === HEADER PRINCIPAL === */
.main-header {
    text-align: center; padding: 2rem;
    background: linear-gradient(135deg, #001e7c 0%, #0052cc 50%, #0066ff 100%);
    color: white; border-radius: 15px; margin-bottom: 2rem;
    box-shadow: 0 8px 25px rgba(0,30,124,0.35);
    animation: fadeInUp 0.6s ease-out;
}

/* === TABS ANIMADOS === */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px 10px 0 0;
    padding: 10px 20px;
    transition: all 0.3s ease;
    font-weight: 600;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(26,86,219,0.1);
    transform: translateY(-2px);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1a56db, #0052cc) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(26,86,219,0.3);
}

/* === BOTONES CON EFECTO === */
.stButton > button {
    transition: all 0.3s ease !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* === CARDS DE ESTADÍSTICAS === */
.stat-card {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    border-radius: 12px; padding: 1.2rem;
    border-left: 4px solid #1a56db;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    animation: slideIn 0.5s ease-out;
    transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-3px); }
.stat-card h3 { margin: 0; color: #1a56db; font-size: 2rem; }
.stat-card p { margin: 0; color: #64748b; font-size: 0.9rem; }

/* === ASISTENCIA REGISTRADA === */
.asist-ok {
    background: linear-gradient(135deg, #dcfce7, #bbf7d0);
    border-radius: 10px; padding: 12px 16px;
    border-left: 4px solid #16a34a;
    animation: fadeInUp 0.4s ease-out;
    margin: 4px 0;
}
.asist-salida {
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    border-radius: 10px; padding: 12px 16px;
    border-left: 4px solid #f59e0b;
    animation: fadeInUp 0.4s ease-out;
    margin: 4px 0;
}

/* === GOOGLE SHEETS STATUS === */
.gs-connected {
    background: linear-gradient(135deg, #dcfce7, #bbf7d0);
    border-radius: 8px; padding: 8px 12px;
    text-align: center; font-weight: 600;
    color: #166534; font-size: 0.85rem;
    animation: pulse 2s infinite;
}
.gs-offline {
    background: #fef3c7; border-radius: 8px;
    padding: 8px 12px; text-align: center;
    color: #92400e; font-size: 0.85rem;
}

/* === RANKING CON ANIMACIÓN === */
.ranking-gold {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    background-size: 200% auto;
    animation: shimmer 3s linear infinite;
    color: #000; padding: 14px; border-radius: 10px;
    font-weight: bold; text-align: center; margin: 5px 0;
    box-shadow: 0 4px 15px rgba(255,215,0,0.4);
}
.ranking-silver {
    background: linear-gradient(135deg, #C0C0C0, #E8E8E8, #C0C0C0);
    background-size: 200% auto;
    animation: shimmer 3s linear infinite;
    color: #000; padding: 14px; border-radius: 10px;
    font-weight: bold; text-align: center; margin: 5px 0;
    box-shadow: 0 4px 12px rgba(192,192,192,0.4);
}
.ranking-bronze {
    background: linear-gradient(135deg, #CD7F32, #E8A849, #CD7F32);
    background-size: 200% auto;
    animation: shimmer 3s linear infinite;
    color: #fff; padding: 14px; border-radius: 10px;
    font-weight: bold; text-align: center; margin: 5px 0;
    box-shadow: 0 4px 12px rgba(205,127,50,0.4);
}

/* === WHATSAPP / LINKS === */
.wa-btn {
    background: linear-gradient(135deg, #25D366, #128C7E); color: white !important;
    padding: 10px 20px; border: none; border-radius: 10px;
    font-size: 15px; width: 100%; text-decoration: none;
    display: block; text-align: center; margin: 4px 0;
    transition: all 0.3s; font-weight: 600;
}
.wa-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(37,211,102,0.4); }
.link-btn {
    background: linear-gradient(135deg, #4285F4, #356AC3); color: white !important;
    padding: 8px 16px; border: none; border-radius: 10px;
    font-size: 14px; width: 100%; text-decoration: none;
    display: block; text-align: center; margin: 4px 0;
    transition: all 0.3s;
}
.link-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(66,133,244,0.4); }
.siagie-btn {
    background: linear-gradient(135deg, #E91E63, #C2185B); color: white !important;
    padding: 8px 16px; border: none; border-radius: 10px;
    font-size: 14px; width: 100%; text-decoration: none;
    display: block; text-align: center; margin: 4px 0;
    transition: all 0.3s;
}
.siagie-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(233,30,99,0.4); }

/* === EXPANDER MEJORADO === */
.streamlit-expanderHeader {
    font-weight: 600 !important;
    border-radius: 8px !important;
}

/* === SIDEBAR === */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
}

/* === SUCCESS/ERROR MEJORADOS === */
.stSuccess { animation: fadeInUp 0.4s ease-out; border-radius: 10px !important; }
.stError { animation: fadeInUp 0.4s ease-out; border-radius: 10px !important; }
.stInfo { animation: fadeInUp 0.4s ease-out; border-radius: 10px !important; }

/* === DASHBOARD GRID === */
.stButton > button[kind="secondary"] {
    min-height: 100px !important;
    font-size: 1.1rem !important;
    border-radius: 16px !important;
    border: 2px solid #e2e8f0 !important;
    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%) !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
}
.stButton > button[kind="secondary"]:hover {
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(26,86,219,0.15) !important;
    border-color: #1a56db !important;
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important;
}

/* === NÚMERO ANIMADO === */
@keyframes countUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.stMetric { animation: countUp 0.5s ease-out; }

/* === INPUTS MEJORADOS === */
.stTextInput > div > div > input { border-radius: 10px !important; transition: all 0.3s; }
.stTextInput > div > div > input:focus { box-shadow: 0 0 0 3px rgba(26,86,219,0.2) !important; border-color: #1a56db !important; }
.stSelectbox > div > div { border-radius: 10px !important; }

/* === DATAFRAME === */
.stDataFrame { border-radius: 12px !important; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }

/* === SEMÁFORO COLORES === */
.semaforo-ad { color: #16a34a; font-weight: bold; }
.semaforo-a { color: #2563eb; font-weight: bold; }
.semaforo-b { color: #f59e0b; font-weight: bold; }
.semaforo-c { color: #dc2626; font-weight: bold; }

/* === LOADING SPINNER === */
.stSpinner > div { border-color: #1a56db transparent transparent transparent !important; }
</style>
""", unsafe_allow_html=True)


def reproducir_sonido_asistencia():
    """Genera un beep/sonido cuando se registra asistencia"""
    st.markdown("""
    <audio autoplay>
        <source src="data:audio/wav;base64,UklGRl4FAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YToFAACAgICAgICAgICAkJigoKiouMDI0Njg6PD4+Pj48PDo4NjQyMC4sKignp6WjoaAgICAgICAgICAgJCYoKCorLjAyNDY4Ojw+Pj4+PDw6ODY0MjAuLCooJ6elo6GgICAgICAgICA" type="audio/wav">
    </audio>
    """, unsafe_allow_html=True)


def reproducir_beep_exitoso():
    """Sonido de éxito para escaneos y registros"""
    # Genera un tono de 800Hz corto usando JavaScript AudioContext
    st.markdown("""
    <script>
    (function() {
        try {
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            var osc = ctx.createOscillator();
            var gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.frequency.value = 800;
            osc.type = 'sine';
            gain.gain.setValueAtTime(0.3, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
            osc.start(ctx.currentTime);
            osc.stop(ctx.currentTime + 0.3);
        } catch(e) {}
    })();
    </script>
    """, unsafe_allow_html=True)


def reproducir_beep_error():
    """Sonido de error"""
    st.markdown("""
    <script>
    (function() {
        try {
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            var osc = ctx.createOscillator();
            var gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.frequency.value = 300;
            osc.type = 'square';
            gain.gain.setValueAtTime(0.2, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
            osc.start(ctx.currentTime);
            osc.stop(ctx.currentTime + 0.5);
        } catch(e) {}
    })();
    </script>
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
            ruta = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
                    else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
            if Path(ruta).exists():
                return ImageFont.truetype(ruta, int(tamanio))
            return ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()


# ================================================================
# PERMISOS — SOLO ADMIN PUEDE BORRAR
# ================================================================

def puede_borrar():
    """Solo el admin puede borrar datos del sistema"""
    return st.session_state.rol == "admin"


# ================================================================
# BASE DE DATOS — ALUMNOS Y DOCENTES
# ================================================================

class BaseDatos:

    @staticmethod
    def cargar_matricula():
        # Intentar Google Sheets primero
        gs = _gs()
        if gs:
            try:
                df_gs = gs.leer_matricula()
                if not df_gs.empty:
                    col_map = {'nombre': 'Nombre', 'dni': 'DNI', 'nivel': 'Nivel',
                               'grado': 'Grado', 'seccion': 'Seccion',
                               'apoderado': 'Apoderado', 'dni_apoderado': 'DNI_Apoderado',
                               'celular_apoderado': 'Celular_Apoderado'}
                    df_gs = df_gs.rename(columns=col_map)
                    # Asegurar que todos los valores sean string
                    for col in df_gs.columns:
                        df_gs[col] = df_gs[col].astype(str).replace('nan', '').replace('None', '')
                    return df_gs
            except Exception:
                pass
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
        try:
            df.to_excel(ARCHIVO_MATRICULA, index=False, engine='openpyxl')
        except Exception:
            # Fallback: guardar como CSV si openpyxl falla
            df.to_csv(ARCHIVO_MATRICULA.replace('.xlsx', '.csv'), index=False)
        # Sincronizar con Google Sheets
        gs = _gs()
        if gs:
            try:
                col_map = {'Nombre': 'nombre', 'DNI': 'dni', 'Nivel': 'nivel',
                           'Grado': 'grado', 'Seccion': 'seccion',
                           'Apoderado': 'apoderado', 'DNI_Apoderado': 'dni_apoderado',
                           'Celular_Apoderado': 'celular_apoderado'}
                df_gs = df.rename(columns=col_map).copy()
                if 'fecha_matricula' not in df_gs.columns:
                    df_gs['fecha_matricula'] = fecha_peru_str()
                gs.sync_matricula_completa(df_gs)
            except Exception:
                pass

    @staticmethod
    def registrar_estudiante(datos):
        df = BaseDatos.cargar_matricula()
        if not df.empty and 'DNI' in df.columns and datos['DNI'] in df['DNI'].values:
            idx = df[df['DNI'] == datos['DNI']].index[0]
            for k, v in datos.items():
                df.at[idx, k] = v
        else:
            df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)
        BaseDatos.guardar_matricula(df)

    @staticmethod
    def buscar_por_dni(dni):
        dni_str = str(dni).strip()
        df = BaseDatos.cargar_matricula()
        if not df.empty and 'DNI' in df.columns:
            df['DNI'] = df['DNI'].astype(str).str.strip()
            res = df[df['DNI'] == dni_str]
            if not res.empty:
                r = res.iloc[0].to_dict()
                r['_tipo'] = 'alumno'
                return r
        df_d = BaseDatos.cargar_docentes()
        if not df_d.empty and 'DNI' in df_d.columns:
            df_d['DNI'] = df_d['DNI'].astype(str).str.strip()
            res2 = df_d[df_d['DNI'] == dni_str]
            if not res2.empty:
                r = res2.iloc[0].to_dict()
                r['_tipo'] = 'docente'
                return r
        try:
            if Path(ARCHIVO_BD).exists():
                df2 = pd.read_excel(ARCHIVO_BD, dtype=str, engine='openpyxl')
                df2.columns = df2.columns.str.strip().str.title()
                if 'Dni' in df2.columns:
                    df2['Dni'] = df2['Dni'].astype(str).str.strip()
                    res3 = df2[df2['Dni'] == dni_str]
                    if not res3.empty:
                        row = res3.iloc[0].to_dict()
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
    def cargar_docentes():
        # Intentar Google Sheets primero
        gs = _gs()
        if gs:
            try:
                df_gs = gs.leer_docentes()
                if not df_gs.empty:
                    col_map = {'nombre': 'Nombre', 'dni': 'DNI', 'cargo': 'Cargo',
                               'especialidad': 'Especialidad', 'celular': 'Celular',
                               'grado_asignado': 'Grado_Asignado'}
                    df_gs = df_gs.rename(columns=col_map)
                    for col in df_gs.columns:
                        df_gs[col] = df_gs[col].astype(str).replace('nan', '').replace('None', '')
                    return df_gs
            except Exception:
                pass
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
        try:
            df.to_excel(ARCHIVO_DOCENTES, index=False, engine='openpyxl')
        except Exception:
            df.to_csv(ARCHIVO_DOCENTES.replace('.xlsx', '.csv'), index=False)
        gs = _gs()
        if gs:
            try:
                col_map = {'Nombre': 'nombre', 'DNI': 'dni', 'Cargo': 'cargo',
                           'Especialidad': 'especialidad', 'Celular': 'celular',
                           'Grado_Asignado': 'grado_asignado'}
                df_gs = df.rename(columns=col_map).copy()
                if 'fecha_registro' not in df_gs.columns:
                    df_gs['fecha_registro'] = fecha_peru_str()
                gs.sync_docentes_completo(df_gs)
            except Exception:
                pass

    @staticmethod
    def registrar_docente(datos):
        df = BaseDatos.cargar_docentes()
        if not df.empty and 'DNI' in df.columns and datos['DNI'] in df['DNI'].values:
            idx = df[df['DNI'] == datos['DNI']].index[0]
            for k, v in datos.items():
                df.at[idx, k] = v
        else:
            df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)
        BaseDatos.guardar_docentes(df)

    @staticmethod
    def eliminar_docente(dni):
        df = BaseDatos.cargar_docentes()
        df['DNI'] = df['DNI'].astype(str).str.strip()
        df = df[df['DNI'] != str(dni).strip()]
        BaseDatos.guardar_docentes(df)

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
                'nombre': nombre, 'entrada': '', 'salida': '',
                'es_docente': es_docente
            }
        asistencias[fecha_hoy][dni][tipo] = hora
        asistencias[fecha_hoy][dni]['nombre'] = nombre
        with open(ARCHIVO_ASISTENCIAS, 'w', encoding='utf-8') as f:
            json.dump(asistencias, f, indent=2, ensure_ascii=False)
        # Sincronizar con Google Sheets
        gs = _gs()
        if gs:
            try:
                grado = ''
                nivel = ''
                df_m = BaseDatos.cargar_matricula()
                if not df_m.empty and 'DNI' in df_m.columns:
                    est = df_m[df_m['DNI'].astype(str).str.strip() == str(dni).strip()]
                    if not est.empty:
                        grado = est.iloc[0].get('Grado', '')
                        nivel = est.iloc[0].get('Nivel', '')
                reg = asistencias[fecha_hoy][dni]
                gs.guardar_asistencia({
                    'fecha': fecha_hoy,
                    'dni': str(dni),
                    'nombre': nombre,
                    'tipo_persona': 'docente' if es_docente else 'alumno',
                    'hora_entrada': reg.get('entrada', ''),
                    'hora_salida': reg.get('salida', ''),
                    'grado': grado,
                    'nivel': nivel,
                })
            except Exception:
                pass

    @staticmethod
    def obtener_asistencias_hoy():
        fecha_hoy = fecha_peru_str()
        if Path(ARCHIVO_ASISTENCIAS).exists():
            with open(ARCHIVO_ASISTENCIAS, 'r', encoding='utf-8') as f:
                return json.load(f).get(fecha_hoy, {})
        return {}

    @staticmethod
    def borrar_asistencias_hoy():
        fecha_hoy = fecha_peru_str()
        if Path(ARCHIVO_ASISTENCIAS).exists():
            with open(ARCHIVO_ASISTENCIAS, 'r', encoding='utf-8') as f:
                a = json.load(f)
            if fecha_hoy in a:
                del a[fecha_hoy]
            with open(ARCHIVO_ASISTENCIAS, 'w', encoding='utf-8') as f:
                json.dump(a, f, indent=2, ensure_ascii=False)

    @staticmethod
    def obtener_estadisticas():
        df = BaseDatos.cargar_matricula()
        df_d = BaseDatos.cargar_docentes()
        return {
            'total_alumnos': len(df) if not df.empty else 0,
            'total_docentes': len(df_d) if not df_d.empty else 0,
            'grados': df['Grado'].nunique() if not df.empty and 'Grado' in df.columns else 0
        }

    # ---- RESULTADOS POR DOCENTE (separados por usuario) ----

    @staticmethod
    def guardar_resultados_examen(resultado, usuario_docente):
        """Guarda resultado asociado al usuario docente"""
        datos = {}
        if Path(ARCHIVO_RESULTADOS).exists():
            try:
                with open(ARCHIVO_RESULTADOS, 'r', encoding='utf-8') as f:
                    raw = json.load(f)
                if isinstance(raw, list):
                    datos = {"migrado": raw}
                elif isinstance(raw, dict):
                    datos = raw
                else:
                    datos = {}
            except Exception:
                datos = {}
        if usuario_docente not in datos:
            datos[usuario_docente] = []
        datos[usuario_docente].append(resultado)
        with open(ARCHIVO_RESULTADOS, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        # Sincronizar con Google Sheets
        gs = _gs()
        if gs:
            try:
                import uuid
                eval_id = str(uuid.uuid4())[:8]
                titulo = resultado.get('titulo', 'Evaluación')
                fecha = resultado.get('fecha', fecha_peru_str())
                grado = resultado.get('grado', '')
                areas_info = resultado.get('areas', [])
                alumnos = resultado.get('alumnos', [])
                gs.guardar_resultados_examen(
                    eval_id, titulo, fecha, usuario_docente,
                    grado, areas_info, alumnos
                )
            except Exception:
                pass

    @staticmethod
    def cargar_resultados_examen(usuario_docente):
        """Carga solo los resultados del docente específico"""
        if Path(ARCHIVO_RESULTADOS).exists():
            try:
                with open(ARCHIVO_RESULTADOS, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                # Si es formato viejo (lista), retornar la lista completa
                if isinstance(datos, list):
                    return datos
                elif isinstance(datos, dict):
                    return datos.get(usuario_docente, [])
            except Exception:
                pass
        return []

    @staticmethod
    def limpiar_resultados_examen(usuario_docente):
        """Limpia solo los resultados del docente"""
        if Path(ARCHIVO_RESULTADOS).exists():
            try:
                with open(ARCHIVO_RESULTADOS, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                if isinstance(datos, list):
                    # Formato viejo, limpiar todo
                    datos = {}
                elif isinstance(datos, dict) and usuario_docente in datos:
                    datos[usuario_docente] = []
                with open(ARCHIVO_RESULTADOS, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=2, ensure_ascii=False)
            except Exception:
                pass

    @staticmethod
    def cargar_todos_resultados():
        """Carga todos los resultados (para admin)"""
        if Path(ARCHIVO_RESULTADOS).exists():
            try:
                with open(ARCHIVO_RESULTADOS, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                todos = []
                if isinstance(datos, list):
                    # Formato viejo
                    for r in datos:
                        r['_docente'] = 'migrado'
                        todos.append(r)
                elif isinstance(datos, dict):
                    for usr, lista in datos.items():
                        if isinstance(lista, list):
                            for r in lista:
                                r['_docente'] = usr
                                todos.append(r)
                return todos
            except Exception:
                pass
        return []


# ================================================================
# GENERADOR PDF — DOCUMENTOS (6 tipos)
# CORREGIDO: "Se expide a solicitud del padre/madre/apoderado"
# ================================================================

class GeneradorPDF:
    def __init__(self, config):
        self.config = config
        self.buffer = io.BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()

    def _fondo(self):
        if Path("fondo.png").exists():
            try:
                self.canvas.drawImage("fondo.png", 0, 0,
                                       width=self.width, height=self.height)
            except Exception:
                pass

    def _marca_agua(self):
        if Path("escudo_upload.png").exists():
            try:
                self.canvas.saveState()
                self.canvas.setFillAlpha(0.06)
                self.canvas.drawImage("escudo_upload.png",
                                       self.width / 2 - 120, self.height / 2 - 120,
                                       240, 240, mask='auto')
                self.canvas.restoreState()
            except Exception:
                pass

    def _encabezado(self, titulo):
        self.canvas.setFont("Helvetica-Oblique", 11)
        self.canvas.drawCentredString(self.width / 2, self.config['y_frase'],
                                       f'"{self.config["frase"]}"')
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

    def _qr(self, datos, tipo):
        data = (f"YACHAY|{tipo}|{datos.get('alumno', datos.get('Nombre', ''))}|"
                f"{datos.get('dni', datos.get('DNI', ''))}|"
                f"{hora_peru().strftime('%d/%m/%Y')}")
        q = qrcode.QRCode(box_size=10, border=1)
        q.add_data(data)
        q.make(fit=True)
        img = q.make_image(fill_color="black", back_color="white")
        tmp = "tmp_qr.png"
        img.save(tmp)
        self.canvas.drawImage(tmp, self.config['qr_x'], self.config['qr_y'], 70, 70)
        self.canvas.setFont("Helvetica", 6)
        self.canvas.drawCentredString(self.config['qr_x'] + 35,
                                       self.config['qr_y'] - 5, "VERIFICACIÓN")
        try:
            os.remove(tmp)
        except Exception:
            pass

    def _solicitante(self, datos, y):
        """CORREGIDO: Se expide a solicitud del padre/madre/apoderado"""
        apoderado = datos.get('apoderado', datos.get('Apoderado', '')).upper()
        dni_apo = datos.get('dni_apo', datos.get('DNI_Apoderado', ''))
        alumno = datos.get('alumno', datos.get('Nombre', '')).upper()
        e = ParagraphStyle('S', parent=self.styles['Normal'],
                            fontSize=10, leading=14, alignment=TA_JUSTIFY)
        if apoderado and apoderado.strip():
            texto = (f"Se expide el presente documento a solicitud del "
                     f"padre/madre/apoderado(a) <b>{apoderado}</b>, "
                     f"identificado(a) con DNI N° <b>{dni_apo}</b>, "
                     f"en representación del/la estudiante <b>{alumno}</b>.")
        else:
            texto = (f"Se expide el presente documento a solicitud de parte "
                     f"interesada, para los fines que estime conveniente.")
        return self._parrafo(texto, 60, y, self.width - 120, e)

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

    def generar_constancia_vacante(self, d):
        self._fondo()
        self._marca_agua()
        self._encabezado("CONSTANCIA DE VACANTE")
        y = self.config['y_titulo'] - 50
        mx, an = 60, self.width - 120
        e = ParagraphStyle('N', parent=self.styles['Normal'],
                            fontSize=11, leading=15, alignment=TA_JUSTIFY)
        el = ParagraphStyle('L', parent=e, leftIndent=25)
        al = d.get('alumno', d.get('Nombre', '')).upper()
        dni = d.get('dni', d.get('DNI', ''))
        gr = d.get('grado', d.get('Grado', '')).upper()
        y = self._parrafo(
            "La Dirección de la I.E.P. ALTERNATIVO YACHAY de Chinchero, "
            "debidamente representada por su Directora, certifica:", mx, y, an, e
        )
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
        self._qr(d, "VACANTE")
        return self._fin()

    def generar_constancia_no_deudor(self, d):
        self._fondo()
        self._marca_agua()
        self._encabezado("CONSTANCIA DE NO ADEUDO")
        y = self.config['y_titulo'] - 50
        mx, an = 60, self.width - 120
        e = ParagraphStyle('N', parent=self.styles['Normal'],
                            fontSize=11, leading=15, alignment=TA_JUSTIFY)
        al = d.get('alumno', d.get('Nombre', '')).upper()
        dni = d.get('dni', d.get('DNI', ''))
        y = self._parrafo(
            "La Dirección de la I.E.P. ALTERNATIVO YACHAY:", mx, y, an, e
        )
        y = self._parrafo(
            f"Que el/la estudiante <b>{al}</b>, DNI N° <b>{dni}</b>, "
            f"ha cumplido con todas sus obligaciones económicas, "
            f"no registrando deuda alguna.", mx, y, an, e
        )
        y = self._solicitante(d, y)
        self._firmas()
        self._qr(d, "NO ADEUDO")
        return self._fin()

    def generar_constancia_estudios(self, d):
        self._fondo()
        self._marca_agua()
        self._encabezado("CONSTANCIA DE ESTUDIOS")
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
            f"cursando <b>{gr}</b>, conforme consta en registros oficiales "
            f"y el Sistema SIAGIE.", mx, y, an, e
        )
        y = self._solicitante(d, y)
        self._firmas()
        self._qr(d, "ESTUDIOS")
        return self._fin()

    def generar_constancia_conducta(self, d):
        self._fondo()
        self._marca_agua()
        self._encabezado("CONSTANCIA DE CONDUCTA")
        y = self.config['y_titulo'] - 50
        mx, an = 60, self.width - 120
        e = ParagraphStyle('N', parent=self.styles['Normal'],
                            fontSize=10, leading=14, alignment=TA_JUSTIFY)
        al = d.get('alumno', d.get('Nombre', '')).upper()
        dni = d.get('dni', d.get('DNI', ''))
        y = self._parrafo(
            f"Que <b>{al}</b>, DNI N° <b>{dni}</b>, obtuvo en CONDUCTA:",
            mx, y, an, e
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
        self._qr(d, "CONDUCTA")
        return self._fin()

    def generar_carta_compromiso(self, d):
        self._fondo()
        self._marca_agua()
        self._encabezado("CARTA DE COMPROMISO")
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
            f"Yo, <b>{apo}</b>, DNI N° <b>{dapo}</b>, "
            f"padre/madre/apoderado(a) de <b>{al}</b>, del <b>{gr}</b>, "
            f"me comprometo a:", mx, y, an, e
        )
        for c in [
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
        ]:
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

    def generar_resolucion_traslado(self, d):
        self._fondo()
        self._marca_agua()
        self.canvas.setFont("Helvetica-Oblique", 11)
        self.canvas.drawCentredString(self.width / 2, 700,
                                       f'"{self.config["frase"]}"')
        self.canvas.setFont("Helvetica-Bold", 14)
        self.canvas.drawCentredString(self.width / 2, 670,
                                       f"RESOLUCIÓN DIRECTORAL N° {d.get('num_resolucion', '')}")
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
        t = Table([
            ['ALUMNO', al],
            ['NIVEL', niv],
            ['IE PROCEDENCIA', 'IEP ALTERNATIVO YACHAY'],
            ['IE DESTINO', d.get('ie_destino', '').upper()]
        ], colWidths=[200, 280])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        t.wrapOn(self.canvas, an, 200)
        t.drawOn(self.canvas, mx, y - 80)
        self._firmas()
        self._qr(d, "TRASLADO")
        return self._fin()


# ================================================================
# REGISTRO AUXILIAR PDF — 3 Cursos × 4 Competencias × 3 Desempeños
# ================================================================

def generar_registro_auxiliar_pdf(grado, seccion, anio, bimestre,
                                  estudiantes_df, cursos=None):
    if cursos is None:
        cursos = ["Matemática", "Comunicación", "Ciencia y Tec."]
    nc = len(cursos)
    dp = 3  # desempeños por competencia
    cp = 4  # competencias por curso
    total_d = nc * cp * dp
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    w, h = landscape(A4)
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
                        "I.E.P. ALTERNATIVO YACHAY - REGISTRO AUXILIAR DE EVALUACIÓN")
    c.setFont("Helvetica", 8)
    c.drawCentredString(w / 2, h - 35,
                        f"Grado: {grado} | Sección: {seccion} | {bimestre} | Año: {anio}")
    c.setFont("Helvetica-Oblique", 7)
    c.drawCentredString(w / 2, h - 47,
                        '"Educar para la Vida — Pioneros en la Educación de Calidad"')

    cols_per_c = cp * dp
    r0 = ["N°", "APELLIDOS Y NOMBRES"]
    for curso in cursos:
        r0.append(curso.upper())
        r0.extend([""] * (cols_per_c - 1))
    r1 = ["", ""]
    for _ in range(nc):
        for ci in range(1, cp + 1):
            r1.append(f"C{ci}")
            r1.extend([""] * (dp - 1))
    r2 = ["", ""]
    for _ in range(nc):
        for _ in range(cp):
            for di in range(1, dp + 1):
                r2.append(f"D{di}")

    if not estudiantes_df.empty:
        est = estudiantes_df.sort_values('Nombre').reset_index(drop=True)
    else:
        est = pd.DataFrame()
    data = [r0, r1, r2]
    ne = len(est) if not est.empty else 25
    for idx in range(ne):
        nm = est.iloc[idx].get('Nombre', '') if idx < len(est) else ""
        if len(nm) > 28:
            nm = nm[:28] + "."
        data.append([str(idx + 1), nm] + [""] * total_d)

    avail = w - 30
    wn = 16
    wname = 115
    wd = max(16, min(25, (avail - wn - wname) / total_d))
    cw = [wn, wname] + [wd] * total_d
    tabla = Table(data, colWidths=cw, repeatRows=3)
    sl = [
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
    colores_c = [
        colors.Color(0, 0.2, 0.5),
        colors.Color(0.15, 0.35, 0.15),
        colors.Color(0.4, 0.15, 0.15)
    ]
    for ci, curso in enumerate(cursos):
        cs = 2 + ci * cols_per_c
        ce = cs + cols_per_c - 1
        sl.append(('SPAN', (cs, 0), (ce, 0)))
        bg = colores_c[ci % len(colores_c)]
        sl.append(('BACKGROUND', (cs, 0), (ce, 0), bg))
        sl.append(('TEXTCOLOR', (cs, 0), (ce, 0), colors.white))
        for ki in range(cp):
            s = cs + ki * dp
            e = s + dp - 1
            sl.append(('SPAN', (s, 1), (e, 1)))
            bg2 = colors.Color(min(bg.red + 0.1, 1),
                               min(bg.green + 0.1, 1),
                               min(bg.blue + 0.1, 1))
            sl.append(('BACKGROUND', (s, 1), (e, 1), bg2))
            sl.append(('TEXTCOLOR', (s, 1), (e, 1), colors.white))
            sl.append(('BACKGROUND', (s, 2), (e, 2), bg2))
            sl.append(('TEXTCOLOR', (s, 2), (e, 2), colors.white))
    tabla.setStyle(TableStyle(sl))
    tw, th = tabla.wrap(w - 20, h - 70)
    tabla.drawOn(c, 10, h - 58 - th)
    c.setFont("Helvetica", 5)
    c.drawString(10, 12,
                 f"C=Competencia | D=Desempeño | AD(18-20) A(14-17) "
                 f"B(11-13) C(0-10) | {bimestre} | YACHAY PRO — {anio}")
    c.save()
    buffer.seek(0)
    return buffer


# ================================================================
# REGISTRO ASISTENCIA PDF (sin sáb/dom, sin feriados + pie feriados)
# ================================================================

def generar_registro_asistencia_pdf(grado, seccion, anio, estudiantes_df,
                                     meses_sel):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    w, h = landscape(A4)
    if not estudiantes_df.empty:
        est = estudiantes_df.sort_values('Nombre').reset_index(drop=True)
    else:
        est = pd.DataFrame()
    ds = {0: "L", 1: "M", 2: "Mi", 3: "J", 4: "V"}
    for mi, mn in enumerate(meses_sel):
        if mi > 0:
            c.showPage()
        mnm = MESES_ESCOLARES.get(mn, f"Mes {mn}")
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
                            f"Mes: {mnm} | Año: {anio}")
        dias = dias_habiles_mes(int(anio), mn)
        nd = len(dias)
        header = ["N°", "APELLIDOS Y NOMBRES"]
        for d in dias:
            dt = date(int(anio), mn, d)
            header.append(f"{d}\n{ds[dt.weekday()]}")
        header.extend(["A", "T", "F", "J"])
        data = [header]
        ne = len(est) if not est.empty else 25
        for idx in range(ne):
            nm = est.iloc[idx].get('Nombre', '') if idx < len(est) else ""
            if len(nm) > 32:
                nm = nm[:32] + "."
            data.append([str(idx + 1), nm] + [""] * nd + ["", "", "", ""])
        dw = max(15, min(22, (w - 18 - 140 - 72 - 30) / max(nd, 1)))
        cw = [18, 140] + [dw] * nd + [18, 18, 18, 18]
        t = Table(data, colWidths=cw, repeatRows=1)
        t.setStyle(TableStyle([
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
        tw, th2 = t.wrap(w - 20, h - 60)
        t.drawOn(c, 10, h - 48 - th2)
        fer = feriados_del_mes(mn)
        c.setFont("Helvetica", 5)
        pie = ("A=Asistió | T=Tardanza | F=Falta | J=Justificada | "
               "Sin sábados, domingos ni feriados")
        if fer:
            pie += f" | FERIADOS EXCLUIDOS: {', '.join(fer)}"
        c.drawString(10, 8, pie)
    c.save()
    buffer.seek(0)
    return buffer


# ================================================================
# RANKING PDF — COLUMNAS FIJAS + COLORES POR ÁREA
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
    c.drawCentredString(w / 2, h - 58, '"Pioneros en la Educación de Calidad"')
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w / 2, h - 85, f"RANKING DE RESULTADOS — {anio}")
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, h - 100,
                        f"Generado: {hora_peru().strftime('%d/%m/%Y %H:%M')}")

    rk = sorted(resultados,
                key=lambda r: r.get('promedio_general', 0), reverse=True)
    all_a = set()
    for r in rk:
        for a in r.get('areas', []):
            all_a.add(a['nombre'])
    all_a = sorted(all_a)

    header = ["#", "APELLIDOS Y NOMBRES", "DNI"]
    header.extend(all_a)
    header.append("PROM.")
    data = [header]
    for idx, r in enumerate(rk):
        nm = r.get('nombre', '')
        if len(nm) > 30:
            nm = nm[:30] + "."
        fila = [str(idx + 1), nm, r.get('dni', '')]
        an_map = {a['nombre']: str(a['nota']) for a in r.get('areas', [])}
        for a in all_a:
            fila.append(an_map.get(a, '-'))
        fila.append(str(r.get('promedio_general', 0)))
        data.append(fila)

    na = len(all_a)
    # Anchos fijos: #=20, Nombre=150, DNI=55, Áreas=50 cada una, Prom=45
    cw = [20, 150, 55] + [50] * na + [45]
    t = Table(data, colWidths=cw, repeatRows=1)
    st_l = [
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (2, 0), colors.Color(0.1, 0.1, 0.4)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (-1, 0), (-1, 0), colors.Color(0.3, 0, 0.3)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.white, colors.Color(0.95, 0.95, 1)]),
    ]
    # Colores diferentes por área
    colores_areas = [
        colors.Color(0, 0.3, 0.6),       # Azul
        colors.Color(0.2, 0.5, 0.1),      # Verde
        colors.Color(0.6, 0.2, 0),         # Naranja
        colors.Color(0.4, 0, 0.4),         # Morado
        colors.Color(0, 0.4, 0.4),         # Teal
        colors.Color(0.5, 0.3, 0),         # Marrón
        colors.Color(0.3, 0.1, 0.5),       # Índigo
        colors.Color(0.6, 0, 0.2),         # Rosa oscuro
    ]
    for i in range(na):
        col_idx = 3 + i
        bg = colores_areas[i % len(colores_areas)]
        st_l.append(('BACKGROUND', (col_idx, 0), (col_idx, 0), bg))
    # Top 3
    bg_top = [
        colors.Color(1, 0.84, 0),
        colors.Color(0.75, 0.75, 0.75),
        colors.Color(0.8, 0.5, 0.2),
    ]
    for i in range(min(3, len(rk))):
        st_l.append(('BACKGROUND', (0, i + 1), (-1, i + 1), bg_top[i]))
    t.setStyle(TableStyle(st_l))
    tw, th2 = t.wrap(w - 40, h - 150)
    t.drawOn(c, 20, h - 120 - th2)
    c.setFont("Helvetica", 7)
    c.drawCentredString(w / 2, 30,
                        f"YACHAY PRO — {hora_peru().strftime('%d/%m/%Y %H:%M')}")
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
                esc = Image.open("escudo_upload.png").convert("RGBA")
                esc = esc.resize((280, 280), Image.LANCZOS)
                capa = Image.new('RGBA', (self.WIDTH, self.HEIGHT), (255, 255, 255, 0))
                capa.paste(esc, ((self.WIDTH - 280) // 2, (self.HEIGHT - 280) // 2))
                px = [(d[0], d[1], d[2], min(d[3], 28)) for d in capa.getdata()]
                capa.putdata(px)
                self.img = Image.alpha_composite(
                    self.img.convert('RGBA'), capa
                ).convert('RGB')
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
        fh = RecursoManager.obtener_fuente("", 36, True)
        fm = RecursoManager.obtener_fuente("", 19, True)
        fc = RecursoManager.obtener_fuente("", 17, True)
        fp = RecursoManager.obtener_fuente("", 13, True)
        self.draw.text((self.WIDTH // 2, 65), "I.E. ALTERNATIVO YACHAY",
                       font=fh, fill="white", anchor="mm")
        self.draw.text((self.WIDTH // 2, 115), '"EDUCAR PARA LA VIDA"',
                       font=fm, fill=self.DORADO, anchor="mm")
        tt = "CARNET DOCENTE" if self.es_docente else "CARNET ESCOLAR"
        self.draw.text((self.WIDTH // 2, 160), f"{tt} {self.anio}",
                       font=fc, fill="white", anchor="mm")
        self.draw.text((self.WIDTH // 2, self.HEIGHT - 35),
                       "PIONEROS EN LA EDUCACIÓN DE CALIDAD",
                       font=fp, fill=self.DORADO, anchor="mm")

    def _foto(self):
        x, y, wf, hf = 40, 228, 220, 280
        if self.foto_bytes:
            try:
                f = Image.open(self.foto_bytes).convert("RGB")
                self.img.paste(f.resize((wf, hf), Image.LANCZOS), (x, y))
            except Exception:
                self._ph(x, y, wf, hf)
        else:
            self._ph(x, y, wf, hf)
        self.draw.rectangle([(x - 3, y - 3), (x + wf + 3, y + hf + 3)],
                            outline=self.DORADO, width=4)

    def _ph(self, x, y, w, h):
        """Avatar por defecto según sexo del estudiante"""
        sexo = self.datos.get('Sexo', 'Masculino')
        if sexo == 'Femenino':
            bg_color = "#fce4ec"
            icon_color = "#e91e63"
            text_icon = "👩"
        else:
            bg_color = "#e3f2fd"
            icon_color = "#1565c0"
            text_icon = "👨"
        self.draw.rectangle([(x, y), (x + w, y + h)], fill=bg_color)
        # Silueta simple
        cx, cy = x + w // 2, y + h // 2
        # Cabeza
        head_r = min(w, h) // 6
        self.draw.ellipse([(cx - head_r, cy - head_r - 30),
                           (cx + head_r, cy + head_r - 30)],
                          fill=icon_color)
        # Cuerpo
        body_w = min(w, h) // 3
        self.draw.ellipse([(cx - body_w, cy + head_r - 10),
                           (cx + body_w, cy + head_r + body_w + 20)],
                          fill=icon_color)
        # Texto
        try:
            fn = RecursoManager.obtener_fuente("", 11)
            self.draw.text((cx, y + h - 15), "FOTO PENDIENTE",
                           font=fn, fill="#666", anchor="mm")
        except Exception:
            pass

    def _datos(self):
        xt = 290
        nm = self.datos.get('Nombre', self.datos.get('alumno', '')).upper()
        dni = str(self.datos.get('DNI', self.datos.get('dni', '')))
        fn = RecursoManager.obtener_fuente("", 19 if len(nm) > 25 else 22, True)
        fl = RecursoManager.obtener_fuente("", 14, True)
        fd = RecursoManager.obtener_fuente("", 14)
        yc = 240
        if len(nm) > 28:
            for l in textwrap.TextWrapper(width=28).wrap(nm)[:3]:
                self.draw.text((xt, yc), l, font=fn, fill="black")
                yc += 26
        else:
            self.draw.text((xt, yc), nm, font=fn, fill="black")
            yc += 30
        yc += 8
        self.draw.text((xt, yc), "DNI:", font=fl, fill="black")
        self.draw.text((xt + 60, yc), dni, font=fd, fill="black")
        yc += 28
        if self.es_docente:
            cg = self.datos.get('Cargo', 'DOCENTE').upper()
            self.draw.text((xt, yc), "CARGO:", font=fl, fill="black")
            self.draw.text((xt + 90, yc), cg, font=fd, fill="black")
            yc += 28
            esp = self.datos.get('Especialidad', '').upper()
            if esp:
                self.draw.text((xt, yc), "ESPEC.:", font=fl, fill="black")
                self.draw.text((xt + 100, yc), esp[:20], font=fd, fill="black")
                yc += 28
        else:
            gr = self.datos.get('Grado', self.datos.get('grado', '')).upper()
            sc = self.datos.get('Seccion', self.datos.get('seccion', ''))
            self.draw.text((xt, yc), "GRADO:", font=fl, fill="black")
            self.draw.text((xt + 90, yc), gr, font=fd, fill="black")
            yc += 28
            if sc:
                self.draw.text((xt, yc), "SECCIÓN:", font=fl, fill="black")
                self.draw.text((xt + 110, yc), str(sc), font=fd, fill="black")
                yc += 28
        self.draw.text((xt, yc), "VIGENCIA:", font=fl, fill="black")
        self.draw.text((xt + 120, yc), str(self.anio), font=fd, fill="black")

    def _qr(self):
        try:
            dni = str(self.datos.get('DNI', self.datos.get('dni', '')))
            q = qrcode.QRCode(box_size=12, border=1)
            q.add_data(dni)
            q.make(fit=True)
            iq = q.make_image(fill_color="black", back_color="white")
            iq = iq.resize((200, 200), Image.LANCZOS)
            self.img.paste(iq, (self.WIDTH - 235, 210))
            fs = RecursoManager.obtener_fuente("", 10, True)
            self.draw.text((self.WIDTH - 135, 418), "ESCANEAR QR",
                           font=fs, fill="black", anchor="mm")
        except Exception:
            pass

    def _barcode(self):
        if not HAS_BARCODE:
            return
        try:
            dni = str(self.datos.get('DNI', self.datos.get('dni', '')))
            buf2 = io.BytesIO()
            Code128(dni, writer=ImageWriter()).write(buf2, options={
                'write_text': False, 'module_width': 0.5,
                'module_height': 10, 'quiet_zone': 2
            })
            buf2.seek(0)
            ib = Image.open(buf2)
            ib = ib.crop(ib.getbbox())
            ib = ib.resize((320, 55), Image.LANCZOS)
            xb = (self.WIDTH - 320) // 2
            yb = self.HEIGHT - 130
            self.img.paste(ib, (xb, yb))
            fbc = RecursoManager.obtener_fuente("", 11, True)
            self.draw.text((self.WIDTH // 2, yb + 58), f"DNI: {dni}",
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
        out = io.BytesIO()
        self.img.save(out, format='PNG', optimize=True, quality=95)
        out.seek(0)
        return out


# ================================================================
# CARNETS LOTE PDF — 8 POR HOJA (fotocheck)
# ================================================================

def generar_carnets_lote_pdf(lista_datos, anio, es_docente=False):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4
    mx = 15 * mm
    my = 10 * mm
    cw2 = (w - 2 * mx - 5 * mm) / 2
    ch2 = (h - 2 * my - 15 * mm) / 4
    gx = 5 * mm
    gy = 3.5 * mm
    pp = 8
    total = len(lista_datos)
    np2 = (total + pp - 1) // pp
    for pag in range(np2):
        if pag > 0:
            c.showPage()
        ini = pag * pp
        fin = min(ini + pp, total)
        for idx in range(ini, fin):
            pos = idx - ini
            col = pos % 2
            fila = pos // 2
            x = mx + col * (cw2 + gx)
            y = h - my - (fila + 1) * ch2 - fila * gy
            gen = GeneradorCarnet(lista_datos[idx], anio, es_docente=es_docente)
            ib = gen.generar()
            tmp = f"tmp_c_{idx}.png"
            with open(tmp, 'wb') as f:
                f.write(ib.getvalue())
            try:
                c.drawImage(tmp, x, y, width=cw2, height=ch2,
                            preserveAspectRatio=True)
                c.setStrokeColor(colors.grey)
                c.setDash(3, 3)
                c.setLineWidth(0.3)
                c.rect(x, y, cw2, ch2)
                c.setDash()
            except Exception:
                pass
            try:
                os.remove(tmp)
            except Exception:
                pass
        c.setFont("Helvetica", 6)
        c.setFillColor(colors.grey)
        c.drawCentredString(w / 2, 10,
                            f"YACHAY — Carnets {anio} — Pág {pag + 1}/{np2} — "
                            f"Cortar por líneas punteadas")
        c.setFillColor(colors.black)
    c.save()
    buffer.seek(0)
    return buffer


# ================================================================
# UTILIDADES
# ================================================================

def generar_link_whatsapp(tel, msg):
    t = str(tel).strip().replace("+", "").replace(" ", "").replace("-", "")
    if len(t) == 9:
        t = "51" + t
    elif not t.startswith("51"):
        t = "51" + t
    # wa.me funciona tanto en móvil como en WhatsApp Web
    return f"https://wa.me/{t}?text={urllib.parse.quote(msg)}"


FRASES_MOTIVACIONALES = [
    "🌟 La puntualidad es la cortesía de los reyes y la obligación de los caballeros.",
    "📚 Educar es sembrar semillas de futuro. ¡Gracias por confiar en YACHAY!",
    "🎯 El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
    "💪 Cada día de clases es una oportunidad para crecer y aprender.",
    "🌈 La educación es el arma más poderosa para cambiar el mundo. — Nelson Mandela",
    "⭐ Un niño puntual hoy será un adulto responsable mañana.",
    "📖 Leer es soñar con los ojos abiertos. ¡Motivemos la lectura!",
    "🏆 El talento gana juegos, pero el trabajo en equipo gana campeonatos.",
    "🌱 Cada estudiante es una semilla; con amor y educación, florecerá.",
    "🔑 La disciplina es el puente entre las metas y los logros.",
    "💡 No hay atajos para ningún lugar que valga la pena ir.",
    "🎓 La mejor inversión es la educación de nuestros hijos.",
    "🌻 Con esfuerzo y dedicación, todo es posible. ¡Vamos YACHAY!",
    "📝 El hábito de estudiar hoy construye el profesional del mañana.",
    "🤝 Familia y escuela juntos: la fórmula del éxito educativo.",
    "⏰ La puntualidad es un valor que se enseña desde casa.",
    "🎒 Cada día es una nueva página en el libro de la vida.",
    "🏫 YACHAY significa aprender. ¡Aprendamos juntos!",
    "✨ El futuro pertenece a quienes creen en la belleza de sus sueños.",
    "🌟 Educar para la Vida — Pioneros en la Educación de Calidad.",
]

import random as _random


def generar_mensaje_asistencia(nombre, tipo, hora):
    saludo = "Buenos días" if int(hora.split(':')[0]) < 12 else "Buenas tardes"
    em = "✅ ENTRADA" if tipo == "entrada" else "🏁 SALIDA"
    frase = _random.choice(FRASES_MOTIVACIONALES)
    return (f"{saludo}\n🏫 I.E. ALTERNATIVO YACHAY informa:\n"
            f"{em} registrada\n👤 {nombre}\n🕒 Hora: {hora}\n\n"
            f"{frase}")


def decodificar_qr_imagen(ib):
    if not HAS_PYZBAR:
        return None
    try:
        img = Image.open(io.BytesIO(ib))
        cod = pyzbar_decode(img)
        if cod:
            return cod[0].data.decode('utf-8')
    except Exception:
        pass
    if HAS_CV2:
        try:
            np2 = np.frombuffer(ib, np.uint8)
            ic = cv2.imdecode(np2, cv2.IMREAD_COLOR)
            gr = cv2.cvtColor(ic, cv2.COLOR_BGR2GRAY)
            for m in [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV]:
                _, th = cv2.threshold(gr, 127, 255, m)
                cod = pyzbar_decode(Image.fromarray(th))
                if cod:
                    return cod[0].data.decode('utf-8')
        except Exception:
            pass
    return None




# ================================================================
# HOJA DE RESPUESTAS + ESCÁNER OMR PROFESIONAL
# Sistema basado en posición con marcadores de alineación
# ================================================================

# Constantes de la hoja (compartidas entre generador y escáner)
HOJA_W = 2480       # Ancho A4 300dpi
HOJA_H = 3508       # Alto A4 300dpi
HOJA_MARKER_SIZE = 100   # Tamaño marcadores esquina
HOJA_MARKER_PAD = 40     # Padding de marcadores desde borde
HOJA_BUBBLE_R = 34       # Radio de burbuja
HOJA_Y_START = 950       # Y donde empiezan las burbujas
HOJA_X_START = 340       # X donde empieza la primera opción
HOJA_SP_Y = 108          # Espacio vertical entre preguntas
HOJA_SP_X = 155          # Espacio horizontal entre opciones A,B,C,D
HOJA_COL_SP = 750        # Espacio entre columnas de preguntas
HOJA_PPC = 20            # Preguntas por columna (máximo seguro)


def _posicion_burbuja(pregunta_idx, opcion_idx):
    """Calcula posición exacta (cx, cy) de una burbuja en la hoja"""
    col = pregunta_idx // HOJA_PPC
    fila = pregunta_idx % HOJA_PPC
    cx = HOJA_X_START + col * HOJA_COL_SP + opcion_idx * HOJA_SP_X
    cy = HOJA_Y_START + fila * HOJA_SP_Y
    return cx, cy


def generar_hoja_respuestas(np_, titulo):
    """Genera hoja de respuestas OPTIMIZADA para escaneo OMR"""
    img = Image.new('RGB', (HOJA_W, HOJA_H), 'white')
    draw = ImageDraw.Draw(img)
    try:
        ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 45)
        fn = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
        fl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    except Exception:
        ft = fs = fn = fl = fb = ImageFont.load_default()

    # ===== 4 MARCADORES DE ESQUINA (cruciales para alineación) =====
    ms = HOJA_MARKER_SIZE
    mp = HOJA_MARKER_PAD
    # Superior izquierdo
    draw.rectangle([(mp, mp), (mp + ms, mp + ms)], fill="black")
    # Superior derecho
    draw.rectangle([(HOJA_W - mp - ms, mp), (HOJA_W - mp, mp + ms)], fill="black")
    # Inferior izquierdo
    draw.rectangle([(mp, HOJA_H - mp - ms), (mp + ms, HOJA_H - mp)], fill="black")
    # Inferior derecho
    draw.rectangle([(HOJA_W - mp - ms, HOJA_H - mp - ms),
                    (HOJA_W - mp, HOJA_H - mp)], fill="black")

    # Marcadores adicionales de orientación (rectángulo pequeño solo arriba-izq)
    draw.rectangle([(mp, mp + ms + 10), (mp + ms, mp + ms + 30)], fill="black")

    # ===== ENCABEZADO =====
    draw.text((HOJA_W // 2, 200), "I.E.P. ALTERNATIVO YACHAY",
              font=ft, fill="black", anchor="mm")
    draw.text((HOJA_W // 2, 290), f"HOJA DE RESPUESTAS — {titulo.upper()}",
              font=fs, fill="black", anchor="mm")
    draw.text((HOJA_W // 2, 360), "SISTEMA DE CALIFICACIÓN YACHAY",
              font=fs, fill="gray", anchor="mm")

    # ===== DATOS DEL ALUMNO =====
    draw.text((220, 480), "Nombre: _____________________________________________",
              font=fs, fill="black")
    draw.text((220, 560), "DNI: __________________  Grado: __________________",
              font=fs, fill="black")
    draw.text((220, 640), f"Fecha: __________________  Total: {np_} preguntas",
              font=fs, fill="black")

    # ===== INSTRUCCIONES =====
    draw.text((220, 740), "✎ RELLENE COMPLETAMENTE el círculo de su respuesta",
              font=fb, fill="red")
    # Ejemplo visual
    ex_y = 795
    draw.text((220, ex_y), "Correcto:", font=fl, fill="gray")
    draw.ellipse([(430, ex_y - 5), (490, ex_y + 55)], fill="black")
    draw.text((530, ex_y), "Incorrecto:", font=fl, fill="gray")
    draw.ellipse([(770, ex_y - 5), (830, ex_y + 55)], outline="black", width=3)

    # Línea separadora gruesa
    draw.line([(100, 880), (HOJA_W - 100, 880)], fill="black", width=4)

    # ===== BURBUJAS =====
    for i in range(np_):
        col = i // HOJA_PPC
        fila = i % HOJA_PPC

        # Número de pregunta
        num_x = HOJA_X_START + col * HOJA_COL_SP - 120
        num_y = HOJA_Y_START + fila * HOJA_SP_Y
        draw.text((num_x, num_y), f"{i + 1}.",
                  font=fn, fill="black", anchor="rm")

        # 4 opciones: A, B, C, D
        for j, letra in enumerate(['A', 'B', 'C', 'D']):
            cx, cy = _posicion_burbuja(i, j)
            r = HOJA_BUBBLE_R
            # Círculo bien definido con borde grueso
            draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)],
                         outline="black", width=5)
            # Letra pequeña dentro
            draw.text((cx, cy), letra, font=fl, fill=(100, 100, 100), anchor="mm")

    # ===== PIE DE PÁGINA CON FRASES DE SEGURIDAD =====
    draw.line([(100, HOJA_H - 250), (HOJA_W - 100, HOJA_H - 250)],
              fill="black", width=2)

    # Frases de seguridad estilo ZipGrade
    frases_seguridad = [
        "DOCUMENTO OFICIAL — CUALQUIER ALTERACIÓN INVALIDA ESTE EXAMEN",
        "PROHIBIDO REPRODUCIR — USO EXCLUSIVO I.E.P. ALTERNATIVO YACHAY",
        "SISTEMA YACHAY PRO — LECTURA ÓPTICA AUTOMATIZADA",
        "No doblar, arrugar, manchar ni realizar marcas fuera de los círculos",
        "Use SOLO lápiz 2B o bolígrafo negro — Rellene completamente cada círculo",
    ]
    y_pie = HOJA_H - 230
    for frase in frases_seguridad:
        draw.text((HOJA_W // 2, y_pie), frase,
                  font=fb, fill="gray", anchor="mm")
        y_pie += 30

    # Código de seguridad único — visible en negro al costado derecho vertical
    codigo_seg = hashlib.md5(f"{titulo}{datetime.now().isoformat()}".encode()).hexdigest()[:12].upper()
    draw.text((HOJA_W // 2, HOJA_H - 60),
              f"Código: {codigo_seg} | YACHAY PRO {datetime.now().year}",
              font=fb, fill="black", anchor="mm")
    
    # Código vertical en margen derecho
    try:
        fv = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    except Exception:
        fv = fb
    codigo_vertical = f"COD: {codigo_seg}"
    for ci, ch in enumerate(codigo_vertical):
        draw.text((HOJA_W - 55, 300 + ci * 28), ch, font=fv, fill="gray")

    # Marca de agua diagonal
    try:
        marca_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except Exception:
        marca_font = fb
    marca_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
    marca_draw = ImageDraw.Draw(marca_img)
    for yy in range(200, HOJA_H - 200, 400):
        for xx in range(-200, HOJA_W, 600):
            marca_draw.text((xx, yy), "YACHAY PRO",
                           font=marca_font, fill=(200, 200, 200, 40))
    img = Image.alpha_composite(img.convert('RGBA'), marca_img).convert('RGB')

    out = io.BytesIO()
    img.save(out, format='PNG', quality=95)
    out.seek(0)
    return out


# ================================================================
# ESCÁNER OMR — DETECCIÓN POR POSICIÓN
# ================================================================

def _encontrar_marcadores(gray):
    """
    Encuentra los 4 marcadores de esquina (cuadrados negros grandes).
    Retorna las coordenadas ordenadas: [TL, TR, BL, BR] o None.
    """
    alto, ancho = gray.shape[:2]
    resultados = []

    # Probar múltiples umbrales para robustez
    for metodo in range(3):
        if metodo == 0:
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 0, 255,
                                       cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        elif metodo == 1:
            blur = cv2.GaussianBlur(gray, (7, 7), 0)
            thresh = cv2.adaptiveThreshold(blur, 255,
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY_INV, 21, 5)
        else:
            blur = cv2.medianBlur(gray, 5)
            _, thresh = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV)

        # Probar ambos modos de contorno para mayor robustez
        for retr_mode in [cv2.RETR_EXTERNAL, cv2.RETR_LIST]:
            contours, _ = cv2.findContours(thresh, retr_mode,
                                            cv2.CHAIN_APPROX_SIMPLE)

            # Buscar contornos grandes y cuadrados (los marcadores)
            candidatos = []
            min_size = min(ancho, alto) * 0.02  # Al menos 2% del tamaño
            max_size = min(ancho, alto) * 0.12  # Máximo 12%

            for ct in contours:
                x, y, w, h = cv2.boundingRect(ct)
                if w < min_size or h < min_size:
                    continue
                if w > max_size or h > max_size:
                    continue

                aspect = w / float(h) if h > 0 else 0
                if not (0.6 <= aspect <= 1.6):
                    continue

                area = cv2.contourArea(ct)
                rect_area = w * h
                solidez = area / rect_area if rect_area > 0 else 0
                if solidez < 0.6:
                    continue

                # Centro del contorno
                cx = x + w // 2
                cy = y + h // 2
                candidatos.append((cx, cy, w * h, x, y, w, h))

            if len(candidatos) < 4:
                continue

            # Ordenar por tamaño y tomar los más grandes
            candidatos = sorted(candidatos, key=lambda c: c[2], reverse=True)

            if len(candidatos) >= 4:
                top = candidatos[:min(12, len(candidatos))]
                mejor = _seleccionar_esquinas(top, ancho, alto)
                if mejor is not None:
                    resultados.append(mejor)
                    break  # Encontrado, no seguir probando modos

    if not resultados:
        return None

    # Retornar el primer resultado exitoso
    return resultados[0]


def _seleccionar_esquinas(candidatos, ancho, alto):
    """
    De una lista de candidatos, selecciona 4 que forman las esquinas
    de la hoja. Retorna [TL, TR, BL, BR] como arrays de coordenadas.
    """
    puntos = [(c[0], c[1]) for c in candidatos]

    # Clasificar por cuadrante
    cx_medio = ancho / 2
    cy_medio = alto / 2

    tl_cands = [(x, y) for x, y in puntos if x < cx_medio and y < cy_medio]
    tr_cands = [(x, y) for x, y in puntos if x > cx_medio and y < cy_medio]
    bl_cands = [(x, y) for x, y in puntos if x < cx_medio and y > cy_medio]
    br_cands = [(x, y) for x, y in puntos if x > cx_medio and y > cy_medio]

    if not (tl_cands and tr_cands and bl_cands and br_cands):
        return None

    # Tomar el más cercano a cada esquina
    tl = min(tl_cands, key=lambda p: p[0]**2 + p[1]**2)
    tr = min(tr_cands, key=lambda p: (ancho - p[0])**2 + p[1]**2)
    bl = min(bl_cands, key=lambda p: p[0]**2 + (alto - p[1])**2)
    br = min(br_cands, key=lambda p: (ancho - p[0])**2 + (alto - p[1])**2)

    return [list(tl), list(tr), list(bl), list(br)]


def _corregir_perspectiva(gray, esquinas):
    """
    Aplica transformación de perspectiva para alinear la hoja.
    esquinas = [TL, TR, BL, BR]
    Retorna imagen corregida de tamaño HOJA_W x HOJA_H
    """
    tl, tr, bl, br = esquinas

    # Puntos origen (de la foto)
    src = np.array([tl, tr, bl, br], dtype="float32")

    # Puntos destino (hoja perfecta) — ajustados a los centros de marcadores
    mp = HOJA_MARKER_PAD + HOJA_MARKER_SIZE // 2
    dst = np.array([
        [mp, mp],
        [HOJA_W - mp, mp],
        [mp, HOJA_H - mp],
        [HOJA_W - mp, HOJA_H - mp]
    ], dtype="float32")

    # Calcular y aplicar transformación
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(gray, M, (HOJA_W, HOJA_H))
    return warped


def _leer_burbujas(warped_gray, num_preguntas):
    """
    Lee las respuestas de la imagen ya corregida/alineada.
    MEJORADO: Lógica estricta anti-falsos positivos.
    - Pre-procesamiento con GaussianBlur + OTSU
    - Erosión para eliminar ruido/sombras
    - Umbral de relleno mínimo 45%
    - Comparación relativa: la más marcada debe ser >1.4x la segunda
    - Si no cumple condiciones → '?' (indeterminado)
    """
    # Pre-procesamiento robusto
    blur = cv2.GaussianBlur(warped_gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255,
                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Erosión para eliminar ruido, trazos débiles y sombras
    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)

    respuestas = []
    radio_muestra = int(HOJA_BUBBLE_R * 0.60)
    UMBRAL_RELLENO_MINIMO = 0.45   # Mínimo 45% del círculo relleno
    RATIO_DIFERENCIA = 1.4          # La más marcada debe ser 1.4x la segunda

    for i in range(num_preguntas):
        intensidades = []
        for j in range(4):  # A, B, C, D
            cx, cy = _posicion_burbuja(i, j)

            # Verificar límites
            if (cy - radio_muestra < 0 or cy + radio_muestra >= HOJA_H or
                    cx - radio_muestra < 0 or cx + radio_muestra >= HOJA_W):
                intensidades.append(0.0)
                continue

            # Crear máscara circular localizada (más eficiente)
            y1 = max(0, cy - radio_muestra - 5)
            y2 = min(HOJA_H, cy + radio_muestra + 5)
            x1 = max(0, cx - radio_muestra - 5)
            x2 = min(HOJA_W, cx + radio_muestra + 5)

            roi = thresh[y1:y2, x1:x2]
            mask_local = np.zeros_like(roi, dtype="uint8")
            cv2.circle(mask_local,
                       (cx - x1, cy - y1),
                       radio_muestra, 255, -1)

            masked = cv2.bitwise_and(roi, roi, mask=mask_local)
            total = cv2.countNonZero(mask_local)
            filled = cv2.countNonZero(masked)
            ratio = filled / total if total > 0 else 0.0
            intensidades.append(ratio)

        if not intensidades:
            respuestas.append('-')  # Sin datos = en blanco = 0 puntos
            continue

        max_val = max(intensidades)
        max_idx = intensidades.index(max_val)

        # Condición 1: Relleno mínimo
        if max_val < UMBRAL_RELLENO_MINIMO:
            respuestas.append('-')  # En blanco = 0 puntos (no marcó nada)
            continue

        # Condición 2: Diferencia significativa con la segunda opción
        sorted_vals = sorted(intensidades, reverse=True)
        segunda = sorted_vals[1] if len(sorted_vals) >= 2 else 0

        if segunda > 0 and max_val / segunda < RATIO_DIFERENCIA:
            respuestas.append('?')  # Ambiguo — corregir manualmente
            continue

        # Respuesta clara
        respuestas.append(['A', 'B', 'C', 'D'][max_idx])

    return respuestas


def _leer_sin_perspectiva(gray, num_preguntas):
    """
    Método alternativo cuando no se detectan marcadores.
    Intenta detectar la región de burbujas directamente.
    Busca patrones de filas de 4 elementos oscuros.
    """
    alto, ancho = gray.shape[:2]

    # Redimensionar a tamaño estándar para posiciones conocidas
    resized = cv2.resize(gray, (HOJA_W, HOJA_H), interpolation=cv2.INTER_LINEAR)

    _, thresh = cv2.threshold(resized, 0, 255,
                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Intentar leer directamente asumiendo que la imagen ya está alineada
    respuestas = _leer_burbujas(resized, num_preguntas)

    # Verificar calidad: si más del 70% son '?', falló
    preguntas_detectadas = sum(1 for r in respuestas if r != '?')
    if preguntas_detectadas < num_preguntas * 0.3:
        return None

    return respuestas


def procesar_examen(image_bytes, num_preguntas):
    """
    ESCÁNER OMR PROFESIONAL - Basado en posición.
    
    Método principal:
    1. Detecta 4 marcadores de esquina
    2. Corrige perspectiva (la foto se vuelve una hoja plana)
    3. Lee cada burbuja en su posición exacta
    
    Método alternativo (sin marcadores):
    - Redimensiona la imagen al tamaño de la hoja
    - Intenta leer las posiciones directamente
    
    Retorna lista de respuestas ['A','B','C','D','?'] o None si falla
    """
    if not HAS_CV2:
        return None

    try:
        # Decodificar imagen
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return None

        # Escalar si es muy grande (>4000px)
        h_orig, w_orig = img.shape[:2]
        escala = 1.0
        if max(h_orig, w_orig) > 4000:
            escala = 4000 / max(h_orig, w_orig)
            img = cv2.resize(img, (int(w_orig * escala), int(h_orig * escala)),
                             interpolation=cv2.INTER_AREA)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # === MÉTODO 1: Con marcadores (el más preciso) ===
        esquinas = _encontrar_marcadores(gray)
        if esquinas is not None:
            warped = _corregir_perspectiva(gray, esquinas)
            respuestas = _leer_burbujas(warped, num_preguntas)
            detectadas = sum(1 for r in respuestas if r != '?')
            if detectadas >= num_preguntas * 0.3:
                return respuestas

        # === MÉTODO 2: Redimensionar directo (sin marcadores) ===
        respuestas = _leer_sin_perspectiva(gray, num_preguntas)
        if respuestas:
            return respuestas

        # === MÉTODO 3: Mejorar contraste y reintentar ===
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        esquinas2 = _encontrar_marcadores(enhanced)
        if esquinas2 is not None:
            warped2 = _corregir_perspectiva(enhanced, esquinas2)
            respuestas2 = _leer_burbujas(warped2, num_preguntas)
            detectadas2 = sum(1 for r in respuestas2 if r != '?')
            if detectadas2 >= num_preguntas * 0.3:
                return respuestas2

        # === MÉTODO 4: Umbral manual y reintentar ===
        for umbral in [100, 120, 140, 160]:
            _, manual_thresh = cv2.threshold(gray, umbral, 255, cv2.THRESH_BINARY)
            esquinas3 = _encontrar_marcadores(manual_thresh)
            if esquinas3 is not None:
                warped3 = _corregir_perspectiva(gray, esquinas3)
                respuestas3 = _leer_burbujas(warped3, num_preguntas)
                detectadas3 = sum(1 for r in respuestas3 if r != '?')
                if detectadas3 >= num_preguntas * 0.3:
                    return respuestas3

        return None

    except Exception:
        return None

# ================================================================
# PANTALLA DE LOGIN (Usuario + Contraseña — SEGURO)
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
            usuarios = cargar_usuarios()
            usuario_lower = usuario.strip().lower()
            if usuario_lower in usuarios:
                datos_u = usuarios[usuario_lower]
                if contrasena == datos_u['password']:
                    st.session_state.rol = datos_u['rol']
                    st.session_state.docente_info = datos_u.get('docente_info')
                    st.session_state.usuario_actual = usuario_lower
                    st.rerun()
                else:
                    st.error("⛔ Contraseña incorrecta")
            else:
                st.error("⛔ Usuario no encontrado")
        st.caption("💡 Ingrese usuario y contraseña asignados por el administrador.")

        # Libro de reclamaciones
        st.markdown("---")
        with st.expander("📕 Libro de Reclamaciones Virtual"):
            st.markdown("*Según normativa MINEDU*")
            with st.form("form_reclamo_login", clear_on_submit=True):
                r_nombre = st.text_input("Nombre completo:", key="rl_nombre")
                r_dni = st.text_input("DNI:", key="rl_dni")
                r_cel = st.text_input("Celular:", key="rl_cel")
                r_tipo = st.selectbox("Tipo:", ["Queja", "Reclamo", "Sugerencia"], key="rl_tipo")
                r_detalle = st.text_area("Detalle:", key="rl_detalle")
                if st.form_submit_button("📩 ENVIAR", type="primary",
                                          use_container_width=True):
                    if r_nombre and r_dni and r_detalle:
                        gs = _gs()
                        if gs:
                            try:
                                ws = gs._get_hoja('config')
                                if ws:
                                    codigo_rec = f"REC-{hora_peru().year}-{int(time.time()) % 10000:04d}"
                                    ws.append_row([
                                        f"reclamo_{codigo_rec}",
                                        json.dumps({
                                            'codigo': codigo_rec, 'nombre': r_nombre,
                                            'dni': r_dni, 'celular': r_cel,
                                            'tipo': r_tipo, 'detalle': r_detalle,
                                            'fecha': fecha_peru_str(), 'hora': hora_peru_str(),
                                            'estado': 'Pendiente'
                                        }, ensure_ascii=False)
                                    ])
                                    st.success(f"✅ Reclamo registrado. Código: **{codigo_rec}**")
                            except Exception:
                                st.error("Error al enviar. Intente más tarde.")
                        else:
                            st.warning("Sistema en modo local.")
                    else:
                        st.error("Complete todos los campos.")


# ================================================================
# SIDEBAR — Con links SIAGIE y Google Institucional
# ================================================================

# ================================================================
# SISTEMA DE BACKUP Y RESTAURACIÓN
# ================================================================

ARCHIVOS_BACKUP = [
    ARCHIVO_MATRICULA,    # matricula.xlsx
    ARCHIVO_DOCENTES,     # docentes.xlsx
    ARCHIVO_BD,           # base_datos.xlsx
    ARCHIVO_ASISTENCIAS,  # asistencias.json
    ARCHIVO_RESULTADOS,   # resultados_examenes.json
    ARCHIVO_USUARIOS,     # usuarios.json
    "escudo_upload.png",
    "fondo.png",
]


def crear_backup():
    """Crea un ZIP con TODOS los datos del sistema"""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for archivo in ARCHIVOS_BACKUP:
            if Path(archivo).exists():
                zf.write(archivo, archivo)
        # Agregar un manifiesto con info del backup
        info = {
            "fecha": hora_peru().strftime('%d/%m/%Y %H:%M:%S'),
            "version": "YACHAY PRO v4.0",
            "archivos": [a for a in ARCHIVOS_BACKUP if Path(a).exists()],
            "total_alumnos": len(BaseDatos.cargar_matricula()),
            "total_docentes": len(BaseDatos.cargar_docentes()),
        }
        zf.writestr("_backup_info.json", json.dumps(info, indent=2, ensure_ascii=False))
    buf.seek(0)
    return buf


def restaurar_backup(zip_bytes):
    """Restaura datos desde un ZIP de backup"""
    errores = []
    restaurados = []
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zf:
            nombres = zf.namelist()
            for archivo in nombres:
                if archivo.startswith("_backup_"):
                    continue  # Saltar manifiesto
                try:
                    zf.extract(archivo, '.')
                    restaurados.append(archivo)
                except Exception as e:
                    errores.append(f"{archivo}: {str(e)}")
    except Exception as e:
        errores.append(f"Error ZIP: {str(e)}")
    return restaurados, errores


def configurar_sidebar():
    with st.sidebar:
        # Escudo
        if Path("escudo_upload.png").exists():
            st.image("escudo_upload.png", width=80)
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

        # Estado Google Sheets
        gs = _gs()
        if gs:
            st.markdown('<div class="gs-connected">☁️ Google Sheets: Conectado ✅</div>',
                       unsafe_allow_html=True)
        else:
            st.markdown('<div class="gs-offline">💾 Modo local (sin Google Sheets)</div>',
                       unsafe_allow_html=True)

        # Links institucionales para directivo y docentes
        if st.session_state.rol in ["directivo", "docente"]:
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(
                    f'<a href="{LINK_SIAGIE}" target="_blank" class="siagie-btn">'
                    f'📚 Ir a SIAGIE</a>', unsafe_allow_html=True)
            with c2:
                st.markdown(
                    f'<a href="{LINK_GOOGLE}" target="_blank" class="link-btn">'
                    f'📧 Cuenta Google</a>', unsafe_allow_html=True)

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
            with st.expander("🔐 Gestionar Usuarios"):
                _gestion_usuarios_admin()
            with st.expander("💾 BACKUP / RESTAURAR", expanded=False):
                st.caption("⚠️ **IMPORTANTE:** Streamlit Cloud puede borrar "
                           "tus datos. Haz backup frecuentemente.")
                st.markdown("---")
                st.markdown("**📥 DESCARGAR BACKUP:**")
                if st.button("💾 CREAR BACKUP AHORA", type="primary",
                             use_container_width=True, key="btn_backup"):
                    with st.spinner("📦 Empaquetando datos..."):
                        backup_zip = crear_backup()
                    fecha_bk = hora_peru().strftime('%Y%m%d_%H%M')
                    st.download_button(
                        f"⬇️ Descargar backup_{fecha_bk}.zip",
                        backup_zip,
                        f"backup_yachay_{fecha_bk}.zip",
                        "application/zip",
                        use_container_width=True,
                        key="dl_backup"
                    )
                    st.success("✅ Backup listo. ¡Guárdalo en tu PC!")
                st.markdown("---")
                st.markdown("**📤 RESTAURAR DESDE BACKUP:**")
                uploaded_backup = st.file_uploader(
                    "Subir archivo .zip de backup:",
                    type=["zip"], key="upload_backup"
                )
                if uploaded_backup:
                    st.warning("⚠️ Esto REEMPLAZARÁ todos los datos actuales "
                               "con los del backup.")
                    if st.button("🔄 RESTAURAR DATOS", type="primary",
                                 use_container_width=True, key="btn_restaurar"):
                        with st.spinner("🔄 Restaurando..."):
                            rest, errs = restaurar_backup(
                                uploaded_backup.getvalue()
                            )
                        if rest:
                            st.success(f"✅ Restaurados {len(rest)} archivos:\n"
                                       f"{', '.join(rest)}")
                        if errs:
                            st.error(f"❌ Errores: {', '.join(errs)}")
                        if rest:
                            st.balloons()
                            time.sleep(1)
                            st.rerun()

        st.markdown("---")
        anio = st.number_input("📅 Año:", 2024, 2040, 2026, key="ai")
        
        # Solo admin y directivo ven estadísticas
        if st.session_state.rol in ['admin', 'directivo']:
            stats = BaseDatos.obtener_estadisticas()
            c1, c2 = st.columns(2)
            with c1:
                st.metric("📚 Alumnos", stats['total_alumnos'])
            with c2:
                st.metric("👨‍🏫 Docentes", stats['total_docentes'])
        
        # Mensaje de guardado para todos
        st.markdown("""<div style="background: #dcfce7; border-radius: 8px; 
                    padding: 8px; text-align: center; font-size: 0.8rem; color: #166534;">
                    💾 Todo se guarda automáticamente en la nube
                    </div>""", unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("🔴 CERRAR SESIÓN", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    return {
        'anio': anio, 'directora': directora, 'promotor': promotor,
        'frase': frase, 'y_frase': 700, 'y_titulo': 630,
        'qr_x': 435, 'qr_y': 47
    }


# ================================================================
# GESTIÓN DE USUARIOS DESDE ADMIN
# ================================================================

def _gestion_usuarios_admin():
    """Admin puede crear/ver usuarios y asignar contraseñas"""
    usuarios = cargar_usuarios()
    st.caption(f"**{len(usuarios)} usuarios registrados:**")
    for usr, datos in usuarios.items():
        st.caption(f"• **{usr}** → {datos.get('label', datos['rol'])}")

    st.markdown("---")
    st.markdown("**➕ Crear nuevo usuario docente:**")
    nu_user = st.text_input("Nombre de usuario:", key="nu_user",
                             placeholder="ej: prof.arte")
    nu_pass = st.text_input("Contraseña:", key="nu_pass",
                             placeholder="contraseña segura")
    nu_label = st.text_input("Nombre completo:", key="nu_label",
                              placeholder="ej: Docente de Arte")
    nu_grado = st.selectbox("Grado asignado:",
                             ["N/A"] + TODOS_LOS_GRADOS + ["ALL_SECUNDARIA"],
                             key="nu_grado")
    nu_nivel = st.selectbox("Nivel:", ["INICIAL", "PRIMARIA", "SECUNDARIA",
                                        "PREUNIVERSITARIO"], key="nu_nivel")
    nu_rol = st.selectbox("Rol:", ["docente", "directivo", "auxiliar"],
                           key="nu_rol")

    if st.button("✅ CREAR USUARIO", type="primary", key="btn_crear_usr"):
        if nu_user and nu_pass and nu_label:
            u_key = nu_user.strip().lower()
            di = None
            if nu_rol == "docente" and nu_grado != "N/A":
                di = {"label": nu_label, "grado": nu_grado, "nivel": nu_nivel}
            usuarios[u_key] = {
                "password": nu_pass,
                "rol": nu_rol,
                "label": nu_label,
                "docente_info": di
            }
            guardar_usuarios(usuarios)
            st.success(f"✅ Usuario **{u_key}** creado")
            st.rerun()
        else:
            st.error("⚠️ Complete todos los campos")

    st.markdown("---")
    st.markdown("**✏️ Editar usuario existente:**")
    edit_usr = st.selectbox("Usuario a editar:",
                             [u for u in usuarios.keys() if u != "administrador"],
                             key="edit_usr")
    if edit_usr:
        datos_edit = usuarios[edit_usr]
        ne_label = st.text_input("Nombre:", value=datos_edit.get('label', ''), key="ne_label")
        ne_pass = st.text_input("Nueva contraseña:", value=datos_edit.get('password', ''), key="ne_pass")
        ne_grado = st.selectbox("Grado:", 
                                 ["N/A"] + TODOS_LOS_GRADOS + ["ALL_SECUNDARIA"],
                                 index=0, key="ne_grado")
        if st.button("💾 GUARDAR CAMBIOS", type="primary", key="btn_edit_usr"):
            usuarios[edit_usr]['label'] = ne_label
            usuarios[edit_usr]['password'] = ne_pass
            if ne_grado != "N/A" and datos_edit.get('rol') == 'docente':
                usuarios[edit_usr]['docente_info'] = {
                    'label': ne_label, 'grado': ne_grado,
                    'nivel': datos_edit.get('docente_info', {}).get('nivel', 'PRIMARIA') if datos_edit.get('docente_info') else 'PRIMARIA'
                }
            guardar_usuarios(usuarios)
            st.success(f"✅ {edit_usr} actualizado")
            st.rerun()

    st.markdown("---")
    st.markdown("**🗑️ Eliminar usuario:**")
    del_usr = st.selectbox("Seleccionar:",
                            [u for u in usuarios.keys() if u != "administrador"],
                            key="del_usr")
    if st.button("🗑️ Eliminar", key="btn_del_usr"):
        if del_usr and del_usr != "administrador":
            del usuarios[del_usr]
            guardar_usuarios(usuarios)
            st.success(f"✅ {del_usr} eliminado")
            st.rerun()


# ================================================================
# TAB: MATRÍCULA (Alumnos + Docentes)
# ================================================================

def tab_matricula(config):
    st.header("📝 Matrícula")
    tab_est, tab_doc, tab_lista, tab_pdf = st.tabs([
        "➕ Registrar Alumno", "👨‍🏫 Registrar Docente",
        "📋 Listas", "⬇️ Registros PDF"
    ])

    with tab_est:
        st.subheader("📝 Matrícula de Estudiante")
        c1, c2 = st.columns(2)
        with c1:
            mn = st.text_input("Apellidos y Nombres:", key="mn")
            md = st.text_input("DNI:", key="md", max_chars=8)
            mnv = st.selectbox("Nivel:", list(NIVELES_GRADOS.keys()), key="mnv")
            mg = st.selectbox("Grado:", NIVELES_GRADOS[mnv], key="mg")
            ms = st.selectbox("Sección:", SECCIONES, key="ms")
        with c2:
            msexo = st.selectbox("Sexo:", ["Masculino", "Femenino"], key="msexo")
            ma = st.text_input("Apoderado (Padre/Madre):", key="ma")
            mda = st.text_input("DNI Apoderado:", key="mda", max_chars=8)
            mc = st.text_input("Celular Apoderado:", key="mc", max_chars=9,
                               placeholder="987654321")
        if st.button("✅ MATRICULAR", type="primary", use_container_width=True,
                     key="bm"):
            if mn and md:
                md_clean = ''.join(c for c in md.strip() if c.isdigit())
                if len(md_clean) != 8:
                    st.error(f"⚠️ El DNI debe tener 8 dígitos ({len(md_clean)} encontrados)")
                else:
                    with st.spinner("💾 Guardando matrícula..."):
                        BaseDatos.registrar_estudiante({
                            'Nombre': mn.strip().upper(), 'DNI': md_clean, 'Nivel': mnv,
                            'Grado': mg, 'Seccion': ms, 'Sexo': msexo,
                            'Apoderado': ma.strip(), 'DNI_Apoderado': mda.strip(),
                            'Celular_Apoderado': mc.strip()
                        })
                        time.sleep(2)  # Esperar sincronización con GS
                    # Verificar que se guardó
                    verificar = BaseDatos.buscar_por_dni(md_clean)
                    if verificar:
                        avatar = "👦" if msexo == "Masculino" else "👧"
                        st.success(f"✅ **MATRICULADO CORRECTAMENTE** ☁️ Guardado en la nube")
                        st.markdown(f"""
                        <div class="asist-ok">
                            <strong>📋 Confirmación de Matrícula</strong><br>
                            {avatar} {mn.strip().upper()}<br>
                            🆔 DNI: {md_clean}<br>
                            🎓 {mg} — Sección {ms}<br>
                            📅 {fecha_peru_str()}<br>
                            <span style="color:green;font-weight:bold;">☑️ VERIFICADO EN BASE DE DATOS</span>
                        </div>
                        """, unsafe_allow_html=True)
                        reproducir_beep_exitoso()
                        st.balloons()
                    else:
                        st.warning("⚠️ Se intentó guardar pero no se pudo verificar. Revise en la lista.")
            else:
                st.error("⚠️ Nombre y DNI son obligatorios")

    with tab_doc:
        st.subheader("👨‍🏫 Registro de Docente / Personal")
        c1, c2 = st.columns(2)
        with c1:
            dn_n = st.text_input("👤 Apellidos y Nombres:", key="dn_nom")
            dn_d = st.text_input("🆔 DNI:", key="dn_dni", max_chars=8)
            dn_c = st.selectbox("💼 Cargo:", [
                "Docente", "Directora", "Auxiliar", "Coordinador",
                "Secretaria", "Personal de Limpieza", "Otro"
            ], key="dn_cargo")
            dn_e = st.text_input("📚 Especialidad:", key="dn_esp",
                                  placeholder="Ej: Educación Primaria")
        with c2:
            dn_t = st.text_input("📱 Celular:", key="dn_cel", max_chars=9,
                                  placeholder="987654321")
            dn_nivel = st.selectbox("🏫 Nivel:", 
                                     ["INICIAL", "PRIMARIA", "SECUNDARIA", "PREUNIVERSITARIO"],
                                     key="dn_nivel_reg")
            if dn_nivel in ["INICIAL", "PRIMARIA"]:
                dn_g = st.selectbox("🎓 Grado Asignado:",
                                     ["N/A"] + NIVELES_GRADOS.get(dn_nivel, []),
                                     key="dn_grado")
                dn_areas_sel = ""
            else:
                # Secundaria/PreU: seleccionar grados/grupos donde enseña
                opciones_asig = NIVELES_GRADOS.get(dn_nivel, []) + ["ALL_SECUNDARIA"]
                dn_g = st.selectbox("🎓 Grado/Grupo:",
                                     ["N/A"] + opciones_asig, key="dn_grado")
                # Áreas que enseña
                todas_areas = AREAS_MINEDU.get(dn_nivel, [])
                if dn_nivel == "PREUNIVERSITARIO":
                    todas_areas = list(set(
                        AREAS_CEPRE_UNSAAC.get('GRUPO AB', []) +
                        AREAS_CEPRE_UNSAAC.get('GRUPO CD', [])
                    ))
                dn_areas_sel = st.multiselect("📚 Áreas que enseña:", 
                                               todas_areas, key="dn_areas_reg")
            dn_email = st.text_input("📧 Email:", key="dn_email",
                                      placeholder="nombre@ieyachay.org")
            dn_foto = st.file_uploader("📸 Foto:", type=['jpg', 'png', 'jpeg'],
                                        key="dn_foto")
            if dn_foto:
                st.image(dn_foto, width=120)
            # Opción para crear cuenta de acceso
            crear_cuenta = st.checkbox("🔐 Crear cuenta de acceso al sistema", value=True, key="crear_cuenta_doc")
            if crear_cuenta:
                cc1, cc2 = st.columns(2)
                with cc1:
                    dn_usuario = st.text_input("👤 Usuario:", 
                                                value=dn_n.strip().lower().replace(' ', '.').split('.')[0] if dn_n else '',
                                                key="dn_usuario_auto",
                                                placeholder="ej: prof.matematica")
                with cc2:
                    dn_password = st.text_input("🔑 Contraseña:", 
                                                 value=dn_d.strip() if dn_d else '',
                                                 key="dn_pass_auto",
                                                 placeholder="DNI por defecto")

        if st.button("✅ REGISTRAR DOCENTE", type="primary",
                     use_container_width=True, key="bd"):
            if dn_n and dn_d:
                if dn_foto:
                    foto_path = f"foto_doc_{dn_d.strip()}.png"
                    with open(foto_path, "wb") as fout:
                        fout.write(dn_foto.getbuffer())
                areas_txt = ', '.join(dn_areas_sel) if dn_areas_sel else dn_e.strip()
                BaseDatos.registrar_docente({
                    'Nombre': dn_n.strip().upper(), 'DNI': dn_d.strip(),
                    'Cargo': dn_c, 'Especialidad': areas_txt,
                    'Celular': dn_t.strip(), 'Grado_Asignado': dn_g,
                    'Email': dn_email.strip(), 'Nivel': dn_nivel,
                    'Areas': areas_txt
                })
                st.success(f"✅ {dn_n} registrado como {dn_c}")
                
                # Auto-crear cuenta de usuario
                if crear_cuenta and dn_usuario and dn_password:
                    usuarios = cargar_usuarios()
                    u_key = dn_usuario.strip().lower()
                    di = {"label": dn_n.strip().upper(), "grado": dn_g, "nivel": dn_nivel}
                    usuarios[u_key] = {
                        "password": dn_password,
                        "rol": "docente" if dn_c == "Docente" else ("auxiliar" if dn_c == "Auxiliar" else "directivo"),
                        "label": dn_n.strip().upper(),
                        "docente_info": di,
                        "grado": dn_g,
                        "nivel": dn_nivel,
                    }
                    guardar_usuarios(usuarios)
                    st.success(f"🔐 Cuenta creada: **{u_key}** / contraseña: **{dn_password}**")
                
                if dn_areas_sel:
                    st.info(f"📚 Áreas: {areas_txt}")
                reproducir_beep_exitoso()
                st.balloons()
            else:
                st.error("⚠️ Nombre y DNI requeridos")

    with tab_lista:
        st.subheader("📚 Alumnos Matriculados")
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
                bq = st.text_input("🔍 Buscar:", key="bq")
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
            # Solo admin puede eliminar
            if puede_borrar():
                with st.expander("🗑️ Eliminar Alumno"):
                    deld = st.text_input("DNI a eliminar:", key="dd")
                    if st.button("🗑️ Eliminar", key="bdel"):
                        if deld:
                            BaseDatos.eliminar_estudiante(deld)
                            st.rerun()
        else:
            st.info("📝 Sin alumnos matriculados.")

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
            if puede_borrar():
                with st.expander("🗑️ Eliminar Docente"):
                    deld2 = st.text_input("DNI:", key="dddoc")
                    if st.button("🗑️ Eliminar", key="bdeldoc"):
                        if deld2:
                            BaseDatos.eliminar_docente(deld2)
                            st.rerun()
        else:
            st.info("📝 Sin docentes registrados.")

    with tab_pdf:
        _seccion_registros_pdf(config)


def _seccion_registros_pdf(config):
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
    st.caption(f"{len(cursos)} cursos × 4 competencias × 3 desempeños")
    if st.button("📝 Generar Registro Auxiliar PDF", type="primary",
                 use_container_width=True, key="gra"):
        sl = sp if sp != "Todas" else "Todas"
        pdf = generar_registro_auxiliar_pdf(gp, sl, config['anio'], bim, dg, cursos)
        st.download_button("⬇️ Descargar Registro Auxiliar", pdf,
                           f"RegAux_{gp}_{bim}.pdf", "application/pdf", key="dra")

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
                               f"RegAsist_{gp}.pdf", "application/pdf", key="dras")


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
        db = st.text_input("🔍 Buscar DNI:", key="db")
        if st.button("🔎 Buscar", use_container_width=True, key="bb"):
            r = BaseDatos.buscar_por_dni(db)
            if r:
                st.session_state.alumno = r.get('Nombre', '')
                st.session_state.dni = r.get('DNI', '')
                st.session_state.grado = r.get('Grado', '')
                st.session_state.apoderado = r.get('Apoderado', '')
                st.session_state.dni_apo = r.get('DNI_Apoderado', '')
                st.success("✅ Datos cargados")
                st.rerun()
            else:
                st.error("❌ No encontrado")
    with c2:
        with st.container(border=True):
            nm = st.text_input("👤 Estudiante:", key="alumno")
            dn = st.text_input("🆔 DNI Estudiante:", key="dni")
            gr = st.text_input("📚 Grado:", key="grado")
            ap = st.text_input("👨‍👩‍👧 Padre/Madre/Apoderado:", key="apoderado")
            da = st.text_input("🆔 DNI Padre/Madre/Apoderado:", key="dni_apo")
            nc = {}
            if td == "CONSTANCIA DE CONDUCTA":
                cols = st.columns(5)
                for i, col in enumerate(cols):
                    with col:
                        nc[f'nota_conducta_{i+1}'] = st.selectbox(
                            f"{i+1}°", ["AD", "A", "B", "C"], key=f"n{i}")
            ex = {}
            if td == "RESOLUCIÓN DE TRASLADO":
                ex['num_resolucion'] = st.text_input("N° Resolución:", key="nr")
                ex['fecha_resolucion'] = st.text_input("Fecha:", key="fr2")
                ex['nivel'] = st.selectbox("Nivel:",
                                           ["INICIAL", "PRIMARIA", "SECUNDARIA"],
                                           key="nl")
                ex['ie_destino'] = st.text_input("IE Destino:", key="ie")
        if st.button("✨ GENERAR DOCUMENTO", type="primary",
                     use_container_width=True, key="gd"):
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
                st.success("✅ Documento generado")
                st.download_button("⬇️ Descargar PDF", pdf,
                                   f"{nm}_{td}.pdf", "application/pdf",
                                   use_container_width=True, key="dd2")


# ================================================================
# TAB: CARNETS (Individual, Matrícula, Lote Alumnos PDF, Lote Docentes PDF)
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
        if st.button("🪪 GENERAR CARNET", type="primary",
                     use_container_width=True, key="gc"):
            if cn and cd:
                fi = io.BytesIO(cf.getvalue()) if cf else None
                cr = GeneradorCarnet(
                    {'Nombre': cn, 'DNI': cd, 'Grado': cg, 'Seccion': cs},
                    config['anio'], fi
                ).generar()
                st.image(cr, use_container_width=True)
                st.download_button("⬇️ Descargar", cr,
                                   f"Carnet_{cn.replace(' ', '_')}.png",
                                   "image/png", use_container_width=True, key="dc")

    with t2:
        dbs = st.text_input("🔍 DNI:", key="cbd")
        if st.button("🔎 Buscar", key="cbb"):
            a = BaseDatos.buscar_por_dni(dbs)
            if a:
                st.session_state['ce'] = a
                st.success(f"✅ {a.get('Nombre', '')}")
            else:
                st.error("❌ No encontrado")
        if st.session_state.get('ce') and isinstance(st.session_state['ce'], dict):
            a = st.session_state['ce']
            es_d = a.get('_tipo', '') == 'docente'
            tt = "DOCENTE" if es_d else "ALUMNO"
            st.markdown(f"**[{tt}]** {a.get('Nombre', '')} | DNI: {a.get('DNI', '')}")
            fm = st.file_uploader("📸 Foto:", type=['jpg', 'png', 'jpeg'], key="cfm")
            if st.button("🪪 GENERAR", type="primary",
                         use_container_width=True, key="gcm"):
                fi = io.BytesIO(fm.getvalue()) if fm else None
                cr = GeneradorCarnet(a, config['anio'], fi, es_docente=es_d).generar()
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
                lista = d.to_dict('records')
                pdf = generar_carnets_lote_pdf(lista, config['anio'], es_docente=False)
                progreso.progress(100)
                st.balloons()
                st.download_button("⬇️ DESCARGAR PDF", pdf,
                                   f"Carnets_Alumnos_{config['anio']}.pdf",
                                   "application/pdf", use_container_width=True,
                                   key="dlz")
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
                pdf = generar_carnets_lote_pdf(lista, config['anio'], es_docente=True)
                st.balloons()
                st.download_button("⬇️ DESCARGAR PDF", pdf,
                                   f"Carnets_Docentes_{config['anio']}.pdf",
                                   "application/pdf", use_container_width=True,
                                   key="dlzd")
        else:
            st.info("📝 Registra docentes en Matrícula.")


# ================================================================
# TAB: ASISTENCIAS (Alumnos + Docentes)
# ================================================================

def tab_asistencias():
    st.header("📋 Control de Asistencia")
    st.caption(f"🕒 **{hora_peru().strftime('%H:%M:%S')}** | "
               f"📅 {hora_peru().strftime('%d/%m/%Y')}")

    # Inicializar tracking de WhatsApp enviados
    if 'wa_enviados' not in st.session_state:
        st.session_state.wa_enviados = set()

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
            f"Registre todos los alumnos/docentes. "
            f"Luego envíe WhatsApp desde la lista de abajo.")
    st.markdown("---")

    # ===== ZONA DE REGISTRO RÁPIDO =====
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
                    _registrar_asistencia_rapida(d)
                else:
                    st.warning("⚠️ QR no detectado.")
        else:
            st.info("💡 Activa la cámara para escanear.")
    with cm:
        st.markdown("### ✏️ Registro Manual / Lector de Código de Barras")
        st.caption("💡 Con lector de barras: apunte al carnet y se registra automáticamente")
        
        # Auto-registro: cuando cambia el valor se registra
        dm = st.text_input("DNI:", key="dm",
                           placeholder="Escanee código de barras o escriba DNI + Enter")
        
        # Auto-registro si hay valor (el lector envía Enter automáticamente)
        if dm and dm.strip() and len(dm.strip()) >= 8:
            dni_limpio = ''.join(c for c in dm.strip() if c.isdigit())
            if len(dni_limpio) == 8:
                _registrar_asistencia_rapida(dni_limpio)
                # JavaScript para vibrar en celular y sonar
                st.markdown("""
                <script>
                    if ('vibrate' in navigator) { navigator.vibrate([200, 100, 200]); }
                    try {
                        var ctx = new (window.AudioContext || window.webkitAudioContext)();
                        var o = ctx.createOscillator();
                        o.type = 'sine'; o.frequency.value = 800;
                        o.connect(ctx.destination);
                        o.start(); setTimeout(function(){ o.stop(); }, 200);
                    } catch(e) {}
                </script>
                """, unsafe_allow_html=True)
        elif dm and dm.strip():
            if st.button("✅ REGISTRAR", type="primary",
                         use_container_width=True, key="rm"):
                _registrar_asistencia_rapida(dm.strip())

    # ===== LISTA DE ASISTENCIA DE HOY =====
    st.markdown("---")
    st.subheader("📊 Registros de Hoy")
    asis = BaseDatos.obtener_asistencias_hoy()
    if asis:
        # Separar alumnos y docentes
        alumnos_h = []
        docentes_h = []
        for dk, v in asis.items():
            reg = {'DNI': dk, 'Nombre': v['nombre'],
                   'Entrada': v.get('entrada', '—'),
                   'Salida': v.get('salida', '—'),
                   'es_docente': v.get('es_docente', False)}
            if v.get('es_docente', False):
                docentes_h.append(reg)
            else:
                alumnos_h.append(reg)

        # Métricas rápidas
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("📚 Alumnos", len(alumnos_h))
        with c2:
            st.metric("👨‍🏫 Docentes", len(docentes_h))
        with c3:
            entradas = sum(1 for v in asis.values() if v.get('entrada'))
            st.metric("🌅 Entradas", entradas)
        with c4:
            salidas = sum(1 for v in asis.values() if v.get('salida'))
            st.metric("🌙 Salidas", salidas)

        if alumnos_h:
            st.markdown("**📚 Alumnos registrados:**")
            st.dataframe(pd.DataFrame(alumnos_h).drop(columns=['es_docente']),
                         use_container_width=True, hide_index=True)
        if docentes_h:
            st.markdown("**👨‍🏫 Docentes registrados:**")
            st.dataframe(pd.DataFrame(docentes_h).drop(columns=['es_docente']),
                         use_container_width=True, hide_index=True)

        # ===== ZONA WHATSAPP — ENVÍO MASIVO =====
        st.markdown("---")
        st.subheader("📱 Enviar Notificaciones WhatsApp")
        st.caption("Toque cada botón para enviar. Al enviar se marca como ✅")

        tipo_actual = st.session_state.tipo_asistencia.lower()
        pendientes = 0
        enviados = 0

        for dk, dat in asis.items():
            # Verificar si ya fue enviado
            clave_envio = f"{dk}_{tipo_actual}_{fecha_peru_str()}"
            ya_enviado = clave_envio in st.session_state.wa_enviados

            # Buscar celular
            al = BaseDatos.buscar_por_dni(dk)
            if not al:
                continue
            cel = str(al.get('Celular_Apoderado', al.get('Celular', ''))).strip()
            if not cel or cel == 'None' or cel == 'nan':
                continue

            hora_reg = dat.get(tipo_actual, '')
            if not hora_reg:
                continue

            nombre = dat['nombre']
            es_doc = dat.get('es_docente', False)
            tipo_icon = "👨‍🏫" if es_doc else "📚"

            if ya_enviado:
                enviados += 1
                st.markdown(
                    f"✅ ~~{tipo_icon} {nombre} — {hora_reg} → {cel}~~ "
                    f"*(enviado)*")
            else:
                pendientes += 1
                msg = generar_mensaje_asistencia(nombre, tipo_actual, hora_reg)
                link = generar_link_whatsapp(cel, msg)
                col_btn, col_check = st.columns([4, 1])
                with col_btn:
                    st.markdown(
                        f'<a href="{link}" target="_blank" class="wa-btn">'
                        f'📱 {tipo_icon} {nombre} — 🕒 {hora_reg} → {cel}</a>',
                        unsafe_allow_html=True)
                with col_check:
                    if st.button("✅", key=f"wa_{dk}_{tipo_actual}",
                                 help="Marcar como enviado"):
                        st.session_state.wa_enviados.add(clave_envio)
                        st.rerun()

        if pendientes == 0 and enviados > 0:
            st.success(f"🎉 ¡Todos los WhatsApp enviados! ({enviados} mensajes)")
        elif pendientes > 0:
            st.info(f"📱 {pendientes} pendientes | ✅ {enviados} enviados")

        # Botón para resetear marcas de enviado
        if enviados > 0:
            if st.button("🔄 Resetear marcas de enviado",
                         key="reset_wa"):
                st.session_state.wa_enviados = set()
                st.rerun()

        st.markdown("---")
        # Solo admin puede borrar
        if puede_borrar():
            if st.button("🗑️ BORRAR ASISTENCIAS DEL DÍA", type="secondary",
                         use_container_width=True, key="borrar_asist"):
                BaseDatos.borrar_asistencias_hoy()
                st.session_state.wa_enviados = set()
                st.success("✅ Eliminadas")
                st.rerun()
    else:
        st.info("📝 No hay registros hoy. Escanee QR o ingrese DNI para registrar.")


def _registrar_asistencia_rapida(dni):
    """Registra asistencia RÁPIDO sin enviar WhatsApp (se envía después)"""
    persona = BaseDatos.buscar_por_dni(dni)
    if persona:
        hora = hora_peru_str()
        tipo = st.session_state.tipo_asistencia.lower()
        nombre = persona.get('Nombre', '')
        es_d = persona.get('_tipo', '') == 'docente'
        tp = "👨‍🏫 DOCENTE" if es_d else "📚 ALUMNO"
        BaseDatos.guardar_asistencia(dni, nombre, tipo, hora, es_docente=es_d)
        emoji_tipo = "🟢" if tipo == "entrada" else "🟡"
        st.markdown(f"""<div class="asist-{'ok' if tipo == 'entrada' else 'salida'}">
            {emoji_tipo} <strong>[{tp}] {nombre}</strong> — {st.session_state.tipo_asistencia}: <strong>{hora}</strong>
        </div>""", unsafe_allow_html=True)
        reproducir_beep_exitoso()
    else:
        st.error(f"❌ DNI {dni} no encontrado en el sistema")
        reproducir_beep_error()


# ================================================================
# TAB: CALIFICACIÓN YACHAY — RANKING POR DOCENTE
# Cada docente ve SOLO su ranking. Selección de alumno por lista.
# Grid estilo ZipGrade + Guardar Evaluaciones + Reportes individuales
# ================================================================

ESCALA_MINEDU = {
    'AD': {'min': 18, 'max': 20, 'nombre': 'Logro Destacado', 'color': '#16a34a',
           'desc': 'El estudiante evidencia un nivel superior a lo esperado. Maneja solventemente las situaciones propuestas.'},
    'A': {'min': 14, 'max': 17, 'nombre': 'Logro Previsto', 'color': '#2563eb',
          'desc': 'El estudiante evidencia el logro de los aprendizajes previstos en el tiempo programado.'},
    'B': {'min': 11, 'max': 13, 'nombre': 'En Proceso', 'color': '#f59e0b',
          'desc': 'El estudiante está en camino de lograr los aprendizajes previstos. Requiere acompañamiento durante un tiempo razonable.'},
    'C': {'min': 0, 'max': 10, 'nombre': 'En Inicio', 'color': '#dc2626',
          'desc': 'El estudiante está empezando a desarrollar los aprendizajes previstos. Necesita mayor tiempo de acompañamiento e intervención del docente.'},
}

def nota_a_letra(nota):
    if nota >= 18: return 'AD'
    elif nota >= 14: return 'A'
    elif nota >= 11: return 'B'
    else: return 'C'

def color_semaforo(letra):
    return ESCALA_MINEDU.get(letra, {}).get('color', '#888')

def generar_reporte_estudiante_pdf(nombre, dni, grado, resultados_hist, config):
    """PDF individual del estudiante con semáforo AD/A/B/C y recomendaciones"""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    
    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w/2, h-50, "INFORME ACADÉMICO INDIVIDUAL")
    c.setFont("Helvetica", 10)
    c.drawCentredString(w/2, h-68, f"I.E.P. ALTERNATIVO YACHAY — {config.get('anio', 2026)}")
    
    c.setFont("Helvetica-Bold", 12)
    y = h - 100
    c.drawString(50, y, f"Estudiante: {nombre}")
    c.drawString(350, y, f"DNI: {dni}")
    y -= 20
    c.drawString(50, y, f"Grado: {grado}")
    c.drawString(350, y, f"Fecha: {fecha_peru_str()}")
    y -= 15
    c.setStrokeColor(colors.HexColor("#1a56db"))
    c.setLineWidth(2)
    c.line(50, y, w-50, y)
    y -= 25
    
    if not resultados_hist:
        c.setFont("Helvetica", 12)
        c.drawString(50, y, "Sin evaluaciones registradas.")
        c.save()
        buf.seek(0)
        return buf
    
    # Tabla de evaluaciones
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "HISTORIAL DE EVALUACIONES")
    y -= 20
    
    # Headers
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#1a56db"))
    c.rect(50, y-2, w-100, 16, fill=True)
    c.setFillColor(colors.white)
    cols_x = [55, 140, 250, 340, 400, 460, 520]
    headers = ["Fecha", "Evaluación", "Área", "Nota", "Literal", "Estado", ""]
    for i, hd in enumerate(headers[:6]):
        c.drawString(cols_x[i], y+2, hd)
    y -= 18
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 7)
    promedios_areas = {}
    total_general = []
    
    for r in resultados_hist:
        for area in r.get('areas', []):
            nota = area.get('nota', 0)
            letra = nota_a_letra(nota)
            col = color_semaforo(letra)
            nombre_area = area.get('nombre', '')
            
            # Acumular para estadísticas
            if nombre_area not in promedios_areas:
                promedios_areas[nombre_area] = []
            promedios_areas[nombre_area].append(nota)
            total_general.append(nota)
            
            c.drawString(cols_x[0], y, str(r.get('fecha', ''))[:10])
            c.drawString(cols_x[1], y, str(r.get('titulo', 'Evaluación'))[:18])
            c.drawString(cols_x[2], y, nombre_area[:15])
            c.drawString(cols_x[3], y, f"{nota}/20")
            c.drawString(cols_x[4], y, letra)
            
            # Semáforo de color
            c.setFillColor(colors.HexColor(col))
            c.circle(cols_x[5]+15, y+3, 5, fill=True)
            c.setFillColor(colors.black)
            
            y -= 14
            if y < 120:
                c.showPage()
                y = h - 60
                c.setFont("Helvetica", 7)
    
    # Resumen estadístico
    y -= 15
    if y < 200:
        c.showPage()
        y = h - 60
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "RESUMEN POR ÁREAS")
    y -= 20
    
    for area_nombre, notas in promedios_areas.items():
        prom = round(sum(notas) / len(notas), 1)
        letra = nota_a_letra(prom)
        col = color_semaforo(letra)
        
        c.setFont("Helvetica-Bold", 9)
        c.drawString(55, y, f"{area_nombre}:")
        c.drawString(200, y, f"Promedio: {prom}/20")
        c.drawString(310, y, f"({letra} — {ESCALA_MINEDU[letra]['nombre']})")
        
        # Barra visual
        c.setFillColor(colors.HexColor("#e2e8f0"))
        c.rect(420, y-2, 120, 12, fill=True)
        c.setFillColor(colors.HexColor(col))
        c.rect(420, y-2, (prom/20)*120, 12, fill=True)
        c.setFillColor(colors.black)
        y -= 18
    
    # Promedio General
    if total_general:
        prom_gen = round(sum(total_general) / len(total_general), 1)
        letra_gen = nota_a_letra(prom_gen)
        y -= 10
        c.setFont("Helvetica-Bold", 13)
        c.drawString(55, y, f"PROMEDIO GENERAL: {prom_gen}/20 ({letra_gen})")
        
        # Semáforo grande
        col_gen = color_semaforo(letra_gen)
        c.setFillColor(colors.HexColor(col_gen))
        c.circle(430, y+5, 12, fill=True)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(430, y+1, letra_gen)
        c.setFillColor(colors.black)
    
    # Recomendaciones pedagógicas
    y -= 35
    if y < 180:
        c.showPage()
        y = h - 60
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "RECOMENDACIONES PEDAGÓGICAS Y PSICOLÓGICAS")
    y -= 18
    c.setFont("Helvetica", 8)
    
    if total_general:
        letra_gen = nota_a_letra(prom_gen)
        desc = ESCALA_MINEDU[letra_gen]['desc']
        c.drawString(55, y, f"• Nivel actual: {desc}")
        y -= 14
        
        if letra_gen == 'AD':
            recs = [
                "Excelente desempeño. Mantener el ritmo y motivar con retos académicos mayores.",
                "Se recomienda participación en concursos académicos y olimpiadas.",
                "Fomentar el liderazgo y tutoría entre pares.",
            ]
        elif letra_gen == 'A':
            recs = [
                "Buen rendimiento. Reforzar áreas con menor puntaje para alcanzar el nivel destacado.",
                "Establecer metas semanales de estudio con apoyo familiar.",
                "Incentivar hábitos de lectura diaria de 30 minutos.",
            ]
        elif letra_gen == 'B':
            recs = [
                "En proceso de logro. Requiere acompañamiento adicional del docente y familia.",
                "Se sugiere sesiones de refuerzo en las áreas con menor calificación.",
                "Establecer un horario de estudio fijo en casa con supervisión.",
                "Diálogo constante entre padres y docentes sobre avances.",
            ]
        else:
            recs = [
                "Necesita apoyo inmediato. Coordinar con el docente un plan de recuperación.",
                "Se recomienda evaluación psicopedagógica para identificar dificultades.",
                "Sesiones de refuerzo diarias con material adaptado a su ritmo.",
                "Reunión urgente con padres para establecer compromisos.",
                "Considerar apoyo emocional si hay factores externos que afectan el aprendizaje.",
            ]
        for rec in recs:
            c.drawString(55, y, f"• {rec}")
            y -= 12
    
    # Escala de calificación
    y -= 20
    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "ESCALA DE CALIFICACIÓN MINEDU:")
    y -= 14
    c.setFont("Helvetica", 7)
    for sigla, info in ESCALA_MINEDU.items():
        c.setFillColor(colors.HexColor(info['color']))
        c.circle(60, y+3, 4, fill=True)
        c.setFillColor(colors.black)
        c.drawString(70, y, f"{sigla} ({info['min']}-{info['max']}): {info['nombre']}")
        y -= 12
    
    # Pie
    c.setFont("Helvetica-Oblique", 7)
    c.drawCentredString(w/2, 30, f"YACHAY PRO — Sistema de Gestión Educativa © {hora_peru().year}")
    
    c.save()
    buf.seek(0)
    return buf


def tab_calificacion_yachay(config):
    st.header("📝 Sistema de Calificación YACHAY")
    usuario_actual = st.session_state.usuario_actual

    tabs_cal = st.tabs([
        "🔑 Crear Claves", "📄 Hoja de Respuestas",
        "✅ Calificar", "🏆 Ranking", "📊 Historial"
    ])

    titulo_eval = "Evaluación"  # Default

    # ===== TAB: CREAR CLAVES (Grid estilo ZipGrade) =====
    with tabs_cal[0]:
        st.subheader("🔑 Crear Claves de Evaluación")
        st.markdown("Marque la alternativa correcta para cada pregunta:")

        ec1, ec2 = st.columns(2)
        with ec1:
            titulo_eval = st.text_input("📝 Nombre de la evaluación:",
                                         "Evaluación Bimestral", key="tit_eval")
        with ec2:
            num_areas = st.number_input("Número de áreas:", 1, 6, 1, key="num_areas_grid")

        areas_grid = []
        total_preguntas = 0
        for a_idx in range(int(num_areas)):
            st.markdown(f"---")
            ac1, ac2 = st.columns([2, 1])
            with ac1:
                area_nom = st.text_input(f"Área {a_idx+1}:", key=f"area_nom_{a_idx}",
                                          value=["Matemática", "Comunicación",
                                                 "Ciencia y Tec.", "Personal Social",
                                                 "Arte y Cultura", "Ed. Física"][a_idx]
                                          if a_idx < 6 else f"Área {a_idx+1}")
            with ac2:
                area_num = st.selectbox(f"Preguntas:",
                                         [5, 10, 15, 20, 25],
                                         index=1, key=f"area_num_{a_idx}")

            # Grid de alternativas
            claves_area = []
            cols_header = st.columns([1, 1, 1, 1, 1])
            with cols_header[0]:
                st.markdown("**#**")
            for opt_idx, opt in enumerate(['A', 'B', 'C', 'D']):
                with cols_header[opt_idx + 1]:
                    st.markdown(f"**{opt}**")

            for p in range(int(area_num)):
                p_global = total_preguntas + p + 1
                resp = st.radio(
                    f"P{p_global}",
                    ['A', 'B', 'C', 'D'],
                    horizontal=True,
                    key=f"grid_{a_idx}_{p}",
                    label_visibility="collapsed" if p > 0 else "visible"
                )
                claves_area.append(resp)

            areas_grid.append({
                'nombre': area_nom,
                'num': int(area_num),
                'claves': claves_area
            })
            total_preguntas += int(area_num)

        st.markdown("---")
        st.info(f"📊 Total: **{total_preguntas} preguntas** en **{len(areas_grid)} áreas**")

        # Resumen visual de claves
        if areas_grid:
            resumen = ""
            for ag in areas_grid:
                resumen += f"**{ag['nombre']}:** {''.join(ag['claves'])}\n\n"
            st.markdown(resumen)

        # Guardar evaluación
        if st.button("💾 GUARDAR EVALUACIÓN", type="primary",
                     use_container_width=True, key="guardar_eval"):
            if titulo_eval:
                eval_data = {
                    'titulo': titulo_eval,
                    'fecha': fecha_peru_str(),
                    'hora': hora_peru_str(),
                    'usuario': usuario_actual,
                    'areas': areas_grid,
                    'total_preguntas': total_preguntas
                }
                # Guardar en session_state
                if 'evaluaciones_guardadas' not in st.session_state:
                    st.session_state.evaluaciones_guardadas = {}
                eval_key = f"{titulo_eval}_{fecha_peru_str()}"
                st.session_state.evaluaciones_guardadas[eval_key] = eval_data

                # Guardar en Google Sheets
                gs = _gs()
                if gs:
                    try:
                        ws = gs._get_hoja('config')
                        if ws:
                            ws.append_row([
                                f"eval_{eval_key}",
                                json.dumps(eval_data, ensure_ascii=False, default=str)
                            ])
                    except Exception:
                        pass

                st.success(f"✅ Evaluación **'{titulo_eval}'** guardada exitosamente")
                st.markdown(f"**Claves:** {total_preguntas} preguntas en {len(areas_grid)} áreas")
                reproducir_beep_exitoso()
            else:
                st.error("⚠️ Ingrese un nombre para la evaluación")

    # ===== TAB: HOJA DE RESPUESTAS =====
    with tabs_cal[1]:
        st.subheader("📄 Hoja de Respuestas")
        c1, c2 = st.columns(2)
        with c1:
            npg = st.selectbox("Preguntas:", [10, 20, 30, 40, 50],
                               index=1, key="npg")
        with c2:
            th = st.text_input("Título:", "EVALUACIÓN BIMESTRAL", key="th")
        
        if st.button("📄 GENERAR HOJA DE RESPUESTAS PDF", type="primary",
                     use_container_width=True, key="gh"):
            hoja_bio = generar_hoja_respuestas(npg, th)
            hoja_bytes = hoja_bio.getvalue()
            
            # Vista previa
            st.image(hoja_bytes, use_container_width=True)
            
            # Siempre generar PDF con 2 hojas por página
            try:
                from PIL import Image as PILImage
                img_pil = PILImage.open(io.BytesIO(hoja_bytes))
                img_w, img_h = img_pil.size
                
                pdf_buf = io.BytesIO()
                page_size = (595.27, 841.89)  # A4 en puntos
                c_pdf = canvas.Canvas(pdf_buf, pagesize=page_size)
                w_page, h_page = page_size
                
                img_path = "/tmp/hoja_temp.png"
                img_pil.save(img_path)
                
                # 2 hojas por página con línea de corte
                half_h = h_page / 2
                scale = min(w_page / img_w, half_h / img_h) * 0.88
                draw_w = img_w * scale
                draw_h = img_h * scale
                x_offset = (w_page - draw_w) / 2
                
                # Hoja superior
                c_pdf.drawImage(img_path, x_offset, half_h + 8,
                                width=draw_w, height=draw_h)
                # Línea de corte
                c_pdf.setStrokeColor(colors.gray)
                c_pdf.setLineWidth(0.5)
                c_pdf.setDash(6, 3)
                c_pdf.line(15, half_h, w_page - 15, half_h)
                c_pdf.setFont("Helvetica", 6)
                c_pdf.drawCentredString(w_page/2, half_h - 8,
                                        "--- CORTAR AQUI ---")
                c_pdf.setDash()
                
                # Hoja inferior
                c_pdf.drawImage(img_path, x_offset, 8,
                                width=draw_w, height=draw_h)
                
                c_pdf.save()
                pdf_buf.seek(0)
                st.download_button("📥 DESCARGAR PDF (2 hojas por página)",
                                   pdf_buf.getvalue(),
                                   f"Hojas_Respuesta_{npg}p.pdf",
                                   "application/pdf",
                                   use_container_width=True, key="dh_pdf")
                st.success("✅ PDF generado con 2 hojas de respuesta por página")
            except Exception as e:
                st.error(f"Error generando PDF: {e}")
                # Fallback: descargar PNG
                st.download_button("⬇️ Descargar PNG", hoja_bytes,
                                   f"Hoja_{npg}p.png", "image/png", key="dh_png")

    # ===== TAB: CALIFICAR =====
    with tabs_cal[2]:
        st.subheader("✅ Calificar Examen")

        # Cargar evaluación guardada o crear nueva
        modo_cal = st.radio("Modo:", [
            "📂 Evaluación Guardada",
            "✏️ Claves Manuales",
            "⚡ Evaluación Rápida (solo nombres)"
        ], key="modo_cal")

        ia = []
        tc_ = []
        tp = 0

        if modo_cal == "📂 Evaluación Guardada":
            # Cargar de Google Sheets
            evals_disp = {}
            gs = _gs()
            if gs:
                try:
                    ws = gs._get_hoja('config')
                    if ws:
                        data = ws.get_all_records()
                        for d in data:
                            clave = str(d.get('clave', ''))
                            if clave.startswith('eval_'):
                                try:
                                    evals_disp[clave[5:]] = json.loads(d.get('valor', '{}'))
                                except Exception:
                                    pass
                except Exception:
                    pass

            # Agregar de session_state
            for k, v in st.session_state.get('evaluaciones_guardadas', {}).items():
                if k not in evals_disp:
                    evals_disp[k] = v

            if evals_disp:
                sel_eval = st.selectbox("Seleccionar evaluación:",
                                         list(evals_disp.keys()), key="sel_eval_cal")
                if sel_eval:
                    ev = evals_disp[sel_eval]
                    st.success(f"📝 **{ev.get('titulo', sel_eval)}** — "
                              f"{ev.get('total_preguntas', 0)} preguntas")
                    for a in ev.get('areas', []):
                        claves_list = a.get('claves', [])
                        ia.append({
                            'nombre': a['nombre'],
                            'num': a['num'],
                            'claves': claves_list
                        })
                        tc_.extend(claves_list)
                        tp += a['num']
            else:
                st.warning("No hay evaluaciones guardadas. Cree una en la pestaña 🔑 Crear Claves.")

        elif modo_cal == "✏️ Claves Manuales":
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
                if st.button("➕ Agregar", key="aa"):
                    if na:
                        st.session_state.areas_examen.append({
                            'nombre': na, 'num': nn, 'claves': ''})
                        st.rerun()

            for i, a in enumerate(st.session_state.areas_examen):
                with st.expander(f"📚 {a['nombre']} ({a['num']}p)", expanded=True):
                    cl = st.text_input("Claves (ej: ABCDABCDAB):",
                                       value=a.get('claves', ''),
                                       key=f"cl{i}", max_chars=a['num'])
                    st.session_state.areas_examen[i]['claves'] = cl.upper()
                    ia.append({'nombre': a['nombre'], 'num': a['num'],
                               'claves': list(cl.upper())})
                    tc_.extend(list(cl.upper()))
                    tp += a['num']
                    if len(st.session_state.areas_examen) > 1:
                        if st.button("🗑️ Quitar", key=f"d{i}"):
                            st.session_state.areas_examen.pop(i)
                            st.rerun()

        else:  # Evaluación Rápida
            st.info("⚡ En este modo solo ingresa nombre del estudiante (sin DNI)")

            ca, cn_, cb = st.columns([2, 1, 1])
            with ca:
                na = st.text_input("Área:", key="na_r")
            with cn_:
                nn = st.selectbox("Preguntas:", [5, 10, 15, 20, 25, 30],
                                  index=1, key="nn_r")
            with cb:
                st.markdown("###")
                if st.button("➕ Agregar", key="aa_r"):
                    if na:
                        st.session_state.areas_examen.append({
                            'nombre': na, 'num': nn, 'claves': ''})
                        st.rerun()

            for i, a in enumerate(st.session_state.get('areas_examen', [])):
                with st.expander(f"📚 {a['nombre']} ({a['num']}p)", expanded=True):
                    cl = st.text_input("Claves:", value=a.get('claves', ''),
                                       key=f"clr{i}", max_chars=a['num'])
                    st.session_state.areas_examen[i]['claves'] = cl.upper()
                    ia.append({'nombre': a['nombre'], 'num': a['num'],
                               'claves': list(cl.upper())})
                    tc_.extend(list(cl.upper()))
                    tp += a['num']

        if ia:
            st.info(f"📊 {tp} preguntas en {len(ia)} áreas")

        # Seleccionar alumno
        st.markdown("---")
        st.markdown("**👤 Seleccionar Alumno:**")

        de = ""
        nombre_sel = ""

        if modo_cal == "⚡ Evaluación Rápida (solo nombres)":
            nombre_sel = st.text_input("Nombre completo del estudiante:",
                                        key="nombre_rapido",
                                        placeholder="Ej: JUAN PEREZ QUISPE")
            de = ""
        else:
            metodo_sel = st.radio("Método:",
                                   ["📋 Lista de mi grado", "🔍 Buscar por DNI"],
                                   horizontal=True, key="metodo_sel")
            if metodo_sel == "📋 Lista de mi grado":
                grado_doc = None
                if st.session_state.docente_info:
                    grado_doc = st.session_state.docente_info.get('grado')
                if not grado_doc and st.session_state.rol in ['admin', 'directivo']:
                    grado_doc = st.selectbox("Grado:", GRADOS_OPCIONES, key="grado_cal_sel")
                if grado_doc:
                    dg = BaseDatos.obtener_estudiantes_grado(grado_doc)
                    if not dg.empty and 'Nombre' in dg.columns:
                        opciones = [f"{row.get('Nombre', '')} — DNI: {row.get('DNI', '')}"
                                    for _, row in dg.iterrows()]
                        sel = st.selectbox("Estudiante:", opciones, key="sel_est")
                        if sel:
                            de = sel.split("DNI: ")[-1].strip()
                            nombre_sel = sel.split(" — ")[0].strip()
                    else:
                        st.warning("No hay estudiantes en este grado.")
                else:
                    de = st.text_input("DNI:", key="de_manual")
            else:
                de = st.text_input("DNI del alumno:", key="de")
                if de:
                    ae = BaseDatos.buscar_por_dni(de)
                    if ae:
                        nombre_sel = str(ae.get('Nombre', ''))
                        st.success(f"👤 {nombre_sel}")

        # Respuestas
        st.markdown("**📝 Respuestas:**")
        met = st.radio("Método:", ["✏️ Manual", "📸 Cámara/Foto"],
                       horizontal=True, key="met")
        ra = []
        if met == "✏️ Manual":
            for i, a in enumerate(ia):
                r = st.text_input(f"{a['nombre']} ({a['num']}):",
                                  key=f"r{i}", max_chars=a['num'],
                                  placeholder="Ej: ABCDABCDAB")
                ra.extend(list(r.upper()))
        else:
            st.info("📸 Use la hoja generada por el sistema. Buena luz, que se vean los 4 cuadrados negros.")
            src_img = st.radio("Fuente:",
                                ["📷 Cámara", "📁 Subir foto"],
                                horizontal=True, key="src_img")
            image_data = None
            if src_img == "📷 Cámara":
                ac = st.checkbox("📷 Activar cámara", key="chce")
                if ac:
                    fe = st.camera_input("Apunta a la hoja:", key="ce")
                    if fe:
                        image_data = fe.getvalue()
            else:
                fu = st.file_uploader("📁 Subir foto:", type=['jpg', 'jpeg', 'png'], key="fu_hoja")
                if fu:
                    image_data = fu.getvalue()

            if image_data:
                with st.spinner("🔍 Escaneando..."):
                    det = procesar_examen(image_data, tp)
                if det:
                    detectadas = sum(1 for x in det if x != '?')
                    if detectadas == len(det):
                        st.success(f"✅ {detectadas}/{len(det)} respuestas detectadas")
                    else:
                        st.warning(f"⚠️ {detectadas}/{len(det)} detectadas. Corrija las '?' abajo.")
                    det_str = ''.join(det)
                    corregido = st.text_input("Respuestas detectadas:", value=det_str,
                                              key="det_corr", max_chars=tp)
                    ra = list(corregido.upper())
                else:
                    st.error("❌ No se pudo leer. Intente con mejor luz o use modo Manual.")

        # CALIFICAR
        st.markdown("---")
        if st.button("📊 CALIFICAR", type="primary",
                     use_container_width=True, key="cal"):
            if tc_ and ra:
                ad = BaseDatos.buscar_por_dni(de) if de else None
                nm = nombre_sel if nombre_sel else (
                    str(ad.get('Nombre', '')) if ad else "Sin nombre")
                grado_est = str(ad.get('Grado', '')) if ad else ""
                res = {
                    'fecha': hora_peru().strftime('%d/%m/%Y %H:%M'),
                    'titulo': titulo_eval if modo_cal == "📂 Evaluación Guardada" else "Evaluación",
                    'dni': de, 'nombre': nm, 'grado': grado_est,
                    'areas': [], 'promedio_general': 0
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
                    lt = nota_a_letra(nota)
                    detalle = []
                    for j in range(n):
                        cj = ck[j] if j < len(ck) else '?'
                        rj = rk[j] if j < len(rk) else '?'
                        detalle.append({
                            'p': idx + j + 1, 'c': cj, 'r': rj,
                            'ok': (j < len(ck) and j < len(rk) and ck[j] == rk[j])
                        })
                    res['areas'].append({
                        'nombre': a['nombre'], 'correctas': ok,
                        'total': n, 'nota': nota, 'letra': lt,
                        'detalle': detalle
                    })
                    sn += nota
                    mw += f"📚 *{a['nombre']}:* {nota}/20 ({lt})\n"
                    idx += n

                pm = round(sn / len(ia), 1) if ia else 0
                lp = nota_a_letra(pm)
                res['promedio_general'] = pm
                mw += f"\n📊 *PROMEDIO: {pm}/20 ({lp})*"
                BaseDatos.guardar_resultados_examen(res, usuario_actual)

                # Confirmación visual
                st.markdown("### 📊 Resultados")
                cols = st.columns(len(ia) + 1)
                for i, ar in enumerate(res['areas']):
                    with cols[i]:
                        st.metric(f"📚 {ar['nombre']}", f"{ar['nota']}/20",
                                  f"{ar['letra']}")
                with cols[-1]:
                    st.metric("📊 PROMEDIO", f"{pm}/20", lp)

                # Detalle por área
                for ar in res['areas']:
                    with st.expander(f"📋 {ar['nombre']}"):
                        st.dataframe(pd.DataFrame([
                            {'#': d['p'], 'Clave': d['c'], 'Resp': d['r'],
                             '': '✅' if d['ok'] else '❌'}
                            for d in ar['detalle']
                        ]), use_container_width=True, hide_index=True)

                # WhatsApp
                if ad:
                    cel = str(ad.get('Celular_Apoderado', '')).strip()
                    if cel and cel not in ('', 'None', 'nan'):
                        link = generar_link_whatsapp(cel, mw)
                        st.markdown(
                            f'<a href="{link}" target="_blank" class="wa-btn">'
                            f'📱 Enviar resultado → {cel}</a>',
                            unsafe_allow_html=True)

                # Reporte PDF individual
                if st.button("📥 Descargar Reporte PDF del Estudiante", key="dl_rep_est"):
                    pdf = generar_reporte_estudiante_pdf(
                        nm, de, grado_est, [res], config)
                    st.download_button("⬇️ PDF", pdf,
                                       f"Reporte_{nm.replace(' ', '_')}.pdf",
                                       "application/pdf", key="dl_rep_est2")

                st.success("✅ Resultado guardado correctamente en la base de datos")
                reproducir_beep_exitoso()
                st.balloons()
            else:
                st.error("⚠️ Configure claves y respuestas")

    # ===== TAB: RANKING =====
    with tabs_cal[3]:
        st.subheader("🏆 Ranking de Evaluación")

        if st.session_state.rol in ["admin", "directivo"]:
            grado_rank = st.selectbox("Ver grado:", ["TODOS"] + GRADOS_OPCIONES,
                                       key="grado_rank")
            rs = BaseDatos.cargar_todos_resultados()
            if grado_rank != "TODOS":
                rs = [r for r in rs if str(r.get('grado', '')) == grado_rank or
                      str(BaseDatos.buscar_por_dni(r.get('dni', '')) or {}).get('Grado', '') == grado_rank]
        else:
            rs = BaseDatos.cargar_resultados_examen(usuario_actual)

        if rs:
            df = pd.DataFrame([{
                'Fecha': r.get('fecha', ''),
                'Nombre': r.get('nombre', ''),
                'DNI': str(r.get('dni', '')),
                'Promedio': r.get('promedio_general', 0),
                'Literal': nota_a_letra(r.get('promedio_general', 0)),
                'Áreas': ', '.join([f"{a['nombre']}:{a['nota']}"
                                    for a in r.get('areas', [])])
            } for r in rs])
            df = df.sort_values('Promedio', ascending=False).reset_index(drop=True)
            df.insert(0, '#', range(1, len(df) + 1))

            st.dataframe(df, use_container_width=True, hide_index=True)

            # Podio
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
                            f'{r["Promedio"]}/20 ({r["Literal"]})</div>',
                            unsafe_allow_html=True)

            st.markdown("---")
            bc1, bc2 = st.columns(2)
            with bc1:
                if st.button("📥 RANKING PDF", type="primary",
                             use_container_width=True, key="grpdf"):
                    pdf = generar_ranking_pdf(rs, config['anio'])
                    st.download_button("⬇️ PDF", pdf,
                                       f"Ranking_{config['anio']}.pdf",
                                       "application/pdf", key="drpdf")
            with bc2:
                if st.button("📥 REPORTES INDIVIDUALES PDF", type="primary",
                             use_container_width=True, key="reps_ind"):
                    # Generar un PDF multi-página con todos los estudiantes
                    buf_all = io.BytesIO()
                    c_all = canvas.Canvas(buf_all, pagesize=A4)
                    w, h_page = A4
                    for r_item in rs:
                        nm = r_item.get('nombre', '')
                        dn = str(r_item.get('dni', ''))
                        gr = str(r_item.get('grado', ''))
                        
                        c_all.setFont("Helvetica-Bold", 14)
                        c_all.drawCentredString(w/2, h_page-40, f"REPORTE: {nm}")
                        c_all.setFont("Helvetica", 10)
                        y = h_page - 70
                        c_all.drawString(50, y, f"DNI: {dn} | Grado: {gr} | Fecha: {r_item.get('fecha', '')}")
                        y -= 25
                        
                        for area in r_item.get('areas', []):
                            nota = area.get('nota', 0)
                            letra = nota_a_letra(nota)
                            c_all.drawString(60, y, f"• {area['nombre']}: {nota}/20 ({letra})")
                            y -= 16
                        
                        pm = r_item.get('promedio_general', 0)
                        lp = nota_a_letra(pm)
                        y -= 10
                        c_all.setFont("Helvetica-Bold", 12)
                        c_all.drawString(60, y, f"PROMEDIO: {pm}/20 ({lp})")
                        c_all.showPage()
                    
                    c_all.save()
                    buf_all.seek(0)
                    st.download_button("⬇️ Reportes PDF", buf_all,
                                       "Reportes_Individuales.pdf",
                                       "application/pdf", key="dl_reps_all")

            # WhatsApp individual
            st.markdown("---")
            st.markdown("### 📱 Enviar por WhatsApp")
            for _, row in df.iterrows():
                al = BaseDatos.buscar_por_dni(row['DNI']) if row['DNI'] else None
                if al:
                    cel = str(al.get('Celular_Apoderado', '')).strip()
                    if cel and cel not in ('', 'None', 'nan'):
                        ro = next((r for r in rs if str(r.get('dni')) == str(row['DNI'])), None)
                        if ro:
                            msg = f"📝 *RANKING YACHAY*\n👤 {row['Nombre']}\n🏆 #{row['#']}°/{len(df)}\n"
                            for a in ro.get('areas', []):
                                msg += f"📚 {a['nombre']}: {a['nota']}/20\n"
                            msg += f"\n📊 *PROMEDIO: {row['Promedio']}/20 ({row['Literal']})*"
                            link = generar_link_whatsapp(cel, msg)
                            st.markdown(
                                f'<a href="{link}" target="_blank" class="wa-btn">'
                                f'📱 #{row["#"]} {row["Nombre"]} — {row["Promedio"]}/20</a>',
                                unsafe_allow_html=True)

            st.markdown("---")
            if st.button("🔄 NUEVA EVALUACIÓN", type="secondary",
                         use_container_width=True, key="nueva_eval"):
                BaseDatos.limpiar_resultados_examen(usuario_actual)
                st.session_state.areas_examen = []
                st.success("✅ Resultados limpiados. Nueva evaluación lista.")
                st.rerun()
        else:
            st.info("📝 Califica exámenes para ver tu ranking.")

    # ===== TAB: HISTORIAL =====
    with tabs_cal[4]:
        st.subheader("📊 Historial de Evaluaciones")

        if st.session_state.rol in ["admin", "directivo"]:
            grado_hist = st.selectbox("Grado:", GRADOS_OPCIONES, key="grado_hist")
            dg = BaseDatos.obtener_estudiantes_grado(grado_hist)
            if not dg.empty:
                est_sel = st.selectbox("Estudiante:",
                                        [f"{r['Nombre']} — {r['DNI']}"
                                         for _, r in dg.iterrows()],
                                        key="est_hist")
                if est_sel:
                    dni_hist = est_sel.split(" — ")[-1].strip()
                    nombre_hist = est_sel.split(" — ")[0].strip()
            else:
                st.warning("No hay estudiantes en este grado.")
                dni_hist = ""
                nombre_hist = ""
        else:
            dni_hist = st.text_input("DNI del estudiante:", key="dni_hist")
            al_h = BaseDatos.buscar_por_dni(dni_hist) if dni_hist else None
            nombre_hist = str(al_h.get('Nombre', '')) if al_h else ""

        if dni_hist or nombre_hist:
            # Buscar todos los resultados
            all_res = BaseDatos.cargar_todos_resultados()
            hist = [r for r in all_res if str(r.get('dni', '')) == str(dni_hist)
                    or (not dni_hist and r.get('nombre', '') == nombre_hist)]

            if hist:
                st.success(f"📋 {len(hist)} evaluaciones encontradas para **{nombre_hist}**")

                for h in hist:
                    with st.expander(f"📝 {h.get('titulo', 'Evaluación')} — {h.get('fecha', '')}"):
                        for a in h.get('areas', []):
                            st.write(f"**{a['nombre']}:** {a['nota']}/20 ({nota_a_letra(a['nota'])})")
                        st.write(f"**Promedio:** {h.get('promedio_general', 0)}/20")

                # Descargar reporte completo
                if st.button("📥 Descargar Reporte Completo PDF", key="dl_hist_pdf"):
                    al_h = BaseDatos.buscar_por_dni(dni_hist)
                    grado_h = str(al_h.get('Grado', '')) if al_h else ""
                    pdf = generar_reporte_estudiante_pdf(
                        nombre_hist, dni_hist, grado_h, hist, config)
                    st.download_button("⬇️ PDF", pdf,
                                       f"Historial_{nombre_hist.replace(' ', '_')}.pdf",
                                       "application/pdf", key="dl_hist_pdf2")
            else:
                st.info("No hay evaluaciones registradas para este estudiante.")


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
                    if 'Grado' in df.columns else [])
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
            st.download_button("⬇️ Excel", buf2,
                               "docentes_export.xlsx", key="dxlsxd")
        else:
            st.info("📝 Sin docentes.")


# ================================================================
# VISTA DOCENTE — Con links Google e institucionales
# ================================================================

def vista_docente(config):
    info = st.session_state.docente_info
    usuario = st.session_state.get('usuario_actual', '')
    
    # Si no hay info, intentar reconstruir desde usuarios
    if not info or not isinstance(info, dict):
        usuarios = cargar_usuarios()
        user_data = usuarios.get(usuario, {})
        info = user_data.get('docente_info')
        if not info:
            # Intentar reconstruir desde datos del usuario
            info = {
                'grado': user_data.get('grado', ''),
                'label': user_data.get('label', usuario.replace('.', ' ').title()),
                'nivel': user_data.get('nivel', ''),
            }
        st.session_state.docente_info = info
    
    grado = str(info.get('grado', ''))
    label = str(info.get('label', usuario.replace('.', ' ').title()))
    if grado:
        st.markdown(f"### 👨‍🏫 {label} — {grado}")
    else:
        st.markdown(f"### 👨‍🏫 {label}")
        st.info("💡 Pida al administrador que asigne su grado en 'Gestionar Usuarios'.")

    tabs = st.tabs([
        "📋 Asistencia", "📝 Registrar Notas", "📝 Registro Auxiliar",
        "📋 Registro PDF", "📝 Calificación YACHAY"
    ])

    with tabs[0]:
        tab_asistencias()

    with tabs[1]:
        tab_registrar_notas(config)

    with tabs[2]:
        st.subheader("📝 Registro Auxiliar de Evaluación")
        tipo_reg = st.radio("Tipo:", ["📄 En blanco", "📊 Con notas registradas"],
                            horizontal=True, key="tipo_reg_aux")
        sec = st.selectbox("Sección:", ["Todas"] + SECCIONES, key="ds")
        bim = st.selectbox("Bimestre:", list(BIMESTRES.keys()), key="dbim")
        
        if tipo_reg == "📄 En blanco":
            st.markdown("**Cursos:**")
            c1, c2, c3 = st.columns(3)
            with c1:
                dc1 = st.text_input("Curso 1:", "Matemática", key="dc1")
            with c2:
                dc2 = st.text_input("Curso 2:", "Comunicación", key="dc2")
            with c3:
                dc3 = st.text_input("Curso 3:", "Ciencia y Tec.", key="dc3")
            cursos_d = [c for c in [dc1, dc2, dc3] if c.strip()]
        else:
            # Determinar nivel para mostrar áreas correctas
            grado_str = str(grado)
            if 'GRUPO AB' in grado_str:
                cursos_d = AREAS_CEPRE_UNSAAC['GRUPO AB'][:3]
            elif 'GRUPO CD' in grado_str:
                cursos_d = AREAS_CEPRE_UNSAAC['GRUPO CD'][:3]
            elif any(x in grado_str for x in ['Sec']):
                cursos_d = AREAS_MINEDU['SECUNDARIA'][:3]
            else:
                cursos_d = AREAS_MINEDU.get('PRIMARIA', ['Matemática', 'Comunicación', 'Ciencia y Tec.'])[:3]
            st.info(f"📚 Áreas: {', '.join(cursos_d)}")
        
        dg = BaseDatos.obtener_estudiantes_grado(grado, sec)
        st.info(f"📊 {len(dg)} estudiantes")
        if not dg.empty:
            st.dataframe(dg[['Nombre', 'DNI', 'Grado', 'Seccion']],
                         use_container_width=True, hide_index=True)
        if st.button("📥 Descargar Registro Auxiliar PDF", type="primary",
                     use_container_width=True, key="ddra"):
            if not dg.empty:
                lg = grado if grado != "ALL_SECUNDARIA" else "Secundaria"
                sl = sec if sec != "Todas" else "Todas"
                pdf = generar_registro_auxiliar_pdf(
                    lg, sl, config['anio'], bim, dg, cursos_d)
                st.download_button("⬇️ PDF", pdf,
                                   f"RegAux_{lg}_{bim}.pdf",
                                   "application/pdf", key="ddra2")

    with tabs[3]:
        st.subheader("📋 Registro de Asistencia PDF")
        sec2 = st.selectbox("Sección:", ["Todas"] + SECCIONES, key="ds2")
        meses_opts = list(MESES_ESCOLARES.items())
        meses_sel = st.multiselect(
            "Meses:",
            [f"{v} ({k})" for k, v in meses_opts],
            default=[f"{v} ({k})" for k, v in meses_opts[:1]],
            key="dmsel")
        meses_nums = [int(m.split('(')[1].replace(')', '')) for m in meses_sel]
        dg2 = BaseDatos.obtener_estudiantes_grado(grado, sec2)
        st.info(f"📊 {len(dg2)} estudiantes")
        if st.button("📥 Descargar Registro Asistencia PDF", type="primary",
                     use_container_width=True, key="ddas"):
            if not dg2.empty and meses_nums:
                lg = grado if grado != "ALL_SECUNDARIA" else "Secundaria"
                sl = sec2 if sec2 != "Todas" else "Todas"
                pdf = generar_registro_asistencia_pdf(
                    lg, sl, config['anio'], dg2, meses_nums)
                st.download_button("⬇️ PDF", pdf,
                                   f"RegAsist_{lg}.pdf",
                                   "application/pdf", key="ddas2")

    with tabs[4]:
        tab_calificacion_yachay(config)


# ================================================================
# REGISTRO DE INCIDENCIAS
# ================================================================

TIPOS_INCIDENCIA = [
    'Conductual (Indisciplina)',
    'Académica (Plagio, falta de tareas)',
    'Convivencia (Conflicto entre pares)',
    'Presunto caso de Violencia Escolar (Bullying)',
    'Salud / Accidente',
    'Infraestructura / Daño a propiedad',
]

DERIVACIONES = [
    'No requiere derivación',
    'Psicología',
    'Dirección',
    'Tutoría',
    'Reporte portal SíseVe',
    'DEMUNA',
    'Otra',
]


def generar_incidencia_pdf(datos, config):
    """Genera PDF del registro de incidencia"""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    # Encabezado
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w / 2, h - 50, config.get('nombre_ie', 'I.E.P. ALTERNATIVO YACHAY'))
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(w / 2, h - 70, "REGISTRO DE INCIDENCIAS")
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, h - 85, config.get('ubicacion', 'Chinchero, Cusco'))

    c.setStrokeColor(colors.HexColor("#1a56db"))
    c.setLineWidth(2)
    c.line(40, h - 95, w - 40, h - 95)

    y = h - 120
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "I. INFORMACIÓN GENERAL")
    y -= 20

    campos = [
        ("Código de Incidencia:", datos.get('codigo', '')),
        ("Fecha y Hora:", f"{datos.get('fecha', '')} — {datos.get('hora', '')}"),
        ("Lugar:", datos.get('lugar', '')),
        ("Nivel:", datos.get('nivel', '')),
        ("Grado y Sección:", f"{datos.get('grado', '')} — {datos.get('seccion', '')}"),
    ]
    c.setFont("Helvetica", 10)
    for label, valor in campos:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y, label)
        c.setFont("Helvetica", 10)
        c.drawString(200, y, str(valor))
        y -= 18

    y -= 10
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "II. IDENTIFICACIÓN DE INVOLUCRADOS")
    y -= 20
    for label_campo in ['Afectado(s)', 'Implicado(s)', 'Reportante']:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y, f"{label_campo}:")
        c.setFont("Helvetica", 10)
        c.drawString(160, y, str(datos.get(label_campo.lower().replace('(s)', '').strip(), '')))
        y -= 18

    y -= 10
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "III. DESCRIPCIÓN DE LA INCIDENCIA")
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, y, f"Tipo: {datos.get('tipo', '')}")
    y -= 20

    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, y, "Relato de los hechos:")
    y -= 15
    c.setFont("Helvetica", 9)
    relato = str(datos.get('relato', ''))
    for linea in textwrap.wrap(relato, 85):
        c.drawString(70, y, linea)
        y -= 13
        if y < 100:
            c.showPage()
            y = h - 50

    y -= 15
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "IV. MEDIDAS Y ACCIONES TOMADAS")
    y -= 20
    for label_accion, key in [("Acción Inmediata:", 'accion_inmediata'),
                               ("Compromisos:", 'compromisos'),
                               ("Derivación:", 'derivacion')]:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y, label_accion)
        y -= 15
        c.setFont("Helvetica", 9)
        for linea in textwrap.wrap(str(datos.get(key, '')), 85):
            c.drawString(70, y, linea)
            y -= 13

    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "V. FIRMAS DE CONFORMIDAD")
    y -= 40
    firmas = ["Responsable del Registro", "Estudiante (si aplica)",
              "Padre de Familia"]
    for i, firma in enumerate(firmas):
        x = 60 + (i * 170)
        c.line(x, y, x + 140, y)
        c.setFont("Helvetica", 8)
        c.drawCentredString(x + 70, y - 12, firma)

    # Pie
    c.setFont("Helvetica", 7)
    c.drawCentredString(w / 2, 30, f"Generado por YACHAY PRO — {hora_peru_str()}")

    c.save()
    buf.seek(0)
    return buf.getvalue()


def tab_incidencias(config):
    """Tab de Registro de Incidencias"""
    st.subheader("📝 Registro de Incidencias")

    gs = _gs()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Nueva Incidencia")

        # Generar código automático
        if gs:
            codigo = gs.generar_siguiente_codigo_incidencia()
        else:
            codigo = f"INC-{hora_peru().year}-{int(time.time()) % 1000:03d}"

        with st.form("form_incidencia", clear_on_submit=True):
            st.info(f"📌 Código: **{codigo}**")

            ci1, ci2 = st.columns(2)
            with ci1:
                fecha_inc = st.date_input("Fecha:", value=hora_peru().date(),
                                           key="fld_inc_fecha")
                nivel_inc = st.selectbox("Nivel:", NIVELES_LIST, key="fld_inc_nivel")
            with ci2:
                hora_inc = st.text_input("Hora:", value=hora_peru().strftime('%H:%M'),
                                          key="fld_inc_hora")
                grado_inc = st.selectbox("Grado:", GRADOS_OPCIONES, key="fld_inc_grado")

            lugar = st.text_input("Lugar:", placeholder="Ej: Aula, patio, alrededores",
                                  key="fld_inc_lugar")
            seccion_inc = st.selectbox("Sección:", SECCIONES, key="fld_inc_sec")

            tipo_inc = st.selectbox("Tipo de Incidencia:", TIPOS_INCIDENCIA,
                                    key="fld_inc_tipo")

            st.markdown("**Involucrados:**")
            afectados = st.text_area("Afectado(s) - Nombres, DNI:",
                                     key="fld_inc_afect")
            implicados = st.text_area("Implicado(s) - Nombres, DNI:",
                                      key="fld_inc_implic")
            reportante = st.text_input("Informante/Reportante:",
                                       key="fld_inc_report")

            relato = st.text_area("Relato de los hechos:",
                                  placeholder="Descripción objetiva...",
                                  key="fld_inc_relato")

            accion = st.text_area("Acción Inmediata:", key="fld_inc_accion")
            compromisos = st.text_area("Compromisos:", key="fld_inc_comp")
            derivacion = st.selectbox("Derivación:", DERIVACIONES, key="fld_inc_deriv")

            submitted = st.form_submit_button("💾 REGISTRAR INCIDENCIA",
                                               type="primary",
                                               use_container_width=True)
            if submitted:
                datos_inc = {
                    'codigo': codigo,
                    'fecha': str(fecha_inc),
                    'hora': str(hora_inc),
                    'lugar': lugar,
                    'nivel': nivel_inc,
                    'grado': grado_inc,
                    'seccion': seccion_inc,
                    'tipo': tipo_inc,
                    'afectados': afectados,
                    'implicados': implicados,
                    'reportante': reportante,
                    'dni_reportante': '',
                    'relato': relato,
                    'accion_inmediata': accion,
                    'compromisos': compromisos,
                    'derivacion': derivacion,
                    'registrado_por': st.session_state.get('usuario_actual', ''),
                }

                # Guardar en Google Sheets
                if gs:
                    gs.guardar_incidencia(datos_inc)
                    st.success(f"✅ Incidencia {codigo} registrada y guardada en Google Sheets")
                else:
                    st.success(f"✅ Incidencia {codigo} registrada")

                # Guardar PDF en session para descargar fuera del form
                pdf = generar_incidencia_pdf(datos_inc, config)
                st.session_state['ultimo_pdf_incidencia'] = pdf
                st.session_state['ultimo_codigo_incidencia'] = codigo

        # Botón de descarga FUERA del formulario
        if st.session_state.get('ultimo_pdf_incidencia'):
            cod = st.session_state.get('ultimo_codigo_incidencia', 'INC')
            st.download_button("📥 Descargar PDF de Incidencia", 
                               st.session_state['ultimo_pdf_incidencia'],
                               f"Incidencia_{cod}.pdf",
                               "application/pdf", key="dl_inc_outside")

    with col2:
        st.markdown("### 📋 Historial")
        if gs:
            incidencias = gs.leer_incidencias()
            if incidencias:
                for inc in reversed(incidencias[-20:]):
                    with st.expander(
                        f"📌 {inc.get('codigo', '?')} — {inc.get('fecha', '')}"):
                        st.write(f"**Tipo:** {inc.get('tipo', '')}")
                        st.write(f"**Grado:** {inc.get('grado', '')}")
                        st.write(f"**Afectados:** {inc.get('afectados', '')}")
                        st.write(f"**Relato:** {inc.get('relato', '')[:200]}")
                        try:
                            pdf_h = generar_incidencia_pdf(inc, config)
                            st.download_button("📥 PDF",
                                               pdf_h,
                                               f"Inc_{inc.get('codigo', '')}.pdf",
                                               "application/pdf",
                                               key=f"dl_hist_{inc.get('codigo', '')}_{id(inc)}")
                        except Exception:
                            pass
            else:
                st.info("Sin incidencias registradas")
        else:
            st.warning("⚠️ Conecta Google Sheets para ver historial")


# ================================================================
# REPORTES MENSUALES Y HISTORIAL
# ================================================================

def generar_reporte_asistencia_mensual_pdf(datos_mes, grado, mes, anio, config):
    """PDF de reporte mensual de asistencia por grado"""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=landscape(A4))
    w, h = landscape(A4)

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w / 2, h - 40,
                        config.get('nombre_ie', 'I.E.P. ALTERNATIVO YACHAY'))
    c.setFont("Helvetica-Bold", 11)
    nombre_mes = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre',
                  'Diciembre']
    c.drawCentredString(w / 2, h - 58,
                        f"REPORTE MENSUAL DE ASISTENCIA — {nombre_mes[mes]} {anio}")
    c.drawCentredString(w / 2, h - 73, f"Grado: {grado}")

    # Calcular días del mes
    import calendar as cal_mod
    dias_mes = cal_mod.monthrange(anio, mes)[1]

    y = h - 100
    c.setFont("Helvetica-Bold", 7)

    # Encabezados
    x_start = 30
    c.drawString(x_start, y, "#")
    c.drawString(x_start + 15, y, "Nombre")
    c.drawString(x_start + 180, y, "DNI")

    # Días como columnas
    x_dia = x_start + 225
    for d in range(1, dias_mes + 1):
        dia_semana = cal_mod.weekday(anio, mes, d)
        if dia_semana < 5:  # L-V
            c.drawCentredString(x_dia, y, str(d))
            x_dia += 18

    c.drawString(x_dia + 5, y, "Total")
    c.drawString(x_dia + 35, y, "%")

    y -= 3
    c.setLineWidth(0.5)
    c.line(x_start, y, w - 30, y)
    y -= 12

    c.setFont("Helvetica", 6)
    num = 0
    for nombre, info in sorted(datos_mes.items()):
        num += 1
        c.drawString(x_start, y, str(num))
        c.drawString(x_start + 15, y, nombre[:30])
        c.drawString(x_start + 180, y, str(info.get('dni', '')))

        x_dia = x_start + 225
        total_asist = 0
        total_dias_hab = 0
        for d in range(1, dias_mes + 1):
            dia_semana = cal_mod.weekday(anio, mes, d)
            if dia_semana < 5:
                total_dias_hab += 1
                fecha_str = f"{anio}-{mes:02d}-{d:02d}"
                if fecha_str in info.get('fechas', {}):
                    c.setFillColor(colors.HexColor("#16a34a"))
                    c.drawCentredString(x_dia, y, "✓")
                    c.setFillColor(colors.black)
                    total_asist += 1
                else:
                    c.setFillColor(colors.HexColor("#dc2626"))
                    c.drawCentredString(x_dia, y, "✗")
                    c.setFillColor(colors.black)
                x_dia += 18

        pct = (total_asist / total_dias_hab * 100) if total_dias_hab > 0 else 0
        c.drawString(x_dia + 5, y, str(total_asist))
        c.drawString(x_dia + 35, y, f"{pct:.0f}%")

        y -= 11
        if y < 40:
            c.showPage()
            y = h - 50
            c.setFont("Helvetica", 6)

    c.setFont("Helvetica", 7)
    c.drawCentredString(w / 2, 20,
                        f"YACHAY PRO — Generado: {hora_peru_str()}")
    c.save()
    buf.seek(0)
    return buf.getvalue()


def generar_reporte_examen_zipgrade(resultado, config):
    """Genera reporte estilo ZipGrade: verde=correcta, rojo=incorrecta, azul=no marcó pero era correcta"""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    titulo = resultado.get('titulo', 'Evaluación')
    fecha = resultado.get('fecha', '')
    areas = resultado.get('areas', [])
    alumnos = resultado.get('alumnos', [])

    # COLOR DEFINITIONS
    COLOR_CORRECTO = colors.HexColor("#16a34a")   # Verde
    COLOR_INCORRECTO = colors.HexColor("#dc2626")  # Rojo
    COLOR_NO_MARCO = colors.HexColor("#2563eb")    # Azul

    pagina = 0
    for alumno in alumnos:
        if pagina > 0:
            c.showPage()
        pagina += 1

        # Encabezado
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(w / 2, h - 40,
                            config.get('nombre_ie', 'I.E.P. ALTERNATIVO YACHAY'))
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(w / 2, h - 58, f"REPORTE DE EVALUACIÓN — {titulo}")
        c.setFont("Helvetica", 9)
        c.drawCentredString(w / 2, h - 73, f"Fecha: {fecha}")

        c.setLineWidth(2)
        c.setStrokeColor(colors.HexColor("#1a56db"))
        c.line(40, h - 80, w - 40, h - 80)

        # Datos del alumno
        y = h - 100
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, f"Alumno: {alumno.get('nombre', '')}")
        c.setFont("Helvetica", 10)
        c.drawString(400, y, f"DNI: {alumno.get('dni', '')}")
        y -= 18
        prom = alumno.get('promedio', 0)
        nota_letra = 'AD' if prom >= 18 else 'A' if prom >= 14 else 'B' if prom >= 11 else 'C'
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"PROMEDIO GENERAL: {prom:.1f}/20 ({nota_letra})")
        y -= 25

        # Leyenda de colores
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(COLOR_CORRECTO)
        c.rect(50, y, 12, 10, fill=1, stroke=0)
        c.setFillColor(colors.black)
        c.drawString(65, y + 2, "= Correcta")

        c.setFillColor(COLOR_INCORRECTO)
        c.rect(150, y, 12, 10, fill=1, stroke=0)
        c.setFillColor(colors.black)
        c.drawString(165, y + 2, "= Incorrecta")

        c.setFillColor(COLOR_NO_MARCO)
        c.rect(270, y, 12, 10, fill=1, stroke=0)
        c.setFillColor(colors.black)
        c.drawString(285, y + 2, "= No marcó (era correcta)")
        y -= 25

        # Por cada área
        notas_alumno = alumno.get('notas', [])
        for idx_area, nota_area in enumerate(notas_alumno):
            area_nombre = nota_area.get('area', f'Área {idx_area + 1}')
            nota_val = nota_area.get('nota', 0)
            correctas = nota_area.get('correctas', 0)
            total = nota_area.get('total', 10)
            respuestas = str(nota_area.get('respuestas', ''))
            claves = str(nota_area.get('claves', ''))

            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(colors.HexColor("#1a56db"))
            c.drawString(50, y, f"📝 {area_nombre} — {nota_val:.1f}/20 ({correctas}/{total})")
            c.setFillColor(colors.black)
            y -= 18

            # Tabla de respuestas con colores
            opciones = ['A', 'B', 'C', 'D']
            c.setFont("Helvetica-Bold", 8)
            c.drawString(60, y, "Preg")
            for oi, op in enumerate(opciones):
                c.drawCentredString(120 + oi * 40, y, op)
            c.drawString(290, y, "Correcta")
            c.drawString(355, y, "Marcó")
            c.drawString(410, y, "Resultado")
            y -= 3
            c.line(55, y, 470, y)
            y -= 12

            c.setFont("Helvetica", 8)
            for p in range(total):
                clave_p = claves[p] if p < len(claves) else '?'
                resp_p = respuestas[p] if p < len(respuestas) else '?'
                es_correcta = resp_p == clave_p and resp_p != '?'
                no_marco = resp_p == '?'

                c.drawString(60, y, f"  {p + 1}")

                # Dibujar burbujas con colores
                for oi, op in enumerate(opciones):
                    cx = 120 + oi * 40
                    if op == clave_p and es_correcta:
                        c.setFillColor(COLOR_CORRECTO)
                        c.circle(cx, y + 3, 7, fill=1, stroke=0)
                        c.setFillColor(colors.white)
                        c.drawCentredString(cx, y + 0.5, op)
                    elif op == resp_p and not es_correcta and not no_marco:
                        c.setFillColor(COLOR_INCORRECTO)
                        c.circle(cx, y + 3, 7, fill=1, stroke=0)
                        c.setFillColor(colors.white)
                        c.drawCentredString(cx, y + 0.5, op)
                    elif op == clave_p and (not es_correcta):
                        c.setFillColor(COLOR_NO_MARCO)
                        c.circle(cx, y + 3, 7, fill=1, stroke=0)
                        c.setFillColor(colors.white)
                        c.drawCentredString(cx, y + 0.5, op)
                    else:
                        c.setStrokeColor(colors.HexColor("#94a3b8"))
                        c.setFillColor(colors.white)
                        c.circle(cx, y + 3, 7, fill=1, stroke=1)
                        c.setFillColor(colors.HexColor("#94a3b8"))
                        c.drawCentredString(cx, y + 0.5, op)

                c.setFillColor(colors.black)
                c.drawString(290, y, clave_p)
                c.drawString(355, y, resp_p)

                if es_correcta:
                    c.setFillColor(COLOR_CORRECTO)
                    c.drawString(410, y, "✓ Correcta")
                elif no_marco:
                    c.setFillColor(COLOR_NO_MARCO)
                    c.drawString(410, y, "— Sin marcar")
                else:
                    c.setFillColor(COLOR_INCORRECTO)
                    c.drawString(410, y, "✗ Incorrecta")

                c.setFillColor(colors.black)
                y -= 14

                if y < 60:
                    c.showPage()
                    y = h - 50
                    c.setFont("Helvetica", 8)

            y -= 10

    # Pie
    c.setFont("Helvetica", 7)
    c.drawCentredString(w / 2, 25, f"YACHAY PRO — Generado: {hora_peru_str()}")
    c.save()
    buf.seek(0)
    return buf.getvalue()


def tab_reportes(config):
    """Tab de reportes y historial — COMPLETO"""
    st.subheader("📊 Reportes e Historial")

    subtab = st.radio("Seleccionar:", [
        "📋 Asistencia Mensual", "📊 Reporte Integral",
        "📄 Reporte ZipGrade"
    ], horizontal=True, key="rep_tipo")

    gs = _gs()

    if subtab == "📋 Asistencia Mensual":
        st.markdown("### 📋 Reporte Mensual de Asistencia por Grado")
        if gs:
            c1, c2, c3 = st.columns(3)
            with c1:
                grado_rep = st.selectbox("Grado:", GRADOS_OPCIONES, key="rep_gr")
            with c2:
                mes_rep = st.selectbox("Mes:", list(range(1, 13)),
                                        format_func=lambda x: ['', 'Enero', 'Febrero',
                                        'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
                                        'Agosto', 'Septiembre', 'Octubre', 'Noviembre',
                                        'Diciembre'][x], key="rep_mes")
            with c3:
                anio_rep = st.number_input("Año:", value=hora_peru().year,
                                            key="rep_anio")

            if st.button("📊 Generar Reporte", type="primary", key="btn_rep_asist"):
                datos = gs.reporte_asistencia_mensual(grado_rep, mes_rep, int(anio_rep))
                if datos:
                    st.success(f"✅ {len(datos)} estudiantes encontrados")
                    for nombre, info_a in sorted(datos.items()):
                        total = len(info_a.get('fechas', {}))
                        st.write(f"**{nombre}** — {total} días asistidos")
                    pdf = generar_reporte_asistencia_mensual_pdf(
                        datos, grado_rep, mes_rep, int(anio_rep), config)
                    st.download_button("📥 PDF Asistencia Mensual", pdf,
                                       f"Asistencia_{grado_rep}_{mes_rep}.pdf",
                                       "application/pdf", key="dl_rep_asist")
                else:
                    st.warning("No hay datos para este período")
        else:
            st.warning("⚠️ Conecta Google Sheets")

    elif subtab == "📊 Reporte Integral":
        st.markdown("### 📊 Reporte Integral del Estudiante")
        st.markdown("*Incluye: Notas + Asistencia + Semáforo + Recomendaciones*")

        rc1, rc2 = st.columns(2)
        with rc1:
            grado_ri = st.selectbox("Grado:", GRADOS_OPCIONES, key="ri_grado")
        with rc2:
            modo_ri = st.radio("Generar:", ["Un estudiante", "Todo el grado"],
                               horizontal=True, key="ri_modo")

        dg = BaseDatos.obtener_estudiantes_grado(grado_ri)
        if dg.empty:
            st.warning("Sin estudiantes en este grado")
            return

        if modo_ri == "Un estudiante":
            opciones = [f"{r['Nombre']} — {r['DNI']}" for _, r in dg.iterrows()]
            sel = st.selectbox("Estudiante:", opciones, key="ri_est")
            if sel:
                dni_ri = sel.split(" — ")[-1].strip()
                nombre_ri = sel.split(" — ")[0].strip()
        else:
            dni_ri = None
            nombre_ri = None

        if st.button("📥 GENERAR REPORTE INTEGRAL", type="primary",
                     use_container_width=True, key="btn_ri"):
            with st.spinner("Generando reporte..."):
                if modo_ri == "Un estudiante" and dni_ri:
                    # Cargar notas del estudiante
                    notas_est = []
                    asist_est = {}
                    if gs:
                        try:
                            ws = gs._get_hoja('config')
                            if ws:
                                data = ws.get_all_records()
                                for d in data:
                                    clave = str(d.get('clave', ''))
                                    if clave.startswith(f'nota_{dni_ri}'):
                                        try:
                                            notas_est.append(json.loads(d.get('valor', '{}')))
                                        except Exception:
                                            pass
                            # Asistencia
                            try:
                                asist_est = gs.historial_asistencia_estudiante(dni_ri) or {}
                            except Exception:
                                asist_est = {}
                        except Exception:
                            pass

                    # También cargar de resultados de examen
                    all_res = BaseDatos.cargar_todos_resultados()
                    for r in all_res:
                        if str(r.get('dni', '')) == str(dni_ri):
                            for area in r.get('areas', []):
                                notas_est.append({
                                    'area': area['nombre'],
                                    'nota': area['nota'],
                                    'literal': nota_a_letra(area['nota']),
                                    'bimestre': r.get('titulo', 'Evaluación'),
                                    'fecha': r.get('fecha', ''),
                                    'tipo': 'examen'
                                })

                    al = BaseDatos.buscar_por_dni(dni_ri)
                    grado_est = str(al.get('Grado', grado_ri)) if al else grado_ri

                    pdf = generar_reporte_integral_pdf(
                        nombre_ri, dni_ri, grado_est, notas_est, asist_est, config)
                    st.download_button("⬇️ Descargar PDF", pdf,
                                       f"Reporte_{nombre_ri.replace(' ', '_')}.pdf",
                                       "application/pdf", key="dl_ri")
                    st.success(f"✅ Reporte de {nombre_ri} generado")

                else:
                    # Todo el grado - un PDF multi-página
                    buf_all = io.BytesIO()
                    c_pdf = canvas.Canvas(buf_all, pagesize=A4)
                    w_page, h_page = A4

                    for _, row in dg.iterrows():
                        n_est = str(row.get('Nombre', ''))
                        d_est = str(row.get('DNI', ''))

                        # Cargar notas
                        notas_est = []
                        if gs:
                            try:
                                ws = gs._get_hoja('config')
                                if ws:
                                    data = ws.get_all_records()
                                    for d in data:
                                        clave = str(d.get('clave', ''))
                                        if clave.startswith(f'nota_{d_est}'):
                                            try:
                                                notas_est.append(json.loads(d.get('valor', '{}')))
                                            except Exception:
                                                pass
                            except Exception:
                                pass

                        # De exámenes también
                        all_res = BaseDatos.cargar_todos_resultados()
                        for r in all_res:
                            if str(r.get('dni', '')) == d_est:
                                for area in r.get('areas', []):
                                    notas_est.append({
                                        'area': area['nombre'],
                                        'nota': area['nota'],
                                        'fecha': r.get('fecha', ''),
                                    })

                        # Página del estudiante
                        c_pdf.setFont("Helvetica-Bold", 14)
                        c_pdf.drawCentredString(w_page/2, h_page-40, f"REPORTE: {n_est}")
                        c_pdf.setFont("Helvetica", 10)
                        y = h_page-65
                        c_pdf.drawString(50, y, f"DNI: {d_est} | Grado: {grado_ri}")
                        y -= 25

                        if notas_est:
                            for n in notas_est:
                                nota_v = float(n.get('nota', 0))
                                lit = nota_a_letra(nota_v)
                                c_pdf.drawString(60, y,
                                    f"• {n.get('area', '')}: {nota_v}/20 ({lit}) — {n.get('fecha', '')}")
                                y -= 14
                                if y < 80:
                                    break

                            # Promedio
                            promedios = [float(n.get('nota', 0)) for n in notas_est if float(n.get('nota', 0)) > 0]
                            if promedios:
                                prom = round(sum(promedios)/len(promedios), 1)
                                lit_p = nota_a_letra(prom)
                                y -= 10
                                c_pdf.setFont("Helvetica-Bold", 12)
                                c_pdf.drawString(60, y, f"PROMEDIO: {prom}/20 ({lit_p})")
                        else:
                            c_pdf.drawString(60, y, "Sin calificaciones registradas.")

                        c_pdf.showPage()

                    c_pdf.save()
                    buf_all.seek(0)
                    st.download_button("⬇️ Reportes Todo el Grado", buf_all,
                                       f"Reportes_{grado_ri}.pdf",
                                       "application/pdf", key="dl_ri_all")
                    st.success(f"✅ Reportes de {len(dg)} estudiantes generados")

    elif subtab == "📄 Reporte ZipGrade":
        st.markdown("### 📄 Reporte estilo ZipGrade")
        usuario = st.session_state.get('usuario_actual', '')
        resultados = BaseDatos.cargar_resultados_examen(usuario)
        if st.session_state.rol in ['admin', 'directivo']:
            resultados = BaseDatos.cargar_todos_resultados()

        if resultados:
            opciones_eval = [
                f"{r.get('nombre', '?')} — {r.get('fecha', '')}"
                for r in resultados
            ]
            sel_eval = st.selectbox("Evaluación:", opciones_eval, key="zg_eval")
            idx_eval = opciones_eval.index(sel_eval)
            eval_sel = resultados[idx_eval]

            # Mostrar detalles
            for area in eval_sel.get('areas', []):
                nota = area.get('nota', 0)
                lit = nota_a_letra(nota)
                col = color_semaforo(lit)
                st.markdown(f"**{area['nombre']}:** <span style='color:{col};'>{nota}/20 ({lit})</span>",
                           unsafe_allow_html=True)

            if st.button("📥 PDF ZipGrade", type="primary", key="btn_zg"):
                pdf = generar_reporte_examen_zipgrade(eval_sel, config)
                st.download_button("⬇️ PDF", pdf,
                                   f"ZipGrade_{sel_eval[:20]}.pdf",
                                   "application/pdf", key="dl_zg")
        else:
            st.info("Sin evaluaciones. Califica exámenes primero.")


# ================================================================
# ÁREAS DEL CURRÍCULO NACIONAL MINEDU — Por Nivel
# ================================================================

AREAS_MINEDU = {
    'INICIAL': [
        'Personal Social', 'Psicomotriz', 'Comunicación',
        'Castellano como segunda lengua', 'Matemática',
        'Ciencia y Tecnología'
    ],
    'PRIMARIA': [
        'Personal Social', 'Educación Física', 'Comunicación',
        'Arte y Cultura', 'Castellano como segunda lengua',
        'Inglés', 'Matemática', 'Ciencia y Tecnología',
        'Educación Religiosa'
    ],
    'SECUNDARIA': [
        'Desarrollo Personal, Ciudadanía y Cívica', 'Ciencias Sociales',
        'Educación para el Trabajo', 'Educación Física', 'Comunicación',
        'Arte y Cultura', 'Castellano como segunda lengua', 'Inglés',
        'Matemática', 'Ciencia y Tecnología', 'Educación Religiosa'
    ],
    'PREUNIVERSITARIO': [
        'Razonamiento Matemático', 'Aritmética', 'Álgebra', 'Geometría',
        'Trigonometría', 'Lenguaje', 'Literatura', 'Razonamiento Verbal',
        'Historia del Perú', 'Historia Universal', 'Geografía', 'Economía',
        'Filosofía y Lógica', 'Psicología', 'Educación Cívica',
        'Biología', 'Química', 'Física', 'Anatomía'
    ]
}

PERIODOS_EVALUACION = [
    'Semana 1', 'Semana 2', 'Semana 3', 'Semana 4',
    'Semana 5', 'Semana 6', 'Semana 7', 'Semana 8',
    'Quincenal 1', 'Quincenal 2',
    'I Bimestre', 'II Bimestre', 'III Bimestre', 'IV Bimestre',
    'Evaluación Parcial', 'Evaluación Final', 'Práctica Calificada',
    'Ciclo Verano', 'Ciclo Regular', 'Ciclo Intensivo',
    'Reforzamiento Pre-U',
]
BIMESTRES_LISTA = PERIODOS_EVALUACION  # Alias

# ================================================================
# TAB: REGISTRAR NOTAS (Manual — Para todos los docentes)
# ================================================================

def tab_registrar_notas(config):
    """Módulo para que docentes registren notas manualmente"""
    st.header("📝 Registrar Notas")

    usuario = st.session_state.get('usuario_actual', '')
    gs = _gs()

    # Determinar grado del docente
    grado_doc = None
    nivel_doc = None
    if st.session_state.docente_info:
        grado_doc = st.session_state.docente_info.get('grado', '')
        nivel_doc = st.session_state.docente_info.get('nivel', '')

    # Admin/directivo puede elegir grado
    if st.session_state.rol in ['admin', 'directivo']:
        grado_sel = st.selectbox("🎓 Grado:", GRADOS_OPCIONES, key="rn_grado")
    elif grado_doc:
        grado_sel = grado_doc
        st.info(f"🎓 **{grado_sel}**")
    else:
        st.warning("No se detectó grado asignado.")
        return

    # Determinar nivel y áreas correspondientes
    nivel = 'PRIMARIA'
    grado_str = str(grado_sel)
    if 'Inicial' in grado_str:
        nivel = 'INICIAL'
    elif any(x in grado_str for x in ['1° Sec', '2° Sec', '3° Sec', '4° Sec', '5° Sec']):
        nivel = 'SECUNDARIA'
    elif 'GRUPO AB' in grado_str:
        nivel = 'CEPRE_AB'
    elif 'GRUPO CD' in grado_str:
        nivel = 'CEPRE_CD'
    elif any(x in grado_str for x in ['Ciclo', 'Reforzamiento']):
        nivel = 'PREUNIVERSITARIO'

    # Seleccionar área y período
    c1, c2 = st.columns(2)
    with c1:
        if nivel == 'CEPRE_AB':
            areas_nivel = AREAS_CEPRE_UNSAAC['GRUPO AB']
        elif nivel == 'CEPRE_CD':
            areas_nivel = AREAS_CEPRE_UNSAAC['GRUPO CD']
        elif nivel == 'SECUNDARIA':
            # Secundaria: áreas MINEDU + todas las áreas CEPRE UNSAAC
            areas_cepre_all = sorted(set(
                AREAS_CEPRE_UNSAAC['GRUPO AB'] + AREAS_CEPRE_UNSAAC['GRUPO CD']
            ))
            areas_nivel = AREAS_MINEDU['SECUNDARIA'] + ['──── CEPRE UNSAAC ────'] + areas_cepre_all
        else:
            areas_nivel = AREAS_MINEDU.get(nivel, AREAS_MINEDU.get('PRIMARIA', []))
        area_sel = st.selectbox("📚 Área:", areas_nivel, key="rn_area")
    with c2:
        bim_sel = st.selectbox("📅 Período:", PERIODOS_EVALUACION, key="rn_bim")
    titulo_eval_rn = st.text_input("📝 Título (opcional):", placeholder="Ej: Evaluación Semanal 3",
                                    key="rn_titulo")

    # Cargar estudiantes
    dg = BaseDatos.obtener_estudiantes_grado(grado_sel)
    if dg.empty:
        st.warning("No hay estudiantes matriculados en este grado.")
        return

    st.markdown(f"### 📋 {len(dg)} estudiantes — {area_sel} — {bim_sel}")

    # Tabla de ingreso de notas
    notas_input = {}
    st.markdown("""
    <style>
    .nota-ad { background: #dcfce7 !important; }
    .nota-a { background: #dbeafe !important; }
    .nota-b { background: #fef3c7 !important; }
    .nota-c { background: #fee2e2 !important; }
    </style>
    """, unsafe_allow_html=True)

    # Header
    hc1, hc2, hc3, hc4 = st.columns([3, 1, 1, 1])
    with hc1:
        st.markdown("**Estudiante**")
    with hc2:
        st.markdown("**Nota (0-20)**")
    with hc3:
        st.markdown("**Literal**")
    with hc4:
        st.markdown("**Estado**")

    for idx, row in dg.iterrows():
        nombre = str(row.get('Nombre', ''))
        dni = str(row.get('DNI', ''))
        nc1, nc2, nc3, nc4 = st.columns([3, 1, 1, 1])
        with nc1:
            st.write(f"👤 {nombre}")
        with nc2:
            nota = st.number_input("Nota", 0, 20, 0,
                                    key=f"rn_{dni}_{area_sel}_{bim_sel}",
                                    label_visibility="collapsed")
            notas_input[dni] = {'nombre': nombre, 'nota': nota}
        with nc3:
            lit = nota_a_letra(nota)
            color = color_semaforo(lit)
            st.markdown(f"<span style='color:{color};font-weight:bold;font-size:1.2em;'>{lit}</span>",
                       unsafe_allow_html=True)
        with nc4:
            desc = ESCALA_MINEDU.get(lit, {}).get('nombre', '')[:12]
            st.caption(desc)

    # Guardar
    st.markdown("---")
    if st.button("💾 GUARDAR NOTAS", type="primary",
                 use_container_width=True, key="btn_guardar_notas"):
        guardadas = 0
        for dni, data in notas_input.items():
            if data['nota'] > 0:
                registro = {
                    'fecha': fecha_peru_str(),
                    'grado': grado_sel,
                    'area': area_sel,
                    'bimestre': bim_sel,
                    'dni': dni,
                    'nombre': data['nombre'],
                    'nota': data['nota'],
                    'literal': nota_a_letra(data['nota']),
                    'docente': usuario,
                    'tipo': 'manual'
                }
                if gs:
                    try:
                        ws = gs._get_hoja('config')
                        if ws:
                            key = f"nota_{dni}_{area_sel}_{bim_sel}"
                            ws.append_row([key, json.dumps(registro, ensure_ascii=False, default=str)])
                            guardadas += 1
                    except Exception:
                        pass

        if guardadas > 0:
            st.success(f"✅ **{guardadas} notas guardadas** correctamente en la nube")
            reproducir_beep_exitoso()
            st.balloons()
        else:
            st.warning("⚠️ Ingrese al menos una nota mayor a 0")

    # Historial de notas guardadas
    st.markdown("---")
    with st.expander("📊 Ver notas guardadas"):
        if gs:
            try:
                ws = gs._get_hoja('config')
                if ws:
                    data = ws.get_all_records()
                    notas_hist = []
                    for d in data:
                        clave = str(d.get('clave', ''))
                        if clave.startswith('nota_'):
                            try:
                                n = json.loads(d.get('valor', '{}'))
                                if n.get('grado') == grado_sel and n.get('area') == area_sel:
                                    notas_hist.append(n)
                            except Exception:
                                pass
                    if notas_hist:
                        df_n = pd.DataFrame(notas_hist)
                        st.dataframe(df_n[['nombre', 'nota', 'literal', 'bimestre', 'fecha']],
                                     use_container_width=True, hide_index=True)
                    else:
                        st.info("Sin notas guardadas para este grado/área")
            except Exception:
                st.info("Sin datos")


# ================================================================
# REPORTE INTEGRAL POR ESTUDIANTE — PDF COMPLETO
# ================================================================

def generar_reporte_integral_pdf(nombre, dni, grado, notas, asistencia, config):
    """Genera PDF completo: notas + asistencia + semáforo + recomendaciones"""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    # === PÁGINA 1: Datos + Notas ===
    # Encabezado con colores
    c.setFillColor(colors.HexColor("#1a56db"))
    c.rect(0, h-80, w, 80, fill=True)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(w/2, h-35, "INFORME INTEGRAL DEL ESTUDIANTE")
    c.setFont("Helvetica", 10)
    c.drawCentredString(w/2, h-55, f"I.E.P. ALTERNATIVO YACHAY — Año Escolar {config.get('anio', 2026)}")
    c.drawCentredString(w/2, h-70, f"Chinchero, Cusco — Perú")

    # Datos del estudiante
    c.setFillColor(colors.black)
    y = h - 110
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Estudiante: {nombre}")
    c.drawString(350, y, f"DNI: {dni}")
    y -= 18
    c.drawString(50, y, f"Grado: {grado}")
    c.drawString(350, y, f"Fecha: {fecha_peru_str()}")

    # Línea separadora
    y -= 12
    c.setStrokeColor(colors.HexColor("#1a56db"))
    c.setLineWidth(2)
    c.line(50, y, w-50, y)
    y -= 25

    # === SECCIÓN: NOTAS ===
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "📊 REGISTRO DE CALIFICACIONES")
    y -= 22

    if notas:
        # Header de tabla
        c.setFillColor(colors.HexColor("#1e293b"))
        c.rect(45, y-2, w-90, 16, fill=True)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 8)
        col_x = [50, 160, 300, 370, 420, 480]
        for i, header in enumerate(["Área", "Bimestre", "Nota", "Literal", "Semáforo", "Fecha"]):
            c.drawString(col_x[i], y+2, header)
        y -= 18

        c.setFillColor(colors.black)
        c.setFont("Helvetica", 7)
        promedios = {}
        for n in notas:
            area = str(n.get('area', ''))
            nota_val = float(n.get('nota', 0))
            literal = nota_a_letra(nota_val)
            col = color_semaforo(literal)

            if area not in promedios:
                promedios[area] = []
            promedios[area].append(nota_val)

            c.drawString(col_x[0], y, area[:22])
            c.drawString(col_x[1], y, str(n.get('bimestre', ''))[:15])
            c.drawString(col_x[2], y, f"{nota_val}/20")
            c.drawString(col_x[3], y, literal)
            c.setFillColor(colors.HexColor(col))
            c.circle(col_x[4]+12, y+3, 5, fill=True)
            c.setFillColor(colors.black)
            c.drawString(col_x[5], y, str(n.get('fecha', ''))[:10])
            y -= 13
            if y < 120:
                c.showPage()
                y = h - 60
                c.setFont("Helvetica", 7)

        # Resumen por áreas
        y -= 15
        if y < 200:
            c.showPage()
            y = h - 60

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.black)
        c.drawString(50, y, "📈 PROMEDIOS POR ÁREA")
        y -= 20

        total_all = []
        for area, notas_area in promedios.items():
            prom = round(sum(notas_area)/len(notas_area), 1)
            total_all.append(prom)
            lit = nota_a_letra(prom)
            col = color_semaforo(lit)

            c.setFont("Helvetica-Bold", 8)
            c.drawString(55, y, f"{area}:")
            c.drawString(220, y, f"{prom}/20 ({lit})")

            # Barra de progreso
            c.setFillColor(colors.HexColor("#e2e8f0"))
            c.rect(320, y-2, 150, 12, fill=True)
            c.setFillColor(colors.HexColor(col))
            c.rect(320, y-2, max(1, (prom/20)*150), 12, fill=True)
            c.setFillColor(colors.black)
            y -= 16
            if y < 100:
                c.showPage()
                y = h - 60

        # Promedio general
        if total_all:
            prom_gen = round(sum(total_all)/len(total_all), 1)
            lit_gen = nota_a_letra(prom_gen)
            col_gen = color_semaforo(lit_gen)
            y -= 10
            c.setFont("Helvetica-Bold", 14)
            c.drawString(55, y, f"PROMEDIO GENERAL: {prom_gen}/20")

            # Círculo semáforo grande
            c.setFillColor(colors.HexColor(col_gen))
            c.circle(350, y+5, 18, fill=True)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(350, y, lit_gen)
            c.setFillColor(colors.black)
    else:
        c.setFont("Helvetica", 10)
        c.drawString(55, y, "Sin calificaciones registradas.")

    # === Asistencia + Recomendaciones (misma página si cabe) ===
    # Solo nueva página si queda poco espacio
    if y < 250:
        c.showPage()
        y = h - 50
    else:
        y -= 25

    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.black)
    c.drawString(50, y, f"REGISTRO DE ASISTENCIA — {nombre}")
    y -= 22

    if asistencia:
        c.setFont("Helvetica", 8)
        total_dias = len(asistencia)
        c.drawString(55, y, f"Total de días registrados: {total_dias}")
        y -= 15
        for fecha_a, datos_a in sorted(asistencia.items())[:60]:
            entrada = datos_a.get('entrada', '—')
            salida = datos_a.get('salida', '—')
            c.drawString(55, y, f"📅 {fecha_a}: Entrada {entrada} | Salida {salida}")
            y -= 12
            if y < 100:
                c.showPage()
                y = h - 50
                c.setFont("Helvetica", 8)
    else:
        c.setFont("Helvetica", 10)
        c.drawString(55, y, "Sin registros de asistencia.")

    # Recomendaciones
    y -= 25
    if y < 200:
        c.showPage()
        y = h - 50

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "📝 RECOMENDACIONES PEDAGÓGICAS")
    y -= 20
    c.setFont("Helvetica", 8)

    if notas and total_all:
        lit_gen = nota_a_letra(prom_gen)
        info_lit = ESCALA_MINEDU.get(lit_gen, {})
        c.drawString(55, y, f"• Nivel de logro: {lit_gen} — {info_lit.get('nombre', '')}")
        y -= 13
        c.drawString(55, y, f"  {info_lit.get('desc', '')}")
        y -= 18

        recomendaciones = {
            'AD': [
                "Mantener el excelente ritmo académico con retos adicionales.",
                "Participar en concursos académicos para potenciar sus habilidades.",
                "Puede ayudar como tutor de compañeros con dificultades.",
                "Orientación vocacional: explorar carreras afines a sus fortalezas.",
            ],
            'A': [
                "Reforzar las áreas con menor puntaje para alcanzar nivel destacado.",
                "Establecer metas semanales de estudio.",
                "Lectura diaria de 30 minutos para fortalecer comprensión.",
                "Continuar con el buen hábito de estudio.",
            ],
            'B': [
                "Requiere acompañamiento permanente del docente y la familia.",
                "Sesiones de refuerzo en las áreas con menor calificación.",
                "Horario de estudio fijo en casa con supervisión del apoderado.",
                "Reuniones quincenales padres-docente para seguimiento.",
            ],
            'C': [
                "ATENCIÓN PRIORITARIA: Plan de recuperación inmediata.",
                "Evaluación psicopedagógica recomendada.",
                "Sesiones de refuerzo diarias con material adaptado.",
                "Reunión urgente con padres para establecer compromisos.",
                "Considerar factores emocionales o externos que afecten el aprendizaje.",
            ]
        }
        for rec in recomendaciones.get(lit_gen, []):
            c.drawString(55, y, f"• {rec}")
            y -= 12

    # Escala MINEDU
    y -= 20
    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "ESCALA DE CALIFICACIÓN — MINEDU Perú:")
    y -= 14
    c.setFont("Helvetica", 7)
    for sigla, info in ESCALA_MINEDU.items():
        c.setFillColor(colors.HexColor(info['color']))
        c.circle(60, y+3, 4, fill=True)
        c.setFillColor(colors.black)
        c.drawString(70, y, f"{sigla} ({info['min']}-{info['max']}): {info['nombre']}")
        y -= 11

    # Pie de página
    c.setFont("Helvetica-Oblique", 7)
    c.drawCentredString(w/2, 25, f"YACHAY PRO — Sistema de Gestión Educativa © {hora_peru().year}")
    c.drawCentredString(w/2, 15, "Documento generado automáticamente — Válido sin firma ni sello")

    c.save()
    buf.seek(0)
    return buf


# ================================================================
# FUNCIÓN PRINCIPAL
# ================================================================

def main():
    if st.session_state.rol is None:
        pantalla_login()
        st.stop()

    config = configurar_sidebar()

    # Saludo personalizado
    usuario = st.session_state.get('usuario_actual', '')
    usuarios = cargar_usuarios()
    nombre_usuario = usuarios.get(usuario, {}).get('label', usuario.capitalize())
    hora_actual = hora_peru().hour
    if hora_actual < 12:
        saludo = "☀️ Buenos días"
    elif hora_actual < 18:
        saludo = "🌤️ Buenas tardes"
    else:
        saludo = "🌙 Buenas noches"

    # ========================================
    # AUXILIAR — Solo asistencia + incidencias
    # ========================================
    if st.session_state.rol == "auxiliar":
        st.markdown(f"### {saludo}, **{nombre_usuario}** 👋")
        st.markdown("*¿Qué vamos a hacer hoy?*")
        ca1, ca2 = st.columns(2)
        with ca1:
            if st.button("📋\n\n**Asistencia**", use_container_width=True, key="aux_asist"):
                st.session_state.modulo_activo = "asistencia"
        with ca2:
            if st.button("📝\n\n**Incidencias**", use_container_width=True, key="aux_inc"):
                st.session_state.modulo_activo = "incidencias"

        mod = st.session_state.get('modulo_activo', 'asistencia')
        st.markdown("---")
        if mod == "asistencia":
            tab_asistencias()
        elif mod == "incidencias":
            tab_incidencias(config)

    # ========================================
    # DOCENTE — Su grado solamente
    # ========================================
    elif st.session_state.rol == "docente":
        st.markdown(f"### {saludo}, **{nombre_usuario}** 👋")
        st.markdown("*¿Qué vamos a hacer hoy?*")
        vista_docente(config)

    # ========================================
    # ADMIN / DIRECTIVO — Dashboard con íconos
    # ========================================
    elif st.session_state.rol in ["directivo", "admin"]:
        # Si no hay módulo seleccionado, mostrar dashboard
        if 'modulo_activo' not in st.session_state:
            st.session_state.modulo_activo = None

        if st.session_state.modulo_activo is None:
            # === DASHBOARD PRINCIPAL ===
            st.markdown(f"""
            <div class='main-header'>
                <h2 style='color:white;margin:0;'>{saludo}, {nombre_usuario} 👋</h2>
                <p style='color:#ccc;'>¿Qué vamos a hacer hoy?</p>
            </div>
            """, unsafe_allow_html=True)

            # Grid de módulos
            # Grid de módulos
            modulos = [
                ("📝", "Matrícula", "matricula", "#2563eb"),
                ("📋", "Asistencia", "asistencia", "#16a34a"),
                ("📄", "Documentos", "documentos", "#7c3aed"),
                ("🪪", "Carnets", "carnets", "#0891b2"),
                ("📊", "Calificación", "calificacion", "#dc2626"),
                ("📝", "Registrar Notas", "reg_notas", "#059669"),
                ("📈", "Reportes", "reportes", "#ea580c"),
                ("📝", "Incidencias", "incidencias", "#be185d"),
                ("💾", "Base Datos", "base_datos", "#4f46e5"),
            ]
            if st.session_state.rol == "admin":
                modulos.append(("📕", "Reclamaciones", "reclamaciones", "#92400e"))

            # Mostrar en grid de 3 columnas con colores
            for i in range(0, len(modulos), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    idx = i + j
                    if idx < len(modulos):
                        icono, nombre, key, color = modulos[idx]
                        with col:
                            st.markdown(f"""
                            <div onclick="window.location.hash='{key}'"
                                 style="background: linear-gradient(135deg, {color}, {color}dd);
                                        color: white; border-radius: 16px; padding: 20px;
                                        text-align: center; cursor: pointer;
                                        box-shadow: 0 4px 15px {color}40;
                                        transition: all 0.3s; margin: 6px 0;
                                        min-height: 100px; display: flex;
                                        flex-direction: column; justify-content: center;
                                        align-items: center;">
                                <span style="font-size: 2.2rem;">{icono}</span>
                                <strong style="font-size: 1rem; margin-top: 8px;">{nombre}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"Abrir {nombre}", key=f"dash_{key}",
                                        use_container_width=True):
                                st.session_state.modulo_activo = key
                                st.rerun()

            # Estadísticas rápidas
            st.markdown("---")
            stats = BaseDatos.obtener_estadisticas()
            s1, s2, s3 = st.columns(3)
            with s1:
                st.markdown(f"""<div class="stat-card">
                    <h3>📚 {stats['total_alumnos']}</h3>
                    <p>Alumnos Matriculados</p>
                </div>""", unsafe_allow_html=True)
            with s2:
                st.markdown(f"""<div class="stat-card">
                    <h3>👨‍🏫 {stats['total_docentes']}</h3>
                    <p>Docentes Registrados</p>
                </div>""", unsafe_allow_html=True)
            with s3:
                asis_hoy = BaseDatos.obtener_asistencias_hoy()
                st.markdown(f"""<div class="stat-card">
                    <h3>📋 {len(asis_hoy)}</h3>
                    <p>Asistencias Hoy</p>
                </div>""", unsafe_allow_html=True)

        else:
            # === MÓDULO SELECCIONADO ===
            if st.button("⬅️ Volver al Menú Principal", key="btn_volver"):
                st.session_state.modulo_activo = None
                st.rerun()

            st.markdown(f"### {saludo}, **{nombre_usuario}** 👋")

            mod = st.session_state.modulo_activo
            if mod == "matricula":
                tab_matricula(config)
            elif mod == "asistencia":
                tab_asistencias()
            elif mod == "documentos":
                tab_documentos(config)
            elif mod == "carnets":
                tab_carnets(config)
            elif mod == "calificacion":
                tab_calificacion_yachay(config)
            elif mod == "reg_notas":
                tab_registrar_notas(config)
            elif mod == "reportes":
                tab_reportes(config)
            elif mod == "incidencias":
                tab_incidencias(config)
            elif mod == "base_datos":
                tab_base_datos()
            elif mod == "reclamaciones":
                tab_libro_reclamaciones(config)


# ================================================================
# LIBRO DE RECLAMACIONES VIRTUAL
# ================================================================

def tab_libro_reclamaciones(config):
    """Libro de Reclamaciones Virtual según normativa MINEDU"""
    st.subheader("📕 Libro de Reclamaciones Virtual")
    st.markdown("*Según normativa del Ministerio de Educación*")

    gs = _gs()

    col1, col2 = st.columns([2, 1])
    with col1:
        with st.form("form_reclamo", clear_on_submit=True):
            st.markdown("### 📋 Registrar Reclamo")
            r_nombre = st.text_input("Nombre completo del reclamante:", key="r_nombre")
            r_dni = st.text_input("DNI:", key="r_dni")
            r_celular = st.text_input("Celular:", key="r_cel")
            r_tipo = st.selectbox("Tipo:", [
                "Queja", "Reclamo", "Sugerencia", "Denuncia"
            ], key="r_tipo")
            r_detalle = st.text_area("Detalle del reclamo:", key="r_detalle")
            r_submit = st.form_submit_button("📩 ENVIAR RECLAMO",
                                              type="primary",
                                              use_container_width=True)
            if r_submit:
                if r_nombre and r_dni and r_detalle:
                    codigo_rec = f"REC-{hora_peru().year}-{int(time.time()) % 10000:04d}"
                    if gs:
                        try:
                            ws = gs._get_hoja('config')
                            if ws:
                                ws.append_row([
                                    f"reclamo_{codigo_rec}",
                                    json.dumps({
                                        'codigo': codigo_rec,
                                        'nombre': r_nombre,
                                        'dni': r_dni,
                                        'celular': r_celular,
                                        'tipo': r_tipo,
                                        'detalle': r_detalle,
                                        'fecha': fecha_peru_str(),
                                        'hora': hora_peru_str(),
                                        'estado': 'Pendiente',
                                    }, ensure_ascii=False)
                                ])
                        except Exception:
                            pass
                    st.success(f"✅ Reclamo registrado exitosamente. Código: **{codigo_rec}**")
                    st.info("📌 Su reclamo será revisado por la dirección en un plazo de 72 horas.")
                else:
                    st.error("⚠️ Complete todos los campos obligatorios")

    with col2:
        st.markdown("### 📋 Reclamos Recibidos")
        if gs:
            try:
                ws = gs._get_hoja('config')
                if ws:
                    data = ws.get_all_records()
                    reclamos = [json.loads(d['valor']) for d in data
                               if str(d.get('clave', '')).startswith('reclamo_')]
                    if reclamos:
                        for rec in reversed(reclamos[-15:]):
                            estado = rec.get('estado', 'Pendiente')
                            emoji = "🟡" if estado == "Pendiente" else "🟢"
                            with st.expander(
                                f"{emoji} {rec.get('codigo', '')} — {rec.get('nombre', '')}"):
                                st.write(f"**Tipo:** {rec.get('tipo', '')}")
                                st.write(f"**Fecha:** {rec.get('fecha', '')}")
                                st.write(f"**Detalle:** {rec.get('detalle', '')}")
                                st.write(f"**Estado:** {estado}")
                    else:
                        st.info("📭 Sin reclamos registrados")
            except Exception:
                st.info("📭 Sin reclamos aún")
        else:
            st.warning("⚠️ Conecta Google Sheets")


if __name__ == "__main__":
    main()
