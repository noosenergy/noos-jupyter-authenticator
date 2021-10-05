from typing import Any, Callable, Dict, Optional
from unittest import mock

import jwt
import pytest


Header = Dict[str, str]
ClaimSet = Dict[str, Any]


@pytest.fixture
def mocked_handler(mocker) -> Callable[[Optional[Header]], mock.Mock]:
    def handler_factory(headers: Optional[Header] = None) -> mock.Mock:
        mocked_request = mocker.Mock()
        mocked_request.headers = headers or {}
        mocked_handler = mocker.Mock()
        mocked_handler.request = mocked_request
        return mocked_handler

    return handler_factory


@pytest.fixture
def mocked_jwt() -> Callable[[str, ClaimSet], str]:
    def jwt_factory(secret_key: str, claim_set: ClaimSet) -> str:
        return jwt.encode(claim_set, secret_key, algorithm="HS256")

    return jwt_factory
