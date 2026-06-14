FROM dhi.io/node:26-alpine-sfw-ent-dev

ARG KILO_VERSION=latest

ENV HOME=/home/kilo \
    KILO_STATE_DIR=/home/kilo/.local/state/kilo \
    XDG_CONFIG_HOME=/home/kilo/.config \
    XDG_DATA_HOME=/home/kilo/.local/share \
    XDG_CACHE_HOME=/home/kilo/.cache \
    XDG_STATE_HOME=/home/kilo/.local/state \
    NODE_ENV=production \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

LABEL org.opencontainers.image.source=https://github.com/javajammer/kiloai-docker
LABEL org.opencontainers.image.description="kiloai on top docker"
LABEL org.opencontainers.image.licenses=MIT

RUN apk add --no-cache \
    ca-certificates \
    curl \
    git \
    openssh-client \
    procps \
    ripgrep \
    tini \
    python3 \
    bash

RUN adduser -D -s /bin/bash kilo || true

RUN mkdir -p \
    /home/kilo/.config/kilo \
    /home/kilo/.local/share/kilo \
    /home/kilo/.local/state \
    /home/kilo/.cache/kilo \
    /home/kilo/.nvm \
  && chown -R kilo:kilo /home/kilo

RUN npm install -g "@kilocode/cli@${KILO_VERSION}" \
  && npm cache clean --force

COPY entrypoint.sh /usr/local/bin/kilo-entrypoint
RUN chmod +x /usr/local/bin/kilo-entrypoint

USER kilo
WORKDIR /workspace

ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/kilo-entrypoint"]
CMD ["kilo"]
