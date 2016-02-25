# standard python imports
import unittest.mock as mock

# 3rd party imports
import click
import pytest

# two1 imports
# naming module doc so theres not a conflict with the fixture name
from two1.lib import server
from two1.lib import bitrequests
from two1.commands import doctor as doc
from two1.tests import mock as mock_objects
from two1.lib.server import machine_auth_wallet


@pytest.fixture()
def config():
    return mock.Mock()


@pytest.fixture()
def doctor(config):
    return doc.Doctor(config)


@pytest.fixture()
def mock_config():
    config = mock_objects.MockConfig()
    config.log = mock.Mock()
    return config


@pytest.fixture()
def mock_wallet():
    return mock_objects.MockTwo1Wallet()


@pytest.fixture()
def mock_rest_client(mock_config, mock_wallet):
    machine_auth = machine_auth_wallet.MachineAuthWallet(mock_wallet)
    mock_rest_client = mock_objects.MockTwentyOneRestClient(None, machine_auth, mock_config.username)
    return mock_rest_client


@pytest.yield_fixture()
def patch_click():
    with mock.patch('click.echo') as patch_click:
        yield patch_click


@pytest.fixture()
def patch_bitrequests(monkeypatch, mock_config, mock_wallet):
    patch_bitrequests = mock_objects.MockBitRequests(machine_auth_wallet.MachineAuthWallet(mock_wallet), mock_config.username)
    monkeypatch.setattr(bitrequests.BitTransferRequests, 'request', patch_bitrequests.request)
    monkeypatch.setattr(bitrequests.BitTransferRequests, 'get_402_info', patch_bitrequests.get_402_info)
    return patch_bitrequests


@pytest.fixture()
def patch_rest_client(monkeypatch, mock_config, mock_wallet):
    machine_auth = machine_auth_wallet.MachineAuthWallet(mock_wallet)
    patch_rest_client = mock_objects.MockTwentyOneRestClient(None, machine_auth, mock_config.username)
    monkeypatch.setattr(server.rest_client.TwentyOneRestClient, 'get_earnings', patch_rest_client.get_earnings)
    return patch_rest_client
