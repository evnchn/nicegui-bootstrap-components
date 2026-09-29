from nicegui import ui

from nicegui_bootstrap_components import StyleMode, bs, setup


def demo() -> None:
    with bs.scope(), bs.card():
        ui.label("Comments").classes("h5")
        bs.placeholder(animation="glow", color="secondary", xs=12)
        bs.placeholder(color="secondary", xs=9)


if __name__ in {"__main__", "__mp_main__"}:
    setup(mode=StyleMode.MIXED)
    demo()
    ui.run(title="Placeholder basic")
