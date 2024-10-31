FROM python:3.12.7-slim-bullseye

# Install system dependencies
RUN apt-get update && \
		apt-get install -y wkhtmltopdf libreoffice && \
		apt-get install -y libxrender1 libxext6 libfontconfig1 && \
		apt-get install -y libpq-dev gcc && \
		apt-get clean && \
		rm -rf /var/lib/apt/lists/*

# Set up Python environment
ENV PYTHONBUFFERED=1

ENV PORT 8000

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD gunicorn server.wsgi:application --bind 0.0.0.0:"${PORT}"

EXPOSE ${PORT}
