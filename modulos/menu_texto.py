"""
menu_texto.py
-------------
SUBMENÚ 1: Procesamiento de bitácoras / textos reales (.txt).
Aquí está la interacción con el usuario (mostrar resultados y pedir datos).
Los cálculos se hacen en analisis_texto.py y los gráficos en graficos.py.
"""

import os

from modulos import graficos
from modulos.analisis_texto import (cargar_texto, calcular_resumen,
                                    analizar_patrones, contar_errores_http,
                                    buscar_patron, longitudes_de_lineas,
                                    agrupar_longitudes)
from modulos.archivos import seleccionar_archivo
from modulos.config import (RUTA_BASE, TOP_PALABRAS_RESUMEN,
                            TOP_PALABRAS_GRAFICO)
from modulos.utilidades import (imprimir_titulo, imprimir_subtitulo, pausar,
                                pedir_opcion, pedir_texto, pedir_si_no, top_n,
                                formatear_numero, porcentaje, nombre_seguro,
                                recortar_texto)


def abrir_texto(directorio):
    """
    Pide al usuario un archivo .txt y lo carga.
    Devuelve el diccionario con los datos del texto, o None si se canceló o
    hubo un error de lectura.
    """
    ruta = seleccionar_archivo(directorio, ".txt")
    if ruta is None:
        return None
    try:
        datos = cargar_texto(ruta)
    except FileNotFoundError:
        print("  [!] El archivo ya no existe: " + ruta)
        return None
    except PermissionError:
        print("  [!] No tiene permisos para leer: " + ruta)
        return None
    except OSError as error:
        print("  [!] No se pudo leer el archivo: " + str(error))
        return None

    print("\n  Archivo cargado: " + datos["nombre"] + "  ("
          + formatear_numero(len(datos["lineas"])) + " líneas, codificación "
          + datos["codificacion"] + ")")
    if datos["licencia_omitida"]:
        print("  Se detectó un libro del Proyecto Gutenberg: se omitió la "
              "licencia en inglés del inicio y del final.")
    if len(datos["lineas"]) == 0:
        print("  [!] El archivo está vacío.")
    return datos


def mostrar_menu_texto(nombre_archivo):
    """Imprime las opciones del Submenú 1."""
    imprimir_titulo("PROCESAR BITÁCORAS / TEXTOS (.txt)")
    print("  Archivo actual: " + nombre_archivo)
    print("  1. Resumen estadístico del texto")
    print("  2. Extracción de patrones (logs)")
    print("  3. Gráfico 1 - Frecuencia de palabras clave (barras horizontales)")
    print("  4. Gráfico 2 - Distribución de longitud de líneas (histograma)")
    print("  5. Cargar otro archivo .txt")
    print("  6. Volver al menú principal")


def menu_textos(directorio):
    """
    OPCIÓN 2 DEL MENÚ PRINCIPAL.
    Carga un .txt y repite el submenú hasta que el usuario elija volver.
    """
    imprimir_titulo("SELECCIONAR ARCHIVO .txt")
    datos = abrir_texto(directorio)
    if datos is None:
        return

    while True:
        mostrar_menu_texto(datos["nombre"])
        opcion = pedir_opcion("Seleccione una opción: ", 1, 6)
        if opcion == 6:
            return
        try:
            if opcion == 1:
                opcion_resumen_texto(datos)
            elif opcion == 2:
                opcion_patrones(datos)
            elif opcion == 3:
                opcion_grafico_palabras(datos)
            elif opcion == 4:
                opcion_grafico_longitudes(datos)
            elif opcion == 5:
                nuevos = abrir_texto(directorio)
                if nuevos is not None:
                    datos = nuevos
        except EOFError:
            raise
        except Exception as error:
            # Cualquier error inesperado se informa sin cerrar el programa
            print("  [!] Ocurrió un error inesperado: " + str(error))
        pausar()


