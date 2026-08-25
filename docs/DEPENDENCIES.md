# Dependency Documentation

## Python Environment
*   **Version:** Python 3 (from system environment)
*   **Package Manager:** pip
*   **Manifest:** `requirements.txt`
*   **Lockfile:** `requirements.lock`
*   **Backend Installation:** `pip install -r requirements.txt`

## Core Technologies Used
*   **PostgreSQL:** Database adapter `psycopg2-binary` is used.
*   **Redis:** In-memory store `redis` is used.
*   **Socket.IO:** Real-time communications via `Flask-SocketIO` and `eventlet`.
*   **Docker:** Containerized setup utilizing `Dockerfile` and `docker-compose.yml`.
*   **Maps:** Frontend relies on Leaflet.js with OSM/Carto tiles for map rendering.

## Frontend Environment
*   No Node.js/npm dependencies are bundled or managed via `package.json`.
*   All frontend assets (CSS, JS) are vanilla implementations without a build step.
