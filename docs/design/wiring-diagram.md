# Design Specification — Electrical Schematic & Wiring Diagram

## 1. Overview
This specification details the point-to-point electrical connections between the ESP32 host microcontroller, power distribution bus, WS2812B LED array, and confirmation pushbuttons.

---

## 2. System Interconnect Diagram

```text
               +--------------------------------------+
               |          5V 2A DC Power Supply       |
               +--------------------------------------+
                 | (+) 5V                      | (-) GND
                 |                             |
                 +---------------+             +---------------+
                 |               |             |               |
                 v               v             v               v
           +-----------+   +-----------+ +-----------+   +-----------+
           | ESP32 VIN |   | LED Strip | | ESP32 GND |   | LED Strip |
           +-----------+   +-----------+ +-----------+   +-----------+
                                                           |
                                                           v
                                                     +-----------+
                                                     | Switch GND|
                                                     +-----------+

  ESP32 GPIO Pin               Hardware Destination
  ================            ======================
  [ GPIO 18 ] ------[470Ω]---> [ WS2812B Data In Pin ]
  [ GPIO 04 ] ----------------> [ Bin 1 Button Signal ] (Internal Pull-Up)

```

## 3. Signal Line Protection
- Data Line Resistor: A 470Ω resistor is placed in series between GPIO 18 and the DIN pad of the first WS2812B LED pixel to prevent impedance mismatches and voltage spikes.

- Power Decoupling: A 1000µF 16V electrolytic capacitor is connected in parallel across the main 5V and GND power supply rails to buffer current spikes during full-brightness RGB illumination cycles.