import time
import logging
from typing import Dict, Any, List, Tuple, Optional
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.preprocessing import LabelEncoder, StandardScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Candidate Algorithms
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_default_candidate_models() -> Dict[str, Any]:
    """Returns the candidate model suite for benchmarking."""
    return {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "DecisionTree": DecisionTreeClassifier(random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "GradientBoosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "GaussianNB": GaussianNB()
    }


class AlgorithmBenchmarker:
    """Evaluates candidate ML models on tabular datasets."""

    def __init__(self, models: Optional[Dict[str, Any]] = None):
        self.models = models if models is not None else get_default_candidate_models()

    def build_preprocessing_pipeline(self, X: pd.DataFrame) -> ColumnTransformer:
        """Constructs an automated preprocessing pipeline for numeric and categorical columns."""
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = [c for c in X.columns if c not in numeric_cols]
        
        numeric_transformer = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
        ])
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_cols),
                ('cat', categorical_transformer, categorical_cols)
            ]
        )
        return preprocessor

    def benchmark_dataset(self, X: pd.DataFrame, y: pd.Series, dataset_name: str) -> List[Dict[str, Any]]:
        """
        Runs Stratified 5-Fold Cross-Validation for all candidate models on (X, y),
        ensuring preprocessing (imputation, scaling, encoding) is fitted ONLY within training folds.
        
        Returns:
            List[Dict[str, Any]]: List of benchmark results per model.
        """
        results = []
        
        # Clean target y
        y_series = pd.Series(y).dropna()
        X_df = X.loc[y_series.index].copy()
        
        # Encode target if object
        le = LabelEncoder()
        y_clean = le.fit_transform(y_series.astype(str))
        
        # CV folds
        n_splits = min(5, len(y_clean))
        if n_splits < 2 or len(np.unique(y_clean)) < 2:
            logger.warning(f"Dataset {dataset_name} has insufficient samples/classes for cross-validation.")
            return results
            
        cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        
        for model_name, model in self.models.items():
            try:
                start_time = time.time()
                preprocessor = self.build_preprocessing_pipeline(X_df)
                full_pipeline = Pipeline([
                    ('preprocessor', preprocessor),
                    ('model', model)
                ])
                
                cv_results = cross_validate(
                    full_pipeline, X_df, y_clean,
                    cv=cv,
                    scoring=['f1_weighted', 'accuracy'],
                    error_score='raise'
                )
                elapsed_time = time.time() - start_time
                
                f1_score = float(np.mean(cv_results['test_f1_weighted']))
                acc_score = float(np.mean(cv_results['test_accuracy']))
                
                results.append({
                    "dataset_name": dataset_name,
                    "algorithm": model_name,
                    "f1_weighted": f1_score,
                    "accuracy": acc_score,
                    "fit_time_sec": float(elapsed_time)
                })
            except Exception as e:
                logger.error(f"Error benchmarking {model_name} on {dataset_name}: {str(e)}")
                
        # Calculate algorithm ranks for this dataset (higher F1 = rank 1)
        if results:
            results.sort(key=lambda r: r['f1_weighted'], reverse=True)
            for rank, res in enumerate(results, start=1):
                res['rank'] = rank
                
        return results

