import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.grover import run_grover, optimal_iterations


def test_optimal_iterations_grows_sqrt():
    # N=4 -> ~1, N=64 -> ~6, N=1024 -> ~25
    assert optimal_iterations(4) == 2       # (π/4)*2 ≈ 1.57 -> 2
    assert 5 <= optimal_iterations(64) <= 7
    assert 24 <= optimal_iterations(1024) <= 26


def test_grover_finds_target_small():
    # For N=4, Grover should reliably find the target
    result = run_grover(n_qubits=2, target_index=3, shots=1024)
    assert result["success_probability"] > 0.9


def test_grover_finds_target_medium():
    result = run_grover(n_qubits=6, target_index=42, shots=2048)
    assert result["success_probability"] > 0.85