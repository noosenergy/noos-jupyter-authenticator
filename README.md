[![CircleCI](https://circleci.com/gh/noosenergy/neptune-jupyter-auth.svg?style=svg&circle-token=f44ebd5b7c018ad366db0b750369693974874d82)](https://circleci.com/gh/noosenergy/neptune-jupyter-auth)

# Neptune Jupyter Auth

Custom JupyterHub `Authenticator` subclass, to enable authentication of [Jupyter hub](https://github.com/noosenergy/neptune-jupyter-hub) via the [auth gateway](https://github.com/noosenergy/neptune-gateway) service.


## Quickstart

Similarly to the rest of the Neptune stack, the application must be deployed onto a machine running:

    - Python 3.8.6
    - a C compiler (either `gcc` via Homebrew, or `xcode` via the App store)


### Local installation

Ensure [Pyenv](https://github.com/pyenv/pyenv) and [Pipenv](https://docs.pipenv.org/) are installed:

    $ brew install pyenv
    $ brew install pipenv

Lock the Python dependencies to build a virtualenv:

    $ pipenv lock

Build and enter your virtualenv:

    $ pipenv sync --dev
    $ pipenv shell

### Local development

The development workflows of this project can be managed by [noos-invoke](https://github.com/noosenergy/noos-invoke), a ready-made CLI for common CI/CD tasks.

```
$ noosinv
Usage: noosinv [--core-opts] <subcommand> [--subcommand-opts] ...
```
