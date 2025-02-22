import logging
import configparser
from pathlib import Path

logger = logging.getLogger(__file__)


def install_dotfile(args, paths):
    host_path = paths.configs / f"{args.hostname}.cfg"
    host_config = configparser.ConfigParser()
    host_config.read(host_path)
    
    src_host = host_config.get("dotfiles", f"{args.target}/{args.name}")
    repo_path = (paths.dotfiles / src_host / args.target / args.name).resolve().absolute()
    assert repo_path.exists(), "The files do not exists in dotfiles repo"

    target_path = Path(host_config.get("targets", f"dotfiles/{args.target}"))
    target_path = (target_path / args.name).expanduser().resolve().absolute()
    
    logger.info(f"linking {target_path} -> {repo_path}")
    target_path.symlink_to(repo_path)


def install():
    pass
