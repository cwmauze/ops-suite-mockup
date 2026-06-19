# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.6] - 2026-06-19
### Changed
- Renamed "Left Hand Litter (Patient)" to "LEFT HAND LITTER" and perfectly aligned its weight input with adjacent stations.
- Reformatted dummy personnel names in the smart search dropdown to "Lastname, Firstname".

## [0.1.5] - 2026-06-19
### Added
- Added the ability for users to enter GPS coordinates directly into the Comm Center Simulator to generate unidentifiable "SCENE" locations.
- Supported multiple coordinate input formats including Decimal Degrees (e.g. `35.85,-77.89`) and Degrees Decimal Minutes (e.g. `3551.38N/07753.51W`).
- Formatted entered coordinates securely for the ForeFlight URL scheme so they map seamlessly to ForeFlight natively.

## [0.1.4] - 2026-06-19
### Fixed
- Fixed an issue where iOS devices aggressively cached an outdated Comm Center Simulator script by standardizing a cache-busting query parameter across all HTML pages.

## [0.1.3] - 2026-06-19
### Fixed
- Fixed an issue where the Comm Center Simulator would not appear when tapping the Chat button on large screens running in native PWA mode (e.g. iPad Pro landscape) due to CSS media query limitations.

## [0.1.2] - 2026-06-19
### Fixed
- Fixed an issue where the changelog UI was cut off by an unescaped `<script>` tag within historic release notes.
- Locked the changelog panel to the viewport height for full scrollability on mobile.
- Added the current mockup version tag to the top sync bar.

## [0.1.1] - 2026-06-19
### Added
- Integrated ForeFlight URL scheme to open active flight routes directly in the ForeFlight Mobile app.
- Hid the Comm Center Simulator dev tools behind the "Chat" bottom navigation item to make it accessible as a toggleable overlay on mobile devices.

## [0.1.0] - 2026-06-19
### Added
- Rebuilt Initial Request Receipt logic in `flightlog.html` to automatically generate only the first leg upon receiving a broadcast flight request.
- Implemented Progressive Leg Generation in the "Save/Add Leg" workflow, dynamically pulling the next leg's origin and destination from the active Comm Center route based on the leg sequence.
- Added Exhausted Waypoint Handling logic to automatically use the previous destination as the new origin with a blank destination field when the Comm Center route sequence is completed.


## [0.0.38] - 2026-06-19
### Added
- Refactored the Comm Center Simulator UI from a static text input to a dynamic, live-updating list of waypoints.
- Added progressive leg generation to the Manifest page (`flightlog.html`) so that it only automatically generates the first leg upon dispatch, and progressively auto-fills subsequent legs based on the flight request as the user saves each leg.
- Added fallback logic for progressive leg generation that safely handles exhausted waypoints by using the previous destination as the new origin.

## [0.0.37] - 2026-06-19
### Changed
- Refined route header flex proportions in `flightlog.html` to widen "Origin", "Destination", "Time", and "NOW" button inputs while perfectly right-sizing "Date" inputs.
- Centered route header labels (Departure Date, Arrival Date, Time) over their respective inputs.
- Swapped out the emoji theme toggle for a native-looking scalable SVG icon.

### Fixed
- Fixed bug where fuel field entries (tanks, burn rate, calculated time) were globally applied; they now correctly save per leg and dynamically inherit values when adding new legs.

## [0.0.36] - 2026-06-19
### Changed
- Split Fuel Time input into separate Hours and Minutes fields with 'H' and 'M' annotations.
- Updated the `--input-bg` CSS variable to a subtle cool gray (`#f7f7f9`) to provide better contrast against the section cards.
- Split Departure and Arrival Time inputs into separate date and time fields.
- Re-labeled "Departed" and "Arrived" to "Departure Date/Time" and "Arrival Date/Time", and removed placeholders.

## [0.0.35] - 2026-06-19
### Added
- Added Quick "Offload Crew and Patient" / "Onload Crew" features to the roadmap.

### Changed
- Reclaimed vertical space in `flightlog.html` by radically reducing padding and gaps within the container and seat cards, ensuring the entire form fits on a single iPad screen without scrolling.
- Re-labeled "Obst. Height" to "HIGHEST OBSTACLE".
- Re-labeled "Back" to "Manifest List" in the header.
- Re-labeled "Flight Req" to "Flight Request" and "Edit Flt" to "Edit Flight".

### Fixed
- Fixed clear "x" buttons on inputs to dynamically hide via CSS `:placeholder-shown` when no text is present.

## [0.0.34] - 2026-06-18
### Added
- Created `flight_request.html` mockup based on the flight request screenshot.
- Added a "View Flight Request" link on the `home.html` dashboard.
- Linked "Edit Manifest" from the flight request view to `flightlog.html`.
- Added a "Flight Req" button in `flightlog.html` to return to the request view.
- Added global sync bar and bottom navigation bar to `flight_request.html`.

### Changed
- Increased vertical padding of bottom action buttons in `flightlog.html` to improve touch target size.
- Compressed map height and component padding in `flight_request.html` to fit content on a single screen seamlessly.

## [0.0.33] - 2026-06-18
### Fixed
- Fixed an overlapping layout bug where the simulated text keyboard clipped beneath the simulated numpad. This was caused by the browser's native `scrollIntoView()` scrolling the hidden boundaries of the app screen. Replaced with an isolated `scrollBy` method and strict visibility transitions.

## [0.0.32] - 2026-06-18
### Fixed
- Fixed a bug where the "Fwd Facing Aft Seat Right Hand" station was missing the quick-clear "x" button to remove personnel.

