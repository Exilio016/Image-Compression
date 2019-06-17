from Heap import Heap
import math
import numpy as np
from Byte import Byte

'''
The Node class represents each node in a tree
Reserved methods:
    __init__(self, value, left = None, right = None)
    __str__(self)
'''
class Node:
    '''
    __init__(self, value, left = None, right = None):
        Class constructor
        Args:
            * value: the value of the node (usually a tuple)
            * left: the left child of the node (optional arg)
            * right: right child of the node (optional arg)
    '''
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right
    
    '''
    __str__(self):
        str representation of the class
        Return value:
            * the value of the class casted to str
    '''
    def __str__(self):
        return str(self.value)

'''
Huffman implementation for strings and arrays
Methods:
    Reserved:
        __init__(self, frequency)
        __len__(self)
        __str__(self)
    Private:
        __depth(self, node, code)
        __freqCountArray(self, img)
        __longestBin(self):
        __toBin(self, node, code = None, fill = 0):
        __huffmanToByte(self):
    Public:
        code(self, array)
        decode(self, string, out=0)
        write(self, ft, outName):
        read(file):
    Static:
        genTree(string, step = 0):
        huffmanFromByte(obj, step = 0):
'''
class Huffman:
    '''
    __init__(self, frequency):
        Class constructor, it creates a heap with the frequency followed by
        the construction of the huffman tree
        Args:
            * frequency: ideally is a dictionary, but can be a string, an array or the huffman tree (from the Node class)
    '''
    def __init__(self, frequency):
        if type(frequency) == Node:
            # if a node is given it is assumed to be the huffman tree
            self.huffmanTree = frequency
            # the __depth function is used to create the huffman table with
            # all the values codes
            self.table = {} # the table with every code of every input from de frequency
            self.__depth(self.huffmanTree, '')
            self.__size = len(self.table) # the ammount of entries in the frequency dic
        else:
            # if the frequency has a string, a dictionary is created by counting 
            # the number of times that each character appears in the string
            # and assigning it to a dictionary input
            if type(frequency) == str:
                self.frequency = {val: frequency.count(val) for val in frequency}
            # if the frequency has an array, an auxiliary function is called to
            # create the dictionary, see '__freqCountArray' for more info
            if type(frequency) == np.ndarray:
                self.frequency = self.__freqCountArray(frequency)

            if type(frequency) == dict:
                self.frequency = frequency
            heap = Heap()
            self.huffmanTree = [] # the binary huffman tree
            self.table = {} # the table with every code of every input from de frequency
            self.__size = len(self.frequency) # the ammount of entries in the frequency dic

            # the frequency must be a dictionary
            if type(self.frequency) == dict:
                # prepares the heap with initial values
                # this is used so every value in the heap
                # will already have a node inside it
                for i in self.frequency:
                    # the heap will use the first value as a key, and the
                    # second value as input for balancing it
                    # the third is optional and will be used to store the
                    # huffman tree
                    # everyting must be inside a tuple: (key, value, node)
                    heap.push((i, self.frequency[i], Node((i, self.frequency[i]))))
                # the operation keeps going until the heap has only one value
                # this single value will contain the huffman tree inside its third
                # element
                while len(heap) > 1:
                    # the heap is a min heap, so the first removed value
                    # will always be smaller than the second one
                    # this way, the left child will have a smaller value
                    # than the right child
                    (left, right) = heap.pop(), heap.pop()
                    nodeLeft = left[2] # assign the node
                    nodeRight = right[2] # assign the node
                    # finally a new heap entry is created, with the sum of the
                    # values from the left and right child
                    # and its node will be a partent from the left node and the right node
                    # assigned above
                    heap.push(('', left[1]+right[1], Node(('', left[1]+right[1]), nodeLeft, nodeRight)))
                # after finishing the task, the heap can be emptied
                # and the huffman tree taken from the third value of the last tuple
                self.huffmanTree = heap.pop()[2]
                # the __depth function is used to create the huffman table with
                # all the values codes
                self.__depth(self.huffmanTree, '')

    '''
    __len__(self):
        Method called when using the function len()
        Return value:
            * the number of entries in the constructor dic
    '''    
    def __len__(self):
        return self.__size

    '''
    __str__(self):
        Method called when using the function str()
            Return value:
                * string representation of the table of codes
    '''
    def __str__(self):
        return str(self.table)

    '''
    __depth(self, node, code):
        Auxiliary method used to run a depth search on the huffman tree
        and assign a code to each value in the dictionary of frequencies
        Args:
            * node: the node to be analyzed
            * code: string containing the code generated so far to an input
        Note that the first node needs to be the root of the huffman tree,
        and the code must be an empty string
    '''
    def __depth(self, node, code):
        # if a node has no children, it is a leaf
        # and every leaf contains a dictionary entry
        if not node.left and not node.right:
            # assigns an entry and a value to the tbale dic
            self.table[node.value[0]] = code
        else:
            self.__depth(node.left, code + '0')
            self.__depth(node.right, code + '1')

    '''
    __freqCountArray(self, img):
        Auxiliary function used to create a dictionary of frequencies
        from a given array
        Args:
            * img: array containing values, can be 2d or 3d
        Return value:
            * a dicitonary with the frequency of each value in the array
    '''
    def __freqCountArray(self, img):
        dic = {}
        # for 3d arrays
        if len(img.shape) > 2:
            for row in img:
                for col in row:
                    for value in col:
                        real = int(np.real(value))
                        imag = int(np.imag(value))
                        # tries to access the dic entry for the real part:
                        try:
                            dic[real] = dic[real] + 1
                        # if the entry does not exist, creates one:
                        except:
                            dic[real] = 1
                        # tries to access the dic entry for the imaginary part:
                        try:
                            dic[imag] = dic[imag] + 1
                        # if the entry does not exist, creates one:
                        except:
                            dic[imag] = 1
        else:
            # for 2d arrays
            for row in img:
                for value in row:
                    real = int(np.real(value))
                    imag = int(np.imag(value))
                    # tries to access the dic entry for the real part:
                    try:
                        dic[real] = dic[real] + 1
                    # if the entry does not exist, creates one:
                    except:
                        dic[real] = 1
                    # tries to access the dic entry for the imaginary part:
                    try:
                        dic[imag] = dic[imag] + 1
                    # if the entry does not exist, creates one:
                    except:
                        dic[imag] = 1
        return dic

    '''
    code(self, array):
        Function used to create a string containing the coded values
        of each value in the array
        Args:
            * array: can be a str or a 2d/3d array 
        Return value:
            * string containing the code for the entire input
    '''
    def code(self, array):
        coded = ''
        if type(array) == str:
            # if the input is a string, simply add the code of
            # each individual letter to the coded string
            for letter in array:
                coded = coded + self.table[letter]
        else:
            # if the input is an array, adds the code of
            # each value in the array to the coded string
            if len(array.shape) > 2:
                # 3d arrays
                for row in array:
                    for col in row:
                        for value in col:
                            real = int(np.real(value))
                            imag = int(np.imag(value))
                            coded += self.table[real] + self.table[imag]
            else:
                # 2d arrays
                for row in array:
                    for value in row:
                        real = int(np.real(value))
                        imag = int(np.imag(value))
                        coded += self.table[real] + self.table[imag]
        return coded
    
    '''
    decode(self, string, out=0):
        Converts an string to a set of values
        Args:
            * string: contains the binary values to be casted to real values
            * out: the format of the output, 0 for a string, tuple for a ndarray
        Return value:
            * the decoded string/ndarray
    '''
    def decode(self, string, out=0):
        if out == 0:
            decoded = ''
            node = self.huffmanTree
            for letter in string:
                # jumps left and right inside the tree until
                # reaching a leaf
                node = node.left if letter == '0' else node.right
                if node.value[0] != '':
                    # when the leaf is found, its value is appended to
                    # the decoded string and the main node resetted as the root
                    # of the huffman tree
                    decoded = decoded + node.value[0]
                    node = self.huffmanTree
        else:
            decoded = []
            realImg = []
            node = self.huffmanTree
            for letter in string:
                # jumps left and right inside the tree until
                # reaching a leaf
                node = node.left if letter == '0' else node.right
                if node.value[0] != '':
                    # when the leaf is found, its value is appended to
                    # the decoded list and the main node resetted as the root
                    # of the huffman tree
                    realImg.append(node.value[0])
                    if len(realImg) == 2:
                        decoded.append(np.complex(int(realImg[0]), int(realImg[1])))
                        realImg = []
                    node = self.huffmanTree
            # finally the list is reshaped into the output format
            decoded = np.reshape(decoded, out)
        return decoded

    '''
    __longestBin(self):
        Returns the length of the longest binary representation of the values in the frequency dict
    '''
    def __longestBin(self):
        biggest = 0
        for i in self.frequency:
            if biggest < np.abs(i):
                biggest = np.abs(i)
        return len('{:b}'.format(np.abs(biggest))) + 1
    
    '''
    __toBin(self, node, code = None, fill = 0):
        Auxiliary recursive function used to generate the binary representation of the huffman tree
        Args:
            * node: the node being evaluated in this iteracion
            * code: the binary generated so far
            * fill: the pad size of the binary representation of the values 
                (this way every value uses the same size, this makes the reading possible)
        Return value:
            * string with the binary representation of the huffman tree
    '''
    def __toBin(self, node, code = None, fill = 0):
        if code == None:
            code = ''
        if not node.left and not node.right:
            return code + '1' + Byte.intToBin(node.value[0], fill)
        else:
            left = self.__toBin(node.left, code, fill)
            right = self.__toBin(node.right, code, fill)
        return '0' + left + right

    '''
    __huffmanToByte(self):
        Generates a byte representation of the huffman tree
    '''
    def __huffmanToByte(self):
        biggest = self.__longestBin()
        return Byte(self.__toBin(self.huffmanTree, fill=biggest))
    
    '''
    genTree(string, step = 1):
        Rebuilds the huffman tree from a given string
        Args:
            * string: the binary representation of the huffman tree
            * strp: the size of the binary representation of each integer value (in bits)
        Return value:
            * the huffamn tree (from Node class)
    '''
    @staticmethod
    def genTree(string, step = 0):
        if string[0] == '0': # not leaf
            string = string[1:] # consumes the leaf/tree flag
            left, string = Huffman.genTree(string, step) # the string is returned so the current position will always be updated
            right, string = Huffman.genTree(string, step) # the string is returned so the current position will always be updated
            # node = (value = empty, left child, right child)
            return Node([''], left, right), string
        else: # leaf
            string = string[1:] # consumes the leaf/tree flag
            return Node([str(Byte.binToInt(string[:step]))]), string[step:]

    '''
    huffmanFromByte(obj, step = 0):
        Uses the genTree method to create a Huffman class and returns it
        Args:
            * obj: Byte representation of the huffman tree
            * step: the size of the binary representation of each integer value (in bits)
        Return value:
            Huffman class with the values gotten from obj
    '''
    @staticmethod
    def huffmanFromByte(obj, step = 0):
        tree, t = Huffman.genTree(Byte.toString(obj.byte), step+1)
        return Huffman(tree)

    '''
    write(self, ft, outName):
        Writes the binary representation of the ft array coded by the huffman code on the instance
        Args:
            * ft: array representing the image, can be 2d or 3d
            * outName: string withe the name of the output
    '''
    def write(self, ft, outName):
        code = self.code(ft)

        byte = Byte(code)
        # the below code is used to generate the file header
        imgDimension = str(len(ft.shape))+'\n' # the img dimension
        imgShape = ''
        for dim in ft.shape:
            imgShape += str(dim)+'\n' # the size of each dimension
        longestBin = str(self.__longestBin()) + '\n'
        tree = str(self.__huffmanToByte())
        treeSize = str(len(tree)) + '\n'
        
        byte.write(outName, imgDimension+imgShape+longestBin+treeSize+tree) # writes the code with the given header
    
    '''
    read(file):
        Reads the file and converts it to an array (2d or 3d depending on the written options)
        Args:
            * file: string with the name of the file to be read
        Return value:
            * 2d or 3d array representing the image
    '''
    @staticmethod
    def read(file):
        imgShape, tree, longestBin, byte = Byte.read(file) # reads the code and the header

        huffman = Huffman.huffmanFromByte(tree, longestBin)
        return huffman.decode(Byte.toString(byte.byte), imgShape) # decodes it
'''
### DEBUG ###
#string  = "SUSIE_SAYS_IT_IS_EASY"
string = {255: 1, 155: 1, 3: 100, 10: 88, -5: 10}
huf = Huffman(string)
step = huf.longestBin()
print(huf)
#print(huf.__huffmanToByte())
hufByte = huf.__huffmanToByte()
print(hufByte)
print(Huffman.huffmanFromByte(hufByte, step))
print(huf)
code = huf.code(string)
print(string)
print(code)
print(huf.decode(code))
### DEBUG ###
'''