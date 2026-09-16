# AlgoRoute — Intelligent Machine Learning Strategy Recommendation Engine

> **IBM Project Use Case #20**: Meta-Learning Machine Learning Strategy Router  
> **Core Objective**: Automated, privacy-preserving machine learning algorithm recommendation for tabular datasets using meta-learning and landmarking probes.
> 
> *For a simple, plain-text student overview of this project, see [PROJECT_OVERVIEW.md](file:///d:/Meta-Learning%20Stratergy%20Router/PROJECT_OVERVIEW.md).*

---


##  Submission & Raw Data Notice

> [!IMPORTANT]
> **Raw Dataset Storage Notice (`data/raw/`)**:  
> To keep the submission package lightweight and manageable, the heavy raw OpenML CSV files inside `data/raw/` have been removed from this archive.  
> 
> **The prototype is 100% operational out-of-the-box without raw files!**  
> All pre-extracted dataset meta-features (`data/processed/meta_learning_dataset.csv`) and the pre-trained hybrid Meta-Router model (`data/processed/meta_router_model.joblib`) are pre-packaged and ready for immediate evaluation.  
> 
> If you wish to re-fetch raw OpenML datasets and rebuild the meta-learning dataset from scratch, see the **[Pipeline Re-Training Guide](#-re-building-the-dataset--training-from-scratch-optional)** below.

---

##  Key Features & Capabilities

- **21 Dataset Meta-Features**: Extracted statistical, structural, target class entropy, and landmarking probe metrics in seconds.
- **Hybrid Meta-Router**: Pre-trained machine learning router trained across OpenML benchmark datasets to predict expected F1 scores for candidate algorithms.
- **6 Candidate ML Strategies**: Evaluates **RandomForest**, **GradientBoosting**, **LogisticRegression**, **K-Nearest Neighbors (KNN)**, **DecisionTree**, and **Gaussian Naive Bayes**.
- **Explainable Recommendation Engine**: Science-backed explanations detailing why the Top-1 strategy was selected for the specific dataset topology.
- **Dataset Health & Suitability Analysis**: Automatic detection of sample size sufficiency, severe class imbalance, missing values, and extreme feature dimensionality.
- **100% Local Data Privacy**: Data processing is strictly performed in-memory. Uploaded CSV datasets are **never** written to disk or sent to external APIs.

---

##  Prerequisites & System Requirements

### Required Runtimes & Dependencies
- **Python**: Version 3.9, 3.10, 3.11, 3.12, 3.13, or 3.14.
- **Node.js**: Version 18.0.0 or higher (with `npm`).
- **Operating System**: Windows, macOS, or Linux.

---

##  Step-by-Step Installation Guide

Follow these simple steps to install and set up the prototype environment:

### Step 1: Clone / Unzip the Repository
Open your terminal or command prompt in the project root directory (`Meta-Learning Stratergy Router`):
```bash
cd "Meta-Learning Stratergy Router"
```

### Step 2: Create & Activate a Python Virtual Environment

- **On Windows (PowerShell / Command Prompt)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```

- **On macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 3: Install Backend Python Dependencies
Install all required scientific computing, web API, and testing libraries:
```bash
pip install -r requirements.txt
```

### Step 4: Install Frontend Node.js Dependencies
Navigate to the `frontend` folder and install NPM packages:
```bash
cd frontend
npm install
cd ..
```

---

##  How to Test the Prototype

We provide comprehensive automated test suites as well as sample datasets for hands-on evaluation.

### 1. Run Automated Backend Test Suite (Pytest)
Run `pytest` from the root directory to verify all core components, extractors, routers, health analyzers, and privacy guarantees:

```bash
pytest
```

#### What the 19 Automated Tests Cover:
- `tests/test_meta_feature_extractor.py`: Validates extraction of all 21 structural, statistical, class entropy, and landmarking meta-features.
- `tests/test_algorithm_benchmarker.py`: Tests 5-fold Stratified Cross-Validation pipelines with isolated preprocessing.
- `tests/test_dataset_health.py`: Verifies automated health checks (missingness, class imbalance, sample size, feature ratio).
- `tests/test_meta_router.py`: Checks Meta-Router training, F1 score predictions, ranking logic, and joblib serialization.
- `tests/test_explanation_engine.py`: Validates generation of scientific explanations for recommended algorithms.
- `tests/test_privacy.py`: Ensures uploaded files are processed strictly in-memory without disk persistence.

Expected Test Output:
```text
======================= 19 passed in 8.40s =======================
```

### 2. Testing with Pre-Packaged Sample Datasets
You can test the Meta-Router immediately using sample datasets provided in `data/sample_datasets/`:

| Sample Dataset File | Problem Type | Characteristics | Recommended Benchmark Focus |
|---|---|---|---|
| `data/sample_datasets/sample_breast_cancer.csv` | Binary Classification | 569 instances, 30 continuous features | High-dimensional numeric features |
| `data/sample_datasets/sample_customer_churn.csv` | Churn Prediction | 1,000 instances, mixed numeric & categorical | Non-linear tabular features |
| `data/sample_datasets/sample_wine_quality.csv` | Multiclass Quality | 1,599 instances, 11 chemical properties | Continuous non-linear interactions |

---

##  How to Run the Prototype

You can run and interact with AlgoRoute through the **Web Dashboard**, the **Swagger API Docs**, or **Python Scripts**.

### Method 1: Running the Full Web Dashboard (Recommended)

#### 1. Start the FastAPI Backend Server
In your activated virtual environment terminal (Root Directory):
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
- The API server will start at `http://127.0.0.1:8000`.

#### 2. Start the React Frontend Dashboard
Open a second terminal window, navigate to the `frontend` folder, and start Vite:
```bash
cd frontend
npm run dev
```
- The Web Dashboard will open at `http://localhost:5173`.

#### 3. Using the Dashboard:
1. Open `http://localhost:5173` in your browser.
2. Drag and drop any CSV dataset (or pick one from `data/sample_datasets/`).
3. Click **"Analyze Dataset & Route Strategy"**.
4. View the extracted **21 Meta-Features**, **Dataset Health Status**, **Top-1 Recommended ML Strategy**, **Predicted F1 Scores**, and **Scientific Explanation Breakdown**.

---

### Method 2: Testing via Swagger Interactive API Docs
Once the backend server is running (`http://127.0.0.1:8000`), open your browser to:
```text
http://127.0.0.1:8000/docs
```
- **`/api/recommend`** (POST): Upload a CSV file directly via the Swagger UI to receive complete json recommendations.
- **`/api/health-check`** (POST): Test dataset health diagnostics.
- **`/api/meta-features`** (POST): Extract raw 21 meta-features from any CSV dataset.

---

### Method 3: Running via Python API / CLI
You can also run prediction logic directly inside Python:

```python
import pandas as pd
from src.meta_feature_extractor import MetaFeatureExtractor
from src.meta_router import MetaLearningStrategyRouter
from src.explanation_engine import ExplanationEngine

# Load dataset
df = pd.read_csv("data/sample_datasets/sample_breast_cancer.csv")
X = df.drop(columns=[df.columns[-1]])
y = df[df.columns[-1]]

# 1. Extract Meta-Features
extractor = MetaFeatureExtractor()
meta_features = extractor.extract_meta_features(X, y, dataset_name="breast_cancer")

# 2. Predict Model Performance & Rank Strategies
router = MetaLearningStrategyRouter.load_model("data/processed/meta_router_model.joblib")
ranking = router.predict_strategy(meta_features)

# 3. Generate Scientific Explanation
engine = ExplanationEngine()
explanation = engine.generate_explanation(meta_features, ranking)

print(f"Top Recommended Algorithm: {ranking[0]['algorithm']}")
print(f"Predicted F1 Score: {ranking[0]['predicted_f1']:.4f}")
print("Explanation:", explanation["summary"])
```

---

##  Re-Building the Dataset & Training from Scratch (Optional)

If an evaluator or reviewer wants to re-fetch raw OpenML datasets and re-train the Meta-Router model end-to-end:

### Step 1: Download OpenML Datasets & Extract Meta-Features
This script fetches benchmark datasets from OpenML, saves raw CSV files to `data/raw/`, and extracts `data/processed/meta_features_inventory.csv`:
```bash
python -m src.meta_dataset_builder
```

### Step 2: Benchmark Candidate Models & Build Meta-Dataset
This script runs 5-fold cross-validation across all candidate algorithms to create `data/processed/meta_learning_dataset.csv`:
```bash
python -m src.meta_dataset_preparer
```

### Step 3: Train & Save Hybrid Meta-Router
This script trains the Meta-Router and saves the model artifact to `data/processed/meta_router_model.joblib`:
```bash
python -m src.meta_router
```

---

##  Repository Directory Structure

```text
Meta-Learning Stratergy Router/
├── backend/
│   └── main.py                     # FastAPI REST API endpoints & CORS configuration
├── data/
│   ├── raw/                        # Raw OpenML CSV files (Re-generated via meta_dataset_builder)
│   ├── processed/
│   │   ├── benchmark_results.csv   # Raw cross-validation evaluation metrics
│   │   ├── meta_features_inventory.csv # Extracted meta-features across datasets
│   │   ├── meta_learning_dataset.csv   # Unified meta-learning training dataset
│   │   └── meta_router_model.joblib    # Pre-trained Meta-Router model binary
│   └── sample_datasets/            # Clean CSV samples for quick testing & evaluation
├── frontend/                       # Vite + React Modern Web Dashboard UI
│   ├── src/                        # Dashboard components, charts, & API client
│   ├── package.json                # Frontend dependencies
│   └── vite.config.js              # Vite server configuration
├── src/                            # Core Algorithmic Framework
│   ├── __init__.py                 # Module exports
│   ├── dataset_fetcher.py          # OpenML API dataset download & local loader
│   ├── dataset_health.py           # Dataset health & quality analyzer
│   ├── explanation_engine.py       # Evidence-based scientific explanation generator
│   ├── meta_dataset_builder.py     # Automated batch meta-feature extractor
│   ├── meta_dataset_preparer.py    # Benchmark dataset evaluator & preprocessor
│   ├── meta_feature_extractor.py   # Extractor for all 21 dataset meta-features
│   └── meta_router.py              # Hybrid Meta-Learning Strategy Router model
├── tests/                          # Automated Pytest Test Suite
│   ├── test_algorithm_benchmarker.py
│   ├── test_dataset_health.py
│   ├── test_explanation_engine.py
│   ├── test_meta_feature_extractor.py
│   ├── test_meta_router.py
│   └── test_privacy.py
├── preparation.md                  # Comprehensive viva & project submission guide
├── README.md                       # Project documentation & execution instructions
└── requirements.txt                # Python backend dependencies
```

---

##  Scientific Foundation: The 21 Meta-Features

AlgoRoute calculates **21 dataset meta-features** grouped into 4 functional domains:

1. **Structural Meta-Features**: Sample size (`n_instances`), feature count (`n_features`), instance-to-feature ratio, numeric feature count/ratio, categorical feature count/ratio, missing value count/ratio.
2. **Target Class Meta-Features**: Class count (`n_classes`), majority class percentage, class imbalance ratio.
3. **Statistical Meta-Features**: Mean & std skewness, mean & std kurtosis, mean absolute Pearson feature correlation, target class entropy, normalized target entropy.
4. **Landmarking Probe Meta-Features**: Fast execution probe models (Decision Stump accuracy, Naive Bayes accuracy).

---

##  Project Alignment & Summary

- **Product Name**: AlgoRoute
- **Project Context**: IBM Project Use Case #20 — Meta-Learning Machine Learning Strategy Router
- **Key Guarantee**: Local, privacy-focused, evidence-backed strategy recommendation in under 3 seconds.
