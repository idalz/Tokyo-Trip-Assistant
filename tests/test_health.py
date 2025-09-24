"""
Basic health check tests for Tokyo Trip Assistant
"""

import pytest
import requests
import time
import subprocess
import signal
import os
from contextlib import contextmanager


@contextmanager
def run_app():
    """Context manager to start and stop the FastAPI app for testing"""
    # Start the app in background
    process = subprocess.Popen([
        "uv", "run", "uvicorn", "app.main:app",
        "--host", "0.0.0.0", "--port", "8000"
    ])

    # Wait for app to start
    time.sleep(5)

    try:
        yield process
    finally:
        # Clean shutdown
        process.send_signal(signal.SIGTERM)
        process.wait(timeout=10)


def test_health_endpoint():
    """Test that the health endpoint returns 200"""
    with run_app():
        response = requests.get("http://localhost:8000/health", timeout=10)
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["service"] == "Tokyo Trip Assistant"


def test_ready_endpoint():
    """Test that the ready endpoint returns 200"""
    with run_app():
        response = requests.get("http://localhost:8000/ready", timeout=10)
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "ready"
        assert "dependencies" in data


def test_root_endpoint():
    """Test that the root endpoint returns service info"""
    with run_app():
        response = requests.get("http://localhost:8000/", timeout=10)
        assert response.status_code == 200

        data = response.json()
        assert data["service"] == "Tokyo Trip Assistant"
        assert data["status"] == "running"


if __name__ == "__main__":
    # Run tests directly
    test_health_endpoint()
    test_ready_endpoint()
    test_root_endpoint()
    print("✅ All health tests passed!")