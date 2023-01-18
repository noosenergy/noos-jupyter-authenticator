import pytest
from tornado import web

from noos_jupyter_authenticator import authenticators


class TestNoosAuthenticator:
    def test_register_handlers(self, mocker):
        auth = authenticators.NoosAuthenticator()

        handlers = auth.get_handlers(mocker.Mock())

        assert len(handlers) == 1
        assert handlers[0][0] == auth.login_url("/")

    @pytest.mark.asyncio
    async def test_authenticate_not_implemented(self, mocked_handler):
        handler = mocked_handler()
        auth = authenticators.NoosAuthenticator()

        with pytest.raises(NotImplementedError):
            await auth.get_authenticated_user(handler, None)


class TestNoosBasicAuthenticator:
    @pytest.mark.asyncio
    async def test_missing_authorization_header(self, mocked_handler):
        handler = mocked_handler()
        auth = authenticators.NoosBasicAuthenticator(auth_header_name="test-header")

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated is None

    @pytest.mark.asyncio
    async def test_authenticate_user(self, mocked_handler):
        handler = mocked_handler({"test-header": "test.user"})
        auth = authenticators.NoosBasicAuthenticator(auth_header_name="test-header")

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated == {"name": "test.user", "admin": None, "auth_state": None}

    @pytest.mark.asyncio
    async def test_authenticate_admin_user(self, mocked_handler):
        handler = mocked_handler({"test-header": "admin.user"})
        auth = authenticators.NoosBasicAuthenticator(auth_header_name="test-header")
        auth.admin_users = {"admin.user"}

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated == {"name": "admin.user", "admin": True, "auth_state": None}


class TestNoosJWTAuthenticator:
    @pytest.mark.asyncio
    async def test_missing_authorization_header(self, mocked_handler):
        handler = mocked_handler()
        auth = authenticators.NoosJWTAuthenticator(auth_header_name="test-header")

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
        auth = authenticators.NoosJWTAuthenticator(
            auth_header_name=header, auth_header_type="bearer"
        )

        with pytest.raises(web.HTTPError):
            await auth.get_authenticated_user(handler, None)

    @pytest.mark.asyncio
    async def test_fail_to_decode_token(self, mocked_client, mocked_handler):
        mocked_client(raise_error=True)
        handler = mocked_handler({"test-header": "bearer myToken"})
        auth = authenticators.NoosJWTAuthenticator(
            auth_header_name="test-header", auth_header_type="bearer"
        )

        with pytest.raises(web.HTTPError):
            await auth.get_authenticated_user(handler, None)

    @pytest.mark.asyncio
    async def test_authenticate_user(self, mocked_client, mocked_handler):
        mocked_client(payload={"email": "test.user", "is_superuser": False})
        handler = mocked_handler({"X-Forwarded-Auth": "Bearer myToken"})
        auth = authenticators.NoosJWTAuthenticator()

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated == {"name": "test.user", "admin": False, "auth_state": None}

    @pytest.mark.asyncio
    async def test_authenticate_admin_user(self, mocked_client, mocked_handler):
        mocked_client(payload={"email": "admin.user", "is_superuser": True})
        handler = mocked_handler({"X-Forwarded-Auth": "Bearer myToken"})
        auth = authenticators.NoosJWTAuthenticator()

        authenticated = await auth.get_authenticated_user(handler, None)

        assert authenticated == {"name": "admin.user", "admin": True, "auth_state": None}
