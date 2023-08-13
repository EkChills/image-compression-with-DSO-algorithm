import numpy as np
from PIL import Image

def compress_image(image_path, compression_ratio):
    # Load the image
    image = Image.open(image_path)

    # Convert the image to grayscale
    image = image.convert('L')

    # Convert the image to a numpy array
    img_array = np.array(image)

    # Define the compression ratio
    rows, cols = img_array.shape
    num_pixels = rows * cols
    num_compressed_pixels = int(num_pixels * compression_ratio)

    # Initialize the compressed image array
    compressed_img_array = np.zeros((rows, cols))

    # Generate random indices for the compressed pixels
    indices = np.random.choice(num_pixels, size=num_compressed_pixels, replace=False)

    # Set the compressed pixels in the compressed image array
    compressed_img_array.flat[indices] = img_array.flat[indices]

    # Convert the compressed image array to 8-bit integer format
    compressed_img_array = compressed_img_array.astype(np.uint8)

    # Convert the compressed image array back to an image
    compressed_image = Image.fromarray(compressed_img_array)

    return compressed_image

# Example usage
compressed_image = compress_image('./arya_star.png', 0.5)
compressed_image.save('compressed_image.jpg')
