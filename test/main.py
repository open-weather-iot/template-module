from machine import Pin
from ..src.example import Example

# ---------------------------------------
# ------------- SETUP    ----------------
# ---------------------------------------

# PORTS CONFIGURATION
led_internal = Pin(25, Pin.OUT)

# READ_INTERVAL (ms) 
interval = 1000

# SENSORS MAPPING
sensors = {
  # nome do sensor: nome da classe()
  "example_sensor": Example() # passe como parâmetros os pinos que deverão ser conectados
}

# ---------------------------------------
# -------------   LOOP   ----------------
# ---------------------------------------

def main():
  led_internal.value(1)

  while True:
    read_map = { name: sensor.read() for (name, sensor) in sensors.items() }
    print(read_map)

    led_internal.toggle() #internal led toggle
    time.sleep_ms(interval)

if __name__ == "__main__":
  main()
