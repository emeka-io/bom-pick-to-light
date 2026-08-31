# ADR 001: Project Foundation & Architecture Stack

* **Status:** Accepted
* **Date:** 2026-08-31
* **Context:** A robust, deterministic architecture is required to bridge desktop BOM parsing with physical pick-to-light bin hardware.

---

## 1. Decision Drivers

* Need for fast string normalization and CSV/JSON processing on the host.
* Requirement for real-time LED timing and button interrupt handling.
* Preference for modular hardware and standard open-source tools.

---

## 2. Decision Summary

| Domain | Choice | Rationale | Alternatives Considered |
| :--- | :--- | :--- | :--- |
| **Host Environment** | Python 3.10+ | Excellent ecosystem for data processing (`dataclasses`, `pytest`) | C++ (higher overhead), Node.js |
| **Microcontroller** | ESP32 (PlatformIO) | High GPIO count, native hardware timers, low cost | Arduino Uno (limited RAM/IO), STM32 |
| **Comms Protocol** | USB-CDC (UART Serial) | Simple, low-latency, cross-platform compatibility | WebSockets / Wi-Fi (added latency) |
| **LED Architecture** | WS2812B NeoPixel | Single data pin drives multiple RGB bin indicators | Discrete GPIO LEDs (limits bin count) |

---

## 3. Consequences

* **Positive:** Decoupled architecture allows core software matching logic to be tested via Python simulators without physical hardware.
* **Negative:** Host-MCU serial connection requires robust retry and packet checksum handling for reliable field operations.