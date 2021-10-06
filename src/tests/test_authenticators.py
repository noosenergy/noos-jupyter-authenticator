import pytest
from tornado import web

from jupyterauth_neptune import authenticators


class TestNeptuneAuthenticator:
    def test_register_handlers(self, mocker):
        auth = authenticators.NeptuneAuthenticator()

        handlers = auth.get_handlers(mocker.Mock())

        assert len(handlers) == 1
        assert handlers[0][0] == auth.login_url("/")

    @pytest.mark.asyncio
    async def test_authenticate_not_implemented(self, mocked_handler):
        handler = mocked_handler()
        auth = authenticators.NeptuneAuthenticator()

        with pytest.raises(NotImplementedError):
            await auth.get_authenticated_user(handler, None)


class TestNeptuneBasicAuthenticator:
    @pytest.mark.asyncio
    async def test_missing_authorization_header(self, mocked_handler):
        handler = mocked_handler()
        auth = authenticators.NeptuneBasicAuthenticator(auth_header_name="test-header")

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated is None

    @pytest.mark.asyncio
    async def test_authenticate_user(self, mocked_handler):
        handler = mocked_handler({"test-header": "test.user"})
        auth = authenticators.NeptuneBasicAuthenticator(auth_header_name="test-header")

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated == {"name": "test.user", "admin": None, "auth_state": None}

    @pytest.mark.asyncio
    async def test_authenticate_admin_user(self, mocked_handler):
        handler = mocked_handler({"test-header": "admin.user"})
        auth = authenticators.NeptuneBasicAuthenticator(auth_header_name="test-header")
        auth.admin_users = {"admin.user"}

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated == {"name": "admin.user", "admin": True, "auth_state": None}


class TestNeptuneJWTAuthenticator:
    @pytest.mark.asyncio
    async def test_missing_authorization_header(self, mocked_handler):
        handler = mocked_handler()
        auth = authenticators.NeptuneJWTAuthenticator(auth_header_name="test-header")

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated is None

    @pytest.mark.parametrize(
        "header,scheme",
        [
            ("test-header", "123"),
            ("test-header", "token 123"),
        ],
    )
    @pytest.mark.asyncio
    async def test_invalid_authorization_header_type(self, header, scheme, mocked_handler):
        handler = mocked_handler({header: scheme})
        auth = authenticators.NeptuneJWTAuthenticator(
            auth_header_name=header, auth_header_type="bearer"
        )

        with pytest.raises(web.HTTPError):
            await auth.get_authenticated_user(handler, None)

    @pytest.mark.asyncio
    async def test_fail_to_decode_token(self, mocked_jwt, mocked_handler):
        token = mocked_jwt("secret_key_1", {"test-claim": "test_value"})
        handler = mocked_handler({"test-header": f"bearer {token}"})
        auth = authenticators.NeptuneJWTAuthenticator(
            auth_header_name="test-header", auth_header_type="bearer", secret_key="secret_key_2"
        )

        with pytest.raises(web.HTTPError):
            await auth.get_authenticated_user(handler, None)

    @pytest.mark.asyncio
    async def test_authenticate_user(self, mocked_jwt, mocked_handler):
        token = mocked_jwt("secret_key", {"username": "test.user", "is_admin": False})
        handler = mocked_handler({"X-Forwarded-Auth": f"Bearer {token}"})
        auth = authenticators.NeptuneJWTAuthenticator(secret_key="secret_key")

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated == {"name": "test.user", "admin": False, "auth_state": None}

    @pytest.mark.asyncio
    async def test_authenticate_admin_user(self, mocked_jwt, mocked_handler):
        token = mocked_jwt("secret_key", {"username": "admin.user", "is_admin": True})
        handler = mocked_handler({"X-Forwarded-Auth": f"Bearer {token}"})
        auth = authenticators.NeptuneJWTAuthenticator(secret_key="secret_key")

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated == {"name": "admin.user", "admin": True, "auth_state": None}
