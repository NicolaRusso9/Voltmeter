import machine
import time

#######################################
# Pin and constant definitions
#######################################
SEG_PINS = {
    "A": machine.Pin(0, machine.Pin.OUT),
    "B": machine.Pin(1, machine.Pin.OUT),
    "C": machine.Pin(2, machine.Pin.OUT),
    "D": machine.Pin(3, machine.Pin.OUT),
    "E": machine.Pin(4, machine.Pin.OUT),
    "F": machine.Pin(5, machine.Pin.OUT),
    "G": machine.Pin(6, machine.Pin.OUT),
    "DP": machine.Pin(7, machine.Pin.OUT),
}

DIGIT_PINS = [
    machine.Pin(11, machine.Pin.OUT),   # Digit 0 
    machine.Pin(10, machine.Pin.OUT),   # Digit 1
    machine.Pin(9, machine.Pin.OUT),  # Digit 2
    machine.Pin(8, machine.Pin.OUT),  # Digit 3 
]

# Button pin (interrupt) ==> GP16
BUTTON_PIN = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

# ADC pin (slide potentiometer by default) ==> GP26 (ADC0)
ADC_PIN = machine.ADC(26)

# Timer for display scanning
display_timer = machine.Timer()

# Debounce
DEBOUNCE_MS = 200

#######################################
# Global variables
#######################################
display_value = 0.0          # voltage in 0..3.3
_current_digit = 0           # index 0..3
_last_button_time = 0        # ms

#######################################
# Digit to segment map (0-9)
#######################################
DIGIT_SEGMENTS = {
    0: {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1, "F": 1, "G": 0},
    1: {"A": 0, "B": 1, "C": 1, "D": 0, "E": 0, "F": 0, "G": 0},
    2: {"A": 1, "B": 1, "C": 0, "D": 1, "E": 1, "F": 0, "G": 1},
    3: {"A": 1, "B": 1, "C": 1, "D": 1, "E": 0, "F": 0, "G": 1},
    4: {"A": 0, "B": 1, "C": 1, "D": 0, "E": 0, "F": 1, "G": 1},
    5: {"A": 1, "B": 0, "C": 1, "D": 1, "E": 0, "F": 1, "G": 1},
    6: {"A": 1, "B": 0, "C": 1, "D": 1, "E": 1, "F": 1, "G": 1},
    7: {"A": 1, "B": 1, "C": 1, "D": 0, "E": 0, "F": 0, "G": 0},
    8: {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1, "F": 1, "G": 1},
    9: {"A": 1, "B": 1, "C": 1, "D": 1, "E": 0, "F": 1, "G": 1},
}

_current_digit = 0
display_value = 0.0

#######################################
# Function definitions
#######################################
def read_analogue_voltage(pin):
    global display_value, _last_button_time

    now = time.ticks_ms()
    if time.ticks_diff(now, _last_button_time) < DEBOUNCE_MS:
        return
    _last_button_time = now

    samples = 16
    acc = 0
    for _ in range(samples):
        acc += ADC_PIN.read_u16()
        time.sleep_us(200)

    avg_raw = acc / samples
    voltage = (avg_raw / 65535.0) * 3.3
    display_value = voltage

    print("Button IRQ: avg_raw =", avg_raw, "voltage =", voltage)

def disable_display_timer():
    display_timer.deinit()

def enable_display_timer():
    display_timer.init(period=2, mode=machine.Timer.PERIODIC, callback=scan_display)

def scan_display(timer_int):
    global _current_digit, display_value

    v = display_value
    if v < 0:
        v = 0.0
    if v > 9.999:
        v = 9.999

    n = int(round(v * 1000))  # Ex. 2.690 -> 2690
    digits = [
        (n // 1000) % 10,  # DIG_1 (Cifra 0)
        (n // 100) % 10,   # DIG_2 (Cifra 1)
        (n // 10) % 10,    # DIG_3 (Cifra 2)
        n % 10,            # DIG_4 (Cifra 3)
    ]

    # Dot must be appear only for first number
    dp_enable = (_current_digit == 0)

    display_digit(digits[_current_digit], _current_digit, dp_enable)

    _current_digit = (_current_digit + 1) % 4


def display_digit(digit_value, digit_index, dp_enable=False):
    # All off
    for d in DIGIT_PINS:
        d.value(0)

    segs = DIGIT_SEGMENTS.get(digit_value, DIGIT_SEGMENTS[0])
    for name, pin in SEG_PINS.items():
        if name == "DP":
            # Only if dp_enable == True
            pin.value(0 if dp_enable else 1)
        else:
            pin.value(0 if segs[name] == 1 else 1)
    DIGIT_PINS[digit_index].value(1)

def display_value_test():
    print("Running display_value_test...")
    disable_display_timer()

    test_digits = [1, 2, 3, 4]
    for i in range(4):
        for d in DIGIT_PINS:
            d.value(0)
        for s in SEG_PINS.values():
            s.value(0)

        display_digit(test_digits[i], i, dp_enable=False)
        print("Test digit", i, "->", test_digits[i])
        time.sleep(0.7)

    for d in DIGIT_PINS:
        d.value(0)
    for s in SEG_PINS.values():
        s.value(0)

    print("display_value_test done.")
    enable_display_timer()

def setup():
    for d in DIGIT_PINS:
        d.value(0)
    for s in SEG_PINS.values():
        s.value(0)

    enable_display_timer()

    BUTTON_PIN.irq(trigger=machine.Pin.IRQ_FALLING, handler=read_analogue_voltage)
    print("Setup completed. Press button to sample analogue voltage.")


if __name__ == '__main__':
    setup()
    # display_value_test()
    while True:
        time.sleep(1)
