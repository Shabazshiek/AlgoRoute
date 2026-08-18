# Project Overview - AlgoRoute

## What is AlgoRoute?

AlgoRoute is a Meta-Learning Machine Learning Strategy Router designed for tabular datasets. This project was developed for IBM Use Case #20.

In machine learning, when you get a new CSV dataset, it is often hard to decide which algorithm to use right away. Normally, a student or data scientist has to manually train and test multiple models like Logistic Regression, Random Forest, Gradient Boosting, and KNN to see which one works best. This trial-and-error approach takes a lot of time and computing power.

AlgoRoute solves this problem by analyzing the dataset itself instead of training full models on it. In less than 3 seconds, it extracts key structural and statistical properties of the dataset (called meta-features) and uses a pre-trained Meta-Router model to predict which algorithm will perform best.

---

## Why We Built This Project

1. The No Free Lunch Theorem: In machine learning, no single algorithm works best for all datasets. An algorithm that performs well on simple numeric data might perform poorly on complex or imbalanced datasets.
2. Saving Time and Compute: Automated ML tools (AutoML) usually train dozens of models on your data, which takes hours. AlgoRoute recommends the best model almost instantly by reading dataset characteristics.
3. Data Privacy: Many web tools send user data to cloud servers or external APIs. AlgoRoute processes all uploaded CSV files strictly in-memory on your local machine. The data is never written to disk or sent outside your system.

---

## How AlgoRoute Works

The workflow of the project follows these main steps:

Step 1: Dataset Upload
The user uploads a CSV dataset through the React web dashboard or sends it via the API.

Step 2: Meta-Feature Extraction
The system calculates 21 specific meta-features from the dataset. These include:
- Structural characteristics: Number of rows, number of columns, ratio of rows to columns, percentage of numeric vs categorical features, and missing value counts.
- Target class characteristics: Number of classes, majority class percentage, and class imbalance ratio.
- Statistical characteristics: Feature skewness, kurtosis, average feature correlations, and target entropy.
- Landmarking probes: Quick micro-tests using simple models (Decision Stump and Naive Bayes) to gauge dataset complexity.

Step 3: Dataset Health Check
Before making recommendations, the system checks dataset quality. It flags potential issues such as very small sample sizes, extreme class imbalance, high missingness, or high feature dimensions.

Step 4: Meta-Routing & Strategy Recommendation
The 21 extracted meta-features are passed into the Meta-Router model. This router was trained on benchmark results across various datasets from OpenML. It predicts the expected F1-scores for 6 candidate algorithms:
- Random Forest
- Gradient Boosting
- Logistic Regression
- K-Nearest Neighbors (KNN)
- Decision Tree
- Gaussian Naive Bayes

Step 5: Explainable AI
The system generates a human-readable explanation justifying why the top algorithm was chosen based on the extracted meta-features (for example, recommending Random Forest due to non-linear feature structures or high feature counts).

---

## Project Structure and Key Files

Here is a breakdown of what the different files in this repository do:

- src/meta_feature_extractor.py: Contains the code that calculates all 21 structural, statistical, and probe meta-features from a pandas DataFrame.
- src/dataset_health.py: Performs quality checks on the uploaded dataset and generates warnings or health status reports.
- src/meta_router.py: Defines the Meta-Learning Strategy Router model that predicts F1 scores and ranks the candidate algorithms.
- src/explanation_engine.py: Generates natural language explanations justifying the top recommendation.
- src/algorithm_benchmarker.py: Benchmarks candidate algorithms across datasets using 5-fold cross-validation.
- src/dataset_fetcher.py: Downloads benchmark datasets from OpenML when building the meta-learning dataset.
- src/meta_dataset_builder.py: Automates extraction of meta-features across benchmark datasets.
- src/meta_dataset_preparer.py: Prepares the final meta-learning training dataset.
- backend/main.py: The FastAPI backend server providing REST API endpoints (/api/recommend, /api/health-check, /api/meta-features).
- frontend/: The web frontend built using React and Vite. It provides an intuitive drag-and-drop dashboard to view recommendations, charts, and explanations.
- data/sample_datasets/: Contains sample CSV files (breast cancer, customer churn, wine quality) that can be used to test the project right away.
- data/processed/: Contains pre-extracted meta-features and the trained model file (meta_router_model.joblib).
- tests/: Contains automated test files for verifying the backend code using pytest.

---

## Note Regarding Raw Data Files (data/raw/)

When submitting or sharing this project, the data/raw/ folder may be kept empty or lightweight. This is done intentionally to avoid sharing very large raw benchmark CSV files downloaded from OpenML.

You do not need the raw dataset files to run, test, or evaluate the application. The processed training data and the pre-trained model file are already saved in data/processed/meta_router_model.joblib. 

If anyone wishes to re-download the raw OpenML datasets and re-train the model from scratch, they can run the script python -m src.meta_dataset_builder.

---

## How to Run the Project

1. Set up the Python virtual environment and install backend requirements:
   python -m venv venv
   source venv/bin/activate (or .\venv\Scripts\activate on Windows)
   pip install -r requirements.txt

2. Run the FastAPI Backend Server:
   python -m uvicorn backend.main:app --reload --port 8000

3. Run the React Web Dashboard:
   cd frontend
   npm install
   npm run dev

4. Open your browser and navigate to http://localhost:5173 to test the project.

5. Run Automated Tests:
   pytest
