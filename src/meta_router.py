import logging
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from src.meta_feature_extractor import MetaFeatureExtractor
from src.algorithm_benchmarker import get_default_candidate_models

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class MetaLearningStrategyRouter:
    """
    Meta-Learning Strategy Router.
    Predicts optimal candidate algorithms for unseen tabular datasets based on extracted meta-features.
    """

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.meta_feature_extractor = MetaFeatureExtractor()
        self.candidate_models = get_default_candidate_models()
        self.candidate_model_names = list(self.candidate_models.keys())
        
        # Meta-learner models
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=self.random_state)
        self.regressor = RandomForestRegressor(n_estimators=100, random_state=self.random_state)
        self.imputer = SimpleImputer(strategy="median")
        
        self.feature_names_: List[str] = []
        self.is_fitted_: bool = False

    def _prepare_features_and_targets(
        self, df_meta: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, List[str]]:
        """
        Extracts feature matrix X_meta, target classification series y_best,
        and target regression matrix Y_scores from the meta-learning dataset.
        """
        non_feature_cols = ["dataset_name", "openml_id", "best_algorithm", "best_f1_score"]
        # Candidate score columns present in the dataset
        score_cols = [col for col in self.candidate_model_names if col in df_meta.columns]
        
        exclude_cols = set(non_feature_cols + score_cols)
        feature_cols = [c for c in df_meta.columns if c not in exclude_cols]
        
        X_meta = df_meta[feature_cols].copy()
        
        # Clean numeric meta-features
        numeric_X = X_meta.select_dtypes(include=[np.number])
        feature_names = numeric_X.columns.tolist()
        
        y_best = df_meta["best_algorithm"] if "best_algorithm" in df_meta.columns else None
        Y_scores = df_meta[score_cols] if score_cols else None
        
        return numeric_X, y_best, Y_scores, feature_names

    def fit(self, df_meta_learning: pd.DataFrame) -> "MetaLearningStrategyRouter":
        """
        Fits both classification and multi-output regression meta-learners on the meta-dataset.
        """
        X_meta, y_best, Y_scores, feature_names = self._prepare_features_and_targets(df_meta_learning)
        self.feature_names_ = feature_names
        
        X_imputed = self.imputer.fit_transform(X_meta)
        
        if y_best is not None:
            self.classifier.fit(X_imputed, y_best)
            
        if Y_scores is not None and not Y_scores.empty:
            self.regressor.fit(X_imputed, Y_scores)
            
        self.is_fitted_ = True
        logger.info(f"MetaLearningStrategyRouter successfully fitted on {len(df_meta_learning)} dataset records.")
        return self

    def _predict_hybrid_scores(
        self, regressor: Any, classifier: Any, X_imp: np.ndarray
    ) -> List[Tuple[str, float, Dict[str, float], List[Tuple[str, float]]]]:
        """
        Single Source of Truth for Hybrid Meta-Router prediction & ranking logic.
        Blends regressor F1 predictions with classifier win probabilities:
        combined_score = 0.4 * reg_score + 0.6 * clf_prob
        """
        reg_preds = regressor.predict(X_imp)  # shape (n_samples, n_algorithms)
        
        if hasattr(classifier, "classes_") and len(classifier.classes_) > 0:
            clf_probs = classifier.predict_proba(X_imp)  # shape (n_samples, n_classes)
            classes = list(classifier.classes_)
        else:
            clf_probs = None
            classes = []
            
        results = []
        for i in range(len(X_imp)):
            reg_scores = reg_preds[i]
            reg_dict = dict(zip(self.candidate_model_names, reg_scores))
            
            if clf_probs is not None:
                clf_dict = dict(zip(classes, clf_probs[i]))
            else:
                clf_dict = {}
                
            score_dict = {}
            for algo in self.candidate_model_names:
                r_score = reg_dict.get(algo, 0.5)
                c_prob = clf_dict.get(algo, 0.0)
                combined = 0.4 * r_score + 0.6 * c_prob
                score_dict[algo] = float(combined)
                
            ranked = sorted(score_dict.items(), key=lambda item: item[1], reverse=True)
            best_algo, best_score = ranked[0]
            reg_best_score = float(reg_dict.get(best_algo, best_score))
            results.append((best_algo, reg_best_score, score_dict, ranked))
            
        return results

    def evaluate_router(self, df_meta_learning: pd.DataFrame, n_splits: int = 5) -> Dict[str, Any]:
        """
        Cross-validates Meta-Router performance using the DEPLOYED HYBRID ROUTER
        against Default Baseline (RandomForest), Random Selection Baseline, and Oracle Best.
        """
        X_meta, y_best, Y_scores, feature_names = self._prepare_features_and_targets(df_meta_learning)
        
        if Y_scores is None or Y_scores.empty:
            raise ValueError("Evaluation requires algorithm F1 score columns in df_meta_learning.")
            
        n_samples = len(df_meta_learning)
        n_folds = min(n_splits, n_samples)
        kf = KFold(n_splits=n_folds, shuffle=True, random_state=self.random_state)
        
        router_f1_scores = []
        default_f1_scores = []
        oracle_f1_scores = []
        random_f1_scores = []
        top1_correct = 0
        top3_correct = 0
        
        for train_idx, val_idx in kf.split(X_meta):
            X_train_raw, X_val_raw = X_meta.iloc[train_idx], X_meta.iloc[val_idx]
            Y_train, Y_val = Y_scores.iloc[train_idx], Y_scores.iloc[val_idx]
            y_train = y_best.iloc[train_idx] if y_best is not None else None
            
            # Fit imputer ONLY on training fold (Completion #1 safeguard preserved)
            fold_imputer = SimpleImputer(strategy="median")
            X_train = fold_imputer.fit_transform(X_train_raw)
            X_val = fold_imputer.transform(X_val_raw)
            
            # Train BOTH components of the Hybrid Router on training fold
            fold_reg = RandomForestRegressor(n_estimators=100, random_state=self.random_state)
            fold_reg.fit(X_train, Y_train)
            
            fold_clf = RandomForestClassifier(n_estimators=100, random_state=self.random_state)
            if y_train is not None and len(np.unique(y_train)) > 1:
                fold_clf.fit(X_train, y_train)
                
            # Call the EXACT SAME Hybrid prediction logic on validation fold
            hybrid_preds = self._predict_hybrid_scores(fold_reg, fold_clf, X_val)
            
            for i, local_val_idx in enumerate(val_idx):
                recommended_algo, _, _, ranked_strategies = hybrid_preds[i]
                true_scores = Y_val.iloc[i]
                
                # True F1 achieved by recommended algorithm
                router_f1 = true_scores[recommended_algo]
                router_f1_scores.append(router_f1)
                
                # Oracle F1 (best possible algorithm choice)
                oracle_f1 = true_scores.max()
                oracle_f1_scores.append(oracle_f1)
                
                # Default baseline F1 (always select RandomForest if present, else first model)
                default_algo = "RandomForest" if "RandomForest" in true_scores.index else true_scores.index[0]
                default_f1_scores.append(true_scores[default_algo])
                
                # Random choice baseline
                random_f1_scores.append(np.mean(true_scores))
                
                # Check top-1 match
                true_best_algo = true_scores.idxmax()
                if recommended_algo == true_best_algo:
                    top1_correct += 1
                    
                # Check top-3 hit rate
                top3_algos = [r[0] for r in ranked_strategies[:3]]
                if true_best_algo in top3_algos:
                    top3_correct += 1
                    
        avg_router_f1 = float(np.mean(router_f1_scores))
        avg_oracle_f1 = float(np.mean(oracle_f1_scores))
        avg_default_f1 = float(np.mean(default_f1_scores))
        avg_random_f1 = float(np.mean(random_f1_scores))
        
        top1_accuracy = float(top1_correct / n_samples)
        top3_hit_rate = float(top3_correct / n_samples)
        average_regret = float(avg_oracle_f1 - avg_router_f1)
        
        results = {
            "n_samples": n_samples,
            "n_folds": n_folds,
            "meta_router_avg_f1": avg_router_f1,          # Average Selected-Model F1
            "oracle_avg_f1": avg_oracle_f1,               # Oracle Best F1
            "default_baseline_rf_avg_f1": avg_default_f1, # Default RandomForest Baseline F1
            "random_baseline_avg_f1": avg_random_f1,     # Random Selection Baseline F1
            "top1_accuracy": top1_accuracy,               # Top-1 Selection Accuracy
            "top3_hit_rate": top3_hit_rate,               # Top-3 Hit Rate
            "average_regret": average_regret,             # Average Regret
            "improvement_over_default": float(avg_router_f1 - avg_default_f1),
            "improvement_over_random": float(avg_router_f1 - avg_random_f1)
        }

        
        logger.info(f"Cross-Validation complete: Meta-Router Avg F1 = {avg_router_f1:.4f} (Regret vs Oracle: {average_regret:.4f})")
        return results

    def get_meta_feature_importances(self) -> pd.DataFrame:
        """
        Extracts meta-feature importances from the trained regressor meta-learner.
        """
        if not self.is_fitted_:
            raise ValueError("Router is not fitted yet. Call fit() before requesting feature importances.")
            
        importances = self.regressor.feature_importances_
        df_importance = pd.DataFrame({
            "meta_feature": self.feature_names_,
            "importance": importances
        }).sort_values(by="importance", ascending=False).reset_index(drop=True)
        
        return df_importance

    def predict_best_strategy(
        self, X: pd.DataFrame, y: pd.Series, dataset_name: str = "unseen_dataset"
    ) -> Dict[str, Any]:
        
        if not self.is_fitted_:
            raise ValueError("Router must be fitted before predicting strategies.")
            
        # 1. Extract meta-features from input X, y
        meta_dict = self.meta_feature_extractor.extract_meta_features(X, y, dataset_name=dataset_name)
        
        # 2. Format features vector aligned with training feature_names_
        feat_vector = [meta_dict.get(fname, 0.0) for fname in self.feature_names_]
        X_vec = pd.DataFrame([feat_vector], columns=self.feature_names_)
        X_imp = self.imputer.transform(X_vec)
        
        # 3. Call the single source of truth Hybrid prediction logic
        hybrid_preds = self._predict_hybrid_scores(self.regressor, self.classifier, X_imp)
        best_algo_name, reg_best_score, score_dict, ranked_strategies = hybrid_preds[0]
        
        # Instantiate recommended model instance
        recommended_model_instance = self.candidate_models[best_algo_name]
        
        return {
            "dataset_name": dataset_name,
            "recommended_algorithm": best_algo_name,
            "predicted_f1_score": float(reg_best_score),
            "model_instance": recommended_model_instance,
            "all_predicted_scores": score_dict,
            "strategy_rankings": ranked_strategies,
            "meta_features": meta_dict
        }



    def save_model(self, file_path: str = "data/processed/meta_router_model.joblib") -> str:
        """
        Saves the fitted MetaLearningStrategyRouter object to disk.
        """
        import os
        import joblib
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        joblib.dump(self, file_path)
        logger.info(f"Saved trained MetaLearningStrategyRouter to {file_path}")
        return file_path

    @staticmethod
    def load_model(file_path: str = "data/processed/meta_router_model.joblib") -> "MetaLearningStrategyRouter":
        
        import joblib
        router = joblib.load(file_path)
        logger.info(f"Loaded MetaLearningStrategyRouter from {file_path}")
        return router

