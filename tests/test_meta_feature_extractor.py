# pyrefly: ignore [missing-import]
import pytest
import numpy as np
import pandas as pd
from src.meta_feature_extractor import MetaFeatureExtractor


def test_meta_feature_extraction_synthetic():
    np.random.seed(42)
    n_samples = 100
    
    df = pd.DataFrame({
        "num1": np.random.randn(n_samples),
        "num2": np.random.randn(n_samples) * 5 + 2,
        "cat1": np.random.choice(["A", "B", "C"], size=n_samples),
        "missing_col": [np.nan if i % 10 == 0 else np.random.randn() for i in range(n_samples)]
    })
    
    y = pd.Series(np.random.choice([0, 1], size=n_samples))
    
    extractor = MetaFeatureExtractor()
    meta = extractor.extract_meta_features(df, y, dataset_name="synthetic_test")
    
    assert meta["n_instances"] == 100
    assert meta["n_features"] == 4
    assert meta["n_numeric_features"] == 3
    assert meta["n_categorical_features"] == 1
    assert meta["n_classes"] == 2
    assert meta["n_missing_values"] == 10
    assert "class_entropy" in meta
    assert "landmarker_decision_stump" in meta
    assert "landmarker_naive_bayes" in meta
    assert 0.0 <= meta["landmarker_decision_stump"] <= 1.0
    assert 0.0 <= meta["landmarker_naive_bayes"] <= 1.0


def test_meta_feature_extraction_no_missing():
    df = pd.DataFrame({
        "f1": [1.0, 2.0, 3.0, 4.0, 5.0],
        "f2": [10.0, 20.0, 30.0, 40.0, 50.0]
    })
    y = pd.Series([0, 0, 1, 1, 1])
    
    extractor = MetaFeatureExtractor()
    meta = extractor.extract_meta_features(df, y, dataset_name="clean_test")
    
    assert meta["n_instances"] == 5
    assert meta["n_features"] == 2
    assert meta["n_missing_values"] == 0
    assert meta["missing_value_ratio"] == 0.0
    assert meta["n_classes"] == 2
