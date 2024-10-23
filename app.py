import os
from PIL import Image
import streamlit as st
import tempfile
from zipfile import ZipFile

# Supported formats for conversion
IMAGE_FORMATS = {
    "PNG": "png",
    "JPG": "jpg",
    "JPEG": "jpeg",
    "BMP": "bmp",
    "GIF": "gif",
    "TIFF": "tiff"
}

# Helper function to convert and optionally compress image
def convert_image_format(input_file, output_format, resize_dimensions=None):
    image = Image.open(input_file)
    
    # Resize/compress image if dimensions are specified
    if resize_dimensions:
        image = image.resize(resize_dimensions)

    converted_file = tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False)
    image.save(converted_file.name, output_format.upper())
    return converted_file.name

# Streamlit app
def main():
    st.title("🖼️ Image Format Converter and Compressor")
    st.write("Easily convert and compress images with this app!")

    # Upload images
    uploaded_files = st.file_uploader(
        "Upload images", 
        accept_multiple_files=True, 
        type=list(IMAGE_FORMATS.values()),
        help="Supported formats: PNG, JPG, JPEG, BMP, GIF, TIFF"
    )

    # Select output format
    output_format = st.selectbox("Select output format", list(IMAGE_FORMATS.keys()))

    # Compression option
    compress_images = st.checkbox("Compress Images")
    resize_dimensions = None
    if compress_images:
        col1, col2 = st.columns(2)
        with col1:
            width = st.number_input("Width (pixels)", min_value=1, value=800, step=1)
        with col2:
            height = st.number_input("Height (pixels)", min_value=1, value=600, step=1)
        resize_dimensions = (width, height)
        st.write(f"Images will be resized to {width}x{height} pixels.")

    # Convert images and zip them
    if uploaded_files and output_format:
        with tempfile.TemporaryDirectory() as tmp_dir:
            converted_files = []
            for uploaded_file in uploaded_files:
                output_file = convert_image_format(
                    uploaded_file, 
                    IMAGE_FORMATS[output_format], 
                    resize_dimensions
                )
                converted_files.append(output_file)

            # Zip all converted/compressed images
            zip_path = os.path.join(tmp_dir, "converted_images.zip")
            with ZipFile(zip_path, 'w') as zipf:
                for file in converted_files:
                    zipf.write(file, os.path.basename(file))

            # Provide download link for ZIP file
            with open(zip_path, "rb") as zipf:
                st.download_button(
                    label="📁 Download All Converted/Compressed Images (ZIP)",
                    data=zipf,
                    file_name="converted_images.zip",
                    mime="application/zip"
                )

if __name__ == "__main__":
    main()