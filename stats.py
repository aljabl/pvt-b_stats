import pandas as pd
import os
import sys

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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py stats.py <path-to-directory>")
        sys.exit()

    a1_summary = analyze_condition(sys.argv[1])
    print("A1 Summary:", a1_summary)