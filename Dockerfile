FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE config.settings.production

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir "setuptools<58.0.0"
RUN pip install --no-cache-dir -r requirements.txt
RUN echo "__version__ = '3.1.0'" >> /usr/local/lib/python3.9/site-packages/jquery/__init__.py
RUN python -c "with open('/usr/local/lib/python3.9/site-packages/django/db/backends/postgresql/utils.py', 'w') as f: f.write('from datetime import timedelta\nfrom django.utils.timezone import utc\n\ndef utc_tzinfo_factory(offset):\n    if offset != 0 and offset != timedelta(0):\n        raise AssertionError(\"database connection isn\'t set to UTC\")\n    return utc\n')"

COPY . /app/

EXPOSE 8080

CMD exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120