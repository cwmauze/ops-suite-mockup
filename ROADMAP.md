# Ops Suite Roadmap

This roadmap tracks feature requests, outstanding bugs, and architectural changes for the Ops Suite prototype. 

## High Priority / Active Work
- [ ] **Modal Redesigns**: Completely revamp the Risk Modal, Weight Details, Edit Manifest, and Equipment Editor. Focus on ruthless compression of vertical space and touch-friendly interaction.
- [ ] **Layout Refactoring**: Implement a final pass on the entire app interface to optimize for "breathing room" after all functional elements are locked in. 

## Backlog / Upcoming
- [ ] Implement backend synchronization logic for offline caching.
- [ ] Add true routing so the Bottom Navigation Bar properly switches between distinct views (Map, Library, Chat).
- [ ] Complete personnel selection auto-suggest with a live search against a realistic dummy database.
- [ ] Lock down exact styling parameters for high-contrast accessibility modes based on web accessibility guidelines.
- [ ] **Souls on Board (SOB) auto-calculation**: Automate the SOB field to dynamically calculate based on the entries in the personnel stations area.
- [ ] **Quick Offload/Onload**: Add "Offload crew and patient" and "Onload Crew" buttons to speed creating new flight legs.
- [ ] **Clickable Waypoints**: Investigate linking waypoints in the flight route to be clickable, opening their respective entries in ForeFlight and/or the hospital/heliport guide. Additionally, explore providing context-rich data (especially for scenes), such as satellite photos or a "virtual high/low recon" (a visual 3D orbit around the LZ using satellite and terrain imagery) with nearby obstacles and terrain visually highlighted.
- [ ] **Flight Request Page Upscale**: Major upscale of the flight request page to include more comprehensive data about duty times, and much more context about individual legs (including estimated fuel, terrain, obstacles, etc.).

---
*Note: This document is a living artifact and will be updated as new requirements are discovered.*
