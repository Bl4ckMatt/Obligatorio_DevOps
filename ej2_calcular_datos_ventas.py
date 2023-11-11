import subprocess
import sys

def mostrar_sintaxis():
    print("Descripción resumida de la sintaxis:")
    print("ej2_calcular_datos_ventas.py [-3] [-t] [-e RExp] Archivoalgo.log DirectorioDestino")

# Verificar la cantidad de argumentos, siendo minimo 2 (archivo y directorio) y maximo 5 (se suman -3, -t y -e)
if not (2 <= len(sys.argv) <= 5):
    print("Error: Cantidad incorrecta de argumentos.")
    mostrar_sintaxis()
    sys.exit(20)

# Nos quedamos solo con los argumentos que necesitamos para el script de Bash (-3 y -t)
argumentos_deseados = []
for arg in sys.argv[1:]:
    if arg in ["-3", "-t"]:
        argumentos_deseados.append(arg)

ruta_script_bash = "./ej1-procesamiento_archivos.sh"

# Construir la lista de argumentos para el script de Bash
argumentos_bash = ["bash", ruta_script_bash] + argumentos_deseados

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
