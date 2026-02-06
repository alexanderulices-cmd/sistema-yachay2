# ========================================
# SISTEMA YACHAY PRO - VERSIÓN DEFINITIVA
# ========================================
# Sistema completo de gestión educativa
# Módulos: Matrícula, Documentos, Carnets, Asistencia QR,
#          Sistema de Calificación Yachay (estilo ZipGrade)
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
from datetime import datetime, timedelta, timezone
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
# ZONA HORARIA PERÚ (UTC-5)
# ========================================
PERU_TZ = timezone(timedelta(hours=-5))

def hora_peru():
    return datetime.now(PERU_TZ)

def hora_peru_str():
    return hora_peru().strftime('%H:%M:%S')

def fecha_peru_str():
    return hora_peru().strftime('%Y-%m-%d')

# ========================================
# INICIALIZACIÓN
# ========================================

def init_session_state():
    defaults = {
        'rol': None, 'cola_carnets': [],
        'alumno': '', 'dni': '', 'grado': '',
        'apoderado': '', 'dni_apo': '',
        'c_temp_nom': '', 'c_temp_dni': '', 'c_temp_gra': '', 'c_temp_cel': '',
        'busqueda_counter': 0, 'asistencias_dia': [],
        'tipo_asistencia': 'Entrada', 'matricula_data': {},
        'activar_camara_asist': False, 'areas_examen': [], 'resultados_examen': [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

st.markdown("""
<style>
.main-header{text-align:center;padding:2rem;background:linear-gradient(135deg,#001e7c 0%,#0052cc 100%);color:white;border-radius:15px;margin-bottom:2rem;box-shadow:0 8px 16px rgba(0,0,0,0.2)}
.wa-btn{background:#25D366;color:white;padding:10px 20px;border:none;border-radius:8px;font-size:15px;cursor:pointer;width:100%;text-decoration:none;display:block;text-align:center;margin:4px 0}
.wa-btn:hover{background:#1da851}
.ranking-gold{background:linear-gradient(135deg,#FFD700,#FFA500);color:black;padding:10px;border-radius:8px;font-weight:bold;text-align:center;margin:5px 0}
.ranking-silver{background:linear-gradient(135deg,#C0C0C0,#A0A0A0);color:black;padding:10px;border-radius:8px;font-weight:bold;text-align:center;margin:5px 0}
.ranking-bronze{background:linear-gradient(135deg,#CD7F32,#B8860B);color:white;padding:10px;border-radius:8px;font-weight:bold;text-align:center;margin:5px 0}
</style>
""", unsafe_allow_html=True)

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
# CONSTANTES
# ========================================
NIVELES_GRADOS = {
    "INICIAL": ["Inicial 3 años", "Inicial 4 años", "Inicial 5 años"],
    "PRIMARIA": ["1° Primaria", "2° Primaria", "3° Primaria", "4° Primaria", "5° Primaria", "6° Primaria"],
    "SECUNDARIA": ["1° Secundaria", "2° Secundaria", "3° Secundaria", "4° Secundaria", "5° Secundaria"],
    "PREUNIVERSITARIO": ["Ciclo Regular", "Ciclo Intensivo", "Ciclo Verano"]
}
SECCIONES = ["Única", "A", "B"]
TODOS_LOS_GRADOS = [g for gs in NIVELES_GRADOS.values() for g in gs]
MESES_ASISTENCIA = ["Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
MESES_ESP = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]

ARCHIVO_BD = "base_datos.xlsx"
ARCHIVO_MATRICULA = "matricula.xlsx"
ARCHIVO_ASISTENCIAS = "asistencias.json"
ARCHIVO_RESULTADOS = "resultados_examenes.json"

# ========================================
# FUENTES
# ========================================
class RecursoManager:
    @staticmethod
    def obtener_fuente(nombre, tam, bold=False):
        try:
            for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "Roboto-Bold.ttf" if bold else "Roboto-Regular.ttf"]:
                if Path(f).exists():
                    return ImageFont.truetype(f, int(tam))
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()

# ========================================
# BASE DE DATOS
# ========================================
class BaseDatos:
    @staticmethod
    def cargar_matricula():
        try:
            if Path(ARCHIVO_MATRICULA).exists():
                df = pd.read_excel(ARCHIVO_MATRICULA, dtype=str, engine='openpyxl')
                df.columns = df.columns.str.strip()
                return df
            return pd.DataFrame(columns=['Nombre','DNI','Nivel','Grado','Seccion','Apoderado','DNI_Apoderado','Celular_Apoderado'])
        except:
            return pd.DataFrame(columns=['Nombre','DNI','Nivel','Grado','Seccion','Apoderado','DNI_Apoderado','Celular_Apoderado'])

    @staticmethod
    def guardar_matricula(df):
        df.to_excel(ARCHIVO_MATRICULA, index=False, engine='openpyxl')

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
        return True

    @staticmethod
    def buscar_por_dni(dni):
        df = BaseDatos.cargar_matricula()
        if df is not None and not df.empty and 'DNI' in df.columns:
            dni = str(dni).strip()
            df['DNI'] = df['DNI'].astype(str).str.strip()
            r = df[df['DNI'] == dni]
            if not r.empty:
                return r.iloc[0].to_dict()
        try:
            if Path(ARCHIVO_BD).exists():
                df2 = pd.read_excel(ARCHIVO_BD, dtype=str, engine='openpyxl')
                df2.columns = df2.columns.str.strip().str.title()
                if 'Dni' in df2.columns:
                    df2['Dni'] = df2['Dni'].astype(str).str.strip()
                    r2 = df2[df2['Dni'] == str(dni).strip()]
                    if not r2.empty:
                        row = r2.iloc[0].to_dict()
                        return {'Nombre': row.get('Alumno', row.get('Nombre','')), 'DNI': row.get('Dni',''),
                                'Grado': row.get('Grado',''), 'Nivel': row.get('Nivel',''), 'Seccion': row.get('Seccion',''),
                                'Apoderado': row.get('Apoderado',''), 'DNI_Apoderado': row.get('Dni_Apoderado', row.get('Dni Apoderado','')),
                                'Celular_Apoderado': row.get('Celular', row.get('Celular_Apoderado',''))}
        except:
            pass
        return None

    @staticmethod
    def eliminar_estudiante(dni):
        df = BaseDatos.cargar_matricula()
        df['DNI'] = df['DNI'].astype(str).str.strip()
        df = df[df['DNI'] != str(dni).strip()]
        BaseDatos.guardar_matricula(df)

    @staticmethod
    def guardar_asistencia(dni, nombre, tipo, hora):
        fecha = fecha_peru_str()
        asis = {}
        if Path(ARCHIVO_ASISTENCIAS).exists():
            with open(ARCHIVO_ASISTENCIAS, 'r', encoding='utf-8') as f:
                asis = json.load(f)
        if fecha not in asis:
            asis[fecha] = {}
        if dni not in asis[fecha]:
            asis[fecha][dni] = {'nombre': nombre, 'entrada': '', 'salida': ''}
        if tipo == 'entrada':
            asis[fecha][dni]['entrada'] = hora
        else:
            asis[fecha][dni]['salida'] = hora
        asis[fecha][dni]['nombre'] = nombre
        with open(ARCHIVO_ASISTENCIAS, 'w', encoding='utf-8') as f:
            json.dump(asis, f, indent=2, ensure_ascii=False)

    @staticmethod
    def obtener_asistencias_hoy():
        fecha = fecha_peru_str()
        if Path(ARCHIVO_ASISTENCIAS).exists():
            with open(ARCHIVO_ASISTENCIAS, 'r', encoding='utf-8') as f:
                return json.load(f).get(fecha, {})
        return {}

    @staticmethod
    def obtener_estadisticas():
        df = BaseDatos.cargar_matricula()
        if df is not None and not df.empty:
            return {'total_alumnos': len(df), 'grados': df['Grado'].nunique() if 'Grado' in df.columns else 0}
        return {'total_alumnos': 0, 'grados': 0}

    @staticmethod
    def guardar_resultados_examen(r):
        datos = []
        if Path(ARCHIVO_RESULTADOS).exists():
            with open(ARCHIVO_RESULTADOS, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        datos.append(r)
        with open(ARCHIVO_RESULTADOS, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    @staticmethod
    def cargar_resultados_examen():
        if Path(ARCHIVO_RESULTADOS).exists():
            with open(ARCHIVO_RESULTADOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

# ========================================
# GENERADOR PDF
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
            try: self.canvas.drawImage("fondo.png", 0, 0, width=self.width, height=self.height)
            except: pass

    def _dibujar_encabezado(self, titulo):
        self.canvas.setFont("Helvetica-Oblique", 11)
        self.canvas.drawCentredString(self.width/2, self.config['y_frase'], f'"{self.config["frase"]}"')
        self.canvas.setFont("Helvetica", 11)
        hoy = hora_peru()
        self.canvas.drawRightString(self.width-60, self.config['y_frase']-25, f"Chinchero, {hoy.day} de {MESES_ESP[hoy.month-1]} de {self.config['anio']}")
        self.canvas.setFont("Helvetica-Bold", 16)
        self.canvas.drawCentredString(self.width/2, self.config['y_titulo'], titulo)
        self.canvas.line(100, self.config['y_titulo']-5, self.width-100, self.config['y_titulo']-5)

    def _parrafo(self, texto, x, y, ancho, estilo):
        p = Paragraph(texto, estilo)
        w, h = p.wrap(ancho, 600)
        p.drawOn(self.canvas, x, y-h)
        return y-h-15

    def _qr(self, datos, tipo):
        data_qr = f"YACHAY|{tipo}|{datos.get('alumno',datos.get('Nombre',''))}|{datos.get('dni',datos.get('DNI',''))}|{hora_peru().strftime('%d/%m/%Y')}"
        qr = qrcode.QRCode(box_size=10, border=1); qr.add_data(data_qr); qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        tmp = "temp_qr.png"; img_qr.save(tmp)
        self.canvas.drawImage(tmp, self.config['qr_x'], self.config['qr_y'], width=70, height=70)
        self.canvas.setFont("Helvetica", 6)
        self.canvas.drawCentredString(self.config['qr_x']+35, self.config['qr_y']-5, "VERIFICACIÓN")
        try: os.remove(tmp)
        except: pass

    def _solicitante(self, datos, y):
        apo = datos.get('apoderado', datos.get('Apoderado','')).upper()
        dni = datos.get('dni_apo', datos.get('DNI_Apoderado',''))
        est = ParagraphStyle('S', parent=self.styles['Normal'], fontSize=10, leading=14, alignment=TA_JUSTIFY)
        return self._parrafo(f"Se expide a solicitud del Padre/Madre <b>{apo}</b> con DNI N° <b>{dni}</b>.", 60, y, self.width-120, est)

    def _firmas(self):
        yf = 110
        self.canvas.line(200, yf, 395, yf)
        self.canvas.setFont("Helvetica-Bold", 11)
        self.canvas.drawCentredString(self.width/2, yf-15, self.config['directora'].upper())
        self.canvas.setFont("Helvetica", 9)
        self.canvas.drawCentredString(self.width/2, yf-28, "DIRECTORA")

    def _fin(self):
        self.canvas.save(); self.buffer.seek(0); return self.buffer

    def generar_constancia_vacante(self, d):
        self._aplicar_fondo(); self._dibujar_encabezado("CONSTANCIA DE VACANTE")
        y=self.config['y_titulo']-50; mx=60; an=self.width-120
        e=ParagraphStyle('N',parent=self.styles['Normal'],fontSize=11,leading=15,alignment=TA_JUSTIFY)
        el=ParagraphStyle('L',parent=e,leftIndent=25)
        y=self._parrafo("La Dirección de la I.E.P. ALTERNATIVO YACHAY de Chinchero, representada por su Directora:",mx,y,an,e)
        self.canvas.setFont("Helvetica-Bold",12); self.canvas.drawString(mx,y,"CONSTANCIA DE VACANTE"); y-=25
        al=d.get('alumno',d.get('Nombre','')).upper(); dni=d.get('dni',d.get('DNI','')); gr=d.get('grado',d.get('Grado','')).upper()
        y=self._parrafo(f"Que la I.E. cuenta con <b>VACANTE DISPONIBLE</b> en {gr}, para <b>{al}</b>, DNI N° <b>{dni}</b>, año escolar <b>{self.config['anio']}</b>.",mx,y,an,e)
        y=self._parrafo("Para formalizar la matrícula, presentar:",mx,y,an,e)
        for r in ["• Certificado de Estudios del SIAGIE (original).","• Resolución de Traslado de Matrícula.","• Libreta de Notas del SIAGIE.",
                   "• Ficha Única de Matrícula del SIAGIE.","• Copia del DNI del estudiante.","• Constancia de No Adeudo.","• Folder o mica transparente."]:
            y=self._parrafo(r,mx,y,an,el)
        y=self._solicitante(d,y); self._firmas(); self._qr(d,"VACANTE"); return self._fin()

    def generar_constancia_no_deudor(self, d):
        self._aplicar_fondo(); self._dibujar_encabezado("CONSTANCIA DE NO ADEUDO")
        y=self.config['y_titulo']-50; mx=60; an=self.width-120
        e=ParagraphStyle('N',parent=self.styles['Normal'],fontSize=11,leading=15,alignment=TA_JUSTIFY)
        y=self._parrafo("La Dirección de la I.E.P. ALTERNATIVO YACHAY, representada por su Directora:",mx,y,an,e)
        self.canvas.setFont("Helvetica-Bold",12); self.canvas.drawString(mx,y,"HACE CONSTAR:"); y-=25
        al=d.get('alumno',d.get('Nombre','')).upper(); dni=d.get('dni',d.get('DNI',''))
        y=self._parrafo(f"Que <b>{al}</b>, DNI N° <b>{dni}</b>, ha cumplido con todas sus obligaciones económicas, no registrando deuda alguna.",mx,y,an,e)
        y=self._solicitante(d,y); self._firmas(); self._qr(d,"NO ADEUDO"); return self._fin()

    def generar_constancia_estudios(self, d):
        self._aplicar_fondo(); self._dibujar_encabezado("CONSTANCIA DE ESTUDIOS")
        y=self.config['y_titulo']-50; mx=60; an=self.width-120
        e=ParagraphStyle('N',parent=self.styles['Normal'],fontSize=11,leading=15,alignment=TA_JUSTIFY)
        y=self._parrafo("La Dirección de la I.E.P. ALTERNATIVO YACHAY, representada por su Directora:",mx,y,an,e)
        self.canvas.setFont("Helvetica-Bold",12); self.canvas.drawString(mx,y,"HACE CONSTAR:"); y-=25
        al=d.get('alumno',d.get('Nombre','')).upper(); dni=d.get('dni',d.get('DNI','')); gr=d.get('grado',d.get('Grado','')).upper()
        y=self._parrafo(f"Que <b>{al}</b>, DNI N° <b>{dni}</b>, se encuentra <b>MATRICULADO(A)</b> para el año <b>{self.config['anio']}</b>, cursando <b>{gr}</b>, conforme al SIAGIE.",mx,y,an,e)
        y=self._solicitante(d,y); self._firmas(); self._qr(d,"ESTUDIOS"); return self._fin()

    def generar_constancia_conducta(self, d):
        self._aplicar_fondo(); self._dibujar_encabezado("CONSTANCIA DE CONDUCTA")
        y=self.config['y_titulo']-50; mx=60; an=self.width-120
        e=ParagraphStyle('N',parent=self.styles['Normal'],fontSize=10,leading=14,alignment=TA_JUSTIFY)
        y=self._parrafo("La Dirección de la I.E.P. ALTERNATIVO YACHAY, representada por su Directora:",mx,y,an,e)
        self.canvas.setFont("Helvetica-Bold",12); self.canvas.drawString(mx,y,"CERTIFICA:"); y-=25
        al=d.get('alumno',d.get('Nombre','')).upper(); dni=d.get('dni',d.get('DNI',''))
        y=self._parrafo(f"Que <b>{al}</b>, DNI N° <b>{dni}</b>, obtuvo en <b>CONDUCTA</b>:",mx,y,an,e)
        y-=15; tx=self.width/2-200
        self.canvas.setFont("Helvetica-Bold",10)
        self.canvas.drawString(tx,y,"GRADO"); self.canvas.drawString(tx+120,y,"AÑO"); self.canvas.drawString(tx+280,y,"CALIFICACIÓN")
        y-=5; self.canvas.line(tx-10,y,tx+380,y); y-=20; self.canvas.setFont("Helvetica",9)
        ab=int(self.config['anio'])-5
        for i,g in enumerate(["PRIMERO","SEGUNDO","TERCERO","CUARTO","QUINTO"]):
            self.canvas.drawString(tx,y,g); self.canvas.drawString(tx+120,y,str(ab+i+1)); self.canvas.drawString(tx+280,y,d.get(f'nota_conducta_{i+1}','AD')); y-=18
        y-=10; y=self._solicitante(d,y); self._firmas(); self._qr(d,"CONDUCTA"); return self._fin()

    def generar_carta_compromiso(self, d):
        self._aplicar_fondo(); self._dibujar_encabezado("CARTA DE COMPROMISO")
        y=self.config['y_titulo']-40; mx=50; an=self.width-100
        e=ParagraphStyle('C',parent=self.styles['Normal'],fontSize=8.5,leading=11,alignment=TA_JUSTIFY)
        ei=ParagraphStyle('I',parent=e,leftIndent=10)
        apo=d.get('apoderado',d.get('Apoderado','')).upper(); dapo=d.get('dni_apo',d.get('DNI_Apoderado',''))
        al=d.get('alumno',d.get('Nombre','')).upper(); gr=d.get('grado',d.get('Grado','')).upper()
        y=self._parrafo(f"Yo, <b>{apo}</b>, DNI N° <b>{dapo}</b>, apoderado(a) de <b>{al}</b>, del <b>{gr}</b>, me comprometo a:",mx,y,an,e)
        for c in ["1. Velar por la asistencia puntual.","2. Supervisar tareas.","3. Uniformado(a) correctamente.",
                   "4. Inculcar respeto.","5. Participar en actividades.","6. Crianza positiva.","7. Atender problemas.",
                   "8. Responsabilidad por daños.","9. Vocabulario apropiado.","10. Acudir cuando sea requerido.",
                   "11. Asistir a reuniones.","12. Justificar inasistencias.","13. Pagar pensiones.","14. Respetar autonomía pedagógica."]:
            y=self._parrafo(c,mx,y,an,ei); y+=2
        y=120; self.canvas.line(80,y,200,y); self.canvas.line(220,y,340,y); self.canvas.line(360,y,480,y)
        y-=10; self.canvas.setFont("Helvetica-Bold",7)
        self.canvas.drawCentredString(140,y,"FIRMA APODERADO")
        self.canvas.drawCentredString(280,y,self.config['directora'].upper()); self.canvas.drawCentredString(280,y-10,"DIRECTORA")
        self.canvas.drawCentredString(420,y,self.config['promotor'].upper()); self.canvas.drawCentredString(420,y-10,"PROMOTOR")
        return self._fin()

    def generar_resolucion_traslado(self, d):
        self._aplicar_fondo()
        self.canvas.setFont("Helvetica-Oblique",11); self.canvas.drawCentredString(self.width/2,700,f'"{self.config["frase"]}"')
        y=670; self.canvas.setFont("Helvetica-Bold",14); self.canvas.drawCentredString(self.width/2,y,f"RESOLUCIÓN DIRECTORAL N° {d.get('num_resolucion','')}")
        y-=30; self.canvas.setFont("Helvetica",11); self.canvas.drawCentredString(self.width/2,y,d.get('fecha_resolucion',''))
        y-=40; mx=60; an=self.width-120; e=ParagraphStyle('N',parent=self.styles['Normal'],fontSize=11,leading=15,alignment=TA_JUSTIFY)
        al=d.get('alumno',d.get('Nombre','')).upper(); niv=d.get('nivel','').upper()
        self.canvas.setFont("Helvetica-Bold",11); self.canvas.drawString(mx,y,"VISTO:"); y-=20
        y=self._parrafo(f"Solicitud del apoderado de <b>{al}</b>, nivel <b>{niv}</b>.",mx,y,an,e)
        self.canvas.setFont("Helvetica-Bold",11); self.canvas.drawString(mx,y,"SE RESUELVE:"); y-=20
        t=[['ALUMNO',al],['NIVEL',niv],['IE PROCEDENCIA','IEP ALTERNATIVO YACHAY'],['IE DESTINO',d.get('ie_destino','').upper()]]
        tabla=Table(t,colWidths=[200,280])
        tabla.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.lightgrey),('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),('GRID',(0,0),(-1,-1),1,colors.black)]))
        tabla.wrapOn(self.canvas,an,200); tabla.drawOn(self.canvas,mx,y-80)
        y-=120; self.canvas.setFont("Helvetica-Bold",11); self.canvas.drawCentredString(self.width/2,y,"REGISTRE Y COMUNÍQUESE")
        self._firmas(); self._qr(d,"TRASLADO"); return self._fin()

# ========================================
# REGISTRO NOTAS / ASISTENCIA PDF
# ========================================
def generar_registro_notas_pdf(grado, seccion, anio, df):
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=landscape(A4)); w, h = landscape(A4)
    c.setFont("Helvetica-Bold",14); c.drawCentredString(w/2,h-30,"I.E.P. ALTERNATIVO YACHAY - REGISTRO DE EVALUACIÓN")
    c.setFont("Helvetica",10); c.drawCentredString(w/2,h-45,f"Grado: {grado} | Sección: {seccion} | Año: {anio}")
    areas=["MAT","COM","CT","PS","EF","ART","ING","REL","TUT"]
    hdr=["N°","APELLIDOS Y NOMBRES","DNI"]
    for a in areas:
        hdr+=[f"{a}\nB1",f"{a}\nB2",f"{a}\nB3",f"{a}\nB4",f"{a}\nPF"]
    data=[hdr]
    rows = df.iterrows() if not df.empty else [(i, {}) for i in range(15)]
    for idx, row in (df.iterrows() if not df.empty else []):
        f=[str(idx+1), row.get('Nombre',''), row.get('DNI','')]+[""]*45
        data.append(f)
    if df.empty:
        for i in range(15):
            data.append([str(i+1),""]+[""]*46)
    cw=[25,160,65]+[18,18,18,18,20]*9
    t=Table(data,colWidths=cw,repeatRows=1)
    t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,0),5),('FONTSIZE',(0,1),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.5,colors.black),('ALIGN',(0,0),(-1,-1),'CENTER'),('ALIGN',(1,1),(1,-1),'LEFT'),
        ('BACKGROUND',(0,0),(-1,0),colors.Color(0,0.2,0.5)),('TEXTCOLOR',(0,0),(-1,0),colors.white)]))
    tw,th=t.wrap(w-40,h-100); t.drawOn(c,20,h-75-th); c.save(); buf.seek(0); return buf

