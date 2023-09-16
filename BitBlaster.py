import sys
import subprocess
import serial
import serial.tools.list_ports
from time import sleep

def main():
    runModes = {
        '--list': listAvailableCOMPorts,
        '--upload': uploadFirmware,
        '--help': printHelp }
    if len(sys.argv) < 2:
        printHelp()
        sys.exit(1)
    mode = sys.argv[1]
    if mode not in runModes:
        print('unrecognized command: ' + mode)
        printHelp()
        sys.exit(1)
    runModes[mode]()

def printHelp():
    print('usage: python FWuploader.py [option] [COM port]')
    print('options:')
    print('\t--list\t\tto list available COM ports')
    print('\t--upload\tto upload firmware to an Arduino')
    print('\t--help\t\tto print this help message')
    sys.exit(0)

def listAvailableCOMPorts():
    # open and close serial port at 1200 baud. This resets the Arduino Leonardo
    print('')
    ports = getAvailableCOMPorts()
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
    sys.exit(0)

def uploadFirmware():
    if len(sys.argv) < 3:
        print('missing COM port argument')
        sys.exit(1)
    print('')
    print('uploading firmware to Arduino Leonardo')
    print('')
    portOfArduino = sys.argv[2]
    if not isInputPortAvailable(portOfArduino):
        print('Could not find port: ' + portOfArduino)
        sys.exit(1)
    availablePortsBeforeInit = getAvailableCOMPorts()
    triggerLeonardoBootloader(portOfArduino)
    newPort = searchForNewPort(availablePortsBeforeInit)
    if newPort is None:
        print('could not find new port')
        sys.exit(1)
    print('found new port: ' + str(newPort))
    runAVRDude(newPort.device)
    sys.exit(0)

def runAVRDude(uploadPort):
    programCommand = ['avrdude\\avrdude.exe',
    '-Cavrdude\\avrdude.conf',
     '-F' ,
     '-patmega32u4',
     '-cavr109',
     '-b57600',
     '-P' + uploadPort,
     '-Uflash:w:firmware.hex:i']
    print('')
    print('start uploading firmware...')
    cmd = subprocess.Popen(programCommand, stdout=subprocess.PIPE, shell=True)
    for line in cmd.stdout.readlines():
        print('\033[91m' + line + '\033[0m')
        sys.stdout.flush()

def isInputPortAvailable(COMport):
    print('getting list of available COM ports')
    availablePorts = getAvailableCOMPorts()
    for port in availablePorts:
        if COMport in port.device:
            return True
    return False

def triggerLeonardoBootloader(COMPort):
    print('opening port at 1200 baud to reset Arduino Leonardo...')
    try:
        ser = serial.Serial(COMPort, 1200)
    except serial.SerialException as e:
        print('Error opening serial port:', e)
        exit(1)
    ser.close()
    sleep(4)  # give the bootloader time to start up

def searchForNewPort(previousPorts):
    print('getting list of available COM ports')
    availablePorts = getAvailableCOMPorts()
    print('searching for new port...')
    newPort = None
    for port in availablePorts:
        if port not in previousPorts:
            newPort = port
            break
    return newPort

def getAvailableCOMPorts():
    availablePorts = serial.tools.list_ports.comports()
    return availablePorts

if __name__ == '__main__':
    main()
