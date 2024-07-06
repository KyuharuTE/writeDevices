import os, re
from checkDevices import *

def checkMode(mode : str, device : Device):
    if device is None:
        return False
    if hasattr(device, 'status') and device.status == mode:
        return True
    else:
        return False

def writeDevices(part : str, imgPath : str, mode : str = "fastboot", device : Device = None):
    if device is None:
        adb = ".\\src\\platform-tools\\adb.exe"
        fastboot = ".\\src\\platform-tools\\fastboot.exe"
    else:
        adb = f".\\src\\platform-tools\\adb.exe -s {device.name}"
        fastboot = f".\\src\\platform-tools\\fastboot.exe -s {device.name}"

    patterns = [
        r'failure',
        r'FAILURE',
        r'Failure',
        r'unknow',
        r'Unknow',
        r'UNKNOW'
    ]
    combined_pattern = '|'.join(patterns)

    if not os.path.exists(imgPath):
        return -3 # Image not found
    
    if mode == "fastboot":
        if not checkMode("fastboot", device):
            return -1 # Device not in fastboot mode
        
        out = os.popen(f"{fastboot} flash {part} {imgPath}").read()
        if re.search(combined_pattern, out, re.IGNORECASE):
            return -2 # Failed to flash
        else:
            return 0 # Success
    
    elif mode == "sideload":
        if not checkMode("sideload", device):
            return -1 # Device not in sideload mode
        
        out = os.popen(f"{adb} sideload {imgPath}").read()
        if re.search(combined_pattern, out, re.IGNORECASE):
            return -2 # Failed to sideload
        else:
            return 0 # Success
    else:
        return -4 # Invalid mode

if __name__ == "__main__":
    devices = checkDevices(None, None)
    if devices and len(devices) > 0:
        device = devices[0]
        print(device.status)
        print(writeDevices("boot", r"D:\Users\Desktop\Mindows工具箱V8\bin\res\perseus\woa\uefi-common.img", "fastboot", device))
    else:
        print("No devices found.")
