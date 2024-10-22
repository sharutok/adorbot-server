# Development stage
FROM python:3.10-slim AS development
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly install gunicorn in the development stage
RUN pip install --no-cache-dir gunicorn

# Copy project files
COPY . /app/

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose port
EXPOSE 8001
CMD ["gunicorn", "adorBotProject.wsgi:application", "--bind", "0.0.0.0:8001"]


