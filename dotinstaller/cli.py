import argparse
import socket
from pathlib import Path
import os

from . import settings
from .dotinit import init, new_host
from .dotmanage import add_dotfile
from .dotinstall import install

try:
    from .tui import run_app
except ImportError:

    def run_app(*args):
        raise ImportError("urwid not installed - please install to run TUI")


COMMAND_MAP = {}


def add_command(name, action, **kwargs):
    def cmd_wrapper(func):
        def wrap_func(subparsers):
            parser = subparsers.add_parser(
                name, formatter_class=argparse.ArgumentDefaultsHelpFormatter, **kwargs
            )
            return func(parser)

        COMMAND_MAP[name] = (action, wrap_func)
        return wrap_func

    return cmd_wrapper


@add_command("add", add_dotfile, help="Add dotfiles to the dotfiles repo")
def build_add_dotfile(parser: argparse.ArgumentParser):
    parser.add_argument("path")
    parser.add_argument(
        "--hostname",
        default="default",
        help="Host to add path to",
    )
    parser.add_argument(
        "-i", "--install", action="store_true", help="Remove and install to this host"
    )
    return parser


@add_command("install", install, help="Install according to a config")
def build_install(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--hostname", default=socket.hostname(), help="Host config to install"
    )
    return parser


@add_command("new", new_host, help="Start a new host config")
def build_new_host(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--hostname",
        default=socket.hostname(),
        help="Hostname to start a new config for",
    )
    return parser


@add_command("init", init, help="Init a dotfiles repo")
def build_init(parser: argparse.ArgumentParser):
    return parser


@add_command("tui", run_app, help="Run the TUI")
def build_run_app(parser: argparse.ArgumentParser):
    return parser


def run():
    parser = argparse.ArgumentParser(
        prog="dotinstaller",
        description="Main CLI for the dotfiles installer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--log", default="INFO", choices=["INFO", "DEBUG"], help="logging level"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    for name, (_, builder) in COMMAND_MAP.items():
        builder(subparsers)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return
    action = COMMAND_MAP[args.command][0]

    base_dir = Path(os.getcwd())
    config = settings.get_config(base_dir)
    paths = settings.PathStore(config, base_dir)

    action(args, config, paths)
