# Run Engineering Calculator in Docker

This project already has a root `Dockerfile` for another app.  
Use these files for the Tkinter calculator:

- `Dockerfile.engineering`
- `docker-compose.engineering.yml`

## 1) One-time setup on macOS (for GUI)

1. Install and open XQuartz.
2. In XQuartz settings, enable:
   - **Allow connections from network clients**
3. Restart XQuartz.
4. In Terminal, run:

```bash
xhost + 127.0.0.1
```

## 2) Build and run

```bash
docker compose -f docker-compose.engineering.yml up --build
```

The calculator window should open via XQuartz.

## 3) Stop

Press `Ctrl+C` in the compose terminal, then:

```bash
docker compose -f docker-compose.engineering.yml down
```
