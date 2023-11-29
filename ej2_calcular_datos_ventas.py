# Para interactuar con el sistema y sus archivos importamos los siguientes modulos
import subprocess
import sys
import os
# Ocultamos las advertencias por drivers y uso del CPU de tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# Para manejos de expresiones regulares importamos el modulo re
import re
# Para manejo de argumentos importamos el modulo argparse
import argparse
# Se importan los siguientes modulos de abajo para la ejecucion de la IA
import tensorflow as tf
import numpy as np
import cv2
from tqdm import tqdm

ruta_modelo_ia = "./resources/fashion_mnist2.h5"
LABEL_NAMES = ['t_shirt', 'trouser', 'pullover', 'dress', 'coat', 'sandal', 'shirt', 'sneaker', 'bag', 'ankle_boots']

def mostrar_sintaxis():
    print("Descripción resumida de la sintaxis:")
    print("ej2_calcular_datos_ventas.py [-3] [-t] [-e RExp] -f,--file Archivoalgo.log -d,--directorio DirectorioDestino")

try:
    # Colocamos un try catch a todo el codigo de abajo y salida con error 20 si ocurre algun error inesperado en el script
    
    # Por defecto argparse, interpreta el argumento -h como la "ayuda" a como se ejecutara el script
    
    parser = argparse.ArgumentParser(description="Script utilizado para calcular cantidad y total de ventas y realizar una clasificacion de imagenes por IA")
    parser.add_argument("-3", action="store_true", help="Verifica que el archivo contenga solo ventas CORRECTAS")
    parser.add_argument("-t", action="store_true", help="Desplegara las lineas INCORRECTAS en el archivo")
    parser.add_argument("-e", metavar="RExp", help="Proporcionar una expresion regular para filtrar el contenido del archivo a analizar")
    
    # El archivo y directorio deben ir en este orden ya que a priori en linea de comandos no se sabe cual es un archivo o directorio, se analizara despues
    parser.add_argument("-f", "--file", help="Archivo log a analizar")
    parser.add_argument("-d", "--directorio", help="Directorio a utilizar para mover los archivos resultantes")
    
    args = parser.parse_args()
    
    # Convertir la ruta del archivo a absoluta si es relativa
    archivo_absoluto = os.path.abspath(args.file)
    
    # Construir la lista de argumentos para el script de Bash
    argumentos_bash = ["bash", "./ej1-procesamiento_archivos.sh"]
    
    # Si contamos con el argumento -e, realizamos el filtrado al archivo con la expresion regular proporcionada
    if args.e:
        contenido = ""
        with open(archivo_absoluto, 'r') as file:
            contenido = file.read()
        # Utilizamos join para unir las lineas filtradas por "contenido", ademas previamente se utiliza split para separar el contenido por lineas
        # Utilizamos re.search para validar que la linea cumple con la expresion proporcionada, si cumple se añade a "contenido_filtrado"
        contenido_filtrado = '\n'.join(linea for linea in contenido.split('\n') if re.search(args.e, linea))
        
        # Obtener el PID del script de Python
        pid_script = os.getpid()
    
        # Crear el nombre del archivo en /tmp con el PID
        archivo_tmp = f'/tmp/contenido_filtrado_{pid_script}.txt'
    
        # Controlamos la excepcion por si no es posible crear el archivo
        try:
            with open(archivo_tmp, 'w') as file_tmp:
                file_tmp.write(contenido_filtrado)
        except IOError as e:
            print(f"Error: No se pudo crear el archivo en /tmp. {e}", file=sys.stderr)
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
            print(f"Error: No se pudo crear el directorio en la ruta absoluta proporcionada. {e}", file=sys.stderr)
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
        print(f"Error: Código de salida {codigo_salida}", file=sys.stderr)
        print(f"Mensajes de error:\n{mensajes_error}", file=sys.stderr)
        sys.exit(codigo_salida)
    
    # Si no hay errores, imprimir la salida estándar y continuar
    salida_estandar = resultado.stdout
    print(f"Salida estándar:\n{salida_estandar}")
    
    # Borrar el archivo temporal si se creó
    if args.e:
        try:
            os.remove(archivo_tmp)
        except OSError as e:
            print(f"Error: No se pudo borrar el archivo temporal {archivo_tmp}. {e}", file=sys.stderr)
            sys.exit(12)
    
    # Ejecucion IA
    modelo = tf.keras.models.load_model(ruta_modelo_ia)
    dir_destino = os.path.abspath(args.directorio)+ "/"
    os.makedirs(dir_destino, exist_ok=True)
    
    # Diccionario para realizar un seguimiento del recuento de cada clase
    recuento_clases = {label: 0 for label in LABEL_NAMES}
    
    directorio_imagenes = "./resources/imagenes_ventas/"
    for imagen_a_ejecutar in tqdm(os.listdir(directorio_imagenes)):
        imagen_en_memoria = cv2.imread(f"./resources/imagenes_ventas/{imagen_a_ejecutar}", cv2.IMREAD_GRAYSCALE)
        prediccion = modelo.predict(np.expand_dims(imagen_en_memoria, axis=0))
        label = LABEL_NAMES[np.argmax(prediccion)]
        # Incrementamos la cantidad de la clase que nos dio la prediccion con su respectiva clave
        recuento_clases[label] += 1
        # Creamos el directorio por cada clase, si ya existe no lo vuelve a crear, y movemos la imagen presente a ese directorio
        os.makedirs(dir_destino + label, exist_ok=True)
        cv2.imwrite(dir_destino + label + "/" + imagen_a_ejecutar, imagen_en_memoria)
    
    # Imprimimos la cantidad de ventas por cada clase, para ello realizamos un for que recorra el diccionario mostrando su clave + valor
    print("Los totales se comportaron de la siguiente manera:")
    for label, count in recuento_clases.items():
        print(f" --> {label} : {count}")
    
    # Salimos del script con el mismo codigo de salida exitoso de bash
    sys.exit(resultado.returncode)
    
except Exception as e:
    print("ERROR: Ocurrio un error inesperado en el script", file=sys.stderr)
    sys.exit(20)
    
