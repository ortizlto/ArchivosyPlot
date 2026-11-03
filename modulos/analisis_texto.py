"""
analisis_texto.py
-----------------
Lógica (cálculos) del Submenú 1: procesamiento de archivos .txt.
Estas funciones NO imprimen ni piden datos: reciben información y devuelven
resultados. La interacción con el usuario está en menu_texto.py.
"""

import os

from modulos.archivos import leer_lineas
from modulos.config import (PALABRAS_VACIAS, SIGNOS_PUNTUACION, NIVELES_LOG,
                            PALABRAS_ERROR, MESES, ANCHO_INTERVALO,
                            MAX_INTERVALOS)


# ----------------------------------------------------------------------------
# Carga del archivo
# ----------------------------------------------------------------------------
def quitar_licencia_gutenberg(lineas):
    """
    Los libros del Proyecto Gutenberg traen una licencia en inglés al inicio
    y al final. Si se encuentran las marcas '*** START OF' y '*** END OF',
    se devuelve solo el texto del libro.
    Retorna (lineas_del_cuerpo, True) o (lineas_originales, False).
    """
    inicio = -1
    fin = len(lineas)
    for i in range(len(lineas)):
        if inicio == -1 and lineas[i].startswith("*** START OF"):
            inicio = i
        elif inicio != -1 and lineas[i].startswith("*** END OF"):
            fin = i
            break
    if inicio == -1:
        return lineas, False
    return lineas[inicio + 1:fin], True


def cargar_texto(ruta):
    """
    Lee un archivo .txt y devuelve un diccionario con todo lo necesario para
    analizarlo. El conteo de palabras se calcula una sola vez aquí y se
    reutiliza en el resumen y en el Gráfico 1.
    """
    lineas, codificacion = leer_lineas(ruta)
    lineas, licencia_omitida = quitar_licencia_gutenberg(lineas)
    datos = {
        "nombre": os.path.basename(ruta),
        "ruta": ruta,
        "lineas": lineas,
        "codificacion": codificacion,
        "licencia_omitida": licencia_omitida,
        "conteo_palabras": contar_palabras(lineas),
    }
    return datos


# ----------------------------------------------------------------------------
# Resumen estadístico
# ----------------------------------------------------------------------------
def limpiar_palabra(token):
    """
    Normaliza una palabra: la pasa a minúscula y le quita signos y números
    de los extremos. Si no queda ninguna letra devuelve "" (no es palabra).
    Ej: '¡Sancho,' -> 'sancho'   |   '404' -> ''
    """
    palabra = token.lower().strip(SIGNOS_PUNTUACION)
    for caracter in palabra:
        if caracter.isalpha():
            return palabra
    return ""


def separar_tokens(linea):
    """Divide una línea en tokens; los guiones largos también separan palabras."""
    linea = linea.replace("--", " ").replace("—", " ")
    return linea.split()


def contar_palabras(lineas):
    """
    Cuenta cuántas veces aparece cada palabra, EXCLUYENDO las palabras vacías
    (conectores, artículos, preposiciones...). Devuelve un diccionario
    {palabra: cantidad}.
    """
    conteo = {}
    for linea in lineas:
        for token in separar_tokens(linea):
            palabra = limpiar_palabra(token)
            if palabra != "" and palabra not in PALABRAS_VACIAS:
                if palabra in conteo:
                    conteo[palabra] = conteo[palabra] + 1
                else:
                    conteo[palabra] = 1
    return conteo


def calcular_resumen(lineas):
    """
    Calcula las estadísticas básicas del texto:
      - total de líneas y cuántas están vacías
      - total de palabras (todo lo separado por espacios)
      - caracteres con espacios (sin contar los saltos de línea)
      - caracteres sin espacios (sin espacios, tabulaciones ni saltos)
    """
    total_palabras = 0
    caracteres_con_espacios = 0
    caracteres_sin_espacios = 0
    lineas_vacias = 0

    for linea in lineas:
        tokens = linea.split()
        if len(tokens) == 0:
            lineas_vacias = lineas_vacias + 1
        total_palabras = total_palabras + len(tokens)
        caracteres_con_espacios = caracteres_con_espacios + len(linea)
        caracteres_sin_espacios = caracteres_sin_espacios + len("".join(tokens))

    resumen = {
        "total_lineas": len(lineas),
        "lineas_vacias": lineas_vacias,
        "total_palabras": total_palabras,
        "caracteres_con_espacios": caracteres_con_espacios,
        "caracteres_sin_espacios": caracteres_sin_espacios,
    }
    return resumen


