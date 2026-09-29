from nicegui import ui

from nicegui_bootstrap_components import StyleMode, bs, setup


def demo() -> None:
    with bs.scope():
        bs.placeholder(animation="glow", color="primary", xs=12)
        bs.placeholder(animation="wave", color="secondary", xs=12)


if __name__ in {"__main__", "__mp_main__"}:
    setup(mode=StyleMode.MIXED)
    demo()
    ui.run(title="Placeholder animation")
