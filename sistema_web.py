import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Image as PlatypusImage, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
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
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SISTEMA YACHAY PRO", page_icon="🎓", layout="wide")

# --- CÓDIGO JAVASCRIPT PARA EL ESCÁNER (NO BORRAR) ---
# Este bloque permite usar la cámara en Web y Celular sin errores de servidor
CAMARA_HTML = """
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
    <div style="margin-bottom: 10px; font-weight: bold; color: #444;">👇 Apunta tu cámara al código QR 👇</div>
    <video id="video" style="width: 100%; max-width: 400px; border-radius: 10px; border: 4px solid #0052cc; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" autoplay playsinline></video>
    <canvas id="canvas" style="display: none;"></canvas>
    <div id="resultado" style="margin-top: 15px; padding: 10px; background-color: #e3f2fd; border-radius: 5px; color: #0052cc; font-weight: bold; width: 100%; max-width: 400px; text-align: center;">Esperando cámara...</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js"></script>
<script>
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const resultado = document.getElementById('resultado');
let scanning = true;

navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
.then(function(stream) {
    video.srcObject = stream;
    video.setAttribute("playsinline", true); 
    video.play();
    requestAnimationFrame(tick);
})
.catch(function(err) {
    resultado.innerText = "Error: No se pudo acceder a la cámara. Verifique permisos.";
});

function tick() {
    if (video.readyState === video.HAVE_ENOUGH_DATA && scanning) {
        canvas.height = video.videoHeight;
        canvas.width = video.videoWidth;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height, { inversionAttempts: "dontInvert" });
        
        if (code) {
            resultado.innerText = "✅ DNI DETECTADO: " + code.data;
            resultado.style.backgroundColor = "#d4edda";
            resultado.style.color = "#155724";
            
            // Lógica para enviar el dato a Streamlit
            try {
                const streamlitInput = window.parent.document.querySelector('input[aria-label="DNI detectado:"]');
                if (streamlitInput) {
                    streamlitInput.value = code.data;
                    streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
                    streamlitInput.dispatchEvent(new Event('change', { bubbles: true }));
                    // Hacemos una pausa para no escanear el mismo código mil veces por segundo
                    scanning = false;
                    setTimeout(() => { scanning = true; resultado.innerText = "Listo para siguiente..."; }, 3000);
                }
            } catch(e) { console.log(e); }
        }
    }
    requestAnimationFrame(tick);
}
</script>
"""

