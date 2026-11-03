import os

try:
    import matplotlib
    import matplotlib.pyplot as plt
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.join(RUTA_BASE, "data")
RUTA_SALIDAS = os.path.join(RUTA_BASE, "outputs")
EXTENSIONES_VALIDAS = (".txt", ".csv")

TOP_RESUMEN, TOP_GRAFICO, ANCHO_INT, MAX_INT = 5, 10, 50, 12
FILAS_INI, FILAS_FIN, ANCHO_CELDA = 10, 5, 14
MAX_PASTEL, MAX_DISP, MAX_ETIQ_X = 7, 3, 10

VALORES_NULOS = {"", "na", "n/a", "nan", "null", "none", "-", "--", "?", "sin dato", "nd", "s/d"}
NIVELES_LOG = ("emerg", "alert", "crit", "critical", "fatal", "error", "warn", "warning", "notice", "info", "debug", "trace")
PALABRAS_ERROR = ("error", "fail", "fatal", "denied", "exception", "timeout", "warn")
MESES = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
SIGNOS_PUNTUACION = ".,;:¡!¿?\"'()[]{}<>«»-—_*/\\|#$%&=+~^`´¨…“”‘’0123456789º"

PALABRAS_VACIAS = {
    "el","la","los","las","un","una","unos","unas","lo","al","del","a","á","ante","bajo","con","contra",
    "de","desde","en","entre","hacia","hasta","para","por","según","sin","so","sobre","tras","durante",
    "mediante","y","e","é","o","ó","u","ni","que","pero","mas","más","sino","aunque","porque","pues",
    "como","cómo","cuando","si","mientras","donde","dónde","ya","así","luego","entonces","también",
    "tampoco","qué","cual","cuál","cuales","cuyo","cuya","quien","quién","quienes","no","sí","muy","tan",
    "tanto","tanta","tantos","tantas","aquí","allí","ahí","acá","allá","solo","sólo","aun","aún","todo",
    "toda","todos","todas","otro","otra","otros","otras","yo","tú","él","ella","ello","ellos","ellas",
    "nosotros","vosotros","me","te","se","nos","os","le","les","mí","ti","conmigo","contigo","consigo",
    "mi","mis","tu","tus","su","sus","nuestro","nuestra","nuestros","nuestras","vuestro","vuestra",
    "vuestros","vuestras","este","esta","esto","estos","estas","ese","esa","eso","esos","esas","aquel",
    "aquella","aquello","aquellos","aquellas","es","son","era","eran","fue","fueron","ser","sea","sido",
    "soy","eres","fuese","fuera","ha","han","he","has","había","habían","hay","haber","habiendo","hubo",
    "hubiese","hubiera","está","están","estaba","estar","estoy","tiene","tienen","tenía","tenían","tener",
    "tengo","tuvo","puede","pueden","podía","podían","poder","pudo","hace","hacen","hacía","hacer","hizo",
    "uno","dos","tres","cada","casi","mismo","misma","mismos","mismas","tal","tales","algo","alguno",
    "alguna","algunos","algunas","ningún","ninguno","ninguna","mucho","mucha","muchos","muchas","poco",
    "poca","pocos","pocas","siempre","nunca","ahora","después","antes","menos","vez","veces","the","an",
    "and","or","of","to","in","on","for","with","at","by","from","as","into","about","than","then","but",
    "if","not","is","are","was","were","be","been","it","its","this","that","these","those","i","you",
    "she","we","they","my","your","his","her","our","their","him","them","do","does","did","have","had",
    "will","would","can","there"
}

COLORES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948")
C_OTROS, C_FONDO, C_TXT, C_SUBTXT, C_APAGADO, C_GRID, C_EJE = "#c3c2b7", "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"

def imprimir_titulo(t): print(f"\n{'=' * (len(t) + 4)}\n  {t}\n{'=' * (len(t) + 4)}")
def imprimir_subtitulo(t): print(f"\n{t}\n{'-' * len(t)}")
def pausar(): input("\nPresione Enter para continuar...")
def pedir_texto(msg): return input(msg).strip()

def pedir_opcion(msg, mini, maxi):
    while True:
        r = input(msg).strip()
        if r.isdigit() and mini <= int(r) <= maxi: return int(r)
        print(f"  [!] Opción inválida ({mini}-{maxi}).")

def pedir_entero_opcional(msg, mini, maxi):
    while True:
        r = input(msg).strip()
        if not r: return None
        if r.isdigit() and mini <= int(r) <= maxi: return int(r)
        print(f"  [!] Escriba un número ({mini}-{maxi}) o Enter para omitir.")

def pedir_si_no(msg):
    while True:
        r = input(msg + " (s/n): ").strip().lower()
        if r in ("s", "si", "sí"): return True
        if r in ("n", "no"): return False
        print("  [!] Responda 's' o 'n'.")

def top_n(conteos, n): return sorted(conteos.items(), key=lambda x: x[1], reverse=True)[:n]
def formatear_numero(v, dec=2): return f"{int(v):,}" if v == int(v) and abs(v) < 1e15 else f"{v:,.{dec}f}"
def porcentaje(p, total): return (p * 100.0 / total) if total else 0.0
def recortar_texto(t, w): return t if len(t) <= w else t[:w - 2] + ".."
def ruta_relativa(r): return os.path.relpath(r, RUTA_BASE)

def tiene_letra(t):
    for c in t:
        if c.isalpha(): return True
    return False

def nombre_seguro(texto):
    s = ""
    for c in texto.lower(): s += c if c.isalnum() else "_"
    while "__" in s: s = s.replace("__", "_")
    return s.strip("_")[:60] or "archivo"

def listar_archivos(d, exts):
    if not os.path.exists(d): raise FileNotFoundError(f"La ruta '{d}' no existe.")
    if not os.path.isdir(d): raise NotADirectoryError(f"'{d}' no es una carpeta.")
    archivos = []
    for f in sorted(os.listdir(d)):
        ruta = os.path.join(d, f)
        ext = os.path.splitext(f)[1].lower()
        if os.path.isfile(ruta) and ext in exts:
            archivos.append({"nombre": f, "ruta": ruta, "extension": ext, "tamano_kb": os.path.getsize(ruta) / 1024})
    return archivos

