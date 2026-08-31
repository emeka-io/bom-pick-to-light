# Design Specification ? Physical & Mechanical Layout

## 1. Overview
This document defines the physical grid layout, mounting geometry, and component integration guidelines for the Pick-to-Light bin matrix frame.

---

## 2. Bin Grid Dimensions & Coordinate System

The physical rack uses a 2D Cartesian coordinate system where the top-left bin represents `(X=1, Y=1)`.

| Dimension Metric | Value | Notes |
| :--- | :--- | :--- |
| **Grid Capacity** | 2 Rows ? 2 Columns (4 Bins) | Scalable up to 4?4 grid |
| **Bin Width (X-axis)** | 100 mm | Outer width per storage bin |
| **Bin Height (Y-axis)** | 80 mm | Outer height per storage bin |
| **Bin Depth (Z-axis)** | 120 mm | Component storage depth |
| **Horizontal Spacing** | 120 mm Pitch | Distance between center points of adjacent X bins |
| **Vertical Spacing** | 100 mm Pitch | Distance between center points of adjacent Y bins |

---

## 3. Indicator & Control Placement

Each bin compartment integrates two hardware human-machine interface (HMI) elements:

1. **WS2812B RGB LED Indicator:** Mounted centrally on the upper lip of each bin compartment for maximum operator visibility.
2. **Tactile Confirmation Button:** Mounted directly below the LED indicator on the front bezel, allowing one-handed pick-and-confirm execution.

---

## 4. Cable Routing & Wire Channels

* **5V Power & Ground Rails:** Run horizontally across the back of each row (Y-axis) using 20 AWG stranded wire.
* **LED Data Bus:** Daisy-chained in an S-curve sequence across the WS2812B pixels using 24 AWG wire.
* **Switch Signal Lines:** Individual signal wires routed from each bin bezel back to the ESP32 GPIO header.
