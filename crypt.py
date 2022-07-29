from datetime import datetime
import datetime
from lib2to3.pytree import convert
from Crypto.Cipher  import AES
import base64
import binascii

# 金鑰（key）, 密斯偏移量（iv） CBC模式加密
BLOCK_SIZE = 32  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

vi = '0102030405060708'  # 偏移量

def encrypt(key, data): 
    data = pad(data)
    # 字串補位
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    # 加密後得到的是bytes型別的數據，使用Base64進行編碼,返回byte字串
    encodestrs = base64.b64encode(encryptedbytes)
    # 對byte字串按utf-8進行解碼
    enctext = encodestrs.decode('utf8')

    enctext = str(binascii.hexlify(enctext.encode()))
    enctext = enctext[2:]
    enctext = enctext[:len(enctext)-1]

    return enctext
 
def decrypt(key, data): 
    data = bytes(data,'utf-8')
    data = binascii.unhexlify(data).decode()

    data = data.encode('utf8')
    encodebytes = base64.decodebytes(data)
    # 將加密數據轉換位bytes型別數據
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    text_decrypted = cipher.decrypt(encodebytes)
    # 去補位
    text_decrypted = unpad(text_decrypted)
    text_decrypted = text_decrypted.decode('utf8')

    return text_decrypted

def getTime():
    now = datetime.datetime.now()
    time = str(now.date()) + str('/') + str(now.hour) + str(':') + str(now.minute) + str(':') + str(now.second)
    return time

# key = "wentaiwentaiwentaiwentai"
# time = getTime()

# s1 = encrypt(key, 'ID=U6fa776bf93abd489c81ea1ceaca7a9a0&time='+time)
# print(type(s1))
# print('ID=U6fa776bf93abd489c81ea1ceaca7a9a0&time='+time)
# print(s1)

# print('---------')

# s2 = decrypt(key, s1) 
# print(type(s2))
# print(s2)
