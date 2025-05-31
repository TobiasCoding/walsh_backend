# app/tests/test_files_api.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_and_download_file(tmp_path, monkeypatch):
    monkeypatch.setenv("FILE_BASE_PATH", str(tmp_path))

    content = b"contenido de prueba"
    response = client.post(
        "/files",
        files={"file": ("archivo.txt", content)},
        headers={"x-user-id": "test_user"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "key" in data
    key = data["key"]

    # Obtener archivo
    get_response = client.get(f"/files/{key}")
    assert get_response.status_code == 200
    assert get_response.content == content
