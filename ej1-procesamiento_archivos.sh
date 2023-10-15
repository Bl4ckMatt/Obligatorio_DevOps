#!/bin/bash

mostrar_ayuda() {
    echo "Uso: $0 [-3] [-t] archivo"
    echo "  -3    Verificar la sintaxis de las líneas del archivo"
    echo "  -t    Mostrar el total de ventas"
    echo "  archivo   Archivo que contiene los nombres de las imágenes"
    exit 1
}

if [ $# -eq 0 ]; then
  echo "Uso: $0 [-3] [-t] archivo"
  exit 1
fi

archivo=""
verificar_sintaxis=false
verificar_error=false
mostrar_total=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -3)
            verificar_sintaxis=true
            ;;
        -t)
            mostrar_total=true
            ;;
        *)
            # Si no es una opción de línea de comandos, asumimos que es el archivo
            archivo="$1"
            ;;
    esac
    shift
done

absoluta_archivo=$(find "$(pwd)" -wholename "$archivo" -print -quit)

if [ -z "$absoluta_archivo" ]; then
  absoluta_archivo=$(find "$(pwd)" -name "$archivo" -print -quit 2>/dev/null) 
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


lineas_no_validas=()

if $verificar_sintaxis; then
  while read -r linea; do
    if [[ "$linea" =~ ^imagenes_ventas/[0-9]{8}_[0-9]{6}_[a-zA-Z0-9_]+\[[0-9]+\.[0-9]{2}-(0|10|22)\]\.(jpg|jpeg|png)$ ]]; then
            ventas_realizadas=$((ventas_realizadas + 1))
    else
            echo "$linea"
	    verificar_error=true
            lineas_no_validas+=("$linea") 
    fi
  done < $absoluta_archivo
fi

if $verificar_error; then
   echo "El archivo $absoluta_archivo contiene imágenes de ventas incorrectas, por favor ingrese un archivo que contenga solo imágenes correctas o no ingrese el modificador -3 para verificar esa sintaxis. Las líneas que no cumplen con el formato son:"

	for linea in "${lineas_no_validas[@]}"; do
        	echo "$linea"
 	done

    exit 1

fi
