from base64 import b64encode, b64decode
import hashlib
from Crypto.Cipher import AES
import os
from Crypto.Random import get_random_bytes

salt=get_random_bytes(AES.block_size)

print(salt)