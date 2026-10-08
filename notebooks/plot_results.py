"""
Generate all figures for the Grover's algorithm research report.

Reads:   results/query_complexity_results.csv
Writes:  results/figures/*.png

Run from project root:
    python notebooks/plot_results.py
    (or)
    python experiments/plot_results.py
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Path setup — works no matter where this file lives
# ------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "results", "query_complexity_results.csv")
FIG_DIR = os.path.join(ROOT, "results", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------
if not os.path.exists(CSV_PATH):
    sys.exit(
        f"\n[ERROR] Could not find {CSV_PATH}\n"
        f"Run the experiment first:\n"
        f"    python experiments/run_query_complexity.py\n"
    )

df = pd.read_csv(CSV_PATH)
print(f"Loaded {len(df)} rows from {CSV_PATH}")
print(df.to_string(index=False))
print()

# Common styling
plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 150,
    "font.size": 11,
    "axes.grid": True,
    "grid.alpha": 0.3,
})

# Theoretical curves for overlay
N_smooth = np.logspace(np.log10(df["N"].min()), np.log10(df["N"].max()), 200)


# ==================================================================
# FIGURE 1: Query complexity — the headline figure (log-log)
# ==================================================================
fig, ax = plt.subplots(figsize=(8, 6))

ax.loglog(df["N"], df["classical_queries"], "o-",
          color="#d62728", linewidth=2, markersize=8,
          label="Classical linear search  O(N)")
ax.loglog(df["N"], df["grover_queries"], "s-",
          color="#1f77b4", linewidth=2, markersize=8,
          label="Grover's algorithm  O(√N)")

# Theoretical curves as dashed references
ax.loglog(N_smooth, N_smooth, "--", color="#d62728",
          alpha=0.4, linewidth=1, label="N (reference)")
ax.loglog(N_smooth, (np.pi / 4) * np.sqrt(N_smooth), "--",
          color="#1f77b4", alpha=0.4, linewidth=1,
          label="(π/4)√N (reference)")

ax.set_xlabel("Search-space size N")
ax.set_ylabel("Number of queries")
ax.set_title("Query Complexity: Classical vs Grover's Algorithm")
ax.legend(loc="upper left", framealpha=0.9)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "01_query_complexity.png"))
plt.close()


# ==================================================================
# FIGURE 2: Grover success probability vs N
# ==================================================================
fig, ax = plt.subplots(figsize=(8, 5))

ax.semilogx(df["N"], df["grover_success_probability"], "o-",
            color="#2ca02c", linewidth=2, markersize=9,
            label="Experimental success probability")
ax.axhline(0.95, color="gray", linestyle="--",
           linewidth=1, label="95% threshold")

ax.set_xlabel("Search-space size N")
ax.set_ylabel("Success probability")
ax.set_title("Grover Success Probability vs Search-Space Size")
ax.set_ylim(0.90, 1.02)
ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "02_success_probability.png"))
plt.close()


# ==================================================================
# FIGURE 3: Qubits vs search-space size (exponential relationship)
# ==================================================================
fig, ax = plt.subplots(figsize=(8, 5))

ax.semilogy(df["n_qubits"], df["N"], "o-",
            color="#9467bd", linewidth=2, markersize=9,
            label="N = 2ⁿ")

# Overlay the theoretical line
n_smooth = np.linspace(df["n_qubits"].min(), df["n_qubits"].max(), 200)
ax.semilogy(n_smooth, 2 ** n_smooth, "--", color="#9467bd",
            alpha=0.4, linewidth=1, label="Theoretical 2ⁿ")

for _, row in df.iterrows():
    ax.annotate(f"2^{int(row['n_qubits'])}={int(row['N'])}",
                (row["n_qubits"], row["N"]),
                textcoords="offset points", xytext=(6, -12),
                fontsize=8, color="#555")

ax.set_xlabel("Number of qubits (n)")
ax.set_ylabel("Search-space size N")
ax.set_title("Qubits vs Search-Space Size (exponential scaling)")
ax.legend(loc="upper left")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "03_qubits_vs_N.png"))
plt.close()


# ==================================================================
# FIGURE 4: Circuit depth and gate count vs N
# ==================================================================
fig, ax1 = plt.subplots(figsize=(8, 5))

color_depth = "#ff7f0e"
color_gates = "#17becf"

ax1.semilogx(df["N"], df["circuit_depth"], "o-",
             color=color_depth, linewidth=2, markersize=8,
             label="Circuit depth")
ax1.set_xlabel("Search-space size N")
ax1.set_ylabel("Circuit depth", color=color_depth)
ax1.tick_params(axis="y", labelcolor=color_depth)

ax2 = ax1.twinx()
ax2.semilogx(df["N"], df["gate_count"], "s--",
             color=color_gates, linewidth=2, markersize=8,
             label="Gate count")
ax2.set_ylabel("Gate count", color=color_gates)
ax2.tick_params(axis="y", labelcolor=color_gates)
ax2.grid(False)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

ax1.set_title("Grover Circuit Complexity vs N")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "04_circuit_complexity.png"))
plt.close()


# ==================================================================
# FIGURE 5: Combined panel for the report
# ==================================================================
fig, axes = plt.subplots(2, 2, figsize=(13, 10))

# Panel A: query complexity
axes[0, 0].loglog(df["N"], df["classical_queries"], "o-",
                  color="#d62728", linewidth=2, markersize=7,
                  label="Classical O(N)")
axes[0, 0].loglog(df["N"], df["grover_queries"], "s-",
                  color="#1f77b4", linewidth=2, markersize=7,
                  label="Grover O(√N)")
axes[0, 0].set_xlabel("N")
axes[0, 0].set_ylabel("Queries")
axes[0, 0].set_title("(a) Query complexity")
axes[0, 0].legend()
axes[0, 0].grid(True, which="both", alpha=0.3)

# Panel B: success probability
axes[0, 1].semilogx(df["N"], df["grover_success_probability"], "o-",
                    color="#2ca02c", linewidth=2, markersize=7)
axes[0, 1].axhline(0.95, color="gray", linestyle="--", linewidth=1)
axes[0, 1].set_xlabel("N")
axes[0, 1].set_ylabel("Success probability")
axes[0, 1].set_title("(b) Grover success probability")
axes[0, 1].set_ylim(0.90, 1.02)
axes[0, 1].grid(True, alpha=0.3)

# Panel C: qubits vs N
axes[1, 0].semilogy(df["n_qubits"], df["N"], "o-",
                    color="#9467bd", linewidth=2, markersize=7)
axes[1, 0].set_xlabel("Qubits (n)")
axes[1, 0].set_ylabel("Search-space size N")
axes[1, 0].set_title("(c) Exponential state space  N = 2ⁿ")
axes[1, 0].grid(True, which="both", alpha=0.3)

# Panel D: circuit depth & gates
axes[1, 1].semilogx(df["N"], df["circuit_depth"], "o-",
                    color="#ff7f0e", linewidth=2, markersize=7,
                    label="Depth")
axes[1, 1].semilogx(df["N"], df["gate_count"], "s--",
                    color="#17becf", linewidth=2, markersize=7,
                    label="Gates")
axes[1, 1].set_xlabel("N")
axes[1, 1].set_ylabel("Count")
axes[1, 1].set_title("(d) Circuit complexity")
axes[1, 1].legend()
axes[1, 1].grid(True, which="both", alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "05_combined_panel.png"))
plt.close()


# ==================================================================
# Done
# ==================================================================
print("=" * 60)
print(f"All figures saved to: {FIG_DIR}")
print("=" * 60)
for f in sorted(os.listdir(FIG_DIR)):
    full = os.path.join(FIG_DIR, f)
    size_kb = os.path.getsize(full) / 1024
    print(f"  {f:35s}  {size_kb:6.1f} KB")