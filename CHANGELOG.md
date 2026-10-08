# Changelog

All notable changes to this project are documented in this file. The format is
based on Keep a Changelog and this project adheres to Semantic Versioning.

## [Unreleased]

### Added

- `wrap=True` on `Stack` / `stack()` adds Bootstrap's `flex-wrap`, so long
  horizontal rows flow onto the next line instead of overflowing narrow
  viewports.

### Fixed

- Container-style helpers (`card_header`, `card_body`, `button`, and other
  `BootstrapElement` subclasses) accept a positional text label and can also
  be used as context managers; the label renders first and block contents are
  appended. Passing element children together with a context manager still
  raises `ChildrenError`, now with a message that names the fix.
- Documented that `setup()` is safe before pages exist (it queues shared head
  HTML and registers static files without creating elements).

## [0.1.0] - 2026-09-26

### Added

- Complete Bootstrap 5 component surface with native (`bs`) and DBC-compat
  (`dbc`) APIs.
- Themes and icons.
- Style modes and color modes.
- Persistence and navigation adaptations.
- Examples, documentation site, and visual harness.
