FROM python:alpine3.7
COPY . /app
WORKDIR /app/demo
COPY requirements.txt .
RUN ls
RUN apk add --update python-dev py-pip build-base gcc musl-dev libffi-dev openssl-dev \
    libxml2-dev libxslt-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
LABEL name="scrapy-docker-image"
ENTRYPOINT ["scrapy"]
CMD []
