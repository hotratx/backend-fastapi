# pull official base image
FROM python:3.10.8-bullseye

# set working directory
ENV HOME=/app
WORKDIR $HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.3.1 \
    POETRY_HOME="/opt/poetry"

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql curl python3-dev \
  && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - --version ${POETRY_VERSION} && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /$HOME/

# Looks like poetry fails to add itself to the Path in Docker. We add it here.
ARG INSTALL_DEV=true
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ENV PYTHONPATH "${PYTHONPATH}:/$HOME"
# ENV PATH $PATH:/usr/bin/java

COPY . .
