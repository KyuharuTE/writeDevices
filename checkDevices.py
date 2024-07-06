import os

adb = ".\\src\\platform-tools\\adb.exe"
fastboot = ".\\src\\platform-tools\\fastboot.exe"

class Device:
    def __init__(self, name, status):
        self.name = name
        self.status = status

def checkDevices(mode=None, maxDevices=None, needList=True):
    os.popen(f"{adb} start-server")
    out = os.popen(f"{adb} devices").read()
    devices = out.split("\n")[1:-1]
    devicesList = []
    if len(devices) != 0:
        for device in devices:
            try:
                name = device.split("\t")[0]
                status = device.split("\t")[1]
                devicesList.append(Device(name, status))
            except IndexError:
                continue

    out = os.popen(f"{fastboot} devices").read()
    fastbootDevices = [device for device in out.split("\n") if device.strip()]
    if len(fastbootDevices) != 0:
        hasT = False
        if fastbootDevices[0].find("\t") != -1:
            hasT = True

        if hasT:
            for device in fastbootDevices:
                parts = device.split("\t")
                if len(parts) == 2:
                    name = parts[0]
                    status = parts[1]
                    if status.find(" ") != -1:
                        status = status.split(" ")[1]
                    devicesList.append(Device(name, status))

    if len(devicesList) == 0:
        return "-1"  # No devices found

    if maxDevices is not None and len(devicesList) > maxDevices:
        return "-2"  # Too many devices found

    if mode is not None:
        passDevices = [device for device in devicesList if device.status == mode]
        if len(passDevices) == 0:
            if needList:
                return devicesList
            else:
                return 0  # No passDevices found
        else:
            if needList:
                return passDevices
            else:
                return 1  # PassDevices found
    else:
        if needList:
            return devicesList
        else:
            return len(devicesList)  # All devices found

if __name__ == "__main__":
    devices = checkDevices(None, None, True)
    for device in devices:
        print(device.name, device.status)

    devices = checkDevices("device", None, True)
    for device in devices:
        print(device.name, device.status)

    devices = checkDevices("offline", None, False)
    print(devices)
