# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.15] - 2026-06-18
### Changed
- Removed the occupant name input field for the "LH Litter (Patient)" station. This station now only accepts a weight input to match actual operational workflows (no names entered).

## [0.0.14] - 2026-06-18
### Changed
- Removed default placeholder names (Mauze, Petty, Dail) from station occupants so the user can test the smart dropdown cleanly.

## [0.0.13] - 2026-06-18
### Changed
- Replaced the full-screen personnel selection modal with an inline `<input>` that has a smart-search autocomplete dropdown. Typing into the field filters the dummy data list, and tapping populates it seamlessly below without obstructing the whole UI.

## [0.0.12] - 2026-06-18
### Added
- Created an interactive personnel list simulating a crew selection. Clicking on a seat's occupant row opens a modal containing 10 male action movie stars and 10 female bombshell actresses with their approximate weights.
- Selecting a star updates the occupant name and seat weight dynamically in the UI.

## [0.0.11] - 2026-06-18
### Changed
- Swapped the UI order so that leg selection tabs appear below the stoplight buttons (`.sticky-action-bar`).

## [0.0.10] - 2026-06-18
### Fixed
- Fixed black borders in PWA mode by applying `viewport-fit=cover` and iOS safe area environment variables.
- Added explicit PWA standalone detection logic.
- Hid the mockup version overlay when in native PWA mode.

## [0.0.9] - 2026-06-18
### Added
- Added `apple-mobile-web-app-capable` and related meta tags to enable full-screen, standalone PWA behavior without the Safari URL bar when users tap "Add to Home Screen" on iOS.

## [0.0.8] - 2026-06-18
### Added
- Native mode detection: When opened on an actual iPad or mobile device, the simulated device frame is removed and the UI scales dynamically to fill 100% of the viewport seamlessly.

## [0.0.7] - 2026-06-18
### Added
- Warning message when attempting to add a leg without verifying the manifest.

### Changed
- Removed the "+ Add Leg" button from the top tabs.
- Renamed the bottom add leg button to "Save/Add Leg".
- Moved the "Manifest Verified" slider to the right side of the action buttons.

## [0.0.6] - 2026-06-18
### Changed
- Changed changelog modal to a right-aligned side panel that doesn't block the simulated iPad display.

## [0.0.5] - 2026-06-18
### Added
- Made the external version number a clickable button that displays a pop-up changelog modal over the screen.

## [0.0.4] - 2026-06-18
### Added
- Added responsive scaling script so the iPad device frame always zooms to fit entirely within the user's browser vertically and horizontally.

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
