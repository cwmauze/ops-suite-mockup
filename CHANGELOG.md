# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.18] - 2026-06-18
### Added
- Added an interactive manual sync animation to the "Last sync" status in the global header. When tapped, the checkmark changes to a blue spinning arrow and the text updates to "Syncing..." for 10 seconds before resetting.

## [0.0.17] - 2026-06-18
### Changed
- Reorganized Action Buttons into distinct "Flight Actions" (Dispatch, Edit, Risk) and "Leg Actions" (Config, Weight, CG) for better visual hierarchy.
- Removed the text headers for "Flight Actions" and "Leg Actions" to ruthlessly compress vertical space, moving the current VCF label directly into the "Config" button.
- Replaced the floating save/close bar with a standard 5-tab App Bottom Navigation Bar (`Home`, `Map`, `Manifest`, `Library`, `Chat`), using clean SVG icons instead of emojis.
- Restored the "Save", "Save/Add Leg", "Close Flt" buttons and the "Manifest Verified" toggle, placing them logically at the very bottom of the scrollable manifest page (just above the new navigation bar).
- Refactored the "Route & Times" Origin and Destination inputs into separate rows with dedicated "Departed (Z)" and "Arrived (Z)" fields alongside quick-action "NOW" buttons.
- Added a "Team" badge ("RWI Medical Team") to the global header under the manifest details.
- Cleaned up the IFR toggle by removing the redundant "IFR FLIGHT" label and renaming the toggle to "IFR leg".
- Moved the Theme toggle button into the top `.sync-bar` to free up real estate in the global header.
- Moved the Dispatch, Edit Flt, and Risk Form action tiles into the global header to save vertical space, placing the fully red Dispatch button on the far right to clearly indicate it needs attention.
- Removed the redundant "Route & Times" section header to further compress vertical layout space, as the Leg indicators are now handled via the tabs.
- Removed the "Stations" section header to reclaim additional vertical space.
- Refactored Spatial Station cards to position the weight input inline with the station title (e.g., `PILOT (RIGHT) [0 KG]`), eliminating an entire line to drastically save vertical scrolling.
- Comprehensively reduced padding, margins, gaps, and component heights (like the bottom navigation bar and form inputs) throughout the entire layout by 75% to practically eliminate unnecessary vertical "dead space" and prevent scrolling.
- Spelled out all Spatial Station titles explicitly in full (e.g., "COPILOT SEAT", "AFT FACING LEFT HAND").
- Removed the "Optional Patient Name" input field entirely from the Left Hand Litter station to save vertical space.
- Removed the default "Empty" text from the Aft Facing Right Hand seat.

## [0.0.16] - 2026-06-18
### Changed
- Refactored the Dispatch Number area, moving it from the "Route & Times" section up into a prominent, interactive button at the top of the screen (in the `.global-header`).

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
