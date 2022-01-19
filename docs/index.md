# furo-topbar (IN-DEVELOPMENT)

## Introduction

`furo-topbar` is an extension of the excellent [furo] sphinx theme (all attribution to `@pradsyung`!).
It aims to add an optional top-bar to pages, with a **pluggable** set of widgets, to add functionality to your documentation.
the widgets are intended to be as unobtrusive as possible, and fit in with the rest of the theme.

Simply add the theme to your sphinx configuration, then you can specify the set of widgets to use in the topbar, with related configuration:

```python
html_theme = "furo_tb"
# theme options inherit directly from furo
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
# optional:
# furo_topbar_hide_on_scroll = True
```

Widgets will only be shown if they are included in `furo_topbar_widgets` and the order of the widgets on the page will be the same as in the key order.

The current set of widgets are:

scroll_to_top
: Press to return to the top of the page

fullscreen
: Toggle fullscreen mode

download
: Download the current page in different formats

theme_toggle
: Toggle between the light and dark theme

github
: Add options, for those using GitHub as a source repository, to open issues and suggest edits on it.

It is hoped that eventually the plugin system will be exposed to allow for anyone to add their own widgets.

Widgets simply specify a dictionary of set options, which are then handled by the `furo_topbar` template, to create the final HTML.
For example, the `scroll_to_top` plugin returns:

```python
{
"button_class": "clickable",
"button_title": "Scroll to top",
"button_onclick": "location.href='#top'",
"button": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M4.97 12.97a.75.75 0 101.06 1.06L11 9.06v12.19a.75.75 0 001.5 0V9.06l4.97 4.97a.75.75 0 101.06-1.06l-6.25-6.25a.75.75 0 00-1.06 0l-6.25 6.25zM4.75 3.5a.75.75 0 010-1.5h14.5a.75.75 0 010 1.5H4.75z"></path></svg>',
}
```

## Design discussion

In the [Executable Books Project](https://executablebooks.org), we have been developing [sphinx-book-theme](https://sphinx-book-theme.readthedocs.io), with a set of features focussed on supporting [Jupyter Book](https://jupyterbook.org).

IMO the general layout and styling of [furo] is much nicer, but it lacks some of the extra features required to be a drop in replacement for [sphinx-book-theme].
These currently include: the top widgets, [Margin content](https://sphinx-book-theme.readthedocs.io/en/latest/content-blocks.html#margin-content), and some of the infrastructure around internationalisation (i.e. text translations).

In addition, there has been an [open issue](https://github.com/executablebooks/meta/issues/279) for a while, to make the theme more configurable.

This is also a "companion" to the already configurable [sidebar elements](https://pradyunsg.me/furo/customisation/sidebar/).

The design here is by no means final, but the idea is to have a simple hook, whereby developers can specify the icon and functionality of a widget, then `furo-topbar` handles their composition into a consistent toolbar.

Building on [furo], the `furo-topbar` very simply adds an additional `div.ftb-container` on the `page.html` template (only when widgets are present), residing at the top of the `article-container` and set to be "sticky".
It also removes the `theme-toggle` button, in order to relocate it to the widget bar.
`furo-topbar` then handles populating the `ftb-container`, in a standardised way for all widgets.

Currently, the whole `page.html` has to be copied from [furo], it would be nice if this did not have to be the case. Or even if this was adopted more specifically by [furo]!

## Moving forward

- Can this extension be more formally integrated with [furo]? (`@pradyung`'s input would be great!)
- Could it even be "theme agnostic", i.e. used within any theme?
- Allow, for example, for [myst-nb](https://myst-nb.readthedocs.io), to define a widget for launching Jupyter Notebooks (in Binder, etc)

[furo]: https://github.com/pradyunsg/furo
[sphinx-book-theme]: https://sphinx-book-theme.readthedocs.io
