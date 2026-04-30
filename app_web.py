#!/usr/bin/env python3
"""Electrical engineering calculator web UI."""

from __future__ import annotations

import math

import streamlit as st

FORMULAS = {
    "[Year 1] Ohm's Law (V = I*R)": {
        "year": "Year 1",
        "variables": [("Voltage V (V)", "V"), ("Current I (A)", "I"), ("Resistance R (ohm)", "R")],
        "solve": {
            "V": lambda d: d["I"] * d["R"],
            "I": lambda d: d["V"] / d["R"] if d["R"] != 0 else (_ for _ in ()).throw(ValueError("Resistance cannot be zero.")),
            "R": lambda d: d["V"] / d["I"] if d["I"] != 0 else (_ for _ in ()).throw(ValueError("Current cannot be zero.")),
        },
    },
    "[Year 1] Electrical Power (P = V*I)": {
        "year": "Year 1",
        "variables": [("Power P (W)", "P"), ("Voltage V (V)", "V"), ("Current I (A)", "I")],
        "solve": {
            "P": lambda d: d["V"] * d["I"],
            "V": lambda d: d["P"] / d["I"] if d["I"] != 0 else (_ for _ in ()).throw(ValueError("Current cannot be zero.")),
            "I": lambda d: d["P"] / d["V"] if d["V"] != 0 else (_ for _ in ()).throw(ValueError("Voltage cannot be zero.")),
        },
    },
    "[Year 1] Capacitor Charge (Q = C*V)": {
        "year": "Year 1",
        "variables": [("Charge Q (C)", "Q"), ("Capacitance C (F)", "C"), ("Voltage V (V)", "V")],
        "solve": {
            "Q": lambda d: d["C"] * d["V"],
            "C": lambda d: d["Q"] / d["V"] if d["V"] != 0 else (_ for _ in ()).throw(ValueError("Voltage cannot be zero.")),
            "V": lambda d: d["Q"] / d["C"] if d["C"] != 0 else (_ for _ in ()).throw(ValueError("Capacitance cannot be zero.")),
        },
    },
    "[Year 1] Energy (E = P*t)": {
        "year": "Year 1",
        "variables": [("Energy E (J)", "E"), ("Power P (W)", "P"), ("Time t (s)", "t")],
        "solve": {
            "E": lambda d: d["P"] * d["t"],
            "P": lambda d: d["E"] / d["t"] if d["t"] != 0 else (_ for _ in ()).throw(ValueError("Time cannot be zero.")),
            "t": lambda d: d["E"] / d["P"] if d["P"] != 0 else (_ for _ in ()).throw(ValueError("Power cannot be zero.")),
        },
    },
    "[Year 2] Inductive Reactance (Xl = 2*pi*f*L)": {
        "year": "Year 2",
        "variables": [("Inductive reactance Xl (ohm)", "Xl"), ("Frequency f (Hz)", "f"), ("Inductance L (H)", "L")],
        "solve": {
            "Xl": lambda d: 2 * math.pi * d["f"] * d["L"],
            "f": lambda d: d["Xl"] / (2 * math.pi * d["L"]) if d["L"] != 0 else (_ for _ in ()).throw(ValueError("Inductance cannot be zero.")),
            "L": lambda d: d["Xl"] / (2 * math.pi * d["f"]) if d["f"] != 0 else (_ for _ in ()).throw(ValueError("Frequency cannot be zero.")),
        },
    },
    "[Year 2] Capacitive Reactance (Xc = 1/(2*pi*f*C))": {
        "year": "Year 2",
        "variables": [("Capacitive reactance Xc (ohm)", "Xc"), ("Frequency f (Hz)", "f"), ("Capacitance C (F)", "C")],
        "solve": {
            "Xc": lambda d: 1 / (2 * math.pi * d["f"] * d["C"]) if (d["f"] * d["C"]) != 0 else (_ for _ in ()).throw(ValueError("Frequency and capacitance must be non-zero.")),
            "f": lambda d: 1 / (2 * math.pi * d["Xc"] * d["C"]) if (d["Xc"] * d["C"]) != 0 else (_ for _ in ()).throw(ValueError("Xc and capacitance must be non-zero.")),
            "C": lambda d: 1 / (2 * math.pi * d["f"] * d["Xc"]) if (d["f"] * d["Xc"]) != 0 else (_ for _ in ()).throw(ValueError("Frequency and Xc must be non-zero.")),
        },
    },
    "[Year 2] Resonance (f0 = 1/(2*pi*sqrt(L*C)))": {
        "year": "Year 2",
        "variables": [("Resonant frequency f0 (Hz)", "f0"), ("Inductance L (H)", "L"), ("Capacitance C (F)", "C")],
        "solve": {
            "f0": lambda d: 1 / (2 * math.pi * math.sqrt(d["L"] * d["C"])) if (d["L"] > 0 and d["C"] > 0) else (_ for _ in ()).throw(ValueError("L and C must be positive.")),
            "L": lambda d: 1 / (((2 * math.pi * d["f0"]) ** 2) * d["C"]) if (d["f0"] > 0 and d["C"] > 0) else (_ for _ in ()).throw(ValueError("f0 and C must be positive.")),
            "C": lambda d: 1 / (((2 * math.pi * d["f0"]) ** 2) * d["L"]) if (d["f0"] > 0 and d["L"] > 0) else (_ for _ in ()).throw(ValueError("f0 and L must be positive.")),
        },
    },
    "[Year 2] Series Resistance (Req = R1 + R2)": {
        "year": "Year 2",
        "variables": [("Equivalent resistance Req (ohm)", "Req"), ("Resistor R1 (ohm)", "R1"), ("Resistor R2 (ohm)", "R2")],
        "solve": {
            "Req": lambda d: d["R1"] + d["R2"],
            "R1": lambda d: d["Req"] - d["R2"],
            "R2": lambda d: d["Req"] - d["R1"],
        },
    },
    "[Year 2] Parallel Resistance (Req = 1/(1/R1 + 1/R2))": {
        "year": "Year 2",
        "variables": [("Equivalent resistance Req (ohm)", "Req"), ("Resistor R1 (ohm)", "R1"), ("Resistor R2 (ohm)", "R2")],
        "solve": {
            "Req": lambda d: 1 / ((1 / d["R1"]) + (1 / d["R2"])) if (d["R1"] != 0 and d["R2"] != 0) else (_ for _ in ()).throw(ValueError("R1 and R2 cannot be zero.")),
            "R1": lambda d: 1 / ((1 / d["Req"]) - (1 / d["R2"])) if (d["Req"] != 0 and d["R2"] != 0 and ((1 / d["Req"]) - (1 / d["R2"])) != 0) else (_ for _ in ()).throw(ValueError("Invalid Req/R2 combination.")),
            "R2": lambda d: 1 / ((1 / d["Req"]) - (1 / d["R1"])) if (d["Req"] != 0 and d["R1"] != 0 and ((1 / d["Req"]) - (1 / d["R1"])) != 0) else (_ for _ in ()).throw(ValueError("Invalid Req/R1 combination.")),
        },
    },
    "[Year 2] Voltage Divider (Vout = Vin*R2/(R1+R2))": {
        "year": "Year 2",
        "variables": [("Output voltage Vout (V)", "Vout"), ("Input voltage Vin (V)", "Vin"), ("Resistor R1 (ohm)", "R1"), ("Resistor R2 (ohm)", "R2")],
        "solve": {
            "Vout": lambda d: d["Vin"] * d["R2"] / (d["R1"] + d["R2"]) if (d["R1"] + d["R2"]) != 0 else (_ for _ in ()).throw(ValueError("R1 + R2 cannot be zero.")),
            "Vin": lambda d: d["Vout"] * (d["R1"] + d["R2"]) / d["R2"] if d["R2"] != 0 else (_ for _ in ()).throw(ValueError("R2 cannot be zero.")),
            "R1": lambda d: (d["Vin"] * d["R2"] / d["Vout"]) - d["R2"] if d["Vout"] != 0 else (_ for _ in ()).throw(ValueError("Vout cannot be zero.")),
            "R2": lambda d: (d["Vout"] * d["R1"]) / (d["Vin"] - d["Vout"]) if (d["Vin"] - d["Vout"]) != 0 else (_ for _ in ()).throw(ValueError("Vin - Vout cannot be zero.")),
        },
    },
    "[Year 2] Transformer Ratio (Vp/Vs = Np/Ns)": {
        "year": "Year 2",
        "variables": [
            ("Primary voltage Vp (V)", "Vp"),
            ("Secondary voltage Vs (V)", "Vs"),
            ("Primary turns Np", "Np"),
            ("Secondary turns Ns", "Ns"),
        ],
        "solve": {
            "Vp": lambda d: d["Vs"] * d["Np"] / d["Ns"] if d["Ns"] != 0 else (_ for _ in ()).throw(ValueError("Ns cannot be zero.")),
            "Vs": lambda d: d["Vp"] * d["Ns"] / d["Np"] if d["Np"] != 0 else (_ for _ in ()).throw(ValueError("Np cannot be zero.")),
            "Np": lambda d: d["Vp"] * d["Ns"] / d["Vs"] if d["Vs"] != 0 else (_ for _ in ()).throw(ValueError("Vs cannot be zero.")),
            "Ns": lambda d: d["Vs"] * d["Np"] / d["Vp"] if d["Vp"] != 0 else (_ for _ in ()).throw(ValueError("Vp cannot be zero.")),
        },
    },
    "[Year 3] Three-Phase Power (P = sqrt(3)*V*I*pf)": {
        "year": "Year 3",
        "variables": [("Power P (W)", "P"), ("Line voltage V (V)", "V"), ("Line current I (A)", "I"), ("Power factor pf", "pf")],
        "solve": {
            "P": lambda d: math.sqrt(3) * d["V"] * d["I"] * d["pf"],
            "V": lambda d: d["P"] / (math.sqrt(3) * d["I"] * d["pf"]) if (d["I"] * d["pf"]) != 0 else (_ for _ in ()).throw(ValueError("I and pf must be non-zero.")),
            "I": lambda d: d["P"] / (math.sqrt(3) * d["V"] * d["pf"]) if (d["V"] * d["pf"]) != 0 else (_ for _ in ()).throw(ValueError("V and pf must be non-zero.")),
            "pf": lambda d: d["P"] / (math.sqrt(3) * d["V"] * d["I"]) if (d["V"] * d["I"]) != 0 else (_ for _ in ()).throw(ValueError("V and I must be non-zero.")),
        },
    },
    "[Year 3] Synchronous Speed (Ns = 120*f/P)": {
        "year": "Year 3",
        "variables": [("Synchronous speed Ns (rpm)", "Ns"), ("Frequency f (Hz)", "f"), ("Poles P", "P")],
        "solve": {
            "Ns": lambda d: 120 * d["f"] / d["P"] if d["P"] != 0 else (_ for _ in ()).throw(ValueError("Poles cannot be zero.")),
            "f": lambda d: d["Ns"] * d["P"] / 120,
            "P": lambda d: 120 * d["f"] / d["Ns"] if d["Ns"] != 0 else (_ for _ in ()).throw(ValueError("Ns cannot be zero.")),
        },
    },
    "[Year 3] Amplifier Gain (Av = Vout/Vin)": {
        "year": "Year 3",
        "variables": [("Voltage gain Av", "Av"), ("Output voltage Vout (V)", "Vout"), ("Input voltage Vin (V)", "Vin")],
        "solve": {
            "Av": lambda d: d["Vout"] / d["Vin"] if d["Vin"] != 0 else (_ for _ in ()).throw(ValueError("Vin cannot be zero.")),
            "Vout": lambda d: d["Av"] * d["Vin"],
            "Vin": lambda d: d["Vout"] / d["Av"] if d["Av"] != 0 else (_ for _ in ()).throw(ValueError("Av cannot be zero.")),
        },
    },
    "[Year 3] Series RLC Impedance (Z = sqrt(R^2 + (Xl-Xc)^2))": {
        "year": "Year 3",
        "variables": [("Impedance magnitude Z (ohm)", "Z"), ("Resistance R (ohm)", "R"), ("Inductive reactance Xl (ohm)", "Xl"), ("Capacitive reactance Xc (ohm)", "Xc")],
        "solve": {
            "Z": lambda d: math.sqrt((d["R"] ** 2) + ((d["Xl"] - d["Xc"]) ** 2)),
            "R": lambda d: math.sqrt((d["Z"] ** 2) - ((d["Xl"] - d["Xc"]) ** 2)) if (d["Z"] ** 2) >= ((d["Xl"] - d["Xc"]) ** 2) else (_ for _ in ()).throw(ValueError("No real solution for R with these values.")),
            "Xl": lambda d: d["Xc"] + math.sqrt((d["Z"] ** 2) - (d["R"] ** 2)) if (d["Z"] ** 2) >= (d["R"] ** 2) else (_ for _ in ()).throw(ValueError("No real solution for Xl with these values.")),
            "Xc": lambda d: d["Xl"] - math.sqrt((d["Z"] ** 2) - (d["R"] ** 2)) if (d["Z"] ** 2) >= (d["R"] ** 2) else (_ for _ in ()).throw(ValueError("No real solution for Xc with these values.")),
        },
    },
    "[Year 3] AC Current (I = V/Z)": {
        "year": "Year 3",
        "variables": [("Current I (A)", "I"), ("Voltage V (V)", "V"), ("Impedance Z (ohm)", "Z")],
        "solve": {
            "I": lambda d: d["V"] / d["Z"] if d["Z"] != 0 else (_ for _ in ()).throw(ValueError("Z cannot be zero.")),
            "V": lambda d: d["I"] * d["Z"],
            "Z": lambda d: d["V"] / d["I"] if d["I"] != 0 else (_ for _ in ()).throw(ValueError("I cannot be zero.")),
        },
    },
    "[Year 3] Apparent Power (S = V*I)": {
        "year": "Year 3",
        "variables": [("Apparent power S (VA)", "S"), ("Voltage V (V)", "V"), ("Current I (A)", "I")],
        "solve": {
            "S": lambda d: d["V"] * d["I"],
            "V": lambda d: d["S"] / d["I"] if d["I"] != 0 else (_ for _ in ()).throw(ValueError("I cannot be zero.")),
            "I": lambda d: d["S"] / d["V"] if d["V"] != 0 else (_ for _ in ()).throw(ValueError("V cannot be zero.")),
        },
    },
    "[Year 3] Power Factor (pf = P/S)": {
        "year": "Year 3",
        "variables": [("Power factor pf", "pf"), ("Real power P (W)", "P"), ("Apparent power S (VA)", "S")],
        "solve": {
            "pf": lambda d: d["P"] / d["S"] if d["S"] != 0 else (_ for _ in ()).throw(ValueError("S cannot be zero.")),
            "P": lambda d: d["pf"] * d["S"],
            "S": lambda d: d["P"] / d["pf"] if d["pf"] != 0 else (_ for _ in ()).throw(ValueError("pf cannot be zero.")),
        },
    },
    "[Year 3] Reactive Power (Q = V*I*sin(phi))": {
        "year": "Year 3",
        "variables": [("Reactive power Q (var)", "Q"), ("Voltage V (V)", "V"), ("Current I (A)", "I"), ("Phase angle phi (deg)", "phi")],
        "solve": {
            "Q": lambda d: d["V"] * d["I"] * math.sin(math.radians(d["phi"])),
            "V": lambda d: d["Q"] / (d["I"] * math.sin(math.radians(d["phi"]))) if (d["I"] * math.sin(math.radians(d["phi"]))) != 0 else (_ for _ in ()).throw(ValueError("I*sin(phi) cannot be zero.")),
            "I": lambda d: d["Q"] / (d["V"] * math.sin(math.radians(d["phi"]))) if (d["V"] * math.sin(math.radians(d["phi"]))) != 0 else (_ for _ in ()).throw(ValueError("V*sin(phi) cannot be zero.")),
            "phi": lambda d: math.degrees(math.asin(d["Q"] / (d["V"] * d["I"]))) if (d["V"] * d["I"]) != 0 and abs(d["Q"] / (d["V"] * d["I"])) <= 1 else (_ for _ in ()).throw(ValueError("Q/(V*I) must be between -1 and 1.")),
        },
    },
    "[Year 4] Efficiency (eta = Pout/Pin)": {
        "year": "Year 4",
        "variables": [("Efficiency eta (0..1)", "eta"), ("Output power Pout (W)", "Pout"), ("Input power Pin (W)", "Pin")],
        "solve": {
            "eta": lambda d: d["Pout"] / d["Pin"] if d["Pin"] != 0 else (_ for _ in ()).throw(ValueError("Pin cannot be zero.")),
            "Pout": lambda d: d["eta"] * d["Pin"],
            "Pin": lambda d: d["Pout"] / d["eta"] if d["eta"] != 0 else (_ for _ in ()).throw(ValueError("eta cannot be zero.")),
        },
    },
    "[Year 4] Battery Runtime (t = Capacity/I)": {
        "year": "Year 4",
        "variables": [("Runtime t (h)", "t"), ("Capacity (Ah)", "Capacity"), ("Current I (A)", "I")],
        "solve": {
            "t": lambda d: d["Capacity"] / d["I"] if d["I"] != 0 else (_ for _ in ()).throw(ValueError("Current cannot be zero.")),
            "Capacity": lambda d: d["t"] * d["I"],
            "I": lambda d: d["Capacity"] / d["t"] if d["t"] != 0 else (_ for _ in ()).throw(ValueError("Runtime cannot be zero.")),
        },
    },
    "[Year 4] RL Time Constant (tau = L/R)": {
        "year": "Year 4",
        "variables": [("Time constant tau (s)", "tau"), ("Inductance L (H)", "L"), ("Resistance R (ohm)", "R")],
        "solve": {
            "tau": lambda d: d["L"] / d["R"] if d["R"] != 0 else (_ for _ in ()).throw(ValueError("Resistance cannot be zero.")),
            "L": lambda d: d["tau"] * d["R"],
            "R": lambda d: d["L"] / d["tau"] if d["tau"] != 0 else (_ for _ in ()).throw(ValueError("tau cannot be zero.")),
        },
    },
    "[Year 4] Load Resistance (R = V^2/P)": {
        "year": "Year 4",
        "variables": [("Load resistance R (ohm)", "R"), ("Voltage V (V)", "V"), ("Power P (W)", "P")],
        "solve": {
            "R": lambda d: (d["V"] ** 2) / d["P"] if d["P"] != 0 else (_ for _ in ()).throw(ValueError("Power cannot be zero.")),
            "V": lambda d: math.sqrt(d["R"] * d["P"]) if d["R"] * d["P"] >= 0 else (_ for _ in ()).throw(ValueError("R*P must be non-negative.")),
            "P": lambda d: (d["V"] ** 2) / d["R"] if d["R"] != 0 else (_ for _ in ()).throw(ValueError("R cannot be zero.")),
        },
    },
    "[Year 4] Load Current (I = P/V)": {
        "year": "Year 4",
        "variables": [("Load current I (A)", "I"), ("Power P (W)", "P"), ("Voltage V (V)", "V")],
        "solve": {
            "I": lambda d: d["P"] / d["V"] if d["V"] != 0 else (_ for _ in ()).throw(ValueError("V cannot be zero.")),
            "P": lambda d: d["I"] * d["V"],
            "V": lambda d: d["P"] / d["I"] if d["I"] != 0 else (_ for _ in ()).throw(ValueError("I cannot be zero.")),
        },
    },
}


