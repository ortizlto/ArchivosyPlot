"""
menu_csv.py
-----------
SUBMENÚ 2: Análisis de datasets de datos abiertos (.csv).
Aquí está la interacción con el usuario (mostrar resultados y pedir datos).
Los cálculos se hacen en analisis_csv.py y los gráficos en graficos.py.
"""

import csv
import os

from modulos import graficos
from modulos.analisis_csv import (cargar_csv, tipos_de_columnas,
                                  obtener_columna, limpiar_numeros,
                                  calcular_estadisticas, pares_para_tendencia,
                                  hay_valores_repetidos, resumir_grupos,
                                  enteros_si_es_posible, promedio_movil, contar_categorias,
                                  agrupar_otros, pares_numericos,
                                  agrupar_puntos, correlacion_pearson,
                                  interpretar_correlacion)
from modulos.archivos import seleccionar_archivo
from modulos.config import (RUTA_BASE, FILAS_INICIO, FILAS_FINAL, ANCHO_CELDA,
                            MAX_CATEGORIAS_PASTEL, MAX_CATEGORIAS_DISPERSION)
from modulos.utilidades import (imprimir_titulo, imprimir_subtitulo, pausar,
                                pedir_opcion, pedir_texto, pedir_si_no,
                                pedir_entero_opcional, formatear_numero,
                                porcentaje, nombre_seguro, recortar_texto)


# ----------------------------------------------------------------------------
# Carga y submenú
# ----------------------------------------------------------------------------
def abrir_csv(directorio):
    """
    Pide al usuario un archivo .csv, lo carga y detecta el tipo de cada
    columna. Devuelve el diccionario de datos o None si hubo un problema.
    """
    ruta = seleccionar_archivo(directorio, ".csv")
    if ruta is None:
        return None
    try:
        datos = cargar_csv(ruta)
    except FileNotFoundError:
        print("  [!] El archivo ya no existe: " + ruta)
        return None
    except PermissionError:
        print("  [!] No tiene permisos para leer: " + ruta)
        return None
    except (ValueError, csv.Error) as error:
        print("  [!] El archivo no tiene un formato CSV válido: " + str(error))
        return None
    except OSError as error:
        print("  [!] No se pudo leer el archivo: " + str(error))
        return None

    datos["tipos"] = tipos_de_columnas(datos)
    print("\n  Archivo cargado: " + datos["nombre"] + "  ("
          + formatear_numero(len(datos["filas"])) + " registros, "
          + str(len(datos["encabezados"])) + " columnas, separador '"
          + datos["delimitador"] + "')")
    return datos


def mostrar_menu_csv(nombre_archivo):
    """Imprime las opciones del Submenú 2."""
    imprimir_titulo("ANALIZAR DATASET DE DATOS ABIERTOS (.csv)")
    print("  Archivo actual: " + nombre_archivo)
    print("  1. Vista previa de datos")
    print("  2. Estadísticas descriptivas de una columna")
    print("  3. Gráfico 3 - Evolución temporal / tendencia (líneas)")
    print("  4. Gráfico 4 - Comparación categórica (pastel)")
    print("  5. Gráfico 5 - Correlación de variables (dispersión)")
    print("  6. Cargar otro archivo .csv")
    print("  7. Volver al menú principal")


def menu_csv(directorio):
    """
    OPCIÓN 3 DEL MENÚ PRINCIPAL.
    Carga un .csv y repite el submenú hasta que el usuario elija volver.
    """
    imprimir_titulo("SELECCIONAR ARCHIVO .csv")
    datos = abrir_csv(directorio)
    if datos is None:
        return

    while True:
        mostrar_menu_csv(datos["nombre"])
        opcion = pedir_opcion("Seleccione una opción: ", 1, 7)
        if opcion == 7:
            return
        try:
            if opcion == 1:
                opcion_vista_previa(datos)
            elif opcion == 2:
                opcion_estadisticas(datos)
            elif opcion == 3:
                opcion_grafico_tendencia(datos)
            elif opcion == 4:
                opcion_grafico_categorias(datos)
            elif opcion == 5:
                opcion_grafico_correlacion(datos)
            elif opcion == 6:
                nuevos = abrir_csv(directorio)
                if nuevos is not None:
                    datos = nuevos
        except EOFError:
            raise
        except Exception as error:
            # Cualquier error inesperado se informa sin cerrar el programa
            print("  [!] Ocurrió un error inesperado: " + str(error))
        pausar()


