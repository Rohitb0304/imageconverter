# Start from the official Python 3.10 image
FROM python:3.10-slim

# Install system dependencies for libheif
RUN apt-get update && apt-get install -y \
    libheif-examples \
    libheif-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]
