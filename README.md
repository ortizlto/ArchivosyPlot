# Analizador de Datos Reales (CLI)

Aplicación de consola interactiva, escrita en Python, para explorar, resumir y graficar archivos reales: textos y bitácoras (`.txt`) y conjuntos de datos abiertos (`.csv`). Todo el código está en un solo archivo: `main_minimal.py`.

Se construyó solo con la biblioteca estándar de Python: no usa NumPy, Pandas ni expresiones regulares (`re`). La única dependencia externa es matplotlib, y es opcional: si no está instalada, el programa funciona igual y simplemente omite los gráficos.

Explicacion del código (Video): https://teams.microsoft.com/l/meetingrecap?driveId=b%21hZWxN5v8AkiPXjc1PnXnuAhT5qDByatOo-T_Z21OqfkfKg9BAM8BRYJV-M8ltQnW&driveItemId=01VOZYFMN22LCDWQXYLZGKHZKW6NE7C6ZZ&sitePath=https%3A%2F%2Fupbeduco-my.sharepoint.com%2F%3Av%3A%2Fg%2Fpersonal%2Fjeronimo_ortizg_upb_edu_co%2FIQC60sQ7QvheTKPlVvNJ8Xs5AX-grGZZGqTpNmID26B3kIo&fileUrl=https%3A%2F%2Fupbeduco-my.sharepoint.com%2F%3Av%3A%2Fg%2Fpersonal%2Fjeronimo_ortizg_upb_edu_co%2FIQC60sQ7QvheTKPlVvNJ8Xs5AX-grGZZGqTpNmID26B3kIo&threadId=19%3A0b9e04e3-9ed6-4943-82fa-24bde53df32c_20b0493d-deb1-4975-aacf-17045fa17276%40unq.gbl.spaces&callId=22e26c5c-be19-4164-9f64-204041675e7e&threadType=OneOnOneChat&meetingType=Unknown&subType=RecapSharingLink_RecapChiclet&recapType=Recording

## Contenido

