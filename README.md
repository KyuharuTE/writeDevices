# writeDevices 脚本说明

## 概述

`writeDevices.py` 脚本用于在设备上写入镜像文件。支持两种模式：`fastboot` 和 `sideload`。脚本会检查设备状态，并根据指定的模式执行相应的操作。

## 依赖

- Python 3.x
- `os` 模块
- `re` 模块
- `checkDevices` 模块（假设包含 `Device` 类）

## 函数说明

### `checkMode(mode: str, device: Device) -> bool`

检查设备是否处于指定模式。

- `mode`: 要检查的模式，可以是 `"fastboot"` 或 `"sideload"`。
- `device`: 要检查的设备对象。

返回值：
- `True`: 如果设备处于指定模式。
- `False`: 如果设备不处于指定模式或设备为 `None`。

### `writeDevices(part: str, imgPath: str, mode: str = "fastboot", device: Device = None) -> int`

向设备写入镜像文件。

- `part`: 要写入的设备分区。
- `imgPath`: 镜像文件的路径。
- `mode`: 写入模式，可以是 `"fastboot"` 或 `"sideload"`，默认为 `"fastboot"`。
- `device`: 要写入的设备对象，默认为 `None`。

返回值：
- `0`: 成功写入。
- `-1`: 设备未处于指定模式。
- `-2`: 写入失败。
- `-3`: 镜像文件不存在。
- `-4`: 无效的模式。

## 使用示例

```python
if __name__ == "__main__":
    devices = checkDevices(None, None)
    if devices and len(devices) > 0:
        device = devices[0]
        print(device.status)
        print(writeDevices("boot", r"D:\Users\Desktop\Mindows工具箱V8\bin\res\perseus\woa\uefi-common.img", "fastboot", device))
    else:
        print("No devices found.")
```

## 注意事项
- 确保设备处于正确的模式（fastboot 或 sideload）。
- 确保镜像文件路径正确且文件存在。
- 脚本使用 os.popen 执行命令，请确保系统环境配置正确