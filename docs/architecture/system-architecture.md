# System Architecture — BOM Pick-to-Light System

## 1. High-Level System Overview

The system is structured as a decoupled, multi-tier architecture consisting of a **Host Control Engine (Python)**, a **Real-Time Controller (ESP32 Firmware)**, and a **Physical Hardware Interface (Bin Module Assembly)**.

+---------------------------------------------------------------+
|                       Host Software Layer                     |
|                                                               |
|  [ BOM File ] ---> [ Parser ] ---> [ Matching Engine ]         |
|  (CSV/JSON)                             |                     |
|                                         v                     |
|                                  [ Pick Queue ]               |
|                                         |                     |
|                                         v                     |
|                              [ Serial Interface Engine ]      |
+---------------------------------------------------------------+
|
(UART / USB)
v
+---------------------------------------------------------------+
|                      Firmware Control Layer                   |
|                                                               |
|                   [ Serial Command Router ]                   |
|                                 |                             |
|                                 v                             |
|                  [ State Machine Controller ]                 |
|                   /                         \                 |
|                  v                           v                |
|           [ LED Driver ]               [ Input Handler ]      |
+---------------------------------------------------------------+
|                             |
v                             v
+---------------------------------------------------------------+
|                         Physical Layer                        |
|                                                               |
|            [ Addressable LEDs ]       [ Pick Buttons/Sensors ] |
+---------------------------------------------------------------+

---

## 2. Core Subsystems

### 2.1 Host Software Subsystem (Python)
* **BOM Parser:** Ingests raw assembly component listings, cleans designators, and standardizes part numbers.
* **Inventory Data Layer:** Maintains state for local bin assignments, part quantities, and bin coordinates.
* **Matching & Queue Engine:** Reconciles BOM line items with available inventory, flags stock deficits, and builds a coordinate-sorted pick list.
* **Host Communications Manager:** Packs structured commands (e.g., `SET_LED:BIN_04:COLOR_GREEN:PULSE`) and sends them over the serial connection while listening for hardware acknowledgment events.

### 2.2 Firmware Subsystem (ESP32 / PlatformIO)
* **Command Dispatcher:** Non-blocking serial parser receiving incoming packets from the host and validating checksums/formatting.
* **Finite State Machine (FSM):** Manages system states (`IDLE`, `PICK_ACTIVE`, `PICK_CONFIRMED`, `ERROR`).
* **LED Driver Subsystem:** Drives NeoPixel/WS2812B addressable strips or discrete LED indicators corresponding to physical bin locations.
* **Sensor/Button Handler:** Reads tactile button presses or optical sensor interruptions with hardware debouncing to trigger pick complete events.

---

## 3. Data Flow & Event Cycle

1. **Ingestion Phase:** User loads a BOM file into the Host Engine.
2. **Matching Phase:** Host Engine queries internal inventory model to pair BOM parts with Bin IDs.
3. **Queue Creation:** Host generates an optimized sequential pick list.
4. **Execution Cycle:**
   * Host sends command to illuminate target bin (`Bin N`).
   * MCU receives command, sets LED state to Active (e.g., Pulsing Green).
   * Operator identifies target bin and retrieves physical parts.
   * Operator presses confirmation button at `Bin N`.
   * MCU detects input, sends `ACK:BIN_N_COMPLETE` packet to Host.
   * Host updates local inventory counts and advances pick queue to `Bin N+1`.

---

## 4. Hardware & Interface Boundary

| Component | Technology / Protocol | Purpose |
| :--- | :--- | :--- |
| Host-to-MCU | USB-CDC (UART Serial) | Bidirectional packet transmission |
| Microcontroller | ESP32 | High-speed IO timing and FSM control |
| Indicators | WS2812B / Neopixel / Discrete LEDs | Visual guidance per bin |
| Pick Verification | Tactile Switch / IR Break-Beam | Physical acknowledgement |