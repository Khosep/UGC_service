FROM python:3.11-bullseye

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY docker-entrypoint.sh docker-entrypoint.sh
COPY pyproject_docker.toml pyproject.toml
COPY poetry_docker.lock poetry.lock
COPY uwsgi/uwsgi.ini uwsgi.ini
RUN pip install --upgrade pip && pip install poetry && poetry install
COPY . .

EXPOSE 8000

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
