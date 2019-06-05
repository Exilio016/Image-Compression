from Huffman import Huffman
from Byte import Byte
import imageio
import matplotlib.pyplot as plt
import numpy as np

fft = np.fft.fft2 # The fast fourier transform 
ifft = np.fft.ifft2 # The inverse fast fourier transform
shift = np.fft.fftshift # The shift method to recenter the image
real = np.real # Method to get the real part of an array

def compress(img):
    ft = np.asarray(fft(img))
    #ft = real(ft).astype(int) # can be done with only the real part, but the quality loss is bigger

    huffman = Huffman(ft)
    #print(len(huffman))
    code = huffman.code(ft)

    byte = Byte(code)
    byte.write('./test')
    byte = Byte.read('./test')

    decompress = huffman.decode(Byte.toString(byte.byte), (img.shape))

    return (real(ifft(decompress))).astype(int)

if __name__ == "__main__":
    #imgName = input().rstrip()
    imgName = './img.tiff'
    img = imageio.imread(imgName)
    
    plt.imshow(compress(img))
    plt.show()
