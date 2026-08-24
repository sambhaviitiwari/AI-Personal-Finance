import numpy as np
import pandas as pd
from datetime import timedelta
from typing import Dict, List, Any
from sklearn.ensemble import RandomForestRegressor


class SpendingForecaster:
    """
    AI/ML Spending Forecasting Engine for Personal Finance.
    Handles total spending and category-wise spending predictions.
    """

    def __init__(self, min_samples_for_ml: int = 15):
        self.min_samples_for_ml = min_samples_for_ml

    def _preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans and standardizes transaction DataFrame."""

        clean_df = df.copy()

        # Ensure date format
        if "date" in clean_df.columns:
            clean_df["date"] = pd.to_datetime(
                clean_df["date"],
                errors="coerce"
            )

        elif "created_at" in clean_df.columns:
            clean_df["date"] = pd.to_datetime(
                clean_df["created_at"],
                errors="coerce"
            )

        else:
            raise ValueError(
                "Transactions data must contain a 'date' or "
                "'created_at' column."
            )

        # Ensure amount is numeric and positive
        clean_df["amount"] = pd.to_numeric(
            clean_df["amount"],
            errors="coerce"
        ).abs()

        # Ensure category exists
        if "category" not in clean_df.columns:
            clean_df["category"] = "General"
        else:
            clean_df["category"] = clean_df["category"].fillna(
                "General"
            )

        return clean_df.dropna(
            subset=["date", "amount"]
        )

    def _extract_time_features(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """Extract temporal features for ML modeling."""

        feat_df = df.copy()

        feat_df["day_of_week"] = (
            feat_df["date"].dt.dayofweek
        )

        feat_df["day_of_month"] = (
            feat_df["date"].dt.day
        )

        feat_df["month"] = (
            feat_df["date"].dt.month
        )

        feat_df["is_weekend"] = (
            feat_df["day_of_week"]
            .isin([5, 6])
            .astype(int)
        )

        return feat_df

    def _heuristic_forecast(
        self,
        daily_series: pd.Series,
        days_ahead: int
    ) -> List[float]:
        """
        Moving Average baseline for sparse transaction histories.
        """

        if (
            daily_series.empty
            or daily_series.sum() == 0
        ):
            return [0.0] * days_ahead

        avg_daily = float(
            daily_series.mean()
        )

        recent_7d = (
            daily_series.tail(7).mean()
            if len(daily_series) >= 7
            else avg_daily
        )

        # Weighted blend between overall mean
        # and recent spending momentum
        projected_daily = (
            0.6 * recent_7d
            + 0.4 * avg_daily
        )

        return [
            round(
                max(0.0, float(projected_daily)),
                2
            )
        ] * days_ahead

    def forecast_total_spending(
        self,
        transactions: pd.DataFrame,
        days_ahead: int = 30
    ) -> Dict[str, Any]:
        """
        Forecasts daily total spending for
        the upcoming days_ahead days.
        """

        df = self._preprocess_data(
            transactions
        )

        # No valid data
        if df.empty:
            return {
                "forecast_days": days_ahead,
                "projected_total": 0.0,
                "daily_forecasts": [],
                "confidence_score": 0.0,
                "model_used": "None"
            }

        # -------------------------------------------------
        # Convert transactions into daily spending
        # -------------------------------------------------

        daily_df = (
            df.groupby(
                pd.Grouper(
                    key="date",
                    freq="D"
                )
            )["amount"]
            .sum()
            .reset_index()
        )

        daily_df["amount"] = (
            daily_df["amount"]
            .fillna(0.0)
        )

        # Future dates
        start_date = (
            daily_df["date"].max()
            + timedelta(days=1)
        )

        future_dates = [
            start_date + timedelta(days=i)
            for i in range(days_ahead)
        ]

        # -------------------------------------------------
        # HEURISTIC MODEL FOR SMALL DATASETS
        # -------------------------------------------------

        if len(daily_df) < self.min_samples_for_ml:

            preds = self._heuristic_forecast(
                daily_df["amount"],
                days_ahead
            )

            model_used = (
                "Heuristic Moving Average"
            )

            confidence = 0.65

        # -------------------------------------------------
        # RANDOM FOREST MODEL
        # -------------------------------------------------

        else:

            daily_feat = (
                self._extract_time_features(
                    daily_df
                )
            )

            # Lag features
            daily_feat["lag_1"] = (
                daily_feat["amount"]
                .shift(1)
                .bfill()
            )

            daily_feat["lag_7"] = (
                daily_feat["amount"]
                .shift(7)
                .bfill()
            )

            daily_feat["rolling_7_mean"] = (
                daily_feat["amount"]
                .rolling(
                    7,
                    min_periods=1
                )
                .mean()
            )

            # Features used by Random Forest
            features = [
                "day_of_week",
                "day_of_month",
                "month",
                "is_weekend",
                "lag_1",
                "lag_7",
                "rolling_7_mean"
            ]

            X = daily_feat[features]
            y = daily_feat["amount"]

            # -------------------------------------------------
            # TRAIN RANDOM FOREST MODEL
            # -------------------------------------------------

            model = RandomForestRegressor(
                n_estimators=60,
                random_state=42,
                max_depth=5,
                min_samples_leaf=2
            )

            model.fit(X, y)

            # -------------------------------------------------
            # ITERATIVE MULTI-STEP FORECAST
            # -------------------------------------------------

            preds = []

            curr_lags = {
                "lag_1": float(
                    daily_feat["amount"].iloc[-1]
                ),

                "lag_7": (
                    float(
                        daily_feat[
                            "amount"
                        ].iloc[-7]
                    )
                    if len(daily_feat) >= 7
                    else float(
                        daily_feat[
                            "amount"
                        ].mean()
                    )
                ),

                "rolling_7_mean": float(
                    daily_feat[
                        "amount"
                    ].tail(7).mean()
                )
            }

            for f_date in future_dates:

                row = pd.DataFrame([
                    {
                        "day_of_week":
                            f_date.weekday(),

                        "day_of_month":
                            f_date.day,

                        "month":
                            f_date.month,

                        "is_weekend":
                            1
                            if f_date.weekday()
                            in [5, 6]
                            else 0,

                        "lag_1":
                            curr_lags["lag_1"],

                        "lag_7":
                            curr_lags["lag_7"],

                        "rolling_7_mean":
                            curr_lags[
                                "rolling_7_mean"
                            ]
                    }
                ])

                # Predict next day's spending
                pred_val = max(
                    0.0,
                    float(
                        model.predict(row)[0]
                    )
                )

                preds.append(
                    round(pred_val, 2)
                )

                # Update lag values
                curr_lags["lag_7"] = (
                    curr_lags["lag_1"]
                )

                curr_lags["lag_1"] = (
                    pred_val
                )

                curr_lags[
                    "rolling_7_mean"
                ] = (
                    curr_lags[
                        "rolling_7_mean"
                    ] * 6
                    + pred_val
                ) / 7

            model_used = (
                "Random Forest Regressor"
            )

            confidence = 0.85

        # -------------------------------------------------
        # DAILY FORECAST OUTPUT
        # -------------------------------------------------

        daily_breakdown = [
            {
                "date": d.strftime(
                    "%Y-%m-%d"
                ),
                "predicted_amount": val
            }
            for d, val in zip(
                future_dates,
                preds
            )
        ]

        return {
            "forecast_days": days_ahead,

            "projected_total": round(
                sum(preds),
                2
            ),

            "daily_forecasts":
                daily_breakdown,

            "confidence_score":
                confidence,

            "model_used":
                model_used
        }

    def forecast_by_category(
        self,
        transactions: pd.DataFrame,
        days_ahead: int = 30
    ) -> Dict[str, Any]:
        """
        Forecast spending separately
        for each expense category.
        """

        df = self._preprocess_data(
            transactions
        )

        if df.empty:
            return {
                "category_forecasts": {},
                "total_projected": 0.0
            }

        category_results = {}
        total_projected = 0.0

        for category, cat_df in df.groupby(
            "category"
        ):

            result = (
                self.forecast_total_spending(
                    cat_df,
                    days_ahead=days_ahead
                )
            )

            cat_total = result[
                "projected_total"
            ]

            total_projected += cat_total

            category_results[
                category
            ] = {
                "projected_total":
                    cat_total,

                "daily_average":
                    round(
                        cat_total
                        / days_ahead,
                        2
                    ),

                "model_used":
                    result["model_used"]
            }

        return {
            "forecast_days":
                days_ahead,

            "total_projected":
                round(
                    total_projected,
                    2
                ),

            "category_forecasts":
                category_results
        }


# ---------------------------------------------------------
# SIMPLE API WRAPPER
# ---------------------------------------------------------

def get_spending_forecast(
    transactions_data: List[
        Dict[str, Any]
    ],
    days_ahead: int = 30
) -> Dict[str, Any]:
    """
    API-friendly wrapper for spending forecasting.

    Example:
    [
        {
            "date": "2026-08-01",
            "amount": 250.0,
            "category": "Food"
        }
    ]
    """

    if not transactions_data:

        return {
            "error":
                "No transactions provided",

            "projected_total":
                0.0
        }

    df = pd.DataFrame(
        transactions_data
    )

    forecaster = (
        SpendingForecaster()
    )

    total_forecast = (
        forecaster.forecast_total_spending(
            df,
            days_ahead=days_ahead
        )
    )

    category_forecast = (
        forecaster.forecast_by_category(
            df,
            days_ahead=days_ahead
        )
    )

    return {
        "summary":
            total_forecast,

        "categories":
            category_forecast[
                "category_forecasts"
            ]
    }