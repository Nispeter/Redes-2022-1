import tqdm
import socket


FORM = "utf-8"
SIZE = 1024
BSIZE = 1024 * 4
S = ' '

def sym_deencr():
    return 'symetrical'
    #COMPLETAR

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
        file_name, file_size,encrypt_opt = head.split(S)  
        client.send(('File size & name received').encode(FORM))

        if (encrypt_opt == 's'): 
            encr_print = sym_deencr()
        if (encrypt_opt == 'o'): encr_print = 'none'

        print("File name received: ", file_name,"\nFile size received: ",file_size,"\nEncryption Option: ",encr_print)
        file_size = int(file_size)

        progress = tqdm.tqdm(range(file_size), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(file_name,"wb") as file:
            while True:
                data = client.recv(BSIZE)
                if not data:    
                    break

                file.write(data)
                progress.update(len(data))
        progress.update(len(data))        
        client.close()
        print(f"Client disconnected - {address[0]}:{address[1]}")
        

if __name__ == "__main__":
    main()