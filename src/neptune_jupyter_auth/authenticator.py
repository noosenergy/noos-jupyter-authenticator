from jupyterhub import auth, handlers, utils
from tornado import gen, web
from traitlets import Unicode


class NeptuneLoginHandler(handlers.BaseHandler):
    """Custom Jupyter hub auto-login handler."""

    async def get(self):
        self.statsd.incr("login.request")

        user = self.current_user
        if user:
            # Set a new login cookie (possibly cleared or incorrect)
            self.set_login_cookie(user)
        else:
            # Auto-login with auth info in the request
            user = await self.login_user()
            if user is None:
                raise web.HTTPError(403)

        self.redirect(self.get_next_url(user))


class NeptuneAuthenticator(auth.Authenticator):
    """Accept the authenticated user from the forwarded header."""

    login_handler = NeptuneLoginHandler

    auth_header = Unicode(
        config=True,
        default_value="X-Forwarded-User",
        help="HTTP header to inspect from the forwarded request.",
    )

    # Register a custom handler and its URL
    def login_url(self, base_url):
        return utils.url_path_join(base_url, "auto_login")

    def get_handlers(self, app):
        return [(r"/auto_login", self.login_handler)]

    # Implement authenticator's main co-routine
    @gen.coroutine
    def authenticate(self, handler, data):
        return handler.request.headers.get(self.auth_header)
