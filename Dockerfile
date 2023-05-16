FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

ENV INTRODIR /intro

WORKDIR ${INTRODIR}

COPY . .

COPY ./requirements/ /tmp/requirements

ARG DEBUG=False

RUN python -m venv /py && \
        /py/bin/pip install --upgrade pip && \
        if [ $DEBUG == "False" ]; then \
            /py/bin/pip install -r /tmp/requirements/production.txt; \
        else \
            /py/bin/pip install -r /tmp/requirements/dev.txt; \
        fi && \
        rm -rf /tmp && \
        adduser --disabled-password --no-create-home django_intro

USER django_intro

ENV PATH "/py/bin:$PATH"

EXPOSE 8000
