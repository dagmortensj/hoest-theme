# syntax=docker/dockerfile:1
# Dockerfile: lag, argumenter, miljø og kommandoer
ARG PYTHON_VERSJON=3.13
FROM python:${PYTHON_VERSJON}-slim AS bygg

LABEL maintainer="Ola" versjon="1.0"
ENV PYTHONUNBUFFERED=1 \
    APP_HJEM=/app
WORKDIR $APP_HJEM

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && apt-get install -y git

COPY --chown=app:app . .
FROM bygg AS kjoring
USER app
EXPOSE 8000/tcp
VOLUME ["/data"]
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/ || exit 1
ENTRYPOINT ["python", "-m", "app"]
CMD ["--port", "8000"]