# ----------------------------------------------------------------------------
# Extracción de patrones (bitácoras / logs)
# ----------------------------------------------------------------------------
def extraer_fecha_log(linea):
    """
    Busca la fecha de una línea de log y la devuelve en formato DD/Mes/AAAA
    (o AAAA-MM-DD si el log usa ese formato). Reconoce tres formatos:
      1) ISO al inicio:        2015-05-17 10:05:03 ...
      2) Apache (accesos):     ... [17/May/2015:10:05:03 +0000] ...
      3) Apache (errores):     [Sun Dec 04 04:47:44 2005] ...
    Si no encuentra fecha devuelve "".
    """
    # Formato 1: AAAA-MM-DD al inicio de la línea
    if (len(linea) >= 10 and linea[4] == "-" and linea[7] == "-"
            and linea[:4].isdigit() and linea[5:7].isdigit()
            and linea[8:10].isdigit()):
        return linea[:10]

    # Formatos 2 y 3: la fecha está entre corchetes
    inicio = linea.find("[")
    if inicio == -1:
        return ""
    fin = linea.find("]", inicio)
    if fin == -1:
        return ""
    contenido = linea[inicio + 1:fin]

    if contenido.count("/") == 2 and ":" in contenido:
        return contenido.split(":")[0]

    partes = contenido.split()
    if len(partes) == 5 and partes[1] in MESES and ":" in partes[3]:
        return partes[2] + "/" + partes[1] + "/" + partes[4]
    return ""


def extraer_codigo_http(linea):
    """
    En un log de accesos el código de estado HTTP va justo después de la
    petición entre comillas:  "GET /index.html HTTP/1.1" 404 512
    Devuelve el código ('404') o "" si la línea no lo tiene.
    """
    partes = linea.split('"')
    if len(partes) < 3:
        return ""
    tokens = partes[2].split()
    if len(tokens) > 0 and len(tokens[0]) == 3 and tokens[0].isdigit():
        return tokens[0]
    return ""


def extraer_nivel_log(linea):
    """
    Busca el nivel de severidad (ERROR, WARN, INFO, NOTICE...) en las
    primeras palabras de la línea. Ej: '[...] [error] mod_jk ...' -> 'ERROR'
    """
    tokens = linea.split()
    limite = min(6, len(tokens))
    for i in range(limite):
        token = tokens[i].strip("[]:()").lower()
        if token in NIVELES_LOG:
            return token.upper()
    return ""


def es_archivo_log(lineas):
    """
    Decide si el texto parece una bitácora: revisa hasta 200 líneas no
    vacías y, si al menos la mitad tienen una fecha reconocible, es un log.
    """
    revisadas = 0
    con_fecha = 0
    for linea in lineas:
        if linea.strip() == "":
            continue
        revisadas = revisadas + 1
        if extraer_fecha_log(linea) != "":
            con_fecha = con_fecha + 1
        if revisadas == 200:
            break
    return revisadas > 0 and con_fecha * 2 >= revisadas


def sumar_uno(diccionario, clave):
    """Suma 1 al contador 'clave' del diccionario (lo crea si no existe)."""
    if clave in diccionario:
        diccionario[clave] = diccionario[clave] + 1
    else:
        diccionario[clave] = 1


def analizar_patrones(lineas):
    """
    Recorre todas las líneas una sola vez y cuenta:
      - líneas que contienen cada palabra clave de error (siempre)
      - niveles de severidad, códigos HTTP y registros por fecha
        (solo si el archivo parece un log)
    Las fechas quedan en orden de aparición (los logs son cronológicos).
    """
    es_log = es_archivo_log(lineas)
    palabras_error = {}
    for palabra in PALABRAS_ERROR:
        palabras_error[palabra] = 0
    niveles = {}
    codigos = {}
    fechas = {}

    for linea in lineas:
        minuscula = linea.lower()
        for palabra in PALABRAS_ERROR:
            if palabra in minuscula:
                palabras_error[palabra] = palabras_error[palabra] + 1

        if es_log:
            nivel = extraer_nivel_log(linea)
            if nivel != "":
                sumar_uno(niveles, nivel)
            codigo = extraer_codigo_http(linea)
            if codigo != "":
                sumar_uno(codigos, codigo)
            fecha = extraer_fecha_log(linea)
            if fecha != "":
                sumar_uno(fechas, fecha)

    resultado = {
        "es_log": es_log,
        "palabras_error": palabras_error,
        "niveles": niveles,
        "codigos": codigos,
        "fechas": fechas,
    }
    return resultado


