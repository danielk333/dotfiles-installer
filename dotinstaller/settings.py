import configparser
from pathlib import Path

HOST_DEFAULT = {
    "dotfiles": {},
    "tools": {},
    "packages": {
        "pacman": "",
    },
    "targets": {
        "tools": "~/.local/bin/",
        "dotfiles/ssh": "~/.ssh/",
        "dotfiles/config": "~/.config/",
    },
}

# The folder structure idea is:
# dotfiles / {host} / {target} / "dotfile"
# configs / "host config"
# tools / "tool"
#
# That way there can be the same dotfile for multiple hosts and 
# with different targets like ssh folder
class PathStore:
    def __init__(self, base_dir):
        self.base_dir = base_dir

        self.dotfiles = base_dir / "dotfiles"
        self.default_host = self.dotfiles / "default"

        self.tools = base_dir / "tools"
        self.configs = base_dir / "configs"
        self.lockfile = base_dir / ".dotinstaller"

        self.init_dirs = [
            self.dotfiles,
            self.default_host,
            self.tools,
            self.configs,
        ]


