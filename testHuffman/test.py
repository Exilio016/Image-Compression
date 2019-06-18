from Huffman import Huffman
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os

fft = np.fft.fft2 # The fast fourier transform 
ifft = np.fft.ifft2 # The inverse fast fourier transform
shift = np.fft.fftshift # The shift method to recenter the image
real = np.real # Method to get the real part of an array

'''
normalize(matrix, normal):
    Normalizes a given 2d array with the given normal factor
    Args:
        * matrix - 2 dimentional array to be normalized
        * normal - max value to be used as reference, the min value will be set as 0
    Return value:
        * normalized 2d array
'''
def normalize(img, normal = 255):
    max = np.amax(img)
    min = np.amin(img)
    dif = max - min
    img = np.uint8((img - min) * (normal / dif))
    return img

def decompress(file):
    decompress = Huffman.read(file)
    return normalize((real(ifft(decompress))).astype(int))


def compress(imgName, outName):
    img = imageio.imread(imgName)
    ft = np.asarray(fft(img))
    # image stuff
    huffman = Huffman(ft) # must generate the huffamn code first
    huffman.write(ft, outName) # then encode it and write to a file

if __name__ == "__main__":
    #imgName = input().rstrip()
    imgName = 'img.tiff'
    compress(imgName, 'test')    
    plt.imshow(decompress('test')) 
    plt.show()