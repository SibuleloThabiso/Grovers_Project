# Grover's Search Algorithm

## COMP717 Group Project

### Project Overview

This project focuses on the implementation and evaluation of **Grover's Search Algorithm**, a quantum search algorithm that provides a quadratic speedup over classical unstructured search.

The project investigates how Grover's algorithm searches for a target element within an unstructured dataset and compares its performance with classical search methods.

### Objectives

* Implement Grover's quantum search algorithm.
* Implement a classical search algorithm for comparison.
* Investigate the number of queries required to locate a target element.
* Evaluate the success probability of Grover's algorithm.
* Analyse how the number of qubits changes with the search space size.
* Examine circuit complexity and visualise experimental results.
* Present the findings through a dashboard and experimental plots.

### Project Structure

```text
Grover_Project/
├── app/
│   └── dashboard.py
├── data/
│   └── dataset.csv
├── docs/
├── experiments/
│   ├── dataset_search.py
│   └── run_query_complexity.py
├── notebooks/
│   ├── Grover_Evaluation.ipynb
│   └── plot_results.py
├── results/
│   ├── figures/
│   └── query_complexity_results.csv
├── src/
│   ├── classical_search.py
│   ├── data_Loader.py
│   ├── diffusion.py
│   ├── grover.py
│   └── oracle.py
├── tests/
│   ├── test_classical_search.py
│   └── test_grover.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Technologies Used

* Python
* Quantum computing and quantum search concepts
* Data analysis and visualisation
* Automated testing
* Git and GitHub for version control and collaboration

### Installation

1. Clone the repository:

   ```bash
   git clone YOUR_REPOSITORY_URL
   ```

2. Navigate into the project directory:

   ```bash
   cd Grover_Project
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the environment on Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

Run the relevant experiment scripts from the project root directory:

```bash
python experiments/dataset_search.py
```

```bash
python experiments/run_query_complexity.py
```

The dashboard can be launched using:

```bash
streamlit run app/dashboard.py
```

If Streamlit is not included in the project dependencies, install it separately or add it to `requirements.txt` if the dashboard uses it.

### Testing

Run the test suite using:

```bash
python -m pytest
```

### Results

The `results/` directory contains experimental outputs and figures used to analyse:

* Query complexity
* Success probability
* Number of qubits required
* Quantum circuit complexity

### Academic Context

**Module:** COMP718

**Project:** Implementation and Evaluation of Grover's Search Algorithm
