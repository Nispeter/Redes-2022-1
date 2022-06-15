
DESC: 
El run.py funciona para windows 
-para hacer que funcione en linux, cambiar los py por python3
-en caso de variar directorios, modificar la busqueda de las claves de 
	la incriptacion asimetrica
Los scripts UDP adaptados de TCP son server_test.py y client_test.py

LOG ERRORES:
Hay un error en el buffer, el servidor tiene falla al recivir informacion
	por que el sistema se congela con mucho peso.
Posible solucion: hacer que el sistema espere a que se vacie el buffer o
	hasta que se termine de escribir el archivo.