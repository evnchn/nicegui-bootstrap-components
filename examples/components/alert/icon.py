"""Alerts with leading icons."""

from nicegui import ui

from nicegui_bootstrap_components import bs

_ICON_ALERTS = (
    ("info", "bi-info-circle-fill", "An example info alert with an icon"),
    ("success", "bi-check-circle-fill", "An example success alert with an icon"),
    ("warning", "bi-exclamation-triangle-fill", "An example warning alert with an icon"),
    ("danger", "bi-x-octagon-fill", "An example danger alert with an icon"),
)


def demo() -> None:
    with bs.scope():
        for color, icon, text in _ICON_ALERTS:
            with bs.alert(color=color).classes("d-flex align-items-center"):
                ui.element("i").classes(f"bi {icon} me-2").props("aria-hidden=true")
                ui.label(text)


if __name__ in {"__main__", "__mp_main__"}:
    demo()
    ui.run(title="Alerts with icons")
