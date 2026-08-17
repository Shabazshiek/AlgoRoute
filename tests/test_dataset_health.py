# pyrefly: ignore [missing-import]
import pytest
import pandas as pd

from src.dataset_health import DatasetHealthAnalyzer
from src.meta_feature_extractor import MetaFeatureExtractor
from src.meta_router import MetaLearningStrategyRouter


def test_dataset_health_breast_cancer():
    df = pd.read_csv("data/sample_datasets/sample_breast_cancer.csv")
    X = df.drop(columns=["target"])
    y = df["target"]

    extractor = MetaFeatureExtractor()
    meta_feats = extractor.extract_meta_features(X, y, dataset_name="sample_breast_cancer")

    analyzer = DatasetHealthAnalyzer()
    health = analyzer.analyze_health(meta_feats)

    assert "status" in health
    assert "status_code" in health
    assert "profile" in health
    assert "findings" in health
    assert "warnings" in health

    assert health["profile"]["rows"] == 569
    assert health["profile"]["features"] == 30
    assert health["profile"]["classes"] == 2
    assert health["profile"]["missing_values_pct"] == "0.0%"
    assert health["status_code"] in ["GREEN", "YELLOW", "RED"]


def test_dataset_health_customer_churn_imbalance_detection():
    df = pd.read_csv("data/sample_datasets/sample_customer_churn.csv")
    X = df.drop(columns=["target"])
    y = df["target"]

    extractor = MetaFeatureExtractor()
    meta_feats = extractor.extract_meta_features(X, y, dataset_name="sample_customer_churn")

    analyzer = DatasetHealthAnalyzer()
    health = analyzer.analyze_health(meta_feats)

    assert health["profile"]["rows"] == 450
    assert health["profile"]["features"] == 7
    assert health["profile"]["numeric_features"] == 4
    assert health["profile"]["categorical_features"] == 3
    
    # Customer churn has 5.43:1 imbalance ratio -> should generate imbalance warning & review status
    assert health["status_code"] in ["YELLOW", "RED"]
    findings_str = " ".join(health["findings"]).lower()
    assert "imbalance" in findings_str or "class" in findings_str


def test_dataset_health_wine_quality_multiclass():
    df = pd.read_csv("data/sample_datasets/sample_wine_quality.csv")
    X = df.drop(columns=["target"])
    y = df["target"]

    extractor = MetaFeatureExtractor()
    meta_feats = extractor.extract_meta_features(X, y, dataset_name="sample_wine_quality")

    analyzer = DatasetHealthAnalyzer()
    health = analyzer.analyze_health(meta_feats)

    assert health["profile"]["rows"] == 178
    assert health["profile"]["features"] == 13
    assert health["profile"]["classes"] == 3


def test_router_predictions_unaffected_by_health_analysis():
    df = pd.read_csv("data/sample_datasets/sample_breast_cancer.csv")
    X = df.drop(columns=["target"])
    y = df["target"]

    router = MetaLearningStrategyRouter.load_model("data/processed/meta_router_model.joblib")
    
    # Predict best strategy
    rec = router.predict_best_strategy(X, y, dataset_name="sample_breast_cancer")

    analyzer = DatasetHealthAnalyzer()
    health = analyzer.analyze_health(rec["meta_features"])

    # Verify original router outputs remain untouched
    assert rec["recommended_algorithm"] in router.candidate_model_names
    assert "predicted_f1_score" in rec
    assert isinstance(health, dict)

