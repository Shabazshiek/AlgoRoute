import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from typing import Dict, Any


class MetaFeatureExtractor:
    """Extracts meta-features from tabular dataset (X, y)."""

    def __init__(self):
        pass

    def extract_meta_features(self, X: pd.DataFrame, y: pd.Series, dataset_name: str = "dataset") -> Dict[str, Any]:
        """
        Extracts comprehensive meta-features for dataset (X, y).
        
        Returns:
            Dict[str, Any]: Key-value dictionary of meta-feature names and numeric values.
        """
        meta_features = {"dataset_name": dataset_name}
        
        # Ensure y is clean series
        y_series = pd.Series(y).dropna()
        X_df = X.loc[y_series.index].copy()
        
        n_instances, n_features = X_df.shape
        meta_features["n_instances"] = int(n_instances)
        meta_features["n_features"] = int(n_features)
        meta_features["ratio_instances_to_features"] = float(n_instances / (n_features + 1e-8))
        
        # Feature types
        numeric_cols = X_df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = [c for c in X_df.columns if c not in numeric_cols]
        
        n_numeric = len(numeric_cols)
        n_categorical = len(categorical_cols)
        meta_features["n_numeric_features"] = int(n_numeric)
        meta_features["n_categorical_features"] = int(n_categorical)
        meta_features["ratio_numeric_features"] = float(n_numeric / (n_features + 1e-8))
        meta_features["ratio_categorical_features"] = float(n_categorical / (n_features + 1e-8))
        
        # Missing values
        total_cells = n_instances * n_features
        n_missing = int(X_df.isna().sum().sum())
        meta_features["n_missing_values"] = n_missing
        meta_features["missing_value_ratio"] = float(n_missing / (total_cells + 1e-8))
        
        # Target characteristics
        class_counts = y_series.value_counts()
        n_classes = len(class_counts)
        meta_features["n_classes"] = int(n_classes)
        
        maj_count = class_counts.max()
        min_count = class_counts.min()
        meta_features["class_imbalance_ratio"] = float(maj_count / (min_count + 1e-8))
        meta_features["majority_class_percentage"] = float(maj_count / (n_instances + 1e-8))
        
        # 2. Statistical Meta-Features (Continuous variables)
        if n_numeric > 0:
            numeric_df = X_df[numeric_cols].fillna(X_df[numeric_cols].median())
            skews = [float(skew(numeric_df[col].dropna())) for col in numeric_cols if len(numeric_df[col].dropna()) > 2]
            kurts = [float(kurtosis(numeric_df[col].dropna())) for col in numeric_cols if len(numeric_df[col].dropna()) > 2]
            
            meta_features["skewness_mean"] = float(np.mean(skews)) if skews else 0.0
            meta_features["skewness_std"] = float(np.std(skews)) if skews else 0.0
            meta_features["kurtosis_mean"] = float(np.mean(kurts)) if kurts else 0.0
            meta_features["kurtosis_std"] = float(np.std(kurts)) if kurts else 0.0
            
            if n_numeric > 1:
                corr_matrix = numeric_df.corr().abs().to_numpy(copy=True)
                np.fill_diagonal(corr_matrix, np.nan)
                meta_features["mean_correlation_abs"] = float(np.nanmean(corr_matrix)) if not np.all(np.isnan(corr_matrix)) else 0.0
            else:
                meta_features["mean_correlation_abs"] = 0.0
        else:
            meta_features["skewness_mean"] = 0.0
            meta_features["skewness_std"] = 0.0
            meta_features["kurtosis_mean"] = 0.0
            meta_features["kurtosis_std"] = 0.0
            meta_features["mean_correlation_abs"] = 0.0

        # 3. Information-Theoretic Meta-Features
        probs = class_counts / n_instances
        entropy = -float(np.sum(probs * np.log2(probs + 1e-12)))
        meta_features["class_entropy"] = entropy
        meta_features["normalized_class_entropy"] = float(entropy / np.log2(max(n_classes, 2)))
        
        # 4. Landmarking Meta-Features
        landmarkers = self._compute_landmarkers(X_df, y_series)
        meta_features.update(landmarkers)
        
        return meta_features

    def _compute_landmarkers(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Runs fast landmarking algorithms on preprocessed copy of X, y."""
        landmarkers = {
            "landmarker_decision_stump": 0.0,
            "landmarker_naive_bayes": 0.0
        }
        try:
            # Simple preprocessing for landmarkers
            X_encoded = X.copy()
            for col in X_encoded.columns:
                if X_encoded[col].dtype == 'object' or isinstance(X_encoded[col].dtype, pd.CategoricalDtype):
                    le = LabelEncoder()
                    X_encoded[col] = le.fit_transform(X_encoded[col].astype(str))
            
            imputer = SimpleImputer(strategy='median')
            X_clean = imputer.fit_transform(X_encoded)
            
            le_y = LabelEncoder()
            y_clean = le_y.fit_transform(y.astype(str))
            
            cv_folds = min(3, len(y_clean))
            if cv_folds >= 2 and len(np.unique(y_clean)) >= 2:
                # Decision Stump
                stump = DecisionTreeClassifier(max_depth=1, random_state=42)
                stump_scores = cross_val_score(stump, X_clean, y_clean, cv=cv_folds, scoring='accuracy')
                landmarkers["landmarker_decision_stump"] = float(np.mean(stump_scores))
                
                # Naive Bayes
                nb = GaussianNB()
                nb_scores = cross_val_score(nb, X_clean, y_clean, cv=cv_folds, scoring='accuracy')
                landmarkers["landmarker_naive_bayes"] = float(np.mean(nb_scores))
        except Exception as e:
            pass  # Fallback to default 0.0 if dataset cannot be landmarked
            
        return landmarkers