def mostrar_lista_archivos(archivos):
    print("\n  N°   Tipo   Tamaño (KB)   Nombre\n  ---  -----  ------------  ----------------------------------------")
    for i, a in enumerate(archivos, 1):
        print(f"  {i:<3}  {a['extension']:<5}  {a['tamano_kb']:>12,.1f}  {a['nombre']}")

def explorar_directorio(actual):
    imprimir_titulo("EXPLORAR DIRECTORIO")
    r = pedir_texto(f"Ruta a explorar [Enter = {actual}]: ") or actual
    r = os.path.abspath(os.path.expanduser(r))
    try: archs = listar_archivos(r, EXTENSIONES_VALIDAS)
    except Exception as e: print(f"  [!] {e}"); return actual
    if not archs: print("\n  Carpeta válida sin archivos .txt ni .csv.")
    else:
        print(f"\n  Carpeta: {r}"); mostrar_lista_archivos(archs)
        txts = 0
        for a in archs:
            if a["extension"] == ".txt": txts += 1
        print(f"\n  Total: {txts} .txt y {len(archs) - txts} .csv")
    return r

def seleccionar_archivo(d, ext):
    try: archs = listar_archivos(d, (ext,))
    except Exception: print(f"  [!] No se pudo leer la carpeta '{d}'."); archs = []
    if archs: print(f"\nArchivos {ext} en {d}:"); mostrar_lista_archivos(archs)
    else: print(f"\n  No hay archivos {ext} en la carpeta actual.")
    print("\n  Escriba el número del archivo, una ruta completa, o 0 para volver.")
    while True:
        resp = pedir_texto("Archivo: ")
        if resp == "0": return None
        if resp.isdigit() and 1 <= int(resp) <= len(archs): return archs[int(resp) - 1]["ruta"]
        if not resp: print("  [!] Escriba una opción."); continue
        r = os.path.abspath(os.path.expanduser(resp))
        if not os.path.isfile(r): print(f"  [!] El archivo '{resp}' no existe.")
        elif os.path.splitext(r)[1].lower() != ext: print(f"  [!] Debe ser extensión {ext}.")
        else: return r

def leer_contenido(ruta):
    for enc in ("utf-8-sig", "latin-1"):
        try:
            with open(ruta, "r", encoding=enc) as f: return f.read(), enc
        except UnicodeDecodeError: pass
    return "", "utf-8"

def cargar_texto(ruta):
    raw, enc = leer_contenido(ruta)
    lines, skip = raw.splitlines(), False
    i1 = -1
    for i, l in enumerate(lines):
        if l.startswith("*** START OF"): i1 = i; break
    if i1 != -1:
        i2 = len(lines)
        for i in range(i1 + 1, len(lines)):
            if lines[i].startswith("*** END OF"): i2 = i; break
        lines, skip = lines[i1 + 1:i2], True
    conteo = {}
    for l in lines:
        for t in l.replace("--", " ").replace("—", " ").split():
            w = t.lower().strip(SIGNOS_PUNTUACION)
            if tiene_letra(w) and w not in PALABRAS_VACIAS:
                conteo[w] = conteo.get(w, 0) + 1
    return {"nombre": os.path.basename(ruta), "ruta": ruta, "lineas": lines,
            "codificacion": enc, "licencia_omitida": skip, "conteo_palabras": conteo}

def calcular_resumen(lines):
    vacias = words = chars = non_space = 0
    for l in lines:
        if not l.strip(): vacias += 1
        words += len(l.split())
        chars += len(l)
        non_space += len("".join(l.split()))
    ct = len(lines) - vacias
    return {"total_lineas": len(lines), "lineas_vacias": vacias, "total_palabras": words,
            "caracteres_con_espacios": chars, "caracteres_sin_espacios": non_space,
            "promedio_caracteres_linea": chars / ct if ct else 0.0}

def extraer_fecha_log(l):
    if len(l) >= 10 and l[:4].isdigit() and l[4] == '-' and l[5:7].isdigit() and l[7] == '-' and l[8:10].isdigit():
        return l[:10]
    if "[" in l and "]" in l:
        c = l[l.find("[") + 1 : l.find("]")]
        if c.count("/") == 2 and ":" in c: return c.split(":")[0]
        p = c.split()
        if len(p) == 5 and p[1] in MESES and ":" in p[3]: return f"{p[2]}/{p[1]}/{p[4]}"
    return ""

def extraer_codigo_http(l):
    p = l.split('"')
    if len(p) >= 3:
        toks = p[2].split()
        if toks and len(toks[0]) == 3 and toks[0].isdigit(): return toks[0]
    return ""

def extraer_nivel_log(l):
    for tok in l.split()[:6]:
        c = tok.strip("[]:()").lower()
        if c in NIVELES_LOG: return c.upper()
    return ""

def analizar_patrones(lines):
    sample, con_fecha = [], 0
    for l in lines:
        if len(sample) == 200: break
        if l.strip(): sample.append(l)
    for l in sample:
        if extraer_fecha_log(l): con_fecha += 1
    es_log = len(sample) > 0 and con_fecha * 2 >= len(sample)
    pe = {}
    for p in PALABRAS_ERROR: pe[p] = 0
    niveles, codigos, fechas, anios = {}, {}, {}, {}
    lit = {"capitulos": 0, "titulos": 0, "preguntas": 0, "exclamaciones": 0, "citas": 0}

    for l in lines:
        low = l.lower()
        for p in PALABRAS_ERROR:
            if p in low: pe[p] += 1
        if es_log:
            nv = extraer_nivel_log(l)
            if nv: niveles[nv] = niveles.get(nv, 0) + 1
            cd = extraer_codigo_http(l)
            if cd: codigos[cd] = codigos.get(cd, 0) + 1
            fc = extraer_fecha_log(l)
            if fc: fechas[fc] = fechas.get(fc, 0) + 1
        else:
            txt = l.strip()
            up = txt.upper()
            if (up.startswith("CAPÍTULO") or up.startswith("CAPITULO")) and len(up.split()) <= 3: lit["capitulos"] += 1
            elif txt and len(txt.split()) <= 8 and tiene_letra(txt) and txt.isupper(): lit["titulos"] += 1
            lit["preguntas"] += l.count("¿")
            lit["exclamaciones"] += l.count("¡")
            lit["citas"] += l.count("«")
            digitos = ""
            for c in l: digitos += c if c.isdigit() else " "
            for y in digitos.split():
                if len(y) == 4 and 1000 <= int(y) <= 2099: anios[y] = anios.get(y, 0) + 1
    return {"es_log": es_log, "palabras_error": pe, "niveles": niveles, "codigos": codigos,
            "fechas": fechas, "literarios": lit, "anios": anios, "años": anios}

