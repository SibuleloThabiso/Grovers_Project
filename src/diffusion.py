"""
Grover's diffusion operator (inversion about the mean).

Corresponds to Section 3 (Diffusion Operator) of the proposal.
"""
from qiskit import QuantumCircuit


def build_diffusion_operator(n_qubits):
    """
    Build the diffusion operator:
        H^n -> X^n -> MCZ -> X^n -> H^n

    where MCZ is a multi-controlled Z acting on the |11...1> state.
    """
    diffusion = QuantumCircuit(n_qubits, name="Diffusion")

    diffusion.h(range(n_qubits))
    diffusion.x(range(n_qubits))

    # Multi-controlled Z
    diffusion.h(n_qubits - 1)
    diffusion.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    diffusion.h(n_qubits - 1)

    diffusion.x(range(n_qubits))
    diffusion.h(range(n_qubits))

    return diffusion