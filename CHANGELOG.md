# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 2026-06-18
### Changed
- Moved the mockup version number outside of the iPad screen depiction so it's clear it tracks the mockup itself, not the UI.

## [0.0.2] - 2026-06-18
### Fixed
- Hotfix: Changed the default UI theme back to light mode.

## [0.0.1] - 2026-06-18
### Added
- Created initial `CHANGELOG.md`.
- Displayed version number `v0.0.1` in the main header.

### Changed
- Refactored `prototype/index.html` to a compressed, zero-vertical-scroll layout.
- Switched default theme to dark mode for NVG cockpit compatibility.
- Consolidated global header to embed metrics into "Stop-Light" validation buttons.
- Restructured `Route & Times` section to compress inputs.

### Fixed
- Added a rigid "Close Flight" modal with strict hard-stop JavaScript validations for Night/NVG/IFR limits (BUG-005).
- Re-labeled spatial station placeholders.