def buscar_patron(lines, patron, max_ej=3):
    p_low = patron.lower()
    matches = []
    for i, l in enumerate(lines):
        if p_low in l.lower(): matches.append((i + 1, l))
    return len(matches), matches[:max_ej]

def agrupar_longitudes(longitudes):
    m = max(longitudes) if longitudes else 0
    cnt = min(MAX_INT, max(1, (m + ANCHO_INT - 1) // ANCHO_INT))
    lim = cnt * ANCHO_INT
    bordes, etiq = [-0.5], []
    for i in range(cnt):
        bordes.append((i + 1) * ANCHO_INT + 0.5)
        etiq.append(("0" if i == 0 else str(i * ANCHO_INT + 1)) + f"-{(i + 1) * ANCHO_INT}")
    if cnt == MAX_INT and m > lim: etiq[-1] = f"{(cnt - 1) * ANCHO_INT + 1}+"
    cant, ajust = [0] * cnt, []
    for l in longitudes:
        v = min(l, lim)
        ajust.append(v)
        cant[0 if v == 0 else (v - 1) // ANCHO_INT] += 1
    return etiq, cant, bordes, ajust

# --- CSV Y ESTADÍSTICAS (SIN NUMPY) ---
def parse_csv(text, sep):
    rows, row, cell, in_q = [], [], [], False
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if in_q:
            if c == '"':
                if i + 1 < n and text[i+1] == '"': cell.append('"'); i += 1
                else: in_q = False
            else: cell.append(c)
        elif c == '"': in_q = True
        elif c == sep: row.append("".join(cell)); cell = []
        elif c == '\n':
            row.append("".join(cell)); rows.append(row); row, cell = [], []
        elif c != '\r': cell.append(c)
        i += 1
    if cell or row: row.append("".join(cell)); rows.append(row)
    return rows

def to_num(val):
    if not val or val.lower().strip() in VALORES_NULOS: return None
    s = val.strip().replace(" ", "")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif s.count(",") == 1: s = s.replace(",", ".")
    try:
        n = float(s)
        return n if n == n and abs(n) != float("inf") else None
    except ValueError: return None

def es_nulo(t): return not t or t.strip().lower() in VALORES_NULOS

def cargar_csv(ruta):
    raw, enc = leer_contenido(ruta)
    p_line = raw.split("\n")[0]
    if not p_line.strip(): raise ValueError("El archivo está vacío.")
    sep = max((",", ";", "\t", "|"), key=p_line.count)
    regs = parse_csv(raw, sep)
    if not regs: raise ValueError("Sin datos.")
    hdrs = []
    for i, c in enumerate(regs[0]): hdrs.append(c.strip() or f"columna_{i+1}")
    filas = []
    for r in regs[1:]:
        if not "".join(r).strip(): continue
        fila = []
        for i in range(len(hdrs)): fila.append(r[i].strip() if i < len(r) else "")
        filas.append(fila)
    if not filas: raise ValueError("Solo tiene encabezados.")
    tipos = []
    for i in range(len(hdrs)):
        validos = numericos = 0
        for f in filas:
            if not es_nulo(f[i]):
                validos += 1
                if to_num(f[i]) is not None: numericos += 1
        if not validos: tipos.append("vacía")
        elif numericos >= 0.9 * validos: tipos.append("numérica")
        else: tipos.append("texto")
    return {"nombre": os.path.basename(ruta), "ruta": ruta, "encabezados": hdrs,
            "filas": filas, "delimitador": sep, "codificacion": enc, "tipos": tipos}

def stats(nums):
    if not nums: return None
    s = sorted(nums); n = len(s)
    med = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    return {"validos": n, "promedio": sum(nums) / n, "mediana": med, "maximo": max(nums), "minimo": min(nums)}

def pearson(xs, ys):
    n = len(xs)
    if n < 2: return None
    mx, my = sum(xs) / n, sum(ys) / n
    num = sx = sy = 0
    for x, y in zip(xs, ys):
        dx, dy = x - mx, y - my
        num += dx * dy
        sx += dx ** 2
        sy += dy ** 2
    den = (sx * sy) ** 0.5
    return num / den if den else None

def interpretar_correlacion(r):
    if r is None: return "no se puede calcular"
    f = abs(r)
    txt = "fuerte" if f >= 0.7 else "moderada" if f >= 0.4 else "débil" if f >= 0.2 else "prácticamente nula"
    return txt if f < 0.2 else f"{txt} {'positiva' if r > 0 else 'negativa'}"

def promedio_movil(ys, k):
    s, res = sum(ys[:k]), [sum(ys[:k]) / k]
    for i in range(k, len(ys)):
        s += ys[i] - ys[i - k]
        res.append(s / k)
    return res

def crear_figura(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(C_FONDO); ax.set_facecolor(C_FONDO)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(C_EJE)
    ax.tick_params(colors=C_SUBTXT, labelsize=9)
    ax.set_axisbelow(True)
    return fig, ax

def poner_titulos(ax, tit, sub, xl, yl):
    ax.set_title(tit, loc="left", fontsize=13, fontweight="bold", color=C_TXT, pad=22)
    ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=9, color=C_SUBTXT)
    ax.set_xlabel(xl, color=C_SUBTXT, fontsize=10)
    ax.set_ylabel(yl, color=C_SUBTXT, fontsize=10)

def guardar_y_mostrar(fig, nombre):
    os.makedirs(RUTA_SALIDAS, exist_ok=True)
    ruta = os.path.join(RUTA_SALIDAS, nombre + ".png")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150, facecolor=C_FONDO)
    if matplotlib.get_backend().lower() != "agg":
        print("  (Cierre la ventana del gráfico para continuar)")
        plt.show()
    plt.close(fig)
    return ruta

def grafico_barras_palabras(pares, fuente, nombre):
    words, counts = [], []
    for w, c in pares: words.append(w); counts.append(c)
    fig, ax = crear_figura(9, 5.5)
    bars = ax.barh(words, counts, color=COLORES[0], height=0.65, edgecolor=C_FONDO, linewidth=2)
    ax.invert_yaxis(); ax.grid(axis="x", color=C_GRID, linewidth=0.8)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=10, labelcolor=C_TXT)
    mx = max(counts)
    for b, c in zip(bars, counts):
        ax.text(b.get_width() + mx * 0.01, b.get_y() + b.get_height() / 2, formatear_numero(c),
                va="center", fontsize=9, color=C_SUBTXT)
    ax.set_xlim(0, mx * 1.12)
    poner_titulos(ax, f"Las {len(pares)} palabras más frecuentes", f"Archivo: {fuente}  ·  sin conectores ni artículos", "Número de apariciones", "")
    return guardar_y_mostrar(fig, nombre)

def histograma_longitudes(longitudes, bordes, etiq, fuente, nombre):
    fig, ax = crear_figura(10, 5.5)
    counts, _, _ = ax.hist(longitudes, bins=bordes, color=COLORES[0], edgecolor=C_FONDO, linewidth=2)
    ax.grid(axis="y", color=C_GRID, linewidth=0.8)
    centros = []
    for i in range(len(etiq)): centros.append((bordes[i] + bordes[i + 1]) / 2)
    ax.set_xticks(centros)
    ax.set_xticklabels(etiq, rotation=45 if len(etiq) > 8 else 0)
    tot = len(longitudes)
    for cnt, cen in zip(counts, centros):
        if cnt > 0:
            ax.text(cen, cnt, f"{formatear_numero(cnt)}\n({porcentaje(cnt, tot):.1f} %)",
                    ha="center", va="bottom", fontsize=8, color=C_SUBTXT)
    ax.set_ylim(0, max(counts) * 1.18 if max(counts) else 1)
    poner_titulos(ax, "Distribución de la longitud de las líneas",
                  f"Archivo: {fuente}  ·  {formatear_numero(tot)} líneas en grupos de 50 caracteres",
                  "Caracteres por línea", "Número de líneas")
    return guardar_y_mostrar(fig, nombre)

def grafico_lineas(xs, ys, x_es_texto, nom_x, nom_y, fuente, nombre, ventana, movil):
    fig, ax = crear_figura(11, 5.5)
    pos = list(range(len(xs))) if x_es_texto else xs
    if movil is None:
        ax.plot(pos, ys, color=COLORES[0], linewidth=2, label=nom_y)
    else:
        ax.plot(pos, ys, color=C_APAGADO, linewidth=0.8, alpha=0.6, label=f"{nom_y} (dato original)")
        ax.plot(pos[ventana - 1:], movil, color=COLORES[0], linewidth=2.2, label=f"Promedio móvil de {ventana} registros")
        rng = max(ys) - min(ys)
        ax.set_ylim(min(ys) - rng * 0.05, max(ys) + rng * 0.22)
        ax.legend(frameon=False, fontsize=9, loc="upper left", ncol=2, labelcolor=C_SUBTXT)
    if not x_es_texto and len(xs) <= 15:
        ax.set_xticks(xs)
        ax.plot(pos, ys, "o", color=COLORES[0], markersize=8, markeredgecolor=C_FONDO, markeredgewidth=2)
    if x_es_texto:
        step = max(1, len(xs) // MAX_ETIQ_X)
        ticks, etiquetas = [], []
        for i in range(0, len(xs), step): ticks.append(i); etiquetas.append(str(xs[i]))
        ax.set_xticks(ticks)
        ax.set_xticklabels(etiquetas, rotation=35, ha="right")
        ax.set_xlim(-1, len(xs))
    ax.grid(axis="y", color=C_GRID, linewidth=0.8)
    poner_titulos(ax, f"Evolución de {nom_y} según {nom_x}", f"Archivo: {fuente}  ·  {formatear_numero(len(xs))} puntos", nom_x, nom_y)
    return guardar_y_mostrar(fig, nombre)

def grafico_pastel(etiq, cant, col_nom, fuente, nombre):
    tot = sum(cant)
    cols = []
    for i, e in enumerate(etiq): cols.append(C_OTROS if e == "Otros" else COLORES[i % len(COLORES)])
    fig, ax = crear_figura(9.5, 6)
    wedges, _, txts = ax.pie(cant, colors=cols, autopct=lambda v: f"{v:.1f} %" if v >= 4 else "",
                             startangle=90, counterclock=False, pctdistance=0.72,
                             wedgeprops={"edgecolor": C_FONDO, "linewidth": 2})
    ax.axis("equal")
    for t, c in zip(txts, cols):
        t.set_color(C_TXT if c in ("#eda100", C_OTROS) else "white")
        t.set_fontsize(10); t.set_fontweight("bold")
    leyenda = []
    for e, c in zip(etiq, cant): leyenda.append(f"{e}  —  {formatear_numero(c)} ({porcentaje(c, tot):.1f} %)")
    ax.legend(wedges, leyenda, loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=10, labelcolor=C_TXT)
    ax.set_title(f"Participación por {col_nom}", loc="left", fontsize=13, fontweight="bold", color=C_TXT)
    ax.text(0, -0.04, f"Archivo: {fuente}  ·  {formatear_numero(tot)} registros con dato", transform=ax.transAxes, fontsize=9, color=C_SUBTXT)
    return guardar_y_mostrar(fig, nombre)

def grafico_dispersion(grupos, nom_x, nom_y, r, interp, fuente, nombre):
    fig, ax = crear_figura(9, 6)
    tot = 0
    for g in grupos: tot += len(g[1])
    s_size = 24 if tot > 800 else 42
    for i, (grp_nom, g_xs, g_ys) in enumerate(grupos):
        c = C_OTROS if grp_nom == "Otros" else COLORES[i % len(COLORES)]
        ax.scatter(g_xs, g_ys, s=s_size, color=c, alpha=0.85, edgecolors=C_FONDO, linewidths=0.8,
                   label=f"{grp_nom} ({formatear_numero(len(g_xs))})")
    if len(grupos) > 1: ax.legend(frameon=False, fontsize=9, labelcolor=C_TXT, loc="best")
    ax.grid(color=C_GRID, linewidth=0.8)
    txt_r = "r no calculable" if r is None else f"r = {r:.2f} (correlación {interp})"
    poner_titulos(ax, f"{nom_y} vs. {nom_x}  ·  {txt_r}", f"Archivo: {fuente}  ·  {formatear_numero(tot)} pares válidos", nom_x, nom_y)
    return guardar_y_mostrar(fig, nombre)

def imprimir_conteo(dic, total, limite=15):
    for i, (k, v) in enumerate(dic.items()):
        if i == limite:
            print(f"  ... y {len(dic) - limite} más")
            break
        print(f"  {k:<14} {formatear_numero(v):>10}   ({porcentaje(v, total):5.1f} %)")

def opcion_resumen_texto(datos):
    res = calcular_resumen(datos["lineas"])
    cp = datos["conteo_palabras"]
    imprimir_titulo("RESUMEN ESTADÍSTICO - " + datos["nombre"])
    print(f"  Total de líneas ...................... {formatear_numero(res['total_lineas'])}")
    print(f"     de ellas vacías ................... {formatear_numero(res['lineas_vacias'])}")
    print(f"  Total de palabras .................... {formatear_numero(res['total_palabras'])}")
    print(f"  Caracteres (con espacios) ............ {formatear_numero(res['caracteres_con_espacios'])}")
    print(f"  Caracteres (sin espacios) ............ {formatear_numero(res['caracteres_sin_espacios'])}")
    print(f"  Promedio de caracteres por línea ..... {formatear_numero(res['promedio_caracteres_linea'], 1)}  (sin contar líneas vacías)")
    print(f"  Palabras distintas (sin conectores) .. {formatear_numero(len(cp))}")
    imprimir_subtitulo(f"Top {TOP_RESUMEN} de palabras más repetidas (excluyendo conectores)")
    if not cp: print("  No se encontraron palabras."); return
    for i, (w, c) in enumerate(top_n(cp, TOP_RESUMEN), 1):
        print(f"  {i}. {w:<20} {formatear_numero(c):>10}")

def opcion_patrones(datos):
    lines = datos["lineas"]
    pat = analizar_patrones(lines)
    tot = len(lines)
    imprimir_titulo("EXTRACCIÓN DE PATRONES - " + datos["nombre"])
    print("  El archivo SÍ tiene formato de bitácora (log)." if pat["es_log"] else "  El archivo NO es una bitácora: se analiza como texto literario.")

    if pat["niveles"]:
        imprimir_subtitulo("Niveles de severidad encontrados")
        imprimir_conteo(dict(top_n(pat["niveles"], len(pat["niveles"]))), tot, 15)

    if pat["codigos"]:
        tc = sum(pat["codigos"].values())
        imprimir_subtitulo("Códigos de estado HTTP (de mayor a menor)")
        imprimir_conteo(dict(top_n(pat["codigos"], len(pat["codigos"]))), tc, 15)
        e4 = e5 = 0
        for k, c in pat["codigos"].items():
            if k.startswith("4"): e4 += c
            elif k.startswith("5"): e5 += c
        print(f"\n  Errores de cliente (4xx): {formatear_numero(e4)}   |   Errores de servidor (5xx): {formatear_numero(e5)}")
        if "404" in pat["codigos"]: print(f"  Páginas no encontradas (404): {formatear_numero(pat['codigos']['404'])}")

    if pat["fechas"]:
        imprimir_subtitulo("Registros por fecha (en orden de aparición)")
        imprimir_conteo(pat["fechas"], tot, 15)
        fp, cp = top_n(pat["fechas"], 1)[0]
        print(f"\n  Fecha con más registros: {fp} ({formatear_numero(cp)})")

    if not pat["es_log"]:
        lit = pat["literarios"]
        imprimir_subtitulo("Patrones literarios")
        print(f"  Encabezados de capítulo (CAPÍTULO ...) .. {formatear_numero(lit['capitulos'])}")
        print(f"  Títulos en MAYÚSCULAS (poemas, partes) .. {formatear_numero(lit['titulos'])}")
        print(f"  Preguntas (¿) ........................... {formatear_numero(lit['preguntas'])}")
        print(f"  Exclamaciones (¡) ....................... {formatear_numero(lit['exclamaciones'])}")
        print(f"  Citas o nombres entre comillas («) ...... {formatear_numero(lit['citas'])}")
        anios = pat["anios"]
        if anios:
            print("\n  Años mencionados (los 8 más frecuentes):")
            for y, c in top_n(anios, 8): print(f"     {y}: {formatear_numero(c)} vez/veces")
        else: print("\n  No se mencionan años (fechas de 4 cifras).")

    imprimir_subtitulo("Líneas que contienen palabras clave de error")
    imprimir_conteo(pat["palabras_error"], tot, 20)

    imprimir_subtitulo("Búsqueda personalizada")
    while True:
        p = pedir_texto("Texto o fecha a buscar (ej. 404, ERROR, Bogotá, 1858) [Enter = terminar]: ")
        if not p: break
        cnt, ejs = buscar_patron(lines, p)
        print(f"  '{p}' aparece en {formatear_numero(cnt)} línea(s) ({porcentaje(cnt, tot):.2f} % del archivo).")
        for num, txt in ejs: print(f"     línea {num}: {recortar_texto(txt.strip(), 95)}")

def opcion_grafico_palabras(datos):
    cp = datos["conteo_palabras"]
    if not cp: print("  [!] Sin palabras para graficar."); return
    pares = top_n(cp, TOP_GRAFICO)
    imprimir_titulo("GRÁFICO 1 - FRECUENCIA DE PALABRAS")
    for i, (w, c) in enumerate(pares, 1): print(f"  {i:>2}. {w:<20} {formatear_numero(c):>10}")
    if not MATPLOTLIB_DISPONIBLE: print("  [!] matplotlib no instalado."); return
    r = grafico_barras_palabras(pares, datos["nombre"], f"g1_barh_palabras_{nombre_seguro(os.path.splitext(datos['nombre'])[0])}")
    print("\n  Gráfico guardado en: " + ruta_relativa(r))

def opcion_grafico_longitudes(datos):
    lines = datos["lineas"]
    if not lines: print("  [!] Sin líneas para graficar."); return
    imprimir_titulo("GRÁFICO 2 - LONGITUD DE LÍNEAS")
    inc_vac = pedir_si_no("¿Incluir las líneas vacías (0 caracteres)?")
    longitudes = []
    for l in lines:
        if inc_vac or l.strip(): longitudes.append(len(l))
    if not longitudes: print("  [!] No quedan líneas para graficar."); return
    etiq, cant, bordes, ajust = agrupar_longitudes(longitudes)
    print("\n  Grupo (caracteres)    Líneas      %")
    for e, c in zip(etiq, cant): print(f"  {e:<18} {formatear_numero(c):>10}  {porcentaje(c, len(longitudes)):5.1f}")
    if not MATPLOTLIB_DISPONIBLE: print("  [!] matplotlib no instalado."); return
    r = histograma_longitudes(ajust, bordes, etiq, datos["nombre"], f"g2_hist_longitudes_{nombre_seguro(os.path.splitext(datos['nombre'])[0])}")
    print("\n  Gráfico guardado en: " + ruta_relativa(r))

def formatear_fila(etiqueta, celdas, anchos):
    txt = "  {:>5} ".format(etiqueta)
    for i in range(len(anchos)): txt += f"| {recortar_texto(celdas[i], anchos[i]).ljust(anchos[i])} "
    return txt

def imprimir_tabla(hdrs, filas, nums):
    limpias = []
    for row in filas:
        limpia = []
        for c in row: limpia.append(str(c).replace("\n", " "))
        limpias.append(limpia)
    anchos = []
    for i, h in enumerate(hdrs):
        mx = len(h)
        for r in limpias: mx = max(mx, len(r[i]))
        anchos.append(max(3, min(mx, ANCHO_CELDA)))
    sep = "  ----- "
    for w in anchos: sep += f"+{'-' * (w + 2)}"
    print(formatear_fila("Fila", hdrs, anchos) + "\n" + sep)
    for num, row in zip(nums, limpias): print(formatear_fila(num, row, anchos))

def seleccionar_columna(datos, mensaje, solo_num):
    permitidas = []
    for i, t in enumerate(datos["tipos"]):
        if not solo_num or t == "numérica": permitidas.append(i)
    if not permitidas:
        print("  [!] El archivo no tiene columnas numéricas."); return None
    print("\n" + mensaje)
    for i in permitidas: print(f"    {i+1:>2}. {datos['encabezados'][i]:<24} ({datos['tipos'][i]})")
    while True:
        resp = pedir_texto("Columna (número o nombre, 0 = cancelar): ")
        if resp == "0": return None
        idx = -1
        if resp.isdigit(): idx = int(resp) - 1
        else:
            for i, h in enumerate(datos["encabezados"]):
                if h.lower() == resp.lower(): idx = i; break
        if idx in permitidas: return idx
        print("  [!] Columna inválida o no numérica. Intente de nuevo.")

def opcion_vista_previa(datos):
    filas = datos["filas"]
    tot = len(filas)
    imprimir_titulo("VISTA PREVIA - " + datos["nombre"])
    print(f"  Registros: {formatear_numero(tot)}   |   Columnas: {len(datos['encabezados'])}   |   Separador: '{datos['delimitador']}'   |   Codificación: {datos['codificacion']}")
    print("\n  Columnas y tipo de dato detectado:")
    for i, (h, t) in enumerate(zip(datos["encabezados"], datos["tipos"]), 1): print(f"    {i:>2}. {h:<24} ({t})")
    if tot <= FILAS_INI + FILAS_FIN:
        imprimir_subtitulo(f"Todas las filas ({tot})")
        imprimir_tabla(datos["encabezados"], filas, list(range(1, tot + 1)))
    else:
        imprimir_subtitulo(f"Primeras {FILAS_INI} filas")
        imprimir_tabla(datos["encabezados"], filas[:FILAS_INI], list(range(1, FILAS_INI + 1)))
        imprimir_subtitulo(f"Últimas {FILAS_FIN} filas")
        imprimir_tabla(datos["encabezados"], filas[tot - FILAS_FIN:], list(range(tot - FILAS_FIN + 1, tot + 1)))

def opcion_estadisticas(datos):
    imprimir_titulo("ESTADÍSTICAS DESCRIPTIVAS")
    idx = seleccionar_columna(datos, "Columnas numéricas disponibles:", True)
    if idx is None: return
    nums, desc = [], 0
    for f in datos["filas"]:
        n = to_num(f[idx])
        if n is None: desc += 1
        else: nums.append(n)
    st = stats(nums)
    if not st: print("  [!] La columna no tiene valores numéricos válidos."); return
    imprimir_subtitulo("Columna: " + datos["encabezados"][idx])
    print(f"  Registros en el archivo ........... {formatear_numero(len(datos['filas']))}")
    print(f"  Nulos / vacíos eliminados ......... {formatear_numero(desc)}")
    print(f"  Total de registros válidos ........ {formatear_numero(st['validos'])}")
    print(f"  Promedio .......................... {formatear_numero(st['promedio'])}")
    print(f"  Mediana ........................... {formatear_numero(st['mediana'])}")
    print(f"  Valor máximo ...................... {formatear_numero(st['maximo'])}")
    print(f"  Valor mínimo ...................... {formatear_numero(st['minimo'])}")

def opcion_grafico_tendencia(datos):
    imprimir_titulo("GRÁFICO 3 - EVOLUCIÓN TEMPORAL / TENDENCIA")
    ix = seleccionar_columna(datos, "Eje X (ej. una fecha o un año):", False)
    if ix is None: return
    iy = seleccionar_columna(datos, "Eje Y (columna numérica):", True)
    if iy is None: return
    x_num = datos["tipos"][ix] == "numérica"
    grupos, desc = {}, 0
    for f in datos["filas"]:
        tx, y = f[ix], to_num(f[iy])
        if es_nulo(tx) or y is None: desc += 1; continue
        x = to_num(tx) if x_num else tx
        if x is None: desc += 1; continue
        grupos.setdefault(x, []).append(y)
    if len(grupos) < 2: print("  [!] Se necesitan al menos 2 valores distintos en X."); return
    metodo = "promedio"
    hay_repetidos = False
    for v in grupos.values():
        if len(v) > 1: hay_repetidos = True; break
    if hay_repetidos:
        print("\n  Hay valores de X repetidos. ¿Cómo combinar Y?\n    1. Promedio\n    2. Suma")
        if pedir_opcion("  Opción: ", 1, 2) == 2: metodo = "suma"
    keys = sorted(grupos.keys()) if x_num else list(grupos.keys())
    x_entera = x_num
    for k in keys:
        if not x_entera: break
        if k != int(k): x_entera = False
    xs, ys = [], []
    for k in keys:
        xs.append(int(k) if x_entera else k)
        ys.append(sum(grupos[k]) / len(grupos[k]) if metodo == "promedio" else sum(grupos[k]))
    ventana, movil = None, None
    if len(ys) >= 6:
        ventana = pedir_entero_opcional("Promedio móvil (ej. 30) [Enter = omitir]: ", 2, len(ys) // 2)
        if ventana: movil = promedio_movil(ys, ventana)
    nx, ny = datos["encabezados"][ix], datos["encabezados"][iy]
    print(f"\n  Puntos: {formatear_numero(len(xs))} | Nulos descartados: {formatear_numero(desc)}")
    print(f"  Primero: {xs[0]} -> {formatear_numero(ys[0])} | Último: {xs[-1]} -> {formatear_numero(ys[-1])}")
    if not MATPLOTLIB_DISPONIBLE: print("  [!] matplotlib no instalado."); return
    base = nombre_seguro(os.path.splitext(datos["nombre"])[0])
    r = grafico_lineas(xs, ys, not x_num, nx, ny, datos["nombre"], f"g3_plot_{base}_{nombre_seguro(ny)}_por_{nombre_seguro(nx)}", ventana, movil)
    print("\n  Gráfico guardado en: " + ruta_relativa(r))

def agrupar_otros(conteo, maximo):
    lbls, counts = [], []
    for e, c in top_n(conteo, maximo if len(conteo) > maximo + 1 else len(conteo)): lbls.append(e); counts.append(c)
    resto = sum(conteo.values()) - sum(counts)
    if resto > 0:
        lbls.append("Otros")
        counts.append(resto)
    return lbls, counts

def opcion_grafico_categorias(datos):
    imprimir_titulo("GRÁFICO 4 - COMPARACIÓN CATEGÓRICA")
    idx = seleccionar_columna(datos, "Columna categórica (ej. ciudad, tipo):", False)
    if idx is None: return
    col_nom = datos["encabezados"][idx]
    conteo, nulos = {}, 0
    for f in datos["filas"]:
        v = f[idx]
        if es_nulo(v): nulos += 1
        else: conteo[v] = conteo.get(v, 0) + 1
    if not conteo: print("  [!] Sin datos."); return
    if len(conteo) == 1: print("  [!] Una sola categoría.")
    if datos["tipos"][idx] == "numérica" and len(conteo) > 15:
        print(f"  [!] Columna numérica con {len(conteo)} valores distintos.")
        if not pedir_si_no("¿Desea continuar de todos modos?"): return
    etiq, cant = agrupar_otros(conteo, MAX_PASTEL)
    tot = len(datos["filas"]) - nulos
    imprimir_subtitulo(f"Participación por {col_nom}")
    for e, c in zip(etiq, cant): print(f"  {recortar_texto(e, 22):<22} {formatear_numero(c):>8}   {porcentaje(c, tot):5.1f} %")
    print(f"  Categorías: {len(conteo)} | Excluidos: {formatear_numero(nulos)}")
    if not MATPLOTLIB_DISPONIBLE: print("  [!] matplotlib no instalado."); return
    base = nombre_seguro(os.path.splitext(datos["nombre"])[0])
    r = grafico_pastel(etiq, cant, col_nom, datos["nombre"], f"g4_pie_{base}_{nombre_seguro(col_nom)}")
    print("\n  Gráfico guardado en: " + ruta_relativa(r))

def pares_numericos(datos, idx_x, idx_y):
    xs, ys, filas_usadas, desc = [], [], [], 0
    for i, f in enumerate(datos["filas"]):
        x, y = to_num(f[idx_x]), to_num(f[idx_y])
        if x is None or y is None: desc += 1
        else: xs.append(x); ys.append(y); filas_usadas.append(i)
    return xs, ys, filas_usadas, desc

def agrupar_puntos(datos, idx_c, xs, ys, filas, maximo):
    conteo = {}
    cats = []
    for f in filas:
        c = datos["filas"][f][idx_c]
        c = "Sin dato" if es_nulo(c) else c
        cats.append(c)
        conteo[c] = conteo.get(c, 0) + 1
    top_cats = set()
    for c, _ in top_n(conteo, maximo): top_cats.add(c)
    grupos = {}
    for c in top_cats: grupos[c] = ([], [])
    if len(conteo) > maximo: grupos["Otros"] = ([], [])
    for x, y, c in zip(xs, ys, cats):
        dest = c if c in top_cats else "Otros"
        grupos[dest][0].append(x)
        grupos[dest][1].append(y)
    resultado = []
    for k, v in grupos.items(): resultado.append((k, v[0], v[1]))
    return resultado

def opcion_grafico_correlacion(datos):
    imprimir_titulo("GRÁFICO 5 - CORRELACIÓN DE VARIABLES")
    ix = seleccionar_columna(datos, "Variable del eje X (numérica):", True)
    if ix is None: return
    iy = seleccionar_columna(datos, "Variable del eje Y (numérica):", True)
    if iy is None: return
    if iy == ix: print("  [!] Elija dos columnas distintas."); return
    xs, ys, filas, desc = pares_numericos(datos, ix, iy)
    if len(xs) < 2: print("  [!] Pares insuficientes."); return
    r = pearson(xs, ys)
    interp = interpretar_correlacion(r)
    ic = seleccionar_columna(datos, "Opcional: columna categórica para colorear (0 = sin agrupar):", False)
    grupos = [("Todos", xs, ys)] if ic is None else agrupar_puntos(datos, ic, xs, ys, filas, MAX_DISP)
    nx, ny = datos["encabezados"][ix], datos["encabezados"][iy]
    imprimir_subtitulo(f"{ny} vs. {nx}")
    print(f"  Pares válidos: {formatear_numero(len(xs))} | Nulos descartados: {formatear_numero(desc)}")
    print("  Coeficiente: no calculable" if r is None else f"  Pearson r = {r:.3f} -> correlación {interp}")
    if len(grupos) > 1:
        for g_nom, g_xs, _ in grupos: print(f"    {g_nom}: {formatear_numero(len(g_xs))} puntos")
    if not MATPLOTLIB_DISPONIBLE: print("  [!] matplotlib no instalado."); return
    base = nombre_seguro(os.path.splitext(datos["nombre"])[0])
    res = grafico_dispersion(grupos, nx, ny, r, interp, datos["nombre"], f"g5_scatter_{base}_{nombre_seguro(ny)}_vs_{nombre_seguro(nx)}")
    print("\n  Gráfico guardado en: " + ruta_relativa(res))

def menu_textos(dir_actual):
    imprimir_titulo("SELECCIONAR ARCHIVO .txt")
    ruta = seleccionar_archivo(dir_actual, ".txt")
    if not ruta: return
    try: datos = cargar_texto(ruta)
    except Exception as e: print(f"  [!] Error al cargar: {e}"); return
    print(f"\n  Archivo cargado: {datos['nombre']} ({formatear_numero(len(datos['lineas']))} líneas, {datos['codificacion']})")
    if datos["licencia_omitida"]: print("  Licencia Gutenberg omitida.")
    while True:
        imprimir_titulo("PROCESAR BITÁCORAS / TEXTOS REALES (.txt)")
        print(f"  Archivo actual: {datos['nombre']}")
        print("  1. Resumen estadístico del texto\n  2. Extracción de patrones (logs y literarios)\n  3. Gráfico 1 - Palabras frecuentes\n  4. Gráfico 2 - Longitud de líneas\n  5. Cargar otro .txt\n  6. Volver al menú principal")
        op = pedir_opcion("Seleccione una opción: ", 1, 6)
        if op == 6: return
        try:
            if op == 1: opcion_resumen_texto(datos)
            elif op == 2: opcion_patrones(datos)
            elif op == 3: opcion_grafico_palabras(datos)
            elif op == 4: opcion_grafico_longitudes(datos)
            elif op == 5:
                r2 = seleccionar_archivo(dir_actual, ".txt")
                if r2: datos = cargar_texto(r2)
        except Exception as e: print(f"  [!] Error: {e}")
        pausar()

def menu_csv(dir_actual):
    imprimir_titulo("SELECCIONAR ARCHIVO .csv")
    ruta = seleccionar_archivo(dir_actual, ".csv")
    if not ruta: return
    try: datos = cargar_csv(ruta)
    except Exception as e: print(f"  [!] Error: {e}"); return
    print(f"\n  Archivo cargado: {datos['nombre']} ({formatear_numero(len(datos['filas']))} registros, {len(datos['encabezados'])} cols, sep '{datos['delimitador']}')")
    while True:
        imprimir_titulo("ANALIZAR DATASET DE DATOS ABIERTOS (.csv)")
        print(f"  Archivo actual: {datos['nombre']}")
        print("  1. Vista previa de datos\n  2. Estadísticas descriptivas de una columna\n  3. Gráfico 3 - Tendencia / líneas\n  4. Gráfico 4 - Comparación categórica / pastel\n  5. Gráfico 5 - Correlación / dispersión\n  6. Cargar otro .csv\n  7. Volver al menú principal")
        op = pedir_opcion("Seleccione una opción: ", 1, 7)
        if op == 7: return
        try:
            if op == 1: opcion_vista_previa(datos)
            elif op == 2: opcion_estadisticas(datos)
            elif op == 3: opcion_grafico_tendencia(datos)
            elif op == 4: opcion_grafico_categorias(datos)
            elif op == 5: opcion_grafico_correlacion(datos)
            elif op == 6:
                r2 = seleccionar_archivo(dir_actual, ".csv")
                if r2: datos = cargar_csv(r2)
        except Exception as e: print(f"  [!] Error: {e}")
        pausar()

def main():
    directorio = RUTA_DATOS
    while True:
        imprimir_titulo("ANALIZADOR DE DATOS REALES - MENÚ PRINCIPAL")
        print(f"  Carpeta de trabajo: {directorio}")
        print("  1. Explorar directorio\n  2. Procesar bitácoras / textos reales (.txt)\n  3. Analizar dataset de datos abiertos (.csv)\n  4. Salir")
        op = pedir_opcion("Seleccione una opción: ", 1, 4)
        if op == 1: directorio = explorar_directorio(directorio)
        elif op == 2: menu_textos(directorio)
        elif op == 3: menu_csv(directorio)
        else: print("\n¡Gracias por usar el analizador! Hasta pronto."); break

if __name__ == "__main__":
    try: main()
    except (KeyboardInterrupt, EOFError): print("\n\nPrograma finalizado por el usuario.")
