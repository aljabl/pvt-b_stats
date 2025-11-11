import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def list_subdirs(dir: str) -> list:
    """
    List all subdirectories of a directory.
    Parameters:
        dir (str): Path to the directory.
    Returns:
        List[str]: List of subdirectories
    """
    return [subdir for subdir in os.listdir(dir) if os.path.isdir(os.path.join(dir, subdir))]

def list_data_files(dir: str, ext: str = "txt") -> list:
    """
    List all files in a directory with a given extension.
    Parameters:
        dir (str): Path to the directory.
        ext (str): File extension to filter by (default "txt").
    Returns:
        List[str]: List of file names.
    """
    return [file for file in os.listdir(dir) if file.endswith(ext)]

def read_trial_data(file_path: str) -> pd.DataFrame:
    """
    Read a trial data file into a pandas DataFrame. Assumes delimiter is whitespace.
    Parameters:
        file_path (str): Full path to the trial data file.
    Returns:
        pd.DataFrame: DataFrame with columns ["Trial", "Error", "RT", "Average RT", "Commissions", "Lapses"].
    """
    df = pd.read_csv(file_path, header = None, delimiter = r"\s+")
    df.columns = ["Trial", "Error", "RT", "Average RT", "Commissions", "Lapses"]
    return df


def calculate_trial_metrics(df: pd.DataFrame) -> dict:
    """
    Calculate mean RT, total commissions, and total lapses for a single trial.
    Only RT values between 100 and 500 (inclusive) are considered valid.
    Parameters:
        df (pd.DataFrame): Trial data.
    Returns:
        dict: Dictionary with keys "mean_rt", "total_commissions", "total_lapses".
    """
    valid_rts = df["RT"][(df["RT"] >= 100) & (df["RT"] <= 500)]
    return {
        "mean_rt": valid_rts.mean(),
        "total_commissions": df["Commissions"].sum(),
        "total_lapses": df["Lapses"].sum()
    }


def analyze_condition(dir: str) -> dict:
    """
    Analyze all trial files in a condition directory.
    Parameters:
        dir (str): Directory containing trial files for the condition.
    Returns:
        dict: Summary statistics for the condition including mean RT, total and mean commissions, and total and mean lapses.
    """
    trial_means = []
    trial_commissions = []
    trial_lapses = []

    files = list_data_files(dir)
    for file in files:
        trial_data = read_trial_data(os.path.join(dir, file))
        trial_metrics = calculate_trial_metrics(trial_data)

        trial_means.append(trial_metrics["mean_rt"])
        trial_commissions.append(trial_metrics["total_commissions"])
        trial_lapses.append(trial_metrics["total_lapses"])

    summary = {
        "mean_of_means": float(sum(trial_means) / len(trial_means)) if trial_means else 0,
        "total_commissions": int(sum(trial_commissions)),
        "mean_commissions": float(sum(trial_commissions) / len(trial_commissions)) if trial_commissions else 0,
        "total_lapses": int(sum(trial_lapses)),
        "mean_lapses": float(sum(trial_lapses) / len(trial_lapses)) if trial_lapses else 0
    }
    return summary

def get_condition_summaries(dir: str) -> str:
    """
    Get the summary statistics for each condition.
    Parameters:
        dir (str): Directory containing condition directories.
    Returns:
        dict: Summary statistics for all conditions.
    """
    condition_keys = ["a1", "b1", "a2", "b2"]
    condition_summaries = []

    conditions = list_subdirs(dir)
    conditions = sorted(conditions, key = lambda x: condition_keys.index(x))
    for condition in conditions:
        summary = analyze_condition(os.path.join(dir, condition))
        condition_summaries.append(summary)

    return dict(zip(condition_keys, condition_summaries))

def plot_rt_bar(summaries: dict):
    conditions = list(summaries.keys())
    mean_rts = [summaries[c]['mean_of_means'] for c in conditions]

    plt.figure(figsize=(6, 4))
    plt.bar(conditions, mean_rts, color="steelblue")
    plt.title("Mean Reaction Time by Condition")
    plt.ylabel("Mean RT (ms)")
    plt.xlabel("Condition")
    plt.ylim(0, max(mean_rts) + 50)
    plt.tight_layout()
    plt.savefig("mean_rts.png", dpi = 300, bbox_inches = "tight")

def plot_commission_bar(summaries: dict):
    conditions = list(summaries.keys())
    mean_commissions = [summaries[c]['mean_commissions'] for c in conditions]

    plt.figure(figsize=(6, 4))
    plt.bar(conditions, mean_commissions, color="orange")
    plt.title("Mean Commissions by Condition")
    plt.ylabel("Mean Count")
    plt.xlabel("Condition")
    plt.ylim(0, max(mean_commissions) + 1)
    plt.tight_layout()
    plt.savefig("mean_commissions.png", dpi = 300, bbox_inches = "tight")

def plot_lapse_bar(summaries: dict):
    conditions = list(summaries.keys())
    mean_lapses = [summaries[c]['mean_lapses'] for c in conditions]

    plt.figure(figsize=(6, 4))
    plt.bar(conditions, mean_lapses, color="crimson")
    plt.title("Mean Lapses by Condition")
    plt.ylabel("Mean Count")
    plt.xlabel("Condition")
    plt.ylim(0, max(mean_lapses) + 1)
    plt.tight_layout()
    plt.savefig("mean_lapses.png", dpi = 300, bbox_inches = "tight")

def generate_graphs(summaries: dict):
    plot_rt_bar(summaries)
    plot_commission_bar(summaries)
    plot_lapse_bar(summaries)

    ## plot_condition_rt()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py stats.py <path-to-directory>")
        sys.exit()

    summaries = get_condition_summaries(sys.argv[1])
    print(summaries)

    generate_graphs(summaries)