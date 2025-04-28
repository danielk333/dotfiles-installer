import os
import logging
import configparser
from pathlib import Path

logger = logging.getLogger(__file__)


def link_wallpapers(args, paths):
    host_path = paths.configs / f"{args.hostname}.cfg"
    cfg = configparser.ConfigParser()
    cfg.read(host_path)

    target_path = Path(cfg.get("targets", "wallpapers"))
    target_path = target_path.expanduser().absolute()
    target_path.symlink_to(paths.wallpapers)


def link_tool(cfg, paths, lang, name):
    repo_path = (paths.tools / lang / name).expanduser().absolute()
    assert repo_path.exists(), f"The files do not exists in dotfiles repo\n{repo_path}"

    target_path = Path(cfg.get("targets", "tools"))
    target_path = (target_path / name).expanduser().absolute()
    if target_path.exists():
        if target_path.is_symlink():
            logger.warning(f"Target path is already symlink, skipping\n{target_path}")
        else:
            logger.warning(f"Target path exists, skipping\n{target_path}")
    else:
        logger.info(f"linking {target_path} -> {repo_path}")
        target_path.symlink_to(repo_path)


def link_dotfile(cfg, paths, target, name, clobber=False):
    src_host = cfg.get("dotfiles", f"{target}/{name}")
    repo_path = (paths.dotfiles / src_host / target / name).expanduser().absolute()
    assert repo_path.exists(), f"The files do not exists in dotfiles repo\n{repo_path}"

    target_path = Path(cfg.get("targets", f"dotfiles/{target}"))
    target_path = (target_path / name).expanduser().absolute()
    if target_path.exists():
        if clobber:
            logger.info(f"Target path {target_path} exists, deleting...")
            target_path.unlink()
        else:
            raise FileExistsError(f"Target path for symlink already exists\n{target_path}")

    logger.info(f"linking {target_path} -> {repo_path}")
    target_path.symlink_to(repo_path)


def install_tool(args, paths):
    host_path = paths.configs / f"{args.hostname}.cfg"
    host_config = configparser.ConfigParser()
    host_config.read(host_path)

    target_path = Path(host_config.get("targets", "tools")).expanduser().absolute()
    if not target_path.is_dir():
        logger.info(f"target path does not exist, creating... {target_path}")
        target_path.mkdir(parents=True)

    tools = host_config.get("tools", args.lang, fallback="")
    tools = [x.strip() for x in tools.split(",") if len(x.strip()) > 0]
    if args.name not in tools:
        tools.append(args.name)
        host_config["tools"][args.lang] = ",".join(tools)
    with open(host_path, "w") as fh:
        host_config.write(fh)

    link_tool(host_config, paths, args.lang, args.name)


def install_tools(args, paths):
    host_path = paths.configs / f"{args.hostname}.cfg"
    host_config = configparser.ConfigParser()
    host_config.read(host_path)

    target_path = Path(host_config.get("targets", "tools")).expanduser().absolute()
    if not target_path.is_dir():
        logger.info(f"target path does not exist, creating... {target_path}")
        target_path.mkdir(parents=True)

    avalible_langs = [x.name for x in paths.tools.iterdir() if x.is_dir()]
    for lang in avalible_langs:
        avalible_tools = [x.name for x in (paths.tools / lang).iterdir() if x.is_file()]

        tools = host_config.get("tools", lang, fallback="")
        tools = [x.strip() for x in tools.split(",") if len(x.strip()) > 0]
        for tool in tools:
            if tool in avalible_tools:
                logger.info(f"installing {tool}")
                link_tool(host_config, paths, lang, tool)


def install_dotfile(args, paths):
    host_path = paths.configs / f"{args.hostname}.cfg"
    host_config = configparser.ConfigParser()
    host_config.read(host_path)

    host_config["dotfiles"][f"{args.target}/{args.name}"] = args.source_host
    try:
        link_dotfile(host_config, paths, args.target, args.name, clobber=args.clobber)
    except PermissionError:
        logging.error("PermissionError: cannot install dotfile, skipping")
        return

    with open(host_path, "w") as fh:
        host_config.write(fh)
    logging.info(f"Appending dotfile to {host_path} config")


def install(args, paths):
    host_path = paths.configs / f"{args.hostname}.cfg"
    host_config = configparser.ConfigParser()
    host_config.read(host_path)

    for key, source_host in host_config.items("dotfiles"):
        target, name = key.split("/", maxsplit=1)

        target_path = Path(host_config.get("targets", f"dotfiles/{target}"))
        link_path = (target_path / name).expanduser().absolute()
        if link_path.is_symlink():
            logger.info(f"symlink detected, skipping {link_path}")
            continue

        link_dotfile(host_config, paths, target, name)

    for lang, tools in host_config.items("tools"):
        tools = [x.strip() for x in tools.split(",")]
        target_path = Path(host_config.get("targets", "tools"))
        for tool in tools:
            link_path = (target_path / tool).expanduser().absolute()
            if link_path.is_symlink():
                logger.info(f"symlink detected, skipping {link_path}")
                continue

            link_tool(host_config, paths, lang, tool)
