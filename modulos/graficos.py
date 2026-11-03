"""
graficos.py
-----------
Los 5 gráficos del proyecto, hechos con matplotlib:
  1. Barras horizontales (barh)  -> palabras más frecuentes
  2. Histograma (hist)           -> longitud de las líneas
  3. Líneas (plot)               -> evolución / tendencia
  4. Pastel (pie)                -> participación por categoría
  5. Dispersión (scatter)        -> correlación entre dos variables

Cada función recibe datos YA calculados, dibuja, guarda la imagen en
/outputs y la muestra en pantalla si el entorno lo permite.
"""

import os

from modulos.config import RUTA_SALIDAS, MAX_ETIQUETAS_EJE_X
from modulos.utilidades import formatear_numero, porcentaje

# Si matplotlib no está instalado el programa sigue funcionando
# (todo lo de consola), solo se desactivan los gráficos.
try:
    import matplotlib
    import matplotlib.pyplot as plt
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False

# Paleta de colores (orden fijo y probado para daltonismo) y tintas neutras
COLORES_SERIES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100",
                  "#e87ba4", "#008300", "#6250d6", "#e34948")
COLOR_OTROS = "#c3c2b7"
COLOR_FONDO = "#fcfcfb"
COLOR_TEXTO = "#0b0b0b"
COLOR_TEXTO_SECUNDARIO = "#52514e"
COLOR_APAGADO = "#898781"
COLOR_CUADRICULA = "#e1e0d9"
COLOR_EJE = "#c3c2b7"


# ----------------------------------------------------------------------------
# Funciones de apoyo
# ----------------------------------------------------------------------------
def crear_figura(ancho, alto):
    """Crea una figura y sus ejes con el estilo común del proyecto."""
    figura, ejes = plt.subplots(figsize=(ancho, alto))
    figura.patch.set_facecolor(COLOR_FONDO)
    ejes.set_facecolor(COLOR_FONDO)
    for lado in ("top", "right"):
        ejes.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ejes.spines[lado].set_color(COLOR_EJE)
    ejes.tick_params(colors=COLOR_TEXTO_SECUNDARIO, labelsize=9)
    ejes.set_axisbelow(True)
    return figura, ejes


def poner_titulos(ejes, titulo, subtitulo, etiqueta_x, etiqueta_y):
    """Escribe título, subtítulo (fuente de datos) y nombres de los ejes."""
    ejes.set_title(titulo, loc="left", fontsize=13, fontweight="bold",
                   color=COLOR_TEXTO, pad=22)
    ejes.text(0, 1.02, subtitulo, transform=ejes.transAxes, fontsize=9,
              color=COLOR_TEXTO_SECUNDARIO)
    ejes.set_xlabel(etiqueta_x, color=COLOR_TEXTO_SECUNDARIO, fontsize=10)
    ejes.set_ylabel(etiqueta_y, color=COLOR_TEXTO_SECUNDARIO, fontsize=10)


def guardar_y_mostrar(figura, nombre_archivo):
    """
    Guarda la figura como PNG en la carpeta /outputs (la crea si no existe),
    la muestra si hay una ventana gráfica disponible y libera la memoria.
    Devuelve la ruta del archivo guardado.
    """
    os.makedirs(RUTA_SALIDAS, exist_ok=True)
    ruta = os.path.join(RUTA_SALIDAS, nombre_archivo + ".png")
    figura.tight_layout()
    figura.savefig(ruta, dpi=150, facecolor=COLOR_FONDO)
    # El backend 'agg' no abre ventanas (por ejemplo, en un servidor sin pantalla)
    if matplotlib.get_backend().lower() != "agg":
        print("  (Cierre la ventana del gráfico para continuar)")
        plt.show()
    plt.close(figura)
    return ruta


# ----------------------------------------------------------------------------
# Gráfico 1: barras horizontales
# ----------------------------------------------------------------------------
def grafico_barras_palabras(pares, nombre_fuente, nombre_archivo):
    """
    pares: [(palabra, cantidad), ...] ordenados de mayor a menor.
    La palabra más frecuente queda arriba.
    """
    palabras = []
    cantidades = []
    for palabra, cantidad in pares:
        palabras.append(palabra)
        cantidades.append(cantidad)

    figura, ejes = crear_figura(9, 5.5)
    barras = ejes.barh(palabras, cantidades, color=COLORES_SERIES[0],
                       height=0.65, edgecolor=COLOR_FONDO, linewidth=2)
    ejes.invert_yaxis()
    ejes.grid(axis="x", color=COLOR_CUADRICULA, linewidth=0.8)
    ejes.spines["left"].set_visible(False)
    ejes.tick_params(axis="y", length=0, labelsize=10, labelcolor=COLOR_TEXTO)

    # Valor al final de cada barra
    maximo = max(cantidades)
    for barra, cantidad in zip(barras, cantidades):
        ejes.text(barra.get_width() + maximo * 0.01,
                  barra.get_y() + barra.get_height() / 2,
                  formatear_numero(cantidad), va="center", fontsize=9,
                  color=COLOR_TEXTO_SECUNDARIO)
    ejes.set_xlim(0, maximo * 1.12)

    poner_titulos(ejes, "Las " + str(len(pares)) + " palabras más frecuentes",
                  "Archivo: " + nombre_fuente + "  ·  sin conectores ni artículos",
                  "Número de apariciones", "")
    return guardar_y_mostrar(figura, nombre_archivo)


