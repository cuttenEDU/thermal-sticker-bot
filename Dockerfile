FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt update && apt install ffmpeg -y

COPY . .

ENTRYPOINT ["python3","src/main.py"]