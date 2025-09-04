from typing import Any


def pytest_configure(config: Any) -> None:
    """Configure pytest."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
