FROM node:18-bookworm-slim

ARG KILO_VERSION=latest

ENV DEBIAN_FRONTEND=noninteractive \
    HOME=/home/kilo \
    KILO_STATE_DIR=/home/kilo/.local/state/kilo \
    XDG_CONFIG_HOME=/home/kilo/.config \
    XDG_DATA_HOME=/home/kilo/.local/share \
    XDG_CACHE_HOME=/home/kilo/.cache \
    XDG_STATE_HOME=/home/kilo/.local/state \
    NODE_ENV=production \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    openssh-client \
    procps \
    ripgrep \
    tini \
    python3 \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -o -u 1000 -s /bin/bash kilo

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

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/kilo-entrypoint"]
CMD ["kilo"]
