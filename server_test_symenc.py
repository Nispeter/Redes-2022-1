import socket
import hashlib 
from Crypto.Cipher import AES
import tqdm
from Crypto.Util.Padding import unpad

FORM = "utf-8"
SIZE = 1024
BSIZE = 1024 * 4
S = ' '

def main():
    ip = socket.gethostbyname(socket.gethostname())
    port = 2222

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)                #CANTIDAD MAXIMA DE CONEXIONES 
    print("Server is active")

    while True: 
        client, address = server.accept()
        print(f"Connection Established - {address[0]}:{address[1]}")

        head = client.recv(BSIZE).decode()
        file_name, file_size, encrypt_opt = head.split(S)  
        client.send(('File size & name received').encode(FORM))

        
        if (encrypt_opt == 'o'):
            encr_print = 'none'

        print("File name received: ", file_name,"\nFile size received: ",file_size,"\nEncryption Option: ",encr_print)
        file_size = int(file_size)

        progress = tqdm.tqdm(range(file_size), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(file_name,"wb") as file:
            while True:
                data = client.recv(BSIZE)
                if not data:
                    break

                progress.update(len(data))
                file.write(data)

        with open(file_name,"wb") as file:

            if (encrypt_opt == 's'): 
                #with open('py_pass.txt', "rb") as c:
                    #encr_pass = c.read()

                encr_pass = b'mysecretpassword'
                iv = file.read(16)
                all_data = file.read()
                cipher = AES.new(encr_pass, AES.MODE_CBC, iv)
                decrypted_file = unpad(cipher.decrypt(all_data),AES.block_size)
                file.write(decrypted_file.decode())
            
                

        progress.update(len(data))
       
        client.close()
        print(f"Client disconnected - {address[0]}:{address[1]}")
        

if __name__ == "__main__":
    main()