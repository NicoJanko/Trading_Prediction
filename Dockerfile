# Use the official Python 3.12 image from the Docker Hub
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install git and other dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    libpq-dev \
    libhdf5-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/NicoJanko/Trading_Prediction.git

# Change to the directory containing the requirements.txt
WORKDIR /app/Trading_Prediction/Dashboard


RUN ls -l
RUN cat requirements.txt
# Install the dependencies
RUN pip install -r requirements.txt


RUN chmod +x /app/Trading_Prediction/Dashboard/run.sh
# Expose the port the app runs on
EXPOSE 8080

# Define the command to run the app
CMD ["/app/Trading_Prediction/Dashboard/run.sh"]
