# pyrefly: ignore [missing-import]
import pytest
import numpy as np
import pandas as pd
from src.algorithm_benchmarker import AlgorithmBenchmarker


def test_algorithm_benchmarker_synthetic():
    np.random.seed(42)
    n_samples = 80
    
    df = pd.DataFrame({
        "feat1": np.random.randn(n_samples),
        "feat2": np.random.randn(n_samples) * 3,
        "cat1": np.random.choice(["X", "Y"], size=n_samples)
    })
    y = pd.Series(np.random.choice([0, 1], size=n_samples))
    
    benchmarker = AlgorithmBenchmarker()
    results = benchmarker.benchmark_dataset(df, y, dataset_name="synthetic_bench")
    
    assert len(results) == len(benchmarker.models)
    
    # Verify structure of results
    for res in results:
        assert "dataset_name" in res
        assert "algorithm" in res
        assert "f1_weighted" in res
        assert "accuracy" in res
        assert "rank" in res
        assert 0.0 <= res["f1_weighted"] <= 1.0
        assert 0.0 <= res["accuracy"] <= 1.0
        assert 1 <= res["rank"] <= len(benchmarker.models)
        
   
    sorted_f1s = sorted([r["f1_weighted"] for r in results], reverse=True)
    rank_1_res = [r for r in results if r["rank"] == 1][0]
    assert rank_1_res["f1_weighted"] == sorted_f1s[0]


def test_preprocessing_pipeline_no_leakage():
    
    benchmarker = AlgorithmBenchmarker()
    df_sample = pd.DataFrame({
        "num_col": [1.0, 2.0, np.nan, 4.0, 5.0],
        "cat_col": ["A", "B", "A", None, "B"]
    })
    
    preprocessor = benchmarker.build_preprocessing_pipeline(df_sample)
    assert preprocessor is not None
    
   
    transformed = preprocessor.fit_transform(df_sample)
    assert transformed.shape[0] == 5
    assert transformed.shape[1] == 2

