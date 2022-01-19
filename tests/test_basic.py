"""A basic test suite for the project."""
from io import StringIO
from pathlib import Path
from typing import Callable

from bs4 import BeautifulSoup
import pytest
from sphinx.testing.util import SphinxTestApp, path


@pytest.fixture()
def app_factory(tmp_path: Path) -> Callable[[str, dict], SphinxTestApp]:
    """Create a Sphinx application."""

    def _create_app(content: str, confoverrides: dict) -> SphinxTestApp:
        # generate a conf.py file
        conf_py = tmp_path / "conf.py"
        conf_py.touch()
        index_rst = tmp_path / "index.rst"
        index_rst.write_text(content.rstrip() + "\n", encoding="utf-8")

        status, warning = StringIO(), StringIO()
        return SphinxTestApp(
            srcdir=path(str(tmp_path)),
            status=status,
            warning=warning,
            confoverrides=confoverrides,
        )

    yield _create_app


def test_no_widgets(app_factory: Callable[[str, dict], SphinxTestApp]):
    """Test building, with no widgets specified."""
    app = app_factory("Test\n----", {"html_theme": "furo_tb"})
    app.build()
    assert app.statuscode == 0
    assert app.outdir.joinpath("index.html").exists()
    content = BeautifulSoup(
        app.outdir.joinpath("index.html").read_text(), "html.parser"
    )
    assert not content.select("div.ftb-container")


def test_a_widget(app_factory: Callable[[str, dict], SphinxTestApp]):
    """Test the basic build, with a widget specified."""
    app = app_factory(
        "Test\n----",
        {"html_theme": "furo_tb", "furo_topbar_widgets": {"scroll_to_top": True}},
    )
    app.build()
    assert app.statuscode == 0
    assert app.outdir.joinpath("index.html").exists()
    content = BeautifulSoup(
        app.outdir.joinpath("index.html").read_text(), "html.parser"
    )
    assert content.select("div.ftb-container")
