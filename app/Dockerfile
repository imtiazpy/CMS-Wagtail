# syntax=docker/dockerfile:1

ARG PYTHON_TAG=3.11-slim-bookworm

# -------------------------
# 1️⃣ Builder stage
# -------------------------
FROM python:${PYTHON_TAG} as builder

WORKDIR /install

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv and dependencies
COPY Pipfile Pipfile.lock ./

RUN pip install --upgrade pip && \
    pip install pipenv==2024.0.1 && \
    pipenv install --deploy --system

# -------------------------
# 2️⃣ Final stage (small image)
# -------------------------
FROM python:${PYTHON_TAG}

RUN useradd -m wagtail

WORKDIR /usr/src/app

# Only runtime dependencies (NO build-essential here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Create directories
RUN mkdir -p /usr/src/app/staticfiles /usr/src/app/mediafiles && \
    chown -R wagtail:wagtail /usr/src/app

# Copy project
COPY --chown=wagtail:wagtail . .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

USER wagtail

# Fix entrypoint
RUN sed -i 's/\r$//g' /usr/src/app/scripts/entrypoint.sh && \
    chmod +x /usr/src/app/scripts/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/usr/src/app/scripts/entrypoint.sh"]