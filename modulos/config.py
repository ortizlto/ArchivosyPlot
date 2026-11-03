"""
config.py
---------
Constantes globales del proyecto: rutas de carpetas, extensiones permitidas,
palabras vacías (conectores) y valores que se consideran "dato faltante".

Tener todo esto en un solo lugar evita "números mágicos" repartidos por el código.
"""

import os

# ----------------------------------------------------------------------------
# Rutas: se calculan a partir de la ubicación de este archivo, así el programa
# funciona sin importar desde qué carpeta se ejecute main.py
# ----------------------------------------------------------------------------
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DATOS = os.path.join(RUTA_BASE, "data")
RUTA_SALIDAS = os.path.join(RUTA_BASE, "outputs")

EXTENSIONES_VALIDAS = (".txt", ".csv")

# ----------------------------------------------------------------------------
# Parámetros de análisis
# ----------------------------------------------------------------------------
TOP_PALABRAS_RESUMEN = 5      # top de palabras en el resumen estadístico
TOP_PALABRAS_GRAFICO = 10     # barras del Gráfico 1
ANCHO_INTERVALO = 50          # ancho de cada grupo del histograma (Gráfico 2)
MAX_INTERVALOS = 12           # máximo de barras del histograma
FILAS_INICIO = 10             # vista previa: primeras filas
FILAS_FINAL = 5               # vista previa: últimas filas
ANCHO_CELDA = 14              # ancho máximo de una celda en la vista previa
MAX_CATEGORIAS_PASTEL = 7     # el resto de categorías se agrupa en "Otros"
MAX_CATEGORIAS_DISPERSION = 3  # categorías con color propio en el Gráfico 5
MAX_ETIQUETAS_EJE_X = 10      # etiquetas visibles en el eje X del Gráfico 3

# Valores (en minúscula) que se tratan como dato faltante en un CSV
VALORES_NULOS = ("", "na", "n/a", "nan", "null", "none", "-", "--", "?",
                 "sin dato", "nd", "s/d")

# Niveles de severidad que se buscan en las bitácoras (logs)
NIVELES_LOG = ("emerg", "alert", "crit", "critical", "fatal", "error",
               "warn", "warning", "notice", "info", "debug", "trace")

# Palabras clave que indican problemas dentro de una línea de log
PALABRAS_ERROR = ("error", "fail", "fatal", "denied", "exception", "timeout",
                  "warn")

# Abreviaturas de los meses en inglés (formato usado por Apache)
MESES = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

# Signos que se quitan al inicio y al final de cada palabra
SIGNOS_PUNTUACION = ".,;:¡!¿?\"'()[]{}<>«»-—_*/\\|#$%&=+~^`´¨…“”‘’0123456789"

# ----------------------------------------------------------------------------
# Palabras vacías (conectores, artículos, preposiciones, pronombres y verbos
# auxiliares) en español e inglés. Se usa un conjunto (set) porque buscar en
# él es mucho más rápido que buscar en una lista.
# ----------------------------------------------------------------------------
PALABRAS_VACIAS = {
    # --- Español: artículos y contracciones
    "el", "la", "los", "las", "un", "una", "unos", "unas", "lo", "al", "del",
    # --- Español: preposiciones
    "a", "ante", "bajo", "con", "contra", "de", "desde", "en", "entre",
    "hacia", "hasta", "para", "por", "según", "sin", "so", "sobre", "tras",
    "durante", "mediante",
    # --- Español: conjunciones y conectores
    "y", "e", "o", "u", "ni", "que", "pero", "mas", "más", "sino", "aunque",
    "porque", "pues", "como", "cómo", "cuando", "si", "mientras", "donde",
    "dónde", "ya", "así", "ansí", "luego", "entonces", "también", "tampoco",
    "qué", "cual", "cuál", "cuales", "cuyo", "cuya", "quien", "quién",
    "quienes", "no", "sí", "muy", "tan", "tanto", "tanta", "tantos", "tantas",
    "aquí", "allí", "ahí", "acá", "allá", "solo", "sólo", "aun", "aún",
    "todo", "toda", "todos", "todas", "otro", "otra", "otros", "otras",
    # --- Español: pronombres y posesivos
    "yo", "tú", "él", "ella", "ello", "ellos", "ellas", "nosotros", "vosotros",
    "me", "te", "se", "nos", "os", "le", "les", "mí", "ti", "conmigo",
    "contigo", "consigo", "mi", "mis", "tu", "tus", "su", "sus", "nuestro",
    "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros",
    "vuestras",
    "este", "esta", "esto", "estos", "estas", "ese", "esa", "eso", "esos",
    "esas", "aquel", "aquella", "aquello", "aquellos", "aquellas",
    # --- Español antiguo (frecuente en libros clásicos): de + pronombre
    "dél", "della", "dellos", "dellas", "desto", "deste", "desta", "destos",
    "destas", "dese", "desa", "deso", "aquese", "aquesta", "aqueste",
    # --- Español: verbos auxiliares muy frecuentes
    "es", "son", "era", "eran", "fue", "fueron", "ser", "sea", "sido", "soy",
    "eres", "fuese", "fuera", "ha", "han", "he", "has", "había", "habían",
    "hay", "haber", "habiendo", "hubo", "hubiese", "hubiera", "está", "están",
    "estaba", "estar", "estoy",
    # --- Inglés: artículos, preposiciones, conectores y pronombres
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
    "at", "by", "from", "as", "into", "about", "than", "then", "but", "if",
    "so", "not", "no", "is", "are", "was", "were", "be", "been", "it", "its",
    "this", "that", "these", "those", "i", "you", "he", "she", "we", "they",
    "my", "your", "his", "her", "our", "their", "me", "him", "them", "do",
    "does", "did", "have", "has", "had", "will", "would", "can", "there",
}
