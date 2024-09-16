# Use an official Python image as a base
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg libsndfile1

# Set a working directory in the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app.py file
COPY app.py .

# Copy the rest of your application files
COPY . .

# Download the Spleeter 5stem model
RUN python -c "from spleeter.separator import Separator; Separator('spleeter:5stems')"

# Set environment variable to use the pre-downloaded model
ENV MODEL_PATH /root/.cache/spleeter/pretrained_models/5stems

# Expose the port that Streamlit uses
EXPOSE 7860

# Command to run your app
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]