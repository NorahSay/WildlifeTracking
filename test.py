import serial
import time

# Change this to your port:
# Windows example: 'COM3'
# Linux/Mac example: '/dev/ttyUSB0' or '/dev/cu.usbserial-XXXX'
PORT = 'COM10'
BAUD = 9600

ser = serial.Serial(
        PORT,
        BAUD,
        timeout=1,
        write_timeout=1,
        rtscts=False,
        dsrdtr=False,
        xonxoff=False)
time.sleep(0.5)  # allow some time for the port to open


ser.write(b"Hello from laptop!\r\n")
print("✅ Message sent to XBee")

ser.write(b'+++')
time.sleep(1)  # wait for guard time
print("CM:",ser.readline().decode().strip())  # should be "OK"

for cmd in (b'ATID\r',  # Network ID
            b'ATMY\r',  # My address 
            b'ATBD\r',  # Baud rate
            b'ATDL\r',  # Destination low address
            b'ATDH\r',  # Destination high address
            b'ATWR\r',  # Write config to non-volatile memory
            b'ATCN\r'): # Exit command mode
    ser.write(cmd)
    time.sleep(0.5)
    response = ser.read(64)
    print(f"{cmd.strip().decode()}: {response.decode().strip()}")

# Optional: read reply (if another XBee is sending back)
response = ser.read(100)
if response:
    print("Received:", response.decode(errors='ignore'))
else:
    print("No response (normal if remote XBee isn't replying).")

ser.close()

# try:
#     print(f"Trying {PORT} @ {BAUD}...")
#     ser = serial.Serial(
#         PORT,
#         BAUD,
#         timeout=1,
#         write_timeout=1,
#         rtscts=False,
#         dsrdtr=False,
#         xonxoff=False)
    
#     # Ensure DTR/RTS are low to avoid resetting the XBee
#     ser.setDTR(False)
#     ser.setRTS(False)
#     time.sleep(0.5)  # allow some time for the port to open

#     # Try entering command mode
#     ser.write(b"+++")
#     time.sleep(1)
#     print(ser.read(16))
#     ser.close()

#     # ser.write(b"Hello from Raspberry Pi!\r\n")
#     # print("Message sent to XBee")    
#     # ser.flush()
#     # ser.close()
# except Exception as e:
#     print("Failed to send message:", e)