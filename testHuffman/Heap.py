class Heap:
    def __init__(self, Min = True):
        self._li = []
        self._Min = Min
    
    def __str__(self):
        return str(self._li)
    
    def __len__(self):
        return len(self._li)
    
    def __iter__(self):
        self.n = 0
        return self
    
    def __next__(self):
        if self.n < len(self):
            self.n = self.n + 1
            return self._li[self.n-1]
        else:
            raise StopIteration
    
    def __check__(self, aIdx, bIdx):
        if self._Min and (self._li[aIdx])[1] < (self._li[bIdx])[1]:
            return True
        if (not self._Min) and (self._li[aIdx])[1] > (self._li[bIdx])[1]:
            return True
        return False
    
    def __swap__(self, aIdx, bIdx):
        self._li[aIdx], self._li[bIdx] = self._li[bIdx], self._li[aIdx]

    def __fixup__(self):
        lastIdx = len(self)-1
        while lastIdx != 0:
            parentIdx = (lastIdx-1)//2
            if not self.__check__(parentIdx, lastIdx):
                self.__swap__(parentIdx, lastIdx)
                lastIdx = parentIdx
            else:
                lastIdx = 0

    def __biggestChild__(self, idx):
        firstChildIdx = idx*2 + 1
        secondChildIdx = idx*2 + 2
        if firstChildIdx < len(self) and secondChildIdx < len(self):
            return firstChildIdx if self.__check__(firstChildIdx, secondChildIdx) else secondChildIdx
        if firstChildIdx < len(self):
            return firstChildIdx
        return -1

    def __fixdown__(self):
        firstIdx = 0
        while firstIdx < len(self):
            biggest = self.__biggestChild__(firstIdx)
            if biggest != -1 and not self.__check__(firstIdx, biggest):
                self.__swap__(firstIdx, biggest)
                firstIdx = biggest
            else:
                firstIdx = len(self)

    def push(self, val):
        self._li.append(val)
        self.__fixup__()
        return self

    def pop(self):
        val = self._li[0]
        self.__swap__(0, len(self)-1)
        self._li.pop(len(self)-1)
        self.__fixdown__()
        return val
    
    def get(self):
        return self._li[0]