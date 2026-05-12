#!/usr/bin/env python3
"""Engineering reference calculator.

A topical formula library covering subjects an electrical-engineering student
sees across the curriculum. Pick a category, then a formula, fill in the
known values, leave exactly one field blank, and Streamlit will solve for it.
"""

from __future__ import annotations

import math

import streamlit as st

# --- Constants used by some formulas ----------------------------------------

SPEED_OF_LIGHT = 299_792_458.0  # m/s
GRAVITY = 9.80665  # m/s²
GAS_CONSTANT = 8.314462618  # J/(mol·K)

# Imperial / SI length (common engineering tables)
IN_TO_M = 0.0254  # 1 in (definition)
FT_TO_M = 0.3048  # 1 ft = 12 in
MI_TO_M = 1609.0  # 1 mi ≈ 1609 m ≈ 1.609 km (table rounding; intl. mile is 1609.344 m)


# --- Categories shown in the order students typically encounter them --------

CATEGORY_ORDER = [
    "Mathematics",
    "Mechanics",
    "Heat & Thermodynamics",
    "DC Circuits",
    "AC Circuits",
    "Electromagnetics",
    "Power Systems",
    "Electronics",
    "Control Systems",
    "Signals & Communications",
    "Digital Systems",
]


# --- Tiny helpers so the lambdas below stay readable ------------------------


def _err(msg: str):
    raise ValueError(msg)


def _div(a: float, b: float, msg: str) -> float:
    if b == 0:
        raise ValueError(msg)
    return a / b


def _sqrt(x: float, msg: str = "Value under the square root must be ≥ 0.") -> float:
    if x < 0:
        raise ValueError(msg)
    return math.sqrt(x)


def _log10(x: float) -> float:
    if x <= 0:
        raise ValueError("Argument of log10 must be > 0.")
    return math.log10(x)


def _ln(x: float) -> float:
    if x <= 0:
        raise ValueError("Argument of ln must be > 0.")
    return math.log(x)


def _log2(x: float) -> float:
    if x <= 0:
        raise ValueError("Argument of log2 must be > 0.")
    return math.log2(x)


def _tan_deg(x_deg: float) -> float:
    if math.cos(math.radians(x_deg)) == 0:
        raise ValueError("tan is undefined at this angle (cos = 0).")
    return math.tan(math.radians(x_deg))


def _atan_deg(x: float) -> float:
    return math.degrees(math.atan(x))


# --- Formulas ---------------------------------------------------------------

