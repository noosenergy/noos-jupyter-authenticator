[![CircleCI](https://dl.circleci.com/status-badge/img/gh/noosenergy/noos-jupyter-authenticator/tree/master.svg?style=svg&circle-token=34ea00fda6c7b93facecbbd26d3a1d7ef1cda9d3)](https://dl.circleci.com/status-badge/redirect/gh/noosenergy/noos-jupyter-authenticator/tree/master)

# Noos JupyterHub Authenticator

Bespoke JupyterHub `Authenticator`, to enable authentication of [Jupyter hub](https://jupyter.org/hub) via the Noos platform.


## Installation

The python package is available from the [PyPi repository](https://pypi.org/project/noos-jupyter-authenticator),

```sh
pip install noos-jupyter-authenticator
```

## Configuration

Edit your `jupyterhub_config.py` file and add the following to register `noos_jupyter_authenticator` as a JupyterHub Authenticator class:

```python
c.Authenticator.auto_login = True

c.JupyterHub.authenticator_class = "noos-jwt"

c.NoosJWTAuthenticator.auth_server_url = "http://<hostname>"
```

:warning: This Authenticator only works with `jupyterhub >= 3.0.0`.


## Development

### Python package manager

On Mac OSX, make sure [poetry](https://python-poetry.org/) has been installed and pre-configured,

```sh
brew install poetry
```

### Local dev workflows

The development workflows of this project can be managed by [noos-invoke](https://github.com/noosenergy/noos-invoke), a ready-made CLI for common CI/CD tasks.

```
$ noosinv
Usage: noosinv [--core-opts] <subcommand> [--subcommand-opts] ...
```