# ----------------------------------------------------------------------------
# Funciones de apoyo para elegir columnas e imprimir tablas
# ----------------------------------------------------------------------------
def mostrar_columnas(datos, solo_numericas):
    """Lista las columnas con su número y el tipo de dato detectado."""
    for i in range(len(datos["encabezados"])):
        if solo_numericas and datos["tipos"][i] != "numérica":
            continue
        print("    {:>2}. {:<24} ({})".format(i + 1, datos["encabezados"][i],
                                            datos["tipos"][i]))


def seleccionar_columna(datos, mensaje, solo_numericas):
    """
    Pide una columna por número o por nombre. Devuelve su índice (desde 0)
    o None si el usuario escribe 0 (cancelar / ninguna).
    Si solo_numericas es True, solo acepta columnas numéricas.
    """
    permitidas = []
    for i in range(len(datos["encabezados"])):
        if not solo_numericas or datos["tipos"][i] == "numérica":
            permitidas.append(i)
    if len(permitidas) == 0:
        print("  [!] El archivo no tiene columnas numéricas.")
        return None

    print("\n" + mensaje)
    mostrar_columnas(datos, solo_numericas)
    while True:
        respuesta = pedir_texto("Columna (número o nombre, 0 = cancelar): ")
        if respuesta == "0":
            return None
        indice = -1
        if respuesta.isdigit():
            indice = int(respuesta) - 1
        else:
            for i in range(len(datos["encabezados"])):
                if datos["encabezados"][i].lower() == respuesta.lower():
                    indice = i
        if indice in permitidas:
            return indice
        if solo_numericas and 0 <= indice < len(datos["encabezados"]):
            print("  [!] Esa columna no es numérica. Elija una de la lista.")
        else:
            print("  [!] Columna no válida. Intente de nuevo.")


def imprimir_tabla(encabezados, filas, numeros_fila):
    """
    Imprime filas en forma de tabla alineada. Cada columna toma el ancho de
    su dato más largo, sin pasar de ANCHO_CELDA caracteres.
    """
    anchos = []
    for i in range(len(encabezados)):
        ancho = len(encabezados[i])
        for fila in filas:
            if len(fila[i]) > ancho:
                ancho = len(fila[i])
        anchos.append(max(3, min(ancho, ANCHO_CELDA)))

    linea = "  {:>5} ".format("Fila")
    separador = "  ----- "
    for i in range(len(encabezados)):
        linea = linea + "| " + recortar_texto(encabezados[i], anchos[i]).ljust(anchos[i]) + " "
        separador = separador + "+" + "-" * (anchos[i] + 2)
    print(linea)
    print(separador)
    for j in range(len(filas)):
        linea = "  {:>5} ".format(numeros_fila[j])
        for i in range(len(encabezados)):
            linea = linea + "| " + recortar_texto(filas[j][i], anchos[i]).ljust(anchos[i]) + " "
        print(linea)


def ruta_relativa(ruta):
    """Muestra la ruta del gráfico relativa a la carpeta del proyecto."""
    return os.path.relpath(ruta, RUTA_BASE)


def nombre_base(datos):
    """Nombre del archivo sin extensión, apto para nombrar las imágenes."""
    return nombre_seguro(os.path.splitext(datos["nombre"])[0])


# ----------------------------------------------------------------------------
# Opciones del submenú
# ----------------------------------------------------------------------------
def opcion_vista_previa(datos):
    """Muestra estructura del archivo, las primeras 10 filas y las últimas 5."""
    filas = datos["filas"]
    total = len(filas)
    imprimir_titulo("VISTA PREVIA - " + datos["nombre"])
    print("  Registros: " + formatear_numero(total) + "   |   Columnas: "
          + str(len(datos["encabezados"])) + "   |   Separador: '"
          + datos["delimitador"] + "'   |   Codificación: " + datos["codificacion"])
    print("\n  Columnas y tipo de dato detectado:")
    mostrar_columnas(datos, False)

    if total <= FILAS_INICIO + FILAS_FINAL:
        imprimir_subtitulo("Todas las filas (" + str(total) + ")")
        numeros = list(range(1, total + 1))
        imprimir_tabla(datos["encabezados"], filas, numeros)
        return

    imprimir_subtitulo("Primeras " + str(FILAS_INICIO) + " filas")
    imprimir_tabla(datos["encabezados"], filas[:FILAS_INICIO],
                   list(range(1, FILAS_INICIO + 1)))
    imprimir_subtitulo("Últimas " + str(FILAS_FINAL) + " filas")
    imprimir_tabla(datos["encabezados"], filas[total - FILAS_FINAL:],
                   list(range(total - FILAS_FINAL + 1, total + 1)))


