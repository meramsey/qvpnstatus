# QVpnStatus

[![pipeline status](https://gitlab.com/mikeramsey/qvpnstatus/badges/master/pipeline.svg)](https://gitlab.com/mikeramsey/qvpnstatus/pipelines)
[![coverage report](https://gitlab.com/mikeramsey/qvpnstatus/badges/master/coverage.svg)](https://gitlab.com/mikeramsey/qvpnstatus/commits/master)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://mikeramsey.gitlab.io/qvpnstatus/)
[![pypi version](https://img.shields.io/pypi/v/qvpnstatus.svg)](https://pypi.org/project/qvpnstatus/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/qvpnstatus/community)

VPN Status tray icon for monitoring VPN connection

## Requirements

QVpnStatus requires Python 3.6 or above.

<details>
<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.6
pyenv install 3.6.12

# make it available globally
pyenv global system 3.6.12
```
</details>

## Installation

With `pip`:
```bash
python3.6 -m pip install qvpnstatus
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.6 -m pip install --user pipx

pipx install --python python3.6 qvpnstatus
```
