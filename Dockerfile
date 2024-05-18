
FROM python:3.12-slim

WORKDIR /app/TradingDash

COPY Trading_Prediction/TradingDash/requirements.txt .

RUN pip install -r requirements.txt

RUN git clone https://github.com/NicoJanko/Trading_Prediction.git

COPY TradingDash /app/TradingDash

EXPOSE 8080

CMD ["python", "TradingDash.py"]