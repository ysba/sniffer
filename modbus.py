def modbus_parser(data):
    print("modbus", "".join("%02x " % x for x in data))
