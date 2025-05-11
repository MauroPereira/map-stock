# MAP Stock

## Introduction
Electronic equipment stock system.

## Python base

### Version used
3.12.0

### Required system packages before compiling and installing Python
<pre><code>sudo apt install -y build-essential libffi-dev ncurses-dev python3-tk zlib1g-dev libssl-dev python3-virtualenv libsqlite3-dev peewee</code></pre>

### Extract
<pre><code>tar -Jxvf Python-3.10.4.tar.xz</code></pre>

### Install
<pre><code>cd Python-3.10.4 && ./configure && make && sudo make install</code></pre>

## Virtual environments and final configuration

### Create virtual environments
<pre><code>virtualenv -p /home/mauro/python/Python-3.10.4/python /home/mauro/python/vir_python/py39_map-stock_env</code></pre>

### Activate virtual environment
<pre><code>source /home/mauro/python/vir_python/py39_map-stock_env/bin/activate</code></pre>

### Update Pip3
<pre><code>python3 -m pip install --upgrade pip</code></pre>

### Update setuptools
<pre><code>pip install -U setuptools</pre></code>

### Required development packages
<pre><code>pip3 install -r ~/repos/map/map-stock/map-stock/requirements_dev.txt</code></pre>

### Required production packages
<pre><code>pip3 install -r ~/repos/map/map-stock/map-stock/requirements.txt</code></pre>

### Deactivate virtual environment
<pre><code>deactivate</code></pre>

## Versions
- stock-mb_v0.1: Allows adding and deleting Products by client/server. GUI functionality works.
- 3.11.0: Allows creating boards groups.
- 3.12.0: Added GitHub Projects integration with automatic issue creation and management through git commit messages. This feature allows you to create and move issues in your GitHub Projects board by using specific keywords in your commit messages (#backlog, #ready, #in-progress, #review, #done). 