# --- INICIALIZACIÓN DE VARIABLES DE ESTADO ---
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
        'c_temp_gra': '', 
        'busqueda_counter': 0, 
        'asistencias_hoy': {}, 
        'registro_counter': 0, 
        'camara_activa': False, 
        'ultimo_dni_escaneado': '',
        'tipo_asistencia': 'Entrada'
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --- ESTILOS CSS ---
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 1rem;
    background: linear-gradient(90deg, #0052cc 0%, #003d99 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.stButton>button {
    width: 100%;
    border-radius: 5px;
    height: 3em;
}
div[data-testid="stMetricValue"] {
    font-size: 1.5rem;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: #f0f2f6;
    border-radius: 5px 5px 0 0;
    padding-top: 10px;
    padding-bottom: 10px;
}
.stTabs [aria-selected="true"] {
    background-color: #0052cc;
    color: white;
}
</style>
""", unsafe_allow_html=True)
# --- CLASE BASE DE DATOS ---
class BaseDatos:
    ARCHIVO = "datos_sistema.json"
    
    @classmethod
    def cargar_datos(cls):
        """Carga los datos del archivo JSON. Si no existe, crea uno vacío."""
        if os.path.exists(cls.ARCHIVO):
            try:
                with open(cls.ARCHIVO, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # Si el archivo está corrupto, retorna estructura vacía
                return {"alumnos": [], "asistencias": []}
        return {"alumnos": [], "asistencias": []}

    @classmethod
    def guardar_datos(cls, datos):
        """Guarda la estructura completa de datos en el archivo JSON."""
        with open(cls.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    @classmethod
    def registrar_estudiante(cls, nombre, dni, grado, apoderado="", dni_apoderado="", celular=""):
        """Registra un nuevo alumno verificando que el DNI no exista."""
        datos = cls.cargar_datos()
        
        # Verificar si ya existe el DNI
        for al in datos["alumnos"]:
            if al["DNI"] == dni:
                return False # Ya existe
        
        nuevo_alumno = {
            "Alumno": nombre.upper(),
            "DNI": dni,
            "Grado": grado.upper(),
            "Apoderado": apoderado.upper(),
            "DNI_Apoderado": dni_apoderado,
            "Celular": celular,
            "FechaRegistro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        datos["alumnos"].append(nuevo_alumno)
        cls.guardar_datos(datos)
        return True

    @classmethod
    def buscar_por_dni(cls, dni):
        """Busca un alumno por su DNI y devuelve sus datos."""
        datos = cls.cargar_datos()
        for al in datos["alumnos"]:
            if str(al["DNI"]).strip() == str(dni).strip():
                return al
        return None

    @classmethod
    def guardar_asistencia(cls, dni, nombre, tipo, hora):
        """Registra la asistencia de entrada o salida."""
        datos = cls.cargar_datos()
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        
        registro = {
            "Fecha": fecha_hoy,
            "Hora": hora,
            "DNI": dni,
            "Alumno": nombre,
            "Tipo": tipo,
            "Timestamp": time.time() # Útil para ordenar
        }
        
        if "asistencias" not in datos:
            datos["asistencias"] = []
            
        datos["asistencias"].append(registro)
        cls.guardar_datos(datos)

    @classmethod
    def obtener_asistencias_hoy(cls):
        """Devuelve una lista con las asistencias registradas HOY."""
        datos = cls.cargar_datos()
        hoy = datetime.now().strftime("%Y-%m-%d")
        if "asistencias" in datos:
            # Filtramos solo las de hoy y las ordenamos por hora (más reciente primero)
            asistencias_hoy = [x for x in datos["asistencias"] if x["Fecha"] == hoy]
            return sorted(asistencias_hoy, key=lambda x: x["Hora"], reverse=True)
        return []

    @classmethod
    def obtener_estadisticas(cls):
        """Calcula totales para el panel de administración."""
        datos = cls.cargar_datos()
        total_alumnos = len(datos.get("alumnos", []))
        total_asistencias = len(datos.get("asistencias", []))
        
        hoy = datetime.now().strftime("%Y-%m-%d")
        asistencias_hoy = len([x for x in datos.get("asistencias", []) if x["Fecha"] == hoy])
        
        return {
            "total_alumnos": total_alumnos,
            "total_asistencias": total_asistencias,
            "asistencias_hoy": asistencias_hoy
        }
        # --- CLASE GENERADOR PDF ---
class GeneradorPDF:
    @staticmethod
    def generar_constancia(datos_alumno, config, tipo_doc="matricula"):
        """Genera un PDF con la constancia solicitada."""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Marco decorativo
        c.setStrokeColor(colors.navy)
        c.setLineWidth(3)
        c.rect(30, 30, width-60, height-60)
        
        # Encabezado Institucional
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height - 80, "INSTITUCIÓN EDUCATIVA PRIVADA")
        c.setFont("Helvetica-Bold", 22)
        c.setFillColor(colors.navy)
        c.drawCentredString(width/2, height - 110, "YACHAY SCHOOL")
        
        # Título del Documento
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 18)
        titulo = "CONSTANCIA DE MATRÍCULA" if tipo_doc == "matricula" else "CONSTANCIA DE ESTUDIOS"
        c.drawCentredString(width/2, height - 180, titulo)
        
        # Cuerpo del texto
        styles = getSampleStyleSheet()
        style_body = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=12,
            leading=20,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        )
        
        fecha_actual = datetime.now().strftime("%d de %B del %Y")
        
        texto_contenido = f"""
        <br/><br/>
        La Dirección de la Institución Educativa Privada <b>"YACHAY SCHOOL"</b>, que suscribe la presente:
        <br/><br/>
        <b>HACE CONSTAR:</b>
        <br/><br/>
        Que el alumno(a): <b>{datos_alumno['Alumno']}</b>
        <br/><br/>
        Identificado con DNI N°: <b>{datos_alumno['DNI']}</b>
        <br/><br/>
        Se encuentra debidamente matriculado(a) en el grado: <b>{datos_alumno['Grado']}</b> de Educación Primaria,
        para el Año Académico <b>{config['anio']}</b>.
        <br/><br/>
        Se expide la presente a solicitud de la parte interesada para los fines que estime conveniente.
        <br/><br/><br/>
        <b>Cusco, {fecha_actual}</b>
        """
        
        p = Paragraph(texto_contenido, style_body)
        p.wrapOn(c, 450, 600)
        p.drawOn(c, 72, height - 550)
        
        # Firmas
        c.setLineWidth(1)
        c.line(100, 150, 250, 150)
        c.setFont("Helvetica", 10)
        c.drawCentredString(175, 135, config['directora'])
        c.drawCentredString(175, 120, "DIRECTORA")
        
        c.line(350, 150, 500, 150)
        c.drawCentredString(425, 135, config['promotor'])
        c.drawCentredString(425, 120, "PROMOTOR")
        
        # Frase pie de página
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(width/2, 50, f'"{config["frase"]}"')
        
        c.save()
        buffer.seek(0)
        return buffer

# --- CLASE GENERADOR CARNET ---
class GeneradorCarnet:
    @staticmethod
    def crear_carnet(alumno, config):
        """Crea una imagen PNG del carnet con código QR."""
        # Dimensiones estándar (aprox 600x370 px)
        ancho, alto = 600, 370
        
        # Crear lienzo blanco
        img = Image.new('RGB', (ancho, alto), color='white')
        d = ImageDraw.Draw(img)
        
        # --- DISEÑO DEL FONDO ---
        # Cabecera azul institucional
        d.rectangle([0, 0, ancho, 80], fill="#003366")
        # Pie de página dorado/amarillo
        d.rectangle([0, alto-40, ancho, alto], fill="#DAA520")
        
        # --- TEXTOS ESTATICOS ---
        try:
            # Intentar cargar fuentes del sistema si es posible (Linux/Windows)
            font_header = ImageFont.truetype("arialbd.ttf", 32)
            font_sub = ImageFont.truetype("arial.ttf", 16)
            font_field = ImageFont.truetype("arialbd.ttf", 18)
            font_val = ImageFont.truetype("arial.ttf", 18)
        except:
            # Fallback a fuente por defecto si no hay Arial
            font_header = ImageFont.load_default()
            font_sub = ImageFont.load_default()
            font_field = ImageFont.load_default()
            font_val = ImageFont.load_default()
            
        # Título Institución
        d.text((20, 20), "I.E.P. YACHAY SCHOOL", fill="white", font=font_header)
        d.text((20, 55), "Educación con Futuro", fill="#cccccc", font=font_sub)
        
        # --- DATOS DEL ALUMNO ---
        # Coordenadas iniciales
        x_labels = 30
        x_values = 150
        y_start = 110
        line_height = 40
        
        campos = [
            ("ESTUDIANTE:", alumno['Alumno']),
            ("DNI:", alumno['DNI']),
            ("GRADO:", alumno['Grado']),
            ("VIGENCIA:", f"AÑO {config['anio']}")
        ]
        
        for i, (label, valor) in enumerate(campos):
            y = y_start + (i * line_height)
            d.text((x_labels, y), label, fill="#003366", font=font_field)
            # Recortar nombre si es muy largo para que no se salga
            valor_safe = valor[:28] + "..." if len(valor) > 28 else valor
            d.text((x_values, y), valor_safe, fill="black", font=font_val)

        # --- CÓDIGO QR ---
        qr = qrcode.QRCode(box_size=4, border=2)
        qr.add_data(alumno['DNI']) # El QR contiene solo el DNI para lectura rápida
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Pegar QR a la derecha
        pos_qr = (430, 100)
        img.paste(qr_img, pos_qr)
        
        d.text((445, 230), "Escanea Aquí", fill="gray", font=font_sub)
        
        # --- PIE DE PÁGINA ---
        d.text((20, alto-30), f"Promotor: {config['promotor']}", fill="black", font=font_sub)
        
        return img
        # --- FUNCIONES DE PESTAÑAS ---

def tab_asistencias():
    st.markdown("## 📋 Registro Inteligente de Asistencias")
    st.markdown("---")
    
    # 1. Selector de Modo (Entrada/Salida)
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        if st.button("☀️ MARCAR ENTRADA", use_container_width=True, type="primary" if st.session_state.tipo_asistencia == "Entrada" else "secondary", key="btn_mode_entrada"):
            st.session_state.tipo_asistencia = "Entrada"
            st.rerun()
    with col_sel2:
        if st.button("🌙 MARCAR SALIDA", use_container_width=True, type="primary" if st.session_state.tipo_asistencia == "Salida" else "secondary", key="btn_mode_salida"):
            st.session_state.tipo_asistencia = "Salida"
            st.rerun()

    st.info(f"Modo Activo: **{st.session_state.tipo_asistencia.upper()}**")

    # 2. Área de Escáner y Validación
    col_cam, col_form = st.columns([1, 1], gap="medium")
    
    with col_cam:
        st.write("#### 📷 Escáner QR")
        activar_camara = st.checkbox("Encender Cámara", value=True, key="chk_camara")
        if activar_camara:
            # Aquí inyectamos el HTML del escáner definido en la PARTE 1
            components.html(CAMARA_HTML, height=450)
        else:
            st.warning("Cámara apagada. Marca la casilla para activar.")

    with col_form:
        st.write("#### 📝 Validación de Datos")
        st.markdown("El DNI aparecerá aquí automáticamente al escanear:")
        
        # ESTE INPUT ES EL QUE RECIBE EL DATO DEL JAVASCRIPT
        dni_detectado = st.text_input("DNI detectado:", key="input_dni_asistencia", help="Escanea el carnet o escribe manualmente")
        
        if st.button("✅ REGISTRAR ASISTENCIA", type="primary", use_container_width=True, key="btn_confirmar_asist"):
            if dni_detectado:
                alumno = BaseDatos.buscar_por_dni(dni_detectado)
                if alumno:
                    hora_actual = datetime.now().strftime('%H:%M:%S')
                    BaseDatos.guardar_asistencia(dni_detectado, alumno['Alumno'], st.session_state.tipo_asistencia, hora_actual)
                    
                    st.success(f"✅ ÉXITO: {st.session_state.tipo_asistencia} registrada para {alumno['Alumno']}")
                    st.balloons()
                    
                    # Generación de Mensaje WhatsApp
                    msg_wa = f"Hola, le informamos que el alumno(a) *{alumno['Alumno']}* ha registrado su *{st.session_state.tipo_asistencia}* a las *{hora_actual}*."
                    msg_encoded = urllib.parse.quote(msg_wa)
                    
                    st.markdown(f"""
                    <div style="background-color:#dcf8c6; padding:10px; border-radius:10px; border:1px solid #25D366; text-align:center;">
                        <p style="color:#075e54; margin:0;"><b>📲 Notificar al Apoderado:</b></p>
                        <a href="https://wa.me/51{alumno.get('Celular', '')}?text={msg_encoded}" target="_blank" style="text-decoration:none;">
                            <button style="background-color:#25D366; color:white; border:none; padding:8px 15px; border-radius:5px; margin-top:5px; cursor:pointer; font-weight:bold;">
                                Enviar WhatsApp
                            </button>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ ERROR: El DNI escaneado no pertenece a ningún alumno registrado.")
            else:
                st.warning("⚠️ Por favor escanee un código o ingrese un DNI.")

    # 3. Historial del Día
    st.divider()
    st.subheader("📊 Registros de Hoy")
    historial = BaseDatos.obtener_asistencias_hoy()
    
    if historial:
        df = pd.DataFrame(historial)
        # Seleccionamos columnas bonitas para mostrar
        # Aseguramos que existan las columnas antes de seleccionar
        cols_to_show = ['Hora', 'Alumno', 'DNI', 'Tipo']
        # Filtramos solo las que existen en el DF para evitar errores si está vacío
        cols_present = [c for c in cols_to_show if c in df.columns]
        
        if cols_present:
            df_show = df[cols_present]
            st.dataframe(df_show, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df, use_container_width=True)
    else:
        st.caption("No hay registros de asistencia el día de hoy.")

