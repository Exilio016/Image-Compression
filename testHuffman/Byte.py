import codecs

class Byte:
    def __init__(self, string = ''):
        if type(string) == str:
            self.byte = string.encode('utf8')
        elif type(string) == bytes:
            self.byte = string
    
    def __str__(self):
        string = self.byte.decode('utf8')
        while len(string)%8:
            string = string + '0'
        return "".join([chr(int(string[i:i+8], 2)) for i in range(0, len(string), 8)])
    
    def __add__(self, other):
        if type(other) == str:
            return Byte(self.byte + other.encode('utf8'))
        elif type(other) == Byte:
            return self + other.byte
        elif type(other) == bytes:
            return Byte(self.byte + other)
        return None

    def __len__(self):
        return len(str(self))

    def write(self, file, mode = 'w'):
        with codecs.open(file, mode, "utf-8") as f:
            f.write(str(self))
            f.close()

    @staticmethod
    def toByte(string):
        return (''.join([format(ord(x), "#010b")[2:] for x in str(string)])).encode('utf-8')
    
    @staticmethod
    def read(file):
        string = ''
        with codecs.open(file, "r", "utf-8") as f:
            string = f.read()
            f.close()
        return Byte(Byte.toByte(string))

'''b = Byte('00101000101010000')
b.write("test.txt")
print(b, b.byte)

a = Byte.read("test.txt")
print(a, a.byte)
'''