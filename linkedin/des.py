from Crypto.Cipher import DES

class MyDESCrypt:
    
    key = chr(11)+chr(11)+chr(11)+chr(11)+chr(11)+chr(11)+chr(11)+chr(11)
    iv = chr(22)+chr(22)+chr(22)+chr(22)+chr(22)+chr(22)+chr(22)+chr(22)
    
    def __init__(self,key='',iv=''):
        if len(key)> 0:
            self.key = key
        if len(iv)>0 :
            self.iv = iv
        
    def ecrypt(self,ecryptText):
       try:
           cipherX = DES.new(self.key, DES.MODE_CBC, self.iv)
           pad = 8 - len(ecryptText) % 8
           padStr = ""
           for i in range(pad):
              padStr = padStr + chr(pad)
           ecryptText = ecryptText + padStr
           x = cipherX.encrypt(ecryptText)
           return x.encode('hex_codec').upper()
       except:
           return ""
      
   
    def decrypt(self,decryptText):
        try:
            
            cipherX = DES.new(self.key, DES.MODE_CBC, self.iv)
            str = decryptText.decode('hex_codec')
            y = cipherX.decrypt(str)
            return y[0:ord(y[len(y)-1])*-1]
        except:
            return ""