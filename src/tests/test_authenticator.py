import pytest

from jupyterauth_neptune import authenticator


@pytest.fixture
def mocked_handler(mocker):
    def handler_factory(headers):
        mocked_request = mocker.Mock()
        mocked_request.headers = headers
        mocked_handler = mocker.Mock()
        mocked_handler.request = mocked_request
        return mocked_handler

    return handler_factory


class TestNeptuneAuthenticator:
    def test_get_handlers(self, mocker):
        auth = authenticator.NeptuneAuthenticator()

        handlers = auth.get_handlers(mocker.Mock())

        assert len(handlers) == 1
        assert handlers[0][0] == auth.login_url("/")

    @pytest.mark.asyncio
    async def test_authenticate_user(self, mocked_handler):
        handler = mocked_handler({"test-header": "test.user"})
        auth = authenticator.NeptuneAuthenticator(auth_header="test-header")

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated == {"name": "test.user", "admin": None, "auth_state": None}

    @pytest.mark.asyncio
    async def test_authenticate_admin_user(self, mocked_handler):
        handler = mocked_handler({"test-header": "admin.user"})
        auth = authenticator.NeptuneAuthenticator(auth_header="test-header")
        auth.admin_users = {"admin.user"}

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated == {"name": "admin.user", "admin": True, "auth_state": None}
