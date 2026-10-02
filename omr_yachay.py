# ================================================================
# OMR YACHAY — Lector óptico de la "Hoja de Respuestas Yachay"
# (Academia Preuniversitaria Yachay — Simulacro, 100 preguntas)
# ================================================================
# Lee: DNI (8 dígitos), Aula (1-9 + A-D), Día, Mes, Año, Grupo (A-D)
#      y las 100 respuestas (A-D) de la hoja oficial A4.
#
# Funciona con: foto de celular, escaneo JPG/PNG o PDF escaneado
# (una hoja por página). Usa los 4 cuadrados negros de las esquinas
# para enderezar la hoja.
#
# Coordenadas medidas sobre la hoja original a 300 dpi (2480 x 3508).
# Si algún día cambias el diseño de la hoja, solo hay que volver a
# medir las constantes de la sección "PLANTILLA".
# ================================================================

import io
import numpy as np

try:
    import cv2
    HAS_CV2 = True
except ImportError:  # pragma: no cover
    HAS_CV2 = False

# ----------------------------------------------------------------
# PLANTILLA (píxeles en la hoja enderezada de 2480 x 3508)
# ----------------------------------------------------------------
W, H = 2480, 3508
# Centros de los 4 cuadrados de las esquinas: TL, TR, BL, BR
MARCAS = [(85.5, 85.5), (2395.5, 85.5), (85.5, 3423.5), (2395.5, 3423.5)]

OPCIONES = ["A", "B", "C", "D"]

# Respuestas: 4 columnas × 25 filas
RESP_X = [[310.5, 410.5, 510.5, 610.5],
          [850.5, 950.5, 1050.5, 1150.5],
          [1390.5, 1490.5, 1590.5, 1690.5],
          [1930.5, 2030.5, 2130.5, 2230.5]]
RESP_Y0, RESP_DY, RESP_FILAS = 1215.5, 80.0, 25
RESP_R = 22            # radio de muestreo (burbuja ≈ 26 px)

# Cabecera (burbujas pequeñas ≈ 17 px de radio)
CAB_Y0, CAB_DY = 585.5, 52.0
CAB_R = 13
AULA_X = [1152.5, 1196.5, 1240.5, 1284.5]          # A B C D ; filas 1..9
DIA_X = [1360.5, 1420.5]                            # decenas(0-3), unidades(0-9)
MES_X = [1500.5, 1560.5]                            # decenas(0-1), unidades(0-9)
DNI_X = [1905.5 + 50 * k for k in range(8)]         # 8 dígitos, filas 0..9
ANIO_X, ANIO_Y = 1646.0, [640.0, 760.0, 880.0, 1000.0]
ANIOS = [2026, 2027, 2028, 2029]
ANIO_R = 17
GRUPO_X, GRUPO_Y, GRUPO_R = [520.0, 670.0, 820.0, 970.0], 1016.0, 26

# Umbrales de decisión (oscuridad 0..1 dentro de la burbuja)
UMBRAL_MARCA = 0.42       # por encima: cuenta como marcada
UMBRAL_DUDA = 0.30        # entre DUDA y MARCA: marca débil -> revisar
MARGEN_DOBLE = 0.18       # si la 2.ª opción está a menos de esto -> doble marca


def posicion_respuesta(i, j):
    """Centro (x, y) de la pregunta i (0..99), opción j (0..3)."""
    col, fila = divmod(i, RESP_FILAS)
    return RESP_X[col][j], RESP_Y0 + fila * RESP_DY


# ----------------------------------------------------------------
# CARGA DE IMÁGENES (foto, escaneo o PDF de varias páginas)
# ----------------------------------------------------------------
def imagenes_desde_archivo(nombre, datos):
    """Devuelve lista de imágenes BGR. Un PDF da una imagen por página."""
    if not HAS_CV2:
        return []
    nombre = (nombre or "").lower()
    if nombre.endswith(".pdf"):
        try:
            try:
                import pymupdf as fitz
            except ImportError:
                import fitz  # PyMuPDF antiguo
        except ImportError:
            raise RuntimeError("Para leer PDF instala 'pymupdf' (requirements.txt).")
        out = []
        doc = fitz.open(stream=datos, filetype="pdf")
        for page in doc:
            pix = page.get_pixmap(dpi=200)
            arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
            if pix.n == 4:
                arr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
            elif pix.n == 3:
                arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
            else:
                arr = cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
            out.append(arr)
        return out
    arr = cv2.imdecode(np.frombuffer(datos, np.uint8), cv2.IMREAD_COLOR)
    return [arr] if arr is not None else []