def opcion_resumen_texto(datos):
    """Muestra líneas, palabras, caracteres y el top 5 de palabras."""
    resumen = calcular_resumen(datos["lineas"])
    conteo = datos["conteo_palabras"]

    imprimir_titulo("RESUMEN ESTADÍSTICO - " + datos["nombre"])
    print("  Total de líneas ...................... "
          + formatear_numero(resumen["total_lineas"]))
    print("     de ellas vacías ................... "
          + formatear_numero(resumen["lineas_vacias"]))
    print("  Total de palabras .................... "
          + formatear_numero(resumen["total_palabras"]))
    print("  Caracteres (con espacios) ............ "
          + formatear_numero(resumen["caracteres_con_espacios"]))
    print("  Caracteres (sin espacios) ............ "
          + formatear_numero(resumen["caracteres_sin_espacios"]))
    print("  Palabras distintas (sin conectores) .. "
          + formatear_numero(len(conteo)))

    imprimir_subtitulo("Top " + str(TOP_PALABRAS_RESUMEN)
                       + " de palabras más repetidas (excluyendo conectores)")
    if len(conteo) == 0:
        print("  No se encontraron palabras.")
        return
    posicion = 1
    for palabra, cantidad in top_n(conteo, TOP_PALABRAS_RESUMEN):
        print("  {}. {:<20} {:>10}".format(posicion, palabra,
                                           formatear_numero(cantidad)))
        posicion = posicion + 1


def imprimir_conteo(diccionario, total, limite):
    """Imprime un conteo {clave: cantidad} con porcentaje, hasta 'limite' filas."""
    mostrados = 0
    for clave in diccionario:
        if mostrados == limite:
            print("  ... y " + str(len(diccionario) - limite) + " más")
            break
        print("  {:<14} {:>10}   ({:5.1f} %)".format(
            clave, formatear_numero(diccionario[clave]),
            porcentaje(diccionario[clave], total)))
        mostrados = mostrados + 1


def opcion_patrones(datos):
    """
    Busca patrones típicos de bitácoras: niveles de severidad (ERROR...),
    códigos HTTP (404, 500...), registros por fecha y palabras de error.
    Al final permite buscar cualquier texto o fecha que el usuario escriba.
    """
    lineas = datos["lineas"]
    patrones = analizar_patrones(lineas)
    total = len(lineas)

    imprimir_titulo("EXTRACCIÓN DE PATRONES - " + datos["nombre"])
    if patrones["es_log"]:
        print("  El archivo SÍ tiene formato de bitácora (log).")
    else:
        print("  El archivo NO parece una bitácora: no se encontraron fechas de log.")
        print("  Solo se mostrarán las palabras clave y la búsqueda libre.")

    niveles = patrones["niveles"]
    if len(niveles) > 0:
        imprimir_subtitulo("Niveles de severidad encontrados")
        imprimir_conteo(niveles, total, 15)

    codigos = patrones["codigos"]
    if len(codigos) > 0:
        total_codigos = 0
        for codigo in codigos:
            total_codigos = total_codigos + codigos[codigo]
        imprimir_subtitulo("Códigos de estado HTTP (de mayor a menor)")
        ordenados = {}
        for codigo, cantidad in top_n(codigos, len(codigos)):
            ordenados[codigo] = cantidad
        imprimir_conteo(ordenados, total_codigos, 15)
        errores_4xx, errores_5xx = contar_errores_http(codigos)
        print("\n  Errores de cliente (4xx): " + formatear_numero(errores_4xx)
              + "   |   Errores de servidor (5xx): " + formatear_numero(errores_5xx))
        if "404" in codigos:
            print("  Páginas no encontradas (404): " + formatear_numero(codigos["404"]))

    fechas = patrones["fechas"]
    if len(fechas) > 0:
        imprimir_subtitulo("Registros por fecha (en orden de aparición)")
        imprimir_conteo(fechas, total, 15)
        fecha_pico, cantidad_pico = top_n(fechas, 1)[0]
        print("\n  Fecha con más registros: " + fecha_pico + " ("
              + formatear_numero(cantidad_pico) + ")")

    imprimir_subtitulo("Líneas que contienen palabras clave de error")
    imprimir_conteo(patrones["palabras_error"], total, 20)

    # Búsqueda libre: se repite hasta que el usuario presione Enter
    imprimir_subtitulo("Búsqueda personalizada")
    while True:
        patron = pedir_texto("Texto o fecha a buscar (ej. 404, ERROR, "
                             "18/May/2015) [Enter = terminar]: ")
        if patron == "":
            break
        cantidad, ejemplos = buscar_patron(lineas, patron)
        print("  '" + patron + "' aparece en " + formatear_numero(cantidad)
              + " línea(s) (" + "{:.2f}".format(porcentaje(cantidad, total))
              + " % del archivo).")
        for numero, texto in ejemplos:
            print("     línea " + str(numero) + ": " + recortar_texto(texto.strip(), 95))


