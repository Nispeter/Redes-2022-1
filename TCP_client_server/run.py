import threading
import time
import os
import subprocess

def call_server():
    os.system("py server_test.py")

def drink_coffee():
    opt = input("symetric encryption (y/n): ")
    if opt == "y":
        opt = 's'
    else:
        opt = 'o'
    os.system(f"py client_test.py -o {opt}")


x = threading.Thread(target=call_server, args=())
x.start()

while x.is_alive():
    time.sleep(1)
    c = input("Send file (y/n): ")
    if c == "n":
        break
    opt = input("symetric encryption (y/n): ")
    if opt == "y":
        opt = 's'
    else:
        opt = 'o'
    subprocess.call(f'py client_test.py -o {opt}', creationflags=subprocess.CREATE_NEW_CONSOLE)

x.join()
