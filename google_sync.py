"""
YACHAY PRO — Módulo de Sincronización con Google Sheets
Almacena TODA la data de forma permanente en Google Sheets/Drive.
Las credenciales se leen de Streamlit Secrets (NUNCA en GitHub).
"""
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import json
import base64
import io
from datetime import datetime
import pandas as pd

# ================================================================
# CONFIGURACIÓN DE HOJAS
# ================================================================
HOJAS = {
    'matricula': 'Matricula',
    'docentes': 'Docentes',
    'usuarios': 'Usuarios',
    'asistencias': 'Asistencias',
    'resultados': 'Resultados',
    'incidencias': 'Incidencias',
    'config': 'Config',
    'fotos': 'Fotos',
    'historial_eval': 'HistorialEval',
    'materiales': 'Materiales',
    'examenes': 'Examenes',
}

COLUMNAS = {
    'matricula': ['nombre', 'dni', 'nivel', 'grado', 'seccion',
                   'apoderado', 'dni_apoderado', 'celular_apoderado',
                   'fecha_matricula'],
    'docentes': ['nombre', 'dni', 'cargo', 'especialidad', 'celular',
                  'grado_asignado', 'fecha_registro'],
    'usuarios': ['username', 'password_hash', 'nombre', 'rol',
                  'grado_asignado', 'nivel_asignado'],
    'asistencias': ['fecha', 'dni', 'nombre', 'tipo_persona',
                     'hora_entrada', 'hora_salida', 'grado', 'nivel'],
    'resultados': ['eval_id', 'eval_titulo', 'fecha', 'docente',
                    'estudiante', 'dni', 'grado',
                    'area', 'num_preguntas', 'claves',
                    'respuestas', 'correctas', 'total', 'nota', 'promedio'],
    'incidencias': ['codigo', 'fecha', 'hora', 'lugar', 'nivel', 'grado',
                     'seccion', 'tipo', 'afectados', 'implicados',
                     'reportante', 'dni_reportante', 'relato',
                     'accion_inmediata', 'compromisos', 'derivacion',
                     'registrado_por'],
    'fotos': ['dni', 'nombre', 'tipo', 'foto_base64', 'fecha'],
    'historial_eval': ['eval_id', 'fecha', 'docente', 'titulo', 'grado',
                        'areas_json', 'total_alumnos', 'promedio_general'],
    'config': ['clave', 'valor'],
    'materiales': ['id', 'docente', 'grado', 'semana', 'area',
                    'fecha_creacion', 'data_json'],
    'examenes': ['id', 'docente', 'grado', 'semana', 'area',
                  'fecha_creacion', 'data_json'],
}


