import logging
import pathlib
import urwid


def exit_on_q(key: str | tuple[str, int, int, int]) -> None:
    if key in {"q", "Q"}:
        raise urwid.ExitMainLoop()


class SelectableText(urwid.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected = False

    def selectable(self):
        return True

    def keypress(self, size, key):
        if key in [" "]:
            if self.selected:
                self.set_text(self.text.replace("[x]", "[ ]"))
                self.selected = False
            else:
                self.set_text(self.text.replace("[ ]", "[x]"))
                self.selected = True
        return key


class DotfilesApp:
    def __init__(self, config, base_dir):
        self.config = config
        self.base_dir = base_dir

        self.palette = [
            ("body", "light blue", "black", "standout"),
            ("foot", "light gray", "black"),
            ("key", "light cyan", "black", "underline"),
            ("title", "white", "black"),
            ("reveal focus", "black", "dark cyan", "standout"),
        ]

        configs = list((self.base_dir / "config").iterdir())
        self.listwalker = urwid.SimpleListWalker([
            urwid.AttrMap(SelectableText("[ ] " + pth.name), "",  "reveal focus")
            for pth in configs
        ])
        self.listbox = urwid.AttrMap(urwid.ListBox(self.listwalker), "body")

        self.build_head_foot()
        self.view = urwid.Frame(self.listbox, header=self.header, footer=self.footer)
        self.loop = urwid.MainLoop(self.view, self.palette, unhandled_input=exit_on_q)

    def build_head_foot(self):
        header_text = "Dotfiles manager"
        footer_text = [
            ("title", "Dotfiles manager"),
            "    ",
            ("key", "UP"),
            ", ",
            ("key", "DOWN"),
            " moves, ",
            ("key", "SPACE"),
            " selects, ",
            ("key", "Q"),
            " exits",
        ]
        self.header = urwid.AttrMap(urwid.Text(header_text), "head")
        self.footer = urwid.AttrMap(urwid.Text(footer_text), "foot")

    def run(self):
        self.loop.run()


def run_app(args, config, base_dir):
    app = DotfilesApp(config, base_dir)
    app.run()

if __name__ == "__main__":
    run_app(None, None, None)