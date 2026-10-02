# Lanzador de escritorio del Sistema Yachay (para el .exe o para `python yachay_launcher.py`)
# Abre el sistema en el navegador de la computadora, sin internet, con los
# datos guardados en la misma carpeta donde está el programa.
import os
import sys
import webbrowser
import threading


def _abrir_navegador():
    import time
    time.sleep(3)
    webbrowser.open("http://localhost:8501")


if __name__ == "__main__":
    congelado = getattr(sys, "frozen", False)
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    # Carpeta de datos = donde está el .exe (así los JSON/Excel no se pierden)
    datos = os.path.dirname(sys.executable) if congelado else base
    os.chdir(datos)
    # Copiar archivos base (hoja PDF, logos, excel) si no existen junto al .exe
    for f in ("Hoja_Yachay_en_blanco.pdf", "logo_academia.png", "logo_academia_marca_agua.png",
              "fondo.png", "base_datos.xlsx", "himno_colegio.mp3", "himno_nacional_peru.mp3"):
        src, dst = os.path.join(base, f), os.path.join(datos, f)
        if os.path.exists(src) and not os.path.exists(dst):
            import shutil
            shutil.copy(src, dst)
    sys.path.insert(0, base)
    if os.environ.get("YACHAY_SELFTEST"):
        # Autoprueba: ejecuta el sistema sin navegador y reporta errores de importación
        from streamlit.testing.v1 import AppTest
        at = AppTest.from_file(os.path.join(base, "sistema_web.py"), default_timeout=300)
        at.run()
        errores = [str(e.value) for e in at.exception]
        print("SELFTEST exceptions:", errores)
        sys.exit(1 if errores else 0)
    from streamlit.web import cli as stcli
    threading.Thread(target=_abrir_navegador, daemon=True).start()
    sys.argv = ["streamlit", "run", os.path.join(base, "sistema_web.py"),
                "--global.developmentMode=false", "--server.port=8501",
                "--server.headless=true", "--browser.gatherUsageStats=false"]
    sys.exit(stcli.main())
