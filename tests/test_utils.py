"""This module test the bigquery handler"""
import pytest
from tableau_api.utils import get_root_path


@pytest.fixture()
def data_sample():  # pylint: disable=redefined-outer-name
    return {"foo": "bar"}


def test_sample(data_sample):  # pylint: disable=redefined-outer-name
    """Test sample"""
    assert data_sample["foo"] == "bar"
    assert "tableau" in get_root_path().name
