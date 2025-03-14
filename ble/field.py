
import asyncio
from bleak import BleakScanner, BleakClient, BleakGATTServiceCollection, BLEDevice
import keyboard
import globals
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def notification_handler(sender, data):
    globals.force = int(data.decode('utf-8').strip('\x00')[:-1]) - globals.tare
    log.info(f"The Smart Instrument Registered {globals.force} Newtons")

# scan all available devices then select the Smart Instrument
async def get_device():
    deviceNo = -1
    devices = await BleakScanner.discover()

    while deviceNo == -1:
        for index, d in enumerate(devices):
            log.info(d.name)
            if (d.name == globals.DEVICE_NAME):
                deviceNo = index
                return d
        if deviceNo != -1:
            break
        log.info(f"No '{globals.DEVICE_NAME}' Devices Found. Attempting Reconnection in 5 Seconds")
        await asyncio.sleep(5)
        devices = await BleakScanner.discover()
    
    return devices[deviceNo]

def set_tar():
    globals.tare = 0 if (globals.force < 0) else globals.force

    log.info(f"TARE SET TO {globals.tare} Newtons")

def handle_disconnect(client: BleakClient):
    log.info("Device disconnected!")
    globals.is_connected = False

async def get_notif(device: BLEDevice):
    async with BleakClient(device.address, disconnected_callback=handle_disconnect) as client:
        log.info(f"Connected to {device.name} ({device.address})")

        globals.is_connected = True
        await client.start_notify(globals.MEASUREMENT_DATA_CHARACTERISTIC_UUID, lambda sender, data: notification_handler(sender, data))
        
        try:
            while  globals.is_connected:
                if not client.is_connected:
                    log.info("Device isn't connected anymore")
                    break
        except Exception as e:
            log.warning(f"BLE ERROR: {e}")
        finally:
            if client.is_connected:
                await client.stop_notify(globals.MEASUREMENT_DATA_CHARACTERISTIC_UUID)
                await client.disconnect()

        # Stop notifications before exiting
        globals.is_connected = False
        await client.stop_notify(globals.MEASUREMENT_DATA_CHARACTERISTIC_UUID)

async def connect_to_device(device: BLEDevice):
    async with BleakClient(device, disconnected_callback=handle_disconnect) as client:
        log.info(f"Connected to {device.name} ({device.address})")

        globals.is_connected = True

        try:
            # data = await client.read_gatt_char(globals.MEASUREMENT_DATA_CHARACTERISTIC_UUID)
            # globals.tare = int(data.decode('utf-8').strip('\x00')[:-1])
            # log.info(f"TARE SET TO {globals.tare} Newtons")

            # voltage_data = await client.read_gatt_char(globals.ADC_VOLTAGE_CHARACTERISTIC_UUID)
            # log.info(f"RAW VOLTAGE READ : {voltage_data}")
            # globals.voltage_data = int(''.join(filter(str.isdigit, voltage_data.decode('utf-8').strip('\x00') )))
            # log.info(f"TRANSFORMED VOLTAGE READ : {globals.voltage_data}")

            #log.info(f"VOLTAGE TARE SET TO {globals.voltage_data} Newtons")

            while globals.is_connected:
                if not client.is_connected:
                    log.info("Device isn't connected anymore")
                    break
                data = await client.read_gatt_char(globals.MEASUREMENT_DATA_CHARACTERISTIC_UUID)
                print(f"READ DATA: {data}")
                print(f"READ DATA UTF 8: {data.decode('utf-8')}")
                globals.force = int(data.decode('utf-8').strip('\x00')[:-1]) - globals.tare
                globals.force = globals.force - (globals.force % 5)
                log.info(f"\nThe Smart Instrument Registered {globals.force} Newtons")

                voltage_data = await client.read_gatt_char(globals.ADC_VOLTAGE_CHARACTERISTIC_UUID)
                globals.voltage = int(''.join(filter(str.isdigit, voltage_data.decode('utf-8').strip('\x00') )))
                log.info(f"The Smart Instrument Registered : {globals.voltage} mV")

                await asyncio.sleep(0.05)
            
        except Exception as e:
            log.warning(f"BLE ERROR: {e}")
        finally:
            if client.is_connected:
                await client.disconnect()

async def field_data_retrieval():
    loop = asyncio.get_event_loop()
    log.info("Searching available devices...")
    keyboard.add_hotkey('space', set_tar)
    device = await get_device()

    def reconnect():
        future = asyncio.run_coroutine_threadsafe(connect_to_device(device), loop)
        def future_callback(f):
            if f.cancelled():
                log.warning("Reconnect task was cancelled.")
            elif f.exception():
                log.warning(f"Reconnect result: {f.exception()}")
            else:
                log.info("Reconnect successful.")

        future.add_done_callback(future_callback)
    keyboard.add_hotkey('r', lambda: loop.call_soon_threadsafe(reconnect))
    
    await connect_to_device(device)
