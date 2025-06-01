# app/tests/test_files_api.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.common.config_store import settings

client = TestClient(app)


def test_upload_and_download_file(tmp_path, monkeypatch):
    monkeypatch.setenv("FILE_BASE_PATH", str(tmp_path))
    content = b"contenido de prueba"
    settings.FILE_BASE_PATH = str(tmp_path)
    settings.KAFKA_TOPIC = "test-topic"
    settings.MAX_UPLOAD_MB = 10  # o cualquier valor razonable

    response = client.post(
        "/save",
        files={"file": ("archivo.txt", content)},
        headers={"x-user-id": "test_user"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "key" in data
    key = data["key"]

    # Obtener archivo
    get_response = client.get(f"/save/{key}")
    assert get_response.status_code == 200
    assert get_response.content == content
