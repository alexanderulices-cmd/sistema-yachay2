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

# Marcas de ajuste (cuadraditos negros de 32 px) — como en ZipGrade / hojas OMR profesionales.
# Van en los márgenes (una por fila de DNI y de respuestas, a cada lado), arriba y en la
# franja entre la cabecera y las respuestas. Sirven para corregir la distorsión de lente
# y la curvatura del papel; el lector las usa si están y las ignora si no (hojas antiguas).
NOMBRE_ZONA = (190, 470, 1258, 762)      # x0, y0, x1, y1: recuadros de apellidos y nombres
AJ_TAM = 32
AJ_IZQ_X, AJ_DER_X = 85.5, 2395.5
AJ_TOP_Y, AJ_BANDA_Y = 72.0, 1133.0
AJ_X = [280.0 + 192.0 * k for k in range(11)]        # 280 ... 2200


def marcas_ajuste():
    """[(cx, cy, grupo)] de todas las marcas de ajuste de la hoja."""
    pts = []
    for r in range(10):                                  # filas de la cabecera (DNI)
        y = CAB_Y0 + CAB_DY * r
        pts += [(AJ_IZQ_X, y, "cab"), (AJ_DER_X, y, "cab")]
    for f in range(RESP_FILAS):                          # filas de respuestas
        y = RESP_Y0 + RESP_DY * f
        pts += [(AJ_IZQ_X, y, "res"), (AJ_DER_X, y, "res")]
    pts += [(x, AJ_TOP_Y, "top") for x in AJ_X]
    pts += [(x, AJ_BANDA_Y, "banda") for x in AJ_X]
    return pts


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


def contar_paginas(nombre, datos):
    """Cuántas hojas trae un archivo (un PDF trae una por página)."""
    if (nombre or "").lower().endswith(".pdf"):
        try:
            try:
                import pymupdf as fitz
            except ImportError:
                import fitz
            return len(fitz.open(stream=datos, filetype="pdf"))
        except Exception:
            return 1
    return 1


def iterar_imagenes(nombre, datos):
    """Igual que imagenes_desde_archivo, pero entrega UNA página a la vez.
    Así un PDF de cientos de hojas no llena la memoria del servidor."""
    if not HAS_CV2:
        return
    if (nombre or "").lower().endswith(".pdf"):
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz
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
            del pix
            try:
                fitz.TOOLS.store_shrink(100)      # libera la memoria de la página ya leída
            except Exception:
                pass
            yield arr
        return
    arr = cv2.imdecode(np.frombuffer(datos, np.uint8), cv2.IMREAD_COLOR)
    if arr is not None:
        yield arr


