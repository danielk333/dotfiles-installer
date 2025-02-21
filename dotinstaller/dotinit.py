import logging
import configparser

from .settings import HOST_DEFAULT

logger = logging.getLogger(__name__)


def init(args, config, paths):
    if paths.installer_config.is_file():
        raise FileExistsError(
            f"dotfiles already initialized '{paths.installer_config}'"
        )
    paths.installer_config.touch()

    logger.info("Initializing dotfiles repo")
    for target in paths.init_dirs:
        logger.info(f"creating {target}")
        target.mkdir(exist_ok=True)


def new_host(args, config, paths):
    host_config = configparser.ConfigParser()
    host_config.read_dict(HOST_DEFAULT)
    host_path = paths.configs / f"{args.hostname}.cfg"
    if host_path.is_file():
        raise FileExistsError(f"host repo already exists '{host_path}'")
    with open(host_path, "w") as fh:
        host_config.write(fh)

    host_repo = paths.dotfiles / args.hostname
    host_repo.mkdir(exist_ok=True)
