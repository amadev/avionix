import logging
from pathlib import Path

import pytest

from avionix import ChartInfo, ObjectMeta
from avionix.kubernetes_objects.pod import Pod, PodSpec
from avionix.tests.utils import get_test_container, get_test_deployment
import pandas

logging.basicConfig(format="[%(filename)s: %(lineno)s] %(message)s", level=logging.INFO)

pandas.set_option("display.max_columns", 50)


@pytest.fixture
def test_deployment1():
    return get_test_deployment(1)


@pytest.fixture
def test_deployment2():
    return get_test_deployment(2)


@pytest.fixture
def chart_info():
    return ChartInfo(
        api_version="3.2.4", name="test", version="0.1.0", app_version="v1"
    )


@pytest.fixture(scope="module")
def test_folder():
    return Path(__file__).parent


@pytest.fixture
def pod():
    return Pod(ObjectMeta(name="test-pod"), spec=PodSpec([get_test_container(0)]))
