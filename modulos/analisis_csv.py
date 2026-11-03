"""
analisis_csv.py
---------------
Lógica (cálculos) del Submenú 2: análisis de datasets .csv.
Estas funciones NO imprimen ni piden datos. La interacción con el usuario
está en menu_csv.py.
"""

import csv
import os

from modulos.archivos import detectar_codificacion
from modulos.config import VALORES_NULOS
from modulos.utilidades import top_n


# ----------------------------------------------------------------------------
# Carga del archivo
# ----------------------------------------------------------------------------
def detectar_delimitador(primera_linea):
    """
    Elige el separador que más se repite en el encabezado.
    Muchos datos abiertos de Colombia usan ';' en lugar de ','.
    """
    mejor = ","
    mayor = -1
    for candidato in (",", ";", "\t", "|"):
        veces = primera_linea.count(candidato)
        if veces > mayor:
            mejor = candidato
            mayor = veces
    return mejor


def cargar_csv(ruta):
    """
    Lee un archivo .csv y devuelve un diccionario con:
    nombre, ruta, encabezados, filas (lista de listas de texto),
    delimitador y codificacion.

    - Se ignoran las filas completamente vacías.
    - Las filas incompletas se rellenan con "" y las que tienen celdas de más
      se recortan, para que todas tengan el mismo número de columnas.
    Lanza ValueError si el archivo no tiene datos.
    """
    codificacion = detectar_codificacion(ruta)
    with open(ruta, "r", encoding=codificacion, newline="") as archivo:
        primera_linea = archivo.readline()
        if primera_linea.strip() == "":
            raise ValueError("El archivo está vacío o la primera línea no tiene encabezados.")
        delimitador = detectar_delimitador(primera_linea)
        archivo.seek(0)
        lector = csv.reader(archivo, delimiter=delimitador)

        encabezados = []
        numero = 1
        for celda in next(lector):
            nombre = celda.strip()
            if nombre == "":
                nombre = "columna_" + str(numero)
            encabezados.append(nombre)
            numero = numero + 1

        filas = []
        total_columnas = len(encabezados)
        for fila in lector:
            if len(fila) == 0 or "".join(fila).strip() == "":
                continue
            fila_limpia = []
            for i in range(total_columnas):
                if i < len(fila):
                    fila_limpia.append(fila[i].strip())
                else:
                    fila_limpia.append("")
            filas.append(fila_limpia)

    if len(filas) == 0:
        raise ValueError("El archivo solo tiene encabezados, no tiene registros.")

    datos = {
        "nombre": os.path.basename(ruta),
        "ruta": ruta,
        "encabezados": encabezados,
        "filas": filas,
        "delimitador": delimitador,
        "codificacion": codificacion,
    }
    return datos


# ----------------------------------------------------------------------------
# Limpieza y tipos de dato
# ----------------------------------------------------------------------------
def es_nulo(texto):
    """True si la celda está vacía o tiene un marcador de dato faltante (NA, null...)."""
    return texto.strip().lower() in VALORES_NULOS


def convertir_a_numero(texto):
    """
    Convierte el texto de una celda en número (float).
    Acepta formato latino y formato inglés:
        '3,5' -> 3.5     '1.200,5' -> 1200.5     '1,200.5' -> 1200.5
    Devuelve None si la celda es nula o no es un número válido.
    """
    if es_nulo(texto):
        return None
    texto = texto.strip().replace(" ", "")
    if "," in texto and "." in texto:
        if texto.rfind(",") > texto.rfind("."):
            texto = texto.replace(".", "").replace(",", ".")   # 1.200,5
        else:
            texto = texto.replace(",", "")                     # 1,200.5
    elif texto.count(",") == 1:
        texto = texto.replace(",", ".")                        # 3,5
    try:
        numero = float(texto)
    except ValueError:
        return None
    # float() acepta 'inf' y 'nan', que no son datos útiles
    if numero != numero or numero == float("inf") or numero == float("-inf"):
        return None
    return numero


def obtener_columna(datos, indice):
    """Devuelve la lista de valores (texto) de la columna 'indice'."""
    valores = []
    for fila in datos["filas"]:
        valores.append(fila[indice])
    return valores


def tipo_de_columna(datos, indice):
    """
    Clasifica una columna como 'numérica', 'texto' o 'vacía'.
    Es numérica si al menos el 90 % de sus valores no nulos son números.
    """
    no_nulos = 0
    numericos = 0
    for valor in obtener_columna(datos, indice):
        if not es_nulo(valor):
            no_nulos = no_nulos + 1
            if convertir_a_numero(valor) is not None:
                numericos = numericos + 1
    if no_nulos == 0:
        return "vacía"
    if numericos >= 0.9 * no_nulos:
        return "numérica"
    return "texto"


def tipos_de_columnas(datos):
    """Devuelve una lista con el tipo de cada columna (en el mismo orden)."""
    tipos = []
    for i in range(len(datos["encabezados"])):
        tipos.append(tipo_de_columna(datos, i))
    return tipos


