# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /app
ENV FLASK_APP=./src/compressing/fastap.py
ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add --no-cache ffmpeg
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "./src/compressing/fastap.py"]
