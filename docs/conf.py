"""Sphinx configuration."""
from furo_tb import __version__

project = "furo-topbar"
version = release = __version__

extensions = [
    "myst_parser",
]
myst_enable_extensions = ["deflist"]
html_theme = "furo_tb"
html_theme_options = {
    "announcement": "This is in development!",
}
furo_topbar_widgets = {
    "scroll_to_top": True,
    "fullscreen": True,
    "github": {
        "url": "https://github.com/chrisjsewell/furo-topbar",
        "branch": "main",
        "path_to_docs": "docs",
    },
    "download": True,
    "theme_toggle": True,
}
