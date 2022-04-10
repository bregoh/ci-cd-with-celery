# pull official base image
FROM python:3.10.1-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# dependencies
RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # psycopg2 dependencies
    && apt-get install -y libpq-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    # Additional dependencies for pkill
    && apt-get install -y procps \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

COPY /entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY /start_app /start_app
RUN sed -i 's/\r$//g' /start_app
RUN chmod +x /start_app

COPY /start_celery /start_celery
RUN sed -i 's/\r$//g' /start_celery
RUN chmod +x /start_celery

COPY /flower_start /flower_start
RUN sed -i 's/\r$//g' /flower_start
RUN chmod +x /flower_start

ENTRYPOINT ["/entrypoint"]