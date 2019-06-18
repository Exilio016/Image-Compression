'''
Heap implementation for python dictionaries (or labeled data -> tuples)
Methods:
    Reserved:
        __init__(self, array = None, Min = True)
        __str__(self)
        __len__(self)
        __iter__(self)
        __next__(self)
    Private:
        __check__(self, aIdx, bIdx)
        __swap__(self, aIdx, bIdx)
        __fixup__(self)
        __chooseChild__(self, idx)
        __fixdown__(self)
    Public:
        push(self, val)
        pop(self)
        peek(self)
'''
class Heap:
    '''
    __init__(self, array = None, Min = True):
        Class constructor
        Args:
            * array: if an array is given the class will automatically fulfill the heap with its values
            * Min: defines if the heap will be a min (smaller values on top) or a max (bigger values on top) heap
    '''
    def __init__(self, array = None, Min = True):
        self._li = [] # the heap will be a list
        self._Min = Min # _Var makes the Var a protected variable
        if array:
            for value in array:
                self.push(value)
    
    '''
    __str__(self):
        Method called when using the function str()
        Return value:
            * string representation of the heap list
    '''
    def __str__(self):
        return str(self._li)
    
    '''
    __len__(self):
        Method called when using the function len()
        Return value:
            * the length of the heap list
    '''
    def __len__(self):
        return len(self._li)
    
    '''
    __iter__(self):
        Creates an iterator for the class so it can be iterated
        Example: for value in heap: 
                print(value)
    '''
    def __iter__(self):
        self.n = 0
        return self
    
    '''
    __next__(self):
        Method called when using the function next() from the iterator
        Python uses it to loop through the values in an iteration:
        loop:
            stuff
            next()
    '''
    def __next__(self):
        if self.n < len(self):
            self.n = self.n + 1
            return self._li[self.n-1]
        else:
            raise StopIteration
    
    '''
    __check__(self, aIdx, bIdx):
        Auxiliary function, it checks the relation of two values in the heap according to its type (min or max)
        Args:
            * aIdx: index of the first element
            * bIdx: index of the second element
        Return value:
            * boolean that represents if the first value is bigger os smaller than the second

        PS: the code is modularized in a way that if someone wanted to change the input method
        from tuples to single value it is only necessary to change '(self._li[aIdx])[1]' to '(self._li[aIdx])'
        or to the necessary format to attend his/her necessities
    '''
    def __check__(self, aIdx, bIdx):
        # if the heap is a min one, the first value must be smaller than the second
        if self._Min and (self._li[aIdx])[1] < (self._li[bIdx])[1]:
            return True
        # if the heap is a max one, the first value must be bigger than the second
        if (not self._Min) and (self._li[aIdx])[1] > (self._li[bIdx])[1]:
            return True
        return False # everything else is false
    
    '''
    __swap__(self, aIdx, bIdx):
        Auxiliary function, it changes the position between two values in the heap list
        Args:
            * aIdx: index of the first element
            * bIdx: index of the second element
    '''
    def __swap__(self, aIdx, bIdx):
        self._li[aIdx], self._li[bIdx] = self._li[bIdx], self._li[aIdx]

    '''
    __fixup__(self):
        Auxiliary function, it is used to restructure the heap after an insertion
    '''
    def __fixup__(self):
        lastIdx = len(self)-1
        while lastIdx != 0: # until reaching the root
            # note that the way the list is constructed the children of a value 
            # will always be its (index*2)+1 and (index*2)+2
            # that's why to find a parent value we must make the floor divison
            parentIdx = (lastIdx-1)//2
            # the next step will return different values depending on the heap type (min or max)
            if not self.__check__(parentIdx, lastIdx): 
                self.__swap__(parentIdx, lastIdx)
                lastIdx = parentIdx # the next item to be checked must be updated
            else:
                lastIdx = 0 # force stop

    '''
    __chooseChild__(self, idx):
        Auxiliary function, it is used to return the biggest or smallest child of a node
        Args:
            * idx: the index of the parent node
        Return value:
            * the index of the chosen child or -1 to represent an error (the parent has no children)
    '''
    def __chooseChild__(self, idx):
        # [parent, child01, child02, child1 of child01, child2 of child01, child1 of child02, child2 of child02, ...]
        # [0,       1,      2,          3,                  4,                  5,                  6           , ...]
        # 0 -> 1, 2
        # 1 -> 3, 4
        # 2 -> 5, 6
        firstChildIdx = idx*2 + 1
        secondChildIdx = idx*2 + 2
        # childIdx < len(self) is used do ensure that the value exists
        # if childIdx >= len(self) then the parent does not have this child
        if firstChildIdx < len(self) and secondChildIdx < len(self):
            return firstChildIdx if self.__check__(firstChildIdx, secondChildIdx) else secondChildIdx
        # if there is only one child, it will be the smallest/biggest
        if firstChildIdx < len(self):
            return firstChildIdx
        return -1

    '''
    __fixdown__(self):
        Auxiliary function, it is used to restructure the heap after a removal
    '''
    def __fixdown__(self):
        # unlike the fixup function, the fixdown begins from the root and proceeds to a leaf (the biggest or smallest one)
        firstIdx = 0
        while firstIdx < len(self): # only if the index exists
            chosen = self.__chooseChild__(firstIdx) # pick the biggest/smallest child
            # next checks for the error and if the child is bigger os smaller then the parent
            if chosen != -1 and not self.__check__(firstIdx, chosen):
                self.__swap__(firstIdx, chosen)
                firstIdx = chosen # descend the list
            else:
                firstIdx = len(self) # force stop

    '''
    push(self, val):
        Inserts a value to the heap
        Args:
            * val: value to be inserted
    '''
    def push(self, val):
        self._li.append(val) # insert into the end of the list
        self.__fixup__() # restructure the heap
        return self

    '''
    pop(self):
        Removes the first value of the heap
        Return value:
            * The value removed from the top of the heap
    '''
    def pop(self):
        val = self._li[0] # saves the value
        self.__swap__(0, len(self)-1) # switches the first with the last value
        self._li.pop(len(self)-1) # removes the last value
        # the above steps are make to keep the list structure after the removal
        self.__fixdown__() # restructure the heap
        return val
    
    '''
    peek(self):
        Returns the first value of the heap
        Note that unlike the pop function, this will not remove the value from the heap
        Return value:
            * The value from the top of the heap
    '''
    def peek(self):
        return self._li[0]