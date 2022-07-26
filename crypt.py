from datetime import datetime
import datetime
from Crypto.Cipher  import AES
import base64

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
    return enctext
 
def decrypt(key, data): 
    data = data.encode('utf8')
    encodebytes = base64.decodebytes(data)
    # 將加密數據轉換位bytes型別數據
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    text_decrypted = cipher.decrypt(encodebytes)
    # 去補位
    text_decrypted = unpad(text_decrypted)
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted

def getSeconds():
    now = datetime.datetime.now()
    today_begin = datetime.datetime(now.year, now.month , now.day,0,0,0)
    seconds = (now-today_begin).seconds
    seconds = str(now.date())+str('/')+str(seconds)
    return seconds

# key = "wentaiwentaiwentaiwentai"
# time = getSeconds()
# print(type(time))
# s1 = encrypt(key, '?LINE_UUID=U6fa776bf93abd489c81ea1ceaca7a9a0&time='+time) 
# s2 = decrypt(key, 'M548aeQznqJti0TnCPKlZY/dNFIUB4anwaxDNMsjuNdOcPK2GWytEjk+NK3KD1OS51K4vlop403V+2XdPl6Uvw==') 
# print(s1)
# print(s2)