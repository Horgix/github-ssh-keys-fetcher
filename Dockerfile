FROM python:3.6.4-alpine

COPY requirements.txt /requirements.txt

RUN apk --update add \
      openssl \
      ca-certificates \
    && apk --update add --virtual .build-dependencies \
      build-base              \
      python-dev              \
      openssl-dev              \
      libffi-dev              \
    && pip install -r /requirements.txt \
    && apk del .build-dependencies \
    && rm -rf /var/cache/apk/*

WORKDIR /usr/local/src/app

COPY *.py ./
COPY fetch_keys.yml ./

CMD python server.py