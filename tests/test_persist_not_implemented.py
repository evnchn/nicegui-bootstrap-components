"""persist= is not implemented on Input, Textarea or Carousel.

These constructors used to accept persist='local' / 'session' and drop it on the
floor, while the docs promised restore-on-reload. Non-'off' values now raise.
"""

from __future__ import annotations

import pytest

from nicegui_bootstrap_components._base import UnsupportedPropError
from nicegui_bootstrap_components.bs._carousel import Carousel
from nicegui_bootstrap_components.bs._inputs import Input, Textarea


@pytest.mark.parametrize("mode", ["local", "session"])
def test_input_persist_not_implemented(mode: str) -> None:
    with pytest.raises(UnsupportedPropError, match="persist"):
        Input(id="name", persist=mode)


@pytest.mark.parametrize("mode", ["local", "session"])
def test_textarea_persist_not_implemented(mode: str) -> None:
    with pytest.raises(UnsupportedPropError, match="persist"):
        Textarea(id="notes", persist=mode)


@pytest.mark.parametrize("mode", ["local", "session"])
def test_carousel_persist_not_implemented(mode: str) -> None:
    with pytest.raises(UnsupportedPropError, match="persist"):
        Carousel(items=[{"content": "a"}], id="slides", persist=mode)