# ----------------------------------------------------------------
# ALINEACIÓN
# ----------------------------------------------------------------
def _candidatos_marca(gray):
    alto, ancho = gray.shape[:2]
    lado = min(alto, ancho)
    cands = []
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    papel = float(np.percentile(blur, 92))                 # nivel del papel blanco en esta foto
    umbrales = [cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1],
                cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY_INV, 51, 15)]
    for frac in (0.30, 0.42):                              # solo lo casi negro respecto al papel
        umbrales.append(((blur < papel * frac).astype(np.uint8)) * 255)
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
    """Elige los 4 cuadrados grandes de las esquinas. No basta con tomar el candidato más
    cercano a cada esquina de la foto: si uno de los 4 no se detecta se colaría otro objeto.
    Se exige que los 4 tengan tamaño parecido y formen un cuadrilátero razonable."""
    alto, ancho = gray.shape[:2]
    cands = _candidatos_marca(gray)
    if len(cands) < 4:
        return None
    # quitar duplicados (mismo cuadrado hallado con varios umbrales)
    unicos = []
    for c in sorted(cands, key=lambda q: -q[2]):
        if all((c[0] - u[0]) ** 2 + (c[1] - u[1]) ** 2 > 25 ** 2 for u in unicos):
            unicos.append(c)
    if len(unicos) < 4:
        return None
    # las esquinas son los cuadrados más grandes y de tamaño parecido
    areas = sorted(c[2] for c in unicos)
    ref = areas[-4] if len(areas) >= 4 else areas[0]
    grandes = [c for c in unicos if c[2] >= 0.55 * ref] or unicos
    esquinas_img = [(0, 0), (ancho, 0), (0, alto), (ancho, alto)]
    mejor_conj, mejor_costo = None, 1e18
    import itertools
    pool = sorted(grandes, key=lambda q: -q[2])[:10]
    if len(pool) < 4:
        return None
    for conj in itertools.combinations(pool, 4):
        # asignar cada uno a su esquina de la foto (TL, TR, BL, BR) por posición
        pts = sorted(conj, key=lambda q: q[1])
        sup = sorted(pts[:2], key=lambda q: q[0])
        inf = sorted(pts[2:], key=lambda q: q[0])
        tl, tr, bl, br = sup[0], sup[1], inf[0], inf[1]
        ar = [tl[2], tr[2], bl[2], br[2]]
        if max(ar) > 2.6 * min(ar):
            continue
        # el cuadrilátero debe ser convexo y con proporciones de hoja A4 (con margen por perspectiva)
        P = np.float32([[tl[0], tl[1]], [tr[0], tr[1]], [br[0], br[1]], [bl[0], bl[1]]])
        if cv2.contourArea(P) < 0.12 * alto * ancho:
            continue
        top = np.hypot(tr[0] - tl[0], tr[1] - tl[1]); bot = np.hypot(br[0] - bl[0], br[1] - bl[1])
        izq = np.hypot(bl[0] - tl[0], bl[1] - tl[1]); der = np.hypot(br[0] - tr[0], br[1] - tr[1])
        lado_h, lado_v = 0.5 * (top + bot), 0.5 * (izq + der)
        prop = max(lado_h, lado_v) / max(min(lado_h, lado_v), 1)
        if not (1.15 <= prop <= 1.75):
            continue
        if not cv2.isContourConvex(P.astype(np.int32)):
            continue
        # preferir los más grandes y los más cercanos a las esquinas de la foto
        costo = -sum(ar) + 0.02 * sum((c[0] - ex) ** 2 + (c[1] - ey) ** 2 for c, (ex, ey) in zip((tl, tr, bl, br), esquinas_img)) ** 0.5
        if costo < mejor_costo:
            mejor_costo, mejor_conj = costo, (tl, tr, bl, br)
    if mejor_conj is None:
        return None
    return [(c[0], c[1]) for c in mejor_conj]


def _esquinas_ok(warped):
    """Comprueba que en la hoja ya enderezada los 4 cuadrados grandes están donde deben."""
    buenos = 0
    for (ex, ey) in MARCAS:
        x0, y0 = int(ex - 30), int(ey - 30)
        n = warped[max(y0, 0):y0 + 60, max(x0, 0):x0 + 60]
        if n.size and float((n < 100).mean()) > 0.75:
            buenos += 1
    return buenos >= 4


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
        if _tiene_barra_tl(warped) and _esquinas_ok(warped):
            try:
                warped, info = _afinar(warped)
            except Exception as e:                     # el afinado nunca debe impedir la lectura
                info = f"sin afinado ({e})"
            return warped, True, "Hoja alineada con las 4 marcas · " + info
        gray = cv2.rotate(gray, cv2.ROTATE_180)   # estaba de cabeza

    # Último recurso: asumir que la imagen ya es la hoja recortada
    warped = cv2.resize(gray, (W, H), interpolation=cv2.INTER_LINEAR)
    return warped, False, "No se encontraron las 4 marcas negras: revise la lectura"