def tab_documentos(config):
    st.subheader("📄 Generación de Documentos")
    col1, col2 = st.columns([1, 2])
    with col1:
        dni_search = st.text_input("Ingrese DNI del Alumno:", key="doc_dni_search")
        tipo_doc = st.selectbox("Tipo de Documento:", ["Constancia de Matrícula", "Constancia de Estudios"], key="doc_type_sel")
        
    if st.button("🔍 Buscar y Generar", key="btn_gen_doc"):
        if dni_search:
            alumno = BaseDatos.buscar_por_dni(dni_search)
            if alumno:
                st.success(f"Alumno encontrado: {alumno['Alumno']}")
                
                # Generar PDF en memoria
                tipo_clave = "matricula" if "Matrícula" in tipo_doc else "estudios"
                pdf_buffer = GeneradorPDF.generar_constancia(alumno, config, tipo_clave)
                
                # Botón de descarga
                nombre_archivo = f"Constancia_{alumno['DNI']}.pdf"
                st.download_button(
                    label="⬇️ DESCARGAR DOCUMENTO PDF",
                    data=pdf_buffer,
                    file_name=nombre_archivo,
                    mime="application/pdf",
                    type="primary"
                )
            else:
                st.error("❌ No se encontró ningún alumno con ese DNI.")
        else:
            st.warning("⚠️ Ingrese un DNI.")

