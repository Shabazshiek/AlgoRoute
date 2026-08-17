# pyrefly: ignore [missing-import]
import pytest
import numpy as np
import pandas as pd
from src.meta_router import MetaLearningStrategyRouter


@pytest.fixture
def synthetic_meta_learning_dataset():
    
    np.random.seed(42)
    n_datasets = 15
    
    records = []
    algorithms = ["LogisticRegression", "DecisionTree", "RandomForest", "GradientBoosting", "KNN", "GaussianNB"]
    
    for i in range(n_datasets):
        n_inst = np.random.randint(50, 1000)
        n_feat = np.random.randint(2, 20)
        
        row = {
            "dataset_name": f"synthetic_ds_{i}",
            "openml_id": 1000 + i,
            "n_instances": n_inst,
            "n_features": n_feat,
            "ratio_instances_to_features": float(n_inst / n_feat),
            "n_numeric_features": n_feat - 1,
            "n_categorical_features": 1,
            "ratio_numeric_features": 0.8,
            "ratio_categorical_features": 0.2,
            "n_missing_values": 0,
            "missing_value_ratio": 0.0,
            "n_classes": 2,
            "class_imbalance_ratio": 1.2,
            "majority_class_percentage": 0.55,
            "skewness_mean": float(np.random.randn()),
            "skewness_std": 0.5,
            "kurtosis_mean": float(np.random.randn()),
            "kurtosis_std": 0.5,
            "mean_correlation_abs": 0.3,
            "class_entropy": 0.98,
            "normalized_class_entropy": 0.98,
            "landmarker_decision_stump": float(np.random.uniform(0.5, 0.8)),
            "landmarker_naive_bayes": float(np.random.uniform(0.5, 0.85))
        }
        
        # Add random benchmark F1 scores for each candidate algorithm
        scores = {}
        for algo in algorithms:
            s = float(np.random.uniform(0.6, 0.95))
            row[algo] = s
            scores[algo] = s
            
        best_algo = max(scores, key=scores.get)
        row["best_algorithm"] = best_algo
        row["best_f1_score"] = scores[best_algo]
        
        records.append(row)
        
    return pd.DataFrame(records)


def test_meta_router_fit_and_predict(synthetic_meta_learning_dataset):
    router = MetaLearningStrategyRouter(random_state=42)
    router.fit(synthetic_meta_learning_dataset)
    
    assert router.is_fitted_ is True
    assert len(router.feature_names_) > 0
    
    # Extract feature importances
    df_imp = router.get_meta_feature_importances()
    assert isinstance(df_imp, pd.DataFrame)
    assert "meta_feature" in df_imp.columns
    assert "importance" in df_imp.columns
    assert len(df_imp) == len(router.feature_names_)
    
    # Unseen tabular dataset
    np.random.seed(99)
    X_unseen = pd.DataFrame({
        "num1": np.random.randn(50),
        "num2": np.random.randn(50) * 2,
        "cat1": np.random.choice(["A", "B"], size=50)
    })
    y_unseen = pd.Series(np.random.choice([0, 1], size=50))
    
    rec = router.predict_best_strategy(X_unseen, y_unseen, dataset_name="unseen_test")
    
    assert rec["dataset_name"] == "unseen_test"
    assert rec["recommended_algorithm"] in router.candidate_model_names
    assert isinstance(rec["predicted_f1_score"], float)
    assert rec["model_instance"] is not None
    assert len(rec["strategy_rankings"]) == len(router.candidate_model_names)


def test_meta_router_evaluation(synthetic_meta_learning_dataset):
    router = MetaLearningStrategyRouter(random_state=42)
    eval_res = router.evaluate_router(synthetic_meta_learning_dataset, n_splits=3)
    
    assert "meta_router_avg_f1" in eval_res
    assert "oracle_avg_f1" in eval_res
    assert "default_baseline_rf_avg_f1" in eval_res
    assert "random_baseline_avg_f1" in eval_res
    assert "top1_accuracy" in eval_res
    assert "top3_hit_rate" in eval_res
    assert "average_regret" in eval_res
    assert eval_res["n_samples"] == len(synthetic_meta_learning_dataset)
    assert 0.0 <= eval_res["meta_router_avg_f1"] <= 1.0
    assert 0.0 <= eval_res["top1_accuracy"] <= 1.0
    assert 0.0 <= eval_res["top3_hit_rate"] <= 1.0
    assert eval_res["top3_hit_rate"] >= eval_res["top1_accuracy"]
    assert eval_res["average_regret"] >= 0.0



def test_meta_router_save_load(synthetic_meta_learning_dataset, tmp_path):
    router = MetaLearningStrategyRouter(random_state=42)
    router.fit(synthetic_meta_learning_dataset)
    
    save_path = str(tmp_path / "meta_router.joblib")
    router.save_model(save_path)
    
    loaded_router = MetaLearningStrategyRouter.load_model(save_path)
    assert loaded_router.is_fitted_ is True
    assert loaded_router.feature_names_ == router.feature_names_


def test_meta_router_hybrid_alignment(synthetic_meta_learning_dataset):
    
    router = MetaLearningStrategyRouter(random_state=42)
    router.fit(synthetic_meta_learning_dataset)
    
    
    X_meta, _, _, _ = router._prepare_features_and_targets(synthetic_meta_learning_dataset)
    X_imp = router.imputer.transform(X_meta.head(2))
    
    preds = router._predict_hybrid_scores(router.regressor, router.classifier, X_imp)
    assert len(preds) == 2
    for best_algo, reg_best_score, score_dict, ranked in preds:
        assert best_algo in router.candidate_model_names
        assert len(score_dict) == len(router.candidate_model_names)
        assert len(ranked) == len(router.candidate_model_names)