# ----------------------------------------------------------------
# ALINEACIÓN
# ----------------------------------------------------------------
def _candidatos_marca(gray):
    alto, ancho = gray.shape[:2]
    lado = min(alto, ancho)
    cands = []
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    umbrales = [cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1],
                cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY_INV, 51, 15)]
    for th in umbrales:
        cs, _ = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for c in cs:
            x, y, w, h = cv2.boundingRect(c)
            if not (lado * 0.018 <= w <= lado * 0.09 and lado * 0.018 <= h <= lado * 0.09):
                continue
            if not (0.7 <= w / float(h) <= 1.4):
                continue
            area = cv2.contourArea(c)
            if area < 0.80 * w * h:
                continue
            # debe ser oscuro por dentro
            roi = gray[y:y + h, x:x + w]
            if roi.size == 0 or roi.mean() > 110:
                continue
            m = cv2.moments(c)
            if m["m00"] == 0:
                continue
            cands.append((m["m10"] / m["m00"], m["m01"] / m["m00"], area))
    return cands


def _esquinas(gray):
    alto, ancho = gray.shape[:2]
    cands = _candidatos_marca(gray)
    if len(cands) < 4:
        return None
    esquinas_img = [(0, 0), (ancho, 0), (0, alto), (ancho, alto)]
    elegidos = []
    for ex, ey in esquinas_img:
        mejor = min(cands, key=lambda c: (c[0] - ex) ** 2 + (c[1] - ey) ** 2)
        # debe estar en el cuadrante correcto
        if abs(mejor[0] - ex) > ancho * 0.5 or abs(mejor[1] - ey) > alto * 0.5:
            return None
        elegidos.append((mejor[0], mejor[1]))
    if len(set(elegidos)) < 4:
        return None
    return elegidos


def _tiene_barra_tl(warped):
    """La hoja Yachay tiene una barrita negra debajo del cuadrado superior
    izquierdo. Sirve para saber si la hoja está de cabeza."""
    roi = warped[150:175, 45:125]
    return roi.size and roi.mean() < 110


