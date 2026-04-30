# EE-cal — Electrical Engineering Calculator

A simple Streamlit web app that solves common electrical-engineering formulas.
Pick a formula, fill in known values, leave **exactly one** field blank, then
click **Solve missing variable**.

The library covers Year 1 → Year 4 topics, including:

- Ohm's law, electrical power, capacitor charge, energy
- Inductive / capacitive reactance, resonance
- Series & parallel resistance, voltage divider, transformer ratio
- Three-phase power, synchronous speed, amplifier gain
- Series RLC impedance, RL / RC time constants
- Battery runtime, load resistance & current

## 🌐 Live demo

> **TODO:** paste your Streamlit Community Cloud URL here after deploying.
> e.g. `https://eaikung-ee-cal.streamlit.app`

## ▶️ Run online (no install)

Just open the **Live demo** link above. It works in any modern browser,
including mobile.

## 🐍 Run locally with Python

Requires Python 3.10 or newer.

```bash
git clone https://github.com/Eaikung/EE-cal.git
cd EE-cal
pip install -r requirements.txt
streamlit run app.py
```

Then open <http://localhost:8501> in your browser.

## 🐳 Run with Docker

```bash
git clone https://github.com/Eaikung/EE-cal.git
cd EE-cal
docker compose -f docker-compose.web.yml up --build
```

Then open <http://localhost:8501>.

## 🖥️ Desktop GUI (Tkinter, alternative)

The repo also ships a Tkinter desktop version (`engineering_calculator.py`)
for users who prefer an offline native app:

```bash
python engineering_calculator.py
```

For a containerised desktop variant (Docker + XQuartz on macOS), see
[`ENGINEERING_DOCKER.md`](ENGINEERING_DOCKER.md).

## 📁 Repository layout

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit web UI (the main app) |
| `engineering_calculator.py` | Tkinter desktop UI (offline alternative) |
| `requirements.txt` | Python dependencies for the Streamlit app |
| `Dockerfile` | Container image for the web app |
| `docker-compose.web.yml` | Compose file for the web app |
| `Dockerfile.engineering` | Container image for the desktop app |
| `docker-compose.engineering.yml` | Compose file for the desktop app |
| `ENGINEERING_DOCKER.md` | Notes on running the desktop app via Docker |

## 📝 License

Educational / personal use.
