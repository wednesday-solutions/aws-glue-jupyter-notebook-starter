#!/bin/bash

# Function to check and install Python and pip
install_python() {
  if ! command -v python3 &> /dev/null; then
    echo "something"
    if [ "$(uname)" == "Darwin" ]; then
      brew install python3
    else
      sudo apt update
      sudo apt install -y python3 python3-pip
    fi
  fi
}

# Function to check and install Jinja2
install_jinja() {
  if ! pip3 show Jinja2 &> /dev/null; then
    pip3 install Jinja2
  fi
}

# Function to check and install yq
install_yq() {
  if ! command -v yq &> /dev/null; then
    if [ "$(uname)" == "Darwin" ]; then
      brew install yq
    else
      wget https://github.com/mikefarah/yq/releases/download/v4.12.2/yq_linux_amd64.tar.gz -O - | tar xz && sudo mv yq_linux_amd64 /usr/bin/yq
    fi
  fi
}

# Detect the Operating System
if [ "$(uname)" == "Darwin" ]; then
  if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  echo "Linux detected"
else
  echo "Unsupported OS"
  exit 1
fi

# Install Python, Jinja2, and yq
install_python
install_jinja
install_yq

echo "Installation complete"
