"""
Streamlit dashboard for the Grover's algorithm research project.

Interactive exploration of:
  - Classical linear search
  - Grover's quantum search
  - Query complexity comparison
  - Success probability
  - Circuit visualisation

Run from project root:
    streamlit run app/dashboard.py
"""
import os
import sys
import math
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ------------------------------------------------------------------
# Path setup — allow importing from src/
# ------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.classical_search import linear_search
from src.grover import (
    build_grover_circuit,
    run_grover,
    optimal_iterations,
)

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Grover's Algorithm Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Title
# ------------------------------------------------------------------
st.title("Grover's Quantum Search — Interactive Dashboard")
st.caption(
    "Experimental evaluation of Grover's algorithm vs classical linear search "
    "— query complexity comparison."
)

# ------------------------------------------------------------------
# Sidebar controls
# ------------------------------------------------------------------
st.sidebar.header("Experiment Controls")

n_qubits = st.sidebar.slider(
    "Number of qubits (n)",
    min_value=2,
    max_value=10,
    value=6,
    help="Search space size N = 2ⁿ",
)

N = 2 ** n_qubits

target_index = st.sidebar.number_input(
    f"Target index (0 to {N - 1})",
    min_value=0,
    max_value=N - 1,
    value=N - 1,
    help="Worst case for classical search: N-1",
)

iterations = st.sidebar.slider(
    "Grover iterations",
    min_value=0,
    max_value=max(1, int((math.pi / 2) * math.sqrt(N))),
    value=optimal_iterations(N),
    help=f"Theoretical optimum for N={N}: {optimal_iterations(N)}",
)

shots = st.sidebar.select_slider(
    "Measurement shots",
    options=[128, 256, 512, 1024, 2048, 4096],
    value=1024,
)