def generar_registro_asistencia_pdf(grado, seccion, anio, df):
    buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=landscape(A4)); w,h=landscape(A4)
    for mi,mes in enumerate(MESES_ASISTENCIA):
        if mi>0: c.showPage()
        c.setFont("Helvetica-Bold",12); c.drawCentredString(w/2,h-25,"I.E.P. ALTERNATIVO YACHAY - REGISTRO DE ASISTENCIA")
        c.setFont("Helvetica",9); c.drawCentredString(w/2,h-40,f"{grado} | {seccion} | {mes} {anio}")
        hdr=["N°","APELLIDOS Y NOMBRES"]+[str(d) for d in range(1,32)]+["A","T","F","J"]
        data=[hdr]
        if not df.empty:
            for idx,row in df.iterrows():
                data.append([str(idx+1),row.get('Nombre','')]+[""]*35)
        else:
            for i in range(20): data.append([str(i+1),""]+[""]*35)
        cw=[20,130]+[17]*31+[20,20,20,20]
        t=Table(data,colWidths=cw,repeatRows=1)
        t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,0),5.5),('FONTSIZE',(0,1),(-1,-1),6),
            ('GRID',(0,0),(-1,-1),0.4,colors.black),('ALIGN',(0,0),(-1,-1),'CENTER'),('ALIGN',(1,1),(1,-1),'LEFT'),
            ('BACKGROUND',(0,0),(-1,0),colors.Color(0,0.3,0.15)),('TEXTCOLOR',(0,0),(-1,0),colors.white)]))
        tw,th=t.wrap(w-30,h-80); t.drawOn(c,15,h-55-th)
        c.setFont("Helvetica",6); c.drawString(15,12,"A=Asistió|T=Tardanza|F=Falta|J=Justificada")
    c.save(); buf.seek(0); return buf

