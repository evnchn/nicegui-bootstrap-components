from nicegui import ui

from nicegui_bootstrap_components import StyleMode, bs, setup


def demo():
    with bs.scope():
        with bs.collapse(is_open=True, dimension="width"):
            ui.label("Revealed along the width axis.")

        with bs.collapse(is_open=True, navbar=True, id="main-nav-collapse"), bs.nav():
            with bs.nav_item():
                bs.nav_link("Home", href="#", active=True)
            with bs.nav_item():
                bs.nav_link("Docs", href="#")
            with bs.nav_item():
                bs.nav_link("Blog", href="#")


if __name__ in {"__main__", "__mp_main__"}:
    setup(mode=StyleMode.MIXED)
    demo()
    ui.run(title="Collapse dimension and navbar")
