FROM python:3.12

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
apt-get install -y ffmpeg tini && \
rm -rf /var/lib/apt/lists/*

WORKDIR /recorder

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["tini", "--"]

CMD [ "python", "app/main.py" ]