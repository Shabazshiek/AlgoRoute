import os
import re
import logging
from typing import Tuple, Dict, Any, Optional
import pandas as pd
# pyrefly: ignore [missing-import]
import openml

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class OpenMLDatasetFetcher:

    def __init__(self, raw_data_dir: str = "data/raw"):
        self.raw_data_dir = raw_data_dir
        os.makedirs(self.raw_data_dir, exist_ok=True)

    def fetch_dataset_by_id(self, dataset_id: int) -> Tuple[pd.DataFrame, pd.Series, Dict[str, Any]]:
        logger.info(f"Fetching OpenML dataset ID: {dataset_id}")
        dataset = openml.datasets.get_dataset(dataset_id, download_data=True, download_qualities=False)
        
        target_name = dataset.default_target_attribute
        X, y, categorical_indicator, attribute_names = dataset.get_data(
            target=target_name, dataset_format="dataframe"
        )
        
        metadata = {
            "dataset_id": dataset_id,
            "name": dataset.name,
            "target_attribute": target_name,
            "n_instances": X.shape[0] if X is not None else 0,
            "n_features": X.shape[1] if X is not None else 0,
            "categorical_indicator": categorical_indicator,
            "attribute_names": attribute_names
        }
        
        return X, y, metadata

    def save_raw_dataset(self, X: pd.DataFrame, y: pd.Series, dataset_name: str) -> str:
        safe_name = re.sub(r'[^\w\-]', '_', dataset_name)
        save_path = os.path.join(self.raw_data_dir, f"{safe_name}.csv")
        df = X.copy()
        df["target"] = y
        df.to_csv(save_path, index=False)
        logger.info(f"Saved dataset '{safe_name}' to {save_path}")
        return save_path

    def load_local_csv(self, file_path: str, target_column: str = "target") -> Tuple[pd.DataFrame, pd.Series]:
        df = pd.read_csv(file_path)
        if target_column not in df.columns:
            target_column = df.columns[-1]
            
        X = df.drop(columns=[target_column])
        y = df[target_column]
        return X, y