def contar_errores_http(codigos):
    """Devuelve (errores_4xx, errores_5xx) a partir del conteo de códigos."""
    errores_cliente = 0
    errores_servidor = 0
    for codigo in codigos:
        if codigo.startswith("4"):
            errores_cliente = errores_cliente + codigos[codigo]
        elif codigo.startswith("5"):
            errores_servidor = errores_servidor + codigos[codigo]
    return errores_cliente, errores_servidor


def buscar_patron(lineas, patron, max_ejemplos=3):
    """
    Cuenta las líneas que contienen 'patron' (sin distinguir mayúsculas)
    y guarda hasta 'max_ejemplos' líneas de ejemplo con su número.
    Devuelve (cantidad, ejemplos) donde ejemplos = [(n_linea, texto), ...].
    """
    patron_minuscula = patron.lower()
    cantidad = 0
    ejemplos = []
    numero = 1
    for linea in lineas:
        if patron_minuscula in linea.lower():
            cantidad = cantidad + 1
            if len(ejemplos) < max_ejemplos:
                ejemplos.append((numero, linea))
        numero = numero + 1
    return cantidad, ejemplos


# ----------------------------------------------------------------------------
# Datos para el Gráfico 2 (histograma)
# ----------------------------------------------------------------------------
def longitudes_de_lineas(lineas):
    """Devuelve una lista con la cantidad de caracteres de cada línea."""
    longitudes = []
    for linea in lineas:
        longitudes.append(len(linea))
    return longitudes


def calcular_intervalos(longitud_maxima):
    """
    Calcula los bordes y etiquetas de los grupos del histograma:
    0-50, 51-100, 101-150, ...  Los bordes van en .5 (ej. 50.5) para que
    cada número entero caiga en un solo grupo sin ambigüedad.
    Si se necesitan más de MAX_INTERVALOS grupos, el último agrupa todo lo
    que sobra (ej. '951+').
    Devuelve (bordes, etiquetas, limite) donde 'limite' es el valor máximo
    representable (las longitudes mayores se ubican en el último grupo).
    """
    cantidad = (longitud_maxima + ANCHO_INTERVALO - 1) // ANCHO_INTERVALO
    if cantidad < 1:
        cantidad = 1
    hay_recorte = cantidad > MAX_INTERVALOS
    if hay_recorte:
        cantidad = MAX_INTERVALOS

    bordes = [-0.5]
    etiquetas = []
    for i in range(cantidad):
        desde = i * ANCHO_INTERVALO + 1
        if i == 0:
            desde = 0
        hasta = (i + 1) * ANCHO_INTERVALO
        bordes.append(hasta + 0.5)
        etiquetas.append(str(desde) + "-" + str(hasta))

    if hay_recorte:
        etiquetas[-1] = str((cantidad - 1) * ANCHO_INTERVALO + 1) + "+"
    limite = cantidad * ANCHO_INTERVALO
    return bordes, etiquetas, limite


def agrupar_longitudes(longitudes):
    """
    Cuenta cuántas líneas caen en cada grupo (para mostrarlo en consola).
    Devuelve (etiquetas, cantidades, bordes, longitudes_ajustadas).
    """
    maximo = 0
    for longitud in longitudes:
        if longitud > maximo:
            maximo = longitud
    bordes, etiquetas, limite = calcular_intervalos(maximo)

    cantidades = []
    for _ in etiquetas:
        cantidades.append(0)
    ajustadas = []
    for longitud in longitudes:
        valor = min(longitud, limite)
        ajustadas.append(valor)
        if valor == 0:
            indice = 0
        else:
            indice = (valor - 1) // ANCHO_INTERVALO
        cantidades[indice] = cantidades[indice] + 1
    return etiquetas, cantidades, bordes, ajustadas
