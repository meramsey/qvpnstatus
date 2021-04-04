# QVpnStatus

[![pipeline status](https://gitlab.com/mikeramsey/qvpnstatus/badges/master/pipeline.svg)](https://gitlab.com/mikeramsey/qvpnstatus/pipelines)
[![coverage report](https://gitlab.com/mikeramsey/qvpnstatus/badges/master/coverage.svg)](https://gitlab.com/mikeramsey/qvpnstatus/commits/master)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://mikeramsey.gitlab.io/qvpnstatus/)
[![pypi version](https://img.shields.io/pypi/v/qvpnstatus.svg)](https://pypi.org/project/qvpnstatus/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/qvpnstatus/community)

VPN Status tray icon for monitoring VPN connections from nmcli. Allows you to specify interval to check and also toggle off sound notifications.

See link [here](https://wizardassistant.com/qvpn-status-monitor-status-and-restart-vpn-connections-in-linux/) for more information.

It is based on my [copier-poetry-fbs](https://gitlab.com/mikeramsey/copier-poetry-fbs) skeleton which uses PyQT5 for the GUI elements and [fbs](https://github.com/mherrmann/fbs) for the installer creation.


## Requirements

QVpnStatus requires Python 3.7 or above.

<details>
<summary>To install Python 3.7, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.7
pyenv install 3.7.12

# make it available globally
pyenv global system 3.7.12
```
</details>

## Installation

With `pip`:
```bash
python3.7 -m pip install qvpnstatus
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.7 -m pip install --user pipx

pipx install --python python3.6 qvpnstatus
```

## Creating a native installer
-  clone the repo locally   
   `git clone git@gitlab.com:mikeramsey/qvpnstatus.git`
-  Install [poetry](https://python-poetry.org/)   
   `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -`   
-  Setting the below settings are highly recommended for ensuring the virtual environment poetry makes is located inside the project folder.    
   `poetry config virtualenvs.create true; poetry config virtualenvs.in-project true;`
-  Run `poetry install` in the path to install all the dependencies
-  Enter the virtual environment that poetry created. This can be found by running `poetry env info` See also [here](https://python-poetry.org/docs/managing-environments/)
-  Run `fbs freeze` and then `fbs installer` afterwards if the frozen "compiled" app runs without issues. See [here](https://github.com/mherrmann/fbs-tutorial) for more on how fbs works. And also [here](https://www.learnpyqt.com/tutorials/packaging-pyqt5-apps-fbs/)

## Credits
Special thanks to below references and resources.

Resources:
Python nmcli api package which made this a breeze:   
https://github.com/ushiboy/nmcli   
https://pypi.org/project/nmcli/

References:  
https://www.learnpyqt.com/tutorials/system-tray-mac-menu-bar-applications-pyqt/   
https://itectec.com/ubuntu/ubuntu-connect-disconnect-from-vpn-from-the-command-line/   
https://www.devdungeon.com/content/python3-qt5-pyqt5-tutorial#toc-9   