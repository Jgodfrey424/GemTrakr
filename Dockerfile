# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && echo "deb http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && apt-get update && apt-get install -y google-cloud-sdk


# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . .


# ✅ Run the script to get credentials BEFORE starting Flask
ENTRYPOINT ["sh", "-c", "python apps/get_and_write_creds.py && python run.py"]

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Expose Flask port
EXPOSE 5000

# Run Flask when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