FORMULAS: dict[str, dict] = {
    # ============================================================
    # Mathematics
    # ============================================================
    "Pythagorean theorem (c² = a² + b²)": {
        "category": "Mathematics",
        "year": "Year 1",
        "variables": [
            ("Hypotenuse c", "c"),
            ("Side a", "a"),
            ("Side b", "b"),
        ],
        "solve": {
            "c": lambda d: _sqrt(d["a"] ** 2 + d["b"] ** 2),
            "a": lambda d: _sqrt(d["c"] ** 2 - d["b"] ** 2, "c must be ≥ b."),
            "b": lambda d: _sqrt(d["c"] ** 2 - d["a"] ** 2, "c must be ≥ a."),
        },
    },
    "Triangle area (A = ½·b·h)": {
        "category": "Mathematics",
        "year": "Year 1",
        "variables": [
            ("Area A", "A"),
            ("Base b", "b"),
            ("Height h", "h"),
        ],
        "solve": {
            "A": lambda d: 0.5 * d["b"] * d["h"],
            "b": lambda d: _div(2 * d["A"], d["h"], "Height cannot be 0."),
            "h": lambda d: _div(2 * d["A"], d["b"], "Base cannot be 0."),
        },
    },
    "Circle area (A = π·r²)": {
        "category": "Mathematics",
        "year": "Year 1",
        "variables": [
            ("Area A", "A"),
            ("Radius r", "r"),
        ],
        "solve": {
            "A": lambda d: math.pi * d["r"] ** 2,
            "r": lambda d: _sqrt(_div(d["A"], math.pi, "π is non-zero."), "Area must be ≥ 0."),
        },
    },
    "Circle circumference (C = 2π·r)": {
        "category": "Mathematics",
        "year": "Year 1",
        "variables": [
            ("Circumference C", "C"),
            ("Radius r", "r"),
        ],
        "solve": {
            "C": lambda d: 2 * math.pi * d["r"],
            "r": lambda d: d["C"] / (2 * math.pi),
        },
    },
    "Polar magnitude (r = √(x² + y²))": {
        "category": "Mathematics",
        "year": "Year 1",
        "variables": [
            ("Magnitude r", "r"),
            ("x component", "x"),
            ("y component", "y"),
        ],
        "solve": {
            "r": lambda d: _sqrt(d["x"] ** 2 + d["y"] ** 2),
            "x": lambda d: _sqrt(d["r"] ** 2 - d["y"] ** 2, "r must be ≥ |y|."),
            "y": lambda d: _sqrt(d["r"] ** 2 - d["x"] ** 2, "r must be ≥ |x|."),
        },
    },
    "Common logarithm (y = log₁₀ x)": {
        "category": "Mathematics",
        "year": "Year 1",
        "variables": [
            ("y = log10(x)", "y"),
            ("x (must be > 0)", "x"),
        ],
        "solve": {
            "y": lambda d: _log10(d["x"]),
            "x": lambda d: 10 ** d["y"],
        },
    },
    "Natural logarithm (y = ln x)": {
        "category": "Mathematics",
        "year": "Year 1",
        "variables": [
            ("y = ln(x)", "y"),
            ("x (must be > 0)", "x"),
        ],
        "solve": {
            "y": lambda d: _ln(d["x"]),
            "x": lambda d: math.exp(d["y"]),
        },
    },
    "Length: mile, meter, kilometer (1 mi ≈ 1609 m)": {
        "category": "Mathematics",
        "year": "Year 1",
        "variables": [
            ("Miles", "mi"),
            ("Meters m", "m"),
            ("Kilometers km", "km"),
        ],
        "solve": {
            "mi": lambda d: d["m"] / MI_TO_M if "m" in d else d["km"] * 1000.0 / MI_TO_M,
            "m": lambda d: d["mi"] * MI_TO_M if "mi" in d else d["km"] * 1000.0,
            "km": lambda d: d["m"] / 1000.0 if "m" in d else d["mi"] * MI_TO_M / 1000.0,
        },
    },
    "Length: foot, meter, centimeter (1 ft = 0.3048 m)": {
        "category": "Mathematics",
        "year": "Year 1",
        "variables": [
            ("Feet ft", "ft"),
            ("Meters m", "m"),
            ("Centimeters cm", "cm"),
        ],
        "solve": {
            "ft": lambda d: d["m"] / FT_TO_M if "m" in d else d["cm"] / (100.0 * FT_TO_M),
            "m": lambda d: d["ft"] * FT_TO_M if "ft" in d else d["cm"] / 100.0,
            "cm": lambda d: d["m"] * 100.0 if "m" in d else d["ft"] * FT_TO_M * 100.0,
        },
    },
    "Length: meter, inch, foot (1 m ≈ 39.37 in ≈ 3.281 ft)": {
        "category": "Mathematics",
        "year": "Year 1",
        "variables": [
            ("Meters m", "m"),
            ("Inches", "inch"),
            ("Feet ft", "ft"),
        ],
        "solve": {
            "m": lambda d: d["inch"] * IN_TO_M if "inch" in d else d["ft"] * FT_TO_M,
            "inch": lambda d: d["m"] / IN_TO_M if "m" in d else d["ft"] * FT_TO_M / IN_TO_M,
            "ft": lambda d: d["m"] / FT_TO_M if "m" in d else d["inch"] * IN_TO_M / FT_TO_M,
        },
    },
    "Length: inch, meter, centimeter (1 in = 0.0254 m = 2.54 cm)": {
        "category": "Mathematics",
        "year": "Year 1",
        "variables": [
            ("Inches", "inch"),
            ("Meters m", "m"),
            ("Centimeters cm", "cm"),
        ],
        "solve": {
            "inch": lambda d: d["m"] / IN_TO_M if "m" in d else d["cm"] / (100.0 * IN_TO_M),
            "m": lambda d: d["inch"] * IN_TO_M if "inch" in d else d["cm"] / 100.0,
            "cm": lambda d: d["m"] * 100.0 if "m" in d else d["inch"] * IN_TO_M * 100.0,
        },
    },
    # ============================================================
    # Mechanics (Year 1 physics)
    # ============================================================
    "Final velocity (v = u + a·t)": {
        "category": "Mechanics",
        "year": "Year 1",
        "variables": [
            ("Final velocity v (m/s)", "v"),
            ("Initial velocity u (m/s)", "u"),
            ("Acceleration a (m/s²)", "a"),
            ("Time t (s)", "t"),
        ],
        "solve": {
            "v": lambda d: d["u"] + d["a"] * d["t"],
            "u": lambda d: d["v"] - d["a"] * d["t"],
            "a": lambda d: _div(d["v"] - d["u"], d["t"], "Time cannot be 0."),
            "t": lambda d: _div(d["v"] - d["u"], d["a"], "Acceleration cannot be 0."),
        },
    },
    "Newton's 2nd Law (F = m·a)": {
        "category": "Mechanics",
        "year": "Year 1",
        "variables": [
            ("Force F (N)", "F"),
            ("Mass m (kg)", "m"),
            ("Acceleration a (m/s²)", "a"),
        ],
        "solve": {
            "F": lambda d: d["m"] * d["a"],
            "m": lambda d: _div(d["F"], d["a"], "Acceleration cannot be 0."),
            "a": lambda d: _div(d["F"], d["m"], "Mass cannot be 0."),
        },
    },
    "Weight (W = m·g)": {
        "category": "Mechanics",
        "year": "Year 1",
        "variables": [
            ("Weight W (N)", "W"),
            ("Mass m (kg)", "m"),
            ("Gravity g (m/s², ≈9.81)", "g"),
        ],
        "solve": {
            "W": lambda d: d["m"] * d["g"],
            "m": lambda d: _div(d["W"], d["g"], "Gravity cannot be 0."),
            "g": lambda d: _div(d["W"], d["m"], "Mass cannot be 0."),
        },
    },
    "Kinetic energy (Ek = ½·m·v²)": {
        "category": "Mechanics",
        "year": "Year 1",
        "variables": [
            ("Kinetic energy Ek (J)", "Ek"),
            ("Mass m (kg)", "m"),
            ("Speed v (m/s)", "v"),
        ],
        "solve": {
            "Ek": lambda d: 0.5 * d["m"] * d["v"] ** 2,
            "m": lambda d: _div(2 * d["Ek"], d["v"] ** 2, "Speed cannot be 0."),
            "v": lambda d: _sqrt(_div(2 * d["Ek"], d["m"], "Mass cannot be 0.")),
        },
    },
    "Potential energy (Ep = m·g·h)": {
        "category": "Mechanics",
        "year": "Year 1",
        "variables": [
            ("Potential energy Ep (J)", "Ep"),
            ("Mass m (kg)", "m"),
            ("Gravity g (m/s²)", "g"),
            ("Height h (m)", "h"),
        ],
        "solve": {
            "Ep": lambda d: d["m"] * d["g"] * d["h"],
            "m": lambda d: _div(d["Ep"], d["g"] * d["h"], "g and h must be non-zero."),
            "g": lambda d: _div(d["Ep"], d["m"] * d["h"], "m and h must be non-zero."),
            "h": lambda d: _div(d["Ep"], d["m"] * d["g"], "m and g must be non-zero."),
        },
    },
    "Linear momentum (p = m·v)": {
        "category": "Mechanics",
        "year": "Year 1",
        "variables": [
            ("Momentum p (kg·m/s)", "p"),
            ("Mass m (kg)", "m"),
            ("Velocity v (m/s)", "v"),
        ],
        "solve": {
            "p": lambda d: d["m"] * d["v"],
            "m": lambda d: _div(d["p"], d["v"], "Velocity cannot be 0."),
            "v": lambda d: _div(d["p"], d["m"], "Mass cannot be 0."),
        },
    },
    "Pressure (P = F/A)": {
        "category": "Mechanics",
        "year": "Year 1",
        "variables": [
            ("Pressure P (Pa)", "P"),
            ("Force F (N)", "F"),
            ("Area A (m²)", "A"),
        ],
        "solve": {
            "P": lambda d: _div(d["F"], d["A"], "Area cannot be 0."),
            "F": lambda d: d["P"] * d["A"],
            "A": lambda d: _div(d["F"], d["P"], "Pressure cannot be 0."),
        },
    },
    # ============================================================
    # Heat & Thermodynamics
    # ============================================================
    "Sensible heat (Q = m·c·ΔT)": {
        "category": "Heat & Thermodynamics",
        "year": "Year 2",
        "variables": [
            ("Heat Q (J)", "Q"),
            ("Mass m (kg)", "m"),
            ("Specific heat c (J/(kg·K))", "c"),
            ("Temperature change ΔT (K)", "dT"),
        ],
        "solve": {
            "Q": lambda d: d["m"] * d["c"] * d["dT"],
            "m": lambda d: _div(d["Q"], d["c"] * d["dT"], "c and ΔT must be non-zero."),
            "c": lambda d: _div(d["Q"], d["m"] * d["dT"], "m and ΔT must be non-zero."),
            "dT": lambda d: _div(d["Q"], d["m"] * d["c"], "m and c must be non-zero."),
        },
    },
    "Latent heat (Q = m·L)": {
        "category": "Heat & Thermodynamics",
        "year": "Year 2",
        "variables": [
            ("Heat Q (J)", "Q"),
            ("Mass m (kg)", "m"),
            ("Latent heat L (J/kg)", "L"),
        ],
        "solve": {
            "Q": lambda d: d["m"] * d["L"],
            "m": lambda d: _div(d["Q"], d["L"], "L cannot be 0."),
            "L": lambda d: _div(d["Q"], d["m"], "m cannot be 0."),
        },
    },
    "Ideal gas law (P·V = n·R·T)": {
        "category": "Heat & Thermodynamics",
        "year": "Year 2",
        "variables": [
            ("Pressure P (Pa)", "P"),
            ("Volume V (m³)", "V"),
            ("Moles n", "n"),
            ("Temperature T (K)", "T"),
        ],
        "solve": {
            "P": lambda d: _div(d["n"] * GAS_CONSTANT * d["T"], d["V"], "Volume cannot be 0."),
            "V": lambda d: _div(d["n"] * GAS_CONSTANT * d["T"], d["P"], "Pressure cannot be 0."),
            "n": lambda d: _div(d["P"] * d["V"], GAS_CONSTANT * d["T"], "Temperature cannot be 0."),
            "T": lambda d: _div(d["P"] * d["V"], d["n"] * GAS_CONSTANT, "n cannot be 0."),
        },
    },
    "Linear thermal expansion (ΔL = α·L₀·ΔT)": {
        "category": "Heat & Thermodynamics",
        "year": "Year 2",
        "variables": [
            ("Length change ΔL (m)", "dL"),
            ("Expansion coefficient α (1/K)", "alpha"),
            ("Original length L0 (m)", "L0"),
            ("Temperature change ΔT (K)", "dT"),
        ],
        "solve": {
            "dL": lambda d: d["alpha"] * d["L0"] * d["dT"],
            "alpha": lambda d: _div(d["dL"], d["L0"] * d["dT"], "L0 and ΔT must be non-zero."),
            "L0": lambda d: _div(d["dL"], d["alpha"] * d["dT"], "α and ΔT must be non-zero."),
            "dT": lambda d: _div(d["dL"], d["alpha"] * d["L0"], "α and L0 must be non-zero."),
        },
    },
    # ============================================================
    # DC Circuits
    # ============================================================
    "Ohm's Law (V = I·R)": {
        "category": "DC Circuits",
        "year": "Year 1",
        "variables": [
            ("Voltage V (V)", "V"),
            ("Current I (A)", "I"),
            ("Resistance R (Ω)", "R"),
        ],
        "solve": {
            "V": lambda d: d["I"] * d["R"],
            "I": lambda d: _div(d["V"], d["R"], "Resistance cannot be 0."),
            "R": lambda d: _div(d["V"], d["I"], "Current cannot be 0."),
        },
    },
    "Electrical power (P = V·I)": {
        "category": "DC Circuits",
        "year": "Year 1",
        "variables": [
            ("Power P (W)", "P"),
            ("Voltage V (V)", "V"),
            ("Current I (A)", "I"),
        ],
        "solve": {
            "P": lambda d: d["V"] * d["I"],
            "V": lambda d: _div(d["P"], d["I"], "Current cannot be 0."),
            "I": lambda d: _div(d["P"], d["V"], "Voltage cannot be 0."),
        },
    },
    "Power dissipation I²R (P = I²·R)": {
        "category": "DC Circuits",
        "year": "Year 1",
        "variables": [
            ("Power P (W)", "P"),
            ("Current I (A)", "I"),
            ("Resistance R (Ω)", "R"),
        ],
        "solve": {
            "P": lambda d: d["I"] ** 2 * d["R"],
            "I": lambda d: _sqrt(_div(d["P"], d["R"], "R cannot be 0.")),
            "R": lambda d: _div(d["P"], d["I"] ** 2, "I cannot be 0."),
        },
    },
    "Power dissipation V²/R (P = V²/R)": {
        "category": "DC Circuits",
        "year": "Year 1",
        "variables": [
            ("Power P (W)", "P"),
            ("Voltage V (V)", "V"),
            ("Resistance R (Ω)", "R"),
        ],
        "solve": {
            "P": lambda d: _div(d["V"] ** 2, d["R"], "R cannot be 0."),
            "V": lambda d: _sqrt(d["P"] * d["R"], "P·R must be ≥ 0."),
            "R": lambda d: _div(d["V"] ** 2, d["P"], "P cannot be 0."),
        },
    },
    "Capacitor charge (Q = C·V)": {
        "category": "DC Circuits",
        "year": "Year 1",
        "variables": [
            ("Charge Q (C)", "Q"),
            ("Capacitance C (F)", "C"),
            ("Voltage V (V)", "V"),
        ],
        "solve": {
            "Q": lambda d: d["C"] * d["V"],
            "C": lambda d: _div(d["Q"], d["V"], "Voltage cannot be 0."),
            "V": lambda d: _div(d["Q"], d["C"], "Capacitance cannot be 0."),
        },
    },
    "Energy from power (E = P·t)": {
        "category": "DC Circuits",
        "year": "Year 1",
        "variables": [
            ("Energy E (J)", "E"),
            ("Power P (W)", "P"),
            ("Time t (s)", "t"),
        ],
        "solve": {
            "E": lambda d: d["P"] * d["t"],
            "P": lambda d: _div(d["E"], d["t"], "Time cannot be 0."),
            "t": lambda d: _div(d["E"], d["P"], "Power cannot be 0."),
        },
    },
    "Series resistance (Req = R1 + R2)": {
        "category": "DC Circuits",
        "year": "Year 2",
        "variables": [
            ("Equivalent Req (Ω)", "Req"),
            ("R1 (Ω)", "R1"),
            ("R2 (Ω)", "R2"),
        ],
        "solve": {
            "Req": lambda d: d["R1"] + d["R2"],
            "R1": lambda d: d["Req"] - d["R2"],
            "R2": lambda d: d["Req"] - d["R1"],
        },
    },
    "Parallel resistance (Req = R1·R2 / (R1+R2))": {
        "category": "DC Circuits",
        "year": "Year 2",
        "variables": [
            ("Equivalent Req (Ω)", "Req"),
            ("R1 (Ω)", "R1"),
            ("R2 (Ω)", "R2"),
        ],
        "solve": {
            "Req": lambda d: _div(d["R1"] * d["R2"], d["R1"] + d["R2"], "R1+R2 cannot be 0."),
            "R1": lambda d: _div(d["Req"] * d["R2"], d["R2"] - d["Req"], "R2 must be > Req."),
            "R2": lambda d: _div(d["Req"] * d["R1"], d["R1"] - d["Req"], "R1 must be > Req."),
        },
    },
    "Voltage divider (Vout = Vin·R2/(R1+R2))": {
        "category": "DC Circuits",
        "year": "Year 2",
        "variables": [
            ("Output Vout (V)", "Vout"),
            ("Input Vin (V)", "Vin"),
            ("Top R1 (Ω)", "R1"),
            ("Bottom R2 (Ω)", "R2"),
        ],
        "solve": {
            "Vout": lambda d: _div(d["Vin"] * d["R2"], d["R1"] + d["R2"], "R1+R2 cannot be 0."),
            "Vin": lambda d: _div(d["Vout"] * (d["R1"] + d["R2"]), d["R2"], "R2 cannot be 0."),
            "R1": lambda d: _div(d["Vin"] * d["R2"], d["Vout"], "Vout cannot be 0.") - d["R2"],
            "R2": lambda d: _div(d["Vout"] * d["R1"], d["Vin"] - d["Vout"], "Vin-Vout cannot be 0."),
        },
    },
    "Load current (I = P/V)": {
        "category": "DC Circuits",
        "year": "Year 4",
        "variables": [
            ("Current I (A)", "I"),
            ("Power P (W)", "P"),
            ("Voltage V (V)", "V"),
        ],
        "solve": {
            "I": lambda d: _div(d["P"], d["V"], "V cannot be 0."),
            "P": lambda d: d["I"] * d["V"],
            "V": lambda d: _div(d["P"], d["I"], "I cannot be 0."),
        },
    },
    # ============================================================
    # AC Circuits
    # ============================================================
    "Inductive reactance (Xl = 2π·f·L)": {
        "category": "AC Circuits",
        "year": "Year 2",
        "variables": [
            ("Reactance Xl (Ω)", "Xl"),
            ("Frequency f (Hz)", "f"),
            ("Inductance L (H)", "L"),
        ],
        "solve": {
            "Xl": lambda d: 2 * math.pi * d["f"] * d["L"],
            "f": lambda d: _div(d["Xl"], 2 * math.pi * d["L"], "L cannot be 0."),
            "L": lambda d: _div(d["Xl"], 2 * math.pi * d["f"], "f cannot be 0."),
        },
    },
    "Capacitive reactance (Xc = 1/(2π·f·C))": {
        "category": "AC Circuits",
        "year": "Year 2",
        "variables": [
            ("Reactance Xc (Ω)", "Xc"),
            ("Frequency f (Hz)", "f"),
            ("Capacitance C (F)", "C"),
        ],
        "solve": {
            "Xc": lambda d: _div(1.0, 2 * math.pi * d["f"] * d["C"], "f·C cannot be 0."),
            "f": lambda d: _div(1.0, 2 * math.pi * d["Xc"] * d["C"], "Xc·C cannot be 0."),
            "C": lambda d: _div(1.0, 2 * math.pi * d["f"] * d["Xc"], "f·Xc cannot be 0."),
        },
    },
    "LC resonance (f0 = 1/(2π·√(L·C)))": {
        "category": "AC Circuits",
        "year": "Year 2",
        "variables": [
            ("Resonant frequency f0 (Hz)", "f0"),
            ("Inductance L (H)", "L"),
            ("Capacitance C (F)", "C"),
        ],
        "solve": {
            "f0": lambda d: _div(1.0, 2 * math.pi * _sqrt(d["L"] * d["C"], "L·C must be > 0."), "denominator 0."),
            "L": lambda d: _div(1.0, ((2 * math.pi * d["f0"]) ** 2) * d["C"], "f0·C cannot be 0."),
            "C": lambda d: _div(1.0, ((2 * math.pi * d["f0"]) ** 2) * d["L"], "f0·L cannot be 0."),
        },
    },
    "Series RLC impedance (Z = √(R² + (Xl-Xc)²))": {
        "category": "AC Circuits",
        "year": "Year 3",
        "variables": [
            ("Impedance Z (Ω)", "Z"),
            ("Resistance R (Ω)", "R"),
            ("Reactance Xl (Ω)", "Xl"),
            ("Reactance Xc (Ω)", "Xc"),
        ],
        "solve": {
            "Z": lambda d: _sqrt(d["R"] ** 2 + (d["Xl"] - d["Xc"]) ** 2),
            "R": lambda d: _sqrt(d["Z"] ** 2 - (d["Xl"] - d["Xc"]) ** 2, "Z must be ≥ |Xl-Xc|."),
            "Xl": lambda d: d["Xc"] + _sqrt(d["Z"] ** 2 - d["R"] ** 2, "Z must be ≥ R."),
            "Xc": lambda d: d["Xl"] - _sqrt(d["Z"] ** 2 - d["R"] ** 2, "Z must be ≥ R."),
        },
    },
    "AC current (I = V/Z)": {
        "category": "AC Circuits",
        "year": "Year 3",
        "variables": [
            ("Current I (A)", "I"),
            ("Voltage V (V)", "V"),
            ("Impedance Z (Ω)", "Z"),
        ],
        "solve": {
            "I": lambda d: _div(d["V"], d["Z"], "Z cannot be 0."),
            "V": lambda d: d["I"] * d["Z"],
            "Z": lambda d: _div(d["V"], d["I"], "I cannot be 0."),
        },
    },
    "RMS to peak (Vp = √2·Vrms)": {
        "category": "AC Circuits",
        "year": "Year 2",
        "variables": [
            ("Peak Vp (V)", "Vp"),
            ("RMS Vrms (V)", "Vrms"),
        ],
        "solve": {
            "Vp": lambda d: math.sqrt(2) * d["Vrms"],
            "Vrms": lambda d: d["Vp"] / math.sqrt(2),
        },
    },
    "Phase angle (φ° = atan(X/R))": {
        "category": "AC Circuits",
        "year": "Year 3",
        "variables": [
            ("Phase φ (degrees)", "phi"),
            ("Net reactance X (Ω)", "X"),
            ("Resistance R (Ω)", "R"),
        ],
        "solve": {
            "phi": lambda d: _atan_deg(_div(d["X"], d["R"], "R cannot be 0.")),
            "X": lambda d: d["R"] * _tan_deg(d["phi"]),
            "R": lambda d: _div(d["X"], _tan_deg(d["phi"]), "tan(φ) cannot be 0."),
        },
    },
    "Apparent power (S = V·I)": {
        "category": "AC Circuits",
        "year": "Year 3",
        "variables": [
            ("Apparent power S (VA)", "S"),
            ("Voltage V (V)", "V"),
            ("Current I (A)", "I"),
        ],
        "solve": {
            "S": lambda d: d["V"] * d["I"],
            "V": lambda d: _div(d["S"], d["I"], "Current cannot be 0."),
            "I": lambda d: _div(d["S"], d["V"], "Voltage cannot be 0."),
        },
    },
    "Power factor (pf = P/S)": {
        "category": "AC Circuits",
        "year": "Year 3",
        "variables": [
            ("Power factor pf", "pf"),
            ("Real power P (W)", "P"),
            ("Apparent power S (VA)", "S"),
        ],
        "solve": {
            "pf": lambda d: _div(d["P"], d["S"], "S cannot be 0."),
            "P": lambda d: d["pf"] * d["S"],
            "S": lambda d: _div(d["P"], d["pf"], "pf cannot be 0."),
        },
    },
    "Reactive power (Q = V·I·sin φ°)": {
        "category": "AC Circuits",
        "year": "Year 3",
        "variables": [
            ("Reactive power Q (VAR)", "Q"),
            ("Voltage V (V)", "V"),
            ("Current I (A)", "I"),
            ("Phase φ (degrees)", "phi"),
        ],
        "solve": {
            "Q": lambda d: d["V"] * d["I"] * math.sin(math.radians(d["phi"])),
            "V": lambda d: _div(d["Q"], d["I"] * math.sin(math.radians(d["phi"])), "I·sin(φ) cannot be 0."),
            "I": lambda d: _div(d["Q"], d["V"] * math.sin(math.radians(d["phi"])), "V·sin(φ) cannot be 0."),
            "phi": lambda d: math.degrees(math.asin(_div(d["Q"], d["V"] * d["I"], "V·I cannot be 0."))),
        },
    },
    # ============================================================
    # Electromagnetics
    # ============================================================
    "Magnetic flux (Φ = B·A)": {
        "category": "Electromagnetics",
        "year": "Year 2",
        "variables": [
            ("Flux Φ (Wb)", "Phi"),
            ("Flux density B (T)", "B"),
            ("Area A (m²)", "A"),
        ],
        "solve": {
            "Phi": lambda d: d["B"] * d["A"],
            "B": lambda d: _div(d["Phi"], d["A"], "A cannot be 0."),
            "A": lambda d: _div(d["Phi"], d["B"], "B cannot be 0."),
        },
    },
    "Force on current-carrying wire (F = B·I·L)": {
        "category": "Electromagnetics",
        "year": "Year 2",
        "variables": [
            ("Force F (N)", "F"),
            ("Flux density B (T)", "B"),
            ("Current I (A)", "I"),
            ("Length L (m)", "L"),
        ],
        "solve": {
            "F": lambda d: d["B"] * d["I"] * d["L"],
            "B": lambda d: _div(d["F"], d["I"] * d["L"], "I·L cannot be 0."),
            "I": lambda d: _div(d["F"], d["B"] * d["L"], "B·L cannot be 0."),
            "L": lambda d: _div(d["F"], d["B"] * d["I"], "B·I cannot be 0."),
        },
    },
    "Force on moving charge (F = q·v·B)": {
        "category": "Electromagnetics",
        "year": "Year 2",
        "variables": [
            ("Force F (N)", "F"),
            ("Charge q (C)", "q"),
            ("Velocity v (m/s)", "v"),
            ("Flux density B (T)", "B"),
        ],
        "solve": {
            "F": lambda d: d["q"] * d["v"] * d["B"],
            "q": lambda d: _div(d["F"], d["v"] * d["B"], "v·B cannot be 0."),
            "v": lambda d: _div(d["F"], d["q"] * d["B"], "q·B cannot be 0."),
            "B": lambda d: _div(d["F"], d["q"] * d["v"], "q·v cannot be 0."),
        },
    },
    "Inductor stored energy (W = ½·L·I²)": {
        "category": "Electromagnetics",
        "year": "Year 2",
        "variables": [
            ("Energy W (J)", "W"),
            ("Inductance L (H)", "L"),
            ("Current I (A)", "I"),
        ],
        "solve": {
            "W": lambda d: 0.5 * d["L"] * d["I"] ** 2,
            "L": lambda d: _div(2 * d["W"], d["I"] ** 2, "I cannot be 0."),
            "I": lambda d: _sqrt(_div(2 * d["W"], d["L"], "L cannot be 0.")),
        },
    },
    "Capacitor stored energy (W = ½·C·V²)": {
        "category": "Electromagnetics",
        "year": "Year 2",
        "variables": [
            ("Energy W (J)", "W"),
            ("Capacitance C (F)", "C"),
            ("Voltage V (V)", "V"),
        ],
        "solve": {
            "W": lambda d: 0.5 * d["C"] * d["V"] ** 2,
            "C": lambda d: _div(2 * d["W"], d["V"] ** 2, "V cannot be 0."),
            "V": lambda d: _sqrt(_div(2 * d["W"], d["C"], "C cannot be 0.")),
        },
    },
    "Faraday induced EMF magnitude (ε = N·ΔΦ/Δt)": {
        "category": "Electromagnetics",
        "year": "Year 3",
        "variables": [
            ("Induced EMF ε (V)", "emf"),
            ("Turns N", "N"),
            ("Flux change ΔΦ (Wb)", "dPhi"),
            ("Time interval Δt (s)", "dt"),
        ],
        "solve": {
            "emf": lambda d: _div(d["N"] * d["dPhi"], d["dt"], "Δt cannot be 0."),
            "N": lambda d: _div(d["emf"] * d["dt"], d["dPhi"], "ΔΦ cannot be 0."),
            "dPhi": lambda d: _div(d["emf"] * d["dt"], d["N"], "N cannot be 0."),
            "dt": lambda d: _div(d["N"] * d["dPhi"], d["emf"], "ε cannot be 0."),
        },
    },
    # ============================================================
    # Power Systems
    # ============================================================
    "Three-phase power (P = √3·V·I·pf)": {
        "category": "Power Systems",
        "year": "Year 3",
        "variables": [
            ("Power P (W)", "P"),
            ("Line voltage V (V)", "V"),
            ("Line current I (A)", "I"),
            ("Power factor pf", "pf"),
        ],
        "solve": {
            "P": lambda d: math.sqrt(3) * d["V"] * d["I"] * d["pf"],
            "V": lambda d: _div(d["P"], math.sqrt(3) * d["I"] * d["pf"], "I·pf cannot be 0."),
            "I": lambda d: _div(d["P"], math.sqrt(3) * d["V"] * d["pf"], "V·pf cannot be 0."),
            "pf": lambda d: _div(d["P"], math.sqrt(3) * d["V"] * d["I"], "V·I cannot be 0."),
        },
    },
    "Synchronous speed (Ns = 120·f/P)": {
        "category": "Power Systems",
        "year": "Year 3",
        "variables": [
            ("Synchronous speed Ns (rpm)", "Ns"),
            ("Frequency f (Hz)", "f"),
            ("Number of poles P", "P"),
        ],
        "solve": {
            "Ns": lambda d: _div(120 * d["f"], d["P"], "Poles cannot be 0."),
            "f": lambda d: d["Ns"] * d["P"] / 120.0,
            "P": lambda d: _div(120 * d["f"], d["Ns"], "Ns cannot be 0."),
        },
    },
    "Transformer turns ratio (Vp/Vs = Np/Ns)": {
        "category": "Power Systems",
        "year": "Year 2",
        "variables": [
            ("Primary voltage Vp (V)", "Vp"),
            ("Secondary voltage Vs (V)", "Vs"),
            ("Primary turns Np", "Np"),
            ("Secondary turns Ns", "Ns"),
        ],
        "solve": {
            "Vp": lambda d: _div(d["Vs"] * d["Np"], d["Ns"], "Ns cannot be 0."),
            "Vs": lambda d: _div(d["Vp"] * d["Ns"], d["Np"], "Np cannot be 0."),
            "Np": lambda d: _div(d["Vp"] * d["Ns"], d["Vs"], "Vs cannot be 0."),
            "Ns": lambda d: _div(d["Vs"] * d["Np"], d["Vp"], "Vp cannot be 0."),
        },
    },
    "Per-unit impedance (Zpu = Z / Zbase)": {
        "category": "Power Systems",
        "year": "Year 4",
        "variables": [
            ("Per-unit Zpu", "Zpu"),
            ("Actual Z (Ω)", "Z"),
            ("Base Zb (Ω)", "Zb"),
        ],
        "solve": {
            "Zpu": lambda d: _div(d["Z"], d["Zb"], "Zb cannot be 0."),
            "Z": lambda d: d["Zpu"] * d["Zb"],
            "Zb": lambda d: _div(d["Z"], d["Zpu"], "Zpu cannot be 0."),
        },
    },
    "Voltage regulation (%VR = (Vnl-Vfl)/Vfl·100)": {
        "category": "Power Systems",
        "year": "Year 4",
        "variables": [
            ("Voltage regulation %VR", "VR"),
            ("No-load voltage Vnl (V)", "Vnl"),
            ("Full-load voltage Vfl (V)", "Vfl"),
        ],
        "solve": {
            "VR": lambda d: _div(d["Vnl"] - d["Vfl"], d["Vfl"], "Vfl cannot be 0.") * 100,
            "Vnl": lambda d: d["Vfl"] * (1 + d["VR"] / 100),
            "Vfl": lambda d: _div(d["Vnl"], 1 + d["VR"] / 100, "1 + VR/100 cannot be 0."),
        },
    },
    "Efficiency (η = Pout/Pin)": {
        "category": "Power Systems",
        "year": "Year 4",
        "variables": [
            ("Efficiency η (0–1)", "eta"),
            ("Output Pout (W)", "Pout"),
            ("Input Pin (W)", "Pin"),
        ],
        "solve": {
            "eta": lambda d: _div(d["Pout"], d["Pin"], "Pin cannot be 0."),
            "Pout": lambda d: d["eta"] * d["Pin"],
            "Pin": lambda d: _div(d["Pout"], d["eta"], "η cannot be 0."),
        },
    },
    "Battery runtime (t = Capacity/I)": {
        "category": "Power Systems",
        "year": "Year 4",
        "variables": [
            ("Runtime t (h)", "t"),
            ("Capacity (Ah)", "Cap"),
            ("Load current I (A)", "I"),
        ],
        "solve": {
            "t": lambda d: _div(d["Cap"], d["I"], "I cannot be 0."),
            "Cap": lambda d: d["t"] * d["I"],
            "I": lambda d: _div(d["Cap"], d["t"], "t cannot be 0."),
        },
    },
    # ============================================================
    # Electronics
    # ============================================================
    "Amplifier voltage gain (Av = Vout/Vin)": {
        "category": "Electronics",
        "year": "Year 3",
        "variables": [
            ("Voltage gain Av", "Av"),
            ("Output Vout (V)", "Vout"),
            ("Input Vin (V)", "Vin"),
        ],
        "solve": {
            "Av": lambda d: _div(d["Vout"], d["Vin"], "Vin cannot be 0."),
            "Vout": lambda d: d["Av"] * d["Vin"],
            "Vin": lambda d: _div(d["Vout"], d["Av"], "Av cannot be 0."),
        },
    },
    "LED series resistor (R = (Vs - Vf)/I)": {
        "category": "Electronics",
        "year": "Year 2",
        "variables": [
            ("Series R (Ω)", "R"),
            ("Supply Vs (V)", "Vs"),
            ("LED forward Vf (V)", "Vf"),
            ("LED current I (A)", "I"),
        ],
        "solve": {
            "R": lambda d: _div(d["Vs"] - d["Vf"], d["I"], "I cannot be 0."),
            "Vs": lambda d: d["Vf"] + d["I"] * d["R"],
            "Vf": lambda d: d["Vs"] - d["I"] * d["R"],
            "I": lambda d: _div(d["Vs"] - d["Vf"], d["R"], "R cannot be 0."),
        },
    },
    "Op-amp inverting gain (Av = -Rf/Rin)": {
        "category": "Electronics",
        "year": "Year 3",
        "variables": [
            ("Voltage gain Av", "Av"),
            ("Feedback Rf (Ω)", "Rf"),
            ("Input Rin (Ω)", "Rin"),
        ],
        "solve": {
            "Av": lambda d: -_div(d["Rf"], d["Rin"], "Rin cannot be 0."),
            "Rf": lambda d: -d["Av"] * d["Rin"],
            "Rin": lambda d: -_div(d["Rf"], d["Av"], "Av cannot be 0."),
        },
    },
    "Op-amp non-inverting gain (Av = 1 + Rf/Rin)": {
        "category": "Electronics",
        "year": "Year 3",
        "variables": [
            ("Voltage gain Av", "Av"),
            ("Feedback Rf (Ω)", "Rf"),
            ("Ground Rin (Ω)", "Rin"),
        ],
        "solve": {
            "Av": lambda d: 1 + _div(d["Rf"], d["Rin"], "Rin cannot be 0."),
            "Rf": lambda d: (d["Av"] - 1) * d["Rin"],
            "Rin": lambda d: _div(d["Rf"], d["Av"] - 1, "Av must differ from 1."),
        },
    },
    # ============================================================
    # Control Systems
    # ============================================================
    "RC time constant (τ = R·C)": {
        "category": "Control Systems",
        "year": "Year 2",
        "variables": [
            ("Time constant τ (s)", "tau"),
            ("Resistance R (Ω)", "R"),
            ("Capacitance C (F)", "C"),
        ],
        "solve": {
            "tau": lambda d: d["R"] * d["C"],
            "R": lambda d: _div(d["tau"], d["C"], "C cannot be 0."),
            "C": lambda d: _div(d["tau"], d["R"], "R cannot be 0."),
        },
    },
    "RL time constant (τ = L/R)": {
        "category": "Control Systems",
        "year": "Year 4",
        "variables": [
            ("Time constant τ (s)", "tau"),
            ("Inductance L (H)", "L"),
            ("Resistance R (Ω)", "R"),
        ],
        "solve": {
            "tau": lambda d: _div(d["L"], d["R"], "R cannot be 0."),
            "L": lambda d: d["tau"] * d["R"],
            "R": lambda d: _div(d["L"], d["tau"], "τ cannot be 0."),
        },
    },
    "Settling time 5% (ts = 3·τ)": {
        "category": "Control Systems",
        "year": "Year 3",
        "variables": [
            ("Settling time ts (s)", "ts"),
            ("Time constant τ (s)", "tau"),
        ],
        "solve": {
            "ts": lambda d: 3 * d["tau"],
            "tau": lambda d: d["ts"] / 3.0,
        },
    },
    "First-order bandwidth (BW = 1/(2π·τ))": {
        "category": "Control Systems",
        "year": "Year 3",
        "variables": [
            ("Bandwidth BW (Hz)", "BW"),
            ("Time constant τ (s)", "tau"),
        ],
        "solve": {
            "BW": lambda d: _div(1.0, 2 * math.pi * d["tau"], "τ cannot be 0."),
            "tau": lambda d: _div(1.0, 2 * math.pi * d["BW"], "BW cannot be 0."),
        },
    },
    # ============================================================
    # Signals & Communications
    # ============================================================
    "Period & frequency (T = 1/f)": {
        "category": "Signals & Communications",
        "year": "Year 2",
        "variables": [
            ("Period T (s)", "T"),
            ("Frequency f (Hz)", "f"),
        ],
        "solve": {
            "T": lambda d: _div(1.0, d["f"], "f cannot be 0."),
            "f": lambda d: _div(1.0, d["T"], "T cannot be 0."),
        },
    },
    "Angular frequency (ω = 2π·f)": {
        "category": "Signals & Communications",
        "year": "Year 2",
        "variables": [
            ("Angular ω (rad/s)", "w"),
            ("Frequency f (Hz)", "f"),
        ],
        "solve": {
            "w": lambda d: 2 * math.pi * d["f"],
            "f": lambda d: d["w"] / (2 * math.pi),
        },
    },
    "Wavelength in vacuum (λ = c/f)": {
        "category": "Signals & Communications",
        "year": "Year 2",
        "variables": [
            ("Wavelength λ (m)", "lam"),
            ("Frequency f (Hz)", "f"),
        ],
        "solve": {
            "lam": lambda d: _div(SPEED_OF_LIGHT, d["f"], "f cannot be 0."),
            "f": lambda d: _div(SPEED_OF_LIGHT, d["lam"], "λ cannot be 0."),
        },
    },
    "Power decibel (dB = 10·log10(P2/P1))": {
        "category": "Signals & Communications",
        "year": "Year 3",
        "variables": [
            ("Decibels dB", "dB"),
            ("Reference P1 (W)", "P1"),
            ("Measured P2 (W)", "P2"),
        ],
        "solve": {
            "dB": lambda d: 10 * _log10(_div(d["P2"], d["P1"], "P1 cannot be 0.")),
            "P1": lambda d: _div(d["P2"], 10 ** (d["dB"] / 10), "Computed denom 0."),
            "P2": lambda d: d["P1"] * 10 ** (d["dB"] / 10),
        },
    },
    "Voltage decibel (dB = 20·log10(V2/V1))": {
        "category": "Signals & Communications",
        "year": "Year 3",
        "variables": [
            ("Decibels dB", "dB"),
            ("Reference V1 (V)", "V1"),
            ("Measured V2 (V)", "V2"),
        ],
        "solve": {
            "dB": lambda d: 20 * _log10(_div(d["V2"], d["V1"], "V1 cannot be 0.")),
            "V1": lambda d: _div(d["V2"], 10 ** (d["dB"] / 20), "Computed denom 0."),
            "V2": lambda d: d["V1"] * 10 ** (d["dB"] / 20),
        },
    },
    "Shannon channel capacity (C = B·log2(1 + S/N))": {
        "category": "Signals & Communications",
        "year": "Year 4",
        "variables": [
            ("Capacity C (bits/s)", "C"),
            ("Bandwidth B (Hz)", "B"),
            ("Signal-to-noise ratio S/N (linear)", "SN"),
        ],
        "solve": {
            "C": lambda d: d["B"] * _log2(1 + d["SN"]),
            "B": lambda d: _div(d["C"], _log2(1 + d["SN"]), "log2(1+SN) cannot be 0."),
            "SN": lambda d: 2 ** (_div(d["C"], d["B"], "B cannot be 0.")) - 1,
        },
    },
    "Quarter-wave antenna length (L = c/(4·f))": {
        "category": "Signals & Communications",
        "year": "Year 4",
        "variables": [
            ("Antenna length L (m)", "L"),
            ("Frequency f (Hz)", "f"),
        ],
        "solve": {
            "L": lambda d: _div(SPEED_OF_LIGHT, 4 * d["f"], "f cannot be 0."),
            "f": lambda d: _div(SPEED_OF_LIGHT, 4 * d["L"], "L cannot be 0."),
        },
    },
    "Nyquist sampling (fs = 2·fmax)": {
        "category": "Signals & Communications",
        "year": "Year 3",
        "variables": [
            ("Sample rate fs (Hz)", "fs"),
            ("Highest signal fmax (Hz)", "fmax"),
        ],
        "solve": {
            "fs": lambda d: 2 * d["fmax"],
            "fmax": lambda d: d["fs"] / 2.0,
        },
    },
    # ============================================================
    # Digital Systems
    # ============================================================
    "Bits for N levels (n = log2(N))": {
        "category": "Digital Systems",
        "year": "Year 2",
        "variables": [
            ("Bits n", "n"),
            ("Number of levels N", "N"),
        ],
        "solve": {
            "n": lambda d: _log2(d["N"]),
            "N": lambda d: 2 ** d["n"],
        },
    },
    "Bytes from bits (B = bits/8)": {
        "category": "Digital Systems",
        "year": "Year 1",
        "variables": [
            ("Bytes B", "B"),
            ("Bits", "bits"),
        ],
        "solve": {
            "B": lambda d: d["bits"] / 8.0,
            "bits": lambda d: d["B"] * 8.0,
        },
    },
    "Bit time (Tb = 1/Rb)": {
        "category": "Digital Systems",
        "year": "Year 3",
        "variables": [
            ("Bit time Tb (s)", "Tb"),
            ("Bit rate Rb (bits/s)", "Rb"),
        ],
        "solve": {
            "Tb": lambda d: _div(1.0, d["Rb"], "Rb cannot be 0."),
            "Rb": lambda d: _div(1.0, d["Tb"], "Tb cannot be 0."),
        },
    },
}