1. [Qué hace](#qué-hace)
2. [Requisitos](#requisitos)
3. [Estructura de carpetas](#estructura-de-carpetas)
4. [Menús del programa](#menús-del-programa)
5. [Gráficos generados](#gráficos-generados)
6. [Mapa de llamadas](#mapa-de-llamadas)
7. [Referencia de funciones](#referencia-de-funciones)
8. [Constantes de configuración](#constantes-de-configuración)
9. [Diagramas de flujo](Diagramas-de-flujo)

## Qué hace

Explorar carpetas: lista los archivos `.txt` y `.csv` de cualquier directorio.

Textos y bitácoras (`.txt`): resumen estadístico, detección automática de bitácoras (logs), extracción de patrones (niveles de severidad, códigos HTTP, fechas, palabras de error y patrones literarios), búsqueda personalizada y dos gráficos.

Datos abiertos (`.csv`): vista previa, estadísticas descriptivas de cualquier columna numérica y tres gráficos (tendencia, participación por categoría y correlación).

## Requisitos

Python 3.7 o superior.

[matplotlib](https://matplotlib.org/) (opcional, solo para los gráficos):

```bash
pip install matplotlib
```

## Estructura de carpetas

```text
.
├── main_minimal.py
├── data/        # archivos .txt y .csv a analizar (carpeta de trabajo por defecto)
└── outputs/     # gráficos .png generados (el programa la crea si no existe)
```

La carpeta `data/` debe existir (el programa no la crea). Desde el menú también es posible explorar otra carpeta o escribir la ruta completa de un archivo.

## Menús del programa

```text
Menú principal
├── 1. Explorar directorio
├── 2. Procesar bitácoras / textos reales (.txt)
│   ├── 1. Resumen estadístico del texto
│   ├── 2. Extracción de patrones (logs y literarios)
│   ├── 3. Gráfico 1 - Palabras frecuentes
│   ├── 4. Gráfico 2 - Longitud de líneas
│   ├── 5. Cargar otro .txt
│   └── 6. Volver al menú principal
├── 3. Analizar dataset de datos abiertos (.csv)
│   ├── 1. Vista previa de datos
│   ├── 2. Estadísticas descriptivas de una columna
│   ├── 3. Gráfico 3 - Tendencia / líneas
│   ├── 4. Gráfico 4 - Comparación categórica / pastel
│   ├── 5. Gráfico 5 - Correlación / dispersión
│   ├── 6. Cargar otro .csv
│   └── 7. Volver al menú principal
└── 4. Salir
```

## Gráficos generados

Todos los gráficos se guardan como PNG (150 dpi) en `outputs/`. Si el entorno es interactivo, además se abren en una ventana que hay que cerrar para continuar.

| N.º | Gráfico | Dónde se genera | Archivo de salida |
|---|---|---|---|
| 1 | Barras horizontales con las 10 palabras más frecuentes | Textos → opción 3 | `g1_barh_palabras_<archivo>.png` |
| 2 | Histograma de la longitud de las líneas | Textos → opción 4 | `g2_hist_longitudes_<archivo>.png` |
| 3 | Líneas: tendencia de una columna numérica según otra (con promedio móvil opcional) | CSV → opción 3 | `g3_plot_<archivo>_<y>_por_<x>.png` |
| 4 | Pastel con la participación por categoría | CSV → opción 4 | `g4_pie_<archivo>_<columna>.png` |
| 5 | Dispersión entre dos columnas numéricas, con coeficiente de Pearson | CSV → opción 5 | `g5_scatter_<archivo>_<y>_vs_<x>.png` |

Los textos entre `<>` (nombre del archivo y de las columnas) se limpian con `nombre_seguro()`.

## Mapa de llamadas

La flecha `←` significa «usa». Las funciones auxiliares como `pedir_*`, `imprimir_*`, `formatear_numero` o `porcentaje` aparecen en casi todos los pasos y no se repiten aquí.

```text
main()
├── explorar_directorio()            ← listar_archivos(), mostrar_lista_archivos()
├── menu_textos()
│   ├── seleccionar_archivo()        ← listar_archivos(), mostrar_lista_archivos()
│   ├── cargar_texto()               ← leer_contenido()
│   ├── opcion_resumen_texto()       ← calcular_resumen(), top_n()
│   ├── opcion_patrones()            ← analizar_patrones(), buscar_patron(), imprimir_conteo()
│                                      (analizar_patrones usa extraer_fecha_log, extraer_nivel_log y extraer_codigo_http)
│   ├── opcion_grafico_palabras()    ← top_n(), grafico_barras_palabras()
│   └── opcion_grafico_longitudes()  ← agrupar_longitudes(), histograma_longitudes()
└── menu_csv()
    ├── seleccionar_archivo()        ← listar_archivos(), mostrar_lista_archivos()
    ├── cargar_csv()                 ← leer_contenido(), parse_csv(), es_nulo(), to_num()
    ├── opcion_vista_previa()        ← imprimir_tabla()
    ├── opcion_estadisticas()        ← seleccionar_columna(), to_num(), stats()
    ├── opcion_grafico_tendencia()   ← seleccionar_columna(), promedio_movil(), grafico_lineas()
    ├── opcion_grafico_categorias()  ← seleccionar_columna(), agrupar_otros(), grafico_pastel()
    └── opcion_grafico_correlacion() ← seleccionar_columna(), pares_numericos(), pearson(),
                                       interpretar_correlacion(), agrupar_puntos(), grafico_dispersion()
```

Todas las funciones `grafico_*` e `histograma_longitudes` se apoyan en `crear_figura()`, `poner_titulos()` y `guardar_y_mostrar()`.

## Referencia de funciones

Las secciones siguen el mismo orden que el código. Los prefijos de los nombres indican el papel de cada función:

| Prefijo | Papel |
|---|---|
| `pedir_*` | Leen y validan lo que escribe el usuario. |
| `imprimir_*`, `mostrar_*` | Muestran información en consola. |
| `cargar_*` | Leen un archivo y devuelven un diccionario `datos` listo para analizar. |
| `extraer_*` | Sacan un dato puntual de una línea de texto. |
| `grafico_*`, `histograma_*` | Construyen y guardan una figura de matplotlib. |
| `opcion_*` | Acciones de los menús: piden datos al usuario, llaman a las funciones de cálculo y de gráfico, y muestran el resultado. |
| `menu_*` | Submenús en bucle (textos y CSV). |

### Utilidades de consola

| Función | Qué hace | Devuelve |
|---|---|---|
| `imprimir_titulo(t)` | Imprime `t` encerrado entre dos líneas de `=`. Es el encabezado de cada pantalla. | `None` |
| `imprimir_subtitulo(t)` | Imprime `t` subrayado con guiones. Separa secciones dentro de un reporte. | `None` |
| `pausar()` | Espera a que se presione Enter, para dar tiempo de leer el resultado antes de volver al menú. | `None` |
| `pedir_texto(msg)` | Muestra `msg`, lee una línea y le quita los espacios sobrantes de los extremos. | `str` |
| `pedir_opcion(msg, mini, maxi)` | Pide un número entero entre `mini` y `maxi`. Si lo escrito no es válido, avisa y vuelve a preguntar. | `int` |
| `pedir_entero_opcional(msg, mini, maxi)` | Igual que `pedir_opcion`, pero la respuesta es opcional: con Enter vacío devuelve `None`. | `int` o `None` |
| `pedir_si_no(msg)` | Hace una pregunta de sí/no. Acepta `s`, `si`, `sí`, `n` y `no` (sin distinguir mayúsculas) y repite hasta recibir una respuesta válida. | `bool` |
| `top_n(conteos, n)` | Ordena un diccionario `{clave: cantidad}` de mayor a menor cantidad y devuelve las `n` primeras parejas. | `list` de `(clave, cantidad)` |
| `formatear_numero(v, dec=2)` | Da formato a un número con separador de miles. Los enteros salen sin decimales (`1,234`) y el resto con `dec` decimales (`1,234.57`). | `str` |
| `porcentaje(p, total)` | Calcula qué porcentaje es `p` de `total`. Si `total` es 0 devuelve `0.0` en lugar de fallar. | `float` |
| `recortar_texto(t, w)` | Acorta `t` para que no pase de `w` caracteres, terminándolo en `..` cuando lo corta. | `str` |
| `ruta_relativa(r)` | Convierte una ruta en relativa a la carpeta del script, para mostrar mensajes más cortos. | `str` |
| `nombre_seguro(texto)` | Convierte un texto en un nombre de archivo válido: minúsculas, todo lo que no sea letra o número pasa a `_`, sin guiones bajos repetidos ni en los extremos y con un máximo de 60 caracteres. Si no queda nada, devuelve `"archivo"`. | `str` |
| `imprimir_conteo(dic, total, limite=15)` | Imprime un diccionario de conteos como tabla: nombre, cantidad y porcentaje sobre `total`. Muestra hasta `limite` filas y avisa cuántas quedaron fuera (`... y N más`). | `None` |

### Archivos

| Función | Qué hace | Devuelve |
|---|---|---|
| `listar_archivos(d, exts)` | Busca en la carpeta `d` los archivos cuya extensión esté en `exts` y los devuelve ordenados por nombre. De cada uno entrega `nombre`, `ruta`, `extension` y `tamano_kb`. Lanza `FileNotFoundError` si la ruta no existe y `NotADirectoryError` si no es una carpeta. | `list` de `dict` |
| `mostrar_lista_archivos(archivos)` | Imprime la lista como tabla numerada (N.º, tipo, tamaño en KB y nombre). El número sirve después para elegir el archivo. | `None` |
| `explorar_directorio(actual)` | Opción 1 del menú principal. Pide una ruta (Enter = la carpeta actual), la convierte en ruta absoluta y lista los `.txt` y `.csv` que contiene, con el total de cada tipo. Si la ruta no existe o no es una carpeta, muestra el error y deja la carpeta de trabajo como estaba. | `str`: la carpeta de trabajo resultante |
| `seleccionar_archivo(d, ext)` | Lista los archivos de extensión `ext` en la carpeta `d` y deja elegir uno escribiendo su número o una ruta completa (`0` para volver). Valida que el archivo exista y que tenga la extensión pedida. | `str` (ruta) o `None` si se cancela |
| `leer_contenido(ruta)` | Lee un archivo de texto completo probando primero UTF-8 (tolera el BOM) y, si falla, Latin-1. | `(texto, codificación)` |

### Textos y patrones (sin `re`)

| Función | Qué hace | Devuelve |
|---|---|---|
| `cargar_texto(ruta)` | Lee un `.txt` y lo deja listo para analizar. Si es un libro de Project Gutenberg, descarta el encabezado y el pie de licencia (lo que queda fuera de las marcas `*** START OF` y `*** END OF`). Después cuenta la frecuencia de cada palabra: pasa a minúsculas, quita puntuación y dígitos de los extremos e ignora las palabras vacías (conectores, artículos…) y los fragmentos sin letras. El diccionario devuelto tiene `nombre`, `ruta`, `lineas`, `codificacion`, `licencia_omitida` y `conteo_palabras`. | `dict` |
| `calcular_resumen(lines)` | Calcula las métricas básicas de una lista de líneas: `total_lineas`, `lineas_vacias`, `total_palabras`, `caracteres_con_espacios`, `caracteres_sin_espacios` y `promedio_caracteres_linea` (dividido entre las líneas no vacías). | `dict` |
| `extraer_fecha_log(l)` | Intenta sacar la fecha de una línea de bitácora. Reconoce tres formas: ISO al inicio de la línea (`2024-03-15`), la de Apache/Nginx entre corchetes (`[10/Oct/2023:13:55:36 -0500]` → `10/Oct/2023`) y la del log de errores de Apache (`[Thu Oct 10 13:55:36 2023]` → `10/Oct/2023`). | `str` (fecha) o `""` |
| `extraer_codigo_http(l)` | Obtiene el código de estado HTTP de una línea de log de acceso: toma lo que sigue a la petición entre comillas (`"GET /index.html HTTP/1.1" 200 512`) y comprueba que sean exactamente 3 dígitos. | `str` (por ejemplo `"404"`) o `""` |
| `extraer_nivel_log(l)` | Busca un nivel de severidad (`ERROR`, `WARN`, `INFO`, `DEBUG`, `CRITICAL`…) entre las primeras 6 palabras de la línea, ignorando corchetes, paréntesis y dos puntos pegados. | `str` en mayúsculas o `""` |
| `analizar_patrones(lines)` | Es el análisis principal del modo texto. Primero decide si el archivo es una bitácora: lo es si al menos la mitad de las primeras 200 líneas no vacías trae una fecha reconocible. Siempre cuenta en cuántas líneas aparece cada palabra clave de error. Si es bitácora, cuenta niveles de severidad, códigos HTTP y registros por fecha; si no, busca patrones literarios: encabezados de capítulo, títulos en mayúsculas, signos `¿`, `¡` y `«`, y años de 4 cifras (entre 1000 y 2099). Devuelve las claves `es_log`, `palabras_error`, `niveles`, `codigos`, `fechas`, `literarios` y `anios` (también disponible como `años`). | `dict` |
| `buscar_patron(lines, patron, max_ej=3)` | Busca `patron` sin distinguir mayúsculas de minúsculas. Cuenta en cuántas líneas aparece y devuelve hasta `max_ej` ejemplos con su número de línea. | `(cantidad, [(n.º de línea, texto), …])` |
| `agrupar_longitudes(longitudes)` | Reparte las longitudes de línea en intervalos de 50 caracteres (`0-50`, `51-100`, …), con un máximo de 12. Las líneas más largas que el último intervalo se acumulan en él, que pasa a rotularse `551+`. | `(etiquetas, cantidades, bordes, longitudes_ajustadas)` |

### CSV y estadísticas (sin NumPy)

| Función | Qué hace | Devuelve |
|---|---|---|
| `parse_csv(text, sep)` | Analizador de CSV hecho a mano. Recorre el texto carácter por carácter y respeta los campos entre comillas (que pueden contener el separador o saltos de línea), las comillas escapadas (`""`) y los finales de línea `\r\n`. | `list` de filas (cada fila, una `list` de `str`) |
| `to_num(val)` | Convierte un texto en `float` de forma tolerante. Devuelve `None` si el valor es nulo o no es un número. Quita los espacios internos y entiende `1.234,56` y `1,234.56` (si hay punto y coma, el último es el decimal); si hay una sola coma, la toma como decimal. | `float` o `None` |
| `es_nulo(t)` | Indica si `t` está vacío o es un marcador de dato faltante (`NA`, `N/A`, `NaN`, `null`, `-`, `sin dato`…), sin distinguir mayúsculas. | `bool` |
| `cargar_csv(ruta)` | Carga y prepara un `.csv`. Detecta el separador (coma, punto y coma, tabulador o barra vertical: el más frecuente en la primera línea), lo interpreta con `parse_csv`, nombra `columna_N` a las columnas sin encabezado, descarta las filas completamente vacías y ajusta cada fila al número de columnas. También detecta el tipo de cada columna: `numérica` (al menos 90 % de sus valores no nulos son números), `texto` o `vacía`. Lanza `ValueError` si el archivo está vacío o solo tiene encabezados. El diccionario devuelto tiene `nombre`, `ruta`, `encabezados`, `filas`, `delimitador`, `codificacion` y `tipos`. | `dict` |
| `stats(nums)` | Calcula estadísticas descriptivas de una lista de números: `validos`, `promedio`, `mediana`, `maximo` y `minimo`. | `dict`, o `None` si la lista está vacía |
| `pearson(xs, ys)` | Calcula el coeficiente de correlación de Pearson (r, entre −1 y 1) entre dos listas de igual largo. | `float`, o `None` si hay menos de 2 pares o una variable no varía |
| `interpretar_correlacion(r)` | Traduce `r` a texto según su valor absoluto: desde 0.7 es fuerte, desde 0.4 moderada, desde 0.2 débil y por debajo prácticamente nula. Desde 0.2 agrega el sentido (positiva o negativa). Si `r` es `None`, responde `"no se puede calcular"`. | `str` |
| `promedio_movil(ys, k)` | Calcula el promedio móvil simple con ventana de `k` datos. Usa una suma acumulada, así no recalcula toda la ventana en cada paso. El resultado tiene `len(ys) - k + 1` valores. | `list` de `float` |

### Gráficos (matplotlib)

| Función | Qué hace | Devuelve |
|---|---|---|
| `crear_figura(w, h)` | Crea una figura de `w × h` pulgadas con el estilo común de todos los gráficos: fondo claro, sin bordes superior y derecho, ejes y marcas en tonos suaves y cuadrícula detrás de los datos. | `(fig, ax)` |
| `poner_titulos(ax, tit, sub, xl, yl)` | Pone el título (a la izquierda y en negrita), un subtítulo pequeño debajo (archivo de origen y datos de apoyo) y los nombres de los ejes X e Y. | `None` |
| `guardar_y_mostrar(fig, nombre)` | Cierra el ciclo de todo gráfico: crea `outputs/` si no existe, guarda la figura como `nombre.png` (150 dpi), la muestra en una ventana si el entorno es interactivo (pide cerrarla para continuar) y libera la figura. | `str` (ruta del PNG) |
| `grafico_barras_palabras(pares, fuente, nombre)` | Gráfico 1. Barras horizontales con las palabras más frecuentes (`pares` es una lista de `(palabra, cantidad)`): la más frecuente arriba y el valor al final de cada barra. | `str` |
| `histograma_longitudes(longitudes, bordes, etiq, fuente, nombre)` | Gráfico 2. Histograma de la longitud de las líneas, con los intervalos de `agrupar_longitudes` y, sobre cada barra, la cantidad de líneas y su porcentaje. | `str` |
| `grafico_lineas(xs, ys, x_es_texto, nom_x, nom_y, fuente, nombre, ventana, movil)` | Gráfico 3. Línea de `ys` según `xs`. Si se pidió promedio móvil, dibuja los datos originales atenuados y encima el promedio móvil, con leyenda. Con X numérica y hasta 15 puntos marca cada punto; con X de texto muestra solo unas 10 etiquetas inclinadas para no saturar el eje. | `str` |
| `grafico_pastel(etiq, cant, col_nom, fuente, nombre)` | Gráfico 4. Pastel con la participación de cada categoría. Escribe el porcentaje en las porciones de 4 % o más, pinta «Otros» en gris y agrega una leyenda con cantidad y porcentaje. | `str` |
| `grafico_dispersion(grupos, nom_x, nom_y, r, interp, fuente, nombre)` | Gráfico 5. Dispersión de `y` contra `x`. Cada grupo `(nombre, xs, ys)` va con su color y entra en la leyenda si hay más de uno. El título muestra `r` y su interpretación, y los puntos se achican si hay más de 800. | `str` |

### Submenú 1: textos (`.txt`)

| Función | Qué hace | Devuelve |
|---|---|---|
| `opcion_resumen_texto(datos)` | Opción 1. Imprime el resumen estadístico del texto (líneas, líneas vacías, palabras, caracteres con y sin espacios, promedio por línea y palabras distintas) y el top 5 de palabras más repetidas, sin conectores. | `None` |
| `opcion_patrones(datos)` | Opción 2. Ejecuta `analizar_patrones` y presenta el reporte: si es bitácora o texto literario, niveles de severidad, códigos HTTP (con los totales de errores 4xx y 5xx y de 404), registros por fecha, patrones literarios (capítulos, títulos, preguntas, exclamaciones, citas y años más mencionados) y líneas con palabras clave de error. Termina con un buscador interactivo (`buscar_patron`) que se repite hasta que se presiona Enter sin escribir nada. | `None` |
| `opcion_grafico_palabras(datos)` | Opción 3. Muestra en consola las 10 palabras más frecuentes y genera el Gráfico 1. Si no hay palabras o matplotlib no está instalado, avisa y omite el gráfico. | `None` |
| `opcion_grafico_longitudes(datos)` | Opción 4. Pregunta si se incluyen las líneas vacías, agrupa las longitudes con `agrupar_longitudes`, imprime la tabla de intervalos con su porcentaje y genera el Gráfico 2. | `None` |

### Submenú 2: CSV (`.csv`)

| Función | Qué hace | Devuelve |
|---|---|---|
| `imprimir_tabla(hdrs, filas, nums)` | Dibuja en consola una tabla con los encabezados, una columna con el número de fila (`nums`) y las filas indicadas. Cada columna mide entre 3 y 14 caracteres (`ANCHO_CELDA`): lo que no cabe se recorta con `..` y los saltos de línea dentro de una celda se reemplazan por espacios. | `None` |
| `seleccionar_columna(datos, mensaje, solo_num)` | Muestra las columnas del dataset con su tipo (solo las numéricas si `solo_num` es `True`) y pide elegir una por número o por nombre; `0` cancela. Repite hasta recibir una opción válida. | `int` (índice) o `None` si se cancela o no hay columnas elegibles |
| `opcion_vista_previa(datos)` | Opción 1. Muestra el número de registros y de columnas, el separador, la codificación, la lista de columnas con su tipo detectado y las primeras 10 y últimas 5 filas (o todas, si son 15 o menos). | `None` |
| `opcion_estadisticas(datos)` | Opción 2. Pide una columna numérica, convierte sus valores con `to_num`, descarta los nulos y muestra registros totales, nulos eliminados, válidos, promedio, mediana, máximo y mínimo (`stats`). | `None` |
| `opcion_grafico_tendencia(datos)` | Opción 3. Pide una columna para X (fecha, año, categoría…) y una numérica para Y. Si hay valores de X repetidos, pregunta si combinar Y con promedio o con suma. Ordena X cuando es numérica (si es texto, respeta el orden de aparición). Con 6 puntos o más ofrece un promedio móvil opcional. Imprime el primer y el último punto y genera el Gráfico 3. Requiere al menos 2 valores distintos de X. | `None` |
| `agrupar_otros(conteo, maximo)` | Deja las `maximo` categorías más frecuentes y suma todas las demás en «Otros». Si fuera a sobrar una sola categoría (hay `maximo + 1` o menos), no agrupa nada. | `(etiquetas, cantidades)` |
| `opcion_grafico_categorias(datos)` | Opción 4. Pide una columna, cuenta cuántas veces aparece cada valor (sin contar nulos), advierte si es numérica con más de 15 valores distintos, agrupa con `agrupar_otros` (máximo 7 categorías), imprime la tabla de participación y genera el Gráfico 4. | `None` |
| `pares_numericos(datos, idx_x, idx_y)` | Recorre el dataset y se queda con las filas donde las dos columnas indicadas (por su índice) tienen un número válido. | `(xs, ys, filas_usadas, descartadas)` |
| `agrupar_puntos(datos, idx_c, xs, ys, filas, maximo)` | Reparte los puntos de la dispersión según una columna categórica, para colorearlos. Conserva las `maximo` categorías más frecuentes (3) y manda el resto a «Otros»; los valores nulos van a «Sin dato». | `list` de `(grupo, xs, ys)` |
| `opcion_grafico_correlacion(datos)` | Opción 5. Pide dos columnas numéricas distintas, arma los pares válidos (`pares_numericos`), calcula Pearson (`pearson`) y su interpretación, ofrece una columna categórica opcional para colorear (`agrupar_puntos`), imprime el resumen y genera el Gráfico 5. | `None` |

### Controladores de menú y punto de entrada

| Función | Qué hace | Devuelve |
|---|---|---|
| `menu_textos(dir_actual)` | Submenú de `.txt` (opción 2 del menú principal). Pide el archivo (`seleccionar_archivo`), lo carga (`cargar_texto`) y avisa si omitió la licencia de Gutenberg. Luego muestra un menú en bucle: resumen, patrones, gráfico 1, gráfico 2, cargar otro `.txt` o volver. Cada opción corre dentro de un `try/except`, así que un error no cierra el programa, y al terminar llama a `pausar()`. | `None` |
| `menu_csv(dir_actual)` | Lo mismo para `.csv` (opción 3 del menú principal): selecciona y carga el archivo con `cargar_csv` y ofrece vista previa, estadísticas, gráficos 3, 4 y 5, cargar otro `.csv` o volver. | `None` |
| `main()` | Punto de entrada. Guarda la carpeta de trabajo (por defecto `data/`) y muestra el menú principal en bucle: explorar directorio, procesar textos, analizar CSV o salir. | `None` |

Al final del archivo, el bloque `if __name__ == "__main__":` ejecuta `main()` y captura `Ctrl+C` y el fin de la entrada (`KeyboardInterrupt`, `EOFError`) para cerrar con un mensaje en vez de mostrar un error.

## Constantes de configuración

Definidas al inicio de `main_minimal.py`; cambiar su valor ajusta el comportamiento sin tocar las funciones.

| Constante | Valor | Para qué sirve |
|---|---|---|
| `RUTA_BASE` | Carpeta del script | Base para construir las demás rutas y para mostrar rutas relativas (`ruta_relativa`). |
| `RUTA_DATOS` | `data/` junto al script | Carpeta de trabajo por defecto. |
| `RUTA_SALIDAS` | `outputs/` junto al script | Destino de los gráficos. |
| `EXTENSIONES_VALIDAS` | `.txt`, `.csv` | Extensiones que lista `explorar_directorio`. |
| `TOP_RESUMEN` | `5` | Palabras del top en el resumen estadístico. |
| `TOP_GRAFICO` | `10` | Palabras del Gráfico 1. |
| `ANCHO_INT` | `50` | Ancho, en caracteres, de cada intervalo del histograma de longitudes. |
| `MAX_INT` | `12` | Máximo de intervalos del histograma (el último acumula las líneas más largas). |
| `FILAS_INI`, `FILAS_FIN` | `10`, `5` | Filas iniciales y finales de la vista previa del CSV. |
| `ANCHO_CELDA` | `14` | Ancho máximo de cada columna al imprimir tablas. |
| `MAX_PASTEL` | `7` | Categorías que se muestran en el pastel antes de agrupar el resto en «Otros». |
| `MAX_DISP` | `3` | Categorías con color propio en la dispersión antes de agrupar el resto en «Otros». |
| `MAX_ETIQ_X` | `10` | Cantidad aproximada de etiquetas en el eje X cuando es texto. |
| `VALORES_NULOS` | `""`, `na`, `n/a`, `nan`, `null`, `none`, `-`, `--`, `?`, `sin dato`, `nd`, `s/d` | Textos tratados como dato faltante. |
| `NIVELES_LOG` | `emerg`, `alert`, `crit`, `critical`, `fatal`, `error`, `warn`, `warning`, `notice`, `info`, `debug`, `trace` | Niveles de severidad que reconoce `extraer_nivel_log`. |
| `PALABRAS_ERROR` | `error`, `fail`, `fatal`, `denied`, `exception`, `timeout`, `warn` | Palabras clave que `analizar_patrones` busca en cada línea. |
| `MESES` | `Jan` … `Dec` | Abreviaturas de mes en inglés para reconocer las fechas de Apache. |
| `SIGNOS_PUNTUACION` | Puntuación, comillas, símbolos y dígitos | Caracteres que se recortan de los extremos de cada palabra al contarlas. |
| `PALABRAS_VACIAS` | Conectores, artículos, preposiciones y pronombres en español e inglés | Palabras que no entran en el conteo de frecuencias. |
| `COLORES`, `C_*` | Paleta de colores | Estilo común de todos los gráficos. |
| `MATPLOTLIB_DISPONIBLE` | `True` o `False` | Indica si matplotlib se pudo importar; si es `False`, se omiten los gráficos. |

## Diagramas de Flujo
Link: https://canva.link/3ykv3j2l6stmukd
