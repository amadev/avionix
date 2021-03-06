import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.admissionregistration import (
    MutatingWebhook,
    MutatingWebhookConfiguration,
    ValidatingWebhook,
    ValidatingWebhookConfiguration,
    WebhookClientConfig,
)
from avionix.kube.apiregistration import ServiceReference
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


@pytest.fixture
def webhook_params():
    return [
        "this.test.com",
        ["v1"],
        WebhookClientConfig("test", ServiceReference("test", "test")),
        "None",
    ]


@pytest.fixture
def mutating_webhook_config(webhook_params):
    return MutatingWebhookConfiguration(
        ObjectMeta(name="test-mutating-webhook"), [MutatingWebhook(*webhook_params,)],
    )


@pytest.fixture
def validating_webhook_config(webhook_params):
    return ValidatingWebhookConfiguration(
        ObjectMeta(name="test-validating-webhook"),
        [ValidatingWebhook(*webhook_params)],
    )


def test_mutating_webhook_config(chart_info, mutating_webhook_config):
    builder = ChartBuilder(chart_info, [mutating_webhook_config])
    with ChartInstallationContext(builder):
        hook_info = kubectl_get("mutatingwebhookconfigurations")
        assert hook_info["NAME"][0] == "test-mutating-webhook"
        assert hook_info["WEBHOOKS"][0] == "1"


def test_validating_webhook_config(chart_info, validating_webhook_config):
    builder = ChartBuilder(chart_info, [validating_webhook_config])
    with ChartInstallationContext(builder):
        hook_info = kubectl_get("validatingwebhookconfigurations")
        assert hook_info["NAME"][0] == "test-validating-webhook"
        assert hook_info["WEBHOOKS"][0] == "1"