def opcion_estadisticas(datos):
    """Limpia los nulos de una columna numérica y calcula sus estadísticas."""
    imprimir_titulo("ESTADÍSTICAS DESCRIPTIVAS")
    indice = seleccionar_columna(datos, "Columnas numéricas disponibles:", True)
    if indice is None:
        return
    nombre = datos["encabezados"][indice]
    numeros, descartados = limpiar_numeros(obtener_columna(datos, indice))
    estadisticas = calcular_estadisticas(numeros)
    if estadisticas is None:
        print("  [!] La columna no tiene valores numéricos válidos.")
        return

    imprimir_subtitulo("Columna: " + nombre)
    print("  Registros en el archivo ........... " + formatear_numero(len(datos["filas"])))
    print("  Nulos / vacíos eliminados ......... " + formatear_numero(descartados))
    print("  Total de registros válidos ........ " + formatear_numero(estadisticas["validos"]))
    print("  Promedio .......................... " + formatear_numero(estadisticas["promedio"]))
    print("  Mediana ........................... " + formatear_numero(estadisticas["mediana"]))
    print("  Valor máximo ...................... " + formatear_numero(estadisticas["maximo"]))
    print("  Valor mínimo ...................... " + formatear_numero(estadisticas["minimo"]))


def opcion_grafico_tendencia(datos):
    """
    GRÁFICO 3: líneas. El usuario elige X (ej. fecha) y Y (numérica).
    Si X se repite, se pregunta si combinar los Y por promedio o por suma.
    Opcionalmente se agrega un promedio móvil para ver la tendencia.
    """
    imprimir_titulo("GRÁFICO 3 - EVOLUCIÓN TEMPORAL / TENDENCIA")
    indice_x = seleccionar_columna(datos, "Eje X (ej. una fecha o un año):", False)
    if indice_x is None:
        return
    indice_y = seleccionar_columna(datos, "Eje Y (columna numérica):", True)
    if indice_y is None:
        return

    x_es_numerica = datos["tipos"][indice_x] == "numérica"
    grupos, descartadas = pares_para_tendencia(datos, indice_x, indice_y, x_es_numerica)
    if len(grupos) < 2:
        print("  [!] Se necesitan al menos 2 valores distintos en X para dibujar una línea.")
        return

    metodo = "promedio"
    if hay_valores_repetidos(grupos):
        print("\n  Hay valores de X repetidos. ¿Cómo combinar sus valores de Y?")
        print("    1. Promedio (ej. temperaturas)")
        print("    2. Suma (ej. ventas)")
        if pedir_opcion("  Opción: ", 1, 2) == 2:
            metodo = "suma"
    xs, ys = resumir_grupos(grupos, metodo, x_es_numerica)
    if x_es_numerica:
        xs = enteros_si_es_posible(xs)

    ventana = None
    movil = None
    if len(ys) >= 6:
        ventana = pedir_entero_opcional(
            "Promedio móvil: cantidad de registros a promediar (ej. 30) "
            "[Enter = omitir]: ", 2, len(ys) // 2)
        if ventana is not None:
            movil = promedio_movil(ys, ventana)

    nombre_x = datos["encabezados"][indice_x]
    nombre_y = datos["encabezados"][indice_y]
    print("\n  Puntos graficados: " + formatear_numero(len(xs))
          + "   |   Filas descartadas por datos nulos: " + formatear_numero(descartadas))
    print("  Primer punto: " + str(xs[0]) + " -> " + formatear_numero(ys[0])
          + "   |   Último punto: " + str(xs[-1]) + " -> " + formatear_numero(ys[-1]))

    if not graficos.MATPLOTLIB_DISPONIBLE:
        print("  [!] matplotlib no está instalado: no se puede dibujar el gráfico.")
        return
    nombre = ("g3_plot_" + nombre_base(datos) + "_" + nombre_seguro(nombre_y)
              + "_por_" + nombre_seguro(nombre_x))
    ruta = graficos.grafico_lineas(xs, ys, not x_es_numerica, nombre_x, nombre_y,
                                   datos["nombre"], nombre, ventana, movil)
    print("\n  Gráfico guardado en: " + ruta_relativa(ruta))


def opcion_grafico_categorias(datos):
    """
    GRÁFICO 4: pastel con el porcentaje de participación de cada categoría.
    Las categorías pequeñas se agrupan en 'Otros' si son demasiadas.
    """
    imprimir_titulo("GRÁFICO 4 - COMPARACIÓN CATEGÓRICA")
    indice = seleccionar_columna(datos, "Columna categórica (ej. ciudad, tipo):", False)
    if indice is None:
        return
    nombre_columna = datos["encabezados"][indice]
    conteo, nulos = contar_categorias(obtener_columna(datos, indice))
    if len(conteo) == 0:
        print("  [!] La columna no tiene datos.")
        return
    if len(conteo) == 1:
        print("  [!] La columna tiene una sola categoría: el pastel sería un círculo completo.")
    if datos["tipos"][indice] == "numérica" and len(conteo) > 15:
        print("  [!] La columna es numérica y tiene " + str(len(conteo))
              + " valores distintos; un pastel no será útil.")
        if not pedir_si_no("¿Desea continuar de todos modos?"):
            return

    etiquetas, cantidades = agrupar_otros(conteo, MAX_CATEGORIAS_PASTEL)
    total = len(datos["filas"]) - nulos
    imprimir_subtitulo("Participación por " + nombre_columna)
    for i in range(len(etiquetas)):
        print("  {:<22} {:>8}   {:5.1f} %".format(
            recortar_texto(etiquetas[i], 22), formatear_numero(cantidades[i]),
            porcentaje(cantidades[i], total)))
    print("  Categorías distintas: " + str(len(conteo))
          + "   |   Registros sin dato (excluidos): " + formatear_numero(nulos))

    if not graficos.MATPLOTLIB_DISPONIBLE:
        print("  [!] matplotlib no está instalado: no se puede dibujar el gráfico.")
        return
    nombre = "g4_pie_" + nombre_base(datos) + "_" + nombre_seguro(nombre_columna)
    ruta = graficos.grafico_pastel(etiquetas, cantidades, nombre_columna,
                                   datos["nombre"], nombre)
    print("\n  Gráfico guardado en: " + ruta_relativa(ruta))


def opcion_grafico_correlacion(datos):
    """
    GRÁFICO 5: dispersión entre dos columnas numéricas y su coeficiente de
    correlación de Pearson. Opcionalmente colorea los puntos por categoría.
    """
    imprimir_titulo("GRÁFICO 5 - CORRELACIÓN DE VARIABLES")
    indice_x = seleccionar_columna(datos, "Variable del eje X (numérica):", True)
    if indice_x is None:
        return
    indice_y = seleccionar_columna(datos, "Variable del eje Y (numérica):", True)
    if indice_y is None:
        return
    if indice_y == indice_x:
        print("  [!] Elija dos columnas distintas: una variable contra sí misma siempre da r = 1.")
        return

    xs, ys, filas_usadas, descartadas = pares_numericos(datos, indice_x, indice_y)
    if len(xs) < 2:
        print("  [!] No hay suficientes pares de datos válidos.")
        return
    r = correlacion_pearson(xs, ys)
    interpretacion = interpretar_correlacion(r)

    indice_color = seleccionar_columna(
        datos, "Opcional: columna categórica para colorear los puntos "
        "(0 = todos del mismo color):", False)
    if indice_color is None:
        grupos = [("Todos", xs, ys)]
    else:
        grupos = agrupar_puntos(datos, indice_color, xs, ys, filas_usadas,
                                MAX_CATEGORIAS_DISPERSION)

    nombre_x = datos["encabezados"][indice_x]
    nombre_y = datos["encabezados"][indice_y]
    imprimir_subtitulo(nombre_y + " vs. " + nombre_x)
    print("  Pares válidos: " + formatear_numero(len(xs))
          + "   |   Filas descartadas por nulos: " + formatear_numero(descartadas))
    if r is None:
        print("  Coeficiente de correlación: no se puede calcular (sin variación).")
    else:
        print("  Coeficiente de correlación de Pearson r = " + "{:.3f}".format(r)
              + "  ->  correlación " + interpretacion)
    if len(grupos) > 1:
        for nombre, xs_grupo, _ in grupos:
            print("    " + nombre + ": " + formatear_numero(len(xs_grupo)) + " puntos")

    if not graficos.MATPLOTLIB_DISPONIBLE:
        print("  [!] matplotlib no está instalado: no se puede dibujar el gráfico.")
        return
    nombre = ("g5_scatter_" + nombre_base(datos) + "_" + nombre_seguro(nombre_y)
              + "_vs_" + nombre_seguro(nombre_x))
    ruta = graficos.grafico_dispersion(grupos, nombre_x, nombre_y, r,
                                       interpretacion, datos["nombre"], nombre)
    print("\n  Gráfico guardado en: " + ruta_relativa(ruta))
