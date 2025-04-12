#!/bin/bash

highlighted_green_text(){
    echo -e "\e[1;32m$1\e[0m"
}

SCRIPT=$(readlink -f $0)
CURRENT_DIR=$(dirname "$SCRIPT")

highlighted_green_text "Starting setup script in $CURRENT_DIR"

# Install all required system packages in one go.
# NOTE: 'tk-dev' and X11-related libraries are necessary to enable Tkinter
# support when compiling Python from source. Without these, the '_tkinter' module won't be built.
highlighted_green_text "Updating system and installing required packages..."

sudo apt update -y && sudo apt install -y \
    git gitk wget tar virtualenv sqlitebrowser python3-dev build-essential \
    tk-dev libx11-dev libxext-dev libxrender-dev libxcb1-dev libxft-dev \
    libffi-dev ncurses-dev zlib1g-dev libssl-dev libsqlite3-dev

highlighted_green_text "Downloading and installing Visual Studio Code..." 
wget -O "code_amd64.deb" "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
sudo apt install -y ./code_amd64.deb
rm code_amd64.deb

highlighted_green_text "Creating Python installation directory..."
mkdir -p $HOME/python 
cd $HOME/python

highlighted_green_text "Downloading and installing PAGE..." 
wget -O "page.tgz" "https://sourceforge.net/projects/page/files/page/7.6/page-7.6.tgz/download"
tar -xvzf page.tgz
rm page.tgz
chmod +x $CURRENT_DIR/page_launcher
sudo cp $CURRENT_DIR/page_launcher /usr/bin/
highlighted_green_text "You can now run PAGE from anywhere using 'page_launcher'" 

highlighted_green_text "Downloading and extracting Python source..."
wget "https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tar.xz"
tar -Jxvf Python-3.10.4.tar.xz
rm Python-3.10.4.tar.xz

highlighted_green_text "Compiling and installing Python..."
cd Python-3.10.4
./configure --enable-optimizations
make -j$(nproc)
sudo make install

highlighted_green_text "Creating Python virtual environment..."
virtualenv -p $HOME/python/Python-3.10.4/python $HOME/python/vir_python/py39_map-stock_env

highlighted_green_text "Activating virtual environment and installing Python packages..."
source $HOME/python/vir_python/py39_map-stock_env/bin/activate
python3 -m pip install --upgrade pip
pip install -U setuptools

highlighted_green_text "Installing development packages..."
pip install -r $CURRENT_DIR/../requirements_dev.txt

highlighted_green_text "Installing production packages..."
pip install -r $CURRENT_DIR/../requirements.txt

highlighted_green_text "Setup script finished successfully."
