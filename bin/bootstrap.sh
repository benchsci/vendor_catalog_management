#!/usr/bin/env bash
set -eu

# Check if an executable exists.
present() {
  command -v $1 >/dev/null 2>&1;
}

brew_present() {
    brew ls | grep $1 >/dev/null 2>&1;
}

if [[ "$OSTYPE" == "darwin"* ]]; then
  if ! present xcode-select; then
    echo You must have Xcode command line utilities
    echo https://apps.apple.com/us/app/xcode/id497799835
    exit 1
  fi

  if ! present gcc; then
    xcode-select --install
  fi

  if ! present brew; then
    # I'm not thrilled with this step of running something random from the
    # internet but it's convenient for the moment and we do checksum.
    brew_install=$( mktemp )
    curl -fsSL https://raw.githubusercontent.com/Homebrew/install/c744a716f9845988d01e6e238eee7117b8c366c9/install > "${brew_install}"
    echo "b9782cc0b550229de77b429b56ffce04157e60486ab9df00461ccf3dad565b0a  ${brew_install}" | shasum -a 256 -c -
    chmod +x "${brew_install}"
    ${brew_install}
  fi

  pushd $( git rev-parse --show-toplevel )
  PYVERSION=$( cat .python-version )

  if ! present pyenv; then
    brew install pyenv
  fi

  brew update && brew upgrade pyenv

  pyenv install --skip-existing ${PYVERSION}
fi
