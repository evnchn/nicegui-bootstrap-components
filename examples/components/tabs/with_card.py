from nicegui import ui

from nicegui_bootstrap_components import StyleMode, bs, setup


def demo() -> None:
    with bs.scope():
        bs.Tabs(
            bs.Tab("Day view content.", label="Day"),
            bs.Tab("Week view content.", label="Week"),
            card=True,
            active_tab="Day",
        )


if __name__ in {"__main__", "__mp_main__"}:
    setup(mode=StyleMode.MIXED)
    demo()
    ui.run()
