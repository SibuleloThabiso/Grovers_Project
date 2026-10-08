"""
Main experiment: compare classical vs Grover query complexity
across increasing search-space sizes.

Corresponds to Sections 10 and 11 of the proposal.
"""
import sys
import os
import pandas as pd

# Allow running as a script: add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.classical_search import linear_search
from src.grover import run_grover


def run_experiment(max_n_qubits=10, shots=1024, output_csv=None):
    """
    Loop n_qubits from 2 to max_n_qubits. For each, run:
      - Classical worst-case linear search (target = N-1)
      - Grover's algorithm (target = N-1)
    """
    rows = []
    for n_qubits in range(2, max_n_qubits + 1):
        N = 2 ** n_qubits
        target = N - 1  # worst case for classical

        # Classical
        space = list(range(N))
        _, classical_q = linear_search(space, target)

        # Grover
        g = run_grover(n_qubits, target, shots=shots)

        rows.append({
            "N": N,
            "n_qubits": n_qubits,
            "classical_queries": classical_q,
            "grover_queries": g["iterations"],
            "grover_success_probability": g["success_probability"],
            "circuit_depth": g["circuit_depth"],
            "gate_count": g["gate_count"],
        })

        print(
            f"N={N:5d} | n={n_qubits:2d} | "
            f"Classical={classical_q:5d} | Grover={g['iterations']:3d} | "
            f"Success={g['success_probability']:.3f} | "
            f"Depth={g['circuit_depth']:4d} | Gates={g['gate_count']:5d}"
        )

    df = pd.DataFrame(rows)

    if output_csv:
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        df.to_csv(output_csv, index=False)
        print(f"\nSaved results to {output_csv}")

    return df


if __name__ == "__main__":
    print("=" * 85)
    print("QUERY COMPLEXITY EXPERIMENT: Classical Linear Search vs Grover's Algorithm")
    print("=" * 85)

    df = run_experiment(
        max_n_qubits=10,
        shots=1024,
        output_csv="results/query_complexity_results.csv",
    )

    print("\nSummary:")
    print(df.to_string(index=False))