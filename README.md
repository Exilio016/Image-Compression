# Image-Compression
## Authors
- Bruno Flávio Ferreira
- Edson Yudi Toma

## Main Objective 
The project aims to compress an image using Fourrier Transform and Huffman Compression.

## Input Images
The input images can be any uncompressed image, we use in this project the "Standard" test images, an .tif image database located at http://imageprocessingplace.com/root_files_V3/image_databases.htm to test the algorithm

The images can be colored or not:

![cameraman](https://user-images.githubusercontent.com/10467900/58565898-f34f0400-8205-11e9-8019-6be10c7a730b.png)
![lena_color_256](https://user-images.githubusercontent.com/10467900/58565899-f34f0400-8205-11e9-9382-6ebf60068b3f.png)

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
