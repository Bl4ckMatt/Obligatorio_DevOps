#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Uso: $0 [-3] [-t] archivo"
  exit 1
fi

absoluta_archivo=$(find "$(pwd)" -type f -name "$1" -print -quit)

if [ -n "$absoluta_archivo" ]; then
  # Verificar si el archivo tiene permisos de lectura
  if [ -r "$absoluta_archivo" ]; then
    echo "Ruta absoluta del archivo: $absoluta_archivo"
    echo "El archivo tiene permisos de lectura."
  else
    echo "Ruta absoluta del archivo: $absoluta_archivo"
    echo "El archivo no tiene permisos de lectura."
  fi
else
  echo "El archivo no se encontró en la ruta relativa especificada."
fi

