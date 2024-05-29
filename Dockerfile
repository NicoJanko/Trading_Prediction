# Use the official Python 3.12 image from the Docker Hub
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# install git

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    libhdf5-dev \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/NicoJanko/Trading_Prediction.git

# Change to the directory containing the requirements.txt
WORKDIR /app/Trading_Prediction/Dashboard

# Install the dependencies
RUN pip install -r requirements.txt

#Launch data_update
WORKDIR /app/Trading_Prediction/Dashboard/data
CMD ["python", "data_update.py"]


WORKDIR /app/Trading_Prediction/Dashboard
# Expose the port the app runs on
EXPOSE 8080

# Define the command to run the app

CMD ["python", "TradingDash.py"]