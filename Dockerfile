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

# Clean up build dependencies to reduce image size
RUN apt-get purge -y build-essential && \
    apt-get autoremove -y

# Copy project files
COPY . /app/

# Run migrations (ensure DB is ready in production, use wait-for-it or similar)
# RUN python3 manage.py makemigrations 
# RUN python3 manage.py migrate

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose port
EXPOSE 8001

# Command to run the application
CMD ["gunicorn", "adorBotProject.wsgi:application", "--bind", "0.0.0.0:8001"]
