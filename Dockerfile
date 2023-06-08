FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

ENV INTRODIR /intro

WORKDIR ${INTRODIR}

COPY . .

COPY ./requirements/ /tmp/requirements

ARG DEBUG=False

RUN --mount=type=cache,target=/root/.cache \
    pip --timeout=60 install -r /tmp/requirements/dev.txt

EXPOSE 8000
