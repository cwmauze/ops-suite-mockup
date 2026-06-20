# Ops Suite Roadmap

This roadmap tracks feature requests, outstanding bugs, and architectural changes for the Ops Suite prototype. 

## High Priority / Active Work
- [x] **Theme Toggles**: Expand beyond Light and Dark modes to include a Neutral mid-theme, High-Contrast Light, and High-Contrast Dark. *(Completed in v0.0.23)*
- [ ] **Modal Redesigns**: Completely revamp the Risk Modal, Weight Details, Edit Manifest, and Equipment Editor. Focus on ruthless compression of vertical space and touch-friendly interaction.
- [ ] **Layout Refactoring**: Implement a final pass on the entire app interface to optimize for "breathing room" after all functional elements are locked in. 
- [x] **Default Theme**: Set the new "Mid" neutral theme as the default theme on initial load to work equally well in both bright sunlight and dark cockpits, superseding the request for Dark Mode. *(Completed in v0.2.1)*.
- [x] **Duty In Layout Polish**: Refactor the Duty In screen to remove the duplicate "Rest from last" display. Fix the wide spacing issue between left-justified labels and right-justified data (for "Rest from last" and "Consecutive shifts") by using compact, half-screen bars *(Requested by Laura McColm)*. *(Completed)*

## Backlog / Upcoming
- [ ] Implement backend synchronization logic for offline caching.
- [ ] Add true routing so the Bottom Navigation Bar properly switches between distinct views (Map, Library, Chat).
- [ ] Complete personnel selection auto-suggest with a live search against a realistic dummy database.
- [ ] Lock down exact styling parameters for high-contrast accessibility modes based on web accessibility guidelines.
- [ ] **Souls on Board (SOB) auto-calculation**: Automate the SOB field to dynamically calculate based on the entries in the personnel stations area.
- [ ] **Quick Offload/Onload**: Add "Offload crew and patient" and "Onload Crew" buttons to speed creating new flight legs.

---
*Note: This document is a living artifact and will be updated as new requirements are discovered.*