# ----------------------------------------------------------------------------
# Gráfico 2: histograma
# ----------------------------------------------------------------------------
def histograma_longitudes(longitudes, bordes, etiquetas, nombre_fuente,
                          nombre_archivo):
    """
    longitudes: lista con los caracteres de cada línea (ya ajustada al límite).
    bordes / etiquetas: grupos calculados en analisis_texto.calcular_intervalos.
    """
    figura, ejes = crear_figura(10, 5.5)
    conteos, _, barras = ejes.hist(longitudes, bins=bordes,
                                   color=COLORES_SERIES[0],
                                   edgecolor=COLOR_FONDO, linewidth=2)
    ejes.grid(axis="y", color=COLOR_CUADRICULA, linewidth=0.8)

    # Etiqueta de cada grupo debajo del centro de su barra
    centros = []
    for i in range(len(etiquetas)):
        centros.append((bordes[i] + bordes[i + 1]) / 2)
    rotacion = 0
    if len(etiquetas) > 8:
        rotacion = 45
    ejes.set_xticks(centros)
    ejes.set_xticklabels(etiquetas, rotation=rotacion)

    # Cantidad encima de cada barra (si no son demasiadas)
    total = len(longitudes)
    if len(etiquetas) <= 12:
        for i in range(len(conteos)):
            if conteos[i] > 0:
                texto = formatear_numero(conteos[i]) + "\n(" + \
                    "{:.1f}".format(porcentaje(conteos[i], total)) + " %)"
                ejes.text(centros[i], conteos[i], texto, ha="center",
                          va="bottom", fontsize=8, color=COLOR_TEXTO_SECUNDARIO)
        ejes.set_ylim(0, max(conteos) * 1.18)

    poner_titulos(ejes, "Distribución de la longitud de las líneas",
                  "Archivo: " + nombre_fuente + "  ·  " +
                  formatear_numero(total) + " líneas en grupos de 50 caracteres",
                  "Caracteres por línea", "Número de líneas")
    return guardar_y_mostrar(figura, nombre_archivo)


