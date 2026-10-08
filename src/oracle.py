"""
Grover's phase oracle: marks a target state by flipping its phase.

Corresponds to Section 3 (Oracle) of the proposal.
"""
from qiskit import QuantumCircuit


def build_oracle(n_qubits, target_index):
    """
    Build a phase oracle that marks |target_index> by flipping its phase.

    Uses the standard trick:
        X on qubits where target bit is 0,
        then multi-controlled-Z on |11...1>,
        then X again to uncompute.

    Args:
        n_qubits: number of qubits.
        target_index: integer in [0, 2^n_qubits).

    Returns:
        QuantumCircuit implementing the oracle.
    """
    oracle = QuantumCircuit(n_qubits, name="Oracle")

    if not (0 <= target_index < 2 ** n_qubits):
        raise ValueError(
            f"target_index {target_index} out of range for {n_qubits} qubits."
        )

    # Qiskit uses little-endian: qubit 0 is the least significant bit.
    target_bits = format(target_index, f"0{n_qubits}b")[::-1]

    # Flip qubits where target bit is 0, so the marked state becomes |11...1>.
    for i, bit in enumerate(target_bits):
        if bit == "0":
            oracle.x(i)

    # Multi-controlled Z: implement as H on last qubit, MCX, H.
    oracle.h(n_qubits - 1)
    oracle.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    oracle.h(n_qubits - 1)

    # Uncompute the X flips.
    for i, bit in enumerate(target_bits):
        if bit == "0":
            oracle.x(i)

    return oracle