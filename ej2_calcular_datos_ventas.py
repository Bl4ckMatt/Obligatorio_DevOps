import subprocess
import sys
import os
import re
import argparse
import tensorflow as tf
import numpy as np
import cv2
from tqdm import tqdm

def mostrar_sintaxis():
    print("Descripción resumida de la sintaxis:")
    print("ej2_calcular_datos_ventas.py [-3] [-t] [-e RExp] Archivoalgo.log DirectorioDestino")

parser = argparse.ArgumentParser(description="Descripción del script")
parser.add_argument("-3", action="store_true", help="Descripción del argumento -3")
parser.add_argument("-t", action="store_true", help="Descripción del argumento -t")
parser.add_argument("-e", metavar="RExp", help="Descripción del argumento -e")

parser.add_argument("archivo", help="Descripción del archivo")
parser.add_argument("directorio", help="Descripción del directorio")

args = parser.parse_args()

# Convertir la ruta del archivo a absoluta si es relativa
archivo_absoluto = os.path.abspath(args.archivo)

# Construir la lista de argumentos para el script de Bash
argumentos_bash = ["bash", "./ej1-procesamiento_archivos.sh"]

if args.e:
    contenido = ""
    with open(archivo_absoluto, 'r') as file:
        contenido = file.read()
    
    contenido_filtrado = '\n'.join(re.findall(args.e, contenido))
    
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

    argumentos_bash.append(archivo_tmp)
else:
    # Agregar la ruta del archivo
    argumentos_bash.append(args.archivo)

# Verificar y crear el directorio
if os.path.isabs(args.directorio):
    try:
        os.makedirs(args.directorio, exist_ok=True)
    except OSError as e:
        print(f"Error: No se pudo crear el directorio en la ruta absoluta proporcionada. {e}")
        sys.exit(12)
else:
    directorio_absoluto = os.path.abspath(args.directorio)
    if not os.path.exists(directorio_absoluto):
        print(f"El directorio '{directorio_absoluto}' no existe.")
        print("Creando el directorio en el directorio corriente.")
        os.makedirs(directorio_absoluto, exist_ok=True)

# Agregar -3 y -t solo si se especifican en el script de Python
if args.__dict__["3"]:
    argumentos_bash.append("-3")

if args.__dict__["t"]:
    argumentos_bash.append("-t")

# Ejecutar el script de Bash desde Python con redirección de salida y error
try:
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

# Borrar el archivo temporal si se creó
if args.e:
    try:
        os.remove(archivo_tmp)
    except OSError as e:
        print(f"Error: No se pudo borrar el archivo temporal {archivo_tmp}. {e}")
        sys.exit(12)

# Ejecucion IA
ruta_modelo_ia = "resources/fashion_mnist2.h5"
LABEL_NAMES = ['t_shirt', 'trouser', 'pullover', 'dress', 'coat', 'sandal', 'shirt', 'sneaker', 'bag', 'ankle_boots']
modelo = tf.keras.models.load_model(ruta_modelo_ia)
# modelo_2 = load_model(ruta_modelo_ia)
dir_destino = "./resources/salida/"
os.makedirs(dir_destino, exist_ok=True)

# imagen_seleccionada = "01012022_102901_coat4_[4796.89-0].jpg"
directorio_imagenes = "./resources/imagenes_ventas/"
for imagen_a_ejecutar in tqdm(os.listdir(directorio_imagenes)):
    print(f"leyendo la imagen {imagen_a_ejecutar}")
    imagen_en_memoria = cv2.imread(f"./resources/imagenes_ventas/{imagen_a_ejecutar}", cv2.IMREAD_GRAYSCALE)
    prediccion = modelo.predict(np.expand_dims(imagen_en_memoria, axis=0))
    label = LABEL_NAMES[np.argmax(prediccion)]
    print(f"La clase del objeto de la imagen es {label}")
    os.makedirs(dir_destino + label, exist_ok=True)
    cv2.imwrite(dir_destino + label + "/" + imagen_a_ejecutar, imagen_en_memoria)


sys.exit(resultado.returncode)

