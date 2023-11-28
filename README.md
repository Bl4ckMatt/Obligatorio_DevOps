# Obligatorio DevOps

Este repositorio cuenta con dos scripts, uno realizado en Bash y otro realizado en Python, los cuales se encargaran de contabilizar la cantidad y totales de ventas realizadas segun un archivo de log.
Ademas se encuenta la opcion de poder realizar chequeos previos de errores sintacticos en dichos archivos e indicar cuales lineas son incorrectas.

## Requisitos

Para ejecutar el script de Python sera necesario instalar algunas dependencias, de forma automatica es posible realizarlo con este comando:

```bash
pip3 install -r requisitos.txt
```

## Dependencias

    subprocess.run
    regex
    argparse
    tensorflow
    numpy
    opencv-python
    tqdm

## Uso

### Script Bash

```bash
ej1-procesamiento_archivos.sh [-3] [-t] archivo
```

- [-3]    Verificar la sintaxis de las líneas del archivo
- [-t]    Desplegara las lineas INCORRECTAS en el archivo
- <archivo>   Archivo que contiene los nombres de las imágenes

### Script Python

```bash
ej2_calcular_datos_ventas.py [-3] [-t] [-e RExp] Archivoalgo.log DirectorioDestino
```
- [-3]    Verifica que el archivo contenga solo ventas CORRECTAS
- [-t]    Desplegara las lineas INCORRECTAS en el archivo
- [-e]    <RExp>   Proporcionar una expresion regular para filtrar el contenido del archivo a analizar
- <archivo>    Archivo log a analizar
- <directorio>   Directorio a utilizar para mover los archivos resultantes
