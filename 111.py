import wmi

def get_cpu_temperature():
    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
    temperature_info = w.Sensor()
    temperatures = {}
    for sensor in temperature_info:
        if sensor.SensorType == u'Temperature':
            temperatures[sensor.Name] = sensor.Value
    return temperatures

cpu_temperatures = get_cpu_temperature()
print(cpu_temperatures)