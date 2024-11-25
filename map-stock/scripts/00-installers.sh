#!/bin/bash

highlighted_green_text(){
    echo -e "\e[1;32m$1\e[0m"
}

SCRIPT=$(readlink -f $0);
CURRENT_DIR=`dirname $SCRIPT`;

highlighted_green_text "Instalador de herramientas de trabajo iniciando en $CURRENT_DIR"
highlighted_green_text "Descargando e instalando paquetes necesarios..."
sudo apt update -y && sudo apt install -y git gitk wget tar virtualenv sqlitebrowser python3
highlighted_green_text "Descargando Visual Studio Code e instalandolo..." 
wget -O "code_amd64.deb" "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
sudo apt install -y ./code_amd64.deb
rm code_amd64.deb
highlighted_green_text "Creando directorio donde instalar Python..."
mkdir $HOME/python 
cd $HOME/python
highlighted_green_text "Descargando Page e instalándolo..." 
wget -O "page.tgz" "https://sourceforge.net/projects/page/files/page/7.6/page-7.6.tgz/download"
tar -xvzf page.tgz
rm page.tgz
chmod +x $CURRENT_DIR/page_launcher
sudo cp $CURRENT_DIR/page_launcher /usr/bin/
highlighted_green_text "Dato: ahora se puede ejecutar PAGE desde cualquier lugar ejecutando 'page_launcher'" 
highlighted_green_text "Descargando Python y descomprimiendo..."
wget "https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tar.xz"
tar -Jxvf Python-3.10.4.tar.xz
rm Python-3.10.4.tar.xz
highlighted_green_text "Paquetes necesarios en el SO antes de compilar e instalar Python..."
sudo apt install -y build-essential libffi-dev ncurses-dev python3-tk zlib1g-dev libssl-dev python3-virtualenv libsqlite3-dev peewee
cd Python-3.10.4 && ./configure --enable-optimizations && make && sudo make install
highlighted_green_text "Creación de entorno virtual..."
virtualenv -p  $HOME/python/Python-3.10.4/python  $HOME/python/vir_python/py39_map-stock_env
highlighted_green_text "Activa el entorno virtual e instala los paquetes de Python necesarios..."
source  $HOME/python/vir_python/py39_map-stock_env/bin/activate
python3 -m pip install --upgrade pip
pip install -U setuptools
highlighted_green_text "Paquetes necesarios para desarrollo..."
pip3 install -r $CURRENT_DIR/../requirements_dev.txt
highlighted_green_text "Paquetes necesarios para producción..."
pip3 install -r $CURRENT_DIR/../requirements.txt
highlighted_green_text "Instalador de herramientas de trabajo finalizado"



