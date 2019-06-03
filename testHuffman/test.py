from Huffman import Huffman
from Byte import Byte
import imageio
from PIL import Image
import numpy as np

fft = np.fft.fft # The fast fourier transform 
ifft = np.fft.ifft # The inverse fast fourier transform
shift = np.fft.fftshift # The shift method to recenter the image
real = np.real

def freqCount(img):
    dic = {}
    try:
        height, width = img.shape
    except:
        height, width, depth = img.shape
    try:
        if depth:
            pass
        for x in range(height):
            for y in range(width):
                for z in range(depth):
                    try:
                        dic[img[x, y, z]] = dic[img[x, y, z]] + 1
                    except:
                        dic[img[x, y, z]] = 1
    except:
        for x in range(height):
            for y in range(width):
                try:
                    dic[img[x, y]] = dic[img[x, y]] + 1
                except:
                    dic[img[x, y]] = 1
    return dic

def compress(img):
    ft = np.asarray(fft(img))
    ft = ft.astype(int)
    frequency = freqCount(ft)
    #print(frequency)
    #print(len(frequency), img.shape[0]*img.shape[1]*img.shape[2])
    huffman = Huffman(frequency)
    code = huffman.code(ft)
    byte = Byte(code)
    byte.write('test')
    print(len(byte))
    byte = Byte.read('test')
    read = huffman.decode(byte, (img.shape))
    return (real(ifft(read))).astype(np.uint8)

if __name__ == "__main__":
    #imgName = input().rstrip()
    imgName = 'img'
    img = imageio.imread(imgName)
    
    compressed = Image.fromarray(compress(img))
    compressed.show()