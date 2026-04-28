#!/usr/bin/env python3
"""Electrical engineering calculator with an easy desktop UI."""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk

GAS_CONSTANT = 8.314462618


def require_nonzero(value: float, field_name: str) -> None:
    if value == 0:
        raise ValueError(f"{field_name} cannot be zero.")


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
}


class EngineeringCalculatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Electrical Engineering Calculator")
        self.root.geometry("700x560")
        self.root.resizable(False, False)

        self.formula_var = tk.StringVar(value=list(FORMULAS.keys())[0])
        self.year_var = tk.StringVar(value="")
        self.status_var = tk.StringVar(value="Fill known values, leave exactly one blank.")
        self.result_var = tk.StringVar(value="Result will appear here.")

        self.inputs_frame = ttk.Frame(self.root, padding=12)
        self.entry_vars: dict[str, tk.StringVar] = {}
        self.entry_widgets: list[ttk.Entry] = []

        self._build_ui()
        self._render_inputs()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=14)
        container.pack(fill="both", expand=True)

        title = ttk.Label(container, text="Electrical Engineering Calculator", font=("Arial", 16, "bold"))
        title.pack(anchor="w")

        subtitle = ttk.Label(
            container,
            text="Choose a formula, fill known values, and leave one unknown blank.",
            foreground="#444444",
        )
        subtitle.pack(anchor="w", pady=(2, 12))

        formula_row = ttk.Frame(container)
        formula_row.pack(fill="x", pady=(0, 10))
        ttk.Label(formula_row, text="Formula:").pack(side="left")

        formula_box = ttk.Combobox(
            formula_row,
            textvariable=self.formula_var,
            values=list(FORMULAS.keys()),
            state="readonly",
            width=50,
        )
        formula_box.pack(side="left", padx=(8, 0))
        formula_box.bind("<<ComboboxSelected>>", lambda _: self._render_inputs())

        year_label = ttk.Label(container, textvariable=self.year_var, foreground="#1b4d89")
        year_label.pack(anchor="w", pady=(0, 8))

        self.inputs_frame = ttk.LabelFrame(container, text="Variables", padding=12)
        self.inputs_frame.pack(fill="x", pady=8)

        buttons = ttk.Frame(container)
        buttons.pack(fill="x", pady=(8, 6))

        calc_btn = ttk.Button(buttons, text="Calculate", command=self.calculate)
        calc_btn.pack(side="left")

        clear_btn = ttk.Button(buttons, text="Clear", command=self.clear_inputs)
        clear_btn.pack(side="left", padx=(8, 0))

        ttk.Separator(container).pack(fill="x", pady=10)

        result_title = ttk.Label(container, text="Result", font=("Arial", 11, "bold"))
        result_title.pack(anchor="w")

        result_label = ttk.Label(
            container,
            textvariable=self.result_var,
            font=("Consolas", 12),
            foreground="#0b4f1f",
            wraplength=500,
        )
        result_label.pack(anchor="w", pady=(2, 10))

        status_label = ttk.Label(
            container,
            textvariable=self.status_var,
            foreground="#8a2d00",
            wraplength=500,
            justify="left",
        )
        status_label.pack(anchor="w")

    def _render_inputs(self) -> None:
        for child in self.inputs_frame.winfo_children():
            child.destroy()
        self.entry_vars.clear()
        self.entry_widgets.clear()

        formula = FORMULAS[self.formula_var.get()]
        self.year_var.set(f"Recommended course level: {formula['year']}")
        for row, (label_text, key) in enumerate(formula["variables"]):
            ttk.Label(self.inputs_frame, text=label_text).grid(row=row, column=0, sticky="w", pady=4)
            var = tk.StringVar()
            entry = ttk.Entry(self.inputs_frame, textvariable=var, width=24)
            entry.grid(row=row, column=1, sticky="w", padx=(8, 0), pady=4)
            self.entry_vars[key] = var
            self.entry_widgets.append(entry)

        if self.entry_widgets:
            self.entry_widgets[0].focus_set()

        self.result_var.set("Result will appear here.")
        self.status_var.set("Enter known values. Leave exactly one field blank to solve it.")

    def clear_inputs(self) -> None:
        for var in self.entry_vars.values():
            var.set("")
        self.result_var.set("Result will appear here.")
        self.status_var.set("Inputs cleared.")
        if self.entry_widgets:
            self.entry_widgets[0].focus_set()

    def calculate(self) -> None:
        formula_name = self.formula_var.get()
        formula = FORMULAS[formula_name]
        values: dict[str, float] = {}

        try:
            missing_keys: list[str] = []

            for _, key in formula["variables"]:
                raw_value = self.entry_vars[key].get().strip()
                if raw_value == "":
                    missing_keys.append(key)
                else:
                    values[key] = float(raw_value)

            if len(missing_keys) != 1:
                raise ValueError("Leave exactly one field blank so the app can solve the missing variable.")

            target_key = missing_keys[0]
            solve_fn = formula["solve"].get(target_key)
            if solve_fn is None:
                raise ValueError(f"This formula cannot solve for {target_key}.")

            result = solve_fn(values)
            self.entry_vars[target_key].set(f"{result:.6g}")
            solved_label = next(label for label, key in formula["variables"] if key == target_key)
            self.result_var.set(f"Solved {solved_label}: {result:.6g}")
            self.status_var.set("Calculated successfully.")
        except ValueError as exc:
            self.status_var.set(str(exc))
            self.result_var.set("Result will appear here.")


def main() -> None:
    root = tk.Tk()
    app = EngineeringCalculatorApp(root)
    root.bind("<Return>", lambda _event: app.calculate())
    root.mainloop()


if __name__ == "__main__":
    main()
