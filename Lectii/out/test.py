"""Housing prices

1. Problem framing and dataset loading
2. Train / Validation / Test split
3. Baseline model
4. Pipeline (proper processing)
5. Cross-validation
6. Ridge regression + hyperparameter tuning
7. Final evaluation on test set
8. Permutation importance
9. Save trained pipeline (joblib) + generate predictions CSV
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from joblib import dump

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.inspection import permutation_importance


@dataclass(frozen=True)
class Metrics:
    mae: float
    rmse: float
    r2: float


def ensure_out_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def evaluate(y_true: np.ndarray, y_pred: np.ndarray) -> Metrics:
    return Metrics(
        mae=float(mean_absolute_error(y_true, y_pred)),
        rmse=rmse(y_true, y_pred),
        r2=float(r2_score(y_true, y_pred)),
    )


def print_metrics(title: str, metrics: Metrics) -> None:
    print(f"{title}")
    print(f"  MAE :  {metrics.mae:.4f}")
    print(f"  RMSE:  {metrics.rmse:.4f}")
    print(f"  R2  :  {metrics.r2:.4f}")


def main(seed: int = 42) -> None:
    np.random.seed(seed)
    out_dir = ensure_out_dir("out")

    # -------------------------------------------------
    # 1. Problem framing and dataset loading
    # -------------------------------------------------
    print("Pasul 1: Problem framing and dataset loading")

    data = fetch_california_housing(as_frame=True)
    df = data.frame.copy()

    target_name = data.target_names[0] if data.target_names else "target"
    if target_name not in df.columns:
        target_name = df.columns[-1]

    X = df.drop(columns=[target_name])
    y = df[target_name]

    print(f"Dataset shape: {df.shape}")
    print(f"Target: {target_name}")
    print(f"Features: {list(X.columns)}")
    print(df.head(3))
    print()

    # -------------------------------------------------
    # 2. Train / Validation / Test split
    # -------------------------------------------------
    print("Pasul 2: Train / Validation / Test split")

    # 20% test
    X_train_full, X_test, y_train_full, y_test = train_test_split(
        X, y, test_size=0.20, random_state=seed
    )

    # Din cei 80% rămași, 25% merg la validation
    # => 0.25 * 0.80 = 0.20 din total
    # => train = 60%, val = 20%, test = 20%
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_full, y_train_full, test_size=0.25, random_state=seed
    )

    print(f"Train shape: {X_train.shape}, {y_train.shape}")
    print(f"Val shape:   {X_val.shape}, {y_val.shape}")
    print(f"Test shape:  {X_test.shape}, {y_test.shape}")
    print()

    # -------------------------------------------------
    # 3. Baseline model
    # -------------------------------------------------
    print("Pasul 3: Baseline model (Linear Regression)")

    baseline_model = LinearRegression()
    baseline_model.fit(X_train, y_train)

    val_pred_baseline = baseline_model.predict(X_val)
    baseline_metrics = evaluate(y_val.to_numpy(), val_pred_baseline)

    print_metrics("Baseline metrics on validation set:", baseline_metrics)
    print()

    # -------------------------------------------------
    # 4. Pipeline (proper processing)
    # -------------------------------------------------
    print("Pasul 4: Pipeline (StandardScaler + Ridge)")

    ridge_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge())
    ])

    ridge_pipeline.fit(X_train, y_train)
    val_pred_pipe = ridge_pipeline.predict(X_val)
    pipeline_metrics = evaluate(y_val.to_numpy(), val_pred_pipe)

    print_metrics("Pipeline metrics on validation set:", pipeline_metrics)
    print()

    # -------------------------------------------------
    # 5. Cross-validation
    # -------------------------------------------------
    print("Pasul 5: Cross-validation")

    cv_scores = cross_val_score(
        ridge_pipeline,
        X_train_full,
        y_train_full,
        cv=5,
        scoring="neg_root_mean_squared_error"
    )

    cv_rmse_scores = -cv_scores

    print(f"CV RMSE scores: {np.round(cv_rmse_scores, 4)}")
    print(f"CV RMSE mean:   {cv_rmse_scores.mean():.4f}")
    print(f"CV RMSE std:    {cv_rmse_scores.std():.4f}")
    print()

    # -------------------------------------------------
    # 6. Ridge regression + hyperparameter tuning
    # -------------------------------------------------
    print("Pasul 6: Ridge regression + hyperparameter tuning")

    param_grid = {
        "model__alpha": [0.01, 0.1, 1.0, 10.0, 100.0]
    }

    grid_search = GridSearchCV(
        estimator=ridge_pipeline,
        param_grid=param_grid,
        cv=5,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1
    )

    grid_search.fit(X_train_full, y_train_full)

    best_model = grid_search.best_estimator_

    print(f"Best params: {grid_search.best_params_}")
    print(f"Best CV RMSE: {-grid_search.best_score_:.4f}")
    print()

    # -------------------------------------------------
    # 7. Final evaluation on test set
    # -------------------------------------------------
    print("Pasul 7: Final evaluation on test set")

    test_pred = best_model.predict(X_test)
    test_metrics = evaluate(y_test.to_numpy(), test_pred)

    print_metrics("Final test metrics:", test_metrics)
    print()

    # -------------------------------------------------
    # 8. Permutation importance
    # -------------------------------------------------
    print("Pasul 8: Permutation importance")

    perm = permutation_importance(
        best_model,
        X_test,
        y_test,
        n_repeats=10,
        random_state=seed,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1
    )

    importance_df = pd.DataFrame({
        "feature": X_test.columns,
        "importance_mean": perm.importances_mean,
        "importance_std": perm.importances_std
    }).sort_values(by="importance_mean", ascending=False)

    print("Top feature importances:")
    print(importance_df.head(10))
    print()

    # -------------------------------------------------
    # 9. Save trained pipeline + generate prediction CSV
    # -------------------------------------------------
    print("Pasul 9: Save trained pipeline + generate predictions CSV")

    model_path = os.path.join(out_dir, "ridge_pipeline.joblib")
    dump(best_model, model_path)

    predictions_df = pd.DataFrame({
        "y_true": y_test.to_numpy(),
        "y_pred": test_pred
    })

    predictions_path = os.path.join(out_dir, "predictions.csv")
    predictions_df.to_csv(predictions_path, index=False)

    importance_path = os.path.join(out_dir, "permutation_importance.csv")
    importance_df.to_csv(importance_path, index=False)

    print(f"Model salvat la: {model_path}")
    print(f"Predicții salvate la: {predictions_path}")
    print(f"Importanțe salvate la: {importance_path}")
    print()
    print("Exercițiul s-a terminat cu succes.")


if __name__ == "__main__":
    main()