# --- UI ---------------------------------------------------------------------


def main() -> None:
    st.set_page_config(
        page_title="Engineering Calculator",
        page_icon="🧮",
        layout="centered",
    )
    st.title("🧮 Engineering Calculator")
    st.caption(
        "Reference formulas an electrical-engineering student meets across "
        "the curriculum. Pick a category, choose a formula, fill in the "
        "values you know, leave **exactly one** blank, then click **Solve**."
    )

    # Group formulas by category for the two-step picker.
    by_category: dict[str, dict] = {}
    for name, spec in FORMULAS.items():
        by_category.setdefault(spec["category"], {})[name] = spec

    ordered_cats = [c for c in CATEGORY_ORDER if c in by_category]
    extras = [c for c in by_category if c not in ordered_cats]
    categories = ordered_cats + sorted(extras)

    pretty_cats = [f"{c}  ({len(by_category[c])})" for c in categories]
    cat_lookup = dict(zip(pretty_cats, categories))

    col_a, col_b = st.columns([1, 2])
    pretty_choice = col_a.selectbox("Category", pretty_cats)
    category = cat_lookup[pretty_choice]

    formula_names = list(by_category[category].keys())
    formula_name = col_b.selectbox("Formula", formula_names)
    formula = by_category[category][formula_name]

    st.info(
        f"📚 Course level: **{formula['year']}**   ·   "
        f"Topic: **{category}**"
    )

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
        solve_clicked = col1.form_submit_button(
            "Solve missing variable", type="primary"
        )
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
            solved_label = next(
                label for label, key in formula["variables"] if key == target
            )
            st.success(f"Solved **{solved_label}** = `{result:.6g}`")
        except ValueError as exc:
            st.error(str(exc))


if __name__ == "__main__":
    main()
