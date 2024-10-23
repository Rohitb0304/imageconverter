import os
from PIL import Image
import streamlit as st
import tempfile
from zipfile import ZipFile
import pyheif
import time  # Import time for simulating the upload delay

# Supported formats for conversion
IMAGE_FORMATS = {
    "PNG": "png",
    "JPG": "jpg",
    "JPEG": "jpeg",
    "BMP": "bmp",
    "GIF": "gif",
    "TIFF": "tiff",
    "HEIC": "heic"
}

# Helper function to convert HEIC to other formats
def convert_heic_to_image(input_file):
    try:
        heif_file = pyheif.read(input_file)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            heif_file.stride,
        )
        return image
    except Exception as e:
        st.error(f"Error converting HEIC image: {e}")
        return None

# Helper function to convert images to another format
def convert_image_format(input_file, output_format):
    try:
        if input_file.type == "image/heic":
            image = convert_heic_to_image(input_file)
            if image is None:
                return None, None  # Return if conversion failed
        else:
            image = Image.open(input_file)

        original_filename = os.path.splitext(input_file.name)[0]
        converted_file = tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False)
        image.save(converted_file.name, output_format.upper())
        return converted_file.name, f"{original_filename}_converted.{output_format}"

    except Exception as e:
        st.error(f"An error occurred during conversion: {e}")
        return None, None

# Helper function to compress images (resize)
def compress_image(input_file, resize_dimensions):
    try:
        image = Image.open(input_file)
        original_filename = os.path.splitext(input_file.name)[0]
        compressed_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        image = image.resize(resize_dimensions)
        image.save(compressed_file.name, "PNG")
        return compressed_file.name, f"{original_filename}_compressed.png"
    except Exception as e:
        st.error(f"An error occurred during compression: {e}")
        return None, None

# Streamlit app with improved styling and logic
def main():
    st.markdown(
        """
        <div style="text-align:center; padding: 20px;">
            <h1 style="color:#2E86C1; font-family: 'Arial';">🖼️ Image Format Converter & Compressor</h1>
            <p style="font-size:18px; color:#34495E; font-family: 'Arial';">
                Convert or compress your images effortlessly with our simple app!
            </p>
        </div>
        """, unsafe_allow_html=True
    )

    compress_images = st.checkbox("🗜️ Compress Images Only", help="If checked, only image compression will be available")

    if compress_images:
        # Compression mode UI
        st.markdown(
            """
            <div style="background-color:#EBF5FB; padding: 10px; border-radius: 10px;">
                <h3 style="color:#1A5276;">Compress Images</h3>
                <p style="color:#1A5276; font-size:16px;">Upload your image and set the desired dimensions for compression.</p>
            </div>
            """, unsafe_allow_html=True
        )

        # Upload image for compression
        uploaded_file = st.file_uploader(
            "Upload image for compression", 
            type=list(IMAGE_FORMATS.values()), 
            help="Supported formats: PNG, JPG, JPEG, BMP, GIF, TIFF, HEIC"
        )

        # Input fields for resizing dimensions
        if uploaded_file:
            col1, col2 = st.columns(2)
            with col1:
                width = st.number_input("📏 Width (pixels)", min_value=1, value=800, step=1)
            with col2:
                height = st.number_input("📏 Height (pixels)", min_value=1, value=600, step=1)
            resize_dimensions = (width, height)

            # Compress and download button
            if st.button("🗜️ Compress Image"):
                compressed_file, compressed_name = compress_image(uploaded_file, resize_dimensions)

                if compressed_file:
                    # Download button for compressed image
                    with open(compressed_file, "rb") as file:
                        st.download_button(
                            label="📥 Download Compressed Image",
                            data=file,
                            file_name=compressed_name,
                            mime="image/png"
                        )

    else:
        # Conversion mode UI
        st.markdown(
            """
            <div style="background-color:#EBF5FB; padding: 10px; border-radius: 10px;">
                <h3 style="color:#1A5276;">Convert Images</h3>
                <p style="color:#1A5276; font-size:16px;">Upload your image and select the desired output format for conversion.</p>
            </div>
            """, unsafe_allow_html=True
        )

        # Select input image type
        input_format = st.selectbox("🎨 Select Input Image Type", list(IMAGE_FORMATS.keys()))

        # Define accepted file types based on input selection
        accepted_types = [IMAGE_FORMATS[input_format]]

        # Upload image for conversion
        uploaded_files = st.file_uploader(
            "Upload images for conversion", 
            accept_multiple_files=True, 
            type=accepted_types, 
            help="Supported formats: " + ", ".join(IMAGE_FORMATS.keys())
        )

        # Select output format
        output_format = st.selectbox("🖌️ Select Output Format", list(IMAGE_FORMATS.keys()))

        # Convert images and zip them
        if uploaded_files and output_format:
            if st.button("🔄 Convert Images"):
                progress_bar = st.progress(0)  # Initialize progress bar
                total_files = len(uploaded_files)
                converted_files = []

                with tempfile.TemporaryDirectory() as tmp_dir:
                    for i, uploaded_file in enumerate(uploaded_files):
                        output_file, converted_name = convert_image_format(uploaded_file, IMAGE_FORMATS[output_format])
                        if output_file:  # Check if the conversion was successful
                            converted_files.append((output_file, converted_name))

                        # Update progress bar
                        progress = (i + 1) / total_files
                        progress_bar.progress(progress)  # Update progress bar

                    # Zip all converted images
                    zip_path = os.path.join(tmp_dir, "converted_images.zip")
                    with ZipFile(zip_path, 'w') as zipf:
                        for file, name in converted_files:
                            zipf.write(file, name)

                    # Download button for ZIP file
                    with open(zip_path, "rb") as zipf:
                        st.download_button(
                            label="📁 Download All Converted Images (ZIP)",
                            data=zipf,
                            file_name="converted_images.zip",
                            mime="application/zip"
                        )

if __name__ == "__main__":
    main()
