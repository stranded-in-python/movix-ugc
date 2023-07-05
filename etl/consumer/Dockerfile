FROM python:3.10 as base

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt \
    && rm requirements.txt

FROM base as prod

COPY . .

CMD ["/usr/local/bin/python", "/app/consumer.py"]