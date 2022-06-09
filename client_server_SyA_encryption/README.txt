Existen  2 formas

La más complicada consiste en 
Ejecutar el servidor:	py server_test.py
Ejecutar el cliente con incriptacion simetrica: py client_test.py -o s	
Ejecutar el cliente con incriptacion asimetrica: py client_test.py -o a	
Ejecutar el cliente: py client_test.py -o o 

La segunda es simplemente correr el ejecutable run.exe
El cual ejecuta el cliente y el servidor de forma simultánea.

Observación:
En caso de fallo del .exe, realizar un 
pyinstaller --onefile run.py 
se crearan 2 carpetas nuevas, build y dist
luego mover el run.exe desde la carpeta dist al mismo nivel que run.py
