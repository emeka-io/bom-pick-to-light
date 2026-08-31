# Design Specification — Inventory Model & Persistence

## 1. Overview
The Inventory Subsystem tracks physical component storage locations, available stock quantities, and physical grid coordinates required for visual route optimization. It acts as the single source of truth for stock availability during BOM matching and post-pick reconciliation.

---

## 2. Entity Schema & Field Definitions

### 2.1 Bin Model Schema

| Field Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **bin_id** | String | Primary Key, Unique | Unique physical bin identifier (e.g., `BIN-A-01`) |
| **part_number** | String | Indexed | Internal component MPN or standard part identifier |
| **quantity_on_hand**| Integer | Non-Negative (>= 0) | Active count of physical components present in bin |
| **unit_of_measure** | String | Default: `"PCS"` | Standard unit designation (`PCS`, `METERS`, etc.) |
| **coordinate_x** | Integer | Non-Negative | Physical horizontal grid index (Column 1..N) |
| **coordinate_y** | Integer | Non-Negative | Physical vertical grid index (Row 1..N) |

---

## 3. Stock Transaction & State Logic

When a pick sequence is executed, the `InventoryStore` processes stock adjustments according to the following state lifecycle:

```text
  [ BOM Request ]
         |
         v
  < Stock >= Qty? > --- NO ---> [ Flag Deficit Warning ] ---> [ Halt / Partial Pick ]
         |
        YES
         |
         v
  [ Reserve Stock ]
         |
         v
  [ Physical Pick Confirmed ]
         |
         v
  [ Deduct Stock: quantity_on_hand -= qty ]
         |
         v
  [ Append Audit Log Entry ]

```


## 4. File Persistence Format (JSON / CSV)
The inventory is stored locally in data/example-inventory/example-inventory.csv for development and testing:

```text
bin_id,part_number,quantity_on_hand,unit_of_measure,coordinate_x,coordinate_y
BIN-A-01,RES-10K-0805,150,PCS,1,1
BIN-A-02,CAP-100NF-0603,200,PCS,1,2
BIN-B-01,MCU-ESP32-WROOM,12,PCS,2,1
BIN-B-02,LED-WS2812B-5050,45,PCS,2,2

```
