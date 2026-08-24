import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    """
    Detect unusual expenses using Isolation Forest.

    Flags transactions whose spending amount deviates significantly from
    the normal pattern in the dataset (unusually high or low amounts).

    Args:
        df: DataFrame with an 'amount' column (numeric expense amounts).
        contamination: Expected proportion of anomalies in the data
            (range 0.0-0.5). Default is 0.05 (~5% of transactions).

    Returns:
        The original DataFrame with an added 'is_anomaly' boolean column.
        Rows with missing/invalid 'amount' values, or datasets too small
        to reliably model, are marked False.

    Raises:
        ValueError: If 'amount' column is missing or not numeric.
    """
    # Nothing to do on an empty DataFrame
    if df.empty:
        df['is_anomaly'] = False
        return df

    # Validate expected column exists
    if 'amount' not in df.columns:
        raise ValueError("DataFrame must contain 'amount' column")

    # Validate column is numeric
    if not pd.api.types.is_numeric_dtype(df['amount']):
        raise ValueError("'amount' column must be numeric")

    # Guard against an all-NaN column
    if df['amount'].isnull().all():
        raise ValueError("'amount' column contains only NaN values")

    # Not enough data to reliably detect anomalies
    if len(df) < 10:
        df['is_anomaly'] = False
        return df

    # Only fit the model on rows with a valid amount
    valid_mask = df['amount'].notna()

    # We use Isolation Forest on 'amount' to find unusually high or low spending.
    # contamination controls the expected fraction of anomalous transactions.
    model = IsolationForest(contamination=contamination, random_state=42)
    predictions = model.fit_predict(df.loc[valid_mask, ['amount']])

    # -1 means anomaly, 1 means normal; map predictions back onto the full frame
    df['is_anomaly'] = False
    df.loc[valid_mask, 'is_anomaly'] = predictions == -1

    return df
