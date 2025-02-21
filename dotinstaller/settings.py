import configparser
from pathlib import Path

DEFAULT_CONFIG = {
    "folders": {
        "configs": "configs",
        "dotfiles": "dotfiles",
        "tools": "tools",
    },
    "targets": {
        "tools": "~/.local/bin",
    },
    "defaults": {
        "host": "default",
    },
}

HOST_DEFAULT = {
    "dotfiles": {},
    "tools": {},
    "packages": {
        "pacman": "",
        "apt": "",
    },
}


class PathStore:
    def __init__(self, config, base_dir):
        self.base_dir = base_dir
        self.installer_config = base_dir / ".dotinstaller"
        self.dotfiles = base_dir / config.get("folders", "dotfiles")
        self.default_dotfiles = self.dotfiles / "default"
        self.tools = base_dir / config.get("folders", "tools")
        self.configs = base_dir / config.get("folders", "configs")

        self.init_dirs = [
            self.dotfiles,
            self.default_dotfiles,
            self.tools,
            self.configs,
        ]


def get_config(path):
    path = Path(path)
    cfg = path / ".dotinstaller"
    config = configparser.ConfigParser()
    config.read_dict(DEFAULT_CONFIG)
    if cfg.is_file():
        config.read(cfg)
    return config


def dump_config(path):
    path = Path(path)
    cfg = path / ".dotinstaller"
    config = configparser.ConfigParser()
    config.read_dict(DEFAULT_CONFIG)
    with open(cfg, "w") as fh:
        config.write(fh)