def tab_carnets(config):
    st.subheader("🪪 Generación de Carnets")
    
    tab_indiv, tab_masivo = st.tabs(["Individual", "Masivo (Por Grado)"])
    
    with tab_indiv:
        dni_carnet = st.text_input("DNI del Alumno:", key="carnet_dni_input")
        if st.button("Generar Carnet Individual", key="btn_carnet_indiv"):
            if dni_carnet:
                alumno = BaseDatos.buscar_por_dni(dni_carnet)
                if alumno:
                    img = GeneradorCarnet.crear_carnet(alumno, config)
                    st.image(img, caption=f"Vista previa: {alumno['Alumno']}", width=400)
                    
                    # Convertir a bytes para descarga
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button("⬇️ Descargar Carnet (PNG)", buf.getvalue(), f"Carnet_{alumno['DNI']}.png", "image/png")
                else:
                    st.error("Alumno no encontrado.")
    
    with tab_masivo:
        st.info("Genera todos los carnets de un salón en un archivo ZIP.")
        grado_sel = st.selectbox("Seleccione Grado:", ["1RO PRIMARIA", "2DO PRIMARIA", "3RO PRIMARIA", "4TO PRIMARIA", "5TO PRIMARIA", "6TO PRIMARIA"], key="grado_masivo_sel")
        
        if st.button("Generar Pack de Carnets", key="btn_carnet_masivo"):
            datos = BaseDatos.cargar_datos()
            alumnos_grado = [al for al in datos["alumnos"] if al["Grado"] == grado_sel]
            
            if alumnos_grado:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zf:
                    for al in alumnos_grado:
                        img = GeneradorCarnet.crear_carnet(al, config)
                        img_byte_arr = io.BytesIO()
                        img.save(img_byte_arr, format='PNG')
                        zf.writestr(f"Carnet_{al['Alumno']}.png", img_byte_arr.getvalue())
                
                st.success(f"Se generaron {len(alumnos_grado)} carnets.")
                st.download_button("⬇️ Descargar ZIP Carnets", zip_buffer.getvalue(), f"Carnets_{grado_sel}.zip", "application/zip")
            else:
                st.warning("No hay alumnos registrados en ese grado.")
                # --- FUNCIÓN PRINCIPAL (MAIN) ---
