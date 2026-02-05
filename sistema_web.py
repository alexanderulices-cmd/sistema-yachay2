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
import streamlit.components.v1 as components

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="SISTEMA YACHAY PRO", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESCÁNER QR JAVASCRIPT (MODIFICADO PARA STREAMLIT) ---
# Este es el bloque mágico que reemplaza a OpenCV
CAMARA_HTML = """
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
    <h3 style="color: #0052cc; margin-bottom: 10px;">📸 Escáner de Carnet</h3>
    <video id="video" style="width: 100%; max-width: 500px; border-radius: 10px; border: 4px solid #0052cc; box-shadow: 0 4px 10px rgba(0,0,0,0.1);" autoplay playsinline></video>
    <canvas id="canvas" style="display: none;"></canvas>
    <div id="status" style="margin-top: 15px; padding: 10px; border-radius: 5px; background-color: white; width: 100%; max-width: 500px; text-align: center; border: 1px solid #ddd;">
        <span style="font-weight: bold; color: #555;">Estado:</span> <span id="resultado" style="color: #0052cc;">Esperando cámara...</span>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js"></script>
<script>
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const resultado = document.getElementById('resultado');
const statusDiv = document.getElementById('status');
let scanning = true;

// Configuración de la cámara
navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
.then(function(stream) {
    video.srcObject = stream;
    video.setAttribute("playsinline", true); 
    video.play();
    requestAnimationFrame(tick);
})
.catch(function(err) {
    resultado.innerText = "Error: No se pudo acceder a la cámara. Verifique permisos.";
    resultado.style.color = "red";
});

function tick() {
    if (video.readyState === video.HAVE_ENOUGH_DATA && scanning) {
        canvas.height = video.videoHeight;
        canvas.width = video.videoWidth;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height, { inversionAttempts: "dontInvert" });
        
        if (code) {
            // QR ENCONTRADO
            const colorExito = "#d4edda";
            const textoExito = "#155724";
            
            resultado.innerText = "✅ DNI DETECTADO: " + code.data;
            statusDiv.style.backgroundColor = colorExito;
            resultado.style.color = textoExito;
            
            // INTENTO DE ENVIAR A STREAMLIT (INPUT OCULTO)
            try {
                // Buscamos cualquier input de texto disponible
                const inputs = window.parent.document.getElementsByTagName('input');
                for (let i = 0; i < inputs.length; i++) {
                    // Filtramos para encontrar el input correcto (el del DNI)
                    if (inputs[i].type === 'text' && !inputs[i].disabled) {
                        inputs[i].value = code.data;
                        inputs[i].dispatchEvent(new Event('input', { bubbles: true }));
                        inputs[i].dispatchEvent(new Event('change', { bubbles: true }));
                        break; 
                    }
                }
            } catch(e) { console.log(e); }
            
            // Pausa temporal para no leer el mismo código mil veces
            scanning = false;
            setTimeout(() => { 
                scanning = true; 
                resultado.innerText = "Listo para escanear..."; 
                statusDiv.style.backgroundColor = "white";
                resultado.style.color = "#0052cc";
            }, 3000);
        }
    }
    requestAnimationFrame(tick);
}
</script>
"""

# --- INICIALIZACIÓN DE ESTADO ---
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
        'camara_activa': False,
        'ultimo_dni_escaneado': '',
        'tipo_asistencia': 'Entrada',
        'registro_counter': 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --- ESTILOS CSS PRO ---
