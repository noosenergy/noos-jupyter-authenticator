from http import client as http_client

from noos_pyk.clients import auth, json


class NoosGatewayAuth(auth.HTTPTokenAuth):
    """Authentication class for the Noos gateway REST API."""

    default_header = "Authorization"
    default_value = "Bearer"


class NoosGatewayClient(json.JSONClient, auth.AuthClient):
    """Client for the Noos gateway REST API."""

    default_auth_class = NoosGatewayAuth

    def whoami(self) -> json.Json:
        """Return infos about the authenticated user."""
        return self.get(path="internal/v1/accounts/whoami/", statuses=(http_client.OK,))
