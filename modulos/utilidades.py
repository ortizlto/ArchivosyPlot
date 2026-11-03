"""
utilidades.py
-------------
Funciones de apoyo usadas por todo el programa:
entrada de datos validada, impresión de títulos, ordenamiento de conteos
y formato de números.
"""


def imprimir_titulo(texto):
    """Imprime un título enmarcado para separar visualmente cada sección."""
    linea = "=" * (len(texto) + 4)
    print("\n" + linea)
    print("  " + texto)
    print(linea)


def imprimir_subtitulo(texto):
    """Imprime un subtítulo subrayado."""
    print("\n" + texto)
    print("-" * len(texto))


def pausar():
    """Detiene el programa hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")


def pedir_texto(mensaje):
    """Pide un texto al usuario y lo devuelve sin espacios a los lados."""
    return input(mensaje).strip()


def pedir_opcion(mensaje, minimo, maximo):
    """
    Pide un número entero entre 'minimo' y 'maximo' (inclusive).
    Repite la pregunta hasta que la respuesta sea válida.
    """
    while True:
        respuesta = input(mensaje).strip()
        if respuesta.isdigit():
            numero = int(respuesta)
            if minimo <= numero <= maximo:
                return numero
        print("  [!] Opción inválida. Escriba un número entre "
              + str(minimo) + " y " + str(maximo) + ".")


def pedir_entero_opcional(mensaje, minimo, maximo):
    """
    Pide un entero opcional. Si el usuario presiona Enter devuelve None.
    Se usa para parámetros que el usuario puede omitir.
    """
    while True:
        respuesta = input(mensaje).strip()
        if respuesta == "":
            return None
        if respuesta.isdigit():
            numero = int(respuesta)
            if minimo <= numero <= maximo:
                return numero
        print("  [!] Escriba un número entre " + str(minimo) + " y "
              + str(maximo) + ", o presione Enter para omitir.")


def pedir_si_no(mensaje):
    """Pregunta sí/no. Devuelve True para 's' y False para 'n'."""
    while True:
        respuesta = input(mensaje + " (s/n): ").strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("  [!] Responda 's' o 'n'.")


def top_n(conteos, n):
    """
    Devuelve una lista con los 'n' pares (clave, conteo) de mayor conteo,
    ordenados de mayor a menor.

    Se implementa con un algoritmo de selección: en cada vuelta se busca el
    mayor conteo que todavía no se haya elegido. En caso de empate gana la
    clave que apareció primero en el texto.
    """
    resultado = []
    elegidos = set()
    vueltas = min(n, len(conteos))
    for _ in range(vueltas):
        mejor_clave = None
        mejor_conteo = -1
        for clave in conteos:
            if clave not in elegidos and conteos[clave] > mejor_conteo:
                mejor_clave = clave
                mejor_conteo = conteos[clave]
        elegidos.add(mejor_clave)
        resultado.append((mejor_clave, mejor_conteo))
    return resultado


def formatear_numero(valor, decimales=2):
    """
    Da formato a un número: separador de miles y 'decimales' cifras.
    Si el número es entero se muestra sin decimales. Ej: 1234.5 -> '1,234.50'
    """
    if valor == int(valor) and abs(valor) < 1e15:
        return "{:,}".format(int(valor))
    return "{:,.{}f}".format(valor, decimales)


def porcentaje(parte, total):
    """Devuelve el porcentaje que representa 'parte' de 'total' (0 si total es 0)."""
    if total == 0:
        return 0.0
    return parte * 100.0 / total


def nombre_seguro(texto):
    """
    Convierte un texto en un nombre de archivo válido: solo letras, números
    y guiones bajos. Ej: 'temp_max vs. wind' -> 'temp_max_vs_wind'
    """
    resultado = ""
    for caracter in texto.lower():
        if caracter.isalnum():
            resultado = resultado + caracter
        elif resultado != "" and resultado[-1] != "_":
            resultado = resultado + "_"
    resultado = resultado.strip("_")
    if resultado == "":
        resultado = "archivo"
    return resultado[:60]


def recortar_texto(texto, ancho):
    """Recorta 'texto' para que no supere 'ancho' caracteres (agrega '..')."""
    if len(texto) <= ancho:
        return texto
    return texto[:ancho - 2] + ".."