def ruta_relativa(ruta):
    """Muestra la ruta del gráfico relativa a la carpeta del proyecto."""
    return os.path.relpath(ruta, RUTA_BASE)


def opcion_grafico_palabras(datos):
    """GRÁFICO 1: barras horizontales con las 10 palabras más frecuentes."""
    conteo = datos["conteo_palabras"]
    if len(conteo) == 0:
        print("  [!] El archivo no tiene palabras para graficar.")
        return
    pares = top_n(conteo, TOP_PALABRAS_GRAFICO)

    imprimir_titulo("GRÁFICO 1 - FRECUENCIA DE PALABRAS")
    posicion = 1
    for palabra, cantidad in pares:
        print("  {:>2}. {:<20} {:>10}".format(posicion, palabra,
                                              formatear_numero(cantidad)))
        posicion = posicion + 1

    if not graficos.MATPLOTLIB_DISPONIBLE:
        print("  [!] matplotlib no está instalado: no se puede dibujar el gráfico.")
        return
    nombre = "g1_barh_palabras_" + nombre_seguro(os.path.splitext(datos["nombre"])[0])
    ruta = graficos.grafico_barras_palabras(pares, datos["nombre"], nombre)
    print("\n  Gráfico guardado en: " + ruta_relativa(ruta))


def opcion_grafico_longitudes(datos):
    """GRÁFICO 2: histograma de la longitud (en caracteres) de las líneas."""
    lineas = datos["lineas"]
    if len(lineas) == 0:
        print("  [!] El archivo no tiene líneas para graficar.")
        return

    imprimir_titulo("GRÁFICO 2 - LONGITUD DE LÍNEAS")
    incluir_vacias = pedir_si_no("¿Incluir las líneas vacías (0 caracteres)?")
    seleccion = []
    for linea in lineas:
        if incluir_vacias or linea.strip() != "":
            seleccion.append(linea)
    if len(seleccion) == 0:
        print("  [!] No quedan líneas para graficar.")
        return

    longitudes = longitudes_de_lineas(seleccion)
    etiquetas, cantidades, bordes, ajustadas = agrupar_longitudes(longitudes)

    print("\n  Grupo (caracteres)    Líneas      %")
    for i in range(len(etiquetas)):
        print("  {:<18} {:>10}  {:5.1f}".format(
            etiquetas[i], formatear_numero(cantidades[i]),
            porcentaje(cantidades[i], len(longitudes))))

    if not graficos.MATPLOTLIB_DISPONIBLE:
        print("  [!] matplotlib no está instalado: no se puede dibujar el gráfico.")
        return
    nombre = "g2_hist_longitudes_" + nombre_seguro(os.path.splitext(datos["nombre"])[0])
    ruta = graficos.histograma_longitudes(ajustadas, bordes, etiquetas,
                                          datos["nombre"], nombre)
    print("\n  Gráfico guardado en: " + ruta_relativa(ruta))
