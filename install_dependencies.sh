#!/usr/bin/env bash

# Check for root.
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root as it will install packages."
  exit
fi

# Find package managers.
YUM_CMD=$(which yum 2>/dev/null)
APT_GET_CMD=$(which apt-get 2>/dev/null)

# FUNCTION DECLARATION

# Installer Function for apt package maanger.
function apt_install_dependency() {
  echo "Checkig for dependency: $1"
  PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $1 | grep "install ok installed")
  if [ "" == "$PKG_OK" ]; then
    echo "Package $1 does not exist on the system - it will be installed."
    sudo apt install $1 -y &>/dev/null
  else
    echo "Package $1 has been found."
  fi
}

# Installer function for yum/dnf package manager.
function yum_install_dependency() {
  echo "Checkig for dependency: $1"
  if ! rpm -qa | grep -qw $1; then
    echo "Package $1 does not exist on the system - it will be installed."
    yum install $1 -y &>/dev/null
  else
    echo "FOUND: $1"
  fi
}

# Start insalling required packages.

# Fedora/Cent/RHEL
if [[ ! -z $YUM_CMD ]]; then
  yum_install_dependency git
  yum_install_dependency python3
  yum_install_dependency python3-devel
  yum_install_dependency python3-pip
  yum_install_dependency python3-dateutil
  yum_install_dependency libopenjp2-7-devel
  yum_install_dependency libtiff-devel

# Debian/Ubuntu (Desktop and Server Distros).
elif [[ ! -z $APT_GET_CMD ]]; then
  echo "Please wait: updating package manager repositories..."
  apt-get update &>/dev/null
  apt_install_dependency git
  apt_install_dependency python3
  apt_install_dependency python3-dev
  apt_install_dependency python3-pip
  apt_install_dependency python3-dateutil
  apt_install_dependency libopenjp2-7
  apt_install_dependency libtiff-dev
else
  echo "Unable to find a suitable package manager."
  exit
fi


# function to install repositories.
function git_clone_and_install_by_pip() {
  git clone https://github.com/$1/$2.git
  cd $2
  pip3 install .
  cd ..
  rm -rf ./$2/
}

git_clone_and_install_by_pip Jamonek Robinhood
git_clone_and_install_by_pip rm-hull luma.led_matrix
