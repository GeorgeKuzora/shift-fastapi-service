# BASE
FROM python:3.12.2-slim AS base
ARG PYTHON_VERSION=3.12.2
ARG APP_NAME="user_service"
ARG APP_PATH="/opt/$APP_NAME"

# STAGING
FROM base AS staging
ARG APP_NAME
ARG APP_PATH
ARG POETRY_VERSION=1.8
ARG PYTHON_VERSION
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=$POETRY_VERSION \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="$PYSETUP_PATH/.venv"
ENV PATH="$POETRY_HOME/bin:$PATH"
WORKDIR $APP_PATH
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -
COPY . .

# DEVELOPMENT
FROM staging AS development
ARG APP_NAME
ARG APP_PATH
WORKDIR $APP_PATH
EXPOSE 8000/tcp
EXPOSE 443/tcp
RUN poetry install --no-root
ENTRYPOINT ["poetry", "run", "python", "manage.py"]
CMD ["runserver_plus", "--key-file", "selftest-key", "--cert-file", "selftest-cert", "0.0.0.0:8000"]

# BUILD
FROM staging as build
ARG APP_NAME
ARG APP_PATH
WORKDIR $APP_PATH
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv $VENV_PATH\
    && chmod +x $VENV_PATH/bin/activate \
    && $VENV_PATH/bin/activate \
    && poetry install --without dev \
    && poetry build --format wheel \
    && poetry export --format requirements.txt --output constraints.txt --without-hashes

# PRODUCTION
FROM base as production
ARG APP_NAME
ARG APP_PATH
ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 
EXPOSE 8000
WORKDIR $APP_PATH
COPY --from=build \
    $APP_PATH/dist/*.whl \
    $APP_PATH/constraints.txt \
    $APP_PATH/manage.py \
    $APP_PATH/docker-entrypoint.sh \
    $APP_PATH
COPY --from=build $APP_PATH/static $STATIC_PATH
COPY --from=build $APP_PATH/static /static/
RUN pip install $APP_NAME*.whl --constraint constraints.txt \
    && rm -f $APP_PATH/constraints.txt $APP_PATH/*.whl \
    && chmod +x $APP_PATH/docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "car_service.wsgi"]