# ----------------------------------------------------------------
# AFINADO CON LAS MARCAS DE AJUSTE
# ----------------------------------------------------------------
def _buscar_marca(g, cx, cy, mx, my):
    """Busca un cuadradito negro cerca de (cx, cy) en la hoja enderezada.
    Devuelve el centro (x, y) con precisión de subpíxel, o None."""
    x0, x1 = int(round(cx - mx)), int(round(cx + mx)) + 1
    y0, y1 = int(round(cy - my)), int(round(cy + my)) + 1
    if x0 < 0 or y0 < 0 or x1 > g.shape[1] or y1 > g.shape[0]:
        return None
    sub = g[y0:y1, x0:x1]
    if int(sub.max()) - int(sub.min()) < 70:
        return None
    _, th = cv2.threshold(sub, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    n, _, st, cen = cv2.connectedComponentsWithStats(th, connectivity=8)
    mejor, dmin = None, 1e18
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if not (AJ_TAM * 0.6 <= w <= AJ_TAM * 1.6 and AJ_TAM * 0.6 <= h <= AJ_TAM * 1.6):
            continue
        if a < 0.7 * w * h:
            continue
        d = (cen[i][0] - (cx - x0)) ** 2 + (cen[i][1] - (cy - y0)) ** 2
        if d < dmin:
            dmin, mejor = d, (x, y, w, h)
    if mejor is None:
        return None
    x, y, w, h = mejor                                     # centroide ponderado por oscuridad
    pad = 3
    ya, yb = max(y - pad, 0), min(y + h + pad, sub.shape[0])
    xa, xb = max(x - pad, 0), min(x + w + pad, sub.shape[1])
    peso = 255.0 - sub[ya:yb, xa:xb].astype(np.float32)
    peso = np.clip(peso - float(peso.min()), 0, None)
    tot = float(peso.sum())
    if tot <= 0:
        return None
    yy, xx = np.mgrid[ya:yb, xa:xb]
    return (x0 + float((peso * xx).sum()) / tot + 0.5 - 0.5, y0 + float((peso * yy).sum()) / tot)


AJ_GRADO = 3


def _terminos(u, v):
    """Base del ajuste: afín + cuadrática + distorsión radial (u·r², v·r²). Es lo bastante
    flexible para la distorsión de lente (con el centro desplazado) y lo bastante rígida para
    no inventar formas en el interior de la hoja."""
    r2 = u * u + v * v
    base = [np.ones_like(u), u, v, u * u, u * v, v * v]
    if AJ_GRADO >= 3:
        base += [u * r2, v * r2]
    return np.stack(base, axis=1)


def _ajustar_desplazamiento(exp, obs):
    """Ajusta un polinomio de 3.er grado al desplazamiento (obs - exp) con rechazo de
    valores atípicos. Devuelve (coef_x, coef_y, usados, error_rms) o None."""
    u = (exp[:, 0] - W / 2.0) / (H / 2.0)
    v = (exp[:, 1] - H / 2.0) / (H / 2.0)
    A = _terminos(u, v)
    d = obs - exp
    ok = np.ones(len(exp), bool)
    for _ in range(4):
        if ok.sum() < 20:
            return None
        cx = np.linalg.lstsq(A[ok].T @ A[ok] + 1e-3 * np.eye(A.shape[1]), A[ok].T @ d[ok, 0], rcond=None)[0]
        cy = np.linalg.lstsq(A[ok].T @ A[ok] + 1e-3 * np.eye(A.shape[1]), A[ok].T @ d[ok, 1], rcond=None)[0]
        res = np.hypot(A @ cx - d[:, 0], A @ cy - d[:, 1])
        lim = max(3.0, 3.0 * float(np.median(res[ok])) * 1.4826)
        nuevo = res <= lim
        if (nuevo == ok).all():
            break
        ok = nuevo
    if ok.sum() < 20:
        return None
    rms = float(np.sqrt(np.mean(res[ok] ** 2)))
    return cx, cy, int(ok.sum()), rms


def _afinar(warped):
    """Corrige la distorsión residual (lente, curvatura) con las marcas de ajuste.
    Devuelve (imagen, texto_info). Si la hoja no las tiene (diseño antiguo) o algo no cuadra,
    devuelve la imagen tal cual."""
    marcas = marcas_ajuste()
    exp, obs = [], []
    # 1.ª pasada: marcas bien separadas entre sí (ventanas amplias)
    for cx, cy, grp in marcas:
        if grp == "cab":
            continue
        mx, my = (60, 45) if grp in ("res",) else (60, 50)
        if grp in ("top", "banda"):
            mx, my = 60, 40
        p = _buscar_marca(warped, cx, cy, mx, my)
        if p is not None:
            exp.append((cx, cy))
            obs.append(p)
    if len(exp) < 24:
        return warped, f"sin afinado ({len(exp)} marcas)"
    exp, obs = np.float64(exp), np.float64(obs)
    aj = _ajustar_desplazamiento(exp, obs)
    if aj is None:
        return warped, "sin afinado (ajuste inestable)"
    cx_, cy_ = aj[0], aj[1]

    def _pred(x, y):
        u, v = (x - W / 2.0) / (H / 2.0), (y - H / 2.0) / (H / 2.0)
        t = _terminos(np.float64([u]), np.float64([v]))[0]
        return x + float(t @ cx_), y + float(t @ cy_)
    # 2.ª pasada: filas de la cabecera (marcas pegadas), buscadas donde las predice el ajuste
    for cx, cy, grp in marcas:
        if grp != "cab":
            continue
        px, py = _pred(cx, cy)
        p = _buscar_marca(warped, px, py, 28, 22)
        if p is not None:
            exp = np.vstack([exp, (cx, cy)])
            obs = np.vstack([obs, p])
    aj = _ajustar_desplazamiento(exp, obs)
    if aj is None:
        return warped, "sin afinado (ajuste inestable)"
    cx_, cy_, usados, rms = aj
    paso = 8
    us = (np.arange(0, W + paso, paso, dtype=np.float64) - W / 2.0) / (H / 2.0)
    vs = (np.arange(0, H + paso, paso, dtype=np.float64) - H / 2.0) / (H / 2.0)
    uu, vv = np.meshgrid(us, vs)
    T = _terminos(uu.ravel(), vv.ravel())
    dx = (T @ cx_).reshape(uu.shape).astype(np.float32)
    dy = (T @ cy_).reshape(uu.shape).astype(np.float32)
    mag = float(np.hypot(dx, dy).max())
    if rms > 4.0 or mag > 70.0:
        return warped, f"sin afinado: hoja muy deformada o curvada (error {rms:.1f} px, desvío {mag:.0f} px)"
    dx = cv2.resize(dx, (W + paso, H + paso), interpolation=cv2.INTER_LINEAR)[:H, :W]
    dy = cv2.resize(dy, (W + paso, H + paso), interpolation=cv2.INTER_LINEAR)[:H, :W]
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    fino = cv2.remap(warped, gx + dx, gy + dy, cv2.INTER_LINEAR, borderValue=255)
    return fino, f"afinada con {usados} marcas de ajuste (desvío máx. {mag:.0f} px, error {rms:.1f} px)"


# ----------------------------------------------------------------
# CÓDIGO QR DE LA HOJA (identifica el simulacro)
# ----------------------------------------------------------------
# Zona del QR en la hoja enderezada (esquina derecha del encabezado).
QR_ZONA = (1960, 80, 2440, 430)        # x0, y0, x1, y1
QR_PREFIJO = "YCH1|"


def leer_qr(img_bgr=None, warped=None, alineada=True):
    """Lee el QR impreso en la hoja. Devuelve el texto o '' si no hay/no se lee.
    Prueba primero la zona esperada de la hoja enderezada (rápido y fiable) y
    luego, como respaldo, la hoja completa y la foto original."""
    if not HAS_CV2:
        return ""
    det = cv2.QRCodeDetector()

    def _probar(g):
        if g is None or g.size == 0:
            return ""
        variantes = [g]
        try:
            variantes.append(cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1])
            variantes.append(cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                   cv2.THRESH_BINARY, 41, 8))
        except cv2.error:
            pass
        for v in variantes:
            try:
                txt, _, _ = det.detectAndDecode(v)
            except cv2.error:
                txt = ""
            if txt:
                return txt
        return ""

    if warped is not None:
        g = warped if warped.ndim == 2 else cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        x0, y0, x1, y1 = QR_ZONA
        zona = g[y0:y1, x0:x1]
        if alineada:
            # Un QR impreso deja ~20 % de la zona en negro; la hoja genérica, menos del 5 %.
            z2 = g[120:380, 2060:2320]
            if float((z2 < 80).mean()) < 0.10:
                return ""
        for f in (1.0, 0.6, 1.5):
            z = zona if f == 1.0 else cv2.resize(zona, None, fx=f, fy=f, interpolation=cv2.INTER_AREA
                                                 if f < 1 else cv2.INTER_CUBIC)
            z = cv2.copyMakeBorder(z, 40, 40, 40, 40, cv2.BORDER_REPLICATE)
            t = _probar(z)
            if t:
                return t
        t = _probar(cv2.resize(g, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA))
        if t:
            return t
    if img_bgr is not None:
        g = img_bgr if img_bgr.ndim == 2 else cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        t = _probar(g)
        if t:
            return t
    return ""


