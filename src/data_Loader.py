"""
Load and validate datasets used as unstructured search spaces.
"""
import os
import pandas as pd


def load_default_dataset():
    """Load the bundled dataset from data/dataset.csv."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "data", "dataset.csv")
    return pd.read_csv(path)


def load_uploaded_csv(file):
    """Load a user-uploaded CSV. First column = item, values coerced to str."""
    df = pd.read_csv(file)
    if df.empty:
        raise ValueError("Uploaded CSV is empty.")
    # Use the first column as the search space
    first_col = df.columns[0]
    df = df[[first_col]].copy()
    df["name"] = df[first_col].astype(str)
    return df[["name"]]


def build_search_space(df, column="name"):
    """Return the list of items (search space) and a name→index map."""
    items = df[column].astype(str).tolist()
    index_map = {item: i for i, item in enumerate(items)}
    return items, index_map


def find_target_index(items, target):
    """Look up the index of a target value (case-insensitive match)."""
    target_lower = str(target).strip().lower()
    for i, item in enumerate(items):
        if str(item).strip().lower() == target_lower:
            return i
    return -1