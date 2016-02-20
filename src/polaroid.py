import bluetooth
import subprocess


class Polaroid():
    def __init__(self):
        self.addr, self.name = find_device('Polaroid')

    def connect(self):
        """Connect to photo-printer"""
        pass # connecting not necessary for blueman (see below)
        #command = "sudo rfcomm bind /dev/rfcomm0 {}".format(self.addr)
        #print(command)
        #subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

    def send_image(self, filename):
        """Send image to photo-printer"""
        # NOTE: might need to try different command line tools
        #       (and change the error check below)
        #command = 'ussp-push /dev/rfcomm0 {} file.png'.format(filename)
        #command = 'bluetooth-sendto --device={} {}'.format(self.addr, filename)
        command = 'blueman-sendto --device={} {}'.format(self.addr, filename)
        print("EXECUTING: {}".format(command))
        sending = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output = sending.stdout.read().decode()
        errors = sending.stderr.read().decode()
        if 'error' in errors.lower()\
                or 'on_transfer_started' not in output.lower():
            raise Exception("Error while sending image over bluetooth: {}".format(errors))


def find_device(name, duration=2):
    """Find bluetooth device given certain name"""
    nearby = bluetooth.discover_devices(lookup_names=True,
                                        duration=duration)
    for addr, dev_name in nearby:
        if name in dev_name:
            print("found module", addr, dev_name)
            return (addr, dev_name)
    raise Exception("Can't find device with name {}".format(name))
