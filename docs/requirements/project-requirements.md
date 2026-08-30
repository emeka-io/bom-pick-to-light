# Project Requirements — BOM Pick-to-Light System

## 1. Executive Overview
The **BOM-Synced Pick-to-Light System** bridges physical inventory management with automated hardware retrieval. The system ingests electronic/mechanical Bills of Materials (BOMs), matches required part numbers against live bin stock, generates an optimized visual picking sequence, drives dynamic bin LEDs via microcontroller firmware, and updates inventory levels upon pick completion.

---

## 2. Functional Requirements

### 2.1 BOM Ingestion & Parsing
* **File Formats:** Support ingestion of CSV and JSON BOM files (exported from CAD/EDA tools like KiCad, Altium, or Onshape).
* **Field Mapping:** Extract critical fields including `Part Number`, `Designator` (e.g., C1, R3), `Quantity Required`, and `Description`.
* **Validation:** Flag missing part numbers, negative quantities, or malformed data structures before processing.

### 2.2 Inventory & Stock Matching
* **Mapping Engine:** Map BOM line items to specific bin IDs (e.g., Bin `A-12`) based on internal Part Number lookups.
* **Stock Verification:** Check current available stock against required quantities.
* **Error Handling:** Generate structured warnings for:
  * **Unmapped Parts:** Components in the BOM not found in the bin inventory model.
  * **Insufficient Stock:** Components with required quantities exceeding available bin counts.

### 2.3 Pick Queue & Sequencing
* **Sequence Generation:** Convert validated BOM requests into an ordered queue of individual pick actions.
* **Optimization:** Sort pick sequences by physical bin layout coordinates to minimize operator retrieval paths.
* **State Management:** Track active pick status (`Pending`, `Active`, `Completed`, `Bypassed`).

### 2.4 Firmware & Hardware Feedback
* **Visual Indication:** Trigger target bin LEDs (solid, pulse, or color-coded by pick status) via serial/network commands.
* **Pick Acknowledgment:** Support manual pick verification (tactile button press, optical sensor break, or software confirmation).
* **Multi-Bin Handling:** Advance automatically to the next sequential bin upon successful pick confirmation.

---

## 3. Technical & System Constraints

* **Host Software Environment:** Built using Python 3.10+ targeting Linux/WSL2 deployment environments.
* **Firmware Platform:** Embedded C++ compiled via PlatformIO targeting ESP32 microcontrollers.
* **Communication Protocol:** Lightweight serial protocol (UART over USB) or local WebSocket messaging for Host-to-MCU messaging.
* **Modular CAD Integration:** CAD/STL artifacts exportable from Onshape models for 3D-printed modular bin assemblies.

---

## 4. Verification & Testing Criteria

* **Unit Tests:** Achieve 100% test coverage on BOM parsing logic, CSV ingestion edge cases, and stock consumption logic.
* **Simulator Integration:** Run complete pick sequences via host-side software simulation prior to physical hardware interface deployment.