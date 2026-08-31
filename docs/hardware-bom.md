# Hardware Bill of Materials & Pinout Specification

## 1. Required Hardware Components

| Item | Component Description | Qty | Specifications / Notes |
| :--- | :--- | :--- | :--- |
| **MCU** | ESP32 Development Board | 1 | 30-pin or 38-pin version (USB-C / Micro-USB) |
| **LED Indicators** | WS2812B Addressable RGB LED Strip | 1 | 5V, 60 LEDs/m (cut to bin count) |
| **Input Buttons** | Tactile Push Buttons (Normally Open) | N | 1 per bin for pick confirmation |
| **Resistors** | 470? Resistor | 1 | Inline on LED Data Line (protects first pixel) |
| **Resistors** | 10k? Resistors | N | External pull-ups for buttons (if not using internal) |
| **Capacitor** | 1000?F 16V Electrolytic Capacitor | 1 | Placed across 5V/GND power rails |
| **Power Supply** | 5V 3A DC Power Adapter | 1 | External power supply for WS2812B LED array |
| **Level Shifter** | 74AHCT125 / Logic Converter | 1 | Optional: Converts ESP32 3.3V logic to 5V LED data |

---

## 2. ESP32 Pin Allocation Matrix

| ESP32 GPIO Pin | Function | Target Hardware Connection | Signal Logic |
| :--- | :--- | :--- | :--- |
| **GPIO 18** | LED Data Output | WS2812B Data In (via 470? resistor) | Digital 3.3V / 5V |
| **GPIO 4** | Pick Confirm Button | Tactile Switch Terminal 1 | Active LOW (Pull-up) |
| **5V / VIN** | Main Power Rail | External 5V Power Source | 5V DC |
| **GND** | System Common Ground | Common Ground (MCU + LEDs + PSU) | 0V |

---

## 3. Power Consumption Calculations

* **Peak LED Current Draw:** `16 LEDs * 60mA (Full White) = 960mA`
* **Idle MCU Current Draw:** `~80mA - 150mA`
* **Recommended PSU Headroom:** `5V / 2A minimum` (prevents brownouts during full LED illuminate cycles).
