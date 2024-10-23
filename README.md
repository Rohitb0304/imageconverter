---

# 🖼️ Image Converter & Compressor App

This is a **Streamlit** web application that allows users to **convert images** between various formats and **compress images** by resizing them. The app provides an easy-to-use interface for image conversions and compression, ensuring that users can download their converted or compressed images in a few clicks.

---

## Features

- **Image Conversion**: Upload images and convert them to different formats, including:
  - PNG, JPG, JPEG, BMP, GIF, TIFF.
  
- **Image Compression**: Upload an image and resize it to specific pixel dimensions, resulting in a compressed version of the image.

- **Download Converted Images**: After conversion, users can download a **ZIP file** containing all converted images.

- **Download Compressed Image**: After compression, users can download the compressed image as a **PNG file**.

---

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python (Pillow for image handling)
- **Containerization**: Docker

---

## How to Run the App Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Rohitb0304/imageconverter.git
cd imageconverter
```

### 2. Create Virtual Environment

It's recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

### 5. Access the App

After running the app, open your browser and go to `http://localhost:8501` to use the image converter and compressor.

---

## Running the App in Docker

You can also run this app using **Docker** for easy deployment across different environments.

### 1. Build the Docker Image

```bash
docker build -t image-converter-app .
```

### 2. Run the Docker Container

```bash
docker run -p 8501:8501 image-converter-app
```

### 3. Access the App

Once the container is running, go to `http://localhost:8501` in your browser to use the app.

---

## App Usage

### **Image Conversion**
1. Uncheck the `Compress Images Only` checkbox to enable the conversion functionality.
2. Upload one or multiple images in formats like **PNG, JPG, JPEG, BMP, GIF, TIFF**.
3. Choose the output format (e.g., convert from PNG to JPG).
4. Click the **Convert Images** button.
5. Download the ZIP file containing all the converted images.

### **Image Compression**
1. Check the `Compress Images Only` checkbox to enable the compression mode.
2. Upload a single image in formats like **PNG, JPG, JPEG, BMP, GIF, TIFF**.
3. Input the desired width and height in pixels.
4. Click the **Compress Image** button.
5. Download the compressed image in PNG format.

---

## Example

**Image Conversion**:
- Convert `sample.png` to `sample.jpg`.

**Image Compression**:
- Upload a `1920x1080` image, resize it to `800x600`, and download the compressed image.

---

## Project Structure

```
image-converter-compressor-app/
├── app.py                # Main Streamlit app file
├── Dockerfile            # Dockerfile for containerization
├── requirements.txt      # Python dependencies
├── README.md             # Project readme
└── screenshots/          # Screenshots of the app UI
```

---

## Deployment on Render

You can deploy this app to Render easily by following these steps:

1. Push the repository to GitHub or another version control system.
2. Log in to [Render](https://render.com/) and connect the repository.
3. Add a new **Web Service** in Render and select the repository.
4. Use the following build and start commands:
   - Build Command: `docker build -t image-converter-app .`
   - Start Command: `docker run -p 8501:8501 image-converter-app`
5. Deploy and access your app via the generated URL!

---

## Future Improvements

- Add more compression options (e.g., JPEG quality control).
- Support for image rotation and cropping.
- Implement batch image compression with ZIP download.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For any questions or suggestions, feel free to contact:

**Your Name** - [rohitb.0304@gmail.com](mailto:rohitb.0304@gmail.com)

---

This **README** provides all the necessary details to run and deploy the project, along with usage instructions, examples, and project structure. Let me know if you need further modifications!