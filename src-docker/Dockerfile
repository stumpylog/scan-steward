# syntax=docker/dockerfile:1
# Stage: python-base
# Purpose: Single location to set version of Python
FROM python:3.11-alpine as python-base

ENV \
    LANG="C.UTF-8" \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_FIND_LINKS="https://wheels.home-assistant.io/musllinux/ https://wheel-index.linuxserver.io/alpine/" \
    PIP_PREFER_BINARY=1 \
    PYTHONDONTWRITEBYTECODE=1

# Stage: poetry-base
# Purpose: Generates a requirements.txt file for building
# Comments:
#  - pipenv dependencies are not left in the final image
#  - pipenv can't touch the final image somehow
FROM python-base as poetry-base

ARG POETRY_VERSION= 1.7.1

WORKDIR /poetry

COPY pyproject.yml .
COPY poetry.lock .

RUN --mount=type=cache,target=/root/.cache/pip/,id=pip-cache \
  set -eux \
  && echo "Installing poetry" \
    && python3 -m pip install --no-cache-dir --upgrade poetry==${POETRY_VERSION} \
		&& poetry self add poetry-plugin-export \
  && echo "Generating requirement.txt" \
    && poetry export --only main --without-hashes > requirements.txt

# Stage: s6-base
# Purpose: Handles setting up s6-overlay
FROM python-base as s6-base

ENV \
    PS1="$(whoami)@$(hostname):$(pwd)$ " \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_CMD_WAIT_FOR_SERVICES=1 \
    TERM="xterm-256color"

ARG S6_OVERLAY_VERSION=3.1.6.2

WORKDIR /s6

RUN set -eux \
    && echo "Installing s6 build time packages" \
      && apk add --no-cache --virtual .s6-temp-deps \
        curl \
        outils-sha256 \
    && echo "Installing s6-overlay" \
      && curl --fail --silent --show-error --location --output s6-overlay-noarch.tar.xz  "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz" \
      && curl --fail --silent --show-error --location --output s6-overlay-noarch.tar.xz.sha256 "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz.sha256" \
      && curl --fail --silent --show-error --location --output s6-overlay-x86_64.tar.xz "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz" \
      && curl --fail --silent --show-error --location --output s6-overlay-x86_64.tar.xz.sha256 "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz.sha256" \
      && ls -ahl . \
      && echo "Validating s6-archives" \
        && sha256sum -c ./*.sha256 \
      && echo "Unpacking archives" \
        && tar -C / -Jxpf s6-overlay-noarch.tar.xz \
        && tar -C / -Jxpf s6-overlay-x86_64.tar.xz \
      && echo "Removing downloaded archives" \
        && rm ./*.tar.xz \
        && rm ./*.sha256 \
    && echo "Cleaning up image" \
      && apk del --no-cache --purge .s6-temp-deps

COPY ./rootfs /

# Stage: main-app
# Purpose: The final image
FROM s6-base as main-app

WORKDIR /app/

ARG SYSTEM_PKGS="redis \
                 mkvtoolnix \
                 ffmpeg"

RUN set -eux \
    && echo "Create user cleaner" \
      && addgroup --gid 1000 cleaner \
      && adduser --home /app/ --disabled-password --uid 1000 --shell /sbin/nologin --ingroup cleaner cleaner \
    && echo "Installing system packages" \
      && apk add --no-cache ${SYSTEM_PKGS}

COPY --chown=cleaner:cleaner --from=poetry-base /pipenv/requirements.txt ./

# hadolint ignore=DL3042
RUN --mount=type=cache,target=/root/.cache/pip/,id=pip-cache \
    set -eux \
    && echo "Installing Python requirements" \
      && pip cache info \
      && python3 -m pip install --default-timeout=1000 --requirement requirements.txt

COPY --chown=cleaner:cleaner ./app /app/

EXPOSE 8000

ENTRYPOINT ["/init"]
