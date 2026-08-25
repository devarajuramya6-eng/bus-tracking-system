# Dependencies

This project relies on the following technologies and libraries:

## Backend

*   **Python**: Version 3.9+ recommended.
*   **Package Manager**: `pip`.
*   **Manifest**: `requirements.txt`.
*   **Lockfile**: `requirements.lock` (run `pip install -r requirements.lock` to install pinned dependencies).
*   **Frameworks & Libraries**:
    *   Flask (Web framework)
    *   Socket.IO (Real-time communication via Flask-SocketIO)
    *   Celery (Background task processing)
*   **Infrastructure**:
    *   PostgreSQL (Relational database)
    *   Redis (Message broker and caching)

## Frontend

*   **Framework**: Vanilla HTML, CSS, JavaScript (No Node/npm dependencies or build steps).
*   **Map Library**: Leaflet (loaded via CDN).
