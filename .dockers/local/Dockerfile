FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
	# psycopg2 dependencies
	&& apk add --virtual build-deps gcc python3-dev musl-dev \
	&& apk add postgresql-dev \
	# Pillow dependencies
	&& apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
	# Translation dependencies
	&& apk add gettext \
	# CFFI dependencies
	&& apk add libffi-dev py-cffi \
	&& apk add --no-cache openssl-dev libffi-dev \
	&& apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev \
	# lxml dependencies
	&& apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev \
    && apk add --no-cache libxslt \
    && pip install --no-cache-dir lxml>=3.5.0 \
    && apk del .build-deps

RUN mkdir /app
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt
COPY . /app/
WORKDIR /app
