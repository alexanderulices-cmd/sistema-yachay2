# -*- mode: python -*-
# Receta de PyInstaller para crear SistemaYachay.exe
import glob
from PyInstaller.utils.hooks import collect_all, collect_submodules

datas, binaries, hiddenimports = [], [], []
for paq in ("streamlit", "pymupdf", "pyzbar", "reportlab", "docx", "gspread", "google.auth",
            "googleapiclient", "gtts", "edge_tts", "qrcode", "barcode", "altair", "pyarrow"):
    try:
        d, b, h = collect_all(paq)
        datas += d; binaries += b; hiddenimports += h
    except Exception:
        pass
hiddenimports += collect_submodules("streamlit") + ["cv2", "numpy", "pandas", "openpyxl", "PIL"]

# Todos los módulos y recursos del sistema van dentro del .exe
for f in glob.glob("*.py"):
    datas.append((f, "."))
for f in ("*.png", "*.pdf", "*.xlsx", "*.mp3"):
    for x in glob.glob(f):
        datas.append((x, "."))

a = Analysis(["yachay_launcher.py"], pathex=["."], binaries=binaries, datas=datas,
             hiddenimports=hiddenimports, noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="SistemaYachay",
          console=True, icon=None)
coll = COLLECT(exe, a.binaries, a.datas, name="SistemaYachay")