# ========================================
# CARNET (CORREGIDO: barcode sin choque, escudo fondo, texto dorado)
# ========================================
class GeneradorCarnet:
    W, H = 1012, 638
    AZUL, DORADO = (0,30,120), (255,215,0)

    def __init__(self, datos, anio, foto_bytes=None):
        self.datos, self.anio, self.foto_bytes = datos, anio, foto_bytes
        self.img = Image.new('RGB', (self.W, self.H), 'white')
        self.draw = ImageDraw.Draw(self.img)

    def _escudo_fondo(self):
        if Path("escudo_upload.png").exists():
            try:
                esc=Image.open("escudo_upload.png").convert("RGBA").resize((280,280),Image.LANCZOS)
                capa=Image.new('RGBA',(self.W,self.H),(255,255,255,0))
                capa.paste(esc,((self.W-280)//2,(self.H-280)//2))
                px=list(capa.getdata()); px=[(d[0],d[1],d[2],min(d[3],28)) for d in px]; capa.putdata(px)
                base=self.img.convert('RGBA'); base=Image.alpha_composite(base,capa)
                self.img=base.convert('RGB'); self.draw=ImageDraw.Draw(self.img)
            except: pass

    def _barras(self):
        self.draw.rectangle([(0,0),(self.W,210)],fill=self.AZUL)
        self.draw.rectangle([(0,207),(self.W,213)],fill=self.DORADO)
        self.draw.rectangle([(0,self.H-65),(self.W,self.H)],fill=self.AZUL)
        self.draw.rectangle([(0,self.H-68),(self.W,self.H-63)],fill=self.DORADO)

    def _textos(self):
        fh=RecursoManager.obtener_fuente("",36,True); fm=RecursoManager.obtener_fuente("",19,True)
        fc=RecursoManager.obtener_fuente("",17,True); fp=RecursoManager.obtener_fuente("",13,True)
        self.draw.text((self.W//2,65),"I.E. ALTERNATIVO YACHAY",font=fh,fill="white",anchor="mm")
        self.draw.text((self.W//2,115),'"EDUCAR PARA LA VIDA"',font=fm,fill=self.DORADO,anchor="mm")
        self.draw.text((self.W//2,160),f"CARNET ESCOLAR {self.anio}",font=fc,fill="white",anchor="mm")
        self.draw.text((self.W//2,self.H-35),"PIONEROS EN LA EDUCACIÓN DE CALIDAD",font=fp,fill=self.DORADO,anchor="mm")

    def _foto(self):
        x,y,w,h=40,228,220,280
        if self.foto_bytes:
            try:
                f=Image.open(self.foto_bytes).convert("RGB").resize((w,h),Image.LANCZOS); self.img.paste(f,(x,y))
            except: self._ph(x,y,w,h)
        else: self._ph(x,y,w,h)
        self.draw.rectangle([(x-3,y-3),(x+w+3,y+h+3)],outline=self.DORADO,width=4)

    def _ph(self,x,y,w,h):
        self.draw.rectangle([(x,y),(x+w,y+h)],fill="#eee")
        self.draw.text((x+w//2,y+h//2),"SIN FOTO",font=RecursoManager.obtener_fuente("",15),fill="#999",anchor="mm")

    def _datos(self):
        xt=290; nom=self.datos.get('alumno',self.datos.get('Nombre','')).upper()
        dni=str(self.datos.get('dni',self.datos.get('DNI',''))); gr=self.datos.get('grado',self.datos.get('Grado','N/A')).upper()
        sec=self.datos.get('seccion',self.datos.get('Seccion',''))
        fn=RecursoManager.obtener_fuente("",19 if len(nom)>25 else 22,True)
        fl=RecursoManager.obtener_fuente("",14,True); fd=RecursoManager.obtener_fuente("",14)
        yc=240
        if len(nom)>28:
            for l in textwrap.TextWrapper(width=28).wrap(nom)[:3]:
                self.draw.text((xt,yc),l,font=fn,fill="black"); yc+=26
        else:
            self.draw.text((xt,yc),nom,font=fn,fill="black"); yc+=30
        yc+=8
        self.draw.text((xt,yc),"DNI:",font=fl,fill="black"); self.draw.text((xt+60,yc),dni,font=fd,fill="black"); yc+=28
        self.draw.text((xt,yc),"GRADO:",font=fl,fill="black"); self.draw.text((xt+90,yc),gr,font=fd,fill="black"); yc+=28
        if sec:
            self.draw.text((xt,yc),"SECCIÓN:",font=fl,fill="black"); self.draw.text((xt+110,yc),str(sec),font=fd,fill="black"); yc+=28
        self.draw.text((xt,yc),"VIGENCIA:",font=fl,fill="black"); self.draw.text((xt+120,yc),str(self.anio),font=fd,fill="black")

    def _qr(self):
        try:
            dni=str(self.datos.get('dni',self.datos.get('DNI','')))
            qr=qrcode.QRCode(box_size=8,border=1); qr.add_data(dni); qr.make(fit=True)
            iq=qr.make_image(fill_color="black",back_color="white").resize((140,140),Image.LANCZOS)
            xq=self.W-180; yq=240; self.img.paste(iq,(xq,yq))
            self.draw.text((xq+70,yq+145),"ESCANEAR QR",font=RecursoManager.obtener_fuente("",9,True),fill="black",anchor="mm")
        except: pass

    def _barcode(self):
        if not HAS_BARCODE: return
        try:
            dni=str(self.datos.get('dni',self.datos.get('DNI','')))
            w=ImageWriter(); buf=io.BytesIO()
            Code128(dni,writer=w).write(buf,options={'write_text':False,'module_width':0.4,'module_height':8,'quiet_zone':2})
            buf.seek(0); ib=Image.open(buf); ib=ib.crop(ib.getbbox()); ib=ib.resize((280,45),Image.LANCZOS)
            xb=(self.W-280)//2; yb=self.H-120; self.img.paste(ib,(xb,yb))
            self.draw.text((self.W//2,yb+50),f"DNI: {dni}",font=RecursoManager.obtener_fuente("",10,True),fill="black",anchor="mm")
        except: pass

    def generar(self):
        self._escudo_fondo(); self._barras(); self._textos(); self._foto(); self._datos(); self._qr(); self._barcode()
        out=io.BytesIO(); self.img.save(out,format='PNG',optimize=True,quality=95); out.seek(0); return out

# ========================================
# UTILIDADES
# ========================================
def generar_link_whatsapp(tel, msg):
    t=str(tel).strip().replace("+","").replace(" ","").replace("-","")
    if len(t)==9: t="51"+t
    elif not t.startswith("51"): t="51"+t
    return f"https://wa.me/{t}?text={urllib.parse.quote(msg)}"

def generar_mensaje_asistencia(nombre, tipo, hora):
    sal="Buenos días" if int(hora.split(':')[0])<12 else "Buenas tardes"
    if tipo=="entrada":
        return f"{sal}\n🏫 I.E. ALTERNATIVO YACHAY\n✅ *ENTRADA*\n👤 {nombre}\n🕒 {hora}"
    return f"{sal}\n🏫 I.E. ALTERNATIVO YACHAY\n🏁 *SALIDA*\n👤 {nombre}\n🕒 {hora}"

def decodificar_qr_imagen(ib):
    if not HAS_PYZBAR: return None
    try:
        img=Image.open(io.BytesIO(ib)); cs=pyzbar_decode(img)
        if cs: return cs[0].data.decode('utf-8')
    except: pass
    if HAS_CV2:
        try:
            np_arr=np.frombuffer(ib,np.uint8); ic=cv2.imdecode(np_arr,cv2.IMREAD_COLOR)
            g=cv2.cvtColor(ic,cv2.COLOR_BGR2GRAY)
            for m in [cv2.THRESH_BINARY,cv2.THRESH_BINARY_INV]:
                _,th=cv2.threshold(g,127,255,m); cs=pyzbar_decode(Image.fromarray(th))
                if cs: return cs[0].data.decode('utf-8')
        except: pass
    return None

# ========================================
# LOGIN
# ========================================
def pantalla_login():
    c1,c2,c3=st.columns([1,2,1])
    with c2:
        st.markdown("""<div class='main-header'>
            <div style='font-size:60px'>🎓</div>
            <h1 style='color:white;margin:0'>SISTEMA YACHAY PRO</h1>
            <p style='color:#ccc'>Sistema Integral de Gestión Educativa</p>
            <p style='color:#FFD700;font-style:italic'>"Educar para la Vida"</p>
            <p style='color:#FFD700;font-size:0.9rem'>Pioneros en la Educación de Calidad</p>
            <hr style='border-color:#FFD700;margin:10px 50px'>
            <p style='color:#aaa;font-size:0.85rem'>📍 Chinchero, Cusco - Perú</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("""<div style='text-align:center;margin:10px 0'>
            <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Chinchero_BW.jpg/1200px-Chinchero_BW.jpg'
                 style='width:100%;max-width:500px;border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,0.2)'
                 onerror="this.style.display='none'" alt='Chinchero'>
        </div>""", unsafe_allow_html=True)
        pwd=st.text_input("🔑 Contraseña:",type="password",key="lp")
        if st.button("🔐 INGRESAR",use_container_width=True,type="primary"):
            roles={"306020":"admin","deyanira":"directivo","123456789":"auxiliar","987654321":"docente"}
            if pwd in roles:
                st.session_state.rol=roles[pwd]; st.rerun()
            else: st.error("⛔ Contraseña incorrecta")
        st.caption("👤 Admin | 📋 Directivo | 👤 Auxiliar | 👨‍🏫 Docente")

# ========================================
# SIDEBAR
# ========================================
def configurar_sidebar():
    with st.sidebar:
        st.title("🎓 YACHAY PRO")
        rn={"admin":"⚙️ Admin","directivo":"📋 Directivo","auxiliar":"👤 Auxiliar","docente":"👨‍🏫 Docente"}
        st.info(f"**{rn.get(st.session_state.rol,'')}**")
        st.caption(f"🕒 {hora_peru().strftime('%H:%M:%S')} | 📅 {hora_peru().strftime('%d/%m/%Y')}")
        st.markdown("---")
        dir_="Prof. Ana María CUSI INCA"; prom="Prof. Leandro CORDOVA TOCRE"
        frase="Año de la Esperanza y el Fortalecimiento de la Democracia"
        if st.session_state.rol=="admin":
            with st.expander("📂 Archivos"):
                ub=st.file_uploader("📊 Base Datos",type=["xlsx"],key="ub")
                if ub:
                    with open(ARCHIVO_BD,"wb") as f: f.write(ub.getbuffer())
                    st.success("✅"); st.rerun()
                uf=st.file_uploader("🖼️ Fondo docs",type=["png"],key="uf")
                if uf:
                    with open("fondo.png","wb") as f: f.write(uf.getbuffer())
                    st.success("✅")
                ue=st.file_uploader("🛡️ Escudo/Logo",type=["png"],key="ue")
                if ue:
                    with open("escudo_upload.png","wb") as f: f.write(ue.getbuffer())
                    st.success("✅")
            with st.expander("👥 Autoridades"):
                dir_=st.text_input("Directora:",dir_,key="di")
                prom=st.text_input("Promotor:",prom,key="pi")
            with st.expander("🎯 Título del Año"):
                frase=st.text_input("Frase/Título:",frase,key="fi")
                st.caption("Modifica según decreto del gobierno peruano cada año")
        st.markdown("---")
        anio=st.number_input("📅 Año:",2024,2040,2026,key="ai")
        st.metric("📚 Alumnos",BaseDatos.obtener_estadisticas()['total_alumnos'])
        st.markdown("---")
        if st.button("🔴 CERRAR SESIÓN",use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
    return {'anio':anio,'directora':dir_,'promotor':prom,'frase':frase,'y_frase':700,'y_titulo':630,'qr_x':435,'qr_y':47}

# ========================================
# TABS
# ========================================
def tab_matricula(config):
    st.header("📝 Matrícula")
    t1,t2,t3=st.tabs(["➕ Registrar","📋 Lista","⬇️ PDFs"])
    with t1:
        c1,c2=st.columns(2)
        with c1:
            nm=st.text_input("Apellidos y Nombres:",key="mn"); dn=st.text_input("DNI:",key="md",max_chars=8)
            nv=st.selectbox("Nivel:",list(NIVELES_GRADOS.keys()),key="mnv"); gr=st.selectbox("Grado:",NIVELES_GRADOS[nv],key="mg")
            sc=st.selectbox("Sección:",SECCIONES,key="ms")
        with c2:
            ap=st.text_input("Apoderado:",key="ma"); da=st.text_input("DNI Apoderado:",key="mda",max_chars=8)
            ce=st.text_input("Celular Apoderado:",key="mc",max_chars=9,placeholder="987654321")
        if st.button("✅ MATRICULAR",type="primary",use_container_width=True,key="bm"):
            if nm and dn:
                BaseDatos.registrar_estudiante({'Nombre':nm.strip(),'DNI':dn.strip(),'Nivel':nv,'Grado':gr,'Seccion':sc,
                    'Apoderado':ap.strip(),'DNI_Apoderado':da.strip(),'Celular_Apoderado':ce.strip()})
                st.success(f"✅ {nm} → {gr} {sc}"); st.balloons()
            else: st.error("⚠️ Nombre y DNI requeridos")
    with t2:
        df=BaseDatos.cargar_matricula()
        if not df.empty:
            c1,c2,c3=st.columns(3)
            with c1: fn=st.selectbox("Nivel:",["Todos"]+list(NIVELES_GRADOS.keys()),key="fn")
            with c2:
                go=["Todos"]+(NIVELES_GRADOS[fn] if fn!="Todos" else TODOS_LOS_GRADOS)
                fg=st.selectbox("Grado:",go,key="fg")
            with c3: bq=st.text_input("🔍",key="bq")
            d=df.copy()
            if fn!="Todos" and 'Nivel' in d.columns: d=d[d['Nivel']==fn]
            if fg!="Todos" and 'Grado' in d.columns: d=d[d['Grado']==fg]
            if bq: d=d[d.apply(lambda r:bq.lower() in str(r).lower(),axis=1)]
            st.metric("Resultados",len(d)); st.dataframe(d,use_container_width=True,hide_index=True,height=400)
            buf=io.BytesIO(); d.to_excel(buf,index=False,engine='openpyxl'); buf.seek(0)
            st.download_button("⬇️ Excel",buf,f"Matricula_{config['anio']}.xlsx",key="dme")
            with st.expander("🗑️ Eliminar"):
                dd=st.text_input("DNI:",key="dd")
                if st.button("🗑️",key="bd"):
                    if dd: BaseDatos.eliminar_estudiante(dd); st.rerun()
        else: st.info("📝 Sin estudiantes.")
    with t3:
        df=BaseDatos.cargar_matricula()
        if not df.empty:
            c1,c2=st.columns(2)
            with c1: np_=st.selectbox("Nivel:",list(NIVELES_GRADOS.keys()),key="pn"); gp=st.selectbox("Grado:",NIVELES_GRADOS[np_],key="pg")
            with c2: sp=st.selectbox("Sección:",SECCIONES,key="ps")
            dg=df.copy()
            if 'Grado' in dg.columns: dg=dg[dg['Grado']==gp]
            if 'Seccion' in dg.columns and sp!="Única": dg=dg[dg['Seccion']==sp]
            st.info(f"📊 {len(dg)} estudiantes")
            c1,c2=st.columns(2)
            with c1:
                if st.button("📝 Registro NOTAS",type="primary",use_container_width=True,key="gn"):
                    p=generar_registro_notas_pdf(gp,sp,config['anio'],dg)
                    st.download_button("⬇️",p,f"Notas_{gp}.pdf","application/pdf",key="dn")
            with c2:
                if st.button("📋 Registro ASISTENCIA",type="primary",use_container_width=True,key="ga"):
                    p=generar_registro_asistencia_pdf(gp,sp,config['anio'],dg)
                    st.download_button("⬇️",p,f"Asistencia_{gp}.pdf","application/pdf",key="da")

def tab_documentos(config):
    st.header("📄 Documentos")
    c1,c2=st.columns([1,2])
    with c1:
        td=st.selectbox("📑 Tipo:",["CONSTANCIA DE VACANTE","CONSTANCIA DE NO DEUDOR","CONSTANCIA DE ESTUDIOS",
            "CONSTANCIA DE CONDUCTA","CARTA COMPROMISO","RESOLUCIÓN DE TRASLADO"],key="td")
        st.markdown("---")
        db=st.text_input("🔍 DNI:",key="db")
        if st.button("🔎",use_container_width=True,key="bb"):
            r=BaseDatos.buscar_por_dni(db)
            if r:
                st.session_state.alumno=r.get('Nombre',''); st.session_state.dni=r.get('DNI','')
                st.session_state.grado=r.get('Grado',''); st.session_state.apoderado=r.get('Apoderado','')
                st.session_state.dni_apo=r.get('DNI_Apoderado',''); st.success("✅"); st.rerun()
            else: st.error("❌")
    with c2:
        with st.container(border=True):
            nm=st.text_input("👤 Nombre:",key="alumno"); dn=st.text_input("🆔 DNI:",key="dni")
            gr=st.text_input("📚 Grado:",key="grado"); ap=st.text_input("👨‍👩‍👧 Apoderado:",key="apoderado")
            da=st.text_input("🆔 DNI Apo:",key="dni_apo")
            nc={}
            if td=="CONSTANCIA DE CONDUCTA":
                cols=st.columns(5)
                for i,c in enumerate(cols):
                    with c: nc[f'nota_conducta_{i+1}']=st.selectbox(f"{i+1}°",["AD","A","B","C"],key=f"n{i}")
            ex={}
            if td=="RESOLUCIÓN DE TRASLADO":
                ex['num_resolucion']=st.text_input("N° Res:",key="nr"); ex['fecha_resolucion']=st.text_input("Fecha:",key="fr2")
                ex['nivel']=st.selectbox("Nivel:",["INICIAL","PRIMARIA","SECUNDARIA"],key="nl"); ex['ie_destino']=st.text_input("IE Dest:",key="ie")
                ex['nivel_destino']=st.text_input("Nivel Dest:",key="nd")
        if st.button("✨ GENERAR",type="primary",use_container_width=True,key="gd"):
            if nm and dn:
                d={'alumno':nm,'dni':dn,'grado':gr,'apoderado':ap,'dni_apo':da,**nc,**ex}
                g=GeneradorPDF(config)
                m={"CONSTANCIA DE VACANTE":g.generar_constancia_vacante,"CONSTANCIA DE NO DEUDOR":g.generar_constancia_no_deudor,
                   "CONSTANCIA DE ESTUDIOS":g.generar_constancia_estudios,"CONSTANCIA DE CONDUCTA":g.generar_constancia_conducta,
                   "CARTA COMPROMISO":g.generar_carta_compromiso,"RESOLUCIÓN DE TRASLADO":g.generar_resolucion_traslado}
                pdf=m[td](d); st.success("✅")
                st.download_button("⬇️ PDF",pdf,f"{nm}_{td}.pdf","application/pdf",use_container_width=True,key="dd2")

def tab_carnets(config):
    st.header("🪪 Carnets")
    t1,t2,t3=st.tabs(["⚡ Individual","📋 Desde Matrícula","📦 Lote"])
    with t1:
        c1,c2=st.columns(2)
        with c1:
            cn=st.text_input("👤",key="cn"); cd=st.text_input("🆔 DNI:",key="cd")
            cg=st.selectbox("📚",TODOS_LOS_GRADOS,key="cg"); cs=st.selectbox("📂",SECCIONES,key="cs")
        with c2:
            cf=st.file_uploader("📸 Foto:",type=['jpg','png','jpeg'],key="cf")
            if cf: st.image(cf,width=180)
        if st.button("🪪 GENERAR",type="primary",use_container_width=True,key="gc"):
            if cn and cd:
                fi=io.BytesIO(cf.getvalue()) if cf else None
                cr=GeneradorCarnet({'alumno':cn,'dni':cd,'grado':cg,'seccion':cs},config['anio'],fi).generar()
                st.image(cr,use_container_width=True)
                st.download_button("⬇️",cr,f"Carnet_{cn.replace(' ','_')}.png","image/png",use_container_width=True,key="dc")
    with t2:
        db=st.text_input("🔍 DNI:",key="cbd")
        if st.button("🔎",key="cbb"):
            a=BaseDatos.buscar_por_dni(db)
            if a: st.session_state['ce']=a; st.success(f"✅ {a.get('Nombre','')}")
            else: st.error("❌")
        if st.session_state.get('ce'):
            a=st.session_state['ce']
            st.markdown(f"**{a.get('Nombre','')}** | {a.get('Grado','')} {a.get('Seccion','')}")
            fm=st.file_uploader("📸",type=['jpg','png','jpeg'],key="cfm")
            if st.button("🪪 GENERAR",type="primary",use_container_width=True,key="gcm"):
                fi=io.BytesIO(fm.getvalue()) if fm else None
                cr=GeneradorCarnet(a,config['anio'],fi).generar()
                st.image(cr,use_container_width=True)
                st.download_button("⬇️",cr,f"Carnet.png","image/png",use_container_width=True,key="dcm")
    with t3:
        df=BaseDatos.cargar_matricula()
        if not df.empty:
            nl=st.selectbox("Nivel:",["Todos"]+list(NIVELES_GRADOS.keys()),key="ln")
            d=df.copy()
            if nl!="Todos" and 'Nivel' in d.columns: d=d[d['Nivel']==nl]
            st.info(f"📊 {len(d)} carnets")
            if st.button("🚀 GENERAR ZIP",type="primary",use_container_width=True,key="gl"):
                buf=io.BytesIO(); pr=st.progress(0)
                with zipfile.ZipFile(buf,"w",zipfile.ZIP_DEFLATED) as z:
                    for i,(_,r) in enumerate(d.iterrows()):
                        c=GeneradorCarnet(r.to_dict(),config['anio']).generar()
                        z.writestr(f"Carnet_{r.get('Nombre','').replace(' ','_')}.png",c.getvalue())
                        pr.progress((i+1)/len(d))
                buf.seek(0); st.balloons()
                st.download_button("⬇️ ZIP",buf,f"Carnets_{config['anio']}.zip","application/zip",use_container_width=True,key="dlz")

def tab_asistencias():
    st.header("📋 Asistencia")
    st.caption(f"🕒 **{hora_peru().strftime('%H:%M:%S')}** | 📅 {hora_peru().strftime('%d/%m/%Y')}")
    c1,c2=st.columns(2)
    with c1:
        if st.button("🌅 ENTRADA",use_container_width=True,type="primary" if st.session_state.tipo_asistencia=="Entrada" else "secondary",key="be"):
            st.session_state.tipo_asistencia="Entrada"; st.rerun()
    with c2:
        if st.button("🌙 SALIDA",use_container_width=True,type="primary" if st.session_state.tipo_asistencia=="Salida" else "secondary",key="bs"):
            st.session_state.tipo_asistencia="Salida"; st.rerun()
    st.info(f"📌 **{st.session_state.tipo_asistencia}**")
    st.markdown("---")
    cc,cm=st.columns(2)
    with cc:
        st.markdown("### 📸 Escanear QR")
        act=st.checkbox("📷 Activar cámara",key="chkc",value=st.session_state.get('activar_camara_asist',False))
        st.session_state.activar_camara_asist=act
        if act:
            foto=st.camera_input("Apunta al QR:",key="ca")
            if foto:
                d=decodificar_qr_imagen(foto.getvalue())
                if d: _reg_asist(d)
                else: st.warning("⚠️ No detectado")
        else: st.info("💡 Activa la cámara cuando necesites escanear")
    with cm:
        st.markdown("### ✏️ Manual")
        dm=st.text_input("DNI:",key="dm")
        if st.button("✅ REGISTRAR",type="primary",use_container_width=True,key="rm"):
            if dm: _reg_asist(dm.strip())
    st.markdown("---")
    st.subheader("📊 Hoy")
    asis=BaseDatos.obtener_asistencias_hoy()
    if asis:
        st.dataframe(pd.DataFrame([{'DNI':d,'Nombre':v['nombre'],'Entrada':v.get('entrada','—'),'Salida':v.get('salida','—')} for d,v in asis.items()]),use_container_width=True,hide_index=True)
        st.markdown("### 📱 WhatsApp")
        for dni,dat in asis.items():
            al=BaseDatos.buscar_por_dni(dni)
            if al:
                cel=al.get('Celular_Apoderado',al.get('Celular',''))
                if cel and cel.strip():
                    e=dat.get('entrada',''); s=dat.get('salida','')
                    msg=f"🏫 YACHAY\n👤 {dat['nombre']}\n✅ Entrada: {e or '—'}\n🏁 Salida: {s or '—'}"
                    st.markdown(f'<a href="{generar_link_whatsapp(cel,msg)}" target="_blank" class="wa-btn">📱 {dat["nombre"]} → {cel}</a>',unsafe_allow_html=True)

def _reg_asist(dni):
    al=BaseDatos.buscar_por_dni(dni)
    if al:
        h=hora_peru_str(); t=st.session_state.tipo_asistencia.lower(); n=al.get('Nombre',al.get('Alumno',''))
        BaseDatos.guardar_asistencia(dni,n,t,h)
        st.success(f"✅ **{n}** — {st.session_state.tipo_asistencia}: **{h}**"); st.balloons()
        cel=al.get('Celular_Apoderado',al.get('Celular',''))
        if cel and cel.strip():
            msg=generar_mensaje_asistencia(n,t,h)
            st.markdown(f'<a href="{generar_link_whatsapp(cel,msg)}" target="_blank" class="wa-btn">📱 WhatsApp → {cel}</a>',unsafe_allow_html=True)
    else: st.error(f"❌ DNI {dni} no encontrado")

# ========================================
# SISTEMA DE CALIFICACIÓN YACHAY (DOCENTES)
# ========================================
def tab_calificacion_yachay():
    st.header("📝 Sistema de Calificación YACHAY")
    st.caption("Genera hojas de respuestas, define claves por área, califica sobre 20 y genera ranking")
    tg,tc,tr=st.tabs(["📄 Generar Hoja","✅ Calificar","🏆 Ranking"])

    with tg:
        st.subheader("📄 Hoja de Respuestas")
        st.markdown("""**¿Cómo funciona?**
1. Genera e imprime la hoja de respuestas
2. Los alumnos rellenan los círculos con lápiz
3. Toma foto con la cámara dentro del sistema o ingresa las respuestas manualmente
4. El sistema califica automáticamente cada área sobre 20 puntos

💡 **Tip:** Buena iluminación + hoja plana = mejor detección""")
        c1,c2=st.columns(2)
        with c1: np_=st.selectbox("N° preguntas:",[10,20,30,40,50],index=1,key="npg")
        with c2: th=st.text_input("Título:","EVALUACIÓN BIMESTRAL",key="th")
        if st.button("📄 GENERAR",type="primary",use_container_width=True,key="gh"):
            h=_gen_hoja(np_,th); st.image(h,use_container_width=True)
            st.download_button("⬇️ PNG",h,f"Hoja_{th}_{np_}p.png","image/png",use_container_width=True,key="dh")

    with tc:
        st.subheader("✅ Calificar Examen")
        st.markdown("**1️⃣ Configura áreas** (cada una se califica sobre 20)")
        if 'areas_examen' not in st.session_state: st.session_state.areas_examen=[]
        ca,cn_,cb=st.columns([2,1,1])
        with ca: na=st.text_input("Área:",key="na")
        with cn_: nn=st.selectbox("Preguntas:",[5,10,15,20,25,30],index=1,key="nn")
        with cb:
            st.markdown("###")
            if st.button("➕ Agregar",key="aa"):
                if na: st.session_state.areas_examen.append({'nombre':na,'num':nn,'claves':''}); st.rerun()

        tp=0; tc_=[]
        ia=[] # info areas
        for i,a in enumerate(st.session_state.areas_examen):
            with st.expander(f"📚 {a['nombre']} ({a['num']}p → sobre 20)",expanded=True):
                cl=st.text_input(f"Claves:",value=a.get('claves',''),key=f"cl{i}",max_chars=a['num'])
                st.session_state.areas_examen[i]['claves']=cl.upper()
                ia.append({'nombre':a['nombre'],'num':a['num'],'claves':list(cl.upper())}); tc_.extend(list(cl.upper())); tp+=a['num']
                if len(st.session_state.areas_examen)>1:
                    if st.button("🗑️",key=f"d{i}"): st.session_state.areas_examen.pop(i); st.rerun()

        if ia: st.info(f"📊 {tp} preguntas en {len(ia)} áreas")

        st.markdown("---")
        st.markdown("**2️⃣ Alumno:**")
        de=st.text_input("DNI alumno:",key="de")
        if de:
            ae=BaseDatos.buscar_por_dni(de)
            if ae: st.success(f"👤 {ae.get('Nombre','')}")

        st.markdown("**3️⃣ Respuestas:**")
        met=st.radio("Método:",["✏️ Manual","📸 Cámara"],horizontal=True,key="met")
        ra=[]
        if met=="✏️ Manual":
            for i,a in enumerate(ia):
                r=st.text_input(f"{a['nombre']} ({a['num']}):",key=f"r{i}",max_chars=a['num'])
                ra.extend(list(r.upper()))
        else:
            ac=st.checkbox("📷 Activar cámara",key="chce")
            if ac:
                fe=st.camera_input("📷 Foto:",key="ce")
                if fe:
                    det=_proc_exam(fe.getvalue(),tp)
                    if det: ra=det; st.success(f"✅ {len(det)} detectadas")
                    else: st.warning("⚠️ No detectadas")

        st.markdown("---")
        if st.button("📊 CALIFICAR",type="primary",use_container_width=True,key="cal"):
            if tc_ and ra:
                ad=BaseDatos.buscar_por_dni(de) if de else None
                nm=ad.get('Nombre','') if ad else "Sin nombre"
                res={'fecha':hora_peru().strftime('%d/%m/%Y %H:%M'),'dni':de,'nombre':nm,'areas':[],'promedio_general':0}
                idx=0; sn=0
                mw=f"📝 *RESULTADOS*\n🏫 I.E. ALTERNATIVO YACHAY\n👤 {nm}\n📅 {hora_peru().strftime('%d/%m/%Y')}\n\n"
                for a in ia:
                    n=a['num']; ck=a['claves'][:n]; rk=ra[idx:idx+n]
                    ok=sum(1 for j in range(min(len(ck),len(rk))) if ck[j]==rk[j])
                    nota=round((ok/n)*20,1) if n else 0
                    lt="AD" if nota>=18 else "A" if nota>=14 else "B" if nota>=11 else "C"
                    res['areas'].append({'nombre':a['nombre'],'correctas':ok,'total':n,'nota':nota,'letra':lt,
                        'detalle':[{'p':idx+j+1,'c':ck[j] if j<len(ck) else '?','r':rk[j] if j<len(rk) else '?',
                                    'ok':j<len(ck) and j<len(rk) and ck[j]==rk[j]} for j in range(n)]})
                    sn+=nota; mw+=f"📚 *{a['nombre']}:* {nota}/20 ({lt}) — {ok}/{n}\n"; idx+=n
                pm=round(sn/len(ia),1) if ia else 0; lp="AD" if pm>=18 else "A" if pm>=14 else "B" if pm>=11 else "C"
                res['promedio_general']=pm; mw+=f"\n📊 *PROMEDIO: {pm}/20 ({lp})*\n✨ Sistema YACHAY"
                BaseDatos.guardar_resultados_examen(res)

                st.markdown("### 📊 Resultados")
                cols=st.columns(len(ia)+1)
                for i,ar in enumerate(res['areas']):
                    with cols[i]: st.metric(f"📚 {ar['nombre']}",f"{ar['nota']}/20",f"{ar['letra']} ({ar['correctas']}/{ar['total']})")
                with cols[-1]: st.metric("📊 PROMEDIO",f"{pm}/20",lp)

                for ar in res['areas']:
                    with st.expander(f"📋 {ar['nombre']}"):
                        st.dataframe(pd.DataFrame([{'#':d['p'],'Correcta':d['c'],'Marcada':d['r'],'':('✅' if d['ok'] else '❌')} for d in ar['detalle']]),use_container_width=True,hide_index=True)

                if ad:
                    cel=ad.get('Celular_Apoderado','')
                    if cel and cel.strip():
                        st.markdown(f'<a href="{generar_link_whatsapp(cel,mw)}" target="_blank" class="wa-btn">📱 Enviar resultados → {cel}</a>',unsafe_allow_html=True)
                st.balloons()
            else: st.error("⚠️ Configure claves y respuestas")

    with tr:
        st.subheader("🏆 Ranking")
        rs=BaseDatos.cargar_resultados_examen()
        if rs:
            rd=[{'Fecha':r.get('fecha',''),'Nombre':r.get('nombre',''),'DNI':r.get('dni',''),'Promedio':r.get('promedio_general',0),
                 'Áreas':', '.join([f"{a['nombre']}:{a['nota']}" for a in r.get('areas',[])])} for r in rs]
            df=pd.DataFrame(rd).sort_values('Promedio',ascending=False).reset_index(drop=True)
            df.insert(0,'#',range(1,len(df)+1))
            st.dataframe(df,use_container_width=True,hide_index=True)

            if len(df)>=1:
                st.markdown("### 🏆 Podio")
                cols=st.columns(min(3,len(df))); med=["🥇","🥈","🥉"]; est=["ranking-gold","ranking-silver","ranking-bronze"]
                for i in range(min(3,len(df))):
                    with cols[i]:
                        r=df.iloc[i]
                        st.markdown(f'<div class="{est[i]}">{med[i]} {r["Nombre"]}<br>Promedio: {r["Promedio"]}/20</div>',unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 📱 Enviar Individual")
            for _,row in df.iterrows():
                al=BaseDatos.buscar_por_dni(row['DNI']) if row['DNI'] else None
                if al:
                    cel=al.get('Celular_Apoderado','')
                    if cel and cel.strip():
                        ro=next((r for r in rs if r.get('dni')==row['DNI']),None)
                        if ro:
                            msg=f"📝 *RESULTADOS*\n🏫 YACHAY\n👤 {row['Nombre']}\n🏆 Puesto: {row['#']}°/{len(df)}\n"
                            for a in ro.get('areas',[]): msg+=f"📚 {a['nombre']}: {a['nota']}/20\n"
                            msg+=f"\n📊 *PROMEDIO: {row['Promedio']}/20*"
                            st.markdown(f'<a href="{generar_link_whatsapp(cel,msg)}" target="_blank" class="wa-btn">📱 #{row["#"]} {row["Nombre"]} — {row["Promedio"]}/20</a>',unsafe_allow_html=True)
            st.markdown("---")
            if st.button("🗑️ Limpiar Ranking",key="lr"):
                if Path(ARCHIVO_RESULTADOS).exists(): os.remove(ARCHIVO_RESULTADOS)
                st.success("✅"); st.rerun()
        else: st.info("📝 Corrige exámenes para ver el ranking.")

def tab_base_datos():
    st.header("📊 Base de Datos")
    df=BaseDatos.cargar_matricula()
    if not df.empty:
        c1,c2,c3=st.columns(3)
        with c1: st.metric("📚 Total",len(df))
        with c2: st.metric("🎓 Grados",df['Grado'].nunique() if 'Grado' in df.columns else 0)
        with c3: st.metric("📱 Con Cel",df['Celular_Apoderado'].notna().sum() if 'Celular_Apoderado' in df.columns else 0)
        st.markdown("---")
        c1,c2=st.columns(2)
        with c1:
            opts=['Todos']+(sorted(df['Grado'].dropna().unique().tolist()) if 'Grado' in df.columns else [])
            fg=st.selectbox("Filtrar:",opts,key="fbd")
        with c2: bq=st.text_input("🔍",key="bbd")
        d=df.copy()
        if fg!='Todos' and 'Grado' in d.columns: d=d[d['Grado']==fg]
        if bq: d=d[d.apply(lambda r:bq.lower() in str(r).lower(),axis=1)]
        st.dataframe(d,use_container_width=True,hide_index=True,height=500)
        c1,c2=st.columns(2)
        with c1: st.download_button("⬇️ CSV",d.to_csv(index=False).encode('utf-8'),"datos.csv","text/csv",key="dcsv")
        with c2:
            buf=io.BytesIO(); d.to_excel(buf,index=False,engine='openpyxl'); buf.seek(0)
            st.download_button("⬇️ Excel",buf,"datos.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",key="dxlsx")
    else: st.info("📝 Registra estudiantes.")

def _gen_hoja(np_,titulo):
    w,h=2480,3508; img=Image.new('RGB',(w,h),'white'); dr=ImageDraw.Draw(img)
    try:
        ft=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",70)
        fs=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",45)
        fn=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",40)
        fl=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",35)
    except: ft=fs=fn=fl=ImageFont.load_default()
    sz=80
    for p in [(50,50),(w-130,50),(50,h-130),(w-130,h-130)]: dr.rectangle([p,(p[0]+sz,p[1]+sz)],fill="black")
    dr.text((w//2,200),"I.E.P. ALTERNATIVO YACHAY",font=ft,fill="black",anchor="mm")
    dr.text((w//2,280),f"HOJA DE RESPUESTAS - {titulo.upper()}",font=fs,fill="black",anchor="mm")
    dr.text((w//2,350),"SISTEMA DE CALIFICACIÓN YACHAY",font=fs,fill="gray",anchor="mm")
    dr.text((200,480),"Nombre: ________________________________________",font=fs,fill="black")
    dr.text((200,560),"DNI: ________________  Grado: ________________",font=fs,fill="black")
    dr.text((200,640),f"Fecha: ________________  Preguntas: {np_}",font=fs,fill="black")
    dr.text((200,740),"Rellene completamente el círculo.",font=fl,fill="gray")
    sy,sx=900,300; sp=100; csp=700; ppc=min(25,(h-sy-200)//sp)
    for i in range(np_):
        col=i//ppc; fi=i%ppc; xb=sx+(col*csp); yb=sy+(fi*sp)
        dr.text((xb-100,yb),f"{i+1}.",font=fn,fill="black",anchor="rm")
        for j,l in enumerate(['A','B','C','D']):
            cx=xb+(j*130); dr.ellipse([(cx-35,yb-35),(cx+35,yb+35)],outline="black",width=4)
            dr.text((cx,yb),l,font=fl,fill="black",anchor="mm")
    out=io.BytesIO(); img.save(out,format='PNG'); out.seek(0); return out

def _proc_exam(ib,np_):
    if not HAS_CV2: return None
    try:
        na=np.frombuffer(ib,np.uint8); img=cv2.imdecode(na,cv2.IMREAD_COLOR)
        if img is None: return None
        g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); bl=cv2.GaussianBlur(g,(5,5),0)
        _,th=cv2.threshold(bl,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        cn,_=cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        bs=[]
        for c in cn:
            x,y,w,h=cv2.boundingRect(c); ar=w/float(h) if h else 0; area=cv2.contourArea(c)
            if 0.7<=ar<=1.3 and 15<=w<=120 and 15<=h<=120 and area>200: bs.append((c,x,y,w,h))
        if not bs: return None
        bs=sorted(bs,key=lambda b:b[2]); filas=[]; fa=[bs[0]]
        for b in bs[1:]:
            if abs(b[2]-fa[-1][2])<=30: fa.append(b)
            else:
                if len(fa)>=3: filas.append(sorted(fa,key=lambda b:b[1]))
                fa=[b]
        if len(fa)>=3: filas.append(sorted(fa,key=lambda b:b[1]))
        rs=[]
        for f in filas[:np_]:
            ops=f[:4]; its=[]
            for (ct,x,y,w,h) in ops:
                mk=np.zeros(g.shape,dtype="uint8"); cv2.drawContours(mk,[ct],-1,255,-1)
                ms=cv2.bitwise_and(th,th,mask=mk); its.append(cv2.countNonZero(ms))
            if its: rs.append(['A','B','C','D'][min(its.index(max(its)),3)])
            else: rs.append('?')
        return rs if rs else None
    except: return None

# ========================================
# MAIN
# ========================================
def main():
    if st.session_state.rol is None: pantalla_login(); st.stop()
    config=configurar_sidebar()
    if st.session_state.rol=="auxiliar":
        tab_asistencias()
    elif st.session_state.rol=="docente":
        tab_calificacion_yachay()
    elif st.session_state.rol in ["directivo","admin"]:
        tabs=st.tabs(["📝 MATRÍCULA","📄 DOCUMENTOS","🪪 CARNETS","📋 ASISTENCIAS","📊 BASE DATOS","📝 CALIFICACIÓN"])
        with tabs[0]: tab_matricula(config)
        with tabs[1]: tab_documentos(config)
        with tabs[2]: tab_carnets(config)
        with tabs[3]: tab_asistencias()
        with tabs[4]: tab_base_datos()
        with tabs[5]: tab_calificacion_yachay()

if __name__=="__main__": main()
