# LoRaWAN Field Test API

A FastAPI-based backend service for managing and analyzing LoRaWAN field test data.

---

## 🚀 Features

- FastAPI server using Astral UV
- PostgreSQL-backed storage (via SQLModel)
- Dockerized for easy deployment
- Secure environment-variable-based config
- Nginx reverse proxy with HTTPS + basic auth
- Systemd unit for automatic startup on boot

---

## 🛠️ Requirements

- Docker + Docker Compose
- PostgreSQL server (remote)
- Python 3.13 (for local dev)

---

## 📦 Docker Deployment

### Option 1: Run Prebuilt Image from Docker Hub

Use this `docker-compose.yml`:

```yaml
services:
  api:
    image: dbwalker/lorawan-fieldtest:latest
    container_name: lorawan-api
    env_file:
      - .env
    ports:
      - "17560:17560"
```

Then run:

```bash
docker-compose build
docker-compose up -d
```

### Option 2: Build Locally

If you'd rather build the image from source, use the following for `docker-compose.yml`:

```yaml
services:
  api:
    build: .
    image: dbwalker/lorawan-fieldtest:latest
    container_name: tracker-api
    env_file:
      - .env
    ports:
      - "17560:17560"
```

```bash
docker-compose build
docker-compose up -d
```

## 🔐 Configuration

Create a `.env` file in the project root (excluded from the image via `.dockerignore`):

```env
POSTGRESQL_HOST=your-db-host
POSTGRESQL_USER=your-user
POSTGRESQL_PASSWD=your-strong-password
HELIUM_API_TOKEN=token-for-helium-api
```

A sample is distributed as `env.example`. You can copy `env.example` to `.env`, and edit.

Notes:

* `POSTGRESQL_HOST` must be a numeric **IPv4 address** (not a domain name)
* `HELIUM_API_TOKEN` is used for accessing the Helium REST API

## ⚙️ Optional: systemd Setup

To run the API at system boot, create this unit at `/etc/systemd/system/lorawan-fieldtest.service`:

```ini
[Unit]
Description=LoRaWAN Field Test API
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/lorawan-fieldtest/app
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
User=lorawan-fieldtest
Group=lorawan-fieldtest
Environment=HOME=/home/lorawan-fieldtest
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Then enable it with:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now lorawan-fieldtest
```

## 📚 API Docs

Once deployed, Swagger/OpenAPI docs are available at:

```http
https://your-domain/docs
```

## 🧪 Local Development (Optional)

To run the app locally:

```
uv sync
uv run app
```