# ================================================================
# CLASE PRINCIPAL DE SINCRONIZACIÓN
# ================================================================
class GoogleSync:
    """Maneja toda la comunicación con Google Sheets"""

    def __init__(self):
        self.client = None
        self.spreadsheet = None
        self.conectado = False
        self._cache = {}
        self._inicializar()

    def _inicializar(self):
        """Conectar a Google Sheets usando Streamlit Secrets"""
        try:
            if 'gcp_service_account' not in st.secrets:
                st.warning("⚠️ Google Sheets no configurado. "
                          "Los datos se guardan solo localmente.")
                return

            creds_dict = dict(st.secrets['gcp_service_account'])
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive',
            ]
            creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
            self.client = gspread.authorize(creds)

            sheet_id = st.secrets.get('google_sheets', {}).get(
                'spreadsheet_id', '')
            if sheet_id:
                self.spreadsheet = self.client.open_by_key(sheet_id)
            else:
                self.spreadsheet = self.client.open("YACHAY PRO — Base de Datos")

            self.conectado = True
            self._asegurar_hojas()
        except Exception as e:
            st.warning(f"⚠️ Error conectando Google Sheets: {str(e)[:100]}")
            self.conectado = False

    def _asegurar_hojas(self):
        """Crear hojas/pestañas que falten"""
        if not self.conectado:
            return
        try:
            hojas_existentes = [ws.title for ws in self.spreadsheet.worksheets()]
            for key, nombre in HOJAS.items():
                if nombre not in hojas_existentes:
                    ws = self.spreadsheet.add_worksheet(
                        title=nombre, rows=1000, cols=20)
                    # Agregar encabezados
                    if key in COLUMNAS:
                        ws.append_row(COLUMNAS[key])
        except Exception as e:
            st.warning(f"⚠️ Error creando hojas: {str(e)[:80]}")

    def _get_hoja(self, key):
        """Obtener worksheet por clave"""
        if not self.conectado:
            return None
        try:
            return self.spreadsheet.worksheet(HOJAS[key])
        except Exception:
            return None

    # ================================================================
    # LECTURA DE DATOS
    # ================================================================

    def leer_matricula(self):
        """Lee todos los estudiantes → DataFrame"""
        ws = self._get_hoja('matricula')
        if ws is None:
            return pd.DataFrame(columns=COLUMNAS['matricula'])
        try:
            data = ws.get_all_records()
            if not data:
                return pd.DataFrame(columns=COLUMNAS['matricula'])
            return pd.DataFrame(data)
        except Exception:
            return pd.DataFrame(columns=COLUMNAS['matricula'])

    def leer_docentes(self):
        """Lee todos los docentes → DataFrame"""
        ws = self._get_hoja('docentes')
        if ws is None:
            return pd.DataFrame(columns=COLUMNAS['docentes'])
        try:
            data = ws.get_all_records()
            if not data:
                return pd.DataFrame(columns=COLUMNAS['docentes'])
            return pd.DataFrame(data)
        except Exception:
            return pd.DataFrame(columns=COLUMNAS['docentes'])

    def leer_usuarios(self):
        """Lee todos los usuarios → dict {username: {...}}"""
        ws = self._get_hoja('usuarios')
        if ws is None:
            return {}
        try:
            data = ws.get_all_records()
            usuarios = {}
            for row in data:
                uname = str(row.get('username', '')).strip()
                if not uname:
                    continue
                # SIEMPRE convertir password a string (GS puede convertir a número)
                pwd = str(row.get('password_hash', '')).strip()
                # Limpiar .0 si GS lo convirtió a float
                if pwd.endswith('.0'):
                    pwd = pwd[:-2]
                usuarios[uname] = {
                    'password': pwd,
                    'label': str(row.get('nombre', uname)).strip(),
                    'nombre': str(row.get('nombre', '')).strip(),
                    'rol': str(row.get('rol', 'docente')).strip(),
                    'grado': str(row.get('grado_asignado', '')).strip(),
                    'nivel': str(row.get('nivel_asignado', '')).strip(),
                }
            return usuarios
        except Exception:
            return {}

    def leer_asistencias(self, fecha=None, grado=None, mes=None, anio=None):
        """Lee asistencias con filtros opcionales"""
        ws = self._get_hoja('asistencias')
        if ws is None:
            return []
        try:
            data = ws.get_all_records()
            resultados = data
            if fecha:
                resultados = [r for r in resultados if r.get('fecha') == fecha]
            if grado:
                resultados = [r for r in resultados if r.get('grado') == grado]
            if mes and anio:
                resultados = [r for r in resultados
                             if r.get('fecha', '').startswith(f"{anio}-{mes:02d}")]
            return resultados
        except Exception:
            return []

    def leer_resultados(self, eval_id=None, dni=None, grado=None):
        """Lee resultados de exámenes con filtros"""
        ws = self._get_hoja('resultados')
        if ws is None:
            return []
        try:
            data = ws.get_all_records()
            if eval_id:
                data = [r for r in data if str(r.get('eval_id')) == str(eval_id)]
            if dni:
                data = [r for r in data if r.get('dni') == dni]
            if grado:
                data = [r for r in data if r.get('grado') == grado]
            return data
        except Exception:
            return []

    def leer_historial_evaluaciones(self, docente=None):
        """Lee historial de evaluaciones"""
        ws = self._get_hoja('historial_eval')
        if ws is None:
            return []
        try:
            data = ws.get_all_records()
            if docente:
                data = [r for r in data if r.get('docente') == docente]
            return data
        except Exception:
            return []

    def leer_incidencias(self):
        """Lee todas las incidencias"""
        ws = self._get_hoja('incidencias')
        if ws is None:
            return []
        try:
            return ws.get_all_records()
        except Exception:
            return []

    def leer_foto(self, dni):
        """Lee foto base64 de un DNI"""
        ws = self._get_hoja('fotos')
        if ws is None:
            return None
        try:
            data = ws.get_all_records()
            for row in data:
                if str(row.get('dni')) == str(dni):
                    return row.get('foto_base64', '')
            return None
        except Exception:
            return None

    # ================================================================
    # ESCRITURA DE DATOS
    # ================================================================

    def guardar_estudiante(self, datos):
        """Agrega o actualiza un estudiante"""
        ws = self._get_hoja('matricula')
        if ws is None:
            return False
        try:
            row = [datos.get(c, '') for c in COLUMNAS['matricula']]
            # Buscar si ya existe por DNI
            cell = ws.find(str(datos.get('dni', '')))
            if cell:
                ws.update(f'A{cell.row}:I{cell.row}', [row])
            else:
                ws.append_row(row)
            return True
        except Exception as e:
            st.error(f"Error guardando estudiante: {e}")
            return False

    def eliminar_estudiante(self, dni):
        """Elimina un estudiante por DNI"""
        ws = self._get_hoja('matricula')
        if ws is None:
            return False
        try:
            cell = ws.find(str(dni))
            if cell:
                ws.delete_rows(cell.row)
                return True
            return False
        except Exception:
            return False

    def guardar_docente(self, datos):
        """Agrega o actualiza un docente"""
        ws = self._get_hoja('docentes')
        if ws is None:
            return False
        try:
            row = [datos.get(c, '') for c in COLUMNAS['docentes']]
            cell = ws.find(str(datos.get('dni', '')))
            if cell:
                ws.update(f'A{cell.row}:G{cell.row}', [row])
            else:
                ws.append_row(row)
            return True
        except Exception:
            return False

    def guardar_usuario(self, username, datos):
        """Guarda un usuario en la hoja"""
        ws = self._get_hoja('usuarios')
        if ws is None:
            return False
        try:
            row = [username, datos.get('password', ''),
                   datos.get('nombre', ''), datos.get('rol', 'docente'),
                   datos.get('grado', ''), datos.get('nivel', '')]
            cell = ws.find(str(username))
            if cell:
                ws.update(f'A{cell.row}:F{cell.row}', [row])
            else:
                ws.append_row(row)
            return True
        except Exception:
            return False

    def eliminar_usuario(self, username):
        """Elimina un usuario"""
        ws = self._get_hoja('usuarios')
        if ws is None:
            return False
        try:
            cell = ws.find(str(username))
            if cell:
                ws.delete_rows(cell.row)
                return True
            return False
        except Exception:
            return False

    def guardar_asistencia(self, datos):
        """Registra una asistencia"""
        ws = self._get_hoja('asistencias')
        if ws is None:
            return False
        try:
            # Buscar si ya existe entrada hoy para este DNI
            all_data = ws.get_all_records()
            fecha = datos.get('fecha', '')
            dni = datos.get('dni', '')

            for i, row in enumerate(all_data):
                if row.get('fecha') == fecha and str(row.get('dni')) == str(dni):
                    # Ya existe, actualizar hora_salida
                    row_num = i + 2  # +2 por encabezado y base-1
                    ws.update_cell(row_num, 6, datos.get('hora_salida', ''))
                    return 'salida'

            # No existe, crear nuevo
            row = [datos.get(c, '') for c in COLUMNAS['asistencias']]
            ws.append_row(row)
            return 'entrada'
        except Exception as e:
            st.error(f"Error registrando asistencia: {e}")
            return False

    def guardar_resultados_examen(self, eval_id, titulo, fecha, docente,
                                   grado, areas_info, resultados_lista):
        """Guarda todos los resultados de una evaluación"""
        ws = self._get_hoja('resultados')
        ws_hist = self._get_hoja('historial_eval')
        if ws is None:
            return False
        try:
            rows = []
            for res in resultados_lista:
                for nota_area in res.get('notas', []):
                    row = [
                        eval_id, titulo, fecha, docente,
                        res.get('nombre', ''), res.get('dni', ''),
                        grado,
                        nota_area.get('area', ''),
                        nota_area.get('total', 0),
                        nota_area.get('claves', ''),
                        nota_area.get('respuestas', ''),
                        nota_area.get('correctas', 0),
                        nota_area.get('total', 0),
                        nota_area.get('nota', 0),
                        res.get('promedio', 0),
                    ]
                    rows.append(row)

            if rows:
                ws.append_rows(rows)

            # Guardar en historial
            if ws_hist:
                promedio_general = 0
                if resultados_lista:
                    promedio_general = sum(
                        r.get('promedio', 0) for r in resultados_lista
                    ) / len(resultados_lista)
                hist_row = [
                    eval_id, fecha, docente, titulo, grado,
                    json.dumps(areas_info, ensure_ascii=False),
                    len(resultados_lista),
                    round(promedio_general, 2),
                ]
                ws_hist.append_row(hist_row)
            return True
        except Exception as e:
            st.error(f"Error guardando resultados: {e}")
            return False

    def guardar_incidencia(self, datos):
        """Registra una incidencia"""
        ws = self._get_hoja('incidencias')
        if ws is None:
            return False
        try:
            row = [datos.get(c, '') for c in COLUMNAS['incidencias']]
            ws.append_row(row)
            return True
        except Exception:
            return False

    def guardar_foto(self, dni, nombre, tipo, foto_bytes):
        """Guarda foto como base64 en Google Sheets"""
        ws = self._get_hoja('fotos')
        if ws is None:
            return False
        try:
            b64 = base64.b64encode(foto_bytes).decode('utf-8')
            # Verificar si ya existe
            cell = ws.find(str(dni))
            if cell:
                row_num = cell.row
                ws.update_cell(row_num, 4, b64)
                ws.update_cell(row_num, 5, datetime.now().strftime('%Y-%m-%d'))
            else:
                ws.append_row([
                    str(dni), nombre, tipo, b64,
                    datetime.now().strftime('%Y-%m-%d')
                ])
            return True
        except Exception as e:
            st.error(f"Error guardando foto: {e}")
            return False

    # ================================================================
    # SINCRONIZACIÓN MASIVA
    # ================================================================

    def sync_matricula_completa(self, df):
        """Reemplaza TODA la hoja de matrícula con el DataFrame"""
        ws = self._get_hoja('matricula')
        if ws is None:
            return False
        try:
            ws.clear()
            ws.append_row(COLUMNAS['matricula'])
            if len(df) > 0:
                rows = df[COLUMNAS['matricula']].fillna('').values.tolist()
                ws.append_rows(rows)
            return True
        except Exception:
            return False

    def sync_docentes_completo(self, df):
        """Reemplaza TODA la hoja de docentes"""
        ws = self._get_hoja('docentes')
        if ws is None:
            return False
        try:
            ws.clear()
            ws.append_row(COLUMNAS['docentes'])
            if len(df) > 0:
                cols = [c for c in COLUMNAS['docentes'] if c in df.columns]
                rows = df[cols].fillna('').values.tolist()
                ws.append_rows(rows)
            return True
        except Exception:
            return False

    def sync_usuarios_completo(self, usuarios_dict):
        """Reemplaza TODA la hoja de usuarios"""
        ws = self._get_hoja('usuarios')
        if ws is None:
            return False
        try:
            ws.clear()
            ws.append_row(COLUMNAS['usuarios'])
            for username, datos in usuarios_dict.items():
                di = datos.get('docente_info') or {}
                grado = di.get('grado', '') if isinstance(di, dict) else ''
                nivel = di.get('nivel', '') if isinstance(di, dict) else ''
                nombre = datos.get('label', datos.get('nombre', ''))
                password = str(datos.get('password', ''))
                row = [username, password, nombre,
                       datos.get('rol', 'docente'), grado, nivel]
                ws.append_row(row, value_input_option='RAW')
            return True
        except Exception:
            return False

    # ================================================================
    # REPORTES
    # ================================================================

    def reporte_asistencia_mensual(self, grado, mes, anio):
        """Genera datos para reporte mensual de asistencia"""
        asistencias = self.leer_asistencias(mes=mes, anio=anio, grado=grado)

        # Agrupar por estudiante
        estudiantes = {}
        for a in asistencias:
            dni = a.get('dni', '')
            nombre = a.get('nombre', '')
            fecha = a.get('fecha', '')
            if nombre not in estudiantes:
                estudiantes[nombre] = {'dni': dni, 'fechas': {}}
            estudiantes[nombre]['fechas'][fecha] = {
                'entrada': a.get('hora_entrada', ''),
                'salida': a.get('hora_salida', ''),
            }

        return estudiantes

    def historial_notas_estudiante(self, dni):
        """Obtiene todo el historial de notas de un estudiante"""
        resultados = self.leer_resultados(dni=dni)
        # Agrupar por evaluación
        evaluaciones = {}
        for r in resultados:
            eid = r.get('eval_id', '')
            if eid not in evaluaciones:
                evaluaciones[eid] = {
                    'titulo': r.get('eval_titulo', ''),
                    'fecha': r.get('fecha', ''),
                    'promedio': r.get('promedio', 0),
                    'areas': [],
                }
            evaluaciones[eid]['areas'].append({
                'area': r.get('area', ''),
                'nota': r.get('nota', 0),
                'correctas': r.get('correctas', 0),
                'total': r.get('total', 0),
                'respuestas': r.get('respuestas', ''),
                'claves': r.get('claves', ''),
            })
        return evaluaciones

    def generar_siguiente_codigo_incidencia(self):
        """Genera el siguiente código de incidencia: INC-2026-XXX"""
        incidencias = self.leer_incidencias()
        anio = datetime.now().year
        count = len([i for i in incidencias
                    if str(i.get('codigo', '')).startswith(f'INC-{anio}')])
        return f"INC-{anio}-{count + 1:03d}"

    def historial_asistencia_estudiante(self, dni):
        """Retorna historial de asistencia de un estudiante específico"""
        try:
            ws = self._get_hoja('asistencia')
            if not ws:
                return {}
            data = ws.get_all_records()
            historial = {}
            for row in data:
                if str(row.get('dni', '')) == str(dni):
                    fecha = str(row.get('fecha', ''))
                    if fecha not in historial:
                        historial[fecha] = {}
                    tipo = str(row.get('tipo', ''))
                    hora = str(row.get('hora', ''))
                    historial[fecha][tipo] = hora
            return historial
        except Exception:
            return {}


# ================================================================
# INICIALIZACIÓN GLOBAL
# ================================================================
@st.cache_resource
def get_google_sync():
    """Retorna instancia singleton de GoogleSync"""
    return GoogleSync()
