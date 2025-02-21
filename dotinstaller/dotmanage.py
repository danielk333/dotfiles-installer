from pathlib import Path
import socket
import configparser
import shutil
import logging

logger = logging.getLogger(__name__)


def append_dotfile_config(config, paths, source_host, target):
    hostname = socket.gethostname()
    logger.info(f"adding {target.name} to {hostname} config from {source_host} dotfiles")
    host_path = paths.configs / f"{hostname}.cfg"
    host_config = configparser.ConfigParser()
    host_config.read(host_path)
    host_config["dotfiles"][target.name] = source_host
    with open(host_path, "w") as fh:
        host_config.write(fh)


def add_dotfile(args, config, paths):
    target = Path(args.path).resolve().absolute()
    repo_path = (paths.dotfiles / args.hostname / target.name).resolve().absolute()
    if repo_path.exists():
        raise FileExistsError(
            "Path already exists for host this repo\n"
            "Maybe choose another host or merge the configs"
        )
    if not repo_path.parent.exists():
        raise FileNotFoundError("Host folder does not exist, add it first")

    if args.install:
        old_path = Path(str(target))
        target.rename(repo_path)
        old_path.symlink_to(repo_path)
        logging.info(f"moved {old_path} -> {repo_path}")
        logging.info(f"linked {old_path} -> {repo_path}")
        append_dotfile_config(config, paths, args.hostname, target)
    else:
        shutil.copytree(target, repo_path)
        logging.info(f"copied {target} -> {repo_path}")