# ----------------------------------------------------------------------------
# Gráfico 3: líneas
# ----------------------------------------------------------------------------
def grafico_lineas(xs, ys, x_es_texto, nombre_x, nombre_y, nombre_fuente,
                   nombre_archivo, ventana=None, movil=None):
    """
    xs, ys: valores de los ejes. Si X es texto (ej. fechas) se ubican los
    puntos en posiciones 0, 1, 2... y solo se rotulan algunas etiquetas para
    que no se amontonen.
    ventana/movil: tamaño y valores del promedio móvil (opcional).
    """
    figura, ejes = crear_figura(11, 5.5)

    if x_es_texto:
        posiciones = list(range(len(xs)))
    else:
        posiciones = xs

    if movil is None:
        ejes.plot(posiciones, ys, color=COLORES_SERIES[0], linewidth=2,
                  label=nombre_y)
    else:
        # Datos originales tenues y la tendencia (promedio móvil) resaltada
        ejes.plot(posiciones, ys, color=COLOR_APAGADO, linewidth=0.8,
                  alpha=0.6, label=nombre_y + " (dato original)")
        ejes.plot(posiciones[ventana - 1:], movil, color=COLORES_SERIES[0],
                  linewidth=2.2,
                  label="Promedio móvil de " + str(ventana) + " registros")
        # Espacio libre arriba para que la leyenda no tape los datos
        minimo_y = min(ys)
        maximo_y = max(ys)
        margen = (maximo_y - minimo_y) * 0.05
        ejes.set_ylim(minimo_y - margen, maximo_y + (maximo_y - minimo_y) * 0.22)
        ejes.legend(frameon=False, fontsize=9, loc="upper left", ncol=2,
                    labelcolor=COLOR_TEXTO_SECUNDARIO)

    if not x_es_texto and len(xs) <= 15:
        # Pocos puntos numéricos (ej. años): una marca por cada valor
        ejes.set_xticks(xs)
        ejes.plot(posiciones, ys, "o", color=COLORES_SERIES[0], markersize=8,
                  markeredgecolor=COLOR_FONDO, markeredgewidth=2)

    if x_es_texto:
        paso = max(1, len(xs) // MAX_ETIQUETAS_EJE_X)
        marcas = []
        etiquetas = []
        for i in range(0, len(xs), paso):
            marcas.append(i)
            etiquetas.append(str(xs[i]))
        ejes.set_xticks(marcas)
        ejes.set_xticklabels(etiquetas, rotation=35, ha="right")
        ejes.set_xlim(-1, len(xs))

    ejes.grid(axis="y", color=COLOR_CUADRICULA, linewidth=0.8)
    poner_titulos(ejes, "Evolución de " + nombre_y + " según " + nombre_x,
                  "Archivo: " + nombre_fuente + "  ·  " +
                  formatear_numero(len(xs)) + " puntos",
                  nombre_x, nombre_y)
    return guardar_y_mostrar(figura, nombre_archivo)


# ----------------------------------------------------------------------------
# Gráfico 4: pastel
# ----------------------------------------------------------------------------
def etiqueta_porcentaje(valor):
    """matplotlib llama esta función con el % de cada porción para rotularla."""
    if valor < 4:
        return ""
    return "{:.1f} %".format(valor)


def grafico_pastel(etiquetas, cantidades, nombre_columna, nombre_fuente,
                   nombre_archivo):
    """
    etiquetas / cantidades: categorías y su conteo (la última puede ser 'Otros').
    Los porcentajes pequeños (< 4 %) no se escriben dentro de la porción para
    que no se encimen; todos aparecen en la leyenda.
    """
    total = 0
    for cantidad in cantidades:
        total = total + cantidad

    colores = []
    for i in range(len(etiquetas)):
        if etiquetas[i] == "Otros":
            colores.append(COLOR_OTROS)
        else:
            colores.append(COLORES_SERIES[i % len(COLORES_SERIES)])

    figura, ejes = crear_figura(9.5, 6)
    porciones, _, textos = ejes.pie(
        cantidades, colors=colores, autopct=etiqueta_porcentaje, startangle=90,
        counterclock=False, pctdistance=0.72,
        wedgeprops={"edgecolor": COLOR_FONDO, "linewidth": 2})
    ejes.axis("equal")

    # Texto blanco sobre colores fuertes, oscuro sobre amarillo y gris
    for i in range(len(textos)):
        if colores[i] in ("#eda100", COLOR_OTROS):
            textos[i].set_color(COLOR_TEXTO)
        else:
            textos[i].set_color("white")
        textos[i].set_fontsize(10)
        textos[i].set_fontweight("bold")

    leyenda = []
    for i in range(len(etiquetas)):
        leyenda.append("{}  —  {} ({:.1f} %)".format(
            etiquetas[i], formatear_numero(cantidades[i]),
            porcentaje(cantidades[i], total)))
    ejes.legend(porciones, leyenda, loc="center left",
                bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=10,
                labelcolor=COLOR_TEXTO)

    ejes.set_title("Participación por " + nombre_columna, loc="left",
                   fontsize=13, fontweight="bold", color=COLOR_TEXTO)
    ejes.text(0, -0.04, "Archivo: " + nombre_fuente + "  ·  " +
              formatear_numero(total) + " registros con dato",
              transform=ejes.transAxes, fontsize=9,
              color=COLOR_TEXTO_SECUNDARIO)
    return guardar_y_mostrar(figura, nombre_archivo)


# ----------------------------------------------------------------------------
# Gráfico 5: dispersión
# ----------------------------------------------------------------------------
def grafico_dispersion(grupos, nombre_x, nombre_y, r, interpretacion,
                       nombre_fuente, nombre_archivo):
    """
    grupos: lista de (nombre_grupo, xs, ys). Si hay un solo grupo, todos los
    puntos tienen el mismo color; si hay varios, cada uno tiene su color y
    aparece en la leyenda.
    r: coeficiente de correlación de Pearson (se muestra en el título).
    """
    figura, ejes = crear_figura(9, 6)
    total = 0
    for _, xs, _ in grupos:
        total = total + len(xs)
    # Con muchos puntos se usan marcadores más pequeños para que no se tapen
    tamano = 42
    if total > 800:
        tamano = 24

    for i in range(len(grupos)):
        nombre, xs, ys = grupos[i]
        if nombre == "Otros":
            color = COLOR_OTROS
        else:
            color = COLORES_SERIES[i % len(COLORES_SERIES)]
        ejes.scatter(xs, ys, s=tamano, color=color, alpha=0.85,
                     edgecolors=COLOR_FONDO, linewidths=0.8,
                     label=nombre + " (" + formatear_numero(len(xs)) + ")")

    if len(grupos) > 1:
        ejes.legend(frameon=False, fontsize=9, labelcolor=COLOR_TEXTO,
                    loc="best")
    ejes.grid(color=COLOR_CUADRICULA, linewidth=0.8)

    if r is None:
        texto_r = "r no calculable"
    else:
        texto_r = "r = {:.2f} (correlación {})".format(r, interpretacion)
    poner_titulos(ejes, nombre_y + " vs. " + nombre_x + "  ·  " + texto_r,
                  "Archivo: " + nombre_fuente + "  ·  " +
                  formatear_numero(total) + " pares válidos",
                  nombre_x, nombre_y)
    return guardar_y_mostrar(figura, nombre_archivo)
