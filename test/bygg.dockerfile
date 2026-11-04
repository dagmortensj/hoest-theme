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

# Vanskelige tilfeller: heredoc, flere ARG/ENV, eksek-form, skallform og escape
ARG DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/venv/bin:${PATH}" \
    TEKST="a + b == c" \
    TOM=
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN <<EOT
set -eux
python -m venv /opt/venv && pip install --upgrade pip
echo "${TEKST}" | tr '+' '-' >> /etc/motd
EOT
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt; \
    if [ "$DEBIAN_FRONTEND" = "noninteractive" ]; then echo ja; fi
COPY --from=bygg --chmod=755 /app/bin/ /usr/local/bin/
ADD --checksum=sha256:abc123 https://example.com/fil.tar.gz /tmp/
STOPSIGNAL SIGTERM
ONBUILD RUN echo "bygger barn"
CMD python -m app --port 8000 && echo ferdig
