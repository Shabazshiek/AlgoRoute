# pyrefly: ignore [missing-import]
import pytest
import pandas as pd

from src.explanation_engine import ExplanationEngine
from src.meta_feature_extractor import MetaFeatureExtractor
from src.meta_router import MetaLearningStrategyRouter


@pytest.fixture
def sample_meta_features():
    return {
        "n_instances": 569,
        "n_features": 30,
        "ratio_instances_to_features": 18.96,
        "n_numeric_features": 30,
        "n_categorical_features": 0,
        "ratio_numeric_features": 1.0,
        "ratio_categorical_features": 0.0,
        "n_missing_values": 0,
        "missing_value_ratio": 0.0,
        "n_classes": 2,
        "class_imbalance_ratio": 1.68,
        "majority_class_percentage": 0.627,
        "skewness_mean": 1.735,
        "skewness_std": 1.253,
        "kurtosis_mean": 7.735,
        "kurtosis_std": 12.547,
        "mean_correlation_abs": 0.394,
        "class_entropy": 0.952,
        "normalized_class_entropy": 0.952,
        "landmarker_decision_stump": 0.884,
        "landmarker_naive_bayes": 0.936
    }


def test_explanation_engine_structure(sample_meta_features):
    engine = ExplanationEngine()
    rankings = [
        {"rank": 1, "algorithm": "RandomForest", "predicted_f1": 0.955},
        {"rank": 2, "algorithm": "GradientBoosting", "predicted_f1": 0.942},
        {"rank": 3, "algorithm": "LogisticRegression", "predicted_f1": 0.930}
    ]
    
    res = engine.explain_recommendation(
        meta_features=sample_meta_features,
        recommended_algorithm="RandomForest",
        predicted_f1_score=0.955,
        rankings=rankings,
        recommendation_score=85.0
    )

    assert "summary" in res
    assert "dataset_profile" in res
    assert "supporting_factors" in res
    assert "cautions" in res
    
    assert res["dataset_profile"]["rows"] == 569
    assert res["dataset_profile"]["features"] == 30
    assert len(res["supporting_factors"]) > 0
    assert "RandomForest" in res["summary"]
    assert "Top-1 strategy" in res["summary"]


def test_no_misleading_causal_language(sample_meta_features):
    engine = ExplanationEngine()
    rankings = [
        {"rank": 1, "algorithm": "LogisticRegression", "predicted_f1": 0.948},
        {"rank": 2, "algorithm": "KNN", "predicted_f1": 0.500}
    ]
    
    res = engine.explain_recommendation(
        meta_features=sample_meta_features,
        recommended_algorithm="LogisticRegression",
        predicted_f1_score=0.948,
        rankings=rankings,
        recommendation_score=80.5
    )

    all_text = " ".join([res["summary"]] + res["supporting_factors"] + res["cautions"])
    
    # Assert absence of misleading causal terms
    forbidden_terms = ["proves feature independence", "favors algorithm", "causes", "guarantees", "proves"]
    for term in forbidden_terms:
        assert term.lower() not in all_text.lower(), f"Forbidden causal term '{term}' found in explanation text."

    # Assert presence of non-causal descriptors & landmarker probe language
    assert "Primary Evidence" in all_text
    assert "Landmarking Probe" in all_text
    assert "not interpreted as proof" in all_text


def test_explanation_engine_graceful_missing_keys():
    engine = ExplanationEngine()
    sparse_meta = {"n_instances": 100, "n_features": 5}
    
    res = engine.explain_recommendation(
        meta_features=sparse_meta,
        recommended_algorithm="DecisionTree",
        predicted_f1_score=0.80,
        rankings=[{"rank": 1, "algorithm": "DecisionTree", "predicted_f1": 0.80}],
        recommendation_score=75.0
    )
    
    assert res["recommended_algorithm"] == "DecisionTree"
    assert res["dataset_profile"]["rows"] == 100
    assert res["dataset_profile"]["features"] == 5


def test_router_prediction_unchanged_by_explanation():
    df_cancer = pd.read_csv("data/sample_datasets/sample_breast_cancer.csv")
    X = df_cancer.drop(columns=["target"])
    y = df_cancer["target"]

    extractor = MetaFeatureExtractor()
    meta_feats = extractor.extract_meta_features(X, y, dataset_name="sample_breast_cancer")

    engine = ExplanationEngine()
    explanation = engine.explain_recommendation(
        meta_features=meta_feats,
        recommended_algorithm="RandomForest",
        predicted_f1_score=0.95,
        rankings=[{"rank": 1, "algorithm": "RandomForest", "predicted_f1": 0.95}],
        recommendation_score=85.0
    )

    assert meta_feats["n_instances"] == 569
    assert meta_feats["n_features"] == 30
    assert isinstance(explanation, dict)
