# Hardware Architecture — BOM Pick-to-Light System

## 1. System Block Diagram

```text
                  +--------------------------+
                  |    5V / 3A DC Adapter    |
                  +--------------------------+
                        |              |
                (5V Main Power)   (5V LED Power)
                        |              |
                        v              v
+--------------+  USB-CDC  +---------------+    GPIO 18    +------------------------+
|  Host PC     |---------->| ESP32 DevKit  |-------------->| WS2812B LED Array      |
|  (Python)    |<----------| Microcontroller|               | (1 LED per Bin Module) |
+--------------+  (Serial) +---------------+               +------------------------+
                                   |
                             GPIOs 12-15
                               (Inputs)
                                   v
                           +------------------------+
                           | Tactile Switches /     |
                           | IR Optical Break-Beams |
                           +------------------------+

```

Pin Name,Function,Direction,Connected Device,Notes
GPIO 18,LED Data Line,Output,WS2812B Strip DIN,Requires 330Ω series resistor
GPIO 12,Bin 1 Pick Sense,Input,Tactile Switch / IR,Internal pull-up enabled
GPIO 13,Bin 2 Pick Sense,Input,Tactile Switch / IR,Internal pull-up enabled
GPIO 14,Bin 3 Pick Sense,Input,Tactile Switch / IR,Internal pull-up enabled
GPIO 15,Bin 4 Pick Sense,Input,Tactile Switch / IR,Internal pull-up enabled
TXD0 / RXD0,Serial Comms,Bidirectional,Host PC USB-UART,Baud rate: 115200 bps

3. Power Distribution Strategy
- Dual-Rail Considerations: The ESP32 logic operates at 3.3V, while WS2812B LEDs require 5V VCC.

- LED Power Allocation: Each WS2812B RGB LED draws approximately 60mA at full white brightness. Power rails must be sized to support peak current for all active bins simultaneously.

- Bulk Capacitance: A 1000µF, 6.3V electrolytic capacitor is connected across the main 5V and GND rails to smooth out switching current spikes.

4. Mechanical Integration & Housing Interface
- Modular Mounting: Bin modules utilize 3D-printable enclosures designed in Onshape (located in mechanical/cad/).

- Light Diffusion: Acrylic or 3D-printed PLA light diffusers mount over each LED channel (mechanical/cad/diffuser/) for soft visual feedback.

- PCB / Wiring Channels: Wire routing channels are integrated into the rear backplane housing (hardware/wiring/) to prevent line snags during picking operations.