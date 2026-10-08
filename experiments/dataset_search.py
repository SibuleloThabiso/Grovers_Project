"""
Search a real dataset using both classical linear search and Grover's algorithm.
Demonstrates that Grover's complexity is data-content-independent.
"""
import os
import sys
import math
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_Loader import (
    load_default_dataset,
    build_search_space,
    find_target_index,
)
from src.classical_search import linear_search
from src.grover import run_grover


def search_dataset(dataset_path=None, target=None, shots=1024):
    """Search a dataset for a target value using both algorithms."""
    if dataset_path is None:
        df = load_default_dataset()
    else:
        df = pd.read_csv(dataset_path)

    items, index_map = build_search_space(df, column="name")
    N = len(items)
    n_qubits = (N - 1).bit_length()

    # Pad the search space to a power of two for Grover
    padded_items = items + [""] * (2 ** n_qubits - N)

    # Find target index (used only to configure the oracle)
    target_index = find_target_index(items, target)
    if target_index < 0:
        raise ValueError(f"Target '{target}' not found in dataset.")

    # Classical search
    _, comparisons = linear_search(items, target)

    # Grover search
    grover_result = run_grover(
        n_qubits=n_qubits,
        target_index=target_index,
        shots=shots,
    )

    return {
        "N": N,
        "n_qubits": n_qubits,
        "target": target,
        "target_index": target_index,
        "classical_queries": comparisons,
        "grover_queries": grover_result["iterations"],
        "grover_success_prob": grover_result["success_probability"],
    }


if __name__ == "__main__":
    result = search_dataset(target="Zoe")
    for k, v in result.items():
        print(f"{k}: {v}")