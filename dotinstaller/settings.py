import configparser
from pathlib import Path

DEFAULT_CONFIG = {
    "folders": {
        "configs": "configs",
        "host_dotfiles": "hosts",
        "tools": "tools",
    },
    "targets": {
        "tools": "~/.local/bin",
    },
}


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