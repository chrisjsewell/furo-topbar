"""Adding a topbar to the furo sphinx theme."""
from pathlib import Path

from sphinx.application import Sphinx

__version__ = "0.0.1"

THEME_PATH = Path(__file__).parent / "theme"


def setup(app: Sphinx):
    """Setup function for the Sphinx extension."""
    app.setup_extension("furo")
    app.add_html_theme("furo_tb", str(THEME_PATH.resolve()))
    app.connect("builder-inited", _become_furo, priority=10)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }


def _become_furo(app: Sphinx):
    """Now that the templates are loaded, lets pretend to be furo 😬"""

    app.add_css_file(str((THEME_PATH / "topbar.css").resolve()))

    if app.config.html_theme == "furo_tb":
        app.config.html_theme = "furo"
