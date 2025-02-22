import logging
import configparser
from pathlib import Path

logger = logging.getLogger(__file__)


def link_tool(cfg, paths, lang, name):
    repo_path = (paths.tools / lang / name).resolve().absolute()
    assert repo_path.exists(), f"The files do not exists in dotfiles repo\n{repo_path}"

    target_path = Path(cfg.get("targets", "tools"))
    target_path = (target_path / name).expanduser().resolve().absolute()
    assert (
        not target_path.exists()
    ), f"Target path for symlink already exists\n{target_path}"

    logger.info(f"linking {target_path} -> {repo_path}")
    target_path.symlink_to(repo_path)


def link_dotfile(cfg, paths, target, name):
    src_host = cfg.get("dotfiles", f"{target}/{name}")
    repo_path = (paths.dotfiles / src_host / target / name).resolve().absolute()
    assert repo_path.exists(), f"The files do not exists in dotfiles repo\n{repo_path}"

    target_path = Path(cfg.get("targets", f"dotfiles/{target}"))
    target_path = (target_path / name).expanduser().resolve().absolute()
    assert (
        not target_path.exists()
    ), f"Target path for symlink already exists\n{target_path}"

    logger.info(f"linking {target_path} -> {repo_path}")
    target_path.symlink_to(repo_path)


def install_tool(args, paths):
    host_path = paths.configs / f"{args.hostname}.cfg"
    host_config = configparser.ConfigParser()
    host_config.read(host_path)

    target_path = Path(host_config.get("targets", "tools")).expanduser()
    if not target_path.is_dir():
        logger.info(f"target path does not exist, creating... {target_path}")
        target_path.mkdir(parents=True)

    link_tool(host_config, paths, args.lang, args.name)


def install_dotfile(args, paths):
    host_path = paths.configs / f"{args.hostname}.cfg"
    host_config = configparser.ConfigParser()
    host_config.read(host_path)

    link_dotfile(host_config, paths, args.target, args.name)


def install(args, paths):
    host_path = paths.configs / f"{args.hostname}.cfg"
    host_config = configparser.ConfigParser()
    host_config.read(host_path)

    for key, source_host in host_config.items("dotfiles"):
        target, name = key.split("/")
        link_dotfile(host_config, paths, target, name)

    for lang, tools in host_config.items("tools"):
        tools = [x.strip() for x in tools.split(",")]
        for tool in tools:
            link_tool(host_config, paths, lang, tool)