st.markdown("""
<style>
.main-header {text-align:center;padding:2rem;background:linear-gradient(135deg,#001e7c 0%,#0052cc 100%);
color:white;border-radius:10px;margin-bottom:2rem;box-shadow:0 4px 6px rgba(0,0,0,0.1);}
.success-msg {background:#d4edda;color:#155724;padding:1rem;border-radius:5px;
border-left:4px solid #28a745;margin:1rem 0;}
div.stButton > button:first-child {border-radius: 8px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Intentar cargar librería de código de barras (opcional)
try:
    from barcode import Code128
    from barcode.writer import ImageWriter
    HAS_BARCODE = True
except ImportError:
    HAS_BARCODE = False
    # --- CLASE BASE DE DATOS ---
class BaseDatos:
    ARCHIVO = "datos_sistema.json"
    
    @classmethod
    def cargar_datos(cls):
        if os.path.exists(cls.ARCHIVO):
            try:
                with open(cls.ARCHIVO, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"alumnos": [], "asistencias": []}
        return {"alumnos": [], "asistencias": []}

    @classmethod
    def guardar_datos(cls, datos):
        with open(cls.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    @classmethod
    def registrar_estudiante(cls, nombre, dni, grado, apoderado="", dni_apoderado="", celular=""):
        datos = cls.cargar_datos()
        
        # Validación de duplicados
        for al in datos.get("alumnos", []):
            if al["DNI"] == dni:
                return False
        
        nuevo_alumno = {
            "Alumno": nombre.upper(),
            "DNI": dni,
            "Grado": grado.upper(),
            "Apoderado": apoderado.upper(),
            "DNI_Apoderado": dni_apoderado,
            "Celular": celular,
            "FechaRegistro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if "alumnos" not in datos:
            datos["alumnos"] = []
            
        datos["alumnos"].append(nuevo_alumno)
        cls.guardar_datos(datos)
        return True

    @classmethod
    def buscar_por_dni(cls, dni):
        datos = cls.cargar_datos()
        # Búsqueda insensible a espacios
        dni_limpio = str(dni).strip()
        for al in datos.get("alumnos", []):
            if str(al["DNI"]).strip() == dni_limpio:
                return al
        return None
    
    @classmethod
    def buscar_por_nombre(cls, nombre_parcial):
        datos = cls.cargar_datos()
        resultados = []
        nombre_limpio = nombre_parcial.upper().strip()
        for al in datos.get("alumnos", []):
            if nombre_limpio in al["Alumno"]:
                resultados.append(al)
        return resultados

    @classmethod
    def guardar_asistencia(cls, dni, nombre, tipo, hora):
        datos = cls.cargar_datos()
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        
        registro = {
            "Fecha": fecha_hoy,
            "Hora": hora,
            "DNI": dni,
            "Alumno": nombre,
            "Tipo": tipo,
            "Timestamp": time.time()
        }
        
        if "asistencias" not in datos:
            datos["asistencias"] = []
            
        datos["asistencias"].append(registro)
        cls.guardar_datos(datos)

    @classmethod
    def obtener_asistencias_hoy(cls):
        datos = cls.cargar_datos()
        hoy = datetime.now().strftime("%Y-%m-%d")
        if "asistencias" in datos:
            # Filtramos solo las de hoy y ordenamos descendente por hora
            asistencias_hoy = [x for x in datos["asistencias"] if x["Fecha"] == hoy]
            return sorted(asistencias_hoy, key=lambda x: x["Hora"], reverse=True)
        return []

    @classmethod
    def obtener_estadisticas(cls):
        datos = cls.cargar_datos()
        total_alumnos = len(datos.get("alumnos", []))
        total_asistencias = len(datos.get("asistencias", []))
        
        hoy = datetime.now().strftime("%Y-%m-%d")
        asistencias_hoy_count = len([x for x in datos.get("asistencias", []) if x["Fecha"] == hoy])
        
        # Desglose por grado (opcional para gráficos futuros)
        grados = {}
        for al in datos.get("alumnos", []):
            g = al.get("Grado", "Sin Grado")
            grados[g] = grados.get(g, 0) + 1
            
        return {
            "total_alumnos": total_alumnos,
            "total_asistencias": total_asistencias,
            "asistencias_hoy": asistencias_hoy_count,
            "por_grado": grados
        }

    @classmethod
    def eliminar_alumno(cls, dni):
        # Función extra para administración
        datos = cls.cargar_datos()
        alumnos_orig = len(datos.get("alumnos", []))
        datos["alumnos"] = [al for al in datos.get("alumnos", []) if al["DNI"] != dni]
        
        if len(datos["alumnos"]) < alumnos_orig:
            cls.guardar_datos(datos)
            return True
        return False
        # --- CLASE GENERADOR PDF (CONSTANCIAS) ---
class GeneradorPDF:
    @staticmethod
    def generar_constancia(datos_alumno, config, tipo_doc="matricula"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # --- MARCO Y ESTILO ---
        c.setStrokeColor(colors.navy)
        c.setLineWidth(3)
        c.rect(30, 30, width-60, height-60)
        
        # --- ENCABEZADO ---
        logo_url = "https://cdn-icons-png.flaticon.com/512/2942/2942813.png" # Placeholder
        try:
            # Intentamos dibujar un logo si es accesible
            pass 
        except:
            pass
            
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height - 80, "INSTITUCIÓN EDUCATIVA PRIVADA")
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.navy)
        c.drawCentredString(width/2, height - 110, "YACHAY SCHOOL")
        
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(colors.black)
        c.drawCentredString(width/2, height - 130, "\"Educación con valores y excelencia académica\"")
        
        # --- TÍTULO ---
        c.setFont("Helvetica-Bold", 20)
        titulo = "CONSTANCIA DE MATRÍCULA" if tipo_doc == "matricula" else "CONSTANCIA DE ESTUDIOS"
        c.drawCentredString(width/2, height - 180, titulo)
        
        # --- CUERPO ---
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
        anio_actual = config.get('anio', 2026)
        
        texto_contenido = f"""
        <br/><br/>
        La Dirección de la Institución Educativa Privada <b>"YACHAY SCHOOL"</b>, hace constar por la presente:
        <br/><br/>
        Que el alumno(a):<br/>
        <b>{datos_alumno['Alumno']}</b>
        <br/><br/>
        Identificado con DNI N°: <b>{datos_alumno['DNI']}</b>
        <br/><br/>
        Se encuentra debidamente matriculado(a) en el grado: <b>{datos_alumno['Grado']}</b> de Educación Primaria,
        correspondiente al Año Académico <b>{anio_actual}</b>.
        <br/><br/>
        Se expide la presente a solicitud de la parte interesada para los fines que estime pertinente.
        <br/><br/><br/>
        <b>Cusco, {fecha_actual}</b>
        """
        
        p = Paragraph(texto_contenido, style_body)
        p.wrapOn(c, 450, 600)
        p.drawOn(c, 72, height - 550)
        
        # --- FIRMAS ---
        c.setLineWidth(1)
        c.line(100, 150, 250, 150)
        c.setFont("Helvetica", 10)
        c.drawCentredString(175, 135, config.get('directora', 'DIRECCION'))
        c.drawCentredString(175, 120, "DIRECTORA")
        
        c.line(350, 150, 500, 150)
        c.drawCentredString(425, 135, config.get('promotor', 'SECRETARIA'))
        c.drawCentredString(425, 120, "PROMOTOR/SECRETARÍA")
        
        # --- PIE DE PÁGINA ---
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(width/2, 50, f"\"{config.get('frase', 'Año del Bicentenario')}\"")
        
        c.save()
        buffer.seek(0)
        return buffer

# --- CLASE GENERADOR CARNET (IMAGEN PNG) ---
class GeneradorCarnet:
    @staticmethod
    def crear_carnet(alumno, config):
        # Dimensiones tipo tarjeta de crédito (Alta resolución)
        ancho, alto = 1016, 648  # Aprox CR80 a 300dpi
        
        img = Image.new('RGB', (ancho, alto), color='white')
        d = ImageDraw.Draw(img)
        
        # Colores
        azul_inst = "#003366"
        dorado = "#DAA520"
        gris_claro = "#f0f0f0"
        
        # --- FONDO ---
        # Cabecera
        d.rectangle([0, 0, ancho, 140], fill=azul_inst)
        # Pie
        d.rectangle([0, alto-60, ancho, alto], fill=dorado)
        
        # --- TIPOGRAFÍA ---
        try:
            # Intentar cargar fuentes del sistema si existen
            font_header = ImageFont.truetype("arialbd.ttf", 55)
            font_sub = ImageFont.truetype("arial.ttf", 28)
            font_field = ImageFont.truetype("arialbd.ttf", 32)
            font_val = ImageFont.truetype("arial.ttf", 32)
        except:
            font_header = ImageFont.load_default()
            font_sub = ImageFont.load_default()
            font_field = ImageFont.load_default()
            font_val = ImageFont.load_default()
            
        # Textos Cabecera
        d.text((40, 30), "I.E.P. YACHAY SCHOOL", fill="white", font=font_header)
        d.text((40, 95), "Educación, Valores y Cultura", fill=gris_claro, font=font_sub)
        d.text((ancho-150, 40), str(config.get('anio', 2026)), fill="white", font=font_header)
        
        # --- FOTO (Simulada) ---
        d.rectangle([50, 180, 270, 450], outline="gray", width=3)
        d.text((100, 300), "FOTO", fill="gray", font=font_header)
        
        # --- DATOS ALUMNO ---
        x_lbl = 320
        x_val = 500
        y_ini = 200
        sep = 60
        
        campos = [
            ("ALUMNO:", alumno['Alumno']),
            ("DNI:", alumno['DNI']),
            ("GRADO:", alumno['Grado']),
            ("SECCIÓN:", "U"), # Asumiendo sección única por defecto
            ("CÓDIGO:", f"E-{alumno['DNI']}")
        ]
        
        for i, (lbl, val) in enumerate(campos):
            y = y_ini + (i*sep)
            d.text((x_lbl, y), lbl, fill=azul_inst, font=font_field)
            # Recorte de nombre largo
            if len(val) > 25: val = val[:25] + "..."
            d.text((x_val, y), val, fill="black", font=font_val)

        # --- CÓDIGO QR ---
        # Generar QR
        qr = qrcode.QRCode(box_size=8, border=2)
        qr.add_data(alumno['DNI'])
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Pegar QR
        pos_qr = (ancho - 250, 250)
        img.paste(qr_img, pos_qr)
        
        d.text((ancho - 230, 460), "Escanea Aquí", fill="gray", font=font_sub)
        
        # --- PIE ---
        d.text((40, alto-45), f"Promotor: {config.get('promotor', 'Dirección General')}", fill="black", font=font_sub)
        
        return img
        # --- FUNCIONES DE PESTAÑAS (UI) ---

def tab_asistencias():
    st.markdown("## 📋 Control de Asistencias")
    st.markdown("---")
    
    # --- 1. SELECCIÓN DE MODO ---
    col_mode1, col_mode2 = st.columns(2)
    with col_mode1:
        if st.button("☀️ MARCAR ENTRADA", use_container_width=True, 
                     type="primary" if st.session_state.tipo_asistencia == "Entrada" else "secondary",
                     key="btn_mode_entrada"):
            st.session_state.tipo_asistencia = "Entrada"
            st.rerun()
            
    with col_mode2:
        if st.button("🌙 MARCAR SALIDA", use_container_width=True,
                     type="primary" if st.session_state.tipo_asistencia == "Salida" else "secondary",
                     key="btn_mode_salida"):
            st.session_state.tipo_asistencia = "Salida"
            st.rerun()
            
    st.info(f"Modo Activo: **{st.session_state.tipo_asistencia.upper()}**")

    # --- 2. ÁREA DE ESCÁNER ---
    col_cam, col_info = st.columns([1, 1.2])
    
    with col_cam:
        st.write("#### 📷 Escáner Web")
        activar = st.checkbox("Encender Cámara", value=True, key="chk_cam_asist")
        
        if activar:
            # Insertamos el componente JS definido en la Parte 1
            components.html(CAMARA_HTML, height=480)
        else:
            st.warning("Cámara desactivada. Marque la casilla para iniciar.")

    with col_info:
        st.write("#### 📝 Validación de Datos")
        st.caption("El DNI aparecerá automáticamente al escanear. También puede escribirlo.")
        
        # INPUT RECEPTOR DEL JS
        dni_leido = st.text_input("DNI Detectado:", key="input_dni_asist", 
                                  help="Campo autocompletado por el escáner")
        
        if st.button("✅ REGISTRAR ASISTENCIA", type="primary", use_container_width=True, key="btn_reg_asist"):
            if dni_leido:
                alumno = BaseDatos.buscar_por_dni(dni_leido)
                
                if alumno:
                    hora_actual = datetime.now().strftime('%H:%M:%S')
                    BaseDatos.guardar_asistencia(dni_leido, alumno['Alumno'], 
                                                 st.session_state.tipo_asistencia, hora_actual)
                    
                    st.balloons()
                    st.success(f"✅ REGISTRO EXITOSO")
                    st.markdown(f"**Alumno:** {alumno['Alumno']}")
                    st.markdown(f"**Hora:** {hora_actual}")
                    st.markdown(f"**Tipo:** {st.session_state.tipo_asistencia}")
                    
                    # --- MENSAJE WHATSAPP ---
                    celular = alumno.get('Celular', '')
                    mensaje_wa = f"Hola, informamos que el alumno(a) *{alumno['Alumno']}* ha registrado su *{st.session_state.tipo_asistencia}* a las *{hora_actual}*."
                    link_wa = f"https://wa.me/51{celular}?text={urllib.parse.quote(mensaje_wa)}"
                    
                    st.markdown("---")
                    st.markdown("##### 📲 Notificación:")
                    if celular:
                        st.markdown(f"""
                        <a href="{link_wa}" target="_blank" style="text-decoration:none;">
                            <button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:5px; font-weight:bold; cursor:pointer; width:100%;">
                                Enviar WhatsApp al Apoderado
                            </button>
                        </a>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("El alumno no tiene número de celular registrado.")
                        
                else:
                    st.error("❌ DNI no encontrado en la base de datos.")
            else:
                st.warning("⚠️ Ingrese un DNI válido.")

    # --- 3. TABLA DE HOY ---
    st.divider()
    st.subheader("📊 Registros de Hoy")
    historial = BaseDatos.obtener_asistencias_hoy()
    
    if historial:
        df = pd.DataFrame(historial)
        # Mostrar columnas relevantes
        cols_mostrar = [c for c in ['Hora', 'Alumno', 'Tipo', 'DNI'] if c in df.columns]
        st.dataframe(df[cols_mostrar], use_container_width=True, hide_index=True)
    else:
        st.info("No hay registros de asistencia el día de hoy.")
                        def tab_documentos(config):
    st.markdown("## 📄 Generación de Documentos")
    
    col_izq, col_der = st.columns([1, 2])
    
    with col_izq:
        st.markdown("### Configuración")
        tipo_doc = st.radio(
            "Seleccione Tipo de Documento:",
            ["Constancia de Matrícula", "Constancia de Estudios"],
            index=0
        )
        
        st.info("ℹ️ Los documentos se generan en formato PDF listos para imprimir.")

    with col_der:
        st.markdown("### Búsqueda de Alumno")
        dni_buscar = st.text_input("Ingrese DNI del Alumno:", key="doc_dni_search")
        nombre_buscar = st.text_input("O buscar por Nombre (parcial):", key="doc_nom_search")
        
        if st.button("🔍 BUSCAR ALUMNO", key="btn_doc_search"):
            st.session_state.busqueda_counter += 1
            
        # Lógica de búsqueda
        alumno_encontrado = None
        
        if dni_buscar:
            alumno_encontrado = BaseDatos.buscar_por_dni(dni_buscar)
        elif nombre_buscar:
            resultados = BaseDatos.buscar_por_nombre(nombre_buscar)
            if len(resultados) == 1:
                alumno_encontrado = resultados[0]
            elif len(resultados) > 1:
                st.warning(f"⚠️ Se encontraron {len(resultados)} coincidencias. Por favor sea más específico o use el DNI.")
                st.table(pd.DataFrame(resultados)[['Alumno', 'DNI', 'Grado']])
            else:
                st.error("No se encontraron coincidencias.")

        # Si se encontró un alumno, mostrar opciones
        if alumno_encontrado:
            st.success(f"✅ Alumno Seleccionado: **{alumno_encontrado['Alumno']}**")
            
            with st.expander("Ver Datos del Alumno", expanded=False):
                st.json(alumno_encontrado)
            
            # Generación del PDF
            tipo_clave = "matricula" if "Matrícula" in tipo_doc else "estudios"
            pdf_buffer = GeneradorPDF.generar_constancia(alumno_encontrado, config, tipo_clave)
            
            nombre_archivo = f"Constancia_{alumno_encontrado['DNI']}_{tipo_clave}.pdf"
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.download_button(
                    label="⬇️ DESCARGAR PDF",
                    data=pdf_buffer,
                    file_name=nombre_archivo,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            with col_d2:
                if st.button("🔄 Nueva Búsqueda", use_container_width=True):
                    st.rerun()
                        def tab_carnets(config):
    st.markdown("## 🪪 Centro de Carnetización")
    st.info("Generación de credenciales en alta resolución para impresión térmica o inyección de tinta.")
    
    tab_ind, tab_lote = st.tabs(["👤 Carnet Individual", "📦 Carnetización Masiva (Lote)"])
    
    # --- SUB-PESTAÑA: INDIVIDUAL ---
    with tab_ind:
        col_c1, col_c2 = st.columns([1, 1.5])
        
        with col_c1:
            dni_carnet = st.text_input("DNI del Alumno:", key="carnet_dni_search")
            if st.button("Buscar para Carnet", key="btn_carnet_search"):
                st.session_state.busqueda_counter += 1
                
        with col_c2:
            if dni_carnet:
                alumno = BaseDatos.buscar_por_dni(dni_carnet)
                if alumno:
                    st.success(f"Alumno: {alumno['Alumno']}")
                    
                    # Generar Previsualización
                    img_carnet = GeneradorCarnet.crear_carnet(alumno, config)
                    
                    # Mostrar Imagen
                    st.image(img_carnet, caption="Vista Previa (Anverso)", use_container_width=True)
                    
                    # Botón Descarga
                    buf = io.BytesIO()
                    img_carnet.save(buf, format="PNG")
                    st.download_button(
                        label="⬇️ DESCARGAR PNG (ALTA CALIDAD)",
                        data=buf.getvalue(),
                        file_name=f"Carnet_{alumno['DNI']}.png",
                        mime="image/png",
                        type="primary"
                    )
                else:
                    st.error("DNI no encontrado.")

    # --- SUB-PESTAÑA: MASIVA ---
    with tab_lote:
        st.markdown("#### Generación por Grado")
        st.write("Esta opción genera un archivo ZIP con todos los carnets de un salón.")
        
        grado_sel = st.selectbox(
            "Seleccione el Grado:",
            ["1° PRIMARIA", "2° PRIMARIA", "3° PRIMARIA", "4° PRIMARIA", "5° PRIMARIA", "6° PRIMARIA"],
            key="grado_lote"
        )
        
        if st.button(f"📦 PROCESAR CARNETS DE {grado_sel}", type="primary"):
            datos = BaseDatos.cargar_datos()
            alumnos_grado = [al for al in datos.get("alumnos", []) if al["Grado"] == grado_sel]
            
            if not alumnos_grado:
                st.warning(f"No hay alumnos registrados en {grado_sel}.")
            else:
                barra = st.progress(0)
                zip_buffer = io.BytesIO()
                total = len(alumnos_grado)
                
                with zipfile.ZipFile(zip_buffer, "w") as zf:
                    for i, al in enumerate(alumnos_grado):
                        # Generar imagen
                        img = GeneradorCarnet.crear_carnet(al, config)
                        img_byte = io.BytesIO()
                        img.save(img_byte, format="PNG")
                        
                        # Añadir al ZIP
                        nombre_file = f"{al['Grado']}_{al['Alumno']}_{al['DNI']}.png"
                        zf.writestr(nombre_file, img_byte.getvalue())
                        
                        # Actualizar barra
                        barra.progress((i + 1) / total)
                        time.sleep(0.05) # Pequeña pausa para no saturar
                
                st.success(f"✅ Proceso completado. Se generaron {total} carnets.")
                st.download_button(
                    label="⬇️ DESCARGAR PACK ZIP",
                    data=zip_buffer.getvalue(),
                    file_name=f"Carnets_{grado_sel}.zip",
                    mime="application/zip",
                    type="primary"
                )
                        # --- SIDEBAR Y CONFIGURACIÓN ---
def configurar_sidebar():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2942/2942813.png", width=100)
        
        # Si está logueado, mostrar info
        if st.session_state.rol:
            st.title(f"Hola, {st.session_state.rol.upper()}")
            st.divider()
            
            # CONFIGURACIÓN EDITABLE
            with st.expander("⚙️ Configuración Global", expanded=True):
                anio = st.number_input("Año Escolar:", value=2026, step=1, key="conf_anio")
                dir_n = st.text_input("Directora:", value="Prof. Ana María CUSI", key="conf_dir")
                prom_n = st.text_input("Promotor:", value="Prof. Leandro CORDOVA", key="conf_prom")
                frase = st.text_input("Lema:", value="Año de la Excelencia", key="conf_frase")
            
            st.divider()
            if st.button("🔴 CERRAR SESIÓN", type="primary", use_container_width=True):
                st.session_state.rol = None
                st.rerun()
                
            return {
                'anio': anio,
                'directora': dir_n,
                'promotor': prom_n,
                'frase': frase
            }
    return {}

# --- PANTALLA DE LOGIN ---
def pantalla_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    
    with col_l2:
        st.markdown("<div class='main-header'><h1>🔐 ACCESO AL SISTEMA</h1></div>", unsafe_allow_html=True)
        
        st.info("👋 Bienvenido al Sistema Yachay Pro")
        
        usuario = st.text_input("Usuario:", placeholder="Ej: admin", key="login_u")
        contrasena = st.text_input("Contraseña:", type="password", placeholder="••••••", key="login_p")
        
        if st.button("INGRESAR", use_container_width=True, type="primary"):
            # Credenciales Hardcoded (Seguro para demos)
            if usuario == "admin" and contrasena == "admin123":
                st.session_state.rol = "admin"
                st.rerun()
            elif usuario == "auxiliar" and contrasena == "123456789":
                st.session_state.rol = "auxiliar"
                st.rerun()
            elif usuario == "directivo" and contrasena == "dir123":
                st.session_state.rol = "directivo"
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas.")
        
        st.markdown("---")
        st.caption("© 2026 Yachay School - Versión Web Pro")
                        def tab_registro():
    st.markdown("## ➕ Registro de Nuevos Estudiantes")
    st.info("Ingrese los datos completos para generar ficha y carnet.")
    
    with st.form("form_registro_nuevo"):
        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("Apellidos y Nombres:")
            dni = st.text_input("DNI Estudiante:")
            grad = st.selectbox("Grado:", ["1° PRIMARIA", "2° PRIMARIA", "3° PRIMARIA", "4° PRIMARIA", "5° PRIMARIA", "6° PRIMARIA"])
        with c2:
            apo = st.text_input("Nombre Apoderado:")
            dni_apo = st.text_input("DNI Apoderado:")
            cel = st.text_input("Celular (WhatsApp):", help="Importante para notificaciones")
            
        btn_save = st.form_submit_button("💾 GUARDAR ESTUDIANTE", type="primary")
        
        if btn_save:
            if nom and dni and grad:
                exito = BaseDatos.registrar_estudiante(nom, dni, grad, apo, dni_apo, cel)
                if exito:
                    st.success("✅ Alumno registrado correctamente en la base de datos.")
                    # Reiniciar script para limpiar campos
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ El DNI ya existe en el sistema.")
            else:
                st.warning("⚠️ Complete los campos obligatorios (Nombre, DNI, Grado).")

def tab_base_datos():
    st.markdown("## 🗄️ Gestión de Base de Datos")
    st.warning("Zona de Administración. Los datos sensibles se muestran aquí.")
    
    datos = BaseDatos.cargar_datos()
    
    tab_a, tab_b = st.tabs(["📚 Alumnos Registrados", "⏱️ Historial de Asistencia"])
    
    with tab_a:
        df_al = pd.DataFrame(datos.get("alumnos", []))
        if not df_al.empty:
            st.dataframe(df_al, use_container_width=True)
            
            # Botón Descarga CSV
            csv = df_al.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Descargar Lista Alumnos (CSV)", csv, "alumnos.csv", "text/csv")
            
            # Opción Eliminar
            st.divider()
            st.write("🗑️ **Eliminar Alumno**")
            dni_del = st.text_input("DNI a eliminar:", key="del_dni")
            if st.button("ELIMINAR PERMANENTEMENTE", type="primary"):
                if BaseDatos.eliminar_alumno(dni_del):
                    st.success("Alumno eliminado.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("DNI no encontrado.")
        else:
            st.info("No hay alumnos registrados.")
            
    with tab_b:
        df_as = pd.DataFrame(datos.get("asistencias", []))
        if not df_as.empty:
            st.dataframe(df_as, use_container_width=True)
            csv_as = df_as.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Descargar Asistencias (CSV)", csv_as, "asistencias.csv", "text/csv")
        else:
            st.info("No hay historial de asistencia.")

# --- FUNCIÓN PRINCIPAL (MAIN) ---
def main():
    # 1. Verificar si hay usuario logueado
    if st.session_state.rol is None:
        pantalla_login()
    else:
        # 2. Cargar Sidebar y Configuración
        config = configurar_sidebar()
        rol = st.session_state.rol
        
        # 3. Mostrar Interfaz según ROL
        if rol == "admin":
            st.markdown("### 🛠️ Panel de Administrador")
            t1, t2, t3, t4, t5 = st.tabs([
                "📋 Asistencia", 
                "➕ Registro", 
                "📄 Documentos", 
                "🪪 Carnets", 
                "📊 Base de Datos"
            ])
            with t1: tab_asistencias()
            with t2: tab_registro()
            with t3: tab_documentos(config)
            with t4: tab_carnets(config)
            with t5: tab_base_datos()
            
        elif rol == "directivo":
            st.markdown("### 🎓 Panel Directivo")
            t1, t2 = st.tabs(["📄 Documentos", "🪪 Carnets"])
            with t1: tab_documentos(config)
            with t2: tab_carnets(config)
            
        elif rol == "auxiliar":
            st.markdown("### 🔔 Panel de Auxiliar")
            t1, t2 = st.tabs(["📋 Tomar Asistencia", "➕ Registrar Alumno"])
            with t1: tab_asistencias()
            with t2: tab_registro()

# --- PUNTO DE ENTRADA ---
if __name__ == "__main__":
    main()
