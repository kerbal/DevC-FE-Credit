from Crypto.Cipher import AES

def decode(s):
  obj = AES.new('0123456789101112'.encode('utf8'), AES.MODE_CBC, '0123456789101112'.encode('utf8'))
  st = obj.decrypt(s)
  return st