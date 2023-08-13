from PIL import Image
import numpy as np

def decode_png_to_numpy(png_file_path):
    # Open the PNG image using Pillow
    image = Image.open(png_file_path)

    # Convert the image to a NumPy array
    image_array = np.array(image)

    return image_array

if __name__ == "__main__":
    compressed_png_file = "path/to/compressed_image.png"  # Replace with the path to your compressed PNG image
    decoded_image_array = decode_png_to_numpy(compressed_png_file)
    print(decoded_image_array)