def main():
    # --- PANTALLA DE LOGIN ---
    if st.session_state.rol is None:
        st.markdown("<br>", unsafe_allow_html=True)
        col_login_izq, col_login_cent, col_login_der = st.columns([1, 2, 1])
        
        with col_login_cent:
            st.markdown("<div class='main-header'><h1>🔐 ACCESO AL SISTEMA</h1></div>", unsafe_allow_html=True)
            # Logo genérico de educación
            st.image("https://cdn-icons-png.flaticon.com/512/2942/2942813.png", width=120)
            
            usuario = st.text_input("Usuario:", key="login_usr")
            contrasena = st.text_input("Contraseña:", type="password", key="login_pwd")
            
            if st.button("INGRESAR AL SISTEMA", key="btn_login_main"):
                if usuario == "admin" and contrasena == "admin123":
                    st.session_state.rol = "admin"
                    st.rerun()
                elif usuario == "auxiliar" and contrasena == "123":
                    st.session_state.rol = "auxiliar"
                    st.rerun()
                elif usuario == "directivo" and contrasena == "dir123":
                    st.session_state.rol = "directivo"
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas. Intente nuevamente.")
            
            st.markdown("---")
            st.caption("© 2026 Sistema Yachay Pro - Versión Final")
        return

    # --- BARRA LATERAL (SIDEBAR) ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2942/2942813.png", width=80)
        st.title(f"Hola, {st.session_state.rol.upper()}")
        st.divider()
        
        # Configuración Global editable desde el sidebar
        st.subheader("⚙️ Configuración")
        anio_config = st.number_input("Año Escolar:", value=2026, step=1, key="conf_anio")
        dir_config = st.text_input("Directora:", value="Prof. Ana María Cusi", key="conf_dir")
        prom_config = st.text_input("Promotor:", value="Prof. Leandro Cordova", key="conf_prom")
        frase_config = st.text_input("Frase del Año:", value="Año de la Excelencia", key="conf_frase")
        
        config_data = {
            'anio': anio_config,
            'directora': dir_config,
            'promotor': prom_config,
            'frase': frase_config
        }
        
        st.divider()
        if st.button("🔴 CERRAR SESIÓN", type="primary", key="btn_logout"):
            st.session_state.rol = None
            st.rerun()

    # --- PANTALLAS SEGÚN ROL ---
    
    # 1. ROL AUXILIAR (Asistencia + Registro)
    if st.session_state.rol == "auxiliar":
        st.title("Panel de Auxiliar")
        tab1, tab2 = st.tabs(["📋 TOMAR ASISTENCIA", "➕ REGISTRAR ALUMNO"])
        
        with tab1:
            tab_asistencias()
            
        with tab2:
            st.subheader("Nuevo Registro de Estudiante")
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                reg_nombre = st.text_input("Nombre Completo:", key="aux_reg_nom")
                reg_dni = st.text_input("DNI Estudiante:", key="aux_reg_dni")
                reg_grado = st.selectbox("Grado:", ["1RO PRIMARIA", "2DO PRIMARIA", "3RO PRIMARIA", "4TO PRIMARIA", "5TO PRIMARIA", "6TO PRIMARIA"], key="aux_reg_grad")
            with col_r2:
                reg_apo = st.text_input("Nombre Apoderado:", key="aux_reg_apo")
                reg_dni_apo = st.text_input("DNI Apoderado:", key="aux_reg_dniapo")
                reg_cel = st.text_input("Celular Apoderado (51...):", key="aux_reg_cel")

            if st.button("💾 GUARDAR ESTUDIANTE", key="aux_btn_save"):
                if reg_nombre and reg_dni and reg_grado:
                    exito = BaseDatos.registrar_estudiante(reg_nombre, reg_dni, reg_grado, reg_apo, reg_dni_apo, reg_cel)
                    if exito:
                        st.success(f"✅ Estudiante {reg_nombre} registrado correctamente.")
                    else:
                        st.error("⚠️ El DNI ya existe en la base de datos.")
                else:
                    st.error("⚠️ Faltan datos obligatorios (Nombre, DNI, Grado).")

    # 2. ROL DIRECTIVO (Documentos + Carnets)
    elif st.session_state.rol == "directivo":
        st.title("Panel Directivo")
        tab1, tab2 = st.tabs(["📄 DOCUMENTOS", "🪪 CARNETS"])
        with tab1:
            tab_documentos(config_data)
        with tab2:
            tab_carnets(config_data)

    # 3. ROL ADMINISTRADOR (Todo + Base de Datos)
    elif st.session_state.rol == "admin":
        st.title("Panel Administrador")
        tab1, tab2, tab3, tab4 = st.tabs(["📋 ASISTENCIA", "📊 BASE DATOS", "📄 DOCUMENTOS", "🪪 CARNETS"])
        
        with tab1:
            tab_asistencias()
            
        with tab2:
            st.subheader("Base de Datos Completa")
            datos = BaseDatos.cargar_datos()
            
            col_db1, col_db2 = st.columns(2)
            with col_db1:
                st.write(f"**Total Alumnos:** {len(datos['alumnos'])}")
                if datos['alumnos']:
                    st.dataframe(pd.DataFrame(datos['alumnos']), use_container_width=True)
            
            with col_db2:
                st.write(f"**Total Asistencias:** {len(datos['asistencias'])}")
                if datos['asistencias']:
                    st.dataframe(pd.DataFrame(datos['asistencias']), use_container_width=True)

        with tab3:
            tab_documentos(config_data)
        with tab4:
            tab_carnets(config_data)

if __name__ == "__main__":
    main()
