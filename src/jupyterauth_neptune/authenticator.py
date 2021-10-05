from typing import List, Optional, Tuple, TypedDict

import jwt
from jupyterhub import auth, handlers, utils
from tornado import gen, httputil, web
from traitlets import Unicode

from . import handler


__all__ = ["NeptuneBasicAuthenticator", "NeptuneJWTAuthenticator"]


UrlHandler = Tuple[str, handlers.BaseHandler]


class UserInfo(TypedDict):
    name: str
    admin: Optional[bool]


class NeptuneAuthenticator(auth.Authenticator):
    """Auto-login Jupyterhub Authenticator.

    Ref: https://github.com/jupyterhub/jupyterhub/blob/master/jupyterhub/auth.py
    """

    login_handler = handler.NeptuneLoginHandler
    login_service = "Neptune Gateway"

    auth_path = "/auto_login"

    # Register a custom handler and its URL
    def login_url(self, base_url: str) -> str:
        return utils.url_path_join(base_url, self.auth_path)

    def get_handlers(self, *args) -> List[UrlHandler]:
        # Combine a raw-string for regex with a f-string for interpolation
        return [(rf"{self.auth_path}", self.login_handler)]

    # Implement authenticator's main co-routine
    @gen.coroutine
    def authenticate(self, handler: web.RequestHandler, *args) -> Optional[UserInfo]:
        raise NotImplementedError


class NeptuneBasicAuthenticator(NeptuneAuthenticator):
    """Null Jupyterhub Authenticator.

    Ref: https://github.com/jupyterhub/jupyterhub/blob/master/jupyterhub/auth.py
    """

    auth_header_name = Unicode(
        config=True,
        default_value="X-Forwarded-User",
        help="The HTTP header to inspect from the forwarded request.",
    )

    @gen.coroutine
    def authenticate(self, handler: web.RequestHandler, *args) -> Optional[UserInfo]:
        header = handler.request.headers.get(self.auth_header_name)
        if not header:
            return None

        return {
            "name": header,
            "admin": None,
        }


class NeptuneJWTAuthenticator(NeptuneAuthenticator):
    """JWT-based Jupyterhub Authenticator.

    Ref: https://github.com/jupyterhub/jupyterhub/blob/master/jupyterhub/auth.py
    """

    auth_header_name = Unicode(
        config=True,
        default_value="X-Forwarded-Token",
        help="The HTTP header to inspect from the forwarded request.",
    )
    auth_header_type = Unicode(
        config=True,
        default_value="Bearer",
        help="The type of HTTP header to be inspected.",
    )

    secret_key = Unicode(
        config=True,
        help="The shared secret key for signing the JWT tokens.",
    )
    name_claim_field = Unicode(
        config=True,
        default_value="username",
        help="The decoded claim field that contains the user name.",
    )
    admin_claim_field = Unicode(
        config=True,
        default_value="is_admin",
        help="The decoded claim field that defines whether a user is an admin.",
    )

    @gen.coroutine
    def authenticate(self, handler: web.RequestHandler, *args) -> Optional[UserInfo]:
        """Authenticate the request and return a UserInfo dict."""
        header = self._get_header(handler.request)
        if not header:
            return None

        token = self._get_token(header)
        return self._get_userinfo(token)

    # Helpers:
    def _get_header(self, request: httputil.HTTPServerRequest) -> Optional[str]:
        """Extract the header containing the token from the given request."""
        return request.headers.get(self.auth_header_name)

    def _get_token(self, header: str) -> str:
        """Extract a token from the given header value."""
        parts = header.split()

        if len(parts) != 2:
            raise web.HTTPError(401, "Invalid authorization header.")

        if parts[0] != self.auth_header_type:
            raise web.HTTPError(401, "Invalid authorization header type.")

        return parts[1]

    def _get_userinfo(self, token: str) -> UserInfo:
        """Attempt to find and return user infos from the given token."""
        # Only implemented with a symetric key for encoding / decoding
        try:
            claim_set = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except Exception:
            raise web.HTTPError(401, "Invalid decoded JWT.")

        username = claim_set.get(self.name_claim_field)
        if not username:
            raise web.HTTPError(401, "Missing name claim field.")

        return {
            "name": username,
            "admin": claim_set.get(self.admin_claim_field),
        }
