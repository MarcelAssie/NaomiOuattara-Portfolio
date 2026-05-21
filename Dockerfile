# ==========================
# STEP 1 : Builder Node.js
# ==========================
FROM node:20-slim AS tailwind-builder

WORKDIR /app

# Copy package files to use the Docker cache
COPY theme/static_src/package*.json ./theme/static_src/

# Node dependencies installation
RUN cd theme/static_src && npm ci

# Manage the entire project so that Tailwind can read all my files. html
COPY . .

# Build Tailwind CSS
RUN cd theme/static_src && npm run build


# ==============================
# STEP 2: Final Python Image
# ==============================
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Installation of execution libraries (Pillow, PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Retrieving the CSS generated in step 1
COPY --from=tailwind-builder /app/theme/static/css/dist/styles.css /app/theme/static/css/dist/styles.css

# Collectstatic with temporary variables to avoid polluting the final image
RUN SECRET_KEY="dummy-build-key" DEBUG=False python manage.py collectstatic --noinput

# Create a non-root user to run the app
RUN adduser --disabled-password --no-create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Gunicorn Command
CMD gunicorn naomiouattara_portfolio.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
