import os
import pydicom
from PIL import Image

def compress_dicom_to_jpeg(input_folder, output_folder, quality=85):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of DICOM files in the input folder
    dicom_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.dcm')]

    for dicom_file in dicom_files:
        # Read DICOM file
        dicom_path = os.path.join(input_folder, dicom_file)
        ds = pydicom.dcmread(dicom_path)

        # Convert pixel data to a numpy array
        pixel_data = ds.pixel_array

        # Create an Image object from the pixel data
        image = Image.fromarray(pixel_data)

        # Save the image as a JPEG file with the specified quality level
        output_file = os.path.splitext(dicom_file)[0] + '.jpg'
        output_path = os.path.join(output_folder, output_file)
        image.save(output_path, format='JPEG', quality=quality)

if __name__ == "__main__":
    input_folder = "./med_images"  # Replace with the folder containing DICOM files
    output_folder = "./compressed_lossy"  # Replace with the folder where JPEG files will be saved
    compress_dicom_to_jpeg(input_folder, output_folder, quality=85)
