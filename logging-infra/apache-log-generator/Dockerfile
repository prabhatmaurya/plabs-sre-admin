FROM python:3.6-alpine

COPY app /app
WORKDIR /app
RUN mkdir -p /var/log/
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["log-generator","/app/config/"]
