FROM python:3.8.13-slim-bullseye

ENV PYTHONUNBUFFERED=1
ARG ENV=develop
ARG POETRY_VER=1.8.2

WORKDIR /usr/lib/app

COPY pyproject.toml poetry.lock ./

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        build-essential \
        libpq-dev \
        curl \
        gosu && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --disable-pip-version-check --no-compile --upgrade pip poetry==${POETRY_VER} && \
    poetry config virtualenvs.create false && \
    if [ "${ENV}" = "develop" ]; then \
        poetry install; \
    else \
        poetry install --only main; \
    fi; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    find /usr/local/lib | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf && \
    find /var/log -type f | xargs rm -rf && \
    rm -r ~/.cache \
        pyproject.toml \
        poetry.lock && \
    groupadd -r backend --gid=990 && \
    useradd -r -g backend --uid=990 --home-dir=/usr/lib/backend --shell=/bin/bash backend && \
    mkdir -p /usr/lib/app/logs && \
    chown backend:backend /usr/lib/app /usr/lib/app/logs

COPY --chown=backend:backend ./app/main.py ./app/main.py

# Future alembic migrations
# CMD bash scripts/entry

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]