# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . .

# Expose port 5000
EXPOSE 9090

# Command to run the Flask app
CMD ["python", "app.py"]