def limpiar_numeros(valores):
    """
    Separa los valores válidos de los inválidos.
    Devuelve (lista_de_numeros, cantidad_descartada).
    """
    numeros = []
    descartados = 0
    for valor in valores:
        numero = convertir_a_numero(valor)
        if numero is None:
            descartados = descartados + 1
        else:
            numeros.append(numero)
    return numeros, descartados


# ----------------------------------------------------------------------------
# Estadísticas descriptivas
# ----------------------------------------------------------------------------
def calcular_mediana(numeros):
    """Ordena una copia de la lista y toma el valor central (o el promedio de los dos centrales)."""
    ordenados = sorted(numeros)
    n = len(ordenados)
    mitad = n // 2
    if n % 2 == 1:
        return ordenados[mitad]
    return (ordenados[mitad - 1] + ordenados[mitad]) / 2


def calcular_estadisticas(numeros):
    """
    Calcula total de registros válidos, promedio, mediana, máximo y mínimo.
    Se recorre la lista una sola vez para la suma, el máximo y el mínimo.
    Devuelve None si la lista está vacía.
    """
    if len(numeros) == 0:
        return None
    suma = 0.0
    maximo = numeros[0]
    minimo = numeros[0]
    for numero in numeros:
        suma = suma + numero
        if numero > maximo:
            maximo = numero
        if numero < minimo:
            minimo = numero
    estadisticas = {
        "validos": len(numeros),
        "promedio": suma / len(numeros),
        "mediana": calcular_mediana(numeros),
        "maximo": maximo,
        "minimo": minimo,
    }
    return estadisticas


# ----------------------------------------------------------------------------
# Datos para el Gráfico 3 (líneas)
# ----------------------------------------------------------------------------
def pares_para_tendencia(datos, indice_x, indice_y, x_es_numerica):
    """
    Arma los pares (x, y) para el gráfico de líneas, descartando las filas
    donde X es nula o Y no es un número.
    Si X se repite (ej. varias ventas el mismo día) los valores de Y se
    acumulan en una lista para luego resumirlos.
    Devuelve (diccionario {x: [y1, y2...]}, filas_descartadas).
    """
    grupos = {}
    descartadas = 0
    for fila in datos["filas"]:
        texto_x = fila[indice_x]
        y = convertir_a_numero(fila[indice_y])
        if es_nulo(texto_x) or y is None:
            descartadas = descartadas + 1
            continue
        if x_es_numerica:
            x = convertir_a_numero(texto_x)
            if x is None:
                descartadas = descartadas + 1
                continue
        else:
            x = texto_x
        if x in grupos:
            grupos[x].append(y)
        else:
            grupos[x] = [y]
    return grupos, descartadas


def hay_valores_repetidos(grupos):
    """True si algún valor de X tiene más de un valor de Y."""
    for x in grupos:
        if len(grupos[x]) > 1:
            return True
    return False


def resumir_grupos(grupos, metodo, ordenar):
    """
    Convierte {x: [y...]} en dos listas (xs, ys).
    metodo: 'promedio' o 'suma' para combinar los Y repetidos.
    ordenar: True para ordenar X de menor a mayor (X numérica); si es False
    se conserva el orden del archivo (útil para fechas).
    """
    claves = list(grupos.keys())
    if ordenar:
        claves = sorted(claves)
    xs = []
    ys = []
    for x in claves:
        total = 0.0
        for y in grupos[x]:
            total = total + y
        if metodo == "promedio":
            total = total / len(grupos[x])
        xs.append(x)
        ys.append(total)
    return xs, ys


def enteros_si_es_posible(valores):
    """
    Si todos los números de la lista son enteros (ej. años 2007.0, 2008.0)
    los devuelve como int para que se vean sin '.0'. Si no, la lista igual.
    """
    for valor in valores:
        if valor != int(valor):
            return valores
    enteros = []
    for valor in valores:
        enteros.append(int(valor))
    return enteros


def promedio_movil(valores, ventana):
    """
    Promedio móvil simple: cada punto es el promedio de los últimos 'ventana'
    valores. Suaviza el ruido diario y deja ver la tendencia.
    Devuelve una lista más corta: empieza en la posición ventana-1.
    """
    resultado = []
    suma = 0.0
    for i in range(len(valores)):
        suma = suma + valores[i]
        if i >= ventana:
            suma = suma - valores[i - ventana]
        if i >= ventana - 1:
            resultado.append(suma / ventana)
    return resultado


# ----------------------------------------------------------------------------
# Datos para el Gráfico 4 (pastel)
# ----------------------------------------------------------------------------
def contar_categorias(valores):
    """
    Cuenta cuántas veces aparece cada categoría, ignorando los valores nulos.
    Devuelve (diccionario {categoria: cantidad}, cantidad_de_nulos).
    """
    conteo = {}
    nulos = 0
    for valor in valores:
        if es_nulo(valor):
            nulos = nulos + 1
        elif valor in conteo:
            conteo[valor] = conteo[valor] + 1
        else:
            conteo[valor] = 1
    return conteo, nulos


