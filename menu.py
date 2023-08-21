from arduino_func import connect, read_socket, send_data, measure_voltage


def main_menu(serial_ports_list):
    message = f"Choose serial port:\n"
    for i, port in enumerate(serial_ports_list):
        message += f"{i + 1} - {port}"
    message += "\n: "
    port_index = input(message)
    try:
        port_index = int(port_index)
    except (ValueError, TypeError):
        print("Wrong input port number\n")
        main_menu(serial_ports_list)
    else:
        if len(serial_ports_list) >= port_index:
            port = serial_ports_list[port_index - 1]
            arduino = connect(port)
            work_type_menu(arduino)
        else:
            print("Wrong input port number\n")
            main_menu(serial_ports_list)


def read_socket_dialog(ard):
    seconds = input("Write how many seconds the socket should listen(0 = infinity): ")
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        print("Wrong seconds input\n")
        read_socket_dialog(ard)
    else:
        read_socket(ard, seconds)
        work_type_menu(ard)


def voltage_measuring_dialog(ard):
    nplc_modes = (1, 5, 10)
    nplc = input("Write NPLC value(1 or 5 or 10): ")
    try:
        nplc = int(nplc)
    except (ValueError, TypeError):
        print("Wrong NPLC input\n")
        voltage_measuring_dialog(ard)
    else:
        if nplc in nplc_modes:
            voltage_measuring_v_max_input_dialog(ard, nplc)
        else:
            print("Wrong NPLC input\n")
            voltage_measuring_dialog(ard)


def voltage_measuring_v_max_input_dialog(ard, nplc):
    v_max_input = input("Write max voltage input(example: 3.3): ")
    try:
        v_max_input = float(v_max_input)
    except (ValueError, TypeError):
        print("Wrong max input voltage\n")
        voltage_measuring_v_max_input_dialog(ard, nplc)
    else:
        print("Tap 'q' for end measuring\n----------------------\n")
        try:
            measure_voltage(ard, nplc, v_max_input)
        except KeyboardInterrupt:
            send_data(ard, 1)
            work_type_menu(ard)


def work_type_menu(ard):
    message = f"Choose work type:\n" \
             f"1. Read socket\n" \
             f"2. Voltage measuring\n"
    message += ': '
    work_type = input(message)
    try:
        work_type = int(work_type)
    except (ValueError, TypeError):
        print("Wrong input type\n")
        work_type_menu(ard)
    else:
        match work_type:
            case 1:
                read_socket_dialog(ard)
            case 2:
                voltage_measuring_dialog(ard)
            case _:
                print("Wrong input type\n")
                work_type_menu(ard)
