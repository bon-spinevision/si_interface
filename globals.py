from dotenv import load_dotenv
import os

def init():
    load_dotenv()

    global FIELD_SERVICE_UUID
    FIELD_SERVICE_UUID= os.getenv("FIELD_SERVICE_UUID")

    global MEASUREMENT_DATA_CHARACTERISTIC_UUID
    MEASUREMENT_DATA_CHARACTERISTIC_UUID = os.getenv("MEASUREMENT_DATA_CHARACTERISTIC_UUID")

    global ADC_VOLTAGE_CHARACTERISTIC_UUID
    ADC_VOLTAGE_CHARACTERISTIC_UUID = os.getenv("ADC_VOLTAGE_CHARACTERISTIC_UUID")

    global DEVICE_NAME
    DEVICE_NAME = os.getenv("DEVICE_NAME")

    global tare
    tare = 0

    global force
    force = 0

    global voltage
    voltage = 0

    global voltage_tare
    voltage_tare = 0

    global is_connected
    is_connected = False

    global message
    message = ""
    