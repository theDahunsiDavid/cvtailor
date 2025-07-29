FROM python:3.9-slim

# Install system dependencies & needed packages
RUN apt-get update && \
		apt-get install -y wkhtmltopdf libreoffice && \
		apt-get install -y libxrender1 libxext6 libfontconfig1 && \
		apt-get install -y libpq-dev gcc && \
		apt-get clean && \
		rm -rf /var/lib/apt/lists/*

# Set up Python environment & environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Add a default SECRET_KEY for collectstatic (not used in production)
ENV SECRET_KEY=build_secret_key_not_used_in_production

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD gunicorn cvtailor_project.wsgi:application --bind 0.0.0.0:${PORT}