run_button = st.sidebar.button("Run Experiment", type="primary", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    **Current configuration**
    - N = 2^{n_qubits} = **{N}**
    - Target = **{target_index}**
    - Optimal iterations = **{optimal_iterations(N)}**
    """
)

# ------------------------------------------------------------------
# Tabs
# ------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 , tab6 = st.tabs([
    "Run Experiment",
    "Query Complexity",
    "Success Probability",
    "Circuit",
    "Stored Results",
    "Search a Dataset",
])

# ==================================================================
# TAB 1 — Run Experiment
# ==================================================================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Classical Linear Search")
        if run_button:
            search_space = list(range(N))
            t0 = time.perf_counter()
            idx, comparisons = linear_search(search_space, target_index)
            t1 = time.perf_counter()

            st.metric("Target found at index", idx)
            st.metric("Comparisons (queries)", comparisons)
            st.metric("Wall-clock time", f"{(t1 - t0) * 1000:.3f} ms")

    with col2:
        st.subheader("Grover's Quantum Search")
        if run_button:
            with st.spinner("Simulating quantum circuit..."):
                result = run_grover(
                    n_qubits=n_qubits,
                    target_index=target_index,
                    shots=shots,
                    iterations=iterations,
                )

            st.metric("Oracle queries", result["iterations"])
            st.metric(
                "Success probability",
                f"{result['success_probability'] * 100:.2f}%",
            )
            st.metric("Circuit depth", result["circuit_depth"])
            st.metric("Gate count", result["gate_count"])

    if run_button:
        st.markdown("---")
        st.subheader("Comparison Summary")

        advantage = comparisons / max(1, result["iterations"])
        st.info(
            f"**Classical:** {comparisons} queries  |  "
            f"**Grover:** {result['iterations']} queries  |  "
            f"**Advantage:** {advantage:.2f}× fewer queries"
        )
    else:
        st.info("Configure parameters in the sidebar and click **Run Experiment**.")

# ==================================================================
# TAB 2 — Query Complexity (stored CSV)
# ==================================================================
with tab2:
    st.subheader("Query Complexity Scaling")

    csv_path = os.path.join(ROOT, "results", "query_complexity_results.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.loglog(df["N"], df["classical_queries"], "o-",
                  color="#d62728", linewidth=2, markersize=8,
                  label="Classical O(N)")
        ax.loglog(df["N"], df["grover_queries"], "s-",
                  color="#1f77b4", linewidth=2, markersize=8,
                  label="Grover O(√N)")
        ax.set_xlabel("Search-space size N")
        ax.set_ylabel("Queries")
        ax.set_title("Query Complexity: Classical vs Grover")
        ax.legend()
        ax.grid(True, which="both", alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Data Table")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇Download CSV",
            csv,
            "query_complexity_results.csv",
            "text/csv",
        )
    else:
        st.warning(
            "No stored results found. Run the experiment first:\n\n"
            "```\npython experiments/run_query_complexity.py\n```"
        )

# ==================================================================
# TAB 3 — Success Probability Sweep
# ==================================================================
with tab3:
    st.subheader("Grover Success Probability vs Iterations")
    st.caption(
        "Shows the characteristic oscillation of amplitude amplification. "
        "Over-iterating reduces success probability."
    )

    if st.button("Run iteration sweep", key="sweep_btn"):
        max_iters = max(1, int((math.pi / 2) * math.sqrt(N)))
        iters_range = list(range(0, max_iters + 1))

        probs = []
        progress = st.progress(0, text="Running sweep...")
        for i, it in enumerate(iters_range):
            res = run_grover(
                n_qubits=n_qubits,
                target_index=target_index,
                shots=shots,
                iterations=max(1, it),  # avoid 0 iterations
            )
            probs.append(res["success_probability"])
            progress.progress((i + 1) / len(iters_range),
                              text=f"iter={it}  prob={res['success_probability']:.3f}")

        progress.empty()

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(iters_range, probs, "o-", color="#2ca02c",
                linewidth=2, markersize=8)
        ax.axvline(optimal_iterations(N), color="red", linestyle="--",
                   label=f"Theoretical optimum = {optimal_iterations(N)}")
        ax.set_xlabel("Number of Grover iterations")
        ax.set_ylabel("Success probability")
        ax.set_title(f"Success probability vs iterations  (N={N})")
        ax.set_ylim(-0.02, 1.05)
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)

        st.success(f"Best probability: {max(probs):.3f} at {iters_range[probs.index(max(probs))]} iterations")
    else:
        st.info("Click **Run iteration sweep** to generate the curve.")

# ==================================================================
# TAB 4 — Circuit Visualisation
# ==================================================================
with tab4:
    st.subheader("Grover Circuit Diagram")
    st.caption(
        f"Circuit for N={N} (n={n_qubits} qubits), "
        f"target={target_index}, iterations={iterations}."
    )

    if st.button("Build circuit", key="circuit_btn"):
        circuit = build_grover_circuit(n_qubits, target_index, iterations)
        fig = circuit.draw(output="mpl", style="iqp", fold=40)
        st.pyplot(fig)
        plt.close(fig)

        col1, col2 = st.columns(2)
        col1.metric("Depth", circuit.depth())
        col2.metric("Gates", sum(circuit.count_ops().values()))

        with st.expander("Show gate breakdown"):
            st.json(dict(circuit.count_ops()))

# ==================================================================
# TAB 5 — Stored results file browser
# ==================================================================
with tab5:
    st.subheader("Project Results")

    results_dir = os.path.join(ROOT, "results")
    if os.path.exists(results_dir):
        for root, _, files in os.walk(results_dir):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, ROOT)
                size_kb = os.path.getsize(full) / 1024
                st.write(f"- `{rel}`  ({size_kb:.1f} KB)")
    else:
        st.warning("No results folder found.")

    figures_dir = os.path.join(ROOT, "results", "figures")
    if os.path.exists(figures_dir):
        st.subheader("Generated Figures")
        for f in sorted(os.listdir(figures_dir)):
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                st.image(
                    os.path.join(figures_dir, f),
                    caption=f,
                    use_container_width=True,
                )

# ==================================================================
# TAB 6 — Search a Dataset
# ==================================================================
with tab6:
    st.subheader("Search an Unstructured Dataset")
    st.caption(
        "Type a value to search for. Both algorithms search the same "
        "dataset — Grover's algorithm wins when N is large."
    )

    # Load default dataset
    from src.data_Loader import (
        load_default_dataset,
        build_search_space,
        find_target_index,
    )

    default_df = load_default_dataset()
    default_items = default_df["name"].astype(str).tolist()

    # Allow user to upload their own CSV
    uploaded = st.file_uploader(
        "Optional: upload your own CSV (first column used as dataset)",
        type=["csv"],
    )

    if uploaded is not None:
        upload_df = pd.read_csv(uploaded)
        items = upload_df.iloc[:, 0].astype(str).tolist()
        st.success(f"Loaded {len(items)} items from uploaded CSV.")
    else:
        items = default_items
        st.info(f"Using bundled dataset with {len(items)} items.")

    N = len(items)
    n_qubits = (N - 1).bit_length()

    st.write(f"**Dataset size:** N = {N}  →  **Qubits needed:** {n_qubits}")

    with st.expander("Preview dataset (first 20 rows)"):
        st.write(items[:20])

    # Target input
    target = st.text_input(
        "Enter a value to search for:",
        value=items[N // 2],  # default to middle item
    )

    if st.button("Run search", type="primary"):
        target_idx = find_target_index(items, target)

        if target_idx < 0:
            st.error(f"'{target}' was not found in the dataset.")
        else:
            col1, col2 = st.columns(2)

            # Classical
            with col1:
                st.markdown("### Classical Linear Search")
                with st.spinner("Searching..."):
                    _, comparisons = linear_search(items, target)
                st.metric("Comparisons", comparisons)
                st.metric("Found at index", target_idx)

            # Grover
            with col2:
                st.markdown("### Grover's Algorithm")
                with st.spinner("Simulating quantum circuit..."):
                    result = run_grover(
                        n_qubits=n_qubits,
                        target_index=target_idx,
                        shots=1024,
                    )
                st.metric("Grover iterations", result["iterations"])
                st.metric(
                    "Success probability",
                    f"{result['success_probability'] * 100:.2f}%",
                )

            st.markdown("---")
            st.markdown(
                f"**Advantage:** classical = {comparisons} queries, "
                f"Grover = {result['iterations']} queries  →  "
                f"**{comparisons / max(1, result['iterations']):.2f}× fewer queries**"
            )
# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Grover's Quantum Search — Experimental Evaluation  |  "
    "Built with Qiskit 2.x + Streamlit"
)