# EE-cal — Engineering Calculator

A Streamlit web app that solves the formulas an electrical-engineering student
meets across the curriculum. Pick a category, choose a formula, fill in the
values you know, leave **exactly one** field blank, then click **Solve**.

**70+ formulas across 11 categories**, organised by topic so you can find
what you need fast:

| Category | Examples |
| --- | --- |
| **Mathematics** | Pythagorean theorem, polar magnitude, log/ln |
| **Mechanics** | F=ma, kinetic & potential energy, momentum, pressure |
| **Heat & Thermodynamics** | Q=mcΔT, latent heat, ideal gas law, expansion |
| **DC Circuits** | Ohm's law, power dissipation (I²R / V²/R), dividers |
| **AC Circuits** | Reactance, RLC impedance, RMS↔peak, phase angle, P/Q/S |
| **Electromagnetics** | Magnetic flux, F=BIL, F=qvB, stored energy, Faraday |
| **Power Systems** | 3-phase, transformer turns, per-unit, voltage regulation |
| **Electronics** | Op-amp gains (inverting / non-inverting), LED resistor |
| **Control Systems** | RC / RL τ, settling time, first-order bandwidth |
| **Signals & Communications** | λ=c/f, dB (P&V), Shannon, Nyquist, ¼-wave antenna |
| **Digital Systems** | Bits ↔ levels, bytes, bit time |

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
