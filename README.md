# Image-Compression
## Authors
- Bruno Flávio Ferreira
- Edson Yudi Toma

## Main Objective 
The project aims to compress an image using Fourrier Transform and Huffman Compression.

## Input Images
The input images can be any uncompressed image, we use in this project the "Standard" test images, an .tif image database located at http://imageprocessingplace.com/root_files_V3/image_databases.htm to test the algorithm.

The images can be colored or not:

![cameraman](https://user-images.githubusercontent.com/10467900/58565898-f34f0400-8205-11e9-8019-6be10c7a730b.png)
![lena_color_256](https://user-images.githubusercontent.com/10467900/58565899-f34f0400-8205-11e9-9382-6ebf60068b3f.png)

## Algorithm Steps (Compression)
* Read uncompressed image
* Apply FFT in the image
* Cut of values below an given threashold
* Apply Huffman compression in the FFT image
* Save the compressed image

## Algorithm Steps (Decompression)
* Read compressed image
* Apply Huffman decompression
* Aplly the Inverse FFT in the decompressed image
* Show the image in the screen

## Results
| Image | Original Size | Threshold = 0.008 | Threshold = 0.01 | Threshold = 0.05 |
| ----- | ------------- | ----------------- | ---------------- | ---------------- |
| cameraman.tif |  262,8 kB | 245,0 kB | 217,1 kB | 138,3 kB |
| lena_color_512.tif |  787,5 kB | 478,3 kB | 454,9 kB | 399,1 kB |
| mandril_color.tif |  787,4 kB | 661,6 kB | 553,6 kB | 399,6 kB |

The program was able to compress the image, but with a loss of quality. This is due to the fact that there are few values repeated after the FFT application, together with the need to save the huffman tree, it is necessary to cut many values (ie a high threshold) resulting in loss of quality.

| Original Image | Threshold = 0.008 | Threshold = 0.01 | Threshold = 0.05 |
| -------------- | ----------------- | ---------------- | ---------------- |
| ![original](https://user-images.githubusercontent.com/10467900/60060045-47de8580-96c5-11e9-9314-8464f9821142.png) | ![t = 0.008](https://user-images.githubusercontent.com/10467900/60060133-a277e180-96c5-11e9-999d-5c28a5163fa7.png) | ![t = 0.01](https://user-images.githubusercontent.com/10467900/60060110-8bd18a80-96c5-11e9-9ba3-2670f19f4e98.png) | ![t = 0.05](https://user-images.githubusercontent.com/10467900/60060168-c1767380-96c5-11e9-8ec4-6bea7cefd6f5.png) |

It is possible to observe that with very high threshold value, the resulting image is incomprehensible.

## Dependencies
To run this program you will need Python3 installed in your machine and some libraries:
* Numpy
* Scipy
* Imageio
* Pillow

To install then you can run the following command:
~~~
pip3 install numpy
pip3 install scipy
pip3 install imageio
pip3 install pillow
~~~
 
You may have to install python-tkinter for the program to work correctly, on Ubuntu you can execute this command:
~~~
sudo apt-get install python3-tk
~~~

## Run the program
To run this program simply execute the run.sh, passing the desired arguments.
To view the possible arguments, execute: `./run.sh -h`

### Compression
To compress an image, run:
~~~
./run.sh -c path-to-image -o output-image
~~~
This will compress the image with the default threshold of 0.01, to especify a threshold, run:
~~~
./run.sh -c path-to-image -o output-image -t value
~~~

### Decompression
To decompress an image, run:
~~~
./run.sh -d path-to-image
~~~

## Demo program
To test this program you can run the following command:
~~~
./run.sh -c standard_test_images/mandril_color.tif -o mandril.bin
./run.sh -d mandril.bin
~~~
This will compress the mandril image, decompress and show on screen
