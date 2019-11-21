from Crypto.Cipher import AES

def decode(s):
  obj = AES.new('0123456789101112', AES.MODE_CBC, '0123456789101112')
  st = obj.decrypt(s)
  return st