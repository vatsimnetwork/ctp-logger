FROM python:3.12-slim
WORKDIR /app
COPY . .
VOLUME ["/app/logs"]
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-u", "main.py"]