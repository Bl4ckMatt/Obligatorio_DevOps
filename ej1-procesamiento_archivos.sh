#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Uso: $0 [-3] [-t] archivo"
  exit 1
fi

absoluta_archivo=$(find "$(pwd)" -wholename "$1" -print -quit)

if [ -z "$absoluta_archivo" ]; then
  absoluta_archivo=$(find "$(pwd)" -name "$1" -print -quit 2>/dev/null) 
fi

if [ -n "$absoluta_archivo" ]; then
  # Verificar si el archivo es regular y tiene permisos de lectura
  if [ -f "$absoluta_archivo" ]; then
    echo "Ruta absoluta del archivo: $absoluta_archivo"
    echo "El archivo es regular"
    if [ -r "$absoluta_archivo" ]; then
      echo "El archivo tiene permisos de lectura."
    else
      echo "No se tienen los permisos necesarios para acceder al archivo $absoluta_archivo"
      exit 3
    fi
  else
    echo "Ruta absoluta del archivo: $absoluta_archivo"
    echo "El parámetro $absoluta_archivo no es un archivo regular válido, sino otro tipo de archivo."
    exit 2
  fi
else
  echo "El archivo $1 no existe, por favor ingrese un archivo regular válido."
  exit 1
fi

total_ventas=wc -l $absoluta_archivo

echo "El total de ventas es: $total_ventas"
