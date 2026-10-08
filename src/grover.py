"""
Grover's quantum search algorithm implementation.

Corresponds to Sections 3, 11 and 12 of the proposal.
"""
import math
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

from src.oracle import build_oracle
from src.diffusion import build_diffusion_operator

def optimal_iterations(N):
    """
    Optimal number of Grover iterations for one marked solution:
        R ≈ (π/4) * sqrt(N)
    Clamped to at least 1.
    """
    return max(1, int((math.pi / 4) * math.sqrt(N)))


def build_grover_circuit(n_qubits, target_index, n_iterations):
    """
    Build the full Grover circuit.

    Steps:
      1. H on all qubits (uniform superposition).
      2. Repeat n_iterations times: oracle, then diffusion.
      3. Measure all qubits.
    """
    qr = QuantumRegister(n_qubits, "q")
    cr = ClassicalRegister(n_qubits, "c")
    circuit = QuantumCircuit(qr, cr, name=f"Grover_N{2**n_qubits}")

    # Step 1: uniform superposition
    circuit.h(qr)

    # Step 2: Grover iterations
    oracle = build_oracle(n_qubits, target_index)
    diffusion = build_diffusion_operator(n_qubits)
    for _ in range(n_iterations):
        circuit.compose(oracle, inplace=True)
        circuit.compose(diffusion, inplace=True)

    # Step 3: measurement
    circuit.measure(qr, cr)

    return circuit


def run_grover(n_qubits, target_index, shots=1024, iterations=None):
    """
    Execute Grover's algorithm on the Aer simulator.

    Returns a dict with:
        n_qubits, N, target_index, iterations,
        success_probability, counts, circuit_depth, gate_count.
    """
    N = 2 ** n_qubits
    if iterations is None:
        iterations = optimal_iterations(N)

    circuit = build_grover_circuit(n_qubits, target_index, iterations)

    simulator = AerSimulator()
    job = simulator.run(circuit, shots=shots)
    counts = job.result().get_counts()

    # Qiskit returns bit strings MSB-first; convert target to same convention.
    target_key = format(target_index, f"0{n_qubits}b")
    target_count = counts.get(target_key, 0)
    success_probability = target_count / shots

    return {
        "n_qubits": n_qubits,
        "N": N,
        "target_index": target_index,
        "iterations": iterations,
        "success_probability": success_probability,
        "counts": counts,
        "circuit_depth": circuit.depth(),
        "gate_count": sum(circuit.count_ops().values()),
    }