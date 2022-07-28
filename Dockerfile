# Base Config
ARG PYTHON_VERSION=3.8.12
FROM python:${PYTHON_VERSION}-slim as base

# Builder
FROM base as builder

WORKDIR /srv/app

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils \
    build-essential \
    libsasl2-dev \
    python3-dev \
    liblzma-dev \
    libpq-dev \
    gnupg2 \
    curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
  && /root/.poetry/bin/poetry export --without-hashes > requirements.txt \
  && pip install --no-cache-dir --disable-pip-version-check --no-warn-script-location --upgrade pip setuptools \
  && pip install --no-cache-dir --disable-pip-version-check --no-warn-script-location --user -r requirements.txt \
  \
  && apt-get clean autoclean \
  && apt-get autoremove --yes \
  && rm -rf /var/lib/{apt,dpkg,cache,log}


# App
FROM base

ARG USER=django

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils \
    build-essential \
    libsasl2-dev \
    python3-dev \
    liblzma-dev \
    libpq-dev \
    gnupg2 \
    curl \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/apt/lists/*

ENV HOME=/home/${USER}
ENV PATH=$PATH:/opt/mssql-tools/bin
ENV PATH=${HOME}/.local/bin:${PATH}

RUN useradd -s /bin/bash -m -d ${HOME} ${USER} \
  && mkdir ${HOME}/project \
  && mkdir ${HOME}/project/media \
  && chown -R ${USER}:${USER} ${HOME}/project

WORKDIR ${HOME}/project

USER ${USER}

VOLUME ${HOME}/project/media

COPY --chown=${USER}:${USER} --from=builder /root/.local ${HOME}/.local
COPY --chown=${USER}:${USER} --from=builder /usr/local/lib/ /usr/local/lib/
COPY --chown=${USER}:${USER} docker/run-* /usr/local/bin/
COPY --chown=${USER}:${USER} src .

CMD [ "run-server" ]
