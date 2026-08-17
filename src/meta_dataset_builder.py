import os
import logging
from typing import List
import pandas as pd
from src.dataset_fetcher import OpenMLDatasetFetcher
from src.meta_feature_extractor import MetaFeatureExtractor

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logger = logging.getLogger(__name__)

# Standard curated set of OpenML datasets for Meta-Learning Strategy Router
DEFAULT_OPENML_DATASETS = [
    # Original 10 Datasets
    61,    # iris
    31,    # credit-g
    37,    # diabetes
    1464,  # blood-transfusion-service-center
    1480,  # ilpd (liver-patients)
    1489,  # phoneme
    1510,  # wdbc (breast cancer)
    1462,  # banknote-authentication
    1049,  # pc4 (software defect detection)
    40981, # Australian
    
    # Candidate Expansion Datasets from Completion #5A Audit
    3,     # kr-vs-kp (chess)
    11,    # balance-scale
    12,    # mstep / vehicle
    14,    # mbreast / cancer
    15,    # breast-w
    18,    # mcar / car
    23,    # cmc
    24,    # mushroom
    28,    # optdigits
    29,    # wave-energy
    32,    # pendigits
    36,    # segment
    44,    # spambase
    46,    # splice
    48,    # bio-assay
    50,    # tic-tac-toe
    54,    # vehicle
    151,   # electricity
    179,   # adult
    182,   # satimage
    188,   # eucalyptus
    300,   # isolet
    310,   # mammography
    1050,  # pc3
    1063,  # kc2
    1067,  # kc1
    1068,  # pc1
    1461,  # bank-marketing
    1467,  # climate-model
    1478,  # har (human activity recognition)
    1485,  # madelon
    1494,  # qsar-biodeg
    1497,  # wall-following
    1501,  # semeion
    1502,  # skin-segmentation
    1504,  # steel-plates-fault
    1512,  # dermo-pat
    1590,  # adult / census
    40975, # car
    40978, # JapaneseCredit
    40979, # Ionosphere
    40982, # steel-plates-fault
    40983, # wilt
    40984, # segment
    40992, # ThoraricSurgery
    40994, # climate-model-simulation
    41027  # dress-sales
]



class MetaDatasetBuilder:
    """Automates meta-feature generation across multiple datasets."""

    def __init__(self, output_dir: str = "data/processed"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.fetcher = OpenMLDatasetFetcher()
        self.extractor = MetaFeatureExtractor()

    def build_meta_features_inventory(self, dataset_ids: List[int] = DEFAULT_OPENML_DATASETS) -> str:
        """
        Extracts meta-features for listed OpenML datasets and exports to CSV.
        """
        records = []
        logger.info(f"Starting meta-feature extraction for {len(dataset_ids)} datasets...")
        
        for dataset_id in dataset_ids:
            try:
                X, y, meta = self.fetcher.fetch_dataset_by_id(dataset_id)
                dataset_name = f"openml_{dataset_id}_{meta['name']}"
                
                # Save raw dataset copy locally
                self.fetcher.save_raw_dataset(X, y, dataset_name)
                
                # Extract meta-features
                meta_feats = self.extractor.extract_meta_features(X, y, dataset_name=dataset_name)
                meta_feats["openml_id"] = dataset_id
                records.append(meta_feats)
                logger.info(f"Successfully processed dataset: {meta['name']} (ID: {dataset_id})")
            except Exception as e:
                logger.error(f"Failed to process OpenML dataset ID {dataset_id}: {str(e)}")

        df_meta = pd.DataFrame(records)
        output_file = os.path.join(self.output_dir, "meta_features_inventory.csv")
        df_meta.to_csv(output_file, index=False)
        logger.info(f"Meta-features inventory created at: {output_file}")
        return output_file


if __name__ == "__main__":
    builder = MetaDatasetBuilder()
    builder.build_meta_features_inventory()
