from Heap import Heap
import math
import numpy as np

class Node:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right
    
    def __str__(self):
        return str(self.value)

class Huffman:
    def __init__(self, frequency):
        if type(frequency) == str:
            frequency = {val: frequency.count(val) for val in frequency}
        heap = Heap()
        self.huffmanTree = []
        self.table = {}
        self.__size = len(frequency)
        if type(frequency) == dict:
            for i in frequency:
                heap.push((i, frequency[i], Node((i, frequency[i]))))
            while len(heap) > 1:
                (left, right) = heap.pop(), heap.pop()
                nodeLeft = left[2]
                nodeRight = right[2]
                heap.push(('', left[1]+right[1], Node(('', left[1]+right[1]), nodeLeft, nodeRight)))
                self.__size += 1
            self.huffmanTree = heap.pop()[2]
            self.__depth__(self.huffmanTree, '')
    
    def __len__(self):
        return self.__size

    def __str__(self):
        li = [self.huffmanTree]
        string = ''
        count = 0
        breaker = 0
        level = int(math.log2(len(self))) + 1
        while len(li) > 0:
            val = li.pop(0)
            count += 1
            if (math.log2(count)).is_integer():
                level -= 1
                string += '\n'
            for i in range(level):
                string += '\t'
            if val is not None:
                breaker += 1
                string += str(val.value)
                li.append(val.left)
                li.append(val.right)
                for i in range(level):
                    string += '\t'
            else:
                string += '_ '
                li.append(None)
                li.append(None)
            if breaker == len(self):
                break
        while not (math.log2(count)).is_integer():
            count += 1
            string += '_ '
        return string

    def __depth__(self, node, code):
        if not node.left and not node.right:
            self.table[node.value[0]] = code
        else:
            self.__depth__(node.left, code + '0')
            self.__depth__(node.right, code + '1')

    def code(self, array):
        coded = ''
        if type(array) == str:
            for letter in array:
                coded = coded + self.table[letter]
        else:
            try:
                height, width = array.shape
            except:
                height, width, depth = array.shape
            try:
                if depth:
                    pass
                for x in range(height):
                    for y in range(width):
                        for z in range(depth):
                            coded += self.table[array[x, y, z]]
            except:
                for x in range(height):
                    for y in range(width):
                        coded += self.table[array[x, y]]
        return coded
    
    def decode(self, array, out=0):
        if out == 0:
            node = self.huffmanTree
            decoded = ''
            for letter in array:
                node = node.left if letter == '0' else node.right
                if node.value[0]:
                    decoded = decoded + node.value[0]
                    node = self.huffmanTree
        else:
            print(out)
            try:
                height, width, depth = out[0], out[1], out[2]
            except:
                height, width = out[0], out[1]
            try:
                if depth:
                    pass
                decoded = np.zeros(out)
                index = 0
                array = str(array)
                leng = []
                print(len(array))
                for x in range(height):
                    for y in range(width):
                        for z in range(depth):
                            node = self.huffmanTree
                            value = None
                            while not value:
                                if index >= len(array):
                                    break
                                node = node.left if array[index] == '0' else node.right
                                if node.value[0]:
                                    value = node.value[0]
                                    leng.append(value)
                                    print(value)
                                index += 1
                                if not index%200000:
                                    print(index, len(leng))

                            decoded[x, y, z] = value
            except:
                decoded = np.zeros(out)
                index = 0
                array = str(array)
                for x in range(height):
                    for y in range(width):
                        node = self.huffmanTree
                        value = None
                        while not value:
                            node = node.left if array[index] == '0' else node.right
                            if node.value[0]:
                                value = node.value[0]
                            index += 1
                        decoded[x, y] = value
        return decoded

'''string  = "SUSIE SAYS IT IS EASY"
huf = Huffman(string)
print(huf)
code = huf.code(string)
print(string)
print(code)
print(huf.decode(code))'''