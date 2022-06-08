import tqdm
import socket
from Crypto.Cipher import AES 
import os
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

FORM = "utf-8"
SIZE = 1024
BSIZE = 1024 * 4
S = ' '
password = 'sexo'
salt = b'\xe8\xc7BD2\x0e\x12u<\xc9\xee\xa7f\x9cO\xbf'

def key_generation(password, salt):#creamos key en base a una clave y salt
    key = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return key

def sym_deencr(key, original_name, file_name, file_size, chunksize=24*1024, type_encryption = 'symetric'):#encriptamos
    with open(file_name, 'rb') as encrypted:
        if(type_encryption == 'asymetric'):#en caso de asimetrico ignoramos los primeros 256bytes
            encrypted.seek(256)
        iv = encrypted.read(16)#leemos el iv almacenado en el archivo
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(original_name,'wb') as decrypted:#desencriptamos el archivo por chunks
            while True:
                chunk = encrypted.read(chunksize)
                if len(chunk) == 0:
                    break
                decrypted.write(cipher.decrypt(chunk))
            decrypted.truncate(file_size)#eliminamos pading


def asym_deencr(original_name, file_name, file_size):
    #obtenemos clave privada
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )
    #obtenemos clave simetrica encriptada
    with open(file_name, 'rb') as encrypted:
        encrypted_key = encrypted.read(256)

    #desencriptamos clave
    key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    #desencriptamos archivo
    sym_deencr(key,original_name, file_name, file_size, type_encryption = 'asymetric')
    



def main():
    ip = socket.gethostbyname(socket.gethostname())
    port = 2222

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)                #CANTIDAD MAXIMA DE CONEXIONES 
    print("Server is active")

    while True: 
        client, address = server.accept()
        print(f"Connection Established - {address[0]}:{address[1]}")

        head = client.recv(BSIZE).decode()
        file_name, file_size,encrypt_opt = head.split(S)  
        client.send(('File size & name received').encode(FORM))

        if (encrypt_opt == 's'): 
            encr_print = 'sym_deencr'
            original_name = file_name
            file_name = 'encr_' + file_name

        elif(encrypt_opt == 'a'):
            encr_print = 'asym_deencr'
            original_name = file_name
            file_name = 'encr_' + file_name

        if (encrypt_opt == 'o'): encr_print = 'none'

        print("File name received: ", file_name, "\nFile size received: ", file_size,"\nEncryption Option: ", encr_print)
        file_size = int(file_size)

        progress = tqdm.tqdm(range(file_size), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(file_name, "wb") as file:
            while True:
                data = client.recv(BSIZE)
                if not data:    
                    break
                file.write(data)
                progress.update(len(data))

        progress.update(len(data))        
        client.close()
        print(f"Client disconnected - {address[0]}:{address[1]}")
        if (encrypt_opt == 's'):
            key = key_generation(password, salt)
            print("un-encrypting")
            sym_deencr(key, original_name, file_name, file_size)
            os.remove(file_name)
            print("unencrypted")

        elif(encrypt_opt == 'a'):
            print("un-encrypting")
            asym_deencr(original_name, file_name, file_size)
            os.remove(file_name)
            print("unencrypted")

if __name__ == "__main__":
    main()