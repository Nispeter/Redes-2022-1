import threading
import time
import os
import subprocess

def call_server():
    os.system("py server_test.py")

def call_client():
    c = input("Send file (y/n): ")
    if c == "n":
        return 1
    opt = input("symetric encryption (y/n): ")
    if opt == "y":
        opt = 's'
    else:
        opt = 'o'
    subprocess.call(f'py client_test.py -o {opt}', creationflags=subprocess.CREATE_NEW_CONSOLE)
    return 0

def run():
    x = threading.Thread(target=call_server, args=())
    x.start()

    while x.is_alive():
        time.sleep(1)
        if call_client():
            print("Closing server")
            time.sleep(1)
            return 

    x.join()

if __name__ == "__main__":
    run()
    
