import bluetooth


class Polaroid():
    def __init__(self):
        self.addr, self.name = find_device('Polaroid')




def find_device(name, duration=2):
    # find device
    nearby = bluetooth.discover_devices(lookup_names=True,
                                        duration=duration)
    for addr, dev_name in nearby:
        if name in dev_name:
            print("found module", addr, dev_name)
            return (addr, dev_name)
    raise Exception("Can't find device with name {}".format(name))


