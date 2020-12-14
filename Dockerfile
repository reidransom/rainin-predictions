FROM python:3-alpine

ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN pip install mysqlclient

RUN apk del build-deps

COPY checkdb.py /

CMD python /checkdb.py
