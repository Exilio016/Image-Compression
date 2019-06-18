import codecs

'''
The Byte class has a binary representation of an utf-8 string and methods to play around with it
Methods:
    Reserved:
        __init__(self, string = '')
        __str__(self)
        __add__(self, other)
        __len__(self)
    Public:
        write(self, file, mode = 'w')
    Static:
        toBin(string)
        toString(byte)
        read(file)
        binToInt(bin)
        intToBin(int, fill=0)
'''
class Byte:
    '''
    __init_(self, string):
        Class constructor
        Args:
            * string: binary-like array, can be from bytes or str classes
    '''
    def __init__(self, string = ''):
        if type(string) == str:
            self.byte = string.encode('utf8') # if the input is from str class, convert it to bytes
        elif type(string) == bytes:
            self.byte = string
    
    '''
    __str__(self):
        Method called when using the function str()
        Example: print(str(Byte('010100110100111101010011')))
                >>> SOS
        Return value:
            * utf-8 str generated by the binary values
    '''
    def __str__(self):
        string = self.byte.decode('utf8')
        while len(string)%8: # pad the string to be a multiple of 8
            string = string + '0'
        # every 8 bits are converted into a utf-8 character
        # note that int(string[i:i+8], 2) reads a binary number as an integer
        # the chr function returns the utf-8 character of a given int
        return "".join([chr(int(string[i:i+8], 2)) for i in range(0, len(string), 8)]) 
    
    '''
    __add__(self, other):
        Concatenator method, used when trying to concatenate the instance with another thing
        Example: result = Byte('01010011') + Byte('01001111') + Byte('01010011')
                >>> SOS
        Args:
            * other: can be from str, Byte or bytes class
        Return value:
            * the concatenated Byte if the operation can be done, None otherwise
    '''
    def __add__(self, other):
        if type(other) == str:
            return Byte(self.byte + other.encode('utf8'))
        elif type(other) == Byte:
            return self + other.byte
        elif type(other) == bytes:
            return Byte(self.byte + other)
        return None 

    '''
    __len__(self):
        Method called when using the function len()
        Example: len(Byte('010100110100111101010011'))
                >>> 24
        Return value:
            * the length of the binary representation (and not the str one)
    '''
    def __len__(self):
        return len(self.byte)

    '''
    write(self, file, mode = 'w'):
        Writes the utf-8 str to the given file with the given mode
        Args:
            * file: file name that indicates where to write the data
            * mode: mode that indicates how the file must be written, the deafult value is 'w' (it can also be 'a' for append)
            * header: string like variable with lines containing: dimension of the image, shapes of de image (rows, cols, rgb)
            each one in a different line, and the json containing the dict of frequencies
    '''
    def write(self, file, header = '', mode = 'w'):
        with codecs.open(file, mode, "utf-8") as f: # the codecs module is used beacause it can properly represent utf-8 characters in files
            if header:
                f.write(header)
            f.write(str(self))
            f.close()

    '''
    toBin(string):
        Converts an utf-8 str class to a binary represantation in bytes
        Static methods can be called from the class instead of the instance
        Example: Byte.toBin('SOS')
                >>> b'010100110100111101010011'
        Args:
            * string: str with the utf-8 characters
        Return value:
            * binary represantation of the given string in bytes
    '''
    @staticmethod
    def toBin(string):
        # each utf-8 character in the string is converted to binary:
        # the format function converts an int to binary and adds zeros to the left so it can be 8 digits length
        # the ord function is the inverse of the chr, it returns the integer value of an utf-8 character
        # the [2:] is used to remove the '0b' from the binary representation
        # finally the encode('utf-8') casts everything to bytes
        return (''.join([format(ord(x), "#010b")[2:] for x in str(string)])).encode('utf-8')
    
    '''
    toString(byte):
        Converts the bytes class to a str class without transforming it to utf-8 characters
        Static methods can be called from the class instead of the instance
        Example: Byte.toString('010100110100111101010011'.encode('utf-8'))
                >>> '010100110100111101010011'
        Args:
            * byte: bytes to be cast to string
        Return value:
            * str cast of the byte array
    '''
    @staticmethod
    def toString(byte):
        return byte.decode('utf-8')

    '''
    read(file):
        Reads utf-8 characters from the given file and creates a Byte instance
        Static methods can be called from the class instead of the instance
        Args:
            * file: file name of the file to be read
        Return Value:
            * an array with the img shape, binary huffman tree, the size of the longest value and the image
    '''
    @staticmethod
    def read(file):
        string = ''
        shape = []
        tree = []
        with codecs.open(file, "r", "utf-8") as f:
            dim = int(f.readline())
            head = []
            for i in range(dim):
                head.append(int(f.readline()))
            shape = tuple(head)
            longestBin = int(f.readline())
            treeSize = int(f.readline())
            string = f.read()
            tree = Byte(Byte.toBin(string[:treeSize]))
            f.close()
        return shape, tree, longestBin, Byte(Byte.toBin(string[treeSize:]))

    '''
    intToBin(int, fill=0):
        Converts an integer to its binary representation padded with fills 0 to the left
        Args:
            * int: value to be converted to binary
            * fill: the size to pad the binary
        Return value:
            * the string representation of the binary representation of int, with at least size fill
    '''
    @staticmethod
    def intToBin(int, fill=0):
        if int >= 0:
            toBin = '0'
        else:
            toBin = '1'
        toBin += '{:b}'.format(abs(int)).zfill(fill)
        return toBin
    
    '''
    binToInt(bin):
        Converts a binary represantation to an integer
        Args:
            * bin: string with the binary representation
        Return value:
            * integer generated by the convertion of bin
    '''
    @staticmethod
    def binToInt(bin):
        return (1 if bin[0] == '0' else -1) * int(bin[1:], 2)

'''
### DEBUG ###
b = Byte('00101000101010000')
b.write("test.txt")
print(b, b.byte)

a = Byte.read("test.txt")
print(a, a.byte)
### DEBUG ###
'''