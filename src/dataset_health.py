from typing import Dict, Any, List


class DatasetHealthAnalyzer:


    def __init__(self):
        pass

    def analyze_health(self, meta_features: Dict[str, Any]) -> Dict[str, Any]:
        
        n_instances = int(meta_features.get("n_instances", 0))
        n_features = int(meta_features.get("n_features", 0))
        n_numeric = int(meta_features.get("n_numeric_features", 0))
        n_categorical = int(meta_features.get("n_categorical_features", 0))
        missing_ratio = float(meta_features.get("missing_value_ratio", 0.0))
        n_classes = int(meta_features.get("n_classes", 2))
        imbalance_ratio = float(meta_features.get("class_imbalance_ratio", 1.0))
        ratio_inst_feat = float(meta_features.get("ratio_instances_to_features", 0.0))

        # 1. Dataset Health Profile
        profile = {
            "rows": n_instances,
            "features": n_features,
            "numeric_features": n_numeric,
            "categorical_features": n_categorical,
            "missing_values_pct": f"{missing_ratio * 100:.1f}%",
            "classes": n_classes,
            "imbalance_ratio": f"{imbalance_ratio:.2f}:1",
            "instance_to_feature_ratio": f"{ratio_inst_feat:.1f}"
        }

        findings = []
        warnings = []

        # 2. Missing Value Analysis
        if missing_ratio > 0.15:
            findings.append(f"High missing value ratio detected ({missing_ratio * 100:.1f}% of cells).")
            warnings.append("Severe missing data ratio (>15%). Verify imputation strategy aligns with business domain expectations.")
        elif missing_ratio > 0.0:
            findings.append(f"Moderate missing values detected ({missing_ratio * 100:.1f}% of cells). Automated fold-safe imputation applied.")
        else:
            findings.append("Data Completeness: Zero missing values detected across feature columns.")

        # 3. Class Imbalance Analysis
        if imbalance_ratio >= 8.0:
            findings.append(f"Extreme class imbalance detected ({imbalance_ratio:.2f}:1 ratio).")
            warnings.append(f"Extreme target class imbalance ({imbalance_ratio:.2f}:1). Monitor minority class recall and precision.")
        elif imbalance_ratio >= 3.0:
            findings.append(f"Significant class imbalance detected ({imbalance_ratio:.2f}:1 ratio).")
            warnings.append(f"Target class imbalance ({imbalance_ratio:.2f}:1 ratio). Precision-recall monitoring recommended during deployment.")
        elif imbalance_ratio >= 1.5:
            findings.append(f"Moderate class imbalance detected ({imbalance_ratio:.2f}:1 ratio).")
        else:
            findings.append("Target Balance: Class distribution is relatively balanced across target categories.")

        # 4. Feature Type Composition
        if n_numeric > 0 and n_categorical > 0:
            findings.append(f"Mixed Feature Types: Contains {n_numeric} continuous numeric and {n_categorical} categorical features.")
        elif n_numeric == n_features:
            findings.append(f"Numeric Dominance: 100% continuous numerical features ({n_numeric}/{n_features}).")
        else:
            findings.append(f"Categorical Dominance: High ratio of categorical features ({n_categorical}/{n_features}).")

        # 5. Dataset Scale & Sample Size
        if n_instances < 50:
            findings.append(f"Very small sample size ({n_instances} rows).")
            warnings.append("Sample size is under 50 rows. Cross-validation evaluation metrics may exhibit high variance.")
        elif n_instances < 300:
            findings.append(f"Compact dataset sample size ({n_instances} rows).")
            warnings.append("Compact sample size (<300 rows). Monitor cross-validation variance across folds.")
        elif n_instances >= 10000:
            findings.append(f"Large-scale dataset ({n_instances} rows). Provides strong statistical sample power.")

        # 6. Dimensionality & Feature-to-Sample Density
        if ratio_inst_feat < 5.0 and n_features > 20:
            findings.append(f"High feature dimensionality relative to samples ({n_features} features for {n_instances} rows).")
            warnings.append("High feature-to-sample ratio (<5:1). Feature selection or regularized splitting is recommended.")

        # 7. Determine Overall Dataset Health Status
        # 🔴 ATTENTION REQUIRED: Severe missingness (>15%), extreme imbalance (>8:1), or tiny sample (<50 rows)
        if missing_ratio > 0.15 or imbalance_ratio >= 8.0 or n_instances < 50:
            status = "ATTENTION REQUIRED"
            status_code = "RED"
            badge_color = "danger"
        # 🟡 REVIEW RECOMMENDED: Any warning condition present
        elif len(warnings) > 0 or missing_ratio > 0.0 or imbalance_ratio >= 3.0 or n_instances < 300:
            status = "REVIEW RECOMMENDED"
            status_code = "YELLOW"
            badge_color = "warning"
        # 🟢 HEALTHY: Clean, balanced, standard dataset
        else:
            status = "HEALTHY"
            status_code = "GREEN"
            badge_color = "success"

        return {
            "status": status,
            "status_code": status_code,
            "badge_color": badge_color,
            "profile": profile,
            "findings": findings,
            "warnings": warnings
        }