# ----------------------------------------------------------------
# LECTURA DE BURBUJAS
# ----------------------------------------------------------------
def _preparar(warped):
    """Normaliza iluminación (sombras de foto) -> imagen 0..1 de 'tinta'."""
    h, w = warped.shape[:2]
    peq = cv2.resize(warped, (w // 4, h // 4), interpolation=cv2.INTER_AREA)
    fondo_p = cv2.morphologyEx(peq, cv2.MORPH_CLOSE,
                               cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))
    fondo = np.maximum(cv2.resize(fondo_p, (w, h), interpolation=cv2.INTER_LINEAR), warped)
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
    """Decisión con umbrales fijos (se conserva por compatibilidad)."""
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


class _Calib:
    """Calibración de UNA hoja: nivel del papel sin marcas (base), ruido y fuerza típica de una
    marca firme. Así una marca clara de lápiz o de lapicero se acepta igual que una oscura, y
    una foto con sombras no confunde burbujas vacías con marcadas."""

    def __init__(self, *matrices):
        resto, s1 = [], []
        for m in matrices:
            for fila in m:
                ord_ = sorted(fila)
                resto += ord_[:-1]
        arr = np.array(resto, dtype=np.float64) if resto else np.array([0.15])
        self.base = float(np.median(arr))
        mad = float(np.median(np.abs(arr - self.base))) * 1.4826
        self.sigma = max(mad, 0.012)
        for m in matrices:
            s1 += [max(f) - self.base for f in m]
        firmes = [s for s in s1 if s >= 0.20]
        self.fuerza = float(np.median(firmes)) if len(firmes) >= 3 else 0.42
        self.t_blanco = max(0.04, 3.5 * self.sigma)
        self.t_ok = min(0.30, max(0.15, 0.42 * self.fuerza))

    def decidir(self, valores, etiquetas):
        """(valor, estado) con estado en ok / blanco / doble / duda."""
        orden = sorted(range(len(valores)), key=lambda k: valores[k], reverse=True)
        s1 = valores[orden[0]] - self.base
        s2 = (valores[orden[1]] - self.base) if len(orden) > 1 else 0.0
        if s1 < self.t_blanco:
            return "", "blanco"
        if s2 >= max(0.15, 0.5 * s1):
            return "*", "doble"
        if s1 >= self.t_ok:
            return etiquetas[orden[0]], "ok"
        return etiquetas[orden[0]], "duda"


def leer_hoja(img_bgr, num_preguntas=100):
    """Lee una hoja Yachay. Devuelve dict con todos los campos."""
    warped, alineada, msg = alinear(img_bgr)
    tinta = _preparar(warped)
    res = {"alineada": alineada, "mensaje": msg, "alertas": []}

    # ---- valores de oscuridad de todas las burbujas ----
    v_resp = [[_oscuridad(tinta, *posicion_respuesta(i, j), RESP_R) for j in range(4)] for i in range(num_preguntas)]
    v_dni = [[_oscuridad(tinta, x, CAB_Y0 + d * CAB_DY, CAB_R) for d in range(10)] for x in DNI_X]
    v_dia = [[_oscuridad(tinta, DIA_X[0], CAB_Y0 + d * CAB_DY, CAB_R) for d in range(4)],
             [_oscuridad(tinta, DIA_X[1], CAB_Y0 + d * CAB_DY, CAB_R) for d in range(10)]]
    v_mes = [[_oscuridad(tinta, MES_X[0], CAB_Y0 + d * CAB_DY, CAB_R) for d in range(2)],
             [_oscuridad(tinta, MES_X[1], CAB_Y0 + d * CAB_DY, CAB_R) for d in range(10)]]
    v_anio = [_oscuridad(tinta, ANIO_X, y, ANIO_R) for y in ANIO_Y]
    v_grupo = [_oscuridad(tinta, x, GRUPO_Y, GRUPO_R) for x in GRUPO_X]
    cal_r = _Calib(v_resp)                                   # respuestas
    cal_c = _Calib(v_dni, v_dia, v_mes)                      # casilleros de la cabecera
    res["calibracion"] = {"base": round(cal_r.base, 3), "ruido": round(cal_r.sigma, 3),
                          "fuerza": round(cal_r.fuerza, 3)}

    # ---- Respuestas ----
    resp, estados = [], []
    for vals in v_resp:
        v, e = cal_r.decidir(vals, OPCIONES)
        resp.append(v)
        estados.append(e)
    res["respuestas"] = resp
    res["estados"] = estados

    # ---- DNI ----
    dni, dni_ok, dni_det = "", True, []
    for k, vals in enumerate(v_dni):
        v, e = cal_c.decidir(vals, [str(d) for d in range(10)])
        dni_det.append((v, e, int(np.argmax(vals))))
        if e != "ok":
            dni_ok = False
            v = "?" if e != "blanco" else "_"
        dni += v
    res["dni"] = dni
    res["dni_det"] = dni_det
    if not dni_ok:
        res["alertas"].append("DNI incompleto o con doble marca")

    # ---- Aula: ya no existe en la hoja (el grado/aula sale de la matrícula con el DNI) ----
    res["aula"] = ""

    # ---- Día y mes ----
    def _dos_digitos(vv, max_dec):
        d, ed = cal_c.decidir(vv[0], [str(k) for k in range(max_dec + 1)])
        u, eu = cal_c.decidir(vv[1], [str(k) for k in range(10)])
        if ed == "ok" and eu == "ok":
            return int(d + u), (int(d), int(u))
        return None, None
    res["dia"], res["dia_idx"] = _dos_digitos(v_dia, 3)
    res["mes"], res["mes_idx"] = _dos_digitos(v_mes, 1)

    # ---- Año ----
    a, e = cal_c.decidir(v_anio, [str(x) for x in ANIOS])
    res["anio"] = int(a) if e == "ok" else None

    # ---- Grupo ----
    g, e = cal_c.decidir(v_grupo, OPCIONES)
    res["grupo"] = g if e == "ok" else ""
    res["grupo_estado"] = e

    n_doble = estados.count("doble")
    n_duda = estados.count("duda")
    if n_doble:
        res["alertas"].append(f"{n_doble} pregunta(s) con doble marca")
    if n_duda:
        res["alertas"].append(f"{n_duda} pregunta(s) con marca débil (revisar)")
    if not alineada:
        res["alertas"].append(msg)
    res["qr"] = leer_qr(img_bgr, warped, alineada)
    if "curvada" in str(msg):
        res["alertas"].append("La hoja está curvada o arrugada: revise bien las lecturas")
    res["_warped"] = warped
    return res


_FUENTES = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/arial.ttf", "/Library/Fonts/Arial Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]


