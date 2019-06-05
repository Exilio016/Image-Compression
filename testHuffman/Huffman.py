from Heap import Heap
import math
import numpy as np

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
        __depth__(self, node, code)
        __freqCountArray__(self, img)
    Public:
        code(self, array)
        decode(self, string, out=0)
'''
class Huffman:
    '''
    __init__(self, frequency):
        Class constructor, it creates a heap with the frequency followed by
        the construction of the huffman tree
        Args:
            * frequency: ideally is a dictionary, but can be a string or an array
    '''
    def __init__(self, frequency):
        # if the frequency has a string, a dictionary is created by counting 
        # the number of times that each character appears in the string
        # and assigning it to a dictionary input
        if type(frequency) == str:
            frequency = {val: frequency.count(val) for val in frequency}
        # if the frequency has an array, an auxiliary function is called to
        # create the dictionary, see '__freqCountArray__' for more info
        if type(frequency) == np.ndarray:
            frequency = self.__freqCountArray__(frequency)

        heap = Heap()
        self.huffmanTree = [] # the binary huffman tree
        self.table = {} # the table with every code of every input from de frequency
        self.__size = len(frequency) # the ammount of entries in the frequency dic

        # the frequency must be a dictionary
        if type(frequency) == dict:
            # prepares the heap with initial values
            # this is used so every value in the heap
            # will already have a node inside it
            for i in frequency:
                # the heap will use the first value as a key, and the
                # second value as input for balancing it
                # the third is optional and will be used to store the
                # huffman tree
                # everyting must be inside a tuple: (key, value, node)
                heap.push((i, frequency[i], Node((i, frequency[i]))))
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
            # the __depth__ function is used to create the huffman table with
            # all the values codes
            self.__depth__(self.huffmanTree, '')

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
    __depth__(self, node, code):
        Auxiliary method used to run a depth search on the huffman tree
        and assign a code to each value in the dictionary of frequencies
        Args:
            * node: the node to be analyzed
            * code: string containing the code generated so far to an input
        Note that the first node needs to be the root of the huffman tree,
        and the code must be an empty string
    '''
    def __depth__(self, node, code):
        # if a node has no children, it is a leaf
        # and every leaf contains a dictionary entry
        if not node.left and not node.right:
            # assigns an entry and a value to the tbale dic
            self.table[node.value[0]] = code
        else:
            self.__depth__(node.left, code + '0')
            self.__depth__(node.right, code + '1')

    '''
    __freqCountArray__(self, img):
        Auxiliary function used to create a dictionary of frequencies
        from a given array
        Args:
            * img: array containing values, can be 2d or 3d
        Return value:
            * a dicitonary with the frequency of each value in the array
    '''
    def __freqCountArray__(self, img):
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
                        decoded.append(np.complex(realImg[0], realImg[1]))
                        realImg = []
                    node = self.huffmanTree
            # finally the list is reshaped into the output format
            decoded = np.reshape(decoded, out)
        return decoded

'''
### DEBUG ###
string  = "SUSIE SAYS IT IS EASY"
huf = Huffman(string)
print(huf)
code = huf.code(string)
print(string)
print(code)
print(huf.decode(code))
### DEBUG ###
'''