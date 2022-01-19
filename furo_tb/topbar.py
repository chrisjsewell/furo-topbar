"""Code to implement top-bar buttons."""
from textwrap import dedent
from typing import Any, Dict

from docutils import nodes
from sphinx.application import Sphinx


def setup_topbar(app: Sphinx):
    """Setup the top-bar."""
    app.add_config_value("furo_topbar_widgets", None, "html", types=Any)
    app.add_config_value("furo_topbar_hide_on_scroll", False, "html", types=[bool])
    app.connect("html-page-context", _html_page_context)


def _html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree: nodes.document,
) -> None:
    # note see: https://www.sphinx-doc.org/en/master/templating.html
    # for context variables
    if app.config.html_theme != "furo":
        return

    config = get_theme_config(app, "furo_topbar_widgets", None)

    if config is None or "page_source_suffix" not in context:
        return
    assert isinstance(config, dict)
    # TODO schema warnings per key

    if get_theme_config(app, "furo_topbar_hide_on_scroll", False):
        app.add_js_file(
            None,
            body=dedent(
                """\
        /* When the user scrolls down, hide the navbar. When the user scrolls up, show the navbar */
        var prevScrollpos = window.pageYOffset;
        window.onscroll = function() {
        var currentScrollPos = window.pageYOffset;
        if (prevScrollpos > currentScrollPos) {
            document.getElementById("ftb-container").style.top = "0";
        } else {
            document.getElementById("ftb-container").style.top = "-100px";
        }
        prevScrollpos = currentScrollPos;
        }
        """
            ),
        )

    context["furo_topbar"] = {}

    if "github" in config and "url" in config["github"]:
        github_config = config["github"]
        github_repo = github_config["url"]
        github_issue = f"{github_repo}/issues/new?title=Issue%20on%20page%20%2F{pagename}{context['file_suffix']}&body=Your%20issue%20content%20here."
        branch = github_config.get("branch", "main")
        path_to_docs = github_config.get("path_to_docs", "docs")
        github_edit = f"{github_repo}/edit/{branch}/{path_to_docs}/{pagename}{context['page_source_suffix']}"
        # TODO translations
        content = "\n".join(
            [
                f'<a href="{github_repo}">Repository</a>',
                f'<a href="{github_issue}">Open Issue</a>',
                f'<a href="{github_edit}" >Suggest Edit</a>',
            ]
        )
        context["furo_topbar"]["github"] = {
            "button_class": "",
            "button_title": "GitHub Menu",
            "button": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>',
            "dropdown": content,
        }

    if config.get("theme_toggle"):
        context["furo_topbar"]["theme_toggle"] = {
            "button_class": "theme-toggle",
            "button_title": "Toggle Light / Dark / Auto color theme",
            "button": dedent(
                """\
                <svg class="theme-icon-when-auto ftb-theme-toggle"><use href="#svg-sun-half"></use></svg>
                <svg class="theme-icon-when-dark ftb-theme-toggle"><use href="#svg-moon"></use></svg>
                <svg class="theme-icon-when-light ftb-theme-toggle"><use href="#svg-sun"></use></svg>
                """
            ),
            "dropdown": "",
        }

    if config.get("download"):
        pathto = context["pathto"]
        sources_url = f'{pathto("_sources", True)}/{context["sourcename"]}'
        context["furo_topbar"]["download"] = {
            "button_class": "",
            "button_title": "Download Menu",
            "button": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M11.25 9.331V.75a.75.75 0 011.5 0v8.58l1.949-2.11A.75.75 0 1115.8 8.237l-3.25 3.52a.75.75 0 01-1.102 0l-3.25-3.52A.75.75 0 119.3 7.22l1.949 2.111z"></path><path fill-rule="evenodd" d="M2.5 3.75a.25.25 0 01.25-.25h5.5a.75.75 0 100-1.5h-5.5A1.75 1.75 0 001 3.75v11.5c0 .966.784 1.75 1.75 1.75h6.204c-.171 1.375-.805 2.652-1.77 3.757A.75.75 0 007.75 22h8.5a.75.75 0 00.565-1.243c-.964-1.105-1.598-2.382-1.769-3.757h6.204A1.75 1.75 0 0023 15.25V3.75A1.75 1.75 0 0021.25 2h-5.5a.75.75 0 000 1.5h5.5a.25.25 0 01.25.25v11.5a.25.25 0 01-.25.25H2.75a.25.25 0 01-.25-.25V3.75zM10.463 17c-.126 1.266-.564 2.445-1.223 3.5h5.52c-.66-1.055-1.098-2.234-1.223-3.5h-3.074z"></path></svg>',
            "dropdown": f'<a href="{sources_url}">{context["page_source_suffix"]}</a>',
        }

    if config.get("scroll_to_top"):
        context["furo_topbar"]["scroll_to_top"] = {
            "button_class": "clickable",
            "button_title": "Scroll to top",
            "button_onclick": "location.href='#top'",
            "button": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M4.97 12.97a.75.75 0 101.06 1.06L11 9.06v12.19a.75.75 0 001.5 0V9.06l4.97 4.97a.75.75 0 101.06-1.06l-6.25-6.25a.75.75 0 00-1.06 0l-6.25 6.25zM4.75 3.5a.75.75 0 010-1.5h14.5a.75.75 0 010 1.5H4.75z"></path></svg>',
        }

    if config.get("fullscreen"):
        # copied from https://www.w3schools.com/howto/howto_js_navbar_hide_scroll.asp
        app.add_js_file(
            None,
            body=dedent(
                """\
            var elem = document.documentElement;

            function openFullscreen() {
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
            } else if (elem.webkitRequestFullscreen) { /* Safari */
                elem.webkitRequestFullscreen();
            } else if (elem.msRequestFullscreen) { /* IE11 */
                elem.msRequestFullscreen();
            }
            }
        """
            ),
        )
        context["furo_topbar"]["fullscreen"] = {
            "button_class": "clickable",
            "button_title": "Fullscreen",
            "button_onclick": "openFullscreen()",
            "button": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill-rule="evenodd" d="M4.75 4.5a.25.25 0 00-.25.25v3.5a.75.75 0 01-1.5 0v-3.5C3 3.784 3.784 3 4.75 3h3.5a.75.75 0 010 1.5h-3.5zM15 3.75a.75.75 0 01.75-.75h3.5c.966 0 1.75.784 1.75 1.75v3.5a.75.75 0 01-1.5 0v-3.5a.25.25 0 00-.25-.25h-3.5a.75.75 0 01-.75-.75zM3.75 15a.75.75 0 01.75.75v3.5c0 .138.112.25.25.25h3.5a.75.75 0 010 1.5h-3.5A1.75 1.75 0 013 19.25v-3.5a.75.75 0 01.75-.75zm16.5 0a.75.75 0 01.75.75v3.5A1.75 1.75 0 0119.25 21h-3.5a.75.75 0 010-1.5h3.5a.25.25 0 00.25-.25v-3.5a.75.75 0 01.75-.75z"></path></svg>',
        }

    # sort the keys in the order provided
    context["furo_topbar"] = {
        key: context["furo_topbar"][key]
        for key in config
        if key in context["furo_topbar"]
    }


def get_theme_config(app: Sphinx, name: str, default=None):
    # account for https://github.com/sphinx-doc/sphinx/issues/10120
    config = getattr(app.config, name, default)
    if (
        hasattr(app.config, "overrides")
        and app.config.overrides.get(name, default) != default
    ):
        config = app.config.overrides[name]
    elif (
        hasattr(app.config, "_raw_config")
        and app.config._raw_config.get(name, default) != default
    ):
        config = app.config._raw_config[name]
    return config
