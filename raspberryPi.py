'''(First time PC setup)
    Run in command prompt:  pip install pyrtlsdr[lib]

    Description:
    Samples radio signals, calculates their average power, and transmits 
    data over a serial connection to XBee Transmitter via USB connection
'''

import serial,time,sys
from rtlsdr import RtlSdr
from numpy import *

PORT = 'COM10'  # Change this to your port
BAUD = 9600

sdr = RtlSdr()
sdr.sample_rate = 2.048e6
sdr.center_freq = 165e6
sdr.freq_correction = 60
sdr.gain = 40
ser = serial.Serial(PORT,BAUD,timeout=1)
try:
    for i in range(1000):
        array = []
        for n in range(100):
            samples = sdr.read_samples(1024)
            log = 10*log10(var(samples))
            array = array + [log]
        avg = average(array[0:n])
        # calib_avg = round(-49.4 + 2.33*avg + 0.0822*avg**2+0.00142*avg**3) # Calibrated value
        calib_avg = round(1.05*avg - 54.4)

        message = f"{avg:.2f}"
        calib_msg = f"{calib_avg:.0f}"
        ser.write(calib_msg.encode('utf-8'))
        print(f"Read from SDR: {message}, Sent to XBee: {calib_msg}")
        time.sleep(2)
except KeyboardInterrupt:
    print("User interrupt")
finally:
    # Close hardware cleanly when you're truly done
    try:
        ser.close()
    except Exception:
        pass
    try:
        sdr.close()
    except Exception:
        pass
