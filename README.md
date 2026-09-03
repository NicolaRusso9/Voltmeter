**Four‑Digit 7‑Segment ADC Voltmeter (MicroPython)**


---
This project implements a **four‑digit multiplexed 7‑segment voltmeter** using **MicroPython** on a Raspberry Pi Pico.  
The system reads an analog voltage through the ADC, samples it when a button interrupt is triggered, and displays the measured value (0.000–9.999 V) on a multiplexed LED display.

A full online simulation is available on Wokwi:

👉 **[https://wokwi.com/projects/473345211724837889](https://wokwi.com/projects/473345211724837889)**

---

## **Features**
- **Interrupt‑driven ADC sampling** with software debounce  
- **16‑sample averaging** for stable voltage readings  
- **High‑frequency multiplexing** using a periodic hardware timer  
- **Dynamic decimal‑point control**  
- **Segment map for digits 0–9**  
- **Self‑test mode** for verifying digit wiring  
- Clean, modular MicroPython code

---

## **Hardware Setup**
### **Components**
- Raspberry Pi Pico  
- 4‑digit 7‑segment display (common anode or common cathode depending on wiring)  
- Push button (with pull‑up)  
- Slide potentiometer or analog sensor  
- Jumper wires  

### **Pin Mapping**
#### **Segment Pins**
| Segment | GPIO |
|--------|------|
| A | GP0 |
| B | GP1 |
| C | GP2 |
| D | GP3 |
| E | GP4 |
| F | GP5 |
| G | GP6 |
| DP | GP7 |

#### **Digit Select Pins**
| Digit | GPIO |
|-------|------|
| D0 | GP11 |
| D1 | GP10 |
| D2 | GP9 |
| D3 | GP8 |

#### **Inputs**
| Function | GPIO |
|----------|------|
| Button (IRQ) | GP16 |
| ADC Input | GP26 (ADC0) |

---

## **How It Works**
### **1. ADC Sampling**
When the button is pressed, an interrupt triggers the `read_analogue_voltage()` function.  
The ADC is sampled 16 times with micro‑delays to reduce noise.  
The raw value (0–65535) is converted to a voltage using the 3.3 V reference.

### **2. Multiplexed Display**
A hardware timer refreshes the display every 2 ms.  
Each digit is activated sequentially, while the corresponding segments are set according to the digit map.

### **3. Decimal Formatting**
The voltage is scaled to four digits:

```
v = 3.141 → display: 3 . 1 4 1
```

The decimal point is enabled only on the first digit.

---

## **Running the Project**
Upload the script to your Raspberry Pi Pico using Thonny or rshell.

Then simply run:

```python
python main.py
```

Press the button to sample the current analog voltage.

---

## **Wokwi Simulation**
You can test the project online without hardware:

🔗 **[https://wokwi.com/projects/473345211724837889](https://wokwi.com/projects/473345211724837889)**

The simulation includes:
- Pico  
- 7‑segment display  
- Button  
- Potentiometer  

---

## **Project Structure**
```
/project
│── main.py        # Main application logic
│── README.md      # Documentation
```

---

## **Possible Extensions**
- Add **auto‑refresh ADC sampling** without button  
- Implement **low‑pass filtering**  
- Add **brightness control via PWM**  
- Replace the display with an **I²C LCD**  
- Log readings to **UART** or **USB serial**

Guided Links utili:  
- ADC filtering  
- PWM brightness  
- I2C LCD

---

## **License**
MIT License — feel free to modify and extend.

---
