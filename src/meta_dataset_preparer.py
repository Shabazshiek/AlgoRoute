import os
import logging
from typing import List, Dict, Any, Tuple
import pandas as pd
from src.dataset_fetcher import OpenMLDatasetFetcher
from src.algorithm_benchmarker import AlgorithmBenchmarker

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class MetaDatasetPreparer:
    """Prepares the training dataset for the Meta-Learning Strategy Router."""

    def __init__(self, raw_data_dir: str = "data/raw", processed_dir: str = "data/processed"):
        self.raw_data_dir = raw_data_dir
        self.processed_dir = processed_dir
        os.makedirs(self.processed_dir, exist_ok=True)
        self.fetcher = OpenMLDatasetFetcher(raw_data_dir=raw_data_dir)
        self.benchmarker = AlgorithmBenchmarker()

    def prepare_meta_learning_dataset(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Benchmarks algorithms across all cached raw datasets, saves benchmark_results.csv,
        and joins with meta_features_inventory.csv to construct meta_learning_dataset.csv.
        """
        all_benchmark_results = []
        raw_files = [f for f in os.listdir(self.raw_data_dir) if f.endswith(".csv")]
        
        logger.info(f"Found {len(raw_files)} raw datasets in {self.raw_data_dir}. Starting benchmarking...")
        
        for raw_file in raw_files:
            file_path = os.path.join(self.raw_data_dir, raw_file)
            dataset_name = os.path.splitext(raw_file)[0]
            try:
                X, y = self.fetcher.load_local_csv(file_path, target_column="target")
                bench_res = self.benchmarker.benchmark_dataset(X, y, dataset_name=dataset_name)
                all_benchmark_results.extend(bench_res)
                logger.info(f"Completed benchmarking for dataset: {dataset_name}")
            except Exception as e:
                logger.error(f"Error benchmarking dataset {dataset_name}: {str(e)}")

        df_benchmarks = pd.DataFrame(all_benchmark_results)
        benchmarks_path = os.path.join(self.processed_dir, "benchmark_results.csv")
        df_benchmarks.to_csv(benchmarks_path, index=False)
        logger.info(f"Saved benchmark results to: {benchmarks_path}")

        # Construct Meta-Learning Dataset (X_meta -> best_algorithm Y_meta)
        meta_inventory_path = os.path.join(self.processed_dir, "meta_features_inventory.csv")
        if not os.path.exists(meta_inventory_path):
            raise FileNotFoundError(f"Meta-features inventory not found at {meta_inventory_path}. Run Chapter 1 first.")

        df_meta_features = pd.read_csv(meta_inventory_path)
        
        # Identify top-performing algorithm per dataset (Rank 1)
        best_algos = (
            df_benchmarks.sort_values(by=["dataset_name", "f1_weighted"], ascending=[True, False])
            .groupby("dataset_name")
            .first()
            .reset_index()
        )
        
        best_algos = best_algos[["dataset_name", "algorithm", "f1_weighted"]].rename(
            columns={"algorithm": "best_algorithm", "f1_weighted": "best_f1_score"}
        )
        
        # Also create wide pivot of algorithm performance per dataset for multi-target learning
        df_algo_scores = df_benchmarks.pivot(
            index="dataset_name", columns="algorithm", values="f1_weighted"
        ).reset_index()
        
        # Merge meta-features with best algorithm target and performance matrix
        df_final = pd.merge(df_meta_features, best_algos, on="dataset_name", how="inner")
        df_final = pd.merge(df_final, df_algo_scores, on="dataset_name", how="inner")

        final_dataset_path = os.path.join(self.processed_dir, "meta_learning_dataset.csv")
        df_final.to_csv(final_dataset_path, index=False)
        logger.info(f"Successfully constructed Meta-Learning Dataset at: {final_dataset_path}")
        
        return df_benchmarks, df_final


if __name__ == "__main__":
    preparer = MetaDatasetPreparer()
    preparer.prepare_meta_learning_dataset()
