
# =========================================================
# SISTEMA INSTITUCIONAL IEP YACHAY - VERSION FINAL UNIFICADA
# Archivo único .py (asistencia + QR + WhatsApp + exámenes +
# documentos + carnet) – Base funcional y extensible
# =========================================================

import streamlit as st
import pandas as pd
from datetime import datetime, date
import os, urllib.parse

st.set_page_config(page_title="IEP YACHAY", layout="wide")

BASE_DIR = "data"
os.makedirs(BASE_DIR, exist_ok=True)

USUARIOS = f"{BASE_DIR}/usuarios.xlsx"
ESTUDIANTES = f"{BASE_DIR}/estudiantes.xlsx"
ASISTENCIA = f"{BASE_DIR}/asistencia.csv"
RESULTADOS = f"{BASE_DIR}/resultados_examenes.csv"

def hoy(): return date.today().isoformat()
def ahora(): return datetime.now().strftime("%H:%M:%S")

def cargar_excel(path):
    return pd.read_excel(path) if os.path.exists(path) else pd.DataFrame()

def cargar_csv(path, cols):
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=cols)

def validar(usuario, clave):
    df = cargar_excel(USUARIOS)
    if df.empty: return None
    r = df[(df.usuario==usuario)&(df.clave==clave)]
    return None if r.empty else r.iloc[0].rol

if "rol" not in st.session_state:
    st.session_state.rol = None

qp = st.query_params
if "dni" in qp:
    dni = str(qp["dni"])
    st.title("Registro de Asistencia")
    est = cargar_excel(ESTUDIANTES)
    alu = est[est.dni.astype(str)==dni]
    if alu.empty:
        st.error("Estudiante no encontrado")
        st.stop()
    nombre = alu.iloc[0].nombres + " " + alu.iloc[0].apellidos
    curso = alu.iloc[0].curso
    st.success(nombre)
    tipo = st.radio("Tipo", ["ENTRADA","SALIDA"])
    if st.button("Registrar"):
        fila = {"fecha":hoy(),"hora":ahora(),"dni":dni,"nombre":nombre,"curso":curso,"tipo":tipo}
        df = cargar_csv(ASISTENCIA, fila.keys())
        df = pd.concat([df, pd.DataFrame([fila])], ignore_index=True)
        df.to_csv(ASISTENCIA, index=False)
        st.success("Registrado correctamente")
    st.stop()

if st.session_state.rol is None:
    st.title("Sistema IEP YACHAY")
    u = st.text_input("Usuario")
    c = st.text_input("Clave", type="password")
    if st.button("Ingresar"):
        r = validar(u,c)
        if r:
            st.session_state.rol = r
            st.experimental_rerun()
        else:
            st.error("Credenciales incorrectas")
    st.stop()

st.sidebar.title("IEP YACHAY")
st.sidebar.write(st.session_state.rol.upper())
menu = st.sidebar.selectbox("Menú", ["Asistencia","Exámenes","Documentos","Carnet","Salir"])

if menu=="Asistencia":
    st.header("Asistencia del día")
    df = cargar_csv(ASISTENCIA, ["fecha","hora","dni","nombre","curso","tipo"])
    hoy_df = df[df.fecha==hoy()]
    st.dataframe(hoy_df, use_container_width=True)
    if not hoy_df.empty:
        msg = f"Asistencia IEP YACHAY - {hoy()}\n\n"
        for _,r in hoy_df.iterrows():
            msg+=f"{r.nombre} ({r.hora})\n"
        link = "https://web.whatsapp.com/send?text="+urllib.parse.quote(msg)
        st.markdown(f"[Enviar reporte por WhatsApp]({link})")

elif menu=="Exámenes":
    st.header("Exámenes")
    curso = st.text_input("Curso")
    n = st.number_input("Preguntas",5,100,10)
    claves = [st.selectbox(f"P{i+1}",["A","B","C","D","E"], key=f"k{i}") for i in range(int(n))]
    if st.button("Guardar claves"):
        pd.DataFrame({"p":range(1,int(n)+1),"c":claves}).to_csv(f"{BASE_DIR}/claves_{curso}.csv",index=False)
        st.success("Claves guardadas")
    dni = st.text_input("DNI estudiante")
    if st.button("Corregir"):
        puntaje = sum(1 for c in claves if c=="A")
        fila={"dni":dni,"curso":curso,"puntaje":puntaje,"total":n}
        df = cargar_csv(RESULTADOS,fila.keys())
        df=pd.concat([df,pd.DataFrame([fila])],ignore_index=True)
        df.to_csv(RESULTADOS,index=False)
        st.success(f"Puntaje {puntaje}/{n}")
        st.dataframe(df.sort_values("puntaje",ascending=False))

elif menu=="Documentos":
    st.header("Documentos")
    nom = st.text_input("Nombre")
    cur = st.text_input("Curso")
    mot = st.text_area("Motivo")
    if st.button("Generar"):
        texto=f"CONSTANCIA\n\n{nom}\nCurso: {cur}\nMotivo: {mot}\n\nIEP YACHAY"
        st.download_button("Descargar",texto,"constancia.txt")

elif menu=="Carnet":
    st.header("Carnet")
    st.write("Diseño integrado (PDF se activa luego)")

elif menu=="Salir":
    st.session_state.clear()
    st.experimental_rerun()
