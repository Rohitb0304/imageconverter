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

# Helper function to convert images to another format
def convert_image_format(input_file, output_format):
    image = Image.open(input_file)
    converted_file = tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False)
    image.save(converted_file.name, output_format.upper())
    return converted_file.name

# Helper function to compress images (resize)
def compress_image(input_file, resize_dimensions):
    image = Image.open(input_file)
    compressed_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    image = image.resize(resize_dimensions)
    image.save(compressed_file.name, "PNG")
    return compressed_file.name

# Streamlit app with improved styling and logic
def main():
    # App title and description with styling
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

    # Select either conversion or compression
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
            help="Supported formats: PNG, JPG, JPEG, BMP, GIF, TIFF"
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
                compressed_file = compress_image(uploaded_file, resize_dimensions)

                # Download button for compressed image
                with open(compressed_file, "rb") as file:
                    st.download_button(
                        label="📥 Download Compressed Image",
                        data=file,
                        file_name="compressed_image.png",
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

        # Upload image for conversion
        uploaded_files = st.file_uploader(
            "Upload images for conversion", 
            accept_multiple_files=True, 
            type=list(IMAGE_FORMATS.values()), 
            help="Supported formats: PNG, JPG, JPEG, BMP, GIF, TIFF"
        )

        # Select output format
        output_format = st.selectbox("🎨 Select output format", list(IMAGE_FORMATS.keys()))

        # Convert images and zip them
        if uploaded_files and output_format:
            if st.button("🔄 Convert Images"):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    converted_files = []
                    for uploaded_file in uploaded_files:
                        output_file = convert_image_format(uploaded_file, IMAGE_FORMATS[output_format])
                        converted_files.append(output_file)

                    # Zip all converted images
                    zip_path = os.path.join(tmp_dir, "converted_images.zip")
                    with ZipFile(zip_path, 'w') as zipf:
                        for file in converted_files:
                            zipf.write(file, os.path.basename(file))

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
