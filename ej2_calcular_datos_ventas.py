import subprocess
import sys
import os
import re

def mostrar_sintaxis():
    print("Descripción resumida de la sintaxis:")
    print("ej2_calcular_datos_ventas.py [-3] [-t] [-e RExp] Archivoalgo.log DirectorioDestino")

if "-h" in sys.argv:
    mostrar_sintaxis()
    sys.exit(0)

# Verificar la cantidad de argumentos, siendo minimo 2 (archivo y directorio) y maximo 5 (se suman -3, -t y -e)
if not (2 <= len(sys.argv) <= 5):
    print("Error: Cantidad incorrecta de argumentos.")
    mostrar_sintaxis()
    sys.exit(20)

# Crear el directorio si se proporciona y es relativo o no existe
if len(sys.argv) > 2:
    directorio = sys.argv[-1]

    # Verificar si el directorio es una ruta absoluta
    if os.path.isabs(directorio):
        try:
            os.makedirs(directorio, exist_ok=True)
        except OSError as e:
            print(f"Error: No se pudo crear el directorio en la ruta absoluta proporcionada. {e}")
            sys.exit(12)
    else:
        # Convertir el directorio a una ruta absoluta
        directorio_absoluto = os.path.abspath(directorio)

        # Verificar si el directorio existe y si es una ruta relativa
        if not os.path.exists(directorio_absoluto):
            print(f"El directorio '{directorio_absoluto}' no existe.")
            print("Creando el directorio en el directorio corriente.")
            os.makedirs(directorio_absoluto, exist_ok=True)



argumentos_validos = {"-3", "-t", "-e"}

# Verificar que todos los argumentos estén dentro de los parámetros deseados
for arg in sys.argv[1:]:
    if arg not in argumentos_validos:
        print(f"Error: Argumento no válido: {arg}")
        mostrar_sintaxis()
        sys.exit(20)

# Verificamos si se proporciono el argumento -e, y en caso de que si, tomamos la expresion regular que le sigue al parametro.
if "-e" in sys.argv:
    indice_e = sys.argv.index("-e")
    expresion_regular = sys.argv[indice_e + 1]

    try:
        re.compile(expresion_regular)
    except re.error:
        print("Error: La expresión regular proporcionada no es válida.")
        sys.exit(20)



# Nos quedamos solo con los argumentos que necesitamos para el script de Bash (-3 y -t)
argumentos_deseados = []
for arg in sys.argv[1:]:
    if arg in ["-3", "-t"]:
        argumentos_deseados.append(arg)

# Obtener el contenido del archivo y aplicar la expresión regular
if len(sys.argv) > 3:
    archivo = sys.argv[-2]

    # Leer el contenido del archivo
    try:
        with open(archivo, 'r') as file:
            contenido = file.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo}' no existe.")
        sys.exit(20)

    # Aplicar la expresión regular y guardar el contenido filtrado en un archivo temporal en /tmp
    if "-e" in sys.argv:
        contenido_filtrado = '\n'.join(re.findall(expresion_regular, contenido))

        # Obtener el PID del script de Python
        pid_script = os.getpid()

        # Crear el nombre del archivo en /tmp con el PID
        archivo_tmp = f'/tmp/contenido_filtrado_{pid_script}.txt'

        try:
            with open(archivo_tmp, 'w') as file_tmp:
                file_tmp.write(contenido_filtrado)
        except IOError as e:
            print(f"Error: No se pudo crear el archivo en /tmp. {e}")
            sys.exit(12)

ruta_script_bash = "./ej1-procesamiento_archivos.sh"

# Construir la lista de argumentos para el script de Bash
argumentos_bash = ["bash", ruta_script_bash] + argumentos_deseados + [archivo_tmp]

# Ejecutar el script de Bash desde Python con redirección de salida y error
try:
    # Utilizamos stdout=subprocess.PIPE, stderr=subprocess.PIPE para capturar con el output de errores y salida
    resultado = subprocess.run(argumentos_bash, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
except subprocess.CalledProcessError as e:
    # Capturar el objeto de excepción para acceder al código de retorno y los mensajes de error
    codigo_salida = e.returncode
    mensajes_error = e.stderr
    print(f"Error: Código de salida {codigo_salida}")
    print(f"Mensajes de error:\n{mensajes_error}")
    sys.exit(codigo_salida)

# Si no hay errores, imprimir la salida estándar y continuar
salida_estandar = resultado.stdout
print(f"Salida estándar:\n{salida_estandar}")

# Borrar el archivo temporal
try:
    os.remove(archivo_tmp)
except OSError as e:
    print(f"Error: No se pudo borrar el archivo temporal {archivo_tmp}. {e}")
    sys.exit(12)


