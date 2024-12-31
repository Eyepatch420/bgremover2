# Use a specific version of Python
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port (optional, but good practice)
EXPOSE 5000

# Start the app using Gunicorn
CMD ["gunicorn", "testing:app", "--bind", "0.0.0.0:5000"]
