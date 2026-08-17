from typing import Dict, Any, List, Optional


class ExplanationEngine:

    def __init__(self):
        pass

    def explain_recommendation(
        self,
        meta_features: Dict[str, Any],
        recommended_algorithm: str,
        predicted_f1_score: float,
        rankings: List[Dict[str, Any]],
        recommendation_score: float
    ) -> Dict[str, Any]:
        # Extract metadata fields safely with defaults
        n_instances = int(meta_features.get("n_instances", 0))
        n_features = int(meta_features.get("n_features", 0))
        n_numeric = int(meta_features.get("n_numeric_features", 0))
        n_categorical = int(meta_features.get("n_categorical_features", 0))
        missing_ratio = float(meta_features.get("missing_value_ratio", 0.0))
        n_classes = int(meta_features.get("n_classes", 2))
        imbalance_ratio = float(meta_features.get("class_imbalance_ratio", 1.0))
        ratio_numeric = float(meta_features.get("ratio_numeric_features", 1.0))
        ratio_inst_feat = float(meta_features.get("ratio_instances_to_features", 0.0))
        mean_corr = float(meta_features.get("mean_correlation_abs", 0.0))
        skew_mean = float(meta_features.get("skewness_mean", 0.0))
        landmarker_stump = float(meta_features.get("landmarker_decision_stump", 0.0))
        landmarker_nb = float(meta_features.get("landmarker_naive_bayes", 0.0))

        # 1. Recommendation Summary (Primary Evidence & Rank)
        summary = (
            f"{recommended_algorithm} is ranked as the Top-1 strategy by the Meta-Router, "
            f"with a predicted F1 score of {predicted_f1_score:.4f} and a Strategy Recommendation Score of {recommendation_score:.1f} / 100."
        )

        # 2. Dataset Profile (Factual Observed Characteristics)
        dataset_profile = {
            "rows": n_instances,
            "features": n_features,
            "missing_values_pct": f"{missing_ratio * 100:.1f}%",
            "classes": n_classes,
            "numeric_features": n_numeric,
            "categorical_features": n_categorical,
            "imbalance_ratio": f"{imbalance_ratio:.2f}"
        }

        # 3. Supporting Factors (Router Ranking Evidence + Meta-Feature Representation)
        supporting_factors = []

        # A. Primary Router Evidence (Model Rankings & Margins)
        if len(rankings) > 1:
            runner_up = rankings[1]
            margin = predicted_f1_score - runner_up["predicted_f1"]
            if margin > 0.02:
                supporting_factors.append(
                    f"Primary Evidence: Meta-Router assigns the highest predicted score to {recommended_algorithm} ({predicted_f1_score:.4f} F1), "
                    f"exceeding the second-ranked strategy ({runner_up['algorithm']}: {runner_up['predicted_f1']:.4f} F1) by a margin of {margin:.4f}."
                )
            else:
                supporting_factors.append(
                    f"Primary Evidence: Meta-Router assigns Top-1 rank to {recommended_algorithm} ({predicted_f1_score:.4f} F1), "
                    f"leading the runner-up strategy ({runner_up['algorithm']}: {runner_up['predicted_f1']:.4f} F1)."
                )

        # B. Meta-Feature Vector Representation (Descriptive, Non-Causal)
        if ratio_numeric >= 0.95:
            supporting_factors.append(
                f"Feature Composition: Dataset contains 100% continuous numerical features ({n_numeric}/{n_features}), "
                f"which is represented in the router's input vector."
            )
        elif n_categorical > 0:
            supporting_factors.append(
                f"Feature Composition: Dataset contains mixed feature types ({n_categorical} categorical, {n_numeric} numeric), "
                f"which is included in the meta-feature representation."
            )

        # Dataset scale & feature density
        supporting_factors.append(
            f"Dataset Dimensions: Sample size is {n_instances} rows across {n_features} features "
            f"(instance-to-feature ratio: {ratio_inst_feat:.1f}:1), recorded in the dataset profile."
        )

        # Class imbalance
        if imbalance_ratio >= 1.5:
            supporting_factors.append(
                f"Target Imbalance: Dataset exhibits a class imbalance ratio of {imbalance_ratio:.2f}:1, "
                f"which is considered among the router's meta-features."
            )
        else:
            supporting_factors.append(
                "Target Structure: Dataset exhibits a balanced class distribution across target categories."
            )

        # Missing values
        if missing_ratio > 0.0:
            supporting_factors.append(
                f"Data Completeness: Dataset contains missing values ({missing_ratio*100:.1f}% of cells), "
                f"where fold-safe median/mode imputation is applied during benchmarking."
            )
        else:
            supporting_factors.append("Data Completeness: Zero missing values observed across feature columns.")

        # Statistical Meta-Features
        if abs(skew_mean) > 1.0:
            supporting_factors.append(
                f"Distribution Shape: Dataset exhibits noticeable feature skewness (mean skewness: {skew_mean:.2f}), "
                f"which is represented in the statistical meta-feature vector."
            )
        if mean_corr >= 0.3:
            supporting_factors.append(
                f"Feature Correlation: Dataset exhibits feature correlation structure (mean absolute correlation: {mean_corr:.2f}), "
                f"included in the router's correlation meta-features."
            )

        # Landmarker Probes (Explicitly described as baseline probes, not proof of optimality)
        if landmarker_stump > 0.0:
            supporting_factors.append(
                f"Landmarking Probe: Decision Stump 1-split baseline produced a probe accuracy of {landmarker_stump*100:.1f}%. "
                f"This fast probe result is included as a meta-feature describing baseline decision boundary behavior."
            )
        if landmarker_nb > 0.0:
            supporting_factors.append(
                f"Landmarking Probe: Naive Bayes baseline produced a probe accuracy of {landmarker_nb*100:.1f}%. "
                f"This fast probe result is included as a meta-feature describing baseline behavior and is not interpreted as proof of feature independence."
            )

        # 4. Factual Deployment Cautions
        cautions = []
        if imbalance_ratio >= 3.0:
            cautions.append(
                f"Dataset contains target class imbalance ({imbalance_ratio:.2f}:1 ratio). "
                f"Consider monitoring precision and recall across minority classes during model deployment."
            )
        if n_instances < 300:
            cautions.append(
                f"Compact dataset size ({n_instances} instances). "
                f"Validation metrics may exhibit cross-validation variance across small sample splits."
            )
        if n_features > 50 and ratio_inst_feat < 10.0:
            cautions.append(
                f"High feature count relative to samples ({n_features} features for {n_instances} rows). "
                f"Consider evaluating feature importance or dimensionality reduction during deployment."
            )
        if missing_ratio > 0.10:
            cautions.append(
                f"Missing data present ({missing_ratio*100:.1f}% of cells). "
                f"Verify that domain-appropriate imputation is maintained in production pipelines."
            )

        return {
            "summary": summary,
            "recommended_algorithm": recommended_algorithm,
            "recommendation_score": recommendation_score,
            "dataset_profile": dataset_profile,
            "supporting_factors": supporting_factors,
            "cautions": cautions
        }
