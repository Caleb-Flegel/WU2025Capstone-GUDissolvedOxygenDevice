import serial 
from time import sleep

led = LED(17)

if __name__ == '__main__':
    # TODO: verify the '/dev/ttyUSBx' system is consistent with more Arduinos... so far have only tested with one device
    # Arduino device 0
    dev0 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    dev0.reset_input_buffer()

    # Arduino device 1
    dev1 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
    dev1.reset_input_buffer()

    # Arduino device 2
    dev2 = serial.Serial('/dev/ttyUSB2', 9600, timeout=1)
    dev2.reset_input_buffer()

    # Arduino device 3
    dev3 = serial.Serial('/dev/ttyUSB3', 9600, timeout=1)
    dev3.reset_input_buffer()

    # Dummy target vars that will be determined by hub Pi
    #   Device targets
    dev0Target = 78
    dev1Target = 92
    dev2Target = 85
    dev3Target = 67
    #   DO error tolerance
    tol = 5

    # Pump control vars
    #   Pump 0s are the AGITATION pump (provides water flow for accurate DO readings)
    #   Pump 1s are the AERATION pump  (aerates the water)
    dev0Pump0Enabled = False
    dev0Pump1Enabled = False

    dev1Pump0Enabled = False
    dev1Pump1Enabled = False

    dev2Pump0Enabled = False
    dev2Pump1Enabled = False

    dev3Pump0Enabled = False
    dev3Pump1Enabled = False

    # Dissolved oxygen measurement reading storage
    dev0Reading = ""
    dev1Reading = ""
    dev2Reading = ""
    dev3Reading = ""

    # Turn on agitation pumps
    #   Arduino 0
    print("Turn on Arduino 0 agitation pump")
    dev0.write(b'EnablePump-0')
    #   Arduino 1
    print("Turn on Arduino 1 agitation pump")
    dev1.write(b'EnablePump-0')
    #   Arduino 2
    print("Turn on Arduino 2 agitation pump")
    dev2.write(b'EnablePump-0')
    #   Arduino 3
    print("Turn on Arduino 3 agitation pump")
    dev3.write(b'EnablePump-0')

    while True:
        # Get DO measurements from devices
        #   TODO: find way to ping devices to see if they are connected
        #   Arduino 0
        if (dev0.in_waiting > 0):
            dev0Reading = dev0.readline().decode('utf-8').rstrip()
            print("Device 0: " + dev0Reading)
            # Send reading to hub Pi

        #   Arduino 1
        if (dev1.in_waiting > 0):
            dev1Reading = dev1.readline().decode('utf-8').rstrip()
            print("Device 1: " + dev1Reading)
            # Send reading to hub Pi

        #   Arduino 2
        if (dev2.in_waiting > 0):
            dev2Reading = dev2.readline().decode('utf-8').rstrip()
            print("Device 2: " + dev2Reading)
            # Send reading to hub Pi

        #   Arduino 3
        if (dev3.in_waiting > 0):
            dev3Reading = dev3.readline().decode('utf-8').rstrip()
            print("Device 3: " + dev3Reading)
            # Send reading to hub Pi


        # Control Arduino motors

        # Arduino 0
        #   First make sure the passed in value is a numeric
        #   Then see if the passed value has a larger error than tolerance
        if (dev0Reading.isnumeric() and float(dev0Reading) < (dev0Target - tol)):
            # Check to see if the pump hasn't already been turned on
            if (not dev0Pump1Enabled):
                # Pump needs to be turned on
                print("Turn on dev 0 aeration pump")
                dev0.write(b'EnablePump-1')

                # Modify pump state
                dev0Pump1Enabled = True
            # Nothing needs to be done
        else:
            # Check to see if pump needs to be turned off
            if (dev0Pump1Enabled):
                # Pump needs to be turned on
                print("Turn off dev 0 aeration pump")
                dev0.write(b'DisablePump-1')

                # Modify pump state
                dev0Pump1Enabled = False
            # Nothing needs to be done

        # Arduino 1
        if (dev1Reading.isnumeric() and float(dev1Reading) < (dev1Target - tol)):
            # Check to see if the pump hasn't already been turned on
            if (not dev1Pump1Enabled):
                # Pump needs to be turned on
                print("Turn on dev 1 aeration pump")
                dev1.write(b'EnablePump-1')

                # Modify pump state
                dev1Pump1Enabled = True
            # Nothing needs to be done
        else:
            # Check to see if pump needs to be turned off
            if (dev1Pump1Enabled):
                # Pump needs to be turned on
                print("Turn off dev 1 aeration pump")
                dev1.write(b'DisablePump-1')

                # Modify pump state
                dev1Pump1Enabled = False
            # Nothing needs to be done
        
        # Arduino 2
        if (dev2Reading.isnumeric() and float(dev2Reading) < (dev2Target - tol)):
            # Check to see if the pump hasn't already been turned on
            if (not dev2Pump1Enabled):
                # Pump needs to be turned on
                print("Turn on dev 2 aeration pump")
                dev2.write(b'EnablePump-1')

                # Modify pump state
                dev2Pump1Enabled = True
            # Nothing needs to be done
        else:
            # Check to see if pump needs to be turned off
            if (dev2Pump1Enabled):
                # Pump needs to be turned on
                print("Turn off dev 2 aeration pump")
                dev2.write(b'DisablePump-1')

                # Modify pump state
                dev2Pump1Enabled = False
            # Nothing needs to be done
        
        # Arduino 3
        if (dev3Reading.isnumeric() and float(dev3Reading) < (dev3Target - tol)):
            # Check to see if the pump hasn't already been turned on
            if (not dev3Pump1Enabled):
                # Pump needs to be turned on
                print("Turn on dev 3 aeration pump")
                dev3.write(b'EnablePump-1')

                # Modify pump state
                dev3Pump1Enabled = True
            # Nothing needs to be done
        else:
            # Check to see if pump needs to be turned off
            if (dev3Pump1Enabled):
                # Pump needs to be turned on
                print("Turn off dev 3 aeration pump")
                dev3.write(b'DisablePump-1')

                # Modify pump state
                dev3Pump1Enabled = False
            # Nothing needs to be done
            

        # TODO: Add calibration passthrough