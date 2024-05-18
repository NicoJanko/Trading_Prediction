
FROM python:3.12-slim

WORKDIR /app/TradingDash

COPY TradingDash/requirements.txt .

RUN pip install -r requirements.txt

COPY TradingDash /app/TradingDash

EXPOSE 8050

CMD ["python", "TradingDash.py"]