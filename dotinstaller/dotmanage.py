from pathlib import Path
import socket
import configparser
import shutil
import logging

logger = logging.getLogger(__name__)


def append_dotfile_config(paths, name, source_host, target):
    hostname = socket.gethostname()
    logger.info(f"adding {target}/{name} to {hostname} config from {source_host} dotfiles")
    host_path = paths.configs / f"{hostname}.cfg"
    host_config = configparser.ConfigParser()
    host_config.read(host_path)
    host_config["dotfiles"][f"{target}/{name}"] = source_host
    with open(host_path, "w") as fh:
        host_config.write(fh)


def add_dotfile(args, paths):
    src_path = Path(args.path).resolve().absolute()
    source_host = socket.gethostname() if args.localhost else "default"
    repo_path = paths.dotfiles / source_host / args.target / src_path.name
    repo_path = repo_path.resolve().absolute()
    if repo_path.exists():
        raise FileExistsError(
            "Path already exists for host this repo\n"
            "Maybe choose another host or merge the configs"
        )
    repo_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Repo store created and verified ready")

    host_path = paths.configs / f"{socket.gethostname()}.cfg"
    if args.install and not host_path.is_file():
        raise FileNotFoundError(
            f"No host config {host_path} exists, cannot install. Create new host config first"
        )

    if args.install:
        old_path = Path(str(src_path))
        src_path.rename(repo_path)
        old_path.symlink_to(repo_path)
        logging.info(f"moved {old_path} -> {repo_path}")
        logging.info(f"linked {old_path} -> {repo_path}")
        append_dotfile_config(paths, repo_path.name, source_host, args.target)
    else:
        if src_path.is_dir():
            shutil.copytree(src_path, repo_path)
        else:
            shutil.copy(src_path, repo_path)
        logging.info(f"copied {src_path} -> {repo_path}")

