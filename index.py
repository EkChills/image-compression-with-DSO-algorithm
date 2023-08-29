import os
from PIL import Image
import numpy as np
from sklearn.metrics import mean_squared_error

def psnr(image1, image2, max_value=255):
    mse = np.mean((image1 - image2) ** 2)
    if mse == 0:
        return float('inf')
    return 20 * np.log10(max_value / np.sqrt(mse))

def compress_image_to_jpeg(input_folder, output_folder, quality=85):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpeg', '.png', '.bmp', '.jpg'))]

    for image_file in image_files:
        # Read original image file
        original_image_path = os.path.join(input_folder, image_file)
        original_image = Image.open(original_image_path)
        original_image_array = np.array(original_image)

        # Create a reference image by saving and reading the original image
        reference_image_path = os.path.join(output_folder, 'reference.jpg')
        original_image.save(reference_image_path, format='JPEG', quality=100)
        reference_image = Image.open(reference_image_path)
        reference_image_array = np.array(reference_image)

        # Calculate PSNR of original image with reference
        psnr_before = psnr(original_image_array, reference_image_array, max_value=255)

        # Calculate MSE of original image with reference
        mse_before = mean_squared_error(original_image_array, reference_image_array)

        # Save the initial size of the original image
        initial_size = os.path.getsize(original_image_path) / 1024  # in KB

        # Save the PSNR and MSE before compression, along with initial size
        print(f"Image: image-{len(image_file)}")
        print(f"Initial Size: {initial_size:.2f} KB")
        print(f"PSNR before compression: {psnr_before:.2f} dB")
        print(f"MSE before compression: {mse_before:.2f}")

        # Save the original image as a reference
        original_output_file = os.path.splitext(image_file)[0] + '_original.jpg'
        original_output_path = os.path.join(output_folder, original_output_file)
        original_image.save(original_output_path, format='JPEG', quality=quality)

        # Read image file for compression
        image = Image.open(original_image_path)

        # Save the image as a JPEG file with the specified quality level
        compressed_output_file = os.path.splitext(image_file)[0] + '_compressed.jpg'
        compressed_output_path = os.path.join(output_folder, compressed_output_file)
        image.save(compressed_output_path, format='JPEG', quality=quality)

        # Calculate compressed image size
        compressed_size = os.path.getsize(compressed_output_path) / 1024  # in KB

        # Calculate compression ratio
        compression_ratio = initial_size / compressed_size

        # Read compressed image for PSNR and MSE calculation
        compressed_image = Image.open(compressed_output_path)
        compressed_image_array = np.array(compressed_image)

        # Calculate PSNR and MSE after compression
        psnr_after = psnr(original_image_array, compressed_image_array, max_value=255)
        mse_after = mean_squared_error(original_image_array, compressed_image_array)

        # Save the compressed size, PSNR, and MSE after compression
        print(f"Compressed Size: {compressed_size:.2f} KB")
        print(f"Compression Ratio: {compression_ratio:.2f}")
        print(f"PSNR after compression: {psnr_after:.2f} dB")
        print(f"MSE after compression: {mse_after:.2f}")
        
        print()

    # Remove the reference image after processing all images
    os.remove(reference_image_path)

if __name__ == "__main__":
    input_folder = "./all_doc/mri"  # Replace with the folder containing image files
    output_folder = "./compressed_mri"  # Replace with the folder where JPEG files will be saved
    compress_image_to_jpeg(input_folder, output_folder, quality=85)
