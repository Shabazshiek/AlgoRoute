import os
import io
# pyrefly: ignore [missing-import]
import pytest
import pandas as pd
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_privacy_endpoint():
    response = client.get("/api/privacy")
    assert response.status_code == 200
    data = response.json()
    
    assert data["processing_mode"] == "LOCAL"
    assert data["external_ai_upload"] is False
    assert data["persistent_user_dataset_storage"] is False
    assert data["temporary_processing_cleanup"] is True
    assert data["openml_user_data_transmission"] is False
    assert "privacy_assurance" in data


def test_no_file_persistence_on_prediction():
    raw_files_before = set(os.listdir("data/raw")) if os.path.exists("data/raw") else set()
    
    csv_content = "feature1,feature2,target\n1.0,2.0,0\n3.0,4.0,1\n5.0,6.0,0\n7.0,8.0,1\n9.0,10.0,0\n"
    response = client.post(
        "/api/predict-strategy",
        files={"file": ("private_test_dataset.csv", csv_content.encode("utf-8"), "text/csv")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "recommended_algorithm" in data
    assert "explanation" in data
    
    # Verify no new file was created in data/raw
    raw_files_after = set(os.listdir("data/raw")) if os.path.exists("data/raw") else set()
    new_files = raw_files_after - raw_files_before
    assert len(new_files) == 0, f"Unexpected files persisted on disk: {new_files}"


def test_error_cleanup_on_invalid_csv():
    raw_files_before = set(os.listdir("data/raw")) if os.path.exists("data/raw") else set()
    
    invalid_csv = "corrupted,data\nnot_a_valid_matrix"
    response = client.post(
        "/api/predict-strategy",
        files={"file": ("invalid_dataset.csv", invalid_csv.encode("utf-8"), "text/csv")}
    )
    
    
    assert response.status_code in [400, 500]
    
   
    raw_files_after = set(os.listdir("data/raw")) if os.path.exists("data/raw") else set()
    new_files = raw_files_after - raw_files_before
    assert len(new_files) == 0, f"Unexpected files left behind on error: {new_files}"
