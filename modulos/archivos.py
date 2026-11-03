"""
archivos.py
-----------
Todo lo relacionado con el sistema de archivos:
  - Explorar un directorio y listar los .txt y .csv (Opción 1 del menú).
  - Elegir un archivo para analizar.
  - Detectar la codificación y leer el contenido de forma segura.
"""

import os

from modulos.config import EXTENSIONES_VALIDAS
from modulos.utilidades import imprimir_titulo, pedir_texto


def listar_archivos(directorio, extensiones):
    """
    Devuelve una lista de diccionarios con los archivos de 'directorio'
    cuya extensión esté en 'extensiones'. Cada diccionario tiene:
    nombre, ruta, extension y tamano_kb.

    Lanza FileNotFoundError si la ruta no existe y NotADirectoryError
    si la ruta existe pero no es una carpeta.
    """
    if not os.path.exists(directorio):
        raise FileNotFoundError("La ruta '" + directorio + "' no existe.")
    if not os.path.isdir(directorio):
        raise NotADirectoryError("'" + directorio + "' no es una carpeta.")

    archivos = []
    for nombre in sorted(os.listdir(directorio)):
        ruta = os.path.join(directorio, nombre)
        extension = os.path.splitext(nombre)[1].lower()
        if os.path.isfile(ruta) and extension in extensiones:
            archivo = {
                "nombre": nombre,
                "ruta": ruta,
                "extension": extension,
                "tamano_kb": os.path.getsize(ruta) / 1024,
            }
            archivos.append(archivo)
    return archivos


def mostrar_lista_archivos(archivos):
    """Imprime una tabla numerada con nombre, tipo y tamaño de cada archivo."""
    print("\n  N°   Tipo   Tamaño (KB)   Nombre")
    print("  ---  -----  ------------  ------------------------------")
    numero = 1
    for archivo in archivos:
        print("  {:<3}  {:<5}  {:>12,.1f}  {}".format(
            numero, archivo["extension"], archivo["tamano_kb"], archivo["nombre"]))
        numero = numero + 1


def explorar_directorio(directorio_actual):
    """
    OPCIÓN 1 DEL MENÚ PRINCIPAL.
    Pide una ruta al usuario, lista los archivos .txt y .csv que contiene y
    devuelve la ruta explorada para que los submenús la usen por defecto.
    Si la ruta no es válida, informa el error y conserva la ruta anterior.
    """
    imprimir_titulo("EXPLORAR DIRECTORIO")
    ruta = pedir_texto("Ruta a explorar [Enter = " + directorio_actual + "]: ")
    if ruta == "":
        ruta = directorio_actual
    ruta = os.path.abspath(os.path.expanduser(ruta))

    try:
        archivos = listar_archivos(ruta, EXTENSIONES_VALIDAS)
    except (FileNotFoundError, NotADirectoryError) as error:
        print("  [!] " + str(error))
        return directorio_actual
    except PermissionError:
        print("  [!] No tiene permisos para leer la carpeta '" + ruta + "'.")
        return directorio_actual

    if len(archivos) == 0:
        print("\n  La carpeta existe, pero no contiene archivos .txt ni .csv.")
    else:
        total_txt = 0
        total_csv = 0
        for archivo in archivos:
            if archivo["extension"] == ".txt":
                total_txt = total_txt + 1
            else:
                total_csv = total_csv + 1
        print("\n  Carpeta: " + ruta)
        mostrar_lista_archivos(archivos)
        print("\n  Total: " + str(total_txt) + " archivo(s) .txt y "
              + str(total_csv) + " archivo(s) .csv")
    print("\n  Esta carpeta queda seleccionada para las opciones 2 y 3.")
    return ruta


def seleccionar_archivo(directorio, extension):
    """
    Muestra los archivos con 'extension' que hay en 'directorio' y deja que
    el usuario elija uno por número o escriba una ruta completa.
    Devuelve la ruta elegida, o None si el usuario cancela.
    """
    archivos = []
    try:
        archivos = listar_archivos(directorio, (extension,))
    except (FileNotFoundError, NotADirectoryError, PermissionError):
        print("  [!] No se pudo leer la carpeta '" + directorio + "'.")

    if len(archivos) > 0:
        print("\nArchivos " + extension + " en " + directorio + ":")
        mostrar_lista_archivos(archivos)
    else:
        print("\n  No hay archivos " + extension + " en la carpeta actual.")

    print("\n  Escriba el número del archivo, una ruta completa, o 0 para volver.")
    while True:
        respuesta = pedir_texto("Archivo: ")
        if respuesta == "0":
            return None
        if respuesta.isdigit() and 1 <= int(respuesta) <= len(archivos):
            return archivos[int(respuesta) - 1]["ruta"]
        if respuesta == "":
            print("  [!] Escriba una opción.")
            continue

        # El usuario escribió una ruta: se valida antes de aceptarla
        ruta = os.path.abspath(os.path.expanduser(respuesta))
        if not os.path.isfile(ruta):
            print("  [!] El archivo '" + respuesta + "' no existe. Intente de nuevo.")
        elif os.path.splitext(ruta)[1].lower() != extension:
            print("  [!] El archivo debe tener extensión " + extension + ".")
        else:
            return ruta


def detectar_codificacion(ruta):
    """
    Intenta leer el archivo como UTF-8; si falla, usa Latin-1 (ISO-8859-1),
    la codificación típica de archivos antiguos en español.
    'utf-8-sig' también elimina la marca BOM que agregan algunos editores.
    """
    try:
        with open(ruta, "r", encoding="utf-8-sig") as archivo:
            archivo.read()
        return "utf-8-sig"
    except UnicodeDecodeError:
        return "latin-1"


def leer_lineas(ruta):
    """
    Lee un archivo de texto y devuelve (lista_de_lineas, codificacion).
    Las líneas se devuelven sin el salto de línea final.
    Los errores (archivo inexistente, sin permisos) se propagan para que
    la función que llama decida cómo informarlos.
    """
    codificacion = detectar_codificacion(ruta)
    with open(ruta, "r", encoding=codificacion) as archivo:
        contenido = archivo.read()
    return contenido.splitlines(), codificacion
