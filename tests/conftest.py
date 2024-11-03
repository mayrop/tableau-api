"""This module configure the pytests"""
import pytest
import time
import uuid


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("PROJECT_ENV", "testing")
    monkeypatch.setenv("MY_ENV_VAR", "my_env_var_value")


@pytest.fixture()
def change_to_production(monkeypatch):
    monkeypatch.setenv("PROJECT_ENV", "production")


@pytest.fixture(autouse=False)
def fixed_ids(monkeypatch, mocker):
    uuid4 = mocker.MagicMock(return_value="id_test")

    monkeypatch.setattr(uuid, "uuid4", uuid4)


@pytest.fixture(autouse=False)
def fixed_time(monkeypatch, mocker):
    timing = mocker.MagicMock(return_value=1)

    monkeypatch.setattr(time, "time", timing)
    monkeypatch.setattr(time, "strftime", timing)
