"""
Meta-Learning Strategy Router Core Package
"""
from src.dataset_fetcher import OpenMLDatasetFetcher
from src.meta_feature_extractor import MetaFeatureExtractor
from src.algorithm_benchmarker import AlgorithmBenchmarker
from src.meta_dataset_builder import MetaDatasetBuilder
from src.meta_dataset_preparer import MetaDatasetPreparer
from src.meta_router import MetaLearningStrategyRouter
from src.explanation_engine import ExplanationEngine
from src.dataset_health import DatasetHealthAnalyzer

__version__ = "0.1.0"
__all__ = [
    "OpenMLDatasetFetcher",
    "MetaFeatureExtractor",
    "AlgorithmBenchmarker",
    "MetaDatasetBuilder",
    "MetaDatasetPreparer",
    "MetaLearningStrategyRouter",
    "ExplanationEngine",
    "DatasetHealthAnalyzer"
]



