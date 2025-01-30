import logging
import configparser

logger = logging.getLogger(__name__)

HOST_DEFAULT = {
    "config": {},
    "tools": {},
    "packages": {
        "pacman": "",
        "apt": "",
    },
}

def init(args, config, base_dir):
    config_file = base_dir / ".dotinstaller"
    if config_file.is_file():
        raise FileExistsError(f"dotfiles repo already initialized '{config_file}'")
    config_file.touch()

    logger.info("Initializing dotfiles repo")
    for folder in config["folders"]:
        target = base_dir / folder
        logger.info(f"creating {target}")
        target.mkdir(exist_ok=True)


def new_host(args, config, base_dir):
    host_config = configparser.ConfigParser()
    host_config.read_dict(HOST_DEFAULT)
    host_path = base_dir / config.get("folders", "configs") / f"{args.hostname}.cfg"
    if host_path.is_file():
        raise FileExistsError(f"host file already exists '{host_path}'")

    with open(host_path, "w") as fh:
        host_config.write(fh)