## [0.0.31] - 2026-06-18
### Added
- Upgraded the "hide keyboard" button on the simulated numpad and keyboard to an explicit iOS-style stow SVG icon.
- Selecting personnel from the smart dropdown automatically stows the keyboard.

## [0.0.30] - 2026-06-18
### Changed
- Refactored Route & Times layout to condense Obstacle Height and IFR leg toggle.
- Removed S.O.B. input from the Fuel Stations block.
- Standardized the padding, font weight, and heights for Arrived/Departed inputs and their adjacent "NOW" buttons.
- Added subtle CSS visual cues (using `:has()`) to automatically highlight seat cards when a station is occupied.

## [0.0.29] - 2026-06-18
### Changed
- Replaced hardcoded pilot names (Stallone, Charles) with Chuck Norris across the UI, leaving Stallone in the dropdown pilot selection list.

## [0.0.28] - 2026-06-18
### Changed
- Removed hardcoded pilot names (Mauze, Leake) from the UI mockups and replaced them with action heroes.
- Cleaned up the repository by permanently deleting all temporary one-off Python scripts, text dumps, and swift files.

## [0.0.27] - 2026-06-18
### Changed
- Refactored the Mockup version and changelog UI to sit cleanly at the bottom of the left instructions panel instead of floating randomly.
- Made the changelog panel overlay available on all simulator pages (index, home, flightlog, manifest).
- Fixed CSS scope bugs to ensure the mockup version tag and changelog display properly across all views in simulator mode, while still hiding seamlessly in native PWA mode.

## [0.0.26] - 2026-06-18
### Added
- Applied global theme toggle logic across all pages.
- Saved user theme preferences to `localStorage` for cross-page persistence.
- Unified theme CSS variables for seamless light/dark/high-contrast mode switching across all layouts.

## [0.0.25] - 2026-06-18
### Fixed
- Standardized the top Sync Bar and Bottom Navigation Bar across all main pages.
- Corrected CSS anchoring for the bottom navigation bar so it sticks to the bottom of the device frame.
- Fixed severe Javascript syntax errors caused by malformed `<script>` tags, restoring the functionality of the Theme Toggle and Sync Animations.

## [0.0.24] - 2026-06-18
### Added
- Created a custom 24-hour iOS-style Time Picker with scroll-snapping rollers to streamline minute-by-minute adjustments, bypassing the clunky native iOS `datetime-local` picker.
- Implemented dynamic Risk Assessment logic containing all 46 risk items. The dashboard tile automatically calculates the score, updates the pill, and changes color (Green/Orange/Red) based on the current threshold.
- Added a "Sign to Approve" toggle in the Risk Assessment modal. When activated, it forces the dashboard tile to green and appends a "✓" symbol.
- Refactored the Fuel section to fit Supply Tanks, Main tanks, Burn Rate, Fuel time, and S.O.B. into a single, compact horizontal row.
- Bound the "IFR leg" toggle to the underlying `AppState` engine so it tracks securely on a per-leg basis, defaulting to OFF for newly created legs.
- Implemented a tiered UI decluttering system for Leg tabs to automatically compress text length and prevent horizontal scrolling as more legs are added.
- Added dynamic local timestamps to the "Last sync" status so it reflects the exact time of page load and updates upon manual sync completion.

### Changed
- Renamed the dashboard "Risk Form" tile to "Risk Assessment".
- Moved the Leg deletion action from an inline "x" on the tabs to a dedicated, red-outlined `Delete Leg` button at the bottom of the screen with a confirmation prompt to prevent accidental fat-finger deletions.

## [0.0.23] - 2026-06-18
### Added
- Expanded theme options. Replaced dual light/dark mode with 5 distinct modes: Light, Dark, Neutral, High-Contrast Light, and High-Contrast Dark.

## [0.0.22] - 2026-06-18
### Added
- Upgraded the "Departed" and "Arrived" inputs to full datetime fields, supporting the YYYY-MM-DD format plus time.
- Wired up the "NOW" buttons to automatically inject the current UTC (Zulu) date and time into their respective fields.
- Enhanced touch-friendly interactions: weight inputs now trigger the native numeric keypad on mobile/tablet devices (`inputmode="decimal"`).

## [0.0.21] - 2026-06-18
### Added
- Added a visual CSS mockup of an iOS keyboard that automatically slides up from the bottom when clicking into any text/number input. This adds realism to desktop demonstrations. The keyboard is automatically disabled on actual touch devices (like a real iPad) to prevent duplicate keyboards.

## [0.0.20] - 2026-06-18
### Added
- Refactored the Fuel Stations section. Replaced the manual Fuel Time input with a live-calculated Fuel Time field that auto-computes `(Supply + Main) / Burn Rate`, and added a new input for the Burn Rate (defaulting to 74 GPH).

## [0.0.19] - 2026-06-18
### Added
- Added quick "x" clear buttons inside personnel selection fields to rapidly remove occupants from seats.

### Fixed
- Fixed an architectural layout bug that caused the bottom navigation bar and action buttons to spill outside of the iPad frame container.

## [0.0.18] - 2026-06-18
### Added
- Added an interactive manual sync animation to the "Last sync" status in the global header. When tapped, the checkmark changes to a blue spinning arrow and the text updates to "Syncing..." for 10 seconds before resetting.

### Changed
- Moved the "Save", "Save/Add Leg", "Close Flt" buttons, and the "Verified" toggle out of the scrolling `main-content` container and fixed them absolutely to the bottom of the screen, just above the navigation bar. 

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
- Removed default placeholder names (Norris, Petty, Dail) from station occupants so the user can test the smart dropdown cleanly.

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
