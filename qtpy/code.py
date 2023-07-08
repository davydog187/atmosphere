import board
import audiobusio
import displayio
import time
import analogio
import pwmio
import adafruit_motor.motor
import busio
import time
import board
import busio
import adafruit_mcp9600
from adafruit_motor import servo
import adafruit_bno055
import adafruit_bme680
import adafruit_scd4x

import os
import ipaddress
import wifi
import socketpool

import ssl
import adafruit_requests

print()
print("Connecting to WiFi")

#  connect to your SSID
wifi.radio.connect("PineapplePalace", "diamonddoge")

print("Connected to WiFi")

pool = socketpool.SocketPool(wifi.radio)

#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)

#  pings Google
ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))

requests = adafruit_requests.Session(pool, ssl.create_default_context())

# print(requests.get(url).text)



# https://learn.adafruit.com/improve-brushed-dc-motor-performance/circuitpython-code-examples

# pwm_a0 = pwmio.PWMOut(board.A0, frequency=50)
# pwm_a1 = pwmio.PWMOut(board.A1, frequency=50)
# motor = adafruit_motor.motor.DCMotor(pwm_a0, pwm_a1)
# motor.decay_mode = adafruit_motor.motor.SLOW_DECAY


i2c = board.STEMMA_I2C()

bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
scd4x = adafruit_scd4x.SCD4X(i2c)

scd4x.start_periodic_measurement()

def sample_sensors():
    return {
        'bme680': {
            'temperature': bme680.temperature,
            'gas': bme680.gas,
            'humidity': bme680.humidity,
            'pressure': bme680.pressure,
        },
        'scd4x': {
        'co2': scd4x.CO2,
        'temperature': scd4x.temperature,
        'relative_humidity': scd4x.relative_humidity,
        }
    }

def loop():
    if scd4x.data_ready:
        data = sample_sensors()
        requests.post(url="http://192.168.50.14:4000/api/ingest", json=data)
        print(data)
    else:
        print("Device not ready")

while True:
    try:
        loop()
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

# sensor = adafruit_bno055.BNO055_I2C(i2c)

# pwm_a0 = pwmio.PWMOut(board.A0, duty_cycle=2 ** 15, frequency=50)
# servo_a0 = servo.Servo(pwm_a0, min_pulse = 500, max_pulse = 2500)

# pwm_a1 = pwmio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=50)
# servo_a1 = servo.Servo(pwm_a1, min_pulse = 500, max_pulse = 2500)

# while True:
#     (x, y, z) = sensor.euler
#     y = int(y) + 90
#     z = int(z) + 90
#     if z > 180: z = 180
#     if y > 180: y = 180
#     if z < 0: z = 0
#     if y < 0: y = 0
#     print(y, z)
#     servo_a0.angle = y
#     servo_a1.angle = z
#     # time.sleep(0.1)



# while True:
#     motor.throttle = -1
#     time.sleep(5)
#     motor.throttle = 0
#     time.sleep(5)


# i2c = busio.I2C(board.SCL1, board.SDA1, frequency=100000)
# i2c = board.STEMMA_I2C()




# uart = busio.UART(board.TX, board.RX, baudrate=9600)
# while True:
#     if uart.in_waiting > 0:
#         # print(uart.in_waiting)
#         data = uart.read(uart.in_waiting)
#         # print(data)  # this is a bytearray type
#         if data is not None:
#             data_string = ''.join([chr(b) for b in data])
#             print(data_string, end="")


# mcp = adafruit_mcp9600.MCP9600(i2c)

# while True:
#     temp_c = mcp.temperature
#     temp_f = temp_c * 9 / 5 + 32
#     print([temp_c, temp_f])
#     time.sleep(0.2)
