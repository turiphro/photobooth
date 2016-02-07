#!/usr/bin/env python
# Run with Python 2
# Script borrowed from @jonathanlking
# https://github.com/jonathanlking/Instagram-Printer-RP/blob/master/setup.py

import sys
import os
import bluetooth
import subprocess

print "Searching for devices..."

# Scan for nearby bluetooth devices
nearbyDevices = bluetooth.discover_devices()

if len(nearbyDevices) == 0:
    print "No bluetooth devices detected, please turn on and run this script again"
    sys.exit()

printerAddress = ''
printerName = ''

for bluetoothDeviceAddress in nearbyDevices:
    deviceName = bluetooth.lookup_name(bluetoothDeviceAddress)
    print "Found bluetooth device with address", bluetoothDeviceAddress, "called", deviceName
    if "Polaroid" in deviceName:
        printerAddress = bluetoothDeviceAddress
        printerName = deviceName

if not len(printerAddress) == 0:
    print "Polaroid Pogo printer detected..."
else:
    print "No printer detected, please turn on and run this script again"
    sys.exit()

# Save the address of the Polaroid Pogo so that it can be easily accessed later when trying to print
with open('settings.txt','w') as file:
    file.write(printerAddress + '\n')
    file.write('# Address for device: ' + printerName + '\n')

# Get the mac address of the bluetooth adaptor
hostDeviceAddress = ''

cmd = subprocess.Popen('hciconfig hci0', shell=True, stdout=subprocess.PIPE)
for line in cmd.stdout:
    if "BD Address" in line:
        data = line.split()
        for field in data:
            if len(field) == len('XX:XX:XX:XX:XX:XX'):
                hostDeviceAddress = field
                
if len(hostDeviceAddress) == 0:
    print "Something went wrong trying to determine the address of you bluetooth adaptor, are you sure it is plugged in and working?"
    sys.exit()

pathToBluetoothPincodeSettings = '/var/lib/bluetooth/' + hostDeviceAddress

if not os.path.exists(pathToBluetoothPincodeSettings):
    os.makedirs(pathToBluetoothPincodeSettings)

# Create the pincodes file, all Polaroid Pogo's have a pin of 6000
settingsFilePath = pathToBluetoothPincodeSettings + '/pincodes'

try:
    with open(settingsFilePath,'a') as file:
        file.write(printerAddress)
        file.write(' 6000\n')
except IOError:
    print "Unable to write file, maybe you did not run as sudo?"
else:
    print "Setup complete."
