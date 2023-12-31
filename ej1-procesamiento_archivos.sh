#!/bin/bash

mostrar_ayuda() {
    echo "Uso: "$0" [-3] [-t] archivo" >&2
    echo "  -3    Verificar la sintaxis de las líneas del archivo" >&2
    echo "  -t    Mostrar el total de ventas" >&2
    echo "  archivo   Archivo que contiene los nombres de las imágenes" >&2
    exit 7
}

# Consultar si la cantidad de argumentos es la correcta
if ! [ $# -eq 1 ] && ! [ $# -eq 2 ] && ! [ $# -eq 3 ]; then
  echo "Cantidad de parámetros incorrecta, solo se reciben los modificadores -3 o -t y un archivo regular accesible." >&2
  exit 4
fi
archivo=""
verificar_sintaxis=false
verificar_error=false
mostrar_incorrectas=false
ventas_realizadas=0
total_resultado=0
lineas_validas=()
lineas_no_validas=()


# Utilizamos este loop para ir argumento por argumento y en base a la coincidencia ejecutar su funcion correspondiente. Si un argumento no esta presente, realiza un chequeo para ver si el mismo es un archivo
while [[ $# -gt 0 ]]; do
    case "$1" in
        -3)
            verificar_sintaxis=true
            ;;
        -t)
            mostrar_incorrectas=true
            ;;
        -h)
	    mostrar_ayuda
	    ;;
     	 *)
            if [[ "$1" != -* ]]; then
               archivo="$1"
            else
                echo "Modificador "$1" inexistente, solo se aceptan -3 y -t, y en ese orden en caso de estar ambos presentes." >&2
                exit 5
            fi
            ;;
	esac
    shift
done

# Buscamos solo por el nombre del archivo en el directorio actual
# Utilizamos basename para extraer solo el nombre del archivo, por lo que si $archivo ya es una ruta absoluta, solo se buscará por el nombre.
absoluta_archivo=$(find "$(pwd)" -name "$(basename "$archivo")" -print -quit 2>/dev/null)

# Si aún no se encuentra, buscamos en todo el sistema
if [ -z "$absoluta_archivo" ]; then
  absoluta_archivo=$(find / -name "$(basename "$archivo")" -print -quit 2>/dev/null)
fi

if [ -n "$absoluta_archivo" ]; then
  # Verificar si el archivo es regular y tiene permisos de lectura
  if [ -f "$absoluta_archivo" ]; then
    echo "Ruta absoluta del archivo: "$absoluta_archivo""
    echo "El archivo es regular"
    if [ -r "$absoluta_archivo" ]; then
      echo "El archivo tiene permisos de lectura."
    else
      echo "No se tienen los permisos necesarios para acceder al archivo "$absoluta_archivo"" >&2
      exit 3
    fi
  else
    echo "El parámetro "$absoluta_archivo" no es un archivo regular válido, sino otro tipo de archivo." >&2
    exit 2
  fi
else
  echo "El archivo "$archivo" no existe, por favor ingrese un archivo regular válido." >&2
  exit 1
fi

# Leemos el archivo, solo las lineas que cumplan con la expresion regular
while read -r linea; do   
	if [[ "$linea" =~ ^imagenes_ventas\/[0-9]{8}_[0-9]{6}_[a-zA-Z0-9_]+\[([0-9]+\.[0-9][0-9]?)?-(0|10|22)\]\.(jpg|jpeg|png)$ ]]; then
 		# Nos quedamos con el segundo "match" de la expresion regular, es decir el precio, para ello utilizamos BASH_REMATCH con el indice 1
		ventas_realizadas=$((ventas_realizadas + 1))  	
		precio=${BASH_REMATCH[1]}
  		# Sumamos los totales y las lineas validas
		total_resultado=$(bc <<< "scale=2; $total_resultado + $precio")
  		if [[ $linea =~ imagenes_ventas\/(.+\.(jpg|png|jpeg)) ]]; then
    			nombre_imagen=${BASH_REMATCH[1]}
       			lineas_validas+=("$nombre_imagen") 
		fi
		
 	fi
done < $absoluta_archivo

# Corresponde al modificador -t
if $mostrar_incorrectas; then
	while read -r linea; do   
		if ! [[ "$linea" =~ ^imagenes_ventas\/[0-9]{8}_[0-9]{6}_[a-zA-Z0-9_]+\[([0-9]+\.[0-9][0-9]?)?-(0|10|22)\]\.(jpg|jpeg|png)$ ]]; then
		        lineas_no_validas+=("$linea") 
    		fi
  	done < $absoluta_archivo
   	echo "Las lineas incorrectas son: "
   	for linea in "${lineas_no_validas[@]}"; do
        	echo "$linea" >&2
 	done
fi

# Corresponde al modificador -3 
if $verificar_sintaxis; then
	ventas_realizadas=0
	while read -r linea; do   
 		if ! [[ "$linea" =~ ^imagenes_ventas\/[0-9]{8}_[0-9]{6}_[a-zA-Z0-9_]+\[([0-9]+\.[0-9][0-9]?)?-(0|10|22)\]\.(jpg|jpeg|png)$ ]]; then
   			verificar_error=true
     			lineas_no_validas+=("$linea") 
		
  		else
    			ventas_realizadas=$((ventas_realizadas + 1))
       		fi
  	done < $absoluta_archivo
fi

# Si hay por lo menos una linea incorrecta, se interrumpe el script
if $verificar_error; then
	echo "El archivo $absoluta_archivo contiene imágenes de ventas incorrectas, por favor ingrese un archivo que contenga solo imágenes correctas o no ingrese el modificador -3 para verificar esa sintaxis. Las líneas que no cumplen con el formato son:" >&2
	for linea in "${lineas_no_validas[@]}"; do
        	echo "$linea" >&2
 	done
	exit 6
fi


if [ $ventas_realizadas = 0 ]; then
	echo "No hay registros de imágenes en el archivo "$absoluta_archivo" pasado como parámetro." >&2
	exit 0
fi

echo "Las lineas correctas son: "
for linea in "${lineas_validas[@]}"; do
	echo "$linea"
done

echo "Se realizaron "$ventas_realizadas" ventas de artículos."
echo "Total: "$total_resultado""

exit 0

