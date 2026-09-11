FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    AL_MEHDI_DB=/data/al_mehdi.db

WORKDIR /app

RUN groupadd --system almehdi && useradd --system --gid almehdi --home-dir /app almehdi

COPY pyproject.toml README.md LICENSE ./
COPY al_mehdi ./al_mehdi

RUN python -m pip install --no-cache-dir --disable-pip-version-check . \
    && mkdir -p /data \
    && chown -R almehdi:almehdi /app /data

USER almehdi

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import json,urllib.request; data=json.load(urllib.request.urlopen('http://127.0.0.1:8080/health',timeout=2)); raise SystemExit(0 if data.get('status')=='ok' else 1)"

CMD ["al-mehdi", "serve", "--host", "0.0.0.0", "--port", "8080"]