def alinear(img_bgr):
    """Endereza la hoja. Devuelve (gray 2480x3508, ok:bool, mensaje)."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY) if img_bgr.ndim == 3 else img_bgr
    h0, w0 = gray.shape[:2]
    # trabajar a tamaño razonable
    escala = 1.0
    if max(h0, w0) > 3600:
        escala = 3600.0 / max(h0, w0)
        gray = cv2.resize(gray, (int(w0 * escala), int(h0 * escala)), interpolation=cv2.INTER_AREA)
    # hoja apaisada -> girarla
    if gray.shape[1] > gray.shape[0] * 1.15:
        gray = cv2.rotate(gray, cv2.ROTATE_90_CLOCKWISE)

    for intento in range(2):
        esq = _esquinas(gray)
        if esq is None:
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            esq = _esquinas(clahe.apply(gray))
        if esq is None:
            break
        M = cv2.getPerspectiveTransform(np.float32(esq), np.float32(MARCAS))
        warped = cv2.warpPerspective(gray, M, (W, H), borderValue=255)
        if _tiene_barra_tl(warped):
            return warped, True, "Hoja alineada con las 4 marcas"
        gray = cv2.rotate(gray, cv2.ROTATE_180)   # estaba de cabeza

    # Último recurso: asumir que la imagen ya es la hoja recortada
    warped = cv2.resize(gray, (W, H), interpolation=cv2.INTER_LINEAR)
    return warped, False, "No se encontraron las 4 marcas negras: revise la lectura"


# ----------------------------------------------------------------
# LECTURA DE BURBUJAS
# ----------------------------------------------------------------
def _preparar(warped):
    """Normaliza iluminación (sombras de foto) -> imagen 0..1 de 'tinta'."""
    fondo = cv2.morphologyEx(warped, cv2.MORPH_CLOSE,
                             cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61)))
    norm = cv2.divide(warped, fondo, scale=255)
    norm = cv2.GaussianBlur(norm, (3, 3), 0)
    return 1.0 - norm.astype(np.float32) / 255.0


def _oscuridad(tinta, cx, cy, r):
    r = int(r)
    cx, cy = int(round(cx)), int(round(cy))
    # pequeña búsqueda local (±6 px) para tolerar errores de alineación
    mejor = 0.0
    for dx in (-6, 0, 6):
        for dy in (-6, 0, 6):
            x, y = cx + dx, cy + dy
            roi = tinta[y - r:y + r + 1, x - r:x + r + 1]
            if roi.shape[0] != 2 * r + 1 or roi.shape[1] != 2 * r + 1:
                continue
            yy, xx = np.ogrid[-r:r + 1, -r:r + 1]
            mask = xx * xx + yy * yy <= r * r
            v = float(roi[mask].mean())
            mejor = max(mejor, v)
    return mejor


def _decidir(valores, etiquetas):
    """Devuelve (valor, estado) con estado en ok / blanco / doble / duda."""
    orden = sorted(range(len(valores)), key=lambda k: valores[k], reverse=True)
    v1 = valores[orden[0]]
    v2 = valores[orden[1]] if len(orden) > 1 else 0.0
    if v1 < UMBRAL_DUDA:
        return "", "blanco"
    if v1 < UMBRAL_MARCA:
        return etiquetas[orden[0]], "duda"
    if v2 >= UMBRAL_MARCA and v1 - v2 < MARGEN_DOBLE:
        return "*", "doble"
    return etiquetas[orden[0]], "ok"


def leer_hoja(img_bgr, num_preguntas=100):
    """Lee una hoja Yachay. Devuelve dict con todos los campos."""
    warped, alineada, msg = alinear(img_bgr)
    tinta = _preparar(warped)
    res = {"alineada": alineada, "mensaje": msg, "alertas": []}

    # ---- Respuestas ----
    resp, estados = [], []
    for i in range(num_preguntas):
        vals = [_oscuridad(tinta, *posicion_respuesta(i, j), RESP_R) for j in range(4)]
        v, e = _decidir(vals, OPCIONES)
        resp.append(v)
        estados.append(e)
    res["respuestas"] = resp
    res["estados"] = estados

    # ---- DNI ----
    dni, dni_ok = "", True
    for x in DNI_X:
        vals = [_oscuridad(tinta, x, CAB_Y0 + d * CAB_DY, CAB_R) for d in range(10)]
        v, e = _decidir(vals, [str(d) for d in range(10)])
        if e != "ok":
            dni_ok = False
            v = "?" if e != "blanco" else "_"
        dni += v
    res["dni"] = dni
    if not dni_ok:
        res["alertas"].append("DNI incompleto o con doble marca")

    # ---- Aula (fila 1..9, letra A..D) ----
    mejores = []
    for f in range(9):
        for j, x in enumerate(AULA_X):
            mejores.append((_oscuridad(tinta, x, CAB_Y0 + f * CAB_DY, CAB_R), f"{f + 1}{OPCIONES[j]}"))
    aula, e = _decidir([m[0] for m in mejores], [m[1] for m in mejores])
    res["aula"] = aula if e in ("ok", "duda") else ""

    # ---- Día y mes ----
    def _dos_digitos(xs, max_dec):
        vd = [_oscuridad(tinta, xs[0], CAB_Y0 + d * CAB_DY, CAB_R) for d in range(max_dec + 1)]
        vu = [_oscuridad(tinta, xs[1], CAB_Y0 + d * CAB_DY, CAB_R) for d in range(10)]
        d, ed = _decidir(vd, [str(k) for k in range(max_dec + 1)])
        u, eu = _decidir(vu, [str(k) for k in range(10)])
        if ed == "ok" and eu == "ok":
            return int(d + u)
        return None
    res["dia"] = _dos_digitos(DIA_X, 3)
    res["mes"] = _dos_digitos(MES_X, 1)

    # ---- Año ----
    va = [_oscuridad(tinta, ANIO_X, y, ANIO_R) for y in ANIO_Y]
    a, e = _decidir(va, [str(x) for x in ANIOS])
    res["anio"] = int(a) if e == "ok" else None

    # ---- Grupo ----
    vg = [_oscuridad(tinta, x, GRUPO_Y, GRUPO_R) for x in GRUPO_X]
    g, e = _decidir(vg, OPCIONES)
    res["grupo"] = g if e == "ok" else ""

    n_doble = estados.count("doble")
    n_duda = estados.count("duda")
    if n_doble:
        res["alertas"].append(f"{n_doble} pregunta(s) con doble marca")
    if n_duda:
        res["alertas"].append(f"{n_duda} pregunta(s) con marca débil (revisar)")
    if not alineada:
        res["alertas"].append(msg)
    res["_warped"] = warped
    return res


def imagen_revision(res, clave=None, ancho=900):
    """Imagen de la hoja enderezada con las lecturas pintadas encima.
    Verde = correcta, rojo = incorrecta, azul = leída (sin clave),
    naranja = revisar (duda/doble). Devuelve bytes PNG."""
    img = cv2.cvtColor(res["_warped"], cv2.COLOR_GRAY2BGR)
    n = len(res["respuestas"])
    for i in range(n):
        r = res["respuestas"][i]
        e = res["estados"][i]
        k = clave[i] if clave and i < len(clave) else None
        if e in ("duda", "doble"):
            for j in range(4):
                cv2.circle(img, tuple(int(v) for v in posicion_respuesta(i, j)), 30, (0, 140, 255), 4)
        if r in OPCIONES:
            col = (255, 120, 0)
            if k in OPCIONES:
                col = (0, 170, 0) if r == k else (0, 0, 230)
            cv2.circle(img, tuple(int(v) for v in posicion_respuesta(i, OPCIONES.index(r))), 30, col, 6)
        if k in OPCIONES and r != k:
            cx, cy = posicion_respuesta(i, OPCIONES.index(k))
            cv2.circle(img, (int(cx), int(cy)), 12, (0, 170, 0), -1)
    esc = ancho / float(W)
    img = cv2.resize(img, (ancho, int(H * esc)), interpolation=cv2.INTER_AREA)
    ok, buf = cv2.imencode(".png", img)
    return buf.tobytes() if ok else None
