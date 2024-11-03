"""This module have utils functions"""
import os
from pathlib import Path


def my_utils_function():
    my_env_var = os.environ.get("MY_ENV_VAR")

    return f"test.{my_env_var}"


def get_root_path():
    return Path(__file__).parent.parent.resolve()
