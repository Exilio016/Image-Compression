# Image-Compression
## Authors
- Bruno Flávio Ferreira
- Edson Yudi Toma

## Main Objective 
The project aims to compress an image using Fourrier Transform and Huffman Compression.

## Input Images
The input images can be any uncompressed image, we use in this project the "Standard" test images, an .tif image database located at http://imageprocessingplace.com/root_files_V3/image_databases.htm to test the algorithm
![Cameraman - Image Example](https://github.com/Exilio016/Image-Compression/blob/master/standard_test_images/cameraman.tif?raw=true)
![Lena Color 512 - Image Example](https://github.com/Exilio016/Image-Compression/blob/master/standard_test_images/lena_color_512.tif?raw=true)

## Algorithm Steps (Compression)
* Read uncompressed image
* Apply FFT in the image
* Cut of values below an given threashold
* Apply Huffman compression in the FFT image
* Save the compressed image

## ALgorithm Steps (Decompression)
* Read compressed image
* Apply Huffman decompression
* Aplly the Inverse FFT in the decompressed image
* Save the new image
