import logging
import configparser

from .settings import HOST_DEFAULT

logger = logging.getLogger(__name__)


def init(args, paths):
    if paths.lockfile.is_file():
        raise FileExistsError(f"dotfiles already initialized '{paths.lockfile}'")
    paths.lockfile.touch()

    logger.info("Initializing dotfiles repo")
    for target in paths.init_dirs:
        logger.info(f"creating {target}")
        target.mkdir(exist_ok=True)
    (paths.default_host / ".gitkeep").touch()

def new_host(args, paths):
    host_config = configparser.ConfigParser()
    host_config.read_dict(HOST_DEFAULT)
    host_path = paths.configs / f"{args.hostname}.cfg"

    logger.info(f"Creating new host config {host_path}")
    if host_path.is_file():
        raise FileExistsError(f"host repo already exists '{host_path}'")
    with open(host_path, "w") as fh:
        host_config.write(fh)

    host_repo = paths.dotfiles / args.hostname
    logger.info(f"Creating host specific dotfiles path {host_repo}")
    host_repo.mkdir(exist_ok=True)
    (host_repo / ".gitkeep").touch()
