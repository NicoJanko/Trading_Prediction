# Use the official Python 3.12 image from the Docker Hub
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app/TradingDash

# Clone the repository
RUN git clone https://github.com/NicoJanko/Trading_Prediction.git /app/Trading_Prediction

# Change to the directory containing the requirements.txt
WORKDIR /app/Trading_Prediction/TradingDash

# Install the dependencies
RUN pip install -r requirements.txt

# Set the working directory to where TradingDash.py is located
WORKDIR /app/Trading_Prediction/TradingDash

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run the app
CMD ["python", "TradingDash.py"]