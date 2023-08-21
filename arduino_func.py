import time

import keyboard
import serial


def connect(com_port):
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.timeout = .1
    ser.port = com_port
    ser.open()
    send_data(ser, 1)

    print(f"Is open {ser.name}:  {ser.is_open}")
    return ser


def get_condition(start, seconds):
    if seconds <= 0:
        condition = True
    else:
        condition = round(time.time()) <= start + seconds
    return condition


def read_socket(ard, seconds=10):
    start = round(time.time())
    print(f"Start time: {start}")
    condition = get_condition(start, seconds)

    while condition:
        condition = get_condition(start, seconds)
        result = ard.readline()
        if result:
            try:
                print(f"---------------------------------\n{result.decode('utf-8')}---------------------------------")
            except UnicodeDecodeError:
                print(f"---------------------------------\n{result}---------------------------------")


def measure_voltage(ard, nplc=1, v_max_input=3.3):
    send_data(ard, 2)
    while True:
        summary_voltage = 0.0
        for i in range(0, nplc):
            start_millis = int(round(time.time() * 1000))
            cycle_summary_voltage = 0.0
            cycles_count = 0
            while (start_millis + 20) >= int(round(time.time() * 1000)):
                if keyboard.is_pressed('q'):
                    raise KeyboardInterrupt

                voltage = ard.readline()
                voltage = voltage.decode('utf-8')
                if voltage and voltage.startswith('v='):
                    try:
                        voltage = float(voltage.split('=')[1])
                        voltage = v_max_input if voltage > v_max_input else voltage

                        cycle_summary_voltage += voltage
                        cycles_count += 1
                    except (ValueError,  TypeError):
                        pass

            cycle_voltage = cycle_summary_voltage / cycles_count if cycles_count > 0 else 0.0
            summary_voltage += cycle_voltage
        summary_avg_voltage = summary_voltage / nplc
        print(f"Voltage: {round(summary_avg_voltage, 6)} V")


def send_data(ard, data):
    ard.write(bytes(str(data), 'utf-8'))
    time.sleep(0.05)
    ard.readlines()
