FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Choreo የሚጠብቀውን ፖርት መክፈት
EXPOSE 8080

CMD ["python", "scanner_bot.py"]
