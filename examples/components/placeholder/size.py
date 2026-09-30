from nicegui import ui

from nicegui_bootstrap_components import StyleMode, bs, setup


def demo() -> None:
    with bs.scope():
        ui.label("size='lg'")
        bs.placeholder(size="lg", color="secondary", animation="glow", xs=12)
        ui.label("size='sm'")
        bs.placeholder(size="sm", color="secondary", animation="glow", xs=12)


if __name__ in {"__main__", "__mp_main__"}:
    setup(mode=StyleMode.MIXED)
    demo()
    ui.run(title="Placeholder size")
