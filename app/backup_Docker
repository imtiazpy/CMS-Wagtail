# syntax=docker/dockerfile:1

ARG PYTHON_TAG=3.11.4-slim-buster
FROM python:${PYTHON_TAG}

RUN useradd wagtail

WORKDIR /usr/src/app
RUN mkdir /usr/src/app/staticfiles

# create mediafiles directory if not already existing
RUN mkdir /usr/src/app/mediafiles

RUN chown -R wagtail:wagtail /usr/src/app

# Port used by this container to serve HTTP.
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
# this line (--mount=type=cache,target=/var/cache/apt) will enable building from the apt cache if the re-build is required
RUN \
    --mount=type=cache,target=/var/cache/apt \
    apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    netcat \
 && rm -rf /var/lib/apt/lists/*

# Install the project requirements.
COPY --chown=wagtail:wagtail ./Pipfile ./Pipfile.lock /usr/src/app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -q 'pipenv==2024.0.1' && \
    pipenv install --deploy --system

# copy project
COPY --chown=wagtail:wagtail ./ /usr/src/app

USER wagtail

# Ensure the entrypoint script has Unix line endings and is executable.
RUN sed -i 's/\r$//g' /usr/src/app/scripts/entrypoint.sh
RUN chmod +x /usr/src/app/scripts/entrypoint.sh

# uncomment bellow command if mediafiles and sqlite3 is already existing
# RUN chmod +x /usr/src/app/mediafiles && \
#     chown -R wagtail:wagtail /usr/src/app/mediafiles && \
#     chown wagtail:wagtail /usr/src/app/db.sqlite3

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/scripts/entrypoint.sh"]