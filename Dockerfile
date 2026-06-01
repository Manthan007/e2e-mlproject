# Use an official lightweight Python runtime
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code and your artifacts folder into the container
COPY . .

# Expose the port your application runs on
EXPOSE 7860

# Command to execute the application
CMD ["python", "app.py"]