def main() -> None:
    st.set_page_config(page_title="Electrical Engineering Calculator", page_icon="🧮", layout="centered")
    st.title("🧮 Electrical Engineering Calculator")
    st.caption("Fill known values, leave exactly one blank, then click Solve.")

    formula_name = st.selectbox("Choose formula", list(FORMULAS.keys()))
    formula = FORMULAS[formula_name]
    st.info(f"Recommended course level: {formula['year']}")

    state_key = f"fields::{formula_name}"
    if state_key not in st.session_state:
        st.session_state[state_key] = {key: "" for _, key in formula["variables"]}

    with st.form("solver_form", clear_on_submit=False):
        for label, key in formula["variables"]:
            st.session_state[state_key][key] = st.text_input(
                label,
                value=st.session_state[state_key].get(key, ""),
                key=f"{state_key}:{key}",
                placeholder="Leave blank for unknown",
            )
        col1, col2 = st.columns([1, 1])
        solve_clicked = col1.form_submit_button("Solve missing variable", type="primary")
        reset_clicked = col2.form_submit_button("Reset fields")

    if reset_clicked:
        st.session_state[state_key] = {key: "" for _, key in formula["variables"]}
        st.rerun()

    if solve_clicked:
        try:
            values: dict[str, float] = {}
            missing: list[str] = []
            for _, key in formula["variables"]:
                raw = st.session_state[state_key][key].strip()
                if raw == "":
                    missing.append(key)
                else:
                    values[key] = float(raw)

            if len(missing) != 1:
                raise ValueError("Please leave exactly one field blank.")

            target = missing[0]
            solve_fn = formula["solve"].get(target)
            if solve_fn is None:
                raise ValueError(f"This formula cannot solve for {target}.")

            result = solve_fn(values)
            st.session_state[state_key][target] = f"{result:.6g}"
            solved_label = next(label for label, key in formula["variables"] if key == target)
            st.success(f"Solved {solved_label}: {result:.6g}")
        except ValueError as exc:
            st.error(str(exc))


if __name__ == "__main__":
    main()
