FROM python:3.6.5-alpine3.7

COPY requirements.txt /requirements.txt

RUN apk --update add \
      openssl \
      ca-certificates \
      shadow \
    && apk --update add --virtual .build-dependencies \
      build-base              \
      python-dev              \
      openssl-dev              \
      libffi-dev              \
    && pip install -r /requirements.txt \
    && apk del .build-dependencies \
    && rm -rf /var/cache/apk/*

RUN ln -s /usr/local/bin/python /usr/bin/python

WORKDIR /usr/local/src/app

COPY external_plugins ./external_plugins/
COPY lookup_plugins ./lookup_plugins/
COPY *.py ansible.cfg fetch_keys.yml ./
COPY useradd.sh /usr/local/bin/useradd

RUN chmod +x /usr/local/bin/useradd

CMD python server.py
