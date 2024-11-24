# MAP Stock

## Introducción
Sistema de stock de equipos electrónicos.

## Python base

### Versión utilizada
3.10.4

### Paquetes necesarios en el SO antes de compilar e instalar Python 
<pre><code>sudo apt install -y build-essential libffi-dev ncurses-dev python3-tk zlib1g-dev libssl-dev python3-virtualenv libsqlite3-dev peewee</code></pre>

### Descomprimir
<pre><code>tar -Jxvf Python-3.10.4.tar.xz</code></pre>

### Instalar
<pre><code>cd Python-3.10.4 && ./configure && make && sudo make install</code></pre>

## Entornos virtuales y configuración final

### Creación de entornos virtuales
<pre><code>virtualenv -p /home/mauro/python/Python-3.10.4/python /home/mauro/python/vir_python/py39_mb-stock_env</code></pre>

### Activar entorno virtual
<pre><code>source /home/mauro/python/vir_python/py39_mb-stock_env/bin/activate</code></pre>

### Actualizar Pip3
<pre><code>python3 -m pip install --upgrade pip</code></pre>

### Actualizar setuptools
<pre><code>pip install -U setuptools</pre></code>

### Paquetes necesarios para desarrollo
<pre><code>pip3 install -r ~/repos/map/mb-stock/mb-stock/requirements_dev.txt</code></pre>

### Paquetes necesarios para producción
<pre><code>pip3 install -r ~/repos/map/mb-stock/mb-stock/requirements.txt</code></pre>

### Desactivar entorno virtual
<pre><code>deactivate</code></pre>

## Versiones
* stock-mb_v0.1
  Permite agregar y borrar Productos por el cliente/servidor. Funciona la parte gráfica.