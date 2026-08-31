# Design Specification — Pick Sequence Engine & Path Optimization

## 1. Overview
The Pick Sequence Engine transforms validated `MatchResult` line items into an ordered, hardware-executable pick queue. It sorts physical bin locations to minimize operator movement and manages sequential state progression from pick initiation to completion.

---

## 2. Path Optimization Algorithm

To maximize retrieval efficiency, picking steps are ordered using a coordinate-based serpentine (S-curve) traversal strategy across the physical bin matrix:

1. **Primary Sort (Row Coordinates):** Group target bins by vertical row (`coordinate_y`).
2. **Secondary Sort (Column Traversal):** 
   * Even rows (`Y = 0, 2, 4...`): Sort horizontal columns (`coordinate_x`) in ascending order (Left-to-Right).
   * Odd rows (`Y = 1, 3, 5...`): Sort horizontal columns (`coordinate_x`) in descending order (Right-to-Left).

This eliminates unnecessary backtracking across bin racks during multi-component assembly picks.

---

## 3. Pick Step State Machine

Each individual pick step advances through a strict 4-stage lifecycle:

```text
+------------------+
|      PENDING     |  (Step queued; bin LED off)
+------------------+
         |
         v
+------------------+
|      ACTIVE      |  (Host sends SET_LED; bin LED pulses GREEN)
+------------------+
         |
         v
+------------------+
|    CONFIRMED     |  (Operator presses button; MCU transmits ACK)
+------------------+
         |
         v
+------------------+
|    COMPLETED     |  (Inventory deducted; queue advances to next step)
+------------------+

```

## 4. Hardware Command Packet Payload
When a pick step transitions to ACTIVE, the Host Serial Engine dispatches a formatted packet to the microcontroller:

Packet Field,Type,Description
Header,String,"Standard command delimiter (""CMD:PICK_STEP"")"
Bin ID,String,"Physical bin identifier (e.g., ""BIN-A-01"")"
Target LED Index,Integer,Hardware index on addressable LED bus
Color Code,Hex / RGB,"Active color state (""0x00FF00"" for Green)"
Quantity Required,Integer,Component count displayed to operator


## 5. Sequence Execution Flow Example
```python
from dataclasses import dataclass

@dataclass
class PickStep:
    step_id: int
    bin_id: str
    part_number: str
    quantity: int
    led_index: int
    status: str = "PENDING"  # PENDING -> ACTIVE -> CONFIRMED -> COMPLETED

```
