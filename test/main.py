import utime as time
from machine import Pin

from util.bus import SPI, I2C
from util.fast_sampling import FastSampling
from util.has_method import has_method

from src.example import Example


def main():
    # ------------------------------------
    # ------------    SETUP   ------------
    # ------------------------------------
    print('starting...')

    led_internal  = Pin('LED', Pin.OUT, value=1)

    read_interval_ms = 1_000

    sensors = {
        # nome do sensor: nome da classe()
        "example_sensor": Example(SPI(port='nome_da_porta')) # passe como parâmetro a instância do barramento que está conectado à determinada porta
        # ou
        # "example_sensor": Example(I2C(bus=0)) # passe como parâmetro a instância do barramento que está conectado à determinada porta
    }

    def reset(sensor):
        if has_method(sensor, 'reset'):
            sensor.reset()

    # inicialização de cada sensor (se o método setup existe)
    for sensor in sensors.values():
        if has_method(sensor, 'setup'):
            sensor.setup()

    # ------------------------------------
    # ------------    LOOP    ------------
    # ------------------------------------
    while True:
        tA = time.ticks_ms()
        measurements = {}
        errors = []

        for (name, sensor) in sensors.items():
            try:
                result = sensor.read()
                if isinstance(sensor, FastSampling):
                    sensor_measurements, sensor_errors = result
                    for i in sensor_errors:
                        errors.append(err_msg)
                else:
                    sensor_measurements = result
            except Exception as e:
                err_msg = f'got error `{type(e).__name__}: {e}` while sampling sensor `{name}`'
                errors.append(err_msg)
                reset(sensor)
                continue

            for (metric, value) in sensor_measurements.items():
                measurements[f'{name}/{metric}'] = value

        pkt = { 'measurements': measurements, 'errors': errors }
        # ao adicionar o protocolo de comunicação, os dados devem ser transmitidos nessa linha!
        print(pkt)

        led_internal.toggle()
        time.sleep_ms(read_interval_ms - (time.ticks_ms() - tA))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        FastSampling.stop_thread()
        print(f'got error `{type(e).__name__}: {e}` on main')
