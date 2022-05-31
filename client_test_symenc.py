import socket                       #programacion de sockets duh...
import os                           #preguntas a sistema 
import hashlib 
import tqdm                         #barra de progreso 
import argparse                     #parsear argumentos pal modo de incriptacion 
import tkinter as tk                #cosas de gui
from tkinter import filedialog      
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

#Valores para incriptar, tamaño del buffer de entrada y de envio, separador de string para el envio 
FORM = "utf-8"
SIZE = 1024
BSIZE = 1024 * 4
S = ' '

def main(encrypt_opt):
    #CONEXION TPC 
    
    ip = socket.gethostbyname(socket.gethostname())
    port = 2222

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip,port))

    #IDENTIFICACION DE DATOS
    root = tk.Tk()                                  #Obtener root
    root.withdraw()
    filepath = filedialog.askopenfilename()         #Seleccion de archivo de forma fansy 
    file_name = os.path.basename(filepath)
    file_size = os.path.getsize(filepath)

     #MODO DE INCRIPTACION
    if(encrypt_opt == 's'):
        #encr_pass = bytes(input("Enter password: ") ,FORM)
        #with open('py_pass.txt', "wb") as p:
            #p.write(encr_pass)
        encr_pass = b'mysecretpassword'
        cipher = AES.new(encr_pass, AES.MODE_CBC)
        with open(filepath, "rb") as f:
            orig_file = f.read()
            padded_file = pad(orig_file,AES.block_size)    
            encrypted_message = cipher.iv + cipher.encrypt(padded_file)
            file_size = len(encrypted_message)
            
    
    #FORMATO DE ENVIO: "nombre_del_archivo 'S' tamaño_del_archivo 'S' forma_de_incriptacion "
    print(f"{file_name}{S}{file_size}{S}{encrypt_opt}")
    server.send(f"{file_name}{S}{file_size}{S}{encrypt_opt}".encode(FORM))
    msg = server.recv(SIZE).decode(FORM)
    print(msg)

    progress = tqdm.tqdm(range(file_size), 
                         f"Sending {file_name}", 
                         unit="B", unit_scale=True, 
                         unit_divisor=1024) #actualizacion de la barra de progreso 

    with open(filepath, "rb") as file:
        while True:
            if(encrypt_opt == 's'):
                data = encrypted_message(BSIZE)  
            else: 
                data = file.read(BSIZE)                 #se envian los datos un buffer a la vez
            if not data:
                break

            server.sendall(data)
            progress.update(len(data))
    
    server.close()

#para generar archivos grandes en linux bash:
# time sh -c 'dd if=/dev/zero iflag=count_bytes count=10G bs=1M of=large; sync'

#para ejecutar el codigo puedes hacer 
# py client_test.py    , para ejecutar sin sifrado
# py client_test.py -o , para ejecutar sin sifrado
# py client_test.py -o s, para sifrar simetricamente 

if __name__ == "__main__":
    par = argparse.ArgumentParser(description="TPC client test")
    par.add_argument("-o",help="Mode of encryption",default = "o")
    arg = par.parse_args()
    encrypt_opt = arg.o
    main(encrypt_opt)
