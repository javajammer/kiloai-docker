# Kilo Docker

Docker image for Kilo Code with state mounted outside the image.

Author: Rizal

Docker Hub image: `siriesal/kiloai:latest`

## Quick Start

```bash
git clone <this-repo>
cd kilo-docker
docker compose build
docker compose run --rm kilo
```

If you only want to run the published image:

```bash
docker pull siriesal/kiloai:latest
```

## What This Is

This image lets you run Kilo Code in Docker while keeping config, model settings, profiles, sessions, and local state in a separate host folder. The image stays reusable, and your data can move to another machine without rebuilding everything from scratch.

## Requirements

- Docker
- Docker Compose
- Git
- Internet access for first image pull/build and model login

## Folder Layout

All persistent data lives under `./state/`:

- `state/config/kilo/` - main Kilo config
- `state/config/kilo/kilo.jsonc` - base config without credentials
- `state/config/kilo/skills/` - existing Kilo skills copied from the local setup
- `state/config/nvm/kilo.json` - Kilo runtime config, including skill paths
- `state/models/opencode.json` - model/provider config without credentials
- `state/profiles/` - profile files
- `state/data/kilo/` - Kilo local data
- `state/data/kilo/auth.json` - auth placeholder
- `state/data/kilo/mcp-auth.json` - MCP auth placeholder
- `state/data/kilo/telemetry-id` - local telemetry id
- `state/state/kilo/` - local state
- `state/cache/kilo/` - cache
- `state/sessions/` - sessions
- `state/logs/` - logs

The repo already ships with empty placeholder files so the first boot works without copying old credentials.

## Setup

1. Clone this repo.
2. Make sure Docker and Docker Compose are installed.
3. Keep the `state/` folder with this repo, or mount it from another location.
4. Build the image:

```bash
docker compose build
```

5. Start Kilo:

```bash
docker compose run --rm kilo
```

6. The first run creates local Kilo state in `state/` and opens the TUI.

## Publish To Docker Hub

```bash
docker tag kilo-code:latest siriesal/kiloai:latest
docker push siriesal/kiloai:latest
```

To update the published image after changes:

```bash
docker build -t kilo-code:latest .
docker tag kilo-code:latest siriesal/kiloai:latest
docker push siriesal/kiloai:latest
```

## Configuration

Edit these files to customize Kilo:

- `state/config/kilo/kilo.jsonc` - permissions and MCP settings
- `state/config/nvm/kilo.json` - runtime config
- `state/models/opencode.json` - model/provider settings

If you want to use a different model, change `state/models/opencode.json`.
If you want to change permissions or MCP servers, edit `state/config/kilo/kilo.jsonc`.
If you want to add or edit reusable skills, place them under `state/config/kilo/skills/`.

### Important Files

- `state/config/kilo/kilo.jsonc` - permissions, MCP, and CLI rules
- `state/config/kilo/kilo.json` - optional extra config if you add it later
- `state/config/nvm/kilo.json` - runtime discovery config
- `state/models/opencode.json` - model selection and provider settings
- `state/data/kilo/auth.json` - auth data placeholder
- `state/data/kilo/mcp-auth.json` - MCP auth placeholder
- `state/data/kilo/telemetry-id` - local telemetry identity

## Usage

Run the TUI:

```bash
docker compose run --rm kilo
```

Run a command:

```bash
docker compose run --rm kilo kilo --help
docker compose run --rm kilo kilo run "hello world"
```

Use a specific model:

```bash
docker compose run --rm kilo kilo run -m kilo/kilo-auto/free "Reply with exactly: hello world"
```

Open a shell inside the container:

```bash
docker compose run --rm kilo bash
```

Check config:

```bash
docker compose run --rm kilo kilo config check
```

List models:

```bash
docker compose run --rm kilo kilo models
```

### Direct Docker Run

If you do not want Docker Compose, use Docker directly:

```bash
docker run --rm -it \
  --name kiloai \
  -e HOME=/home/kilo \
  -e KILO_STATE_DIR=/home/kilo/.local/state/kilo \
  -e XDG_CONFIG_HOME=/home/kilo/.config \
  -e XDG_DATA_HOME=/home/kilo/.local/share \
  -e XDG_CACHE_HOME=/home/kilo/.cache \
  -e XDG_STATE_HOME=/home/kilo/.local/state \
  -v "$(pwd)/state/config/kilo:/home/kilo/.config/kilo" \
  -v "$(pwd)/state/config/nvm/kilo.json:/home/kilo/.nvm/kilo.json" \
  -v "$(pwd)/state/models/opencode.json:/home/kilo/.config/kilo/opencode.json" \
  -v "$(pwd)/state/profiles:/home/kilo/.config/kilo/profiles" \
  -v "$(pwd)/state/data/kilo:/home/kilo/.local/share/kilo" \
  -v "$(pwd)/state/state/kilo:/home/kilo/.local/state/kilo" \
  -v "$(pwd)/state/data/kilo/auth.json:/home/kilo/.local/share/kilo/auth.json" \
  -v "$(pwd)/state/data/kilo/mcp-auth.json:/home/kilo/.local/share/kilo/mcp-auth.json" \
  -v "$(pwd)/state/data/kilo/telemetry-id:/home/kilo/.local/share/kilo/telemetry-id" \
  -v "$(pwd)/state/cache/kilo:/home/kilo/.cache/kilo" \
  -v "$(pwd)/state/sessions:/home/kilo/.local/share/kilo/sessions" \
  -v "$(pwd)/state/logs:/home/kilo/.local/share/kilo/logs" \
  -v "$(pwd)/workspace:/workspace" \
  siriesal/kiloai:latest
```

## Customize For Your Machine

If you want a different host path, edit the bind mounts in `docker-compose.yml`.

If you do not want to use compose, run the image directly and mount the same files/folders into:

- `/home/kilo/.config/kilo`
- `/home/kilo/.nvm/kilo.json`
- `/home/kilo/.local/share/kilo`
- `/home/kilo/.local/state/kilo`
- `/home/kilo/.cache/kilo`

## Migrate To Another Computer

1. Copy the repo.
2. Copy the `state/` folder.
3. Run `docker pull siriesal/kiloai:latest` or rebuild locally.
4. Start the container.

No credentials are baked into the image, so the same `state/` folder can be reused on another machine.

## First Login Flow

1. Start the container.
2. Open `kilo auth login` inside the container.
3. Complete provider login in the browser or terminal flow.
4. The resulting auth data is stored in `state/data/kilo/`.

## Troubleshooting

- If Kilo says a directory is missing, make sure the matching folder exists in `state/`.
- If the container cannot write state, check host file permissions.
- If your model list is empty, verify `state/models/opencode.json` and your provider login.
- If you move machines, copy the full `state/` folder, not only `state/config/`.

## Notes

- Do not commit real credentials into public git repositories.
- Keep `state/` private if it contains secrets.
- The image is designed to be portable, but your config files are still your responsibility.
- Replace `siriesal/kiloai:latest` with your own Docker Hub namespace if you fork this project.