def agrupar_otros(conteo, maximo):
    """
    Ordena las categorías de mayor a menor. Si hay más de 'maximo', deja las
    'maximo' más grandes y suma el resto en una categoría 'Otros' (un pastel
    con demasiadas porciones no se puede leer).
    Devuelve (etiquetas, cantidades).
    """
    total = 0
    for categoria in conteo:
        total = total + conteo[categoria]

    if len(conteo) <= maximo + 1:
        pares = top_n(conteo, len(conteo))
    else:
        pares = top_n(conteo, maximo)

    etiquetas = []
    cantidades = []
    suma_mostrada = 0
    for categoria, cantidad in pares:
        etiquetas.append(categoria)
        cantidades.append(cantidad)
        suma_mostrada = suma_mostrada + cantidad
    if suma_mostrada < total:
        etiquetas.append("Otros")
        cantidades.append(total - suma_mostrada)
    return etiquetas, cantidades


# ----------------------------------------------------------------------------
# Datos para el Gráfico 5 (dispersión)
# ----------------------------------------------------------------------------
def pares_numericos(datos, indice_x, indice_y):
    """
    Devuelve (xs, ys, filas_usadas, descartadas) con las filas donde ambas
    columnas son números válidos. 'filas_usadas' guarda el índice de cada
    fila original para poder colorear los puntos por categoría después.
    """
    xs = []
    ys = []
    filas_usadas = []
    descartadas = 0
    for i in range(len(datos["filas"])):
        fila = datos["filas"][i]
        x = convertir_a_numero(fila[indice_x])
        y = convertir_a_numero(fila[indice_y])
        if x is None or y is None:
            descartadas = descartadas + 1
        else:
            xs.append(x)
            ys.append(y)
            filas_usadas.append(i)
    return xs, ys, filas_usadas, descartadas


def agrupar_puntos(datos, indice_categoria, xs, ys, filas_usadas, maximo):
    """
    Reparte los puntos del gráfico de dispersión según una columna
    categórica (ej. especie). Las 'maximo' categorías más frecuentes tienen
    su propio grupo; las demás van a 'Otros'.
    Devuelve una lista [(nombre_grupo, xs_grupo, ys_grupo), ...].
    """
    # 1) Categoría de cada punto
    categorias = []
    conteo = {}
    for indice_fila in filas_usadas:
        categoria = datos["filas"][indice_fila][indice_categoria]
        if es_nulo(categoria):
            categoria = "Sin dato"
        categorias.append(categoria)
        if categoria in conteo:
            conteo[categoria] = conteo[categoria] + 1
        else:
            conteo[categoria] = 1

    # 2) Se eligen las más frecuentes, de mayor a menor (el mismo orden del
    #    gráfico de pastel, así cada categoría conserva su color)
    elegidas = []
    for categoria, _ in top_n(conteo, maximo):
        elegidas.append(categoria)

    # 3) Se reparten los puntos
    grupos = {}
    for categoria in elegidas:
        grupos[categoria] = ([], [])
    hay_otros = len(conteo) > maximo
    if hay_otros:
        grupos["Otros"] = ([], [])
    for i in range(len(xs)):
        categoria = categorias[i]
        if categoria not in elegidas:
            categoria = "Otros"
        grupos[categoria][0].append(xs[i])
        grupos[categoria][1].append(ys[i])

    resultado = []
    for nombre in grupos:
        resultado.append((nombre, grupos[nombre][0], grupos[nombre][1]))
    return resultado


def correlacion_pearson(xs, ys):
    """
    Coeficiente de correlación de Pearson (r), entre -1 y 1:
       r = Σ(x - x̄)(y - ȳ) / sqrt( Σ(x - x̄)² · Σ(y - ȳ)² )
    Devuelve None si no se puede calcular (menos de 2 datos o sin variación).
    """
    n = len(xs)
    if n < 2:
        return None
    media_x = 0.0
    media_y = 0.0
    for i in range(n):
        media_x = media_x + xs[i]
        media_y = media_y + ys[i]
    media_x = media_x / n
    media_y = media_y / n

    numerador = 0.0
    suma_cuadrados_x = 0.0
    suma_cuadrados_y = 0.0
    for i in range(n):
        dx = xs[i] - media_x
        dy = ys[i] - media_y
        numerador = numerador + dx * dy
        suma_cuadrados_x = suma_cuadrados_x + dx * dx
        suma_cuadrados_y = suma_cuadrados_y + dy * dy
    if suma_cuadrados_x == 0 or suma_cuadrados_y == 0:
        return None
    return numerador / (suma_cuadrados_x * suma_cuadrados_y) ** 0.5


def interpretar_correlacion(r):
    """Traduce el valor de r a palabras (fuerza y dirección de la relación)."""
    if r is None:
        return "no se puede calcular"
    fuerza = abs(r)
    if fuerza >= 0.7:
        texto = "fuerte"
    elif fuerza >= 0.4:
        texto = "moderada"
    elif fuerza >= 0.2:
        texto = "débil"
    else:
        return "prácticamente nula"
    if r > 0:
        return texto + " positiva"
    return texto + " negativa"
