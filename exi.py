import os
import pydicom
import numpy as np
from PIL import Image
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def quantize_image(image_array, num_levels):
    # ... (your existing quantization code)
    min_pixel_value = np.min(image_array)
    max_pixel_value = np.max(image_array)
    
    # Compute the interval size for quantization
    interval_size = (max_pixel_value - min_pixel_value + 1) // num_levels
    
    # Apply quantization by mapping pixel values to quantized levels
    quantized_image = ((image_array - min_pixel_value) // interval_size) * interval_size + min_pixel_value

    return quantized_image

def psnr(image1, image2, max_value=255):
    mse = np.mean((image1 - image2) ** 2)
    if mse == 0:
        return float('inf')
    return 20 * np.log10(max_value / np.sqrt(mse))

def compress_and_convert_dicom_to_png(input_folder, output_folder, num_levels=64, compression_level=0):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of DICOM files in the input folder
    dicom_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.dcm')]

    mse_list = []
    psnr_list = []

    for dicom_file in dicom_files:
        # Read DICOM file
        dicom_path = os.path.join(input_folder, dicom_file)
        ds = pydicom.dcmread(dicom_path)

        # Convert pixel data to a numpy array
        pixel_data = ds.pixel_array

        # Apply quantization to reduce the number of intensity levels
        quantized_pixel_data = quantize_image(pixel_data, num_levels)

        # Calculate performance metrics
        mse = mean_squared_error(pixel_data.flatten(), quantized_pixel_data.flatten())
        psnr_value = psnr(pixel_data, quantized_pixel_data)
        mse_list.append(mse)
        psnr_list.append(psnr_value)
        dicom_path = os.path.join(input_folder, dicom_file)
        ds = pydicom.dcmread(dicom_path)

        # Convert pixel data to a numpy array
        pixel_data = ds.pixel_array

        # Apply quantization to reduce the number of intensity levels
        quantized_pixel_data = quantize_image(pixel_data, num_levels)

        # Create an Image object from the quantized pixel data
        quantized_image = Image.fromarray(quantized_pixel_data)

        # Save the image as a PNG file with the specified compression level
        output_file = os.path.splitext(dicom_file)[0] + '_quantized.png'
        output_path = os.path.join(output_folder, output_file)
        quantized_image.save(output_path, format='PNG', compress_level=compression_level)


if __name__ == "__main__":
    input_folder = "./med_images"  # Replace with the folder containing DICOM files
    output_folder = "./compressed"  # Replace with the folder where PNG files will be saved
    num_levels = 64  # Number of intensity levels for quantization
    compression_level = 3  # Example compression level (1-9)

    mse_list = []
    psnr_list = []

    # Get a list of DICOM files in the input folder
    dicom_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.dcm')]

    for dicom_file in dicom_files:
        # ... (your existing code)
       dicom_path = os.path.join(input_folder, dicom_file)
       ds = pydicom.dcmread(dicom_path)

        # Convert pixel data to a numpy array
       pixel_data = ds.pixel_array

        # Apply quantization to reduce the number of intensity levels
       quantized_pixel_data = quantize_image(pixel_data, num_levels)

        # Calculate performance metrics
       mse = mean_squared_error(pixel_data.flatten(), quantized_pixel_data.flatten())
       psnr_value = psnr(pixel_data, quantized_pixel_data)
       mse_list.append(mse)
       psnr_list.append(psnr_value)

        # Create an Image object from the quantized pixel data
       quantized_image = Image.fromarray(quantized_pixel_data)

        # Save the image as a PNG file with the specified compression level
       output_file = os.path.splitext(dicom_file)[0] + '_quantized.png'
       output_path = os.path.join(output_folder, output_file)
       quantized_image.save(output_path, format='PNG', compress_level=compression_level)

    # Calculate overall performance metrics
       avg_mse = np.mean(mse_list)
       avg_psnr = np.mean(psnr_list)

    # Output the evaluation performance metrics
    print("Average Mean Squared Error:", avg_mse)
    print("Average Peak Signal-to-Noise Ratio:", avg_psnr)

    # Plot the performance metrics
    plt.figure(figsize=(10, 5))
    plt.bar(['MSE', 'PSNR'], [avg_mse, avg_psnr], color=['blue', 'green'])
    plt.ylabel('Value')
    plt.title('Performance Metrics')
    plt.show()