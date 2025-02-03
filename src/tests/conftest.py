from typing import Any
from unittest import mock

import pytest

from noos_pyk.clients import http, json


Header = dict[str, str]
ClaimSet = dict[str, Any]


@pytest.fixture
def mocked_handler(mocker):
    def _handler_factory(headers: Header | None = None) -> mock.Mock:
        mocked_request = mocker.Mock()
        mocked_request.headers = headers or {}
        mocked_handler = mocker.Mock()
        mocked_handler.request = mocked_request
        return mocked_handler

    return _handler_factory


@pytest.fixture
def mocked_client(mocker):
    def _client_factory(payload: dict[str, Any] | None = None, raise_error: bool = False) -> None:
        mocker.patch.object(json.JSONClient, "_send")
        side_effect = http.HTTPError if raise_error else None
        mocker.patch.object(json.JSONClient, "_check", side_effect=side_effect)
        mocker.patch.object(json.JSONClient, "_deserialize", return_value=payload)
        return

    return _client_factory
