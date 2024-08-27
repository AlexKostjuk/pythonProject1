
import time
import wmi
import socket

def get_all_sensors():
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        sensor_info = w.Sensor()
        sensors = {}
        for sensor in sensor_info:
            sensors[sensor.Name] = {
                "Type": sensor.SensorType,
                "Value": sensor.Value,
                "Min": sensor.Min,
                "Max": sensor.Max
            }
        return sensors
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return {}

def get_computer_name():
    try:
        return socket.gethostname()
    except Exception as e:
        print(f"Ошибка при получении имени компьютера: {e}")
        return "Unknown"



def compare_and_update_nested_dicts(main_dict1, main_dict2):
    updated_dict = main_dict1.copy()

    for key in updated_dict.keys():
        if key in main_dict2:
            nested_dict1 = updated_dict[key]
            nested_dict2 = main_dict2[key]

            for nested_key in nested_dict1.keys():
                if nested_key in nested_dict2 and nested_dict2[nested_key] > nested_dict1[nested_key]:
                    nested_dict1[nested_key] = nested_dict2[nested_key]

    return updated_dict

all_sensors = get_all_sensors()
computer_name = get_computer_name()
# Початкові словники
main_dict1 = get_all_sensors()

main_dict2 = {}



data = {
    "ComputerName": computer_name,
    "Sensors": all_sensors
}

print(all_sensors)

# Невідомо, як часто змінюється main_dict2, тому імітуємо це в циклі
while True:
    main_dict2= get_all_sensors()
    main_dict1 = compare_and_update_nested_dicts(main_dict1, main_dict2)
    print(main_dict1)  # Виводимо оновлений словник

    # Тут можна додати зміну main_dict2, якщо це необхідно для тестування
    # Наприклад, для тесту можна змінювати значення в main_dict2 на кожній ітерації:

    # Невелика пауза, щоб уникнути надмірного використання процесора
    time.sleep(2)

