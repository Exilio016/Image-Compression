import imageio
import numpy as np 
import sys
import getopt
import struct
from scipy.fftpack import fftn, ifftn, fftshift
from matplotlib.pyplot import imshow, show

def compress(image, threshold):
  fft_img = fftn(image) #Apply FFT to the original image
  threshold = 0.1 * threshold * np.amax(np.abs(fft_img)) #With a given threshold, find the value that inferior numbers will be cut of the fft_image
  comp_fft_img = np.where(np.abs(fft_img) > threshold, fft_img, 0) #Numbers less than the threshold will be turn to 0
  return comp_fft_img #Return the compressed FFT image

def int2byte(num, signed=True):
  return num.to_bytes(4, byteorder='big', signed=signed) 

def byte2int(fourBytes, signed=True):
  return int.from_bytes(fourBytes, byteorder='big', signed=signed)

def float2byte(num):
  return struct.pack('<f',num)

def byte2float(eigthBytes):
  return struct.unpack('<f', eigthBytes)[0]

def image_save(compressed_image, file):
  x, y ,z = compressed_image.shape
  file.write(int2byte(x, signed=False))
  file.write(int2byte(y, signed=False))
  file.write(int2byte(z, signed=False))

  for i in range(x):
    for j in range(y):
      for k in range(z):
        if compressed_image[i][j][k] != 0:
          file.write(int2byte(i))
          file.write(int2byte(j))
          file.write(int2byte(k))
          real = np.real(compressed_image[i][j][k])
          imag = np.imag(compressed_image[i][j][k])
          file.write(float2byte(real))
          file.write(float2byte(imag))
          
def read_bin(filename):
  file = open(filename, 'rb')
  x = byte2int(file.read(4), signed=False)
  y = byte2int(file.read(4), signed=False)
  z = byte2int(file.read(4), signed=False)
  fft_image = np.zeros((x, y, z), np.complex)

  while True:
    aux = file.read(4)
    if not aux:
      break

    i = byte2int(aux)
    j = byte2int(file.read(4))
    k = byte2int(file.read(4))
    real = byte2float(file.read(4))
    imag = byte2float(file.read(4))
    fft_image[i][j][k] = np.complex(real, imag)

  file.close()

  return fft_image

def decompress(fft_image):
  image = np.real(ifftn(fft_image))
  return normalize(image, 255).astype(np.uint8)

def normalize(matrix, normal):    
    maxi = np.max(matrix)
    mini = np.min(matrix)

    matrix_norm = np.subtract(matrix, mini)
    return np.multiply(matrix_norm, (normal/(maxi - mini)))

def print_help(progname):
  print('Usage: '+ progname + ' [OPTIONS]\n')
  print('Options:')
  print('-h\t\t\tthis help screen')
  print('-c <INPUTFILE>\t\tcompress the <INPUTFILE> image')
  print('-o <OUTPUTFILE>\t\toutput file for the compression')
  print('-d <INPUTFILE>\t\tdecompress the <INPUTFILE> image')
  print('-t <THRESHOLD>\t\tthreshold for the FFT compression, default value is 0.0001')
  sys.exit(0)

if __name__ == "__main__":
  progname = sys.argv[0]
  opts, args = getopt.getopt(sys.argv[1:], 'hc:o:d:t:')
  inputFile = None
  outputFile = None
  isCompress = False
  isDecompress = False
  threshold = 0.0001
  np.set_printoptions(threshold=sys.maxsize)

  for opt, arg in opts:
    if(opt == '-c'):
      inputFile = imageio.imread(arg)
      isCompress = True
    elif(opt == '-t'):
      threshold = float(arg)
    elif(opt == '-o'):
      outputFile = open(arg, 'wb')
    elif(opt == '-d'):
      inputFile = read_bin(arg)
      isDecompress = True
    elif(opt == '-h'):
      print_help(progname)

  if isCompress:
    if outputFile is None:
      print('Output file is not defined! Did you use -o <outputfile> ?')
      sys.exit(1)
    if isDecompress:
      print('The options -c and -d cannot be used in the same time. Is not possible compress and decompress in the same execution!')
      sys.exit(1)

    c = compress(inputFile, threshold)
    imageio.imsave('uncompress.jpg', inputFile)
    imageio.imwrite('compress.jpg', decompress(c))
    #image_save(c, outputFile)
    outputFile.close()

  elif isDecompress:
    image = decompress(inputFile)
