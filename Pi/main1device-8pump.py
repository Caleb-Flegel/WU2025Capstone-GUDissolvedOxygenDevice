import serial 
from time import sleep

if __name__ == '__main__':
    # Main Arduino device
    dev0 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    dev0.reset_input_buffer()

    # Dummy target vars that will be determined by hub Pi
    #   DO error tolerance
    tol = 5
    #   Selected DO probe
    selProbe = 0
    nextProbe = 0
    #   Time to wait between enabling agitation pump and sending data
    agitationTimeout = 15

    # Pump control vector
    #   All pumps are AGITATION pumps (provides water flow for accurate DO readings)
    devEnabled = [False * 8]

    # Dissolved oxygen measurement reading storage
    dev0Reading = ""

    
    while True:
        # Check to see if a new probe has been selected via the hub Pi
        #*Assign new nextProbe from hub arduino commands*
        if (nextProbe != selProbe):
            # Send new probe to Arduino; pump switching will happen on Arduino
            writeStr = f'next-{nextProbe}'
            dev0.write(writeStr.encode())

            # Overwrite stored probe
            selProbe = nextProbe

            # Wait for requested time
            sleep(agitationTimeout)

        # A new probe has not been selected, get the reading from the Arduino/current probe
        if (dev0.in_waiting > 0):
            dev0Reading = dev0.readline().decode('utf-8').rstrip()
            print("Device 0, probe " + selProbe + " reading: " + dev0Reading)
            # Send reading to hub Pi

        sleep(1)

        # TODO: Add calibration passthrough