import imageio
import numpy as np 
import sys
import getopt
import struct
from scipy.fftpack import fftn, ifftn, fftshift
from PIL import Image
def compress(image, threshold):
  fft_img = fftn(image) #Apply FFT to the original image
  threshold = 0.1 * threshold * np.amax(np.abs(fft_img)) #Calculate the threashold
  comp_fft_img = np.where(np.abs(fft_img) > threshold, fft_img, 0) #Values below the threshold will be turn to 0
  return comp_fft_img #Return the compressed FFT image

def int2byte(num, signed=True, size=4):
  return num.to_bytes(size, byteorder='big', signed=signed) #Convert an integer to bytes

def byte2int(fourBytes, signed=True):
  return int.from_bytes(fourBytes, byteorder='big', signed=signed) #Convert bytes to integer

def float2byte(num):
  return struct.pack('<f',num) #Convert float to bytes

def byte2float(fourBytes):
  return struct.unpack('<f', fourBytes)[0] #Convert bytes to float

def image_save(compressed_image, file):
  #If the image is black and white we need to reshape that to a 3D Matrix
  if len(compressed_image.shape) == 2:
    x, y = compressed_image.shape
    compressed_image = compressed_image.reshape((x, y, 1))

  x, y ,z = compressed_image.shape #Get image size

  #Save image size
  file.write(int2byte(x, signed=False))
  file.write(int2byte(y, signed=False))
  file.write(int2byte(z, signed=False))

  #Save image
  for i in range(x):
    for j in range(y):
      for k in range(z):
        #If the value is not 0, it is saved 
        if compressed_image[i][j][k] != 0:
          file.write(int2byte(1, size=1)) #Flag to say that exist a value in this position
          real = np.real(compressed_image[i][j][k]) #Get the real part 
          imag = np.imag(compressed_image[i][j][k]) #Get the imaginary part
          file.write(float2byte(real)) #Save the real part
          file.write(float2byte(imag)) #Save the imaginary part

        else:
          file.write(int2byte(0, size=1)) #Flag to say that in this position the value is 0

          
def read_bin(filename):
  file = open(filename, 'rb') #Open file

  #Read image size
  x = byte2int(file.read(4), signed=False)
  y = byte2int(file.read(4), signed=False)
  z = byte2int(file.read(4), signed=False)

  fft_image = np.zeros((x, y, z), np.complex) #Allocate image on the memory

  #Read all image
  for i in range(x):
    for j in range(y):
      for k in range(z):
        flag = byte2int(file.read(1)) # Read the flag

        if(flag == 1):
          real = byte2float(file.read(4)) #Read the real part
          imag = byte2float(file.read(4)) #Read the imaginary part
          fft_image[i][j][k] = np.complex(real, imag) #Save in the image the complex number

  file.close() #Close the file

  #If Z is 1, the image is black and white then we need to reshape to an 2D Matrix
  if z == 1:
    fft_image = fft_image.reshape((x, y))

  return fft_image

def decompress(fft_image):
  image = np.real(ifftn(fft_image)) #Apply the Inverse FFT in the fft_image
  return normalize(image, 255).astype(np.uint8) #Normalize and return the decompressed image

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
  progname = sys.argv[0] #Get the program name
  opts, args = getopt.getopt(sys.argv[1:], 'hc:o:d:t:') #Get program options

  #Set default options, and auxiliar variables
  inputFile = None
  outputFile = None
  isCompress = False
  isDecompress = False
  threshold = 0.0001

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
    image_save(c, outputFile)
    outputFile.close()

  elif isDecompress:
    image = decompress(inputFile)
    Image.fromarray(image).show()
