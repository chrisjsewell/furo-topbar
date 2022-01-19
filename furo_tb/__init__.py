"""Adding a topbar to the furo sphinx theme."""
from pathlib import Path

from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset_file

from .topbar import setup_topbar

__version__ = "0.0.1"

THEME_PATH = Path(__file__).parent / "theme"


def setup(app: Sphinx):
    """Setup function for the Sphinx extension."""
    app.setup_extension("furo")
    app.add_html_theme("furo_tb", str(THEME_PATH.resolve()))
    app.connect("builder-inited", _become_furo, priority=10)
    app.add_css_file("ftb.css")
    app.connect("build-finished", _add_global_html_resources)
    setup_topbar(app)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }


def _become_furo(app: Sphinx):
    """Now that the templates are loaded, lets pretend to be furo 😬"""
    if app.config.html_theme == "furo_tb":
        app.config.html_theme = "furo"


def _add_global_html_resources(app: Sphinx, exception):
    """Add HTML resources that apply to all pages."""
    # see https://github.com/sphinx-doc/sphinx/issues/1379
    if app.builder.format == "html" and not exception:
        source_path = str((THEME_PATH / "topbar.css").resolve())
        destination = Path(app.builder.outdir, "_static", "ftb.css")
        copy_asset_file(str(source_path), str(destination))