def _fuente(px):
    from PIL import ImageFont
    for ruta in _FUENTES:
        try:
            return ImageFont.truetype(ruta, px)
        except Exception:
            continue
    return None


def _texto(img, t, x, y, esc, color=(30, 30, 30), grosor=2):
    """Escribe texto sobre la imagen (con tildes y Ñ si hay una fuente disponible)."""
    t = str(t)
    f = _fuente(int(esc * 34))
    if f is not None:
        from PIL import Image, ImageDraw
        pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ImageDraw.Draw(pil).text((int(x), int(y) - int(esc * 30)), t, font=f, fill=(color[2], color[1], color[0]))
        img[:] = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
        return
    import unicodedata
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    cv2.putText(img, t, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, esc, color, grosor, cv2.LINE_AA)


def imagen_revision(res, clave=None, ancho=900, nombre=None):
    """Imagen de la hoja enderezada con las lecturas pintadas encima.
    Verde = correcta, rojo = incorrecta, azul = leída (sin clave), naranja = revisar.
    En la cabecera, puntitos verdes sobre el DNI, el día, el mes, el año y el área leídos,
    y una franja arriba con el DNI y los datos leídos. Devuelve bytes JPEG."""
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

    # ---- cabecera: lo que se leyó (puntitos verdes) ----
    VERDE, NARANJA = (0, 190, 0), (0, 140, 255)
    for k, x in enumerate(DNI_X):
        det = res.get("dni_det", [])
        if k < len(det):
            v, e, idx = det[k]
            cy = CAB_Y0 + idx * CAB_DY
            if e == "ok":
                cv2.circle(img, (int(x), int(cy)), 11, VERDE, -1)
            elif e in ("duda", "doble"):
                cv2.circle(img, (int(x), int(cy)), 25, NARANJA, 5)
            else:
                cv2.circle(img, (int(x), int(CAB_Y0 - 38)), 10, (0, 0, 230), -1)      # columna sin marca
    for xs, idx in ((DIA_X, res.get("dia_idx")), (MES_X, res.get("mes_idx"))):
        if idx:
            for x, d in zip(xs, idx):
                cv2.circle(img, (int(x), int(CAB_Y0 + d * CAB_DY)), 11, VERDE, -1)
    if res.get("anio") in ANIOS:
        cv2.circle(img, (int(ANIO_X), int(ANIO_Y[ANIOS.index(res["anio"])])), 14, VERDE, -1)
    if res.get("grupo") in OPCIONES:
        cv2.circle(img, (int(GRUPO_X[OPCIONES.index(res["grupo"])]), int(GRUPO_Y)), 24, VERDE, 7)

    # ---- franja superior con los datos leídos ----
    dni = res.get("dni", "")
    fecha = "{}/{}/{}".format(*(("%02d" % res["dia"]) if res.get("dia") else "??",
                               ("%02d" % res["mes"]) if res.get("mes") else "??",
                               res.get("anio") or "????"))
    banda = np.full((190, W, 3), 255, np.uint8)
    cv2.rectangle(banda, (0, 0), (W - 1, 189), (245, 235, 245), -1)
    ok_dni = "?" not in dni and "_" not in dni and len(dni) == 8
    _texto(banda, "DNI leido: " + (dni if dni else "-"), 60, 85, 2.4, (0, 120, 0) if ok_dni else (0, 0, 220), 6)
    _texto(banda, "Area: %s    Fecha: %s" % (res.get("grupo") or "?", fecha), 60, 160, 1.7, (60, 60, 60), 4)
    if nombre:
        _texto(banda, str(nombre)[:34], 1250, 85, 1.8, (30, 30, 30), 4)
    img = np.vstack([banda, img])
    esc = ancho / float(W)
    img = cv2.resize(img, (ancho, int(img.shape[0] * esc)), interpolation=cv2.INTER_AREA)
    ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 76])
    return buf.tobytes() if ok else None


def recorte_nombre(res):
    """Recorte (JPEG, escala de grises) de la zona donde el alumno escribió sus apellidos y
    nombres: sirve cuando no hay DNI (examen relámpago), como hace ZipGrade."""
    w = res.get("_warped")
    if w is None:
        return None
    x0, y0, x1, y1 = NOMBRE_ZONA
    zona = w[y0:y1, x0:x1]
    zona = cv2.resize(zona, None, fx=0.55, fy=0.55, interpolation=cv2.INTER_AREA)
    ok, buf = cv2.imencode(".jpg", zona, [cv2.IMWRITE_JPEG_QUALITY, 62])
    return buf.tobytes() if ok else None
